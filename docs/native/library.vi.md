> **Ngôn ngữ / Language:** [Tiếng Việt](library.vi.md) · [English](library.en.md) · [中文](library.md)

# Thư viện

Ngày: 2026-10-02. Các trang dữ liệu không có trong phiên bản gốc: "Thư viện" ở phía bên trái của MOD ở góc dưới bên phải của màn hình tiêu đề, cũng có thể được truy cập từ "Thư viện·Sách minh họa" trên trang "Chung" của cài đặt (đối với bộ điều khiển không thể chạm tới nút tiêu đề). Cửa sổ đi theo khung cửa sổ cài đặt, bên trái có danh sách và bên phải chi tiết, được chia thành hai trang: “Đơn vị” và “Nhân vật”.

## Nguồn dữ liệu

Tất cả đều được đọc từ ROM của trình phát trong thời gian chạy (`src/host/library.cpp`) và dữ liệu gốc không được bao gồm trong gói phát hành; cơ sở trường có thể được tìm thấy trong [Thư mục dữ liệu trò chơi gốc](../data/original-data-catalog.md). Các bài đọc trên trang này đã được kiểm tra dựa trên mã tải:

| Nội dung | Nguồn | Cơ sở |
| --- | --- | --- |
| Giá trị đơn vị | ROM `0x71B80`, 363 mục × 0x24 | `800A6E68` được sao chép vào thời gian chạy: +0 HP, +2 EN, +4 bit kích thước, +5 bit loại chuyển động, +6 khả năng di chuyển, +8 khả năng di chuyển, +Áo giáp, +giới hạn C, +E..+11 địa hình, +14 chi phí sửa chữa, +18 Thiết bị (2 = Khiên), +1C Khả năng đặc biệt |
| Kích cỡ/Loại/Tên Khả năng Đặc biệt | Nhắn tin `0x446+n`; bảng biểu tượng chuyển động `801DC8F0` của lớp phủ khả năng ユニット, bảng khả năng `801DC8FC` (16 mục `mask, text`) | Tương tự như `ability_page.cpp`; HP reply Hai người chia sẻ một tin nhắn, nhấn `801FA544` Nạp tiền 10%/20% |
| Vũ khí cơ thể | Danh sách vũ khí `0x7E210`, chỉ lấy những mục có số hiệu cơ thể trong ô biểu mẫu | `800A68BC`; Danh sách các dạng phổ biến sẽ không trộn lẫn các loại vũ khí khác |
| Giá trị vũ khí | ROM `0x74E90`, 16 byte | `800A6A18`: +1×100 sức tấn công, +2/+3 tầm bắn, +4 đòn đánh, +5 viên đạn (không có FF), +6 EN, +7 sức mạnh, +8 kỹ năng cần thiết, +9..+C địa hình, +D hiệu chỉnh đòn chí mạng; lưới tên/chụp/P/B/MAP Được đánh dấu bằng `upgrade_page::weapon_markers` bị phá bỏ |
| Khả năng nhân vật | Nhân vật → Bản ghi khả năng `s16[800CA9C4]`, bản ghi `0x7A1A0` × 16 | `800A7FBC`: +1..+6 chiến đấu, bắn, tránh, đánh, phản ứng, kỹ năng, +7..+Địa hình A, +C SP, +khe kỹ năng F |
| Cấp độ hành động vòng thứ hai | Bản ghi khả năng +E | `800A6238`: Sau khi đạt đến cấp độ này, +34 (số hành động mỗi vòng) của người lái xe là 2, nếu không thì là 1; mỗi hành động trên bản đồ giảm +35 đi 1 (`801C2AA4`). Phi công phụ và yêu tinh là 0, hiển thị "-" |
| Tăng trưởng | Hằng số | `800A6238`: Chiến đấu/bắn/phản ứng/kỹ năng +1, tránh/đánh/SP +2 ở mỗi cấp độ, mọi người đều giống nhau; nâng cấp (`801FC470`) cũng được tính toán lại từ bản ghi cơ bản với `800A7F8C` sau cấp +1. Không có con đường phát triển nào khác. Trang này hiển thị các giá trị của cấp 1 (màu trắng) và cấp 99 (màu xanh) cạnh nhau. G Gundunda Fighter (Nhân vật 4, 8, 11, 12, 13, 18) còn có sáu vật phẩm `801FEB70` thuộc trạng thái đặc biệt `0x40000000` +10, và địa hình toàn A, không bao gồm hình minh họa |
| Cấp độ kỹ năng đặc biệt | Ngưỡng `0x7B1B0` × 30 | `800A80F0`: Mức L = giá trị khác 0 nhỏ nhất thứ L trong số 9 ngưỡng; chỉ mức cao nhất được hiển thị cho các mức đạt được ở cùng cấp độ người lái xe vào cùng một thời điểm |
| Lệnh tinh thần | Nhân vật → Hồ sơ tinh thần `s16[800CA6F4]`, hồ sơ `0x7CFB0` × 12 | Sáu nhóm (mức độ mua lại, lệnh); tên `969+指令` |
| Tiêu hao tinh thần | `D_80217F70` (ROM `0x100AD0`), một u8 cho mỗi lệnh | Tương tự cho tất cả mọi người: `801E195C` trừ trực tiếp giá trị đồng hồ đo từ caster SP mà không cần người điều khiển sửa (xem [Tính toán chiến đấu](../gameplay/battle-formulas.md)) |
| Tên | Nội dung `527+id`, ký tự `4382+id`/`4743+id` | Nhân vật chính và đối tác (nhân vật 25–32) sử dụng bản ghi tên mặc định 487/495, không đọc bộ đệm tên đã điền trong kho lưu trữ |
| Hình ảnh | `units` (chân dung chiến đấu), `portraits` (hình đại diện) của `battle_assets` | Sử dụng phiên bản HD ở chế độ HD |

