from typing import List, Optional
from pydantic import BaseModel, Field

class PPECheckItem(BaseModel):
    item_name: str = Field(..., description="Name of the PPE item, e.g. Safety Helmet")
    detected_count: int = Field(0, description="Count of compliant workers wearing this PPE")
    missing_count: int = Field(0, description="Count of workers missing this PPE")
    compliance_percentage: float = Field(0.0, description="Compliance rate percentage from 0 to 100")
    status: str = Field("Compliant", description="Compliant, Partial, or Non-Compliant")
    details: str = Field("", description="Observation notes")

class SiteHazard(BaseModel):
    hazard_name: str = Field(..., description="Hazard title")
    severity: str = Field(..., description="Low, Medium, High, or Critical")
    location: str = Field(..., description="Location in image/site")
    standard_violation: str = Field(..., description="OSHA or IS 456 / IS 2925 standard violated")
    remedy: str = Field(..., description="Recommended corrective action")
    immediate_action_required: bool = Field(False, description="Whether immediate stoppage is required")

class WorkerDetection(BaseModel):
    worker_id: str
    bounding_box: Optional[List[float]] = None  # [ymin, xmin, ymax, xmax] normalized
    ppe_worn: List[str] = Field(default_factory=list)
    ppe_missing: List[str] = Field(default_factory=list)
    risk_level: str = "Low"

class SafetyAuditResponse(BaseModel):
    platform_id: str = "6ac4c98d1dcde6d7857c1642"
    audit_id: str
    timestamp: str
    safety_score: int = Field(..., ge=0, le=100, description="Safety compliance score 0-100")
    overall_status: str = Field(..., description="Compliant, Minor Infractions, High Risk, or Critical Violation")
    workers_detected_count: int = 0
    ppe_checklist: List[PPECheckItem] = Field(default_factory=list)
    identified_hazards: List[SiteHazard] = Field(default_factory=list)
    worker_detections: List[WorkerDetection] = Field(default_factory=list)
    executive_summary: str
    recommendations: List[str] = Field(default_factory=list)
    standards_referenced: List[str] = Field(default_factory=list)
    execution_mode: str = "demo_fallback"
