> **Ngôn ngữ / Language:** [Tiếng Việt](native-model-viewer.vi.md) · [English](native-model-viewer.en.md) · [中文](native-model-viewer.md)

# Duyệt tài nguyên mô hình cục bộ và xác minh 5600

5600 Tùy chọn "giọt nước bản địa · 3.968 khuôn mặt" và so sánh trò chơi thực tế đã được thêm vào. Phiên bản này sử dụng lưới GPU chủ và ánh sáng theo từng pixel; xem [Thay thế mô hình gốc](../native/native-model-replacement.md) để biết mục nhập thử nghiệm, phương pháp truy cập và bằng chứng.

Được thành lập vào ngày 2026-09-09, bổ sung xác minh trò chơi thực tế vào ngày 2026-09-10. Mã nguồn trang nằm trong `tools/model_viewer/` và trang, mô hình cũng như kết cấu đã tạo được giữ trong `build/model-viewer/` bị bỏ qua. Dịch vụ chỉ nghe `127.0.0.1`, không có yêu cầu tải lên, xuất bản trên đám mây hoặc kết cấu bên ngoài.

## Duyệt trang

Trang này chứa **483** vùng chứa hình học được phân tích lần này, với tổng số **82.122** hình tam giác được vẽ; bao gồm cả hình học không gian và hình học đồng phẳng, số lượng vật chứa không thể được coi là số lượng vật thể hoặc cảnh độc lập.

- Lọc theo tìm kiếm số/tên, loại hình học và trạng thái vị trí; hình thu nhỏ bên trái là từ tọa độ ban đầu.
- "Trước/Tiếp theo" ở đầu cửa sổ mô hình và các phím mũi tên trái và phải trên bàn phím chuyển đổi theo kết quả lọc hiện tại; vị trí hiện tại được hiển thị và các nút tương ứng sẽ tự động bị tắt ở đầu và cuối. Việc chọn thẻ sẽ cuộn đến vị trí hiển thị trong danh sách.
- Kéo chuột để xoay, cuộn bánh xe để thu phóng và nhấp chuột phải để xoay; cung cấp chế độ xem nheo/phía trước/trên cùng, xoay, đặt lại và lớp phủ khung dây.
- Ba phương pháp hiển thị: bản đồ nguồn, khuôn xám và wireframe; nhiều tài nguyên danh sách hiển thị có thể hiển thị các thành phần riêng lẻ.
- Xuất OBJ hình học của phần hiện tại theo tọa độ cục bộ ban đầu của nó; không có vật liệu, xương hoặc hình ảnh động nào được xuất khẩu.
- 5600 được bật theo mặc định; khi có tài nguyên nhãn HD gốc (`build/recomp/native-marker`) cục bộ, bạn có thể chuyển đổi giữa hình thoi ban đầu (8 cạnh) và lưới HD gốc và hình ảnh so sánh máy thực tế của nó được hiển thị ở góc trên bên phải. Các đoạn URL có thể được nhắm mục tiêu trực tiếp, chẳng hạn như `/#5584`.

Sử dụng lại đầu vào khảo sát tĩnh hiện tại:

```sh
npm ci --prefix tools/model_viewer --ignore-scripts --no-audit --no-fund
.venv/bin/python tools/model_viewer/build.py
.venv/bin/python tools/model_viewer/serve.py
```

In URL cục bộ sau khi dịch vụ được khởi động; cổng có thể được chỉ định bằng `--port`. Đầu vào của bản dựng là các tài nguyên gốc trong `assets/models/3d-2026-09-09/`, `geometry-data.json` và `geometry-survey.json`, hãy xem [Phân tích 3D](3d-model-replacement-analysis.md) để biết chi tiết. Three.js được cố định thành `0.180.0` và giấy phép phụ thuộc được xuất cùng với trang.

## Hiển thị giới hạn và kiểm tra

Trang này hiển thị các đỉnh cục bộ, hình tam giác và các vật liệu đơn giản hóa và không mô phỏng các chuyển đổi cảnh, ống kính, hoạt ảnh, pha trộn RDP đầy đủ hoặc ánh sáng trong trò chơi gốc. Nhiều phần cũng có thể là khung hiệu ứng và tất cả các phần được hiển thị cùng lúc không thể được coi là một cử chỉ trò chơi.

**2.713** tệp kết cấu đã được trích xuất; **27** tài nguyên chứa các phương pháp tải kết cấu chưa được xác nhận và các lô tương ứng sẽ chuyển về màu đồng nhất, như trang nhắc nhở rõ ràng. Chế độ xem bản đồ nguồn giúp dễ dàng xác định nội dung và không cho là tương đương với cảnh quay trò chơi RT64.

Tất cả 483 mô hình đã được kiểm tra sau khi xây dựng về số lượng tam giác, độ dài đỉnh/UV, giá trị hữu hạn và tất cả các tham chiếu kết cấu/hình thu nhỏ. Mỗi kết cấu trong số 70 kết cấu nguồn trong 5604 và 5605 đều nhất quán với các pixel RGBA của trình trích xuất bản đồ hiện có. Cú pháp JavaScript, trình biên dịch Python và các yêu cầu HTTP gốc đều được chuyển.

