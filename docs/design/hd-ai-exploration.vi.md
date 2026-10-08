> **Ngôn ngữ / Language:** [Tiếng Việt](hd-ai-exploration.vi.md) · [English](hd-ai-exploration.en.md) · [中文](hd-ai-exploration.md)

# Độ phân giải cao về giao diện người dùng và kết cấu: Khảo sát lựa chọn AI trên nền tảng đám mây của Alibaba

Ngày điều tra: 2026-09-08. Kết luận: Sử dụng kết hợp việc tái tạo phông chữ/đồ họa thông thường, độ phân giải quá mức trung thực và vẽ lại tổng quát có giới hạn để ưu tiên xác minh nền cắt cảnh và một số ít nội dung trang trí.

Trạng thái tiếp theo: Sau khi người dùng xác nhận, vòng đầu tiên gồm 42 đầu ra mô hình và phát lại bản đồ từng khung hình đã hoàn tất. Sau khi nhìn hình thì Qwen 3.0 Ứng viên 2 được ưu tiên làm avatar; Các biểu tượng đơn vị cơ khí không được xử lý, các ô bản đồ như rừng bị tạm dừng, bản đồ cắt cảnh và đường viền giao diện người dùng không được cải thiện đáng kể và việc tiếp tục tạo bị tạm dừng. Xem [Kết quả đo thực tế và quyết định thủ công bằng cách xem hình ảnh](hd-ai-benchmark.md). Việc điều tra và lập kế hoạch sau đây trước khi gọi điện được giữ lại trong bài viết này. Số lượng, chi phí và hạn chế thực tế phải tuân theo hồ sơ đo lường thực tế.

Lần này, việc xác minh tài liệu chính thức, truy vấn danh mục mô hình chứng nhận về không gian kinh doanh Bailian hiện tại và kiểm tra dự án hiện tại đã được hoàn thành. Không có tác vụ suy luận hình ảnh nào được gửi và không có hình ảnh trò chơi nào được tải lên đám mây; các đánh giá chất lượng sau đây là các giải pháp ứng cử viên và không có sự so sánh hiệu ứng mô hình nào cho trò chơi này.

## Các dịch vụ và bằng chứng hiện có

- Tái sử dụng cấu hình DashScope/Bailian hiện có của dự án SRW Z, thực thi `GET /compatible-mode/v1/models` chỉ đọc trong không gian kinh doanh Bắc Trung Quốc 2 (Bắc Kinh), HTTP 200 và trả về tổng cộng 249 ID mẫu.
- Đã liệt kê các ảnh chụp nhanh `qwen-image-3.0-pro`, `qwen-image-3.0`, `wan2.7-image-pro`, `wan2.7-image` và `qwen-image-2.0-pro-2026-06-22`.
- Bản ghi truy vấn cục bộ: `assets/hd-ai/research/aliyun-hd-2026-09-08/model-catalog.json`. Hồ sơ không chứa thông tin xác thực; khả năng hiển thị trong thư mục được chứng nhận không tương đương với thẩm quyền suy luận, số dư, tín dụng miễn phí, giá thực tế hoặc chất lượng hình ảnh đã được xác minh.
- `imageenhan` của Nền tảng mở Visual Intelligence là một bộ dịch vụ khác sử dụng xác thực RAM/Khóa truy cập đám mây của Alibaba; Không thể sử dụng Khóa API Bailian làm thông tin xác thực cho dịch vụ này. Việc kích hoạt dịch vụ và quyền tài khoản chưa được xác minh lần này.
- Dự án hiện tại đã có thử nghiệm phông chữ độ phân giải cao một khung với danh sách hiển thị thực, xem thử nghiệm thay thế phông chữ tại thời điểm đó (đã xóa). Văn bản có thể được sắp xếp lại từ các phông chữ phác thảo mà không cần dựa vào các mô hình tổng quát để đoán từ. Thử nghiệm này chưa bao gồm công cụ văn bản thời gian thực và tất cả giao diện người dùng.
- Việc triển khai giải mã hình ảnh độc lập của kho hiện tại bao gồm thư viện phông chữ I4; các nội dung khác như bản đồ và bản vẽ dọc vẫn cần xác nhận định dạng tài nguyên, mối nối và nguồn bản vẽ thực tế. Khả năng tài nguyên được giải nén không có nghĩa là tài nguyên đó đã được giải mã chính xác thành hình ảnh có thể thay thế.

