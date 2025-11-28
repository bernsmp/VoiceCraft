# Prompt Fusion Feature 🎨

## What This Is

**Prompt Fusion** is the unique feature that sets VoiceCraft apart. It blends your authentic voice with master writer prompts (James Clear, Malcolm Gladwell, Paul Graham, Morgan Housel, Tim Urban) to create content that sounds like you, but elevated.

## How It Works

1. **Your Base Voice (70%)** - Your authentic voice profile from analyzed content
2. **Writer Prompts (30%)** - Sophisticated prompts that capture each writer's style
3. **Intelligent Blending** - The AI incorporates stylistic elements while maintaining your core voice

## Available Writers

All prompts are in `/writing prompts/`:

- **James Clear** - Actionable frameworks, 2-minute rules, systems thinking
- **Malcolm Gladwell** - Narrative hooks, specific details, mystery-driven openings
- **Paul Graham** - Contrarian essays, first-principles thinking, sharp insights
- **Morgan Housel** - Timeless principles, historical parallels, simple truths
- **Tim Urban** - Explainer style, memorable characters, "oh shit" moments

## Usage

### CLI Command

```bash
voicecraft generate fusion \
  --profile "Max Bernstein" \
  --topic "How AI is revealing hidden expertise patterns" \
  --writers "James Clear:0.3,Paul Graham:0.2" \
  --length 1200 \
  --output "./output/fusion-article.md"
```

### Python API

```python
from core.prompt_fusion_generator import PromptFusionGenerator

generator = PromptFusionGenerator("Max Bernstein")

result = generator.generate_with_prompt_fusion(
    topic="How to make expertise visible",
    writer_influences=[
        ("James Clear", 0.3),
        ("Malcolm Gladwell", 0.1)
    ],
    output_format="article",
    target_length=1200
)

print(result["content"])
```

## What Makes This Special

1. **Uses Your Actual Prompts** - Not generic style descriptions, but your sophisticated prompts that capture each writer's technique
2. **Maintains Your Voice** - The base voice (70%) ensures it still sounds like you
3. **Intelligent Blending** - Incorporates stylistic elements naturally, not frankensteined
4. **Mix and Match** - Combine multiple writers with different weights

## Example Output

When blending your voice with 30% James Clear on "How AI is revealing hidden expertise patterns":

- ✅ Opens with a specific story (your style)
- ✅ Includes actionable framework (Clear's influence)
- ✅ Maintains your direct, grounded tone
- ✅ Adds Clear's "2-minute starting point" pattern
- ✅ Still sounds authentically like you

## Technical Details

- **Model**: Claude Haiku 4.5 (fast, cost-effective)
- **Prompt Structure**: Base voice + full writer prompts + blending instructions
- **Output**: Content + fusion metadata (writers used, weights, word count)

## Adding New Writers

1. Create a new prompt file in `/writing prompts/`
2. Format: `{writer_name}_prompt.md`
3. Include:
   - Role description
   - Formula/structure
   - Calibration examples (good and bad)
   - Voice markers
   - Anti-patterns
   - Usage instructions

The system will automatically detect and load it.

## Why This Matters

This is what makes VoiceCraft different from just "giving Claude your voice kit." You're not just matching your voice—you're **elevating it** with proven techniques from master writers, while maintaining authenticity.

The prompts you created are sophisticated teaching tools that capture not just what these writers do, but **how** they do it. That's the secret sauce.

