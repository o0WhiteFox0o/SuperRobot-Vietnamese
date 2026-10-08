> **Ngôn ngữ / Language:** [Tiếng Việt](touch-controls.vi.md) · [English](touch-controls.en.md) · [中文](touch-controls.md)

# Thao tác trên màn hình cảm ứng của điện thoại di động (được thiết kế theo hiện trường)

2026-10-03. Cách sử dụng điện thoại Android không cần bộ điều khiển. Phiên bản trước là bộ điều khiển ảo cố định (`src/host/touch_pad.hpp`, 1c55cd9 chính) và tất cả các màn hình đều hiển thị cùng một bộ phím N64. Phiên bản này hiển thị các nút có tên chức năng theo cảnh. Các phím vẫn là phím N64 và phím máy chủ ở cấp độ thấp nhất nên không cần phải thay đổi trò chơi, trang của chúng tôi hoặc các lời nhắc phím.

## 1. Mục tiêu do người dùng đặt ra

- **Giống như game MOBA trên di động:** Không có phím điều hướng cố định ở bên trái. Bất cứ khi nào bạn nhấn ngón tay vào khu vực bên trái, tâm của phím điều hướng sẽ ở nơi bạn muốn, chỉ cần kéo nó.
- **Giảm thiểu số lượng nút:** Mỗi cảnh chỉ hiển thị các nút được sử dụng trong cảnh này.
- **Hiển thị tên chức năng:** Các nút ghi "OK", "Tua đi nhanh" và "Đơn vị tiếp theo" thay vì A, R2, R1. Ngôn ngữ văn bản và trò chơi (tiếng Trung, tiếng Nhật, tiếng Anh).
- **Không phân chia:** Các trang riêng của chúng tôi (xác nhận trước chiến tranh, chuẩn bị, v.v.) ít nhất phải giữ nguyên hướng "OK" và "Quay lại". Chúng ta không thể chỉ vào trang và chỉ có những cú nhấp chuột giữa.

## 2. Bố cục khung

Tất cả các cảnh đều có chung một khung và cảnh chỉ xác định những gì được đặt trong mỗi vị trí và liệu nó có được hiển thị hay không. Vị trí cố định nhưng lời nói sẽ thay đổi.

| Khe | Vị trí | Kích thước | Mục đích |
| --- | --- | --- | --- |
| Khu vực định hướng | Màn hình game: Toàn bộ cạnh trái rộng khoảng 42%, phía dưới thanh cạnh trên. Trang của chúng tôi: góc dưới bên trái có diện tích khoảng 34 mm vuông | rocker xuất hiện ở nơi bị ép, bán kính khoảng 10 mm, vùng chết 2,5 mm | bốn hướng. Khi không chạm vào, cần điều khiển sáng sẽ hiển thị ở góc dưới bên trái, cho biết có sẵn |
| Chìa khóa chính | Góc dưới bên phải, chính giữa cách bên phải 12 mm và cách đáy 14 mm | Đường kính khoảng 16 mm | Hành động "Xác nhận" trong cảnh này |
| Khóa phụ 1 | Ở bên trái phím chính, 180° trên cung | Đường kính khoảng 11 mm | Hành động "Trở về", luôn ở đây |
| Phím phụ 2, 3 | Phím chính phía trên bên trái 135°, hướng thẳng lên 90° | Đường kính khoảng 9 mm | Hai hành động phổ biến trong cảnh này (trước/tiếp theo, tua đi nhanh, v.v.) |
| Phím nhỏ phía trên | Một thanh ở trên cùng, hai dấu cách ở phía trên bên trái và hai dấu cách ở phía trên bên phải | Khoảng 12×5,5 mm | Hành động ít được sử dụng; khoảng trống đầu tiên ở phía trên bên trái luôn là "Cài đặt" |
| Bấm vào màn hình | Các màn hình ngoài khu vực định hướng và nút bấm | Toàn màn hình | Chỉ hợp lệ trong hội thoại và bất kỳ cửa sổ phím nào, bằng khóa chính |

