# 03 — Quản lý JSON và dữ liệu

> Nguồn 🔍: [Kiến trúc nội dung](../../docs/native/native-content-foundation.en.md), [Danh mục dữ liệu gốc](../../docs/data/original-data-catalog.en.md), [Gói MOD](../../docs/design/mod-packages.en.md), [Kiến trúc mở rộng](../../docs/design/native-extensibility-architecture.en.md).

## 3.1 Bố cục thư mục — ai sở hữu cái gì

| Thư mục | Chứa | Sở hữu | Commit? |
| --- | --- | --- | :---: |
| `config/` | toolchain, profile, bảng bố cục dữ liệu, script kiểm chứng, định nghĩa màn mini | kỹ thuật | ✔ |
| `content/` | nội dung do dự án quản lý (locale, thoại, art manifest, font) | nội dung | ✔ |
| `reference/` | dữ liệu tham khảo được phép lưu (kèm hash) | nghiên cứu | ✔ |
| `assets/` | dữ liệu xuất lớn, gói HD | sinh ra | ✘ (có `README.md`) |
| `build/` | catalog sinh, bằng chứng chạy, log | sinh ra | ✘ |

Quy tắc SRW64: **`content/` là dữ liệu của bạn; `assets/` và `build/` xoá đi tạo lại được** (trừ HD — có ghi chú cách tái tạo trong `assets/README.md`).

## 3.2 Mọi tệp JSON có `schema` + phiên bản

Mọi tệp mở đầu bằng khoá `schema`. Đây là kỷ luật quan trọng nhất của dự án (đều có ở SRW64):

| `schema` | Tệp |
| --- | --- |
| `srw64.play-profile.v1` | profile chạy |
| `srw64.locale.v1` | `content/locales/<lang>.json` |
| `srw64.art-pack.v1` | `content/art/*.json` |
| `srw64.original-data-layout.v1` | `config/data/original-jp-v1.json` |
| `srw64.mini-stage.v1` | màn mini |
| `srw64.campaign.v1` | chiến dịch |
| `srw64.upgrade-rules.v1` | luật cải tạo |
| `srw64.mod.v1` | gói MOD |
| `srw64.translation-roster.v1` | danh sách nhân vật dịch thuật |

🧭 Quy ước đặt tên: `<game>.<loại>.v<N>`. Quy tắc tiến hoá (lấy từ gói MOD):

- Sau khi đặt `v1`: **chỉ thêm trường**, không đổi nghĩa trường cũ.
- **Trường lạ ⇒ lỗi** (strict) — không lặng lẽ bỏ qua. Bắt được lỗi chính tả trong khi tác giả còn ở trước màn hình.
- Đổi cấu trúc phá vỡ ⇒ `v2` + công cụ di trú.

## 3.3 Manifest + khoá danh tính (hash)

Dữ liệu có thể đến từ nguồn *không được phân phối* (ROM) → khoá bằng hash, không bằng đường dẫn:

```json
{
  "schema": "srw64.original-data-layout.v1",
  "rom_sha256": "ee5f4a21…b13e",
  "tables": [
    { "id": "units", "rom_offset": 465792, "stride": 36, "count": 363,
      "extent_basis": "code-stride/adjacent-boundary",
      "loader_vram": "0x800A6E68", "sha256": "45be20fe…6be" }
  ]
}
```

| Trường | Vai trò |
| --- | --- |
| `rom_offset`, `stride`, `count` | bố cục vật lý của bảng |
| `extent_basis` | **vì sao tin** số lượng này (đọc mã / ranh giới kế bên) |
| `loader_vram` | mã tiêu thụ — bằng chứng ngữ nghĩa |
| `sha256` | khoá byte bảng — thay đổi sẽ chặn nạp |

🧭 Với dữ liệu tự viết, dùng `build/catalog/manifest.json` sinh bởi công cụ biên dịch: liệt kê từng tệp, `sha256`, schema, số bản ghi. Profile **tham chiếu hash** chứ không tham chiếu "tệp mới nhất".

## 3.4 Từ bản ghi đến "danh mục" (catalog)

Mỗi bản ghi trích xuất giữ đủ để truy nguyên:

```json
{
  "id": "base:units:0036",
  "fields": { "hp": 4500, "en": 180 },
  "raw_hex": "11 94 00 B4 …",
  "source": { "table": "units", "rom_offset": 465792, "index": 36 },
  "semantic_confidence": "confirmed",
  "profile": { "search_terms": ["…"], "summary": "…", "has_stats": true }
}
```

| Thành phần | Mục đích |
| --- | --- |
| `id` dạng `base:<bảng>:<số>` | ID ổn định, deep link được |
| `fields` | giá trị đã giải mã |
| `raw_hex` | không bao giờ mất byte gốc |
| `semantic_confidence` | `confirmed` / `structure-confirmed` / `unknown` |
| `profile` (hợp nhất, chỉ-đọc) | gộp actor+pilot+spirit+skill để duyệt nhanh; **không sửa `fields`** |

`profile` được sinh bởi mã riêng (`original_profiles.py`) và gắn vào bản ghi; chỉ mục nhẹ (`search_terms`, `summary`, `has_stats`) cho phép trang duyệt không phải ghép nhiều bảng.

## 3.5 Cấu hình profile — chọn *những chiều độc lập*

```json
{
  "schema": "srw64.play-profile.v1",
  "baseline": "srw64-jp-rev0",
  "presentation": { "locale": "zh-Hans", "images": "original", "model_5600": "waterdrop",
                    "resolution_scale": 4, "font_size": 13 },
  "locales": { "ja": "content/locales/ja.json", "zh-Hans": "content/locales/zh-Hans.json",
               "en": "content/locales/en.json", "vi": "content/locales/vi.json" },
  "art_pack": "content/art/stage1-hd.json",
  "gameplay_mods": []
}
```

