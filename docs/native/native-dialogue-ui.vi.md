> **Ngôn ngữ / Language:** [Tiếng Việt](native-dialogue-ui.vi.md) · [English](native-dialogue-ui.en.md) · [中文](native-dialogue-ui.md)

# Giao diện người dùng đối thoại gốc

11-09-2026: Đã thêm các mục nhập thư mục ngôn ngữ tiếng Nhật và tiếng Trung cho JP ROM gốc thống nhất, xem [Triển khai lô đầu tiên của kiến trúc nội dung gốc](native-content-foundation.md). Hồ sơ hợp nhất hiện đang được sử dụng; bằng chứng lịch sử đang diễn ra dưới đây vẫn giữ nguyên phạm vi xác minh ban đầu.

2026-09-09. Việc triển khai này kết nối đoạn hội thoại cốt truyện khung đôi tiêu chuẩn trong bản đồ thế giới mở đầu siêu nhân nữ và bản đồ chiến thuật đầu tiên với giao diện người dùng chủ. Nó chạy tập lệnh cốt truyện gốc, đọc ID văn bản hiện tại, loa, đoạn STOP và trạng thái chờ, sắp chữ bằng công cụ văn bản đa nền tảng (FreeType + HarfBuzz + ICU, HarmonyOS Sans được đóng gói) và vẽ nó trên màn hình Metal cuối cùng. Phiên bản ban đầu sử dụng macOS Core Text, được thay đổi thành công cụ đa nền tảng bắt đầu từ ngày 20-09-2026. Xem [đối thoại văn bản và trò chơi đa nền tảng tiếng Trung, tiếng Nhật và tiếng Anh](portable-text.md).

## Hoạt động

Đoạn văn bản zoom mở đầu bầu trời đầy sao cũng hỗ trợ E + Enter để bỏ qua toàn bộ đoạn văn. Để biết chi tiết, hãy xem [Mở văn bản thu phóng](native-intro.md). Các chức năng đọc còn lại trong bảng dưới đây dành cho hội thoại tiêu chuẩn.

| Chức năng | Chìa khóa trò chơi | Sơ đồ bàn phím hiện tại |
|---|---|---|
| Trang đọc tiếp theo; trang cuối cùng nâng cao cốt truyện gốc | Xác nhận A | Z |
| Để tăng tốc độ đọc tự động, nhấn và giữ để điều chỉnh liên tục | Lên | ↑ |
| Giảm tốc độ về 0 và quay về hướng dẫn sử dụng | Tiếp theo | ↓ |
| Tắt tự động đọc/hủy bỏ qua | B |
| Chuyển tiếp nhanh: nhấn một lần để lật một trang, nhấn và giữ trong 0,3 giây để lật một trang cứ sau 0,1 giây; phát hành để trở về chế độ thủ công và tính năng đọc tự động cũng sẽ bị tắt | R + A | E + Z |
| Bỏ qua ngắn: Kịch bản cốt truyện được thực thi trực tiếp đến điểm dừng tiếp theo (kết thúc kịch bản, chọn chi, chọn tấn công, chuyển sang chiến trường, v.v.), đoạn hội thoại và màn trình diễn không được phát và kết quả giống như sau khi đọc ([bỏ qua ngắn](script-skip.md)) | R + START (bộ điều khiển R1 + menu) | E + Nhập |
| Bật/tắt xem lại cuộc trò chuyện | L | Q |
| Đánh giá: cuộn lên xuống một dòng, rẽ trái và phải một màn hình (nhấn và giữ liên tục; phím điều khiển giống như phím chéo) / return; quay lại không tiến triển cốt truyện | phím chéo hoặc cần điều khiển / A, B, L, START | ↑↓←→ hoặc WASD / K, L, Q, Enter |
| Cỡ chữ 10–18, mặc định 13 | C trên/C dưới | Tôi/K |

Tay cầm cũng có hai phím chủ (không hiển thị trong trò chơi): R2 để tua nhanh (giống như R+A; R2+menu cũng được phát âm là R+Start, nhưng nhấn R2 sẽ kết thúc trang hiện tại trước. Phím menu thường nằm giữa hai câu nên thanh nhắc nhở đọc R1+menu) và L2 chuyển sang đọc tự động (tốc độ cuối cùng được sử dụng, lần đầu tiên là số 2). Xem [Bàn phím Steam Deck](../design/steam-deck-controls.md).

