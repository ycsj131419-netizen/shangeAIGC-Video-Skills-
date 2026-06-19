#!/usr/bin/env python3
"""Sample video frames and build a contact sheet for visual fallback analysis."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path


def sample(video: Path, outdir: Path, step: float, width: int) -> dict:
    try:
        import cv2
        from PIL import Image, ImageDraw
    except ImportError as exc:
        raise RuntimeError("Missing dependency: install with `python -m pip install opencv-python Pillow`.") from exc

    outdir.mkdir(parents=True, exist_ok=True)
    cap = cv2.VideoCapture(str(video))
    fps = cap.get(cv2.CAP_PROP_FPS) or 0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    duration = total_frames / fps if fps else 0
    src_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 0)
    src_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 0)
    if not fps or not total_frames:
        raise RuntimeError("Could not read video metadata.")

    times = [round(i * step, 2) for i in range(int(duration / step) + 1)]
    if times[-1] < duration - 0.1:
        times.append(round(max(0, duration - 0.05), 2))

    frame_paths: list[str] = []
    for t in times:
        cap.set(cv2.CAP_PROP_POS_MSEC, max(0, t * 1000))
        ok, frame = cap.read()
        if not ok:
            continue
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(rgb)
        w, h = im.size
        im = im.resize((width, int(h * width / w)))
        draw = ImageDraw.Draw(im)
        draw.rectangle((0, 0, 74, 24), fill=(0, 0, 0))
        draw.text((5, 5), f"{t:.1f}s", fill=(255, 255, 255))
        path = outdir / f"frame_{t:.1f}s.jpg"
        im.save(path, quality=90)
        frame_paths.append(str(path))
    cap.release()

    contact_sheet = None
    if frame_paths:
        thumbs = [Image.open(p).convert("RGB") for p in frame_paths]
        cols = 4
        tw, th = thumbs[0].size
        rows = math.ceil(len(thumbs) / cols)
        sheet = Image.new("RGB", (cols * tw, rows * th), (245, 245, 245))
        for i, im in enumerate(thumbs):
            sheet.paste(im, ((i % cols) * tw, (i // cols) * th))
        sheet_path = outdir / "contact_sheet.jpg"
        sheet.save(sheet_path, quality=92)
        contact_sheet = str(sheet_path)

    return {
        "source": str(video),
        "fps": fps,
        "frames": total_frames,
        "duration": duration,
        "width": src_w,
        "height": src_h,
        "frame_paths": frame_paths,
        "contact_sheet": contact_sheet,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Sample video frames for 拉片 fallback analysis.")
    parser.add_argument("video", help="Local video file path.")
    parser.add_argument("-o", "--outdir", default="sampled_frames", help="Output directory.")
    parser.add_argument("-s", "--step", type=float, default=0.5, help="Seconds between frames.")
    parser.add_argument("-w", "--width", type=int, default=240, help="Thumbnail width.")
    args = parser.parse_args()

    try:
        video = Path(args.video).expanduser().resolve()
        if not video.is_file():
            raise FileNotFoundError(f"Source not found: {video}")
        result = sample(video, Path(args.outdir).expanduser().resolve(), args.step, args.width)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
