from typing import List, Optional
from pydantic import BaseModel, Field

class WeatherAdvisoryRequest(BaseModel):
    condition: str = Field(..., description="High Wind (>45 km/h), Heavy Rain / Monsoon, Extreme Heat (>40°C), Normal / Mild, etc.")
    site_phase: str = Field("Concrete Pouring & Curing", description="Active construction phase")
    temperature_celsius: Optional[float] = Field(32.0, description="Ambient temperature")
    wind_speed_kmh: Optional[float] = Field(25.0, description="Wind speed in km/h")
    humidity_pct: Optional[float] = Field(65.0, description="Relative humidity percentage")

class SafetyProtocol(BaseModel):
    category: str = Field(..., description="Crane & Lifting, Scaffolding, Concrete Curing, Electrical, Worker Welfare")
    action_level: str = Field(..., description="HALT OPERATION, RESTRICTED PROTOCOL, ENHANCED MONITORING, STANDARD")
    protocol_title: str
    detailed_procedure: str
    code_reference: str

class WeatherAdvisoryResponse(BaseModel):
    timestamp: str
    condition: str
    site_phase: str
    risk_level: str = Field(..., description="Low, Moderate, High, or Critical")
    operational_status: str = Field(..., description="Normal, Restricted Operations, or Complete Work Stoppage")
    weather_headline: str
    safety_protocols: List[SafetyProtocol] = Field(default_factory=list)
    emergency_checklist: List[str] = Field(default_factory=list)
    concrete_curing_advisory: str
    crane_lifting_advisory: str
    worker_shift_advisory: str
