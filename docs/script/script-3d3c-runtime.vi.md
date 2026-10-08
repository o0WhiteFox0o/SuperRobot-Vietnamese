> **Ngôn ngữ / Language:** [Tiếng Việt](script-3d3c-runtime.vi.md) · [English](script-3d3c-runtime.en.md) · [中文](script-3d3c-runtime.md)

# 3D3C: Chạy im lặng quan sát phần mở đầu siêu phẩm nam

Để biết tiến trình tiếp theo, vui lòng xem [Thử nghiệm kiểm soát thông số đơn](script-3d3c-experiment.md). Bài viết này giữ lại ranh giới bằng chứng của các quan sát tham số ban đầu.

2026-09-12. Phiên bản gốc của phần tóm tắt tiếng Nhật thực sự chạy khoảng 154,9 giây, nhập tập đầu tiên từ tên mặc định của siêu loại nam và đến bản đồ chiến thuật hoạt động sau khi mở hoàn toàn. Đã thoát qua giao thức điều khiển tại VI 9252 với mã thoát 0, không để lại quá trình kiểm tra giao tử. Đầu ra của thiết bị âm thanh bị tắt và tác vụ âm thanh vẫn được tính toán; SRAM trống độc lập, hình ảnh/mô hình gốc, bố cục hội thoại tiếng Nhật và bản địa được sử dụng. Không có tham số ROM hoặc tập lệnh nào được sửa đổi lần này.

## Đang chạy bằng chứng

Thư mục: `build/recomp/script-analysis/male-opening-2/`. ROM SHA-256: `ee5f4a21d8e5f7827d21199e27800edf250df9a8e4d10befb1a6992df597b13e`.

| Kiểm tra | Kết quả |
| --- | --- |
| Cảnh/Tuyến Đường | 0／`3DD3`, siêu mẫu nam |
| Sự kiện thực tế | `base:stage_events:0019bf10` |
| Lệnh thông thường/đối thoại | 56 lần, đều hoàn thành; thứ tự phù hợp với toàn bộ sự kiện khai trương |
| Lệnh đối thoại/Loại lệnh | 18／17 |
| Byte tham số gốc | Trận 56/56 |
| PC hoặc thông số không nhất quán/Cuộc thăm dò không khớp/Nhật ký xấu | 0/0/0 |
| Phiên bản ghi nhật ký | `srw64.script-poll.v2`, 103 bản ghi ranh giới cuộc thăm dò |
| Đầu ra âm thanh | `false` |

Báo cáo hoàn chỉnh: [Chấp nhận](../../build/recomp/script-analysis/male-opening-2/acceptance.json), [Thư từ lệnh](../../build/recomp/script-analysis/male-opening-2/script-observation.json), [Báo cáo máy chủ](../../build/recomp/script-analysis/male-opening-2/report.json). Màn hình cuối cùng: [Lựa chọn đơn vị cho bản đồ chiến thuật](../../build/recomp/script-analysis/male-opening-2/present-4615.png). Việc nhấn phím chỉ bỏ qua văn bản thu phóng mở đầu và đoạn hội thoại sự kiện được nâng cao bằng phím A thông thường.

## Sửa đổi ý nghĩa tham số

`3D3C` ban đầu được gắn nhãn "Hiệu ứng vị trí bản đồ (loại, vị trí)", giờ được đổi thành **"Đơn vị di chuyển đến vị trí (người lái xe, vị trí)"**, `unknown → structure-confirmed`. Tham số đầu tiên được liên kết với hồ sơ trình điều khiển.

Link mã máy:

1. Đóng cửa sổ có cư dân `800A0360`, sử dụng `800A38DC` để giải mã tham số thứ hai, sau đó gọi `8020A030(x, y, 第一参数)` của lớp phủ chiến trường.
2. `8020A030` vượt qua ba phe `8015E100`, mỗi phe có 30 vị trí, kích thước bước của vị trí là `0x14` và kích thước bước của vị trí là `0x258`. `+0xC` của vị trí hợp lệ trỏ đến thiết bị, `+0x38` của thiết bị trỏ đến trình điều khiển và số `+2` của trình điều khiển được so sánh. Lấy lần xuất hiện đầu tiên theo thứ tự truyền tải. Vì vậy, tham số đầu tiên là số lượng trình điều khiển.
3. Tọa độ lưới mục tiêu được chuyển đổi thành `格坐标 × 16 + 32`. Bảng trạng thái `8021E230` trỏ tới chuyển động ngang `8020A4BC`, chuyển động dọc `8020A5F0`, đóng `8020A724` và lần lượt xử lý trống. Chuyển động ngang và dọc sử dụng các bước 8 đơn vị đã ký; nó không thể được chuyển đổi trực tiếp sang "khung hình trên mỗi khung hình" của trò chơi gốc vì nó cần phân biệt giữa VI, tần suất bỏ phiếu và rút thăm.
4. `8020A788` cập nhật ống kính với vị trí sprite và trở về hoàn thành ở trạng thái 3. Trình xử lý thường trú nâng tham số PC thêm 4 byte.

Cửa sổ bằng chứng `script_actor_movement` khóa byte ROM thô của `load_000AB160:8020A030..8020A874` bằng SHA-256; liên kết bằng chứng hướng dẫn trong thư mục đã liên kết với cửa sổ này. Kiểm tra hồi quy kiểm tra độc lập các hướng dẫn tải Đơn vị→Trình điều khiển→Số của ROM và kiểm tra các tham chiếu ký tự và giải mã vị trí cho năm phiên bản tập lệnh thực.

## Năm lệnh gọi tham số ban đầu

Phần bù có liên quan đến thời điểm bắt đầu sự kiện; tọa độ lưới là giá trị ban đầu của tập lệnh, không phải pixel màn hình.

