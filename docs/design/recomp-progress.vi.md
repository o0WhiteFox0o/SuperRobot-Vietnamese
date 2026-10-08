> **Ngôn ngữ / Language:** [Tiếng Việt](recomp-progress.vi.md) · [English](recomp-progress.en.md) · [中文](recomp-progress.md)

# Bản ghi thực hiện biên dịch lại SRW64

Bổ sung 2026-09-12: Các suất giải phóng mặt bằng cho tập đầu tiên hiện đã được đọc qua phần khởi động nguội nguyên bản, tổng vòng chuẩn bị đã được khôi phục thành 7, vốn là 14.500 và Manami cấp 2 / SP 102/102 đã được kiểm tra; tập thứ hai chưa được nhập và không có so sánh mô phỏng tham chiếu nào được thêm vào. Xác minh thông báo và khôi phục đã được thêm vào lựa chọn SRAM lịch sử, hãy xem [Bản ghi khôi phục lưu trữ hiện tại](../guide/native-save-recovery.md) để biết chi tiết. “Đọc các khe thông quan cần xác minh” sau đây vẫn là tình trạng bằng chứng tại thời điểm đó.

Cập nhật: 2026-09-08. Điểm cơ sở hoạt động: `bc93a869e99fcafaf2c836751a6d46ee9c7a14dc`.
Văn bản trò chơi hiện được vẽ bằng công cụ văn bản đa nền tảng, xem [đối thoại và văn bản đa nền tảng tiếng Trung, tiếng Nhật và tiếng Anh](../native/portable-text.md); thăm dò phông chữ tại thời điểm đó đã bị xóa.
Mục tiêu vẫn là hoàn thành "Trò chơi mới → Trận chiến hoàn chỉnh → Hoàn thành và chuẩn bị → Lưu → Thoát và khởi động lại tải tệp" trong phiên bản tiếng Nhật.
Xem [Kiến trúc nội dung gốc](../native/native-content-foundation.md) để biết trạng thái truy cập ngôn ngữ hiện tại. Máy chủ bản địa RT64/Metal đã được nâng cấp từ trò chơi mới lên chương đầu tiên của loạt siêu phẩm nữ
Hoàn thành cấp độ và tiết kiệm tổng số tiền cho vòng 7 và 14.500. Người dùng yêu cầu dừng kiểm tra tự động tại kho lưu trữ này và người dùng sẽ
Chơi thử; các hoạt động khởi động lại, tải và bảo trì của khe hở vẫn được xác minh.
Để biết các liên kết bàn phím và mục khởi động, hãy xem [Hướng dẫn dùng thử gốc](../guide/native-playtest.md).

## Đã thu được bằng chứng

