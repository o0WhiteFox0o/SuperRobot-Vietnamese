> **Ngôn ngữ / Language:** [Tiếng Việt](native-title-and-story-images.vi.md) · [English](native-title-and-story-images.en.md) · [中文](native-title-and-story-images.md)

# Màn hình tiêu đề và hình ảnh văn bản cốt truyện

24-09-2026. Logo và ngọn lửa trên màn hình tiêu đề được thay thế bằng hình ảnh độ phân giải cao toàn khung hình và các đường nối của ô biến mất; các từ trong menu tiêu đề và văn bản được hiển thị bằng hình ảnh trong cốt truyện (thẻ tiêu đề chương, trang mở đầu, trang kết thúc) đều được vẽ bằng văn bản gốc theo ngôn ngữ đọc và các chuyển động tuân theo tỷ lệ, xoay và lật riêng của trò chơi. Hình ảnh văn bản cốt truyện **không còn hiển thị ảnh gốc**, điều này cũng đúng khi F6 cắt về ảnh gốc; logo và ngọn lửa theo F6.

| Màn hình | Hình ảnh gốc | Bây giờ |
| --- | --- | --- |
| Logo tiêu đề | Cảnh 683: 64 chi tiết 16×16 ghép thành 256×64 | Ảnh full frame HD, theo dõi F6 |
| Ngọn lửa tiêu đề | Cảnh 686: 16 khung hình với 40 phần 32×32 trên mỗi khung hình | 16 ô HD có thể lặp theo chiều ngang, theo F6 |
| NHẤN NÚT BẮT ĐẦU, bốn mục trong menu chuông | Cảnh 651–655 (Phòng trưng bày 623) | Văn bản gốc, theo ngôn ngữ (tiếng Trung: vui lòng nhấn phím BẮT ĐẦU, bắt đầu, đọc, tiếp tục, tùy chọn) |
| Tiêu đề tác phẩm bay qua khi khởi động | Cảnh 628–650 (Album 623 / Bảng màu 624), 23 tác phẩm | Văn bản gốc, ngôn ngữ sau: phụ đề nhỏ ở trên, tên tác phẩm ở dưới, lấy danh từ tác phẩm |
| Tên máy bay trước trận trình diễn | Cảnh 658–680 (Atlas 656 / Palette 657), 23 chiếc | Văn bản gốc, theo ngôn ngữ: model ở trên cùng (giống nhau ở mỗi ngôn ngữ), tên máy bay ở dưới cùng, lấy mục danh từ máy bay |
| Thẻ tiêu đề chương | 133 thẻ (bảng 0x84B20), "Tập N" là cảnh 5106+N−1 | Văn bản gốc "Tập N" và "Tiêu đề", giữ lại hành động nhập |
| Lời mở đầu | 30 trang văn bản (5506–5535) | Văn bản gốc, bản dịch được lấy từ `intro.txt` |
| Kết thúc | 7 hình ảnh (5570–5576) | Văn bản gốc, bản dịch lấy từ `ending.txt` (mới viết lần này) |
| Tín dụng | 20 trang (5544–5563), giữa phần kết và "kết thúc" | Văn bản gốc, ngôn ngữ sau, được lấy từ `credits.txt` |
| Trang bản quyền | 620 lúc khởi động (cảnh 622) | Văn bản gốc, tất cả các ngôn ngữ đều giữ nguyên văn bản gốc |
| Logo BANPRESTO, TRÒ CHƠI TRÒ CHƠI | 617 (cảnh 619), 615 (cảnh 614) | Hình ảnh độ nét cao full frame, được tạo từ ROM khi game đang chạy, theo F6; không có AI |

Không xử lý: dòng tiêu đề tiêu đề (611, hoạt ảnh bảng màu).

## Cách vẽ trò chơi

### Trình hướng dẫn cảnh

Các thành phần tiêu đề và hình ảnh văn bản cốt truyện đều là **hình ảnh cảnh**: một khung được tạo thành từ một số phần được liệt kê trong tài nguyên cảnh và mỗi phần được lấy từ album. `80097C68` Chọn họa sĩ theo chế độ (nhảy bảng `800D0530`, chế độ chỉ số dưới − 1):