## Phân nhóm công việc

Có hai màn hình trong lớp phủ tiêu đề gốc (`load_0010DA50`, ROM `0x10DA50` có trong `801C4500`) mà người chơi không thể nhập "キャラクターリスト" và "ロボットリスト" (khởi tạo) `801C8F1C`/`801C96FC` không có người gọi, hãy xem [Menu tiêu đề](native-title-menus.md)), dữ liệu và mã hiển thị đã hoàn chỉnh và chúng được sử dụng để nhóm các hình minh họa:

| Bảng | Vị trí | Định dạng | Cách sử dụng ban đầu |
| --- | --- | --- | --- |
| Bảng ký tự | `D_801CB3A0`, ROM `0x1148F0`, 246 mục | `u16 人物, s16 作品, u16 标志` | `801C8AF8` Tạo bảng, `801C8D74` Chi tiết hiển thị họ tên và chức danh công việc |
| Bàn cơ thể | `D_801CB964`, ROM `0x114EB4`, 316 mục | `u16 机体, s16 作品, s16 型号` | `801C930C` Tạo bảng, `801C9578` Mô hình hiển thị chi tiết (văn bản `110+型号`, −1 Không có) và tên công việc |
| Tiêu đề công việc | Văn bản `60+作品` (phiên bản có ngắt dòng `85+作品`), 25 tác phẩm | | Bản dịch tiếng Trung và tiếng Anh nằm trong phần `series` của bảng nhập |
| Bí danh bản ghi trùng lặp | Ký tự `D_800C6A08` (ROM `0x513F8`, 33 cặp), nội dung `D_800C6A8C` (ROM `0x5147C`, 22 cặp) | `u16 重复编号, u16 主编号` | Phán quyết "đã nhìn thấy" ban đầu `80091574`/`80091670` Sử dụng nó để trả lại các bản ghi trùng lặp cho bản ghi chính; khi cùng một số xuất hiện nhiều lần thì cặp cuối cùng sẽ có hiệu lực, sao chép |

Phiên bản gốc không có văn bản giới thiệu: hai màn hình chi tiết chỉ hiển thị như trên và không có đoạn giới thiệu nhân vật/máy trong văn bản ROM. Danh sách ban đầu cũng xác định danh sách nào sẽ hiển thị dựa trên bitmap "đã xem" (`D_8010F4D0`/`D_8010F520`). Các hình minh họa không được mở khóa và tất cả đều được hiển thị.

Thứ tự nhóm: trong bảng → tìm bản ghi chính theo bí danh → bản ghi cùng tên trong bảng → bảng phụ của `library.cpp` (đi bộ ドモンVv., hệ thống Hakuta オーラバトラー, Getter Fighter, ビッグゴールド,ドラゴノザウルス, và những người lính linh tinh có công việc có thể được xác định từ tên của đơn vị)→ Những người không làm việc được phân loại là "những người khác" (AI, ゲリラ, v.v.). **Main・ゲッター1/2/3 Danh sách gốc thuộc về オリジナル, và sách minh họa thuộc về ゲッターロボ** (quyết định của người dùng). Thứ tự của nhóm là thứ tự các tác phẩm xuất hiện lần đầu trong danh sách ban đầu (các tác phẩm của UC → G → W → Super Series → Original). Trong nhóm, thứ tự nằm trong danh sách gốc, còn những thứ ngoài danh sách là thứ tự ROM; các chi tiết của máy cộng với số kiểu máy và tên tác phẩm được hiển thị trên cả hai trang chi tiết.

