---
name: ffmpeg-editor
description: Deterministic FFmpeg video/audio pipeline helpers.
version: 1.0.0
author: Smolnikov Research
license: MIT
platforms: [linux, macos, windows]
metadata:
  capyagent:
    tags: [ffmpeg, video, audio, editing, pipeline]
    category: media
    related_skills: [youtube-content, ascii-video, manim-video]
---

# FFmpeg Editor Pipeline

Run repeatable FFmpeg/FFprobe workflows for cutting, scaling to `1920x1080`, concatenating storyboard segments, extracting poster covers, and muxing EBU R128 loudness-normalized audio tracks.

## Core Operations via Terminal

1. Probe stream metadata and durations:

```bash
python3 SKILL_DIR/scripts/ffmpeg_pipeline.py probe input.mp4 --json
```

2. Mux a normalized audio stem (`-16 LUFS`, true peak `<= -4 dBFS`) onto silent or raw rendered video:

```bash
python3 SKILL_DIR/scripts/ffmpeg_pipeline.py mux raw.mp4 soundtrack.wav out.mp4
```

3. Extract an optical cover frame (`1920x1080` PNG) at a chosen timestamp:

```bash
python3 SKILL_DIR/scripts/ffmpeg_pipeline.py cover out.mp4 4.5 cover.png
```

Always inspect final loudness, frame rate, and resolution via `ffprobe` and `probe` before publishing artifacts.
