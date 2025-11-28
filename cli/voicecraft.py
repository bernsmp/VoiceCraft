#!/usr/bin/env python3
"""
VoiceCraft CLI - Command-line interface for content generation

Usage:
    voicecraft profile create --name "Author Name" --samples "./samples/*.md"
    voicecraft generate --profile "Author" --input "Topic" --format article
    voicecraft style analyze --name "Writer" --samples "./samples/*.txt"
"""

import sys
import os
from pathlib import Path
import glob
import json

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import click
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress
    from rich import print as rprint
except ImportError:
    print("Installing required packages...")
    os.system(f"{sys.executable} -m pip install click rich")
    import click
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress
    from rich import print as rprint

from core.style_analyzer import StyleAnalyzer
from core.voice_profiler import VoiceProfiler
from core.style_blender import StyleBlender
from core.content_generator import ContentGenerator, GenerationConfig
from core.prompt_fusion_generator import PromptFusionGenerator
from core.prompt_library import get_prompt_library

console = Console()


@click.group()
@click.version_option(version="0.1.0")
@click.option("--yes", "-y", is_flag=True, help="Skip all confirmation prompts (auto-yes)")
@click.pass_context
def cli(ctx, yes):
    """🎨 VoiceCraft - AI Content Generation with Style Fusion"""
    # Store yes flag in context for all commands
    ctx.ensure_object(dict)
    ctx.obj['yes'] = yes or os.getenv('AUTO_YES') == '1'


@cli.group()
def profile():
    """Manage voice profiles"""
    pass


@profile.command("create")
@click.option("--name", required=True, help="Profile name")
@click.option("--samples", required=True, help="Path to sample files (glob pattern)")
@click.option("--description", help="Profile description")
@click.option("--tags", help="Comma-separated tags")
@click.pass_context
def create_profile(ctx, name, samples, description, tags):
    """Create a new voice profile from content samples"""
    console.print(f"\n[bold cyan]Creating voice profile for: {name}[/bold cyan]\n")
    
    # Load samples
    sample_files = glob.glob(samples)
    if not sample_files:
        console.print(f"[red]No files found matching: {samples}[/red]")
        return
    
    console.print(f"Found {len(sample_files)} sample file(s)")
    
    # Read content
    content_samples = []
    with Progress() as progress:
        task = progress.add_task("[cyan]Reading samples...", total=len(sample_files))
        
        for file_path in sample_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    content_samples.append(content)
                    progress.update(task, advance=1)
            except Exception as e:
                console.print(f"[yellow]Warning: Could not read {file_path}: {e}[/yellow]")
    
    if not content_samples:
        console.print("[red]No valid content found[/red]")
        return
    
    # Create profile
    profiler = VoiceProfiler()
    tag_list = tags.split(",") if tags else None
    
    with console.status("[bold green]Analyzing writing style..."):
        profile = profiler.create_profile(
            name=name,
            content_samples=content_samples,
            description=description,
            tags=tag_list
        )
    
    # Display results
    console.print("\n[bold green]✓ Profile created successfully![/bold green]\n")
    
    style = profile["style"]
    
    # Create results table
    table = Table(title=f"Voice Profile: {name}")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Sample Count", str(profile["samples"]["count"]))
    table.add_row("Total Words", f"{style['total_words']:,}")
    table.add_row("Avg Sentence Length", f"{style['sentence_structure']['avg_sentence_length']:.1f} words")
    table.add_row("Reading Ease", f"{style['vocabulary']['reading_ease_score']:.0f}")
    table.add_row("Grade Level", f"{style['vocabulary']['grade_level']:.1f}")
    
    console.print(table)
    console.print(f"\n[dim]Profile saved to: data/voices/{name.lower().replace(' ', '_')}.json[/dim]\n")


