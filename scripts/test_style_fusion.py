#!/usr/bin/env python3
"""
Test Style Fusion End-to-End

This is the ACTUAL unique feature - blending your voice with admired writers.
Let's make it work properly.
"""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent.parent / '.env.local'
if env_path.exists():
    load_dotenv(env_path)

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.content_generator import ContentGenerator, GenerationConfig
from core.voice_profiler import VoiceProfiler
from core.style_blender import StyleBlender


def create_influence_profile(name: str, samples: list) -> dict:
    """Create a style influence profile from samples"""
    from core.style_analyzer import StyleAnalyzer
    
    analyzer = StyleAnalyzer()
    profile = analyzer.analyze_samples(samples, name)
    
    return {
        "metadata": {"name": name},
        "style": profile.to_dict()
    }


def test_style_fusion():
    """Test generating content with style fusion"""
    
    print("="*70)
    print("Testing Style Fusion - The ACTUAL Unique Feature")
    print("="*70)
    print()
    
    # Step 1: Load your voice profile
    print("Step 1: Loading your voice profile...")
    profiler = VoiceProfiler()
    your_voice = profiler.load_profile("Max Bernstein")
    
    if not your_voice:
        print("❌ Your voice profile not found!")
        print("   Run: python3 scripts/create_max_profile.py")
        return
    
    print("✓ Your voice loaded")
    print()
    
    # Step 2: Create influence profiles (or use existing)
    print("Step 2: Creating influence profiles...")
    print("   (We'll create simple ones for testing)")
    
    # Example: Alex Hormozi style (direct, urgent, short sentences)
    hormozi_samples = [
        """
        Most people are broke because they're stupid with money. I'm going to teach you how to not be stupid with money. Ready? Here we go.
        
        First: Stop buying stuff you don't need. Second: Start selling stuff people do need. Third: Take the money from selling stuff and invest it. That's it. That's the whole game.
        
        You want to make $100M? Cool. Sell $100M worth of stuff. It's literally that simple. Not easy. But simple.
        """,
        """
        Everyone wants the secret. There is no secret. It's just work. Lots of work. For a long time. With no guarantee of success.
        
        But here's what I can tell you: If you work harder than everyone else, for longer than everyone else, and you don't quit... you'll probably win. Not definitely. Probably.
        
        That's the game. Work harder. Work longer. Don't quit. The people who win are just the people who didn't stop. That's the whole secret.
        """
    ]
    
    hormozi_profile = create_influence_profile("Alex Hormozi", hormozi_samples)
    print("✓ Alex Hormozi profile created")
    
    # Step 3: Blend styles
    print()
    print("Step 3: Blending your voice with influences...")
    blender = StyleBlender()
    
    blended = blender.blend_styles(
        base_voice=your_voice,
        influences=[
            (hormozi_profile, 0.3)  # 30% Hormozi influence
        ]
    )
    
    print(f"✓ Blend created: {blended['blend_summary']}")
    print()
    
    # Step 4: Generate content with blend
    print("Step 4: Generating content with style fusion...")
    print("   Topic: 'How AI is changing expertise'")
    print("   Blend: Your voice + 30% Hormozi directness")
    print()
    
    generator = ContentGenerator()
    
    if not generator.openai_client and not generator.anthropic_client:
        print("❌ No API keys found!")
        return
    
    try:
        # Convert blended style to format generator expects
        # For now, we'll use the blended instructions directly
        
        result = generator.generate(
            content_brief="How AI is changing the way we think about expertise and irreplaceable knowledge",
            voice_profile=your_voice,
            style_influences=[(hormozi_profile, 0.3)],
            config=GenerationConfig(format="article", target_length=600),
            model="claude-haiku-4-5-20251001"
        )
        
        print("✓ Content generated!")
        print()
        
        # Step 5: Show results
        print("="*70)
        print("Style Fusion Result")
        print("="*70)
        print()
        print(f"Blend: {blended['blend_summary']}")
        print(f"Voice Match: {result['voice_verification']['match_score']}%")
        print()
        print("Generated Content:")
        print("-" * 70)
        print(result['content'])
        print("-" * 70)
        print()
        
        # Step 6: Compare to pure voice
        print("Step 6: Comparing to pure voice (no influences)...")
        pure_result = generator.generate(
            content_brief="How AI is changing the way we think about expertise and irreplaceable knowledge",
            voice_profile=your_voice,
            style_influences=None,
            config=GenerationConfig(format="article", target_length=600),
            model="claude-haiku-4-5-20251001"
        )
        
        print()
        print("Pure Voice (No Influences):")
        print("-" * 70)
        print(pure_result['content'][:500] + "...")
        print("-" * 70)
        print()
        
        print("="*70)
        print("Style Fusion Test Complete!")
        print("="*70)
        print()
        print("This is the unique feature:")
        print("  ✅ Blends YOUR voice with admired writers")
        print("  ✅ Creates content that sounds like you, but elevated")
        print("  ✅ No one else does this")
        print()
        print("Next: Build influence library (Hormozi, Godin, Gladwell, etc.)")
        print()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_style_fusion()

