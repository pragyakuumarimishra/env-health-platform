from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date
from app.database import get_db
from app.models import ExposureLog, User
from app.schemas import ExposureLogResponse
from app.auth import get_current_user

router = APIRouter()


@router.get("/today", response_model=ExposureLogResponse)
def get_today_exposure(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get daily cumulative exposure for today"""
    today = date.today()
    exposure = db.query(ExposureLog).filter(
        ExposureLog.user_id == current_user.id,
        ExposureLog.date == today
    ).first()
    
    if not exposure:
        # Return mock data if no exposure logged yet
        return ExposureLogResponse(
            date=today,
            cumulative_pm25=50.0,
            cumulative_no2=20.0,
            risk_score=30
        )
    
    return exposure
