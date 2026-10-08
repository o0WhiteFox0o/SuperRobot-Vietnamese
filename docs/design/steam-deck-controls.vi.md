> **Ngôn ngữ / Language:** [Tiếng Việt](steam-deck-controls.vi.md) · [English](steam-deck-controls.en.md) · [中文](steam-deck-controls.md)

# Phím và biểu tượng nút Steam Deck

2026-09-25. Phiên bản Steam Deck hoạt động theo **Mẫu bộ điều khiển mặc định của Steam** và người chơi không cần thay đổi cài đặt đầu vào Steam. Trang này ghi lại vị trí phím hiện tại (theo mã), mục cài đặt được thêm lần này và biểu tượng phím (PromptFont). Để biết gói cao cấp hơn, hãy xem [Chuyển cổng ba nền tảng](three-platform-port.md) X2 và để biết cách xây dựng và cài đặt, hãy xem [Bản dựng Linux](../guide/linux-build.md).

## Nguyên tắc

- Chỉ sử dụng nghĩa gốc của nút Deck trong mẫu mặc định: SDL nhìn thấy bộ điều khiển tiêu chuẩn (Steam Virtual Controller) và tên nút giống với bố cục Xbox.
- Một phím chỉ làm được một việc trong cùng một cảnh; sự kết hợp đã được phiên bản gốc chiếm giữ sẽ không bị thay đổi.
- Các chức năng mới được máy chủ thêm vào (cài đặt, đọc hội thoại, bỏ qua) ưu tiên các phím không được sử dụng trong phiên bản gốc: phím xem, phím L2, R2 và phím quay lại. L2 và R2 được trao cho máy chủ (được người dùng đồng ý 2026-09-25), hai phím này không hiển thị trong chính trò chơi.
- Lời nhắc theo sau thiết bị được sử dụng gần đây nhất của người chơi: lời nhắc của bộ điều khiển (mục nhập`<key>_pad`) được hiển thị sau khi nhập bộ điều khiển và lời nhắc bàn phím được thay thế sau khi nhập bằng bàn phím, chuột hoặc màn hình cảm ứng.
- Bạn có thể sử dụng màn hình cảm ứng để nhấp vào bất cứ nơi nào bạn có thể nhấp vào.

## Khóa hiện có

Việc ánh xạ bộ điều khiển tới các nút N64 là liên kết mặc định của `src/host/input_bindings.hpp`. Người chơi có thể thay đổi nó trên trang cài đặt "Thao tác" ([Thay đổi phím](../native/controls-remapping.md)); 28-09-2026 Nhấn [Phân tích nút gốc](../gameplay/original-controls.md) để thay đổi mức độ ưu tiên của chức năng: các phím A, B, START hữu ích ban đầu, các phím chéo, cần điều khiển, L/R vẫn giữ nguyên, Z và X/Y Giải phóng nó cho chức năng này. Trang gốc sử dụng `frontend.cpp` và `pad_keys` để chuyển đổi tay cầm thành các nút trang; cửa sổ cài đặt là `settings_pad` và trang xác nhận trước chiến tranh là `battle_buttons`.

