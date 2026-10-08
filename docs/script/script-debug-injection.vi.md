> **Ngôn ngữ / Language:** [Tiếng Việt](script-debug-injection.vi.md) · [English](script-debug-injection.en.md) · [中文](script-debug-injection.md)

# Gỡ lỗi chèn tập lệnh: sử dụng hướng dẫn tùy chỉnh để xác minh tác dụng của hướng dẫn

Cập nhật: 2026-09-16. Trang này ghi lại chức năng gỡ lỗi chèn tập lệnh của máy chủ gốc: chuyển tập lệnh sự kiện bạn viết cho công cụ tập lệnh gốc để thực thi trong trò chơi đang chạy và sử dụng tính năng theo dõi thăm dò, thăm dò trạng thái và khung lấy mẫu để kiểm tra hiệu quả thực tế của từng lệnh. Đây là công cụ dành cho bước 3 và 4 của [Xác nhận ngữ nghĩa hướng dẫn còn lại](script-semantics-confirmation.md). Nó không phải là một bản viết lại tập lệnh, cũng không thay đổi ROM, dữ liệu thư mục hoặc các sự kiện ban đầu.

## Cơ chế phía máy chủ

- Công tắc `SRW64_SCRIPT_INJECT=1`; `src/host/script_inject.hpp` được gọi bởi `game_hooks.cpp` và `host.cpp`. `run_host_probe.py` chỉ chấp nhận chuyển đổi này khi cấu hình phiên bản tiếng Nhật, `--graphics`, im lặng, giới hạn VI và `SRW64_SCRIPT_TRACE=1` được bật cùng lúc và báo cáo ghi `script_inject_enabled`.
- Tệp yêu cầu `script-inject.txt`: một dòng `SRWJ1 <sequence> <at_vi> <hex>`, hex là tiêu đề sự kiện 5 từ (loại + bốn tham số), chuỗi lệnh và kết thúc `FFFF`. Chuỗi VI đọc với cùng tốc độ (cứ sau 6 VI) như `control.txt`; số thứ tự phải được tăng lên, từ chối và ghi lại khi máy chủ bận (xếp hàng đợi hoặc thực thi).
- Tập lệnh ghi vào vùng lưu trữ tạm thời 64 KiB hàng đầu của RDRAM `807F0000`; toàn bộ khu vực lưu trữ tạm thời phải bằng 0 trước khi áp dụng và sau đó bị xóa sau khi hoàn thành.
- Xác định nhàn rỗi (`idle_reason`): `engine+4 = 0xC0`, `+0x97C = 0x80` (không có hoạt động sự kiện), `+0x9AA = 0` (giai đoạn bỏ phiếu 0), `8010F5E8 = 1` (giai đoạn của chúng tôi; giai đoạn số 1 đội của chúng tôi/2 kẻ thù/3 bên thứ ba, giữa các cấp độ: 0), `8010F6B0 = 0` (không có quy trình đánh bại), `8015DA02 ∈ {3, 0xB}` (bản đồ chiến thuật). Khi không hài lòng sẽ ghi là `deferred`. Khi vượt quá 1800 VI sẽ ghi là `idle-timeout` và bỏ cuộc.
- Bắt đầu hình ảnh `8009EE98 → 8009EDB8`: `owner+0x1C` trỏ đến byte thứ 10 của vùng lưu trữ tạm thời (bỏ qua tiêu đề sự kiện), xóa `+0x22..+0x2E`, `+0x30`, `+8/+9 = FF`, `engine+0x990 = 0`, `+0x97C = 0x2000`. Sau đó sẽ có `8009EFDC` thăm dò ban đầu ở mỗi khung hình.
- Đã hoàn thành: PC là 0 và trạng thái là `0x80` hoặc `+0x97C` quay về `0x80`. Tại thời điểm này, số đăng ký `+0x98E` được khôi phục và vùng lưu trữ tạm thời bị xóa và `complete` được ghi lại; PC rời khỏi phạm vi lưu trữ tạm thời và được ghi là `escaped`; 3600 VI không có tiến triển và được ghi là `stalled`.
- Tệp sự kiện `script-inject-events.jsonl` (lược đồ `srw64.script-inject-event.v1`: `queued / deferred / rejected / applied / complete / escaped / stalled`, `applied` và `complete` với ảnh chụp nhanh động cơ). Thăm dò trạng thái lưu trữ ảnh chụp nhanh khu vực tại mỗi ranh giới trong số hai ranh giới `script-inject-applied` và `script-inject-complete`.
- Kiểm tra đơn vị `tests/native_script_inject.cpp` (ASan, `make recomp-script-inject-test`, được sáp nhập vào `recomp-native-check`) bao gồm từ chối phân tích cú pháp, xác định nhàn rỗi, ứng dụng, khôi phục hoàn thành, số thứ tự và từ chối bận.