| Sự kiện bù đắp | Số tài xế | Vị trí mục tiêu | VI bắt đầu và kết thúc | VI tốn thời gian |
| --- | --- | --- | --- | --- |
| `006C` | 298 | `1508` → (21, 8) | 5668–5700 | 32 |
| `00BE` | 27 ngày | `191C` → (25, 28) | 6932–6958 | 26 |
| `00C8` | 27 ngày | `1912` → (25, 18) | 6994–7054 | 60 |
| `00DE` | 31 ngày | `171C` → (23, 28) | 7560–7586 | 26 |
| `00E8` | 31 ngày | `1713` → (23, 19) | 7622–7678 | 56 |

Các khung hình liên tiếp của GPU dường như tương ứng với chuyển động của thiết bị và theo dõi camera. Bảng liên hệ sau lấy các khung từ `frame-trace.rgb` theo thứ tự ghi trong `frame-trace.jsonl`, mỗi khung có kích thước 160×120 RGB; có tựa đề Real VI. Chúng được sử dụng cho hành vi căn chỉnh và không thay thế việc chấp nhận bộ nhớ của tọa độ đơn vị logic.

![Hành động thứ hai của Brad](../../build/recomp/script-analysis/male-opening-2/move-2-27.png)

![Nước đi thứ hai của Kaz](../../build/recomp/script-analysis/male-opening-2/move-4-31.png)

Các ví dụ khác: [298](../../build/recomp/script-analysis/male-opening-2/move-0-298.png), [đoạn đầu tiên của Brad](../../build/recomp/script-analysis/male-opening-2/move-1-27.png), [đoạn đầu tiên của Katz](../../build/recomp/script-analysis/male-opening-2/move-3-31.png).

Phần tương tự cũng được thực thi hai lần, cụ thể là VI 3946-3964 và 4142-4160, mỗi phần chờ 18 VI; điều này chỉ xác nhận việc thực thi và tốn thời gian chứ không xác nhận ngữ nghĩa hiệu suất hoàn chỉnh của tham số và mức độ tin cậy vẫn chưa được biết.

## Chưa được chấp nhận và so sánh với lần sau

Lần này, tôi không hoàn thành trận chiến, không đánh bại cò súng, không vượt qua cấp độ, cũng như không tuân theo các hướng dẫn có điều kiện bên trong. Chuyển động của tọa độ tuyệt đối thông thường được hỗ trợ lẫn nhau bởi mã và màn hình; những điều sau đây vẫn cần được xác nhận: vị trí tương đối và nhánh sửa, số trình điều khiển được chia sẻ bởi nhiều đơn vị hợp lệ, không tìm thấy mục tiêu, vị trí ngoài giới hạn, tọa độ logic và trạng thái chiếm dụng sau khi hoàn thành di chuyển và ghi lại lưu trữ.

Có thể sửa lỗi so sánh tối thiểu tiếp theo: chỉ thay đổi tham số thứ hai của sự kiện `0019BF10 + 00C8` thành `1912 → 1911`, nghĩa là mục tiêu đoạn thứ hai của Brad được thay đổi từ (25,18) thành (25,17), giữ lại trình điều khiển 27 và tất cả các byte khác. Địa chỉ ROM gốc của tham số là `0019BFDC`; địa chỉ tham số thời gian chạy của kịch bản này là `8019B4CC`. Danh tính tải phải được kiểm tra lại trước khi có thể ghi đè. Địa chỉ thời gian chạy không thể được sử dụng trong các trường hợp khác.

Chỉ mong đợi điểm cuối và thời gian của động thái này thay đổi. Việc so sánh cần ghi lại đồng thời vị trí sprite, tọa độ đơn vị logic, trạng thái chiếm đóng và chuyển động tiếp theo của Kaz, đồng thời đăng ký rõ ràng các byte đã thay đổi dưới dạng thử nghiệm và không thể âm thầm phát hành kiểm tra tính nhất quán của giá trị ban đầu. Lần này chỉ có thiết kế thử nghiệm được xác định và không có sự thay thế tham số nào được thực hiện.

## Tái phát

```sh
SRW64_SCRIPT_TRACE=1 SRW64_FRAME_TRACE_FROM=3600 SRW64_FRAME_TRACE_TO=12000 \
.venv/bin/python -B tools/recomp/run/run_host_probe.py \
  --graphics --profile config/recomp/profiles/play-profile.json --language ja \
  --images original --original-name-entry --resolution-scale 2 \
  --input build/recomp/script-analysis/male-opening-input.json \
  --output build/recomp/script-analysis/male-opening-next --vis 14500
.venv/bin/python -B tools/recomp/analysis/analyze_script_trace.py \
  build/recomp/script-analysis/male-opening-next
```

Không vượt qua `--audio`. Tóm tắt tệp đầu vào nằm trong báo cáo máy chủ; thư mục đầu ra không được tồn tại. Sau khi đến bản đồ chiến thuật, hãy sử dụng `control_host.py RUN --quit` để kết thúc, nhằm tránh việc chọn đơn vị phím A tiếp theo. Lần thử đầu tiên tại `male-opening-1` đã bị từ chối trước khi khởi chạy trò chơi vì `--vis 13000` nhỏ hơn phạm vi sự kiện đầu vào; báo cáo này chỉ sử dụng `male-opening-2` thành công sau đó mà không trộn lẫn nhật ký hai lần.

Xác minh: `PYTHONDONTWRITEBYTECODE=1 make check`, 97 bài kiểm tra đã đạt, kiểm tra biên dịch và kiểm tra phụ thuộc đã đạt; thư mục gốc đã được tạo lại, 82 mục bằng chứng và tất cả các tài liệu tham khảo đều có thể phân tích được.