> **Ngôn ngữ / Language:** [Tiếng Việt](battle-ui-design-brief.vi.md) · [English](battle-ui-design-brief.en.md) · [中文](battle-ui-design-brief.md)

# Giao diện người dùng trước chiến tranh: Hướng dẫn thiết kế tấn công và phản công

Ngày: 21-09-2026. Bài viết này được sử dụng để xem xét thiết kế giao diện và điều chỉnh tiếp theo. Ảnh chụp màn hình máy thực tế (mini cấp tự tạo) lúc đó được dùng làm đường cơ sở hiện tại và không được lưu vào kho; Mục tiêu thiết kế và yêu cầu chấp nhận không có nghĩa là mọi chi tiết hình ảnh đều đạt được hiệu quả cuối cùng.

## Mục tiêu thiết kế

1. **Có thể đưa ra quyết định chiến đấu trước khi xác nhận. ** Người chơi có thể so sánh nhanh chóng đòn đánh, đòn chí mạng, sát thương và khả năng phòng thủ của cả hai bên cũng như thay đổi hoàn toàn vũ khí, sử dụng linh hồn và chọn phương thức phản ứng trên trang hiện tại.
2. ** Bên trái và bên phải đối xứng và mối quan hệ chiến tranh rõ ràng. ** Kẻ thù cố định ở bên trái và chúng tôi cố định ở bên phải; tấn công và phản công theo cùng một bố cục. Phần thân hướng về phía trung tâm, các thông tin tương tự ở cùng độ cao và các giá trị chính dễ dàng so sánh theo chiều ngang.
3. **Tiếp tục giao diện của phiên bản gốc và tiếp thu cách tổ chức thông tin của Machine War Y. ** Giữ lại bảng màu xanh đậm, đường viền màu lục lam và bản đồ chiến trường; tham khảo hình ảnh phản chiếu của Y cả hai bên, khu vực thông tin lái xe, lưới trạng thái tinh thần và khu vực điều hành trung tâm.
4. **Hiển thị kết quả đáng tin cậy và dễ hiểu. ** Lượt truy cập, đòn chí mạng và sát thương phù hợp với giải quyết thực tế. Các tác dụng của tinh thần, kỹ năng, khiên, v.v. phải dễ hiểu đối với người chơi; giao diện không tiết lộ trước kết quả xác định ngẫu nhiên.
5. **Giữ lại cảm giác về vị trí chiến trường. ** Bản đồ và các đơn vị vẫn có thể được nhìn thấy giữa và bên dưới các bảng, ngăn việc xác nhận trước trận chiến chặn hoàn toàn chiến trường.

## Hình 1: Cuộc tấn công chủ động của chúng ta

Cảnh: Vạn Chương ở bên phải chủ động tấn công máy bay địch ở bên trái. Cú đánh chắc chắn và rễ lớn đã được sử dụng, SP còn lại là 18, HP được phục hồi về 3000/3000 và sức mạnh cơ bản không được kích hoạt. Sơ đồ này được sử dụng để xem xét thông tin, trạng thái tinh thần và điểm bắt đầu hoạt động của cả hai bên liên quan đến các cuộc tấn công tích cực.

**Yêu cầu hoạt động**

- Hoạt động chính là "Bắt đầu chiến đấu"; các hoạt động phụ trợ bao gồm "Chọn vũ khí", "Tinh thần", "Bật/Tắt hoạt hình chiến đấu" và "Quay lại lựa chọn".
- Chọn vũ khí sẽ trực tiếp mở danh sách vũ khí. Phạm vi, đạn, EN, năng lượng và các hạn chế về tính khả dụng sau khi di chuyển được giữ nguyên; bản xem trước được tính toán lại sau khi chọn vũ khí và mục tiêu hợp pháp.
- Quay trở lại giao tranh hiện tại sau khi sử dụng linh hồn, giữ lại vũ khí và mục tiêu hợp lệ, làm mới SP, HP, năng lượng, đòn đánh, đòn chí mạng, sát thương và trạng thái khả năng.
- Quay lại lựa chọn mục tiêu hoặc hủy cuộc tấn công không làm tiêu tốn hành động tấn công; linh hồn đã được sử dụng và mức tiêu thụ SP của nó được giữ lại.

## Hình 2: Địch tấn công/ta phản công

