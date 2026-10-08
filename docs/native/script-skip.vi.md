> **Ngôn ngữ / Language:** [Tiếng Việt](script-skip.vi.md) · [English](script-skip.en.md) · [中文](script-skip.md)

# Bỏ qua cốt truyện ngắn (R + START)

2026-09-29. "Bỏ qua ngắn" trong chiến đấu máy hiện đại: Nhấn R + START (Bàn phím E + Enter, Steam Deck R1 + Menu) trong khi đối thoại cốt truyện. Kịch bản cốt truyện sẽ được thực thi trực tiếp đến điểm dừng tiếp theo. Đoạn hội thoại ở giữa sẽ không được hiển thị và phần chờ và biểu diễn sẽ không được phát. Tất cả các lệnh vẫn được thực thi bởi chức năng xử lý ban đầu, do đó, kết quả của cờ, biến, quỹ, diện mạo và chuyển động của đơn vị cũng như chuyển đổi bản đồ đều giống như đọc chúng từng câu. Nhấn B hoặc bật phát lại sẽ dừng bạn ở vị trí hiện tại. Mã: `skip_begin`/`skip_polls` của [script_skip.hpp](../../src/host/script_skip.hpp), [game_hooks.cpp](../../src/host/game_hooks.cpp), việc bắt đầu và dừng do [trình đọc hội thoại](native-dialogue-ui.md) ([native_dialogue.cpp](../../src/host/native_dialogue.cpp) xử lý).

Việc bỏ qua trước đó chỉ cho phép người đọc xác nhận một trang cho trình phát trong mỗi khung hình và tập lệnh được thực thi ở tốc độ ban đầu. Có rất nhiều màn trình diễn, cảnh quay và sự chờ đợi. Nó trông giống như chuyển tiếp nhanh với các dòng nhấp nháy suốt (đoạn bản đồ thế giới trong tập đầu tiên dài khoảng 14 giây). Đoạn tương tự hiện đã được hoàn thành trong 2 VI.

## Hợp đồng thăm dò kịch bản (phân tích tĩnh)

Công cụ sự kiện nằm trong `8015F950` và ngữ cảnh nằm trong `+0x948` (sau đây gọi là vm). Mỗi khung `8009E180` gọi `8009EFDC(engine, vm)` một lần khi một sự kiện đang diễn ra và ghi giá trị trả về vào `engine+0x97C`.

- `8009EFDC`: Khi trạng thái lệnh `vm+0x24` là 0 thì gặp sự kiện kết thúc `FFFF` (trạng thái 0x80); mặt khác, `8009F0E8` xử lý điều kiện và dấu lộ trình, đồng thời `8009EED0` tìm nạp lệnh (PC chỉ tiến lên 2 byte, chức năng xử lý ghi `vm+0x30` và trạng thái được đặt thành 1). Nếu trạng thái khác 0, hàm xử lý sẽ được gọi; sau cuộc gọi, trạng thái được thay đổi từ 1 thành 2. Nhiều nhất một cuộc thăm dò được thực hiện và chức năng xử lý được gọi một lần.
- Trình xử lý thực hiện công việc riêng của nó: xóa trạng thái về 0 và đẩy PC qua các tham số. `+0x26`, `+0x28`, `+0x2A`, `+0x2E` là các trường cục bộ của chúng và bị xóa khi tìm nạp hướng dẫn.

Vì vậy, để bỏ qua, chỉ cần tiếp tục bỏ phiếu trong cùng một khung: lấy cái tiếp theo ngay khi lệnh hoàn thành.

## Luyện tập

