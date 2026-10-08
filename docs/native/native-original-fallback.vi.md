> **Ngôn ngữ / Language:** [Tiếng Việt](native-original-fallback.vi.md) · [English](native-original-fallback.en.md) · [中文](native-original-fallback.md)

# Dự phòng tài nguyên HD ở chế độ gốc

Ngày: 2026-09-12. Nó thuộc về mô-đun kết xuất tích hợp của dự án này; không có giao diện MOD bên ngoài mới.

## Hành vi hiện tại

| Cấu hình và tài nguyên | Hành vi khởi nghiệp |
| --- | --- |
| Hình ảnh HD nguyên bản, đầy đủ cũng như tài nguyên tên và hình đại diện | Xác minh và chuẩn bị tài nguyên HD, F6 có thể chuyển đổi hình ảnh và mô hình 5600 trong cấu hình |
| Thiếu tệp hình đại diện gốc, bản kê khai HD, hình ảnh hoặc tên | Sử dụng hình ảnh ROM và tám hình đại diện mở ban đầu; giữ lại ngôn ngữ, phông chữ và giao diện người dùng đã chọn; Chuyển đổi HD bị vô hiệu hóa cho lần chạy này, không có mô hình giọt nước nào được chuẩn bị |
| HD, thiếu các file HD cần thiết | Lỗi khởi động, cần hoàn thành tài nguyên hoặc chuyển rõ ràng sang Bản gốc |
| Tóm tắt hình ảnh/avatar không khớp, danh sách trái luật, đường dẫn vượt quá giới hạn | Báo lỗi, đừng bỏ qua thiệt hại do “thiếu nguồn lực” |

Nhật ký khởi động cho biết đường dẫn bị thiếu; tiêu đề cửa sổ hiển thị `Original | HD unavailable` và cả yêu cầu F6 lẫn HD được xác thực tự động đều không bật nội dung chưa được chuẩn bị. Khởi động lại sau khi khôi phục tài nguyên có thể lấy lại khả năng chuyển mạch; hiện tại, việc chạy cài đặt/tải lại tài nguyên không được hỗ trợ.

Dự phòng này chỉ dành cho các tệp nghệ thuật HD tùy chọn. Các đầu vào cơ bản như ROM gốc, danh mục ngôn ngữ, bản đồ glyph, chuỗi công cụ, v.v. vẫn phải hợp lệ. Mô hình giọt nước vẫn sẽ được tạo/xác minh theo quy trình ban đầu khi có ảnh full HD và bật cấu hình; thiệt hại cho các mô hình hiện có không nằm trong phạm vi khôi phục này.

```sh
.venv/bin/python tools/recomp/run/play_native.py \
  --profile config/recomp/profiles/play-profile.json --language zh-Hans --images original --new-game
```

Nguyên có nghĩa là nghệ thuật nguyên bản; Các trang tên tiếng Trung, bản địa và phông chữ độc lập vẫn có thể được sử dụng, điều này không có nghĩa là khôi phục toàn bộ giao diện người dùng N64. Ngôn ngữ vẫn được chọn khi khởi động và phạm vi đa ngôn ngữ của toàn bộ trò chơi cũng như chuyển đổi ngôn ngữ nhanh chóng vẫn chưa được hoàn thành.

## Thực hiện ranh giới

- `profile.py` chỉ chụp `FileNotFoundError` ở chế độ HD; Bản ghi gốc `hd_available: false` và lý do, còn HD tiếp tục báo lỗi. Hình ảnh đầu ra đã được biên soạn nhưng sau đó phát hiện thiếu ảnh đại diện sẽ không được máy chủ tải.
- `name_assets.py` Xác minh hình đại diện HD trước khi viết ra; Trích xuất chỉ ROM không đọc danh sách hình đại diện HD. Tám hình ảnh gốc vẫn xác minh bảng ROM và hình dạng hình ảnh.
- `run_host_probe.py` Chuẩn bị mô hình sau khi đã rõ nội dung sẵn có; không vượt qua đường dẫn mô hình/gói hình ảnh khi không có HD và chuyển rõ ràng trạng thái không có HD.
- `ImageMode` phân biệt rõ ràng ba trạng thái: chưa định cấu hình, Chỉ gốc và có thể chuyển đổi. Tiêu đề cửa sổ và bản ghi hoạt động phản ánh khả năng thực tế.

