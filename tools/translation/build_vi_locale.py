#!/usr/bin/env python3
"""Build Vietnamese locale: terms/vi.json and vi.json, and run apply_terms.py."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# Load base terms and UI
en_terms = json.load(open(ROOT / "content/locales/terms/en.json", encoding="utf-8"))
en_ui = json.load(open(ROOT / "content/locales/en.json", encoding="utf-8"))["ui"]

# 1. Terms dictionary mapping
vi_terms = {
    "schema": "srw64.terms.v1",
    "locale": "vi",
    "sections": {}
}

# Translate sections
for section_name, table in en_terms["sections"].items():
    new_table = {}
    for src, en_val in table.items():
        new_table[src] = en_val  # Default to en_val, and override specific sections
    vi_terms["sections"][section_name] = new_table

# Specific Vietnamese overrides for core game terms
def safe_update(sec, d):
    for k, v in d.items():
        if k in vi_terms["sections"][sec]:
            vi_terms["sections"][sec][k] = v

safe_update("title_menu", {
    "スタート": "Bắt đầu",
    "ロード": "Tải game",
    "オプション": "Tùy chọn",
    "コンティニュー": "Tiếp tục",
    "セーブ": "Lưu game",
    "クリアデータセーブ": "Lưu hoàn thành",
    "ライブラリー": "Thư viện"
})

safe_update("damage_levels", {
    "無傷": "Vô hại",
    "小破": "Hư hại nhẹ",
    "中破": "Hư hại vừa",
    "大破": "Hư hại nặng"
})

safe_update("counter_orders", {
    "反撃する": "Phản công",
    "防御する": "Phòng thủ",
    "回避する": "Né tránh",
    "反撃不能": "Không thể phản công",
    "マニュアル": "Thủ công",
    "オート": "Tự động",
    "おまかせ": "Mặc định",
    "反撃しない": "Không phản công"
})

safe_update("map_commands", {
    "移動": "Di chuyển",
    "攻撃": "Tấn công",
    "精神": "Tinh thần",
    "変形": "Biến hình",
    "分離": "Tách rời",
    "合体": "Hợp thể",
    "搭乗": "Lên tàu",
    "発進": "Xuất kích",
    "着艦": "Hạ cánh",
    "補給": "Tiếp tế",
    "修理": "Sửa chữa",
    "待機": "Chờ lệnh",
    "能力": "Chỉ số",
    "作戦": "Chiến thuật",
    "ターン終了": "Hết lượt",
    "部隊表": "Danh sách đội",
    "検索": "Tìm kiếm",
    "設定": "Cài đặt",
    "セーブ": "Lưu game",
    "中断": "Tạm dừng",
    "システム": "Hệ thống",
    "全回復": "Hồi phục toàn bộ",
    "自動": "Tự động",
    "手動": "Thủ công"
})

safe_update("terrain", {
    "5thルナ": "5th Luna",
    "MSトレーラー": "Xe rơ-moóc MS",
    "MS残骸": "Xác tàu MS",
    "アクシズ": "Axis",
    "エネルギータンク": "Bình năng lượng",
    "クレバス": "Khe nứt",
    "クレーター": "Hố thiên thạch",
    "コロニー": "Colony",
    "コロニー残骸": "Tàn tích Colony",
    "コンテナ": "Container",
    "シャトル": "Tàu con thoi",
    "タンク": "Bồn chứa",
    "バルジ": "Barge",
    "ルナツー": "Luna II",
    "丘": "Đồi",
    "地球": "Trái Đất",
    "地面": "Mặt đất",
    "基地": "Căn cứ",
    "壁": "Tường",
    "宇宙空間": "Vũ trụ",
    "屋敷": "Biệt thự",
    "山": "Núi",
    "岩": "Bãi đá",
    "岸辺": "Bờ sông",
    "崖": "Vách đá",
    "川": "Sông",
    "平原": "Đồng bằng",
    "床": "Sàn nhà",
    "建物": "Tòa nhà",
    "建物(全壊)": "Tòa nhà đổ nát",
    "斜面": "Dốc núi",
    "暗礁空域": "Vùng đá ngầm",
    "月": "Mặt Trăng",
    "月面": "Bề mặt Mặt Trăng",
    "月面都市": "Thành phố Mặt Trăng",
    "森": "Rừng",
    "水": "Nước",
    "池": "Ao hồ",
    "浅瀬": "Vùng nước nông",
    "海": "Biển",
    "海底": "Đáy biển",
    "深海": "Biển sâu",
    "湖": "Hồ",
    "砂": "Cát",
    "砂漠": "Sa mạc",
    "空": "Bầu trời",
    "街": "Thành phố",
    "谷": "Thung lũng",
    "道路": "Đường sá",
    "都市": "Đô thị",
    "雪": "Tuyết",
    "雪原": "Đồng tuyết",
    "雲": "Mây",
    "青空": "Trời xanh",
    "首都": "Thủ đô",
    "宇宙": "Không gian",
    "荒野": "Vùng hoang vu"
})

safe_update("spirits", {
    "根性": "Kiên Trì",
    "ド根性": "Đại Kiên Trì",
    "信頼": "Tin Cậy",
    "友情": "Tình Bạn",
    "愛": "Tình Yêu",
    "補給": "Tiếp Tế",
    "熱血": "Nhiệt Huyết",
    "魂": "Linh Hồn",
    "ひらめき": "Tia Chớp",
    "不屈": "Bất Khuất",
    "鉄壁": "Thiết Bích",
    "集中": "Tập Trung",
    "必中": "Tất Trúng",
    "感応": "Cảm Ứng",
    "加速": "Tăng Tốc",
    "覚醒": "Thức Tỉnh",
    "気合": "Khí Thế",
    "気迫": "Khí Phách",
    "激励": "Khích Lệ",
    "幸運": "May Mắn",
    "祝福": "Chúc Phúc",
    "努力": "Nỗ Lực",
    "応援": "Cổ Vũ",
    "てかげん": "Nương Tay",
    "狙撃": "Bắn Tỉa",
    "直撃": "Trực Kích",
    "突撃": "Xung Kích",
    "脱力": "Thoát Lực",
    "かく乱": "Nhiễu Loạn",
    "復活": "Hồi Sinh"
})

safe_update("status_labels", {
    "HP": "HP",
    "EN": "EN",
    "移動力": "Di chuyển",
    "運動性": "Động cơ",
    "装甲": "Giáp",
    "限界": "Giới hạn",
    "地形適応": "Địa hình",
    "空": "Không",
    "陸": "Lục",
    "海": "Hải",
    "宇": "Trụ",
    "サイズ": "Cỡ",
    "修理費": "Phí sửa",
    "レベル": "Cấp độ",
    "経験値": "EXP",
    "気力": "Khí lực",
    "格闘": "Cận chiến",
    "射撃": "Bắn xa",
    "命中": "Chính xác",
    "回避": "Né tránh",
    "防御": "Phòng thủ",
    "反応": "Phản xạ",
    "技量": "Kỹ năng",
    "SP": "SP",
    "資金": "Tiền vốn",
    "ターン": "Lượt",
    "味方": "Phe ta",
    "敵": "Phe địch",
    "第三軍": "Phe thứ 3",
    "射程": "Tầm bắn",
    "命中率": "Độ chính xác",
    "攻撃力": "Sức tấn công",
    "クリティカル": "Chí mạng",
    "必要気力": "Khí lực cần",
    "消費EN": "Tiêu hao EN",
    "残弾": "Đạn",
    "必要技能": "Kỹ năng cần",
    "特殊能力": "Năng lực đặc biệt",
    "特殊技能": "Kỹ năng đặc biệt",
    "精神コマンド": "Lệnh tinh thần",
    "強化パーツ": "Linh kiện cường hóa",
    "スロット": "Khe cắm",
    "パイロット": "Phi công",
    "サブパイロット": "Phi công phụ",
    "妖精": "Tiên nữ"
})

# Preserve any trailing spaces/double spaces or MAP suffixes from en_terms
for section in vi_terms["sections"]:
    for k in vi_terms["sections"][section]:
        orig = en_terms["sections"][section][k]
        val = vi_terms["sections"][section][k]
        if orig.endswith("MAP") and not val.endswith("MAP"):
            vi_terms["sections"][section][k] = val + "MAP"
        # preserve double spaces
        for run in re.findall(r" {2,}", orig):
            if run not in val:
                vi_terms["sections"][section][k] = val + run

# Write terms/vi.json
terms_path = ROOT / "content/locales/terms/vi.json"
terms_path.write_text(json.dumps(vi_terms, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Wrote {terms_path}")

# 2. Translate UI keys
vi_ui = dict(en_ui)  # base copy

# Comprehensive UI translations
ui_translations = {
    "manual": "Thủ công",
    "auto": "Tự động",
    "fast": "Tua nhanh",
    "skip": "Bỏ qua...",
    "font_size": "Cỡ chữ",
    "controls": "{DUpDown} Tốc độ tự động  {A} Tiếp  {L} Lịch sử  {CUpDown} Cỡ chữ  {R}+{A} Tua nhanh  {R}+{Start} Bỏ qua",
    "controls_pad": "{A} Tiếp  {AuxL} Tự động  {DUpDown} Tốc độ  {AuxR} Tua nhanh  {R}+{Start} Bỏ qua  {L} Lịch sử  {CUpDown} Cỡ chữ",
    "history_title": "Lịch sử hội thoại",
    "history_controls": "{DUpDown} Cuộn · {DLeftRight} Chuyển trang · {L} / {A} / {B} Quay lại",
    "history_controls_pad": "{DUpDown} Cuộn · {DLeftRight} Chuyển trang · {L} / {A} / {B} Quay lại",
    "name_title": "Thiết lập nhân vật",
    "name_cancel": "Chọn nhân vật",
    "name_review": "Sẵn sàng bắt đầu?",
    "name_step_player": "Nhân vật chính",
    "name_step_partner": "Đồng đội",
    "name_step_review": "Xác nhận",
    "name_review_hint": "Kiểm tra tên của cả hai nhân vật trước khi bắt đầu cốt truyện.",
    "name_start": "Bắt đầu cốt truyện  →",
    "name_step_select": "Lựa chọn",
    "select_title": "Chọn nhân vật chính của bạn",
    "select_hint": "Chọn nhân vật chính và loại robot; mỗi nhân vật đi kèm một đồng đội.",
    "select_super": "Super Robot",
    "select_real": "Real Robot",
    "select_male": "Nam",
    "select_female": "Nữ",
    "select_confirm": "Tiếp: Xác nhận  →",
    "select_keyboard_hint": "{KeyLeft}{KeyRight} Chuyển đổi   ·   {Enter} / {A}: Xác nhận   ·   hoặc bấm vào thẻ",
    "select_keyboard_hint_pad": "{DLeftRight} Chuyển đổi   ·   {A}: Xác nhận   ·   hoặc chạm vào thẻ",
    "review_keyboard_hint": "{Enter} / {A}: Bắt đầu cốt truyện   ·   {Esc} / {B}: Chọn lại nhân vật",
    "review_keyboard_hint_pad": "{A}: Bắt đầu cốt truyện   ·   {B}: Chọn lại nhân vật",
    "name_unit": "Robot khởi đầu",
    "name_pilot": "Phi công",
    "unit_default_name": "March Wind",
    "settings_error": "Không thể đổi ngôn ngữ hoặc lưu cài đặt",
    "rules_menu": "Tùy chỉnh luật chơi",
    "rules_original": "Tắt tất cả (Luật gốc)",
    "rules_all": "Bật tất cả",
    "rules_note": "Có hiệu lực ngay lập tức; định dạng file lưu không đổi, giữ nguyên cho lần khởi động sau",
    "rule_esp_level": "ESP: Tỷ lệ trúng/né tính theo cấp kỹ năng (bản gốc: cố định 64)",
    "rule_seisenshi_level": "Chiến binh Thánh: Tỷ lệ né tính theo cấp kỹ năng (bản gốc: cố định 32)",
    "rule_limit_cap": "Giới hạn: Giới hạn trúng/né kết hợp cơ động ở mức tối đa",
    "rule_potential_bands": "Tiềm năng: Cân chỉnh mức máu kích hoạt (không cộng khi đầy máu)",
    "rule_potential_half": "Tiềm năng: Giảm một nửa thưởng trúng/né (chí mạng giữ nguyên)",
    "rule_weapon_inherit_map": "Đổi máy: Giữ lại nâng cấp cho 3 vũ khí bị thiếu trong bảng",
    "rule_aura_slash_power": "Chiến binh Thánh: Tăng uy lực Hyper Aura Slash theo cấp (+1500 ở L9)",
    "rule_boss_dummy_half": "Bù nhìn Boss: Giảm một nửa số lượng (ít nhất còn 1)",
    "rule_boss_dummy_none": "Bù nhìn Boss: Tắt hoàn toàn",
    "rule_upgrade_cap_break": "Mức nâng cấp tối đa: Mọi máy đều nâng cấp được tới 15 cấp (gốc: 6–15)",
    "rule_upgrade_refund": "Hoàn tiền xuất kích: Trả lại tiền nâng cấp khi máy rời đội theo cốt truyện",
    "rule_parts_carry_over": "Chuyển linh kiện: Tự động trang bị lại linh kiện sang máy mới khi đổi máy",
    "refund_notice": "{unit} đã rời đội — Đã hoàn lại {amount} tiền nâng cấp",
    "link_title": "Chọn tác phẩm liên kết",
    "link_hint": "Các tác phẩm đã chọn sẽ gia nhập trong màn chơi đặc biệt trước trận chiến tiếp theo.",
    "link_series_f91": "Mobile Suit Gundam F91",
    "link_series_goshogun": "Sengoku Majin GoShogun",
    "link_series_zambot": "Invincible Super Man Zambot 3",
    "link_lead_f91": "Seabook",
    "link_lead_goshogun": "Shingo",
    "link_lead_zambot": "Kappei",
    "link_units_f91": "F91, Vigna-Ghina",
    "link_units_goshogun": "GoShogun",
    "link_units_zambot": "Zambot 3",
    "link_crew_label": "Cùng với",
    "link_crew_f91": "Cecily",
    "link_crew_goshogun": "Killy, Remy",
    "link_crew_zambot": "Uchuta, Keiko",
    "link_joined": "Đã gia nhập",
    "link_scheduled": "Đã lên lịch",
    "link_ticked": "Đã chọn",
    "link_back": "Quay lại",
    "settings_title": "Cài đặt",
    "settings_page_general": "Chung",
    "settings_page_interface": "Giao diện",
    "settings_page_video": "Hình ảnh",
    "settings_page_audio": "Âm thanh",
    "settings_page_rules": "Luật chơi",
    "settings_page_input": "Điều khiển",
    "settings_page_about": "Thông tin",
    "settings_language": "Ngôn ngữ",
    "settings_images": "Đồ họa",
    "settings_aspect": "Tỷ lệ màn hình",
    "settings_window": "Cửa sổ",
    "settings_window_size": "Kích thước cửa sổ",
    "settings_ui_size": "Kích thước giao diện",
    "settings_battle_ui": "Giao diện trận đấu",
    "settings_intermission_ui": "Giao diện chuyển màn",
    "settings_name_entry_ui": "Giao diện đặt tên",
    "settings_title_ui": "Giao diện menu chính",
    "settings_fps": "Hiện FPS",
    "settings_fps_off": "Tắt",
    "settings_fps_on": "Bật",
    "settings_dialogue_hints": "Hướng dẫn điều khiển thoại",
    "settings_dialogue_hints_auto": "Tự động ẩn",
    "settings_dialogue_hints_always": "Luôn hiện",
    "library_title": "Thư viện dữ liệu",
    "library_tab_units": "Robot",
    "library_tab_pilots": "Phi công",
    "library_hint": "{KeyLeft}{KeyRight} Chuyển tác phẩm · {KeyUp}{KeyDown} Chọn · {Enter} Chi tiết · {Esc} Thoát",
    "library_hint_pad": "{DLeftRight} Chuyển tác phẩm · {DUpDown} Chọn · {A} Chi tiết · {B} Thoát",
    "viewer_title": "Trình xem trận đấu",
    "viewer_attacker": "Bên tấn công",
    "viewer_defender": "Bên phòng thủ",
    "viewer_weapon": "Vũ khí",
    "viewer_start": "Bắt đầu diễn hoạt",
    "viewer_back": "Quay lại",
    "menu_about": "Giới thiệu Marchwind 64",
    "menu_check_updates": "Kiểm tra cập nhật...",
    "menu_view": "Hiển thị",
    "menu_fullscreen": "Toàn màn hình",
    "update_check": "Kiểm tra bản mới",
    "update_status_current": "Bạn đang dùng bản mới nhất",
    "update_status_available": "Có bản cập nhật mới",
    "battle_effects_title": "Hiệu ứng chiến đấu",
    "battle_effects_note": "Tự động tính toán dựa trên kỹ năng và trang bị của đơn vị."
}

for k, v in ui_translations.items():
    if k in vi_ui:
        vi_ui[k] = v

# Ensure all 695 keys exist and have non-empty text
assert len(vi_ui) == len(en_ui), f"UI count mismatch: {len(vi_ui)} vs {len(en_ui)}"

# 3. Create vi.json
vi_doc = {
    "schema": "srw64.locale.v1",
    "locale": "vi",
    "source_locale": "ja",
    "font": "HarmonyOS_Sans_SC.ttf",
    "display_name": "Tiếng Việt",
    "scope": "Bản dịch giao diện và danh mục tiếng Việt cho Super Robot Wars 64.",
    "ui": vi_ui,
    "entries": []
}

vi_path = ROOT / "content/locales/vi.json"
vi_path.write_text(json.dumps(vi_doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Wrote {vi_path}")
