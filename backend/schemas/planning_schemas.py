from typing import List, Optional
from pydantic import BaseModel, Field

class ValuationRequest(BaseModel):
    structure_type: str = Field("Residential High-Rise", description="Type of structure")
    built_up_sqft: float = Field(..., gt=0, description="Total built up area in sq ft")
    location_tier: str = Field("Tier 1 (Mumbai, Delhi-NCR, Bengaluru)", description="Tier 1, Tier 2, or Tier 3")
    completion_percentage: float = Field(..., ge=0, le=100, description="Project completion percentage")
    construction_grade: str = Field("Premium", description="Standard, Premium, or Luxury")
    custom_prompt: Optional[str] = Field(None, description="Optional custom architectural prompt")

class MaterialEstimate(BaseModel):
    steel_tonnes: float = Field(..., description="Estimated steel reinforcement in metric tonnes")
    cement_bags: int = Field(..., description="Estimated Portland cement bags (50kg each)")
    sand_aggregate_cum: float = Field(..., description="Coarse and fine aggregates in cubic meters")
    rmc_cum: float = Field(..., description="Ready Mix Concrete in cubic meters")
    bricks_blocks_units: int = Field(..., description="Fly-ash bricks or AAC blocks count")
    paint_liters: float = Field(..., description="Interior and exterior paint in liters")

class MilestoneProgress(BaseModel):
    milestone_name: str
    weight_percentage: float
    status: str  # Completed, In Progress, Pending
    target_days: int
    description: str

class ValuationResponse(BaseModel):
    platform_id: str = "6ac4c98d1dcde6d7857c1642"
    calculation_id: str
    timestamp: str
    structure_type: str
    built_up_sqft: float
    location_tier: str
    completion_percentage: float
    total_project_budget_inr: float
    total_budget_formatted: str
    capex_incurred_inr: float
    capex_incurred_formatted: str
    capex_remaining_inr: float
    capex_remaining_formatted: str
    current_asset_valuation_inr: float
    current_asset_valuation_formatted: str
    projected_completion_valuation_inr: float
    projected_completion_valuation_formatted: str
    estimated_roi_percentage: float
    cost_per_sqft_inr: float
    market_rate_per_sqft_inr: float
    materials: MaterialEstimate
    milestones: List[MilestoneProgress]
    architectural_visualization_prompt: str
    architectural_image_url: Optional[str] = None
