> **Ngôn ngữ / Language:** [Tiếng Việt](battle-animation-rendering.vi.md) · [English](battle-animation-rendering.en.md) · [中文](battle-animation-rendering.md)

# Phân tích cơ chế kết xuất hiệu suất chiến đấu

2026-09-30. Phân tích tĩnh (tháo gỡ + bảng dữ liệu ROM, không thêm đầu dò mới) để hoàn thiện việc điều chỉnh màn hình rộng và thiết lập phiên bản HD của hiệu suất chiến đấu. Máy trạng thái, hệ thống treo và giải quyết nằm trong [battle-animation-skip.md](../native/battle-animation-skip.md) và phần đã được thực hiện cho màn hình rộng nằm trong [deck-16x10.md](deck-16x10.md) Mục 8/13; bài viết này sẽ không lặp lại những nội dung đó. Ai viết “suy luận” cũng chưa kiểm chứng được bằng máy thực tế đâu.

Quy ước địa chỉ: lớp phủ chiến đấu `load_00121560` nằm trong `801C2600` (ROM offset = `0x121560 + RAM − 0x801C2600`); phần còn lại là phân khúc dân cư.

## 1. Tổng quan: lớp phủ Tôi hầu như không vẽ gì cả.

Chỉ 5 từ lệnh RDP xuất hiện trong toàn bộ lớp phủ trận chiến (`FF`, `F6`, `FA`, `B6` và danh sách tĩnh của dải mặt nạ). Cơ thể, các hiệu ứng đặc biệt, bầu trời, mặt đất và HUD đều được vẽ thông qua công cụ **Sprite/Node Engine**. Do đó, không cần thay đổi danh sách hiển thị của lớp phủ ở cả màn hình rộng và HD. Bạn chỉ cần sửa đổi một số trình kết xuất và quy trình ma trận của công cụ thường trú. Điều này phù hợp với đường dẫn đã được thực hiện giữa bản đồ và trường.

Hình ảnh của một màn trình diễn bao gồm bốn lớp, từ sau ra trước theo mức độ ưu tiên của nút:

| Lớp | Thực hiện | Họa sĩ | Ghi chú |
| --- | --- | --- | --- |
| Bầu trời/bầu trời đầy sao | Khe yêu tinh 0/1 (lớp thứ hai 3/4), chế độ 2 | `80095974` | VĂN BẢN khối 32×32, được bọc modulo 320×240 |
| Mặt đất | Nút mô hình 3D 3 khối × 3 lớp (danh sách hiển thị tài nguyên) | Nút loại 2 | x = −1000·s / 0 / +1000·s, phép chiếu phối cảnh |
| Cơ thể, hiệu ứng đặc biệt của vũ khí, cut-in, vụ nổ | Cảnh sprite, chế độ 0xE/0xF/0x10 | `8009761C` | Một G_QUAD cho mỗi phần có 4 đỉnh, tùy thuộc vào phép chuyển đổi ma trận nút |
| Lớp hiệu ứng đặc biệt lăn (đường tốc độ, đám mây chảy) | Khe 0x19, chế độ 2 | `80095974` | `801C3610(kind, speed)` được tạo, cũng modulo 320 |
| HUD (Cửa sổ HP, thước đo, số, hình đại diện, hộp thoại, dải mặt nạ) | Chế độ 9/7 sprite, công cụ văn bản, danh sách tĩnh `80222D50` | `800945D4``8009B74C``801C2C98``8008EB5C``800964E4` | Đã được cung cấp bởi `battle_hud.cpp` welt |

## 2. Tài nguyên dữ liệu

Mã giải mã nằm trong `src/srw64_native/battle_graphics.py` và thư mục xuất là `assets/original-graphics/` (`battle-scenes/` 321 bản xem trước thư viện ảnh, `cutins/` 15 nhóm, `animations.json` ba thư viện hoạt ảnh).

### 2.1 Bộ ba kịch bản

Mỗi đối tượng có thể vẽ là một bộ ba (cảnh, tập bản đồ, bảng màu), một mục 6 byte:

| Bảng | ROM | Số lượng mặt hàng | Người đọc | Mục đích |
| --- | --- | --- | --- | --- |
| `unit_poses` | `0x84E40` | 365 | `8009C864` | Tư thế cơ bản của cơ thể (nó cũng được sử dụng trong các bức tranh lớn trên trang liên trường) |
| `battle_scenes` | `0x11E3D0` | 1053 (1051 hợp lệ) | `801C3170` | Mẫu đăng ký biểu diễn: chuyển động cơ thể, vũ khí, hiệu ứng đặc biệt, cắt cảnh (984–1038), vụ nổ |
| `chapter_titles` | `0x84B20` | 133 | `8009C8EC` | Không liên quan đến chiến đấu |

Tài nguyên cảnh = trình tự bước (số khung, số khung) + bảng khung; một khung là một số phần 16 byte {cờ (lật ngang 0x10), s, t, w, h, x, y, offset đỉnh}, `vertex_mode` 0 8 đỉnh trên mỗi phần (bình thường 4 + gương 4), 1 chỉ 4, 2 không có. Thống kê ROM:

- 1051 cảnh, 3905 khung hình, 34130 phần; 99% các bộ phận là 32×32 (33779 mảnh), còn lại là 16×32, 24×32, 8×32, v.v., lên đến 40×40.
- vertex_mode: 0 có 965, 1 có 84, 2 có 2.
- 527 ảnh trong atlas: 303 ảnh loại 5 (CI4, 16 màu), 179 ảnh loại 7 (CI8), 45 ảnh loại 6 (CI8), tổng cộng khoảng 27,1 M pixel (CI4 16,8 M, CI8 10,3 M). 4 u16 đầu tiên là {type, width+1, Height+1, 0}. Kích thước phổ biến là 64×32, 96×32, 64×64, 96×160, 512×512 (album lớn gồm 11 ảnh).
- 611 bảng màu: 333 trên 32 byte (16 màu), 185 trên 256 byte (128 màu), 54 trên 128 byte, 35 trên 224 byte, 4 trên 1184 byte (592 màu). CI8 chỉ có thể lập chỉ mục 256 màu đầu tiên. Để biết các phần bổ sung, hãy xem §5.4 Palette Animation.
- Canvas cảnh lớn nhất (hộp giới hạn của tất cả các khung) là 64×32, 32×32, 64×64, 96×96, 128×128, 128×96.
- **Tổng cộng có 18398 lát cắt phần khác nhau (tập bản đồ, bảng màu, s, t, w, h)**, trong đó 391 lát được sử dụng cho tư thế cơ bản của cơ thể. Đây là thứ tự độ lớn của lộ trình "thay thế bằng hàm băm kết cấu".

### 2.2 Bản ghi hoạt hình vũ khí (không phải mã byte)

Ba thư viện (`ANIMATION_BANKS`): `weapon` 1329 mục (theo số vũ khí), `hit` 159 mục (hit_script trong tiêu đề vũ khí; 156–158 là hạ gục), `reaction` 28 mục (mã phản ứng của người phòng thủ). Trình đọc `801C3128`/`801C31E8`/`801C3230`, cửa sổ DMA 0x3C0 byte.

Một bản ghi = 4 giây đầu tiên16 {máy ảnh 0–3, hit_script, hành động, hậu vệ_action} + danh sách hiệu ứng âm thanh (8, kết thúc bằng 0xFFFF) + danh sách diễn viên (24, 16 byte cho mỗi mục: số đăng ký battle_scenes, x, y, z, h4, h5, h6, hành vi). hành vi là một chỉ mục trong bảng chuyển hành vi `80225030` (389 mục nhập, 294 quy trình khác nhau, xem §6). Thống kê ROM: chế độ camera 1 chiếm 905 mục, 0 chiếm 405, 2 chỉ 17, 3 chỉ 2; số lượng diễn viên từ 1–12, nhiều nhất là 2 người (472 người); vũ khí tham khảo tổng cộng 815 mục đăng ký khác nhau.

Có hai bảng 7×s16 bổ sung: Nhật ký chiến đấu máy bay `0x118610` (354 hàng; +1 tỷ lệ phần trăm sprite, +2..4 sprite lá chắn, +5 cảnh bổ sung, +6 vụ nổ) và Nhật ký chiến đấu vũ khí `0x119970` (1329 hàng; số vũ khí hội thoại, loại liên hệ, kiểu đánh, mã pha).

### 2.3 Bản ghi nền (ROM `0x5BC30`, 0x26 byte một)

`8008422C` đã đọc; chỉ mục `80084A78(a, b, side)`: số bản ghi = `D_800C5940[a]` (ROM `0x50330`, 32 mục → nhóm 0–0x17) × 101 + b, a/b từ bản ghi chiến đấu +0xB/+0xA (suy ra b là số bản đồ). Khoảng 2366 mặt hàng có giá trị.

| Bù đắp | Ý nghĩa |
| --- | --- |
| +0 | Kiểu; khi 1, tạo nút gradient/sương mù của khe side+0x25 (gọi lại `8009BCC4`), +1..+7 là màu → `D_8010F5B7..BE` |
| +8 / +0xE / +0x14 | Ba lớp nền {loại u8, ?, tài nguyên u16, tham số u8, ?} |
| +0x1A / +0x1C / +0x1E | Loại bầu trời (0 không có; 2 chung; 5/6/8/9/10 hiếm), tài nguyên bầu trời, tài nguyên thứ cấp (được suy ra là bảng màu) |
| +0x20 / +0x22 / +0x24 | Lớp bầu trời thứ hai (khe 3/4), chỉ có 14 được sử dụng |