## Xác minh

`make check`: 115 thử nghiệm Python đã vượt qua, với 7 thử nghiệm mới bao gồm các gói bị thiếu, hình đại diện bị thiếu, lỗi HD rõ ràng, lỗi hiển thị bất hợp pháp, bảo toàn ngôn ngữ/phông chữ, trích xuất hình đại diện chỉ trong ROM và hình đại diện bị hỏng.

`make recomp-native-check`: 9 chương trình thành phần gốc đã đậu; trường hợp sử dụng chế độ hình ảnh xác nhận rằng chỉ khi yêu cầu Bản gốc thì cả HD lẫn chuyển đổi đều không thể thay đổi chế độ. Việc chuyển giao các thành phần gốc không tương đương với việc chấp nhận toàn bộ trò chơi.

Lần chạy thực tế với bằng chứng thô được đặt trong `build/recomp/original-fallback-check/`, sử dụng cấu hình mới trỏ tới bản kê khai nghệ thuật không tồn tại; không có tệp HD hiện có nào bị di chuyển hoặc xóa, không có trình phát nào lưu đã đọc hoặc bị ghi đè.

- `missing-zh`: Khởi đầu nguội gốc Trung Quốc, VI 1270 mở trang tên hiện đại; ghi lại rằng HD không có sẵn, mẫu gốc và không có gói hình ảnh; VI 2400 thoát bình thường và cả 4 luồng trò chơi đều được tái chế. Các khung GPU vẫn ghi lại Bản gốc sau khi gửi yêu cầu HD xung quanh VI 780. Vòng này không chụp ảnh màn hình cửa sổ trang tên Cocoa và ảnh chụp màn hình GPU không bao gồm lớp phủ trang.
- `intact-ja`: Quan sát chuyển đổi cấu hình đầu tiên của Nhật Bản, các chế độ mô hình của Original→HD→Original đều đúng, nhưng U+0010 đã xuất hiện trong trường tên trước ảnh chụp nhanh đầu tiên; nguồn không được xác định và không thể được chấp nhận làm tính toàn vẹn của tên mặc định. Sau khi khôi phục mặc định, quá trình chụp lại sẽ thoát khi đạt đến giới hạn trên VI và bản ghi lỗi sẽ được giữ lại.
- `intact-ja-final`: Vượt qua bài kiểm tra lại độc lập bằng cách sử dụng cùng một tệp nhị phân. Trang tên tiếng Nhật được chuyển sang Bản gốc→HD→Bản gốc ba lần, hình ảnh đại diện được chuyển đổi và khôi phục và tên/họ/biệt danh vẫn giữ nguyên `マナミ` / `ハミル` / `マナミ`; VI 1404 yêu cầu thoát, mã thoát máy chủ là 0 và tất cả 4 luồng trò chơi đều được tái chế. Xem `build/recomp/original-fallback-check/verification.json` và vòng hiện tại `roundtrip-verification.json` để biết bản tóm tắt cuối cùng.

Vòng này không xác minh phạm vi phủ sóng HD toàn trò chơi, tất cả các tuyến đường, lưu khôi phục hoặc trạng thái trò chơi/RNG tương đương đầy đủ; trạng thái mô hình trang tên chỉ xác nhận lựa chọn chế độ và không thay thế sự chấp nhận trực quan của mô hình bản đồ thế giới. Để biết bằng chứng về việc chuyển đổi bản đồ thế giới hiện có, hãy xem [Kiến trúc nội dung](native-content-foundation.md).