## Chọn phương thức theo nội dung

| Tài sản | Phương pháp ưa thích | Mục đích của AI | Những gì phải được bảo tồn |
| --- | --- | --- | --- |
| Văn bản, tên, giá trị, nhãn menu | Phông chữ phác thảo và sắp chữ xác định | Hỗ trợ xác định văn bản hình ảnh chưa đăng ký | Văn bản gốc, ký tự điều khiển, quy tắc kerning, thời gian hiển thị |
| Đường viền, cửa sổ, con trỏ, thanh giá trị | Tái tạo vectơ hoặc tham số, sau đó tạo kết cấu cần thiết | Tham khảo sơ đồ trang trí | Kích thước chính xác, căn chỉnh, các góc của lưới chín ô vuông, sự khác biệt về trạng thái |
| Cắt cảnh nền bản đồ thế giới | Độ tương phản có độ trung thực cao + các ứng cử viên vẽ lại bị hạn chế | Bổ sung các chi tiết kết cấu như núi, mặt đất, mặt biển, v.v. | Đường bờ biển, vị trí thành phố/tuyến đường, khung hình, hình chiếu và bảng màu |
| Nền tĩnh như trong nhà, bầu trời, mặt đất, v.v. | Chỉnh sửa hình ảnh/siêu độ phân giải | Chi tiết và vật liệu sơn bổ sung | Bố cục, phối cảnh, số lượng đồ vật, phong cách vẽ nguyên bản |
| Avatar, chân dung nhân vật, biểu tượng máy móc | Ưu tiên vượt điểm; hãy thử vẽ lại nếu bạn có tham chiếu cài đặt ký tự | Làm sạch các cạnh lởm chởm và các đường bổ sung | Đặc điểm khuôn mặt, quần áo, biểu tượng, cấu trúc cơ khí, đường nét và độ trong suốt |
| Gạch bản đồ chiến thuật | Các loại ô và mối quan hệ nối được xác nhận và xử lý riêng biệt | Ứng cử viên kết cấu bề mặt | Khả năng đọc địa hình, ranh giới lưới, lát gạch lặp đi lặp lại và các đường nối liền kề |
| Hình ảnh động, con trỏ nhấp nháy, hiệu ứng chiến đấu đặc biệt | Xử lý và đánh giá toàn bộ bộ ảnh động | Hỗ trợ địa phương đã được xác minh | Nhận dạng giữa các khung hình, tư thế, phối màu, độ trong suốt và nhịp điệu |

Thử nghiệm đầu tiên tập trung vào các tài sản tĩnh độc lập. Các mô hình sáng tạo thay đổi từng khung hình hoạt hình có xu hướng bị nhấp nháy và lệch hình dạng. Một bức ảnh đẹp thôi là không đủ để chứng minh rằng hoạt ảnh đó có thể sử dụng được.

## Ứng viên mô hình và API

Giá sau đây là giá gốc chính thức được công bố tại Trung Quốc đại lục vào ngày khảo sát; Bailian đến từ khu vực Bắc Kinh và việc sản xuất hình ảnh VIAPI thường sử dụng khu vực Thượng Hải. Đơn vị là RMB, không khấu trừ hạn ngạch miễn phí hoặc giảm giá. Từ bảng này không thể suy ra rằng tài khoản này đã đạt được hạn ngạch.

