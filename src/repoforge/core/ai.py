"""AI-powered content generation for scaffolded repos."""

from __future__ import annotations

import os
from repoforge.core.config import ScaffoldConfig


def generate_readme(config: ScaffoldConfig) -> str:
    """Generate a README using the Anthropic API.

    Falls back to a structured template if the API key is not set.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return _readme_template(config)

    try:
        from openai import OpenAI
        client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
        message = client.chat.completions.create(
            model="meta-llama/llama-3.1-8b-instruct:free",
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": (
                    f"Write a professional GitHub README.md for a project called '{config.name}'. "
                    f"Description: {config.description}. "
                    f"Industry context: {config.industry} (regulated financial services / fintech). "
                    f"Template type: {config.template}. "
                    "Include: badges section, overview, architecture diagram placeholder, "
                    "quick start, configuration, contributing, and license sections. "
                    "Use clear markdown. Be concise and technical. No fluff."
                ),
            }],
        )
        return message.choices[0].message.content
    except Exception:
        return _readme_template(config)


def _readme_template(config: ScaffoldConfig) -> str:
    return f"""# {config.name}

> {config.description}

![CI](https://github.com/brianpelow/{config.name}/actions/workflows/ci.yml/badge.svg)
![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.12+-green.svg)

## Overview

{config.description}

Built for **{config.industry}** engineering teams in regulated environments.

## Quick start

```bash
git clone https://github.com/brianpelow/{config.name}
cd {config.name}
uv sync
uv run {config.name} --help
```

## Configuration

| Variable | Description | Required |
|----------|-------------|----------|
| `ANTHROPIC_API_KEY` | Enables AI-generated READMEs | No |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Apache 2.0 — see [LICENSE](LICENSE).
"""
