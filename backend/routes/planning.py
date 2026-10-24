from fastapi import APIRouter, HTTPException, status
from ..schemas.planning_schemas import ValuationRequest, ValuationResponse
from ..services.valuation_engine import calculate_planning_and_valuation

router = APIRouter(prefix="/api", tags=["Planning & Real Estate Valuation"])

@router.post(
    "/calculate-valuation",
    response_model=ValuationResponse,
    summary="Calculate total budget, capex incurred, market asset valuation in INR, and material estimates"
)
async def calculate_valuation_endpoint(request: ValuationRequest):
    """
    Planning & Valuation endpoint: Calculates project budget, capex incurred, market asset valuation
    in INR (Lakhs/Crores), IS 456 material requirements (steel tonnes, cement bags, aggregates, RMC),
    milestone progress schedules, and generative 3D architectural rendering integration.
    """
    if request.built_up_sqft <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Built-up square footage must be greater than zero."
        )
    if not (0 <= request.completion_percentage <= 100):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Completion percentage must be between 0 and 100."
        )

    try:
        response = calculate_planning_and_valuation(request)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Valuation calculation failed: {str(e)}"
        )
