> **Ngôn ngữ / Language:** [Tiếng Việt](shared-game-ui.vi.md) · [English](shared-game-ui.en.md) · [中文](shared-game-ui.md)

# Giao diện game SDL/RmlUi

2026-09-20. Giao diện trong trò chơi chuyển sang các sự kiện SDL2, bố cục RmlUi và phông chữ FreeType theo mặc định.
Đã sửa phiên bản của trình kết xuất RecompFrontend RT64/Plume. Lựa chọn nhân vật chính, nhập tên, xác nhận, Link Battler,
Các cài đặt và chú giải công cụ được vẽ trên bề mặt GPU của trò chơi. Máy chủ mặc định không còn biên dịch trang AppKit tương ứng nữa.

"Cài đặt..." hoặc Ctrl/Cmd+ trong menu ứng dụng trên cùng của macOS, mở cài đặt chia sẻ, Esc hoặc "Quay lại" để đóng;
Màn hình trò chơi không có nút tùy chọn cố định. Menu hệ thống chỉ chịu trách nhiệm mở lối vào và trang cài đặt vẫn được chia sẻ SDL/RmlUi. quy tắc, cài đặt trước, ngôn ngữ,
Original/HD vẫn gọi giao diện gốc. F7 thống nhất đi vào đường dẫn sự kiện SDL và khoảng thời gian nhóm từ được chuyển sang phương thức nhập.
Bộ điều hợp trò chơi tiếp tục chịu trách nhiệm mã hóa tên, kiểm tra trùng lặp, ghi lại, trạng thái liên kết và nâng cao tập lệnh.

## Ranh giới mã và luồng

- `src/native/ui/frontend.cpp`: Sự kiện SDL, bối cảnh RmlUi, cài đặt/liên kết/thông báo được chia sẻ và giao diện người dùng gỡ lỗi.
- `name_page.*`, `text_input.*`: Tên trang và cầu từ nhóm được chia sẻ với các nguyên mẫu độc lập.
- `presentation_settings.cpp`: Logic yêu cầu/hoàn thành/giải phóng khóa bằng ngôn ngữ gốc, lưu và sử dụng `app::atomic_write` công khai.
- `window_test_control.cpp`: Kích thước cửa sổ và phần phụ trợ SDL QA đã đóng.
- `src/host/macos/app_menu.mm`: Một lối vào cài đặt duy nhất của menu ứng dụng hệ thống, tiêu đề ngôn ngữ sẽ chuyển đổi theo trò chơi;
Nhấp vào Chỉ gửi yêu cầu mở để bàn giao trang cài đặt chia sẻ trong chuỗi cửa sổ.
- `src/host/graphics.cpp`: Kết nối hook render RT64, vẽ UI sau khi chặn tên tương ứng với khối lượng công việc,
Lệnh gọi lại hoàn thành GPU sẽ mở khóa tài nguyên; ảnh chụp màn hình chứa giao diện người dùng trong cùng một lần gửi GPU và lớp phủ ảnh chụp màn hình AppKit không còn được thực hiện nữa.

Tất cả các lệnh gọi RmlUi đều được bảo vệ bởi cùng một mutex. Luồng cửa sổ chịu trách nhiệm về các sự kiện, bố cục và hành động ngữ nghĩa, còn luồng kết xuất chỉ ghi lại
Lệnh vẽ. Kết cấu bố cục/bản phát hành tiếp theo chờ hoàn thành lần gửi trước đó; Đã sửa lỗi hàng đợi hiện tại RT64 chờ từng khung hàng rào,
Đáp ứng các ràng buộc không có bộ đệm đôi của trình kết xuất ngược dòng. Việc bắt đầu, dừng và định vị hộp ứng viên của văn bản SDL được hoãn lại để thực thi luồng cửa sổ.
Phá hủy RmlUi và trình kết xuất trước khi phá hủy GPU; duy trì thứ tự tái chế luồng của máy chủ ban đầu.

Giao diện người dùng chỉ đọc `names::Request`, `link_page::Request`, ảnh chụp nhanh cài đặt và thư mục ngôn ngữ không thể thay đổi, không đọc RDRAM.
Việc che tên tiếp tục được tìm kiếm theo khối lượng công việc RT64 và khối lượng công việc cũ đến muộn sẽ không hiển thị lại lưới ban đầu do chuyển đổi luồng cửa sổ.
Hình đại diện được đăng ký bằng tên tài nguyên nội bộ để tránh việc chuẩn hóa URL RmlUi làm thay đổi đường dẫn tệp tuyệt đối; Bản gốc/HD vẫn sử dụng nội dung cục bộ.
Việc kiểm soát phát hành khóa sau khi đóng một trang phương thức sẽ được tính vào trạng thái thực tế SDL và gỡ lỗi các khóa ảo.

## Bản dựng và phông chữ