## Trang

Bố cục được thiết kế dựa trên giao diện "cực lớn" của Steam Deck (1280×800 pixel, 1,48 pixel/dp, khoảng 865×540dp): bảng điều khiển gần như lấp đầy cửa sổ (96%×94%, giới hạn trên 1180×760dp), tiêu đề và tab nằm trên cùng một dòng và danh sách được cố định ở 210dp; khung hình lấy chiều rộng của vùng chi tiết 30% (150–220dp, Deck khoảng 164), địa hình được đặt dưới bản đồ; nhãn vàng (giới hạn trên của chuyển đổi/hành động thứ hai) nằm ở bên phải tên và các nhãn ngắn như trại của nhân vật theo sau tên đầy đủ; giá trị nội dung là 3 ô trên mỗi dòng, ký tự 7 vật phẩm cộng với ô chú giải "Lv1 → Lv99" là 4 ô trên mỗi dòng và phần sửa lỗi tình yêu nằm trên một dòng riêng biệt; nhãn sau tên vũ khí được đổi sang dòng mới, các tên dài trong danh sách sẽ tự động được viết tắt. Toàn bộ trang được xây dựng lại khi kích thước giao diện hoặc cửa sổ thay đổi. Bố cục tương tự thoải mái hơn ở kích thước "tiêu chuẩn" của Mac.

Hai trang có bố cục giống nhau: hình vuông lớn ở bên trái (chân dung chiến đấu của máy bay, hình đại diện nhân vật), tác phẩm ở bên phải (máy bay cộng với mẫu), tên (nhân vật cộng với tên đầy đủ), dòng nhãn, thanh giá trị và địa hình; dưới đây là các phần tương ứng của họ.

- **Đơn vị**: Nhãn vàng là giới hạn sửa đổi trên (+0x20, cấp 6–15, được chia sẻ bởi vũ khí), tiếp theo là loại chuyển động, kích thước, khả năng đặc biệt, lá chắn, khe thành phần gia cố (+0x19) và chi phí sửa chữa. Sáu thanh số chứa 10% hàng đầu trong tổng số (HP 22000, EN 300, khả năng di chuyển 10, khả năng di chuyển 130, áo giáp 2300, giới hạn 380). Bảng vũ khí bổ sung thêm "sửa đổi đầy đủ" (thay đổi thành giới hạn trên của sức tấn công) và "loại" (loại sửa đổi I-IV, vũ khí +0xE; mỗi lần tăng là một hàng của bảng thường trú `D_800CA590` và chi phí là bốn bảng u32 trong lớp phủ của màn hình sửa đổi). Bảng bên dưới liệt kê tổng sức tấn công được thêm vào và số tiền bỏ ra theo loại xuất hiện trên máy. Vũ khí được mở khóa bằng cách sửa đổi hoàn toàn (`D_801DC87C` 18 vật phẩm, đã có trong bảng vũ khí cơ thể, +0xF với bit đã mở khóa 0x04) được đánh dấu là "được mở khóa bằng cách sửa đổi hoàn toàn" và +0xF 0x02 được đánh dấu là "kỹ năng kết hợp".
- **Nhân vật**: Nhãn vàng là cấp độ của hành động thứ hai, tiếp theo là trại (trường thứ ba của bảng nhân vật gốc, 1 = xuất hiện với tư cách là kẻ thù), đồng phi công/yêu tinh (0x80/0x40 với bản ghi khả năng +0; hai loại sáu khả năng này và hành động thứ hai hiển thị "-" như trên trang khả năng ban đầu và điểm tinh thần như thường lệ). Sửa tình yêu (Bảng ROM `0x1012B4`) Mỗi ​​đối tác có một avatar nhỏ, được đánh dấu là "hai chiều" hoặc "một chiều": đối tác cũng có một dòng ám chỉ ngược lại người đó, được coi là hai chiều. Phiên bản gốc có 7 đường một chiều (Allenbi → Domon, Lixiu → Cerein, Emmary → Bright, Bicha → Ellu, Ellu → Jidu, Boss → Jun, Boss → Sayaka). Thanh giá trị chuyển từ màu trắng đến cấp 1 và màu lục lam đến cấp 99. Lệnh tinh thần là các thẻ (cấp độ thu được, mức tiêu thụ) và các kỹ năng đặc biệt được rút ra theo thang điểm từ cấp 1–99.
- Dữ liệu gốc không được hiển thị: danh mục chuyển (máy bay +0x12, tài xế +0xB), giá bán cơ bản (chỉ có 9 máy sản xuất hàng loạt có sẵn để bán, bảng ROM `0x109030`), không được hiển thị theo quyết định của người dùng.

