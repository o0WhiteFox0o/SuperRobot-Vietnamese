> **Ngôn ngữ / Language:** [Tiếng Việt](original-controls.vi.md) · [English](original-controls.en.md) · [中文](original-controls.md)

# Liên kết khóa gốc (phân tích tĩnh)

28-09-2026. Bài viết này trả lời câu hỏi “Trò chơi đọc bộ điều khiển như thế nào và mỗi phím trên mỗi màn hình có tác dụng gì?” Mọi kết luận đều đến từ việc tháo rời (`build/recomp/cpu-scan/<overlay>/*.text.s`) và bảng dữ liệu ROM, **không được xác minh bằng máy thực tế**; nơi nào có hồ sơ máy thực tế vui lòng ghi rõ nguồn. Phía máy chủ (bàn phím/bộ điều khiển → Mặt nạ N64, ánh xạ lại) nằm ngoài phạm vi của bài viết này, xem [Bàn phím Steam Deck](../design/steam-deck-controls.md) và `src/host/input_bindings.hpp`.

Phương pháp quét: Tìm tất cả các hướng dẫn đọc bảng đầu vào (318), ghi hàm và mặt nạ cho các lần kiểm tra tiếp theo, sau đó phân loại theo lớp phủ và bảng trạng thái; tập lệnh nằm trong thư mục tạm thời của phiên khác với `tools` và chưa được gửi.

## 1. Lớp lấy mẫu (phần thường trú)

| Chức năng | Hiệu ứng |
| --- | --- |
| `80087730` | Khởi tạo: `osContInit` Nhận mặt nạ kết nối `D_8010F6C0`, xóa tất cả các bảng, khóa đầu vào `D_8010F6BA=0` |
| `8008163C` | Mỗi lần vòng lặp chính được gọi: `80087A48` bắt đầu đọc từ cổng 0 (`osContStartReadData`/`osContGetReadData` → `OSContPad D_800F97B0[4]`), `80087AA4` **HOẶC phím lần này được đọc thành** từ tích lũy `D_8010F1A4[口]` và hướng chuyển đổi cần điều khiển là OR `D_8015F73C[口]`. Chỉ tiếp tục khi đạt đến khung trò chơi (`D_80172D0C ≥ D_8010F0C8`): `80087DD4` tính các cạnh, `80087C9C` gieo hạt lại với các giá trị hiện tại, `80081D60` tổng hợp ba bảng |
| `80087AA4` | Cần điều khiển → Hướng: `|x|≥45` dành cho vị trí bên trái và bên phải, `|y|≥45` dành cho vị trí trên và dưới; giá trị cần điều khiển được lưu trữ chỉ tắt và bị xóa khi nó được rút lại (bánh cóc), do đó thanh lỏng sẽ không rung |
| `80087C9C` | Ghép lại cuối khung: ngưỡng thay đổi thành ±50 |
| `80087DD4` | Mỗi cổng: cờ hợp lệ `D_80178D24[口]`, được tính khi khóa đầu vào bằng 0; `press = new & ~old` |
| `80081D60` | Tổng hợp: Khi cần điều khiển có hướng, hãy sử dụng bit `0xF00` của cần điều khiển để **thay thế** bit phím chéo; xem các từ liên tục bên dưới |

Nhiều mẫu giữa hai khung hình trò chơi được tích lũy bằng OR và nhấn nhanh sẽ không bị mất.

### Ba bảng (một u16 cho mỗi cổng, cổng 0 ở địa chỉ thấp nhất)

| Bảng | Ý nghĩa |
| --- | --- |
| `D_8015D9FA` / `D_8015CAF0` | Giữ gốc / Cạnh gốc (không có cần điều khiển) |
| `D_8010F124` / `D_8010F724` | Hướng chuyển đổi cần điều khiển Nhấn và giữ / Edge |
| `D_800F97D0` **Nhấn và giữ** | Ban đầu nhấn và giữ, khi cần điều khiển có hướng thì vị trí hướng được đổi thành cần điều khiển |
| `D_80178A08` **Nhấn** | Phiên bản cạnh giống nhau; hầu hết các màn hình đều đọc nó |
| `D_801612E0` **Bùng nổ** | Có một lần nhấn trong khung này → Burst = nhấn, đếm 12; nếu không thì số lượng đạt đến 0 và có một lần nhấn → Burst = nhấn và giữ, đếm 3. Tức là độ trễ đầu tiên là 12 khung hình, sau đó là 3 khung hình một lần. **Burst là toàn bộ từ**, không chỉ các phím điều hướng: nhấn A, L, R nơi bạn đọc từ cũng sẽ bung ra (ca khúc chủ đề, chuyển đổi bản đồ L/R) |

