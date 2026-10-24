import os
import sys
import time
from fastapi import APIRouter
from ..config import PLATFORM_ID, PLATFORM_NAME, PLATFORM_VERSION, GEMINI_API_KEY, DEFAULT_GEMINI_MODEL

router = APIRouter(prefix="/api", tags=["System Health & Samples"])

START_TIME = time.time()

# Small 1x1 or SVG/dataURI base placeholders for instant 1-click testing
SAMPLE_PRESETS = {
    "safety_scenarios": [
        {
            "id": "sample-safety-1",
            "title": "High-Rise Concrete Deck & Edge Framing",
            "context": "Active 14th floor deck slab formwork with rebar tie operations and tower crane hook transfer.",
            "expected_focus": "Fall protection harnesses, edge guardrails, hard hats, safety boots under OSHA 1926 & IS 456.",
            "demo_image_type": "high_risk"
        },
        {
            "id": "sample-safety-2",
            "title": "Excavation Pit & Shoring Laydown Zone",
            "context": "Foundation excavation pit depth 4.5m with soil nails and transit mixer unloading bay.",
            "expected_focus": "High-vis vest conspicuity around heavy mobile plant, trench edge barriers, IS 2925 helmets.",
            "demo_image_type": "compliant"
        }
    ],
    "crack_scenarios": [
        {
            "id": "sample-crack-shear",
            "title": "45° Diagonal Shear Crack in RCC Transfer Girder",
            "context": "Diagonal crack propagating at 45 degrees near support of 600mm deep reinforced concrete transfer beam.",
            "expected_defect": "Structural Shear Crack",
            "severity": "Severe"
        },
        {
            "id": "sample-crack-settlement",
            "title": "Stepped Masonry Settlement Crack at Plinth",
            "context": "Stepped diagonal crack through mortar joints on external load-bearing brick wall near corner.",
            "expected_defect": "Settlement Crack",
            "severity": "Severe"
        },
        {
            "id": "sample-crack-hairline",
            "title": "Plastic Shrinkage Hairline Craze on Slab Soffit",
            "context": "Fine random shallow surface map cracking on fresh concrete slab top face following high-wind day.",
            "expected_defect": "Hairline Crack",
            "severity": "Low"
        },
        {
            "id": "sample-crack-spalling",
            "title": "Rebar Corrosion Delamination & Spalled Cover",
            "context": "Cover concrete spalled with visible rusted longitudinal reinforcement bars on basement column.",
            "expected_defect": "Spalling & Delamination",
            "severity": "Moderate"
        }
    ],
    "valuation_presets": [
        {
            "name": "Luxury Residential High-Rise (Mumbai)",
            "structure_type": "Residential High-Rise",
            "built_up_sqft": 120000,
            "location_tier": "Tier 1 (Mumbai, Delhi-NCR, Bengaluru)",
            "completion_percentage": 65,
            "construction_grade": "Luxury"
        },
        {
            "name": "Commercial Tech Park Campus (Bengaluru)",
            "structure_type": "Commercial Complex",
            "built_up_sqft": 250000,
            "location_tier": "Tier 1 (Mumbai, Delhi-NCR, Bengaluru)",
            "completion_percentage": 40,
            "construction_grade": "Premium"
        },
        {
            "name": "Gated Villa Development (Pune)",
            "structure_type": "Villa / Row House",
            "built_up_sqft": 45000,
            "location_tier": "Tier 2 (Pune, Hyderabad, Ahmedabad, Chennai)",
            "completion_percentage": 85,
            "construction_grade": "Premium"
        }
    ]
}

@router.get("/health", summary="Get system status and AI connectivity")
async def get_health():
    uptime_seconds = round(time.time() - START_TIME, 1)
    gemini_ready = bool(GEMINI_API_KEY and len(GEMINI_API_KEY.strip()) > 5)

    return {
        "status": "online",
        "platform_id": PLATFORM_ID,
        "platform_name": PLATFORM_NAME,
        "version": PLATFORM_VERSION,
        "python_version": sys.version.split()[0],
        "uptime_seconds": uptime_seconds,
        "gemini_api_configured": gemini_ready,
        "gemini_model": DEFAULT_GEMINI_MODEL,
        "demonstration_mode_active": not gemini_ready,
        "supported_epics": [
            "Epic 1: Requirements & Development Environment",
            "Epic 2: PPE Safety Vision & Crack Diagnostics",
            "Epic 3: Project Planning & Real Estate Valuation",
            "Epic 4: Multimodal AI & Strict JSON Contracts",
            "Epic 5: Daily Site Chatbot & Weather Advisory",
            "Epic 6: Interface, Testing & Deployment"
        ]
    }

@router.get("/sample-data", summary="Retrieve preset scenarios and sample prompts")
async def get_sample_data():
    return SAMPLE_PRESETS
