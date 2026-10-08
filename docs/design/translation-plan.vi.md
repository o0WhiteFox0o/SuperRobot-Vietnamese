> **Ngôn ngữ / Language:** [Tiếng Việt](translation-plan.vi.md) · [English](translation-plan.en.md) · [中文](translation-plan.md)

# Bản địa hóa toàn văn: xuất văn bản và dịch tiếng Trung-Anh

Ngày: 23-09-2026. Tài liệu này giải thích những điều sau đây:

- Cách xuất toàn bộ văn bản;
- Ai chịu trách nhiệm dịch thuật;
- Cách sử dụng DeepSeek trên Alibaba Cloud Bailian để tạo bản thảo đầu tiên bằng tiếng Trung và tiếng Anh và thực hiện đánh giá AI;
- Cách cung cấp bản dịch cho trò chơi;
- Sau đó còn những bước nào?

Các con số được lấy từ các cuộc gọi thực tế và kết quả sản xuất trong ngày.

## Kết luận

- **XUẤT**: Bao gồm tất cả 51.174 bản ghi văn bản ROM, 30 trang văn bản mở rộng (được phiên âm bởi con người) và 244 bản sao giao diện người dùng gốc, mỗi bản được nhóm thành một danh mục có ngữ cảnh. Công cụ xuất sẽ kiểm tra hai điều: mỗi bản ghi xuất hiện chính xác một lần và vùng ô (bắt đầu từ 17347) khớp chính xác với 33.628 số văn bản thực sự được tham chiếu trong tập lệnh.
- **Phân công lao động**:
- Tên, giao diện và lời nhắc hệ thống (các phần của bản ghi 0–5798 cần dịch) được liệt kê trong danh sách dự thi và cả bộ tiếng Trung và tiếng Anh đã được hoàn thành trong một phiên khác. Xem [Trung Quốc hóa văn bản dữ liệu: danh sách mục nhập và thông số dịch thuật](../native/localization-terms.md);
- Lời thoại cốt truyện, lựa chọn nhân vật, lời thoại chiến đấu và đoạn mở đầu đều tuân theo quy trình dịch máy sang máy của bài viết này. Tên người, tên máy, tên vũ khí đều được lấy từ danh sách nhập. Ngoài ra còn có danh sách từ vựng tiếng Trung và tiếng Anh (`content/translation/story-terms.json`) cho các tên riêng duy nhất trong dòng.
- **Trạng thái hoàn thành (23-09-2026)**: Bản thảo đầy đủ đầu tiên và một vòng đánh giá AI bằng cả tiếng Trung và tiếng Anh đã được hoàn thành.
- Bản nháp đầu tiên sử dụng `deepseek-v4.1-flash` (DeepSeek với số phiên bản mới nhất trong không gian kinh doanh), các mục không được kiểm tra sẽ được thử lại trong ba vòng và `deepseek-v4-pro-0813` được sử dụng trong vòng cuối cùng.
- Sử dụng `deepseek-v4-pro-0813` để xem xét.
- Kết quả: 45.197/45.206 mặt hàng Trung Quốc đã vượt qua tất cả các cuộc kiểm tra cơ học, và 45.139 mặt hàng Anh đã vượt qua; 2.114 mục tiếng Trung và 1.931 mục tiếng Anh đã được sửa đổi.
- **Cách chuyển giao cho trò chơi**: Các dòng do người dùng quyết định được tạo thành một tệp văn bản mà người chơi có thể thay đổi và không được hợp nhất vào thư mục ngôn ngữ.
- `tools/translation/write_dialogue.py` đã được viết `content/dialogue/{zh-Hans,en}/`, 422 tệp cho mỗi ngôn ngữ, với 45.013 bản dịch máy, 70 mẫu cần dịch và 30 trang mở đầu.
- Có 93 đoạn hội thoại viết tay khác trong `story/scene-0001.txt`, không bị trình tạo thay đổi.
- Kết thúc đọc được thực hiện bởi một phiên khác (`da649d3`) và kết quả mở rộng của C++ và Python nhất quán từng cái một, không có lỗi.
- **Chi phí**: Tất cả các cuộc gọi có giá khoảng 50 nhân dân tệ dựa trên giá flash; trong đó quá trình đánh giá và vòng thử lại cuối cùng là chuyên nghiệp và giá của bản chuyên nghiệp tùy thuộc vào bảng điều khiển.
- **Bước tiếp theo**: Chủ yếu xem xét thủ công (văn bản gốc duy nhất khoảng 910.000 từ) và truy cập hiển thị.
- **Sắp chữ đối thoại (Được xác định vào ngày 23-09-2026)**: Phông chữ HarmonyOS được đóng gói theo cách thống nhất và cỡ chữ tiếng Anh gấp 0,85 lần cỡ chữ. Một câu thoại được sắp xếp thành một hàng và các bước ngoặt của trang gốc chỉ được đồng bộ hóa. Tên vẫn nguyên trong ô nhưng dòng tên được thắt chặt. Theo mô phỏng, số lần lật trang giảm 24% bằng tiếng Trung và 37% bằng tiếng Anh, xem [Sắp xếp hội thoại](dialogue-typesetting.md).
- Giờ đây, đoạn hội thoại cốt truyện có thể được hiển thị trong trò chơi;
- Các chiến tuyến đã được kết nối và xác minh máy thực tế vào ngày 23/09/2026 rằng việc chuyển đổi giữa tiếng Trung và tiếng Anh là bình thường;
- Đoạn mở đầu, thẻ tiêu đề chương và trang kết thúc 2026-09-24 đã được vẽ nguyên bản bằng ngôn ngữ đọc, xem [Màn hình tiêu đề và hình ảnh văn bản cốt truyện](../native/native-title-and-story-images.md); việc lựa chọn tay chân và điều kiện thắng thua vẫn chưa được kết nối.
- Ở trang đánh giá cốt truyện, bạn có thể so sánh văn bản gốc với bản dịch tiếng Trung và tiếng Anh (xem P3).

## 1. Xuất khẩu

```sh
.venv/bin/python -B tools/content/extract_original.py      # 先有原始数据目录（make recomp-data）
.venv/bin/python -B tools/content/export_text.py           # → assets/text-export/
```

Đầu ra chứa văn bản gốc tiếng Nhật, chỉ được đặt trong `assets/text-export/`, văn bản này bị git bỏ qua và được thay thế toàn bộ mỗi lần. Hoàn thành trong khoảng 2 giây.

| Tài liệu | Nội dung |
| --- | --- |
| `manifest.json` | ROM, mã sản xuất và tóm tắt tệp đầu vào, số lượng từng danh mục, bảng khoảng số, ký tự điều khiển và mô tả thẻ, SHA-256 của tất cả các tệp đầu ra |
| `records.jsonl` | Một dòng cho mỗi bản ghi: `key`, `category`, `group`, cơ sở (`code`/`content`/`transcribed`), văn bản gốc không mất dữ liệu `source` (bao gồm) `<BR>`/`<STOP>`/`<G:XXXX>`), `display` (tên động được xếp thành [tên nhân vật chính], v.v.), `source_sha256`, số từ hiển thị, thẻ, `native_page`, `terms_section`, có sẵn bản dịch tiếng Trung và tiếng Anh và ngữ cảnh theo danh mục |
| `summary.md` | Số lượng bản ghi trong mỗi danh mục, số lượng văn bản gốc duy nhất, số từ, trang gốc và độ bao phủ của bảng mục nhập |
| `categories/*.csv` | Một bảng cho mỗi danh mục (UTF-8 BOM, có thể mở trực tiếp bằng Excel): khóa, tóm tắt ngữ cảnh, văn bản gốc (⏎ nghĩa là ngắt dòng, ▸ nghĩa là lật trang), đánh dấu, bản dịch hiện có |
| `story/scene-NNNN.json` | 142 cảnh, liệt kê diễn biến, giai đoạn, điều kiện kích hoạt, đoạn lộ trình, diễn giả và ứng cử viên, phương thức đối thoại của từng câu theo thứ tự kịch bản |
| `battle/speaker-runs.json` | Các chiến tuyến theo thứ tự trong bảng và cùng một người nói là một đoạn văn liên tục (1.524 đoạn) |
| `battle/triggers.json` | Bảng chọn dòng chiến đấu được sắp xếp theo giọng nói (ngược lại 27-09-2026, xem [battle-quotes.md](../data/battle-quotes.md)): chín đoạn chung cho mỗi giọng nói, cũng như mã điều kiện, diễn giải các dòng điều kiện và ghi lại chuỗi số của các cuộc hội thoại nhiều người |

Các trường ngữ cảnh khác nhau theo danh mục:

- Cốt truyện: Tất cả các vị trí đều xuất hiện. Các tập lệnh được chia sẻ sẽ xuất hiện trong nhiều cảnh, trong đó cảnh đầu tiên đóng vai trò là bối cảnh chính.
- Dòng chiến đấu: loa (ba chữ số đầu tiên của tiêu đề văn bản), đoạn văn và vị trí trong đoạn văn, câu mở đầu của kỹ năng kết hợp (tiêu đề văn bản có hậu tố `0024`); `triggers` (diễn giải các điều kiện kích hoạt như tình huống, vũ khí, đối thủ, phi công phụ, kỹ năng kết hợp, v.v. cũng như trình tự và vị trí được đưa ra trong cuộc trò chuyện nhiều người), `voice` và `voice_actors` (số giọng nói và nhân vật sở hữu nó).
- Tên: cơ thể/vũ khí/số ký tự và các bản ghi tương ứng, chẳng hạn như tên menu vũ khí ↔ tên thuần túy, tên viết tắt ↔ tên đầy đủ, tên tinh thần ↔ mô tả.

