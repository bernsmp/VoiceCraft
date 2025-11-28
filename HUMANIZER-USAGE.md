# Using the Built-In Humanizer

## 🎯 Why Built-In?

**You asked:** "Why would we do that outside of Cursor?"

**Answer:** We don't! The humanizer is now **built directly into VoiceCraft** so you can use it right here.

---

## 🚀 Quick Usage

### CLI Command

```bash
# Humanize text directly
voicecraft humanize \
  --profile "Max Bernstein" \
  --text "AI-generated text here..." \
  --output "./output/humanized.md"

# From a file
voicecraft humanize \
  --profile "Max Bernstein" \
  --input "./ai-draft.md" \
  --output "./humanized.md" \
  --analysis  # Show what changed
```

### Python Function

```python
from core.humanizer import humanize_text

# Quick humanize
cleaned = humanize_text("AI-generated text here...")

# Or with more control
from core.humanizer import Humanizer

humanizer = Humanizer(profile_name="Max Bernstein")
result = humanizer.humanize(
    text="AI-generated text...",
    show_analysis=True  # See what changed
)

print(result["humanized"])
print(result["analysis"])  # What changed
```

---

## 💡 Use Cases

### 1. Clean AI-Generated First Drafts

```bash
# Generate article
voicecraft generate article \
  --profile "Max Bernstein" \
  --topic "AI content creation" \
  --output "./draft.md"

# Humanize it
voicecraft humanize \
  --profile "Max Bernstein" \
  --input "./draft.md" \
  --output "./final.md"
```

### 2. Clean Client Content

```bash
# Humanize content for Louie
voicecraft humanize \
  --profile "Louie Bernstein" \
  --input "./louie-draft.md" \
  --output "./louie-final.md"
```

### 3. Batch Processing

```python
from core.humanizer import Humanizer
from pathlib import Path

humanizer = Humanizer("Max Bernstein")

for file in Path("./ai-drafts/").glob("*.md"):
    with open(file) as f:
        text = f.read()
    
    result = humanizer.humanize(text)
    
    output_file = Path("./humanized/") / file.name
    output_file.parent.mkdir(exist_ok=True)
    
    with open(output_file, 'w') as f:
        f.write(result["humanized"])
    
    print(f"✓ {file.name}")
```

---

## 🎨 What It Does

1. **Eliminates AI-isms** - Removes all robotic patterns
2. **Maintains Your Voice** - Keeps your authentic style
3. **Speaks to Your Audience** - Calibrated for Signal>Noise readers
4. **Preserves Facts** - Never changes meaning or data

---

## 📊 Example

**Input (AI-generated):**
```
In today's fast-paced digital landscape, leveraging AI-powered solutions has become increasingly important for content creators seeking to optimize their workflow and maximize productivity.
```

**Output (Humanized in your voice):**
```
When we think about weaving AI into our content creation, it's like discovering a new tool that can help us work smarter—not harder. But here's the thing: the real value isn't in the tool itself. It's in how we use it to reveal the patterns that make our expertise irreplaceable.
```

**What Changed:**
- Removed: "In today's fast-paced digital landscape" (formulaic opening)
- Removed: "leveraging," "increasingly important" (AI buzzwords)
- Added: Your conversational tone ("When we think about...")
- Added: Your signature metaphor ("it's like discovering...")
- Added: Your pattern-focused thinking ("reveal the patterns...")

---

## 🔧 Advanced Usage

### Show Analysis

```bash
voicecraft humanize \
  --profile "Max Bernstein" \
  --input "./draft.md" \
  --analysis  # Shows what changed
```

### Use Different Model

```bash
voicecraft humanize \
  --profile "Max Bernstein" \
  --input "./draft.md" \
  --model "claude-3-sonnet-20240229"
```

### Python with Full Control

```python
from core.humanizer import Humanizer

humanizer = Humanizer(
    profile_name="Max Bernstein",
    model="gpt-4o"
)

result = humanizer.humanize(
    text="Your AI text here...",
    show_analysis=True,
    model="gpt-4o"  # Override
)

# Access results
print("Humanized:", result["humanized"])
print("Analysis:", result.get("analysis"))
print("Model:", result["model_used"])
```

---

## ✅ Benefits of Built-In

1. **No Copy/Paste** - Use it directly in VoiceCraft
2. **Automated Workflows** - Integrate into your pipeline
3. **Consistent Results** - Same prompt every time
4. **Batch Processing** - Handle multiple files
5. **CLI Integration** - Use from command line
6. **Python API** - Integrate into scripts

---

## 🎯 Workflow Integration

### Complete Content Pipeline

```bash
# 1. Generate content
voicecraft generate article \
  --profile "Max Bernstein" \
  --topic "Your topic" \
  --output "./draft.md"

# 2. Humanize it
voicecraft humanize \
  --profile "Max Bernstein" \
  --input "./draft.md" \
  --output "./final.md"

# 3. Review and publish
```

### Python Script

```python
from core.content_generator import ContentGenerator
from core.humanizer import Humanizer
from core.voice_profiler import VoiceProfiler

# Generate
profiler = VoiceProfiler()
profile = profiler.load_profile("Max Bernstein")

generator = ContentGenerator()
article = generator.generate(
    content_brief="Your topic",
    voice_profile=profile
)

# Humanize
humanizer = Humanizer("Max Bernstein")
final = humanizer.humanize(article["content"])

# Save
with open("final.md", "w") as f:
    f.write(final["humanized"])
```

---

**Everything stays in VoiceCraft. No external tools needed!** 🎨✨