Tình huống: Kẻ địch tấn công bên trái, Vạn Chương đáp trả bên phải. Vạn Chương sử dụng nhất định phải né, còn lại 3 SP, đối phương trúng đòn là 0%; chọn lại vũ khí hợp pháp và tiếp tục phản công. HP 1575/3000, EN 75/150, phần bị mất được biểu thị bằng màu đỏ.

**Yêu cầu hoạt động**

- Hỗ trợ ba phản ứng: “phản công”, “né tránh” và “phòng thủ” để làm rõ lựa chọn hiện tại; nút xác nhận hoặc trạng thái liền kề sẽ cho người chơi biết nút nào sẽ được thực thi.
- Bạn có thể thay đổi vũ khí phản công và bạn cũng có thể sử dụng linh hồn trên trang này. Sử dụng tinh thần sau khi chọn né tránh/phòng thủ và giữ nguyên tùy chọn phản ứng khi quay lại; chọn lại vũ khí phản công hợp pháp và chuyển về phản công.
- Khi việc tránh/phòng thủ ngăn cản chúng ta tấn công, giá trị tấn công sẽ được hiển thị là "-" và sẽ giải thích lý do. Chiều cao thẻ và vị trí thông tin sẽ được giữ ổn định.
- Khi cuộc tấn công của địch đã được thiết lập, không có lối vào hủy bỏ thông thường để thoát khỏi giao tranh; việc đóng menu tinh thần sẽ chỉ quay lại trang phản hồi.

## Nhu cầu chung của cả 2 trang

| Khu vực thông tin | Hiển thị và hành vi bắt buộc |
| --- | --- |
| Cơ thể và phi công | Hình ảnh lớn của cơ thể, tên của cơ thể, hình đại diện và tên của người lái xe, cấp độ và sức mạnh. Hai bên của máy hướng vào nhau; avatar của tài xế vẫn giữ nguyên hướng ban đầu. |
| Tài nguyên | HP và EN hiện tại/tối đa của cả hai bên, SP hiện tại/tối đa của người lái xe. HP/EN hiện có một phần màu xanh lá cây và đã mất đi một số màu đỏ; hướng điền bên trái và bên phải được phản ánh và các giá trị nhất quán với độ dài thanh. |
| Vũ khí | Tên vũ khí hiện tại, mức tiêu thụ EN/đạn, đòn đánh của vũ khí và hiệu chỉnh đòn chí mạng; các tùy chọn không có sẵn cho biết các hạn chế. Việc chỉnh sửa vũ khí đã được đưa vào xác suất cuối cùng và không thể thêm lại. |
| Xem trước cốt lõi | Tỷ lệ trúng đích, tỷ lệ trúng đòn chí mạng, sát thương trên đòn đánh và sát thương chí mạng của cả hai bên. Làm nổi bật các giá trị chính và đặt các giải thích nhỏ ở các khu vực hoặc chi tiết lân cận. |
| Trạng thái tinh thần | Tinh thần mà cả hai bên đã học được và hiện đang có hiệu lực được thể hiện trên lưới trạng thái. Màu xám khi không có hiệu lực, được đánh dấu khi có hiệu lực; các loại phục hồi tức thời không được hiển thị dưới dạng các phép bổ trợ liên tục. Hiển thị tên để tránh thể hiện trạng thái chỉ bằng màu sắc. |
| Lựa Chọn Tinh Thần | Mỗi phi công trên máy bay tham gia của chúng tôi lần lượt hiển thị tinh thần có được, SP hiện tại, mức tiêu thụ và trạng thái sẵn có; không được phép thấu chi, khấu trừ sai sót nhiều lần hoặc tiêu thụ SP của phi công khác. |
| Phòng thủ đặc biệt | Cả hai bên đều hiển thị xác suất chém, phòng thủ bằng khiên và phân thân. Giải thích các hạn chế về trang bị, cấp độ kỹ năng, sức mạnh, phạm vi tấn công được đảm bảo, liệu vũ khí có thể bị cắt đứt hay không, v.v.; đây là những xác suất có điều kiện của mỗi phán đoán và không thể cộng trực tiếp. |
| Khiên | Dựa trên loại khiên thực tế và thuộc tính vũ khí của trò chơi này, nó sẽ hiển thị liệu nó có được áp dụng hay không, khả năng vô hiệu hóa/giảm sát thương/xuyên thủng, thay đổi sát thương và mức tiêu thụ EN. Bạn không thể đánh giá chỉ dựa vào việc tên vũ khí có chứa "tia" hay không. |
| Hiệu ứng khả năng | Sức mạnh cơ bản, con người mới/thế giới con người được nâng cao, chiến binh thần thánh, siêu năng lực và các khả năng khác ảnh hưởng đến đòn đánh, né tránh, phòng thủ, cấp độ hiển thị, liệu lần này nó có hiệu lực hay không, những điều chỉnh cụ thể và lý do không có hiệu lực. Sức mạnh cơ bản được làm mới với lượng HP hiện tại và phần thưởng áo giáp từ các tác phẩm khác không được sử dụng. |

