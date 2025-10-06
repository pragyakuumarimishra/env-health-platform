from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime
from uuid import UUID


class SensorDeviceCreate(BaseModel):
    label: str
    location_lat: Optional[float] = None
    location_lon: Optional[float] = None
    indoor: bool = True
    firmware_version: Optional[str] = None


class SensorDeviceResponse(BaseModel):
    id: UUID
    user_id: UUID
    label: str
    location_lat: Optional[float]
    location_lon: Optional[float]
    indoor: bool
    firmware_version: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class SensorReadingCreate(BaseModel):
    device_id: UUID
    ts: datetime
    pm25: Optional[float] = None
    pm10: Optional[float] = None
    co2: Optional[float] = None
    voc_index: Optional[float] = None
    temp: Optional[float] = None
    humidity: Optional[float] = None
