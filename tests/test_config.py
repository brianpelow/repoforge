"""Tests for ScaffoldConfig."""

from pathlib import Path
from repoforge.core.config import ScaffoldConfig


def test_scaffold_config_defaults() -> None:
    config = ScaffoldConfig(name="my-service")
    assert config.template == "python-service"
    assert config.industry == "fintech"
    assert config.ai_readme is True
    assert config.push is False


def test_scaffold_config_repo_path() -> None:
    config = ScaffoldConfig(name="my-service", output_dir=Path("/tmp"))
    assert config.repo_path == Path("/tmp/my-service")


def test_scaffold_config_custom() -> None:
    config = ScaffoldConfig(name="trade-engine", template="mcp-server", industry="fintech")
    assert config.name == "trade-engine"
    assert config.template == "mcp-server"
