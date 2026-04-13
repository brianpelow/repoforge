"""Tests for RepoAuditor."""

import tempfile
from pathlib import Path
from repoforge.core.auditor import RepoAuditor


def test_audit_empty_repo_fails_most_checks() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        auditor = RepoAuditor(Path(tmpdir))
        results = auditor.run()
        passed = [r for r in results if r["passed"]]
        assert len(passed) < len(results)


def test_audit_detects_license() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir)
        (path / "LICENSE").write_text("Apache 2.0")
        auditor = RepoAuditor(path)
        results = auditor.run()
        license_check = next(r for r in results if r["name"] == "LICENSE present")
        assert license_check["passed"] is True


def test_audit_clean_secrets() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir)
        (path / "config.py").write_text('api_key = os.environ.get("API_KEY")')
        auditor = RepoAuditor(path)
        results = auditor.run()
        secret_check = next(r for r in results if "secrets" in r["name"])
        assert secret_check["passed"] is True
