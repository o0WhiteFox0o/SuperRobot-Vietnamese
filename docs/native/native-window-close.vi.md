> **Ngôn ngữ / Language:** [Tiếng Việt](native-window-close.vi.md) · [English](native-window-close.en.md) · [中文](native-window-close.md)

# Sự cố thoát khỏi máy chủ khi đóng cửa sổ

Cập nhật ngày 12 tháng 9 năm 2026: Việc hợp tác dừng, đánh thức và tái chế hoàn toàn chuỗi trò chơi đã được triển khai; các phiên bản cuối cùng của cửa sổ đóng tên → ô hiện đại và cửa sổ đóng trang tên gốc đã được thông qua. Lỗi ban đầu "4 chủ đề trò chơi vẫn tồn tại khi RDRAM được phát hành" đã được loại bỏ trong các mục này. Kết quả và bằng chứng đầy đủ về đợt xuất cảnh tự động này của VI được tóm tắt trong biên bản nghiệm thu dưới đây; chúng tôi không khẳng định rằng toàn bộ trò chơi, khôi phục kho lưu trữ hoặc bất kỳ cảnh bị kẹt nào đã được chấp nhận dựa trên điều này.

## 2026-09-12 Đã sửa

Mã nguồn nằm ở `tools/recomp/toolchain/prepare_runtime_lifecycle.py` và `src/host/runtime-support/guest_shutdown.hpp`. Trình tạo được kiểm tra dựa trên phiên bản cố định và tạo ra các điều chỉnh cục bộ của `threads.cpp`, `mesgqueue.cpp`, `scheduling.cpp`, `timer.cpp` và `recomp.cpp`, không thay đổi quá trình kiểm tra ngược dòng và xây dựng CPU C.

- Đăng ký luồng máy chủ được tạo bởi `osCreateThread` và sử dụng cùng một khóa để đăng ký, giải phóng tay cầm luồng và xác nhận khởi tạo. Từ chối chủ đề mới sau khi thoát; ngăn chặn trình dọn dẹp hủy trước semaphore khởi tạo khi luồng thoát ngay lập tức.
- Đánh thức lịch chờ và chờ tin nhắn bên ngoài khi thoát; chuỗi trò chơi đưa ra một ngoại lệ chấm dứt hiện có trong thời gian chạy tại điểm an toàn lập lịch/thông báo và đường dẫn thoát sẽ không còn khôi phục logic trò chơi hoặc tiếp tục lên lịch cho các chuỗi khác.
- Trình dọn dẹp không còn dừng sớm với `exited` nữa và phải tham gia từng chủ đề đã đăng ký. Ngữ cảnh luồng đã được nối trong quá trình thoát được giữ lại cho đến khi tất cả các luồng trò chơi kết thúc, ngăn các luồng vẫn đang trong hoạt động lập lịch truy cập vào semaphore đã phát hành.
- RDRAM được phát hành sau khi chuỗi nhập, bộ đếm thời gian, chuỗi sự kiện, trình dọn dẹp chuỗi trò chơi và chuỗi lưu đều được tái chế. Các chủ đề trò chơi chưa đạt đến điểm dừng sẽ ngăn việc phát hành; không buộc phải giải phóng, tách ra hoặc trì hoãn.
- Dấu vân tay tái sử dụng nhị phân được thêm vào trình tạo vòng đời và mã nguồn hỗ trợ. Sau khi sửa đổi các tệp này, máy chủ cũ không thể được sử dụng làm bằng chứng sửa chữa hiện tại.

Việc xác minh phân biệt giữa mã thoát của máy chủ, bản ghi tham gia thực tế và quan sát luồng macOS. `shutdown_verified` yêu cầu số lần tạo/kết nối bằng nhau, xóa các quan sát luồng bằng 0 trước và sau khi RDRAM được phát hành cũng như ghi nhật ký tham gia trước khi phát hành. Khi việc liệt kê luồng hệ thống chưa hoàn tất, `UNOBSERVED` sẽ xuất ra và không thể được coi là luồng không.