Bit: A `0x8000`, B `0x4000`, Z `0x2000`, START `0x1000`, trên `0x800`, dưới `0x400`, trái `0x200`, phải `0x100`, L `0x20`, R `0x10`, C↑ `8`, C↓ `4`, C← `2`, C→ `1`.

- Logic trò chơi chỉ đọc cổng 0 (phần tử đầu tiên của bảng); chỉ `1p–4p ON/OFF` của menu gỡ lỗi và hai vòng lặp cổng nhấn của trình xem.
- Lớp phủ liên trường cũng có bảng chuỗi riêng với cùng thuật toán `D_801DD62C`/count `D_801DECE0` (`801C4538`, `801C4A20`, v.v. đọc nó).
- Khóa đầu vào `D_8010F6BA`: Khi đặt thành 1, cả bốn cổng đều bị xóa. `800A344C` (nhấp nháy/mờ toàn màn hình, dòng tập lệnh `3D3B`) và chiến thuật `801F2AAC` được thiết lập và xóa sau khi hoàn thành.
- Tiến bộ đối thoại `8008D748` đọc A của **cạnh gốc** `D_8015CAF0` mà không cần qua bảng tổng hợp.

## 2. Kết hợp toàn cầu

| Kết hợp | Mã | Hiệu ứng |
| --- | --- | --- |
| Giữ Z + nhấn BẮT ĐẦU | `80085EF8`=`rawhold&Z && rawpress&START`. Bản đồ thế giới `801C28E4`, Chiến thuật `801DFBD0`, Cần bán `801C3788`, Tiêu đề `801CA9CC`, Chiến đấu `801C9710`, Quản lý Pak `801C34B0` Đã gọi mọi khung hình; Giữa các trường `801D8D20`, Trang tên `801C657C`, hai người xem tự đánh giá `rawhold&0x3000` | `80099814(5,1,2)` mờ dần, sau đó là chế độ 1 (logo BANPRESTO → tiêu đề). Khi kết thúc giảm dần, nếu START **vẫn được nhấn** và nửa từ bit15 đầu tiên của SRAM `0x08003E10` là 1 (`80093610`) → chế độ `0x11` tải lại cấp độ hiện tại, nếu không thì tiêu đề chế độ 7 (trận chiến `801C97E4`, bản đồ thế giới `801C2968`, liên trường `801D8DDC` giống nhau ở ba vị trí). Đối với hộp mực bán lẻ, bit này là 0 và người chơi sẽ chỉ trả lại tiêu đề. Xem số đo thực tế trong hiệu suất chiến đấu [Bỏ qua hiệu suất chiến đấu](../native/battle-animation-skip.md) |
| Bật nguồn và giữ phím START | `800801A4` mẫu một lần `D_8010F1A4&START` | Chế độ ban đầu `0x19` (`load_0022CFD0`, コントローラパック quản lý), nếu không thì chế độ 7 |
| Phần lựa chọn tập lệnh `3D44` | `8009F3A8` | Từ liên tục ↑↓ Di chuyển con trỏ (âm thanh 0xB9), nhấn A để xác nhận |
| Đối thoại | `8008D748` | Chỉ có A. Không có tua đi nhanh, B không có tác dụng; chức năng tương tự của chiến tuyến |

## 3. Chế độ và lớp phủ

