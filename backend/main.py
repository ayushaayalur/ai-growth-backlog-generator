"""
Main entry point for the AI Growth Backlog Generator API
"""

import os
from dotenv import load_dotenv
import uvicorn

# Load environment variables from .env file
load_dotenv()

from app.api.endpoints import app

if __name__ == "__main__":
    uvicorn.run(
        "app.api.endpoints:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 