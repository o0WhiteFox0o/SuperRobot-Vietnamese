> **Ngôn ngữ / Language:** [Tiếng Việt](native-worldmap-regions-hd.vi.md) · [English](native-worldmap-regions-hd.en.md) · [中文](native-worldmap-regions-hd.md)

# Story World Map HD: Tất cả các khu vực

24-09-2026. Nền giữa các cảnh trong cốt truyện được vẽ bằng lớp phủ bản đồ thế giới (`load_000A7EC0`) và hiện tại tất cả các khu vực đều là HD. Bắt đầu từ ngày 25-09-2026, cả bốn bề mặt đều được vẽ lại bằng image_gen ([use_gen](#改用-image_gen2026-09-25) của Codex) và phong cách vẽ theo phiên bản image_gen của Châu Âu trong tập đầu tiên ([World Map HD](native-worldmap-hd.md)). Bắt đầu từ ngày 25-09-2026, Châu Âu sẽ chuyển sang Bailian. Vui lòng thêm chi tiết vào phiên bản image_gen. Xem [Châu Âu chuyển sang Bailian](#欧洲改用百炼2026-09-25).

## Có những khu vực nào?

Bảng đối tượng mô hình `801C5670` liệt kê bề mặt của từng vùng. Bảng vị trí `801C5310` có tổng cộng 127 mục, mỗi mục có ba nửa từ được ký (bề mặt = chỉ số dưới của bảng mô hình, x, y), xem [Cấp độ nhỏ](../script/mini-stage.md). Có 827 lần (661/166) `3D32`/`3D33` trong tập lệnh, thống kê dựa trên vị trí:

| Tài nguyên | Nội dung | Số lượng địa điểm | Số lượng nhắm mục tiêu | Làm thế nào để |
| --- | --- | ---: | ---: | --- |
| 5599 | Vũ trụ: bầu trời đầy sao, trái đất, mặt trăng, thiên thạch, hai cơ sở nhỏ, thẻ tên | 32 | 369 | Bầu trời đầy sao được vẽ toàn bộ, phần còn lại được thay thế bằng RT64 và bảng tên được vẽ lại theo ngôn ngữ |
| 5602 | Toàn bộ Trái đất | 28 | 184 | 6 cửa sổ được tạo |
| 5603 | Toàn bộ Trái đất (cùng từng ô với 5602, chỉ là một lưới khác) | 29 | 164 | Chia sẻ HD với 5602 |
| 5606 | Bắc Mỹ | 22 | 70 | 9 cửa sổ được tạo |
| 5604 | Địa Trung Hải, Châu Âu, Trung Đông và Bắc Phi (Chương 1) | 10 | 28 | image_gen phiên bản 1, chi tiết về Bailianbu, 9 cửa sổ (25-09-2026) |
| 5605 | Trung Á, Ấn Độ | 6 | 12 | Tạo 8 cửa sổ |

Mỗi khu vực trên Trái đất là một lưới lát gạch gồm các ô CI4 64×64, mỗi ô có bảng màu 16 màu riêng; biển trong suốt hiển thị màu màn hình rõ ràng RGB (0,55,90).

## Bề mặt trái đất

[`worldmap_surfaces.py`](../../tools/hd_ai/worldmap_surfaces.py):

- `prepare`: Đặt tất cả các thành phần trong mỗi khu vực thành một hình ảnh theo các đỉnh lưới (hướng bắc lên trên), cắt nó thành cửa sổ 256×256 với độ chồng lên nhau là 48 và phóng to hàng xóm gần nhất 8 lần làm đầu vào (2048²).
- **Tham khảo phong cách hội họa** (Hình 2): Lấy bốn họa tiết đất thuần khiết (rừng, núi, cồn cát, núi sa mạc) từ bức tranh HD đã xem xét về Châu Âu trong tập đầu tiên và ghép chúng lại thành mẫu 1024².
- Ban đầu, bản đồ Châu Âu được sử dụng trực tiếp làm tài liệu tham khảo và mô hình sẽ sao chép đường bờ biển của nó: cửa sổ Trung Á trở thành Biển Địa Trung Hải và có thêm một lục địa sa mạc ở Thái Bình Dương.
- Sau khi chỉ đưa ra kết cấu chứ không đưa ra đường bờ biển, chúng ta sẽ không sao chép nó nữa.
- `run`: Model `qwen-image-3.0-pro`, một trang được hiển thị trong mỗi cửa sổ và sau đó được kiểm tra tự động:
- Giảm đầu ra về kích thước ban đầu, so sánh phân bố đất/đại dương (IoU) với ảnh gốc, bỏ qua 1 pixel gốc ở 2 bên bờ biển (mô hình sẽ vẽ một vòng tròn vùng nước nông dọc bờ biển);
- Nếu thấp hơn 0,90 thì thay hạt và vẽ lại, tối đa 3 lần, lấy hạt tốt nhất;
- Đầu ra sao chép chỉ 0,34–0,84, trong khi đầu ra bình thường trên 0,90.
- `compose`:
- Mỗi cửa sổ được đăng ký vào lưới ảnh gốc theo chế độ thu phóng và dịch thuật;
- Chuyển tiếp tuyến tính ở các vùng chồng lấn tạo thành một bức tranh tổng thể;
- Đường bờ biển được mở rộng và làm mịn bằng cách sử dụng mặt nạ ảnh gốc, mặt biển vẫn trong suốt.
- Phong cách vẽ ban đầu yêu cầu thay đổi màu sắc nên màu tần số thấp của ảnh gốc không bị khóa theo mặc định (có thể bật `--colour-lock`).
- `pack`: Cắt tọa độ khối ban đầu thành 512×512 và sử dụng `rt64_hash.map_hash` để tính key RT64 của từng khối:
- 5603 và 5602 chia sẻ cùng một hình ảnh HD;
- Toàn bộ gạch biển còn lại màu sắc trong suốt;
- Cùng một key tương ứng với 2 nội dung khác nhau, có 2 khối, giữ nguyên;
- 57 phần được review trong tập đầu tiên sẽ được giữ nguyên (trước ngày 25/09/2026).

Kết quả: 152 khối mới, cộng thêm 57 khối đã được xem xét, nâng tổng số 209 bản đồ thay thế. 25-09-2026 Châu Âu chuyển sang Bailian, các khu vực khác vẫn có 213 khối (`pack-v4`) sau khi thay đổi phong cách vẽ và 213 khối tương tự (`pack-v5`) sau khi chuyển sang image_gen. `srw64-worldmap-hd.json` Đã thêm trường `resources`, máy chủ chấp nhận 5602–5606, định dạng một vùng cũ của tập đầu tiên vẫn có sẵn.

### Cửa sổ riêng lẻ

- Sơn lại: Earth-04, Central-asia-05, Coast-05, Coast-06, Coast-08. Việc phân bổ đất ở hình đầu tiên là sai. Nó trôi qua sau khi tự động thay đổi hạt giống; Earth-01 chụp bức ảnh thứ ba.
- Cao nguyên Tây Tạng (trung-asia-03) gần như hoàn toàn là đất liền:
- Ba bức tranh đầu tiên có nhiều hòn đảo hơn hoặc vẽ cao nguyên thành đồng cỏ xanh;
- Bức tranh thứ tư đã thêm "hầu hết đất đai, tan là núi, không vẽ đồng cỏ" trong lời nhắc. Vị trí đúng nhưng phong cách sơn nhạt hơn so với cửa sổ liền kề.
- Khi vẽ lại, đã gặp phải giới hạn chi phí một đợt của công cụ (18,12 nhân dân tệ cho mỗi thư mục đầu ra), vì vậy bức ảnh thứ tư được giữ lại trước.

## VŨ TRỤ

[`worldmap_space.py`](../../tools/hd_ai/worldmap_space.py)：

- Trái đất (khối 4×4) và mặt trăng (2×2) được ghép thành hình bảng thông báo theo các đỉnh; kết cấu 32×32 của 4 thiên thạch và hai cơ sở nhỏ được đưa vào lưới.
- Bầu trời đầy sao 5582 (CI4 320×240, Palette 5583) được xử lý làm toàn bộ nền.
- Yêu cầu `qwen-image-3.0-pro` mỗi lần một lần, tổng cộng 4 lần. Sau khi đăng ký, Alpha lấy mặt nạ ảnh gốc và làm mịn nó, rồi cắt theo ô; khóa RT64 của ô CI4 được tính bằng `ci4_hash` (64×64 giống với `map_hash`, độ rộng dòng 32×32 giảm đi một nửa), tổng cộng có 27 khối. Chúng là một danh mục mới trong kho `space` và không tham gia vào quá trình kiểm tra 64→512 trên bản đồ thế giới.
- 7 thẻ tên (サイド1/2/3/5/6/7, スウィートウォーター) là văn bản và sẽ không được thay thế bằng RT64. Chúng là những biển báo có khung màu xanh lá cây có kích thước 200×30 giống như biển hiệu tàu và cột mốc (danh sách hiển thị mục 6–12 loại 5 gồm 5599). Chúng được vẽ lại bằng bảng tên của mô hình cắt cảnh bản đồ thế giới HD theo ngôn ngữ đọc: gói mô hình gốc chỉ nhập chúng vào bảng tên, không có mục lưới, tiếng Trung và tiếng Anh là Mặt 1...Mặt 7 (cách dịch các dòng) và Oasis/Sweetwater.

### Bầu trời đầy sao

Bầu trời đầy sao được vẽ trong khe sprite 0 và có cùng cách với nền liên trường `80095974`. Nó được vẽ hoàn toàn bởi [`native_background.cpp`](../../src/host/native_background.cpp) và tệp được đặt trong `backgrounds/whole-v2` (16 hình nền xen kẽ cộng với 1 bầu trời đầy sao). Có hai điểm khác biệt so với nền liên trường:

- Hình ảnh CI4 được tải dưới dạng 8 bit, một nửa chiều rộng (`SETTIMG` rộng 160). Tọa độ cột của `LOADTILE` phải được nhân với "chiều rộng ảnh gốc ` chiều rộng SETIMG" để thu được pixel.
- Bầu trời đầy sao là điều đầu tiên được vẽ trong mỗi khung hình. Khi máy chủ vẽ toàn bộ hình ảnh ở khối đầu tiên, RT64 vẫn chưa thực hiện xóa màn hình khung này và sẽ xóa nó thành màu đen khi bắt đầu lượt kết xuất tiếp theo.
- Bây giờ giữ nguyên khối đầu tiên được vẽ bởi RT64 để kích hoạt đường chuyền của nó; toàn bộ bức tranh được vẽ ở vị trí khối cuối cùng, bao phủ khối đầu tiên.
- Phông nền giữa các cảnh cũng được xử lý theo cách này và hình thức không thay đổi.

## Châu Âu chuyển sang Bailian (25-09-2026)

Tập đầu tiên của Châu Âu ban đầu được vẽ bởi image_gen đi kèm với công cụ mã hóa (`worldmap-runtime/pack-v6`). Trong quá trình tổng hợp, đường bờ biển hẹp và ranh giới cắt xén của ảnh gốc vẫn được giữ lại. Khoảng 6% số pixel hiển thị được phóng to so với ảnh gốc và có một vài mảng ở góc trên bên phải không phải là HD. Gói HD cần được phát hành ra công chúng và phần mô tả nói rằng nó được tạo ra bởi Bailian, vì vậy Châu Âu sử dụng Bailian để vẽ lại và phong cách vẽ tranh tuân theo phiên bản image_gen:

- Lần đầu tiên (`worldmap-surfaces/europe-1`) được vẽ lại từ ảnh gốc như các khu vực khác: Bán đảo Ả Rập và Ai Cập biến thành đồng cỏ xanh khi không giữ được màu sắc; màu sắc chính xác sau khi `compose --colour-lock` được giữ nguyên, nhưng phong cách vẽ có màu xám và phẳng, đồng thời có các đường nối do ranh giới của các khối hình ảnh gốc gây ra. Sau khi đọc xong, người dùng cho rằng nó kém hơn nhiều so với phiên bản image_gen và không chấp nhận.
- Phương pháp được áp dụng (`worldmap-surfaces/europe-2`): 8 lần phiên bản image_gen của Châu Âu vào toàn bộ bức tranh (`approved_canvas`, các ô không có HD được phóng to bởi ảnh lân cận gần nhất của ảnh gốc), cắt thành 9 cửa sổ giống như ảnh 1, các lời nhắc yêu cầu kiểu vẽ, phối màu, bố cục và phân bố địa hình vẫn hoàn toàn không thay đổi và chỉ thêm một lượng nhỏ chi tiết. Không có mẫu kiểu vẽ nào được đưa ra và màu sắc không được giữ nguyên. `samples.json` ghi lại phần tóm tắt đầu vào và các từ nhắc nhở cho mỗi cửa sổ.
- Quá trình tổng hợp diễn ra như bình thường: đăng ký vào ảnh gốc, đường bờ biển được cắt mịn theo mặt nạ ảnh gốc và phần đảo sơn quá mức trong mô hình được loại bỏ.
- Kết quả: 61 khối đều đến từ Bailian. Có thể thấy, số pixel giống với ảnh gốc là 0. Có 5 địa điểm ở Nga ở góc trên bên phải có chung kết cấu ảnh gốc (`b820c653dd7fc5ec`). Một hình ảnh HD không thể khớp 5 vị trí cùng lúc và vẫn sẽ được hiển thị như hình ảnh gốc.

## Các khu vực khác dựa vào kiểu image_gen (25-09-2026)

Người dùng yêu cầu tất cả các khu vực phải gần giống với phong cách của phiên bản image_gen của tập đầu tiên. Trái đất, Trung Á và Bắc Mỹ không có phiên bản image_gen có thể được sử dụng làm bản đồ nền, vì vậy `restyle` được sử dụng:

- Hình 1: `run-5` Cửa sổ vùng tổng hợp, độ bão hòa ×1,3, làm cho màu sắc địa hình trở nên rõ ràng hơn; Hình 2: Mẫu tranh theo phong cách tương tự.
- Từ gợi ý (`RESTYLE_PROMPT`) chỉ cho phép bạn thay đổi cách vẽ: màu sắc và kiểu địa hình của từng nơi phải giống như trong Hình 1. Cao nguyên nâu vẫn là núi đá nâu, màu vàng vẫn là sa mạc, chỉ có những nơi xanh mướt là đồng cỏ và rừng rậm, không thêm hồ, biển mới. Lời nhắc ban đầu không có những hạn chế này, vẽ cao nguyên Tây Tạng như một đồng cỏ xanh và thêm một hồ nước (`restyle-trial-central-asia`).
- Chấp nhận: Vẫn chỉ sử dụng trùng đất ( ≥ 0,90) để tự động thay đổi giống. Tôi đã từng thử so sánh các địa hình bằng cách phân loại màu sắc và tự động vẽ lại, nhưng bản thân các nét vẽ mới sẽ thay đổi cách phân loại màu sắc. Kết quả là những ứng viên "gần như không có thay đổi" đã được chọn nên tôi chuyển sang chỉ ghi hai số này (`terrain`, `new_water`) và để mọi người nhìn vào từng cửa sổ hình ảnh.
- Một số bổ sung bổ sung đã được thực hiện sau khi xem xét thủ công: `earth-01` đã chọn ứng cử viên thứ 3; `central-asia-04` lấy cái thứ 3 (cái thứ 1 là một bức tranh khảm lộn xộn); `earth-04` Người thứ 2 yếu nhưng các ứng cử viên khác đã di chuyển toàn bộ vùng đất và giữ nó; `central-asia-07` cái đầu tiên có một chút hỗn hợp, nhưng hai cái còn lại vẽ Bangladesh-Đông Dương như một sa mạc và cái đầu tiên được giữ lại.
- Kết quả theo `restyle-earth`, `restyle-central-asia`, `restyle-coast` và `europe-2` ở Châu Âu đã ghi điểm `pack-v4`. Tất cả các pixel hiển thị trên bề mặt giống với ảnh gốc là 0.

## Thay vào đó hãy sử dụng image_gen (25-09-2026)

Sau khi nhìn thấy hai phương pháp của Qianwen (`europe-2`, `restyle-*`), người dùng cho rằng chúng thua xa image_gen nên bốn bề mặt đều được người dùng vẽ bằng image_gen trong Codex:

- Tạo gói `assets/hd-ai/imagegen-kit`: 1 toàn bộ khu vực trong mỗi khu vực (phóng to lân cận gần nhất của ảnh gốc 1) cộng với cửa sổ cục bộ 3:2 (384×256 pixel nguồn, 4 lần, 1536×1024; gần như toàn bộ cửa sổ biển không được vẽ), tổng cộng 24 ảnh. Hình 2 luôn là một phần của Châu Âu được vẽ bởi 9-09 image_gen (`worldmap-runtime/ai-detail-v1/map-ai.png`). Lời gợi ý được viết lại từ hai đoạn văn trong câu 9-09 và mỗi loại địa hình bắt buộc phải giữ nguyên; `manifest.json` ghi lại vị trí cửa sổ và việc tạo Codex được ghi trong `outputs/generation-records.json` (công cụ chỉ báo cáo `image_gen.imagegen (built-in)` chứ không phải kiểu máy cụ thể).
- Tổng hợp `worldmap_surfaces.py imagegen --kit … --output worldmap-surfaces/imagegen-1`:
- Bản đồ toàn khu vực được đăng ký vào nền lưới 8x; các cửa sổ được đăng ký từng cái một.
- Các cửa sổ chồng lên nhau tới 2/3 và trung bình hai bức tranh sẽ bị mờ, vì vậy hãy hòa trộn theo "Cửa sổ xa mép trong nhất sẽ chiếm ưu thế" (`kit_weight`) và chỉ thực hiện chuyển tiếp nhẹ gần đường phân chia.
- Cửa sổ giữ nguyên các chi tiết riêng, màu sắc trên 48 pixel HD được làm tròn toàn bộ khu vực, đồng nhất màu sắc các cửa sổ liền kề; màu sắc chỉ được lấy từ các pixel được vẽ dưới dạng đất liền và độ lệch bờ biển không tính đến màu biển.
- Có một bờ biển nông ở vòng ngoài của mặt nạ đất trong ảnh gốc, còn bên trong bức tranh là biển: khi không có điểm ảnh nào được vẽ là đất gần đó, ảnh được giữ nguyên và không được vẽ bằng màu đất.
- Bờ biển vẫn được cắt bỏ theo mặt nạ ảnh gốc.
- Kết quả được tính là `pack-v5`: trong số 4 pixel hiển thị trên bề mặt, giống với ảnh gốc khi phóng to là 0. 5 khối họa tiết được chia sẻ của Nga ở góc trên bên phải vẫn là ảnh gốc.

## Đường may, viền tím ven biển, làm sắc nét và cận cảnh (27-09-2026)

Nhìn vào tập đầu tiên và các vị trí khác nhau ở phía nam 5604 trên máy thật (ống kính phối cảnh phóng to 1 pixel của ảnh gốc lên 19–30 pixel trong cửa sổ 1440p), có một đường nối ngang ở điểm nối của mỗi hàng gạch, và có một viền màu tím trên bờ biển Libya và Tunisia, tổng thể mềm mại. Hai vị trí đầu tiên nằm trong công cụ:

- **Đường may**: `assemble` Đặt tất cả các hình tứ giác dưới dạng `UNIT` (611/64), nhưng lưới chỉ có 600 đơn vị thế giới (62,85 pixel) khoảng cách hàng và 611 khoảng cách cột. Do đó, mỗi hàng trong câu đố thấp hơn hàng trước 62–63 pixel thay vì 64 và hàng tiếp theo bao gồm một hoặc hai hàng pixel cuối cùng của hàng trước; `pack` rồi cắt đi 64 pixel, phần đầu của khối tiếp theo sẽ được cắt thành phần cuối của khối trước đó. Trong trò chơi, 1 pixel (HD 8 pixel) được hiển thị hai lần, trở thành một đường ngang. Không có đường nối dọc vì khoảng cách hàng chính xác là 64. Bây giờ `pack` sử dụng `tile_span` để lấy phạm vi thực tế của từng mảnh trong câu đố (cho đến mảnh tiếp theo trong cùng một cột, hàng 62–64), sau đó kéo nó trở lại 512×512 (`cut_tile`). Bản thân câu đố không bị thay đổi, gói tạo image_gen và hình ảnh tổng hợp đều được đăng ký theo nó. Kiểm tra offline 52 cặp khối liền kề trên và dưới của 5604: chênh lệch trung bình các hàng liền kề tại ngã ba giảm từ 14,4 xuống 3,4, giống như các hàng liền kề trong một khối.
- **Cạnh Tím**: Vòng ngoài của mặt nạ đất liền trong ảnh gốc là vòng tròn của biển nông, bên trong của tranh là biển. Khi tổng hợp, “giữ nguyên hình ảnh”, trong khi image_gen vẽ vòng tròn biển nông màu tím, trộn màu tím thành dải cát sát bờ biển. `imagegen` Thêm `coast_tidy` vào cuối bố cục: các pixel trong mặt nạ được vẽ dưới dạng nước (xanh lam lớn hơn đỏ và xanh lục) chỉ thay đổi sắc thái thành sắc thái của màu biển trong; mặt trong của bờ biển `COAST_BAND` (10 HD Pixel), dải đất rộng, màu sắc được lấy từ vùng đất nội địa hơn (`land_blur`), giữ nguyên độ sáng riêng và kết cấu của bức tranh không thay đổi; hòn đảo không có nội địa để lựa chọn (`land_blur`, trọng số tiến về 0 sẽ tính toán các màu loang lổ màu xám, vàng và đỏ, đã xuất hiện ở cả hai đầu của Malta) và chỉ thay đổi màu ở những nơi đủ trong đất liền.
- **Làm sắc nét**: Hình vẽ 4x, zoom lên 8x rồi phóng to bằng ống kính, nhìn mềm mại. Bản đồ đất liền tổng hợp là USM tổng thể (`SHARPEN`, bán kính 3, 60%), trước `coast_tidy`.

Đã tổng hợp lại thành `imagegen-2`, nhập lại vào `pack-v5` thành `pack-v6`:

```sh
.venv/bin/python -m tools.hd_ai.worldmap_surfaces imagegen --kit assets/hd-ai/imagegen-kit \
  --output assets/hd-ai/worldmap-surfaces/imagegen-2
.venv/bin/python -m tools.hd_ai.worldmap_surfaces pack --output assets/hd-ai/worldmap-surfaces/imagegen-2 \
  --base-pack assets/hd-ai/worldmap-surfaces/pack-v5 --pack-output assets/hd-ai/worldmap-surfaces/pack-v6 --bind
```

### Đóng cửa sổ xem

Ống kính gần như nhau với mỗi bề mặt: khi đặt ở vị trí trung tâm của màn hình, khoảng 3,2 pixel màn hình (cơ sở 320) đến 1 pixel gốc, tức là khoảng 100×75 pixel gốc trên mỗi màn hình. Cửa sổ cục bộ của image_gen là 384×256 và các pixel gốc được vẽ thành 1536×1024 (4 lần). Khi phóng to lên 8 lần rồi phóng to lên 2,5-7 lần, hình ảnh cận cảnh sẽ bị mờ. Chỉ có thể thực hiện cải tiến bằng cách tạo các cửa sổ nhỏ hơn theo vị trí:

- `closeup-kit`: Tính số lần sử dụng của từng vị trí từ bảng vị trí ROM `801C5310` và các sự kiện cảnh được trích xuất (3D32/3D33 từ trong `assets/original-data/records/stage_events.jsonl`, tổng cộng 827 lần, 458 lần trên bề mặt trái đất), độ bao phủ tham lam theo số: mỗi cửa sổ 120×80 Điểm ảnh gốc (`CLOSEUP`) được căn giữa trên điểm được sử dụng phổ biến nhất không được che chắn vị trí và hấp thụ các vị trí gần trung tâm. `--always` chỉ định vị trí được ưu tiên cho cửa sổ (mặc định là 4, 0, 1, 2 trong tập đầu tiên) và `--count` giới hạn số lượng hình ảnh. Hai ảnh được cung cấp cho mỗi ảnh: `*-input.png` là bản cắt 8 lần (960×640) của cửa sổ này trên ảnh tổng hợp hiện tại (`--base` thư mục đang chạy), `*-source.png` là bản phóng to pixel cứng của ảnh gốc 12 lần (1440×960); các từ nhắc nhở cho phép mô hình duy trì bố cục, màu sắc và phong cách vẽ, đồng thời chỉ làm tăng mật độ chi tiết. Đường bờ biển như trong Hình 2. `manifest.json` ghi lại vị trí cửa sổ (`box`, tọa độ câu đố), vị trí và thời gian được bao phủ; `index.jpg` là hình thu nhỏ.
- `closeup`: Đăng ký `outputs/*-out.png` đã vẽ trở lại cửa sổ ảnh gốc tương ứng, đặt nó lên ảnh tổng hợp 8 lần, tô điểm cạnh 12 pixel gốc để chuyển giao và sử dụng ảnh cơ sở cho Coast alpha, thực hiện lại `coast_tidy` và viết thư mục chạy mới cho `pack`.

```sh
.venv/bin/python -m tools.hd_ai.worldmap_surfaces closeup-kit --base assets/hd-ai/worldmap-surfaces/imagegen-2 \
  --output assets/hd-ai/imagegen-closeup-kit --count 13 --always 4,0,1,2
.venv/bin/python -m tools.hd_ai.worldmap_surfaces closeup --kit assets/hd-ai/imagegen-closeup-kit \
  --base assets/hd-ai/worldmap-surfaces/imagegen-2 --output assets/hd-ai/worldmap-surfaces/imagegen-3
.venv/bin/python -m tools.hd_ai.worldmap_surfaces pack --output assets/hd-ai/worldmap-surfaces/imagegen-3 \
  --base-pack assets/hd-ai/worldmap-surfaces/pack-v6 --pack-output assets/hd-ai/worldmap-surfaces/pack-v7 --bind
```

27-09-2026 Người dùng vẽ xong 13 bức tranh trong Codex, `closeup` được tổng hợp thành `imagegen-3`, gõ vào `pack-v7` và đóng bìa. Tỷ lệ đăng ký nằm trong khoảng từ 0,93–1,02 (image_gen sẽ thu nhỏ khung hình đi một vài điểm phần trăm) và phần đệm `place` sẽ vẽ các sọc trên các cạnh không được vẽ, do đó, đường viền được tính toán từ phạm vi mà bản vẽ thực sự bao phủ (`covered` trong báo cáo). Xem dãy Alps (Vị trí 0) và Ý (Vị trí 2) trong tập đầu tiên trên máy thật: các đỉnh núi và cây cối được xác định rõ ràng, chúng kết nối một cách tự nhiên với các địa điểm xung quanh nơi không có góc nhìn cận cảnh; Atlas (Vị trí 15, không có cửa sổ cận cảnh) chỉ dựa vào độ sắc nét và không có đường nối.

Ảnh mở đầu (vị trí 4) vẫn là ảo: 5603 vẽ các ô giống như 5602, nhưng bản đồ được xoay theo chiều ngang bởi 4 ô (không thể nhìn thấy câu đố theo vị trí đỉnh và ảnh gốc 7 khung được thu nhỏ 15–20 lần để thực hiện hiệu chỉnh NCC với bản đồ bề mặt ban đầu, y hoàn toàn chính xác và chênh lệch x là 256). `locations()` cộng 256 vào x của chỉ số dưới 17 và lấy modulo 576 (`SURFACE_WRAP`); `closeup-kit --extend` giữ lại cửa sổ đã vẽ, chỉ thêm các vị trí mới chưa được che và thêm cận cảnh-14 vào 19, trong đó 14 là cảnh mở đầu. Sáu bức tranh được vẽ trong cùng một ngày và 19 bức tranh được tổng hợp thành `imagegen-3`, được nhập vào `pack-v8` và đóng bìa; cảnh mở đầu của máy thật, Greenland và Nam Mỹ đều là cận cảnh.

Chế độ xem cận cảnh vẫn là bản đồ 8x (máy chủ `graphics.cpp` chỉ chấp nhận các khối thay thế là 512). Lên 16x sẽ phải cho phép kiểm tra chấp nhận 1024 khối và để `pack` cắt riêng 1024 cho các khối cận cảnh, TBD.

## Tiêu

- Bề mặt trái đất: 34 lần, 17,68 nhân dân tệ. Trong số đó, 3 cửa sổ thử nghiệm được sử dụng 5 lần, 20 cửa sổ còn lại được sử dụng 27 lần (trong đó có 7 lần vẽ lại tự động), 5604 được thêm một lần và bức tranh thứ tư về Cao nguyên Tây Tạng được sử dụng một lần.
- Một vài vòng thử nghiệm phong cách hội họa đầu tiên (phong cách hiện thực và tham chiếu bản đồ đơn): 6,76 nhân dân tệ, không hợp lệ.
- Vũ trụ: 4 lần, 2,08 tệ.
- Châu Âu (25-09-2026): `europe-1` 9 lần 4,68 nhân dân tệ (không được thông qua); `europe-2` 10 lần 5,20 nhân dân tệ (một cửa sổ được vẽ lại một lần).
- Thay đổi phong cách vẽ ở khu vực khác: 2 lần thử với giá 1,04 nhân dân tệ; `restyle-*` tổng cộng 46 lần với giá 23,92 nhân dân tệ, khoảng một nửa trong số đó được chi cho việc tự động vẽ lại các phân loại màu mà sau đó đã bị xóa.

## Máy thực tế (24/09/2026, chế độ HD)

- `worldmap-regions` Các cấp độ nhỏ đi đến các vị trí 3 (Trung Á 5605), 18 (Bắc Mỹ 5606), 5 (Toàn Trái đất 5602), 9 (Toàn Trái đất 5603), 0 (Biển Địa Trung Hải 5604).
- Lúc đầu, tôi đọc danh sách vị trí 12 byte và những cái được chọn là 5605, 5603 và ba lần 5604. Không bao gồm Bắc Mỹ và 5602. Sau khi sửa, tôi chạy lại và thấy rằng Trung Á, Bắc Mỹ, Ấn Độ và Thanh Hải-Tây Tạng trên 5602 và Trung Đông trên 5603 đều là HD.
- `worldmap-space` Du lịch đến tất cả 32 địa điểm trong vũ trụ.
- Bề mặt của từng khu vực, bầu trời đầy sao của vũ trụ, trái đất và thiên thạch đã được thay đổi thành HD và cài đặt sẽ được khôi phục sau khi chuyển về hình ảnh gốc.
- Tất cả 1506 bức vẽ về bầu trời đầy sao đã được viết lại, với 0 lỗi nhận dạng.
- Bảng tên: Với gói model gốc, vận hành bằng tiếng Trung, mỗi bảng trong số 7 bảng tên đã được vẽ 7300 lần; màn hình là Oasis, Side 1/2/3/7, phù hợp với bảng tên con tàu (Libra).

## Lệnh

Gói hiện tại `pack-v5` đã được nhập lại vào `pack-v4` vào ngày 25 tháng 9 năm 2026: tất cả bốn bề mặt đều được lấy từ image_gen để tổng hợp `imagegen-1`.

```sh
.venv/bin/python -m tools.hd_ai.worldmap_surfaces imagegen --kit assets/hd-ai/imagegen-kit \
  --output assets/hd-ai/worldmap-surfaces/imagegen-1
.venv/bin/python -m tools.hd_ai.worldmap_surfaces pack --output assets/hd-ai/worldmap-surfaces/imagegen-1 \
  --base-pack assets/hd-ai/worldmap-surfaces/pack-v4 --pack-output assets/hd-ai/worldmap-surfaces/pack-v5 --bind
```

Cách thực hiện `pack-v4` (phiên bản Qianwen):

`pack-v4` đã được nhập lại vào `pack-v3` (bao gồm vũ trụ, đường viền hộp thoại và đường viền HUD chiến đấu) vào ngày 25-09-2026: `restyle-*` được sử dụng cho Trái đất, Trung Á và Bắc Mỹ và `europe-2` được sử dụng cho Châu Âu. 57 khối được vẽ bởi image_gen trong tập đầu tiên không còn được bao gồm trong gói.

```sh
for s in earth central-asia coast; do
  .venv/bin/python -m tools.hd_ai.worldmap_surfaces restyle --output assets/hd-ai/worldmap-surfaces/restyle-$s \
    --from assets/hd-ai/worldmap-surfaces/run-5 --surface $s
  .venv/bin/python -m tools.hd_ai.worldmap_surfaces run --output assets/hd-ai/worldmap-surfaces/restyle-$s --env-file .env
  .venv/bin/python -m tools.hd_ai.worldmap_surfaces compose --output assets/hd-ai/worldmap-surfaces/restyle-$s
done
.venv/bin/python -m tools.hd_ai.worldmap_surfaces compose --output assets/hd-ai/worldmap-surfaces/europe-2
.venv/bin/python -m tools.hd_ai.worldmap_surfaces pack --output assets/hd-ai/worldmap-surfaces/restyle-earth \
  --extra-run assets/hd-ai/worldmap-surfaces/restyle-central-asia --extra-run assets/hd-ai/worldmap-surfaces/restyle-coast \
  --extra-run assets/hd-ai/worldmap-surfaces/europe-2 \
  --base-pack assets/hd-ai/worldmap-surfaces/pack-v3 --pack-output assets/hd-ai/worldmap-surfaces/pack-v4 --bind
```

`pack-v1` Cách tiếp cận ban đầu:

```sh
.venv/bin/python -m tools.hd_ai.worldmap_surfaces prepare --output assets/hd-ai/worldmap-surfaces/run-5
.venv/bin/python -m tools.hd_ai.worldmap_surfaces run --output assets/hd-ai/worldmap-surfaces/run-5 --env-file /path/to/.env
.venv/bin/python -m tools.hd_ai.worldmap_surfaces compose --output assets/hd-ai/worldmap-surfaces/run-5
.venv/bin/python -m tools.hd_ai.worldmap_surfaces pack --output assets/hd-ai/worldmap-surfaces/run-5 \
  --base-pack assets/hd-ai/portrait-matte/v2/pack --pack-output assets/hd-ai/worldmap-surfaces/pack-v1 --bind
.venv/bin/python -m tools.hd_ai.worldmap_space pack --output assets/hd-ai/worldmap-space/run-1 \
  --pack assets/hd-ai/worldmap-surfaces/pack-v1 \
  --backgrounds-from assets/hd-ai/backgrounds/whole-v1 --backgrounds-to assets/hd-ai/backgrounds/whole-v2 --bind
```

`SRW64_BG_DUMP=1` sẽ ghi danh sách hiển thị bản vẽ đầu tiên của nền sprite không có HD vào thư mục đang chạy `background-draws.jsonl`, thư mục này sẽ được dùng để kiểm tra phương pháp vẽ khi nhận được ảnh mới.