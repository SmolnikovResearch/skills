---
name: hallmark-styles
description: Curated non-generic UI design systems and tokens.
version: 1.0.0
author: Smolnikov Research
license: MIT
platforms: [linux, macos, windows]
metadata:
  capyagent:
    tags: [design-system, tokens, typography, css, ui]
    category: creative
    related_skills: [design-md, claude-design, popular-web-designs, unslop]
---

# Hallmark Styles

Commit to an authentic aesthetic direction instead of generic card-soup dashboards. Use this catalog to pair typography, color contrast, surface grain, radius discipline, and motion curves cohesively.

## Workflow

1. Read `SKILL_DIR/references/style-catalog.md` using `read_file`.
2. Select one direction matching the product's physical metaphor (editorial print, archival paper, precision hardware, botanical telemetry, or monochrome terminal).
3. Map CSS variables cleanly to semantic tokens (`--background`, `--foreground`, `--accent`, `--border`, `--radius`) and preserve strict contrast ratios (`>= 4.5:1` body text, `>= 3:1` UI chrome).
4. Cross-check final components with the `unslop` skill before shipping.
