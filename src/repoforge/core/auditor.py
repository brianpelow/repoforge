"""Repo auditor — checks a repo against regulated-industry standards."""

from __future__ import annotations

import re
from pathlib import Path


SECRET_PATTERNS = [
    r"(?i)(api[_-]?key|secret|password|token)\s*=\s*['""][^'""]{8,}['""]",
    r"(?i)ghp_[A-Za-z0-9]{36}",
    r"(?i)sk-[A-Za-z0-9]{48}",
]


class RepoAuditor:
    """Audits a local repository against engineering standards."""

    def __init__(self, path: Path, industry: str = "fintech") -> None:
        self.path = path.resolve()
        self.industry = industry

    def run(self) -> list[dict]:
        return [
            self._check_file("LICENSE", "LICENSE present"),
            self._check_file("CONTRIBUTING.md", "CONTRIBUTING.md present"),
            self._check_file("CHANGELOG.md", "CHANGELOG.md present"),
            self._check_file("README.md", "README.md present"),
            self._check_ci("CI workflow present"),
            self._check_lockfile("Dependency lock file present"),
            self._check_secrets("No hardcoded secrets detected"),
            self._check_file(".github/CODEOWNERS", "CODEOWNERS defined"),
            self._check_file(".gitignore", ".gitignore present"),
            self._check_file("docs/adr", "ADR directory present"),
        ]

    def _check_file(self, relative: str, name: str) -> dict:
        exists = (self.path / relative).exists()
        return {"name": name, "passed": exists, "detail": "" if exists else f"Missing: {relative}"}

    def _check_ci(self, name: str) -> dict:
        workflows_path = self.path / ".github" / "workflows"
        workflows = list(workflows_path.glob("*.yml")) if workflows_path.exists() else []
        passed = len(workflows) > 0
        return {"name": name, "passed": passed, "detail": f"{len(workflows)} workflow(s)" if passed else "No workflows found"}

    def _check_lockfile(self, name: str) -> dict:
        candidates = ["uv.lock", "poetry.lock", "package-lock.json", "yarn.lock", "Pipfile.lock"]
        found = next((c for c in candidates if (self.path / c).exists()), None)
        return {"name": name, "passed": found is not None, "detail": found or "No lock file found"}

    def _check_secrets(self, name: str) -> dict:
        violations: list[str] = []
        for f in self.path.rglob("*"):
            if f.is_file() and f.suffix in {".py", ".ts", ".js", ".env", ".yml", ".yaml", ".toml"}:
                try:
                    text = f.read_text(errors="ignore")
                    for pattern in SECRET_PATTERNS:
                        if re.search(pattern, text):
                            violations.append(f.relative_to(self.path).as_posix())
                            break
                except Exception:
                    pass
        passed = len(violations) == 0
        return {"name": name, "passed": passed, "detail": f"Flagged: {', '.join(violations[:3])}" if violations else "Clean"}
