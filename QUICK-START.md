# VoiceCraft Quick Start 🚀

Get up and running with VoiceCraft in 5 minutes!

---

## Step 1: Install Dependencies

```bash
cd "/Users/maxb/Desktop/Vibe Projects/VoiceCraft"
pip install -r requirements.txt
```

**Important:** Download spaCy model:
```bash
python -m spacy download en_core_web_sm
```

---

## Step 2: Set Up API Keys

Create a `.env` file (or set environment variables):

```bash
# OpenAI (recommended)
export OPENAI_API_KEY="sk-your-key-here"

# Or Anthropic
export ANTHROPIC_API_KEY="your-key-here"
```

---

## Step 3: Create Your First Voice Profile

### Using Louie's Content

```bash
python cli/voicecraft.py profile create \
  --name "Louie Bernstein" \
  --samples "../aeo-optimizer-business/clients/louiebernstein/articles/*.md" \
  --description "Sales consultant and fractional sales leader" \
  --tags "sales,consulting,leadership"
```

### Using Jay's Content

```bash
python cli/voicecraft.py profile create \
  --name "Jay Abraham" \
  --samples "../Jay Article Writer/output/**/*.md" \
  --description "Marketing strategist and business consultant" \
  --tags "marketing,strategy,preeminence"
```

---

## Step 4: Generate Your First Article

### Simple Generation (Just Your Voice)

```bash
python cli/voicecraft.py generate article \
  --profile "Louie Bernstein" \
  --topic "How to fix a broken sales process in 30 days" \
  --length 1200 \
  --output "./data/outputs/test-article.md"
```

### With Style Fusion (Your Voice + Influences)

First, create some influence profiles (or use pre-made ones):

```bash
# Create Alex Hormozi profile (you'll need his content samples)
python cli/voicecraft.py profile create \
  --name "Alex Hormozi" \
  --samples "./styles/custom/hormozi/*.txt" \
  --tags "direct,urgent,results"
```

Then generate with blend:

```bash
python cli/voicecraft.py generate article \
  --profile "Louie Bernstein" \
  --topic "Why your sales team is failing (and how to fix it)" \
  --influences "Alex Hormozi:0.3" \
  --length 1000 \
  --output "./data/outputs/blended-article.md"
```

---

## Step 5: Review Results

The output will show:
- ✅ Generated content
- ✅ Word count
- ✅ Voice match score (how well it matches your style)
- ✅ Style blend used

Example output:
```
✓ Content generated!

Format:        article
Word Count:    1,205
Style Blend:   Louie Bernstein + Alex Hormozi (30%)
Voice Match:   87.3%
Model:         gpt-4-turbo-preview
```

---

## Quick Reference Commands

### Manage Profiles

```bash
# List all profiles
python cli/voicecraft.py profile list

# Show profile details
python cli/voicecraft.py profile show "Louie Bernstein"
```

### Generate Content

```bash
# Article (default format)
python cli/voicecraft.py generate article \
  --profile "Your Name" \
  --topic "Your topic"

# With custom length
python cli/voicecraft.py generate article \
  --profile "Your Name" \
  --topic "Your topic" \
  --length 1500

# Save to file
python cli/voicecraft.py generate article \
  --profile "Your Name" \
  --topic "Your topic" \
  --output "./outputs/article.md"
```

### Style Analysis

```bash
# Analyze any writer's style
python cli/voicecraft.py style analyze \
  --name "Writer Name" \
  --samples "./samples/*.txt" \
  --output "./styles/profiles/writer.json"
```

---

## Pro Tips 💡

### 1. More Samples = Better Voice Match
- Use 3-5 substantial pieces (1000+ words each)
- Mix different content types (articles, posts, etc.)
- More samples = more accurate voice profile

### 2. Style Blend Weights
- **Base voice:** Always 60-70% automatically
- **Influences:** Split the remaining 30-40%
- Example: Hormozi:0.3, Godin:0.2 = 30% + 20% = 50% influence
- System auto-normalizes to keep your voice dominant

### 3. Choosing Influences
- **Alex Hormozi:** Direct, urgent, bold claims, action-oriented
- **Seth Godin:** Brief, philosophical, insightful
- **Malcolm Gladwell:** Story-driven, narrative hooks
- **Neil Patel:** SEO-optimized, data-driven, practical

### 4. Model Selection
- **GPT-4 Turbo:** Best overall quality (default)
- **Claude Sonnet:** Great for nuanced, sophisticated content
- **GPT-3.5:** Faster, cheaper, still good quality

```bash
# Use specific model
--model "claude-3-sonnet-20240229"
```

---

## Common Issues & Solutions

### "No AI API keys found"
```bash
# Set environment variable
export OPENAI_API_KEY="your-key"

# Or create .env file (not tracked in git)
echo 'OPENAI_API_KEY="your-key"' > .env
```

### "Profile not found"
```bash
# List all profiles
python cli/voicecraft.py profile list

# Create missing profile
python cli/voicecraft.py profile create --name "Name" --samples "path/*.md"
```

### "No files found matching pattern"
```bash
# Use absolute paths
--samples "/Users/maxb/Desktop/Vibe Projects/..."

# Or relative from VoiceCraft directory
--samples "../aeo-optimizer-business/..."
```

---

## Next Steps

1. ✅ Create voice profiles for your key clients (Louie, Jay, etc.)
2. ✅ Test generation with different style blends
3. ✅ Build library of influence profiles (Hormozi, Godin, etc.)
4. 🚧 Build web dashboard (Phase 2)
5. 🚧 Add auto-publishing to websites (Phase 2)
6. 🚧 Add voice transcription for audio notes (Phase 2)

---

## Example Workflow for Client Content

### For Louie Bernstein:

```bash
# 1. Create his voice profile (once)
python cli/voicecraft.py profile create \
  --name "Louie Bernstein" \
  --samples "../aeo-optimizer-business/clients/louiebernstein/articles/*.md"

# 2. Generate article with his voice + some Hormozi directness
python cli/voicecraft.py generate article \
  --profile "Louie Bernstein" \
  --topic "The Position Contract: Why your sales reps are confused" \
  --influences "Alex Hormozi:0.25" \
  --length 1200 \
  --output "../aeo-optimizer-business/clients/louiebernstein/articles/new-article.md"

# 3. Review the output, adjust if needed
# 4. Publish to his website
```

---

## Getting Help

```bash
# Show all commands
python cli/voicecraft.py --help

# Show examples
python cli/voicecraft.py examples

# Help for specific command
python cli/voicecraft.py profile create --help
```

---

**Ready to create content at scale!** 🎨✨

