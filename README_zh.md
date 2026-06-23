# 连环翻译工具 (Chain Translator)

[中文](README_zh.md) | [English](README.md)

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

> **注意**：由于 `gTTS` 依赖的 `urllib3` 版本需为 1.x，请务必指定 `urllib3==1.26.18` 以保证兼容性。

### 🚀 快速开始

### 可以不用加 `--output-audio-dir ./audio --output-text-dir ./results`，将默认保存在 `./15steps` 或者 `./20steps` 文件夹

```bash
# 从文件读取，逐句+全文翻译，生成音频和文本
python translator_chain.py --file test.txt --output-audio-dir ./audio --output-text-dir ./results
```

```bash
# 使用 20 步语言链
python translator_chain.py --file test.txt --chain-length 20 --output-audio-dir ./audio --output-text-dir ./results
```

```bash
# 使用 Bing 翻译服务，自定义简短语言链
python translator_chain.py --file test.txt --service bing --chain en ja zh-cn --output-audio-dir ./audio
```

```bash
# 命令行直接输入文本
python translator_chain.py "你好，世界。今天天气不错。" --output-text-dir ./results
```

### 📖 命令行参数

| 参数 | 说明 | 默认 |
| ------ | ------ | ------ |
| `text` | 要翻译的文本（与 `--file` 二选一） | - |
| `--file`, `-f` | 从 UTF-8 文本文件读取内容 | - |
| `--lines` | 按行分割句子（否则按句号分割） | - |
| `--delay` | 每次翻译请求后延迟秒数 | 1.0 |
| `--retries` | 单步翻译失败重试次数 | 3 |
| `--chain-length` | 预设语言链长度：15 或 20 | 15 |
| `--chain` | 自定义语言链（空格分隔），例如 `en ja zh-cn` | - |
| `--service` | 翻译服务：`google`, `bing`, `baidu`, `youdao`, `tencent`, `alibaba`, `deepl` | google |
| `--output-text-dir` | 保存最终翻译文本的根目录 | 15steps or 20steps |
| `--output-audio-dir` | 保存最终音频的根目录 | 15steps or 20steps |

### 📂 输出结构示例

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

## MIT License
