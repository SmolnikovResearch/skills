---
name: logo-design
description: Craft optical-grid SVG logos and icon variants.
version: 1.0.0
author: Smolnikov Research
license: MIT
platforms: [linux, macos, windows]
metadata:
  capyagent:
    tags: [logo, svg, branding, icons, vector]
    category: creative
    related_skills: [design-md, baoyu-infographic, unslop]
---

# Optical-Grid SVG Logo Design

Design recognizable marks, monochrome wordmarks, and favicon/desktop-icon bundles that stay crisp from `16x16` tray icons up to `1024x1024` launch covers.

## Brand Geometry Rules

1. **Grid Discipline**: Define an explicit integer `viewBox` (for example `0 0 300 220` or `0 0 64 64`), anchor silhouettes cleanly off canvas edges, and test silhouette legibility at `16px`.
2. **Accessible Vector Markup**: Include `<title>` and `<desc>` inside root SVG symbols (`role="img" aria-labelledby="title desc"`).
3. **Variant System**: Provide full-color primary symbol, monochrome dark/light adaptations, and square app-icon pad margins without ungrounded outer halos.
4. **Vector Restraint**: Keep SVG files clean without embedded raster images (`<image>`), scripts (`<script>`), or arbitrary inline event attributes.

## Validation

Inspect existing brand artwork with `read_file`, then validate any SVG asset using `terminal`:

```bash
python3 SKILL_DIR/scripts/validate_svg_logo.py web/public/favicon.svg
```
