from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from app.database import get_db
from app.models import SensorDevice, SensorReading, User
from app.schemas import SensorDeviceCreate, SensorDeviceResponse, SensorReadingCreate, SensorReadingResponse
from app.auth import get_current_user

router = APIRouter()


@router.get("/devices", response_model=List[SensorDeviceResponse])
def list_devices(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all sensor devices for the current user"""
    devices = db.query(SensorDevice).filter(SensorDevice.user_id == current_user.id).all()
    return devices


@router.post("/devices", response_model=SensorDeviceResponse)
def register_device(
    device: SensorDeviceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Register a new indoor sensor device"""
    db_device = SensorDevice(
        user_id=current_user.id,
        label=device.label,
        location_lat=device.location_lat,
        location_lon=device.location_lon,
        indoor=device.indoor,
        firmware_version=device.firmware_version,
        calibration=device.calibration
    )
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device


@router.get("/readings", response_model=List[SensorReadingResponse])
def get_readings(
    device_id: str = Query(..., description="Device UUID"),
    hours: int = Query(24, ge=1, le=168, description="Hours of history to retrieve"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Query indoor sensor readings for a device"""
    # Verify device belongs to current user
    device = db.query(SensorDevice).filter(
        SensorDevice.id == device_id,
        SensorDevice.user_id == current_user.id
    ).first()
    
    if not device:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Device not found")
    
    time_threshold = datetime.utcnow() - timedelta(hours=hours)
    readings = db.query(SensorReading).filter(
        SensorReading.device_id == device_id,
        SensorReading.ts >= time_threshold
    ).order_by(SensorReading.ts.desc()).all()
    
    return readings


@router.post("/readings", response_model=SensorReadingResponse)
def create_reading(
    reading: SensorReadingCreate,
    db: Session = Depends(get_db)
):
    """Create a new sensor reading (used by IoT devices via MQTT or direct HTTP)"""
    # In production, this should be authenticated differently (API key, device token, etc.)
    db_reading = SensorReading(
        device_id=reading.device_id,
        ts=reading.ts,
        pm25=reading.pm25,
        pm10=reading.pm10,
        co2=reading.co2,
        voc_index=reading.voc_index,
        temp=reading.temp,
        humidity=reading.humidity
    )
    db.add(db_reading)
    db.commit()
    db.refresh(db_reading)
    return db_reading
