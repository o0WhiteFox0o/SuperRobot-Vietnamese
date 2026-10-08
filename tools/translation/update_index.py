#!/usr/bin/env python3
"""Update docs/README.md table columns to include Vietnamese and English document links."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
README_PATH = ROOT / "docs/README.md"


def update_docs_index():
    content = README_PATH.read_text(encoding="utf-8")
    sections = re.split(r"\n(?=## )", content)
    new_sections = []

    for sec in sections:
        first_line = sec.splitlines()[0] if sec.splitlines() else ""
        if "（" in first_line and "/）" in first_line and "guide/" not in first_line:
            # This is a topic table to update
            lines = sec.splitlines()
            new_lines = []
            for line in lines:
                if line.startswith("| 文档 | 内容 |"):
                    new_lines.append("| 文档 / Document | Ngôn ngữ / Language | 内容 / Summary |")
                elif line.startswith("| --- | --- |"):
                    new_lines.append("| --- | --- | --- |")
                elif line.startswith("|") and not line.startswith("| 目录"):
                    # Table row: | [Title](folder/file.md) | Desc |
                    # Check for multi-doc rows
                    doc_links = re.findall(r"\[([^\]]+)\]\(([^)]+\.md)\)", line)
                    if len(doc_links) == 1:
                        title, link = doc_links[0]
                        parts = line.strip().split("|")
                        # parts = ['', ' [Title](link) ', ' Desc ', '']
                        desc = parts[2].strip() if len(parts) > 2 else ""
                        stem_path = Path(link)
                        stem = stem_path.stem
                        folder = stem_path.parent.as_posix()
                        vi_link = f"{folder}/{stem}.vi.md"
                        en_link = f"{folder}/{stem}.en.md"
                        lang_cell = f"[Tiếng Việt]({vi_link}) · [English]({en_link})"
                        new_lines.append(f"| [{title}]({link}) | {lang_cell} | {desc} |")
                    elif len(doc_links) == 2:
                        # Split into two rows
                        (t1, l1), (t2, l2) = doc_links
                        parts = line.strip().split("|")
                        desc = parts[2].strip() if len(parts) > 2 else ""
                        stem1 = Path(l1).stem
                        folder1 = Path(l1).parent.as_posix()
                        vi1 = f"{folder1}/{stem1}.vi.md"
                        en1 = f"{folder1}/{stem1}.en.md"

                        stem2 = Path(l2).stem
                        folder2 = Path(l2).parent.as_posix()
                        vi2 = f"{folder2}/{stem2}.vi.md"
                        en2 = f"{folder2}/{stem2}.en.md"

                        new_lines.append(f"| [{t1}]({l1}) | [Tiếng Việt]({vi1}) · [English]({en1}) | {desc} |")
                        new_lines.append(f"| [{t2}]({l2}) | [Tiếng Việt]({vi2}) · [English]({en2}) | {t2}相关实验与记录 |")
                    else:
                        new_lines.append(line)
                else:
                    new_lines.append(line)
            new_sections.append("\n".join(new_lines))
        else:
            new_sections.append(sec)

    updated_content = "\n".join(new_sections)
    README_PATH.write_text(updated_content, encoding="utf-8")
    print("docs/README.md updated with 3-column multilingual tables!")


if __name__ == "__main__":
    update_docs_index()

