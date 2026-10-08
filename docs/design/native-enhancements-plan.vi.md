> **Ngôn ngữ / Language:** [Tiếng Việt](native-enhancements-plan.vi.md) · [English](native-enhancements-plan.en.md) · [中文](native-enhancements-plan.md)

# Kế hoạch triển khai nâng cao bản địa SRW64

Cập nhật kế hoạch 12-09-2026: Các ưu tiên tiếp theo và ranh giới ra mắt phải tuân theo [Lộ trình sản phẩm MOD](mod-roadmap.md).
Lưu trữ nút an toàn, nhiều khe cắm và sao lưu hiện được bao gồm trong bản phát hành đầu tiên; mô tả về "năm hướng" và quản lý lưu trữ không duy nhất dưới đây nằm trong phạm vi thời gian đó.
Bài viết này giữ lại những lựa chọn kỹ thuật ban đầu và nền tảng thử nghiệm và không thể sử dụng để đánh giá liệu các nhiệm vụ trong lộ trình mới đã được hoàn thành hay chưa.
Phạm vi MOD hiện tại chỉ là các mô-đun chức năng tích hợp được dự án duy trì; các ý tưởng sau đây về quyền truy cập gói bên ngoài tạm thời bị đình chỉ và sẽ không được sử dụng làm phần phụ thuộc trong lần chạy đầu tiên.

Ngày: 2026-09-09. T0 đã hoàn thành nguyên mẫu kết xuất văn bản của hệ thống cảnh cố định; sau đó, hội thoại tiêu chuẩn thời gian thực, cỡ chữ và phân trang, đánh giá, tốc độ cốt truyện và tỷ lệ cửa sổ đã được tích hợp. Để biết bằng chứng hoạt động và phạm vi triển khai mới nhất, hãy xem [Giao diện người dùng Apple thời gian thực](../native/native-dialogue-ui.md). Bài viết này giữ nguyên kế hoạch thực hiện tổng thể; Toàn bộ quá trình, các nhánh và sự kết hợp của màn hình thực tế vẫn cần được xác minh từng mục một.

Người dùng đã chọn năm hướng: Hệ thống văn bản tiếng Trung, điều khiển nhịp điệu chiến đấu, bảng thông tin chiến thuật, màn hình rộng và cải tiến nghệ thuật, Mod liên kết và nội dung. Các kế hoạch chi tiết và ưu tiên sẽ được đưa ra trong vòng này; kết xuất văn bản sẽ ưu tiên cho công nghệ văn bản hệ thống macOS. Tính chính xác của các bản lưu trữ và lần đọc hiện có sẽ tiếp tục là điều kiện chấp nhận ở mỗi giai đoạn và các chức năng của sản phẩm quản lý kho lưu trữ sẽ không được đưa vào riêng trong năm phạm vi.

## 1. Trình tự thực hiện và ranh giới phân phối

| Trình tự | Giai đoạn | Sản phẩm bàn giao | Sự phụ thuộc và độ khó tương đối |
| --- | --- | --- | --- |
| 1 | T0: Hệ thống xác minh chất lượng văn bản | Văn bản lõi / Đồ họa lõi tạo văn bản và tổng hợp nó trong hình ảnh cuối cùng của cảnh RT64 thực; xác minh kích thước phông chữ và mật độ pixel | Trung bình; đầu tiên chứng minh rằng quyền truy cập kết xuất và màu sắc là chính xác |
| 2 | T1: Nhận dạng hội thoại theo thời gian thực | Ghi nhật ký thời gian chạy với ID văn bản, loa, tiến trình hiển thị và kiểm soát sự kiện | Trung bình đến cao; yêu cầu công nhận trình thông dịch và trạng thái cảnh |
| 3 | T2: Hệ thống hội thoại hoàn chỉnh | Tập đầu tiên của nữ chính có thể điều chỉnh cỡ chữ, ngắt dòng/phân trang tự động, dịch hoàn chỉnh, phát lại đoạn hội thoại | Cao; phụ thuộc vào T0/T1, phạm vi được giới hạn ở đối thoại trước |
| 4 | B1: Nhịp điệu chiến đấu | Chỉ định khả năng tăng tốc của hiệu suất chiến đấu; sau đó mở rộng hoạt động di chuyển của địch và chờ đợi | Trung bình đến cao; đầu tiên xác định ranh giới giữa hiệu suất và logic |
| 5 | U1: Bảng thông tin và W1: Thùng chứa màn hình rộng | 4:3 Hiển thị thông tin đơn vị/vũ khí hiện tại bên cạnh khu vực trò chơi, chia sẻ phần phụ trợ văn bản gốc | Trung bình đến cao; hoàn thành việc ánh xạ trường và trạng thái lựa chọn trước |
| 6 | B2/W2 | Giải quyết trận chiến nhanh chóng; mở rộng trường xem bản đồ thực tế, màn hình rộng theo từng cảnh và cải thiện nghệ thuật | Cao; tiến lên sau khi xác minh tình trạng chiến đấu và phạm vi vẽ tương ứng |
| 7 | M1/M2 | Gói Mod dữ liệu; Dự án đặc biệt tương thích Link Battler | Gói dữ liệu từ trung bình đến cao, khả năng tương thích giao thức cao; khảo sát liên kết có thể được thực hiện trước, nhưng có những ngưỡng bổ sung để thực hiện |