| Chế độ | Họa sĩ | Phương pháp vẽ |
| --- | --- | --- |
| 11, 12 | `800975A4` → `80096CD8` | Một VĂN BẢN cho mỗi phần (tọa độ màn hình, không thể chia tỷ lệ) |
| 13 | `8009751C` → `80096CD8` | Tương tự như trên, y trừ độ sâu |
| 14, 15, 16 | `8009761C` | Bốn đỉnh của mỗi phần cộng với một G_QUAD, chịu sự biến đổi ma trận sprite (chia tỷ lệ, xoay, phối cảnh) |

Lệnh hiển thị từng phần trong danh sách:

- `80096CD8`: `FD48` Ngói, `F5`, `E6`, `F4` LoadTile, `E7`, `F5`, `F2` THIẾT LẬP KÍCH THƯỚC, sau đó `E4`/`E1`/`F1` bao gồm ba VĂN BẢN. Khi tọa độ âm, kẹp về 0 và điều chỉnh S.
- `8009761C`: `01004008` G_VTX (4 đỉnh của phần), tải bản đồ, hai `F2`, sau đó `07` G_QUAD. Khi đọc tĩnh, tôi nghĩ G_VTX gần bằng quad, nhưng chỉ trong kết xuất máy thực tế, tôi mới nhìn thấy rõ ràng trước khi kết cấu được tải.

Cả hai đều tải bảng màu 16 màu ở đầu (`FD10` + LoadTLUT); khi độ trong suốt của sprite không phải là FF, hãy viết một màu chính `FA` khác (alpha nằm ở byte thấp).

** Số tài nguyên có thể được đọc trực tiếp. ** Sprite được ghi trong `800FFAAC + 槽 × 0xC4 + 子 × 0x30`: cảnh +0xA, tập bản đồ +0xC, bảng màu +0xE đều là các thẻ điều khiển tài nguyên, +0x11 là bước hiện tại. Bảng điều khiển nằm trong `80160340`, mỗi mục có 20 byte: +0 đang sử dụng, +2 **số tài nguyên ROM**, +0x10 địa chỉ dữ liệu (`8008A11C` lấy địa chỉ, `80089EB0` tìm kiếm hoặc phân bổ theo số tài nguyên). Vì vậy không cần phải xác định bằng pixel tóm tắt như avatar. Byte thứ 0 của dữ liệu cảnh là số bước và mỗi bước bắt đầu từ byte thứ 2 là (số khung, thời lượng).

### Màn hình tiêu đề

Lớp phủ tiêu đề nằm trong ROM `0x10DA50` (RAM `801C4500`).

| Yếu tố | Khe | Chế độ | Cảnh/Thư viện/Bảng màu |
| --- | --- | --- | --- |
| Ngọn lửa | 9 | 11 | 686/684/685, địa điểm (160, 120) |
| Logo | 2 | 11 sau 14 (nhập) | 683/681/682 |
| NHẤN NÚT BẮT ĐẦU | 3 | 11 | 651/623/625 |
| Thực đơn chuông | 3–6 | 14 | 652 スタート, 653 ロード, 654 コンティニュー, 655 オプション; Phòng trưng bày 623 |
| Tên công việc bay | Được chỉ định bởi `801C5500` | 14 | 628 + n/623/624, n lấy từ `D_801CC340` |
| Tên đơn vị trước khi trình diễn | 2 | 15 | 658+n/656/657 (`801C9EA8`), đơn vị được kéo dọc ở slot 3 |

Menu bánh rán phân biệt các trạng thái theo bảng màu: 624 màu trắng nhạt, 625 và 626 màu xanh lam (mục phía trước), 627 màu tối. Văn bản gốc được vẽ với dải màu từ trắng đến xám nhạt, được nhân với màu sáng nhất trong bảng màu hiện tại, do đó các điểm sáng và tối ban đầu vẫn có hiệu lực.

