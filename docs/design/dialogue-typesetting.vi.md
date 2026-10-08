> **Ngôn ngữ / Language:** [Tiếng Việt](dialogue-typesetting.vi.md) · [English](dialogue-typesetting.en.md) · [中文](dialogue-typesetting.md)

# Sắp chữ đối thoại: hiển thị nhiều từ hơn và lật ít trang hơn

Ngày: 23-09-2026. Mục tiêu mà người dùng đặt ra là hiển thị càng nhiều từ trong hộp thoại càng tốt và giảm số lần nhấn A để lật trang. Bài viết này ghi lại các quy tắc sắp chữ và phông chữ được đặt cho điều này, dữ liệu dựa trên nó và những vị trí ban đầu cần được thay đổi.

Để biết cách triển khai sắp chữ hiện tại, hãy xem [đối thoại trò chơi và văn bản đa nền tảng tiếng Trung-Nhật-Anh](../native/portable-text.md), để biết định dạng tệp dòng, hãy xem [Tệp văn bản dòng](../guide/dialogue-text.md) và để biết các nguồn dịch, hãy xem [Lập kế hoạch bản địa hóa toàn văn bản](translation-plan.md).

## Kết luận

| Số trang lật (tất cả 33.512 dòng hội thoại) | Tiếng Trung | Tiếng Anh |
|---|---:|---:|
| Bản gốc tiếng Nhật | 46.870 | 46.870 |
| Bây giờ (phiên bản gốc bắt đầu trên một trang mới mỗi khi bạn lật trang, phông chữ 13 point, 2 dòng mỗi trang) | 49.738 | 62.071 |
| Kế hoạch đã được quyết định (xem bên dưới) | **37.750** | **38,958** |
| Giới hạn tối thiểu (ít nhất một trang trên mỗi dòng hội thoại) | 33.512 | 33.512 |

Kế hoạch đã quyết định: phông chữ HarmonyOS; giữ nguyên tên trong ô nhưng siết chặt dòng tên, vùng văn bản cao khoảng 43 inch; Cỡ 13 của tiếng Trung và cỡ 11 của tiếng Anh đều có 3 dòng trên một trang; một câu thoại được sắp xếp thành một hàng; sử dụng quy hoạch động để chọn vị trí lật trang.

- Lượt trang ít hơn 24% đối với tiếng Trung và ít hơn 37% đối với tiếng Anh, cả hai ngôn ngữ đều có ít trang hơn bản gốc tiếng Nhật.
- Cắt trang ở giữa câu: giảm từ 3.856 xuống 199 trong tiếng Trung và từ 4.692 xuống 409 trong tiếng Anh. Số trang không thay đổi, chỉ thay đổi vị trí lật trang.

Nguồn số:
- Sử dụng phông chữ đã chọn để tính độ rộng ký tự và mô phỏng việc sắp chữ theo quy tắc sau. Đây là một ước tính.
- Độ rộng ký tự không bao gồm kerning và ngôn ngữ tiếng Anh thực sự sẽ hẹp hơn một chút.
- Tên nhân vật chính được tính bằng ba ký tự (năm chữ cái trong tiếng Anh).

## Bộ quy tắc

### 1. Font: đóng gói thống nhất HarmonyOS Sans

| Ngôn ngữ | Phông chữ | Tập tin |
|---|---|---|
| Tiếng Trung | HarmonyOS Sans SC, Thông thường (400) | `HarmonyOS_Sans_SC.ttf`, 20,6 MB |
| Tiếng Anh | HarmonyOS Sans Condensed, Regular (400), những từ còn thiếu sẽ được SC | `HarmonyOS_Sans_Condensed.ttf`, 0,3 MB |
| Tiếng Nhật | Tạm thời sử dụng HarmonyOS Sans SC | Tương tự như tiếng Trung |