Ví dụ: Bản ghi 20 (Makoto Z so với ザクⅡ bản đồ đó) Mặt đất (1,5701) (1,5652) (1,5653), Sky 6092/6170; Kỷ lục 87 (Không gian) Mặt đất (1.5683) (6.5684) (1.5685), Bầu trời 6109/6216. Khi bầu trời thuộc loại 9 (tài nguyên 6104 bầu trời đầy sao), hãy thay mảnh đất đầu tiên bằng tài nguyên 5840.

Phạm vi nội dung HD sẽ được thay thế: Bầu trời 6067–6115 (Nội dung phụ 6116–6224), Mô hình và kết cấu mặt đất 5584–6066, Bầu trời đầy sao 6104/5840, Lớp cuộn 3186/3190/3191 (Nội dung phụ 3455–4747).

## 3. Elf và node engine

### 3.1 Bố cục bản ghi

- **Tiêu đề vị trí** `800FFA70 + 槽×0xC4` (300 vị trí): chế độ +0, +1 hợp lệ, +4/+8/+C xyz (f32), tỷ lệ +10/14/18, xoay 1C/20/24 (rad), +28/2C/30 Chỉ đọc theo thói quen chuyển động (được suy ra là tốc độ, không được nhập vào ma trận), +0x50 (`800FFAC0`) trại / bit gương.
- **Bản ghi phụ** `800FFAA4 + 槽×0xC4 + 子×0x30` (3 mỗi vị trí): +0 hợp lệ, +1 alpha, +4 con trỏ nút, +8/9/A bit danh mục chế độ, +C/E/10 số tài nguyên thô, +12/14/16 cảnh/thư viện/bảng màu **xử lý** (`80089E9C` phân bổ, `8008A11C` lấy địa chỉ, xử lý bảng `80160340` 20 byte mỗi mục: +2 số tài nguyên ROM, +0x10 địa chỉ dữ liệu), +18 khung hình còn lại của bước này, +19 bước hiện tại, +1A cờ hoạt hình (bit0 đơn, bit1 dừng; `801C5328` vượt qua 2 = bước thủ công), +1C bit gương, +1E..+2A bản ghi hiệu ứng bảng màu. +0xA/+0xC/+0xE/+0x11 của `800FFAAC + …` được viết ở nơi khác trong tài liệu là +12/+14/+16/+19 ở đây.
- **Nút** (0x6C byte, nhóm `80163630`, đầu chuỗi `80163638`): +0 mức độ ưu tiên, +1 loại 2 bit thấp (0 danh sách hiển thị tĩnh, 1 lệnh gọi lại, 2 hình ảnh) | 4 ẩn | chuyển đổi 8 bóng | bóng 0x10 | Căn chỉnh 0x20/0x40, gọi lại +C, **+14 Ma trận 4×4 dấu phẩy động**, +64 vị trí, +68 phụ. `8008B614` được chèn theo thứ tự ưu tiên tăng dần, với các giá trị bằng nhau được chèn trước các giá trị hiện có.

### 3.2 Xây dựng Yêu tinh

`80098158(槽, 子, 模式, 优先级, 场景, 图集, 调色板, 动画标志)` là vỏ của `80097C68`: nhấn `jtbl_800D0530[模式−1]` để chọn họa sĩ, sau đó nhấn `8008B4F4(槽, 子, 模式, 优先级, 4, 1, 节点标志, 绘制器)` để tạo nút. `80098204/80098590/80098604` Thay đổi cảnh/tập bản đồ/bảng màu tương ứng (nhả bộ điều khiển cũ và phân bổ bộ điều khiển mới).

Bảng lược đồ (phần mà bài viết này đề cập đến):

| Chế độ | Họa sĩ | Cờ nút | Cách sử dụng |
| --- | --- | --- | --- |
| 2/4 | `80095974` | — | VĂN BẢN được chia nhỏ, vị trí làm tròn +4/+8, có alpha: bầu trời, lớp cuộn, nền liên trường |
| 7 | `800964E4` | — | Hình đại diện |
| 8/9 | `800945D4` | — | VĂN BẢN dạng lưới 16×16, không có alpha: hộp HUD, huy hiệu |
| 0xB / 0xC | `800975A4` → `80096CD8` | — | Một VĂN BẢN cho mỗi phần (tọa độ màn hình, không chia tỷ lệ) |
| 0xD | `8009751C` → `80096CD8` | — | Tương tự như trên, y trừ z |
| 0xE | `80097D94` → `8009761C` | 0 | Quad, tịnh tiến + chia tỷ lệ + xoay quanh Z/Y/X |
| **0xF** | `80097D1C` → `8009761C` | 0x20 | Quad, sau khi dịch + zoom guCăn chỉnh về phía camera (biển quảng cáo) - thân máy và hầu hết các hiệu ứng đặc biệt |
| 0x10 | `80097D58` → `8009761C` | 0x40 | Tương tự như 0xF, chỉ căn chỉnh với các thành phần y/z |

Phương pháp xây dựng trong trận chiến: `801C50D8` (diễn viên) kiểm tra `800C9C6C` đến `8009C130` để lấy byte loại và mức độ ưu tiên (mặc định 0x9A); gõ 0x90/0x93/0x9C → chế độ 0xB (tọa độ màn hình TEXRECT, được suy ra là đoạn cắt, loại phụ đề), phần còn lại → 0xF; `8009C18C` chạm vào bảng `800C9C40` → 0x10. `801C4160` (thân máy, khe được đánh dấu từ +0x95) và `801C5328` (khe 0x9A) được cố định thành 0xF. Bóng được tạo bởi `801C28E0` ở cấp độ phụ 1, atlas 0x1580/bảng màu 0x1581, tiến tới `8009C004` → `8009BD68` LOADBLOCK.

**Tỷ lệ**: `801C34D8` → `801C30D0(id, 1)` Lấy tỷ lệ phần trăm của bản ghi nội dung 100 và viết +10/14/18 cho ba trục.
**Hình ảnh phản chiếu không phải là lật vectơ**: Bit trại của `800FFAC0` được viết bởi `801C55FC`/`801C7D40` (`801C5280` nhận âm x cùng lúc); `8009761C` ở vertex_mode 0 và khi bit này được đặt, địa chỉ đỉnh là +0x40, tức là nhóm thứ hai (ảnh phản chiếu) gồm 4 đỉnh được lưu trong phần sẽ được lấy. 84 cảnh của vertex_mode 1 không có nhóm gương.

### 3.3 Ma trận: tính toán thống nhất một nơi

Trình kết xuất `8009761C` **không tự phát hành G_MTX**. `8008261C` (`801C9BA8` được điều chỉnh ở cuối mỗi khung) đi qua 300 vị trí

- `800B4090` ma trận nhận dạng → cờ nút 0x10 (được tô bóng) `8007EA10` dịch (x, 0, z) + `8007EA64` tỷ lệ (1 − y·0,003); nếu không thì dịch (x, y, z), chia tỷ lệ (sx, sy, sz).
- Chế độ 0xE thì `8007EE8C/EDC0/ECF0` quay quanh Z/Y/X (+24/+20/+1C).
- Chế độ 0xF (cờ 0x20) được nhân trái với guAlignF `800B31E0(0, 旋转 + eye − at)` với `800B3CC0`; 0x10 (0x40) chỉ sử dụng thành phần y/z.
- Kết quả được ghi vào nút +14. Khi vẽ `8008B324` của `8008AE90` sử dụng `800B3F50` (guMtxF2L) + `DA380003` (MODELVIEW LOAD, không được đẩy lên ngăn xếp).

**Phép chiếu**: `800883FC` = guPerspective(`800B4430`) fovy **50°**, khía cạnh = `D_8010F5C0 / D_8010F5C2` (320/240, từ bảng phân giải ROM `0x51320`, được viết bởi `8008BF60`), gần **20**, xa **3000** → `D_8015DCAC`; sau đó guLookAtReflect `800B3C48` (mắt `D_8015DDFC..`, tại `D_8015DDF0..`, lên `D_8015DE14..`) → `D_8010F71C`. Cờ nút 8 thay đổi khi `800885B4` phối cảnh LOAD, sau đó `80088580` xem MUL. Chế độ xem `D_800C6950` (ROM `0x51340`) chỉ được điền một lần bởi `8008C1D4(sx, sy)`/`8008C390(tx, ty)` khi `8008C1AC/1B8` được khởi tạo. Lớp phủ chiến đấu không thay đổi khung nhìn.

**Không có bộ đệm Z**: `E200001C 00000000` ở đầu khung, trình kết xuất không gửi E2, ngữ cảnh phụ thuộc hoàn toàn vào mức độ ưu tiên của nút; z chỉ bị ảnh hưởng bởi sự phân chia phối cảnh.

### 3.4 Tải họa tiết (mỗi phần một lần)

