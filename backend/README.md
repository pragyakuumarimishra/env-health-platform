# Environmental Health Platform - Backend

FastAPI backend for the Personalized Environmental Health & Air Quality Decision Support Platform.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Run database migrations:
```bash
alembic upgrade head
```

4. Start the development server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
backend/
├── app/
│   ├── api/              # API route handlers
│   │   ├── auth.py       # Authentication endpoints
│   │   ├── aq.py         # Air quality endpoints
│   │   ├── indoor.py     # Indoor sensor endpoints
│   │   ├── symptoms.py   # Symptom logging
│   │   ├── exposure.py   # Exposure tracking
│   │   ├── activity.py   # Activity recommendations
│   │   ├── routing.py    # Route planning
│   │   └── alerts.py     # Alert management
│   ├── main.py           # FastAPI application
│   ├── config.py         # Configuration settings
│   ├── database.py       # Database setup
│   ├── models.py         # SQLAlchemy models
│   ├── schemas.py        # Pydantic schemas
│   └── auth.py           # Authentication utilities
├── alembic/              # Database migrations
├── requirements.txt      # Python dependencies
└── .env.example          # Environment template
```

## API Endpoints

### Authentication
- POST `/api/auth/register` - Register new user
- POST `/api/auth/login` - Login and get token
- GET `/api/auth/profile` - Get user profile
- PUT `/api/auth/profile` - Update user profile

### Air Quality
- GET `/api/aq/current` - Get current outdoor AQ
- GET `/api/aq/forecast` - Get AQ forecast

### Indoor Sensors
- GET `/api/indoor/devices` - List sensor devices
- POST `/api/indoor/devices` - Register new device
- GET `/api/indoor/readings` - Get sensor readings
- POST `/api/indoor/readings` - Create reading (for IoT)

### Symptoms
- POST `/api/symptoms` - Log symptom
- GET `/api/symptoms` - Get symptom history

### Exposure
- GET `/api/exposure/today` - Get today's exposure

### Activity
- POST `/api/activity/recommend` - Get activity recommendation

### Routing
- POST `/api/routing/plan` - Plan route with exposure

### Alerts
- GET `/api/alerts` - Get alert history

## Development

The backend is built with:
- FastAPI - Modern Python web framework
- SQLAlchemy - ORM for database operations
- Alembic - Database migrations
- Pydantic - Data validation
- JWT - Token-based authentication
