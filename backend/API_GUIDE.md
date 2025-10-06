# API Usage Guide

## Environmental Health Platform API

This guide provides examples of how to use the Environmental Health Platform API.

## Base URL

```
http://localhost:8000/api
```

## Authentication

The API uses JWT (JSON Web Token) for authentication.

### Register a New User

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123",
    "name": "John Doe",
    "sensitivity_level": 3,
    "conditions": {
      "asthma": true,
      "allergies": ["pollen", "dust"]
    }
  }'
```

Response:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "name": "John Doe",
  "sensitivity_level": 3,
  "conditions": {
    "asthma": true,
    "allergies": ["pollen", "dust"]
  },
  "locale": "en"
}
```

### Login

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

## Profile Management

### Get User Profile

```bash
curl -X GET http://localhost:8000/api/profile \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Update User Profile

```bash
curl -X PUT http://localhost:8000/api/profile \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "sensitivity_level": 4,
    "conditions": {
      "asthma": true,
      "copd": false
    }
  }'
```

## Air Quality Data

### Get Current Air Quality

```bash
curl -X GET "http://localhost:8000/api/aq/current?lat=40.7128&lon=-74.0060" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

Response:
```json
{
  "location": {
    "lat": 40.7128,
    "lon": -74.0060
  },
  "air_quality": {
    "station_id": "NYC-Station-1",
    "pm25": 12.5,
    "pm10": 22.1,
    "no2": 15.3,
    "aqi": 52
  },
  "weather": {
    "temperature": 22.5,
    "humidity": 65.0,
    "pressure": 1013
  }
}
```

### Get Air Quality Forecast

```bash
curl -X GET "http://localhost:8000/api/aq/forecast?lat=40.7128&lon=-74.0060&hours=6" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Indoor Sensors

### Register a New Sensor Device

```bash
curl -X POST http://localhost:8000/api/indoor/devices \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "label": "Living Room Sensor",
    "location_lat": 40.7128,
    "location_lon": -74.0060,
    "indoor": true,
    "firmware_version": "1.0.0"
  }'
```

Response:
```json
{
  "id": "650e8400-e29b-41d4-a716-446655440001",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "label": "Living Room Sensor",
  "location_lat": 40.7128,
  "location_lon": -74.0060,
  "indoor": true,
  "firmware_version": "1.0.0",
  "created_at": "2025-01-15T10:30:00Z"
}
```

### List User's Sensor Devices

```bash
curl -X GET http://localhost:8000/api/indoor/devices \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Submit Sensor Reading

```bash
curl -X POST http://localhost:8000/api/indoor/readings \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "650e8400-e29b-41d4-a716-446655440001",
    "ts": "2025-01-15T10:35:00Z",
    "pm25": 12.4,
    "pm10": 22.1,
    "co2": 945,
    "voc_index": 112,
    "temp": 27.1,
    "humidity": 54.0
  }'
```

### Get Sensor Readings

```bash
curl -X GET "http://localhost:8000/api/indoor/readings?device_id=650e8400-e29b-41d4-a716-446655440001&limit=100" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Activity Recommendations

### Get Activity Recommendation

```bash
curl -X POST http://localhost:8000/api/activity/recommend \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "activity_type": "jogging",
    "lat": 40.7128,
    "lon": -74.0060
  }'
```

Response:
```json
{
  "activity_type": "jogging",
  "score": 85,
  "label": "Good",
  "rationale": "Conditions are acceptable. Minor concerns: PM2.5 is 12.5 µg/m³ (elevated)",
  "pm25": 12.5,
  "temperature": 22.5,
  "humidity": 65.0
}
```

### Activity Types Supported

- `jogging` / `running` - Outdoor jogging or running
- `walking` - Walking outdoors
- `cycling` - Cycling outdoors

### Score Interpretation

- **≥70 (Good)**: Favorable conditions for activity
- **40-69 (Caution)**: Exercise with caution
- **<40 (Avoid)**: Not recommended
- **0 (Not Recommended)**: Unsafe conditions (for sensitive individuals)

## Example: Complete Workflow

### 1. Register and Login

```bash
# Register
TOKEN=$(curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"runner@example.com","password":"run123456","name":"Jane Runner","sensitivity_level":2}' \
  | jq -r '.id')

# Login
TOKEN=$(curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"runner@example.com","password":"run123456"}' \
  | jq -r '.access_token')
```

### 2. Check Activity Recommendation

```bash
curl -X POST http://localhost:8000/api/activity/recommend \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"activity_type":"jogging","lat":40.7128,"lon":-74.0060}'
```

### 3. Register Indoor Sensor

```bash
DEVICE_ID=$(curl -X POST http://localhost:8000/api/indoor/devices \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"label":"Bedroom Sensor","indoor":true}' \
  | jq -r '.id')
```

### 4. Submit Sensor Data

```bash
curl -X POST http://localhost:8000/api/indoor/readings \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"device_id\":\"$DEVICE_ID\",\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"pm25\":15.2,\"co2\":850,\"temp\":23.5,\"humidity\":55.0}"
```

## Error Handling

### Common Error Responses

**401 Unauthorized**
```json
{
  "detail": "Invalid authentication credentials"
}
```

**404 Not Found**
```json
{
  "detail": "Device not found"
}
```

**400 Bad Request**
```json
{
  "detail": "Email already registered"
}
```

## Rate Limiting

Currently no rate limiting is implemented in Phase 1 MVP. This will be added in future phases.

## Support

For issues or questions, please open an issue on GitHub.
