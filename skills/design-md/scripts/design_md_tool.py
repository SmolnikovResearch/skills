#!/usr/bin/env python3
"""Generator and static linter for project-level DESIGN.md brand contracts."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

BANNED_COPY_PATTERNS = [
    (re.compile(r"\b(?:elevate|supercharge|unleash|revolutionize)\s+your\b", re.I), "generic_ai_headline"),
    (re.compile(r"\bseamless(?:ly)?\s+integrate", re.I), "cliche_saas_promise"),
    (re.compile(r"lorem\s+ipsum", re.I), "placeholder_copy"),
]

CSS_SLOP_PATTERNS = [
    (re.compile(r"transition\s*:\s*all\b", re.I), "transition_all"),
    (re.compile(r"background[^;]*linear-gradient\([^)]*#(?:a855f7|ec4899|8b5cf6)", re.I), "unapproved_purple_pink_gradient"),
]


def render_design_md(brand: str = "CapyAgent", accent_hex: str = "#b86a16") -> str:
    """Render a complete machine-readable DESIGN.md specification."""
    clean_brand = brand.strip() or "CapyAgent"
    return f"""# DESIGN.md - {clean_brand} Design Contract

## 1. Reader-First Structure
- Identify the single concrete job of the page before choosing components.
- Above the fold: direct statement of capability, concrete proof/metric, and one clear primary CTA.
- Never open with vague SaaS filler ("Supercharge", "Next-gen AI", "Seamless productivity").

## 2. Tables vs Charts vs Prose
- Structured comparisons, pricing, limits, and checksums MUST use tables with `font-variant-numeric: tabular-nums;`.
- Multi-point time series or cost trends MUST use crisp labeled axes with explicit units.
- Workflows and constraints use numbered lists (max 2 sentences per bullet).

## 3. Approved Typography & Color Tokens
- Primary UI sans: `Onest`, `Inter`, `system-ui`, `-apple-system`, sans-serif.
- Monospace: `JetBrains Mono`, `ui-monospace`, `SFMono-Regular`, monospace.
- Light editorial surface: `#f7f5ef` (paper), `#ffffff` (card), `#172b25` (ink), `#53615b` (muted).
- Brand accents: `#254d3c` (forest primary), `{accent_hex}` (capy amber highlight), `#dedfd8` (hairline border).
- Motion token: `--ease-out-expo: cubic-bezier(0.22, 1, 0.36, 1)`.

## 4. Interactive Brand Identity
- Render the interactive v1.1 mascot (`CapyMascot` / `data-capy-mascot`) with 9-direction cursor tracking and 6 click moods (`calm`, `happy`, `wink`, `surprised`, `focused`, `sleepy`).
- Always honor `@media (prefers-reduced-motion: reduce)` by disabling transforms and transitions.

## 5. Forbidden Patterns
- `transition: all` in CSS.
- Unapproved neon/purple-pink SaaS gradients.
- Numbers/prices without `tabular-nums`.
- Non-keyboard-accessible clickable icons (`div` without `role`, `tabindex`, key handlers, or `:focus-visible`).
- Long/en dashes (`U+2014`, `U+2013`) in Cyrillic product copy (use `-` hyphen only).
"""


def audit_tree(target: Path, *, require_tabular_nums: bool = True) -> Dict[str, Any]:
    """Scan CSS/HTML/TSX/MD files under ``target`` for DESIGN.md violations."""
    findings: List[Dict[str, Any]] = []
    exts = {".css", ".html", ".htm", ".tsx", ".jsx", ".vue", ".svelte", ".md"}
    files = [target] if target.is_file() else sorted(p for p in target.rglob("*") if p.is_file() and p.suffix.lower() in exts)
    css_has_tabular = False
    scanned = 0

    for fp in files:
        if any(part in {"node_modules", ".git", "dist", "build", "web_dist"} for part in fp.parts):
            continue
        scanned += 1
        text = fp.read_text(encoding="utf-8", errors="ignore")
        rel = fp.name if target.is_file() else fp.relative_to(target).as_posix()
        if fp.suffix.lower() in {".css", ".html", ".tsx", ".vue", ".svelte"} and "tabular-nums" in text:
            css_has_tabular = True
        for rx, rule in BANNED_COPY_PATTERNS + (CSS_SLOP_PATTERNS if fp.suffix.lower() in {".css", ".html", ".tsx", ".vue", ".svelte"} else []):
            for m in rx.finditer(text):
                line = text.count("\n", 0, m.start()) + 1
                findings.append({"file": rel, "line": line, "rule": rule, "match": m.group(0)[:80]})

    if require_tabular_nums and scanned > 0 and any(p.suffix.lower() in {".css", ".html", ".tsx", ".vue", ".svelte"} for p in files) and not css_has_tabular:
        findings.append({"file": ".", "line": 1, "rule": "missing_tabular_nums", "match": "font-variant-numeric: tabular-nums"})

    return {
        "skill": "design-md",
        "files_scanned": scanned,
        "finding_count": len(findings),
        "findings": findings,
        "ok": len(findings) == 0,
    }


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Generate or audit DESIGN.md contracts.")
    sub = parser.add_subparsers(dest="cmd", required=True)
    gen = sub.add_parser("generate")
    gen.add_argument("--brand", default="CapyAgent")
    gen.add_argument("--accent", default="#b86a16")
    gen.add_argument("--out", default="")
    aud = sub.add_parser("audit")
    aud.add_argument("target", nargs="?", default=".")
    aud.add_argument("--no-require-tabular", action="store_true")
    args = parser.parse_args(argv)
    if args.cmd == "generate":
        content = render_design_md(args.brand, args.accent)
        if args.out:
            out_p = Path(args.out)
            out_p.parent.mkdir(parents=True, exist_ok=True)
            out_p.write_text(content, encoding="utf-8")
        else:
            print(content)
        return 0
    res = audit_tree(Path(args.target), require_tabular_nums=not args.no_require_tabular)
    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
