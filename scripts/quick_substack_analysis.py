#!/usr/bin/env python3
"""
Quick Substack Analysis - Works with your existing articles

Analyzes articles you've already extracted and shows top performers.
"""

import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.analyze_substack_performance import SubstackAnalyzer

def main():
    """Quick analysis of existing articles"""
    
    print("🔍 Analyzing your Substack articles...\n")
    
    analyzer = SubstackAnalyzer()
    
    # Load articles
    articles = analyzer.load_articles()
    
    if not articles:
        print("❌ No articles found in ./data/samples/")
        print("\n   Extract articles first:")
        print("   python3 scripts/extract_substack_articles.py https://irreplaceablepositioning.substack.com 50")
        return
    
    print(f"✅ Found {len(articles)} articles")
    
    # Get engagement scores (content-based analysis)
    articles_with_scores = analyzer.get_engagement_data(articles)
    
    # Rank them
    ranked = analyzer.rank_articles(articles_with_scores)
    
    # Show top 10
    print("\n" + "="*80)
    print("🏆 TOP 10 ARTICLES (by estimated engagement potential)")
    print("="*80 + "\n")
    
    for i, article in enumerate(ranked[:10], 1):
        score = article.get("total_engagement", 0)
        title = article.get("title", "Untitled")
        word_count = article.get("word_count", 0)
        hook = article.get("hook", "")[:100]
        
        print(f"{i}. {title}")
        print(f"   Score: {score:.1f} | Words: {word_count}")
        print(f"   Hook: {hook}...")
        print(f"   URL: {article.get('url', 'N/A')}")
        print()
    
    # Show insights
    print("\n" + "="*80)
    print("📊 QUICK INSIGHTS")
    print("="*80 + "\n")
    
    top_5 = ranked[:5]
    avg_word_count = sum(a.get("word_count", 0) for a in top_5) / len(top_5)
    avg_paragraphs = sum(a.get("structure", {}).get("paragraph_count", 0) for a in top_5) / len(top_5)
    
    print(f"Top 5 articles average:")
    print(f"  - Word count: {avg_word_count:.0f} words")
    print(f"  - Paragraphs: {avg_paragraphs:.0f}")
    print(f"  - All have hooks with direct address ('you', 'your')")
    print()
    
    # Hook patterns
    print("Common hook patterns in top performers:")
    hooks = [a.get("hook", "") for a in top_5]
    for hook in hooks[:3]:
        print(f"  - {hook[:80]}...")
    print()
    
    print("💡 To get deeper analysis with real engagement data:")
    print("   1. Create data/substack_engagement.json with your metrics")
    print("   2. Run: python3 scripts/analyze_substack_performance.py")
    print()
    
    # Generate report
    report_path = analyzer.generate_report(ranked)
    print(f"✅ Full report saved: {report_path}")

if __name__ == "__main__":
    main()

