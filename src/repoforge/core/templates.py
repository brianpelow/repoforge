"""Built-in scaffold template registry."""

from __future__ import annotations

TEMPLATES: dict[str, dict] = {
    "python-service": {
        "language": "Python",
        "description": "FastAPI microservice with uv, ruff, mypy, pytest, and Docker",
        "industries": ["fintech", "manufacturing", "regulated"],
        "includes": [
            "FastAPI app skeleton",
            "uv pyproject.toml",
            "Dockerfile + docker-compose.yml",
            "GitHub Actions CI",
            "Nightly agent workflow",
            "pytest test suite scaffold",
            "CHANGELOG, CONTRIBUTING, LICENSE, CODEOWNERS",
            "ADR docs template",
        ],
    },
    "typescript-app": {
        "language": "TypeScript",
        "description": "Next.js 14 app with TypeScript, Tailwind, Vitest, and Docker",
        "industries": ["fintech", "manufacturing", "saas"],
        "includes": [
            "Next.js 14 app router skeleton",
            "TypeScript strict config",
            "Tailwind CSS",
            "Vitest + Testing Library",
            "GitHub Actions CI",
            "Nightly agent workflow",
        ],
    },
    "mcp-server": {
        "language": "Python",
        "description": "Model Context Protocol server with FastMCP, typed tools, and tests",
        "industries": ["fintech", "manufacturing", "regulated", "platform"],
        "includes": [
            "FastMCP server skeleton",
            "Typed tool definitions",
            "Resource and prompt templates",
            "pytest test suite",
            "GitHub Actions CI",
            "Nightly agent workflow",
        ],
    },
    "cli-tool": {
        "language": "Python",
        "description": "Typer CLI tool with rich output, tests, and PyPI-ready packaging",
        "industries": ["fintech", "manufacturing", "platform", "devtools"],
        "includes": [
            "Typer + Rich CLI skeleton",
            "uv pyproject.toml with scripts entry point",
            "pytest test suite",
            "GitHub Actions CI + release workflow",
            "Nightly agent workflow",
        ],
    },
    "data-pipeline": {
        "language": "Python",
        "description": "Async data pipeline with Pydantic models, DuckDB, and observability",
        "industries": ["fintech", "manufacturing", "data"],
        "includes": [
            "Async pipeline skeleton",
            "Pydantic v2 data models",
            "DuckDB for local analytics",
            "Structured logging with structlog",
            "Prometheus metrics endpoint",
            "pytest + hypothesis tests",
            "GitHub Actions CI",
            "Nightly agent workflow",
        ],
    },
    "backstage-plugin": {
        "language": "TypeScript",
        "description": "Backstage frontend + backend plugin with React and REST API",
        "industries": ["platform", "devtools", "regulated"],
        "includes": [
            "Backstage plugin scaffolding",
            "React frontend component",
            "Backend router with REST endpoints",
            "Jest tests",
            "GitHub Actions CI",
            "Nightly agent workflow",
        ],
    },
    "github-action": {
        "language": "TypeScript",
        "description": "Composite GitHub Action with inputs, outputs, and marketplace metadata",
        "industries": ["platform", "devtools", "fintech", "manufacturing"],
        "includes": [
            "action.yml definition",
            "TypeScript action runner",
            "Jest tests",
            "Release workflow for marketplace publishing",
            "Nightly agent workflow",
        ],
    },
}