`800801A4 → 800CFEC8[模式−1]`, mỗi mục là một phần tải sơ khai. Các chế độ được yêu cầu với các hằng số: 1 logo, 2 trận chiến, chiến thuật 3/0x11/0x16/0x22, 4 trò chơi xen kẽ, 5/6 tên, 7 danh hiệu, bản đồ thế giới 12/13, tải 0x12–0x15, biến thể chiến đấu 0x1A/0x1C, 0x1F, kết thúc 0x20, giảm giá 0x21, 0x23/0x24. Những mục sau chỉ có thể truy cập được từ menu gỡ lỗi hoặc tổ hợp khởi động:

| chế độ | lớp phủ | nội dung (chuỗi ASCII trong ROM) |
| --- | --- | --- |
| 1 | `load_000856D0` | cờ BANPRESTO; `[64 BASE SAMPLES]` menu gỡ lỗi trong cùng một lớp phủ |
| 9/8 | `load_00089EA0` | `ROBO VIEWER !!` (Trình xem Sprite/Hoạt hình, `komaokuri!` từng khung hình) |
| 10 | `load_0008E580` | `ROBO VIEWER !!` Phiên bản 3D (`FOG`, `rotx/roty/rotz`, `dist`) |
| 16 | `load_00216730` | `BTLINIT`: Chỉnh sửa tham số chiến đấu, nhấn và giữ Z để vào chế độ 2 |
| 0x18 | `load_0022E580` | `[KARAOKE MAKER]` (`BLOCK EDIT`, `TIMING EDIT`) |
| 0x19 | `load_0022CFD0` | コントローラパック Management (nhấn và giữ START khi khởi động) |

Menu gỡ lỗi `801C3174` (bảng `801C69C8`): ↑↓ liên tục quay vòng qua 27 mục; ←→ và C←/C→ điều chỉnh hai tham số, đồng thời giữ B, giữ hướng để thay đổi liên tục; A thực thi `801C35D0 → 80080188(D_801C69D4[项])`. Mục: TITLE, NAMEENTRY0/1, VIEWER, VIEWER2, ​​​​HMF VIEWER, TIẾP TỤC, LOAD1–4, KẾT THÚC, INTERMISSION, TACTICS, BTLINIT, WGADRS, KARAOKE, BÁN ĐƠN VỊ, GỠ LỖI TIẾP TỤC, DỮ LIỆU MẪU 0–3, 1p–4p BẬT/TẮT, fbuf màu rõ ràng. Không theo đuổi các điều kiện để vào menu (không thể nhập khi khởi động bình thường).

## 4. Mỗi màn hình

Phương pháp viết: `按下`=`D_80178A08`, `按住`=`D_800F97D0`, `连发`=`D_801612E0`, `原始`=`D_8015D9FA`/`D_8015CAF0`. Nếu B đo trước rồi đo A ở cùng một chỗ thì ghi là "B/A".

### Tiêu đề `load_0010DA50`

| Màn hình | Chức năng | Chìa khóa |
| --- | --- | --- |
| NHẤN BẮT ĐẦU Trang | `801C5188`, `801C53F4`, `801C591C`, `801C5D94`, `801C6514` | Nhấn A hoặc BẮT ĐẦU (`0x9000`) |
| Thực đơn chuông | `801C642C` | **Giữ** ←→ Di chuyển con trỏ (không phải cạnh, xem [Menu tiêu đề](../native/native-title-menus.md)) |
| オプション | `801C6B14` | Bắn liên tục ↑↓, nhấn A |
| ロード Mỗi trang | `801C709C`, `801C783C`, `801C7A48`, `801C8074` | Liên tục ↑↓, nhấn A/B |
| danh sách サウンド | `801C8724`, `801C9904`; Tiêu điểm EXIT `801C89E4`, `801C9ADC` | Liên tục ↑↓ (↓ đo riêng), nhấn A, A/B |
| Đang chơi | `801C9268`, `801C97AC` | Nhấn B để quay lại; bùng nổ Z/↑/L cho bài hát trước, ↓/R cho bài hát tiếp theo; nhấn C↑ −10, C↓ +10; C← chỉ trong các bản nhạc `0x124` và `D_801CC1FA[项]==1` Thỉnh thoảng có hành động (mục ẩn, không được truy đuổi) |
| Trang mở đầu | `801C9EA8`, `801CA0A4`, `801CA1C0` | Phím bất kỳ → `801C5F04(1)` để chuyển sang trang tiếp theo; `801CA608` Nhấn A |