| Dự án | Kết quả đo | Phạm vi bằng chứng |
| --- | --- | --- |
| Chuỗi công cụ | biên dịch macOS arm64 của N64Recomp, RSPRecomp, n64sym, N64ModernRuntime và RT64 đầy đủ thành công | Máy chủ bản ghi tác vụ được liên kết và máy chủ đồ họa RT64/Metal |
| Lập bản đồ khởi động | Phạm vi tải thường trú ở mục khởi tạo giống với từng byte ROM, BSS bằng 0 và địa chỉ ngăn xếp khớp với | quan sát thời gian chạy ares |
| LZ bản địa | 6.436 / 6.436 tài nguyên nhất quán, tổng cộng 57.061.848 byte được giải mã; addressSanitizer chạy trên arm64 sau khi tạo C qua | ba chức năng MIPS gốc; I/O ROM, phân bổ và phân bổ được cung cấp bởi bộ điều hợp thử nghiệm rõ ràng |
| LZ trong trò chơi | Bắt cuộc gọi và quay lại từ trò chơi gốc, đầu ra 127.016 byte phù hợp với bộ giải mã độc lập | Chức năng ban đầu thực sự được sử dụng trong trò chơi và các tham số/return/stack và ngữ nghĩa giải mã đã được xác nhận chéo |
| Phạm vi tải | Khôi phục 20 lần chuyển, 18 phạm vi khác nhau, từ một bộ hàm tải đường thẳng | Một trong số đó là truyền có độ dài bằng 0 và một là 16 byte dữ liệu bằng 0; bạn không thể gọi số phạm vi là số lớp phủ mã |
| Nội dung lớp phủ | ROM `0x121560..0x184730` giống hệt RAM `0x801C2600..0x802257D0` ở phạm vi đầy đủ | 405.968 byte nội dung tải thời gian chạy; quan sát này không được đặt tên theo kịch bản được con người chấp nhận |
| Quét chức năng CPU | Sau khi xem xét ranh giới văn bản/dữ liệu, có 3.526 thí sinh; có 3 phần chia chính xác hơn ở lối vào hệ thống | 3.407 chức năng CPU dự trữ được tạo ra; vẫn cần chạy kịch bản để xác minh ranh giới và các cuộc gọi gián tiếp |
| Ràng buộc hệ thống | 282 chữ ký chuẩn hóa hoàn chỉnh trong số 355 thẻ chức năng của n64sym; 122 tên hệ thống được áp dụng kết hợp với xem xét theo hướng dẫn | Chứa các lựa chọn thay thế thời gian chạy và nội bộ hệ thống bị bỏ qua; 11 cuộc gọi còn lại sử dụng mục nhập chẩn đoán với báo cáo lỗi rõ ràng |
| Thực thi gốc CPU | 600 VI liên tiếp, 296 tác vụ đồ họa, 598 tác vụ âm thanh, 1.186.432 mẫu âm thanh, tốc độ mẫu 44.100 Hz | Mục nhập trò chơi và thực thi luồng gốc; đồ họa sử dụng trình ghi tác vụ, mẫu âm thanh vào bộ thu chẩn đoán, màn hình/loa chưa được xác minh |
| Đọc lớp phủ gốc | ROM `0x10DA50` → RAM `0x801C4500`, dài `0x7C50`, tất cả byte đều giống ROM | Bảng tra cứu chức năng được cập nhật sau khi hoàn tất quá trình đọc chặn trò chơi; quan sát này chỉ bao gồm lớp phủ |
| Màn hình GPU gốc | RT64/Metal thực sự chạy trên Apple M4 Max; móc rút đọc lại PNG thông qua GPU blit đã hoàn thành | Bầu trời đầy sao mở đầu, tiếng Nhật phóng to và phần mở đầu công khai đã được xem; đoạn nội dung đầu tiên nhất quán với hình ảnh mô phỏng hiện có và việc so sánh từng pixel/toàn cảnh vẫn chưa được thực hiện |
| Đầu vào gốc | Mặt nạ bit nút N64 độc lập nhấn VI đánh dấu phát lại để nâng cao phần mở đầu công khai | Tệp đầu vào có lược đồ, hàm băm tập lệnh nguồn và hàm băm được biên dịch; không trộn lẫn đánh số RetroPad và mặt nạ N64 gốc |
| Nữ siêu mẫu | `gfx-probes/female-route-1` Đã hoàn thành 5.400 VI; Xem hiện tại-2400 Xác nhận tên mặc định của nữ chính Malino・Hamaru và đối thủ Aアイシャ・リッジモンド; hiện tại-2700 là sự mở đầu của tuyến đường | Xác minh lựa chọn và đặt tên, chưa đạt bản đồ chiến thuật |
| Bản đồ chiến thuật đầu tiên | `gfx-probes/female-map-audio-1/present-6660.png` đã hiển thị địa hình, thị trấn và đơn vị quân địch; Present-7080 hiển thị diện mạo của các đơn vị của chúng tôi bằng màu xanh lam | Màn hình GPU thực tế đã được xem; chuyển động, tấn công và cản phá của cầu thủ vẫn đang được xác minh |
| Hoạt động bản đồ và lưu và tải bị gián đoạn | `female-map-audio-3` Hai thiết bị ban đầu di chuyển, chờ và lưu; sau khi thoát, `first-map-reload-2` khôi phục vòng đầu tiên, tiền 0, vị trí đơn vị và trạng thái hành động | Lưu và tải chiến thuật xuyên suốt quá trình gốc; việc chuẩn bị và lưu pass vẫn cần được xác minh |
| Sự tham gia hoàn chỉnh đầu tiên | `first-map-reload-2` Tên lửa địch tấn công Big Titan 3, HP 8000 → 7990; máy bay địch HP 1500 → 0 sau cuộc phản công bằng tia laser mặt trời, quay trở lại bản đồ sau vụ nổ và kích hoạt cuộc giao chiến tiếp theo | Bản đồ tấn công/phản công/dàn xếp/trở về hoàn chỉnh đã được xem; chưa hoàn thành toàn bộ cấp độ |
| Tập đầu tiên được xóa và lưu | `first-map-turn5-reload-1/present-34260.png` cho thấy tập đầu tiên đã hoàn thành, Malani cấp 2, tổng vòng 7, quỹ 14.500; 32 KiB SRAM đã bị đóng băng | Đánh bại tất cả kẻ thù nguyên bản, cốt truyện sau chiến tranh và vượt qua cấp độ lưu; việc đọc khởi động lại của khe này chưa được so sánh với đầu tham chiếu |
| Nhiệm vụ RSP | Ghi lại đồ họa và âm thanh thực OSTask, ghi lại vi mã, dữ liệu, lệnh và hàm băm | Bằng chứng nộp nhiệm vụ; không có nghĩa là màn hình hoặc loa gốc đã được kết nối |
| Nhiệm vụ âm thanh gốc | Một nhiệm vụ thực sự đã hoàn thành; 117 phạm vi ghi lại RSP DMA được ghi lại đều nhất quán với đầu tham chiếu và ASan vượt qua | Đầu tham chiếu là RDRAM sau cùng một tác vụ và trước lần tải tiếp theo; SP HALT/BROKE/SIG2 đã được cài đặt xong |
| Đầu ra âm thanh gốc | `gfx-probes/female-map-audio-1` đã được kết nối với thiết bị âm thanh SDL; người dùng báo cáo "Tôi nghe thấy âm thanh ổn" trong lần chạy này | Âm thanh mở đầu gốc đã vượt qua buổi thử giọng thủ công; nó không thể được sử dụng để ghi đè các hiệu ứng âm thanh chiến đấu chưa được nhập |
| Kiểm tra kho hàng | 39 bài kiểm tra `make check`, quá trình biên dịch Python và kiểm tra phần phụ thuộc đã đạt | Kiểm tra tĩnh và công cụ; không thay thế việc chấp nhận cảnh gốc |

Phiên bản tiếng Nhật của SHA-256:
`ee5f4a21d8e5f7827d21199e27800edf250df9a8e4d10befb1a6992df597b13e`.
Tài liệu tham khảo độc lập về giải nén gốc là kho lưu trữ `src/srw64_rom/resources.py` này.
Cổng tham chiếu âm thanh được cố định ares v148; việc triển khai vectơ của thời gian chạy cũng bắt nguồn từ ares, do đó việc so sánh đầu ra chứng tỏ
Tính nhất quán của đường dẫn truy cập/biên dịch lại của tác vụ này không phải là bằng chứng giữa hai triển khai phần cứng hoàn toàn độc lập.

