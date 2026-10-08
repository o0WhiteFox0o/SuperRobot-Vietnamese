> **Ngôn ngữ / Language:** [Tiếng Việt](tactical-map-hd-kit.vi.md) · [English](tactical-map-hd-kit.en.md) · [中文](tactical-map-hd-kit.md)

# Bản đồ chiến thuật HD: Sắp xếp lại danh sách, các yếu tố động và lập kế hoạch gói tạo image_gen

2026-09-25. Bản đồ nền HD của bản đồ chiến thuật được vẽ bằng image_gen của Codex (phương pháp tương tự như [Story World Map](../native/native-worldmap-regions-hd.md#改用-image_gen2026-09-25)). Bài viết này sắp xếp lại danh sách bản đồ theo tầm cỡ của "nội dung HD", xác nhận từng phần một cách giữ lại các phần tử động trên bản đồ ở chế độ HD, lập kế hoạch thành phần của gói thế hệ và đưa ra phương pháp bảng địa hình "gạch giả". Cơ chế thời gian chạy tuân theo [Quy hoạch HD §3](hd-pipeline-plan.md#3-战术地图) (mẫu bản đồ 20) và bạn có thể tìm thấy từng dữ liệu động trong [danh sách bản đồ chiến thuật](../data/tactical-maps.md).

Các con số trong bài viết này được tính bằng `build/content/map-dynamics.json` và ROM (phân chia cửa sổ được tính bằng tập lệnh một lần, xem §3.4) mà không cần chạy trò chơi.

## 1. Danh sách bản đồ (theo cỡ tài sản HD)

Nội dung thời gian chạy được khóa bằng **số bố cục** (`find_asset(layout)` của `native_map.cpp`) và bảng màu không được khóa. Vì vậy, đối tượng kiểm kê không phải là 158 bản ghi bản đồ mà là bố cục sẽ được vẽ:

| Tầm cỡ | Số lượng | Mô tả |
| --- | ---: | --- |
| Bản ghi bản đồ | 158 | bảng `map_assets` |
| Bố cục khác nhau | 154 | 0/138/139, 60/64, 66/157 Ba nhóm có bố cục giống nhau, chỉ thay đổi bảng màu, một nhóm HD sẽ tự động che |
| Xóa 25 ảnh không có tham chiếu tĩnh | 131 | Xem [Danh sách §5](../data/tactical-maps.md#5-未找到静态引用的-25-张) để biết danh sách; mặc dù 138/139 nằm trong số đó, nhưng nó có cùng bố cục với 0, vì vậy nhân tiện, nó ở đó |
| Trong số đó, biến thể 3D34 | 22 | Sử dụng biểu đồ gốc làm cơ sở, chỉ vẽ lại lưới đã thay đổi (§1.2), không phải toàn bộ hình ảnh riêng biệt |
| **Muốn vẽ toàn bộ bức tranh gốc** | **109** | 7 hình là màn hình đơn 320×240 |

### 1.1 Bản đồ gốc theo họ atlas

Mỗi album trong số 8 bức tranh đều mang phong cách hội họa. Các mẫu phong cách vẽ tranh của Image_gen được gia đình tặng:

| Bản đồ | Nội dung (nhìn hình và gọi tên) | Bản đồ gốc | Số bản đồ |
| --- | --- | ---: | --- |
| 6228 | Mặt đất: đồng cỏ, rừng, thành phố, đường bộ, sông biển | 60 | 0–6, 8–27, 29–33, 38, 40–43, 45–48, 51–59, 61–63, 65, 67–69, 71, 73, 119 |
| 6229 | Vũ trụ: bầu trời đầy sao, vành đai thiên thạch, thuộc địa, đống đổ nát | 37 | 75–78, 81–102, 104, 105, 107–111, 113–116 |
| 6230 | Bên trong pháo đài/căn cứ tiểu hành tinh: cấu trúc màu xám và lỗ đen | 5 | 7, 35, 37, 44, 72 |
| 6231 | Bề mặt mặt trăng: miệng núi lửa, bề mặt màu xám | 3 | 49, 50, 60 |
| 6232 | Tranh sa mạc và Nazca | 1 | 36 |
| 6233 | Mây nhìn ra bờ biển | 1 | 66 |
| 6234 | Thiên hà | 1 | 112 |
| 6236 | Bề mặt dưới những đám mây (màn hình đơn) | 1 | 74 |

Sơ đồ gốc màn hình đơn: 65, 66, 73, 74, 81, 116, 119.

### 1.2 biến thể 3D34 (22 ảnh)

Các biến thể có cùng kích thước với sơ đồ gốc, chỉ khác nhau ở một vài ô. Hộp giới hạn chênh lệch (lưới):

| đồ thị gốc → biến thể | số lưới chênh lệch | hộp giới hạn (lưới) | mô tả |
| --- | ---: | --- | --- |
| 109 → 121, 123, 125, 127, 129, 131, 133, 135, 136 | 38–46 | x14–52 × y8–28, 39×21 | Cảnh 103 truyện tranh, 9 bước chung một khung giới hạn |
| 111 → 141, 143 … 155 | 28–43 | Tăng dần từ 8×4 lên 22×4 (y12–15) | Cảnh 105 Truyện tranh, một dải phát triển theo chiều ngang |
| 111 → 156 | 42 | 26×10 (x12–37 × y6–15) | kết thúc chuỗi |
| 37 → 39 | 5 | 3×2 | Cảnh 134 |
| 116 → 117 | 17 | 7×4 | Cảnh 38, màn đơn |
| 90 → 118 | 22 | 8×5 | Cảnh 54 |
| 104 → 137 | 17 | 6×5 | Cảnh 97 |

Các số chẵn (120–134, 140–154) trong chuỗi không có tham chiếu tĩnh, vì vậy chúng ta sẽ không thực hiện điều đó ngay bây giờ; nếu tìm thấy bảng trạng thái `8021E240` của 3D34 loại 0 trong quá trình hoạt động, chúng sẽ bị cắt theo biến thể và chúng cũng sẽ được điền vào theo biến thể.

## 2. Bảng xác nhận phần tử động

Mỗi mục liệt kê cơ chế cơ bản, khả năng lưu giữ ở chế độ HD, nội dung bắt buộc và trạng thái trong mẫu bản đồ 20.

| # | Năng động | Cơ học Vani | Giữ HD | Tài sản | Trạng thái |
| --- | --- | --- | --- | --- | --- |
| 1 | Chu kỳ bảng màu: mặt nước, ánh sáng, dung nham, xung màu đỏ, bầu trời đầy sao nhấp nháy (có thể nhìn thấy 67 hình ảnh) | `8009CC0C` ghi màu khung tiếp theo vào bảng bản đồ ở mỗi lần nhảy; `800945D4` tải lại TLUT ở mỗi khung hình | Shader `底图 + (当帧色 − 参考色)[色号]`, nhịp điệu và điều khiển cổng tạm dừng nhất quán một cách tự nhiên với bản gốc | Mỗi bức tranh có bản đồ số màu 4x (MMPX, chỉ sao chép số màu gốc); khu vực vòng lặp chưa được bàn giao AI | Đã triển khai |
| 2 | Vòng lặp không hợp lệ (28 ảnh) | Tài nguyên vòng lặp được trích dẫn nhưng không có số màu tương ứng trong tập bản đồ | Cơ chế giống như 1, hình ảnh tự nhiên không chuyển động | Không có | Đã triển khai |
| 3 | Xoay thuộc địa (39 hình ảnh, 53 trường hợp) | Bản đồ vũ trụ của chế độ byte 1 sao chép khung tiếp theo 6235 (64×48, 8 khung) vào tập bản đồ (208,0) cứ sau 27 bước nhảy; số khung `80178C6D` | Một hình ảnh HD 8 khung hình được xếp chồng lên bản đồ cơ sở; vị trí của phiên bản được tính từ bố cục khi xuất số lưới (chiếm 12 vùng này của tập bản đồ), ghi vào `meta.json` | Hình ảnh 8 khung hình (§3.3) | Sẽ được thực hiện |
| 4 | Thay đổi bố cục 3D34 (22 biến thể) | Bố cục quá tải, tập bản đồ, bảng màu, aux, thuộc địa | Biến thể là một tài sản khác, được tự động chuyển đổi theo số bố cục | Biến thể chỉ vẽ lưới thay đổi (§3.3) | Thời gian chạy được hỗ trợ; cần phải xác minh xem hai bức ảnh có được vẽ trong cùng một khung trong quá trình chuyển đổi dải hay không (§7) |
| 5 | 3D34 Bảng màu thay đổi bố cục giống nhau (cảnh đêm/ban ngày, đèn đỏ → tối dần, toàn màu đen) | Thay đổi tài nguyên bảng màu | Cơ chế tương tự như 1: chuyển màu theo số màu pixel theo pixel | Không có | Đã triển khai |
| 6 | Cuộn, rung (3D36) | Ống kính bù pixel số nguyên, độ rung là ống kính X xoay | Nguồn gốc khe đọc từng khung + `8010F5D4/D8` | Không có | Đã triển khai |
| 7 | Làm mờ dần trong và ngoài (3D3B) | Lớp phủ khối màu toàn màn hình | Được vẽ trên bản đồ, không bị ảnh hưởng | Không có | Đã triển khai |
| 8 | Chia tỷ lệ tổng quan | `800943E0` Tính tỷ lệ, `800945D4` vẽ toàn bộ hình ảnh thành 266×200 với byte chế độ khác 0 (bản ghi phụ + 3), bỏ qua đường viền 2 khung bên ngoài | Bản đồ cơ sở tương tự được vẽ ở kích thước giảm; mipmap là bắt buộc | Không có | Việc cần làm (§5) |
| 9 | Bảng địa hình | `801E2D54` Lấy lưới con trỏ ra khỏi tập bản đồ và phóng to lên 37×37 | Cắt khối 64×64 của lưới con trỏ từ toàn bộ bản đồ cơ sở HD và sử dụng cùng một trình đổ bóng | Không có | Việc cần làm (§4) |
| 10 | Đường tập trung 610–612 | Cùng một ngăn kéo `800945D4` | Được xác định theo số bố cục, không tiếp quản | Không có | Đã triển khai |
| 11 | 2 viền đậm ở vòng tròn bên ngoài (gạch 1/2) | Một phần của bố cục | Không được bàn giao cho AI; được vẽ bằng bản đồ số màu + bảng màu (tức là khuếch đại pixel) | Không có | Đã triển khai |

Kết luận vẫn không thay đổi: tất cả động lực được tái tạo trong thời gian chạy bằng "bản đồ số màu + bảng khung hiện tại + thay đổi nội dung theo số bố cục". Gói được tạo chỉ yêu cầu bản đồ cơ sở tĩnh và bản đồ khung thuộc địa.

## 3. gói tạo image_gen

### 3.1 Điểm tương đồng và khác biệt với gói bản đồ thế giới

Thực hiện theo phương pháp `assets/hd-ai/imagegen-kit` (`manifest.json`, một `*-input.png` + `*-prompt.txt` cho mỗi thẻ và đặt `outputs/`, README cho người dùng). Gói mới đặt `assets/hd-ai/tactical-kit` và thêm một phần của `maps` vào tệp kê khai. Sự khác biệt:

- **Phải được căn chỉnh theo lưới**. 16 pixel mỗi khung hình ↔ HD 64 pixel. Ranh giới cửa sổ chỉ rơi vào cạnh của lưới. Kiểm tra từng lưới sau khi đăng ký (§3.5), nếu không bảng địa hình sẽ không cắt lưới con trỏ.
- **Mặt nước và đường viền không vừa với hình**. Vùng màu tuần hoàn trong hình ảnh đầu vào được cung cấp nguyên trạng (để cho mô hình biết rằng đó là nước) và từ gợi ý yêu cầu nó phải được vẽ dưới dạng mặt nước phẳng lặng và đồng nhất; trong quá trình tổng hợp, các vùng này sẽ bị loại bỏ và thay thế bằng bản đồ màu. Viền 2 khung bên ngoài được cắt trực tiếp từ đầu vào và không chiếm màn hình.
- **Các khuẩn lạc xoay được loại trừ khỏi biểu đồ được tạo tĩnh**. Đầu vào ban đầu giữ lại khung 0 làm tham chiếu vị trí và từ nhắc yêu cầu thân, vòng và bảng gương phải bị xóa và lấp đầy bầu trời đầy sao tối gần đó, không để lại hình bóng hoặc quầng sáng. Hoạt ảnh 8 khung hình được sản xuất riêng biệt và vẫn phải được xử lý theo khu vực phiên bản khi tổng hợp và chạy; việc xóa các đối tượng trong ảnh tĩnh không có nghĩa là quyền truy cập ảnh động đã được xác minh.
- **Hình 2 theo gia đình**. Hiện tại chưa có bản đồ chiến thuật do image_gen vẽ nên trước tiên chúng tôi vẽ 8 mẫu họ (§3.6), sau khi người dùng đồng ý thì cắt ra một phần để trở thành Hình 2.

### 3.2 Thành phần của mỗi đồ thị gốc

| mục | pixel nguồn | khuếch đại đầu vào | đầu ra mục tiêu | số lượng |
| --- | --- | --- | --- | --- |
| Toàn bộ hình ảnh | Toàn bộ hình ảnh sau khi bỏ viền | Hàng xóm gần nhất, cạnh dài khoảng 1536 | Cùng tỷ lệ như Hình 1, image_gen thực sự cho khoảng 1,5 MP | 1 hình ảnh cho mỗi gốc |
| Cửa sổ cục bộ | Thông thường là 384×256 (24×16 lưới), bước 320×192 (chồng 4 lưới), cửa sổ viền co lại vào trong; map-054 hình ảnh hẹp có kích thước 368×256 | hàng xóm gần nhất 4 lần | thường là 1536×1024 (3:2); thu hẹp hình ảnh 1472×1024, luôn duy trì tỷ lệ đầu vào thực tế | Xem §3.4 |

Chức năng của toàn bộ bản đồ cũng giống như chức năng của gói bản đồ thế giới: màu sắc và sự phân bố địa hình của toàn bộ bản đồ được xác định và nó cũng là bản đồ cơ sở khi không có cửa sổ; cửa sổ thêm chi tiết gấp 4 lần. Bộ logic tương tự `worldmap_surfaces.py imagegen` đã được sử dụng để tổng hợp (toàn bộ hình ảnh được đăng ký làm cơ sở, cửa sổ được pha trộn theo "hình ảnh xa nhất tính từ cạnh trong chiếm ưu thế" và màu trên 48 pixel HD được làm tròn), thay đổi thành căn chỉnh lưới rồi chuyển sang `tactical_map_hd.py`.

### 3.3 Biến thể và thuộc địa

27-09-2026: Gói biến thể đã được tạo từ `tactical_map_kit.py build-variants` đến `assets/hd-ai/tactical-kit-variants` (22 biến thể, 50 cửa sổ, ~81 MB). Hình 1 là một cửa sổ được cắt ra từ sơ đồ cơ sở tổng hợp hình ảnh gốc (`runtime-integrated-v4` của Codex), với lưới thay đổi được thay thế bằng các pixel cứng của biến thể; Hình 2 là mặt nạ lưới màu trắng; chỉ có lưới thay đổi được lấy và 1 lưới được thêm vào để tạo lông trong quá trình tổng hợp. Có 4 cửa sổ cho mỗi bước trong số 9 bước của cảnh 103, 1 cho mỗi bước trong số 8 bước của 105, 2 cho bước cuối cùng và 1 cho mỗi trong số 4 biến thể cục bộ.

Tổng hợp biến thể `compose-variants`: Dựa trên bản đồ cơ sở tổng hợp hình ảnh gốc, sau khi đăng ký bản vẽ của từng cửa sổ, chỉ có lưới biến thể được thêm vào và lấy lông nửa khung hình; các cửa sổ không được sơn sẽ quay trở lại mức phóng to pixel hình ảnh số màu (`pixel_fallback`), do đó, có sẵn một tập hợp nội dung biến thể trước khi Codex hoàn tất. Màu chu kỳ, đường viền và khối thuộc địa được khôi phục theo cùng các quy tắc để tổng hợp biểu đồ gốc, đồng thời các trường hợp khuẩn lạc và số màu nền tuân theo `tactical_colony_pack` của Codex. Đầu ra có dạng `tactical-kit-variants/runtime/map-NNN`. Siêu dữ liệu có cùng định dạng với gói chạy biểu đồ gốc. `layout` là số bố cục của chính biến thể đó. `runtime-all/` sử dụng các liên kết tượng trưng để kết hợp gói chạy biểu đồ gốc và các biến thể vào một thư mục cho `SRW64_HD_MAPS`. Máy thực tế (`map-variant-view` cấp độ nhỏ, 109 → 121 loại 1): Sau khi chuyển đổi, nội dung biến thể được rút ra, tất cả 131 nội dung đều được tải, bỏ qua 0, không đánh dấu 0.

27-09-2026 Codex đã vẽ xong 50 cửa sổ và chạy lại `compose-variants`. Tất cả 22 hình ảnh đã được chuyển đổi thành hình vẽ (pixel được cuộn lại 0 ô). Màu nền của bầu trời đầy sao của bản vẽ hơi khác so với màu nền của ảnh gốc và các hình vuông sẽ lộ ra trên cạnh có lông, do đó việc bảo toàn màu tần số thấp được thực hiện trước khi tổng hợp: ảnh tham chiếu lấy các đối tượng được hiển thị trong các pixel gốc biến thể trong lưới thay đổi và phần còn lại sử dụng nền của ảnh gốc được nội suy từ vùng không thay đổi xung quanh (`variant_reference`, bán kính 192 pixel HD) để tránh mang lại độ sáng của đối tượng cũ hoặc nền đen tuyền nguyên bản. Màu cơ bản còn lại chênh lệch 1–2 mức ánh sáng. Máy thực tế 109 → 121 kiểm tra lại bỏ qua 0, không đánh dấu 0.


- **Cửa sổ biến thể**: Hình 1 = Kết quả HD của ảnh gốc (sau khi tổng hợp), thay thế các lưới đã thay đổi trở lại ảnh gốc và phóng to các pixel cứng; từ nhắc chỉ ra rằng chỉ những lưới này sẽ được vẽ lại và phần còn lại sẽ không thay đổi. Việc tổng hợp chỉ lấy lưới biến đổi và thêm 1 lưới lông vũ. Cảnh 103 có một khung bao gồm 39×21 ô trên một cửa sổ, 2 hình ảnh mỗi bước; cảnh 105 có 1–2 hình ảnh mỗi bước; 1 hình ảnh cho mỗi biến thể trong số 4 biến thể cục bộ. Khoảng 32 ảnh.
- **Ảnh khung thuộc địa**: 8 khung hình 6235 được ghép thành hình 4×2 (256×192 ×8 = 1024×384), được hoàn thành trong một yêu cầu để đảm bảo tính nhất quán giữa các khung; từ gợi ý cho biết đây là 8 giai đoạn quay của cùng một thuộc địa và nền bầu trời đầy sao phải phù hợp với các khung liền kề. Nếu bức tranh không thẳng, hãy quay lại MMPX để phóng to. 1 tờ.

### 3.4 Số lượng và phân loại

Gói đã tạo được tạo từ [`tactical_map_kit.py`](../../tools/hd_ai/tactical_map_kit.py) đến `assets/hd-ai/tactical-kit` (được tạo vào ngày 25-09-2026: 109 toàn bộ ảnh, 772 cửa sổ, 1 ảnh khung thuộc địa, khoảng 99 MB, chưa được nhập vào git). Cửa sổ chỉ bao phủ hình ảnh sau khi loại bỏ đường viền. Toàn bộ bản đồ một màn hình lớn hơn gấp 4 lần và cửa sổ không còn bị cắt nữa. README trong gói nêu rõ cách bắt đầu với mẫu trước và chia thành 11 lô theo thứ tự của cốt truyện; gói thứ hai sẽ được phát hành sau khi phiên bản biến thể được hoàn thiện.

Chia theo các cửa sổ trong §3.2, có 109 biểu đồ gốc với tổng số 772 cửa sổ (ước tính trước khi loại bỏ đường viền là 904). Tôi đã thử lọc các cửa sổ nền thuần túy bằng cách nhấp vào "Ô nền trong Thống kê số lưới" và chỉ có thể xóa 3: khu rừng đồng cỏ của họ Ground lẽ ra phải được vẽ lại và các mảnh vỡ thiên thạch của họ Space nằm rải rác khắp bản đồ. Vì vậy mình không lưu được, chỉ có thể chia thành các loại khác nhau:

| Tập tin | Nội dung | Số tờ |
| --- | --- | ---: |
| Cấp độ đầu tiên: toàn bộ bức tranh | Bao gồm 1 trong số 109 ảnh gốc + mẫu gia đình | 109 |
| Tầng 2: Cửa sổ gia đình mặt đất | 60 ảnh gốc | 349 |
| Thiết bị thứ hai: Cửa sổ gia đình vũ trụ | 37 hình ảnh gốc | 339 |
| Cấp 2: 6 cửa sổ gia đình khác | 12 ảnh gốc | 84 |
| Biến thể + Thuộc địa | | 33 |

Hiệu quả của việc chỉ sử dụng toàn bộ hình ảnh: kích thước thực tế của bản đồ lớn là khoảng 1,5–2,6 lần và màn hình đơn là khoảng 4,4 lần; sau khi zoom to gấp 4 lần canvas thì tốt hơn nhiều so với zoom hàng xóm gần nhất ở ảnh gốc, mặt nước vẫn rõ nét theo bản đồ màu.

**Gợi ý**: Tạo giai đoạn đầu tiên (109 bản đồ) trước, với tất cả các bản đồ có phiên bản HD trước; sau đó làm giai đoạn thứ hai của họ mặt đất (349 bức, chia làm 8 đợt, mỗi đợt bản đồ một chương) theo trình tự cốt truyện; bầu trời đầy sao của gia đình vũ trụ là nguồn sáng điểm, giai đoạn thứ hai có lợi nhuận nhỏ nhất nên hãy để nó ở cuối để điền vào khi cần thiết. Nếu muốn nhấn mức thứ hai của số lượng ảnh, bạn có thể thay đổi cửa sổ thành 3 lần (512×341 pixel nguồn → 1536×1024, không cần thay đổi mã khi chạy `scale: 3`). Số lượng hình ảnh sẽ giảm khoảng 40%, khiến hình ảnh cơ bản mềm hơn 4 lần một chút.

### 3.5 Xác minh căn chỉnh

Đăng ký cửa sổ tuân theo `fit_scale` (bình phương nhỏ nhất cho tỷ lệ hai trục + dịch). Bản đồ chiến thuật cũng bổ sung thêm xác minh theo từng ô vuông: thu nhỏ cửa sổ đã đăng ký 1 lần, so sánh màu trung bình với ảnh gốc theo từng ô vuông và báo cáo hình vuông có độ lệch lớn nhất; cửa sổ có độ lệch hơn nửa hình vuông (8 pixel nguồn) được vẽ lại. Đây là tiền đề chính xác cho các ô giả trong bảng địa hình.

### 3.6 Mẫu và trình tự họ

1. Mỗi gia đình trong số 8 gia đình sẽ có một bức tranh đầy đủ, và 6 gia đình có cửa sổ sẽ có một cửa sổ khác số 01, tổng cộng có 14 bức tranh (20 trên mặt đất, 87 trong vũ trụ, 35 trong pháo đài, 49 trên mặt trăng, 36 trên sa mạc, 66 trong biển mây, 112 trong Dải Ngân hà và 74 dưới mây); hai gia đình đám mây không có cửa sổ khác. Sau khi người dùng đồng ý, họ cửa sổ sẽ sử dụng cửa sổ như Hình 2, còn họ đám mây sẽ sử dụng toàn bộ hình ảnh.
2. Một tập tin chứa toàn bộ 109 bức ảnh.
3. 1 bức tranh khung thuộc địa (có thể được thực hiện sau khi vượt qua mẫu gia đình vũ trụ).
4. Cấp độ thứ hai được chia thành các đợt theo chương.
5. Các biến thể được thực hiện sau khi sơ đồ gốc của chúng được hoàn thiện.

Sau khi hoàn thành mỗi đợt, `export` sẽ được sử dụng để xem trên máy thực tế; sau khi chất lượng hình ảnh được phê duyệt sẽ được đăng ký vào danh sách nghệ thuật và vào gói full HD.

## 4. “Gạch giả” của bảng địa hình

### 4.1 Cách vẽ phiên bản gốc (`801E2D54`, đọc từ dịch ngược)

1. Ghi `800FFA74 + 槽×0xC4` từ khe hình bảng để lấy gốc của bảng (x, y); khi ghi +0x70 bằng 0x495, đó là bảng phiên bản cao (hình chữ nhật nền là y+0x5D), nếu không thì là y+0x44.
2. Đọc từ lưới `80172ED8` của ô nơi đặt con trỏ (nửa từ cao là dấu lật: 0x4000 gương, 0x8000 lật lên và xuống; nửa từ thấp là số ô), bộ xử lý tập bản đồ `801027E4`, bộ điều khiển bảng màu `801027E6` và dữ liệu được lấy thông qua `8008A11C`.
3. Số lưới → Tọa độ Atlas: `sx = (t & 15)×8 + ((t & 0x300) >> 1)`, `sy = ((t & 0xF0) >> 1) + ((t & 0xC00) >> 3)`, giống `map_dynamics.compose`; tải 16×16, đặt gương/lật theo cờ.
4. Vẽ một văn bản từ (x+4, y+5) đến (x+41, y+42), 37×37 pixel, dsdx = dtdy = 0x1BA ≈ 16/37, tức là phóng to 2,31 lần.

Nói cách khác, bảng điều khiển hiển thị ô trong tập bản đồ chứ không phải chính lưới trên bản đồ; cả hai đều giống nhau trong phiên bản gốc, vì lưới là bản sao của ô.

### Phương pháp 4.2 HD

Bản đồ cơ sở HD được vẽ toàn bộ và cùng một ô được vẽ khác nhau ở các vị trí khác nhau, do đó, "ô" được thay đổi thành **khối 64×64 của lưới con trỏ trên bản đồ cơ sở**:

- Lấy con trỏ `80102308/0C` từ gốc pixel của lưới trên bản đồ (f32 pixel bản đồ, bao gồm cả đường viền; [Giữ R để nhảy đến lưới xa nhất] bản ghi của (../native/move-jump.md) là lưới × 16+32). Cắt uv = [cx/W, cy/H, (cx+16)/W, (cy+16)/H], W và H là kích thước pixel bản đồ.
- Sử dụng cùng một shader `HdMap` để vẽ đến vị trí của văn bản gốc, khi khung TLUT được đọc từ danh sách hiển thị của chính bảng điều khiển (tìm `F0` sau `FD` như bản đồ). Vì vậy, khi con trỏ dừng lại trên dòng sông, nước trong bảng cũng luân chuyển theo bảng màu; bảng màu cảnh đêm cũng có hiệu lực.
- Khi lưới con trỏ nằm trong thể hiện thuộc địa, khối con 64×64 tương ứng của sprite thuộc địa được xếp chồng lên nhau (số khung cũng ghi `80178C6D`).
- Đừng lo lắng về cờ lật: hình ảnh cơ sở đã ở hướng tổng hợp.
- Khi lấy mẫu tia UV rút nửa texel vào trong để tránh hiện tượng song tuyến làm mất màu các ô liền kề.
- Nếu không có nội dung nào cho bố cục này hoặc ở chế độ ban đầu, nó sẽ không được viết lại và các ô gốc sẽ vẫn được vẽ.

### 4.3 Triển khai và xác minh (Hoàn thành vào ngày 27-09-2026)

Việc thực hiện được thực hiện theo các bước sau và máy thực tế đã đạt:

- Móc `load_000AB160_func_801E2D54 → srw64_original_terrain_panel_draw` (`generate_cpu.py`), được bọc trong `game_hooks.cpp`, gọi lại `srw64_game_hooks.terrain_panel_drawn(ram, begin, end)`, `host.cpp` nhận `hdmap::rewrite_panel`.
- `rewrite_panel` của `native_map.cpp`: nhớ nội dung bản đồ được viết lại gần đây nhất (`current_map`), đọc TLUT và hình chữ nhật duy nhất từ danh sách hiển thị bảng điều khiển, uv lấy lưới con trỏ và rút một nửa HD texel vào trong và dấu được viết trên `SETTILESIZE` ở phía trước hình chữ nhật; lớp phủ thuộc địa tuân theo Codex `project_overlay`, số khung cũng là `80178C6D`. Số đếm được ghi vào `hd-map-summary.json` của `panel_draws` / `panel_unmarked`.
- **Kích hoạt bảng địa hình**: Ở trạng thái không hoạt động (`801C8B04`), nhấn **B** vào khoảng trắng, `801CABAC` để mở cửa sổ (cảnh 0x8E); dừng con trỏ trên thiết bị và nhấn B để mở cửa sổ thiết bị. Lần đầu chạy không chụp được bảng vì không bấm B.
- **Con trỏ là nguồn gốc lưới đã được xác nhận**: `801CABAC` Sử dụng `trunc(光标) >> 4` trực tiếp làm số lưới (bao gồm cả đường viền) và kiểm tra `801E2074`, khác 2 với số lưới trò chơi là "grid=(v−32)>>4", chính xác là đường viền 2 lưới.
- Kịch bản xác minh `tools/recomp/debug/check_terrain_panel.py`: Ở cấp độ di chuyển-nhảy, di chuyển con trỏ đến lưới đường (11,8) và lưới rừng (13,12) để mở mỗi cửa sổ và chụp ảnh màn hình của phiên bản HD và gốc; so sánh các ô bảng với lưới con trỏ và 8 lưới liền kề trên bản đồ cơ sở HD. Chênh lệch lưới con trỏ là 3,7 / 2,7 và lưới liền kề tối thiểu là 6,4 / 14,1, bảng hiển thị lưới con trỏ. Khi chuyển `map87-colony-view` để mở một cửa sổ trong ô thuộc địa, các giai đoạn của khối con thuộc địa trong bảng điều khiển sẽ khác nhau ở hai ảnh chụp màn hình cách nhau 1,6 giây và chế độ ban đầu vẫn là ô gốc.

### 4.4 Các bước triển khai ban đầu

1. Thêm `load_000AB160_func_801E2D54 → srw64_original_terrain_panel_draw` vào `NATIVE_HOOKS` của `generate_cpu.py` và tạo lại (bạn cần chạy thủ công sau khi thay đổi bảng).
2. Thêm gói vào `game_hooks.cpp`: con trỏ danh sách hiển thị ở `*a0`, đọc nó một lần trước và sau cuộc gọi để lấy phạm vi và đưa nó cho `srw64_game_hooks.terrain_panel_drawn(ram, begin, end)`.
3. Thêm `native_map.cpp` vào `rewrite_panel`: Tìm hình chữ nhật `E4` duy nhất trong phạm vi, tính uv theo 4.2 và viết lại bằng cơ chế ghi dấu + vòng hiện có; số bố cục hiện tại lấy giá trị được ghi trong lần ghi lại bản đồ gần đây nhất.
4. Xác minh tập lệnh `tools/recomp/debug/check_terrain_panel.py`: Sử dụng giao diện gỡ lỗi để đặt con trỏ trên lưới sông, thành phố, biên giới và thuộc địa theo trình tự, chụp ảnh từng ô và so sánh khu vực bảng với khối tương ứng của bản đồ cơ sở (giảm xuống 37×37). Phần bù đăng ký phải bằng 0.

## 5. Thu phóng tổng quan

27-09-2026 Đã hoàn thành và xác minh trên máy thực tế. **Vào là nhấn C-phải trên bản đồ nhàn rỗi** (B để thoát); giao diện gỡ lỗi bàn phím không ánh xạ phím này nên bạn cần sử dụng tên khóa N64 `c_right` được gọi bởi `buttons`. Bảng quân đội (C-top, `801CB1B4`) chỉ được tính toán trước, chia tỷ lệ và lưu trữ trong `80172EF8`, còn bản vẽ đơn vị `801E21F8`/`801E26C0` được chia tỷ lệ theo bảng đó trong phần tổng quan.

Viết lại toàn bộ đường dẫn (`MapDraw.overview`, được đánh giá bởi bản ghi phụ +3), uv đảo ngược các đường viền bị bỏ qua dựa trên số lượng lưới và hàng được vẽ thực tế, kết cấu sơ đồ cơ sở có chuỗi mip bộ lọc hộp (được tính trong luồng giải mã) và bộ lấy mẫu bật mipmap. `check_hd_overview.py`: Tổng quan về bản đồ 20 chiếm cùng khung màn hình (864×1008 pixel màn hình) ở chế độ HD và phiên bản gốc, vị trí đơn vị nhất quán và tổng quan được vẽ 75 lần không bỏ qua.

Thiết kế ban đầu:

`800945D4` thu nhỏ toàn bộ bản đồ (không bao gồm 2 ô bên ngoài) thành 266×200 khi byte chế độ khác 0. Bây giờ `host.cpp` trực tiếp bỏ qua việc viết lại khi gặp kiểu vẽ này. Phương pháp HD:

- Viết lại đường dẫn tương tự, đánh dấu hình chữ nhật và lấy hộp giới hạn của tất cả các hình chữ nhật và uv được cố định thành [32/W, 32/H, (W−32)/W, (H−32)/H].
- Mipmap tạo kết cấu bản đồ nền (hiện chỉ còn một lớp), nếu không bản đồ nền 4x sẽ nhấp nháy khi giảm xuống còn 1/13. Bản đồ số màu không thể là mip. Trong phần tổng quan, chỉ cần nhấn số màu gần nhất để nhận số lượng dịch. Màu sắc của vùng mặt nước vẫn giống với khung hình.

## 6. Chấp nhận

- Sử dụng `SRW64_HD_MAPS` sau mỗi đợt `SRW64_HD_MAPS`. Xem máy thực tế: cuộn bốn góc và cắt rời một đoạn, độ lệch so với đăng ký ban đầu là 0 (phương pháp bản đồ 20 mẫu).
- Chọn bản đồ cho từng mặt nước, flash mob và thuộc địa để ghi lại một phân đoạn phù hợp với nhịp điệu từng khung hình ban đầu.
- Bảng địa hình được kiểm tra theo bước 4 của §4.3.
- Cảnh đêm/cảnh ngày (chuyển cảnh 90/102 sang 60/64/157) màu sắc theo máy thật.

## 6.5 Truy cập vào trò chơi (27-09-2026)

- **Gói nội dung**: `tactical_map_kit.py pack` Sao chép gói và biến thể chạy bản đồ gốc (`runtime-all`, giải nén liên kết tượng trưng) vào `assets/hd-ai/tactical-maps/pack-v1`: mỗi bản đồ 131 có `base.png`, `index.png`, `meta.json`, cộng với 8 thuộc địa Khung, `tactical-maps.json` ghi lại SHA-256 của mỗi tệp.
- **Bản kê khai nghệ thuật**: `content/art/stage1-hd.json` Đã thêm `tactical_maps` (đường dẫn và tóm tắt tệp kê khai). `compile_art` Xác minh từng tệp: `art/maps` được sao chép khi hoạt động đóng gói và phát triển (`profile.py`) không sao chép và trỏ trực tiếp vào thư mục nội dung; cả hai đều viết `art/srw64-tactical-maps.json`, `root` là đường dẫn tương đối `maps` hoặc tuyệt đối.
- **Máy chủ**: Khi không đặt `SRW64_HD_MAPS`, thư mục bản đồ được tìm thấy từ chỉ mục của `SRW64_ART_PACK`, do đó, trình khởi chạy, gói full HD tự sử dụng và quá trình phát triển của `--images hd` sẽ được tự động đưa vào. Bản đồ được thay đổi để tải theo yêu cầu: khi một bố cục nhất định được vẽ lần đầu tiên, nó sẽ được chuyển sang luồng giải mã (được tính cùng với chuỗi mip). Chuỗi trò chơi chờ tới 400 mili giây. Theo số đo thực tế, khung hình đầu tiên sau khi vào mức là HD; khoảng 900 bản đồ không được sử dụng trong bản vẽ bản đồ, sử dụng `gpu::retire` để giải phóng kết cấu trong chuỗi kết xuất, sau đó giải mã nó vào lần tiếp theo (`SRW64_HD_MAPS_EVICT_AFTER` có thể điều chỉnh để kiểm tra). Trước đây, tất cả các bản đồ đều được giải mã vào bộ nhớ khi khởi động, dung lượng khoảng 4 GB.
- **Gói Full HD để bạn sử dụng**: `compress_hd.py` chuyển đổi bản đồ cơ sở thành JPEG (chất lượng 95), `base` của `base` điểm thành `base.jpg`, bản đồ màu và khung thuộc địa vẫn ở định dạng PNG; phần bản đồ 1.0 GB → 350 MB, toàn bộ thư mục HD khoảng 708 MB.
- **Gói công cộng cũng đi kèm với** (2026-09-28 do người dùng xác định: gói HD công khai giống như gói dành cho mục đích sử dụng cá nhân): bản đồ số màu và các pixel vùng vòng lặp được phóng to từ các pixel bản đồ gốc. Điều này được nêu trong THÔNG BÁO và ghi chú phát hành. Trước đây, `build_release.py` đã liệt kê `art/maps` vào `ROM_DERIVED` và xóa nó khỏi gói công cộng, gói này đã bị hủy. Bản đồ nền JPEG chất lượng 92, 4:2:0 (`compress_hd.py`), phần bản đồ khoảng 236 MB.
- **Xác minh**: `test_tactical_maps_pack.py` (xác minh và nén), `test_hd_release.py`; máy thực tế đã sử dụng bản đồ JPEG trong gói tự sử dụng để chạy bảng địa hình (176 lần) và thuộc địa (8 khung hình), đồng thời sử dụng đường dẫn phát triển để chạy tổng quan và công tắc 109→121 (nhả 1 lần). Không có lỗi bỏ qua hoặc giải mã.

## 7. Cần được xác minh

27-09-2026 Đã xác minh **Chuyển đổi thay đổi hình ảnh 3D34** (`map-switch-view` cấp độ nhỏ, bản đồ 9 → 62, loại 0): Hình ảnh cũ bị bôi đen ở mọi dòng khác, đen hoàn toàn trong một khung và hình ảnh mới được hiển thị ở các dòng thay thế. Hai bản đồ không bao giờ xuất hiện trong cùng một khung và quá trình ghi lại HD diễn ra bình thường (bỏ qua 0, không đánh dấu 0). Trình tự biến thể sử dụng loại 1 (chuyển đổi tức thời) và không gặp phải vấn đề này. Còn lại:


- `8021E240` Bảng trạng thái có chuyển sang bản đồ số chẵn theo thứ tự hay không.
- Cách kích hoạt thu phóng tổng quan (không tìm thấy điểm ghi `801027DB`) và cách nhập tổng quan trên máy thực tế.