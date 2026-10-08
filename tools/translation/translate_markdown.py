#!/usr/bin/env python3
"""Translate markdown documentation files from Chinese to Vietnamese and English.

Preserves code blocks, inline code, links, image URLs, and table formatting.
"""
from __future__ import annotations

import argparse
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


def is_table_separator(line: str) -> bool:
    s = line.strip()
    if not s or not s.startswith("|") or not s.endswith("|"):
        return False
    cells = [c.strip() for c in s.split("|")[1:-1]]
    if not cells:
        return False
    return all(re.fullmatch(r":?-+:?", c) for c in cells)


def is_hr(line: str) -> bool:
    return line.strip() in ("---", "***", "___", "- - -", "* * *")


def fix_markdown_formatting(line: str, original: str) -> str:
    # 0. Fix split markdown symbols: '# #' -> '##', '* *' -> '**'
    while re.match(r"^#+\s+#", line):
        line = re.sub(r"^(#+)\s+#", r"\1#", line)
    line = re.sub(r"\*\s+\*", "**", line)
    line = re.sub(r"_\s+_", "__", line)

    # 1. Heading spacing: ensure space after hashes, but not between hashes
    if re.match(r"^#{1,6}[^#\s]", line):
        line = re.sub(r"^(#{1,6})([^#\s])", r"\1 \2", line)

    # 2. List spacing: bullet list (-, +, or * not followed by *)
    line = re.sub(r"^(\s*(?:[-+]|\*(?!\*)))([^\s\-*+])", r"\1 \2", line)
    # Numbered list: 1.item -> 1. item
    if re.match(r"^(\s*\d+\.)[^\s]", line):
        line = re.sub(r"^(\s*\d+\.)([^\s])", r"\1 \2", line)

    # 3. Blockquote spacing: >text -> > text
    if re.match(r"^(>+)[^\s>]", line):
        line = re.sub(r"^(>+)([^\s>])", r"\1 \2", line)

    # 4. Table row alignment
    orig_s = original.strip()
    line_s = line.strip()
    if orig_s.startswith("|") and not line_s.startswith("|"):
        line = "| " + line_s
    if orig_s.endswith("|") and not line_s.endswith("|"):
        line = line + " |"
    return line


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

    # 2. Protect inline code
    inline_codes = {}
    inline_counter = 0

    def protect_inline(m):
        nonlocal inline_counter
        key = f"__INL_CODE_{inline_counter}__"
        inline_counter += 1
        inline_codes[key] = m.group(0)
        return key

    # 3. Protect markdown link and image URLs
    url_map = {}
    url_counter = 0

    def protect_url(m):
        nonlocal url_counter
        prefix = m.group(1)
        url = m.group(2)
        key = f"__MD_URL_{url_counter}__"
        url_counter += 1
        url_map[key] = url
        return f"{prefix}({key})"

    lines_to_translate = []
    for line in processed_lines:
        if line.startswith("__CODE_FENCE_BLOCK_"):
            lines_to_translate.append(line)
        else:
            # First protect inline code
            protected = re.sub(r"`[^`\n]+`", protect_inline, line)
            # Then protect URLs in markdown links: [text](url) and ![alt](url)
            protected = re.sub(r"(\!?\[[^\]]*\])\(([^)\s]+(?:\s+[\"'][^\"']*[\"'])?)\)", protect_url, protected)
            lines_to_translate.append(protected)

    # 4. Filter lines to translate
    trans_indices = []
    batch_texts = []

    for i, line in enumerate(lines_to_translate):
        s = line.strip()
        if (
            line.startswith("__CODE_FENCE_BLOCK_")
            or not s
            or is_hr(s)
            or is_table_separator(s)
        ):
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
        time.sleep(0.04)

    for idx, tr in zip(trans_indices, translated_texts):
        lines_to_translate[idx] = fix_markdown_formatting(tr, processed_lines[idx])

    # 5. Restore URLs and code
    result_lines = []
    for line in lines_to_translate:
        if line.startswith("__CODE_FENCE_BLOCK_"):
            result_lines.append(code_blocks.get(line.strip(), line))
        else:
            restored = line
            # Restore URLs: handle `] ( __MD_URL_0__ )` or `](__MD_URL_0__)`
            for k, v in url_map.items():
                pattern = re.compile(rf"\]\s*\(\s*{re.escape(k)}\s*\)")
                restored = pattern.sub(f"]({v})", restored)
                restored = restored.replace(k, v)

            # Restore inline codes
            for k, v in inline_codes.items():
                restored = restored.replace(k, v)

            result_lines.append(restored)

    return "\n".join(result_lines)


