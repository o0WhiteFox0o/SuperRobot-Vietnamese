> **Ngôn ngữ / Language:** [Tiếng Việt](native-backgrounds-hd.vi.md) · [English](native-backgrounds-hd.en.md) · [中文](native-backgrounds-hd.md)

# NỀN HD

24-09-2026. 8 hình nền của màn hình インターミッション đã được tạo ở dạng HD và được tích hợp vào trò chơi dưới dạng hình ảnh hoàn chỉnh, với một bộ cho mỗi phiên bản sáng và phiên bản tối.

## Nền là gì?

- Tổng cộng có 8 hình minh họa 3D CG 320×240 CI8, tài nguyên 5470–5477 (`0x155E`–`0x1565`). Mỗi bức ảnh thể hiện một chiếc máy nhân vật chính có logo SRW64 ở góc trên bên phải.
- Hai bảng màu 256 màu trên mỗi tờ: phiên bản sáng 5478–5485, phiên bản tối 5486–5493. Sử dụng phiên bản nhẹ khi vào lần đầu tiên; chuyển sang phiên bản tối sau khi menu được xây dựng và khi quay lại từ màn hình phụ. Bản thân biểu đồ vẫn không thay đổi.
- Chọn hình ảnh theo máy nhân vật chính đầu tiên và không thay đổi theo số lượng từ. Để biết chi tiết, hãy xem [Menu chính giữa các cảnh](native-intermission-menu.md) §3.
- Màu 0 là màu đen trong suốt. Nền của trò chơi được đặt thành màu đen nên hình ảnh HD được làm mờ.

## Cách vẽ trò chơi

Nền được vẽ trong khe sprite 0, chế độ 4, `80098158(槽, 0, 4, 0xA4, 0, 图, 调色板, 0)` và chức năng vẽ là `80095974` (chế độ 2 cũng sử dụng nó). Danh sách hiển thị được chụp trên máy thật:

- Bộ đầu tiên `E3000C00`, `E3001001` (TLUT RGBA16), bộ kết hợp `FC119623 FF2FFFFF`, tức là màu và Alpha đều là TEXEL0 × PRIM; sau đó sử dụng `FA` để đặt PRIM (tăng giảm dần tùy thuộc vào nó).
- Sau đó nạp bảng màu 256.
- Sau đó vẽ 80 khối 32×32: `SETTIMG` cho mỗi khối (toàn bộ hình ảnh), `LOADTILE` để tải vùng của khối này (tải thêm 1 pixel để lọc song tuyến tính), `SETTILESIZE` để đặt ô kết xuất thành (0,0)–(31,31) và cuối cùng `TEXRECT` để vẽ ra màn hình.
- Bản ghi con Elf +0xC/+0xE là phần xử lý tài nguyên. Số tài nguyên có thể được trao đổi bằng cách nhấn bảng xử lý `8008A11C` (`0x160340`, mỗi mục là 20 byte, +2 là số tài nguyên ROM).

## Thay thế toàn bộ trang tính

Phương thức của [`native_background.cpp`](../../src/host/native_background.cpp) giống với hình đại diện:

1. Treo `80095974`;
2. Sử dụng số tài nguyên để kiểm tra hình ảnh HD tương ứng với (hình ảnh, bảng màu);
3. Tính toán phạm vi của từng khối trên ảnh gốc từ điểm bắt đầu của `LOADTILE`, S/T của `TEXRECT` và dsdx/dtdy, rồi ghi ra (hình chữ nhật màn hình, hình chữ nhật ảnh gốc);
4. Thay đổi khối cuối cùng thành dấu được gắn nhãn, giữ nguyên khối đầu tiên (để RT64 bắt đầu quá trình kết xuất của khung này trước, xem phần bầu trời đầy sao của [Story World Map HD](native-worldmap-regions-hd.md)) và để trống phần còn lại;
5. Máy chủ sử dụng bản vẽ phiên bản để vẽ tất cả các khối cùng một lúc (plume, `src/host/shaders/HdBackground*.hlsl`, cùng một bản sao của Metal/Vulkan/D3D12), lấy mẫu cùng một hình ảnh HD, do đó không có đường nối giữa các khối.

