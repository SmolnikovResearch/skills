---
name: obscura-browser
description: Low-RAM stealth headless browser via on-demand Obscura.
version: 1.0.0
author: Smolnikov Research
license: MIT
platforms: [linux, macos, windows]
metadata:
  capyagent:
    tags: [browser, automation, stealth, scraping, optional]
    category: web-development
    related_skills: [page-agent, har-derived-api-client]
---

# Obscura Low-RAM Stealth Browser

Lightweight headless browser runner loaded strictly on user demand (`optional-skills`), engineered for low memory footprint (~30 MB RAM target) when standard full browsers are too heavy.

## Lazy Activation and On-Demand Bootstrap

This skill is disabled by default. Install the skill only when needed, inspect readiness with `read_file` on `SKILL_DIR/on-demand.json`, and run dependency setup only when requested:

```bash
python3 scripts/optional_skill_bootstrap.py obscura-browser --status
python3 scripts/optional_skill_bootstrap.py obscura-browser --install
```

## Usage via Terminal

Use `SKILL_DIR/scripts/obscura_client.py` to probe binary availability or launch a bounded page fetch / DOM extraction task without keeping background browser daemons alive at rest:

```bash
python3 SKILL_DIR/scripts/obscura_client.py status --json
python3 SKILL_DIR/scripts/obscura_client.py fetch https://example.com --mode text
```
