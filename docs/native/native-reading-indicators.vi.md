> **Ngôn ngữ / Language:** [Tiếng Việt](native-reading-indicators.vi.md) · [English](native-reading-indicators.en.md) · [中文](native-reading-indicators.md)

# Tự động đọc bánh răng, tiến độ nâng cao và lấy nét khung đôi

Ngày: 2026-09-11. Tham khảo các ảnh chụp màn hình của "Mech Z" do người dùng cung cấp, tiến trình thăng tiến và trang bị tự động được thêm vào hộp thoại kép gốc.

## Hiệu suất trong trò chơi

- Thanh phía dưới hiển thị “Auto 3/4” và thang chia 4 đoạn, số lượng đèn phù hợp với số hiện tại. Giới hạn trên tự động là 4, chế độ thủ công hiển thị "Thủ công" và thang đo tắt.
- Hộp thoại hội thoại hiện tại chỉ được phân biệt bằng tên sáng hơn một chút: tên ở 2 ô đều có màu xanh, ô còn lại độ sáng là 80%; văn bản của hộp kia vẫn bị mờ. Hóa ra có một vòng tròn các góc màu lục lam ở bốn góc của khung và một dấu hình tam giác ở phía bên trái của tên. Vào ngày 26-09-2026, những nội dung này đã bị xóa theo yêu cầu của người dùng (`verify_reading_indicators.py` không còn kiểm tra hình tam giác nữa).
- Thanh mỏng ở đầu hộp hiện tại cho biết tiến trình cho đến lần tiến bộ tự động tiếp theo: nó có màu lục lam khi văn bản được hiển thị, màu cam trong khoảng thời gian chờ sau khi văn bản được hiển thị và tiến lên sau khi văn bản được điền. Văn bản dài vào trang đọc tiếp theo trước, sau đó trang cuối cùng được giao lại cho trò chơi gốc để vào đoạn tiếp theo. Các số trang như "1/2" sẽ không còn hiển thị kể từ ngày 23-09-2026: trang tiếp theo giống như trang gốc. Nhấn A để tiếp tục hiển thị.
- Tạm dừng đồng hồ đọc khi phát lại và tiếp tục sau khi quay lại; thanh đếm ngược tự động sẽ không hiển thị khi thực hiện thủ công, chuyển tiếp nhanh hoặc bỏ qua.
- Các tên trong review sẽ luân phiên giữa màu xanh/cam khi đổi người, các clip liên tiếp của cùng một người sẽ giữ nguyên màu. Màu sắc được xác định khi bản ghi xem lại được ghi, việc cuộn hoặc gỡ bỏ các bản ghi cũ hơn sẽ không làm thay đổi màu của tên hiện có; văn bản vẫn trắng.
- Trong quá trình chuyển giao, nếu cả hai hộp tạm thời không hoạt động, dấu vẫn còn trên hộp vừa được đọc và vẫn hiển thị và chuyển đổi sau khi hộp tiếp theo bắt đầu. Các dấu không được giữ lại sau khi hộp thoại bị đóng hoặc tập lệnh bị vô hiệu.

Các thao tác tuân theo các phím hiện có: ↑↓ để điều chỉnh bánh răng, người Nhật và người Trung Quốc tiếp tục sử dụng các mục nhập giao diện người dùng bên ngoài tương ứng của họ; văn bản giao diện mới không được mã hóa cứng trong nhánh tiếng Trung.

## Ảnh chụp màn hình thực tế

Sau đây là ảnh chụp màn hình thực tế của phiên bản tám cấp độ đầu tiên. Dựa trên phản hồi tiếp theo, nó đã được giảm xuống còn bốn bánh răng; tốc độ ban đầu của các bánh răng 1–4 được giữ lại và các hằng số bánh răng tương tự được sử dụng cho các số, tỷ lệ và các giới hạn trên chính.

Nói chuyện ở khung trên:

![Tự động đọc ở khung trên](../../build/recomp/reading-indicators/zh-full/present-3600.png)

Nói bên dưới:

![Đọc tự động ở ô bên dưới](../../build/recomp/reading-indicators/zh-full/present-3660.png)

Văn bản tiếng Nhật, hình ảnh gốc, văn bản số 18 và phân trang: [ảnh chụp màn hình thực tế](../../build/recomp/reading-indicators/ja-full/present-3780.png). Tiếng Trung, HD, văn bản và phân trang số 18: [ảnh chụp màn hình thực tế](../../build/recomp/reading-indicators/zh-full/present-5220.png). Tất cả đều là các bản đọc lại sau khi GPU hoàn thành chứ không phải sơ đồ nguyên lý.

## Trạng thái và thời gian

`dialogue_model.hpp` và `page_timing()` được sử dụng để xác nhận tự động thực tế và hiển thị tiến trình cùng một lúc. Công thức tốc độ hiển thị từ gốc và thời gian chờ được sử dụng để tránh tạo ra một bộ đếm thời gian hoạt ảnh khác không liên quan đến tiến trình của cốt truyện. Tiến trình được tính toán dựa trên các dấu tích đã được đầu đọc xử lý, nằm giữa 0-1000; phát lại sẽ tạm dừng dòng thời gian này, đặt lại trang đọc mới và giữ cho lưới luôn đầy trong khi chờ trò chơi nhận được xác nhận.