Mỗi khung của ngọn lửa thực chất là một ô 128×128 trong tập bản đồ, trải theo chiều ngang 2,5 lần (x −160…160, y −8…120, thứ tự cột 3, 0–3, 0–3, 0). Có hai trường hợp ngoại lệ:

- Có hai khối bị thiếu ở hàng trên cùng của khung 4 và 10. Hai khối đó trong tập bản đồ là các pixel màu vàng sáng không liên quan, không được cố ý vẽ trong tác phẩm gốc;
- Ở khung 5, vẽ thêm hai ngọn lửa 16×16 (y −24) phía trên ô.

Do đó, bức ảnh có độ phân giải cao được xây dựng lại theo "các phần được vẽ thực tế", để lại thêm 16 px ở trên cùng.

### Tên tác phẩm và tên máy trình diễn tiêu đề

Có 23 hình ảnh trong mỗi nhóm, tương ứng với 23 bản trình diễn tiêu đề (23 bản ghi trình diễn cuối cùng của ROM `0x83110`).

- **Tên tác phẩm**: Sau khi khởi động, sau BANPRESTO và trang bản quyền và trước khi logo xuất hiện, `801C5500` làm cho tên tác phẩm bay từ xa (chế độ 14, có dư ảnh đệm khung). Hình ảnh là văn bản hai lớp: phụ đề bằng chữ nhỏ ở trên cùng (Chiến binh cơ động, Lực siêu điện từ, v.v.) và tên tác phẩm ở phía dưới; 0083, bên dưới là STARDUST MEMORY, ジャイアント・ロボ, bên dưới là THE ANIMATION và "The Earth Stands Still".
- **Tên đơn vị**: Trong trường sáng có nền trắng trước khi bắt đầu mỗi phần trình diễn, tên của đơn vị (khe 2) và hình vẽ ba chiều của đơn vị (khe 3) xuất hiện cùng nhau. Số cảnh = 658 + `D_801CC198[D_80161566]`, nội dung và BGM được lấy từ bảng `D_801CB124` (mỗi mục là số nội dung s16, số bài hát s16). 8 máy thuộc dòng Gundunda có số model bằng chữ nhỏ phía trên tên của chúng (MSZ-006, RX-93, v.v.).

### Thẻ tiêu đề chương

Máy trạng thái mở `D_80217AE8` của lớp phủ bản đồ (`load_000AB160`):

1. `801C72C8` tạo hai chế độ 14 Wizard: slot 0x9C là tiêu đề (số thẻ = `D_802195B1[场景 × 2]`, `8009C8EC` tra cứu bảng `0x84B20` để lấy cảnh/tập bản đồ/bảng màu), slot 0x9D là "Tập thứ N" (cảnh 5106 + số tập, giới hạn trên 98). Giá trị ban đầu: tỷ lệ 20, độ sâu 740, 180° quanh trục Y; và gọi `800836CC(1)` để bật dư ảnh.
2. `801C7460`: Mức thu phóng được trừ đi 1/24 cho mỗi khung hình và xoay 5° quanh trục Z cho đến khi mức thu phóng là ≤ 1.
3. `801C7514`: Tiếp tục đến hết vòng tròn.
4. `801C765C`: Xoay 5° mỗi khung hình từ 180° quanh trục Y (lật).
5. `801C77A0`: Thả hai yêu tinh sau khi dừng 91 khung hình, `800836CC(2)` tắt dư ảnh.

Hậu ảnh được triển khai bởi `80083744`: Khi `D_8010F5B6` là 1–3, khung trước đó được sử dụng làm kết cấu và xếp chồng trở lại màn hình với mức alpha giảm dần (từ 200). RT64 sao chép bộ đệm khung này ở độ phân giải gốc, do đó vết mờ khi xoay là hình vuông; điều này không liên quan gì đến sự thay thế này, bản thân thẻ đông lạnh là văn bản gốc có độ phân giải cao.

### Mở đầu và kết thúc

