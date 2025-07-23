"""
Main entry point for the AI Growth Backlog Generator API
"""

import os
import sys
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables from .env file
load_dotenv()

from app.api.endpoints import app

# This is needed for gunicorn to find the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 