@profile.command("list")
def list_profiles():
    """List all available voice profiles"""
    profiler = VoiceProfiler()
    profiles = profiler.list_profiles()
    
    if not profiles:
        console.print("[yellow]No voice profiles found. Create one with 'voicecraft profile create'[/yellow]")
        return
    
    table = Table(title="Available Voice Profiles")
    table.add_column("Name", style="cyan")
    table.add_column("Description", style="white")
    table.add_column("Samples", style="green")
    table.add_column("Tags", style="yellow")
    
    for profile in profiles:
        table.add_row(
            profile["name"],
            profile.get("description", "")[:50],
            str(profile["sample_count"]),
            ", ".join(profile.get("tags", []))
        )
    
    console.print("\n")
    console.print(table)
    console.print("\n")


@profile.command("show")
@click.argument("name")
def show_profile(name):
    """Show detailed information about a profile"""
    profiler = VoiceProfiler()
    profile = profiler.load_profile(name)
    
    if not profile:
        console.print(f"[red]Profile '{name}' not found[/red]")
        return
    
    console.print(f"\n[bold cyan]Voice Profile: {name}[/bold cyan]\n")
    console.print(Panel(json.dumps(profile, indent=2), title="Complete Profile"))


@cli.group()
def generate():
    """Generate content with style fusion"""
    pass


@generate.command("fusion")
@click.option("--profile", required=True, help="Base voice profile name")
@click.option("--topic", required=True, help="What to write about")
@click.option("--writers", required=True, help="Writer prompts to blend (name:weight,name:weight)")
@click.option("--length", default=1200, help="Target word count")
@click.option("--output", help="Output file path (optional)")
@click.option("--format", default="article", help="Output format (article, linkedin, etc.)")
@click.option("--model", default="claude-haiku-4-5-20251001", help="AI model to use")
def generate_fusion(profile, topic, writers, length, output, format, model):
    """Generate content using your voice + writer prompts (THE UNIQUE FEATURE)"""
    console.print(f"\n[bold cyan]🎨 Style Fusion Generation[/bold cyan]\n")
    
    # Check prompt library
    library = get_prompt_library()
    available_writers = library.list_writers()
    
    if not available_writers:
        console.print("[red]No writer prompts found![/red]")
        console.print("[yellow]Add prompts to: ./writing prompts/[/yellow]")
        return
    
    # Parse writer influences
    writer_influences = []
    for writer_str in writers.split(","):
        try:
            name, weight = writer_str.split(":")
            # Try to match writer name
            matched_writer = None
            for aw in available_writers:
                if name.lower() in aw.lower() or aw.lower() in name.lower():
                    matched_writer = aw
                    break
            
            if matched_writer:
                writer_influences.append((matched_writer, float(weight)))
                console.print(f"[green]✓[/green] Using {matched_writer} ({float(weight)*100:.0f}%)")
            else:
                console.print(f"[yellow]⚠ Writer '{name}' not found. Available: {', '.join(available_writers)}[/yellow]")
        except:
            console.print(f"[yellow]⚠ Invalid format '{writer_str}'. Use: name:weight[/yellow]")
    
    if not writer_influences:
        console.print("[red]No valid writer influences specified[/red]")
        return
    
    # Generate
    try:
        generator = PromptFusionGenerator(profile)
        
        with console.status("[bold green]Generating with prompt fusion..."):
            result = generator.generate_with_prompt_fusion(
                topic=topic,
                writer_influences=writer_influences,
                output_format=format,
                target_length=length,
                model=model
            )
    except Exception as e:
        console.print(f"[red]Generation failed: {e}[/red]")
        import traceback
        traceback.print_exc()
        return
    
    # Display results
    console.print("\n[bold green]✓ Content generated with prompt fusion![/bold green]\n")
    
    # Show fusion details
    fusion = result["fusion"]
    info_table = Table(show_header=False, box=None)
    info_table.add_column("", style="cyan")
    info_table.add_column("", style="white")
    
    info_table.add_row("Base Voice:", fusion["base_voice"])
    info_table.add_row("Word Count:", str(result["word_count"]))
    info_table.add_row("Model:", result["model_used"])
    info_table.add_row("", "")
    
    influences_text = "\n".join([
        f"  • {inf['writer']} ({inf['weight']*100:.0f}%)"
        for inf in fusion["influences"]
    ])
    info_table.add_row("Style Influences:", influences_text)
    
    console.print(info_table)
    console.print()
    
    # Show content
    console.print(Panel(result["content"], title="Generated Content", border_style="green"))
    
    # Save to file if requested
    if output:
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            f.write(result["content"])
            f.write("\n\n---\n\n")
            f.write(f"Generated with VoiceCraft Prompt Fusion\n")
            f.write(f"Base Voice: {fusion['base_voice']}\n")
            f.write(f"Influences:\n")
            for inf in fusion["influences"]:
                f.write(f"  - {inf['writer']} ({inf['weight']*100:.0f}%)\n")
        
        console.print(f"\n[dim]Saved to: {output}[/dim]\n")


