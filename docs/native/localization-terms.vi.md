> **Ngôn ngữ / Language:** [Tiếng Việt](localization-terms.vi.md) · [English](localization-terms.en.md) · [中文](localization-terms.md)

# Trung Quốc hóa văn bản dữ liệu: danh sách đầu vào và thông số dịch thuật

Ngày: 23-09-2026. Bài viết này giải thích cách dịch "văn bản dữ liệu" như tên, nhãn và lời nhắc hệ thống, cách nhập thư mục ngôn ngữ và thông số dịch thống nhất cho tiếng Trung (`zh-Hans`) và tiếng Anh (`en`). Các dòng không xuất hiện ở đây: Các dòng chiến đấu (khoảng 5799–17346), đoạn hội thoại trong cốt truyện và các chi được chọn (từ 17347) được đặt trong các tệp văn bản thuần túy độc lập. Người chơi có thể sửa đổi từng cái một, xem [Tệp văn bản dòng](../guide/dialogue-text.md); có một quy trình riêng cho bản nháp dịch máy của họ và các bản dịch phải tuân theo danh sách đầu vào của bài viết này.

## Tại sao nên sử dụng danh sách từ?

5. 650 mục đầu tiên trong bảng văn bản `base:t00` là tên và văn bản giao diện: địa hình, tiêu đề công việc, tiêu đề cấp độ, cơ thể, phi công, vũ khí, lệnh tinh thần, khả năng và kỹ năng đặc biệt, chương trình nâng cao, nhãn và lời nhắc trên màn hình liên trường, cũng như lời nhắc nhập tên, danh sách nhân vật, hướng dẫn lệnh phản công, điều kiện chiến thắng hoặc thất bại và mức độ thiệt hại. Văn bản gốc tiếng Nhật giống nhau sẽ được lặp lại trong nhiều bản ghi (một cho mỗi thân máy có cùng tên vũ khí, một cho mỗi dạng của cùng một phi công) và văn bản danh sách vũ khí (`格ビームサーベルP`) là sự kết hợp của "dấu + tên vũ khí + dấu". Bản dịch từng dòng vừa lặp đi lặp lại vừa có xu hướng không nhất quán.

Vì vậy, có một danh sách các mục cho mỗi ngôn ngữ `content/locales/terms/<locale>.json`: "Văn bản gốc tiếng Nhật → bản dịch" được liệt kê theo phân vùng và mỗi văn bản gốc khác nhau chỉ được dịch một lần. `content/locales/terms/sections.json` chỉ định phạm vi bản ghi tương ứng với từng phân vùng. `tools/content/apply_terms.py` mở rộng bảng mục nhập thành các mục nhập thông thường với `source_sha256` (được gắn nhãn `"origin": "terms"`) trong thư mục ngôn ngữ. Thời gian chạy và trình nhập đầu tiên của C++ vẫn chỉ đọc các mục nhập và không cần biết bảng mục nhập.

- Danh sách vũ khí (phân vùng `weapon_menus`) không được dịch riêng: bản dịch từ phân vùng `weapons` được viết theo cú pháp gốc - `格`/`射` tiền tố, bản dịch, `P`/`B`/`MAP` hậu tố không thay đổi. Những chữ cái này chỉ là phần giữ chỗ: các bản vẽ gốc sử dụng glyph biểu tượng đặc biệt (241–244, 575) trong thư viện phông chữ và bảng vũ khí gốc cũng vẽ các biểu tượng gốc này, bất kể ngôn ngữ. Đối với vũ khí có tên gốc kết thúc bằng `MAP` (`ファンネルMAP`), bản dịch cũng phải kết thúc bằng `MAP`.
- Phân vùng có dấu `complete` yêu cầu mỗi văn bản gốc chứa văn bản tiếng Nhật đều phải có bản dịch; `models` (kiểu khung máy bay) chỉ dịch văn bản không phải kiểu máy bay, chẳng hạn như `飛行試作型MA`.
- Khi không tìm thấy bản ghi tương ứng cho văn bản gốc trong bảng nhập (văn bản gốc sai chính tả hoặc phân vùng đặt sai vị trí), công cụ báo "unused".
- Bài dự thi và bài viết tay không được trùng một hồ sơ; 73 bản dịch viết tay gốc trong vùng dữ liệu đã được chuyển sang bảng nhập và 93 đoạn hội thoại viết tay của tập đầu tiên đã được chuyển sang tệp văn bản dòng. Bây giờ chỉ còn lại các mục nhập trong thư mục ngôn ngữ.

