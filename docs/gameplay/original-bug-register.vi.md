> **Ngôn ngữ / Language:** [Tiếng Việt](original-bug-register.vi.md) · [English](original-bug-register.en.md) · [中文](original-bug-register.md)

# SRW64 lỗi gốc và đăng ký hành vi khó hiểu

Ngày điều tra: 16-09-2026. Phạm vi: Báo cáo "スーパーロボット大戦64" được công bố trực tuyến được sử dụng để so sánh và tái tạo phiên bản gốc Rev 0 tiếng Nhật của dự án này. **Đây là danh sách báo cáo, không phải danh sách các lỗi đã được dự án này xác minh hoặc sửa chữa và cũng không tuyên bố là đã hoàn thành. ** Không có lượt chơi lại nào được chạy, lý do mã được xác nhận hoặc luật chơi đã thay đổi trong vòng này.

Các nguồn bao gồm báo cáo trực tiếp của người chơi, hướng dẫn cá nhân và wiki cộng đồng. Hồ sơ từ nhiều địa điểm không có nghĩa là xác minh độc lập; mối quan hệ in lại, phiên bản ROM và việc sử dụng máy/trình giả lập thực thường không rõ ràng. Cái “đáng lẽ phải có” trong chiến lược không thể được sử dụng trực tiếp như một công thức sửa sai, đặc biệt không thể áp dụng các quy tắc của các công tác chiến đấu cơ giới khác. Các nguồn được lấy vào ngày trên; video chỉ được xác minh bằng mô tả và thông tin chương chứ không phải từng khung hình.

## 1. Phản hồi của cộng đồng này phù hợp với lộ trình như thế nào?

Các câu trả lời của Reddit được người dùng chuyển tiếp đặt bỏ qua hoạt ảnh chiến đấu trước, sau đó là sửa lỗi kỹ năng của trình điều khiển và đề xuất thêm bản xem trước và xác nhận trước khi chuyển đổi Wing→Endless Waltz. Mô tả về việc thừa kế vũ khí của anh ta có tính chất thu hồi và không có thân máy, vũ khí, kho lưu trữ hoặc liên kết vĩnh viễn cụ thể nào đến bài đăng được đưa ra.

| Phản hồi | Đang xử lý |
| --- | --- |
| Hoạt hình chiến đấu có thể được bỏ qua | Tương ứng với lộ trình B01; nó là một yêu cầu chức năng. Phần trình diễn bỏ qua đoạn hội thoại hiện tại không thể được coi là bỏ qua hoạt ảnh chiến đấu đã hoàn thành. |
| Lỗi kỹ năng lái xe | Được chia thành BUG01-03, xem BUG02 để biết những khác biệt liên quan trong phòng thủ đặc biệt; sau khi xuất hiện lại từng mục, các sửa đổi quy tắc tùy chọn sẽ được nhập và số dư của phiên bản gốc sẽ không bị thay đổi âm thầm. |
| Xem trước và xác nhận EW | Được đánh dấu là QOL01, truy cập vào quy trình bảo trì/ngân sách sửa đổi M2; đầu tiên hãy xác minh các điều kiện thay thế ban đầu và lập bản đồ vũ khí. |
| Một số vũ khí không được kế thừa chính xác | Được đánh dấu là LEAD01. Vẫn chưa thể xác định rằng EW là cụ thể, cũng như "sự biến mất của vũ khí" không thể tự động tương đương với "sự mất mát của một bản sửa đổi vũ khí vẫn còn tồn tại". |

## 2. Danh sách ứng cử viên lỗi

**Trạng thái cục bộ của các mục trong bảng sau ban đầu được sao chép**; sau đó, nguyên nhân của BUG01–04 (2026-09-17, quy tắc tùy chọn) và BUG05 (2026-09-18, [Sửa chữa cơ bản](base-fixes.md)) có hiệu lực theo mặc định đã được xác nhận và phần còn lại vẫn đang được sao chép. “Có các bước cụ thể”, “nhiều hồ sơ” và “nguồn khác nhau” chỉ cho thấy bản chất của bằng chứng bên ngoài. Những sửa đổi làm thay đổi sự cân bằng giữa điểm mạnh và điểm yếu được thực hiện thành các quy tắc tùy chọn; Giống như BUG05, trong đó "trò chơi không nhất quán với dữ liệu của chính nó và việc sửa chữa không thay đổi bất kỳ cài đặt gốc nào", việc sửa chữa cơ bản sẽ được thực hiện theo nguyên tắc phân loại của lộ trình. Các mục khác trước tiên phải được chứng minh là bất thường thay vì các quy tắc về cốt truyện/tài nguyên.

