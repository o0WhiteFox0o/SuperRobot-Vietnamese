> **Ngôn ngữ / Language:** [Tiếng Việt](unit-pose-hd.vi.md) · [English](unit-pose-hd.en.md) · [中文](unit-pose-hd.md)

# Kết xuất 3D HD: quy mô và sản xuất thử nghiệm đầu tiên

26-09-2026. Các hình ảnh lớn về máy bay được vẽ trên các trang gốc như xác nhận trước chiến tranh, biến đổi, khả năng và のりかえ là từ `battle_assets.units` (tư thế cơ bản của máy bay, được sao chép theo bộ ba Cảnh/Album/Bảng màu). Trang có thể được phóng to lên tới 6 lần và các khối pixel hiển thị rõ ràng. Bài viết này ghi lại ước tính quy mô của việc vẽ lại bằng `qwen-image-3.0-pro` và kết quả sản xuất thử nghiệm của 3 khung máy bay. Công cụ: [`unit_pose_hd.py`](../../tools/hd_ai/unit_pose_hd.py), xuất ra `assets/hd-ai/unit-poses/` (không nhập git).

## Quy mô

```sh
.venv/bin/python -m tools.hd_ai.unit_pose_hd scale
```

| mục | số |
| --- | ---: |
| Thân hình | 363 |
| Tư thế cơ bản sau khi giảm cân | 332 |
| 96×96 | 249 |
| 128×128 | 57 |
| 128×96 | 16 |
| Phần còn lại (32×32 ×3, 128×64 ×3, 96×97, 160×128, 144×144, 130×228) | 10 |

Lệ phí dựa trên một yêu cầu, một ứng viên và giá gốc:

| Phương pháp | Số lượng yêu cầu | Chi phí (nhân dân tệ) |
| --- | ---: | ---: |
| Tờ rơi, `qwen-image-3.0-pro` | 332 | Giới thiệu về 173 |
| Tờ rơi, `qwen-image-3.0` | 332 | Giới thiệu về 66 |
| 2×2 Puzzle, Pro (chưa được xác minh trên cơ thể) | 83 | Xấp xỉ. 43 |
| Câu đố 3 × 3, Pro (chưa được xác minh) | 37 | Khoảng 19 |

Các yêu cầu bị bộ lọc IP từ chối sẽ không được tính phí (xem bên dưới). `aliyun.py` Mỗi thư mục đầu ra có giới hạn trên dành riêng là 18,12 nhân dân tệ, phải được giải phóng trước khi chạy đầy đủ.

## Hãy thử nó

Ba đơn vị: 3 Seiko (96), 177 Shin・ゲッター1 (128), 156 Dark General (128). Mỗi hình ảnh: nền xám (100.100.112), phóng đại trước 6 lần, đầu ra 20482, đăng ký và cắt bỏ bằng `portrait_matte`, chính 8 lần (96 → 768).

| Mục lục | Tiền khuếch đại | Lời nhắc | Kết quả |
| --- | --- | --- | --- |
| kiểm tra-1 | Hàng xóm gần nhất | `faithful` (chỉ định "Bản vẽ dọc theo pixel") | Cả hai đều đậu; Pro đã sao chép nó dưới dạng bản vẽ pixel, nhưng làm thẳng các đường nét và giữ lại tất cả các cạnh lởm chởm. Đăng ký IoU 0,995 / 0,987 |
| kiểm tra-2 | Hàng xóm gần nhất | `smooth` (yêu cầu khử răng cưa, được vẽ dưới dạng hình minh họa cel) | シャイニング bản nháp nửa dòng nửa pixel, giảm theo chiều ngang 3,5%, đăng ký vượt quá ngưỡng; ゲッター bị từ chối |
| **kiểm tra-3** | **Khối đôi** | **`smooth`** | **シャイニング là một bản vẽ đường celluloid rõ ràng với cấu trúc trung thực, đăng ký x1.000/y0.998, IoU 0,986 và lỗi lọc cạnh trung bình là 0,86. Đặt làm đường cơ sở. ** ゲッター bị từ chối |
| kiểm tra-4 | Nhân đôi ba lần | `smooth-plain` (xóa SD/từ nội dung hai đầu) | ゲッター Vẫn bị từ chối |
| kiểm tra-5 | Nhân ba | `faithful` | ゲッター bị từ chối (sau 45 giây suy luận, phía đầu ra); Dark General bị từ chối sau 5,7 giây (phía đầu vào) |

