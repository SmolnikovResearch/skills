# Smolnikov Research Agent Skills

Open-source collection of **14 clean-room AI agent skills** by **Smolnikov Research Center**, published under the MIT license.

Every skill follows strict authoring standards (compact YAML frontmatter, zero bloat in default prompts) and ships with explicit **lazy on-demand dependency manifests** (`on-demand.json`, `auto_load_on_startup: false`) so nothing heavy is installed or loaded until a user explicitly asks for it.

---

## Catalog (14 Skills)

### Security & Auditing
| Skill | Purpose | On-Demand Dependencies |
|---|---|---|
| [`security-audit`](skills/security-audit/SKILL.md) | Two-phase attack surface discovery, secret hygiene, and release bundle audit | Pure Python stdlib |
| [`ego-lite-reversing`](skills/ego-lite-reversing/SKILL.md) | Defensive static inspection of compiled binaries and shipped web bundles | Optional `radare2` / `ego-lite` |

### Design, UI/UX Craft & Brand Vectors
| Skill | Purpose | On-Demand Dependencies |
|---|---|---|
| [`unslop`](skills/unslop/SKILL.md) | Static anti-slop UI linter (`tabular-nums`, easing curves, `prefers-reduced-motion`, border restraint) | Pure Python |
| [`hallmark-styles`](skills/hallmark-styles/SKILL.md) | 12 curated non-generic UI design systems and semantic token palettes | Reference catalog |
| [`learn-taste`](skills/learn-taste/SKILL.md) | Extracts CSS variables, typography, radii, and motion curves into a reusable taste profile | Pure Python |
| [`logo-design`](skills/logo-design/SKILL.md) | Optical-grid SVG mark crafting and vector accessibility/safety validator | Pure Python XML |

### Video & Audio Production
| Skill | Purpose | On-Demand Dependencies |
|---|---|---|
| [`ffmpeg-editor`](skills/ffmpeg-editor/SKILL.md) | Deterministic `ffprobe`, poster cover extraction, and `-16 LUFS` H.264/AAC muxing | `ffmpeg`, `ffprobe` |
| [`promo-video-maker`](skills/promo-video-maker/SKILL.md) | Beat-synced `1920x1080` launch promo video assembly from storyboard JSON | `ffmpeg`, `pillow` |
| [`audio-beat-master`](skills/audio-beat-master/SKILL.md) | Harmonic beat-grid synthesis, sub-120 Hz onset detection, and EBU R128 mastering | `ffmpeg` |

### Browser & Web-to-MCP (On-Demand)
| Skill | Purpose | On-Demand Dependencies |
|---|---|---|
| [`obscura-browser`](skills/obscura-browser/SKILL.md) | Low-RAM stealth headless browser runner with explicit launch guard | `obscura` binary (`OBSCURA_BIN`) |
| [`pomerado-mcp`](skills/pomerado-mcp/SKILL.md) | Convert HAR traces and authenticated web flows into typed MCP server stubs | `pomerado` (`POMERADO_BIN`) |

### Generative Media (On-Demand)
| Skill | Purpose | On-Demand Dependencies |
|---|---|---|
| [`voxcpm2-voice`](skills/voxcpm2-voice/SKILL.md) | 48 kHz voice cloning and speech synthesis via local checkpoints or HTTP endpoint | `torch`, `soundfile`, `OpenBMB/VoxCPM2` |
| [`flux-qwen-image`](skills/flux-qwen-image/SKILL.md) | FLUX 3 Image Klein and Qwen-Image-2.1 image generation wrapper | `torch`, `diffusers`, `transformers`, `Qwen/Qwen-Image` |
| [`qwen-livetranslate`](skills/qwen-livetranslate/SKILL.md) | Real-time speech and video stream translation workflow | `ffmpeg`, `torch`, `transformers`, `Qwen/Qwen3-Omni` |

---

## Installation in CapyAgent / Skills Hub

Install individual skills strictly on demand:

```bash
# Search official tap
capyagent skills search security-audit

# Install any skill by full tap identifier
capyagent skills install SmolnikovResearch/skills/skills/unslop
capyagent skills install SmolnikovResearch/skills/skills/ffmpeg-editor
capyagent skills install SmolnikovResearch/skills/skills/voxcpm2-voice
```

Or copy a skill folder directly into your agent's `~/.capyagent/skills/` (or `~/.agents/skills/`) directory.

## Lazy Dependency & Model Bootstrap (`on-demand.json`)

Each skill stays dormant until invoked. Inspect readiness without downloading anything:

```bash
python3 scripts/optional_skill_bootstrap.py voxcpm2-voice --status
```

Install Python dependencies only (dry-run or live), and optionally pull heavy model checkpoints only when `--models` is passed:

```bash
python3 scripts/optional_skill_bootstrap.py voxcpm2-voice --install --dry-run
python3 scripts/optional_skill_bootstrap.py voxcpm2-voice --install --models
```

## Validation & Security

All 14 skills and helper scripts follow clean-room authoring rules (no embedded secrets, zero hidden Unicode/HTML/URL exfil patterns, valid frontmatter <= 60 chars, syntax-checked Python helpers):

```bash
python3 scripts/validate_skills.py
```

## License

MIT - [Smolnikov Research Center](https://github.com/SmolnikovResearch)
