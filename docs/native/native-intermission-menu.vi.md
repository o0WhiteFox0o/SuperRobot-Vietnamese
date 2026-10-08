> **Ngôn ngữ / Language:** [Tiếng Việt](native-intermission-menu.vi.md) · [English](native-intermission-menu.en.md) · [中文](native-intermission-menu.md)

# Menu chính liên trường: logic gốc và tiếp quản gốc

Ngày: 21-09-2026. Trạng thái: **Đã triển khai, menu đầy đủ đã được xác minh trên máy thật; hai menu và điều khiển RNG chưa được chạy để xác minh** (xem Phần 9). Phần 1–3 là kết luận phân tích tĩnh (bảng dữ liệu ROM và tháo rời) của `load_0008F4B0` và phần thường trú; Phần 4 trở đi là kế hoạch tiếp quản. Đường cơ sở của màn hình là ảnh chụp màn hình gốc do `sdl-link-01` đang chạy để lại và thư mục đang chạy không được giữ lại.

## 1. Màn hình gốc

Nền là một bức tranh lớn được chọn khi quá trình diễn ra, với bốn tấm góc vuông trong mờ màu xanh đậm với các cạnh mỏng màu xanh lam xếp chồng lên nhau. Mục menu hiện tại được biểu thị bằng thanh đánh dấu màu xanh lục và các ký tự ma trận điểm màu trắng. Các tọa độ đều là 320 × 240:

| Bảng điều khiển | Hình chữ nhật (trên cùng bên trái – dưới cùng bên phải) | Nội dung |
| --- | --- | --- |
| Tiêu đề | (120,25)–(199,39) | `0xFCC` インターミッション, điểm bắt đầu văn bản (124,25) |
| Thực đơn | (33,41)–(103,183); hai menu là (33,41)–(103,71) | Văn bản x=34, y=41+16×n; thanh đánh dấu x=33, rộng 70, cao 16 |
| Thông tin | (145,49)–(287,79) | `0xFD6` 総ターンsố/số tiền trong (146,50); các giá trị được căn phải, `%4d` trong (254,49), `%8d` trong (222,65) |
| Chương | (34,193)–(287,207) | `0xFD7` tập ␣␣ có trong (34.193); số tập `%2d` có trong (48.193); số văn bản tiêu đề `8010F5F1+0x119` nằm trong (82.193), theo sau là `0xFE0`クリア |

Hình chữ nhật xuất phát từ danh sách hiển thị của bố cục (F3DEX2 `G_FILLRECT`, 10,2 điểm cố định), không được đo từ ảnh chụp màn hình.のりかえ cửa sổ bật lên (bố cục 0x86) hình chữ nhật (109,121)–(155,160), hai mục `0xFEC` パイロット (112,123), `0x1002` tiên (112,143), kích thước bước con trỏ 20.

Số văn bản của mục menu `0xFCD`–`0xFD5`：データセーブ、ユニット开Xây dựng, sửa đổi vũ khí, khả năng ユニット, khả năng パイロット, のりかえ, được tăng cườngパーツ, リンク, phụ のマップへ.

## 2. Khung lịch trình

- Mục nhập `801D8F74(mode)`: xóa `D_801DECB8` (màn hình tiếp theo), `D_801DECCC` (màn hình hiện tại), `D_801DD540` (mã thoát), `D_801DD548` (con trỏ menu chính), điều chỉnh khởi tạo menu chính, `8007E810(0x21)` và đăng ký `801D8D20` làm tác vụ trên mỗi khung hình.
- `801D8D20` Đọc trạng thái chuyển tiếp `80099B30()` cho mỗi khung:
- 3 (kết thúc mờ dần): mã thoát 2 → nhập cấp độ tiếp theo (`80080188(0xC)` theo sau là `801D9F74`); mã thoát 1 → thiết lập lại mềm; nếu không hãy xóa sprite và khe văn bản, nhấn `D_801DECB8×8` để kiểm tra `D_801DC9D0` nhằm điều chỉnh việc khởi tạo màn hình.
- -1 (không hoạt động) và `D_8015D9FA & 0x3000 == 0x3000` (cả hai phím được nhấn đồng thời): Thoát mã 1, chuyển tiếp.
- Không phải 0 hoặc 2: điều chỉnh chức năng của từng khung hình của hình ảnh hiện tại.
- Bảng màn hình 23 mục {khởi tạo, từng khung}: 0 menu chính; 1–8 tương ứng với các mục menu 1–8; 9–22 màn hình phụ (10 chi tiết biến hình, 20/21 Tiên のりかえ, 22 do Rinko đạt được). Viết số 0 vào B của mỗi màn hình để quay lại menu chính và các chuyển đổi sẽ luôn là `80099814(5,1,2)`.
- `801D796C`–`801D8CC8` là một chuỗi các khung kiểm tra cũ mà không ai tham khảo.

