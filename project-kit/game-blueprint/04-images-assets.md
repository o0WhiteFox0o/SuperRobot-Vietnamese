# 04 — Quản lý ảnh và tài nguyên đồ hoạ

> Nguồn 🔍: [Ảnh gốc](../../docs/data/original-images.en.md), [Ảnh chiến đấu](../../docs/data/battle-graphics.en.md), [Danh mục dữ liệu](../../docs/data/original-data-catalog.en.md), [`assets/README.md`](../../assets/README.md), [Hồ sơ HD](../../docs/data/hd-asset-inventory.en.md), [Bản đồ chiến thuật](../../docs/data/tactical-maps.en.md).

## 4.1 Nguyên tắc cốt lõi

> [!IMPORTANT]
> **Ảnh ràng buộc với thực thể qua BẢNG GẮN, không qua tên hay số liền kề.** Ở SRW64, "ảnh nào đi với bảng màu nào" lấy từ bảng mà *mã game đọc*, tuyệt đối không suy ra từ số bên cạnh hay độ giống tên. Ví dụ: nhân vật 28 → ảnh `33` + palette `333`; 162 → `166/466`; 165 → `169/469`.

## 4.2 Các loại ảnh ở SRW64 🔍

| Loại | Định dạng/kích thước | Phạm vi tài nguyên | Khoá gắn |
| --- | --- | --- | --- |
| Chân dung | CI8, 96×96 (một số 97×97) + palette | 9–308, palette 309–609 | `0x84220 + actor×4` → `(ảnh, palette)` |
| Icon máy trên bản đồ | CI4, 16×16 | 687–1009, palette 1010 (+phe) | bảng `0x100D78` theo `unit_id` |
| Atlas chiến đấu của máy | CI8, kích thước `32k+1` (ví dụ 257×193) | 1612–1907, palette 1908–2212 | tam bộ `(cảnh, atlas, palette)` 6 byte, bảng theo `unit_id` |
| Cảnh sprite (scene) | nhị phân mô tả khung/bước | 2213–2476 (tư thế cơ bản) | cùng bảng |
| Hiệu ứng vũ khí / cut-in | atlas CI4/CI8 + palette + cảnh | 1337–1368 (cut-in), 3006–3532 (hiệu ứng) | bảng chiến cảnh tổng 1.053 ô |
| Hoạt cảnh bản đồ (ghép thể…) | nhiều đoạn | 1399–1611 | bảng 12 đoạn, 95 mục |
| Tiêu đề chương | CI4 514×65, palette 16 màu dùng chung | 4988–5334 | bảng theo số tiêu đề |
| Nền chiến đấu | CI4 320×240 + palette | 6067–6227 | byte môi trường theo `palette` |
| Bản đồ chiến thuật | layout + atlas CI8 512×512 (≤1024 ô 16×16) + palette | 158 bản ghi × 12 byte | số bản đồ |

Giải mã:
- Loại tài nguyên: chân dung `15|6` (8 byte header + CI8); icon `14` (CI4, nibble cao trước); palette `3` (RGBA5551 big‑endian).
- Palette giữ **bit trong suốt**; 5-bit → 8-bit theo quy ước dự án.
- Bản đồ: layout header `(7, số nhóm, w, h)` đơn vị 8px, lưới ô 16×16 = `w/2 × h/2`, mỗi ô 4 byte `(u16 địa hình+lật, u16 tile)`.

## 4.3 Cây xuất ảnh đặt tên theo thực thể 🔍

SRW64 xuất lại *theo tên máy/nhân vật/vũ khí* (thư viện ảnh dễ dùng), khác với bản duyệt dữ liệu (đặt theo số tài nguyên):

