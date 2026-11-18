---
name: promo-video-maker
description: Storyboard-driven 1080p launch promo video builder.
version: 1.0.0
author: Smolnikov Research
license: MIT
platforms: [linux, macos, windows]
metadata:
  capyagent:
    tags: [promo, video, storyboard, launch, motion]
    category: media
    related_skills: [ffmpeg-editor, audio-beat-master, ascii-video]
---

# Launch Promo Video Maker

Build beat-synced `1920x1080` product promo videos from a structured shot storyboard JSON, crisp typographic frames, poster covers, and EBU R128 mastered audio without generic fade slideshows.

## Production Sequence

1. **Author Storyboard JSON**: Define a `15s`-`30s` sequence locked to a fixed BPM (`120 BPM` = `0.5s` per beat, `15 frames` at `30fps`), split into clear narrative acts:
   - Hook (problem contrast in under `3s`)
   - Product Core (real terminal/agent/workflow capability)
   - Security and Design Craft Proof (verified metrics/badges)
   - Closing Mark + Action CTA (`CapyAgent Beta`)
2. **Synthesize or Align Audio**: Use `audio-beat-master` to generate a beat grid or extract sub-`120Hz` onsets and normalize loudness to `-16 LUFS` (`TP <= -4 dBFS`).
3. **Render Frames and Encode**: Use `scripts/generate_capyagent_promo.py` or `ffmpeg-editor` via `terminal` to render crisp 1080p `yuv420p` H.264 MP4 and extract a matching `cover.png`.
4. **Ship Companion Copy**: Write a concise bilingual/Russian launch post (`launch-post-ru.md`) anchored only to verified release capabilities via `write_file`.