| ID | Hiện tượng được báo cáo trực tuyến | Điều kiện, tranh chấp và nguồn | Phân loại sơ bộ |
| --- | --- | --- | --- |
| LỖI01 | Cấp độ siêu sức mạnh (ESP) không ảnh hưởng đến một số điều chỉnh và thiếu phần thưởng sức mạnh tấn công | Dữ liệu của Nhật Bản cho biết cả đòn đánh và đòn tránh đều cố định ở mức +64; Akurasu Bugs tuyên bố rằng chỉ có khả năng tránh +64. Bạn không thể trực tiếp chọn một kết luận đo lường thực tế. [S1][S2][S3] | Sửa đổi quy tắc; kiểm tra đòn đánh, né tránh và sức tấn công riêng biệt |
| LỖI02 | Khả năng né tránh của Aura Warrior được cố định ở mức +32 và thiếu khả năng điều chỉnh sức mạnh tấn công của Hyper Aura Slash | Cũng có báo cáo cho rằng khả năng điều chỉnh của Aura Barrier cao hơn trong sách chiến lược. Bảng kỹ năng vẫn liệt kê các công cụ sửa đổi rào cản thay đổi theo cấp độ, vì vậy nó không phải là "tất cả các hiệu ứng đã được sửa". [S2] [S4] [S5] | Sửa đổi quy tắc; Kiểm soát rào cản một mình |
| LỖI03 | Khả năng điều chỉnh lượt đánh và tránh quá cao | Akurasu nặng gấp đôi và L9/HP 10% là +100; bảng tiếng Nhật liệt kê +90 ở vị trí tương ứng. Tất cả các giá trị, ngưỡng và bảng dự kiến ​​tối đa đều cần được xác minh. [S1][S2] | Sửa quy tắc; không thể trực tiếp chia mọi thứ thành hai |
| BUG04 | Phản ứng giới hạn không thực sự hạn chế việc đánh/né tránh | Lời nhắc văn bản màu đỏ ban đầu có thể không nhất quán với việc giải quyết thực tế; sửa đổi giới hạn vẫn tham gia vào ngưỡng thay thế EW dòng W và không thể xóa hoàn toàn thuộc tính này. [S1][S6] | Sửa đổi quy tắc; Giao diện người dùng và các phần phụ thuộc có điều kiện được xử lý riêng |
| LỖI05 | Số lượng phân thân khi địch năm ruồi bị ảnh hưởng bởi số lần tiêu diệt trước đó | Dữ liệu chỉ ra "Miền không gian quyết định Phần 1" của Quân đội Độc lập và "Tương lai của sự sống và cái chết" của OZ; nó không phải là "21 lần" cố định. **2026-09-18 Tái diễn và xác nhận nguyên nhân**, xem cập nhật bên dưới. [S5][S6] | Tương ứng với FIX01; đã được coi là bản sửa lỗi cơ bản có hiệu lực theo mặc định |
| LỖI06 | Sau khi nhân vật chính ngoài đời thực rời khỏi OZ, Wan Zhang/Titan 3 xuất hiện trong đoạn hội thoại nhưng không thể chơi | Sau khi chiến lược đã định vị được "そのkenに心素して"; ở giai đoạn sau, "Haruka no Gamble", người đã đến vũ trụ Miya có thể được thêm vào, nhưng vòng tròn trái đất còn lại sẽ tiếp tục vắng bóng. [S6] | Tương ứng với FIX02; tính nhất quán của đội và cốt truyện |
| LỖI07 | Quá trình chuyển đổi đã được thiết lập lại sau khi Spiegel rời đội và gia nhập lại | Mục nhập đơn vị nằm ở Cao nguyên Guyana liên quan đến việc rời/gia nhập lại đội; không biết liệu tất cả các tuyến đường và tất cả các trường chuyển đổi có bị ảnh hưởng hay không. [S7] | Tương ứng với FIX03; phân biệt đầu tiên giữa việc tham gia tạm thời vào cuộc chiến và tham gia lâu dài |
| BUG08 | Reznar → Việc sửa đổi súng phun lửa bị mất khi cường hóa Reznar | Akurasu đã liệt kê rõ ràng nó là "có thể thiếu sót/lỗi"; một số người chơi đã thảo luận về việc không được thừa kế cùng một loại vũ khí. Người ta vẫn chưa chứng minh được liệu đó là do lập bản đồ sai hay do quy tắc thay thế vũ khí. [S8][S9] | Tương ứng với FIX04; Nghi ngờ về việc thừa kế vũ khí |
| LỖI09 | Menu các bộ phận nâng cao vượt quá khe cắm, có thể vượt quá thiết bị khe cắm và phá hủy trạng thái đang chạy | Wiki ghi lại rằng con trỏ trên A+ nằm ngoài giới hạn; Các tầng 5ch 573, 574 và 576 (2022-06) có nỗ lực cá nhân, giá trị bất thường/thay đổi trình điều khiển/báo cáo sự cố màn hình đen. Phạm vi viết thực tế và tác động lưu trữ chưa được xác nhận. [S5][S10] | Đã thêm FIX05; kiểm tra đầu vào/ranh giới, mức độ ưu tiên tái diễn |

