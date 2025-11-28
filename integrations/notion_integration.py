"""
Notion Integration for VoiceCraft

Automatically tracks articles in Notion when generated.
"""

import os
import requests
from typing import Dict, Optional
from datetime import datetime


class NotionIntegration:
    """Integration with Notion for article tracking"""
    
    def __init__(
        self,
        api_token: Optional[str] = None,
        database_id: Optional[str] = None
    ):
        """
        Initialize Notion integration
        
        Args:
            api_token: Notion API token (or from NOTION_API_TOKEN env var)
            database_id: Notion database ID (or from NOTION_DATABASE_ID env var)
        """
        self.api_token = api_token or os.getenv('NOTION_API_TOKEN')
        self.database_id = database_id or os.getenv('NOTION_DATABASE_ID')
        
        if not self.api_token:
            raise ValueError("Notion API token required. Set NOTION_API_TOKEN env var.")
        if not self.database_id:
            raise ValueError("Notion database ID required. Set NOTION_DATABASE_ID env var.")
    
    def create_article_page(
        self,
        title: str,
        topic: str,
        content: str,
        status: str = "Draft",
        word_count: Optional[int] = None,
        platform: str = "Substack",
        notes: Optional[str] = None
    ) -> Dict:
        """
        Create a new article page in Notion database
        
        Args:
            title: Article title
            topic: Original topic/input
            content: Article content (draft)
            status: Status (Draft, Editing, Published)
            word_count: Word count (auto-calculated if not provided)
            platform: Target platform
            notes: Optional notes
            
        Returns:
            Created page data
        """
        if word_count is None:
            word_count = len(content.split())
        
        # Notion API v1 format
        properties = {
            "Title": {
                "title": [{"text": {"content": title}}]
            },
            "Topic": {
                "rich_text": [{"text": {"content": topic[:2000]}}]  # Notion limit
            },
            "Status": {
                "select": {"name": status}
            },
            "Word Count": {
                "number": word_count
            },
            "Platform": {
                "select": {"name": platform}
            },
            "Generated Date": {
                "date": {"start": datetime.now().isoformat()}
            }
        }
        
        # Add notes if provided
        if notes:
            properties["Notes"] = {
                "rich_text": [{"text": {"content": notes[:2000]}}]
            }
        
        # Create page with content
        page_data = {
            "parent": {"database_id": self.database_id},
            "properties": properties,
            "children": [
                {
                    "object": "block",
                    "type": "heading_1",
                    "heading_1": {
                        "rich_text": [{"text": {"content": "Draft Content"}}]
                    }
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": self._split_text_to_rich_text(content)
                    }
                }
            ]
        }
        
        url = "https://api.notion.com/v1/pages"
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        
        try:
            response = requests.post(url, json=page_data, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"⚠️  Notion integration error: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"   Response: {e.response.text}")
            return {"success": False, "error": str(e)}
    
    def _split_text_to_rich_text(self, text: str, max_length: int = 2000) -> list:
        """
        Split text into Notion rich_text blocks (2000 char limit per block)
        """
        blocks = []
        # Split by paragraphs first
        paragraphs = text.split('\n\n')
        
        current_block = ""
        for para in paragraphs:
            if len(current_block) + len(para) + 2 > max_length:
                if current_block:
                    blocks.append({"text": {"content": current_block.strip()}})
                current_block = para
            else:
                if current_block:
                    current_block += "\n\n" + para
                else:
                    current_block = para
        
        if current_block:
            blocks.append({"text": {"content": current_block.strip()}})
        
        return blocks if blocks else [{"text": {"content": text[:2000]}}]
    
    def update_article_status(
        self,
        page_id: str,
        status: str,
        edited_content: Optional[str] = None,
        final_content: Optional[str] = None,
        publish_url: Optional[str] = None
    ) -> Dict:
        """
        Update article status and content
        
        Args:
            page_id: Notion page ID
            status: New status (Draft, Editing, Published)
            edited_content: Edited version (if status = Editing)
            final_content: Final version (if status = Published)
            publish_url: Published URL (if status = Published)
            
        Returns:
            Updated page data
        """
        properties = {"Status": {"select": {"name": status}}}
        
        if publish_url:
            properties["Published Date"] = {"date": {"start": datetime.now().isoformat()}}
            properties["Publish URL"] = {"url": publish_url}
        
        url = f"https://api.notion.com/v1/pages/{page_id}"
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        
        payload = {"properties": properties}
        
        try:
            response = requests.patch(url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            
            # If we have edited/final content, append to page
            if edited_content or final_content:
                self._append_content_to_page(page_id, edited_content or final_content)
            
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"⚠️  Notion update error: {e}")
            return {"success": False, "error": str(e)}
    
    def _append_content_to_page(self, page_id: str, content: str):
        """Append content blocks to existing Notion page"""
        url = f"https://api.notion.com/v1/blocks/{page_id}/children"
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        
        children = [
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"text": {"content": "Edited Content"}}]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": self._split_text_to_rich_text(content)
                }
            }
        ]
        
        try:
            requests.patch(url, json={"children": children}, headers=headers, timeout=10)
        except Exception as e:
            print(f"⚠️  Failed to append content: {e}")


def save_to_notion(
    title: str,
    topic: str,
    content: str,
    **kwargs
) -> Optional[Dict]:
    """
    Convenience function to save article to Notion
    
    Usage:
        save_to_notion(
            title="My Article",
            topic="AI expertise",
            content="Article content here..."
        )
    """
    try:
        integration = NotionIntegration()
        return integration.create_article_page(
            title=title,
            topic=topic,
            content=content,
            **kwargs
        )
    except ValueError as e:
        # Missing config - silently skip
        return None
    except Exception as e:
        print(f"⚠️  Notion save failed: {e}")
        return None

