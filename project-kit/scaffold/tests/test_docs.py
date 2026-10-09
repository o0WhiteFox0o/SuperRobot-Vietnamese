"""Kiểm tra tài liệu: link tương đối phải tồn tại, đường dẫn repo trong backtick phải tồn tại,
mọi tài liệu trong docs/<chủ đề>/ phải được liệt kê trong docs/README.md.

Tổng quát hoá từ tests/test_docs.py của SuperRobot. Chỉnh các hằng số ở đầu tệp cho dự án của bạn.
"""
from __future__ import annotations

from pathlib import Path
import os
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]

# Thư mục mẫu chứa placeholder {{...}}: không kiểm, không cần liệt kê.
TEMPLATE_DIR = ROOT / "docs" / "templates"
# Tài liệu chỉ có trên máy người bảo trì (đã .gitignore): không kiểm, không liệt kê.
LOCAL_ONLY: set[Path] = set()
# Tiền tố thư mục cấp cao mà đường dẫn trong backtick phải tồn tại.
TOP_DIRS = ("src", "tools", "tests", "config", "content", "scripts", "docs", "reference")
# Đường dẫn cố ý trỏ ra ngoài repo hoặc chưa viết.
ELSEWHERE: set[str] = set()


def _is_template(path: Path) -> bool:
    return TEMPLATE_DIR in path.parents or path == TEMPLATE_DIR


MARKDOWN = sorted(
    p for p in {*ROOT.glob("*.md"), *(ROOT / "docs").rglob("*.md")}
    if p not in LOCAL_ONLY and not _is_template(p)
)
LINK = re.compile(r"\]\(([^)\s#]+)(?:#[^)\s]*)?\)")
CODE = re.compile(r"```.*?```|`[^`\n]+`", re.S)  # link ví dụ trong code không bị kiểm
REPO_PATH = re.compile(r"`((?:" + "|".join(TOP_DIRS) + r")/[^`\s*<>{}|]+)`")


def local_evidence(path: Path) -> bool:
    """build/ và assets/ là bằng chứng cục bộ, không có trong repo."""
    return path.is_relative_to(ROOT / "build") or (
        path.is_relative_to(ROOT / "assets") and path.name != "README.md"
    )


class DocsTests(unittest.TestCase):
    def test_relative_links_resolve(self):
        broken = []
        for doc in MARKDOWN:
            for target in LINK.findall(CODE.sub("", doc.read_text(encoding="utf-8"))):
                if re.match(r"[a-z]+:", target):
                    continue
                path = Path(os.path.normpath(doc.parent / target))
                if not local_evidence(path) and not path.exists():
                    broken.append(f"{doc.relative_to(ROOT)} -> {target}")
        self.assertEqual(broken, [])

    def test_named_repository_paths_exist(self):
        missing = []
        for doc in MARKDOWN:
            for name in REPO_PATH.findall(doc.read_text(encoding="utf-8")):
                name = name.rstrip("/.,:;").split(":")[0]
                if name in ELSEWHERE or (ROOT / name).exists() or any(ROOT.glob(name)):
                    continue
                missing.append(f"{doc.relative_to(ROOT)}: {name}")
        self.assertEqual(missing, [])

    def test_docs_live_in_topic_folders(self):
        loose = [p.name for p in (ROOT / "docs").glob("*.md") if p.name != "README.md"]
        self.assertEqual(loose, [], "đặt tài liệu mới vào thư mục chủ đề và liệt kê trong docs/README.md")
        index = (ROOT / "docs/README.md").read_text(encoding="utf-8")
        unlisted = [
            p.relative_to(ROOT / "docs").as_posix()
            for p in (ROOT / "docs").glob("*/*.md")
            if p not in LOCAL_ONLY and not _is_template(p)
            and f"({p.relative_to(ROOT / 'docs').as_posix()})" not in index
        ]
        self.assertEqual(unlisted, [])


if __name__ == "__main__":
    unittest.main()
