"""scaffold command — generate a new repo from a template."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt

from repoforge.core.generator import RepoGenerator
from repoforge.core.config import ScaffoldConfig
from repoforge.core.ai import generate_readme

scaffold_app = typer.Typer(help="Scaffold a new repository from a template.")
console = Console()


@scaffold_app.command("new")
def scaffold_new(
    name: str = typer.Argument(..., help="Repository name"),
    template: str = typer.Option("python-service", "--template", "-t", help="Template to use"),
    industry: str = typer.Option("fintech", "--industry", "-i", help="Target industry context"),
    description: Optional[str] = typer.Option(None, "--description", "-d", help="Repo description"),
    output_dir: Path = typer.Option(Path("."), "--output", "-o", help="Output directory"),
    ai_readme: bool = typer.Option(True, "--ai-readme/--no-ai-readme", help="Generate README with AI"),
    push: bool = typer.Option(False, "--push/--no-push", help="Create and push to GitHub"),
) -> None:
    """Scaffold a new production-ready repository."""
    if description is None:
        description = Prompt.ask(
            "[bold]Short description[/bold]",
            default=f"A {industry} engineering service",
        )

    config = ScaffoldConfig(
        name=name,
        template=template,
        industry=industry,
        description=description,
        output_dir=output_dir,
        ai_readme=ai_readme,
        push=push,
    )

    console.print(Panel.fit(
        f"[bold]Scaffolding[/bold] [cyan]{name}[/cyan]\n"
        f"Template: [yellow]{template}[/yellow]  |  Industry: [green]{industry}[/green]",
        title="repoforge",
        border_style="blue",
    ))

    generator = RepoGenerator(config)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Creating project structure...", total=None)
        generator.create_structure()

        progress.update(task, description="Writing configuration files...")
        generator.write_configs()

        progress.update(task, description="Generating CI/CD workflows...")
        generator.write_workflows()

        if ai_readme:
            progress.update(task, description="Generating README with AI...")
            readme_content = generate_readme(config)
            generator.write_readme(readme_content)
        else:
            generator.write_readme()

        if push:
            progress.update(task, description="Creating GitHub repo and pushing...")
            generator.push_to_github()

    repo_path = output_dir / name
    console.print(f"\n[bold green]✓[/bold green] Created [cyan]{name}[/cyan] at [dim]{repo_path}[/dim]")


@scaffold_app.command("list-templates")
def list_templates() -> None:
    """List all available scaffold templates."""
    from repoforge.core.templates import TEMPLATES
    console.print("\n[bold]Available templates:[/bold]\n")
    for key, meta in TEMPLATES.items():
        console.print(f"  [cyan]{key:<30}[/cyan] {meta['description']}")
    console.print()
