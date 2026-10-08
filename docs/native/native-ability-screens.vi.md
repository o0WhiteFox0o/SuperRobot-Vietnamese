> **Ngôn ngữ / Language:** [Tiếng Việt](native-ability-screens.vi.md) · [English](native-ability-screens.en.md) · [中文](native-ability-screens.md)

# Màn hình xem khả năng: Tiếp quản bản chất khả năng ユニット/khả năng パイロット

Ngày: 23-09-2026. Mục 4 và 5 của menu giữa phiên. Năm màn hình chỉ đọc (màn hình số 4, 13, 14, 5 và 15) được trang RmlUi tiếp quản, duy trì thành phần ban đầu; chuyển đổi giữa các màn hình được đưa vào cạnh phím và chuyển sang chức năng ban đầu mà không thay đổi bất kỳ dữ liệu trò chơi nào. Bạn có thể chọn lại màn hình gốc trong "Màn hình giữa phiên" trên trang cài đặt, xem [Menu chính giữa phiên](native-intermission-menu.md).

## 1. Màn hình gốc (phân tích tĩnh)

Các tọa độ đều là 320 × 240. Việc tháo gỡ lấy các nhận xét hướng dẫn từ đầu ra biên dịch lại.

### Danh sách đơn vị (Màn hình 4) và danh sách phi công (Màn hình 5)

| Dự án | Cơ sở |
| --- | --- |
| Bố cục 0x6D/0x6E: một bảng (21,21)–(299,219); tag ユニットabilities/パイロットabilities (144,24), 0x1002 (Fairy) (24.200), レベル (248.200) | Bảng bố trí |
| Khởi tạo `801D14BC`/`801D22E0`: nền (bao gồm số ngẫu nhiên), bố cục, `801C87DC` (`801C4FB0(0)` tạo danh sách tất cả máy bay `D_801DD210`) hoặc `801C8DD8` (`801C549C(0)` tạo danh sách tất cả phi công `D_801DD3A8`, phần tử là chỉ số đăng ký bảng trình điều khiển), **9 hàng trên mỗi trang**, bắt đầu từ trang `D_801DD14A` 1, hàng `D_801DEBC8` (bản sao `D_801DD53A`); `801C8854`/`801C8ED8` danh sách bản vẽ; `801C8BAC`/`801CA524` Vẽ chi tiết và ghi các mục đã chọn vào `D_801DEC5C` (số khe thân hoặc chỉ số đăng ký trình điều khiển); trình hướng dẫn con trỏ 0x14 (21,48) 278×16 | `801D14BC`, `801D22E0` |
| Hàng khung máy bay y=48+16n: tên khung máy bay x=24, tên phi công x=152 (không người lái `--------`), HP (0xFE7) x=232, hiển thị HP (`800A5254`+`801C4DE4`) x=256 | `801C8854` |
| Hàng phi công: tên phi công x=24, tên máy bay x=96 (tên cộng `801C8E50` mang lại hình dạng bù trừ của nhóm ゲッター; cơ thể vô cơ `--`), レベル x=248, cấp x=280 | `801C8ED8` |
| Dòng chi tiết y=200: Khi thân con trỏ (thân phi công) có ≥2 thành viên phi hành đoàn và thành viên phi hành đoàn thứ hai `+4 & 0x40`, vẽ tên thành viên phi hành đoàn thứ hai (thân yêu tinh) x=64 và cấp x=280, nếu không thì `--------`/`--` | `801C8BAC`, `801CA524` |
| Mỗi khung: A → ảnh tiếp theo 15/13; B → 0; Vòng lặp lên xuống 9 dòng, lật trang trái phải (`801CD2D4`/`801CD5B4`), vẽ lại chi tiết | `801D1554`, `801D2378` |

