> **Ngôn ngữ / Language:** [Tiếng Việt](native-parts-screens.vi.md) · [English](native-parts-screens.en.md) · [中文](native-parts-screens.md)

# Tăng cường màn hình パーツ: danh sách đơn vị, vị trí và kho đồ, quyền tiếp quản bản địa của chủ sở hữu

Ngày: 23-09-2026. Mục 7 của Menu Intersession. Ba màn hình gốc (màn hình số 7, 18 và 19) được trang RmlUi tiếp quản và thành phần ban đầu được duy trì; thiết bị, tháo dỡ, lấy các bộ phận từ máy bay khác đều được đưa vào cạnh A và bàn giao cho chức năng ban đầu để hoàn thiện. Hồ sơ máy bay và hồ sơ kiểm kê không được trang viết lại trực tiếp. Bạn có thể chọn lại màn hình gốc trong "Màn hình giữa phiên" trên trang cài đặt, xem [Menu chính giữa phiên](native-intermission-menu.md).

## 1. Màn hình gốc (phân tích tĩnh)

Các tọa độ đều là 320 × 240. Quá trình tháo gỡ lấy nhận xét hướng dẫn (`build/recomp/cpu-bound/generated/`) từ đầu ra biên dịch lại.

### Danh sách đơn vị (Màn hình 7)

| Dự án | Cơ sở |
| --- | --- |
| Bố cục 0x70: một bảng (21,21)–(299,219); thẻ cố định được tăng cường パーツ (120,24), thiết bị trong のパーツ (24,184) | Bảng bố cục thường trú `D_800C8BB8` (mỗi mục là 24 byte, từ thứ hai trỏ đến danh sách {text number, x, y}, cuối 0xFFFF) |
| Khởi tạo `801D4A00`: `80085B94(0,1)` làm tối nền (bao gồm các cuộc gọi số ngẫu nhiên), xây dựng bố cục, `801CB540` (`801C5D3C` tạo danh sách và bong bóng sắp xếp danh sách đó theo thứ tự giảm dần theo cấp độ trình điều khiển `+0x5`, sau đó đếm số trang), `801CB5A0` vẽ danh sách, `801CB910` Vẽ chi tiết và viết nội dung đã chọn vào `D_801DEC5C`, khe hình con trỏ 0x14 (21,48) 278×16, mờ dần | `801D4A00` |
| Danh sách mảng `D_801DD210` (số khe nội dung u16, số lượng `D_801DD0A0`), **8 dòng trên mỗi trang**, số trang `D_801DD14A` bắt đầu từ 1, dòng `D_801DEBC8` (sao chép `D_801DD53A`); số trang `D_801DDA04`, số dòng trang cuối `D_801DDA2E` | `801CB540`, `801CB5A0` |
| Mỗi dòng y=48+16n: tên cơ thể (0x20F+số cơ thể) x=24, tên phi công (0x111E+số tài xế) x=152 hoặc `--------`, RIL (0xFE1) x=248, cấp độ `%2d` x=280; số trang `%2d/%2d` (24,24) | `801CB5A0` |
| Chi tiết: Chọn tên thành phần (0x469+số bộ phận) hoặc `--------` của từng khe của thân máy và bảng vị trí `D_801DC6C4`: (112,184) (209,184) (112,202) (209,202) | `801CB910` |
| Mỗi khung hình `801D4A98`: A → hiệu ứng âm thanh 0xB7, `D_801DEC58=0`, hình tiếp theo 18, chuyển tiếp; B → 0xB8, hình tiếp theo 0. Các phím điều hướng là `801C4A20` (lên và xuống, 8 dòng trên một trang hoặc số dòng trên trang cuối cùng), `801CDA88` (xoay trang sang trái và phải, hạ con trỏ khi số dòng trên trang cuối không đủ), `801CDC24` (vẽ lại chi tiết); viết số 0 khi không có chìa khóa | `801D4A98` |

### Slots và Inventory (Màn hình 18)

