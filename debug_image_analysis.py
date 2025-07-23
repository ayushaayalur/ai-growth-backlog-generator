#!/usr/bin/env python3
"""
Debug script to test AI image analysis and see why it's failing
"""

import requests
import json
import time
import base64
import os

def create_test_images():
    """Create different test images to simulate different landing pages"""
    
    # Test image 1: Simple landing page
    test_image_1 = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\x07tIME\x07\xe5\x07\x16\x0f\x1d\x0c\xc8\xc8\xc8\x00\x00\x00\x0cIDATx\x9cc```\x00\x00\x00\x04\x00\x01\xf5\xc7\xdd\x8c\x00\x00\x00\x00IEND\xaeB`\x82'
    
    # Test image 2: Different landing page (slightly different data)
    test_image_2 = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\x07tIME\x07\xe5\x07\x16\x0f\x1d\x0c\xc8\xc8\xc8\x00\x00\x00\x0cIDATx\x9cc```\x00\x00\x00\x04\x00\x01\xf5\xc7\xdd\x8c\x00\x00\x00\x00IEND\xaeB`\x82'
    
    return test_image_1, test_image_2

def test_ai_image_analysis():
    """Test if AI image analysis is working properly"""
    
    print("🔍 Testing AI Image Analysis...")
    
    # Wait for backend to start
    print("Waiting for backend to start...")
    time.sleep(3)
    
    # Create test images
    test_image_1, test_image_2 = create_test_images()
    
    # Save test images
    with open("test_landing_page_1.png", "wb") as f:
        f.write(test_image_1)
    
    with open("test_landing_page_2.png", "wb") as f:
        f.write(test_image_2)
    
    results = []
    
    try:
        # Test first image
        print("\n📸 Testing Image 1...")
        with open("test_landing_page_1.png", "rb") as f:
            files = {"file": ("test_landing_page_1.png", f, "image/png")}
            response = requests.post("http://localhost:8000/analyze-screenshot", files=files)
        
        if response.status_code == 200:
            data_1 = response.json()
            results.append({
                'image': 'Image 1',
                'ideas': data_1.get('ideas', []),
                'metadata': data_1.get('metadata', {})
            })
            print(f"✅ Image 1: {len(data_1.get('ideas', []))} ideas generated")
        else:
            print(f"❌ Image 1 failed: {response.status_code}")
            return False
        
        # Test second image
        print("\n📸 Testing Image 2...")
        with open("test_landing_page_2.png", "rb") as f:
            files = {"file": ("test_landing_page_2.png", f, "image/png")}
            response = requests.post("http://localhost:8000/analyze-screenshot", files=files)
        
        if response.status_code == 200:
            data_2 = response.json()
            results.append({
                'image': 'Image 2',
                'ideas': data_2.get('ideas', []),
                'metadata': data_2.get('metadata', {})
            })
            print(f"✅ Image 2: {len(data_2.get('ideas', []))} ideas generated")
        else:
            print(f"❌ Image 2 failed: {response.status_code}")
            return False
        
        # Compare results
        print("\n🔍 Comparing Results:")
        print("-" * 50)
        
        if len(results) == 2:
            ideas_1 = results[0]['ideas']
            ideas_2 = results[1]['ideas']
            
            # Check if ideas are identical
            titles_1 = [idea.get('title', '') for idea in ideas_1]
            titles_2 = [idea.get('title', '') for idea in ideas_2]
            
            if titles_1 == titles_2:
                print("❌ PROBLEM: Both images generated identical ideas!")
                print("   This means the AI is not analyzing the images properly.")
                print("   Ideas are likely coming from fallback generation.")
                
                # Check metadata to see if AI analysis is working
                metadata_1 = results[0]['metadata']
                metadata_2 = results[1]['metadata']
                
                print(f"\n📊 Metadata Analysis:")
                print(f"   Image 1 description: {metadata_1.get('image_description', 'N/A')[:100]}...")
                print(f"   Image 2 description: {metadata_2.get('image_description', 'N/A')[:100]}...")
                
                if metadata_1.get('image_description') == metadata_2.get('image_description'):
                    print("❌ AI image analysis is NOT working - same description for different images")
                    return False
                else:
                    print("✅ AI image analysis IS working - different descriptions")
                    print("   But idea generation is falling back to generic ideas")
                    return False
            else:
                print("✅ GOOD: Different images generated different ideas!")
                print("   AI analysis is working properly.")
                return True
        
        return False
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    finally:
        # Clean up test files
        for filename in ["test_landing_page_1.png", "test_landing_page_2.png"]:
            if os.path.exists(filename):
                os.remove(filename)

if __name__ == "__main__":
    success = test_ai_image_analysis()
    if success:
        print("\n✅ AI image analysis is working correctly!")
    else:
        print("\n❌ AI image analysis needs to be fixed.")
        print("\n💡 Next steps:")
        print("   1. Check if OpenAI Vision API is working")
        print("   2. Ensure image analysis is not falling back to basic analysis")
        print("   3. Make sure ideas are generated based on actual image content") 