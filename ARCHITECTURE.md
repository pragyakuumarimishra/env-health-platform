# System Architecture

## Overview

The Environmental Health Platform follows a layered architecture designed for scalability, maintainability, and extensibility.

## Architecture Layers

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend Layer                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Web Client  │  │ Mobile App   │  │  Dashboard   │     │
│  │   (React)    │  │  (Flutter)   │  │     UI       │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            ↓ HTTP/WebSocket
┌─────────────────────────────────────────────────────────────┐
│                      API Gateway                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              FastAPI Application                     │  │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐  │  │
│  │  │  Auth   │ │ Profile │ │   AQ    │ │ Sensors │  │  │
│  │  │ Routes  │ │ Routes  │ │ Routes  │ │ Routes  │  │  │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘  │  │
│  │  ┌─────────┐ ┌─────────┐                          │  │
│  │  │Activity │ │  Alert  │                          │  │
│  │  │ Routes  │ │ Routes  │                          │  │
│  │  └─────────┘ └─────────┘                          │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    Business Logic Layer                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Activity   │  │   External   │  │    Alert     │     │
│  │   Service    │  │  API Service │  │   Service    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                     Data Access Layer                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  SQLAlchemy  │  │    Models    │  │   Schemas    │     │
│  │     ORM      │  │              │  │  (Pydantic)  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    Data Storage Layer                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  PostgreSQL  │  │     Redis    │  │  TimescaleDB │     │
│  │  (Relational)│  │    (Cache)   │  │ (Time-series)│     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    External Services                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   OpenAQ     │  │ OpenWeather  │  │  MQTT Broker │     │
│  │     API      │  │     API      │  │   (Sensors)  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

## Components

### 1. Frontend Layer
- **Web Client**: React-based dashboard for desktop users
- **Mobile App**: Flutter-based mobile application (Phase 2+)
- **Dashboard UI**: Real-time data visualization

### 2. API Gateway (FastAPI)
- RESTful API endpoints
- JWT-based authentication
- Request validation with Pydantic
- Auto-generated API documentation (Swagger/OpenAPI)

### 3. Business Logic Layer

#### Activity Service
- Calculates activity recommendations
- Implements scoring algorithms
- Handles user sensitivity profiles

#### External API Service
- Fetches air quality data from OpenAQ
- Retrieves weather data from OpenWeatherMap
- Caches responses to minimize API calls
- Handles API rate limiting

#### Alert Service (Phase 2)
- Rule-based alert evaluation
- Threshold monitoring
- Multi-channel notifications

### 4. Data Access Layer

#### Models (SQLAlchemy)
- User, SensorDevice, SensorReading
- AirQualityExternal, Forecast
- Alert, ActivityRecommendation
- SymptomLog, ExposureLog

#### Schemas (Pydantic)
- Request/response validation
- Type checking
- Serialization/deserialization

### 5. Data Storage

#### PostgreSQL
- Primary relational database
- User accounts and profiles
- Sensor metadata
- Historical data

#### Redis (Optional)
- Caching layer
- Session storage
- Rate limiting counters
- Real-time data buffer

#### TimescaleDB (Phase 2+)
- Time-series optimization
- Sensor readings
- Air quality measurements
- Performance analytics

### 6. External Services

#### OpenAQ API
- Global air quality data
- PM2.5, PM10, NO2, O3, SO2
- Historical data access

#### OpenWeatherMap API
- Current weather conditions
- Temperature, humidity, pressure
- Weather forecasts

#### MQTT Broker (Phase 2)
- IoT sensor communication
- Real-time data ingestion
- Pub/sub messaging

## Data Flow

### 1. User Registration & Authentication
```
User → POST /api/auth/register → Validate → Hash Password → Store in DB → Return User
User → POST /api/auth/login → Validate → Check Password → Generate JWT → Return Token
```

### 2. Activity Recommendation
```
User → POST /api/activity/recommend
    ↓
Fetch External Data (OpenAQ + OpenWeather)
    ↓
Calculate Activity Score (Business Logic)
    ↓
Apply User Sensitivity Profile
    ↓
Return Recommendation
```

### 3. Sensor Data Ingestion
```
IoT Device → POST /api/indoor/readings
    ↓
Authenticate User
    ↓
Validate Device Ownership
    ↓
Store Reading in Database
    ↓
Trigger Alert Rules (if applicable)
    ↓
Return Success
```

### 4. Air Quality Query
```
User → GET /api/aq/current?lat=X&lon=Y
    ↓
Check Cache (Redis)
    ↓
If Miss: Fetch from OpenAQ + OpenWeather
    ↓
Calculate AQI
    ↓
Cache Result
    ↓
Return Combined Data
```

## Security Architecture

### Authentication Flow
```
1. User registers → Password hashed with bcrypt
2. User logs in → Credentials validated
3. Server generates JWT token (HS256)
4. Token sent to client
5. Client includes token in Authorization header
6. Server validates token on each request
7. Token expires after 30 minutes
```

