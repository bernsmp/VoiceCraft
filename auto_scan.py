#!/usr/bin/env python3
"""
Auto-scan script for VoiceCraft project
Automatically scans all files and updates PROJECT-SCAN-SUMMARY.md
Runs without prompts or user interaction
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import json

# Get project root
PROJECT_ROOT = Path(__file__).parent
SUMMARY_FILE = PROJECT_ROOT / "PROJECT-SCAN-SUMMARY.md"

def count_files(directory, extensions=None, exclude_dirs=None):
    """Count files in directory, optionally filtered by extension"""
    if exclude_dirs is None:
        exclude_dirs = {'__pycache__', '.git', 'node_modules', '.next', 'dist', 'build', '.venv', 'venv'}
    
    count = 0
    for root, dirs, files in os.walk(directory):
        # Remove excluded directories from dirs list to prevent traversal
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            if extensions is None or any(file.endswith(ext) for ext in extensions):
                count += 1
    return count

def get_file_structure():
    """Get project file structure"""
    structure = {
        'core': [],
        'cli': [],
        'scripts': [],
        'writing_prompts': [],
        'integrations': [],
        'data': {'voices': [], 'outputs': [], 'samples': []},
        'docs': [],
        'root_files': []
    }
    
    # Core files
    core_dir = PROJECT_ROOT / 'core'
    if core_dir.exists():
        structure['core'] = [f.name for f in core_dir.glob('*.py') if f.is_file()]
    
    # CLI files
    cli_dir = PROJECT_ROOT / 'cli'
    if cli_dir.exists():
        structure['cli'] = [f.name for f in cli_dir.glob('*.py') if f.is_file()]
    
    # Scripts
    scripts_dir = PROJECT_ROOT / 'scripts'
    if scripts_dir.exists():
        structure['scripts'] = [f.name for f in scripts_dir.glob('*.py') if f.is_file()]
    
    # Writing prompts
    prompts_dir = PROJECT_ROOT / 'writing prompts'
    if prompts_dir.exists():
        structure['writing_prompts'] = [f.name for f in prompts_dir.glob('*.md') if f.is_file()]
    
    # Integrations
    integrations_dir = PROJECT_ROOT / 'integrations'
    if integrations_dir.exists():
        structure['integrations'] = [f.name for f in integrations_dir.glob('*.py') if f.is_file()]
    
    # Data subdirectories
    data_dir = PROJECT_ROOT / 'data'
    if data_dir.exists():
        voices_dir = data_dir / 'voices'
        if voices_dir.exists():
            structure['data']['voices'] = [f.name for f in voices_dir.glob('*.json') if f.is_file()]
        
        outputs_dir = data_dir / 'outputs'
        if outputs_dir.exists():
            structure['data']['outputs'] = [f.name for f in outputs_dir.glob('*') if f.is_file()]
        
        samples_dir = data_dir / 'samples'
        if samples_dir.exists():
            structure['data']['samples'] = [f.name for f in samples_dir.glob('*.md') if f.is_file()]
    
    # Root markdown files
    structure['root_files'] = [f.name for f in PROJECT_ROOT.glob('*.md') if f.is_file()]
    
    return structure

def generate_summary():
    """Generate updated summary"""
    timestamp = datetime.now().strftime("%B %d, %Y at %H:%M:%S")
    
    # Count files
    python_files = count_files(PROJECT_ROOT, ['.py'])
    markdown_files = count_files(PROJECT_ROOT, ['.md'])
    json_files = count_files(PROJECT_ROOT, ['.json'])
    
    # Get structure
    structure = get_file_structure()
    
    summary = f"""# VoiceCraft Project - Auto-Scanned Summary

**Last Updated:** {timestamp}  
**Location:** `/Users/maxb/Desktop/Vibe Projects/VoiceCraft`  
**Status:** MVP Phase - Core Engine Complete ✅

---

## Quick Stats

- **Python Files:** {python_files}
- **Markdown Files:** {markdown_files}
- **JSON Files:** {json_files}
- **Total Files Scanned:** {python_files + markdown_files + json_files}+

