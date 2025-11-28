#!/usr/bin/env python3
"""
Final Voice Refinement

Adds critical instructions to match Max's actual voice:
- More direct, less flowery
- Story-driven but grounded
- Conversational "we" and direct "you"
- Historical examples, not just metaphors
"""

from pathlib import Path


def final_refinement():
    """Final refinement of humanizer prompt"""
    
    prompt_path = Path("./data/outputs/max-bernstein-ai-humanizer-prompt.md")
    
    with open(prompt_path, 'r') as f:
        prompt = f.read()
    
    # Add critical refinement section
    refinement = """
### CRITICAL: Voice Matching Instructions

**Your voice is NOT:**
- Flowery or overly poetic
- Generic business inspiration
- Prescriptive "you should" language
- Overly metaphorical without substance

**Your voice IS:**
- Direct and conversational ("You can't explain...", "The same thing is happening to you")
- Story-driven with historical examples (Stradivarius, not abstract metaphors)
- Grounded and practical, even when philosophical
- Uses "we" to create community ("we assumed", "we thought")
- Short, punchy sentences mixed with longer reflective ones
- Humble and exploratory, not authoritative

**When Humanizing:**

1. **If text is too flowery:** Make it more direct and grounded
   - ❌ "Imagine standing at the edge of a vast ocean..."
   - ✅ "France, 1737. Antonio Stradivarius knows he's dying."

2. **If text lacks story:** Add historical example or concrete metaphor
   - ❌ "AI integration is important..."
   - ✅ "For two centuries after Stradivarius died, that's exactly what we assumed."

3. **If text is prescriptive:** Make it exploratory
   - ❌ "You should embrace AI..."
   - ✅ "The same thing is happening to you."

4. **If text lacks direct address:** Add "you" for intimacy
   - ❌ "Content creators need to..."
   - ✅ "You can't explain what makes you different."

5. **If text is too formal:** Make it conversational
   - ❌ "It is imperative that..."
   - ✅ "Most people think this is a communication problem."

**Voice Test:** After humanizing, ask: "Does this sound like Max Bernstein from Signal>Noise?" If it sounds like generic business writing or flowery inspiration, refine further.
"""
    
    # Insert before </my_voice_identity>
    if "</my_voice_identity>" in prompt:
        prompt = prompt.replace("</my_voice_identity>", refinement + "\n</my_voice_identity>")
    
    # Also enhance the phase 2 check
    phase2_enhancement = """
**Additional Voice Checks:**

- [ ] Does this sound like Max Bernstein from Signal>Noise?
- [ ] Is it too flowery? (If yes, make more direct)
- [ ] Is it too prescriptive? (If yes, make exploratory)
- [ ] Does it use "we" and "you" naturally?
- [ ] Would Max actually write this?
- [ ] Does it have a story or historical example?
- [ ] Is it grounded, not abstract?
"""
    
    if "## <phase_2_voice_integrity_check>" in prompt:
        # Find and enhance phase 2 section
        phase2_start = prompt.find("## <phase_2_voice_integrity_check>")
        phase2_end = prompt.find("</phase_2_voice_integrity_check>")
        
        if phase2_end > phase2_start:
            phase2_section = prompt[phase2_start:phase2_end]
            if "Does this sound like Max Bernstein" not in phase2_section:
                prompt = prompt[:phase2_end] + phase2_enhancement + "\n</phase_2_voice_integrity_check>" + prompt[phase2_end+len("</phase_2_voice_integrity_check>"):]
    
    # Save
    with open(prompt_path, 'w') as f:
        f.write(prompt)
    
    print(f"✓ Final refinement complete: {prompt_path}")
    print("\nAdded:")
    print("  ✅ Critical voice matching instructions")
    print("  ✅ What your voice IS and ISN'T")
    print("  ✅ Specific transformation examples")
    print("  ✅ Voice test checklist")
    print("\nTest:")
    print("  voicecraft humanize --profile 'Max Bernstein' --input './data/test-ai-text.txt'")


if __name__ == "__main__":
    final_refinement()