| Dự án | Cơ sở |
| --- | --- |
| Bố cục 0x7E: Bảng điều khiển (21,21)–(299,219), được chia nội bộ thành phía trên bên trái (số trang + lựa chọn nâng cao), giữa bên trái (danh sách vị trí), phía dưới bên trái (sáu khả năng), phía trên bên phải (tên nội dung), giữa bên phải (danh sách khoảng không quảng cáo), phía dưới bên phải (mô tả phần); thẻ cố định 0xFF0 (40,24), 0x1016 (72,24), HP/EN/Mobility/Mobility/Armor/Limit (0xFE7, 0xFE8, 0x1024, 0xFE9, 0xFEA, 0xFEB) x=24 y=120+16n, mỗi hàng ► (0x101E) x=104 | Bảng bố trí |
| Khởi tạo `801D4BEC`: nền, bố cục, trang khoảng không quảng cáo `D_801DD63C=1`, `801CBA78` Tạo danh sách khoảng không quảng cáo, `D_801DECCA=0`, chế độ `D_801DECD8=0`, `801CBFAC` vẽ toàn bộ màn hình, hình con trỏ vị trí 0x14 (21,45) 144×17, mờ dần, `D_801DEC50=0` | `801D4BEC` |
| Danh sách tồn kho `D_801DD3A8` (u16): Mục đầu tiên 0x12 nghĩa là はずす, theo sau là mã bộ phận (0...17) của mỗi ** số giữ > 0**; 6 hàng trên mỗi trang, số trang `D_801DECF0`, số hàng trang cuối cùng `D_801DD542`, hàng `D_801DD0A2` | `801CBA78`, `801CBB18` |
| Hiển thị kho: số trang (24,24); trang 1, dòng 0 はずす (0x1017) (168,64); các dòng còn lại y=64+16n: tên bộ phận x=176, số lượng thiết bị `%d` x=268, số lượng sở hữu `(%d)` x=276; mũi tên chuyển trang 0x1041 (168,48)／0x1042 (288,48) | `801CBB18` |
| Bản ghi hàng tồn kho `D_8015E990`: một u16 cho mỗi bộ phận, số giữ byte cao, số thiết bị byte thấp | `801CBB18`, `801D4C94` |
| Nội dung: `+0x21` Số lượng vị trí, `+0x22` Số lượng trang bị, `+0x23…+0x26` Mã bộ phận của mỗi vị trí (s8, −1 trống) | `801CBFAC`, `801D4C94` |
| Cột khả năng: `800A5254(机体,2)` Sau khi tính toán lại, `801C4DE4` sẽ chứa các giá trị hiển thị của các thành phần (HP `D_801DEB08`, khả năng cơ động `D_801DD14C`, khả năng di chuyển `D_801DD14E`, áo giáp `D_801DEB06`, giới hạn `D_801DEB04`, đọc trực tiếp EN `+0x08`). **Cột bên trái "bây giờ" = giá trị hiển thị trừ đi phần thưởng của phần trên khe con trỏ**, cột bên phải "Xem trước" thêm phần thưởng của phần dưới con trỏ trong kho ở chế độ 1 (はずす không thêm); bản xem trước có màu xanh lá cây phía trên giá trị hiện tại và màu đỏ bên dưới giá trị hiện tại | `801CBFAC` |
| Bảng phần thưởng `D_801DC578`: 7 u16 mỗi mảnh - HP, Cơ động, Di chuyển, Giáp, Giới hạn, Hai Cờ. 18 miếng; Số 7 là linh kiện có cường độ +5 (`801D4BB4` thay đổi driver `+0x20` khi xếp dỡ), số 9 và 10 chỉ có logo | Dữ liệu ROM |
| Bảng mô tả `D_801DC97C`: Mỗi mục {text base address, line number}, text number 0x10AF＋base address＋n, rút ​​ra tại (168,168+16n) | `801D4C94` |
| Trên mỗi khung hình `801D4C94`: Chế độ 0: B → màn hình tiếp theo 7; A → xây dựng sprite con trỏ kiểm kê 0x15 (166,64) 132×16, hàng 0, chế độ 1. Chế độ 1: B → Giải phóng văn bản sprite và mô tả, chế độ 0; A → Trang 1, dòng 0 (はずす): Nếu slot trống thì chỉ cần vào lại màn hình, nếu không thì `+0x22` trừ 1, số lượng trang bị tồn kho trừ 1, phần số 7 phục hồi sức mạnh, ghi slot −1, `800A5924(机体,1)` trải rộng, vào lại màn 18; Các dòng khác: `D_801DD63E=槽位光标`, `D_801DEC58=0`, màn hình tiếp theo 19. Sau đó di chuyển con trỏ theo chế độ (số vị trí hoặc số dòng trên mỗi trang), lật trang (`801CDC94`), viết các phần dưới con trỏ kho vào `D_801DECCA` và vẽ lại hướng dẫn | `801D4C94` |

### Danh sách chủ sở hữu (Màn hình 19)

