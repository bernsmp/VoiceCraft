# VoiceCraft - Agent Reference Guide

## Project Location

**Absolute Path:**
```
/Users/maxb/Desktop/Vibe Projects/VoiceCraft
```

## Quick Start for Agents

### 1. Read These First (in order)
- `START-HERE.md` - Overview and quick start (5 min)
- `PROMPT-FUSION-FEATURE.md` - The unique feature (5 min)
- `README.md` - Complete documentation (20 min)

### 2. Key Files to Understand

**Core System:**
- `core/prompt_library.py` - Loads writer prompts from `/writing prompts/`
- `core/prompt_fusion_generator.py` - Blends voice + writer prompts
- `core/voice_profiler.py` - Creates voice profiles
- `core/content_generator.py` - Generates content
- `core/humanizer.py` - Humanizes AI text

**CLI:**
- `cli/voicecraft.py` - Main CLI interface

**Writer Prompts:**
- `writing prompts/` - Directory with all writer prompts:
  - `james_clear_prompt.md`
  - `malcolm_gladwell_prompt.md`
  - `paul_graham_prompt.md`
  - `morgan_housel_prompt.md`
  - `tim_urban_prompt.md`

**Voice Profiles:**
- `data/voices/` - JSON files with voice profiles
- Example: `data/voices/max_bernstein.json`

**Documentation:**
- `START-HERE.md` - Entry point
- `PROMPT-FUSION-FEATURE.md` - Unique feature explanation
- `HUMANIZER-USAGE.md` - Humanizer guide
- `STYLE-FUSION-DEMO.md` - Style fusion examples

### 3. Main Commands

```bash
# Generate with prompt fusion (THE UNIQUE FEATURE)
voicecraft generate fusion \
  --profile "Max Bernstein" \
  --topic "Your topic" \
  --writers "James Clear:0.3,Paul Graham:0.2" \
  --length 1200

# Generate regular article
voicecraft generate article \
  --profile "Max Bernstein" \
  --topic "Your topic" \
  --length 1200

# Humanize AI text
voicecraft humanize \
  --profile "Max Bernstein" \
  --input "./ai-draft.md" \
  --output "./humanized.md"
```

### 4. What Makes This Special

**Prompt Fusion** - The unique feature that:
- Uses sophisticated writer prompts (not generic descriptions)
- Blends your voice (70%) with writer styles (30%)
- Maintains authenticity while elevating content
- Can mix multiple writers with different weights

**Location:** `core/prompt_fusion_generator.py`

### 5. Project Structure

```
VoiceCraft/
├── core/                      # Core engine
│   ├── prompt_library.py      # Writer prompt loader
│   ├── prompt_fusion_generator.py  # THE UNIQUE FEATURE
│   ├── voice_profiler.py      # Voice profile creator
│   ├── content_generator.py    # Content generator
│   └── humanizer.py           # AI text humanizer
├── cli/                       # CLI tool
│   └── voicecraft.py          # Main CLI
├── writing prompts/           # Writer prompts (THE SECRET SAUCE)
│   ├── james_clear_prompt.md
│   ├── malcolm_gladwell_prompt.md
│   ├── paul_graham_prompt.md
│   ├── morgan_housel_prompt.md
│   └── tim_urban_prompt.md
├── data/
│   ├── voices/                # Voice profiles (JSON)
│   └── outputs/               # Generated content
├── scripts/                   # Utility scripts
└── docs/                      # Documentation
```

### 6. Environment Setup

```bash
# Required environment variables
export ANTHROPIC_API_KEY="your-key-here"  # For Claude (used for writing)
export OPENAI_API_KEY="your-key-here"      # Optional (for GPT-4)
```

### 7. Dependencies

See `requirements.txt` for full list. Key ones:
- `anthropic` - Claude API
- `openai` - OpenAI API (optional)
- `click` - CLI framework
- `rich` - Terminal output formatting

### 8. Current Status

✅ **Working:**
- Prompt fusion (blends voice + writer prompts)
- Voice profiling
- Content generation
- Humanizer
- CLI tool

🎯 **Unique Feature:**
- Prompt Fusion - Uses sophisticated writer prompts to blend styles

📝 **Key Insight:**
This isn't just "give Claude your voice kit" - it's **elevating your voice** with proven techniques from master writers while maintaining authenticity.

### 9. For New Agents

**Start here:**
1. Read `START-HERE.md` (5 min)
2. Read `PROMPT-FUSION-FEATURE.md` (5 min)
3. Run a test: `python3 scripts/test_prompt_fusion.py`
4. Check `cli/voicecraft.py` for available commands

**Key concept:**
The project blends your authentic voice (from analyzed content) with sophisticated writer prompts (in `/writing prompts/`) to create content that sounds like you, but elevated.

---

**Project Path:** `/Users/maxb/Desktop/Vibe Projects/VoiceCraft`  
**Entry Point:** `START-HERE.md`  
**Unique Feature:** `PROMPT-FUSION-FEATURE.md`

