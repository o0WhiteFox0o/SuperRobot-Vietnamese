> **Ngôn ngữ / Language:** [Tiếng Việt](recomp-peer-comparison.vi.md) · [English](recomp-peer-comparison.en.md) · [中文](recomp-peer-comparison.md)

# Dự án recomp N64 tương tự và tính khả thi nâng cao SRW64

Ngày xác minh: 2026-09-10.

Lần này, chúng tôi đã kiểm tra mã nguồn mở của bốn dự án trò chơi và năm Bản mod câu chuyện thu hoạch, đồng thời so sánh chúng với ghi chú phát hành và cách triển khai máy chủ hiện tại của SRW64. Các dự án bên ngoài không được biên dịch hoặc chạy trên máy này; "Mã nguồn đã được triển khai" và "Xác minh/Phát hành của Bên Dự án" được mô tả tương ứng. Nhánh hiện tại có thể chứa các sửa đổi chưa được đưa vào phiên bản phát hành. Cơ sở hoạt động của SRW64 tuân theo hồ sơ nghiệm thu hiện có. Không có hoạt động trò chơi mới hoặc sửa đổi cách triển khai trò chơi vào thời điểm này.

Kết luận: Các hướng dẫn trưởng thành có thể học được tập trung vào cài đặt gốc và Mod, nội suy chuyển động 2D, màn hình rộng cảnh, thông tin trạng thái và chỉnh sửa tài nguyên. SRW64 đã có đoạn hội thoại bản địa của Trung Quốc, kết cấu có độ phân giải cao một phần và nguyên mẫu mô hình GPU độc lập. Bước tiếp theo có thể là tích hợp chúng vào một phiên bản có thể định cấu hình, sau đó mở rộng thanh bên thông tin, nhịp điệu chiến đấu và màn hình cảnh. Mã từ các dự án bên ngoài không thể thay thế trực tiếp công việc ánh xạ tài nguyên, đối tượng và tập lệnh của SRW64.

## 1. Phiên bản mã nguồn đã được xác minh