Vòng kiểm tra thành phần này sử dụng mã nguồn lập kế hoạch/nhắn tin/dọn dẹp được điều chỉnh thực tế. ASan/UBSan bao gồm việc tiếp nhận bị chặn, chờ tin nhắn nhàn rỗi, chủ đề chưa bắt đầu, chạy bỏ phiếu, hủy/tái sử dụng thông thường, lưu giữ các đối tượng lập lịch trong khi thoát, 40 lần tạo/thoát điều kiện cuộc đua, không có chuỗi trò chơi và tham gia lặp lại. Mục nhập là `make recomp-guest-shutdown-test` và `make recomp-native-check` đã được thêm.

### Chấp nhận cuối cùng

Tóm tắt: [guest-shutdown-check/verification.json](../../build/recomp/guest-shutdown-check/verification.json). Ba cổng này sử dụng cùng một hệ nhị phân máy chủ cuối cùng, tóm tắt mã nguồn viết tay và điều chỉnh vòng đời, tất cả đều im lặng.

| Chạy | Lối thoát | Mã thoát máy chủ | Đã tạo/đã tham gia | Chủ đề game sinh tồn trước/sau khi phát hành RDRAM |
| --- | --- | --- | --- | --- |
| `name-window-final` | Hoàn thành xác minh tên hiện đại, ghi lại, thu phóng, đóng cửa sổ thực sau khi vào cốt truyện | 0 | 4/4 | 0 / 0 |
| `original-window-final-2` | Trang chọn tên ban đầu đã thực sự đóng | 0 | 4/4 | 0 / 0 |
| `vi-stop-final` | Giới hạn trên 600 VI kích hoạt thoát thời gian chạy | 0 | 4/4 | 0 / 0 |

Trạng thái của hai trình bao bọc đã đóng cửa sổ trước là `native-run-ended-before-VI-limit` và CLI trả về 1; đây là chiến lược ban đầu chưa đạt đến giới hạn trên VI đặt trước và máy chủ thoát ra bình thường. Sự chấp nhận thực tế được đánh giá dựa trên mã thoát của máy chủ, hành động đóng cửa sổ, tham gia và quan sát luồng hệ thống.

Lần chạy cuối cùng đầu tiên của `original-window-final` gặp phải việc liệt kê luồng hệ thống chưa hoàn chỉnh trước khi được giải phóng; `shutdown_lifecycle_verified: false` của nó được giữ nguyên và không được tính là vượt qua. `original-window-final-2` tiếp theo của cùng một tệp nhị phân thu được quan sát đầy đủ. `original-window-1` / `name-window-1` sớm là các phiên bản trung gian trước khi bối cảnh gia cố được giữ lại và không được tính vào ma trận cuối cùng.

- `make check`: 98 bài kiểm tra Python, biên dịch tất cả, kiểm tra phụ thuộc đã vượt qua.
- `make recomp-native-check`: 9 chương trình thành phần đã được thông qua và thành phần luồng trò chơi mới sử dụng ASan/UBSan; máy chủ gốc thực tế không được xây dựng bằng cách sử dụng chất khử trùng.
- Ba bản dựng mục tiêu máy chủ đồ họa đã vượt qua và kiểm tra N64ModernRuntime ngược dòng không được sửa đổi.
- `page-exited-to-story-window.png` của lần chạy tên hiện đại cuối cùng đã được xem, biệt hiệu tùy chỉnh, hội thoại tiếng Trung và cửa sổ 1200×800 hiển thị bình thường; không được mở rộng để chấp nhận hình ảnh toàn cảnh.

Bản sửa lỗi này sẽ đóng lỗi "RDRAM được phát hành trong khi chuỗi trò chơi vẫn còn tồn tại" tái diễn. Không có xác minh về việc khôi phục toàn bộ trò chơi hoặc khởi động nguội SRAM; đối với bất kỳ vòng lặp vô hạn nào không còn gọi đến điểm kiểm tra lịch trình/tin nhắn, điểm dừng hợp tác có thể chờ mà không quay trở lại và bộ nhớ sẽ không được giải phóng ngoài quá trình tham gia vào thời điểm này.

## Tái hiện lịch sử và bằng chứng trước khi trùng tu

Sau đây là bản ghi gốc từ 2026-09-11. Lúc đó khuyết điểm đã được thừa nhận nhưng chưa được khắc phục; quá trình thoát bình thường không thể ghi đè lên các bằng chứng luồng này.

## Xác minh hiện tại

Tóm tắt bằng chứng: `build/recomp/window-close-check/verification.json`. Tất cả các bài kiểm tra đều bị tắt tiếng và sử dụng thư mục chạy mới cho mỗi vòng.

