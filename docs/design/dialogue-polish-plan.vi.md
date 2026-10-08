> **Ngôn ngữ / Language:** [Tiếng Việt](dialogue-polish-plan.vi.md) · [English](dialogue-polish-plan.en.md) · [中文](dialogue-polish-plan.md)

# Lập kế hoạch đánh bóng đường nét: đánh giá phong cách dựa trên tông màu của nhân vật

Ngày: 26-09-2026. Thực hiện phần "Đánh bóng so sánh tham chiếu" của [Bản địa hóa toàn văn bản](translation-plan.md).

## Kết luận

- Các dòng được dịch bằng máy (45.013 dòng bằng tiếng Trung và tiếng Anh) đã đáng tin cậy ở **mức độ ý nghĩa**: 366 dòng được so sánh từng dòng với bản dịch thủ công bằng tiếng Anh của Serenes Forest. Bản dịch của chúng tôi không có lỗi về nghĩa, nhưng phần tham khảo mắc năm sáu lỗi; chúng tôi đã quét toàn bộ cơ sở dữ liệu với hơn 100 thành ngữ thông dụng và đạt được 17 thành ngữ, tất cả đều được dịch chính xác. Lợi ích của việc tìm lỗi từng dòng một là thấp.
- Khoảng cách còn lại là **giọng điệu**: tiểu thư quý tộc, lão quản gia, chàng trai nóng nảy, quân nhân và lão phản diện có sự khác biệt rõ rệt về đại từ nhân xưng, đuôi câu và cấp độ kính ngữ trong tiếng Nhật. Bản dịch tiếng Trung và tiếng Anh đều trung lập và nhất quán. Nội dung chính của vòng đánh bóng này là: trước tiên hãy sắp xếp các cài đặt ký tự theo tác phẩm, sau đó để người mẫu đọc lại từng dòng với các cài đặt, chỉ thay đổi giọng điệu, tiêu đề và giọng điệu mà không thay đổi ý nghĩa.
- Còn một kiểu đọc sai cục bộ khác cần kiểm tra riêng: lật trang cắt một câu (đặc biệt là thành ngữ) ở giữa, mẫu chỉ nhìn nửa câu (17831 "渜のscaleでも｜せんじて Uống ませて"). Có 9.930 dòng lật trang trong tổng số 45.176 mục trong thư viện, trong đó có 8.885 dòng không có dấu câu ở cuối trang và các câu kéo dài hai trang. Thể loại này được bao phủ bởi "đọc lại toàn bộ dòng".

## 1. Cài đặt ký tự (`content/translation/voices.json`)

Từ hai nguồn, xác minh lẫn nhau:

1. **Bối cảnh tác phẩm**: Danh tính, tuổi tác, tính cách và mối quan hệ của nhân vật với nhân vật chính trong tác phẩm gốc. Được Claude tổ chức theo 15 tác phẩm tham gia chiến tranh, dựa trên sự hiểu biết của bản thân về tác phẩm gốc; các dấu hiệu không chắc chắn là `status: "check"`, để lại cho người dùng xác nhận.
2. **Thống kê văn bản gốc**: `tools/translation/speaker_features.py` Đếm đại từ nhân xưng, ngôi kép, kết thúc câu, kính ngữ và lời chửi thề của mỗi người nói từ tất cả các dòng tiếng Nhật (cốt truyện + trận chiến) và viết vào `assets/translation-runs/voice/speaker-features.{json,md}`. Đây là bằng chứng trực tiếp của mõm, ví dụ:マナミ 「あたし＋のよ／だわ／かしら」、アイシャ 「わたくし＋ですわ／わね」、ギャリソン 「ですな／ございます」,マスター 「ワシ＋様」, ジャネラ 「じゃ／のじゃ」. Mô tả giai điệu trong cài đặt phải khớp với số liệu thống kê.

Phạm vi và phân tầng: Có 259 loa âm mưu, trong đó 202 loa có ≥20 dòng chiếm 97% số dòng.

| Lớp | Loa | Nội dung thẻ |
| --- | --- | --- |
| A: ≥100 dòng cốt truyện (khoảng 100 người) | Nhóm nhân vật chính, nhân vật phản diện chính | Danh tính/câu ký tự, cơ sở thanh điệu tiếng Nhật, bản dịch tiếng Trung (người, địa chỉ của người, thanh điệu), bản dịch tiếng Anh, địa chỉ của các ký tự cụ thể |
| B: Dòng 20–99 | Vai phụ | Một câu về danh tính + một câu bằng tiếng Trung và tiếng Anh |
| Nhóm | スペシャルズ, ゲリラ, binh lính từ mọi phía | Thẻ một nhóm: giọng quân đội, ngắn gọn |
| Nhân vật chính/đối thủ chiếm giữ | Nhân vật chính, đối thủ (thay thế theo lộ trình) | Thẻ chỉ vào bốn nhân vật chính ban đầu và bốn đối thủ |

Nguyên tắc tiếng Trung (phù hợp với [chọn tên riêng](../native/localization-terms.md), chỉ sử dụng phong tục đại lục): tất cả các đại từ nhân xưng là "tôi", chỉ có ông già/lão phản diện ワシ/わし sử dụng "老夫", hoàng đế không sử dụng "朕" (không có trong văn bản gốc), オイラNó không được dịch là "tôi"; mức độ kính ngữ được thể hiện qua mẫu câu và chức danh (“bạn” chỉ được trao cho những người có kính ngữ rõ ràng: quản gia, cấp dưới với cấp trên, người trẻ với người lớn tuổi); giọng quý tộc dựa vào các cụm từ như "xin vui lòng/xin lỗi/không cần" hơn là tiếng Trung cổ điển.
Nguyên tắc tiếng Anh: Không có sự khác biệt về đại từ nhân xưng và giọng điệu phụ thuộc hoàn toàn vào cấu trúc câu, cách rút gọn, tiêu đề và các từ kính ngữ: Lawrence/Garrison sử dụng "my lady/Master Banjo" mà không rút gọn cho chủ; cấp dưới dùng quân đội thưa ông/bà; nhân vật phản diện cấp cao sử dụng các câu hoàn chỉnh mà không rút gọn, và thỉnh thoảng sử dụng "đồ ngốc"; thanh niên nóng nảy dùng những câu rút gọn, cảm thán, tiếng lóng nhưng không chửi thề; những quý cô quý tộc không sử dụng going/wanna.

Các trường thẻ: `work`, `gender`, `role`, `persona`, `ja` (tóm tắt thống kê), `zh`, `en`, `address` (gọi là những người cụ thể, ví dụ:マナミ →ローレンス "Lawrence", ローレンス → マナミ "Quý cô/quý cô"), `status` (dự thảo/đã phê duyệt/kiểm tra). `Characters.card()` sẽ đưa `zh`/`en` và `persona` vào thẻ ký tự của từ gợi ý.

## 2. Đánh giá về phong cách (`run_mt.py style`)

