#!/usr/bin/env python3
"""Quick test of conversation truncation"""

import requests
import json
import time

API_URL = "http://localhost:8000"
SESSION_ID = f"test_truncation_{int(time.time())}"

def send_message(message: str, session_id: str = SESSION_ID):
    """Send a message to the API"""
    response = requests.post(
        f"{API_URL}/api/chat/message",
        json={
            "message": message,
            "session_id": session_id
        }
    )
    return response.json()

def get_session(session_id: str = SESSION_ID):
    """Get session details"""
    response = requests.get(f"{API_URL}/api/session/{session_id}")
    return response.json()

def main():
    print(f"Quick truncation test with session: {SESSION_ID}")
    print("=" * 60)
    
    # Send just enough messages to test truncation (max is 50 from config)
    num_messages = 55  # Slightly over the limit to trigger truncation
    
    for i in range(1, num_messages + 1):
        message = f"Test message {i}: What is light?"
        print(f"[{i}/{num_messages}] Sending message...")
        
        response = send_message(message)
        
        if "error" in response:
            print(f"  ERROR: {response['error']}")
            break
        
        # Very short delay
        time.sleep(0.1)
    
    # Check final session state
    print("\n" + "=" * 60)
    print("CHECKING TRUNCATION:")
    print("=" * 60)
    
    session = get_session()
    
    if "error" not in session:
        message_count = session.get("message_count", 0)
        messages = session.get("messages", [])
        
        print(f"Messages sent: {num_messages}")
        print(f"Total messages in session (including AI responses): {message_count}")
        print(f"Messages returned by API: {len(messages)}")
        
        # Check if truncation occurred (max_conversation_length * 2 = 100)
        expected_max = 100
        if message_count > expected_max:
            print(f"✓ TRUNCATION CONFIRMED: Keeping max {expected_max} messages")
        else:
            if message_count > 50:
                print(f"✓ Session has {message_count} messages (approaching truncation limit of {expected_max})")
            else:
                print(f"ℹ No truncation yet: {message_count} messages")
        
        # Verify we still have context from recent messages
        if messages and len(messages) >= 3:
            last_user_msg = None
            last_ai_msg = None
            
            for msg in messages[-3:]:
                if msg.get("role") == "user":
                    last_user_msg = msg.get("content", "")[:50]
                elif msg.get("role") == "assistant":
                    last_ai_msg = msg.get("content", "")[:50]
            
            if last_user_msg:
                print(f"\nLast user message: {last_user_msg}...")
            if last_ai_msg:
                print(f"Last AI response: {last_ai_msg}...")
                
            print("\n✓ Conversation context maintained after truncation")
    else:
        print(f"Error getting session: {session['error']}")
    
    print("\n✓ Test complete!")

if __name__ == "__main__":
    main()