**Tự động ẩn thanh dưới cùng (2026-10-06, người dùng xác định):** Thanh dưới cùng (chế độ đọc, tốc độ tự động, cỡ chữ, lời nhắc phím) bên dưới đoạn hội thoại bị ẩn trong 5 giây sau khi đoạn hội thoại xuất hiện và được hiển thị trong 3 giây khi nhấn bất kỳ phím điều hướng nào hoặc thay đổi chế độ đọc (cỡ chữ, tốc độ tự động, tự động chuyển, xem lại, tua đi, bỏ qua); nó luôn được hiển thị khi tua đi và bỏ qua; chuyển đổi bàn phím và tay cầm (biểu tượng nhắc thay đổi tương ứng) cũng được hiển thị trong 3 giây. 0,3 giây cuối cùng mờ dần. Việc lật trang thông thường không được tính. Bấm giờ VI (60 lần/giây), ở `native_dialogue.cpp` (`bar_until`, `show_bar`); `Frame.bar_fade` được chuyển cho `dialogue_scene.cpp`, `Painter::fade` được nhân với phần đệm và độ trong suốt của văn bản của thanh dưới cùng và nhập khóa bộ đệm của bản vẽ tăng dần. Khi nó bằng 0, toàn bộ thanh không được vẽ. Có khối `controls_bar` (`fade`) trong báo cáo kịch bản. Có thể thay đổi "Tùy chọn → Giao diện → Lời nhắc thao tác đối thoại" thành luôn hiển thị (`presentation.json`'s `dialogue_hints`: `auto`/`always`).

Tốc độ tự động 1–4 thay đổi đồng thời tốc độ hiển thị và thời gian chờ sau khi đọc; 0 là thủ công. Phím xác nhận sẽ chuyển trực tiếp đến trang đọc tiếp theo và không cần phải hoàn thành hoạt ảnh từng từ trước khi nhấn lại. Giữ Bình thường để xác nhận sẽ không thăng tiến liên tục. Cốt truyện nhanh vẫn tiến triển theo trang đọc. Bỏ qua ngắn (từ 29-09-2026) không còn xác nhận từng trang: máy chủ liên tục thực thi các lệnh tập lệnh trong cùng một khung và không hiển thị đoạn hội thoại, chờ và thực hiện khi khung hoàn thành, xem [bỏ qua ngắn](script-skip.md). Toàn bộ đồng hồ của trò chơi chưa được sửa đổi.

**Khóa phát hành chuyển tiếp nhanh (2026-09-27):** Người dùng yêu cầu sau khi nhả phím Chuyển tiếp nhanh, họ sẽ ngay lập tức quay lại "Nhấp để chuyển tiếp".

- Trước khi thay đổi (kết luận mã chỉ đọc): ở trạng thái tua nhanh, mỗi khung hình được tính toán lại theo phím hiện tại (nhấn R và A cùng lúc) và không có chốt. Vì vậy, sau khi thả khung ra sẽ không tua đi nhanh nữa, không vào chế độ đọc tự động và chữ Z đầu tiên sau khi thả ra sẽ không bị nuốt. Có ba lý do khiến nó không giống như “click and go”:
- Nhấn khung đó để lật 1 trang trước, sau đó là 6 VI (0,1 giây). Như vậy giữ tổ hợp phím hơn 0,1 giây sẽ lật được hai trang. Trên bàn phím, trước tiên hãy nhả Z rồi nhấn Z trong khi vẫn nhấn E và nó sẽ tua nhanh trở lại; điều tương tự cũng xảy ra khi nhấn nhanh R2 trên tay cầm. Một cú nhấp chuột bình thường thường lật hai trang.
- Tua nhanh mà không tắt tính năng đọc tự động. Hóa ra chế độ tự động đọc đang bật nhưng sau khi nhả ra thì nó lại tiếp tục tự động tắt.
- Với tốc độ 10 trang mỗi giây cộng với thời gian phản hồi, thông thường bạn sẽ đọc được thêm 2–3 trang nữa khi bạn buông tay. Trang cuối cùng của bài viết này đã được xác nhận. Phiên bản gốc sẽ kết thúc bài viết này như thường lệ. Dừng lại và đợi A sau khi bài viết tiếp theo xuất hiện. Đây chính là tốc độ tua đi nhanh, không tính trạng thái dư.
- Bây giờ (`Reader::update`, [dialogue_model.hpp](../../src/host/dialogue_model.hpp)):
- Nhấn phím tua nhanh để lật ngay một trang; sau khi nhấn và giữ trong `fast_hold_vis` (18 VI, 0,3 giây), cứ mỗi `fast_step_vis` (6 VI) sẽ lật một trang. Bấm nhanh chỉ lật một trang: Z khi vẫn nhấn E, bấm nhanh R2.
- Bản cập nhật đã phát hành sẽ trở về chế độ thủ công và tính năng đọc tự động sẽ bị tắt (người dùng chọn; nếu bạn muốn quay lại chế độ tự động, hãy nhấn L2 hoặc ↑). Trang hiện tại đã dừng chờ A và xác nhận lý lịch sẽ không vượt ra ngoài trang hiện tại. Nếu mục này đã được xác nhận khi bạn phát hành, bạn cũng sẽ đợi A sau khi mục tiếp theo xuất hiện.
- Trạng thái tua đi chỉ tuân theo các lần nhấn phím: ranh giới chữ viết và thay đổi ngôn ngữ sẽ không còn xóa được nữa. Vì vậy, khi bạn nhấn liên tục qua viền sẽ không được coi là click mới và phải chờ thêm 0,3 giây nữa.
- Bàn phím và bộ điều khiển tuân theo cùng một phán đoán: bộ điều khiển R2 được đọc là R+A trong `input()`, giống như E+Z. Menu R2+(R+A+Start) đi vào để bỏ qua phân đoạn hiện tại; việc phát hành R2 trong khi quá trình bỏ qua đang diễn ra sẽ không được xử lý và việc bỏ qua sẽ tiếp tục cho đến khi kết thúc tập lệnh, lựa chọn hoặc chuyển cảnh.
- Hai bản ghi mới được thêm vào nhật ký sự kiện: `fast` (`held`, `automatic`, `skip`) được ghi lại mỗi khi nhấn và nhả phím tua đi nhanh và `turn` (`page`, `pending`) được ghi lại mỗi khi người đọc lật một trang (kể cả trang cuối cùng và bước vào trạng thái chờ) và liệu có phải trang đó không vào thời điểm đó. `fast`). Ảnh chụp nhanh trạng thái đã được thêm `fast`.
- Kiểm thử thành phần (`tests/native_dialogue.cpp`, chạy dưới dạng `dialogue-reader` trong `tests/dialogue_cpu`) bao gồm các tình huống sau. Người đọc trước khi thay đổi không thành công ở mục "bấm nhanh để chỉ lật trang":
- Bấm nhanh và E trong khi giữ điểm Z sẽ chỉ lật được một trang.
- Nhịp điệu lật trang khi nhấn.
- Sau khi phát hành không có chuyển trang hay xác nhận lý lịch trong vòng 1900 VI. A chỉ lật một trang mỗi lần.
- Hãy thả vật phẩm này ra sau khi xác nhận và chờ đợi vật phẩm tiếp theo. A. Tắt tính năng đọc tự động.
- Nhấn và giữ qua ranh giới script không phải chờ lại.
- R2+Menu Bỏ qua để tiếp tục sau khi phát hành R2.
- Kịch bản kiểm tra máy thực tế `tools/recomp/debug/check_fast_release.py`: Đọc đoạn hội thoại đầu tiên của trò chơi mới, thực hiện tuần tự các thao tác sau, phán đoán theo `fast`/`turn` vào nhật ký và ghi kết quả là `fast-release-checks.json`:
- E+Z Nhấn và thả ra, sau đó nhấn Z lần nữa.
- Nhấn và giữ E điểm Z.
- Nhấn và thả R2 rồi nhấn lại A.
- Bấm nhanh R2.
- Nhấn và thả R2 trong khi tự động đọc đang bật.
- Thực đơn R2+.