| Nút boong | Trong trò chơi (N64) | Trang gốc (phiên, tiêu đề, lưu trữ, tên, v.v.) | Đọc đối thoại | Cửa sổ cài đặt |
| --- | --- | --- | --- | --- |
| A | A | được | Trang tiếp theo | Nhấn nút hiện tại |
| B | B | Trở về | — | Đóng |
|
| Y | Đối với chủ nhà: Chuyển hoạt ảnh trận chiến trên trang xác nhận trước trận chiến | Chuyển hoạt ảnh trận chiến trên trang xác nhận trước trận chiến | — | — |
| L2 | Đối với máy chủ: Khi bản đồ không hoạt động, con trỏ sẽ di chuyển đến xác địch trước đó | — | Tự động bật/tắt đọc | — |
| R2 | Đối với máy chủ: Khi bản đồ không hoạt động, con trỏ sẽ chuyển sang xác kẻ địch tiếp theo | — | Nhấn và giữ để tua nhanh; Menu R2+ để bỏ qua đoạn văn | — |
| L1/R1 | L / R (chuyển cơ thể không hoạt động của chúng tôi khi bản đồ không hoạt động) | L/R (xoay sân khấu, bài hát trước đó...) | Đánh giá L1; R1 và các tổ hợp phím khác | Trang trước/trang tiếp theo |
| Phím menu ☰ | BẮT ĐẦU | OK (một phần trang) | R2 (hoặc R1) + menu Bỏ qua đoạn | Nhấn nút hiện tại |
| Xem phím ⧉ | - (dành cho chủ nhà) | Mở cài đặt | Mở cài đặt | Đóng cài đặt |
| D-pad/Cần điều khiển bên trái | D-pad/Cần điều khiển bên trái | Di chuyển con trỏ | ↑↓ Tốc độ tự động | ↑↓ Nguồn cấp dữ liệu dòng, ←→ thay đổi trang (trên tab trang ←→ thay đổi trang) |
| Cần điều khiển bên phải | Phím C (lên, xuống, trái và phải; ↑↓ ca khúc chủ đề ±10) | phím C; trang xác nhận trước trận chiến ↓ cũng chuyển hoạt ảnh trận chiến | điều chỉnh kích thước phông chữ lên hoặc xuống | — |
| L3/R3 (nhấn cần điều khiển) | Đối với máy chủ: chuyển đổi ngôn ngữ/gốc và màn hình HD | Tương tự như bên trái | Tương tự như bên trái | Tương tự như bên trái |
| (không có) | Z: đồng nghĩa với L trong danh sách, Z+Start quay về tiêu đề; không có phím nào trên tay cầm và bàn phím vẫn là khoảng trống | — | — | — |
| L4 L5 R4 R5 Phím quay lại | Không được sử dụng | — | — | — |
| Phím Steam, Phím truy cập nhanh | Thuộc sở hữu của Steam | — | — | — |

Những người khác:

- **Đối thoại:** R2 nhấn và giữ tua đi nhanh, menu R2+bỏ qua đoạn hiện tại, L2 chuyển sang đọc tự động (tốc độ cuối cùng được sử dụng khi mở, lần đầu tiên là 2 số; ↑↓ vẫn có thể điều chỉnh tốc độ), L1 mở xem lại (↑↓ cuộn trong xem lại, quay lại L1/A/B). Menu R1+A, R1+ ban đầu vẫn có sẵn (tổ hợp phím R của N64). Triển khai: R2 được chuyển tới đầu đọc dưới dạng R+A trong `input()` của `native_dialogue.cpp`; L2 được gọi là `Reader::toggle_auto`.
- **Trang truyền và xác nhận:** A xác nhận, B quay lại truyền trên trang xác nhận. Không thể thay đổi tên (27-09-2026) và bàn phím ảo không còn cần thiết nữa.
- **Trang xác nhận trước trận chiến:** A xác nhận, B quay lại, L1 đổi vũ khí, linh hồn R1, cần điều khiển bên phải ↓ chuyển hoạt ảnh chiến đấu (công tắc toàn cầu ban đầu `D_8015DDA8` bit2, trận chiến sẽ không vào chương trình sau khi tắt).
- **Bản đồ chiến thuật:** L1/R1 chuyển đổi giữa máy bay không hoạt động của chúng tôi (phiên bản gốc), L2/R2 chuyển đổi giữa máy bay địch và máy bay bên thứ ba (thực hành chiến tranh máy bay hiện đại, [`enemy_cycle.cpp`](../../src/host/enemy_cycle.cpp), xem [L2 / R2 chuyển đổi máy bay địch](../native/enemy-cycle.md)).
- **Khởi động:** Tự động toàn màn hình khi `SteamDeck=1`; Nhấn START trong vòng 2 giây sau khi khởi động sẽ bị bỏ qua (Màn hình quản lý Pak sẽ bị chấm dứt).

## Đặt lối vào (Thêm vào ngày 25-09-2026)

