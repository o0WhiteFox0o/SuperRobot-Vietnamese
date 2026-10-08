#!/usr/bin/env python3
"""Enrich assets/original-graphics/index.html with full Vietnamese and English annotations.

Translates:
- Interface headings, descriptions, notices, and guides
- Unit names and IDs
- Weapon names and animation details
- Pilot names and portrait labels
- Battle cut-in attack names
- Map movie combination/transformation titles and trigger descriptions
- Chapter and stage titles
- Search filter & language switch controls (Tiếng Việt / English / Song ngữ / Tiếng Nhật)
"""
from __future__ import annotations

import html
import json
import os
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from srw64_native.catalog import source_catalog

ORIGINAL_HTML = ROOT / "assets/original-graphics/index.html"
ROM_PATH = ROOT / "rom.z64"
TERMS_VI_PATH = ROOT / "content/locales/terms/vi.json"
TERMS_EN_PATH = ROOT / "content/locales/terms/en.json"

MOVIE_TRANS = {
    0: {
        "title_en": "Combattler V Combination",
        "title_vi": "Hợp thể Combattler V",
        "desc_en": "Triggered by script 3D67 0 (Unit 196 combine)",
        "desc_vi": "Kịch bản 3D67 0 (Hợp thể đơn vị 196 Combattler V)",
    },
    1: {
        "title_en": "Aura Road · Zwarth",
        "title_vi": "Con đường Aura · Zwarth",
        "desc_en": "Triggered by script 3D67 1 (Aura Battler Zwarth)",
        "desc_vi": "Kịch bản 3D67 1 (Aura Battler Zwarth)",
    },
    2: {
        "title_en": "Aura Road (Unused in Story)",
        "title_vi": "Con đường Aura (Chưa gán kịch bản)",
        "desc_en": "Unused map movie in retail game script",
        "desc_vi": "Hoạt ảnh dự phòng trong dữ liệu ROM",
    },
    3: {
        "title_en": "Aura Road · Todd",
        "title_vi": "Con đường Aura · Todd",
        "desc_en": "Triggered by script 3D67 3 (Todd Guinness)",
        "desc_vi": "Kịch bản 3D67 3 (Todd Guinness)",
    },
    4: {
        "title_en": "Aura Road · Jeril",
        "title_vi": "Con đường Aura · Jeril",
        "desc_en": "Triggered by script 3D67 4 (Jeril Cozubey)",
        "desc_vi": "Kịch bản 3D67 4 (Jeril Cozubey)",
    },
    5: {
        "title_en": "Change · Getter Dragon",
        "title_vi": "Biến hình · Getter Dragon",
        "desc_en": "Unit 174 first form transformation",
        "desc_vi": "Biến hình dạng đầu của đơn vị 174",
    },
    6: {
        "title_en": "Change · Getter Liger",
        "title_vi": "Biến hình · Getter Liger",
        "desc_en": "Unit 176 first form transformation",
        "desc_vi": "Biến hình dạng đầu của đơn vị 176",
    },
    7: {
        "title_en": "Change · Getter Poseidon",
        "title_vi": "Biến hình · Getter Poseidon",
        "desc_en": "Unit 175 first form transformation",
        "desc_vi": "Biến hình dạng đầu của đơn vị 175",
    },
    8: {
        "title_en": "Change · Getter 1",
        "title_vi": "Biến hình · Getter 1",
        "desc_en": "Unit 171 first form transformation",
        "desc_vi": "Biến hình dạng đầu của đơn vị 171",
    },
    9: {
        "title_en": "Change · Getter 2",
        "title_vi": "Biến hình · Getter 2",
        "desc_en": "Unit 172 first form transformation",
        "desc_vi": "Biến hình dạng đầu của đơn vị 172",
    },
    10: {
        "title_en": "Change · Getter 3",
        "title_vi": "Biến hình · Getter 3",
        "desc_en": "Unit 173 first form transformation",
        "desc_vi": "Biến hình dạng đầu của đơn vị 173",
    },
    11: {
        "title_en": "Godmars Combination",
        "title_vi": "Hợp thể Godmars",
        "desc_en": "Triggered by script 3D6A (6 God Robots combine)",
        "desc_vi": "Kịch bản 3D6A (6 Thần robot hợp thể)",
    },
}

