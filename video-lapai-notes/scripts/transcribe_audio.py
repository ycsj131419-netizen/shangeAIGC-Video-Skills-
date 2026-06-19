#!/usr/bin/env python3
"""Extract audio from a video and transcribe it with faster-whisper."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def _ffmpeg_exe() -> str:
    try:
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return "ffmpeg"


def extract_audio(video: Path, wav: Path) -> None:
    wav.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        _ffmpeg_exe(),
        "-y",
        "-i",
        str(video),
        "-vn",
        "-ac",
        "1",
        "-ar",
        "16000",
        str(wav),
    ]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr[-2000:])


def transcribe(wav: Path, model_name: str, language: str) -> dict:
    try:
        from faster_whisper import WhisperModel
    except ImportError as exc:
        raise RuntimeError(
            "Missing dependency: install with `python -m pip install faster-whisper imageio-ffmpeg`."
        ) from exc

    model = WhisperModel(model_name, device="cpu", compute_type="int8")
    segments, info = model.transcribe(
        str(wav),
        language=language,
        vad_filter=False,
        beam_size=5,
    )
    items = [
        {"start": seg.start, "end": seg.end, "text": seg.text.strip()}
        for seg in segments
        if seg.text and seg.text.strip()
    ]
    return {
        "provider": "faster-whisper",
        "model": model_name,
        "language": info.language,
        "duration": info.duration,
        "segments": items,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Local video dialogue transcription fallback.")
    parser.add_argument("video", help="Local video file path.")
    parser.add_argument("-m", "--model", default="small", help="faster-whisper model, e.g. base/small/medium.")
    parser.add_argument("-l", "--language", default="zh", help="Speech language code.")
    parser.add_argument("-o", "--output", help="Write transcript JSON to this file.")
    parser.add_argument("--keep-wav", action="store_true", help="Keep extracted wav next to output.")
    args = parser.parse_args()

    try:
        video = Path(args.video).expanduser().resolve()
        if not video.is_file():
            raise FileNotFoundError(f"Source not found: {video}")
        out_path = Path(args.output).expanduser().resolve() if args.output else None
        workdir = out_path.parent if out_path else Path.cwd()
        wav = workdir / f"{video.stem}_audio.wav"
        extract_audio(video, wav)
        result = transcribe(wav, args.model, args.language)
        result["source"] = {"path": str(video), "audio": str(wav)}
        if out_path:
            out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        if not args.keep_wav:
            try:
                os.remove(wav)
            except OSError:
                pass
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
