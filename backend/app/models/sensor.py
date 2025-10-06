from sqlalchemy import Column, String, Float, Boolean, ForeignKey, BigInteger, TIMESTAMP, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid
from app.core.database import Base


class SensorDevice(Base):
    __tablename__ = "sensor_devices"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    label = Column(String(255))
    location_lat = Column(Float)
    location_lon = Column(Float)
    indoor = Column(Boolean, default=True)
    firmware_version = Column(String(50))
    calibration = Column(JSONB, default={})
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())


class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    device_id = Column(UUID(as_uuid=True), ForeignKey("sensor_devices.id"), nullable=False)
    ts = Column(TIMESTAMP(timezone=True), nullable=False)
    pm25 = Column(Float)
    pm10 = Column(Float)
    co2 = Column(Float)
    voc_index = Column(Float)
    temp = Column(Float)
    humidity = Column(Float)
