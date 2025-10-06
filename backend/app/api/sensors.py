from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.user import User
from app.models.sensor import SensorDevice, SensorReading
from app.schemas.sensor import SensorDeviceCreate, SensorDeviceResponse, SensorReadingCreate
from app.api.dependencies import get_current_user

router = APIRouter()


@router.get("/devices", response_model=List[SensorDeviceResponse])
async def list_devices(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all sensor devices for current user"""
    devices = db.query(SensorDevice).filter(
        SensorDevice.user_id == current_user.id
    ).all()
    return devices


@router.post("/devices", response_model=SensorDeviceResponse, status_code=status.HTTP_201_CREATED)
async def register_device(
    device_data: SensorDeviceCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Register a new sensor device"""
    device = SensorDevice(
        user_id=current_user.id,
        label=device_data.label,
        location_lat=device_data.location_lat,
        location_lon=device_data.location_lon,
        indoor=device_data.indoor,
        firmware_version=device_data.firmware_version
    )
    
    db.add(device)
    db.commit()
    db.refresh(device)
    
    return device


@router.post("/readings", status_code=status.HTTP_201_CREATED)
async def create_reading(
    reading_data: SensorReadingCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new sensor reading"""
    # Verify device belongs to user
    device = db.query(SensorDevice).filter(
        SensorDevice.id == reading_data.device_id,
        SensorDevice.user_id == current_user.id
    ).first()
    
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )
    
    reading = SensorReading(
        device_id=reading_data.device_id,
        ts=reading_data.ts,
        pm25=reading_data.pm25,
        pm10=reading_data.pm10,
        co2=reading_data.co2,
        voc_index=reading_data.voc_index,
        temp=reading_data.temp,
        humidity=reading_data.humidity
    )
    
    db.add(reading)
    db.commit()
    
    return {"status": "success", "message": "Reading recorded"}


@router.get("/readings")
async def get_readings(
    device_id: str,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get recent readings for a device"""
    # Verify device belongs to user
    device = db.query(SensorDevice).filter(
        SensorDevice.id == device_id,
        SensorDevice.user_id == current_user.id
    ).first()
    
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )
    
    readings = db.query(SensorReading).filter(
        SensorReading.device_id == device_id
    ).order_by(SensorReading.ts.desc()).limit(limit).all()
    
    return {"device_id": device_id, "readings": readings}
