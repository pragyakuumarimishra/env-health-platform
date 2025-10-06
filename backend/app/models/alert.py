from sqlalchemy import Column, String, Integer, TIMESTAMP, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid
from app.core.database import Base


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    ts = Column(TIMESTAMP(timezone=True), server_default=func.now())
    type = Column(String(100), nullable=False)
    payload = Column(JSONB, default={})
    channel = Column(String(50))  # sms, email, push
    status = Column(String(50), default="pending")  # pending, sent, failed


class ActivityRecommendation(Base):
    __tablename__ = "activity_recommendations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    ts = Column(TIMESTAMP(timezone=True), server_default=func.now())
    activity_type = Column(String(100), nullable=False)
    window_start = Column(TIMESTAMP(timezone=True))
    window_end = Column(TIMESTAMP(timezone=True))
    score = Column(Integer)
    rationale = Column(Text)
