#!/usr/bin/env python3
"""On-demand defensive static reversing readiness check for release bundles and binaries."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path
from typing import Dict, List

_URL_RE = re.compile(r"https?://[^\s\"'<>]{6,}")


def audit_target(target: Path, *, max_files: int = 200) -> Dict[str, object]:
    """Inspect build artifacts for exposed source maps, external URLs, and debug symbols."""
    target = Path(target).resolve()
    files = [target] if target.is_file() else [p for p in sorted(target.rglob("*")) if p.is_file()][:max_files]
    exposed_maps: List[str] = []
    source_map_hints: List[str] = []
    urls_sample: List[str] = []

    for f in files:
        rel = f.name if target.is_file() else f.relative_to(target).as_posix()
        if f.suffix == ".map":
            exposed_maps.append(rel)
            continue
        if f.suffix.lower() in {".js", ".mjs", ".css", ".txt", ".json"} and f.stat().st_size < 2_000_000:
            text = f.read_text(encoding="utf-8", errors="ignore")
            if "sourceMappingURL" in text:
                source_map_hints.append(rel)
            for url in _URL_RE.findall(text):
                if len(urls_sample) < 15 and url not in urls_sample:
                    urls_sample.append(url)

    return {
        "target": str(target),
        "files_inspected": len(files),
        "optional_tools": {
            "ego-lite": shutil.which("ego-lite") is not None,
            "radare2": shutil.which("r2") is not None,
            "objdump": shutil.which("objdump") is not None,
            "strings": shutil.which("strings") is not None,
        },
        "exposed_sourcemaps": exposed_maps,
        "sourcemap_comment_files": source_map_hints,
        "embedded_urls_sample": urls_sample,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Defensive artifact reversing audit (on-demand).")
    parser.add_argument("target", help="Artifact file or bundle directory")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = audit_target(Path(args.target))
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
