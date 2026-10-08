> **Ngôn ngữ / Language:** [Tiếng Việt](unit-icon-hd.vi.md) · [English](unit-icon-hd.en.md) · [中文](unit-icon-hd.md)

# Logo máy bay (biểu tượng đơn vị bản đồ) HD: sơ đồ sơn lại vẫn giữ được cảm giác pixel

26-09-2026. Mỗi máy bay trên bản đồ chiến thuật là một hình đại diện CI4 SD 16×16 (tài nguyên 688–1009, 320 hình ảnh khác nhau, 323 bản ghi máy bay). Các màu trại hoàn toàn đến từ bảng màu (1010 xanh, 1011 đỏ, 1012 vàng, 1013 xám; số 1–6 là thang màu trại, số 7–13 là các màu cố định như mắt và hồng, còn số 0 là trong suốt). Yêu cầu của người dùng: Độ phân giải cao phải **bảo toàn cảm giác pixel**, nhưng thay vì chỉ phóng to các pixel gốc, tốt nhất là trông giống như một bức tranh pixel mới được vẽ với độ phân giải cao hơn. Bài viết này ghi lại các lộ trình đã thử và các phương pháp được áp dụng. Công cụ [`unit_icon_hd.py`](../../tools/hd_ai/unit_icon_hd.py), tài liệu đầu ra và nghiên cứu nằm trong `assets/hd-ai/unit-icons/` (không nhập git).

## Kết luận (hoàn thành vào ngày 26-09-2026)

**MMPX×2 → 4x-PixelPerfectV4 → Lượng tử hóa cứng 32 → MMPX×2, sản phẩm là bản đồ màu 64×64. ** Toàn bộ quá trình diễn ra cục bộ, không làm mờ, khử răng cưa và phối màu. Mỗi pixel đầu ra chỉ lấy số màu được sử dụng trong ảnh gốc:

1. MMPX×2 (`pixel_scale.py`, chỉ sao chép số màu): làm mịn các bước, lắc bàn cờ và thu nhỏ thành hình vuông 2 pixel;
2. 4x-PixelPerfectV4 (ESRGAN cục bộ, `build/esrgan-models`) lấy 32×32 này và tạo ra bức tranh mịn 128×128 (màu sắc và alpha được phân tách thông qua mô hình và các pixel trong suốt được lấp đầy bằng màu đồng nhất gần nhất trước tiên);
3. HỘP được giảm xuống 32×32, mỗi pixel được dán vào số màu được sử dụng trong ảnh gốc theo khoảng cách CIELAB và các pixel bị cô lập sẽ bị xóa hai lần;
4. Sau đó, MMPX×2 thành 64×64 và chỉ làm theo các bước của kết quả 32 pixel.

Điều quan trọng là đặt MMPX ở phía trước mô hình: nếu mô hình tiêu thụ trực tiếp 16 pixel, jitter sẽ được cuộn thành một khối tròn ("vết bẩn") và nếu sử dụng MMPX×4, nó sẽ bị khóa bởi khối lớn và gần như không thay đổi; Bước cuối cùng của MMPX được so sánh với lượng tử hóa cứng trực tiếp thành 64. Hình dạng gọn gàng hơn và giống những bức tranh pixel được vẽ bằng tay hơn. 320 bức ảnh trong 17 giây trên MPS, không mất phí, không gặp vấn đề về lọc IP.

```sh
build/esrgan-venv/bin/python tools/hd_ai/unit_icon_hd.py export --output assets/hd-ai/unit-icons/v2
build/esrgan-venv/bin/python tools/hd_ai/unit_icon_hd.py run --output assets/hd-ai/unit-icons/v2   # --pre 2 --size 32 --post 2
```

`v2/hd/<rid>.idx.png` là hình ảnh số màu 64×64, `<rid>-<palette>.png` là bốn bộ kết xuất; `review.png` là 9 mẫu (ảnh gốc, mịn, 64 px, đỏ, xám) và `sheet.png` là danh sách tất cả 320 hình ảnh.

**Độ phân giải**: `resolution_scale` của cấu hình phát là 4 (giới hạn trên là 8). Biểu tượng 16 pixel chiếm 64×64 pixel bên trong trên màn hình, do đó, bản gốc 64 bit được vẽ ở tỷ lệ 1:1 ở độ phóng đại mặc định; nó được hiển thị ở tỷ lệ 2:1 ở độ phóng đại 8. Thông tin nguồn bị hạn chế và phiên bản 128 chỉ có nhiều chuyển tiếp hơn ở cạnh huyền, điều này là không cần thiết.

