> **Ngôn ngữ / Language:** [Tiếng Việt](hd-ai-benchmark.vi.md) · [English](hd-ai-benchmark.en.md) · [中文](hd-ai-benchmark.md)

# SRW64 Vòng thử nghiệm thực tế đầu tiên của hình ảnh độ phân giải cao trên Đám mây Alibaba

2026-09-08. Đã hoàn thành các phép đo trực tiếp của 6 bản đồ nguồn, 4 mô hình chỉnh sửa hình ảnh, 42 đầu ra và gắn bản đồ HD được bảo vệ vào ảnh chụp nhanh danh sách hiển thị RT64/Kim loại thực. Tổng ước tính giá công khai là ** ¥ 17,64**, chưa có hóa đơn thực tế nào được đọc.

**Hướng đi sau khi xem ảnh ở vòng này: Qwen 3.0 Thí sinh 2 là lựa chọn đầu tiên cho avatar hiện tại; Các biểu tượng đơn vị cơ khí không được xử lý, các ô bản đồ chiến thuật như rừng bị hoãn lại, sự cải thiện rõ ràng của bản đồ cắt cảnh và đường viền giao diện người dùng là không rõ ràng và việc tiếp tục tạo bị hoãn lại. ** Văn bản tiếp tục sử dụng phông chữ phác thảo; nếu đường viền cửa sổ cần có độ phân giải cao, lợi ích của việc vẽ quy tắc có thể được xác minh riêng. Lựa chọn này được giới hạn ở mẫu hiện tại và không thể hiện sự chấp nhận gói HD đầy đủ của trò chơi hoặc xếp hạng mô hình tổng thể.

Cập nhật: [Cấu hình nội dung gốc](../native/native-content-foundation.md) riêng biệt đã được tạo, sử dụng đầu ra hình đại diện nhỏ hơn và bản đồ Lanczos 4x cục bộ. Phạm vi lịch sử và kết quả của vòng so sánh mô hình đầu tiên được giữ lại dưới đây.

## Xem lại hình ảnh thủ công (2026-09-08)

- **Avatar nhân vật**: Người dùng tin rằng Ứng viên 2 của `qwen-image-3.0` có tác dụng tốt nhất và sử dụng hình ảnh đã lưu này làm hình đại diện ưa thích hiện tại và điểm chuẩn so sánh tiếp theo. Nó chưa được cài đặt hoặc triển khai cho các nhân vật khác trong trò chơi.
- **Biểu tượng đơn vị cơ khí**: Không cần xử lý và nó sẽ được chuyển ra khỏi phạm vi độ phân giải cao tiếp theo.
- **Rừng và các ô bản đồ khác**: Hiện tại khó giải quyết nên sẽ bị hoãn lại.
- **Cắt bản đồ cảnh**: Người dùng cho rằng độ tương phản không rõ ràng, rút lại đề xuất nâng bản đồ lên trước và giữ lại các ứng cử viên vòng hiện tại cũng như phát lại khung hình đã chụp.
- **Đường viền giao diện người dùng**: Người dùng cho rằng hiệu ứng không đáng kể nên việc tạo tiếp bị hoãn lại; lợi ích của việc vẽ quy tắc/tái thiết lưới chín ô vuông vẫn chưa được xác minh.

Tệp ưu tiên là Avatar Qwen 3.0 Ứng viên 2 (`runs/portrait--qwen-image-3.0--2/output.png`), đầu ra thô SHA-256: `45ac1a1c6719c2c117853f7f8b6844f0117809b55f2b9e2d31d7dfb24e13406f`. Vào thời điểm đó, `review_decisions.json` được sử dụng để ghi lại phạm vi và lựa chọn.

## Tệp vòng hiện tại

> 24-09-2026: Tất cả đầu ra, bản đồ so sánh, bản ghi yêu cầu, bằng chứng phát lại và các trang duyệt cục bộ (`assets/hd-ai/2026-09-08/`) cho vòng này đã bị xóa trong quá trình dọn dẹp HD cũ. Xem `build/cleanup-2026-09-24.tsv` để biết danh sách. Các kết luận, số liệu tại thời điểm đó được giữ lại dưới đây, tên hồ sơ chỉ mang tính lịch sử.

