# 字里行间 · Entrelinhas

> © 2026 申屠余夏 (Shentu Yuxia). **All rights reserved / Alle Rechte vorbehalten / 保留所有权利。** Free for personal, non-commercial learning in the app. Copying, redistribution, and any commercial or institutional use require prior written permission — see [LICENSE](LICENSE). Third-party components keep their own licences.


每天的外语阅读加单词卡：德语、英语、葡萄牙语（巴西）、法语、西班牙语（拉美）。
Daily reading and flashcards in German, English, Brazilian Portuguese and French.

纯网页应用，部署在 GitHub Pages。没有服务器、没有构建步骤：改完文件推送到 `main` 就上线。

## 功能

- **今天（Today）**：间隔重复的单词卡，来自 `data/` 里的分级词库和自己存的词；每日目标和连续天数。
- **阅读（Read）**：每天自动更新的文章（见下文「每日内容」）。点任意词看释义（Wiktionary），存进单词本；逐段译文（葡、法、西语）、重点词汇、语法说明、理解问题。葡语和西语文章下有「写一写」：写几句，免费用 LanguageTool 检查拼写和语法（不需要 Key，草稿自动保存并同步）。「我的文章」：粘贴或导入自己的文本（Word `.docx`、PDF）来读。
- **朗读**：设备自带语音，或在设备上运行的开源神经语音 Piper（德、英、葡、法共 15 个声音，文字不离开设备）。
- **字典（Dictionary）**：葡语先查自带的离线词典（`dict/pt/`，约十几万词，含巴西发音 IPA；变位形式如 *falei* 自动指向 *falar*，说明按界面语言显示），查不到再联网查 Wiktionary；其他语言直接查 Wiktionary。附 Dicio、Duden、Cambridge、Larousse 等外部词典链接；查到的词直接收进闪卡，查不到的一键「自己加词」。
- **词匣（Word box）**：自己加词，浏览全部词汇和生词堆（练习堆）。
- **我的**：统计（Stats）和设置（Settings）。
- **界面语言**：中文／English／Deutsch／Português；释义和语法说明的语言可单独设置，没有的语言退回英文。
- **同步**：用电子邮件登录（Supabase），或用自己的私有 GitHub 仓库保存进度。改动后约 5 秒上传；App 开着时每分钟、切回 App 时都会取回其他设备的进度。每个浏览器（Safari、Chrome、加到主屏幕的 App）各算一台设备，都要用同一个邮箱登录。不登录时，一切只存在这台设备的浏览器里。见 `privacy.html`。
- **离线**：打开过一次以后没有网络也能用（`sw.js`）。

## 文件结构

```
index.html              整个应用：界面、样式、程序都在这一个文件里
sw.js                   离线缓存
manifest.webmanifest    加到主屏幕用的设置与图标
privacy.html            隐私说明
icon*.png, icon.svg, apple-touch-icon.png, favicon-32.png

marginalia/             ← 「阅读」页的内容（详细规则见 marginalia/README.md）
  YYYY-MM-DD.json         一天的文章和推荐
  index.json              所有日期和标题的目录（由 tools/mg_index.py 生成）
  config.json             每种语言的难度和来源清单
  weekly.json             每周回顾和测验

dict/pt/                ← 离线葡语词典：512 个分片 NNN.json + meta.json（由 tools/build_ptdict.py 在 GitHub 上生成，CC BY-SA 4.0，见 dict/pt/LICENSE.md）

data/                   ← 单词卡词库：{语言}-{级别}.json，例如 de-B1.json
                          语言 de en pt fr，级别 A1–C2；每行 8 个字符串（格式见 tools/wb_add.py）

tools/
  mg_index.py             重新生成 marginalia/index.json
  mg_recent.py            最近文章的一行摘要（定时任务用来避免重复，不必打开旧文件）
  wb_add.py               向词库添加单词（自动跳过重复）并检查所有词库文件
  build_ptdict.py         从 Wiktionary（kaikki.org 的 wiktextract 数据）生成 dict/pt/

.github/workflows/build-ptdict.yml   在 GitHub 上下载数据、运行 build_ptdict.py 并提交 dict/pt/（Actions 里可手动重跑以更新）

tts/piper-worker.js     Piper 神经语音（在 Web Worker 里运行）
vendor/                 第三方库：onnxruntime-web（ort/）、Piper 音素化（piper/）、
                        pdf.js（读 PDF）、mammoth（读 .docx）
fonts/                  自带字体：Source Sans 3、Source Serif 4（拉丁文），EL Hei / 霞鹜新晰黑（中文，按需加载的分片）
supabase/schema.sql     邮箱登录同步需要的数据表（在 Supabase 里运行一次）
```

