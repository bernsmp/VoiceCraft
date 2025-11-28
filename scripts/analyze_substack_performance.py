#!/usr/bin/env python3
"""
Analyze Substack Articles for Performance

Identifies most popular/engaging articles and analyzes why they worked.
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
import re

try:
    from openai import OpenAI
    from anthropic import Anthropic
except ImportError:
    OpenAI = None
    Anthropic = None


class SubstackAnalyzer:
    """Analyze Substack articles for performance patterns"""
    
    def __init__(
        self,
        articles_dir: str = "./data/samples",
        openai_api_key: Optional[str] = None,
        anthropic_api_key: Optional[str] = None
    ):
        self.articles_dir = Path(articles_dir)
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.anthropic_api_key = anthropic_api_key or os.getenv("ANTHROPIC_API_KEY")
        
        # Initialize AI clients
        if OpenAI and self.openai_api_key:
            self.openai_client = OpenAI(api_key=self.openai_api_key)
        else:
            self.openai_client = None
        
        if Anthropic and self.anthropic_api_key:
            self.anthropic_client = Anthropic(api_key=self.anthropic_api_key)
        else:
            self.anthropic_client = None
    
    def load_articles(self) -> List[Dict]:
        """Load all articles from directory"""
        articles = []
        
        if not self.articles_dir.exists():
            print(f"⚠️  Directory not found: {self.articles_dir}")
            return articles
        
        for file_path in sorted(self.articles_dir.glob("*.md")):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Parse article
                article = self._parse_article(file_path, content)
                if article:
                    articles.append(article)
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
        
        return articles
    
    def _parse_article(self, file_path: Path, content: str) -> Optional[Dict]:
        """Parse article from markdown content"""
        lines = content.split('\n')
        
        # Extract title (first # heading)
        title = None
        url = None
        word_count = 0
        
        for i, line in enumerate(lines):
            if line.startswith('# ') and not title:
                title = line[2:].strip()
            elif line.startswith('**Source:**'):
                url = line.replace('**Source:**', '').strip()
            elif line.startswith('**Word Count:**'):
                try:
                    word_count = int(line.replace('**Word Count:**', '').strip())
                except:
                    pass
        
        # Get actual content (after metadata)
        content_start = 0
        for i, line in enumerate(lines):
            if line.strip() == '---':
                content_start = i + 1
                break
        
        article_content = '\n'.join(lines[content_start:])
        
        if not title:
            title = file_path.stem
        
        if not word_count:
            word_count = len(article_content.split())
        
        return {
            "title": title,
            "url": url or str(file_path),
            "content": article_content,
            "word_count": word_count,
            "file_path": str(file_path),
            "first_paragraph": self._get_first_paragraph(article_content),
            "hook": self._extract_hook(article_content),
            "structure": self._analyze_structure(article_content)
        }
    
    def _get_first_paragraph(self, content: str) -> str:
        """Get first paragraph"""
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        return paragraphs[0] if paragraphs else ""
    
    def _extract_hook(self, content: str) -> str:
        """Extract opening hook (first 3 sentences)"""
        sentences = re.split(r'[.!?]+', content)
        first_3 = ' '.join([s.strip() for s in sentences[:3] if s.strip()])
        return first_3[:300]  # Limit length
    
    def _analyze_structure(self, content: str) -> Dict:
        """Analyze article structure"""
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        
        # Count headings
        headings = [line for line in content.split('\n') if line.startswith('#')]
        
        # Count lists
        list_items = [line for line in content.split('\n') if line.strip().startswith(('-', '*', '1.', '2.'))]
        
        return {
            "paragraph_count": len(paragraphs),
            "heading_count": len(headings),
            "list_count": len(list_items),
            "avg_paragraph_length": sum(len(p.split()) for p in paragraphs) / len(paragraphs) if paragraphs else 0
        }
    
    def get_engagement_data(self, articles: List[Dict]) -> List[Dict]:
        """
        Get engagement data for articles.
        
        Note: Substack doesn't have a public API for engagement metrics.
        Options:
        1. Manually input engagement data (CSV/JSON)
        2. Scrape from Substack dashboard (requires auth)
        3. Use estimated metrics based on content analysis
        """
        print("\n📊 Getting engagement data...")
        print("⚠️  Substack doesn't provide public engagement API.")
        print("\nOptions:")
        print("1. Manually provide engagement data (see load_engagement_from_file)")
        print("2. Use content analysis to estimate performance")
        print("3. Scrape from Substack dashboard (requires authentication)\n")
        
        # For now, use content analysis to estimate
        return self._estimate_engagement(articles)
    
    def _estimate_engagement(self, articles: List[Dict]) -> List[Dict]:
        """Estimate engagement based on content analysis"""
        print("Analyzing content to estimate engagement potential...")
        
        for article in articles:
            score = 0
            
            # Hook quality (first paragraph)
            hook = article.get("hook", "")
            if len(hook) > 50 and len(hook) < 200:
                score += 20  # Good hook length
            if any(word in hook.lower() for word in ['you', 'your', 'why', 'how', 'what']):
                score += 15  # Direct address
            
            # Structure
            structure = article.get("structure", {})
            if 5 <= structure.get("paragraph_count", 0) <= 20:
                score += 15  # Good length
            if structure.get("heading_count", 0) > 0:
                score += 10  # Has headings
            if structure.get("list_count", 0) > 0:
                score += 10  # Has lists
            
            # Content signals
            content_lower = article.get("content", "").lower()
            if any(phrase in content_lower for phrase in ['example', 'story', 'case study']):
                score += 10  # Has examples
            if '?' in article.get("content", ""):
                score += 10  # Has questions (engagement)
            if any(word in content_lower for word in ['insight', 'pattern', 'framework', 'strategy']):
                score += 10  # Value keywords
            
            article["estimated_engagement_score"] = score
        
        return articles
    
    def load_engagement_from_file(self, file_path: str) -> Dict[str, Dict]:
        """
        Load engagement data from CSV or JSON file.
        
        CSV format:
        url,views,likes,comments,shares
        
        JSON format:
        {
          "article_url": {
            "views": 1000,
            "likes": 50,
            "comments": 10,
            "shares": 5
          }
        }
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            print(f"⚠️  File not found: {file_path}")
            return {}
        
        engagement_data = {}
        
        if file_path.suffix == '.csv':
            import csv
            with open(file_path, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    url = row.get('url', '')
                    engagement_data[url] = {
                        "views": int(row.get('views', 0)),
                        "likes": int(row.get('likes', 0)),
                        "comments": int(row.get('comments', 0)),
                        "shares": int(row.get('shares', 0))
                    }
        elif file_path.suffix == '.json':
            with open(file_path, 'r') as f:
                engagement_data = json.load(f)
        
        return engagement_data
    
    def rank_articles(self, articles: List[Dict], engagement_data: Optional[Dict] = None) -> List[Dict]:
        """Rank articles by engagement"""
        if engagement_data:
            # Use real engagement data
            for article in articles:
                url = article.get("url", "")
                metrics = engagement_data.get(url, {})
                article["views"] = metrics.get("views", 0)
                article["likes"] = metrics.get("likes", 0)
                article["comments"] = metrics.get("comments", 0)
                article["shares"] = metrics.get("shares", 0)
                article["total_engagement"] = (
                    article["views"] * 0.1 +
                    article["likes"] * 10 +
                    article["comments"] * 20 +
                    article["shares"] * 30
                )
        else:
            # Use estimated scores
            for article in articles:
                article["total_engagement"] = article.get("estimated_engagement_score", 0)
        
        # Sort by engagement
        ranked = sorted(articles, key=lambda x: x.get("total_engagement", 0), reverse=True)
        
        return ranked
    
    def analyze_top_performers(
        self,
        top_articles: List[Dict],
        num_to_analyze: int = 5
    ) -> Dict:
        """Analyze why top articles performed well"""
        if not self.anthropic_client:
            print("⚠️  Anthropic API key not set. Skipping deep analysis.")
            return {}
        
        print(f"\n🔍 Analyzing top {num_to_analyze} performers...")
        
        # Prepare analysis prompt
        articles_text = ""
        for i, article in enumerate(top_articles[:num_to_analyze], 1):
            articles_text += f"""
## Article {i}: {article['title']}
URL: {article.get('url', 'N/A')}
Engagement Score: {article.get('total_engagement', 0):.1f}
Word Count: {article.get('word_count', 0)}
Hook: {article.get('hook', '')[:200]}...
Structure: {article.get('structure', {})}
"""
        
        prompt = f"""
Analyze these top-performing Substack articles and identify why they worked so well.

{articles_text}

Provide analysis on:
1. **Hook Patterns** - What makes the openings effective?
2. **Structure Patterns** - How are they organized?
3. **Content Elements** - What types of content appear?
4. **Engagement Triggers** - What drives interaction?
5. **Voice/Tone** - How do they communicate?
6. **Key Takeaways** - What patterns should be replicated?

Be specific and actionable.
"""
        
        try:
            # Use the same model as workflow automation
            message = self.anthropic_client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=2000,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            analysis = message.content[0].text
            
            return {
                "analysis": analysis,
                "top_articles": top_articles[:num_to_analyze]
            }
        
        except Exception as e:
            print(f"Error analyzing: {e}")
            return {}
    
    def generate_report(
        self,
        ranked_articles: List[Dict],
        analysis: Optional[Dict] = None,
        output_file: str = "./data/substack_analysis_report.md"
    ):
        """Generate analysis report"""
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        report = f"""# Substack Article Performance Analysis

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Total Articles Analyzed:** {len(ranked_articles)}

---

## 📊 Top 10 Performing Articles

"""
        
        for i, article in enumerate(ranked_articles[:10], 1):
            engagement = article.get("total_engagement", 0)
            views = article.get("views", "N/A")
            likes = article.get("likes", "N/A")
            
            report += f"""
### {i}. {article['title']}

- **Engagement Score:** {engagement:.1f}
- **Views:** {views} | **Likes:** {likes}
- **Word Count:** {article.get('word_count', 0)}
- **URL:** {article.get('url', 'N/A')}

**Hook:**
> {article.get('hook', '')[:200]}...

**Structure:**
- Paragraphs: {article.get('structure', {}).get('paragraph_count', 0)}
- Headings: {article.get('structure', {}).get('heading_count', 0)}
- Lists: {article.get('structure', {}).get('list_count', 0)}

---
"""
        
        if analysis:
            report += f"""
## 🔍 Why Top Articles Worked

{analysis.get('analysis', 'Analysis not available')}

---

## 📈 Patterns Identified

Based on analysis of top performers, here are the key patterns to replicate:

1. **Hook Patterns:** [See analysis above]
2. **Structure:** [See analysis above]
3. **Content Elements:** [See analysis above]
4. **Engagement Triggers:** [See analysis above]

---
"""
        
        report += f"""
## 📋 Full Ranking

"""
        
        for i, article in enumerate(ranked_articles, 1):
            engagement = article.get("total_engagement", 0)
            report += f"{i}. {article['title']} - Score: {engagement:.1f}\n"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n✅ Report saved to: {output_path}")
        return output_path


def main():
    """Main function"""
    import sys
    
    analyzer = SubstackAnalyzer()
    
    # Load articles
    print("📚 Loading articles...")
    articles = analyzer.load_articles()
    
    if not articles:
        print("❌ No articles found!")
        print(f"   Make sure articles are in: {analyzer.articles_dir}")
        print("\n   To extract articles:")
        print("   python3 scripts/extract_substack_articles.py <substack_url>")
        sys.exit(1)
    
    print(f"✅ Loaded {len(articles)} articles")
    
    # Get engagement data
    engagement_data = None
    
    # Check for engagement file
    engagement_file = Path("./data/substack_engagement.json")
    if engagement_file.exists():
        print(f"\n📊 Loading engagement data from {engagement_file}...")
        engagement_data = analyzer.load_engagement_from_file(str(engagement_file))
        print(f"✅ Loaded engagement data for {len(engagement_data)} articles")
    else:
        print("\n💡 Tip: Create data/substack_engagement.json with engagement metrics")
        print("   Format: {\"article_url\": {\"views\": 1000, \"likes\": 50, ...}}")
    
    # Get engagement scores
    articles_with_engagement = analyzer.get_engagement_data(articles)
    
    # Merge real engagement data if available
    if engagement_data:
        for article in articles_with_engagement:
            url = article.get("url", "")
            if url in engagement_data:
                article.update(engagement_data[url])
    
    # Rank articles
    print("\n🏆 Ranking articles...")
    ranked = analyzer.rank_articles(articles_with_engagement, engagement_data)
    
    # Analyze top performers
    analysis = analyzer.analyze_top_performers(ranked, num_to_analyze=5)
    
    # Generate report
    print("\n📄 Generating report...")
    report_path = analyzer.generate_report(ranked, analysis)
    
    print(f"\n✅ Analysis complete!")
    print(f"   Report: {report_path}")
    print(f"\n   Top 3 Articles:")
    for i, article in enumerate(ranked[:3], 1):
        print(f"   {i}. {article['title']} (Score: {article.get('total_engagement', 0):.1f})")


if __name__ == "__main__":
    main()

