> **Ngôn ngữ / Language:** [Tiếng Việt](shared-name-page-probe.vi.md) · [English](shared-name-page-probe.en.md) · [中文](shared-name-page-probe.md)

# RecompFrontend Nguyên mẫu trang tên chia sẻ

2026-09-20. Tiếp tục P2/P3 của [Kế hoạch phát hành đa nền tảng](../design/cross-platform-release-plan.md).

Đây là một thử nghiệm cửa sổ độc lập: sử dụng lại trình kết xuất RT64/Plume của RecompFrontend với phiên bản cố định của nó
RmlUi, hiển thị trang xác nhận và lựa chọn nhân vật chính (không cần nhập tên nữa kể từ ngày 27-09-2026, xem [Hiển thị ba ngôn ngữ tên mặc định](default-names.md)). Trò chơi chính thức hiện sử dụng cùng một trang được chia sẻ theo mặc định, hãy xem [Tích hợp trò chơi](shared-game-ui.md).
Các yêu cầu trong nguyên mẫu được cung cấp bởi bộ điều hợp tổng hợp và không thực thi trò chơi gốc, ghi vào SRAM hoặc chứng minh
Các trò chơi Windows/Linux có thể chơi được.

## Các phần phụ thuộc và ranh giới mã

- `config/recomp/frontend.json` Đã sửa lỗi cam kết RecompFrontend với RmlUi.
- `tools/recomp/toolchain/prepare_frontend.py --fetch` tải xuống thư mục phụ thuộc bị bỏ qua; từ chối
Phiên bản sai hoặc ngược dòng bị lỗi, thanh toán hiện tại không được cập nhật tự động. Không có quyền truy cập mạng theo mặc định.
- Nguyên mẫu sử dụng triển khai hiển thị đầy đủ `RmlRenderInterface_RT64` của thượng nguồn. Công cụ chuẩn bị chỉ chuyển đổi tệp tiêu đề
Ô của trình khởi chạy được thay đổi thành mức phụ thuộc tối thiểu của RmlUi/Plume; bản sao và bản tóm tắt được tạo vẫn giữ nguyên cục bộ.
Không giao tiếp với trình khởi chạy đầy đủ, menu MOD, cấu hình, biên dịch lại hoặc tính năng chuyển đổi toàn cầu của macOS ngược dòng.
- `src/native/ui/name_page.*` sử dụng `names::Request` hiện có và lệnh gọi lại ngữ nghĩa có nối tiếp.
Trang này chỉ xử lý hiển thị và nhập liệu, không chạm vào bộ nhớ trò chơi; việc xác minh, ghi lại và nâng cao trạng thái ở phía trò chơi thực vẫn được thực hiện bởi
`src/host/native_name_entry.cpp` chịu trách nhiệm. Các tệp thực thi độc lập vẫn sử dụng bộ điều hợp tổng hợp mà máy chủ chính thức đã được kết nối.
- `src/native/ui/text_input.*` Bổ sung phiên bản cố định phụ trợ SDL thiếu sự kiện từ nhóm (văn bản tạm thời,
Gửi, hủy, khôi phục tiêu điểm, cách ly khóa xác nhận), giờ đây chỉ sử dụng hộp nhập quỹ trong máy chủ trò chơi và trang tên và thăm dò không còn được sử dụng.
- `src/native/ui/probe_surface_macos.cpp` lưu trữ riêng biệt tính năng đọc lại ảnh chụp màn hình cửa sổ Metal và GPU.
Mã trang và mã nhóm không tham chiếu Cocoa, CoreText hoặc Metal; mục xây dựng thăm dò hiện tại vẫn bị giới hạn ở macOS.

## Xây dựng và tương tác

Trước tiên, hãy nhấn [Hướng dẫn phát triển](../guide/native-development.md) để chuẩn bị chuỗi công cụ đồ họa gốc, sau đó thực thi:

```sh
make recomp-ui-probe
./build/recomp/gfx-build/ui-probe/srw64-ui-probe \
  --catalog-dir content/locales \
  --font '/absolute/path/to/local-cjk-font.ttf' \
  --output build/recomp/ui-manual-01
```

Phông chữ phải được cung cấp rõ ràng cục bộ; được tải vào FreeType và được đăng ký thống nhất là `srw64-ui`, không sử dụng thư mục ngôn ngữ
Tên macOS PostScript trong , phông chữ hệ thống không được sao chép hoặc gửi. Ví dụ này yêu cầu phông chữ bao gồm tiếng Trung, tiếng Nhật và tiếng Anh.
Việc lựa chọn và cấp phép phông chữ để phân phối vẫn cần được thực hiện riêng.

Bốn thẻ là dữ liệu tổng hợp. Sử dụng phím trái và phải để chọn, Enter/Z để vào trang xác nhận; Enter để bắt đầu trang xác nhận, Esc để quay lại quá trình truyền;
F7 chuyển đổi giữa tiếng Nhật/tiếng Trung/tiếng Anh. Xác nhận cuối cùng của quá trình tổng hợp chỉ ghi `starts`, trả về `backs` và không bắt đầu trò chơi.
Tên được hiển thị theo yêu cầu: việc thay đổi sang ngôn ngữ đọc là vấn đề của giao diện người dùng máy chủ trò chơi chứ không phải của người thăm dò.