HarmonyOS Sans 2.040 (`9029cb9`) sẽ được đóng gói bắt đầu từ ngày 24-09-2026. Cả hai tệp đều có phông chữ có thể thay đổi (nặng 40–900), với phiên bản Thông thường mặc định được sử dụng cho nội dung văn bản; menu tiêu đề và thẻ tiêu đề chương sử dụng phiên bản In đậm của cùng một tệp. Sau khi thay đổi phiên bản, ngắt dòng, ranh giới trang và khoảng cách dòng của 30 trường hợp sử dụng phân trang không thay đổi. Chỉ có các chi tiết phông chữ đã thay đổi: "——" được kết nối thành một glyph, chữ ghép chữ Th tiếng Anh và chênh lệch độ rộng dấu ngoặc kép xoăn của tiếng Trung là 0,03 em.

- **Không còn dựa vào phông chữ hệ thống. ** Hiện tại, macOS, Linux và Windows đều sử dụng các phông chữ hệ thống khác nhau với độ rộng phông chữ khác nhau. Cùng một câu được phân trang khác nhau trên ba nền tảng. Sau khi đóng gói, ba nền tảng đều nhất quán và những gì người hiệu đính nhìn thấy cũng chính là những gì người chơi nhìn thấy.
- **Tình trạng bảo hiểm. ** SC bao gồm 3.614 ký tự được sử dụng trong tiếng Trung và 1.981 ký tự được sử dụng trong tiếng Nhật (bao gồm tất cả kana).
- Bốn ký tự đặc biệt ► ▷ ◀ 🔧 đều bị thiếu trong cả ba ngôn ngữ. Người dùng quyết định tạo một phông chữ ký hiệu riêng biệt `content/fonts/SRW64Symbols.ttf` (gửi cùng kho) và đặt nó ở cấp độ cuối cùng của mỗi chuỗi phông chữ ngôn ngữ.
- Được tạo bởi `tools/content/build_symbol_font.py`, cùng một dữ liệu đầu vào sẽ nhận được các byte giống nhau.
- ▶▷◀ Lấy từ DejaVu Sans bản địa: giấy phép của nó cho phép sửa đổi và phân phối lại. Các glyph được chia tỷ lệ theo kích thước và chiều rộng Arial Unicode hiện tại (0,6 em) và bố cục giao diện hiện tại không thay đổi.
- 🔧 Nhấn biểu tượng sửa chữa trong ROM để tự vẽ: cờ lê kết hợp đường chéo, lỗ mở ở phía trên bên phải và vòng cổ ở phía dưới bên trái. Chỉ các biểu tượng cảm xúc màu của Apple mới có ký tự này nguyên bản và không thể phân phối được nữa.
- Sau đó, thêm 5 dấu vũ khí (`218f327`) được thêm vào và đặt trong khu vực riêng tư U+E000 cộng với số glyph ban đầu: U+E0F4 chiến đấu (nắm đấm), U+E0F3 bắn (tầm nhìn), U+E0F1 vòng tròn P, U+E0F2 vòng tròn B, huy hiệu U+E23F MAP.
- Đồ họa được vẽ tay theo ROM gốc, các chữ cái P, B, MAP được lấy từ DejaVu Sans Bold nên cần thêm `--dejavu-bold` cho bản dựng.
- Bảng vũ khí ở chế độ đồ họa HD sử dụng trực tiếp các ký tự này; chế độ đồ họa vanilla vẫn sử dụng các biểu tượng pixel được cắt từ ROM.
- Phông chữ hiện có tổng cộng 9 glyph, 3 KB.
- Bản quyền các phông chữ hệ thống (Arial Unicode, biểu tượng cảm xúc Apple, v.v.) thuộc về Monotype hoặc Apple và không được phép chọn lọc và phân phối lại nên vô dụng.
- Phép đo theo chiều dọc giống như SC, là phép đo dự phòng, nó không làm tăng chiều cao của hàng.
- Hướng dẫn cấp phép trong `content/fonts/LICENSE-SRW64Symbols.txt`, kiểm tra trong `tests/test_symbol_font.py`.
- 28-09-2026 Phông chữ biểu tượng được theo sau bởi phông chữ biểu tượng nút `content/fonts/SRW64Prompts.ttf`: Lấy 57 nút điều khiển và biểu tượng nút bàn phím từ NhắcFont (SIL OFL) và di chuyển chúng đến khu vực riêng tư bắt đầu từ U+E800. Thay thế các ký hiệu như `{A}` và `{Esc}` trong mục nhắc nhở bằng các ký tự này (xem [Vị trí phím và biểu tượng phím của Steam Deck](steam-deck-controls.md#按键图标)). Văn bản của các dòng không sử dụng vùng riêng tư và việc sắp chữ và phân trang không bị ảnh hưởng.
- Một số từ "bắn" và "mạng" chưa dịch trong dòng tiếng Anh đã được SC điền vào.
- **Viết tiếng Nhật. ** SC vẽ chữ Hán theo cách viết chữ Hán giản thể như "Zhi, Gu, Jin, Ling, Ci, Gu" khác với cách viết tiếng Nhật. Arial Unicode hiện được sử dụng ở chế độ tiếng Nhật không phải là phương pháp viết tiếng Nhật tiêu chuẩn, do đó hiện tại không có phông chữ tiếng Nhật riêng; phông chữ tiếng Nhật sẽ được thêm vào tiếng Nhật khi cần thiết trong tương lai.
- ** Khoảng cách Kern. ** Cả 3 font đều có dữ liệu kerning, HarfBuzz sẽ mặc định sử dụng, không cần đổi mã.
- **SC không có chức năng ngắt nửa độ rộng (dừng). ** Dấu chấm câu nửa độ rộng ở cuối dòng (xem Điều 7) chỉ có thể được tính bởi người dùng bản địa.
- **Giấy phép: Giấy phép phông chữ HarmonyOS Sans, không phải giấy phép nguồn mở. **
- Nó có thể được đóng gói, phân phối và sử dụng thương mại cùng với trò chơi miễn phí;
- Việc sử dụng HarmonyOS Sans phải được nêu rõ trong trò chơi;
- Không được phép sửa đổi nên không thể cắt bỏ những ký tự không sử dụng. Phông chữ tiếng Trung đi kèm với các tập tin hoàn chỉnh;
- Phông chữ có thể không được phân phối riêng lẻ;
- Phải lưu giữ toàn bộ nội dung tuyên bố về bản quyền và thỏa thuận cấp phép;
- Thỏa thuận có thể bị hủy bỏ.
- **Nguồn:** Gói gốc của trang web chính thức của Huawei (https://developer.huawei.com/consumer/cn/design/resource/). Bản sao cục bộ nằm ở `assets/fonts/HarmonyOS-Sans-2.040.zip` và hàm băm của tệp nằm ở `content/fonts/harmonyos-sans.json`. Không sử dụng hình ảnh của bên thứ ba.
- **Phương pháp đóng gói (thỏa thuận với phiên gốc):**
- Tệp phông chữ không được bao gồm trong git: kho lưu trữ là công khai và thỏa thuận cấm phân phối riêng biệt. Chỉ siêu dữ liệu (địa chỉ tải xuống và hàm băm tệp), chẳng hạn như `content/fonts/harmonyos-sans.json` mới được đặt trong kho.
- Khi xây dựng hoặc chuẩn bị lần đầu tiên hãy kiểm tra SHA-256 của gói chính thức rồi giải mã font chữ; khi không có gói chính thức trong tài sản, một lời nhắc rõ ràng và địa chỉ tải xuống chính thức sẽ được cung cấp và phông chữ hệ thống sẽ không được âm thầm trả lại.
- Phát triển chạy đọc từ tài sản.
- Gói phân phối đi kèm với phông chữ, toàn bộ văn bản thỏa thuận cấp phép và tuyên bố nổi bật (`HarmonyOS Sans/LICENSE-update.txt` trong gói, được đóng gói dưới dạng `LICENSE-HarmonyOS-Sans.txt`, giống như phiên bản cũ của văn bản thỏa thuận): viết "Phông chữ: HarmonyOS Sans" ở cuối trang cài đặt và cũng viết một câu trong README hoặc lời cảm ơn.
- Các thỏa thuận có thể bị thu hồi, do đó việc lựa chọn phông chữ vẫn có thể cấu hình được.

Biểu đồ so sánh và tập lệnh đo lường sau đó được đặt trong thư mục tạm thời của phiên. Các ứng cử viên được so sánh là: Source Sans 3, Fira Sans Condensed, IBM Plex Sans (condensed), Noto Sans (condensed SemiCondensed), Atkinson Hyperlegible. Khi số trang bằng tiếng Trung, HarmonyOS Sans Condensed có chữ cái viết thường lớn nhất (x-high 5,7 pixel, Arial Unicode là 5,1).

### 2. Ký hiệu tiếng Anh gấp 0,85 lần giá trị cài đặt

I/K vẫn chỉ chỉnh một cỡ chữ, số hiển thị ở cột dưới cùng không thay đổi; văn bản tiếng Anh được sắp xếp gấp 0,85 lần con số này (khi đặt cỡ 13 thì cỡ tiếng Anh là 11). Khi F7 chuyển ngôn ngữ thì số trang 2 bên và nhịp đọc tương đương nhau. Công cụ sắp chữ ban đầu chấp nhận số thập phân; kích thước phông chữ trong `typeset()` và Reader hiện là số nguyên và cần được đổi thành số thập phân.

### 3. Một dòng hội thoại được sắp xếp thành một hàng và bước ngoặt trang gốc chỉ dùng để đồng bộ hóa.

- **Hiển thị:** Tất cả các đoạn của bản ghi (đoạn gốc được hiển thị mỗi lần bằng cách nhấn A) được kết nối thành một đoạn văn bản và các trang được đánh trang lại theo cỡ chữ và cỡ khung hiện tại. Tiếng Trung được kết nối trực tiếp; Tiếng Anh được kết nối với không gian.
- **Đồng bộ hóa:** Kịch bản gốc vẫn cần xác nhận từng bước ngoặt của từng trang (`<STOP>`). Khi trang được lật bởi phiên bản gốc đã có phần đầu của đoạn tiếp theo, điểm chuyển trang trước đó sẽ được xác nhận cho phiên bản gốc ở chế độ nền; nếu phiên bản gốc không phản hồi trong vòng 0,5 giây, nó sẽ được gửi lại. Văn bản gốc ban đầu được bao phủ bởi bản gốc và người chơi không thể nhìn thấy quá trình này. Sau khi nhấn A ở trang cuối cùng, trước tiên hãy xác nhận các bước ngoặt của trang còn lại, sau đó xác nhận `<END>` để vào đoạn hội thoại tiếp theo. Phiên bản gốc xác nhận rằng nó sẽ chỉ tiến lên chứ không lùi lại. Trong bản ghi sự kiện, mỗi xác nhận nền được ghi là `guest_stop` và xác nhận END được ghi là `guest_confirm`.
- **Số lượng đoạn dựa trên ROM tiếng Nhật (được đảm bảo):** Nếu `---` của văn bản dịch nhỏ hơn văn bản gốc, phần xác nhận còn thiếu sẽ được đặt ở trang cuối cùng và được điền lại; nếu nhiều hơn văn bản gốc thì những đoạn thừa sẽ chỉ được coi như những đoạn câu thông thường, không bị mắc kẹt hay đánh giá sai. Việc kiểm tra file dòng vẫn yêu cầu số phải nhất quán.
- **Tệp dòng không thay đổi:** Số `---` vẫn phải nhất quán với văn bản gốc. Nó là cơ sở để căn chỉnh văn bản gốc và văn bản gốc chứ không còn quyết định cách phân trang trên màn hình nữa. Hiện có hơn 45.000 bản dịch không cần chỉnh sửa. Sau khi triển khai gốc, mô tả của `---` trong [Tệp văn bản dòng](../guide/dialogue-text.md) đã được thay đổi thành "Bước ngoặt của trang gốc; trang lại trong trò chơi theo kích thước của khung."
- **Giữ nguyên tạm dừng:** Hiển thị nguyên văn sẽ dừng trong 18 khung hình (0,3 giây) khi đến điểm chuyển trang ban đầu và thời gian tạm dừng ban đầu được tạo bằng cách lật trang sẽ được giữ lại.
- **Không gộp các bản ghi:** Giữa hai dòng hội thoại là các câu lệnh script. Tập lệnh có thể thay đổi hình đại diện, di chuyển đơn vị hoặc phát hiệu ứng âm thanh.
- **Hiện tại không có dấu chuyển trang bắt buộc:** Mục tiêu là giảm chuyển trang. Khi thực sự cần ngắt dòng, hãy sử dụng ngắt dòng trong tệp dòng.
- **Không nằm trong phạm vi:** Các dòng chiến đấu (chỉ được thay thế và hiển thị, tiến độ được tính theo phiên bản gốc) không nằm trong cột này và vẫn được xử lý theo cỡ chữ giảm hiện tại.

### 4. Giữ nguyên tên trong ô, siết chặt dòng tên và thay đổi vùng văn bản từ cao 35 thành cao khoảng 43

Dòng tên bây giờ chiếm khoảng một phần ba chiều cao của hộp. Phiên gốc tạo ra ba loại kết xuất thương hiệu: nhãn được nhúng trong đường viền, khoảng trống ở đường viền và viên nang bên ngoài khung. Sau khi đọc xong, người dùng quyết định giữ nguyên tên trong ô và chọn bản “Thắt chặt dòng tên”:
- Sử dụng font chữ cỡ 10 cho tên của bạn và đặt ở góc trên bên trái của ô;
- Văn bản chính nằm ngay bên dưới tên và vùng văn bản chính cao khoảng 43 inch.

Điều này chỉ thay đổi màn hình và không chạm vào dữ liệu trò chơi.

Chiều cao của vùng văn bản được so sánh với 42, 43 và 44:
- **42:** Số 13 tiếng Trung chỉ được viết 2 dòng thôi, không được.
- **44:** Cỡ chữ mặc định giống hệt 43, chỉ có thêm một dòng cho một số cỡ chữ nhất định: Cài đặt tiếng Trung là 10 điểm và cài đặt tiếng Anh là 11 điểm. Khi cài đặt tiếng Anh là 15, 44 bị kẹt chính xác trên ranh giới của 3 dòng và kết quả không ổn định và không được tính là lợi nhuận.
- **Kết luận:** Lấy 43; nếu chỉ có thêm một pixel trong bố cục thì 44 pixel cũng sẽ hoạt động.

### 5. Số dòng trên trang tùy chỉnh theo cỡ chữ

- **Vấn đề hiện tại:** Khoảng cách dòng được cố định ở mức 1,22 lần cỡ chữ. Khi vùng văn bản cao 35, chỉ có thể đặt một dòng có kích thước 15–18.
- **Quy tắc mới:** Trước tiên hãy tính xem có thể đặt bao nhiêu dòng theo khoảng cách dòng tối thiểu (1,08 lần đối với tiếng Trung, 1,15 lần đối với tiếng Anh), sau đó chia đều chiều cao còn lại cho các dòng, với khoảng cách dòng tối đa là 1,22 lần.
- **Vùng văn bản dài khoảng 43 giây** (mỗi dòng hội thoại xếp thành một hàng, số trang là số lượt lật trang của tất cả các đoạn hội thoại cốt truyện; cỡ chữ tiếng Anh là 0,85 lần giá trị đặt):

| Cài đặt cỡ chữ | Số dòng tiếng Trung trên mỗi trang | Số trang tiếng Trung | Số dòng tiếng Anh trên mỗi trang | Số trang tiếng Anh |
|---:|---:|---:|---:|---:|
| 10 | 3 | 35.437 | 4 | 34.476 |
| 11 | 3 | 36.115 | 3 | 36.887 |
| 12 | 3 | 36.975 | 3 | 37.880 |
| **13 (mặc định)** | **3** | **37.750** | **3** | **38,958** |
| 14 | 2 | 46.369 | 3 | 40.079 |
| 15 | 2 | 48.725 | 2 | 50.224 |
| 16 | 2 | 50.738 | 2 | 52.424 |
| 17 | 2 | 54.045 | 2 | 54.744 |
| 18 | 2 | 55.245 | 2 | 57.000 |

Ở kích thước mặc định là 13, khoảng cách dòng tiếng Trung khoảng 1,10 lần. Để viết được 4 dòng tiếng Anh thì vùng văn bản cần cao khoảng 51, 43 không vừa.

### 6. Sử dụng lập trình động cho vị trí lật trang

- **Vị trí ứng cử viên:** Vị trí ngắt dòng pháp lý do ICU đưa ra.
- **Thứ tự so sánh:**
1. Giảm thiểu số lượng trang và kết quả giống như "điền càng nhiều trang càng tốt vào một dòng";
2. Cắt ở giữa câu với số lần ít nhất (dấu chấm, dấu chấm hỏi, dấu chấm than, dấu chấm lửng, dấu ngoặc kép đóng đều được tính là cuối câu; chuyển trang gốc chỉ được tính là cuối câu trong tiếng Nhật);
3. Cắt ở dấu phẩy và ngắt quãng càng ít lần càng tốt;
4. Còn lại ít nhất một hoặc hai từ hoặc một từ tiếng Anh ở dòng cuối cùng (dấu chấm câu và dấu ngoặc kép không được tính là từ, “Up!” được tính là một từ);
5. Khi tất cả các mục trên đều giống nhau thì các trang trước đã đầy (lấy điểm bắt đầu mới nhất).
- **2026-09-24 Ba điều chỉnh** dựa trên các dòng có thêm dấu câu ở cuối trang (gốc `a6a70ed`):
- Ở phiên bản gốc, bước ngoặt trang trước đây được tính là kết thúc câu trong tất cả các ngôn ngữ, nhưng hiện tại nó chỉ được tính ở tiếng Nhật. Sau khi chấm câu xong ở cuối trang tiếng Trung, những chỗ lật trang gốc chưa được chấm câu sẽ được lấp đầy bằng một câu tiếp tục xuyên suốt trang (chẳng hạn như “Hãy đến | đi cùng em” và “Sư phụ sẽ | khóc”). Các quy tắc ban đầu sẽ chọn cụ thể những nơi này để lật trang. Khoảng dừng 0,3 giây không thay đổi.
- Đồng thời, các trang trước đều đầy: ví dụ trang đầu tiên của 17358 vốn chỉ có “Bạn là kẻ ngốc”, nhưng bây giờ lại là “Bạn là kẻ ngốc. Du kích bất lực khi thua trong trận chiến”.
- Khi đếm số từ ở dòng cuối cùng sẽ không tính dấu chấm câu và dấu ngoặc kép: nếu không thì "Up!" sẽ được tính là 3 từ và 17364 sẽ để yên ở trang cuối cùng sau khi trang trước được điền.
- Trích xuất 1.500 bản ghi nhiều trang, số lượng trang hoàn toàn không thay đổi:
- Tiếng Trung: trang 116 → 31 cắt giữa câu, trang đầu chỉ có một dòng 156 → 55;
- Tiếng Anh: trang cắt giữa câu 229 → 80, trang đầu chỉ có một dòng 164 → 77;
- Giá: 118 → 147 chỉ còn một chữ ở dòng cuối cùng tiếng Anh.
- **Số lượng tính toán:** Chỉ có hàng chục vị trí ứng cử viên cho mỗi bản ghi, có thể bỏ qua.
- **Đừng làm điều đó:** Tiếp tục sử dụng phương pháp hiện tại trong dòng (nên điền càng nhiều dòng càng tốt, đó là số dòng tối thiểu); không có sự biện minh và dấu gạch nối.
- **Phân loại ký tự (chung với C++ và Python):**
- Cuối câu: `。！？…!?.` và dấu ngoặc kép đóng, dấu ngoặc phải `」』）”"`, cộng với dấu chuyển trang gốc;
- Cấp độ dấu phẩy: `，、；：—,;:`;
- Có thể nhấn cuối dòng đến nửa độ rộng (khoản 7): `。，、；：」』）》】〕`;
- Dấu ngoặc kép mở (bỏ qua cùng với 2 nhóm trước khi đếm số từ ở dòng cuối cùng): `“「『（《【〔"`;
- Tránh đưa đầu và đuôi vào ICU theo quy định nghiêm ngặt.
- **Kiểm tra kiểm soát:** C++ và Python chia sẻ tệp ca sử dụng. Viết ra từng trường hợp sử dụng:
- Đầu vào: văn bản, ngôn ngữ, font chữ, cỡ chữ, chiều rộng, chiều cao, vị trí lật trang bắt buộc;
- Đại lượng trung gian được đo bằng C++: vị trí cuối và chiều rộng của mỗi đồ thị và vị trí ngắt dòng hợp lệ do ICU đưa ra;
- Kỳ vọng: khoảng cách dòng, số dòng trên trang, ranh giới dòng, ranh giới trang, vị trí dấu câu nửa độ rộng.
  
Python sử dụng các đại lượng trung gian này để chạy cùng một bộ quy tắc và ranh giới trang phải hoàn toàn giống nhau; sự khác biệt về độ rộng từ do phông chữ gây ra không được đưa vào so sánh thuật toán.

### 7. Nhấn dấu chấm câu ở cuối dòng tiếng Trung đến nửa độ rộng

- **Tình hình hiện tại:** "Nhân vật +." Khi không khớp được, quy tắc tránh đầu đuôi sẽ đẩy ký tự này lại với nhau sang dòng tiếp theo.
- **Quy tắc mới:** Đặt dấu ".,,;:"　)》]" ở cuối dòng chỉ rộng bằng nửa từ (phù hợp với danh sách ký tự ở Mục 6).
- **Lợi ích:** Có thể nén ít từ hơn vào phông chữ hiện tại dài khoảng 5.360 dòng.
- **Thực hiện:** SC không có chức năng ngắt dòng nên độ rộng của dấu chấm câu ở cuối dòng sẽ giảm đi một nửa khi ngắt dòng. Điều này chỉ được thực hiện khi có thể thêm một từ bổ sung.

### 8. Thay đổi cỡ chữ và chuyển ngôn ngữ

- **Thay đổi cỡ chữ:** Đánh số trang lại toàn bộ bài viết và đặt phần đầu của trang hiện tại làm vị trí phải lật trang. Bằng cách này, trang hiện tại vẫn bắt đầu từ cùng một từ và chỉ các trang sau được sắp xếp lại. Xác nhận ban đầu sẽ chỉ được tiến hành và sẽ không bị ảnh hưởng.
- **Đánh giá:** Đã thay đổi để lưu toàn bộ bản ghi.
- **Chuyển ngôn ngữ:** Thay thế toàn bộ đoạn văn và tiếp tục đọc từ đầu đoạn hiện tại trong phiên bản gốc.

### Chưa làm ngay: hãy phóng to khung hình

- **Đã thêm vào chiều cao ~51 (+8 pixel):** Cài đặt kích thước tiếng Anh 13 có 4 dòng trên mỗi trang, số lượt xem trang giảm từ 38.958 xuống ~35.900 (−8%), tiếng Trung không thay đổi.
- **Thêm vào chiều cao khoảng 57:** Size 13 của Trung Quốc cũng có thể đựng được 4 dòng.
- **Chi phí:** Khung cần được mở rộng để bao phủ nhiều bản đồ hơn. Chuyển động của đơn vị và dấu con trỏ trong biểu đồ nằm ở giữa màn hình.
- **Khi nào cần xem lại:** Đợi cho đến khi sơ đồ dòng tên được nhìn thấy trên máy thật trước khi đánh giá nó; khi thực hiện màn ảnh rộng sau này, bạn cũng có thể mở rộng khung hình sang cả hai bên.

## Phân công lao động và nghiệm thu

Cuộc đối thoại gốc được viết trong một phiên khác (Tổ chức và phát triển dự án) và những thay đổi gốc đối với các mục 1–8 đã được triển khai trong đó:
- Lựa chọn phông chữ: `game_fonts.cpp`;
- Phân trang, giãn dòng, chấm câu: `portable_text.*`;
- Thương hiệu: `dialogue_scene.cpp`;
- Sắp xếp và đồng bộ toàn bộ chuỗi: `native_dialogue.cpp`, `dialogue_model.hpp`.

Phiên này có trách nhiệm:
- Triển khai tham chiếu Python: `src/srw64_native/dialogue_paging.py`, đã hoàn thành. Nó chịu trách nhiệm về bố cục liên tục, cỡ chữ và khoảng cách dòng cũng như vị trí lật trang; nó chia sẻ 30 trường hợp sử dụng `tests/data/dialogue-paging-cases.json` với trò chơi. `tests/test_dialogue_paging.py` kiểm tra xem ranh giới trang, ranh giới dòng và vị trí nhấn nửa chiều rộng có giống nhau không. Trong trường hợp sử dụng, chỉ độ rộng từ và vị trí ngắt dòng hợp lệ là từ quá trình sắp chữ của trò chơi; để thêm trường hợp sử dụng, hãy thêm một trường hợp sử dụng vào `tests/data/dialogue-paging-inputs.json`, sau đó sử dụng `srw64-paging-cases` (trong `tests/dialogue_cpu`, `SRW64_FONT_DIR=build/fonts` là bắt buộc) để tạo lại.
- Mô tả tệp dòng: Ý nghĩa của `---` trong [Tệp văn bản dòng](../guide/dialogue-text.md) đã được thay đổi.

**Trạng thái triển khai (23-09-2026):** Phần gốc đã được gửi:
- `3beb303`: phông chữ;
- `04cab4b`: phân trang;
- `f5e6bb6`: sắp xếp và đồng bộ hóa toàn bộ chuỗi;
- `4af09ec`: Trường hợp sử dụng chung.

Tên được đánh số 10 ở góc trên bên trái của hộp và vùng văn bản là 177×43 (từ 20 phía trên gốc văn bản đến 34 bên dưới trong hộp). Tất cả các thử nghiệm tĩnh đều đã vượt qua nhưng máy thực tế vẫn chưa được triển khai.

Chấp nhận:
- **Kiểm tra tĩnh**
- Số trang trong lập trình động bằng số trang có thể “lấp đầy một hàng nhiều nhất có thể”;
- Vị trí lật trang cưỡng bức không thay đổi;
- Khoảng cách dòng thích ứng;
- Số lượng xác nhận bản gốc sau các hàng liên tiếp bằng số bước ngoặt trang cộng một;
- Vị trí của người đọc không thay đổi sau khi thay đổi cỡ chữ và chuyển đổi ngôn ngữ.
- **Máy thật (phải có sự đồng ý của người dùng trước để tránh cạnh tranh hosting với các phiên khác)**
- Xem ba cảnh bằng tiếng Trung và tiếng Anh: F7 chuyển ngôn ngữ, I/K thay đổi cỡ chữ và có nhiều bước ngoặt trang gốc trong một đoạn hội thoại;
- Kiểm tra phiên bản gốc từ bản ghi sự kiện để xác nhận số lần không hơn không kém;
- Kiểm tra dòng tên và nội dung chính không bị trùng nhau hoặc bị cắt xén.