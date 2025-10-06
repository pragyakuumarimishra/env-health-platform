from app.schemas.user import UserCreate, UserLogin, UserResponse, UserUpdate
from app.schemas.sensor import SensorDeviceCreate, SensorDeviceResponse, SensorReadingCreate
from app.schemas.air_quality import AirQualityResponse, ForecastResponse
from app.schemas.activity import ActivityRecommendationRequest, ActivityRecommendationResponse

__all__ = [
    "UserCreate",
    "UserLogin",
    "UserResponse",
    "UserUpdate",
    "SensorDeviceCreate",
    "SensorDeviceResponse",
    "SensorReadingCreate",
    "AirQualityResponse",
    "ForecastResponse",
    "ActivityRecommendationRequest",
    "ActivityRecommendationResponse",
]
