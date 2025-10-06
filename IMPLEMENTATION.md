# Implementation Details

## Overview

This document describes the implementation of the Environmental Health Platform MVP (Phase 1) based on the comprehensive specification document.

## Architecture

### Backend (FastAPI)

```
backend/
├── app/
│   ├── api/                      # API route handlers
│   │   ├── auth.py              # Authentication endpoints
│   │   ├── aq.py                # Air quality data endpoints
│   │   ├── indoor.py            # Indoor sensor endpoints
│   │   ├── symptoms.py          # Symptom logging
│   │   ├── exposure.py          # Exposure tracking
│   │   ├── activity.py          # Activity recommendations
│   │   ├── routing.py           # Route planning
│   │   └── alerts.py            # Alert management
│   ├── main.py                  # FastAPI application
│   ├── config.py                # Configuration settings
│   ├── database.py              # Database connection
│   ├── models.py                # SQLAlchemy models
│   ├── schemas.py               # Pydantic schemas
│   └── auth.py                  # Authentication utilities
├── alembic/                     # Database migrations
├── examples/                    # Example scripts
│   └── sensor_simulator.py     # Mock sensor data generator
└── requirements.txt             # Python dependencies
```

### Frontend (React)

```
frontend/
├── src/
│   ├── components/
│   │   ├── Dashboard.js                # Main dashboard
│   │   ├── Login.js                    # Authentication UI
│   │   ├── AirQualityDisplay.js        # AQ visualization
│   │   ├── IndoorSensors.js            # Sensor management
│   │   └── ActivityRecommendation.js   # Activity suggestions
│   ├── App.js                   # Main application component
│   └── index.js                 # Entry point
├── public/
│   └── index.html               # HTML template
└── package.json                 # Node dependencies
```

## Database Schema

Implemented as per specification Section 12:

### Core Tables

1. **users**: User profiles with health data
   - UUID primary key
   - Email, phone, password_hash
   - Health conditions (JSONB)
   - Sensitivity level (1-5)
   - Preferences and locale

2. **sensor_devices**: IoT sensor registration
   - Device ID (UUID)
   - User association
   - Location (lat/lon)
   - Indoor/outdoor flag
   - Firmware version
   - Calibration data

3. **sensor_readings**: Time-series sensor data
   - Device association
   - Timestamp
   - PM2.5, PM10, CO2, VOC
   - Temperature, humidity

4. **aq_external**: External air quality data
   - Source identifier
   - Station ID
   - Timestamp and location
   - PM2.5, PM10, NO2, O3, SO2
   - AQI value

5. **forecasts**: Air quality predictions
   - Model version
   - Target timestamp
   - Location
   - Percentile predictions (p10, p50, p90)

6. **symptom_logs**: User symptom tracking
   - User association
   - Timestamp
   - Symptom data (JSONB)
   - Severity rating
   - Notes

7. **exposure_logs**: Daily exposure tracking
   - User and date
   - Cumulative PM2.5 and NO2
   - Risk score

8. **routes**: Route planning history
   - User association
   - Origin and destination
   - Route geometry (GeoJSON)
   - Time and exposure estimates

9. **alerts**: User notifications
   - Alert type and payload
   - Channel (SMS/email/push)
   - Status tracking

10. **activity_recommendations**: Activity suggestions
    - User and activity type
    - Time window
    - Score and rationale

## API Implementation

All endpoints from specification Section 13 are implemented:

### Authentication (`/api/auth/`)
- `POST /register`: User registration with validation
- `POST /login`: OAuth2 password flow, returns JWT
- `GET /profile`: Get authenticated user profile
- `PUT /profile`: Update user profile

### Air Quality (`/api/aq/`)
- `GET /current?lat={}&lon={}`: Current AQ for location
- `GET /forecast?lat={}&lon={}&hours={}`: Short-term forecast

### Indoor Sensors (`/api/indoor/`)
- `GET /devices`: List user's sensors
- `POST /devices`: Register new sensor
- `GET /readings?device_id={}&hours={}`: Query sensor data
- `POST /readings`: Ingest sensor reading (for IoT devices)

### Symptoms (`/api/symptoms/`)
- `POST /`: Log symptom entry
- `GET /`: Get symptom history

### Exposure (`/api/exposure/`)
- `GET /today`: Get today's cumulative exposure

### Activity (`/api/activity/`)
- `POST /recommend`: Get activity recommendation

### Routing (`/api/routing/`)
- `POST /plan`: Calculate route with exposure

