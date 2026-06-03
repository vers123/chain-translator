import io
import time
import re
import os
import sys
import argparse
from typing import List, Optional
from enum import Enum

from gtts import gTTS

try:
    import translators as ts
    TRANSLATORS_AVAILABLE = True
except ImportError:
    TRANSLATORS_AVAILABLE = False
    print("⚠️ 未安装 translators 库，将仅支持 Google 翻译。如需多服务支持请运行: pip install translators")


# ---------- 配置 ----------
# 15 步默认语言链
DEFAULT_LANG_CHAIN = [
    'en', 'ja', 'ko', 'fr', 'de', 'es', 'it',
    'ru', 'ar', 'hi', 'pt', 'nl', 'tr', 'th', 'zh-cn'
]

# 20 步语言链
LANG_CHAIN_20 = [
    'en', 'ja', 'ko', 'fr', 'de', 'es', 'it',
    'ru', 'ar', 'hi', 'pt', 'nl', 'tr', 'th',
    'vi', 'id', 'ms', 'pl', 'uk', 'zh-cn'
]

SUPPORTED_SERVICES = ['google', 'bing', 'baidu', 'youdao', 'tencent', 'alibaba', 'deepl'] if TRANSLATORS_AVAILABLE else ['google']

GTTS_LANG_MAP = {
    'zh-cn': 'zh',
    'zh-tw': 'zh',
    'pt': 'pt',
    'ar': 'ar',
    'hi': 'hi',
}

def get_gtts_lang(lang_code: str) -> str:
    return GTTS_LANG_MAP.get(lang_code, lang_code)


# ---------- 文件冲突处理 ----------
class ConflictStrategy(Enum):
    OVERWRITE = 1
    SKIP = 2
    RENAME = 3
    CANCEL = 4

def get_conflict_strategy() -> ConflictStrategy:
    print("\n⚠️ 输出目录中存在同名文件。请选择处理方式：")
    print("  1. 覆盖所有 (overwrite)")
    print("  2. 跳过所有 (skip)")
    print("  3. 重命名新文件 (rename，自动添加数字后缀)")
    print("  4. 取消执行 (cancel)")
    choice = input("请输入数字 (1-4): ").strip()
    if choice == '1':
        return ConflictStrategy.OVERWRITE
    elif choice == '2':
        return ConflictStrategy.SKIP
    elif choice == '3':
        return ConflictStrategy.RENAME
    else:
        return ConflictStrategy.CANCEL

def resolve_file_path(filepath: str, strategy: ConflictStrategy) -> Optional[str]:
    if strategy == ConflictStrategy.OVERWRITE:
        return filepath
    elif strategy == ConflictStrategy.SKIP:
        if os.path.exists(filepath):
            print(f"⏭️ 跳过已存在文件: {filepath}")
            return None
        return filepath
    elif strategy == ConflictStrategy.RENAME:
        if not os.path.exists(filepath):
            return filepath
        base, ext = os.path.splitext(filepath)
        counter = 1
        while True:
            new_path = f"{base}_{counter}{ext}"
            if not os.path.exists(new_path):
                print(f"✏️ 重命名为: {new_path}")
                return new_path
            counter += 1
    else:
        print("❌ 用户取消执行。")
        sys.exit(0)


# ---------- 音频保存器（仅保存，不播放） ----------
class AudioSaver:
    def __init__(self):
        pass

    def save_audio(self, text: str, lang_code: str, filepath: str, strategy: ConflictStrategy) -> bool:
        """保存文本为音频文件，不播放"""
        if not text.strip():
            return False
        target_path = resolve_file_path(filepath, strategy)
        if target_path is None:
            return False
        try:
            tts = gTTS(text, lang=lang_code, slow=False)
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            tts.save(target_path)
            print(f"💾 音频已保存: {target_path}")
            return True
        except Exception as e:
            print(f"❌ 保存音频失败 {target_path}: {e}")
            return False