Tiêu đề Atlas u16[0] loại 5/0xE → CI4 (`F0 0703C000` chứa 16 màu), nếu không thì CI8 (`073FC000` chứa 256 màu); bảng màu từ +8 RGBA16. Mỗi phần: `FD` SETTIMG (chiều rộng = chiều rộng bản đồ) → `F5` ô7 TMEM 0 → `F4` LOADTILE (s,t)-(s+w,t+h) → `F5` ô 0 dòng=(w+8)/8, word1=0 (không có mặt nạ, không kẹp)→ Hai `F2` (đầu tiên (s,t)-(s+w,t+h), sau đó được bao phủ bởi (0,0)-(w,h), UV đỉnh so với bộ phận) → `E3000C00 80000` hiệu chỉnh phối cảnh, `D7 FFFF`, `07000204/406` G_QUAD. CI chỉ sử dụng TMEM 2 KB thấp hơn: CI8 2048 texel, CI4 4096 nên phần lớn các phần đều có kích thước 32×32. Khi alpha không phải là 0xFF, hãy thay đổi CC thành `FC119623/FF2FFFFF` đồng thời `FA` alpha nguyên thủy (`8009768C`).

### 3,5 Trên mỗi khung hình

`801C9D84` đăng ký `801C9710` (đã cập nhật) với `801C96F4` (đã rút ra → `8008AE90`). `801C9710`: `801C9DAC` (đầu vào) → bảng trạng thái `80222DD4[D_80250000]` → `80098880` (300 vị trí mỗi lần chạy `80098738` trình tự bước: +18 và giảm xuống 0 bước; khi đạt đến số bước, bit0 được đặt thành bit1 và dừng, nếu không thì bỏ qua loop_step) → tập lệnh diễn viên `801C9404/801C8F4C` → `8008261C` Tính ma trận. `8008AE90` xóa màn hình ở đầu khung `F6`, ba đèn `DC08`, `8008AD40` gửi `gSPViewport(D_800C6950)`, `gSPClipRatio(1)`, `800883FC`, sau đó vẽ chúng theo thứ tự tăng dần về mức độ ưu tiên của chuỗi nút - **bất kể số vị trí và z**.

## 4. Ống kính

Máy ảnh không di chuyển mối quan hệ giữa mắt và tại, mà "sprite di chuyển về phía điểm mục tiêu và điểm tại theo sau":

- Khởi tạo `801C9BD4` (từ 801C9C04): khoảng cách `D_8015DE2C` = 260, cao độ `D_8015DE08` = 2,4°, góc phương vị `D_8015DE0C` = 0, at.y `D_8015DE24` = 32, at.z = 0, x vị trí của cả hai máy ±800 (`D_802501F8/80250210`). Mỗi khung `801C9BA0` điều chỉnh cư dân `800816D8`: mắt = at + tọa độ hình cầu (khoảng cách, cao độ, góc phương vị) và tính toán lại. `801C76A0` (801C7804) Một trạng thái nhất định sẽ đặt lại góc về 2,4°/0. Lượng rung `D_80178D44/D48` (thường trú `80088650…` được viết) được xếp thành x tại `801C9AE0`.
- Điểm mục tiêu `D_80250228/22C/230`: `801C6224` ghi giá trị ban đầu từ bản ghi hiển thị (+chế độ camera 0x24, mục tiêu ban đầu +0x54/58/5C, hướng +0x7E) và đồng bộ hóa at.x/at.y; `801C685C` ở cuối mỗi khung `D_80250228 += D_80250240` (tốc độ x) và đặt ở giá trị Ghi làm giá trị đích. Bốn chế độ máy ảnh được bộ xử lý chọn thông qua `801C67EC`: 0 → `801C63BC`, 1 → `801C64D8` (các giá trị bất hợp pháp cũng lấy nó), 2 → `801C6584`, 3 → `801C6678`; họ đọc mã điều khiển được theo dõi (+0x894 của người tham gia 0 = `D_800FA074`, chế độ 3 đầu tiên theo sau +0x78 = `D_800F9858`), ghi −2× hướng vào +0x20 và đăng ký `D_80250220` (khe)/`D_80250252` (hướng) qua `801C637C`. Suy luận: Sự khác biệt duy nhất giữa bốn chế độ là ai sẽ theo dõi và có phát `801C63A8` trước hay không.
- `801C9DD0(a0)`: a0 là phần xử lý của +0x78 {+0 số vị trí, +0x32 hướng} trong bản ghi tham gia chiến tranh (`D_800F97E0` + idx×0x1074) và điểm gọi là `801C7F78/801C8120/801C81F4`. Nó di chuyển khe về phía mục tiêu với tốc độ (đích − vị trí)/8 (ghi +28/2C/30, x cộng với 2×hướng), |dx| < 3 trả về 0, đó là "máy ảnh tại chỗ" cho trạng thái 21, v.v.
- Hoán đổi bên `801C7E1C` chỉ trao đổi `D_80178C78`↔`D_80178B50`, đặt lại vị trí các họa tiết (`801C40E0`×2, `801C39B0`×2) rồi điều chỉnh `801C685C`; **Không có gương ma trận**, trái và phải đều là ±800 Các byte vị trí và hướng được xác định (suy ra).

## 5. Màn hình rộng: Hiện trạng và phần còn lại

Đã thực hiện (2026-09-29/30, `deck-16x10.md` Điều 13/8): Bầu trời được vẽ thêm hai lần ở ±320, khung nhìn 3D không còn được căn giữa (mặt đất, thân máy và các hiệu ứng đặc biệt được mở rộng với khung nhìn), dải mặt nạ được để trống và HUD được viền. Theo phân tích này, các rủi ro mã hóa cứng còn lại:

1. **Khía cạnh chiếu đến từ 320/240** (`800883FC` đọc `D_8010F5C0/C2`). Giờ đây, khung nhìn mở rộng của RT64 đang được nới lỏng, bản thân hình học vẫn được tính là 4:3 và các phần bổ sung ở cả hai bên là những phần đã được cắt ban đầu, đó chính xác là những gì mong muốn; miễn là `D_8010F5C0` không bị thay đổi.
2. **Phạm vi của mô hình mặt đất**: 3 khối × 1000·s (tỷ lệ mẫu 1,0 hoặc 1,5, ROM `0x5A988`), khoảng cách mắt 260, góc nhìn 50°, gần 20 giờ 16:9, trường nhìn khoảng ±(260+z)·tan25°·1,78, suy luận là đủ; nhưng một mặt đất duy nhất <5608 (chỉ Cạnh ngoài của 1 nút) và mối nối 9 nút có thể bị lộ ở tỷ lệ 21:9 hoặc khi máy ảnh được thu nhỏ. Vui lòng kiểm tra hình ảnh thực tế của máy bằng hình ảnh.
3. **Lớp hiệu ứng đặc biệt cuộn** `801C3610` (khe 0x19, chế độ 2) được mô phỏng ở mức 320 giống như bầu trời. Lần sơn lại ±320 hiện tại chỉ được treo trên "`80095974` trong khi chiến đấu" - nếu lần sơn lại được lọc theo vị trí thì cần phải bao gồm vị trí 0x19 (cần được kiểm tra `host.cpp` Điều kiện số 434 gần hàng).
4. **Lớp bầu trời thứ hai** (khe 3/4, 14 bản ghi) sử dụng cùng một trình kết xuất, lẽ ra phải được che lại nhưng chưa được triển khai trong máy thực tế.
5. The **cut-in mask** is the four black rectangles programmed with 320 in the resident static list `800C6D00` (§6.3): the upper and lower blocks will be filled up by RT64, and the left and right blocks (0,45)-(90,165), (230,45)-(320,165) will only cover the middle 4:3, after widening, the performance screen will be lộ ra cả hai bên, còn các phần bên trái và bên phải phải tính toán lại theo chiều rộng của màn hình (cửa sổ vẫn được giữ ở giữa). Bản thân hình ảnh cut-in được căn giữa với camera x và không cần phải di chuyển. The actor type 0x90/0x93/0x9C in mode 0xB (screen coordinates TEXRECT) in `801C50D8` has not been matched yet, and it is also centered at 4:3.
6. **Hình chữ nhật toàn màn hình**: Có 4 `F6` và 2 `FA` (flash, mặt nạ) trong lớp phủ. Quy tắc "hình chữ nhật có chiều rộng tối đa" RT64 đã được áp dụng; nếu có một dấu nháy được vẽ bởi (0,0)-(320,240) trong quy trình hành vi, nó sẽ được điền theo cách tương tự, xem §6.
7. **Screenshake** là chuyển vị 3D được chồng lên at.x và không cần xử lý sau khi thư giãn.

## 6. Thói quen hành vi và hiệu ứng màn hình

### 6.1 Quy trình hành vi của diễn viên

