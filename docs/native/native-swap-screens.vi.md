> **Ngôn ngữ / Language:** [Tiếng Việt](native-swap-screens.vi.md) · [English](native-swap-screens.en.md) · [中文](native-swap-screens.md)

# のりかえ Màn hình: Danh sách phi công, danh sách đơn vị, trang xác nhận và việc tiếp quản Fairy Transfer bản địa

Ngày: 23-09-2026. Mục 6 của menu tương tác (menu phụ パイロット／Fairy). Năm màn hình gốc (màn hình số 6, 16, 17, 20 và 21) được trang RmlUi tiếp quản và thành phần ban đầu được duy trì; bản thân việc chuyển giao được đưa vào cạnh A và bàn giao cho chức năng ban đầu để hoàn thành, còn việc chuyển giao danh sách, bộ phận và hành khách đồng hành không được trang viết lại. Bạn có thể chọn lại màn hình gốc trong "Màn hình giữa phiên" trên trang cài đặt, xem [Menu chính giữa phiên](native-intermission-menu.md).

## 1. Màn hình gốc (phân tích tĩnh)

Các tọa độ đều là 320 × 240. Việc tháo gỡ lấy các nhận xét hướng dẫn từ đầu ra biên dịch lại. Để xử lý のりかえ trong menu chính (cửa sổ bật lên và còi khi danh sách ứng viên trống), hãy xem [Menu chính liên trường](native-intermission-menu.md) §3.

### Danh sách driver (Màn hình 6) và Danh sách yêu tinh (Màn hình 20)

| Dự án | Cơ sở |
| --- | --- |
| Bố cục 0x6F／0x88: Bảng (21,21)–(299,219); Tag のりかえ（0xFD2）(144,24), 0x1002 Fairy／0xFEC (24.200), レベル (248.200) | Bảng bố trí |
| Khởi tạo `801D25A4`/`801D4164`: Nền (bao gồm số ngẫu nhiên), bố cục, `801CA75C` (`801C5618` Tạo bảng thí điểm ứng cử viên `D_801DD3A8`: Sinh vật, phi công có danh mục có nhiều hơn hai máy bay có sẵn, `801C58BC` sắp xếp; sau đó đếm số trang và sắp xếp theo `D_801DD538` Quyết định xem có quay lại trang cuối cùng hay không) hoặc `801CAC0C` (`801C60DC` tạo bảng cổ tích `D_801DD550`); **9 hàng mỗi trang**, bắt đầu từ trang `D_801DD14A` 1, hàng `D_801DEBC8`; `801C8ED8`/`801CAC84` Vẽ danh sách; `801CA524`/`801CAFE0` vẽ chi tiết và ghi các mục đã chọn vào `D_801DEC5C` | `801D25A4`, `801D4164` |
| Hàng y=48＋16n: tên phi công x=24, tên máy bay đang bay trên x=96 (độ lệch hình thái của nhóm ゲッター cộng với `801C8E50`; cơ thể vô cơ `--`), Lenox=248, cấp x=280 | `801C8ED8`, `801CAC84` |
| Dòng chi tiết y=200: Màn hình 6 là tên và cấp độ của yêu tinh (thành viên phi hành đoàn thứ hai `+4 & 0x40`) trên cơ thể người điều khiển con trỏ; Màn 20 là phi công chính của cơ thể nơi đặt yêu tinh | `801CA524`, `801CAFE0` |
| Mỗi khung `801D263C`/`801D41FC`: A → `D_801DEC58=0`, ảnh tiếp theo 16/21; B → 0; chín dòng lên xuống, lật trang sang trái và phải (`801CD5B4`), vẽ lại chi tiết | Tương tự như trên |

### Danh sách máy bay mục tiêu (Màn hình 16) và danh sách phi công mục tiêu (Màn hình 21)

