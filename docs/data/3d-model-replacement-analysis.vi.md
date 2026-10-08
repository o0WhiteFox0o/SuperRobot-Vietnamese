> **Ngôn ngữ / Language:** [Tiếng Việt](3d-model-replacement-analysis.vi.md) · [English](3d-model-replacement-analysis.en.md) · [中文](3d-model-replacement-analysis.md)

# SRW64 Phân tích thay thế mô hình và 3D gốc

Cập nhật ngày 10-09-2026: [Thay thế giọt nước GPU gốc](../native/native-model-replacement.md) của 5600 đã hoàn thành xác minh giới hạn từ phần mở đầu của nhân vật nữ chính cho đến bản đồ chiến thuật của tập đầu tiên. Các lưới điểm nổi hiện đại và vật liệu Kim loại đã được tích hợp vào thứ tự vẽ cảnh và trò chơi gốc cung cấp các tư thế và máy ảnh.

2026-09-09. Đối tượng là ROM Rev 0 của Nhật Bản trong kho lưu trữ này và máy chủ gốc N64Recomp + RT64/Metal hiện tại. Cấu trúc cơ bản của màn chiến đấu rõ ràng là **Nền 3D + Hình ảnh cơ thể 2D**. Tác phẩm gốc có hình học ba chiều có thể được trích xuất, phù hợp để bắt đầu từ điểm đánh dấu cốt truyện, bối cảnh cảnh chiến đấu và tài nguyên hình dạng con tàu; hiệu suất 2D của các cơ quan chiến đấu thông thường cần được xử lý theo một loại kỹ thuật khác.

## Những phần nào của tác phẩm gốc được sử dụng 3D?

| Phần | Bằng chứng và phán quyết hiện tại | Ý nghĩa của việc thay thế mô hình |
| --- | --- | --- |
| Nền chiến đấu | Nền 3D, được trình bày kết hợp với các họa tiết cơ thể 2D. Bề mặt đất, bề mặt phù điêu, các mảng nền dọc và hình dạng tòa nhà có thể nhìn thấy được trong tài nguyên hình học ROM. Điều cần xác nhận là cảnh, camera và draw call tương ứng với từng ID nền | Hướng đi đáng giá nhất để mở rộng đầu tư nghệ thuật, có thể thay thế địa hình, kiến ​​trúc, hình học nhìn xa và vật liệu theo từng cảnh, trong khi vẫn giữ nguyên các họa tiết cơ thể và kịch bản chiến đấu ban đầu |
| Câu chuyện bản đồ thế giới | 5604 và 5605 mỗi cái có 70 mặt hình chữ nhật và 140 hình tam giác được vẽ. Tọa độ Y của tất cả các đỉnh dùng để vẽ là 0; những ngọn núi trong ảnh gốc chủ yếu là họa tiết | Lưới lưu trữ bản đồ có thể được thay thế; thêm núi thật là địa hình ba chiều mới dựa trên mặt phẳng ban đầu |
| Vẽ bản đồ đánh dấu ba chiều | 5600 phiên bản gốc với tổng cộng 16 hình tam giác được vẽ. Đã hoàn tất xác nhận quyền sở hữu, phát lại bên Diamond 8 → 96 và mở thực tế ROM thử nghiệm cho bản đồ chiến thuật tập đầu tiên | Đã xác minh trình tải gốc, xoay, thay đổi và cắt vị trí lô; bước tiếp theo để xác minh việc nhập lại/lưu phục hồi và nhiều cảnh hơn |
| Tài nguyên hình dạng tàu/máy bay | 5584–5597 là con tàu được vẽ ở phía trước đường ray khi đi trên bản đồ thế giới cốt truyện `3D33`. Tên tàu đã được gắn vào bảng mô hình và bảng phù hợp (5584 アルビオン, 5585 アーガマ, 5588ネェル・アーガマ, 5591 ラー・カイラム, v.v., xem [Cảnh cắt bản đồ thế giới Mẫu HD](../native/native-ship-model.md)); 5590, 5592, 5596 có thẻ tên, 5598/5607 là cảnh quan | 15 5597 và 5601 đã được cài đặt lại theo cài đặt và thay thế bằng máy thật, 5597 và 5601 không có đường thoát và chưa được xử lý |
| Một số ứng cử viên lớp nền/hiệu ứng | 5598, 5610, v.v. là các phần phẳng hoặc nhiều phần phẳng; 5599, v.v. là sự kết hợp của nhiều phần. Chưa có phân tích đầy đủ về mối quan hệ giữa hoạt hình và tổ chức cảnh | Bản thân mặt phẳng cũng có thể nhập kết xuất 3D; kết cấu và trình tự thời gian cần được kết hợp để phân biệt nền, khung hiệu ứng và các thành phần rắn |
| Chương 1 Bàn cờ chiến thuật | Đã xem hình ảnh GPU bản đồ; ảnh chụp nhanh nhiệm vụ cuối cùng của `female-map-audio-*` đã kiểm tra chủ yếu là bản vẽ có kết cấu hình chữ nhật và không có lệnh tải đỉnh/tam giác nào xuất hiện. Hình dáng ba chiều của tòa nhà không đủ để chứng minh rằng có một mô hình tòa nhà có thể thay thế được | Gạch có độ phân giải cao thuộc về quy trình kết cấu hiện có; việc xây dựng các thị trấn và khu rừng bàn cờ đòi hỏi phải hiển thị cảnh bản đồ mới. Kết luận này chỉ giới hạn ở các bản đồ và nhiệm vụ đã được kiểm tra |
| Cơ thể chiến đấu thông thường, hình đại diện nhân vật, giao diện người dùng | Nhà sản xuất tuyên bố rõ ràng rằng bản thân robot là 2D. Những hình ảnh chiến đấu của Titan 3 ở tập đầu tiên đã được xem; tỷ lệ và phối cảnh không thể được sử dụng làm bằng chứng của mô hình bộ xương | Điều trực tiếp nhất là tiếp tục sử dụng vật liệu có độ phân giải cao 2D; việc thay đổi sang cơ thể 3D yêu cầu một mô hình, hành động và ràng buộc hiệu suất mới và bằng chứng hiện tại không hỗ trợ việc mô tả nó như một sự thay đổi mô hình đơn giản |