`make host` / `run_host_probe.py --graphics` tự động chuẩn bị những cái cố định trong `config/recomp/frontend.json`
RecompFrontend với RmlUi; không ghi đè lên các phiên bản ngược dòng hoặc phiên bản xấu. Việc chuẩn bị và biên dịch mã nguồn yêu cầu các công cụ phát triển, trò chơi
Python vẫn không cần thiết để chạy và nhập ROM cục bộ. Nguyên mẫu trang tên độc lập được giữ lại dưới dạng `make recomp-ui-probe`.

Giao diện người dùng và hội thoại được chia sẻ sử dụng cùng một bộ phông chữ được đóng gói: trình khởi chạy trỏ `SRW64_FONT_DIR` tới `tools/content/prepare_fonts.py`
Thư mục đã chuẩn bị sẵn (HarmonyOS Sans SC và Condensed, cùng với phông chữ biểu tượng `content/fonts/SRW64Symbols.ttf` và phông chữ biểu tượng nút `SRW64Prompts.ttf` trong kho),
Báo cáo rõ ràng lỗi khi thiếu tệp. Gói ứng dụng chứa các phông chữ và giấy phép này ở dạng `Contents/Resources/fonts/` và trang "Giới thiệu" của cửa sổ cài đặt cho biết nguồn của phông chữ.
`SRW64_UI_FONT` có sẵn trong môi trường phát triển để chỉ định một phông chữ duy nhất; chỉ tìm máy cục bộ khi không có `SRW64_FONT_DIR` (kiểm tra đơn vị, thăm dò cũ)
Arial Unicode, Microsoft Yahei hoặc Noto Sans CJK. Xem [đối thoại văn bản và trò chơi đa nền tảng tiếng Trung, tiếng Nhật và tiếng Anh](portable-text.md).

## Gỡ lỗi và hồi quy

`ui.tree` Trả về tọa độ `id`, văn bản, có sẵn, tiêu điểm và điểm cửa sổ của phần tử RmlUi.
`text` trong số `ui.click` hỗ trợ văn bản hiển thị hoặc ID ổn định như `route1`, `field0`, `next`,
`rule:esp-level`, `locale:en`, `images:hd`, `link:0`. Sau khi cửa sổ cài đặt phân trang, nhấn id và nhấp vào điều khiển cài đặt trên trang khác sẽ chuyển sang trang đó trước;
Bản thân tab đó là `settings-page:general`, v.v. (xem [Cửa sổ cài đặt](settings-window.md) §7).
Các lần nhấp được RmlUi kiểm tra lần truy cập và các chức năng trò chơi không được gọi trực tiếp. `ui.key` sử dụng tên khóa SDL,
`ui.type` sử dụng `SDL_TEXTINPUT` / `SDL_TEXTEDITING_EXT`; không còn dựa vào key_code của macOS nữa.
Ảnh chụp màn hình sử dụng cửa sổ trò chơi mặc định và cài đặt không còn là cửa sổ hệ điều hành riêng biệt nữa. `menu` trả về tiêu đề thiết lập và trạng thái sẵn sàng `native_menu`;
macOS thực sự thực thi mục menu hệ thống khi được gọi bằng tiêu đề cài đặt và tiêu đề quy tắc vẫn tương thích với chuyển tiếp.
Tập lệnh tệp kiểm soát quy tắc/tên AppKit cũ không phải là cổng chấp nhận của giao diện người dùng được chia sẻ.

Thực thi trong **phiên cách ly mới** (sẽ bắt đầu trò chơi mới và thay đổi tên, không chạy trên phiên người chơi):

```sh
SRW64_DEBUG=1 .venv/bin/python tools/recomp/run/run_host_probe.py \
  --graphics --interactive \
  --profile config/recomp/profiles/play-profile.json --language zh-Hans \
  --images original --output build/recomp/shared-game-test
# 在另一终端运行：
.venv/bin/python tools/recomp/verify/verify_shared_ui.py --run build/recomp/shared-game-test
```

Kiểm tra mức độ phù hợp: mở và truyền thực sự, từ chối các ký tự không được hỗ trợ, cách ly Return/F7 trong khi soạn thảo văn bản, gửi văn bản,
Chuyển đổi ngôn ngữ duy trì việc chỉnh sửa, cài đặt quy tắc, chia tỷ lệ 800×600 và 1100×760, đối tác/xác nhận, ghi lại tên trò chơi và kích hoạt câu chuyện.
Báo cáo xác minh và ảnh chụp màn hình GPU được lưu trong thư mục chạy cục bộ và không được lưu trữ trong thư viện.

## Bằng chứng địa phương (2026-09-20, cam kết giao diện người dùng chung a8a2de)

