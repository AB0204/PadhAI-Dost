#!/bin/bash
cd python-backend

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Install dependencies if requirements.txt differs
echo "Installing dependencies..."
pip install -r requirements.txt

# Run server
echo "Starting FastAPI server on port 8000..."
uvicorn api:app --reload --port 8000
