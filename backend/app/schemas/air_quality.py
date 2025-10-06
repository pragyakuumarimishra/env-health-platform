from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AirQualityResponse(BaseModel):
    source: str
    station_id: Optional[str]
    ts: datetime
    lat: Optional[float]
    lon: Optional[float]
    pm25: Optional[float]
    pm10: Optional[float]
    no2: Optional[float]
    o3: Optional[float]
    so2: Optional[float]
    aqi: Optional[int]

    class Config:
        from_attributes = True


class ForecastResponse(BaseModel):
    model_version: Optional[str]
    lat: Optional[float]
    lon: Optional[float]
    ts_target: datetime
    pm25_p10: Optional[float]
    pm25_p50: Optional[float]
    pm25_p90: Optional[float]
    no2_p50: Optional[float]
    created_at: datetime

    class Config:
        from_attributes = True
