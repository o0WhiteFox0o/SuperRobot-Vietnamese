> **Ngôn ngữ / Language:** [Tiếng Việt](move-jump.vi.md) · [English](move-jump.en.md) · [中文](move-jump.md)

# Di chuyển khung hình đã chọn: Nhấn và giữ R để nhảy tới khung hình xa nhất

25/09/2026 Người dùng yêu cầu thao tác bổ sung máy bay chiến đấu hiện đại: khi chọn điểm đến di chuyển, nhấn R1 và đánh dấu lưới xa nhất có thể tiếp cận; nhấn hướng trong khi giữ R, con trỏ sẽ nhanh chóng nhảy giữa các lưới này và nhấn A để xác nhận di chuyển. Tham khảo "Super Robot Wars 30": Nhấn R1 khi phạm vi di chuyển được hiển thị và con trỏ nhảy đến phạm vi tối đa ([ナノゲームス TIPS](https://ds-can.com/srw30/system/s_tips.html)).

Được triển khai trong [`move_jump.cpp`](../../src/host/move_jump.cpp). Các địa chỉ bên dưới đều được lấy từ phân tích tĩnh (lớp phủ chiến thuật `load_000AB160`, mã được tạo `build/recomp/cpu-bound/generated/`).

## Hoạt động

- **Giữ R** (Bàn phím E, Bộ điều khiển RB): Xếp một lớp màu vàng ấm ở lưới xa nhất, thở chậm và phạm vi không vượt quá lưới ban đầu. Nếu con trỏ đã rời khỏi đơn vị trước khi nhấn R, nó sẽ nhảy đến lưới xa nhất theo hướng này; con trỏ sẽ không di chuyển khi nó vẫn ở trên thiết bị.
- **Nhấn hướng trong khi giữ R** (D-pad hoặc cần điều khiển, đường chéo cũng hoạt động):
- Con trỏ ở ô xa nhất: nhảy tới ô xa nhất gần nhất trong phạm vi 45° về bên trái và bên phải của hướng này. Giữ hướng và đi dọc theo vòng tròn bên ngoài từng ô vuông một, không bỏ qua các góc; nếu không có ai trong phạm vi này, chỉ cần lấy người có độ lệch ít nhất ở phía trước.
- Con trỏ không ở ô xa nhất: Nhảy tới ô xa nhất theo hướng này tính từ đơn vị.
- Di chuyển theo nhịp điệu riêng của trò chơi trong khi giữ hướng: nhấn để di chuyển ngay một khung hình và cứ 3 khung hình sau 12 khung hình.
- **A／B**: Xác nhận và hủy như bình thường, có lỏng hay không thì như nhau. Nhả R, phần đánh dấu biến mất, con trỏ giữ nguyên vị trí cũ và các phím mũi tên tiếp tục chuyển động theo từng khung hình ban đầu.

## "Lưới xa nhất" là gì

Trong số các ô mà đơn vị có thể dừng lại, không có con đường ngắn nhất nào đi qua nó và dẫn đến một ô khác mà đơn vị có thể dừng lại. Đường dẫn ngắn nhất được tính toán dựa trên chi phí đầu vào của từng lưới trong lưới, nhất quán với `801C3B0C` của biểu mẫu ban đầu.

- Mặt đất bằng phẳng là vòng tròn bên ngoài của dãy; sự kết thúc của một ngõ cụt cũng được tính.
- Khi phạm vi chạm vào mép bản đồ thì chỉ tính 2 đầu của đường.
- Các lưới chỉ bị chặn bởi các hồ và lực lượng thiện chiến ở một bên không được tính: bạn có thể tiến xa hơn bằng cách đi xung quanh chúng.

## Cách tạo phiên bản gốc (phân tích tĩnh)

| Mục | Địa chỉ | Mô tả |
| --- | --- | --- |
| Phân phối trạng thái trên mỗi khung hình | `801DFBD0` | Bảng `0x80217E0C[状态]`, byte trạng thái trong `0x80172EB0`. Sau đó gọi `801C3020` (đơn vị dưới con trỏ), `80081BFC` (tốc độ đối tượng), `801FFADC` (theo sau ống kính) |
| Trạng thái 0xC | `801CD6E4` | Kiểm tra bảng `0x80217B38` theo tiểu bang `0x80172EB2`: 0 lựa chọn `801CBB04`, 1 đơn vị đi bộ `801CC290`, 2 `801CC72C`, sau 3–6 |
| Lựa chọn | `801CBB04` | A xác nhận, B hủy (âm 0xB8, con trỏ quay về điểm neo, trở về trạng thái 8), gọi hướng `801C66E8`→`801C63D8`, nhấn và giữ C xuống/C sang trái để tăng tốc chuyển động. **R, L, Z và START không được đọc ở trạng thái 0xC và 6** |
| Nhập từ | `D_80178A08` Nhấn khung này, nhấn `D_800F97D0` và giữ, `D_801612E0` bật | Một từ rưỡi mỗi miệng, cần điều khiển được tích hợp vào phím chéo. A 0x8000, B 0x4000, R 0x10, trên 0x0800, dưới 0x0400, trái 0x0200, phải 0x0100 |
| Con trỏ | `0x80102308`/`0C` | pixel bản đồ f32, bằng lưới × 16+32 (đối tượng 0x35); mục tiêu `0x80172EB4`/`EB8`, tốc độ `0x8010232C`/`30` |
| Ống kính | `0x8010F5D4`/`D8` | Số nguyên, tọa độ màn hình = tọa độ bản đồ + offset. `801FFCB0(px,py)` Di chuyển điểm đến giữa màn hình: x offset = kẹp(152−px, 320−chiều rộng bản đồ, 0), y offset = kẹp(112−py, 240−chiều cao bản đồ, 0); `801FFE34` xác định xem điểm có nằm trong [32,288]×[32,208] |
| Kích thước bản đồ | `0x80172EC4`/`EC8` | Điểm ảnh |
| Phạm vi di chuyển | `0x80227BD0` | Lưới 31×31 tập trung vào đơn vị, được lưu thành hàng, đơn vị ở mức (15,15): 2 có thể dừng lại, 3 chỉ có thể đi qua nếu có quân đồng minh và trung tâm là 0. Chi phí tham gia tại `0x80227328` |
| Phạm vi vẽ | `801E4760` | Gọi lại nút 0x2E (đăng ký `801CB9B0`), a0 = `Gfx**`. Giả sử bộ kết hợp là màu nguyên thủy, không có kết cấu, màu nguyên thủy (0,192,0,96), mỗi lưới có giá trị 2 là G_FILLRECT 16×16; góc trên bên trái = điểm neo + độ lệch camera + (lưới −15) × 16 |
| Xác nhận | Nhánh A của `801CBB04` | `801E0B94(2, 光标x, 光标y)` Kiểm tra xem ô con trỏ có phải là 2 hay không; nếu không thì nó sẽ buzz 0xBA, nếu có thì nó sẽ báo ngay cả khi đường dẫn và đơn vị đã đi qua |

Trong phiên bản gốc, khi con trỏ được đặt ở đâu đó (`801C8E20`, đơn vị chuyển đổi, v.v.), cùng một đoạn sẽ được nội tuyến: con trỏ và mục tiêu được viết cùng nhau. Nếu điểm không nằm trong màn hình, `801FFCB0` sẽ được gọi và ký hiệu con trỏ 0xB9 sẽ được phát. Thực hiện tương tự cho các tab trong khi giữ phím R.

## Phương thức tiếp quản

- `NATIVE_HOOKS` bao bọc hai hàm ([`game_hooks.cpp`](../../src/host/game_hooks.cpp)):
- `801CBB04` đã được đổi tên thành `srw64_original_move_select`.
- `801E4760` đã được đổi tên thành `srw64_original_move_range_draw`.
- Sau khi thay đổi `NATIVE_HOOKS`, hãy chạy lại `generate_cpu.py`.
- **Lựa chọn ô**: Khi nhấn R và không nhấn A hoặc B trong khung này, máy chủ sẽ xử lý khung này, chức năng ban đầu sẽ không chạy và hướng sẽ không cho phép con trỏ di chuyển từng khung hình (không thể nhập trạng thái 6). Trong các trường hợp khác, nó chạy như phiên bản gốc.
- **Tap Frame**: Cách thực hiện giống như đoạn gốc đặt con trỏ và điều kiện di chuyển camera về giữa cũng giống.
- **Đánh dấu**: Sau khi hoàn thành phạm vi vẽ ban đầu, thêm màu nguyên thủy (màu vàng ấm, alpha 72–128, nhấn VI để thở) và khung xa nhất G_FILLRECT sau cùng danh sách hiển thị và cắt nó ra màn hình. Chế độ hòa trộn tuân theo các cài đặt của phạm vi vẽ ban đầu.
- **Tính toán lại thời gian**: Nếu điểm neo thay đổi (đơn vị được thay đổi), nếu thả R rồi nhấn thì lưới xa nhất sẽ được tính toán lại.
- **Nhật ký**: `move-jump-events.jsonl`, ghi lại các sự kiện bật, tắt và nhảy.

## Xác minh máy thực tế

Cấp độ kiểm tra [`move-jump.json`](../../config/recomp/mini-stages/move-jump.json): Bản đồ 20, タケル ở mức (8,8), ダンバイン thân thiện ở mức (10,8), kẻ thù ở mức (15,12). Kiểm tra tập lệnh [`check_move_jump.py`](../../tools/recomp/debug/check_move_jump.py) Bằng cách gỡ lỗi thao tác bàn phím (E là R), hãy kiểm tra 10 mục sau:

1. Nhập vào ô lựa chọn;
2. Nhấn và giữ R để hiển thị lưới xa nhất và con trỏ sẽ không di chuyển;
3. Những điểm nổi bật được rút ra;
4. Nhấn phải để nhảy tới lưới ngoài cùng bên phải;
5. Nhấn xuống hai lần để đi dọc theo vòng tròn bên ngoài;
6. Nhấn và giữ nút chụp trái;
7. Điểm nổi bật biến mất sau khi nhả R;
8. Các phím định hướng tiếp tục di chuyển từng khung hình;
9. Nhấn và giữ R lần nữa để nhảy ra theo tia;
10. Nhấn A trong khi giữ R. Thiết bị sẽ di chuyển tới và menu sau di chuyển sẽ xuất hiện.

Kết quả (`build/recomp/debug/20260925T103341.713940Z/`):

- Cả 10 đều đậu.
- Phạm vi của ガイヤー là một hình thoi có bán kính là 6, ô xa nhất đúng bằng 24 ô tính từ vòng tròn bên ngoài.
- Trong khi nhấn trái, di chuyển dọc theo vòng tròn bên ngoài từng ô vuông đến ô vuông ngoài cùng bên trái, cũng đi qua góc dưới cùng. Khi chạy lần đầu, đường thẳng được ưu tiên và bỏ qua góc dưới. Nó đã được thay đổi thành giá trị gần nhất trong vòng 45°.
- Điểm nhấn là màu vàng ấm trong mờ, chồng lên lưới xanh nguyên bản mà không vượt quá lưới.

Không được bảo hiểm:

- Lưới xa nhất khi địa hình chặn đường (hồ, núi): phạm vi của cấp độ này là một viên kim cương hoàn chỉnh.
- Camera shift khi nhảy ra khỏi màn hình: toàn bộ phạm vi của cấp độ này đều có trên màn hình.
- Nhấn và giữ hướng trước (con trỏ đã di chuyển, trạng thái 6) rồi nhấn R: lúc này nó sẽ không tiếp quản và bạn phải đợi phím định hướng được nhả ra.
- Giữ R trong khi xem phạm vi của kẻ thù (chỉ đọc cờ danh sách): Cũng có thể bỏ qua, nhưng A-shot không hoạt động.