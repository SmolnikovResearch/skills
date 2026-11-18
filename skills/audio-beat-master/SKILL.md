---
name: audio-beat-master
description: Synthesize beat grids and normalize audio to -16 LUFS.
version: 1.0.0
author: Smolnikov Research
license: MIT
platforms: [linux, macos, windows]
metadata:
  capyagent:
    tags: [audio, beats, lufs, mastering, ffmpeg]
    category: media
    related_skills: [ffmpeg-editor, songwriting-and-ai-music, songsee]
---

# Audio Beat Master

Generate beat-locked original backing stems, detect sub-`120Hz` kick/bass onset timestamps for video cut alignment, and verify EBU R128 loudness (`-16 LUFS`, true peak `<= -4 dBFS`) using pure Python plus `ffmpeg`.

## Core Commands via Terminal

1. Generate a clean royalty-free beat-synced WAV stem at a given BPM and duration:

```bash
python3 SKILL_DIR/scripts/audio_master.py synth --bpm 120 --duration 15 --output beat.wav
```

2. Detect sub-`120Hz` beat onset timestamps (in seconds) for storyboard cut timing:

```bash
python3 SKILL_DIR/scripts/audio_master.py beats beat.wav --json
```

3. Measure and normalize audio to `-16 LUFS` with true-peak ceiling `-4.0 dBFS`:

```bash
python3 SKILL_DIR/scripts/audio_master.py master beat.wav mastered.wav --json
```
