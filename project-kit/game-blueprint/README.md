# Game Blueprint — Thiết kế game chiến thuật có chiều sâu kiểu SRW64

Bộ tài liệu này **mổ xẻ cách SRW64 được cấu trúc** (nhân vật, máy, vũ khí, dữ liệu, ảnh, kịch bản, thoại) rồi chuyển thành **bản thiết kế dữ liệu hướng JSON** để bạn dựng một game mới có độ sâu tương đương.

> [!IMPORTANT]
> **Hai loại thông tin trong bộ này — luôn phân biệt:**
> - 🔍 **Quan sát ở SRW64** — lấy từ phân tích ROM/mã của dự án này, có địa chỉ/bảng/bằng chứng (link tới tài liệu gốc).
> - 🧭 **Khuyến nghị cho game mới** — thiết kế của chúng tôi dựa trên bài học đó (SRW64 lưu bằng bảng nhị phân trong ROM; game mới nên dùng JSON + ảnh PNG có lược đồ).
>
> SRW64 là game N64 (ROM 32 MB). Chúng tôi **không** sao chép nội dung/bản quyền; chỉ học *kiến trúc*.

## Mục lục

| # | Tài liệu | Nội dung |
| --- | --- | --- |
| 01 | [architecture.md](01-architecture.md) | Kiến trúc tổng thể 5 tầng, luồng dữ liệu, nguyên tắc ID ổn định |
| 02 | [characters-units-weapons.md](02-characters-units-weapons.md) | **Xây dựng nhân vật:** actor / pilot / máy / vũ khí / tinh thần / kỹ năng / cải tạo / tăng cấp |
| 03 | [json-data-management.md](03-json-data-management.md) | **Quản lý JSON:** bố cục thư mục, lược đồ, manifest + hash, lớp chồng, kiểm định |
| 04 | [images-assets.md](04-images-assets.md) | **Quản lý ảnh:** loại ảnh, định dạng, bảng ràng buộc, đặt tên, gói HD, dự phòng |
| 05 | [story-scripting.md](05-story-scripting.md) | **Quản lý cốt truyện:** cảnh, sự kiện, điều kiện, biến, tuyến, chiến dịch |
| 06 | [dialogue-localization.md](06-dialogue-localization.md) | Thoại, lượt chọn, thoại chiến đấu có điều kiện, đa ngôn ngữ |
| 07 | [battle-and-rules.md](07-battle-and-rules.md) | Công thức chiến đấu, địa hình, cải tạo, luật tuỳ chọn |
| 08 | [build-roadmap.md](08-build-roadmap.md) | Lộ trình dựng game mới: giai đoạn, ngưỡng nghiệm thu, checklist chiều sâu |
| — | [examples/](examples/) | Bộ nội dung mẫu chạy được + `validate_content.py` + test |

## Bản đồ ánh xạ: SRW64 → game mới

| Khái niệm | SRW64 (ROM) 🔍 | Game mới (JSON) 🧭 |
| --- | --- | --- |
| Danh tính nhân vật | `actor_id` 0–360 + bảng tên | `actors.json` |
| Chỉ số phi công | bản ghi 16 byte ×257, ánh xạ actor→record | `pilots.json` (record) + `actor.pilot` |
| Máy | bản ghi 36 byte ×363 | `units.json` |
| Vũ khí | bản ghi 16 byte ×1329 + danh sách theo máy | `weapons.json` + `unit.weapons[]` |
| Tinh thần | bảng học 12 byte ×148 + tên `969+cmd` | `spirits.json` + `pilot.spirits[]` |
| Kỹ năng/NT | cờ `+0xF` + ngưỡng 30 byte ×256 | `skills.json` + `pilot.skills` |
| Cải tạo | 5 đường cong ×15 bậc, giá, trần 6–15 | `rules/upgrade-rules.json` |
| Ảnh | tài nguyên 6.436 khối, bảng gắn | `art/manifest.json` + thư mục theo khoá |
| Cốt truyện | 142 cảnh, 1.812 sự kiện, 73 lệnh | `scenes/*.json` + `campaign.json` |
| Thoại | bảng 0: 50.975 bản ghi, `TextKey` | `dialogue/<ngôn ngữ>/*.txt` + `locales/*.json` |

## Cách dùng

1. Đọc 01 → 02 để nắm mô hình.
2. Chạy thử bộ mẫu: `python project-kit/game-blueprint/tools/validate_content.py project-kit/game-blueprint/examples/content`
3. Sao chép `examples/content/` làm điểm khởi đầu cho game của bạn; làm theo [08-build-roadmap.md](08-build-roadmap.md).
4. Mọi nội dung mới đi qua validator **trước khi** chạy game.