```sh
PYTHONPATH=src .venv/bin/python tools/content/apply_terms.py            # 改完词条表后重写语言目录
PYTHONPATH=src .venv/bin/python tools/content/apply_terms.py --check    # 只检查，目录过期时失败
PYTHONPATH=src .venv/bin/python tools/content/apply_terms.py --missing  # 列出 complete 分区还缺的原文
```

`tests/test_terms.py` Kiểm tra xem các phân vùng của bảng nhập tiếng Trung và tiếng Anh có phù hợp với tập hợp văn bản gốc không và bản dịch vẫn không thay đổi. `<G:...>` Các tham số và mục nhập đều là bản nháp; khi có ROM, đồng thời xác nhận rằng thư mục ngôn ngữ phù hợp với kết quả mở rộng của bảng nhập.

## Hiển thị vị trí và ranh giới

- Trang gốc (trang xác nhận trước chiến tranh, mỗi màn hình giữa các trận đấu) lấy các văn bản này thông qua thư mục ngôn ngữ và chuyển sang tiếng Trung hoặc tiếng Anh để hiển thị bản dịch; bản dịch bị thiếu sẽ quay trở lại tiếng Nhật.
- Khi chuyển giao diện về phiên bản gốc trong phần cài đặt, màn hình gốc được vẽ bằng mẫu font ROM và vẫn hiển thị chữ tiếng Nhật; đây là chế độ ban đầu được cố ý giữ lại.
- Các nhãn trong menu bản đồ chiến thuật gốc, hoạt ảnh chiến đấu và văn bản được đưa vào hình ảnh chưa được tích hợp vào thư mục ngôn ngữ; hồ sơ của họ đã được dịch và sẽ có sẵn trực tiếp khi chúng được tích hợp.
- Không được dịch: thẻ gỡ lỗi (các mục hiragana 1179–1369, 4307–4381 dành cho trình chỉnh sửa hoạt hình trận chiến, trình chỉnh sửa cờ trận chiến và câu chuyện 5644–5798), tiêu đề âm nhạc (232–280), thanh tỷ lệ được sửa đổi (4145–4267), phông chữ biểu tượng bản đồ (5104–5149), bảng nhập tên (5220–5239, 5247–5449).

## Thông số chung

**Tiếng Trung (Giản thể)**: Sử dụng bản dịch thông dụng của người chơi đại lục (Gundam, Mazinger Z, Getter) và không sử dụng bản dịch Hồng Kông và Đài Loan (Gundam, Magnum, Getter).パイロット luôn được dịch là "phi công" (phó パイロット là "phi công phụ"; được xác định bởi người dùng trên 25-09-2026, "thí điểm" trong các tuyến sẽ được thay đổi đồng thời và ghi vào `content/translation/renames.json`). Sử dụng dấu cách `·` (U+00B7) giữa các tên; sử dụng dấu chấm than, dấu hỏi và dấu ngoặc đơn có độ rộng tối đa. Kích thước của kiểu máy, `HP`, `EN`, `MAP`, `L1`–`L9`, `S`/`M`/`L`, v.v. vẫn giữ nguyên. Những cái tên phổ biến được ưu tiên hơn cách viết chính thức: bản dịch hiện tại là giữ lại những cái tên phổ biến ở Trung Quốc đại lục (Camus Bidan, Shira Wei, Zaku, Dongfang Bubai); khi không có tên phổ biến thì sử dụng tiếng Trung giản thể chính thức; nếu không có, hãy nhấn phiên âm và thử sử dụng tên người thường được sử dụng. **Không sử dụng bản dịch tiếng Đài Loan và Hồng Kông** (Quyết định của người dùng 2026-09-24): Phiên bản tiếng Trung phồn thể, tiếng Đài Loan, tên đồng âm tiếng Đài Loan và phiên bản Hồng Kông không được sử dụng làm cơ sở, chỉ để tham khảo. King of Thunder là một ngoại lệ được người dùng xác nhận: bản phát sóng ở Trung Quốc đại lục năm 1994-95 là phiên bản Đài Loan và không có phiên bản chính thức từ Station B; chỉ có tên tác phẩm và tên máy được giữ lại, còn tên và bước di chuyển của phiên bản Đài Loan sẽ được xem xét riêng.

