#!/usr/bin/env python3
"""Check whether video-lapai-notes can run Gemini video analysis."""

from __future__ import annotations

import importlib.util
import json
import os
import shutil


def main() -> int:
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    result = {
        "python_package": {
            "google_genai": importlib.util.find_spec("google.genai") is not None,
        },
        "environment": {
            "GEMINI_API_KEY_or_GOOGLE_API_KEY": bool(api_key),
            "api_key_prefix": api_key[:4] if api_key else None,
        },
        "optional_tools": {
            "ffmpeg": shutil.which("ffmpeg") is not None,
            "ffprobe": shutil.which("ffprobe") is not None,
        },
        "ready": bool(api_key) and importlib.util.find_spec("google.genai") is not None,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