## 3. Menu chính (Màn hình 0)

| Chức năng | Hiệu ứng |
| --- | --- |
| `801CDF30` Khởi tạo | Mục nhập đầu tiên (`D_801DC240==0`): `80085B94(0,0)` làm sáng nền, `D_801DD5CC=30` độ trễ khung hình; nhập lại: `80085B94(0,1)` làm tối nền, không có độ trễ. Xóa `D_801DEC50` (cờ đã tạo), mờ dần trong `80099814(4,2,0)`. |
| `801CDFB0` Bản dựng | Kiểm tra xem `8010F5F1` có ở trong `D_801DC6D4` (13 cảnh "(trước)" + 132 "アクシズのtấn công và phòng thủ (ở giữa)"): nhấn với bố cục 0x8D, `D_801DECD8=10`; nếu không thì bố cục 0x69, `D_801DECD8=0`. Vẽ các giá trị và tiêu đề chương, xây dựng con trỏ (khe elf 0x14, hình ảnh 0x8E, hoạt ảnh `801C45F4`), `80085B94(0,1)`, `D_801DEC50=1`. |
| `801CE19C` mỗi khung hình | Khi được xây dựng, trước tiên hãy chạy con trỏ `801C4A20` (đọc 0x800/0x400 của `D_801DD62C`, vòng lặp, hiệu ứng âm thanh 0xB9) và **mỗi khung** ghi `D_801DECB8` dưới dạng con trỏ + 1 (hai menu: 0→1, 1→9). Nhàn rỗi và chưa được xây dựng: xây dựng sau khi đếm ngược. Nhàn rỗi và được xây dựng: xem bên dưới. |

Xử lý khóa khi không hoạt động (`D_80178A08`: A=0x8000, B=0x4000):

- `D_801DECD8==0` (toàn menu) Nhấn A, hiệu ứng âm thanh 0xB7:
- Màn hình tiếp theo 9: `D_801DD540=2`, chuyển tiếp (sang cấp độ tiếp theo).
- Màn hình tiếp theo 8 (リンク): `801D9300`, `801D93C4` → `D_801DD114`; nếu bằng 0 thì chuyển sang màn hình 8, nếu không bằng 0 thì chuyển sang màn hình 22.
- Màn hình tiếp theo 6 (のりかえ): Tạo cửa sổ bật lên bố cục 0x86 và khe con trỏ 0x15, `D_801DECD8=1`, không chuyển tiếp.
- Phần còn lại: `801CDE9C` (xóa bộ đệm lựa chọn của từng màn hình phụ) rồi chuyển tiếp.
- `D_801DECD8==1` (のりかえ cửa sổ bật lên): B đóng cửa sổ bật lên (0xB8); `801CDE9C` đầu tiên, con trỏ 0 điều chỉnh `801C5618`, con trỏ 1 điều chỉnh `801C5E64` để tạo danh sách ứng cử viên, trả về 0 và buzz 0xB8 vẫn còn trong cửa sổ bật lên, nếu không thì `D_801DEC60=光标`, yêu tinh đã thay đổi màn hình tiếp theo thành 0x14, chuyển tiếp. Nhánh A không chạm vào trình hướng dẫn bật lên.
- `D_801DECD8==10` (menu hai mục) Nhấn A: Tương tự như "Màn hình tiếp theo 9" hoặc chuyển đổi bình thường.

Hai điểm sẽ hạn chế phương pháp tiếp quản:

1. `80085B94` điều chỉnh `80082334` (giới hạn trên ngẫu nhiên) mỗi lần, **tiêu thụ RNG**, xem bên dưới. Các cuộc gọi đến nó trong quá trình khởi tạo và xây dựng phải được giữ nguyên.
2. `801C5618`/`801C5E64` chỉ ghi bảng ứng viên trong phân đoạn bao phủ (không có `jal`), đây là bảng sẽ được sử dụng sau này trong màn hình のりかえ và có thể được gọi cục bộ.

