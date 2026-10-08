> **Ngôn ngữ / Language:** [Tiếng Việt](script-runtime-observation.vi.md) · [English](script-runtime-observation.en.md) · [中文](script-runtime-observation.md)

# Quan sát lần chạy script im lặng đầu tiên

Tiến trình theo dõi: [Mở siêu loại nam và chuyển động của đơn vị 3D3C](script-3d3c-runtime.md). Phạm vi bằng chứng từ lần chạy đầu tiên được giữ lại dưới đây.

2026-09-12. Chạy thực tế bản recomp gốc của Nhật Bản, chọn tên mặc định của siêu loại nữ từ trò chơi mới, thông qua cảnh mở đầu của tập đầu tiên đến bản đồ chiến thuật có thể chơi được. Đã thoát thông qua giao thức điều khiển với mã thoát máy chủ 0 sau khi chạy khoảng 185,8 giây và 11.100 VI. Đầu ra thiết bị âm thanh bị tắt và các tác vụ âm thanh của trò chơi gốc vẫn được tính toán bình thường. Sử dụng SRAM trống độc lập, không có lịch sử dùng thử nào được đọc hoặc ghi đè.

## Bằng chứng này

Thư mục đang chạy: `build/recomp/script-analysis/opening-1/`. ROM SHA-256 là `ee5f4a21d8e5f7827d21199e27800edf250df9a8e4d10befb1a6992df597b13e`.

| Kiểm tra | Kết quả |
| --- | --- |
| Sự kiện thực tế | Cảnh 1, sự kiện khai mạc `0019C1B0` |
| Lệnh thông thường/đối thoại | 123 lần, đều quan sát và hoàn thành |
| Đối thoại | 58 hướng dẫn, giống hệt như trình tự ban đầu của phần mở đầu này |
| Các loại hướng dẫn | 13 loại |
| Tham số byte thô | Trận 123/123 |
| Thông số không nhất quán hoặc tiến bộ của PC | 0 |
| Nhật ký/thăm dò ý kiến ​​bị hỏng không có sẵn | 0 / 0 |
| Tự động bỏ qua toàn bộ đoạn hội thoại | Không được sử dụng; chỉ sử dụng phím A bình thường để chuyển tiếp đoạn hội thoại |

Đầu vào khởi động chỉ bỏ qua văn bản mở đầu thu phóng trước đó và lưới tên ban đầu sử dụng tên mặc định; bắt đầu từ dòng hội thoại đầu tiên, toàn bộ lệnh sự kiện được thông qua. Chọn Ảnh và mô hình gốc, ngôn ngữ tiếng Nhật và vẫn sử dụng kiểu sắp chữ hội thoại gốc, vì vậy đây không phải là so sánh từng pixel của phần cứng gốc.

Báo cáo: [`acceptance.json`](../../build/recomp/script-analysis/opening-1/acceptance.json), [`script-observation.json`](../../build/recomp/script-analysis/opening-1/script-observation.json), [`report.json`](../../build/recomp/script-analysis/opening-1/report.json).

## Kết luận thu được

### 3D32: Liên quan đến cách trình bày vị trí bản đồ thế giới, các trường trong bảng vẫn cần được tách rời

Lần này các tham số được thực thi theo `4 → 0 → 1` và ba mục nhập nhất quán với ROM. Bảng `801C5310` có ba nửa từ có dấu cho mỗi mục nhập; tham số 0 tương ứng với `(18, -257, -1010)`, tham số 1 tương ứng với `(18, -144, -372)` và tham số 4 tương ứng với `(17, 721, -435)`.

`801C4BCC` Chuyển đổi hai nửa từ cuối cùng thành giá trị dấu phẩy động và chuyển chúng vào lệnh gọi vẽ/định vị bản đồ; tùy thuộc vào trạng thái hiện tại, nó có thể được đặt trực tiếp hoặc có thể chuyển qua các máy trạng thái mờ dần và tiếp theo. Vì vậy, hướng nghiên cứu chính xác hơn là “lựa chọn cấu hình và định vị trình bày bản đồ”. Chúng ta không thể gọi tất cả các mục trong bảng là cùng một loại chuyển động của camera.

- Tham số 0: VI 3179–3293, lấy 114 VI; màn hình tiếp theo hiển thị vị trí nội địa của lục địa.
- Tham số 1: VI 5791–5845, lấy 54 VI; màn hình tiếp theo là vị trí bờ biển/đảo.
- Tham số 4: Đã hoàn thành trong cùng một cuộc bình chọn. Điều này không thể được sử dụng để kết luận rằng nó không hiệu quả.

Tương ứng với khung máy chủ thực: [sau tham số 0](../../build/recomp/script-analysis/opening-1/present-1680.png), [sau tham số 1](../../build/recomp/script-analysis/opening-1/present-2940.png). Lần này, chỉ các tham số ban đầu được quan sát và không thực hiện thay thế tham số đơn lẻ nào; cấu hình ngữ nghĩa chính thức vẫn giữ mức độ tin cậy ban đầu.

### 3D4D: Quan sát chuyển đổi bản đồ thế giới sang tải chiến trường

