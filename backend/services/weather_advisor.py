import time
from typing import List
from ..schemas.weather_schemas import (
    WeatherAdvisoryRequest,
    WeatherAdvisoryResponse,
    SafetyProtocol
)

def generate_weather_advisory(request: WeatherAdvisoryRequest) -> WeatherAdvisoryResponse:
    """Generate dynamic construction site safety protocols and engineering directives based on weather."""
    cond = request.condition.lower()
    phase = request.site_phase
    temp = request.temperature_celsius or 32.0
    wind = request.wind_speed_kmh or 20.0

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
    protocols: List[SafetyProtocol] = []
    emergency_checklist: List[str] = []

    if "wind" in cond or wind >= 45:
        risk_level = "High"
        operational_status = "Restricted Operations (Cranes Suspended)"
        headline = f"GALE WARNING: High Wind Speeds ({wind:.0f} km/h) Detected - Immediate Crane & Height Restrictions Active"

        protocols.append(SafetyProtocol(
            category="Crane & Lifting",
            action_level="HALT OPERATION",
            protocol_title="Mandatory Tower Crane Shutdown & Weathervaning",
            detailed_procedure=(
                "Immediately dog off and lower all suspended loads to the deck. Disengage slew brakes to allow the "
                "jib to free-wheel (weathervane) with wind direction, preventing structural mast twist. "
                "Lock trolley at minimum radius per manufacturer guidelines."
            ),
            code_reference="OSHA 1926.1431 / IS 13367 (Safe Use of Cranes)"
        ))
        protocols.append(SafetyProtocol(
            category="Scaffolding & Heights",
            action_level="RESTRICTED PROTOCOL",
            protocol_title="Suspended Cradle & Edge Work Evacuation",
            detailed_procedure=(
                "Ground all rope-access window cleaning and exterior scaffolding cradles immediately. Inspect and double-latch "
                "all perimeter debris netting, loose formwork panels, and plywood sheeting to prevent airborne projectiles."
            ),
            code_reference="IS 4014 (Code of Practice for Steel Scaffolding)"
        ))
        protocols.append(SafetyProtocol(
            category="Worker Welfare & PPE",
            action_level="ENHANCED MONITORING",
            protocol_title="Mandatory Chinstrap & Eye Protection Enforcement",
            detailed_procedure="Enforce 3-point chinstraps on all safety helmets to prevent dislodgement in gusts. Issue wrap-around safety spectacles.",
            code_reference="IS 2925 / OSHA 1926.100"
        ))

        emergency_checklist = [
            "Weathervane all tower crane jibs and park hook blocks at minimum radius.",
            "Lash down loose formwork sheets, insulation boards, and metal roof purlins.",
            "Evacuate personnel from perimeter scaffolding tiers above 15 meters.",
            "Inspect perimeter hoarding and temporary signboards along site boundary."
        ]
        concrete_curing = "High wind accelerates plastic surface drying. Apply aliphatic evaporative retarder or fog spray immediately after screeding."
        crane_lifting = "HALTED: Zero lifting operations permitted while wind gusts exceed 38 km/h (20 knots)."
        worker_shift = "Restrict exterior high-elevation tasks; reassign labor to sheltered interior MEP works."

    elif "rain" in cond or "monsoon" in cond:
        risk_level = "High"
        operational_status = "Restricted Operations (Dewatering & Electrical Alert)"
        headline = "MONSOON DIRECTIVE: Heavy Precipitation - Electrical Safety, Dewatering & Trench Stability Protocols"

        protocols.append(SafetyProtocol(
            category="Electrical & Grounding",
            action_level="HALT OPERATION",
            protocol_title="Temporary Power De-energization in Standing Water",
            detailed_procedure=(
                "De-energize all non-essential temporary supply panels located in basements or open areas. "
                "Test Residual Current Devices (RCDs) / ELCBs; ensure all supply lines are lifted on insulated stands at least 450mm above grade."
            ),
            code_reference="IS 732 / OSHA 1926.404"
        ))
        protocols.append(SafetyProtocol(
            category="Excavation & Shoring",
            action_level="RESTRICTED PROTOCOL",
            protocol_title="Trench Slope Saturation & Sump Dewatering",
            detailed_procedure=(
                "Station continuous submersible dewatering pumps in deep basement sumps. Inspect soil nailing and soldier piles for hydrostatic "
                "buildup. Zero personnel permitted in un-shored excavations exceeding 1.2m depth."
            ),
            code_reference="IS 3764 (Safety in Excavation Work)"
        ))
        protocols.append(SafetyProtocol(
            category="Concrete Curing & Chemistry",
            action_level="RESTRICTED PROTOCOL",
            protocol_title="Rain Protection for Fresh Concrete Placements",
            detailed_procedure=(
                "Suspend fresh slab pours unless fully sheltered. If rain begins mid-pour, erect polyethylene rain shelters immediately. "
                "Do NOT trowel rainwater into fresh concrete surface (prevents weak dusting layer). Conduct slump tests on all RMC transit mixers."
            ),
            code_reference="IS 456:2000 Clause 13.3"
        ))

        emergency_checklist = [
            "Verify all diesel and electric dewatering sump pumps are primed with backup generators.",
            "Inspect basement retaining walls and earth berms for signs of sloughing or cracking.",
            "Cover cement godowns with double-layered waterproof tarpaulins on raised timber dunnage.",
            "Halt all hot-works and external arc welding in exposed damp zones."
        ]
        concrete_curing = "Protect freshly cast slabs with heavy 250-micron poly sheeting. Adjust batching plant water-cement ratio to compensate for aggregate moisture."
        crane_lifting = "Operate with extreme caution; check outrigger ground bearing plates for mud subsidence."
        worker_shift = "Issue waterproof gumboots and high-visibility rain suits. Ensure covered dry walkways."

    elif "heat" in cond or temp >= 40:
        risk_level = "Moderate"
        operational_status = "Enhanced Heat-Stress & Concrete Hydration Protocols"
        headline = f"HEATWAVE PROTOCOL: Extreme Ambient Temperature ({temp:.0f}°C) - Hydration & Slag Curing Controls Active"

        protocols.append(SafetyProtocol(
            category="Worker Welfare & PPE",
            action_level="RESTRICTED PROTOCOL",
            protocol_title="Heat Stress Work-Rest Regimen & Electrolyte Stations",
            detailed_procedure=(
                "Institute a 45-minute work / 15-minute shaded rest cycle. Provide chilled potable water enriched with ORS electrolytes. "
                "Train site supervisors to identify early symptoms of heat exhaustion, cramping, and syncope."
            ),
            code_reference="OSHA Heat Illness Prevention / Factory Act Guidelines"
        ))
        protocols.append(SafetyProtocol(
            category="Concrete Curing & Chemistry",
            action_level="RESTRICTED PROTOCOL",
            protocol_title="Hot-Weather Concreting & Continuous Wet Ponding",
            detailed_procedure=(
                "Shift major slab pours to night shift (6:00 PM to 6:00 AM) or early dawn. Dose batching water with flake ice to maintain placement "
                "temperature under 32°C. Initiate continuous wet hessian ponding within 20 minutes of initial set to stop rapid drying shrinkage."
            ),
            code_reference="IS 456:2000 Clause 14.1 & IS 7861 Part 1 (Hot Weather Concreting)"
        ))
        protocols.append(SafetyProtocol(
            category="Scaffolding & Heights",
            action_level="STANDARD",
            protocol_title="Reflective Shading & Thermal Surface Inspection",
            detailed_procedure="Inspect steel handrails and formwork surfaces before handling; require leather palm work gloves to prevent contact burns.",
            code_reference="OSHA 1926.28"
        ))

        emergency_checklist = [
            "Stock 500 liters of electrolyte-fortified water at every stair core and staging deck.",
            "Ensure concrete curing burlap is kept continuously saturated (zero dry spots).",
            "Monitor slump loss in transit mixers; keep retarder admixtures ready on standby.",
            "Reschedule high-exertion manual rebar carting away from solar noon."
        ]
        concrete_curing = "Mandatory continuous ponding/hessian curing for minimum 14 days (IS 456 Clause 13.5.1 for hot dry environments). Use curing compound as secondary barrier."
        crane_lifting = "Normal operation; monitor hydraulic oil temperatures on crane power packs."
        worker_shift = "Split shift model: Morning 06:00 - 11:30, Evening 15:30 - 19:30."

    elif "storm" in cond or "lightning" in cond:
        risk_level = "Critical"
        operational_status = "Complete Work Stoppage (Lightning Stand-Down)"
        headline = "LIGHTNING DETECTED: Severe Thunderstorm Imminent - Immediate Site Evacuation to Hard Shelters"

        protocols.append(SafetyProtocol(
            category="Worker Welfare & PPE",
            action_level="HALT OPERATION",
            protocol_title="30-30 Lightning Rule Mandatory Evacuation",
            detailed_procedure=(
                "When lightning-to-thunder interval falls below 30 seconds, immediately clear all personnel from roofs, tower cranes, "
                "scaffolding, and steel erection decks. Shelter in enclosed concrete or steel structures. Remain sheltered 30 mins after last thunder."
            ),
            code_reference="NFPA 780 / IS 2309 (Lightning Protection of Buildings)"
        ))
        emergency_checklist = [
            "Order all tower crane operators down the mast immediately.",
            "Disconnect all sensitive laser leveling instruments and survey total stations.",
            "Clear open ground and scaffold bays."
        ]
        concrete_curing = "Cover open pours with tarpaulins and evacuate deck."
        crane_lifting = "SHUT DOWN IMMEDIATELY."
        worker_shift = "All personnel muster in ground floor dining or basement shelter."

    else:
        risk_level = "Low"
        operational_status = "Normal Construction Operations"
        headline = "FAVORABLE WEATHER: Optimal Ambient Conditions - Full Production Throughput Authorized"

        protocols.append(SafetyProtocol(
            category="Crane & Lifting",
            action_level="STANDARD",
            protocol_title="Routine Heavy Rigging & Tandem Lifts",
            detailed_procedure="Proceed with scheduled structural steel framing, precast panel erection, and rebar bundle hoisting per lift plan.",
            code_reference="IS 13367"
        ))
        protocols.append(SafetyProtocol(
            category="Concrete Curing & Chemistry",
            action_level="STANDARD",
            protocol_title="Standard 7-Day Moist Curing Cycle",
            detailed_procedure="Maintain routine wet burlap covering or certified liquid membrane curing per IS 456 Clause 13.5.",
            code_reference="IS 456:2000"
        ))

        emergency_checklist = [
            "Daily pre-shift visual inspection of wire ropes and slings.",
            "Toolbox safety briefing on active phase hazards.",
            "Verify clear fire egress paths across all active floors."
        ]
        concrete_curing = "Standard IS 456 moist curing for OPC (minimum 7 days) and PPC/Fly-ash blends (minimum 10 days)."
        crane_lifting = "Unrestricted within rated load charts and designated slewing zones."
        worker_shift = "Standard 8-hour construction shift."

    return WeatherAdvisoryResponse(
        timestamp=timestamp,
        condition=request.condition,
        site_phase=phase,
        risk_level=risk_level,
        operational_status=operational_status,
        weather_headline=headline,
        safety_protocols=protocols,
        emergency_checklist=emergency_checklist,
        concrete_curing_advisory=concrete_curing,
        crane_lifting_advisory=crane_lifting,
        worker_shift_advisory=worker_shift
    )