### Data Protection
- **Passwords**: Hashed with bcrypt (cost factor: 12)
- **Tokens**: JWT with HS256 algorithm
- **Sensitive Data**: Encrypted at rest (future phase)
- **API Keys**: Stored in environment variables
- **HTTPS**: Required in production

## Scalability Considerations

### Current Design (Phase 1)
- Single-server deployment
- PostgreSQL on same host
- Suitable for up to 10,000 users

### Future Scaling (Phase 3+)
- **Horizontal Scaling**: Multiple API servers behind load balancer
- **Database**: Read replicas for query scaling
- **Caching**: Redis cluster for distributed cache
- **Message Queue**: Celery with RabbitMQ/Redis for async tasks
- **CDN**: Static asset delivery
- **Microservices**: Split services by domain

## Technology Stack

### Backend
- **Framework**: FastAPI 0.109.0
- **Language**: Python 3.11
- **ORM**: SQLAlchemy 2.0
- **Validation**: Pydantic 2.5
- **Authentication**: python-jose (JWT)
- **Database**: PostgreSQL 15

### External Dependencies
- **httpx**: Async HTTP client
- **Redis**: Caching (optional)
- **Celery**: Task queue (Phase 2+)
- **MQTT**: paho-mqtt (Phase 2+)

### ML/Analytics (Phase 2+)
- **numpy**: Numerical computing
- **pandas**: Data manipulation
- **scikit-learn**: ML models
- **statsmodels**: Time series analysis

## Monitoring & Observability (Future)

### Metrics
- API request latency (p50, p95, p99)
- Error rates by endpoint
- Database query performance
- External API response times
- Cache hit/miss ratio

### Logging
- Structured JSON logs
- Request/response logging
- Error tracking
- Audit trail for sensitive operations

### Alerting
- High error rate
- Database connection failures
- External API failures
- Disk space warnings

## Deployment Architecture

### Development
```
Local machine → uvicorn --reload → PostgreSQL (local)
```

### Production (Recommended)
```
Internet → Load Balancer → API Servers (N) → PostgreSQL Primary
                                           → PostgreSQL Replicas
                                           → Redis Cluster
```

### Docker Deployment
```
docker-compose up
    ↓
PostgreSQL Container (port 5432)
Redis Container (port 6379)
Backend Container (port 8000)
```

## API Versioning Strategy

### Current
- Version 1.0: `/api/*` endpoints
- No explicit version in URL

### Future
- Version 2.0: `/api/v2/*` endpoints
- Maintain backward compatibility for v1
- Deprecation notices before breaking changes

## Database Schema Evolution

### Migrations
- **Tool**: Alembic
- **Strategy**: Forward-only migrations
- **Rollback**: Tested for each migration
- **Zero-downtime**: Online schema changes for production

## Performance Optimization

### Query Optimization
- Indexes on frequently queried fields
- Eager loading for related data
- Connection pooling
- Query result caching

### API Response Time Targets
- `/auth/*`: < 500ms (p95)
- `/profile`: < 300ms (p95)
- `/aq/current`: < 800ms (p95) - includes external API calls
- `/activity/recommend`: < 800ms (p95)
- `/indoor/*`: < 400ms (p95)

### Caching Strategy
- External API responses: 10-15 minutes TTL
- User profile data: 5 minutes TTL
- Static data: 1 hour TTL
- Cache invalidation on updates

## Error Handling

### HTTP Status Codes
- **200**: Success
- **201**: Created
- **400**: Bad Request (validation error)
- **401**: Unauthorized (invalid/missing token)
- **403**: Forbidden (insufficient permissions)
- **404**: Not Found
- **500**: Internal Server Error

### Error Response Format
```json
{
  "detail": "Error message",
  "code": "ERROR_CODE",
  "timestamp": "2025-01-15T10:30:00Z"
}
```

## Future Architecture Enhancements

### Phase 2
- Time-series database (TimescaleDB)
- ML model serving (TensorFlow Serving)
- Background job processing (Celery)
- WebSocket support for real-time updates

### Phase 3
- Microservices architecture
- Service mesh (Istio)
- Event-driven architecture (Kafka)
- Advanced caching (Redis Cluster)

### Phase 4
- Edge computing for IoT devices
- Multi-region deployment
- CDN integration
- Advanced observability (Prometheus, Grafana)

## Documentation

- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **Alternative Docs**: http://localhost:8000/redoc
- **OpenAPI Spec**: http://localhost:8000/openapi.json

## Development Workflow

```
1. Local Development → Feature Branch
2. Unit Tests → Pytest
3. Integration Tests → Test Database
4. Code Review → Pull Request
5. CI Pipeline → GitHub Actions
6. Staging Deployment → Docker
7. Production Deployment → After approval
```

## Conclusion

This architecture provides a solid foundation for Phase 1 while remaining flexible enough to accommodate future enhancements. The modular design allows for incremental improvements without major refactoring.
