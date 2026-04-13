"""Configuration models for repoforge."""

from __future__ import annotations

from pathlib import Path
from pydantic import BaseModel, Field


class ScaffoldConfig(BaseModel):
    """Configuration for a scaffold operation."""

    name: str = Field(..., description="Repository name")
    template: str = Field("python-service", description="Template identifier")
    industry: str = Field("fintech", description="Target industry context")
    description: str = Field("", description="Short repository description")
    output_dir: Path = Field(Path("."), description="Output directory")
    ai_readme: bool = Field(True, description="Generate README with AI")
    push: bool = Field(False, description="Push to GitHub after creation")

    @property
    def repo_path(self) -> Path:
        return self.output_dir / self.name