Lệnh này được thực thi tại VI 7803 và nâng cao PC; `3D65` tiếp theo sẽ không bắt đầu cho đến VI 8415, với quá trình tải chiến trường và màn hình tiêu đề tập đầu tiên xuất hiện ở giữa. Điều này cho thấy trong ví dụ này, nó đã kích hoạt công tắc quy trình bên ngoài và không thể sử dụng nó để suy ra rằng toàn bộ công tắc màn hình sẽ được hoàn thành ngay lập tức bởi "mục này được hoàn thành ngay lập tức".

Bằng chứng: [Khung tiêu đề tập 1](../../build/recomp/script-analysis/opening-1/present-4140.png). Máy trạng thái bên ngoài và các bối cảnh cuộc gọi khác vẫn cần được theo dõi và lần này sẽ không được nâng cấp lên xác nhận ngữ nghĩa toàn cầu.

### 3D45: Cả 3 nhóm triển khai đều được thực thi theo sự kiện khai mạc

Nhóm 0, 1 và 2 được thực thi lần lượt tại VI 8423–8845, 8849–9141 và 9465–9777; Các đơn vị địch và bạn xuất hiện trên màn hình thực tế và các đơn vị bạn có thể được chọn sau. Bằng chứng: [Bản đồ sau khi xuất hiện](../../build/recomp/script-analysis/opening-1/present-4800.png), [Phạm vi lựa chọn đơn vị](../../build/recomp/script-analysis/opening-1/present-5220.png).

Tất cả ba cuộc gọi đều nằm trong sự kiện mở đầu `0019C1B0` và sự kiện loại 13 độc lập `0019C3A0` không được thực thi vào thời điểm này. Do đó, danh mục "Cấu hình ban đầu" trong trình xem câu chuyện không có nghĩa là các lần thực thi bổ sung phải được thực hiện theo thứ tự này trong trò chơi mới; đường dẫn vào C2 vẫn được xác nhận.

### Vẫn chưa thu được bằng chứng

Không có `3D3C`, `3D36`, `3D55` trong đoạn này và chúng không thể được xác nhận dựa trên bản dùng thử này. Không có trận chiến nào đã hoàn thành, không có yếu tố kích hoạt đánh bại, không có lượt chơi theo cấp độ và không có bản viết lại hoặc bản sửa đổi nào được xác minh. Lần tới, bạn có thể chọn phần mở đầu chuỗi siêu nam có chứa `3D3C`, sử dụng lại máy ghi để phân tích giá trị ban đầu, sau đó thực hiện so sánh một tham số riêng biệt.

## Trình ghi nhật ký và sao chép

`SRW64_SCRIPT_TRACE=1` Cho phép ghi nhật ký ranh giới thăm dò chỉ đọc ở trình bao bọc `8009EFDC` hiện có, tắt theo mặc định. Nhật ký đi vào `RUN.native.log`, bắt đầu bằng `SRW64_SCRIPT_TRACE`. `tools/recomp/analysis/analyze_script_trace.py` sử dụng mục nhập thời gian chạy cảnh, ranh giới lệnh ban đầu, trình xử lý và byte tham số để tạo một kết quả khớp duy nhất và xuất ra các lệnh hội thoại/bình thường thực tế đã được truyền.

Trình ghi nhật ký không chặn mọi chức năng điều kiện bên trong; một cuộc thăm dò có thể quét nhiều điều kiện và sau đó thực hiện một lệnh bình thường. Máy phân tích sẽ không khai báo bất cứ điều gì được quét qua là được thực hiện thực sự. Lệnh cần có thời gian để sử dụng máy chủ VI và không được xử lý trực tiếp như tập lệnh gốc chờ tham số.

```sh
SRW64_SCRIPT_TRACE=1 .venv/bin/python -B tools/recomp/run/run_host_probe.py \
  --graphics --profile config/recomp/profiles/play-profile.json --language ja \
  --images original --original-name-entry --resolution-scale 2 \
  --input build/recomp/script-analysis/opening-input.json \
  --output build/recomp/script-analysis/opening-next --vis 14500
.venv/bin/python -B tools/recomp/analysis/analyze_script_trace.py \
  build/recomp/script-analysis/opening-next
```

Nếu `--audio` không được thông qua, đầu ra của thiết bị sẽ bị tắt. Thư mục chạy không được tồn tại, tập lệnh gõ phím và tóm tắt của nó đã được lưu trong bằng chứng này.

**Ranh giới phiên bản ghi:** Lần chạy hoàn chỉnh này sử dụng `script-poll.v1`, PC, trình xử lý, trạng thái và các tham số đều bình thường nhưng vòng phụ chỉ ghi lại byte cao, giai đoạn ghi lại giá trị 32 bit ban đầu và số trại ghi lại nửa từ thô liền kề. Các trường phụ trợ này không được sử dụng cho việc chấp nhận này. Cuối cùng, `v2` đã sửa độ rộng trường và khóa dòng nhật ký hoàn chỉnh. Nó đã vượt qua các bài kiểm tra về độ bền, độ rộng trường, ranh giới và không ghi cũng như quá trình biên dịch máy chủ của ASan/UBSan; nhật ký trò chơi hoàn chỉnh này vẫn giữ lại v1 và không giả vờ là bằng chứng chạy v2.

Mã thoát chỉ cho biết kết thúc bình thường của thời gian này và không thay thế việc chấp nhận vấn đề thoát khỏi vòng đời của luồng hiện có.