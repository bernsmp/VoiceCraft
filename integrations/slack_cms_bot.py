"""
Standalone Slack Bot for Website CMS Editing
No ML dependencies - just website editing via Payload CMS
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, str(Path(__file__).parent.parent))

from flask import Flask, request, jsonify
import json
import hmac
import hashlib
import time

from integrations.cms_integration import WebsiteEditor

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
    """Create Flask app for Slack bot"""
    app = Flask(__name__)
    editor = WebsiteEditor("louie")
    
    slack_token = os.getenv('SLACK_BOT_TOKEN')
    slack_client = WebClient(token=slack_token) if slack_token and SLACK_SDK_AVAILABLE else None
    
    pending_confirmations = {}
    
    @app.before_request
    def verify_request():
        """Verify Slack request signature"""
        if request.path.startswith("/slack"):
            timestamp = request.headers.get("X-Slack-Request-Timestamp", "")
            signature = request.headers.get("X-Slack-Signature", "")
            
            if abs(time.time() - int(timestamp or 0)) > 60 * 5:
                return jsonify({"error": "Invalid timestamp"}), 403
            
            if not verify_slack_signature(
                request.get_data(as_text=True),
                timestamp,
                signature
            ):
                return jsonify({"error": "Invalid signature"}), 403
    
    @app.route("/", methods=["GET"])
    def health():
        """Health check"""
        return jsonify({
            "status": "healthy",
            "service": "Louie Website CMS Bot",
            "version": "1.0.0"
        })
    
    @app.route("/slack/events", methods=["POST"])
    def handle_events():
        """Handle Slack Events API"""
        data = request.json
        
        if data.get("type") == "url_verification":
            return jsonify({"challenge": data.get("challenge")})
        
        event = data.get("event", {})
        
        if event.get("bot_id") or event.get("subtype") == "message_changed":
            return jsonify({"status": "ok"})
        
        message = event.get("text", "")
        user = event.get("user", "")
        channel = event.get("channel", "")
        thread_ts = event.get("ts")
        
        # Debug logging
        print(f"📩 Received message: '{message}' from user: {user} in channel: {channel}")
        print(f"🔍 Is website edit? {_is_website_edit(message) if message else False}")
        
        if message and _is_website_edit(message):
            result = editor.process_command(message)
            
            if slack_client:
                try:
                    if result.get("success"):
                        # Show preview with confirmation
                        confirmation_id = f"{user}_{channel}_{int(time.time())}"
                        pending_confirmations[confirmation_id] = {
                            'result': result,
                            'user': user,
                            'channel': channel,
                            'command': message
                        }
                        
                        blocks = [
                            {
                                "type": "section",
                                "text": {
                                    "type": "mrkdwn",
                                    "text": f"*🔍 Preview Change*\n\n*Field:* {result.get('field')}\n*New Value:* {result.get('new_value')}\n*Previous:* {result.get('old_value')}"
                                }
                            },
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
                            text="Preview change",
                            blocks=blocks
                        )
                    else:
                        slack_client.chat_postMessage(
                            channel=channel,
                            thread_ts=thread_ts,
                            text=f"❌ {result.get('message', 'Failed')}"
                        )
                except SlackApiError as e:
                    print(f"⚠️  Slack API error: {e.response['error']}")
            else:
                print(f"Response: {json.dumps(result, indent=2)}")
        
        return jsonify({"status": "ok"})
    
    @app.route("/slack/interactive", methods=["POST"])
    def handle_interactive():
        """Handle button clicks"""
        payload = json.loads(request.form.get("payload", "{}"))
        
        user = payload.get("user", {}).get("id")
        channel = payload.get("channel", {}).get("id")
        message_ts = payload.get("message", {}).get("ts")
        
        actions = payload.get("actions", [])
        for action in actions:
            action_id = action.get("action_id")
            confirmation_id = action.get("value")
            
            if action_id == "confirm_change" and confirmation_id in pending_confirmations:
                conf = pending_confirmations.pop(confirmation_id)
                result = conf['result']
                
                if slack_client:
                    try:
                        slack_client.chat_update(
                            channel=channel,
                            ts=message_ts,
                            text="✅ Change applied!",
                            blocks=[{
                                "type": "section",
                                "text": {
                                    "type": "mrkdwn",
                                    "text": f"✅ *Change Applied!*\n\n*Field:* {result.get('field')}\n*New Value:* {result.get('new_value')}"
                                }
                            }]
                        )
                    except SlackApiError as e:
                        print(f"⚠️  Slack update error: {e.response['error']}")
            
            elif action_id == "cancel_change" and confirmation_id in pending_confirmations:
                pending_confirmations.pop(confirmation_id, None)
                
                if slack_client:
                    try:
                        slack_client.chat_update(
                            channel=channel,
                            ts=message_ts,
                            text="❌ Change cancelled.",
                            blocks=[{
                                "type": "section",
                                "text": {"type": "mrkdwn", "text": "❌ Change cancelled."}
                            }]
                        )
                    except SlackApiError as e:
                        print(f"⚠️  Slack update error: {e.response['error']}")
        
        return jsonify({"status": "ok"})
    
    def _is_website_edit(message: str) -> bool:
        """Check if message is a website edit command"""
        triggers = [
            "change", "update", "set", "edit", "modify",
            "headline", "tagline", "description", "email", "phone"
        ]
        message_lower = message.lower()
        return any(trigger in message_lower for trigger in triggers)
    
    return app


if __name__ == "__main__":
    port = int(os.getenv("PORT", 3001))
    
    print(f"""
╔═══════════════════════════════════════════════╗
║   Louie Bernstein Website CMS Bot             ║
║   Listening on port {port}                      ║
╚═══════════════════════════════════════════════╝
""")
    
    app = create_app()
    app.run(host="0.0.0.0", port=port, debug=False)