| Dự án | Cơ sở |
| --- | --- |
| Bố cục 0x7C／0x89: Bảng (18,10)–(299,219); のりかえ (208,16), レベル (248,44), 0x1002／0xFEC (116,64), レベル (248,64) | Bảng bố trí |
| Khởi tạo `801D2758`/`801D42FC`: nền, bố cục, `801CA824` (`801C59AC` tạo bảng nội dung `D_801DCF02` mà phi công có thể cưỡi, số lượng `D_801DD0A4`) hoặc `801CB1A8` (`801C5C00` Tạo danh sách phi công có thể cưỡi cùng các nàng tiên), **7 dòng mỗi trang**, bắt đầu từ trang `D_801DD544` 1, hàng `D_801DEC58`; hình đại diện `801C6350` (16,8); họ và tên (0x1287) (116,44), cấp độ (280,44); dòng thứ hai tên người điều khiển chính/điều khiển chính (152,64) với cấp độ hoặc `--------`/`--`; số trang `%2d/%2d` (112,16); con trỏ sprite 0x14 (18,105) 281×16 | `801D2758`, `801D42FC` |
| Hàng y=106+16n: Màn hình 16 tên máy x=24, tên phi công x=152, HP (0xFE7) x=232, hiển thị HP x=256; màn hình 21 tên phi công x=24, tên máy x=152, Ryuru x=248, cấp x=280 | `801CA8AC`, `801CB230` |
| Mỗi khung hình `801D2A24`: A → `D_801DD0A2=0`, màn hình tiếp theo 17; B → 6; sau khi di chuyển ghi số khe nội dung của dòng con trỏ vào `D_801DD3A0`. Mỗi khung `801D4578`: Chế độ 0 A → Xây dựng cửa sổ bật lên (bố cục 0x8A: 0x1012 (56,104), よろしいですか (56,122), はい／いいえ (224,128)/(224,148), con trỏ 0x15), chế độ 1; ở chế độ 1, B đóng cửa sổ bật lên, A và con trỏ là 0 → Bảng Goblin: Goblin `+0x38` trỏ vào phần thân mục tiêu, phần thân mục tiêu `+0x3C`=goblin, `+0x34`=2, phần thân ban đầu `+0x34`=1, `+0x3C`=0, quay lại màn hình 20; B → 20 ở chế độ 0 | `801D2A24`, `801D4578` |

### Trang xác nhận (Màn hình 17)

| Dự án | Cơ sở |
| --- | --- |
| Bố cục 0x7D: Bảng (18,10)–(302,219); レベル (114,18), HP (114,42), 0x1012 (182,138), よろしいですか (182,154), はい(224,176), いいえ (224,196), 0x1002 (24.106), 0x1013 (24.128), 0x1014 (20.144), giới hạn (24.168), tránh (0x100D) (24.185), đánh (0xFF4) (24.202), địa hình (0xFF6) (268.138), trên không, đất liền và biển (264.154…202) | Bảng bố trí |
| Khởi tạo `801D2B64`: avatar (16,8), bản đồ chiến đấu cơ thể mục tiêu `801C6410` (176,8); tên phi công (32,88), cấp bậc (158,18); tên tiên (64.106); `D_801DECBC` = khả năng di chuyển của cơ thể hiện tại (thời gian sinh vật) `800A5254` + `801C4DE4` tính toán lại, nếu không thì 0); cơ thể mục tiêu sau khi tính toán lại: HP (134,42), tên cơ thể (184.120), giới hạn (64.168); tránh = `+0x26`, đánh = `+0x28`: `值+目标運動性` (64,y) Màu đỏ khi vượt quá giới hạn mục tiêu, `值+当前運動性` (128,y); địa hình: `800A6194(1, 驾驶员 rank, 机体 rank)` = tổng của cả hai: 0 cho `-`, 1–3 D, 4–5 C, 6–7 B, 8 trên A (288.154…); Con trỏ 0x14 (220,173) 30×20 | `801D2B64` |
| Mỗi khung `801D3A90`: A và con trỏ 0 (はい) → chuyển: tài xế trao đổi với tài xế gốc của thân mục tiêu (bao gồm hành khách đồng hành và bit trạng thái `+0x34`), các bộ phận được vận chuyển theo `801D33F4`, `801D35A4`/`801D3838` Tính toán lại, `800ABF70`, màn hình tiếp theo 6; A và con trỏ 1 hoặc B → màn hình 16 | `801D3A90` |

