# Getting Started with Environmental Health Platform

This guide will help you set up and run the Environmental Health Platform on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.9 or higher**: [Download Python](https://www.python.org/downloads/)
- **Node.js 16 or higher**: [Download Node.js](https://nodejs.org/)
- **PostgreSQL 12 or higher**: [Download PostgreSQL](https://www.postgresql.org/download/)
- **Git**: [Download Git](https://git-scm.com/downloads)

Optional (for easier setup):
- **Docker & Docker Compose**: [Get Docker](https://docs.docker.com/get-docker/)

## Quick Start (Recommended)

The fastest way to get started is using Docker Compose:

### 1. Clone the Repository

```bash
git clone https://github.com/pragyakuumarimishra/env-health-platform.git
cd env-health-platform
```

### 2. Start Services with Docker

```bash
docker-compose up -d
```

This starts PostgreSQL, Redis, and MQTT broker.

### 3. Run Setup Script

```bash
./setup.sh
```

This will:
- Copy environment configuration files
- Install Python dependencies
- Install Node.js dependencies

### 4. Setup Database

```bash
cd backend
alembic upgrade head
cd ..
```

### 5. Start Backend

```bash
cd backend
uvicorn app.main:app --reload
```

The backend API will be available at http://localhost:8000

### 6. Start Frontend (in a new terminal)

```bash
cd frontend
npm start
```

The frontend will open automatically at http://localhost:3000

## Manual Setup (Without Docker)

If you prefer not to use Docker, follow these steps:

### 1. Setup PostgreSQL

Create a database:
```bash
psql -U postgres
CREATE DATABASE envhealth;
CREATE USER envuser WITH PASSWORD 'envpass';
GRANT ALL PRIVILEGES ON DATABASE envhealth TO envuser;
\q
```

### 2. Setup Backend

```bash
cd backend

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your database credentials
nano .env  # or use your preferred editor

# Run migrations
alembic upgrade head
```

### 3. Setup Frontend

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env
```

### 4. Run the Application

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # if using venv
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

## First Steps

### 1. Register a User Account

1. Open http://localhost:3000
2. Click "Need an account? Register"
3. Enter your email and password
4. Click "Register"

### 2. Login

1. Enter your email and password
2. Click "Login"
3. You'll be redirected to the dashboard

### 3. Explore the Dashboard

The dashboard shows:
- **Outdoor Air Quality**: Current AQI and pollutant levels
- **Indoor Sensors**: List of registered sensors
- **Activity Recommendation**: Get suggestions for outdoor activities

### 4. Get an Activity Recommendation

1. Enter an activity type (e.g., "jogging")
2. Click "Get Recommendation"
3. View the score and recommendation

### 5. Simulate Sensor Data (Optional)

In a new terminal:
```bash
cd backend/examples
python sensor_simulator.py
```

Follow the prompts to:
1. Login with your account
2. Create a virtual sensor device
3. Send simulated readings every 60 seconds

## Testing the API

### Using Swagger UI

Visit http://localhost:8000/docs for interactive API documentation.

### Example API Calls

**Register a user:**
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "sensitivity_level": 2
  }'
```

**Login:**
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=password123"
```

**Get air quality (requires token):**
```bash
curl -X GET "http://localhost:8000/api/aq/current?lat=40.7128&lon=-74.0060" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Configuration

### Backend Configuration (.env)

Key settings in `backend/.env`:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/envhealth

# Security
SECRET_KEY=your-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30

# External APIs (optional for MVP)
OPENWEATHER_API_KEY=your-api-key
WAQI_API_KEY=your-api-key

# MQTT (for IoT sensors)
MQTT_BROKER=localhost
MQTT_PORT=1883
```

### Frontend Configuration (.env)

```env
REACT_APP_API_URL=http://localhost:8000/api
```

## Project Structure

```
env-health-platform/
├── backend/           # FastAPI backend
│   ├── app/          # Application code
│   ├── alembic/      # Database migrations
│   └── examples/     # Example scripts
├── frontend/         # React frontend
│   ├── src/          # Source code
│   └── public/       # Static files
├── docker-compose.yml # Docker services
└── setup.sh          # Setup script
```

## Troubleshooting

### Backend won't start

**Error: `ModuleNotFoundError`**
- Solution: Ensure dependencies are installed: `pip install -r requirements.txt`

**Error: `sqlalchemy.exc.OperationalError`**
- Solution: Check PostgreSQL is running and credentials in `.env` are correct

**Error: `alembic.util.exc.CommandError`**
- Solution: Ensure database exists and run `alembic upgrade head`

### Frontend won't start

**Error: `Cannot find module`**
- Solution: Run `npm install` in the frontend directory

**Error: `EADDRINUSE`**
- Solution: Port 3000 is already in use. Either stop the other process or change the port:
  ```bash
  PORT=3001 npm start
  ```

### API returns 401 Unauthorized

- Solution: Ensure you're logged in and token is included in request headers
- Token format: `Authorization: Bearer <token>`

### Database connection issues

**Can't connect to PostgreSQL:**
1. Verify PostgreSQL is running: `pg_isready`
2. Check credentials in `backend/.env`
3. If using Docker: `docker-compose ps` to verify postgres is running

## Next Steps

After getting the platform running:

1. **Explore the API**: Visit http://localhost:8000/docs
2. **Customize your profile**: Update sensitivity level and health conditions
3. **Register sensors**: Add indoor air quality monitors
4. **Try the sensor simulator**: Generate test data
5. **Read the specification**: Understand the full vision
6. **Read IMPLEMENTATION.md**: Learn about the technical details

## Getting Help

- Check the [README.md](README.md) for overview
- Read [IMPLEMENTATION.md](IMPLEMENTATION.md) for technical details
- Review the specification document for requirements
- Check GitHub Issues for known problems

## Development Tips

### Hot Reload

Both backend and frontend support hot reload:
- Backend: Automatically reloads when Python files change
- Frontend: Automatically reloads when React files change

### Database Migrations

When you modify models:
```bash
cd backend
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```

### View Logs

**Backend logs:**
- Console output shows all requests and errors
- FastAPI shows detailed tracebacks in development mode

**Frontend logs:**
- Browser console (F12) shows React errors and API calls

### Reset Database

To start fresh:
```bash
cd backend
alembic downgrade base
alembic upgrade head
```

Or drop and recreate:
```bash
psql -U postgres
DROP DATABASE envhealth;
CREATE DATABASE envhealth;
\q
cd backend
alembic upgrade head
```

## Production Deployment

This setup is for development only. For production:

1. Set strong `SECRET_KEY` in backend `.env`
2. Use production PostgreSQL instance
3. Configure proper CORS origins
4. Set up HTTPS/TLS
5. Use production build: `npm run build`
6. Deploy with gunicorn/nginx
7. Set up monitoring and logging
8. Configure backup strategy

See deployment documentation for detailed instructions.