1. Trình đọc phát hiện R + START (`Reader::update`) và hiện tại có một tập lệnh đang được đọc, đó là `script_skip::start(vm)`.
2. Trước lần bỏ phiếu đầu tiên của khung tập lệnh này (`skip_begin`): Nếu nó mới bắt đầu, trước tiên hãy gọi `800A34D8` để đóng cửa sổ hội thoại đang đọc (giống như `3D48`). Sau đó, `8008FED4` trực tiếp trả về 3 trong phần bỏ qua, đây là câu trả lời ban đầu của "Trang này đã được đọc" và hộp thoại không mở.
3. Sau mỗi lần bỏ phiếu (`skip_polls`): Lệnh vừa thực hiện dừng ở điểm dừng; nếu lệnh vẫn đang đợi thì nhấn vào bàn để đẩy nó về điểm cuối và thăm dò lại. Khi gặp lệnh không giải được thì bỏ frame hiện tại và tiếp tục ở frame tiếp theo. Nó sẽ hoàn thành phần này với tốc độ ban đầu.
4. Vẫn có thể xem từng trang bị bỏ qua (`Reader::skipped`). `8008FED4` bị dừng với bảng và số văn bản (a0, a1); máy chủ gọi `8008CE54` ban đầu để đọc số người nói trong tiêu đề bản ghi và tên được lấy từ bản ghi `0x111E 加说话人数字`. Đây chính xác là bản ghi hiển thị trong ô tên gốc (`8008F648` được gọi là `8008D0E8` với số bảng gốc `+0x20C` cộng với 0x111E), do đó nhân vật chính và đối tác số 25–32 cũng được hiển thị dưới dạng tên người chơi thông qua `record_text`. Lưu một bản sao của văn bản và tên cho mỗi ngôn ngữ đọc. Sau khi thay đổi ngôn ngữ, bạn có thể đọc lại và thay đổi chúng. Trang bạn đang đọc lúc đầu sẽ bị bỏ qua và không được lặp lại, chỉ những mục đã đọc đầy đủ mới được hoàn thành. Tập 1 Đo lường thực tế: Bốn trang bị bỏ qua của diễn giả (Katz, Katz, Brad, Katz) giống hệt như chính trò chơi thể hiện khi đọc từng câu.
5. Hiệu ứng âm thanh bị tắt trong khoảng thời gian bỏ qua (`8007E8A8`, -1 ngừng phát hành), nếu không các lệnh được thực hiện trong một khung sẽ phát ra cùng lúc; BGM chuyển như bình thường.

| Lệnh | Hàm xử lý | Phương pháp khi hoàn thành khung |
| --- | --- | --- |
| Đối thoại `3D3E`–`3D43` | `8009F654` mỗi 0x1C | Gọi phiên bản gốc lần đầu tiên để dịch chuyển camera đến loa (`80209DAC`, nếu tham số thứ ba khác 0, dịch chuyển tức thời); lần sau `8008FED4` trả về 3 |
| Đợi `3D38` | `800A00F0` | Đặt số `+0x2E` thành 0, cuộc gọi tiếp theo sẽ hoàn thành < 0 |
| Đóng cửa sổ và đợi 32 khung hình `3D47` | `800A013C` | `+0x2E` Đặt thành 0x1F và gọi tới 32 vào lần sau |
| Đóng cửa sổ và để một khung `3D4E` | `800A0468` | Thăm dò một lần nữa để hoàn thành |
| Làm mờ `3D3B` | `8009F948` | Làm mờ bản ghi công cụ 1 (`800FF9E8`): `+C` Độ trong suốt hiện tại được viết dưới dạng mục tiêu `+5`, `+4` được xóa thành 0. Đây chính xác là bước cuối cùng của `8009AD64`; sau đó trình xử lý sẽ tự mở khóa đầu vào `8010F6BA` |
| Rung màn hình `3D36` | `8009F880` | Phán quyết kết thúc `8020D4B0` (bản đồ chiến thuật) / `801C5138` (bản đồ thế giới) Mỗi ​​lần gọi một lần đẩy, cùng một khung sẽ được thăm dò liên tục |
| Ngoại hình `3D45` | `8009FC04` | Chỉ bản đồ chiến thuật: số lượng hai khung 10 được đẩy lên 9; hoạt ảnh ngoại hình `8020C524(0)` được đẩy từng bước một và được thăm dò liên tục. Thân tàu và hoa tiêu được tạo như bình thường bởi `8020B154` |
| Phong trào đơn vị `3D3C` | `800A0360` | Chỉ bản đồ chiến thuật: `8020A788` Chỉ đặt tốc độ (±8 pixel) của đơn vị sprite mỗi lần và vị trí được tích hợp bởi chuyển động của sprite theo từng khung hình `80081BFC`; bỏ phiếu liên tục, gọi `80081BFC` một lần trước mỗi lần. Sau khi vào lưới, `801CBEB8` được ghi lại vào tọa độ danh sách |

"Bỏ phiếu liên tục" cho phép mỗi lệnh được thăm dò tối đa 600 lần trên mỗi khung. Nếu vượt quá giới hạn, khung hiện tại sẽ bị hủy.

Khi `8020C524` được gọi với tham số 1, tất cả các đơn vị sẽ được đặt ngay lập tức thông qua `8020BE34`, nhưng người gọi duy nhất trong phiên bản gốc, `3D45`, chỉ vượt qua 0. Đường dẫn này chưa bao giờ được thực thi nên không được sử dụng.

## Điểm dừng

Bỏ qua kết thúc ở vị trí sau và người đọc quay lại hướng dẫn sử dụng:

