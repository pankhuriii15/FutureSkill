import io
import time
import uuid
from typing import Optional, Dict, Any
from PIL import Image

from ..schemas.crack_schemas import CrackDiagnosisResponse
from .gemini_service import GeminiMultimodalClient
from .prompt_templates import CRACK_DIAGNOSIS_PROMPT

def generate_fallback_crack_diagnosis(image_bytes: bytes, context: Optional[str] = None) -> CrackDiagnosisResponse:
    """Generate engineering-grade structural crack diagnostics for demonstration and offline mode."""
    ctx_lower = (context or "").lower()

    if "shear" in ctx_lower or "diagonal" in ctx_lower or "beam" in ctx_lower:
        defect_type = "Structural Shear Crack"
        confidence = 94.8
        width = 3.4
        depth = "Through-Section"
        severity = "Severe"
        urgency = "Immediate (Stop Work)"
        surface = "Reinforced Cement Concrete (RCC) Transfer Girder"
        causes = [
            "Excessive principal tensile stress exceeding concrete shear capacity (IS 456 Clause 40.1)",
            "Inadequate shear stirrup spacing / shear link density near support",
            "Superimposed dead load exceeding initial design assumptions",
            "Thermal differential strain causing shear stress concentration"
        ]
        integrity_risk = "CRITICAL STRUCTURAL RISK: Diagonal tension crack propagating at 45° angle across web of reinforced concrete beam. Indicates imminent risk of brittle shear failure without significant preliminary deflection."
        standards = ["IS 456:2000 Clause 40 (Shear Reinforcement)", "ACI 318-19 Section 22.5", "ACI 224.1R-07"]
        repairs = [
            "Temporary emergency propping / Acrow jack shoring under the affected span.",
            "Pressure injection of ultra-low viscosity structural epoxy resin (ASTM C881 Type I/IV).",
            "External post-tensioned CFRP (Carbon Fiber Reinforced Polymer) composite laminates wrapped around beam web.",
            "Structural re-grouting using non-shrink high-strength micro-concrete (M60 grade)."
        ]
        steps = [
            "Install heavy-duty hydraulic or mechanical props at 1.0m centers beneath the beam.",
            "Clean crack perimeter using wire brushes and compressed oil-free air; seal surface with polyester putty.",
            "Affix injection ports at 150mm intervals along diagonal path.",
            "Inject high-modulus epoxy from lowest port upward until resin emerges from adjacent port; cap and maintain 0.4 MPa pressure.",
            "Bond bidirectional CFRP wrap (200 g/m²) over primed concrete substrate with epoxy saturant."
        ]
        monitoring = "Install 2D acrylic Tell-Tale Crack Monitoring Gauges calibrated to 0.1mm accuracy. Log daily dimensional readings for 60 days following structural remediation."

    elif "settlement" in ctx_lower or "foundation" in ctx_lower or "ground" in ctx_lower:
        defect_type = "Settlement Crack"
        confidence = 91.2
        width = 4.8
        depth = "Through-Section"
        severity = "Severe"
        urgency = "High (Repair within 7 days)"
        surface = "Load-Bearing Brick Masonry & Plinth Beam Interface"
        causes = [
            "Differential subgrade settlement due to unequal soil bearing capacity",
            "Poor soil compaction or water table fluctuation beneath shallow strip footing",
            "Plinth beam deflection resulting from local soil washout during monsoon"
        ]
        integrity_risk = "MODERATE TO SEVERE RISK: Stepped shear cracking propagating through mortar bed joints. Continued foundation movement will cause secondary diagonal distortion in floor slabs."
        standards = ["IS 1905:1987 (Structural Safety of Masonry)", "IS 456:2000 Clause 35.3.2", "IS 1080 (Shallow Foundations)"]
        repairs = [
            "Subsurface geotechnical investigation and soil compaction grouting.",
            "Foundation underpinning with micropiles or expanding polyurethane resin injection.",
            "Helical stainless-steel masonry crack stitching ties bedded in thixotropic mortar.",
            "High-tensile structural re-pointing with polymer-modified cementitious grout."
        ]
        steps = [
            "Perform core drilling at 1.2m spacing beneath plinth to inject expanding polyurethane geo-grout.",
            "Chase horizontal slots in bed joints 500mm past crack zone at 450mm vertical centers.",
            "Embed helical stainless steel reinforcement bars (6mm dia) into 2-part polymer anchoring resin.",
            "Fill stepped crack void with thixotropic micro-cement grout.",
            "Restore aesthetic surface plaster with fiber-reinforced lime-cement matrix."
        ]
        monitoring = "Deploy precision digital tiltmeters and electronic crack displacement transducers (LVDT) with automated alert thresholds for movements > 0.5mm."

    elif "spalling" in ctx_lower or "rebar" in ctx_lower or "rust" in ctx_lower or "corrosion" in ctx_lower:
        defect_type = "Spalling & Delamination"
        confidence = 96.5
        width = 6.2
        depth = "Cover Concrete Delamination"
        severity = "Moderate"
        urgency = "High (Repair within 7 days)"
        surface = "RCC Slab Soffit and Column Perimeter"
        causes = [
            "Carbonation-induced depassivation of reinforcing steel",
            "Inadequate concrete cover (<20mm) failing IS 456:2000 Table 16 durability specifications",
            "Moisture and chloride ingress generating volumetric expansion of ferric rust (up to 600% rebar volume)",
            "Honeycombing and porous concrete compaction during original pour"
        ]
        integrity_risk = "SIGNIFICANT DURABILITY RISK: Flaking concrete poses falling debris danger to personnel. Structural rebar cross-section has reduced by an estimated 10-15%, impairing tensile reserve capacity."
        standards = ["IS 456:2000 Table 16 (Nominal Cover Requirements)", "EN 1504-9 (Concrete Repair Products)", "ICRI Technical Guideline 310.1R"]
        repairs = [
            "Mechanical breakout of all unsound, carbonated hollow concrete until 20mm behind rebar is exposed.",
            "Abrasive blasting of corroded rebar to Sa 2.5 standard followed by zinc-rich anti-corrosive primer.",
            "Sacrificial zinc galvanic anode installation for cathodic protection.",
            "Application of polymer-modified shrinkage-compensated repair mortar (PMM) with bonding agent."
        ]
        steps = [
            "Delineate boundary with saw-cut 15mm deep perpendicular to surface to avoid feathered edges.",
            "Chisel concrete around rebar circumference providing minimum 20mm clean clearance.",
            "Wire-brush rebar rust to bare metal; apply two coats of active zinc-rich epoxy primer.",
            "Attach discrete zinc sacrificial anodes at 400mm intervals along rebar.",
            "Apply bonding slurry and pack polymer-modified repair mortar in layers under 35mm thickness."
        ]
        monitoring = "Measure half-cell corrosion potential according to ASTM C876 and monitor cover concrete resistivity annually."

    elif "hairline" in ctx_lower or "shrinkage" in ctx_lower:
        defect_type = "Hairline Crack"
        confidence = 92.0
        width = 0.18
        depth = "Surface"
        severity = "Low"
        urgency = "Low (Routine Monitoring)"
        surface = "RCC Floor Slab Top Surface"
        causes = [
            "Plastic shrinkage cracking from rapid surface moisture evaporation during initial set",
            "High ambient temperature and windy conditions exceeding critical evaporation rate (1.0 kg/m²/h)",
            "Delayed application of curing compound or wet burlap covering"
        ]
        integrity_risk = "LOW RISK: Non-structural surface defect. Crack does not penetrate past reinforcement depth and does not compromise ultimate structural load-bearing capacity under IS 456 limit state criteria."
        standards = ["IS 456:2000 Clause 35.3.2 (Crack width limit 0.3mm for mild exposure)", "ACI 224R-01"]
        repairs = [
            "Surface impregnation with silane/siloxane penetrative hydrophobic sealer.",
            "Application of flexible elastomeric crack-bridging polymer membrane.",
            "Routine photographic logging over 90 days."
        ]
        steps = [
            "Clean crack groove using industrial vacuum and high-pressure air blast.",
            "Apply low-viscosity penetrative acrylic sealer to prevent moisture and chloride intrusion.",
            "Apply high-elongation elastomeric waterproofing finish coat."
        ]
        monitoring = "Inspect quarterly; verify crack does not exceed allowable 0.30mm threshold for moderate exposure under IS 456."

    else:
        # Balanced structural crack diagnostic
        defect_type = "Thermal Expansion Crack"
        confidence = 88.5
        width = 1.65
        depth = "Medium Depth"
        severity = "Moderate"
        urgency = "Moderate (Repair within 30 days)"
        surface = "Parapet Wall and Roof Slab Junction"
        causes = [
            "Restrained thermal movement between exposed roof slab and shaded masonry wall",
            "Absence of expansion/contraction joint at 30-meter intervals as stipulated by IS 456 Clause 27",
            "Extreme diurnal temperature fluctuations (15°C to 42°C)"
        ]
        integrity_risk = "MODERATE RISK: Water ingress potential during monsoon season. If left unsealed, freeze-thaw or moisture seepage will cause degradation of roof waterproofing and corrosion of slab reinforcement."
        standards = ["IS 456:2000 Clause 27.2 (Expansion Joints)", "IS 3414:1968 (Code of Practice for Design of Joints in Buildings)"]
        repairs = [
            "Rake out crack and install a flexible elastomeric polyurethane joint sealant system.",
            "Backer rod insertion to maintain 2:1 width-to-depth sealant ratio.",
            "Over-banding with flexible hypalon waterproofing tape."
        ]
        steps = [
            "Groove out crack with V-shaped diamond blade cutter to 10mm width x 10mm depth.",
            "Prime joint edges with polyurethane primer.",
            "Insert closed-cell polyethylene foam backer rod at 8mm depth.",
            "Gun apply low-modulus polyurethane building sealant; tool surface smooth and flush."
        ]
        monitoring = "Visual inspection and optical crack width comparator check before and after monsoon season."

    return CrackDiagnosisResponse(
        defect_id=f"CRK-{uuid.uuid4().hex[:8].upper()}",
        timestamp=time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        defect_type=defect_type,
        confidence_score=confidence,
        estimated_crack_width_mm=width,
        crack_depth_category=depth,
        severity_level=severity,
        urgency_rating=urgency,
        surface_material=surface,
        probable_root_causes=causes,
        structural_integrity_risk=integrity_risk,
        applicable_standards=standards,
        recommended_engineering_repairs=repairs,
        repair_steps=steps,
        monitoring_protocol=monitoring,
        execution_mode="demo_fallback"
    )

