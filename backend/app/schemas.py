from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from uuid import UUID


# User schemas
class UserBase(BaseModel):
    email: EmailStr
    phone: Optional[str] = None
    name: Optional[str] = None
    dob: Optional[date] = None
    conditions: Optional[Dict[str, Any]] = None
    sensitivity_level: int = Field(default=1, ge=1, le=5)
    locale: str = "en"


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    dob: Optional[date] = None
    conditions: Optional[Dict[str, Any]] = None
    sensitivity_level: Optional[int] = Field(default=None, ge=1, le=5)


class UserResponse(UserBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


# Auth schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


# Sensor Device schemas
class SensorDeviceBase(BaseModel):
    label: str
    location_lat: Optional[float] = None
    location_lon: Optional[float] = None
    indoor: bool = True
    firmware_version: Optional[str] = None
    calibration: Optional[Dict[str, Any]] = None


class SensorDeviceCreate(SensorDeviceBase):
    pass


class SensorDeviceResponse(SensorDeviceBase):
    id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


# Sensor Reading schemas
class SensorReadingCreate(BaseModel):
    device_id: UUID
    ts: datetime
    pm25: Optional[float] = None
    pm10: Optional[float] = None
    co2: Optional[float] = None
    voc_index: Optional[float] = None
    temp: Optional[float] = None
    humidity: Optional[float] = None


class SensorReadingResponse(SensorReadingCreate):
    id: int

    class Config:
        from_attributes = True


# Air Quality schemas
class AQCurrentResponse(BaseModel):
    lat: float
    lon: float
    ts: datetime
    pm25: Optional[float] = None
    pm10: Optional[float] = None
    no2: Optional[float] = None
    o3: Optional[float] = None
    so2: Optional[float] = None
    aqi: Optional[int] = None
    source: str


class AQForecastResponse(BaseModel):
    lat: float
    lon: float
    ts_target: datetime
    pm25_p10: Optional[float] = None
    pm25_p50: Optional[float] = None
    pm25_p90: Optional[float] = None
    no2_p50: Optional[float] = None
    model_version: str


# Symptom Log schemas
class SymptomLogCreate(BaseModel):
    ts: datetime
    symptoms: Dict[str, Any]
    severity: int = Field(ge=1, le=10)
    notes: Optional[str] = None


class SymptomLogResponse(SymptomLogCreate):
    id: UUID
    user_id: UUID

    class Config:
        from_attributes = True


# Exposure Log schemas
class ExposureLogResponse(BaseModel):
    date: date
    cumulative_pm25: Optional[float] = None
    cumulative_no2: Optional[float] = None
    risk_score: Optional[int] = None

    class Config:
        from_attributes = True


# Activity Recommendation schemas
class ActivityRecommendationRequest(BaseModel):
    activity_type: str
    preferred_time: Optional[datetime] = None
    location_lat: Optional[float] = None
    location_lon: Optional[float] = None


class ActivityRecommendationResponse(BaseModel):
    id: UUID
    activity_type: str
    window_start: Optional[datetime] = None
    window_end: Optional[datetime] = None
    score: Optional[int] = None
    rationale: Optional[str] = None
    ts: datetime

    class Config:
        from_attributes = True


# Route schemas
class RouteRequest(BaseModel):
    origin_lat: float
    origin_lon: float
    dest_lat: float
    dest_lon: float


class RouteResponse(BaseModel):
    id: UUID
    origin_geo: Dict[str, Any]
    dest_geo: Dict[str, Any]
    route_geojson: Optional[Dict[str, Any]] = None
    time_minutes: Optional[int] = None
    exposure_estimate: Optional[float] = None
    alternative_rank: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


# Alert schemas
class AlertResponse(BaseModel):
    id: UUID
    type: str
    payload: Dict[str, Any]
    channel: str
    status: str
    ts: datetime

    class Config:
        from_attributes = True
