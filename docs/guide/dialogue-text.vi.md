> **Ngôn ngữ / Language:** [Tiếng Việt](dialogue-text.vi.md) · [English](dialogue-text.en.md) · [中文](dialogue-text.md)

# Tệp văn bản dòng: định dạng, vị trí lưu trữ và phương thức sửa đổi

Ngày: 23-09-2026. Lời thoại cốt truyện, các chi tùy chọn và lời thoại chiến đấu không được ghi vào thư mục ngôn ngữ `content/locales/<locale>.json`. Mỗi ngôn ngữ có một bộ tệp văn bản thuần túy riêng biệt mà người chơi có thể sửa đổi trực tiếp. Tên, nhãn giao diện và lời nhắc hệ thống vẫn có trong [danh sách thuật ngữ](../native/localization-terms.md).

## Đặt nó ở đâu

| Vị trí | Mục đích |
| --- | --- |
| `content/dialogue/<locale>/` (kho); `Contents/Resources/dialogue/<locale>/` trong gói ứng dụng | Bản dịch đi kèm với chương trình. Cốt truyện được chia thành các file theo cảnh; các chiến tuyến được chia thành các tệp theo ký tự (`battle/speaker-NNN.txt`). Nhận xét `# 触发：` phía trên mỗi dòng cho biết tình huống nào, loại vũ khí nào được sử dụng và đối thủ nào mà câu xuất hiện (xem [Bảng lựa chọn chiến tuyến](../data/battle-quotes.md)); toàn bộ bộ được thay thế khi cập nhật chương trình |
| `dialogue/<locale>/` trong thư mục người dùng (ứng dụng macOS: `~/Library/Application Support/SRW64Recomp/dialogue/<locale>/`; bản dùng thử phát triển `scripts/Play SRW64 Native.command`: `build/recomp/profile-play/dialogue/<locale>/`; phiên gỡ lỗi: `dialogue/` trong thư mục đang chạy tương ứng) | Những sửa đổi của riêng người chơi. **Nội dung theo từng mục** Đi kèm với bản dịch, tên file và cấu trúc thư mục là tùy ý; chương trình cập nhật sẽ không chạm vào nơi này |

`<locale>` là `zh-Hans`, `en` hoặc `ja` (thư mục `ja` được sử dụng để thay đổi cách hiển thị văn bản gốc tiếng Nhật, tùy chọn). Chương trình đọc tất cả `*.txt` của một ngôn ngữ nhất định: trước tiên đọc những ngôn ngữ đính kèm, sau đó đọc những ngôn ngữ trong thư mục người dùng; trên cùng một dòng, thư mục người dùng sẽ được ưu tiên áp dụng.

Nếu muốn thay đổi câu nào, chỉ cần sao chép câu trong file đính kèm (hoặc toàn bộ file cảnh) vào thư mục người dùng rồi thay đổi. Không cần phải sao chép các mục không thay đổi, nếu không, nếu bản dịch đi kèm được cập nhật trong tương lai, bản cũ của bạn vẫn sẽ che nó.

## Định dạng

Văn bản thuần túy UTF-8, bao nhiêu tùy thích trong một tệp. Ví dụ:

```text
# 第一话「出撃！スイームルグ」
@17412 ローレンス
> お嬢様、お茶のご用意ができました。本日はロシアンティーでございます。
小姐，茶已经准备好了。今天是俄罗斯红茶。
---
> どちらにお持ちしましょう？
要送到哪里呢？

@17413 {HeroNick}
> ……ローレンス、お茶のことはいいわ。
……劳伦斯，茶的事就算了。

@18020 选择肢
> * 協力する
> * 断る
* 合作
* 拒绝
```

| Viết | Ý nghĩa |
| --- | --- |
| `@17412 ローレンス` | Sự khởi đầu của một dòng. Số là số bản ghi của bảng văn bản 0; theo sau là phần nhận xét (thường được viết với tư cách là người nói), chương trình không đọc |
| `> …` | Văn bản gốc tiếng Nhật, chỉ để so sánh. Chương trình sẽ so sánh với văn bản gốc của ROM. Nếu chúng không nhất quán, điều đó có nghĩa là số bản ghi được ghi không chính xác và điều này sẽ không có hiệu lực. Bạn có thể xóa nó mà không cần viết |
| Các dòng khác | Bản dịch. Một trang thường được viết dưới dạng một dòng và chương trình sẽ tự động gấp các dòng theo chiều rộng của hộp thoại. Việc ngắt dòng thủ công sẽ buộc một dòng mới trong trò chơi, chỉ sử dụng khi thực sự cần thiết |
| `---` | Bước ngoặt trang của phiên bản gốc (trang tiếp theo xuất hiện sau khi nhấn A một lần trong phiên bản gốc). Con số này phải giống với văn bản gốc và trò chơi dựa vào đó để phù hợp với tiến trình của văn bản gốc. Trong trò chơi, nếu một dòng hội thoại được kết nối toàn bộ, trang sẽ được đánh trang lại theo kích thước của hộp thoại và trang này không nhất thiết phải được lật ở đây; hiển thị từng từ sẽ dừng ở đây trong khoảng 0,3 giây và trang sẽ bị ngắt kết nối ở đây trước tiên trong quá trình phân trang |
| `* …` | Chọn một tùy chọn cho các chi, mỗi chi một dòng, số phải giống với văn bản gốc |
| `# …` | Bình luận |
| Dòng trống | vô nghĩa, bạn có thể thêm vào tùy thích |

