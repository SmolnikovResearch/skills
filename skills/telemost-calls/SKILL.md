---
name: telemost-calls
description: Join Yandex Telemost, Zoom, Meet calls and transcribe.
version: 1.0.0
author: Smolnikov Research
license: MIT
platforms: [linux, macos, windows]
metadata:
  capyagent:
    tags: [telemost, zoom, google-meet, calls, transcription, russia]
    category: communication
    related_skills: [meeting-minutes, meeting-action-items, qwen-livetranslate]
---

# Telemost & Online Calls Recording Skill

Join online video calls on **Yandex Telemost** (`telemost.yandex.ru`, `telemost.360.yandex.ru`), **Zoom**, **Webex**, and **Google Meet**, record audio reliably, and transcribe conversations locally or through MeetScribe for structured `meeting-minutes` summaries.

## Critical Routing Rule

Never send a video meeting link (`telemost.yandex.ru`, `meet.google.com`, `zoom.us`) into a standard headless browser tool: generic headless browsers lack an audio sink and join silently with zero recorded audio. Route call links through `meeting_recorder` MCP (`join_meeting`, `meeting_status`, `leave_meeting`, `get_transcript`) or the `telemost_client.py` bridge below.

## Lazy Activation and On-Demand Bootstrap

This skill ships inside `optional-skills` (`auto_load_on_startup: false`) and loads runtime components only when enabled:

```bash
python3 scripts/optional_skill_bootstrap.py telemost-calls --status
python3 scripts/optional_skill_bootstrap.py telemost-calls --install
```

Supported execution backends:

1. **Local MCP (`meeting_recorder` / `capy-meet-mcp`)**: No API keys required. Joins muted with camera off into an isolated virtual sink + Xvfb session (`capymeet-<id>.scope`), waits up to `90s` in lobby, confirms entry only when WAV bytes grow, and transcribes locally with `faster-whisper`.
2. **Remote MeetScribe HTTP service (`MEETSCRIBE_URL`)**: Sends join/status/transcript API calls to a running MeetScribe instance (`MEETSCRIBE_TOKEN` optional).

## Usage via Terminal

Inspect readiness or auto-detect platform and inspect remote MeetScribe transcripts using `SKILL_DIR/scripts/telemost_client.py`:

```bash
python3 SKILL_DIR/scripts/telemost_client.py status --json
python3 SKILL_DIR/scripts/telemost_client.py detect "https://telemost.yandex.ru/j/123456"
python3 SKILL_DIR/scripts/telemost_client.py join "https://telemost.yandex.ru/j/123456" --name "CapyAgent"
python3 SKILL_DIR/scripts/telemost_client.py transcripts --limit 10
```

Notice that any guest recording bot appears visibly in the call roster under `display_name`; inform meeting participants before admitting the bot, then pass finished transcripts into `meeting-minutes` or `meeting-action-items` via `read_file`.