| Mô hình/Khả năng | Nhân vật được đề xuất | Khả năng và hạn chế đã được xác nhận | Chi phí tham khảo duy nhất |
| --- | --- | --- | --- |
| `qwen-image-3.0-pro` | Ứng cử viên sơn lại chất lượng cao để so sánh chính | Hỗ trợ nhập và chỉnh sửa hình ảnh; khuyến nghị chính thức hiện tại; Đầu ra tệp 2K | 1 đầu vào + 1 đầu ra 2K khoảng 0,52 nhân dân tệ; 1K khoảng 0,27 nhân dân tệ |
| `qwen-image-3.0` | So sánh chi phí hàng loạt của cùng một giải pháp | Hỗ trợ nhập và chỉnh sửa hình ảnh; liệu nó có đủ độ trung thực hay không cần xác minh mẫu của dự án này | 1 đầu vào + 1 đầu ra có giá khoảng 0,20 nhân dân tệ và đơn giá của đầu ra 1K/2K là như nhau |
| `wan2.7-image-pro` | Nhiều hình ảnh tham khảo, sửa đổi cục bộ và đề xuất tính nhất quán về phong cách | Tối đa 9 hình ảnh tham khảo; mỗi hình ảnh có thể có tối đa 2 khung giới hạn; được chỉnh sửa thành tệp 2K, 4K bị giới hạn ở các cảnh hình ảnh Vincentian được chỉ định | 0,50 nhân dân tệ/hình ảnh đầu ra |
| `qwen-image-2.0-pro-2026-06-22` | So sánh hồi quy phiên bản mô hình cố định | Đã sửa ảnh chụp nhanh; tạo và chỉnh sửa hình ảnh; đầu ra cuối cùng vẫn cần được đông lạnh | 0,50 nhân dân tệ/hình ảnh đầu ra |
| `MakeSuperResolutionImage` | Ứng cử viên cơ sở siêu giải quyết trung thực | 1/2/3/4 lần; `Mode` đã bị bỏ qua, việc chuyển nó vào sẽ không ảnh hưởng đến kết quả | 100 quy tắc miễn phí mỗi tháng tự nhiên, vượt quá là 0,02 nhân dân tệ/lần; số dư chưa được kiểm tra |
| `GenerateSuperResolutionImage` | Ứng viên siêu điểm sáng tạo với việc điền chi tiết nhỏ | 1/2/3/4 lần; giao diện không đồng bộ; tỷ lệ khung hình đầu vào không vượt quá 2:1 | Lớp một 0,06 nhân dân tệ/lần |

