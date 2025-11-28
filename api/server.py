"""
VoiceCraft API Server - External Input System

Enables content creation from anywhere:
- Mobile apps
- Voice notes
- Webhooks
- Email integrations
- Third-party services

The real value: Input from anywhere → World-class content → Auto-published
"""

import os
import json
from pathlib import Path
from typing import Optional, Dict, List
from datetime import datetime

from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent / '.env.local'
if env_path.exists():
    load_dotenv(env_path)

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.workflow_automation import ContentWorkflow, quick_content


# API Models
class ContentRequest(BaseModel):
    """Request model for content generation"""
    input_text: str = Field(..., description="Topic, voice note transcript, or bullet points")
    profile_name: Optional[str] = Field(None, description="Voice profile name (defaults to env or 'Max Bernstein')")
    input_type: Optional[str] = Field(None, description="Auto-detect if not provided: 'topic', 'voice_note', 'bullet_points', 'whatsapp'")
    output_format: Optional[str] = Field(None, description="Auto-detect if not provided: 'article', 'linkedin', 'twitter', 'faq', 'email'")
    target_length: Optional[int] = Field(1200, description="Target word count")
    auto_humanize: bool = Field(True, description="Automatically humanize output")
    auto_publish: bool = Field(False, description="Automatically publish after generation")
    publish_config: Optional[Dict] = Field(None, description="Publishing configuration (GitHub, WordPress, etc.)")
    style_influences: Optional[List[Dict]] = Field(None, description="Style blend influences: [{'name': 'Hormozi', 'weight': 30}]")


class WebhookRequest(BaseModel):
    """Webhook request model"""
    event: str = Field(..., description="Event type: 'content_request', 'voice_note', 'idea'")
    data: Dict = Field(..., description="Event data")
    source: Optional[str] = Field(None, description="Source system (e.g., 'mobile_app', 'zapier')")


class VoiceNoteRequest(BaseModel):
    """Voice note request model"""
    transcript: str = Field(..., description="Voice note transcript")
    profile_name: Optional[str] = Field(None, description="Voice profile name")
    output_format: Optional[str] = Field(None, description="Output format (auto-detect if not provided)")
    auto_publish: bool = Field(False, description="Auto-publish after generation")
    publish_config: Optional[Dict] = Field(None, description="Publishing configuration")


class QuickContentRequest(BaseModel):
    """Quick content request (minimal input)"""
    input_text: str = Field(..., description="Topic or input text")
    profile_name: Optional[str] = Field(None, description="Voice profile name")


# Initialize FastAPI app
app = FastAPI(
    title="VoiceCraft API",
    description="AI-powered content generation with Style Fusion Technology",
    version="1.0.0"
)