- Đầu vào: Tiếng Nhật toàn trang một dòng, toàn trang bản dịch có sẵn, thẻ người phát biểu, tên người đối thoại (người nói ở dòng trước và dòng sau), tiêu đề cảnh. Chia chúng thành từng đợt theo cảnh, mỗi đợt có khoảng 30 món. Cố gắng sử dụng cùng một người nói hoặc cùng một cuộc trò chuyện trong cùng một đợt.
- Hướng dẫn: Ý nghĩa, tên riêng, phần giữ chỗ, số trang không thay đổi; chỉ thay đổi khi **âm** không khớp với thẻ, **tiêu đề** không khớp với địa chỉ, **cường độ âm** không khớp với văn bản gốc (cảm thán, kéo dài, lắp bắp) hoặc sai **mức độ tương ứng** (dùng giọng điệu chung với cấp trên); những thay đổi nên càng nhỏ càng tốt; viết lý do cho mỗi thay đổi. Đọc toàn bộ bài viết và hiểu toàn bộ câu mà không có dấu chấm câu ở cuối trang.
- Kiểu máy: `deepseek-v4-pro-0813`; chạy riêng tiếng Trung và tiếng Anh; đầu ra `zh-v2-style`/`en-v2-style` (giai đoạn=kiểu), `write_dialogue.py --runs` được xếp chồng sau lô hiện có.
- Việc kiểm tra cơ học tuân theo `check_item` (số trang, phần giữ chỗ, dấu câu, bản dịch); hai kiểm tra tính nhất quán bổ sung được thêm vào: đại từ nhân xưng của cùng một người nói là duy nhất trong tiếng Trung ("I" hoặc "老夫") và tỷ lệ xuất hiện của tiêu đề được chỉ định trong bảng địa chỉ trong các câu có chứa tên.
- Điểm khác biệt so với đánh giá hiện tại (`review`): đánh giá tìm thấy lỗi, phong cách chỉ quan tâm đến âm thanh; không sử dụng câu dịch tham khảo.

## 3. Đọc lại toàn bộ bài viết trên trang

Bản thân giai đoạn `style` yêu cầu đọc qua hoàn chỉnh, bao gồm 8.885 dòng không có dấu câu ở cuối trang. Không còn phải làm một vòng một mình nữa.

## 4. Chấp nhận

- Chọn một đoạn hội thoại trong mỗi tác phẩm (một cho nhân vật chính và một cho nhân vật chính của tác phẩm) và đọc những thay đổi trước sau và lý do tại trang xem lại cốt truyện (`export_review.py`);
- Xem thực tế tập đầu tiên của bốn nhân vật chính Manami/Lawrence, Master Asia/Domon và Bright/Amuro;
- Vẽ 10 người dựa vào file loa cho tuyến chiến đấu.

## 5. Lệnh và phí

1. Cài đặt ký tự: Do Claude soạn thảo → Đánh giá của người dùng (xem lớp A trước, lớp B chuyển theo mặc định) → ghi vào voice.json.
2. Sử dụng tập đầu tiên (một trò chơi cho mỗi tuyến đường trong số bốn tuyến đường) để chạy thử nghiệm `style`, kiểm tra tốc độ và chất lượng thay đổi, sau đó điều chỉnh các từ gợi ý.
3. Khối lượng đầy đủ: khoảng 45k mặt hàng × 2 ngôn ngữ, mỗi đầu vào có giá khoảng 400 mã thông báo (bao gồm cả thẻ), giá chuyên nghiệp dựa trên bảng điều khiển; ước tính cao gấp 2–3 lần so với toàn bộ khối lượng của bản nháp đầu tiên (khoảng 50 nhân dân tệ).
4. Viết tập lệnh, chấp nhận và gửi nó.

## Kết quả thí điểm (26-09-2026, cảnh 0–3, tập đầu tiên của bốn nhân vật chính, dòng 335)

| Ngôn ngữ | Thay đổi | Bị từ chối bởi Kiểm tra cơ khí | Quan sát |
| --- | --- | --- | --- |
| Tiếng Anh | Dòng 19–27 (6–8%, dao động trong ba lần chạy) | Trả về các dòng 68–109 như cũ; thêm 5 dòng địa chỉ tự | Những thay đổi hiệu quả tập trung vào: Toàn bộ đoạn văn của Brad không bị rút ngắn và cứng nhắc (Do not/Let us → Don’t/Let’s); quản gia của Master Banjo cho chủ; Sự mâu thuẫn của Manami với Lord/Mr. Mô hình sẽ chơi quá mức theo thẻ: nếu văn bản gốc không có cuộc gọi, thưa ngài/quý bà/nếu tôi có thể nói như vậy sẽ được thêm vào và tính năng chặn cơ học đã được thêm vào (nếu văn bản gốc không có cuộc gọi 様/宫/cấp bậc quân đội, v.v., cuộc gọi mới sẽ bị từ chối). |
| Tiếng Trung | 2–6 dòng (1–2%) | Trả về 25 dòng như cũ | Giọng điệu của bản dịch máy tiếng Trung là nguyên bản; phiên bản đầu tiên của thẻ có nội dung "kết thúc câu là / nó" đã được mô hình sao chép một cách máy móc ("Chắc chắn rồi") và đã được thay đổi để dựa vào từ ngữ và địa chỉ chứ không phải các hạt phương thức. Những thay đổi hiệu quả duy nhất là các danh hiệu giống nhau (Lãnh chúa Wan Zhang→Ông Wan Zhang, Chúa Simone→Cô). |

Kết luận: Tiếng Anh đáng chạy đầy đủ, trong khi tiếng Trung chỉ cần chạy nhất quán về tiêu đề và một vài nhân vật (quý tộc, quản gia, phản diện cũ). Các sửa đổi đối với mô hình yêu cầu ai đó (Claude) xem xét từng cái một trước khi triển khai chúng. Dựa trên 6%, ước tính có khoảng 2.700 dòng bằng tiếng Anh và vài trăm dòng bằng tiếng Trung, giá cả phải chăng. Bản ghi đang chạy: `assets/translation-runs/{en,zh}-v2-style-pilot*`, bảng trước và sau các thay đổi nằm trong report.md tương ứng.

## Kết quả đầy đủ (2026-09-26)

Mỗi ngôn ngữ trong số hai ngôn ngữ đều chạy qua `style_review.py` (câu chuyện + chiến đấu, 1.407 đợt, mô hình chuyên nghiệp). Các thay đổi được Claude xem xét từng thay đổi một bằng cách sử dụng `tools/translation/curate.py` rồi viết vào `zh-v2-style-ok`/`en-v2-style-ok`, sau đó `write_dialogue.py` được chồng lên lô ban đầu và viết lại. `content/dialogue/` (282 lần thay đổi tệp).

| | Thay đổi mô hình | Không có sự khác biệt sau khi đổi tên (bỏ qua) | Chấp nhận | Viết lại thủ công | Trở về |
| --- | --- | --- | --- | --- | --- |
| Tiếng Trung | 1.015 | 423 | 343 | 2 | 247 |
| Tiếng Anh | 1.732 | 135 | 1.189 | 21 | 387 |