Theo dõi `gfx-probes/female-story-1` Ban đầu được lên kế hoạch cho 11.400 VI, nhưng quá trình đã kết thúc với mã 0 ở 5.473 VI
Kết thúc; không thể suy ra thông tin đầu vào hoàn chỉnh với `native-graphics-frames-captured` từ báo cáo cũ.
Nguồn thoát không được ghi lại vào thời điểm đó và không thể kết luận rằng người dùng đã đóng cửa sổ hoặc trò chơi bị trục trặc. Nhật ký sự kiện thoát cửa sổ đã được thêm vào.
Và các lần chạy không đủ VI thực tế sẽ được đánh dấu riêng là `native-run-ended-before-VI-limit`.
Ảnh chụp màn hình GPU hiện được đính kèm với JSON của VI thời gian vẽ và hình ảnh cũng như siêu dữ liệu chỉ được ghi sau khi bộ đệm lệnh GPU hoàn tất.

Để tiếp tục hoạt động chiến đấu của cùng một quy trình, máy chủ thêm `control.txt` đọc lệnh nguyên tử, `live-state.json` mỗi giây
Và `control-events.jsonl` được ghi theo VI thực tế; mục nhập công cụ là `tools/recomp/run/control_host.py`.
Các thao tác nhấn phím trực tiếp đã được thực hiện trong `female-story-2` để nâng cao khả năng đối thoại của nhân vật trên bản đồ thế giới; các sự kiện VI và nhấn phím thực tế được lưu trong
Thư mục đang chạy hiện tại. Mục này chỉ chứng tỏ đầu vào có hiệu quả và không thể thay thế bản đồ chiến thuật, trận chiến hay xác minh lưu và nạp.

`female-map-audio-1` Sau đó, hai chiếc máy bay của chúng tôi đã được vận hành trên bản đồ chiến thuật đầu tiên để di chuyển và chờ đợi.
Nhưng đã thoát khỏi SIGBUS sau khoảng 19.333 VI. Xác nhận ngăn xếp sự cố hệ thống `srw64_queue_audio`
Độ dài mẫu lớn bất thường đã được nhân rộng. Việc gửi âm thanh của `0x8007E28C` thô đọc AI_LEN, theo mục tiêu
736 khung trừ đi các khung còn lại cộng với 240, cuối cùng được viết dưới dạng nửa chữ đã ký; ghi toàn bộ hàng đợi SDL dưới dạng AI_LEN
Sẽ làm cho độ dài này trở thành âm khi tồn đọng. `n64/ai/io.cpp` trong tổng số lượt đọc ares v148
`dmaLength[0]`, là DMA hiện tại chứ không phải tổng của phân đoạn hiện tại và phân đoạn tiếp theo.

Bản vá đầu tiên đã thay đổi để theo dõi DMA hiện tại, nhưng `female-map-audio-2` đã bộc lộ một vấn đề khác: phản hồi của người dùng
Âm thanh và hình ảnh không đồng bộ, 17.418 VI Sau khi dừng bình thường, đỉnh hàng đợi SDL là 1.480.816 khung hình,
Đó là 33,58 giây. Độ dài DMA hiện tại không phản ánh tổng số tồn đọng của thiết bị gốc, do đó việc triển khai này không vượt qua được quá trình đồng bộ hóa
Chấp nhận. `sync-issue.json` Giữ nguyên các phép đo và phản hồi thủ công; âm thanh không thể được truyền dưới dạng "không gặp sự cố".

Máy chủ hiện tại sử dụng lại toàn bộ hàng đợi thiết bị để phản hồi nhịp tổng hợp, giữ lại biên độ đầu ra VI ở giao diện người dùng và
Lượng phản hồi được giới hạn ở VI và sau đó được xử lý theo thời gian thực hiện hiện tại của thời gian chạy. Đây là âm thanh gốc SRW64
Việc điều chỉnh không yêu cầu mô phỏng đầy đủ FIFO hai giai đoạn của AI. Đầu vào nằm ngoài phạm vi độ dài AI DMA sẽ báo lỗi rõ ràng;
Khi tồn đọng thiết bị vượt quá 100 ms, hàng đợi cũ sẽ bị loại bỏ và sự kiện khôi phục được ghi lại, quá trình phát lại bình thường sẽ không yêu cầu khôi phục này.
Đã thêm `audio-live.json` để ghi lại thời lượng hàng đợi và thời gian khôi phục mỗi giây.
`tests/native_audio_queue.cpp` hiện kết hợp công thức độ dài trò chơi ban đầu với mức độ chi tiết tiêu thụ thiết bị 512 khung,
Sự kết hợp gọi lại bị trì hoãn đã chạy 36.000 VI trong khi kiểm tra độ dài và giới hạn tồn đọng, đồng thời ASan/UBSan đã vượt qua.
Thư mục chạy lại gốc là `female-map-audio-3`. Hai phút liên tiếp, 120 mẫu, bao gồm
VI 2.924..10.064: Thời gian xếp hàng SDL là 24,67–38,82 ms, trung bình là 30,98 ms;
Khi kết thúc lấy mẫu, giá trị cao nhất của toàn bộ quá trình chạy là 41,00 ms và số lần khôi phục tồn đọng là bằng không. Bằng chứng nằm ở
`audio-timing-report.json` và `audio-timing-observations.jsonl`.
Mục này xác minh rằng hàng đợi thiết bị không còn tiếp tục tăng nữa; độ trễ đầu ra thực tế của card âm thanh và đồng bộ hóa âm thanh và video hoàn chỉnh vẫn được chấp nhận khi phát lại thực tế.
Quá trình sau đó chạy tới 23.100 VI và thoát bình thường sau lệnh điều khiển; giá trị đỉnh cuối cùng của hàng đợi thiết bị vẫn là
1. 808 khung hình (41,00 ms), không khôi phục được tồn đọng nào, không tái diễn sự cố trước đó ở mức ~19.333 VI.

