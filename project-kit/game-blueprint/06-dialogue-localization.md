# 06 — Thoại, lời thoại chiến đấu & bản địa hoá

🔍 = quan sát ở SRW64 · 🧭 = khuyến nghị.

## 1. Định dạng file thoại `.txt`

🔍
```text
# comment
@17412 001
> 原文 (dòng so sánh nguồn)
Bản dịch dòng 1
---
Trang tiếp theo, xin chào {HeroNick}!
* Lựa chọn A
* Lựa chọn B
```
- `@<recordId> speaker` mở một câu; `>` là dòng gốc; dòng kế tiếp là bản dịch; `---` lật trang; `* ` là lựa chọn; `#` là chú thích.
- Placeholder: `{HeroNick}`, `{HeroName}`, `{HeroSurname}`, `{HeroFull}`, `{Partner*}`, `{HeroMech}`, `{G:0104}`.
- Ký tự đặc biệt đầu dòng được escape bằng `\`; không dùng `<` nửa-rộng.

Vị trí: `content/dialogue/<locale>/story/scene-NNNN.txt`, `battle/speaker-NNN.txt`, `intro.txt`, `ending.txt`, `credits.txt`.
Fallback: thư mục user → bản đóng gói → bản gốc tiếng Nhật; lỗi sẽ vô hiệu hoá **cả entry**; F5 nạp lại; báo cáo ghi vào `dialogue-report.txt`.
Xem: [`docs/guide/dialogue-text`](../../docs/guide/dialogue-text.vi.md).

🧭 Giữ định dạng "một dòng gốc + một dòng dịch" (dễ diff, dễ review), nhưng dùng **khoá ổn định** (`scene.001.line.012`) thay cho số record; kiểm tra placeholder khớp giữa gốc và bản dịch trong validator.

## 2. Khoá văn bản & locale

🔍 TextKey dạng `base:t00_17412`; bảng 0 có 50.975 bản ghi. Locale JSON `srw64.locale.v1`: `locale`, `source_locale`, `font`, `display_name`, `scope`, `ui{}`. Bảng thuật ngữ trong `content/locales/terms/` (mở rộng bằng `apply_terms.py`). Locale hiện có: en, ja, vi, zh-Hans.

🧭 `locales/<lang>.json` chứa `ui`, `names` (theo `name_key`) và `terms`. Mọi `name_key` trong dữ liệu phải có ở locale gốc; locale khác thiếu thì fallback về locale gốc và cảnh báo (không lỗi).

## 3. Lời thoại chiến đấu

🔍 Giọng nhân vật: `D_800CA9C4[actor]` (257 giọng). Bảng chung có 9 tình huống: 0 tấn công · 1 bị hạ · 2 thiệt hại nặng · 3 vừa · 4 nhẹ · 5 né · 6 vô hiệu đòn · 7 hết đạn/EN · 8 ngoài tầm. Danh sách có điều kiện: mã điều kiện (vũ khí 900+/2600+, đối thủ nữ 5000, combo 8000+, tình huống 10000+2500·s+k) chia 3 nhóm ưu tiên; nhóm cao nhất thắng, chọn ngẫu nhiên trong nhóm. Dòng chung bị re-roll với xác suất loại 2/3. Mỗi dòng có chú thích `# 触发：`.
Xem: [`docs/data/battle-quotes`](../../docs/data/battle-quotes.vi.md).

🧭 JSON:
```json
{"speaker":"pilot.hero","lines":[
  {"when":{"situation":"attack"},"text_key":"q.hero.atk1","priority":0},
  {"when":{"weapon":"weapon.beam_saber"},"text_key":"q.hero.saber","priority":2}]}
```
Quy tắc: ưu tiên cao thắng → ngẫu nhiên trong nhóm → fallback bảng chung. Có bộ test "mọi pilot có ≥1 dòng cho mỗi tình huống".

## 4. Quy trình dịch
1. Xuất khung từ nguồn (key + dòng gốc).
2. Áp bảng thuật ngữ (`terms`) trước, dịch tay sau.
3. Chạy validator: placeholder, độ dài tối đa theo font/hộp thoại, key thiếu.
4. Review trong game (F5 nạp lại), xem báo cáo.
5. Mỗi ngôn ngữ độc lập; một lỗi không làm hỏng ngôn ngữ khác.
