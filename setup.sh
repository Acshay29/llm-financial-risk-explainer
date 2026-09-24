#!/bin/bash

# Exit on error
set -e

echo "Setting up LLM-Powered Financial Risk Explainer..."

# 1. Generate sample data
echo "Generating sample data..."
python3 ml/src/generate_data.py

# 2. Train the model
echo "Training model and logging to MLflow..."
export PYTHONPATH=$PYTHONPATH:$(pwd)/ml/src
python3 ml/src/train.py

# 3. Check if Docker is installed
if command -v docker-compose &> /dev/null
then
    echo "Starting services with docker-compose..."
    docker-compose up --build -d
    echo "Services started. API is available at http://localhost:8000"
    echo "MLflow UI is available at http://localhost:5000"
else
    echo "Docker Compose not found. Please install Docker to run the full stack."
    echo "You can still run the FastAPI app locally using:"
    echo "uvicorn app.api.main:app --reload"
fi
