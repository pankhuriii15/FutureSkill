from typing import List, Dict, Any, Optional
from ..schemas.chat_schemas import ChatRequest, ChatResponse, ChatMessage
from .gemini_service import GeminiMultimodalClient
from .prompt_templates import CHAT_ASSISTANT_SYSTEM_PROMPT

EXPERT_KNOWLEDGE_BASE = [
    {
        "keywords": ["formwork", "stripping", "striking", "de-shuttering", "shuttering"],
        "reply": (
            "Per IS 456:2000 Clause 11.3 (Stripping Time of Formwork), under ordinary circumstances with OPC concrete:\n\n"
            "1. **Vertical formwork to columns, walls, beams**: 16 – 24 hours\n"
            "2. **Soffit formwork to slabs (props left under)**: 3 days\n"
            "3. **Soffit formwork to beams (props left under)**: 7 days\n"
            "4. **Props to slabs**:\n"
            "   - Spanning up to 4.5m: 7 days\n"
            "   - Spanning over 4.5m: 14 days\n"
            "5. **Props to beams and arches**:\n"
            "   - Spanning up to 6m: 14 days\n"
            "   - Spanning over 6m: 21 days\n\n"
            "⚠️ Note: If blended cement (PPC / GGBS) or retarders are utilized, stripping times must be extended until concrete reaches at least 70% characteristic compressive strength."
        ),
        "references": ["IS 456:2000 Clause 11.3", "SP 34: Handbook on Concrete Reinforcement and Detailing"],
        "followups": [
            "What is the required compressive strength before striking beam props?",
            "How do low temperatures affect formwork striking duration?"
        ]
    },
    {
        "keywords": ["curing", "days", "water curing", "curing period"],
        "reply": (
            "Per IS 456:2000 Clause 13.5 (Curing of Concrete):\n\n"
            "• **Ordinary Portland Cement (OPC)**: Minimum **7 days** of continuous moist curing under normal atmospheric conditions.\n"
            "• **Mineral Admixtures (Fly-ash, GGBS, Silica Fume)**: Minimum **10 days** due to slower pozzolanic hydration.\n"
            "• **Hot and Dry Weather Conditions (Temp > 35°C, RH < 50%)**: Curing must be extended to at least **14 days**.\n\n"
            "Methods: Water ponding is mandatory for horizontal slabs; wet hessian/burlap wrapping or compliant membrane curing compounds (ASTM C309) for vertical columns and shear walls."
        ),
        "references": ["IS 456:2000 Clause 13.5", "IS 7861 (Part 1): Hot Weather Concreting"],
        "followups": [
            "What curing compound is recommended for high-rise facades?",
            "What are the consequences of delayed curing on plastic shrinkage cracks?"
        ]
    },
    {
        "keywords": ["m25", "m30", "mix design", "ratio", "water cement", "slump"],
        "reply": (
            "Concrete mix designs under IS 10262:2019 guidelines:\n\n"
            "• **M25 Nominal / Design Mix**:\n"
            "  - Characteristic compressive strength: 25 N/mm² at 28 days.\n"
            "  - Nominal proportion benchmark: ~1 : 1 : 2 (Cement : Fine Agg : Coarse Agg).\n"
            "  - Maximum Water-Cement ratio: **0.50** for Moderate exposure.\n"
            "  - Minimum cement content: 300 kg/m³ per IS 456 Table 5.\n"
            "• **M30 Design Mix**:\n"
            "  - Mandatory standard grade for severe exposure / post-tensioned members.\n"
            "  - Maximum W/C ratio: **0.45** (Severe exposure) or **0.40** (Very Severe).\n"
            "  - Recommended slump: 100-125mm for pumpable concrete with polycarboxylate superplasticizer."
        ),
        "references": ["IS 10262:2019 (Concrete Mix Proportioning)", "IS 456:2000 Table 5"],
        "followups": [
            "What slump range is required for tremie concrete in diaphragm walls?",
            "How do fly-ash blends affect 7-day vs 28-day concrete strength gains?"
        ]
    },
    {
        "keywords": ["crack", "epoxy", "injection", "repair", "shear crack"],
        "reply": (
            "For active structural crack remediation in RCC members:\n\n"
            "1. **Cracks > 0.3mm wide (Structural)**:\n"
            "   - Low-viscosity epoxy resin injection under 0.2 to 0.4 MPa pressure (ASTM C881 Type I/IV).\n"
            "   - Re-establishes monolithic tensile load transfer across the concrete matrix.\n"
            "2. **Water-bearing cracks / basement leaks**:\n"
            "   - Hydrophobic polyurethane (PU) expanding chemical injection foam.\n"
            "3. **Shear deficiency / rebar yielding**:\n"
            "   - External Carbon Fiber Reinforced Polymer (CFRP) composite laminates wrapped around tension zones."
        ),
        "references": ["ACI 224.1R (Causes, Evaluation, and Repair of Cracks)", "IS 456:2000 Clause 35.3.2"],
        "followups": [
            "What is the maximum allowable crack width under IS 456 for severe exposure?",
            "How do I set up acrylic tell-tale monitoring gauges?"
        ]
    },
    {
        "keywords": ["lap", "development length", "ld", "rebar", "splice"],
        "reply": (
            "Per IS 456:2000 Clause 26.2.1, Development Length ($L_d$) is calculated as:\n\n"
            "$$L_d = \\frac{\\phi \\cdot \\sigma_s}{4 \\cdot \\tau_{bd}}$$\n\n"
            "Where $\\phi$ is bar diameter, $\\sigma_s$ is design stress in bar ($0.87 f_y$), and $\\tau_{bd}$ is design bond stress.\n\n"
            "• For **Fe 500** steel in **M25** concrete in tension:\n"
            "  - Design bond stress $\\tau_{bd} = 1.4 \\times 1.6 = 2.24$ N/mm² (with 60% boost for deformed bars).\n"
            "  - $L_d \\approx 48.5 \\times \\phi$ (typically rounded to **50d** on site).\n"
            "• Lap Splices: Must not be located in zones of high flexural moments; stagger splices so not more than 50% are spliced at any cross-section."
        ),
        "references": ["IS 456:2000 Clause 26.2", "SP 34:1987 (SCTA Detailing Manual)"],
        "followups": [
            "What is the required lap length for bars in direct compression?",
            "Can mechanical couplers replace lap splices for bars larger than 32mm?"
        ]
    }
]

