#!/usr/bin/env python3
"""
Enhance Humanizer with Real Examples

Adds actual examples from Max's writing to the humanizer prompt
so it can better match his distinctive voice.
"""

from pathlib import Path
import json


def enhance_humanizer():
    """Add real examples to humanizer prompt"""
    
    prompt_path = Path("./data/outputs/max-bernstein-ai-humanizer-prompt.md")
    
    if not prompt_path.exists():
        print("Humanizer prompt not found. Run refine_voice_matching.py first.")
        return
    
    with open(prompt_path, 'r') as f:
        prompt = f.read()
    
    # Extract real examples from articles
    examples_section = """
### Real Examples of Your Voice (For Reference)

**Example Opening (Story-Driven):**
```
France, 1737. Antonio Stradivarius, the greatest violin maker who ever lived, knows he's dying.

At 93, his breath is shallow and slow. His hands, callused from seventy years of chisel work, stained by countless coats of varnish, lie still against the bedsheets.

His two sons sit beside him. Francesco and Omobono. Men he'd trained since they were boys.

What died with Antonio wasn't knowledge. He'd shared all of that.

It was the hundreds of micro-adjustments he made without thinking.

The same thing is happening to you.
```

**Example Direct Address:**
```
You can't explain what makes you different.

Not because you're bad at marketing. Not because you lack expertise.

But because your most valuable expertise has become invisible, even to you.

And that invisibility is costing you everything.
```

**Example Conversational "We":**
```
Most people think this is a communication problem.

Just find the right words. The right framework. The right documentation system.

For two centuries after Stradivarius died, that's exactly what we assumed.
```

**Example Metaphor/Philosophical Depth:**
```
Antonio Stradivarius couldn't explain his expertise because he'd become too good at it.

His brain had automated the patterns so completely that they bypassed conscious thought.

The same thing is happening to you.
```

**Key Voice Elements to Maintain:**
- **Story-driven openings:** Start with historical examples, metaphors, or compelling narratives
- **Direct address:** Use "you" to create intimacy and connection ("The same thing is happening to you")
- **Conversational "we":** Use "we" and "us" to create community ("that's exactly what we assumed")
- **Short, punchy sentences:** Mix with longer reflective ones for rhythm
- **Philosophical depth:** Wrap complex ideas in accessible stories
- **Humility:** Position as fellow traveler, not authority ("we assumed", "we thought")
- **Metaphors:** Use analogies to bridge complex concepts ("His brain had automated...")
- **Reflective tone:** Invite exploration, don't dictate conclusions
"""
    
    # Add examples section before </my_voice_identity>
    if "</my_voice_identity>" in prompt:
        prompt = prompt.replace("</my_voice_identity>", examples_section + "\n</my_voice_identity>")
    
    # Enhance the task section with specific instructions
    task_enhancement = """
**CRITICAL VOICE MATCHING REQUIREMENTS:**

When humanizing text, ensure it matches these specific patterns from Max's actual writing:

1. **Opening Style:** If the text starts generically, transform it to start with:
   - A story, historical example, or metaphor
   - Direct address ("You can't...", "The same thing is happening to you")
   - A compelling hook that draws readers in

2. **Tone:** 
   - Conversational and reflective, not prescriptive
   - Use "we" and "us" to create community
   - Direct "you" address for intimacy
   - Humility: "we assumed", "we thought", not "you should"

3. **Sentence Structure:**
   - Mix short, punchy sentences with longer reflective ones
   - Use fragments for impact ("Excellent violins. Just not Stradivarius violins.")
   - Vary rhythm to create engagement

4. **Metaphors & Stories:**
   - Wrap complex ideas in accessible stories
   - Use historical examples or analogies
   - Bridge abstract concepts with concrete metaphors

5. **Philosophical Depth:**
   - Don't just state facts—explore the deeper meaning
   - Invite readers to think, not just consume information
   - Show the hidden patterns, not just the surface

6. **Avoid:**
   - Generic business speak
   - Prescriptive "you should" language
   - Formulaic structures
   - Overly technical jargon without explanation
"""
    
    # Add to task section
    if "<task>" in prompt and "</task>" in prompt:
        task_start = prompt.find("<task>")
        task_end = prompt.find("</task>")
        task_section = prompt[task_start:task_end]
        
        if "CRITICAL VOICE MATCHING" not in task_section:
            prompt = prompt[:task_end] + task_enhancement + "\n</task>" + prompt[task_end+7:]
    
    # Save enhanced prompt
    with open(prompt_path, 'w') as f:
        f.write(prompt)
    
    print(f"✓ Enhanced humanizer with real examples: {prompt_path}")
    print("\nThe humanizer now includes:")
    print("  ✅ Real opening examples from your writing")
    print("  ✅ Specific voice patterns to match")
    print("  ✅ Critical matching requirements")
    print("\nTest it:")
    print("  voicecraft humanize --profile 'Max Bernstein' --input './data/test-ai-text.txt'")


if __name__ == "__main__":
    enhance_humanizer()


