> **Ngôn ngữ / Language:** [Tiếng Việt](native-title-menus.vi.md) · [English](native-title-menus.en.md) · [中文](native-title-menus.md)

# Màn hình menu Tiêu đề: tiếp quản bản địa của ロード, オプション, サウンドセレクト, カラオケモード

Ngày: 24-09-2026. Màn hình sau bốn mục trong menu tiêu đề.ロード sử dụng lại [trangデータセーブ](native-save-screens.md) và thay đổi nó thành bản sao và quy trình đã đọc; オプション và hai danh sách bài hát đều là trang mới ([`title_page.cpp`](../../src/host/title_page.cpp)). Trang chỉ chịu trách nhiệm vẽ và chức năng trạng thái ban đầu tiếp tục quản lý việc mở khóa, cuộn, phát bài hát và chuyển đổi lớp phủ. Việc lựa chọn trang được giao cho họ dưới hình thức nhấn nút. Bạn có thể chọn quay lại màn hình gốc trong "Màn hình menu tiêu đề" của trang cài đặt. Tên của bốn mục trên menu chuông được hiển thị trong [Màn hình tiêu đề và hình ảnh văn bản lô](native-title-and-story-images.md).

## 1. Màn hình gốc (phân tích tĩnh)

Lớp phủ tiêu đề là `load_0010DA50` (RAM `801C4500`, ROM `0x10DA50`, BSS bắt đầu từ `0x801CC150`, không bị xóa khi tải lại). Mỗi tác vụ khung `801CA9CC` trước tiên nhìn vào trạng thái mờ dần và mờ dần `80099B30()`: chỉ khi khác 0 hoặc 2 thì nhấn trạng thái chính `D_801CC3A6` tra bảng `D_801CB250` để điều chỉnh chức năng trạng thái và trạng thái phụ là `D_801CC3A7`. Các tọa độ đều là 320 × 240.

### Menu chuông và nơi để đi

| Dự án | Cơ sở |
| --- | --- |
| Con trỏ `D_801CC3AC`: 0 スタート, 1 オプション, 2 コンティニュー, 3 ロード. Giữ con trỏ phải +1, con trỏ trái -1. Sau khi nhấn A hoặc BẮT ĐẦU, trạng thái chính = con trỏ + 4, hiệu ứng âm thanh gốc sẽ không được phát ở đây và sẽ được phát ở màn hình tiếp theo | `801C6514`, `801C642C` |
| Tên vật phẩm chỉ là các họa tiết (cảnh 652–655). Không có chuỗi nào như vậy trong bảng văn bản, vì vậy một `title_start/load/continue/option` bổ sung sẽ được thêm vào thẻ `ui` | bàn cảnh |
| Quay lại menu vòng để thống nhất trạng thái chính 7 Trạng thái phụ 0xC `801C7BE0`: Vẽ lại logo và ngọn lửa, xây dựng lại vòng theo con trỏ hiện tại, BGM 0x1E; Trạng thái phụ 0xD `801C7C48` Quay lại trạng thái chính 3 sau khi quá trình mờ dần hoàn tất | `801C7BE0` |
| **コンティニュー (trạng thái chính 6) không có hình ảnh**: `8009365C` đọc SRAM `0x3E10` và bắt đầu 0x3AE0 byte dữ liệu ngắt; nếu không hợp lệ, nó sẽ phát còi 0xBA và ở lại võ đài, nếu hợp lệ, nó sẽ chuyển chế độ 0x11 và quay thẳng về bản đồ chiến thuật | `801C6D1C` |
| **キャラクターリスト (trạng thái chính 9), ロボットリスト (trạng thái chính 10) không thể truy cập được**: khởi tạo `801C8F1C`, `801C96FC` Không có người gọi trong toàn bộ ROM và không có mã để ghi trạng thái chính là 9 hoặc 10. Nó sẽ không xuất hiện sau khi vượt qua cấp độ | Quét tham chiếu toàn bộ ROM |

### オプション (trạng thái chính 5)

