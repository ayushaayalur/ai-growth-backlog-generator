"""
API endpoints for the AI Growth Backlog Generator
"""

import os
import tempfile
from typing import Dict, Any
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from app.services.growth_analyzer import GrowthAnalyzer

app = FastAPI(title="AI Growth Backlog Generator API")

# Get frontend URL from environment or use confirmed working default
FRONTEND_URL = os.getenv("FRONTEND_URL", "https://ai-yushas-growth-backlog-generator-ui.onrender.com")

# Add CORS middleware with comprehensive origins for both development and production
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React dev server
        "http://127.0.0.1:3000",  # Alternative localhost
        "https://ai-yushas-growth-backlog-generator-ui.onrender.com",  # Confirmed frontend URL
        FRONTEND_URL,  # Environment variable frontend URL
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Add startup event to log CORS configuration
@app.on_event("startup")
async def startup_event():
    print(f"FastAPI app starting up...")
    print(f"CORS configured for frontend: {FRONTEND_URL}")
    print(f"OpenAI API Key configured: {'Yes' if os.getenv('OPENAI_API_KEY') else 'No'}")

# Initialize the growth analyzer
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is required")

growth_analyzer = GrowthAnalyzer(OPENAI_API_KEY)

class AnalysisResponse(BaseModel):
    ideas: list
    summary: dict
    metadata: dict

@app.post("/analyze-screenshot", response_model=AnalysisResponse)
async def analyze_screenshot(file: UploadFile = File(...)):
    """
    Analyze a screenshot and generate growth backlog with ICE scores
    """
    try:
        print(f"Received file: {file.filename}, content_type: {file.content_type}")
        
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            print(f"Starting analysis of file: {temp_file_path}")
            print(f"File size: {len(content)} bytes")
            
            # Analyze the screenshot
            analysis_result = growth_analyzer.analyze_landing_page(temp_file_path)
            
            print(f"Analysis completed. Ideas count: {len(analysis_result.get('ideas', []))}")
            print(f"Summary: {analysis_result.get('summary', {})}")
            
            return AnalysisResponse(
                ideas=analysis_result['ideas'],
                summary=analysis_result['summary'],
                metadata=analysis_result['metadata']
            )
            
        except Exception as analysis_error:
            print(f"Analysis error: {str(analysis_error)}")
            print(f"Error type: {type(analysis_error)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            raise HTTPException(status_code=500, detail=f"Analysis failed: {str(analysis_error)}")
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
                
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "AI Growth Backlog Generator"}

@app.get("/")
async def root():
    """Root endpoint to verify the API is running"""
    return {"message": "AI Growth Backlog Generator API is running", "docs_url": "/docs"} 