Trình duyệt tái tạo sự cố với thẻ mục lục bị nén lên cao 2 pixel bởi các hàng lưới tự động; thay vào đó, nó tính toán độ cao của hàng dựa trên nội dung và cho phép hình thu nhỏ chia tỷ lệ theo tỷ lệ. Sau khi sửa chữa, chiều cao bố cục của tất cả 483 thẻ đã được kiểm tra, ảnh chụp màn hình của 5631 và 5604 trang đã được xem thực tế và 5631 → 5632 → 5631, việc vô hiệu hóa đầu và đuôi trong bộ lọc định vị và đo việc vô hiệu hóa kết quả tìm kiếm trống. Lỗi JavaScript không được trình duyệt ghi lại. Những bước kiểm tra này chỉ xác minh các tương tác trên trang và không thêm bằng chứng về thời gian chạy trò chơi.

## 5600: Đã xác nhận quyền sở hữu màn hình và biến dạng cấu trúc liên kết cố định

Bằng cách sử dụng ảnh chụp nhanh tác vụ hiện có của `female-story-2`, ba bản sao độc lập sẽ được tạo. Các bộ mô tả tác vụ giống hệt nhau theo từng byte và ảnh chụp nhanh ban đầu không thay đổi.

| Phát lại | Phạm vi sửa đổi | Kết quả hình ảnh GPU |
| --- | --- | --- |
| đường cơ sở | Không sửa đổi | Nhẫn chấm và kim cương màu vàng nguyên bản |
| ẩn | 12 bộ lệnh tam giác được đổi thành F3DEX2 SP no-op; 52 byte thay đổi thực tế | những viên kim cương và những chiếc nhẫn vụn đã biến mất; 1.369 thay đổi pixel, phạm vi `(437,305)–(521,377)` |
| kéo dài | Chỉ có sáu đỉnh ba chiều được thay đổi, X/Z được nhân với 2, Y được nhân với 3; 14 byte thực sự đã được thay đổi | Phần ba chiều được kéo dài, các vòng và các hình ảnh khác được giữ lại; 4.639 pixel được thay đổi, phạm vi là `(439,282)–(521,395)` |

Ba lần phát lại RT64/Metal đều thoát 0; các hình ảnh 960×720 được GPU đọc lại sau khi hoàn thành đã được xem từng hình một. Sự khác biệt pixel bên ngoài vùng được đánh dấu mục tiêu là 0.

Điều này chứng tỏ rằng **5600 thực sự tương ứng với các mặt phẳng vòng và hình thoi màu vàng của bản đồ cốt truyện, đồng thời cũng chứng minh rằng việc sửa đổi các đỉnh của nó sẽ đi vào bản vẽ RT64 thực tế**. Phạm vi của bằng chứng trong phần này là phát lại kết xuất một tác vụ; xem bên dưới để biết cách thay thế cấu trúc liên kết tiếp theo và tải trò chơi thực tế.

## 5600: Nguyên mẫu mô hình cao và ROM thử nghiệm (đã xóa)

24-09-2026: Nguyên mẫu mô-đun cao 96 mặt, ROM thử nghiệm đã mã hóa lưới thành Tài nguyên 5600, cũng như tính năng phát lại và xác minh máy thực của chúng, đã được thay thế bằng [thẻ HD gốc](../native/native-model-replacement.md). Các tập lệnh có liên quan, các biến thể `model5600` ROM, các bài kiểm tra và hai thư mục mô hình đã bị xóa trong quá trình dọn dẹp kế thừa HD và trình duyệt không còn hiển thị chúng nữa; bằng chứng phát lại từ phần trước chỉ nhằm mục đích lịch sử.

## 5584: Đã tìm thấy lối vào tĩnh, vẫn cần bằng chứng kích hoạt âm mưu

Cập nhật ngày 24 tháng 9 năm 2026: Bảng này là bảng đối tượng mô hình của bản đồ thế giới cốt truyện. 5584 là アルビオン (nội dung → bảng khớp mô hình `801C560C`), được vẽ bởi `3D33` trong quá trình điều hướng; mỗi tàu tương ứng với 5591 ラー・カイラムĐể thay thế máy thật, hãy xem [Mô hình cắt cảnh bản đồ thế giới HD](../native/native-ship-model.md). Phân tích tĩnh tại thời điểm đó được giữ lại dưới đây.

`load_000A7EC0` trong ROM `0xAAF30`/VRAM `0x801C5670` là bảng tài nguyên đối tượng mô hình, chỉ số 0 là 5584, chỉ số 15 là 5600. Bảng cũng chứa tài nguyên hình dạng tàu và tài nguyên bản đồ đã được trích xuất trước đó.

`0x801C3490` chọn mục nhập bảng theo byte thấp của tham số thứ hai; `0x801C34EC` đọc ID tài nguyên và sau đó `0x801C3560` gọi `0x8008B4F4` để ghi ID tài nguyên vào vùng tham số `sp+0x1C`. Ngoài ra còn có `0x801C4DC0` so sánh/cập nhật các đối tượng với các giá trị đã chọn trong `0x801C58BC` và gọi cùng một đường dẫn xây dựng trong `0x801C4E30`.

Phương pháp xác minh tiếp theo là: sau khi xác nhận danh tính của lớp phủ này, hãy theo dõi lệnh gọi chỉ mục 0 của `0x801C3490`, ghi lại người gọi, vị trí tập lệnh và cảnh, sau đó lấy khung GPU thực tế. Hiện tại, chỉ có các bảng tĩnh và đường dẫn cuộc gọi được định vị và không có xác nhận nào về các chương, tên tàu hoặc hình thức thực tế của tài nguyên này trong tuyến đường đã đo. Để biết bản ghi có cấu trúc, hãy xem [model-5584-reference.json](../../assets/models/3d-2026-09-09/model-5584-reference.json).