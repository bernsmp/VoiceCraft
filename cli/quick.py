#!/usr/bin/env python3
"""
Quick CLI - Ultra low-friction content creation

Just paste your input and go. Auto-detects everything.
"""

import sys
import os
from pathlib import Path

# Load environment variables from .env.local if it exists
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent / '.env.local'
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    pass  # dotenv not installed, skip

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.workflow_automation import quick_content

def main():
    """Quick content creation - just input and go"""
    
    # Get input from command line or stdin
    if len(sys.argv) > 1:
        # Input from command line arguments
        input_text = " ".join(sys.argv[1:])
    else:
        # Input from stdin (for piping/redirection)
        input_text = sys.stdin.read().strip()
    
    if not input_text:
        print("Usage: quick.py 'your topic or input here'")
        print("   or: echo 'your input' | quick.py")
        sys.exit(1)
    
    # Get profile from env or default
    profile = os.getenv('VOICECRAFT_PROFILE', 'Max Bernstein')
    
    # Generate content (completely automatic)
    try:
        content = quick_content(
            input_text=input_text,
            profile_name=profile,
            auto_yes=True  # Silent mode
        )
        
        # Output content
        print(content)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

