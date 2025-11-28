# VoiceCraft Installation Guide

## Quick Install

```bash
cd "/Users/maxb/Desktop/Vibe Projects/VoiceCraft"

# Install all dependencies
pip3 install -r requirements.txt

# Download spaCy language model
python3 -m spacy download en_core_web_sm

# Set your OpenAI API key
export OPENAI_API_KEY="your-key-here"

# Test the installation
python3 test_style_analyzer.py
```

## What Gets Installed

### Core AI Libraries
- `openai` - GPT-4 for content generation
- `anthropic` - Claude for content generation
- `spacy` - NLP text analysis
- `textstat` - Readability metrics
- `textblob` - Sentiment analysis

### CLI & Interface
- `click` - Command-line framework
- `rich` - Beautiful terminal output

### Utilities
- `python-dotenv` - Environment variables
- `pyyaml` - Configuration files
- And more...

## Troubleshooting

### "No module named 'X'"
```bash
pip3 install -r requirements.txt
```

### "spaCy model not found"
```bash
python3 -m spacy download en_core_web_sm
```

### "No AI API keys found"
```bash
export OPENAI_API_KEY="sk-your-key"
# Or create a .env file:
echo 'OPENAI_API_KEY="sk-your-key"' > .env
```

## Verify Installation

```bash
# Test without API keys (style analysis only)
python3 test_style_analyzer.py

# Test full system (requires API key)
python3 cli/voicecraft.py --help
```

## Next Steps

Once installed, read:
1. `QUICK-START.md` - Get up and running
2. `README.md` - Full documentation
3. `PROJECT-STATUS.md` - Current status and roadmap

---

**Estimated install time:** 5-10 minutes (depending on internet speed)

