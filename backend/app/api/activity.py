from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models import ActivityRecommendation, User
from app.schemas import ActivityRecommendationRequest, ActivityRecommendationResponse
from app.auth import get_current_user

router = APIRouter()


def jogging_score(pm25: float, humidity: float, temp_c: float, sensitive: bool) -> tuple:
    """
    Calculate jogging feasibility score based on air quality and weather.
    From specification section 24.
    """
    score = 100
    
    if pm25 > 10:
        score -= (pm25 - 10)
    
    if humidity > 85:
        score -= 10
    
    if temp_c > 32 or temp_c < 5:
        score -= 15
    
    if sensitive and pm25 > 25:
        return 0, "Not Recommended (sensitivity + elevated PM2.5)"
    
    if score >= 70:
        label = "Good"
    elif score >= 40:
        label = "Caution"
    else:
        label = "Avoid"
    
    return score, label


@router.post("/recommend", response_model=ActivityRecommendationResponse)
def recommend_activity(
    request: ActivityRecommendationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get activity recommendation based on current/forecasted conditions"""
    # Mock environmental data (in production, fetch from AQ and weather APIs)
    pm25 = 15.0
    humidity = 60.0
    temp_c = 22.0
    sensitive = current_user.sensitivity_level >= 3
    
    if request.activity_type.lower() == "jogging":
        score, rationale = jogging_score(pm25, humidity, temp_c, sensitive)
    else:
        # Generic activity scoring
        score = 75
        rationale = f"{request.activity_type} conditions are generally favorable"
    
    db_recommendation = ActivityRecommendation(
        user_id=current_user.id,
        activity_type=request.activity_type,
        window_start=request.preferred_time or datetime.utcnow(),
        window_end=None,
        score=score,
        rationale=rationale
    )
    db.add(db_recommendation)
    db.commit()
    db.refresh(db_recommendation)
    
    return db_recommendation
