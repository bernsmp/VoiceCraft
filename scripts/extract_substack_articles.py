#!/usr/bin/env python3
"""
Extract articles from Substack for voice analysis

This script helps collect your Substack articles for voice profiling.
"""

import requests
import json
import os
from pathlib import Path
from typing import List, Dict
import time

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Installing beautifulsoup4...")
    os.system(f"pip3 install beautifulsoup4")
    from bs4 import BeautifulSoup


class SubstackExtractor:
    """Extract articles from Substack newsletter"""
    
    def __init__(self, substack_url: str, output_dir: str = "./data/samples"):
        self.substack_url = substack_url.rstrip('/')
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def extract_article_urls(self) -> List[str]:
        """
        Extract article URLs from Substack archive page.
        
        Note: Substack doesn't have a public API, so this uses web scraping.
        You may need to manually provide article URLs or export content.
        """
        # Substack archive URL format
        archive_url = f"{self.substack_url}/archive"
        
        try:
            response = requests.get(archive_url, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            })
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find article links (Substack structure may vary)
            article_links = []
            for link in soup.find_all('a', href=True):
                href = link.get('href')
                if href and '/p/' in href:  # Substack post URLs contain /p/
                    full_url = href if href.startswith('http') else f"{self.substack_url}{href}"
                    if full_url not in article_links:
                        article_links.append(full_url)
            
            return article_links
        
        except Exception as e:
            print(f"Error extracting URLs: {e}")
            print("\nAlternative: Manually provide article URLs or export content.")
            return []
    
    def extract_article_content(self, article_url: str) -> Dict:
        """Extract content from a single article URL"""
        try:
            response = requests.get(article_url, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            })
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title_elem = soup.find('h1') or soup.find('title')
            title = title_elem.get_text().strip() if title_elem else "Untitled"
            
            # Extract content (Substack uses specific classes)
            content_elem = soup.find('div', class_='post') or soup.find('article')
            if not content_elem:
                # Try alternative selectors
                content_elem = soup.find('div', {'data-testid': 'post-content'})
            
            if content_elem:
                # Remove scripts, styles, etc.
                for script in content_elem(["script", "style", "nav", "footer", "header"]):
                    script.decompose()
                
                # Get text content
                content = content_elem.get_text(separator='\n\n', strip=True)
            else:
                content = soup.get_text()
            
            return {
                "title": title,
                "url": article_url,
                "content": content,
                "word_count": len(content.split())
            }
        
        except Exception as e:
            print(f"Error extracting {article_url}: {e}")
            return None
    
    def save_articles(self, articles: List[Dict], prefix: str = "article"):
        """Save extracted articles to files"""
        saved_files = []
        
        for i, article in enumerate(articles, 1):
            if not article:
                continue
            
            filename = f"{prefix}_{i:03d}_{article['title'][:50].replace('/', '_')}.md"
            filepath = self.output_dir / filename
            
            # Create markdown file
            content = f"""# {article['title']}

**Source:** {article['url']}
**Word Count:** {article['word_count']}

---

{article['content']}
"""
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            saved_files.append(str(filepath))
            print(f"✓ Saved: {filename}")
        
        return saved_files
    
    def extract_all(self, max_articles: int = 10) -> List[str]:
        """
        Extract all articles and save them.
        
        Returns list of saved file paths.
        """
        print(f"Extracting articles from: {self.substack_url}\n")
        
        # Get article URLs
        print("Finding article URLs...")
        article_urls = self.extract_article_urls()
        
        if not article_urls:
            print("\n⚠️  Could not automatically extract URLs.")
            print("\nAlternative methods:")
            print("1. Manually provide article URLs")
            print("2. Export content from Substack dashboard")
            print("3. Copy/paste articles into files")
            return []
        
        print(f"Found {len(article_urls)} articles")
        
        # Limit if requested
        if max_articles:
            article_urls = article_urls[:max_articles]
            print(f"Extracting first {len(article_urls)} articles...\n")
        
        # Extract content
        articles = []
        for url in article_urls:
            print(f"Extracting: {url}")
            article = self.extract_article_content(url)
            if article:
                articles.append(article)
            time.sleep(1)  # Be respectful
        
        # Save articles
        print(f"\nSaving {len(articles)} articles...")
        saved_files = self.save_articles(articles)
        
        print(f"\n✅ Successfully extracted {len(saved_files)} articles!")
        print(f"Files saved to: {self.output_dir}")
        
        return saved_files


def main():
    """Main function for CLI usage"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python3 extract_substack_articles.py <substack_url> [max_articles]")
        print("\nExample:")
        print("  python3 extract_substack_articles.py https://irreplaceablepositioning.substack.com 10")
        sys.exit(1)
    
    substack_url = sys.argv[1]
    max_articles = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    
    extractor = SubstackExtractor(substack_url)
    saved_files = extractor.extract_all(max_articles=max_articles)
    
    if saved_files:
        print("\n" + "="*60)
        print("Next steps:")
        print("="*60)
        print(f"\n1. Review articles in: {extractor.output_dir}")
        print("\n2. Create voice profile:")
        print(f"   voicecraft profile create-deep \\")
        print(f"     --name 'Max Bernstein' \\")
        print(f"     --samples '{extractor.output_dir}/*.md' \\")
        print(f"     --use-llm-analysis")
        print("\n3. Or use Python directly:")
        print("   from core.llm_voice_analyzer import LLMVoiceAnalyzer")
        print("   analyzer = LLMVoiceAnalyzer()")
        print("   # ... create profile")


if __name__ == "__main__":
    main()

