> **Ngôn ngữ / Language:** [Tiếng Việt](original-images.vi.md) · [English](original-images.en.md) · [中文](original-images.md)

# Trích xuất hình ảnh gốc và đánh dấu vũ khí

Cập nhật: 2026-09-11.

Trình duyệt dữ liệu thô hiện hiển thị hình ảnh thô cho các ký tự, đơn vị và bản đồ. Hình ảnh là PNG gốc được giải mã từ ROM cố định của Nhật Bản và được bao gồm trong tệp kê khai đầu ra cùng với các byte thô. Không có sửa đổi đối với đường dẫn kết xuất ROM hoặc thời gian chạy.

Xem [Hình ảnh chiến đấu](battle-graphics.md) để biết hình ảnh quy mô lớn về máy bay, các phần hoạt hình, hiệu ứng đặc biệt và đoạn cắt cảnh trong các cảnh chiến đấu; xuất khẩu được tổ chức theo tên máy bay/nhân vật cũng có ở đó.

## Phạm vi bảo hiểm và mục nhập

| Danh mục | Phạm vi liên quan | Hình ảnh hiện tại |
| --- | --- | --- |
| Nhân vật | 361 tên và danh tính | hình đại diện 96×96 hoặc 97×97; được giải mã bằng các bảng màu tương ứng, danh tính có thể chia sẻ hình ảnh. |
| Máy bay | 363 khung/hình thức máy bay | Biểu tượng bản đồ chiến thuật 16×16, sử dụng thống nhất bảng màu 1010 của chúng tôi; không phải là một bức tranh lớn cho hoạt hình chiến đấu. |
| Bản đồ | 158 bản ghi tài nguyên bản đồ | Hoàn thành sơ đồ cơ sở chiến trường tĩnh; giữ lại việc lật ô, ngoại trừ máy bay, lớp phủ phụ, thay đổi sự kiện và hiệu ứng thời gian chạy. |
| Cảnh/Kịch bản | 144 ô bản đồ vật lý, 142 ô tập lệnh | Sử dụng lại bản xem trước bản đồ ban đầu; không đại diện cho số cấp độ có thể chơi được cũng như không dự đoán những thay đổi bản đồ tiếp theo trong tập lệnh. |

Danh sách hiển thị hình thu nhỏ, hiển thị chi tiết hình ảnh và link tài nguyên nguồn, click vào ảnh để mở kích thước gốc PNG. "Bản đồ" đã được thăng cấp lên danh mục chính. 815 bản xem trước độc lập được loại bỏ trùng lặp và ghi vào `images/portrait/`, `images/unit-icon/`, `images/map/`; bản đồ cũng tạo ra hình thu nhỏ.

Phương pháp tạo vẫn là:

```sh
.venv/bin/python -B tools/content/extract_original.py \
  --snapshot build/recomp/gfx-probes/female-map-audio-1/latest-gfx-rdram.bin
```

`--snapshot` có thể được bỏ qua khi không cần đến hồ sơ quan sát lịch sử. Trích xuất hình ảnh không dựa vào ảnh chụp nhanh.

## Cơ sở để ràng buộc ký tự và nội dung

Các khóa byte mã và ràng buộc được đặt trong `images`, `evidence` của `config/data/original-jp-v1.json`.