**Kết luận**

- Có sẵn tiền khuếch đại bicubic + `smooth` từ gợi ý; Đầu vào lân cận gần nhất sẽ hướng dẫn mô hình duy trì gió pixel.
- **Lọc IP là rủi ro chính**: Đúng・ゲッター1 Chỉ phiên bản kiểu pixel được thông qua và bản vẽ đường nét mượt mà bị chặn bởi bộ lọc phía đầu ra; Dark General thậm chí không chấp nhận đầu vào. Chỉ có 1 trong 3 máy thành công theo phương pháp cơ bản và không có dữ liệu về tỷ lệ đậu hoàn toàn. Dự kiến ​​sẽ chọn 10-20 máy chạy qua (máy bị loại sẽ không bị tính phí, chỉ máy thành công mới được thanh toán).
- Khi không có lựa chọn thay thế nào cho nội dung bị từ chối, bạn có thể trả về `faithful`+hàng xóm gần nhất (kết quả của thử nghiệm-1 "tổ chức các dòng mà không khử răng cưa") hoặc khuếch đại bằng thuật toán cục bộ.

## Truy cập

Đã hoàn tất, hãy xem phần "Hoàn thiện và truy cập" bên dưới. Hình ảnh HD được đặt tên theo key của `battle_assets` (`unit-<scene>-<atlas>-<palette>.png`). Trong trang, `unit_art` bị cắt theo alpha thành `rect`. Vùng trong suốt của bản gốc được lấp đầy bằng màu đồng nhất gần nhất mà không có cạnh tối.

## So sánh ESRGAN cục bộ (26-09-2026)

[`esrgan_pose.py`](../../tools/hd_ai/esrgan_pose.py) Sử dụng spandrel để chạy mô hình ESRGAN 4x cộng đồng: bản đồ màu trước tiên sẽ lấp đầy các pixel trong suốt thành màu đồng nhất gần nhất và alpha được chuyển qua mô hình một cách riêng biệt dưới dạng hình ảnh thang độ xám, sau đó Lanczos thu nhỏ nó xuống 8 lần bản chính. Môi trường `build/esrgan-venv` (python3.14 + torch + spandrel), mô hình `build/esrgan-models/` (4x-PixelPerfectV4 WTFPL; 4x-AnimeSharp CC-BY-NC-SA 4.0, Kim2091), không phải gói git hay gói công khai. Xuất `assets/hd-ai/unit-poses/esrgan-1/`, so sánh từng dòng của trang: hình ảnh gốc, lượt vượt qua AnimeSharp ×1/×2, lượt vượt qua PixelPerfectV4 ×1/×2, Pro (nếu có).

| mặt hàng | kết quả |
| --- | --- |
| Tốc độ | 0,6 giây cho 96² một chuyến, 1,3 giây cho hai chuyến trên MPS; khoảng gấp đôi số đó trên 128². 332 ảnh được hoàn thành trong vài phút, không mất phí, không lọc IP |
| Sự trung thực | Tương ứng từng pixel, không bị trôi cấu trúc, các cạnh alpha mượt mà |
| AnimeSharp | Các cạnh cứng, đường đậm, gần giống với đường vẽ bằng celluloid; hai đường chuyền sạch hơn một đường chuyền. Thích hợp cho nghệ thuật pixel có góc cạnh cứng như シャイニング và ゲッター |
| PixelPerfectV4 | Nhẹ nhàng hơn, đẹp hơn, với sự chuyển đổi mượt mà của các cấp độ màu; phù hợp với những bức ảnh như Dark General với độ chuyển màu sáng tối vốn có |
| So sánh với Pro | Các đường nét của Pro giống đường nét do bàn tay con người vẽ hơn, bề mặt khối gọn gàng hơn nhưng có những thay đổi nhỏ về chi tiết (ngực, ngón tay); Đường nét của ESRGAN hơi "run" nhưng mọi chi tiết đều được giữ lại |

Kết luận: ESRGAN có thể được sử dụng làm cơ sở cho tất cả các ứng dụng và hai máy bị lọc IP từ chối cũng đã được xử lý; Pro chỉ được dùng làm bonus cho máy chính.

## Hoàn thiện và truy cập (26/09/2026)