Phản hồi của người dùng: Phiên bản Deck không có mục chuyển trực tiếp ngôn ngữ, HD và các tùy chọn. Nguyên nhân là do lối vào trên Mac nằm ở thanh menu, không có thanh menu trên Deck. Bạn chỉ có thể dựa vào phím xem và không có lời nhắc nào trên màn hình. Giờ đây, hai lối vào hiển thị đã được thêm vào, cả hai đều mở cùng một cửa sổ cài đặt (ngôn ngữ, đồ họa gốc/HD, sửa đổi quy tắc và chuyển đổi giữa các giao diện):

- **Màn hình tiêu đề** (NHẤN BẮT ĐẦU và chuông menu, trạng thái chính của tiêu đề 2, 3): một nút nhỏ ở góc trên bên trái (từ 2026-10-02; góc dưới bên phải dành cho lối vào MOD, xem [Chiến dịch tùy chỉnh](custom-campaign.md) §8). Lời nhắc điều khiển là "Xem cài đặt phím" và bên dưới bàn phím là "Cài đặt...". Nó cũng có thể được mở bằng cách chạm vào màn hình hoặc nhấp chuột. Mac có thanh menu chỉ xuất hiện sau khi nhập bộ điều khiển. Mã nằm trong `home_sync` trong số `frontend.cpp`.
- **Menu chính giữa các trò chơi**: Thêm "Xem cài đặt phím" ở cuối lời nhắc tay cầm.

Một dòng "Ngôn ngữ/Màn hình/Quy tắc..." đã được thêm vào dưới ba mục ban đầu của trang tiêu đề オプション. Người dùng không nên chèn cài đặt máy chủ vào trang cài đặt gốc. Nó đã bị xóa (2026-09-25). Điều người dùng mong muốn là cài đặt "gọi bằng một cú nhấp chuột trong trò chơi": xem phần "Sửa đổi giao diện cài đặt" bên dưới.

Đồng thời, một điều đã được sửa: lời nhắc ở cuối trang xác nhận trước trận chiến và lời nhắc chuyển đổi hoạt hình của HUD trận chiến ban đầu được mã hóa cứng vào bàn phím và tên khóa N64 ("Z/A" "K/C▼"). A, L1, R1, phím điều khiển bên phải ↓ và B hiện được hiển thị dưới tay cầm.

Phần trên chỉ được biên soạn trên Mac và chưa được kiểm tra bằng ảnh chụp màn hình thực tế, cũng như chưa được xác minh trên Deck.

## Sự cố đã biết và sự cố đang chờ xử lý

- **Z + START là "cấp thoát" ban đầu**: nhấn nó trong khi biểu diễn trận chiến sẽ quay trở lại màn hình tiêu đề và logo BANPRESTO, đồng thời tất cả tiến trình chưa được lưu sẽ bị mất (nhánh hủy bỏ ban đầu `801C97E4` chọn chế độ 7 hoặc 0x11, 2026-09-25 Phiên bị bỏ qua bởi hiệu suất trận chiến sẽ trở về tiêu đề, được ghi trong nhận xét mã thăm dò của nó và chưa được gửi). Thì ra L2 cũng là Z, menu L2+ là ngón trỏ trái và ngón cái bên phải, dễ bấm nhầm; bây giờ L2 thuộc về chủ nhà và chỉ còn lại menu Y+ (cả hai đều ở bên tay phải và bạn phải cố tình nhấn vào). Việc có chặn menu Y+ trong khi biểu diễn **tùy theo quyết định của người dùng** hay không.
- **Bỏ qua giữa phần biểu diễn**: Một phiên khác đang thực hiện "Nhấn B trong khi biểu diễn để đi thẳng đến phần cuối biểu diễn", mã chưa được gửi và quá trình xác minh máy thực tế chưa được hoàn tất. Nên nhận dạng R2 trên bộ điều khiển cùng lúc (phù hợp với "R2 tua nhanh" trong đoạn hội thoại, nhắc ghi R2), B vẫn có sẵn; phiên họp đã được thông báo.
- **Phím quay lại không hoạt động**: Chưa sử dụng (không phải bộ điều khiển nào cũng có).
- **Chuyển đổi nhanh giữa ngôn ngữ và HD**: Bàn phím có F7 (ngôn ngữ) và F6 (bản gốc/HD). Hiện tại, tay cầm chỉ truy cập vào cửa sổ cài đặt mà không thêm tổ hợp phím để tránh việc vô tình chạm vào.
- **Xử lý điều hướng của cửa sổ cài đặt**: Đã thay đổi thành phân trang (2026-09-27): Thay đổi trang L1/R1, ↑↓ để di chuyển giữa các cài đặt, ←→ để di chuyển giữa các tùy chọn liên tiếp, xem phần tiếp theo.

