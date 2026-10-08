> **Ngôn ngữ / Language:** [Tiếng Việt](battle-graphics.vi.md) · [English](battle-graphics.en.md) · [中文](battle-graphics.md)

# Hình ảnh chiến đấu: hình ảnh chiến đấu của máy bay, phần hoạt hình, hiệu ứng đặc biệt và đoạn cắt

Cập nhật: 2026-09-19. Bài viết này ghi lại hình ảnh 2D được sử dụng để chiến đấu và trình diễn cốt truyện: phân phối tài nguyên, bảng ràng buộc, định dạng và tổ chức và xuất "cảnh yêu tinh". Cách sử dụng những cảnh này cho hoạt ảnh vũ khí và liệu bạn có thể thêm cơ thể và vũ khí tùy chỉnh hay không, hãy xem [Hoạt hình chiến đấu và cơ thể tùy chỉnh](battle-animation.md). Tất cả phân tích ROM tĩnh, không có trò chơi nào được khởi chạy.

## Xuất bằng một cú nhấp chuột

```sh
.venv/bin/python -B tools/content/export_graphics.py
```

Khoảng 15 giây, xuất ra `assets/original-graphics/` bị bỏ qua (khoảng 70 MB), chạy lại toàn bộ quá trình thay thế. `index.html` là thư viện ảnh (cần được mở qua HTTP cục bộ, chẳng hạn như `python3 -m http.server --directory assets/original-graphics`). Các hình thu nhỏ được sắp xếp theo chiều ngang theo từng khung hình và được nhấp vào để tạo hoạt ảnh APNG; `manifest.json` ghi lại loại, SHA-256, tài nguyên nguồn và chỉ mục bảng liên kết cho mỗi tệp.

| Thư mục/Tệp | Nội dung |
| --- | --- |
| `units/NNN-机体名/` | Một thư mục cho mỗi chiếc trong số 363 máy bay: `battle.png` tư thế chiến đấu cơ bản, `battle-sheet.png` tập bản đồ chiến đấu của máy bay (với bảng màu riêng), `map-icon.png` biểu tượng bản đồ, `animations/` Tất cả các phần hoạt hình trên tập bản đồ máy bay, `unit.json` (giá trị; giá trị của từng loại vũ khí, dấu thuộc tính, bản ghi chiến đấu, bản ghi hoạt hình và bản ghi hiệu ứng đặc biệt, diễn viên chỉ vào tệp hình ảnh đã xuất từng cái một) |
| `cutins/NNNN-武器名/` | Hỗ trợ chiến đấu: 14 Vũ khíァイナルゴッドマーズ, Siêu điện từ スピン, Sora Light Răng Sword, V-MAX, v.v.), được nhóm theo vũ khí, với album ảnh được sử dụng |
| `movies/NN-名称/` | 12 phân đoạn hoạt ảnh hợp nhất/chuyển hóa trên bản đồ (コン・バトラーV, ゴッドマーズ hợp nhất, ゲッター 6 biến đổi, オーラロード 4 phân đoạn), được đánh số theo thứ tự phát lại |
| `battle-scenes/atlas-AAAA/` | Các cảnh chiến đấu còn lại: các hiệu ứng đặc biệt như tia, vụ nổ, nhát chém và khiên, được nhóm theo album, có đính kèm toàn bộ album |
| `portraits/NNN-全名.png` | Avatar của 361 danh tính (nhiều danh tính có thể chia sẻ cùng một hình ảnh) |
| `chapter-titles/`, `maps/` | 133 chương thẻ tiêu đề; 158 bản đồ nền chiến trường tĩnh |
| `units.csv`, `weapons.csv` | Bảng tổng hợp giá trị cơ thể và vũ khí (UTF-8 BOM, phần mềm bảng có thể mở trực tiếp) |
| `animations.json` | Kết quả phân tích tất cả hoạt ảnh của vũ khí, hiệu ứng đánh đặc biệt và hồ sơ phản ứng phòng thủ |