- Ký tự: cư dân `8009C768..8009C7DC` đọc hai u16 lớn từ ROM `0x84220 + actor_id × 4`, đó là tài nguyên hình ảnh và tài nguyên bảng màu. Bạn không thể chỉ cần thêm một hằng số vào ID ký tự làm ID hình ảnh. Ví dụ: ký tự 28 → `33/333`, 162 → `166/466`, 165 → `169/469`. Các ràng buộc hình đại diện 361 độc lập với bản đồ chỉ số/tinh thần chỉ có 360 vị trí.
- Body: `load_000AB160:801C60A4..801C6180` Lấy body ID của bản ghi body đang chạy `+2`, kiểm tra VRAM `0x80218218`, tương ứng với bảng u16 của ROM `0x100D78`. Tham số bảng màu là `1010 + 阵营`. Hiện tại, 1010 được sử dụng thống nhất, được đánh dấu là màu phù hợp của chúng tôi. Ví dụ: phần thân 0 → 688, 36 → 718, 216 → 898, 362 → 1009.
- Loại tài nguyên hình đại diện là 15 hoặc 6 và theo sau tiêu đề 8 byte là chỉ mục CI8; loại biểu tượng cơ thể là 14, tiếp theo là chỉ số CI4, với mức nibble cao đầu tiên. Loại bảng màu là 3, u16 thứ hai là số byte trong bảng màu và sau tiêu đề là màu cuối lớn RGBA5551. Các bit trong suốt được bảo lưu; Mức màu 5 bit được ánh xạ thành 8 bit theo quy ước giải mã hình ảnh hiện có của dự án.

Mỗi mục `images[]` giữ lại đường dẫn tệp, kích thước, ID tài nguyên và giải nén SHA-256; các ký tự và nội dung cũng giữ lại địa chỉ ROM, byte gốc và bảng đầy đủ SHA-256 của bản ghi liên kết. Hình ảnh không được khớp dựa trên sự gần kề của tệp hoặc sự giống nhau về tên.

## Định dạng bố cục bản đồ

Ba u16 đầu tiên của bản ghi tài nguyên là bố cục, tập bản đồ và bảng màu. `801C6EFC` được chuyển vào chế độ 8 và trình kết xuất `800945D4` được chọn thông qua `80097C68`.

Tiêu đề 8 byte của bố cục là `(type=7, group_count, width, height)`. `width`, `height` có đơn vị 8 pixel; lưới ô 16×16 thực tế là `width/2 × height/2`. Lưới này được theo sau bởi một bản ghi địa hình bốn byte. Lô này giữ lại các byte ban đầu và không giải thích các thuộc tính địa hình.

Các nhóm vẽ bắt đầu ở `8 + width × height`, mỗi nhóm có 6 byte:

```text
u16 tile      图集索引
u16 count     放置次数
u16 offset    放置列表相对布局资源起点的偏移
```

Mỗi bản ghi vị trí cũng có sáu byte: `u16 flags, u16 x, u16 y`. Tọa độ nguồn atlas được tính theo trình kết xuất gốc:

```text
sx = (tile & 0x000F) * 8 + ((tile & 0x0300) >> 1)
sy = ((tile & 0x00F0) >> 1) + ((tile & 0x0C00) >> 3)
```

Lấy 16×16 pixel từ vị trí đó và vẽ theo bản ghi vị trí. `0x4000` lật theo chiều ngang, `0x8000` lật theo chiều dọc; một số bản đồ cũng chứa `0x2000`, đường dẫn vẽ này không đọc được, không cung cấp ngữ nghĩa bổ sung và các cờ hoàn chỉnh được để lại trong siêu dữ liệu xem trước.

Tất cả 158 bố cục, chứa tổng cộng 290.706 mục đã đặt, đã vượt qua giới hạn canvas, giới hạn bản đồ, không có vị trí trùng lặp, bao phủ toàn bộ lưới, tính liên tục của danh sách thả và kiểm tra giới hạn đuôi tài nguyên. Bản đồ 20 của Chương 1 của Phụ nữ sử dụng `6284/6228/6243`, tạo ra bản đồ cơ sở dạng lưới 448×512, 28×32; tài nguyên phụ trợ `6422/6429` vẫn còn trong bản ghi gốc và không được đưa vào bản đồ cơ sở này.

## Tên và thuộc tính vũ khí

Trang tích hợp ban đầu lặp lại toàn bộ chuỗi menu bên dưới tên vũ khí thuần túy, chẳng hạn như `格アイアンネットP`. Bây giờ nó xuất hiện dưới dạng:

| Tên vũ khí | Thuộc tính |
| --- | --- |
| アイアンネット | Lưới · P |

`格` dành cho chiến đấu, `射` dành cho bắn súng, `P` dành cho sử dụng trên thiết bị di động, `B` dành cho chùm tia và `MAP` dành cho vũ khí bản đồ. Trang này cung cấp các cột thuộc tính, màu sắc, mô tả di chuột và chú giải văn bản độc lập. Tên ban đầu, văn bản menu và TextKey của nó được giữ lại trong chi tiết bản ghi và nguồn.

Phân tích cú pháp yêu cầu "tiền tố + tên gốc + hậu tố thuộc tính được phép" hoàn toàn bằng chuỗi menu gốc; chữ P và B trong tên sẽ không bị cắt bớt. Một số tên thuần túy có MAP và menu chèn B trước MAP. Trong trường hợp này, MAP sẽ chỉ bị xóa khỏi tên hiển thị khi hai chuỗi khớp với nhau. Tất cả 1.329 hồ sơ vũ khí hiện tại đều khớp; định dạng không xác định giữ lại tên và hiển thị "Đánh dấu phân tích cú pháp đang chờ xử lý".

`weapon_traits.source` rõ ràng là `original-menu-text`. Đây là những dấu thuộc tính hiển thị trên giao diện gốc. Chúng không phải là lời giải thích về các bit giá trị ROM mới, cũng không thay thế việc kiểm tra khả năng sử dụng hoàn chỉnh về sức mạnh, đạn dược, hình thức, kỹ năng, v.v.

## Mã và xác minh

- Giải mã và tương quan: `src/srw64_native/original_images.py`.
- Đánh dấu vũ khí: `src/srw64_native/weapon_traits.py`.
- Trang web: `tools/data_viewer/web/images.js`, `weapons.js` và mô-đun hiển thị tệp.
- Đã thêm mô-đun SHA vào bản ghi trình tạo, tất cả PNG đều được bao gồm trong `manifest.json.files` và tất cả các tham chiếu tài nguyên đều sử dụng danh tính ổn định hiện có.
- `PYTHONDONTWRITEBYTECODE=1 make check`: Đã vượt qua 103 bài kiểm tra, đã vượt qua kiểm tra phụ thuộc. Chứa các bit trong suốt và thứ tự CI4, CI8, độ dài kém/chỉ số xấu, bốn lần lật, ngoài giới hạn/vị trí bản đồ trùng lặp, tất cả các ràng buộc hình ảnh thực tế và phạm vi bao phủ bản đồ hoàn chỉnh, bảo vệ tên vũ khí và tất cả các điểm đánh dấu phù hợp.

Nhật ký kiểm tra: `build/original-data-qa/check-images.log`; Nhật ký bản dựng: `build/original-data-qa/build-images.log`; Kiểm tra tham chiếu tệp, kích thước hình ảnh và tài nguyên: `build/original-data-qa/verification-images.json`. Kích thước của 7.725 tệp và khả năng giải mã thực tế của SHA-256, 972 PNG và 1.168 liên kết hình ảnh tệp đều vượt qua; số lượng bản sao hình ảnh gốc là 338 hình đại diện, 320 biểu tượng nội dung và 157 bản đồ.

Trình duyệt đã kiểm tra hình thu nhỏ/chi tiết/lưới và cột thuộc tính độc lập P của phần thân 0, hình đại diện và hồ sơ của nhân vật 28, bản đồ cơ sở hoàn chỉnh của bản đồ 20, hình ảnh được cập nhật đồng thời khi dòng tiếp theo được cắt thành bản đồ 21 và trang tập lệnh của cảnh 1 đã sử dụng lại bản đồ 20. Sau khi kiểm tra, quay lại phần thân 0 và giữ lại dịch vụ 59110 ban đầu. Phạm vi của vòng xác minh này là giải mã ROM tĩnh và trình duyệt dữ liệu, trò chơi chưa được khởi chạy.