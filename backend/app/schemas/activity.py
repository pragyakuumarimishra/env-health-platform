from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ActivityRecommendationRequest(BaseModel):
    activity_type: str  # e.g., "jogging", "cycling", "walking"
    lat: float
    lon: float
    time: Optional[datetime] = None  # If None, use current time


class ActivityRecommendationResponse(BaseModel):
    activity_type: str
    score: int
    label: str  # "Good", "Caution", "Avoid", "Not Recommended"
    rationale: str
    window_start: Optional[datetime] = None
    window_end: Optional[datetime] = None
    pm25: Optional[float] = None
    temperature: Optional[float] = None
    humidity: Optional[float] = None
