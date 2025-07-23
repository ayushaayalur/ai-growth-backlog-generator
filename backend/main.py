"""
Main entry point for the AI Growth Backlog Generator API
For local development only - production uses gunicorn with app.py
"""

import os
import sys
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables from .env file
load_dotenv()

from app.api.endpoints import app

# This is for local development only
if __name__ == "__main__":
    import uvicorn
    print("Starting FastAPI development server...")
    print(f"Frontend URL: {os.getenv('FRONTEND_URL', 'https://ai-yushas-growth-backlog-generator-ui.onrender.com')}")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True) 