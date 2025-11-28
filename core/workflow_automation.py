"""
Workflow Automation - The Real Product

Input from anywhere → World-class content → Auto-publish

This is the actual value proposition.
"""

import os
import json
from pathlib import Path
from typing import Dict, Optional, List
from datetime import datetime
import re

try:
    from openai import OpenAI
    from anthropic import Anthropic
except ImportError:
    OpenAI = None
    Anthropic = None

from .content_generator import ContentGenerator, GenerationConfig
from .humanizer import Humanizer
from .voice_profiler import VoiceProfiler


class ContentWorkflow:
    """
    Complete workflow: Input → Generate → Humanize → Publish
    
    The real product: Add topic/voice note from anywhere, get world-class content.
    """
    
    def __init__(
        self,
        profile_name: str,
        openai_api_key: Optional[str] = None,
        anthropic_api_key: Optional[str] = None
    ):
        self.profile_name = profile_name
        self.generator = ContentGenerator(
            openai_api_key=openai_api_key,
            anthropic_api_key=anthropic_api_key
        )
        self.humanizer = Humanizer(profile_name=profile_name)
        self.profiler = VoiceProfiler()
        
        # Load voice profile
        self.voice_profile = self.profiler.load_profile(profile_name)
        if not self.voice_profile:
            raise ValueError(f"Profile '{profile_name}' not found")
    
    def process_input(
        self,
        input_text: str,
        input_type: Optional[str] = None,  # Auto-detect if None
        output_format: Optional[str] = None,  # Auto-detect if None
        target_length: int = 1200,
        style_influences: Optional[List[tuple]] = None,
        auto_humanize: bool = True,
        auto_publish: bool = False,
        publish_config: Optional[Dict] = None,
        auto_yes: bool = True  # Skip all prompts by default
    ) -> Dict:
        """
        Process input from anywhere and create world-class content.
        
        Args:
            input_text: Topic, voice note transcript, or bullet points
            input_type: "topic", "voice_note", "bullet_points"
            output_format: "article", "linkedin", "twitter", "faq"
            target_length: Target word count
            style_influences: Optional list of (profile, weight) tuples
            auto_humanize: Automatically humanize the output
            auto_publish: Automatically publish to configured destination
            publish_config: Publishing configuration (GitHub, WordPress, etc.)
            
        Returns:
            Complete workflow result with all steps
        """
        
        # Auto-detect input type if not specified
        if input_type is None:
            input_type = self._detect_input_type(input_text)
        
        # Auto-detect output format if not specified
        if output_format is None:
            output_format = self._detect_output_format(input_text, auto_yes)
        
        workflow_result = {
            "input": input_text,
            "input_type": input_type,
            "output_format": output_format,
            "timestamp": datetime.now().isoformat(),
            "steps": []
        }
        
        # Step 1: Process input based on type
        if not auto_yes:
            print(f"📥 Processing {input_type}...")
        
        if input_type == "voice_note":
            content_brief = self._process_voice_note(input_text)
        elif input_type == "bullet_points":
            content_brief = self._process_bullet_points(input_text)
        elif input_type == "whatsapp":
            content_brief = self._process_whatsapp_paste(input_text)
        else:  # topic
            content_brief = input_text
        
        workflow_result["steps"].append({
            "step": "input_processing",
            "result": content_brief,
            "status": "complete"
        })
        
        # Step 2: Generate content
        if not auto_yes:
            print(f"✍️  Generating {output_format}...")
        
        config = GenerationConfig(
            format=output_format,
            target_length=target_length
        )
        
        generation_result = self.generator.generate(
            content_brief=content_brief,
            voice_profile=self.voice_profile,
            style_influences=style_influences,
            config=config,
            model="claude-haiku-4-5-20251001"
        )
        
        workflow_result["steps"].append({
            "step": "generation",
            "result": generation_result["content"],
            "metadata": generation_result["metadata"],
            "status": "complete"
        })
        
        content = generation_result["content"]
        
        # Step 3: Humanize (if enabled)
        if auto_humanize:
            if not auto_yes:
                print("🎨 Humanizing content...")
            
            humanize_result = self.humanizer.humanize(
                text=content,
                show_analysis=False,
                model="claude-haiku-4-5-20251001"
            )
            
            content = humanize_result["humanized"]
            
            workflow_result["steps"].append({
                "step": "humanization",
                "result": content,
                "status": "complete"
            })
        
        # Step 4: Save output
        output_path = self._save_output(content, output_format)
        workflow_result["output_path"] = str(output_path)
        
        # Step 4.5: Save to Notion (if configured)
        try:
            from integrations.notion_integration import save_to_notion
            notion_result = save_to_notion(
                title=generation_result.get("metadata", {}).get("title", "Untitled Article"),
                topic=input_text[:100],  # First 100 chars of input
                content=content,
                status="Draft",
                word_count=len(content.split()),
                platform=output_format.title()
            )
            if notion_result and notion_result.get("id"):
                workflow_result["notion_page_id"] = notion_result.get("id")
                if not auto_yes:
                    print("📝 Saved to Notion")
        except ImportError:
            pass  # Notion integration not available
        except Exception as e:
            if not auto_yes:
                print(f"⚠️  Notion save skipped: {e}")
        
        # Step 4.6: Save to AITable (if configured) - legacy support
        try:
            from integrations.aitable_integration import save_to_aitable
            aitable_result = save_to_aitable(
                title=generation_result.get("metadata", {}).get("title", "Untitled Article"),
                topic=input_text[:100],
                content=content,
                status="Draft",
                word_count=len(content.split()),
                platform=output_format.title()
            )
            if aitable_result and aitable_result.get("id"):
                workflow_result["aitable_record_id"] = aitable_result.get("id")
                if not auto_yes:
                    print("📊 Saved to AITable")
        except (ImportError, ValueError):
            pass  # AITable integration not available
        except Exception as e:
            if not auto_yes:
                print(f"⚠️  AITable save skipped: {e}")
        
        # Step 5: Auto-publish (if enabled)
        if auto_publish and publish_config:
            if not auto_yes:
                print("🚀 Publishing...")
            
            publish_result = self._publish(
                content=content,
                config=publish_config,
                format=output_format
            )
            
            workflow_result["steps"].append({
                "step": "publishing",
                "result": publish_result,
                "status": "complete" if publish_result.get("success") else "failed"
            })
        
        workflow_result["final_content"] = content
        workflow_result["status"] = "complete"
        
        if not auto_yes:
            print("✅ Workflow complete!")
        
        return workflow_result
    
    def _detect_input_type(self, input_text: str) -> str:
        """Auto-detect input type from text"""
        text_lower = input_text.lower().strip()
        lines = input_text.split('\n')
        word_count = len(input_text.split())
        
        # Check for WhatsApp patterns (check first, most specific)
        whatsapp_patterns = ['[', ']']
        has_timestamps = any('[' in line and ']' in line for line in lines)
        has_colon_format = sum(1 for line in lines if ':' in line and len(line.split(':')) >= 2) >= 2
        
        if has_timestamps and has_colon_format:
            return "whatsapp"
        
        # Check for bullet points (check before voice note)
        bullet_markers = ['-', '*', '•', '1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.']
        bullet_count = sum(1 for line in lines if any(line.strip().startswith(marker) for marker in bullet_markers))
        if bullet_count >= 2:
            return "bullet_points"
        
        # Check for voice note patterns (transcript-like)
        # Look for speech patterns - more lenient threshold
        speech_indicators = ['um', 'uh', 'like', 'you know', 'so', 'well', 'actually', 'kind of', 'sort of', 'i mean', 'you see']
        speech_count = sum(1 for indicator in speech_indicators if indicator in text_lower)
        
        # Also check for run-on sentences and conversational patterns
        has_long_sentences = any(len(sentence.split()) > 30 for sentence in input_text.split('.'))
        
        # More lenient: if it has speech indicators and is conversational, it's likely a voice note
        if speech_count >= 2 and word_count > 30:
            return "voice_note"
        # Or if it's very long with at least one speech indicator
        if word_count > 100 and speech_count >= 1:
            return "voice_note"
        
        # Default to topic
        return "topic"
    
    def _detect_output_format(self, input_text: str, auto_yes: bool = True) -> str:
        """Auto-detect best output format from input"""
        text_lower = input_text.lower()
        word_count = len(input_text.split())
        
        # Check for explicit format hints in the text (highest priority)
        format_keywords = {
            'linkedin': ['linkedin', 'linkedin post', 'social post', 'social media', 'post on linkedin'],
            'twitter': ['twitter', 'tweet', 'thread', 'twitter thread', 'x thread'],
            'faq': ['faq', 'question', 'questions', 'q&a', 'q and a', 'frequently asked'],
            'email': ['email', 'newsletter', 'email newsletter', 'send email', 'email to']
        }
        
        for format_type, keywords in format_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return format_type
        
        # Smart detection based on input characteristics
        # Very short input (< 10 words) → LinkedIn post
        if word_count < 10:
            return "linkedin"
        
        # Short input (10-30 words) → Check if it's a full thought or just a topic
        elif word_count < 30:
            # If it's a complete sentence/question, might be LinkedIn
            # If it's just a topic phrase (no punctuation, no complete thought), default to article
            has_punctuation = any(char in input_text for char in ['?', '!', '.'])
            is_complete_thought = has_punctuation and word_count > 5
            
            if is_complete_thought:
                return "linkedin"
            else:
                return "article"  # Default to article for topic phrases (most common use case)
        
        # Medium input (30-50 words) → Usually article, but could be LinkedIn if very conversational
        elif word_count < 50:
            return "article"  # Default to article for medium-length topics
        
        # Medium to long input (50+ words) → Article (most common)
        else:
            return "article"
        
        # Default fallback
        return "article"
    
    def _process_voice_note(self, transcript: str) -> str:
        """Process voice note transcript into content brief"""
        # Clean up common voice note artifacts
        cleaned = transcript.strip()
        
        # Remove filler words and pauses (basic cleanup)
        filler_words = ['um', 'uh', 'like', 'you know', 'so', 'well', 'actually']
        words = cleaned.split()
        cleaned_words = [w for w in words if w.lower() not in filler_words]
        
        # Rejoin and return
        return ' '.join(cleaned_words)
    
    def _process_bullet_points(self, bullets: str) -> str:
        """Process bullet points into content brief"""
        # Convert bullet points to narrative brief
        lines = [line.strip() for line in bullets.split('\n') if line.strip()]
        
        # Remove bullet markers
        cleaned_lines = []
        for line in lines:
            # Remove common bullet markers
            for marker in ['-', '*', '•', '1.', '2.', '3.', '4.', '5.']:
                if line.startswith(marker):
                    line = line[len(marker):].strip()
                    break
            cleaned_lines.append(line)
        
        # Join into narrative
        return " ".join(cleaned_lines)
    
    def _process_whatsapp_paste(self, text: str) -> str:
        """Process WhatsApp conversation paste into content brief"""
        # Remove WhatsApp metadata (timestamps, names, etc.)
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Skip lines that look like metadata
            if any(pattern in line for pattern in ['[', ']', 'AM', 'PM', ':', '→']):
                # Might be timestamp or metadata, skip
                continue
            # Skip empty lines
            if not line.strip():
                continue
            cleaned_lines.append(line.strip())
        
        return " ".join(cleaned_lines)
    
    def _save_output(self, content: str, format: str) -> Path:
        """Save content to file"""
        output_dir = Path("./data/outputs/workflow")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{format}_{timestamp}.md"
        output_path = output_dir / filename
        
        with open(output_path, 'w') as f:
            f.write(content)
        
        return output_path
    
    def _publish(self, content: str, config: Dict, format: str) -> Dict:
        """Publish content to configured destination"""
        destination = config.get("destination", "github")
        
        if destination == "github":
            return self._publish_to_github(content, config, format)
        elif destination == "wordpress":
            return self._publish_to_wordpress(content, config, format)
        elif destination == "file":
            return self._publish_to_file(content, config, format)
        else:
            return {"success": False, "error": f"Unknown destination: {destination}"}
    
    def _publish_to_github(self, content: str, config: Dict, format: str) -> Dict:
        """Publish to GitHub repository"""
        try:
            from github import Github
            
            token = config.get("github_token") or os.getenv("GITHUB_TOKEN")
            repo_name = config.get("repo")
            file_path = config.get("file_path", f"content/{format}/{datetime.now().strftime('%Y-%m-%d')}.md")
            
            if not token or not repo_name:
                return {"success": False, "error": "GitHub token or repo not configured"}
            
            g = Github(token)
            repo = g.get_repo(repo_name)
            
            # Create or update file
            try:
                file = repo.get_contents(file_path)
                repo.update_file(
                    file_path,
                    f"Update {format} via VoiceCraft",
                    content,
                    file.sha
                )
            except:
                repo.create_file(
                    file_path,
                    f"Add {format} via VoiceCraft",
                    content
                )
            
            return {
                "success": True,
                "url": f"https://github.com/{repo_name}/blob/main/{file_path}",
                "file_path": file_path
            }
        
        except ImportError:
            return {"success": False, "error": "PyGithub not installed"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _publish_to_wordpress(self, content: str, config: Dict, format: str) -> Dict:
        """Publish to WordPress via REST API"""
        try:
            import requests
            from requests.auth import HTTPBasicAuth
            
            # WordPress configuration
            site_url = config.get("site_url") or config.get("site")
            username = config.get("username") or os.getenv("WORDPRESS_USERNAME")
            password = config.get("password") or os.getenv("WORDPRESS_PASSWORD")
            app_password = config.get("app_password") or os.getenv("WORDPRESS_APP_PASSWORD")
            
            if not site_url:
                return {"success": False, "error": "WordPress site URL not configured"}
            
            # Use app password if available (recommended), otherwise username/password
            if app_password:
                auth = HTTPBasicAuth(username, app_password)
            elif username and password:
                auth = HTTPBasicAuth(username, password)
            else:
                return {"success": False, "error": "WordPress credentials not configured"}
            
            # Clean up site URL
            site_url = site_url.rstrip('/')
            if not site_url.startswith('http'):
                site_url = f"https://{site_url}"
            
            # WordPress REST API endpoint
            api_url = f"{site_url}/wp-json/wp/v2/posts"
            
            # Extract title from content (first line or first 50 chars)
            lines = content.split('\n')
            title = lines[0].strip('#').strip() if lines else content[:50]
            if len(title) > 100:
                title = title[:97] + "..."
            
            # Prepare post data
            post_data = {
                "title": title,
                "content": content,
                "status": config.get("status", "draft"),  # 'draft', 'publish', 'pending'
                "format": "standard"
            }
            
            # Add categories if specified
            if config.get("categories"):
                post_data["categories"] = config["categories"]
            
            # Add tags if specified
            if config.get("tags"):
                post_data["tags"] = config["tags"]
            
            # Add featured image if specified
            if config.get("featured_image_id"):
                post_data["featured_media"] = config["featured_image_id"]
            
            # Make API request
            response = requests.post(
                api_url,
                json=post_data,
                auth=auth,
                timeout=30
            )
            
            if response.status_code == 201:
                post = response.json()
                return {
                    "success": True,
                    "url": post.get("link", ""),
                    "post_id": post.get("id"),
                    "edit_url": post.get("link", "").replace("/", "/wp-admin/post.php?post=") + "&action=edit"
                }
            else:
                return {
                    "success": False,
                    "error": f"WordPress API error: {response.status_code} - {response.text}"
                }
        
        except ImportError:
            return {"success": False, "error": "requests library not installed. Install with: pip install requests"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _publish_to_file(self, content: str, config: Dict, format: str) -> Dict:
        """Publish to local file"""
        file_path = Path(config.get("file_path", f"./published/{format}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"))
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w') as f:
            f.write(content)
        
        return {
            "success": True,
            "file_path": str(file_path)
        }


# Convenience function for quick workflow
def quick_content(
    input_text: str,
    profile_name: str = "Max Bernstein",
    input_type: Optional[str] = None,  # Auto-detect
    output_format: Optional[str] = None,  # Auto-detect
    auto_humanize: bool = True,
    auto_yes: bool = True  # Skip prompts by default
) -> str:
    """
    Quick workflow: Input → World-class content (completely automatic)
    
    Usage:
        content = quick_content("How AI is changing expertise")
        # Auto-detects type and format, returns humanized article ready to publish
    """
    workflow = ContentWorkflow(profile_name)
    result = workflow.process_input(
        input_text=input_text,
        input_type=input_type,
        output_format=output_format,
        auto_humanize=auto_humanize,
        auto_publish=False,
        auto_yes=auto_yes
    )
    return result["final_content"]