- Đoạn mở đầu (lớp phủ tiêu đề): `801CA468` Xây dựng chế độ 14 sprite ở khe 2 hoặc 3 (cảnh và thư viện lấy từ `D_801CB230[组][页]`, bảng màu 5536), tỷ lệ 10; `801CA608` đã chuyển đổi sang chế độ 11 trang tĩnh sau khi trừ 0,4 xuống 1 trên mỗi khung hình.
- Kết thúc (`load_001156A0`): Bảng trang `D_801C3050` (ROM `0x1160F0`), mỗi mục (cảnh, thư viện, số khung), kết thúc ở 0xFFFF. Đầu tiên là phần kết 5570-5575, sau đó là phần ghi công 5544-5563, và cuối cùng là "kết thúc" 5576; bảng màu đều là 5564 và cùng chế độ 14 được sử dụng để phóng to và sau đó chuyển sang chế độ 11.
- Kiểm kê tài sản từng được phân loại 5582 là bầu trời đầy sao ở cuối phần tín dụng, nhưng thực tế nó là nền của lớp phủ bản đồ thế giới (`load_000A7EC0`).

### Tín dụng, trang bản quyền, logo BANPRESTO và GAME OVER

24/09/2026 đã thêm. Cả bốn đều là cảnh trong Chế độ 14, sử dụng cùng một bộ móc:

| Màn hình | Khe | Cảnh/Album/Bảng màu | Tạo bởi |
| --- | --- | --- | --- |
| Logo BANPRESTO | 2 | 619/617/618 | lớp phủ tiêu đề `801C4E8C` |
| Trang bản quyền | 0 | 622/620/621 | Lớp phủ tiêu đề `801C5104` |
| TRÒ CHƠI KẾT THÚC | 0x3D | 614/615/616 | Lớp phủ bản đồ `801DF338` (`3D4C` Trò chơi kết thúc) |
| Tín dụng | 2, 3 | 5565–5569 / 5544–5563 / 5564 | Bảng trang kết thúc, 85 khung hình trên trang 1, mỗi khung 55 khung hình |

- **Tín dụng**: Cách xử lý tương tự như trang kết thúc, `staff_style` của [`sprite_text.cpp`](../../src/host/sprite_text.cpp) được căn giữa và khoảng cách dòng là khoảng 30 đơn vị (khoảng cách dòng của hình ảnh gốc). Văn bản nằm trong mục `@intro:<资源号>` của `content/dialogue/<语言>/credits.txt`: vị trí được dịch; tên tiếng Trung được chuyển sang chữ Hán giản thể, bút danh kana được giữ nguyên; tên tiếng Anh được La Mã hóa, đặt tên đầu tiên. Dòng văn bản gốc (`>`) là nội dung hiển thị bằng tiếng Nhật.
- **Trang bản quyền**: `copyright_style` được căn trái và cũng được đặt trong `credits.txt` (`@intro:620`). Theo yêu cầu của người dùng, chỉ thay đổi văn bản gốc và ba ngôn ngữ đều là văn bản gốc.
- **logo BANPRESTO với GAME OVER**: Độ phóng đại 8x (1792×768, 1280×256). Logo là nhãn hiệu chứ không phải AI: cả hai đều chỉ có một vài màu phẳng và khử răng cưa. Mỗi pixel được phân tách theo hai màu chính gần nhất. Mỗi lớp màu được phóng to và làm mịn để có giá trị mềm tối đa dốc. Cạnh rộng khoảng 1 pixel đầu ra; GAME OVER lớp nét xám vẫn giữ nguyên độ sáng và tối ban đầu.
- Được tạo từ ROM của người chơi khi trò chơi đang chạy (do người dùng xác định) từ 25-09-2026, hai hình ảnh này không được bao gồm trong gói HD: [`rom_art.cpp`](../../src/host/rom_art.cpp)'s `flat_image` đã ghép thuật toán của [`flat_scene_hd.py`](../../tools/hd_ai/flat_scene_hd.py) (Gối Tỷ lệ hai khối và mờ kiểu hộp gần đúng Gaussian đều được triển khai tương ứng), `host.cpp` được đăng ký trong `on_init` với `add_generated_image` của [`native_sprite`](../../src/host/native_sprite.cpp). Cảnh được tạo trên luồng giải mã khi nó xuất hiện lần đầu và toàn bộ khung hình được vẽ giống như hình ảnh tệp. Chỉ đăng ký nếu bạn có gói nghệ thuật HD (`SRW64_ART_PACK`).
- `scene_images` trong số `stage1-hd.json` được đổi lại thành `assets/hd-ai/title/whole-v1` (logo tiêu đề có ngọn lửa). Đầu ra của `flat_scene_hd.py``whole-v2` chỉ được sử dụng để so sánh trên máy này: `make recomp-rom-art-test` so sánh sự khác biệt sau khi nhân trước, BANPRESTO trung bình 0,2 mức; GAME OVER có khoảng 4 cấp độ, sự khác biệt so le nhau một pixel ở cạnh nét vẽ và hình ảnh giống nhau.
- Máy thực tế: BANPRESTO vẽ đồ thị sinh ra (`build/recomp/debug/20260925T071832.109292Z/banpresto.png`) từ khung hình thứ 147 sau khi khởi động; GAME OVER vẽ biểu đồ được tạo ở cấp độ thử nghiệm (`20260925T072039.132657Z`, `scene-sprites.jsonl` của `20260925T072411.224535Z` và `image` dòng của cảnh 614). Người dùng đã nhìn thấy trên máy thực tế và không có vấn đề gì.
- Cấp độ kiểm tra `game-over.json`: Trực tiếp `3D4C` sau khi chuyển sang chiến trường lúc đầu.