```text
assets/original-graphics/
├─ units/NNN-<tên máy>/          # một thư mục mỗi máy (363)
│   ├─ battle.png                 #   tư thế chiến đấu cơ bản
│   ├─ battle-sheet.png           #   atlas chiến đấu (kèm palette riêng)
│   ├─ map-icon.png               #   icon bản đồ
│   ├─ animations/                #   mọi bộ phận hoạt hình
│   └─ unit.json                  #   chỉ số, vũ khí, bản ghi chiến đấu/hoạt hình/hiệu ứng → tệp ảnh
├─ cutins/NNNN-<tên vũ khí>/     # theo vũ khí
├─ movies/NN-<tên>/               # hoạt cảnh theo thứ tự phát
├─ battle-scenes/atlas-AAAA/      # hiệu ứng: tia, nổ, chém, khiên…
├─ portraits/NNN-<tên đầy đủ>.png # 361 danh tính (nhiều danh tính dùng chung ảnh)
├─ chapter-titles/  maps/
├─ units.csv  weapons.csv         # bảng tổng, UTF-8 BOM
├─ animations.json                # phân tích hoạt hình/hiệu ứng/phản ứng phòng thủ
├─ manifest.json                  # mỗi tệp: loại, SHA-256, tài nguyên nguồn, chỉ số bảng gắn
└─ index.html                     # thư viện ảnh; hover → APNG
```

Quy ước: `NNN-` là **ID ổn định** + tên đọc được; đổi tên không đổi ID. `manifest.json` là nguồn chân lý: **không khớp ảnh bằng tên tệp**.

## 4.4 Định dạng "cảnh sprite" (hoạt hình ghép mảnh) 🔍

Một atlas được cắt thành mảnh (thường 32×32), lắp thành khung, rồi phát theo danh sách bước. Big‑endian:

```text
u8 step_count, u8 vertex_mode
step_count × (u8 frame, u8 ticks)        # frame = 0xFF: nhịp này không vẽ gì
u8 0xFF, u8 loop_step                      # kết thúc; loop_step = bước lặp lại
u16 frame_offsets[n]
frame: các mảnh 16 byte đến khi flags & 0x8000
  u16 flags (0x0010 = lật ngang) · u16 s,t (toạ độ nguồn) · u8 w,h · s16 x,y · u32 vertex_offset
```

🧭 Với game mới dùng JSON dễ chỉnh hơn nhị phân:

```json
{ "id": "swimmurg.idle", "sheet": "units/036/battle-sheet.png", "loop": 0,
  "steps": [{"frame": 0, "ticks": 6}, {"frame": 1, "ticks": 6}],
  "frames": [[{"src": [0, 0, 32, 32], "at": [-16, -32], "flip": false}]] }
```

## 4.5 Gói ảnh có lược đồ (`art manifest`) 🔍

```json
{
  "schema": "srw64.art-pack.v1",
  "id": "srw64.stage1-art",
  "locale": "neutral",
  "source": { "path": "assets/hd-ai/worldmap-surfaces/pack-v8", "manifest_sha256": "3e963925…0851" },
  "textures": [ { "hash": "0082929fd8c9a1fc", "kind": "frame", "sha256": "4aab3949…11bd" } ]
}
```

| Khái niệm | Quy tắc |
| --- | --- |
| Hai cơ chế thay ảnh | **(1) Thay texture theo hash** (RT64) cho viền hộp thoại/bản đồ thế giới; **(2) host vẽ cả tấm** cho chân dung/nền/tiêu đề |
| Danh sách cho phép | Khi biên dịch **ngoại tuyến** lọc theo `kind`; không đoán loại tài nguyên theo tên tệp lúc chạy |
| Mỗi tệp có `sha256` | lệch ⇒ gói không nạp |
| `locale: neutral` | ảnh không chứa chữ; ảnh có chữ phải tách theo ngôn ngữ |
| Mất gói HD | Original vẫn khởi động, hiện "HD không khả dụng" (xem [Original fallback](../../docs/native/native-original-fallback.en.md)); *yêu cầu HD tường minh mà hash lệch ⇒ báo lỗi* |
| Chuyển Original/HD | luồng cửa sổ gửi yêu cầu; luồng render xác nhận sau khi **workload đã gửi hoàn tất** rồi mới đổi bảng thay thế — không huỷ texture GPU đang dùng |

