# Environmental Health Platform

Personalized Environmental Health & Air Quality Decision Support Platform

## Overview

This platform provides personalized, predictive, and actionable environmental health intelligence by integrating:
- Indoor IoT sensors
- Public air quality data
- Weather information
- User health profiles
- Exposure modeling
- Route optimization
- Activity recommendations

## Features

### Phase 1 (MVP) - Implemented

- **User Authentication**: Secure JWT-based authentication with user profiles
- **Air Quality Monitoring**: Real-time outdoor air quality data with forecasting
- **Indoor Sensors**: Integration with IoT sensors for indoor air quality monitoring
- **Activity Recommendations**: Rule-based recommendations for outdoor activities (jogging, cycling, etc.)
- **Exposure Tracking**: Daily exposure logging and monitoring
- **Alert System**: Framework for threshold-based alerts
- **Route Planning**: Route exposure estimation

## Architecture

The platform consists of:
- **Backend**: FastAPI-based REST API with PostgreSQL database
- **Frontend**: React-based web dashboard with Material-UI
- **Database**: PostgreSQL with TimescaleDB extensions (recommended)
- **Message Queue**: MQTT for sensor data ingestion

## Quick Start

### Prerequisites

- Python 3.9+
- Node.js 16+
- PostgreSQL 12+
- (Optional) MQTT broker for sensor integration

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your configuration
alembic upgrade head
uvicorn app.main:app --reload
```

Backend will be available at http://localhost:8000

API documentation: http://localhost:8000/docs

### Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env
# Edit .env with backend API URL
npm start
```

Frontend will be available at http://localhost:3000

## Project Structure

```
env-health-platform/
├── backend/
│   ├── app/
│   │   ├── api/              # API endpoints
│   │   ├── models.py         # Database models
│   │   ├── schemas.py        # Pydantic schemas
│   │   ├── auth.py           # Authentication
│   │   ├── config.py         # Configuration
│   │   └── main.py           # FastAPI app
│   ├── alembic/              # Database migrations
│   └── requirements.txt      # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── App.js            # Main app
│   │   └── index.js          # Entry point
│   └── package.json          # Node dependencies
└── README.md
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get token
- `GET /api/auth/profile` - Get user profile
- `PUT /api/auth/profile` - Update user profile

### Air Quality
- `GET /api/aq/current` - Get current outdoor AQ
- `GET /api/aq/forecast` - Get AQ forecast

### Indoor Sensors
- `GET /api/indoor/devices` - List sensor devices
- `POST /api/indoor/devices` - Register new device
- `GET /api/indoor/readings` - Get sensor readings

### Activity & Exposure
- `POST /api/activity/recommend` - Get activity recommendation
- `GET /api/exposure/today` - Get today's exposure

### Routing & Alerts
- `POST /api/routing/plan` - Plan route with exposure
- `GET /api/alerts` - Get alert history

## Data Model

Key entities:
- **Users**: Health profiles with sensitivity levels
- **Sensor Devices**: Indoor air quality monitors
- **Sensor Readings**: Time-series sensor data
- **AQ External**: External air quality data
- **Forecasts**: Predicted air quality
- **Activity Recommendations**: Personalized activity suggestions
- **Exposure Logs**: Daily exposure tracking
- **Routes**: Route planning with exposure estimates
- **Alerts**: User notifications

## Development

### Running Tests

```bash
cd backend
pytest
```

### Code Style

```bash
cd backend
black app/
flake8 app/
```

## Specification

This implementation follows the comprehensive specification document that defines:
- 4-phase development roadmap
- Database schema
- API endpoints
- ML components (forecasting, risk classification, exposure estimation)
- Alert rules
- Activity recommendation algorithms
- Privacy and security requirements

See the full specification document for detailed requirements.

## Future Enhancements (Phase 2-4)

- LSTM-based forecasting
- Symptom diary correlation
- What-if activity scheduling
- Exposure budgets
- Pollen and wildfire layers
- Advanced ML models
- Smart home integration
- Multi-language support
- Community sensor network

## License

MIT License - see LICENSE file

## Disclaimer

This platform provides educational environmental risk information and does not constitute medical advice. Users should consult qualified healthcare professionals for diagnosis or treatment decisions.