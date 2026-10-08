> **Ngôn ngữ / Language:** [Tiếng Việt](native-save-screens.vi.md) · [English](native-save-screens.en.md) · [中文](native-save-screens.md)

# データセーブ Màn hình: Tiếp quản tự nhiên thanh lưu trữ và lựa chọn phương tiện

Ngày: 23-09-2026. Mục menu tương tác 1. Hai màn hình gốc (màn hình số 1 và 9) được trang RmlUi tiếp quản và giữ nguyên bố cục ban đầu; trang này chạy máy trạng thái của riêng nó và chỉ gọi các quy trình đọc tiêu đề lưu trữ ban đầu và quy trình ghi SRAM/コントローラパック. Bạn có thể chọn lại màn hình gốc trong "Màn hình giữa phiên" trên trang cài đặt, xem [Menu chính giữa phiên](native-intermission-menu.md).ロード của màn hình tiêu đề sử dụng lại cùng một trang (`context` là `title`), hãy xem [Màn hình menu tiêu đề](native-title-menus.md).

## 1. Màn hình gốc (phân tích tĩnh)

Các tọa độ đều là 320 × 240. Việc tháo gỡ lấy các nhận xét hướng dẫn từ đầu ra biên dịch lại; bảng bố cục `D_800C8BB8` có 24 byte cho mỗi mục, từ thứ hai là bảng nhãn `{文本号,x,y,0}` và từ thứ ba là danh sách hiển thị hình chữ nhật được điền (`G_FILLRECT`, 10 bit cho mỗi tọa độ).

### Lựa chọn phương tiện (Màn hình 1)

| Dự án | Cơ sở |
| --- | --- |
| Bố cục 0x6A: hộp tùy chọn (117,61)–(203,99), nhãn ROMカートリッジ (0xFD9) (124,63), コントローラパック (0xFDA) (124,83); hộp tin nhắn (85,125)–(235,147), gắn thẻ にセーブします. (0xFDC)(169,128) | Bảng bố trí |
| Khởi tạo `801CEA30`: `80085B94(0,1)` nền tối (bao gồm số ngẫu nhiên), bố cục, `801C6620` vẽ tên phương tiện con trỏ vào (90／88,128) và ghi lại ô văn bản `D_801DD0B0`; con trỏ sprite 0x14 (87,61) liên kết 116×20 `D_801DEBC8` (trung bình: 0 ROM, 1 Pak); nhạt dần; `D_801DDA30=0`, `D_801DECD8=0` | `801CEA30` |
| Mỗi khung hình `801CEABC`: Khi không có thông báo nào được phát, B → âm thanh 0xB8, mờ dần, hình ảnh tiếp theo 0; A → âm thanh 0xB7, bố cục cửa sổ 0x72 (khung (101,109)–(219,131), nhãn (0xFDD) (112,112)), `D_801DDA30=1`, `D_801DECD8=30`; đếm ngược khi tin nhắn xuất hiện, về 0 → `D_801DD0A2=0` (con trỏ cột lưu trữ), màn hình tiếp theo 9, mờ dần. Khi không có thông báo nào được phát, hãy chạy con trỏ `801C4A20` mọi khung hình và vẽ lại tên phương tiện `801C6680` khi nhấn phím lên và xuống (`D_801DD62C & 0xC00`) | `801CEABC` |

### Cột Lưu trữ (Màn hình 9)

