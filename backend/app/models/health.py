from sqlalchemy import Column, String, Float, Integer, Date, BigInteger, TIMESTAMP, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid
from app.core.database import Base


class SymptomLog(Base):
    __tablename__ = "symptom_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    ts = Column(TIMESTAMP(timezone=True), server_default=func.now())
    symptoms = Column(JSONB, default={})
    severity = Column(Integer)  # 1-10 scale
    notes = Column(Text)


class ExposureLog(Base):
    __tablename__ = "exposure_logs"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)
    cumulative_pm25 = Column(Float)
    cumulative_no2 = Column(Float)
    risk_score = Column(Integer)