## Quy tắc bao gồm

- Phân nhóm theo công trình, xem ở trên.
- Phần giữ chỗ có tên trống, `???` hoặc số thuần túy sẽ không được chấp nhận.
- Các mục tiếp theo có cùng tên và bản ghi giống nhau sẽ bị loại bỏ (so sánh bản ghi 36 byte và số vũ khí của máy; so sánh khả năng, ngưỡng và bản ghi tinh thần của nhân vật); giữ nguyên tên nhưng khác giá trị và thêm "(2)" và "(3)" bắt đầu từ cái thứ hai trong cùng một tác phẩm (các ký tự có cùng tên ở các tác phẩm khác nhau, chẳng hạn như hai "kiệt tác" sẽ không được đánh số). ROM hiện tại: 353 đơn vị và 293 ký tự.
- Những nhân vật không có bản ghi khả năng (được ánh xạ là −1) chỉ hiển thị hình đại diện và tên của họ, kèm theo ghi chú "Nhân vật không chiến đấu".
- Giá trị là giá trị cơ bản: không bao gồm các sửa đổi, phần nâng cao, ảnh hưởng về tinh thần và thể chất. Giá trị ngưỡng của ký tự 284 (クェス của chúng tôi) được đọc vào bảng linh hồn theo phương pháp đọc thực tế của trò chơi và trang được hiển thị theo trò chơi.

## Hoạt động

| Đầu vào | Chức năng |
| --- | --- |
| ↑↓ / Phím chéo lên xuống (nhấn và giữ để bật) | Chọn một mục; nhấn lên mục đầu tiên để quay lại tab |
| ←→ / Phím chéo trái và phải | Chuyển đến mục đầu tiên của tác phẩm tiếp theo; ← Khi đang làm việc, quay lại mục đầu tiên của tác phẩm này, sau đó nhấn để chuyển sang tác phẩm trước; Trên tab trang, cắt trang |
| C lên/xuống (Nút xoay bên phải, I/K mặc định trên bàn phím), con lăn chuột | Cuộn chi tiết (nhấn và giữ tay cầm để cuộn liên tục) |
| Q／E／L1／R1 | Đơn vị ↔ Ký tự |
| Chuột | Bấm vào các mục, bấm vào tab, cuộn danh sách và chi tiết bằng con lăn |
| Esc／X／B | Đóng |

Lớp dưới cùng của Thư viện và Đánh giá trận chiến mờ đục và tiêu đề không hiển thị bên dưới; khi bất kỳ trang nào (Thư viện, MOD, Cài đặt) trên khung cửa sổ cài đặt mở, `battle_viewer::hold_title` đặt hai số lần chờ của tiêu đề trên mỗi khung hình (`D_801CC390` thành 180 khung hình để mở bản demo, `D_801CC3A4` thành 0x385 Khung quay lại ô mở đầu) sẽ bị xóa và tiêu đề vẫn giữ nguyên và bản demo hoặc ô mở đầu sẽ không được mở ở cuối trang (thử nghiệm thực tế trên 2026-10-04: Trước khi sửa đổi, tiêu đề đã vào cốt truyện mở đầu trong khoảng 55 giây sau khi mở Thư viện và nó vẫn ở trạng thái chính 2 sau 65 giây).

Mỗi trang trong số hai trang sẽ ghi nhớ vị trí bạn đã chọn; chuyển đổi ngôn ngữ và Bản gốc/HD sẽ xây dựng lại trang. Chi tiết sau lựa chọn được cập nhật cục bộ bằng `SetInnerRML` mà không cần xây dựng lại toàn bộ cửa sổ. Giao diện gỡ lỗi: `ui.click --id library-open`, `lib-tab:0|1`, `lib-item:N`.

## mã

- `src/host/library.{hpp,cpp}`: Phân tích cú pháp và sao chép ROM, lưu vào bộ đệm bằng ngôn ngữ đọc, gọi chuỗi cửa sổ.
- `src/native/ui/frontend.cpp`: Nút góc tiêu đề (`home_sync`), thiết lập mục nhập trang chung, `library_panel`/`library_select`/`library_move`; được treo trên `settings_open` của cửa sổ cài đặt, do đó việc tiếp quản đầu vào giống như trình quản lý MOD.
- Bài dự thi: `library_*` trong tổng số `content/locales/*.json`, đã đăng ký `UI_KEYS`.