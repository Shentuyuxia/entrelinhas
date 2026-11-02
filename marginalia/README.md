# Marginalia · 阅读（Entrelinhas）

Entrelinhas 的「阅读」标签页读的就是这个文件夹。

- `YYYY-MM-DD.json`：一天的文章（德语、英语、葡语、法语），由每天的定时任务写入。
- `index.json`：所有日期和标题的目录，用 `python3 tools/mg_index.py` 重新生成。
- `config.json`：每种语言的难度（A1–C2）。改这里，第二天起生效。
- `weekly.json`：每周回顾（周日更新）。

文章都是原创写作，事实来自文末列出的来源；每个来源标了许可（CC BY、official 或 link only）。

## 选题与来源规则（定时任务写作时遵守）

每天每种语言最多两篇文章（推荐链接不算）：德语长文 + 短文，英语长文 + 短文，葡语三篇 A1，西语两篇，法语一篇。

- **English**（每天早上一篇 C2，按星期轮换）：周一移民、周二音乐、周三视觉文化（当代艺术/摄影/建筑与城市，按周轮换）、周四书与思想、周五社会与政治经济、周六人文·自然·科学、周日电影。来源偏左翼和自由派：Dissent、The Nation、n+1、Boston Review、Jacobin、The Baffler、Aeon、Noema、Public Books、Hyperallergic、Frieze、Aperture、Places Journal、Bandcamp Daily、The Quietus、Sight and Sound 等。The Guardian 在写作工具里无法访问，暂不使用。不用德国政府文件。
- **Deutsch**（每天早上一篇 C1 长文，轻松的文化与生活读物，不写政治新闻）：周一人物与移民故事、周二音乐、周三视觉文化（艺术/摄影/建筑与设计，按周轮换）、周四书与阅读、周五日常生活（饮食、语言、居住、习惯）、周六自然与知识、周日电影与剧集。来源：Deutschlandfunk Kultur/Nova、taz 与 Tagesspiegel 文化版、Freitag 文化版、Monopol、Perlentaucher、Börsenblatt、epd Film、Bauwelt、Photonews、Spektrum、Deutsch Perfekt 等。
- **Français**（给朋友用；周一到周五每天傍晚一篇，级别按星期轮换：一 A1、二 A2、三 B1、四 B2、五 C1；不写推荐）：周一移民、周二音乐、周三视觉文化（当代艺术/摄影/建筑）、周四哲学与书、周五社会与世界（资本主义·不平等 / 地缘政治，隔周轮换）、周六茶文化 / 世界小知识 / 人文与自然（三周轮换）、周日电影。来源偏左翼和自由派：Le Monde diplomatique、Politis、L'Humanité、Alternatives Économiques、Le Vent Se Lève、Ballast、Regards、AOC、Libération 文化版、Les Inrockuptibles、Orient XXI、Afrique XXI、France Culture、France Musique、Philosophie Magazine、La Vie des idées、Cahiers du cinéma、L'Œil de la photographie、D'Architectures 等。
- **短篇（B2）**：周一、三、五、日「Alltagsdeutsch」——一段真实自然的日常对话（面包店、WG、同事闲聊、看医生、打电话、约朋友……），用地道的口语、语气词（doch, mal, halt, eben, ja）和常用习语，附说明；周二、四、六「Deutschland kurios」德国冷知识。不写汉诺威或其他本地新闻。
- 话题（广，偏自由派/绿党/左翼视角）：移民与融合、难民、女性与平权、气候与环境、社会正义与劳工、科技与 AI、教育、科学、语言学、社会学、经济学、国际关系。避免连续两天同一领域。本地新闻不限话题。不写 AfD。
- 写法：每篇以一篇当期报道为出发点，用自己的话重新写成适合学习者的原创文章，不复制、不摘录、不近似改写原文，不编造引语；文末列出原文链接（「原文」）和其他事实来源，标注许可（all rights reserved 的来源只放链接）。

## 每日推荐（kind: picks）

- 每天早上推送德语、英语各一份「推荐」，3–6 篇值得读完的原文链接，只给标题、作者、出处和一句中文介绍，读者自己去原网站读。
- 英语可包含 The Guardian、The Atlantic、The New Yorker 等：只有当链接出现在可访问的推荐来源（如 Longreads）里时才列入，介绍只依据推荐来源的摘要。否则每天在英语推荐末尾附上 Guardian「The Long Read」和 Atlantic「Ideas」两个栏目入口（genre 写 Browse），读者自己去挑。
- 推荐覆盖面要广：政治与国际关系、经济、气候与环境、科学、语言学、社会学、文化、科技；德语和英语各 4–6 篇，避免和前两天重复同一领域。
- 不编造链接；每个 URL 都必须来自实际打开过的页面。

## 辅助语言（2026 年 11 月起精简，省 token）

规则写在 `config.json` → `helper_languages`，定时任务照它写。字段少了没关系：App 会退回英文，再退回中文。

| 文章语言 | 逐段译文 | 词汇表 | 语法说明 |
|---|---|---|---|
| 英语 | 不写 | `w` + `en` + `zh` | `grammar`（英文）+ `grammar_zh` |
| 德语 | 不写 | `w` + `de`（简单德语，主解释）+ `zh` | `grammar` + `grammar_zh` |
| 葡语 | `paragraphs_en` + `paragraphs_zh` | `w` + `en` + `zh` | `grammar` + `grammar_zh` |
| 法语 | `paragraphs_en` + `paragraphs_de` | `w` + `fr`（简单法语，主解释）+ `de` | `grammar` + `grammar_de` |
| 西语 | `paragraphs_en` + `paragraphs_de` | `w` + `en` + `de` | `grammar` + `grammar_de` |

- 推荐阅读每条写 `en`、`zh`、`de`、`pt` 四句简介（不变）。
- 每篇新文章加 `tags`：2–4 个短词（国家/地区、话题或场景、语法点），供 `tools/mg_recent.py` 使用。

## 避免重复：先看摘要，不要打开旧文件

```sh
python3 tools/mg_recent.py es 30            # 西语最近 30 天，每篇一行（日期 · 级别 · 栏目 · 标题 · tags · 来源 · 语法点）
python3 tools/mg_recent.py de 14 --urls     # 加上所有来源和推荐链接
python3 tools/mg_recent.py pt --last Diário 2   # 连载最近两集的全文（保持人物和细节一致）
```
