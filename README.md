# Multimodal Construction Intelligence Platform
**Category:** Generative AI | Real Estate Decision Support  
**Platform ID:** `6ac4c98d1dcde6d7857c1642`  
**Standards:** IS 456:2000, IS 2925, OSHA 29 CFR 1926, ACI 224R-01  

---

## 🌟 Executive Overview
The **AI-Powered Multimodal Construction Intelligence Platform** is an intelligent full-stack decision-support platform designed to assist civil engineers, safety auditors, project managers, and real-estate developers across all stages of construction planning, execution, and forensic monitoring.

By combining computer vision, multimodal LLM reasoning (Google Gemini 1.5 Flash), and structural engineering domain models, the platform analyzes site photos, architectural parameters, and environmental conditions to produce actionable, standards-compliant decisions.

---

## 📐 Kanban Epics Coverage

| Epic | Module | Key Capabilities |
| :--- | :--- | :--- |
| **Prerequisites** | Environment & Dependencies | Python 3.9+, Node.js 18+, FastAPI, React.js, Vite, Pillow, Pydantic v2 |
| **Epic 1** | Requirements & Env Setup | Modular FastAPI service architecture, secure environment config, CORS handling |
| **Epic 2** | PPE Safety & Crack Diagnostics | Computer vision PPE audits (IS 2925/OSHA), fracture classification (IS 456:2000 Clause 35.3.2) |
| **Epic 3** | Project Planning & Valuation | Construction costing in INR (Lakhs/Crores), CapEx tracking, material estimation, Pollinations 3D render |
| **Epic 4** | Multimodal AI & JSON Contracts | Strict Pydantic models, JSON data contracts, graceful autonomous fallback |
| **Epic 5** | Daily Chatbot & Weather Advisory | Wind/Monsoon/Heat safety protocols, crane shutdown mandates, StrucAI multi-turn assistant |
| **Epic 6** | Testing, Interface & Deployment | 12-test pytest suite, Vite production build, 1-click startup scripts |

---

## 🏗️ System Architecture

```
                       ┌────────────────────────────────────────────────────────┐
                       │          React.js + Vite Web Application               │
                       │     (Dark Glassmorphism, Tailwind/CSS, Lucide)         │
                       └──────────────────────────┬─────────────────────────────┘
                                                  │ HTTP / JSON API Contracts
                       ┌──────────────────────────▼─────────────────────────────┐
                       │               FastAPI Backend Gateway                  │
                       │  CORS • Pydantic Schema Validation • Image Validation  │
                       └─────┬──────────────────┬──────────────────┬────────────┘
                             │                  │                  │
               ┌─────────────▼──────┐    ┌──────▼────────────┐     ▼─────────────────┐
               │  Multimodal Vision │    │ Engineering Logic │     │ AI Assistance   │
               │  Gemini 1.5 Flash  │    │ IS 456 / CPWD     │     │ StrucAI Chatbot │
               │  (Autonomous Demo  │    │ Materials & CapEx │     │ Weather Alerts  │
               │   Fallback Mode)   │    │ 3D Visualizer     │     │ Crane Mandates  │
               └────────────────────┘    └───────────────────┘     └─────────────────┘
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- **Python:** 3.9+ (Python 3.14 compatible)
- **Node.js:** v18+ or v24+ with `npm`

### 2. Full-Stack Setup (FastAPI + React.js)

#### Backend Setup
```bash
# In project root
python -m venv venv
.\venv\Scripts\activate
pip install -r backend/requirements.txt

# Start FastAPI server
uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```
API Documentation will be live at: **`http://127.0.0.1:8000/docs`**

#### Frontend Setup
```bash
# In a new terminal
cd frontend
npm install
npm run dev
```
Web application will be live at: **`http://127.0.0.1:5173/`**

#### 1-Click Launch (Windows)
Double-click `run_fullstack.bat` in the root directory to automatically launch both the backend and frontend simultaneously.

---

### 3. Turnkey Streamlit Companion Runner
For seamless 1-click execution or cloud deployment without Node.js:
```bash
.\venv\Scripts\streamlit run app.py
```
Or double-click `run_streamlit.bat`.

---

## 🛡️ Core Functional Modules

### 1. Tab 1: Site Safety & PPE Audit (Epic 2)
- **Inputs:** Construction site photographs (JPEG/PNG) + inspector observation notes.
- **Standards:** OSHA 29 CFR 1926 & Indian Standard IS 2925 (Hard Hats), IS 15298 (Boots), IS 3521 (Fall Protection).
- **Outputs:**
  - `safety_score` (0 to 100)
  - `overall_status` (Compliant, Minor Infractions, High Risk, Critical Violation)
  - PPE Compliance Checklist Table (Hard Hats, High-Vis Vests, Boots, Harnesses)
  - Identified Site Hazards with severity rating (`Low`, `Medium`, `High`, `Critical`) and actionable engineering remedies
  - Downloadable JSON Audit Report.