## Nhận dạng văn bản

- **Thẻ Tiêu đề Chương**: 133 ảnh được đọc từng ảnh một (được Claude nhận dạng), lưu dưới dạng `assets/transcriptions/chapter-titles.ja.json`, các ảnh gốc được giữ lại và xếp dòng, còn "trước/giữa/sau chỉnh sửa" được tách thành các dòng riêng biệt. So sánh với văn bản tiêu đề 281 + từng cảnh một: 136 trên 143 cảnh giống hệt nhau; thẻ 8 "Jie Farewell" và dòng chữ "Jie Farewell のとき", thẻ 89 "戦 field へ帰る" và "戦 field に帰る" mỗi thẻ khác nhau bởi một bút danh; cảnh dành riêng 125–127 chia sẻ thẻ với cảnh 81 82 "Thanh lọc"; thẻ 0 và 1 chỉ có "Tập 1" (giữ chỗ, dùng trong cảnh 58 và 142); quân bài 127 và 128 giống nhau "Hợp lưu".
- **Trang cuối**: 7 trang ảnh đọc từng dòng, được lưu dưới dạng `assets/transcriptions/ending-pages.ja.json`.
- **Lời mở đầu**: Theo phiên âm ngày 23-09-2026 `assets/transcriptions/intro-pages.ja.json`.

Bản ghi âm chứa văn bản gốc tiếng Nhật và chỉ được đặt cục bộ trong `assets/`. Chỉ những thẻ thu được từ nó mới được gửi đến kho → so sánh số văn bản ([`story_cards.hpp`](../../src/host/story_cards.hpp), được tạo bởi [`text_images.py`](../../tools/content/text_images.py) và được kiểm tra bằng thử nghiệm).

## Bản dịch đến từ đâu?

