#!/usr/bin/env python3
"""Check whether video-lapai-notes can run Gemini and fallback analysis."""

from __future__ import annotations

import importlib.util
import json
import os
import shutil


def has_module(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def main() -> int:
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    packages = {
        "google_genai": has_module("google.genai"),
        "faster_whisper": has_module("faster_whisper"),
        "imageio_ffmpeg": has_module("imageio_ffmpeg"),
        "cv2": has_module("cv2"),
        "PIL": has_module("PIL"),
    }
    result = {
        "python_package": packages,
        "environment": {
            "GEMINI_API_KEY_or_GOOGLE_API_KEY": bool(api_key),
            "api_key_prefix": api_key[:4] if api_key else None,
        },
        "optional_tools": {
            "ffmpeg": shutil.which("ffmpeg") is not None,
            "ffprobe": shutil.which("ffprobe") is not None,
        },
        "ready": bool(api_key) and packages["google_genai"],
        "fallback_ready": (
            packages["faster_whisper"]
            and packages["imageio_ffmpeg"]
            and packages["cv2"]
            and packages["PIL"]
        ),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if (result["ready"] or result["fallback_ready"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