| Dự án | Cơ sở |
| --- | --- |
| Bố cục 0x73: hộp tiêu đề (117,21)–(203,43); hai cột (21,69)–(299,139), (21,149)–(299,219), nhãn セーブデータ (0xFDE) (90,72), (90,152); khung avatar (21,y)–(87,y+70) được đặt bởi sprite của `801C6260` | bảng bố trí, ảnh chụp màn hình |
| Khởi tạo `801CECE8`: nền, bố cục; tên phương tiện (0xFD9/0xFDA) (122,26); Trước tiên hãy đóng gói `80094168(0)` → `D_801DD116`, ≥2 rồi đến `801CE578` nhắc, `D_801DECD8=2`; nếu không thì `80085CD4(介质, D_801DD118)` Đọc hai cột tiêu đề lưu trữ; Số cột `"1"`/`"2"` (140,72/152); `801C66B8` Vẽ các cột đã sử dụng; Con trỏ sprite 0x14 (89,69/149) 209×19 Liên kết `D_801DD0A2`; `D_801DECD8=0`; Làm mờ dần | `801CECE8` |
| Bản ghi tiêu đề lưu trữ `D_801DD118`, mỗi cột 0x18: `+0` được sử dụng; `+2` sáu mã glyph tên (`0x801C2698`, mã giống như trang nhập tên, khoảng trống 0x1549); `+0xE` nhân vật chính loại 0–3 (0x19–0x1C trong bảng nội dung lưu trữ) một); cấp độ `+0xF`; `+0x10` số từ (`0x801C264F`); `+0x11` số tiêu đề chương (`0x801C2651`, văn bản `0x119+`); `+0x12` tổng số vòng (u16, `0x801C264C`); `+0x14` tiền (u32, `0x801C2654`). Đầu đọc ROM `80092744(栏)`, Đầu đọc Pak `80093F4C(栏)` | `80085CD4` |
| Cột đã sử dụng `801C66B8` (y=69＋80n): hình đại diện `801C6260(n, 类别, 21, y)`, tài nguyên `D_801DC680[类别]`=hình ảnh `0x51C+类别`, bảng màu `0x520+类别`; tên `801D920C` (160,y+3);レベル(0xFE1)(248), cấp độ `%2d` (280); Số (0xFD7)(90,y+20), số từ `%2d` (104); tiêu đề `0x119+号` (89,y+37), theo sau làクリア (0xFE0); 総ターンsố (0x101B) (90,y+54), `%3d` (146); Quỹ (0x1019) (192), `%8d` (232) | `801C66B8` |
| Mỗi khung hình `801CEEF8`, chế độ `D_801DECD8`: **0** B → âm thanh 0xB8, mờ dần, hình tiếp theo 1; A → âm thanh 0xB7, nếu trường trống, hãy viết (ROM `80092678(栏)`; Pak trước `80094168` sau đó `80093FD4(栏)`), `D_801DD116==0` Sau đó mờ dần, màn hình tiếp theo 9 (nhập lại), nếu không `801CEC00` sẽ xóa văn bản elf, `801CE578` bật lên lời nhắc, chế độ 2; nếu cột được sử dụng, hãy mở bố cục cửa sổ 0x74 (khung (53,101)–(267,139), ghi をUpdateします (0xFE3) (56,104), よろしいですか? (0xFE4) (56,120),はい／いいえ. (224,128)/(224,148), hộp tùy chọn (221,122)–(251,163)), con trỏ 0x15 giới hạn `D_801DDA08`, chế độ 1. **1** B hoặc A trong いいえ → Đóng cửa sổ, chế độ 0; A trong はい → Tương tự như viết. **2** Mỗi khung hình `800906A0`; B → mờ dần, hình tiếp theo 1; A → `80090844(0x8015F508,0)` đã sửa khi trạng thái 7, nếu không thì `80094168(0)` kiểm tra lại, <2 hoặc thay đổi trạng thái, mờ dần và nhập lại ảnh 9. Khi chế độ <2 và phương tiện là Pak, mỗi khung hình `8009412C`, không phải 0 (Pak được kéo ra) → Lời nhắc bật lên trạng thái 2, chế độ 2 | `801CEEF8` |
| Mẹo `801CE578`: Bố cục cửa sổ 0x8C (khung (29,77)–(291,179)), nhấn `D_801DD116` để đặt văn bản: 2/3 → 0x1A8 (80,86), 0x1AA (80,106), 0x1AE (104,126), 0x1AF (72,156); 4 → 0x1BC, 0x1BD, 0x1BE, 0x1BF, 0x1AF; 5 → 0x1B7, 0x1BA, 0x1BB, 0x1AF; 6 → 0x1B3, 0x1B4, 0x1C0, 0x1AE, 0x1B0; 7 → 0x1A9, 0x1B8, 0x1B9, 0x1B2, 0x1B5, 0x1B6, 0x1AF | `801CE578` |

