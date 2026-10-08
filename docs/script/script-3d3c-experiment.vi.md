> **Ngôn ngữ / Language:** [Tiếng Việt](script-3d3c-experiment.vi.md) · [English](script-3d3c-experiment.en.md) · [中文](script-3d3c-experiment.md)

# Thí nghiệm điều khiển thông số đơn 3D3C

2026-09-12. Sau [Năm quan sát thông số gốc](script-3d3c-runtime.md), hãy sử dụng mã nhị phân gốc cố định, các khóa giống nhau và SRAM trống độc lập để so sánh tập đầu tiên của loạt phim siêu nam. Tắt đầu ra của thiết bị âm thanh trong thời gian chạy và sử dụng tiếng Nhật, hình ảnh gốc và hiển thị kiểu máy.

## Kết quả nghiệm thu

**Ví dụ về tọa độ tuyệt đối này đã vượt qua: mục tiêu di chuyển lên một khoảng trống và tọa độ logic của điểm cuối yêu tinh và danh sách đơn vị đã được thay đổi cùng lúc. **Cả hai nhóm đã hoàn thành 56 câu lệnh thông thường/đàm thoại mở đầu, 18 câu hội thoại và mã thoát 0.

| Kiểm tra | Nhóm giá trị gốc `move-baseline-2` | Nhóm giá trị đã thay đổi `move-target17-1` |
| --- | --- | --- |
| Thông số mục tiêu | `1912` | `1911` tạm thời, được khôi phục sau khi hoàn thành `1912` |
| Vị trí logic trước khi di chuyển | `(25,28)` | `(25,28)` |
| Vị trí logic sau khi hoàn thành | `(25,18)` | `(25,17)` |
| Vị trí Sprite sau khi hoàn thành | `(432,320)` | `(432,304)` |
| Hướng dẫn mục tiêu VI | 6994–7054 | 6995–7059 |
| Tốn thời gian | 60 VI | 64 VI |
| Vị trí của Brad ở cuối cảnh mở đầu | `(25,18)` | `(25,17)` |
| Vị trí của Kaz ở cuối cảnh mở đầu | `(23,19)` | `(23,19)` |
| Xác minh tham số gốc | Tất cả 56 mục phù hợp | 55 mục trùng khớp và 1 mục còn lại chỉ có chênh lệch tham số được xác định trước |

Cả hai bộ SHA-256 nhị phân đều là `a8d361fb8683453ee8c1bc58d8f9d195d488766c026674fdd8791e168f7d12b4` và mã nguồn máy chủ, ROM, cấu hình đầu vào và hiển thị đều nhất quán. Tại hai ranh giới hoàn thành chuyển động và kết thúc mở, các trường được ghi của tất cả các đơn vị hợp lệ chỉ hiển thị chênh lệch y của Brad trừ 1 và y của Elf trừ 16. Điểm bắt đầu `(25,28)` trong danh sách đã bị bỏ trống; nhóm được đánh giá lại `(25,18)` không còn đơn vị nào, `(25,17)` chỉ có Brad chiếm giữ. Toàn bộ tập lệnh 256 byte trong ảnh chụp nhanh RDRAM cuối cùng cũng nhất quán với ROM gốc.

Hình ảnh sẽ chuyển động khi vị trí của Brad thay đổi. Sau đây không phải là sự khác biệt giữa từng pixel của ống kính cố định; bạn có thể quan sát khoảng cách tương đối giữa Brad và Kaz. VI và tên tệp của khung nguồn được lưu dưới dạng JSON có cùng tên.

![Màn hình trò chơi thực tế với giá trị ban đầu và mục tiêu được di chuyển lên một khoảng trống](../../build/recomp/script-analysis/move-position-comparison.png)

Bằng chứng cuối cùng: [Tất cả 25 lần kiểm tra kiểm soát đã vượt qua](../../build/recomp/script-analysis/move-comparison-2.json), [Báo cáo máy chủ có giá trị ban đầu](../../build/recomp/script-analysis/move-baseline-2/report.json), [Báo cáo máy chủ có giá trị đã thay đổi](../../build/recomp/script-analysis/move-target17-1/report.json). Hai bộ `script-observation.json` giữ lại sự tương ứng hướng dẫn hoàn chỉnh và giá trị ban đầu không khớp trong nhóm giá trị đã sửa đổi được giữ lại một cách rõ ràng.

