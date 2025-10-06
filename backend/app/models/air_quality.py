from sqlalchemy import Column, String, Float, Integer, BigInteger, TIMESTAMP, Text
from sqlalchemy.sql import func
from app.core.database import Base


class AirQualityExternal(Base):
    __tablename__ = "aq_external"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    source = Column(String(100), nullable=False)
    station_id = Column(String(255))
    ts = Column(TIMESTAMP(timezone=True), nullable=False)
    lat = Column(Float)
    lon = Column(Float)
    pm25 = Column(Float)
    pm10 = Column(Float)
    no2 = Column(Float)
    o3 = Column(Float)
    so2 = Column(Float)
    aqi = Column(Integer)


class Forecast(Base):
    __tablename__ = "forecasts"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    model_version = Column(String(100))
    lat = Column(Float)
    lon = Column(Float)
    ts_target = Column(TIMESTAMP(timezone=True), nullable=False)
    pm25_p10 = Column(Float)  # 10th percentile
    pm25_p50 = Column(Float)  # Median
    pm25_p90 = Column(Float)  # 90th percentile
    no2_p50 = Column(Float)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