Bảng trình điều khiển: 100 mục nhập × 0x4C byte, bắt đầu từ `0x80172F40`. Các trường: số `+0x02`, cờ `+0x04` (khả năng được hiển thị dưới dạng `---` khi đặt 0xC0), cấp độ `+0x05`, cấp độ kỹ năng `+0x06/+0x07/+0x08`, `+0x0A` mã số linh hồn, `+0x0B…` id linh hồn, `+0x12` kinh nghiệm, `+0x16/+0x18` SP hiện tại giá trị/giới hạn trên, `+0x20` sức mạnh, lưới `+0x22`, `+0x24` bắn, `+0x26` tránh, `+0x28` trúng đích, `+0x2A` Phản ứng, `+0x2C` kỹ năng, `+0x2E…+0x31` thích ứng với địa hình, `+0x36` dấu kỹ năng, `+0x37` sinh vật, `+0x38` con trỏ nội dung.

### Khả năng cơ thể (Màn hình 13)

| Dự án | Cơ sở |
| --- | --- |
| Bố cục 0x79: Panel (21,10)–(302,219), nội thất được chia theo ảnh chụp màn hình gốc: tên thân (21,10)–(175,35); サイズ (0x1003)/chi phí sửa chữa (0x1004) (21,36)–(175,58); bộ phận gia cố (21,59)–(175,131); HP/EN (21.132)–(155.163); Khả năng đặc biệt (0x1005) (21,164)–(155,219); タイプ (0x1006)/Tính cơ động (0x1007)/Tính cơ động/Giáp/Giới hạn (156,132)–(259,219); Địa hình (0xFF6) Trên không, Đất liền và Biển (0xFF7–0xFFA) (260.132)–(299.219); Bản đồ chiến đấu (176,8)–(302,132) | Bảng bố trí, ảnh chụp màn hình |
| Kích thước: `801D1680` Theo nội dung `+0x0C` bit 1/2/4/8/0x10 là 0–4, văn bản 0x446+n (SS…LL); chi phí sửa chữa `+0x1C` | `801D16D8` |
| Phần: `+0x21` số vị trí, `+0x23…` số phần, tên 0x469+n | Tương tự như trên |
| HP／EN: Hiển thị HP `D_801DEB08` được vẽ hai lần (giá trị hiện tại/giới hạn trên, bằng nhau giữa các trường), EN `+0x0A`; hai hình con trỏ cao 2 pixel 0x14/0x15 có thang màu xanh lục | Tương tự như trên |
| Loại chuyển động: `+0x0D` Bit 0–3 và 0x10 tương ứng với văn bản biểu tượng `D_801DC8F0[0…4]`, được xếp từ phải sang trái (258.138) | Tương tự như trên |
| シールド：`+0x20 & 2` → văn bản 0x38F (có) nếu không thì 0x390 (không), rút ​​ra tại (104,168) | Tương tự như trên |
| Khả năng đặc biệt: Bảng so sánh cờ 32 bit của `+0x28``D_801DC8FC` (16 mục × 8 byte: mặt nạ u32, văn bản u16, chiều rộng u8), gói từ (25.188) (trang gốc cũng gói theo chiều ngang; có thể hiển thị tối đa 3, chẳng hạn như trang của ビルバインChangsha/Clone/オーラバリア, toàn bộ cột bị giảm khi có nhiều hơn hai dòng, 2026-09-29) | Tương tự như trên |
| Cột bên phải: Tính cơ động `D_801DD14C`, Tính cơ động `D_801DD14E`, Giáp `D_801DEB06`, Giới hạn `D_801DEB04`; Địa hình `+0x16…+0x19` nhận được các chữ cái thông qua `800A6104(1,rank)` (4=A, 3=B, 2=C, 1=D, tương tự đối với vũ khí), điều chỉnh trên không trong `D_801DDA06` Khi không phải 0, nhấn 4 để hiển thị | Tương tự như trên |
| Mỗi khung hình `801D2030`: L/R (`D_80178A08 & 0x2030`) → `801CCDA0(&行, 8)` Di chuyển tiến và lùi trong danh sách, `D_801DEC5C` thay đổi sang nội dung mới, vào lại màn hình 13; A → màn hình 14 (`D_801DEC58=0`); B → màn 4 | `801D2030` |