### Alerts (`/api/alerts/`)
- `GET /`: Get alert history

## Algorithm Implementations

### Jogging Score (Section 24 of spec)

```python
def jogging_score(pm25, humidity, temp_c, sensitive):
    score = 100
    
    # Penalize elevated PM2.5
    if pm25 > 10:
        score -= (pm25 - 10)
    
    # Penalize high humidity
    if humidity > 85:
        score -= 10
    
    # Penalize extreme temperatures
    if temp_c > 32 or temp_c < 5:
        score -= 15
    
    # Hard stop for sensitive users
    if sensitive and pm25 > 25:
        return 0, "Not Recommended"
    
    # Classification
    if score >= 70:
        return score, "Good"
    elif score >= 40:
        return score, "Caution"
    else:
        return score, "Avoid"
```

## Security Features

1. **Authentication**: JWT tokens with configurable expiration
2. **Password Hashing**: Bcrypt via passlib
3. **CORS**: Configured for frontend origin
4. **Input Validation**: Pydantic schemas on all endpoints
5. **Authorization**: Token-based access control

## Mock Data

Since this is MVP without external API integration yet, endpoints return mock data when database is empty:

- Air quality: Returns sample AQI 50 data
- Forecasts: Generates 6-hour forecast with reasonable values
- Activity recommendations: Uses mock environmental conditions

## Development Setup

### Quick Start with Docker

```bash
# Start services
docker-compose up -d

# Setup and run
./setup.sh

# Backend
cd backend
alembic upgrade head
uvicorn app.main:app --reload

# Frontend (in new terminal)
cd frontend
npm start
```

### Manual Setup

**Backend:**
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with database URL
alembic upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
cp .env.example .env
npm start
```

## Testing

### Manual Testing with Sensor Simulator

```bash
cd backend/examples
python sensor_simulator.py
```

This simulates an IoT device sending readings to the platform.

### API Testing

Visit http://localhost:8000/docs for interactive API documentation (Swagger UI).

Example flow:
1. Register user: `POST /api/auth/register`
2. Login: `POST /api/auth/login`
3. Get AQ data: `GET /api/aq/current?lat=40.7128&lon=-74.0060`
4. Register sensor: `POST /api/indoor/devices`
5. Get recommendation: `POST /api/activity/recommend`

## Configuration

### Backend Environment Variables

```env
DATABASE_URL=postgresql://user:password@localhost:5432/envhealth
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
MQTT_BROKER=localhost
MQTT_PORT=1883
OPENWEATHER_API_KEY=optional-api-key
WAQI_API_KEY=optional-api-key
```

### Frontend Environment Variables

```env
REACT_APP_API_URL=http://localhost:8000/api
```

## Data Flow

1. **User Registration/Login**: Frontend → Auth API → Database
2. **Air Quality Display**: Frontend → AQ API → (Mock/Database) → Frontend
3. **Sensor Data**: IoT Device → Indoor API → Database → Frontend
4. **Activity Recommendation**: Frontend → Activity API → Algorithm → Database → Frontend

## Differences from Full Specification

The MVP implements core Phase 1 features. Not yet implemented:

- External API integration (OpenWeatherMap, WAQI, etc.)
- Real-time forecasting models (ARIMA/LSTM)
- MQTT sensor ingestion pipeline
- WebSocket real-time updates
- Advanced route optimization
- What-if scheduling
- Exposure budgets
- Pollen and wildfire data
- Chat assistant

These are planned for Phase 2-4 as per the specification roadmap.

## Performance Considerations

Current implementation:
- Single-region deployment
- Synchronous API calls
- In-memory mock data when DB empty
- No caching layer active

Production improvements needed:
- Redis caching for AQ data
- Background task queue for ingestion
- Database connection pooling
- Rate limiting
- CDN for frontend assets

## Next Steps

To make this production-ready:

1. **External API Integration**: Connect to OpenWeatherMap, WAQI, OpenAQ
2. **Forecasting**: Implement ARIMA baseline forecasting
3. **MQTT Ingestion**: Set up sensor data pipeline
4. **Alerts**: Implement alert evaluation and dispatch
5. **Testing**: Add unit and integration tests
6. **Monitoring**: Set up logging and metrics
7. **Deployment**: Containerize and deploy to cloud
8. **Documentation**: API documentation and user guides

## Contributing

When extending this implementation:
1. Follow existing code structure
2. Add Pydantic schemas for new endpoints
3. Update database models via Alembic migrations
4. Document new endpoints in README
5. Maintain consistency with specification document
