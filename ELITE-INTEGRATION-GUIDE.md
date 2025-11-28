# ELITE Intelligence Unit Integration Guide

## ✅ What's Been Set Up

I've integrated the **ELITE Intelligence Unit** prompt system into VoiceCraft. Here's what's ready:

### 1. **ELITE Intelligence Unit System** (`prompts/elite_intelligence_unit.py`)
- Complete prompt generation system
- Integrates all 5 knowledge files
- Quality checkpoints built-in
- Anti-AI protocols included
- Voice profile integration

### 2. **Knowledge Files Structure** (`prompts/knowledge/`)
Created 5 knowledge file templates:
- ✅ `psychological_triggers.md`
- ✅ `business_integration.md`
- ✅ `platform_psychology.md`
- ✅ `content_structure.md`
- ✅ `viral_hooks.md`

### 3. **Content Generator Integration**
- Added `use_elite_unit` option to `GenerationConfig`
- Automatically uses ELITE prompts when enabled
- Falls back to regular prompts if ELITE not available

---

## 📝 Next Steps: Add Your Content

### Step 1: Fill in the Knowledge Files

Edit these files with your actual knowledge:

1. **`prompts/knowledge/psychological_triggers.md`**
   - Your psychological trigger frameworks
   - Patterns that work
   - Examples

2. **`prompts/knowledge/business_integration.md`**
   - How to integrate business value
   - Frameworks you use
   - Examples

3. **`prompts/knowledge/platform_psychology.md`**
   - Platform-specific insights
   - What works on each platform
   - Format optimizations

4. **`prompts/knowledge/content_structure.md`**
   - Your proven structures
   - Opening patterns
   - Transition strategies

5. **`prompts/knowledge/viral_hooks.md`**
   - Hook patterns that work
   - Opening strategies
   - Shareability elements

---

## 🚀 How to Use

### Option 1: Use in Content Generator

```python
from core.content_generator import ContentGenerator, GenerationConfig
from core.voice_profiler import VoiceProfiler

# Load your voice profile
profiler = VoiceProfiler()
voice_profile = profiler.load_profile("Max Bernstein")

# Create generator
generator = ContentGenerator()

# Generate with ELITE Intelligence Unit
config = GenerationConfig(
    format="article",
    target_length=1200,
    use_elite_unit=True  # Enable ELITE system
)

result = generator.generate(
    content_brief="How AI is changing expertise",
    voice_profile=voice_profile,
    config=config
)
```

### Option 2: Use in Workflow Automation

The workflow automation will automatically use ELITE if you enable it:

```python
from core.workflow_automation import ContentWorkflow

workflow = ContentWorkflow("Max Bernstein")

# The workflow will use ELITE when generating content
# (You'll need to modify workflow_automation.py to pass use_elite_unit=True)
```

### Option 3: Direct ELITE Prompt Generation

```python
from prompts.elite_intelligence_unit import get_elite_prompt

prompt = get_elite_prompt(
    topic="How AI is changing expertise",
    output_format="article",
    target_length=1200,
    voice_profile=voice_profile
)

# Use this prompt with Claude/OpenAI directly
```

---

## 🔧 Customization

### Modify the ELITE Prompt Structure

Edit `prompts/elite_intelligence_unit.py` to:
- Change role definitions
- Adjust quality checkpoints
- Modify anti-AI protocols
- Add custom sections

### Add More Knowledge Files

1. Create new `.md` file in `prompts/knowledge/`
2. Add to `knowledge_files` dict in `EliteIntelligenceUnit._load_knowledge_files()`
3. Reference in `get_content_generation_prompt()`

---

## 📋 Current Status

✅ **Structure:** Complete  
✅ **Integration:** Complete  
⏳ **Knowledge Files:** Need your content  
⏳ **Testing:** Ready to test once knowledge files are filled

---

## 🎯 What You Need to Do

1. **Fill in the 5 knowledge files** with your actual frameworks and knowledge
2. **Test the system** with a simple generation
3. **Refine as needed** based on outputs

The system is ready - just add your knowledge content!

---

## 💡 Example Knowledge File Structure

Here's how you might structure a knowledge file:

```markdown
# Psychological Triggers

## Core Principles
- [Your principle 1]
- [Your principle 2]

## Trigger Patterns
### Pattern 1: [Name]
- How it works: [explanation]
- When to use: [guidance]
- Example: [example]

### Pattern 2: [Name]
- How it works: [explanation]
- When to use: [guidance]
- Example: [example]

## Usage Guidelines
- Use authentically, not manipulatively
- Integrate naturally into content
- Test and refine based on results
```

---

**The system is ready - add your knowledge and start generating!**