- **Bảng**: `80220C0C(behavior)` Sử dụng hành vi − 3 để kiểm tra `jtbl_80225030` (380 mục hợp lệ, hành vi 3–382; chỉ số dưới ≥ 0x17C và 9 mục cuối cùng thuộc về `802219A0`). Mỗi mục là một đoạn 12 byte và trả về quy trình thực; `80221988` (được chia sẻ bởi 95 mục) là **vị trí trống** của `v0 = 0`. Nó nhận được giá trị NULL khi tải và `801C5BAC` bị bỏ qua. 284 thủ tục hợp lệ. ROM `0x21AE0C` có danh sách người chỉnh sửa trong thời gian phát triển. Chỉ những biên tập viên cao cấp mới có thể sánh được với nó (359 Stay, 362 Shield, 367 CoverDiffence, 375 BeamShield, 379 Dummy). Người ta suy ra rằng chúng còn sót lại từ các phiên bản khác nhau.
- **Quy ước gọi** (`801C5BAC(block)`): Tác nhân ghi 0x50 byte, trong khối+0x9C+i×0x50, khối lượng+0x26; khi khối byte pha+0x25 chứa 0x40 hoặc diễn viên+0x2E == 4 (khung đầu tiên) `jalr *(+0x4C)(a0 = 演员)`, giá trị trả về sẽ bị bỏ qua. Không có số lượng khung ở mức khung, mỗi quy trình sử dụng +0x44 (205 quy trình), trạng thái phụ +0x3C, phụ trợ +0x3E/40/42. Các trường: +0 khe elf, +2 căn chỉnh, +8/C/10 cơ sở xyz (cờ không đổi z), dịch chuyển tích lũy +14/18/1C, tốc độ +20/24/28 (tích lũy trên mỗi khung), +2C số đăng ký, hướng +32 ±1, +34 h4, +36 hoạt động, chế độ +38 (1/3 = tọa độ tuyệt đối, nếu không thì được xếp chồng lên sprite máy chủ +4..C Với tốc độ +28..30), +3A h5 → sprite +0x35, con trỏ byte pha +48.
- **Phân loại theo các chức năng phụ trợ được sử dụng** (một quy trình có thể thuộc nhiều danh mục): vị trí/tốc độ `801C6038` 136 (bao gồm 14 sử dụng sinf/cosf); khoảng cách máy chủ tương đối `801C32D4` 44. Tìm diễn viên đồng hành `801C58E8` 16; chia tỷ lệ (viết sprite +10/14/18) 21; lật `801C3BE0` 67; hiển thị và ẩn `801C37FC/3840` 274; hiệu ứng âm thanh `801C355C` 188 (`8008FFAC` 10); thay đổi cảnh `801C5700` 232. thay đổi tập bản đồ/bảng màu `80098204/590/604` 51; ghi byte pha (kích hoạt nhấn Script/Concatenation) 273; camera theo dõi `801C637C`/hủy `801C63A8` 16; đèn flash toàn màn hình `801C9520/95CC`, `8009AC84` 41; hiệu ứng bảng sprite `801C963C` 38 (chế độ 4 có 73, 1 có 32, 9 có 9, 3 có 4, 2 có 3, 6 có 1); nền bị ẩn/khôi phục `801C3C40/3C64` 23. Quá tải nền `801C28E0` 17; nhịp sát thương `801C8DFC/8A44` 9; chương trình con dẫn xuất `80220C0C/801E4668` 13; yêu tinh phòng thủ `801C4574` 3; cắt vào 5; end(`sb 0, 0x36`) 279. Thể hiện: `801E4E20` chế độ chờ chụp, `801EB410` tia, `801E6064` định giờ, `8021F5A4` lá chắn, `8021FB4C` hỗ trợ, `80220734` vụ nổ.

### 6.2 Hiệu ứng toàn màn hình

- **Fade/Flash** là bản ghi 3 lớp thường trú `D_800FF9D8 + 16n`: `8009AC84(层, 类型, R, G, B, 目标 α, 间隔, 步长)` ghi, `8009AFCC` bước trên mỗi khung hình (loại 1 `8009AD64` α dừng sau khi tiếp cận mục tiêu; loại 2 `8009AE9C` Tự động ẩn sau một hoặc hai khung hình, được suy ra là đang nhấp nháy), bản vẽ `8009A954`: SETCOMBINE + `FA` PRIM + **`F65003C0 00000000` tức là (0,0)-(320,240) FILLRECT mã hóa cứng** (ROM `0x25358–0x2536C`), mức độ ưu tiên của nút 0x9D/0x83/0x9B. Lớp vỏ cho lớp phủ: `801C9520(层, 白?, 目标 α, 步长)` gradient trắng/đen, `801C95CC`/`801C94A0` lớp 1 màu đen α250 loại 2. Hình chữ nhật có chiều rộng đầy đủ được lấp đầy bởi RT64 và màn hình rộng được che phủ.
- **Chặn**: `801C2C3C` sử dụng `8008A5C4(0x85, 4, 0, 0x00222D50)` để đăng ký danh sách tĩnh đã bị `battle_hud.cpp` làm trống.
- **Lắc**: Không có hiện tượng rung ngẫu nhiên trong lớp phủ; nguồn gốc cuộn `D_8015DDF0/DDF4` chỉ được viết bởi `801C2600/32D4/6224/685C/7494/840C`. Phân tích đầu tiên cho thấy `801C9AE0` chồng cư dân `D_80178D44/D48` vào x. Có thể suy ra rằng mức độ rung do tập lệnh bản đồ (3D36) để lại vẫn tiếp tục trong quá trình thực hiện. Nó sẽ được xác nhận bởi máy thực tế xem nó có thực sự hiệu quả hay không.
- **Đèn flash khi nhấn không phải toàn bộ màn hình, cũng không phải PRIM**: `801C87C8` Khi nhấn, tông màu là `801C963C(演员, 0, 颜色, 模式 4)`, màu là RGBA5551 (trắng 0xFFFF, đỏ 0xF801, xanh 0x3F) → `80099C88` thay đổi **bảng màu của sprite** (chế độ 1 = thay đổi tài nguyên bảng màu khác, chẳng hạn như 0xBB4; chế độ 4 = thay thế toàn bộ màu sắc), trong khi `801C94A0` kích hoạt đèn flash màu đen lớp 1.

### 6.3 cắt vào

Không phải chế độ đặc biệt, **diễn viên thông thường**: Số đăng ký 984–1038, hành vi 240 `801FBE3C` (37 địa điểm), 350 `80211378`, 351/352, 373 `8021F3C0` (h6 = 2 để điều khiển, 14 vũ khí). Hiển thị sau pha bằng nhau == h4, chuyển cảnh sang mục đăng ký này, tỷ lệ sprite 1,29, tọa độ tuyệt đối chế độ 1 x = `D_80250228` (ống kính x, tâm màn hình) y = 47 (hằng số trong `801FBE5C`/`8021F3E0`); ghi giai đoạn 0x56 sau khi hoạt ảnh được phát. Không có mã trượt và tất cả các hiệu ứng hoạt hình đều có trong khung cảnh. Khi tác nhân z == 1 `8009C68C(0x35)` → `8008B4F4(…, 0x8E, 0x000C6D00)` treo danh sách tĩnh thường trú (RAM `800C6D00`, ROM `0x516F0`): FILLRECT đen (0,0)-(320,45), (0,165)-(320,240), (0,45)-(90,165), (230,45)-(320,165), **Để lại cửa sổ 140×120**; `8009C6C8` đã bị xóa. Hình ảnh là một sprite 128×96 (55 cảnh, 27 tập bản đồ, bao gồm tập bản đồ lớn loại 6 512×448), không phải là hình ảnh toàn màn hình.

### 6,4 Xuống

Trạng thái 22 `801C818C`: Bản ghi nội dung `801C30D0(unit, 6) == 2` (30 đơn vị) chọn lần truy cập 156, nếu không thì +0xD của `801C49A0` == 2 → 157, nếu không thì 158; `801C84C0` đang tải; giai đoạn 0x56 giải phóng/ẩn sprite, 0x57 trở về trạng thái 0x15. Cả ba kịch bản đều có 7 diễn viên, hành vi 382 `80220734` (`801C6038` bay, `801C95CC` đèn flash đen, `801C963C` đổi màu), cảnh cháy nổ 1042 (128², 11 khung hình), 1043 (192²), 1044 (176²), 1045 (192×176). `801C9DD0` Để chiếc máy bay bị bắn rơi di chuyển 1/8 đến gần tâm máy ảnh hơn trong mỗi khung hình. Vụ nổ = sprite + đèn flash toàn màn hình, không có đồ họa vector.

### 6,5 thanh HP và lượng sát thương

Hàng đợi `D_80250270` được tạo bởi `801C8A58` (trạng thái 1 `801C70A8`/14 `801C7FC4`) bằng hồ sơ vũ khí [5] kiểm tra `D_80222E50`. `801C87C8(0x45, 0x45)` được bộ xử lý trạng thái điều chỉnh trong mỗi khung hình: pha 0x45 và `D_80250488 == 0` bắt đầu, `801C8D04` bật lên một bước → `801C8D6C` ghi giá trị không xác định để hiển thị HP (bản ghi chiến đấu +0x22, suy ra), bộ bảo vệ flash, đèn flash đen; quy trình cũng có thể là `801C8DFC` Nâng cao (5 vị trí), `801C8A44` bộ `D_80250490 = 200` (được coi là tính giờ kỹ thuật số). `801C2C98` (đăng ký `801C728C`) vẽ các thanh rộng 88 ở mức +0x22/+0x20 trên mỗi khung: x 44–132/184–272, y 29–31 (const ROM `0x121C0C–0x121E30`), đã bị ràng buộc bởi `battle_hud.cpp` với cửa sổ HP.