@generate.command("article")
@click.option("--profile", required=True, help="Base voice profile name")
@click.option("--topic", required=True, help="What to write about")
@click.option("--influences", help="Style influences (name:weight,name:weight)")
@click.option("--length", default=1000, help="Target word count")
@click.option("--output", help="Output file path (optional)")
@click.option("--model", default="gpt-4-turbo-preview", help="AI model to use")
def generate_article(profile, topic, influences, length, output, model):
    """Generate an article with optional style influences"""
    console.print(f"\n[bold cyan]Generating article...[/bold cyan]\n")
    
    # Load voice profile
    profiler = VoiceProfiler()
    voice_profile = profiler.load_profile(profile)
    
    if not voice_profile:
        console.print(f"[red]Profile '{profile}' not found[/red]")
        console.print("[yellow]Create one with: voicecraft profile create[/yellow]")
        return
    
    # Parse influences
    style_influences = []
    if influences:
        for influence_str in influences.split(","):
            try:
                name, weight = influence_str.split(":")
                influence_profile = profiler.load_profile(name.strip())
                if influence_profile:
                    style_influences.append((influence_profile, float(weight)))
                else:
                    console.print(f"[yellow]Warning: Profile '{name}' not found, skipping[/yellow]")
            except:
                console.print(f"[yellow]Warning: Invalid influence format '{influence_str}'[/yellow]")
    
    # Initialize generator
    generator = ContentGenerator(default_model=model)
    
    if not generator.openai_client and not generator.anthropic_client:
        console.print("[red]No AI API keys found![/red]")
        console.print("[yellow]Set OPENAI_API_KEY or ANTHROPIC_API_KEY environment variable[/yellow]")
        return
    
    # Generate content
    config = GenerationConfig(format="article", target_length=length)
    
    with console.status("[bold green]Generating content with AI..."):
        try:
            result = generator.generate(
                content_brief=topic,
                voice_profile=voice_profile,
                style_influences=style_influences if style_influences else None,
                config=config,
                model=model
            )
        except Exception as e:
            console.print(f"[red]Generation failed: {e}[/red]")
            return
    
    # Display results
    console.print("\n[bold green]✓ Content generated![/bold green]\n")
    
    # Show metadata
    metadata = result["metadata"]
    voice_match = result["voice_verification"]
    
    info_table = Table(show_header=False, box=None)
    info_table.add_column("", style="cyan")
    info_table.add_column("", style="white")
    
    info_table.add_row("Format:", metadata["format"])
    info_table.add_row("Word Count:", str(metadata["word_count"]))
    info_table.add_row("Style Blend:", metadata["style_blend"])
    info_table.add_row("Voice Match:", f"{voice_match['match_score']}%")
    info_table.add_row("Model:", metadata["model_used"])
    
    console.print(info_table)
    console.print()
    
    # Show content
    console.print(Panel(result["content"], title="Generated Content", border_style="green"))
    
    # Save to file if requested
    if output:
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            f.write(result["content"])
            f.write("\n\n---\n\n")
            f.write(f"Generated with VoiceCraft\n")
            f.write(f"Style: {metadata['style_blend']}\n")
            f.write(f"Voice Match: {voice_match['match_score']}%\n")
        
        console.print(f"\n[dim]Saved to: {output}[/dim]\n")