Ba loại nội dung "HD" ở SRW64: ảnh thay theo hash (270 mục: 213 mặt đất thế giới, 27 vật thể vũ trụ, 30 viền), vẽ cả tấm (chân dung, nền giữa màn, logo tiêu đề), và mô hình 3D native.

## 4.6 Bộ đệm lớp ảnh (tùy chọn) và chống lỗi viền

Bài học thực từ chân dung HD: **xử lý trong suốt sai gây viền đen**.
- Màu của điểm trong suốt phải **điền bằng màu đặc gần nhất** (không để đen) — lấy mẫu song tuyến *không nhân alpha* sẽ ra viền tối.
- Đăng ký (register) ảnh mới với ảnh gốc trước khi lấy mặt nạ; chỉ cho đường viền lệch ≤ ±1,5 điểm ảnh gốc.
- Nền xám chỉ "tràn" từ các điểm vốn trong suốt của ảnh gốc.
- Thu nhỏ: lấy mẫu lại **màu và alpha riêng**.
- Nghiệm thu bằng số: IoU đường viền 0,984–0,994; điểm lệch >16 mức sau phóng 3× = 0.

## 4.7 Lớp ảnh chồng (key → tệp)

| Nội dung | Khoá |
| --- | --- |
| Chân dung | `ảnh-palette` |
| Tranh máy | `cảnh-atlas-palette` |
| Bản đồ chiến thuật | số bản đồ (cả tấm) |
| Nền/tranh cốt truyện | số tài nguyên |
| Icon, bản đồ thế giới, viền | hash texture |

Thứ tự: gốc → gói tích hợp → gói người dùng → tuỳ chỉnh người chơi; lớp sau thắng.

## 4.8 Bản đồ chiến thuật HD — "vẽ cả tấm"

Thay vì thay từng ô, host **vẽ cả tấm** theo số layout (131/158 bản đồ). Thành phần: ảnh nền, bảng *địa hình* (cho logic), tuỳ chọn *bản đồ màu* (cho nước/hiệu ứng palette cycle), thuộc tính địa hình (100 mục × 11 byte: tên, phòng thủ, hiệu chỉnh trúng, hồi HP/EN, 6 mức tiêu hao di chuyển).

🧭 Khuyến nghị: **tách "hình" và "logic"**: ảnh nền chỉ để nhìn; luật di chuyển/phòng thủ nằm ở bảng địa hình. Đổi nghệ thuật không đổi cân bằng.

## 4.9 Quy tắc đặt tên & thư mục cho game mới 🧭

```text
art/
├─ portraits/<actor_id>-<slug>/{256.png, 96.png, 48.png}
├─ units/<unit_id>-<slug>/{icon.png, battle-sheet.png, battle.json, anim/*.json}
├─ weapons/<weapon_id>-<slug>/{cutin.png, fx/*.png}
├─ maps/<map_id>/{base.png, terrain.json, palette-cycle.png}
├─ chapters/<scene_id>-title.png        # có chữ ⇒ tách theo ngôn ngữ: chapters/<lang>/…
├─ backgrounds/<id>.png
└─ source/                               # PSD/Krita, không đóng gói
content/art/manifest.json                # NGUỒN CHÂN LÝ (khoá → tệp → sha256 → dùng bởi)
```

Mỗi mục manifest: `{key, file, sha256, kind, size, locale, used_by[]}`. Test kiểm: mọi `used_by` có thật, mọi ảnh trong cây có trong manifest (không "ảnh mồ côi"), mọi `sha256` khớp.

## 4.10 Vệ sinh tài nguyên

SRW64 chỉ giữ phiên bản đang dùng hoặc cần để tái tạo từng dòng HD; có **bản kê dọn dẹp** (`build/cleanup-YYYY-MM-DD.tsv`) và `assets/README.md` ghi *"đường dẫn → nội dung → nguồn/người dùng → xoá thì sao"*. 🧭 Làm y vậy ngay từ đầu.