Đối với hai mục nhấn nhanh, trước tiên hãy kiểm tra xem thời lượng nhấn và giữ có thực sự nằm trong khoảng 6-18 VI hay không. Nếu nó không nằm trong phạm vi này, nó sẽ bị coi là không hợp lệ. **Chưa chạy trên máy thật** (Người dùng quyết định chưa chạy nó vào ngày 27-09-2026).

Giao diện hiện tại giữ nguyên avatar gốc và bố cục khung đôi. Sử dụng `#69BFFF` màu xanh lam cho tên người; văn bản hiện tại có màu trắng và hộp thoại còn lại có màu xám. Phát lại lưu 256 đoạn hội thoại mới nhất của phiên hiện tại; trang đang được đọc chỉ ghi lại nội dung đã được hiển thị, các trang đã xác nhận có thể được đọc lại hoàn toàn và các tập lệnh tiếp theo chưa đến sẽ không được thêm trước.

**Sắp chữ (23-09-2026, để biết các quy tắc, hãy xem [Sắp chữ đối thoại](../design/dialogue-typesetting.md)): **
- Tên là số 10, đặt ở góc trên bên trái của ô; vùng văn bản nằm ngay bên dưới, chiều rộng 177 và chiều cao 43. Hộp có phạm vi từ 20 phía trên gốc văn bản đến 34 bên dưới, tổng cộng có 54 chiều cao.
- Số dòng trên mỗi trang có thể thích ứng theo cỡ chữ: trước tiên hãy tính xem có thể đặt bao nhiêu dòng theo khoảng cách dòng tối thiểu (1,08 lần đối với tiếng Trung, 1,15 lần đối với tiếng Anh), sau đó chia chiều cao còn lại cho mỗi dòng, tối đa 1,22 lần. Số 13 mặc định là 3 dòng trên mỗi trang cho cả tiếng Trung và tiếng Anh. Văn bản tiếng Anh được sắp xếp ở mức 0,85 lần cài đặt cỡ chữ và số hiển thị ở cột dưới cùng không thay đổi.
- Sử dụng lập trình động để chọn vị trí lật trang: số trang ít nhất, theo sau là ít cắt giữa câu, ít cắt dấu phẩy, ít một hoặc hai từ ở cuối dòng (không tính dấu câu và dấu ngoặc kép); khi các mục này giống nhau thì trang đầu sẽ đầy. Bước ngoặt trang gốc chỉ được tính là kết thúc câu trong tiếng Nhật: bản dịch đánh dấu sự kết thúc của chính câu đó, còn bước ngoặt trang gốc không có dấu câu là câu tiếp tục xuyên suốt trang. Do đó, dấu câu ở cuối dòng tiếng Trung có thể giảm xuống một nửa độ rộng khi thêm một từ.
- Ba chi tiết này được thiết lập vào ngày 24-09-2026 theo các dòng có dấu chấm câu ở cuối trang. 1.500 bản ghi nhiều trang được chọn để sắp chữ, số trang không thay đổi: trang tiếng Trung có câu cắt ở giữa là 116 → 31, trang đầu chỉ có một dòng là 156 → 55; trang tiếng Anh lần lượt là 229 → 80, 164 → 77.
- **Cả một câu thoại. ** Trong phiên bản gốc, các đoạn (giữa `<STOP>`) được bật ra bằng cách nhấn A mỗi lần sẽ được kết nối thành một đoạn. Tiếng Trung được kết nối trực tiếp và tiếng Anh được kết nối bằng dấu cách. Các trang được đánh số trang lại theo kích thước của khung. Khi trang được máy chủ lật chứa phần đầu của đoạn tiếp theo, `<STOP>` trước đó sẽ được xác nhận cho phiên bản gốc ở chế độ nền; `<END>` sẽ được xác nhận khi nhấn A ở trang cuối cùng. Số lượng xác nhận ban đầu luôn là số mảnh vỡ cộng với một và nó sẽ chỉ tiến về phía trước. Việc hiển thị từng từ sẽ dừng trong 0,3 giây khi đến điểm chuyển trang gốc.
- Số lượng clip dựa trên bản ghi ROM của Nhật Bản (là những gì trò chơi thực sự thực hiện). Khi `---` của bản dịch nhỏ hơn văn bản gốc, những bản dịch còn thiếu sẽ được xác nhận ở trang cuối cùng; những phần bổ sung sẽ được coi như những đoạn câu thông thường.
- Khi thay đổi cỡ chữ, toàn bộ bài viết sẽ được sắp xếp lại và trang hiện tại vẫn bắt đầu từ cùng một phông chữ. Khi chuyển đổi ngôn ngữ, toàn bộ đoạn văn sẽ được thay đổi sang ngôn ngữ khác và việc đọc tiếp tục từ đầu đoạn hiện tại trong phiên bản gốc.
- Các tuyến chiến đấu không được sắp xếp liền mạch: vẫn được thay thế và hiển thị từng đoạn theo clip gốc, cỡ chữ giảm dần khi không vừa.
- **Xác minh máy thật (24-09-2026, `tools/recomp/debug/check_dialogue.py`): ** Đối với trò chơi mới, chọn nhân vật chính và tên mặc định, đọc 18 đoạn hội thoại từ đầu tuyến (15 đoạn hội thoại tiếng Trung, 3 đoạn tiếng Anh, 11 đoạn trong số đó có điểm chuyển trang gốc, tối đa 3) và tất cả 25 cuộc kiểm tra đều vượt qua.
- Số lần xác nhận lý lịch cho mỗi mục bằng số `<STOP>` và `<END>` đúng một lần; phiên bản gốc không bao giờ xuất hiện ở đầu trang chủ.
- I/K được thực hiện hai lần bằng tiếng Trung và tiếng Anh và phần đầu của trang hiện tại không thay đổi.
- F7 xoay tiếng Trung→Anh→Nhật→Trung (hoặc Anh→Nhật→Trung→Anh) ba lần. Mỗi lần như vậy, nó tiếp tục đọc từ đầu phân đoạn hiện tại của phiên bản gốc và phiên bản gốc không tiến lên.
- Trong ảnh chụp màn hình, dòng tên không trùng với văn bản và cả ba dòng văn bản đều nằm trong khung.
- Vấn đề về nội dung nhìn thấy: Tiếng Trung dịch bằng máy thường không có dấu câu khi lật trang gốc, đọc thành câu (chẳng hạn như “Thật ngớ ngẩn khi quân du kích của bạn thua trận…”); tên mặc định của nhân vật chính và đối tác vẫn là katakana tiếng Nhật.
- Các trường hợp sử dụng được so sánh với triển khai tham chiếu Python là `tests/data/dialogue-paging-cases.json`: 30 (dòng thực bằng tiếng Trung và tiếng Anh, bao gồm các kích thước phông chữ khác nhau và chuyển trang bắt buộc). Tất cả số lượng trung gian được sử dụng bằng cách sắp chữ các quy tắc trên mỗi dải (ranh giới và chiều rộng của biểu đồ, ngắt dòng hợp lệ, dòng đầy đủ tại mỗi điểm bắt đầu), cũng như khoảng cách trò chơi, ranh giới dòng, lề và vị trí nửa chiều rộng. Nhập `dialogue-paging-inputs.json` trong cùng thư mục, được tạo bởi `tests/dialogue_cpu/paging_cases.cpp`; sử dụng `--check` để sắp xếp lại và so sánh, đồng thời chạy dưới dạng kiểm tra `dialogue-paging-cases` khi CMake đặt `SRW64_TEST_FONT_DIR`.

