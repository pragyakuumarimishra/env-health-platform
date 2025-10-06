from fastapi import APIRouter, Depends, Query
from typing import Optional
from app.models.user import User
from app.api.dependencies import get_current_user
from app.services.external_api_service import ExternalAPIService

router = APIRouter()


@router.get("/current")
async def get_current_air_quality(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    current_user: User = Depends(get_current_user)
):
    """Get current air quality data for a location"""
    
    # Fetch air quality data
    aq_data = await ExternalAPIService.fetch_openaq_data(lat, lon)
    
    # Fetch weather data
    weather_data = await ExternalAPIService.fetch_openweather_current(lat, lon)
    
    # Combine and return
    result = {
        "location": {"lat": lat, "lon": lon},
        "air_quality": aq_data[0] if aq_data and len(aq_data) > 0 else None,
        "weather": weather_data
    }
    
    # Calculate AQI if PM2.5 is available
    if result["air_quality"] and result["air_quality"].get("pm25"):
        result["air_quality"]["aqi"] = ExternalAPIService.calculate_aqi_from_pm25(
            result["air_quality"]["pm25"]
        )
    
    return result


@router.get("/forecast")
async def get_air_quality_forecast(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    hours: int = Query(6, description="Forecast hours ahead", ge=1, le=24),
    current_user: User = Depends(get_current_user)
):
    """Get air quality forecast for a location"""
    # For MVP, return placeholder data
    # In Phase 2+, this would use actual forecasting models
    return {
        "location": {"lat": lat, "lon": lon},
        "forecast": {
            "message": "Forecasting feature coming in Phase 2",
            "hours_ahead": hours,
            "note": "Currently using persistence model (current conditions projected forward)"
        }
    }
