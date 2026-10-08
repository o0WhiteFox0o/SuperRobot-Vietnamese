> **Ngôn ngữ / Language:** [Tiếng Việt](cheats.vi.md) · [English](cheats.en.md) · [中文](cheats.md)

# ngón tay vàng

Ngày: 2026-10-05. Trang "Gian lận" của cửa sổ cài đặt (sau "Quy tắc") đều bị đóng theo mặc định; hàng cấp độ thí điểm được đóng theo mặc định. Nhấp vào "Mở rộng" để liệt kê các phi công. Nội dung là sáu mục được xác định bởi người dùng. Tất cả đều được tự thực hiện theo các trường và giới hạn trên trong mã gốc. Mã GameShark không được đọc và `.cht` của RetroArch không được nhập. Mã: `src/host/cheats.hpp` (trường, giới hạn trên và quy tắc ghi cho từng khung), `src/host/cheats.cpp` (móc, danh sách thử nghiệm, cấp độ thay đổi), giao diện nằm trong `cheats_page` của `frontend.cpp` (trạng thái mở rộng không được lưu và cài đặt sẽ được thu gọn mỗi khi mở) và công tắc được lưu với `cheats` của `presentation-settings.json`.

## 1. Tại sao không sử dụng mã libretro?

Chỉ có 7 `cht/Nintendo - Nintendo 64/Super Robot Taisen 64 (Japan).cht` cơ sở dữ liệu libretro và không ai trong số chúng có thể có hiệu lực theo tên khi được kiểm tra theo mã (`mupencheat.txt` của mupen64plus không có cái này):

| mục | mã | thực tế |
| --- | --- | --- |
| Kích hoạt mã | `F10C0FE0 2400` | Thay đổi đoạn mã cư trú (`80076610`–`800C34B0`); các hướng dẫn đã thay đổi không hợp lệ sau khi biên dịch lại. Máy nguyên bản đã được GameShark thử nghiệm |
| Hai chất kích hoạt | `D00F97B0`／`D00F97B1`／`D10F97B0` | Chỉ cần điều kiện "khi nhấn phím" (`800F97B0` là `OSContPad`), chỉ mở nó ra sẽ không có tác dụng gì |
| Tiền | `8110F5F6 0000` | Quỹ `8010F5F4` là u32 (chỉ lw/sw trong toàn bộ quá trình). Điều này xóa nửa từ dưới và giảm số tiền |
| Cuộc sống | `8116A214 00A0`+`8116A268 0000` | Ví dụ cơ thể +4 là HP hiện tại (`800A55D0` được lấp đầy bởi +6): Khe 0 HP được đặt thành 160, khe 1 được đặt thành 0 |
| Năng lượng | `811613F2 00A0`+`811613FA 0000` | Rơi vào nhóm trình hướng dẫn số `801613E0` (20 × 8 byte), chỉ thay đổi số được hiển thị |

## 2. Sáu mục

| Mục | Viết gì | Cơ sở |
| --- | --- | --- |
| Số tiền tối đa | `8010F5F4` = 99.999.999 mỗi khung hình | Không có giới hạn cao nhất cho cách thêm tiền (`3D5B``800A0D24`, loại bỏ thu nhập `801FC5E8`, quỹ đạo cụ `801D5CE0`, bán); tất cả số tiền được hiển thị dưới dạng `%8d`. Khấu trừ cuối cấp `8020DA98` Xét theo dấu thì tiền không thể đạt 0x80000000, 99.999.999 là xa |
| Tất cả 9 phần nâng cao | Viết số lượng của 18 loại phần (`8015E990`, mỗi u16: byte cao được giữ, byte thấp được trang bị) trong mỗi khung là max(9, in Equipment) | Số loại 0x12 (`800A8BC8`); chỉ giảm khi được giữ + được tính + rơi vào trường này < 9 Khi được ghi (`801F88C0`), số lần giữ của màn hình phần chỉ rộng một bit (`801CBEB4`). Phiên bản gốc sẽ không còn rơi ra các phần sau khi đầy. `8015E9B4` là ngưỡng của đạo cụ tài chính, đừng chạm vào nó |
| EN của chúng tôi không bị giảm | Viết +8 = +0xA vào nhóm nội dung của chúng tôi (`8016A210`, 140 × 0x54, +0 ≠ 0) mỗi khung hình | Vũ khí EN được trừ trực tiếp từ phiên bản +8 (`801FC8D8`), không sao chép; đầy đủ vô điều kiện thay vì "bù ít hơn", vì khoản hoàn trả cho chuyển động bị hủy (`801CC1F0`) và hoạt ảnh khôi phục từng khung hình sẽ nhanh chóng vượt quá giới hạn trên |
| SP không giảm | Viết +0x16 = +0x18 vào bảng điều khiển của chúng tôi (`80172F40`, 100 × 0x4C, +0 ≠ 0) mỗi khung hình | Tiêu hao tinh thần chỉ được trừ trực tiếp tại `801E195C` +0x16 |
| Công suất 150 | Viết +0x20 = 150 trong cùng một bảng, bỏ qua trình điều khiển có hai bit trên của +4 (0xC0) được đặt | 150 là giới hạn trên không đổi của tất cả các đường dẫn điện (`801FAD58`, `801E1460`), không có sự phân biệt đối với con người; `801F12D0` so với 0xC0 Phi công ở vị trí không đặt lại hoặc mất sức. Chưa rõ nghĩa vẫn bị bỏ qua |
| Đánh giá phi công | Xem §3 | |

