from fastapi import APIRouter
from app.api import auth, profile, air_quality, sensors, activity

router = APIRouter()

# Include all sub-routers
router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
router.include_router(profile.router, prefix="/profile", tags=["Profile"])
router.include_router(air_quality.router, prefix="/aq", tags=["Air Quality"])
router.include_router(sensors.router, prefix="/indoor", tags=["Indoor Sensors"])
router.include_router(activity.router, prefix="/activity", tags=["Activity Recommendations"])
