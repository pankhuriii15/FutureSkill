from typing import List, Optional
from pydantic import BaseModel, Field

class CrackDiagnosisResponse(BaseModel):
    platform_id: str = "6ac4c98d1dcde6d7857c1642"
    defect_id: str
    timestamp: str
    defect_type: str = Field(..., description="Hairline Crack, Settlement Crack, Structural Shear Crack, Thermal Expansion Crack, Spalling & Delamination, etc.")
    confidence_score: float = Field(..., ge=0.0, le=100.0, description="Confidence percentage")
    estimated_crack_width_mm: float = Field(..., description="Estimated crack width in mm")
    crack_depth_category: str = Field("Medium Depth", description="Surface, Medium Depth, or Through-Section")
    severity_level: str = Field(..., description="Low, Moderate, Severe, or Catastrophic")
    urgency_rating: str = Field(..., description="Immediate (Stop Work), High (Repair within 7 days), Moderate (Repair within 30 days), Low (Routine Monitoring)")
    surface_material: str = Field("Reinforced Cement Concrete (RCC)", description="Surface material identified")
    probable_root_causes: List[str] = Field(default_factory=list)
    structural_integrity_risk: str = Field(..., description="Risk assessment of structural load capacity")
    applicable_standards: List[str] = Field(default_factory=list, description="IS 456:2000, ACI 224R-01, etc.")
    recommended_engineering_repairs: List[str] = Field(default_factory=list)
    repair_steps: List[str] = Field(default_factory=list)
    monitoring_protocol: str = Field(..., description="Monitoring frequency and gauge setup")
    execution_mode: str = "demo_fallback"