Việc ghi từng khung được thực hiện trong móc ranh giới khung `80085F30` (`srw64_game_hooks.cheats_frame`). Tắt công tắc sẽ không ghi nữa và các giá trị đã ghi sẽ không thay đổi.

Tác dụng phụ: Khi sức mạnh được cố định ở mức 150, linh hồn "chỉ có thể sử dụng được nếu sức mạnh dưới 150" (như Jihe, khu vực `801EFEA4`, cần xác minh) sẽ chuyển sang màu xám. Hiệu ứng của Super Mode, Mirror Shisui, V-MAX và Clone với sức mạnh bắt đầu từ 130 sẽ luôn có hiệu lực.

## 3. Thay đổi cấp độ thí điểm

- **Cấp độ được rút ra từ kinh nghiệm**: +0x12 là kinh nghiệm tích lũy (u16), cấp độ = min(kinh nghiệm / 500 + 1, 99) (`800A630C`) và giới hạn trên của kinh nghiệm là 49.000 (`801FC0E4`). Kho lưu trữ của mỗi người chỉ lưu số nhân vật, điểm kinh nghiệm, số lần tiêu diệt và vị trí cơ thể (`800923B4`), số này sẽ được xây dựng lại dựa trên kinh nghiệm khi tải tệp (`800A8E0C` → `800A7F8C(record, 1)`). Vì vậy nếu bạn chỉ viết +5 mà không trải nghiệm thì việc tải file sẽ đưa bạn về mức ban đầu.
- **Cách viết gốc** (`800AC220`, người mới tham gia bù vào cấp cơ sở): +5 = L, +0x12 = (L − 1) × 500 (`800AC340`–`800AC368`), sau đó `800A7F8C(record, 1)`. Người chủ nhà làm như được bảo.
- **`800A7F8C` là một bộ tính toán lại hoàn chỉnh**: viết lại sáu khả năng, địa hình, giới hạn trên SP, các khe kỹ năng từ bản ghi cơ bản (`D_800CA9C4[人物]` → ROM `0x7A1A0`), sau đó thêm (L − 1) mức tăng trưởng cố định vào `800A6238` (chiến đấu, bắn súng, phản ứng, kỹ năng +1 mỗi cái, tránh, đánh, giới hạn SP trên mỗi +2), tinh thần được nạp lại theo cấp độ tiếp thu +0x0A/+0x0B (`800A63E0`), cấp độ kỹ năng được nạp lại theo ngưỡng +6/+7/+8 (`800A6340`) và cấp độ hành động thứ hai được ghi là +0x34. Khi a1 = 1, SP và số hành động trong vòng này được lấp đầy, tương tự như việc tải. Điều này cũng đúng với việc hạ cấp.
- **Chỉ được thực hiện trong menu liên trường**: Yêu cầu được xếp hàng đầu tiên, trước mỗi bước của menu liên trường (`801CE19C` trình bao bọc, `srw64_game_hooks.cheats_intermission`) và được thực thi sau khi màn hình mờ dần kết thúc (`8015E9C5` = −1). Khi trò chơi không ở giữa các trò chơi, trang này cho biết "Bạn chỉ có thể sửa đổi cấp độ sau khi quay lại menu trò chơi", nhưng nút không xuất hiện.
- **Danh sách ai**: Giống như danh sách thí điểm ban đầu `801C549C`, bảng của chúng tôi có +0 ≠ 0 và không có bản ghi 0x80 bit; tên là văn bản `0x111E + 人物号`.
- **Phần thưởng siêu chế độ của G Gun Fighter** (`801FEB70`, trong lớp phủ chiến thuật) sẽ bị loại bỏ khi tính toán lại và sẽ được bổ sung ngay sau khi phiên bản gốc được nâng cấp sau chiến tranh; nó cũng sẽ không khả dụng khi tải tệp và sẽ được khôi phục theo quy tắc ban đầu sau khi vào bản đồ. Việc thay đổi cấp độ giữa các trò chơi phù hợp với việc tải tệp.
- Việc thay đổi cấp độ sẽ ảnh hưởng đến chuẩn cấp độ của địch cho các cấp độ tiếp theo (`D_8010F5F3`, khi vào bản đồ chiến thuật lấy trung bình của 15 phi công đứng đầu bên ta, `800A4BE0`).