- Những thay đổi chính được chấp nhận trong tiếng Anh là: thêm các từ viết tắt và tiếng lóng cho các nhân vật máu nóng như Brad, Shinobu và Dio; các từ viết tắt và tiếng lóng được loại bỏ đối với Invincible East, Aisha, Lilina, Dorothy, Letty và những người quản gia; những người quản gia có tên thống nhất cho Master/Mr. Banjo, Rashid Master Quatre, Leti Your Excellence, và Tiến sĩ Hassan; hơn chục lỗi về tham chiếu hoặc ý nghĩa (30383/30384 "Aside with Telles" dịch là chống lại, 39956 Kẻ thù rút lui, 49993 レディ・アン dịch là Anna, 20612 "うようよ").
- Những thay đổi tiếng Trung được chấp nhận chủ yếu là: “I” cho Hoàng đế Zulu, “Ông già” cho Phương Đông bất khả chiến bại, “Lao Shen” cho Ganela, không có “I” cho Saisi và “La” cho thói quen truyền miệng của Boss; những chức danh như Ông Wan Zhang/Ngài Telles/Master Cartel; loại bỏ các tựa tiếng Nhật như "Classmate" và "Jun"; hơn một chục lỗi tham chiếu.
- Các trường hợp đổi trả điển hình: Người mẫu tự mình đổi tên dịch (Jiedu → Jieduo, シーラ → Shira, レイン → Rein, danh sách dự thi lần lượt là Jiedu, Sheila, Ling); thay đổi thư pháp Nhật Bản ("Char" → Quattro, "Kabuto" → Jia'er, シーラさん → "bạn"); Trò đùa "Thuyền trưởng/Thuyền trưởng" của Amuro; thêm thưa ngài/quý cô/"Tôi nói"/"Tôi nói với bạn"/"em yêu"/"nói dối" mà không được phép; cấp bậc thiếu úy/đại úy đặc biệt (sẽ được xác định).
- Tình cờ tôi phát hiện và sửa chữa: dấu câu JSON "]," (`fix_junk.py` → `zh-v1-junk`/`en-v1-junk`) bị rò rỉ ở cuối hơn 20 dòng bản dịch tiếng Trung và tiếng Anh.
- JSON được hai lô mô hình trả về bị cắt bớt (battle-09699 không chạy lại được bằng tiếng Anh hai lần) và những dòng này vẫn còn trong bản dịch gốc.
- Viết lại rồi chạy `check_voice.py`: Zulu I 100/I 25, Eastern Invincible I 60/I 84 ("I" bao gồm "we", v.v.), Lady vs. Tres Lord 38/Sir 24, Lady→Treize English Lord Treize 31/Treize 10. Sự không nhất quán còn lại tập trung ở các hàng không được mô hình trả về. Bước tiếp theo là sử dụng thay thế cơ khí ở cuối.

## TBD

- Các mục được đánh dấu `check` trong thẻ A-level yêu cầu người dùng xác nhận (chủ yếu là tính cách của các nhân vật gốc và 64 nhân vật phản diện gốc, cũng như một số nhân vật phụ không quen thuộc).
- Liệu phạm vi sử dụng “bạn” trong tiếng Trung có được siết chặt theo nguyên tắc trên hay không.
- Liệu những nhân vật phản diện người Anh cổ có giữ lại bản dịch "Đồ ngốc!/Thằng nhóc trơ tráo!" (bản dịch hiện nay chủ yếu là "Kẻ ngu xuẩn xấc xược").
- (2026-10-07) Ba mục trên chỉ ảnh hưởng đến các từ gợi ý khi chạy lại đánh giá kiểu; việc đọc chuyên sâu và đọc kỹ đã hoàn thành và sẽ không được xử lý trước khi xuất bản.
- ~~Phương pháp viết Trung úy đặc biệt/Đại tá đặc biệt/Sĩ quan đặc biệt~~ 2026-09-26 Người dùng xác định: Dự trữ ở cấp bậc quân đội lực lượng đặc biệt, Trung úy đặc biệt/Đại tá đặc biệt/Sĩ quan đặc biệt, Trung úy đặc biệt/Đại tá đặc biệt/Sĩ quan đặc biệt người Anh; Letty gọi Ngài là Ngài (người thứ ba là Ngài). `tools/translation/fix_consistency.py` Thống nhất cơ học (`zh-v1-consist`/`en-v1-consist`, chỉ những dòng có văn bản gốc chỉ chứa cấp bậc quân sự đó đã được thay đổi; 12 dòng của văn bản gốc có các cấp bậc quân sự khác đã được cải thiện từng dòng trong cùng một đợt).

## Tiến độ đọc chuyên sâu giai đoạn 2 (từ 26-09-2026)

Công cụ: `tools/translation/read_scene.py` (`dump --scene N --tag v3-read` in tiếng Nhật/tiếng Anh/tiếng Trung theo thứ tự chữ viết; `apply --fixes 文件 --scene N` hoặc `--batch 名` được `check_item` xác minh rồi ghi vào `en-v3-read`/`zh-v3-read`, `write_dialogue.py` Xếp chồng hai đợt này vào cuối). Các thay đổi được ghi lại trong `assets/translation-runs/read-fixes/` (một `scene-NNNN.json` cho mỗi trò chơi và một tệp dành cho các sửa đổi cơ học toàn cầu, cả hai đều có lý do).

Đọc chuyên sâu: Các cảnh 0–141, nghĩa là tất cả các cảnh (0 và 125 có cùng khóa; 1, 2, 3, 6, 8 đã được đọc lại vào ngày 27-09-2026) (tuyến công cộng, phân chia OZ, chiến tranh giữa thần và ác quỷ, tham gia tuyến OZ, Kilimanjaro, Axis Messenger và chi nhánh Vương quốc Sank; `dump` phải được mang theo `--tag v3-read`, nếu không bạn sẽ thấy văn bản trước khi sửa). Số lần thay đổi mỗi trận là từ 2-20 dòng. Vấn đề điển hình: tham khảo sai (できるな “có khả năng” được dịch là “Tôi có thể làm được”, やられてしまった chủ đề, riêng も／会いたかったecho), cách diễn đạt thành ngữ (từ đầu đến cuối cuốn sách, Kanbian,ラチがあかない, sự cảm thông từ されたいほう), thuật ngữ (不発 = bắn sai, オーバーヒート = quá nhiệt, 6つめĐề cập đến thân máy thứ sáu), phần cuối trang để trống/chỉ còn lại dấu ngoặc kép.

Nhân tiện, sự cố đã được phát hiện và khắc phục một cách cơ học trên toàn cầu (tên tệp = tên lô):

| Lô | Nội dung | Số Hàng |
| --- | --- | --- |
| `missing` | 66 dòng tiếng Anh và 9 dòng tiếng Trung không có bản dịch đủ tiêu chuẩn trong tất cả các đợt (giữ chỗ sai trang, sai số trang, trang trống) và được Claude dịch trực tiếp | 66／9 |
| `eiji-gale` | Tên thứ hai là Gale. Tổ tiên: Tên thống nhất trong tiếng Anh là Gale (ban đầu là Senior Gale/Sir được trộn lẫn) | 21 |
| `kun` | くん không dịch là "bạn cùng lớp" (chỉ giữ lại một nơi giáo viên giới thiệu học sinh) | 11 |
| `global-2` | ああ→"Chà" (ban đầu 108 "ahhh" giống như tiếng hét); Ngài ル・カイン→Ngài (Chúa ban đầu trộn lẫn); Chuẩn tướng Commodore→Chuẩn tướng | 73／12 |
| `aa-2` | ああ……→“Hmm…” | 31 |
| `quotes` | Lặp lại việc mở và đóng dấu ngoặc kép ở cuối/đầu trang qua các trang | 46／12 |
| `outer-quotes` | Toàn bộ dòng bị thiếu dấu ngoặc kép bên ngoài (311 dòng tiếng Anh, tập trung ở 17 cảnh; 46 dòng tiếng Trung) | 311／46 |
| `life` | ライフ (viết tắt của tổ chức Mặt trận Giải phóng Trái đất) thống nhất LIFE (trước đây là L.I.F.E./Liffe/Lives/La Vie en Rose/Life/Leif) | 7 |
| `muge`, `names-2`, `names-3` | Muge/Mugai→Muge, Shu Sama→Zama Sho, Galalia→Calalia, Cham→Cham, Shapiro→Shabiro, Dianan→Diana, Aphrodai→Aphrodite, Bran→Buran, Burn→Bern, Cham→Chum (danh sách từ vựng đã được xác định nhưng Phương pháp viết không được đổi tên.json) | 93／351 |
| 13 cảnh | Tiếng Trung 39 Chữ thêm "..." ở cuối dòng (thói quen dịch máy theo đợt đó) | 39 |
| `captain` | Đội trưởng luôn là Đội trưởng (Trung úy Amuro/Quattro hỗn hợp); Thiếu úy vẫn là Thiếu úy | 39 |
| `parens` | Thay đổi dấu ngoặc nửa độ rộng của độc thoại tiếng Trung thành toàn chiều rộng | 60 |
| `names-4`～`names-6` | Gula→Tiến sĩ. Guerra, Trăm quỷ→Hyakki, Kenji/Ming/Mika→Take/Kenji/Hui/Mika, Deathgaiyer→Death Gaia, Weiner/Người chiến thắng→Người chiến thắng | Khoảng 120 |
| `names-7`, `names-7b`, `names-8`, `zuul-en` | Tên các nhân vật trong trận chiến giữa thần và quỷ: Mars/Mars/Mars → Mars, Mag → Magu, Zuhl/Zil → Zulu (Tiếng Anh Zuhl → Zuul), Gundar → Gandal, Goldmas → Thunder King, Fried → Fried (`names-7` Thay thế "mas" sẽ nuốt chửng "godmas", `names-7b` sửa) | 678/41/17/một lượng nhỏ |
| `names-9`～`names-12`, `muge-2`, `hasan-*`, `barge-2`, `imperial` | Maz→Mars, Rose→Rose, Brachi→Brachi, Schott/Weibang→Sute/Weipeng, Qian→Qian'en, ムゲNhầm là "vô hạn"→Mr. Moog, ハサン→Dr. Hasan/Dr. Hasan, Balgy/Balgi→Sà lan, lực lượng đế quốc Anh→Imperial | 89/179/34/40/5/49/34 |
| Mỗi cảnh | Bỏ dấu gạch ngang trong tiếng Anh (thay dấu phẩy/dấu chấm/dấu chấm lửng); đổi số tiếng Trung sang ký tự tiếng Trung (hai khung, năm phút); hoàng đế Zulu tự gọi mình là "朕"; トレーズ様→Thưa ngài／Thưa ngài; Ông ハサン→Dr. Hasan／Bác sĩ Hasan | Từng cảnh |

Việc cần làm: Tất cả các cảnh đã được đọc kỹ (27-09-2026); lỗi trong --batch của read_scene.py đã được sửa (misc bị chặn trước scene-* và các phím tiếng Anh 55/99 tiếng Trung đã được hợp nhất thành zz-merge). Bây giờ mỗi ứng dụng ghi z<timestamp>-<name>.json; scene-0001 ban đầu là mẫu chữ viết tay đàm thoại 09-23, đã bị xóa và thay thế bằng cách tạo đường ống; trang đánh giá thủ công (tiêu đề/dấu ngoặc kép thẳng/eh): tất cả các dấu ngoặc kép thẳng và “eh” đều được sử dụng, tiêu đề vẫn giữ nguyên, chỉ có ông Gao → Daisuke là thống nhất; sau khi đọc kỹ, toàn bộ kho ngữ liệu cơ khí mech-en-1/2 (!?→?!, Gaiya→Gaia, Prof.→Giáo sư, ông Banjo→Banjo, các dấu gạch ngang còn lại là tất cả→hình elip, nền tảng Romfila→Foundation, 'em→'em, Sheela→Ciela), mech-zh-1 (nửa chiều rộng!?,..., người ngoài hành tinh), du kích-eei-zh, đại từ-master-zuul (Tôi trượt qua ròng); được thêm vào trong 106–141 zuul-master-zh (ズール＝Zulu, Dongfang Bubai tự gọi mình là tôi, sử dụng dòng['display'] làm văn bản bảo vệ gốc), virose-en (ヴァイローズ＝Virose), crest-en2 ('Seal' → 'Crest'), goshogun-title (《The Wolf of the Bronx》/‘The Wolf of the Bronx’), master-asia-chant (Thần chú bất khả chiến bại của trường học phương Đông: Câu tiếng Anh + Romaji Zenshin Keiretsu/Tenpa Kyoran); 43033/31709 Trang trống đã được cắt lại; khi ギシン星 xuất hiện một mình, việc đổi tên không được che đậy và nó đã được đổi thủ công thành ngôi sao động đất ngoài hành tinh; cũng thêm vào haman-side-zh（ハマーン堂→Haman-sama, viết bên N）、ellipsis-en/zh、quote-close-en、maelstrom-zh（メールシュトローム作戦Chuyển ngữ là Mellström, giữ nguyên cách chơi chữ), răng trắng → răng nanh trắng); 43774/44371/44503/44901/45035/47860/47912 trong số các trang TODO đã được cắt lại; và thêm Alien-zh (Alien→Alien), cựufed-en, ciela-mark-en (Sheela→Ciela, ‘Mark’→‘Crest’, 118 thiếu sót), master-zh (Mr. Dongfang→Mr. Dongfang, ランタオ岛→Lantau Island, Dongfang Invincible tự nhận là một ông già); scene-0089 thuận tiện cắt lại bản dịch máy và chép toàn bộ câu thành 17 mục trên hai trang (bản gốc quotes.json (đã sửa nhầm); Đã thêm grados-en/zh, mark-en ( khắc = Grados Crest, những người đầu tiên sống ở Grados), quotepage-en/zh (chỉ những trang có dấu ngoặc kép mới được quay về trang trước; 44901/47912/43033/31709 trang không khớp và cần phải được cắt lại); lô toàn cầu mới Zoole-en/zolbados-en (đánh vần Zuul), proton-zh (yang → proton), zh-punct (nửa độ rộng!? và dấu cách sau dấu chấm câu); write_dialogue đã được viết lại sau khi đọc tới 80; lô cơ khí toàn cầu đã được thêm các đặc biệt-zh (Lực lượng đặc biệt→Lực lượng đặc biệt), seiatsu-zh (Đàn áp→Đàn áp), sà lan-4 (Balge→Sà lan), relena-zh (リリーナ様→Lelina-sama), lavie-zh (Labian Rose→Lavian Rose); rewrite_dialogue đã được viết lại sau khi đọc đến 72; ghi chú `content/translation/renames.json` Đây là cách viết cuối cùng khi viết (ví dụ: đổi Simurgh thành Sweemurg, Balji → Baruch). trong lô; khi greping tệp vận chuyển, loại trừ dòng nhận xét `# 审校` và bản dịch cũ sẽ được trích dẫn trong nhận xét; `read-fixes/TODO-pages.txt` Liệt kê các dòng chỉ có dấu chấm câu trên trang và cần được phân trang lại (xử lý khi đọc cảnh tương ứng);

## Giai đoạn 2b: Đọc chuyên sâu chiến tuyến (27/09/2026)

Tiền đề: Bảng chọn dòng cho lớp phủ trận chiến được thiết kế ngược trong cùng ngày ([battle-quotes.md](../data/battle-quotes.md)) và `context.triggers` (tình huống/vũ khí/đối thủ/đồng phi công/kỹ năng kết hợp, xếp hạng hội thoại nhiều người) đã được thêm vào mỗi dòng chiến đấu khi xuất. `tools/translation/read_battle.py` đã được kết xuất bằng giọng nói và tệp vận chuyển đã được thay đổi thành một tệp cho mỗi giọng nói và được đưa vào. `# 触发：` nhận xét.

Phương pháp: 257 giọng (11.495 câu) được chia thành 15 nhóm (khoảng 780 câu/nhóm) theo thứ tự các giọng và giao cho 15 tiểu tác nhân song song đọc chuyên sâu. Mỗi tác nhân lấy cùng một mô tả công việc (ý nghĩa tình huống, thẻ giai điệu, quy tắc kiểu tiếng Trung và tiếng Anh, quy tắc cứng đánh số trang, định dạng đầu ra JSON) và chỉ tạo các tệp chỉnh sửa; nhóm phiên chính theo nhóm `read_scene.py apply --batch battle-gNN` (tất cả 0 từ chối), hãy thực hiện thêm ba việc:
- Toàn bộ thư viện máy được thống nhất `battle-sweep` (Dấu nháy đơn thẳng/dấu ngoặc kép thẳng → uốn cong, `!?` → `?!`, lắp bắp, デュオ's Thần chết → Thần chết; Tiếng Trungちっ→啧, くっ→Chà, ダミー→Bait, Aurali→Sức mạnh của Aura (âm mưu 29:5), ... );
- Tên các chiêu thức được căn chỉnh theo `battle-names` (Các mục hô chuyển động của G Gund Split Sound/draw Sound: Erupting Burning Finger/Burning Slash/Sekiha Tenkyoken/Chokyu Hao Den'eidan/Juni Ohohai Daisharin, Nobel Hula Hoop), cách viết thông thường là đổi tên (Rose Bits/Rose Float Cannon, Rose Roaring, Rose Hurricane, Rising Sun Arrow, Gravity Bolas, True Meteor Butterfly Sword, God's Slash, Burning Ngón tay/Chém, Nắm đấm Borot đặc biệt, Chém ánh trăng, Tấn công mặt trời, Kiếm đôi quỷ);
- Viết lại_đối thoại.

Số lượng thay đổi: 15 bộ tiếng Anh chuyên sâu, 1.493 câu, 2.020 câu trung cấp (khoảng 13%/18%), tiếng Anh thống nhất cơ học 3.218 (gần như toàn bộ dấu nháy đơn), 76 trung gian, di chuyển tên 30/5. Tệp bó có tại `assets/translation-runs/read-fixes/battle-*.json`.

Các vấn đề lặp lại trong mỗi nhóm (dịch máy trước khi đọc chuyên sâu + hiệu đính): tình huống không khớp ("だめか" đã dùng hết được dịch thành "không được", "や" bị bắn hạ "られた" được dịch là "đánh", và "そこか／なんの／干い" được dùng làm câu hỏi hoặc khen, "やったな／やってくれる" được dịch sang khen ngợi, hết đạn/ngoài tầm, chủ ngữ bị đảo ngược); trong hội thoại nhiều người, mỗi câu được dịch độc lập mà không cần đọc liên tục (ダブルゴッドフィンガー, シャッフルAlliance Boxing, hai thành viên của phi hành đoàn lấy hết câu này đến câu khác); cùng một câu được lưu ở hai giọng nhưng có cách dịch khác nhau (Kỹ thuật kết hợp cả hai mặt, Miケロス/デモニカ); thanh điệu (cuối câu) Ne/oh xếp chồng, thanh điệu quý tộc dựa vào các tiểu từ tình thái, sếp だわさChuyển ngữ là "Wasa", phương ngữ sử dụng các từ phía bắc); ちっ→cắt, ええい→hum, くっ→ho; thiếu trích dẫn tiếng Anh Các phần được phân đoạn của chiếc sừng (アリアス, ジェリド, シロッコ, エル, デル／ダニー／デューン, v.v.) đã được hoàn thành; số dấu chấm than không khớp với văn bản gốc.

Chưa quyết định, để lại cho người dùng: Một người chỉ được gọi là "Ofu" "Ofu" (biệt danh "Oshi Kali" cũng được gọi là "Ofu" (Oshikashi Ghost/ブライ大帝/ガンダル/Hell Marshal/ドレイク), và tình hình hiện tại là "Ofu" đối với Ushio Ghost và tôi đối với những người khác); “Namu San” được dịch theo ký tự. A Di Đà/Thiên Tử; チボデー Tiếng Trung và tiếng Anh (Ôi chúa ơi/Nooo/baby) được bảo lưu; “rơi” chủ yếu là “để tôi ngã”, còn nhân vật nữ thì dè dặt “ngã”; オッパイミサイルPhiên âm tiếng Anh được giữ lại; tên viết tắt của "ロボ" trong kiệt tác vẫn là "robot"; âm thẻ của ケーラ/カトル không khớp với âm điệu của văn bản gốc (thẻ cần phải thay đổi).

## Giai đoạn 2c: Mở đầu, Kết thúc, Lựa chọn và Tiêu đề Chương (27-09-2026)

Việc cần làm của người dùng 1: "Bản dịch tinh tế của phụ đề mở đầu và các phần khác". Sau khi lấy kho, phạm vi do người dùng xác định là: 30 trang cho phần mở đầu, 7 trang cho phần kết, 133 tín chỉ, 133 tiêu đề chương và 48 dòng phần tùy chọn (điều kiện thắng bại nằm trong văn bản hệ thống và chưa được hoàn thành).

- **Mở đầu** (Đợt `read-fixes/intro-close.json`): Claude dịch lại từ tiếng Trung sang tiếng Anh từng trang. Trang tường thuật đầu tiên cố tình lặp lại những câu nói tiếng Trung và tiếng Anh thông dụng của đoạn tường thuật mở đầu của phần đầu tiên, nhưng nội dung được dịch từ văn bản gốc của tác phẩm này (người dùng đã chọn "Echo, nhưng không sao chép"). Dùng từ ngữ để căn chỉnh thư viện hội thoại: thuộc địa vệ tinh (không dùng “thuộc địa”), chủ nhân (không dùng “master”), Chiến tranh giành độc lập Zeon/Chiến tranh một năm, phong trào kháng chiến, du kích; năm, tháng ghi là "A.C. January 191..."/"January, A.C. 191..." theo sơ đồ dịch thuật. Sự tương ứng giữa lộ trình và nhân vật chính có thể được tìm thấy trong kế hoạch dịch thuật; giới tính của anh em và đệ tử không thể nhìn thấy trong văn bản. Trong tiếng Trung, "cùng một đệ tử" được sử dụng. Nhân tiện, "dì" của おばさん trong 32625 đã được đổi thành "dì", phù hợp với đoạn mở đầu và 17604.
- **Trang cuối** (file viết tay `ending.txt`, sửa đổi trực tiếp): 6 điểm trau chuốt bằng tiếng Trung; 5574 thiếu mệnh đề "that" được thêm vào bằng tiếng Anh, khiến hai trang đối đầu "không thể quên".
- **Các nhánh được chọn** (đợt `read-fixes/choices-close.json`): `read_scene.py dump` ban đầu chỉ được liệt kê với loại=đối thoại và 48 hàng các nhánh được chọn đã bị bỏ sót trong toàn bộ lô trong quá trình đọc chuyên sâu (bây giờ chúng được liệt kê cùng nhau, được đánh dấu `[选项]`). Ba điều đã được thống nhất lần này: các tùy chọn không có "" trong văn bản gốc sẽ không được đặt trong dấu ngoặc kép; các tùy chọn sẽ không có dấu chấm ở cuối (giữ nó!?...); bản sao của cùng một tùy chọn trong các tình huống khác nhau sử dụng cùng một bản dịch. Ngoài ra, một số từ như "Muge→Muge", sóng xung kích của Takeru (để Takeru đánh thức Daisuke bằng sóng xung kích) và Cannian だわ đã được sửa đổi.
- **Tiêu đề chương** (phần giai đoạn trong bảng nhập, `apply_terms.py` Mở rộng): Dấu tập phim Trung Quốc đã được thay đổi từ (trước) (giữa) (sau) thành (trên cùng) (giữa) (dưới); các tên được căn chỉnh theo các mục và dòng (Zir → Hoàng đế Zulu, Fu → Feng, Mars → Mars); cách diễn đạt tiếng Nhật đã được thay đổi (fajin → tấn công, xuất hiện → lộ diện, nhầm lẫn → hỗn loạn); và một số bản dịch thẳng thừng theo nghĩa đen đã được thay đổi (trái tim ở trong nắm tay đó → trái tim ở trong nắm tay này, ý nghĩa của chiến đấu là gì → ý nghĩa của chiến đấu là gì). 6 bài viết đã được sửa đổi bằng tiếng Anh.
- **Danh sách ghi công** (file viết tay `credits.txt`): Nomura Kyoyu đổi thành Michihiro Nomura bản tiếng Anh (wikipedia tiếng Anh, VGMdb); Jin Akabane, Kono さち子 こうの, Hamada Tomoyuki Hamada đã tìm ra nguồn, các bài đọc còn lại vẫn chỉ là suy đoán và được liệt kê ở đầu file tiếng Anh. Vị trí: Tiếng Trung ディレクター sử dụng "đạo diễn" và bức tranh trình diễn gốc làm "bức tranh gốc trình diễn trận chiến" và loại bỏ "(căng thẳng)"; English Battle Animation Key Art, Hợp tác, Lập kế hoạch & Xuất bản. Trang danh sách MobyGames đã được máy tính xác minh và chưa được đọc.

## Giai đoạn 3: Kiểm tra cơ học và kiểm tra ngẫu nhiên (27/09/2026)

Kế hoạch (được người dùng phê duyệt): 1. Kiểm tra cơ học → 4. Kiểm tra ngẫu nhiên để đưa ra quyết định → Quyết định dựa trên kết quả 2. Đọc cốt truyện theo lộ trình, 3. Đọc bằng tiếng Anh → 5. Xem bố cục trên máy thực tế.

Kết quả khám thực thể:
- **Khung trận quá dài**: Theo kích thước khung tĩnh `dialogue_paging.py`, dòng chiến dài nhất là 31 ký tự tiếng Trung và 91 ký tự tiếng Anh. Kích thước phông chữ mặc định có thể vừa với nó và không cần phải rút ngắn.
- **Cùng nguồn nhưng khác bản dịch**: Cùng một câu trong tiếng Nhật, cùng một người nói, các bản dịch khác nhau, 2.664 nhóm (6.419 câu) trong tiếng Trung và 2.832 nhóm trong tiếng Anh. Các câu đối (720 câu) được thống nhất thành bản chuyên sâu/đa số; cốt truyện **không** tự động thống nhất: lấy mẫu nhận thấy rằng cùng một câu đề cập đến những thứ khác nhau trong các cảnh khác nhau ("bạn/bạn", "cô ấy/anh ấy", ngôi thứ hai và ngôi thứ ba), và sự thống nhất máy móc sẽ sửa những câu đúng. Đã báo cáo trong bảng ghi nhớ phiên `polish/samesrc.json`, để lại để tham khảo khi đọc qua.
- **Trôi tên đặc biệt**: Sử dụng chứng từ vận chuyển để so sánh danh sách nhập và đổi tên. Những sự trôi dạt thực sự duy nhất là Rayne→Ling, Janella→Ganela, Wil Wiphs→Will-Wips, Quebeley→Qubeley và hai tên tách câu/nói lắp, đã được đổi tên hoặc sửa đổi thủ công. Các "lỗi" còn lại là dương tính giả chuỗi con (レミー∈グレミー, パンチ∈ロケットパンチ). Hai cách viết chính bảng mục nhập (`Ten'o Shohazan` dấu nháy đơn thẳng, `Prof. Yumi`) thuộc về cuộc hội thoại trong bảng mục nhập.
- **Từ tượng thanh**: Tiếng Anh Kuh→Ngh, Uwah→Waah, Guwah→Gwah, Eei→Chết tiệt; Tiếng Trung ちっ→啧 (hoàn thành cốt truyện). Tổng cộng có 234 câu tiếng Anh và 74 câu tiếng Trung.

Kiểm tra ngẫu nhiên: Đọc ngẫu nhiên 300 câu (200 cho cốt truyện, 100 cho trận chiến) bằng tiếng Trung và tiếng Anh một lần để tạo trang nhấp chuột (bộ sưu tập hiện vật JAyBc2MjoTSJnrVynfSkoK, `qa`). Dựa trên tỷ lệ lỗi, hãy quyết định xem có đọc toàn bộ phần 2 và 3 hay không. 48 thẻ âm trong `voices.json` vẫn ở trạng thái kiểm tra và yêu cầu xác nhận của người dùng.

Kết quả đọc qua giai đoạn 3 (28/09/2026):
- **Đọc cốt truyện theo lộ trình (Kế hoạch số 2)**: 142 cảnh được xâu chuỗi với nhau theo thứ tự tôpô `next_scenes`, cắt thành 40 khối (mỗi khối khoảng 600–1000 câu) và đọc song song. Mỗi khối chỉ xem liệu tiếng Trung đọc có trôi chảy hay không và tiếng Anh có giống dòng bản địa hay không (hướng dẫn công việc có trong bảng ghi nhớ hội thoại `route/brief.md`). Áp dụng tất cả 40 khối (đợt `read-fixes/route-r01…r40.json`, 3 câu bị từ chối: giữ chỗ trải khắp các trang), tổng cộng khoảng 4.700 câu tiếng Trung và khoảng 3.400 câu tiếng Anh, chiếm khoảng 14%/10% cốt truyện; các bản sao nhánh (một bản sao của cùng một đoạn được lưu trên các tuyến khác nhau) được đồng bộ hóa theo cùng một phương pháp sửa đổi.
- Các vấn đề điển hình được phát hiện qua quá trình đọc: sai tham chiếu ở câu trước và câu sau (bạn/bạn, anh ấy/cô ấy, hoán đổi chủ ngữ và tân ngữ), hoán đổi câu hỏi và câu, tách chữ khi lật trang hoặc chỉ có “Is it left” ở cuối trang, dịch trực tiếp từ tiếng Nhật sang Hán tự (yuyu, tính sai, tái xuất hiện, trách nhiệm, hành động sai), thuộc tính dài; Giọng Nhật trong tiếng Anh (Không còn cách nào khác, Đúng như dự đoán, tôi sẽ không tha thứ cho bạn, X, phải không) đã bị xóa trong toàn bộ cơ sở dữ liệu; còn có hàng chục lỗi nghĩa đã bị bỏ qua ở vòng trước (ví dụ: 流とさせるな dịch là "không cho nó thoát", và easy ではないかと dịch là "không dễ dàng").
- **Đọc tiếng Anh bản ngữ (Kế hoạch số 3)**: Được lồng ghép vào phần đọc qua ở trên; Ngoài ra, cốt truyện tiếng Anh của toàn bộ thư viện và dấu nháy đơn thẳng của nhánh được chọn được thống nhất thành ’ (15.692 câu) và không có `Prof.`, em-dash, `!?` trong toàn bộ thư viện.
- Danh hiệu và tự xưng: Hầu tước ヤヌスわらわ thống nhất "vợ lẽ"; thêm tên: Ngôi sao hôn → Ngôi sao ngoài hành tinh, Ngôi sao chạy trốn → Hành tinh chạy trốn; Master Asia còn lại bằng tiếng Trung đã bị xóa.
- Đối với người sử dụng: “Sự không chắc chắn” trong mỗi báo cáo đã được xử lý theo lẽ thường hoặc được giữ nguyên hiện trạng. Các vấn đề tập trung bao gồm việc Ka'er gọi Sayaka là "Sayaka" hay "Bà Sayaka" (cả hai đều có mặt trong cốt truyện), Thuyền trưởng được dịch là từ giống như đội trưởng, Ensign được dịch là Ensign (Quân đội phải là Thiếu úy), Holy Woman/Saint được viết bằng tiếng Anh và năm "AC 195" được viết bằng nửa chiều rộng. (Quyết định ngày 27-09-2026, `b89af8a`: cấp bậc quân sự theo hệ thống ngôn ngữ mục tiêu, Thiếu úy; Jia'er gọi trực tiếp cho Sayaka và nhắc đến "Cô Sayaka"; Thánh; năm vẫn còn nửa chữ số.)
- **Máy thực tế (Kế hoạch số 5)**: 2026-09-27 Chứng từ vận chuyển sau khi chạy qua `tools/recomp/debug/check_dialogue.py --reuse-build --records 25`: 18 bản ghi, 25 lần kiểm tra đều đạt (ranh giới trang được căn chỉnh với phiên bản gốc, I/K thay đổi cỡ chữ để giữ nguyên trang, F7 chuyển về cùng một trang cho tiếng Trung, tiếng Anh và tiếng Nhật), không có `battle_overflow`; Việc sắp chữ tiếng Trung và tiếng Anh cũng như dấu ngoặc kép trong ảnh chụp màn hình là bình thường. Tất cả các tuyến chiến đấu có thể được đặt theo quy tắc bố trí tĩnh và chưa được thử nghiệm riêng biệt trong trận chiến. Lưu ý: Hộp tên của người nói trong ảnh chụp màn hình này hiển thị tên tiếng Nhật (カーツ, ブラッド). Bạn cần kiểm tra xem đó là cài đặt ngôn ngữ tập lệnh hay sự cố truy cập tên.
- **Kiểm tra tại chỗ (Điều 4 Kế hoạch)**: Sau khi đọc qua, 300 câu ngẫu nhiên của các bản dịch vận chuyển sẽ được đánh giá từng câu bằng cách xem xét độc lập: 9 câu tiếng Trung có vấn đề (3,0%, toàn dịch sát nghĩa, không có lỗi nghĩa), 10 câu tiếng Anh (3,3%: 6 dịch sát nghĩa, 2 sai nghĩa, 2 câu không phù hợp với tình hình chiến đấu); theo ngưỡng dự kiến ​​(khoảng 3%), sẽ không đọc lại đầy đủ nữa và chỉ sửa lại 19 câu đã trích. và quét toàn bộ thư viện các câu hỏi tương tự (tiếng Anh chiến đấu "聄い" → tùy theo tình huống Quá chậm/Bạn cởi mở/Quá yếu, "hiệu ứng かない" → Điều đó không có tác dụng với tôi, tổng cộng có 63 câu). Trang nhấp chuột (bộ sưu tập giả tạo JAyBc2MjoTSJnrVynfSkoK, `qa`) được dành riêng để người dùng đánh giá và đã được thay thế bằng văn bản đọc qua.

