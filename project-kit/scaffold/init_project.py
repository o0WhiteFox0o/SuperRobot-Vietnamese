#!/usr/bin/env python3
"""Tạo khung dự án mới từ project-kit.

    python project-kit/scaffold/init_project.py D:\\Projects\\MyApp --name "My App"

Tạo: thư mục chuẩn, docs/ với 6 chủ đề + docs/README.md (chỉ mục), docs/templates/ (bản sao mẫu),
docs/guide/ (nguyên tắc & quy trình của kit), tests/test_docs.py, README.md, CONTRIBUTING.md, .gitignore.
Không ghi đè tệp đã tồn tại (trừ khi --force).
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from datetime import date
from pathlib import Path

KIT = Path(__file__).resolve().parents[1]
TOPICS = ["guide", "design", "analysis", "features", "quality", "decisions"]
SRC_DIRS = ["src", "tools/toolchain", "tools/run", "tools/verify", "tools/analysis", "tools/debug",
            "tests", "config", "content", "reference", "scripts"]
GITIGNORE = "build/\nassets/*\n!assets/README.md\ndist/\n.venv/\n__pycache__/\n*.pyc\n"


def write(path: Path, text: str, force: bool) -> None:
    if path.exists() and not force:
        print(f"  giữ nguyên {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    print(f"  tạo {path}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target", type=Path, help="Thư mục dự án mới")
    ap.add_argument("--name", required=True, help="Tên dự án")
    ap.add_argument("--force", action="store_true", help="Ghi đè tệp đã có")
    args = ap.parse_args()

    target: Path = args.target.resolve()
    today = date.today().isoformat()
    target.mkdir(parents=True, exist_ok=True)
    print(f"Khởi tạo '{args.name}' tại {target}")

    for rel in SRC_DIRS:
        d = target / rel
        d.mkdir(parents=True, exist_ok=True)
        keep = d / ".gitkeep"
        if not any(d.iterdir()):
            keep.write_text("", encoding="utf-8")
    for topic in TOPICS:
        (target / "docs" / topic).mkdir(parents=True, exist_ok=True)

    # Mẫu + hướng dẫn của kit (bản sao để chép khi viết tài liệu mới).
    for src in sorted((KIT / "templates").glob("*.md")):
        write(target / "docs" / "templates" / src.name, src.read_text(encoding="utf-8"), args.force)
    def mark_foreign(text: str) -> str:
        """Đường dẫn ví dụ lấy từ SuperRobot không tồn tại trong dự án mới -> gắn nhãn nguồn."""
        def repl(m: re.Match) -> str:
            name = m.group(1).rstrip("/.,:;")
            if name in {"tests/test_docs.py", "docs/README.md"} or (target / name).exists() or any(target.glob(name)):
                return m.group(0)
            return f"`SuperRobot: {m.group(1)}`"
        return re.sub(r"`((?:src|tools|tests|config|content|scripts|docs|reference)/[^`\s*<>{}|]+)`", repl, text)

    for src in sorted((KIT / "guide").glob("*.md")):
        dst = target / "docs" / "guide" / src.name
        text = src.read_text(encoding="utf-8").replace("../scaffold/tests/test_docs.py", "../../tests/test_docs.py")
        write(dst, text, args.force)
    for dst in sorted((target / "docs" / "guide").glob("0*.md")):
        dst.write_text(mark_foreign(dst.read_text(encoding="utf-8")), encoding="utf-8", newline="\n")

    kit_rows = "\n".join(
        f"| [Kit: {p.stem}](guide/{p.name}) | Quy trình và nguyên tắc của project-kit |"
        for p in sorted((target / "docs" / "guide").glob("0*.md"))
    )
    index = (KIT / "templates" / "docs-index.md").read_text(encoding="utf-8")
    index = index.replace("{{YYYY-MM-DD}}", today)
    index = index.replace(
        "| Tài liệu | Nội dung |\n| --- | --- |\n| [{{…}}](guide/{{…}}.md) | |",
        "| Tài liệu | Nội dung |\n| --- | --- |\n" + kit_rows,
        1,
    )
    # Bỏ các hàng placeholder còn lại để test_docs không bắt link giả.
    index = "\n".join(
        line for line in index.splitlines()
        if "{{…}}" not in line and "{{sổ lỗi}}" not in line and "{{lộ trình}}" not in line and "{{sửa}}" not in line
    ) + "\n"
    write(target / "docs" / "README.md", index, args.force)

    write(target / "tests" / "test_docs.py", (KIT / "scaffold" / "tests" / "test_docs.py").read_text(encoding="utf-8"), args.force)
    write(target / "README.md", f"# {args.name}\n\nNgày: {today}. Trạng thái: **Ý tưởng**.\n\nMô tả một đoạn: dự án là gì, **không phải là gì**.\n\n- Tài liệu: [docs/README.md](docs/README.md)\n- Quy trình: bắt đầu từ [docs/guide/06-new-project-checklist.md](docs/guide/06-new-project-checklist.md)\n", args.force)
    write(target / "CONTRIBUTING.md", f"# Đóng góp cho {args.name}\n\n1. Dùng mẫu trong `docs/templates/` cho tài liệu mới.\n2. Mọi tài liệu phải được liệt kê trong [docs/README.md](docs/README.md).\n3. Chạy `python -m unittest discover tests` trước khi commit.\n4. Mỗi kết luận cần bằng chứng; phần chưa kiểm chứng ghi vào mục \"Chưa xác minh\".\n", args.force)
    write(target / ".gitignore", GITIGNORE, args.force)
    write(target / "assets" / "README.md", "# assets/\n\nSản phẩm sinh ra lớn, không commit. Ghi cách tạo lại ở đây.\n", args.force)

    print("\nXong. Chạy: python -m unittest discover tests")
    return 0


if __name__ == "__main__":
    sys.exit(main())