## Khách hàng `tools/recomp/script_lab/script_debug.py`

- `assemble`: JSON của lược đồ đầu vào `srw64.debug-script.v1` (danh sách `{"op": "3D3B", "args": [0], "note": "…"}`, `event_type` tùy chọn và `header`). Độ dài tham số chỉ được lấy từ khóa bố cục `stage_scripts`. Các hướng dẫn không xác định, trình xử lý trống `3D76/3D77`, `3D78/3D79` không thể truy cập và các tham số nằm ngoài giới hạn đều bị từ chối và một danh sách hex và offset sẽ được xuất ra.
- `inject`: viết `script-inject.txt`, lưu `script-inject-N.json`, đợi `complete / rejected / escaped`.
- `report`: Liên kết đường bỏ phiếu của `SRW64_SCRIPT_TRACE` với ranh giới lệnh theo PC thực tế. Đầu tiên, cuộc thăm dò sẽ quét các điều kiện và cờ, sau đó thực thi tối đa một lệnh: PC dừng sau mã hoạt động trong khi lệnh vẫn đang thực thi và PC dừng ở ranh giới tiếp theo khi hoàn thành; do đó, các lệnh bị bỏ qua bởi các khối điều kiện sai hoặc các đoạn tuyến khác sẽ không bị ghi nhầm là đã thực thi và được đưa vào `commands_not_executed`. VI bắt đầu/kết thúc của mỗi lệnh lấy khung mẫu mới nhất từ ​​`frame-trace.rgb` và lưu nó dưới dạng PNG. Khu vực thăm dò trạng thái so sánh và giải mã tiền, biến và tọa độ danh sách theo byte.
- Đã sửa các tập lệnh trong `config/recomp/debug-scripts/`: `fade`, `scroll`, `map`, `deploy`, `move`, `values`, `dialogue`.

## Bằng chứng đang chạy: `build/recomp/script-debug/inject-2`

Chương 1 (Mục lục cảnh 1 "Depu! スイームルグ", tuyến đường Marino) Lưu trữ giai đoạn của phe chúng ta ở vòng đầu tiên, tắt tiếng, `--vis 12000`, lấy mẫu khung hình 160×120. Bảy tập lệnh được chèn theo trình tự, tất cả `complete`, không có `escaped` hoặc `stalled`; báo cáo `script-debug-report.json`, sự kiện `script-inject-events.jsonl`, nhật ký máy chủ `build/recomp/script-debug/inject-2.native.log`.

| Trình tự | Kịch bản | Lệnh | Kết quả |
| --- | --- | --- | --- |
| 1 | mờ dần | `3D3B` 0/1/2/3 mỗi cái được kết nối với `3D38` | Mỗi chế độ trong số bốn chế độ có 88 VI; giá trị khung lấy mẫu trung bình là 54,6 → 0,6 (đen đục) → 54 (đen trong suốt) → 252,5 (trắng đục) → 57 (trắng trong suốt). `3D38` 45/30 lần đếm tương ứng 90/60 VI: 2 VI mỗi lần đếm. |
| 2 | cuộn | `3D35` (5,5), `3D54`, `3D35` 0x4000/0x4103/0x4203 | `3D35` Cuộc thăm dò tương tự đã hoàn tất, hình ảnh được di chuyển trên các khung tiếp theo (thay đổi mục tiêu tuyệt đối 15006/19200 pixel); 0x4000 trở lại `3D54` Hình ảnh được khôi phục sau khi ghi nhớ vị trí; 3 trên cùng/3 bên phải chỉ thay đổi 85–100 pixel do cạnh góc nhìn. |
| 3 | bản đồ | `3D34` 0,10,10,0 và 0,24,24,1 | Chỉ số bản đồ hiện tại `8010F5EE` 20 → 0, bảng số ngẫu nhiên được xây dựng lại và toàn bộ hình ảnh được thay thế bằng bản đồ 0; 64/42 VI. Tham số đầu tiên là số bản đồ, không phải chế độ: `8020A874` Ghi vào `8010F5EE` rồi tải lại tài nguyên (bằng chứng `script_map_switch_direct`). |
| 4 | triển khai | `3D45` 3 | 292 VI sau danh sách 0/2 xuất hiện (12,21) Đơn vị nhóm 3, cơ thể mới, người lái xe (nhân vật 204) và bản ghi phiên bản vũ khí, đơn vị của chúng tôi xuất hiện ở giữa màn hình. |
| 5 | di chuyển | `3D3C` 28,(25,20); `3D46` 503,1 | 100 VI sau danh sách 0/0 đã thay đổi từ (19,5) thành (25,20); `3D46` 36 VI sau danh sách 0/2 đã bị xóa, bản ghi phiên bản máy bay được giữ lại: xác nhận thoát. |
| 6 | Các khối giá trị, `3DD4`/`3DD1`/`3DD0` mỗi phân đoạn chứa `3D5B` | Vốn 0 → 8000 = (5+1+2)×1000; biến 7 được viết từ 3 đến 2; ACC = 9; biến 7=1 Các khối và phần bị bỏ qua (`commands_not_executed`). +0x4C..+0x50 của phần sửa đổi cơ thể 36 đều là 3 và các phiên bản vũ khí được tính toán lại đồng thời; +0x20 của ba phi công thay đổi từ 100 thành 70, nghĩa là cường độ là −30. |
| 7 | đối thoại | `3D3F`, `3D3E`, `3D48`, `3D38` | Văn bản được chèn sẽ hiển thị trong cửa sổ hội thoại và người nói được phân tích cú pháp là Malina theo lộ trình thời gian chạy; hai đoạn hội thoại là 740/2260 VI (kể cả chờ nhấn A), `3D48` Xong ngay. |

