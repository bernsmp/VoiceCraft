"""
Deploy Webhook Integration

Triggers Vercel deployments after CMS updates and notifies Slack of deploy status.

Usage:
    from integrations.deploy_webhook import trigger_deploy_and_notify

    trigger_deploy_and_notify(
        slack_channel='#website-updates',
        user_id='U12345'
    )
"""

import os
import requests
from typing import Optional


def trigger_vercel_deploy(deploy_hook_url: Optional[str] = None) -> bool:
    """
    Trigger Vercel deployment via deploy hook.
    
    Args:
        deploy_hook_url: Vercel deploy hook URL (or from VERCEL_DEPLOY_HOOK_URL env)
    
    Returns:
        True if deploy triggered successfully, False otherwise
    """
    hook_url = deploy_hook_url or os.getenv('VERCEL_DEPLOY_HOOK_URL')
    
    if not hook_url:
        print("⚠️  VERCEL_DEPLOY_HOOK_URL not set, skipping deploy trigger")
        return False
    
    try:
        response = requests.post(hook_url, timeout=10)
        if response.ok:
            print("✅ Vercel deploy triggered")
            return True
        else:
            print(f"❌ Deploy trigger failed: {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"❌ Deploy trigger error: {e}")
        return False


def notify_slack_deploy_status(
    status: str,
    channel: str,
    user_id: Optional[str] = None,
    details: Optional[str] = None
) -> bool:
    """
    Notify Slack of deploy status.
    
    Args:
        status: One of 'started', 'success', 'failed'
        channel: Slack channel ID
        user_id: User who triggered the change (optional)
        details: Additional details to include
    
    Returns:
        True if notification sent, False otherwise
    """
    slack_token = os.getenv('SLACK_BOT_TOKEN')
    if not slack_token:
        print("⚠️  SLACK_BOT_TOKEN not set, skipping notification")
        return False
    
    try:
        from slack_sdk import WebClient
        client = WebClient(token=slack_token)
        
        emoji_map = {
            'started': '🚀',
            'success': '✅',
            'failed': '❌'
        }
        emoji = emoji_map.get(status, '📦')
        
        message_map = {
            'started': 'Deploy started for louiebernstein.com',
            'success': 'Deploy completed successfully!',
            'failed': 'Deploy failed'
        }
        message = message_map.get(status, 'Deploy status update')
        
        text = f"{emoji} {message}"
        if details:
            text += f"\n{details}"
        
        if user_id:
            text = f"<@{user_id}> {text}"
        
        client.chat_postMessage(
            channel=channel,
            text=text
        )
        return True
    except Exception as e:
        print(f"❌ Slack notification error: {e}")
        return False


def trigger_deploy_and_notify(
    slack_channel: Optional[str] = None,
    user_id: Optional[str] = None
) -> bool:
    """
    Trigger Vercel deploy and notify Slack.
    
    Args:
        slack_channel: Slack channel ID (or from SLACK_DEPLOY_CHANNEL env)
        user_id: User who triggered the change
    
    Returns:
        True if deploy triggered successfully
    """
    channel = slack_channel or os.getenv('SLACK_DEPLOY_CHANNEL', '#website-updates')
    
    # Notify deploy started
    notify_slack_deploy_status('started', channel, user_id)
    
    # Trigger deploy
    success = trigger_vercel_deploy()
    
    if success:
        # Notify success
        notify_slack_deploy_status(
            'success',
            channel,
            user_id,
            details="Changes will be live in ~2 minutes"
        )
    else:
        # Notify failure
        notify_slack_deploy_status(
            'failed',
            channel,
            user_id,
            details="Check deploy logs for details"
        )
    
    return success


# Optional: Payload CMS webhook handler (for integration with Payload hooks)
def payload_webhook_handler(data: dict) -> bool:
    """
    Handle Payload CMS webhook for globals.site-settings updates.
    
    Add this to Payload config:
    ```js
    globals: [{
      slug: 'site-settings',
      hooks: {
        afterChange: [
          async ({ doc, req }) => {
            // Call this webhook
            await fetch('https://your-bot.railway.app/webhooks/cms-update', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ collection: 'site-settings', doc })
            });
          }
        ]
      }
    }]
    ```
    
    Args:
        data: Webhook payload from Payload
    
    Returns:
        True if deploy triggered
    """
    collection = data.get('collection')
    
    if collection == 'site-settings':
        print(f"📦 CMS update detected for {collection}, triggering deploy...")
        return trigger_deploy_and_notify()
    
    return False