**Tiếng Anh**: Ưu tiên viết chính thức: Bản tiếng Anh chính thức của Bandai Namco (Super Robot Wars V/X/T/30), trang web tiếng Anh chính thức của GTA, bản phát hành chính thức bằng tiếng Anh (Discotek, v.v.) và thẻ chính thức; nếu không, hãy tuân theo các ký tự La Mã phổ biến và quy ước trong vòng tròn tiếng Anh (Hepburn, các âm dài không có ký hiệu: `Koji Kabuto`). Giữ nhãn càng ngắn càng tốt: chiều rộng cột của trang gốc được thiết kế theo tiếng Nhật, phần văn bản quá dài sẽ bị cắt bỏ.

**Cả hai ngôn ngữ**: Giữ nguyên thông tin của văn bản gốc mà không cần giải thích; giữ các số, `+`, `%` trong văn bản gốc; hai hoặc nhiều khoảng trắng liên tiếp trong văn bản gốc là phần giữ chỗ để điền số (`第  話`, `(最大で  段階まで)`, `あと  機`, `命中率    %`), trang gốc thay thế khoảng trắng kép đầu tiên bằng một số và bản dịch phải giữ nguyên các khoảng trắng này (`第  话`, `(最多  段)`, `Stage  `); trong lời nhắc nhiều dòng Có thể điều chỉnh vị trí của `<BR>`.

## Tiêu đề công việc

| Bản gốc | Tiếng Trung | Tiếng Anh |
| --- | --- | --- |
| Bộ đồ di động Mobile | Bộ đồ di động Mobile |
| Nhóm MS thứ 08 | Nhóm MS thứ 08 | Nhóm MS thứ 08 |
| Bộ đồ di độngGundam 0083 | Bộ đồ di độngGundam 0083 |
| Bộ đồ di động Zeta Gunma | Bộ đồ di động Zeta Gunma |
| Bộ đồ di độngGundam ZZ | Bộ đồ di độngGundam ZZ |
|Cuộc phản công của Char | Cuộc phản công của Char |
| Bộ đồ di độngGundam F91 | Bộ đồ di độngGundam F91 | Bộ đồ di độngGundam F91 |
| Máy bay chiến đấu di động G Mobile | Máy bay chiến đấu di động G Mobile |
| Bộ đồ di động mới Cánh Gun | Bộ đồ di động mới Cánh Gun |
| Mazinger Z | Mazinger Z |
| グレートマジンガー | Mazinger vĩ đại |
| Máy phóng Robot UFO | Máy phóng Robot UFO |
| Getter Robo / Getter Robo G | Getter Robo / Getter Robo G |
| Robot chiến đấu siêu điện từ V | Robot chiến đấu siêu điện từ V |
| Siêu nhân bất khả chiến bại Zambot 3 | Siêu nhân bất khả chiến bại Zambot 3 |
| Người Thép Bất Bại Titan 3 | Người Thép Bất Bại Titan 3 |
| Sengoku Majin GoShogun | Sengoku Majin GoShogun | Sengoku Majin GoShogun |
| Thánh chiến binh Dunbine | Thánh chiến binh Dunbine | Aura Battler Dunbine |
| Dancouga: Siêu Thần Máy Thần | Dancouga: Siêu Thần Máy Thần |
| Sao chổi xanh SPT Layzner | Sao chổi xanh SPT Layzner |
| Lục Thần Kết Hợp Thần Hỏa | Lục Thần Kết Hợp Vua Sấm | Lục Thần Kết Hợp Thần Hỏa |
| ジャイアント・ロボ | Robot khổng lồ |
| オリジナル | Bản gốc | Bản gốc |

## Các dạng từ thường dùng