## Chỉnh sửa giao diện cài đặt (thực hiện vào ngày 27-09-2026)

25-09-2026 Ảnh chụp màn hình thực tế: Phím xem thực sự mở cài đặt chỉ bằng một cú nhấp chuột, nhưng nó sẽ mở ra một trang "tùy chọn" toàn màn hình, mờ đục (cột quy tắc bên trái, cột bên phải của ngôn ngữ và chuyển đổi giao diện cần được cuộn), giống như trang cài đặt của chương trình máy tính để bàn, bao gồm toàn bộ trò chơi. Điều người dùng mong muốn là “cảm giác gọi tên chỉ bằng một cú nhấp chuột trong game”:

- Tạo lớp nền mờ trên màn hình trò chơi và một bảng ở giữa. Phong cách phù hợp với trang gốc. Khi đóng lại bạn sẽ trở về vị trí ban đầu;
- Một phím để gọi ra, phím tương tự hoặc phím B để đóng: phím xem trên Deck, chờ trên bàn phím (Esc hiện đã thoát khỏi trò chơi);
- Phân trang (ví dụ: chung: ngôn ngữ, màn hình; giao diện: từng chuyển đổi phiên bản gốc/mới; quy tắc: sửa đổi và độ khó; phím: sơ đồ phím), lật trang L1/R1, tùy chọn phím chéo, chuyển đổi A;
- TBD: Có tạm dừng trò chơi khi mở hay không.

Phiên "Cài đặt và kết nối SSH Steam Deck" đề cập đến các hướng tương tự (phân trang, L1/R1, nhất quán với RecompFrontend).

27-09-2026 Triển khai: bảng mờ được đặt trên trò chơi, năm trang (chung: ngôn ngữ, màn hình; giao diện: mỗi chuyển đổi phiên bản gốc/mới; quy tắc; thao tác: bảng phím; về: phiên bản và phông chữ), lật trang L1/R1, tùy chọn phím chéo, A để xác nhận, phím B hoặc xem để đóng, phân trang cuối cùng được ghi vào `presentation.json` và sẽ được sử dụng vào lần tiếp theo. Bàn phím vẫn là Ctrl/Cmd+ để mở, Esc để đóng và Q/E để lật trang. Trò chơi vẫn không tạm dừng. Xem [Cửa sổ cài đặt](../native/settings-window.md) §7 để biết chi tiết. Chưa có ảnh chụp màn hình thực tế.

## Biểu tượng phím

28/09/2026 Đã thực hiện được. Kế hoạch ban đầu là tôi sẽ tự mình vẽ một bộ phông chữ biểu tượng; người dùng đã chỉ ra rằng có một phông chữ chính được tạo sẵn và thay vào đó đã sử dụng **PromptFont** (Yukari "Shinmera" Hafner, SIL OFL 1.1). Zelda64Recomp cũng sử dụng nó; một bản sao (`Zelda64Recomp-reference/assets/promptfont`, 2023-12-29) được bao gồm trong quá trình kiểm tra ngược dòng cố định của máy này nên không cần phải tải xuống riêng. Phạm vi do người dùng đặt: dấu nhắc tay cầm hiển thị biểu tượng phím của bộ điều khiển trên tay và dấu nhắc bàn phím thêm biểu tượng keycap cho các phím chức năng như Esc và Enter; các phím N64 ban đầu không làm được điều này. 30-09-2026 Biểu tượng keycap cũng được sử dụng cho các phím chữ cái, phím số, Backspace, Shift, Alt và Delete (PromptFont được vẽ trên các chữ cái có độ rộng đầy đủ U+FF21–FF3A, các số có độ rộng đầy đủ U+FF10–FF19 và được chuyển sang U+E850–E87D): Người dùng yêu cầu tất cả các nhắc nhở chính đều sử dụng NhắcFont. Trang xác nhận trước trận chiến trước đó có viết “K để bắt đầu trận chiến · Q Chọn vũ khí”. Những thứ duy nhất vẫn có thể viết được là dấu chấm câu và các phím trên bàn phím không có biểu tượng.

