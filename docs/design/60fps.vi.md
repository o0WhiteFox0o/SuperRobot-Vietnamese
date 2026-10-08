> **Ngôn ngữ / Language:** [Tiếng Việt](60fps.vi.md) · [English](60fps.en.md) · [中文](60fps.md)

Nghiên cứu khung #60

**Trạng thái: Đang chờ xử lý, chưa bắt đầu** (Quyết định của người dùng 2026-10-01). Bắt đầu lại với thí nghiệm ở Phần 7.

2026-10-01. Phân tích tĩnh (tháo gỡ vòng lặp chính, tất cả các mã được tạo lớp phủ, RT64 và mã nguồn tối tân, lớp bản vẽ máy chủ), không thay đổi mã, không có máy thật. Bất cứ điều gì được viết là "suy luận" hoặc "chưa được xác minh" phải được xác nhận trong bài kiểm tra ở Phần 7.

## 1. Kết luận

1. **Logic gốc được cố định ở tốc độ 30 khung hình/giây**: cứ 2 VI chạy một khung logic trò chơi và gửi danh sách hiển thị. Giá trị khoảng thời gian chỉ được ghi một lần trong toàn bộ chương trình khi khởi động và không có kịch bản nào để thay đổi giá trị đó.
2. **Việc thay đổi logic thành 60 là không khả thi**: Tất cả các bước chờ, hoạt ảnh và cuộn đều được tính theo khung. Thay đổi khoảng thời gian thành 1 sẽ tăng gấp đôi tốc độ của toàn bộ trò chơi. (Sản phẩm phụ: đây là công tắc tốc độ gấp 2 lần toàn cầu được tạo sẵn, xem §2.1.)
3. **Điều khả thi là hiển thị các khung hình nội suy**: logic vẫn là 30, RT64 vẽ thêm một vài khung hình giữa hai khung hình theo tốc độ làm mới màn hình. RT64 đi kèm với khả năng này và máy chủ hiện tắt tính năng này (`RefreshRate::Original`).
4. **Chèn khung chỉ hợp lệ đối với bản vẽ ma trận 3D**. Tác phẩm này được chia thành hai loại theo cảnh:
- Có khả năng cao là nó sẽ có sẵn ngay lập tức: nội dung và các hiệu ứng đặc biệt của chương trình chiến đấu (một hình tứ giác với MODELVIEW LOAD một lần trên mỗi nút), mặt đất 3D, mô hình bản đồ thế giới và văn bản thu phóng của tiêu đề và phần mở đầu. Bản vẽ chủ của sơ đồ thân HD và mô hình HD đã đọc ma trận nội suy của RT64 và sẽ được kích hoạt cùng nhau.
- Hoàn toàn bất động: mọi thứ VĂN BẢN - ô xếp, đơn vị, con trỏ, cuộn để tìm bản đồ chiến thuật, lớp bầu trời cho các trận chiến, hình nền, hình đại diện, HUD, hội thoại. RT64 không khớp với hình chữ nhật.
5. **Bản đồ chiến thuật muốn có 60 khung hình nhất lại là loại không di chuyển**. Cần thêm bản vá "nội suy các hình chữ nhật được đánh số" vào RT64 (hoặc thay đổi hình chữ nhật của lớp bản đồ thành hình tứ giác trực giao). Đây là phần công việc lớn nhất trong toàn bộ sự việc.
6. Giao diện (trang RmlUi, thanh hội thoại) do chính máy chủ vẽ ra sẽ được hiển thị và vẽ một lần trong hook kết xuất; bây giờ nó chỉ được hiển thị 30 lần mỗi giây. Khi bật nội suy khung, số lượng bài thuyết trình sẽ theo màn hình. Hoạt ảnh chuyển tiếp của các giao diện này có thể đạt tới 60/90/120 mà không thay đổi.

Thứ tự đề xuất: trước tiên hãy thêm công tắc thử nghiệm vào máy thực tế để xem hiệu ứng mở hộp (nửa ngày) → đánh số các nhóm ma trận theo số vị trí nút cho chương trình chiến đấu/bản đồ thế giới/tiêu đề và xử lý cắt gương (vài ngày) → nội suy hình chữ nhật của bản đồ chiến thuật (tối đa).

## 2. Nhịp khung gốc

