from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.schemas.activity import ActivityRecommendationRequest, ActivityRecommendationResponse
from app.services.activity_service import calculate_activity_recommendation
from app.services.external_api_service import ExternalAPIService
from app.api.dependencies import get_current_user

router = APIRouter()


@router.post("/recommend", response_model=ActivityRecommendationResponse)
async def get_activity_recommendation(
    request: ActivityRecommendationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get activity recommendation based on current environmental conditions.
    Implements the jogging recommendation logic from the specification.
    """
    # Fetch current environmental data
    aq_data = await ExternalAPIService.fetch_openaq_data(request.lat, request.lon)
    weather_data = await ExternalAPIService.fetch_openweather_current(request.lat, request.lon)
    
    # Extract values
    pm25 = 0.0
    if aq_data and len(aq_data) > 0 and aq_data[0].get("pm25"):
        pm25 = aq_data[0]["pm25"]
    
    temperature = 20.0  # Default fallback
    humidity = 50.0     # Default fallback
    if weather_data:
        temperature = weather_data.get("temperature", 20.0)
        humidity = weather_data.get("humidity", 50.0)
    
    # Check if user has elevated sensitivity
    sensitive = current_user.sensitivity_level >= 3
    
    # Calculate recommendation
    score, label, rationale = calculate_activity_recommendation(
        activity_type=request.activity_type,
        pm25=pm25,
        humidity=humidity,
        temp_c=temperature,
        sensitive=sensitive
    )
    
    return ActivityRecommendationResponse(
        activity_type=request.activity_type,
        score=score,
        label=label,
        rationale=rationale,
        pm25=pm25,
        temperature=temperature,
        humidity=humidity
    )