Quy tắc:

- Các slot không hiển thị không chiếm diện tích cảm ứng. Khi ngón tay của bạn rơi vào đó, đó là "màn hình nhấp chuột" hoặc khu vực định hướng.
- Trong cùng một cảnh, một hành động chỉ xuất hiện một lần.
- Cảm giác bấm theo cách thực hiện hiện tại: nhấn bằng nhiều ngón tay cùng lúc; kéo ngón tay vào vùng hướng để đổi hướng; trượt từ nút này sang nút khác để chuyển đổi; nhấp và giữ ít nhất 80 mili giây.
- Toàn bộ bộ này bị ẩn khi sử dụng bộ điều khiển vật lý hoặc bàn phím; nó xuất hiện khi bạn chạm vào màn hình.

## 3. Bảng cảnh

Cột “Nhận dạng” là căn cứ được người dẫn chương trình dùng để phán đoán hiện trường. Tất cả các địa chỉ đều ở dạng RDRAM và được luồng trò chơi đọc ra trong mỗi khung hình và được xuất bản lên luồng giao diện (Phần 4). Cột "N64" là phím mà nút thực sự phát ra.

| Cảnh | Công nhận | Hướng | Khóa chính | Khóa phụ 1 | Khóa phụ 2, 3 | Cạnh trên | Bấm vào màn hình |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Logo khởi động, demo mở đầu, NHẤN BẮT ĐẦU | Chế độ `8015DA02` = 1, 7, `title_major` không phải là 3 | Không có | Bắt đầu (BẮT ĐẦU) | Không có | Không có | Cài đặt | Bắt đầu |
| Menu vòng tiêu đề | `title_major` = 3 | Xoay vòng sang trái và phải (nhấn và giữ) | Được rồi (BẮT ĐẦU) | Không có | Không có | Cài đặt; phóng to nút "MOD" và "Sách ảnh" ở góc, nhấp trực tiếp | Không có |
| Trang văn bản mở đầu | Lớp phủ tiêu đề Trang mở đầu (nhóm `801C9EA8`) | Không có | Trang tiếp theo (A) | Không có | Bỏ qua (R1+BẮT ĐẦU) | Cài đặt | Trang tiếp theo |
| Đối thoại (cốt truyện, bản đồ thế giới, tạm dừng, chiến tuyến) | Trình đọc hội thoại gốc có hộp thoại và đang chờ lật trang | Không có (vùng định hướng vẫn có thể dùng để nhìn qua lại mà không cần vẽ cần điều khiển) | Câu tiếp theo (A) | Không có | Chuyển tiếp nhanh (nhấn và giữ R2), tự động (L2) | Cài đặt, bỏ qua (R1+BẮT ĐẦU, chỉ hiển thị trong sơ đồ), xem lại (L1) | Câu tiếp theo |
| Chọn chi (script `3D44`) | Chọn cửa sổ nhánh mở ra (lệnh hiện tại của công cụ tập lệnh `3D44`) | Chọn lên và xuống | Được rồi (A) | Không có | Không có | Cài đặt | Không có |
| Bản đồ chiến thuật · Nhàn rỗi | Chế độ mang tính chiến thuật, trạng thái chính `0x80172EB0` = 5 (6 khi di chuyển con trỏ) | Di chuyển con trỏ; kéo xuống dưới để tăng tốc trong 1 giây (C←) | Lựa chọn (A) | Thông tin đơn vị (B) | Đơn vị trước (L1), đơn vị tiếp theo (R1) | Cài đặt, kẻ thù trước (L2), kẻ thù tiếp theo (R2) | Không có |
| Menu đơn vị, menu đã di chuyển, menu hành động, menu không gian | Trạng thái chính 8, 0x3A, 0xD, 0x16 | Lựa chọn lên xuống | Được rồi (A) | Trở về (B) | Không có | Cài đặt | Không có |
| Chọn điểm di chuyển | Trạng thái chính 0xC, trạng thái phụ 0 | Di chuyển con trỏ | Di chuyển đến đây (A) | Hủy bỏ (B) | Xa nhất (giữ R1) | Cài đặt | Không có |
| Danh sách vũ khí, mục tiêu, tinh thần | Họ 0x17 trạng thái chính, 0x19 | Lựa chọn lên xuống | Được rồi (A) | Trở về (B) | Mục tiêu trước (L1), mục tiêu tiếp theo (R1), chỉ khi chọn mục tiêu | Cài đặt | Không có |
| Cửa sổ thông tin, trang năng lực | Trạng thái chính 0x1B, 0x22, 0x2E–0x37, 0x3C, trang khả năng | Lật trang, liệt kê | Được rồi (A) | Đóng (B) | Đơn vị trước (L1), đơn vị tiếp theo (R1) | Cài đặt | Không có |
| Danh sách lưới (lựa chọn xuất kích, v.v.) | `801EDBE0` Trạng thái gia đình | Chọn lưới | Xác nhận (A) | Trở về (B) | Trang trước (L1), trang tiếp theo (R1) | Cài đặt | Không có |
| Trận chiến | Chế độ 2 | Không có | Không có | Không có | Bỏ Qua Chương Trình (R2) | Cài đặt | Không có |
| Màn hình kết quả, lời nhắc đánh bại, cửa sổ phím bất kỳ | Kết quả `8020DA08`, đánh bại `801DF53C` Trạng thái | Không có | Tiếp tục (A) | Không có | Không có | Cài đặt | Tiếp tục |
| Kết thúc | Chế độ 0x20 | Không có | Tiếp tục (A) | Không có | Không có | Không có | Tiếp tục |
| Xác nhận trước trận chiến (thay đổi bố cục màn hình cảm ứng khi chạm vào, xem bên dưới) | Yêu cầu trang xác nhận trước trận `visible`, không chọn thần | Khu vực hướng cố định phía dưới bên trái: chuyển sang trái và phải để phản công/né tránh/phòng thủ | Bắt đầu chiến đấu (lệnh trang) | Trở về (B) | Chọn vũ khí, tinh thần (trang lệnh) | Cài đặt, bật/tắt hoạt ảnh | Chọn trực tiếp một trong ba tùy chọn |
| Chọn tinh thần | `spirit_menu` trên trang xác nhận trước chiến tranh | Khu vực hướng cố định phía dưới bên trái | Xác nhận (A) | Trở về (B) | Không có | Cài đặt | Điểm trực tiếp vào danh sách tinh thần |
| Trang của chúng tôi: Chuẩn bị từng trang, trang lưu trữ, trang con tiêu đề, trang tên | Yêu cầu cho mỗi trang `visible` | Khu vực hướng cố định phía dưới bên trái | Được rồi (A) | Trở về (B) | Khi trang hỗ trợ: trang trước (L1), trang tiếp theo (R1) | Cài đặt | Nhấp trực tiếp vào nút riêng của trang |
| Cửa sổ cài đặt, hình ảnh minh họa, quản lý MOD | `settings_open`, `library_open` | Không có | Không có | Không có | Không có | Không có | Nhấp vào tất cả trực tiếp; trả lại phím để đóng |
| Màn hình không được nhận dạng | Không có điều nào ở trên | Khu vực định hướng hoàn chỉnh | Được rồi (A) | Trở về (B) | L1, R1 | Cài đặt, BẮT ĐẦU, L2, R2 | Không có |

