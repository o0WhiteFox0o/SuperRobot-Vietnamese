# 07 — Chiến đấu & luật chơi

🔍 = quan sát ở SRW64 · 🧭 = khuyến nghị. Nguồn: [`docs/gameplay/battle-formulas`](../../docs/gameplay/battle-formulas.vi.md).

## 1. Thứ tự phân xử một đòn đánh
🔍 Tính trúng → phân thân (bunshin) → chém đỡ (切り払い) → thân giả → rào chắn → phòng thủ S.
🧭 Mô hình thành **pipeline các bước** có thứ tự cố định, mỗi bước là hàm thuần `(ctx) -> ctx` có thể bị thoát sớm; dễ test từng bước và thêm bước mới.

## 2. Công thức sát thương
🔍
- `stat` = chỉ số cận chiến nếu vũ khí có cờ `0x80`, ngược lại xa.
- `A = sức mạnh vũ khí × địa hình vũ khí × stat/100 × sĩ khí công/100 × địa hình máy`
- `D = giáp × (iron wall ? 2 : 1) × sĩ khí thủ/100 × địa hình thủ`
- `R = (A−D) × (100−phòng thủ ô)/100`; tình yêu/hữu nghị ±30%
- `R = max(R,10)`; 魂 ×3, 熱血 ×2, còn lại chí mạng ×1.5; lệnh Defend ÷2; trần 65535.
- Hạng địa hình `-/D/C/B/A → 0/60/80/100/120%`, nhân dồn.
- Hàm **ước lượng** không tiêu thụ RNG.

🧭 Lưu công thức trong `data/rules/*.json` (hệ số, trần, sàn) và hàm thuần trong code; mọi hằng số có tên, không số ma thuật. Hàm ước lượng và hàm thực dùng chung một lõi, khác nhau ở chỗ RNG được truyền vào.

## 3. Tinh thần (spirit/skill)
🧭 Trạng thái = bitmap cờ + thời hạn (`until: "next_attack" | "turn_end" | n_turns`); tiêu SP theo bảng; hiệu ứng khai báo dạng dữ liệu (`{"op":"damage_mult","value":2}`) chứ không if-else rải rác.

## 4. Luật nâng cấp
🔍 Trần nâng cấp 6–15 ("vịt xấu xí"), đường cong và giá: xem [02](02-characters-units-weapons.md).
🧭 `rules/upgrade-rules.json`: `curve` dài 15, `cap` 5–15, `price` 1–99998 (validator kiểm tra).

## 5. Nguyên tắc: sửa nền vs luật tuỳ chọn
- **Sửa nền (base fix)**: sửa lỗi rõ ràng (tràn chỉ số, trỏ ngoài bảng). Bật mặc định, có test.
- **Luật tuỳ chọn**: thay đổi cân bằng → để trong `config/profiles/*.json`, tắt mặc định.
- Không trộn hai loại; ghi rõ vào changelog.

## 6. Xác minh
1. **So sánh hai lần chạy**: cùng seed, bản gốc vs bản sửa — chỉ phần mong muốn được đổi.
2. Test thuần cho từng bước pipeline.
3. ⚠️ Đường cong khớp dữ liệu **không chứng minh** công thức đúng; hãy đối chiếu với nhiều mẫu độc lập và ghi độ tin cậy.
