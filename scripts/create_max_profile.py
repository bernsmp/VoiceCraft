#!/usr/bin/env python3
"""
Create Max Bernstein's Voice Profile

This script creates a comprehensive voice profile using:
1. Articles from Signal>Noise Substack
2. LLM-powered analysis with sophisticated prompts
3. Complete Personal & Brand Voice Guide
"""

import sys
import os
from pathlib import Path
import json
from dotenv import load_dotenv

# Load environment variables from .env.local
env_path = Path(__file__).parent.parent / '.env.local'
if env_path.exists():
    load_dotenv(env_path)

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.llm_voice_analyzer import LLMVoiceAnalyzer
from core.voice_profiler import VoiceProfiler


def load_articles_from_directory(directory: str) -> list:
    """Load all markdown articles from a directory"""
    articles = []
    dir_path = Path(directory)
    
    if not dir_path.exists():
        print(f"⚠️  Directory not found: {directory}")
        return articles
    
    for md_file in sorted(dir_path.glob("*.md")):
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                articles.append({
                    "filename": md_file.name,
                    "content": content,
                    "word_count": len(content.split())
                })
        except Exception as e:
            print(f"Error reading {md_file}: {e}")
    
    return articles


def create_max_profile():
    """Create Max Bernstein's voice profile"""
    
    print("="*70)
    print("Creating Max Bernstein's Voice Profile")
    print("="*70)
    print()
    
    # Step 1: Load articles
    print("Step 1: Loading articles...")
    articles_dir = "./data/samples"  # Where extracted articles are saved
    
    # Check if articles exist
    articles = load_articles_from_directory(articles_dir)
    
    if not articles:
        print(f"\n⚠️  No articles found in {articles_dir}")
        print("\nOptions:")
        print("1. Run extract_substack_articles.py first:")
        print("   python3 scripts/extract_substack_articles.py https://irreplaceablepositioning.substack.com")
        print("\n2. Manually add articles to ./data/samples/")
        print("\n3. Provide article URLs or content directly")
        return
    
    print(f"✓ Found {len(articles)} articles")
    print(f"  Total words: {sum(a['word_count'] for a in articles):,}")
    print()
    
    # Extract just the content
    writing_samples = [article['content'] for article in articles]
    
    # Step 2: Initialize analyzer
    print("Step 2: Initializing LLM analyzer...")
    analyzer = LLMVoiceAnalyzer()
    
    if not analyzer.openai_client and not analyzer.anthropic_client:
        print("\n⚠️  No AI API keys found!")
        print("Set OPENAI_API_KEY or ANTHROPIC_API_KEY environment variable")
        return
    
    print("✓ Analyzer ready")
    print()
    
    # Step 3: Create voice guide
    print("Step 3: Creating comprehensive voice guide...")
    print("  (This uses the Personal & Brand Voice Guide prompt)")
    print("  Analyzing at 3 levels: Mechanics → Style → Strategy")
    print("  This may take 1-2 minutes...")
    print()
    
    try:
        voice_guide = analyzer.create_personal_brand_voice_guide(
            writing_samples=writing_samples,
            author_name="Max Bernstein",
            avatar_blueprint=None,  # Add if you have one
            voice_connoisseur_analysis=None,  # Add if you've done Voice Connoisseur
            brand_context={
                "newsletter": "Signal>Noise",
                "description": "Using AI to reveal the hidden patterns that make human expertise valuable and irreplaceable",
                "substack_url": "https://irreplaceablepositioning.substack.com"
            }
        )
        
        print("✓ Voice guide created!")
        print()
        
        # Step 4: Save profile
        print("Step 4: Saving profile...")
        profiler = VoiceProfiler()
        
        # Save the LLM analysis
        profile_path = profiler._get_profile_path("Max Bernstein")
        profile_data = {
            "metadata": {
                "name": "Max Bernstein",
                "created_at": "2025-11-24",
                "analysis_type": "llm",
                "sources": {
                    "newsletter": "Signal>Noise",
                    "article_count": len(articles),
                    "total_words": sum(a['word_count'] for a in articles)
                }
            },
            "llm_analysis": voice_guide,
            "articles_analyzed": [
                {
                    "filename": a['filename'],
                    "word_count": a['word_count']
                }
                for a in articles
            ]
        }
        
        with open(profile_path, 'w') as f:
            json.dump(profile_data, f, indent=2)
        
        print(f"✓ Profile saved to: {profile_path}")
        print()
        
        # Step 5: Display summary
        print("="*70)
        print("Profile Creation Complete!")
        print("="*70)
        print()
        print("Next steps:")
        print()
        print("1. Review the voice guide:")
        print(f"   cat {profile_path}")
        print()
        print("2. Generate content in your voice:")
        print("   voicecraft generate article \\")
        print("     --profile 'Max Bernstein' \\")
        print("     --topic 'Your topic here'")
        print()
        print("3. Create AI humanizer:")
        print("   python3 scripts/create_humanizer.py")
        print()
        print("4. Find voice-avatar friction (if you have avatar):")
        print("   python3 scripts/find_friction.py")
        print()
        
    except Exception as e:
        print(f"\n❌ Error creating profile: {e}")
        print("\nTroubleshooting:")
        print("1. Check API keys are set")
        print("2. Verify articles loaded correctly")
        print("3. Check API quota/limits")
        raise


if __name__ == "__main__":
    create_max_profile()

