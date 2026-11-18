---
name: ego-lite-reversing
description: On-demand binary and bundle reverse-engineering audit.
version: 1.0.0
author: Smolnikov Research
license: MIT
platforms: [linux, macos, windows]
metadata:
  capyagent:
    tags: [security, reversing, forensics, audit, optional]
    category: security
    related_skills: [oss-forensics, web-pentest, security-audit]
---

# On-Demand Binary and Bundle Reversing Audit

Defensive static inspection toolkit (symbol entropy, embedded URLs, accidental source maps, unmasked license checks, and stripped ELF/Mach-O/PE section headers) activated only on demand. Use strictly for authorized defensive audits of first-party builds and incident forensics.

## Lazy Activation and On-Demand Bootstrap

```bash
python3 scripts/optional_skill_bootstrap.py ego-lite-reversing --status
python3 scripts/optional_skill_bootstrap.py ego-lite-reversing --install
```

## Defensive Inspection Workflow

Run `SKILL_DIR/scripts/ego_lite_audit.py` via `terminal` to verify whether a compiled artifact or archive exposes debug symbols, `.map` trailers, or suspicious high-entropy blobs before shipping:

```bash
python3 SKILL_DIR/scripts/ego_lite_audit.py capyagent_cli/web_dist --json
```
