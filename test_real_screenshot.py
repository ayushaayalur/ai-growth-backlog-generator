#!/usr/bin/env python3
"""
Test script to simulate the Calm app screenshot and test AI analysis
"""

import requests
import json
import time
import base64

def test_real_screenshot():
    """Create a test that simulates the Calm app screenshot analysis"""
    
    print("🧘 Testing with Calm app screenshot simulation...")
    
    # Wait for backend to start
    print("Waiting for backend to start...")
    time.sleep(3)
    
    # Create a more realistic test image (simulating a landing page)
    # This is a basic approach - in real testing you'd use the actual screenshot
    
    # Create a simple test image (1x1 pixel PNG)
    test_image_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\x07tIME\x07\xe5\x07\x16\x0f\x1d\x0c\xc8\xc8\xc8\x00\x00\x00\x0cIDATx\x9cc```\x00\x00\x00\x04\x00\x01\xf5\xc7\xdd\x8c\x00\x00\x00\x00IEND\xaeB`\x82'
    
    # Save test image
    with open("calm_app_test.png", "wb") as f:
        f.write(test_image_data)
    
    try:
        # Test the analyze endpoint
        with open("calm_app_test.png", "rb") as f:
            files = {"file": ("calm_app_test.png", f, "image/png")}
            response = requests.post("http://localhost:8000/analyze-screenshot", files=files)
        
        if response.status_code == 200:
            data = response.json()
            ideas = data.get('ideas', [])
            metadata = data.get('metadata', {})
            
            print(f"✅ Generated {len(ideas)} ideas")
            
            # Analyze the metadata
            print("\n📊 Analysis Metadata:")
            print(f"   Image description: {metadata.get('image_description', 'N/A')[:300]}...")
            print(f"   Extracted text: {metadata.get('extracted_text', 'N/A')[:200]}...")
            print(f"   Visual elements: {len(metadata.get('visual_elements', {}))} types")
            
            # Check if ideas are specific to meditation/wellness apps
            print(f"\n🎯 Analyzing Idea Specificity:")
            
            # Look for ideas that should be specific to the Calm app
            calm_specific_indicators = [
                'meditation', 'sleep', 'calm', 'relaxation', 'wellness', 'mindfulness',
                'app', 'mobile', 'subscription', 'free trial', 'headline', 'cta',
                'button', 'landing page', 'conversion', 'signup'
            ]
            
            specific_count = 0
            generic_count = 0
            
            for i, idea in enumerate(ideas[:10], 1):  # Check first 10 ideas
                title = idea.get('title', '').lower()
                description = idea.get('description', '').lower()
                hypothesis = idea.get('hypothesis', '').lower()
                
                # Check if idea references specific elements
                has_specific = any(indicator in title or indicator in description or indicator in hypothesis for indicator in calm_specific_indicators)
                
                if has_specific:
                    specific_count += 1
                    idea_type = "✅ SPECIFIC"
                else:
                    generic_count += 1
                    idea_type = "❌ GENERIC"
                
                print(f"{i}. {idea_type} - {idea.get('title', 'No title')}")
                print(f"   Category: {idea.get('category', 'N/A')}")
                print(f"   ICE Score: {idea.get('ice', {}).get('score', 'N/A')}")
                print()
            
            # Overall assessment
            specificity_ratio = specific_count / (specific_count + generic_count) if (specific_count + generic_count) > 0 else 0
            
            print(f"🎯 Specificity Assessment:")
            print(f"   Specific ideas: {specific_count}")
            print(f"   Generic ideas: {generic_count}")
            print(f"   Specificity ratio: {specificity_ratio:.1%}")
            
            # Check if AI analysis is working
            image_description = metadata.get('image_description', '')
            if 'enhanced landing page analysis' in image_description.lower():
                print("❌ AI analysis is NOT working - using fallback analysis")
                return False
            elif 'calm' in image_description.lower() or 'meditation' in image_description.lower():
                print("✅ AI analysis IS working - detected app-specific content")
                return True
            else:
                print("⚠️  AI analysis may be working but not detecting specific content")
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
        if os.path.exists("calm_app_test.png"):
            os.remove("calm_app_test.png")

if __name__ == "__main__":
    success = test_real_screenshot()
    if success:
        print("\n✅ AI analysis is working correctly!")
    else:
        print("\n❌ AI analysis needs to be fixed.")
        print("\n💡 The system should generate ideas specific to:")
        print("   - Meditation/sleep app features")
        print("   - 'Calm your mind. Change your life.' headline")
        print("   - 'Try Calm for Free' CTAs")
        print("   - Wellness app conversion optimization") 