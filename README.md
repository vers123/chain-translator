# 连环翻译工具 (Chain Translator)

[中文](#chinese) | [English](#english)

---

<h2 id="chinese">🇨🇳 中文版</h2>
## 🇨🇳 中文版

一个支持多语言连环翻译、生成音频文件、自动分类保存的翻译工具。原始文本经过自定义语言链（如 中文→英语→日语→...→中文）逐级翻译，最终得到有趣的信息变形结果。

### ✨ 主要功能

- 🔄 **连环翻译**：按自定义语言链（默认15步）逐级翻译，最终回到原语言。
- 🔊 **生成音频**：将最终翻译结果自动合成为 MP3 音频文件（不实时播放）。
- 🌐 **多翻译服务**：支持 Google、Bing、百度、有道、腾讯、阿里、DeepL 等（通过 `translators` 库）。
- 📁 **结构化输出**：
  - 逐句翻译结果保存为独立子文件夹（`sentence_001/final_text.txt`、`sentence_001/final.mp3`）
  - 全文翻译结果保存于 `full/` 子文件夹
  - 同时生成汇总文本文件（`sentence_results.txt`、`full_result.txt`）
- 🛡️ **文件冲突处理**：覆盖/跳过/重命名/取消，灵活控制输出。
- 🔁 **重试与延迟**：网络不稳定时自动重试，可调请求间隔。

### 📦 安装

```bash
git clone <repository-url>
cd translator_chain
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
.venv\Scripts\activate         # Windows
pip install -r requirements.txt
```

`requirements.txt` 内容：
```
gTTS>=2.5.0
translators>=5.9.0
deep-translator>=1.11.0
urllib3==1.26.18
```

> **注意**：由于 `gTTS` 依赖的 `urllib3` 版本需为 1.x，请务必指定 `urllib3==1.26.18` 以保证兼容性。

### 🚀 快速开始

```bash
# 从文件读取，逐句+全文翻译，生成音频和文本
python translator_chain.py --file test.txt --output-audio-dir ./audio --output-text-dir ./results

# 使用 20 步语言链
python translator_chain.py --file test.txt --chain-length 20 --output-audio-dir ./audio --output-text-dir ./results

# 使用 Bing 翻译服务，自定义简短语言链
python translator_chain.py --file test.txt --service bing --chain en ja zh-cn --output-audio-dir ./audio

# 命令行直接输入文本
python translator_chain.py "你好，世界。今天天气不错。" --output-text-dir ./results
```

### 📖 命令行参数

| 参数 | 说明 |
|------|------|
| `text` | 要翻译的文本（与 `--file` 二选一） |
| `--file`, `-f` | 从 UTF-8 文本文件读取内容 |
| `--lines` | 按行分割句子（否则按句号分割） |
| `--delay` | 每次翻译请求后延迟秒数（默认 1.0） |
| `--retries` | 单步翻译失败重试次数（默认 3） |
| `--chain-length` | 预设语言链长度：15 或 20（默认 15） |
| `--chain` | 自定义语言链（空格分隔），例如 `en ja zh-cn` |
| `--service` | 翻译服务：`google`, `bing`, `baidu`, `youdao`, `tencent`, `alibaba`, `deepl`（默认 google） |
| `--output-text-dir` | 保存最终翻译文本的根目录 |
| `--output-audio-dir` | 保存最终音频的根目录 |

### 📂 输出结构示例

```
15steps/
    results/
        sentence_001/final_text.txt
        sentence_002/final_text.txt
        full/final_text.txt
        sentence_results.txt
        full_result.txt
    audio/
        sentence_001/final.mp3
        sentence_002/final.mp3
        full/final.mp3
```

- 使用 `--chain-length 20` → `20steps/`
- 使用 `--chain` → `custom/`

### 🛠️ 常见问题

**Q: 为什么翻译结果有时不准确？**  
A: 这是连环翻译的“传话游戏”特性，用于娱乐和测试语言模型。

**Q: 翻译服务需要 API key 吗？**  
A: `translators` 库基于网页爬虫，无需 key，但稳定性不如官方 API。

**Q: 遇到 `ModuleNotFoundError: No module named 'urllib3.contrib.anytls'` 怎么办？**  
A: 执行以下命令降级 urllib3：
```bash
pip uninstall urllib3 urllib3-future -y
pip install urllib3==1.26.18
```

### 📄 许可证

MIT License

---

<h2 id="english">🇬🇧 English Version</h2>
## 🇬🇧 English Version

**Chain Translator** – A tool that performs multi‑step language chaining, generates audio files (MP3), and organizes output automatically. The original text is translated step by step through a custom language chain (e.g. Chinese → English → Japanese → ... → Chinese), resulting in an interesting “telephone game” effect.

### ✨ Features

- 🔄 **Chain translation**: Translate through a user‑defined language chain (default 15 steps) and finally return to the original language.
- 🔊 **Generate audio**: Convert the final translation into an MP3 file (no real‑time playback).
- 🌐 **Multiple translation services**: Google, Bing, Baidu, Youdao, Tencent, Alibaba, DeepL (via `translators` library).
- 📁 **Structured output**:
  - Each sentence gets its own subfolder: `sentence_001/final_text.txt` + `sentence_001/final.mp3`
  - Full text output under `full/` subfolder
  - Summary files: `sentence_results.txt`, `full_result.txt`
- 🛡️ **File conflict handling**: Overwrite / Skip / Rename / Cancel.
- 🔁 **Retry & delay**: Automatic retries with exponential backoff.

### 📦 Installation

```bash
git clone <repository-url>
cd translator_chain
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
.venv\Scripts\activate         # Windows
pip install -r requirements.txt
```

`requirements.txt` content:
```
gTTS>=2.5.0
translators>=5.9.0
deep-translator>=1.11.0
urllib3==1.26.18
```

> **Note**: `urllib3==1.26.18` is required for compatibility with Python 3.13+.

### 🚀 Quick Start

```bash
# Read from file, sentence‑by‑sentence + full‑text translation, generate audio & text
python translator_chain.py --file test.txt --output-audio-dir ./audio --output-text-dir ./results

# Use 20‑step language chain
python translator_chain.py --file test.txt --chain-length 20 --output-audio-dir ./audio --output-text-dir ./results

# Use Bing service with a custom short chain
python translator_chain.py --file test.txt --service bing --chain en ja zh-cn --output-audio-dir ./audio

# Direct text input
python translator_chain.py "Hello, world. Nice weather today." --output-text-dir ./results
```

### 📖 Command Line Arguments

| Argument | Description |
|----------|-------------|
| `text` | Text to translate (mutually exclusive with `--file`) |
| `--file`, `-f` | Read from a UTF‑8 text file |
| `--lines` | Split by line instead of by sentence‑ending punctuation |
| `--delay` | Delay between API requests (default 1.0) |
| `--retries` | Number of retries per translation step (default 3) |
| `--chain-length` | Preset chain length: 15 or 20 (default 15) |
| `--chain` | Custom language chain (space‑separated), e.g. `en ja zh-cn` |
| `--service` | Translation service: `google`, `bing`, `baidu`, `youdao`, `tencent`, `alibaba`, `deepl` (default `google`) |
| `--output-text-dir` | Root directory for saving final text files |
| `--output-audio-dir` | Root directory for saving final MP3 files |

### 📂 Output Structure Example

```
15steps/
    results/
        sentence_001/final_text.txt
        sentence_002/final_text.txt
        full/final_text.txt
        sentence_results.txt
        full_result.txt
    audio/
        sentence_001/final.mp3
        sentence_002/final.mp3
        full/final.mp3
```

- `--chain-length 20` → `20steps/`
- `--chain` → `custom/`

### 🛠️ FAQ

**Q: Why are the results sometimes inaccurate or strange?**  
A: This is the intended “telephone game” behavior – it’s for fun and testing language models, not professional translation.

**Q: Do any translation services require an API key?**  
A: The `translators` library uses web scraping, so no key is needed, but reliability may be lower than official APIs.

**Q: I get `ModuleNotFoundError: No module named 'urllib3.contrib.anytls'`.**  
A: Downgrade `urllib3` with:
```bash
pip uninstall urllib3 urllib3-future -y
pip install urllib3==1.26.18
```

### 📄 License

MIT License
```

## ✨ 更新说明

- **语言切换**：在文件顶部添加了 `[中文]` 和 `[English]` 链接，点击可跳转到同一文件内的对应章节。
- **完整英文翻译**：将原有中文所有内容（功能、安装、参数、输出结构、FAQ 等）逐项翻译为英文，保持格式一致。
- **保持兼容**：原有中文内容不变，仅增加了英文版本和锚点。