#!/usr/bin/env python3
"""
Quick test script to verify API endpoints are working
"""
import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint"""
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Health check failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Failed to connect to backend: {e}")
        return False

def test_chat():
    """Test the chat endpoint"""
    print("\nTesting chat endpoint...")
    test_message = {
        "message": "Hello, can you help me learn about light?",
        "session_id": "test-session-123"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/chat/message",
            json=test_message,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Chat endpoint working")
            print(f"   Provider: {data.get('provider', 'unknown')}")
            print(f"   Mode: {data.get('mode', 'unknown')}")
            print(f"   Response preview: {data['response'][:100]}...")
            return True
        else:
            print(f"❌ Chat endpoint failed with status {response.status_code}")
            print(f"   Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Failed to test chat endpoint: {e}")
        return False

def test_session():
    """Test session retrieval"""
    print("\nTesting session endpoint...")
    session_id = "test-session-123"
    
    try:
        response = requests.get(f"{BASE_URL}/api/session/{session_id}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Session endpoint working")
            print(f"   Messages in session: {len(data.get('messages', []))}")
            return True
        elif response.status_code == 404:
            print("✅ Session endpoint working (session not found as expected)")
            return True
        else:
            print(f"❌ Session endpoint failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Failed to test session endpoint: {e}")
        return False

def main():
    print("=" * 50)
    print("AI Tutor Backend API Test")
    print("=" * 50)
    
    all_passed = True
    
    # Test health endpoint
    if not test_health():
        print("\n⚠️  Backend may not be running. Start it with:")
        print("  cd backend && python -m uvicorn app.main:app --reload")
        sys.exit(1)
    
    # Test chat endpoint
    if not test_chat():
        all_passed = False
    
    # Test session endpoint
    if not test_session():
        all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed. Check the errors above.")
    print("=" * 50)

if __name__ == "__main__":
    main()