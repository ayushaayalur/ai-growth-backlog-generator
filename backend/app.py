"""
Simple app entry point for gunicorn
"""

from app.api.endpoints import app

# This makes the app available to gunicorn
if __name__ == "__main__":
    app.run() 