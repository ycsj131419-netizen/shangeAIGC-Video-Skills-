#!/usr/bin/env python3
"""Analyze a local video or URL with Gemini full-video understanding."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path


DEFAULT_PROMPT = (
    "完整理解这个视频，不要只做抽帧描述。请按连续时间线分析：画面内容、镜头切换、"
    "人物或主体动作、表情和反应、台词或字幕、音效/BGM、画面节奏、关键信息、"
    "容易遗漏的细节。请输出带时间戳的分段拆解，并区分事实和推断。"
)


def _log(message: str, quiet: bool) -> None:
    if not quiet:
        print(f"[video-lapai-notes] {message}", file=sys.stderr)


def _read_text(response: object) -> str:
    text = getattr(response, "text", None)
    if text:
        return text
    candidates = getattr(response, "candidates", None) or []
    parts: list[str] = []
    for candidate in candidates:
        content = getattr(candidate, "content", None)
        for part in getattr(content, "parts", []) or []:
            value = getattr(part, "text", None)
            if value:
                parts.append(value)
    return "\n".join(parts)


def _wait_for_file(client: object, file_obj: object, quiet: bool) -> object:
    state = getattr(getattr(file_obj, "state", None), "name", None)
    while state == "PROCESSING":
        _log("Waiting for Gemini to process video...", quiet)
        time.sleep(2)
        file_obj = client.files.get(name=file_obj.name)
        state = getattr(getattr(file_obj, "state", None), "name", None)
    if state == "FAILED":
        raise RuntimeError("Gemini file processing failed.")
    return file_obj


def analyze(source: str, prompt: str, model: str, quiet: bool) -> dict:
    try:
        from google import genai
    except ImportError as exc:
        raise RuntimeError("Missing dependency: install with `python -m pip install google-genai`.") from exc

    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("Missing GEMINI_API_KEY or GOOGLE_API_KEY environment variable.")

    client = genai.Client(api_key=api_key)
    is_url = source.startswith(("http://", "https://"))

    _log(f"Using Gemini model: {model}", quiet)
    if is_url and ("youtube.com" in source or "youtu.be" in source):
        _log("Sending YouTube URL to Gemini.", quiet)
        response = client.models.generate_content(
            model=model,
            contents=[prompt, {"video_url": source}],
        )
    elif is_url:
        raise RuntimeError("Only local video files and YouTube URLs are supported by this script.")
    else:
        path = Path(source).expanduser().resolve()
        if not path.is_file():
            raise FileNotFoundError(f"Source not found: {path}")
        _log(f"Uploading local video: {path}", quiet)
        file_obj = client.files.upload(file=path)
        file_obj = _wait_for_file(client, file_obj, quiet)
        _log("Generating analysis...", quiet)
        response = client.models.generate_content(model=model, contents=[prompt, file_obj])

    return {
        "source": {"path": source, "type": "youtube" if is_url else "local"},
        "provider": "gemini",
        "model": model,
        "capability": "full_video",
        "response": _read_text(response),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Gemini full-video analysis for 拉片 notes.")
    parser.add_argument("source", help="Local video path or YouTube URL.")
    parser.add_argument("-p", "--prompt", default=DEFAULT_PROMPT, help="Analysis prompt.")
    parser.add_argument("-m", "--model", default="gemini-2.5-flash", help="Gemini model.")
    parser.add_argument("-o", "--output", help="Write JSON output to this file.")
    parser.add_argument("-q", "--quiet", action="store_true", help="Suppress progress logs.")
    args = parser.parse_args()

    try:
        result = analyze(args.source, args.prompt, args.model, args.quiet)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    output = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        _log(f"Output written to: {args.output}", args.quiet)
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
