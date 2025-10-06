#!/bin/bash

echo "Environmental Health Platform Setup"
echo "===================================="
echo ""

# Check for required commands
command -v python3 >/dev/null 2>&1 || { echo "Python 3 is required but not installed. Aborting." >&2; exit 1; }
command -v node >/dev/null 2>&1 || { echo "Node.js is required but not installed. Aborting." >&2; exit 1; }
command -v docker-compose >/dev/null 2>&1 || { echo "Warning: docker-compose not found. You'll need to setup PostgreSQL, Redis, and MQTT manually."; }

echo "Setting up backend..."
cd backend

if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created backend/.env - please edit with your configuration"
fi

echo "Installing Python dependencies..."
pip install -r requirements.txt

cd ..

echo ""
echo "Setting up frontend..."
cd frontend

if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created frontend/.env"
fi

echo "Installing Node dependencies..."
npm install

cd ..

echo ""
echo "Setup complete!"
echo ""
echo "To start the development environment:"
echo "1. Start services: docker-compose up -d"
echo "2. Run migrations: cd backend && alembic upgrade head"
echo "3. Start backend: cd backend && uvicorn app.main:app --reload"
echo "4. Start frontend: cd frontend && npm start"
echo ""
echo "Access the application at http://localhost:3000"
echo "API documentation at http://localhost:8000/docs"
