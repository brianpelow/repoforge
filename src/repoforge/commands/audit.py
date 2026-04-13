"""audit command — check an existing repo against regulated-industry standards."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from repoforge.core.auditor import RepoAuditor

audit_app = typer.Typer(help="Audit a repo against regulated-industry standards.")
console = Console()


@audit_app.command("run")
def audit_run(
    path: Path = typer.Argument(Path("."), help="Path to the repository to audit"),
    industry: str = typer.Option("fintech", "--industry", "-i", help="Industry standard to check against"),
) -> None:
    """Audit a repository against regulated-industry engineering standards."""
    auditor = RepoAuditor(path, industry)
    results = auditor.run()

    table = Table(title=f"Audit: {path.resolve().name} [{industry}]", border_style="dim")
    table.add_column("Check", style="bold")
    table.add_column("Status", justify="center")
    table.add_column("Detail", style="dim")

    passed = 0
    for check in results:
        status = "[green]✓[/green]" if check["passed"] else "[red]✗[/red]"
        if check["passed"]:
            passed += 1
        table.add_row(check["name"], status, check.get("detail", ""))

    console.print(table)
    score = int((passed / len(results)) * 100)
    color = "green" if score >= 80 else "yellow" if score >= 60 else "red"
    console.print(f"\n[bold]Score: [{color}]{score}%[/{color}][/bold] ({passed}/{len(results)} checks passed)\n")
