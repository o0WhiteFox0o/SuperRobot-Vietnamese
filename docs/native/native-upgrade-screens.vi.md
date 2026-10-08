> **Ngôn ngữ / Language:** [Tiếng Việt](native-upgrade-screens.vi.md) · [English](native-upgrade-screens.en.md) · [中文](native-upgrade-screens.md)

# Màn hình sửa đổi: danh sách cơ thể, tiếp quản năm sửa đổi và sửa đổi vũ khí

Ngày: 22-09-2026. Trạng thái: Năm màn hình chuyển đổi **ユニット (danh sách máy bay, năm lần biến hình) và chuyển đổi vũ khí (danh sách máy bay, danh sách vũ khí, xác nhận chuyển đổi) đã được tiếp quản và xác minh trên máy thực tế; bước chuyển đổi vũ khí thực tế thành công (sau khấu trừ, giá trị gia tăng, sửa đổi lời nhắc vũ khí bổ sung) vẫn chưa được hoàn thành do không đủ kinh phí lưu trữ. Phương pháp này giống như [Menu chính Interfield](native-intermission-menu.md): chức năng khởi tạo ban đầu bỏ qua bản vẽ và trang gốc vẽ cùng một bảng theo hình chữ nhật bố cục trong ROM; chọn chỉ viết con trỏ và chèn cạnh A/B vào chức năng từng khung ban đầu. Giá trị sửa đổi, giá, giới hạn trên, chênh lệch và trang bị EW vẫn được xác định bởi hàm ban đầu và móc nối của [quy tắc sửa đổi 15 đoạn](../gameplay/upgrade-limits.md).

## 1. Màn hình gốc (phân tích tĩnh)

Số màn hình liên trường: 2 = ユニット danh sách đơn vị đã sửa đổi, 3 = Danh sách đơn vị đã sửa đổi vũ khí, 10 = năm sửa đổi, 11 = danh sách vũ khí, 12 = xác nhận sửa đổi vũ khí. Các tọa độ đều là 320 × 240.

### Danh sách đơn vị (Màn hình 2/3)

| Dự án | Cơ sở |
| --- | --- |
| Bố cục 0x6B (0x6C cho màn hình 3), một bảng (21,21)–(299,219); thẻ cố định: ユニット biến đổi (128,24), tính cơ động (24,176), áo giáp (136,176), giới hạn (232,176), パイロット(24,200), quỹ (192,200) | Bảng bố trí thường trú `D_800C8BB8` |
| Danh sách được tạo bởi `801C6BFC` (Màn hình 3 là `801C6B80`): mảng u16 với số vị trí nội dung bắt đầu từ `D_801DD210`, số lượng `D_801DD0A0`; 7 dòng mỗi trang, số trang `D_801DD14A` **bắt đầu từ 1**, hàng `D_801DEBC8` (bản sao `D_801DD53A`); `D_801DECD4` Ghi nhớ số máy bay được chọn gần đây nhất và con trỏ sẽ quay lại số đó khi nhập lại | `801CF388`, `801C6F80` (khe = mảng [(trang−1)×7+hàng]) |
| Mỗi dòng: tên máy bay (văn bản 0x20F + số máy bay) x=24, `HP␣␣␣␣EN` (0x101A) x=176, HP `%4d` x=200, EN `%3d` x=272; y=44+18× dòng | `801C6C78` |
| Phần thân được chọn: `800A5254(机体,2)` Sau khi tính toán lại, `801C4DE4` cộng với các bộ phận tăng cường được thêm vào để thu được các giá trị được hiển thị: HP `D_801DEB08`, khả năng di chuyển `D_801DD14E`, áo giáp `D_801DEB06`, giới hạn `D_801DEB04`; EN Ví dụ đọc trực tiếp `+0x0A` | `801C6F80`, `801C4DE4` |
| Số trang `%2d/%2d` (24,24); Giá trị cơ động (80.176), Giáp (176.176), Giới hạn (272.176); Tên tài xế (4382 + số tài xế) (72.200), không người lái `--------`; Tài trợ `%8d` (230,201) | Tương tự như trên |
| Mỗi khung `801CF564`: A → `D_801DEC58=0`, ảnh tiếp theo 10 (ảnh 3 là 11 và xóa `D_801DEBD2/D_801DD20A/D_801DEC5A=999`), chuyển tiếp; B → hình tiếp theo 0. Các phím điều hướng được xử lý bởi `801CCEC4` (lật trang), `801CD060` (vẽ lại chi tiết), **Số 0 được ghi khi không nhấn phím** | `801CF564`, `801D04A4` |
| Danh sách sửa đổi vũ khí liệt kê từng dạng (ダイターン3／ダイファイター／ダイタンク), vì vũ khí được chia theo dạng | `801C6B80` |