"+64", "+32", v.v. tuân theo ký hiệu dữ liệu. Vòng này chưa xác nhận liệu chúng là giá trị nội năng, tỷ lệ phần trăm tỷ lệ trúng đích cuối cùng hay vật phẩm chỉnh sửa trung gian; chúng không thể được nhân trực tiếp với tỷ lệ phần trăm khi thực hiện. Phần thưởng chí mạng của sức mạnh cơ bản cũng phải được đo lường độc lập và từ vấn đề đánh/né đòn không thể suy ra rằng đòn chí mạng cũng có lỗi.

**Cập nhật 2026-09-17 (BUG01–04)**: Lý do đã được tìm thấy trong mã và một sửa đổi quy tắc tùy chọn đã được thực hiện và quy tắc này bị tắt theo mặc định. Xem [Sửa quy tắc tùy chọn](rule-fixes.md). Điểm chính: Chức năng điều chỉnh của siêu năng lực và chiến binh thánh thiện là chức năng trống. Những gì người gọi nhận được chính là cờ kỹ năng (64, 32), được cộng hoặc trừ trực tiếp theo tỷ lệ phần trăm tỷ lệ trúng đích, bất kể cấp độ và nó cũng có hiệu lực ở cấp 0; siêu năng lực có sẵn ở cả tấn công và phòng thủ, trong khi các chiến binh thánh thiện chỉ có mặt phòng thủ; cũng không có vật phẩm sức mạnh tấn công trong công thức sát thương. Các giới hạn chỉ được sử dụng cho màu cảnh báo trang trạng thái, sửa đổi và điều kiện EW, đồng thời không đọc được công thức nhấn. Bảng sức mạnh cơ bản tối đa là 90, cấp HP sớm hơn hai dữ liệu một cấp, các đòn đánh, né tránh và chí mạng có cùng giá trị; câu lệnh "2 lần" không khớp với giá trị tối đa của mã và hiệu chỉnh giảm một nửa chỉ được cung cấp dưới dạng tùy chọn cơ sở yếu. Đầu dò máy thật đã kiểm tra sự thay đổi số của từng lần hiệu chỉnh theo công thức.

**Cập nhật 2026-09-18 (BUG05)**: Nó đã được sao chép và lý do đã được xác nhận trong mã. **Là bản sửa lỗi cơ bản có hiệu lực theo mặc định và không có nút chuyển**, hãy xem [Bản sửa lỗi cơ bản](base-fixes.md). Những điểm chính: Hồ sơ điều khiển của đơn vị địch `+0x14` là số lượng nhân bản, và trường tương tự của đơn vị chúng tôi là số lần tiêu diệt được; năm phi công dòng W cũng có các bảng dự phòng tiêu diệt liên tục `801614E0`, `800A5054`. Khi tạo bản ghi trình điều khiển mới, bản sao lưu được ghi lại vào `+0x14`, được sử dụng để giữ lại số lần tiêu diệt được sau khi rời nhóm và gia nhập lại, nhưng nó không kiểm tra trại. Hồ sơ triển khai hai kẻ địch của Wu Fei không có vị trí giả nên số vị trí giả mà anh ta có khi gây thù địch là số lần tiêu diệt cộng dồn của bên ta (giới hạn trên là 999, không phải cố định 21). Việc tiêu thụ hình nộm sẽ không ảnh hưởng đến việc sao lưu và số lần tiêu diệt được sẽ được khôi phục như bình thường khi tham gia lại.

