# repoforge

> AI-assisted repo scaffolding CLI for regulated industries engineering teams.

![CI](https://github.com/brianpelow/repoforge/actions/workflows/ci.yml/badge.svg)
![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.12+-green.svg)

## Overview

`repoforge` is a command-line tool that scaffolds production-ready repositories
in seconds. Purpose-built for engineering teams in regulated financial services,
fintech, and manufacturing where every new service needs consistent CI/CD,
compliance artifacts, security hygiene, and documentation from day one.

Ships with 7 built-in templates and generates READMEs using the Anthropic API.
Every scaffold includes a nightly autonomous agent workflow.

## Quick start

```bash
pip install repoforge

repoforge scaffold new payments-gateway --template python-service --industry fintech
repoforge audit run ./my-service --industry fintech
repoforge templates list
```

## Commands

| Command | Description |
|---------|-------------|
| `repoforge scaffold new` | Create a new repo from a template |
| `repoforge templates list` | Show all templates |
| `repoforge templates show <name>` | Inspect a template |
| `repoforge audit run` | Audit a repo against regulated-industry standards |

## Templates

| Template | Language | Description |
|----------|----------|-------------|
| `python-service` | Python | FastAPI microservice with uv, ruff, mypy, pytest |
| `typescript-app` | TypeScript | Next.js 14 app with Tailwind and Vitest |
| `mcp-server` | Python | Model Context Protocol server with FastMCP |
| `cli-tool` | Python | Typer CLI with rich output and PyPI packaging |
| `data-pipeline` | Python | Async pipeline with Pydantic, DuckDB, Prometheus |
| `backstage-plugin` | TypeScript | Backstage frontend + backend plugin |
| `github-action` | TypeScript | Composite GitHub Action |

## Industry context

Designed for teams under regulatory frameworks including PCI-DSS, SOX, FFIEC,
IEC 62443, SOC 2, and ISO 27001.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Apache 2.0 — see [LICENSE](LICENSE).