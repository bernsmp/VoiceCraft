#!/usr/bin/env python3
"""
Refine Voice Matching

This script:
1. Re-creates profile with more articles (10 instead of 5)
2. Extracts specific voice patterns from actual articles
3. Refines humanizer prompt with real examples
4. Tests the improved matching
"""

import sys
import os
import json
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent.parent / '.env.local'
if env_path.exists():
    load_dotenv(env_path)

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.llm_voice_analyzer import LLMVoiceAnalyzer
from core.voice_profiler import VoiceProfiler


def extract_voice_patterns(articles_dir: str) -> dict:
    """Extract specific voice patterns from actual articles"""
    from pathlib import Path
    
    patterns = {
        "opening_hooks": [],
        "signature_phrases": [],
        "sentence_patterns": [],
        "metaphors": [],
        "direct_address": []
    }
    
    dir_path = Path(articles_dir)
    for md_file in sorted(dir_path.glob("*.md"))[:5]:  # Sample first 5
        with open(md_file, 'r') as f:
            content = f.read()
            lines = content.split('\n')
            
            # Extract opening hooks (first 3-5 lines)
            opening = '\n'.join([l.strip() for l in lines[10:20] if l.strip()])
            if opening:
                patterns["opening_hooks"].append(opening[:200])
            
            # Look for signature patterns
            if "The same thing is happening to you" in content:
                patterns["signature_phrases"].append("The same thing is happening to you")
            if "Here's the thing" in content:
                patterns["signature_phrases"].append("Here's the thing")
            if "But here's" in content:
                patterns["signature_phrases"].append("But here's...")
            
            # Direct address patterns
            if "You can't" in content:
                patterns["direct_address"].append("You can't...")
            if "You're" in content[:500]:
                patterns["direct_address"].append("You're...")
    
    return patterns


def refine_profile():
    """Re-create profile with more articles and refine voice matching"""
    
    print("="*70)
    print("Refining Voice Matching")
    print("="*70)
    print()
    
    # Step 1: Load more articles
    print("Step 1: Loading articles...")
    articles_dir = "./data/samples"
    articles = []
    
    for md_file in sorted(Path(articles_dir).glob("*.md")):
        with open(md_file, 'r') as f:
            content = f.read()
            articles.append({
                "filename": md_file.name,
                "content": content,
                "word_count": len(content.split())
            })
    
    print(f"✓ Found {len(articles)} articles")
    print(f"  Total words: {sum(a['word_count'] for a in articles):,}")
    print()
    
    # Step 2: Extract voice patterns
    print("Step 2: Extracting voice patterns from your actual writing...")
    patterns = extract_voice_patterns(articles_dir)
    
    print("✓ Patterns extracted:")
    print(f"  Opening hooks: {len(patterns['opening_hooks'])}")
    print(f"  Signature phrases: {len(set(patterns['signature_phrases']))}")
    print(f"  Direct address patterns: {len(set(patterns['direct_address']))}")
    print()
    
    # Step 3: Re-create profile with more data
    print("Step 3: Re-creating voice profile with {len(articles)} articles...")
    print("  (This will take 1-2 minutes...)")
    print()
    
    analyzer = LLMVoiceAnalyzer()
    
    writing_samples = [a['content'] for a in articles]
    
    try:
        voice_guide = analyzer.create_personal_brand_voice_guide(
            writing_samples=writing_samples,
            author_name="Max Bernstein",
            avatar_blueprint=None,
            voice_connoisseur_analysis=None,
            brand_context={
                "newsletter": "Signal>Noise",
                "description": "Using AI to reveal the hidden patterns that make human expertise valuable and irreplaceable",
                "substack_url": "https://irreplaceablepositioning.substack.com"
            }
        )
        
        print("✓ Profile re-created with more data!")
        print()
        
        # Step 4: Add extracted patterns to profile
        print("Step 4: Adding extracted voice patterns...")
        
        profiler = VoiceProfiler()
        profile_path = profiler._get_profile_path("Max Bernstein")
        
        profile_data = {
            "metadata": {
                "name": "Max Bernstein",
                "created_at": "2025-11-24",
                "updated_at": "2025-11-24",
                "analysis_type": "llm_refined",
                "sources": {
                    "newsletter": "Signal>Noise",
                    "article_count": len(articles),
                    "total_words": sum(a['word_count'] for a in articles)
                }
            },
            "llm_analysis": voice_guide,
            "extracted_patterns": patterns,
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
        
        print(f"✓ Profile saved: {profile_path}")
        print()
        
        # Step 5: Regenerate humanizer with refined patterns
        print("Step 5: Regenerating humanizer with refined voice patterns...")
        
        avatar_blueprint = {
            "strategic_positioning": {
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
                    "Seek authentic voice in AI-driven world"
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
                ]
            }
        }
        
        humanizer_prompt = analyzer.create_ai_humanizer_prompt(
            voice_guide=voice_guide,
            avatar_blueprint=avatar_blueprint,
            author_name="Max Bernstein"
        )
        
        # Enhance prompt with extracted patterns
        enhanced_prompt = enhance_humanizer_with_patterns(humanizer_prompt, patterns)
        
        output_path = Path("./data/outputs/max-bernstein-ai-humanizer-prompt.md")
        with open(output_path, 'w') as f:
            f.write(enhanced_prompt)
        
        print(f"✓ Enhanced humanizer saved: {output_path}")
        print()
        
        # Step 6: Summary
        print("="*70)
        print("Voice Matching Refined!")
        print("="*70)
        print()
        print("Improvements:")
        print(f"  ✅ Profile now uses {len(articles)} articles (was 5)")
        print(f"  ✅ Extracted {len(set(patterns['signature_phrases']))} signature phrases")
        print(f"  ✅ Added real opening hook examples")
        print(f"  ✅ Enhanced humanizer with actual patterns")
        print()
        print("Next: Test the improved humanizer!")
        print("  voicecraft humanize --profile 'Max Bernstein' --input './data/test-ai-text.txt'")
        print()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        raise


def enhance_humanizer_with_patterns(prompt: str, patterns: dict) -> str:
    """Add extracted patterns to humanizer prompt"""
    
    # Find the voice DNA section and enhance it
    enhancement = """
### Extracted Voice Patterns (From Your Actual Writing)

**Opening Hook Style:**
"""
    
    if patterns['opening_hooks']:
        enhancement += f"- {patterns['opening_hooks'][0][:150]}...\n"
        enhancement += f"- {patterns['opening_hooks'][1][:150] if len(patterns['opening_hooks']) > 1 else ''}...\n"
    
    enhancement += """
**Signature Phrases You Actually Use:**
"""
    unique_phrases = list(set(patterns['signature_phrases']))
    for phrase in unique_phrases[:5]:
        enhancement += f"- \"{phrase}\"\n"
    
    enhancement += """
**Direct Address Patterns:**
"""
    unique_address = list(set(patterns['direct_address']))
    for addr in unique_address[:3]:
        enhancement += f"- {addr}\n"
    
    enhancement += """
**Voice Characteristics to Maintain:**
- Story-driven openings (historical examples, metaphors)
- Conversational "you" and "we" to create connection
- Short, punchy sentences mixed with longer reflective ones
- Direct address that creates intimacy ("The same thing is happening to you")
- Philosophical depth wrapped in accessible stories
- Humility and learner's mindset (not authoritative)
"""
    
    # Insert before </my_voice_identity>
    if "</my_voice_identity>" in prompt:
        prompt = prompt.replace("</my_voice_identity>", enhancement + "\n</my_voice_identity>")
    
    return prompt


if __name__ == "__main__":
    refine_profile()