## 3. Thiết kế tái sản xuất (dự án này đã được lên kế hoạch nhưng chưa triển khai)

| Đối tượng | Thử nghiệm tối thiểu và bằng chứng được giữ lại |
| --- | --- |
| BUG01 Siêu năng lực | Thay đổi từng cấp độ kỹ năng trong cùng điều kiện chiến đấu, tăng trưởng trình điều khiển, địa hình, sức mạnh, tinh thần, tình yêu/tình bạn riêng biệt; ghi lại giá trị hiển thị lượt truy cập, đầu vào giải quyết thực tế, tránh và thiệt hại không nghiêm trọng. Phải che kỹ năng/không kỹ năng và vừa địch vừa thân để tránh kẹp 0%/100% nhằm che đậy sự khác biệt. |
| BUG02 Thánh Chiến Binh | Kiểm tra độc lập khả năng tránh, sức tấn công của vũ khí được chỉ định và ngưỡng rào cản; Việc so sánh kỹ năng L1/L5/L9 không thể chỉ dựa vào một đòn hay một sát thương. Giữ các giá trị vũ khí cơ bản và điều chỉnh độ phân giải, đồng thời kiểm tra các điều kiện tài nguyên và vũ khí hiện hành của rào chắn. |
| BUG03 Sức mạnh cơ bản | So sánh hai chiều giữa cấp độ kỹ năng và tỷ lệ HP, lấy giá trị trước và sau các ranh giới 10%, 20%, v.v.; loại trừ sự khác biệt làm tròn, ghi lại các cú đánh, tránh và các đòn chí mạng tương ứng mà không lập trình trước +90 hoặc +100. |
| Giới hạn BUG04 | Chọn các phản ví dụ có tổng khả năng thấp hơn/cao hơn giới hạn và thay đổi giới hạn riêng lẻ; so sánh chữ đỏ, xem trước trận chiến, giải quyết thực tế và trình độ chuyển đổi hoàn toàn EW. |
| BUG05 Năm bay | ~~Thiết lập các trạm kiểm soát trước khi rời đội với số lần tiêu diệt khác nhau và đếm mức tiêu thụ thực tế của cơ thể giả sau các sự kiện thù địch trên cùng một tuyến đường~~; Cấp độ nhỏ `wufei-dummy.json` đã được sử dụng để hoàn thành "Tiêu diệt → Rời khỏi đội → Kẻ thù xuất hiện" ở một cấp độ và kiểm tra các trường, xem cập nhật bên dưới. Việc so sánh số lượng tiêu diệt khác nhau trên lộ trình ban đầu và kết quả sau khi thêm chúng vẫn chưa được đề cập. |
| BUG06 Vạn Chương | Loại thực nam và nữ × OZ được báo cáo là ví dụ tích cực, siêu loại × OZ, loại thực × quân đội độc lập là những ví dụ ứng cử viên; giữ lại danh sách trước và sau khi tham gia sự kiện, danh sách các đòn tấn công có sẵn, cờ lộ trình và trạng thái bất đồng sau này. |
| BUG07 Spiegel | Trước khi rời nhóm, hãy đặt số lượng các giai đoạn sửa đổi cơ thể/vũ khí có thể phân biệt được và ghi lại các trường hợp thành phần; kiểm tra sau khi thêm chúng lần lượt, kiểm tra các phiên bản đơn vị mới và cũ cũng như các lệnh gọi khởi tạo và không cần tạo bản sao lưu để bao gồm tất cả trước khi thêm. |
| BUG08 Kế thừa vũ khí | Đặt các mức sửa đổi khác nhau trên các loại vũ khí khác nhau của máy cũ và so sánh từng ID vũ khí, tên, giá trị sửa đổi và sức mạnh cơ bản thông qua tập lệnh thay thế máy thực; ít nhất phải bao quát được con đường thay thế OZ/Quân đội Độc lập được liệt kê trong hướng dẫn. |
| BUG09 Phần ngoài giới hạn | Sử dụng kho lưu trữ cách ly để kiểm tra A/ trên cùng một khung và đầu vào khung liền kề trên trang chuẩn bị nơi số lượng phần lớn hơn số lượng vị trí. Trước tiên hãy quan sát con trỏ và ranh giới viết, sau đó kiểm tra kho bộ phận và các trường thân/thí điểm; không sử dụng trạng thái sự cố làm phán đoán duy nhất và không chạy các kho lưu trữ được sử dụng phổ biến. |