**Bố cục màn hình cảm ứng của trang xác nhận trước chiến tranh** (được người dùng chọn vào ngày 2026-10-03, chỉ khi các nút trên màn hình cảm ứng được hiển thị, ba kiểu giao diện trước chiến tranh được thay thế bằng phiên bản này): Hàng nút dưới cùng và lời nhắc phím không được hiển thị và chức năng được trao cho nhóm nút bên phải (màu xanh lá cây "Bắt đầu chiến đấu" ở vị trí phím chính); hai thanh thông tin thí điểm bên dưới được chuyển vào giữa, phía dưới bên trái dành cho khu vực định hướng và phía dưới bên phải dành cho nhóm nút; toàn bộ trang được di chuyển xuống khoảng 8 mm, đặt "Cài đặt" và "Bật/Tắt hoạt ảnh" ở cạnh trên. Khi chuyển từ né tránh hoặc phòng thủ sang phản công, hãy làm theo quy trình ban đầu và tiến tới danh sách vũ khí ban đầu để chọn vũ khí phản công.

Mô tả:

- Trên **trang xác nhận trước trận chiến**, "Bắt đầu trận chiến", "Chọn vũ khí", "Tinh thần" và "Hoạt hình chiến đấu" ban đầu là các nút trên trang, hãy nhấp trực tiếp vào chúng; các nút ảo chỉ giữ lại hướng, xác nhận và quay lại, đáp ứng “không phân tách”.
- **Đối thoại** Hành động thường được sử dụng nhất là lật trang, vì vậy hãy nhấp vào bất kỳ vị trí nào trên màn hình để lật trang; vùng định hướng vẫn chấp nhận kéo để xem nhưng không rút joystick ra để tránh bị tắc.
- **Bản đồ chiến thuật·Nhàn rỗi** là cảnh có nhiều nút nhất (cộng thêm 5 cài đặt). L2 và R2 (đổi kẻ thù) được đặt ở phía trên vì chúng ít được sử dụng.
- **Màn hình không được nhận dạng** trả về một bộ hoàn chỉnh để đảm bảo không thiếu phím nào trên bất kỳ màn hình nào. Trong quá trình thực hiện, hãy ghi lại mọi cảnh thuộc dòng này vào nhật ký, sau đó thêm từng cảnh vào bảng.
- Phím quay lại và cử chỉ quay lại bằng phím phụ 1 (B) trong tất cả các cảnh; đóng cửa sổ trong cửa sổ cài đặt, sách minh họa và quản lý MOD.