## 7. Đánh giá lộ trình HD

Cả hai tuyến ứng viên đều không cần chạm vào lớp phủ:

### 7.1 Thay thế băm kết cấu RT64 (như biểu tượng nội dung bản đồ)

- Key: Nội dung TMEM của LOADTILE một lần cho mỗi phần (bao gồm cả các mục TLUT đã sử dụng). 18398 lát khác nhau; các bảng màu khác nhau (màu của quân bạn và màu của kẻ thù) trong cùng một tập bản đồ được tính là các phím khác nhau. Băm RT64 v5 chứa TLUT, điều này được xác minh trên biểu tượng.
- Ưu điểm: Không cần tái tạo bất kỳ phép biến đổi nào, ma trận, gương, alpha và mức độ ưu tiên đều nguyên gốc; màn ảnh rộng theo sau một cách tự nhiên.
- Khó khăn:
- **Đường may**: Các bộ phận được lấy mẫu độc lập ở kích thước 32×32. Sau khi hình ảnh HD được nhân lên 8 lần, các kẹp song tuyến tính lần lượt được kẹp ở các cạnh của các lát cắt và các đường mảnh sẽ xuất hiện ở các khớp nối (vấn đề về đường nối câu đố đã gặp phải trên bản đồ thế giới). Để thêm 1–2 pixel của nội dung khối liền kề vào lát HD để đệm, hãy cắt toàn bộ khung theo khung chính khi xuất.
- **Hoạt hình bảng màu** (§5.4, `8009A358` viết lại dữ liệu bảng màu trong mỗi khung hình, `80098604` thay đổi toàn bộ trang tính) sẽ khiến hàm băm TLUT thay đổi theo từng khung hình và các sprite bị ảnh hưởng phải có khóa cho từng trạng thái, nếu không nó sẽ quay lại hình ảnh gốc. Trước tiên cần phải đếm xem mục đăng ký nào có bản ghi hiệu ứng bảng màu (bản ghi phụ +1E..+2A).
- Áp dụng tương tự cho 4 hiệu ứng đặc biệt của bảng màu 592 màu.
- Áp dụng cho: thân máy, hầu hết các hiệu ứng đặc biệt của vũ khí và vụ nổ.

### 7.2 Lưu trữ bản vẽ toàn khung (như ảnh đại diện, ảnh tiêu đề)

- Đã có nền tảng: trình bao bọc máy chủ của `resident_func_8009761C` và `native_sprite.cpp` bằng bản ghi phụ +12/14/16 nhận dạng xử lý (cảnh, tập bản đồ, bảng màu), đọc +19 cách tiếp cận bước hiện tại.
- Cần tái tạo trên máy chủ: ma trận nút +14 (**chỉ đọc trực tiếp bộ nhớ, không cần tính toán lại `8008261C`**), phối cảnh `8015DCAC` và xem `8010F71C` và cờ nút 8, bit gương +1C/`800FFAC0`, alpha +1, bước → khung → Lắp ráp các bộ phận, thứ tự ưu tiên (thay thế xảy ra tại vị trí nút ban đầu, giữ nguyên trật tự tự nhiên), bảng màu hiệu ứng (chỉ cần đọc dữ liệu bảng màu hiện tại và toàn bộ khung được tô màu lại).
- Ưu điểm: Một hình ảnh HD trên mỗi khung hình, không có đường nối; hoạt ảnh bảng màu có thể được ánh xạ lại trên máy chủ theo TLUT hiện tại; bản vẽ có thể lớn hơn khung vẽ gốc (nên hạn chế mở rộng các hiệu ứng đặc biệt, xem [[srw64-hd-effect-keep-footprint]] để biết bài học).
- Độ khó: Một khung hình phải được xác định theo (cảnh, tập bản đồ, bảng màu, số khung), 3905 khung hình × phối màu; tứ giác theo phối cảnh phải sử dụng cùng một hình chiếu như RT64 (hình ảnh tiêu đề chế độ 14 hiện có đã trải qua quá trình chuyển đổi ma trận và có thể được sử dụng lại).

### 7.3 Gợi ý

- Phần thân và các hiệu ứng đặc biệt được ưu tiên **7.1**: Xuất nhanh, không rủi ro, quay lại ảnh gốc, trước tiên sử dụng công thức ESRGAN (`unit-pose-hd.md` đã hoàn thiện) để phóng to toàn bộ bộ 527 ảnh 8 lần, sau đó cắt theo các phần và thực hiện đệm; các họa tiết của hoạt ảnh bảng màu được loại bỏ trước tiên và sau đó được hoàn thiện sau khi thống kê.
- Bầu trời, kết cấu mặt đất, hàm băm RT64 trên bầu trời đầy sao + bầu trời có thể được tạo bằng cách mở rộng bên ngoài (phương pháp tương tự như nền liên trường `background_wide.py`).
- Cut-in (55 cảnh, 27 tập bản đồ, canvas 128×96, khoảng 165×124 sau khi phóng to 1,29) và nổ (4 cảnh) **7,2**: số lượng ảnh lớn nhỏ, không cần lo lắng về hoạt ảnh bảng màu, chất lượng hình ảnh toàn khung đạt được là lớn nhất; khung mặt nạ cut-in được tính toán lại theo chiều rộng màn hình.
- **Nhấp nháy khi nhấn và các biến thể khớp màu trước tiên**: `80099C88` Chế độ 1 (thay đổi tài nguyên bảng màu) và chế độ 4 (thay thế toàn bộ màu) hoạt động trên bảng màu sprite. Cả hai tuyến phải có khả năng đổi màu theo TLUT hiện tại - tuyến băm là khóa cho từng trạng thái màu (trắng/đỏ/xanh × màu chính) và tuyến máy chủ đọc bảng màu hiện tại để ánh xạ. Trước tiên, hãy sử dụng đầu dò chỉ đọc để đếm số lượng trạng thái TLUT xuất hiện trong một trận chiến điển hình trước khi đưa ra quyết định.
- Nếu bạn muốn thay đổi hình dạng của mô hình mặt đất 3D, hãy làm theo lộ trình thay thế mô hình của `native-model-replacement.md`.

## 8. Được xác minh trên máy thật

- Các loại tác nhân ở chế độ 0xB trong `801C50D8` (0x90/0x93/0x9C) là gì?
- Mức độ rung của `D_80178D44/D48` có thực sự gây ra dịch chuyển trong quá trình biểu diễn hay không.
- Tính toán lại và hiệu ứng thực tế sau khi khung mặt nạ cut-in được nới lỏng.
- Mép ngoài mặt đất 9 nút tỷ lệ 16:9/21:9; danh sách cấp độ cho mặt đất đơn (<5608).
- Liệu bản vá ở khe lớp cuộn 0x19 có bị ghi đè bởi bản vá bầu trời hiện có hay không.
- Danh sách các mục đăng ký được bao phủ bởi hoạt ảnh bảng màu (chỉ cần thêm đầu dò chỉ đọc vào `80099C88`).
- Mối quan hệ giữa gần 20/xa 3000 và tốc độ tiến vào của máy bay dưới khung nhìn mở rộng RT64 (16:9 là khoảng 54 đơn vị, được quan sát).

## 9. Bản đồ mô hình mặt đất HD thí điểm (30-09-2026, thành phố, máy thật đã qua)

Cảnh: Bản ghi nền 58 (khối 0, địa hình 58), mặt đất 5836 (mặt biển) + 5837 (tòa nhà, tàu chở hàng, bến tàu) + 5838 (lớp tiền cảnh), bầu trời 6087. Sử dụng phương pháp `check_battle_backgrounds.py` để viết `800F97EA/B` (mỗi bên một bản) trong cấp độ nhỏ `battle-ui` trước khi bắt đầu trận chiến để ép nền. Thư mục làm việc `assets/hd-ai/battle-backgrounds/test-1` (không nhập git):

1. `run_battle_bg.py OUT 块 地形 --dump`: Chạy trò chơi có kết cấu RT64 và ghi lại 180 kết xuất TMEM mới xuất hiện sau khi chiến tranh bắt đầu.
2. `decode_dumps.py 5836 5837 5838`: Nhấn `tile.json` để giải `.tmem` (CI4/CI8, hai từ được hoán đổi cứ sau 8 byte trong các dòng đánh số lẻ, bảng màu là 8 byte cho mỗi mục bắt đầu từ 0x800) và so sánh từng pixel với bản đồ được giải quyết bởi trình xem mô hình. Tất cả 16 bản đồ của ba mô hình đều được so khớp từng cái một và hàm băm là chìa khóa cho RT64.
3. `upscale.py`: Mở rộng 16 pixel theo phương pháp gói của họa tiết (gạch lát lặp lại, ép cạnh), sau đó trộn đôi UltraSharpV2+PixelPerfectV4, 4 lần, cắt lại; đi qua alpha một lần nữa với độ trong suốt. Viết gói kiểm tra, liệt kê `art.json` (loại tạm mượn `space`) và hồ sơ chỉ chứa 16 ảnh này.
4. `run_battle_bg.py OUT 0 58 --profile profile.json`: Ảnh chụp màn hình thực tế của cùng một trận chiến.