Phỏng vấn trực tiếp nhà sản xuất: [Dengeki Online, 2022-02-11](https://dengekionline.com/articles/109826/). Cuộc phỏng vấn sử dụng từ ngữ "nghi ngờ 3D" làm nền; báo cáo này phân loại rõ ràng dự án theo "nền 3D + hình ảnh nội dung 2D" để tránh hiểu cách diễn đạt này có nghĩa là nền chỉ là một bức tranh phẳng. Cảnh 3D có thể chứa cả lưới ba chiều và mặt phẳng kết cấu, đồng thời bố cục cụ thể của từng phần tử nền vẫn cần được ràng buộc từng phần một. Lần này, chúng tôi không suy luận việc thực hiện tất cả các hiệu ứng đặc biệt của vũ khí dựa trên điều này.

## Khảo sát tĩnh ROM này

Nhập SHA-256: `ee5f4a21d8e5f7827d21199e27800edf250df9a8e4d10befb1a6992df597b13e`.

- Quét tất cả các mục **6,436** trong bảng tài nguyên nén.
- Tổng số tài nguyên **5584–6066****483** với tiêu đề `36340038`, nhất quán với các vùng chứa được các trình phân tích cú pháp bản đồ hiện có nhận dạng.
- Tải trọng đỉnh và tham chiếu tam giác đã được giải quyết cho **606** danh sách hiển thị loại 0/5 trong các vùng chứa này; tất cả đều đạt đến lệnh cuối cùng và các kiểm tra tham chiếu cũng như phạm vi đều được thông qua. 624 MoveWords đều có cài đặt màu sáng và không thay đổi vị trí đỉnh của thống kê này.
- Kiểm tra tọa độ cục bộ các đỉnh tham chiếu của mỗi container: **182** đồng phẳng, **301** không đồng phẳng. Việc ghép nhiều mặt phẳng khác nhau cũng có thể không đồng phẳng và không thể được gọi là mô hình 301 thực thể đóng, 301 vật thể hoặc 301 mô hình cảnh giới hạn tương ứng.
- Phân cấp cảnh, hoạt ảnh, cắt có điều kiện và tài liệu đầy đủ không được trình phân tích cú pháp giải thích. 5638 cũng chứa các bộ mô tả loại 8, chức năng của chúng sẽ không được giải thích lần này. Các khu vực khác của ROM và hình học được tạo trong thời gian chạy cũng không được bao gồm trong tầm cỡ thống kê vùng chứa này.
- Bộ vị trí đỉnh và số tam giác 5604/5605 phù hợp với kết quả trích xuất bản đồ hiện có.

Các sơ đồ chẩn đoán được vẽ dựa trên tọa độ thô được trích xuất, không tải kết cấu, vật liệu, máy ảnh trò chơi hoặc hoạt ảnh gốc. Thẻ hình dạng tiếng Anh là một danh mục ứng cử viên và không phải là tên nội dung trò chơi đã được xác nhận.

![Mẫu hình học gốc của ROM](../../assets/models/3d-2026-09-09/geometry-samples.png)

Sản phẩm khảo sát địa phương:

- [Điều tra dân số về nguồn lực](../../assets/models/3d-2026-09-09/header-survey.json)
- [Kiểm tra danh sách hình học và từng danh sách hiển thị](../../assets/models/3d-2026-09-09/geometry-survey.json)
- [Tập lệnh phân tích cú pháp tĩnh](../../assets/models/3d-2026-09-09/survey_geometry.py) và [Kết quả xác minh](../../assets/models/3d-2026-09-09/validation.json)
- [Liên kết ảnh chụp nhanh nhiệm vụ hiện tại](../../assets/models/3d-2026-09-09/snapshot-bindings.json)
- Mẫu OBJ hình học: [5584](../../assets/models/3d-2026-09-09/resource-5584-geometry.obj), [5592](../../assets/models/3d-2026-09-09/resource-5592-geometry.obj), [5600](../../assets/models/3d-2026-09-09/resource-5600-geometry.obj), [5604](../../assets/models/3d-2026-09-09/resource-5604-geometry.obj), [5614](../../assets/models/3d-2026-09-09/resource-5614-geometry.obj), [5750](../../assets/models/3d-2026-09-09/resource-5750-geometry.obj). Chỉ chứa các đỉnh và mặt cục bộ, không chứa vật liệu, tia cực tím, xương hoặc hình ảnh động; bị bỏ qua `build/`.

## Ranh giới bằng chứng thời gian chạy

Đánh giá phân tích ban đầu là ảnh chụp nhanh tác vụ/RDRAM hiện có trên đĩa. Sau đó, quá trình phát lại RT64/Metal của các bản sao độc lập, ẩn riêng lẻ, biến dạng đỉnh cấu trúc liên kết cố định và thay thế poly cao 96 mặt đã được hoàn thành cho 5600. 2026-09-10 Mô-đun cao được biên dịch thành các tài nguyên ROM độc lập và trình tải ban đầu được sử dụng để hoàn thành quá trình chạy thực tế của 16.800 VI bắt đầu từ SRAM trống, đoạn hội thoại mở đầu của phụ nữ đối với bản đồ chiến thuật của tập đầu tiên. Tải, xoay, thay đổi vị trí cốt truyện và cắt đều có bằng chứng về nhiệm vụ/GPU; tuyến đường đầy đủ không được xác minh bằng phần cứng N64. Để biết chi tiết, hãy xem [Trang tài nguyên cục bộ và bản ghi xác minh](native-model-viewer.md).

Trong `build/recomp/gfx-probes/female-story-2/`, 5604, nội dung giải nén hoàn chỉnh khớp với bộ nhớ `0x2BF9F0` và mục nhập danh sách hiển thị của nó `0x2E4480` được gọi bởi tác vụ gốc; 5600 nội dung hoàn chỉnh khớp với `0x2BDE68` và mục nhập `0x2BF7D0` được gọi. Địa chỉ chỉ thuộc về ảnh chụp nhanh này và không thể ghi dưới dạng địa chỉ cố định cho toàn bộ khung cảnh.

`first-map-reload-2` ảnh chụp nhanh cuối cùng cũng nằm ở 5729, 5734, 5878, 5879, 5974, 5975; `first-map-turn5-reload-1` cư trú tại 5746, 5747, 5748, 5920, 5975. Tác vụ gốc không được quan sát khi gọi danh sách hiển thị hình học của chúng tại thời điểm này, vì vậy chúng chỉ cung cấp manh mối theo dõi cảnh tiếp theo và không thể quy trực tiếp cho nền hiện có.

Đã xem hình ảnh GPU hiện có: Bản đồ thế giới `worldmap-runtime/live-v6/present-3540.png`, Bảng chiến thuật `female-map-audio-1/present-6660.png`, Battle of Titans 3 `first-map-reload-2/present-3780.png`. Quan sát hình ảnh, hình học tĩnh, vị trí bộ nhớ và lệnh gọi danh sách hiển thị được ghi lại riêng biệt và không thay thế lẫn nhau.

## Dự án gốc hiện tại có thể làm gì?

[`graphics.cpp`](../../src/host/graphics.cpp) hiện tại chấp nhận tác vụ ban đầu trong `send_dl()` và cho phép sửa đổi trong `display_copy` trước khi gửi trong `processDisplayLists()`; đây là điểm bắt đầu sẵn sàng để nghiên cứu sự thay thế hình học cục bộ. Các phông chữ, hình đại diện và bản đồ thế giới hiện có đã được chuyển đổi sang độ phân giải cao thành `loadReplacementDirectory()`, đây là sự thay thế kết cấu.

RT64 cố định được sử dụng là `43373749dac9bbc1b653e6a02aed40a9e1783bed`. README của nó và [mô tả ngược dòng](https://github.com/rt64/rt64#features-in-development-in-priority-order) của kiểm tra này vẫn liệt kê các thay thế Mô hình đang được phát triển. Máy chủ hiện tại không có trình tải gói thay thế mô hình glTF/FBX/OBJ và không thể hứa rằng mô hình có thể được thay thế bằng cách đặt nó vào thư mục gói kết cấu.

Các thử nghiệm hiện đã hoàn thành và các dự án tiếp theo:

1. ** Nhiệm vụ phát lại và mở thực tế 5600 đã được thông qua. ** Vị trí, kích thước và vòng nét đứt ban đầu được sử dụng sau bề mặt kim cương 8 → 96 và sự khác biệt giữa các khung so sánh trò chơi thực được giới hạn ở khu vực kiểm tra kim cương. Giữ mục nhập danh sách hiển thị ban đầu, nối hình học mới vào tài nguyên và sử dụng con trỏ tương đối phân đoạn 4. Trình tải ban đầu chịu trách nhiệm về bộ nhớ tài nguyên; địa chỉ cố định của ảnh chụp nhanh không được đưa vào thời gian chạy.
2. **Nhập lưới điện toàn cầu và phạm vi phủ sóng rộng hơn vẫn cần được triển khai. ** Hiện tại, nó là trình biên dịch dành riêng cho 5600 và hệ thống nhận dạng cảnh tùy ý và nhập OBJ/glTF chưa được thiết lập. Các tài nguyên khác vẫn cần được xác minh riêng về chất liệu, độ trong suốt, độ sâu, crop, camera, dung lượng và vòng đời; nhập lại và khôi phục lưu trữ 5600 chưa được chấp nhận.

Việc hoán đổi trực tiếp ROM vẫn bị hạn chế bởi khả năng nén, bộ nhớ và danh sách hiển thị cũ. Thử nghiệm 5600 giải quyết vấn đề tăng trưởng công suất bằng cách chuyển hướng các mục trong bảng tài nguyên sang vùng trống ROM; điều này chỉ chứng tỏ rằng tài nguyên và quy trình này có sẵn. Máy chủ gốc cũng có thể cung cấp quyền truy cập hiển thị và nội dung bổ sung, đồng thời chức năng kết cấu độ phân giải cao hiện có sẽ không tự động cung cấp khả năng thay thế hình học phổ quát.

## Thứ tự ưu tiên được đề xuất

| Trình tự | Đối tượng | Lý do lựa chọn và xác minh tiếp theo |
| --- | --- | --- |
| 1 | 5600 điểm cốt truyện | 96 lần chạy mở ROM thử nghiệm đã được hoàn thành để xác minh việc xoay, thay đổi vị trí và cắt; lần vào lại tiếp theo, khôi phục kho lưu trữ và nhiều tuyến đường khác sẽ được thêm vào |
| 2 | Một nền tảng chiến đấu chung | Lợi ích có thể nhìn thấy cao nhất. Chụp các khung hình ổn định trong trận chiến, liên kết mặt đất, tầm nhìn xa và các tòa nhà với ID tương ứng, sau đó tạo một mẫu cảnh duy nhất |
| 3 | Một con tàu đã được liên kết đến hiện trường | Lưới có thể được chiết xuất; đầu tiên thêm kết cấu và quyền sở hữu ống kính, xác minh các thành phần, hướng và chuyển động, sau đó mở rộng sang các tàu khác |
| 4 | Bản đồ thế giới cốt truyện ba chiều | Phiên bản gốc bằng phẳng và có thể thêm núi hoặc cột mốc; bờ biển, tên địa điểm/vị trí đánh dấu lô đất và hiệu suất ống kính ban đầu phải được duy trì |
| Theo dõi hướng độc lập | Bàn cờ chiến thuật 3D đầy đủ và cơ thể chiến đấu 3D đầy đủ | Cái trước yêu cầu tạo cảnh bản đồ và các quy tắc lựa chọn/tắc, trong khi cái sau yêu cầu hệ thống hiệu suất hành động và vũ khí; phạm vi công việc lớn hơn đáng kể so với việc thay thế hình học hiện có |

Đề xuất hiện tại là "Hiệu suất 2D của khung máy bay ban đầu + hình học cảnh tinh tế hơn + kết cấu độ phân giải cao", trước tiên hãy sử dụng công nghệ xác minh dấu hiệu, sau đó sử dụng nền chiến đấu để xác minh lợi ích của màn hình. Việc đặt tên cho tất cả nội dung tuyến đường và phạm vi bao phủ của tất cả các kịch bản vẫn chưa được hoàn thành. Báo cáo này cung cấp phạm vi đầu vào và ứng viên đã được xác minh.