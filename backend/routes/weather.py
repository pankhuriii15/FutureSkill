from fastapi import APIRouter, HTTPException, status
from ..schemas.weather_schemas import WeatherAdvisoryRequest, WeatherAdvisoryResponse
from ..services.weather_advisor import generate_weather_advisory

router = APIRouter(prefix="/api", tags=["Daily Site Assistant & Weather-Aware Advisory"])

@router.post(
    "/weather-advisory",
    response_model=WeatherAdvisoryResponse,
    summary="Generate weather-aware dynamic safety alerts and engineering protocols"
)
async def weather_advisory_endpoint(request: WeatherAdvisoryRequest):
    """
    Generates safety protocols and checklists based on weather conditions (High Wind, Heavy Rain,
    Extreme Heat, Normal, Thunderstorm) including crane suspension, electrical safety, and IS 456 curing protocols.
    """
    try:
        response = generate_weather_advisory(request)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Weather advisory generation failed: {str(e)}"
        )
