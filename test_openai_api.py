#!/usr/bin/env python3
"""
Test script to check if OpenAI API is working properly
"""

import os
import openai
from dotenv import load_dotenv

def test_openai_api():
    """Test if OpenAI API is working"""
    
    print("🔍 Testing OpenAI API...")
    
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your-openai-api-key-here":
        print("❌ No valid OpenAI API key found in .env file")
        print("   Please set OPENAI_API_KEY=sk-your-actual-key-here")
        return False
    
    print(f"✅ OpenAI API key found: {api_key[:10]}...")
    
    # Initialize OpenAI client
    try:
        client = openai.OpenAI(api_key=api_key)
        print("✅ OpenAI client initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize OpenAI client: {e}")
        return False
    
    # Test simple text completion
    try:
        print("🧪 Testing text completion...")
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": "Say 'Hello, OpenAI API is working!'"}],
            max_tokens=50
        )
        
        content = response.choices[0].message.content
        print(f"✅ Text completion successful: {content}")
        
    except Exception as e:
        print(f"❌ Text completion failed: {e}")
        return False
    
    # Test vision API with a simple image
    try:
        print("🧪 Testing vision API...")
        
        # Create a simple test image (1x1 pixel PNG)
        import base64
        test_image_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\x07tIME\x07\xe5\x07\x16\x0f\x1d\x0c\xc8\xc8\xc8\x00\x00\x00\x0cIDATx\x9cc```\x00\x00\x00\x04\x00\x01\xf5\xc7\xdd\x8c\x00\x00\x00\x00IEND\xaeB`\x82'
        
        image_data = base64.b64encode(test_image_data).decode('utf-8')
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "What do you see in this image? Be very specific."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image_data}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=200
        )
        
        content = response.choices[0].message.content
        print(f"✅ Vision API successful: {content}")
        
    except Exception as e:
        print(f"❌ Vision API failed: {e}")
        print(f"Error type: {type(e).__name__}")
        return False
    
    print("\n✅ All OpenAI API tests passed!")
    return True

if __name__ == "__main__":
    success = test_openai_api()
    if success:
        print("\n🎉 OpenAI API is working correctly!")
    else:
        print("\n❌ OpenAI API has issues that need to be fixed.") 