**Trạng thái (2026-09-27)**: Người dùng xác nhận vào trò chơi theo quy trình này trước (HD/phiên bản gốc sử dụng F6 hoặc cài đặt để chuyển đổi, biểu tượng được chuyển đổi bằng gói nghệ thuật) và có thể điều chỉnh sau; điều chỉnh chỉ thay đổi `--pre`, `--size`, `--post`, `--model` và chạy lại `run` và `pack --bind`, không cần kết nối.

## Quá trình thăm dò

### Vòng 1: Smooth → Re-pixelate 32 (Không)

PixelPerfectV4 ăn trực tiếp 16 pixel → Gaussian 0,7 → BOX thành 32 → dán số màu → xóa các pixel bị cô lập. Sau khi xem xong, người dùng nói: **"Không còn cảm giác pixel nữa"**, quá trình chuyển đổi màu sắc quá mượt mà, các cạnh cứng và mùi bàn cờ của tác phẩm gốc đều biến mất. Hãy để nó là `--pre 0 --post 0 --blur 0.7` trong công cụ.

### Vòng 2: Lấy lại cảm giác pixel (bị loại)

- Bayer phối màu theo thứ tự 2×2 / 4×4 của toàn bộ hình ảnh: nó trở nên nhiễu, không giống như các hình ảnh được vẽ bằng tay;
- Khối màu phẳng + nét tối 1 pixel (bộ lọc đa số): vẫn mịn và hầu hết các bộ lọc sẽ ăn hết điểm nhấn và mắt của một pixel;
- kết hợp (các pixel gốc bao gồm bàn cờ được sử dụng nội bộ và chỉ sử dụng kết quả vẽ lại trong các đường viền và các bước): cảm giác pixel mạnh nhất nhưng hầu như không có chi tiết mới;
- Người dùng nêu rõ: **Vui lòng sử dụng ảnh nghệ thuật pixel "có độ phân giải rất cao, được điểm lại", không bị lem hoặc làm mịn**.

### Vòng 3: Lượng tử hóa cứng (không mờ, không jitter)

Nguồn xBRZ×4 → Cứng 64: Các bước sạch sẽ và bề mặt khối phẳng, nhưng xBRZ là GPLv3 và hình dạng được vector hóa; thay vào đó người dùng đã hỏi **MMPX + ESRGAN**.

### Vòng 4: MPX ở phía trước

| chuỗi | kết quả |
| --- | --- |
| MMPX×2 → PPv4 → Cứng 64 (F) | Cấu trúc tương ứng một-một, phối màu trở thành hướng sáng và tối, lựa chọn chính của người dùng |
| MMPX×2 → PPv4 → Cứng 32 | Phiên bản 2x của cùng một chuỗi, khối lớn hơn |
| MMPX×4 → PPv4 → Cứng 64 (G) | Bị khóa bởi hình vuông 4 pixel, nó gần như là ảnh gốc; đổi sang UltraSharpV2 / Nomos8kSC / 2x AnimeSharpV3, mô hình hai lượt, MMPX×8, không có sự khác biệt; thêm nhiều bộ lọc để ăn hết những điểm nổi bật. Người dùng: "Lần này chất lượng đã đi xuống" |
| Hình ảnh nguồn nửa F và G (H) | Thỏa hiệp, không được chọn |
| Biến thể của F: Không loại bỏ các pixel bị cô lập, hai lượt, làm sắc nét trước khi lượng tử hóa, Scal2x / xBRZ×2 ở phía trước, kết hợp UltraSharpV2 | Không loại bỏ các pixel bị cô lập và giữ lại một số điểm nổi bật của một pixel; phần còn lại không có cải tiến đáng kể hoặc tròn trịa hơn |

### Vòng 5: Hoán vị và kết hợp MPX×2 và PPv4

| Kết hợp | Kết quả |
| --- | --- |
| PPv4 → Cứng 64 (không có MPX) | Lắc và nhào thành từng miếng lớn, "bôi nhọ" nhất, mặt ドモン bị biến dạng |
| MMPX×2 → PPv4 → Cứng 64(F) | Điểm cân bằng |
| PPv4 → Cứng 32 → MMPX×2 | Khuếch đại cơ học các kết quả 32 pixel, với độ tròn PPv4 |
| **MMPX×2 → PPv4 → Cứng 32 → MMPX×2** | Phiên bản 32 của F sau đó sử dụng MPX theo các bước; **Hoàn thiện người dùng** |
| PPv4 hai lượt → Cứng 64 | Tròn hơn, giống như một hình minh họa |
| riêng MMPX×4 | Đảm bảo gần như bằng ảnh gốc |