Yêu cầu chung: khóa nhận dạng ROM, xây dựng máy chủ lưu trữ, đầu vào, điểm kiểm tra và môi trường tham chiếu ban đầu; phân biệt các lỗi ban đầu với các lỗi do recomp đưa ra. Việc sửa đổi một biến duy nhất trong quá trình chẩn đoán phải được đánh dấu là thử nghiệm có kiểm soát và không thể ngụy trang thành trạng thái thu được bằng quy trình thông thường. Thời gian ngẫu nhiên ban đầu được giữ nguyên; Sự khác biệt RNG do thời gian kết xuất được báo cáo riêng.

## 4. Wing → EW: Đầu tiên, tách riêng "thay đổi" và "kế thừa"

### LEAD01: Vẫn chưa biết vũ khí nào có lỗi.

Phần phụ của Reddit không đặt tên cho vũ khí. Thông tin hiện tại đủ để xây dựng danh sách kiểm tra, nhưng chưa đủ để khẳng định đã tìm ra nguyên nhân cụ thể của "Lỗi kế thừa vũ khí EW".

| Tình huống | Dữ liệu hiện có và xử lý |
| --- | --- |
| W Máy giai đoạn đầu → TV Máy giai đoạn cuối | Hồ sơ Akurasu không kế thừa sự biến đổi cũ và cỗ máy giai đoạn cuối có ba giai đoạn. Đây là một ứng cử viên cho quy tắc thay thế máy và không tương đương với việc mất máy → EW sau này. [S8] |
| Máy truyền hình sau → EW | Hướng dẫn tiếng Nhật ghi lại trigger khi tất cả các hạng mục của máy đã đầy. Những thay đổi về vũ khí cùng tồn tại với sự kế thừa một phần; chúng nên được xác minh từng mục một chứ không chỉ so sánh tổng sức chiến đấu. [S11] |
| Vũ khí biến mất trong EW | Tập trung vào việc kiểm tra vũ khí tầm xa của sa mạc, Khiên Buster của Reaper, Dao quân đội được trang bị vũ khí hạng nặng và Pháo tia của Rồng hai đầu; "vũ khí không có phần tiếp theo" không trực tiếp có nghĩa là một bản sao bị thiếu của chương trình. [S11] |
| EW đi kèm với vũ khí MAP bổ sung | Vũ khí MAP bổ sung cho Zero và Heavy có thể được lấy trực tiếp sau khi thân máy bay được sửa đổi hoàn toàn và không nhất thiết phải vũ khí tương ứng phải được sửa đổi hoàn toàn trước; chúng được liệt kê là xác minh hành vi ban đầu và không thể xóa nếu không được phép. [S11] |
| Các bộ phận không còn trên thân máy sau khi tự động xuất kích | Akurasu ghi lại rằng các bộ phận sẽ được tháo ra khi thay máy và xuất kích tự động. Hàng tồn kho phải được kiểm tra trước và "dỡ hàng" không được báo cáo nhầm là "đã phá hủy". [S8] |

### QOL01: Xem trước và xác nhận thay thế (kế hoạch)

EW không trở nên mạnh hơn theo một hướng đối với tất cả các phương pháp sử dụng: các ô thành phần được ghi trong tài liệu có thể bị giảm, tầm bắn của Desert/Reaper bị rút ngắn và Zippleback mất đi khẩu pháo tầm xa. [S11] Điều này hỗ trợ việc bổ sung các trang xác nhận, nhưng không chứng minh rằng bản thân những thay đổi đó là lỗi.

Các yêu cầu thiết kế được đề xuất bởi dự án này:

