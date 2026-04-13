"""Tests for the template registry."""

from repoforge.core.templates import TEMPLATES


def test_templates_not_empty() -> None:
    assert len(TEMPLATES) > 0


def test_all_templates_have_required_keys() -> None:
    required = {"language", "description", "industries", "includes"}
    for name, meta in TEMPLATES.items():
        assert required.issubset(meta.keys()), f"Template '{name}' missing keys"


def test_python_service_template_exists() -> None:
    assert "python-service" in TEMPLATES


def test_mcp_server_template_exists() -> None:
    assert "mcp-server" in TEMPLATES


def test_fintech_industry_coverage() -> None:
    fintech_templates = [k for k, v in TEMPLATES.items() if "fintech" in v["industries"]]
    assert len(fintech_templates) >= 3