| Thư mục đang chạy | Đường dẫn | Mã thoát quy trình | Chủ đề trò chơi sau khi phát hành RDRAM |
| --- | --- | --- | --- |
| `window-1` | Tên đầy đủ của trang mới → Câu chuyện → Real Cocoa Đóng cửa sổ | 0 | Chẩn đoán chưa được bật |
| `control-trace` | Tên đầy đủ của trang mới → Cốt truyện → Thoát script VI | 0 | 4 |
| `window-trace` | Tên đầy đủ của trang mới → Lô → Real Cocoa Đóng cửa sổ | 0 | 4 |
| `original-ui-trace` | Vô hiệu hóa UI tên mới và đóng cửa sổ trong giao diện chọn từ gốc | 0 | 4 |

Việc đóng cửa sổ thực tế ở đây được thực hiện bằng cách gọi hành động đóng của chính cửa sổ thông qua `NSWindow.performClose`, được tạo thông qua ủy quyền cửa sổ của SDL. Không có sự tổng hợp trực tiếp SDL_QUIT và không có quá trình tiêu diệt. `window-close-events.jsonl` ghi lại các hành động và VI. `run_host_probe.py` Trả về trạng thái CLI khác 0 để đóng cửa sổ sớm là chiến lược để không đạt đến giới hạn trên của VI. Giá trị trả về của trình bao bọc này không thể được coi là sự cố máy chủ; `report.json.exit_code` sẽ chiếm ưu thế.

Ba vòng kiểm tra tên hoàn chỉnh đã được xác nhận: chỉnh sửa nhân vật chính/đối tác, Tab/Shift-Tab, gửi bàn phím cửa sổ, đầu vào không hợp lệ và từ chối tên trùng lặp, hủy nhập lại, quay lại trang xác nhận để sửa đổi, tám trường tên cho hai người và biệt hiệu tùy chỉnh trong cốt truyện. 800×600 → 1200×800 Sau khi chia tỷ lệ, kích thước raster GPU/đối thoại là nhất quán và vị trí khung đối thoại và khung trong cửa sổ thực tế đã được kiểm tra. Ảnh chụp màn hình mới nhất là `window-trace/page-exited-to-story-window.png`.

## Thoát bằng chứng

`SRW64_SHUTDOWN_TRACE=1` Chỉ được bật trong các lần chạy chẩn đoán. Trước và sau khi `recomp::start` giải phóng RDRAM, hãy kiểm tra luồng riêng của máy chủ hiện tại thông qua macOS `proc_pidinfo`. Người ta quan sát thấy rằng **Chủ đề trò chơi 1, 6, 4 và 3** vẫn tồn tại khi tập lệnh thoát và Cocoa đóng cửa sổ. Kết quả tương tự sau khi vô hiệu hóa giao diện người dùng tên mới. Họ chờ đợi hầu hết mẫu; Chủ đề trò chơi 1 đang chạy trong một mẫu trước khi phát hành.

Vì vậy, người ta đã xác nhận rằng thời gian chạy không đợi tất cả các luồng trò chơi kết thúc trước khi giải phóng bộ nhớ mà chúng vẫn tham chiếu; đây không phải là vấn đề riêng của giao diện tên mới. SIGSEGV không được kích hoạt lại trong vòng này và chẩn đoán mới cũng có thể thay đổi trình tự cuộc đua. Bốn lần thoát quy trình thông thường không thể được hiểu là đã được sửa chữa.

Sự cố ban đầu xảy ra lúc `build/recomp/name-page/final-hd/`, nhật ký kết thúc lúc `SRW64_WINDOW_QUIT event=256 vi=2855`, theo sau là mã thoát của máy chủ `-11`. Bằng chứng trực tiếp thu được sau khi đọc lại báo cáo sự cố hệ thống:

- Chuỗi chính nằm ở `__munmap → recomp::start → main`.
- Chuỗi bị lỗi là `Game Thread 6`, nằm ở `resident_func_8008AE90 → load_000A7EC0_func_801C28C8`.
- Địa chỉ lỗi là `0x7000025c00`, tương ứng với địa chỉ cơ sở RDRAM được máy này quan sát `0x7000000000` cộng với `0x25c00`.

