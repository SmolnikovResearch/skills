# Smolnikov Research Agent Skills

Open-source collection of **19 clean-room AI agent skills** by **Smolnikov Research Center**, published under the MIT license.

Every skill is available both in this unified catalog repository and as an **independent dedicated repository** under [`@SmolnikovResearch`](https://github.com/SmolnikovResearch), each shipping with compact YAML frontmatter and explicit **lazy on-demand dependency manifests** (`on-demand.json`, `auto_load_on_startup: false`).

---

## Catalog (19 Standalone Repositories)

### Security & Auditing
| Skill | Standalone Repo | Purpose | On-Demand Dependencies |
|---|---|---|---|
| [`security-audit`](skills/security-audit/SKILL.md) | [SmolnikovResearch/security-audit](https://github.com/SmolnikovResearch/security-audit) | Two-phase attack surface discovery, secret hygiene, and release bundle audit | Pure Python stdlib |
| [`ego-lite-reversing`](skills/ego-lite-reversing/SKILL.md) | [SmolnikovResearch/ego-lite-reversing](https://github.com/SmolnikovResearch/ego-lite-reversing) | Defensive static inspection of compiled binaries and shipped web bundles | Optional `radare2` / `ego-lite` |

### Design, UI/UX Craft & Brand Vectors
| Skill | Standalone Repo | Purpose | On-Demand Dependencies |
|---|---|---|---|
| [`unslop`](skills/unslop/SKILL.md) | [SmolnikovResearch/unslop](https://github.com/SmolnikovResearch/unslop) | Static anti-slop UI linter (`tabular-nums`, easing curves, `prefers-reduced-motion`, border restraint) | Pure Python |
| [`hallmark-styles`](skills/hallmark-styles/SKILL.md) | [SmolnikovResearch/hallmark-styles](https://github.com/SmolnikovResearch/hallmark-styles) | 12 curated non-generic UI design systems and semantic token palettes | Reference catalog |
| [`learn-taste`](skills/learn-taste/SKILL.md) | [SmolnikovResearch/learn-taste](https://github.com/SmolnikovResearch/learn-taste) | Extracts CSS variables, typography, radii, and motion curves into a reusable taste profile | Pure Python |
| [`logo-design`](skills/logo-design/SKILL.md) | [SmolnikovResearch/logo-design](https://github.com/SmolnikovResearch/logo-design) | Optical-grid SVG mark crafting and vector accessibility/safety validator | Pure Python XML |
| [`design-md`](skills/design-md/SKILL.md) | [SmolnikovResearch/design-md](https://github.com/SmolnikovResearch/design-md) | Project `DESIGN.md` brand contract generator and AI-slop layout auditor | Pure Python |
| [`ui-sdk-builder`](skills/ui-sdk-builder/SKILL.md) | [SmolnikovResearch/ui-sdk-builder](https://github.com/SmolnikovResearch/ui-sdk-builder) | Accessible WAI-ARIA agent UI primitives (`menu`, `form`, `approval-card`, `table`) | Pure Python |

### Video & Audio Production
| Skill | Standalone Repo | Purpose | On-Demand Dependencies |
|---|---|---|---|
| [`ffmpeg-editor`](skills/ffmpeg-editor/SKILL.md) | [SmolnikovResearch/ffmpeg-editor](https://github.com/SmolnikovResearch/ffmpeg-editor) | Deterministic `ffprobe`, poster cover extraction, and `-16 LUFS` H.264/AAC muxing | `ffmpeg`, `ffprobe` |
| [`promo-video-maker`](skills/promo-video-maker/SKILL.md) | [SmolnikovResearch/promo-video-maker](https://github.com/SmolnikovResearch/promo-video-maker) | Beat-synced `1920x1080` launch promo video assembly from storyboard JSON | `ffmpeg`, `pillow` |
| [`audio-beat-master`](skills/audio-beat-master/SKILL.md) | [SmolnikovResearch/audio-beat-master](https://github.com/SmolnikovResearch/audio-beat-master) | Harmonic beat-grid synthesis, sub-120 Hz onset detection, and EBU R128 mastering | `ffmpeg` |

### Desktop & Browser Control (On-Demand)
| Skill | Standalone Repo | Purpose | On-Demand Dependencies |
|---|---|---|---|
| [`capy-desktop-control`](skills/capy-desktop-control/SKILL.md) | [SmolnikovResearch/capy-desktop-control](https://github.com/SmolnikovResearch/capy-desktop-control) | Native macOS/Windows/Linux accessibility-tree control via pinned `agent-desktop` v1.0.2 | `agent-desktop` v1.0.2 (SHA-256 verified) |
| [`browser-live-session`](skills/browser-live-session/SKILL.md) | [SmolnikovResearch/browser-live-session](https://github.com/SmolnikovResearch/browser-live-session) | Live signed-in browser tabs in isolated group with user lease approval & human gate handoff | `capy-browser-relay` (`127.0.0.1:18791`) |
| [`obscura-browser`](skills/obscura-browser/SKILL.md) | [SmolnikovResearch/obscura-browser](https://github.com/SmolnikovResearch/obscura-browser) | Low-RAM stealth headless browser runner with explicit launch guard | `obscura` binary (`OBSCURA_BIN`) |
| [`pomerado-mcp`](skills/pomerado-mcp/SKILL.md) | [SmolnikovResearch/pomerado-mcp](https://github.com/SmolnikovResearch/pomerado-mcp) | Convert HAR traces and authenticated web flows into typed MCP server stubs | `pomerado` (`POMERADO_BIN`) |

### Calls & Meetings (Telemost / MeetScribe)
| Skill | Standalone Repo | Purpose | On-Demand Dependencies |
|---|---|---|---|
| [`telemost-calls`](skills/telemost-calls/SKILL.md) | [SmolnikovResearch/telemost-calls](https://github.com/SmolnikovResearch/telemost-calls) | Join Yandex Telemost, Zoom, Webex & Google Meet calls and extract transcripts | `MEETSCRIBE_URL` or `meeting_recorder` MCP (`ffmpeg`) |

### Generative Media (On-Demand)
| Skill | Standalone Repo | Purpose | On-Demand Dependencies |
|---|---|---|---|
| [`voxcpm2-voice`](skills/voxcpm2-voice/SKILL.md) | [SmolnikovResearch/voxcpm2-voice](https://github.com/SmolnikovResearch/voxcpm2-voice) | 48 kHz voice cloning and speech synthesis via local checkpoints or HTTP endpoint | `torch`, `soundfile`, `OpenBMB/VoxCPM2` |
| [`flux-qwen-image`](skills/flux-qwen-image/SKILL.md) | [SmolnikovResearch/flux-qwen-image](https://github.com/SmolnikovResearch/flux-qwen-image) | FLUX 3 Image Klein and Qwen-Image-2.1 image generation wrapper | `torch`, `diffusers`, `transformers`, `Qwen/Qwen-Image` |
| [`qwen-livetranslate`](skills/qwen-livetranslate/SKILL.md) | [SmolnikovResearch/qwen-livetranslate](https://github.com/SmolnikovResearch/qwen-livetranslate) | Real-time speech and video stream translation workflow | `ffmpeg`, `torch`, `transformers`, `Qwen/Qwen3-Omni` |

---

## Installation in CapyAgent / Skills Hub

Install from either an individual skill repository or this catalog repository:

```bash
# Install from an individual skill repo
capyagent skills install SmolnikovResearch/unslop/skills/unslop
capyagent skills install SmolnikovResearch/ffmpeg-editor/skills/ffmpeg-editor

# Or install from the multi-skill catalog repo
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

All 19 skills and helper scripts follow clean-room authoring rules (no embedded secrets, zero hidden Unicode/HTML/URL exfil patterns, valid frontmatter <= 60 chars, syntax-checked Python helpers):

```bash
python3 scripts/validate_skills.py
```

## License

MIT - [Smolnikov Research Center](https://github.com/SmolnikovResearch)
