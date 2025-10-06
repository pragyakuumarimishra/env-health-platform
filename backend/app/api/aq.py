from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from app.database import get_db
from app.models import AQExternal, Forecast, User
from app.schemas import AQCurrentResponse, AQForecastResponse
from app.auth import get_current_user

router = APIRouter()


@router.get("/current", response_model=AQCurrentResponse)
def get_current_aq(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current outdoor air quality for a location"""
    # Find nearest station within last hour
    time_threshold = datetime.utcnow() - timedelta(hours=1)
    
    # Simple nearest station query (in production, use PostGIS for better spatial queries)
    nearest = db.query(AQExternal).filter(
        AQExternal.ts >= time_threshold
    ).order_by(
        ((AQExternal.lat - lat) ** 2 + (AQExternal.lon - lon) ** 2)
    ).first()
    
    if not nearest:
        # Return mock data if no data available
        return AQCurrentResponse(
            lat=lat,
            lon=lon,
            ts=datetime.utcnow(),
            pm25=12.5,
            pm10=22.0,
            no2=15.0,
            o3=45.0,
            so2=5.0,
            aqi=50,
            source="mock"
        )
    
    return AQCurrentResponse(
        lat=nearest.lat,
        lon=nearest.lon,
        ts=nearest.ts,
        pm25=nearest.pm25,
        pm10=nearest.pm10,
        no2=nearest.no2,
        o3=nearest.o3,
        so2=nearest.so2,
        aqi=nearest.aqi,
        source=nearest.source
    )


@router.get("/forecast", response_model=List[AQForecastResponse])
def get_aq_forecast(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    hours: int = Query(6, ge=1, le=48, description="Forecast horizon in hours"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get short-term air quality forecast"""
    now = datetime.utcnow()
    forecast_end = now + timedelta(hours=hours)
    
    # Query forecasts for the location and time range
    forecasts = db.query(Forecast).filter(
        Forecast.ts_target >= now,
        Forecast.ts_target <= forecast_end
    ).order_by(
        ((Forecast.lat - lat) ** 2 + (Forecast.lon - lon) ** 2),
        Forecast.ts_target
    ).limit(hours).all()
    
    if not forecasts:
        # Return mock forecast data
        mock_forecasts = []
        for i in range(1, hours + 1):
            mock_forecasts.append(AQForecastResponse(
                lat=lat,
                lon=lon,
                ts_target=now + timedelta(hours=i),
                pm25_p10=10.0,
                pm25_p50=15.0 + i * 0.5,
                pm25_p90=25.0,
                no2_p50=18.0,
                model_version="mock-v1"
            ))
        return mock_forecasts
    
    return [
        AQForecastResponse(
            lat=f.lat,
            lon=f.lon,
            ts_target=f.ts_target,
            pm25_p10=f.pm25_p10,
            pm25_p50=f.pm25_p50,
            pm25_p90=f.pm25_p90,
            no2_p50=f.no2_p50,
            model_version=f.model_version
        )
        for f in forecasts
    ]
