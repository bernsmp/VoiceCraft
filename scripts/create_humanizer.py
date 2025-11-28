#!/usr/bin/env python3
"""
Create Personalized AI Text Humanizer Prompt

This generates a complete, ready-to-use humanizer prompt based on:
1. Your voice profile
2. Your avatar/audience
3. Master AI-ism list
"""

import sys
import os
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent / '.env.local'
if env_path.exists():
    load_dotenv(env_path)

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.llm_voice_analyzer import LLMVoiceAnalyzer
from core.voice_profiler import VoiceProfiler


def create_humanizer_prompt():
    """Create personalized AI humanizer prompt for Max"""
    
    print("="*70)
    print("Creating Your Personalized AI Text Humanizer")
    print("="*70)
    print()
    
    # Step 1: Load voice profile
    print("Step 1: Loading your voice profile...")
    profiler = VoiceProfiler()
    voice_profile = profiler.load_profile("Max Bernstein")
    
    if not voice_profile:
        print("❌ Voice profile not found!")
        print("   Run: python3 scripts/create_max_profile.py first")
        return
    
    print("✓ Voice profile loaded")
    print()
    
    # Step 2: Create avatar blueprint (Signal>Noise audience)
    print("Step 2: Creating avatar blueprint...")
    
    # Extract from voice profile or create based on Signal>Noise
    avatar_blueprint = {
        "strategic_positioning": {
            "positioning_statement": "Signal>Noise serves established experts and ambitious professionals who value research-backed frameworks over generic influencer advice, seek strategic AI integration without losing authenticity, and want sustainable systems that respect their time and expertise level.",
            "key_differentiators": [
                "Deep analysis over surface-level tips",
                "AI integration that preserves human expertise",
                "Pattern recognition and strategic thinking",
                "Community of thoughtful practitioners"
            ],
            "broader_audience_segment": "Established experts and ambitious professionals navigating AI adoption--specifically those who value research-backed frameworks, want to create depth without becoming content machines, and seek strategic AI integration that maintains authentic voice."
        },
        "psychographics": {
            "values": [
                "Research-backed methodologies over generic advice",
                "Authentic differentiation in AI-saturated market",
                "Depth over volume in content creation",
                "Strategic thinking and pattern recognition"
            ],
            "mindsets": [
                "Overwhelmed by options but committed to depth",
                "Want results without becoming 'content machines'",
                "Seek authentic voice in AI-driven world",
                "Value expertise and nuanced thinking"
            ],
            "what_they_seek": [
                "Hidden patterns that make expertise valuable",
                "AI integration that enhances rather than replaces",
                "Sustainable systems for content creation",
                "Community of thoughtful practitioners"
            ]
        },
        "communication_preferences": {
            "what_resonates": [
                "Deep analysis with clear explanations",
                "Metaphors and analogies that clarify complex ideas",
                "Conversational tone that invites exploration",
                "Stories and historical context",
                "Humility and learner's mindset"
            ],
            "what_they_resist": [
                "Generic influencer advice",
                "Surface-level tips without depth",
                "Overly technical jargon without explanation",
                "Authoritative tone that talks down",
                "Formulaic content patterns"
            ],
            "natural_language": [
                "Hidden patterns",
                "Strategic integration",
                "Research-backed",
                "Authentic voice",
                "Sustainable systems",
                "Depth over volume"
            ],
            "sophistication_level": "High - appreciate complexity but need clarity",
            "context": "Professionals actively navigating AI adoption while maintaining expertise"
        }
    }
    
    print("✓ Avatar blueprint created")
    print()
    
    # Step 3: Initialize analyzer
    print("Step 3: Initializing analyzer...")
    analyzer = LLMVoiceAnalyzer()
    
    if not analyzer.openai_client and not analyzer.anthropic_client:
        print("❌ No AI API keys found!")
        print("   Set OPENAI_API_KEY or ANTHROPIC_API_KEY")
        return
    
    print("✓ Analyzer ready")
    print()
    
    # Step 4: Generate humanizer prompt
    print("Step 4: Generating personalized humanizer prompt...")
    print("   (This uses your voice profile + avatar blueprint)")
    print("   This may take 30-60 seconds...")
    print()
    
    try:
        humanizer_prompt = analyzer.create_ai_humanizer_prompt(
            voice_guide=voice_profile.get("llm_analysis", {}),
            avatar_blueprint=avatar_blueprint,
            author_name="Max Bernstein"
        )
        
        print("✓ Humanizer prompt generated!")
        print()
        
        # Step 5: Save prompt
        print("Step 5: Saving humanizer prompt...")
        output_path = Path("./data/outputs/max-ai-humanizer-prompt.md")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(humanizer_prompt)
        
        print(f"✓ Saved to: {output_path}")
        print()
        
        # Step 6: Display summary
        print("="*70)
        print("AI Humanizer Prompt Created!")
        print("="*70)
        print()
        print("What you got:")
        print("  ✅ Personalized to YOUR voice (Max Bernstein)")
        print("  ✅ Calibrated for YOUR audience (Signal>Noise readers)")
        print("  ✅ Complete AI-ism detection system")
        print("  ✅ Ready to use - just copy and paste!")
        print()
        print("How to use:")
        print("  1. Copy the prompt from: data/outputs/max-ai-humanizer-prompt.md")
        print("  2. Paste it into Claude/ChatGPT")
        print("  3. Add your text below the prompt")
        print("  4. Get back humanized text in YOUR voice")
        print()
        print("Example usage:")
        print("  ---")
        print("  [Paste your humanizer prompt]")
        print("  ---")
        print("  [Paste AI-generated text to humanize]")
        print("  ---")
        print()
        print("The prompt will:")
        print("  ✅ Eliminate all AI-isms ruthlessly")
        print("  ✅ Maintain YOUR authentic voice")
        print("  ✅ Speak to YOUR audience")
        print("  ✅ Preserve all facts and meaning")
        print()
        
    except Exception as e:
        print(f"\n❌ Error creating humanizer: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    create_humanizer_prompt()

