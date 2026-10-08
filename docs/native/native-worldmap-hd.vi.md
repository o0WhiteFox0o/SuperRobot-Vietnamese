> **Ngôn ngữ / Language:** [Tiếng Việt](native-worldmap-hd.vi.md) · [English](native-worldmap-hd.en.md) · [中文](native-worldmap-hd.md)

# Đối thoại tài nguyên HD bản đồ thế giới

2026-09-09. Mục tiêu hiện tại là "cũng quan trọng. Thông tin tình báo mà không ai khác có thể có được", bản đồ thế giới đằng sau cuộc trò chuyện này. Người dùng đã sửa rõ ràng phạm vi bằng ảnh chụp màn hình trò chơi: các thí nghiệm về rừng và đường trên bảng chiến đấu không thuộc phạm vi phân phối này và không được bao gồm trong gói dùng thử độ phân giải cao hiện tại.

Cập nhật tiếp theo: Hộp thoại cốt truyện tiêu chuẩn của lối vào độ phân giải cao đã được kết nối với [Giao diện người dùng Apple thời gian thực](native-dialogue-ui.md), cung cấp tính năng ngắt dòng, phân trang, phát lại và kiểm soát tốc độ tự động. Hồ sơ hiện tại chỉ đọc các họa tiết nghệ thuật thuần túy trong danh sách được phép; Hình tượng Trung Quốc trong các gói hợp nhất lịch sử không được đưa vào gói nghệ thuật gốc.

## Tài nguyên và đường dẫn hiển thị

Tài nguyên ban đầu là **5604** và dữ liệu được giải nén hoàn chỉnh khớp duy nhất với bộ nhớ đã ghi `0x2CF200`. Khôi phục bản đồ từ các đỉnh và tia UV của danh sách hiển thị ban đầu, sau đó lấy khu vực Châu Âu để lấy bản đồ nguồn 512×512. Bản đồ gốc sử dụng các ô CI4 64×64; 512×512 là kích thước vật liệu cũ và không phải là giới hạn trên của bản recomp gốc hoặc RT64.

Tập lệnh đóng gói tại thời điểm đó `build_worldmap_runtime_pack.py` (đã bị xóa vào ngày 24-09-2026) cắt bản đồ độ phân giải cao trở lại các ô **512×512** theo tọa độ ban đầu, **8 lần mật độ tuyến tính** của kết cấu ban đầu, tương ứng với khung vẽ bản đồ **4096×4096**. Trò chơi vẫn gửi lưới bản đồ, máy ảnh và điểm đánh dấu ban đầu, đồng thời RT64 chọn nội dung HD với hàm băm kết cấu đã được xác minh. Bản đồ không bị đẩy lùi về CI4, cũng như không được tạo thành lớp phủ toàn màn hình với các ký tự và văn bản.

[`graphics.cpp`](../../src/host/graphics.cpp) đọc `srw64-worldmap-hd.json` trong gói, kiểm tra kích thước thay thế thực tế và độ phóng đại UV trong khóa của bộ đệm kết cấu và ghi kết quả vào `worldmap-texture-runtime.json` trong thư mục chạy. Đây chính là tập dữ liệu được trình tạo ô GPU đọc; việc kiểm tra không sửa đổi bản ghi truy cập của kết cấu hoặc RDRAM trò chơi. Trong cùng một nhiệm vụ phát lại, người ta đã xác nhận rằng kích thước ban đầu của ô 57/57 là 64 × 64, kích thước thay thế là 512 × 512 và độ phóng đại tọa độ là 8 × 8.

`TextureSampler.hlsli` của RT64 sử dụng `tcScale` thực tế để thay thế họa tiết; lượng tử hóa UV tự nhiên có độ chính xác thấp của nó không áp dụng cho việc thay thế HD. Tính năng lọc kết cấu thông thường vẫn tồn tại và độ phóng đại kết xuất bên trong và mật độ pixel vật liệu là hai cài đặt độc lập. Chỉ tăng độ phóng đại hiển thị bên trong không thể làm nổi bật các chi tiết không có trong cảnh quay cũ.

## Vật liệu AI và hình học gốc