# CORS middleware for mobile/web access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check
@app.get("/")
async def root():
    """API health check"""
    return {
        "status": "online",
        "service": "VoiceCraft API",
        "version": "1.0.0",
        "endpoints": {
            "content": "/api/v1/content",
            "quick": "/api/v1/quick",
            "voice-note": "/api/v1/voice-note",
            "webhook": "/api/v1/webhook"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


# Main content generation endpoint
@app.post("/api/v1/content")
async def create_content(request: ContentRequest):
    """
    Generate content from any input type
    
    Supports:
    - Topics: "How AI is changing expertise"
    - Voice notes: Transcript text
    - Bullet points: "- Point 1\n- Point 2"
    - WhatsApp: Formatted chat export
    
    Auto-detects input type and output format if not specified.
    """
    try:
        # Get profile name (from request, env, or default)
        profile_name = request.profile_name or os.getenv('VOICECRAFT_PROFILE', 'Max Bernstein')
        
        # Initialize workflow
        workflow = ContentWorkflow(profile_name)
        
        # Convert style_influences from List[Dict] to List[tuple] if provided
        style_influences = None
        if request.style_influences:
            style_influences = [
                (inf['name'], inf['weight']) 
                for inf in request.style_influences
            ]
        
        # Process input
        result = workflow.process_input(
            input_text=request.input_text,
            input_type=request.input_type,
            output_format=request.output_format,
            target_length=request.target_length,
            style_influences=style_influences,
            auto_humanize=request.auto_humanize,
            auto_publish=request.auto_publish,
            publish_config=request.publish_config,
            auto_yes=True  # Skip prompts in API mode
        )
        
        return {
            "success": True,
            "content": result.get("final_content", ""),
            "metadata": {
                "input_type": result.get("input_type"),
                "output_format": result.get("output_format"),
                "output_path": str(result.get("output_path", "")),
                "publish_result": result.get("publish_result"),
                "timestamp": result.get("timestamp")
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Quick content endpoint (ultra-low friction)
@app.post("/api/v1/quick")
async def quick_content_endpoint(request: QuickContentRequest):
    """
    Quick content generation - minimal input, maximum automation
    
    Just send your topic/idea, get world-class content back.
    Perfect for mobile apps and quick integrations.
    """
    try:
        profile_name = request.profile_name or os.getenv('VOICECRAFT_PROFILE', 'Max Bernstein')
        
        # Use quick_content for maximum automation
        content = quick_content(
            input_text=request.input_text,
            profile_name=profile_name,
            auto_yes=True
        )
        
        return {
            "success": True,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Voice note endpoint
@app.post("/api/v1/voice-note")
async def process_voice_note(request: VoiceNoteRequest):
    """
    Process voice note transcript into content
    
    Optimized for voice note inputs with automatic cleanup and formatting.
    """
    try:
        profile_name = request.profile_name or os.getenv('VOICECRAFT_PROFILE', 'Max Bernstein')
        
        workflow = ContentWorkflow(profile_name)
        
        result = workflow.process_input(
            input_text=request.transcript,
            input_type="voice_note",
            output_format=request.output_format,
            auto_humanize=True,
            auto_publish=request.auto_publish,
            publish_config=request.publish_config,
            auto_yes=True
        )
        
        return {
            "success": True,
            "content": result.get("final_content", ""),
            "metadata": {
                "output_format": result.get("output_format"),
                "output_path": str(result.get("output_path", "")),
                "publish_result": result.get("publish_result"),
                "timestamp": result.get("timestamp")
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Webhook endpoint for external integrations
@app.post("/api/v1/webhook")
async def webhook(request: WebhookRequest, x_api_key: Optional[str] = Header(None)):
    """
    Webhook endpoint for external integrations
    
    Supports:
    - Zapier
    - Make.com (Integromat)
    - Custom integrations
    - Mobile apps
    
    Requires API key in header: X-API-Key
    """
    # TODO: Add API key validation
    # if x_api_key != os.getenv('VOICECRAFT_API_KEY'):
    #     raise HTTPException(status_code=401, detail="Invalid API key")
    
    try:
        event_type = request.event
        data = request.data
        
        profile_name = data.get('profile_name') or os.getenv('VOICECRAFT_PROFILE', 'Max Bernstein')
        workflow = ContentWorkflow(profile_name)
        
        # Handle different event types
        if event_type == "content_request":
            input_text = data.get('input_text', '')
            result = workflow.process_input(
                input_text=input_text,
                input_type=data.get('input_type'),
                output_format=data.get('output_format'),
                auto_humanize=True,
                auto_publish=data.get('auto_publish', False),
                publish_config=data.get('publish_config'),
                auto_yes=True
            )
            
            return {
                "success": True,
                "event": event_type,
                "result": {
                    "content": result.get("final_content", ""),
                    "output_path": str(result.get("output_path", "")),
                    "publish_result": result.get("publish_result")
                }
            }
        
        elif event_type == "voice_note":
            transcript = data.get('transcript', '')
            result = workflow.process_input(
                input_text=transcript,
                input_type="voice_note",
                auto_humanize=True,
                auto_publish=data.get('auto_publish', False),
                publish_config=data.get('publish_config'),
                auto_yes=True
            )
            
            return {
                "success": True,
                "event": event_type,
                "result": {
                    "content": result.get("final_content", ""),
                    "output_path": str(result.get("output_path", ""))
                }
            }
        
        else:
            raise HTTPException(status_code=400, detail=f"Unknown event type: {event_type}")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# List available profiles
@app.get("/api/v1/profiles")
async def list_profiles():
    """List all available voice profiles"""
    try:
        from core.voice_profiler import VoiceProfiler
        
        profiler = VoiceProfiler()
        profiles = profiler.list_profiles()
        
        return {
            "success": True,
            "profiles": profiles
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

