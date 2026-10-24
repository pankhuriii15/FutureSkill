import io
from PIL import Image
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def create_test_image(color=(200, 150, 80), size=(300, 200), format="JPEG") -> bytes:
    """Generate a clean test image in memory."""
    buf = io.BytesIO()
    img = Image.new("RGB", size, color=color)
    img.save(buf, format=format)
    return buf.getvalue()

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert data["platform_id"] == "6ac4c98d1dcde6d7857c1642"
    assert "version" in data
    assert len(data["supported_epics"]) == 6

def test_sample_data_endpoint():
    response = client.get("/api/sample-data")
    assert response.status_code == 200
    data = response.json()
    assert "safety_scenarios" in data
    assert "crack_scenarios" in data
    assert "valuation_presets" in data

def test_valuation_calculation_tier1():
    payload = {
        "structure_type": "Residential High-Rise",
        "built_up_sqft": 100000,
        "location_tier": "Tier 1 (Mumbai, Delhi-NCR, Bengaluru)",
        "completion_percentage": 50,
        "construction_grade": "Premium"
    }
    response = client.post("/api/calculate-valuation", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["platform_id"] == "6ac4c98d1dcde6d7857c1642"
    assert data["total_project_budget_inr"] > 0
    assert "Crores" in data["total_budget_formatted"] or "Lakhs" in data["total_budget_formatted"]
    assert data["capex_incurred_inr"] == data["total_project_budget_inr"] * 0.5
    assert data["materials"]["cement_bags"] == 40000
    assert data["materials"]["steel_tonnes"] == 420.0
    assert len(data["milestones"]) == 5
    assert "pollinations.ai" in data["architectural_image_url"]

def test_valuation_validation_errors():
    # Negative sqft
    response = client.post("/api/calculate-valuation", json={
        "structure_type": "Villa / Row House",
        "built_up_sqft": -500,
        "location_tier": "Tier 2",
        "completion_percentage": 20,
        "construction_grade": "Standard"
    })
    assert response.status_code == 422 or response.status_code == 400

    # Completion pct > 100
    response = client.post("/api/calculate-valuation", json={
        "structure_type": "Villa / Row House",
        "built_up_sqft": 5000,
        "location_tier": "Tier 2",
        "completion_percentage": 150,
        "construction_grade": "Standard"
    })
    assert response.status_code == 422 or response.status_code == 400

def test_weather_advisory_high_wind():
    payload = {
        "condition": "High Wind (>45 km/h)",
        "site_phase": "Structural Steel & Facade",
        "wind_speed_kmh": 52.0
    }
    response = client.post("/api/weather-advisory", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["risk_level"] == "High"
    assert "Crane" in data["operational_status"] or "Suspended" in data["operational_status"]
    # Verify tower crane shutdown protocol exists
    categories = [p["category"] for p in data["safety_protocols"]]
    assert "Crane & Lifting" in categories
    assert len(data["emergency_checklist"]) > 0

def test_weather_advisory_extreme_heat():
    payload = {
        "condition": "Extreme Heat (>40°C)",
        "site_phase": "Concrete Pouring & Curing",
        "temperature_celsius": 43.0
    }
    response = client.post("/api/weather-advisory", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "IS 456" in data["concrete_curing_advisory"] or "curing" in data["concrete_curing_advisory"].lower()

def test_audit_safety_endpoint_valid():
    img_bytes = create_test_image()
    response = client.post(
        "/api/audit-safety",
        files={"file": ("site.jpg", img_bytes, "image/jpeg")},
        data={"notes": "High-risk elevated scaffold inspection"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "safety_score" in data
    assert 0 <= data["safety_score"] <= 100
    assert "overall_status" in data
    assert len(data["ppe_checklist"]) > 0
    assert len(data["identified_hazards"]) > 0

def test_diagnose_crack_endpoint_valid():
    img_bytes = create_test_image(color=(180, 180, 180))
    response = client.post(
        "/api/diagnose-crack",
        files={"file": ("crack.jpg", img_bytes, "image/jpeg")},
        data={"notes": "45 degree diagonal shear crack in beam web"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "defect_type" in data
    assert data["estimated_crack_width_mm"] > 0
    assert len(data["recommended_engineering_repairs"]) > 0
    assert len(data["repair_steps"]) > 0

def test_edge_case_corrupted_image():
    # Sending invalid bytes with image mime type
    bad_bytes = b"This is not a real JPEG image file, corrupted bytes."
    response = client.post(
        "/api/audit-safety",
        files={"file": ("corrupt.jpg", bad_bytes, "image/jpeg")},
        data={"notes": "Testing corrupted upload"}
    )
    assert response.status_code in [400, 422]

def test_edge_case_non_image_file():
    text_bytes = b"Text file contents"
    response = client.post(
        "/api/audit-safety",
        files={"file": ("doc.txt", text_bytes, "text/plain")},
        data={"notes": "Testing text upload"}
    )
    assert response.status_code == 400

def test_edge_case_empty_file():
    response = client.post(
        "/api/audit-safety",
        files={"file": ("empty.jpg", b"", "image/jpeg")},
        data={"notes": "Testing zero byte upload"}
    )
    assert response.status_code == 400

def test_site_chat_endpoint():
    response = client.post(
        "/api/site-chat",
        json={
            "messages": [
                {"role": "user", "content": "What is the stripping time of formwork for beam props spanning 5 meters under IS 456?"}
            ],
            "site_context": "Site B, RCC Column Framing"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "reply" in data
    assert "14 days" in data["reply"] or "IS 456" in data["reply"]
    assert len(data["references"]) > 0
