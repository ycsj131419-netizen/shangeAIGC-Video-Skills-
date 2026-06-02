---
name: video-reverse-prompts
description: Create detailed Chinese video reverse-engineering notes and prompt-prep analysis from a user-provided reference video, screen recording, keyframes, or visual/audio description. Use when the user asks for 视频反推提示词, 视频反推, 视频复刻, 视频拉片, 拉片笔记, 镜头拆解, 完整读懂视频, 像 Gemini 一样读取视频, not merely frame sampling, or wants a shot-by-shot table with 景别/角度, 运动, 画面内容, 音频, and 时长 before writing generation prompts.
---

# 视频反推提示词 Skill

## Goal

Produce a structured Chinese analysis that fully understands a reference video over time before writing or preparing video-generation prompts. The first deliverable is usually a 拉片笔记: story beats, shots, camera language, motion, visible content, subtitles/dialogue/audio, style, and pacing. Treat frame sheets as navigation aids only; do not reduce the analysis to isolated screenshots.

## Core Workflow

1. Inspect the source video directly when available.
   - Read metadata first: duration, resolution, frame rate, streams, orientation, and audio presence.
   - If direct tools fail on a path, copy to a safe ASCII filename in the working directory and retry.
   - Use `ffmpeg`/`ffprobe` when available. If not available, install or use `imageio-ffmpeg` as a local fallback.

2. Understand the video as a continuous time sequence.
   - Detect scene changes or shot boundaries.
   - Review low-frequency timeline previews only as navigation aids.
   - Pay attention to action continuity, reaction beats, camera motion, composition changes, emotional pacing, and sound/subtitle timing.
   - Use subtitles, visible mouth movement, and extracted audio together. If speech transcription is uncertain, mark the line as approximate instead of inventing precision.

3. Segment the video into shots or meaningful beats.
   - Use exact or approximate time ranges.
   - Merge tiny cuts when they are part of the same dramatic beat.
   - Split longer scenes when the visual subject, action purpose, emotional beat, or audio speaker changes.

4. Write the user's requested output.
   - Default to Chinese.
   - If the user asks for 拉片笔记, 视频反推, 视频复刻, or 反推提示词, the 拉片笔记 section MUST use the strict standard template below before writing prompts.
   - The standard 拉片笔记 MUST include the exact Markdown table columns: 镜号, 景别/角度, 运动, 画面内容, 音频, 时长(秒).
   - The 音频 cell MUST be split into labeled lines whenever possible: **BGM**, **音效**, **配音/字幕**. If one item is absent, state it briefly (e.g. 无明显音效). Do not leave audio generic.
   - After the table, MUST add `## 总结描述` with these exact subsections: `### 画面风格`, `### 纹理与材质`, `### 光影与环境`, `### 动作逻辑`, `### 音频风格`.
   - Do not replace these required summary subsections with 叙事结构, 镜头语言, or 复刻要点. Those may be added only as extra subsections after the required five.
   - Read `references/lapai-template.md` when the user asks for the standard table format or when no custom template is provided.
   - If the user asks for actual video-generation prompts, use the analysis to write master prompts, shot-by-shot prompts, negative prompts, and platform notes.

## Analysis Rules

- Prefer video-understanding language over screenshot description. Describe how events unfold, not only what appears in a representative frame.
- Separate facts from inference. If a subtitle is readable, quote it. If audio cannot be transcribed reliably, say "字幕可读为..." or "听感近似..." as appropriate.
- Do not invent unseen dialogue, character identity, brand names, locations, or causes. Infer only from visible content, subtitles, audio, and narrative context.
- For AI-generated videos, explicitly note visible AI traits: inconsistent anatomy, stylized realism, waxy skin, over-smooth motion, lip-sync quality, texture consistency, or physics issues.
- For drama, ad, or short-video references, capture the emotional function of each shot: setup, conflict, contrast, reversal, escalation, release, or theme statement.
- When the video includes text cards, transcribe the text and include them as shots if they carry narrative meaning.

## Tooling Notes

- Useful commands:
  - Metadata: `ffprobe -v error -show_format -show_streams -of json <video>`
  - Fallback ffmpeg path: `python -c "import imageio_ffmpeg as ff; print(ff.get_ffmpeg_exe())"`
  - Audio extraction: `ffmpeg -i <video> -vn -ac 1 -ar 16000 audio.wav`
  - Scene changes: `ffmpeg -i <video> -vf "select='gt(scene,0.25)',showinfo" -an -f null -`
  - Timeline preview: sample at 1 fps into a contact sheet for navigation, then return to the video timeline for interpretation.
- If transcription models are unavailable, rely on visible subtitles and state that limitation.
- If the user explicitly rejects frame-only analysis, reassure through method: continuous timeline, shot boundaries, audio/subtitle reading, and action continuity.

## Output Discipline

- Preserve the user's requested format exactly when they provide one.
- When the user asks for 拉片笔记 or when this skill prepares prompt reverse-engineering, strictly preserve the standard 拉片笔记 format from `references/lapai-template.md`: six-column table first, then the five required summary subsections.
- Keep each table row concrete and production-useful: subject, action, setting, composition, motion, audio, and duration.
- Avoid overly generic adjectives. Replace "高级感" with observable traits such as "冷色办公室灯光, 浅景深, 玻璃反光, 高对比夜景".
- Include limitations only when they materially affect accuracy, such as missing audio transcription or unreadable subtitles.