CUTIN_TRANS = {
    "0018-爆熱ゴッドフィンガー": {
        "en": "Bakunetsu God Finger",
        "vi": "Hỏa Long God Finger (Bộc Nhiệt God Finger)",
    },
    "0019-石破天驚拳": {
        "en": "Sekiha Tenkyoken",
        "vi": "Thạch Phá Thiên Kinh Quyền",
    },
    "0024-シャイニングフィンガー": {
        "en": "Shining Finger",
        "vi": "Shining Finger (Bàn tay Tỏa sáng)",
    },
    "0029-シャイニングフィンガー": {
        "en": "Shining Finger",
        "vi": "Shining Finger (Bàn tay Tỏa sáng)",
    },
    "0742-ファイナルゴッドマーズ": {
        "en": "Final Godmars",
        "vi": "Final Godmars (Đòn kết liễu Godmars)",
    },
    "0778-超電磁スピン": {
        "en": "Choudenji Spin",
        "vi": "Xoáy Siêu Điện Từ (Choudenji Spin)",
    },
    "0820-ロケットバズーカ": {
        "en": "Rocket Bazooka",
        "vi": "Rocket Bazooka",
    },
    "0821-ロケットミサイル": {
        "en": "Rocket Missile",
        "vi": "Tên lửa Rocket",
    },
    "0874-断空光牙剣": {
        "en": "Dankuu Kougaken",
        "vi": "Đoạn Không Quang Nha Kiếm",
    },
    "0881-断空光牙剣": {
        "en": "Dankuu Kougaken",
        "vi": "Đoạn Không Quang Nha Kiếm",
    },
    "1062-V-MAX": {
        "en": "V-MAX",
        "vi": "V-MAX",
    },
    "1075-V-MAX": {
        "en": "V-MAX",
        "vi": "V-MAX",
    },
    "1216-石破ラブラブ天驚拳": {
        "en": "Sekiha Love-Love Tenkyoken",
        "vi": "Thạch Phá Love-Love Thiên Kinh Quyền",
    },
    "1217-シャッフル同盟拳": {
        "en": "Shuffle Alliance Fist",
        "vi": "Quyền Liên Minh Shuffle",
    },
    "unreferenced": {
        "en": "Unreferenced Cut-ins",
        "vi": "Chiêu thức không gán trực tiếp",
    },
}

EXTRA_UNITS = {
    "F91": "Gundam F91",
}


def load_terms():
    vi = json.loads(TERMS_VI_PATH.read_text(encoding="utf-8"))["sections"]
    en = json.loads(TERMS_EN_PATH.read_text(encoding="utf-8"))["sections"]
    return vi, en


def get_stage_translations():
    stages_map = {}
    if ROM_PATH.exists():
        sources, _, _ = source_catalog(ROOT, ROM_PATH)
        vi_stages = json.loads(TERMS_VI_PATH.read_text(encoding="utf-8"))["sections"].get("stages", {})
        en_stages = json.loads(TERMS_EN_PATH.read_text(encoding="utf-8"))["sections"].get("stages", {})
        for i in range(133):
            raw = sources.get(f"base:t00_{281 + i:05d}")
            if raw:
                jp = raw.replace("<END>", "").replace("<BR>", " ").strip()
                en_name = en_stages.get(jp, jp)
                vi_name = vi_stages.get(jp, en_name)
                stages_map[i] = {"jp": jp, "en": en_name, "vi": vi_name}
    return stages_map


