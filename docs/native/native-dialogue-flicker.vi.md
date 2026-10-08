> **Ngôn ngữ / Language:** [Tiếng Việt](native-dialogue-flicker.vi.md) · [English](native-dialogue-flicker.en.md) · [中文](native-dialogue-flicker.md)

# Khắc phục hiện tượng nhấp nháy không liên tục của đoạn hội thoại cốt truyện

Ngày: 2026-09-11. Người dùng báo cáo rằng đoạn hội thoại trong cốt truyện sẽ nhấp nháy không liên tục ở chế độ HD. Lần này âm thanh sẽ bị tắt cho tất cả các lần quay lại tiếp theo.

## Phát hiện thực tế

Việc đọc lại GPU liên tục tìm thấy hai loại vấn đề không thể giải quyết thỏa đáng bằng một ảnh chụp màn hình hoặc bằng cách lấy mẫu sau mỗi 60 khung hình:

1. **Thỉnh thoảng xen vào các khung hội thoại cũ. ** Sau khi dừng ở `base:t00_17412` đoạn 1 và chuyển chế độ hình ảnh, hình tượng gốc tiếng Nhật và bố cục hội thoại gốc đột nhiên xuất hiện trong một số khung hình và giao diện gốc tiếng Trung được khôi phục ở khung hình tiếp theo. Bản đồ và hình đại diện vẫn ở chế độ HD. Trong quá trình ghi liên tục trước khi khôi phục, phát hiện 24 lỗi nhảy hình không mong muốn, tương ứng với việc vào/ra của 12 khung thoại cũ ngắn ngủi.
2. **Việc phát thử bình thường sẽ được ghi lại định kỳ. ** Máy chủ cũ đã mã hóa PNG trong lệnh gọi lại hoàn thành GPU sau mỗi 60 khung hình kết xuất, xuất 8 MiB bộ nhớ sau mỗi 120 tác vụ đồ họa. Trong cảnh tĩnh HD, khoảng thời gian sau khi chụp ảnh màn hình trung bình là 4,87 VI và tối đa 5 VI (khoảng 81–83 mili giây); các khung khác trung bình khoảng 2 VI (33 ms).

Ví dụ trước khi sửa chữa: [Đoạn hội thoại cũ hiển thị trong khung](../../build/recomp/flicker-check/switch-before-1/present-4023.png), [Khôi phục tiếng Trung ở khung tiếp theo](../../build/recomp/flicker-check/switch-before-1/present-4024.png). Những gì được chụp lần này là bố cục hội thoại xen kẽ và toàn bộ khung màu đen không được chụp.

## Sửa đổi

### Giữ một ảnh chụp nhanh hội thoại khác của danh sách hiển thị

Trò chơi gốc có thể chuẩn bị trước hai bộ đệm danh sách hiển thị A và B. Ban đầu, nếu `take_frame()` xóa A rồi thực thi `drawings.clear()` thì ảnh chụp nhanh đã chuẩn bị của B sẽ bị xóa cùng nhau. Khi kết xuất B, nó quay trở lại đường dẫn glyph ban đầu để tạo thành khung flash.

Bây giờ, hãy sử dụng `src/native/presentation/display_list_snapshots.hpp` để quản lý hàng ảnh chụp nhanh được giới hạn và chỉ xóa các bản ghi phù hợp với tác vụ hiện tại; nó sẽ bị xóa hoàn toàn khi cảnh thất bại. Hàng đợi được đồng bộ hóa bởi mutex đối thoại hiện có và bên kết xuất tiếp tục tìm kiếm theo khối lượng công việc thực tế mà không cần đoán khung văn bản từ trạng thái trò chơi mới nhất để che đậy vấn đề.

