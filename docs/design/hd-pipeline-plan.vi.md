> **Ngôn ngữ / Language:** [Tiếng Việt](hd-pipeline-plan.vi.md) · [English](hd-pipeline-plan.en.md) · [中文](hd-pipeline-plan.md)

# HD: Hiện trạng, phương thức truy cập và theo dõi

Soạn thảo ngày 23-09-2026, viết lại theo thực tế triển khai ngày 24-09-2026. Ranh giới sản phẩm tuân theo [Lộ trình MOD tích hợp](mod-roadmap.md) §6 (Bản gốc / HD có thể được khôi phục từng mục và hình ảnh gốc sẽ được sử dụng nếu thiếu mục nào). Để biết toàn bộ kho tài nguyên ROM và lựa chọn mô hình Đám mây Alibaba của từng loại, vui lòng xem [Kho tài sản HD](../data/hd-asset-inventory.md); để biết từng hiệu ứng động của bản đồ chiến thuật, vui lòng xem [Danh sách bản đồ chiến thuật](../data/tactical-maps.md).

Danh sách nghệ thuật là `content/art/stage1-hd.json`. Hồ sơ phát triển mặc định là `images: original`. HD cần được bắt đầu bằng `--images hd` hoặc nhấn F6 trong trò chơi.

Gói tự sử dụng Full HD (24/09/2026) bắt đầu từ HD. Để biết phương pháp, hãy xem [bản dựng macOS · Gói tự sử dụng Full HD](../native/macos-release.md#全-hd-自用包):
- [`prepare_hd_bundle.py`](../../tools/release/prepare_hd_bundle.py) Biên soạn danh sách nghệ thuật và sao chép trong gói mô hình tàu đã được xác minh và gói 5600 điểm;
- `package_macos.py --hd` Đưa nó vào ứng dụng; trình khởi chạy nhìn thấy nó và mở gói HD và hai gói mô hình.

Gói này chỉ dành cho sử dụng cục bộ và không được phân phối. Bản đồ chiến thuật (từ 27-09-2026) được bao gồm trong gói cùng với danh sách nghệ thuật và bản đồ cơ sở được lưu dưới dạng JPEG.

## 1. Tình hình hiện tại

| Danh mục | Thực hành | Trạng thái | Tài liệu |
| --- | --- | --- | --- |
| Avatar nhân vật (300 hình, 4 nhân vật chính còn lại) | Toàn bộ bức tranh được chủ nhà vẽ, 768×768 | Đã truy cập | [Hình đại diện nhân vật HD](../native/native-portraits-hd.md) |
| Nền liên trường (8 ảnh, sáng/tối) | Chủ nhà vẽ toàn bộ bức tranh | Đã kết nối | [Nền liên trường HD](../native/native-backgrounds-hd.md) |
| Tiêu đề Logo và ngọn lửa | Lưu trữ toàn bộ khung vẽ (cảnh sprite) | Đã kết nối | [Màn hình tiêu đề và hình ảnh văn bản cốt truyện](../native/native-title-and-story-images.md) |
| Menu tiêu đề, thẻ tiêu đề chương, mở đầu, kết thúc, ghi công | Văn bản gốc, ngôn ngữ sau | Đã kết nối | Tương tự như trên |
| Bản đồ thế giới câu chuyện (bề mặt 5602–5606, vũ trụ 5599) | Thay thế hàm băm RT64, lát cắt 512 px; bầu trời đầy sao được vẽ toàn bộ | Đã truy cập | [bản đồ thế giới câu chuyện HD](../native/native-worldmap-regions-hd.md) |
| Bản đồ thế giới tàu, địa danh, đường đi | Người mẫu bản địa | Đã truy cập | [Mô hình cắt cảnh bản đồ thế giới HD](../native/native-ship-model.md) |
| 5600 điểm đánh dấu bản đồ lô | Người mẫu bản địa | Đã truy cập | [Thay thế mẫu](../native/native-model-replacement.md) |
| Đường viền hộp thoại | Thay thế băm RT64, vẽ lại theo mã thiết kế ban đầu | Đã kết nối | [Đường viền HD của hộp thoại](../native/native-dialogue-runtime-hd.md) |
| Bản đồ chiến thuật (131 bố cục được sử dụng, bao gồm 22 biến thể 3D34) | Toàn bộ bản đồ được chủ nhà vẽ, bản đồ số màu + bảng màu thời gian thực; Bao phủ 8 khung hình của thuộc địa; bảng địa hình và tổng quan có cùng bản đồ cơ sở | Danh sách nghệ thuật và gói HD đã được kết nối (27/09/2026; gói công khai cũng sẽ được đưa vào từ 28/09/2026) | §3, [Lập kế hoạch gói thế hệ](tactical-map-hd-kit.md) |
| Nhận dạng máy bay (320 biểu tượng đơn vị bản đồ) | MMPX×2 → ESRGAN cục bộ → Lượng tử hóa cứng 32 → Bản đồ màu MMPX×2, 64×64; Thay thế băm RT64, một bản sao cho mỗi trại | Đã truy cập (gói cục bộ, không có trong gói công cộng) | [HD nhận dạng máy bay](unit-icon-hd.md) |
| Chiến đấu: họa tiết, hiệu ứng đặc biệt, cut-in, nền 3D | — | Đình chỉ (quyết định ngày 23-09-2026) | Tương tự như trên |

## 2. Bốn đường dẫn truy cập

### Lưu trữ toàn bộ bản vẽ

Được sử dụng cho những cảnh "bản gốc chia một bức tranh lớn thành nhiều phần": hình đại diện, hình nền giữa các cảnh, khung tiêu đề và bản đồ chiến thuật.

- Trò chơi ra lệnh chunking như bình thường.
- Máy chủ nhận ra bức tranh nào đang được vẽ lần này, loại bỏ các khối ban đầu và vẽ toàn bộ bức tranh có độ phân giải cao cùng một lúc ở cùng một vị trí và theo cùng thứ tự vẽ của cùng một bộ đệm lệnh trong RT64 (lớp của toàn bộ bức tranh đã được thay đổi thành chùm, xem [Kế hoạch chuyển ba nền tảng](three-platform-port.md) X1).
- Ưu điểm: Không có đường nối giữa các khối; các phiên bản có bảng màu khác nhau không cần phải băm từng khối; hình ảnh không bị giới hạn bởi phương pháp cắt ban đầu.
- Xác định hook vẽ gốc của RT64 (`NativeMeshHooks`). Cả TRI1/TRI2 và cuộc gọi văn bản đều phân loại và mỗi mô-đun được treo phía sau nó thành một chuỗi.
- Thực hiện:
- Hình đại diện: `native_portrait.cpp`
- Nền liên trường: `native_background.cpp`
- Tiêu đề và các họa tiết cảnh khác: `native_sprite.cpp`
- Bản đồ chiến thuật: `native_map.cpp`

### Thay thế băm kết cấu RT64

Được sử dụng cho các cảnh vốn độc lập với các kết cấu nhỏ và hàm băm ổn định: các khối bề mặt bản đồ thế giới 64 px, các đối tượng vũ trụ, các lát hộp thoại.

- Khóa là hàm băm nội dung RT64 v5, được tính ngoại tuyến bởi [`rt64_hash.py`](../../tools/hd_ai/rt64_hash.py).
- Tệp kê khai cho phép bốn danh mục: `worldmap`, `frame`, `space`, `icon`; `icon` (nhận dạng máy bay) được vẽ lại từ các pixel gốc và sẽ được đưa vào gói HD công khai cùng với các danh mục khác từ ngày 28 tháng 9 năm 2026.
- Không sử dụng phương pháp này nếu bảng màu thay đổi, cùng một khối xuất hiện ở nhiều nơi hoặc nếu thay thế nội dung bằng khối để lại các đường nối.

### Mô hình gốc

Đối với danh sách hiển thị 3D: 5600 điểm đánh dấu, tàu bản đồ thế giới và các địa danh. `native_marker.cpp` Xác định DL gốc, loại bỏ nó và vẽ lưới máy chủ.

### Văn bản gốc

Văn bản được sử dụng để nướng trong hình ảnh: menu tiêu đề, thẻ tiêu đề chương, phần mở đầu, phần kết thúc, phần ghi công. Văn bản được sắp xếp lại theo ngôn ngữ đọc và các chuyển động chia tỷ lệ, xoay và lật của phiên bản gốc được giữ lại.

## 3. Bản đồ chiến thuật

Bản đồ có chu kỳ bảng màu (nước, ánh sáng, dung nham), khung kết cấu thuộc địa và hoán đổi bản đồ đầy đủ 3D34, xem [Danh sách bản đồ chiến thuật](../data/tactical-maps.md) để biết chi tiết. Kết cấu ở những khu vực này thay đổi theo từng bước nhảy và tính năng thay thế hàm băm không hoạt động ở đây, vì vậy máy chủ sẽ vẽ toàn bộ khung và màu được lấy từ bảng khung của trò chơi.

### Thời gian chạy (`src/host/native_map.cpp`)

1. **Hook**: Sau khi chức năng vẽ bản đồ `800945D4` được thực thi, `game_hooks.cpp` bàn giao phạm vi danh sách hiển thị, vị trí và bản ghi phụ được ghi lần này cho máy chủ.
2. **Nhận dạng**: Máy chủ đọc số bố cục từ bản ghi phụ và chỉ tiếp quản bố cục bản đồ với nội dung HD; các họa tiết khác được vẽ bởi cùng một trình kết xuất, chẳng hạn như các đường tập trung, không di chuyển.
3. **Viết lại**: Nó sẽ không được viết lại ở chế độ ban đầu, khi không có nội dung hoặc khi nhận dạng không thành công. Mặt khác:
- Đọc địa chỉ TLUT và chụp 256 màu của khung hình hiện tại;
- Tính toán tọa độ bản đồ bằng cách sử dụng hộp giới hạn của mỗi hình chữ nhật và độ lệch camera (gốc khe + `8010F5D4/D8`);
- Để lại một hình chữ nhật đã đánh dấu trong danh sách hiển thị và để trống phần còn lại. Các lệnh tải kết cấu và trạng thái không thay đổi.
4. **Vẽ**: RT64 gọi lại máy chủ khi xử lý hình chữ nhật này và máy chủ tính toán (`src/host/shaders/HdMapPS.hlsl`) `底图 + (当帧色 − 参考色)[色号]` bằng pixel. Khi bảng màu không thay đổi, bản đồ cơ sở vẫn giữ nguyên; khi mặt nước thay đổi khung hình và bảng màu thay đổi, màu sắc sẽ theo trò chơi.
5. **Tài sản**: `SRW64_HD_MAPS` trỏ tới thư mục đầu ra của `tools/hd_ai/tactical_map_hd.py export`. Một thư mục con trên mỗi bản đồ chứa bản đồ cơ sở 4x `base.png`, bản đồ màu 4x `index.png` và `meta.json` với bảng màu tham chiếu.

Cạm bẫy: `screenScale`/`screenOffset` do RT64 vẽ cho hình chữ nhật có liên quan đến phạm vi của chính hình chữ nhật đó chứ không phải toàn bộ màn hình. Toàn bộ bản đồ phải được chuyển trực tiếp sang tọa độ N64 toàn màn hình, nếu không sẽ bị kéo giãn theo chiều ngang và “thở” khi cuộn.

Xác thực mẫu bản đồ 20:
- Chụp ảnh màn hình ở cùng vị trí và sau khi cuộn xuống phía dưới. Độ lệch đăng ký giữa phiên bản HD và phiên bản gốc sẽ bằng 0 trên toàn bộ màn hình.
- Nhịp điệu màn hình phía trên giống với phiên bản gốc: cứ 33 ms một khung hình, tối đa 38 ms.
- Khả năng phán đoán trôi chảy không còn bị ảnh hưởng bởi chẩn đoán: "Chẩn đoán hoàn chỉnh" chụp ảnh màn hình định kỳ 5K hình ảnh và xuất bộ nhớ đã bị xóa vào ngày 01/10/2026 (nó sẽ gây ra độ trễ 200-270 ms).

### Sản xuất ngoại tuyến (`tools/hd_ai/tactical_map_hd.py`)

1. **`prepare`**: Tạo bản đồ mã màu 1x và hình ảnh gốc theo bố cục, tạo mặt nạ hoạt hình và mặt nạ viền, sử dụng MMPX để phóng to bản đồ mã màu 4 lần và đóng băng yêu cầu.
2. **Yêu cầu**: `python -m tools.hd_ai.aliyun` Gửi một lần, mỗi thư mục đầu ra đều có giới hạn ngân sách.
3. **`compose`**：
- Khuếch đại tổng thể và chuyển đổi nghịch đảo của đầu ra mô hình được trang bị theo hai trục. Qianwen sẽ đặt khoảng 0,2–0,5% nội dung.
- Bảo toàn màu sắc: Chỉ lấy các chi tiết tần số cao của mô hình, còn các màu tần số thấp tiếp tục được sử dụng trong ảnh gốc.
- Kết quả của việc không sử dụng mô hình cho vùng hoạt ảnh và đường viền ngoài.
- Báo cáo so sánh đầu ra và xem trước vòng lặp mặt nước.
4. **`export`**: Viết ra nội dung thời gian chạy.

Bản đồ 20 (448×512) có thể tạo toàn bộ bản đồ 1792×2048 trong một yêu cầu; lựa chọn cuối cùng là `qwen-image-3.0-pro`.

### Sẽ được thực hiện

Để sắp xếp lại gói thế hệ và danh sách bản đồ, bảng xác nhận phần tử động, bảng địa hình và phần tổng quan, vui lòng xem [Kế hoạch gói thế hệ bản đồ chiến thuật HD](tactical-map-hd-kit.md) (25-09-2026).

- **Làm mịn đường bờ biển**: Bản đồ số màu được phóng to theo pixel và đường bờ biển vẫn có bậc. Ranh giới cần được làm phẳng và sau đó căn chỉnh với vùng đất do AI vẽ ra.
- **Hình ảnh lớn được chia thành các cửa sổ**: 135 trong số 155 bố cục vượt quá 20482 sau khi được phóng to 4 lần. Chúng cần được tạo trong các cửa sổ riêng biệt, có lớp phủ chồng lên nhau, sau đó được kết hợp trong khu vực được bảo vệ.
- **Yêu tinh thuộc địa**: Bộ 8 khung hình, số khung là `80178C6D`.
- **Biến thể 3D34**: Dựa trên bước trước, chỉ vẽ lại lưới đã thay đổi.
- **Bảng điều khiển thu phóng và địa hình tổng quan**: Thu phóng tổng quan (`800943E0`) và Bảng điều khiển địa hình (`801E2D54`) vẫn vẽ lưới ban đầu.
- **Đơn hàng trước**: Đầu tiên hãy tạo bản đồ có vùng nước rộng (56, 13, 16, 46, 15), sau đó tạo hai chuỗi truyện tranh.

## 4. Công cụ sản xuất

| Công cụ | Mục đích |
| --- | --- |
| [`aliyun.py`](../../tools/hd_ai/aliyun.py) | Dừng việc gửi yêu cầu một lần: ghi bản ghi yêu cầu trước khi gửi, không thử lại POST, mỗi thư mục đầu ra có giới hạn ngân sách; `load_env` Đọc khóa DashScope trong `.env` |
| [`rom_images.py`](../../tools/hd_ai/rom_images.py) | Bảng ROM và giải mã bản đồ màu |
| [`pixel_scale.py`](../../tools/hd_ai/pixel_scale.py) | Chỉ sao chép ảnh phóng to pixel art của số màu gốc (MMPX, Scal2x) để sử dụng trong sơ đồ số màu và nhận dạng cơ thể |
| `portrait_batch.py`, `build_portrait_images.py`, `build_portrait_review_site.py`, `portrait_matte.py` | Avatar: Tạo câu đố 2×2, đăng ký từng khung hình, cắt bỏ, toàn bộ đầu ra và trạm xem lại hình ảnh |
| `background_hd.py` | Bối cảnh giữa các cảnh |
| `title_hd.py`, `flat_scene_hd.py` | Tiêu đề Logo, Ngọn lửa và Cảnh khối màu phẳng |
| `worldmap_surfaces.py`, `worldmap_space.py` | Vẽ bề mặt bản đồ thế giới và vũ trụ |
| [`dialogue_frame_asset.py`](../../tools/hd_ai/dialogue_frame_asset.py) | Cắt đường viền hộp thoại |
| `tactical_map_hd.py` | Bản đồ chiến thuật |

Quy trình chung: yêu cầu đóng băng → truyền đơn → đăng ký và bảo toàn màu sắc → tổng hợp hoặc cắt vùng được bảo vệ → xuất → danh sách cập nhật (đính kèm với SHA-256) → so sánh máy thực tế. Tất cả các biểu đồ, bản ghi yêu cầu và tệp trung gian đã tạo đều được đặt trong `assets/hd-ai/` không có trong git. Để biết mô tả thư mục, hãy xem `assets/README.md`.

## 5. Theo dõi

1. **Bản đồ chiến thuật**: Đã hoàn thành và truy cập (xem [Quy hoạch gói thế hệ](tactical-map-hd-kit.md) §6.5). Các tính năng duy nhất còn lại là làm mịn đường bờ biển và liệu gói công khai có tạo bản đồ màu từ ROM khi chạy hay không.
2. **ID cơ thể**: Đã truy cập ([ID cơ thể HD](unit-icon-hd.md)); bóng elip còn lại 687 không bị thay đổi.
3. **Trận đấu**: Đình chỉ. Khi khôi phục, các họa tiết và hiệu ứng đặc biệt được làm chủ theo tập bản đồ rồi cắt thành nhiều phần, đồng thời nền 3D được thay thế bằng họa tiết và thêm hình học gốc.
4. **Màn hình rộng**: Trong tương lai, toàn bộ bức tranh được vẽ có thể được vẽ rộng hơn 4:3, nhưng việc này phải được thực hiện sau khi triển khai vùng chứa màn hình rộng.