Lần đầu tiên, nhóm giá trị ban đầu `move-baseline-1` và nhóm giá trị được sửa đổi có cùng mã nguồn và so sánh trạng thái phù hợp với mong đợi. Tuy nhiên, trình khởi chạy sẽ tạo lại RSP và liên kết nó, còn bản tóm tắt nhị phân thì khác, do đó [vòng so sánh nghiêm ngặt đầu tiên không thành công](../../build/recomp/script-analysis/move-comparison-1.json). Sau đó thêm `--reuse-build-from` bằng xác minh dấu vân tay và sử dụng lại tệp gốc của nhóm giá trị đã sửa đổi để chạy `move-baseline-2`; sự chấp nhận cuối cùng sử dụng kết quả chạy lại. Các báo cáo cũ không được ghi đè.

## Ý nghĩa và ranh giới của cấp độ Mod

`3D3C` tọa độ tuyệt đối thông thường có thể thay đổi vị trí đơn vị cấp thực tế. Nhóm giá trị ban đầu cũng hiển thị: yêu tinh đến điểm cuối trước và tọa độ logic vẫn giữ nguyên điểm bắt đầu; chúng không được viết lại cho đến khi cuộc gọi kết thúc hoàn tất. Do đó, các sự kiện tiếp theo phụ thuộc vào vị trí sẽ đợi lệnh này hoàn tất.

Các vị trí tương đối, mục tiêu ngoài giới hạn hoặc không thể tiếp cận, nhiều đơn vị có cùng số điều khiển, mục tiêu không tồn tại, chiến đấu hoàn chỉnh và lưu tải lại không được chấp nhận trong vòng này. Mức độ tin cậy chính thức tiếp tục là `structure-confirmed`, nhưng có bằng chứng hoạt động cho thấy sự dịch chuyển tọa độ tuyệt đối, đóng bản ghi lại và thử nghiệm tham số duy nhất này.

## Thiết kế và cách ly thí nghiệm

Sự can thiệp duy nhất là tham số thứ hai của sự kiện `0019BF10 + 00C8`: `1912 → 1911`, tức là mục tiêu của trình điều khiển 27 ブラッド được thay đổi từ `(25,18)` thành `(25,17)`. File ROM gốc không thay đổi.

`script_move_probe.hpp` bị tắt theo mặc định, `SRW64_SCRIPT_MOVE_PROBE=baseline` chỉ được ghi lại và `target17` bị ghi đè tạm thời. Thử nghiệm cố định sẽ kiểm tra cảnh 0, lộ trình `3DD3`, giai đoạn `C1`, PC sẽ được thực thi `8019B4C8`, dấu vân tay sự kiện 256 byte và hướng dẫn/tham số gốc và chỉ viết `8019B4CC` nếu tất cả đều khớp. Chỉ được thực hiện một lần, `1912` sẽ được khôi phục sau khi lệnh hoàn tất; nếu phát hiện tham số đã bị mã khác ghi đè thì xung đột sẽ được ghi lại mà không ghi đè. Trình khởi chạy yêu cầu JP thô, tắt tiếng, SRAM trống, bật ghi nhật ký tập lệnh.

Cả hai lần chạy đều sử dụng cùng một [tệp đầu vào](../../config/recomp/inputs/script-move-probe-input.json). `SRW64_SCRIPT_TRACE` trong nhật ký vẫn giữ lại các tham số thực tế, do đó nhóm thay đổi phải tạo ra sự không khớp rõ ràng với giá trị ban đầu; bộ so sánh độc lập chỉ chấp nhận `1912 → 1911` được chỉ định trước và không che giấu sự khác biệt.

## Trạng thái đã ghi

Mỗi cuộc thăm dò lệnh mục tiêu ghi lại tất cả các đơn vị hợp lệ trong 30 vị trí cho mỗi phe trong số ba phe: phe, vị trí, con trỏ đơn vị, số trình điều khiển, byte trạng thái, x/y logic, chỉ mục sprite và x/y sprite. Đồng thời ghi lại ranh giới trước khi di chuyển, sau khi ghi đè, hoàn thành lệnh, sau khi khôi phục và hoàn thành câu cuối cùng của phần mở đầu.

