"""
Main entry point for the AI Growth Backlog Generator API
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from app.api.endpoints import app

# This is needed for gunicorn to find the app
app = app 