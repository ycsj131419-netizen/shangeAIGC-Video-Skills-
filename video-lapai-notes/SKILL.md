---
name: video-lapai-notes
description: Use Gemini full-video understanding plus a Chinese 拉片 workflow to deeply analyze videos. Use when the user asks for 视频识别, 视频理解, 视频拉片, 拉片笔记, 视频拆解, 镜头拆解, 时间线分析, 节奏分析, 台词/字幕/音频分析, 视频内容总结, 像 Gemini 一样读取视频, or explicitly says not to rely on frame-only sampling. Handles local video files, video URLs, YouTube URLs, screen recordings, and reference videos.
---

# Video 拉片笔记

## Goal

Produce a complete Chinese 拉片笔记 from a video by using Gemini full-video understanding, then converting the result into a shot/beat-level analysis. The goal is continuous video comprehension, not isolated screenshot description.

## Requirements

Required:

- No Codex plugin is required.
- Python 3.10+.
- Python package: `google-genai`.
- User-provided Gemini API key in `GEMINI_API_KEY` or `GOOGLE_API_KEY`.

Optional:

- `ffmpeg` and `ffprobe` for local metadata, frame inspection, or fallback analysis. Gemini full-video analysis works without them.

Never ask the user to paste API keys into chat. Tell the user to configure the key locally:

```powershell
python -m pip install google-genai
[Environment]::SetEnvironmentVariable("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY", "User")
$env:GEMINI_API_KEY=[Environment]::GetEnvironmentVariable("GEMINI_API_KEY","User")
```

On macOS/Linux:

```bash
python -m pip install google-genai
export GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
```

If an API key appears in chat or a screenshot, tell the user to rotate it.

## Setup Check

Run the bundled setup check before the first analysis:

```powershell
python scripts/check_setup.py
```

Proceed only when `ready` is `true`. If it is false, install `google-genai` or ask the user to configure `GEMINI_API_KEY`.

## Core Workflow

1. Read the user's request and identify the output target:
   - 拉片笔记: detailed table plus summary.
   - 时间线拆解: emphasize continuous actions, visual changes, camera movement, sound, and subtitles.
   - 问答/识别: answer the user's specific questions with timestamps when possible.

2. Run Gemini full-video understanding with the bundled script. Prefer `gemini-2.5-flash` for speed and reliability. Use another Gemini model only if the user requests it or the local account supports it:

```powershell
python scripts/analyze_video.py "VIDEO_PATH_OR_URL" -m gemini-2.5-flash -p "完整理解这个视频，不要只做抽帧描述。请按连续时间线分析：画面内容、镜头切换、人物或主体动作、表情和反应、台词或字幕、音效/BGM、画面节奏、关键信息、容易遗漏的细节。请输出带时间戳的分段拆解，并区分事实和推断。"
```

To preserve the raw Gemini result for later formatting:

```powershell
python scripts/analyze_video.py "VIDEO_PATH_OR_URL" -o analysis.json
```

3. If the video path contains Chinese characters or spaces and the script fails, copy the source to a short ASCII filename in a temporary working location and retry. Do not modify or delete the original video.

4. Convert the JSON `response` into a clean Chinese 拉片 note. Use the standard template in `references/lapai-template.md` unless the user provides a stricter format.

## Analysis Rules

- Treat the video as a continuous timeline. Describe how actions unfold, not only what appears in sampled frames.
- Pay attention to action continuity, reaction beats, camera movement, composition changes, lighting changes, subtitles, BGM, sound effects, and pacing.
- Merge tiny cuts when they belong to one continuous action. Split longer scenes when the subject, action purpose, speaker, audio, or visual focus changes.
- Quote visible subtitles or reliable transcription only when clear. Mark uncertain speech as approximate.
- Separate facts from inference. Do not invent unseen dialogue, identities, causes, brands, places, or plot motivations.
- For AI-generated videos, mention visible AI traits only when observable: inconsistent anatomy, over-smooth motion, lip-sync issues, texture drift, physics issues, or style instability.

## Output Format

Default to Chinese. For 拉片笔记, include:

```markdown
## 视频拉片笔记

| 镜号 | 景别/角度 | 运动 | 画面内容 | 音频 | 时长(秒) |
|------|-----------|------|----------|------|----------|
| 1 | ... | ... | ... | **BGM**: ...<br>**音效**: ...<br>**配音/字幕**: ... | ... |

## 总结描述

### 画面风格
### 内容结构
### 镜头语言
### 音频风格
### 关键细节
```

## Quality Checklist

Before answering, verify:

- Gemini full-video provider was available, or any fallback limitation is disclosed.
- Timestamps cover the full video roughly from start to end.
- Table rows describe motion and causality, not static images.
- Audio/subtitles are not left generic when they matter.
- Summary explains visible form, content organization, camera language, and audio.
- Uncertain details are labeled rather than invented.