| Địa chỉ | Chức năng |
| --- | --- |
| `80080838` | Lập kế hoạch chủ đề. Thông báo `0x29A` (VI truy xuất): Điều chỉnh cọc `80085F30`, `D_80172D0C`+1, `D_8015DC50`+1, sau đó `80080A14`. `0x29B`/`0x29C` là hoàn thành SP/DP, `0x29D` là PreNMI |
| `80080600` | Tạo chuỗi lên lịch, `osViSetEvent(队列, 0x29A, 回扫数)`; số truy tìm được người gọi chuyển vào và số ngay lập tức không bị bắt. Nó được suy ra 1 từ 30 khung hình được đo (suy luận) |
| `8007F9A0` | Vòng lặp chính của chuỗi trò chơi, mỗi khi nhận được tin nhắn loại 1, hãy truy cập `8008163C` (được suy ra là một truy xuất được chuyển từ chuỗi lập lịch) |
| `8008163C` | Đọc bộ điều khiển mỗi lần và tích lũy (`80087A48`, `80087AA4`); **`D_80172D0C < D_8010F0C8` sẽ trả lại **; nếu không, hãy xóa số lượng, đếm các cạnh chính và chạy chức năng khung của cảnh hiện tại `D_8015DC7C` |
| `8007FC48` | Khởi tạo khi bật nguồn, **`D_8010F0C8 = 2`** |

- Tìm kiếm quyền truy cập vào `8010F0C8` trong tất cả mã được tạo (`build/recomp/cpu-bound/generated`, phần lưu trú cộng với tất cả lớp phủ): một lần ghi (`8007FC64`), một lần đọc (`80081660`), không có quyền truy cập qua con trỏ địa chỉ cơ sở. Vì vậy, khoảng thời gian luôn là 2, logic luôn là 30 khung hình và sẽ thấp hơn khi khung hình bị loại bỏ.
- Phù hợp với số đo thực tế: màn hình tiêu đề được ghi trong 8 giây để thu được 240 khung hình ([debug-interface.md](../guide/debug-interface.md)); chỉ số tốc độ khung hình (`frame_rate.hpp`) tính danh sách hiển thị được gửi mỗi giây.
- Mỗi VI của bộ điều khiển đọc và OR thành các từ tích lũy, do đó lấy mẫu đầu vào là 60 Hz và mức tiêu thụ là 30 Hz ([origin-controls.md](../gameplay/original-controls.md)).
- `80085F30` là một sơ khai trống được mỗi VI gọi một lần (ban đầu có thể là để quản lý hiệu suất). Máy chủ coi nó như một "ranh giới khung" và treo một loạt móc (`game_hooks.cpp`). Nói cách khác, máy chủ đã có nhịp 60 Hz, nhưng logic trò chơi chỉ thay đổi nhịp đó theo từng nhịp khác.

### 2.1 Tại sao logic không thể thay đổi thành 60?

Sau `D_8010F0C8 = 1`, mỗi VI chạy một khung logic. Việc chờ đợi trong trò chơi ("đợi 20 khung hình" và "độ trễ 30 khung hình"), các bước hoạt ảnh, bước cuộn và hệ số tiếp cận camera 1/8 đều được mã hóa cứng theo khung hình. Không có khái niệm về bước thời gian và kết quả là tốc độ toàn cầu tăng gấp đôi. Việc giảm một nửa kích thước bước theo từng bước tương đương với việc viết lại tất cả các lớp phủ, bất kể.

Sản phẩm phụ: Đây là **tốc độ gấp 2 lần toàn cầu** không di chuyển VI và đồng hồ âm thanh (suy luận, không thực tế). Chuỗi âm thanh tự gửi lại tin nhắn quét, tốc độ âm nhạc không thay đổi và kích hoạt hiệu ứng âm thanh được tăng gấp đôi; hai đồng hồ phát sóng không bị ảnh hưởng bởi VI. Kỷ lục trước đó cho rằng “chủ nhà không có bất kỳ phương tiện kiểm soát tốc độ nào” ám chỉ hệ số nhân tốc độ của cực kỳ hiện đại; miếng đệm này là của riêng trò chơi. Nếu bạn muốn "nhấn và giữ tua đi nhanh", bạn có thể thử từ đây, nó không liên quan gì đến 60 khung hình.

## 3. Hiện tại Host xuất hiện như thế nào?