def build_enhanced_html():
    vi, en = load_terms()
    stage_map = get_stage_translations()

    unit_vi = vi.get("units", {})
    unit_en = en.get("units", {})
    weapon_vi = vi.get("weapons", {})
    weapon_en = en.get("weapons", {})
    pilot_vi = vi.get("pilots", {})
    pilot_en = en.get("pilots", {})
    pilot_full_vi = vi.get("pilot_full_names", {})
    pilot_full_en = en.get("pilot_full_names", {})

    content = ORIGINAL_HTML.read_text(encoding="utf-8")

    # 1. Update Unit cards
    def unit_replacer(match):
        full_card = match.group(0)
        uid_str = match.group(1)
        name_jp = match.group(2)
        uid = int(uid_str)

        trans_en = unit_en.get(name_jp) or EXTRA_UNITS.get(name_jp) or name_jp
        trans_vi = unit_vi.get(name_jp) or EXTRA_UNITS.get(name_jp) or trans_en

        # Translate header
        head_old = f'<div class="head"><img loading="lazy" src="{match.group(3)}" title="" class="icon"><b>{uid_str}</b> {name_jp}</div>'
        head_new = (
            f'<div class="head"><img loading="lazy" src="{match.group(3)}" title="{html.escape(trans_en)}" class="icon">'
            f'<div><div class="name-jp"><b>{uid_str}</b> {html.escape(name_jp)}</div>'
            f'<div class="name-trans" data-en="{html.escape(trans_en)}" data-vi="{html.escape(trans_vi)}">{html.escape(trans_vi)}</div></div></div>'
        )

        card = full_card.replace(head_old, head_new)

        # Translate note for shared sheet: 共用图集：309 -> Dùng chung atlas với / Shared atlas: 309
        card = re.sub(
            r'<div class="note">共用图集：([^<]+)</div>',
            r'<div class="note-shared" title="Dùng chung texture atlas với robot khác / Shared sheet with other mechs">🔗 Atlas: \1</div>',
            card
        )

        # Translate links line: sheet · unit.json · 武器 5 -> sheet · unit.json · 5 Vũ khí / Weapons
        card = re.sub(
            r'· 武器 (\d+)',
            r'· <span class="badge-weapon">\1 vũ khí (weapons)</span>',
            card
        )

        # Translate details summary
        card = card.replace(
            '<summary>武器动画零件</summary>',
            '<summary>⚡ Hoạt ảnh vũ khí / Weapon Animations</summary>'
        )

        return card

    # Regex for unit cards
    unit_pattern = re.compile(
        r'<div class="card unit" id="unit-\d+"><div class="head"><img loading="lazy" src="([^"]+)" title="" class="icon"><b>(\d+)</b> ([^<]+)</div>',
        re.DOTALL
    )

    def unit_card_transform(match):
        img_src = match.group(1)
        uid_str = match.group(2)
        name_jp = match.group(3)
        trans_en = unit_en.get(name_jp) or EXTRA_UNITS.get(name_jp) or name_jp
        trans_vi = unit_vi.get(name_jp) or EXTRA_UNITS.get(name_jp) or trans_en
        return (
            f'<div class="card unit" id="unit-{int(uid_str)}" data-search="{html.escape(name_jp.lower())} {html.escape(trans_en.lower())} {html.escape(trans_vi.lower())} {uid_str}">'
            f'<div class="head"><img loading="lazy" src="{img_src}" title="{html.escape(trans_en)}" class="icon">'
            f'<div><div class="name-jp"><b>{uid_str}</b> {html.escape(name_jp)}</div>'
            f'<div class="name-trans" data-en="{html.escape(trans_en)}" data-vi="{html.escape(trans_vi)}">{html.escape(trans_vi)}</div>'
            f'</div></div>'
        )

    content = unit_pattern.sub(unit_card_transform, content)

    # Clean up unit note and summary tags
    content = re.sub(
        r'<div class="note">共用图集：([^<]+)</div>',
        r'<div class="note-shared" title="Dùng chung texture atlas / Shared atlas">🔗 Atlas chung: \1</div>',
        content
    )
    content = re.sub(
        r'· 武器 (\d+)',
        r'· <span class="badge-weapon">⚔️ \1 vũ khí</span>',
        content
    )
    content = content.replace(
        '<summary>武器动画零件</summary>',
        '<summary class="weapon-summary">⚡ Danh sách vũ khí & Hoạt ảnh (Weapons & Effects)</summary>'
    )

    # 2. Translate weapon rows inside unit details
    def weapon_replacer(match):
        wid = match.group(1)
        wname_jp = match.group(2)
        wen = weapon_en.get(wname_jp, wname_jp)
        wvi = weapon_vi.get(wname_jp, wen)
        label = f'<b>{wid}</b> {html.escape(wname_jp)}'
        if wvi != wname_jp:
            label += f' <span class="trans-sub" data-en="{html.escape(wen)}" data-vi="{html.escape(wvi)}">({html.escape(wvi)})</span>'
        return f'<div class="weapon"><span>{label}</span>'

    content = re.sub(r'<div class="weapon"><span>(\d+) ([^<]+)</span>', weapon_replacer, content)

    # 3. Translate Cut-ins
    def cutin_replacer(match):
        group_path = match.group(1)
        info = CUTIN_TRANS.get(group_path, {})
        en_t = info.get("en", group_path)
        vi_t = info.get("vi", en_t)
        return (
            f'<div class="group"><h3>⚡ {html.escape(group_path)} '
            f'<span class="group-trans" data-en="{html.escape(en_t)}" data-vi="{html.escape(vi_t)}">[{html.escape(vi_t)}]</span></h3>'
        )

    content = re.sub(r'<div class="group"><h3>([^<]+)</h3>', cutin_replacer, content)

    # 4. Translate Portraits
    def portrait_replacer(match):
        src = match.group(1)
        full_jp = match.group(2)
        idx_str = match.group(3)
        short_jp = match.group(4)

        full_trans_en = pilot_full_en.get(full_jp) or pilot_en.get(full_jp) or full_jp
        full_trans_vi = pilot_full_vi.get(full_jp) or pilot_vi.get(full_jp) or full_trans_en

        short_trans_en = pilot_en.get(short_jp) or full_trans_en
        short_trans_vi = pilot_vi.get(short_jp) or full_trans_vi

        tip = f"{full_jp} / {full_trans_en}" if full_jp != short_jp else full_trans_en

        return (
            f'<div class="card small portrait-card" data-search="{html.escape(short_jp.lower())} {html.escape(full_jp.lower())} {html.escape(full_trans_en.lower())} {idx_str}">'
            f'<img loading="lazy" src="{src}" title="{html.escape(tip)}">'
            f'<div class="pilot-info"><div class="name-jp"><b>{idx_str}</b> {html.escape(short_jp)}</div>'
            f'<div class="name-trans" data-en="{html.escape(short_trans_en)}" data-vi="{html.escape(short_trans_vi)}">{html.escape(short_trans_vi)}</div>'
            f'</div></div>'
        )

    content = re.sub(
        r'<div class="card small"><img loading="lazy" src="([^"]+)" title="([^"]*)"[^>]*><div>(\d+) ([^<]+)</div></div>',
        portrait_replacer,
        content
    )

    # 5. Translate Movies
    def movie_replacer(match):
        mid_str = match.group(1)
        title_jp = match.group(2)
        trigger_jp = match.group(3)
        mid = int(mid_str)
        t_info = MOVIE_TRANS.get(mid, {})
        m_en = t_info.get("title_en", title_jp)
        m_vi = t_info.get("title_vi", m_en)
        d_en = t_info.get("desc_en", trigger_jp)
        d_vi = t_info.get("desc_vi", d_en)

        return (
            f'<div class="group movie-group">'
            f'<h3>🎬 #{mid_str} {html.escape(title_jp)} '
            f'<span class="movie-title-trans" data-en="{html.escape(m_en)}" data-vi="{html.escape(m_vi)}">({html.escape(m_vi)})</span> '
            f'<span class="note movie-desc-trans" data-en="{html.escape(d_en)}" data-vi="{html.escape(d_vi)}">💡 {html.escape(d_vi)}</span></h3>'
        )

    content = re.sub(
        r'<div class="group"><h3>#(\d+) ([^<]+) <span class="note">([^<]+)</span></h3>',
        movie_replacer,
        content
    )

    # 6. Translate Chapter Titles
    def chapter_replacer(match):
        path = match.group(1)
        idx_str = match.group(2)
        scene_str = match.group(3)
        idx = int(idx_str)

        info = stage_map.get(idx, {})
        s_jp = info.get("jp", "")
        s_en = info.get("en", "")
        s_vi = info.get("vi", s_en)

        label_trans = f'<div class="stage-title" data-en="{html.escape(s_en)}" data-vi="{html.escape(s_vi)}">{html.escape(s_vi)}</div>' if s_vi else ""
        jp_sub = f'<div class="stage-jp">{html.escape(s_jp)}</div>' if s_jp else ""

        return (
            f'<div class="card stage-card" data-search="{idx_str} {html.escape(s_jp.lower())} {html.escape(s_en.lower())} {html.escape(s_vi.lower())}">'
            f'<a href="{path}"><img loading="lazy" src="{path}" title="#{idx_str}: {html.escape(s_en)}" class="movie"></a>'
            f'<div class="stage-meta"><b>#{idx_str}</b> · scene {scene_str}</div>'
            f'{jp_sub}{label_trans}</div>'
        )

    content = re.sub(
        r'<div class="card"><a href="([^"]+)"><img loading="lazy" src="[^"]*" title="" class="movie"></a><div>#(\d+) · scene (\d+)</div></div>',
        chapter_replacer,
        content
    )

    # 7. Update Navigation and Header
    new_nav = """
<nav id="top-nav">
  <div class="nav-links">
    <a href="#units" class="nav-item">🤖 Cơ thể / Units <span class="count">(363)</span></a>
    <a href="#cutins" class="nav-item">⚡ Chiêu thức / Cut-ins <span class="count">(15)</span></a>
    <a href="#portraits" class="nav-item">👤 Phi công / Pilots <span class="count">(361)</span></a>
    <a href="#battle" class="nav-item">💥 Hiệu ứng / Effects <span class="count">(524)</span></a>
    <a href="#movies" class="nav-item">🎬 Hợp thể / Movies <span class="count">(12)</span></a>
    <a href="#chapter-titles" class="nav-item">📜 Màn chơi / Stages <span class="count">(133)</span></a>
    <a href="#maps" class="nav-item">🗺️ Bản đồ / Maps <span class="count">(158)</span></a>
  </div>
  <div class="nav-controls">
    <div class="search-box">
      <input type="text" id="filter-input" placeholder="🔍 Tìm kiếm robot, vũ khí, phi công (Search mechs, weapons...)" autocomplete="off">
      <button id="clear-search" title="Xóa tìm kiếm">✕</button>
    </div>
    <div class="lang-switcher">
      <button class="lang-btn active" data-lang="vi" title="Hiển thị tiếng Việt">🇻🇳 Tiếng Việt</button>
      <button class="lang-btn" data-lang="bilingual" title="Song ngữ Tiếng Việt & Tiếng Anh">🇻🇳/🇬🇧 Song ngữ</button>
      <button class="lang-btn" data-lang="en" title="Show English">🇬🇧 English</button>
      <button class="lang-btn" data-lang="jp" title="Nguyên bản tiếng Nhật">🇯🇵 Tiếng Nhật</button>
    </div>
  </div>
</nav>
"""

    header_block = """
<header class="gallery-header">
  <div class="header-main">
    <h1>SRW64 Original Graphics Gallery</h1>
    <h2>Kho Lưu Trữ & Tra Cứu Hình Ảnh Gốc Super Robot Wars 64 (N64)</h2>
    <div class="stats-pills">
      <span class="pill">🤖 363 Robot (Units)</span>
      <span class="pill">⚔️ 580 Vũ khí (Weapons)</span>
      <span class="pill">👤 361 Phi công (Pilots)</span>
      <span class="pill">⚡ 15 Cảnh cắt (Cut-ins)</span>
      <span class="pill">🎬 12 Hoạt ảnh hợp thể</span>
      <span class="pill">📜 133 Màn chơi (Stages)</span>
      <span class="pill">🗺️ 158 Bản đồ (Maps)</span>
    </div>
  </div>

  <div class="guide-box">
    <div class="guide-col vi-guide">
      <h3>📖 Hướng dẫn & Ghi chú kỹ thuật (Tiếng Việt):</h3>
      <ul>
        <li><b>Nguồn tài nguyên</b>: Trích xuất trực tiếp từ ROM gốc <i>Super Robot Taisen 64</i> (Japan, Rev 0) bởi công cụ <code>tools/content/export_graphics.py</code>. Cấu trúc liên kết theo bảng ROM cố định tại <code>manifest.json</code>.</li>
        <li><b>Ảnh thu nhỏ (Thumbnails)</b>: Hiển thị dải toàn bộ khung hình ngang (Frame Strip) của hoạt ảnh trong một dải băng.</li>
        <li><b>Xem ảnh động APNG</b>: Nhấp chuột trực tiếp vào bất kỳ hình nào để mở ảnh động APNG chuẩn chu kỳ bước sprite (~33ms/nhịp theo sprite tick của engine N64).</li>
        <li><b>Liên kết <code>sheet</code></b>: Tải bảng texture atlas gốc được nạp trực tiếp vào VRAM.</li>
        <li><b>Liên kết <code>unit.json</code></b>: Xem toàn bộ dữ liệu chỉ số chiến đấu, liên kết vũ khí và animation binding trích xuất từ ROM.</li>
      </ul>
    </div>
    <div class="guide-col en-guide">
      <h3>Technical Guide & Notes (English):</h3>
      <ul>
        <li><b>Source Data</b>: Extracted directly from original ROM <i>Super Robot Taisen 64</i> (Japan, Rev 0) via <code>tools/content/export_graphics.py</code>. Structure mapped from fixed ROM tables in <code>manifest.json</code>.</li>
        <li><b>Thumbnails</b>: Displays the horizontal frame strip of distinct animation frames.</li>
        <li><b>Animated APNG</b>: Click on any image to open full APNG animation rendered according to the engine step list (~33ms per tick preview).</li>
        <li><b><code>sheet</code> Link</b>: Raw texture atlas decoded directly into VRAM layout.</li>
        <li><b><code>unit.json</code> Link</b>: Complete machine statistics, weapon assignments, and animation binding metadata.</li>
      </ul>
    </div>
  </div>
</header>
"""

    # Replace Header & Nav in original HTML
    content = re.sub(r'<h1>SRW64 原版图像导出</h1>.*?<nav>.*?</nav>', header_block + new_nav, content, flags=re.DOTALL)

    # Replace Section headers
    section_headers = {
        r'<section id="units"><h2>机体 \(363\)</h2>': '<section id="units"><div class="section-title"><h2>🤖 Robot & Cơ thể Chiến Đấu (Units & Mechs - 363)</h2><span class="badge-count">363 Mechs</span></div>',
        r'<section id="cutins"><h2>战斗 cut-in \(15 组\)</h2>': '<section id="cutins"><div class="section-title"><h2>⚡ Cảnh Cắt Chiêu Thức Đặc Biệt (Battle Cut-ins - 15 nhóm)</h2><span class="badge-count">15 Sets</span></div>',
        r'<section id="portraits"><h2>人物头像 \(361\)</h2>': '<section id="portraits"><div class="section-title"><h2>👤 Chân Dung Phi Công & Nhân Vật (Character Portraits - 361)</h2><span class="badge-count">361 Pilots</span></div>',
        r'<section id="battle"><h2>战斗特效与其他战斗图集 \(524\)</h2>': '<section id="battle"><div class="section-title"><h2>💥 Hiệu Ứng Chiến Đấu & Tập Ảnh (Battle Effects & Atlases - 524)</h2><span class="badge-count">524 Atlases</span></div>',
        r'<section id="movies"><h2>地图合体／变形动画 \(12\)</h2>': '<section id="movies"><div class="section-title"><h2>🎬 Hoạt Ảnh Hợp Thể & Biến Hình Trên Bản Đồ (Map Movies - 12)</h2><span class="badge-count">12 Animations</span></div>',
        r'<section id="chapter-titles"><h2>章节标题 \(133\)</h2>': '<section id="chapter-titles"><div class="section-title"><h2>📜 Tiêu Đề Màn Chơi & Kịch Bản (Chapter & Stage Titles - 133)</h2><span class="badge-count">133 Stages</span></div>',
        r'<section id="maps"><h2>战场底图 \(158\)</h2>': '<section id="maps"><div class="section-title"><h2>🗺️ Bản Đồ Địa Hình Chiến Trường (Battlefield Maps - 158)</h2><span class="badge-count">158 Maps</span></div>',
    }

    for pattern, repl in section_headers.items():
        content = re.sub(pattern, repl, content)

    # Enrich Styles & Scripts
    enhanced_styles = """
<style>
:root{
  --bg:#f3f4f8;--card:#ffffff;--ink:#1a1c23;--muted:#5c6170;--line:#d8dce6;
  --accent:#2563eb;--accent-light:#dbeafe;--badge:#e0e7ff;--badge-text:#3730a3;
  --card-hover:#f8faff;--green:#059669;--green-bg:#d1fae5;
}
@media (prefers-color-scheme: dark){
  :root{
    --bg:#0f1117;--card:#1a1d26;--ink:#e4e7ee;--muted:#8b92a5;--line:#2c3240;
    --accent:#3b82f6;--accent-light:#1e293b;--badge:#232b42;--badge-text:#93c5fd;
    --card-hover:#202533;--green:#10b981;--green-bg:#064e3b;
  }
}
body{margin:0;padding:0 20px 80px;background:var(--bg);color:var(--ink);font:14px -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;line-height:1.5}
a{color:var(--accent);text-decoration:none} a:hover{text-decoration:underline}

/* Header */
.gallery-header{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:24px;margin:20px 0;box-shadow:0 4px 12px #0000000d}
.header-main h1{margin:0 0 6px;font-size:26px;color:var(--accent)}
.header-main h2{margin:0 0 16px;font-size:16px;color:var(--muted);font-weight:normal}
.stats-pills{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:18px}
.pill{background:var(--badge);color:var(--badge-text);font-size:12px;font-weight:600;padding:4px 10px;border-radius:20px}

/* Guides */
.guide-box{display:grid;grid-template-columns:1fr 1fr;gap:20px;background:var(--bg);padding:16px;border-radius:8px;border:1px solid var(--line)}
@media (max-width:850px){.guide-box{grid-template-columns:1fr}}
.guide-col h3{margin:0 0 8px;font-size:14px;color:var(--accent)}
.guide-col ul{margin:0;padding-left:18px;font-size:13px;color:var(--muted)}
.guide-col li{margin-bottom:6px}

/* Sticky Nav */
nav#top-nav{position:sticky;top:0;background:var(--card);padding:10px 16px;border:1px solid var(--line);border-radius:10px;z-index:100;box-shadow:0 4px 16px #00000014;margin-bottom:24px}
.nav-links{display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin-bottom:10px}
.nav-item{font-weight:600;color:var(--ink);padding:4px 8px;border-radius:6px;transition:background .2s}
.nav-item:hover{background:var(--accent-light);color:var(--accent);text-decoration:none}
.nav-item .count{font-weight:normal;color:var(--muted);font-size:12px}

.nav-controls{display:flex;flex-wrap:wrap;gap:14px;justify-content:space-between;align-items:center}
.search-box{display:flex;align-items:center;background:var(--bg);border:1px solid var(--line);border-radius:8px;padding:4px 10px;flex:1;max-width:480px}
.search-box input{border:none;background:transparent;outline:none;color:var(--ink);width:100%;font-size:13px}
.search-box button{background:none;border:none;color:var(--muted);cursor:pointer;font-size:14px}
.lang-switcher{display:flex;gap:6px}
.lang-btn{background:var(--bg);border:1px solid var(--line);color:var(--ink);padding:5px 12px;border-radius:6px;cursor:pointer;font-size:12px;font-weight:500;transition:.2s}
.lang-btn:hover{border-color:var(--accent)}
.lang-btn.active{background:var(--accent);border-color:var(--accent);color:#fff}

/* Sections */
.section-title{display:flex;align-items:center;gap:12px;margin:32px 0 16px;border-bottom:2px solid var(--line);padding-bottom:8px}
.section-title h2{margin:0;font-size:20px}
.badge-count{background:var(--accent-light);color:var(--accent);font-size:12px;padding:2px 8px;border-radius:12px;font-weight:bold}
.grid{display:flex;flex-wrap:wrap;gap:14px}

/* Cards */
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px;width:240px;box-sizing:border-box;transition:transform .15s,box-shadow .15s;position:relative}
.card:hover{transform:translateY(-2px);box-shadow:0 6px 16px #0000001a;border-color:var(--accent)}
.card.unit{width:290px}
.card.small{width:115px;text-align:center;font-size:12px;padding:8px}

.head{display:flex;gap:10px;align-items:center;margin-bottom:8px}
.icon{width:36px;height:36px;image-rendering:pixelated;flex-shrink:0}
.name-jp{font-weight:bold;font-size:14px}
.name-trans{color:var(--accent);font-size:12px;font-weight:600}

.pose{max-width:230px;max-height:170px;image-rendering:pixelated;display:block;margin:10px auto;transition:transform .2s}
.pose:hover{transform:scale(1.05)}
.anim{max-height:96px;max-width:230px;image-rendering:pixelated;margin:3px;background:#0000001a;border-radius:4px}
.movie{max-width:240px;max-height:180px;image-rendering:pixelated;border-radius:6px}
.map{max-width:180px;image-rendering:pixelated;border-radius:6px}

.note-shared{background:var(--badge);color:var(--badge-text);padding:4px 8px;border-radius:6px;font-size:11px;margin:6px 0;font-weight:500}
.badge-weapon{background:var(--green-bg);color:var(--green);font-size:11px;padding:2px 6px;border-radius:6px;font-weight:bold}
.links{color:var(--muted);font-size:12px;margin:8px 0 4px}

details{background:var(--bg);border-radius:6px;padding:6px;margin-top:8px}
summary.weapon-summary{cursor:pointer;font-size:12px;font-weight:600;color:var(--accent);outline:none}
.weapon{margin:8px 0;font-size:12px;border-bottom:1px dashed var(--line);padding-bottom:6px}
.weapon:last-child{border-bottom:none}
.trans-sub{color:var(--accent);font-weight:500}

/* Pilots & Stages */
.portrait-card img{width:64px;height:64px;image-rendering:pixelated;margin:0 auto 6px;display:block}
.pilot-info .name-jp{font-size:12px;margin-bottom:2px}
.pilot-info .name-trans{font-size:11px;color:var(--accent);line-height:1.2}

.stage-card{width:260px}
.stage-meta{font-size:11px;color:var(--muted);margin-top:6px}
.stage-jp{font-weight:bold;font-size:13px;margin:2px 0}
.stage-title{font-size:12px;color:var(--accent);font-weight:600}

.group{width:100%;margin-bottom:20px;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px}
.group h3{font-size:15px;margin:0 0 10px;color:var(--ink)}
.group-trans{color:var(--accent);font-weight:bold}
.movie-title-trans{color:var(--accent);font-weight:bold}
.movie-desc-trans{font-size:12px;color:var(--muted);margin-left:8px}

/* Back to Top */
#back-to-top{position:fixed;bottom:24px;right:24px;background:var(--accent);color:#fff;border:none;border-radius:50%;width:44px;height:44px;font-size:18px;cursor:pointer;box-shadow:0 4px 12px #00000033;display:none;z-index:99;transition:.2s}
#back-to-top:hover{transform:scale(1.1)}

/* Language display modes */
body.lang-vi .name-jp, body.lang-vi .stage-jp { color: var(--muted); font-size: 11px; font-weight: normal; }
body.lang-vi .name-trans, body.lang-vi .stage-title { font-size: 14px; font-weight: bold; color: var(--accent); }
body.lang-vi .en-guide { display: none; }
body.lang-vi .guide-box { grid-template-columns: 1fr; }

body.lang-en .name-jp, body.lang-en .stage-jp { color: var(--muted); font-size: 11px; font-weight: normal; }
body.lang-en .name-trans, body.lang-en .stage-title { font-size: 14px; font-weight: bold; color: var(--accent); }
body.lang-en .vi-guide { display: none; }
body.lang-en .guide-box { grid-template-columns: 1fr; }

body.lang-jp .name-trans, body.lang-jp .stage-title, body.lang-jp .group-trans, body.lang-jp .movie-title-trans, body.lang-jp .trans-sub { display: none; }
body.lang-jp .name-jp, body.lang-jp .stage-jp { font-size: 14px; font-weight: bold; color: var(--ink); }
</style>
"""

    enhanced_scripts = """
<button id="back-to-top" title="Lên đầu trang / Back to Top">↑</button>
<script>
// Search filter
const filterInput = document.getElementById('filter-input');
const clearBtn = document.getElementById('clear-search');
const cards = document.querySelectorAll('.card');

filterInput.addEventListener('input', (e) => {
  const query = e.target.value.toLowerCase().trim();
  clearBtn.style.display = query ? 'block' : 'none';
  if (!query) {
    cards.forEach(c => c.style.display = '');
    return;
  }
  cards.forEach(c => {
    const text = (c.getAttribute('data-search') || c.innerText || '').toLowerCase();
    c.style.display = text.includes(query) ? '' : 'none';
  });
});

clearBtn.addEventListener('click', () => {
  filterInput.value = '';
  filterInput.dispatchEvent(new Event('input'));
  filterInput.focus();
});

// Back to top
const topBtn = document.getElementById('back-to-top');
window.addEventListener('scroll', () => {
  topBtn.style.display = window.scrollY > 400 ? 'block' : 'none';
});
topBtn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));

// Language switch
const langBtns = document.querySelectorAll('.lang-btn');
const setLang = (lang) => {
  document.body.className = 'lang-' + lang;
  langBtns.forEach(b => b.classList.toggle('active', b.dataset.lang === lang));
  
  // Update data-trans targets
  document.querySelectorAll('[data-vi]').forEach(el => {
    if (lang === 'vi') {
      el.textContent = el.dataset.vi;
    } else if (lang === 'en') {
      el.textContent = el.dataset.en;
    } else if (lang === 'bilingual') {
      el.textContent = el.dataset.vi !== el.dataset.en ? `${el.dataset.vi} (${el.dataset.en})` : el.dataset.vi;
    }
  });
  localStorage.setItem('srw64_gallery_lang', lang);
};

langBtns.forEach(btn => {
  btn.addEventListener('click', () => setLang(btn.dataset.lang));
});

// Restore saved language preference
const savedLang = localStorage.getItem('srw64_gallery_lang') || 'vi';
setLang(savedLang);
</script>
"""

    # Inject styles and scripts into HTML
    content = content.replace("<style>", enhanced_styles + "<style>")
    content = content.replace("</body>", enhanced_scripts + "</body>")

    ORIGINAL_HTML.write_text(content, encoding="utf-8")
    print(f"Successfully updated {ORIGINAL_HTML} with Vietnamese & English annotations!")


if __name__ == "__main__":
    build_enhanced_html()

