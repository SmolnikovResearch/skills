---
name: design-md
description: Enforce brand design.md rules to prevent AI SaaS slop.
version: 1.0.0
author: Smolnikov Research
license: MIT
platforms: [linux, macos, windows]
metadata:
  capyagent:
    tags: [design, design-md, anti-slop, brand, typography, css, ui]
    category: creative
    related_skills: [ui-sdk-builder, unslop, hallmark-styles, learn-taste]
---

# `design.md` Brand & Layout Contract Skill

Prevent generic AI SaaS templates by requiring every UI task, report, or landing page to read the project's `design.md` contract before generating markup or styles.

## When to Use

Use this skill whenever an agent creates or refactors a web interface, product landing page, dashboard, interactive report, or customer proposal (`kp-builder`), or when establishing a new repository's `DESIGN.md`.

## What a Valid `design.md` Governs

1. **Reader Task Hierarchy:** Every page states its primary reader question first and organizes blocks strictly to answer it (never filler hero slogans + 3 generic cards + random gradient).
2. **Data Presentation Matrix:**
   - Exact comparisons & specifications -> HTML tables with `font-variant-numeric: tabular-nums`.
   - Trends over time -> compact SVG/Canvas chart with explicit axis units.
   - Decisions, limits & next steps -> concise bullet lists (`<= 3` clauses per item).
3. **Approved Visual Tokens:** Font families (`Onest`, system fallbacks), exact hex surface/ink/accent palette, container widths, border radii, and `--ease-out-expo: cubic-bezier(0.22, 1, 0.36, 1)`.
4. **Hard Anti-Slop Bans:** No `transition: all`, no arbitrary unapproved linear/radial rainbow gradients, no glassmorphism blur over noisy photos without contrast guard, no placeholder copy ("Elevate your workflow"), and strict keyboard/reduced-motion (`prefers-reduced-motion: reduce`) compliance.

## CLI Workflow (`SKILL_DIR/scripts/design_md_tool.py`)

```bash
python3 SKILL_DIR/scripts/design_md_tool.py generate --brand "CapyAgent" --out ./DESIGN.md
python3 SKILL_DIR/scripts/design_md_tool.py audit ./src
```

This skill loads lazily from `optional-skills` (`auto_load_on_startup: false`) and works with zero external binaries.