### Phông chữ

- NhắcFont đặt các biểu tượng trên các điểm mã thông dụng (mũi tên, ký hiệu toán học). HarmonyOS Sans cũng có 9 trong số đó. Nếu nó chỉ được sử dụng làm phông chữ dự phòng thì nó sẽ không bao giờ được sử dụng. и sẽ được hiển thị dưới dạng một mũi tên bình thường.
- Vì vậy [`build_prompt_font.py`](../../tools/content/build_prompt_font.py) chỉ chọn 99 glyph sẽ sử dụng (chữ cái, số và bốn phím bổ trợ được thêm vào ngày 30-09-2026), di chuyển chúng đến khu vực riêng tư bắt đầu từ U+E800, chia tỷ lệ theo tỷ lệ chiều cao của chữ in hoa của hai phông chữ 700/660 và số đo dọc như được hiển thị trong HarmonyOS Sans SC. `content/fonts/SRW64Prompts.ttf` được tạo có kích thước khoảng 18 KB và được gửi cùng với kho; nó được đổi tên theo OFL, giấy phép và chữ ký ở `LICENSE-SRW64Prompts.txt`.
- Cả hai bộ công cụ văn bản đều kết nối nó với cuối chuỗi phông chữ (RmlUi được đăng ký làm phông chữ dự phòng, công cụ đối thoại nhìn thấy `game_fonts.cpp`) và được `prepare_fonts.py` đưa vào thư mục phông chữ cùng với các phông chữ khác. Trang "Giới thiệu" của cửa sổ cài đặt được ký theo yêu cầu của NhắcFont.
- Lưu ý: `promptfont.h` của Zelda64Recomp và RecompFrontend đảo ngược hai bit mã của phím định hướng bàn phím. Thực ra nó là U+23F5 ở bên phải và U+23F6 ở trên cùng. Phông chữ sẽ chiếm ưu thế.

### Cách viết văn bản

Các dấu được viết trong mục nhập và `expand_prompts()` của [`button_prompts.hpp`](../../src/native/text/button_prompts.hpp) được thay đổi thành ký tự biểu tượng trước khi hiển thị: trang RmlUi được thay đổi trong `label()`, trang tên được thay đổi trước khi chuyển bảng mục nhập và cột dưới cùng của hộp thoại và phần đánh giá được thay đổi trong `dialogue_scene.cpp`. Các phần giữ chỗ như `{n}` không bị ảnh hưởng.

| Đánh dấu | Bộ bài | Xbox | PlayStation | Chuyển đổi |
| --- | --- | --- | --- | --- |
| `{A}``{B}``{X}``{Y}` | A B |
| `{L1}``{R1}``{L2}``{R2}` | L1 R1 L2 R2 | LB RB LT RT | L1 R1 L2 R2 | L R ZL ZR |
| `{View}``{Menu}` | Xem/Thực đơn | Xem/Thực đơn | Tạo／Tùy chọn | − / + |
| `{DPad}``{DUp}` … `{DUpDown}``{DLeftRight}` | Phím chéo (hướng toàn bộ hoặc được đánh dấu) | Tương tự như bên trái | Tương tự như bên trái | Tương tự như bên trái |
| `{LStick}``{RStick}``{RStickUp}``{RStickDown}``{RStickUpDown}` | Cần điều khiển (có mũi tên chỉ hướng) | Tương tự như bên trái | Tương tự như bên trái | Tương tự như bên trái |

Ký hiệu bàn phím giống nhau cho mỗi nhóm: `{Esc}``{Enter}``{Tab}``{Space}``{Ctrl}``{KeyUp}``{KeyDown}``{KeyLeft}``{KeyRight}``{Arrows}``{WASD}``{F5}``{F6}``{F7}` (`{IJKL}` bị xóa khỏi bảng bàn phím cũ; bàn phím mặc định có bố cục PCSX2, xem [Thay đổi phím](../native/controls-remapping.md)).