## Giai đoạn 4: Dịch sát nghĩa cốt truyện tiếng Trung (2026-10-07)

Người dùng hy vọng sẽ "cải thiện tổng thể và giảm bớt dịch nghĩa đen". Sau vài vòng đầu tiên, vấn đề chính của tiếng Trung là đọc như được sao chép từng chữ từ tiếng Nhật và có rất ít lỗi về nghĩa.

luyện tập:
- Đầu tiên, người đàm thoại chính đã thay tập đầu tiên của Ake (Cảnh 2, 117 câu đã đổi thành 57 câu) làm mẫu (`1e755c3`), đồng thời biên soạn danh sách dịch sát nghĩa từ đó: dịch sát nghĩa các từ tiếng Nhật trong tiếng Trung (đảm bảo, loại bỏ, hiểu biết, tiêu diệt, giác ngộ, tái sinh, trốn thoát…), sao chép các mẫu câu (“…” được xếp lớp, “…” dùng để biến câu phát biểu thành câu hỏi, thuộc tính dài, bị động câu), từ chứng minh tương ứng theo từng từ, ngôn ngữ viết trong hội thoại và xếp chồng các tiểu từ tình thái ở cuối câu.
- 141 cảnh còn lại được cắt thành 40 đoạn theo trình tự (mỗi đoạn khoảng 900 câu), mỗi đoạn giao cho một tiểu cảnh, người này lấy mô tả giống nhau: danh sách dịch nghĩa đen và ví dụ trước và sau khi thay đổi; những đồ vật không được phép di chuyển (ý nghĩa, tên riêng, chức danh, quân hàm, người, từ tượng thanh hét, số trang, phần giữ chỗ, dấu ngoặc kép bên ngoài); thẻ thoại của các nhân vật xuất hiện trong khối này. Tác nhân phụ chỉ gửi `{键: 新译文}` và sử dụng tập lệnh xác minh để tự kiểm tra và phát hiện lỗi không (số trang, phần giữ chỗ, trang trống; xóa tên, thay đổi dấu câu bên ngoài và kéo dài rõ ràng).
- Phiên chính xem xét các báo cáo, ứng dụng, cam kết theo từng khối (một `polish(zh): story scenes … (N/40)` cam kết trên mỗi khối). **Thay đổi trực tiếp `content/dialogue/zh-Hans/story/*.txt`** vận chuyển, không còn qua `write_dialogue.py`: tạo lại chứng từ vận chuyển không còn xuất hiện (trước đó đã có thay đổi trực tiếp), bản thân chứng từ vận chuyển là phiên bản cuối cùng.
- Các bản nhánh của cùng một câu tiếng Nhật và cùng một bản dịch cũ được đồng bộ hóa; tuy nhiên, những dòng rất ngắn ("いくぞ!" "まったく" "そうだよ") có ý nghĩa khác nhau trong các ngữ cảnh khác nhau. Đồng bộ hóa được giới hạn trong cùng một cảnh hoặc các câu dài hơn và không chạm vào chiến tuyến. Hạn chế này không tồn tại trong những ngày đầu và 11 câu sai đã được sửa lần lượt.
- Giới tính của nhân vật chính và bạn đồng hành thay đổi tùy theo nhân vật chính do người chơi lựa chọn: nghĩa là họ không thêm "anh ấy/cô ấy" (tôi thấy rằng một chỗ đã được đổi thành "cô ấy", và "cô ấy" được thêm vào ở hai vị trí, và nó đã được đổi về trung tính).