- Kịch bản sự kiện kết thúc (`FFFF`);
- Chọn chi `3D44` (`8009FA94`, trang lựa chọn hiện ra như bình thường);
- Lựa chọn tấn công `3D3D`, phân chia chiến thắng theo cấp độ `3D4A`, kết thúc trò chơi `3D4C`, kết thúc `3D71`;
- Chuyển từ bản đồ thế giới sang chiến trường `3D4D` (`800A031C`): Nó chỉ đặt `engine+4` thành 3. Phải mất một vài khung hình để lớp phủ chuyển đổi và tập lệnh tiếp tục gỡ xuống một mục trong khoảng thời gian này. Phiên bản gốc dựa trên 10 khung bắt đầu bằng `3D45` để đợi cho đến khi lớp phủ chiến thuật được cài đặt; việc nén nó sẽ khiến `8020B0D4` của lớp phủ chiến thuật được gọi trong lớp phủ bản đồ thế giới và bị lỗi (đo thực tế). Vì vậy không có khả năng tăng tốc sau `3D4D`;
- Chuyển lớp phủ, thay thế chữ viết, đặt lại hội thoại (điểm dừng gốc của đầu đọc).

## Xác minh

- Kiểm tra thành phần: `make recomp-script-skip-test` ([tests/native_script_skip.cpp](../../tests/native_script_skip.cpp), được sáp nhập vào `recomp-native-check`), bao gồm bảng điểm dừng, nhận dạng chức năng xử lý hội thoại, các trường được viết bởi mỗi lệnh, bản đồ phi chiến thuật không được tăng tốc.
- Máy thực tế: [check_script_skip.py](../../tools/recomp/debug/check_script_skip.py) Trong trò chơi mới (lộ trình của Brad), đoạn hội thoại đầu tiên bị bỏ qua sau khi đọc hai trang và câu đầu tiên của chiến trường cũng bị bỏ qua. Đoạn bản đồ thế giới 2 VI dừng ở `3D4D`, đoạn mở đầu chiến trường (triển khai, bốn `3D3C`, hội thoại) 2 VI thực thi đến cuối tập lệnh và không có đoạn hội thoại nào được hiển thị hai lần. `SRW64_SCRIPT_SKIP_TRACE=1` bản ghi lần lượt bỏ qua các lệnh thực thi; các lệnh được thực thi ở tốc độ ban đầu luôn ghi một dòng `SRW64_SCRIPT_SKIP wait`.
- So sánh trạng thái: [check_script_skip_state.py](../../tools/recomp/debug/check_script_skip_state.py) Chạy liên tiếp hai hiệp, mỗi hiệp nhấn A từng câu để đọc phần mở đầu, bỏ qua hai hiệp trong một hiệp và đi đến bản đồ chiến thuật. Sau khi lượt của chúng tôi không hoạt động, hãy chuyển qua giao diện gỡ lỗi `memory.read` Đọc danh sách, phiên bản đơn vị, phiên bản thí điểm, biến cốt truyện, trường cấp độ (giai đoạn, lượt, bản đồ, cảnh, tiền), bối cảnh sự kiện, danh sách loại trừ xuất kích và bảng quyền làm mẹ: 2026-09-29 Tám khu vực giống hệt nhau từng byte (đọc VI 8222, bỏ qua VI 6496). Không có đơn vị nào dưới con trỏ trong khung hình cuối cùng của hai trò chơi và việc chụp liên tục xác nhận rằng đó là nhấp nháy ban đầu.

## Sự khác biệt chưa được tạo ra và đã biết

- Các lệnh hiệu suất khác (`3D32`/`3D33` quỹ đạo và định vị bản đồ thế giới, `3D35` chặn cuộn, `3D37` hiệu ứng đặc biệt trên lưới, `3D46`/`3D4F` thoát và đánh bại, `3D49` Chiến đấu theo kịch bản, `3D51` vũ khí MAP, `3D55` Tâm linh hiệu suất, `3D50`/`3D5C`/`3D63`/`3D67`/`3D6A`/`3D75` v.v.) vẫn được thực thi ở tốc độ ban đầu; việc thực hiện là chính xác, nhưng phần đó không nhanh. Điền theo thứ tự xảy ra.
- Bỏ qua các khung ít chạy hơn sẽ khiến hai đồng hồ gieo hạt ngẫu nhiên (`8015DC50`, `80172D0C`) khác với việc đọc chúng và việc chọn ngẫu nhiên đường, hình nền, v.v. cho các trận chiến tiếp theo có thể khác. Đã có những khác biệt tương tự trong việc chuyển tiếp nhanh đoạn hội thoại và kết quả trận chiến trong trò chơi này được giải quyết trước khi chiếu.