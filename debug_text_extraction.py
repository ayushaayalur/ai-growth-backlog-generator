#!/usr/bin/env python3
"""
Debug script to see what text is being extracted from screenshots
"""

import requests
import json
import time
import os

def debug_text_extraction():
    """Debug what text is being extracted from screenshots"""
    
    print("🔍 Debugging Text Extraction...")
    print("=" * 50)
    
    # Wait for backend to start
    print("Waiting for backend to start...")
    time.sleep(3)
    
    # Check if there's a screenshot to test with
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
        return False
    
    print(f"📸 Using test file: {test_file}")
    
    try:
        # Test the analyze endpoint
        with open(test_file, "rb") as f:
            files = {"file": (test_file, f, "image/png")}
            response = requests.post("http://localhost:8000/analyze-screenshot", files=files)
        
        if response.status_code == 200:
            data = response.json()
            metadata = data.get('metadata', {})
            
            extracted_text = metadata.get('extracted_text', '')
            image_description = metadata.get('image_description', '')
            visual_elements = metadata.get('visual_elements', {})
            
            print(f"\n📝 EXTRACTED TEXT:")
            print(f"   Length: {len(extracted_text)} characters")
            print(f"   Content: '{extracted_text}'")
            
            print(f"\n🖼️  IMAGE DESCRIPTION:")
            print(f"   Length: {len(image_description)} characters")
            print(f"   Content: '{image_description[:300]}...'")
            
            print(f"\n🔍 VISUAL ELEMENTS:")
            print(f"   Buttons: {len(visual_elements.get('buttons', []))}")
            print(f"   Forms: {len(visual_elements.get('forms', []))}")
            print(f"   Headlines: {len(visual_elements.get('headlines', []))}")
            print(f"   Images: {len(visual_elements.get('images', []))}")
            
            # Analyze what business type should be detected
            text_lower = extracted_text.lower()
            
            print(f"\n🏢 BUSINESS TYPE ANALYSIS:")
            
            # Check for different business types
            meditation_indicators = ['calm', 'meditation', 'sleep', 'relaxation', 'mindfulness', 'stress', 'anxiety']
            learning_indicators = ['learn', 'masterclass', 'course', 'lesson', 'education', 'skill', 'training', 'instructor', 'teacher']
            ecommerce_indicators = ['shop', 'buy', 'purchase', 'product', 'store', 'cart', 'checkout', 'price', 'sale']
            saas_indicators = ['software', 'app', 'platform', 'tool', 'solution', 'service', 'subscription', 'trial']
            
            meditation_score = sum(1 for indicator in meditation_indicators if indicator in text_lower)
            learning_score = sum(1 for indicator in learning_indicators if indicator in text_lower)
            ecommerce_score = sum(1 for indicator in ecommerce_indicators if indicator in text_lower)
            saas_score = sum(1 for indicator in saas_indicators if indicator in text_lower)
            
            print(f"   Meditation indicators found: {meditation_score}")
            print(f"   Learning indicators found: {learning_score}")
            print(f"   E-commerce indicators found: {ecommerce_score}")
            print(f"   SaaS indicators found: {saas_score}")
            
            # Determine expected business type
            scores = [
                ("meditation_app", meditation_score),
                ("learning_platform", learning_score),
                ("ecommerce", ecommerce_score),
                ("saas", saas_score)
            ]
            
            best_type = max(scores, key=lambda x: x[1])
            print(f"   Expected business type: {best_type[0]} (score: {best_type[1]})")
            
            # Check if text extraction is working properly
            if len(extracted_text) < 50:
                print(f"\n❌ PROBLEM: Text extraction is not working properly")
                print(f"   Only {len(extracted_text)} characters extracted")
                print(f"   This means the system can't identify the business type")
                return False
            elif best_type[1] == 0:
                print(f"\n⚠️  WARNING: No business type indicators found in extracted text")
                print(f"   This means the system will use generic ideas")
                return False
            else:
                print(f"\n✅ Text extraction is working and business type can be identified")
                return True
                
        else:
            print(f"❌ Request failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = debug_text_extraction()
    if success:
        print("\n✅ Text extraction is working properly!")
    else:
        print("\n❌ Text extraction needs to be fixed.") 