- Luồng VI của Ultramodern được cố định ở tần số 60 Hz (`events.cpp``vi_thread_func`, hằng số nhân tốc độ 1) và mỗi VI xếp hàng đợi cập nhật màn hình cho luồng đồ họa.
- Trò chơi gửi danh sách hiển thị cho mỗi 2 VI → `send_dl` → khối lượng công việc RT64.
- RT64 `updateScreen` chỉ tạo kết xuất (`rt64_state.cpp:1950`) khi nội dung thanh ghi VI hoặc bộ đệm khung thay đổi, tức là 30 kết xuất mỗi giây.
- `graphics.cpp:399`: `refreshRate = RefreshRate::Original`, tốc độ khung hình mục tiêu 0, không khớp khung, không chèn khung.
- Móc hiển thị của máy chủ (`capture_frame`) được điều chỉnh một lần cho mỗi lần hiển thị: màu đen ở cả hai bên, thanh hội thoại, RmlUi (`context->Update()`/`Render()`). Vì vậy giao diện máy chủ bây giờ cũng là 30 khung hình/giây.

## 4. Tính năng chèn khung RT64 hoạt động như thế nào?

Mã nguồn nằm trong `build/recomp/upstream/RT64` (cam kết 4337374 cộng với bản vá dự án này).

