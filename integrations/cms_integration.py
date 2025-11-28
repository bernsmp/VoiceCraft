"""
CMS Integration - Connect VoiceCraft to Payload CMS

Allows editing website content through natural language commands.
Works with Slack bot or direct API calls.
"""

import os
import json
import requests
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class CMSConfig:
    """Configuration for a CMS-enabled website"""
    name: str
    base_url: str
    api_path: str = "/api"
    admin_email: str = ""
    admin_password: str = ""
    
    @property
    def api_url(self):
        return f"{self.base_url}{self.api_path}"


# Pre-configured websites
WEBSITES = {
    "louie": CMSConfig(
        name="Louie Bernstein",
        base_url=os.getenv("LOUIE_SITE_URL", "https://louiebernstein.com"),
        admin_email=os.getenv("LOUIE_ADMIN_EMAIL", "louis30092@gmail.com"),
        admin_password=os.getenv("LOUIE_ADMIN_PASSWORD", ""),
    ),
}


class PayloadCMSClient:
    """
    Client for interacting with Payload CMS API with token caching and refresh.
    """
    
    def __init__(self, config: CMSConfig):
        self.config = config
        self.token: Optional[str] = None
        self.token_expiry: Optional[float] = None  # Unix timestamp
        self._max_retries = 3
        self._backoff_factor = 0.5
    
    def login(self) -> bool:
        """Authenticate with the CMS"""
        try:
            response = requests.post(
                f"{self.config.api_url}/users/login",
                json={
                    "email": self.config.admin_email,
                    "password": self.config.admin_password,
                },
                headers={"Content-Type": "application/json"},
                timeout=10,
            )
            
            if response.ok:
                data = response.json()
                self.token = data.get("token")
                # Payload JWT typically expires in 7 days; set expiry conservatively
                import time
                self.token_expiry = time.time() + (6 * 24 * 3600)  # 6 days
                return True
            else:
                print(f"Login failed: {response.status_code} {response.text}")
            return False
        except requests.RequestException as e:
            print(f"Login request failed: {e}")
            return False
    
    def _ensure_valid_token(self) -> bool:
        """Ensure token is valid; refresh if expired"""
        import time
        if not self.token or (self.token_expiry and time.time() >= self.token_expiry):
            print("🔄 Token expired or missing, refreshing...")
            return self.login()
        return True
    
    def _headers(self) -> Dict[str, str]:
        """Get request headers with auth token"""
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"JWT {self.token}"
        return headers
    
    def _request_with_retry(self, method: str, url: str, **kwargs) -> requests.Response:
        """Make HTTP request with exponential backoff retry"""
        import time
        for attempt in range(self._max_retries):
            try:
                response = requests.request(method, url, **kwargs)
                # Retry on 5xx or 429 (rate limit)
                if response.status_code < 500 and response.status_code != 429:
                    return response
                
                if attempt < self._max_retries - 1:
                    wait_time = self._backoff_factor * (2 ** attempt)
                    print(f"⚠️  Request failed ({response.status_code}), retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    return response  # Last attempt, return whatever we got
            except requests.RequestException as e:
                if attempt < self._max_retries - 1:
                    wait_time = self._backoff_factor * (2 ** attempt)
                    print(f"⚠️  Request exception ({e}), retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    raise
        
        # Fallback (shouldn't reach here)
        raise requests.RequestException("Max retries exceeded")
    
    def get_site_settings(self) -> Dict[str, Any]:
        """Get current site settings"""
        if not self._ensure_valid_token():
            print("❌ Failed to authenticate")
            return {}
        
        try:
            response = self._request_with_retry(
                "GET",
                f"{self.config.api_url}/globals/site-settings",
                headers=self._headers(),
                timeout=10
            )
            return response.json() if response.ok else {}
        except requests.RequestException as e:
            print(f"Failed to get settings: {e}")
            return {}
    
    def update_site_settings(self, updates: Dict[str, Any]) -> bool:
        """Update site settings"""
        if not self._ensure_valid_token():
            print("❌ Failed to authenticate")
            return False
        
        try:
            # Get current settings
            current = self.get_site_settings()
            
            # Deep merge updates
            merged = self._deep_merge(current, updates)
            
            # Update via API
            response = self._request_with_retry(
                "POST",
                f"{self.config.api_url}/globals/site-settings",
                json=merged,
                headers=self._headers(),
                timeout=10
            )
            
            if response.ok:
                return True
            else:
                print(f"❌ Update failed: {response.status_code} {response.text}")
                return False
        except requests.RequestException as e:
            print(f"Failed to update settings: {e}")
            return False
    
    def _deep_merge(self, base: Dict, updates: Dict) -> Dict:
        """Deep merge two dictionaries"""
        result = base.copy()
        for key, value in updates.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        return result


class WebsiteEditor:
    """
    Natural language interface for editing website content
    
    Usage:
        editor = WebsiteEditor("louie")
        editor.process_command("Change the headline to 'Sales Leadership Expert'")
        editor.process_command("Update the tagline to 'Grow Your Revenue'")
    """
    
    # Map of natural language patterns to settings paths
    FIELD_MAPPINGS = {
        # Hero section
        "headline": "hero.headline",
        "main headline": "hero.headline",
        "hero headline": "hero.headline",
        "tagline": "hero.tagline",
        "slogan": "hero.tagline",
        "hero description": "hero.description",
        "main description": "hero.description",
        "intro": "hero.description",
        "video": "hero.videoId",
        "video id": "hero.videoId",
        "youtube video": "hero.videoId",
        
        # Credentials
        "credential": "credentials.primary",
        "primary credential": "credentials.primary",
        "badge": "credentials.primary",
        "secondary credential": "credentials.secondary",
        "experience": "credentials.secondary",
        
        # Value proposition
        "value headline": "valueProposition.headline",
        "value prop": "valueProposition.headline",
        "value subheadline": "valueProposition.subheadline",
        "value description": "valueProposition.description",
        "cta": "valueProposition.ctaText",
        "call to action": "valueProposition.ctaText",
        
        # Contact
        "email": "contact.email",
        "phone": "contact.phone",
        "phone number": "contact.phone",
        
        # Social
        "linkedin": "social.linkedin",
        "linkedin url": "social.linkedin",
        "youtube": "social.youtube",
        "youtube url": "social.youtube",
        "calendly": "social.calendly",
        "calendly url": "social.calendly",
        
        # SEO
        "site title": "seo.siteTitle",
        "meta title": "seo.siteTitle",
        "site description": "seo.siteDescription",
        "meta description": "seo.siteDescription",
        "keywords": "seo.keywords",
        "seo keywords": "seo.keywords",
    }
    
    def __init__(self, website_key: str = "louie"):
        if website_key not in WEBSITES:
            raise ValueError(f"Unknown website: {website_key}")
        
        self.config = WEBSITES[website_key]
        self.client = PayloadCMSClient(self.config)
        self._authenticated = False
    
    def ensure_authenticated(self) -> bool:
        """Ensure we're logged in"""
        if not self._authenticated:
            self._authenticated = self.client.login()
        return self._authenticated
    
    def process_command(self, command: str) -> Dict[str, Any]:
        """
        Process a natural language command to edit the website
        
        Examples:
            "Change the headline to 'Sales Expert'"
            "Update the tagline to 'More Sales, Less Hassle'"
            "Add testimonial from John Smith, CEO at Acme - 'Great results!'"
            "Add FAQ: What is fractional sales? Answer: It's..."
        
        Returns:
            {
                "success": bool,
                "message": str,
                "field": str,
                "old_value": str,
                "new_value": str,
            }
        """
        command_lower = command.lower()
        
        # Check for "add" commands (add testimonial, add FAQ, etc.)
        if any(word in command_lower for word in ['add', 'create', 'new']):
            return self._handle_add_command(command)
        
        # Try pattern matching first (fast path)
        field_path = None
        field_name = None
        
        for pattern, path in self.FIELD_MAPPINGS.items():
            if pattern in command_lower:
                field_path = path
                field_name = pattern
                break
        
        # If pattern matching failed, try LLM parsing for ambiguous commands
        if not field_path:
            llm_result = self._parse_with_llm(command)
            if llm_result.get('success'):
                field_path = llm_result.get('field_path')
                field_name = llm_result.get('field_name')
            else:
                # Suggest similar fields
                suggestions = self._get_field_suggestions(command_lower)
                suggestion_text = f" Did you mean: {', '.join(suggestions)}?" if suggestions else ""
                return {
                    "success": False,
                    "message": f"I didn't understand which field to edit.{suggestion_text} Available fields: headline, tagline, description, email, phone, etc.",
                    "available_fields": list(self.FIELD_MAPPINGS.keys()),
                }
        
        # Extract the new value
        new_value = self._extract_value(command)
        
        if not new_value:
            return {
                "success": False,
                "message": f"I understood you want to change the {field_name}, but couldn't find the new value. Try: 'Change {field_name} to \"Your New Value\"' or '{field_name}: Your New Value'",
            }
        
        # Ensure authenticated
        if not self.ensure_authenticated():
            return {
                "success": False,
                "message": "Failed to authenticate with the CMS. Please check credentials.",
            }
        
        # Get current value
        current_settings = self.client.get_site_settings()
        old_value = self._get_nested_value(current_settings, field_path)
        
        # Build update object
        update = self._build_nested_update(field_path, new_value)
        
        # Apply update
        success = self.client.update_site_settings(update)
        
        if success:
            return {
                "success": True,
                "message": f"✅ Updated {field_name}!",
                "field": field_name,
                "path": field_path,
                "old_value": old_value,
                "new_value": new_value,
            }
        else:
            return {
                "success": False,
                "message": f"Failed to update {field_name}. Please try again.",
            }
    
    def _handle_add_command(self, command: str) -> Dict[str, Any]:
        """Handle commands to add new items to arrays (testimonials, FAQs, etc.)"""
        command_lower = command.lower()
        
        # Ensure authenticated
        if not self.ensure_authenticated():
            return {
                "success": False,
                "message": "Failed to authenticate with the CMS. Please check credentials.",
            }
        
        # Get current settings
        current_settings = self.client.get_site_settings()
        
        # Try to detect what to add
        if 'testimonial' in command_lower:
            return self._add_testimonial(command, current_settings)
        elif 'faq' in command_lower or 'question' in command_lower:
            return self._add_faq(command, current_settings)
        elif 'service' in command_lower:
            return self._add_service(command, current_settings)
        elif 'video' in command_lower and 'featured' in command_lower:
            return self._add_featured_video(command, current_settings)
        else:
            # Use LLM to parse what to add
            return self._parse_add_command_with_llm(command, current_settings)
    
    def _add_testimonial(self, command: str, current_settings: Dict) -> Dict[str, Any]:
        """Add a new testimonial"""
        import re
        
        # Try to parse: "Add testimonial from John Smith, CEO at Acme - 'Great results!'"
        # Or: "Add testimonial: 'Quote' - Author, Role at Company"
        patterns = [
            r"from\s+([^,]+),\s*([^-\n]+)\s*[-–]\s*['\"]([^'\"]+)['\"]",
            r"['\"]([^'\"]+)['\"]\s*[-–]\s*([^,]+),\s*([^-\n]+)",
            r"['\"]([^'\"]+)['\"]\s*from\s+([^,]+),\s*([^-\n]+)",
        ]
        
        quote = None
        author = None
        role_company = None
        
        for pattern in patterns:
            match = re.search(pattern, command, re.IGNORECASE)
            if match:
                groups = match.groups()
                if len(groups) == 3:
                    quote = groups[0] if "'" in groups[0] or '"' in groups[0] else groups[2]
                    author = groups[1] if quote == groups[2] else groups[0]
                    role_company = groups[2] if quote == groups[0] else groups[1]
                    break
        
        # If parsing failed, use LLM
        if not quote:
            llm_result = self._parse_testimonial_with_llm(command)
            if llm_result.get('success'):
                quote = llm_result.get('quote')
                author = llm_result.get('author')
                role_company = llm_result.get('role_company', '')
            else:
                return {
                    "success": False,
                    "message": "Couldn't parse testimonial. Try: 'Add testimonial from John Smith, CEO at Acme - \"Great results!\"'",
                }
        
        # Parse role and company
        role = None
        company = None
        if role_company:
            if ' at ' in role_company.lower():
                parts = role_company.split(' at ', 1)
                role = parts[0].strip()
                company = parts[1].strip()
            elif ',' in role_company:
                parts = role_company.split(',', 1)
                role = parts[0].strip()
                company = parts[1].strip()
            else:
                role = role_company.strip()
        
        # Get current testimonials (if they exist as a collection) or add to a testimonials array
        # Note: Payload might have testimonials as a collection, not in site-settings
        # For now, we'll assume they're in site-settings.testimonials or similar
        
        # Create new testimonial object
        new_testimonial = {
            "quote": quote,
            "author": author or "Anonymous",
            "role": role or "",
            "company": company or "",
        }
        
        # Try to add to testimonials array if it exists in site-settings
        # Otherwise, we'd need to use the Testimonials collection API
        # For now, return success with instructions
        return {
            "success": True,
            "message": f"✅ Testimonial parsed! Quote: '{quote[:50]}...' from {author}",
            "testimonial": new_testimonial,
            "note": "Testimonials may need to be added via Payload Testimonials collection API",
        }
    
    def _add_faq(self, command: str, current_settings: Dict) -> Dict[str, Any]:
        """Add a new FAQ item"""
        import re
        
        # Try to parse: "Add FAQ: What is X? Answer: Y"
        # Or: "Add question: What is X? Answer: Y"
        patterns = [
            r"(?:question|faq)[:\s]+([^?]+\?)\s*(?:answer|ans)[:\s]+(.+)",
            r"['\"]([^'\"]+\?)['\"]\s*[-–]\s*(.+)",
        ]
        
        question = None
        answer = None
        
        for pattern in patterns:
            match = re.search(pattern, command, re.IGNORECASE)
            if match:
                question = match.group(1).strip()
                answer = match.group(2).strip()
                break
        
        # If parsing failed, use LLM
        if not question or not answer:
            llm_result = self._parse_faq_with_llm(command)
            if llm_result.get('success'):
                question = llm_result.get('question')
                answer = llm_result.get('answer')
            else:
                return {
                    "success": False,
                    "message": "Couldn't parse FAQ. Try: 'Add FAQ: What is fractional sales? Answer: It is...'",
                }
        
        # Get current FAQ items
        current_faq_items = current_settings.get('faq', {}).get('items', [])
        if not isinstance(current_faq_items, list):
            current_faq_items = []
        
        # Add new FAQ item
        new_faq = {
            "question": question,
            "answer": answer,
        }
        
        updated_faq_items = current_faq_items + [new_faq]
        
        # Update CMS
        update = {
            "faq": {
                **current_settings.get('faq', {}),
                "items": updated_faq_items,
            }
        }
        
        success = self.client.update_site_settings(update)
        
        if success:
            return {
                "success": True,
                "message": f"✅ Added FAQ: '{question[:50]}...'",
                "faq": new_faq,
                "total_faqs": len(updated_faq_items),
            }
        else:
            return {
                "success": False,
                "message": "Failed to add FAQ. Please try again.",
            }
    
    def _add_service(self, command: str, current_settings: Dict) -> Dict[str, Any]:
        """Add a new service item"""
        # Use LLM to parse service details
        llm_result = self._parse_service_with_llm(command)
        if not llm_result.get('success'):
            return {
                "success": False,
                "message": "Couldn't parse service. Try: 'Add service: Sales Training - Description here'",
            }
        
        title = llm_result.get('title')
        description = llm_result.get('description', '')
        icon = llm_result.get('icon', '/icons/business-team-6621979.svg')
        highlight = llm_result.get('highlight', False)
        
        # Get current services
        current_services = current_settings.get('services', {}).get('items', [])
        if not isinstance(current_services, list):
            current_services = []
        
        # Add new service
        new_service = {
            "title": title,
            "description": description,
            "icon": icon,
            "highlight": highlight,
        }
        
        updated_services = current_services + [new_service]
        
        # Update CMS
        update = {
            "services": {
                **current_settings.get('services', {}),
                "items": updated_services,
            }
        }
        
        success = self.client.update_site_settings(update)
        
        if success:
            return {
                "success": True,
                "message": f"✅ Added service: '{title}'",
                "service": new_service,
                "total_services": len(updated_services),
            }
        else:
            return {
                "success": False,
                "message": "Failed to add service. Please try again.",
            }
    
    def _add_featured_video(self, command: str, current_settings: Dict) -> Dict[str, Any]:
        """Add a new featured video"""
        import re
        
        # Extract YouTube video ID
        video_id_match = re.search(r'([a-zA-Z0-9_-]{11})', command)
        if not video_id_match:
            return {
                "success": False,
                "message": "Couldn't find YouTube video ID. Try: 'Add featured video ABC123xyz'",
            }
        
        video_id = video_id_match.group(1)
        
        # Use LLM to extract title and description if provided
        title = None
        description = None
        
        # Try to extract title/description from command
        title_match = re.search(r'title[:\s]+["\']?([^"\']+)["\']?', command, re.IGNORECASE)
        if title_match:
            title = title_match.group(1).strip()
        
        desc_match = re.search(r'description[:\s]+["\']?([^"\']+)["\']?', command, re.IGNORECASE)
        if desc_match:
            description = desc_match.group(1).strip()
        
        # Get current featured videos
        current_videos = current_settings.get('videosPage', {}).get('featuredVideos', [])
        if not isinstance(current_videos, list):
            current_videos = []
        
        # Add new video
        new_video = {
            "videoId": video_id,
            "title": title or f"Video {video_id}",
            "description": description or "",
        }
        
        updated_videos = current_videos + [new_video]
        
        # Update CMS
        update = {
            "videosPage": {
                **current_settings.get('videosPage', {}),
                "featuredVideos": updated_videos,
            }
        }
        
        success = self.client.update_site_settings(update)
        
        if success:
            return {
                "success": True,
                "message": f"✅ Added featured video: {video_id}",
                "video": new_video,
                "total_videos": len(updated_videos),
            }
        else:
            return {
                "success": False,
                "message": "Failed to add video. Please try again.",
            }
    
    def _parse_add_command_with_llm(self, command: str, current_settings: Dict) -> Dict[str, Any]:
        """Use LLM to parse what type of item to add"""
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            return {
                "success": False,
                "message": "LLM parsing unavailable. Please specify: 'Add testimonial...', 'Add FAQ...', etc.",
            }
        
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)
            
            prompt = f"""Parse this command to add content to a website CMS:

Command: "{command}"

Determine what type of content to add (testimonial, FAQ, service, featured video, etc.) and extract the relevant information.

Respond in JSON:
{{
  "type": "testimonial|faq|service|featured_video",
  "data": {{...relevant fields...}}
}}

If unclear, respond with {{"error": "reason"}}."""
            
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}]
            )
            
            import json
            result_text = response.content[0].text.strip()
            if result_text.startswith('```'):
                result_text = result_text.split('\n', 1)[1].rsplit('\n```', 1)[0]
            
            parsed = json.loads(result_text)
            
            if 'error' in parsed:
                return {'success': False, 'message': parsed['error']}
            
            content_type = parsed.get('type')
            data = parsed.get('data', {})
            
            # Route to appropriate handler
            if content_type == 'testimonial':
                return self._add_testimonial_from_data(data, current_settings)
            elif content_type == 'faq':
                return self._add_faq_from_data(data, current_settings)
            elif content_type == 'service':
                return self._add_service_from_data(data, current_settings)
            elif content_type == 'featured_video':
                return self._add_featured_video_from_data(data, current_settings)
            else:
                return {'success': False, 'message': f'Unknown content type: {content_type}'}
                
        except Exception as e:
            return {'success': False, 'message': f'LLM parsing failed: {str(e)}'}
    
    def _parse_testimonial_with_llm(self, command: str) -> Dict[str, Any]:
        """Use LLM to parse testimonial from command"""
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            return {'success': False}
        
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)
            
            prompt = f"""Extract testimonial information from this command:

"{command}"

Respond in JSON:
{{
  "quote": "the testimonial quote",
  "author": "person name",
  "role_company": "role at company or just role"
}}"""
            
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=200,
                messages=[{"role": "user", "content": prompt}]
            )
            
            import json
            result_text = response.content[0].text.strip()
            if result_text.startswith('```'):
                result_text = result_text.split('\n', 1)[1].rsplit('\n```', 1)[0]
            
            parsed = json.loads(result_text)
            parsed['success'] = True
            return parsed
            
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def _parse_faq_with_llm(self, command: str) -> Dict[str, Any]:
        """Use LLM to parse FAQ from command"""
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            return {'success': False}
        
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)
            
            prompt = f"""Extract FAQ question and answer from this command:

"{command}"

Respond in JSON:
{{
  "question": "the question",
  "answer": "the answer"
}}"""
            
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}]
            )
            
            import json
            result_text = response.content[0].text.strip()
            if result_text.startswith('```'):
                result_text = result_text.split('\n', 1)[1].rsplit('\n```', 1)[0]
            
            parsed = json.loads(result_text)
            parsed['success'] = True
            return parsed
            
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def _parse_service_with_llm(self, command: str) -> Dict[str, Any]:
        """Use LLM to parse service from command"""
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            return {'success': False}
        
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)
            
            prompt = f"""Extract service information from this command:

"{command}"

Respond in JSON:
{{
  "title": "service title",
  "description": "service description",
  "icon": "/icons/default.svg (optional)",
  "highlight": false
}}"""
            
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=200,
                messages=[{"role": "user", "content": prompt}]
            )
            
            import json
            result_text = response.content[0].text.strip()
            if result_text.startswith('```'):
                result_text = result_text.split('\n', 1)[1].rsplit('\n```', 1)[0]
            
            parsed = json.loads(result_text)
            parsed['success'] = True
            return parsed
            
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def _add_testimonial_from_data(self, data: Dict, current_settings: Dict) -> Dict[str, Any]:
        """Add testimonial from parsed data"""
        # Similar to _add_testimonial but uses provided data
        new_testimonial = {
            "quote": data.get('quote', ''),
            "author": data.get('author', 'Anonymous'),
            "role": data.get('role', ''),
            "company": data.get('company', ''),
        }
        
        return {
            "success": True,
            "message": f"✅ Testimonial parsed! Quote: '{new_testimonial['quote'][:50]}...'",
            "testimonial": new_testimonial,
            "note": "Testimonials may need to be added via Payload Testimonials collection API",
        }
    
    def _add_faq_from_data(self, data: Dict, current_settings: Dict) -> Dict[str, Any]:
        """Add FAQ from parsed data"""
        return self._add_faq(
            f"Add FAQ: {data.get('question', '')} Answer: {data.get('answer', '')}",
            current_settings
        )
    
    def _add_service_from_data(self, data: Dict, current_settings: Dict) -> Dict[str, Any]:
        """Add service from parsed data"""
        return self._add_service(
            f"Add service: {data.get('title', '')} - {data.get('description', '')}",
            current_settings
        )
    
    def _add_featured_video_from_data(self, data: Dict, current_settings: Dict) -> Dict[str, Any]:
        """Add featured video from parsed data"""
        return self._add_featured_video(
            f"Add featured video {data.get('videoId', '')} title: {data.get('title', '')}",
            current_settings
        )
    
    def _extract_value(self, command: str) -> Optional[str]:
        """Extract the new value from a command"""
        import re
        
        # Try double quotes
        match = re.search(r'"([^"]+)"', command)
        if match:
            return match.group(1)
        
        # Try single quotes
        match = re.search(r"'([^']+)'", command)
        if match:
            return match.group(1)
        
        # Try "to X" pattern with more variations
        patterns = [
            r"to\s+(.+)$",
            r"as\s+(.+)$",
            r"with\s+(.+)$",
            r":\s*(.+)$",  # "headline: New Value"
            r"=\s*(.+)$",  # "headline = New Value"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, command, re.IGNORECASE)
            if match:
                value = match.group(1).strip()
                # Remove trailing punctuation
                value = re.sub(r'[.!?]+$', '', value)
                if value:
                    return value
        
        return None
    
    def _get_nested_value(self, obj: Dict, path: str) -> Any:
        """Get a nested value from a dict using dot notation"""
        keys = path.split(".")
        for key in keys:
            if isinstance(obj, dict):
                obj = obj.get(key)
            else:
                return None
        return obj
    
    def _build_nested_update(self, path: str, value: Any) -> Dict:
        """Build a nested dict from a dot-notation path"""
        keys = path.split(".")
        result = {}
        current = result
        
        for i, key in enumerate(keys[:-1]):
            current[key] = {}
            current = current[key]
        
        current[keys[-1]] = value
        return result
    
    def _parse_with_llm(self, command: str) -> Dict[str, Any]:
        """
        Use Claude Opus 4.5 to parse ambiguous commands.
        
        Falls back gracefully if ANTHROPIC_API_KEY is not set or parsing fails.
        """
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            return {'success': False, 'message': 'LLM parsing unavailable (no API key)'}
        
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)
            
            # Build prompt with available fields
            fields_list = ', '.join(sorted(set(self.FIELD_MAPPINGS.keys())))
            prompt = f"""Parse this website editing command and extract the field and new value.

Command: "{command}"

Available fields: {fields_list}

Respond in JSON format:
{{
  "field": "<field_name from available fields>",
  "value": "<new_value>"
}}

If you can't determine the field or value, respond with {{"error": "reason"}}."""
            
            response = client.messages.create(
                model="claude-sonnet-4-20250514",  # Using Sonnet 4.5 for cost efficiency
                max_tokens=200,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Parse JSON response
            import json
            result_text = response.content[0].text.strip()
            # Remove markdown code fences if present
            if result_text.startswith('```'):
                result_text = result_text.split('\n', 1)[1].rsplit('\n```', 1)[0]
            
            parsed = json.loads(result_text)
            
            if 'error' in parsed:
                return {'success': False, 'message': parsed['error']}
            
            field_name = parsed.get('field', '').lower()
            new_value = parsed.get('value')
            
            # Map field name to path
            field_path = self.FIELD_MAPPINGS.get(field_name)
            if field_path and new_value:
                return {
                    'success': True,
                    'field_name': field_name,
                    'field_path': field_path,
                    'new_value': new_value
                }
            
            return {'success': False, 'message': 'Could not map field to known path'}
            
        except Exception as e:
            print(f"⚠️  LLM parsing failed: {e}")
            return {'success': False, 'message': str(e)}
    
    def _get_field_suggestions(self, command_lower: str) -> list:
        """Suggest fields based on partial match"""
        suggestions = []
        for field in self.FIELD_MAPPINGS.keys():
            # Simple substring match
            if any(word in field for word in command_lower.split()):
                suggestions.append(field)
        return suggestions[:3]  # Top 3
    
    def get_current_settings(self) -> Dict[str, Any]:
        """Get the current site settings (for display)"""
        if not self.ensure_authenticated():
            return {"error": "Not authenticated"}
        return self.client.get_site_settings()
    
    def list_editable_fields(self) -> str:
        """List all editable fields"""
        fields = sorted(set(self.FIELD_MAPPINGS.keys()))
        return "Editable fields:\n• " + "\n• ".join(fields)


# Convenience functions
def edit_louie_site(command: str) -> Dict[str, Any]:
    """Quick function to edit Louie's site"""
    editor = WebsiteEditor("louie")
    return editor.process_command(command)


def get_louie_settings() -> Dict[str, Any]:
    """Get current settings for Louie's site"""
    editor = WebsiteEditor("louie")
    return editor.get_current_settings()


if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) > 1:
        command = " ".join(sys.argv[1:])
        result = edit_louie_site(command)
        print(json.dumps(result, indent=2))
    else:
        print("Usage: python cms_integration.py 'Change the headline to \"New Headline\"'")
        print("\nAvailable commands:")
        editor = WebsiteEditor("louie")
        print(editor.list_editable_fields())

