#!/usr/bin/env python3
"""Static anti-slop auditor for TSX/JSX/CSS web interfaces."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List

_TRANSITION_ALL_RE = re.compile(r"\btransition-all\b|transition:\s*all\b")
_DEFAULT_EASE_RE = re.compile(r"ease-in-out\b|\bease\b(?!-out)")
_PURPLE_SLOP_RE = re.compile(r"from-(?:indigo|violet|purple)-\d+\s+(?:via-[^\s]+\s+)?to-(?:blue|cyan|pink|indigo)-\d+")
_TEXT_EXTENSIONS = {".tsx", ".jsx", ".css", ".scss", ".html"}


def audit_ui_directory(target: Path) -> Dict[str, object]:
    """Scan CSS/TSX files under *target* for common AI-slop UI smells."""
    target = Path(target).resolve()
    findings: List[dict] = []
    files_scanned = 0
    has_reduced_motion = False
    has_tabular_nums = False

    for path in sorted(target.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in _TEXT_EXTENSIONS:
            continue
        if "node_modules" in path.parts or "dist" in path.parts:
            continue
        files_scanned += 1
        rel = path.relative_to(target).as_posix()
        text = path.read_text(encoding="utf-8", errors="ignore")
        if "prefers-reduced-motion" in text:
            has_reduced_motion = True
        if "tabular-nums" in text:
            has_tabular_nums = True

        for lineno, line in enumerate(text.splitlines(), start=1):
            if _TRANSITION_ALL_RE.search(line):
                findings.append(
                    {
                        "rule": "avoid_transition_all",
                        "severity": "medium",
                        "file": rel,
                        "line": lineno,
                        "note": "Prefer explicit transition properties (color, transform, opacity) over transition-all.",
                    }
                )
            if _PURPLE_SLOP_RE.search(line):
                findings.append(
                    {
                        "rule": "generic_purple_gradient",
                        "severity": "high",
                        "file": rel,
                        "line": lineno,
                        "note": "Replace cliché indigo/purple-to-blue gradient with purposeful palette tokens.",
                    }
                )
            if "animate-" not in line and path.suffix in {".css", ".scss"} and _DEFAULT_EASE_RE.search(line):
                findings.append(
                    {
                        "rule": "non_exponential_ease",
                        "severity": "low",
                        "file": rel,
                        "line": lineno,
                        "note": "Consider cubic-bezier(0.22, 1, 0.36, 1) for responsive UI exits/entrances.",
                    }
                )

    if files_scanned > 0 and not has_reduced_motion:
        findings.append(
            {
                "rule": "missing_reduced_motion",
                "severity": "medium",
                "file": ".",
                "line": 0,
                "note": "No prefers-reduced-motion media/hook guard found in scanned UI files.",
            }
        )
    if files_scanned > 0 and not has_tabular_nums:
        findings.append(
            {
                "rule": "missing_tabular_nums",
                "severity": "low",
                "file": ".",
                "line": 0,
                "note": "Apply tabular-nums on numeric readouts, metrics, and tables to stop layout jitter.",
            }
        )

    return {
        "target": str(target),
        "files_scanned": files_scanned,
        "has_reduced_motion": has_reduced_motion,
        "has_tabular_nums": has_tabular_nums,
        "finding_count": len(findings),
        "findings": findings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit web UI files for anti-slop design hygiene.")
    parser.add_argument("target", help="UI source directory (e.g. web/src)")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    args = parser.parse_args()
    report = audit_ui_directory(Path(args.target))
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(
            f"Unslop UI Audit: files={report['files_scanned']}, findings={report['finding_count']}, "
            f"reduced_motion={report['has_reduced_motion']}, tabular_nums={report['has_tabular_nums']}"
        )
        for item in report["findings"][:20]:
            print(f"  [{item['severity']}] {item['rule']} {item['file']}:{item['line']} - {item['note']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