| Dự án | Cơ sở |
| --- | --- |
| Bố cục 0x7F: Bảng điều khiển (21,21)–(299,219), nhãn Được trang bị のパーツ (24,24); bảng vị trí tên thành phần vị trí cục bộ `D_801DC6CC`: (112,24) (209,24) (112,42) (209,42) | Bảng bố trí, `801CCA80` |
| Khởi tạo `801D5168`: nền, bố cục, `801CC988` tạo bảng giữ `D_801DCF10` (một mục cho mỗi bản sao được giữ: số vị trí của máy giữ nó hoặc 0xFFF nghĩa là không được trang bị), `801CCA80` danh sách bản vẽ, hình con trỏ 0x14 (21,63) 278×17, mờ dần | `801D5168`, `801CC988` |
| Mỗi hàng y=64+17n: tên thành phần x=24; có giá đỡ: tên thân x=120, tên phi công x=232; không được trang bị: `------------` x=120, `--------` x=232 | `801CCA80` |
| Mỗi khung `801D51EC`: B → Quay lại màn hình 18. A: Bản sao đã chọn không được trang bị → Nếu ​​khe mục tiêu trống, hãy thêm 1 vào `+0x22` và thêm 1 vào số thiết bị, nếu không thì thay thế (loại bỏ các bộ phận ban đầu và khôi phục sức mạnh về số 7); bản sao nằm trên một phần thân khác → xóa nó khỏi phần thân đó (`+0x22` trừ 1, viết −1, `800A5924`) rồi cài đặt nó vào máy này. Nếu máy giống nhau và có cùng khe cắm thì cũng giống như tháo ra. Cuối cùng `800A5924(本机,1)`, `D_801DEC58=0`, quay lại màn hình 18 | `801D51EC` |

## 2. Phương thức tiếp quản

Mã nguồn: [`parts_page.cpp`](../../src/host/parts_page.cpp) (bộ điều hợp chuỗi trò chơi), [`frontend.cpp`](../../src/native/ui/frontend.cpp)'s `parts_sync` (trang), bao bì [`game_hooks.cpp`](../../src/host/game_hooks.cpp) (`parts_build`/`parts_step`/`parts_frame`, sáu móc nằm trong `generate_cpu.py` và `NATIVE_HOOKS`, mã CPU phải được tạo lại sau khi sửa đổi). Khi phiên bản gốc được chọn trong "Màn hình liên trường" của trang cài đặt, cả ba lối vào công trình đều được đưa về màn hình gốc; `SRW64_NATIVE_PARTS=0` hoặc khi hồ sơ không được tải, màn hình gốc được giữ lại trong suốt quá trình chạy.

| chức năng ban đầu | giấy gói |
| --- | --- |
| `801D4A00` Khởi tạo danh sách | Không điều chỉnh chức năng ban đầu. Giữ các cuộc gọi nền (bao gồm các số ngẫu nhiên), `801CB540` (sắp xếp, số trang), bản sao hàng và ghi `D_801DEC5C` vào máy đã chọn; không xây dựng bố cục, văn bản hoặc hình con trỏ. Làm mờ dần sau khi đăng ảnh chụp nhanh |
| `801D4A98` danh sách trên mỗi khung hình | Di chuyển/lật trang: Bộ điều hợp ghi trang, dòng, sao chép và `D_801DEC5C`, phát 0xB9 (8 dòng trên mỗi trang, trang cuối cùng hạ thấp con trỏ để phù hợp với bản gốc). Xác nhận/Quay lại: Chèn chức năng định hình lại cạnh A/B |
| `801D4BEC` Khởi tạo vị trí | Không điều chỉnh chức năng ban đầu. Giữ nền, trang kiểm kê 1, `801CBA78`, chế độ 0, xóa số đếm; ghi giá trị ban đầu của `D_801DECCA` là 0x12 (ghi 0 trong phiên bản gốc, sẽ làm cho bản xem trước không di chuyển có phần thưởng là phần 0 - trang sẽ được hiển thị không thay đổi theo はずす dưới con trỏ) |
| `801D4C94` khe trên mỗi khung hình | Chế độ 0: ghi di động `D_801DEC58`; xác nhận rằng bộ điều hợp chuyển sang chế độ 1 (nhánh A ban đầu chỉ xây dựng các họa tiết con trỏ, xóa và đếm dòng, không có họa tiết nào được xây dựng ở đây); quay lại tiêm B. Chế độ 1: Di chuyển/lật trang để ghi `D_801DD0A2`/`D_801DD63C` và ghi thành phần dưới con trỏ vào `D_801DECCA`; hủy bỏ việc chuyển về chế độ 0 bằng bộ điều hợp (các họa tiết và văn bản do nhánh B ban đầu phát hành chưa bao giờ được xây dựng ở đây); xác nhận tiêm A, hoàn tất việc dỡ hàng hoặc vào màn hình từ phiên bản gốc 19 |
| `801D5168` khởi tạo chủ sở hữu | Không điều chỉnh chức năng ban đầu. Giữ nguyên nền bằng `801CC988` |
| `801D51EC` giá đỡ trên mỗi khung | Di chuyển ghi `D_801DEC58`; xác nhận/trả lại tiêm A/B |

