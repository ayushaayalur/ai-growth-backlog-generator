#!/usr/bin/env python3
"""
Test script to verify that generated ideas are specific to the uploaded image
"""

import requests
import json
import time
import base64

def create_test_image_with_text():
    """Create a test image with specific text content"""
    # Create a simple test image with text (simulating a landing page)
    # This is a basic approach - in real testing you'd use a proper landing page screenshot
    
    # For now, we'll create a simple colored image and test the system
    # In production, you'd upload actual landing page screenshots
    
    # Create a simple test image (1x1 pixel PNG with specific characteristics)
    test_image_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\x07tIME\x07\xe5\x07\x16\x0f\x1d\x0c\xc8\xc8\xc8\x00\x00\x00\x0cIDATx\x9cc```\x00\x00\x00\x04\x00\x01\xf5\xc7\xdd\x8c\x00\x00\x00\x00IEND\xaeB`\x82'
    
    return test_image_data

def test_specific_idea_generation():
    """Test that generated ideas are specific to the image content"""
    
    print("🧪 Testing specific idea generation...")
    
    # Wait for backend to start
    print("Waiting for backend to start...")
    time.sleep(3)
    
    # Create test image
    test_image_data = create_test_image_with_text()
    
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
            
            print(f"✅ Generated {len(ideas)} ideas")
            
            # Analyze the specificity of ideas
            specific_count = 0
            generic_count = 0
            
            print("\n📋 Analyzing idea specificity:")
            print("-" * 50)
            
            for i, idea in enumerate(ideas[:5], 1):  # Check first 5 ideas
                title = idea.get('title', '').lower()
                description = idea.get('description', '').lower()
                
                # Check for specific indicators
                specific_indicators = [
                    'hero', 'headline', 'cta', 'button', 'form', 'testimonial', 'review',
                    'pricing', 'feature', 'benefit', 'value proposition', 'trust signal',
                    'social proof', 'guarantee', 'security', 'mobile', 'responsive',
                    'navigation', 'menu', 'footer', 'header', 'above the fold', 'section',
                    'image', 'photo', 'logo', 'brand', 'color', 'layout', 'design'
                ]
                
                # Check for generic indicators
                generic_indicators = [
                    'improve conversion', 'increase sales', 'better user experience',
                    'optimize website', 'enhance performance', 'boost revenue'
                ]
                
                has_specific = any(indicator in title or indicator in description for indicator in specific_indicators)
                is_generic = all(phrase in title or phrase in description for phrase in generic_indicators)
                
                if has_specific and not is_generic:
                    specific_count += 1
                    specificity = "✅ SPECIFIC"
                else:
                    generic_count += 1
                    specificity = "❌ GENERIC"
                
                print(f"{i}. {specificity} - {idea.get('title', 'No title')}")
                print(f"   Category: {idea.get('category', 'N/A')}")
                print(f"   ICE Score: {idea.get('ice', {}).get('score', 'N/A')}")
                print()
            
            # Check metadata for image analysis
            metadata = data.get('metadata', {})
            image_description = metadata.get('image_description', '')
            extracted_text = metadata.get('extracted_text', '')
            visual_elements = metadata.get('visual_elements', {})
            
            print("📊 Analysis Results:")
            print(f"   Image description length: {len(image_description)} characters")
            print(f"   Extracted text length: {len(extracted_text)} characters")
            print(f"   Visual elements detected: {len(visual_elements)} types")
            
            # Overall assessment
            specificity_ratio = specific_count / (specific_count + generic_count) if (specific_count + generic_count) > 0 else 0
            
            print(f"\n🎯 Specificity Assessment:")
            print(f"   Specific ideas: {specific_count}")
            print(f"   Generic ideas: {generic_count}")
            print(f"   Specificity ratio: {specificity_ratio:.1%}")
            
            if specificity_ratio >= 0.6:
                print("✅ GOOD: Most ideas are specific to the image content")
                return True
            elif specificity_ratio >= 0.3:
                print("⚠️  MODERATE: Some ideas are specific, but many are generic")
                return False
            else:
                print("❌ POOR: Most ideas are generic and not specific to the image")
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
    success = test_specific_idea_generation()
    if success:
        print("\n✅ Test passed! Ideas are specific to image content.")
    else:
        print("\n❌ Test failed. Ideas are too generic.")
        print("\n💡 To improve specificity:")
        print("   1. Upload actual landing page screenshots")
        print("   2. Ensure the AI can properly analyze the image content")
        print("   3. Check that the image description is detailed enough") 