Chuỗi trò chơi thêm các sự kiện đọc, tiến trình và trạng thái giao diện vào `Frame` bất biến. Kết xuất vẫn sử dụng ảnh chụp nhanh tương ứng với khối lượng công việc RT64. `focused_box()` ưu tiên chọn khung hoạt động duy nhất; khi không có khung hoạt động, chỉ có thể chọn khung trong khung khớp với sự kiện đọc cuối cùng và vẫn hiển thị. Người nói hoặc từ ngữ không được mượn từ các khối lượng công việc khác.

Thanh tiến trình sử dụng khoảng trống trên cùng của hộp thoại gốc mà không làm giảm độ rộng tên hoặc vùng bố cục văn bản. Thanh dưới cùng tiếp tục được hiển thị theo khả năng hiển thị của toàn bộ giao diện hội thoại, giữ lại [Sửa chữa nhấp nháy thanh dưới cùng Tự động phát] trước đó (native-dialogue-flicker.md).

## Xác minh

Cả hai bộ đều là bản triển khai RT64/Metal thực tế của ROM gốc Nhật Bản, mỗi bộ chạy 11800 VI, đã tắt âm thanh:

| Kiểm tra | Tiếng Trung / HD, Số 13 → Số 18 | Tiếng Nhật / Ảnh gốc, số 18 |
| --- | ---: | ---: |
| Khung hoàn thành GPU liên tiếp | 2206 | 2300 |
| Kiểm tra pixel cột dưới cùng | 2135 | 2300 |
| Kiểm tra pixel điểm đánh dấu tam giác của loa hiện tại | 1955 | 2120 |
| Kiểm tra pixel điền vào thanh đẩy | 1756 | 1919 |
| Xem lại khung tạm dừng | 180 | 180 |
| Khung chuyển giao không có khung hoạt động | 107 | 10 |
| Kiểm tra không thành công | 0 | 0 |

Hai bộ ấn bản đầu tiên ở trên đã trải qua tất cả các bánh răng từ 0-8 vào thời điểm đó, hai hộp thoại trên và dưới, hiển thị/chờ, khôi phục thủ công, xem lại và phân trang văn bản dài. Các giá trị sự kiện, trang đã đọc và tiến trình không thay đổi trong quá trình phát lại. Ở nhóm tiếng Trung, có 71 khung hình khác tắt lời thoại và ẩn thanh dưới bình thường; trong số các khung hội thoại vẫn hiển thị, thanh phía dưới không biến mất một cách đột ngột. Sau khi điều chỉnh cấp độ thứ tư, việc kiểm tra cấu trúc máy chủ và thành phần đọc hiện có sẽ được hoàn thành riêng biệt; phiên bản đầu tiên chạy bằng chứng sẽ vẫn còn nguyên.

`verify_reading_indicators.py` đọc các dấu tích sáng, tam giác tên và độ dài thanh tiến trình từ các pixel GPU liên tiếp và so sánh chúng với trạng thái của khối lượng công việc này theo từng khung hình. Các hình tam giác bị che khuất và thanh tiến trình không được chọn khi xem lại hộp thoại lớp phủ; thanh dưới cùng vẫn được kiểm tra. Điểm cuối cho phép khử răng cưa cho pixel được lấy mẫu có độ phân giải thấp.

60 bài kiểm tra Python, biên dịch và kiểm tra phần phụ thuộc đã được thông qua cho `make check`; đã vượt qua cho `make recomp-content-test`. Các thành phần mới quay trở lại để đáp ứng thời hạn tự động thực tế, tiến trình đơn điệu và lưới đầy đủ, đóng băng đánh giá, ẩn thủ công/chuyển tiếp nhanh, xóa phân trang, tập trung chuyển giao, hộp hoạt động kép không rõ ràng và hộp đóng.

Đánh giá:

```sh
.venv/bin/python tools/recomp/verify/verify_reading_indicators.py build/recomp/reading-indicators/zh-full
.venv/bin/python tools/recomp/verify/verify_reading_indicators.py build/recomp/reading-indicators/ja-full
.venv/bin/python tools/recomp/analysis/analyze_toolbar_trace.py build/recomp/reading-indicators/zh-full \
  --require-matching-dialogue --output build/recomp/reading-indicators/zh-full/toolbar-boundaries.json
```

Xem [acceptance.json](../../build/recomp/reading-indicators/acceptance.json) để biết các tệp nguồn, thông tin đầu vào và hàm băm bằng chứng. Phạm vi của cỗ máy thực tế này là đoạn hội thoại mở đầu bản đồ thế giới, bao gồm hai cấu hình hình ảnh/ngôn ngữ được liệt kê; bản ghi chẩn đoán đầy đủ được sử dụng và thời gian kết xuất của nó không được sử dụng làm dữ liệu hiệu suất để phát bình thường.