- **Switch**: `RefreshRate::Display` (lấy tốc độ làm mới chuỗi hoán đổi, Metal qua `CocoaWindow::getRefreshRate`) hoặc `Manual` (`refreshRateTarget`).
- **Tốc độ khung hình gốc**: `VIHistory::logicalRateFromFactors` - Một số VI đã bị tách ra giữa một vài lần thay đổi màn hình gần đây nhất. Nếu tất cả đều giống nhau thì cho khoảng 60 , nếu không thì cho 0 (không chèn). Khi game ổn định là 30; khi đọc đĩa hoặc chuyển cảnh, nó sẽ tạm thời trở về trạng thái chưa được cắm và sẽ tự động phục hồi sau khi ổn định. Có thể đóng đinh bằng hướng dẫn mở rộng `gEXSetRefreshRate(30)`.
- **Tiền đề**: Bộ đệm khung được trình bày phải là bản đồ màu được vẽ bởi khối lượng công việc này (`interpolationEnabled`, kiểm tra lịch sử VI ở chế độ SkipBuffering mặc định). Công việc này là một bộ đệm đôi thông thường, được cho là đúng nhưng chưa được xác minh.
- **Mỗi khung hình trò chơi được hiển thị N lần** (N=target `origin, 60 Hz là 2, 90 Hz là 3, 120 Hz là 4) và mỗi lần chuyển đổi "khung hình trước → khung hình hiện tại" được nội suy với các trọng số khác nhau, toàn bộ khung hình được vẽ lại, không phải là phép chiếu lại rẻ tiền. Tải GPU được tính bằng N lần.
- **Trùng khớp** (`rt64_game_frame.cpp`):
- Chỉ nhìn hình vẽ theo hai kiểu chiếu: phép chiếu phối cảnh và phép chiếu trực giao; **Hình chiếu hình chữ nhật (TEXRECT/FILLRECT) không tham gia** (chuyển đổi `GameFrame::set` bị bỏ qua trực tiếp).
- Khi không có số rõ ràng (`G_EX_ID_AUTO`): Đầu tiên hãy gộp hàm băm theo lệnh gọi rút thăm. Hàm băm chỉ chứa bộ tổng hợp, OtherMode, chế độ hình học, số tam giác, **không bao gồm kết cấu**; trong nhóm, tính toán sự khác biệt về vị trí, hướng và vị trí màn hình cho tất cả "ma trận hiện tại × ma trận khung trước đó" và khớp chúng một cách tham lam từ nhỏ đến lớn.
- Khi có số rõ ràng (`gEXMatrixGroup…`) thì sẽ ghép theo số đó. Nội suy hoặc bỏ qua có thể được chỉ định thành phần theo thành phần và có thể bật nội suy đỉnh và nội suy UV.
- Ma trận xem/chiếu, cuộn kết cấu (uls/ult của ô), LookAt cũng nội suy.
- **Có gì đó không khớp** Vẽ trực tiếp theo khung hình hiện tại vẫn là 30 khung hình. Sẽ không có lỗi nhưng nó không mượt mà. **Không khớp** sẽ gây ra vấn đề (hai vật trượt về phía vị trí của nhau).
- Độ trễ: Khung được chèn đi trước khung hình hiện tại và chính khung hình hiện tại được hiển thị sau. Ở tần số 60 Hz, nó dài hơn khoảng nửa khung hình trò chơi (17 ms) và điều đó không thành vấn đề trong trò chơi.

## 5. Có thể chèn từng cảnh được không?

| Cảnh | Di chuyển mọi thứ | Phương pháp vẽ | Giải mã kỳ vọng | Những điều cần trang điểm |
| --- | --- | --- | --- | --- |
| Hiệu suất chiến đấu | Cơ thể, hiệu ứng vũ khí, nổ, cut-in | Chế độ 0xE/0xF/0x10: `8008B324` Mỗi nút `DA380003` MODELVIEW LOAD, một nút cho mỗi phần G_QUAD ([battle-animation-rendering.md](battle-animation-rendering.md) §3) | Tích cực. Tuy nhiên, giá trị băm tứ giác của tất cả các phần đều giống nhau và chúng chỉ khớp với nhau theo khoảng cách: đạn dày đặc, ngọn lửa ở đuôi và cụm vụ nổ rất dễ không khớp (cùng nguồn gốc của các vấn đề đã biết trong quá trình biên dịch lại của Mischief Makers) | Đánh số rõ ràng nhóm ma trận theo (khe, phụ); bỏ qua nội suy tại khung khi tạo nút, thay đổi tài nguyên cảnh hoặc cắt ống kính |
| Trận chiến | Máy ảnh | ma trận khung nhìn guLookAtReflect | Đang hoạt động | Bỏ qua khi máy ảnh cắt mạnh |
| Hiệu suất chiến đấu | Mặt đất 3D, thành phố HD và mặt nước | Nút mô hình; Đi bộ HD `native_marker.cpp` | Tích cực; bản vẽ máy chủ đã đọc `lerpWorldTransforms`/`modViewProjTransforms` | Tham số thời gian của trình đổ bóng mặt nước được nâng cao theo khung kết xuất (không kiểm tra trạng thái hiện tại) |
| Hiệu suất chiến đấu | Hình ảnh tổng thể HD của máy bay | `native_sprite.cpp` Sử dụng ma trận được rút ra lần này | Tương tự như trên, theo dõi chuyển động | — |
| Hiệu suất chiến đấu | Bầu trời, lớp cuộn | Chế độ 2, khối 32×32 TEXRECT | **Bất động** | Không thể nhìn thấy nó khi bầu trời cuộn chậm; khi camera di chuyển nhanh sẽ không đồng bộ với thân máy 60 khung hình, các bạn hãy xem lại nhé |
| Hiệu suất chiến đấu | Chế độ 0xB màn hình tọa độ diễn viên, HUD, số sát thương | VĂN BẢN | Đừng di chuyển | Đừng quan tâm |
| Hiệu suất chiến đấu | Thay đổi khung hình Sprite, bảng màu nhấp nháy | Thay đổi kết cấu | Không thể chèn được (bản thân nội dung có 30 khung hình trở xuống) | Không có giải pháp nào và không nên chèn nó |
| Bản đồ thế giới | Mô hình tàu, cột mốc, đường ray, ống kính | Mô hình 3D cộng với ma trận; Đi bộ HD `native_marker.cpp` | Đang hoạt động | Cận cảnh các hình tứ giác và khối bản đồ ở hai bên bầu trời đầy sao để xem có đường nối nào nhấp nháy không |
| Tiêu đề, mở đầu, thẻ tiêu đề chương, kết thúc | Chế độ 14 chia tỷ lệ/xoay văn bản | Ma trận tứ giác cộng | Đang hoạt động | Dư ảnh (`80083744` phản hồi khung) đọc bộ đệm khung thực và khung được chèn không tham gia phản hồi. Nó được cho là vô hại và cần được nhìn thấy trên máy thật |
| Tiêu đề | Ngọn lửa, dòng tập trung | thay đổi khung VĂN BẢN | Bất động | — |
| **Bản đồ chiến thuật** | Cuộn bản đồ, con trỏ, di chuyển đơn vị, nhấp nháy phạm vi, hiệu ứng đặc biệt trên bản đồ | Chế độ 4/5/6/8/12/13, tất cả VĂN BẢN; Lớp bản đồ HD là một hình chữ nhật được chủ nhà vẽ theo `view_left` | **Toàn bộ màn hình không di chuyển, vẫn còn 30 khung hình** | Xem §6.2 |
| Các giao diện máy chủ như hội thoại, liên cảnh, xác nhận trước chiến tranh, cài đặt, v.v. | Chuyển đổi RmlUi, văn bản xuất hiện từng chữ | Vẽ trong móc trình bày | Vẽ mỗi khi tính năng chèn khung được bật và tự động điều chỉnh theo tốc độ khung hình của màn hình | Nhấn khối lượng công việc vào hook để kiểm tra hạch toán (§6.3) |
| Liên cảnh/đối thoại ở chế độ gốc | — | VĂN BẢN | Không di chuyển | Về cơ bản nó là một bức ảnh tĩnh, không thành vấn đề |

## 6. Những việc cần làm

### 6.1 Bánh răng đầu tiên: cảnh ma trận

1. Đặt mục "Tốc độ khung hình: Gốc 30/Theo dõi màn hình" (để mặc định 30), lưu `presentation.json`; tương ứng với `RefreshRate::Original`/`Display`, chuyển sang `updateUserConfig` hiện có. Phiên gỡ lỗi đã sửa lỗi 30: Tập lệnh so sánh ảnh chụp màn hình (`check_aspect.py` và các so sánh "chỉ khung hình động" khác) và bản ghi giả định một khối lượng công việc trên mỗi khung hình.
2. `srw64_render_node` (`game_hooks.cpp`) đã gói bản vẽ của từng nút elf và thu được (khe, con). Đối với các nút chế độ 0xE/0xF/0x10 và mô hình, hãy chèn `gEXMatrixGroup` (số = vị trí × 3 + phụ + hằng số) trước khi vẽ nút, sau đó đặt lại. GBI mở rộng đã được kê toa thường xuyên.
3. Bỏ qua các điều kiện: Nút có cảnh/tập bản đồ mới hoặc đã thay đổi trong khung này (khe này được các tác nhân khác sử dụng lại), bước nhảy vị trí vượt quá ngưỡng, ống kính bị cắt mạnh và máy trạng thái hiệu suất thay đổi các phân đoạn. Khung tương ứng được cấp cho nhóm `G_EX_COMPONENT_SKIP` và ảnh được chuyển sang nhóm xem.
4. Chèn `gEXSetRefreshRate(30)` vào đầu khung để tránh chuyển đổi qua lại khi đọc từ đĩa.
5. Giữ một bàn được đóng theo cảnh (theo cách tiếp cận của Những kẻ nghịch ngợm) và màn trình diễn có vấn đề sẽ được kết thúc trước tiên.
6. Hiệu suất: 4×MSAA cộng với lớp HD trên Deck, mỗi khung hình phải được đẩy xuống 16,7 ms (OLED 90 Hz là 11,1 ms) mới có ý nghĩa; nếu không thể đạt được, RT64 sẽ không xuống cấp mà chỉ chậm lại về tổng thể. Để đo lường thực tế, hãy giới hạn mục tiêu ở mức 60 nếu cần thiết.

### 6.2 Trang bị thứ hai: Bản đồ chiến thuật

Tất cả các chuyển động trên bản đồ đều là các bản dịch hình chữ nhật: cuộn là cùng một độ lệch cho tất cả các họa tiết trên lớp bản đồ và con trỏ và các đơn vị là tọa độ màn hình tương ứng của chúng. Hai cách tiếp cận:

- **A. Bản vá RT64: Nội suy hình chữ nhật được đánh số**. Sử dụng thẻ G_NOOP được đánh số trong danh sách hiển thị (các móc HD hiện có đã sử dụng thẻ này) để đánh dấu số nhóm cho hình chữ nhật sau; RT64 ghi lại nó trong `DrawCall`. Khi ghép các khung, hãy ghép các hình chữ nhật của hai khung trước và sau theo "số nhóm + số sê-ri trong nhóm". Khi hiển thị khung nội suy, hãy chèn tọa độ hình chữ nhật (và cắt) theo trọng số. Hình chữ nhật không sử dụng bộ đệm vận tốc đỉnh (bộ `pos − vel × (1 − w)` đó chỉ có trong tính năng đổ bóng đỉnh RSP) và phải được thêm riêng khi hình chữ nhật được chuyển đổi sang tọa độ màn hình. Phía máy chủ `srw64_render_node` gửi nhãn tới các họa tiết của lớp bản đồ; bản vẽ chủ của các lớp bản đồ HD và biểu tượng đơn vị HD phải có cùng độ lệch nội suy. Các thay đổi tập trung vào RT64 và không lớn về mặt trò chơi, nhưng các bản vá RT64 cần phải theo kịp quá trình bảo trì ngược dòng.
- **B. Về phía trò chơi, thay đổi hình chữ nhật của lớp bản đồ thành hình tứ giác dưới hình chiếu trực giao**. Mỗi sprite có một ma trận và có thể sử dụng phép nội suy ma trận làm sẵn của RT64. Không thay đổi RT64 mà hãy viết lại hướng dẫn do một số trình kết xuất đưa ra, chẳng hạn như `80095974`, `800945D4`, `80096CD8`, v.v. Màn hình rộng đã áp dụng `gEXSetRectAlign`/cắt xén cho các bản vẽ này và việc thay thế kết cấu HD được xác định bằng hàm băm hình chữ nhật, việc này rất phức tạp.

Xu hướng A. Bất kể cái nào được sử dụng, hoạt ảnh thay đổi khung của khối bản đồ (mặt nước, nhấp nháy phạm vi) và hoạt ảnh khung của chính con trỏ đều không được chèn.

Không có số lượng cuộn bản đồ và số lượng pixel con trỏ di chuyển trên mỗi khung hình (`801FFADC` được theo sau bởi chuyển đổi trực tiếp, chẳng hạn như "số lượng cuộn = 32 − con trỏ x" và kích thước bước tùy thuộc vào chuyển động của chính con trỏ). Chúng được đo cùng nhau trong quá trình thử nghiệm để xác định lợi ích thị giác là 30 → 60.

### 6.3 Điểm kiểm tra trên lớp máy chủ

- Mỗi khối lượng công việc của hook kết xuất sẽ được gọi N lần: các dải hiển thị `srw64::ui::presented()`/`in_flight`, `names::cover_presented(workload)`, `dialogue::gpu_draw(workload)`, `wide_map` được tính theo số lượng khối lượng công việc. Các cuộc gọi lặp lại phải bình thường và được xác nhận từng cái một.
- `record.start` đọc lại một khung hình trên mỗi kết xuất và số lượng khung hình sẽ tăng gấp đôi; `srw64_screenshot` có thể chặn các khung nội suy.
- Việc đọc tốc độ khung hình bây giờ đếm danh sách hiển thị (không đổi 30). Bạn cần thêm số lượng kết xuất để xem việc chèn khung có hiệu quả hay không.
- `get_display_framerate()` Hai deadlock số 60 (`host.cpp:106`, `graphics.cpp:524`), cực chất dùng cho các nhịp khác, chưa đụng tới.
- Âm thanh hoàn toàn không bị ảnh hưởng (logic và nhịp độ VI không thay đổi).

## 7. Kế hoạch test (nửa ngày, yêu cầu thi công và máy thực tế)

1. `graphics.cpp` cộng với `SRW64_REFRESH_RATE=display|<数字>`, tương ứng với `Display`/`Manual`; đọc tốc độ khung hình cộng với số lượng kết xuất.
2. Xem và ghi theo trình tự: tiêu đề (thu phóng văn bản, ngọn lửa), phần mở đầu, bản đồ thế giới, chương trình chiến đấu với chuyển động của camera và đòn tấn công, cuộn bản đồ chiến thuật và chuyển động của đơn vị, hội thoại và trang RmlUi liên trò chơi.
3. Ghi lại: tốc độ khung hình kết xuất có đạt 60 hay không; những gì đã di chuyển; ví dụ về sự không phù hợp; lớp máy chủ có bị nhấp nháy, bị lệch hoặc bị trùng lặp hay không; liệu `logicalRateFromFactors` có ổn định ở mức 30 hay không; Thời gian GPU trên mỗi khung hình trên Mac.
4. Đo số lượng pixel trên mỗi khung hình để cuộn bản đồ chiến thuật, con trỏ và chuyển động của đơn vị.
5. Dựa vào đó hãy quyết định quy tắc đánh số, bỏ số của số một và nên đi A hay B ở số hai.

## 8. Chưa được xác minh

- Số truy xuất của `osViSetEvent` (ước tính ngược lại là 1 dựa trên 30 khung hình được đo thực tế).
- Phương pháp tải vào bộ đệm của trò chơi này đáp ứng điều kiện `interpolationEnabled` của RT64.
- Hiệu ứng dư ảnh (phản hồi khung hình) và nội suy khung hình cùng tồn tại.
- Tự động khớp tỷ lệ không khớp thực tế trong hiệu suất chiến đấu.
- Giá trị của tốc độ làm mới chuỗi hoán đổi trong Bộ bài (Vulkan) và hiệu suất khi khung hình gamescope bị giới hạn.
- Việc tăng tốc gấp 2 lần `D_8010F0C8 = 1` có tác dụng phụ phi logic nào không (cho biết bộ đệm danh sách có đủ cho mỗi VI hay không).