async def answer_site_chat(request: ChatRequest) -> ChatResponse:
    """Answer site engineering questions using live Gemini or domain knowledge engine."""
    user_query = ""
    for msg in reversed(request.messages):
        if msg.role == "user":
            user_query = msg.content
            break

    client = GeminiMultimodalClient(api_key=request.api_key)
    if client.is_configured():
        system_instruction = (
            f"{CHAT_ASSISTANT_SYSTEM_PROMPT}\n"
            f"Active Site Context: {request.site_context or 'General Civil Site'}"
        )
        msg_dicts = [{"role": m.role, "content": m.content} for m in request.messages]
        llm_reply = await client.generate_chat_response(
            messages=msg_dicts,
            system_instruction=system_instruction
        )
        if llm_reply:
            return ChatResponse(
                reply=llm_reply,
                references=["IS 456:2000", "OSHA 29 CFR 1926", "National Building Code (NBC) 2016"],
                suggested_followups=[
                    "What specific quality inspection checks should be documented?",
                    "How does this impact the project critical path schedule?"
                ],
                execution_mode="live_gemini"
            )

    # Intelligent fallback knowledge retrieval
    q_lower = user_query.lower()
    for entry in EXPERT_KNOWLEDGE_BASE:
        if any(kw in q_lower for kw in entry["keywords"]):
            return ChatResponse(
                reply=entry["reply"],
                references=entry["references"],
                suggested_followups=entry["followups"],
                execution_mode="demo_fallback"
            )

    # Generic comprehensive civil engineering reply
    generic_reply = (
        f"Regarding your query on '{user_query}':\n\n"
        "According to standard Indian Civil Engineering practice and IS 456:2000 / National Building Code (NBC 2016):\n"
        "1. All structural operations must follow approved Quality Assurance & Quality Control (QA/QC) inspection test plans (ITP).\n"
        "2. Concrete batching must verify slump tolerance (±25mm) and 28-day cube sampling per IS 516.\n"
        "3. Prior to casting or structural alteration, verify structural engineer clearance and verify reinforcement rebar cover with calibrated cover blocks.\n"
        "4. Strict OSHA 1926 fall protection and personal protective equipment (IS 2925) must remain active throughout operations."
    )
    return ChatResponse(
        reply=generic_reply,
        references=["IS 456:2000", "IS 516 (Methods of Tests for Strength of Concrete)", "OSHA 1926"],
        suggested_followups=[
            "What are the standard slump test tolerances for pumpable concrete?",
            "What are the curing requirements under IS 456?"
        ],
        execution_mode="demo_fallback"
    )