| văn bản | Nguồn |
| --- | --- |
| Bốn mục menu, NHẤN NÚT BẮT ĐẦU | văn bản giao diện ngôn ngữ `title_start`, `title_load`, `title_continue`, `title_option`, `title_press_start` |
| "Chương N" | Văn bản giao diện `intermission_episode` |
| Tiêu đề chương | Nhập từ (`story.chapter_title`), máy chủ lấy ngôn ngữ hiện tại thông qua `dialogue::ui_text`; thêm "" cho tiếng Trung và tiếng Nhật |
| Lời mở đầu | `@intro:<资源号>` mục nhập cho `content/dialogue/<语言>/intro.txt` |
| Kết thúc | `content/dialogue/<语言>/ending.txt`, cũng là mục nhập `@intro:<资源号>`, lần này được viết tay, `---` có nghĩa là một dòng trống |
| Tiêu đề công việc được chứng minh | Văn bản 85 + số tác phẩm (viết thành hai dòng, có phụ đề trước và tên tác phẩm sau ngắt dòng; hai dòng được đổi chỗ khi phụ đề tiếng Anh kết thúc bằng dấu hai chấm, chẳng hạn như Dancouga); văn bản cho phụ đề của CounterAttack のシャア, MS Team 60 thứ 08 (chiến binh di động ガンダム); BỘ NHỚ STARDUST, HÌNH ẢNH Như vốn có; "Trái đất vẫn đứng yên" là dòng chữ giao diện `title_demo_giant_robo_subtitle` |
| Tên máy bay trình diễn | Văn bản 527 + số hiệu máy bay; bảng trình diễn ghi MASCUBAZ (JS) (263), và hình ảnh ghi MASKODEZ, vì vậy hãy lấy 262; số model được ghi như trong hình ở `sprite_text.cpp` |

Màn hình tiếng Nhật sử dụng trực tiếp các dòng gốc trong các mục này (`>`). Tệp dòng có thể được đặt trong thư mục người dùng và được ghi đè. Sau khi nhấn F5 để đọc lại, trang văn bản cũng sẽ được cập nhật.

## Triển khai máy chủ

- [`native_sprite.cpp`](../../src/host/native_sprite.cpp) (được chia sẻ bởi ba máy chủ): `generate_cpu.py` Đổi tên `80096CD8`, `8009761C` về chức năng ban đầu, bọc một lớp bằng [`game_hooks.cpp`](../../src/host/game_hooks.cpp) và lưu ý phạm vi danh sách hiển thị được ghi lần này. Sau khi vẽ, lấy (cảnh, tập bản đồ, bảng màu, khung) theo bảng ghi phụ và bảng điều khiển, rồi quyết định những gì cần thay thế:
- Với văn bản gốc: luôn được thay thế;
- Có hình ảnh độ phân giải cao của khung này trong gói nghệ thuật và ở chế độ HD: Thay thế;
- Nếu không giữ nguyên linh kiện.

Khi thay, để lại phần cuối làm dấu và để trống phần còn lại: TEXRECT chuyển thành hình chữ nhật bao phủ toàn bộ khung; tứ giác giữ lại G_VTX và G_QUAD ban đầu. Đánh dấu lệnh trước đó bằng thẻ G_NOOP được đánh số. RT64 nhận dạng thẻ khi xây dựng, gọi lại máy chủ gọi lại ở cùng vị trí vẽ và vẽ qua Plume (`src/host/shaders/HdSprite*.hlsl`): TEXRECT vẽ hình chữ nhật theo tọa độ màn hình; tứ giác lấy ma trận thế giới và hình chiếu được vẽ lần này, đồng thời vẽ một hình chữ nhật trong không gian mô hình, do đó tỷ lệ, xoay, lật và phối cảnh nhất quán với phiên bản gốc.
- Văn bản được đặt theo tâm khung gốc (tiêu đề chương theo cạnh trên), kích thước do cách sắp chữ quyết định và có thể rộng hơn ảnh gốc.
- Việc giải mã và rasterization văn bản của hình ảnh độ nét cao được hoàn thành trong luồng nền. Khi chưa sẵn sàng, khung hình có độ phân giải cao lần này sẽ vẽ hình gốc và văn bản sẽ không được vẽ (chủ yếu là một vài khung hình phóng to đầu tiên). Kết cấu được nhân trước Alpha với mipmap; sau khi lưu trữ hơn 48 hình ảnh, những hình ảnh không hoạt động trong hơn 20 giây sẽ được giải phóng.
- [`sprite_text.cpp`](../../src/host/sprite_text.cpp) (chỉ trong máy chủ trò chơi) xác định văn bản nào được hiển thị cho mỗi sprite và các loại, nét và bóng được thêm vào:
- Menu và thẻ tiêu đề sử dụng phông chữ biến đổi HarmonyOS Sans 2.040 **Bold** (wght 706, `game_font_sources(locale, 700)`), không có tệp in đậm riêng biệt; Tiếng Anh sử dụng Condensed trước, sau đó là SC và phông chữ ký hiệu được đệm;
- Sử dụng Regular cho trang mở đầu và trang kết thúc, có chiều rộng 256 và giảm dần cỡ chữ khi không vừa;
- Nét vẽ có được bằng cách chuyển đổi khoảng cách và văn bản có độ dốc dọc.
- Nhật ký: `scene-sprites.jsonl` trong thư mục đang chạy ghi lại phương pháp xử lý đầu tiên và VI của từng loại (cảnh, tập bản đồ, bảng màu, khung hình); viết `scene-sprite-summary.json` khi thoát.