| Dự án | Cơ sở |
| --- | --- |
| Bản dựng `801C697C`: Khe miễn phí 2–6 (vòng) và 9 (ngọn lửa); bố cục 0x5A đến ô 0x2E, hộp tiêu đề (133,21)–(187,43) vẽ オプション(0xE1), hộp vật phẩm (109,84)–(213,139) vẽサウンド(0x3EF),サウンドセレクト(0xE2), カラオケモード(0xE5), nhãn giá trịステレオ(0x3F0)/モノラル(0x3F1) được rút ra ở (176,90). Khe con trỏ 0x27 là (110,87+16n). Tổng cộng 3 vật phẩm, không có vật phẩm ẩn | `801C697C` |
| Mỗi khung `801C6B14`: Phím lên và xuống xoay vòng con trỏ `D_801CC397`. A nằm trong mục 0: `D_8015DDA8=(D_8015DDA8^1)&0xFB`, `8009187C` ngay lập tức ghi lại byte thứ 7 của tiêu đề SRAM, `80076D90(bit0)` chuyển kênh âm thanh. A ở mục 1 và 2: Cùng một khung gọi `801C86A8`/`801C9888` để tạo danh sách. B: Làm mờ dần, quay lại menu tròn | `801C6B14` |
| Byte thiết lập `D_8015DDA8`: bit0 là mono, bit2 là bit tạm thời của bản đồ chiến thuật (nó sẽ bị xóa mỗi khi ghi cài đặt), bit3 đã bị xóa (kết thúc được đặt) | `8009171C`, `8009187C` |

### サウンドセレクト (trạng thái chính 8) và カラオケモード (trạng thái chính 11)

| Dự án | Cơ sở |
| --- | --- |
| Xây dựng `801C86A8`/`801C9888`: `801C4850` sạch, dừng BGM; bố cục 0x5B/0x61 vẽ khung toàn màn hình (21,21)–(299,219), tiêu đề (80,25), EXIT (0xE6) (248,25); `801C81C0(0／1)` Tạo danh sách, `801C83D0` vẽ 10 dòng (x=80, y=52+16r); bố trí mũi tên 0x5C trong khe 0x2F | `801C86A8`, `801C9888` |
| Biến danh sách: `D_801CC190` Số lượng mục, `D_801CC192` Mục hiện tại, `D_801CC194` Số dòng trong cửa sổ (0–9), `D_801CC196` Mục đầu tiên trong cửa sổ, `D_801CC198[]` là chỉ số dưới bảng | `801C81C0` |
| Mỗi mục trong danh sách nhạc là {text number, music number}: サウンドセレクト sử dụng `D_801CB290` (49 mục, văn bản 0xE8–0x118) và カラオケモード sử dụng `D_801CB354` (19 mục). Số bài hát hiện đang được phát là `D_800FFA6C` | đoạn dữ liệu |
| Điều kiện mở khóa: F91 ガンダム出撃, 行けザンボット3, ゴーショーグン発进せよ yêu cầu xem máy tương ứng (`80091670`, bit minh họa `D_8010F520`); Đất Xanh yêu cầu `D_8015DDA8 & 8`, nghĩa là vượt qua cấp độ.カラオケ's ザンボット3, ゴーショーグン hai bài hát giống nhau | `801C81C0` |
| Mỗi khung của danh sách `801C8724`/`801C9904`: lên xuống (đọc các từ liên tiếp `D_801612E0`) di chuyển và cuộn qua `801C8520`. Nhấn vào mục đầu tiên sẽ chuyển tiêu điểm sang EXIT (trạng thái phụ 1, `801C89E4`/`801C9ADC`).サウンドセレクト: A phát bài hát (phát lại từ đầu khi phát cùng một bài hát), B chỉ dừng bài hát khi phát bài hát và quay lại オプション khi không phát, Z/L (0x2020) và R (0x10) di chuyển lên hoặc xuống một bài hát và phát bài hát đó ngay lập tức.カラオケモード: A viết `D_80172D08=曲号`, chuyển sang chế độ 0x1A, tham gia chiến đấu và phủ lên trận chiến trình diễn và lời bài hát; sau khi kết thúc, quay lại tiêu đề cổng 1 ở chế độ 0x1B, di chuyển con trỏ đến bài hát vừa nãy | `801C8724`, `801C9904` |