Phạm vi hồi quy C++: xuất bản A và B trước, sau đó sử dụng A, B vẫn phải đọc được; mỗi ảnh chụp nhanh chỉ có thể được sử dụng một lần; các tác vụ không khớp sẽ không tiêu tốn các ảnh chụp nhanh khác; kịch bản chuyển đổi làm mất hiệu lực các ảnh chụp nhanh đang chờ xử lý.

### Bản dùng thử thông thường sử dụng chẩn đoán nhẹ

2026-10-01: Chẩn đoán hoàn chỉnh đã bị xóa hoàn toàn, máy chủ chỉ có hành vi nhẹ được đề cập ở trên và thông số `--diagnostics` cũng đã bị xóa. Sau đây là ghi chép về thời điểm đó.

`--interactive` cho `run_host_probe.py` được mặc định là `--diagnostics light`, vì vậy tất cả các trình khởi chạy thử nghiệm hiện tại sẽ được hưởng lợi. Chế độ nhẹ tắt tính năng chụp ảnh màn hình GPU định kỳ, xuất bộ nhớ 8 MiB và ghi JSON đối thoại theo từng khung hình, trong khi vẫn giữ lại bản vẽ hội thoại gốc, chuyển đổi hình ảnh và lưu trò chơi.

Thăm dò giới hạn vẫn được đặt mặc định là `--diagnostics full`, duy trì quy trình chấp nhận ảnh chụp màn hình/phát lại hiện có; nó cũng có thể được chọn một cách rõ ràng. Chế độ chẩn đoán ghi báo cáo, không có ảnh chụp màn hình nào bị báo cáo sai là lỗi kết xuất khi chạy các thao tác nhẹ.

## Xem lại khung hình liên tục

Bạn có thể sử dụng `SRW64_FRAME_TRACE_FROM` và `SRW64_FRAME_TRACE_TO` để chỉ định phạm vi VI. Mỗi khung GPU hoàn chỉnh trong phạm vi ghi lại các mẫu 160×120 RGB, khối lượng công việc, chế độ hình ảnh và các thay đổi khung liền kề; những thay đổi quan trọng sau đó được lưu dưới dạng PNG đầy đủ. Chẩn đoán này bị tắt theo mặc định và không vào đường dẫn người chơi bình thường.

```sh
# 静音：不传 --audio。
SRW64_BACKGROUND=1 SRW64_WINDOW_CONTROL=1 \
SRW64_FRAME_TRACE_FROM=7000 SRW64_FRAME_TRACE_TO=10800 \
.venv/bin/python tools/recomp/run/run_host_probe.py --graphics \
  --diagnostics light --profile config/recomp/profiles/play-profile.json \
  --input assets/hd-ai/dialogue-polish/dialogue-only.json \
  --output build/recomp/flicker-check/new-run --vis 11000

.venv/bin/python tools/recomp/analysis/analyze_frame_trace.py \
  build/recomp/flicker-check/new-run --from-vi 7100 --require-stable
```

Phân tích chỉ áp dụng cho đoạn hội thoại tĩnh nói trên: giọt nước được phép xoay và khung hình trong đó hình ảnh được chủ động cắt sẽ bị loại trừ. Nó không thể được sử dụng để nhận biết các chuyển tiếp cốt truyện bình thường là nhấp nháy.

Thư mục bằng chứng `build/recomp/flicker-check/` giữ lại các lần chạy chẩn đoán và chẩn đoán ánh sáng hoàn chỉnh trước khi sửa chữa, chỉ tắt tính năng ghi lại và sau khi sửa chữa ảnh chụp nhanh. Kết quả được thể hiện trong biên bản nghiệm thu bên dưới.

## Sự chấp nhận này

Sau đây là trò chơi RT64/Metal thực tế chạy với ROM gốc tiếng Nhật, hội thoại tiếng Trung bản địa và mô hình giọt nước bản địa và không phải là phát lại danh sách hiển thị cố định. Cả hai đợt chạy cuối cùng đều tắt đầu ra âm thanh, mỗi đợt chạy 11.000 VI; và chủ động chuyển đổi bản gốc/HD bốn lần trong khi đối thoại tĩnh.