Bốn chiều độc lập (không chồng chéo): **Ngôn ngữ · Ảnh · Trải nghiệm cơ bản · Luật & hỗ trợ**. Ngôn ngữ không đổi ROM/tuyến/luật/trạng thái ngẫu nhiên.

> `gameplay_mods` **phải rỗng** ở giai đoạn đầu — để cấu hình không "trông như" đang chấp nhận mod chưa thực sự được nạp. 🧭 Nguyên tắc: *đừng có trường cấu hình nào hứa điều chưa làm.*

## 3.6 Lớp chồng nội dung (layering)

```text
gốc  →  gói tích hợp (built-in)  →  gói người dùng (theo thứ tự phụ thuộc)  →  tuỳ chỉnh của người chơi
```

- **Khoá → tệp**: gộp mọi lớp vào một bảng `khoá → tệp/giá trị`; lớp sau thắng; khoá không có → rơi về lớp dưới.
- Ví dụ khoá: chân dung `ảnh-bảng màu`; tranh máy `cảnh-atlas-palette`; bản đồ `số bản đồ`; thoại `số bản ghi (@17410)`; nhạc `số bài`; texture RT64 `hash`.
- **Tài nguyên mới** (không có ở gốc) có tên gói: `example.newpilots:portraits/ryu.png` — không đè nhau; gói khác dùng tên này để tham chiếu (đây là lý do tồn tại của "phụ thuộc").
- **Số liệu** ghi đè **từng trường**, không viết lại cả bản ghi:

```json
// data/units.json — ghi đè từng trường, phần không viết giữ nguyên gốc
{ "36": { "hp": 4500, "armor": 1300, "upgrade_cap": 12 } }
```

- Thời điểm có hiệu lực **ghi theo trường**: *mỗi lần đọc* (chỉ số cơ bản máy), *chép một lần khi tạo vũ khí mới* (loại cải tạo), *chưa xác minh* (chỉ số phi công). Đây là thông tin bắt buộc hiển thị trong trình quản lý MOD.

## 3.7 Gói MOD (chỉ dữ liệu, không mã)

```text
mod.json  campaign/  challenge/  story/  data/  rules.json  art/  dialogue/  audio/
```

```json
{ "schema": "srw64.mod.v1", "id": "example.gaiden", "version": "1.2.0",
  "name": {"ja": "外伝", "en": "Gaiden"}, "game": ">=0.4",
  "requires": {"example.newpilots": ">=1.0"},
  "optional": {"srw64.hd": ">=1.0"},
  "conflicts": {"someone.oldgaiden": "*"} }
```

| Quy tắc | Chi tiết |
| --- | --- |
| Quan hệ | **requires** / **optional** / **conflicts** |
| Thứ tự | tự tính: phụ thuộc ở dưới; người chơi chỉ chỉnh gói không liên quan; vòng phụ thuộc ⇒ lỗi |
| Xác minh trước khi chạy | cùng bộ quy tắc giữa công cụ Python và host; gói hỏng không bật; lỗi chỉ rõ **tệp, trường, lý do** |
| Không tải trực tuyến | thiếu phụ thuộc ⇒ báo thiếu gì, người chơi tự cài |
| Gói tích hợp | liệt kê dưới gói người dùng, đánh dấu "built-in", không xoá được |
| Bản gốc | **không** nằm trong danh sách MOD — gốc chính là game; MOD chỉ là thay đổi |

## 3.8 Quy tắc kiểm định (bắt buộc cho game mới)

Validator tối thiểu — xem [`validate_content.py`](tools/validate_content.py) trong bộ mẫu:

1. `schema` đúng, **trường lạ ⇒ lỗi**.
2. ID duy nhất, không tái sử dụng.
3. **Toàn vẹn tham chiếu**: `unit.weapons→weapon`, `actor.pilot→pilot`, `deployment→unit/actor`, mọi `name_key` tồn tại trong locale mặc định, `portrait` có trong art manifest.
4. **Biên số**: đường cong đúng độ dài, trần 5–15, giá trong khoảng, `terrain_rank` ∈ tập hợp hợp lệ.
5. Ô kiểm biên khi tra bảng ánh xạ (bài học nhân vật 284).
6. Mỗi bản ghi có thể truy nguyên (nguồn, hash).

Bước này chạy trong CI **và** trước khi khởi động game; **tệp hỏng không bao giờ được nạp một nửa**.

## 3.9 Công cụ dữ liệu — những gì SRW64 xây ngoài game

| Công cụ | Việc | Bài học 🧭 |
| --- | --- | --- |
| Trình duyệt dữ liệu cục bộ (`tools/data_viewer/serve.py`, chỉ nghe loopback, không có API ghi) | duyệt máy/phi công/cảnh/ảnh, deep link theo ID | xây ngay từ đầu; nó tự thành *tài liệu sống* |
| Trình xem cốt truyện (`story.html`) | đọc theo chương, lọc theo tuyến | cho biên kịch xem kết quả mà không cần chạy game |
| Bảng tổng (`units.csv`, `weapons.csv`) | so sánh cân bằng bằng bảng tính | luôn xuất CSV UTF‑8 BOM |
| `export` luật + `--units/--weapons` kèm tên | người chơi sửa số: *xuất giá trị gốc → sửa → xoá phần không đổi* | khuyến khích người chơi viết mod bằng *khác biệt* |
