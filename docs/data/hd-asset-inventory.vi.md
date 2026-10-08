> **Ngôn ngữ / Language:** [Tiếng Việt](hd-asset-inventory.vi.md) · [English](hd-asset-inventory.en.md) · [中文](hd-asset-inventory.md)

# Kiểm kê tài sản HD: phân loại, hiệu ứng động bản đồ và lựa chọn mô hình Đám mây Alibaba

Ngày: 23-09-2026, 24-09-2026 để bổ sung hiện trạng các loại. Bản thân hàng tồn kho đến từ phân tích tĩnh. Trò chơi lúc đó không chạy và giao diện sạc không được gọi. Để biết thông tin về đường dẫn truy cập sẽ sử dụng cho từng loại và bước cần thực hiện, hãy xem [Quy hoạch HD](../design/hd-pipeline-plan.md); để biết số đo thực tế của các mẫu trước đó, hãy xem [Alibaba Cloud Benchmark](../design/hd-ai-benchmark.md).

Công cụ kiểm kê là [`asset_inventory.py`](../../tools/content/asset_inventory.py). Nó giải nén tất cả tài nguyên của ROM, xác định loại và kích thước theo tiêu đề, sau đó sắp xếp chúng theo phạm vi số tài nguyên và ghi kết quả vào `build/content/asset-inventory.json`. Kiểm tra tương ứng là [`test_asset_inventory.py`](../../tests/test_asset_inventory.py). Khi có ROM, tổng số lượng và số lượng hình ảnh trong từng danh mục chính sẽ được kiểm tra.

**Quyết định phạm vi 23-09-2026**: Các danh mục liên quan đến hoạt hình chiến đấu (hình chiến đấu, hình vũ khí, lá chắn, hình cắt, hiệu ứng đặc biệt, hình nền chiến đấu 3D, HUD chiến đấu) tạm thời bị đình chỉ; LoRA sẽ không được đào tạo và tính nhất quán về phong cách sẽ phụ thuộc vào hình ảnh tham khảo và đánh giá theo từng đợt.

Có hai nguồn khoảng. Các khoảng có bảng liên kết hoặc trình trích xuất hiện có được đánh dấu là `table`; phần còn lại được xác định thủ công sau khi hiển thị thành ảnh và được đánh dấu là `inspected`. Bài viết này sử dụng "kiểm tra trực quan". Kiểm tra bằng mắt chỉ có thể giải thích được nội dung của hình ảnh chứ không thể giải thích được nó nằm trên màn hình nào hoặc nó được vẽ bằng chức năng nào.

## 1. Tổng số tiền

ROM tổng cộng 6.436 tài nguyên:

| Loại | Số lượng | Mô tả |
| --- | ---: | --- |
| Hình ảnh | 1.641 | 919 hình ảnh 4 bit, 722 hình ảnh 8 bit |
| Bảng màu | 1.368 | RGBA5551 |
| thùng chứa hình học 3D | 483 | F3DEX2 |
| Bố cục bản đồ | 155 | 158 hồ sơ bản đồ được chia sẻ |
| Dữ liệu khác | 2.789 | Tạo cảnh, mô tả, tập lệnh và bảng |

## 2. Phân loại và lộ trình xử lý

Xem Phần 4 để biết các khả năng của mô hình trong cột "Ưu tiên trên nền tảng đám mây của Alibaba". "Không có AI" có nghĩa là việc phóng to theo quy tắc, vẽ lại văn bản gốc hoặc giao diện gốc sẽ phù hợp hơn.

### Nhân vật

| Danh mục | Số tài nguyên | Số lượng hình ảnh | Kích thước phổ biến | Tuyến đường | Ưu tiên đám mây của Alibaba | Thay thế |
| --- | --- | ---: | --- | --- | --- | --- |
| Hình đại diện | 9–609 | 300 hình ảnh / 301 bộ bảng màu | CI8 96×96×232, 97×97×68 | Toàn bộ hình ảnh đăng trực tiếp | `qwen-image-3.0` Xuất 2K rồi thu nhỏ xuống 4 lần; hình đại diện HD được phê duyệt làm hình ảnh tham khảo thứ hai | `wan2.7-image` (tối đa 9 ảnh tham chiếu); sử dụng siêu điểm thông thường để đảm bảo |
| Avatar nhân vật chính (kiểm tra trực quan) | 1308–1336 | 4 | CI8 96×96 | Tương tự như trên | Tương tự như trên | Tương tự như trên |

- Nhận dạng ký tự 361 sử dụng 300 hình ảnh và cùng một hình ảnh có thể được ghép với các bảng màu khác nhau.
- **Tình hình hiện tại (24-09-2026)**: Tất cả 300 bức tranh được tạo ra bằng câu đố 2×2 sử dụng `qwen-image-3.0` và người tổ chức sẽ vẽ toàn bộ bức tranh, xem [Hình đại diện nhân vật HD](../native/native-portraits-hd.md). Việc so sánh mô hình và khuyến nghị hai tầng dưới đây là bản ghi lại sự lựa chọn tại thời điểm đó.
- Đừng huấn luyện LoRA. Phong cách nhất quán dựa trên hai điều: hình ảnh tham khảo có phong cách cố định và cùng một loạt tác phẩm được sản xuất theo đợt và được xem xét theo từng đợt.

Các mô hình tùy chọn khác cho hình đại diện. Bốn mô hình chỉnh sửa Alibaba Cloud đầu tiên đã được thử nghiệm vào ngày 08-9, nhưng bảng sau chưa được thử nghiệm:

| Người mẫu | Loại | Đơn giá | Giấy phép/Hạn chế | Bình luận |
| --- | --- | ---: | --- | --- |
| `wan2.7-image` (không phải Pro) | Biên tập viên đám mây của Alibaba | 0,20 nhân dân tệ | — | Tối đa 9 ảnh tham khảo, có thể đặt cùng lúc các avatar khác của cùng nhân vật |
| Điểm siêu sáng tạo VIAPI / Điểm siêu bình thường | Siêu điểm đám mây của Alibaba | 0,06 / 0,02 nhân dân tệ | — | Không có bí danh, nhưng chi tiết hạn chế. |
| [Seedream 4.5 / 5.0](https://seed.bytedance.com/en/seedream4_5) | Trình chỉnh sửa động cơ núi lửa Byte | Khoảng 0,03–0,054 USD | API thương mại | Có sẵn trong nước, có tính nhất quán cao trong tham chiếu nhiều hình ảnh |
| [Hình ảnh chuyên nghiệp của Gemini 3](https://ai.google.dev/gemini-api/docs/pricing) | Google Chỉnh sửa | 0,134 USD | API thương mại | Hình ảnh tham chiếu tối đa 5 ký tự; Hạn chế truy cập trong nước |
| [Real-CUGAN](https://github.com/bilibili/ailab/tree/main/Real-CUGAN) | Siêu điểm hoạt hình địa phương | 0 | MIT | Do Station B sản xuất, chuyên dùng cho hình ảnh hoạt hình, chân thực và không vẽ lại |
| Anime Real-ESRGAN 6B / waifu2x | Siêu điểm anime địa phương | 0 | BSD-3 / MIT | Tương tự |
| [APISR](https://github.com/Kiteretsu77/APISR) | Siêu điểm hoạt hình địa phương | 0 | GPL-3.0, chỉ sử dụng trong học tập | Không phù hợp để phân phối |
| [Qwen-Image-Edit-2511](https://github.com/QwenLM/Qwen-Image) | Trình soạn thảo mã nguồn mở cục bộ, 20B | 0 | Apache 2.0 | Cùng nguồn gốc với Qwen trên đám mây; Bộ nhớ 128 GB có thể chạy cục bộ |
| [Nhà phát triển FLUX.2](https://huggingface.co/black-forest-labs/FLUX.2-dev) / Nhà phát triển FLUX.1 Kontext | Chỉnh sửa mã nguồn mở cục bộ | 0 | Giấy phép phi thương mại | Vai trò được duy trì nhưng bị hạn chế giấy phép |
| Qwen-Image-2.1 (2026-09-20, 7B) | Trình soạn thảo mã nguồn mở cục bộ | 0 | Giấy phép nghiên cứu Qwen, phi thương mại | Quá mới, giấy phép bị hạn chế |

- Gói địa phương không tính phí theo đơn hàng. Thí sinh có thể sản xuất bao nhiêu tùy ý và có thể sao chép các hạt giống cố định. Giá là lần tải xuống ban đầu hàng chục GB mô hình và thời gian tạo của mỗi hình ảnh. Máy này là M4 Max, bộ nhớ thống nhất 128 GB, model 20B chạy được.
- Nên chia thành hai lớp:
- Tất cả 300 bức ảnh lần đầu tiên được hiển thị cục bộ bằng Real-CUGAN, không mất phí và không có răng cưa;
- Vẽ lại tổng quát các ký tự chính (đám mây `qwen-image-3.0` hoặc Qwen-Image-Edit-2511 cục bộ).
- Vòng so sánh tiếp theo đề xuất thêm Real-CUGAN, Seedream 4.5 và Qwen-Image-Edit-2511 gốc để so sánh song song với ứng cử viên qwen-image-3.0 đã chọn 2.

### Bản đồ

| Danh mục | Số tài nguyên | Số lượng | Định dạng/kích thước | Tuyến đường | Ưu tiên đám mây của Alibaba | Thay thế |
| --- | --- | ---: | --- | --- | --- | --- |
| Atlas địa hình chiến thuật | 6228–6236 | 8 512×512 + 1 khung khuẩn lạc (512×48), 27 bảng màu | CI8 | Phương án thay thế: đầu tiên phóng to theo tập bản đồ rồi ghép lại bản đồ (không sử dụng) | Điểm siêu bình thường VIAPI (duy trì tính minh bạch) | `wan2.7-image-pro` Xử lý toàn bộ tập bản đồ |
| Bố trí bản đồ chiến thuật | 6264–6418 | 155 bản (158 bản ghi) | Phổ biến 800×640 (23 ảnh), 880×720 (21 ảnh), tối đa 960×720 | Dán trực tiếp toàn bộ bản đồ, bản đồ số màu + bảng thời gian thực (Phần 3); Mẫu bản đồ 20 đã được lập nhưng chưa gửi | Toàn bộ bức tranh đã được tinh chỉnh và ghép lại với nhau: `qwen-image-3.0-pro`, bức tranh lớn được tạo theo khối theo cửa sổ | Chỉ dùng siêu điểm, không sàng lọc |
| Hoạt hình bảng bản đồ | 6419–6435 | 17 bản | Bảng màu | Các lớp động, được sao chép chính xác từ dữ liệu gốc | Không cần AI | — |
| ID khung máy bay (biểu tượng đơn vị) | 687–1015 | 323 bản ghi (320 bản ghi khác nhau) | CI4 16×16 | Độ phân giải siêu cao cục bộ + pixel lại, xem [ID đơn vị HD](../design/unit-icon-hd.md) | Không có AI trên nền tảng đám mây | Hàng xóm gần nhất đảm bảo ×4 |
| Hoạt hình hiệu suất bản đồ | 1472–1611 | tập bản đồ 21 | CI8 513×(33–417) | Bậc thầy Atlas + lát cắt phần | VIAPI siêu điểm bình thường | `wan2.7-image-pro` |
| Bản đồ thế giới | Ô nội tuyến cho 5602–5606, vũ trụ 5599 | 5 bề mặt + vũ trụ | Khối CI4 64×64 | Thay thế băm RT64, lát cắt 512 px; **Đã kết nối** | `qwen-image-3.0-pro` + Bảo vệ bờ biển | — |

- Hầu hết các bản đồ chiến thuật đều có kích thước 3200×2560 đến 3840×2880 khi phóng to 4 lần, vượt quá giới hạn diện tích đầu ra của Qianwen 2048². 135 trong số 155 bố cục vượt quá giới hạn, do đó toàn bộ hình ảnh phải được tinh chỉnh và tạo trong các cửa sổ, có lớp phủ chồng lên nhau, sau đó được kết hợp trong vùng được bảo vệ.
- 8 bộ bản đồ có tổng số chỉ 2,12 triệu pixel, trong khi toàn bộ bản đồ được ghép lại có 73,47 triệu pixel. Siêu điểm cấp độ Atlas có chi phí thấp và cùng một ô giống nhau nhất quán trên mỗi bản đồ nhưng nó không thể vẽ chi tiết tổng thể trên các lưới. Mẫu Bản đồ 20 được tạo trực tiếp từ toàn bộ bản đồ: 448×512 và 1792×2048 được lấy trong một yêu cầu.

### Nhận dạng khung máy bay (biểu tượng đơn vị bản đồ)

Mỗi máy bay trên bản đồ chiến thuật là một hình đại diện SD 16×16. Hai vị trí phụ yêu tinh được `801C60A4` tạo cho mỗi đơn vị, cả hai đều ở chế độ 5:

- **Khe phụ 0**: Bản thân biểu tượng, mức độ ưu tiên 0x91, tham số bảng màu là `1010 + 阵营`.
- **Khe phụ 1**: Hình elip bóng (tài nguyên 687), mức độ ưu tiên 0x92, được vẽ phía sau biểu tượng.

Các màu của trại hoàn toàn đến từ bảng màu: 1010 xanh, 1011 đỏ, 1012 vàng, 1013 xám. Thay đổi bảng màu của cùng một biểu tượng là một vấn đề khác. Ý nghĩa của trại tương ứng năm 1013 và liệu "hành động" có được thay thế bởi nó hay không vẫn chưa được xác nhận. 1015 không phải là màu phù hợp với nhóm này và việc sử dụng nó vẫn chưa được nghiên cứu.

Các số 1–6 của bảng màu là các màu trại, các số 7–13 là các màu cố định (mắt xanh, hồng, v.v.) và số 0 là trong suốt. Vì vậy, phiên bản HD phải tiếp tục thay đổi màu sắc theo bảng màu chứ không thể chỉ làm một bộ RGB.

**Không có AI**:
- Trong đợt đo thực tế ngày 08-9, phần thân 16 pixel sẽ được tái tạo thành hình dạng mới;
- 16×16 cũng nằm dưới kích thước đầu vào tối thiểu cho tất cả các dịch vụ.

Thay vào đó, hãy sử dụng thuật toán nâng cấp pixel art xác định. Chúng được tính toán trực tiếp từ ROM cục bộ và có thể được tạo trong lần nhập đầu tiên mà không cần phân phối tệp nghệ thuật.

| Phương pháp | Hiệu ứng | Bảng Màu | Kết luận |
| --- | --- | --- | --- |
| Song tuyến tính (tình hình hiện tại) | Rõ ràng bị mờ ở độ phân giải bên trong gấp 4 lần | — | Cần thay đổi |
| hàng xóm gần nhất |
| Scal4x (EPX hai lần) | Các dấu gạch chéo trở nên mượt mà hơn, vẫn mang phong cách pixel | **Chỉ sử dụng màu cơ bản**: Thao tác trực tiếp trên bản đồ màu, một kết quả áp dụng cho tất cả các trại | Lựa chọn đầu tiên khi giữ lại cảm giác pixel |
| hqx×4 | Giữa cả hai, giữ lại nhiều chi tiết hơn và vẫn có các cạnh lởm chởm | Màu sắc mới sẽ được pha trộn | Thay thế |
|
| Vẽ lại thủ công 64×64 | Chất lượng tốt nhất | Chỉ cần vẽ theo bản đồ màu | 317 bức ảnh là rất nhiều công việc, chỉ dành cho những lựa chọn trong tương lai |

- **Thuật toán trộn màu** cần được tạo riêng theo bảng màu: 317 ảnh × 4 trại, khoảng 1.300 ảnh 64×64.
- **Truy cập**: Sử dụng thay thế hàm băm kết cấu RT64. Biểu tượng là một kết cấu 16 × 16 được tải lên riêng biệt và bản thân hàm băm phân biệt bảng màu, tương ứng với "một bản sao cho mỗi trại".
- **Độ phân giải**: Lấy mẫu một-một ở độ phóng đại bên trong 4; Phiên bản 8× hoặc mipmap có sẵn ở độ phóng đại cao hơn.
- **MMPX (Đã thử)**: Thuật toán nâng cấp sprite chỉ sử dụng các màu cơ bản (McGuire & Gagiu 2021, Giấy phép MIT). [`pixel_scale.py`](../../tools/hd_ai/pixel_scale.py) đã được ghép vào bản đồ màu theo triển khai tham chiếu (cũng có Scal2x) và 5 biểu tượng đã được thử. Kết quả rất thận trọng, gần như duy trì hình dạng pixel lân cận gần nhất và chỉ cắt bớt một số răng cưa bị cô lập. Đối với loại hình đại diện 16 pixel có nhiều jitter này, sự cải thiện không rõ ràng như Scal4x.
- **Tùy chọn AI**: 16×16 chỉ có 256 pixel thông tin. Những gì AI làm thực chất là "vẽ lại" chứ không phải "phóng to". Để điền thông tin chi tiết thực tế, bạn phải cung cấp thêm nguồn thông tin. Theo ý tưởng này, thí sinh được chia thành ba loại và trước tiên họ phải làm bài thi với 5 bức ảnh:
1. **Dịch vụ tạo pixel chuyên dụng**: Đầu ra vẫn là pixel drawing nhưng kích thước lớn hơn và chi tiết hơn, phù hợp để "bảo toàn kiểu pixel".
- Việc thay đổi kích thước của [PixelLab](https://www.pixellab.ai/docs/tools/resize) sử dụng AI để vẽ lại pixel sang kích thước mới, trong khoảng từ 16–200 px. Nên phóng to tối đa 2 lần mỗi bước (16→32→64). Tài liệu cho biết nó chỉ có sẵn trong plug-in Aseprite; cũng có [API](https://api.pixellab.ai/v2/docs), nhưng vẫn phải xác nhận xem nó có chức năng tương đương hay không.
- [Retro Diffusion](https://retrodiffusion.ai/) cung cấp mô hình pixel art, hỗ trợ img2img (cường độ có thể điều chỉnh), nền trong suốt và bảng màu đầu ra hạn chế.
- Cả hai đều là dịch vụ thương mại ở nước ngoài, cần phải đăng ký và giá phải được xác nhận sau khi đăng ký. Bạn có thể giới hạn đầu ra ở 14 màu ban đầu của biểu tượng, sau đó ánh xạ nó trở lại bản đồ màu và tất cả bốn màu trại sẽ tự động có hiệu lực.
2. **Mô hình chỉnh sửa ảnh phổ thông + ảnh tham khảo**: phù hợp với "Làm mịn HD". Gửi biểu tượng 16×16 cùng với hình ảnh chiến đấu của cùng một thân máy (ảnh nghệ thuật pixel từ 97 px trở lên có cùng hình dạng trong ROM) và để mô hình vẽ lại biểu tượng theo hình dạng của hình ảnh. Bài viết này chỉ sử dụng các mô hình chiến đấu làm tài liệu tham khảo và không liên quan đến hoạt ảnh chiến đấu HD bị trì hoãn.
- Thất bại ngày 08-9 chính là do không có hình ảnh tham khảo.
- Có sẵn `qwen-image-3.0` (3 ảnh đầu vào) hoặc `wan2.7-image` (9 ảnh tham khảo). Mỗi ứng cử viên có 317 vé có giá khoảng 63 nhân dân tệ.
- Sau khi đầu ra giảm xuống còn 64×64, các số màu cũng được lượng tử hóa trở lại bảng màu ban đầu.
3. **Mô hình siêu phân giải pixel cộng đồng**: Chạy cục bộ, miễn phí nhưng đều là các mô hình cũ được đào tạo bằng hình ảnh hoạt hình vào năm 2020.
- [4x PixelPerfectV4](https://openmodeldb.info/models/4x-PixelPerfectV4): Đã được cấp phép WTFPL, bạn có thể thoải mái sử dụng.
- [4x Fatal Pixels](https://openmodeldb.info/models/4x-Fatal-Pixels): được cấp phép CC-BY-NC-SA, không sử dụng cho mục đích thương mại.
- `4x xbrz`, `4x scalenx`: Chỉ cần sử dụng mạng để bắt chước thuật toán cùng tên.

Chúng không có nguồn thông tin bổ sung, gần với xBR đã học và có mức độ ưu tiên thấp nhất.
- **Vectorization**: [Depixelizing Pixel Art](https://www.cs.jhu.edu/~misha/ReadingSeminar/Papers/Kopf11.pdf) của Kopf–Lischinski không phải là AI. Nó chuyển đổi ảnh nghệ thuật pixel thành các đường viền vector mượt mà có thể phóng to tùy ý và giữ lại các vùng màu gốc. "Tracing Bitmap → Pixel Art" của Inkscape sử dụng nó ([libdepixelize](https://gitlab.com/inkscape/devel/libdepixelize)). Nó bỏ qua kênh trong suốt và xử lý các đường viền riêng biệt. Máy này chưa được cài đặt và không được đưa vào so sánh.

### Chiến đấu (tạm dừng)

| Danh mục | Số tài nguyên | Số lượng hình ảnh | Định dạng/kích thước | Tuyến đường | Ưu tiên đám mây của Alibaba | Thay thế |
| --- | --- | ---: | --- | --- | --- | --- |
| Yêu tinh chiến đấu máy bay | 1612–2476 | 296 tập bản đồ / 305 bộ bảng màu | CI8 97×97 ×94, 129×129 ×40, v.v. | Bậc thầy Atlas + cắt từng phần | Điểm siêu thông thường VIAPI, dựa trên toàn bộ tập bản đồ | `wan2.7-image-pro` Xử lý toàn bộ tập bản đồ, sử dụng phác thảo chấp nhận IoU |
| Các họa tiết dành riêng cho vũ khí (kiểm tra trực quan) | 2477–3005 | 26 | CI8, tối đa 321×257 | Tương tự như trên | Tương tự như trên | Tương tự như trên |
| Khiên | 4258–4364 | 31 | CI4 66×65, v.v. | Tương tự như trên | Điểm vượt mức bình thường của VIAPI | — |
| Cắt vào | 1337–1471 | 32 | CI8 513×449, v.v. và các bộ phận CI4 | Khung tĩnh được dán trực tiếp toàn bộ hình ảnh, khung hình động được cắt thành từng phần | `wan2.7-image-pro`, sử dụng hình đại diện HD đã được phê duyệt của người lái xe làm thông tin nhận dạng | `qwen-image-3.0-pro` 2K |
| Hiệu ứng đặc biệt | 3006–4257 | 238 bức tranh/289 bộ bảng màu (trong đó có 3 bộ 592 màu) | CI4 chủ yếu, 66×33 đến 514×513 | Phóng to hình ảnh chỉ mục và giữ lại hoạt ảnh bảng màu | Không có AI | Hiệu ứng đặc biệt mới trong tương lai: video nền đen (Phần 4) |
| Hiệu ứng đặc biệt bổ sung (kiểm tra trực quan) | 4365–4987 | 89 | Chủ yếu là CI4 | Tương tự như trên | Không có AI | — |
| Bản đồ mảnh hiệu ứng đặc biệt (kiểm tra trực quan, sử dụng để xác định) | 5335–5374 | 22 | CI4 512×(64–336) | Tương tự như trên | Không có AI | — |
| Kết cấu nền chiến đấu 3D | 6067–6227 | 49 hình ảnh / 112 bộ bảng màu | CI4 320×240 | Thay thế kết cấu, hình học theo đường dẫn lưới gốc | Siêu điểm tổng hợp VIAPI (tuân thủ tỷ lệ 4:3) | Các cảnh chính sử dụng `qwen-image-3.0-pro` 2K |
| Nhãn HUD chiến đấu (kiểm tra trực quan) | 1159–1160 | 1 | CI4 256×88, được viết bằng "chống/phòng thủ/trở lại" và 14 tên khả năng (Iフィールド, オーラバリア, nhân bản, シールド phòng thủ, v.v.) | Văn bản gốc, **ĐỂ LÀM** (24/09/2026 người dùng quyết định đặt nó sang một bên trước) | Không có AI | — |

- Chỉ có 4519 hiệu ứng đặc biệt với nhân vật (bổ sung hiệu ứng đặc biệt, CI4 514×193): 16 chiêu thức đặc biệt bằng chữ Hán: Phượng Hoàng, Ánh Sáng, Bạo Chúa, Mã Tương, Triệu, Long Lôi, Diệt Quỷ Hình, Vương Kiệt, Phá và Chém. 24-09-2026 Người dùng quyết định không dịch mà chỉ dịch ở độ phân giải cao nhất, **được thực hiện**. 238 bức ảnh của Main Effects 3006–4257 đã được xem từng cái một mà không có văn bản.
- Họa tiết nền 3D là bầu trời, đường chân trời, thành phố, biển và vũ trụ.

### Hình ảnh và văn bản

| Danh mục | Số tài nguyên | Số lượng | Tuyến đường | Ưu tiên đám mây của Alibaba |
| --- | --- | ---: | --- | --- |
| Nền liên trường | 5470–5493 | ​​8 bức tranh, hai bộ bảng màu sáng/tối | Toàn bộ hình ảnh được đăng trực tiếp, **đã được kết nối** ([Nền Interfield HD](../native/native-backgrounds-hd.md)) | `qwen-image-3.0-pro` 2K; siêu điểm thế hệ thay thế. Phiên bản tối thu được bằng cách sử dụng ánh xạ màu xác định |
| Tiêu đề ngọn lửa nền (kiểm tra trực quan) | 684 | 1 (CI8 512×512) | Đăng trực tiếp toàn khung hình, **đã kết nối** ([màn hình tiêu đề](../native/native-title-and-story-images.md)) | `qwen-image-3.0-pro` hoặc siêu điểm thông thường |
| Đường tập trung (kiểm tra trực quan) | 611 | 1 (CI4 512×64, với hoạt ảnh bảng màu 613) | Bảo tồn hoạt ảnh bảng màu | Không có AI |
| Bầu trời đầy sao (kiểm tra trực quan) | 5582 | 1 (CI4 320×240) | Toàn bộ hình ảnh được đăng tải trực tiếp; nó đã được truy cập bằng vũ trụ bản đồ thế giới và nền trường `whole-v2` | Siêu điểm sáng tạo |
| Tiêu đề Logo, logo nhà sản xuất, GAME OVER, trang bản quyền (kiểm tra trực quan) | 615, 617, 620, 681 | 4 | Logo tiêu đề đã được chèn vào toàn bộ khung tiêu đề; phần còn lại được khuếch đại hoặc vẽ lại thủ công theo quy định và nhãn hiệu không được AI | Không sử dụng AI |
| Menu tiêu đề, tên tác phẩm khởi động (623) và tên đơn vị trình diễn (656) | 623, 656 | 2 album ảnh | Văn bản gốc, **được kết nối** (2026-10-04 đã thêm tên công việc 628–650, tên đơn vị 658–680) | Không cần AI |
| Tiêu đề chương | 4988–5105 | 117 CI4 514×65, chia sẻ 1 bảng màu | Văn bản gốc, **được kết nối** | Không cần AI |
| Mở trang văn bản | 5506–5543 | 30 | Văn bản gốc, **được kết nối** | Không cần AI |
| Tín dụng (kiểm tra trực quan) | 5544–5569 | 20 | Văn bản gốc, **được kết nối** | Không cần AI |
| Trang văn bản kết thúc (kiểm tra trực quan) | 5570–5581 | 7 | Văn bản gốc, **được kết nối** | Không cần AI |
| Bản đồ cửa sổ và HUD, thanh viền hội thoại, con trỏ, giao diện người dùng linh tinh | 1295, 1296, 1302, 5494–5505 | 7 | Vẽ theo quy tắc hoặc sử dụng RmlUi; viền hộp thoại đã được vẽ lại theo mã thiết kế ban đầu ([Dialog HD border](../native/native-dialogue-runtime-hd.md)) | Không có AI |
| Phông chữ | 0–8 | 2 | Văn bản gốc | Không có AI |
| Hình học 3D | 5584–6066 | 483 container | Lưới bản địa; 5600 điểm đánh dấu và bản đồ thế giới tàu và địa danh được kết nối | `Tripo` chỉ được sử dụng để làm lại ý tưởng, không thay thế 1-1 |

Những hình ảnh có chữ trên phải được xử lý riêng theo ngôn ngữ. Tắt HD cũng không tắt được dịch.

## 3. Hiệu ứng động của bản đồ chiến thuật

Phần này xuất phát từ việc đọc tĩnh `801C6EFC`, `800945D4`, `8009CB04`/`8009CC0C`, `800858DC` và triển khai 3D34 `8020A874`. "Nhảy" là việc thực hiện vòng lặp chính chiến thuật `801DFBD0` một lần; 1 lần nhảy và khoảng 2 VI là suy đoán chưa được xác minh.

### 3.1 Bản ghi bản đồ

12 byte cho mỗi bản ghi:

```text
u16 layout, atlas, palette, aux1, aux2; u8 模式; u8 参数
```

`group_count` là số ô sau khi loại bỏ trùng lặp. Mỗi nhóm tương ứng với một ô và danh sách vị trí của nó và không liên quan gì đến hoạt ảnh. Không có mã để viết lại một ô trong quá trình hoạt động: người đọc bố cục chỉ có thể vẽ, lấy địa hình và lấy kích thước, tất cả đều ở chế độ chỉ đọc. Cờ vị trí `0x2000` xuất hiện tổng cộng trong bản đồ 43, 45, 47, 119, 444 và không có mã nào đọc nó.

### 3.2 Mặt nước: Chu kỳ bảng màu (xác nhận mã)

- **LOAD**: aux1/aux2 khác 0 được tải bởi `8009CB04(通道, 资源)`, kênh được ghi tại `80178D50 + 通道×0x12`.
- **PUSH**: `801DFBD0` gọi `8009CC0C` mỗi bước nhảy. Khi đếm ngược về 0, màu của khung tiếp theo sẽ được ghi trực tiếp vào tài nguyên bảng bản đồ (khe 0x3B). `800945D4` TLUT được tải lại mọi khung hình nên việc ghi sẽ xuất hiện ngay lập tức. Các điều kiện cổng là `8010279D != 0` và `80178C6A & 0x81 == 0`, chưa kiểm tra xem menu hoặc tạm dừng có bị đóng băng hay không.
- **định dạng tài nguyên phụ trợ**: `u8 帧数 F, u8 起始色号 S, u8 颜色数 N` trước tiên, sau đó là F byte bước nhảy trên mỗi khung hình, sau đó là N×F RGBA5551. Độ lệch của khung c có màu f là `3 + F + (c×F + f)×2`. Tất cả 16 tài nguyên đều có độ dài tương tự nhau.
- **Thông số mặt nước**: 6419–6424, số màu 0xC0–0xD0, 17 màu × 9 khung hình × 9 lần nhảy trên mỗi khung hình, 81 lần nhảy trong một vòng.
- 38 tài liệu tham khảo bản đồ, 36 trong số đó có pixel chứa các số màu này trong tập bản đồ của chúng.
- Vùng nước rộng: Bản đồ 56 có 1.489/2.700 ô, khoảng 205.000 pixel; Bản đồ 13 có 834 ô.
- **Vòng lặp khác**:
- 6426: 0xB0–0xBE, 5 bản đồ
- 6427: 32 khung hình, bản đồ 7
- 6429/6430: 0x15–0x17 xung đỏ, đồ 0, 19, 20
- 6431: Flash với một khung hình cho mỗi lần nhảy, 17 bản đồ
- Ngoài ra 6428, 6432–6435 cho các hiệu ứng ánh sáng, dung nham và vũ trụ
- **Tổng cộng**: 67 bản đồ có hoạt ảnh bằng bảng màu hiển thị. 28 ảnh tham chiếu phụ trợ khác, nhưng không có pixel nào có số màu tương ứng trong tập bản đồ, đây là các tham chiếu không hợp lệ (4, 23, 65, 104, 111, 113–118, 137, 140–155). Để biết danh sách từng bản đồ, hãy xem [Danh sách bản đồ chiến thuật](tactical-maps.md).
- **Ví dụ**: Map 20 tập đầu tiên của nữ chính, 6422 là dòng sông (66 ô vuông), còn 6429 là xung đỏ 6 ô vuông.

### 3.3 Cập nhật khác

| Năng động | Cơ chế | Quy mô |
| --- | --- | --- |
| Xoay thuộc địa | Bản đồ vũ trụ chế độ byte 1 (atlas 6229) sao chép khung tiếp theo 6235 (64×48, tổng cộng 8 khung hình) vào tập bản đồ (208,0) cứ sau 27 tích tắc | 77 bản đồ vũ trụ được kích hoạt; 39 chứa 1–5 phiên bản thuộc địa, mỗi ô 4×3, tất cả đều được đồng bộ hóa |
| Thay đổi toàn bộ hình ảnh (3D34) | Bố cục quá tải, tập bản đồ, bảng màu, phụ trợ và thuộc địa; hai loại chuyển đổi băng tần và chuyển mạch ngay lập tức | Phong cách truyện tranh: cảnh 103 cắt theo trình tự 121, 123...136, cảnh 105 cắt theo trình tự 141...156, mỗi bước 18-29 khối khác nhau. Biến thể cục bộ: 37→39 có 5 ô khác nhau |
| Bố cục giống nhau nhưng các bảng màu khác nhau | Bố cục giống nhau nhưng các bảng màu khác nhau | 0/138/139 là cảnh đêm và ban ngày; 60→64 tối đi do ánh sáng đỏ; 157 toàn màu đen |
| Rung (3D36) | Cứ để ống kính |
| Làm mờ dần trong và ngoài (3D3B) | Lớp phủ khối màu toàn màn hình mà không thay đổi bảng màu | — |
| Cuộn | Độ lệch ống kính bằng pixel nguyên, không cuộn UV | — |
| Thu phóng tổng quan | `800943E0` Thu nhỏ toàn bộ bản đồ xuống 266×200, bỏ qua đường viền 2 khung bên ngoài (ô 1 / 2) | Nhấn C-phải để vào bản đồ nhàn rỗi (máy thực tế 2026-09-27) |
| Bảng địa hình | `801E2D54` Phóng to ô con trỏ khoảng 2,3 lần | — |

Thứ tự vẽ: Bản đồ là lớp thấp nhất của cảnh chiến thuật (ưu tiên 0x93), tiếp theo là điểm nổi bật phạm vi, đơn vị, hoạt ảnh bản đồ, cửa sổ và lớp phủ toàn màn hình. Ngoài ra, `800945D4` còn được dùng để vẽ các đường nồng độ 610–612.

### 3.4 Tác động lên HD

Kết luận: Thay thế băm kết cấu sẽ không hoạt động ở đây. Nội dung TLUT hoặc atlas của màu chu kỳ và lưới thuộc địa thay đổi theo mỗi bước nhảy và hàm băm cũng vậy. Bản đồ chiến thuật cần được tiếp quản toàn bộ. Để triển khai và xác minh mẫu bản đồ 20, hãy xem [Quy hoạch HD §3](../design/hd-pipeline-plan.md#3-战术地图).

Ý tưởng cốt lõi là "bản đồ cơ sở độ phân giải cao + bản đồ số màu độ phân giải cao + bảng màu thời gian thực của khung trò chơi". Ưu điểm là không cần phải thực hiện lại logic vòng tròn: trò chơi ghi gì vào bảng màu thì màn hình độ phân giải cao sẽ hiển thị tương ứng. Theo ý tưởng này, các loại động lực học khác nhau được xử lý như sau:

| Năng động | Đang xử lý | Nội dung HD bắt buộc |
| --- | --- | --- |
| Mặt nước, ánh sáng, dung nham, xung đỏ, đèn flash (chu kỳ bảng màu) | Trình đổ bóng kiểm tra bảng khung theo số màu, đồng thời điều khiển cổng thời gian và tạm dừng phù hợp với phiên bản gốc | Một bản đồ số màu cho mỗi bản đồ, không yêu cầu nội dung theo từng khung hình |
| Cảnh đêm, ban ngày, tối, toàn màu đen (3D34 có cùng bố cục nhưng thay đổi bảng màu) | Cơ chế tương tự tự động có hiệu lực | Không có |
| Thay thế bản đồ theo phong cách truyện tranh, biến thể cục bộ (thay đổi bố cục 3D34) | Hãy coi như một bản đồ khác | Dựa trên bước trước, chỉ vẽ lại 18–29 ô đã thay đổi |
| Xoay thuộc địa | Xếp chồng lên một sprite 8 khung, số khung là `80178C6D` | 8 khung hình; được tạo cùng nhau trong một yêu cầu để đảm bảo tính nhất quán giữa các khung |
| Rung, cuộn | Đọc offset ống kính cho từng khung hình, tự động theo dõi | Không có |
| Làm mờ dần trong và ngoài | Lớp phủ được vẽ trên bản đồ và không bị ảnh hưởng | Không có |
| Thu phóng tổng quan | Cùng một bộ họa tiết được rút gọn và vẽ, dựa vào mipmap để đảm bảo chất lượng hình ảnh (đã thực hiện) | Không có |
| Bảng địa hình | Phiên bản đầu tiên giữ nguyên bản vẽ gốc và sẽ lấy mẫu hình chữ nhật phụ của hình ảnh độ phân giải cao trong tương lai | Không có |

Các điểm khác:

- **Lọc theo tài nguyên**: `800945D4` cũng được dùng để vẽ các đường nồng độ 610–612. Khi tiếp quản phải xác định theo số tài nguyên bố cục bản đồ để tránh tiếp quản nhầm.
- **Khóa nội dung**: Nội dung HD được khóa theo số bố cục. Bảng màu không được nhập và màu được xác định khi chạy.
- **Vùng hoạt ảnh không được bàn giao cho AI để vẽ lại**: Bản đồ số màu của mặt nước và các khu vực khác được phóng to bằng thuật toán chỉ sao chép số màu gốc (MMPX dùng cho mẫu, bộ công cụ tương tự như nhận dạng cơ thể). Phương pháp này cũng giống như việc bảo vệ bờ biển trên bản đồ thế giới. Bằng cách này, hình dạng của họa tiết nước sẽ mượt mà hơn và chuyển động giống như phiên bản gốc. AI chỉ chịu trách nhiệm về các chi tiết ở vùng tĩnh.
- **Nước tăng cường tùy chọn**: Kết cấu chi tiết chuyển động chậm được phủ trong bóng đổ, với các màu vẫn được lấy từ bảng khung hiện tại. Đây là cách biểu diễn mới và phải được bật tắt riêng biệt.

### 3.5 Bản đồ thế giới

Không có mặt biển hoạt hình dưới bản đồ thế giới. Vùng biển trong suốt hiển thị màu màn hình rõ ràng RGB(0,55,90), được đặt bởi `801C3490`. Nếu muốn vẽ mặt biển ở bản HD thì là nội dung mới, cần bật tắt riêng, không thể tính là phục hồi. Chỉ có khu vực 5599 sẽ vẽ bầu trời đầy sao 5582 ở slot 0.

## 4. Mô hình Đám mây Alibaba (tài liệu chính thức 23/09/2026)

Giá là giá gốc ở Bắc Kinh, bằng Nhân dân tệ, không giảm giá.

| Người mẫu | Mục đích | Hạn chế chính | Giá | Tài liệu |
| --- | --- | --- | --- | --- |
| `qwen-image-3.0` | Chỉnh sửa, 1–3 hình ảnh đầu vào | Diện tích đầu ra 512²–20482, tỷ lệ 1:8–8:1; không minh bạch; 20 vòng/phút | 0,02 + 0,18/hình (1K và 2K đồng giá) | [Thẻ](https://help.aliyun.com/zh/model-studio/qwen-image-3-0) |
| `qwen-image-3.0-pro` | Tương tự như trên | Tương tự như trên; 5 vòng/phút | 0,02 + 0,25 (1K) / 0,50 (2K) | [Thẻ](https://help.aliyun.com/zh/model-studio/qwen-image-3-0-pro) |
| `wan2.7-image-pro` / `wan2.7-image` | Chỉnh sửa, tối đa 9 hình ảnh tham khảo | Nhập 240–8000 px, 8:1; PNG không hỗ trợ tính minh bạch; chỉnh sửa đầu ra lên tới 2K | 0,50 / 0,20 | [Tài liệu](https://help.aliyun.com/zh/model-studio/wan-image-edit) |
| `qwen-image-2.0(-pro)` | Chỉnh sửa | Tương tự như 3.0 | 0,20 / 0,50 | [Thẻ](https://help.aliyun.com/zh/model-studio/qwen-image-2-0-pro) |
| VIAPI `MakeSuperResolutionImage` | Điểm vượt mức bình thường 1–4x | Cạnh dài đầu vào ≤ 1920; **Đầu vào RGBA vẫn trong suốt** | Miễn phí 100 lần đầu tiên mỗi tháng, sau đó 0,02 | [API](https://help.aliyun.com/zh/viapi/developer-reference/api-px24vm) |
| VIAPI `GenerateSuperResolutionImage` | Điểm vượt mức sáng tạo 1–4 lần | Đầu vào ≥ 642, tỷ lệ 2:1 | 0,06 | [API](https://help.aliyun.com/zh/viapi/developer-reference/api-generated-image-super-score) |
| `wanx2.1-imageedit` (phiên bản cũ) | Siêu điểm, phóng to, vẽ lại theo mặt nạ | Mỗi bên ≥ 512 | 0,14 | [API](https://help.aliyun.com/zh/model-studio/wanx-image-edit-api-reference) |
| `image-out-painting` | Hình ảnh mở rộng, có thể chỉ định 16:9 | 512–4096 mỗi bên | 0,18 | [API](https://help.aliyun.com/zh/model-studio/image-scaling-api) |
| `SegmentHDCommonImage` / `RefineMask` | Cắt bỏ / Tinh chỉnh mặt nạ | Chú thích phân đoạn phổ quát không áp dụng cho hình ảnh hoạt hình | 0,007 | [Cắt](https://help.aliyun.com/zh/viapi/developer-reference/api-universal-hd-split) |
| `wan2.2-kf2v-flash` | Tạo video từ khung hình đầu tiên và cuối cùng | Đã sửa lỗi 5 giây, không minh bạch | 480P 0,10/giây | [API](https://help.aliyun.com/zh/model-studio/image-to-video-by-first-and-last-frame-api-reference) |
| `Tripo/Tripo-P1.0`, `Tripo/Tripo-H3.1` | Vincent, Tusheng 3D, đầu ra GLB | P1.0 20.000 mặt; không có thông số kiểu dáng hoặc low-poly | 1,4–4,2/lần | [Hướng dẫn](https://help.aliyun.com/zh/model-studio/tripo-3d-generation-guide) |
| `qwen3-vl-flash` / `qwen3.7-plus` | Hiểu biết trực quan, QA tự động | Đầu vào nhiều hình ảnh | 0,15 / 1,5 trên một triệu token, hoặc 2/8 (đầu vào / đầu ra) | [Hình ảnh](https://help.aliyun.com/zh/model-studio/vision) |

Những hạn chế ảnh hưởng đến dự án này:

- **Kênh minh bạch**: Các mô hình tạo không nhận cũng như không minh bạch đầu ra. Alpha tiếp tục được lấy từ mặt nạ hình ảnh gốc ([`portrait_matte.py`](../../tools/hd_ai/portrait_matte.py) cho hình đại diện). Chỉ có siêu điểm bình thường mới có thể trực tiếp giữ lại RGBA.
- **Kích thước tối thiểu**: Lưới và biểu tượng 16×16 thấp hơn mức đầu vào tối thiểu của tất cả các dịch vụ sẽ được gửi dưới dạng tập bản đồ hoặc toàn bộ hình ảnh và được người hàng xóm gần nhất phóng to trước trước.
- **Tỷ lệ**: Tiêu đề chương có tỷ lệ khoảng 7,9:1, chỉ được chấp nhận bởi wan2.7 và qwen 3.0; sản xuất vượt quá giới hạn 2:1.
- **Ngoại tuyến**: Đài quốc tế thông báo loạt phim cũ `qwen-image-edit` và `qwen-image` sẽ ngoại tuyến vào ngày 10-10-2026. Bản thay thế là 3.0, không ảnh hưởng đến bốn mẫu máy được thử nghiệm trong điểm chuẩn. Nội dung thông báo trong nước không được ghi lại.
- **Chi tiết giao diện**: Tài liệu wan2.7 liệt kê `prompt_extend` và `negative_prompt` là không được hỗ trợ, trong khi [`aliyun.py`](../../tools/hd_ai/aliyun.py) vượt qua `prompt_extend:false` cho tất cả kiểu máy. Nó cần được thay đổi trước đợt yêu cầu wan2.7 tiếp theo.
- **9-08 Lỗi siêu điểm**: 403 Nó có thể liên quan đến tiền tố đường dẫn tải lên của nhóm tạm thời, nhưng không có xác nhận. Trong tương lai, bạn sẽ chuyển sang tải SDK cục bộ lên hoặc xây dựng OSS của riêng mình ở khu vực Thượng Hải.
- **Auto QA**: Chủ yếu dựa trên các chỉ số xác định (mặt nạ IoU, chênh lệch màu sắc sau khi thu nhỏ về kích thước ban đầu). Mô hình trực quan chỉ đưa ra phán đoán thứ hai và không đóng vai trò là sự chấp nhận duy nhất.

## 5. Ước tính chi phí sơ bộ

Được tính toán dựa trên giá gốc và thành công duy nhất, không bao gồm số lần thử lại. Các hạng mục sáng tạo dựa trên 2 ứng cử viên cho mỗi bức ảnh. LoRA không được đào tạo.

| Danh mục | Số lượng yêu cầu | Người mẫu | Tổng phụ (nhân dân tệ) |
| --- | ---: | --- | ---: |
| Avatar + Avatar của nhân vật chính | 304 × 2 | `qwen-image-3.0` | 122 |
| Nền Interfield, ngọn lửa, bầu trời đầy sao | 10 × 2 | `qwen-image-3.0-pro` 2K / Điểm siêu sáng tạo | 11 |
| Hoạt hình hiệu suất bản đồ | 21 × 2 | `wan2.7-image-pro` | 21 |
| Atlas địa hình chiến thuật | 9 | Siêu điểm bình thường | 0,2 |
| Nhận dạng cơ thể | Khoảng 1.300 hình ảnh | Thuật toán cục bộ, không cần điều chỉnh giao diện | 0 |
| Kiểm tra chất lượng tự động | Khoảng 800 lần | `qwen3-vl-flash` | Khoảng 8 |
| **Tổng phạm vi hiện tại** | | | **Khoảng 162** |
| Tùy chọn: Tinh chỉnh tất cả các bản đồ chiến thuật | Khoảng 500 cửa sổ | `qwen-image-3.0-pro` 2K | Thí sinh mỗi vòng +260 |
| Bị đình chỉ: Cắt vào | 32 × 2 | `wan2.7-image-pro` | 32 |
| Đình chỉ: Yêu tinh chiến đấu, Yêu tinh vũ khí, Khiên | 353 | Siêu điểm bình thường (được tạo cộng 177) | 7 |
| Đang chờ: Kết cấu nền chiến đấu 3D | 49 | Siêu điểm sáng tạo | 3 |

Hình đại diện là mục lớn nhất nhưng lý do không phải là độ phân giải: `qwen-image-3.0` có giá trên mỗi bức ảnh, 1K và 2K có cùng mức giá, cả hai đều là 0,20 nhân dân tệ. Chi phí đến từ số lượng và số lượng ứng viên: 304 thẻ × 2 ứng viên. Theo lộ trình:

| Lộ trình Avatar | Đơn giá | Tổng cộng 304 ảnh | Hiệu ứng |
| --- | ---: | ---: | --- |
| Vẽ lại sáng tạo, 2 ứng cử viên (trên bảng) | 0,20 | 122 | Điền các chi tiết mới; có nguy cơ bị trôi dạt danh tính, vì vậy hãy xem xét từng cái một |
| Vẽ lại sáng tạo, 1 ứng cử viên | 0,20 | 61 | Tương tự như trên |
| Siêu điểm sáng tạo VIAPI | 0,06 | 18 | Ít chi tiết được thêm vào hơn so với vẽ lại và danh tính về cơ bản không thay đổi |
| VIAPI siêu điểm bình thường | 0,02 (100 lần đầu tiên mỗi tháng là miễn phí) | Khoảng 4 | Chỉ để làm rõ chứ không điền chi tiết |
| Mô hình siêu phân giải hoạt hình cục bộ | 0 | 0 | Tương tự như siêu phân giải thông thường; cần tải model và môi trường chạy |

Nó cũng có thể được trộn lẫn: tất cả các avatar đều được vẽ bằng điểm siêu trước và chỉ các nhân vật chính được vẽ lại một cách tự nhiên.

Không có mô hình chỉnh sửa nào có sẵn rẻ hơn 0,20 nhân dân tệ trên Alibaba Cloud (kiểm tra trang chính thức vào ngày 23-09-2026):

- [`z-image-turbo`](https://help.aliyun.com/zh/model-studio/z-image-turbo) 0,10 nhân dân tệ, nhưng chỉ có thể sử dụng văn bản để tạo hình ảnh và không thể nhập hình ảnh gốc.
- `wanx2.1-imageedit` 0,14 nhân dân tệ, là phiên bản cũ, chức năng siêu điểm không hơn gì siêu điểm VIAPI.
- Hạn ngạch miễn phí cho người dùng mới không được ghi trên các trang này. Bạn cần xác nhận nó trên bảng điều khiển.

**Xử lý hàng loạt câu đố**: `qwen-image-3.0` Được định giá theo từng mảnh, đầu ra 1K và 2K có cùng mức giá và diện tích đầu ra tối đa là 2048². Do đó, bạn có thể đặt nhiều hình đại diện vào một lưới và nhập chúng, yêu cầu một hình ảnh có kích thước 2048² mỗi lần, sau đó cắt nó.

| Chính tả | Đầu ra trên mỗi lưới | Đơn giá mỗi avatar | Tổng cộng 304 ảnh |
| --- | --- | ---: | ---: |
| Tờ đơn (thông lệ hiện tại) | Tối đa 20482 | 0,20 | 61 (1 ứng viên) |
| 2×2 | khoảng 10242 | 0,05 | khoảng 15 |
| 3×3 | khoảng 680² | 0,022 | khoảng 7 |
| 4×4 | Xấp xỉ. 512² | 0,013 | Xấp xỉ. 4 |

Mục tiêu là 3842 (4x), vì vậy 3×3 cũng sẽ đủ. Rủi ro là mô hình có thể kết hợp các đặc điểm của các ô liền kề với nhau hoặc xử lý từng ô một cách không nhất quán. Các phương pháp giảm thiểu:
- Để lại không gian màu trung tính giữa các lưới;
- Các ký tự của cùng một tác phẩm được xếp trên cùng một tờ;
- Các từ gợi ý chỉ ra rằng mỗi lưới là độc lập.

Phong cách nhân vật trong cùng một bức tranh sẽ tự nhiên nhất quán, đây thực sự là một lợi ích. 2×2 đã được thử và thành công: `portrait_batch.py` nhận được tất cả 300 trong 75 yêu cầu.

Bản thân số tiền không phải là điểm nghẽn, chi phí chính nằm ở việc xem xét và kiểm soát tính nhất quán. Trước khi yêu cầu hàng loạt, hãy cố định các từ đầu vào và lời nhắc theo quy tắc của [Điểm chuẩn](../design/hd-ai-benchmark.md) và không gửi các yêu cầu trùng lặp nếu đã có bản ghi yêu cầu.

## 6. Đang được điều tra

1. Kiểm tra trực quan màn hình nào và trình kết xuất nào sử dụng từng danh mục. Đặc biệt là các hiệu ứng đặc biệt chung atlas 4861, các sprite cơ thể nhỏ 4923–4954 (được nghi ngờ là vũ khí trên bản đồ hoặc khi hoạt ảnh chiến đấu bị tắt) và đoạn atlas hiệu ứng đặc biệt 5335–5374.
2. Ghép nối bảng màu: 49 bản đồ nền 3D so với 112 bảng màu, 9 bản đồ địa hình so với 27 bảng màu. Điều này phải được xác nhận từ bảng ràng buộc và không thể đoán được dựa trên các số liền kề.
3. Cần phải xác minh máy thật: 1 lần nhảy bằng vài VI; liệu menu và chu trình bảng màu có bị treo trong khi tạm dừng hay không; liệu có thể nhập thu phóng tổng quan vào các trò chơi thông thường hay không; thời gian chờ đợi giữa mỗi bước của truyện tranh; liệu 15 tham chiếu phụ không có pixel tương ứng có thực sự không có thay đổi trên màn hình hay không.