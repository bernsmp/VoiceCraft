"""
AITable.ai Integration for VoiceCraft

Automatically tracks articles in AITable when generated.
"""

import os
import requests
from typing import Dict, Optional
from datetime import datetime
from pathlib import Path


class AITableIntegration:
    """Integration with AITable.ai for article tracking"""
    
    def __init__(
        self,
        api_token: Optional[str] = None,
        base_url: Optional[str] = None,
        database_id: Optional[str] = None,
        table_id: Optional[str] = None
    ):
        """
        Initialize AITable integration
        
        Args:
            api_token: AITable API token (or from AITABLE_API_TOKEN env var)
            base_url: AITable base URL (or from AITABLE_BASE_URL env var)
            database_id: Database ID (or from AITABLE_DATABASE_ID env var)
            table_id: Table ID (or from AITABLE_TABLE_ID env var)
        """
        self.api_token = api_token or os.getenv('AITABLE_API_TOKEN')
        self.base_url = base_url or os.getenv('AITABLE_BASE_URL', 'https://aitable.ai/api/v1')
        self.database_id = database_id or os.getenv('AITABLE_DATABASE_ID')
        self.table_id = table_id or os.getenv('AITABLE_TABLE_ID')
        
        if not self.api_token:
            raise ValueError("AITable API token required. Set AITABLE_API_TOKEN env var.")
        if not self.database_id:
            raise ValueError("AITable database ID required. Set AITABLE_DATABASE_ID env var.")
        if not self.table_id:
            raise ValueError("AITable table ID required. Set AITABLE_TABLE_ID env var.")
    
    def create_article_record(
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
        Create a new article record in AITable
        
        Args:
            title: Article title
            topic: Original topic/input
            content: Article content (draft)
            status: Status (Draft, Editing, Published)
            word_count: Word count (auto-calculated if not provided)
            platform: Target platform
            notes: Optional notes
            
        Returns:
            Created record data
        """
        if word_count is None:
            word_count = len(content.split())
        
        payload = {
            "fields": {
                "title": title,
                "topic": topic,
                "status": status,
                "draft_content": content,
                "word_count": word_count,
                "generated_date": datetime.now().isoformat(),
                "platform": platform
            }
        }
        
        if notes:
            payload["fields"]["notes"] = notes
        
        url = f"{self.base_url}/databases/{self.database_id}/tables/{self.table_id}/records"
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"⚠️  AITable integration error: {e}")
            return {"success": False, "error": str(e)}
    
    def update_article_status(
        self,
        record_id: str,
        status: str,
        edited_content: Optional[str] = None,
        final_content: Optional[str] = None,
        publish_url: Optional[str] = None
    ) -> Dict:
        """
        Update article status and content
        
        Args:
            record_id: AITable record ID
            status: New status (Draft, Editing, Published)
            edited_content: Edited version (if status = Editing)
            final_content: Final version (if status = Published)
            publish_url: Published URL (if status = Published)
            
        Returns:
            Updated record data
        """
        fields = {"status": status}
        
        if edited_content:
            fields["edited_content"] = edited_content
        
        if final_content:
            fields["final_content"] = final_content
        
        if publish_url:
            fields["publish_url"] = publish_url
            fields["published_date"] = datetime.now().isoformat()
        
        url = f"{self.base_url}/databases/{self.database_id}/tables/{self.table_id}/records/{record_id}"
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
        
        payload = {"fields": fields}
        
        try:
            response = requests.patch(url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"⚠️  AITable update error: {e}")
            return {"success": False, "error": str(e)}
    
    def get_draft_articles(self) -> list:
        """Get all articles with status = Draft"""
        url = f"{self.base_url}/databases/{self.database_id}/tables/{self.table_id}/records"
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
        params = {
            "filter": '{"status": "Draft"}'
        }
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            return response.json().get("data", [])
        except requests.exceptions.RequestException as e:
            print(f"⚠️  AITable fetch error: {e}")
            return []


def save_to_aitable(
    title: str,
    topic: str,
    content: str,
    **kwargs
) -> Optional[Dict]:
    """
    Convenience function to save article to AITable
    
    Usage:
        save_to_aitable(
            title="My Article",
            topic="AI expertise",
            content="Article content here..."
        )
    """
    try:
        integration = AITableIntegration()
        return integration.create_article_record(
            title=title,
            topic=topic,
            content=content,
            **kwargs
        )
    except ValueError as e:
        # Missing config - silently skip
        return None
    except Exception as e:
        print(f"⚠️  AITable save failed: {e}")
        return None

