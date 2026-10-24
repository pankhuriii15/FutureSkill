"""
Multimodal Construction Intelligence Platform
Turnkey Streamlit Application (Skill Wallet Capstone Project 1)
Platform ID: 6ac4c98d1dcde6d7857c1642
Category: Generative AI | Real Estate Decision Support
"""

import os
import json
import asyncio
import streamlit as st
from PIL import Image

# Import existing backend domain services directly
from backend.services.safety_analyzer import analyze_site_safety
from backend.services.crack_analyzer import diagnose_crack_defect
from backend.services.valuation_engine import calculate_planning_and_valuation, format_inr
from backend.services.weather_advisor import generate_weather_advisory
from backend.services.site_chatbot import answer_site_chat
from backend.schemas.planning_schemas import ValuationRequest
from backend.schemas.weather_schemas import WeatherAdvisoryRequest
from backend.schemas.chat_schemas import ChatRequest, ChatMessage

# Streamlit Page Configuration
st.set_page_config(
    page_title="Multimodal Construction Intelligence Platform",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main {
        background-color: #0b0f19;
        color: #f8fafc;
    }
    .metric-card {
        background: rgba(15, 23, 42, 0.75);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .status-pill {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
    }
    .pill-compliant { background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.4); }
    .pill-warning { background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.4); }
    .pill-danger { background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.4); }