Cấu trúc từ tương tự vẫn nhất quán trong tên máy, tên vũ khí, tên khả năng và tiêu đề cấp độ.

| Bản gốc | Tiếng Trung | Tiếng Anh |
| --- | --- | --- |
| ガンダム | Gundam | Gundam |
| マジンガー | 魔神 | Mazinger |
| ゲッター | Người nhận | Người nhận |
| オーラ | Hào quang | Hào quang |
| ビーム | Chùm |
| Pháo hạt Mega | Pháo hạt Mega |
| ビームサーベル | Chùm Saber | Chùm Saber |
| ビームライフル | Súng trường chùm | Súng trường chùm |
| Vulcan | Vulcan |
| ミサイル | Tên lửa | Tên lửa |
| ファンネル | Pháo nổi | Kênh |
| ドリル | Khoan | Khoan |
| ロケットパンチ | Cú đấm tên lửa | Cú đấm tên lửa |
| Lực Photon ビーム | Tia lực Photon | Chùm Photon |
| ブレストファイヤー | Lửa Vú |
| Tomahawk | Tomahawk |
| ミノフスキー | Minovsky | Minovsky |
| Tôiフィールド | Tôi buộc trường | I-Field |
| Siêu hợp kim Z／Siêu hợp kim NiニューZ | Siêu hợp kim Z／Siêu hợp kim Z mới | Siêu hợp kim Z / Siêu hợp kim Z mới |

## Nhân vật chính

| Bản gốc | Tiếng Trung | Tiếng Anh |
| --- | --- | --- |
| アムロ・レイ | Amuro Ray | Amuro Ray |
| シャア・アズナブル | Char Aznable | Char Aznable |
| カミーユ・ビダン | Kamille Bidan | Kamille Bidan |
| ジュドー・アーシタ | Judau Ashta |
| ドモン・カッシュ | Domon Kasshu | Domon Kasshu |
| ヒイロ・ユイ | Heero Yuy | Heero Yuy |
| Koji Kabuto | Koji Kabuto |
| 剣鉄也 | 剑 Tetsuya | Tetsuya Tsurugi |
| Ryoma Nagare | Ryoma Nagare |
| Hyoma Aoi | Hyoma Aoi |
| 神胜平 | 神胜平 | Kappei Jin |
|Banjo Haran |Banjo Haran|
| ショウ・ザマ | Zama Sho | Hiển thị Zama |
| Shinobu Fujiwara | Shinobu Fujiwara |
| Myojin タケル | Myojin Wu | Takeru Myojin |
| Daisaku Kusama | Daisaku Kusama | Daisaku Kusama |

Tên mặc định của ký tự gốc sử dụng cùng tên dịch với ký tự tương tự trong danh sách thí điểm (ví dụ: Manami Hamill). Phân vùng `default_names` (bản ghi 487–502) cũng là nguồn dữ liệu cho tên mặc định hiển thị ba ngôn ngữ trong trò chơi. Họ và tên được phân tách khỏi tên đầy đủ theo dấu phân cách, xem [Hiển thị ba ngôn ngữ tên mặc định](default-names.md).

## Hiển thị quyền truy cập và tồn đọng dự án (23/09/2026)

Tất cả văn bản gốc đều đi qua công cụ văn bản thường trú: `8008D0E8`/`8008D140` nhóm thẻ một dòng (60 vị trí, `0x8015CB00`), `8008C9C0` nhóm văn bản nội dung (`0x800FBAB0`), `8008C88C` nhóm số, được vẽ mọi khung bằng `8008DC40`. Hàm truy xuất từ ​​`8008CF14` chỉ đọc bảng văn bản 0 và thay thế bản ghi tên của nhân vật chính và đối tác bằng tên bộ nhớ. Chỉ có hai cách để đi qua thư mục ngôn ngữ: bộ điều hợp hội thoại (đối thoại cốt truyện; dòng chiến đấu chỉ hiển thị sẽ được thêm từ ngày 23 tháng 9 năm 2026) và các trang RmlUi gốc (màn hình giữa các cảnh, trang trước trận chiến, trang tên, trang liên kết, cài đặt).

