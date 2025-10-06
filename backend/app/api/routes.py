from fastapi import APIRouter
from app.api import auth, aq, indoor, symptoms, exposure, activity, routing, alerts

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(aq.router, prefix="/aq", tags=["air-quality"])
router.include_router(indoor.router, prefix="/indoor", tags=["indoor-sensors"])
router.include_router(symptoms.router, prefix="/symptoms", tags=["symptoms"])
router.include_router(exposure.router, prefix="/exposure", tags=["exposure"])
router.include_router(activity.router, prefix="/activity", tags=["activity"])
router.include_router(routing.router, prefix="/routing", tags=["routing"])
router.include_router(alerts.router, prefix="/alerts", tags=["alerts"])