Sau đó `first-map-reload-2` tiếp tục cho đến 70.583 VI (khoảng 19,61 phút), bao gồm nhiều vòng
Địch phản công, ta chủ động tấn công và quay trở lại bản đồ. Đỉnh hàng đợi thiết bị cho điểm kiểm tra này là 2.016 khung hình
(45,71 ms), số lần khôi phục vẫn bằng 0; xem `audio-sync-checkpoint.json` trong thư mục này.
Đã vượt qua 39 bài kiểm tra `make check`, kiểm tra biên dịch Python và kiểm tra phần phụ thuộc; âm thanh gốc
Đoàn hệ được thử nghiệm bởi ASan/UBSan. Ở đây chúng tôi chỉ chứng minh hàng đợi thiết bị và quy trình gốc chứ không viết chúng dưới dạng
Đo lường vòng lặp card âm thanh hoặc sự chấp nhận thủ công của người dùng về đồng bộ hóa hình ảnh và âm thanh trận chiến.

Quá trình sau đó được lưu ở vòng 5, vốn 8.300, chạy tới 100.968 VI, thông qua lệnh điều khiển
Thoát bình thường (đo được 1.683,92 giây). Đỉnh cao nhất của hàng đợi âm thanh cuối cùng vẫn là 45,71 mili giây và không có khả năng phục hồi.
Cố định SHA-256 của `first-map-turn5.sram` dưới dạng
`591c7db67fb909bc4216f16103757309332fe12e7c65cc64636559cba5579953`.
Quá trình theo dõi `first-map-turn5-reload-1` tiếp tục từ kho lưu trữ này; cũng bắt đầu giai đoạn khởi động này của trình mô phỏng tham chiếu
Tám lần khôi phục tồn đọng đã được ghi lại ở VI 292..536, đạt mức cao nhất là 5.008 khung hình (113,56 ms). sau đó cho đến khi
VI 70.770 thoát ra bình thường, không tăng thời gian tiếp tục, thời gian xếp hàng thông thường là khoảng 25–40 ms. Hiện tượng này xảy ra đồng thời với các tải khởi động song song và chưa được chứng minh
Nhân quả duy nhất; nó được bảo lưu dưới dạng rủi ro bỏ qua âm thanh ngắn hạn trong giai đoạn khởi động và không thể được che đậy bằng hoạt động khôi phục bằng 0 trước đó.
Quá trình khởi động này cũng cho thấy tập lệnh đầu vào VI tuyệt đối sẽ bị ảnh hưởng bởi tiến trình khởi tạo: tập lệnh tiêu đề cố định chưa hoàn thành
Tiếp tục và sau đó tiếp tục đọc tệp thành công thông qua ảnh chụp màn hình menu thực tế và các sự kiện kiểm soát.

Trong quá trình này, ở vòng thứ bảy, tôi đã sử dụng "Hot Blood" và Santiago để đánh bại con quái vật chiến đấu cuối cùng,
Nâng cao câu chuyện thời hậu chiến và lưu trạng thái giải phóng tập đầu tiên trong Lưu 1 của hộp ROM. Tệp bị đóng băng là
`first-map-turn5-reload-1/stage1-clear-turn7.sram`, SHA-256:
`0c6ded15fdf60c6b0064b2260a335d17a4ff77386d14d634bfd7d3bcb8de7484`.
`intermission-save-evidence.json` Ghi lại trạng thái và màn hình lưu; sau đó người dùng yêu cầu kiểm tra tự động
Đến đây là kết thúc nên chúng ta sẽ không tiếp tục với tập thứ hai, các thao tác chuẩn bị, giải phóng mặt bằng và bắt đầu lại việc đọc.

Để chuyển chế độ phát lại thủ công, máy chủ thêm đầu vào bàn phím SDL có giới hạn tiêu điểm và sử dụng ảnh chụp nhanh trạng thái nguyên tử trên các luồng.
`scripts/Play SRW64.command` / `tools/recomp/run/play_native.py` Sao chép kho lưu trữ đông lạnh ở trên lần đầu tiên và sau đó
Sao chép SRAM của thư mục dùng thử độc lập gần đây nhất; mỗi lần chỉ được phép mở một quy trình dùng thử. Chế độ tương tác chưa được đặt
Tự động giới hạn thời gian thoát, hình ảnh GPU sử dụng tên tệp cố định của ảnh chụp màn hình mới nhất. Máy chủ mới đã có sẵn
`keyboard-build-smoke-1` Đã hoàn thành kiểm tra khởi động 600 VI; Đồng bộ bàn phím vật lý và loa vẫn được kiểm tra thủ công.

Trong `female-map-audio-3/present-10500.png`, trò chơi hiển thị rằng quá trình lưu trong bản đồ đã hoàn tất.
SRAM SHA-256 ban đầu là `97a08fb524d03b8f0caaf344205b1dda9f5ea18b42bd48d0627b146998e19904`,
Sau khi lưu, nó sẽ là `b340a9c686b627d00dfaee9b4d89c896039547f8d607cb51b035d3f7bb2d756b`,
Cả hai đều có chiều dài 32 KiB. Bản sao cố định độc lập `first-map-turn1.sram` sẽ được sử dụng cho các quy trình mới để đọc tệp;
Trạng thái hiện tại là vòng đầu tiên, vốn là 0, hai đơn vị thiện chiến ban đầu đang di chuyển và chờ đợi. Đây là sự gián đoạn mang tính chiến thuật để bảo vệ bằng chứng,
Công tác hoàn thiện trận chiến, chuẩn bị giải phóng mặt bằng và cứu nguy giai đoạn này vẫn cần tiếp tục được kiểm chứng.

