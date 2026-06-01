---
name: subtitle-to-script
description: Convert complete subtitle files or pasted subtitle text into a strict full short-drama/manhua-drama script. Use when the user provides SRT/VTT/TXT subtitles, episode subtitles, raw captions, timestamped dialogue, or asks to 根据字幕修改剧本、字幕推导完整剧本、从字幕还原剧本、把完整字幕改成完整短剧/漫剧/影视剧本、按剧本格式输出. Must preserve all subtitle content and output in professional script format, not a line-number transcript.
---

# Subtitle To Script

## Non-Negotiable Rule

Create a real industry-style short-drama script, not a subtitle cleanup, transcript, outline, summary, or line-number dump.

Every meaningful subtitle line must be represented in the final script as one of:

- Character dialogue.
- OS / inner monologue / narration.
- On-screen text / system prompt / phone message.
- Action, reaction, transition, or scene description.

Do not omit plot beats, jokes, prices, numbers, names, relationship clues, system prompts, sound reactions, or repeated catchphrases. The final script should normally be much longer than the subtitle source because it adds人物小传、故事梗概、scene headings, visual descriptions, actions, blocking, expressions, props, transitions, and episode hooks.

Do not use vague speaker labels such as `人物`, `某人`, or `未知人物` in the main script. If the exact speaker cannot be known from subtitles, assign a stable playable label based on context, such as `债主甲`, `债主乙`, `买家`, `村民甲`, `船员甲`, `游客甲`, `朋友甲`, `众人`, or `旁白`. The reader must always know who says the line well enough to shoot or draw the scene.

Every dialogue block should include playable expression/action guidance when useful, especially when the subtitle itself does not show emotion. Examples:

```markdown
**【债主甲】**
（拍门，语气逼迫）李绍安赶紧给老子开门。

**【李少安】**
（压住慌乱，迅速权衡）你们给我三个月时间。
```

Do not output a script that is “all dialogue with a simple scene header.” Every scene must be enriched with multiple visual action beats, like a production script:

- Opening visual setup: location, light, character position, clothes/props when inferable, emotional state.
- Action before key dialogue: who enters, sits, looks, hands over objects, opens phone, points at sea, pulls net, reacts.
- Action after key dialogue: silence, expression change, movement, cut, crowd reaction, object close-up.
- Transition language: `同场切`, `闪入`, `闪出`, `切至`, `字幕：`.
- Camera-drawable detail: avoid abstract comments like “很震惊”; write visible behavior like “手指攥紧欠条”“眼神一沉”“众人探头围上来”.

## Required Pre-Work

Before writing, calculate and report internally or in the final note:

- Original subtitle character count including whitespace.
- Original subtitle character count excluding whitespace.
- Number of non-empty subtitle lines.

If writing to a file, verify after generation:

- Output character count excluding whitespace is greater than the subtitle count unless the user explicitly requested compression.
- Every non-empty subtitle line is accounted for.
- Missing subtitle line count is `0`.

For long subtitles, write the full script to a `.md` file in the current workspace. Do not truncate chat output.

## Default Delivery To Feishu/Lark

After generating the final strict script file, import it into Feishu/Lark as an online document by default, unless the user explicitly says not to.

Use the Lark Drive workflow:

```bash
lark-cli drive +import --as user --file "<relative-path-to-final-md>" --type docx --name "<document-title>"
```

Rules:

- Use a relative file path from the current working directory; `lark-cli` may reject absolute paths.
- Import the final strict script version, not an audit file or line-number transcript.
- Return the Feishu/Lark document URL to the user.
- If import fails because authentication or permissions are missing, explain the exact blocker and keep the local `.md` file available.
- If `lark-cli` prints an update notice, mention it after completing the user task.

## Input Handling

Accept pasted subtitles or file paths. Support `.srt`, `.vtt`, `.txt`, and raw timestamped captions.

When a file path is provided, read the whole file. If encoding displays as mojibake in PowerShell, try UTF-8 explicitly before assuming the file is corrupt.

When multiple subtitle files are provided, sort by episode/part number and preserve order.

## Script Format Standard

Use the industry reference format in `references/script-output-template.md` unless the user gives another standard. The default must match the style of a professional竖屏短剧剧本, not Markdown notes.