Hệ thống văn bản được phân phối đầu tiên; tăng tốc chiến đấu theo sau; bảng thông tin và thùng chứa màn hình rộng được thiết kế cùng nhau. Hoàn thành việc giải quyết nhanh chóng, trường xem bản đồ thực tế mở rộng và liên kết được để lại cho đến khi ranh giới thời gian chạy liên quan được làm rõ. Trên đây là trình tự công việc và độ khó tương đối. Nó chưa được hiệu chỉnh bằng nguyên mẫu từ đầu đến cuối và không thể chuyển đổi thành giai đoạn xây dựng lịch đáng tin cậy.

“Bản dịch hoàn chỉnh” trong hệ thống văn bản được chấp nhận có nghĩa là bản dịch được cung cấp sẽ không bị cắt bớt hoặc buộc phải rút ngắn do dung lượng của khung gốc. Việc dịch, đánh giá và đưa ra lộ trình của toàn bộ trò chơi là công việc nội dung và cần được thanh toán riêng; 153 bản dự thảo thử nghiệm hiện tại của Trung Quốc không có nghĩa là chúng đã được hoàn thiện đầy đủ. Để biết kích thước văn bản, hãy xem [Thư mục dữ liệu gốc](../data/original-data-catalog.md).

## 2. Nền tảng kỹ thuật hiện tại và khoảng cách thực tế

| Các mục đã kiểm tra | Những gì có thể được tái sử dụng | Những gì vẫn cần phải hoàn thành |
| --- | --- | --- |
| [`catalog.py`](../../src/srw64_native/catalog.py), [`text.py`](../../src/srw64_rom/text.py) | Bảng/ID văn bản ổn định, lớp phủ dịch, bộ điều khiển gốc | Mô hình đoạn thời gian chạy Unicode, ánh xạ vị trí điều khiển ban đầu sang đoạn dịch |
| `resident_func_8008C510` trong số [`host.cpp`](../../src/host/host.cpp) | Chặn đọc mô tả văn bản; có một bản ghi ảo tên mặc định của Trung Quốc | Liệu bài đọc hiện tại có thuộc về đoạn hội thoại, người nói, nguyên văn/tạm dừng/xác nhận được hiển thị hay không |
| `resident_func_8007F704` của cùng một tệp | Đọc ROM, xác minh danh tính lớp phủ và tải thông báo | Xóa trạng thái cũ khi chuyển cảnh văn bản để ngăn chặn việc xác định sai lớp phủ địa chỉ tương tự |
| `dialogue_layout.hpp` (đã xóa vào ngày 24-09-2026) | Bản vẽ glyph một phần của đoạn hội thoại mở đầu và trang tên đã được công nhận | Hiện tại chỉ có vị trí được thay đổi; không thể tự động ngắt dòng và nó không phải là trình thông dịch văn bản hoàn chỉnh |
| [`graphics.cpp`](../../src/host/graphics.cpp) | Móc kéo khung cuối cùng RT64, Kim loại, đọc lại GPU sau khi hoàn thành, thay thế kết cấu | Tổng hợp văn bản có độ phân giải cuối cùng, xử lý dpi thống nhất, loại bỏ glyphs gốc một cách đáng tin cậy |
| [`audio_timing.hpp`](../../src/host/audio_timing.hpp) | Đã có phản hồi về hàng đợi âm thanh và giới hạn thời lượng | Hiện đang giả sử 60 VI; mọi giải pháp thay đổi tốc độ mô phỏng cần được xác nhận lại |
| `auto_counter.py` (đã bị xóa trong 5b997c7 ngày 2026-10-01) | Đầu dò tự động xác nhận menu truy cập hiện có bị giới hạn | Nó sử dụng mẫu ảnh chụp màn hình đã được đánh giá và không cung cấp mô hình dữ liệu đơn vị hoặc máy trạng thái chiến đấu |
| `host.cpp::get_device` và `ultramodern/input.hpp` của thư viện thời gian chạy cố định | Đầu vào bộ điều khiển hiện tại | Máy chủ trả về `Pak::None`; `TransferPak` của thư viện thời gian chạy vẫn là chú thích và cần có sự điều chỉnh đặc biệt |