### Hình nền

Tổng cộng có **8 ảnh**, mỗi ảnh là ảnh được lập chỉ mục 8 bit 320×240 (tài nguyên `0x155E`–`0x1565`), mỗi ảnh có hai bộ 256 bảng màu (`0x1566`–`0x156D`, `0x156E`–`0x1575`). Xác nhận rằng tất cả các bộ giải mã tài nguyên của dự án đã sử dụng đã được giải mã.

`80085A24` Quét nhóm cơ thể của chúng tôi (`8016A210`, 140 vị trí × 0x54, số cơ thể là `+2`), lấy máy nhân vật chính đầu tiên để xác định danh mục; `80085B94(槽, 暗)` Kiểm tra theo danh mục `D_800C59AC` (8 byte/mục: hình ảnh, bảng màu sáng, bảng màu tối, số lượng đề xuất):

| Danh mục | Nhân Vật Chính | Hình ảnh |
| ---: | --- | --- |
| 0 | アシュクリーフ `0x1F` | `0x155E` |
| 1 | ソルデファー `0x1E` | `0x155F` |
| 2 | スヴァンヒルド `0x20` | `0x1560` |
| 3 | ラーズグリーズ `0x21` | `0x1561` |
| 4 | アースゲイン `0x22` | `0x1562` |
| 5 | スーパーアースゲイン `0x132` | `0x1563` |
| 6 | スイームルグ `0x24` | `0x1564` |
| 7 | スイームルグS `0x133` | `0x1565` |
| 8 | Máy nhân vật chính không thể tìm thấy | Cùng loại 0 |

Vì vậy, bối cảnh không thay đổi theo số tập mà chỉ thay đổi theo máy của nhân vật chính (bao gồm cả hai mẫu nâng cấp sẽ được chuyển sang sau). Mỗi số ứng cử viên là 1, `80082334(1)` luôn nhận được 0, nhưng bản thân cuộc gọi vẫn nâng cao RNG; nhánh "chọn một trong chín" thuộc loại 9 không có trong trò chơi này. Bảng màu sáng được sử dụng khi vào lần đầu tiên và bảng màu tối được thay đổi khi menu được xây dựng và khi quay lại từ màn hình phụ và bản thân hình ảnh vẫn không thay đổi. Nền được vẽ ở khe sprite 0, `80098158(槽, 0, 4, 0xA4, 0, 图, 调色板, 0)`.

## 4. Tiếp quản mục tiêu

1. **Giao diện không thay đổi, rõ ràng và ngôn ngữ được hiện đại hóa. ** Giữ nguyên hình nền, tỷ lệ vị trí của bốn tấm, đáy mờ màu xanh đậm, các cạnh mỏng màu xanh lam, các thanh đánh dấu màu xanh lá cây và văn bản màu trắng; sử dụng phông chữ vector, thực hiện theo tỷ lệ cửa sổ và văn bản sẽ nằm trong thư mục tiếng Trung/tiếng Nhật/tiếng Anh. Không thay đổi sang thiết kế kiểu thẻ mới (việc sắp xếp lại toàn trang như trang Rinko không áp dụng ở đây).
2. **Không thay đổi quy trình. ** Điều gì xảy ra sau khi chọn mục nào (kiểm tra, hiệu ứng âm thanh, chuyển tiếp, RNG, mã thoát) vẫn được xác định bởi chức năng ban đầu; lớp thích ứng chỉ thay thế "vẽ" và "khóa đọc".
3. **Cả chuột và bàn phím đều có thể hoàn thành mọi thao tác** và hành vi B/Esc nhất quán với phiên bản gốc (B trên menu chính không hợp lệ và B trong cửa sổ bật lên bị đóng).
4. Có thể tắt: Chọn phiên bản gốc (`intermission_ui` của `presentation.json`, giao diện gỡ lỗi `settings {"intermission_ui": "original"}`) trong "Màn hình liên trường" trên trang cài đặt. Nó sẽ có hiệu lực khi màn hình tiếp theo được xây dựng. Trang gốc đã mở sẽ bị đóng khi rời khỏi; `SRW64_NATIVE_INTERMISSION=0` hoặc nếu hồ sơ không được tải, màn hình gốc sẽ được giữ lại trong toàn bộ quá trình chạy. Tập lệnh xác minh `tools/recomp/debug/check_intermission_ui_switch.py` (2026-09-23, `build/recomp/debug/20260923T025544.572614Z/`, 8 mục đã vượt qua, mã thoát 0: Khi menu gốc mở, chuyển sang phiên bản gốc, nhập chuyển đổi ユニット, danh sách ban đầu xuất hiện, B quay lại menu gốc; sau khi chuyển về phiên bản mới, Z vào danh sách gốc, B quay lại menu gốc và con trỏ vẫn ở đó cóユニット chuyển đổi; `presentation-settings.json` theo sau là viết `intermission_ui`; 2026-09-23 `build/recomp/debug/20260923T045406.607280Z/` 9 mục đã được thông qua, được thêm vào menu gốc và đi lên リンク Màn hình liên kết ban đầu xuất hiện thay vì trang liên kết gốc).

