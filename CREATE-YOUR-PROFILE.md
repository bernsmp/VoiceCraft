# Creating Your Voice Profile from Signal>Noise

## 🎯 Quick Start

You have two options:

### Option 1: Automated Extraction (Recommended)

```bash
# Extract articles from your Substack
cd VoiceCraft
python3 scripts/extract_substack_articles.py https://irreplaceablepositioning.substack.com 10

# Create your voice profile
python3 scripts/create_max_profile.py
```

### Option 2: Manual Collection

1. **Copy articles manually** into `./data/samples/` as `.md` files
2. **Run profile creation:**
   ```bash
   python3 scripts/create_max_profile.py
   ```

---

## 📋 Step-by-Step Process

### Step 1: Extract Articles

**Automated:**
```bash
python3 scripts/extract_substack_articles.py https://irreplaceablepositioning.substack.com
```

**Manual:**
- Go to your Substack dashboard
- Export articles or copy/paste into files
- Save as `./data/samples/article_001.md`, etc.

**What You Need:**
- 5-10 articles minimum (more = better)
- Mix of different types (long-form, short posts, etc.)
- Your authentic writing (not edited by others)

### Step 2: Set API Keys

```bash
export OPENAI_API_KEY="sk-your-key-here"
# OR
export ANTHROPIC_API_KEY="your-key-here"
```

### Step 3: Create Profile

```bash
python3 scripts/create_max_profile.py
```

This will:
1. ✅ Load all articles from `./data/samples/`
2. ✅ Analyze using your sophisticated prompts (3-level analysis)
3. ✅ Create Personal & Brand Voice Guide
4. ✅ Save profile for future use

### Step 4: Review Results

```bash
# View your profile
cat data/voices/max_bernstein.json

# Or pretty print
python3 -m json.tool data/voices/max_bernstein.json
```

---

## 🎨 What Gets Analyzed

### Using Your Prompts (3-Level Analysis)

**Level 1: Mechanics**
- Vocabulary and word choice
- Grammatical patterns
- Punctuation style

**Level 2: Style**
- Sentence structure and length
- Rhetorical devices
- Paragraph organization
- Flow and rhythm

**Level 3: Strategy**
- Tone and mood
- Coherence and cohesion
- Idiosyncrasies and quirks
- Figurative language

### Output: Complete Voice Guide

You'll get:
- ✅ Personal Voice Guide (authentic you)
- ✅ Brand Voice Guide (professional you)
- ✅ Quick reference (DO/DON'T lists)
- ✅ Before/After examples
- ✅ Implementation checklist

---

## 💡 Optional Enhancements

### Add Voice Connoisseur (Discover Through Heroes)

1. **Write a transcript** about writers you admire:
   ```
   "I love Alex Hormozi's directness... Seth Godin's brevity... etc."
   ```

2. **Run discovery:**
   ```python
   from core.llm_voice_analyzer import LLMVoiceAnalyzer
   
   analyzer = LLMVoiceAnalyzer()
   discovery = analyzer.discover_voice_through_heroes(transcript)
   ```

3. **Use in profile creation:**
   ```python
   voice_guide = analyzer.create_personal_brand_voice_guide(
       ...,
       voice_connoisseur_analysis=discovery
   )
   ```

### Add Avatar Blueprint

If you have a customer avatar document:
```python
voice_guide = analyzer.create_personal_brand_voice_guide(
    ...,
    avatar_blueprint={
        "strategic_positioning": "...",
        "psychographics": "..."
    }
)
```

### Find Voice-Avatar Friction

After creating profile:
```python
friction = analyzer.find_voice_avatar_friction(
    voice_guide=voice_guide,
    avatar_blueprint=avatar
)
# Returns: 5 adjustment rules
```

---

## 🚀 After Profile Creation

### Generate Content in Your Voice

```bash
voicecraft generate article \
  --profile "Max Bernstein" \
  --topic "The future of AI-powered content creation" \
  --length 1200 \
  --output "./output/my-article.md"
```

### Create AI Humanizer

```python
from core.llm_voice_analyzer import LLMVoiceAnalyzer

analyzer = LLMVoiceAnalyzer()
humanizer_prompt = analyzer.create_ai_humanizer_prompt(
    voice_guide=your_voice_guide,
    avatar_blueprint=your_avatar,
    author_name="Max Bernstein"
)

# Save it
with open("my-humanizer-prompt.md", "w") as f:
    f.write(humanizer_prompt)
```

### Use for Client Work

Once your profile is created, you can:
1. Generate content for Signal>Noise
2. Use as reference for client voice profiles
3. Train AI to write in your style
4. Maintain consistency across all content

---

## 📊 Expected Results

### Profile Structure

```json
{
  "metadata": {
    "name": "Max Bernstein",
    "analysis_type": "llm",
    "sources": {
      "newsletter": "Signal>Noise",
      "article_count": 10,
      "total_words": 25000
    }
  },
  "llm_analysis": {
    "personal_voice_guide": {...},
    "brand_voice_guide": {...},
    "mechanics": {...},
    "style": {...},
    "strategy": {...}
  }
}
```

### What You'll Learn

- ✅ Your authentic writing patterns
- ✅ How to maintain voice consistency
- ✅ When to use personal vs. brand voice
- ✅ How to integrate admired writer techniques
- ✅ How to align with your audience

---

## 🎯 Quick Commands

```bash
# Extract articles
python3 scripts/extract_substack_articles.py https://irreplaceablepositioning.substack.com

# Create profile
python3 scripts/create_max_profile.py

# Generate content
voicecraft generate article --profile "Max Bernstein" --topic "Your topic"

# View profile
cat data/voices/max_bernstein.json
```

---

## ❓ Troubleshooting

### "No articles found"
- Check `./data/samples/` directory exists
- Verify articles are `.md` files
- Run extraction script first

### "No API keys found"
```bash
export OPENAI_API_KEY="sk-your-key"
```

### "Analysis failed"
- Check API quota/limits
- Verify articles loaded correctly
- Try with fewer articles first (3-5)

### "Profile not found"
```bash
# List all profiles
voicecraft profile list
```

---

**Ready to create your voice profile?** Start with extracting articles! 🚀