## Kết quả và chi phí của mô hình

| Người mẫu | Xuất thành công | Ước tính giá công khai | Thời gian yêu cầu trung bình của vòng này | Quan sát vòng này |
| --- | ---: | ---: | ---: | --- |
| `qwen-image-3.0` | 12 | ¥2,40 | 41,98 giây | Ứng viên Avatar 2 được chọn làm lựa chọn đầu tiên cho vòng này sau khi người dùng xem ảnh; lợi ích trực quan của bản đồ là không rõ ràng; bức tranh cơ khí nhỏ dễ dàng tái tạo thành hình dạng mới |
| `qwen-image-3.0-pro` | 12 | ¥6,24 | 44,67 giây | Bản đồ châu Âu tương đối ổn định, ứng cử viên đầu tiên được chọn để tổng hợp và phát lại được bảo vệ; avatar vẫn cần được sửa đổi |
| `wan2.7-image-pro` | 12 | ¥6,00 | 10,36 giây | Vòng này trả về nhanh nhất; bản đồ và hình đại diện đáng được lưu giữ làm ứng cử viên; máy móc/rừng có xu hướng giữ lại các khối pixel lớn và các chi tiết hiệu quả mới bị hạn chế |
| `qwen-image-2.0-pro-2026-06-22` | 6 | ¥3,00 | 35,08 giây | Phiên bản cố định rất dễ theo dõi, nhưng các ngọn núi và hình đại diện của bản đồ hình tròn hiện tại được vẽ lại rất nhiều; thành phần của bản đồ cơ học nhỏ rõ ràng đã được thay đổi |

Thời gian thực hiện bao gồm mạng cục bộ, suy luận và tải xuống, đồng thời là giá trị quan sát cho 42 yêu cầu này, không phải là cam kết về hiệu suất dịch vụ. 1 đầu vào hình ảnh, 1 đầu ra hình ảnh cùng một lúc, POST không được tự động thử lại; mọi yêu cầu đều thành công. Chi phí được tích lũy dựa trên [giá công khai ở Bắc Kinh đã được xác minh trước đó](hd-ai-exploration.md) và hạn mức chiết khấu/miễn phí không được khấu trừ, điều đó không có nghĩa là hóa đơn đã được xác nhận.