### 2. Tab 2: Concrete Crack Diagnostics & Structural Integrity (Epic 2)
- **Inputs:** Concrete/masonry surface fracture images.
- **Classification Types:**
  - **Structural Shear Crack (45° diagonal):** High urgency, epoxy pressure injection + CFRP wrap.
  - **Settlement Crack:** Stepped masonry/plinth settlement, compaction grouting + stitching ties.
  - **Spalling & Delamination:** Rebar corrosion, sacrificial zinc anodes + polymer repair mortar.
  - **Plastic Shrinkage Hairline:** Crack width < 0.3mm, hydrophobic surface silane impregnator.
- **Outputs:** Millimeter crack width, structural load risk, repair methodology, and tell-tale gauge monitoring protocol.

### 3. Tab 3: Planning, Costing & Real Estate Valuation in INR (Epic 3)
- **Inputs:** Structure type, built-up sq.ft., Location Tier (Tier 1/2/3 Indian cities), Construction Grade, Completion % slider.
- **Calculations:**
  - Total construction budget in INR (Lakhs / Crores)
  - CapEx incurred to date vs CapEx remaining
  - Current Market Asset Valuation in INR (incorporating land base + progress appreciation)
  - Projected completion valuation + estimated ROI percentage
  - IS 456 Material Estimates: Steel reinforcement (MT), Portland cement (50kg bags), aggregates, and Ready-Mix Concrete
  - Conceptual 3D architectural rendering via Pollinations AI / Flux generator.

### 4. Tab 4: Daily Site Assistant & Weather-Aware Advisory (Epic 5)
- **Dynamic Weather Protocols:**
  - **High Wind (>45 km/h):** Immediate tower crane shutdown, weathervaning jibs, suspended cradle grounding.
  - **Heavy Rain / Monsoon:** Electrical 30mA RCD tests, basement sump dewatering, concrete rain protection.
  - **Extreme Heat (>40°C):** Continuous wet hessian curing (IS 456 Clause 14), 15-min rest cycles, chilled mix water.
- **StrucAI Assistant:** Multi-turn conversational engineering knowledge base answering IS 456, formwork stripping periods, mix proportions, and bar development lengths.

---

## 🧪 Automated Test Suite

Run the comprehensive pytest test suite validating all endpoints and edge cases:
```bash
.\venv\Scripts\python -m pytest backend/tests/ -v
```

### Verified Test Cases:
- `test_health_endpoint`: Uptime, platform metadata, supported epics.
- `test_sample_data_endpoint`: Pre-configured 1-click test scenarios.
- `test_valuation_calculation_tier1`: Financial calculations and IS 456 thumb rules.
- `test_valuation_validation_errors`: Negative areas and out-of-bound percentages.
- `test_weather_advisory_high_wind`: Automatic tower crane suspension triggers.
- `test_weather_advisory_extreme_heat`: Concrete curing protocols under IS 456 Clause 14.
- `test_audit_safety_endpoint_valid`: Real image inspection and PPE contract verification.
- `test_diagnose_crack_endpoint_valid`: Defect classification, width measurement, and repair steps.
- `test_edge_case_corrupted_image`: Proper HTTP 422 error on invalid image payloads.
- `test_edge_case_non_image_file`: Proper HTTP 400 rejection for non-image MIME types.
- `test_edge_case_empty_file`: Proper HTTP 400 rejection for zero-byte uploads.
- `test_site_chat_endpoint`: Engineering answers with IS code citations.

---

## 🔒 Security & API Key Management
- Custom API keys can be entered via the client interface or loaded via `.env` (`GEMINI_API_KEY`).
- Keys are retained strictly in client storage (`localStorage`) and forwarded directly to Google Generative Language APIs.
- When an API key is not supplied or quota is exhausted, the system automatically falls back to domain-informed autonomous demonstration intelligence.

---

## 📋 Known Limitations & Future Enhancements
1. **Direct Video Stream Processing:** Currently processes individual high-resolution stills; future versions can ingest live CCTV RTSP feeds for automated continuous geofencing.
2. **Thermal Infrared Integration:** Extending multimodal vision to accept FLIR thermal camera inputs for subsurface void and water seepage detection behind plaster.
3. **BIM IFC Export:** Future roadmap includes exporting structural defect coordinates directly into Autodesk Revit / IFC 4.0 models.
