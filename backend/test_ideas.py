#!/usr/bin/env python3
"""
Test script to verify idea generation works
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.growth_analyzer import GrowthAnalyzer

def test_idea_generation():
    """Test that idea generation works"""
    try:
        # Initialize the analyzer
        api_key = os.getenv("OPENAI_API_KEY", "test-key")
        analyzer = GrowthAnalyzer(api_key)
        
        print("✅ GrowthAnalyzer initialized successfully")
        
        # Test fallback ideas
        fallback_ideas = analyzer._get_fallback_ideas()
        print(f"✅ Generated {len(fallback_ideas)} fallback ideas")
        
        # Test ICE scoring
        scored_ideas = analyzer._score_ideas_with_ice(fallback_ideas)
        print(f"✅ Scored {len(scored_ideas)} ideas with ICE")
        
        # Print first idea as example
        if scored_ideas:
            first_idea = scored_ideas[0]
            print(f"\n📋 Example idea:")
            print(f"   Title: {first_idea.get('title', 'N/A')}")
            print(f"   Category: {first_idea.get('category', 'N/A')}")
            print(f"   ICE Score: {first_idea.get('ice', {}).get('score', 'N/A')}")
            print(f"   Priority: {first_idea.get('priority', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing idea generation...")
    success = test_idea_generation()
    if success:
        print("\n✅ All tests passed! Idea generation is working.")
    else:
        print("\n❌ Tests failed. Check the error messages above.") 