Tổng cộng **12 kết quả đầu ra của kế hoạch không được thực thi** đối với siêu điểm thông thường và siêu điểm tổng quát: `GetOssStsToken` trả về thành công thông tin xác thực tạm thời, nhưng khi cố gắng chuyển hình ảnh nguồn đầu tiên sang OSS tạm thời của VIAPI, `403 AccessDenied` sẽ được trả về. Kết quả này chỉ có thể chứng minh lần này liên kết tải lên chưa được kết nối và không thể suy ra dịch vụ siêu điểm đã được kích hoạt hay chưa; cả API siêu điểm đều chưa gửi suy luận. Không có thay đổi chính sách RAM, tạo nhóm hoặc mua dịch vụ. Thông tin xác thực tạm thời không được ghi vào đĩa. URL tải lên tạm thời của Bailian được liên kết với mô hình và không thể được sử dụng trực tiếp làm địa chỉ đầu vào chung cho một nhóm dịch vụ khác. [Xử lý tệp VIAPI](https://help.aliyun.com/zh/viapi/getting-started/the-file-url-processing), [Hạn chế URL tạm thời của Bailian](https://help.aliyun.com/zh/model-studio/get-temporary-file-url)

## Nguồn đầu vào và ranh giới áp dụng

| Mẫu | Nguồn | Kích thước/Xử lý | Phạm vi xác thực |
| --- | --- | --- | --- |
| Bản đồ Châu Âu | Danh sách hiển thị mô hình của Resource 5604, các ô CI4 và bảng màu RGBA16 độc lập | 70 mặt hình chữ nhật; khôi phục tập bản đồ theo các đỉnh và lấy toàn bộ khu vực 512×512, lật sang phía bắc | Toàn bộ tài nguyên giống như các byte RDRAM đã thu được; các pixel và bảng màu của 63 họa tiết đã chụp được khớp từng byte |
| Lớp bản đồ châu Á | Resource 5605, mô hình cấu trúc gạch tương tự | Khôi phục hình chữ nhật hiệu dụng của tập bản đồ, sau đó cắt bỏ vùng 640×320 | Giải mã tĩnh và kiểm tra trực quan; Không có ràng buộc thời gian thực/phát lại của cảnh này |
| Hình đại diện | Tài nguyên 29, 96×96 CI8 | TLUT sử dụng tính năng chụp thực tế; suy luận RGB màu xám + nguồn alpha được bảo toàn | Ghi lại các byte tài nguyên phù hợp, bảng màu từ mẫu thực tế |
| Viền trang trí | Vẽ dải tài nguyên 1296 | Cắt `[320,0,400,16]`, đặt trên canvas trong suốt 96×96 | Sử dụng TLUT được chụp thực tế; chỉ là một phần của đường viền, chưa được xác minh toàn bộ lưới chín ô vuông |
| Biểu tượng cơ khí | Tài nguyên 688 + Bảng màu nhóm chia sẻ 1010 | 16×16 gốc, nâng cấp trước hàng xóm gần nhất xác định | Màu sắc phù hợp được kiểm tra trực quan; ánh xạ đơn vị thực tế và hoạt ảnh chưa được xác minh |
| Mẫu rừng | Tài nguyên Atlas 6228 + bảng màu 6237 | Bản cắt Atlas `[272,16,304,48]`, 32×32 | Không phải là một cảnh hoàn chỉnh; phân đoạn ô thật và bản đồ liền kề chưa được phê duyệt |

Nền cảnh thông thường theo kế hoạch ban đầu đã được thay thế bằng các đoạn cắt bản đồ rừng trong vòng này: mặc dù tài nguyên nền cảnh có thể được giải nén nhưng việc kết hợp bảng màu chính xác của chúng vẫn chưa được xác nhận và các màu đoán được không được gửi đến mô hình dưới dạng so sánh chính thức.

Đầu vào có độ phân giải thấp được khuếch đại trước đầu vào lân cận gần nhất để đáp ứng kích thước đầu vào của mô hình chỉnh sửa; điều này không làm tăng thông tin ban đầu. Đầu ra là 2048×2048, mẫu châu Á là 2048×1024. Sự so sánh cuối cùng cũng được thu nhỏ lại về cùng kích thước nguồn/kích thước gấp 4 lần, để tránh đánh đồng kích thước tệp lớn với HD hiệu quả.

Có một hạn chế thử nghiệm rõ ràng trên mẫu châu Á: vùng nước trong ảnh gốc có phần trong suốt và nền màu xám được tổng hợp khi gửi đến mô hình, nhưng các từ gợi ý bản đồ được sử dụng vẫn yêu cầu mặt biển có màu xanh đậm. Đầu vào này không phù hợp với các ràng buộc kịp thời và một số đầu ra cố gắng sơn lại làn nước trong xanh. Các kết quả chỉ được sử dụng để phơi bày các vấn đề với quá trình xử lý lớp trong suốt và không được đưa vào phân loại độ trung thực giữa các mô hình và không được sử dụng làm bản đồ cơ sở có thể xuất bản. Ở vòng tiếp theo, trước tiên phải làm rõ lớp nước và màu nền độc lập, sau đó sửa lại các từ gợi ý đặc biệt.

Các từ nhắc biểu tượng cơ học cũng mô tả cách giải thích cấu trúc cơ thể của hình ảnh có độ phân giải thấp. Sự xuất hiện của quá trình tái tạo toàn bộ cơ thể cho thấy rằng "đầu vào 16 pixel + lời nhắc này" không đủ hạn chế; vòng này không thể quy tất cả sự biến dạng cho chính mô hình đó. Sau khi xem hình ảnh, người dùng đã xác định rằng biểu tượng bộ phận cơ khí không cần phải xử lý và do đó không tiếp tục đi tiếp tuyến đường này.

## Xác minh quyền truy cập thực tế của bản đồ

1. Chọn ứng cử viên đầu tiên cho bản đồ Châu Âu bằng `qwen-image-3.0-pro`.
2. Tạo mặt nạ nước từ bảng màu gốc, giữ lại mức khuếch đại song tuyến xác định của mặt biển và khu vực cách bờ biển khoảng 3 pixel nguồn. Việc kết hợp AI chỉ mang lại kết quả bên trong vùng đất rộng lớn. Sự khác biệt RGB của vùng được bảo vệ so với đường cơ sở này là **0 pixel**; alpha nguồn được phục hồi riêng biệt.
3. Chuyển về các ô 256×256 theo tọa độ bản đồ ban đầu và phép biến đổi lật, đồng thời liên kết **58 giá trị băm RT64** thực sự xuất hiện và nằm trong ô đã chọn. Các ô khác tiếp tục sử dụng tài nguyên ban đầu.
4. Đã xác minh kết xuất thứ 60 ở đầu ra 960×720 bằng RDRAM, OSTask và RT64/Metal thô; GPU đọc khung khi hoàn tất. Gói ô cuối cùng là `map-probe-final/hd-pack-stall`.
5. Tạo một bản đồ khác + gói 22 nét phác thảo hiện có, cho thấy rằng hai đường dẫn của văn bản và nền có thể có hiệu lực cùng một lúc. Phông chữ đến từ thử nghiệm thay thế phông chữ vào thời điểm đó (đã xóa); vòng này không cho phép AI tạo văn bản và cũng không cài đặt các hình đại diện AI chưa được xem xét vào cuộc trình diễn.

Bằng chứng tại thời điểm đó là bốn báo cáo: liên kết tài nguyên và kết cấu, bảo vệ bản đồ và ghi ô, phát lại bản đồ cũng như phát lại kết hợp bản đồ và phông chữ.

Kết cấu bề mặt đã được thêm vào ảnh chụp nhanh này, nhưng người dùng cho rằng sự cải thiện tổng thể là không rõ ràng khi nhìn vào ảnh. Để duy trì đường nét địa lý, bờ biển vẫn giữ được cảm giác bước đi do việc lấy mẫu hạn chế của ảnh gốc mang lại; Chỉ truy cập thành công không có nghĩa là lợi ích trực quan là đủ. Bản đồ lưu giữ các quan sát.

Thử nghiệm kiểm soát giải mã hình ảnh gốc thành PNG và sau đó thay thế nó không đạt được các pixel hoàn toàn nhất quán trong toàn bộ khung hình: so với phát lại không có gói mới của cùng một máy chủ, 32.561 trong số 691.200 pixel là khác nhau và hầu hết các lỗi kênh tối đa là 1; chỉ 100 pixel có lỗi kênh tối đa lớn hơn 2 và lỗi tuyệt đối RGB trung bình là 0,01922/255. Thí nghiệm kiểm soát này không thể được gắn nhãn là không có sự khác biệt. Kết hợp byte kết cấu/bảng màu nguồn và kết xuất cuối cùng giống hệt nhau từng pixel là hai bằng chứng khác nhau.

Xác nhận mục nhập trùng lặp cho RT64 `ReplacementMap::addLoadedTexture` được kích hoạt khi gói HD ban đầu sử dụng `preload`. Để hoàn tất quá trình phát lại cách ly này, gói đã được tải bằng `stall` được hỗ trợ chính thức và đã thu được thành công đầu ra; mã nguồn của trình kết xuất không được sửa đổi và nguyên nhân cốt lõi của xác nhận không được coi là đã khắc phục. Chiến lược tải sản xuất vẫn đang được nghiên cứu. [Phương pháp tải RT64](https://github.com/rt64/rt64/blob/main/TEXTURE-PACKS.md#operation)

## Hướng đi giai đoạn tiếp theo sau khi xem hình

- **Avatar**: Qwen 3.0 Ứng viên 2 là lựa chọn hàng đầu hiện nay. Sau đó, trước tiên chúng tôi sẽ xác minh nguồn tổng hợp Alpha, kích thước hiển thị thực tế của trò chơi và đặc điểm nhân vật gốc, sau đó sử dụng một số ít nhân vật khác để kiểm tra phong cách và độ ổn định danh tính. Đóng băng các đầu ra đã chọn và không coi các mô hình bị thu hồi là các ứng cử viên giống hệt nhau.
- **Văn bản**: Tiếp tục sử dụng font chữ phác thảo.
- **Đường viền giao diện người dùng**: Hiệu ứng xử lý AI không đáng kể và quá trình tạo bị trì hoãn; nếu bạn cần tiếp tục, hãy xác minh riêng đường viền/lưới chín ô vuông được xây dựng lại theo kích thước.
- **Biểu tượng bộ phận cơ khí**: Không được xử lý, vật liệu gốc sẽ được sử dụng.
- **Rừng và các ô bản đồ khác**: Đang tạm dừng, việc tạo và thay thế hàng loạt hiện không được thực hiện.
- **Bản đồ xuyên cảnh**: Giữ lại để quan sát; nếu bạn tiếp tục sau, trước tiên hãy giải thích những lợi ích có thể nhìn thấy dưới màn hình thực tế, sau đó đánh giá phạm vi mở rộng. Các bản phát lại hiện tại chỉ chứng minh liên kết thay thế trong ảnh chụp nhanh và không thay thế quy trình trò chơi thời gian thực cũng như xác minh đa nền tảng.

IoU mặt nạ nước có độ phân giải thấp cho ứng cử viên ban đầu cho Euromap là 0,9779–0,9922; nó phản ánh sự trôi dạt phác thảo thô của mẫu này và không chứng minh rằng danh tính hòn đảo, vị trí núi hoặc chất lượng hình ảnh đều chính xác. "Tỷ lệ vượt qua sản xuất" không được tính toán dựa trên điều này. Tất cả các ứng cử viên vẫn đang là tài liệu thử nghiệm và chưa được phát hành.

## Sự lặp lại và ranh giới tập tin

> 24-09-2026: `extract_samples`, `prepare_samples`, `run_approved_batch`, `review_outputs`, `build_map_probe`, `build_gallery` và `review_decisions.json` dùng trong vòng này đã bị xóa trong quá trình dọn dẹp HD cũ. Các lệnh sau chỉ được sử dụng cho các bản ghi lịch sử; chúng được sử dụng cho các yêu cầu đơn lẻ. `tools/hd_ai/aliyun.py` (trước đây là `run_benchmark.py`).

Tập lệnh lúc đó được đặt tại `tools/hd_ai/`. Hình ảnh được tạo, nội dung được giải mã ROM, bảng màu, bộ nhớ chụp, phần phụ thuộc tạm thời và báo cáo đều nằm trong `assets/hd-ai/` bị bỏ qua; ROM gốc, mã nguồn trò chơi trực tiếp và các gói phông chữ hiện có chưa được sửa đổi. Cam kết/đẩy không được thực thi.

```sh
.venv/bin/python tools/hd_ai/extract_samples.py
.venv/bin/python -m tools.hd_ai.prepare_samples
# 有费用的运行必须沿用冻结清单。已存在请求记录会跳过，不会自动重试 POST。
.venv/bin/python -m tools.hd_ai.run_approved_batch /absolute/path/to/existing/.env
.venv/bin/python -m tools.hd_ai.review_outputs
.venv/bin/python -m tools.hd_ai.build_map_probe
```

Các từ gợi ý của vòng này được lưu trong `prepare_samples` và nó yêu cầu ảnh chụp nhanh/kết cấu kết cấu thực; không phải là một nhà xuất khẩu tài nguyên nói chung đã ly dị với bằng chứng của dự án này. Đầu vào mô hình Châu Âu sử dụng bảng màu gốc của RGB làm sơ đồ cơ sở mờ và gói thời gian chạy cũng khôi phục thêm bảng màu Alpha gốc. Các ứng viên đã tạo không nên yêu cầu lại mô hình trên bản dựng sản xuất.