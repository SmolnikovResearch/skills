#!/usr/bin/env python3
"""On-demand client and readiness checker for VoxCPM2 48kHz voice synthesis."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import urllib.request
from pathlib import Path
from typing import Dict, Optional


def default_model_dir() -> Path:
    return Path(os.environ.get("CAPYAGENT_MODELS_DIR", Path.home() / ".capyagent" / "cache" / "models")) / "voxcpm2"


def inspect_status() -> Dict[str, object]:
    """Check endpoint, local cached weights, and python deps without downloading."""
    model_dir = default_model_dir()
    endpoint = os.environ.get("VOXCPM2_ENDPOINT", "").strip()
    torch_ready = importlib.util.find_spec("torch") is not None
    soundfile_ready = importlib.util.find_spec("soundfile") is not None
    weights_cached = model_dir.is_dir() and any(model_dir.iterdir())
    return {
        "skill": "voxcpm2-voice",
        "auto_load_on_startup": False,
        "ready": bool(endpoint or (weights_cached and torch_ready)),
        "endpoint_configured": bool(endpoint),
        "weights_cached": weights_cached,
        "model_dir": str(model_dir),
        "python_deps": {"torch": torch_ready, "soundfile": soundfile_ready},
    }


def synthesize_via_endpoint(
    text: str,
    output_wav: Path,
    *,
    reference_wav: Optional[str] = None,
    sample_rate: int = 48000,
) -> Dict[str, object]:
    """Call configured VOXCPM2_ENDPOINT on-demand to render a 48kHz WAV stem."""
    endpoint = os.environ.get("VOXCPM2_ENDPOINT", "").strip()
    if not endpoint:
        return {
            "ok": False,
            "error": "VoxCPM2 weights/endpoint not loaded yet. Run scripts/optional_skill_bootstrap.py voxcpm2-voice --install --models or set VOXCPM2_ENDPOINT.",
            **inspect_status(),
        }
    payload = json.dumps(
        {
            "text": text,
            "sample_rate": sample_rate,
            "reference_audio": reference_wav,
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        f"{endpoint.rstrip('/')}/v1/tts",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        audio_bytes = resp.read()
    output_wav.parent.mkdir(parents=True, exist_ok=True)
    output_wav.write_bytes(audio_bytes)
    return {"ok": True, "output": str(output_wav), "bytes": len(audio_bytes)}


def main() -> int:
    parser = argparse.ArgumentParser(description="On-demand VoxCPM2 48kHz TTS helper.")
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_st = sub.add_parser("status", help="Inspect VoxCPM2 readiness.")
    p_st.add_argument("--json", action="store_true")
    p_syn = sub.add_parser("synthesize", help="Render WAV via VOXCPM2_ENDPOINT.")
    p_syn.add_argument("--text", required=True)
    p_syn.add_argument("--output", required=True)
    p_syn.add_argument("--ref", default="")

    args = parser.parse_args()
    if args.cmd == "status":
        print(json.dumps(inspect_status(), indent=2, ensure_ascii=False))
        return 0
    res = synthesize_via_endpoint(args.text, Path(args.output), reference_wav=args.ref or None)
    print(json.dumps(res, indent=2, ensure_ascii=False))
    return 0 if res.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
