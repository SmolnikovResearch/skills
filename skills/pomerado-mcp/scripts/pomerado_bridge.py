#!/usr/bin/env python3
"""On-demand generator for Pomerado website-to-MCP tool manifests from HAR traces."""

from __future__ import annotations

import argparse
import json
import os
import shutil
from pathlib import Path
from typing import Dict, List
from urllib.parse import urlparse


def extract_api_endpoints_from_har(har_path: Path, *, max_endpoints: int = 20) -> List[Dict[str, str]]:
    """Inspect a captured HAR file safely without replaying credentials."""
    raw = json.loads(Path(har_path).read_text(encoding="utf-8"))
    entries = ((raw.get("log") or {}).get("entries") or [])
    seen = set()
    endpoints: List[Dict[str, str]] = []
    for entry in entries:
        req = entry.get("request") or {}
        method = str(req.get("method") or "GET").upper()
        url = str(req.get("url") or "")
        parsed = urlparse(url)
        if not parsed.scheme.startswith("http"):
            continue
        key = (method, f"{parsed.scheme}://{parsed.netloc}{parsed.path}")
        if key in seen:
            continue
        seen.add(key)
        endpoints.append({"method": method, "url": key[1], "host": parsed.netloc, "path": parsed.path})
        if len(endpoints) >= max_endpoints:
            break
    return endpoints


def build_mcp_stub(server_name: str, endpoints: List[Dict[str, str]]) -> Dict[str, object]:
    """Emit a side-effect-free JSON descriptor describing an on-demand MCP server bridge."""
    return {
        "name": server_name,
        "runtime": "pomerado",
        "binary_present": shutil.which("pomerado") is not None or bool(os.environ.get("POMERADO_BIN")),
        "endpoints": endpoints,
        "auth_env_hint": f"{server_name.upper().replace('-', '_')}_SESSION_COOKIE",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect HAR and generate on-demand Pomerado MCP stub.")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status", help="Report Pomerado binary readiness.")
    p_gen = sub.add_parser("from-har", help="Extract endpoint map from HAR.")
    p_gen.add_argument("har", help="Path to .har archive")
    p_gen.add_argument("--name", default="web-bridge")
    p_gen.add_argument("--output", default="")

    args = parser.parse_args()
    if args.cmd == "status":
        print(json.dumps(build_mcp_stub("status-check", []), indent=2))
        return 0
    endpoints = extract_api_endpoints_from_har(Path(args.har))
    doc = build_mcp_stub(args.name, endpoints)
    payload = json.dumps(doc, indent=2, ensure_ascii=False)
    if args.output:
        Path(args.output).write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