## Chấp nhận bố cục và tương tác

- Các thẻ ở cả hai bên có chiều rộng và chiều cao bằng nhau, các khu vực HP/EN, danh tính, tinh thần, vũ khí, giá trị cốt lõi, phòng thủ đặc biệt và khả năng được căn chỉnh theo từng dòng. Không thể nâng toàn bộ thẻ lên vì một mặt có nhiều nội dung hơn.
- Hit, thiệt hại và phản ứng hiện tại được hiển thị đầu tiên; chỉnh sửa chi tiết cho phép cuộn độc lập, nhưng không thể thoát ra khỏi vùng thao tác chính. Những cái tên dài và những ô trạng thái tinh thần không thể chồng lên nhau hoặc che khuất dữ liệu chính.
- Khi menu tinh thần mở, các thao tác nền không thể được kích hoạt; các phím mũi tên và Tab chỉ duyệt qua các tùy chọn hiện có. Esc đóng menu con trước và phím xác nhận không thể xâm nhập vào bản đồ.
- Hoàn thành thao tác thông qua chuột và bàn phím. Sau khi thay đổi vũ khí, sử dụng linh hồn và chuyển đổi phản ứng, tất cả các giá trị liên quan sẽ được làm mới đồng thời.
- Dưới các cửa sổ logic của tiếng Trung 960×720, tiếng Anh 800×600 và tiếng Nhật 1100×760, các nút chính hiển thị và có thể hoạt động được, đồng thời cấu trúc bên trái và bên phải vẫn nhất quán.
- Xác minh bằng bản dựng gốc mới → Menu chính → Cấp độ nhỏ được tùy chỉnh; sử dụng giao diện gỡ lỗi hiện có, thay đổi SP/tài nguyên thực tế và chấp nhận ảnh chụp màn hình GPU.

## Ranh giới hiện tại và vòng tập trung trực quan tiếp theo

- Tinh thần chọn mục tiêu trên bản đồ cũng như tự hủy và hồi sinh hiện bị tắt trên trang trước chiến tranh và lời nhắc vào bản đồ; trang hiện tại không bao gồm quá trình lựa chọn mục tiêu bản đồ.
- Trong màn phản công lúc đó, “0% trúng đích” vẫn được đặt cạnh sát thương có điều kiện. Trong tương lai, ý nghĩa “sát thương khi đánh” nên đặt gần giá trị để tránh bị hiểu là chắc chắn phải nhận sát thương này.
- Nút xác nhận phản công hiện tại vẫn ghi "Bắt đầu chiến đấu"; trong tương lai, "Bắt đầu phản công/Tránh/Phòng thủ" có thể được hiển thị dựa trên phản hồi để củng cố trạng thái hoạt động hiện tại.
- Phần có nhiều thông tin hơn hiện yêu cầu cuộn để xem một số chỉnh sửa. Những điều chỉnh tiếp theo nên ưu tiên hiển thị các giá trị số chính và trạng thái khả năng, sau đó nén và lặp lại các giải thích, đồng thời tiếp tục giữ lại không gian bản đồ.

Ảnh chụp màn hình được lấy từ `actions-zh-Hans.png` và `counter-ready.png` của lần chạy gỡ lỗi cục bộ và kiểm tra lần chạy tương ứng là `action-checks.json`; các tệp cục bộ này không được lưu cùng với kho.

Để biết chi tiết triển khai, hồ sơ xác minh và tầm cỡ công thức, hãy xem [Tài liệu kỹ thuật giao diện người dùng trước chiến tranh](native-battle-ui.md).