kết quả:
- Có 9.654 bản Hán ngữ sửa đổi cốt truyện (bao gồm cả bản nhánh), tỷ lệ sửa đổi mỗi khối là 10%-49%, trung bình khoảng 30%; các tệp dòng tiếng Trung và tiếng Anh được xác minh đầy đủ mà không có lỗi nào bằng cách sử dụng `dialogue_text.load`.
- Nhân tiện, phó tác nhân đã sửa hơn 20 lỗi nghĩa (đảo ngược cách đọc có điều kiện, hoán đổi chủ ngữ-tân ngữ, câu hỏi tu từ dưới dạng câu "お手与み拝见", "よくもいったものだ", "まったく", ​​​​v.v.).
- Thuật ngữ kết thúc: sức mạnh オーラ luôn là "sức mạnh hào quang", オーラ luôn là "Aura" (loại bỏ sức mạnh hào quang/hào quang/lực hào quang); Zeon tái sinh → Zeon hồi sinh; Đại từ nhân xưng của Delmaio và Ganeela trở thành ông già / thân xác già.
- **Tỷ lệ mù**: Chọn ngẫu nhiên 100 bản dịch, bản dịch mới và cũ được sắp xếp ngẫu nhiên theo A/B và giao cho người đánh giá độc lập: bản dịch mới tốt hơn 78, bản dịch cũ tốt hơn 15, gần 7; Có 2 lỗi về nghĩa trong bản dịch mới (tất cả các từ được thêm vào, thay đổi) và 1 lỗi ở bản dịch cũ.

