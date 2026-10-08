> **Ngôn ngữ / Language:** [Tiếng Việt](native-intro.vi.md) · [English](native-intro.en.md) · [中文](native-intro.md)

# Mở văn bản thu phóng: bỏ qua và thư mục tài nguyên

2026-09-10. Máy chủ RT64 gốc hỗ trợ **R + START** để bỏ qua toàn bộ văn bản thu phóng mở đầu và sơ đồ bàn phím hiện tại là **E + Enter**. Đoạn mở đầu công khai và đoạn mở đầu tuyến đường sau khi chọn nhân vật chính sử dụng cùng một lối vào điều khiển. Xác nhận thông thường vẫn tiến lên từng trang theo trò chơi gốc; tổ hợp phím bỏ qua bị chặn cho đến khi được nhả sau khi chuyển cảnh để tránh thao tác sai trong việc lựa chọn nhân vật chính hoặc dòng hội thoại đầu tiên.

Trải nghiệm trò chơi mới:

```sh
python3 tools/recomp/run/play_native.py --profile config/recomp/profiles/play-profile.json --new-game
```

Đầu tiên sử dụng Enter để chuyển logo, tiêu đề và chọn Trò chơi mới; nhập văn bản thu phóng trên nền bầu trời đầy sao và nhấn E + Enter. Hai phần mở đầu cần được nhấp vào một lần tương ứng. Tính năng này được bật theo mặc định trong máy chủ đồ họa, bất kể giao diện người dùng hội thoại gốc có được bật hay không.

## Tài nguyên gốc

Chạy `.venv/bin/python tools/content/extract_intro.py`, xuất ra `build/recomp/intro/assets/`:

- `index.html`: Duyệt theo thứ tự phát lại, hỗ trợ kích thước gốc/2 lần, đổ bóng trong suốt và mở một trang.
- `group-0.png` tới `group-4.png`: Tổng quan về 5 nhóm.
- `pages/`: Một trang văn bản hoàn chỉnh được sắp xếp lại theo mô hình ban đầu, 30 PNG trong suốt.
- `textures/`: Tập bản đồ kết cấu gốc, giữ nguyên kích thước ban đầu và bảng màu gốc.
- `decoded/`, `manifest.json`: Tài nguyên được giải nén, nhận dạng ROM, bù trừ tài nguyên, SHA-256, thứ tự trang và tọa độ mối nối trên mỗi khối.

| Nhóm | Số trang chơi | Tài nguyên |
|---|---:|---|
| Lời mở đầu công khai | 11 | 5506–5516 |
| Tuyến 1 | 6 | 5517, 5524, 5525, 5533, 5526, 5527 |
| Route 2 (máy thực tế ở vòng này là siêu phẩm nữ) | 6 | 5517, 5528, 5529, 5534, 5530, 5531 |
| Tuyến 3 | 5 | 5517, 5518, 5519, 5520, 5535 |
| Tuyến 4 | 5 | 5517, 5521, 5522, 5532, 5523 |

Tổng cộng 33 lần hiển thị, 30 kết cấu riêng lẻ. 5517 là trang niên đại được chia sẻ bởi bốn tuyến đường; 5536 là bảng màu RGBA16 được chia sẻ và 5537–5543 là bảy hình dạng trang văn bản.

Kết cấu ban đầu chủ yếu rộng 304 pixel và trang rộng 256 pixel. Chúng là các tập bản đồ và không thể được coi trực tiếp dưới dạng các trang văn bản hoàn chỉnh: ví dụ: mẫu 5537 lưu trữ văn bản 32×32 đầu tiên trong hình ảnh nguồn `(256,0)`, văn bản này thực tế được đặt ở góc trên bên trái của toàn bộ trang. Trình trích xuất sắp xếp lại trang thành các bộ mô tả sprite 16 byte và kiểm tra bốn đỉnh được sử dụng bởi hoạt ảnh chia tỷ lệ, độ bao phủ pixel và chồng chéo. Chiều rộng chính của trang thực tế là 256 pixel, rộng khoảng 224 pixel; chiều cao 32–192 pixel. Thư viện hiển thị các trang đã được sắp xếp lại, trong khi thư viện chưa được sắp xếp lại vẫn còn.