Các shader được nhân với PRIM và mờ dần như ban đầu; kết cấu được nhân lên trước alpha với mipmap. Nó sẽ không được viết lại ở chế độ ảnh gốc. Khi cuộn hoặc vẽ chỉ một phần, mỗi khối cũng được ánh xạ theo phạm vi ảnh gốc của riêng nó.

## Tạo

[`background_hd.py`](../../tools/hd_ai/background_hd.py):

- `prepare`: Phiên bản sáng được phóng to bởi người hàng xóm gần nhất 6 lần làm đầu vào. Các từ nhắc nhở được yêu cầu giữ lại bố cục, nội dung và văn bản logo (ký tự lớn "SRW64", ký tự nhỏ "cuộc chiến siêu robot 64").
- `run`: Yêu cầu `qwen-image-3.0-pro` và `qwen-image-3.0` một lần cho mỗi hình ảnh, xuất ra 2048×1536, tổng cộng 16 lần, 5,76 nhân dân tệ. Tất cả đều hoạt động cùng một lúc, không có 400 trường hợp nào xảy ra.
- `compose`: Đăng ký theo cửa sổ, điều chỉnh tỷ lệ và dịch theo trục (độ lệch nằm trong 0,2%), lấy mẫu lại thành 1920×1440 (6 lần) và xuất biểu đồ so sánh.
- `build`: Lấy model đã chọn (Pro mặc định) làm phiên bản được đánh dấu. Phiên bản tối sử dụng bảng màu 17³ được trang bị từ hai bộ bảng ROM, được ánh xạ từ phiên bản sáng.
- Bản màu tối không được làm tối đồng đều: tỷ lệ mỗi màu nằm trong khoảng 0,5–0,95.
- Dùng ảnh gốc để kiểm chứng: mức chênh lệch trung bình giữa bảng màu và phiên bản tối của game là 1,2-2,6 cấp, khi nhân với 0,75 thì chênh lệch là 3-23 cấp.

Cả hai mẫu đều giữ nguyên bố cục, các bộ phận và văn bản logo. Bóng và bề mặt của Pro sạch hơn, trong khi phiên bản thông thường sắc nét hơn một chút và có các cạnh hơi lởm chởm. Sau khi thu nhỏ về kích thước ban đầu, độ chênh lệch so với ảnh gốc đều là 2–5 cấp độ. Mặc định là Pro, bạn có thể sử dụng `build --choice '{"background-5470": "qwen-image-3.0"}'` để thay đổi từng lựa chọn một.

Tài nguyên trong `assets/hd-ai/backgrounds/whole-v1`: 16 hình ảnh 1920×1440, tổng dung lượng 42 MB. Tệp kê khai hiện sử dụng `whole-v2`, toàn bộ phiên bản 1 cộng với bầu trời đầy sao của bản đồ thế giới câu chuyện ([bản đồ thế giới câu chuyện HD](native-worldmap-regions-hd.md)). Phần `backgrounds` của [`stage1-hd.json`](../../content/art/stage1-hd.json) liệt kê chúng và `compile_art` được sao chép vào thư mục đang chạy `art/backgrounds/` sau khi xác minh.

## Máy thực tế (24/09/2026, chế độ HD)

- Sau khi đọc tập đầu tiên và xóa file lưu và nhập インターミッション: hình nền (スイームルグ, 5476) hiển thị dưới dạng phiên bản HD tối, và bảng menu được xếp chồng lên nhau như bình thường.
- Cài đặt chuyển về ảnh gốc rồi chuyển ngược lại, hai ảnh chụp màn hình HD sẽ thống nhất từng pixel.
- Số lần thoát: 986 bản vẽ nền được viết lại tất cả, 0 lỗi nhận dạng, 2 lần giải mã (sáng, tối).

## Lệnh

```sh
.venv/bin/python -m tools.hd_ai.background_hd prepare --output assets/hd-ai/backgrounds/run-1
.venv/bin/python -m tools.hd_ai.background_hd run --output assets/hd-ai/backgrounds/run-1 --env-file /path/to/.env
.venv/bin/python -m tools.hd_ai.background_hd compose --output assets/hd-ai/backgrounds/run-1
.venv/bin/python -m tools.hd_ai.background_hd build --output assets/hd-ai/backgrounds/run-1 --images assets/hd-ai/backgrounds/whole-v1 --bind
```

Sau khi thay đổi hook của `generate_cpu.py`, bạn cần chạy lại nó trước rồi mới build máy chủ.