Báo cáo ban đầu là `~/Library/Logs/DiagnosticReports/srw64-gfx-host-2026-09-11-165355.ips`; ngăn xếp và các hàm băm liên quan đến vấn đề này đã được trích xuất thành `build/recomp/window-close-check/original-crash-evidence.json`.

Thời gian chạy cố định `thread_cleaner_func` kết thúc vòng lặp sau khi `exited` được đặt; quá trình thoát chỉ chờ các luồng nhập, sự kiện, dọn dẹp, lưu trữ và điều chỉnh bộ đếm thời gian mà không dừng hoàn toàn, đánh thức và tái chế tất cả các luồng trò chơi được tạo bởi `osCreateThread`. Việc sửa chữa trước tiên phải hoàn thành việc hợp tác thoát và tham gia chuỗi trò chơi, sau đó giải phóng RDRAM. Nó không thể dựa vào việc phát hành bị trì hoãn hoặc các sự cố ẩn.

## Tái phát

Vào thời điểm đó, việc đặt tên hoàn chỉnh và đóng cửa sổ thực được điều khiển bởi tệp điều khiển của trang tên AppKit và verify_native_name_entry.py, cả hai đều đã bị xóa cùng với trang AppKit; trang tên hiện tại được điều khiển bởi giao diện gỡ lỗi (xem [Nhập tên gốc](native-name-entry.md#验证与证据)). Khi xác minh giao diện người dùng đầu vào ban đầu, hãy thêm `--original-name-entry` vào trình khởi chạy và sử dụng `verify_window_close.py --run RUN --at-vi 1350` để kích hoạt việc đóng cửa sổ thực tế của VI đã chỉ định. Hành động đóng chỉ khả dụng khi `SRW64_WINDOW_CONTROL` được bật.

Vòng này chỉ thêm các mục xác minh mới, bản ghi kết quả và chẩn đoán chuỗi được đóng theo mặc định và thuật toán thoát không bị thay đổi. 60 bài kiểm tra `make check` đã vượt qua.

## Hồi quy sau khi dọn dẹp mã

11-09-2026: Các điều khiển kiểm tra chế độ hình ảnh, thu phóng và đóng cửa sổ chung đã được chia thành các tệp độc lập (sau đó là `window_test_control_macos.mm`, bây giờ là `src/native/ui/window_test_control.cpp`), được gọi bởi bản cập nhật cửa sổ máy chủ đồ họa và không còn dựa vào trang tên nữa. Mã nguồn chẩn đoán luồng được lưu trữ độc lập trong `src/host/runtime-support/shutdown_trace.hpp` và trình tạo vẫn ghi lại bản tóm tắt và đưa nó vào mã nguồn thời gian chạy cục bộ. Thuật toán thoát không thay đổi.

- `build/recomp/cleanup-check/name-window/`: hoàn tất quy trình đặt tên hiện đại, xác minh ban đầu, đọc lại 8 trường, hiển thị ô 1200×800 và đóng cửa sổ thực, mã thoát máy chủ 0.
- `build/recomp/cleanup-check/original-window/`: Vô hiệu hóa trang tên gốc, gọi cửa sổ thực đóng tại VI 1350 trong giao diện chọn từ gốc; Việc chia tỷ lệ SDL độc lập và các yêu cầu/ứng dụng gốc/HD cũng vượt qua, với mã thoát của máy chủ là 0. Điều này chỉ xác thực đường dẫn điều khiển chung và không sao chép toàn bộ so sánh ROI nghệ thuật.
- 4 chủ đề trò chơi vẫn được quan sát thấy sau khi phát hành RDRAM ở cả hai vòng. Báo cáo mới này rõ ràng sử dụng "mã thoát quy trình 0" và ghi lại `shutdown_lifecycle_verified: false`, đồng thời không đánh đồng việc thoát quy trình thông thường với việc tái chế an toàn.

Ba bản tổng hợp máy chủ đồ họa, 60 lượt kiểm tra Python và 8 chương trình thành phần của `make recomp-native-check` đã vượt qua và toàn bộ quá trình kiểm tra diễn ra im lặng. Kết quả sắp xếp mới nhất được đặt tại `build/recomp/cleanup-check/verification.json`; để biết lối vào phát triển, vận hành và bảo trì, hãy xem [Hướng dẫn phát triển bản địa](../guide/native-development.md).