Hình ảnh trình duyệt dữ liệu gốc `assets/original-data/images/` vẫn được đặt tên theo số tài nguyên để sử dụng cho trình duyệt; lần xuất này sắp xếp lại cùng một loạt hình đại diện, biểu tượng bản đồ và bản đồ cơ sở chiến trường theo tên máy bay, nhân vật và vũ khí, đồng thời thêm tất cả hình ảnh chiến đấu. Cả hai đều sử dụng cùng một bộ ràng buộc.

## Phân phối tài nguyên

Số này là ID của bảng tài nguyên 6.436 mục. Bảng sau đây chỉ là tổng quan về phân phối; bảng màu nào khớp với hình ảnh sẽ dựa trên bảng liên kết được mã đọc và không được suy ra dựa trên các số liền kề.

| Phạm vi tài nguyên | Nội dung |
| --- | --- |
| 9–308, 309–609 | Avatar nhân vật (CI8 96×96) và bảng màu; 1308–1311 là hình đại diện trên màn hình lưu trữ/chọn lọc cho bốn nhân vật chính ban đầu |
| 687–1009, 1010 | Biểu tượng bản đồ (CI4 16×16) và bảng màu của chúng tôi |
| 1337–1368 | trận chiến cắt cảnh Album ảnh cận cảnhントロボ, レイズナー, ダンクーガ, シャッフルAlliance, v.v.) và ゲッターTransformation Atlas |
| 1472–1478, 1521–1587 | Album của ゴッドマーズ fusion, ゲッターG biến hình, オーラロード, コン・バトラーV fusion |
| 1399–1471, 1486–1611 | Dữ liệu cảnh của hoạt hình bản đồ/bản đồ ở trên |
| 1612–1907 (và 2762–2767, 2894, v.v.) | **Bản đồ chiến đấu trên máy bay**, CI8, loại hình ảnh 7, kích thước 32k+1 (ví dụ: 257×193) |
| 1908–2212 | Bảng màu Atlas chiến đấu máy bay |
| 2213–2476 | Cảnh tư thế cơ bản |
| 2477–2749, 3533–4257, v.v. | Phần hoạt hình vũ khí và cảnh hiệu ứng đặc biệt |
| 3006–3243, 3244–3532 | Tập bản đồ hiệu ứng đặc biệt (CI4/CI8) và bảng màu |
| 4267–4296, 4297–4326, 4327–4357 | Sơ đồ khiên, bảng màu, cảnh phòng thủ khiên |
| 4988–5104, 5105, 5106–5334 | Hình ảnh tiêu đề chương (CI4 514×65), bảng màu 16 màu dùng chung, cảnh tiêu đề |
| 6067–6115, 6116–6227 | Bản đồ nền và bảng màu 320×240 CI4, thuộc nền chiến đấu 3D và không có trong bản xuất này |

## Bảng ràng buộc

(Cảnh, Atlas, Bảng màu) Bộ ba đều có 6 byte `u16 scene, u16 atlas, u16 palette`, với 2 byte ở cuối bảng được đệm bằng số 0. Byte bảng SHA-256 được cố định ở `src/srw64_native/battle_graphics.py`.

| Bảng | ROM | Nhập cảnh | Đọc Mã | Chỉ mục |
| --- | --- | ---: | --- | --- |
| Tư thế chiến đấu cơ bản của máy | `0x84E40` | 365 vị trí (0–362 hợp lệ) | Thường trú `func_8009C864` | ID máy |
| Bảng tóm tắt cảnh chiến đấu | `0x11E3D0` | 1.053 vị trí (1.051 hiệu quả) | `func_801C3170` cho lớp phủ trận chiến `load_00121560` | Trường đăng ký diễn viên hoạt hình vũ khí |
| Hoạt hình bản đồ | `0x106F20–0x107200` | 12 đoạn, 95 món | Trình phát cho lớp phủ bản đồ chiến thuật `load_000AB160``func_802176A8(id)` | Số hoạt hình 0–11 |
| Tiêu đề chương | `0x84B20` | 133 | Cư dân `func_8009C8EC` (bản đồ chiến thuật `func_801C72C8` được gọi khi khai mạc) | Số tiêu đề |