## 2. Phương thức tiếp quản

Mã nguồn: [`swap_page.cpp`](../../src/host/swap_page.cpp) (bộ chuyển đổi luồng trò chơi), [`frontend.cpp`](../../src/native/ui/frontend.cpp)'s `swap_sync` (trang), [`game_hooks.cpp`](../../src/host/game_hooks.cpp) bao bì (`swap_build`/`swap_step`/`swap_frame`, mười móc trong `generate_cpu.py` của `NATIVE_HOOKS`). Khi phiên bản gốc được chọn trong "Màn hình liên trường" của trang cài đặt, tất cả năm lối vào công trình sẽ được đưa về màn hình gốc; `SRW64_NATIVE_SWAP=0` hoặc khi hồ sơ không được tải, màn hình gốc được giữ lại trong suốt quá trình chạy.

| chức năng ban đầu | giấy gói |
| --- | --- |
| `801D25A4`／`801D4164` Khởi tạo danh sách | Không điều chỉnh chức năng ban đầu. Duy trì các cuộc gọi nền (với số ngẫu nhiên) và tạo bảng ứng cử viên, bản sao hàng, ghi `D_801DEC5C` |
| `801D263C`/`801D41FC` Danh sách trên mỗi khung hình | Di chuyển/bộ điều hợp trang do chính nó viết (9 dòng trên mỗi trang); xác nhận/trả lại A/B được đưa vào |
| `801D2758`/`801D42FC` Khởi tạo danh sách mục tiêu | Không điều chỉnh chức năng ban đầu. Giữ nền và tạo bảng mục tiêu; `D_801DD3A0` nhấn con trỏ trước để viết |
| `801D2A24` Mỗi khung của danh sách nội dung | Di chuyển/lật trang, viết trang, dòng và `D_801DD3A0`; xác nhận/quay lại tiêm A/B |
| `801D4578` Mục tiêu thần tiên trong mọi khung hình | Chế độ danh sách: tự di chuyển và viết; xác nhận chuyển từ bộ điều hợp sang chế độ bật lên (nhánh A ban đầu chỉ xây dựng các hình ảnh và văn bản bật lên); quay lại tiêm B. Chế độ bật lên: はい Tiêm A (phiên bản gốc hoàn thành máy tính và quay lại màn hình 20); いいえ/Hủy cửa sổ đóng bằng adapter |
| `801D2B64` Xác nhận khởi tạo | Không điều chỉnh chức năng ban đầu. Giữ nền; `D_801DECBC` được viết là khả năng di chuyển ban đầu của cơ thể hiện tại |
| `801D3A90` Xác nhận từng khung hình | Di chuyển con trỏ và tự viết; xác nhận/quay lại để tiêm A/B (phiên bản gốc thực hiện chuyển khi はい) |

**Ảnh chụp nhanh**: `status.swap_page`: `screen` (`pilots`/`fairies`/`targets`/`fairy_targets`/`confirm`), `serial`, `labels`; danh sách là `page`, `pages`, `cursor`, `rows[]` (`index`, `number`, __I NL_CODE_117__, `full_name`, `level`, `unit`, `art`), `sub{name,level}`; danh sách mục tiêu bổ sung `pilot{…,unit}`, OK (khung máy bay: `slot`, `name`, `pilot`, `hp`; phi công: cùng hàng danh sách), mục tiêu yêu tinh là `mode`, `window_cursor`; trang xác nhận là `pilot`, `from{name,pilot,sub,art}`, `to{slot,name,hp,limit,mobility,sub,art}`, `evade`/`hit{value,after,now,over}`, `terrain`, `cursor`. Nhật ký sự kiện `swap-page-events.jsonl`.

