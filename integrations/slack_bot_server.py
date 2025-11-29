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

# Lazy import to avoid blocking health checks
try:
    from integrations.slack_bot import SlackContentBot
    from integrations.deploy_webhook import trigger_deploy_and_notify, payload_webhook_handler
    SLACK_BOT_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Warning: Could not import SlackContentBot: {e}")
    SLACK_BOT_AVAILABLE = False
    SlackContentBot = None
    trigger_deploy_and_notify = None
    payload_webhook_handler = None

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
    # Lazy load bot to avoid import errors blocking health checks
    bot = None
    
    def get_bot():
        """Lazy load bot instance"""
        nonlocal bot
        if bot is None:
            if not SLACK_BOT_AVAILABLE or SlackContentBot is None:
                # Return a mock bot if imports failed
                class MockBot:
                    def process_slack_message(self, *args, **kwargs):
                        return {"text": "⚠️ Bot module not available. Check dependencies."}
                    def _do_site_edit(self, *args, **kwargs):
                        return {"success": False, "message": "Bot module not available"}
                bot = MockBot()
            else:
                try:
                    bot = SlackContentBot("Louie Bernstein")
                except Exception as e:
                    print(f"⚠️  Warning: Failed to initialize bot: {e}")
                    import traceback
                    traceback.print_exc()
                    # Return a mock bot that handles errors gracefully
                    class MockBot:
                        def process_slack_message(self, *args, **kwargs):
                            return {"text": f"⚠️ Bot initialization failed: {str(e)[:100]}. Check logs."}
                        def _do_site_edit(self, *args, **kwargs):
                            return {"success": False, "message": f"Bot initialization failed: {str(e)[:100]}"}
                    bot = MockBot()
        return bot
    
    # Initialize Slack WebClient for posting responses
    slack_token = os.getenv('SLACK_BOT_TOKEN')
    if not slack_token:
        print("⚠️  WARNING: SLACK_BOT_TOKEN not set. Bot will not be able to post messages.")
    elif not SLACK_SDK_AVAILABLE:
        print("⚠️  WARNING: slack-sdk not installed. Install with: pip install slack-sdk")
    
    slack_client = WebClient(token=slack_token) if slack_token and SLACK_SDK_AVAILABLE else None
    
    if slack_client:
        try:
            # Test the connection
            auth_test = slack_client.auth_test()
            print(f"✅ Slack bot connected: {auth_test.get('user', 'unknown')}")
        except Exception as e:
            print(f"⚠️  Slack connection test failed: {e}")
            slack_client = None
    
    # In-memory store for pending confirmations (production: use Redis)
    pending_confirmations = {}
    
    # Track processed events to prevent duplicates (Slack can retry events)
    processed_events = set()
    
    @app.before_request
    def verify_request():
        """Verify Slack request signature"""
        if request.path.startswith("/slack"):
            # Skip verification for interactive endpoint (handled separately)
            if request.path == "/slack/interactive":
                return None
            
            # Skip verification for URL verification challenge (no signature header)
            if request.path == "/slack/events" and request.method == "POST":
                signature = request.headers.get("X-Slack-Signature", "")
                # Challenge requests don't have signature header
                if not signature:
                    return None  # Skip signature check for challenge requests
            
            timestamp = request.headers.get("X-Slack-Request-Timestamp", "")
            signature = request.headers.get("X-Slack-Signature", "")
            
            # Skip verification if no signature (development mode or challenge)
            if not signature:
                return None
            
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
        """Health check endpoint - must always respond for Render health checks"""
        try:
            return jsonify({
                "status": "healthy",
                "service": "VoiceCraft Slack Bot",
                "version": "1.0.0",
            }), 200
        except Exception as e:
            # Even if JSON encoding fails, return a simple response
            return "OK", 200
    
    @app.route("/ ", methods=["GET"])  # Route with space - Flask decodes %20 to space
    def health_with_space():
        """Health check endpoint that handles Render's space-in-path issue"""
        try:
            return jsonify({
                "status": "healthy",
                "service": "VoiceCraft Slack Bot",
                "version": "1.0.0",
            }), 200
        except Exception as e:
            return "OK", 200
    
    @app.route("/healthz", methods=["GET"])
    def healthz():
        """Alternative health check endpoint (common convention)"""
        return "OK", 200
    
    @app.route("/slack/events", methods=["POST"])
    def handle_events():
        """Handle Slack Events API"""
        data = request.json
        
        # URL verification challenge - Slack requires plaintext response
        if data.get("type") == "url_verification":
            challenge = data.get("challenge", "")
            # Return plaintext challenge as Slack requires
            from flask import Response
            return Response(challenge, mimetype='text/plain', status=200)
        
        # Handle message events
        event = data.get("event", {})
        
        # Ignore bot messages and message_changed events
        if event.get("bot_id") or event.get("subtype") == "message_changed":
            return jsonify({"status": "ok"})
        
        # Deduplication: Check if we've already processed this event
        event_ts = event.get("ts")  # Unique timestamp for each event
        if event_ts and event_ts in processed_events:
            # Already processed, just acknowledge
            return jsonify({"status": "ok"})
        
        # Mark as processed (keep last 1000 events to prevent memory bloat)
        if event_ts:
            processed_events.add(event_ts)
            if len(processed_events) > 1000:
                # Remove oldest entries (simple cleanup - convert to list, remove first)
                oldest = min(processed_events)
                processed_events.remove(oldest)
        
        message = event.get("text", "")
        user = event.get("user", "")
        channel = event.get("channel", "")
        thread_ts = event.get("ts")  # For threading replies
        
        # Debug logging
        print(f"📩 Received event: user={user}, channel={channel}, message='{message[:50]}...'")
        
        # Only process if we have a message
        if not message:
            print("⚠️  No message text in event")
            return jsonify({"status": "ok"})
        
        try:
            # Process the message (lazy load bot if needed)
            result = get_bot().process_slack_message(message, user, channel, thread_ts)
            print(f"✅ Processed message, result keys: {list(result.keys()) if isinstance(result, dict) else 'not a dict'}")
            
            # Post response back to Slack
            if slack_client:
                try:
                    # If it's a website edit command, show confirmation first
                    if result.get('preview'):
                        confirmation_id = f"{user}_{channel}_{int(time.time())}"
                        pending_confirmations[confirmation_id] = {
                            'result': result,
                            'user': user,
                            'channel': channel,
                            'command': result.get('command')  # Store original command for re-execution
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
                        
                        response = slack_client.chat_postMessage(
                            channel=channel,
                            thread_ts=thread_ts,
                            text=result.get('text', 'Preview'),
                            blocks=blocks
                        )
                        print(f"✅ Posted preview message: {response.get('ts', 'no ts')}")
                    else:
                        # Post directly (non-edit commands or errors)
                        response = slack_client.chat_postMessage(
                            channel=channel,
                            thread_ts=thread_ts,
                            text=result.get('text', 'Response'),
                            blocks=result.get('blocks')
                        )
                        print(f"✅ Posted response message: {response.get('ts', 'no ts')}")
                except SlackApiError as e:
                    error_msg = e.response.get('error', 'unknown error') if hasattr(e, 'response') else str(e)
                    print(f"❌ Slack API error: {error_msg}")
                    # Try to send a simple error message
                    try:
                        slack_client.chat_postMessage(
                            channel=channel,
                            text=f"⚠️ Error: {error_msg}"
                        )
                    except:
                        pass
                except Exception as e:
                    print(f"❌ Unexpected error posting to Slack: {e}")
                    import traceback
                    traceback.print_exc()
            else:
                # Fallback: print to console
                print(f"⚠️  No Slack client available. Response would be: {json.dumps(result, indent=2)}")
        except Exception as e:
            print(f"❌ Error processing message: {e}")
            import traceback
            traceback.print_exc()
            # Try to send error to Slack if possible
            if slack_client:
                try:
                    slack_client.chat_postMessage(
                        channel=channel,
                        text=f"❌ Error processing your message: {str(e)[:200]}"
                    )
                except:
                    pass
        
        return jsonify({"status": "ok"})
    
    @app.route("/slack/commands", methods=["POST"])
    def handle_commands():
        """Handle Slack slash commands"""
        try:
            command = request.form.get("command", "")
            text = request.form.get("text", "")
            user_id = request.form.get("user_id", "")
            channel_id = request.form.get("channel_id", "")
            
            print(f"📩 Received command: {command} {text} from user {user_id}")
            
            # Combine command and text
            full_message = f"{command} {text}".strip()
            
            # Process the command (lazy load bot if needed)
            result = get_bot().process_slack_message(full_message, user_id, channel_id)
            
            print(f"✅ Processed command, returning response")
            
            # Return response (Slack will display this)
            return jsonify({
                "response_type": "in_channel",  # or "ephemeral" for private
                **result
            })
        except Exception as e:
            print(f"❌ Error handling command: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({
                "response_type": "ephemeral",
                "text": f"❌ Error: {str(e)[:200]}"
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
                    original_command = conf.get('command')
                    preview_result = conf.get('result')
                    
                    # Re-execute the command with preview_only=False to actually apply it
                    if original_command:
                        apply_result = get_bot()._do_site_edit(original_command, preview_only=False)
                    else:
                        apply_result = preview_result  # Fallback if no command stored
                    
                    if slack_client:
                        try:
                            # Update the original message to show it was applied
                            success_text = f"✅ Change applied! {apply_result.get('text', preview_result.get('message', 'Change applied!'))}"
                            blocks = apply_result.get('blocks', preview_result.get('blocks', [])) if isinstance(apply_result, dict) else preview_result.get('blocks', [])
                            
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
