#!/bin/bash
# Startup script for Render deployment

# Install dependencies
pip install -r requirements.txt

# Start the application with gunicorn
gunicorn main:app --bind 0.0.0.0:$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker --timeout 300 --keep-alive 5 