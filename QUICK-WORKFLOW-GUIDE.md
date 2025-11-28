# Quick Workflow Guide - Low Friction Content Creation

## The Goal

**Just input → Get content. No questions, no friction.**

---

## Ultra-Simple Usage

### Method 1: Quick CLI Command

```bash
# Just paste your topic/idea
python3 cli/quick.py "How AI is changing content creation"

# Or pipe input
echo "Sales team optimization tips" | python3 cli/quick.py

# Or from a file
cat my-idea.txt | python3 cli/quick.py
```

### Method 2: Workflow Command (Auto-Detects Everything)

```bash
# Just give it your input - it figures out the rest
python3 cli/workflow.py quick "Your topic here"

# Works with any input type:
python3 cli/workflow.py quick "Your voice note transcript here..."
python3 cli/workflow.py quick "• Point one
• Point two  
• Point three"
```

### Method 3: Full Workflow (More Control)

```bash
# Still simple, but you can specify options
python3 cli/workflow.py create "Your input" --profile "Louie Bernstein"
```

---

## What Gets Auto-Detected

### Input Type Detection

The system automatically detects:
- **Topic** - Short, simple idea
- **Voice Note** - Long text with speech patterns (um, uh, like)
- **Bullet Points** - Lines starting with -, *, •, or numbers
- **WhatsApp** - Conversation format with timestamps/metadata

### Output Format Detection

Automatically chooses the best format:
- **Short input (< 50 words)** → LinkedIn post
- **Medium input (50-200 words)** → Article
- **Long input (> 200 words)** → Article
- **Keywords detected** → Respects explicit requests (e.g., "twitter thread")

---

## Examples

### Example 1: Simple Topic
```bash
python3 cli/quick.py "How to fix a broken sales process"
```
**Result:** Full article, auto-detected, ready to publish

### Example 2: Voice Note Transcript
```bash
python3 cli/quick.py "So I was thinking about this problem where sales teams are struggling with... um... you know, the whole process is broken and we need to..."
```
**Result:** Cleaned up and turned into article

### Example 3: Bullet Points
```bash
python3 cli/quick.py "- Sales process is broken
- Need better training
- Communication issues
- Fix in 30 days"
```
**Result:** Converted to narrative article

### Example 4: WhatsApp Paste
```bash
python3 cli/quick.py "[11:23 AM] You: Hey, I have an idea
[11:24 AM] Me: What's that?
[11:25 AM] You: We should write about sales optimization"
```
**Result:** Extracted idea, turned into content

---

## Mobile-Friendly Usage

### Via Shortcuts App (iOS)

Create a shortcut that:
1. Takes text input
2. Runs: `python3 /path/to/VoiceCraft/cli/quick.py "{input}"`
3. Outputs result

### Via Terminal App (Mobile)

```bash
# SSH into your machine, then:
echo "Your idea" | python3 cli/quick.py
```

### Via API (Future)

```bash
# POST to endpoint
curl -X POST http://localhost:8000/quick \
  -d "input=Your topic here"
```

---

## Environment Variables

Set these for defaults:

```bash
# Default profile
export VOICECRAFT_PROFILE="Louie Bernstein"

# Auto-execute (no prompts)
export AUTO_YES=1

# Then just run:
python3 cli/quick.py "Your topic"
```

---

## Output

By default, content is:
1. ✅ Generated in your voice
2. ✅ Humanized (AI-isms removed)
3. ✅ Saved to `data/outputs/workflow/`
4. ✅ Ready to publish

**File location:** Printed to stdout (for piping/automation)

---

## Advanced: Custom Output Path

```bash
# Save to specific location
python3 cli/workflow.py create "Your topic" --output "./my-article.md"
```

---

## The Magic

**Before:** 
- Input topic → Answer questions → Choose format → Generate → Review → Publish
- **5+ steps, lots of friction**

**Now:**
- Input topic → Get content
- **1 step, zero friction**

---

## What's Next

1. ✅ Auto-detection working
2. ✅ Low-friction CLI ready
3. 🚧 Mobile app integration (coming)
4. 🚧 API endpoint (coming)
5. 🚧 Voice note transcription (coming)

**Try it now:**
```bash
cd "/Users/maxb/Desktop/Vibe Projects/VoiceCraft"
python3 cli/quick.py "Your idea here"
```

