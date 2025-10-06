from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import SymptomLog, User
from app.schemas import SymptomLogCreate, SymptomLogResponse
from app.auth import get_current_user

router = APIRouter()


@router.post("", response_model=SymptomLogResponse)
def log_symptom(
    symptom: SymptomLogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Log a symptom entry"""
    db_symptom = SymptomLog(
        user_id=current_user.id,
        ts=symptom.ts,
        symptoms=symptom.symptoms,
        severity=symptom.severity,
        notes=symptom.notes
    )
    db.add(db_symptom)
    db.commit()
    db.refresh(db_symptom)
    return db_symptom


@router.get("", response_model=List[SymptomLogResponse])
def get_symptoms(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get symptom history for the current user"""
    symptoms = db.query(SymptomLog).filter(
        SymptomLog.user_id == current_user.id
    ).order_by(SymptomLog.ts.desc()).all()
    return symptoms
