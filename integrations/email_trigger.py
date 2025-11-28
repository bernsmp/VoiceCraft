"""
Email Integration - Trigger workflow from email

Send email with topic → Get content back
"""

import os
import re
from typing import Dict
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.workflow_automation import ContentWorkflow


class EmailContentTrigger:
    """
    Process emails and trigger content workflow
    
    Usage:
        Send email to: content@yourdomain.com
        Subject: [CONTENT] How AI is changing expertise
        Body: (optional details)
        
        Or use special format:
        Subject: [VOICE-NOTE] Article idea
        Body: [paste transcript]
    """
    
    def __init__(self, profile_name: str = "Max Bernstein"):
        self.workflow = ContentWorkflow(profile_name)
    
    def process_email(
        self,
        subject: str,
        body: str,
        from_email: str
    ) -> Dict:
        """Process email and trigger workflow"""
        
        # Parse email type from subject
        if "[VOICE-NOTE]" in subject.upper():
            input_type = "voice_note"
            input_text = body
        elif "[BULLETS]" in subject.upper():
            input_type = "bullet_points"
            input_text = body
        else:
            input_type = "topic"
            # Extract topic from subject (remove [CONTENT] prefix)
            input_text = re.sub(r'\[.*?\]', '', subject).strip()
            if body:
                input_text += "\n\n" + body
        
        # Process workflow
        result = self.workflow.process_input(
            input_text=input_text,
            input_type=input_type,
            auto_humanize=True,
            auto_publish=False
        )
        
        # Return email response
        return {
            "to": from_email,
            "subject": f"Re: {subject} - Content Ready",
            "body": f"""
Your content has been generated!

Topic: {input_text[:100]}...

Content saved to: {result['output_path']}

Preview:
{result['final_content'][:500]}...

Full content available at: {result['output_path']}
            """,
            "attachments": [result['output_path']]
        }