## 4. Nhận dạng cảnh

Chuỗi giao diện không đọc bộ nhớ trò chơi (quy tắc của `frontend.cpp`), do đó, mô-đun chuỗi trò chơi mới được thêm vào. Mỗi khung trò chơi đọc các giá trị sau, tính toán số cảnh và một số cờ rồi xuất bản nó với trọng lượng nguyên tử:

| Cơ sở | Nguồn | Đã xác nhận |
| --- | --- | --- |
| Chế độ cấp cao nhất | `8015DA02` (`800801A4` phân phối chỉ số dưới bảng, xem Phần 3 của tài liệu khóa gốc) | Tĩnh |
| Giai đoạn tiêu đề | `intro::title_major()` | Máy thực tế |
| Chiến thuật trạng thái chính, trạng thái phụ | `0x80172EB0``+0`, `+2` | Máy thực tế (bảng trạng thái giao diện người dùng chiến thuật) |
| Đối thoại chờ lật trang | Khung hiện tại của trình đọc hội thoại gốc (`native_dialogue.cpp`) | Máy thực tế |
| Chọn chi | Lệnh hiện tại của công cụ tập lệnh (`8009EFDC` đã thăm dò vm), `3D44` | Chờ máy thật |
| Trang mở đầu | `intro::title_major()` là 13 (phần mở đầu chung và phần mở đầu của mỗi tuyến đường, được thêm sau 0.4.0) | Chờ máy thật |
| Màn hình kết quả, nhắc nhở đánh bại | Móc của hàm tương ứng hoặc chỉ số bảng trạng thái của nó | Chờ máy thật |
| Trang của chúng tôi | Bản thân chuỗi giao diện có `visible` được mỗi trang yêu cầu | Máy thực tế |

Kết quả nhận dạng chỉ xác định nút nào được hiển thị. Các nút vẫn phát ra phím N64 nên dù nhận diện sai cũng chỉ là thiếu nút hoặc nhãn sai mà game sẽ không nhận được thao tác sai.

## 5. Văn bản