Đã sửa lỗi (`cb86e82`, `27b221e`): Trang gốc hiển thị tên mặc định thay vì tên do người chơi nhập, loa thoại không được dịch, tên không được làm mới sau khi chuyển ngôn ngữ trên trang liên cảnh, trang xác nhận vũ khí và phần thưởng sửa đổi đầy đủ hiển thị tên menu được đánh dấu, tên máy của lời nhắc hoàn tiền và dòng chiến đấu. 23-09-2026 Xác minh máy thực bằng `tools/recomp/debug/check_localization.py`: Tất cả các màn hình trong tập đầu tiên của tệp thông quan đã vượt qua tất cả các kiểm tra bằng tiếng Trung và tiếng Anh, bao gồm chuyển đổi ngôn ngữ khi mở, tên nhân vật chính nhất quán trong ba ngôn ngữ, trang xác nhận vũ khí và báo cáo lỗi tải lại F5; Chế độ `battle` xác nhận rằng các dòng được vẽ lại nguyên bản và người nói đã được dịch trong trận chiến. Không thể truy cập màn hình chuyển trong kho lưu trữ này (quá ít trình điều khiển) và không được che phủ. (Từ 27/09/2026, tên mặc định được hiển thị theo ngôn ngữ và mục "Tên nhân vật chính nhất quán trong ba ngôn ngữ" được thay đổi để kiểm tra xem tên mặc định có thay đổi theo ngôn ngữ hay không.)

Việc cần làm, theo thứ tự ưu tiên:

1. **Bố cục trang gốc**:
- Các mảnh ghép theo thứ tự từ tiếng Nhật đã được thay đổi thành mẫu giao diện với `{name}`: phần thưởng sửa đổi đầy đủ, chuyến đi cổ tích, phương tiện lưu trữ, lời nhắc Pak và chân trang giữa các trò chơi.
- Thay đổi phần giữ chỗ số khoảng cách kép thành mẫu `{n}`. Tiếng Anh hiện đang hiển thị `Stage12`.
- ~~RmlUi tải phông chữ theo ngôn ngữ~~: Bắt đầu từ ngày 23-09-2026, gói HarmonyOS Sans (`3beb303`) sẽ được sử dụng bằng tiếng Trung, tiếng Anh và tiếng Nhật, đồng thời các phông chữ hệ thống như Hiragino và Arial Unicode sẽ không còn được sử dụng; không có trọng lượng phông chữ đậm.
- Thay đổi chiều rộng thành số đo thực tế và thêm kích thước phông chữ và hình elip tối thiểu. Có một số nhãn trên trang khả năng của người lái xe trùng lặp với các giá trị.
- ~~Huy hiệu nhãn hiệu vũ khí được thay đổi để sử dụng id nhãn hiệu và bản sao giao diện~~: 2026-09-24 Thay đổi để vẽ trực tiếp biểu tượng gốc, giống nhau ở mỗi ngôn ngữ, xem [Màn hình sửa đổi](native-upgrade-screens.md).
- Tên kỹ năng trên trang trước trận chiến và trang kỹ năng được thống nhất từ cùng một nguồn.
2. **Chọn cửa sổ chi và cửa sổ mục tiêu chiến đấu**: Sử dụng cùng `8008F648`, điểm khác biệt là không có hộp tên và con trỏ.
3. **Giao diện gốc của bản đồ chiến thuật**: menu lệnh, trang trạng thái/khả năng, danh sách và mô tả tinh linh, bảng quân, lệnh phản công, lựa chọn xuất kích. 25-09-2026 Lớp phủ phổ quát đã được hoàn thành: các nhãn, số và văn bản bên ngoài hộp thoại của hai dòng văn bản (`8008DC40`, `8008EB5C`) được vẽ lại theo ngôn ngữ đọc gốc, xem [văn bản giao diện gốc](native-ui-text.md). Các trang trạng thái được xem thường xuyên vẫn có thể được chuyển thành trang gốc trong tương lai.
4. **Văn bản hình ảnh**: văn bản thu phóng mở đầu (đã dịch), thẻ tiêu đề chương, biểu ngữ sân khấu, văn bản hiệu ứng đặc biệt trong trận chiến. Nó có thể được sắp xếp lại bằng văn bản gốc hoặc được thay thế bằng hình ảnh được chuẩn bị sẵn ngôn ngữ và toàn bộ cơ chế chia sẻ thay thế hình ảnh trong quy hoạch HD.
5. **Chuỗi công cụ**:
- Thêm điểm đánh giá vào danh sách đầu vào. Trước khi thay đổi định dạng, hãy thông báo cho máy tập lệnh cách dịch nó.
- Danh sách người tiêu dùng của báo cáo bảo hiểm được thay đổi thành "sổ cái bảo hiểm văn bản" thực sự.
- ~~Thông số nhập sau khi hợp nhất các dòng quá lớn~~: Nó đã được thay đổi để các dòng không được nhập vào thư mục ngôn ngữ và thay vào đó, một [Tệp văn bản dòng](../guide/dialogue-text.md) độc lập được sử dụng. Thông số nhập được nhúng vẫn chỉ có tên và văn bản giao diện (khoảng 1,7 MB).
6. ~~** Cần xác định**: Tên mặc định tiếng Trung không có trong bộ ký tự ROM. Bây giờ nó không thể được nhập dưới dạng tên và bản dịch của tên mặc định không bao giờ được hiển thị~~: 2026-09-27 Người ta xác định rằng không được phép thay đổi tên. Chỉ có glyph gốc được lưu trữ trong vùng tên. Tên mặc định được thay đổi thành ngôn ngữ đọc khi hiển thị. Xem [Hiển thị ba ngôn ngữ tên mặc định](default-names.md).

