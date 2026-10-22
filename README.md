# 字里行间 · Entrelinhas

> © 2026 申屠余夏 (Shentu Yuxia). **All rights reserved / Alle Rechte vorbehalten / 保留所有权利。** Free for personal, non-commercial learning in the app. Copying, redistribution, and any commercial or institutional use require prior written permission — see [LICENSE](LICENSE). Third-party components keep their own licences.


每天的外语阅读加单词卡：德语、英语、葡萄牙语（巴西）、法语。
Daily reading and flashcards in German, English, Brazilian Portuguese and French.

纯网页应用，部署在 GitHub Pages。没有服务器、没有构建步骤：改完文件推送到 `main` 就上线。

## 功能

- **今天（Today）**：间隔重复的单词卡，来自 `data/` 里的分级词库和自己存的词；每日目标和连续天数。
- **阅读（Read）**：每天自动更新的文章（见下文「每日内容」）。点任意词看释义（Wiktionary），存进单词本；逐段译文、重点词汇、语法说明、理解问题；每周回顾测验。「我的文章」：粘贴或导入自己的文本（Word `.docx`、PDF）来读。
- **朗读**：设备自带语音，或在设备上运行的开源神经语音 Piper（德、英、葡、法共 15 个声音，文字不离开设备）。
- **新词（New）**、**练习堆（Pile）**、**词表（Browse）**、**统计（Stats）**、**设置（Settings）**。
- **界面语言**：中文／English／Deutsch／Português；释义和语法说明的语言可单独设置，没有的语言退回英文。
- **同步**：用电子邮件登录（Supabase），或用自己的私有 GitHub 仓库保存进度。不登录时，一切只存在这台设备的浏览器里。见 `privacy.html`。
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

data/                   ← 单词卡词库：{语言}-{级别}.json，例如 de-B1.json
                          语言 de en pt fr，级别 A1–C2；每行 8 个字符串（格式见 tools/wb_add.py）

tools/
  mg_index.py             重新生成 marginalia/index.json
  wb_add.py               向词库添加单词（自动跳过重复）并检查所有词库文件

tts/piper-worker.js     Piper 神经语音（在 Web Worker 里运行）
vendor/                 第三方库：onnxruntime-web（ort/）、Piper 音素化（piper/）、
                        pdf.js（读 PDF）、mammoth（读 .docx）
fonts/                  自带字体：Source Sans 3、Source Serif 4（拉丁文），EL Hei / 霞鹜新晰黑（中文，按需加载的分片）
supabase/schema.sql     邮箱登录同步需要的数据表（在 Supabase 里运行一次）
```

## 每日内容（自动）

内容由 Claude 的定时任务每天写好并推送到这个仓库，App 打开时读取最新的 `marginalia/`。时间均为柏林时间：

| 时间 | 任务 | 写入 |
|---|---|---|
| 每天 03:23 | Wortschatz / Word bank | `data/`：每种语言约 150 个新词，从最低的未满级别开始 |
| 每天 06:13 | English | 一篇 C2 长文，按星期轮换主题 |
| 每天 06:37 | Lesetipps / Reading list | 德语、英语各一份「推荐阅读」原文链接 |
| 每天 06:52 | Deutsch | 一篇 C1 文化与生活长文（不写政治新闻）+ 一篇 B2 短文（「Wort & Wendung」词语来历／「Deutschland kurios」冷知识） |
| 每天 16:47 | Français | 两篇，一易一难，级别按星期轮换（见 `marginalia/config.json`）；不写推荐 |
| 每天 19:52 | Português | 连载故事「Tito e Ana」+ 一段日常对话（A1） |
| 周日 18:37 | Wochenrückblick | `marginalia/weekly.json`：本周回顾和测验 |

写作规则（选题、来源、立场、版权、文件格式）都在 `marginalia/README.md`，难度和来源清单在 `marginalia/config.json`。
每种语言每天最多两篇文章（推荐链接不算）。
**想改难度**：改 `marginalia/config.json` 里的 `levels`，第二天起生效。

## 手动维护

```sh
python3 tools/mg_index.py marginalia     # 改过或删过某天的文章后，重建目录
python3 tools/wb_add.py --check          # 检查词库格式，显示每个级别的进度
python3 tools/wb_add.py de B1 rows.json  # 把 rows.json 里的新词加进 de-B1（重复的自动跳过）
python3 -m http.server                   # 本地预览：打开 http://localhost:8000
```

> 本地预览必须用 `http://` 打开；直接双击 `index.html`（`file://`）读不到 `marginalia/` 和 `data/`。

## 上线与更新

- GitHub → Settings → Pages → Deploy from a branch → `main` / `(root)`。
- 内容文件（`marginalia/`、`data/`）总是先从网络读取，推送后马上可见。
- 程序文件（`index.html`、字体等）先用缓存、后台更新，所以改了界面以后**第二次**打开才看到新版。改了 `sw.js` 的缓存规则时，把里面的 `CACHE` 版本号加一。
- 邮箱登录：在 Supabase 项目里运行一次 `supabase/schema.sql`；`index.html` 里的 `SB_URL` 和公开的 publishable key 指向这个项目。

## 致谢与授权

- 释义：Wiktionary（CC BY-SA）
- 神经语音：Piper（rhasspy/piper-voices，各声音的授权见其模型说明），onnxruntime-web（MIT）
- pdf.js（Apache-2.0），mammoth.js（BSD-2-Clause）
- 字体：Source Sans 3、Source Serif 4（SIL OFL 1.1），霞鹜新晰黑 LXGW Neo XiHei（IPA Font License，见 `fonts/neoxihei/LICENSE.txt`）
- 文章均为原创写作；事实来源和许可列在每篇文章末尾。
