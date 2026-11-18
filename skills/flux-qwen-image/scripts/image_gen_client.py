#!/usr/bin/env python3
"""On-demand image generation wrapper for FLUX Klein and Qwen-Image checkpoints/endpoints."""

from __future__ import annotations

import argparse
import base64
import importlib.util
import json
import os
import urllib.request
from pathlib import Path
from typing import Dict


def default_model_dir() -> Path:
    return Path(os.environ.get("CAPYAGENT_MODELS_DIR", Path.home() / ".capyagent" / "cache" / "models")) / "flux-qwen-image"


def inspect_status() -> Dict[str, object]:
    """Report model cache, python packages, and endpoint state without downloads."""
    model_dir = default_model_dir()
    endpoint = os.environ.get("IMAGE_GEN_ENDPOINT", "").strip()
    diffusers_ok = importlib.util.find_spec("diffusers") is not None
    weights_cached = model_dir.is_dir() and any(model_dir.iterdir())
    return {
        "skill": "flux-qwen-image",
        "auto_load_on_startup": False,
        "ready": bool(endpoint or (weights_cached and diffusers_ok)),
        "endpoint_configured": bool(endpoint),
        "weights_cached": weights_cached,
        "model_dir": str(model_dir),
        "python_deps": {"diffusers": diffusers_ok, "torch": importlib.util.find_spec("torch") is not None},
    }


def generate_image(prompt: str, output_png: Path, *, width: int = 1280, height: int = 720, model: str = "flux-klein") -> Dict[str, object]:
    """Send an on-demand image request to IMAGE_GEN_ENDPOINT."""
    endpoint = os.environ.get("IMAGE_GEN_ENDPOINT", "").strip()
    if not endpoint:
        return {
            "ok": False,
            "error": "Image generation backend not loaded yet. Run scripts/optional_skill_bootstrap.py flux-qwen-image --install --models or set IMAGE_GEN_ENDPOINT.",
            **inspect_status(),
        }
    req = urllib.request.Request(
        f"{endpoint.rstrip('/')}/v1/images/generations",
        data=json.dumps({"model": model, "prompt": prompt, "size": f"{width}x{height}", "response_format": "b64_json"}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    b64 = ((data.get("data") or [{}])[0]).get("b64_json", "")
    if not b64:
        return {"ok": False, "error": "Endpoint returned empty image payload."}
    output_png.parent.mkdir(parents=True, exist_ok=True)
    output_png.write_bytes(base64.b64decode(b64))
    return {"ok": True, "output": str(output_png), "model": model}


def main() -> int:
    parser = argparse.ArgumentParser(description="On-demand FLUX Klein / Qwen-Image client.")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status", help="Inspect model/endpoint readiness.").add_argument("--json", action="store_true")
    p_gen = sub.add_parser("generate", help="Generate PNG via IMAGE_GEN_ENDPOINT.")
    p_gen.add_argument("--prompt", required=True)
    p_gen.add_argument("--output", required=True)
    p_gen.add_argument("--model", default="flux-klein", choices=("flux-klein", "qwen-image-2.1"))
    args = parser.parse_args()
    if args.cmd == "status":
        print(json.dumps(inspect_status(), indent=2, ensure_ascii=False))
        return 0
    res = generate_image(args.prompt, Path(args.output), model=args.model)
    print(json.dumps(res, indent=2, ensure_ascii=False))
    return 0 if res.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