MMPX chỉ có ý nghĩa khi đặt ở phía trước mô hình; đặt nó phía sau chỉ là phóng to cơ học, nhưng nó được sử dụng trên kết quả lượng tử hóa cứng là 32 pixel, gọn gàng hơn so với lượng tử hóa cứng trực tiếp là 64.

## So sánh tất cả các lộ trình ở vòng đầu tiên

9 mẫu: ガンダム 737, マジンガーZ 944, ゲッター1 853, ダンバイン 929, ザクⅡ 779, アーガマ733. Kono・バトラーV 878. Tướng quân hắc ám 838. ドモン 692 (Sinh ra). Biểu đồ so sánh ở dạng `assets/hd-ai/unit-icons/research-2026-09-26/`.

| Chỉ đường | Kết quả | Kết luận |
| --- | --- | --- |
| Hàng xóm gần nhất ×4 | Như là | Đảm bảo |
| Scal4x (EPX hai lần, biểu đồ số màu) | Các đường chéo trở nên mượt mà hơn nhưng tạo ra nhiều góc nhọn và "vờ" nhỏ, đồng thời các vùng bị giật được phóng to thành các họa tiết | Không sử dụng |
| MMPX ×4 (biểu đồ số màu) | Quá bảo thủ, gần như là hàng xóm gần nhất | Không sử dụng |
| xBRZ ×4 / ×6 (GPLv3, Zenju) | Đồ họa vector mượt mà nhất; vùng bị biến dạng trở thành toàn bộ cấp độ màu | Được sử dụng một mình, không có pixel; là hình ảnh nguồn "được pixel lại", hiệu ứng tương tự như hàng tiếp theo |
| **4x-PixelPerfectV4 ăn trực tiếp 16 px** | Bức tranh mịn màng, chuyển tiếp ánh sáng tự nhiên và bóng tối, cấu trúc trung thực | **Hình ảnh nguồn được pixel lại** |
| 4x-PixelPerfectV4 Ăn hàng xóm gần nhất ×4 | Chỉ cần làm sắc nét các cạnh của khối pixel, vẫn là 16 khung hình | Không cần |
| 4x-deviantPixelHD, 4x-Fatality | Điểm sáng quá sắc nét, nứt và đặt sai vị trí | Không được sử dụng |
| 4x-UltraSharpV2, 4x-AnimeSharp, 4x-Nomos8kSC | Tương tự hoặc khó hơn PixelPerfectV4 | Thay thế |
| 4x-NXbrz, 4x-Fatal-Pixels (OpenModelDB) | Nguồn tải xuống tính bằng KB mỗi giây, không có sẵn | Chưa thử |
| Tái tạo pixel 32 (hình ảnh nguồn PixelPerinfV4 + độ mờ 0,7) | Nghệ thuật pixel 2x như một bức tranh mới; bốn bộ bảng màu có sẵn trực tiếp | Vòng hoàn thiện đầu tiên, sau đó bị người dùng từ chối (không có cảm giác pixel) |
| Pixelate lại 32 (hình ảnh nguồn PixelPerfectV4 và một nửa xBRZ ×6) | Gần giống như hàng trước, ít nhiễu ở cạnh hơn một chút | Không cần thiết phải giới thiệu mã GPL, thay vào đó hãy sử dụng Gaussian Blur để đạt được hiệu quả tương tự |
| Tái tạo pixel 48/64 | Đang dần tiệm cận độ mượt của xBRZ | Không được sử dụng |
| qwen-image-3.0, hàng xóm gần nhất ×32 đầu vào | Sao chép 16 ô, chỉ sửa sai màu (mắt xuất hiện màu đỏ, xanh lá cây và hồng) | Không |
| qwen-image-3.0, đầu vào bicubic ×32 | Vẫn được xây dựng lại thành 16 ô | Không |
| qwen-image-3.0, đầu vào hình ảnh mượt mà PixelPerfectV4 | Vẽ một hình ảnh pixel 48–64 px, nhưng hình dạng bị tắt (ăng-ten hình chữ V của ガンダム trở thành hai góc và khuôn mặt bị mờ) | Không |
| qwen-image-3.0, thêm bản vẽ ba chiều tương tự của cơ thể làm hình ảnh tham khảo | Hình ảnh toàn thân được vẽ theo hình ảnh tham khảo và không còn là bố cục chân dung đầu | Không |

