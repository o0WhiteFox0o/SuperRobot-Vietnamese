> **Ngôn ngữ / Language:** [Tiếng Việt](native-foundations-verification.vi.md) · [English](native-foundations-verification.en.md) · [中文](native-foundations-verification.md)

# Cài đặt ngôn ngữ, bộ sưu tập đã lưu và so sánh trạng thái

2026-09-12. Phạm vi là các mô-đun riêng của dự án và không kết nối với các MOD bên ngoài. Việc sản xuất nội dung ngôn ngữ sẽ được dời lại; thời gian ngẫu nhiên của phiên bản gốc không thay đổi và chỉ những khác biệt mới được xác minh và ghi lại.

> Đây là hồ sơ xác minh cho ngày 12-09-2026. Kích thước bản dịch (153 mục), Cocoa F7 và tập lệnh tệp điều khiển đã được thay thế: các bản dịch hiện tại nằm trong [Kiến trúc nội dung gốc](native-content-foundation.md#多语言内容) và quá trình kiểm tra chuyển đổi ngôn ngữ thực tế của máy nằm trong `tools/recomp/debug/check_localization.py`.

## Cài đặt và ghi đè ngôn ngữ

Nhấn **F7** trong khi cấu hình hợp nhất đang chạy và nhấn **Tiếng Nhật → Tiếng Trung → Tiếng Anh** để chuyển đổi nhanh, **không có cửa sổ bật lên** và ghi nhớ lựa chọn cho lần khởi động tiếp theo; tiêu đề cửa sổ hiển thị ngôn ngữ hiện tại. Cài đặt được ghi vào `build/recomp/profile-play/presentation.json`, tách biệt với SRAM của trò chơi và nhận dạng trò chơi. Mức độ ưu tiên của trình khởi chạy rõ ràng `--language`, cài đặt đã lưu, cấu hình mặc định. Cài đặt không hợp lệ sẽ báo cáo lỗi rõ ràng và có thể được ghi đè bằng ngôn ngữ rõ ràng để tiếp tục khởi động.

Bắt đầu từ ngày 13 tháng 9 năm 2026, các phím nóng sẽ xoay vòng theo thứ tự đăng ký hồ sơ `ja` → `zh-Hans` → `en` và tên ngôn ngữ của cửa sổ xuất phát từ cấu hình thư mục; đầu dò ngôn ngữ đơn cũ vẫn có thể chạy. F7 xử lý màn hình trò chơi và trình chỉnh sửa tên thông qua cùng một đường dẫn sự kiện gốc; tự động lặp lại, các kết hợp với các phím bổ trợ không kích hoạt chuyển đổi và F7 được để lại cho phương thức nhập khi phương thức nhập đang soạn từ. Đợi bàn phím vật lý và đầu vào trò chơi gốc được giải phóng trong và sau khi chuyển đổi để tránh việc các phím OK/Start/R vẫn được nhấn bị coi là phím mới. Yêu cầu chuyển đổi được chuyển đến chuỗi trò chơi và bố cục mới được chuẩn bị trước. Sau khi thành công, thư mục bất biến và trạng thái đọc được giải phóng; nếu thất bại, thư mục cũ và trạng thái đọc sẽ được giữ lại. Định cấu hình lỗi ghi đĩa được báo cáo trong tiêu đề và nhật ký cửa sổ mà không có cửa sổ bật lên hoặc giả vờ như đã ghi nhớ cài đặt.

Hội thoại hiện tại vẫn giữ nguyên TextKey, phân đoạn cấu trúc và nhận dạng sự kiện, được định dạng lại và hiển thị từ đầu phân đoạn, đồng thời tự động tiến/chuyển tiếp nhanh/bỏ qua tạm dừng; câu tiếp theo sẽ không được xác nhận cho người chơi. Clip phát lại hoàn chỉnh được chuyển sang ngôn ngữ mới và các tham số động như tên sử dụng kết quả mở rộng được lưu tại thời điểm diễn ra sự kiện. Không có ánh xạ vị trí ký tự đa ngôn ngữ đáng tin cậy cho các đoạn chưa hoàn thành, vì vậy các ngôn ngữ mới sẽ đọc từ đầu đoạn và không tự động đưa phần đuôi chưa đọc vào lịch sử. Trường tên gốc của trò chơi không được dịch hoặc viết lại. Trường nhập và tiêu điểm hiện tại được giữ lại khi bản sao trang tên được làm mới.

Mỗi khung được hiển thị mang một tham chiếu đến thư mục ngôn ngữ khi được tạo; các khung hình cũ vẫn còn trong hàng đợi GPU tiếp tục sử dụng phông chữ/nhãn cũ và các khung hình mới sử dụng toàn bộ thư mục mới để tránh trộn lẫn văn bản cũ với nhãn mới. Chuyển đổi hiển thị không ghi vào bộ nhớ trò chơi. Menu gốc, văn bản nướng, v.v. không được điều chỉnh và người tiêu dùng vẫn sử dụng văn bản gốc. Không thể nói toàn bộ UI đã được bản địa hóa.

`prepare_profile()` biên soạn tất cả các thư mục đã đăng ký, xác minh bản dịch theo phiên bản nguồn và cấu trúc điều khiển rồi xuất ra `coverage.json`. Kết quả của `tools/content/compile_profile.py` bao gồm đường dẫn báo cáo và tóm tắt. Báo cáo tính riêng các bản dịch, bản nháp, bản dịch đã xem xét, bản dịch còn thiếu và từng bảng văn bản; ghi lại những người tiêu dùng chưa truy cập menu gốc, thẻ chiến đấu, mở văn bản nướng, v.v. Nếu thiếu bản dịch, văn bản gốc tiếng Nhật sẽ được sử dụng. Tiếng Nhật là ngôn ngữ nguồn nên "0 bản dịch" không được sử dụng để biểu thị rằng tiếng Nhật bị thiếu.

Có **51.174 mục** trong dữ liệu nguồn này; có **153 mục nháp bằng tiếng Trung và tiếng Anh, 0 mục đã được xem xét và 51.021 mục đã bị trả lại do thiếu bản dịch**. Phạm vi tiếng Anh giống như tiếng Trung hiện có và cũng có tất cả 40 phần copywriting UI gốc. Mẫu số là các bản ghi văn bản được trích xuất, điều này không có nghĩa là tất cả các bản ghi đều có đường dẫn vẽ gốc; 153 không thể được gọi là phạm vi dịch thuật trò chơi đầy đủ.

Bằng chứng cửa sổ và hồi quy:

- Bản ghi về việc khởi động lại sớm có hiệu lực và chuyển đổi nóng bật lên được lưu giữ trong `build/recomp/three-foundations/settings-live/`, `language-restart-ui/`, `hot-locale-flow-final/`; các giao diện này đã được thay thế bằng các phím nóng trực tiếp.
- Phiên bản song ngữ trước đó của verify_locale_switch.py ​​​​(đã xóa, hiện được kiểm tra bởi `tools/recomp/debug/check_localization.py`) gửi các sự kiện nhấn/nhả Cocoa F7 thực tế để xác minh bốn công tắc hai chiều, không có trang tính, cùng một đoạn/số lịch sử, xem lại bản dịch, các phím lặp lại/sửa đổi không được kích hoạt và khu vực quan sát trước và sau khi gửi là nhất quán; bản ghi lần chạy cuối cùng là `hotkey-flow-final/hot-locale-verification.json` và ảnh chụp màn hình cửa sổ là `hotkey-flow-final/hotkey-ja-window.png`.
- Tập lệnh đầu vào ban đầu hình thành tổ hợp phím mới và tắt tính năng xem lại khi vẫn nhấn START/R; `ModalInputRelease` đã được sửa và lần chạy phím nóng cuối cùng vẫn bao gồm tình huống giữ lại này.
- F7, bảo vệ từ nhóm, lưu giữ văn bản chưa gửi và chuyển đổi độc lập HD/Bản gốc của trang tên đã được xác minh và ghi lại độc lập dưới dạng `hotkey-name-final/hotkey-name-verification.json`. Đầu vào kiểm tra `ナナ` duy trì trường gốc sau khi chuyển đổi giữa tiếng Nhật + HD và tiếng Trung + Bản gốc mà không xác nhận tên của trò chơi.
- Các yêu cầu chuyển đổi được xử lý bởi cầu nối bộ điều hợp với chức năng trống cuối khung ban đầu `80085F30`, do đó, các cảnh trang tên/không hội thoại cũng có thể được áp dụng; lệnh gọi hàm ban đầu được giữ lại và bộ điều hợp không ghi ngữ cảnh khách hoặc RAM trò chơi. Vấn đề "chỉ xử lý các yêu cầu khi hội thoại được cập nhật" do thử nghiệm trang tên đầu tiên phát hiện vẫn tồn tại trong `hotkey-name/` và không được coi là đã đạt.
- Kiểm tra trình khởi chạy xác minh rằng ngôn ngữ lưu nhập vào tham số máy chủ, ghi đè rõ ràng có hiệu lực và cài đặt lưu không bị ghi đè. Thử nghiệm này được giữ tách biệt với bằng chứng cửa sổ thực tế.

## Bổ sung xác minh kỹ thuật tiếng Anh (2026-09-13)

`content/locales/en.json` Viết bản nháp tiếng Anh một cách độc lập, phạm vi giống như 153 bản ghi tiếng Trung hiện có, bao gồm 60 menu/thẻ tên và 93 đoạn hội thoại tập đầu tiên, đồng thời hoàn thành thêm 40 đoạn sao chép giao diện người dùng gốc. Tóm tắt nguồn, STOP/END và các tham số tên động được kiểm tra dựa trên bản ghi gốc tiếng Nhật; không có văn bản từ các dự án dịch tiếng Anh khác được trích dẫn. Tiếng Anh sử dụng Helvetica và Core Text để gói từ và phân trang tự động. Ngôn ngữ mới sẽ không mở rộng phạm vi truy cập hiển thị của menu gốc; trường tên và tên của người nói hội thoại sẽ vẫn sử dụng các giá trị gốc của trò chơi và sẽ chuyển về tiếng Nhật nếu không có bản dịch.

Bằng chứng địa phương này được đặt tại `build/recomp/english-support/` và không được phát hành cùng với kho hàng:

- `compiled-en/coverage.json`: 153 bản nháp tiếng Anh, 0 được đánh giá, 51.021 bản dự phòng, giao diện người dùng gốc 40/40.
- `dialogue-live/hot-locale-verification.json`: F7 thực tế chuyển sáu lần trong hai vòng; mỗi khi cài đặt được lưu, các sự kiện cốt truyện giống nhau và số lượng mục nhập lịch sử sẽ được duy trì. Nội dung đánh giá hoàn chỉnh được viết bằng ba ngôn ngữ khác nhau. Các phím lặp lại/sửa đổi không được kích hoạt và không có cửa sổ bật lên. Vùng bộ nhớ trò chơi được quan sát trước và sau khi gửi là nhất quán.
- `name-live/hotkey-name-verification.json`: bốn lần chuyển qua cả ba ngôn ngữ; giá trị đã chỉnh sửa `ナナ` và tiêu điểm được giữ lại, F7 không được kích hoạt khi IME đang nhóm các từ, HD/Bản gốc được chuyển đổi độc lập và tên trò chơi không được xác nhận.
- `english-live/english-reading-verification.json`: Bắt đầu trực tiếp bằng tiếng Anh, đọc tám đoạn hội thoại với xác nhận thông thường, bao gồm các đoạn dài hai trang; mỗi mục lịch sử đã hoàn thành đều nhất quán với văn bản tiếng Anh hoàn chỉnh.
- `verification.json`: Ba lần chạy sử dụng cùng một tệp nhị phân máy chủ, mã thoát là 0, tất cả quá trình tạo/tham gia được quan sát là 4/4, còn lại là 0 và không có chuỗi trò chơi nào trước và sau khi phát hành RDRAM; tóm tắt tập tin nguồn cũng được ghi lại.

`make check` đã được thông qua cho 131 mục, `make recomp-native-check` đã được thông qua. Kiểm tra trình khởi chạy ghi đè các tham số máy chủ mục nhập `en` đã lưu, cũng như ghi đè rõ ràng bằng tiếng Nhật/tiếng Trung mà không ghi đè các tùy chọn hiện có. Cửa sổ thực tế đã được kiểm tra đối thoại tiếng Anh, đoạn phát lại và trang tên; điều này không thể hiện việc đánh giá từng màn hình của tất cả 153 mục, bản dịch tiếng Anh đầy đủ của trò chơi hoặc sự chấp nhận khả năng tương thích toàn bộ quy trình. Thời gian ngẫu nhiên ban đầu không thay đổi.

## Lưu: Giao dịch file đã được xác minh, vẫn còn ngưỡng để khôi phục hoàn toàn

`src/srw64_native/checkpoints.py` là **nguyên mẫu lưu trữ** của bộ sưu tập đã lưu, được lưu tự động bởi những người chơi chưa kết nối. SRAM và trạng thái mở rộng được ghi vào các thế hệ mới bất biến, SHA-256 được tính toán theo từng thành viên và một chỉ mục duy nhất được phát hành nguyên tử sau khi xác minh bảng kê khai. Việc khôi phục chọn thế hệ hoàn chỉnh theo chỉ mục. Khi bị hư hỏng, toàn bộ nhóm sẽ bị lùi lại và các thành viên thuộc các thế hệ khác nhau không bị tách rời. Các thư mục chưa được xuất bản bị bỏ lại do ngừng hoạt động sẽ không được tự động thăng hạng lên các kho lưu trữ có thể phục hồi được. Xoay giới hạn số lượng thế hệ trong chỉ mục và hiện không tự động xóa các thư mục cũ.

Các thử nghiệm bao gồm các thành viên bị hỏng, bảng kê khai bị hỏng, ghi một phần, cam kết chỉ mục không thành công, trạng thái/quy tắc không xác định, chỉ mục xấu và liên kết tượng trưng. `node_verified` ở đây là điều kiện tiên quyết mà lớp thích ứng phải cung cấp. Bản thân kho lưu trữ không xác định nút an toàn của trò chơi. Nguyên mẫu tiện ích mở rộng hiện có chỉ chứa các bảng và chỉ mục RNG và chưa bao gồm số lần gieo hạt lại, trạng thái đọc và không có trình tiêu dùng phục hồi sản xuất nào.

Khóa mục nhập tuần tự hóa ban đầu cho JP Rev 0:

| Lối vào | Chức năng đã được xác nhận |
| --- | --- |
| `800924D8` | Dữ liệu điều hòa được ghi vào RAM `801C2600`, dài `1F00`. RAM này sẽ bao phủ một lớp phủ khác trong giai đoạn bản đồ và không thể gọi được bất cứ lúc nào. |
| `80093278` | Dữ liệu chiến thuật được ghi vào RAM `800FBEF0`, dài `3AE0`. Tham số 0 là bản sao lưu bộ nhớ gốc và tham số 1 được ghi vào SRAM. |
| `800927A4` / `800936A0` | Chuẩn bị ban đầu/phục hồi chiến thuật. |
| `8009EDB8` | Khi giai đoạn tập lệnh `C1` hoàn tất, trạng thái `80` được chuyển đổi thành `C0` và bản sao lưu bộ nhớ chiến thuật sẽ được gọi. |

`original_saves.py` Xác minh định dạng ban đầu: Ba khe SRAM được đặt tại `10`, `1F10` và `3E10`. Kiểm tra thô chiến thuật chỉ tích lũy `1F00` byte, ngay cả khi toàn bộ phân đoạn chiến thuật dài `3AE0`; lỗi đuôi có thể vượt qua kiểm tra thô và do đó không thể thay thế bản tóm tắt tệp đầy đủ.

Hoạt động thực tế đã chiếm được bản sao lưu bộ nhớ gốc sau sự kiện mở đầu tập đầu tiên của Series Siêu Nữ: `first-tactical-capture/state-96-tactical-save.json`, `tactical-95.payload`. Việc mua lại này sử dụng một đầu dò cũ hơn với số chênh lệch số tệp là 1; đầu dò mới đã được thay đổi để tham chiếu rõ ràng đến tệp đính kèm được đánh số tương tự trong hồ sơ quan sát.

Tải bản sao lưu này vào SRAM thử nghiệm độc lập và sử dụng `config/recomp/inputs/load-continue.json` để thoát hoàn toàn rồi khởi động nguội và bạn đã quay lại bản đồ tập đầu tiên. Bản ghi xác minh nguồn, tóm tắt và gốc nằm trong `first-turn-candidate.json`; quan sát được khôi phục nằm ở `first-turn-cold/state-1-tactical-restored.json` và ảnh chụp màn hình bản đồ là `first-turn-cold/present-1620.png`.

`first-turn-restore-comparison.json` So sánh khu vực quan sát chung giữa kết quả trả về tuần tự ban đầu và kết quả khôi phục ban đầu: cờ chiến dịch, các biến cốt truyện, tiến trình/tên người chơi, máy, thí điểm và mảng thành phần đều nhất quán; có **sự khác biệt 2.079 byte** trong khu vực RNG và **sự khác biệt 28 byte** trong bản ghi đơn vị bản đồ. Tất cả các cái sau đều nằm trong trường `+2` của bản ghi 14 `20` byte; quá trình khôi phục trả về `FFFF`, đã được phân bổ lại sau khi xây dựng lại bản đồ xong. Hướng dẫn `801DE0B8` và `801E06C4` của lớp phủ `000AB160` ghi phần xử lý của đối tượng hiển thị `800FFA70 + index*C4 + 48` vào trường này, do đó có cơ sở tĩnh để xây dựng lại tài nguyên bản trình bày. Những khác biệt ban đầu vẫn còn, không có sự khác biệt RNG nào bị loại bỏ hoặc sự tương đương hoàn toàn được yêu cầu trên cơ sở này. Bộ sưu tập cũ chưa bao gồm hai lần gieo hạt lại.

**Kết luận: Người ta đã xác minh rằng bản sao lưu ban đầu này có thể được khởi động nguội trở lại bản đồ, nhưng việc khôi phục trạng thái hoàn toàn vẫn chưa được xác minh. ** Do đó, không đặt nguyên mẫu lưu trữ hoặc thử nghiệm này làm lưu tự động mặc định và không cho rằng các dấu trang khác nhau và tất cả các vòng/nút bảo trì đã được hoàn thành. Ngưỡng triển khai tiếp theo là hoàn thành trạng thái mở rộng và trình tự khôi phục, xác minh tham chiếu tái thiết và hành động thực tế tiếp theo sau khi khôi phục, sau đó bật lưu tự động theo từng nút.

## Bỏ qua so sánh: giữ nguyên thời gian ngẫu nhiên ban đầu

`SRW64_STATE_PROBE=1` Quan sát đồng bộ các đoạn hội thoại, lựa chọn, ranh giới khôi phục và tuần tự hóa ban đầu trong chuỗi trò chơi, đồng thời ghi lại các vùng bộ nhớ chính, lệnh gọi RNG và giá trị trả về. Lưu ý rằng luôn gắn cờ `coverage_complete=false`; `compare_game_states.py` không xuất ra sự tuân thủ byte cục bộ dưới dạng tương đương đầy đủ.

Bảng RNG vani có tại `800D49E0`, được lập chỉ mục tại `800D49D0`; chiến đấu và hiển thị gieo hạt cũng có nội dung `8015DC50`, `80172D0C`. Vòng lặp chính `80080838` nâng cao hai mục cuối cùng trong mỗi khung. Các quan sát mới đã được tích hợp vào cả hai số liệu và không thể loại bỏ vì thời gian hiển thị không liên quan.

Thử nghiệm Đẩy/bỏ qua thông thường đầu tiên khác nhau bởi một hạt giống ban đầu trước khi xảy ra bỏ qua và sự khác biệt trong toàn bộ bảng RNG không thể được quy cho việc bỏ qua. Để làm điều này, hãy thêm căn chỉnh trạng thái ban đầu SRAM QA trống, chỉ im lặng, có thời lượng giới hạn, trống: `SRW64_STATE_FIXTURE` Chỉ ghi bảng RNG, chỉ mục và hai lần đếm lại một lần ở ranh giới hộp thoại đầu tiên được chỉ định. Chỉ cho phép địa chỉ và độ dài cố định, tất cả đều được xác minh trước khi viết và hồ sơ ứng dụng được lưu giữ; trạng thái sẽ không được ghi lại bởi các nút so sánh tiếp theo. Các bản lưu trữ do thử nghiệm tạo ra sẽ bị loại khỏi mục nhập khôi phục lịch sử thông thường.

Cơ sở này được sử dụng để tạo các trạng thái ban đầu thử nghiệm giống hệt nhau, không lưu các bộ tải hoặc sửa đổi quy tắc ngẫu nhiên. Các biến môi trường này không được đặt trong quá trình hoạt động chính thức và thứ tự cập nhật và gieo hạt lại của phiên bản gốc trên mỗi khung vẫn không thay đổi. Do đó, cần phải phân biệt trạng thái ban đầu, các nút đối thoại tiếp theo và phạm vi chiến đấu, đồng thời thử nghiệm đối thoại không thể mở rộng sang chấp nhận chiến đấu toàn diện/hoàn toàn.

Các kết quả của cùng một tệp nhị phân và cùng một trạng thái cố định ban đầu được lưu trữ trong `paired-verification.json`: vùng quan sát hội thoại đầu tiên hoàn toàn nhất quán; các nút trùng khớp **5** tiếp theo đều có `battle_seed_clock` điểm khác biệt và các khu vực được quan sát còn lại đều nhất quán. Ví dụ: nếu cùng một đoạn `17410` tiếp theo đến VI 3721 của tiến trình bình thường và VI 3601 của bỏ qua, thì số lần gieo lại sẽ khác. Theo quyết định của vòng người dùng này, sự khác biệt ban đầu này sẽ được giữ lại, **không đánh dấu trạng thái tương đương ngẫu nhiên nghiêm ngặt là đã vượt qua và sẽ không có tùy chọn sửa đổi quy tắc nào được thêm vào**. Thử nghiệm này chưa bao gồm độ phân giải hoạt ảnh chiến đấu.

## Mục xác minh

```sh
make check
make recomp-native-check
.venv/bin/python tools/content/compile_profile.py \
  --profile config/recomp/profiles/play-profile.json --language zh-Hans \
  --images original --output build/recomp/coverage-review
.venv/bin/python tools/recomp/analysis/compare_game_states.py LEFT.json RIGHT.json \
  --output build/recomp/state-comparison.json
```

Kiểm tra tĩnh/thành phần, thao tác cửa sổ, khởi động nguội bản đồ và tương đương toàn bộ lối chơi là các mức chấp nhận khác nhau. Bản ghi này không đóng toàn bộ M0/M1.

Trong vòng này, `make check` có nghĩa là **129 mục đã được thông qua**; `make recomp-native-check` có nghĩa là **10 chương trình thành phần gốc đã được thông qua**. Lần chạy phím nóng cuối cùng vẫn ghi lại mã thoát của máy chủ và tái chế chuỗi trò chơi 4/4 tương ứng và không thay thế việc kiểm tra cửa sổ thực tế bằng việc chuyển thành phần.