Lần này chỉ có nội dung gốc tiếng Nhật được trích xuất, không có văn bản nào được thay thế hoặc vẽ lại. Văn hóa Trung Quốc sau này có thể sắp xếp các trang này thành văn bản và bố cục lại chúng bằng công cụ văn bản gốc, trong khi vẫn giữ nguyên thời gian và thứ tự của hoạt ảnh thu phóng ban đầu.

## Triển khai và xác minh

`native_intro.cpp` Trong mục nhập gói `801CA9CC` của lớp phủ ROM `0x10DA50` (RAM `0x801C4500`, độ dài `0x7C50`) tuân theo trạng thái chính 13. Số nhóm pháp lý và số trang, trạng thái phụ 0/1. Nếu nhận được yêu cầu trong quá trình làm mờ ban đầu, hãy đợi đối tượng văn bản được tạo trước khi hoàn tất. Gọi bản phát hành đối tượng ban đầu `8008B888` và phần cuối của đoạn gốc `801CA5B4`, đặt số trang thành điểm cuối và trạng thái phụ thành 2; nhạc dừng, nhỏ dần và lựa chọn chế độ tiếp theo tiếp tục được thực hiện bởi trò chơi gốc. lớp phủ lớp phủ hủy các yêu cầu đang chờ xử lý trong khi tải và giữ các lần nhấn phím đã sử dụng cho đến khi được giải phóng về mặt vật lý.

- `make check`: 53 lần kiểm tra Python, kiểm tra tổng hợp và kiểm tra phụ thuộc đã được thông qua.
- `tests/native_intro.cpp`: Cạnh tổ hợp phím, chờ giảm dần ban đầu, kích hoạt đơn, che chắn liên tục giữa các cảnh, khôi phục nhả phím, truyền trong suốt xác nhận thông thường; ASan/UBSan đã được thông qua.
- `tests/native_intro_adapter.cpp`: Bộ điều hợp bộ nhớ thực, với 8 MiB RDRAM và sơ khai chức năng ban đầu để xác minh trạng thái kết thúc, vị trí đối tượng, lưu giữ ngữ cảnh cuộc gọi, cách ly lớp phủ; ASan/UBSan đã được thông qua.
- `build/recomp/intro/common-3/`: RT64/Metal gốc, 1.200 VI, thoát 0. Trang tĩnh mở đầu công khai VI 600 bị bỏ qua, VI 634 tải lựa chọn nhân vật chính; tổ hợp phím tiếp tục cho đến VI 900 và quá trình đọc lại GPU vẫn dừng ở lựa chọn nhân vật chính. Dữ liệu đầu vào là `config/recomp/inputs/intro-skip-common.json`.
- `build/recomp/intro/female-1/`: đối thoại RT64/Metal + Apple gốc, 4.800 VI, thoát 0. VI 500 yêu cầu bỏ qua, VI 518 kết thúc trong giai đoạn chia tỷ lệ văn bản; chọn siêu loại nữ bình thường và điền tên mặc định. Tuyến 2 bỏ qua tại VI 3100, VI 3134 đi vào bản đồ thế giới, VI 3290 xuất hiện với dòng chữ Lawrence 17410; tổ hợp phím tiếp tục cho đến VI 3400 và câu đầu tiên vẫn được giữ thủ công cho đến VI 4800. Đầu vào là `config/recomp/inputs/intro-skip-female.json`.

`report.json` của mỗi thư mục đang chạy sẽ lưu các giá trị băm đầu vào và mã, `intro-events.jsonl` lưu các sự kiện và `present-*.png` là quá trình đọc lại sau khi hoàn thành GPU. Danh mục tài sản 1/2x với bóng trong suốt được xem trong trình duyệt gốc.

`common-1` là lần chạy không thành công trước khi phần mở rộng ký hiệu địa chỉ khách được sửa chữa và không được sử dụng làm bằng chứng thành công. Tổ hợp phím `common-2` bắt đầu từ menu Trò chơi mới và không được thiết kế để bỏ qua phần mở đầu được nhập sau đó. Hoạt động thực tế hiện tại bao gồm các tuyến đường mở đầu công khai và siêu phẩm dành cho nữ; ba tuyến còn lại chia sẻ mã thích ứng và chưa được chạy riêng để được chấp nhận. Quá trình kiểm tra đã gửi các khóa qua đường dẫn đầu vào N64 của máy chủ nhưng bộ điều khiển vật lý không được kết nối.

Kiểm tra thành phần có thể được chạy bằng `make recomp-intro-test`.