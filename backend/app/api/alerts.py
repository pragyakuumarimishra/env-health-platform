from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Alert, User
from app.schemas import AlertResponse
from app.auth import get_current_user

router = APIRouter()


@router.get("", response_model=List[AlertResponse])
def get_alerts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get alert history for the current user"""
    alerts = db.query(Alert).filter(
        Alert.user_id == current_user.id
    ).order_by(Alert.ts.desc()).limit(50).all()
    return alerts