### Lựa chọn nhân vật chính và tên `load_001090A0`

`801C50B8` Lựa chọn nhân vật chính A (←→ trong `801C34E4`), `801C5644`/`801C5AD0` Chỉnh sửa tên A, B, A hoặc B, `801C5E88` Xác nhận cuối cùng A/B, `801C62D8` Kana tấm A, B. Mỗi khung hình `801C657C` tự xác định Z+BẮT ĐẦU và BẮT ĐẦU. Máy chủ đã tiếp quản, xem [tên trang](../native/native-name-entry.md) và [tên đơn vị đã sửa](../native/fixed-unit-name.md).

### Bản đồ thế giới `load_000A7EC0`

Chỉ có Z+BẮT ĐẦU cho mỗi khung hình. Phần còn lại đều có kịch bản (Đối thoại A, Chọn chi).

### Bản đồ chiến thuật `load_000AB160` (bảng trạng thái chính `D_80217E0C`, ý nghĩa trạng thái xem [chu kỳ địch](../native/enemy-cycle.md), [di chuyển-nhảy](../native/move-jump.md))

| Trạng thái/Chức năng | Chức năng | Chìa khóa |
| --- | --- | --- |
| Chuyển động con trỏ | `801C63D8` (được điều chỉnh bởi `801C66E8`) | Đọc nhấn khi không có hướng trong khung trước, nếu không thì giữ; bảng hướng `D_80217AAC` bao gồm hướng xiên; **Giữ C↓ hoặc C←** 8 pixel mỗi khung hình, nếu không thì 4 |
| Nhàn rỗi 5 | `801C8B04` | Bắn liên tục Z/L Trước, R tiếp theo không hành động bên ta (`0x2030`, Z đồng nghĩa với L); nhấn A để chọn; Cửa sổ/bảng địa hình căn hộ B |
| Menu đơn vị 8, 0x3A | `801CA7E4` | Nổ ↑↓; nhấn A để quyết định; nhấn START chỉ hợp lệ ở mục loại 5 (Mothership Haijin) → `801D050C(0,0)`, đọc START trong đó (không theo dõi chi tiết) |
| Di chuyển lựa chọn 0xC/0 | `801CBB04` | A xác nhận, B hủy bỏ; không đọc R, L, Z, BẮT ĐẦU |
| 0xC/7 | `801CDF7C` | Liên tục ↑↓ `D_80172ED6`, nhấn A／B |
| Bang 9 | `801CB074` | Nhấn phím bất kỳ để đóng cửa sổ và chọn đơn vị dưới con trỏ |
| Trạng thái 0xB | `801CB88C` | Phím bất kỳ để đóng cửa sổ; Công tắc `0x2030` (Z/L trước, R tiếp theo) |
| Họ 0xD/0xE | `801CE144` (`801CE1E4`, `801CE234`, `801CE3A0`); `801CE234`; `801CF70C`; `801D21D0` | `801CE144`: Z/L Trước, R tiếp theo (`D_80172ED6`). `801CE234`: Khi có nhiều trình điều khiển, A hoặc → tiếp theo, ← trước đó, B trả về. `801CF70C`: B được trả lại và giải phóng. `801D21D0`: A hoặc B đóng cửa sổ tin nhắn |
| Tấn công/vũ khí gia đình 0x17 | `801D3010` (7 giai điệu bao gồm `801D3140`), `801D2A10`, `801D3140`…`801D4320` | Nhấn A để quyết định từng trạng thái phụ, B Hủy; `801D26B4` (Phím `801D3140`, `801D6FFC`): Chuyển đổi mục tiêu Z/L/R trong danh sách 60 vị trí |
| Khẳng định trước chiến tranh | `801D5064`, `801D5294` | A/B; `801D5294` Ngoài ra còn có một vụ nổ ↑↓. Tiếp quản, xem [Giao diện người dùng chiến đấu](../native/native-battle-ui.md) |
| Cửa sổ thông tin 0x1B, 0x22, 0x2E, 0x2F, 0x30, 0x34, 0x36, 0x37, 0x3C | Nhấn A để nâng cao từng chức năng trạng thái; chia sẻ `801D6FFC` B để đóng + `801D26B4` L/R/Z để chuyển đổi đơn vị |
| Trang khả năng | `801F9BB4` (khóa `801D1DB8`), `801D6784`, `801F1B10` | MỘT; phím chéo liên tục; Lật trang L/R (trang R tiếp theo, trang Z/L trước, `D_80227A82..84`); `801D6784` B quay lại, bắn liên tục ↑↓ Danh sách `D_80227A81` |
| Danh sách lưới (lựa chọn xuất kích, v.v.) | `801EDBE0` (`801C7DB8`, `801D0EE0`, `801D1C28`, `801DBEE4`), `801EE060` (`801D1CE8`), `801EE594` | Nhấn ←→ cột `D_8015DA0B`, bật ↑↓ hàng `D_8015DA0F`, R trang tiếp theo, Z/L trang trước, Quyết định |
| Danh sách hai chiều | `801F9238` (`801CE3A0`, `801D2FB8`, `801D5404`) | Liên tục ↑↓ `D_802271DB`, nhấn ←→ `D_802271D8`, B |
| Cửa sổ tùy chọn | `801D1F88` | B/A; ghi `D_8015DDA8` (bao gồm cả chuyển đổi hoạt ảnh chiến đấu) và `8009187C` ghi lại vào tiêu đề SRAM |
| Quay lại xác nhận tiêu đề | `801D22FC` (bảng `80217C84`) | Liên tục ↑↓(`801C2600`); A ở mục 1 → Tiêu đề chế độ 7; B hoặc A ở mục 0 → `801C8AB4` Return |
| Mẹo đánh bại | `801DF53C` (bảng `80217DF4`/`80217E08`) | Nhấn A, B hoặc START → âm thanh 0xB4, chế độ `0x16` để khởi động lại cấp độ này |
| Màn hình kết quả | `8020DA08` (bảng `8021E274`) | Đợi 20 khung hình và nhấn A để tiến |
| Bảng phụ trạng thái mở 2 `80217AFC` | `801C7BF0`, `801C7DB8`, `801C7E30`, `801C7FA0`, `801C80A4` | Bất kỳ chìa khóa nào để thăng tiến; B; A quyết định ở mục 0, A/B trả về (suy ra là danh sách và xác nhận trước khi tấn công) |
| Mỗi khung hình | `801DFBD0` | Z+BẮT ĐẦU |
| Mã chết | `801E03C4` | Nhấn thô BẮT ĐẦU chuyển đổi `D_8015DDA8` bit2 (hoạt ảnh chiến đấu); không có cuộc gọi hoặc tham chiếu bảng |

