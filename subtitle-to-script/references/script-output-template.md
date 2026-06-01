# Industry Short-Drama Script Output Template

Use this format for subtitle-to-script conversion unless the user specifies another professional standard. This is the default target style for竖屏短剧/漫剧剧本交付.

```markdown
竖屏男频短剧

《片名或暂定名》剧本

一、人物小传

李少安
男，年龄，身份。外貌气质、性格、背景经历、核心动机、人物弧光。写成完整段落，信息密度要高。

宋天明
男，年龄，身份。与主角关系、性格功能、喜剧功能、成长变化。

二、故事梗概

用 500-1000 字概括完整故事：开局困境、主角能力、主要爽点、关键人脉、感情线、事业线、反派冲突、结局方向。

三、剧本正文

第一集

1-1 李少安家 日 内
人物：李少安、债主甲、债主乙、债主若干

△破旧木门被砸得砰砰作响，门框上的灰尘震落。
△屋内，李少安猛地睁眼，额头沁出冷汗，耳边还残留着前世商务谈判的回音。
债主甲：李绍安，赶紧给老子开门！
△债主甲一掌拍在门板上，债主乙攥着欠条，身后几个债主围住院门。
债主乙：把我们的血汗钱还回来！
李少安（OS）：前一秒还在谈几个亿的项目，一个哆嗦就重生到2009年。
△李少安低头看见自己身上的旧衬衫，又看向桌上散乱的欠条，眼神一沉。

1-2 李少安家 日 内
人物：李少安

△债主散去，屋里只剩一桌欠条。
△李少安坐在木椅上，指尖敲着桌面，强迫自己冷静。
△字幕：今日10点到12点，白沙村东边红树林，有大量青蟹出没。
李少安：鱼获情报系统？这是金手指吗？
△李少安抬头看向墙上的旧钟，上午九点。

第二集

2-1 白沙村路口 日 外
人物：李少安、宋天明

△宋天明穿着夸张外套，甩着头发走来。
宋天明：天明你怎么来了？
△李少安看见宋天明，眼神一亮，像是终于抓到帮手。
```

Rules:

- Must include `一、人物小传`, `二、故事梗概`, `三、剧本正文`.
- Scene heading format: `1-1 地点 日/夜/晨/雨 内/外`.
- Immediately after each scene heading, write `人物：角色A、角色B、群演若干`.
- Visual/action lines begin with `△`.
- Dialogue format is `角色：台词`; do not use bold Markdown dialogue blocks by default.
- Inner monologue: `角色（OS）：内容`.
- Voice-over narration: `角色（画外音）：内容`.
- Visible text/system message: `△字幕：内容`.
- Flashback: write `闪入`, then a sub-scene such as `5-1-1 树林 日 外`, then `闪出`.
- Same-location cut/time shift: use `同场切`.
- Do not include original subtitle line numbers in the main script unless the user asks for audit mode.
- Keep all source dialogue and information; the script should be significantly richer and longer than the subtitle file.
- Avoid sparse scenes. Add visual action beats before, between, and after important dialogue.
