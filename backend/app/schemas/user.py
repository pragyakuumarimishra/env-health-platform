from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict
from datetime import date
from uuid import UUID


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    name: Optional[str] = None
    phone: Optional[str] = None
    dob: Optional[date] = None
    conditions: Optional[Dict] = None
    sensitivity_level: int = Field(default=1, ge=1, le=5)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: UUID
    email: str
    name: Optional[str]
    phone: Optional[str]
    dob: Optional[date]
    conditions: Optional[Dict]
    sensitivity_level: int
    locale: str

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    dob: Optional[date] = None
    conditions: Optional[Dict] = None
    sensitivity_level: Optional[int] = Field(None, ge=1, le=5)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