Tất cả các thí nghiệm sau Chuỗi 3 được tiến hành trên bản đồ 0; điều này không ảnh hưởng đến danh sách và kết luận bằng số, nhưng số liệu thống kê pixel của loại quan điểm tùy thuộc vào cảnh hiện tại. Lần chạy đầu tiên của `inject-1` đã bị từ chối vì quá trình xác định không hoạt động coi số giai đoạn bắt đầu từ 0 (`not-player-side`). Nó đã được sửa để bắt đầu từ 1 và các khóa bố cục `engine` và `operand_roles` đã được viết.

Những kết quả này đã được chèn lấp vào trường `runtime` của mỗi lệnh `config/data/original-jp-v1.json` (được hiển thị dưới dạng "Chạy quan sát tiêm" trên trang hướng dẫn của Danh mục và Trình xem): `3D34`, `3D3B`, `3D46`, `3D5F`, `3D6C` đã được nâng cấp lên `code-confirmed`, `3D34` đã được đổi tên thành "Chuyển bản đồ và cuộn đến vị trí", `3D46` đã được đổi tên thành "Lối ra đơn vị", `3D5F` đã được xác nhận là sức mạnh tổng thể −30. Hướng dẫn chung hiện nay là 33 mục `code-confirmed`, 21 mục `structure-confirmed`, 19 mục `unknown`.

## Hạn chế

- Chỉ có thể được thêm vào trong giai đoạn của chúng tôi, khi bản đồ chiến thuật không hoạt động và khi không có sự kiện nào đang diễn ra; lệnh hội thoại cần được nâng cao thông qua nút `control_host.py`.
- Phạm vi quan sát được giới hạn trong vùng cố định của đầu dò trạng thái, khung lấy mẫu 160×120 và thăm dò kịch bản; những thay đổi bộ nhớ không được đầu dò đề cập sẽ không xuất hiện trong báo cáo.
- Việc chèn chứng minh "tác dụng của hướng dẫn này trong ngữ cảnh này" và không thể thay thế việc xác minh phiên bản tập lệnh gốc; ghi lại vào ROM hoặc chỉnh sửa sự kiện ban đầu vẫn yêu cầu sự chấp nhận và chu trình khứ hồi byte độc ​​lập.

## Tái phát

```sh
SRW64_SCRIPT_INJECT=1 SRW64_SCRIPT_TRACE=1 SRW64_STATE_PROBE=1 SRW64_FRAME_TRACE_FROM=2400 SRW64_FRAME_TRACE_TO=9600 \
  .venv/bin/python tools/recomp/run/run_host_probe.py --graphics --profile config/recomp/profiles/play-profile.json --language ja \
  --images original --original-name-entry --resolution-scale 2 --input config/recomp/inputs/load-continue.json \
  --save-from build/recomp/gfx-probes/female-map-audio-3/first-map-turn1.sram \
  --save-sha256 b340a9c686b627d00dfaee9b4d89c896039547f8d607cb51b035d3f7bb2d756b \
  --output build/recomp/script-debug/inject-3 --vis 12000
```

```sh
.venv/bin/python tools/recomp/script_lab/script_debug.py inject build/recomp/script-debug/inject-3 --script config/recomp/debug-scripts/fade.json
```

```sh
.venv/bin/python tools/recomp/script_lab/script_debug.py report build/recomp/script-debug/inject-3
```

Sử dụng thư mục đầu ra mới cho mỗi lần chạy; `control_host.py --buttons` dành cho kịch bản hội thoại và `control_host.py --quit` dành cho việc chấm dứt.