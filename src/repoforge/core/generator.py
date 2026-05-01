"""Core repo generation logic."""

from __future__ import annotations

import subprocess
from pathlib import Path
from datetime import date

from repoforge.core.config import ScaffoldConfig
from repoforge.core.templates import TEMPLATES


class RepoGenerator:
    """Generates a scaffold repo from a config."""

    def __init__(self, config: ScaffoldConfig) -> None:
        self.config = config
        self.path = config.repo_path
        self.template = TEMPLATES.get(config.template, TEMPLATES["python-service"])

    def create_structure(self) -> None:
        dirs = [
            self.path,
            self.path / "src",
            self.path / "tests",
            self.path / "docs" / "adr",
            self.path / ".github" / "workflows",
            self.path / ".github" / "ISSUE_TEMPLATE",
        ]
        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "init", "-b", "main"], cwd=self.path, capture_output=True)

    def write_configs(self) -> None:
        today = date.today().isoformat()
        (self.path / ".gitignore").write_text("__pycache__/\n*.pyc\n.venv/\n.env\n*.egg-info/\ndist/\n.pytest_cache/\n.coverage\n")
        (self.path / "LICENSE").write_text("Apache License\nVersion 2.0, January 2004\nhttp://www.apache.org/licenses/\n")
        (self.path / "CONTRIBUTING.md").write_text("# Contributing\n\nSee README for development setup.\n")
        (self.path / "CHANGELOG.md").write_text(f"# Changelog\n\n## [Unreleased]\n\n## [0.1.0] - {today}\n\n### Added\n- Initial scaffold\n")
        (self.path / ".github" / "CODEOWNERS").write_text("* @brianpelow\n")
        (self.path / ".github" / "pull_request_template.md").write_text("## Summary\n\n## Type of change\n\n- [ ] Bug fix\n- [ ] New feature\n- [ ] Documentation update\n\n## Checklist\n\n- [ ] Tests added\n- [ ] CHANGELOG updated\n")
        (self.path / "docs" / "adr" / "README.md").write_text("# Architecture Decision Records\n\nThis directory contains ADRs for this project.\n")

    def write_workflows(self) -> None:
        (self.path / ".github" / "workflows" / "ci.yml").write_text(self._python_ci())
        (self.path / ".github" / "workflows" / "nightly-agent.yml").write_text(self._nightly_agent())

    def write_readme(self, content: str | None = None) -> None:
        if content:
            (self.path / "README.md").write_text(content)
        else:
            (self.path / "README.md").write_text(f"# {self.config.name}\n\n{self.config.description}\n\n## Quick start\n\n```bash\n# TODO\n```\n")

    def push_to_github(self) -> None:
        subprocess.run(
            ["gh", "repo", "create", self.config.name, "--public",
             "--description", self.config.description, "--source", str(self.path), "--push"],
            check=True,
        )

    def _python_ci(self) -> str:
        return "name: CI\n\non:\n  push:\n    branches: [main]\n  pull_request:\n    branches: [main]\n\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - uses: astral-sh/setup-uv@v4\n        with:\n          python-version: \"3.12\"\n      - run: uv sync --all-extras\n      - run: uv run ruff check .\n      - run: uv run pytest --cov=src --cov-report=xml\n"

    def _nightly_agent(self) -> str:
        return "name: Nightly agent\n\non:\n  schedule:\n    - cron: \"0 2 * * *\"\n  workflow_dispatch:\n\npermissions:\n  contents: write\n\njobs:\n  agent:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n        with:\n          token: ${{ secrets.GITHUB_TOKEN }}\n      - uses: astral-sh/setup-uv@v4\n        with:\n          python-version: \"3.12\"\n      - name: Run nightly agent\n        env:\n          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}\n        run: uv run python scripts/nightly_agent.py\n      - name: Commit agent output\n        run: |\n          git config user.name \"repoforge-agent[bot]\"\n          git config user.email \"agent@repoforge\"\n          git add -A\n          git diff --staged --quiet || git commit -m \"chore(agent): nightly update $(date -u +%Y-%m-%d)\"\n          git push\n"
