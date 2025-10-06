#!/bin/bash
# Script to run the Environmental Health Platform API

echo "Starting Environmental Health Platform API..."
cd "$(dirname "$0")"
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
