---
name: subtitle-remix-pipeline
description: Complete end-to-end workflow for turning subtitle files into a calibrated source script and then into a substantially original adapted short-drama/manhua-drama script. Use when the user provides SRT/VTT/TXT subtitles and asks for 根据字幕改编, 字幕转剧本再改编, 爆款改编, 红果漫剧改编, 避免侵权, 完整剧本, or wants the whole process from subtitle calibration to final adapted script with self-scoring and Feishu delivery.
---

# Subtitle Remix Pipeline

## Purpose

Convert subtitle material into a complete, original, market-fit adapted script without losing source information or copying protected expression.

This skill combines two stages:

1. Subtitle calibration: preserve and correctly attribute the source.
2. Original adaptation: extract the hook, rebuild the story, and deliver a new complete script.

Do not skip either stage unless the user explicitly says the calibrated script already exists and is reliable.

## Hard Gates

Do not deliver the final adapted script until all gates pass:

- Source file inventory is recorded.
- Clean subtitle source is selected as authority when multiple files exist.
- Original episode count is verified or reasonably inferred.
- Missing subtitle line count is `0` for the calibration stage.
- Speaker attribution audit passes.
- Cross-story/trailer residue is excluded or clearly marked.
- Adapted work is substantially original, not a renamed or lightly rewritten copy.
- Full adaptation means full episode count unless the user explicitly asks for a sample or compression.
- Final self-score is at least `90/100`.
- Long final output is written to a local `.md` file and imported to Feishu/Lark by default.

Automatic fail:

- Outputting only 3-5 sample episodes when the user asked for the full adaptation.
- Arbitrarily reducing a 70+ episode source to a small number of episodes.
- Speaker labels are visibly wrong, including self-address errors.
- A character or name appears that was not in the source or the new adaptation plan.
- The protagonist's money-making path does not match the chosen era/industry.
- A requested system/golden-finger appears at the wrong trigger point or replaces protagonist skill.
- The score is written as a decoration but low-scoring problems are not fixed.

## Workflow

### 1. Source Inventory

For every source file, record:

- Absolute path.
- File type and encoding.
- Rough/clean status.
- Character count with whitespace.
- Character count without whitespace.
- Non-empty line count.
- Inferred episode count.
- First and last meaningful line.
- Suspected contamination, trailer residue, or unrelated character names.

If the user provides both a rough file and a clean file, use the clean file as the authority, but remember what was wrong in the rough file.

Never silently merge unrelated tail content into the main story.

### 2. Subtitle Calibration

Create a strict source script before original adaptation.

Requirements:

- Preserve every meaningful subtitle line.
- Convert each line into dialogue, OS, narration, screen text, action, reaction, or transition.
- Add playable scene description and action beats; do not output a bare transcript.
- Match the source episode count unless the user asks otherwise.
- Keep scene order aligned with the source.
- Use stable playable labels for unknown speakers.

Speaker audit rules:

- A name inside a line is often the addressee, not the speaker.
- Prevent self-address errors such as a character saying their own name without context.
- Restrict each scene to characters who are actually present.
- If the line says “爸爸/爷爷/卫东/小柔/圆圆” etc., infer who is being addressed before assigning speaker.
- If uncertain, use a stable group label and note the uncertainty instead of inventing a named character.

Coverage audit:

- Count all non-empty source lines.
- Confirm every line is represented.
- Missing line count must be `0`.
- If a line is merged, it must still be traceable.

### 3. Hook And Risk Diagnosis

From the calibrated script, extract only abstract mechanisms:

- Audience hook.
- Emotional engine.
- Structural engine.
- Protagonist pressure.
- Antagonist pressure.
- Escalation rhythm.
- Payoff type.

Create a must-not-copy list:

- Original names.
- Exact relationship setup.
- Scene order.
- Signature set pieces.
- Unique props/rules.
- Distinctive dialogue.
- Iconic visuals.
- Ending mechanism.

Use copyright-safe abstraction. Do not preserve exact expression.

### 4. Market And User Constraint Calibration

Respect the user's latest direction over earlier drafts.

If the user asks for current platform fit, verify current platform/genre tendencies before selecting the adaptation direction. For Red Fruit/Hongguo-style manhua drama, identify a practical genre match instead of forcing a random trend.

For period-realism adaptations:

- Keep the chosen era's economy, transport, documents, food, business, and social relations plausible.
- Profit must come from a believable chain: skill, legal permission, processing, transport, buyer, contract/order, pricing pressure, risk.
- The male lead's distinctive skill must be visible in repeated actions.
- Generic scavenging or simple collecting cannot justify large dividends unless the business logic is rebuilt.

For system/golden-finger adaptations:

- Define when the system first appears.
- Define who can see it.
- Define what it reports.
- Define what it cannot solve.
- Keep protagonist skill necessary.
- If the user says the system appears only after a specific event, that trigger point is mandatory.

### 5. Original Rebuild

Rebuild at least these elements:

- Era/social environment.
- Industry/business domain.
- Core resource.
- Protagonist identity, wound, goal, and active skill.
- Antagonist power base.
- Character relationship web.
- System/rule/business mechanism.
- Main locations and visual symbols.
- Climax and public reckoning arena.

Changing names is not enough. The new world must create different choices, conflicts, scenes, and payoffs.

### 6. Full Script Draft

For a full adapted script, include:

1. 改编策略说明
2. 原作吸引力机制
3. 避险替换表
4. 原创世界观与人物小传
5. 原创故事梗概
6. 分集大纲
7. 剧本正文
8. 自查自纠报告与评分

For long sources, write the full deliverable to a `.md` file. Do not rely on chat-only output.

If the source has a known episode count, output the same adapted episode count unless the user explicitly requests compression or expansion.

### 7. Self-Review And Revision

Score using this 100-point gate:

- Source coverage and episode integrity: 15
- Speaker attribution and source integrity: 15
- Hook extraction and audience value: 10
- Original worldview and causality: 15
- Character goal, skill, and active choices: 15
- Conflict escalation and payoff: 10
- Setup/rule consistency: 10
- Copyright-risk distance: 10

If any hard gate fails, the score must be below 90. Revise before delivery.

Do not present a below-90 draft as final.

### 8. Feishu/Lark Delivery

After generating a long final script file, import it into Feishu/Lark as a docx unless the user explicitly says not to.

Use a relative file path from the file's directory:

```bash
lark-cli drive +import --as user --file ".\\final-script.md" --type docx --name "document-title"
```

Return:

- Local file path.
- Feishu/Lark URL.
- Final score.
- Key self-check results.

If import fails, explain the exact blocker and keep the local file available.

## Final Response Checklist

Include:

- Authoritative source file used.
- Episode count.
- Subtitle coverage result.
- Speaker audit result.
- What hook was extracted.
- What was rebuilt.
- Why it is not merely a renamed copy.
- Final score.
- Feishu/Lark document URL for long deliverables.