- Trước khi kích hoạt thanh toán cho lần sửa đổi cuối cùng của việc thay thế máy bay, hãy hiển thị khả năng phía trước và phía sau, tăng giảm vũ khí, tầm bắn/mức tiêu thụ, kế thừa sửa đổi vũ khí và đích đến thành phần; cho phép giấu tên của chiếc máy bay kế nhiệm.
- Khi hủy, số tiền, sửa đổi, vũ khí, linh kiện và cờ sẽ không thay đổi; khi xác nhận, các điều kiện thực tế sẽ được kiểm tra lại và gửi một lần.
- Mặc định trigger vẫn dựa trên ngưỡng ban đầu; nếu "nội dung đã được sửa đổi hoàn toàn, nhưng EW sẽ không bị thay đổi trong thời điểm hiện tại", đây là một tùy chọn hành vi bổ sung, yêu cầu định nghĩa về lưu giữ tiêu chuẩn, kích hoạt lại và lưu trữ và sẽ không được trộn lẫn một cách lặng lẽ vào trang xác nhận.
- Bản xem trước chỉ hiển thị các bản đồ đã được xác minh; các vật phẩm không xác định được đánh dấu rõ ràng, không có kế thừa đầy đủ theo mặc định, không hoàn lại tiền tự động và không sao chép vũ khí hoặc bộ phận bị thiếu.

## 5. Hành vi và các manh mối khác không được phân loại trực tiếp là lỗi

| ID | Hành vi/Lãnh đạo | Quyết định đăng ký |
| --- | --- | --- |
| XEM01 | Gaia → Godmars, sự xuất hiện trở lại của Wing Zero của Hiro ở OZ và các hồ sơ biến đổi và bị mất khác | Akurasu liệt kê các nút tuyến đường và một số chỉ ra các tuyến đường khác cần được kiểm tra. [S8] Là hạt giống trả về tuyến đường của FIX04; sẽ không có lỗi nào được phát hiện trước khi khởi tạo và lấy cơ sở cốt truyện. |
| XEM02 | Quyền làm mẹ sớm hoặc vũ khí biến mất sau khi thay thế không được kế thừa | Dữ liệu đã liệt kê các mục không được kế thừa. [S8][S9] Đưa ra lời khuyên trước; thừa kế/hoàn trả thống nhất là các quy tắc tùy chọn; việc sửa đổi và hoàn trả máy bay đã xóa cốt truyện đã được triển khai dưới dạng điều chỉnh độ khó `upgrade-refund`, xem [Sửa đổi quy tắc tùy chọn](rule-fixes.md) §2.6. |
| XEM03 | Giới hạn trên của số tiền nhận được trong một trận chiến là 65.535 | Nhật ký người chơi gọi đó là lỗi và SRW Wiki ghi nhận nó là giới hạn trên. [S12][S13] Trước tiên hãy phân biệt giữa kẹp, tràn và cắt bớt hiển thị mà không trực tiếp xác định rằng giới hạn trên phải được tăng lên. |
| XEM04 | Tuyên bố chung rằng "các biện pháp phòng thủ đặc biệt như chém, phòng thủ bằng khiên và nhân bản đều có lỗi" | Lần này, không có báo cáo vấn đề độc lập SRW64 cụ thể đầy đủ; có lỗi khi không mở rộng "nhiều kỹ năng Phi công bị lỗi" để bao gồm tất cả các kỹ năng. Tách biệt khỏi khác biệt Aura Barrier của BUG02. |
| XEM05 | Vũ khí loại 0 sửa đổi có sức mạnh lớn hơn 0 có thể được "sửa đổi miễn phí" | Phân tích tĩnh của dự án này (2026-09-18), không có báo cáo bên ngoài. Danh sách sửa đổi chỉ loại trừ các kỹ năng kết hợp và vũ khí chưa được mở khóa và chỉ những vũ khí có sức mạnh bằng 0 mới bị từ chối trước khi xác nhận; loại 0 có giá là 0 và công suất xem trước là 0. Sau khi xác nhận, số giai đoạn +1 và công suất tạm thời thay đổi thành 0 cho đến lần tính toán lại tiếp theo. Chúng tôi chỉ có các vũ khí như Cấu trúc H, Liên minh Cấu trúc S và đai Bion, không thể đạt được ở dạng cơ bản trong quá trình chuẩn bị. Xem Phần 6.1 của [Phần sửa đổi](upgrade-limits.md); trước tiên hãy sử dụng máy thực tế để xác nhận xem có thể tiếp cận được máy không và không trực tiếp chẩn đoán lỗi. |
| QOL02 | Cơ thể giả của ông chủ được giấu kín và quá trình tiêu thụ rườm rà | Cơ chế cơ thể giả thông thường khác với BUG05. Hiển thị thời gian còn lại là nâng cao thông tin và giảm số lượng là thay đổi quy tắc. |
| QOL03 | Những màn trình diễn chiến đấu không thể bỏ qua | Tương ứng với khoảng cách chức năng B01 và không được liệt kê là lỗi chương trình gốc; ưu tiên vẫn là cốt lõi đầu tiên. |

