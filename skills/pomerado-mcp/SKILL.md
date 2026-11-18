---
name: pomerado-mcp
description: Turn websites without APIs into on-demand MCP tools.
version: 1.0.0
author: Smolnikov Research
license: MIT
platforms: [linux, macos, windows]
metadata:
  capyagent:
    tags: [mcp, web-api, har, integration, optional]
    category: web-development
    related_skills: [har-derived-api-client, page-agent]
---

# Pomerado On-Demand Website-to-MCP Bridge

Generate typed MCP tool descriptors and local bridges from captured web sessions or OpenAPI/HAR traces only when explicitly enabled by the user.

## Lazy Activation and On-Demand Bootstrap

Keep this skill unloaded until a target web workflow has no public API:

```bash
python3 scripts/optional_skill_bootstrap.py pomerado-mcp --status
python3 scripts/optional_skill_bootstrap.py pomerado-mcp --install
```

## Workflow via Terminal and File Tools

1. Inspect an existing HAR or session manifest with `read_file`.
2. Scaffold a local `.mcp.json` snippet via `SKILL_DIR/scripts/pomerado_bridge.py` using `terminal`, keeping auth tokens in user-managed environment variables and never hardcoding secrets inside skill directories.
3. Verify any modified `.mcp.json` conforms to strict host allowlists (`security-audit`).
