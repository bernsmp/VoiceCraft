"""
Slack Integration - VoiceCraft + Website CMS

Trigger content workflow and edit website from Slack messages.
"""

import os
import json
from pathlib import Path
import sys
from typing import Dict, List, Any

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.workflow_automation import ContentWorkflow


class SlackContentBot:
    """
    Slack bot that processes messages and triggers content workflow
    
    Content Commands:
        /content "How AI is changing expertise"
        /content-voice [paste transcript]
        /content-blend "topic" Hormozi:30 Godin:20
    
    Website Commands:
        /site headline "New Headline Here"
        /site tagline "New Tagline"
        /site video fCVKpcpD8tA
        /site show  (shows current settings)
        /site help  (shows available commands)
    
    Natural Language:
        "Change the headline to 'Sales Expert'"
        "Update the tagline"
        "What's the current hero description?"
    """
    
    def __init__(self, profile_name: str = "Louie Bernstein"):
        self.workflow = ContentWorkflow(profile_name)
        self._website_editor = None
    
    @property
    def website_editor(self):
        """Lazy load website editor"""
        if self._website_editor is None:
            from integrations.cms_integration import WebsiteEditor
            self._website_editor = WebsiteEditor("louie")
        return self._website_editor
    
    def process_slack_message(
        self,
        message: str,
        user: str,
        channel: str
    ) -> Dict:
        """
        Process Slack message and route to appropriate handler
        """
        message = message.strip()
        
        # Website editing commands
        if message.startswith("/site"):
            return self._handle_site_command(message)
        
        # Check for natural language website editing (including "add" commands)
        if self._is_website_edit_request(message) or any(word in message.lower() for word in ['add', 'create', 'new']):
            return self._handle_natural_language_edit(message)
        
        # Content generation commands
        if message.startswith("/content"):
            return self._handle_content_command(message, user, channel)
        
        # Unknown command
        return self._format_help_response()
    
    def _handle_site_command(self, message: str) -> Dict:
        """Handle /site commands"""
        parts = message.replace("/site", "").strip().split(None, 1)
        
        if not parts:
            return self._format_site_help()
        
        command = parts[0].lower()
        value = parts[1] if len(parts) > 1 else None
        
        # Show current settings
        if command in ["show", "settings", "current"]:
            return self._show_site_settings()
        
        # Help
        if command in ["help", "?"]:
            return self._format_site_help()
        
        # Edit a field
        if value:
            # Clean up value (remove quotes)
            value = value.strip('"').strip("'")
            edit_command = f'Change the {command} to "{value}"'
            return self._do_site_edit(edit_command)
        
        return {
            "text": f"❓ Missing value. Try: `/site {command} \"Your Value\"`"
        }
    
    def _handle_natural_language_edit(self, message: str) -> Dict:
        """Handle natural language website editing requests"""
        return self._do_site_edit(message)
    
    def _do_site_edit(self, command: str, preview_only: bool = True) -> Dict:
        """Execute a website edit command (with preview support)"""
        try:
            result = self.website_editor.process_command(command)
            
            if result.get("success"):
                # Check if this is an "add" command (testimonials, FAQs, etc.)
                is_add_command = any(word in command.lower() for word in ['add', 'create', 'new'])
                
                response = {
                    "text": f"🔍 Preview: {result.get('field', 'field')} → {str(result.get('new_value', ''))[:50]}" if preview_only else f"✅ {result.get('message', 'Updated!')}",
                    "preview": preview_only,  # Flag for confirmation flow
                    "command": command,  # Store for later execution
                    "result": result,  # Full result for execution
                    "blocks": [
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": f"*🔍 Preview: {result.get('message')}*" if preview_only else f"*✅ {result.get('message')}*"
                            }
                        },
                        {
                            "type": "section",
                            "fields": [
                                {
                                    "type": "mrkdwn",
                                    "text": f"*Field:*\n{result.get('field', 'Unknown')}"
                                },
                                {
                                    "type": "mrkdwn",
                                    "text": f"*New Value:*\n{str(result.get('new_value', 'N/A'))[:200]}"
                                }
                            ]
                        },
                        {
                            "type": "context",
                            "elements": [
                                {
                                    "type": "mrkdwn",
                                    "text": f"Previous: {str(result.get('old_value', 'N/A'))[:100]}"
                                }
                            ]
                        }
                    ]
                }
                
                # Add additional info for "add" commands
                if is_add_command and result.get('faq'):
                    response['blocks'].append({
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*Question:* {result.get('faq', {}).get('question', '')[:100]}\n*Answer:* {result.get('faq', {}).get('answer', '')[:200]}"
                        }
                    })
                elif is_add_command and result.get('service'):
                    response['blocks'].append({
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*Service:* {result.get('service', {}).get('title', '')}\n*Description:* {result.get('service', {}).get('description', '')[:200]}"
                        }
                    })
                elif is_add_command and result.get('testimonial'):
                    testimonial = result.get('testimonial', {})
                    response['blocks'].append({
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*Quote:* {testimonial.get('quote', '')[:200]}\n*From:* {testimonial.get('author', '')}, {testimonial.get('role', '')} at {testimonial.get('company', '')}"
                        }
                    })
                elif is_add_command and result.get('video'):
                    video = result.get('video', {})
                    response['blocks'].append({
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*Video ID:* {video.get('videoId', '')}\n*Title:* {video.get('title', '')}\n*Description:* {video.get('description', '')[:200]}"
                        }
                    })
                
                return response
            else:
                return {
                    "text": f"❌ {result.get('message', 'Edit failed')}",
                    "preview": False,
                    "blocks": [
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": f"*{result.get('message')}*"
                            }
                        }
                    ]
                }
        except Exception as e:
            import traceback
            return {
                "text": f"❌ Error: {str(e)}",
                "preview": False,
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*Error:*\n```{str(e)[:500]}```"
                        }
                    }
                ]
            }
    
    def _show_site_settings(self) -> Dict:
        """Show current site settings"""
        try:
            settings = self.website_editor.get_current_settings()
            
            if "error" in settings:
                return {"text": f"❌ {settings['error']}"}
            
            hero = settings.get("hero", {})
            credentials = settings.get("credentials", {})
            contact = settings.get("contact", {})
            
            return {
                "text": "📄 Current Site Settings",
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": "🌐 louiebernstein.com Settings"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*Hero Section:*\n• Headline: {hero.get('headline', 'N/A')}\n• Tagline: {hero.get('tagline', 'N/A')}\n• Video ID: {hero.get('videoId', 'N/A')}"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*Credentials:*\n• Primary: {credentials.get('primary', 'N/A')}\n• Secondary: {credentials.get('secondary', 'N/A')}"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*Contact:*\n• Email: {contact.get('email', 'N/A')}\n• Phone: {contact.get('phone', 'N/A')}"
                        }
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "context",
                        "elements": [
                            {
                                "type": "mrkdwn",
                                "text": "To edit: `/site headline \"New Text\"` or just say \"Change the headline to...\""
                            }
                        ]
                    }
                ]
            }
        except Exception as e:
            return {"text": f"❌ Error loading settings: {str(e)}"}
    
    def _is_website_edit_request(self, message: str) -> bool:
        """Check if message is a website editing request"""
        triggers = [
            "change the", "update the", "set the", "make the",
            "edit the", "modify the", "what's the", "what is the",
            "show me the", "headline", "tagline", "description",
            "website", "site", "add", "create", "new"
        ]
        message_lower = message.lower()
        return any(trigger in message_lower for trigger in triggers)
    
    def _handle_content_command(
        self,
        message: str,
        user: str,
        channel: str
    ) -> Dict:
        """Handle content generation commands"""
        
        # Parse command
        if message.startswith("/content-voice"):
            # Voice note
            transcript = message.replace("/content-voice", "").strip()
            result = self.workflow.process_input(
                input_text=transcript,
                input_type="voice_note",
                auto_humanize=True
            )
        
        elif message.startswith("/content-blend"):
            # Style blend
            parts = message.replace("/content-blend", "").strip().split()
            topic = parts[0].strip('"')
            influences = self._parse_influences(parts[1:])
            
            result = self.workflow.process_input(
                input_text=topic,
                input_type="topic",
                style_influences=influences,
                auto_humanize=True
            )
        
        else:
            # Regular topic
            topic = message.replace("/content", "").strip().strip('"')
            result = self.workflow.process_input(
                input_text=topic,
                input_type="topic",
                auto_humanize=True
            )
        
        # Format response for Slack
        return {
            "text": f"✅ Content generated!",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Content Ready*\n\n{result['final_content'][:500]}..."
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Saved to:* `{result['output_path']}`"
                    }
                }
            ]
        }
    
    def _parse_influences(self, parts: List[str]) -> List[tuple]:
        """Parse influence string like 'Hormozi:30,Godin:20'"""
        influences = []
        # TODO: Load influence profiles and parse weights
        return influences
    
    def _format_site_help(self) -> Dict:
        """Format help message for site commands"""
        return {
            "text": "🌐 Website Editing Commands",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "🌐 Website Editing Commands"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Quick Commands:*\n• `/site show` - View current settings\n• `/site headline \"New Headline\"` - Update headline\n• `/site tagline \"New Tagline\"` - Update tagline\n• `/site video ABC123` - Update YouTube video ID"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Natural Language:*\n• \"Change the headline to 'Sales Expert'\"\n• \"Update the tagline\"\n• \"Set the phone number to (555) 123-4567\""
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Editable Fields:*\nheadline, tagline, description, video, credential, email, phone, linkedin, youtube, calendly, cta, site title, site description, keywords"
                    }
                }
            ]
        }
    
    def _format_help_response(self) -> Dict:
        """Format general help message"""
        return {
            "text": "🤖 VoiceCraft Bot Commands",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "🤖 VoiceCraft Bot"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Content Generation:*\n• `/content \"Topic\"` - Generate article\n• `/content-voice [transcript]` - Process voice note\n• `/content-blend \"topic\" Style:30` - Generate with style"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Website Editing:*\n• `/site show` - View settings\n• `/site headline \"New Text\"` - Update field\n• Or just say: \"Change the headline to...\""
                    }
                }
            ]
        }