### Danh sách vũ khí (Màn hình 14)

Bố cục 0x7A, bảng (21,21)–(299,219), tiêu đề 0xFF1–0xFF4 (tên vũ khí/sức tấn công/tầm bắn/đòn đánh) y=24, nhãn hàng chi tiết 0xFF5–0xFFA y=160, 0xFFB/0xFFD y=184, 0xFFC/0xFFE y=201. Khởi tạo `801D2144`: `801C7254` Tạo danh sách vũ khí (giống như sửa đổi vũ khí: `D_801DEC68`, số lượng `D_801DECBE`, 6 hàng mỗi trang, trang `D_801DD20C`, hàng `D_801DEC58`), `801C75C0`/`801C7A9C` Bản vẽ danh sách và chi tiết (số lượng tên lửa, địa hình bốn chữ cái, công suất yêu cầu (màu đỏ nếu nguồn không đủ), mức tiêu thụ EN (màu đỏ nếu EN không đủ), các kỹ năng cần thiết, chỉnh sửa クリティカル). Mỗi khung `801D21F8`: chỉ B → ảnh 13; lên xuống, lật trang (`801CD0CC`).

### Khả năng của người lái xe (Màn hình 15)

| Dự án | Cơ sở |
| --- | --- |
| Bố cục 0x7B: Bảng điều khiển (18,10)–(299,219), được chia theo ảnh chụp màn hình gốc: avatar (18,10)–(110,101) (`801C6350`); nhắc LRZ: 二のパイロット (0x1008) (111,10)–(299,35); khối tên (111,36)–(299,101): tên đầy đủ (0x1287+số) (120,40), giá trị 気力 (0x1009) (128,64) (160,64), giá trị レベル (192,64) Khối khả năng (18,102)–(299,137): lưới (0x100C) (24.106) giá trị (64.106), tránh (0x100D) (112.106) `值+ 運動性` (152.106), giá trị phản ứng (0x100E) (232.106) (272.106), bắn (0x1023) (24.122), đánh (0xFF4) (112.122), kỹ năng (0x100F) (232.122); sức khỏe tâm thần (0x1010) (24.144) sáu vị trí lưới `D_801DC6B0`: (136.144) (192.144) (24.162) (80.162) (136.162) (192.162), thiếu `---`; kỹ năng đặc biệt (0x1011) (24.184) vị trí `D_801DC6BC`: (96.184) (96.202) (168.202); địa hình (0xFF6) (254.150), trên không, trên bộ và trên biển (240.176) (272.176) (240.200) (272.200) | Bảng bố cục, `801C936C`, ảnh chụp màn hình |
| TIẾP THEO: Cấp 99 hiển thị `---`, nếu không thì giá trị trả về là `8008407C(+0x12)` | `801C936C` |
| Né tránh/đánh: `值+ 運動性`, giá trị + tính cơ động. Màu đỏ khi vượt quá giới hạn của máy bay (máy bay được tính toán lại với `800A5254` + `801C4DE4`; phi công của nhóm ゲッター tìm thấy máy bay dùng chung với `801C924C`) | Tương tự như trên |
| Kỹ năng: `+0x36` bit 0x04/0x08/0x10/0x20/0x40 chọn một theo thứ tự → văn bản 0x433/0x40F/0x418/0x421/0x42A + `+0x06`; bit 0x01 và `+0x07` → 0x43C+`+0x07`; bit 0x02 và `+0x08` → 0x406+`+0x08`; số 4 và `800A4BB8()` không phải 0 → văn bản 0xF1 | Tương tự như trên |
| Mỗi khung `801D24C8`: L／R → `801CCDA0(&行, 8)` Di chuyển tới lui và nhập lại màn hình 15 (`D_801DEC5C` được đổi thành chỉ số đăng ký trình điều khiển mới); B → Màn hình 5 | `801D24C8` |