Kết quả: Các tấm sàn, tàu chở hàng, tay cần cẩu đã trở nên thông thoáng hơn đáng kể, các mối nối ngói không còn xuất hiện; kết cấu mặt biển ban đầu là một gợn sóng mịn màng, ít thay đổi. Sky 6087 là bản đồ khối 2D, không nằm trong phạm vi này. Nó vẫn là khối màu hoà sắc của phiên bản gốc. Nó dễ thấy hơn đằng sau những tòa nhà rõ ràng, vì vậy nó nên được thực hiện cùng nhau.

Vẫn chưa có quyền truy cập chính thức: `compile_art` đã được thêm vào danh sách trắng danh mục (hiện chỉ có bản đồ thế giới/khung/dấu cách/biểu tượng); khóa của tất cả 442 mô hình có thể được tính trực tiếp từ các tính toán tĩnh tài nguyên theo giải pháp `decode_dumps.py` mà không cần dựa vào kết xuất (`rt64_hash.py` đã có thuật toán CI4 64×64 và cần được CI8 bổ sung với các kích thước khác), sau đó sử dụng một kết xuất nhỏ để kiểm tra tại chỗ.

## 10. Thí điểm lưới HD mô hình mặt đất (30-09-2026, thành phố 5837, đã qua máy thực tế)

Các thay đổi máy chủ (mô hình nướng, đổ bóng mặt nước) và các công cụ tạo mô hình ở Phần 10 và 11 vẫn chưa được gửi và chỉ được thử nghiệm cục bộ. Người dùng đã từ chối thực hành một bản đồ nướng 40962 cho mỗi mô hình và chuyển sang vật liệu có thể xếp được + đỉnh AO để sản xuất hàng loạt.

§9 Chỉ có các nhãn dán được thay đổi, nhưng tòa nhà vẫn là nhãn dán đó. Phần này thay thế toàn bộ 5837 bằng một lưới mới và sử dụng mô hình gốc của tàu bản đồ thế giới ([native-ship-model.md](../native/native-ship-model.md)):

- **Nhận dạng được thiết lập trong chiến đấu**: Mô hình mặt đất và tàu có cùng định dạng tài nguyên (bảng mô tả + danh sách hiển thị mô hình loại 0) và phân đoạn 4 cũng được đặt khi trò chơi được gọi; danh sách 5837 chỉ có lệnh tam giác (227 mục), không có chuyển đổi ma trận và danh sách con. Máy chủ truy cập từng khung hình và mỗi khối trong số ba khối ghép nối (x −1000/0/+1000) được rút ra một lần. Bản vẽ ban đầu được sử dụng để kiểm tra độ sâu và viết độ sâu. Nhấn F6 để quay lại bản vẽ ban đầu. Trước tiên, hãy sử dụng lưới giữ chỗ được chuyển đổi từ hình học ban đầu sang màu đỉnh để xác nhận, sau đó thay đổi thành lưới chính thức.
- **Sự thật về mô hình ban đầu**: "Thành phố" ở phía xa là một bảng kết cấu thấp tầng rộng 1000 mét (z −500, y 17..77) cộng với hai bảng kết cấu cao tầng (z −475, từ trên xuống y 147); phía xa là bệ bến (y 26) và tường bến, tàu khách màu trắng "Yokohama Maru" và tàu công tác thân đen (cần cẩu cửa, cần cẩu màu đỏ và trắng).
- **HD Grid**: Tập lệnh Local Blender `battle_city_blender.py` (không vào kho, xem `assets/models/generators/`; Blender 4.3 chạy không đầu, xuất ra `assets/models/battle-city/mesh.json`, không nhập git). 7.3 Hàng nghìn hình tam giác, màu đỉnh: trụ cầu có khớp nối tường bến, chắn bùn, cột chắn, cây xanh, đèn đường; ba dãy nhà (lõi kính tháp văn phòng + tường ngăn cửa sổ mỗi tầng + pilaster + thiết bị mái, ban công và lan can từng tầng của tòa nhà chung cư, cửa sổ dạng dải của tòa nhà văn phòng trung tầng), vị trí, chiều cao ban đầu của hai tòa nhà cao tầng được giữ nguyên; Hai con tàu được xây dựng lại theo các hộp giới hạn ban đầu và đường viền thân tàu (cấu trúc thượng tầng nhiều lớp của tàu chở khách, dải cửa sổ, xuồng cứu sinh, ống khói, lưới văn bản tên tàu; giàn cần trục cửa tàu, container, nhà boong, cần màu đỏ và trắng). Chỉ xây dựng mặt phẳng +z và các cạnh mà máy ảnh có thể nhìn thấy. Hàng nghìn ô vuông được ghép thành một lượng nhỏ bmesh theo màu sắc rồi gửi về Kit để xuất.
- **Bao bì**: Thêm 5837 mặt hàng vào bảng mẫu của `build_native_models.py`; `--output build/recomp/native-models/battle-city-test`, `SRW64_NATIVE_MODELS` trỏ tới nó (`test-1/run_battle_bg.py --models`) khi chạy.

**Nhìn và Cảm nhận**: Các tòa nhà có độ nhấp nhô sàn thực và mức độ từ trước ra sau, có thị sai khi lia máy ảnh, và các chi tiết về tàu khách và thuyền làm việc nhiều hơn so với phiên bản gốc. Màu tàu của chủ nhà (màu đỉnh + đèn phím cố định) xám hơn bản đồ gốc và các tòa nhà dày đặc hơn bản gốc; màu sắc và mật độ phải được điều chỉnh theo các tòa nhà màu trắng sáng của bản gốc.

**Mô hình bầu trời không di chuyển**: Bầu trời là hình ảnh khối 2D của Chế độ 2 và chức năng vẽ tương tự như nền liên trường là `80095974`; việc thay thế toàn bộ hình ảnh của `native_background.cpp` được xác định bằng số tài nguyên của bản ghi phụ (hình ảnh, bảng màu), bất kể chế độ nào, vì vậy bầu trời chiến đấu (cảnh này 6087/6145) chỉ cần tạo toàn bộ hình ảnh HD và đăng ký nó vào danh sách nền. Bầu trời được quay theo chiều ngang 320 độ, hình ảnh HD phải được vẽ sao cho hai bên trái và phải liền mạch, hai bên màn hình rộng được bao phủ bởi các hình ảnh lấp đầy ±320.

**Khối lượng công việc cần dàn trải**: Hầu hết trong số 442 mô hình mặt đất là tấm nền và một lượng nhỏ cảnh quan. Những thứ thực sự đáng để xây dựng lại lưới là các thành phố, di tích, căn cứ, cầu và rừng với phong cảnh (khoảng hàng chục tài nguyên) và phần còn lại chỉ có kết cấu (§9). Một tài nguyên yêu cầu tập lệnh Blender dài khoảng 400 dòng.

## 11. Mô hình chiếu sáng nướng và mặt nước thời gian thực (30-09-2026, thành phố, máy thật đã qua)

**Chưa được phát hành** (2026-10-01 người dùng: "Chưa muốn cái này"): Mã máy chủ được giữ lại và nhà đóng gói `build_native_models.py` đặt ba mục này vào `BATTLE_BACKGROUNDS`. Gói HD không được bao gồm theo mặc định. Bối cảnh chiến đấu của 0.3.2 vẫn là phiên bản gốc; bản dựng cục bộ `SRW64_BATTLE_BACKGROUNDS=1` được nhập.

Lưới màu đỉnh của §10 được người dùng đánh giá là "không đủ độ phân giải cao": bóng tàu chủ chỉ có màu đỉnh cộng với ánh sáng cố định, không có họa tiết, phản chiếu hoặc che khuất xung quanh. Đã thay đổi thành hai đường ống mới:

- **Mô hình chiếu sáng nướng** (`shading: baked`): Tập lệnh cục bộ `battle_bake.py` kết hợp các phần của tập lệnh mô hình thành một đối tượng, gán vật liệu theo tên màu (kính được sáng và tối ngẫu nhiên theo từng ô, tiếng ồn của bê tông và đường, độ bóng bán phần của thân tàu), thêm bầu trời và mặt trời Nishita, xóa bề mặt phía sau và phía dưới mà máy ảnh không bao giờ có thể nhìn thấy và sử dụng Chu kỳ sau khi mở rộng Smart UV (GPU kim loại, 128 mẫu, khoảng 70 giây) để tổng hợp ánh sáng tổng thể, bóng tối, ánh sáng bầu trời và phản chiếu vào bản đồ 4096². Lưới có 46.000 hình tam giác, Mesh.json v2 với uv và kết cấu; kính tiêu chuẩn vertex color alpha 200. Máy chủ `HdBakedVS/PS.hlsl` trực tiếp lấy mẫu kết cấu (mip, tuyến tính) và kính được xếp lớp với một lớp Fresnel bầu trời và làm nổi bật tùy theo góc nhìn.
- **Mặt nước thời gian thực** (`shading: water`): Thực tế có hai lớp nước, 5836 là mặt phẳng và 5838 là lớp sóng bao phủ toàn bộ mặt đất (y 3..14). Thứ hai là nước bạn nhìn thấy. 5838 Mặt phẳng lưới (y 6) do trình đóng gói tạo ra tiếp quản, 5836 được đặt thành `hidden` (tất cả các hình tam giác đều bị chặn và không được vẽ). `HdWaterPS.hlsl`: Độ dốc của 16 sóng định hướng được tổng hợp thành một đường bình thường, thành phần x của vectơ sóng là 2π·số nguyên/1000 và ba đường nối thẳng hàng; màu nước sẫm và độ dốc của bầu trời được trộn lẫn theo Fresnel, mặt trời xuống thấp về phía thành phố, tạo thành dải chớp; khoảng cách mờ mịt đến tận chân trời; thời gian được lấy từ đồng hồ chủ.
- **Thay đổi máy chủ**: mô hình của `native_marker.cpp` thêm `Shading` (màu/nướng/nước/ẩn), kích thước bước đỉnh theo loại (28 hoặc 36), họa tiết bị ràng buộc sau khi tải lên khi vẽ lần đầu; dữ liệu bổ sung cho mặt nước là ma trận khung nhìn mô hình và thời gian. `native_gpu.cpp` Đăng ký HdBaked, HdWater. Trình đóng gói `build_native_models.py` hỗ trợ lưới uv, sao chép kết cấu và tạo lưới mặt nước.