### Hiệu suất chiến đấu `load_00121560`

- `801C9710` Vòng lặp chính: Khi nhấn cờ `0x1A` (`8008016C`) và `D_80161310==1`, **B** sẽ kết thúc đoạn hiện tại và mờ dần; khi `D_80161310==0`, nó sẽ tự động kết thúc; khi cờ `0x1C`, **bất kỳ khóa nào** sẽ kết thúc. Không có đầu vào nào được đọc bên ngoài: không bỏ qua, không chuyển tiếp nhanh. Z+BẮT ĐẦU Xem Phần 2.
- `801C9DAC` Mỗi khung: Nhấn và giữ **C↑** để xóa `D_8010F5BA` (`8008422C` được đặt và cờ của từng mục lớp phủ bị xóa, mục đích không được theo đuổi).

### Trường liên kết `load_0008F4B0` (bảng màn hình `D_801DC9D0`)

Nhấp vào bảng để đọc tất cả và hướng dẫn được xuất bản bởi liên kết riêng tư. Màn hình A/B: menu chính `801CE19C`, lưu trữ `801CEABC`/`801CEEF8`, chuyển đổi `801CF564`/`801CF988`/`801D04A4`/`801D087C`/`801D1100`, khả năng `801D1554`／`801D2378`, danh sách vũ khí `801D21F8` (chỉ B), chuyển `801D263C`／`801D2A24`／`801D3A90`／`801D41FC`／`801D4578`, các bộ phận `801D4A98`/`801D4C94`/`801D51EC`, Trình chiến đấu liên kết `801D70FC`.