Tên động được viết dưới dạng giữ chỗ và được thay thế bằng tên do người chơi trong trò chơi đặt:

| giữ chỗ | nội dung | giữ chỗ | nội dung |
| --- | --- | --- | --- |
| `{HeroNick}` | Biệt danh của nhân vật chính | `{PartnerNick}` | Biệt danh của đối tác |
| `{HeroName}` | Tên nhân vật chính | `{PartnerName}` | Tên đối tác |
| `{HeroSurname}` | Họ của nhân vật chính | `{PartnerSurname}` | Họ của đối tác |
| `{HeroFull}` | Tên đầy đủ của nhân vật chính | `{PartnerFull}` | Tên đầy đủ của đối tác |
| `{HeroMech}` | Tên đơn vị (tên giữ chỗ theo sau tên cũ, xem [Tên đơn vị cố định](../native/fixed-unit-name.md)) | `{G:0104}` | Các hình tượng đặc biệt khác (được giữ nguyên) |

Các phần giữ chỗ trên một trang phải có nhiều và cùng loại với các phần giữ chỗ được sử dụng trên trang gốc và thứ tự có thể được điều chỉnh theo thứ tự từ của bản dịch.

Để có một dòng dịch bắt đầu bằng `>`, `*`, `#`, `@`, `\` hoặc đối với toàn bộ dòng là `---`, hãy thêm `\` vào trước (ví dụ: `\*`). Nửa độ rộng `<` không thể xuất hiện trong bản dịch, vui lòng sử dụng `＜` toàn chiều rộng.

## Xác thực, tải lại và lỗi

- Đọc khi khởi động. Nhấn **F5** trong trò chơi (hoặc sử dụng menu "Tải lại dòng") để đọc lại tất cả các tệp dòng: dòng hiện tại sẽ được hiển thị từ đầu bằng văn bản mới và phần đánh giá cũng sẽ được thay thế bằng văn bản mới.
- Toàn bộ mục nhập có lỗi sẽ không có hiệu lực và chuyển sang cấp độ tiếp theo: thư mục người dùng → bản dịch đính kèm → văn bản gốc tiếng Nhật. Các mục khác sẽ vẫn như bình thường. Sau mỗi lần đọc, số mục nhập và lỗi sẽ được nhắc ở đầu cửa sổ và thông tin chi tiết sẽ được ghi vào `dialogue-report.txt` (tên tệp, số dòng, số bản ghi, lý do) trong thư mục người dùng.
- Các lỗi thường gặp: Số trang (`---`) không khớp với văn bản gốc; số lượng lựa chọn không nhất quán; phần giữ chỗ bị sai chính tả hoặc bị thiếu; dòng văn bản gốc (`>`) không khớp với số bản ghi; có một nửa chiều rộng `<` trong bản dịch.
- Cách sắp chữ trong game (cách gõ cả dòng, số dòng trên một trang, cỡ chữ tiếng Anh và vị trí lật trang), vui lòng xem [Soạn hội thoại](../design/dialogue-typesetting.md).
- Đường chiến đấu chỉ được thay thế và hiển thị, nhịp tiến quân ban đầu không thay đổi. Nếu nó không vừa trên một trang, kích thước phông chữ sẽ tự động bị giảm và sẽ không có ngắt trang, vì vậy hãy giữ nó càng ngắn càng tốt.

## File đính kèm: Gửi tác giả tool

- Triển khai đọc: `src/srw64_native/dialogue_text.py` (Python, để tạo và kiểm tra) và `src/native/localization/dialogue_text.hpp` (trong trò chơi). Quy tắc của cả hai đều nhất quán và bị ràng buộc chung bởi `tests/test_dialogue_text.py` và `tests/native_content.cpp`; kết quả mở rộng của hai tệp đính kèm cho cùng một lô đều nhất quán từng tệp một.
- Một dòng được mở rộng sang định dạng thư mục ngôn ngữ: `<BR>` giữa các dòng, `<STOP>` giữa các trang, phần giữ chỗ trở thành `<G:0124>`–`<G:012C>` và `<END>` ở cuối. Khi một tên chiếm nhiều khoảng trắng trong văn bản gốc (lặp lại cùng một mã ký tự), chỉ viết một phần giữ chỗ; trong trò chơi, nó được hiển thị bằng một tên.
- Phân trang: `src/srw64_native/dialogue_paging.py` là tham chiếu Python cho quy tắc phân trang của trò chơi (hàng liên tục, cỡ chữ và khoảng cách dòng, vị trí lật trang). Nó chia sẻ trường hợp sử dụng `tests/data/dialogue-paging-cases.json` với trò chơi và `tests/test_dialogue_paging.py` được sử dụng để kiểm tra xem ranh giới các trang có giống nhau hay không.
- Trang văn bản: `@intro:<资源号>` là nội dung cốt truyện được vẽ trong hình, đoạn mở đầu ở `intro.txt` (5506–5535), và phần kết thúc ở `ending.txt` (5570–5576). Không có so sánh ROM nào được thực hiện; trò chơi được vẽ nguyên bản bằng ngôn ngữ đọc và tiếng Nhật sử dụng dòng gốc trong mục nhập (`>`). `---` trong trang văn bản có nghĩa là một dòng trống, không phải là lật trang. Xem [Hình ảnh tiêu đề và Hình ảnh câu chuyện](../native/native-title-and-story-images.md).