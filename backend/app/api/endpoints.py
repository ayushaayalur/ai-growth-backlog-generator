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

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React dev server
        "https://ai-yushas-growth-backlog-generator-ui.onrender.com",  # Production frontend
        "https://ai-yushas-growth-backlog-generator-ui.onrender.com/",  # Production frontend with trailing slash
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
            
            # Analyze the screenshot
            analysis_result = growth_analyzer.analyze_landing_page(temp_file_path)
            
            print(f"Analysis completed. Ideas count: {len(analysis_result.get('ideas', []))}")
            print(f"Summary: {analysis_result.get('summary', {})}")
            
            return AnalysisResponse(
                ideas=analysis_result['ideas'],
                summary=analysis_result['summary'],
                metadata=analysis_result['metadata']
            )
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
                
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "AI Growth Backlog Generator"} 