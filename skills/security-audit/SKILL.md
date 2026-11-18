---
name: security-audit
description: Two-phase CapyAgent security audit and hardening workflow.
version: 1.0.0
author: Smolnikov Research
license: MIT
platforms: [linux, macos, windows]
metadata:
  capyagent:
    tags: [security, audit, hardening, secrets, skills-guard]
    category: devops
    related_skills: [sdlc-review, agent-handover]
---

# CapyAgent Security Audit

Two-phase repository security review combining attack-surface discovery, `skills_guard` skill scanning, and static bundle hardening checks before release.

## When to Use

- Preparing a CapyAgent release build or auditing `capyagent_cli/web_dist`.
- Reviewing untrusted or newly authored skills before installation.
- Verifying secret hygiene, dependency manifests, and `.mcp.json` / `.env` boundaries.

## Phase 1: Attack Surface Discovery

Use `search_files` and `read_file` to inventory:

1. Entrypoints and privileged surfaces (`agent/`, `gateway/`, `capyagent_cli/`, `web/`).
2. Dependency manifests (`pyproject.toml`, `web/package.json`, lockfiles) and `.mcp.json` tool definitions.
3. Shipped static assets (`capyagent_cli/web_dist/`) for unstripped `.map` source maps or exposed comments.

## Phase 2: Automated Verification and Hardening

Run the two-phase audit and skill scanner through `terminal`:

```bash
python3 scripts/security_audit.py --output reports/security-audit-2026-11-18.json
```

Inspect individual skill risk scores (`0..100`) and extended Unicode / injection checks in `tools/skills_guard.py`:

- Unicode Tag blocks (`U+E0000..U+E007F`) and steganographic variation-selector sequences.
- Hidden multi-line HTML comments (`<!-- ... -->`) and Markdown image query/template exfiltration.
- `.mcp.json` / `mcpServers` shell or prose tampering rules.

For release static assets, produce a hardened staging copy with `scripts/build_hardening.py`:

```bash
python3 scripts/build_hardening.py --input capyagent_cli/web_dist --output /tmp/capyagent-web-hardened --json
```

This strips `.map` files and `sourceMappingURL` comments, masks sensitive license/quota identifiers deterministically, and adds isolated `.hardened-traps/` decoys without modifying runtime entrypoints.
