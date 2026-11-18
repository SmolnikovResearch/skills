---
name: browser-live-session
description: Work in signed-in browser tabs with user approval.
version: 1.0.0
author: Smolnikov Research
license: MIT
platforms: [linux, macos, windows]
metadata:
  capyagent:
    tags: [browser, live-session, tabs, relay, auth, chrome]
    category: browser
    related_skills: [capy-desktop-control, obscura-browser, pomerado-mcp]
---

# Live Signed-In Browser Session Skill

Connect CapyAgent to the user's real signed-in browser cleanly via the local `capy-browser-relay` extension bridge (`127.0.0.1:18791`) rather than launching an empty unauthenticated browser.

## When to Use

Use this skill when a workflow needs authenticated access to web apps (CRM dashboards, recruiting portals, admin consoles, publishing panels) where the user is already signed in, while strictly isolating agent tabs and respecting user control.

## Operating Contract

1. **Visible Isolated Tab Group:** Create or focus tabs inside an isolated collapsed session group (`capyagent/<session>`, `active: false` by default) so the user can observe progress without interrupting foreground typing.
2. **Explicit Tab Borrowing:** Never capture or mutate a user-owned tab silently. Request a temporary lease via `request_tab_lease(tab_id, reason)` and always release it via `release_tab_lease(tab_id, lease_id)` upon completion.
3. **Human Handoff on Verification Gates:** Whenever CAPTCHA, anti-bot challenge, 2FA prompt, password entry, or payment confirmation appears (`detect_human_gate`), return `needs_human: true` immediately and let the user complete it directly. Never bypass security checks.
4. **Local Terminal Interface (`SKILL_DIR/scripts/browser_live_client.py`):** Works with any CLI-capable agent via JSON commands (`status`, `open-tab`, `lease-request`, `lease-release`, `check-gate`).

## Lazy Activation and On-Demand Bootstrap

This skill ships inside `optional-skills` (`auto_load_on_startup: false`):

```bash
python3 scripts/optional_skill_bootstrap.py browser-live-session --status
python3 SKILL_DIR/scripts/browser_live_client.py status --json
```
