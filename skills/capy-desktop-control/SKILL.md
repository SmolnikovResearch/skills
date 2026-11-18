---
name: capy-desktop-control
description: Control desktop apps via semantic accessibility refs.
version: 1.0.0
author: Smolnikov Research
license: MIT
platforms: [linux, macos, windows]
metadata:
  capyagent:
    tags: [desktop, computer-use, accessibility, automation, ui]
    category: desktop
    related_skills: [browser-live-session]
---

# Native Desktop Control (`agent-desktop` Backend)

Operate native desktop applications on macOS, Windows, and Linux through structured accessibility-tree snapshots and semantic `@ref` actions via the `tools.computer_use.agent_desktop_backend` adapter, without stealing focus or relying on blind pixel guessing.

## When to Use

Use this skill when an automated workflow must inspect windows, read accessibility trees, click UI controls, fill native form fields, or trigger window shortcuts in desktop apps outside a web browser.

## Lazy Activation and On-Demand Setup

This skill ships inside `optional-skills` (`auto_load_on_startup: false`) and downloads/verifies the pinned `agent-desktop` `v1.0.2` binary (`Apache-2.0`) only on explicit request:

```bash
python3 SKILL_DIR/scripts/desktop_control.py status --json
python3 SKILL_DIR/scripts/desktop_control.py pins
python3 SKILL_DIR/scripts/desktop_control.py verify /path/to/agent-desktop
```

To enable the backend for `computer_use`:

```bash
export CAPYAGENT_COMPUTER_USE_BACKEND=agent-desktop
export CAPYAGENT_AGENT_DESKTOP_CMD=/path/to/agent-desktop
```

## Safety and Observe-Act-Reobserve Loop

1. Always list windows and take an accessibility snapshot (`snapshot --window-id <id> -i --compact --include-bounds`) before issuing semantic input.
2. Re-read the target window tree after every state-changing action (`click`, `right-click`, `type`, `set-value`, `scroll`, `press`).
3. Never retry blindly after `STALE_REF`, `AMBIGUOUS_TARGET`, or `POLICY_DENIED`; inspect the refreshed snapshot first.
4. External HTTP(S) URLs embedded in element labels and physical coordinate fallback without `CAPYAGENT_AGENT_DESKTOP_HEADED=1` remain blocked by default.