Các lỗi kỹ năng liên tác, các đơn vị bất thường do mã gian lận gây ra, trục trặc về đồ họa/âm thanh dành riêng cho trình mô phỏng và các liên hệ Transfer Pak kém sẽ không được hợp nhất vào danh sách lỗi ban đầu trong vòng này.

## 6. Trình tự khảo sát và bàn giao

1. Hoạt ảnh chiến đấu B01 sẽ bị bỏ qua và tiếp tục là lõi khởi đầu; cuộc khảo sát này không tuyên bố rằng sự tương đương ngẫu nhiên đã được thông qua.
2. Việc điều tra lỗi ưu tiên sự tái diễn ranh giới của BUG09 và kiểm tra tính nhất quán trạng thái của BUG06; BUG05 đã được hoàn thành (2026-09-18) và phần còn lại là so sánh và trả lại các kho lưu trữ trên lộ trình ban đầu.
3. ~~BUG01–04 Thiết lập bảng so sánh kỹ năng/cách giải quyết và quyết định các quy tắc sửa lỗi tùy chọn sau khi giải quyết xung đột về số~~: Đã hoàn thành (17-09-2026), xem [Sửa đổi quy tắc tùy chọn](rule-fixes.md).
4. BUG07/08 và LEAD01 thiết lập các bản ghi chênh lệch cấp trường để chuyển đổi thiết bị, rời khỏi nhóm và sau đó tham gia; QOL01 sử dụng ánh xạ đã được xác minh.

Mỗi lần nâng cấp lên "được sao chép" yêu cầu ít nhất: đường cơ sở và tóm tắt đầu vào, các bước rõ ràng, quan sát ban đầu và quan sát trên máy chủ, cơ sở dự kiến và các ví dụ mẫu chưa được kích hoạt. Việc nâng cấp lên "Đã sửa" cũng yêu cầu bằng chứng về nguyên nhân, các bản sửa lỗi cục bộ, hồi quy và khả năng tương thích cũ. Lượng dữ liệu bên ngoài không thể thay thế cho các ngưỡng này.

## 7. Mục lục nguồn

Tất cả các nguồn đều là manh mối; không tìm thấy lỗi chính thức hoặc gói thử nghiệm hoàn chỉnh nào có nhận dạng phiên bản có thể được sử dụng để chấp nhận trực tiếp dự án này. Toàn văn hướng dẫn hoặc toàn bộ bảng giá trị sẽ không được sao chép bên dưới.