| Chạy | Hoàn thành khung hình liên tục | Nhảy màn hình bất ngờ | Kết quả |
| --- | ---: | ---: | --- |
| Trước khi phục hồi, chẩn đoán đầy đủ, chuyển đổi hình ảnh | 2144 | 24 | 12 khung hình flash hội thoại cũ và cách phục hồi chúng |
| Sau khi sửa chữa, chẩn đoán đầy đủ | 1823 | 0 | Đoạn hội thoại cũ không còn bị trộn lẫn khi tải bản ghi nặng hơn |
| Sau khi sửa chữa, chẩn đoán nhẹ | 1846 | 0 | Cấu hình trình phát bình thường và kiểm tra cắt ảnh đã thành công |

Lần chạy đèn cuối cùng sau lần chuyển cuối cùng về HD và ổn định (VI 9500 trở đi), 649 quãng của 650 khung hình liên tiếp đều là 2 VI, khoảng 33 ms. Chẩn đoán đầy đủ vẫn giữ lại chi phí ghi và không thể coi thời gian khung hình là hiệu suất chơi game thông thường. Các cập nhật tài nguyên tại thời điểm cắt hình ảnh, theo dõi chẩn đoán và chủ động lưu ảnh chụp màn hình các thay đổi không được đưa vào kết luận về hiệu suất cảnh ổn định.

Ngoài ra, quá trình chạy im lặng bắt đầu bằng `--interactive` mà không vượt qua `--diagnostics` xác nhận rằng `light` được chọn theo mặc định, thoát bình thường và không có tệp bộ nhớ PNG hoặc 8 MiB định kỳ. `make check` vượt qua 60 bài kiểm tra Python, kiểm tra biên dịch và kiểm tra phần phụ thuộc; `make recomp-content-test` vượt qua hồi quy hàng đợi ảnh chụp nhanh và kiểm tra Kiểm soát đọc/văn bản cốt lõi.

Bản tóm tắt, tệp nguồn và hàm băm bằng chứng có sẵn trong [acceptance.json](../../build/recomp/flicker-check/acceptance.json). Điều này chứng tỏ hiện tượng chập chờn đoạn hội thoại và tạm dừng ghi định kỳ đã được khắc phục; phạm vi chấp nhận là đoạn hội thoại và chuyển đổi hình ảnh ở cấp độ đầu tiên, điều đó không có nghĩa là toàn bộ cốt truyện hoặc tất cả các loại màn hình đen/nhấp nháy đã được che phủ.

## Thanh trạng thái phía dưới biến mất khi phát lại tự động

Phản hồi tiếp theo trong cùng ngày nằm ở cột "Tự động 3/Cỡ chữ 13/Mẹo thao tác" ở phía dưới. Kiểm tra hội thoại tĩnh trước đó không bao gồm trạng thái chuyển giao của các thay thế tự động.

Tái tạo thực tế cho thấy: khi trò chơi gốc xác nhận một câu và chuyển loa, cả hai hộp thoại có thể tạm thời không hoạt động nhưng vẫn hiển thị trên màn hình. Thanh gốc dưới cùng được vẽ trong phạm vi `if (box.active)` của `native_dialogue_text.cpp`, do đó, thanh này sẽ biến mất cùng với khoảng trống tạm thời của người đang nói và xuất hiện cùng với câu tiếp theo. Đây là tình trạng kích hoạt khác với tình trạng mất khung hình trước đó trong hàng đợi ảnh chụp nhanh.

