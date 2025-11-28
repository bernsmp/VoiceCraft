#!/usr/bin/env python3
"""
Workflow CLI - The Real Product

Input from anywhere → World-class content
"""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent.parent / '.env.local'
if env_path.exists():
    load_dotenv(env_path)

sys.path.insert(0, str(Path(__file__).parent.parent))

import click
from rich.console import Console
from rich.panel import Panel

from core.workflow_automation import ContentWorkflow, quick_content

console = Console()


@click.group()
def workflow():
    """🚀 Content Workflow - Input from anywhere → World-class content"""
    pass


@workflow.command("create")
@click.argument("input_text")
@click.option("--profile", default="Max Bernstein", help="Voice profile")
@click.option("--type", "input_type", default=None, type=click.Choice(["topic", "voice_note", "bullet_points"]), help="Input type (auto-detected if not specified)")
@click.option("--format", "output_format", default=None, type=click.Choice(["article", "linkedin", "twitter", "faq", "email"]), help="Output format (auto-detected if not specified)")
@click.option("--length", default=1200, help="Target word count")
@click.option("--blend", help="Style influences (e.g., 'Hormozi:30,Godin:20')")
@click.option("--no-humanize", is_flag=True, help="Skip humanization")
@click.option("--publish", is_flag=True, help="Auto-publish after generation")
@click.option("--output", help="Output file path")
@click.option("--yes", "-y", is_flag=True, default=True, help="Skip all prompts (default: enabled)")
def create_content(input_text, profile, input_type, output_format, length, blend, no_humanize, publish, output, yes):
    """Create content from input - completely automatic with smart defaults"""
    
    # Check environment variable for auto-yes
    auto_yes = yes or os.getenv('AUTO_YES') == '1' or os.getenv('AUTO_YES', '1') == '1'
    
    if not auto_yes:
        console.print(f"\n[bold cyan]🚀 Content Workflow[/bold cyan]\n")
        console.print(f"Profile: {profile}")
        if input_type:
            console.print(f"Input Type: {input_type}")
        else:
            console.print(f"Input Type: [dim]auto-detecting...[/dim]")
        if output_format:
            console.print(f"Format: {output_format}")
        else:
            console.print(f"Format: [dim]auto-detecting...[/dim]")
        console.print()
    
    # Parse style influences
    style_influences = None
    if blend:
        # TODO: Parse and load influence profiles
        console.print(f"[yellow]Style blend: {blend}[/yellow]")
    
    # Initialize workflow
    try:
        workflow = ContentWorkflow(profile)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        return
    
    # Process input (silent if auto_yes)
    if auto_yes:
        result = workflow.process_input(
            input_text=input_text,
            input_type=input_type,
            output_format=output_format,
            target_length=length,
            style_influences=style_influences,
            auto_humanize=not no_humanize,
            auto_publish=publish,
            auto_yes=True
        )
    else:
        with console.status("[bold green]Processing..."):
            result = workflow.process_input(
                input_text=input_text,
                input_type=input_type,
                output_format=output_format,
                target_length=length,
                style_influences=style_influences,
                auto_humanize=not no_humanize,
                auto_publish=publish,
                auto_yes=False
            )
    
    # Display results (only if not silent)
    if not auto_yes:
        console.print("\n[bold green]✅ Content created![/bold green]\n")
        console.print(Panel(
            result["final_content"],
            title="Generated Content",
            border_style="green"
        ))
        console.print(f"\n[dim]Saved to: {result['output_path']}[/dim]\n")
    else:
        # Silent mode - just print file path
        print(result['output_path'])
    
    # Save to custom path if specified
    if output:
        with open(output, 'w') as f:
            f.write(result["final_content"])
        if not auto_yes:
            console.print(f"[dim]Also saved to: {output}[/dim]\n")


@workflow.command("quick")
@click.argument("topic")
@click.option("--profile", default="Max Bernstein")
@click.option("--yes", "-y", is_flag=True, default=True, help="Skip all prompts (default: enabled)")
def quick(topic, profile, yes):
    """Quick workflow: Topic → Content (completely automatic, no prompts)"""
    
    # Check environment variable for auto-yes
    auto_yes = yes or os.getenv('AUTO_YES') == '1' or os.getenv('AUTO_YES', '1') == '1'
    
    if not auto_yes:
        console.print(f"\n[bold cyan]⚡ Quick Content[/bold cyan]\n")
    
    content = quick_content(topic, profile_name=profile, auto_yes=auto_yes)
    
    if auto_yes:
        # Silent mode - just output content
        print(content)
    else:
        console.print(Panel(content, title="Content", border_style="green"))
        console.print()


if __name__ == "__main__":
    workflow()