@cli.group()
def style():
    """Analyze and manage writing styles"""
    pass


@style.command("analyze")
@click.option("--name", required=True, help="Writer name")
@click.option("--samples", required=True, help="Path to sample files")
@click.option("--output", help="Output JSON file")
def analyze_style(name, samples, output):
    """Analyze writing style from samples"""
    console.print(f"\n[bold cyan]Analyzing style: {name}[/bold cyan]\n")
    
    # Load samples
    sample_files = glob.glob(samples)
    if not sample_files:
        console.print(f"[red]No files found matching: {samples}[/red]")
        return
    
    content_samples = []
    for file_path in sample_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content_samples.append(f.read())
    
    # Analyze
    analyzer = StyleAnalyzer()
    with console.status("[bold green]Analyzing..."):
        profile = analyzer.analyze_samples(content_samples, name)
    
    console.print("\n[bold green]✓ Analysis complete![/bold green]\n")
    console.print(Panel(profile.to_json(), title="Style Profile"))
    
    if output:
        with open(output, 'w') as f:
            f.write(profile.to_json())
        console.print(f"\n[dim]Saved to: {output}[/dim]\n")


@cli.command("humanize")
@click.option("--profile", default="Max Bernstein", help="Voice profile to use")
@click.option("--input", help="Text file to humanize")
@click.option("--text", help="Text to humanize (or use --input)")
@click.option("--output", help="Output file (optional)")
@click.option("--analysis", is_flag=True, help="Show analysis of changes")
@click.option("--model", default="gpt-4o", help="AI model to use")
def humanize_text(profile, input, text, output, analysis, model):
    """Humanize AI-generated text using your voice profile"""
    console.print(f"\n[bold cyan]Humanizing text with {profile}'s voice...[/bold cyan]\n")
    
    # Get text to humanize
    if input:
        with open(input, 'r') as f:
            text_to_humanize = f.read()
    elif text:
        text_to_humanize = text
    else:
        console.print("[red]Error: Provide --input file or --text string[/red]")
        return
    
    # Import humanizer
    try:
        from core.humanizer import Humanizer
    except ImportError:
        console.print("[red]Error: Could not import humanizer module[/red]")
        return
    
    # Initialize humanizer
    humanizer = Humanizer(profile_name=profile, model=model)
    
    # Humanize
    with console.status("[bold green]Humanizing..."):
        try:
            result = humanizer.humanize(text_to_humanize, show_analysis=analysis, model=model)
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            return
    
    # Display results
    console.print("\n[bold green]✓ Text humanized![/bold green]\n")
    
    if analysis and "analysis" in result:
        console.print("[bold yellow]Analysis:[/bold yellow]")
        console.print(Panel(result["analysis"], border_style="yellow"))
        console.print()
    
    console.print("[bold cyan]Humanized Text:[/bold cyan]")
    console.print(Panel(result["humanized"], border_style="green"))
    
    # Save if requested
    if output:
        with open(output, 'w') as f:
            f.write(result["humanized"])
        console.print(f"\n[dim]Saved to: {output}[/dim]\n")


@cli.group()
def workflow():
    """🚀 Content Workflow - Input from anywhere → World-class content"""
    pass