Mỗi tên hàm là một mục nhập giao diện, có sẵn bằng ba ngôn ngữ và được đăng ký bằng `UI_KEYS` (`src/srw64_native/profile.py`). Cố gắng giới hạn số lượng ký tự tiếng Trung ở mức bốn ký tự để nút tròn có đường kính 12 mm có thể vừa vặn; nếu không vừa, kích thước phông chữ sẽ tự động giảm theo chiều rộng. L1, R1, L2 và R2 chỉ được sử dụng cho những hình ảnh không được nhận dạng.

| Chìa khóa | Tiếng Trung giản thể | Tiếng Nhật | Tiếng Anh |
| --- | --- | --- | --- |
| `touch_settings` | Cài đặt | Cài đặt |
| `touch_ok` | được | Quyết định | được |
| `touch_back` | Trở về | 戻る | Quay lại |
| `touch_close` | Đóng | đóng じる | Đóng |
| `touch_start` | Bắt đầu | スタート | Bắt đầu |
| `touch_l1` | L1 | L1 | L1 |
| `touch_r1` | R1 | R1 | R1 |
| `touch_l2` | L2 | L2 | L2 |
| `touch_r2` | R2 | R2 | R2 |
| `touch_next_page` | Trang tiếp theo | 时ページ | Trang tiếp theo |
| `touch_prev_page` | Trang trước | 前ページ | Trang trước |
| `touch_skip` | Bỏ qua | スキップ | Bỏ qua |
| `touch_next_line` | Câu tiếp theo | Thời gian | Tiếp theo |
| `touch_fast` | Chuyển tiếp nhanh | Giao hàng sớm | Nhanh |
| `touch_auto` | Tự động | オート | Tự động |
| `touch_select` | Chọn | Chọn | Chọn |
| `touch_info` | Thông tin đơn vị | Tình báo | Thông tin |
| `touch_prev_unit` | Đơn vị trước | 前の丝方 | Đơn vị trước |
| `touch_next_unit` | Đơn vị tiếp theo | 时の丝方 | Đơn vị tiếp theo |
| `touch_prev_enemy` | Kẻ thù trước đây | Kẻ thù trước đây | Trước kẻ thù |
| `touch_next_enemy` | Kẻ thù tiếp theo | 下 kẻ thù | Kẻ thù tiếp theo |
| `touch_move_here` | Di chuyển đến đây | ここへ | Di chuyển đến đây |
| `touch_cancel` | Hủy bỏ | キャンセル | Hủy bỏ |
| `touch_farthest` | Xa nhất | Xa nhất | Xa nhất |
| `touch_prev_target` | Mục tiêu trước đó | Mục tiêu trước đó | Mục tiêu trước |
| `touch_next_target` | Mục tiêu tiếp theo | Mục tiêu thứ hai | Mục tiêu tiếp theo |
| `touch_skip_battle` | Bỏ qua cảnh | Hiệnスキップ | Bỏ qua cảnh |
| `touch_continue` | Tiếp tục | Lần | Tiếp tục |

Tiếng Nhật và tiếng Anh là những bản nháp đầu tiên, và tôi sẽ xem lại chúng theo quy tắc chọn tên riêng (tiếng Trung giản thể đại lục, tiếng Anh chính thức được ưu tiên).

## 6. Trình tự thực hiện