Các bổ sung mới nhất bao gồm thang đo tự động, tiến trình nâng cao tiếp theo và dấu loa hiện tại khung đôi, hãy xem [Mẹo đọc và xác minh máy thực tế](native-reading-indicators.md).

Tên trong bài đánh giá xen kẽ giữa màu xanh và cam theo người nói, và các clip liên tiếp của cùng một người vẫn giữ nguyên màu; cuộn qua phần xem lại hoặc cắt xén các bản ghi cũ hơn không làm thay đổi màu của các tên hiện có.

## Ranh giới dữ liệu và tập lệnh

- `8008C9C0` Sau khi văn bản được tải, ID văn bản thực tế được liên kết với phiên bản tập lệnh; đoạn hội thoại cốt truyện sử dụng quá trình tải của từng vị trí làm nhận dạng sự kiện (một bản ghi cho một sự kiện) và các dòng chiến đấu được thêm vào với số thứ tự STOP. Các khung lặp đi lặp lại không được nhập lại vào lịch sử.
- `8008D748` là chức năng nâng cao hội thoại gốc. Bộ đệm văn bản là `0x800FBAB0 + slot × 0x218`; bộ đệm tên là `0x8015CB00 + slot × 52`. Đọc trạng thái, văn bản, tên, chế độ thời gian, số lượng STOP và đoạn hiện tại và không coi số lần tải tài nguyên văn bản là tiến trình cốt truyện.
- Đường dẫn hiển thị vanilla này vẽ toàn bộ phân đoạn STOP cùng một lúc mà không có con trỏ nguyên văn vanilla có thể được kế thừa trực tiếp. Giao diện người dùng mới tự duy trì tiến trình hiển thị của các cụm glyph Unicode; trò chơi cung cấp các đoạn và trạng thái chờ. Việc kết hợp các ký tự và cặp thay thế UTF-16 không bị cắt thành nửa từ.
- Nguồn văn bản bên ngoài mặc định là `content/locales/zh-Hans.json`. Các bản dịch Unicode được chọn thông qua TextKey đầy đủ, với văn bản không được che phủ sẽ được đưa trở lại từ thư mục nguồn ROM gốc. Cho phép thêm văn bản và ngắt dòng nhưng phải giữ lại các rào cản tập lệnh STOP/END ban đầu. Tên động được mở rộng từ vùng đệm tên hiện tại của trò chơi.
- Trang đọc của giao diện người dùng mới chỉ tiêu thụ đầu vào của máy chủ. Khi trang lưu trữ đến đoạn tiếp theo, nó sẽ tạm thời gửi trình kích hoạt A tới `8008D748` ban đầu để xác nhận `<STOP>` và ngay lập tức khôi phục trường đầu vào; nếu phiên bản gốc không nâng cấp, nó sẽ bị gửi lại sau 0,5 giây. Sau khi nhấn A ở trang cuối cùng, tất cả `<STOP>` đều được xác nhận và sau đó `<END>` được gửi. Gia số STOP, trạng thái hoàn thành và biểu đồ tiếp theo đều được xử lý bởi hàm ban đầu. Cuộc đối thoại được hẹn giờ cũng chờ trang đọc của giao diện người dùng mới. Trong bản ghi sự kiện, mỗi xác nhận lý lịch được ghi dưới dạng `guest_stop` và `<END>` dưới dạng `guest_confirm`.
- `8009EFDC` cung cấp ranh giới phiên bản tập lệnh; nhìn lại chỉ tạm dừng bỏ phiếu cho tập lệnh sở hữu. `8009FA94` Chọn mục nhập nhánh, chấm dứt tập lệnh và các thay đổi lớp phủ cần bỏ qua để ngăn chúng được đưa sang giai đoạn tiếp theo.
- Bộ điều hợp đồng thời kiểm tra lớp phủ bản đồ thế giới/bản đồ chiến thuật (ROM `0xA7EC0`, `0xAB160`), tên điểm đánh dấu hiển thị, tọa độ và hộp thoại tiêu chuẩn `189×61`. Các giao diện không khớp vẫn tiếp tục hiển thị như cũ.
- Tên người phát biểu được dịch sang ngôn ngữ hiện tại theo số bản ghi (`+0`) trong thẻ tên; nếu phông chữ hiển thị trên thẻ không nhất quán với văn bản gốc tiếng Nhật của bản ghi (chẳng hạn như tên nhân vật chính do người chơi nhập vào), nó sẽ không thay đổi. Khi xem lại các mục nhập, hãy lưu người nói theo ngôn ngữ và thay đổi chúng cùng nhau khi chuyển bằng phím F7.
- **Battle Lines** (Tham gia vào ngày 23-09-2026; Xác minh thực tế ở cấp độ nhỏ `battle-ui` trong cùng một ngày: 4 dòng đều là bản vẽ lại gốc, không còn hình tượng gốc, văn bản và loa tiếng Trung và tiếng Anh chuyển đổi đều từ thư mục ngôn ngữ và tệp dòng, không có `battle_overflow`): Trải nghiệm dòng của lớp phủ trận chiến (ROM `0x121560`) `8008FFAC → 8008F648 → 8008CD8C` nhập cùng một bộ vùng đệm văn bản và tên cũng như cùng một hộp `189×61`, do đó, nó cũng nằm trong phạm vi thích ứng, nhưng chỉ **thay thế hiển thị** được thực hiện: không có sự kiện đọc nào được tạo, không có đầu vào nào được tiếp nhận và các trường thời gian không bị thay đổi. Phiên bản gốc được nâng cao và tính giờ như bình thường, số khung và gieo số ngẫu nhiên vẫn không thay đổi. Bản dịch không được đánh số trang. Nếu nó không vừa trên một trang, nó sẽ giảm dần kích thước phông chữ hiện tại xuống 9. Nếu vẫn không khớp, nhật ký sẽ ghi `battle_overflow` và mỗi câu sẽ ghi `battle_quote`. Thanh trạng thái đọc ở phía dưới không được hiển thị và không thể xem lại chiến tuyến.

