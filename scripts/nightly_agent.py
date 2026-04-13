"""Nightly agent — automated maintenance for the repoforge repo."""

from __future__ import annotations

import json
import sys
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

REPO_ROOT = Path(__file__).parent.parent


def update_template_stats() -> None:
    from repoforge.core.templates import TEMPLATES
    stats = {
        "generated_at": datetime.utcnow().isoformat(),
        "date": date.today().isoformat(),
        "templates": {k: {"language": v["language"], "industry_count": len(v["industries"])} for k, v in TEMPLATES.items()},
    }
    out = REPO_ROOT / "docs" / "template-stats.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(stats, indent=2))
    print(f"[agent] Updated template stats -> {out}")


def refresh_changelog() -> None:
    changelog = REPO_ROOT / "CHANGELOG.md"
    if not changelog.exists():
        return
    today = date.today().isoformat()
    content = changelog.read_text()
    if today not in content:
        content = content.replace("## [Unreleased]", f"## [Unreleased]\n\n_Last checked: {today}_", 1)
        changelog.write_text(content)
    print(f"[agent] Refreshed CHANGELOG timestamp")


if __name__ == "__main__":
    print(f"[agent] Starting nightly agent - {date.today().isoformat()}")
    update_template_stats()
    refresh_changelog()
    print("[agent] Done.")
