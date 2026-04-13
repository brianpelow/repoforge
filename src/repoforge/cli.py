"""repoforge CLI entry point."""

from __future__ import annotations

import typer
from rich.console import Console

from repoforge import __version__
from repoforge.commands.scaffold import scaffold_app
from repoforge.commands.templates import templates_app
from repoforge.commands.audit import audit_app

app = typer.Typer(
    name="repoforge",
    help="AI-assisted repo scaffolding for regulated industries engineering teams.",
    add_completion=True,
    rich_markup_mode="rich",
)
console = Console()

app.add_typer(scaffold_app, name="scaffold")
app.add_typer(templates_app, name="templates")
app.add_typer(audit_app, name="audit")


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: bool = typer.Option(False, "--version", "-v", help="Show version and exit."),
) -> None:
    """repoforge — forge production-ready repos in seconds."""
    if version:
        console.print(f"repoforge v{__version__}")
        raise typer.Exit()
    if ctx.invoked_subcommand is None:
        console.print(ctx.get_help())
