#!/usr/bin/env python3
"""On-demand Qwen LiveTranslate speech/audio translation client and readiness probe."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import urllib.request
from pathlib import Path
from typing import Dict


def default_model_dir() -> Path:
    return Path(os.environ.get("CAPYAGENT_MODELS_DIR", Path.home() / ".capyagent" / "cache" / "models")) / "qwen-livetranslate"


def inspect_status() -> Dict[str, object]:
    """Inspect endpoint, cached checkpoint, and ffmpeg readiness without side effects."""
    model_dir = default_model_dir()
    endpoint = os.environ.get("QWEN_LIVETRANSLATE_ENDPOINT", "").strip()
    weights_cached = model_dir.is_dir() and any(model_dir.iterdir())
    return {
        "skill": "qwen-livetranslate",
        "auto_load_on_startup": False,
        "ready": bool(endpoint or weights_cached),
        "endpoint_configured": bool(endpoint),
        "weights_cached": weights_cached,
        "model_dir": str(model_dir),
        "ffmpeg_available": shutil.which("ffmpeg") is not None,
    }


def translate_audio(input_path: Path, *, source_lang: str = "auto", target_lang: str = "ru") -> Dict[str, object]:
    """Dispatch an on-demand audio translation request to QWEN_LIVETRANSLATE_ENDPOINT."""
    endpoint = os.environ.get("QWEN_LIVETRANSLATE_ENDPOINT", "").strip()
    if not endpoint:
        return {
            "ok": False,
            "error": "LiveTranslate backend not loaded. Run scripts/optional_skill_bootstrap.py qwen-livetranslate --install --models or set QWEN_LIVETRANSLATE_ENDPOINT.",
            **inspect_status(),
        }
    req = urllib.request.Request(
        f"{endpoint.rstrip('/')}/v1/audio/translations",
        data=json.dumps(
            {
                "input_path": str(Path(input_path).resolve()),
                "source_lang": source_lang,
                "target_lang": target_lang,
            }
        ).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="On-demand Qwen LiveTranslate helper.")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status", help="Inspect readiness.").add_argument("--json", action="store_true")
    p_tr = sub.add_parser("translate", help="Translate audio stream/file.")
    p_tr.add_argument("input")
    p_tr.add_argument("--source-lang", default="auto")
    p_tr.add_argument("--target-lang", default="ru")
    p_tr.add_argument("--json", action="store_true")

    args = parser.parse_args()
    if args.cmd == "status":
        print(json.dumps(inspect_status(), indent=2, ensure_ascii=False))
        return 0
    res = translate_audio(Path(args.input), source_lang=args.source_lang, target_lang=args.target_lang)
    print(json.dumps(res, indent=2, ensure_ascii=False))
    return 0 if res.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