Tọa độ logic được ghi lại từ `load_000AB160:801CBEB8`: `801E510C` tìm trại/khe từ chỉ mục sprite và ghi `(精灵位置−32)>>4` vào `8015E100 + 阵营×0x258 + 槽×0x14 + 4/+5`. Cửa sổ bằng chứng `script_actor_movement_commit` mới khóa mã máy thô này; bài kiểm tra sẽ kiểm tra hai hướng dẫn ghi tọa độ một cách độc lập.

"Sức chứa" ở đây dựa trên bảng liệt kê tọa độ danh sách hợp lệ và không có nghĩa là truy vấn va chạm trong trò chơi, khả năng vượt qua địa hình, quy tắc chặn hoặc bộ nhớ đệm nghề nghiệp độc lập đã được xác minh.

## Lệnh sao chép

```sh
# 先运行改值组，保留构建指纹。
SRW64_SCRIPT_TRACE=1 SRW64_SCRIPT_MOVE_PROBE=target17 \
SRW64_FRAME_TRACE_FROM=6800 SRW64_FRAME_TRACE_TO=8100 \
.venv/bin/python -B tools/recomp/run/run_host_probe.py \
  --graphics --profile config/recomp/profiles/play-profile.json --language ja \
  --images original --original-name-entry --resolution-scale 2 \
  --input config/recomp/inputs/script-move-probe-input.json \
  --output build/recomp/script-analysis/move-target17-next --vis 9000

# 原值组复用同一文件，拒绝二进制、源码、ROM、生成报告或 ABI 指纹变化。
SRW64_SCRIPT_TRACE=1 SRW64_SCRIPT_MOVE_PROBE=baseline \
SRW64_FRAME_TRACE_FROM=6800 SRW64_FRAME_TRACE_TO=8100 \
.venv/bin/python -B tools/recomp/run/run_host_probe.py \
  --graphics --profile config/recomp/profiles/play-profile.json --language ja \
  --images original --original-name-entry --resolution-scale 2 \
  --input config/recomp/inputs/script-move-probe-input.json \
  --reuse-build-from build/recomp/script-analysis/move-target17-next \
  --output build/recomp/script-analysis/move-baseline-next --vis 9000

.venv/bin/python -B tools/recomp/analysis/analyze_move_probe.py \
  build/recomp/script-analysis/move-baseline-next \
  build/recomp/script-analysis/move-target17-next \
  --output build/recomp/script-analysis/move-comparison-next.json
```

Sau khi khai mạc, bạn có thể thoát sớm thông qua `control_host.py RUN --quit`; thí nghiệm này không yêu cầu phải hoàn thành trận chiến. Sự chấp nhận cuối cùng của hai nhóm dựa trên lệnh mục tiêu và ranh giới mở và không yêu cầu thời gian bắt đầu và thoát ra của đồng hồ treo tường phải giống hệt nhau.

## Mã và xác minh

- [Đầu dò thử nghiệm cố định](../../src/host/script_move_probe.hpp): Tắt máy mặc định, xác minh danh tính, ghi đè một lần, khôi phục lần cuối và chụp nhanh trạng thái.
- [Bộ so sánh](../../tools/recomp/analysis/analyze_move_probe.py): Chấp nhận chính xác một chênh lệch tham số được xác định trước trong khi kiểm tra nguồn/nhị phân, trình tự lệnh, khôi phục và thay đổi danh sách.
- [Kiểm tra thành phần](../../tests/native_script_move_probe.cpp): Xác minh theo ASan/UBSan mặc định là không ghi, từ chối tính không tương thích danh tính, chỉ thay đổi một byte, khôi phục, thực thi đơn lẻ và xung đột sẽ không bị ghi đè.
- `PYTHONDONTWRITEBYTECODE=1 make check`: 97 mục đã được thông qua, các bước kiểm tra biên dịch và phụ thuộc đã được thông qua; thư mục được xây dựng lại thành 83 mục bằng chứng, tất cả các tài liệu tham khảo đều có thể phân giải được.
- Ví dụ tiêu cực về trình khởi chạy: thử nghiệm bật âm thanh bị từ chối; yêu cầu sử dụng lại bản tóm tắt nhị phân giả mạo đã bị từ chối. Bộ so sánh cũng từ chối hai bản ghi giá trị ban đầu dưới dạng thử nghiệm thay đổi giá trị.