@workflow.command("create")
@click.argument("input_text")
@click.option("--profile", default="Max Bernstein", help="Voice profile")
@click.option("--type", "input_type", default="topic", type=click.Choice(["topic", "voice_note", "bullet_points"]))
@click.option("--format", "output_format", default="article", type=click.Choice(["article", "linkedin", "twitter", "faq"]))
@click.option("--length", default=1200, help="Target word count")
@click.option("--no-humanize", is_flag=True, help="Skip humanization")
@click.option("--output", help="Output file path")
def workflow_create(input_text, profile, input_type, output_format, length, no_humanize, output):
    """Create content from input (topic, voice note, or bullet points)"""
    try:
        from core.workflow_automation import ContentWorkflow
    except ImportError:
        console.print("[red]Error: workflow_automation module not found[/red]")
        return
    
    console.print(f"\n[bold cyan]🚀 Content Workflow[/bold cyan]\n")
    
    try:
        workflow = ContentWorkflow(profile)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        return
    
    with console.status("[bold green]Processing..."):
        result = workflow.process_input(
            input_text=input_text,
            input_type=input_type,
            output_format=output_format,
            target_length=length,
            auto_humanize=not no_humanize,
            auto_publish=False
        )
    
    console.print("\n[bold green]✅ Content created![/bold green]\n")
    console.print(Panel(result["final_content"], title="Generated Content", border_style="green"))
    console.print(f"\n[dim]Saved to: {result['output_path']}[/dim]\n")
    
    if output:
        with open(output, 'w') as f:
            f.write(result["final_content"])
        console.print(f"[dim]Also saved to: {output}[/dim]\n")


@workflow.command("quick")
@click.argument("topic")
@click.option("--profile", default="Max Bernstein")
def workflow_quick(topic, profile):
    """Quick workflow: Topic → Content (one command)"""
    try:
        from core.workflow_automation import quick_content
    except ImportError:
        console.print("[red]Error: workflow_automation module not found[/red]")
        return
    
    console.print(f"\n[bold cyan]⚡ Quick Content[/bold cyan]\n")
    
    content = quick_content(topic, profile_name=profile)
    
    console.print(Panel(content, title="Content", border_style="green"))
    console.print()


@cli.command()
def examples():
    """Show usage examples"""
    examples_text = """
[bold cyan]VoiceCraft Usage Examples[/bold cyan]

[yellow]1. Create a voice profile:[/yellow]
   voicecraft profile create --name "Louie Bernstein" --samples "./samples/louie/*.md"

[yellow]2. List all profiles:[/yellow]
   voicecraft profile list

[yellow]3. Generate an article:[/yellow]
   voicecraft generate article --profile "Louie Bernstein" --topic "Sales team optimization tips"

[yellow]4. Generate with style influences:[/yellow]
   voicecraft generate article \\
     --profile "Louie Bernstein" \\
     --topic "Building a sales process" \\
     --influences "Alex Hormozi:0.3,Seth Godin:0.2" \\
     --length 1200

[yellow]5. Generate with PROMPT FUSION (your voice + writer prompts):[/yellow]
   voicecraft generate fusion \\
     --profile "Max Bernstein" \\
     --topic "How to make expertise visible" \\
     --writers "James Clear:0.3,Paul Graham:0.2" \\
     --length 1200 \\
     --output "./output/fusion-article.md"
   
   # Available writers: James Clear, Malcolm Gladwell, Paul Graham, 
   #                    Morgan Housel, Tim Urban

[yellow]6. Analyze a writer's style:[/yellow]
   voicecraft style analyze --name "Alex Hormozi" --samples "./samples/hormozi/*.txt" \\
     --output "./styles/profiles/alex_hormozi.json"

[yellow]7. Generate and save to file:[/yellow]
   voicecraft generate article \\
     --profile "Louie Bernstein" \\
     --topic "Fractional sales leadership" \\
     --output "./output/article.md"

[yellow]8. Humanize AI-generated text:[/yellow]
   voicecraft humanize \\
     --profile "Max Bernstein" \\
     --text "AI-generated text here..." \\
     --output "./output/humanized.md"

   # Or from file
   voicecraft humanize \\
     --profile "Max Bernstein" \\
     --input "./ai-draft.md" \\
     --output "./humanized.md" \\
     --analysis  # Show what changed
"""
    console.print(Panel(examples_text, title="Examples", border_style="cyan"))


if __name__ == "__main__":
    cli()

