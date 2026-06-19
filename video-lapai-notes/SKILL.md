---
name: video-lapai-notes
description: Use Gemini full-video understanding and local fallbacks to produce Chinese video 拉片 notes, timeline/shot breakdowns, dialogue/subtitle extraction, and copy-ready batch prompts for video recreation. Use when the user asks for 视频识别, 视频理解, 视频拉片, 拉片笔记, 镜头拆解, 时间线分析, 台词/字幕/音频分析, 视频反推提示词, 拉片提示词, 按批次输出提示词, or explicitly says not to rely only on frame sampling. Handles local video files, video URLs, YouTube URLs, screen recordings, and reference videos.
---

# Video 拉片笔记

## Goal

Produce a complete Chinese 拉片 result from a video:

1. Prefer Gemini full-video understanding for continuous visual/audio comprehension.
2. If Gemini is unavailable, blocked, rate-limited, or the user needs dialogue, use bundled local fallbacks for audio transcription and keyframe sampling.
3. When the user asks for 拉片提示词, 复刻提示词, or 按批次输出提示词, convert the analysis into copy-ready batch prompts using the fixed batch format in `references/prompt-batch-format.md`.

The goal is continuous video comprehension, not isolated screenshot description.

## Requirements

Required for Gemini mode:

- Python 3.10+.
- Python package: `google-genai`.
- User-provided Gemini API key in `GEMINI_API_KEY` or `GOOGLE_API_KEY`.

Optional but recommended fallbacks:

- `imageio-ffmpeg` for extracting audio without a system ffmpeg install.
- `faster-whisper` for local speech transcription.
- `opencv-python` and `Pillow` for keyframe/contact-sheet fallback analysis.

Never ask the user to paste API keys into chat. Tell the user to configure the key locally:

```powershell
python -m pip install -r requirements.txt
[Environment]::SetEnvironmentVariable("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY", "User")
$env:GEMINI_API_KEY=[Environment]::GetEnvironmentVariable("GEMINI_API_KEY","User")
```

If an API key appears in chat or a screenshot, tell the user to rotate it.

## Setup Check

Run before first analysis:

```powershell
python scripts/check_setup.py
```

Proceed with Gemini only when `ready` is `true`. If it is false, use local fallbacks when available and disclose the limitation.

## Core Workflow

1. Identify the requested output:
   - 拉片笔记: shot table plus summary.
   - 台词/字幕识别: prioritize dialogue extraction with timestamps.
   - 拉片提示词/复刻提示词/按批次输出提示词: produce generation-ready batch prompts, not just analysis.

2. Run Gemini full-video understanding first:

```powershell
python scripts/analyze_video.py "VIDEO_PATH_OR_URL" -m gemini-2.5-flash -o analysis.json
```

Use this prompt for general 拉片:

```text
完整理解这个视频，不要只做抽帧描述。请按连续时间线分析：画面内容、镜头切换、人物或主体动作、表情和反应、台词或字幕、音效/BGM、画面节奏、关键信息、容易遗漏的细节。请输出带时间戳的分段拆解，并区分事实和推断。
```

Use this prompt for dialogue:

```text
请完整读取这个视频，重点识别所有中文台词、字幕、拟人配音内容。不要只描述画面。请按时间线输出：时间戳、说话主体、准确台词、画面内容、镜头变化、音效/BGM。台词听不清时标注不确定，不要编造。
```

3. If Gemini fails with 403/429/503/model errors, retry useful models when appropriate (`gemini-3.5-flash`, `gemini-3-flash-preview`, `gemini-2.0-flash`). If the error is an API key restriction/enforcement problem, do not keep retrying blindly; disclose it and run fallbacks.

4. Local fallback for dialogue:

```powershell
python scripts/transcribe_audio.py "VIDEO_PATH" -o transcript.json
```

Use the transcript for exact dialogue when it is plausible. Mark uncertain lines as uncertain.

5. Local fallback for visual analysis:

```powershell
python scripts/sample_frames.py "VIDEO_PATH" -o frames
```

Open `frames/contact_sheet.jpg`, inspect keyframes, then reconstruct the timeline. Disclose that this is frame-based fallback if Gemini full-video understanding was unavailable.

6. If the video path contains Chinese characters or spaces and a script fails, copy the source to a short ASCII filename in a temporary working location and retry. Do not modify or delete the original video.

## Analysis Rules

- Treat the video as a continuous timeline. Describe how actions unfold, not only what appears in sampled frames.
- Pay attention to continuity, reaction beats, camera movement, composition changes, lighting, subtitles, BGM, sound effects, and pacing.
- Quote dialogue only when Gemini/local transcription is reliable. Do not invent original-video dialogue.
- Separate facts from inference.
- For AI-generated videos, mention visible AI traits only when observable: inconsistent anatomy, over-smooth motion, lip-sync issues, texture drift, physics issues, style instability.
- When the user supplies replacement roles/images, keep source-video dialogue and structure unless the user explicitly asks to rewrite the plot.

## Output Formats

For normal 拉片笔记, use `references/lapai-template.md`.

For 拉片提示词/复刻提示词/按批次输出提示词, read `references/prompt-batch-format.md` and follow it exactly. Each batch must be a complete copy-ready prompt with:

1. style/scene paragraph;
2. `主角：`;
3. `全局空间锚点：`;
4. `【分镜故事】`;
5. optional batch-specific negative prompt when useful.

Preserve source-video dialogue exactly for source beats. Only add dialogue in user-specified new scenes.

## Quality Checklist

- State whether Gemini full-video understanding was used or a fallback was used.
- Cover the whole video from start to end.
- Include dialogue/subtitles when available, not generic placeholders.
- Keep rows/beats about continuous action and causality, not static image descriptions.
- If producing prompts, make them generation-ready and concrete: scene, character refs, positions, action, expression, lens/movement, audio, timing, continuity.
- Do not output vague analysis when the user asked for prompts.
