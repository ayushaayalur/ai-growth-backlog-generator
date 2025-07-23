#!/bin/bash
# Startup script for Render deployment

echo "Starting AI Growth Backlog Generator API..."

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Export environment variables if needed
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Start the application with gunicorn
echo "Starting gunicorn server..."
echo "PORT: $PORT"
echo "Working directory: $(pwd)"

# Use app.py:app instead of main:app for cleaner import
gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker --log-level info --access-logfile - --error-logfile - 