Ngoài phạm vi của trang này: Tám màn hình phụ vẫn là màn hình gốc (ngoại trừ trang đầu Rinko). Sẽ có một công tắc giao diện khi vào màn hình phụ ban đầu từ menu chính gốc, đây là trạng thái chuyển tiếp đã biết để tiếp quản theo từng giai đoạn.

## 5. Kế hoạch tiếp quản

Làm theo mẫu của trang trước chiến tranh: bộ điều hợp luồng trò chơi xuất bản ảnh chụp nhanh JSON, `frontend.cpp` ảnh chụp nhanh chỉ đọc, trả về các hành động ngữ nghĩa theo chuỗi và không đọc RDRAM.

**Hook** (hai mục mới được thêm vào `NATIVE_HOOKS` của `generate_cpu.py` và mã CPU cần được tạo lại sau khi sửa đổi):

| Chức năng gốc | Hành vi đóng gói |
| --- | --- |
| `801CDFB0` Bản dựng | Không điều chỉnh chức năng ban đầu. Sao chép phần không vẽ của nó: xác định hai mục menu và viết `D_801DECD8`, `80085B94(0,1)`, `D_801DEC50=1`. Không có bố cục, văn bản và con trỏ nào được tạo nên bảng gốc sẽ không xuất hiện và nó sẽ không chiếm vị trí sprite hoặc vị trí văn bản. Sau đó xuất bản ảnh chụp nhanh và trang sẽ hiển thị. |
| `801CE19C` mỗi khung hình | Đầu vào đã được lọc về 0 trong khi trang hiển thị và hàm ban đầu được gọi như bình thường (nó sẽ chỉ ở chế độ chờ và làm mới `D_801DECB8`). Nhận `choose:N`: viết `D_801DD548=N`, cho `D_80178A08` cạnh A, điều chỉnh chức năng ban đầu và khôi phục `D_80178A08`. Đã nhận `move:N`: Viết con trỏ và phát âm thanh chuyển động ban đầu 0xB9, để con trỏ ở lại trong trò chơi và dừng ở mục gốc khi quay lại từ sprite. |

Quá trình khởi tạo `801CDF30` không được kết nối: nền, độ trễ 30 khung hình và độ mờ dần vẫn không thay đổi.

Lưu ý rằng hàm trên mỗi khung ban đầu được gọi là `801C4A20` cho vị trí 0x14 khi nó được tạo. Nó chỉ có hai nhánh, `0x800` và `0x400`. Nếu không có nhánh nào chạm vào, nó sẽ trả về trực tiếp và ghi số 0 (được xác nhận bằng quá trình tháo gỡ); `D_801DD62C` của khung nơi cạnh A được đưa vào vẫn bằng 0. Do đó, an toàn là không tạo hình con trỏ.

Hàm ban đầu chỉ xử lý A khi `80099B30()==-1`. Bộ điều hợp phải thực hiện hành động trong cùng điều kiện, nếu không nó sẽ được chuyển sang khung tiếp theo và không thể bị mất.