### ロード (trạng thái chính 7)

Bố cục màn hình và định dạng tiêu đề lưu trữ giống với định dạng của データセーブ trong trường này. Sự khác biệt nằm ở văn bản và quy trình:

| tiểu bang | Chức năng | Hiệu ứng |
| --- | --- | --- |
| 3 | `801C709C` (Bản dựng `801C6F3C`) | Lựa chọn phương tiện truyền thông. Trung bình `D_801CC359`; tin nhắn là からロードします. (0x1E3). A: Pak `D_801CC37C=80094168(1)`, sau đó mở "データを动べています." cửa sổ, `D_801CC368=0`, nhập 4; B: Lặp lại |
| 4, 5 | `801C71C0`, `801C777C` | Kiểm tra tình trạng đứng hình (ROM 7 khung hình), mờ dần. Khi Pak và trạng thái khác 0 thì gọi `801C7C90(状态)` thành 0xE, ngược lại gọi `801C7328` để tạo cột lưu trữ |
| 7 | `801C783C` (bản dựng `801C7328`) | Thanh lưu trữ. `80085CD4(介质, 0x801CC158)` Đọc hai cột của tiêu đề lưu trữ, con trỏ `D_801CC358`. A Ở cột trống: buzzer; trong cột có dữ liệu: bật. Ghi を読み込みます. (0x1E4)／よろしいですか? Cửa sổ xác nhận, `D_801CC150=0`, nhập 0xA. `8009412C` phát hiện xem có kéo ra mọi khung hình hay không khi Pak |
| 0xA | `801C7A48` | Cửa sổ xác nhận.はい: `80080188(ROM 0x12+栏，Pak 0x14+栏)` rồi mờ dần. Việc đọc tệp thực tế được thực hiện trong `801D8F74` của lớp phủ liên trường, sau đó vào menu chính của liên trường.いいえ hoặc B: quay lại 7 |
| 0xE |

## 2. Phương thức tiếp quản

Mã nguồn: [`title_page.cpp`](../../src/host/title_page.cpp) (bộ chuyển đổi chủ đề trò chơi cho オプション và danh sách bài hát), [`save_page.cpp`](../../src/host/save_page.cpp) `title_*` (ロード), [`frontend.cpp`](../../src/native/ui/frontend.cpp)'s `title_sync` (オプション và trang danh sách bài hát; ロード vẫn được thực hiện bởi `save_sync``SRW64_TITLE_BUILD`/`SRW64_TITLE_STEP` gói của [`game_hooks.cpp`](../../src/host/game_hooks.cpp). 16 chức năng đã được đổi tên thành `srw64_original_title_*` trong `NATIVE_HOOKS` trong số `generate_cpu.py` Sau khi thay đổi, `generate_cpu` phải được chạy lại.

