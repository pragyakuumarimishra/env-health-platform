# Environmental Health Platform

Personalized Environmental Health & Air Quality Decision Support Platform

## Overview

This platform provides personalized, predictive, and actionable environmental health intelligence by integrating indoor IoT sensors, public air quality data, weather information, user health profiles, exposure modeling, route optimization, and a conversational decision-support assistant.

## Features (Phase 1 - MVP)

- **User Authentication**: Secure registration and login with JWT tokens
- **Health Profiles**: Personalized health conditions and sensitivity levels
- **Indoor Sensor Integration**: Support for IoT sensors tracking PM2.5, PM10, CO2, VOC, temperature, and humidity
- **External Air Quality Data**: Integration with OpenAQ and OpenWeatherMap APIs
- **Activity Recommendations**: Smart recommendations for outdoor activities (jogging, cycling, walking) based on environmental conditions
- **Real-time Monitoring**: Track both indoor and outdoor air quality in real-time

## Architecture

### Backend (FastAPI)
- **API Layer**: RESTful endpoints for all platform features
- **Authentication**: JWT-based secure authentication
- **Database**: PostgreSQL with SQLAlchemy ORM
- **External APIs**: Integration with OpenAQ and OpenWeatherMap
- **Business Logic**: Activity recommendation engine based on environmental factors

### Data Models
- Users with health profiles
- Sensor devices and readings
- External air quality data
- Forecasts (Phase 2)
- Alerts and activity recommendations
- Symptom and exposure logs

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get JWT token

### Profile
- `GET /api/profile` - Get user profile
- `PUT /api/profile` - Update user profile

### Air Quality
- `GET /api/aq/current` - Get current air quality for location
- `GET /api/aq/forecast` - Get air quality forecast (Phase 2)

### Indoor Sensors
- `GET /api/indoor/devices` - List user's sensor devices
- `POST /api/indoor/devices` - Register new sensor device
- `POST /api/indoor/readings` - Submit sensor reading
- `GET /api/indoor/readings` - Get sensor readings

### Activity Recommendations
- `POST /api/activity/recommend` - Get activity recommendation

## Installation

### Prerequisites
- Python 3.9+
- PostgreSQL 12+
- Redis (optional, for caching)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/pragyakuumarimishra/env-health-platform.git
   cd env-health-platform
   ```

2. **Set up backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Set up database**
   ```bash
   # Create PostgreSQL database
   createdb env_health_platform
   ```

5. **Run the application**
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

6. **Access the API**
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

## Configuration

Copy `.env.example` to `.env` and configure:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/env_health_platform
SECRET_KEY=your-secret-key-here
OPENAQ_API_KEY=your-openaq-key (optional)
OPENWEATHER_API_KEY=your-openweather-key (optional)
```

## Activity Recommendation Logic

The platform implements intelligent activity recommendations based on:

### Jogging/Running Score Calculation
- Base score: 100
- Deductions:
  - PM2.5 > 10 µg/m³: -1 point per µg/m³ above 10
  - Humidity > 85%: -10 points
  - Temperature > 32°C or < 5°C: -15 points
- Hard stop: If user has sensitivity ≥3 and PM2.5 > 25 µg/m³, activity is "Not Recommended"

### Score Interpretation
- **≥70**: Good - Favorable conditions
- **40-69**: Caution - Exercise with caution
- **<40**: Avoid - Not recommended
- **0**: Not Recommended - Unsafe conditions

## External Data Sources

- **OpenAQ**: Global air quality data (PM2.5, PM10, NO2, O3, SO2)
- **OpenWeatherMap**: Weather data (temperature, humidity, pressure)

## Future Phases

### Phase 2
- Short-term forecasting (ARIMA/LSTM models)
- Symptom diary with exposure correlation
- Route exposure optimization
- Basic chat assistant

### Phase 3
- What-if scheduling
- Exposure budgets
- Pollen & wildfire layers
- Advanced alert logic

### Phase 4
- Crowd-sourced micro-sensors
- Adaptive learning
- Smart home integration
- Multi-language support

## Testing

```bash
# Run tests (when implemented)
pytest
```

## API Documentation

Interactive API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## License

MIT License - See LICENSE file for details

## Disclaimer

This platform provides educational environmental risk information and does not constitute medical advice. Users should consult qualified healthcare professionals for diagnosis or treatment decisions.

## Contact

For questions or support, please open an issue on GitHub