## Vẽ tranh

`native_dialogue.cpp` Phát hành ảnh chụp nhanh bất biến từ chuỗi trò chơi. `graphics.cpp` Chỉ xóa hình chữ nhật glyph cũ khớp với hai hộp văn bản trong phạm vi bản vẽ hộp thoại `8008DC40` ban đầu, sửa đổi bản sao được gửi tới RT64 mà không thay đổi danh sách hiển thị gốc RDRAM. Nền, hình đại diện, đường khung và điểm đánh dấu bản đồ được giữ lại riêng biệt.

Móc kết xuất RT64 hiển thị ID khối lượng công việc hiện tại và văn bản mới được liên kết với khung trò chơi tương ứng để tránh sai lệch tên/hộp thoại do sự chậm trễ trong hàng đợi kết xuất gây ra. Công cụ văn bản chia các trang thành các dòng trong độ rộng văn bản logic (xem [Thiết lập đối thoại](../design/dialogue-typesetting.md) để biết các quy tắc), phân loại theo điểm ảnh có thể vẽ cuối cùng và Kim loại được tổng hợp trong quá trình kết xuất cuối cùng. Các thay đổi về cửa sổ sẽ tạo lại văn bản rõ ràng mà không làm giãn hình ảnh văn bản có độ phân giải thấp. Bố cục trò chơi hiện tại vẫn là tỷ lệ 4:3 ở giữa; mở rộng cửa sổ không có nghĩa là mở rộng trường nhìn bản đồ.

