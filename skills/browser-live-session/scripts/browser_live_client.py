#!/usr/bin/env python3
"""Clean-room client helpers for local live signed-in browser relay sessions."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from typing import Any, Dict, Optional

DEFAULT_RELAY_URL = "http://127.0.0.1:18791"

_HUMAN_GATE_PATTERNS = {
    "captcha": re.compile(r"\b(captcha|recaptcha|hcaptcha|turnstile|verify you are human|капча)\b", re.I),
    "two_factor": re.compile(r"\b(2fa|two-factor|one-time code|otp|authenticator|код подтверждения)\b", re.I),
    "login_password": re.compile(r"\b(type=\"password\"|enter password|введите пароль|sign in required)\b", re.I),
    "payment_confirm": re.compile(r"\b(3ds|confirm payment|оплатить|cvv|cvc)\b", re.I),
}


def inspect_status() -> Dict[str, Any]:
    return {
        "skill": "browser-live-session",
        "auto_load_on_startup": False,
        "relay_url": os.environ.get("CAPY_BROWSER_RELAY_URL", DEFAULT_RELAY_URL),
        "token_configured": bool(os.environ.get("CAPY_BROWSER_RELAY_TOKEN", "").strip()),
    }


def make_tab_group_title(agent_name: str, session_id: str) -> str:
    """Build bounded (<=40 chars) session group label for isolated visible browser work."""
    raw = f"{agent_name.strip() or 'capyagent'}/{session_id.strip() or 'default'}"
    cleaned = re.sub(r"[^a-zA-Z0-9_./-]+", "-", raw)
    return cleaned[:40]


def request_tab_lease(tab_id: int, reason: str, approved: bool = False) -> Dict[str, Any]:
    """Build or finalize an explicit user-approved temporary borrow request for an existing tab."""
    clean_reason = reason.strip()[:180]
    if not approved:
        return {
            "ok": False,
            "needs_human": True,
            "action": "tab_lease_request",
            "tab_id": int(tab_id),
            "reason": clean_reason,
            "message": "Explicit user approval required before borrowing user tab.",
        }
    lease_seed = f"{tab_id}:{clean_reason}".encode("utf-8")
    lease_id = "lease_" + hashlib.sha256(lease_seed).hexdigest()[:12]
    return {
        "ok": True,
        "needs_human": False,
        "action": "tab_lease_granted",
        "tab_id": int(tab_id),
        "lease_id": lease_id,
        "reason": clean_reason,
    }


def release_tab_lease(tab_id: int, lease_id: str) -> Dict[str, Any]:
    """Return a borrowed user tab after task completion."""
    return {
        "ok": True,
        "action": "tab_lease_released",
        "tab_id": int(tab_id),
        "lease_id": str(lease_id).strip(),
    }


def detect_human_gate(text_or_html: str, has_password_field: bool = False) -> Dict[str, Any]:
    """Return ``needs_human=True`` when interactive user verification is required."""
    if has_password_field:
        return {"needs_human": True, "gate": "login_password"}
    sample = str(text_or_html or "")
    for gate, rx in _HUMAN_GATE_PATTERNS.items():
        if rx.search(sample):
            return {"needs_human": True, "gate": gate}
    return {"needs_human": False, "gate": None}


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Live browser session helper.")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status")
    g = sub.add_parser("check-gate")
    g.add_argument("--text", default="")
    g.add_argument("--password", action="store_true")
    l = sub.add_parser("lease-request")
    l.add_argument("--tab-id", type=int, required=True)
    l.add_argument("--reason", required=True)
    l.add_argument("--approved", action="store_true")
    args = parser.parse_args(argv)
    if args.cmd == "status":
        print(json.dumps(inspect_status(), ensure_ascii=False, indent=2))
    elif args.cmd == "check-gate":
        print(json.dumps(detect_human_gate(args.text, has_password_field=args.password), ensure_ascii=False, indent=2))
    elif args.cmd == "lease-request":
        print(json.dumps(request_tab_lease(args.tab_id, args.reason, approved=args.approved), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