Chưa hoàn thành/còn lại cho người dùng:
- Vòng này không thực hiện các dòng chiến đấu (11.500 dòng) và tiếng Anh.
- Trong danh sách đầu vào, ガラバ (chiến binh Ora của Bahn) và tổ chức カラバ đều được dịch là "Karaba". Người chơi sẽ bối rối và cần phải trò chuyện trong bàn vào để đưa ra quyết định.
- `voices.json` Các tên trong thẻ âm được viết theo lối cũ (Lei Yin, Henken, Sai Sisi...) và các dòng viết theo lối viết hiện có (Ling, Henken, Cai Saixi...); đại lý phụ đã nhiều lần báo cáo những khác biệt như vậy là có vấn đề.

## Giai đoạn 5: Toàn bộ dòng chiến đấu tiếng Trung và tiếng Anh sẽ được dịch hoàn toàn (2026-10-07)

Sau đó, ở giai đoạn 4, chúng tôi sử dụng quy trình tương tự để tạo ba phần còn lại, mỗi phần có một mô tả tác phẩm (Trận chiến tiếng Trung: sử dụng danh sách dịch theo nghĩa đen của mô tả cốt truyện, cộng với một tình huống kích hoạt, khoảng 30 từ mỗi trang và một phương pháp viết cố định; tiếng Anh: lấy bản dịch nghĩa đen của cảnh thứ hai bằng tiếng Anh làm ví dụ, các quy tắc sắp chữ được thực thi bởi tập lệnh xác minh - chỉ có dấu ngoặc kép, không có dấu gạch ngang, "?!"). Mỗi chiến tuyến đều có một tình huống kích hoạt; Tiếng Anh cũng không được phép thêm he/she để chỉ nhân vật chính hoặc bạn đồng hành.