## 2. Phương thức tiếp quản

Mã nguồn: [`ability_page.cpp`](../../src/host/ability_page.cpp) (bộ chuyển đổi luồng trò chơi), [`frontend.cpp`](../../src/native/ui/frontend.cpp)'s `ability_sync` (trang), bao bì của [`game_hooks.cpp`](../../src/host/game_hooks.cpp) (`ability_build`/`ability_step`/`ability_frame`, mười móc trong `generate_cpu.py` của `NATIVE_HOOKS`). Tái sử dụng nhãn hàng vũ khí và cột vũ khí `upgrade_page::weapon_row_json`/`weapon_labels_json`. Khi phiên bản gốc được chọn trong "Màn hình liên trường" của trang cài đặt, tất cả năm lối vào công trình sẽ được đưa về màn hình gốc; `SRW64_NATIVE_ABILITY=0` hoặc khi hồ sơ không được tải, màn hình gốc được giữ lại trong suốt quá trình chạy.

| chức năng ban đầu | giấy gói |
| --- | --- |
| `801D14BC`／`801D22E0` Khởi tạo danh sách | Không điều chỉnh chức năng ban đầu. Giữ các cuộc gọi nền (bao gồm các số ngẫu nhiên) và tạo danh sách, sao chép hàng, viết `D_801DEC5C`; không xây dựng bố cục, văn bản, hình con trỏ |
| `801D1554`/`801D2378` danh sách trên mỗi khung hình | Di chuyển/Trang: Bộ điều hợp ghi trang, hàng, sao chép bằng `D_801DEC5C` (9 hàng trên mỗi trang); xác nhận/trả lại tiêm A/B |
| `801D16D8`／`801D2480` Khởi tạo trang khả năng | Không điều chỉnh chức năng ban đầu. Giữ cuộc gọi nền; trang lấy các trường trực tiếp từ bản ghi |
| `801D2030`/`801D24C8` Trang khả năng trên mỗi khung hình | L/R chèn máy trước/tiếp theo (phiên bản gốc di chuyển con trỏ danh sách và vào lại màn hình, và trang được xây dựng lại); A (trang nội dung)/B tiêm |
| `801D2144` Khởi tạo danh sách vũ khí | Không điều chỉnh chức năng ban đầu. Giữ nền, `801C7254`; trang viết 1 |
| `801D21F8` Danh sách vũ khí mọi khung hình | Tự viết bộ điều hợp chuyển trang/di động; tiêm trở lại B |

**Ảnh chụp nhanh**: `status.ability_page`: `screen` (`units`/`pilots`/`unit`／`weapons`／`pilot`), `serial`, `labels`, `weapon_labels`; danh sách là `page`, `pages`, `cursor`, `rows[]` (nội dung: `slot`, `number`, `name`, `pilot`, __I NL_CODE_159__, `art`; Phi công: `index`, `number`, `name`, `unit`, `level`), `sub{name,level}`; Trang máy bay có `unit`, `size`, `repair`, `parts[]`, `hp`/`hp_max`, `en`/`en_max`, `types[]`,__ INL_CODE_176__, `abilities[]`, `move`, `mobility`, `armor`, `limit`, `terrain`, `index`, `count`; danh sách vũ khí là `unit{…,en,morale}`, `page`, `pages`, `cursor`, `rows[]` (giống như sửa đổi vũ khí); Trang trình điều khiển có `pilot{index,number,name,full_name,level,hidden,art}`, `unit`, `morale`, `next`, `sp`/`sp_max`, `stats{melee,ranged,hit,evade,skill,reaction}`, `over{hit,evade}`, `mobility`, `spirits[]`, `skills[]`, `terrain`, `index`, `count`. Nhật ký sự kiện `ability-page-events.jsonl`.