Thanh dưới cùng hiện được chia sẻ bởi hai khung, được vẽ một lần trên mỗi khung; miễn là hộp thoại gốc phù hợp với khối lượng công việc GPU hiện tại vẫn hiển thị thì chế độ đọc, cỡ chữ và lời nhắc thao tác sẽ được hiển thị. Hội thoại tích cực vẫn quyết định độ sáng của văn bản và đánh số trang. Khi hộp thoại đóng hoàn toàn, thanh dưới cùng cũng đóng và không có hiện tượng điền khung hoặc văn bản bị trì hoãn từ các khối lượng công việc khác. (2026-10-06 Thanh dưới cùng sẽ tự động ẩn theo mặc định: đoạn hội thoại sẽ mờ đi sau 5 giây và các phím điều hướng sẽ hiển thị thêm 3 giây nữa. Xem [Giao diện đối thoại · Thao tác](native-dialogue-ui.md#操作). Việc so sánh từng khung hình sau đây đã được thực hiện trước đó; để xem lại bây giờ, bạn cần đặt "Nhắc nhở thao tác đối thoại" trong "Tùy chọn → Giao diện" để luôn hiển thị hoặc chỉ so sánh khối `controls_bar``fade` lớn hơn 0).

Sử dụng cùng một tập lệnh đầu vào, cùng cấu hình ROM và HD gốc, thực hiện chạy thời gian thực im lặng ở tốc độ tự động 3, chạy 11400 VI trước và sau:

| Kiểm tra | Trước khi sửa chữa | Sau khi sửa chữa |
| --- | ---: | ---: |
| Đối thoại tương tự, VI 7200–8580 | 669 khung hình đã hoàn thành | 685 khung hình đã hoàn thành |
| Thanh dưới cùng biến mất bất ngờ | 8 lần, mỗi lần một khung hình | 0 lần |
| Kiểm tra mở rộng, VI 7200–11200 | — | 1959 khung hoàn thành |
| Khung có lời thoại và không có người phát biểu | — | 109 khung hình, giữ lại tất cả các thanh phía dưới |
| Các khung trong đó hộp thoại đã bị đóng | — | 73 khung hình, thanh dưới cùng bị ẩn |

Sự khác biệt về số lượng khung hình hoàn thành trước và sau là do các phiên bản nhấp nháy cũ hơn sẽ kích hoạt các lần lưu PNG chẩn đoán bổ sung. Kiểm tra mở rộng so sánh thanh dưới cùng trong pixel GPU thực tế với trạng thái hiển thị của hộp thoại cho khối lượng công việc đó trên cơ sở từng khung hình và không có sự mâu thuẫn nào. Tính năng phát hiện này cũng kiểm tra bảng điều khiển phía dưới tối và văn bản nhắc nhở của thanh dưới cùng để tránh nhầm toàn bộ cảnh chuyển tiếp màu đen với thanh dưới cùng.

Xem [hiện tại-3628.png](../../build/recomp/auto-toolbar-check/before/present-3628.png) để biết khung biến mất trước khi sửa chữa; xem [handoff-3627-sample.png](../../build/recomp/auto-toolbar-check/after/handoff-3627-sample.png) để biết mẫu GPU khi cùng một VI và cả hai bên tạm thời không hoạt động sau khi sửa chữa. Sau này là các mẫu 160×120 được đọc lại liên tục, không phải ảnh chụp màn hình có độ phân giải gốc.

Lệnh xem lại:

```sh
.venv/bin/python tools/recomp/analysis/analyze_toolbar_trace.py \
  build/recomp/auto-toolbar-check/after --to-vi 8580 --require-visible
.venv/bin/python tools/recomp/analysis/analyze_toolbar_trace.py \
  build/recomp/auto-toolbar-check/after --require-matching-dialogue \
  --output build/recomp/auto-toolbar-check/after/toolbar-boundaries.json
```

Lần này 60 bài kiểm tra Python cho `make check` và `make recomp-content-test` đã vượt qua. Xem [Chấp nhận sửa lỗi thanh dưới cùng](../../build/recomp/auto-toolbar-check/acceptance.json) để biết các hàm băm bằng chứng, đầu vào và cấu hình chạy.