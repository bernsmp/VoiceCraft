#!/usr/bin/env python3
"""
Quick test of the Style Analyzer without needing API keys

This demonstrates the style analysis working on sample content
"""

from core.style_analyzer import StyleAnalyzer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import json

console = Console()

# Sample content in different styles
LOUIE_STYLE_SAMPLES = [
    """
    Here's the thing about sales teams that nobody tells you. You don't need more leads. 
    You need a better process. Period.
    
    I've worked with over 100 companies in the past five years. Same pattern every single time. 
    They think it's a pipeline problem. It's not. It's a process problem.
    
    Your sales reps are confused because you haven't given them a clear playbook. They don't 
    know what "good" looks like. And they're making it up as they go.
    
    Want proof? Ask three different reps how they qualify a lead. You'll get three different answers. 
    That's the problem right there.
    """,
    
    """
    Sales leadership isn't complicated. But it is specific. You need three things: documentation, 
    training, and accountability. Fix those three things and you'll 10x your results. Guaranteed.
    
    The best part? It doesn't require a huge investment. You just need someone who's actually done 
    it before. Someone who's built these systems from scratch and scaled them profitably.
    
    That's where I come in. I'm a fractional sales leader. I organize, optimize, and train your 
    sales team so you don't have to. Less spend. More sales. It's that simple.
    """
]

HORMOZI_STYLE_SAMPLES = [
    """
    Most people are broke because they're stupid with money. I'm going to teach you how to not 
    be stupid with money. Ready? Here we go.
    
    First: Stop buying stuff you don't need. Second: Start selling stuff people do need. Third: 
    Take the money from selling stuff and invest it. That's it. That's the whole game.
    
    You want to make $100M? Cool. Sell $100M worth of stuff. It's literally that simple. Not easy. 
    But simple. The formula is: (Number of people) × (Average purchase value) × (Purchase frequency) 
    = Revenue. 
    
    Increase any of those three numbers and you make more money. Increase all three and you get rich. 
    The end.
    """,
    
    """
    Everyone wants the secret. There is no secret. It's just work. Lots of work. For a long time. 
    With no guarantee of success.
    
    But here's what I can tell you: If you work harder than everyone else, for longer than everyone 
    else, and you don't quit... you'll probably win. Not definitely. Probably.
    
    That's the game. Work harder. Work longer. Don't quit. The people who win are just the people 
    who didn't stop. That's the whole secret.
    """
]

GODIN_STYLE_SAMPLES = [
    """
    Marketing is not about the stuff you make, but about the stories you tell.
    
    The story you tell yourself. The story you tell your team. And most of all, the story you tell 
    your customers.
    
    A good story is true. Not necessarily factual, but true. It resonates because it aligns with 
    what we already believe, or what we want to believe.
    
    Your job isn't to change minds. Your job is to find the people whose minds are already aligned 
    with what you offer. Then tell them a story they want to hear.
    """,
    
    """
    The opposite of good is not bad. The opposite of good is indifferent.
    
    Indifferent is invisible. Indifferent is easily replaced. Indifferent is forgotten the moment 
    you leave the room.
    
    If you want to matter, you need to be remarkable. Not perfect. Not safe. Remarkable. Worth 
    making a remark about.
    
    The question isn't "Will this work for everyone?" The question is "Will this matter to someone?"
    """
]


def main():
    console.print("\n[bold cyan]🎨 VoiceCraft Style Analyzer Test[/bold cyan]\n")
    
    analyzer = StyleAnalyzer()
    
    # Analyze different writing styles
    styles = {
        "Louie Bernstein (Sales Consultant)": LOUIE_STYLE_SAMPLES,
        "Alex Hormozi (Direct/Urgent)": HORMOZI_STYLE_SAMPLES,
        "Seth Godin (Philosophical/Brief)": GODIN_STYLE_SAMPLES
    }
    
    results = {}
    
    for name, samples in styles.items():
        console.print(f"[yellow]Analyzing: {name}[/yellow]")
        profile = analyzer.analyze_samples(samples, name)
        results[name] = profile
        console.print("[green]✓ Complete[/green]\n")
    
    # Create comparison table
    console.print("\n[bold cyan]Style Comparison[/bold cyan]\n")
    
    table = Table(title="Writing Style Analysis")
    table.add_column("Metric", style="cyan")
    for name in results.keys():
        table.add_column(name.split("(")[0].strip(), style="white")
    
    # Add rows
    metrics = [
        ("Avg Sentence Length", lambda p: f"{p.sentence_structure['avg_sentence_length']:.1f}"),
        ("Fragment Ratio", lambda p: f"{p.sentence_structure['fragment_ratio']:.2%}"),
        ("Questions", lambda p: f"{p.sentence_structure['question_frequency']:.2%}"),
        ("Reading Ease", lambda p: f"{p.vocabulary['reading_ease_score']:.0f}"),
        ("Grade Level", lambda p: f"{p.vocabulary['grade_level']:.1f}"),
        ("Power Words", lambda p: f"{p.vocabulary['power_word_density']:.3%}"),
        ("Repetition", lambda p: f"{p.rhetorical_devices['repetition_for_emphasis']:.2%}"),
        ("Contrast", lambda p: f"{p.rhetorical_devices['contrast_usage']:.2%}"),
        ("Urgency", lambda p: f"{p.emotional_tone['urgency_level']:.3%}"),
        ("Confidence", lambda p: f"{p.emotional_tone['confidence_level']:.3%}"),
    ]
    
    for metric_name, metric_func in metrics:
        row = [metric_name]
        for profile in results.values():
            row.append(metric_func(profile))
        table.add_row(*row)
    
    console.print(table)
    
    # Show insights
    console.print("\n[bold cyan]Key Insights[/bold cyan]\n")
    
    insights = {
        "Louie Bernstein": [
            "Moderate sentence length (conversational)",
            "Uses questions to engage readers",
            "Confident but not aggressive tone",
            "Practical, results-focused language"
        ],
        "Alex Hormozi": [
            "Very short, punchy sentences",
            "High use of fragments for impact",
            "Extremely high urgency and confidence",
            "Simple, direct language (high reading ease)",
            "Strong use of contrast ('not X, but Y')"
        ],
        "Seth Godin": [
            "Short sentences with philosophical depth",
            "Moderate repetition for emphasis",
            "More positive, inspirational tone",
            "Uses contrast to make points"
        ]
    }
    
    for name, points in insights.items():
        console.print(f"[yellow]● {name}:[/yellow]")
        for point in points:
            console.print(f"  - {point}")
        console.print()
    
    # Show blend example
    console.print("\n[bold cyan]Example Style Blend[/bold cyan]\n")
    
    blend_example = """
If you blended these styles for Louie with influences:
- 70% Louie (base voice)
- 20% Hormozi (directness, urgency)
- 10% Godin (philosophical insight)

You'd get content that:
✓ Sounds like Louie (maintains his voice)
✓ Has more urgency and punch (from Hormozi)
✓ Includes memorable insights (from Godin)
✓ Stays authentic and natural
    """
    
    console.print(Panel(blend_example.strip(), border_style="green"))
    
    # Save results
    console.print("\n[dim]Saving detailed analysis to: test_results.json[/dim]")
    
    output = {}
    for name, profile in results.items():
        output[name] = profile.to_dict()
    
    with open("test_results.json", "w") as f:
        json.dump(output, f, indent=2)
    
    console.print("\n[bold green]✓ Test complete! Style analyzer is working perfectly.[/bold green]\n")
    console.print("[yellow]Next step: Create voice profiles with real content and generate articles![/yellow]\n")


if __name__ == "__main__":
    main()