| Dự án | Gửi xác minh | Phạm vi |
| --- | --- | --- |
| [Harvest Moon 64 được biên dịch lại](https://github.com/HarvestMoon64Recomp/HarvestMoon64Recomp) | `399a4f2b82a8b8dde4bb033e81f8a9b41d796a32` | Nội suy Bản đồ/Sprite, Màn hình rộng, Trình khởi chạy và Giao diện Mod |
| [Người gây rắc rối](https://github.com/ThiagoLira/trouble-makers-pc-recomp) | `765b179c6f4bfbbb65dc7b371035798ca573202b` | Màn hình rộng, tua lại cảnh, tua đi nhanh, các vấn đề hiển thị đã biết; tương ứng với phiên bản trước v0.8.2 |
| [Tiến sĩ Mario 64 Recomp Plus](https://github.com/theboy181/drmario64_recomp_plus) | `af91e3bf56b1ffc329ff4327fdc2380515463de7` | Bản vá vẽ viên nang và mô tả chức năng công cộng |
| [Giấy Mario ReCut](https://github.com/SMCGames/Paper-Mario-ReCut) | `098be0a501eecd5bb894a47964061d05eeedc3a2` | Xuất kết cấu, cập nhật nóng thay thế, biên tập bản đồ |
| [Hiển thị số liệu thống kê HM64](https://github.com/SrBananaMan/HarvestMoon64StatsDisplayMod) | `2d4b700434002a55611d4bf2e075c0f6301f9db8` | Đọc trường trò chơi, giao diện người dùng trạng thái phân trang, gọi lại làm mới |
| [HM64 nâng cao](https://github.com/HarvestMoon64Recomp/HarvestMoon64EnhancedMod) | `b13995f5662fa5068958f3361c5136a8e67e297f` | Tốc độ văn bản, tiếp tục âm nhạc, tối ưu hóa tải bản đồ |
| [Âm thanh tùy chỉnh HM64](https://github.com/harvestwhisperer/HarvestMoon64RecompAudioMod) | `2c5ad56aaff0239a09d76f464a10545cfb2ef3b2` | Tệp trình tự bên ngoài, bản đồ bản đồ và bản vá cuộc gọi âm thanh |
| [Cấu hình FOV HM64](https://github.com/SrBananaMan/HarvestMoon64FOVConfigMod) | `3ff901b4f916acf596f73deed58727d4edad80bd` | Chia tỷ lệ khung nhìn trực giao và bù kích thước giao diện người dùng |
| [Tốc độ đồng hồ HM64](https://github.com/SrBananaMan/HarvestMoon64ClockSpeedMod) | `73e8bd781807b5411d79f354162464b47cb6447f` | Phóng to bước đồng hồ trong trò chơi |

## 2. Chính xác thì họ đã làm gì?

### Harvest Moon 64: Kịch bản hỗn hợp và tiện ích mở rộng gốc

- **Nội suy có chiến lược nhận dạng và phân loại đối tượng. ** Sprite tương ứng với đối tượng liên khung thông qua ID nhóm ma trận; nội suy bị cấm đối với một số nền. Việc xây dựng bản đồ cố gắng giữ trật tự các ô ổn định; khi có sự thay đổi một lần trong cấu trúc liên kết hoặc khu vực bản đồ, phép nội suy đỉnh/bản đồ sẽ bị bỏ qua và phép nội suy chuyển đổi tổng thể được giữ lại. Các đỉnh có cùng số trong hai khung không thể tự động được coi là cùng một đối tượng. [Triển khai yêu tinh](https://github.com/HarvestMoon64Recomp/HarvestMoon64Recomp/blob/399a4f2b82a8b8dde4bb033e81f8a9b41d796a32/patches/sprites.c) · [Xây dựng bản đồ](https://github.com/HarvestMoon64Recomp/HarvestMoon64Recomp/blob/399a4f2b82a8b8dde4bb033e81f8a9b41d796a32/patches/culling.c) · [Chiến lược nội suy](https://github.com/HarvestMoon64Recomp/HarvestMoon64Recomp/blob/399a4f2b82a8b8dde4bb033e81f8a9b41d796a32/patches/patches.h)
- **Màn hình rộng yêu cầu mở rộng phạm vi gửi trò chơi gốc. ** Bản vá bản đồ hiện tại hủy bỏ việc loại bỏ khả năng hiển thị ô và mở rộng danh sách hiển thị bộ đệm đôi và dung lượng đỉnh; Ngoài ra còn có điểm đánh dấu mở rộng nền 2D. Ghi chú phát hành cho v1.2.0/1.2.1 cũng sửa lỗi riêng việc nội suy các đối tượng như phạm vi mưa và tuyết, ô nền hướng dẫn và NPC. [Bản ghi phát hành](https://github.com/HarvestMoon64Recomp/HarvestMoon64Recomp/releases) · [Thể loại màn hình rộng 2D](https://github.com/HarvestMoon64Recomp/HarvestMoon64Recomp/blob/399a4f2b82a8b8dde4bb033e81f8a9b41d796a32/patches/widescreen.c)
- **Cài đặt và Mod là một phần của sản phẩm. ** Chương trình chính được kết nối với RecompUI và đăng ký xuất giao diện người dùng, bắt đầu và dừng gói kết cấu cũng như cập nhật các lệnh gọi lại; vòng lặp trò chơi cung cấp thời gian thực hiện lệnh gọi lại giao diện người dùng. [Khởi động và đăng ký Mod](https://github.com/HarvestMoon64Recomp/HarvestMoon64Recomp/blob/399a4f2b82a8b8dde4bb033e81f8a9b41d796a32/src/main/main.cpp)

Mod độc lập của nó cung cấp các ví dụ phù hợp hơn để SRW64 học hỏi từ:

| Mod | Hành vi thực tế trong mã nguồn | Cảm hứng cho SRW64 |
| --- | --- | --- |
| [Hiển thị số liệu thống kê](https://github.com/SrBananaMan/HarvestMoon64StatsDisplayMod/blob/2d4b700434002a55611d4bf2e075c0f6301f9db8/src/stats_display.c) | Đọc sức mạnh thể chất, thời gian, kinh phí, mức độ ưa thích của nhân vật, tiến độ, v.v. từ trạng thái trò chơi; làm mới giao diện người dùng phân trang theo từng khoảng thời gian trong lệnh gọi lại trò chơi | HP/EN, sức mạnh, trạng thái hành động, địa hình và thanh bên vũ khí của đơn vị đã chọn |
| [Cấu hình FOV](https://github.com/SrBananaMan/HarvestMoon64FOVConfigMod/blob/3ff901b4f916acf596f73deed58727d4edad80bd/src/fov_config.c) | Sửa đổi ranh giới trực giao trái, phải, trên và dưới của máy ảnh, đồng thời bù cho các nút UI không thay đổi theo cảnh | Tách tỷ lệ bản đồ khỏi giao diện người dùng; Camera SRW64, phạm vi ô và mối quan hệ con trỏ cần được khôi phục trước tiên |
| [Cấu hình văn bản nâng cao](https://github.com/HarvestMoon64Recomp/HarvestMoon64EnhancedMod/blob/b13995f5662fa5068958f3361c5136a8e67e297f/src/message_box.c) | Thay đổi cài đặt giao diện văn bản, tốc độ cuộn và hiệu ứng âm thanh văn bản | Đối thoại tiêu chuẩn của chúng tôi đã có thể điều chỉnh tốc độ, phân trang và phát lại, nhưng nó chủ yếu thiếu cài đặt thống nhất và phạm vi giao diện nhiều hơn |
| [Tối ưu hóa bản đồ nâng cao](https://github.com/HarvestMoon64Recomp/HarvestMoon64EnhancedMod/blob/b13995f5662fa5068958f3361c5136a8e67e297f/src/map_loading.c) | Giảm việc tái thiết lặp đi lặp lại trong quá trình tải hàng loạt, tài nguyên được sử dụng lại vào bộ đệm và độ cao địa hình | Sử dụng các phép đo để tìm ra công việc lặp đi lặp lại cụ thể của việc tạm dừng tải, sau đó tối ưu hóa các chức năng tương ứng |
| [Tốc độ đồng hồ](https://github.com/SrBananaMan/HarvestMoon64ClockSpeedMod/blob/73e8bd781807b5411d79f354162464b47cb6447f/src/clock_speed.c) | Chỉ điều chỉnh hệ số bước của thời gian trong trò chơi | Tốc độ của các quy trình cụ thể có thể được kiểm soát riêng biệt; đây không phải là bằng chứng về tốc độ tối đa của trò chơi hoặc việc bỏ qua trận chiến |
| [Âm thanh tùy chỉnh](https://github.com/harvestwhisperer/HarvestMoon64RecompAudioMod/blob/2c5ad56aaff0239a09d76f464a10545cfb2ef3b2/src/custom_music.c) | Tải `.seq` từ máy chủ, ánh xạ bản đồ/âm mưu và đưa nó trở lại công cụ âm thanh gốc để phát lại; công cụ chuyển đổi MIDI thành seq | Vui lòng tham khảo lộ trình hỗ trợ thay thế nhạc bằng ID bài hát; phát lại trực tiếp OGG/FLAC yêu cầu thiết lập đường dẫn đồng bộ hóa và phát lại máy chủ riêng biệt |

### Kẻ lừa đảo: Màn hình rộng theo từng cảnh, nội suy và tua đi nhanh

Mã và tài liệu kỹ thuật cho thấy rằng dự án mở rộng phạm vi vẽ, cắt xén và tạo/biến mất của các họa tiết/gạch nền và một số đối tượng; giữ lại tỷ lệ 4:3 cho các đoạn cắt cảnh có khung vẽ cố định và khôi phục màn hình rộng sau khi vào cảnh hoạt động ổn định. [Phân tích kết xuất](https://github.com/ThiagoLira/trouble-makers-pc-recomp/blob/765b179c6f4bfbbb65dc7b371035798ca573202b/docs/README.md)

Tốc độ khung hình cao dựa trên nội suy hiển thị của khung hình trò chơi 60 Hz gốc. Các họa tiết thay đổi nhanh chóng như ngọn lửa đuôi tên lửa sẽ không khớp. Dự án sẽ tắt tính năng nội suy cho các cảnh và giao diện chọn cấp độ cụ thể, đồng thời khôi phục các lựa chọn của người dùng sau khi rời khỏi. v0.8.2 cũng tạo một phần mở rộng toàn cảnh riêng cho nền núi tuyết; Không thể ngoại suy mô tả "không kéo dài" của README về các cảnh cuộn thông thường cho tất cả các nền. [Chiến lược kịch bản](https://github.com/ThiagoLira/trouble-makers-pc-recomp/blob/765b179c6f4bfbbb65dc7b371035798ca573202b/src/game/presentation.h) · [v0.8.2](https://github.com/ThiagoLira/trouble-makers-pc-recomp/releases/tag/v0.8.2)

Việc nhấn giữ Tab chuyển tiếp nhanh gấp 3 lần được thực hiện thông qua hệ số nhân tốc độ thời gian chạy máy chủ, sửa đổi tốc độ VI/thời gian. Đó không phải là tính năng “chỉ tăng tốc độ chiến đấu, giữ nhạc bình thường”; tính liên tục về thời gian, hàng đợi âm thanh và ranh giới đầu vào vẫn cần được xác minh trước khi chuyển sang SRW64. [Nhập nhanh](https://github.com/ThiagoLira/trouble-makers-pc-recomp/blob/765b179c6f4bfbbb65dc7b371035798ca573202b/src/game/main.cpp) · [Bản vá thư viện thời gian chạy](https://github.com/ThiagoLira/trouble-makers-pc-recomp/blob/765b179c6f4bfbbb65dc7b371035798ca573202b/patches/N64ModernRuntime/0004-Add-ultramodern-set_speed_multiplier-for-host-fast-f.patch)

Dự án giải quyết rõ ràng hai loại vấn đề: các ký tự nhiều phần có thể bị mờ hoặc bị lệch trong quá trình nội suy và các đường nối dải sprite/địa hình không được tự động loại bỏ bằng tính năng khử răng cưa. Quá trình xác minh đầy đủ vẫn đang chờ xử lý. [Vấn đề đã biết](https://github.com/ThiagoLira/trouble-makers-pc-recomp/blob/765b179c6f4bfbbb65dc7b371035798ca573202b/KNOWN_ISSUES.md)

### Dr. Mario 64: Chuyển đổi kết xuất 2D một phần

Việc triển khai cụ thể của "viên nang được chuyển sang bản vẽ GPU" là thay thế chức năng vẽ ban đầu của CPU, tải tập bản đồ viên nang CI4, tải bảng màu cho nửa bên trái và bên phải, đồng thời ra lệnh hình chữ nhật kết cấu để tiếp tục vẽ bằng RT64. Nó chứng minh rằng các chức năng vẽ cục bộ có thể bị ghi đè và không ngụ ý rằng các vật liệu PBR hiện đại hoặc poly cao độc lập đã được sử dụng. [Bản vá viên nang](https://github.com/theboy181/drmario64_recomp_plus/blob/af91e3bf56b1ffc329ff4327fdc2380515463de7/patches/theboy181_workspace.c)

README cũng liệt kê nội suy tốc độ khung hình cao, bộ điều khiển bốn người chơi và hiệu ứng CRT, đồng thời lưu ý rằng có rất ít thử nghiệm tổng thể. Lần này, không có tệp nguồn nào khác được mẫu kế thừa sẽ được coi là các chức năng trò chơi đã hoàn thành. [Mô tả dự án](https://github.com/theboy181/drmario64_recomp_plus/blob/af91e3bf56b1ffc329ff4327fdc2380515463de7/README.md)

### Paper Mario ReCut: Thay thế tài liệu vào quá trình chỉnh sửa

Paper Atlas Tool hỗ trợ kéo và thả các PNG phân mảnh đã xuất vào tập bản đồ, lưu bố cục, gửi đến trình chỉnh sửa hình ảnh bên ngoài để sửa đổi, sau đó chuyển về thư mục thay thế theo bố cục ban đầu. Bối cảnh kết xuất trò chơi sẽ kiểm tra thời gian sửa đổi mới nhất của thư mục thay thế cứ sau 750 mili giây và tải lại sau khi thay đổi. [Công cụ Atlas](https://github.com/SMCGames/Paper-Mario-ReCut/blob/098be0a501eecd5bb894a47964061d05eeedc3a2/tools/PaperAtlasTool/README.md) · [Mã chỉnh sửa Atlas](https://github.com/SMCGames/Paper-Mario-ReCut/blob/098be0a501eecd5bb894a47964061d05eeedc3a2/tools/PaperAtlasTool/MainForm.cs) · [Tải thay thế](https://github.com/SMCGames/Paper-Mario-ReCut/blob/098be0a501eecd5bb894a47964061d05eeedc3a2/src/paper_rt64_context.cpp)

SRW64 đã có tính năng xây dựng câu đố bản đồ, cắt hình đại diện và trình xem tài nguyên, phù hợp để sắp xếp các tập lệnh hiện có vào quá trình chỉnh sửa "xem kịch bản sử dụng → xuất ảnh hoàn chỉnh → nhập sửa đổi → cắt tự động → so sánh trong trò chơi". Phiên bản đầu tiên của bản cập nhật nóng có thể bị giới hạn ở chế độ phát triển và gói chính thức sẽ tiếp tục giữ lại xác minh danh tính và các phiên bản rõ ràng.

## 3. So sánh SRW64: Làm được gì

Các mức độ khó sau đây là các đánh giá kỹ thuật dựa trên các lối vào đã biết và không phải là cam kết về thời gian xây dựng.

| Mục tiêu | Khái niệm cơ bản hiện tại | Công việc cần hoàn thành | Độ khó tương đối |
| --- | --- | --- | --- |
| Cài đặt nâng cao thống nhất | Có các công tắc thử nghiệm mô hình, hội thoại gốc và độ phân giải cao nhưng chúng ở các cấu hình dùng thử khác nhau | Hợp nhất các cấu hình tương thích, thêm bảng cài đặt, tùy chọn lưu giữ và ánh xạ bộ điều khiển thực thể; xác minh chung | Trung bình |
| Chỉnh sửa tài liệu và quản lý gói | Thay thế kết cấu RT64, tập lệnh xây dựng bản đồ/hình đại diện, trình xem 3D | Nhập và xuất toàn bộ hình ảnh, ánh xạ lát cắt, liên kết cảnh, chuyển đổi A/B, phụ thuộc gói và quản lý xung đột | Trung bình |
| Thanh bên thông tin chiến thuật | Có văn bản cốt lõi/Giao diện người dùng kim loại và móc chạy trò chơi | Khôi phục các đơn vị và trường hiện được chọn, xuất bản ảnh chụp nhanh nhất quán; kiểm tra với menu gốc | Trung bình đến Cao |
| Hiệu suất chiến đấu 2×/4× | Có sẵn khả năng đọc nhanh đối thoại và bỏ qua phần mở đầu và có thể chạy toàn bộ quá trình chiến đấu | Định vị các bước thực hiện, ranh giới chờ và giải quyết; trở về tốc độ bình thường khi chọn; kiểm tra HP/EN, thăng tiến ngẫu nhiên, phần thưởng, cốt truyện và âm thanh | Trung bình đến Cao |
| Chuyển động mượt mà của bản đồ, ống kính và một số họa tiết | RT64 đã được kết nối; chế độ làm mới ban đầu vẫn được sử dụng | Nhận dạng đối tượng ổn định, chuyển đổi khung hình phía trước và phía sau, vô hiệu hóa cảnh, chiến lược nội suy riêng biệt; mô hình gốc cũng phải sử dụng thời điểm hiển thị tương tự | Cao |
| Trường nhìn thực tế 16:9 | Hiện đang ở giữa 4:3 | Chiếu mở rộng bản đồ/trận chiến, trình xếp ô, cắt xén, nền và hiệu ứng tương ứng; con trỏ được căn chỉnh với lựa chọn | Cao |
| Nền chiến đấu độ nét cao và vật liệu mô hình hiện đại | Đã xác minh nguyên mẫu lưới, ánh sáng, tắc nghẽn GPU độc lập 5600 | Tìm tài nguyên và vòng đời của nền chiến đấu cụ thể; làm mô hình/vật liệu; xác minh lớp phủ sprite, máy ảnh và các hiệu ứng khác nhau | Cảnh đơn trung bình đến cao; hệ thống chung cao |
| Gói nhạc tùy chọn | Link âm thanh gốc có thể chạy được | Theo dõi ID, ngữ nghĩa chuyển đổi/vòng lặp/làm mờ; chọn trình tự để thay thế hoặc thêm máy chủ | Trung bình đến Cao |

**Nội suy có thể làm cho việc dịch chuyển, chia tỷ lệ và xoay toàn bộ bản đồ cơ thể trở nên mượt mà hơn; khi cơ thể chuyển từ bản đồ hành động này sang bản đồ hành động tiếp theo, tư thế cánh tay ở giữa sẽ không được tạo ra một cách ngẫu nhiên. ** Bổ sung các khung hành động, làm lại hoạt ảnh ghép nối hoặc thay đổi sang hoạt hình bộ xương 3D là những tài liệu và hệ thống hoạt hình bổ sung.

Đối với 3D gốc, các mã hiện có sẵn để tham khảo trong một số dự án chủ yếu là thích ứng RT64, bản vẽ hình chữ nhật/sprite và luồng tài nguyên; lần này, không tìm thấy giải pháp thay thế high-poly/PBR phổ quát nào có thể chuyển trực tiếp vào SRW64. Đường dẫn mô hình máy chủ của 5600 vẫn cần được mở rộng bằng ngữ nghĩa cảnh của riêng chúng tôi.

## 4. Xác minh việc triển khai hiện tại và trình tự đề xuất

- [`src/host/graphics.cpp`](../../src/host/graphics.cpp) Cài đặt rõ ràng hiện tại là `AspectRatio::Original`, `RefreshRate::Original`; Khả năng nội suy/màn hình rộng của RT64 không thể được coi là sự thích ứng của SRW64.
- [`play_native.py`](../../tools/recomp/run/play_native.py) Đã vượt qua `--profile` để thống nhất ngôn ngữ, nghệ thuật HD và mô hình bản địa; mức chấp nhận hiện tại nằm trong [Cấu trúc nội dung](../native/native-content-foundation.md).
- [Đối thoại thời gian thực](../native/native-dialogue-ui.md) Sắp chữ Unicode, phân trang, cỡ chữ, tốc độ xem lại và đọc đã được triển khai; vẫn còn những khoảng trống trong phạm vi bao phủ toàn bộ giao diện người dùng và các cách xử lý vật lý.
- [Bản địa 5600](../native/native-model-replacement.md) Có bằng chứng về lối chơi thực tế và sự tắc nghẽn có kiểm soát; hiện chỉ có Raster kim loại, không có khúc xạ trong suốt, trình chiếu động và triển khai phụ trợ chéo.
- Thông tin chiến thuật, nhịp điệu chiến đấu và các phần phụ thuộc trên màn ảnh rộng tuân theo [Kế hoạch triển khai tổng thể](native-enhancements-plan.md); báo cáo này bổ sung các trường hợp bên ngoài và không thay đổi mục kế hoạch khi đã hoàn thành.

Nên tiến hành dựa trên kết quả có thể chấp nhận được:

1. **Tích hợp các cải tiến và cài đặt hiện có. ** Phiên bản tương tự có thể bật và tắt giao diện người dùng Trung Quốc, gói HD và thay thế mô hình, duy trì cấu hình lưu rõ ràng và hoàn tất xác minh chung từ cấp độ mở đến cấp độ đầu tiên cũng như lưu và đọc tệp.
2. ** Cung cấp các mẫu nâng cao mang tính thực tế. ** Trước tiên, hãy tạo ảnh chụp nhanh trạng thái của đơn vị đã chọn và tạo thanh bên thông tin bên cạnh khu vực trò chơi 4:3; tốc độ chiến đấu được xác minh là một chức năng độc lập. Quá trình chỉnh sửa tài liệu có thể được cải thiện dần dần mà không thay đổi lối chơi.
3. **Mẫu cải tiến màn hình phân phối. **Chọn nền chiến đấu thực tế để tạo ra các mô hình/vật liệu hiện đại; Trước tiên hãy thử nội suy cục bộ cho bản đồ hoặc ống kính, sau đó mở rộng chúng theo danh mục. Màn hình rộng thực sự được chấp nhận theo cảnh và cốt truyện có bố cục cố định vẫn giữ nguyên chiến lược trình bày tương ứng.

Nội dung mới này chỉ là một hồ sơ nghiên cứu; không có dự án nào khác được bắt đầu, các triển khai bên ngoài chưa được sao chép vào SRW64 và các thử nghiệm hoặc kho lưu trữ hiện có không bị thay đổi.