from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, ForeignKey, JSON, Date, BigInteger, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False, index=True)
    phone = Column(String, nullable=True)
    password_hash = Column(String, nullable=False)
    name = Column(String, nullable=True)
    dob = Column(Date, nullable=True)
    conditions = Column(JSON, nullable=True)
    sensitivity_level = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    locale = Column(String, default="en")

    sensor_devices = relationship("SensorDevice", back_populates="user")
    symptom_logs = relationship("SymptomLog", back_populates="user")
    exposure_logs = relationship("ExposureLog", back_populates="user")
    routes = relationship("Route", back_populates="user")
    alerts = relationship("Alert", back_populates="user")
    activity_recommendations = relationship("ActivityRecommendation", back_populates="user")


class SensorDevice(Base):
    __tablename__ = "sensor_devices"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    label = Column(String, nullable=False)
    location_lat = Column(Float, nullable=True)
    location_lon = Column(Float, nullable=True)
    indoor = Column(Boolean, default=True)
    firmware_version = Column(String, nullable=True)
    calibration = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="sensor_devices")
    readings = relationship("SensorReading", back_populates="device")


class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    device_id = Column(UUID(as_uuid=True), ForeignKey("sensor_devices.id"), nullable=False)
    ts = Column(DateTime, nullable=False, index=True)
    pm25 = Column(Float, nullable=True)
    pm10 = Column(Float, nullable=True)
    co2 = Column(Float, nullable=True)
    voc_index = Column(Float, nullable=True)
    temp = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)

    device = relationship("SensorDevice", back_populates="readings")


class AQExternal(Base):
    __tablename__ = "aq_external"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    source = Column(String, nullable=False)
    station_id = Column(String, nullable=True)
    ts = Column(DateTime, nullable=False, index=True)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    pm25 = Column(Float, nullable=True)
    pm10 = Column(Float, nullable=True)
    no2 = Column(Float, nullable=True)
    o3 = Column(Float, nullable=True)
    so2 = Column(Float, nullable=True)
    aqi = Column(Integer, nullable=True)


class Forecast(Base):
    __tablename__ = "forecasts"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    model_version = Column(String, nullable=False)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    ts_target = Column(DateTime, nullable=False, index=True)
    pm25_p10 = Column(Float, nullable=True)
    pm25_p50 = Column(Float, nullable=True)
    pm25_p90 = Column(Float, nullable=True)
    no2_p50 = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class SymptomLog(Base):
    __tablename__ = "symptom_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    ts = Column(DateTime, nullable=False)
    symptoms = Column(JSON, nullable=False)
    severity = Column(Integer, nullable=False)
    notes = Column(Text, nullable=True)

    user = relationship("User", back_populates="symptom_logs")


class ExposureLog(Base):
    __tablename__ = "exposure_logs"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)
    cumulative_pm25 = Column(Float, nullable=True)
    cumulative_no2 = Column(Float, nullable=True)
    risk_score = Column(Integer, nullable=True)

    user = relationship("User", back_populates="exposure_logs")


class Route(Base):
    __tablename__ = "routes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    origin_geo = Column(JSON, nullable=False)
    dest_geo = Column(JSON, nullable=False)
    route_geojson = Column(JSON, nullable=True)
    time_minutes = Column(Integer, nullable=True)
    exposure_estimate = Column(Float, nullable=True)
    alternative_rank = Column(Integer, nullable=True)

    user = relationship("User", back_populates="routes")


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    ts = Column(DateTime, default=datetime.utcnow)
    type = Column(String, nullable=False)
    payload = Column(JSON, nullable=False)
    channel = Column(String, nullable=False)
    status = Column(String, default="pending")

    user = relationship("User", back_populates="alerts")


class ActivityRecommendation(Base):
    __tablename__ = "activity_recommendations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    ts = Column(DateTime, default=datetime.utcnow)
    activity_type = Column(String, nullable=False)
    window_start = Column(DateTime, nullable=True)
    window_end = Column(DateTime, nullable=True)
    score = Column(Integer, nullable=True)
    rationale = Column(Text, nullable=True)

    user = relationship("User", back_populates="activity_recommendations")
