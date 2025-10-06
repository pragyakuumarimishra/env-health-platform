# Contributing to Environmental Health Platform

Thank you for your interest in contributing to the Environmental Health Platform! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/env-health-platform.git`
3. Set up the development environment (see [GETTING_STARTED.md](GETTING_STARTED.md))
4. Create a new branch: `git checkout -b feature/your-feature-name`

## Development Workflow

### 1. Before Making Changes

- Read the [specification document](specification.md) to understand the project vision
- Check existing issues to avoid duplicate work
- Create an issue to discuss major changes before implementing

### 2. Making Changes

#### Backend Changes

**Code Style:**
- Follow PEP 8 style guide
- Use type hints where possible
- Add docstrings to functions and classes
- Keep functions focused and small

**Example:**
```python
from typing import Optional
from sqlalchemy.orm import Session

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    Retrieve a user by their email address.
    
    Args:
        db: Database session
        email: User's email address
        
    Returns:
        User object if found, None otherwise
    """
    return db.query(User).filter(User.email == email).first()
```

**Database Changes:**
1. Modify models in `backend/app/models.py`
2. Generate migration: `alembic revision --autogenerate -m "Description"`
3. Review generated migration in `backend/alembic/versions/`
4. Test migration: `alembic upgrade head`
5. Test rollback: `alembic downgrade -1` then `alembic upgrade head`

**Adding New Endpoints:**
1. Add Pydantic schemas in `backend/app/schemas.py`
2. Create route handler in appropriate file in `backend/app/api/`
3. Include router in `backend/app/api/routes.py` if new module
4. Test endpoint manually or with tests
5. Update API documentation in README

**Example:**
```python
# In schemas.py
class NewFeatureRequest(BaseModel):
    name: str
    value: int

class NewFeatureResponse(BaseModel):
    id: UUID
    name: str
    value: int
    created_at: datetime

# In api/new_feature.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/", response_model=NewFeatureResponse)
def create_feature(
    request: NewFeatureRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Implementation
    pass
```

#### Frontend Changes

**Code Style:**
- Use functional components with hooks
- Follow Material-UI patterns
- Keep components small and focused
- Use meaningful variable names

**Example:**
```javascript
import React, { useState, useEffect } from 'react';
import { Card, CardContent, Typography } from '@mui/material';
import axios from 'axios';

function NewComponent({ userId }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, [userId]);

  const fetchData = async () => {
    try {
      const response = await axios.get(`/api/endpoint/${userId}`);
      setData(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching data:', error);
      setLoading(false);
    }
  };

  if (loading) return <div>Loading...</div>;

  return (
    <Card>
      <CardContent>
        <Typography variant="h6">{data?.name}</Typography>
      </CardContent>
    </Card>
  );
}

export default NewComponent;
```

### 3. Testing Your Changes

**Backend Testing:**
```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload

# Test endpoints at http://localhost:8000/docs
```

**Frontend Testing:**
```bash
cd frontend

# Install dependencies
npm install

# Run the development server
npm start

# Test in browser at http://localhost:3000
```

**Manual Testing Checklist:**
- [ ] Code runs without errors
- [ ] New features work as expected
- [ ] Existing features still work
- [ ] API endpoints return correct data
- [ ] UI displays correctly
- [ ] Mobile responsive (if UI changes)
- [ ] Database migrations work

### 4. Committing Changes

**Commit Message Format:**
```
<type>: <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples:**
```
feat: Add pollen data integration

- Add pollen API endpoint
- Update dashboard to display pollen levels
- Add database table for pollen data

Closes #42
```

```
fix: Correct jogging score calculation

The humidity penalty was being applied twice. Fixed to apply only once
as specified in the algorithm.

Fixes #38
```

### 5. Submitting Changes

1. Commit your changes with meaningful commit messages
2. Push to your fork: `git push origin feature/your-feature-name`
3. Create a Pull Request from your fork to the main repository
4. Fill in the PR template with:
   - Description of changes
   - Related issue numbers
   - Testing performed
   - Screenshots (if UI changes)

**PR Checklist:**
- [ ] Code follows project style guidelines
- [ ] Changes are documented
- [ ] Database migrations included (if schema changes)
- [ ] Manual testing completed
- [ ] No sensitive data (passwords, API keys) committed
- [ ] README updated (if needed)

## Project Structure

When adding new features, follow this structure:

### Backend
```
backend/app/
├── api/              # API endpoints
│   ├── module.py    # Group related endpoints
│   └── routes.py    # Router aggregator
├── models.py        # Database models
├── schemas.py       # Pydantic schemas
├── auth.py          # Authentication utilities
├── config.py        # Configuration
└── main.py          # Application entry point
```

### Frontend
```
frontend/src/
├── components/       # React components
│   └── Component.js # One component per file
├── App.js           # Main app
└── index.js         # Entry point
```

## Coding Standards

### Python (Backend)

1. **Imports**: Group in order: standard library, third-party, local
2. **Naming**: 
   - Classes: `PascalCase`
   - Functions/variables: `snake_case`
   - Constants: `UPPER_CASE`
3. **Type Hints**: Use for function parameters and return types
4. **Error Handling**: Use appropriate exceptions, don't catch generic Exception

### JavaScript (Frontend)

1. **Imports**: Group by source (libraries, components, utilities)
2. **Naming**:
   - Components: `PascalCase`
   - Functions/variables: `camelCase`
   - Constants: `UPPER_CASE`
3. **Components**: Functional components with hooks
4. **State**: Use useState for component state, useEffect for side effects

## Adding New Features

### Example: Adding Pollen Data

**1. Database Model (backend/app/models.py):**
```python
class PollenData(Base):
    __tablename__ = "pollen_data"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    location_lat = Column(Float, nullable=False)
    location_lon = Column(Float, nullable=False)
    ts = Column(DateTime, nullable=False, index=True)
    tree_pollen = Column(Integer, nullable=True)
    grass_pollen = Column(Integer, nullable=True)
    weed_pollen = Column(Integer, nullable=True)
    source = Column(String, nullable=False)
```

**2. Schema (backend/app/schemas.py):**
```python
class PollenResponse(BaseModel):
    lat: float
    lon: float
    ts: datetime
    tree_pollen: Optional[int]
    grass_pollen: Optional[int]
    weed_pollen: Optional[int]
    
    class Config:
        from_attributes = True
```

**3. API Endpoint (backend/app/api/pollen.py):**
```python
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/current", response_model=PollenResponse)
def get_current_pollen(
    lat: float = Query(...),
    lon: float = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Implementation
    pass
```

**4. Include Router (backend/app/api/routes.py):**
```python
from app.api import pollen

router.include_router(pollen.router, prefix="/pollen", tags=["pollen"])
```

**5. Frontend Component (frontend/src/components/PollenDisplay.js):**
```javascript
import React, { useState, useEffect } from 'react';
import { Card, CardContent, Typography } from '@mui/material';

function PollenDisplay() {
  const [pollen, setPollen] = useState(null);
  
  useEffect(() => {
    fetchPollen();
  }, []);
  
  const fetchPollen = async () => {
    // Implementation
  };
  
  return (
    <Card>
      <CardContent>
        <Typography variant="h6">Pollen Levels</Typography>
        {/* Display pollen data */}
      </CardContent>
    </Card>
  );
}
```

**6. Migration:**
```bash
cd backend
alembic revision --autogenerate -m "Add pollen data table"
alembic upgrade head
```

## Documentation

When adding features:

1. **Code Comments**: Explain why, not what
2. **Docstrings**: For all public functions and classes
3. **README Updates**: Document new endpoints and features
4. **API Documentation**: FastAPI generates this automatically
5. **User Documentation**: Update guides if user-facing changes

## Questions and Help

- Open an issue for questions
- Join discussions in existing issues
- Reference the specification document for requirements
- Check IMPLEMENTATION.md for technical details

## Code Review Process

1. Maintainer reviews PR
2. Feedback provided as comments
3. Address feedback and update PR
4. Approval given when ready
5. PR merged by maintainer

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be:
- Listed in commit history
- Acknowledged in release notes
- Added to CONTRIBUTORS.md (for significant contributions)

Thank you for contributing to making air quality information accessible to everyone! 🌍