# Flask app for Slack webhook
def create_slack_app():
    """Create Flask app for Slack webhook"""
    try:
        from flask import Flask, request, jsonify
    except ImportError:
        print("Flask not installed. Install with: pip install flask")
        return None
    
    app = Flask(__name__)
    bot = SlackContentBot()
    
    @app.route('/slack/events', methods=['POST'])
    def handle_slack():
        data = request.json
        
        # URL verification challenge
        if data.get("type") == "url_verification":
            return jsonify({"challenge": data.get("challenge")})
        
        # Handle events
        event = data.get("event", {})
        message = event.get("text", "")
        user = event.get("user", "")
        channel = event.get("channel", "")
        
        # Ignore bot messages
        if event.get("bot_id"):
            return jsonify({"status": "ok"})
        
        # Process message
        result = bot.process_slack_message(message, user, channel)
        return jsonify(result)
    
    @app.route('/slack/commands', methods=['POST'])
    def handle_command():
        """Handle slash commands"""
        command = request.form.get("command", "")
        text = request.form.get("text", "")
        user = request.form.get("user_id", "")
        channel = request.form.get("channel_id", "")
        
        # Combine command and text
        full_message = f"{command} {text}".strip()
        
        result = bot.process_slack_message(full_message, user, channel)
        return jsonify(result)
    
    return app


if __name__ == "__main__":
    # Test mode
    bot = SlackContentBot()
    
    print("VoiceCraft Slack Bot - Test Mode")
    print("=" * 40)
    
    test_commands = [
        "/site show",
        "/site help",
        "Change the headline to 'Test Headline'",
        "/site tagline \"Less Spend. More Sales.\"",
    ]
    
    for cmd in test_commands:
        print(f"\n> {cmd}")
        result = bot.process_slack_message(cmd, "test_user", "test_channel")
        print(json.dumps(result, indent=2))