---

## Project Structure

### Core Engine (`/core/`)
{len(structure['core'])} Python modules:
{chr(10).join(f"- `{f}`" for f in sorted(structure['core'])) if structure['core'] else "- No files found"}

### CLI Tool (`/cli/`)
{len(structure['cli'])} Python files:
{chr(10).join(f"- `{f}`" for f in sorted(structure['cli'])) if structure['cli'] else "- No files found"}

### Scripts (`/scripts/`)
{len(structure['scripts'])} utility scripts:
{chr(10).join(f"- `{f}`" for f in sorted(structure['scripts'])) if structure['scripts'] else "- No files found"}

### Writer Prompts (`/writing prompts/`)
{len(structure['writing_prompts'])} prompt files:
{chr(10).join(f"- `{f}`" for f in sorted(structure['writing_prompts'])) if structure['writing_prompts'] else "- No files found"}

### Integrations (`/integrations/`)
{len(structure['integrations'])} integration files:
{chr(10).join(f"- `{f}`" for f in sorted(structure['integrations'])) if structure['integrations'] else "- No files found"}

### Data Storage (`/data/`)

**Voice Profiles:** {len(structure['data']['voices'])} files
{chr(10).join(f"- `{f}`" for f in sorted(structure['data']['voices'])) if structure['data']['voices'] else "- No voice profiles"}

**Outputs:** {len(structure['data']['outputs'])} files
{chr(10).join(f"- `{f}`" for f in sorted(structure['data']['outputs'])[:10]) if structure['data']['outputs'] else "- No outputs"}
{f"{chr(10)}... and {len(structure['data']['outputs']) - 10} more" if len(structure['data']['outputs']) > 10 else ""}

**Samples:** {len(structure['data']['samples'])} sample files
{chr(10).join(f"- `{f}`" for f in sorted(structure['data']['samples'])) if structure['data']['samples'] else "- No samples"}

### Documentation (Root)
{len(structure['root_files'])} markdown files:
{chr(10).join(f"- `{f}`" for f in sorted(structure['root_files'])) if structure['root_files'] else "- No documentation files"}

---

## Project Status

✅ **Core Engine:** Complete  
✅ **CLI Tool:** Complete  
✅ **Documentation:** Complete  
🚧 **Web Dashboard:** Planned  
🚧 **Auto-Publishing:** In Progress  

---

## Next Steps

1. Test with real content (Louie Bernstein, Jay Abraham)
2. Build style library (Hormozi, Godin, Gladwell)
3. Refine prompt fusion
4. Add auto-publishing integrations
5. Build web dashboard

---

**Auto-generated by:** `auto_scan.py`  
**Run manually:** `python3 auto_scan.py`  
**Auto-updates:** Every time this script runs

"""
    
    return summary

def check_auto_config():
    """Check if auto-scan is enabled"""
    config_file = PROJECT_ROOT / ".voicecraft_auto"
    if config_file.exists():
        with open(config_file, 'r') as f:
            content = f.read()
            return "AUTO_SCAN=1" in content
    # Also check environment variable
    return os.getenv('AUTO_SCAN') == '1'

def main():
    """Main function - runs automatically without prompts"""
    # Check if auto-scan is enabled (unless forced)
    if len(sys.argv) > 1 and sys.argv[1] == '--force':
        pass  # Force run
    elif not check_auto_config():
        # Silent exit if auto-scan not enabled
        sys.exit(0)
    
    print("🔍 Auto-scanning VoiceCraft project...")
    
    try:
        summary = generate_summary()
        
        # Write summary file
        with open(SUMMARY_FILE, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        print(f"✅ Summary updated: {SUMMARY_FILE}")
        print(f"📊 Files scanned: Python={count_files(PROJECT_ROOT, ['.py'])}, Markdown={count_files(PROJECT_ROOT, ['.md'])}")
        
    except Exception as e:
        print(f"❌ Error during scan: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

