# Marginalia · 阅读（Entrelinhas）

Entrelinhas 的「阅读」标签页读的就是这个文件夹。

- `YYYY-MM-DD.json`：一天的文章（德语、英语、葡语、法语），由每天的定时任务写入。
- `index.json`：所有日期和标题的目录，用 `python3 tools/mg_index.py` 重新生成。
- `config.json`：每种语言的难度（A1–C2）。改这里，第二天起生效。
- `weekly.json`：每周回顾（周日更新）。

文章都是原创写作，事实来自文末列出的来源；每个来源标了许可（CC BY、official 或 link only）。

## 选题与来源规则（定时任务写作时遵守）

每天每种语言最多两篇文章（推荐链接不算）：德语长文 + 短文（词语或冷知识），英语长文，葡语故事 + 对话，法语两篇。

- **English**（每天早上一篇 C2，按星期轮换）：周一移民、周二音乐、周三视觉文化（当代艺术/摄影/建筑与城市，按周轮换）、周四书与思想、周五社会与政治经济、周六人文·自然·科学、周日电影。来源偏左翼和自由派：Dissent、The Nation、n+1、Boston Review、Jacobin、The Baffler、Aeon、Noema、Public Books、Hyperallergic、Frieze、Aperture、Places Journal、Bandcamp Daily、The Quietus、Sight and Sound 等。The Guardian 在写作工具里无法访问，暂不使用。不用德国政府文件。
- **Deutsch**（每天早上一篇 C1 长文，轻松的文化与生活读物，不写政治新闻）：周一人物与移民故事、周二音乐、周三视觉文化（艺术/摄影/建筑与设计，按周轮换）、周四书与阅读、周五日常生活（饮食、语言、居住、习惯）、周六自然与知识、周日电影与剧集。来源：Deutschlandfunk Kultur/Nova、taz 与 Tagesspiegel 文化版、Freitag 文化版、Monopol、Perlentaucher、Börsenblatt、epd Film、Bauwelt、Photonews、Spektrum、Deutsch Perfekt 等。
- **Français**（给朋友用；每天傍晚两篇，一易一难，级别按星期轮换：一 A1+B2、二 A2+C1、三 B1+C1、四 A1+B2、五 A2+C1、六 B1+B2、日 A2+C1；不写推荐）：周一移民、周二音乐、周三视觉文化（当代艺术/摄影/建筑）、周四哲学与书、周五社会与世界（资本主义·不平等 / 地缘政治，隔周轮换）、周六茶文化 / 世界小知识 / 人文与自然（三周轮换）、周日电影。来源偏左翼和自由派：Le Monde diplomatique、Politis、L'Humanité、Alternatives Économiques、Le Vent Se Lève、Ballast、Regards、AOC、Libération 文化版、Les Inrockuptibles、Orient XXI、Afrique XXI、France Culture、France Musique、Philosophie Magazine、La Vie des idées、Cahiers du cinéma、L'Œil de la photographie、D'Architectures 等。
- **短篇（B2）**：周一、三、五、日「Alltagsdeutsch」——一段真实自然的日常对话（面包店、WG、同事闲聊、看医生、打电话、约朋友……），用地道的口语、语气词（doch, mal, halt, eben, ja）和常用习语，附说明；周二、四、六「Deutschland kurios」德国冷知识。不写汉诺威或其他本地新闻。
- 话题（广，偏自由派/绿党/左翼视角）：移民与融合、难民、女性与平权、气候与环境、社会正义与劳工、科技与 AI、教育、科学、语言学、社会学、经济学、国际关系。避免连续两天同一领域。本地新闻不限话题。不写 AfD。
- 写法：每篇以一篇当期报道为出发点，用自己的话重新写成适合学习者的原创文章，不复制、不摘录、不近似改写原文，不编造引语；文末列出原文链接（「原文」）和其他事实来源，标注许可（all rights reserved 的来源只放链接）。

## 每日推荐（kind: picks）

- 每天早上推送德语、英语各一份「推荐」，3–6 篇值得读完的原文链接，只给标题、作者、出处和一句中文介绍，读者自己去原网站读。
- 英语可包含 The Guardian、The Atlantic、The New Yorker 等：只有当链接出现在可访问的推荐来源（如 Longreads）里时才列入，介绍只依据推荐来源的摘要。否则每天在英语推荐末尾附上 Guardian「The Long Read」和 Atlantic「Ideas」两个栏目入口（genre 写 Browse），读者自己去挑。
- 推荐覆盖面要广：政治与国际关系、经济、气候与环境、科学、语言学、社会学、文化、科技；德语和英语各 4–6 篇，避免和前两天重复同一领域。
- 不编造链接；每个 URL 都必须来自实际打开过的页面。

## 辅助语言

- **词汇释义的主语言跟着文章语言走**：葡语、英语文章用英文解释；德语文章用德语解释（简单德语，像学习词典）；法语文章用法语解释。
- **读者自己的语言作为可选的第二语言**：App 里有一个按钮（简中用户是「中文」，德语用户是「Deutsch」……），打开后词汇、点词查询和逐段译文都会同时显示这种语言。
- 所以 `glossary` 每条写 `{"w","en","zh","de","pt"}`，法语文章再加 `"fr"`（法语解释）；德语文章的 `de`、葡语文章的 `pt` 写成简单的本语言解释。
- 语法说明：`grammar`（英文）、`grammar_zh`、`grammar_de`、`grammar_pt`，按读者的界面语言显示。
- 逐段译文：德语、葡语、法语文章附 `paragraphs_en`；所有文章都附 `paragraphs_zh`、`paragraphs_de`、`paragraphs_pt`（文章本身的语言除外），供读者打开自己语言的译文。
- 推荐阅读每条写 `en`、`zh`、`de`、`pt` 四句简介。