**Gỡ lỗi**: ID ổn định `swap:N` (dòng danh sách), `swap-yes`/`swap-no`; bàn phím ↑↓, ←→ (lật trang), Enter/Z, Esc/X; điều kiện chờ `swap_page`.

## 3. Xác minh máy thật (2026-09-23)

```sh
.venv/bin/python tools/recomp/debug/check_swap.py            # 构建、跑测试关卡并检查
.venv/bin/python tools/recomp/debug/check_swap.py --reuse-build
```

Không có đối tượng có thể chuyển nhượng trong kho lưu trữ của tập đầu tiên (menu chính sẽ phát ra tiếng bíp trực tiếp). Điều kiện ứng viên (`801C5618`): danh mục trình điều khiển (bản ghi ROM thí điểm `+0xB`, thời gian chạy `+0x32`) khác 0 và cùng danh mục trong danh sách (bản ghi ROM máy bay `+0x12`, thời gian chạy `+0x1A`), `+0x0C & 0x80` Có nhiều hơn hai đơn vị của máy (loại 1 cũng có thể được sử dụng làm danh mục 7, loại 3 cũng có thể được sử dụng làm loại 4). Máy ban đầu (loại 0) chưa bao giờ là ứng cử viên nên cấp độ kiểm tra `config/recomp/mini-stages/swap-test.json` đã được đăng ký với `3D5A 95,0,117,500`, `3D5A 91,0,115,500` ở đầu `flow.json` (không chiến đấu, `3D4A` đã kết thúc)ヒイロ／ウイングガンダム và 五飞／ガンダムシュピーゲル (cả hai loại 3), sau khi hoàn thành cấp độ và vào màn hình tương tác sẽ có ứng viên cho のりかえ. **Đăng ký máy bay không người lái với `3D5A 999,0,机体,500` để trải nghiệm danh sách tiêu diệt**: `800ABF70` → `800ABF08` đọc lỗi con trỏ xấu trong vòng chiến thuật.

Đang chạy `build/recomp/debug/20260923T042217.100733Z/`: `swap-checks.json` đã vượt qua 12 mục, mã thoát 0.

| Kiểm tra | Kết quả |
| --- | --- |
| Danh sách ứng viên | ヒイロ／ウイングガンダム、五飞／アルトロンガンダム； ↓ Di chuyển |
| Danh sách đơn vị | Máy bay duy nhất mà Hako có thể lên máy bay là Aアルトロンガンダム (Wu Fei đã có trong danh sách; Atolu không có trong danh sách - quy tắc của `801C59AC` ban đầu, trang sao chép kết quả) |
| Trang xác nhận | ヒイロ → アルトロンガンダム: Giới hạn 330, tránh 120+115 (220), đánh 113+115 (213), địa hình CABA; ↓ đến いいえ, danh sách đơn vị trả về Z |
| はい | Phiên bản gốc thực hiện chuyển giao: ヒイロ trong danh sách ứng cử viên trở thành アルトロンガンダム, Wufei trở thành ウイングガンダム; và sau đó thay đổi trở lại |
| Trở về |

So sánh phiên bản gốc (`build/recomp/debug/20260923T041326.824813Z/swapo-confirm.png`, đặt quy trình tương tự sau khi cắt phiên bản gốc): Xác nhận rằng địa hình của trang là Trống C Đất A Biển B Yu A——`800A6194` là tổng của hai cấp bậc. Phiên bản đầu tiên của trang được tính là `-ABA` theo cấp độ thấp hơn, đã được sửa; tên của máy bay nằm bên dưới bản đồ chiến đấu (184.120), hai dòng giải thích "khả năng をうける hạn chế/( )内は本のkhả năng" ở bên trái và trang thứ hai của trang được định dạng tương ứng.

## 4. Chưa được xác minh

- Goblin list và goblin boarding (Màn hình 20/21): Không có file save với goblin, chỉ có phân tích tĩnh.
- Lật trang của danh sách nhiều trang.