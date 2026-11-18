#!/usr/bin/env python3
"""CLI and SHA-256 verification helper for pinned agent-desktop v1.0.2 binaries."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Dict

AGENT_DESKTOP_VERSION = "v1.0.2"
AGENT_DESKTOP_LICENSE = "Apache-2.0"

PLATFORM_PINS: Dict[str, Any] = {
    "linux/amd64": [
        {
            "name": "agent-desktop",
            "size": 6967864,
            "sha256": "05427281a6746489bc0e15c16698a70a86322125c76c7a9e2f4c2d7a12bf7c5b",
        },
        {
            "name": "agent-desktop-linux-clipboard-owner",
            "size": 586512,
            "sha256": "bf17de139902724e86b3616970b7b7f16f5f1fb4143910b532a38dd2182720fa",
        },
    ],
    "linux/arm64": [
        {
            "name": "agent-desktop",
            "size": 5648808,
            "sha256": "529ae49006278f778bcda6b68d7460a55148e2cefb1cb69a23485381d9dbdec0",
        },
        {
            "name": "agent-desktop-linux-clipboard-owner",
            "size": 512640,
            "sha256": "dcd6f2ce9a0e92e42f4d2ee9161ea1b9f2b11c0e4b1878119a19c0a2db3630a6",
        },
    ],
    "darwin/amd64": [
        {
            "name": "agent-desktop",
            "size": 4378968,
            "sha256": "9684916bb4b5486c02cef8b2d480e55a551639b08358284f90a87cef43b2da8b",
        },
        {
            "name": "agent-desktop-macos-helper",
            "size": 571156,
            "sha256": "ce52467818ac601ae1145a0b9ecaa14aaf04d2e72d24cf6d29d26757340f9c6b",
        },
    ],
    "darwin/arm64": [
        {
            "name": "agent-desktop",
            "size": 3741392,
            "sha256": "bf0a3c9256512f2f57288d37ccd17d7f03665fccc53c2f74011a49b98e61ba59",
        },
        {
            "name": "agent-desktop-macos-helper",
            "size": 529616,
            "sha256": "522829116cb006b5770c6a82b361f466a4775f794d6af4083e75231a2d6bb551",
        },
    ],
    "windows/amd64": [
        {
            "name": "agent-desktop.exe",
            "size": 3464704,
            "sha256": "409e58cbdd6aed47e29771ffa60bc122a9843505a227af488cded85215943988",
        },
    ],
}


def verify_pinned_binary(binary_path: Path, platform_key: str) -> Dict[str, Any]:
    """Verify binary size and SHA-256 against the pinned v1.0.2 manifest."""
    entries = PLATFORM_PINS.get(platform_key)
    if not entries:
        return {"ok": False, "error": f"Unsupported platform: {platform_key}"}
    if not binary_path.is_file():
        return {"ok": False, "error": f"File not found: {binary_path}"}

    data = binary_path.read_bytes()
    actual_sha = hashlib.sha256(data).hexdigest()
    actual_size = len(data)
    match = next((e for e in entries if e["name"] == binary_path.name), entries[0])
    ok = actual_sha == match["sha256"] and actual_size == match["size"]
    return {
        "ok": ok,
        "version": AGENT_DESKTOP_VERSION,
        "license": AGENT_DESKTOP_LICENSE,
        "expected_sha256": match["sha256"],
        "actual_sha256": actual_sha,
        "expected_size": match["size"],
        "actual_size": actual_size,
    }


def inspect_status() -> Dict[str, Any]:
    return {
        "skill": "capy-desktop-control",
        "auto_load_on_startup": False,
        "version": AGENT_DESKTOP_VERSION,
        "license": AGENT_DESKTOP_LICENSE,
        "platforms": sorted(PLATFORM_PINS.keys()),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Inspect and verify agent-desktop binaries.")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status")
    sub.add_parser("pins")
    v = sub.add_parser("verify")
    v.add_argument("path")
    v.add_argument("--platform", default="linux/amd64")
    args = parser.parse_args(argv)
    if args.cmd == "status":
        print(json.dumps(inspect_status(), ensure_ascii=False, indent=2))
    elif args.cmd == "pins":
        print(json.dumps({"version": AGENT_DESKTOP_VERSION, "pins": PLATFORM_PINS}, ensure_ascii=False, indent=2))
    elif args.cmd == "verify":
        res = verify_pinned_binary(Path(args.path), args.platform)
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 0 if res.get("ok") else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