## Đợt dịch đầu tiên (23/09/2026)

Tất cả 2.433 văn bản gốc trong 31 phân vùng đều có bản dịch tiếng Trung và tiếng Anh, được mở rộng thành 4.674 bản ghi ở mỗi ngôn ngữ; `--missing` và `unused` đều bằng 0.

29-09-2026 Đã thêm phân vùng `songs` (bản ghi 232–280, tên bản nhạc trong chế độ đánh giá âm nhạc và chế độ karaoke): Deck Trong quá trình kiểm tra video, người ta nhận thấy rằng danh sách bản nhạc tiếng Trung hiển thị tên bài hát tiếng Nhật. 38 tên bài hát tiếng Nhật đều có bản dịch tiếng Trung-Anh. Các tên tiếng Anh gốc như `FLYING THE SKY` không được dịch; Tên bài hát tiếng Anh viết bằng katakana (サイレント・ヴォイス, バーニング・ラブ) cũng sử dụng tên gốc tiếng Anh bằng tiếng Trung. Bây giờ có 32 phân vùng, 2.471 văn bản gốc, 4.712 bản ghi cho mỗi ngôn ngữ.

2026-09-30 Rút bản dịch tên bài hát: Người dùng yêu cầu tên bài hát trong chế độ thưởng thức âm nhạc và karaoke phải vẫn bằng tiếng Nhật. Phân vùng `songs` đã được đổi thành `complete: false` và 38 tên bài hát đã bị xóa khỏi hai danh sách mục nhập. Sau khi mở rộng, mỗi ngôn ngữ quay trở lại 4.674 bản ghi và danh sách bản nhạc hiển thị văn bản gốc của ROM. Không thêm bất kỳ bản dịch bổ sung nào vào đoạn này trong tương lai.

Lô bản dịch đầu tiên ngoài những bản dịch được liệt kê ở trên:

