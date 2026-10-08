> **Ngôn ngữ / Language:** [Tiếng Việt](controls-remapping.vi.md) · [English](controls-remapping.en.md) · [中文](controls-remapping.md)

# Thay đổi phím

28-09-2026. Yêu cầu của người dùng: Cài đặt nút cộng với so sánh sơ đồ bộ điều khiển, cộng với các nút bổ sung của trò chơi này, có thể được xác định và đặt bằng một cú nhấp chuột. Quy trình: Đầu tiên, tôi sử dụng sơ đồ bộ điều khiển N64 do người dùng cung cấp (hai phiên bản, phiên bản thứ hai đã thêm L2/R2 ảo dưới L/R và nhãn cho mỗi hướng trong số bốn hướng của phím chéo); Sau khi đọc [phân tích nút gốc](../gameplay/original-controls.md), người dùng cho rằng phiên bản gốc không có nhiều phím hữu ích nên đã đổi thành **sắp xếp theo chức năng** và bố cục của Steam Deck ("Chỉ cần sử dụng steamdeck" "), hình do chính chúng tôi vẽ theo phong cách phẳng do người dùng đưa ra (nền xám đậm, hình nút màu trắng, tên phím ghi trên hình). Cùng ngày, người dùng quyết định không chụp ảnh ("Tôi vẫn cảm thấy không muốn chụp ảnh"): bộ điều khiển sẽ được thiết lập là Steam Deck theo mặc định và bàn phím sẽ được thiết lập là PCSX2 theo mặc định.

- Sau khi đổi key, trang gốc sẽ theo key mới, và luôn có sẵn các phím Enter, Esc, mũi tên;
- Joystick không cần thay riêng (người dùng: không cần joystick), "di chuyển" như phím chéo;
- Các giá trị mặc định của bộ điều khiển được sắp xếp lại theo chức năng. Bàn phím mặc định có bố cục của PCSX2, ở cùng vị trí và chức năng với bộ điều khiển (xem phần "Dữ liệu" bên dưới);
- Trang thao tác chỉ có menu và không có sơ đồ tay cầm.

## Dữ liệu

[`input_bindings.hpp`](../../src/host/input_bindings.hpp) (không dựa vào SDL, mã khóa và số bộ điều khiển theo SDL, kiểm tra với `static_assert` trong `graphics.cpp`):

- **Hành động**: A, B, Z, START, L, R, C bốn chiều, D-pad bốn chiều, cần điều khiển bốn chiều của N64 - cửa sổ cài đặt (phím xem), chức năng 1 (L2: công tắc đọc tự động hội thoại, kẻ thù trên bản đồ), chức năng 2 (R2: tua nhanh hội thoại, kẻ thù tiếp theo trên bản đồ, kết thúc chương trình trong trận chiến), công tắc hoạt ảnh chiến đấu (Y), chuyển đổi ngôn ngữ (L3), gốc/HD (R3).
- **Binding**: Mỗi thao tác đều có danh sách phím trên bàn phím (quét mã) và danh sách đầu vào tay cầm (phím hoặc hướng của một trục nhất định, được tính sau 16000 lần nhấn). Giá trị mặc định của tay cầm đã được thay đổi thành ưu tiên chức năng vào ngày 28-09-2026 (hướng do người dùng xác định sau khi đọc [phân tích nút gốc](../gameplay/original-controls.md)): A, B, START, LB/RB, phím chéo và cần điều khiển bên trái giống như trong phiên bản gốc; Z chỉ là bí danh của L trong danh sách và chỉ còn lại Z+Start để quay lại tiêu đề và không đưa ra thêm khóa nào; tăng tốc con trỏ bản đồ); Y chuyển hoạt ảnh chiến đấu; nhấn cần điều khiển trái và phải để chuyển ngôn ngữ và bản gốc/HD; phím điều khiển bên phải vẫn là phím C (cỡ chữ hội thoại ↑↓, tựa đề ±10); phím xem và hai trình kích hoạt quay trở lại máy chủ.
- **Mặc định bàn phím** (Người dùng 2026-09-28: "Các vị trí phím mặc định của PC/MAC sử dụng phương pháp cài đặt mặc định của PCSX2"): Ánh xạ tự động bàn phím của PCSX2 (`pcsx2/Input/InputManager.cpp`'s `GetKeyboardGenericBindingMapping`) cấp cho mỗi phím của bộ điều khiển một vị trí phím và chúng tôi để mỗi phím thực hiện công việc tương tự như phím của bộ điều khiển:

| Bộ điều khiển (Deck) | Chìa khóa PCSX2 | Chức năng |
  |---|---|---|
| A (dưới cùng) | K | Xác nhận (A) |
| B (phải) | L | Hủy bỏ (B) |
| X (trái) | J | Nhấn và giữ con trỏ để tăng tốc (C←) |
| Y (trên) | Tôi | Chuyển đổi hoạt hình chiến đấu |
| Thực đơn | Nhập | BẮT ĐẦU |
| Xem | Phím lùi | Cửa sổ cài đặt (cũng đã sửa Ctrl/Cmd + ,) |
| L1／R1 | Q／E | L／R |
| L2／R2 | 1／3 | Chức năng 1/ Chức năng 2 |
| Nhấn phím điều khiển trái/phải | 2/4 | Chuyển đổi ngôn ngữ/HD gốc (cũng có F7/F6 cố định) |
| Phím chéo | Phím định hướng | Phím chéo |
| Cần điều khiển bên trái | W A S D | Cần điều khiển |
| Cần điều khiển bên phải | T F G H | Phím C (F cũng là C←) |

Z, giống như bộ điều khiển, không có phím. Bảng bàn phím trước khi thay đổi (Z=A,
- **Seize**: Khi một đầu vào được cung cấp cho một hành động, nó sẽ thay thế tất cả đầu vào của hành động trên thiết bị này; hành động vốn chiếm giữ nó sẽ làm mất nó. Nếu không có khóa vì điều này, khóa đầu tiên ban đầu của hành động này sẽ được lấy - tương đương với trao đổi, sẽ không có khóa nào bị mất.
- **Lưu**: `input.json` (trình khởi chạy được đặt trong thư mục người dùng, `SRW64_INPUT_SETTINGS`; quá trình phát triển được đặt bên cạnh cài đặt bản trình bày), chỉ ghi các hành động khác với mặc định, theo tên SDL (`"Z"`, `"Return"`; `"a"`, `"leftshoulder"`, `"righty-"`). Nếu bạn đọc một cái tên mà bạn không nhận ra, hãy vứt nó đi.
- **Trên mỗi khung**: `graphics.cpp` đếm bit N64 và bit chủ theo liên kết; phím ảo được giữ bởi giao diện gỡ lỗi không nhìn vào liên kết và được cố định theo `classic_keys()`, vì vậy `z` trong tập lệnh vẫn là A. Đọc trạng thái hợp nhất của ba vị trí của phím L2/R2/view (đối thoại, chuyển đổi kẻ thù, mục nhập cài đặt), vì vậy nó có thể được sử dụng ngay cả khi được buộc vào bàn phím.

## Mẹo và Trang

- Token của mục nhập lời nhắc là một hành động (`{A}``{Start}``{L}``{CUp}``{DPad}``{Settings}``{AuxL}` ...), hiển thị liên kết hiện tại: dấu nhắc tay cầm hiển thị biểu tượng phím (nhấn họ bộ điều khiển) và dấu nhắc bàn phím hiển thị biểu tượng key cap hoặc tên phím (theo bố cục bàn phím). Các biểu tượng kết hợp hiển thị một biểu tượng tổng thể theo mặc định. Các phím cố định trang `{Enter}``{Esc}``{Tab}` và các biểu tượng phím mũi tên không thay đổi khi liên kết. Xem [`button_prompts.hpp`](../../src/native/text/button_prompts.hpp).
- Native page: Mã trang nhấn các phím nhận dạng bàn phím cũ (Z để xác nhận, X để hủy...). Khi có sự kiện bàn phím xảy ra, phím liên kết với một phím N64 nhất định sẽ được dịch sang phím trong bảng cũ (A→Z, L→Q, phím chéo/cần điều khiển→phím hướng..., `follow_bindings` của `frontend.cpp`); Các phím Enter, Esc, Tab và hướng không được dịch; các phím chữ không bị ràng buộc với chức năng nào thì không hoạt động trên trang (nếu không thì Z, X mặc định vẫn sẽ xác nhận, hủy); các phím liên kết với cửa sổ cài đặt để mở và đóng cửa sổ cài đặt; các phím liên kết với chức năng 1 và 2 không có tác dụng trên trang. Phím được nhấn trong giao diện gỡ lỗi không có số cửa sổ. Nhấn vào bảng cũ để vào trang trực tiếp. Trang tên không còn hộp nhập liệu (tên đã cố định) và cũng bị ràng buộc. Tay cầm đã được di chuyển theo vị trí N64 qua `pad_keys` và theo sau một cách tự nhiên.
- Lời nhắc ở thanh dưới cùng của đoạn hội thoại được mở rộng khi máy chủ chụp nhanh khung hình (`Frame.controls_text`), bản vẽ cảnh di động không yêu cầu SDL.

## Trang hoạt động

`controls_page` trong số `frontend.cpp`:

1. **Recognized Handle**: Tên của tay cầm do SDL báo cáo, được nhận dạng khi cắm vào (nhấn Deck khi `SteamDeck=1`); nếu không có tay cầm thì ghi "không kết nối". Thay đổi biểu tượng nút theo họ bộ điều khiển (Xbox/Deck/PlayStation/Nintendo). Dòng tiếp theo cho biết bàn phím mặc định có bố cục PCSX2.
2. **Thay đổi phím**: Một hàng cho mỗi chức năng (`control_rows[]`: OK, Hủy, BẮT ĐẦU, Trước, Tiếp theo, Chức năng 1, Chức năng 2, Tăng tốc con trỏ, Phóng to cỡ chữ, Giảm kích thước phông chữ, Hoạt ảnh chiến đấu, Cửa sổ cài đặt, Ngôn ngữ, Bản gốc/HD, Phím chéo bốn chiều, Z). Hai cột bên phải là các ràng buộc hiện tại của bàn phím và bộ điều khiển. Chọn một dòng và thông báo bật lên "Vui lòng nhấn phím mới cho "..." sẽ xuất hiện. Phím bàn phím hoặc phím điều khiển tiếp theo (nhấn nút hoặc đẩy cần điều khiển hoặc cò đến cuối) sẽ được liên kết với nó và thiết bị sẽ được thay đổi từ thiết bị được nhấn. Esc hủy và nó sẽ bị hủy nếu không được nhấn trong 6 giây; F5-F8 bị từ chối. Sau khi nhấn vào tay cầm, bạn phải đợi cho đến khi tất cả được nhả trước khi trang có thể chấp nhận lại điều hướng tay cầm.
3. **Đã sửa lỗi phím tắt** và **Khôi phục phím mặc định**: Ctrl/Cmd +, cài đặt, F5 để tải lại dòng, F6 gốc/HD, ngôn ngữ F7, Esc để thoát, không thể thay đổi.

Bốn bộ bảng khóa chỉ đọc ban đầu (`settings_key_*`/`settings_bind_*`) được thay thế bằng bảng chức năng này và các mục nhập đã bị xóa. Sơ đồ bộ điều khiển Steam Deck hiện có (tập lệnh vẽ draw_deck_diagram.py, nội dung thư mục hình ảnh/ui, `SRW64_UI_ASSETS` và thư mục ui trong gói, xem 8b7518d trở về trước) đã bị xóa cùng với "những hình ảnh không cần thiết".

## Kiểm tra

- `make recomp-input-bindings-test`: Bàn phím mặc định có bố cục PCSX2 và có chức năng tương tự như bộ điều khiển. Bảng cũ, quy tắc trao đổi, bản lưu chỉ được lưu khi có thay đổi thực sự.
- `make recomp-button-prompts-test`: Dấu được mở rộng theo ràng buộc và lời nhắc sẽ thay đổi sau khi thay đổi khóa.
- `tests/test_button_prompts.py`: Các ký hiệu trong ba ngôn ngữ nhất quán, lời nhắc điều khiển không yêu cầu phím cố định trang và lời nhắc bàn phím không còn viết ra các chữ cái.
- `tests/test_debug_coverage.py`: Các key trong bảng cũ đều có key ảo trùng tên. Phím ảo tính theo bảng cũ, phím vật lý tính theo ràng buộc.
- Rekey bàn phím 2026-09-28 đã được xác minh trên máy thực tế (lúc đó cũng có hình ảnh của bộ điều khiển); việc khóa lại tay cầm chưa được triển khai trên máy thực tế.