- Trang khả năng `801D2030`/`801D24C8` và Link Battler `801D6D34`: `0x2030` → `801CCDA0`: Z/L cho trang trước, R cho trang tiếp theo.
- `801D8D20` Trên mỗi khung hình: **Giữ** Z+START (`0x3000`) → mã thoát 1 → mờ dần → tiêu đề (hoặc bit gỡ lỗi SRAM + START → `0x11`).
- Chuỗi kế thừa không được tham chiếu `801D796C`–`801D8CC8` (A/B/↑↓) và `801DA2C0`–`801DAAEC` (R/Z＋L,↑↓,C←,A,Z＋START) xem [Menu xen kẽ](../native/native-intermission-menu.md), [Link Chiến binh](link-battler.md).

### Cần bán `load_00107BF0`, Đang kết thúc `load_001156A0`

Cần bán: `801C3088` Khóa bất kỳ, `801C3514` Liên tục ↑↓, A, A hoặc B, `801C3788` Z+START. Kết thúc `801C2D1C`: Tiến lên bằng phím bất kỳ.

### Lớp phủ gỡ lỗi

- Quản lý Pak `load_0022CFD0`: `801C35E4` A/B, bùng nổ ↑↓; `801C36BC` bùng nổ ←→, B/A; `801C37F0`/`801C382C` A; thoát trở lại chế độ 7.
- Wizard Viewer `load_00089EA0`: Nhấn bằng miệng để đọc L, C←, Z+START.
- Trình xem 3D `load_0008E580`: Nhấn và giữ ←→/↑↓ để điều chỉnh camera (`D_8015DDF0` một tập hợp các dấu phẩy động, `80081CB8` đặt lại), START, L/R, Z, Z+Start.
- BTLINIT `load_00216730`: `801C32EC` Mỗi phím trong số 10 phím thay đổi tham số liên tục (chỉ số dưới `D_8010F7BE`, bảng `D_8015DCBA…`), `801C3850` nhấn và giữ Z → trạng thái 0x17 → chế độ 2.
- MÁY LÀM KARAOKE `load_0022E580`: ↓／↑／C→, C↑, L／R, bùng nổ ↑↓, A＋B＋→, C→／Z, B.

## 5. Kết luận hữu ích cho việc ánh xạ lại

- **Z là bí danh của L trong danh sách**: tất cả các bài kiểm tra "trước" `0x2020`, bài kiểm tra "tiếp theo" `0x10`; công dụng duy nhất của Z là đặt lại Z+Start và BTLINIT. Bạn sẽ không bị mất chức năng khi gán một phím khác cho Z.
- **Phím C chỉ có ba chức năng trong quy trình thông thường**: tăng tốc con trỏ bản đồ (C↓, C←), ca khúc chủ đề ±10 (C↑, C↓) và giữ phím C↑ để xóa dấu trong trận chiến. C→ Không được sử dụng trong các quy trình thông thường.
- **BẮT ĐẦU trong quy trình bình thường chỉ có **: NHẤN BẮT ĐẦU, Z+BẮT ĐẦU, mục nhập quyền làm mẹ và "phím bất kỳ" cho lời nhắc đánh bại. Công tắc hoạt ảnh chiến đấu đi qua cửa sổ tùy chọn, không phải BẮT ĐẦU (công tắc BẮT ĐẦU đó là mã chết).
- **Các phím chéo tương đương với phím điều khiển**. Khi cần điều khiển có hướng, nó sẽ che các phím chéo; hướng xiên được xác định trong bảng con trỏ bản đồ.
- **Từ liên tục là toàn bộ từ**: Việc gán một phím nào đó để "nhấn và giữ" sẽ kích hoạt liên tục trên màn hình đọc từ liên tục (L/R để chuyển đơn vị, chuyển track).
- The dialogue only recognizes the original edge of A, and any synthesis and fast forwarding are done by the host.
- Short presses will not be lost (inter-frame OR accumulation), but the button must span one game frame sample to be seen; just give a frame edge when injecting the button (this is already done for field-to-field takeover).