- Chiến tuyến của Trung Quốc: 13 khối, 2.083 thay đổi (12%–26% mỗi khối).
- Cốt truyện tiếng Anh: 40 khối, 11.660 thay đổi (21%–51% cho mỗi khối, cao hơn tiếng Trung, chủ yếu là rút gọn, cấu trúc câu và sáo rỗng cố định). Một trong những phần đã bị gián đoạn do lọc nội dung và được viết ra thành từng phần rồi chạy lại.
- Tuyến chiến đấu của Anh: 13 khối, 2.017 thay đổi (12%–26% mỗi khối).
- Cái kết thống nhất: Ten’o Shohazan (dấu nháy cong), Chizuru Nambara (liệt kê theo mục và tên), BF Group, Dark Gundunda, Aura Power, và Raki trong trận chiến đều “Đi xuống!”, Doctor Hassan được gọi là Doctor; "đầu ra" của trận chiến Trung Quốc và súng chính Libra được đổi thành "sức mạnh"; Câu "Xem tôi giết bạn" của Shinobu được đổi thành "Xem tôi chiến đấu."
- Tệp hội thoại tiếng Trung và tiếng Anh `dialogue_text.load` được xác minh đầy đủ không có lỗi.

So sánh mù quáng (cũ và mới được sắp xếp ngẫu nhiên thành A/B, được xem xét độc lập):