**のりかえ**: Trang gốc tự hiển thị menu phụ "Driver/Fairy" và cửa sổ bật lên ban đầu không được tạo. Khi xác nhận, bộ điều hợp ghi `D_801DECB8=6`, `D_801DECD8=1`, `D_801DEC58=选择`, tiêm A và điều chỉnh chức năng ban đầu; nó hoàn tất việc kiểm tra `D_801DEC60`, số ảnh và quá trình chuyển đổi. Nếu quá trình chuyển đổi không bắt đầu sau khi quay lại (ứng cử viên trống và phiên bản gốc đã được phát), hãy đặt lại `D_801DECD8` thành 0 và trang sẽ vẫn mở và nhắc rằng trang này không khả dụng. Nâng cao: Khi mở menu phụ, trước tiên hãy điều chỉnh cục bộ hai chức năng của bảng ứng cử viên và tô xám chức năng trống.

**リンク**: Không có xử lý đặc biệt, hàm ban đầu sẽ tự lấy nhánh `801D9300/801D93C4` sau cạnh A, sau đó trang リンク hiện tại sẽ tiếp quản.

**Trường ảnh chụp nhanh**: `serial`, `visible`, `restricted` (menu hai mục), `cursor`, `turns` (`8010F5EC` u16), `funds` (`8010F5F4` u32), `episode` (`8010F5EF`), `scene` (`8010F5F1`), `title_key` (`base:t00_{281+scene}`), `submenu` (のりかえ trạng thái menu phụ).

**Thời gian hiển thị**: `D_801DECCC==0` hiển thị khi nó được tạo và mã thoát là 0; khi hành động được gửi (quá trình chuyển đổi bắt đầu), nó sẽ bị ẩn và đi vào cổng nhả khóa. Hiệu ứng fade in và fade out vẫn là hiệu ứng nguyên bản trong màn chơi. Bản thân trang này thực hiện một quá trình chuyển đổi độ mờ ngắn để căn chỉnh cho phù hợp với nó; nó không theo đuổi việc đồng bộ hóa từng khung hình.

**Đầu vào**: `host.cpp` Thêm `intermission_page::input` vào chuỗi bộ lọc; thêm một kênh vào mỗi kênh trong số `sync/choose/dispatch/summary` của `frontend.cpp`, song song với liên kết/trận chiến. Các phím mũi tên và chuyển động theo chu kỳ Tab (giữ lại chu trình từ đầu đến cuối ban đầu), xác nhận Enter/Z và Esc/X chỉ hợp lệ trong menu phụ.

**Tổ hợp phím reset mềm**: Phiên bản gốc đọc và giữ trạng thái `D_8015D9FA` trong bộ lập lịch. Sự kết hợp này sẽ được ăn khi trang có đầu vào. Giải pháp: Bộ lọc cho phép "nhấn và giữ hai phím cùng lúc" và không tạo mục nhập thay thế gốc.

## 6. Thông số trực quan

- Sử dụng tọa độ thiết kế 320×240, tỉ lệ cân xứng theo cạnh ngắn của cửa sổ, sử dụng hình chữ nhật Mặt cắt 1 cho 4 ô; tập trung toàn bộ ở tỷ lệ cửa sổ khác với 4:3 và nền vẫn được trò chơi vẽ.
- Bảng điều khiển: đáy mờ màu xanh đậm (lấy cảm giác ban đầu, khoảng `rgba(10,14,60,0.78)`, điều chỉnh cho phù hợp với ảnh chụp màn hình khi thực hiện), viền xanh 1 pixel thiết kế (khoảng `#3A78E0`), góc vuông.
- Thanh đánh dấu: thanh liền màu xanh lục nguyên bản (khoảng `#00C800`), chiều rộng bằng chiều rộng của bảng menu và văn bản vẫn giữ nguyên màu trắng; sử dụng cùng màu và độ trong suốt thấp khi di chuột để tránh nhầm lẫn với mục hiện tại; màu di chuột chỉ được hiển thị sau khi chuột thực sự được di chuyển hoặc nhấp vào và được rút lại ngay khi nhấn nút hoặc tay cầm (`pointer_mode` của `frontend.cpp`, `pointer_mode` của nội dung trang lớp `pointer`), nếu không, con trỏ được đặt trong cửa sổ sẽ giữ một dòng nhất định với thanh màu xanh lục nhạt (được phát hiện bởi người dùng 2026-09-25 trên đường đua danh sách).
- Phông chữ: Thực hiện theo khám phá phông chữ có trong giao diện người dùng được chia sẻ; chiều cao phông chữ được thiết kế là 16 pixel và khoảng cách dòng khoảng 13–14. Nếu tiếng Trung và tiếng Anh quá rộng, hãy thu hẹp khoảng cách ký tự trước rồi giảm bớt. Không ngắt dòng hoặc mở rộng bảng (tiếng Anh "Khả năng thí điểm" là mục dài nhất và cần phải đo).
- Các giá trị được căn phải về vị trí ban đầu; quỹ giữ lại đường cơ sở căn chỉnh độ rộng 8 bit mà không cần thêm phần nghìn (phù hợp với màn hình gốc và màn hình đã sửa đổi).
- Định dạng dòng chương tuân theo mẫu mục lục, chẳng hạn như `第{n}话 {title} 通关` và tiêu đề sẽ trở lại tiếng Nhật khi không được dịch.
- Hiện đại hóa chỉ bổ sung thêm hai thứ: một nút nhắc rất nhẹ ở dòng dưới cùng (giống như trang Rinko) và một mô tả một câu tùy chọn về mục hiện tại; cả hai đều không vào bốn bảng và chúng lần lượt tương ứng với bảng gốc sau khi chúng bị tắt.