## Sao chép và bằng chứng

`scripts/Play SRW64 Native.command` được bật theo mặc định. Để xem lại phần mở đầu trò chơi mới:

```sh
.venv/bin/python tools/recomp/run/play_native.py --profile config/recomp/profiles/play-profile.json --new-game
```

Chọn siêu loại nữ và tên mặc định. Lối vào này vẫn sử dụng thư mục dùng thử độc lập và bản lưu trữ.

Tập lệnh giao diện gỡ lỗi để kiểm tra máy thực `tools/recomp/debug/check_dialogue.py`: Khi bắt đầu lộ trình đọc sau trò chơi mới, hãy kiểm tra từng số xác nhận nền, I/K và F7. Kết quả được thể hiện ở phần “Sắp chữ” bên trên.

Dưới đây là bằng chứng lịch sử cho phiên bản gốc vào ngày 2026-09-09. Tại thời điểm hiển thị bằng Core Text, việc kiểm tra verify_native_dialogue.py được thực hiện bởi tệp điều khiển, cả hai tệp này đều đã bị xóa. Việc kiểm tra tại thời điểm đó chỉ gửi các lần nhấn phím và kích thước cửa sổ SDL tùy chọn tới máy chủ và không sửa đổi bộ nhớ trò chơi. Bằng chứng được ghi lại riêng biệt: `dialogue-state.json` là trạng thái hội thoại của CPU, `dialogue-events.jsonl` là sự kiện phân đoạn/xác nhận/ranh giới, `dialogue-present.json` là khối lượng công việc kết xuất thực tế, `present-*.png` là đọc lại sau khi hoàn thành GPU và `ui-checks/acceptance.json` là kiểm tra lần chạy.

