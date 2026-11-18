#!/usr/bin/env python3
"""Validate brand SVG logo hygiene, viewBox geometry, and accessibility metadata."""

from __future__ import annotations

import argparse
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List


def validate_svg_file(svg_path: Path) -> Dict[str, object]:
    """Check an SVG file for viewBox, accessibility tags, and unsafe embedded elements."""
    svg_path = Path(svg_path).resolve()
    raw = svg_path.read_text(encoding="utf-8")
    root = ET.fromstring(raw)

    issues: List[str] = []
    warnings: List[str] = []

    viewbox = root.attrib.get("viewBox", "").strip()
    if not viewbox:
        issues.append("Missing viewBox attribute on root <svg>.")

    has_title = any(el.tag.endswith("title") and (el.text or "").strip() for el in root.iter())
    has_desc = any(el.tag.endswith("desc") and (el.text or "").strip() for el in root.iter())
    if not has_title:
        warnings.append("Missing non-empty <title> element for screen readers.")
    if not has_desc:
        warnings.append("Missing non-empty <desc> element.")

    forbidden_tags = []
    shape_count = 0
    for el in root.iter():
        tag = el.tag.split("}")[-1].lower()
        if tag in {"script", "foreignobject", "image"}:
            forbidden_tags.append(tag)
        if tag in {"path", "circle", "rect", "ellipse", "polygon", "polyline", "line"}:
            shape_count += 1
        for attr in el.attrib:
            if attr.lower().startswith("on"):
                issues.append(f"Disallowed inline event handler attribute: {attr}")

    if forbidden_tags:
        issues.append(f"Disallowed embedded elements in clean SVG logo: {', '.join(sorted(set(forbidden_tags)))}")
    if shape_count == 0:
        issues.append("SVG contains zero vector geometry elements.")

    return {
        "file": str(svg_path),
        "valid": len(issues) == 0,
        "viewBox": viewbox,
        "shape_count": shape_count,
        "has_title": has_title,
        "has_desc": has_desc,
        "issues": issues,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an SVG brand logo asset.")
    parser.add_argument("svg", help="Path to .svg logo file")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    args = parser.parse_args()
    result = validate_svg_file(Path(args.svg))
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(
            f"SVG Logo Check: valid={result['valid']} viewBox='{result['viewBox']}' "
            f"shapes={result['shape_count']} issues={len(result['issues'])} warnings={len(result['warnings'])}"
        )
        for msg in result["issues"]:
            print(f"  [ERROR] {msg}")
        for msg in result["warnings"]:
            print(f"  [WARN]  {msg}")
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
