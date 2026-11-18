---
name: voxcpm2-voice
description: On-demand 48kHz voice cloning and TTS with VoxCPM2.
version: 1.0.0
author: Smolnikov Research
license: MIT
platforms: [linux, macos, windows]
metadata:
  capyagent:
    tags: [tts, voice, audio, generative, optional]
    category: media
    related_skills: [audio-beat-master, ffmpeg-editor]
---

# VoxCPM2 48kHz Voice Cloning and TTS (On-Demand)

High-fidelity `48 kHz` bilingual text-to-speech and reference-prompt voice synthesis backed by user-selected VoxCPM2 local checkpoints or an inference endpoint. Zero weights are downloaded until you explicitly bootstrap the skill.

## Lazy Activation and On-Demand Bootstrap

```bash
python3 scripts/optional_skill_bootstrap.py voxcpm2-voice --status
python3 scripts/optional_skill_bootstrap.py voxcpm2-voice --install --models
```

## Synthesis via Terminal

Check local checkpoint / GPU readiness or render voiceover WAV stems cleanly before normalizing to `-16 LUFS` with `audio-beat-master`:

```bash
python3 SKILL_DIR/scripts/voxcpm2_tts.py status --json
python3 SKILL_DIR/scripts/voxcpm2_tts.py synthesize --text "CapyAgent Beta is ready." --output voice.wav
```