thẻ:

| Đánh dấu | Ý nghĩa |
| --- | --- |
| `numeric-gap` | Bản gốc vẽ số vào khoảng trắng, bản dịch phải giữ lại khoảng trắng |
| `fragment` | Các đoạn câu được ghép lại với nhau khi chạy |
| `dynamic-name` | Chứa tên động |
| `paged` | Chứa `<STOP>` Lần lượt trang |
| `blank` | Không có ký tự hiển thị |

Được triển khai trong `src/srw64_native/text_export.py` (phân loại và ngữ cảnh) và `tools/content/export_text.py` (ghi tệp), được thử nghiệm trong `tests/test_text_export.py`.

### Phân loại và cơ sở

Khoảng đánh số được so sánh theo từng phần; khoảng được xác nhận bởi công thức mã được đánh dấu `code`:

- Tập 281 + Cảnh
- Khung máy bay 527+
- Thần 969＋Số.
- Kích thước 1094+
- Bộ phận 1129＋Bộ phận
- Vũ khí 1370/2699+vũ khí
- Nhãn giữa cảnh và màn hình 4044–4144
- Ký tự 4382／4743＋Ký tự
- Cốt truyện đối thoại và lựa chọn cơ thể

Các khoảng còn lại được chia theo nội dung và được đánh dấu `content`. Số được trang gốc sử dụng trực tiếp được lấy từ hằng số `src/host/*_page.cpp` và được ghi trong `native_page`.

| Chịu trách nhiệm | Danh mục (số lượng hồ sơ) | Số từ hiển thị |
| --- | --- | ---: |
| **Bài viết này được dịch từ máy** | Cốt truyện đối thoại 33,582, lựa chọn tứ chi 46, mở đầu 30, chiến tuyến 11,534, chiến tuyến đặc biệt 14 | 1.145.144 (chỉ 908.925) |
| **danh sách tham gia** (phiên khác) | Từ tên 143, điều kiện thắng thua 73; thân 363, vũ khí 1.329 (tên menu 1.329 bắt nguồn từ đây), ký tự viết tắt/tên đầy đủ 361 mỗi ký tự, tên mặc định 16, danh sách ký tự 108; tinh thần 30 và ký tự đơn viết tắt 30, khả năng đặc biệt 15, kỹ năng 79, phần 20, địa hình 60, chức danh 50; nhãn giao diện 260, dấu nhắc hệ thống 65, nhập tên và trò chơi mới 27; tinh thần/bộ phận/sửa đổi/hướng dẫn phản công 96; tùy chọn tiêu đề 7 | Khoảng 36.000 |
| Giao diện người dùng gốc (bảng `ui`, bảo trì thủ công) | 244 mặt hàng; cả tiếng Trung và tiếng Anh đều được cung cấp | 2.777 |
| Sao chép, không dịch | Mô hình nội dung 115 (chỉ dịch văn bản không phải mô hình trong danh sách mục nhập), biểu tượng bản đồ 46, thanh tỷ lệ và mũi tên chuyển trang 123 | — |
| Không hiển thị hoặc đã được thay thế | Gỡ lỗi văn bản như trình chỉnh sửa hoạt hình trận chiến, trình chỉnh sửa logo cốt truyện, v.v. 421; quay số tên gốc 223 | — |
| **Quyết Tâm** | Tên bài hát 49, Lời bài hát Karaoke 199 (Bảng 1–19 trên 20) | 3.313 |

### Văn bản không có trong bảng văn bản

- **Văn bản thu phóng mở đầu**: 30 trang, phần mở đầu công khai 11 trang, bốn lộ trình, mỗi lộ trình 5–6 trang. Chúng là những hình ảnh kết cấu, không phải bản ghi văn bản.
- 2026-09-23 được chép thủ công từng dòng, có `assets/transcriptions/intro-pages.ja.json`, mỗi trang đều có đính kèm hình SHA-256; khi hình ảnh thay đổi thì quá trình xuất sẽ báo lỗi.
- Khóa xuất là `intro:<资源号>`, có đính kèm lộ trình và trình tự phát lại.
- Nhân vật chính nào tương ứng với Đường 1/3/4 được suy ra dựa vào nội dung văn bản: một chàng trai thuộc phong cách chiến đấu võ thuật, một chàng trai sinh ra từ vệ tinh thuộc địa và một cô gái du kích. Route 2 đã được máy thực tế xác nhận là Malino.
- 2026-09-27 Bản dịch từng trang tiếng Trung và tiếng Anh của Claude (đợt `read-fixes/intro-close.json`), xem [Kế hoạch đánh bóng dòng](dialogue-polish-plan.md) Giai đoạn 2c.
- **Thẻ tiêu đề chương**: 133 hình ảnh (`assets/original-graphics/chapter-titles/`). 24-09-2024 Nhận biết từng bức ảnh và so sánh với tên của cuộc gọi từng cái một. Trò chơi được vẽ theo bản dịch của tên cuộc gọi ([màn hình tiêu đề và hình ảnh văn bản cốt truyện](../native/native-title-and-story-images.md)).
- **Trang cuối**: 7 (5570–5576). 24-09-2026 Bản dịch tiếng Trung-Anh được chép lại và viết tay, được đặt trong `content/dialogue/<语言>/ending.txt`, cũng được vẽ nguyên bản; 2026-09-27 tinh chế.
- **Văn bản khác được đưa vào hình**: các từ hiệu ứng đặc biệt trong trận chiến, logo tiêu đề, v.v., chưa được hệ thống tính. Bài viết này không đưa ra tuyên bố nào đã được bảo hiểm.

## 2. Phân công lao động và ranh giới chữ viết

- **Bảng thuật ngữ**: Tên và văn bản hệ thống được duy trì theo phân vùng bởi `content/locales/terms/<locale>.json` và mỗi văn bản gốc khác nhau chỉ được dịch một lần; `tools/content/apply_terms.py` được mở rộng thành các mục nhập thư mục ngôn ngữ (`"origin": "terms"`). Dịch máy không viết các phím này.
- **Bản dịch máy**: `assets/translation-runs/<tag>/` tồn tại trước tiên, một bản sao cho mỗi lô, lưu ngữ cảnh yêu cầu, cách sử dụng và kiểm tra từng kết quả và có thể tiếp tục chạy. `run_mt.py collect` sắp xếp các mục đã kiểm tra thành định dạng thư mục ngôn ngữ (`"origin": "mt"`, `"review_status": "draft"`, với mô hình, phiên bản từ nhắc và thẻ lô) và xác minh chúng bằng `compile_locale`.
- **Đích cuối cùng của các dòng (cập nhật vào ngày 23-09-2026)**: Người dùng quyết định rằng cốt truyện và các dòng chiến đấu được tạo thành các tệp văn bản độc lập (dự kiến `content/dialogue/<locale>/`). Người chơi có thể tự sửa đổi chúng. Các tập tin đính kèm với chương trình có thể bị ghi đè bởi các tập tin có cùng tên trong thư mục người dùng. Các dòng không được hợp nhất vào `content/locales/*.json` cũng như không được hợp nhất vào thông số nhập được nhúng.
- Việc định dạng tệp, đọc, xác minh và ghi đè được xử lý bởi phiên bảng thuật ngữ và nội dung tệp được tạo ra bởi quá trình này; sau khi định dạng được hoàn tất, `collect` sẽ được xuất trực tiếp ở định dạng mới.
- Một trong những lý do từ bỏ việc sáp nhập vào thư mục ngôn ngữ là do kích thước. Theo số đo thực tế, nếu 45.013 dòng tiếng Trung và tiếng Anh được hợp nhất, mỗi tệp ngôn ngữ sẽ tăng từ khoảng 1,1 MB lên 13,5 MB, thông số nhập được sử dụng để nhúng sẽ tăng từ 1,7 MB lên khoảng 23 MB và tệp tiêu đề C++ được tạo ước tính có dung lượng khoảng 76 MB (hiện tại là 5,6 MB).
- **Thẻ nhân vật**: SRW64 Giới tính, danh tính và giọng nói của nhân vật gốc được viết bằng `content/translation/zh-Hans/roster.json`. Bản dịch không được xác định ở đây, bản dịch vẫn dựa trên danh sách đầu vào.

## 3. Quá trình dịch máy

Công cụ trong `tools/translation/`:

| Tập tin | Chức năng |
| --- | --- |
| `run_mt.py` | Hàng loạt, yêu cầu, kiểm tra, sửa (`run`), đánh giá AI (`review`), kiểm tra lại (`recheck`), báo cáo (`report`), sắp xếp thành định dạng thư mục ngôn ngữ (`collect`, các đợt tiếp theo ghi đè lên các đợt trước) |
| `run_full.sh` | Toàn bộ quá trình của một ngôn ngữ: hai bản nháp (lần thứ hai chỉ dành cho những đợt không đạt), hai bản hiệu đính và một báo cáo |
| `dashscope.py` | Giao diện tương thích Bailian OpenAI |
| `references.py` | Thẻ từ vựng và ký tự (tiếng Trung và tiếng Anh) |
| `term_candidates.py`, `draft_terms.py`, `audit_terms.py` | Đề xuất, soạn thảo và kiểm tra tính thống nhất của tên dòng |

Logic để đảm bảo cấu trúc dịch chính xác nằm trong `src/srw64_native/translation.py` và kiểm tra nằm trong `tests/test_translation.py`.