Default professional short-drama format:

```markdown
竖屏男频短剧

《片名》剧本

一、人物小传
角色名
性别，年龄，身份。外貌气质、性格、背景、动机、人物弧光。写成完整段落，不要只写标签。

二、故事梗概
用 500-1000 字概括完整主线、核心爽点、人物关系、起承转合和结局方向。

三、剧本正文

第一集

1-1 李少安家 日 内
人物：李少安、债主甲、债主乙、债主若干

△破旧木门被砸得砰砰作响，门框上的灰尘震落。
△屋内，李少安猛地睁眼，额头沁出冷汗。
债主甲：李绍安，赶紧给老子开门！
△门外债主甲拍门，债主乙举着欠条，身后几个村民探头围观。
债主乙：把我们的血汗钱还回来！
李少安（OS）：前一秒还在谈几个亿的项目，一个哆嗦就重生到2009年。
```

Scene heading must use `集数-场次 地点 日/夜/晨/雨 内/外`. Every scene must include `人物：...`. Use `△` for visual action lines. Dialogue uses `角色：台词`, not bold Markdown blocks. Use `角色（OS）：` for inner monologue, `角色（画外音）：` for narration, and `△字幕：` for visible text/system prompts. Use `闪入/闪出` for flashbacks, `同场切` for same-location time/angle shifts.

## Conversion Workflow

1. Clean subtitle formatting only.
   Remove SRT/VTT sequence numbers, timestamps, tags, and platform watermarks. Preserve all meaningful text.

2. Rebuild speaker attribution.
   Infer speakers from names, vocatives, alternating turns, relationship cues, and scene logic. Use actual names once known. Before known, use stable labels such as `债主`, `李少安`, `宋天明`, `买家`, `村民`, `系统`, `众人`.

3. Merge broken subtitle fragments carefully.
   Combine obvious fragments into a single line only when it does not lose wording. If unsure, keep the wording intact in adjacent dialogue lines.

4. Split into episodes and scenes.
   Use setting changes, time jumps, new fishery intelligence, new business transaction, new conflict, or emotional turn as scene boundaries. For short-drama output, group scenes into episodes with hooks.

5. Add script-only material.
   Add enough visual descriptions, character movements, expressions, props, camera-visible actions, transitions, and episode hooks to match professional script density. Added material must be plausible and must not contradict the subtitles. A scene should not be only one `画面` line followed by dialogue; it should have repeated `△` action beats before and between key dialogue turns.

6. Preserve all source content.
   Every subtitle line must be mapped into script content. Avoid “剧情概括式” rewriting that drops dialogue.

7. Verify.
   Run a missing-line check when possible. If using a script or manual process, compare every non-empty subtitle line against the output or a coverage map.

## What Not To Output

Do not output:

- A “逐句行号稿” as the final script unless the user asks for audit mode.
- A plot summary that is shorter than the subtitles.
- A rough outline with only major scenes.
- Dialogue without scene headings.
- Scene headings without `人物：` and `日/夜` and `内/外`.
- Markdown-style dialogue blocks such as `**【角色】**` as the default deliverable.
- Sparse scenes where the only non-dialogue content is a single generic visual sentence.

If the user asks to audit coverage, you may create a separate line-number coverage file, but the main deliverable must remain a readable script.

## Quality Checklist

Before finishing, verify:

- Output follows strict script format: title, character list, episode title, scene heading, visual description, dialogue, OS/screen text where needed, episode hook.
- Output includes `一、人物小传`, `二、故事梗概`, and `三、剧本正文`.
- Scene headings match the industry pattern: `1-1 地点 日 内`, followed by `人物：...`.
- Visual action lines use `△` and appear throughout the scene, not only at the beginning.
- No subtitle line is omitted.
- Output word/character count is greater than the source unless compression was requested.
- Speaker names are consistent.
- No dialogue block uses vague labels such as `人物`; uncertain speakers use stable playable group labels.
- Important dialogue includes expression/action notes that actors, directors, or storyboard artists can execute.
- Scene order matches subtitle order.
- Added action does not contradict the source.
- The result reads like a producible short-drama/manhua-drama script, not a transcript.
