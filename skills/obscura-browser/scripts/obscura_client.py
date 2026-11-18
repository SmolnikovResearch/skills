#!/usr/bin/env python3
"""On-demand wrapper for lightweight Obscura headless browser workflows."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Optional


def resolve_obscura_binary() -> Optional[str]:
    """Return configured or PATH-installed Obscura browser executable without auto-downloading."""
    env_bin = os.environ.get("OBSCURA_BIN", "").strip()
    if env_bin and Path(env_bin).is_file():
        return env_bin
    for name in ("obscura", "obscura-browser"):
        found = shutil.which(name)
        if found:
            return found
    return None


def inspect_status() -> Dict[str, object]:
    """Report Obscura runtime readiness safely with zero background spawn."""
    binary = resolve_obscura_binary()
    return {
        "skill": "obscura-browser",
        "installed": binary is not None,
        "binary": binary,
        "install_hint": "Install or set OBSCURA_BIN=/path/to/obscura, or run scripts/optional_skill_bootstrap.py obscura-browser --install",
    }


def fetch_page(url: str, *, mode: str = "text", timeout_s: int = 30) -> Dict[str, object]:
    """Invoke Obscura CLI on-demand to extract page text or snapshot JSON."""
    binary = resolve_obscura_binary()
    if not binary:
        return {"ok": False, "error": "obscura binary not installed (lazy on-demand load required)", **inspect_status()}
    proc = subprocess.run(
        [binary, "fetch", url, "--format", mode, "--timeout", str(timeout_s)],
        text=True,
        capture_output=True,
        check=False,
    )
    return {
        "ok": proc.returncode == 0,
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr.strip(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="On-demand Obscura browser wrapper.")
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_st = sub.add_parser("status", help="Check Obscura binary availability.")
    p_st.add_argument("--json", action="store_true")
    p_fetch = sub.add_parser("fetch", help="Fetch a page on-demand.")
    p_fetch.add_argument("url")
    p_fetch.add_argument("--mode", default="text", choices=("text", "html", "links", "json"))
    p_fetch.add_argument("--timeout", type=int, default=30)

    args = parser.parse_args()
    if args.cmd == "status":
        print(json.dumps(inspect_status(), indent=2, ensure_ascii=False))
        return 0
    res = fetch_page(args.url, mode=args.mode, timeout_s=args.timeout)
    print(json.dumps(res, indent=2, ensure_ascii=False))
    return 0 if res.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