- **Bảng đơn vị** Được lập chỉ mục theo ID đơn vị, kiểm tra trực quan từng cái một: 0 ガンダムシュピーゲル, 3 シャイニングガンダム, 5ドモン・カッシュ(生生, album nhỏ chuyên dụng 4930), 7 ノーベルガンダムB, v.v. Những người gọi được phân bổ trong chiến đấu `load_00121560` (`801C5328`, `801C5808`, `8021FB4C`), bản đồ chiến thuật `load_000AB160` và `load_0008E580`, `load_0008F4B0`, `load_0010DA50`, `load_00217FD0`. 330 tập bản đồ phục vụ 363 đơn vị; sự khác biệt về hình thái thường có chung các tập bản đồ (chẳng hạn như 12/11 ガンダムローズ).
- **354–362** (イーグル号…シャトル号, ブラックジョーカー, シュバルツ) có giá trị tương đương với vũ khí (HP 4000,パンチ/キック/rush), tất cả đều mượn từ bản đồ chiến đấu của シャイニングガンダム, và bảng đơn vị chiến đấu chỉ có 354 hàng - đó là bản ghi giữ chỗ, xem [Tính khả thi](battle-animation.md#加入自定义机体与武器).
- **Cảnh chiến đấu** là các mục 984–1038 trong danh sách tổng thể cảnh chiến đấu, được các diễn viên bình thường tham chiếu cho hoạt hình vũ khí; 9 trong số đó không được đề cập trực tiếp đến bất kỳ hồ sơ vũ khí nào.
- **Hoạt hình bản đồ**: Người chơi sử dụng `80098158(slot, 0, 0xB, 0x8D, scene, atlas, palette, 1)` để tải từng phần một. ID 5–10 chia sẻ một phần dữ liệu gồm 30 mục, được chia thành các nhóm gồm 5 mục. Nguồn kích hoạt (xác nhận mã): Lệnh tập lệnh `3D67` (ID 0–4), `3D6A` (tổ hợp ゴッドマーズ, ID 11), ゲッター phần thân hệ thống 171–176 chuyển đổi đầu tiên (được điều khiển bởi biến tập lệnh 2 bit, chỉ được phát hành một lần; nhấn giữ START Có thể xem lại, ý nghĩa của nút là suy đoán) và sự kết hợp giữa Kono và Toro V (196). Không tìm thấy ID người gọi 2.
- Resident `0x847D0` có một bảng 141 ô khác có cùng định dạng, là bảng tóm tắt các hoạt ảnh cut-in và bản đồ, nhưng hàm đọc `func_8009C7DC` của nó không có bất kỳ lệnh gọi nào (nó không có trong bảng con trỏ hàm) và một số mục nhập khác với hai bản sao thực tế được sử dụng; bảng 1.449 mục nhập của ROM `0x8AB58` thuộc về ROBO để gỡ lỗi VIEWER(`load_00089EA0`). Hai bảng này không được sử dụng trong lần xuất này.

## Định dạng cảnh yêu tinh

Tài nguyên cảnh cắt album thành nhiều phần (chủ yếu là 32×32), tập hợp chúng thành nhiều khung rồi phát chúng theo danh sách bước. Cuối cùng lớn:

```text
u8  step_count, u8 vertex_mode
step_count × (u8 frame, u8 ticks)     frame = 0xFF：这几拍什么都不画
u8  0xFF, u8 loop_step                 结束标记；loop_step 为循环回到的步骤
u16 frame_offsets[n]                   n = (frame_offsets[0] − 表起点) / 2
frame：16 字节零件，直到 flags & 0x8000
    u16 flags   0x0010 = 水平翻转（其余位全 ROM 未出现）
    u16 s, t    图集内源坐标
    u8  w, h    零件尺寸
    s16 x, y    相对场景原点的屏幕坐标（y 向下）
    u32 vertex_offset
```

- **Phát lại** (xác nhận mã): Cư dân `func_80098880` gọi `func_80098738` một lần trên mỗi khung lớp phủ cho mỗi trong số 300 vị trí sprite (bản ghi vị trí `0x800FFA70 + slot × 0xC4`). Nó đếm ngược và chuyển sang bước tiếp theo khi về 0; khi bước cuối cùng hoàn thành, cờ phát bit0 của vị trí được đặt và nó dừng ở bước cuối cùng (hoạt ảnh bản đồ), nếu không nó sẽ nhảy trở lại `loop_step` (`80098838`). Vì vậy, một lần bắn = một lần cập nhật sprite; số lượng VI tương ứng với nó không được kiểm tra và APNG đã xuất tạm thời được xem trước ở tốc độ 33 mili giây mỗi lần chụp.
- **Vẽ**: Họa sĩ hình chữ nhật `80096CD8` (chế độ 11, dành cho hoạt ảnh bản đồ) chỉ đọc các bản ghi phần; họa sĩ đỉnh `8009761C` (chế độ 14–16) đọc `vertex_mode`: 0 = 8 đỉnh mỗi phần, 4 đỉnh đầu tiên là một nhóm theo hình chữ nhật của bộ phận, 4 đỉnh cuối cùng là các nhóm gương đảo ngược x (hướng kẻ thù và kẻ thù, khi vẽ) +0x40 tùy chọn); 1 = 4 đỉnh mỗi phần; 2 = không vẽ. Cả hai đều bỏ qua bước 0xFF.
- Các hình chữ nhật đỉnh và vị trí lật của 19.408 bộ phận Chế độ 0 đều nhất quán với các bản ghi bộ phận và việc xuất được vẽ trực tiếp theo các bản ghi bộ phận. Chế độ 1 có 686 phần có các đỉnh không phải là hình chữ nhật đơn giản (hiệu suất kiểu tỷ lệ/xoay) và những ảnh này được xuất không bị biến dạng.
- Các tư thế cơ bản của máy bay chỉ có một khung; có 470 cảnh chiến đấu và một số hoạt ảnh trên bản đồ có nhiều khung hình.
- Có những phần trong 19 cảnh vượt quá mép phải/dưới của tập bản đồ, còn những phần ngoài viền được coi là trong suốt (máy thực tế lấy mẫu theo quy tắc kẹp/lặp lại kết cấu và sự khác biệt chỉ là ở mép).
- Một số bảng màu có nhiều hơn mức hình ảnh có thể lập chỉ mục: Hiệu ứng đặc biệt CI4 thường có 112 màu (7 nhóm × 16), và một số bảng màu CI8 có 592 màu. Nhóm 0 dùng để xuất khẩu; phần còn lại là dữ liệu hoạt ảnh bảng màu và phương pháp chọn nhóm không được theo dõi.

