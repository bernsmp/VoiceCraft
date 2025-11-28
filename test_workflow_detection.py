#!/usr/bin/env python3
"""
Test workflow auto-detection without requiring API keys
"""

import sys
sys.path.insert(0, '.')

from core.workflow_automation import ContentWorkflow

def test_detection():
    """Test auto-detection logic"""
    
    # Create workflow instance (without initializing API clients)
    workflow = ContentWorkflow.__new__(ContentWorkflow)
    
    print("=" * 60)
    print("Testing Input Type Detection")
    print("=" * 60)
    
    test_cases = [
        ("How AI is changing content creation", "topic"),
        ("- Point one\n- Point two\n- Point three", "bullet_points"),
        ("So I was thinking um you know like this is a really long transcript with lots of um filler words and stuff that goes on and on", "voice_note"),
        ("[11:23 AM] You: Hey, I have an idea\n[11:24 AM] Me: What's that?\n[11:25 AM] You: We should write about sales", "whatsapp"),
    ]
    
    for text, expected in test_cases:
        detected = workflow._detect_input_type(text)
        status = "✅" if detected == expected else "❌"
        print(f"\n{status} Detected: {detected} (Expected: {expected})")
        print(f"   Input: {text[:60]}...")
    
    print("\n" + "=" * 60)
    print("Testing Output Format Detection")
    print("=" * 60)
    
    format_tests = [
        ("How AI is changing content creation", "article"),
        ("Short idea here", "linkedin"),  # Short = LinkedIn
        ("Write a twitter thread about AI", "twitter"),
        ("FAQ questions about sales", "faq"),
        ("Email newsletter about", "email"),
        ("This is a longer topic that should become an article because it has more words and provides more context about the subject matter", "article"),
    ]
    
    for text, expected in format_tests:
        detected = workflow._detect_output_format(text)
        # Check if detection makes sense
        word_count = len(text.split())
        if expected == "linkedin" and word_count < 50:
            status = "✅" if detected == "linkedin" else "⚠️"
        elif expected == "twitter" and "twitter" in text.lower():
            status = "✅" if detected == "twitter" else "⚠️"
        elif expected == "article":
            status = "✅" if detected == "article" else "⚠️"
        else:
            status = "✅" if detected == expected else "⚠️"
        
        print(f"\n{status} Detected: {detected} (Expected: {expected})")
        print(f"   Input: {text[:60]}...")
        print(f"   Word count: {word_count}")
    
    print("\n" + "=" * 60)
    print("✅ Detection tests complete!")
    print("=" * 60)

if __name__ == "__main__":
    test_detection()