## 每日内容（自动）

内容由 Claude 的定时任务每天写好并推送到这个仓库，App 打开时读取最新的 `marginalia/`。时间均为柏林时间：

| 时间 | 任务 | 模型 | 写入 |
|---|---|---|---|
| 周二、五 03:23 | Wortschatz / Word bank | Sonnet | `data/`：只扩充西语和德语口语 UG（其他词库暂停） |
| 周一至五 06:13 | English | Opus | 一篇 C2 长文 + 一篇 C1 短文，主题按星期轮换 |
| 周一至五 11:52 | Deutsch | Opus | 一篇 C1 文化与生活长文 + 一篇 B2 短文（Alltagsdeutsch／Deutschland kurios） |
| 周一、三、五 13:37 | Lesetipps / Reading list | Sonnet | 德语、英语各 2 个原文链接 |
| 周一至五 16:47 | Français | Opus | 一篇，级别按星期：一 A1、二 A2、三 B1、四 B2、五 C1 |
| 周一至五 17:41 | Español | Sonnet | 一段对话 + 一篇阅读（拉美文化、女性、日常），A1–B2 |
| 每天 19:52 | Português | Sonnet | 三篇 A1：日记 + 对话 + Textinho；生词进 `data/pt-BS.json` |
| 周三、六 21:23 | Histórias de canções / Crônica | Opus | B1/B2 文章给传承语朋友；周六另有一篇 A1 歌曲故事 |
| 每月 1 日 09:47 | 唱片盒 & 小事卡片 | Sonnet | `marginalia/records.json` |

写作规则（选题、来源、立场、版权、文件格式）都在 `marginalia/README.md`，难度和来源清单在 `marginalia/config.json`。
每种语言每天最多两篇文章（推荐链接不算；法语一篇）。各语言只写需要的辅助语言字段（见 `marginalia/README.md`「辅助语言」），写之前用 `tools/mg_recent.py` 看最近写过什么，不打开旧文件——这样省 token。
**想改难度**：改 `marginalia/config.json` 里的 `levels`，第二天起生效。

## 手动维护

```sh
python3 tools/mg_index.py marginalia     # 改过或删过某天的文章后，重建目录
python3 tools/mg_recent.py es 30         # 西语最近 30 天的文章，每篇一行
python3 tools/wb_add.py --check          # 检查词库格式，显示每个级别的进度
python3 tools/wb_add.py de B1 rows.json  # 把 rows.json 里的新词加进 de-B1（重复的自动跳过）
python3 -m http.server                   # 本地预览：打开 http://localhost:8000
```

> 本地预览必须用 `http://` 打开；直接双击 `index.html`（`file://`）读不到 `marginalia/` 和 `data/`。

## 上线与更新

- GitHub → Settings → Pages → Deploy from a branch → `main` / `(root)`。
- 内容文件（`marginalia/`、`data/`、`dict/`）总是先从网络读取，推送后马上可见。
- 程序文件（`index.html`、字体等）先用缓存、后台更新，所以改了界面以后**第二次**打开才看到新版。改了 `sw.js` 的缓存规则时，把里面的 `CACHE` 版本号加一。
- 邮箱登录：在 Supabase 项目里运行一次 `supabase/schema.sql`；`index.html` 里的 `SB_URL` 和公开的 publishable key 指向这个项目。

## 致谢与授权

- 释义：Wiktionary（CC BY-SA）；离线葡语词典数据来自 Wiktionary，经 wiktextract／kaikki.org 提取（CC BY-SA 4.0，见 `dict/pt/LICENSE.md`）
- 神经语音：Piper（rhasspy/piper-voices，各声音的授权见其模型说明），onnxruntime-web（MIT）
- pdf.js（Apache-2.0），mammoth.js（BSD-2-Clause）
- 字体：Source Sans 3、Source Serif 4（SIL OFL 1.1），霞鹜新晰黑 LXGW Neo XiHei（IPA Font License，见 `fonts/neoxihei/LICENSE.txt`）
- 文章均为原创写作；事实来源和许可列在每篇文章末尾。