Các nguồn khả năng: [Tổng quan về mô hình Bailian](https://help.aliyun.com/zh/model-studio/image-model/), [Chỉnh sửa hình ảnh Qianwen](https://help.aliyun.com/zh/model-studio/qwen-image-edit-guide), [Chỉnh sửa hình ảnh Wanxiang](https://help.aliyun.com/zh/model-studio/wan-image-edit), [Siêu điểm bình thường](https://help.aliyun.com/zh/viapi/developer-reference/api-px24vm), [Siêu điểm sáng tạo](https://help.aliyun.com/zh/viapi/developer-reference/api-generated-image-super-score).

Nguồn giá: [Qianwen 3.0 Pro](https://help.aliyun.com/zh/model-studio/qwen-image-3-0-pro), [Qianwen 3.0](https://help.aliyun.com/zh/model-studio/qwen-image-3-0), [Wanxiang 2.7 Pro](https://help.aliyun.com/zh/model-studio/wan2-7-image-pro), [Qianwen 2.0 Pro và ảnh chụp nhanh](https://help.aliyun.com/zh/model-studio/qwen-image-2-0-pro), [Thanh toán VIAPI](https://help.aliyun.com/zh/viapi/product-overview/billing-is-introduced-12).

Độ phân giải siêu cao nói chung "độ trung thực hơn" là một giả định lựa chọn liên quan đến việc vẽ lại tổng quát và không phải là lời hứa về khả năng phục hồi không mất dữ liệu; nó cũng có thể thay đổi các cạnh và chi tiết nhỏ. Không thể khẳng định rằng mô hình khôi phục lại các chi tiết chân thực không có trong ảnh gốc.

`z-image-turbo` là mô hình sơ đồ Vincent không có khả năng chỉnh sửa hình ảnh và không phải là lựa chọn đầu tiên cho độ phân giải cao trung thực. `qwen-image-edit-max`/`plus` trong danh mục có thể được sử dụng để so sánh với các phiên bản cũ nhưng không cần phải mở rộng số lượng mẫu trong đợt đầu tiên. Mô hình hiểu biết trực quan có thể hỗ trợ phân loại, OCR và tìm ra các điểm bất thường, nhưng không thể là mô hình chấp nhận duy nhất.

## Những hạn chế thực sự cần lưu ý khi truy cập

1. **Đầu vào hình ảnh nhỏ**: Điểm siêu bình thường tối thiểu là 32×32, cạnh dài tối đa là 1920/cạnh ngắn 1080 và tệp không vượt quá 5MB; siêu điểm tổng quát tối thiểu là 64×64, cạnh dài không vượt quá 5000, cạnh ngắn vượt quá 1080, sẽ tự động điều chỉnh và tỷ lệ không vượt quá 2:1. Không thể gửi các thanh hẹp và biểu tượng nhỏ tới tất cả các dịch vụ.
2. **Kênh trong suốt**: Thông số đầu vào chỉnh sửa Wanxiang nêu rõ rằng PNG không hỗ trợ các kênh trong suốt. Nội dung trong suốt phải giữ lại mặt nạ gốc độc lập và chỉ gửi vùng RGB cần tạo cho mô hình, sau đó tổng hợp và chấp nhận nó theo quy tắc phác thảo đã đăng ký; hình ảnh nền trắng được tạo ra không thể được sử dụng trực tiếp làm kết cấu trong suốt.
3. **Định dạng đầu ra siêu phân giải**: Độ phân giải siêu cao thông thường thường phải chỉ định rõ ràng PNG; tài liệu nêu rõ rằng PNG sẽ bị ép buộc khi nhập RGBA, nhưng nó có thể tự động được thay đổi thành JPEG khi độ phân giải đầu ra vượt quá 3840×2160. Định dạng, kích thước và alpha thực tế cần được xác minh, không chỉ phần mở rộng tệp.
4. **Lựa chọn khung không bằng khóa pixel**: `bbox_list` của Wanxiang là hướng dẫn chỉnh sửa và không thể sử dụng nó để đảm bảo rằng các pixel bên ngoài khung sẽ không thay đổi. Các khu vực được phép sửa đổi phải được tổng hợp thành các mặt nạ độc lập và các khu vực được bảo vệ được sao chép từ đường cơ sở xác định và kiểm tra sự khác biệt.
5. **Giao diện yêu cầu**: Không thể sử dụng trực tiếp đường dẫn `chat/completions` tương thích với OpenAI của tác vụ văn bản hiện có làm giao diện chỉnh sửa hình ảnh. Hướng dẫn chỉnh sửa Qianwen cung cấp DashScope `MultiModalConversation`, Wanxiang cung cấp `ImageGeneration` và giao diện tạo đa phương thức; mỗi bộ chuyển đổi xây dựng một yêu cầu tương ứng với tài liệu hiện tại.
6. **Kích thước và lời nhắc**: Chọn kích thước đầu ra, tỷ lệ khung hình và kích thước đầu vào theo API mô hình; giữ lại chuyển đổi cắt xén khi cần đệm cạnh. Đối với các kiểu máy hỗ trợ `prompt_extend`, các cuộc kiểm tra tái tạo trung thực phải tắt tính năng mở rộng tự động một cách rõ ràng để tránh thay đổi các từ nhắc nhở bị kiểm duyệt. Đừng cho rằng có một tham số "cường độ vẽ lại" chung cho tất cả các mô hình.
7. **Khả năng tái tạo**: Ảnh chụp nhanh đã sửa, hàm băm đầu vào, tham số yêu cầu và hạt giống rất hữu ích cho việc theo dõi, nhưng tuyên bố chính thức nêu rõ rằng cùng một hạt giống không đảm bảo cùng một đầu ra. Xuất bản sử dụng hình ảnh đã được xem xét và lưu hàm băm, đồng thời không yêu cầu lại mô hình trên bản dựng sản xuất.
8. **Hạn ngạch và lô**: Các giới hạn hiện tại mặc định ở Bắc Kinh được liệt kê trên thẻ chính thức là Qianwen 3.0 Pro 5 RPM, Qianwen 3.0 20 RPM, Qianwen 2.0 Pro Snapshot 2 RPM và Wanxiang 2.7 Pro 300 RPM; giới hạn thực tế có thể bị trả lại tài khoản. "Suy luận hàng loạt không được hỗ trợ" không ngăn khách hàng gửi từng yêu cầu thông thường theo giới hạn hiện tại, nhưng nó không thể áp dụng giảm giá suy luận hàng loạt.

Các thông số kỹ thuật trên được căn cứ vào từng tài liệu mẫu; phiên bản cũ của bảng tham số API chỉnh sửa Qianwen vẫn chưa bao gồm đầy đủ 3.0 và việc triển khai yêu cầu 3.0 phải dựa trên các ví dụ 3.0 hiện tại và xác minh thực tế. [API chỉnh sửa Qianwen](https://help.aliyun.com/zh/model-studio/qwen-image-edit-api)

## Quy trình cụ thể của nền bản đồ cắt cảnh

1. **Trích xuất bản đồ cơ sở hoàn chỉnh**: Xác định vị trí các tài nguyên ban đầu và các mẫu RT64 thực tế, đồng thời không sử dụng ảnh chụp màn hình cuối cùng chứa văn bản, ký tự, dấu và con trỏ làm đầu vào sản xuất. Nếu hình ảnh cơ sở được tải lên theo từng phần, trước tiên hãy khôi phục hình ảnh hoàn chỉnh và các mối quan hệ cắt xén, lật và bảng màu của từng khối.
2. **Thiết lập các lớp bảo vệ cấu trúc**: Đăng ký riêng đường bờ biển, đường, sông, ranh giới và các điểm mốc chính. Các cấu trúc có thể được xây dựng lại từ vectơ hoặc mặt nạ nguyên thủy được vẽ riêng lẻ; kết cấu bề mặt, bề mặt biển và đám mây có sẵn dưới dạng các vùng có thể chỉnh sửa. Văn bản được nướng trong ảnh gốc cũng phải được xây dựng lại riêng biệt.
3. **So sánh cùng một nguồn**: Cùng một hình ảnh gốc lần lượt được nội suy thông thường, siêu phân giải thông thường, siêu phân giải tổng quát, chỉnh sửa hàng nghìn câu hỏi và chỉnh sửa nhiều giai đoạn. Nội suy thông thường đóng vai trò là đường cơ sở trực quan không bổ sung thêm ngữ nghĩa mới.
4. **Nhiệm vụ vẽ lại có giới hạn**: Giữ bảng màu gốc và kiểu vẽ tay, đồng thời chỉ bổ sung kết cấu của vùng có thể chỉnh sửa; mô hình không bắt buộc phải biến bản đồ thành ảnh vệ tinh thực tế. Các bản vẽ tham khảo hỗ trợ được sử dụng để thống nhất nghệ thuật và không được sử dụng để thay thế bố cục không gian.
5. **Tổng hợp xác định**: Tổng hợp các tài liệu đã được phê duyệt theo lớp bảo vệ và vẽ lại tên địa điểm, tuyến đường và điểm đánh dấu. Chuyển về các ô có độ phân giải cao theo mối quan hệ lấy mẫu ban đầu và thống nhất các phương pháp lọc, mở rộng cạnh và tỷ lệ.
6. **Chấp nhận trong thời gian chạy**: Liên kết với hàm băm kết cấu RT64 đã được xác nhận, kiểm tra các đường nối, căn chỉnh sai, quang sai màu, cạnh trong suốt và nhấp nháy mẫu trong khi xoay, thu phóng, chuyển tiếp và làm mờ. Sơ đồ cơ sở cắt cảnh và ô bản đồ chiến thuật sẽ được chấp nhận riêng.

Điểm bắt đầu từ được đề xuất cho bản đồ nền không có từ (các hạn chế về không gian cuối cùng vẫn được đảm bảo bởi lớp cấu trúc và xem xét thủ công):

> Sử dụng Hình 1 làm tiêu chuẩn bố cục không gian duy nhất, giữ nguyên khung hình, hình chiếu, hướng camera và bảng màu tranh gốc. Giữ nguyên vị trí, hình dạng và số lượng bờ biển, sông, đường, đảo và thành phố. Dựa trên phong cách bản đồ chiến lược khoa học viễn tưởng vẽ tay hai chiều ban đầu, độ rõ của kết cấu bề mặt và mặt biển được cải thiện, đồng thời các ngọn núi và thảm thực vật hiện có được tinh chỉnh. Duy trì mối quan hệ màu sắc khối lớn và nhận dạng địa hình. Xuất bản đồ cơ sở bản đồ không có văn bản, nhãn, đơn vị, con trỏ và giao diện, đồng thời không thêm các tính năng mới.

## Gợi ý và chi phí so sánh vòng đầu tiên

Có 6 nội dung gốc được trích xuất và đăng ký: hai bản đồ cắt cảnh với các phong cách khác nhau, nền cảnh, hình đại diện, biểu tượng cơ học và kết cấu trang trí giao diện người dùng. Dưới đây là gợi ý danh mục mẫu, 6 tài nguyên chưa được định vị và đưa vào danh sách thực thi.

Mỗi mẫu:

- Qianwen 3.0 Pro, Qianwen 3.0 và Wanxiang 2.7 Pro mỗi bên yêu cầu độc lập 2 ứng viên (mỗi lần một đầu vào và một đầu ra).
- Qianwen 2.0 Pro đã sửa lỗi chụp nhanh yêu cầu 1 so sánh.
- Một so sánh cho mỗi điểm siêu thông thường và siêu điểm tổng quát. Xác nhận các điều kiện kích hoạt và đầu vào của nó trước khi thêm nó.
- Nội suy thông thường cục bộ được sử dụng làm đường cơ sở bổ sung, bất kể số lượng hình ảnh được tạo ra trên đám mây.

Tổng cộng có 54 bức ảnh được xuất lên đám mây. Ước tính dựa trên mức giá 2K của Qianwen 3.0 Pro, tất cả thông tin đầu vào từ mẫu yêu cầu và mức giá trên của các mẫu máy khác:

`6 × [2 × (0.52 + 0.20 + 0.50) + 0.50 + 0.02 + 0.06] = 18.12元`.

Đây là chi phí của một cuộc kiểm tra tham chiếu chưa được thực hiện và không phải là hóa đơn hoặc ủy quyền ngân sách. Không bao gồm số lần thử lại, hình ảnh tham chiếu bổ sung, lưu lượng lưu trữ và tín dụng miễn phí; không cần phải mua phiên bản GPU hoặc đào tạo mô hình cho vòng thử nghiệm này.

Được xác định trước bởi nội dung thông qua tiêu chí:

- **Đúng về mặt cấu trúc**: Các mốc, đường bờ biển, các bộ phận cơ khí và nhận dạng ký tự không bị giả mạo; thí sinh sai sẽ bị loại ngay cả khi họ sắc bén hơn.
- **Đúng về mặt kỹ thuật**: Kích thước phù hợp với bản đồ kết cấu, các khu vực được bảo vệ vượt qua kiểm tra khác biệt, đường viền trong suốt không có cạnh màu trắng, đường nối gạch chính xác.
- **Hợp lệ trực quan**: So sánh khả năng đọc, tính nhất quán về phong cách và chi tiết ở kích thước hiển thị trò chơi mục tiêu, thay vì chỉ xem bản xem trước tĩnh phóng to.
- **Chạy chính xác**: Hoàn thành việc cuộn, thu phóng, xếp lớp và so sánh hoạt ảnh của cảnh mục tiêu; việc truyền các hình ảnh tĩnh không có nghĩa là chấp nhận hiển thị thời gian thực.
- **Chi phí hiệu quả**: Thống kê về tỷ lệ vượt qua đánh giá, số lượng yêu cầu cho từng nội dung đủ điều kiện và thời gian chỉnh sửa thủ công được sử dụng để xác định mô hình hàng loạt. Giá API duy nhất không phải là toàn bộ chi phí sản xuất.

## Ghi lại và phát hành tài sản tiếp theo

Mỗi mục ghi lại ID tài nguyên gốc, hàm băm hình ảnh nguồn, lấy mẫu/băm RT64, bảng màu và mặt nạ, ID mô hình hoàn chỉnh, ngày gọi, các từ và thông số nhắc nhở, hàm băm ứng viên, kết luận đánh giá, kích thước đầu ra, chuyển đổi thành phần/gạch và bằng chứng thời gian chạy. Những mô hình không cung cấp ảnh chụp nhanh cố định phải được ghi lại dưới dạng phiên bản dịch vụ nổi, với kết quả đầu ra sẽ bị đóng băng sau khi xem xét.

Nội dung HD được mang theo các gói kết cấu RT64 độc lập. Việc tạo AI chỉ diễn ra ở giai đoạn sản xuất ngoại tuyến và kết quả được xem xét sẽ được tải khi trò chơi đang chạy; nội dung có thể được sử dụng lại trên máy tính để bàn/Android và các nền tảng khác, đồng thời định dạng, bộ nhớ video và hiệu ứng lấy mẫu được xác minh riêng. Các chiến lược sản xuất, nén và tải trước gói họa tiết được triển khai theo [Tài liệu gói họa tiết RT64](https://github.com/rt64/rt64/blob/main/TEXTURE-PACKS.md).

Không có sửa đổi nào được thực hiện đối với mã trò chơi, ROM, gói phông chữ hiện có hoặc cấu hình thời gian chạy tại thời điểm này. Thử nghiệm hiệu ứng mô hình, trích xuất nền cắt cảnh mục tiêu và chấp nhận gói HD vẫn là những nhiệm vụ tiếp theo.