## Chất liệu HD

[`title_hd.py`](../../tools/hd_ai/title_hd.py) được chia thành bốn bước: `prepare` đóng băng yêu cầu từ ROM, `run` được gửi qua `run_benchmark.run_one`, `compose` đăng ký, giữ nguyên màu sắc và cắt hình ảnh, đồng thời `build` ghi thư mục thời gian chạy.

- Mẫu là `qwen-image-3.0`, hạt giống 640903 (giống hình đại diện), tổng cộng 5 yêu cầu, giá công khai khoảng 1 tệ:
- Logo 1 lần: Để lề 16 px trên nền đen, phóng to 7 lần;
- Ngọn lửa bốn lần: 2×2 bốn khung hình mỗi khung hình, với 64 px nội dung lặp riêng ở bên trái và bên phải của mỗi khung hình, phóng to 4x.
- Đăng ký: Đo cửa sổ dịch chuyển theo cửa sổ, căn chỉnh tỷ lệ và độ lệch theo hai trục; khi lấy mẫu lại, các cạnh của ô được sao chép ra ngoài để tránh hút các khoảng màu đen vào cạnh dưới.
- Bảo toàn màu sắc: Các chi tiết tần số cao được lấy từ đầu ra của mô hình, còn các màu tần số thấp được lấy từ ảnh gốc (bán kính 2 pixel gốc). Alpha lấy mặt nạ 1 bit của ảnh gốc, phóng to và làm mịn nó sang một bên rộng khoảng 1 pixel đầu ra.
- Vòng lặp: 8 pixel gốc ở phía bên trái của ô xếp chéo mờ dần thành nội dung tiếp tục được mô hình vẽ ở bên ngoài phía bên phải, do đó phần đầu và phần cuối liền mạch.
- Chênh lệch trung bình so với ảnh gốc sau khi thu nhỏ về kích thước gốc: logo 5.1, ngọn lửa 3,7–8,5.
- Đầu ra ở dạng `assets/hd-ai/title/whole-v1` (Logo 1792×448, ngọn lửa 16 tờ 512×576), được tham chiếu bởi phần `scene_images` của [`stage1-hd.json`](../../content/art/stage1-hd.json), [`assets.py`](../../src/srw64_native/assets.py) Sau khi xác minh bản tóm tắt, sao chép nó vào gói nghệ thuật và viết `srw64-scene-images.json`.

## Xác minh máy thực tế (24-09-2026)