Kiểm tra tĩnh: `make check`. Kiểm tra trạng thái sắp chữ và đọc: `cmake --build build/recomp/gfx-build --target srw64-dialogue-test`, sau đó chạy `build/recomp/gfx-build/srw64-dialogue-test`.

Các bước kiểm tra đang chạy thực tế ở `build/recomp/native-dialogue/live-4/ui-checks/acceptance.json`: hội thoại đích `17412 / STOP 1`, ngắt trang 18, tạm dừng và cuộn phát lại, xác nhận quay lại mà không chuyển tiếp, tốc độ tự động quay về 0, ba kích thước cửa sổ, phím nhả chuyển tiếp nhanh, mở bỏ qua ranh giới và câu đầu tiên của bản đồ chiến thuật `17460` đã vượt qua. Trong số đó, "Fast Forward Release Key" là sử dụng tệp điều khiển để giữ R+A 24 VI cùng lúc rồi thả ra cùng lúc. Sau đó, các sự kiện đối thoại trong 160 VI không thay đổi và không còn tự động đọc; không có xác minh nào rằng A chỉ lật một trang sau khi phát hành và không có xác minh nào rằng E vẫn được nhấn, R2 và bật tính năng đọc tự động. Những tình huống này sau đó đã được thêm vào phần "Khóa phát hành chuyển tiếp nhanh" ở trên. Các ảnh chụp màn hình đều là các lần đọc lại GPU sau khi tập lệnh CPU thực sự chạy. Bỏ qua chuyển đổi lớp phủ đã dừng ở VI 18056, câu đầu tiên của bản đồ xuất hiện ở VI 19364 và tiếp tục chờ thủ công.

