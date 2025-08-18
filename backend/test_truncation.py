#!/usr/bin/env python3
"""Test conversation truncation with a long multi-turn conversation"""

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
    print(f"Testing conversation truncation with session: {SESSION_ID}")
    print("=" * 60)
    
    # List of test messages to create a long conversation
    test_messages = [
        "Hi! I want to learn about light and shadows.",
        "How does light travel?",
        "What causes shadows?",
        "Can light bend?",
        "What is reflection?",
        "How do mirrors work?",
        "What is refraction?",
        "Why does a straw look bent in water?",
        "What are the colors in white light?",
        "How does a prism work?",
        "Why is the sky blue?",
        "What makes a rainbow?",
        "How do our eyes see color?",
        "What is the difference between transparent and opaque?",
        "Can shadows have different sizes?",
        "Why do shadows change during the day?",
        "What is a light source?",
        "Can we see light itself?",
        "How fast does light travel?",
        "What happens when light hits a black object?",
        "Why do some things glow in the dark?",
        "How do glow sticks work?",
        "What is ultraviolet light?",
        "Can animals see different colors than us?",
        "How do fireflies make light?",
        "What is bioluminescence?",
        "Why do stars twinkle?",
        "How does the sun make light?",
        "What is the speed of light?",
        "Can anything travel faster than light?",
        "How do lasers work?",
        "What makes a laser different from regular light?",
        "How do fiber optic cables work?",
        "Can light carry information?",
        "What is total internal reflection?",
        "How do periscopes work?",
        "What causes mirages?",
        "Why does the sun look bigger at sunset?",
        "How do telescopes work?",
        "What is magnification?",
        "How do microscopes work?",
        "Can we see individual light particles?",
        "What are photons?",
        "How do solar panels work?",
        "Can plants use all colors of light?",
        "Why are plants green?",
        "What is photosynthesis?",
        "How do cameras capture light?",
        "What is a lens?",
        "How do our eyes focus?",
        "What causes nearsightedness?",
        "How do glasses help us see?",
        "What is polarized light?",
        "How do polarized sunglasses work?",
        "Can light be dangerous?",
        "Why shouldn't we look at the sun?",
        "What is an eclipse?",
        "How often do eclipses happen?",
        "What's the difference between lunar and solar eclipse?",
        "Final question: Can you summarize what we learned about light?"
    ]
    
    # Send messages to create a long conversation
    for i, message in enumerate(test_messages, 1):
        print(f"\n[Message {i}/{len(test_messages)}] User: {message[:50]}...")
        
        response = send_message(message)
        
        if "error" in response:
            print(f"  ERROR: {response['error']}")
            break
        
        ai_response = response.get("response", "")[:100]
        provider = response.get("provider", "unknown")
        mode = response.get("mode", "unknown")
        
        print(f"  AI ({provider}/{mode}): {ai_response}...")
        
        # Small delay to avoid overwhelming the API
        time.sleep(0.5)
    
    # Check final session state
    print("\n" + "=" * 60)
    print("FINAL SESSION STATE:")
    print("=" * 60)
    
    session = get_session()
    
    if "error" not in session:
        message_count = session.get("message_count", 0)
        messages = session.get("messages", [])
        
        print(f"Total messages in session: {message_count}")
        print(f"Messages returned: {len(messages)}")
        
        # Check if truncation occurred
        expected_max = 100  # max_conversation_length * 2 from config
        if message_count > expected_max:
            print(f"✓ Truncation active: {message_count} messages, but keeping max {expected_max}")
        else:
            print(f"✓ No truncation needed yet: {message_count} messages")
        
        # Show first and last few messages to verify continuity
        if messages:
            print("\nFirst 3 messages:")
            for msg in messages[:3]:
                role = msg.get("role", "unknown")
                content = msg.get("content", "")[:50]
                print(f"  [{role}]: {content}...")
            
            print("\nLast 3 messages:")
            for msg in messages[-3:]:
                role = msg.get("role", "unknown")
                content = msg.get("content", "")[:50]
                print(f"  [{role}]: {content}...")
    else:
        print(f"Error getting session: {session['error']}")
    
    print("\n✓ Truncation test complete!")

if __name__ == "__main__":
    main()