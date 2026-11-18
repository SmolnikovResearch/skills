#!/usr/bin/env python3
"""Beat-grid synthesis, sub-120Hz kick-onset detector, and EBU R128 loudness normalization."""

from __future__ import annotations

import argparse
import json
import math
import re
import struct
import subprocess
import wave
from pathlib import Path
from typing import Dict, List


def synthesize_beat_track(
    bpm: float,
    duration_s: float,
    output_wav: Path,
    *,
    sample_rate: int = 48000,
) -> Dict[str, object]:
    """Synthesize a clean CapyAgent harmonic synth + sub-kick stem synced strictly to *bpm*."""
    output_wav = Path(output_wav)
    output_wav.parent.mkdir(parents=True, exist_ok=True)
    total_samples = int(round(duration_s * sample_rate))
    beat_period = 60.0 / bpm

    pcm = bytearray()
    chord_freqs = (196.0, 246.94, 293.66, 392.0)  # G3, B3, D4, G4 (warm teal editorial pad)
    for idx in range(total_samples):
        t = idx / sample_rate
        beat_pos = (t / beat_period)
        beat_index = int(beat_pos)
        local_t = (beat_pos - beat_index) * beat_period

        # Sub-kick punch under 120Hz on every beat (95Hz -> 44Hz rapid pitch drop)
        kick_env = math.exp(-local_t * 14.0) if local_t < 0.35 else 0.0
        kick_freq = 44.0 + 52.0 * math.exp(-local_t * 28.0)
        kick = 0.55 * kick_env * math.sin(2.0 * math.pi * kick_freq * local_t)

        # Crisp offbeat percussive tick on half-beats
        half_pos = (t / (beat_period / 2.0))
        half_local = (half_pos - int(half_pos)) * (beat_period / 2.0)
        tick_env = math.exp(-half_local * 55.0)
        tick = 0.14 * tick_env * math.sin(2.0 * math.pi * 1840.0 * half_local)

        # Subtle evolving warm pad switching harmony every 4 beats
        bar = (beat_index // 4) % 2
        root_mult = 1.0 if bar == 0 else 1.122462  # G major <-> A suspended lift
        pad = 0.0
        for h_idx, base_f in enumerate(chord_freqs):
            weight = 0.095 / (h_idx + 1)
            pad += weight * math.sin(2.0 * math.pi * (base_f * root_mult) * t)

        # Smooth fade-in (0.2s) and fade-out (0.4s)
        fade = 1.0
        if t < 0.2:
            fade = t / 0.2
        elif duration_s - t < 0.4:
            fade = max(0.0, (duration_s - t) / 0.4)

        sample = max(-0.92, min(0.92, (kick + tick + pad) * fade))
        pcm.extend(struct.pack("<h", int(sample * 32767)))

    with wave.open(str(output_wav), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(bytes(pcm))

    beat_times = [round(i * beat_period, 3) for i in range(int(duration_s / beat_period))]
    return {
        "wav": str(output_wav),
        "bpm": bpm,
        "duration_s": duration_s,
        "sample_rate": sample_rate,
        "beat_times_s": beat_times,
    }


def detect_subbass_beats(
    wav_path: Path,
    *,
    cutoff_hz: float = 120.0,
    min_spacing_s: float = 0.25,
) -> List[float]:
    """Detect kick/bass onset timestamps below *cutoff_hz* using a first-order low-pass energy envelope."""
    with wave.open(str(wav_path), "rb") as wf:
        sr = wf.getframerate()
        nch = wf.getnchannels()
        sw = wf.getsampwidth()
        raw = wf.readframes(wf.getnframes())

    if sw != 2:
        raise ValueError("detect_subbass_beats supports 16-bit PCM WAV files")

    samples_total = len(raw) // (2 * nch)
    dt = 1.0 / sr
    rc = 1.0 / (2.0 * math.pi * cutoff_hz)
    alpha = dt / (rc + dt)

    lp = 0.0
    win_size = max(1, int(0.02 * sr))  # 20ms hop
    energies: List[float] = []
    acc = 0.0
    count = 0

    for i in range(samples_total):
        offset = i * 2 * nch
        val = struct.unpack_from("<h", raw, offset)[0] / 32768.0
        lp = lp + alpha * (val - lp)
        acc += lp * lp
        count += 1
        if count >= win_size:
            energies.append(acc / count)
            acc = 0.0
            count = 0

    if not energies:
        return []

    peak_ref = max(energies) or 1.0
    threshold = peak_ref * 0.28
    onsets: List[float] = []
    last_t = -min_spacing_s
    for idx in range(1, len(energies) - 1):
        e = energies[idx]
        if e >= threshold and e >= energies[idx - 1] and e >= energies[idx + 1]:
            t = round(idx * (win_size / sr), 3)
            if t - last_t >= min_spacing_s:
                onsets.append(t)
                last_t = t
    return onsets


def measure_ebur128(audio_path: Path) -> Dict[str, float]:
    """Run ffmpeg ebur128 filter and parse integrated loudness (LUFS) + true peak (dBFS)."""
    proc = subprocess.run(
        [
            "ffmpeg",
            "-nostats",
            "-i",
            str(audio_path),
            "-af",
            "ebur128=peak=true",
            "-f",
            "null",
            "-",
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"ffmpeg ebur128 failed: {proc.stderr}")

    i_matches = re.findall(r"I:\s*(-?\d+(?:\.\d+)?)\s*LUFS", proc.stderr)
    tp_matches = re.findall(r"Peak:\s*(-?\d+(?:\.\d+)?)\s*dBFS", proc.stderr)
    return {
        "integrated_lufs": float(i_matches[-1]) if i_matches else -70.0,
        "true_peak_dbfs": float(tp_matches[-1]) if tp_matches else -70.0,
    }


def normalize_lufs(
    input_path: Path,
    output_path: Path,
    *,
    target_lufs: float = -16.0,
    true_peak_db: float = -4.0,
) -> Dict[str, object]:
    """Master audio to *target_lufs* with peak ceiling *true_peak_db* using ffmpeg loudnorm."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    limit_linear = 10 ** (true_peak_db / 20.0)
    af = f"loudnorm=I={target_lufs:.1f}:TP={true_peak_db:.1f}:LRA=11,alimiter=limit={limit_linear:.6f}:level=disabled"
    proc = subprocess.run(
        ["ffmpeg", "-y", "-i", str(input_path), "-af", af, str(output_path)],
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"ffmpeg normalize failed: {proc.stderr}")
    measured = measure_ebur128(output_path)
    return {"output": str(output_path), **measured}


def main() -> int:
    parser = argparse.ArgumentParser(description="Beat synthesis, onset detection, and -16 LUFS mastering.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_synth = sub.add_parser("synth", help="Generate beat-locked WAV track.")
    p_synth.add_argument("--bpm", type=float, default=120.0)
    p_synth.add_argument("--duration", type=float, default=15.0)
    p_synth.add_argument("--output", required=True)

    p_beats = sub.add_parser("beats", help="Detect sub-120Hz onset timestamps.")
    p_beats.add_argument("input")
    p_beats.add_argument("--json", action="store_true")

    p_master = sub.add_parser("master", help="Normalize audio to -16 LUFS / -4 dBFS TP.")
    p_master.add_argument("input")
    p_master.add_argument("output")
    p_master.add_argument("--json", action="store_true")

    args = parser.parse_args()
    if args.cmd == "synth":
        res = synthesize_beat_track(args.bpm, args.duration, Path(args.output))
        print(json.dumps(res, indent=2))
    elif args.cmd == "beats":
        onsets = detect_subbass_beats(Path(args.input))
        print(json.dumps({"onsets_s": onsets}, indent=2) if args.json else onsets)
    elif args.cmd == "master":
        res = normalize_lufs(Path(args.input), Path(args.output))
        print(json.dumps(res, indent=2) if args.json else res)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