Máy chủ không có コントローラパック: `80090778` (`osPfsIsPlug`) bị `game_hooks.cpp` tiếp quản để "không có Pak nào được lắp vào bốn bộ điều khiển" và đường dẫn Pak ổn định chuyển sang trạng thái 7 (cần sửa chữa).

## 2. Phương thức tiếp quản

Mã nguồn: [`save_page.cpp`](../../src/host/save_page.cpp) (bộ chuyển đổi chủ đề trò chơi), bao bì của [`frontend.cpp`](../../src/native/ui/frontend.cpp)'s `save_sync` (trang), [`game_hooks.cpp`](../../src/host/game_hooks.cpp) (`save_build`/`save_step`/`save_frame`, bốn móc trong `generate_cpu.py` của `NATIVE_HOOKS`). Khi phiên bản gốc được chọn trong "Màn hình liên trường" của trang cài đặt, cả hai lối vào công trình sẽ được đưa về màn hình gốc; `SRW64_NATIVE_SAVE=0` hoặc khi hồ sơ không được tải, màn hình gốc sẽ được giữ lại trong suốt quá trình chạy.

| chức năng ban đầu | giấy gói |
| --- | --- |
| `801CEA30` Khởi tạo lựa chọn phương tiện | Không điều chỉnh chức năng ban đầu. Giữ các cuộc gọi trong nền (bao gồm các số ngẫu nhiên), xóa `D_801DDA30`, `D_801DECD8` |
| `801CEABC` lựa chọn phương tiện trên mỗi khung hình | Con trỏ được ghi bởi bộ điều hợp `D_801DEBC8`; xác nhận được thiết lập bởi bộ điều hợp `D_801DDA30=1`, `D_801DECD8=30` và hiển thị データを动べています. , sau đó mỗi khung trả về hàm đếm ngược và chuyển tiếp ban đầu (không có gì được rút ra); quay lại và tiêm B |
| `801CECE8` Khởi tạo cột lưu trữ | Không điều chỉnh chức năng ban đầu. Giữ nền; `80094168` trạng thái xác định khi Pak, nếu không thì `80085CD4(介质, D_801DD118)` Đọc hai cột |
| `801CEEF8` Mỗi khung của thanh lưu trữ | Không điều chỉnh chức năng ban đầu (A và Pak ban đầu kéo nhánh ra và tự vẽ cửa sổ bật lên). Bộ điều hợp tuân theo trạng thái ban đầu của máy: ghi cuộc gọi `80092678`/`80094168`+`80093FD4`, mờ dần thành công và vào lại màn hình 9, không vào được chế độ nhắc; chế độ nhắc nhở mọi khung hình `800906A0`, A tiến hành `80090844`/`80094168` kiểm tra lại; chế độ <2 và Thời gian Pak trên mỗi khung hình `8009412C` |

**Ảnh chụp nhanh**: `status.save_page`: `screen` (`choice`/`slots`), `serial`, __INL_ CODE_117__ (rom, pak, save_to, kiểm tra, slot, cấp độ, tập, xóa, lượt, nạp tiền, ghi đè, hỏi, có, không); tùy chọn phương tiện là `cursor`, `waiting`; cột lưu trữ có `medium`, `cursor`, `mode` (0 danh sách, 1 xác nhận ghi đè, 2 lời nhắc), `window_cursor`, `status`, `slots[]` (`index`, `used`, `name`, __INL_CODE _129__, `level`, `episode`, `title`, `turns`, `funds`, `art`), chế độ nhắc nhở được bổ sung `message[]` (`text`, `x`, `y`). nhật ký sự kiện `save-page-events.jsonl` (`open`, `choose`, `window-open`/`window-close`, __INL_COD E_145__, `recheck`, `pak-removed`, `back`, `close`/`left`).

**GỠ LỖI**: ID ổn định `save:N` (phương tiện hoặc thanh lưu trữ), `save-yes`/`save-no`; bàn phím ↑↓, Enter/Z, Esc/X; điều kiện chờ `save_page`.

