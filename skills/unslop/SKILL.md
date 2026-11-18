---
name: unslop
description: Anti-slop UI polish and visual QA discipline.
version: 1.0.0
author: Smolnikov Research
license: MIT
platforms: [linux, macos, windows]
metadata:
  capyagent:
    tags: [design, ui, ux, css, quality]
    category: creative
    related_skills: [design-md, claude-design, popular-web-designs]
---

# Unslop UI Polish

Eliminate generic AI-generated UI tells ("purple-blue gradient slop", inflated rounded cards, jittery numeric counters, harsh borders, and unguarded motion) and enforce craft-grade visual discipline across React, Tailwind, and vanilla web interfaces.

## Core Anti-Slop Checklist

1. **Typography and Numbers**: Apply `font-variant-numeric: tabular-nums` (`tabular-nums`) to live counters, tables, timestamps, token counts, and pricing so numbers never shift width horizontally.
2. **Surface and Border Restraint**: Keep hairline borders subtle (`10%-18%` foreground alpha or Tailwind `/15` mixes) and prefer concentric border radii (`outerRadius = innerRadius + padding`).
3. **Motion Choreography and Accessibility**: Use exponential ease-out (`cubic-bezier(0.22, 1, 0.36, 1)`), avoid `transition-all`, gate hover transforms with `@media (hover: hover) and (pointer: fine)`, and respect `prefers-reduced-motion: reduce`.
4. **Copy and Layout Hierarchy**: Replace vague hype headlines with scannable state labels, align baselines strictly, and ensure interactive hit targets remain at least `36px`.

## Audit Workflow

Inspect styling and components via `read_file` and `search_files`, then run the static auditor via `terminal`:

```bash
python3 SKILL_DIR/scripts/audit_ui_slop.py web/src
```

Fix high-signal warnings first (`missing tabular-nums on metric/table containers`, `linear/default ease on UI panels`, `unconstrained transition: all`, missing `prefers-reduced-motion` guard), then verify layout spacing and dark/light contrast interactively.