- **Mệnh lệnh tâm linh bằng tiếng Anh** Theo T/30, phiên bản tiếng Anh có tên: Bullseye, Flash, Vigor, Guts, Wall, Valor, Soul, Faith, Rouse và Daunt. Trong tiếng Trung, những cái tên cộng đồng phổ biến như trực giác, sự kiên trì, sự kiên trì tuyệt vời, bức tường sắt, niềm đam mê và tâm hồn được sử dụng. Chữ viết tắt một ký tự (1149–1178) lấy chữ cái đầu tiên của tên dịch trong tiếng Trung và lấy "lớn" cho "sự kiên trì tuyệt vời"; nó có ba chữ cái bằng tiếng Anh và nó phát nổ thành `SD`.
- **Trạng thái và Kỹ năng**: 気力 trong tiếng Anh đã được thống nhất thành Will, và Tinh thần ban đầu trên trang trước chiến tranh đã được thay đổi. Phiên bản tiếng Anh của Holy Warrior được thống nhất thành Holy Warrior và các quy tắc của Chiến binh hào quang ban đầu đã được thay đổi. Cắt り払い trong tiếng Trung có nghĩa là "cắt đứt", tăng cường có nghĩa là "tăng cường sức mạnh cho con người" và S phòng thủ có nghĩa là "S phòng thủ". Các nhãn viết tay trên trang trước chiến tranh đã được thống nhất bởi các thuật ngữ: Aura Barrier, I Force Field, Planetary Defender, Mach Special, Shadow of God.
- **Phần cứng và tên riêng**: コントローラパック là "thẻ nhớ cầm tay", 64GB パック là "thẻ chuyển 64GB" và シャッフル được hợp nhất thành "Liên minh Shuffle". Phiên bản tiếng Trung của "Eastern Invincible" thường được sử dụng ở Trung Quốc đại lục là "Supreme Gund".
- **Vũ khí MAP tiếng Anh** được viết là `Buster Rifle MAP`. Văn bản danh sách đánh vần sẽ có thêm khoảng trắng trước dấu nhưng phải được giữ lại khi phân tách theo cú pháp gốc trong thời gian chạy nên không thể nhìn thấy trên màn hình.
- **Lỗi chính tả ROM** Không sao chép: モンド・アガケ và モンド・アカゲ đều được dịch là Mondo Agake. Chữ viết chính thức là Agake, và アカゲ trong ROM là lỗi đánh máy (đợt アカゲ đầu tiên được dịch là Akage, sửa vào ngày 24-09-2026).ゲーツ・キャバ và ゲーツ・キャパ đều được dịch là Gates Capa/Gates Capa.
- Chữ "・" trong **Điều kiện thắng thua** đã được đổi thành dấu phẩy trong tiếng Trung và dấu chấm phẩy trong tiếng Anh. "～の撃波" được viết là trung lập "～撃撃／～ bị phá hủy", bởi vì cùng một câu sẽ xuất hiện trong cả danh sách chiến thắng và danh sách thất bại.

## Kiểm tra các bản dịch chính thức và phổ biến (24/09/2026)

Phiên "Lập kế hoạch dịch và xuất hệ thống định dạng văn bản" đã kiểm tra từng bản dịch chính thức và phổ biến của từng tác phẩm theo các thông số kỹ thuật trên. Tham chiếu đến các phiên bản tiếng Trung và tiếng Anh chính thức của Machine War, GUNDAM.INFO, Discotek, Bilibili, Baidu Encyclopedia, Mengniang Encyclopedia, v.v. Bảng so sánh ban đầu nằm trong `assets/translation-runs/official-names/` (không nhập git) và nguyên tắc lựa chọn có thể được tìm thấy trong `POLICY.md` trong cùng một thư mục.
- Tổng cộng có 625 mục, trong đó có 595 mục đã được nghiên cứu, 30 mục còn lại được viết đồng bộ với việc đổi tên trong tên cấp độ và điều kiện thắng thua. Danh sách tên cốt truyện được duy trì bởi bên kia.
- Viết vào bảng nhập: 403 giá trị tiếng Trung và 174 giá trị tiếng Anh.
- Ví dụ:
- Tiếng Trung: Hanazono Rei, Zama Sho, Ming Shenwu, Fukamura Rei, Zanbo 3, Thunder King, Big Iron Man (tiêu đề và nội dung tác phẩm), ngọn lửa ngực, tia lực photon;
- Tiếng Anh: G Gundam sử dụng tên Bắc Mỹ Burning Gundunda/DarkGundam; máy ban đầu sử dụng cách đánh vần thẻ chính thức là Sweemurg, Virose và Razgreez.
- Bản dịch tiếng Anh của các đối thủ ban đầu là Kurtz Forneus, Rish Griswell và Ehrlich Stasen: cách viết cộng đồng là phát âm sai, còn Forneus là tên của quỷ dữ.
- Tên trong nội dung các dòng được bên kia thay thế theo cùng bảng nên người nói trong hộp thoại phù hợp với nội dung văn bản.

