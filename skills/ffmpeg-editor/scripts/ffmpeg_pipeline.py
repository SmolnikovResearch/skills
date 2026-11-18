#!/usr/bin/env python3
"""Deterministic FFmpeg/FFprobe helpers for CapyAgent media workflows."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any, Dict, List


def run_cmd(cmd: List[str]) -> subprocess.CompletedProcess[str]:
    """Run an ffmpeg/ffprobe command and raise a readable error on failure."""
    proc = subprocess.run(cmd, text=True, capture_output=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(f"Command failed ({proc.returncode}): {' '.join(cmd)}\n{proc.stderr}")
    return proc


def probe_media(path: Path) -> Dict[str, Any]:
    """Inspect streams and format metadata using ffprobe."""
    proc = run_cmd(
        [
            "ffprobe",
            "-v",
            "quiet",
            "-print_format",
            "json",
            "-show_format",
            "-show_streams",
            str(path),
        ]
    )
    return json.loads(proc.stdout or "{}")


def extract_cover(video_path: Path, timestamp_s: float, output_png: Path) -> Path:
    """Extract a single lossless PNG poster frame from *video_path*."""
    output_png.parent.mkdir(parents=True, exist_ok=True)
    run_cmd(
        [
            "ffmpeg",
            "-y",
            "-ss",
            f"{max(0.0, timestamp_s):.3f}",
            "-i",
            str(video_path),
            "-frames:v",
            "1",
            "-update",
            "1",
            str(output_png),
        ]
    )
    return output_png


def mux_normalized_audio(
    video_path: Path,
    audio_path: Path,
    output_path: Path,
    *,
    target_lufs: float = -16.0,
    true_peak_db: float = -4.0,
    lra: float = 11.0,
) -> Path:
    """Mux *video_path* with loudness-normalized *audio_path* into H.264/AAC MP4."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    audio_filter = (
        f"loudnorm=I={target_lufs:.1f}:TP={true_peak_db:.1f}:LRA={lra:.1f},"
        f"alimiter=limit={10 ** (true_peak_db / 20):.6f}:level=disabled"
    )
    run_cmd(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(video_path),
            "-i",
            str(audio_path),
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-pix_fmt",
            "yuv420p",
            "-r",
            "30",
            "-af",
            audio_filter,
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-shortest",
            "-movflags",
            "+faststart",
            str(output_path),
        ]
    )
    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(description="FFmpeg/FFprobe media helpers.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_probe = sub.add_parser("probe", help="Inspect media streams.")
    p_probe.add_argument("input")
    p_probe.add_argument("--json", action="store_true")

    p_cover = sub.add_parser("cover", help="Extract cover PNG frame.")
    p_cover.add_argument("video")
    p_cover.add_argument("timestamp", type=float)
    p_cover.add_argument("output")

    p_mux = sub.add_parser("mux", help="Mux video + normalized audio into MP4.")
    p_mux.add_argument("video")
    p_mux.add_argument("audio")
    p_mux.add_argument("output")

    args = parser.parse_args()
    if args.cmd == "probe":
        info = probe_media(Path(args.input))
        print(json.dumps(info, indent=2, ensure_ascii=False))
    elif args.cmd == "cover":
        out = extract_cover(Path(args.video), args.timestamp, Path(args.output))
        print(f"Extracted cover frame: {out}")
    elif args.cmd == "mux":
        out = mux_normalized_audio(Path(args.video), Path(args.audio), Path(args.output))
        print(f"Muxed MP4: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
