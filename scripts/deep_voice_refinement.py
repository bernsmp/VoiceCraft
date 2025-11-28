#!/usr/bin/env python3
"""
Deep Voice Refinement

Analyzes Max's actual writing to extract precise patterns and create
a more accurate voice matching system.
"""

import json
from pathlib import Path
import re


def analyze_actual_voice():
    """Deep analysis of Max's actual writing patterns"""
    
    articles_dir = Path("./data/samples")
    all_text = []
    
    # Load all articles
    for md_file in sorted(articles_dir.glob("*.md")):
        with open(md_file, 'r') as f:
            content = f.read()
            all_text.append(content)
    
    combined = "\n\n".join(all_text)
    
    # Extract specific patterns
    patterns = {
        "opening_sentences": [],
        "direct_address": [],
        "we_patterns": [],
        "sentence_lengths": [],
        "fragments": [],
        "historical_references": [],
        "signature_transitions": []
    }
    
    # Analyze opening patterns
    for text in all_text[:5]:
        lines = text.split('\n')
        # Find first substantial paragraph
        for i, line in enumerate(lines[10:30]):
            if len(line.strip()) > 50 and not line.startswith('#'):
                patterns["opening_sentences"].append(line.strip()[:200])
                break
    
    # Find direct address patterns
    direct_patterns = re.findall(r'You [^.!?]+[.!?]', combined)
    patterns["direct_address"] = list(set(direct_patterns[:20]))
    
    # Find "we" patterns
    we_patterns = re.findall(r'[Ww]e [^.!?]+[.!?]', combined)
    patterns["we_patterns"] = list(set(we_patterns[:20]))
    
    # Find sentence fragments
    fragments = re.findall(r'^[A-Z][^.!?]{1,30}\.\s*$', combined, re.MULTILINE)
    patterns["fragments"] = list(set(fragments[:15]))
    
    # Find historical references
    historical = re.findall(r'\d{4}[^.!?]*[.!?]', combined)
    patterns["historical_references"] = list(set(historical[:10]))
    
    # Find signature transitions
    transitions = [
        "The same thing is happening to you",
        "Here's the thing",
        "But here's",
        "What died",
        "Most people think",
        "For years",
        "And he had"
    ]
    found_transitions = []
    for trans in transitions:
        if trans.lower() in combined.lower():
            found_transitions.append(trans)
    patterns["signature_transitions"] = found_transitions
    
    # Calculate sentence lengths
    sentences = re.split(r'[.!?]+', combined)
    for sent in sentences[:100]:
        words = len(sent.split())
        if 5 < words < 50:
            patterns["sentence_lengths"].append(words)
    
    avg_length = sum(patterns["sentence_lengths"]) / len(patterns["sentence_lengths"]) if patterns["sentence_lengths"] else 15
    
    return patterns, avg_length


