# GitHub Copilot Instructions for Environmental Health Platform

## Project Overview

This is the Environmental Health Platform - a personalized environmental health & air quality decision support platform. It integrates indoor IoT sensors, public air quality data, weather information, user health profiles, exposure modeling, and conversational decision-support features.

**Current Phase**: Phase 1 MVP (Completed)
**Tech Stack**: FastAPI (Python) backend, React frontend, PostgreSQL database, Docker deployment

## Repository Structure

```
env-health-platform/
├── backend/              # FastAPI backend application
│   ├── app/
│   │   ├── main.py      # FastAPI application entry point
│   │   ├── api/         # API route handlers
│   │   ├── core/        # Core functionality (config, database, security)
│   │   ├── models/      # SQLAlchemy database models
│   │   ├── schemas/     # Pydantic validation schemas
│   │   └── services/    # Business logic services
│   ├── tests/           # Pytest unit and integration tests
│   └── requirements.txt # Python dependencies
└── frontend/            # React frontend application
    └── src/
```

## Coding Standards

### Python (Backend)

- **Style Guide**: Follow PEP 8 strictly
- **Type Hints**: Always use type hints for function parameters and return values
- **Docstrings**: Write comprehensive docstrings for all functions, classes, and modules
- **Async/Await**: Use async/await for all I/O operations (database queries, external API calls)
- **Error Handling**: Use proper exception handling with specific exception types
- **Validation**: Use Pydantic models for all request/response validation

### Code Organization

- **Models**: SQLAlchemy models go in `backend/app/models/`
- **Schemas**: Pydantic schemas go in `backend/app/schemas/`
- **Services**: Business logic goes in `backend/app/services/`
- **API Routes**: API endpoints go in `backend/app/api/`
- **Keep functions small**: Each function should do one thing well
- **Single Responsibility**: Each module should have a clear, single purpose

### Database

- **ORM**: Use SQLAlchemy for all database operations
- **Migrations**: Use Alembic for database migrations (forward-only)
- **Async Operations**: Use async database sessions
- **Relationships**: Define proper relationships between models
- **Indexing**: Add appropriate indexes for frequently queried fields

### Security

- **Authentication**: JWT tokens with HS256 algorithm
- **Password Hashing**: Use bcrypt for password hashing
- **Environment Variables**: Store all secrets in environment variables, never in code
- **Input Validation**: Validate all user inputs using Pydantic schemas
- **Authorization**: Verify user ownership of resources (e.g., sensor devices)
- **CORS**: Configure CORS middleware appropriately

## API Design

- **RESTful**: Follow REST principles
- **Versioning**: Current version at `/api/*` endpoints (no explicit version in URL)
- **Status Codes**: Use appropriate HTTP status codes:
  - 200: Success
  - 201: Created
  - 400: Bad Request (validation errors)
  - 401: Unauthorized
  - 403: Forbidden
  - 404: Not Found
  - 500: Internal Server Error
- **Response Format**: Consistent JSON response format
- **Error Messages**: Provide clear, actionable error messages

## External APIs

The platform integrates with:
- **OpenAQ**: Air quality data from public monitoring stations
- **OpenWeatherMap**: Weather data including temperature, humidity
- Cache responses to minimize API calls and handle rate limiting

## Testing

- **Framework**: pytest
- **Coverage**: Aim for high test coverage, especially for business logic
- **Test Types**:
  - Unit tests for services and utilities
  - Integration tests for API endpoints
  - Test all edge cases and error scenarios
- **Run Tests**: `pytest` from the backend directory
- **Test Data**: Use fixtures for test data setup
- **Mocking**: Mock external API calls in tests

## Activity Recommendation Logic

The platform implements sophisticated scoring algorithms for activity recommendations:
- **Input Factors**: PM2.5, temperature, humidity, user sensitivity level
- **Activity Types**: Jogging, walking, cycling
- **Scoring**: 0-100 scale with thresholds:
  - ≥70: Good conditions
  - 40-69: Caution
  - <40: Avoid
  - 0: Not recommended (for sensitive individuals)

## Development Workflow

1. **Feature Development**: Create feature branch from main
2. **Branch Naming**:
   - `feature/description` - New features
   - `fix/description` - Bug fixes
   - `docs/description` - Documentation
   - `refactor/description` - Code refactoring
3. **Commits**: Use clear, descriptive commit messages in present tense
4. **Testing**: Write tests for new features, ensure all tests pass
5. **Pull Requests**: Include clear description, link to issues, ensure CI passes

## Commit Message Format

```
Add activity recommendation endpoint

- Implement jogging score calculation
- Add support for walking and cycling
- Include tests for different scenarios

Fixes #123
```

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 72 characters
- Reference issues and PRs liberally

## Common Patterns

### Creating a New API Endpoint

1. Define Pydantic schemas in `backend/app/schemas/`
2. Create database model in `backend/app/models/` (if needed)
3. Implement business logic in `backend/app/services/`
4. Create route handler in `backend/app/api/`
5. Add route to router in `backend/app/api/routes.py`
6. Write tests in `backend/tests/`

### Adding External API Integration

1. Add API configuration to `backend/app/core/config.py`
2. Create service class in `backend/app/services/external_api.py`
3. Use async HTTP client (httpx)
4. Implement error handling and retry logic
5. Cache responses when appropriate

### Database Model Pattern

```python
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class ModelName(Base):
    __tablename__ = "table_name"
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    # ... other fields
```

### Pydantic Schema Pattern

```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class SchemaBase(BaseModel):
    field1: str = Field(..., description="Description")
    field2: Optional[int] = None

class SchemaCreate(SchemaBase):
    pass

class SchemaResponse(SchemaBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
```

## Documentation

- **API Docs**: Auto-generated at `/docs` (Swagger UI) and `/redoc`
- **Code Comments**: Use sparingly, prefer self-documenting code
- **README**: Keep README.md up to date
- **Architecture**: Major architectural changes should be documented in ARCHITECTURE.md

## Future Phases

Be aware of planned features to avoid design decisions that would complicate future work:

**Phase 2**:
- Time series forecasting (ARIMA/LSTM)
- Symptom diary with exposure correlation
- Route exposure optimization
- Chat assistant

**Phase 3**:
- What-if scheduling
- Exposure budgets
- Pollen & wildfire data layers
- Advanced alert logic

**Phase 4**:
- Crowd-sourced micro-sensors
- Adaptive learning
- Smart home integration
- Multi-language support

## Key Principles

1. **User Privacy**: Handle health data with utmost care
2. **Accuracy**: Environmental data must be accurate and reliable
3. **Performance**: Optimize for fast response times
4. **Scalability**: Design for future growth
5. **Maintainability**: Write clean, well-documented code
6. **Testability**: Make code easy to test
7. **Security**: Security is not optional

## Resources

- **Contributing Guide**: See CONTRIBUTING.md for detailed guidelines
- **Architecture**: See ARCHITECTURE.md for system design
- **API Guide**: See backend/API_GUIDE.md for API usage examples
- **Quick Start**: See QUICKSTART.md for getting started

## Avoid

- Don't commit secrets or API keys
- Don't skip input validation
- Don't write synchronous I/O code (use async)
- Don't ignore error cases
- Don't duplicate code - create reusable functions/services
- Don't modify working code unless necessary for the task
- Don't add dependencies without justification
- Don't skip tests for new features
