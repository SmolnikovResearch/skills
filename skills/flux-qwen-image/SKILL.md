---
name: flux-qwen-image
description: On-demand image generation with FLUX Klein and Qwen.
version: 1.0.0
author: Smolnikov Research
license: MIT
platforms: [linux, macos, windows]
metadata:
  capyagent:
    tags: [image, generation, flux, qwen, optional]
    category: media
    related_skills: [comfyui, logo-design]
---

# FLUX Klein and Qwen-Image On-Demand Studio

Text-to-image and poster cover generation using FLUX 3 Image Klein or Qwen-Image-2.1, remaining completely unloaded until the user installs the optional skill or triggers model bootstrap.

## Lazy Activation and On-Demand Bootstrap

```bash
python3 scripts/optional_skill_bootstrap.py flux-qwen-image --status
python3 scripts/optional_skill_bootstrap.py flux-qwen-image --install --models
```

## Usage via Terminal

Inspect configured local weights or remote inference endpoints first, then render images only on demand:

```bash
python3 SKILL_DIR/scripts/image_gen_client.py status --json
python3 SKILL_DIR/scripts/image_gen_client.py generate --prompt "Minimalist editorial poster" --output poster.png
```