def process_doc_file(doc_path: Path, force: bool = False):
    stem = doc_path.stem
    dir_path = doc_path.parent

    vi_path = dir_path / f"{stem}.vi.md"
    en_path = dir_path / f"{stem}.en.md"

    if not force and vi_path.exists() and en_path.exists():
        print(f"Skipping {doc_path.relative_to(ROOT)} (already exists).")
        return

    print(f"Processing {doc_path.relative_to(ROOT)}...")
    content = doc_path.read_text(encoding="utf-8")

    nav_vi = f"> **Ngôn ngữ / Language:** [Tiếng Việt]({stem}.vi.md) · [English]({stem}.en.md) · [中文]({stem}.md)\n\n"
    nav_en = f"> **Language / Ngôn ngữ:** [English]({stem}.en.md) · [Tiếng Việt]({stem}.vi.md) · [中文]({stem}.md)\n\n"
    nav_zh = f"> **语言 / Language:** [中文]({stem}.md) · [Tiếng Việt]({stem}.vi.md) · [English]({stem}.en.md)\n\n"

    # Add navigation bar to original if not present
    if not content.startswith("> **语言"):
        doc_path.write_text(nav_zh + content, encoding="utf-8")
        clean_content = content
    else:
        # Strip existing navigation bar when translating so it's not double-translated
        first_nl = content.find("\n\n")
        clean_content = content[first_nl + 2:] if first_nl != -1 else content

    # Generate VI
    if force or not vi_path.exists():
        print(f"  Generating {vi_path.name}...")
        vi_text = translate_markdown(clean_content, "vi", source_lang="zh-CN")
        vi_path.write_text(nav_vi + vi_text, encoding="utf-8")

    # Generate EN
    if force or not en_path.exists():
        print(f"  Generating {en_path.name}...")
        en_text = translate_markdown(clean_content, "en", source_lang="zh-CN")
        en_path.write_text(nav_en + en_text, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--file", type=str, default=None, help="Specific markdown file to translate")
    parser.add_argument("--dir", type=str, default=None, help="Directory of markdown files to translate (e.g. docs/gameplay)")
    parser.add_argument("--all", action="store_true", help="Translate all docs directories")
    parser.add_argument("--force", action="store_true", help="Force re-translation of existing files")
    args = parser.parse_args()

    if args.file:
        doc = Path(args.file)
        if not doc.is_absolute():
            doc = ROOT / doc
        process_doc_file(doc, force=args.force)
    elif args.dir:
        target_dir = Path(args.dir)
        if not target_dir.is_absolute():
            target_dir = ROOT / target_dir
        docs = sorted(target_dir.glob("*.md"))
        base_docs = [p for p in docs if not p.name.endswith(".vi.md") and not p.name.endswith(".en.md") and p.name != "README.md" and p.name != "website.md"]
        print(f"Translating {len(base_docs)} documents in {target_dir.relative_to(ROOT)}...")
        for doc in base_docs:
            process_doc_file(doc, force=args.force)
    elif args.all:
        for folder_name in ["gameplay", "script", "data", "native", "design"]:
            target_dir = ROOT / "docs" / folder_name
            docs = sorted(target_dir.glob("*.md"))
            base_docs = [p for p in docs if not p.name.endswith(".vi.md") and not p.name.endswith(".en.md") and p.name != "website.md"]
            print(f"Translating {len(base_docs)} documents in docs/{folder_name}...")
            for doc in base_docs:
                process_doc_file(doc, force=args.force)
    else:
        print("Please specify --file, --dir, or --all.")


if __name__ == "__main__":
    main()