- Nhóm bộ điều khiển: `SteamDeck=1` Cố định Deck (SDL thấy bộ điều khiển ảo Steam trong chế độ trò chơi và sẽ được coi là Xbox); ngược lại khi nhấn kết nối, `SDL_GameControllerGetType`: PS3/4/5 → PlayStation, Switch Pro → Switch, phần còn lại → Xbox. `input::pad_family` tồn tại và một bản sao cũng được đưa vào ảnh chụp nhanh khung hội thoại.
- Tay cầm Switch hiển thị theo vị trí của nó (OK là phím dưới, Return là phím phải), không in ra nên sử dụng sơ đồ 4 điểm phổ quát của NhắcFont.
- Tất cả 57 mục `_pad` và các mục nhập bàn phím tương ứng, `pad_rstick_down` (công tắc hoạt ảnh của giao diện ban đầu trước chiến tranh), tổng cộng 303 mục nhập bằng ba ngôn ngữ, đã được đổi thành ký hiệu.

### Kiểm tra

- `tests/test_button_prompts.py`: Mọi ký tự được sử dụng trong bảng C++ đều có phông chữ và bit mã gốc đã bị xóa; các ký hiệu trong mục nhập đều đã biết và không có `{{`; các ký hiệu trong ba ngôn ngữ của cùng một mục giống nhau; mục nhập tay cầm chỉ sử dụng dấu tay cầm và mục nhập bàn phím chỉ sử dụng dấu bàn phím; phông chữ và giấy phép có trong danh sách đóng gói.
- `make recomp-button-prompts-test` (`tests/native_button_prompts.cpp`): Kết quả thay thế và phần giữ chỗ của mỗi họ không bị ảnh hưởng.
- Chưa có ảnh chụp màn hình thực tế.

## Kế hoạch xác minh

- **Chèn bộ điều khiển vào giao diện gỡ lỗi:** Phương thức `pad` (`srw64ctl pad r2 l2`) hợp nhất bộ điều khiển ảo vào trạng thái của bộ điều khiển thực (cùng mặt nạ với `srw64_pad_state()`). Bạn có thể chặn các lời nhắc và biểu tượng của bộ điều khiển và kiểm tra L2/R2 trên máy Mac.
- **Kiểm tra ảnh chụp màn hình máy Mac:** Lối vào ở góc dưới bên phải của tiêu đề, phím xem để mở cài đặt, lời nhắc giữa các trò chơi, lời nhắc trang xác nhận trước chiến tranh, mỗi lời nhắc bằng tiếng Trung, tiếng Nhật và tiếng Anh; hai trạng thái của bàn phím và bộ điều khiển.
- **Đơn vị thực tế của bộ bài:** Trong chế độ trò chơi, chỉ sử dụng bộ điều khiển, mở cài đặt từ tiêu đề, chuyển đổi ngôn ngữ và HD, rồi đi qua Tên → Tập 1 → Trận chiến → Liên cảnh → Lưu trữ; xác nhận rằng phím xem có truy cập được trò chơi theo mẫu mặc định.

## Trình tự thực hiện

1. Đặt lời nhắc truy cập và trang xác nhận trước trận chiến; L2 đọc tự động, R2 tua nhanh; Chuyển đổi L2/R2 giữa các kẻ thù trên bản đồ (lần này, nó đã được biên dịch và đã thêm bài kiểm tra đơn vị đọc, chờ ảnh chụp màn hình và máy thực tế).
2. Đưa phần điều khiển của giao diện gỡ lỗi (phương thức `pad` và `srw64ctl pad`, đã thêm) rồi thêm ảnh chụp màn hình máy Mac để kiểm tra.
3. Phông chữ biểu tượng: Thay vào đó hãy sử dụng NhắcFont (thực hiện vào ngày 28-09-2026, xem ở trên).
4. Thay đổi tất cả các mục nhập `_pad` thành ký hiệu (đã hoàn tất).
5. Có một số điều do người dùng quyết định: có chặn menu Y+ trong khi biểu diễn hay không; có bỏ qua lời nhắc R2 sau khi buổi biểu diễn trực tuyến hay không.