```sh
export SRW64_DASHSCOPE_ENV=<百炼 .env>
tools/translation/run_full.sh zh-Hans zh-v1 draft      # 或 review / all；en 同理
PYTHONPATH=src .venv/bin/python -B tools/translation/run_mt.py collect --tag zh-v1 --tag zh-v1-review --output <zh 文件>
```

**Đánh giá AI (`review`)**:

- Sử dụng `deepseek-v4-pro-0813`, tối đa 70 câu/đợt. Người mẫu xem văn bản gốc và bản nháp đầu tiên và chỉ trả về các mục cần thay đổi và lý do (bằng tiếng Trung).
- Những thay đổi cũng phải vượt qua tất cả các cuộc kiểm tra cơ học. Những thay đổi giống với dự thảo đầu tiên hoặc không thể kiểm tra được sẽ không được thông qua.
- Danh sách mục mới nhất và tên dòng được tải trong quá trình xem xét và những tên được quyết định sau bản nháp đầu tiên cũng có thể được thống nhất trong vòng này.

Thông tin xác thực được đọc từ `--env-file`, `SRW64_DASHSCOPE_ENV` hoặc gốc kho lưu trữ `.env` (bị git bỏ qua) và chỉ được gửi tới địa chỉ HTTPS của `*.aliyuncs.com`. Quá trình chạy thử đã sử dụng cấu hình không gian kinh doanh North China 2 hiện có của phiên bản tiếng Trung của "Mech Z".

Tham số yêu cầu: `temperature 0.1`, đầu ra JSON, tắt suy nghĩ; chỉ thử lại trên 429 hoặc 5xx. Tôi đã thử chế độ suy nghĩ trong chương đặc biệt của "Mech Z", nhưng lý luận sẽ cạn kiệt giới hạn đầu ra nên tôi đã không sử dụng nó.

### Đảm bảo tải

Mỗi văn bản nguồn được cắt thành các trang tại `<STOP>` và nhánh lựa chọn được cắt thành các tùy chọn tại `<BR>`. Xử lý trong trang:

- Xóa `<BR>` và hộp thoại gốc sẽ tự động ngắt dòng và phân trang;
- Mỗi chuỗi ký tự trong tên động sẽ trở thành phần giữ chỗ như [Tên nhân vật chính] và [Biệt danh của đối tác], đồng thời các ký tự đặc biệt khác trở thành ⟦G1⟧.

Mô hình phải trả về một mảng có cùng số trang và số lượng cũng như thứ tự của phần giữ chỗ không được thay đổi. Khi khôi phục, chuỗi mã gốc được đặt lại như cũ nên cấu trúc trang và `signature` nhất quán với văn bản gốc. Bất kỳ sự khác biệt nào sẽ dẫn đến lỗi và sẽ không có sửa chữa thầm lặng nào được thực hiện. `<` và `>` trong bản dịch sẽ được thay thế bằng các ký tự có độ rộng đầy đủ và mô hình không thể ghi các ký tự điều khiển.

### Phân khối và bối cảnh

**Cốt truyện**: Theo từng cảnh, không quá 40 câu hoặc 2.400 từ mỗi đợt. Các câu trong tập lệnh chia sẻ chỉ được dịch ở cảnh đầu tiên chúng xuất hiện và được sử dụng làm ngữ cảnh chỉ đọc (`ctx`) trong các cảnh khác. Các tập của cùng một cảnh được chạy theo thứ tự, tập sau chứa văn bản gốc và bản dịch của 8 câu cuối của tập trước; các cảnh khác nhau được chạy song song. Tổng cộng có 904 lô. Mỗi lô đi kèm:

- Tiêu đề cảnh và nhân vật chính;
- Các giai đoạn, đoạn đường và điều kiện kích hoạt của từng câu;
- Thẻ nhân vật người thuyết trình: Tên tiếng Trung lấy từ danh sách dự thi, ký tự gốc lấy từ danh sách, ký tự của các tác phẩm hiện có lấy từ phần giới thiệu và giới tính của sách minh họa tiếng Trung “Mech Z”, chỉ mang tính chất tham khảo;
- Danh sách từ liên quan: "Phải sử dụng" xuất phát từ các phân chia tên, cơ thể, vũ khí và tên công việc trong danh sách đầu vào của dự án này. Có ba trường hợp ngoại lệ chỉ mang tính "tham khảo": tên 1-2 ký tự (コウ, kiệt tác, nin), tên hiragana (ひかる), ボス, マスター và các từ thông dụng khác. Tên vũ khí Hiragana (した, くちばし) không tham gia so khớp; tinh thần, khả năng và các bộ phận chỉ mang tính chất "tham khảo". Một phần khác của "tham chiếu" đến từ danh mục tên riêng trong danh sách từ vựng tiếng Trung của "Mech Z". Nó chỉ chấp nhận các mục tiếng Nhật chưa được xác định trong danh sách đầu vào của dự án này và loại bỏ các mục chỉ viết bằng tiếng Anh.

**Battle Lines**: Mỗi đợt 60-80 câu theo thứ tự trong bảng, cố gắng cắt khi người nói thay đổi, tổng cộng 164 đợt. Trước khoảng 14000, đây là khối tình huống chung cho mỗi nhân vật. Thứ tự gần đúng là tấn công → bị bắn hạ → sát thương lớn → sát thương nhỏ → né tránh → tia phòng thủ → ngoài tầm/ngoài tầm. Tiếp theo là các dòng dành riêng cho vũ khí và đối thoại kỹ năng kết hợp nhiều người chơi. Bảng lựa chọn vẫn chưa được đảo ngược trong quá trình dịch máy và các từ gợi ý chỉ đưa ra mô tả về người nói và phần; quá trình đảo ngược được hoàn thành vào ngày 27-09-2026 ([battle-quotes.md](../data/battle-quotes.md)) và giai đoạn đọc chuyên sâu được xem xét bằng các điều kiện về giọng nói và kích hoạt (`tools/translation/read_battle.py`).

**Mở đầu**: Gồm 30 trang, tương ứng với các đoạn văn.

### Kiểm tra và sửa

Kiểm tra từng mục sau đây; những mục không kiểm tra được thì viết câu hỏi bằng tiếng Trung rồi gửi lại, chỉ dịch lại những mục này:

- Số trang, phần giữ chỗ, ký tự điều khiển;
- Bản dịch trống;
- Các bút danh còn lại;
- Chưa chuyển đổi "" "";
- Toàn bộ dấu ngoặc kép có theo cặp hay không;
- Tỷ lệ độ dài của bản dịch so với văn bản gốc.

Nếu bản dịch "phải sử dụng" không xuất hiện, nó sẽ chỉ được ghi lại dưới dạng cảnh báo và sẽ không được tự động truyền lại để ngăn những cái tên như "ボス" cũng là những từ thông thường bị buộc phải thay thế. Các câu hỏi do chính mô hình đánh dấu (tài liệu tham khảo không rõ ràng, cách chơi chữ, bản dịch mới) được viết bằng `flag`.

## 4. Kết quả chạy thử (23-09-2026)

phạm vi:

- Cảnh 0-2 của cốt truyện: Tập đầu tiên của 3 lộ trình ブラッド, マナミ, và アーク, có tổng cộng 273 câu, bao gồm các diễn giả được đặt tên theo các đoạn lộ trình;
- Đường chiến đấu 5813–5912 (khối chung của コウ/ガトー) và 15340–15420 (đối thoại nhiều người chơi của ファイナルダイナミックスペシャル), tổng cộng 181 dòng;
- Mở 30 trang.

| đợt | số lượng mặt hàng | vượt qua | mã thông báo đầu vào/đầu ra | mô tả |
| --- | ---: | ---: | --- | --- |
| Cốt truyện, lời nhắc v1 | 273 | 263 | Có bánh xe điều chỉnh | 9 câu ghép hai trang thành một trang, 1 câu để lại một trang trống; lời nhắc sửa lỗi của v1 bằng tiếng Anh và chưa được sửa chữa |
| Cốt truyện, lời nhắc v2 | 273 | 272 | 35.373 / 8.461 | Đánh số trang cho mỗi câu và quy định phải đặt dấu ngoặc kép ở đầu và cuối văn bản gốc; bánh xe chỉnh sửa đã cố định 2 câu, chừa lại 1 câu (8 trang đến 7 trang) để xử lý thủ công |
| Chiến tuyến | 181 | 181 | 10.645 / 3.846 | Vượt qua tất cả ở vòng đầu tiên |
| Lời mở đầu | 30 | 30 | 3.104 / 1.917 | Mẫu được đánh dấu bằng 3 bản dịch mới |
| Cảnh 1, `deepseek-v4-pro-0813` so sánh | 93 | 92 | 15.142 / 3.777 | 68 trên 93 câu trong flash có cách diễn đạt khác nhau |

Quá trình kiểm tra cơ học của lô v1 từng báo cáo 94 lỗi, hầu hết nguyên nhân là do người kiểm tra đánh giá xem các dấu ngoặc kép có được ghép nối dựa trên một trang hay không: dấu ngoặc kép của đoạn hội thoại ban đầu được mở ở trang đầu tiên và đóng ở trang cuối cùng. Toàn bộ phán đoán đã được thay đổi và kết quả đã lưu đã được kiểm tra lại bằng `recheck`. v1 Tất cả 13 lô đều có giá $0,26 (giá dựa trên giờ bận rộn).

Quan sát từ việc đọc thủ công:

- **Giọng điệu**: Sự kính trọng của quản gia Rurasu, sự lạnh lùng của Kara và điệu cười điên cuồng của Hắc tướng quân đều được thể hiện; "Mukiha Ken-ryu" được chuyển đổi chính xác thành "Mukiha Ken-ryu"; [Tên đầy đủ của nhân vật chính] và các phần giữ chỗ khác ở đúng vị trí.
- **Không nhất quán**, tất cả là do danh sách dự thi lúc đó chỉ có 73 hạt giống:
- アースゲイン Có ba cách dịch Earth Gein/Ax Gein/As Gein;
- スイームルグ được dịch là Siimlug, và danh sách đầu vào là Swailug;
- ムゲゾルバドス xuất hiện dưới hai cách viết: Mugai/Muge;
- おじい様 đôi khi được dịch là ông nội và đôi khi là ông nội trong cùng một câu.
- **flash and pro**: pro có cách diễn đạt hơi ngắn gọn và nhất quán trong tiêu đề; flash có nghĩa đen hơn một chút. Không phải là một sự dịch sai rõ ràng.
- **Dấu chấm cuối câu**: Khi không có "." cuối trang tiếng Nhật chắc bản dịch sẽ không thêm vào nhưng cũng không hoàn toàn nhất quán. Điều này đòi hỏi một quy tắc thống nhất (xem Phần 8).

## 5. Kết quả đầy đủ (23-09-2026)

| | Tiếng Trung (`zh-v1`) | Tiếng Anh (`en-v1`) |
| --- | ---: | ---: |
| Số mục (truyện 33,628 + trận chiến 11,548 + mở đầu 30) | 45.206 | 45.206 |
| Đã vượt qua kiểm tra cơ khí sau bản phác thảo đầu tiên | 45.110 | 44.962 |
| Đạt sau ba lần thử lại | **45.197** | **45,139** |
| Mã thông báo đầu vào/đầu ra cho bản nháp đầu tiên và thử lại | 6,42M / 1,28M | 7,60M / 1,48M |
| Chi phí dựa trên giá flash (thời gian bận/thời gian rảnh) | 22,1/11,0 nhân dân tệ | 24,0/12,0 nhân dân tệ |
| Người đánh giá: Đã đánh giá / Sửa đổi | 45.127 / 2.114 | 45.139 / 1.931 |
| Đánh giá token (pro) | 5,00M / 0,72M | 5,18M / 0,95M |

- **Bản thảo đầu tiên**: Hai ngôn ngữ được chạy cùng lúc, mỗi ngôn ngữ 6 tuyến song song, mỗi ngôn ngữ khoảng 1 giờ. Cả hai ngôn ngữ đều gặp sự cố "Hai đối tượng JSON được trả lời" một lần trong hơn 20 lô đầu tiên và trình phân tích cú pháp đã được thay đổi để hợp nhất nhiều đối tượng.
- **Chặn đánh giá nội dung**: Một loạt tệp tiếng Trung đã bị từ chối bởi quá trình xem xét đầu vào của Bailian (`data_inspection_failed`) và cùng một loạt tệp tiếng Anh đã được thông qua. `retry` Khi gặp tình huống này, trước tiên hãy loại bỏ ngữ cảnh, sau đó chia thành các câu đơn và cuối cùng là dịch riêng đợt này.
- **Trình giữ chỗ tiếng Anh**: Trình giữ chỗ trong bản nháp đầu tiên bằng tiếng Anh ban đầu sử dụng nhãn tiếng Trung và mô hình sẽ "dịch" [Tên đối tác] thành [Tên đối tác], chiếm 118 lỗi. Hãy thử lại sau khi sử dụng phần giữ chỗ ASCII như `{PartnerName}` và loại lỗi này về cơ bản sẽ biến mất.
- **Điều chỉnh dành cho thanh tra**:
- Tỷ lệ độ dài được thay đổi để tính toán dựa trên cả dòng và ký tự tiếng Nhật được tính theo loại ký tự (katakana được tính là một nửa, âm thanh dài và kana viết thường không được tính), nếu không các động tác hét lên như ライトニングソォォォォード→Lightning Sword sẽ bị báo sai;
- Đã thêm kiểm tra kính trọng tiếng Nhật (`-sama`, `-san`) bằng tiếng Anh.
- **Còn lại không thành công**: 9 mục tiếng Trung và 67 mục tiếng Anh, chủ yếu là do hợp nhất trang và thiếu `{HeroMech}`. Các mục này được viết dưới dạng mẫu để dịch sang cả hai ngôn ngữ trong tệp dòng, có kèm theo ghi chú nháp.
- **Đánh giá**:
- Ban đầu, mô hình đánh giá được trả về bằng cách sử dụng trường `tr`, trường này thường sao chép bản nháp đầu tiên. Sau khi thay đổi thành trường `revised` riêng biệt và yêu cầu trường này khác với bản nháp đầu tiên, những thay đổi đã thực sự được triển khai.
- Những thay đổi chính bao gồm: dịch sai (gọi せんのか), cách diễn đạt tiếng Nhật (发jin→khởi hành), đại từ và người xưng hô, さん→Mr., và thiếu dấu ngoặc kép.
- Người phản biện sẽ thêm dấu chấm vào văn bản tiếng Trung, điều này mâu thuẫn với quy tắc “dấu câu cuối trang theo nguyên văn” (xem Phần 8).
- 2-3 đợt, mỗi đợt 2 lần thất bại do bị cắt bớt phản hồi, và các đợt này giữ lại bản thảo đầu tiên.
- **Dấu câu cuối trang (2026-09-24, `zh-v1-joins`)**: Sau khi game đổi thành cả bộ, máy thực tế phát hiện ra tiếng Trung khi lật trang gốc thường thiếu dấu câu, hai câu trước và sau bị dính vào nhau. Nguyên nhân là do quy định v4 “Dấu câu cuối trang theo nguyên văn”: Các trang tiếng Nhật thường không có dấu chấm ở cuối.
- Tỷ lệ: Khoảng 5.200 trong số 13.358 trang tiếng Trung không có dấu câu, gồm 4.347 mục. Tiếng Anh không cần phải được xử lý: 304 vị trí mà trang kết thúc bằng một chữ cái và trang tiếp theo bắt đầu bằng chữ in hoa hầu hết đều là tên riêng.
- Cách thực hiện: `run_mt.py joins` Cho `deepseek-v4-pro-0813` đọc qua toàn bộ đoạn văn tiếng Trung được nối (có kèm theo văn bản gốc tiếng Nhật) để điền dấu câu. Chương trình so sánh các từ từng từ, chỉ giữ lại các dấu câu (.,!?, v.v.) được chèn chính xác tại các lượt trang này, loại bỏ tất cả các thay đổi khác và giữ nguyên các dấu câu hiện có; 39 câu trả lời bị bỏ lỡ đã được đặt lại câu hỏi bằng `--missing`.
- Kết quả: Đã thay đổi 401 mục, thêm 477 dấu chấm, 6 dấu phẩy, 6 dấu chấm hỏi; 4.700 mục còn lại được đánh giá là những câu kéo dài xuyên suốt các trang (chẳng hạn như “Sư phụ sẽ khóc dưới Cửu Xuân |”) và không được thêm vào. Nhập 0,47M, xuất 0,16M mã thông báo.
- Dấu câu kết thúc trang cuối (`zh-v1-final`, `zh-v1-final2`, `joins --final`): Có 3.057 (9%) dòng hội thoại cốt truyện không có dấu câu cuối câu trước dấu ngoặc kép đóng. 91% còn lại đã có sẵn nên đều được thêm vào. Chỉ được phép trước dấu ngoặc kép hoặc dấu ngoặc đơn đóng. ! ? ..., mô hình di chuyển dấu chấm vào dấu ngoặc kép khi đặt chúng bên ngoài dấu ngoặc kép.
- Kết quả: Đã thêm 2.967 mặt hàng; Còn lại 59 mục và mô hình xác định rằng không cần thêm chúng.
- Vòng 1 bỏ sót khoảng 400 mục do mẫu ghi dấu chấm ngoài dấu ngoặc kép và chương trình không nhận diện. Sau khi thay đổi để chấp nhận cách viết này, nó đã được làm lại ở vòng thứ hai.
- Dấu chấm than và dấu chấm hỏi nửa độ rộng: Có 74 chỗ trong tiếng Trung sử dụng nửa độ rộng ! ? của văn bản gốc tiếng Nhật. Khi viết dòng, hãy thay đổi chúng thành chiều rộng đầy đủ! ? ; Dấu chấm ngay sau dấu chấm lửng ("...", 171 vị trí, hầu hết được sao chép từ tiếng Nhật trong bản nháp đầu tiên) cũng bị xóa khi viết (`chinese_marks`).
- Hai phương pháp đã bị loại bỏ trong quá trình chạy thử: một phương pháp là để mô hình trực tiếp đưa ra dấu câu đầy đủ ở cuối mỗi trang, dẫn đến việc xóa dấu "!?" đúng ban đầu.
- **Chuẩn hóa trước khi viết**:
- Khi văn bản gốc là một cặp dấu "..." hoặc (...) kéo dài khắp các trang thì nên thống nhất thành dấu ngoặc kép mở ở trang đầu và dấu ngoặc kép đóng ở trang cuối. Bước này khắc phục lỗi thiếu dấu ngoặc kép trong mô hình hoặc thêm một cặp dấu ngoặc kép trên mỗi trang: số mục tiếng Anh không tương thích giảm từ 888 xuống 47, còn lại là trường hợp có nhiều cặp dấu ngoặc kép trong một câu và không có thay đổi nào được thực hiện.
- Kết quả đợt ban đầu không thay đổi.

## 6. Sân khấu

