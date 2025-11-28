# VoiceCraft Workflow - Quick Reference

## 🚀 The Complete Flow (At a Glance)

```
INPUT → DETECT → PROCESS → ASSEMBLE → GENERATE → HUMANIZE → PUBLISH → DONE
```

---

## 📥 Input Types

| Type | Detection | Processing |
|------|-----------|------------|
| **Voice Note** | Speech patterns, filler words | Removes filler, preserves energy |
| **WhatsApp** | Timestamps, chat format | Extracts conversation content |
| **Bullet Points** | List markers (-, *, •) | Converts to narrative |
| **Topic** | Default | Used as-is |

---

## 📤 Output Formats

| Format | Detection | Characteristics |
|--------|-----------|-----------------|
| **Article** | 50+ words, default | 2,400-3,400 words, 8-18 lists |
| **LinkedIn** | <30 words, mentions "linkedin" | 150-300 words, first line hook |
| **Twitter** | Mentions "twitter", "tweet" | Thread format, 8-12 tweets |
| **FAQ** | Mentions "faq", "question" | Q&A format |
| **Email** | Mentions "email", "newsletter" | Newsletter format |

---

## 🔧 Components

### 1. Workflow Automation
**File:** `core/workflow_automation.py`  
**Does:** Orchestrates everything  
**Key Method:** `process_input()`

### 2. Content Generator
**File:** `core/content_generator.py`  
**Does:** Generates content with AI  
**Key Method:** `generate()`

### 3. Prompt Assembler
**File:** `core/prompt_assembler.py`  
**Does:** Loads modular prompts  
**Key Method:** `build_prompt()`

### 4. Humanizer
**File:** `core/humanizer.py`  
**Does:** Removes AI-isms  
**Key Method:** `humanize()`

### 5. Publisher
**File:** `core/workflow_automation.py` (publishing methods)  
**Does:** Auto-publishes content  
**Destinations:** GitHub, WordPress, File

---

## 🎯 Quick Examples

### CLI Quick
```bash
python3 cli/quick.py "Your topic here"
```

### Python Quick
```python
from core.workflow_automation import quick_content
content = quick_content("Your topic here")
```

### Full Workflow
```python
from core.workflow_automation import ContentWorkflow

workflow = ContentWorkflow("Max Bernstein")
result = workflow.process_input(
    input_text="Your voice note",
    auto_publish=True,
    publish_config={"destination": "wordpress", "site_url": "yoursite.com"}
)
```

### API Quick
```bash
curl -X POST http://localhost:8000/api/v1/quick \
  -H "Content-Type: application/json" \
  -d '{"input_text": "Your topic"}'
```

---

## 📊 Modular Prompts Loaded

**Always:**
- Voice Profile (Max's patterns)
- Anti-AI Patterns
- Hook Engineering
- Content Structure
- Output Schema

**Conditionally:**
- Viral Psychology (if include_viral)
- Platform Optimization (if platforms specified)
- Input Processing (if input_type != topic)
- Content Multiplication (if multiple platforms)

---

## ✅ Quality Checks

Before output, verifies:
- ✓ Hook grabs in first 3 words
- ✓ Zero banned AI patterns
- ✓ Matches voice calibration
- ✓ Specific numbers included
- ✓ Story-first structure
- ✓ List density 8-18
- ✓ Paragraph average <10 words

---

## 🎨 Voice Patterns Applied

- **Scene Drop:** "France, 1737. Antonio Stradivarius..."
- **Triple Beat:** "Not won't tell. Not don't want to tell. Can't tell."
- **Specific Numbers:** "$10 million" not "significant investment"
- **Named Frameworks:** "The Stradivarius Scanner"
- **Short Punch:** "There it was."

---

## 📱 Platform Optimization

**LinkedIn:** First line hook, professional angle  
**TikTok:** 0-2 second hook, 30-60 sec  
**Instagram:** 0-3 second hook, aesthetic focus  
**YouTube:** 0-5 second hook, series potential

---

## 🔄 Complete Flow Diagram

```
┌─────────────┐
│   INPUT     │ (Voice Note/Topic/etc.)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   DETECT    │ (Auto-detect type & format)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   PROCESS   │ (Clean, extract, structure)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  ASSEMBLE   │ (Load modular prompts)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  GENERATE   │ (AI creates content)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  HUMANIZE   │ (Remove AI-isms)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   PUBLISH   │ (GitHub/WordPress/File)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│     DONE    │ ✅
└─────────────┘
```

---

## ⚡ Speed Reference

- Input Detection: <1 sec
- Prompt Assembly: 1-2 sec
- AI Generation: 20-40 sec
- Humanization: 10-20 sec
- Publishing: 5-10 sec

**Total: 40-75 seconds**

---

## 🎯 Use Cases

**Voice Note → Article:**
```python
workflow.process_input(voice_note, input_type="voice_note", output_format="article")
```

**Topic → LinkedIn:**
```python
quick_content("Your topic", output_format="linkedin")
```

**Multi-Platform:**
```python
config = GenerationConfig(platforms=["linkedin", "tiktok"])
```

**Auto-Publish:**
```python
workflow.process_input(..., auto_publish=True, publish_config={...})
```

---

**See `WORKFLOW-DOCUMENTATION.md` for complete details!**