### Ngũ Biến (Màn 10)

| Dự án | Cơ sở |
| --- | --- |
| Bố cục 0x75, Bảng điều khiển (21,10)–(302,219); Thẻ: どのkhả năngを Biến đổiしますか? (24,50), (TỐI ĐA で␣␣ giai đoạnまで) (24,70), Quỹ (24,96), Phí (24,114), HP/EN/Tính cơ động/Giáp/Giới hạn x=24 y=135+17n, mỗi hàng ► tại x=112 | Bảng bố trí |
| Khởi tạo `801CF680`: nền `80085B94(0,1)` (bảng màu tối, sử dụng số ngẫu nhiên), sơ đồ nội dung `801C6410(机体号,176,8)`, giới hạn trên `%2d` (68,70), tên nội dung (32,18), quỹ (110,96), `801C80E0` vẽ năm dòng, con trỏ `D_801DEC58` Khe yêu tinh 0x14; đã xóa trạng thái: `D_801DDA30=2`, `D_801DECD8=0`, `D_801DEC50=0xFF`, `D_801DECC1/C0=0` | `801CF680` |
| `801C80E0` Mỗi hàng: giá trị hiện tại x≈72–88, giá trị xem trước x≈128–144 (số lượng phân đoạn = giới hạn trên `-----`), văn bản tỷ lệ x=176; xem trước = giá trị hiện tại + `D_801DC4AC[项][段数]` | `801C80E0` |
| Mỗi khung `801CF988`, trạng thái `D_801DECD8`: 0 chọn hàng (con trỏ `801C4A20` 0–4; vẽ lại chi phí và lưu giá khi con trỏ thay đổi `D_801DEBCC`, `D_801DEC50` ghi nhớ hàng đã vẽ); A: số lượng phân đoạn < giới hạn trên và quỹ ≥ giá → trạng thái 1 bomよろしいですか?／はい／いいえ (bố cục 0x74＋0x76, con trỏ `D_801DD0A2`), nếu không thì thông báo bật lên trạng thái 2 (bố cục 0x87, văn bản 0x102Fこれ上の Reformはできません hoặc quỹ 0x1030がfootりません） B → màn hình tiếp theo 2 | `801CF988` |
| Trạng thái 1 Nhấn A và con trỏ = はい: Quỹ −= `D_801DEBCC`, khả năng += tăng xem trước, +1 nếu số lượng phân đoạn < giới hạn trên, `800A5924` truyền sang dạng kết hợp/biến dạng, `801CF85C` Phán đoán EW (trả về ≠999, sau đó chuyển đến màn hình chỉnh trang), nếu không thì vào lại màn hình 10 (vẽ lại sau khi mờ dần và ra ngoài) | Tương tự như trên |

### Danh sách vũ khí (Màn hình 11) và xác nhận sửa đổi vũ khí (Màn hình 12)

| Dự án | Cơ sở |
| --- | --- |
| Bố cục danh sách 0x77, bảng (21,21)–(299,219); nhãn cột: tên vũ khí (98,24), sức tấn công (170,24), tầm bắn (226,24), đánh trúng (266,24); nhãn chi tiết: số lượng tên lửa (24.160), địa hình (104.160), trên không/đất/biển/không gian (144/184/224/264.160), sức mạnh cần thiết (24.184), kỹ năng cần thiết (168.184), mức tiêu thụ EN (24.201), chỉnh sửa クリティカル (168.201) | Bảng bố trí |
| `801C7254` Tạo danh sách: Vũ khí có `+0x18 & 0x600` là 0 trong mảng vũ khí cơ thể (`+0x30`, 0x24 byte/mảnh), lưu trữ chỉ mục `D_801DEC68`, số lượng `D_801DECBE`, số trang `D_801DDA9C`, số hàng trên trang này `D_801DEC56`; 6 dòng mỗi trang; hàng `D_801DEC58` (sao chép `D_801DDA34`), trang `D_801DD20C` bắt đầu từ 1; `D_801DEBD2` Ghi nhớ chỉ số vũ khí sửa đổi lần cuối | `801C7254`, `801D0600` |
| Mỗi dòng (y=47+16×line): tên menu (0xA8B+số vũ khí, có lưới/bắn/dấu P) x=24, sức tấn công `%4d` x=176, phạm vi `%d_%2d` (một số khi tối thiểu=tối đa), nhấn `+%2d`/`-%2d` (0 Đối với `$%2d`, `$` hình tượng chưa được xác nhận) | `801C75C0` |
| Chi tiết: Số lượng mũi tên là `%2d/%2d` (`--/--` khi `+0xC` là −1). Bốn lưới địa hình được chuyển đổi từ `800A6104` để chuyển cấp độ `+0x10..+0x13` thành chữ cái (1 `-`, 2 D, 3 C, 4 B, 5 A). Công suất yêu cầu là `%3d(%3d)`=Vũ khí `+0xE` (sức mạnh hiện tại của người lái là `+0x20`), mức tiêu thụ EN=vũ khí `+0xD` (sức mạnh hiện tại của máy là EN `+0x08`), kỹ năng yêu cầu=`+0xF` ≥2 Hiển thị bằng số văn bản, クリティカルsửa = `+0x14` có dấu | `801C7A9C` |
| `801D087C` mỗi khung: Chỉ có tiếng bíp trên vũ khí có công suất 0; nếu không thì `D_801DD0A2=0`, màn hình tiếp theo 12; B → đặt lại trang, màn hình tiếp theo 3. Đã thay đổi lời nhắc vũ khí bổ sung (`D_801DEC5A≠999`) để được vẽ với bố cục 0x8C trong quá trình khởi tạo danh sách, trạng thái 1, A/B đã đóng | `801D0600`, `801D087C` |
| Xác nhận bố cục 0x78: (21,61)–(299,107) Tên vũ khí (24,64), tỷ lệ (176,64), sức tấn công (24,88) hiện tại (88,88) ► (120,88) xem trước (144,88), giá trị quỹ (184,88) (230,89); (181.107)–(299.123) Giá trị chi phí (254.107); (261,133)–(291,171) はい／いいえ, con trỏ `D_801DD0A2` | bảng bố trí, `801D0C7C` |
| `801D0C7C`: Theo loại vũ khí `+0x15` lấy bảng giá và bảng xem trước rồi viết `D_801DEBCC`, `D_801DECD0`; khi số lượng đoạn ≥ giới hạn trên (phạm vi `+0x51`, `weapon`), hãy thay đổi bố cục bản vẽ thành 0x87これ上の Reformはできません | `801D0C7C` |
| `801D1100`：はい → Khấu trừ nếu quỹ ≥ giá, sức mạnh = xem trước, số phân đoạn < giới hạn trên +1, `800A5F84` Đồng bộ hóa vũ khí đôi, số phân đoạn = giới hạn trên `801D0AE4` Mở khóa thêm vũ khí và xây dựng lại danh sách, quay lại màn hình 11; Rút tiền không đủ tiềnが足りません；いいえ／B／Bất kỳ phím nào trên tin nhắn → Quay lại màn hình 11 | `801D1100` |

Người đọc bảng giá, bảng tăng và giới hạn trên có thể tham khảo Phần 3 và 5 của [Số lượng phân đoạn chuyển đổi và giới hạn trên](../gameplay/upgrade-limits.md).

## 2. Phương thức tiếp quản

Mã nguồn: [`upgrade_page.cpp`](../../src/host/upgrade_page.cpp) (bộ điều hợp chuỗi trò chơi), trình bao bọc của [`frontend.cpp`](../../src/native/ui/frontend.cpp)'s `upgrade_sync` (trang), [`game_hooks.cpp`](../../src/host/game_hooks.cpp). Khi phiên bản gốc được chọn trong "Màn hình liên trường" trên trang cài đặt, tất cả bốn mục xây dựng sẽ được đưa về màn hình gốc (`original_screens()` và trang vẫn đang mở sẽ bị đóng cùng lúc); `SRW64_NATIVE_UPGRADE=0` hoặc khi hồ sơ không được tải, màn hình gốc được giữ lại trong toàn bộ quá trình chạy.

| chức năng ban đầu | giấy gói |
| --- | --- |
| `801CF388`／`801D03D0` Khởi tạo danh sách | Không điều chỉnh chức năng ban đầu. Dành riêng: lệnh gọi nền (bao gồm số ngẫu nhiên), chức năng tạo danh sách, khôi phục con trỏ bằng cách nhấn `D_801DECD4`, tính toán lại máy bay đã chọn; bố cục, văn bản và các họa tiết con trỏ sẽ không được xây dựng. Làm mờ dần sau khi đăng ảnh chụp nhanh. |
| `801CF564`/`801D04A4` danh sách trên mỗi khung hình | Khi đầu vào được lọc về 0, hàm ban đầu được viết bằng 0 và được gọi như bình thường. Di chuyển: Bộ điều hợp ghi trang, dòng, `D_801DEC5C` và tính toán lại nội dung, phát 0xB9. Xác nhận/Quay lại: Đưa chức năng điều chỉnh cạnh A/B để viết cảnh và chuyển tiếp tiếp theo. |
| `801CF680` Năm lần khởi tạo | Trong phạm vi `decide` hiện có: Không điều chỉnh chức năng ban đầu, giữ lại lệnh gọi trong nền và xóa trạng thái; `D_801DEC50` được viết dưới dạng con trỏ hiện tại, do đó, mỗi hàm khung ban đầu sẽ không tự vẽ lại. |
| `801C80E0` năm dòng vẽ | bị bỏ qua hoàn toàn khi trang hiển thị (nó chỉ vẽ nhưng sẽ điều chỉnh `800A5254` trước; bộ điều hợp tự điều chỉnh `800A5254`+`801C4DE4` trước khi xuất bản ảnh chụp nhanh). |
| `801D0600` Khởi tạo danh sách vũ khí | Không điều chỉnh chức năng ban đầu. Giữ nền, `801C7254`, nhấn `D_801DEBD2` để khôi phục con trỏ; đọc `D_801DD20A`/`D_801DEC5A` để quyết định xem có hiển thị lời nhắc vũ khí bổ sung hay không rồi xóa nó thành 999. |
| `801D087C` Danh sách vũ khí trên mỗi khung hình | Tương tự như danh sách nội dung: di chuyển các dòng và trang viết của riêng bạn; xác nhận/quay lại để tiêm A/B. Khi đóng cửa sổ nhắc, chỉ xóa trạng thái và chức năng ban đầu không được điều chỉnh (nó chỉ giải phóng những gì nó vẽ). |
| `801D0C7C` xác nhận khởi tạo | Trong phạm vi `weapon`: chức năng ban đầu không được điều chỉnh. Giữ nguyên nền và viết `D_801DEBCC`, `D_801DECD0` theo loại; khi số lượng đoạn ≥ giới hạn trên hợp lệ, trang sẽ hiển thị trực tiếp ở trên. |
| `801D1100` thừa nhận từng khung hình | trong phạm vi `weapon`.はい: Khi không đủ tiền, trang hiển thị "Tiền đủ" (chức năng ban đầu không chạy), nếu không A sẽ được đưa vào; "いいえ", tin nhắn được đóng lại và trả về: B được tiêm. |
| `801CF988` Năm mục trên mỗi khung | Trong phạm vi `decide`. Di chuyển: ghi con trỏ và `D_801DEC50`. Lựa chọn: Bộ điều hợp xác định xem có bật lên cửa sổ xác nhận hay thông báo dựa trên "số lượng phân đoạn < giới hạn trên hiệu dụng và số tiền ≥ giá". Cả hai sẽ được hiển thị trên trang gốc và cửa sổ bật lên ban đầu sẽ không được tạo. Xác nhận: Viết `D_801DEBCC=价格`, `D_801DECD8=1`, `D_801DD0A2=0`, tiêm A và hàm ban đầu hoàn thành việc khấu trừ, cộng giá trị, truyền bá, xác định EW và nhập lại. Trở lại: Tiêm B. |

**Quy tắc cỡ 15 phân đoạn**: Mỗi mục trong ảnh chụp nhanh chứa `level`, `cap` (giới hạn trên hiệu quả là `allowed_cap`: mức đột phá là 15), `original_cap`, `price`/`preview` (chỉ khả dụng khi số lượng phân đoạn < giới hạn trên hiệu quả, bảng trong bộ nhớ được đọc trực tiếp và bản vá tệp quy tắc có hiệu lực) và `gauge`. Các quy tắc của chuỗi tỷ lệ nhất quán với `upgrade_rules.hpp`: trong giới hạn trên của tác phẩm gốc ▶/▷ và vượt quá ●/☆; bật đột phá và vẽ đến giới hạn trên hiệu quả, tắt và chỉ vẽ theo số phân đoạn hiện có. "N giai đoạn tối đa" hiển thị giới hạn trên hiệu quả; khi quy tắc tăng giới hạn trên (`original_cap` < `cap`), hộp quỹ/chi phí và màn hình xác nhận vũ khí của năm màn hình, mỗi màn hình có thêm một dòng `upgrade_cap_original` (giới hạn trên ban đầu của N màn chơi ►▷ · Đột phá giới hạn trên ●☆), cho phép người chơi phân biệt số lượng màn chơi vốn có và số lượng màn đột phá. Hai móc phạm vi của phiên bản gốc không bị thay đổi, do đó, nó có thể được thay đổi hay không và số tiền sẽ bị trừ là bao nhiêu vẫn được xác định bởi phiên bản gốc sau khi `+0x51` được viết lại bởi phạm vi - bộ điều hợp chỉ sử dụng cùng một `allowed_cap` để xác định cửa sổ nào sẽ bật lên.

**Ảnh chụp nhanh**: `status.upgrade_page`: `screen` (`list`/`stats`/`weapons`/`weapon` ), `kind` (`stats`/`weapons`), `serial`, `funds`, `cursor`; danh sách là `page`(0 (từ), `pages`, `rows[]` (`slot`, `number`, `name`, __INL_COD E_180__, `en`, `mobility`, `armor`, `limit`, `pilot`); năm mục là `unit` (`slot`, `number`, `name`, `art`), __INL_CODE_191 __, `rows[]` (ở trên), `window` (trống/`confirm`/`maxed`/`poor`); danh sách vũ khí là `rows[]` (`index`, `number`, `name`, `power`, `range_min/max`, __ INL_CODE_203__, `critical`, `en`, `morale`, `skill`, `ammo`, __IN L_CODE_209__, `terrain`, `level`, `type`, `cap`, `price`, __INL_ CODE_215__, `gauge`), `unit.en`/`unit.morale`, `window` (trống/`bonus`); màn hình xác nhận có `weapon` (cùng một dòng), `cursor` (はい 0／いいえ 1), `window` Nhật ký sự kiện `upgrade-page-events.jsonl`.

**Trang**: Bảng danh sách được bố trí theo hình chữ nhật 0x6B và các vị trí cột giống như trong phiên bản gốc; Năm màn hình được chia thành năm phần theo ảnh chụp màn hình ban đầu: tên máy bay, câu hỏi, kinh phí/chi phí, sơ đồ máy bay và năm yếu tố (bố cục ban đầu chỉ có một khung bên ngoài và khoảng cách bên trong được vẽ bởi hình gốc, ở đây nó được xác định theo ảnh chụp màn hình). Sơ đồ cơ thể sử dụng tư thế chiến đấu được nhập từ ROM cục bộ (`battle_assets.units`). Cửa sổ xác nhận và cửa sổ thông báo được bố trí trong hình chữ nhật có kích thước 0x74/0x87.

**Quỹ**: Số liệu quỹ trên ba màn hình có thể được sửa đổi trực tiếp bằng cách nhấp vào chúng (xem Phần 6a của [Menu chính liên trang](native-intermission-menu.md)). Việc sửa đổi sẽ ngay lập tức ảnh hưởng đến việc đánh giá và khấu trừ chi phí.

**Gỡ lỗi**: ID ổn định `upgrade:N` (dòng; nhấp vào dòng hiện tại để xác nhận, nhấp vào các dòng khác để di chuyển con trỏ), `upgrade-confirm`, `upgrade-cancel`, `upgrade-dismiss`; bàn phím ↑↓, ←→ (lật trang danh sách), Enter/Z, Esc/X.

## 3. Xác minh máy thật (22-09-2026)

```sh
.venv/bin/python tools/recomp/debug/check_upgrade.py            # 构建并检查
.venv/bin/python tools/recomp/debug/check_upgrade.py --reuse-build
```

`intermission-cold-1` Chương 1 đã hoàn thành và được lưu trữ (quỹ 14500, giới hạn ダイターン3 7). Đang chạy `build/recomp/debug/20260922T044204.774117Z/`: `upgrade-checks.json` đã vượt qua 21 mục, mã thoát 0.

| Kiểm tra | Kết quả |
| --- | --- |
| Danh sách | Ba đơn vị, 1/1 trang, HP 8000/EN 200/Driver Wan Zhang/Capital 14500; ↑↓ Chu kỳ đầu tiên và chu kỳ cuối cùng |
| Năm mục mở | ダイターン3, tối đa 7 cấp, HP 0 cấp, giá 2000, xem trước 8200, tỷ lệ `▷×7` |
| Cửa sổ xác nhận | Z bật lên, X hủy |
| Biến đổi một lần | Vốn 12500, HP đoạn 1 8200, đoạn tiếp theo 4000, tỷ lệ `▶▷▷▷▷▷▷` (đọc sau khi vào lại màn hình) |
| Thay đổi ba đoạn liên tiếp | Quỹ 2500, đoạn 3; đoạn 4 8000 → Quỹ が足りません, Esc để đóng |
| Trở về | Con trỏ trong danh sách vẫn ở mức ダイターン3, HP 8600 (giá trị hiển thị sau khi truyền); sau đó quay lại menu chính, con trỏ ở ユニットTransformation |
| Sửa đổi vũ khí | 6 dòng danh sách nội dung gốc (HP của ba dạng đều là 8600, biểu thị rằng mức lây lan `800A5924` có hiệu quả); Z lọt vào danh sách vũ khí bản địa |
| Danh sách vũ khí | ダイターン3 sáu vũ khí; đầu tiên ダイターンミサイル loại 2, màn 0, giá 4000, xem trước 900→1000; ↑↓ di chuyển |
| Xác nhận vũ khí | Z mở cửa sổ はい／いいえ; いいえ trở lại danh sách và con trỏ không thay đổi; はい hiển thị quỹ がfootりません dưới 2500 quỹ, X đóng danh sách; |

Ảnh chụp màn hình của danh sách được chụp khi bắt đầu phần mờ dần và nền vẫn màu đen: trang xuất hiện trước phần mờ dần ban đầu, giống như menu chính và là trạng thái chuyển tiếp đã biết.

### Bắt đầu đột phá (22-09-2026)

```sh
.venv/bin/python tools/recomp/debug/check_cap_break.py            # 构建并检查
.venv/bin/python tools/recomp/debug/check_cap_break.py --reuse-build
```

Đối với cùng một kho lưu trữ, các quy tắc là `fixed` + `upgrade-cap-break` và số tiền được đổi thành 900000 bằng cách sử dụng hộp quỹ trên trang (không cần tạo một bản lưu trữ khác). Chạy `build/recomp/debug/20260922T150623.097491Z/` (năm mục) và `20260922T151306.190823Z/` (chạy lại với các dòng được đánh dấu), `cap-break-checks.json`:

| Kiểm tra | Kết quả |
| --- | --- |
| Năm mục mở | ダイターン3 `cap` 15, `original_cap` 7; thang âm năm dòng đều là `▷×7 ☆×8`; HP cấp 0, giá 2000, xem trước 8200; tiêu đề "Tối đa 15 cấp độ" |
| HP 1–7 giai đoạn | Mỗi giai đoạn sẽ trừ 2000/4000/…/14000 vào giá bàn và số tiền sẽ giảm tương ứng |
| Đoạn 7 (giới hạn trên của tác phẩm gốc) | Vẫn có thể thay đổi: phí 16000, xem trước 9600; thang đo `▶×7 ☆×8` |
| Đoạn 8 | Quỹ 828000 (trừ 16000), HP 9600, đoạn tiếp theo 18000; thang đo `▶×7 ● ☆×7` |
| Đoạn 15 | Vốn 660000 (2000+…+30000=240000), HP 11000, không mất phí; Bom Z phía trên これの SỬA ĐỔI はできません |
| Quay lại danh sách | HP hiển thị 11000 (giá trị sau khi truyền) |
| Vũ khí はい | ダイターンミサイル Loại 2: khấu trừ 4000, công suất 900→1000, 1 đoạn, tỷ lệ `▶ ▷×6 ☆×8`; đoạn tiếp theo 8000. **Sau khi nâng cấp phiên bản gốc, viết màn hình tiếp theo 12 và vào lại màn hình xác nhận của cùng loại vũ khí**, không quay lại danh sách (phù hợp với việc nhập lại màn hình năm mục), phiên bản đầu tiên của tập lệnh sẽ hết thời gian chờ sau khi nhấn "Quay lại danh sách" để chờ |

Phiên bản đầu tiên của dòng được đánh dấu được đặt vào ô câu hỏi và bị cắt ở cuối ô (ô chỉ cao hai dòng) và được chuyển sang dòng thứ ba của ô quỹ/chi phí; phiên bản này chỉ được kiểm tra ngữ pháp và không có ảnh chụp màn hình nào được chụp lại. Người dùng 2026-09-22 đã thử chuyển đổi đột phá theo cách thủ công và chức năng đã được thông qua.

**Chưa được xác minh**:

- Quy mô và suy diễn vũ khí thay đổi vượt quá giới hạn trên ban đầu (8 đoạn): Kịch bản đã được viết (`weapon-level-8`, `weapon-past-original-cap`) nhưng không đạt đến bước này sau khi chạy hai lần (lần đầu kịch bản chờ màn hình lỗi, lần thứ hai Host bị đóng thủ công).
- Thay đổi cửa sổ nhắc vũ khí bổ sung: vũ khí ダイターン3 không được kích hoạt trong hai lần chạy này và cửa sổ nhắc nhở vẫn chỉ có mã tĩnh.
- EW Liệu trang có được đóng chính xác hay không sau khi kích hoạt trang phục từ năm màn hình (`frame` gọi lại được đóng bằng cách nhấn "màn hình tiếp theo ≠ màn hình hiện tại", chưa được kiểm tra).
- Lật trang danh sách nhiều trang (trên 8 đơn vị).
- Hiển thị sau khi sửa giá trong file quy tắc (`SRW64_UPGRADE_RULES`).
- **Biểu tượng dấu vũ khí** (24/09/2026, yêu cầu của người dùng): Lưới, bắn, P (có sẵn sau khi di chuyển), B (chùm) và dấu MAP trong danh sách vũ khí được thay thế bằng biểu tượng gốc và không còn sử dụng huy hiệu văn bản màu nữa. Các trang vũ khí để xem khả năng chia sẻ cùng một bảng.
- Hình tượng biểu tượng gốc: 244 lưới (nắm tay), 243 phát bắn (tầm nhìn), 241 P, 242 B, 575 MAP (`reference/original-glyph-map.csv`).
- **Chế độ hình ảnh HD**: Sử dụng biểu tượng vector ở phông chữ ký hiệu `SRW64Symbols.ttf`, điểm mã là U+E000+cỡ phông chữ gốc (U+E0F4, U+E0F3, U+E0F1, U+E0F2, U+E23F).
- Vẽ lại bởi `tools/content/build_symbol_font.py` theo biểu tượng gốc; các chữ cái P, B và MAP được lấy từ DejaVu Sans Bold.
- Nắm tay: Sử dụng biểu tượng gốc làm cơ sở, ba phiên bản được vẽ lại bằng Qianwen Image 3.0 Pro. Người dùng chọn phiên bản 3. Sau đó, sử dụng `tools/content/trace_marker.py` để vẽ `content/fonts/marker-fist.svg` và làm dày đường kẻ lên 9,5% chiều cao của biểu tượng. Hình tượng vừa với hộp 680×680, rộng hơn và ngắn hơn một chút so với biểu tượng hẹp (600×760), khiến nó có vẻ lớn như các biểu tượng khác.
- Tạo bản ghi (đầu vào, từ nhắc, tham số, ba ứng viên) trong `assets/hd-ai/weapon-markers/`, không nhập git.
- Người dùng không hài lòng với phiên bản vẽ tay: phiên bản gốc có hình nắm tay hướng về bên trái với ngón cái ở trên.
- MAP là huy hiệu nền đỏ có các chữ cái bị cắt bỏ và trang này nhuộm màu đỏ ban đầu `#DE416A`.
- **Chế độ ảnh gốc**: Sử dụng các biểu tượng pixel được cắt ra từ thư viện phông chữ ROM và hiển thị chúng ở kích thước pixel gốc (biểu tượng hẹp 8×10, MAP 13×10).
- `src/srw64_native/battle_assets.py` Được tạo từ ROM của người chơi khi chuẩn bị hồ sơ: tài nguyên phông chữ 0 được tô màu bởi tài nguyên bảng màu trắng 2 (1 màu trắng, 2–10 nét thang độ xám, 11 là nền đỏ của MAP), được phóng to lên 8 lần hàng xóm gần nhất.
- Những hình ảnh này không đi vào git. Bảng màu tối là tài nguyên 4 và chưa được sử dụng.
- Trả lại huy hiệu văn bản khi không có sẵn (không có phông chữ đóng gói, không có biểu tượng).
- 24-09-2026 Xác minh máy thật (`tools/recomp/debug/check_weapon_marks.py`, kho lưu trữ vượt qua chương đầu tiên): Danh sách vũ khí để sửa đổi và xem khả năng hiển thị các biểu tượng tương ứng ở cả chế độ độ phân giải cao và chế độ gốc, với lưới/phát ở phía trước tên và P sau tên.
- Trong lần chạy đầu tiên, các biểu tượng pixel của chế độ vanilla đã đẩy tên vũ khí sang dòng tiếp theo: `.im-panel img` trong bảng điều khiển là thành phần khối. Hình ảnh đánh dấu đã được thay đổi thành các phần tử nội tuyến.
- Số lượng tên lửa tối đa trong chi tiết vũ khí `+0xB` và số văn bản kỹ năng cần thiết `+0xF` được suy ra từ các trường đã đọc và chưa được so sánh từng mục với màn hình gốc. Chữ cái địa hình 2026-09-23 Đã sửa theo ảnh chụp màn hình danh sách vũ khí ban đầu (hạng 4=A).

## 4. Bước tiếp theo

1. Chạy lại `check_cap_break.py` đến phần thứ 8 của vũ khí và cắt vị trí mới của đường được đánh dấu; tìm một cỗ máy trong bảng thêm vũ khí đã sửa đổi để trải nghiệm cửa sổ nhắc nhở.
2. Phần còn lại của màn hình liên trường: Tăng cường パーツ → のりかえ → Xem khả năng → データセーブ.