| Phần | Lấy mẫu | Bản dịch mới tốt hơn | Bản dịch cũ hay hơn | Hầu như | Sai nghĩa (mới/cũ) |
| --- | --- | --- | --- | --- | --- |
| Cốt truyện Trung Quốc (giai đoạn 4) | 100 | 78 | 15 | 7 | 2／1 |
| Chiến đấu Trung Quốc | 50 | 45 | 4 | 1 | 0／2 |
| Kịch Tiếng Anh | 70 | 54 | 9 | 7 | 4／1 |
| Trận Anh | 30 | 26 | 2 | 2 | 0／1 |

Bản dịch mới của cốt truyện tiếng Anh có thêm 4 ý nghĩa bổ sung hoặc tài liệu tham khảo không chính xác (Chúc ngủ ngon, với anh ấy, chủ nhà của chúng tôi, Nó đã làm vậy), đã được sửa chữa. Sau đó, tất cả 13.731 câu tiếng Anh được sửa trong vòng này đều được kiểm tra "chỉ ý nghĩa" theo yêu cầu của người dùng (14 tác nhân phụ, mỗi câu được dịch sang tiếng Nhật, trước và sau khi sửa, chỉ thêm nghĩa, thiếu nghĩa, tham chiếu sai, thêm đại từ giới tính cho nhân vật chính/đối tác, những thay đổi tối thiểu không làm thay đổi cách viết): 81 bản sửa lỗi (bao gồm 87 bản sao), khoảng. 0,6%, thấp hơn nhiều so với ước tính tỷ lệ mù với một mẫu nhỏ; khi bị đánh, "やったな／やってくれたな" giữ lại "Mày sẽ phải trả giá cho việc đó!" và không chấp nhận đề nghị đổi nó thành "Bạn hiểu rồi!".

Người dùng để tôi quyết định (2026-10-07): Phiên bản tiếng Trung của ガラバ (Chiến binh Ora của Bahn) đã được đổi thành "Garaba", ハイパーガラバ "Super Galaba", và được phân biệt với tổ chức カラバ "Karaba" (danh sách tham gia và đổi tên đã được thay đổi, và bài viết đổi tên đã có đã được thay đổi để chỉ bao gồm văn bản gốc) The Saints of Cusco (クスコの圣女, người độc thân vẫn là Saint of Cusco), 23 câu đã đổi động từ sang số nhiều. Chúng vẫn cùng tồn tại: trận chiến "もらった" của Trung Quốc thành công/thắng, việc tránh "gan い" là quá ngây thơ/quá trẻ. Hai phương pháp viết cùng tồn tại (cả hai đều trơn tru và không bị thống nhất một cách gượng ép).