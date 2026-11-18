#!/usr/bin/env python3
"""Extract recurring CSS tokens, font families, radii, and easing curves from UI sources."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Dict

_HEX_RE = re.compile(r"#[0-9a-fA-F]{3,8}\b")
_VAR_RE = re.compile(r"(--[a-zA-Z0-9_-]+)\s*:\s*([^;}{]+);")
_FONT_RE = re.compile(r"font-family\s*:\s*([^;}{]+);")
_CUBIC_RE = re.compile(r"cubic-bezier\([^)]+\)")


def extract_taste_profile(target: Path) -> Dict[str, object]:
    """Summarize design tokens and recurring style signatures under *target*."""
    target = Path(target).resolve()
    hex_counts: Counter[str] = Counter()
    css_vars: Dict[str, str] = {}
    fonts: Counter[str] = Counter()
    easings: Counter[str] = Counter()
    files_read = 0

    for path in sorted(target.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".css", ".ts", ".tsx"}:
            continue
        if "node_modules" in path.parts or "dist" in path.parts:
            continue
        files_read += 1
        text = path.read_text(encoding="utf-8", errors="ignore")
        for hx in _HEX_RE.findall(text):
            hex_counts[hx.lower()] += 1
        for k, v in _VAR_RE.findall(text):
            css_vars.setdefault(k.strip(), v.strip())
        for f in _FONT_RE.findall(text):
            fonts[f.strip()] += 1
        for e in _CUBIC_RE.findall(text):
            easings[e.strip()] += 1

    return {
        "target": str(target),
        "files_scanned": files_read,
        "top_colors": [c for c, _ in hex_counts.most_common(12)],
        "top_fonts": [f for f, _ in fonts.most_common(6)],
        "motion_curves": [e for e, _ in easings.most_common(6)],
        "css_variable_sample": dict(list(sorted(css_vars.items()))[:25]),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract design taste tokens from UI codebases.")
    parser.add_argument("target", help="UI source directory")
    parser.add_argument("--output", default="", help="Optional JSON output file")
    args = parser.parse_args()
    profile = extract_taste_profile(Path(args.target))
    payload = json.dumps(profile, indent=2, ensure_ascii=False)
    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
