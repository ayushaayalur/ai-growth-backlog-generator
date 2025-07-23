#!/usr/bin/env python3
"""
Test script to debug the image analysis and idea generation process
"""

import requests
import json
import time
import base64

def test_detailed_analysis():
    """Test the complete analysis process with detailed logging"""
    
    print("🔍 Testing detailed analysis process...")
    
    # Wait for backend to start
    print("Waiting for backend to start...")
    time.sleep(3)
    
    # Create a more complex test image (simulating a landing page)
    # This is a simple colored image - in real use you'd upload actual screenshots
    
    # Create a simple test image (1x1 pixel PNG)
    test_image_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\x07tIME\x07\xe5\x07\x16\x0f\x1d\x0c\xc8\xc8\xc8\x00\x00\x00\x0cIDATx\x9cc```\x00\x00\x00\x04\x00\x01\xf5\xc7\xdd\x8c\x00\x00\x00\x00IEND\xaeB`\x82'
    
    # Save test image
    with open("test_landing_page.png", "wb") as f:
        f.write(test_image_data)
    
    try:
        # Test the analyze endpoint
        with open("test_landing_page.png", "rb") as f:
            files = {"file": ("test_landing_page.png", f, "image/png")}
            response = requests.post("http://localhost:8000/analyze-screenshot", files=files)
        
        if response.status_code == 200:
            data = response.json()
            ideas = data.get('ideas', [])
            metadata = data.get('metadata', {})
            
            print(f"✅ Generated {len(ideas)} ideas")
            
            # Analyze the metadata
            print("\n📊 Analysis Metadata:")
            print(f"   Image description: {metadata.get('image_description', 'N/A')[:200]}...")
            print(f"   Extracted text: {metadata.get('extracted_text', 'N/A')[:200]}...")
            print(f"   Visual elements: {len(metadata.get('visual_elements', {}))} types")
            
            # Check if we're getting AI-generated ideas or fallbacks
            print(f"\n🎯 Idea Generation Analysis:")
            
            # Look for specific tactical ideas vs generic ones
            tactical_indicators = [
                'change', 'replace', 'add', 'move', 'reduce', 'create', 'implement',
                'specific', 'tactical', 'action-oriented', 'benefit-first'
            ]
            
            generic_indicators = [
                'optimize', 'improve', 'enhance', 'better', 'good', 'great'
            ]
            
            tactical_count = 0
            generic_count = 0
            
            for i, idea in enumerate(ideas, 1):
                title = idea.get('title', '').lower()
                description = idea.get('description', '').lower()
                
                has_tactical = any(indicator in title or indicator in description for indicator in tactical_indicators)
                has_generic = any(indicator in title or indicator in description for indicator in generic_indicators)
                
                if has_tactical and not has_generic:
                    tactical_count += 1
                    idea_type = "✅ TACTICAL"
                else:
                    generic_count += 1
                    idea_type = "❌ GENERIC"
                
                print(f"{i}. {idea_type} - {idea.get('title', 'No title')}")
                print(f"   Category: {idea.get('category', 'N/A')}")
                print(f"   ICE Score: {idea.get('ice', {}).get('score', 'N/A')}")
                print(f"   Hypothesis: {idea.get('hypothesis', 'N/A')[:100]}...")
                print()
            
            # Overall assessment
            tactical_ratio = tactical_count / len(ideas) if ideas else 0
            
            print(f"🎯 Tactical Assessment:")
            print(f"   Tactical ideas: {tactical_count}")
            print(f"   Generic ideas: {generic_count}")
            print(f"   Tactical ratio: {tactical_ratio:.1%}")
            
            if len(ideas) >= 15:
                print("✅ GOOD: Generated sufficient number of ideas")
            else:
                print(f"⚠️  WARNING: Only {len(ideas)} ideas generated (should be 20)")
            
            if tactical_ratio >= 0.7:
                print("✅ GOOD: Most ideas are tactical and specific")
                return True
            elif tactical_ratio >= 0.4:
                print("⚠️  MODERATE: Some ideas are tactical, but many are generic")
                return False
            else:
                print("❌ POOR: Most ideas are generic and not tactical")
                return False
                
        else:
            print(f"❌ Request failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    finally:
        # Clean up test file
        import os
        if os.path.exists("test_landing_page.png"):
            os.remove("test_landing_page.png")

if __name__ == "__main__":
    success = test_detailed_analysis()
    if success:
        print("\n✅ Test passed! Analysis is working well.")
    else:
        print("\n❌ Test failed. Analysis needs improvement.")
        print("\n💡 Issues to address:")
        print("   1. Ensure AI image analysis is working")
        print("   2. Generate 20 ideas instead of 3")
        print("   3. Make ideas more tactical and specific") 