# ---------- 多服务翻译器 ----------
class MultiServiceTranslator:
    def __init__(self, service: str = 'google', retries: int = 3):
        self.service = service.lower()
        self.retries = retries
        if service not in SUPPORTED_SERVICES:
            print(f"⚠️ 服务 '{service}' 不支持，已回退到 'google'")
            self.service = 'google'
        if not TRANSLATORS_AVAILABLE and self.service != 'google':
            print(f"⚠️ translators 库未安装，无法使用 '{self.service}'，回退到 Google 翻译")
            self.service = 'google'

    def translate(self, text: str, source_lang: str, target_lang: str) -> Optional[str]:
        if source_lang == target_lang:
            return text
        for attempt in range(1, self.retries + 1):
            try:
                if TRANSLATORS_AVAILABLE:
                    translated = ts.translate_text(
                        text,
                        from_language=source_lang,
                        to_language=target_lang,
                        translator=self.service
                    )
                    return translated
                else:
                    from deep_translator import GoogleTranslator
                    translator = GoogleTranslator(source=source_lang, target=target_lang)
                    return translator.translate(text)
            except Exception as e:
                print(f"  ⚠️ 翻译尝试 {attempt}/{self.retries} 失败 ({self.service}): {e}")
                if attempt < self.retries:
                    time.sleep(2 ** attempt)
                else:
                    return None
        return None


# ---------- 翻译链 ----------
class TranslatorChain:
    def __init__(self, lang_chain: List[str], audio_saver: Optional[AudioSaver] = None,
                 request_delay: float = 1.0, retries: int = 3, service: str = 'google'):
        self.lang_chain = lang_chain
        self.audio_saver = audio_saver
        self.request_delay = request_delay
        self.retries = retries
        self.service = service
        self.translator = MultiServiceTranslator(service=service, retries=retries)

    def translate_full(self, text: str, verbose: bool = True,
                       audio_save_dir: Optional[str] = None,
                       text_save_dir: Optional[str] = None,
                       audio_conflict_strategy: ConflictStrategy = ConflictStrategy.OVERWRITE,
                       text_conflict_strategy: ConflictStrategy = ConflictStrategy.OVERWRITE,
                       context: str = "") -> str:
        """
        执行翻译链，保存最终音频和文本（不播放任何语音）
        """
        current_text = text
        current_lang = 'zh-cn'

        if verbose:
            preview = current_text[:100] + '…' if len(current_text) > 100 else current_text
            print(f"🌱 原始文本: {preview}")

        for i, target_lang in enumerate(self.lang_chain, 1):
            if verbose:
                print(f"  🔄 第 {i} 步: 翻译到 [{target_lang}] (服务: {self.service})")

            translated = self.translator.translate(current_text, current_lang, target_lang)
            if translated is None:
                if verbose:
                    print("  ⚠️ 翻译中断，保留上一结果")
                break

            if verbose:
                preview = translated[:80] + '…' if len(translated) > 80 else translated
                print(f"     📝 {preview}")

            # 不再播放任何语音，只更新文本和语言
            current_text = translated
            current_lang = target_lang

            if i < len(self.lang_chain):
                time.sleep(self.request_delay)

        # 保存最终音频（始终保存，只要指定了目录）
        if audio_save_dir and self.audio_saver:
            final_audio_dir = os.path.join(audio_save_dir, context)
            final_audio_path = os.path.join(final_audio_dir, "final.mp3")
            final_lang_gtts = get_gtts_lang('zh-cn')
            self.audio_saver.save_audio(current_text, final_lang_gtts, final_audio_path, audio_conflict_strategy)

        # 保存最终文本
        if text_save_dir:
            final_text_dir = os.path.join(text_save_dir, context)
            final_text_path = os.path.join(final_text_dir, "final_text.txt")
            target_path = resolve_file_path(final_text_path, text_conflict_strategy)
            if target_path:
                try:
                    os.makedirs(os.path.dirname(target_path), exist_ok=True)
                    with open(target_path, 'w', encoding='utf-8') as f:
                        f.write(current_text)
                    print(f"📄 最终文本已保存: {target_path}")
                except Exception as e:
                    print(f"❌ 保存文本失败: {e}")

        if verbose:
            final_preview = current_text[:100] + '…' if len(current_text) > 100 else current_text
            print(f"  ✅ 最终中文: {final_preview}\n")
        return current_text


