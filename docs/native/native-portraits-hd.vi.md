> **Ngôn ngữ / Language:** [Tiếng Việt](native-portraits-hd.vi.md) · [English](native-portraits-hd.en.md) · [中文](native-portraits-hd.md)

# hình đại diện HD

24-09-2026. Tất cả các avatar nhân vật đã được tạo dưới dạng bậc thầy có độ phân giải cao, được cắt trong suốt và kết nối với trò chơi dưới dạng **toàn bộ hình ảnh**: mỗi avatar là một hình ảnh 768×768 và người chủ sẽ vẽ tất cả cùng một lúc ở vị trí mà avatar được vẽ trong trò chơi mà không thay thế họa tiết thành các khối nhỏ 32×32. Để biết phương pháp cắt bỏ và các vấn đề với phiên bản cũ, hãy xem [Hình ảnh gốc và độ phân giải cao](native-content-foundation.md#原图与高清图).

## Phạm vi

- Bảng ký tự `0x84220` gán một bộ (hình ảnh, bảng màu) cho mỗi bộ trong số 361 đặc điểm nhận dạng, tổng cộng có 338 bộ, bao gồm 300 hình ảnh khác nhau (Tài nguyên 9–308). Ngoài ra còn có 4 bức chân dung nhân vật chính 1308–1311, với bảng màu 1312–1315, được `save_page.cpp` sử dụng.
- Mỗi bức ảnh chỉ được tạo 1 lần theo bảng màu cơ bản:
- Bảng màu cơ bản là "ảnh số + 300", 294 trong số 300 ảnh như thế này;
- 259–264 6 hình ảnh này được ghép bằng các bảng màu lệch (559–564) trong bảng và bên trong, như trong bảng;
- Các bảng màu còn lại được coi là biến thể, xuất phát từ kết quả HD và không được tạo riêng:
- 609 là bảng màu bóng, chỉ có một màu xám đậm (41,41,41), được sử dụng trong 34 hình ảnh;
- Mặt phổ thông số 134 được mượn từ 4 bộ khác: 309, 313, 392 và 515.
- Bảng màu chỉ có 64 màu, độ trong suốt số 0; hình ảnh là CI8 96×96 (232 ảnh) hoặc 97×97 (68 ảnh).
- 29, 33, 166 và 169 đã được xem xét trong tập đầu tiên sẽ không được tạo lại. Lần này có tổng cộng 300 bức ảnh.

## Tạo

`prepare` của [`portrait_batch.py`](../../tools/hd_ai/portrait_batch.py) được giải mã từ ROM, đóng băng dữ liệu đầu vào và các từ nhắc nhở; `run` gửi yêu cầu theo trình tự và lớp dưới cùng là `run_benchmark.run_one` (phí dành riêng, không tự động lặp lại POST).

- Model `qwen-image-3.0`, đầu ra 20482, hạt giống 640903, giống với hình đại diện đơn đã được đánh giá.
- Mỗi yêu cầu là một câu đố 2×2: nền xám (100.100.112), 16 pixel gốc trong lưới và đầu vào được phóng to 6 lần bởi hàng xóm gần nhất. Nhóm theo kích thước (nhóm riêng 97 px), sắp xếp theo số tài nguyên trong cùng kích thước, các ký tự của cùng một tác phẩm hầu hết ở cùng nhau.
- Tổng cộng 15,0 nhân dân tệ cho 75 yêu cầu (giá công khai ước tính, giá mỗi sản phẩm). `400 InvalidParameter` đã được gửi 12 lần trên đường đi, tất cả đều được trả lại trong vòng 2 giây mà không mất phí và quá trình gửi lại đã thành công. Các bản ghi bị từ chối sẽ được chuyển đến `rejected/` để lưu giữ.
- Khoảng 819 px mỗi ô, lớn hơn 768 px của bản gốc 8x. 3×3 chỉ có khoảng 560 px mỗi ô vuông nên đừng sử dụng nó.

Đầu tiên, chúng tôi thực hiện thử nghiệm so sánh bằng cách sử dụng 4 hình đại diện được đánh giá (`grid-test-1`):
- Sau khi giảm nền xám 2×2 về kích thước ban đầu, chênh lệch so với ảnh gốc là 8,1/9,0/9,8/6,7 và tờ rơi được xét duyệt là 14,8/10,4/10,1/5,9;
- Nền màu xanh lục đồng nhất (0,255,0) là màu xa nhất so với màu của nhân vật, nhưng mô hình sẽ phóng to từng lưới và lấp đầy khoảng trống nên không cần phải key nền bằng màu đồng nhất.

## Căn chỉnh và cắt bỏ

Mô hình xử lý từng ô một cách khác nhau: phóng đại 3–10%, dịch tối đa 7 pixel gốc và vát góc cho một số ô (số 14 là 5 pixel gốc ở trên và dưới). Vì vậy, `compose` đăng ký theo từng khung:

1. Tìm độ dịch chuyển của toàn bộ lưới ở độ phân giải một nửa;
2. Xung quanh sự dịch chuyển này, sử dụng cửa sổ 32 px để khớp từng khối và hình vuông nhỏ nhất phù hợp với phép biến đổi affine hoàn chỉnh (6 tham số);
3. Theo sự chuyển đổi của lưới này, 8 lần bản gốc được lấy mẫu lại từ toàn bộ đầu ra và nội dung tràn vào lưới cũng có thể được truy xuất;
4. Để lại cho [`portrait_matte.py`](../../tools/hd_ai/portrait_matte.py) để đăng ký và cắt bỏ.

Phần dư đăng ký chính xác từ 3–5 px (pixel thời gian chạy, 4 px bằng 1 pixel gốc) được đánh dấu là "biến dạng cục bộ" để xem xét và những phần vượt quá 5 px sẽ bị từ chối. Cạnh cắt của khung ảnh chỉ kiểm tra vị trí cách vùng trong suốt của ảnh gốc hơn 2 pixel gốc và vị trí gần hơn được coi là đường viền nổi.

## Kết quả

- Toàn bộ 300 ảnh được cắt ra, IoU trung bình của các đường viền là 0,991, thấp nhất là 0,935 (1310 gai). Chênh lệch so với ảnh gốc sau khi thu nhỏ về kích thước ban đầu, trung vị là 8,8 và tối đa là 17,5.
- Sau khi mô phỏng khuếch đại song tuyến tính không nhân trước, các pixel có độ lệch biên vượt quá 16 mức: 292 ảnh có 0, 8 ảnh có 1–87, tất cả đều nằm trên vạch tối 1 pixel ở cuối ảnh 97 px.
- Tôi đã đọc thủ công từng trang một và không có gì cần phải vẽ lại.
- Ở bức số 14, tôi từng nghĩ rằng mình vẽ một cái miệng khép thay vì một cái miệng mở, nhưng bức tranh gốc ban đầu vẽ một cái miệng đang mở nên tôi giữ lại phiên bản đầu tiên. Phiên bản được vẽ lại bằng cách nhấn Shut Up (`redo-1`) chưa được sử dụng.
- 196, 200, 1310 được đánh dấu là biến dạng cục bộ và không có vấn đề gì khi xem hình ảnh.
- Các ảnh đánh giá có dạng `assets/hd-ai/portrait-batch/full-1/review/page-01.png`–`page-15.png`, 20 ảnh/trang, các ảnh gốc đặt cạnh HD và nền là nền xanh của hộp thoại. Được báo cáo là `report.json` trong cùng thư mục.

**Các khoảng trống xung quanh khung có màu xám. ** Khi mô hình vẽ một câu đố, nó thường dừng lại ở một vị trí cách mép lưới một hoặc hai pixel gốc, do đó cạnh mà khung hình bị cắt sẽ để lại một khoảng trống màu xám giữa các lưới (130 trên 300 hình ảnh). Khi cắt hình ảnh, hãy tìm tối đa 3 pixel gốc ở vị trí mờ của ảnh gốc trên mép khung: nếu chỉ có màu xám nền ở giữa (cộng với phần chuyển tiếp lên đến 3 pixel), hãy mở rộng màu đồng nhất đầu tiên ra cạnh; quần áo màu xám ban đầu ở đó. Sau khi xử lý chỉ còn lại 6 bức ảnh còn hơn 10%. Các hình ảnh đều có nội dung màu xám như bảng mạch và áo giáp màu xám.

## Truy cập trò chơi

### Cách vẽ avatar trong game

Tất cả hình đại diện được vẽ ở Chế độ Sprite 7. Một số chức năng tải đọc bảng ký tự `0x84220` xây dựng các họa tiết như sau: hội thoại `8008F970` và `801C6350`, `801CB4D0`, `801CD718`, `801C3280`, `801C8D74` trong các lớp phủ như trận chiến, bản đồ chiến thuật, sơ hở, v.v. Hình thức gọi là `80098158(槽, 0, 7, 0x8D, …, 图像, 调色板, 2)` và chức năng vẽ là `800964E4`. Kết quả đọc tĩnh:

- Trước tiên hãy thêm `SETTIMG` (`FD10`, RGBA16) vào `LoadTLUT` để tải bảng màu 64 màu.
- Sử dụng thêm hai vòng lặp không đổi (`y`, `x` lấy 0/32/64) để vẽ các khối 3×3. Mỗi khối có kích thước `SETTIMG` (`FD48`, CI8, tiêu đề hình ảnh chụp chiều rộng), `LoadTile` 32×32, `SETTILESIZE`, `TEXRECT`. **Hình 97 px chỉ vẽ 96×96 phía trên bên trái, hàng thứ 97 và cột thứ 97 không bao giờ được vẽ. **
- `E3000C00 / 0` tắt hiệu chỉnh phối cảnh kết cấu; `E3001001 / 8000` đặt TLUT thành RGBA16. Phương pháp lọc không được đặt trong chức năng này.
- Chuyển cờ ở bản ghi con +0x14. Khi lật, chữ S của mỗi khối bắt đầu từ 32 và được vẽ bằng cách phản chiếu ô và nội dung kết cấu không thay đổi.
- Sprite được ghi trong `800FFAAC + 槽×0xC4 + 子×0x30`, +0xC/+0xE lưu trữ **xử lý tài nguyên** (số thập phân được đo thực tế như 17, 18, 19 và 20), không phải số tài nguyên ROM.

### Thay thế toàn bộ trang tính

[`native_portrait.cpp`](../../src/host/native_portrait.cpp) Thực hiện theo phương pháp bản đồ chiến thuật (`native_map.cpp`):

1. `generate_cpu.py` Đổi tên `800964E4` thành `srw64_original_portrait_draw`, bọc `game_hooks.cpp` một lớp và lưu ý phạm vi danh sách hiển thị được viết lần này.
2. Xác định hình đại diện trên chuỗi trò chơi: Tay cầm không đáng tin cậy nên hãy tính trực tiếp tóm tắt FNV-1a 64 cho pixel được trỏ bởi `FD48` (96² hoặc 97² byte) và bảng được trỏ bởi `FD10` (128 byte) và sử dụng (pixel, bảng màu) để tra cứu danh sách. Bảng màu cơ bản tìm thấy hình ảnh màu; bảng màu hình bóng 609 tìm thấy hình ảnh tương tự và thay vào đó sử dụng (41,41,41) để tô màu. Có một cặp ảnh có cùng pixel nhưng có bảng màu khác nhau nên phải sử dụng key cho cả hai.
3. Chỉ viết lại nếu có 9 hình chữ nhật có tổng kích thước chính xác là 96×96 và không được chia tỷ lệ: hình chữ nhật cuối cùng được đổi thành thẻ che toàn bộ hình đại diện, `SETTILESIZE` ở phía trước được đổi thành thẻ G_NOOP được đánh số và 8 hình chữ nhật còn lại để trống. Trong các trường hợp khác, giữ nguyên bản vẽ gốc.
4. RT64 nhận dạng nhãn khi xây dựng bản vẽ, gọi lệnh gọi lại máy chủ ở cùng vị trí trình tự bản vẽ và vẽ một hình chữ nhật thông qua Plume (`src/host/shaders/HdPortrait*.hlsl`):
- Kết cấu được nhân trước alpha, có mipmap, lấy mẫu tuyến tính;
- Phương pháp trộn One/OneMinusSrcAlpha;
- Hoán đổi tia UV sang trái và phải khi lật.
5. Kết cấu được giải mã trong lần xuất hiện đầu tiên (~10 ms) và mipmap được tạo. Sau khi lưu trữ hơn 64 ảnh, những ảnh không được sử dụng trong 20 giây sẽ bị loại bỏ.

Ở chế độ hình ảnh gốc (F6), không có thao tác viết lại nào được thực hiện và trò chơi vẫn được vẽ như cũ. Đường dẫn này đi qua Plume giống như các lớp HD khác và có sẵn trong cả Metal và Vulkan (Vulkan đã được thử nghiệm với MoltenVK trên Mac và Steam Deck thực tế sẽ được thử nghiệm, xem [Cổng ba nền tảng](../design/three-platform-port.md)).

### Tài nguyên

- [`build_portrait_images.py`](../../tools/hd_ai/build_portrait_images.py) Cắt phần trên bên trái 768×768 từ bản cái 8x (bản cái 96 px là 768, 97 px là 776), xuất ra `assets/hd-ai/portrait-batch/whole-v1/portrait-<图号>.png`, tổng cộng 304 trang, 183 MB.
- Đồng thời tạo `portraits.json`, ghi lại SHA-256, tóm tắt pixel và tóm tắt bảng màu của từng hình ảnh, cũng như tóm tắt màu và bảng màu bóng.
- `--bind` Thêm phần `portraits` vào [`stage1-hd.json`](../../content/art/stage1-hd.json) và xóa các mục nhập lát hình đại diện ban đầu, chỉ để lại 70 bản thay thế bản đồ thế giới và đường viền hội thoại.
- `compile_art` Sau khi xác minh tóm tắt, sao chép biểu đồ vào thư mục đang chạy `art/portraits/`, viết `srw64-portraits-hd.json` và máy chủ sẽ đọc từ đây.
- Bốn bảng màu mà số 134 mượn đều bị lộn xộn, đáng lẽ chúng phải là những mục giữ chỗ không được sử dụng. Những hình ảnh gốc nên được giữ lại.

### Máy thực tế (24/09/2026, chế độ HD)

- Trong trận chiến demo mở đầu, hình đại diện của Ryoma ở chế độ full HD.
- Ở cấp độ nhỏ của Tập 8, hình đại diện đối thoại của Bioti, Jia'er, Wan Zhang, Garrison và Lijia đều ở dạng HD. Khi sử dụng hội thoại khung đôi, khung trên và khung dưới sẽ được thay thế.
- F6 có thể chuyển đổi qua lại giữa ảnh HD và ảnh gốc.
- Số lần thoát (`hd-portrait-summary.json`):
- 6977 bản vẽ avatar được viết lại;
- Nhận dạng nội dung không bị lỗi một lần;
- RT64 vẽ hai mục tiêu trên mỗi khung hình, do đó bản vẽ gốc có số lần viết lại gấp đôi;
- Tổng cộng 22 hình ảnh được giải mã.
- 713 bản vẽ khác được giữ nguyên, tất cả đều có "độ rộng kết cấu 3": không có hình đại diện của nhóm nhân vật chính được khởi tạo (アーク, Lu, Era, ký tự 25-32) ở cấp độ nhỏ và chúng cũng bị cắt xén ở chế độ hình ảnh gốc, không liên quan gì đến HD.

### Trang gốc

Các trang do RmlUi tiếp quản cũng sử dụng bộ hình đại diện HD này: xác nhận trước trận chiến, のりかえ, kiểm tra khả năng, データセーブ, リンク và trang tên.

- Khi chuẩn bị chạy cấu hình, `assets.portrait_lookup` tìm toàn bộ avatar theo (hình ảnh, bảng màu):
- Bảng màu cơ bản sử dụng trực tiếp các hình ảnh trong thư mục biên dịch;
- Bảng màu Silhouette 609 được tô màu (41,41,41) theo ảnh gốc Alpha. Mỗi hình ảnh chỉ được tạo một lần và được đặt trong thư mục đang chạy `portraits/`;
- Các bảng màu khác (4 bộ mượn từ 134) không có ở chế độ HD.
- `battle_assets` thêm `hd` vào 357 trong số 361 danh tính; `name_assets` thêm `hd` vào 8 thẻ mở và 8 thẻ kết hợp. Số 33, ban đầu được đăng ký riêng trong danh sách phủ sóng của trang tên, không còn cần thiết nữa. Danh sách đó đã bị xóa vào ngày 24-09-2026.
- Trang hiển thị HD khi chế độ hình ảnh hiện đang áp dụng là HD và mục nhập có `hd`, nếu không thì hiển thị hình ảnh gốc. Khóa bộ đệm của mỗi trang chứa chế độ này và trang sẽ được tạo lại sau khi chuyển đổi.
- Lấy mẫu RmlUi không có mipmap, việc giảm trực tiếp 768 px xuống 56–160 dp sẽ tạo ra hiện tượng răng cưa. Do đó, `frontend.cpp` thực hiện giảm diện tích trung bình theo chiều rộng hiển thị thực tế (dp × mật độ hiện tại hoặc đơn vị pixel của trang liên trường) khi tải, tính toán dựa trên Alpha được nhân trước và lưu vào bộ nhớ đệm một bản sao của mỗi kích thước. Hình ảnh gốc nhỏ hơn 96 px so với kích thước được hiển thị và được tải nguyên trạng.

Máy thực tế (24-09-2026, `battle-ui` cấp mini): Hai avatar tài xế trên trang xác nhận trước chiến tranh là hình ảnh rõ ràng và đầy đủ ở chế độ HD; sử dụng cài đặt để chuyển về hình ảnh gốc rồi chuyển lại, hình đại diện sẽ chuyển đổi tương ứng và hai ảnh chụp màn hình HD nhất quán từng pixel. Khi trang xác nhận trước chiến tranh được mở, F6 bị chặn bởi nút mà trang nhận được, chuyển sang cài đặt. Các trang khác chia sẻ cùng một bộ mã chụp và giảm ảnh và không có ảnh chụp màn hình thực tế từng cái một.

### Kế hoạch cắt đã sử dụng

Ban đầu, băm kết cấu RT64 được sử dụng: 9 khối 128×128 cho mỗi mặt, tổng cộng 3037 khối, bao gồm các phiên bản cơ sở và hình bóng của 304 hình ảnh. Hàm băm có thể được tính toán ngoại tuyến và tất cả 72 khối được ghi lại trong trận đấu tập đầu tiên. Các quy tắc như sau:
- Dòng lẻ đổi chỗ 4 byte;
- Mỗi mục bảng màu được sử dụng được lặp lại 4 lần;
- Các thông số cuối cùng là (32, 32, 32768, 4, 1, 2).

Sau khi đổi sang thay thế hoàn toàn thì bộ này đã bị xóa.

## Lệnh

```sh
.venv/bin/python -m tools.hd_ai.portrait_batch prepare --output assets/hd-ai/portrait-batch/full-1 --skip 29 33 166 169
.venv/bin/python -m tools.hd_ai.portrait_batch run --output assets/hd-ai/portrait-batch/full-1 --env-file /path/to/.env
.venv/bin/python -m tools.hd_ai.portrait_batch compose --output assets/hd-ai/portrait-batch/full-1 [--only grid-058]
.venv/bin/python -m tools.hd_ai.build_portrait_images --batch assets/hd-ai/portrait-batch/full-1 \
  --reviewed assets/hd-ai/portrait-matte/v2 --output assets/hd-ai/portrait-batch/whole-v1 --bind
```

Các nhóm đã có bản ghi yêu cầu sẽ không được gửi lại. `compose` và `build_portrait_images` không mất phí và có thể chạy nhiều lần; thư mục đầu ra sau này không được tồn tại. Sau khi thay đổi hook `generate_cpu.py`, bạn phải chạy lại hook đó trước rồi mới build máy chủ.