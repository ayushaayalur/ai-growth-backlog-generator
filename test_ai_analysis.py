#!/usr/bin/env python3
"""
Comprehensive test to verify AI analysis with real screenshots
"""

import requests
import json
import time
import os

def test_ai_analysis_with_real_screenshot():
    """Test AI analysis with a real screenshot"""
    
    print("🔍 Testing AI Analysis with Real Screenshot...")
    print("=" * 60)
    
    # Wait for backend to start
    print("Waiting for backend to start...")
    time.sleep(3)
    
    # Check if there's a real screenshot to test with
    test_files = [
        "screenshot.png",
        "landing_page.png", 
        "test_screenshot.png",
        "calm_app.png",
        "test_image.png"
    ]
    
    test_file = None
    for file in test_files:
        if os.path.exists(file):
            test_file = file
            break
    
    if not test_file:
        print("❌ No test screenshot found!")
        print("   Please place a screenshot file in the current directory")
        print("   Supported names: screenshot.png, landing_page.png, test_screenshot.png")
        return False
    
    print(f"📸 Using test file: {test_file}")
    
    try:
        # Test the analyze endpoint
        with open(test_file, "rb") as f:
            files = {"file": (test_file, f, "image/png")}
            response = requests.post("http://localhost:8000/analyze-screenshot", files=files)
        
        if response.status_code == 200:
            data = response.json()
            ideas = data.get('ideas', [])
            metadata = data.get('metadata', {})
            
            print(f"✅ Generated {len(ideas)} ideas")
            
            # Check AI analysis status
            ai_working = metadata.get('ai_analysis_working', False)
            image_description = metadata.get('image_description', '')
            extracted_text = metadata.get('extracted_text', '')
            
            print(f"\n🤖 AI Analysis Status: {'✅ WORKING' if ai_working else '❌ FAILED'}")
            
            if ai_working:
                print("   AI analysis is working properly!")
                print("   Ideas should be specific to your screenshot content")
            else:
                print("   AI analysis failed - using fallback analysis")
                print("   This means ideas may be generic rather than specific")
            
            # Analyze the metadata
            print(f"\n📊 Analysis Details:")
            print(f"   Image description length: {len(image_description)} characters")
            print(f"   Extracted text length: {len(extracted_text)} characters")
            print(f"   Visual elements detected: {len(metadata.get('visual_elements', {}))} types")
            
            # Show image description preview
            print(f"\n📝 Image Description Preview:")
            print(f"   {image_description[:300]}...")
            
            # Analyze idea specificity
            print(f"\n🎯 Idea Analysis:")
            
            specific_count = 0
            generic_count = 0
            
            for i, idea in enumerate(ideas[:10], 1):  # Check first 10 ideas
                title = idea.get('title', '').lower()
                description = idea.get('description', '').lower()
                
                # Check for specific vs generic indicators
                specific_indicators = [
                    'change', 'replace', 'add', 'move', 'reduce', 'create', 'implement',
                    'specific', 'tactical', 'action-oriented', 'benefit-first'
                ]
                
                generic_indicators = [
                    'optimize', 'improve', 'enhance', 'better', 'good', 'great'
                ]
                
                has_specific = any(indicator in title or indicator in description for indicator in specific_indicators)
                is_generic = any(phrase in title or phrase in description for phrase in generic_indicators)
                
                if has_specific and not is_generic:
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
            
            print(f"🎯 Overall Assessment:")
            print(f"   Specific ideas: {specific_count}")
            print(f"   Generic ideas: {generic_count}")
            print(f"   Specificity ratio: {specificity_ratio:.1%}")
            
            # Provide recommendations
            print(f"\n💡 Recommendations:")
            
            if ai_working and specificity_ratio >= 0.7:
                print("   ✅ EXCELLENT: AI analysis is working and generating specific ideas!")
                print("   ✅ Your system is ready for real-world use")
                return True
            elif ai_working and specificity_ratio >= 0.4:
                print("   ⚠️  GOOD: AI analysis is working but some ideas are generic")
                print("   💡 Consider improving the AI prompts for better specificity")
                return True
            elif not ai_working:
                print("   ❌ PROBLEM: AI analysis is not working")
                print("   💡 This means you'll get the same generic ideas for all screenshots")
                print("   🔧 Need to fix OpenAI Vision API integration")
                return False
            else:
                print("   ⚠️  MODERATE: Some issues with idea specificity")
                print("   💡 Consider improving the idea generation logic")
                return False
                
        else:
            print(f"❌ Request failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_ai_analysis_with_real_screenshot()
    if success:
        print("\n🎉 Test completed successfully!")
    else:
        print("\n❌ Test failed - AI analysis needs to be fixed.")
        print("\n🔧 To fix AI analysis issues:")
        print("   1. Check OpenAI API key is valid")
        print("   2. Ensure OpenAI Vision API is working")
        print("   3. Verify image format is supported")
        print("   4. Check network connectivity") 