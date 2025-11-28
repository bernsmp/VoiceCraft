"""
AITable CMS Adapter for VoiceCraft Website Editing

Provides an adapter to read/write site settings to AITable.ai instead of Payload CMS.
This allows using AITable's simpler API and UI while maintaining compatibility with
the existing WebsiteEditor command interface.

Usage:
    from integrations.cms_aitable_adapter import AITableCMSAdapter

    adapter = AITableCMSAdapter(
        api_token=os.getenv('AITABLE_API_KEY'),
        base_id=os.getenv('AITABLE_BASE_ID'),
        datasheet_id=os.getenv('AITABLE_DATASHEET_ID')  # site-settings table
    )

    # Read settings
    settings = adapter.get_site_settings()

    # Update a field
    adapter.update_site_settings({'hero': {'headline': 'New Headline'}})
"""

import os
import requests
from typing import Dict, Any, Optional


class AITableCMSAdapter:
    """
    Adapter for AITable.ai to store website settings as structured data.

    AITable schema assumption (datasheet with columns):
    - section (text): e.g. 'hero', 'credentials', 'about'
    - field (text): e.g. 'headline', 'tagline'
    - value (text or long text): the content
    - record_id (auto): AITable primary key

    For arrays/objects, store JSON-encoded string in value column or use
    linked records if needed. For MVP, flatten to key-value pairs.
    """

    def __init__(
        self,
        api_token: Optional[str] = None,
        base_id: Optional[str] = None,
        datasheet_id: Optional[str] = None,
        base_url: str = "https://aitable.ai/fusion/v1"
    ):
        """
        Initialize AITable adapter.

        Args:
            api_token: AITable API key (or from AITABLE_API_KEY env)
            base_id: AITable space/base ID (or from AITABLE_BASE_ID env)
            datasheet_id: Datasheet ID for site-settings (or from AITABLE_DATASHEET_ID env)
            base_url: AITable Fusion API base URL
        """
        self.api_token = api_token or os.getenv('AITABLE_API_KEY')
        self.base_id = base_id or os.getenv('AITABLE_BASE_ID')
        self.datasheet_id = datasheet_id or os.getenv('AITABLE_DATASHEET_ID')
        self.base_url = base_url

        if not self.api_token:
            raise ValueError("AITable API token required (set AITABLE_API_KEY)")
        if not self.base_id:
            raise ValueError("AITable base ID required (set AITABLE_BASE_ID)")
        if not self.datasheet_id:
            raise ValueError("AITable datasheet ID required (set AITABLE_DATASHEET_ID)")

    def _headers(self) -> Dict[str, str]:
        """Build request headers with API token"""
        return {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json'
        }

    def get_site_settings(self) -> Dict[str, Any]:
        """
        Fetch all site settings from AITable and reconstruct nested structure.

        Returns:
            Dictionary matching Payload CMS site-settings shape (hero, credentials, etc.)
        """
        url = f"{self.base_url}/spaces/{self.base_id}/datasheets/{self.datasheet_id}/records"
        
        try:
            response = requests.get(url, headers=self._headers(), params={'pageSize': 500})
            response.raise_for_status()
            data = response.json()

            # Reconstruct nested dict from flat key-value records
            settings: Dict[str, Any] = {}
            for record in data.get('data', {}).get('records', []):
                fields = record.get('fields', {})
                section = fields.get('section', '')
                field = fields.get('field', '')
                value = fields.get('value')
                
                if section and field:
                    if section not in settings:
                        settings[section] = {}
                    settings[section][field] = value

            return settings
        except requests.RequestException as e:
            print(f"⚠️  AITable fetch failed: {e}")
            return {}

    def update_site_settings(self, updates: Dict[str, Any]) -> bool:
        """
        Update site settings by upserting records in AITable.

        Args:
            updates: Nested dict with structure like {'hero': {'headline': 'New'}}

        Returns:
            True if successful, False otherwise
        """
        url = f"{self.base_url}/spaces/{self.base_id}/datasheets/{self.datasheet_id}/records"

        try:
            # Flatten updates to section.field -> value mapping
            flat_updates = self._flatten_dict(updates)

            # For each key, upsert or patch existing record
            # (For MVP, we assume manual setup of records in AITable; production would use batch upsert)
            for key, value in flat_updates.items():
                section, field = key.split('.', 1) if '.' in key else (key, '')
                if not field:
                    continue

                # Check if record exists (simplified: query all, match locally)
                current = self.get_site_settings()
                record_id = self._find_record_id(section, field, current)

                if record_id:
                    # Update existing
                    patch_url = f"{url}/{record_id}"
                    payload = {'fields': {'value': value}}
                    response = requests.patch(patch_url, json=payload, headers=self._headers())
                    response.raise_for_status()
                else:
                    # Create new
                    payload = {'records': [{'fields': {'section': section, 'field': field, 'value': value}}]}
                    response = requests.post(url, json=payload, headers=self._headers())
                    response.raise_for_status()

            return True
        except requests.RequestException as e:
            print(f"⚠️  AITable update failed: {e}")
            return False

    def _flatten_dict(self, d: Dict[str, Any], parent_key: str = '') -> Dict[str, str]:
        """Recursively flatten nested dict to dot-notation keys"""
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}.{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key).items())
            else:
                items.append((new_key, str(v)))
        return dict(items)

    def _find_record_id(self, section: str, field: str, current: Dict[str, Any]) -> Optional[str]:
        """
        Find the AITable record ID for a given section.field (if it exists in current data).
        
        Note: This is a simplified approach. In production, maintain a record ID cache or
        use AITable query filters.
        """
        # For MVP, return None (always create). Extend with a local cache or query by filter.
        return None


# Feature flag: use AITable instead of Payload for website edits
USE_AITABLE_CMS = os.getenv('USE_AITABLE_CMS', 'false').lower() == 'true'


def get_cms_adapter():
    """
    Factory function to return the appropriate CMS adapter (Payload or AITable).

    Returns:
        PayloadCMSClient or AITableCMSAdapter depending on USE_AITABLE_CMS env flag.
    """
    if USE_AITABLE_CMS:
        return AITableCMSAdapter()
    else:
        from integrations.cms_integration import PayloadCMSClient, WEBSITES
        config = WEBSITES.get('louie')
        if not config:
            raise ValueError("Louie website config not found in cms_integration")
        return PayloadCMSClient(config)