## Xác minh

- `tests/test_battle_graphics.py`: Các trường hợp sử dụng thành phần cho bảng bước/khung trống/vòng lặp, lật, đầu vào bất hợp pháp, bảng màu quá dài và ghi hoạt ảnh. Khi có ROM, hãy kiểm tra từng bảng băm và liên kết khóa, phân tích cú pháp tất cả các cảnh được tham chiếu bởi tất cả các bảng, giải mã tất cả các tập bản đồ và so sánh từng phần và đỉnh của chế độ 0, xác nhận rằng hoạt ảnh 1.329+159+28 ghi lại tất cả các cảnh thực tham chiếu và phần cắt vào được tham chiếu bởi chính xác 14 loại vũ khí.
- `tests/test_original_images.py`: hình đại diện, biểu tượng bản đồ, ràng buộc bản đồ cơ sở chiến trường (loại hình ảnh 7 không thay đổi sau khi thêm các loại có thể giải mã).
- Kiểm tra trực quan tất cả 363 tư thế cơ bản của khung máy bay, đoạn cắt, hoạt ảnh bản đồ và một số bộ phận vũ khí trong trình duyệt; bảng nhóm bản đồ nền ROM `0x1161C0` (cặp `(首资源, 数量)`, bao gồm 6063–6214) được để lại làm đầu mối tiếp theo cho nền 3D.