Sau khi so sánh 14 mô hình cục bộ ([`esrgan_pose.py`](../../tools/hd_ai/esrgan_pose.py), đầu ra `assets/hd-ai/unit-poses/esrgan-2`) trên ba máy, quyết định cuối cùng đã được đưa ra: sự kết hợp một nửa giữa 4x-UltraSharpV2 và 4x-PixelPerfectV4**. UltraSharpV2 (DAT) có nhiều chi tiết nhất và đường nét rõ ràng nhất nhưng người dùng cảm thấy nó sắc nét hơn một chút; trong số sáu phương pháp làm sắc nét (một phương pháp cộng với Lanczos, Gaussian 1,5 / 2,5 px, hỗn hợp nửa rưỡi với BS-Deviance / PixelPerfectV4, `esrgan-5`), hỗn hợp PixelPerfectV4 đã được chọn. Đã loại bỏ: AnimeSharpV4_RCAN, HFA2k_realplksr (bóng mờ xám), Drawimation (mờ), NumericFrames (quá tối), Faithful-Lite (giữ lại pixel), hai AnimeSharp 2x (ba đường chuyền chồng lên nhau, mềm hoặc nổi hạt). Bắt đầu từ 27-09-2026 `build/esrgan-models/` Chỉ còn lại 4x-UltraSharpV2 và 4x-PixelPerfectV4 để hoàn thiện (chỉ 4x-UltraSharpV2 và 4x-PixelPerfectV4 mới được hoàn thiện (chỉ 4x-UltraSharpV2 được sử dụng trong quy trình biểu tượng). Các mô hình so sánh khác đã bị xóa và cần được tải xuống lại từ OpenModelDB khi thực hiện lại quá trình so sánh.

Đường ống:

```sh
.venv/bin/python -m tools.hd_ai.unit_pose_hd prepare --output assets/hd-ai/unit-poses/all-1 --all --prescale bicubic
build/esrgan-venv/bin/python tools/hd_ai/esrgan_pose.py --samples assets/hd-ai/unit-poses/all-1 \
    --models build/esrgan-models --output assets/hd-ai/unit-poses/all-1 --blend 4x-UltraSharpV2 4x-PixelPerfectV4
.venv/bin/python -m tools.hd_ai.build_unit_images --run assets/hd-ai/unit-poses/all-1 --output assets/hd-ai/unit-poses/whole-v1 --bind
```

- `esrgan_pose.py --blend` Chạy hai mô hình cho mỗi tư thế (hai mô hình, mỗi mô hình là 16x, Lanczos quay lại 8x; alpha chỉ chuyển mô hình), viết `hd/unit-<scene>-<atlas>-<palette>.png`. 332 bức ảnh trong khoảng 1 giờ trên MPS.
- [`build_unit_images.py`](../../tools/hd_ai/build_unit_images.py) tạo các thư mục gói `whole-v1/` (PNG giữ nguyên alpha) và `units.json` (`srw64.unit-images.v1`, được lập chỉ mục theo bộ ba), `--bind` ghi phần `units` vào `content/art/stage1-hd.json`.
- Truy cập và đi theo đường dẫn của ảnh đại diện: `compile_art` được sao chép vào `art/units/` và `srw64-units-hd.json`; `assets.unit_lookup` tìm tệp theo bộ ba; `profile.py` → `prepare_battle_assets(..., hd_unit)` được thêm vào `battle_assets.units[n]``hd`; trình khởi chạy phát hành `launch.cpp` đọc cùng chỉ mục với bộ ba `resources` bị treo `hd` (mục nhập nội dung của trình nhập C++ thêm `resources`).
- Trang: Trang xác nhận trước chiến tranh `battle_unit` và trang chuyển đổi sử dụng `portrait_path()` (khi ở chế độ HD và với `hd` lấy file HD), trang khả năng/のりかえ/lưu ban đầu sử dụng `portrait_path`, không cần thay đổi. Xác nhận rằng giới hạn phóng to trang tối đa được tính bằng pixel ROM (6 × chiều rộng ROM ` chiều rộng tệp) và các tệp HD được lấy mẫu lại theo chiều rộng màn hình.
- Xác minh máy thực tế: [`check_unit_pose_hd.py`](../../tools/recomp/debug/check_unit_pose_hd.py), Ảnh chụp màn hình HD của trang xác nhận trước khi vào trận, F6 để cắt ảnh gốc để so sánh.
- Bản quyền: Để biết giấy phép của mô hình, hãy xem mô tả của [`esrgan_pose.py`](../../tools/hd_ai/esrgan_pose.py); sản phẩm được lấy từ màn hình gốc và được phát hành cùng với gói HD (gói công khai giống như gói dành cho mục đích sử dụng cá nhân, do người dùng xác định vào ngày 28 tháng 9 năm 2026), THÔNG BÁO cho biết kiểu máy được sử dụng. Gói phát hành lưu trữ JPEG với số pixel gấp 6 lần ROM cộng với PNG trong suốt (`compress_hd.py`).

## Hoạt ảnh chiến đấu có thể được xử lý theo cách này không?

Có, và đó là lộ trình "atlas master + part slicing" được chỉ định trong kho, nhưng nó không đơn giản như việc ném toàn bộ tập bản đồ vào mô hình. Có ba việc cần làm:

1. **Các bộ phận là các kết cấu được tải theo khối. ** Mỗi phần được tải bởi `8009761C` bằng LoadTile từ tập bản đồ CI8 (chủ yếu là 32×32, tối đa 2 KB TMEM) và RT64 tính toán hàm băm cho phần được tải và thay thế nó. Vì vậy, HD nên được cắt theo từng phần chứ không phải toàn bộ atlas; cùng một khu vực được tải với các kích thước khác nhau và được tính bằng các kết cấu khác nhau. Thuật toán băm RT64 của khối CI8 chưa được thử nghiệm với các kết xuất TMEM như CI4 (`rt64_hash.py` chỉ có hai loại: phông chữ và bản đồ), vì vậy cần phải xác minh trước.
2. ** Đường may. ** Các phần liền kề trong atlas có thể không liền kề trên màn hình. Việc phóng to toàn bộ tập bản đồ sẽ trộn màu của các khối liền kề vào các cạnh. Cách an toàn là tổng hợp toàn bộ khung hình giống như một tư thế, sau đó phóng to rồi cắt lại theo vị trí của phần trong khung (người xuất có thể ghi và tổng hợp từng khung hình theo phần đó); phần được chia tỷ lệ và xoay ở chế độ 1 sử dụng khung không bị biến dạng.
3. **Tạo riêng theo bảng màu. ** ESRGAN chỉ nhận ra RGB. Có 296 tập bản đồ với 305 bộ bảng màu (sự khác biệt màu sắc giữa kẻ thù và bạn bè). Mỗi bộ phải được sản xuất riêng biệt. Chỉ cần lưu các lát cắt 4 lần (32×32 → 128×128) là đủ. Âm lượng gấp 8 lần là không cần thiết.

Phạm vi được giới hạn ở bản đồ cơ thể, các bộ phận vũ khí, lá chắn và phần cắt vào; các hiệu ứng đặc biệt sử dụng hoạt ảnh bảng màu và hàm băm thay đổi theo mỗi lần nhảy, điều này không thể áp dụng được (kết luận tương tự đã được đưa ra trong phần bản đồ chiến thuật). Tuyến đường này không chạm đến logic chiến đấu và thời gian mà chỉ thay đổi kết cấu, phù hợp với hạn chế của "hiệu suất chiến đấu không thay đổi cách giải quyết".

**Hai lỗi trong máy thực đầu tiên (đã được sửa)**: Alpha của ESRGAN để lại các giá trị yếu lẻ tẻ trên toàn bộ khung vẽ và `rect` của trang được tính toán dựa trên alpha sẽ trở thành toàn bộ tài liệu và phần nội dung co lại và nổi trong khung vẽ trong suốt; `clean_alpha` (còn được gọi là `build_unit_images.py`, `esrgan_pose.run_pose`) giới hạn alpha ở 12 px bên ngoài mặt nạ gốc. và xóa các giá trị nhỏ hơn 8. Ranh giới trang chỉ tính các pixel có alpha ≥ 16. Ngoài ra, `<img>` của trang xác nhận không thể được lấy mẫu lại theo chiều rộng hiển thị và `rect` nằm trong tệp pixel. Ảnh chụp màn hình `check_unit_pose_hd.py` đã chỉnh sửa có cùng kích thước và vị trí với phiên bản gốc.

## Hình ảnh lớn của cơ thể được chia tỷ lệ theo cấp độ kích thước (26/09/2026, đang đánh giá)

Người dùng gợi ý rằng hình ảnh lớn của máy bay nên được chia tỷ lệ theo "khối lượng" thay vì từng đơn vị lấp đầy diện tích. Nguồn dữ liệu là mức kích thước của bản ghi khung máy bay: bảng khung máy bay ROM (`0x71B80`, 36 byte mỗi thanh) **+4 5 bit thấp hơn** là 1/2/4/8/0x10 → SS/S/M/L/LL (bản ghi thời gian chạy `+0x0C`, trang khả năng `801D1680` cùng một thuật toán; bit cao 0x80 có ý nghĩa khác). 363 trạm theo thống kê pixel cấp độ và tư thế:

| Cấp độ | Số lượng đơn vị | Tạo dáng canvas | Chiều cao của hộp giới hạn pixel (tối thiểu/trung bình/tối đa) |
| --- | ---: | --- | --- |
| SS | 5 | 32² × 3 (ドモン, マスターアジア, アルベルト生生), 96² × 2 | 25/18/87 |
| S | 57 | 96² ×55, 128×96 ×2 | 39/84/96 |
| M | 205 | 96² ×173, 128² ×20, 128×96 ×10, 130×228 ×1 | 40/87/122 |
| L | 58 | 96² ×46, 128² ×10, 144² ×1, 128×96 ×1 | 65/88/126 |
| LL | 38 | 128² ×28, 160×128, 128×64 ×3, 128×96 ×3, 96² ×3 | 53/94/128 |

Kết luận: **Kích thước pixel Sprite không phản ánh loại kích thước**. Hầu hết các cấp độ S, M và L được vẽ trên khung vẽ 96² và hộp giới hạn nằm trong khoảng 85-90 px (cấp độ S của dòng ダンバイン cũng là 96 px). Chỉ LL thường sử dụng 1282; trong cùng một cấp độ, có các hình ảnh phẳng hoặc nhỏ như Gフォートレス (96×40) và バトルクラフト (60×39). Vì vậy, việc “thống nhất tỷ lệ theo pixel ROM” sẽ không hiệu quả. Nó phải dựa trên mức độ dữ liệu cơ thể.

Bản nháp (được triển khai trong không gian làm việc, chưa được gửi): Ảnh chụp nhanh trang xác nhận trước chiến tranh có `size` (0–4). Trang lấy một phần diện tích theo cấp độ và sau đó điều chỉnh nó theo hộp giới hạn, vẫn giữ lại 6 lần giới hạn pixel ROM. Phiên bản đầu tiên có LL 100%, L 86%, M 72%, S 58% và SS 46%; Sau khi đọc nó, người dùng đã yêu cầu nén lại bảng điều khiển, thân máy lớn hơn, SS/S nhỏ hơn và LL ngột ngạt hơn. Phiên bản thứ hai: vùng hiệu ứng khả năng 70dp → 44dp, hằng số chiều cao vùng cơ thể 462 → 436, giới hạn trên 320 → 360dp (960×720 Khung cơ thể dưới cửa sổ logic là 258 → 300dp), và tỷ lệ chia sẻ là LL 100%, L 84%, M 70%, S 52% và SS 30%. Phiên bản thứ ba (đã hoàn thiện): LL đề cập 115%, với banner trên cùng và bảng điều khiển phía dưới, vừa đủ để không lấn át các yếu tố khác; cấp độ kiểm tra `config/recomp/mini-stages/battle-ui-ll.json` (kẻ thù được thay thế bằng デビルガンダム), `check_unit_pose_hd.py` có thể vượt qua đường cấp độ. Sơ đồ nguyên lý (ba đơn vị cho mỗi cấp độ, được tổng hợp ngoại tuyến từ toàn bộ phiên bản 1) và ảnh chụp màn hình máy thực tế (ゼーロン L so với Miミニフォー S) đã được hiển thị cho người dùng. Được xác định: giá trị cổ phần; Đặc tính sinh học của 32² bị giới hạn gấp 6 lần giới hạn trên chỉ khoảng 120 px, liệu có nên nới lỏng hay không; 362 シュバルツ và các bản ghi giữ chỗ khác được đánh dấu SS nhưng mượn từ hình ảnh của シャイニング.