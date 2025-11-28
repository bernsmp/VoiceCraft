# VoiceCraft Tests

All test files are located in the `tests/` folder.

## Test Files

### `test_workflow_detection.py`
Tests auto-detection logic without requiring API keys.
- Input type detection (topic, bullet points, voice note, WhatsApp)
- Output format detection (article, LinkedIn, Twitter, FAQ, email)

**Run:**
```bash
python3 tests/test_workflow_detection.py
```

### `test_real_workflow.sh`
Full workflow tests with API key (requires ANTHROPIC_API_KEY or OPENAI_API_KEY).

**Run:**
```bash
export ANTHROPIC_API_KEY="your-key"
./tests/test_real_workflow.sh
```

### `TEST-RESULTS.md`
Documentation of test results and expected behavior. Includes all test cases and expected outputs.

### `TEST-WITHOUT-API.md`
Guide for testing without API keys. Explains what can be tested without API access.

## Running All Tests

```bash
# Detection tests (no API key needed)
cd /Users/maxb/Desktop/Vibe\ Projects/VoiceCraft
python3 tests/test_workflow_detection.py

# Full workflow tests (requires API key)
export ANTHROPIC_API_KEY="your-key"
./tests/test_real_workflow.sh
```

## Test Output Location

Generated content from tests is saved to:
- `data/outputs/workflow/` - Workflow test outputs
- Check timestamps in filenames to find latest test results
- Example: `linkedin_20251124_135255.md`

## Test Results Summary

✅ **Auto-detection:** Working for topic, bullet points, WhatsApp  
✅ **Format detection:** Working for article, LinkedIn, Twitter, FAQ, email  
✅ **Workflow:** Successfully generated 3 pieces of content  
✅ **API integration:** Working with Claude 4.5 Haiku

## Quick Test

```bash
# Test detection (no API key)
python3 tests/test_workflow_detection.py

# Test full workflow (needs API key)
python3 cli/quick.py "Your topic here"
```

