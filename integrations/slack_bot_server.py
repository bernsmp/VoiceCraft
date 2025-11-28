"""
Slack Bot Server

Run the VoiceCraft Slack bot with Flask.
Supports both Slack Events API and Slash Commands.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from flask import Flask, request, jsonify
import json
import hmac
import hashlib
import time

from integrations.slack_bot import SlackContentBot
from integrations.deploy_webhook import trigger_deploy_and_notify, payload_webhook_handler

try:
    from slack_sdk import WebClient
    from slack_sdk.errors import SlackApiError
    SLACK_SDK_AVAILABLE = True
except ImportError:
    print("⚠️  slack_sdk not installed. Run: pip install slack-sdk")
    SLACK_SDK_AVAILABLE = False


def verify_slack_signature(request_data, timestamp, signature):
    """Verify the request came from Slack"""
    signing_secret = os.getenv("SLACK_SIGNING_SECRET", "")
    if not signing_secret:
        return True  # Skip verification in development
    
    sig_basestring = f"v0:{timestamp}:{request_data}"
    my_signature = "v0=" + hmac.new(
        signing_secret.encode(),
        sig_basestring.encode(),
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(my_signature, signature)


def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    bot = SlackContentBot("Louie Bernstein")
    
    # Initialize Slack WebClient for posting responses
    slack_token = os.getenv('SLACK_BOT_TOKEN')
    slack_client = WebClient(token=slack_token) if slack_token and SLACK_SDK_AVAILABLE else None
    
    # In-memory store for pending confirmations (production: use Redis)
    pending_confirmations = {}
    
    @app.before_request
    def verify_request():
        """Verify Slack request signature"""
        if request.path.startswith("/slack"):
            # Skip verification for interactive endpoint (handled separately)
            if request.path == "/slack/interactive":
                return None
            
            timestamp = request.headers.get("X-Slack-Request-Timestamp", "")
            signature = request.headers.get("X-Slack-Signature", "")
            
            # Check timestamp to prevent replay attacks
            if timestamp and abs(time.time() - int(timestamp or 0)) > 60 * 5:
                return jsonify({"error": "Invalid timestamp"}), 403
            
            if signature and not verify_slack_signature(
                request.get_data(as_text=True),
                timestamp,
                signature
            ):
                return jsonify({"error": "Invalid signature"}), 403
    
    @app.route("/", methods=["GET"])
    def health():
        """Health check endpoint"""
        return jsonify({
            "status": "healthy",
            "service": "VoiceCraft Slack Bot",
            "version": "1.0.0",
        })
    
    @app.route("/slack/events", methods=["POST"])
    def handle_events():
        """Handle Slack Events API"""
        data = request.json
        
        # URL verification challenge
        if data.get("type") == "url_verification":
            return jsonify({"challenge": data.get("challenge")})
        
        # Handle message events
        event = data.get("event", {})
        
        # Ignore bot messages and message_changed events
        if event.get("bot_id") or event.get("subtype") == "message_changed":
            return jsonify({"status": "ok"})
        
        message = event.get("text", "")
        user = event.get("user", "")
        channel = event.get("channel", "")
        thread_ts = event.get("ts")  # For threading replies
        
        # Only process direct messages or mentions
        if message:
            result = bot.process_slack_message(message, user, channel)
            
            # Post response back to Slack
            if slack_client:
                try:
                    # If it's a website edit command, show confirmation first
                    if result.get('preview'):
                        confirmation_id = f"{user}_{channel}_{int(time.time())}"
                        pending_confirmations[confirmation_id] = {
                            'result': result,
                            'user': user,
                            'channel': channel
                        }
                        
                        # Build confirmation blocks
                        blocks = result.get('blocks', []) + [
                            {
                                "type": "actions",
                                "elements": [
                                    {
                                        "type": "button",
                                        "text": {"type": "plain_text", "text": "✅ Confirm"},
                                        "style": "primary",
                                        "action_id": "confirm_change",
                                        "value": confirmation_id
                                    },
                                    {
                                        "type": "button",
                                        "text": {"type": "plain_text", "text": "❌ Cancel"},
                                        "style": "danger",
                                        "action_id": "cancel_change",
                                        "value": confirmation_id
                                    }
                                ]
                            }
                        ]
                        
                        slack_client.chat_postMessage(
                            channel=channel,
                            thread_ts=thread_ts,
                            text=result.get('text', 'Preview'),
                            blocks=blocks
                        )
                    else:
                        # Post directly (non-edit commands or errors)
                        slack_client.chat_postMessage(
                            channel=channel,
                            thread_ts=thread_ts,
                            text=result.get('text', ''),
                            blocks=result.get('blocks')
                        )
                except SlackApiError as e:
                    print(f"⚠️  Slack API error: {e.response['error']}")
            else:
                # Fallback: print to console
                print(f"Response: {json.dumps(result, indent=2)}")
        
        return jsonify({"status": "ok"})
    
    @app.route("/slack/commands", methods=["POST"])
    def handle_commands():
        """Handle Slack slash commands"""
        command = request.form.get("command", "")
        text = request.form.get("text", "")
        user_id = request.form.get("user_id", "")
        channel_id = request.form.get("channel_id", "")
        
        # Combine command and text
        full_message = f"{command} {text}".strip()
        
        # Process the command
        result = bot.process_slack_message(full_message, user_id, channel_id)
        
        # Return response (Slack will display this)
        return jsonify({
            "response_type": "in_channel",  # or "ephemeral" for private
            **result
        })
    
    @app.route("/slack/interactive", methods=["POST"])
    def handle_interactive():
        """Handle interactive components (buttons, menus, etc.)"""
        # Verify signature for interactive payloads
        timestamp = request.headers.get("X-Slack-Request-Timestamp", "")
        signature = request.headers.get("X-Slack-Signature", "")
        
        if signature:
            # Get raw body for signature verification
            body = request.get_data(as_text=True)
            if not verify_slack_signature(body, timestamp, signature):
                return jsonify({"error": "Invalid signature"}), 403
        
        payload = json.loads(request.form.get("payload", "{}"))
        
        action_type = payload.get("type")
        user = payload.get("user", {}).get("id")
        channel = payload.get("channel", {}).get("id")
        message_ts = payload.get("message", {}).get("ts")
        
        if action_type == "block_actions":
            actions = payload.get("actions", [])
            for action in actions:
                action_id = action.get("action_id")
                confirmation_id = action.get("value")
                
                if action_id == "confirm_change" and confirmation_id in pending_confirmations:
                    # Apply the change
                    conf = pending_confirmations.pop(confirmation_id)
                    command = conf.get('command')
                    preview_result = conf.get('result')
                    
                    # The WebsiteEditor.process_command already executed the change
                    # So we just need to confirm it worked and update the message
                    if slack_client:
                        try:
                            # Update the original message to show it was applied
                            success_text = f"✅ Change applied! {preview_result.get('message', '')}"
                            blocks = preview_result.get('blocks', []) if isinstance(preview_result, dict) else []
                            
                            # Replace preview text with success in blocks
                            updated_blocks = []
                            for block in blocks:
                                if block.get('type') == 'section':
                                    text_obj = block.get('text', {})
                                    if isinstance(text_obj, dict):
                                        text_content = text_obj.get('text', '')
                                        # Replace preview indicators
                                        text_content = text_content.replace('🔍 Preview:', '✅ Applied:')
                                        text_content = text_content.replace('Preview:', 'Applied:')
                                        block['text']['text'] = text_content
                                updated_blocks.append(block)
                            
                            # Remove confirmation buttons (they're no longer needed)
                            updated_blocks = [b for b in updated_blocks if b.get('type') != 'actions']
                            
                            slack_client.chat_update(
                                channel=channel,
                                ts=message_ts,
                                text=success_text,
                                blocks=updated_blocks if updated_blocks else None
                            )
                            
                            # Optionally trigger deployment notification
                            # trigger_deploy_and_notify(channel, "Website content updated")
                            
                        except SlackApiError as e:
                            print(f"⚠️  Slack update error: {e.response['error']}")
                            # Try to post a new message if update fails
                            try:
                                slack_client.chat_postMessage(
                                    channel=channel,
                                    text=f"✅ Change applied! (Update message failed: {e.response.get('error', 'unknown error')})"
                                )
                            except:
                                pass
                
                elif action_id == "cancel_change" and confirmation_id in pending_confirmations:
                    # Cancel the change
                    pending_confirmations.pop(confirmation_id, None)
                    
                    if slack_client:
                        try:
                            slack_client.chat_update(
                                channel=channel,
                                ts=message_ts,
                                text="❌ Change cancelled.",
                                blocks=[
                                    {
                                        "type": "section",
                                        "text": {
                                            "type": "mrkdwn",
                                            "text": "❌ Change cancelled."
                                        }
                                    }
                                ]
                            )
                        except SlackApiError as e:
                            print(f"⚠️  Slack update error: {e.response['error']}")
        
        return jsonify({"status": "ok"})
    
    @app.route("/webhooks/cms-update", methods=["POST"])
    def handle_cms_webhook():
        """Handle CMS update webhooks (from Payload afterChange hooks)"""
        try:
            data = request.json
            # Trigger deploy and notify Slack
            success = payload_webhook_handler(data)
            return jsonify({"status": "ok", "deploy_triggered": success})
        except Exception as e:
            print(f"❌ Webhook error: {e}")
            return jsonify({"status": "error", "message": str(e)}), 500
    
    return app


if __name__ == "__main__":
    port = int(os.getenv("PORT", 3001))
    debug = os.getenv("FLASK_DEBUG", "true").lower() == "true"
    
    print("=" * 60)
    print("           VoiceCraft Slack Bot Server")
    print("=" * 60)
    print()
    print("  Endpoints:")
    print(f"  - Health:      http://localhost:{port}/")
    print(f"  - Events:      http://localhost:{port}/slack/events")
    print(f"  - Commands:    http://localhost:{port}/slack/commands")
    print(f"  - Interactive: http://localhost:{port}/slack/interactive")
    print()
    print("  For public access, use ngrok:")
    print(f"  $ ngrok http {port}")
    print()
    print("=" * 60)
    
    app = create_app()
    app.run(host="0.0.0.0", port=port, debug=debug)