- **Tiêu đề**: Trong ảnh chụp màn hình tiếng Trung và tiếng Anh, logo và ngọn lửa ở độ phân giải cao toàn khung hình và các đường nối biến mất; các từ trong menu được hiển thị theo ngôn ngữ, với các mục phía trước màu xanh lam và các mục còn lại có màu xám, phù hợp với phiên bản gốc. Sau khi F6 chuyển về phiên bản gốc thì logo và ngọn lửa sẽ trở về hình ảnh ban đầu, còn văn bản menu vẫn là văn bản gốc. Người dùng đã chuyển đổi ngôn ngữ trong cửa sổ và xác nhận đa ngôn ngữ là bình thường.
- **Lời mở đầu**: Lời mở đầu công khai của trò chơi mới, được hiển thị nguyên bản theo từng trang bằng tiếng Trung, tiếng Anh và tiếng Nhật, với mục thu phóng và chuyển trang do phiên bản gốc điều khiển.
- **Kết thúc**: `ending.json` Cấp độ nhỏ được thực thi ở dạng 3D71 và 7 trang kết thúc đều được vẽ nguyên bản (tiếng Trung); các khoản tín dụng tiếp theo vẫn là bản vẽ gốc.
- **Thẻ Tiêu đề Chương**: Cả ba vị trí đều được phóng to và xoay vào cảnh: `act.json` Cấp độ nhỏ, tập thứ hai được nhập thông qua "Chuyển sang cấp độ tiếp theo" trong tập đầu tiên và tập đầu tiên của trò chơi mới. `act.json` Lần đó tôi nhấn VI để chụp ảnh màn hình điểm cố định và chụp được khung hình lật và đóng băng cuối cùng: "Tập 2" và "Chiến đấu! Những chiến binh máu lửa", bằng tiếng Trung Quốc (số tập ở cấp độ nhỏ tăng thêm 1 cho "Tập N").
- Thống kê xuất cảnh (tập 2): 2951 bản vẽ được viết lại, 0 bản giữ nguyên, giải mã thành công toàn bộ 24 tài liệu.
- **Danh sách tín dụng và màn hình khởi động** (Bổ sung): `ending.json` tiếng Trung được cắt toàn bộ đến trang nghệ thuật 2D và tiếng Anh được cắt thành trang nghệ thuật gốc SD (17 trang trong tổng số 20 trang). Văn bản gốc được hiển thị theo từng trang. Logo BANPRESTO khi khởi động là full frame độ phân giải cao, chữ gốc trên trang bản quyền và các ký tự tiếng Nhật như "Reed" là bình thường.
- **GAME OVER** (Bổ sung): Tiếng Anh `game-over.json`, đóng băng khung hình ở độ nét cao, cắt về phiên bản gốc để xem ảnh gốc (có những đường mảnh tạo thành bởi đường nối của các bộ phận ở dưới cùng của ảnh gốc), sau đó cắt lại về độ nét cao.

## Lệnh

```sh
.venv/bin/python -m tools.hd_ai.title_hd prepare --output assets/hd-ai/title/v1
.venv/bin/python -m tools.hd_ai.title_hd run --output assets/hd-ai/title/v1 --env-file /path/to/.env
.venv/bin/python -m tools.hd_ai.title_hd compose --output assets/hd-ai/title/v1
.venv/bin/python -m tools.hd_ai.title_hd build --output assets/hd-ai/title/v1 --target assets/hd-ai/title/whole-v1
.venv/bin/python tools/content/text_images.py header --write   # 卡片 → 话名对照
.venv/bin/python tools/content/text_images.py render           # 结局页原图，供转写核对
.venv/bin/python -m tools.hd_ai.flat_scene_hd build --base assets/hd-ai/title/whole-v1 --target assets/hd-ai/title/whole-v2 --bind
```

Sau khi thay đổi hook của `generate_cpu.py`, bạn cần chạy lại nó trước rồi mới build máy chủ.

## Di sản

- Dòng tiêu đề tập trung vẫn là ảnh gốc.
- Hầu hết tên tiếng Anh trong phần ghi công sản xuất đều dựa trên cách phát âm của ký tự Trung Quốc và tác phẩm gốc không có ký hiệu phiên âm; các nguồn đã được xác minh vào ngày 27-09-2026, bao gồm Akabane Jin, Nomura Kyouhiro (Michihiro, ban đầu bị nhầm là Norihiro), Kono Yuko, Hamada Tomoyuki và những người còn lại vẫn được liệt kê ở đầu `content/dialogue/en/credits.txt` để được xác minh.
- Dư ảnh khi xoay thẻ tiêu đề vẫn ở độ phân giải gốc (cách RT64 sao chép bộ đệm khung).
- Phần kết chỉ được thử nghiệm ở cấp độ mini; đoạn kết đầy đủ chưa được phát từ lượt lưu.
- Đường dẫn này đi theo Plume giống như các lớp HD khác và có sẵn trong cả Metal và Vulkan; Vulkan mới chỉ được thử nghiệm với MoltenVK trên Mac.