Tùy chọn `--dialogue /absolute/path/to/prepared/dialogue.json` để sử dụng nội dung được chuẩn bị sẵn tại địa phương
Tám bức chân dung đầu tiên. Hình đại diện chỉ là một ví dụ về tài liệu trực quan và không có nghĩa là nhân vật bị ràng buộc với tên tổng hợp.
Đây là một dẫn xuất ROM riêng và không được phân phối cùng với mã nguyên mẫu.

## Kiểm soát ngữ nghĩa có thể chạy lại

```sh
./build/recomp/gfx-build/ui-probe/srw64-ui-probe \
  --catalog-dir content/locales \
  --font '/absolute/path/to/local-cjk-font.ttf' \
  --output build/recomp/ui-script-01 \
  --script config/recomp/ui-probe/name-entry.json
```

Thư mục đầu ra không được tồn tại. Tập lệnh sử dụng `srw64.ui-probe-script.v1` và hỗ trợ `click` (ID kiểm soát),
`key`, `language`, `resize`, `capture`, `expect` và `quit`. SDL/RmlUi được sử dụng để tương tác với nút
Đường dẫn xử lý; `click` gọi trực tiếp hành động ngữ nghĩa của trang chứ không phải thử nghiệm nhấn chuột. Trả về khác 0 khi xác nhận không thành công. Mỗi trạng thái bước được ghi vào `events.jsonl`;
Ảnh chụp màn hình được đọc lại sau khi hàng rào GPU hoàn thành, cùng với trạng thái khung JSON. `result.json` cho biết phạm vi của quá trình tổng hợp.

Xác minh tập lệnh: lựa chọn, trang truyền Esc không hợp lệ, xác nhận, chuyển đổi ba ngôn ngữ, thu phóng, trang xác nhận quay lại truyền, xác nhận thay thế, bắt đầu.
27-09-2026 Nó chưa được chạy lại sau khi viết lại.

### Hồ sơ xác minh địa phương (2026-09-20, giai đoạn trang chỉnh sửa tên)

macOS arm64 đã hoàn thành bằng cách sử dụng các phông chữ RT64/Plume, AppleClang, FreeType và CJK cố định hiện có
Biên dịch và thực thi cửa sổ Metal thực tế. Tập lệnh 66 bước, 17 xác nhận trạng thái đã được thông qua, 7 ảnh chụp màn hình đọc lại GPU
Đã kiểm tra trang chọn tiếng Trung và tiếng Anh, trang tên theo từ nhóm, thông báo lỗi tiếng Nhật, trang tên tiếng Anh, trang đối tác và trang xác nhận.
Cũng được kiểm tra là gửi nhóm từ tiếng Trung, xóa lùi tiếng Nhật và giữ nguyên tiêu điểm đầu vào sau khi chuyển đổi ngôn ngữ.

Thư mục ghi cục bộ là `build/recomp/ui-probe-check-07`, `verification.json` tập lệnh ghi, mã nguồn,
Tóm tắt nhị phân và ảnh chụp màn hình; tên tổng hợp với hình đại diện cục bộ để xác minh trực quan,
Không phải ràng buộc nhân vật trò chơi gốc hoặc bằng chứng về việc trò chơi đang chạy. `make check` đã vượt qua 256 bài kiểm tra (11 bài bị bỏ qua),
Được ghi vào `build/recomp/ui-make-check.log`. Phông chữ, hình đại diện, ảnh chụp màn hình và các sản phẩm phụ thuộc không được đưa vào cơ sở dữ liệu.
Ngoài ra, `srw64-gfx-host` chính thức đã được biên dịch lại để xác nhận rằng nguyên mẫu tùy chọn không chặn bản dựng máy chủ ban đầu; nó không được xây dựng với cái này
Chạy chấp nhận thay vì trò chơi thực sự.

## Chấp nhận sau nguyên mẫu

1. ~~Xác minh ứng viên tiếng Trung/tiếng Nhật theo phương thức nhập hệ điều hành thực~~: Trang tên không còn nhập văn bản nữa.
2. Yêu cầu tên thật, chặn khối lượng công việc và tuần tự hóa cửa sổ/kết xuất đã được kết nối với máy chủ mặc định, hãy xem tài liệu tích hợp trò chơi.
3. Theo mặc định, máy chủ sử dụng lại cổng phát hành đầu vào; các nền tảng tiếp theo sẽ tiếp tục xác minh rằng nút đóng không xuyên qua được.
4. Di chuyển điều hướng/biên dịch lại bộ điều khiển và thêm xác minh bề mặt và bản dựng Windows/Linux.
5. Trang chia sẻ đã vượt qua phần mở và đặt tên thực sự; tập đầu tiên và kho lưu trữ khởi động nguội của ba nền tảng vẫn phải được chấp nhận sau đó.