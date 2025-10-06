from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Route, User
from app.schemas import RouteRequest, RouteResponse
from app.auth import get_current_user

router = APIRouter()


@router.post("/plan", response_model=RouteResponse)
def plan_route(
    route_request: RouteRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Calculate route with exposure estimate"""
    # Mock route calculation (in production, integrate with Mapbox/OpenRouteService)
    # Calculate simple exposure estimate based on PM2.5 concentration
    mock_pm25 = 15.0
    distance_km = (
        ((route_request.dest_lat - route_request.origin_lat) ** 2 +
         (route_request.dest_lon - route_request.origin_lon) ** 2) ** 0.5
    ) * 111  # rough km conversion
    
    time_minutes = int(distance_km * 12)  # ~5 km/h walking speed
    exposure_estimate = mock_pm25 * (time_minutes / 60.0)  # Simple exposure calc
    
    db_route = Route(
        user_id=current_user.id,
        origin_geo={"lat": route_request.origin_lat, "lon": route_request.origin_lon},
        dest_geo={"lat": route_request.dest_lat, "lon": route_request.dest_lon},
        route_geojson=None,  # In production, return actual route geometry
        time_minutes=time_minutes,
        exposure_estimate=exposure_estimate,
        alternative_rank=1
    )
    db.add(db_route)
    db.commit()
    db.refresh(db_route)
    
    return db_route
