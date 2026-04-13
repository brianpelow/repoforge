"""templates command — manage and inspect scaffold templates."""

from __future__ import annotations

import typer
from rich.console import Console
from rich.table import Table

from repoforge.core.templates import TEMPLATES

templates_app = typer.Typer(help="Manage scaffold templates.")
console = Console()


@templates_app.command("list")
def templates_list() -> None:
    """List all available templates with metadata."""
    table = Table(title="repoforge templates", border_style="dim")
    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("Language", style="yellow")
    table.add_column("Industry fit", style="green")
    table.add_column("Description")

    for key, meta in TEMPLATES.items():
        table.add_row(
            key,
            meta["language"],
            ", ".join(meta["industries"]),
            meta["description"],
        )

    console.print(table)


@templates_app.command("show")
def templates_show(
    name: str = typer.Argument(..., help="Template name to inspect"),
) -> None:
    """Show detailed information about a template."""
    if name not in TEMPLATES:
        console.print(f"[red]Template '{name}' not found.[/red]")
        raise typer.Exit(1)

    meta = TEMPLATES[name]
    console.print(f"\n[bold]{name}[/bold]")
    console.print(f"  Language:    [yellow]{meta['language']}[/yellow]")
    console.print(f"  Description: {meta['description']}")
    console.print(f"  Industries:  [green]{', '.join(meta['industries'])}[/green]")
    console.print(f"  Includes:")
    for item in meta["includes"]:
        console.print(f"    [dim]-[/dim] {item}")
    console.print()