`live-3` là vòng kiểm tra trước: chức năng chính hiển thị nhưng kiểm tra ảnh chụp màn hình thay đổi kích thước đã sử dụng nhầm mẫu trạng thái 60-VI dày hơn và có thể tham chiếu nhiều lần khung cũ, do đó việc chấp nhận chia tỷ lệ cửa sổ sử dụng khung độc lập `live-4` đã sửa đổi. Kiểm tra chuyển tiếp nhanh ban đầu của `live-4` cũng được lấy mẫu trước khi khóa được giải phóng; thay vào đó, nó đợi VI thực tế và thời lượng trong biên nhận kiểm soát, sau đó vượt qua bài kiểm tra lại trong cùng một quy trình trò chơi. Vấn đề trên thuộc về thời gian lấy mẫu của tập lệnh xác minh và các xác nhận không thành công không được tính là bằng chứng thành công.

Vòng này không có nghĩa là tất cả giao diện người dùng của toàn bộ trò chơi đã được tiếp quản. Đầu vào tên, menu tùy chọn, menu chiến thuật/vũ khí và văn bản trong ảnh vẫn đi theo đường dẫn hiện có; các nhánh sau chiến tranh, các phân đoạn lịch sử sau tải và tất cả các kết hợp DPI màn hình thực phải được thêm vào với phạm vi chạy tương ứng. Các nút điều khiển hiện tại được xác minh bởi trạng thái đầu vào N64 của máy chủ; máy chủ này chưa được kết nối với thiết bị điều khiển vật lý.

## Sửa lỗi thoát khỏi máy chủ

Quá trình kiểm tra khởi động/thoát thực tế của mục HD đã phát hiện ra rằng luồng hẹn giờ trong thời gian chạy phiên bản cố định sử dụng `detach`, luồng này có thể vẫn chạy sau khi chương trình chính giải phóng RDRAM và hủy hàng đợi. Báo cáo sự cố xác định hàng chờ tại `timer_thread`.

`prepare_runtime_lifecycle.py` Tạo hai bản sao được biên dịch cục bộ từ nguồn ngược dòng bị khóa và chưa sửa đổi: đánh thức chuỗi hẹn giờ bằng thông báo dừng và `join` trước khi giải phóng RDRAM. Thanh toán ngược dòng vẫn còn nguyên; SHA-256 trước và sau tệp được tạo được ghi vào `build/recomp/runtime-lifecycle/manifest.json` và báo cáo chạy trên máy chủ cũng ghi lại sự thích ứng này. `tests/native_timer_shutdown.cpp` kiểm tra hàng đợi trống, thời gian chờ lâu, bộ đếm thời gian, tắt máy lặp lại và vòng đời RDRAM trên mã nguồn thích ứng thực tế và lặp lại addressSanitizer / Und xác địnhBehaviorSanitizer 30 lần.

Kiểm tra khởi động/thoát mục nhập HD cuối cùng đã hoàn thành 1.704 VI, thoát 0, SHA-256 của SRAM ban đầu không thay đổi. Việc sử dụng vòng đời quy trình xác minh thiết bị âm thanh giả SDL này không được sử dụng làm bằng chứng thử giọng của diễn giả. 47 Kiểm tra Python, kiểm tra trạng thái đọc/văn bản cốt lõi và kiểm tra thoát khởi động máy chủ CPU đã vượt qua. Tổng bản ghi phân phối là `build/recomp/native-dialogue/acceptance.json`, phân biệt giữa một lần chạy giao diện người dùng trực tiếp gồm 22.758 VI, thử nghiệm thành phần tự động văn bản dài tiếp theo đang chờ sửa lỗi và kiểm tra mục nhập sau khi sửa lỗi cuối cùng trong vòng đời.

Để tái tạo việc kiểm tra bộ đếm thời gian:

```sh
clang++ -std=c++20 -fsanitize=address,undefined -g \
  -I build/recomp/runtime-lifecycle \
  -I build/recomp/upstream/N64ModernRuntime/ultramodern/include \
  -I build/recomp/upstream/N64ModernRuntime/thirdparty \
  -I build/recomp/upstream/N64ModernRuntime/thirdparty/concurrentqueue \
  tests/native_timer_shutdown.cpp -o build/recomp/native-dialogue/timer-shutdown-test
build/recomp/native-dialogue/timer-shutdown-test
```