## 4. Lưu trữ và chuyển đổi

- Quỹ, bộ phận và cấp độ được ghi về trạng thái riêng của trò chơi và được lưu cùng nhau khi người chơi lưu trò chơi. Do người dùng xác định: **Việc sử dụng mánh gian lận sẽ không được ghi lại trong kho lưu trữ**.
- Switch được lưu trong `cheats` của `presentation-settings.json` (danh sách id: `funds`, `parts`, `en`, `sp`, `morale`) và sẽ được sử dụng ở lần khởi động tiếp theo. Các lần chạy gỡ lỗi có thể sử dụng biến môi trường `SRW64_CHEATS=funds,en` thay vì danh sách đã lưu.
- Các sự kiện được ghi vào `cheat-events.jsonl` trong thư mục đang chạy (trước và sau khi thay đổi switch và thay đổi cấp độ).

## 5. Xác minh

- Tĩnh: Các địa chỉ trên và giới hạn trên đều là từ việc tháo gỡ (hai vòng xác minh tĩnh, 2026-10-05).
- Đơn vị: `make recomp-cheats-test` (`tests/native_cheats.cpp`) Kiểm tra từng khung quy tắc viết và chuyển đổi cấp độ/kinh nghiệm.
- Máy thực tế (2026-10-05, `tools/recomp/debug/check_cheats.py`, đang chạy `build/recomp/debug/20261005T064406.061075Z`, vượt qua tất cả 12 hạng mục): Tập đầu tiên của trò chơi được đọc vào trò chơi và trang "Quy tắc" được đặt (vị trí hiện tại) để liệt kê 4 phi công; Manami 2 → Cấp 12: 5.500 kinh nghiệm, sáu khả năng +1/+1/+2/+2/+1/+1 Ở mỗi cấp độ, giới hạn SP trên +20 và được bổ sung, tinh thần 1 → 4, sau đó giảm trở lại cấp 2 để phù hợp với giá trị ban đầu; sau khi bật năm công tắc, quỹ là 99.999.999, 18 loại bộ phận giữ 9; thay đổi thủ công EN, SP thành thấp và cường độ thành 100 và quay lại giới hạn trên/150 trong khung tiếp theo; sau khi lưu ở cột 2, danh sách lưu trữ hiển thị cấp 12, kinh phí 99.999.999 (danh sách dựa trên cấp độ kinh nghiệm đã lưu).
- Đổi sang trang "gian lận" riêng, mặc định đóng cấp độ thí điểm rồi chạy lại (chạy `build/recomp/debug/20261005T065348.468538Z`, hết 13 mục đều pass, và có thêm mục "không có hàng thí điểm khi mở trang").
- Không có chiến đấu thực tế: việc tiêu thụ EN và SP trong trận chiến chỉ được xác nhận tĩnh (trừ trực tiếp từ phiên bản, không có bản sao) và "150 sức mạnh làm cho sự kết hợp màu xám" chưa được nhìn thấy trong chiến đấu thực tế.