- **S1 — [Akurasu:64/Bugs](https://akurasu.net/wiki/Super_Robot_Wars/64/Bugs)**. Tóm tắt cộng đồng, trang hiển thị oldid=62318; giá trị siêu năng lực và sức mạnh cơ bản mâu thuẫn với dữ liệu của Nhật Bản.
- **S2 — [Điều hướng S-RPG:パイロットKỹ năng đặc biệt](https://s-rpg-navi.com/srw64/sp-skill/)**. Bảng hiệu ứng kỹ năng cho chiến lược cá nhân; không có đầu vào thử nghiệm có thể chơi lại nào được cung cấp cho dự án này.
- **S3 — [SRW Wiki: Siêu năng lực](https://srw.wiki.cre.jp/wiki/超能力)**. Chỉ sử dụng phần "64" và không thể áp dụng cho các bảng làm việc khác trên cùng một trang.
- **S4 — [SRW Wiki: Những chiến binh thần thánh](https://srw.wiki.cre.jp/wiki/聖戦士)**. Chỉ sử dụng phần 64; tài liệu về những thay đổi rào cản theo cấp độ.
- **S5 — [SRW Wiki：バグ（ゲーム）](https://srw.wiki.cre.jp/wiki/バグ_%28ゲーム%29)**. Chỉ sử dụng phần "64"; năm cảnh bay, vấn đề tham gia, menu tiện ích vượt quá giới hạn. "Năm phát hiện" trên trang này không đề cập đến báo cáo đầu tiên và không nhằm mục đích là một ngày chính xác.
- **S6 — [Điều hướng S-RPG：バグ](https://s-rpg-navi.com/srw64/bug/)**. Mô tả chiến lược chi tiết cho Wan Zhang, Wu Fei và Limit.
- **S7 — [SRW Wiki：ガンダムシュピーゲル](https://srw.wiki.cre.jp/wiki/ガンダムシュピーゲル)**. Chỉ sử dụng tiểu mục "64"; xem thêm bản ghi tham gia lại tại [Game Directory Wiki](https://w.atwiki.jp/gcmatome/pages/3679.html), cả hai đều chưa được chứng minh là có tính pháp lý độc lập.
- **S8 — [Akurasu: Nâng cấp quyền thừa kế](https://akurasu.net/wiki/Super_Robot_Wars/64/Upgrades_inheritance)**. Trang này hiển thị oldid=62286; có bảng lộ trình thay đổi và Rezner nghi ngờ, bao gồm cả hướng dẫn đặt chỗ cho các tuyến khác chưa được kiểm tra.
- **S9 — [5ch: Toàn diện 12](https://mevius.5ch.io/test/read.cgi/gamerobo/1432899611)**. 2015-08-14 Người chơi lân cận thảo luận về vũ khí không được thừa kế; điều này chỉ có thể chứng minh báo cáo của người chơi chứ không phải mục đích thiết kế.
- **S10 — [5ch: Toàn diện 14](https://mevius.5ch.io/test/read.cgi/gamerobo/1615283967)**. 25-06-2022～26 Báo cáo trực tiếp từ Tòa nhà 573/574/576, bao gồm liên kết hình ảnh và mô tả hoạt động; việc đọc bị giới hạn ở văn bản hiển thị trong chỉ mục tìm kiếm, việc thu thập thông tin URL trong phạm vi tầng phụ không thành công và các ảnh đính kèm không được tải xuống hoặc xác định.
- **S11 — [Điều hướng S-RPG: Chuyển đổi các mối quan hệ](https://s-rpg-navi.com/srw64/modification/)**. Tùy chỉnh dòng W và lập bản đồ vũ khí; bảng này chỉ trích xuất các hiện tượng liên quan đến việc xác minh và không được coi là bảng chuyển đổi hoàn chỉnh hoặc đã được xác minh.
- **S12 — [たくよ：スパロボ64をクリア](https://takuyo.blog.jp/archives/33876877.html)**. Nhật ký giải phóng mặt bằng của người chơi có phân loại lỗi về giới hạn tiền trên; không có bằng chứng công thức được đính kèm.
- **S13 — [SRW Wiki：スーパーロボット大戦64](https://srw.wiki.cre.jp/wiki/スーパーロボット大戦64)**. Ghi chú của cộng đồng về giới hạn tài trợ và cơ chế vanilla.
- **Video manh mối — [ぎんぱちゅ：スパロボ64のバグ 5 lựa chọn](https://www.youtube.com/watch?v=mCOgwvxBmHQ)**. 30-08-2022; Phần mô tả nói rằng máy Nintendo 64 thực tế đã được sử dụng và các chương là 00:28 Giới hạn, 02:16 Kỹ năng, 04:56 Titan 3, 06:27 Nội dung sai lầm, 07:31 Một lỗi khác. Vòng này chỉ đọc mô tả tác giả và các chương trong mục lục. Trang phát lại không được ghi lại. Nó không khẳng định đã xem màn hình thực tế hoặc xác nhận các bước để tái hiện phần cuối cùng.

Trả về: [Lộ trình MOD tích hợp](../design/mod-roadmap.md) · [Chỉ mục tài liệu kỹ thuật](../README.md)

[S1]: https://akurasu.net/wiki/Super_Robot_Wars/64/Bugs
[S2]: https://s-rpg-navi.com/srw64/sp-skill/
[S3]: https://srw.wiki.cre.jp/wiki/Superpowers
[S4]: https://srw.wiki.cre.jp/wiki/圣戦士
[S5]: https://srw.wiki.cre.jp/wiki/バグ_%28ゲーム%29
[S6]: https://s-rpg-navi.com/srw64/bug/
[S7]: https://srw.wiki.cre.jp/wiki/ガンダムシュピーゲル
[S8]: https://akurasu.net/wiki/Super_Robot_Wars/64/Upgrades_inheritance
[S9]: https://mevius.5ch.io/test/read.cgi/gamerobo/1432899611
[S10]: https://mevius.5ch.io/test/read.cgi/gamerobo/1615283967
[S11]: https://s-rpg-navi.com/srw64/modification/
[S12]: https://takuyo.blog.jp/archives/33876877.html
[S13]: https://srw.wiki.cre.jp/wiki/スーパーロボット大戦64