async def diagnose_crack_defect(
    image_bytes: bytes,
    mime_type: str = "image/jpeg",
    notes: Optional[str] = None,
    api_key: Optional[str] = None
) -> CrackDiagnosisResponse:
    """Diagnose crack defect using Gemini multimodal LLM with automatic fallback."""
    # Validate image with Pillow
    try:
        with Image.open(io.BytesIO(image_bytes)) as img:
            img.verify()
    except Exception as e:
        raise ValueError(f"Invalid or corrupted image file: {str(e)}")

    client = GeminiMultimodalClient(api_key=api_key)
    if client.is_configured():
        prompt = CRACK_DIAGNOSIS_PROMPT
        if notes:
            prompt += f"\nInspector Observations & Structural Location: {notes}"

        result_dict = await client.generate_multimodal_json(
            prompt=prompt,
            image_bytes=image_bytes,
            mime_type=mime_type,
            temperature=0.2,
            system_instruction="You are a Principal Structural Forensic Engineer specializing in concrete structures and IS 456:2000."
        )

        if result_dict and isinstance(result_dict, dict) and "defect_type" in result_dict:
            try:
                return CrackDiagnosisResponse(
                    defect_id=f"CRK-{uuid.uuid4().hex[:8].upper()}",
                    timestamp=time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
                    defect_type=str(result_dict.get("defect_type", "Structural Defect")),
                    confidence_score=float(result_dict.get("confidence_score", 90.0)),
                    estimated_crack_width_mm=float(result_dict.get("estimated_crack_width_mm", 1.5)),
                    crack_depth_category=str(result_dict.get("crack_depth_category", "Medium Depth")),
                    severity_level=str(result_dict.get("severity_level", "Moderate")),
                    urgency_rating=str(result_dict.get("urgency_rating", "Moderate (Repair within 30 days)")),
                    surface_material=str(result_dict.get("surface_material", "RCC")),
                    probable_root_causes=result_dict.get("probable_root_causes", []),
                    structural_integrity_risk=str(result_dict.get("structural_integrity_risk", "")),
                    applicable_standards=result_dict.get("applicable_standards", ["IS 456:2000 Clause 35.3.2"]),
                    recommended_engineering_repairs=result_dict.get("recommended_engineering_repairs", []),
                    repair_steps=result_dict.get("repair_steps", []),
                    monitoring_protocol=str(result_dict.get("monitoring_protocol", "")),
                    execution_mode="live_gemini"
                )
            except Exception:
                pass

    return generate_fallback_crack_diagnosis(image_bytes, notes)
