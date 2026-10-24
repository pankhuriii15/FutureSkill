import uuid
import time
import urllib.parse
from typing import List, Dict, Any, Tuple
from ..schemas.planning_schemas import (
    ValuationRequest,
    ValuationResponse,
    MaterialEstimate,
    MilestoneProgress
)

def format_inr(amount: float) -> str:
    """Format currency in Indian Lakhs and Crores."""
    if amount >= 10_000_000:  # 1 Crore = 10,000,000
        crores = amount / 10_000_000
        return f"₹{crores:.2f} Crores"
    elif amount >= 100_000:  # 1 Lakh = 100,000
        lakhs = amount / 100_000
        return f"₹{lakhs:.2f} Lakhs"
    else:
        return f"₹{amount:,.0f}"

def calculate_planning_and_valuation(request: ValuationRequest) -> ValuationResponse:
    """Calculate project budget, capex, valuation in INR, material estimation and milestones."""
    sqft = request.built_up_sqft
    comp_pct = request.completion_percentage
    tier = request.location_tier.lower()
    grade = request.construction_grade.lower()
    struct = request.structure_type.lower()

    # Base construction cost per sqft (INR)
    base_cost = 2400.0  # Default Tier 1 Standard
    if "tier 1" in tier:
        base_cost = 2400.0 if "standard" in grade else (3200.0 if "premium" in grade else 4600.0)
    elif "tier 2" in tier:
        base_cost = 1950.0 if "standard" in grade else (2600.0 if "premium" in grade else 3800.0)
    else:  # Tier 3
        base_cost = 1600.0 if "standard" in grade else (2100.0 if "premium" in grade else 3100.0)

    # Structure type cost factor
    struct_factor = 1.0
    if "high-rise" in struct:
        struct_factor = 1.18
    elif "commercial" in struct:
        struct_factor = 1.25
    elif "villa" in struct:
        struct_factor = 1.10
    elif "warehouse" in struct:
        struct_factor = 0.75
    elif "bridge" in struct or "infrastructure" in struct:
        struct_factor = 1.65

    effective_cost_per_sqft = round(base_cost * struct_factor, 2)
    total_budget = round(sqft * effective_cost_per_sqft, 2)
    capex_incurred = round(total_budget * (comp_pct / 100.0), 2)
    capex_remaining = round(total_budget - capex_incurred, 2)

    # Real Estate Market Sale Rate per sqft in INR
    market_rate_base = 14500.0
    if "tier 1" in tier:
        market_rate_base = 16500.0 if "standard" in grade else (22500.0 if "premium" in grade else 34000.0)
    elif "tier 2" in tier:
        market_rate_base = 7800.0 if "standard" in grade else (11200.0 if "premium" in grade else 16500.0)
    else:  # Tier 3
        market_rate_base = 4500.0 if "standard" in grade else (6200.0 if "premium" in grade else 8800.0)

    # Commercial / High-Rise market multiplier
    market_multiplier = 1.15
    if "commercial" in struct:
        market_multiplier = 1.35
    elif "villa" in struct:
        market_multiplier = 1.20
    elif "warehouse" in struct:
        market_multiplier = 0.70
    elif "bridge" in struct:
        market_multiplier = 1.10

    effective_market_rate = round(market_rate_base * market_multiplier, 2)
    projected_valuation = round(sqft * effective_market_rate, 2)

    # Current Asset Valuation = Land & Planning Value (35% base) + Progress Value (65% * progress)
    land_and_permits_val = projected_valuation * 0.35
    progress_val = (projected_valuation * 0.65) * (comp_pct / 100.0)
    current_asset_valuation = round(land_and_permits_val + progress_val, 2)

    # ROI estimate
    roi_pct = round(((projected_valuation - total_budget) / total_budget) * 100.0, 1)

    # IS 456 Material Estimation Thumb Rules
    steel_tonnes = round(sqft * 0.0042, 2)
    cement_bags = int(sqft * 0.40)
    sand_agg = round(sqft * 0.048, 2)
    rmc_volume = round(sqft * 0.035, 2)
    bricks_count = int(sqft * 16)
    paint_liters = round(sqft * 0.16, 2)

    materials = MaterialEstimate(
        steel_tonnes=steel_tonnes,
        cement_bags=cement_bags,
        sand_aggregate_cum=sand_agg,
        rmc_cum=rmc_volume,
        bricks_blocks_units=bricks_count,
        paint_liters=paint_liters
    )

    # Milestone Progress Breakdown
    # 5 Key Stages: Foundation (0-20%), Superstructure (20-55%), Masonry & Facade (55-70%), MEP (70-85%), Finishing & Handover (85-100%)
    milestones: List[MilestoneProgress] = [
        MilestoneProgress(
            milestone_name="Phase 1: Excavation, Piling & Raft Foundation",
            weight_percentage=20.0,
            status="Completed" if comp_pct >= 20 else ("In Progress" if comp_pct > 0 else "Pending"),
            target_days=60,
            description="Deep excavation, subgrade compaction, retaining diaphragm wall, and raft foundation casting."
        ),
        MilestoneProgress(
            milestone_name="Phase 2: RCC Superstructure & Slab Framing",
            weight_percentage=35.0,
            status="Completed" if comp_pct >= 55 else ("In Progress" if comp_pct >= 20 else "Pending"),
            target_days=120,
            description="Columns, shear walls, post-tensioned beam casting, and formwork cycles."
        ),
        MilestoneProgress(
            milestone_name="Phase 3: Masonry, External Cladding & Glazing",
            weight_percentage=15.0,
            status="Completed" if comp_pct >= 70 else ("In Progress" if comp_pct >= 55 else "Pending"),
            target_days=50,
            description="Autoclaved Aerated Concrete (AAC) blocks, structural glazing, and weatherproofing."
        ),
        MilestoneProgress(
            milestone_name="Phase 4: MEP Services & Fire Life-Safety",
            weight_percentage=15.0,
            status="Completed" if comp_pct >= 85 else ("In Progress" if comp_pct >= 70 else "Pending"),
            target_days=45,
            description="Electrical risers, HVAC ducting, plumbing shafts, sprinkler lines, and lift installation."
        ),
        MilestoneProgress(
            milestone_name="Phase 5: Interior Finishes & Occupancy Handover",
            weight_percentage=15.0,
            status="Completed" if comp_pct >= 100 else ("In Progress" if comp_pct >= 85 else "Pending"),
            target_days=40,
            description="Flooring, wall acoustics, testing & commissioning, occupancy certificate (OC)."
        )
    ]

    # Pollinations AI Prompt & 3D Render Image Generation
    arch_prompt = request.custom_prompt or (
        f"Ultra-luxurious 3D architectural rendering of a {request.construction_grade} {request.structure_type}, "
        f"modern Indian city skyline background, contemporary geometric glass facade, lush biophilic sky gardens, "
        f"dramatic sunset golden hour lighting, 8k resolution, octane render, architectural photography masterpiece"
    )
    encoded_prompt = urllib.parse.quote(arch_prompt)
    seed = int(sqft) % 9999 + int(comp_pct) * 7
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=640&seed={seed}&nologo=true"

    return ValuationResponse(
        calculation_id=f"VAL-{uuid.uuid4().hex[:8].upper()}",
        timestamp=time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        structure_type=request.structure_type,
        built_up_sqft=sqft,
        location_tier=request.location_tier,
        completion_percentage=comp_pct,
        total_project_budget_inr=total_budget,
        total_budget_formatted=format_inr(total_budget),
        capex_incurred_inr=capex_incurred,
        capex_incurred_formatted=format_inr(capex_incurred),
        capex_remaining_inr=capex_remaining,
        capex_remaining_formatted=format_inr(capex_remaining),
        current_asset_valuation_inr=current_asset_valuation,
        current_asset_valuation_formatted=format_inr(current_asset_valuation),
        projected_completion_valuation_inr=projected_valuation,
        projected_completion_valuation_formatted=format_inr(projected_valuation),
        estimated_roi_percentage=roi_pct,
        cost_per_sqft_inr=effective_cost_per_sqft,
        market_rate_per_sqft_inr=effective_market_rate,
        materials=materials,
        milestones=milestones,
        architectural_visualization_prompt=arch_prompt,
        architectural_image_url=image_url
    )