**Gỡ lỗi**: ID ổn định `ability:N` (dòng danh sách; nhấp vào dòng con trỏ để nhập, nhấp vào dòng con trỏ để quay lại danh sách vũ khí); bàn phím ↑↓, ←→ (lật trang), Enter/Z, Esc/X, trang khả năng Q/E (hoặc ←→) để chuyển qua lại; điều kiện chờ `ability_page`.

## 3. Xác minh máy thật (2026-09-23)

```sh
.venv/bin/python tools/recomp/debug/check_ability.py            # 构建并检查
.venv/bin/python tools/recomp/debug/check_ability.py --reuse-build
```

`intermission-cold-1` Tập đầu tiên đã được xóa và lưu. Đang chạy `build/recomp/debug/20260923T033850.329381Z/`: `ability-checks.json` đã vượt qua 18 mục, mã thoát 0.

| Kiểm tra | Kết quả |
| --- | --- |
| Danh sách cơ thể | Sáu dòng (ダイターン3／ダイファイター／ダイタンク／スイームルグ／ドール／ドール(bay), `801C4FB0` Liệt kê từng mẫu), HP 8000, driver vạn chân; ↑↓ Chuyển động |
| Trang đơn vị | Sussex LL, chi phí sửa chữa 14000, HP 8000/EN 200, khả năng cơ động 5, khả năng di chuyển 70, áo giáp 1800, giới hạn 270, địa hình AABA, シールド有, khả năng đặc biệt 変, タイプ trên bộ và trên không |
| Chuyển đổi qua lại | E → ダイファイター (đã thêm nối tiếp, phiên bản gốc vào lại màn hình), Q → ダイターン3 |
| Danh sách vũ khí | Sáu dòng, 2 trang, dòng đầu tiên Bắn ダイターンミサイル 900; → chuyển sang trang 2, ← quay lại; ↓ di chuyển; X quay lại trang nội dung |
| Trở về | X trở về danh sách (con trỏ 0), |
| Danh sách thí điểm | Manzhang／シモーヌ／Marioミ／ローレンス Tên từng đơn vị và cấp độ |
| Trang trình điều khiển | Vượt núi: 気力 100, レベル 5, TIẾP THEO 444, SP 83/83, lưới 150, bắn 126, né tránh 108+70, đánh 108+70, phản ứng 92, kỹ năng 124, tinh thần Phải đánh/ドgốc thiên nhiên/気合/ひらめき/nóng máu+?????, kỹ năng cơ bản L4/cắt り払いL4/S phòng thủ L4, địa hình AAAA - phù hợp với ảnh chụp màn hình gốc từng mục |
| Chuyển tiếp và quay lại và quay lại | E → trình điều khiển thứ hai; X quay lại danh sách (con trỏ 1); |

Đã sửa các lỗi phân tích tĩnh trong quá trình: `+0x20` của trình điều khiển là sức mạnh chứ không phải số lần tiêu diệt; `+0x26` là né tránh, `+0x28` bị trúng đòn (văn bản tránh 0x100D, trúng 0xFF4, phản ứng 0x100E, kỹ năng 0x100F); cấp địa hình là 0–4 (4=A), vũ khí cũng vậy (trang sửa đổi ban đầu được hiển thị là 5=A và lần này sẽ được sửa); khóa tài nguyên hình đại diện là `battle_assets.portraits`.

## 4. Chưa được xác minh

- Lật trang danh sách nhiều trang (hơn 10 đơn vị/phi công, hơn 7 loại vũ khí).
- Phi công ẩn (`+4 & 0xC0`) có khả năng được hiển thị là `---`, tên bù trừ của đơn vị được chia sẻ bởi nhóm ゲッター và dòng chữ màu đỏ trong hàng vũ khí khi nguồn/EN không đủ: kho lưu trữ tập đầu tiên không có những tình huống này.
- Giá trị hiện tại và giới hạn trên của HP trên trang máy bay: hai giá trị này bằng nhau giữa các trường. Trang này sẽ hiển thị HP hai lần, giống như phiên bản gốc.