## 3. Xác thực máy thật

```sh
.venv/bin/python tools/recomp/debug/check_save.py            # 构建、读第一话存档并检查
.venv/bin/python tools/recomp/debug/check_save.py --reuse-build
```

Lưu trữ `intermission-cold-1.source.sram` (Đã xóa Chương 1, Cột 1 Malina Cấp 2, Chương 1 "Out! スイームルグ", 7 vòng, 14500). Đang chạy `build/recomp/debug/20260923T044601.424135Z/`: `save-checks.json` đã vượt qua 19 mục, mã thoát 0.

| Kiểm tra | Kết quả |
| --- | --- |
| Lựa chọn phương tiện | Con trỏ 0, ↓ đến コントローラパック, Z rồi データを动べています. (`waiting`) Vào thanh lưu trữ trong khoảng nửa giây |
| Cột Lưu trữ | Cột 1 Tên được giải mã từ mã glyph "Mama" và hình đại diện là mặt số 28 (loại 3) trên trang nhập tên; Cột 2 trống |
| Viết vào cột trống | ↓ Cột 2, Z: `80092678(1)` sau đó màn hình sẽ nhập lại và nội dung cột 2 và cột 1 trùng khớp |
| Xác nhận ghi đè | Z mở cửa sổ ở cột 1, ↓ いいえ, Z đóng cửa sổ; mở lại cửa sổ はい và nhập lại sau khi viết |
| Quay lại Pak |

So sánh phiên bản gốc (`build/recomp/debug/20260923T041741.927962Z/save-*.png`, `80090778` ảnh gốc sau khi móc có hiệu lực): bố cục nhất quán; phiên bản gốc trong hộp nhắc chia cùng một dòng thành hai đoạn văn bản (ví dụ: 0x1B8+0x1B9) và trang được hợp nhất thành một dòng bằng cách nhấn y.

## 4. Cột mở rộng (2026-10-01)

Để biết về thiết kế, hãy xem [Cột lưu trữ đa dạng và tự động lưu trữ](../design/save-slots-autosave.md). Ứng dụng độc lập chuyển thư viện lưu trữ (thư mục người dùng `saves/`) đến máy chủ thông qua `SRW64_SAVE_LIBRARY`; khi không được đặt (phiên gỡ lỗi, `check_save.py`), chỉ có hai cột, hoạt động tương tự như trên.

- **Định tuyến lại**: [`save_store.cpp`](../../src/host/save_store.cpp) kết thúc `80090E5C` (`NATIVE_HOOKS` đổi tên `srw64_original_sram_transfer`). Trong một thao tác, trang sử dụng `save_store::Window` để ánh xạ cột trò chơi 0/1 tới cột mở rộng. Việc đọc và ghi địa chỉ `0x10`/`0x1F10` và độ dài 0x1F00 được thay đổi thành đọc và ghi `saves/slots/NNN.rec`. Sau khi ghi và chạy `80092678` (tuần tự hóa, ghi, đọc lại và so sánh) theo phiên bản gốc thì file đọc lại là file vừa ghi.
- **Xuất bản ngay lập tức**: Phần còn lại của nội dung ghi vào băng cassette như bình thường và một bản sao của băng cassette trong máy chủ được cập nhật cùng lúc; bản sao được xuất bản ngay lập tức dưới dạng `saves/cartridge.sram` khi tiêu đề tệp và tổng kiểm tra chính xác. `0x78F0` Các khối được chia sẻ không được xuất bản khi được viết riêng lẻ và được viết cùng với các cột tiếp theo. Không có tiêu đề tệp trong quá trình định dạng trò chơi mới và nó sẽ không được xuất bản.
- **Danh sách**: Sau 2 cột của băng cassette là cột mở rộng hiện có, số trống nhỏ nhất sẽ được thêm vào khi lưu trữ. Tiêu đề lưu trữ của cột mở rộng được ánh xạ và đọc từ `80085CD4` gốc (hai cột một lần). Sau khi đọc xong, đọc lại hai cột của băng cassette, bảng tiêu đề lưu trữ được khôi phục về trạng thái ban đầu. Còn nhiều trạng thái trang khác: `count`, `page`, `pages`, `slots[]`. Chỉ có hai cột được đặt trên trang hiện tại, với `number` (số cột) và `index` (vị trí danh sách), `cursor` là vị trí danh sách; con trỏ của trò chơi chỉ ghi 0/1.
- **Giao diện**: Giữ nguyên bố cục hai cột ban đầu, hai cột trên mỗi trang. ↑↓ Đi hết các cột, ←→ lật trang; dấu phía trên bên trái của trang 1 là "カートリッジ" và phía trên bên phải là số trang. Thay vào đó, hãy nhắc sử dụng `save_slots_hint_pages`/`title_load_hint_pages`.
- **Đọc tiêu đề**: Khi chọn cột mở rộng `save_store::arm_load(栏号)`, viết con trỏ trò chơi là 0, sau đó đưa cho phiên bản gốc để xác nhận; sau một vài khung, phủ `80092C70(0)` giữa các trường và đọc cột 0 để lấy tệp này và giải phóng nó sau khi đọc. Cũng được phát hành khi quay lại vòng tiêu đề, mở lại danh sách cột hoặc màn hình lưu giữa các trò chơi.
- **Màn hình gốc**: Khi chuyển về phiên bản gốc trong cài đặt, màn hình gốc chỉ hiển thị hai cột của băng cassette và việc ánh xạ không có hiệu lực.
- **Nhật ký sự kiện**: `save-store-events.jsonl` (`open`, `slot-write`, `slot-read`, `publish`, `arm`, `disarm`, `*-error`).

