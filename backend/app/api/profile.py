from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate
from app.api.dependencies import get_current_user

router = APIRouter()


@router.get("", response_model=UserResponse)
async def get_profile(current_user: User = Depends(get_current_user)):
    """Get current user's profile"""
    return current_user


@router.put("", response_model=UserResponse)
async def update_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user's profile"""
    # Update fields if provided
    if user_update.name is not None:
        current_user.name = user_update.name
    if user_update.phone is not None:
        current_user.phone = user_update.phone
    if user_update.dob is not None:
        current_user.dob = user_update.dob
    if user_update.conditions is not None:
        current_user.conditions = user_update.conditions
    if user_update.sensitivity_level is not None:
        current_user.sensitivity_level = user_update.sensitivity_level
    
    db.commit()
    db.refresh(current_user)
    
    return current_user