| Sân khấu | Nội dung | Trạng thái (2026-09-23) |
| --- | --- | --- |
| Xuất P0 | Phần 1 của bài viết này | Đã hoàn thành |
| P1 Tên và tên riêng | Hai bộ danh sách nhập cảnh bằng tiếng Trung và tiếng Anh (một cuộc trò chuyện khác); 647 ứng cử viên cho tên riêng của các dòng. Sau khi soạn thảo bằng tiếng Trung và tiếng Anh, Claude đã kiểm tra và sửa chữa 37 mục, dán nhãn lại 12 đoạn bị cắt cụt và 1 từ thông dụng, cuối cùng có 269 tên riêng; kiểm tra tính nhất quán với danh sách đầu vào | Hoàn thành; 24-09-2026 Bản thảo cuối cùng sẽ được kiểm tra cùng với bản dịch chính thức (xem "Bản dịch chính thức của danh từ riêng"). Phương pháp viết cuối cùng sẽ là `renames.json`. `status: draft` trong `story-terms.json` chưa được lấp đầy |
| P2 bản thảo đầu tiên | 45.206 mục bằng tiếng Trung và tiếng Anh, bao gồm cả lần thử lại | Đã hoàn thành, tỷ lệ đỗ 99,98% (tiếng Trung) / 99,85% (tiếng Anh) |
| Đánh giá P3 | Một vòng đánh giá AI đã được hoàn thành. Có thể thực hiện xem xét thủ công trong phần so sánh "Dịch" trên trang xem lại cốt truyện: `tools/translation/export_review.py` tạo dữ liệu, nguồn của từng dấu câu (mục nhập, chữ viết tay, dịch máy, đánh giá, không thành công), lý do xem xét và câu hỏi dịch máy được hiển thị trong lời nhắc di chuột | Đánh giá AI đã hoàn tất; xem xét thủ công chưa bắt đầu |
| P4 được viết dưới dạng tệp dòng | `write_dialogue.py --runs zh-Hans=zh-v1,zh-v1-review,zh-v1-joins,zh-v1-final,zh-v1-final2,zh-v1-names,zh-v1-fixes,zh-v1-names2 --runs en=en-v1,en-v1-review,en-v1-fixes` Viết `content/dialogue/<locale>/`: cốt truyện dựa trên cảnh và lời thoại chiến đấu dựa trên giọng nói, mỗi người một tệp (`battle/speaker-NNN.txt`, NNN là số ký tự có giọng nói; đầu tiên là các phân đoạn chung của chín tình huống, sau đó là các dòng điều kiện theo thứ tự của bảng, mỗi dòng có chú thích `# 触发：`; 27-09-2026 (bắt đầu), 39 câu không có bảng trích dẫn nằm trong `battle/other.txt` và có `battle/special.txt` (thuyền trưởng hàng đầu) và `intro.txt`. Chỉ viết lại các tệp có thẻ thế hệ; hãy sử dụng `dialogue_text.load` để xác minh rằng hai ngôn ngữ không có lỗi và có cùng một bộ khóa trước khi viết ra | Đã hoàn thành, chưa gửi |
| Truy cập màn hình P5 | Cốt truyện và lời thoại chiến đấu (`27b221e`) đã được truy cập và đã được xác minh vào ngày 23-09-2026. F7 chuyển đổi tiếng Trung/Anh/Nhật; lời mở đầu, thẻ tiêu đề chương, trang kết thúc truy cập 2026-09-24 (bản vẽ gốc, không còn ảnh gốc); cửa sổ lựa chọn chi, cửa sổ mục đích chiến đấu không được truy cập | Đang tiến hành (phiên khác) |
| P6 nghiệm thu máy thực tế | Tập đầu tiên trong bốn tuyến đường, một số tập khác nhau, lấy mẫu đường chiến đấu, lưu trữ và tải | Chưa bắt đầu |

Trong tương lai, nếu danh sách từ vựng, từ gợi ý hoặc tên riêng được xác định theo cách thủ công, bạn chỉ cần chạy lại những phần bị ảnh hưởng. Cả `run_mt.py` và `write_dialogue.py` đều hỗ trợ tiếp tục và tái tạo tổng thể, đồng thời các tệp lớp phủ do người chơi đặt trong thư mục người dùng sẽ không bị ảnh hưởng.

## Phiên bản tiếng Anh

Ngôn ngữ tiếng Trung và tiếng Anh chia sẻ cùng một bộ quy trình xuất, phân lô, bảo vệ giữ chỗ, kiểm tra và hợp nhất. Chỉ có quy tắc ngôn ngữ và nguồn từ vựng của từ gợi ý là khác nhau. Tiếng Anh được dịch trực tiếp từ tiếng Nhật mà không cần dịch sang tiếng Trung để tránh chồng lỗi 2 lần.

- **Từ vựng**:
- Tên xuất phát từ phiên bản tiếng Anh của danh sách dự thi (`content/locales/terms/en.json`, được hoàn thiện cùng đợt với phiên bản tiếng Trung);
- Tên riêng của dòng lấy từ trường `en` của `content/translation/story-terms.json`;
- Từ vựng tham khảo tiếng Trung của "Mech Z" không được sử dụng bằng tiếng Anh.
- **Thẻ nhân vật**: Tên tiếng Anh được lấy từ danh sách tham gia. Mô tả giới tính và danh tính của nhân vật gốc, giới tính trong sách minh họa "Mech Z", tác phẩm và phần giới thiệu (tiếng Trung) đều bằng hai ngôn ngữ và người mẫu có thể hiểu được.
- **Giải thích về thế giới quan**: Tất cả tên riêng trong các từ gợi ý phải được viết bằng tên gốc tiếng Nhật (ムゲゾルバドスEmpire, v.v.), không phải bằng tiếng Trung, để tránh bản dịch tiếng Trung thấm sang tiếng Anh.
- **Viết**: Theo thông lệ của 153 bản thảo tiếng Anh hiện có, đoạn hội thoại được gói trong dấu ngoặc kép xoăn " ", お嬢様 = "my lady". Xem Phần 7 để biết thêm các quy định.
- **KIỂM TRA**: Kiểm tra được thực hiện bằng cả hai ngôn ngữ dành cho số trang, phần giữ chỗ, kana dư và toàn bộ cặp trích dẫn. Trong tiếng Anh, hãy kiểm tra thêm các mục sau, bất kỳ mục nào trong số chúng sẽ được cấp lại:
- Chữ Hán còn lại;
- Dấu câu có độ rộng đầy đủ;
- dấu ngoặc kép trực tiếp;
- Kính ngữ được La Mã hóa, chẳng hạn như `-sama`, `-san`. "Banjo-sama" xuất hiện một lần trong quá trình chạy thử nghiệm nên vật phẩm này đã được thêm vào.
  
Ngưỡng tỷ lệ độ dài cho tiếng Anh được nới lỏng ở mức 0,6–8.
- **Phủ sóng bằng hai ngôn ngữ**: Cả hai ngôn ngữ sẽ được hoàn thiện nhiều nhất có thể; nếu có những mục chỉ vượt qua vòng kiểm tra bằng một ngôn ngữ thì ngôn ngữ kia sẽ quay lại tiếng Nhật. Các dòng không được nhập vào thư mục ngôn ngữ nên không bị ràng buộc bởi `tests/test_english_locale.py` "Bộ phím tiếng Trung và tiếng Anh phải giống nhau".

Bài kiểm tra tiếng Anh (cùng phạm vi với tiếng Trung, 484 mặt hàng) đều vượt qua kiểm tra ở vòng đầu tiên và vòng chỉnh sửa chỉ được sử dụng một lần. Đánh giá thủ công:

- Câu thoại của コウ ngắn gọn và tự nhiên, chẳng hạn như “Tại sao bạn—!!” và “Lấy cái này!!”;
- Kính ngữ ローレンス tương ứng với "Thưa cô... Tôi sẽ mang nó cho cô ở đâu?";
- Kỹ năng kết hợp "Final Dynamic Special!!" giữ lại tên của di chuyển.

## Tên dòng

Không có tên riêng nào được ghi trong vùng dữ liệu, chẳng hạn như các tổ chức (ロームフェラ财団, カラバ, Mặt trận Giải phóng Trái đất), Tên địa danh (ジャブロー, サンクキングダム) và tàu thuyền (ブライトship) được xử lý bằng ba tập lệnh:

1. `term_candidates.py` Tìm ứng viên từ các dòng: katakana và các từ có hậu tố như empire/finance/base/team/stream, tổng cộng có 647 từ;
2. `draft_terms.py` sẽ được giao cho `deepseek-v4-pro-0813` phân chia từng ứng viên thành tên riêng, từ thông dụng hoặc đoạn cắt ngắn, đồng thời soạn thảo bản dịch tiếng Trung và tiếng Anh. Thí sinh đầu tiên được sắp xếp bằng tiếng Nhật sao cho các từ liên quan được sắp xếp lại với nhau; các bản dịch liên quan được xác định trước đó sẽ được chuyển sang các đợt tiếp theo dưới dạng ràng buộc;
3. `audit_terms.py` So sánh tên riêng của từng dòng với tất cả các mục có chứa nó trong danh sách mục (bao gồm các câu như điều kiện chiến thắng hay thất bại), bằng cả tiếng Trung và tiếng Anh.

Kết quả cho ngày 23-09-2026:

- Kết quả soạn thảo: 282 tên riêng, 337 từ thông dụng, 28 đoạn, sử dụng 98.000 mã đầu vào và 35.000 mã đầu ra.
- Review thủ công (Claude) đã sửa 37 mục và đánh dấu 4 mục còn lại là đoạn:
- Bản thảo đầu tiên của "ムゲゾルバドスEmpire" đã bỏ sót "ムゲ" và đổi thành Đế chế Muge Zolbados/Đế chế Muge Zolbados;
- Gemma bị nhầm là tên một quốc gia, nhưng thực ra là một nhân vật trong ZGundam;
- Danh sách hơn 20 mục được căn chỉnh bao gồm ザンボット, ランタオ岛 (Đảo Lantau), v.v.;
- Tên tiếng Anh của tàu ブライト và các tàu khác được đổi thành "Tàu của Bright".
- Có 4 nhóm từ đồng nghĩa trong bảng nhập đã được thống nhất bởi hội thoại bảng nhập: ムゲ=Moog, ジオン=Zion, バイストンウェル=Beston Will, ミネルバ=Minerva (đã gửi `c62a01f`).
- 18 mục còn lại trong kiểm tra đều là các chuỗi con vô tình va chạm với các từ không liên quan, chẳng hạn như ライフ va chạm với ライフル, ブライ va chạm với ウェイブライダー.
- Sau này tôi phát hiện ra rằng quy tắc hậu tố cắt ○○Thuyền trưởng/○○Thuyền trưởng thành ○○ship/○○Đội: 188 người trong tàu ブライト thực chất là Thuyền trưởng ブライト. 8 mục này đã được dán nhãn lại thành các mảnh vỡ và các quy tắc đã được sửa đổi (tàu, đội, quân không được tuân theo bởi người chỉ huy, thành viên, người, v.v.). Bản thảo đầu tiên bằng tiếng Anh không sử dụng sai “con tàu của Bright”; "Thuyền trưởng Bright" của Trung Quốc ban đầu bao gồm "con tàu của Bright" và không bị ảnh hưởng. Hiện tại có 269 tên riêng.

Trạng thái tên thích hợp đều là `draft`; thay đổi mục nhập thành `approved` hoặc `rejected` theo cách thủ công rồi chạy lại cảnh bị ảnh hưởng.

## Bản dịch chính thức của danh từ riêng (24/09/2026)

Người dùng yêu cầu "cố gắng tìm một người dịch chính thức, sắp xếp các danh từ thích hợp như tên, máy bay, vũ khí, v.v. và đánh bóng chúng."

**Phạm vi**: ~1.900 tên, được phân bổ như sau:
- `units`, `weapons`, `pilots`, `pilot_full_names`, `character_list`, `series`, `default_names` của bảng nhập;
- 269 tên dòng trong `content/translation/story-terms.json`.

**Phương pháp**: Chia các tác phẩm thành 7 nhóm, sử dụng các nhiệm vụ con để tìm kiếm nguồn song song.
- Dòng sản phẩm Gundam: Trang web tiếng Trung và tiếng Anh giản thể chính thức của GUNDAM.INFO, trang web tiếng Trung Bandai Model, G Century.
- Super Series: Phiên bản tiếng Trung giản thể và tiếng Anh chính thức của Mecha 30/Y, phiên bản tiếng Trung phồn thể của Mecha DD, phiên bản chính thức từ Station B và Discotek.
- 64 Nguyên bản: Chữ viết bằng tiếng nước ngoài của thẻ chính thức "スクランブルギャザー" năm 2001 (theo srw.wiki), và chữ viết của cộng đồng.
- Mỗi tên được cung cấp nguồn gốc và mức độ tin cậy: Chính thức, Đạt, Đánh bóng, Bảo lưu.
- Khoảng 300 tác phẩm bị phân loại sai đã được chuyển cho đoàn tương ứng để kiểm tra lại.

**Lựa chọn (do người dùng xác định)**: Ưu tiên tên tiếng Trung thường dùng và tên tiếng Anh chính thức được ưu tiên. Chi tiết:
- Bản dịch hiện tại là tên phổ biến ở Trung Quốc đại lục, được giữ lại, ngay cả khi tiếng Trung giản thể chính thức khác, như Camus Bidan, Hero Wei, Zaku, Dongfang Bubai;
- Nếu bản dịch hiện tại không có nguồn thì đổi sang tên thông dụng;
- Nếu không có tên phổ biến thì sử dụng cách chính thống.

**Kết quả**: 625 mục đã được thay đổi, bao gồm 483 bằng tiếng Trung và 220 bằng tiếng Anh; 30 mục còn lại là danh hiệu cấp độ và điều kiện chiến thắng và thất bại được đồng bộ hóa với việc thay đổi tên. Bảng mục nhập đã được ghi (`9477893`) bởi phiên duy trì nó, 14 trong số đó đang chờ xử lý (xem bên dưới).
- Trang so sánh: https://claude.ai/artifact/6uGNTsTAydmzZsnAJW4BQz
- Dữ liệu: `assets/translation-runs/official-names/` (gốc), trong đó mỗi nhóm có `final-*.json` và kết quả tổng hợp là `term-changes.json`.
- Bảng nhập được viết sau khi xem xét bởi phiên duy trì nó.

**Các dòng sẽ được thay đổi tương ứng**:
- `content/translation/renames.json`: 521 lần đổi tên, được `run_mt.final_target` áp dụng khi viết dòng.
- Tên tiếng Trung trong vòng hai ký tự, tên tiếng Anh trong vòng năm chữ cái (Burn, Todd, Cham, v.v.), phát âm tiếng Anh (Swooord) và tên cũ vẫn là tên hiện tại của các mục khác (Rosamia Vẫn là một ロザミア, pháo nổi vẫn là một ファンネル), chỉ thay thế các dòng chứa tên trong văn bản gốc tiếng Nhật; khi so sánh, hãy xóa dòng mới, dấu cách, "・" và "=" và viết riêng (シャーリー) khi so sánh. Nếu tên dài hơn đủ độc đáo thì toàn bộ văn bản sẽ được thay thế;
- Tên dài cửa không mở không chặn được tên ngắn bên trong (“Duke Delmayo” vẫn được thay bằng “Duke Delmayo” trong câu chỉ nói “Duke Delmayo”);
- Tên dòng chỉ là các đoạn tên (コン・バトラー thiếu V, nửa sau của cuộc gọi và メールシュトローム thiếu "chiến đấu") sẽ không được thay thế trên toàn cầu;
- Tên nguyên, khớp dài nhất: tên dài hơn đã biết sẽ được bảo vệ và sẽ không bị thay thế dưới dạng chuỗi con;
- Trận đấu tiếng Anh theo toàn bộ từ;
- Tên giữ chỗ không di chuyển.
- Tên viết tắt một ký tự (Xiu → Xiang, Zun → Wu, Fo → Feng, Fa → Hua) không thể thay thế bằng từ:
- Sử dụng `run_mt.py names` để đánh số cho từng từ trong dòng sao cho mô hình chỉ chọn ra số chỉ người này và chương trình sẽ thay thế tương ứng;
- Những cái tên dài hơn đã biết (chẳng hạn như Soltifa) được che trước và không tham gia đánh số;
- Tổng cộng có 472 dòng được thay đổi và kết quả là `zh-v1-names`.
- Tổng cộng có 4.342 dòng tiếng Trung và 1.702 dòng tiếng Anh đã được cập nhật tương ứng (tên người nói trong phần bình luận bài dự thi cũng thay đổi theo danh sách dự thi). Một phiên khác kiểm tra những cái tên còn lại theo tên cũ, cuối cùng chỉ còn lại 3 chỗ đã được xử lý: chữ viết khác của シャーリー; hai chỗ trong bản nháp đầu tiên đã nhầm マーズ là "mag" và sửa lô `zh-v1-fixes` thành "mas" theo cách thủ công; một địa điểm trong tiếng Anh được gọi là ロザミィ`en-v1-fixes` đổi thành Rosamy.
- Những tiếng hét dài (Eiji~~, Lightning Sword——) sẽ không bị thay thế trên toàn cầu.

**Chỉ tiếng Trung giản thể (kiểm tra lại)**: Sau đó, người dùng đã yêu cầu "Không có bản dịch tiếng Đài Loan, mà là tiếng Trung giản thể".
- Chỉ dựa trên các nguồn đại lục được công nhận: Baidu, Mengniang, wiki trạm B, mecha, trạm mecha đại lục, GUNDAM.INFO Tiếng Trung giản thể;
- Không tính quan chức phồn thể, phiên bản Đài Loan, phiên bản Hồng Kông, cách viết chỉ thấy trên Wiki tiếng Trung, cũng như không tính những cách viết từ bản dịch tiếng Đài Loan trên Bách khoa toàn thư Baidu;
- Kiểm tra lại 146 mục theo "Truy cập đại lục → Tiếng Trung giản thể chính thức → Giữ bản dịch cũ hoặc phiên âm".

**Xác nhận của người dùng**: Nhấp vào từng cái một trên trang xác nhận bản dịch (https://claude.ai/artifact/X2N7dwfbXZb6fMUSnFjmtA).
- 640 cách viết kết hợp thành 396 tên. Cách viết cùng một tên trong mỗi khu vực, cũng như vũ khí, mẫu mã, tên đầy đủ, danh hiệu cấp độ và các điều kiện chiến thắng hoặc thất bại có chứa tên này đều tuân theo cùng một lựa chọn.
- Toàn bộ 100 tên đã được quyết định: 43 tên thay đổi và 57 tên giữ nguyên; những người còn lại sẽ giữ tên hiện tại của họ.
- Các tên đồng âm trong bản tiếng Đài Loan không được sử dụng, giữ nguyên phiên âm: Boqiong, Miuji, Dozdozi, Jinjin.
- Hãy gọi cho VSBR.
- “Vua Sấm” chỉ được dùng trong tên tác phẩm và tên máy. Nó không khớp với tên của người đó: Magu, Rose.
- アラン giữ lại Alan, アキラ đổi thành Hui, và ケンジ đổi thành Kenji.
- Kirara・スーン Trở lại Kira Mori, phù hợp với tên viết tắt Kira.
- ビューティ Tên viết tắt được giữ nguyên Biyoti, tên đầy đủ được đổi thành Tachibana Meili.
- Danh sách dự thi: Viết `9638799`, và hai mục sau của キャラ・スーン.
- Dòng: `deferred` trong tổng số `renames.json` đã bị xóa; Ming→Hui đã thay đổi 8 dòng từ `run_mt.py names` và kết quả là `zh-v1-names2`.
- Tập lệnh đọc lựa chọn trang sau `finalize.py` và dữ liệu trong `assets/translation-runs/official-names/`.

Bản dịch tiếng Anh của những người phản đối ban đầu là Kurtz Forneus, Rish Griswell và Ehrlich Stasen, vì cách viết chính tả của cộng đồng là phát âm sai.

**So sánh tiếng Anh Akurasu (2026-09-24)**: Người dùng yêu cầu tham khảo trang SRW64 của Akurasu và đưa cho Claude đánh giá.
- Đã thu thập 58 trang và thu được 809 bộ so sánh tiếng Nhật và tiếng Anh. So với tiếng Anh của chúng tôi, có khoảng 600 bộ giống hệt nhau.
- Ngoài ra, so sánh từng bước cách viết trong phiên bản tiếng Anh chính thức của Aircraft War 30/T/V/X/DD. Để biết trang so sánh, hãy xem https://claude.ai/artifact/6uHNPqtvUM5M6gvHUy2PVB.
- Lệnh tinh thần: Trang SRW64 của Akurasu là sự kết hợp giữa những tên người chơi đầu tiên (Sure-Hit, Guts, Awaken) và một nhóm tên cũ khác (Strike, Alert, Luck, Tyre). Chúng tôi sử dụng tên chính thức là T/30, được bảo lưu.
- Tên cá nhân và tên máy: Cách viết khác nhau của Akurasu hầu hết là ký tự La Mã có âm dài, hoặc chúng tôi đã thay đổi theo cách viết chính thức nên sẽ giữ nguyên.
- Tiêu đề cấp độ: Akurasu là bản dịch theo nghĩa đen, hãy giữ nguyên tên của chúng tôi.
- Chỉ có 4 vật phẩm được thay đổi: アフロダイA Aphrodite A, ダイアナンA Diana A, ダイアナンミサイル Diana Missile, レーダー High-Fidelity Radar (T/X chính thức) hiệu suất cao.
- Dữ liệu và tập lệnh có trong `assets/translation-runs/official-names/akurasu/`.

## Chất đánh bóng kiểm soát tham khảo: Serenes Forest English LP (26-09-2026)

Người dùng tìm thấy bản dịch tiếng Anh của con người: Diễn đàn Serenes Forest Balcerzak's Let's Play (https://forums.serenesforest.net/topic/104832-super-robot-wars-64/, 2024-07 đến 2026-04, 56 tập, một tập của lộ trình Manami, toàn bộ cốt truyện được viết thành khối gấp theo "Loa: Lines"). Người dùng quyết định **chỉ tham khảo và không sao chép**: chụp lại để so sánh và kiểm tra phiên bản tiếng Trung để tìm các vấn đề phát hiện bằng tiếng Anh.

- **Tìm nạp**: Trang web chặn cuộn tròn, sử dụng trình duyệt tích hợp để mở rộng khối đã gấp và lưu dưới dạng `assets/translation-runs/reference-en/raw/chNN.txt` (không cần nhập git), đồng thời lọc ra các báo cáo trận chiến và bảng dữ liệu. Các tập 1–5 hiện đã được lưu.
- **Căn chỉnh**: `tools/translation/align_reference.py` Theo lộ trình, cố gắng căn chỉnh và tìm từng cảnh một (cách viết tiêu đề rất khác nhau nên hãy chọn dựa trên số lần căn chỉnh). Ở cấp độ dòng, sử dụng loa + từ trùng lặp giữa hai ngôn ngữ tiếng Anh để làm Needleman-Wunsch. Tự động tìm hiểu bí danh của người nói (Brai Đại đế=Hoàng đế Burai), viết `reference-en/aligned/scene-NNNN.jsonl`. Các tập 1–5 khớp với 82–91% số dòng tham chiếu (366 dòng).
- **So sánh**: `tools/translation/polish_reference.py` Hiển thị ja/en/zh/ref thành `deepseek-v4-pro-0813`, chỉ thay đổi khi ý nghĩa, thiếu bản dịch, tham chiếu và âm điệu rõ ràng không nhất quán. Thay đổi lô được viết bằng stage=polish (`en-<tag>`, `zh-<tag>`), có thể được xếp chồng lên nhau trong các lần chạy write_dialogue Phía sau; `--report` hiển thị bảng trước và sau khi thay đổi.
- **Kết quả thí điểm (thẻ `ref-pilot`, cảnh 1/4/5/6/7)**: Trong số 366 hàng, mô hình chỉ cho rằng 9 hàng có vấn đề. Sau khi kiểm tra cơ học, tiếng Anh đổi thành 1 và tiếng Trung đổi thành 4; kiểm tra thủ công 5 hàng sau: 17916 Việc điền các vị từ bị bỏ qua là một cải tiến thực sự; Mô hình 17831 (paw no vảy を chiên じ て uống む = "học hỏi từ người khác") có vấn đề với phiên bản tiếng Trung, nhưng bản dịch theo nghĩa đen là "nước sắc vảy móng tay" không thể sử dụng được và **thiếu bản dịch nghĩa đen tiếng Anh** (do người dùng chỉ ra); 17958 đổi "she" thành "he" là một sự cải tiến; 17497 Bản sửa đổi tiếng Anh không nằm trong văn bản.
- Chính Claude đã đọc từng dòng 130 của Chương 1 và 4: Bản dịch của chúng tôi không mắc lỗi về ý nghĩa, nhưng các tham chiếu sai ở năm hoặc sáu chỗ ("bạn có mang theo Búp bê không", "hơn một nửa nhân viên kỹ thuật", Jia'er "ông nội được gọi đi", Giáo sư Gong "những người cần được bảo vệ", v.v.). Tôi cũng tìm thấy hai vấn đề không được tiết lộ trong tài liệu tham khảo, cả trong cảnh viết tay-0001 (quay lại cuộc trò chuyện trong bảng mục nhập): 17497 "Western Federal/Western Federal" (văn bản gốc "Old Federal") bị thiếu cả tiếng Trung và tiếng Anh, 17461 "后は頼む" bị thiếu trong tiếng Trung.
- Kết luận: **Bản dịch máy đã đạt đến mức độ tương đương với tài liệu tham khảo này về mặt ý nghĩa. Hiệu suất so sánh ý nghĩa theo từng dòng rất thấp** và việc thu hồi so sánh DeepSeek cũng không đáng tin cậy; sự khác biệt chủ yếu nằm ở giọng điệu của các nhân vật (trong tài liệu tham khảo, giọng quý phái của Manami và giọng quản gia của Lawrence khác biệt hơn, trong khi giọng của chúng ta trung tính hơn).
- Kiểm tra tại chỗ thành ngữ: Sử dụng hơn 100 thành ngữ thông dụng để quét thư viện chữ viết và đánh 17 (ngoại trừ các từ thông dụng như vỡ dầu và gốc hơi thở), đồng thời kiểm tra từng bản dịch tiếng Trung và tiếng Anh; 17831 Đây là một trường hợp cá biệt, nguyên nhân có lẽ là do thành ngữ bị cắt ở giữa khi lật trang ("paw no dirty でも｜せんじて Drink ませて"). 17831 đã được ghi vào manual.json của `en-v1-fixes`/`zh-v1-fixes` và đã tạo lại tệp dòng.

## 7. Thông số dịch thuật (được nêu rõ trong phần nhắc)

- Giọng điệu trung thực, tự nhiên, thông tục, phù hợp với tính cách, giọng điệu của nhân vật; không thêm hoặc xóa thông tin, hoặc thêm bình luận.
- Số trang phù hợp với văn bản gốc, không có ngắt dòng trong trang; dấu ngoặc kép theo sau trang đầu và trang cuối của văn bản gốc.
- Các phần giữ chỗ như [Tên nhân vật chính] được giữ nguyên, số lượng và thứ tự không thay đổi; hầu hết さん và くん sau tên đều bị lược bỏ.
- Dấu câu:
- "" được đổi thành "", "" được đổi thành '';
- () độc thoại nội tâm vẫn giữ nguyên dấu ngoặc nhọn;
- Sử dụng... cho dấu chấm lửng, và -- cho dấu gạch ngang;
- ! ? Sử dụng toàn bộ chiều rộng; sử dụng nửa chiều rộng cho số; sử dụng dấu cách · cho tên nước ngoài.
- Chức danh và quân hàm: Thiếu úy/Trung úy/Đại úy = Thiếu úy/Trung úy/Đại úy, Thiếu tá/Trung tá/Đại tá = Thiếu tá/Trung tá/Đại tá, Đại úy = Đại úy, お嬢様 = Cô, Thưa ngài, Bệ hạ = Thưa ngài, Thầy = Thầy.
- Giữ được thói quen nói lắp, nói lắp, phát âm, kính ngữ; duy trì đà khi hô tên nước đi.
- Danh sách từ vựng: Các mục “must-use” phải được sử dụng như bình thường; những tên riêng nằm ngoài danh sách từ vựng, các tác phẩm như Gunma, v.v., sử dụng những tên được dịch phổ biến ở Trung Quốc đại lục. Không có phiên âm của các tên thường được dịch ở Trung Quốc đại lục và tên bản dịch mới phải được viết bằng `flag`.
- Chung cho cả hai ngôn ngữ: thêm chủ ngữ hoặc đại từ khi cần thiết, dựa trên giới tính của người nói, đối tác đàm thoại, ngữ cảnh và thẻ vai trò; khi không thể xác định được tham chiếu, hãy sử dụng tên hoặc thuật ngữ trung lập và đánh dấu "tham chiếu không xác định". Trò chơi nối các trang của một dòng thành một đoạn để hiển thị (xem [Bố cục hội thoại](dialogue-typesetting.md)), do đó, cần có dấu câu khi cuối trang nằm ở ranh giới của một câu hoặc mệnh đề, chứ không phải khi câu tiếp tục xuyên suốt các trang (các từ gợi ý bắt đầu từ v5; quy tắc của v4 là "dấu câu ở cuối trang tuân theo văn bản gốc").

Tiếng Anh:

- Có thể sử dụng ngôn ngữ nói tự nhiên, dạng viết tắt; tên theo thứ tự phương Tây trong danh sách đầu vào.
- Loại bỏ -san／-kun／-chan; các chức danh dùng làm lời chào được dịch sang tiếng Anh: お嬢様 thưa quý cô, Chủ nhân, Thưa ngài, Thuyền trưởng.
- Cấp bậc: Thiếu Úy, Thiếu Úy, Đại Úy, Thiếu Tá, Trung Tá, Đại Tá.
- Chỉ sử dụng dấu câu ASCII cộng với dấu ngoặc nhọn “ ” ‘ ’:... Viết...,! ? Viết ?!, độc thoại nội tâm với ( ).
- Tên di chuyển được viết dưới dạng Title Case theo danh sách nhập; tiếng rên rỉ và tiếng la hét được viết bằng tiếng Anh tự nhiên, chẳng hạn như Ngh!, Gah!.

## 8. Các vấn đề đã được xử lý mặc định

Được xử lý theo mặc định (có thể thay đổi, chạy lại các phần bị ảnh hưởng sau khi thay đổi):

- **Mẫu**: Sử dụng `deepseek-v4.1-flash` cho bản nháp đầu tiên, `deepseek-v4-pro-0813` cho bản chỉnh sửa và bản in lại cuối cùng.
- **Đại từ**: Thêm khi cần, đánh dấu nếu tài liệu tham khảo không rõ ràng, làm theo phương pháp của chương đặc biệt của "Mech Z".
- **Viết tiếng Anh**: Sử dụng dấu ngoặc kép cho đoạn hội thoại; tuân theo các quy ước tiếng Anh về chức danh (my lady, Master, Captain); sử dụng dấu câu tiếng Anh thông thường cho các dấu chấm ở cuối trang.
- **Lời bài hát và tên bài hát Karaoke**: Chưa dịch đợt này.

- **Dấu câu cuối trang bằng tiếng Trung** (Được xác định vào ngày 24-09-2026): Sau khi trò chơi được đổi thành cả bộ, phần cuối của trang được xác định theo cấu trúc câu và sẽ không còn theo văn bản tiếng Nhật nữa. Xem Phần 5 "Dấu chấm câu cuối trang".
- **Mở đầu và Thẻ tiêu đề chương** (Được xác định vào ngày 24-09-2026): Sử dụng văn bản gốc để sắp xếp lại theo ngôn ngữ đọc và không còn hiển thị hình ảnh gốc; trang kết thúc sẽ được xử lý tương tự.

Tên gốc của các dòng cần quyết định đã được chốt trong lần kiểm tra dịch chính thức ngày 24-09-2026 (người dùng bấm vào 100 tên để xác định lần lượt) và các dòng được viết theo `renames.json`; trường `status` của `story-terms.json` chưa được lấp đầy, điều đó không có nghĩa là trường này chưa được hoàn thiện.

## Những hạn chế đã biết

- Bối cảnh cốt truyện được đưa ra theo thứ tự script tĩnh, các đoạn tuyến và khối điều kiện không được đánh giá. Cảnh tương tự có thể liệt kê văn bản chi nhánh cho một số tuyến đường cùng một lúc.
- Bảng chọn tuyến chiến đấu đã bị đảo ngược (27-09-2026), nhưng ngữ nghĩa của cờ âm mưu 45–49 và ý nghĩa của loại bản ghi hiếu chiến `0x14` vẫn chưa được nghiên cứu chi tiết. Xem [battle-quotes.md](../data/battle-quotes.md) "Chưa nghiên cứu chi tiết".
- Việc chép lời mở đầu dựa vào việc đọc hình thủ công; sự tương ứng giữa tuyến mở đầu và nhân vật chính, ngoại trừ tuyến 2, được suy ra dựa trên nội dung.
- Văn bản trong ảnh chưa được tính ngoại trừ phần mở đầu, thẻ tiêu đề chương, trang kết thúc và menu tiêu đề.
- Kiểm tra cơ khí chỉ có thể đảm bảo đúng cấu trúc và các vấn đề về định dạng rõ ràng; chất lượng của bản dịch phụ thuộc vào việc xem xét thủ công. AI review thay đổi khoảng 4,5%, không có nghĩa là 95% còn lại đã được xác nhận.

### Cơ thể và vũ khí của nhân vật chính (xác minh vào ngày 27-09-2026)

Tên máy tiếng Anh sẽ luôn sử dụng cách viết chính thức của "Ký hiệu ngoại ngữ" của Wiki tiếng Nhật (Earthgain, Virose, Svanheld, Sigroon, Razgreez, Soldifar, Ashcleef, Sweemurg, Elbulls), thay vì Vairose/Svanhild/Razgriz/Simurgh/Elbrus thường được sử dụng trong vòng tròn tiếng Anh; Phiên âm tiếng Trung dựa trên katakana và các bản dịch thần thoại không được sử dụng. Các chiêu thức của phong cách Wujiba Fist vẫn sử dụng chữ Hán bằng tiếng Trung và chữ La Mã bằng tiếng Anh. Sự thay đổi này: シグルーン Sigrun → Sigroon; アッシャークルー Ashekru → Bánh xe ánh sáng thiên thần (bánh xe ánh sáng liên tục trong ngực, không rõ nguồn); スプラッシュブレイカー Splash Destroyer → Scatter Breaker (Splash Là tên của tháp pháo tự động); ダブルライトニングソード Double Lightning Sword → Double Lightning Sword (sử dụng kép); ノーブルフェニックス Phượng Hoàng Cao Quý → Phượng Hoàng Tấn Công. Để biết trang và nguồn xác minh, vui lòng xem "Xác minh máy nhân vật chính và vũ khí" do phiên này tạo ra.

## Cấp bậc quân đội, chức danh và cách viết (quyết định của người dùng 2026-09-28)

- **Cấp bậc quân đội được viết theo hệ thống của ngôn ngữ đích và không sao chép chữ Kanji của Nhật**. Các cấp bậc quân hàm của quân đội Trung Quốc như sau: Tướng→Tướng, Đại tá→Đại tá, Trung tá→Trung tá, Thiếu tá→Thiếu tá, Đại úy→Đại úy, Trung úy/Thiếu úy không thay đổi, Chuẩn tướng không thay đổi; Tiếng Anh thống nhất sử dụng hệ thống Quân đội: Đại úy, Thiếu tá, Trung tá, Đại tá, Chuẩn tướng, Trung úy, Thiếu úy (ban đầu là Hải quân đã được thay đổi). Captain (thuyền trưởng) còn được gọi là Captain trong tiếng Anh. Từ tương tự như quân hàm là một quy ước trong tiếng Anh và sẽ không thay đổi. Danh hiệu "Tướng bóng tối" không phải là một cấp bậc quân sự như thường lệ; tên gọi chung “Tướng” (ông chủ) được dịch theo ý nghĩa. Mục "Thuyền trưởng ゴーマン" đã được đổi thành "Thuyền trưởng Gorman". Các trung úy đặc biệt/trung úy đặc biệt/lính đặc biệt của OZ vẫn giống nhau (Trung úy đặc biệt, v.v.).
- **Jia'er đối xử với Sayaka tùy theo dịp**: trực tiếp gọi cô ấy là "Sayaka" (hàng ngày, trong trận chiến); sử dụng "Ms. Sayaka" khi đề cập đến cô ấy với người khác. Tiếng Anh luôn là Sayaka.
- **Thánh** Thánh đoàn kết tiếng Anh (Saint Julia, the Saint, 'Saint of Cusco', tên tổ chức Saints' Corps).
- **Năm thế kỷ vũ trụ** Sử dụng nửa độ rộng: tiếng Trung "A.C. 195", tiếng Anh "A.C. 195". Khi bao gồm tháng, tiếng Trung là "Tháng Một, A.C. 191" (không có dấu phẩy) và tiếng Anh là "Tháng Một, A.C. 191".
- **Dấu tập cho tiêu đề chương** (2026-09-27): Tiếng Nhật (trước) (giữa) (sau), tiếng Trung (trên) (giữa) (dưới), tiếng Anh (Phần 1)/(Phần 2)/(Phần 3).
- **Chọn chi** (2026-09-27): Văn bản gốc không có "" và trong bản dịch không có dấu ngoặc kép; không có dấu chấm ở cuối tùy chọn,! ? … Giữ nguyên văn bản gốc.