`first-map-reload-2` Sử dụng SRAM đã được cố định đó để hoàn thành tiêu đề trong quy trình mới → Tiếp tục →
Bản đồ chiến thuật hiện tại-1320 hiển thị vị trí của hai máy sau khi di chuyển và trạng thái màu xám của hành động;
Menu hệ thống của hiện tại-1740 hiển thị Vòng 1, Quỹ 0. Bằng chứng và hàm băm có thể được tìm thấy trong thư mục này
`save-reload-evidence.json`. Menu tiêu đề xoay các tùy chọn thông qua các phím trái và phải và nút Tiếp tục ở đầu màn hình
Bạn không thể sử dụng phím lên để chọn trực tiếp; lần đầu tiên bạn cố gắng vào một trò chơi mới, nó không được tính là tải tệp thành công.

SRAM bị đóng băng tương tự cũng đã được đọc bằng khởi động nguội lõi Mupen64Plus-Next cố định. Lưu nguyên bản dưới dạng
Người cuối lớn; khu vực lưu tổng hợp của lõi tham chiếu đặt 32 KiB SRAM tại `0x20800`, theo
Quy tắc truy cập S8 cho `sram.c` Sau khi chuyển đổi độ bền nội bộ từ, chỉ ghi vào phạm vi này và thực hiện kiểm tra đọc lại hoàn chỉnh.
Đầu tham chiếu thực sự khôi phục bản đồ thông qua Tiếp tục, vị trí cơ thể khớp với trạng thái hành động và menu được hiển thị.
Vòng đầu tiên, viết hoa 0. Hàm băm SRAM vẫn giữ nguyên trước khi nhập và sau khi chạy tham chiếu. Bằng chứng nằm ở
`reference-save/turn1-load-1` và `turn1-inspect-1`; mục nhập là
`tools/recomp/probes/run_reference_save.py`. Đây là trình đọc tệp mô phỏng tham chiếu thực tế và so sánh màn hình.
Trạng thái trực tiếp của phía tham chiếu không được sử dụng làm điểm kiểm tra gốc và cũng không ghi đè trạng thái giải phóng mặt bằng chưa hoàn thành.

Khoản tiết kiệm ban đầu của Vòng 5 cũng đã được khôi phục thành 8.300 quỹ trong trình mô phỏng tham chiếu, đồng thời các vị trí bản đồ và máy đã được khôi phục.
`reference-save/turn5-load-1`, `turn5-inspect-1` so sánh. Hơn nữa từ cùng một SRAM
Phát lại trạng thái đã phục hồi và nhân vật chính di chuyển xuống ba ô và sang trái một ô, đồng thời sử dụng tỷ lệ trúng 100%
HP của Dexter: Cả phiên bản gốc và phiên bản tham chiếu đều thay đổi HP của Dexter từ 3.000
Giảm xuống 0, HP của nhân vật chính vẫn ở mức 3,881 và EN giảm từ 85 xuống 45. Đầu tham chiếu thực sự đã thực hiện
Các cuộc tấn công di động và hoàn chỉnh; `reference-save/turn5-attack-1/visual-comparison.json`
Ghi lại hình ảnh và hàm băm tương ứng. Điều này không suy luận rằng tất cả các trận chiến ngẫu nhiên, thời gian khung hình hoặc các cấp độ tiếp theo sẽ nhất quán.

Danh tính của phiên bản tiếng Nhật hiện tại và thử nghiệm mô hình 5600 đã bị khóa trong `config/recomp/rom-variants.json`, máy chủ lưu trữ
Bảng nhận dạng XXH3 được tạo từ tệp này. Xác minh ROM SHA-256 hoàn chỉnh, 1 MiB ban đầu và tất cả trước khi biên dịch
Phân đoạn tải bị kiểm duyệt; Kết quả CPU từ các bản dựng đã được xác minh của Nhật Bản. Chuyển đổi ngôn ngữ bản địa luôn sử dụng ROM tiếng Nhật.

## Nền tảng và ranh giới cứng rắn

Hiện đang chạy macOS ARM64 + Metal Host. Windows/Linux là các mục tiêu có thể được điều chỉnh theo kiến trúc ngược dòng,
Dự án này vẫn chưa được biên soạn và xác minh trò chơi cho các nền tảng này. Một phiên bản trình duyệt cũng chưa được triển khai.