Máy thật: `tools/recomp/debug/check_save_slots.py`, chạy hai vòng với thư viện lưu trữ mới và vượt qua 14 mục:

- Vòng 1: Danh sách cột 1, 2 và cột 3 trống; sau khi lưu trữ trong cột 3, `003.rec` (cặp tổng kiểm tra) được tạo và tệp băng cassette không thay đổi; ← quay lại trang 1; cột 3 bị ghi đè và viết lại sau khi xác nhận; khi băng cassette cột 2 được lưu trữ, băng cassette sẽ được giải phóng ngay lập tức và còn lại `.prev`.
- Vòng 2: Đầu tiên đổi quỹ `003.rec` thành 123456 và tính lại tổng kiểm tra. Cột 3 trong danh sách đọc tiêu đề hiển thị 123456. Sau khi đọc tệp, quỹ trong menu liên trang là 123456. Có `slot-read` trong cột 3 trong nhật ký và tệp cassette vẫn không thay đổi.
- Ảnh chụp màn hình: `build/recomp/save-slots-check/<时间>/`. `check_save.py` (16 mục nhập) không có thư viện lưu trữ cũng được coi là `check_title_menus.py --skip-karaoke` (16 mục nhập).

Tự động lưu trữ và xóa (01-10-2026): Danh sách tiêu đề ロード được liệt kê trong phần lưu trữ tự động sau cột mở rộng (`kind` là `intermission`/`turn`, với `time`; tiêu đề, vòng, quỹ, tên của vòng đã lưu trữ là từ việc đọc khối tiến trình +0x26C của bản ghi, không có cấp độ và hình đại diện); trạng thái trang có thêm `tools` (mục bên dưới con trỏ có thể xóa được không) và chế độ 3 (xác nhận xóa). Nhấn R để xóa và nhắc sử dụng `save_slots_hint_delete`/`title_load_hint_delete` thay thế. Không có chức năng ghi chú cột. Để biết cách thực hành và xác minh, hãy xem [Tài liệu thiết kế](../design/save-slots-autosave.md) §8.

## 5. Chưa được xác minh

- Chỉ phương tiện SRAM mới thực sự được ghi; đường dẫn コントローラパック luôn là dấu nhắc (trạng thái 7) vì máy chủ không có Pak và các nhánh viết và sửa chữa chỉ có phân tích tĩnh.
- Lời nhắc bằng văn bản cho các trạng thái 2–6 được sắp xếp theo tọa độ tháo gỡ và không có ảnh chụp màn hình thực tế để so sánh.