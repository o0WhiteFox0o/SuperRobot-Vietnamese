> **Ngôn ngữ / Language:** [Tiếng Việt](enemy-cycle.vi.md) · [English](enemy-cycle.en.md) · [中文](enemy-cycle.md)

# Bản đồ chiến thuật: L2/R2 chuyển máy bay địch

25-09-2026 Yêu cầu của người dùng: Sử dụng L2 và R2 để vượt qua máy bay địch trên chiến trường giống như máy bay chiến đấu hiện đại. L/R (và Z) ban đầu đã chuyển đổi giữa các đơn vị không hoạt động của chúng tôi và ở đây chúng tôi điền vào đơn vị của kẻ thù. Nó được triển khai trong [`enemy_cycle.cpp`](../../src/host/enemy_cycle.cpp) và có thể tìm thấy danh sách khóa trong [Steam Deck Keys](../design/steam-deck-controls.md).

## Hoạt động

- Khi bản đồ ở chế độ chờ (không mở menu đơn vị, không chọn lưới): **R2** đặt con trỏ lên xác kẻ địch tiếp theo, **L2** đặt con trỏ lên kẻ địch trước đó. Nhấn giữ để bắn từng loạt: 24 VI, tiếp theo là một VI cho mỗi 8 VI.
- Nếu con trỏ ban đầu ở trên máy bay địch, hãy đếm tiến hoặc lùi từ nó; nếu con trỏ không ở trên bất kỳ máy bay địch nào, R2 bắt đầu từ chiếc đầu tiên, L2 bắt đầu từ chiếc cuối cùng và chu kỳ bắt đầu từ đầu đến cuối.
- Thứ tự là danh sách: đầu tiên là địch (Faction 1) 30 slot, sau đó bên thứ ba (Faction 2) 30 slot, chỉ những ai trên bản đồ mới được tính (byte trạng thái là 1).
- Các thao tác sau khi đặt con trỏ giống như ban đầu: nhấn A để xem nội dung (khả năng, phạm vi di chuyển, v.v.), tương tự như sử dụng các phím định hướng để di chuyển con trỏ.
- Nó không hoạt động khi nhấn hai nút kích hoạt cùng lúc và cửa sổ cài đặt đang mở. L2 và R2 là khóa máy chủ và không thể nhìn thấy trong trò chơi; chúng có những cách sử dụng khác trong hội thoại (tự động đọc L2, tua đi nhanh R2).

Hiện tại, chỉ có thể sử dụng bộ điều khiển và không có phím tương ứng trên bàn phím.

## Cách tạo phiên bản gốc (phân tích tĩnh)

`load_000AB160_func_801C8B04` trong mã được tạo `build/recomp/cpu-bound/generated/funcs_32.c` là chức năng của từng khung hình ở trạng thái không hoạt động của bản đồ chiến thuật (trạng thái chính 5, bảng trạng thái `0x80217E0C`):

| Bước | Hướng dẫn |
| --- | --- |
| Kích hoạt | Đọc các từ liên tiếp `D_801612E0 & 0x2030` (Z, L, R); nếu không phải là 0, hãy chuyển đổi, nếu không thì xử lý hướng (`801C66E8`), A, B, v.v. |
| Danh sách | Duyệt qua danh sách của chúng tôi `0x8015E100 + 槽×0x14` (30 vị trí): Byte trạng thái `+0` = 1. Phi công (`+0xC` nội dung → `+0x38`) `+0x35` không phải là 0, `+1 & 0x80` là 0 (không có hành động); `801E514C(阵营, 槽)` xử lý |
| Vị trí hiện tại | `801C2BFC()` là phần điều khiển dưới con trỏ, tìm chỉ số dưới của nó trong danh sách có `0x80172EDF`; Z hoặc L giảm một, R tăng một, vòng lặp ngoài giới hạn |
| Đặt con trỏ | Tọa độ đối tượng `0x800FFA74 + 句柄×0xC4` (`+0`, `+4`, f32 pixel bản đồ) tương ứng với tay cầm được ghi vào con trỏ `0x80102308/0C` và đích `0x80172EB4/B8`; `801FFE34(x, y)` được đánh giá có ở trên màn hình hay không, `801FFCB0(x, y)` Di chuyển camera |
| Hiệu ứng âm thanh | Chơi lại từ đầu `8007E8A8(0xB9)` |

`801E514C` chỉ thay thế trại và ô bằng tay cầm: trại 0/1/2 lần lượt là `0x42`/`0x60`/`0x7E` cộng với số ô. Danh sách `0x258` byte mỗi trại.

## Phương thức tiếp quản

- `NATIVE_HOOKS` đổi tên `801C8B04` thành `srw64_original_map_idle` và bao bì của [`game_hooks.cpp`](../../src/host/game_hooks.cpp) trước tiên sẽ hỏi móc `map_idle`. Nếu `NATIVE_HOOKS` bị thay đổi, hãy chạy lại `make recomp-cpu`.
- Trong khung khi vừa nhấn cò (hoặc giữ cho đến thời điểm chụp), máy chủ sẽ đặt con trỏ như trong phiên bản gốc: đầu tiên phát 0xB9, ghi con trỏ và mục tiêu, camera sẽ chỉ di chuyển khi thân máy rời khỏi màn hình, khi đó chức năng ban đầu sẽ không chạy trong khung này. Các khung khác chạy nguyên trạng và các hướng A, B, L, R không bị ảnh hưởng.
- Kẻ địch và bên thứ ba đều không nhìn vào vị trí hành động, cũng như `+0x35` của người lái xe (hai mục này chỉ có ý nghĩa với chúng tôi).
- Việc con trỏ đã ở trên cơ thể kẻ thù hay chưa được đánh giá theo tọa độ (sự khác biệt nhỏ hơn nửa lưới) và `801C2BFC` không được gọi.
- Nhật ký: `enemy-cycle-events.jsonl`, mỗi dòng một bước (hướng, trại, vị trí, tay cầm, tọa độ, số lượng kẻ thù). Giao diện gỡ lỗi `status` có `enemy_cycle` (số bước và bước cuối cùng).

## Xác minh

Nó chưa được chạy trên máy thật. Cách chuẩn bị:

- Giao diện gỡ lỗi thêm phương thức `pad` và `srw64ctl pad` (nhấn tên phím Deck, chẳng hạn như `srw64ctl pad r2 r2 l2`), để bạn có thể nhấn L2 và R2 trên Mac mà không cần sử dụng bộ điều khiển thực.
- Ở cấp độ nhỏ có nhiều kẻ thù: nhấn R2 liên tục để vượt qua tất cả kẻ thù và cuối cùng quay lại kẻ địch đầu tiên; L2 đảo ngược; camera theo dõi kẻ thù khi nó ở ngoài màn hình; nhấn A bằng con trỏ vào kẻ thù để mở chế độ xem kẻ thù ban đầu; nhấn và giữ R2 để bắn liên tục.
- Suy luận tĩnh cần xác nhận: tọa độ đối tượng của phần xử lý bên thứ ba (trại 2) cũng nằm trong bảng đối tượng; khi byte trạng thái của kẻ địch là 1 thì nó phải có trên bản đồ và có thể được trỏ bằng con trỏ.