1. **Bộ xương:** Khu vực định hướng (bất cứ nơi nào trên màn hình trò chơi, góc dưới bên trái của trang của chúng tôi), phím chính cộng với cung phím phụ, phím nhỏ ở trên cùng, nhấp vào màn hình. Các cảnh được chia thành ba loại: trang của chúng tôi, thiết lập loại cửa sổ toàn màn hình cảm ứng này và các loại khác (một bộ hoàn chỉnh). Chấp nhận: Quá trình hiện tại (mở màn → danh hiệu → cấp độ nhỏ → trận chiến) chỉ có thể được hoàn thành bằng cách chạm vào.
2. **Lớp nhận dạng:** Mô-đun chuỗi trò chơi và số cảnh, cảnh hiện tại có thể được xem trong giao diện gỡ lỗi `status` để dễ kiểm tra.
3. **Truy cập theo từng cảnh:** Trước tiên hãy kết nối hội thoại và bản đồ chiến thuật (nhàn rỗi, menu, lựa chọn trên thiết bị di động), chiếm phần lớn thời gian của trò chơi; sau đó kết nối tiêu đề, hiệu suất chiến đấu, kết quả và bất kỳ cửa sổ chính nào; cuối cùng kết nối danh sách, cửa sổ thông tin và trang khả năng. Mỗi lần chọn cảnh, hãy sử dụng giao diện gỡ lỗi để vào và chụp ảnh màn hình để kiểm tra.
4. **Cuối cùng:** Điền vào từng cảnh không thể nhận dạng được từ nhật ký; xem qua các mục ba ngôn ngữ; phát một tập hoàn chỉnh trên Seeker (mở đầu → tập 1 → trận chiến → lưu), chỉ cần chạm.

### Tiến độ (2026-10-03)

- Đã hoàn thành bước 1 và 2; Bước 3 truy cập phần mở đầu, tiêu đề, hội thoại, bản đồ nhàn rỗi, menu đơn vị, lựa chọn điểm đến di chuyển, danh sách vũ khí và mục tiêu, cửa sổ thông tin, chương trình chiến đấu, kết thúc, cũng như trang của chúng tôi và cửa sổ màn hình cảm ứng đầy đủ.
- Người tìm kiếm đã xác minh khả năng nhận dạng và các nút trong máy thật: mở, tiêu đề, hội thoại (nhấp vào màn hình để lật trang), bản đồ nhàn rỗi, menu đơn vị, chọn điểm di chuyển, xác nhận trước trận chiến, hiệu suất chiến đấu ("bỏ qua màn trình diễn" trên phím chính). "Sách ảnh", "MOD" và "Cài đặt" ở góc của tiêu đề đã được thay đổi thành các nút cảm ứng ở trên cùng.
- Chưa nhặt: Chọn chi, danh sách lưới, kết quả và nhắc nhở đánh bại (nhấn tạm thời "Không nhận dạng" để hiển thị toàn bộ và chọn chi để hiển thị cùng với lời thoại). Danh sách vũ khí, mục tiêu và cửa sổ thông tin được kết nối theo bảng trạng thái, nhưng tôi chưa đến đó để kiểm tra trên máy thực tế.
- 2026-10-07 (sau khi phát hành 0.4.0): Trang mở đầu ban đầu nằm ở phần "Mở" và chỉ BẮT ĐẦU, không bỏ qua; nó đã được đổi thành tiêu đề giai đoạn 13 để xác định đây là trang mở đầu (trang tiếp theo + bỏ qua). Máy chủ cũng truyền lại `title_waiting`, NHẤN BẮT ĐẦU hiển thị lại hai nút trên cùng của sách minh họa và trình xem trận chiến.
- Khi tập lệnh đang chạy giữa hai đoạn hội thoại, trạng thái bản đồ cũng không hoạt động khi đọc và nút bản đồ sẽ hiển thị nhanh chóng; nó không ảnh hưởng đến hoạt động.

## 7.TBD

Đã xác định (người dùng 2026-10-03): Sẽ không có chuyển động lưới điểm nào được thực hiện trên bản đồ và con trỏ sẽ vẫn sử dụng vùng định hướng để thêm "Chọn" và "Thông tin đơn vị" (A, B).


- Có nên vẽ cần điều khiển ở vùng điều hướng trong đoạn hội thoại không? Kế hoạch hiện tại của tôi không phải là vẽ mà chỉ kéo và xem lại.
- Khi những cảnh không thể nhận biết được xếp thành một bộ hoàn chỉnh thì hình thức rất khác so với những cảnh khác; có nên thay đổi nó thành một nút "Thêm" nữa hay không, sau đó mở rộng nó để hiển thị các nút khác.