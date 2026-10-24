import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import PLATFORM_ID, PLATFORM_NAME, PLATFORM_VERSION
from .routes import safety, cracks, planning, weather, chat, health

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("construction_intelligence")

app = FastAPI(
    title=PLATFORM_NAME,
    description="Multimodal decision-support system analyzing site photos for PPE compliance, concrete crack forensics, project estimation & valuation in INR, and weather-aware safety protocols.",
    version=PLATFORM_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for frontend Vite development & cross-origin API access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all route modules
app.include_router(health.router)
app.include_router(safety.router)
app.include_router(cracks.router)
app.include_router(planning.router)
app.include_router(weather.router)
app.include_router(chat.router)

@app.get("/", tags=["Root"])
def root():
    return {
        "platform_id": PLATFORM_ID,
        "name": PLATFORM_NAME,
        "version": PLATFORM_VERSION,
        "status": "operational",
        "documentation": "/docs",
        "category": "Generative AI | Real Estate Decision Support"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