**Máy thật** (`test-1/water2`, cửa sổ 1280×720): 5837, 5838 mỗi lần rút 1389 lần, 5836 tất cả bị chặn. Thành phố sáng sủa, có nhiều ánh sáng và bóng tối, các ô cửa sổ xen kẽ giữa ánh sáng và bóng tối; mặt nước có gợn sóng động, phản chiếu của bầu trời và dải đèn flash. Vẫn là bản gốc: hình ảnh bầu trời 2D (thay thế toàn bộ hình ảnh trong §10 bằng HD ở bước tiếp theo), các họa tiết cơ thể và hiệu ứng đặc biệt.

Cần điều chỉnh: vị trí của dải đèn flash (hướng của mặt trời là giả định cố định), lựa chọn giữa màu nước sâu và màu xanh bão hòa ban đầu cũng như phối cảnh trên không của các tòa nhà ở xa.

## 12. Thân chiến đấu được thay thế bằng kết xuất HD hiện có và phối cảnh dưới nước (30-09-2026, máy bay thực tế đã qua)

**Đơn vị**: Bộ ba cảnh được sử dụng cho phần thân chính của máy bay trong trận chiến giống với hình ảnh phần thân lớn trên trang (`unit_poses`). Nó là một khung đơn và được vẽ theo ranh giới cảnh. Có thể thay thế trực tiếp bức tranh dọc HD hiện có (`unit-poses/whole-v1`, 8 lần, 332 ảnh). Việc thay thế toàn bộ khung hình của hình ảnh cảnh `native_sprite.cpp` ban đầu được treo trên trình kết xuất tứ giác (được sử dụng cho ảnh tiêu đề), được xác định bởi (cảnh, tập bản đồ, bảng màu, khung) và sử dụng ma trận của trò chơi để vẽ toàn bộ bức tranh; bây giờ `configure` đọc `srw64-units-hd.json` trong gói nghệ thuật cùng lúc và mỗi bức ảnh được đăng ký làm khung 0. Gương ban đầu sẽ lấy tập đỉnh thứ hai của bộ phận. Khi thay thế toàn bộ hình ảnh, việc lật được đánh giá dựa trên tọa độ S của các đỉnh ngoài cùng bên trái và ngoài cùng bên phải của phần đó. Khi lật, tia UV trái và phải được hoán đổi. Danh sách này đã tồn tại trong gói HD chính thức, vì vậy không cần thêm tài nguyên và nó sẽ có hiệu lực trong các trò chơi thông thường; F6 trở về phiên bản gốc.

Máy thực tế (`test-1/units`, `pairs`): MINUEP ォー (2365/1765/2065) và ダンバイン (2438/1841/2141) đã được thay thế, đồng thời kích thước và hướng cũng nhất quán với phiên bản gốc.

Không được bảo hiểm:
- Cùng một máy có các bảng màu khác nhau: 11 bộ giống nhau (cảnh, album) với nhiều bảng màu trong `unit_poses` (chẳng hạn như ギラ・ドーガ 91/315, バウンド・ドック 105/317/318) mỗi bộ đều có Tư thế đứng HD; バストール Các sơ đồ đã giải của 2953 và 2144 giống hệt nhau đến từng pixel và cũng đã được che phủ. 5 đăng ký thay đổi màu trong `battle_scenes` chỉ được sử dụng cho các màn trình diễn vũ khí (xác minh tĩnh 2026-10-02): 675/676 (Loạt phim Mascuit "锔 Dance・Reappearance Jianghu デッドリーウェーブ", vũ khí 111/120, đỏ và cam), 862 (ヴァルディスキューズ 「スピリッツクラッシュ」1248, màu xanh), 863 (アヴィエスレルム 「オ"メガクラッシュ" 1253, thay đổi màu mắt), 864 (スーパーアースゲイン "Explosive Axe Unparalleled Break" 1177, màu xanh), là một dư ảnh/doppelganger (hành vi) của sự thay đổi màu tổng thể 314;272 7 mỗi màu, h5 tăng 50–230), bắt nguồn từ §13 "Thay đổi màu sắc hoặc ánh sáng toàn cầu" và được đóng gói với `unit_extras` (bảng màu 2997/2998/2992/2993/2994). Do đó, tất cả các biến thể màu sắc của thế đứng của cơ thể đã được che đậy. **Đánh giá thay đổi màu sắc (2026-10-02)**: Một số sơ đồ thay đổi màu thuần túy dựa trên tỷ lệ màu bị mờ và thiếu chi tiết (các đường khối của mắt, đá quý và MASK 2997/2998 chuyển sang màu xanh ô liu) và được thay đổi thành bảng tra cứu màu: `unit_extra_derive.py``PALETTE_SWAPS`／`palette_swap` Chọn màu mục tiêu phổ biến nhất cho mỗi thế đứng màu nơi khung ban đầu trùng với thế đứng. Mỗi pixel HD được tính trọng số và thay đổi theo màu sắc của 4 trạng thái cuối cùng. Những nơi có tư thế nhưng không nằm trong khung sẽ được loại bỏ bằng mặt nạ có viền mềm. Hiện đang được sử dụng cho 8 tờ: マスターガンダム 2997/2998 (màu gốc khớp 1935), ゴッドガンダムH gold 2485,スーパーアースゲイン2901, アヴィエスレルム 2928, ヴァルディスキューズ 2934,ヴァイローズ tím 2862, スヴァンヒルド 2809. Đối với những người có linh kiện mới (nòng súng của Masukura S 2758, khoang tên lửa của Sagittarius 2802) thì các linh kiện đó sẽ bị mất khi tra cứu bảng, và dẫn xuất ban đầu vẫn sẽ được tuân theo. Trong `unit_poses`, mỗi nhóm trong số 11 nhóm tư thế nhiều màu được phóng to bằng ESRGAN và so sánh từng nhóm với "Bảng tra cứu màu của Brothers": các phiên bản hiện tại tốt hơn (thường có nhiều cặp bảng màu một đối một và phiên bản màu trắng của ズワァース, ガンダムmkⅡ sẽ sai màu khi tra cứu bảng) và sẽ không bị thay đổi.
- Các hình ảnh bổ sung về thân máy (đạo cụ, tư thế thứ hai, các bộ phận kết hợp, § "Body Vẽ" tổng cộng khoảng 300) và các hiệu ứng đặc biệt của vũ khí vẫn là ảnh gốc.
- Nhấp nháy màu trắng khi nhấn: Chế độ 4 ghi lại bảng màu tại chỗ và hình ảnh HD không đổi màu; Chế độ 1 thay đổi tài nguyên bảng màu và những khung hình đó không được nhận dạng và quay trở lại phiên bản gốc.

**Phối cảnh dưới nước**: Nước ban đầu có hai lớp - mặt phẳng đục 5836 (y 0) và lớp lượn sóng 5838 (đỉnh alpha 178, không có độ sâu, y 3..14). Phần chìm của cơ thể nằm giữa hai lớp và có thể nhìn thấy qua lớp sóng. §11 Làm cho nước mờ đi và ẩn đi 5836, như vậy phần dưới nước sẽ biến mất. Bây giờ cả hai lớp đều sử dụng bộ đổ bóng mặt nước: 5836 mờ, 5838 trộn theo alpha ban đầu (đục hơn theo Fresnel ở góc nhìn), và có thể nhìn thấy chân của cơ thể qua mặt nước trên máy thật.

## 13. Phân loại và rút ra sơ đồ cơ thể bổ sung (2026-09-30)

Đối với các hình ảnh trong body atlas không phải tư thế đứng, hãy tháo các bộ phận chống đỡ và căn chỉnh, so sánh từng tư thế đứng theo tọa độ trò chơi (các trường `assets/hd-ai/battle-backgrounds/unit-extra-analysis.json`, `method`):

| Phương pháp xử lý | Số lượng |
| --- | --- |
| Trực tiếp tái sử dụng lập trường | 6 |
| Thay đổi màu sắc tổng thể hoặc phát sáng | 11 |
| Hiệu ứng dư ảnh hoặc phân hủy | 8 |
| Tư thế đứng + pháo bay ra ngoài | 2 |
| Thay đổi một phần (đứng + vá một mảnh) | 47 |
| Bức tranh hoàn toàn mới | 16 (hai cái giống nhau, hình thật là 15) |