## 6a. Điều chỉnh trực tiếp quỹ (2026-09-22)

Số quỹ trong menu chính và màn hình chuyển đổi là một nút: sau khi nhấp vào, vị trí ban đầu sẽ trở thành hộp nhập liệu (số cũ được chọn). Sau khi nhập số nguyên từ 0 đến 99999999, Enter ngay lập tức ghi `D_8010F5F4` và Esc hủy. Quá trình viết được hoàn thành trên chuỗi trò chơi (hành động bộ điều hợp `funds:N`, `intermission_menu.hpp::parse_funds` kiểm tra), trang và các phán đoán chuyển đổi tiếp theo sẽ đọc số mới; bản ghi nhật ký sự kiện `{"kind":"funds"}`. Đây là một chức năng tiện lợi của MOD tích hợp. Nó không được điều khiển bởi công tắc quy tắc và không đưa ra phán đoán về tính hợp pháp vượt quá giới hạn trên (chiều rộng hiển thị ban đầu là 8 chữ số, do đó giới hạn trên là 99.999.999).

Giao diện gỡ lỗi: `ui.click --text intermission-funds` (màn hình đổi mới `upgrade-funds`) → `ui.type 900000` → `ui.key return`; `tools/recomp/debug/check_funds.py` bao gồm sửa đổi menu chính, hủy Esc, năm sửa đổi màn hình, cửa sổ xác nhận/tiền và khoản khấu trừ dựa trên số mới (8 Nếu mục nhập vượt qua, hãy chạy `build/recomp/debug/` (xem đầu ra tập lệnh).

## 7. Bản địa hóa

- `entries` của `content/locales/*.json` hiện không có sẵn `t00_04044`–`04055` (tiêu đề, chín mục, thẻ thông tin, chương ␣␣), `04064` (クリア), `04076`/`04098` (パイロット/ nàng tiên). Cần có bản dịch tiếng Trung và tiếng Anh; văn bản nguồn tiếng Nhật là bắt buộc.
- Tiêu đề chương `t00_00281`+: khoảng 140 mục. Mục lục hiện tại chỉ bao gồm bản thảo đầu tiên của chương. Chúng tôi không chịu trách nhiệm hoàn thiện trang này và sẽ trả lại trang này bằng tiếng Nhật nếu không được dịch.
- Đặt thẻ `ui` trong bản sao mẫu (tập thứ n, dấu nhắc chính và lý do không có sẵn) và tiền tố tên khóa là `intermission_`.

## 8. Kế hoạch xác minh

Tĩnh và các thành phần:

- "Xác định hai menu" của bộ điều hợp được viết dưới dạng các hàm thuần túy và các thử nghiệm đơn vị được thực hiện trên 14 số cảnh cộng với một số giá trị không trúng đích (kiểu `tests/native_*.cpp`).
- `test_*` Đã thêm: `NATIVE_HOOKS` chứa hai móc mới, `game_hooks.cpp` có bao bì tương ứng (bắt chước `test_link_battler.py`).

Chạy (cần phải có sự đồng ý trước; tiếp tục sử dụng giao diện gỡ lỗi):

1. `srw64ctl launch --save build/recomp/save-recovery-check/intermission-cold-1.source.sram`, đọc tệp qua vòng tiêu đề và vào địa điểm.
2. `ui.tree` Khẳng định: danh hiệu, 9 mục, vòng 7, quỹ 14500, `第 1 话 …`; ảnh chụp màn hình được so sánh thủ công với đường cơ sở ban đầu cạnh nhau để biết vị trí của bảng điều khiển.
3. Nhập từng mục và nhấn B để quay lại: trang sẽ xuất hiện lại mỗi lần và con trỏ sẽ dừng ở mục gốc (`D_801DD548` ban đầu không bị xóa).
4. のりかえ Menu phụ: tài xế, yêu tinh (không nên có yêu tinh trong kho lưu trữ tập đầu tiên → còi, trang vẫn còn đó), Esc để đóng.
5. リンク → Trang liên kết gốc → Quay lại → Menu chính.
6. Submariner: Thoát mã 2, vào cấp độ tiếp theo.
7. Hai menu: yêu cầu lưu sau cảnh "(trước)". Đầu tiên hãy tìm một kho lưu trữ làm sẵn; nếu không, hãy sử dụng công cụ chỉnh sửa lưu trữ để thay đổi byte cảnh thành 38 để tạo mẫu được kiểm soát và cho biết đó là mẫu đã chỉnh sửa trong báo cáo.
8. Ba ngôn ngữ × 800×600/960×720/1100×760; điều khiển cổng nhả sau khi nhấn và giữ Z để xác nhận; menu chính không phản hồi khi lớp phủ trang cài đặt được mở.
9. So sánh RNG: Cùng một kho lưu trữ, cùng một chuỗi đầu vào, chạy phiên bản gốc và tiếp quản mỗi lần một lần và so sánh trạng thái RNG khi vào màn hình phụ (xác minh rằng số lượng cuộc gọi `80085B94` không thay đổi).

## 9. Tình trạng và các bước thực hiện

Đã hoàn thành (2026-09-21):

- [`intermission_page.cpp`](../../src/host/intermission_page.cpp): Xây dựng/ba lệnh gọi lại trên mỗi khung/ranh giới khung, ảnh chụp nhanh, hành động, nhật ký sự kiện `intermission-events.jsonl`; logic thuần túy trong [`intermission_menu.hpp`](../../src/host/intermission_menu.hpp).
- [`game_hooks.cpp`](../../src/host/game_hooks.cpp), `generate_cpu.py`: hai móc; `host.cpp` chuỗi bộ lọc đầu vào; `status.intermission_page` trong số `debug_server.cpp`.
- [`frontend.cpp`](../../src/native/ui/frontend.cpp): Bốn bảng được định vị bằng nhau theo tọa độ 320×240, văn bản được tự động thu nhỏ theo độ rộng của bảng (các mục menu tiếng Anh rộng hơn tiếng Nhật), menu phụ のりかえ, thao tác bàn phím và chuột.
- Danh mục tiếng Trung và tiếng Anh được bổ sung 15 văn bản và 4 thẻ `intermission_*` bằng mỗi ngôn ngữ trong số ba ngôn ngữ.
- Kiểm tra: `make recomp-intermission-test` (hai phán đoán menu, lọc đầu vào, ASan/UBSan) đã đạt; `tests/test_intermission_page.py` (móc nối dây, nhãn, bảng điều khiển hình chữ nhật/bảng cảnh/bảng nền trong ROM) đã đạt; tệp C++ đã sửa đổi chỉ được kiểm tra cú pháp bằng các tham số biên dịch của máy chủ.

实机验证（2026-09-21，`intermission-cold-1` 第一话通关存档，经标题环读档）：

```sh
.venv/bin/python tools/recomp/debug/check_intermission.py            # 构建并检查
.venv/bin/python tools/recomp/debug/check_intermission.py --reuse-build
```

Đang chạy `build/recomp/debug/20260921T140756.835850Z/`: `intermission-checks.json` đã vượt qua 12 mục, mã thoát 0.

| Kiểm tra | Kết quả |
| --- | --- |
| Dữ liệu | Vòng 7, Quỹ 14500, Tập 1, Cảnh 1, Thực đơn chín món, không hai món |
| 光标 | ↑ 从首项绕到末项，↓ 绕回；音效走原版 0xB9 |
| のりかえ | Z mở menu phụ; chọn yêu tinh (không có yêu tinh trong tập đầu tiên). Tiếng bíp ban đầu, trang vẫn ở menu phụ và lời nhắc; X đóng |
| 子画面 | 鼠标点 「ユニット改造」进原版改造画面，B 返回后页面重新出现（serial 增加），光标停在原项 |
| リンク | Để nó ở trang liên kết gốc và con trỏ sẽ dừng ở リンク sau khi Esc quay lại |
| Ngôn ngữ | Sau khi chuyển sang tiếng Trung và tiếng Anh, văn bản menu sẽ được cập nhật ngay lập tức; Các mục menu tiếng Anh sẽ tự động được giảm xuống cỡ chữ nhỏ |
| 次のマップへ | 退出码 2,页面关闭、输入归还,随后进入下一话对白 |

Ngoài ra, tôi thấy cửa sổ 800×600 (tiếng Anh) trong phiên hướng dẫn sử dụng đầu tiên và bốn bảng và văn bản đều nằm trong phạm vi.

**Chưa được xác minh**:

- 两项菜单（`（前)」场景之后)没有现成存档,只有组件测试覆盖判定；页面的两项布局没实机看过。
- Điều khiển RNG (mục 8, mục 9) không chạy. Móc xây dựng được điều chỉnh một lần thành `80085B94(0,1)` như hiện tại. Chức năng của mỗi khung là chính chức năng ban đầu, phải nhất quán theo cấu trúc, nhưng đây không phải là thử nghiệm thực tế.
- Tổ hợp phím soft reset mới chỉ được ra mắt qua thử nghiệm linh kiện và chưa được ép trên máy thật.
- Cổng nhả điều khiển nhấn phím xác nhận theo cơ chế của các trang khác và chưa được thử nghiệm riêng.
- Các thông số hình ảnh (màu nền `#0a0e3c` 78%, màu cạnh `#3a78e0`, vùng sáng `#00c800`) được xác định dựa trên ảnh chụp màn hình gốc và màu không được lấy từ tài nguyên ảnh gốc.

Từng bước ban đầu (hoàn thành 1–4):

1. Bộ điều hợp `intermission_page.{hpp,cpp}` + hai móc + lọc đầu vào, trước tiên xuất bản ảnh chụp nhanh và chỉ vẽ các bảng tĩnh không tương tác trên trang. Đảm bảo rằng bảng gốc biến mất và nền và độ mờ là bình thường.
2. Tương tác: di chuyển, xác nhận, chuột; thực đơn phụ; cửa xả; phát hành thiết lập lại mềm.
3. Các mục nhập được bản địa hóa và thẻ `ui`; sắp chữ ba ngôn ngữ.
4. Các trường giao diện gỡ lỗi (`status.intermission_page`, ID ổn định `intermission:0..8`, `intermission-swap:0|1`, điều kiện chờ `intermission_page`, nhật ký sự kiện `intermission`) và tập lệnh kiểm tra [`check_intermission.py`](../../tools/recomp/debug/check_intermission.py).
5. Xác minh, bài viết này được viết lại thành văn bản thực hiện.

Các trang tiếp theo: biến đổi ユニット/chuyển đổi vũ khí ([Chiếm màn hình chuyển đổi](native-upgrade-screens.md)), tăng cường パーツ ([tăng cường パーツ Chiếm màn hình](native-parts-screens.md)), khả năng ユニット/khả năng パイロット([Chiếm quyền kiểm soát màn hình khả năng xem](native-ability-screens.md)), のりかえ ([のりかえ chiếm quyền kiểm soát màn hình](native-swap-screens.md)) và Việc chiếm quyền kiểm soát màn hình データセーブ([データセーブ](native-save-screens.md)) đã được thực hiện qua ; trang リンク (`link_page.cpp`) cũng đã trả về màn hình liên kết ban đầu với các cài đặt tương tự. Giờ đây, tất cả các cảnh liên trường có thể được chuyển đổi giữa phiên bản gốc và phiên bản gốc.

## 10. Các vấn đề mở

- Mục đích của màn hình 22 không được đọc (mục リンク được nhập khi `801D93C4` khác 0, được coi là màn hình nhắc).
- Đường viền bảng được vẽ bởi `80098158` sử dụng hình ảnh `0x499/0x50F/0x511`. Màu sắc và độ rộng đường kẻ chính xác phải được lấy từ ảnh gốc đã xuất, không được ước tính từ ảnh chụp màn hình.