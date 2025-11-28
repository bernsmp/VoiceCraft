#!/usr/bin/env python3
"""
Quick script to help you extract Substack metrics from dashboard

Since Substack doesn't have a public API, you can manually input metrics
or export from dashboard and convert to JSON.
"""

import json
from pathlib import Path

# Example: Add your metrics here based on what you see in the dashboard
# Format: article_url -> metrics
SUBSTACK_METRICS = {
    # Add your articles here
    # Example:
    # "https://irreplaceablepositioning.substack.com/p/article-slug": {
    #     "views": 1260,
    #     "opened": 35,  # percentage
    #     "subs": 4,  # new subscribers
    #     "likes": 0,  # if visible
    #     "comments": 0,  # if visible
    #     "shares": 0  # if visible
    # }
}

def create_metrics_template():
    """Create a template JSON file for metrics"""
    template = {
        "instructions": "Add your Substack article metrics here",
        "format": {
            "article_url": {
                "views": 0,
                "opened": 0,
                "subs": 0,
                "likes": 0,
                "comments": 0,
                "shares": 0
            }
        },
        "examples": {
            "https://irreplaceablepositioning.substack.com/p/example-1": {
                "views": 1260,
                "opened": 35,
                "subs": 4,
                "likes": 0,
                "comments": 0,
                "shares": 0
            }
        }
    }
    
    output_file = Path("./data/substack_engagement.json")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(template, f, indent=2)
    
    print(f"✅ Created template: {output_file}")
    print("\nNext steps:")
    print("1. Open the file and add your article metrics")
    print("2. Get article URLs from your Substack dashboard")
    print("3. Add metrics for each article")
    print("4. Run: python3 scripts/analyze_substack_performance.py")

if __name__ == "__main__":
    create_metrics_template()

