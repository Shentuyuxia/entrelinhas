# Marginalia · 阅读（Entrelinhas）

Entrelinhas 的「阅读」标签页读的就是这个文件夹。

- `YYYY-MM-DD.json`：一天的文章（德语、英语、葡语、法语），由每天的定时任务写入。
- `index.json`：所有日期和标题的目录，用 `python3 tools/mg_index.py` 重新生成。
- `config.json`：每种语言的难度（A1–C2）。改这里，第二天起生效。
- `weekly.json`：每周回顾（周日更新）。

文章都是原创写作，事实来自文末列出的来源；每个来源标了许可（CC BY、official 或 link only）。

## 选题与来源规则（定时任务写作时遵守）

- **English**（轮换）：Jacobin、The Intercept、Mother Jones、Dissent、New Internationalist；补充：ProPublica、The Marshall Project（移民）、Rest of World（科技）、The 19th（性别平等）。The Guardian 在写作工具里无法访问，暂不使用。不用德国政府文件。
- **Deutsch**（轮换）：Tagesspiegel（时事优先）、taz、Mediendienst Integration、Missy Magazine、Deutsch Perfekt。Tagesschau 在写作工具里无法访问，暂不使用。
- **Français**（每天傍晚，A1、A2、B1、B2、C1 各一篇，读者在 App 里选级别；周二、周日偏音乐，周四偏哲学，推荐里每天至少一篇音乐、一篇哲学）：话题是国际政治与地缘政治、资本主义与政治经济、移民、社会不平等、音乐、哲学、茶文化，以及世界小知识——尤其是东亚、南亚、非洲、拉丁美洲。事实来源轮换：Le Monde diplomatique、Politis、L'Humanité、Alternatives Économiques、Le Vent Se Lève、Revue Ballast、Regards、AOC；补充：Libération、Mediapart、Socialter、Frustration、Orient XXI、Afrique XXI、RFI、France Culture、Le Grand Continent、The Conversation France、Philosophie Magazine、France Musique、Courrier international。另附一份「Lectures」推荐（kind: picks），3–5 篇左翼杂志原文链接，付费墙文章照样列出并注明，不绕过。
- **Hannover**：每天早上德语推送附一条汉诺威本地短讯（hannover.de、Region Hannover、Presseportal 等公开渠道）。
- 话题（广，偏自由派/绿党/左翼视角）：移民与融合、难民、女性与平权、气候与环境、社会正义与劳工、科技与 AI、教育、科学、语言学、社会学、经济学、国际关系。避免连续两天同一领域。本地新闻不限话题。不写 AfD。
- 写法：每篇以一篇当期报道为出发点，用自己的话重新写成适合学习者的原创文章，不复制、不摘录、不近似改写原文，不编造引语；文末列出原文链接（「原文」）和其他事实来源，标注许可（all rights reserved 的来源只放链接）。

## 每日推荐（kind: picks）

- 每天早上推送德语、英语各一份「推荐」，3–6 篇值得读完的原文链接，只给标题、作者、出处和一句中文介绍，读者自己去原网站读。
- 英语可包含 The Guardian、The Atlantic、The New Yorker 等：只有当链接出现在可访问的推荐来源（如 Longreads）里时才列入，介绍只依据推荐来源的摘要。否则每天在英语推荐末尾附上 Guardian「The Long Read」和 Atlantic「Ideas」两个栏目入口（genre 写 Browse），读者自己去挑。
- 推荐覆盖面要广：政治与国际关系、经济、气候与环境、科学、语言学、社会学、文化、科技；德语和英语各 4–6 篇，避免和前两天重复同一领域。
- 不编造链接；每个 URL 都必须来自实际打开过的页面。

## 辅助语言：英文优先，简体中文辅助

- 德语、葡语、法语文章附逐段英文译文 `paragraphs_en`（App 里的「EN」按钮）；葡语另保留 `paragraphs_zh`（「中」按钮）。英语文章不附译文。
- 重点词汇 `glossary` 每条写 `{"w","en","zh"}`：英文释义为主，中文为辅（可简短）。
- 语法说明 `grammar` 用英文写，可在末尾加一句简短中文括注。
- 推荐阅读每条写英文介绍 `en`，可附简短中文 `zh`。
- 每周回顾用 `summary_en`、`explain_en`（可附中文）。