- `build/recomp/sdl-game-07/shared-ui-verification.json`: mở đầu thật, truyền cảm hứng, kết hợp từ, ngôn ngữ, bối cảnh,
Cửa sổ nhỏ, viết lại tên, xác nhận đối tác và bắt đầu câu chuyện; nhấn và giữ W để đóng cài đặt, nhấn và giữ Return để xác nhận cổng phát hành câu chuyện,
Đoạn mở đầu tuyến đường đã được bỏ qua thành công và các nút trò chơi đã được khôi phục sau khi xác nhận rằng trang đã bị đóng.
- `build/recomp/sdl-game-03/shared-small.png`, v.v. Quá trình đọc lại GPU trải qua quá trình kiểm tra hình ảnh thủ công; 800×600 so với
Hộp nhập liệu 1100×760, hình đại diện và các nút đều nằm trong phạm vi của giao diện.
- `build/recomp/sdl-link-01/shared-link-verification.json`: Đọc SRAM hiện có và vào trang liên kết.
Chọn F91 và Zambot; bản ghi bộ điều hợp trò chơi gốc `selection=5`, `kind=linked`.
`status.link_page.scheduled` là ảnh chụp nhanh khi trang được mở. Nó không được sử dụng để suy ra trạng thái trò chơi sau khi gửi.
- Chạy qua `window close`/`quit`, mã thoát 0, log `created=4 joined=4 remaining=0`.
`sdl-shutdown-01` bổ sung mở dấu vết luồng hệ điều hành: được coi là 0 sau khi phát hành nhưng được ghi lại như trước khi phát hành
`UNOBSERVED`, do đó `shutdown_lifecycle_verified=false` được báo cáo; không thoát bình thường
hoặc tham gia được tính là đã vượt qua cổng ranh giới hệ điều hành đầy đủ.
- `build/recomp/ui-probe-sdl-final`: Tập lệnh trang tên 66 bước độc lập đã được thông qua.
- `make check`: 245 trong số 256 bài kiểm tra đã vượt qua, 11 bài kiểm tra bị bỏ qua, cộng với kiểm tra tổng hợp và kiểm tra phụ thuộc.

Trên đây là bằng chứng về trò chơi và GPU thực được gửi trên macOS cho giao diện người dùng được chia sẻ này và không phải là sự chấp nhận của trò chơi cho quá trình phân chia phụ trợ đối thoại tiếp theo;
Từ nhóm là sự kiện chèn SDL và cửa sổ ứng cử viên hệ điều hành không được xác minh. Thanh nhắc đã được kết nối với kết xuất được chia sẻ, nhưng vòng này không kích hoạt hoàn tiền cốt truyện để chấp nhận riêng thanh nhắc.

## Văn bản và bố cục đối thoại

Hội thoại mặc định đã được truy cập [văn bản đa nền tảng tiếng Trung, tiếng Nhật và tiếng Anh](portable-text.md), CoreText/CoreGraphics sẽ không còn được nhập
Mục tiêu đối thoại của trò chơi. `src/host/dialogue_scene.cpp` chịu trách nhiệm về nội dung chính, tên người, chỉ báo đọc, cột dưới cùng và phần đánh giá,
`src/host/dialogue_layout_adapter.hpp` cho phép Reader và Draw có chung bố cục bất biến.
`src/host/dialogue_plume.cpp` sử dụng [bộ tổng hợp Plume phổ quát](plume-pixel-compositor.md),
Lưu giữ ảnh chụp nhanh hội thoại về khối lượng công việc phù hợp và tham chiếu tài nguyên trước khi hoàn thành GPU.

Mục xác minh CPU cục bộ là `tests/dialogue_cpu/`, không có CI từ xa; xem tài liệu văn bản để biết các lệnh, phần phụ thuộc và cấu hình phông chữ.
Việc so sánh từng pixel của phần tách CoreText trước đó là xác minh lịch sử. Phần phụ trợ mới sử dụng hành vi tiếng Trung, tiếng Nhật và tiếng Anh, cắt xén và chấp nhận màn hình trò chơi thực tế.
Không cần khử răng cưa để mô phỏng phông chữ hệ thống cũ.

## Công việc đa nền tảng chưa hoàn thành

Các lớp HD, đọc lại ảnh chụp màn hình và chặn trang tên được triển khai trong Plume phụ trợ phi kim loại và phiên bản Linux/Steam Deck có thể được xây dựng và chạy.
([Cổng ba nền tảng](../design/three-platform-port.md)); Bộ chọn ROM lần đầu tiên trên máy tính để bàn vẫn chỉ được triển khai trong macOS,
Windows vẫn chưa được xây dựng.
Cửa sổ đề xuất phương thức nhập hệ điều hành thực sự của Trung Quốc và Nhật Bản, điều hướng bộ điều khiển, phông chữ có thể phân phối lại và khởi động nguội tập/kho lưu trữ đầu tiên của ba nền tảng vẫn cần được chấp nhận độc lập.