#!/usr/bin/env python3
"""
Test Prompt Fusion - The ACTUAL Unique Feature

Blend your voice with writer prompts (James Clear, Gladwell, Graham, etc.)
"""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent.parent / '.env.local'
if env_path.exists():
    load_dotenv(env_path)

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.prompt_fusion_generator import PromptFusionGenerator, generate_with_fusion

def test_prompt_fusion():
    """Test generating content with writer prompt fusion"""
    
    print("="*70)
    print("Testing Prompt Fusion - Your Voice + Writer Prompts")
    print("="*70)
    print()
    
    # Show available writers
    from core.prompt_library import get_prompt_library
    library = get_prompt_library()
    
    writers = library.list_writers()
    print(f"Available writers: {', '.join(writers)}")
    print()
    
    # Test 1: Your voice + James Clear
    print("Test 1: Your voice + 30% James Clear (Actionable Framework)")
    print("-" * 70)
    
    try:
        generator = PromptFusionGenerator("Max Bernstein")
        
        result = generator.generate_with_prompt_fusion(
            topic="How to make your expertise visible when it's become invisible",
            writer_influences=[("James Clear", 0.3)],
            output_format="article",
            target_length=800
        )
        
        print(f"\n✅ Generated with fusion:")
        print(f"   Base: Max Bernstein (70%)")
        print(f"   Influence: James Clear (30%)")
        print(f"   Word count: {result['word_count']}")
        print()
        print("Content:")
        print("-" * 70)
        print(result['content'])
        print("-" * 70)
        print()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 2: Your voice + Multiple influences
    print("\n" + "="*70)
    print("Test 2: Your voice + Multiple influences")
    print("-" * 70)
    print("   Base: Max Bernstein (70%)")
    print("   + James Clear actionable framework (20%)")
    print("   + Malcolm Gladwell narrative hook (10%)")
    print()
    
    try:
        result2 = generator.generate_with_prompt_fusion(
            topic="Why your best work is dying with you",
            writer_influences=[
                ("James Clear", 0.2),
                ("Malcolm Gladwell", 0.1)
            ],
            output_format="article",
            target_length=600
        )
        
        print("✅ Generated with multi-influence fusion:")
        print()
        print("Content:")
        print("-" * 70)
        print(result2['content'])
        print("-" * 70)
        print()
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("="*70)
    print("Prompt Fusion Test Complete!")
    print("="*70)
    print()
    print("This is the unique feature:")
    print("  ✅ Uses your sophisticated writer prompts")
    print("  ✅ Blends multiple styles intelligently")
    print("  ✅ Maintains your authentic voice")
    print("  ✅ Creates content that sounds like you, but elevated")
    print()
    print("Available writers for fusion:")
    for writer in writers:
        prompt_data = library.get_prompt(writer)
        print(f"  - {writer} ({prompt_data['type']})")
    print()


if __name__ == "__main__":
    test_prompt_fusion()