Sử dụng image_gen tích hợp để chỉnh sửa hình ảnh tài nguyên thực tế và tham khảo kiểu nền do người dùng cung cấp. Không có ký tự, cửa sổ hoặc điểm đánh dấu màu vàng nào được vẽ vào nội dung bản đồ.

- Đề xuất hình ảnh toàn bộ: `assets/hd-ai/worldmap-runtime/ai-v1/`, đầu ra mô hình thực tế **1254×1254**.
- Đề thi chi tiết Châu Âu: `ai-detail-v1/`, vùng nguồn là ảnh gốc `(0,64)-(320,256)`, kết quả thực tế là **1619×971**. Tinh chỉnh riêng từng vùng thấu kính để đạt được mật độ chi tiết hiệu quả cao hơn và tỷ lệ núi nhỏ hơn.
- Hiệu chỉnh vị trí: `ai-detail-registered-v2/`, sử dụng các vùng màu đất, biển và địa hình của bản đồ gốc để hạn chế trường tọa độ trơn tru và lấy mẫu lại để tạo các pixel gốc của bản đồ. Ghi lại đầu ra thô, tập lệnh chỉnh sửa, trường tọa độ, phiên bản thư viện và chỉ báo trùng khớp mặt nạ đất phía trước và phía sau. Hình ảnh gốc đã chỉnh sửa không bằng hình học chính xác ban đầu và khu vực chỉnh sửa vẫn bị giới hạn bởi lớp bảo vệ hình ảnh nguồn.
- Mặt biển nguyên gốc, rìa bờ hẹp và ranh giới ngói được giữ lại trong quá trình tổng hợp; các pixel bề mặt biển được tạo ra bị cấm thêm vùng nước mới vào vùng đất ban đầu. Alpha được lấy từ bảng màu RGBA16 ban đầu, đầu tiên được phóng to trên toàn bộ hình ảnh, sau đó được cắt lát.

4096×4096 là **kích thước họa tiết chạy cuối cùng** và không có nghĩa là mô hình trực tiếp xuất ra hình ảnh 4K gốc. Các chi tiết có sẵn đến từ đầu ra AI bị đóng băng nói trên. Lớp bảo vệ hình ảnh gốc và hình chiếu của trò chơi cũng sẽ ảnh hưởng đến giao diện của các cạnh cục bộ.

57 bản đồ băm đã được xác minh đã được thay thế; các hàm băm được chia sẻ có sự mơ hồ về vùng lân cận tiếp tục sử dụng gói ban đầu. Giữ lại các nguồn tài nguyên hiện có bên ngoài các khối cắt của Châu Âu. Lần này không có gì khẳng định rằng tất cả bản đồ thế giới hoặc bản đồ chiến đấu đã được chuyển đổi thành độ phân giải cao.

## Bao bì hiện tại

57 ô Châu Âu này được lưu trữ trong `assets/hd-ai/worldmap-runtime/pack-v6/`. Bắt đầu từ 25-09-2026, chúng không còn nằm trong gói nữa: Châu Âu đã đổi sang Bailian để sử dụng chúng làm bản đồ cơ sở để điền thông tin chi tiết và vẽ lại, xem [Châu Âu chuyển sang Bailian](native-worldmap-regions-hd.md#欧洲改用百炼2026-09-25). pack-v6 vẫn nên được giữ lại: đây là bản đồ cơ sở của Châu Âu Mới và mẫu phong cách vẽ của [`worldmap_surfaces.py`](../../tools/hd_ai/worldmap_surfaces.py) `prepare` cũng được lấy từ kết cấu đất của nó.

Tập lệnh đóng gói ban đầu, gói hình tượng vuông hình quả táo và gói cũ kết hợp hình tượng, lát hình đại diện và bản đồ đã bị xóa trong quá trình dọn dẹp di sản HD vào ngày 24 tháng 9 năm 2026. Xác minh kết cấu 57/57 ở trên và bản ghi chạy `live-v6` của ngày 2026-09-09 chỉ mang tính chất tham khảo lịch sử và không thể hiện việc chấp nhận lại gói hiện tại.