| chức năng ban đầu | giấy gói |
| --- | --- |
| `801C697C` オプション Xây dựng | Không điều chỉnh chức năng ban đầu. Chỉ miễn phí các ô 2–6 và 9, sau đó mở trang |
| `801C6B14` オプション trên mỗi khung hình | Di động: được ghi bởi bộ điều hợp `D_801CC397` và phát sóng 0xB9.サウンド: Bộ điều hợp tự hoàn tất quá trình chuyển đổi, `8009187C`, `80076D90` (nhánh ban đầu sẽ rút các từ vào khe thẻ có thể đã hết hạn). A và B của các mục khác: gọi hàm ban đầu bằng cách nhấn một phím và để nó gọi cấu trúc danh sách nối hoặc tắt dần vòng lặp |
| `801C86A8`／`801C9888` Xây dựng danh sách | Không điều chỉnh chức năng ban đầu. Thực hiện `801C4850`, `8007E810(-1)`, `801C81C0(0／1)` rồi mở trang |
| `801C8724`, `801C89E4`, `801C9904`, `801C9ADC` Liệt kê từng khung | Chức năng ban đầu được điều chỉnh cho từng khung hình (cần theo dõi xem bài hát có đang phát hay không, hành vi của B phụ thuộc vào điều này). Dùng các phím viết chữ lên xuống liên tục, A, B, Z, R viết vào khung hiện tại và nhấn chữ; khi một dòng nhất định được nhấp vào, biến danh sách sẽ được bộ điều hợp thay đổi; sau khi điều chỉnh xong, mũi tên của khe 0x2F được nhả ra |
| `801C83D0` Danh sách rút thăm | Chuyển sang trạng thái không hoạt động và gửi lại trang. Nó cũng sẽ được gọi trong quá trình quay lại và mờ dần của カラオケ, và trang sẽ theo con trỏ ở đây |
| `801C6F3C`, `801C709C`, `801C7328`, `801C783C`, `801C7A48`, `801C7C90`, `801C8074` ロード | Nhấn phương pháp [データセーブ](native-save-screens.md): Chức năng xây dựng không điều chỉnh chức năng ban đầu và việc đọc tiêu đề lưu trữ, chuyển đổi phương tiện, cửa sổ xác nhận và lời nhắc Pak được bộ điều hợp xử lý theo trạng thái ban đầu của máy. B. はい trong cửa sổ xác nhận và A/B trên trang nhắc nhở. Sau khi ghi các biến, nhấn nút để gọi hàm gốc, hàm gốc sẽ mờ dần hoặc chuyển chế độ |
| `801CA9CC` Tác vụ trên mỗi khung hình | Kiểm tra trạng thái chính sau khi chức năng gốc kết thúc: đóng trang khi không ở trạng thái chính tương ứng hoặc đã đạt trạng thái phụ 0xD |

**chuyển đổi lớp phủ**: phát カラオケ, xác nhận ロード, コンティニュー sẽ cho phép cài đặt các lớp phủ khác vào `801C4500`. `overlay_loaded` Miễn là phạm vi mới được tải trùng với `801C4500–801CC150`, trang sẽ bị đóng dưới dạng khung và BSS của lớp phủ tiêu đề sẽ không được đọc nữa.

**Phiên bản gốc/mới**: Trang cài đặt "Màn hình menu tiêu đề" (`title_ui` của `presentation.json`, giao diện gỡ lỗi `settings {"title_ui": "original"}`). Nó sẽ có hiệu lực vào lần mở màn hình tiếp theo, bao gồm ロード, オプション, サウンドセレクト, và カラオケモード.

**Trang**: Theo vị trí ban đầu của khung, tiêu đề, EXIT, tên bài hát 10 dòng và mũi tên lên xuống; thêm ► trước tên bài hát của bài hát đang được phát và thay đổi văn bản thành màu xanh nhạt khi nó không nằm trong dòng con trỏ.

**Văn bản**: Tiêu đề, dự án và tên bài hát đều được tìm nạp từ bảng văn bản thông qua `dialogue::ui_text`, theo ngôn ngữ đọc; ロード thay thế hai câu bằng 0x1E3 và 0x1E4 trong môi trường tiêu đề. Tên bài hát (text 0xE8–0x118) hiện tại chưa có trong bảng nhập dữ liệu nên tên gốc tiếng Nhật vẫn hiển thị ở giao diện tiếng Trung và tiếng Anh.

**Ảnh chụp nhanh**: Các trường `status.title_page` như sau và các sự kiện được viết bằng `title-page-events.jsonl`.

- Phổ biến: `screen` (`options`/`sound`/`karaoke`), `serial`, `title`.
- オプション: `items[]` (`label`, và tùy chọn `value`), `cursor`, `mono`.
- Danh sách bài hát: `songs[]` (`text`, `song`, `playing`), `current`, `top`, `rows`, `exit`, `exit_focus`.
- ロード: Sử dụng `status.save_page`, cộng với `context` (`title` hoặc `intermission`).