def create_refined_instructions(patterns, avg_length):
    """Create highly specific voice matching instructions"""
    
    instructions = f"""
### PRECISE VOICE MATCHING INSTRUCTIONS

**Your Voice is Characterized By:**

1. **Opening Style:**
   - Start with direct statements or historical examples
   - NOT flowery metaphors ("Imagine standing at a crossroads" ❌)
   - YES grounded, direct ("You can't explain..." ✅)
   - YES historical hooks ("France, 1737. Antonio Stradivarius..." ✅)

2. **Sentence Structure:**
   - Average sentence length: {avg_length:.1f} words
   - Mix of short fragments and longer reflective sentences
   - Fragments for impact: {patterns['fragments'][:3] if patterns['fragments'] else 'Example fragments'}
   - NOT overly long, complex sentences

3. **Direct Address:**
   - Use "you" frequently and directly
   - Examples from your writing:
{chr(10).join(f'   - "{p}"' for p in patterns['direct_address'][:5])}

4. **Conversational "We":**
   - Use "we" to create community, not authority
   - Examples:
{chr(10).join(f'   - "{p}"' for p in patterns['we_patterns'][:5])}

5. **Signature Transitions:**
   - Use these specific phrases:
{chr(10).join(f'   - "{t}"' for t in patterns['signature_transitions'])}

6. **Tone:**
   - Direct and grounded, NOT flowery
   - Conversational, NOT prescriptive
   - Exploratory, NOT authoritative
   - Humble ("we assumed"), NOT "you should"

**CRITICAL: When Humanizing Text**

1. **If opening is generic:** Replace with direct statement or historical example
   - ❌ "Imagine standing at a crossroads..."
   - ✅ "You can't explain what makes you different."
   - ✅ "France, 1737. Antonio Stradivarius..."

2. **If too flowery:** Make it direct and grounded
   - ❌ "woven into the fabric of our professional lives"
   - ✅ "AI is changing how we work."

3. **If lacks direct address:** Add "you" statements
   - ❌ "Professionals need to..."
   - ✅ "You can't explain..."

4. **If too prescriptive:** Make it exploratory
   - ❌ "You should embrace AI..."
   - ✅ "The same thing is happening to you."

5. **If too abstract:** Ground it with examples or stories
   - ❌ "AI offers transformative possibilities..."
   - ✅ "For two centuries after Stradivarius died, that's exactly what we assumed."

**Voice Test:**
After humanizing, read it aloud. Does it sound like Max Bernstein from Signal>Noise?
- ✅ Direct and grounded?
- ✅ Uses "you" and "we" naturally?
- ✅ Story-driven or historically grounded?
- ✅ Conversational, not prescriptive?
- ❌ Flowery or abstract?
- ❌ Generic business writing?
"""
    
    return instructions


def refine_humanizer():
    """Refine humanizer with deep voice analysis"""
    
    print("="*70)
    print("Deep Voice Refinement")
    print("="*70)
    print()
    
    print("Step 1: Analyzing your actual writing patterns...")
    patterns, avg_length = analyze_actual_voice()
    
    print(f"✓ Analyzed {len(patterns['opening_sentences'])} openings")
    print(f"✓ Found {len(patterns['direct_address'])} direct address patterns")
    print(f"✓ Found {len(patterns['we_patterns'])} 'we' patterns")
    print(f"✓ Average sentence length: {avg_length:.1f} words")
    print()
    
    print("Step 2: Creating precise voice matching instructions...")
    instructions = create_refined_instructions(patterns, avg_length)
    
    print("✓ Instructions created")
    print()
    
    print("Step 3: Updating humanizer prompt...")
    prompt_path = Path("./data/outputs/max-bernstein-ai-humanizer-prompt.md")
    
    with open(prompt_path, 'r') as f:
        prompt = f.read()
    
    # Replace or add the instructions section
    if "### PRECISE VOICE MATCHING INSTRUCTIONS" in prompt:
        # Replace existing
        start = prompt.find("### PRECISE VOICE MATCHING INSTRUCTIONS")
        end = prompt.find("**Voice Test:**", start)
        if end > start:
            end = prompt.find("\n\n", end) + 2
            prompt = prompt[:start] + instructions + prompt[end:]
    else:
        # Add before </my_voice_identity>
        if "</my_voice_identity>" in prompt:
            prompt = prompt.replace("</my_voice_identity>", instructions + "\n</my_voice_identity>")
    
    with open(prompt_path, 'w') as f:
        f.write(prompt)
    
    print(f"✓ Humanizer updated: {prompt_path}")
    print()
    
    print("Step 4: Saving patterns for reference...")
    patterns_path = Path("./data/outputs/max-voice-patterns.json")
    with open(patterns_path, 'w') as f:
        json.dump({
            "patterns": {k: v[:10] if isinstance(v, list) else v for k, v in patterns.items()},
            "avg_sentence_length": avg_length
        }, f, indent=2)
    
    print(f"✓ Patterns saved: {patterns_path}")
    print()
    
    print("="*70)
    print("Refinement Complete!")
    print("="*70)
    print()
    print("Improvements:")
    print("  ✅ Analyzed actual writing patterns")
    print("  ✅ Extracted specific sentence structures")
    print("  ✅ Added precise matching instructions")
    print("  ✅ Included real examples from your writing")
    print()
    print("Test:")
    print("  voicecraft humanize --profile 'Max Bernstein' --input './data/test-ai-draft.md'")
    print()


if __name__ == "__main__":
    refine_humanizer()