Tổng cộng 27 ảnh trong bốn danh mục đầu tiên được lấy từ thế đứng HD bởi `tools/hd_ai/unit_extra_derive.py` (đầu ra `assets/hd-ai/unit-extras-derived/`, 111 khung hình): phán đoán pixel theo pixel "cùng một thế đứng → thế đứng HD" "thay đổi màu cùng một vị trí → HD nhân với tỷ lệ màu" "các pixel mới không ở tư thế → phóng to hình ảnh gốc" "trống → trong suốt"; độ phát quang tổng thể của một tông màu được thay đổi thành bảng ánh xạ "độ sáng đứng → "Màu mục tiêu", dư ảnh trước tiên ước tính độ lệch bên theo từng hàng. Không có hình ảnh phản chiếu riêng biệt nào được vẽ, hướng trái và phải hoàn toàn phụ thuộc vào việc thay đổi các đỉnh. Toàn bộ 15 ảnh mới được tạo thành gói thế hệ image_gen `assets/hd-ai/unit-extra-imagegen/` (ảnh gốc, tư thế HD có cùng màu để tham khảo kiểu, nhắc nhở từng từ một, README). 47 thay đổi một phần và prop parts have not yet been processed. The 15 pictures (chest, arms, fists) that were once classified as "partial color change" were tested to "whether the same color in the standing posture always corresponds to the same color in the new picture". The consistency is only 23-59% (the true color change is close to 100%). They are actually redrawn and have been incorporated into local changes.

## 14. Gói Access HD (gửi ngày 30-09-2026)

- Art list `content/art/stage1-hd.json` adds `unit_extras`, pointing to `assets/hd-ai/unit-extras-derived/pack` (`unit_extra_derive.py --pack` generation: each frame is cropped according to the range of the parts it actually draws, and the transparent parts are filled with the nearest solid color, index `unit-extras.json`, schema `srw64.unit-extra-images.v1`, 96 frames).
- `compile_art` Biên dịch thành `srw64-unit-extras-hd.json` và `unit-extras/`; xuất bản và nén `compress_hd.py` theo cách tương tự như kết xuất nội dung, giảm xuống còn 6 lần và phân tách JPEG+alpha PNG.
- Host `native_sprite.cpp`: Read `srw64-units-hd.json` (frame 0) and `srw64-unit-extras-hd.json` (by frame number), and use the shared `presentation::load_rgba` (JPEG+alpha of the release package) for decoding; ảnh gốc được đánh giá và lật theo phần đỉnh S; không có hình tứ giác trong hình ảnh HD. `scene-sprites.jsonl` Ghi lại `no image`.
- Máy thật (Mac, profile chơi bình thường): Nhật ký tải 332 bức tranh dọc và 96 khung hình đồ họa phái sinh; ở cấp độ nhỏ battle-ui, ミニフォー, ダンバイン và ゴッドガンダム đều được thay thế. Các khung bổ sung không xuất hiện trong các trận chiến này (chúng chỉ được sử dụng khi thực hiện các loại vũ khí cụ thể). Chúng chỉ được so sánh ngoại tuyến và chưa được nhìn thấy trên máy thực tế.

**Orientation correction (2026-10-01)**: Initially, the mirror image was judged according to the S direction of the vertex of the part, but 134 of the 316 stances (mostly enemy aircraft) were stored upside down, and each part had a flip mark (0x10). Khi vẽ bình thường thì chữ S bị đảo ngược nên bị đánh giá nhầm là ảnh phản chiếu, còn ảnh HD quay sai hướng. Change to accurate judgment: the vertex address of the quadrilateral is equal to "scene data + part vertex offset" which is the first group, plus 0x40 is the mirror group (`vertex_set`). HD của デスアーミー(khôi phục) và ダンバイン thực tế đều có cùng hướng với phiên bản gốc cùng một lúc.

## 15. Hình ảnh bổ sung của thân máy bay image_gen, cut-in, đạo cụ, họa tiết mặt đất (2026-10-02, hoàn thành offline, không phải máy thật)

**Extra body image image_gen access**: Generate package `assets/hd-ai/unit-extra-imagegen` (62 pictures: 15 new pictures, 47 partial changes, see `selected-manifest.json` for the selected version). Accessed by `tools/hd_ai/unit_extra_imagegen.py compose`: use `portrait_matte.matte_portrait` to register each picture and cut out the original frame outline into an 8x master (55 The default threshold is passed; the overall size of 01, 03, 07, and 08 deviates from the original image by 2–8%, and the redrawn parts of 17, 18, and 24 deviate from the original image, and are relaxed to `RELAXED = (0.09, 20, 9)` rồi kiểm tra thủ công); đối với các thay đổi cục bộ, hãy sử dụng chế độ HD trong vùng màu xám của hình ảnh được đánh dấu và lấy bản nháp ở vùng màu đỏ và tăng thêm 1 pixel gốc; các khung hình còn lại của hoạt ảnh nhiều khung hình được sử dụng với cảnh `also`. `derive_frame` được lấy từ khung vẽ. Các kết quả được hợp nhất thành `unit-extras-derived/manifest.json` với `method: image_gen`, `unit_extra_derive.py` Việc chạy lại đầy đủ sẽ giữ lại các mục nhập này. 196 khung hình trong gói, bao gồm 100 khung hình trong image_gen.

**cut-in** (§6.3, đăng ký 984–1038, 55 cảnh 308 khung hình, loại bỏ trùng lặp 208): `tools/hd_ai/cutin_hd.py` Kết xuất từng khung hình, cắt thành từng phần khung giới hạn, phóng to bằng công thức ESRGAN về tư thế cơ thể; thay thế toàn bộ khung giống như phần thân, máy chủ chỉ đọc thêm một chỉ mục. Khuôn mặt chỉ có 6-20 pixel gốc. ESRGAN will fabricate the facial features (1029 five figures with palms raised into a ball), and redraw it by image_gen according to the **whole picture in the atlas**: the cut-in frame is cut from the parts of the picture that is completely stored in the atlas (translation, several characters gathered together are the same picture to change the position), so `tools/hd_ai/cutin_imagegen.py compose` redraw the 10 After registering and cutting out the images, they were pasted into the 8x atlas, and then all involved frames were reconstructed according to the original parts list (stacked in order, flipped horizontally at 0x10), for a total of 36 frames. 1029 f24 stacks 5 eye patches (15×7 pixels) from other places, omit them first during reconstruction (`OVERLAY_LIMIT`), and generate package No. 16 to add the eyes separately. Cận cảnh khuôn mặt lớn (1000, 1009, 1022, 1023 cận cảnh, 1034, 1037) ESRGAN phù hợp với ảnh gốc mà không cần vẽ lại.

**Prop Parts**: Registrations other than standing poses, extra pictures, and cut-in in the body atlas (289 scenes, 431 frames, 394 deduplication; `cutin_hd.prop_registries`), amplified by the same recipe, packaged with cut-in.

**Index and size**: cut-in and props share the `battle_sprites` of the art list (runtime `srw64-battle-sprites-hd.json`, schema the same as the extra image `srw64.unit-extra-images.v1`, host `native_sprite.cpp` loaded). The full frame image that only appears in battle is packaged in `PACK_SCALE = 5` (body scaling 80–110%, cut-in 129%, 3.2–5.2 screen pixels per native pixel at default 4x internal resolution), the 8x master remains in `hd/`; tư thế cơ thể vẫn được công bố 6x (được hiển thị phóng to trên trang).

**Ground model texture**: `tools/hd_ai/battle_ground_hd.py` Don’t run the game, statically calculate RT64 v5 hash from ROM: simulate RDP loading according to the display list (dxt odd line change/LOADTILE/LOADTLUT four copies of SETTIMG/SETTILE/SETTILESIZE/LOADBLOCK) to get 4 KB TMEM, and then follow `rt64_tmem_hasher.h` Version 5 hash (sampling width and chiều cao lấy kích thước kết cấu và mặt nạ nhỏ hơn, TLUT chỉ băm các mục được sử dụng và đuôi là chiều rộng/chiều cao/tlut/line/siz/fmt). §9 Tất cả 16 giá trị băm máy thực của thí điểm đều được sao chép. Có 424 mô hình mặt đất với tổng số 1419 họa tiết. Sau khi mở rộng thêm 16 pixel theo cách bao quanh, ESRGAN lớn hơn gấp 4 lần. The texture package written into RT64 is `battle-<hash>.png`, and the art list category is `battle` (`compile_art` whitelist has been added). Các kết cấu nhiễu (cỏ, cỏ khô, sỏi) xuất hiện dưới dạng kết cấu nét vẽ khi được phóng to, điều này được người dùng chấp nhận.

**ESRGAN speedup actual measurement** (M4 Max, cut-in 4 frames): bfloat16/float16 is 1.3 times faster, and only PixelPerfectV4 is used for the transparency channel, which is 1.9 times faster in one pass, and both have no impact on the face; thu nhỏ lại 2 lần trước lần thứ hai nhanh hơn 3,6 lần nhưng sẽ làm thay đổi đặc điểm khuôn mặt nên bị từ chối. Chưa có công cụ nào được thêm vào.