"""
Simple app entry point for gunicorn
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.api.endpoints import app

# This makes the app available to gunicorn
if __name__ == "__main__":
    app.run() 