Quyết định của người dùng (2026-09-24):
- 14 mặt hàng bị đình chỉ:
- Các tên đồng âm trong bản Đài Loan không được sử dụng, giữ nguyên phiên âm: Boqiuen, Miuji Poe, Dozdozi, Jinjin;
- アラン giữ lại Alan; ケンジ đổi thành Kenji, アキラ đổi thành Hui; ヴェスバー sử dụng VSBR;
- Thunder King giữ nguyên tên tác phẩm và tên máy. Đó là một ngoại lệ: phiên bản phát sóng ở Trung Quốc đại lục năm 1994-95 là phiên bản Đài Loan và không có phiên bản gốc từ Station B.
- Sau đó, bên kia nhấn vào “Không cần dịch tiếng Đài” để xem lại toàn bộ danh sách và tạo trang web để người dùng chọn từng mục một. Lựa chọn của người dùng đã được thay đổi thành 65 giá trị tiếng Trung khác, trong khi các giá trị tiếng Anh không thay đổi. Sáu trong số đó là tên cấp độ và điều kiện chiến thắng và thất bại được đồng bộ hóa với việc thay đổi tên.
- Tên: Mako (Marco), Rose (Roger), Kara Suen (Kira Mori), Bran, Reika Sanjo, Tachibana Meili, Tokida Garrison, Quake Soldiers, Chỉ huy Otsuka;
- Đơn vị: Gondor, Zvas, Laineke, Leprakon, Hound;
- Vũ khí: Gaia Crush, Dark Finger, Honorable Belt, Roaring Rose, Solar Flash Bomb, Spin Drill, Cosmic Thunder, v.v.
- Những thay đổi cũ dựa trên tiếng Trung Phồn thể chính thức cũng do người dùng quyết định lần lượt trong vòng này.

## Đang chờ xem xét và chưa được xác minh

- Tất cả bản dịch đều là bản nháp (`review_status: draft`). Sau khi xem xét, thay đổi từng mục nhập thành `reviewed`: Sửa đổi danh sách mục nhập, chạy lại `apply_terms.py` và sau đó đánh dấu mục đó trong thư mục ngôn ngữ.
- Những điều sau đây chỉ là dự kiến: phiên âm từ máy bay gốc, máy bay địch và các chiêu thức không có tên tiếng Trung phổ biến, chẳng hạn như アースゲイン Asgain, ヴァルディスキューズ Valdisquez; "Con dấu" của Layzner; Khổng Minh và những cái tên khác chỉ có một nguồn gốc. Việc xác minh vào ngày 24-09-2026 đã được xác định là シャインスパーク Flash Explosion, ストナーサンシャイン Sun Flash Bomb (người dùng đã chọn), レイン・ミカムラ Fukamura Rei.
- Tên dài tiếng Anh có thể bị cắt bỏ trong danh sách bản địa. Các chữ viết tắt được sử dụng trong danh sách đã được rút ngắn từ "Tướng bóng tối" và "Nguyên soái địa ngục" thành Tướng hắc ám và Thống chế địa ngục, đồng thời tên đầy đủ vẫn giữ nguyên bản dịch chính thức của chúng. Danh sách gốc sẽ giảm kích thước phông chữ theo chiều rộng của hộp; tên đơn vị tiếng Anh dài nhất sau khi kiểm tra là Super Beast Shishiris Garo/Kiba (26 ký tự).
- Lời nhắc được chia thành nhiều phần được đánh vần để dịch, bao gồm lời nhắc Pak, hướng dẫn lệnh phản công, phần thưởng sửa đổi đầy đủ và "X が, Y になります". Phương pháp nối và ngắt dòng thực tế chưa được xác minh trên màn hình.
- Ảnh chụp màn hình thực tế bằng tiếng Trung và tiếng Anh của trang gốc đã được `check_localization.py` tạo và kiểm tra, xem ở trên.
- Cốt truyện và lời thoại chiến đấu không nằm trong phạm vi của bài viết này: chúng nằm trong tệp văn bản dòng, được tạo ra bởi một quá trình dịch máy khác và bản dịch dựa trên bảng nhập ở đây.