**Gỡ lỗi**: ID ổn định là `tp-option:N`, `tp-song:N`, `tp-exit`; bàn phím ↑↓, Q/E (bài hát trước/tiếp theo), Enter/Z, Esc/X.

## 3. Xác thực máy thật

```sh
.venv/bin/python tools/recomp/debug/check_title_menus.py              # 中文界面，含 カラオケ
.venv/bin/python tools/recomp/debug/check_title_menus.py --skip-karaoke
```

Lưu trữ `intermission-cold-1.source.sram` (đã xóa tập đầu tiên). Đang chạy `build/recomp/debug/20260924T070500.307818Z/`: `title-checks.json` Đã vượt qua tất cả 18 mục. Sau khi thay đổi phần đệm nút và dấu "hiện đang phát" của danh sách bản nhạc, tôi chạy lại danh sách đó với `--skip-karaoke` (`build/recomp/debug/20260924T071216.285758Z/`) và tất cả 16 mục đều đạt. Giao diện tiếng Trung đã xóa khoảng trắng giữa tên phương tiện và câu rồi chạy lại (`build/recomp/debug/20260924T071435.026778Z/`) và tất cả 16 mục vẫn vượt qua.

| Kiểm tra | Kết quả |
| --- | --- |
| オプション | Ba mục: âm thanh/đánh giá âm nhạc/chế độ karaoke, con trỏ 0; nhấp vào âm thanh để chuyển sang đơn âm rồi chuyển về âm thanh nổi, `mono` thay đổi được đồng bộ hóa |
| サウンドセレクト | 49 bài hát đã được mở khóa được liệt kê và không có bài hát nào phát khi bạn vào lần đầu; ↓3 Sau khi Z phát FLYING THE SKY, Q phát bài hát trước đó サイレント・ヴォイス; ↓12 Sau khi cửa sổ cuộn đến mục đầu tiên 5; Esc Dừng bài hát, sau đó Esc để quay lại オプション và con trỏ ở vị trí 1 |
| カラオケモード | Có ít nhất 15 bài hát trong danh sách; chọn bài hát thứ 2 để bắt đầu, vào trận カラオケ, nhấn X sau khoảng 12 giây và con trỏ vẫn ở bài hát thứ 2 khi quay lại danh sách |
| Công tắc gốc | Chuyển `title_ui=original` sang lùi オプション là màn hình gốc, không có trang gốc; X lặp lại, sau đó chuyển về phiên bản mới |
| ロード | Lựa chọn phương tiện `context=title`; sau khi vào cột lưu trữ, cột 1 trống và cột 2 trống; nhấn Z ở cột trống để bị từ chối (chế độ vẫn là 0); cột 1 sẽ mở ra một cửa sổ xác nhận và có nội dung Đọc bản ghi lưu trữ. /Bạn có chắc không? ; Có → Vào menu chính giữa các ván, 7 vòng, vốn 14500 |

## 4. Chưa được xác minh và bị hạn chế

- Nhánh tải và sửa chữa file của コントローラパック chỉ có phân tích tĩnh: máy chủ không có Pak, đường dẫn Pak ổn định ở trạng thái 7.
- Không có kho lưu trữ đặc biệt nào để xác minh việc mở khóa của những người đã hoàn thành trò chơi (Vùng đất thượng của Trái đất xanh) và đã nhìn thấy máy bay cụ thể; trang này chỉ hiển thị danh sách được tạo bởi `801C81C0`.
- Tên bài hát chưa có sẵn tiếng Trung hoặc tiếng Anh, bạn phải đợi bảng nhập dữ liệu có thêm dòng chữ 0xE8–0x118.
- Ô tùy chọn của cửa sổ xác nhận ban đầu: `native-save-screens.md` được viết là (221,122)–(251,163), còn bảng bố cục là cửa sổ chính (53,101)–(267,139) rồi tiếp tục xuống (221,139)–(251,163). Trang gốc được vẽ theo trang cũ ở cả hai nơi và chưa được so sánh với ảnh chụp màn hình gốc.