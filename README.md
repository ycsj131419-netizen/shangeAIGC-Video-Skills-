# shangeAIGC Video Skills

个人 AIGC 视频、短剧、漫剧工作流 Codex Skills 集合。

## Skills

### `video-lapai-notes`

**用途：用 Gemini full-video 理解视频，并输出结构化中文拉片笔记。**

当你提供本地视频、YouTube URL、录屏或参考视频，或提出“视频识别”“视频理解”“视频拉片”“镜头拆解”“时间线分析”“不要只抽帧”等需求时使用。

适合处理：

- 连续时间线视频理解。
- 镜头、动作、字幕/台词、音效/BGM、画面节奏拆解。
- 输出标准中文拉片表格。
- 发现仅靠截帧容易遗漏的动作、表情、转场和音频细节。

安装依赖：

```bash
python -m pip install -r video-lapai-notes/requirements.txt
```

配置 API：

```bash
# macOS / Linux
export GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
```

```powershell
# Windows PowerShell
[Environment]::SetEnvironmentVariable("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY", "User")
$env:GEMINI_API_KEY=[Environment]::GetEnvironmentVariable("GEMINI_API_KEY","User")
```

检查环境：

```bash
python video-lapai-notes/scripts/check_setup.py
```

命令行测试：

```bash
python video-lapai-notes/scripts/analyze_video.py "path/to/video.mp4" -o analysis.json
```

说明：

- 不需要额外 Codex 插件。
- API Key 需要用户自己配置，不应写入仓库或聊天记录。
- `ffmpeg` / `ffprobe` 是可选依赖，用于本地媒体辅助处理；Gemini full-video 分析本身不强制依赖它们。

### `video-reverse-prompts`

**用途：视频复刻 / 拉片分析 / 镜头反推提示词。**

当你提供参考视频、录屏、关键帧、视频描述，或提出“视频复刻”“拉片”“镜头拆解”“像 Gemini 一样读视频”“根据视频写生成提示词”等需求时使用。

适合处理：

- 参考视频逐镜头分析。
- 画面内容、景别、角度、运镜、节奏、字幕、音频拆解。
- 为即梦、可灵、Runway、Pika、Seedance 等视频模型准备复刻提示词。
- 输出镜号表、风格总结、镜头语言分析、分镜级提示词。

默认输出：

- 拉片笔记。
- 镜头表。
- 画面/音频/字幕/节奏分析。
- 视频生成提示词或复刻提示词。

### `subtitle-to-script`

**用途：根据完整台词 / 字幕文件反推并完善成专业短剧剧本。**

当你提供完整字幕、SRT/VTT/TXT、逐行台词、 raw captions，或提出“根据字幕改剧本”“从台词反推剧本”“字幕推导完整剧本”“把字幕整理成短剧/漫剧剧本”等需求时使用。

这个 Skill 的重点不是简单整理字幕，而是把台词反推成可拍摄、可分镜、可交付的工业剧本。

适合处理：

- 只有字幕，没有剧本的短剧/漫剧素材。
- 根据台词还原人物、场次、动作、表情、道具、转场。
- 将零散字幕补全为完整短剧剧本。
- 对标竖屏短剧剧本格式输出。

默认输出格式：

- `一、人物小传`
- `二、故事梗概`
- `三、剧本正文`
- 场次格式：`1-1 地点 日/夜 内/外`
- 每场写：`人物：角色A、角色B`
- 动作行用：`△动作描写`
- 台词用：`角色：台词`
- 内心独白用：`角色（OS）：内容`
- 画外音用：`角色（画外音）：内容`
- 屏幕/系统文字用：`△字幕：内容`
- 回忆用：`闪入 / 闪出`
- 同场转切用：`同场切`

质量要求：

- 保留所有有效字幕和台词信息，不遗漏。
- 不使用 `人物`、`某人`、`未知人物` 这类模糊说话人。
- 不输出“只有台词”的稿子，必须补充场景、动作、表情、道具、人物反应、转场和画面调度。
- 剧本字数通常应明显多于原字幕字数。
- 生成最终稿后，默认导入飞书文档并返回链接。

## Repository Rules

- 每个 Skill 使用一个顶层文件夹。
- Skill 文件夹必须包含 `SKILL.md`。
- 如需模板或规范，放入该 Skill 的 `references/`。
- 提交前运行 Skill 校验。
- 不要提交用户原始素材、生成剧本、视频、PDF、截图等私有工作文件。