# ---------- 文本处理工具 ----------
def split_sentences(text: str) -> List[str]:
    sentences = re.split(r'(?<=[。.])', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    return sentences

def read_text_from_file(filepath: str, by_lines: bool = False) -> str:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            if by_lines:
                lines = [line.strip() for line in f if line.strip()]
                return '\n'.join(lines)
            else:
                return f.read().strip()
    except FileNotFoundError:
        print(f"❌ 文件不存在: {filepath}")
        raise
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")
        raise

def save_translation_result(filepath: str, content: str, strategy: ConflictStrategy, mode: str = 'w'):
    target_path = resolve_file_path(filepath, strategy)
    if target_path is None:
        return
    try:
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        with open(target_path, mode, encoding='utf-8') as f:
            f.write(content)
        print(f"📄 翻译结果已保存: {target_path}")
    except Exception as e:
        print(f"❌ 保存文本失败: {e}")


# ---------- 主程序 ----------
def main():
    parser = argparse.ArgumentParser(description="连环翻译工具：支持多翻译服务，只保存最终音频和文本（不实时朗读）")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("text", nargs="?", default=None,
                       help="要翻译的文本（命令行直接输入，与 --file 二选一）")
    group.add_argument("--file", "-f", type=str, help="从文本文件读取要翻译的内容（UTF-8 编码）")
    parser.add_argument("--lines", action="store_true",
                        help="按行分割句子（每行为一个独立句子），默认按句号分割")
    
    parser.add_argument("--delay", type=float, default=1.0, help="翻译请求间延迟（秒）")
    parser.add_argument("--retries", type=int, default=3, help="单次翻译重试次数")
    
    parser.add_argument("--chain-length", type=int, choices=[15, 20], default=15,
                        help="选择预设语言链长度：15 步或 20 步（默认 15）。若同时使用 --chain 则此参数被忽略")
    parser.add_argument("--chain", nargs="+", default=None,
                        help="自定义语言链（空格分隔），例如：en ja zh-cn。若提供则忽略 --chain-length")
    
    parser.add_argument("--service", type=str, default="google", choices=SUPPORTED_SERVICES,
                        help=f"选择翻译服务: {', '.join(SUPPORTED_SERVICES)} (默认: google)")
    parser.add_argument("--output-text-dir", type=str, default=None,
                        help="保存翻译结果文本的根目录（会在其中为每个句子创建子文件夹，并生成汇总文件）")
    parser.add_argument("--output-audio-dir", type=str, default=None,
                        help="保存最终音频的根目录（会在其中为每个句子创建子文件夹，保存 final.mp3）")
    args = parser.parse_args()

    # 确定使用的语言链
    if args.chain:
        lang_chain = args.chain
        chain_folder = "custom"
        print(f"📌 使用自定义语言链（{len(lang_chain)} 步）: {' → '.join(lang_chain)}")
    else:
        if args.chain_length == 20:
            lang_chain = LANG_CHAIN_20
            chain_folder = "20steps"
            print(f"📌 使用预设 20 步语言链: {' → '.join(lang_chain)}")
        else:
            lang_chain = DEFAULT_LANG_CHAIN
            chain_folder = "15steps"
            print(f"📌 使用预设 15 步语言链: {' → '.join(lang_chain)}")

    # 构建输出路径：放在链文件夹下
    def build_output_path(user_dir: Optional[str], base_folder: str) -> Optional[str]:
        if user_dir is None:
            return None
        user_dir = user_dir.rstrip(os.sep)
        base_name = os.path.basename(user_dir)
        parent = os.path.join(os.getcwd(), base_folder)
        new_path = os.path.join(parent, base_name)
        return new_path

    if args.output_text_dir is None:
        text_output_dir = build_output_path("results", chain_folder)
    else:
        text_output_dir = build_output_path(args.output_text_dir, chain_folder)
    
    if args.output_audio_dir is None:
        audio_output_dir = build_output_path("audio", chain_folder)
    else:
        audio_output_dir = build_output_path(args.output_audio_dir, chain_folder)

    print(f"📁 文本输出目录: {text_output_dir}")
    print(f"📁 音频输出目录: {audio_output_dir}")

    # 获取待翻译文本
    if args.file:
        try:
            full_text = read_text_from_file(args.file, by_lines=False)
            if args.lines:
                sentences = [line for line in full_text.split('\n') if line.strip()]
                print(f"📄 从文件读取 {len(sentences)} 行（行模式）")
            else:
                sentences = split_sentences(full_text)
                print(f"📄 从文件读取全文，按句号分为 {len(sentences)} 个句子")
        except Exception:
            return
    else:
        if not args.text:
            print("❌ 请提供文本（--file 或直接传入文本）")
            return
        full_text = args.text
        if args.lines:
            sentences = [line.strip() for line in full_text.split('\n') if line.strip()]
            print(f"📝 命令行输入，按行分为 {len(sentences)} 行")
        else:
            sentences = split_sentences(full_text)
            print(f"📝 命令行输入，按句号分为 {len(sentences)} 个句子")

    if not sentences:
        print("⚠️ 未检测到有效句子，退出")
        return

    # 冲突检测
    text_conflict_strategy = ConflictStrategy.OVERWRITE
    audio_conflict_strategy = ConflictStrategy.OVERWRITE
    any_exists = False
    if text_output_dir and os.path.exists(text_output_dir):
        sent_summary = os.path.join(text_output_dir, "sentence_results.txt")
        full_summary = os.path.join(text_output_dir, "full_result.txt")
        if os.path.exists(sent_summary) or os.path.exists(full_summary):
            any_exists = True
        elif any(os.scandir(text_output_dir)):
            any_exists = True
    if audio_output_dir and os.path.exists(audio_output_dir) and os.listdir(audio_output_dir):
        any_exists = True
    if any_exists:
        strategy = get_conflict_strategy()
        text_conflict_strategy = strategy
        audio_conflict_strategy = strategy

    audio_saver = AudioSaver()
    translator = TranslatorChain(
        lang_chain=lang_chain,
        audio_saver=audio_saver,
        request_delay=args.delay,
        retries=args.retries,
        service=args.service
    )

    # 逐句翻译
    print("\n" + "=" * 60)
    print("📌 逐句翻译模式（每个句子独立经过翻译链）")
    print("=" * 60)
    sentence_results = []
    for idx, sent in enumerate(sentences, 1):
        context = f"sentence_{idx:03d}"
        print(f"\n--- 句子 {idx}: {sent} ---")
        final = translator.translate_full(
            sent, verbose=True,
            audio_save_dir=audio_output_dir,
            text_save_dir=text_output_dir,
            audio_conflict_strategy=audio_conflict_strategy,
            text_conflict_strategy=text_conflict_strategy,
            context=context
        )
        sentence_results.append(final)

    if text_output_dir:
        summary_file = os.path.join(text_output_dir, "sentence_results.txt")
        content = "\n".join([f"{i}. {res}" for i, res in enumerate(sentence_results, 1)])
        save_translation_result(summary_file, content, text_conflict_strategy)

    print("\n📋 逐句翻译最终结果：")
    for idx, res in enumerate(sentence_results, 1):
        print(f"{idx}. {res}")

    # 全文翻译
    print("\n" + "=" * 60)
    print("📌 全文翻译模式（整个文本作为一个整体）")
    print("=" * 60)
    if args.lines:
        full_text_for_translate = '\n'.join(sentences)
    else:
        full_text_for_translate = full_text

    full_result = translator.translate_full(
        full_text_for_translate, verbose=True,
        audio_save_dir=audio_output_dir,
        text_save_dir=text_output_dir,
        audio_conflict_strategy=audio_conflict_strategy,
        text_conflict_strategy=text_conflict_strategy,
        context="full"
    )

    if text_output_dir:
        full_summary_file = os.path.join(text_output_dir, "full_result.txt")
        save_translation_result(full_summary_file, full_result, text_conflict_strategy)

    print("\n📋 全文翻译最终结果：")
    print(full_result)


if __name__ == "__main__":
    main()