</style>
""", unsafe_allow_html=True)

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.title("🏗️ Construction AI")
    st.markdown("**Platform ID:** `6ac4c98d1dcde6d7857c1642`")
    st.markdown("Generative AI & Decision Support Platform")
    st.divider()

    st.subheader("🔑 AI Engine Configuration")
    user_api_key = st.text_input(
        "Google Gemini API Key",
        type="password",
        value=os.getenv("GEMINI_API_KEY", ""),
        help="Optional: Supply your Google Gemini API key. If omitted, high-fidelity autonomous demonstration mode activates automatically."
    )

    if user_api_key:
        st.success("🟢 Gemini 1.5 Active")
    else:
        st.info("🟡 Autonomous Demonstration Mode Active")

    st.divider()
    st.subheader("🏛️ Architecture Overview")
    st.markdown("""
    - **Multimodal LLM:** Gemini 1.5 Flash Vision
    - **Safety Standard:** OSHA 1926 & IS 456 / IS 2925
    - **Valuation:** IS 456 & CPWD Rates in INR
    - **3D Render:** Pollinations / Flux API
    - **Contracts:** Strict Pydantic JSON Schemas
    """)
    st.divider()
    st.caption("v2.4.0 • Zero External DB Dependencies")

# ----------------- MAIN TABS -----------------
tab1, tab2, tab3, tab4 = st.tabs([
    "🦺 Site Safety & PPE Audit",
    "🔍 Crack Diagnostics & Forensics",
    "📊 Planning & Real Estate Valuation",
    "🌦️ Daily Site Assistant & Weather"
])

# ----------------- TAB 1: SITE SAFETY -----------------
with tab1:
    st.header("🦺 Construction Site Safety & PPE Audit")
    st.caption("OSHA 29 CFR 1926 & IS 456 / IS 2925 Compliance Verification")

    col1, col2 = st.columns([1, 1])

    with col1:
        uploaded_safety_img = st.file_uploader("Upload Site Photo (JPG/PNG)", type=["jpg", "jpeg", "png"], key="safety_upload")
        safety_notes = st.text_area("Site Context / Observations", "Inspect elevated deck framing for worker harnesses and chinstrap retention under IS 2925.")
        run_safety_btn = st.button("Run AI Safety & PPE Audit", type="primary", use_container_width=True)

    with col2:
        if uploaded_safety_img:
            st.image(uploaded_safety_img, caption="Uploaded Construction Site Photo", use_container_width=True)

    if run_safety_btn and uploaded_safety_img:
        with st.spinner("Analyzing site hazards and PPE compliance..."):
            img_bytes = uploaded_safety_img.getvalue()
            result = asyncio.run(analyze_site_safety(
                image_bytes=img_bytes,
                mime_type=uploaded_safety_img.type,
                notes=safety_notes,
                api_key=user_api_key or None
            ))

            st.divider()
            mcol1, mcol2, mcol3 = st.columns(3)
            mcol1.metric("Safety Score", f"{result.safety_score} / 100")
            mcol2.metric("Overall Status", result.overall_status)
            mcol3.metric("Workers Identified", result.workers_detected_count)

            st.subheader("📋 PPE Compliance Checklist (IS 2925 & OSHA)")
            checklist_data = [
                {
                    "PPE Item": item.item_name,
                    "Detected": item.detected_count,
                    "Missing": item.missing_count,
                    "Compliance %": f"{item.compliance_percentage}%",
                    "Status": item.status,
                    "Observations": item.details
                }
                for item in result.ppe_checklist
            ]
            st.table(checklist_data)

            st.subheader(f"⚠️ Identified Site Hazards ({len(result.identified_hazards)})")
            for h in result.identified_hazards:
                with st.expander(f"{h.hazard_name} — [{h.severity} Severity]"):
                    st.markdown(f"**Location:** {h.location}")
                    st.markdown(f"**Standard Violated:** `{h.standard_violation}`")
                    st.markdown(f"**Remedy:** {h.remedy}")

            st.subheader("📝 Executive Audit Summary")
            st.info(result.executive_summary)

            st.download_button(
                "⬇️ Download Audit Report (.JSON)",
                data=json.dumps(result.model_dump(), indent=2),
                file_name=f"Safety_Audit_{result.audit_id}.json",
                mime="application/json"
            )

# ----------------- TAB 2: CRACK DIAGNOSTICS -----------------
with tab2:
    st.header("🔍 Concrete Crack Diagnostics & Structural Integrity")
    st.caption("Structural Forensic Analysis per IS 456:2000 Clause 35.3.2 & ACI 224R-01")

    ccol1, ccol2 = st.columns([1, 1])

    with ccol1:
        uploaded_crack_img = st.file_uploader("Upload Defect Image (JPG/PNG)", type=["jpg", "jpeg", "png"], key="crack_upload")
        crack_notes = st.text_area("Structural Location & Notes", "Diagonal 45-degree shear crack in reinforced concrete transfer beam web.")
        run_crack_btn = st.button("Diagnose Structural Defect", type="primary", use_container_width=True)

    with ccol2:
        if uploaded_crack_img:
            st.image(uploaded_crack_img, caption="Uploaded Surface Defect", use_container_width=True)

    if run_crack_btn and uploaded_crack_img:
        with st.spinner("Classifying crack mechanics and estimating width..."):
            img_bytes = uploaded_crack_img.getvalue()
            c_result = asyncio.run(diagnose_crack_defect(
                image_bytes=img_bytes,
                mime_type=uploaded_crack_img.type,
                notes=crack_notes,
                api_key=user_api_key or None
            ))

            st.divider()
            cm1, cm2, cm3 = st.columns(3)
            cm1.metric("Defect Type", c_result.defect_type, f"{c_result.confidence_score}% Conf.")
            cm2.metric("Crack Width", f"{c_result.estimated_crack_width_mm} mm", "IS 456 Limit: 0.30mm")
            cm3.metric("Urgency Rating", c_result.urgency_rating)

            st.subheader("🛡️ Structural Risk Assessment")
            st.warning(c_result.structural_integrity_risk)

            st.subheader("🔬 Probable Root Causes")
            for rc in c_result.probable_root_causes:
                st.markdown(f"- {rc}")

            st.subheader("🛠️ Recommended Engineering Repairs")
            for rep in c_result.recommended_engineering_repairs:
                st.markdown(f"**Method:** {rep}")

            st.markdown("**Step-by-Step Repair Execution:**")
            for i, step in enumerate(c_result.repair_steps, 1):
                st.markdown(f"{i}. {step}")

            st.caption(f"Monitoring Protocol: {c_result.monitoring_protocol}")

            st.download_button(
                "⬇️ Download Diagnostics Report (.JSON)",
                data=json.dumps(c_result.model_dump(), indent=2),
                file_name=f"Crack_Diagnosis_{c_result.defect_id}.json",
                mime="application/json"
            )

# ----------------- TAB 3: PLANNING & VALUATION -----------------
with tab3:
    st.header("📊 Project Planning & Real Estate Valuation (INR)")
    st.caption("Budgeting, CapEx, Material Quantities, and 3D Architectural Renders")

    pcol1, pcol2 = st.columns([1, 1])

    with pcol1:
        st_type = st.selectbox("Structure Type", [
            "Residential High-Rise",
            "Commercial Complex",
            "Villa / Row House",
            "Industrial Warehouse",
            "Infrastructure / Bridge"
        ])
        built_sqft = st.number_input("Built-Up Area (sq. ft.)", min_value=1000, value=85000, step=5000)
        loc_tier = st.selectbox("Location Tier", [
            "Tier 1 (Mumbai, Delhi-NCR, Bengaluru)",
            "Tier 2 (Pune, Hyderabad, Ahmedabad, Chennai)",
            "Tier 3 (Emerging Urban Centers)"
        ])
        grade = st.radio("Construction Grade", ["Standard", "Premium", "Luxury"], horizontal=True, index=1)
        comp_slider = st.slider("Project Completion Progress (%)", min_value=0, max_value=100, value=45)
        custom_arch_prompt = st.text_input("Custom 3D Architecture Prompt (Optional)", "")

    val_response = calculate_planning_and_valuation(ValuationRequest(
        structure_type=st_type,
        built_up_sqft=built_sqft,
        location_tier=loc_tier,
        completion_percentage=comp_slider,
        construction_grade=grade,
        custom_prompt=custom_arch_prompt or None
    ))

    with pcol2:
        st.subheader("Financial Asset Valuation Summary")
        vm1, vm2 = st.columns(2)
        vm1.metric("Total Project Budget", val_response.total_budget_formatted, f"₹{val_response.cost_per_sqft_inr}/sqft")
        vm2.metric("CapEx Incurred", val_response.capex_incurred_formatted, f"Rem: {val_response.capex_remaining_formatted}")

        vm3, vm4 = st.columns(2)
        vm3.metric("Current Asset Valuation", val_response.current_asset_valuation_formatted, f"At {comp_slider}% Progress")
        vm4.metric("Projected Completed Valuation", val_response.projected_completion_valuation_formatted, f"+{val_response.estimated_roi_percentage}% ROI")

        st.progress(comp_slider / 100.0, text=f"Milestone Completion: {comp_slider}%")

    st.divider()
    st.subheader("🧱 IS 456 Material Estimation Thumb Rules")
    mat_col1, mat_col2, mat_col3, mat_col4 = st.columns(4)
    mat_col1.metric("Steel Reinforcement", f"{val_response.materials.steel_tonnes} MT")
    mat_col2.metric("Cement Bags (50kg)", f"{val_response.materials.cement_bags:,}")
    mat_col3.metric("Aggregates & Sand", f"{val_response.materials.sand_aggregate_cum} Cu.m")
    mat_col4.metric("Ready Mix Concrete", f"{val_response.materials.rmc_cum} Cu.m")

    st.subheader("🖼️ Conceptual 3D Architectural Rendering (Pollinations / Flux AI)")
    st.image(val_response.architectural_image_url, caption=val_response.architectural_visualization_prompt, use_container_width=True)

    st.download_button(
        "⬇️ Download Valuation Report (.JSON)",
        data=json.dumps(val_response.model_dump(), indent=2),
        file_name=f"Valuation_{val_response.calculation_id}.json",
        mime="application/json"
    )

# ----------------- TAB 4: WEATHER ADVISORY & ASSISTANT -----------------
with tab4:
    st.header("🌦️ Daily Site Assistant & Weather-Aware Advisory")
    st.caption("Dynamic Safety Protocols & IS 456 Chatbot")

    wcol1, wcol2 = st.columns([1, 1])

    with wcol1:
        weather_cond = st.selectbox("Weather Condition", [
            "High Wind (>45 km/h)",
            "Heavy Rain / Monsoon",
            "Extreme Heat (>40°C)",
            "Severe Thunderstorm / Lightning",
            "Normal / Mild"
        ])
        phase = st.selectbox("Active Construction Phase", [
            "Excavation & Foundation",
            "Concrete Pouring & Curing",
            "Structural Steel & Facade",
            "Interior Finishing & MEP"
        ])

        w_resp = generate_weather_advisory(WeatherAdvisoryRequest(
            condition=weather_cond,
            site_phase=phase
        ))

        st.subheader(w_resp.weather_headline)
        st.markdown(f"**Risk Level:** `{w_resp.risk_level}` • **Status:** `{w_resp.operational_status}`")

        for p in w_resp.safety_protocols:
            st.warning(f"**[{p.action_level}] {p.protocol_title}**\n\n{p.detailed_procedure}\n\n*Reference: {p.code_reference}*")

    with wcol2:
        st.subheader("🤖 StrucAI: Resident Engineering Assistant")
        st.caption("Ask questions regarding IS 456:2000, OSHA 1926, formwork striking times, or mix design.")

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = [
                ChatMessage(role="assistant", content="Hello! Ask me any structural engineering question, IS 456 clause, or OSHA safety protocol.")
            ]

        for chat in st.session_state.chat_history:
            with st.chat_message(chat.role):
                st.markdown(chat.content)

        user_chat_input = st.chat_input("Ask a construction engineering question...")
        if user_chat_input:
            st.session_state.chat_history.append(ChatMessage(role="user", content=user_chat_input))
            with st.chat_message("user"):
                st.markdown(user_chat_input)

            with st.spinner("StrucAI consulting IS codes..."):
                c_ans = asyncio.run(answer_site_chat(ChatRequest(
                    messages=st.session_state.chat_history,
                    site_context=f"Condition: {weather_cond}. Phase: {phase}",
                    api_key=user_api_key or None
                )))

                st.session_state.chat_history.append(ChatMessage(role="assistant", content=c_ans.reply))
                with st.chat_message("assistant"):
                    st.markdown(c_ans.reply)
                    if c_ans.references:
                        st.caption(f"Citations: {', '.join(c_ans.references)}")