**Ảnh chụp nhanh**: `status.parts_page`: `screen` (`list`/`slots`/`holders`), `serial`, `labels`; danh sách có `page` (0 (từ), `pages`, `cursor`, `rows[]` (`slot`, `number`, `name`, `pilot`, `level`, `parts[]{part,name}`, `en`); màn hình vị trí có `unit` (giống như trên), `cursor` (vị trí), `mode` (0 vị trí/1 Kho), `stats[]{key,current,preview}`, `selected` (số phần dưới con trỏ kho, 0x12＝はずす), `description[]`, `inventory{page,pages,cursor,rows[]{part,name,remove,equipped,owned}}`; màn hình chủ có `unit`, `part{part,name}`, `target_slot`, `cursor`, `rows[]{free,slot,name,pilot}` Nhật ký sự kiện `parts-page-events.jsonl`.

**Trang**: Bố cục ba khối dựa trên hình chữ nhật ở trên; mỗi hàng của danh sách là 16, hàng vị trí là 17, hàng tồn kho là 16 và hàng chủ sở hữu là 17; cột xem trước có màu xanh lá cây phía trên giá trị hiện tại và màu đỏ bên dưới (phiên bản gốc sử dụng hai màu văn bản).

**Gỡ lỗi**: ID ổn định `parts:N` (hàng danh sách hiện tại: danh sách nội dung/khoảng không quảng cáo/người giữ; nhấp vào dòng con trỏ để xác nhận, nhấp vào các dòng khác để di chuyển), `parts-slot:N` (dòng vị trí; nhấp để quay lại vị trí đầu tiên khi kho được mở); bàn phím ↑↓, ←→ (lật trang), Enter/Z, Esc/X; điều kiện chờ `parts_page`.

## 3. Xác minh máy thật (2026-09-23)

```sh
.venv/bin/python tools/recomp/debug/check_parts.py            # 构建并检查
.venv/bin/python tools/recomp/debug/check_parts.py --reuse-build
```

`intermission-cold-1` Đã lưu xong chương 1 (không có phần nào). Đang chạy `build/recomp/debug/20260923T031518.017920Z/`: `parts-checks.json` đã vượt qua 14 mục, mã thoát 0.

| Kiểm tra | Kết quả |
| --- | --- |
| Danh sách | ダイターン3（万 Zhang Lv5), ドール（シモーヌ Lv3）, スイームルグ（マナミ Lv2), theo thứ tự giảm dần theo cấp độ người lái; 1/1 trang; ↑↓ vòng lặp đầu tiên và cuối cùng; tags Tăng cường パーツ／Trang bị のパーツ／レベル Lấy từ văn bản gốc |
| Màn hình khe | ダイターン3 Hai ô trống; Giá trị hiện tại của sáu khả năng = xem trước (HP 8000, EN 200, khả năng di chuyển 5, khả năng di chuyển 70, áo giáp 1800, giới hạn 270); hàng tồn kho đầu tiên はずす, con trỏ 0, trang 1 |
| Con trỏ khe | ↓ tới ô thứ hai, ↑ quay lại |
| Hàng tồn kho | Z mở (chế độ 1, `selected` = 0x12, không có mô tả); X đóng lại chế độ 0 |
| はずす Khe chống trống | Z Z Sau khi phiên bản gốc vào lại màn hình (tăng nối tiếp), slot vẫn trống |
| Trở về |

Ở phiên bản đầu tiên, bàn phím không phản hồi nhưng chuột vẫn bấm được: Trong bản phân phối bàn phím của `frontend.cpp`, có hai người bảo vệ bấm vào "Trang nào đang mở" để thả ra, không tính các trang mới đã được thêm vào. Con trỏ kiểm kê phiên bản đầu tiên đọc 0xFFFF: phiên bản gốc chỉ xóa `D_801DD0A2` khi vào chế độ 1 và ghi 0 vào chính trang đó khi xây dựng.

## 4. Chưa được xác minh

- Thiết bị, thay thế, lấy từ máy bay khác: Không có phần nào trong kho lưu trữ của tập đầu tiên và bạn chỉ có thể kiểm tra màn hình vào lại của slot trống bằng はずす; tập lệnh `check_parts.py` sẽ tiếp tục kiểm tra màn hình thiết bị và giá đỡ khi có các bộ phận trong kho và cần phải lưu các bộ phận đó.
- Lật trang danh sách nhiều trang (trên 8 đơn vị, trên 7 phần).
- Những thay đổi về sức mạnh của phần 7 và hiệu ứng logo của phần 9/10 chỉ được xử lý bởi phiên bản gốc và sẽ không hiển thị trên trang.