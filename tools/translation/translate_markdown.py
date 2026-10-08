#!/usr/bin/env python3
"""Translate markdown documentation files from Chinese to Vietnamese and English.

Preserves code blocks, inline code, links, and table formatting.
"""
from __future__ import annotations

import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def request_translate(text: str, sl: str = "zh-CN", tl: str = "vi", timeout: float = 12.0) -> str:
    url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={sl}&tl={tl}&dt=t&q=" + urllib.parse.quote(text)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    resp = urllib.request.urlopen(req, timeout=timeout)
    data = json.loads(resp.read().decode("utf-8"))
    return "".join(p[0] for p in data[0] if p and p[0])


def translate_chunk(chunk: list[str], sl: str = "zh-CN", tl: str = "vi") -> list[str]:
    if not chunk:
        return []
    separator = "\n===---===\n"
    body = separator.join(chunk)

    for attempt in range(3):
        try:
            translated_full = request_translate(body, sl, tl, timeout=15.0)
            parts = [s.strip() for s in translated_full.split("===---===")]
            if len(parts) == len(chunk):
                return parts
            break
        except Exception:
            time.sleep(1.0 * (attempt + 1))

    # Fallback to single requests
    results = []
    for t in chunk:
        success = False
        for attempt in range(3):
            try:
                tr = request_translate(t, sl, tl, timeout=10.0)
                results.append(tr.strip())
                success = True
                break
            except Exception:
                time.sleep(1.0)
        if not success:
            results.append(t)
        time.sleep(0.04)
    return results


def translate_markdown(content: str, target_lang: str, source_lang: str = "zh-CN") -> str:
    """Translate markdown text to target_lang ('vi' or 'en')."""
    lines = content.splitlines()
    code_blocks = {}
    code_block_counter = 0
    in_code_block = False
    current_block = []

    processed_lines = []
    
    # 1. Extract fenced code blocks
    for line in lines:
        if line.strip().startswith("```"):
            if not in_code_block:
                in_code_block = True
                current_block = [line]
            else:
                current_block.append(line)
                in_code_block = False
                key = f"__CODE_FENCE_BLOCK_{code_block_counter}__"
                code_block_counter += 1
                code_blocks[key] = "\n".join(current_block)
                processed_lines.append(key)
                current_block = []
        elif in_code_block:
            current_block.append(line)
        else:
            processed_lines.append(line)

    # 2. Protect inline code in remaining lines
    inline_codes = {}
    inline_counter = 0

    def protect_inline(m):
        nonlocal inline_counter
        key = f"__INL_CODE_{inline_counter}__"
        inline_counter += 1
        inline_codes[key] = m.group(0)
        return key

    lines_to_translate = []
    for line in processed_lines:
        if line.startswith("__CODE_FENCE_BLOCK_"):
            lines_to_translate.append(line)
        else:
            protected = re.sub(r"`[^`\n]+`", protect_inline, line)
            lines_to_translate.append(protected)

    # 3. Translate non-code, non-empty lines
    trans_indices = []
    batch_texts = []

    for i, line in enumerate(lines_to_translate):
        if line.startswith("__CODE_FENCE_BLOCK_") or not line.strip() or line.strip() == "---":
            continue
        trans_indices.append(i)
        batch_texts.append(line)

    # Batch translate in chunks of 25
    batch_size = 25
    translated_texts = []
    for i in range(0, len(batch_texts), batch_size):
        chunk = batch_texts[i:i + batch_size]
        translated_chunk = translate_chunk(chunk, sl=source_lang, tl=target_lang)
        translated_texts.extend(translated_chunk)
        time.sleep(0.05)

    for idx, tr in zip(trans_indices, translated_texts):
        # Fix table delimiters if translator messed them up
        if lines_to_translate[idx].strip().startswith("|") and not tr.strip().startswith("|"):
            tr = "| " + tr
        lines_to_translate[idx] = tr

    # 4. Restore inline code
    result_lines = []
    for line in lines_to_translate:
        if line.startswith("__CODE_FENCE_BLOCK_"):
            result_lines.append(code_blocks.get(line.strip(), line))
        else:
            restored = line
            for k, v in inline_codes.items():
                restored = restored.replace(k, v)
            result_lines.append(restored)

    return "\n".join(result_lines)


def process_guide_file(doc_path: Path, force: bool = False):
    stem = doc_path.stem
    dir_path = doc_path.parent

    vi_path = dir_path / f"{stem}.vi.md"
    en_path = dir_path / f"{stem}.en.md"

    if not force and vi_path.exists() and en_path.exists():
        print(f"Skipping {doc_path.name} (already exists).")
        return

    print(f"Processing {doc_path.name}...")
    content = doc_path.read_text(encoding="utf-8")

    nav_vi = f"> **Ngôn ngữ / Language:** [Tiếng Việt]({stem}.vi.md) · [English]({stem}.en.md) · [中文]({stem}.md)\n\n"
    nav_en = f"> **Language / Ngôn ngữ:** [English]({stem}.en.md) · [Tiếng Việt]({stem}.vi.md) · [中文]({stem}.md)\n\n"
    nav_zh = f"> **语言 / Language:** [中文]({stem}.md) · [Tiếng Việt]({stem}.vi.md) · [English]({stem}.en.md)\n\n"

    if stem == "pc-windows-build":
        # Already Vietnamese
        vi_path.write_text(nav_vi + content, encoding="utf-8")
        print(f"  Generating {en_path.name} from Vietnamese...")
        en_text = translate_markdown(content, "en", source_lang="vi")
        en_path.write_text(nav_en + en_text, encoding="utf-8")
        return

    # Add navigation bar to original if not present
    if not content.startswith("> **语言"):
        doc_path.write_text(nav_zh + content, encoding="utf-8")

    # Generate VI
    print(f"  Generating {vi_path.name}...")
    vi_text = translate_markdown(content, "vi", source_lang="zh-CN")
    vi_path.write_text(nav_vi + vi_text, encoding="utf-8")

    # Generate EN
    print(f"  Generating {en_path.name}...")
    en_text = translate_markdown(content, "en", source_lang="zh-CN")
    en_path.write_text(nav_en + en_text, encoding="utf-8")


def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--file", type=str, default=None, help="Specific markdown file to translate")
    parser.add_argument("--force", action="store_true", help="Force re-translation of existing files")
    args = parser.parse_args()

    guide_dir = ROOT / "docs/guide"
    if args.file:
        doc = Path(args.file) if Path(args.file).is_absolute() else guide_dir / args.file
        process_guide_file(doc, force=args.force)
    else:
        docs = sorted(guide_dir.glob("*.md"))
        base_docs = [p for p in docs if not p.name.endswith(".vi.md") and not p.name.endswith(".en.md")]
        print(f"Translating {len(base_docs)} guide documents in {guide_dir}...")
        for doc in base_docs:
            process_guide_file(doc, force=args.force)

    print("Done generating VI and EN guides!")


if __name__ == "__main__":
    main()
