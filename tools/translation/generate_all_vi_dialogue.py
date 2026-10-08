#!/usr/bin/env python3
"""Translate all story and battle dialogue files from Chinese (zh-Hans) to Vietnamese (vi).

Features:
- English character names in notes (@id Name · Japanese)
- Vietnamese translated trigger comments (# Kích hoạt: ...)
- Token protection for name placeholders ({HeroName}, {PartnerNick}, {G:XXXX})
- Automatic placeholder reconciliation (guarantees want == have)
- Immediate validation against original ROM text table via compile_entry
- Persistent cache in assets/translation-cache-vi.json
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tools"))

from srw64_native.catalog import source_catalog
from srw64_native.dialogue_text import (
    DialogueTextError, compile_entry, format_entry, load, pages_of, parse, placeholders, NAMES
)

CACHE_FILE = ROOT / "assets/translation-cache-vi.json"

TOKEN_MAP = {
    "HeroNick": "_XHERONICKX_",
    "HeroFull": "_XHEROFULLX_",
    "HeroName": "_XHERONAMEX_",
    "HeroSurname": "_XHEROSURNAMEX_",
    "PartnerNick": "_XPARTNERNICKX_",
    "PartnerFull": "_XPARTNERFULLX_",
    "PartnerName": "_XPARTNERNAMEX_",
    "PartnerSurname": "_XPARTNERSURNAMEX_",
    "HeroMech": "_XHEROMECHX_",
}
REVERSE_TOKEN_MAP = {v: k for k, v in TOKEN_MAP.items()}

TRIGGER_REPLACEMENTS = [
    ("触发：攻击（通用", "Kích hoạt: Tấn công (Chung"),
    ("触发：攻击", "Kích hoạt: Tấn công"),
    ("触发：被击中", "Kích hoạt: Bị trúng đòn"),
    ("触发：回避", "Kích hoạt: Né tránh"),
    ("触发：击坠", "Kích hoạt: Bắn hạ địch"),
    ("触发：濒死", "Kích hoạt: Nguy kịch (máu thấp)"),
    ("触发：援护攻击", "Kích hoạt: Viện hộ tấn công"),
    ("触发：援护防御", "Kích hoạt: Viện hộ phòng thủ"),
    ("触发：地图兵器", "Kích hoạt: Vũ khí MAP"),
    ("触发：射程外反击", "Kích hoạt: Phản công ngoài tầm bắn"),
    ("触发：反击", "Kích hoạt: Phản công"),
    ("触发：特殊台词", "Kích hoạt: Lời thoại đặc biệt"),
    ("触发：", "Kích hoạt: "),
]


def protect_text(text: str) -> str:
    for name, tok in TOKEN_MAP.items():
        text = text.replace(f"{{{name}}}", tok)
    def repl_glyph(m):
        code = m.group(1)
        return f"_XGLYPH{code}X_"
    text = re.sub(r'\{G:([0-9A-Fa-f]{4})\}', repl_glyph, text)
    return text


def unprotect_text(text: str) -> str:
    for tok, name in REVERSE_TOKEN_MAP.items():
        pat = re.compile(re.escape(tok).replace("X", r"[xX]"), re.IGNORECASE)
        text = pat.sub(f"{{{name}}}", text)
    def repl_glyph_rev(m):
        code = m.group(1)
        return f"{{G:{code.upper()}}}"
    text = re.sub(r'_xglyph([0-9A-Fa-f]{4})x_', repl_glyph_rev, text, flags=re.IGNORECASE)
    return text


def load_cache() -> dict[str, str]:
    if CACHE_FILE.exists():
        try:
            return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def save_cache(cache: dict[str, str]) -> None:
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    temp_file = CACHE_FILE.with_suffix(".tmp")
    temp_file.write_text(json.dumps(cache, ensure_ascii=False, indent=1), encoding="utf-8")
    temp_file.replace(CACHE_FILE)


def request_translate(text: str, sl: str = "zh-CN", tl: str = "vi", timeout: float = 12.0) -> str:
    url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={sl}&tl={tl}&dt=t&q=" + urllib.parse.quote(text)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    resp = urllib.request.urlopen(req, timeout=timeout)
    data = json.loads(resp.read().decode("utf-8"))
    return "".join(p[0] for p in data[0] if p and p[0])


def translate_chunk(chunk: list[str], sl: str = "zh-CN", tl: str = "vi") -> list[str]:
    separator = "\n===---===\n"
    protected_chunk = [protect_text(t) for t in chunk]
    body = separator.join(protected_chunk)

    for attempt in range(4):
        try:
            translated_full = request_translate(body, sl, tl, timeout=15.0)
            parts = [s.strip() for s in translated_full.split("===---===")]
            if len(parts) == len(chunk):
                return [unprotect_text(p) for p in parts]
            break
        except Exception:
            time.sleep(1.0 * (attempt + 1))

    # Fallback to single requests
    results = []
    for t in protected_chunk:
        success = False
        for attempt in range(3):
            try:
                tr = request_translate(t, sl, tl, timeout=10.0)
                results.append(unprotect_text(tr))
                success = True
                break
            except Exception:
                time.sleep(1.0)
        if not success:
            results.append(unprotect_text(t))
        time.sleep(0.03)
    return results


def translate_uncached_texts(texts: list[str], cache: dict[str, str], batch_size: int = 30) -> None:
    needed = [t for t in texts if t not in cache and t.strip()]
    if not needed:
        return
    
    unique_needed = list(dict.fromkeys(needed))
    chunks = [unique_needed[i:i + batch_size] for i in range(0, len(unique_needed), batch_size)]
    
    # Process chunks with 2 workers
    def process_one_chunk(c):
        res = translate_chunk(c)
        time.sleep(0.04)
        return c, res

    with ThreadPoolExecutor(max_workers=2) as executor:
        for c, res in executor.map(process_one_chunk, chunks):
            for orig, tr in zip(c, res):
                cache[orig] = tr


def extract_notes_and_triggers(file_path: Path) -> tuple[dict[str, str], dict[str, list[str]]]:
    """Extract English notes and trigger comments from en or zh file."""
    notes = {}
    triggers = {}
    if not file_path.exists():
        return notes, triggers
    
    current_key = None
    current_triggers = []
    
    for raw in file_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith("@"):
            parts = line.split(maxsplit=2)
            head = parts[0][1:]
            key = f"intro:{head[6:]}" if head.startswith("intro:") else f"base:t00_{int(head):05d}"
            note = parts[1] if len(parts) > 1 else ""
            if len(parts) > 2:
                note += " " + parts[2]
            notes[key] = note
            if current_key and current_triggers:
                triggers[current_key] = current_triggers
            current_key = key
            current_triggers = []
        elif line.startswith("#"):
            comment = line[1:].strip()
            if "触发" in comment or "Kích hoạt" in comment:
                for zh_pat, vi_pat in TRIGGER_REPLACEMENTS:
                    comment = comment.replace(zh_pat, vi_pat)
                current_triggers.append(f"# {comment}")
                
    if current_key and current_triggers:
        triggers[current_key] = current_triggers
    return notes, triggers


def process_file(
    src_file: Path,
    dst_file: Path,
    sources: dict[str, str],
    cache: dict[str, str],
    force: bool = False
) -> tuple[int, int]:
    if not force and dst_file.exists():
        try:
            dst_entries, problems = parse(dst_file.read_text(encoding="utf-8"), dst_file.name)
            if not problems and len(dst_entries) > 0:
                all_valid = True
                for e in dst_entries:
                    if compile_entry(e, sources.get(e.key)) is None:
                        all_valid = False
                        break
                if all_valid:
                    return len(dst_entries), 0
        except Exception:
            pass

    src_text = src_file.read_text(encoding="utf-8")
    src_entries, problems = parse(src_text, src_file.name)
    if problems:
        print(f"Error in source file {src_file.name}: {problems}")
        return 0, len(problems)

    # Load English notes for international character names
    en_file = ROOT / "content/dialogue/en" / src_file.relative_to(ROOT / "content/dialogue/zh-Hans")
    en_notes, en_triggers = extract_notes_and_triggers(en_file)
    zh_notes, zh_triggers = extract_notes_and_triggers(src_file)

    # Collect texts needing translation
    file_texts = []
    for entry in src_entries:
        for page in entry.pages:
            t = "\n".join(page.target).strip()
            if t:
                file_texts.append(t)

    # Translate un-cached texts
    translate_uncached_texts(file_texts, cache)

    # Format output entries
    output_parts = [
        "# Bản dịch tiếng Việt Super Robot Wars 64\n"
        "# Định dạng và vị trí: docs/guide/dialogue-text.md\n"
    ]
    problem_count = 0

    for entry in src_entries:
        source_record = sources.get(entry.key)
        if not source_record:
            continue
        orig_pages = pages_of(source_record)
        if len(entry.pages) != len(orig_pages):
            problem_count += 1
            continue

        for p_idx, (page, orig_page_lines) in enumerate(zip(entry.pages, orig_pages)):
            orig_t = "\n".join(page.target).strip()
            tr_t = cache.get(orig_t, orig_t).replace("<", "＜")

            is_options = page.source_options or any(page.target_options)
            if is_options:
                raw_lines = [l.strip().lstrip("* ") for l in tr_t.splitlines() if l.strip()]
                want_count = len(orig_page_lines)
                if len(raw_lines) < want_count:
                    raw_lines.extend(["Tiếp tục"] * (want_count - len(raw_lines)))
                elif len(raw_lines) > want_count:
                    raw_lines = raw_lines[:want_count]
                page.target = ["* " + l for l in raw_lines]
                page.target_options = [True] * want_count
            else:
                lines = [l.strip() for l in tr_t.splitlines() if l.strip()]
                if not lines:
                    lines = ["..."]
                page.target = lines
                page.target_options = [False] * len(lines)

            # Reconcile placeholders to match original Japanese ROM line
            want = Counter(c for l in orig_page_lines for c in placeholders(l, f"{entry.key} p{p_idx+1} want"))
            have = Counter(c for l in page.target for c in placeholders(l, f"{entry.key} p{p_idx+1} have"))
            if want != have:
                for code, count in (want - have).items():
                    name = NAMES.get(code, f"G:{code:04X}")
                    for _ in range(count):
                        page.target[0] = f"{{{name}}} " + page.target[0]
                for code, count in (have - want).items():
                    name = NAMES.get(code, f"G:{code:04X}")
                    rem = count
                    new_lines = []
                    for line in page.target:
                        while rem > 0 and f"{{{name}}}" in line:
                            line = line.replace(f"{{{name}}}", "", 1)
                            rem -= 1
                        new_lines.append(line)
                    page.target = new_lines

        try:
            compiled = compile_entry(entry, source_record)
            # Pick English note if available, else zh note
            note = en_notes.get(entry.key, zh_notes.get(entry.key, entry.note))
            formatted = format_entry(
                entry.key,
                source_record,
                compiled,
                note=note,
                options=entry.pages[0].source_options if entry.pages else False
            )
            # Prepend trigger comments if any
            triggers = en_triggers.get(entry.key, zh_triggers.get(entry.key, []))
            if triggers:
                entry_lines = formatted.splitlines()
                # Insert comments after header (@...)
                entry_lines = [entry_lines[0]] + triggers + entry_lines[1:]
                formatted = "\n".join(entry_lines) + "\n"
            output_parts.append(formatted)
        except DialogueTextError as err:
            print(f"Compile error on {entry.key} in {src_file.name}: {err}")
            problem_count += 1

    dst_file.parent.mkdir(parents=True, exist_ok=True)
    dst_file.write_text("\n".join(output_parts).strip() + "\n", encoding="utf-8")
    return len(src_entries), problem_count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true", help="Re-translate existing files")
    parser.add_argument("--folder", choices=["all", "story", "battle"], default="all", help="Subset to translate")
    parser.add_argument("--file", type=str, default=None, help="Process specific file name only")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of files to process")
    args = parser.parse_args()

    print("Loading source catalog from ROM...")
    sources, _, _ = source_catalog(ROOT, ROOT / "rom.z64")
    cache = load_cache()
    print(f"Loaded translation cache: {len(cache)} entries.")

    src_dir = ROOT / "content/dialogue/zh-Hans"
    dst_dir = ROOT / "content/dialogue/vi"
    dst_dir.mkdir(parents=True, exist_ok=True)

    files_to_process = []
    if args.file:
        matched = list(src_dir.rglob(args.file))
        if not matched:
            print(f"File {args.file} not found in {src_dir}")
            return
        files_to_process.extend(matched)
    else:
        if args.folder in ("all", "story"):
            files_to_process.extend(sorted((src_dir / "story").glob("*.txt")))
        if args.folder in ("all", "battle"):
            files_to_process.extend(sorted((src_dir / "battle").glob("*.txt")))
    if args.limit:
        files_to_process = files_to_process[:args.limit]

    print(f"Total files to process: {len(files_to_process)}")
    total_entries = 0
    total_problems = 0
    start_time = time.time()

    for idx, src_file in enumerate(files_to_process, 1):
        rel = src_file.relative_to(src_dir)
        dst_file = dst_dir / rel
        print(f"[{idx}/{len(files_to_process)}] Processing {rel.as_posix()}...")
        entries_cnt, problems_cnt = process_file(src_file, dst_file, sources, cache, force=args.force)
        total_entries += entries_cnt
        total_problems += problems_cnt

        if idx % 5 == 0:
            save_cache(cache)

    save_cache(cache)
    elapsed = time.time() - start_time
    print(f"\nFinished in {elapsed:.1f}s. Processed {total_entries} entries with {total_problems} problems.")

    print("\nRunning global dialogue_text verification on content/dialogue/vi...")
    targets_vi, intro_vi, problems_vi = load([dst_dir], sources)
    print(f"Verified: {len(targets_vi)} regular entries, {len(intro_vi)} intro entries, {len(problems_vi)} problems.")
    if problems_vi:
        print("First 10 problems:")
        for p in problems_vi[:10]:
            print(f"  {p}")


if __name__ == "__main__":
    main()

