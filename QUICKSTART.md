# Quick Start Guide

Get the Environmental Health Platform up and running in minutes!

## Option 1: Docker (Recommended)

### Prerequisites
- Docker and Docker Compose installed
- 4GB RAM available

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/pragyakuumarimishra/env-health-platform.git
   cd env-health-platform
   ```

2. **Start the platform**
   ```bash
   docker-compose up -d
   ```

3. **Verify services are running**
   ```bash
   docker-compose ps
   ```

4. **Access the API**
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs

5. **Create your first user**
   ```bash
   curl -X POST http://localhost:8000/api/auth/register \
     -H "Content-Type: application/json" \
     -d '{
       "email": "user@example.com",
       "password": "securepass123",
       "name": "Test User",
       "sensitivity_level": 2
     }'
   ```

6. **Login and get token**
   ```bash
   curl -X POST http://localhost:8000/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{
       "email": "user@example.com",
       "password": "securepass123"
     }'
   ```

7. **Test activity recommendation**
   ```bash
   # Replace YOUR_TOKEN with the token from login
   curl -X POST http://localhost:8000/api/activity/recommend \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "activity_type": "jogging",
       "lat": 40.7128,
       "lon": -74.0060
     }'
   ```

## Option 2: Local Development

### Prerequisites
- Python 3.9 or higher
- PostgreSQL 12 or higher
- pip and virtualenv

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/pragyakuumarimishra/env-health-platform.git
   cd env-health-platform
   ```

2. **Set up database**
   ```bash
   # Start PostgreSQL service
   sudo service postgresql start
   
   # Create database
   createdb env_health_platform
   ```

3. **Set up Python environment**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   nano .env
   ```

5. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

6. **Access the API**
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs

## Testing the Platform

### 1. Register a User
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "runner@example.com",
    "password": "run123456",
    "name": "Jane Runner",
    "sensitivity_level": 3,
    "conditions": {"asthma": true}
  }'
```

### 2. Login
```bash
TOKEN=$(curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "runner@example.com",
    "password": "run123456"
  }' | jq -r '.access_token')

echo "Token: $TOKEN"
```

### 3. Get Profile
```bash
curl -X GET http://localhost:8000/api/profile \
  -H "Authorization: Bearer $TOKEN"
```

### 4. Check Air Quality
```bash
# New York City coordinates
curl -X GET "http://localhost:8000/api/aq/current?lat=40.7128&lon=-74.0060" \
  -H "Authorization: Bearer $TOKEN"
```

### 5. Get Activity Recommendation
```bash
curl -X POST http://localhost:8000/api/activity/recommend \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "activity_type": "jogging",
    "lat": 40.7128,
    "lon": -74.0060
  }'
```

### 6. Register Indoor Sensor
```bash
DEVICE_ID=$(curl -X POST http://localhost:8000/api/indoor/devices \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "label": "Living Room Sensor",
    "indoor": true,
    "location_lat": 40.7128,
    "location_lon": -74.0060,
    "firmware_version": "1.0.0"
  }' | jq -r '.id')

echo "Device ID: $DEVICE_ID"
```

### 7. Submit Sensor Reading
```bash
curl -X POST http://localhost:8000/api/indoor/readings \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"device_id\": \"$DEVICE_ID\",
    \"ts\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",
    \"pm25\": 15.2,
    \"pm10\": 28.5,
    \"co2\": 850,
    \"voc_index\": 120,
    \"temp\": 23.5,
    \"humidity\": 55.0
  }"
```

### 8. Get Sensor Readings
```bash
curl -X GET "http://localhost:8000/api/indoor/readings?device_id=$DEVICE_ID&limit=10" \
  -H "Authorization: Bearer $TOKEN"
```

## API Endpoints Overview

### Authentication
- `POST /api/auth/register` - Create account
- `POST /api/auth/login` - Get JWT token

### Profile
- `GET /api/profile` - View profile
- `PUT /api/profile` - Update profile

### Air Quality
- `GET /api/aq/current` - Current AQ data
- `GET /api/aq/forecast` - Forecast (Phase 2)

### Indoor Sensors
- `GET /api/indoor/devices` - List devices
- `POST /api/indoor/devices` - Register device
- `POST /api/indoor/readings` - Submit reading
- `GET /api/indoor/readings` - Query readings

### Activity
- `POST /api/activity/recommend` - Get recommendation

## Configuring External APIs

To get real air quality and weather data:

1. **Get API Keys**
   - OpenAQ: https://openaq.org/ (optional, has free tier)
   - OpenWeatherMap: https://openweathermap.org/api (free tier available)

2. **Update .env file**
   ```bash
   OPENAQ_API_KEY=your-openaq-key
   OPENWEATHER_API_KEY=your-openweather-key
   ```

3. **Restart the application**
   ```bash
   # Docker
   docker-compose restart backend
   
   # Local
   # Stop with Ctrl+C and restart
   uvicorn app.main:app --reload
   ```

## Stopping the Platform

### Docker
```bash
# Stop services
docker-compose stop

# Stop and remove containers
docker-compose down

# Stop and remove containers + volumes (clears database)
docker-compose down -v
```

### Local
```bash
# Press Ctrl+C in terminal running uvicorn
```

## Troubleshooting

### Docker Issues

**Port already in use**
```bash
# Check what's using port 8000
lsof -i :8000

# Change port in docker-compose.yml or stop conflicting service
```

**Database connection error**
```bash
# Check PostgreSQL is running
docker-compose ps postgres

# View logs
docker-compose logs postgres
```

### Local Development Issues

**Module not found**
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall requirements
pip install -r requirements.txt
```

**Database connection error**
```bash
# Check PostgreSQL is running
sudo service postgresql status

# Verify database exists
psql -l | grep env_health
```

**Permission denied on run.sh**
```bash
chmod +x run.sh
```

## Next Steps

1. **Explore API Documentation**: http://localhost:8000/docs
2. **Read the full README**: See [README.md](README.md)
3. **Check Architecture**: See [ARCHITECTURE.md](ARCHITECTURE.md)
4. **Sensor Integration**: See [SENSOR_INTEGRATION.md](SENSOR_INTEGRATION.md)
5. **API Usage Guide**: See [backend/API_GUIDE.md](backend/API_GUIDE.md)

## Getting Help

- **Issues**: Open an issue on GitHub
- **Documentation**: Check the docs folder
- **API Docs**: http://localhost:8000/docs

## What's Next?

The platform is now running! You can:
- Test different activity types (jogging, walking, cycling)
- Experiment with different locations
- Register multiple sensor devices
- Update user sensitivity levels
- Explore the interactive API documentation

Happy coding! 🌍💨
