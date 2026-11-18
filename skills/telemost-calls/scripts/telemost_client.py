#!/usr/bin/env python3
"""On-demand call joining and transcript client for Telemost, Zoom, Webex, and Google Meet."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Dict, Optional

SUPPORTED_PLATFORMS = ("telemost", "zoom", "webex", "google_meet")
JOIN_DEADLINE_S = 90
API_DEADLINE_S = 30


def detect_platform(url: str) -> str:
    """Infer call platform slug from URL host."""
    host = urllib.parse.urlparse(url.strip()).netloc.lower()
    if "telemost.yandex" in host or "telemost.360.yandex" in host:
        return "telemost"
    if "zoom.us" in host:
        return "zoom"
    if "webex.com" in host:
        return "webex"
    if "meet.google.com" in host:
        return "google_meet"
    return "unknown"


def inspect_status() -> Dict[str, Any]:
    """Read-only check of configured MeetScribe URL and local meeting_recorder runtime tools."""
    endpoint = os.environ.get("MEETSCRIBE_URL", "").strip()
    local_mcp_bins = {
        "capy-meet-mcp": shutil.which("capy-meet-mcp") is not None,
        "ffmpeg": shutil.which("ffmpeg") is not None,
        "xvfb-run": shutil.which("xvfb-run") is not None,
        "pactl": shutil.which("pactl") is not None,
    }
    return {
        "skill": "telemost-calls",
        "auto_load_on_startup": False,
        "supported_platforms": list(SUPPORTED_PLATFORMS),
        "remote_meetscribe_configured": bool(endpoint),
        "remote_meetscribe_url": endpoint or None,
        "local_tools": local_mcp_bins,
        "ready": bool(endpoint or (local_mcp_bins["capy-meet-mcp"] and local_mcp_bins["ffmpeg"])),
    }


def _meetscribe_request(
    method: str,
    path: str,
    payload: Optional[dict] = None,
    *,
    timeout: int = API_DEADLINE_S,
) -> Any:
    base = os.environ.get("MEETSCRIBE_URL", "").strip().rstrip("/")
    if not base:
        raise RuntimeError(
            "MEETSCRIBE_URL is not configured. Use optional-mcps/meeting_recorder (join_meeting) "
            "for local recording or set MEETSCRIBE_URL=http://127.0.0.1:8000."
        )
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(f"{base}{path}", data=body, method=method)
    req.add_header("Content-Type", "application/json")
    token = os.environ.get("MEETSCRIBE_TOKEN", "").strip()
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:300]
        raise RuntimeError(f"MeetScribe HTTP {exc.code}: {detail}") from None
    except urllib.error.URLError as exc:
        raise RuntimeError(f"MeetScribe unreachable at {base}: {exc.reason}") from None
    return json.loads(raw) if raw else {}


def join_call(url: str, *, platform: str = "auto", display_name: str = "CapyAgent") -> Dict[str, Any]:
    """Dispatch call-bot join request to MeetScribe API."""
    resolved = detect_platform(url) if platform == "auto" else platform.strip().lower()
    if resolved not in SUPPORTED_PLATFORMS:
        raise ValueError(f"Unsupported platform {resolved!r}; choose one of {', '.join(SUPPORTED_PLATFORMS)}")
    return _meetscribe_request(
        "POST",
        "/api/bot/join",
        {
            "meeting_url": url.strip(),
            "platform": resolved,
            "display_name": display_name.strip() or "CapyAgent",
        },
        timeout=JOIN_DEADLINE_S,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Telemost/Zoom/Meet on-demand call assistant.")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status", help="Inspect readiness without connecting.").add_argument("--json", action="store_true")

    p_det = sub.add_parser("detect", help="Detect platform from URL.")
    p_det.add_argument("url")

    p_join = sub.add_parser("join", help="Send recording bot to a call via MEETSCRIBE_URL.")
    p_join.add_argument("url")
    p_join.add_argument("--platform", default="auto")
    p_join.add_argument("--name", default="CapyAgent")

    p_st = sub.add_parser("bot-status", help="Fetch bot status by ID.")
    p_st.add_argument("bot_id")

    p_list = sub.add_parser("transcripts", help="List recent transcripts.")
    p_list.add_argument("--limit", type=int, default=20)

    p_tr = sub.add_parser("transcript", help="Fetch transcript text by ID.")
    p_tr.add_argument("transcript_id")

    args = parser.parse_args()
    if args.cmd == "status":
        print(json.dumps(inspect_status(), indent=2, ensure_ascii=False))
        return 0
    if args.cmd == "detect":
        print(json.dumps({"url": args.url, "platform": detect_platform(args.url)}, ensure_ascii=False))
        return 0
    try:
        if args.cmd == "join":
            out = join_call(args.url, platform=args.platform, display_name=args.name)
        elif args.cmd == "bot-status":
            out = _meetscribe_request("GET", f"/api/bot/{urllib.parse.quote(args.bot_id)}")
        elif args.cmd == "transcripts":
            out = _meetscribe_request("GET", f"/api/transcripts?limit={int(args.limit)}")
        elif args.cmd == "transcript":
            out = _meetscribe_request("GET", f"/api/transcripts/{urllib.parse.quote(args.transcript_id)}")
        else:
            return 2
    except (RuntimeError, ValueError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
        return 1
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