8 yêu cầu của Qianwen có tổng trị giá khoảng 1,6 nhân dân tệ, được ghi trong `assets/hd-ai/unit-icons/test-1`, `test-2`. 16×16 chỉ có 256 pixel thông tin và mô hình chỉnh sửa phải sao chép lưới hoặc tạo lại hình dạng; "siêu phân giải + lượng tử hóa" cục bộ là trung thực nhất. **Sau đó, người dùng đã quyết định rằng không nên sử dụng mô hình đám mây nào cho các tài nguyên đó. ** Máy này (M4 Max, 128 GB) chạy SDXL/Flux + pixel art LoRA. Tạo hình ảnh là con đường cục bộ duy nhất có thể thêm "chi tiết mới", nhưng nó yêu cầu phải cài đặt và xem xét từng môi trường một nên chưa được bắt đầu.

## Truy cập (thực hiện vào ngày 26-09-2026)

Thực hiện thay thế hàm băm kết cấu RT64, giống như cách làm với bản đồ thế giới và các đối tượng vũ trụ:

- **Khóa**: Biểu tượng được vẽ từ khe con 0 (chế độ 5) được tích hợp trong `801C60A4`, là bản đồ CI4 16×16 được tải riêng, tham số bảng màu `1010 + 阵营`. Hàm băm TMEM của RT64 v5 cũng tính các mục trong bảng màu được sử dụng, do đó, bốn phe của cùng một biểu tượng là bốn khóa khác nhau, tương ứng với bốn bộ kết xuất. Thuật toán băm tuân theo `worldmap_space.ci4_hash` (Dòng số Rich TMEM 4 byte được hoán đổi, số màu được sử dụng mỗi dòng 8 byte, cộng với chiều rộng 16/chiều cao 16/tlut 0x8000/dòng 1/siz 0/fmt 2), **được kiểm tra bằng kết xuất thực**: `--dump-textures` Đang chạy (`Session.launch(dump_textures=True)`, viết `<run>/textures/<hash>.{tmem,tile.json,rice.json}` cho RT64), kết cấu 16 × 16 (dòng gạch 1, fmt 2, siz 0, mặt nạ 4) của ba máy trên bản đồ tương ứng với các phím được tính toán từng cái một.
- **Gói**: `unit_icon_hd.py pack --output v2 --pack assets/hd-ai/worldmap-surfaces/pack-v5 --bind` Viết ảnh 320 × 4 có kích thước 64×64 dưới dạng `icon-<hash>.png` (RGB của các pixel trong suốt được lấp đầy bằng màu đồng nhất gần nhất và lấy mẫu tuyến tính không tạo ra các cạnh tối; 1256 ảnh biểu tượng có cùng pixel được loại bỏ trùng lặp) và được hợp nhất vào `rt64.json`, được đăng ký là `content/art/stage1-hd.json``kind: icon`; `compile_art` chấp nhận lớp này và giữ lại `kind` trong `rt64.json` đã biên dịch (RT64 bỏ qua các trường thừa).
- **Máy thật**: `check_unit_icon_hd.py` Di chuyển-nhảy ảnh chụp màn hình cấp độ nhỏ ở chế độ HD, cắt phiên bản gốc bằng F6 và chụp một ảnh chụp màn hình khác, đồng thời xác nhận rằng hàm băm kết cấu nội dung 16×16 trong kết xuất có trong gói. Được vẽ theo tỷ lệ 1:1 với 64 pixel ở độ phóng đại mặc định là 4, màu sắc chính xác và không có viền tối ở các cạnh.
- **Gói công cộng**: Gói HD công khai bắt đầu từ ngày 28-09-2026 giống như gói dành cho mục đích sử dụng cá nhân và biểu tượng cũng có trong đó; THÔNG BÁO cho biết rằng nó được phóng to và vẽ lại từ hình ảnh pixel gốc. Trước đây `build_release.py` đã được chọn lọc bởi `kind` (`ROM_DERIVED_TEXTURE_KINDS`), đã bị hủy.
- Chưa xong: Bóng elip (tài nguyên 687) chưa được thay đổi; ý nghĩa của trại tương ứng với 1013 (màu xám) và liệu bảng màu của "Đã hành động" có bị thay đổi hay không vẫn chưa được xác nhận - phiên bản màu xám đã có sẵn trong gói và sẽ có hiệu lực một cách tự nhiên khi sử dụng.
- Bản quyền: PixelPerfectV4 là WTFPL; sản phẩm được lấy từ hình ảnh gốc và được nêu trong THÔNG BÁO khi phát hành cùng với gói HD (xem [Quy hoạch HD](hd-pipeline-plan.md)).