Thượng nguồn [RT64](https://github.com/rt64/rt64) hiện liệt kê D3D12, Vulkan, Metal và
Windows/Linux/macOS, không có chương trình phụ trợ WebGPU sẵn có. Nếu bạn tạo phiên bản trình duyệt, hãy lên kế hoạch sử dụng lại trò chơi C được tạo tự động
và phân tích tài nguyên, với xác minh bổ sung về Emscripten/Wasm, hàng đợi luồng/tin nhắn, phân bổ bộ nhớ, đồ họa và lưu trữ liên tục.
Phiên bản cố định của librecomp của N64ModernRuntime cũng liên kết với LiveRecomp/SLJIT; xây dựng web phải được xem xét và
Để tách biệt loại đường dẫn mã được tạo trong thời gian chạy gốc này, bạn không thể thay đổi trình biên dịch CMake thành emcc.
[Tài liệu pthread Emscripten](https://emscripten.org/docs/porting/pthreads.html) giải thích về đa luồng
Phụ thuộc vào SharedArrayBuffer và COOP/COEP; [Tài liệu về môi trường thời gian chạy](https://emscripten.org/docs/porting/emscripten-runtime-environment.html)
Giải thích sự khác biệt giữa vòng lặp chính của trình duyệt và tính bền vững của tệp. Đây là những kế hoạch thích ứng tiếp theo và chưa có bằng chứng nào về khả năng thực thi Wasm.

[Zelda64Recomp](https://github.com/Zelda64Recomp/Zelda64Recomp) kết hợp chuyển đổi tĩnh, lớp thời gian chạy hiện đại,
RT64 kết hợp với các bản vá dành riêng cho game. Trong phiên bản tham chiếu cố định đã đọc, `patches/sky_transform_tagging.c`
Hỗ trợ nội suy giữa các khung thông qua các cờ chuyển đổi, `patches/ui_patches.c` thêm GBI mở rộng và căn chỉnh giao diện,
`patches/autosaving.c` Chọn thời gian lưu dựa trên trạng thái trò chơi. Nếu SRW64 muốn được tăng cường thì nó cũng cần được xác định và sửa đổi.
Logic vẽ, bố cục, thời gian và lưu của trò chơi; các bản vá Zelda này không nhằm mục đích thay thế trực tiếp cho các chức năng SRW64.

## Khởi động, bộ nhớ và tải

Các mối quan hệ khởi nghiệp được quan sát:

- Mục nhập tiêu đề ROM: `0x80076610`.
- Mục khởi tạo: `0x8007F5B8`, ngăn xếp: `0x8010F0B0`.
- Tải thường trú: ROM `[0x1000, 0x5BC30)` → RAM `[0x80076610, 0x800D1240)`.
- Tiếp theo văn bản CPU thường trú là RSP boot và cuối văn bản là ROM `0x4DEA0`/RAM `0x800C34B0`.
- Bắt đầu BSS: `[0x800D1240, 0x8018DAC0)`.
- `osMemSize` của trình mô phỏng hiện tại là 8 MiB; trình chụp bây giờ đọc trường này theo mặc định. 4 MiB sớm
Tệp này là ảnh chụp nhanh RDRAM một phần và không thể được sử dụng để loại trừ mã hoặc dữ liệu trong khu vực Expansion Pak.

`0x8007F704` là chức năng chặn đọc ROM của trò chơi. Các thông số là ROM offset, RAM đích,
Chiều dài; phân chia nội bộ PI DMA tối đa `0x400` byte và chờ tin nhắn. họ hàm tải
Các tham số không đổi của `[0x8007FD80, 0x8008016C)` có thể được xây dựng lại từ `analyze_layout.py`.
Trình phân tích cú pháp hỗ trợ một số lượng nhỏ lệnh thực sự xảy ra, xử lý các khe độ trễ của JAL và từ chối tiếp tục các hướng dẫn/đối số không xác định.

Các phạm vi ROM khác nhau được tải liên tục vào `0x801C2600` hoặc `0x801C4500` và được chuyển sang `0x80400000`.
Do đó, danh tính hàm phải bao gồm phân đoạn ROM và bảng tra cứu thời gian chạy phải được cập nhật theo tải chứ không chỉ RAM
Địa chỉ cung cấp cho hàm một tên duy nhất trên toàn cầu. Bản quét hiện tại đã xuất `load_ROMOFFSET_func_VRAM`, danh tính được giữ nguyên.

Vòng tạo mã thường trú đầu tiên không thành công do thiếu ký hiệu `0x801FD020`. Một trong những nguồn của nó hiện được xác nhận là
ROM `0x15BF80`, thuộc về `load_00121560`. Sau khi điền vào các ứng viên được phân biệt theo phạm vi tải, bản gốc
Các vấn đề về biểu tượng bị thiếu đối với 64 mục tiêu JAL bên ngoài khác nhau không còn là trình chặn đầu tiên cho trình tạo.
Kết luận này không có nghĩa là tất cả các cuộc gọi đều có sự chấp nhận ràng buộc thời gian chạy.

Trình tạo có thể liên kết trực tiếp một địa chỉ đích chỉ xuất hiện một lần với một phân đoạn ROM nhất định, nhưng tính duy nhất của ứng viên không chứng minh được
Không có mã cho địa chỉ này trong các phần khác. Bản dựng hiện tại thay đổi rõ ràng 7.213 lệnh gọi được đặt tên thành lớp phủ thành
`LOOKUP_FUNC` của cùng một địa chỉ MIPS vẫn giữ nguyên định nghĩa hàm và địa chỉ gọi ban đầu.
Đọc toàn bộ phần ROM vẫn thực hiện chức năng MIPS gốc; sau khi quay lại, tất cả các byte đã đọc sẽ được kiểm tra, sau đó phần xung đột sẽ được dỡ bỏ và
Đăng ký phân khúc mới. Chỉ một thời gian chạy cập nhật PI DMA duy nhất của `0x400` không có nghĩa là lớp phủ đầy đủ đã được tải.

Lần chạy máy chủ thực đầu tiên gây ra lỗi truy cập khi đọc `AI_LEN_REG` từ `0x800AEBC0` trên chuỗi trò chơi 3.
Xác nhận rằng đó là hướng dẫn `osAiGetLength` theo hướng dẫn rồi nhận nó từ thư viện thời gian chạy. Vòng hoạt động liên tục tiếp theo sẽ trôi qua.
Đồng hồ khách của `osInitialize` được lấp đầy trên toàn cầu bằng đồng hồ `46,875,000` và NTSC VI theo hướng dẫn ban đầu.
`48,681,812`; Hiện tại, đây là quyền truy cập ngữ nghĩa tĩnh và việc so sánh từng trường của điểm trả về hàm ban đầu vẫn chưa được ghi lại.

11 mục không được hỗ trợ trong máy chủ chẩn đoán sẽ in tên hàm và chấm dứt; không có giá trị thành công giả nào được trả về.
Lần chạy thành công hiện tại không kích hoạt chúng và do đó không thể yêu cầu Controller Pak, Transfer Pak hoặc tất cả
Cuộc gọi hệ thống được hỗ trợ. Mỗi lần chạy sử dụng một thư mục SRAM/config độc lập mới và chưa được xác minh để lưu trữ nhiều quá trình.

Máy chủ ghi tác vụ đã hoàn thành thêm 1.800 VI chạy liên tục: 896 tác vụ đồ họa, 1.797 tác vụ âm thanh.
`gfx-probes/boot-3` của máy chủ đồ họa hoàn thành 600 VI và xuất ra 5 hình ảnh GPU;
Đoạn đầu tiên của lời mở đầu công khai của `start-1/present-420.png` giống với đoạn hiện có
`build/libretro/start-scan/screenshots/frame-000900.png` có cùng nội dung. Các pixel đầu ra của cả hai
Tỷ lệ là khác nhau. Chỉ có cảnh/văn bản tương ứng thu được bằng cách xem trực tiếp mới được ghi lại ở đây.

## So sánh tác vụ và vi mã âm thanh

Vi mã khởi động quan sát được nằm trong ROM `0x4DEA0`/RAM `0x800C34B0`, kích thước `0xD0`.
SHA-256 của nó là
`5759e9bb21f2e504bfbb3e5b75173cb81aa50c60b19e77bcee1d0f6fc34e8fa4`.
khởi động sẽ tải `0xF80` byte vào IMEM `0x1080`; âm thanh OSTask `ucode_size=0`
Không có nghĩa là không có vi mã. Tác vụ đồ họa trỏ tới ROM `0x4DF70`, có dữ liệu hiển thị F3DEX fifo 2.08.

Tiền tố thực thi âm thanh nằm trong ROM `[0x4F300, 0x50120)`, dài `0xE20`, SHA-256 là
`14e3b245e8cd4e0bdf4cbb864af82d1ccba6d3d3ff33f73cb52c5821a76f30fc`.
Ở vòng đầu tiên, phần cuối bị cắt nhầm ở `0xE10` và trình biên dịch máy chủ phát hiện ra rằng `L_1E94` bị thiếu; sau khi kiểm tra khe trễ và nhảy đuôi
Đã sửa thành `0xE20`. Dữ liệu CPU tiếp theo cũng được đọc vào IMEM khi khởi động, nhưng tác vụ hiện tại không thực thi nó.
Sự khác biệt 24 byte trong khối `0xF80` đầy đủ trong quá trình thu thập sớm bắt đầu ở mức tương đối `0xE21`, với các tiền tố thực thi nhất quán;
Sự khác biệt này không được coi là vi mã tự sửa đổi.

Bảng nhảy lệnh âm thanh nằm trong dữ liệu vi mã `+0x10`, tương ứng với 16 nửa từ của ROM `0x59ED0`.
`audio-probe.toml` Ghi lại rõ ràng các mục tiêu nhảy gián tiếp này; kiểm tra xem các giá trị trong ảnh chụp nhanh có giống nhau hay không trước khi phát lại.
Thử nghiệm âm thanh bằng cách sử dụng vectơ RSP thực và trình trợ giúp DMA của N64ModernRuntime. Chỉ khi tạo mã
Giao diện ghi DMA thêm một người quan sát, giữ lại hành vi ghi ban đầu và ghi lại phạm vi đích.

So sánh luồng: Dừng ở mục nhập âm thanh `osSpTaskLoad` → Lưu mô tả với đầu vào 8 MiB →
Tiếp tục đến mục `osSpTaskLoad` liên tiếp tiếp theo → Kiểm tra trạng thái SP và lưu bộ nhớ tham chiếu →
Thiết bị phát lại cùng một đầu vào → so sánh tất cả các phạm vi đích DMA đã ghi.
Trạng thái SP của mẫu này là `0x243` và tất cả 117 lần viết lại đều nhất quán. Theo dõi `female-map-audio-1`
PCM gốc đã được xuất qua SDL và người dùng xác nhận rằng buổi thử giọng mở đầu là bình thường. BGM hoàn chỉnh, hiệu ứng âm thanh chiến đấu khác nhau,
Thời gian phát lại và tốc độ mẫu/trộn mẫu dài vẫn cần được đề cập một cách độc lập.

## Lối vào có thể chạy lại

```sh
# 隔离的固定版本分析工具；首次需要网络及本机 clang/cmake/ninja。
make recomp-bootstrap

# 静态装载范围与按段的函数候选。
make recomp-layout
make recomp-scan

# 全部资源的真实 MIPS → C → arm64 对照。
make recomp-lz

# 带系统符号复核、overlay 地址查找和明确 unsupported 诊断入口的 CPU 生成。
make recomp-cpu

# 编译完整 CPU 宿主并运行；目录必须新建，图形仍为任务记录器。
python3 tools/recomp/run/run_host_probe.py \
  --output build/recomp/host-probes/new-boot --vis 600

# 图形依赖与可选的运行时 Metal 源码编译适配；只改变 build/ 下的固定克隆。
python3 tools/recomp/toolchain/prepare_rt64.py
python3 tools/recomp/run/run_host_probe.py --graphics \
  --input config/recomp/inputs/start-scan.json \
  --output build/recomp/gfx-probes/new-start --vis 960
```

ares sử dụng bản sao cơ sở của `build/recomp/runtime/srw64-jp.z64` và các cài đặt độc lập, việc lưu tệp sẽ không
Được viết bên cạnh `rom.z64` gốc. Hành vi nền sử dụng `Input/Defocus=Block`, cho phép mô phỏng tiếp tục mà không cần
Nhận tổ hợp phím nền. Tín hiệu gỡ lỗi `S10` chỉ cho phép tiếp tục xử lý ngoại lệ ban đầu trên các hướng dẫn COP1 đã được kiểm tra;
Các trường hợp ngoại lệ không mong muốn khác sẽ không thành công và được ghi lại.

```sh
# 输出目录必须尚不存在；--already-halted 仅用于等待 GDB 的冷启动状态。
python3 tools/recomp/probes/rsp_capture.py \
  --session build/recomp/runtime/session.json \
  --output build/recomp/captures/new-memory

python3 tools/recomp/toolchain/analyze_layout.py \
  --capture build/recomp/captures/idle-8mb \
  --output build/recomp/layout-observed.json

python3 tools/recomp/probes/capture_rsp_tasks.py \
  --session build/recomp/runtime/session.json \
  --output build/recomp/captures/new-audio-task --count 6 \
  --snapshot-first-type 2 --snapshot-following-task

.venv/bin/python tools/recomp/probes/run_audio_probe.py \
  --capture build/recomp/captures/new-audio-task \
  --output build/recomp/audio-probe/new-audio-task
```

Bằng chứng chính tại địa phương (tất cả đều bị bỏ qua `build/`):

| con đường | nội dung |
| --- | --- |
| `recomp/toolchain-build.json` | Gửi công cụ, trình biên dịch, phần phụ thuộc và băm nhị phân |
| `recomp/captures/init-entry-2/` | Khởi tạo thanh ghi mục nhập và một phần của RDRAM |
| `recomp/captures/lz-first-call-3/report.json` | Cuộc gọi giải nén trong trò chơi và so sánh đầu ra |
| `recomp/lz-probe/report.json` | Kết quả gốc cho 6.436 tài nguyên |
| `recomp/captures/idle-8mb/` | 8 bộ nhớ thời gian chạy MiB và băm |
| `recomp/layout.json` | Tải các hàm, phạm vi, hàm băm, lệnh gọi bên ngoài so với ảnh chụp nhanh hiện tại |
| `recomp/cpu-scan/report.json` | 3.526 lệnh quét phân đoạn ứng cử viên và kết quả |
| `recomp/cpu-bound/report.json` | Liên kết hệ thống, băm tệp được tạo, điều chỉnh cuộc gọi lớp phủ và các bảng kê khai không được hỗ trợ |
| `recomp/host-probes/boot-2/` | Kỷ lục về lỗi đọc phần cứng AI sau khi vào chuỗi trò chơi lần đầu tiên |
| `recomp/host-build/boot-2-debug.log` | Vị trí lỗi truy cập gốc được LLDB ghi lại |
| `recomp/host-probes/boot-3/` | Chạy thành công và số lượng nhiệm vụ là 600 VI; ảnh chụp nhanh bộ nhớ chỉ dành cho chẩn đoán |
| `recomp/host-probes/boot-4/` | 1.800 VI chạy liên tục và đếm nhiệm vụ |
| `recomp/gfx-probes/boot-3/` | Mở hình ảnh GPU và báo cáo chạy đầy đủ |
| `recomp/gfx-probes/start-1/` | Bắt đầu phát lại và mở đầu màn hình đầu tiên |
| `recomp/gfx-probes/prologue-1/` | Nhấn A để chuyển sang màn hình GPU của phần mở đầu công khai thứ hai |
| `recomp/captures/rsp-tasks-idle-2/` | 24 tác vụ đồ họa/âm thanh và mẫu vi mã |
| `recomp/captures/audio-differential-1/` | Ảnh chụp nhanh ranh giới tải đầu vào và tải tiếp theo của cùng một tác vụ âm thanh |
| `recomp/audio-probe/differential-1/report.json` | 117 so sánh phạm vi DMA cho các tác vụ âm thanh gốc |

## Bước tiếp theo và ngưỡng hoàn thành

1. Tiếp tục xem xét tình huống và khả năng tương thích của hệ thống. Xây dựng, biên dịch gốc và một lần chạy liên tục đã trôi qua; yêu cầu xác minh
Chuyển đổi lớp phủ cùng một trang, các cuộc gọi gián tiếp, các đường dẫn toàn hệ thống và sau khi bắt đầu.
2. Tiếp tục so sánh bối cảnh RT64 và nâng cao bản đồ và trận chiến. Lựa chọn nhân vật chính, đặt tên, mở tuyến và âm thanh mở đầu đã được
Thu thập bằng chứng; GPU, đầu vào và đầu ra của thiết bị âm thanh cần phải che chắn đường chiến đấu.
3. Mở rộng ngôn ngữ, kịch bản mục tiêu và chấp nhận lưu trữ hồ sơ JP thống nhất; giữ cho mỗi loại bằng chứng độc lập.

Tự động hóa chịu trách nhiệm lấy mẫu, phân tích, tạo, biên dịch, phát lại và so sánh; giữ lại danh tính đầu vào, lệnh,
Trạng thái và nhật ký, sau đó chuyển sang các khoảng trống cụ thể. Thế hệ thành công, các thành phần đang chạy, bối cảnh mục tiêu và toàn bộ trò chơi lần lượt được hoàn thành.
ghi lại. Tỷ lệ phần trăm hoàn thành tổng thể hiện không được báo cáo và các vòng lặp có thể chơi được cũng không được thay thế bằng số chức năng.