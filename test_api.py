#!/usr/bin/env python3
"""
Test script to verify the API endpoint returns data
"""

import requests
import json
import time

def test_api_endpoint():
    """Test the analyze-screenshot endpoint"""
    
    # Wait for backend to start
    print("Waiting for backend to start...")
    time.sleep(3)
    
    # Test health endpoint
    try:
        health_response = requests.get("http://localhost:8000/health")
        print(f"Health check: {health_response.status_code}")
        print(f"Health response: {health_response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")
        return False
    
    # Create a simple test image (1x1 pixel PNG)
    test_image_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\x07tIME\x07\xe5\x07\x16\x0f\x1d\x0c\xc8\xc8\xc8\x00\x00\x00\x0cIDATx\x9cc```\x00\x00\x00\x04\x00\x01\xf5\xc7\xdd\x8c\x00\x00\x00\x00IEND\xaeB`\x82'
    
    # Save test image
    with open("test_image.png", "wb") as f:
        f.write(test_image_data)
    
    print("Testing analyze-screenshot endpoint...")
    
    try:
        # Test the analyze endpoint
        with open("test_image.png", "rb") as f:
            files = {"file": ("test_image.png", f, "image/png")}
            response = requests.post("http://localhost:8000/analyze-screenshot", files=files)
        
        print(f"Response status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response data keys: {list(data.keys())}")
            
            if 'ideas' in data:
                ideas = data['ideas']
                print(f"Number of ideas returned: {len(ideas)}")
                
                if ideas:
                    first_idea = ideas[0]
                    print(f"First idea keys: {list(first_idea.keys())}")
                    print(f"First idea title: {first_idea.get('title', 'N/A')}")
                    print(f"First idea ICE score: {first_idea.get('ice', {}).get('score', 'N/A')}")
                    
                    return True
                else:
                    print("❌ No ideas returned in response")
                    return False
            else:
                print("❌ No 'ideas' key in response")
                print(f"Response content: {data}")
                return False
        else:
            print(f"❌ Request failed with status {response.status_code}")
            print(f"Response content: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False
    finally:
        # Clean up test file
        import os
        if os.path.exists("test_image.png"):
            os.remove("test_image.png")

if __name__ == "__main__":
    print("🧪 Testing API endpoint...")
    success = test_api_endpoint()
    if success:
        print("\n✅ API test passed! Backend is returning data.")
    else:
        print("\n❌ API test failed. Check the error messages above.") 