Phạm vi bằng chứng cho quá trình lưu thông quan tập 1 hiện tại của JP, cấu hình ngôn ngữ bản địa và độ phân giải cao cũng như thử nghiệm phông chữ một khung hình được hiển thị trong [tiến trình biên dịch lại](recomp-progress.md), [cấu hình nội dung gốc](../native/native-content-foundation.md) và thử nghiệm phông chữ (đã xóa cuộc thăm dò ngày 24-09-2026). Cả ba không thể thay thế nhau.

## 3. Hệ thống văn bản tiếng Trung: sử dụng kết xuất văn bản gốc của OS

> Không còn được sử dụng từ năm 2026-09: Văn bản trò chơi sẽ được vẽ bằng công cụ FreeType+HarfBuzz+ICU đa nền tảng và đóng gói HarmonyOS Sans, xem [đối thoại trò chơi và văn bản đa nền tảng tiếng Trung, tiếng Nhật và tiếng Anh](../native/portable-text.md). Phần này giữ nguyên kế hoạch hiện tại và lý do.

### 3.1 Ra quyết định và hiệu ứng màn hình

ưu tiên macOS **Sắp chữ văn bản lõi + Rasterization đồ họa lõi + Bố cục màn hình cuối cùng bằng kim loại**. Điều này thực sự gọi công nghệ văn bản hệ thống để xử lý các số liệu phông chữ, lựa chọn glyph, bố cục và bản vẽ. Bạn có thể tìm thấy lời giải thích của Apple về mối quan hệ giữa hai yếu tố này và phông chữ dự phòng trong [Tổng quan về văn bản cốt lõi](https://developer.apple.com/library/archive/documentation/StringsTextFonts/Conceptual/CoreText_Programming/Overview/Overview.html).

Nguồn phông chữ độc lập với trình kết xuất: bạn có thể chọn phông chữ tiếng Trung của hệ thống hoặc sử dụng HarmonyOS Sans SC thông qua cùng một chương trình phụ trợ kết xuất hệ thống. Phiên bản đầu tiên cung cấp hai ứng cử viên là "Hệ thống tiếng Trung" và phông chữ hiện tại, được so sánh theo cùng một văn bản, kích thước, độ dày phông chữ và nền để xác định giá trị mặc định. Tuân theo việc lựa chọn phông chữ của hệ thống bằng API nhận biết ngôn ngữ, viết bằng chứng về phông chữ được phân giải thực tế và phông chữ dự phòng mà không giả sử một tên phông chữ nhất định tồn tại trên tất cả các máy.

Văn bản được tạo theo mật độ pixel của hình vẽ cuối cùng và kích thước phông chữ được thể hiện theo đơn vị logic giao diện; độ phóng đại kết xuất bên trong của trò chơi tách biệt với kích thước văn bản. Chuyển tiếp/rasterization khi cửa sổ được thay đổi kích thước hoặc di chuyển trên các màn hình. Chất lượng văn bản trên máy tính để bàn được nhắm mục tiêu; phiên bản hệ thống, phiên bản phông chữ, cài đặt khử răng cưa và tổng hợp ảnh hưởng đến pixel và không được đảm bảo giống hệt từng pixel với bất kỳ ứng dụng macOS nào.

Core Text cung cấp tính năng sắp chữ trong hộp và ngắt dòng tự động; Dự án này vẫn triển khai tính năng phân trang, hiển thị nguyên văn, lịch sử và tập lệnh của trò chơi. Các lệnh cấm chấm câu tiếng Trung, dấu chấm lửng liên tiếp, bố cục hỗn hợp và các ký hiệu đặc biệt phải được xác minh thông qua các mẫu và việc gọi API sắp chữ không thể được coi là chấp nhận. Tham khảo [Thao tác bố cục văn bản của Apple](https://developer.apple.com/library/archive/documentation/StringsTextFonts/Conceptual/CoreText_Programming/LayoutOperations/LayoutOperations.html).

### 3.2 Cấu trúc đề xuất

```text
原游戏对白解释器 / 场景与文本 ID
              ↓
DialogueSnapshot：完整片段、说话者、控制边界、显示进度、事件序号
              ↓
翻译覆盖层 + 动态姓名 + 专用符号
              ↓
Core Text：字形选择、度量、行布局、分页所需范围
              ↓
Core Graphics：按最终像素密度绘制可见字形
              ↓
Metal：游戏画面完成后合成 → GPU 完成后截图
              ↓
已显示片段进入对话历史
```

Logic chia sẻ có trong C++; chương trình phụ trợ macOS được đưa vào một tệp `.mm` riêng biệt và được xây dựng dựa trên CoreText, CoreGraphics và các khung hệ thống bắt buộc. Giao diện được xác định xung quanh đầu vào bố cục, phạm vi cụm glyph và đầu ra pixel có thể tổng hợp mà không truyền bá các loại macOS tới trình thông dịch trò chơi. Các phần phụ trợ nền tảng khác được dành riêng cho các điểm chuyển tiếp theo và vòng này không hứa hẹn các pixel phông chữ nhất quán trên các nền tảng.

Bố cục ban đầu được lưu vào bộ nhớ đệm theo phân đoạn hội thoại và chỉ hiển thị lại khi văn bản, phông chữ, độ dày, chiều rộng hoặc độ nhạy sáng thay đổi. Hiển thị từng từ sử dụng các vị trí glyph được sắp xếp và cập nhật bản vẽ theo phạm vi hiển thị; trước tiên hãy đo thời gian tải lên kết cấu và rasterization của CPU, sau đó quyết định xem có nên giới thiệu tập bản đồ glyph phức tạp hơn hay không.

### 3.3 T0: Đầu tiên hãy chứng minh rằng kết xuất của hệ thống có thể vào màn hình trò chơi một cách chính xác

1. Sử dụng ảnh chụp nhanh hiện trường của các danh tính được ghi lại, cùng với các mẫu chữ cái và số tiếng Trung, tiếng Nhật, tiếng Latinh và đóng hộp; bao gồm dấu ngoặc kép, dấu ngoặc, dấu chấm lửng và tên dài hơn.
2. Sử dụng Văn bản lõi / Đồ họa lõi để tạo văn bản nền trong suốt; chỉ định rõ ràng không gian màu, định dạng alpha và texel được nhân trước.
3. Draw hook tổng hợp văn bản ở khung cuối cùng. Đã sửa lỗi `rt64_present_queue.cpp` cho RT64 đã được kiểm tra: hook nằm sau `viRenderer->render` nhưng trước khi gửi kết xuất; ảnh chụp màn hình GPU hiện có cũng sử dụng mục này. Việc thêm các tác phẩm mới nên được thực hiện trước khi chụp ảnh màn hình.
4. Trước tiên, hãy sử dụng một khu vực độc lập để so sánh chất lượng của các nét vẽ, sau đó chỉ thay thế các nét vẽ ban đầu đã được chỉ định rõ ràng. Đường khung, hình nền, hình đại diện, con trỏ và các biểu tượng đặc biệt phải được giữ lại; kết cấu tương tự nói chung không thể được ẩn đi.
5. Xác minh ba kích thước phông chữ, hộp văn bản hẹp/rộng, chia tỷ lệ cửa sổ và mật độ điểm ảnh 1×/2× có sẵn; ghi lại kích thước logic của cửa sổ và kích thước có thể vẽ thực tế. Các kết hợp màn hình thực không được kết nối sẽ được dành riêng để thử nghiệm.

Điều kiện vượt qua T0: không có văn bản kép, đổ màu, cạnh tối, cắt xén hoặc làm mờ tỷ lệ thêm; hình ảnh GPU cuối cùng chứa văn bản mới. Đầu ra bao gồm các lệnh có thể tái tạo, nhận dạng cảnh/phông chữ, tham số bố cục và khung GPU. Giai đoạn này chỉ chứng minh kết xuất và không khẳng định hệ thống đối thoại thời gian thực đã hoàn thiện.

### 3.4 T1: Ngữ nghĩa hội thoại và nhận dạng sự kiện

Mục đọc văn bản chỉ được sử dụng để liên kết ID và dữ liệu và mỗi lần đọc ROM không thể được ghi lại dưới dạng một đoạn hội thoại lịch sử. Cần xác định vị trí chức năng hiển thị thực tế và trình thông dịch văn bản, đồng thời xác định người nói, đoạn hiện tại, vị trí hiển thị, chờ xác nhận và trạng thái kết thúc của từng hộp thoại trong hai hộp thoại.

Chuỗi trò chơi đưa ra các ảnh chụp nhanh bất biến vào những thời điểm cụ thể; luồng kết xuất sử dụng ảnh chụp nhanh được liên kết với tác vụ hiển thị đó. Sự kiện này mang số thứ tự đơn điệu và việc tạo cảnh để ngăn việc vẽ lặp lại tạo ra các nhật ký trùng lặp hoặc văn bản của cảnh trước đó xuất hiện sau khi chuyển đổi lớp phủ. Có sự kiểm tra ranh giới giữa các luồng và luồng kết xuất bị cấm sửa đổi con trỏ văn bản của trò chơi theo ý muốn.

Đầu tiên, giữ nguyên màn hình gốc và thu thập các đường dẫn như xác nhận tên siêu loại nữ, mở hội thoại khung đôi, đối thoại bản đồ và đối thoại sau chiến tranh. Sử dụng hình ảnh thực tế và các sự kiện kiểm soát để chứng minh rằng cùng một văn bản có thể xuất hiện nhiều lần và mỗi lần xuất hiện chỉ tạo ra một tập hợp các sự kiện hiển thị tương ứng.

### 3.5 T2: Cỡ chữ, dịch hoàn chỉnh, phân trang và lịch sử

- **Văn bản Unicode**: Tải các bản dịch bên ngoài theo ID ổn định hiện có; tên động giữ lại ngữ nghĩa chèn. Các ký hiệu đặc biệt chưa được nhận dạng nhưng vẫn giữ được khả năng giữ chỗ/hình ảnh gốc rõ ràng và không bị xóa một cách âm thầm. Nội dung dịch có thể được nâng cao từng đoạn và không bị giới hạn bởi dung lượng phông chữ ROM.
- **Cờ kiểm soát**: Giữ trình tự ban đầu của `END=FFFF`, `BR=FFFE`, `STOP=FFFD` và các ký tự đặc biệt. Lượt đầu tiên giữ nguyên gói từ rõ ràng; gói từ tự động chỉ thêm các điểm dừng của lớp trình bày và không viết lại luồng điều khiển ROM. Ngữ nghĩa chờ/đẩy thực tế của `STOP` sẽ được xác nhận bằng bằng chứng thời gian chạy T1.
- **Bản dịch dài**: Định dạng lại văn bản trong đoạn điều khiển tương ứng và thêm trang đọc nếu cần. Trang mới được thêm trước tiên sẽ sử dụng đầu vào xác nhận ở lớp máy chủ, sau đó gửi xác nhận tương ứng với đoạn của trò chơi sau khi trang được đọc; sự kiện tập lệnh tiếp theo không thể được sử dụng trước. Điểm chặn cụ thể được xác định bởi T1.
- **Hiển thị nguyên văn**: Độ dài của đoạn dịch không phụ thuộc vào văn bản gốc; đặt tốc độ hiển thị các từ theo cụm glyph và làm rõ ánh xạ phạm vi UTF-16, cụm glyph Unicode và mã thông báo trò chơi. Hoàn thiện bố cục từng trang trước khi hiện nội dung để tránh bỏ sót cả dòng mỗi khi thêm một từ.
- **Xem lại cuộc hội thoại**: Lưu lại nội dung đã trình bày, tên và người nói lúc đó, số thứ tự; sẽ không có bản ghi mới nào được thêm vào cho các khung lặp lại và văn bản tiếp theo không được tiết lộ sẽ không được hiển thị trước. Phiên bản đầu tiên lưu lịch sử giới hạn của phiên hiện tại, tải tệp và tạo phân đoạn mới cho trò chơi mới. Phục hồi lịch sử nhiều quá trình được thiết kế riêng cho liên kết lưu trữ.
- **Nhập và Tạm dừng**: Cửa sổ lịch sử sử dụng thao tác cuộn của chính nó, xác nhận và trả về dữ liệu nhập. Chỉ mở tại các điểm chờ đối thoại đã được xác minh; không có hành động nào được gửi đến trò chơi trong khi chơi lại. Nếu có tiến trình hội thoại tự động, cơ chế tạm dừng cảnh an toàn phải được thiết lập trước khi có thể mở đường dẫn.
- **Kích thước và màu sắc**: Kích thước phông chữ/khoảng cách dòng/lề có thể điều chỉnh được. Đồng bộ hóa với màu văn bản gốc, độ mờ và khả năng hiển thị hộp thoại của trò chơi; những hiệu ứng này phải được xử lý riêng biệt trong quá trình bố cục ảnh cuối cùng để tránh văn bản nổi giữa các cảnh.

Phạm vi phân phối đầu tiên của T2: lời thoại cốt truyện liên quan đến tập đầu tiên của Siêu phẩm nữ; trang tên, menu chiến thuật, menu vũ khí và văn bản nướng trong ảnh lần lượt được đăng ký trạng thái phủ sóng. Bản dịch hoàn chỉnh của tập đầu tiên được kiểm tra bởi những người đánh giá chi nhánh khi đưa tin. Phạm vi bảo hiểm đầy đủ không thể được khai báo chỉ dựa trên phạm vi ID liên tục.

Phạm vi chấp nhận: bản dịch dài, chèn tên, hộp thoại đôi, tạm dừng rõ ràng, trang chéo, chuyển đổi lịch sử, dự phòng từ bị thiếu, chuyển đổi kích thước phông chữ, thay đổi cửa sổ/DPI, chuyển cảnh và đọc tệp. Thực hiện trò chơi mới để lưu sau trận chiến và tiếp tục tải trong quy trình mới; so sánh trạng thái trò chơi và chuỗi sự kiện tương ứng. Kiểm tra bố cục tĩnh, phát lại từng khung hình và quá trình chấp nhận trò chơi trong thời gian thực được ghi lại riêng biệt.

## 4. Kiểm soát nhịp chiến đấu

**Khảo sát B0**: Xác định vị trí các tùy chọn tấn công/phản công, tính toán thiệt hại, tiêu thụ tài nguyên, hoạt ảnh, tiêu diệt, kinh nghiệm/tiền và trả lại ranh giới bản đồ thông qua các cuộc giao tranh thực tế; ghi lại trạng thái trò chơi ở từng giai đoạn. Người ta vẫn chưa chứng minh được rằng có một lối vào bỏ qua ban đầu có thể được tái sử dụng trực tiếp.

**B1 Phiên bản đầu tiên**: Cung cấp khả năng tăng tốc tạm thời bình thường/tăng tốc và nhấn và giữ để đạt được lộ trình hiệu suất đã được xác minh. Ưu tiên xem xét thời gian chờ chiếu và bước hoạt ảnh; nếu sử dụng khả năng tăng tốc đồng hồ analog thì VI, phản hồi âm thanh, mẫu đầu vào và thời gian luồng phải được xử lý đồng thời chứ không chỉ thay đổi `get_display_framerate()`. Chiến lược thay đổi tốc độ được sử dụng cho nhạc nền và hiệu ứng âm thanh được làm rõ trong nguyên mẫu và được thử giọng thủ công.

Sau đó, nó bao gồm chuyển động của kẻ thù, nhắc nhở lặp đi lặp lại và chờ giải quyết; nhịp điệu tương tác được khôi phục khi cần lựa chọn người chơi hoặc cốt truyện được kích hoạt. Sử dụng phán đoán trạng thái cảnh, tập lệnh đầu vào VI tuyệt đối và mẫu ảnh chụp màn hình không thể trở thành máy trạng thái sản phẩm.

**B2 Giải quyết nhanh**: Sau khi chứng minh rằng việc thực thi quy tắc và hiệu suất có thể tách biệt, hãy thêm "hoạt ảnh bình thường/hiệu suất nhanh/kết quả ngắn gọn". Mỗi chế độ phải làm cho mức tiêu thụ tài nguyên, HP, tiêu diệt, phần thưởng, kích hoạt và thăng tiến số ngẫu nhiên phù hợp với chế độ bình thường trong cùng điều kiện. Bạn không thể trực tiếp đặt biến kết quả để giả vờ rằng trận chiến đã hoàn thành.

Việc xác minh bắt đầu từ cùng một kho lưu trữ và trạng thái có thể kiểm soát được; các trạng thái ngẫu nhiên có thể được so sánh chính xác khi cố định, nếu không thì phạm vi so sánh sẽ rõ ràng. Bao gồm các lượt truy cập, trượt, phản công, hạ gục, nâng cấp, kích hoạt âm mưu và quay lại bản đồ, thời gian xử lý và hàng đợi âm thanh được đo tương ứng.

## 5. Bảng thông tin chiến thuật và màn hình rộng

**Khảo sát dữ liệu U0**: Thiết lập bản đồ của đơn vị, trình điều khiển, HP/EN, năng lượng, trạng thái hành động, địa hình, vũ khí và trường đạn/tiêu thụ hiện được chọn. Nguồn của mỗi bản ghi là lớp phủ/địa chỉ hoặc chức năng, loại, điều kiện hợp lệ và so sánh đo lường thực tế. Đầu tiên, chỉ hiển thị những thông tin có thể xác minh được bằng menu gốc.

**U1 + W1 phiên bản đầu tiên**: Thiết kế cửa sổ vào khu vực trò chơi 4:3 gốc cộng với thanh bên. Trạng thái đơn vị được hiển thị khi một đơn vị được chọn; cả hai bên và vũ khí đã chọn sẽ được hiển thị sau khi bước vào lựa chọn tấn công. Thanh bên sử dụng khả năng văn bản của T0/T2 và kích thước phông chữ được liên kết với chiều rộng cửa sổ; nó có thể được rút lại khi không đủ không gian. Phiên bản đầu tiên ở chế độ chỉ đọc và không thay đổi các đơn vị đã chọn hoặc quyết định chiến đấu.

Bước này cung cấp vùng chứa giao diện màn hình rộng và không khẳng định rằng chế độ xem bản đồ đã được mở rộng. Cập nhật bảng điều khiển sử dụng ảnh chụp nhanh an toàn để kiểm tra trạng thái đã chọn thực tế của trò chơi; các trường không xác định hoặc hiện không hợp lệ không được hiển thị rõ ràng và không thể kế thừa từ bộ đệm cảnh cũ.

**Bản đồ thực tế/Màn hình rộng trận chiến W2**: Khôi phục camera bản đồ, phạm vi gửi ô, loại bỏ khả năng hiển thị, tọa độ con trỏ và cuộn cạnh tương ứng; trận chiến cũng kiểm tra mức độ bao phủ của hậu cảnh, họa tiết/hiệu ứng đặc biệt, ống kính và cắt xén. Trước tiên, hãy xác minh tỷ lệ 16:9, sau đó mở rộng tỷ lệ mà không kéo dài nội dung 4:3 ban đầu.

**Nghệ thuật**: Chuẩn bị hình đại diện, bản đồ, giao diện và danh sách tài liệu chiến đấu dựa trên các cảnh hoàn chỉnh ngoại trừ hình tượng; thống nhất phong cách, đường viền, độ trong suốt, màu sắc và khôi phục hình ảnh gốc. Gói thay thế RT64 ghi lại nhận dạng kết cấu ban đầu và cảnh phủ sóng. Các tài liệu có sự mơ hồ về hàm băm nguồn đã biết cần có giải pháp ngữ cảnh trước khi thay thế. Hình ảnh AI hiện có có thể được sử dụng làm ứng cử viên và việc tạo ra vật liệu mới là tác phẩm nghệ thuật tiếp theo.

## 6. Mod liên kết và nội dung

**M1 Data Mod xuất hiện trước**: Đầu tiên hỗ trợ các gói dịch và kết cấu ở các định dạng đã hiểu và bản kê khai ghi lại các phiên bản gói, ROM hiện hành, phần phụ thuộc, xung đột và băm dữ liệu. Chỉ khi đó các giá trị đơn vị/vũ khí của cấu trúc đã được xác minh mới được mở; việc thay đổi phạm vi và giá trị mặc định có thể được xem lại và việc đóng Mod có thể khôi phục cấu hình cơ bản. Việc khởi động lại để có hiệu lực có thể được sử dụng làm ranh giới của phiên bản đầu tiên và mọi hoạt động tải lại nóng hiện không được thiết kế.

Các bản vá chức năng gốc và gói dữ liệu được quản lý riêng biệt. Bản vá chức năng phải liên kết phiên bản, nhận dạng lớp phủ và ký hiệu; phương pháp đầu ra bản vá của N64Recomp có thể được đánh giá và phần thân chính tiếp tục được tạo theo nhóm. Mỗi đối tượng của thư viện tĩnh hiện tại chứa nhiều hàm. Độ chi tiết của liên kết và các định nghĩa lặp lại cần phải được xác minh trước khi ghi đè các ký hiệu có cùng tên. Bạn không thể chỉ thêm `single_file_output=true` và cho rằng cơ chế ghi đè đã được thiết lập.

**M2 Link Battler Special** được chia làm 2 hướng sản phẩm rõ ràng:

1. **Tương thích với quy trình liên kết ban đầu**: Điều tra các lệnh gọi và giao thức của hộp mực Pak/GB được trò chơi sử dụng, xác định các định dạng dữ liệu, xác minh và hành vi đọc và ghi. Thư viện thời gian chạy cố định chưa kích hoạt triển khai Transfer Pak và cần bổ sung giao diện và lớp tương thích. Đầu vào đúng, không có thiết bị, đầu vào không chính xác và các liên kết trùng lặp trước tiên được kiểm tra đối với các bản sao dữ liệu độc lập; nếu cần có tham chiếu kho lưu trữ/ROM GB thực thì nguồn và tính khả dụng của nó sẽ được sử dụng làm phần phụ thuộc triển khai.
2. **Mod mở nội dung tùy chọn**: Nêu rõ nội dung và điều kiện để mở trực tiếp, trước tiên hãy xác minh thẻ nội dung, tài nguyên và các phụ thuộc của sự kiện tiếp theo, sau đó thực hiện các quy tắc có thể đóng. Chế độ này được xác định độc lập và không được sử dụng làm bằng chứng về tính tương thích của giao thức Transfer Pak.

Kịch bản cấp độ, viết lại tuyến đường, ngẫu nhiên hóa và các đơn vị mới yêu cầu định dạng và mô hình sự kiện hoàn chỉnh hơn, được đặt phía sau lớp dữ liệu M1 và mở rộng phạm vi cảnh.

## 7. Vòng nhiệm vụ phát triển và xác minh đầu tiên

Vòng phát triển đầu tiên chỉ đảm nhận việc xác minh tính khả thi của T0/T1. Sau khi bàn giao, khối lượng công việc của T2 sẽ được sàng lọc dựa trên các bằng chứng:

1. Thêm công cụ kiểm tra và phụ trợ văn bản macOS độc lập để xuất ra ba cỡ chữ, câu dài và so sánh bố cục hỗn hợp của phông chữ hệ thống/phông chữ hiện tại.
2. Truy cập phần tổng hợp khung hình cuối cùng và điều chỉnh thứ tự của ảnh chụp màn hình để hoàn thành kiểm tra màu sắc, Alpha, DPI và thay đổi cửa sổ.
3. Thu thập ID văn bản, diễn giả và tiến trình điều khiển cho cảnh đối thoại mở đầu đã được xác minh để tạo thành mô hình và bằng chứng sự kiện rõ ràng.
4. Làm rõ phạm vi ngăn chặn glyph ban đầu và giao diện nâng cấp hội thoại; chỉ sau khi hai mục này được thiết lập, việc thay thế và phân trang theo thời gian thực của T2 mới bắt đầu.

Bạn nên đặt mô-đun mới trong `src/host/text/`, với phần phụ trợ nền tảng, bố cục/phân trang, điều chỉnh sự kiện trò chơi và mô hình lịch sử làm ranh giới độc lập; tên tệp cụ thể sẽ được xác định trong quá trình phát triển. Cấu hình rơi vào `config/recomp/`, dữ liệu, phông chữ, hình ảnh, bản ghi phiên có nguồn gốc từ ROM thực vẫn còn trong `build/`.

Quá trình gửi được phân tách bằng "Phần cuối văn bản → Nhận dạng cảnh → Phân trang và nhập liệu trong thời gian thực → Lịch sử → Chấp nhận chạy"; các trận chiến tiếp theo, bảng điều khiển, màn hình rộng và liên kết là độc lập. Khi bắt đầu làm việc với mã, hãy kiểm kê lại cây công việc. Nội dung không được cam kết hiện có không thể được trộn lẫn vào toàn bộ gói gửi mới.

Thử nghiệm tĩnh tập trung vào việc kiểm soát chuỗi sự kiện, ranh giới Unicode, tính toàn vẹn của trang, chống trùng lặp lịch sử và lỗi cảnh; thử nghiệm gốc bao gồm vòng đời tài nguyên, phạm vi bố cục và ảnh chụp nhanh luồng. Kết quả GPU ghi lại phông chữ, nền tảng, cấu hình và nhận dạng cảnh; nâng cấp hệ thống có thể thay đổi pixel glyph và không làm cho sự bình đẳng băm PNG của hệ thống chéo trở thành điều kiện chung. Việc kiểm tra theo yêu cầu của kho được thực hiện trước khi nộp chính thức và bằng chứng thời gian chạy được ghi lại theo phạm vi hoàn thành thực tế.

Khi giải pháp được thiết lập, mục nhập mã nguồn và giao diện chính thức đã được kiểm tra; sau đó quá trình xác minh kết xuất Văn bản cốt lõi cảnh cố định của T0 được triển khai theo yêu cầu của người dùng. Thử nghiệm này sử dụng mục tiêu phát lại đồ họa độc lập và không bắt đầu phiên trò chơi mới hoặc thay đổi tệp lưu; bản ghi xác minh và thăm dò Core Text đã bị xóa vào ngày 24-09-2026.