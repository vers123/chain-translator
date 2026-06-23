# Chain Translator

[中文](README_zh.md) | [English](README.md)

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
git clone https://github.com/vers123/chain-translator.git
```

```bash
cd translator_chain
```

```bash
python -m venv .venv
```

```bash
# Linux/macOS
source .venv/bin/activate
```

```bash
# Windows
.venv\Scripts\activate
```

```bash
pip install -r requirements.txt
```

> **Note**: `urllib3==1.26.18` is required for compatibility with Python 3.13+.

### 🚀 Quick Start

### You do not need to include `--output-audio-dir ./audio --output-text-dir ./results`; the files will be saved by default in the `./15steps` or `./20steps` folder.

```bash
# Read from file, sentence‑by‑sentence + full‑text translation, generate audio & text
python translator_chain.py --file ./test/test.txt --output-audio-dir ./audio --output-text-dir ./results
```

```bash
# Use 20‑step language chain
python translator_chain.py --file ./test/test.txt --chain-length 20 --output-audio-dir ./audio --output-text-dir ./results
```

```bash
# Use Bing service with a custom short chain
python translator_chain.py --file ./test/test.txt --service bing --chain en ja zh-cn --output-audio-dir ./audio
```

```bash
# Direct text input
python translator_chain.py "Hello, world. Nice weather today." --output-text-dir ./results
```

### 📖 Command Line Arguments

| Argument | Description | default |
| ---------- | ------------- | ------------- |
| `text` | Text to translate (mutually exclusive with `--file`) | - |
| `--file`, `-f` | Read from a UTF‑8 text file | - |
| `--lines` | Split by line instead of by sentence‑ending punctuation | - |
| `--delay` | Delay between API requests | 1.0 |
| `--retries` | Number of retries per translation step | 3 |
| `--chain-length` | Preset chain length: 15 or 20 | 15 |
| `--chain` | Custom language chain (space‑separated), e.g. `en ja zh-cn` | - |
| `--service` | Translation service: `google`, `bing`, `baidu`, `youdao`, `tencent`, `alibaba`, `deepl` | google |
| `--output-text-dir` | Root directory for saving final text files | 15steps or 20steps |
| `--output-audio-dir` | Root directory for saving final MP3 files | 15steps or 20steps |

### 📂 Output Structure Example

```text
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

## MIT License
