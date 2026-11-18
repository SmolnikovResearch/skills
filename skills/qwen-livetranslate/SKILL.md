---
name: qwen-livetranslate
description: On-demand real-time speech and video stream translation.
version: 1.0.0
author: Smolnikov Research
license: MIT
platforms: [linux, macos, windows]
metadata:
  capyagent:
    tags: [translation, speech, audio, streaming, optional]
    category: media
    related_skills: [ffmpeg-editor, youtube-content]
---

# Qwen LiveTranslate (On-Demand)

Real-time speech-to-speech and bilingual subtitle translation for calls, recordings, and video streams, isolated in `optional-skills` and loaded strictly when the user turns it on.

## Lazy Activation and On-Demand Bootstrap

```bash
python3 scripts/optional_skill_bootstrap.py qwen-livetranslate --status
python3 scripts/optional_skill_bootstrap.py qwen-livetranslate --install --models
```

## Usage via Terminal

Inspect runtime state or translate an extracted audio/subtitle track on-demand via `SKILL_DIR/scripts/livetranslate_stream.py`:

```bash
python3 SKILL_DIR/scripts/livetranslate_stream.py status --json
python3 SKILL_DIR/scripts/livetranslate_stream.py translate input.wav --target-lang ru --json
```
