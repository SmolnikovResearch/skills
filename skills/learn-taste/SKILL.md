---
name: learn-taste
description: Extract design taste rules from reference captures.
version: 1.0.0
author: Smolnikov Research
license: MIT
platforms: [linux, macos, windows]
metadata:
  capyagent:
    tags: [design, taste, tokens, audit, css]
    category: creative
    related_skills: [design-md, claude-design, unslop]
---

# Learn Taste

Analyze an existing high-craft website, component tree, or design screenshot bundle to extract durable visual taste rules (palette tokens, font pairings, radius ratios, border discipline, spacing scale, and motion easing) rather than guessing aesthetics from scratch.

## Workflow

1. Read candidate stylesheets and theme definitions using `read_file` and `search_files`.
2. Run the automated token extractor via `terminal`:

```bash
python3 SKILL_DIR/scripts/extract_taste_rules.py web/src --output /tmp/taste-profile.json
```

3. Synthesize explicit design invariants (for example: dominant surface hexes, display-vs-mono font pairing, border opacity ceiling, preferred easing curve) into `DESIGN.md` or component theme presets.
4. Validate generated interfaces with `unslop` so numeric readouts, focus rings, and reduced-motion fallbacks match the learned system.
