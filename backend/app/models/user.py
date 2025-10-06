from sqlalchemy import Column, String, Date, Integer, Text, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(50))
    password_hash = Column(Text, nullable=False)
    name = Column(String(255))
    dob = Column(Date)
    conditions = Column(JSONB, default={})  # Health conditions
    sensitivity_level = Column(Integer, default=1)  # 1-5 scale
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    locale = Column(String(10), default="en")
