> **Ngôn ngữ / Language:** [Tiếng Việt](link-battler.vi.md) · [English](link-battler.en.md) · [中文](link-battler.md)

# Link Battler liên kết: F91, ゴーショーグン, ザンボット3 Cách mở

2026-09-19. Bài viết này dựa trên phiên bản tiếng Nhật bị khóa Rev 0 `rom.z64` để phân tích tĩnh: lớp mã thường trú của trình điều khiển GB Pak, lớp phủ màn hình chuẩn bị `load_0008F4B0` (ROM `0x8F4B0`, VRAM `801C4500`; offset bảng ROM = VRAM − `0x801C4500` + `0x8F4B0`), và các tập lệnh và bản ghi triển khai cho các cảnh 109–122 trong `assets/original-data/records`. So sánh dữ liệu cộng đồng [Akurasu Wiki: Link Battler Units][wiki] (truy cập cùng ngày). **Không có trò chơi nào được chạy trong vòng này và không có hộp mực hoặc kho lưu trữ Link Battler nào để so sánh với**. Các mục yêu cầu chạy để hoàn thiện được liệt kê trong Phần 8.

## 1. Tóm tắt kết luận

| Kết luận | Cơ sở |
| --- | --- |
| Không có "dấu mở khóa" trong trò chơi. Công việc của liên kết là **thay đổi cấp độ tiếp theo thành cấp độ chèn**: cấp độ tiếp theo ban đầu được lưu trữ trong `8010F5F2`, `8010F5F0` được thay đổi thành cấp độ liên kết; sau khi hoàn thành cấp độ liên kết, tập lệnh sử dụng `3D4B 500` để quay lại cấp độ tiếp theo ban đầu | `801D9F80`; sự kiện cuối cảnh 109–122 |
| Các đơn vị mở được xác định **theo công việc**, với tổng cộng 3 vị trí: dòng F91 (vị trí 1), ゴーショーグン (vị trí 2) và ザンボット3 (vị trí 4). Mỗi trong số 7 sự kết hợp tương ứng với một cấp độ liên kết và mỗi cấp độ liên kết có hai phiên bản (dựa trên việc cấp độ tiếp theo có được chọn trong vũ trụ hay không, nó được suy ra là phiên bản mặt đất và phiên bản không gian), với tổng cộng 14 cảnh | Bảng `D_801DCABC` |
| Để một tác phẩm được mở, nó phải đáp ứng các yêu cầu sau: 64 Ở đây chưa có nội dung tác phẩm nào; có một trong những vị trí phi công cơ thể hoặc nhân vật chính của tác phẩm trong kho lưu trữ GB | `801D9F80` |
| Mức độ liên kết xuất hiện khi chúng tôi triển khai: F91＋シーブック、ビギナ・ギナ＋セシリー；ゴーショーグン＋ Shingo; Nhân Mã + Katsuhira, Nhân Mã + Thái Vũ Trụ, Nhân Mã + Kaizi (tổ hợp mở đầu là Nhân Mã 3) | Nhóm triển khai 1 cho các kịch bản 109–122 |
| Các biến tiến trình var48 (F91), var49 (ゴーショーグン), var50 (ザンボット3) được viết là 0 ở cuối cấp độ liên kết, sau đó 23 sự kiện trong dòng chính chỉ sử dụng chúng để thêm đoạn hội thoại của ký tự được thêm vào | `3E13 48/49/50,0`; điểm đọc của `3E03`/`3E02` |
| Mối liên kết tương tự cũng sẽ thực hiện hai việc: mang lại giá trị kinh nghiệm phi công lớn hơn cho cả hai bên ("căn chỉnh cấp độ"); ghi 12 phi công và 18 đơn vị 64 vào kho lưu trữ GB | `801D975C`, `801D992C`; `801D9B54`, `801D9D70` |

## 2. Quy trình

1. Chọn mục liên kết trên màn hình bảo trì và xác nhận (nhánh `load_0008F4B0:801CE318`, trạng thái màn hình 8). Trước tiên hãy xóa bộ đệm 4 KB (`801D9300`), sau đó gọi `801D93C4` để kiểm tra băng cassette. Chỉ khi trả về 0 thì nó mới vào màn hình liên kết, nếu không nó sẽ vào màn hình lỗi (trạng thái `0x16`).
2. Khởi tạo màn hình được liên kết (`801D6FF4`) gọi quy trình chính `801D5B10`:
1. `801D9544`: Đọc khối dữ liệu GB và xác minh nó (phần 3), sau đó sử dụng `801D975C` để liệt kê các trình điều khiển ở cả hai bên;
2. `801D9B54`/`801D9CF4`, `801D9D70`/`801D9ECC`: Đăng ký phi công và máy bay có sẵn ở dạng 64 nhưng không có GB vào khối dữ liệu. Chỉ cần có phần bổ sung mới, chúng sẽ được ghi lại vào băng cassette trước `801D966C` (Mục 6);
3. Đọc lại khối dữ liệu;
4. `801D9F80`: Xác định tác phẩm nào nên mở và viết lại cấp độ tiếp theo (phần 4);
5. Danh sách tổng số trình điều khiển theo thứ tự giảm dần, 7 mỗi trang.
3. Trình phát xác nhận căn chỉnh cấp độ trong danh sách (`801D70FC` → `801D62D0` → `801D966C`) và kết quả căn chỉnh được ghi lại vào băng cassette (Phần 6).

Bước 2.4 không phụ thuộc vào bước 3: chỉ cần đọc thẻ thành công thì cấp độ tiếp theo đã được sửa đổi trong bộ nhớ và việc căn chỉnh cấp độ tiếp theo có được thực hiện hay không không quan trọng.

## 3. Nhận dạng băng cassette và khối dữ liệu

**Nhận dạng băng cassette** (thường trú `80090F44` → `osGbpakInit`, `osGbpakReadId`; `800910C4` so sánh): 16 byte vùng tiêu đề thẻ phải bằng `S ROBOT LB\0AL6J\x80` (tiêu đề, mã sản phẩm `AL6J`, logo CGB `0x80`), hai byte mã nhà sản xuất phải là `44 39` (ASCII "D9"). Giá trị mong đợi được lưu trữ trong dữ liệu thường trú `800C69E0`.

Giá trị trả về của `801D93C4`:

| Giá trị | Ý nghĩa |
| --- | --- |
| 0 | Là Liên kết Battler |
| 1 | Đầu bài không khớp (không phải Link Battler) |
| 2 | Các lỗi Pak khác (chẳng hạn như Transfer Pak không được chèn) |
| 3 | Pak có ở đó nhưng hộp mực GB chưa được lắp vào (`osGbpakInit` trả về 12) |
| 5 | Giao tiếp không thành công (trả về 4) |

Ý nghĩa của 2, 3 và 5 được suy ra từ hằng số lỗi PFS của libultra và không được so sánh với văn bản trên màn hình lỗi.

**Quyền truy cập SRAM**: Cư dân `80091120` trước tiên ghi `0x01` vào địa chỉ GB `0x6000`, sau đó ghi `0x0A` vào `0x0000` (mở băng cassette RAM). `80091284(读/写, 线性地址, 缓冲, 长度)` chia địa chỉ tuyến tính thành ngân hàng RAM (địa chỉ >> 13, viết `0x4000` để chuyển đổi) và `0xA000` offset trong cửa sổ, đọc và ghi thành các phân đoạn 8 KB. Liên kết sửa địa chỉ tuyến tính đầu vào `0xA000` và độ dài `0x1000`, tức là 4 KB ở đầu ngân hàng 5. Dung lượng SRAM thực tế của Link Battler chưa được kiểm tra và cách số ngân hàng được gói trên hộp mực chưa được xác nhận.

**Định dạng khối dữ liệu** (bộ đệm `801DDAA0`):

| Bù đắp | Nội dung | Người dùng |
| --- | --- | --- |
| `+0x000` | Số ma thuật `ROBOT_TAISENN_GB` (16 byte) | `801DAEAC` Kiểm tra |
| `+0x010` | Bitmap trình điều khiển 64 → GB (12 bit) | `801D9CF4` Viết |
| `+0x018` | 64 → Bản đồ bit nội dung GB (22 bit) | `801D9ECC` viết |
| `+0x020` | Bitmap trình điều khiển được giữ bởi GB (92 bit, tương ứng với số ký tự 64 theo bảng `D_801DCB90`) | Căn chỉnh mức độ, quyết tâm mở |
| `+0x02D` trở lên | Bitmap nội dung do GB nắm giữ | Phán quyết công khai, `801D9D70` |
| `+0x138 + 2i` | GB Giá trị kinh nghiệm của trình điều khiển thứ i, u16 little endian | Căn chỉnh cấp độ |
| `+0x9B9` | Số ma thuật `LINK_BATTLER_V00` (16 byte) | `801DAEAC` Kiểm tra |
| `+0x9C9` | Tổng `0x9C9` byte đầu tiên, u16 little endian | Tính từ `801D98EC` trước khi viết lại |

Khi đọc, chỉ kiểm tra hai số ma thuật đầu tiên và cuối cùng và không kiểm tra tổng kiểm tra.

## 4. Xác định mở: `801D9F80`

1. **Kế thừa liên kết đã lên lịch**: Nếu `8010F5F0` đã là một trong 109-122 (được liên kết trước khi điều chỉnh này), trước tiên hãy hợp nhất vị trí làm việc tương ứng của cảnh vào kết quả này.
2. **64 tác phẩm hiện có**: Quét bảng phiên bản máy của chúng tôi `8016A210` (140 × 0x54), số máy là 42 F91 hoặc 289 ビギナ・ギナ → F91 series; 184 ゴーショーグン, 206ザンボット3 Nguyên tắc tương tự cũng được áp dụng. Các tác phẩm hiện tại không còn được kiểm tra đối với GB.
3. **Điều kiện GB**: Đối với các tác phẩm chưa tồn tại, nếu bất kỳ bit nào sau đây là 1 thì chúng là mở:

| Hoạt động | Bit | Các bit nội dung GB (từ `+0x2D`, byte/mặt nạ) | Bit trình điều khiển GB (từ `+0x20`) |
| --- | --- | --- | --- |
| Dòng F91 | 1 | 3／`0x10`, 16／`0x02` | Vị trí thứ 23 シーブック, vị trí thứ 80 セシリー |
| ゴーショーグン | 2 | 11／`0x40` | Số 55 Shingo |
| ザンボット3 | 4 | 12／`0x08` | Số 59 Shengping |

Ghế lái được xác nhận bằng bảng `D_801DCB90` tương ứng với các vai trò 41, 230, 133 và 152 của 64. Hai vị trí thân xe của dòng F91 được suy ra là F91 và ビギナ・ギナ dựa trên cấu trúc của chúng. Số lượng cơ thể của Link Battler chưa được xác minh. Hằng số nằm trong `D_801DCD04..D_801DCD13`.

4. **Viết lại cấp độ tiếp theo**: Khi kết quả khác 0, nếu cấp độ liên kết cũ không được sử dụng ở bước 1, trước tiên hãy lưu `8010F5F0` vào `8010F5F2`; sau đó nhấn `D_801DCABC` để chọn cảnh và ghi vào `8010F5F0`:

| Vị trí công việc | Cảnh | Tiêu đề |
| --- | --- | --- |
| 1 | 109／110 | F91発jin |
| 2 | 111／112 | ゴーショーグン発jinせよ! |
| 4 | 113／114 | Ổn định 3 xuất hiện! |
| 1+2 | 115/116 | Hội tụ |
| 1+4 | 117／118 | Hội tụ |
| 2+4 | 119／120 | 2つの大きな力 |
| 1+2+4 | 121／122 | 新しきđồng chí |

Việc chọn cảnh trước hay cảnh sau được xác định bởi `801D9F1C`: nếu cấp tiếp theo ban đầu (`8010F5F2` được chọn khi nó đã ở cấp liên kết) nằm trong số 52 cảnh trong bảng `D_801DCAD8` thì cảnh sau sẽ được sử dụng. 52 cảnh này bao gồm từ "Hòa bình giả", "Geki Ka! Rareland" đến "Miền không gian quyết định (Phần 2)". Theo tiêu đề, tất cả họ đều ở trong vũ trụ. Phiên bản trước sử dụng bản đồ 52, phiên bản sau sử dụng bản đồ 114 và bản đồ thế giới lần lượt kết thúc ở vị trí 117 và 122. Do đó, suy ra rằng cái trước là phiên bản mặt đất và cái sau là phiên bản không gian và địa hình chưa được xác nhận trên máy thực tế.

Đối với nhiều liên kết trong cùng một bước chuẩn bị, điểm công việc sẽ chỉ được tích lũy và `8010F5F2` sẽ luôn được dành cho cấp độ tiếp theo trước liên kết đầu tiên.

## 5. Liên kết và theo dõi

Cảnh 109–122 chia sẻ 7 bộ kịch bản (mỗi cặp một bộ) có cùng cấu trúc:

- **Mở**: Chọn điểm bắt đầu và điểm kết thúc của bản đồ thế giới theo chỉ số cảnh hiện tại; chuyển sang chiến trường sau cuộc trò chuyện với nhân vật mới được thêm vào; điều kiện thắng thua là `3D65 17,41`; triển khai nhóm kẻ thù 0, sau đó triển khai nhóm 1 của chúng tôi. Phiên bản có Gatorade cuối cùng thực thi `3D5C 152,1`, kết hợp Gatorade của Katsuhira.
- **Thất bại**: Trò chơi kết thúc khi các nhân vật mới được thêm vào như Seiko (41), Seiko (230) và Shingo (133) bị đánh bại (kích hoạt loại 2).
- **Chiến thắng**: Tiêu diệt toàn bộ kẻ địch → `3D4A`.
- **Kết thúc**: Viết `var48`/`var49`/`var50` = 0 cho các tác phẩm tham gia, sau đó thực hiện `3D4B 500` và khôi phục cấp độ ban đầu tiếp theo từ `8010F5F2`.

Nơi duy nhất mà dòng chính đọc ba biến này là `3E03 变量,0`/`3E02 变量,0` các đoạn hội thoại có điều kiện, chẳng hạn như "Âm thanh của vũ trụ", "Giấc mơ, hãy quay lại", "Cuộc sống, Sanって", v.v.; ở cuối "Giấc mơ, hãy trở lại", Nana sẽ nói một trong 7 câu theo sự kết hợp của cả ba. Không có biến nào trong ba biến kiểm soát việc tham gia nhóm, việc này được hoàn thành khi chúng tôi triển khai thông qua cấp độ liên kết.

## 6. Trao đổi dữ liệu hai chiều

**Căn chỉnh cấp độ** (danh sách `801D975C`, thực thi `801D992C`): Đối với mỗi bit trong bitmap trình điều khiển GB, hãy nhấn `D_801DCB90` để tìm ký tự tương tự trong bảng trình điều khiển `80172F40` (100 × 0x4C). Có hai cặp bí danh trong bảng: 36 アムロ cũng khớp với 262 và 96 ミリアルド cũng khớp với 286 ゼクス. Sự so sánh là giá trị kinh nghiệm của người lái xe `+0x12`:

- GB thấp hơn → ghi giá trị 64 vào khối dữ liệu;
- 64 thấp hơn → Trải nghiệm 64 được đổi thành giá trị GB, cấp độ `+5` được đổi thành giá trị được tính trước trên màn hình liên kết, sau đó khả năng được tính toán lại bằng `800A7F8C`. Đồng đội của máy kết hợp cộng với chênh lệch kinh nghiệm tương tự sẽ được quy đổi thành cấp độ theo trải nghiệm mới trước `800A630C`. Nhóm đồng đội được hiển thị trong bảng `D_801DCA88`: Shinobi (Sara, Ryo, Masato), Leopard Horse (Daisuu, Mizu, Kosuke, Ju) 3), Shengping (恵子, Cosmo Tai), Shingo (キリー, レミー), Malino (ローレンス,アイシャ).

`801D62D0` chỉ có thể căn chỉnh người ở vị trí có con trỏ hoặc căn chỉnh theo đợt theo danh sách `D_801DD5D0` (kết thúc bằng `0xFF`); không có theo dõi về cách điền vào danh sách này. Sau khi xác nhận, `801D966C` tính toán lại tổng kiểm tra và ghi lại vào hộp mực.

**64 → GB**:

- lái xe(`D_801DCC48`, 12 Tên): アーク, セレイン, ブラッド, マナミ, エルリッヒ, リッシュ, カーツ,デューク, マリア, ひかる, キリカ, ナイーダ;
- Nội dung (`D_801DCC78`, 18 trên 22 vị trí Hợp lệ ở Đài Loan): ソルデファー, アシュクリーフ, ノウルーズ, スヴァンヒルド,ラーズグリーズ、シグルーン、スイームルグ、スイームルグS、アルトロンガンダム、ウイングゼロ、ガンダムサンドロック开、ガンダムデスサイズH、ガンダムヘビーアームズ开、グレンダイザー、真・ゲッター1、アースゲイン、スーパーアースゲイン、ヴァイローズ.

Điều kiện là 64 tồn tại trong bảng của chúng tôi, nhưng không tồn tại trong bitmap lưu giữ của GB (`+0x20`/`+0x2D`); khi hài lòng thì viết `+0x10`/`+0x18`. Bỏ qua các vị trí phi công được đánh dấu bằng `0x80` và các phiên bản khung máy bay được đánh dấu bằng `+0xC`. Cách Link Battler sử dụng hai bitmap này không có trong ROM này.

## 7. So sánh với chiến lược

| Tuyên bố của Akurasu | Mã |
| --- | --- |
| Mua thiết bị trong Link Battler, kết nối nó với Transfer Pak và chọn liên kết trên màn hình chuẩn bị | Nhất quán. Điều kiện thực tế là kho GB có vị trí thân xe tương ứng ** hoặc ** ghế lái của nhân vật chính. Một trong hai người sẽ mang theo tất cả các nhân vật và nội dung của tác phẩm |
| Liên kết sẽ làm cho trình độ của các tay lái hai bên ngang bằng nhau | Thống nhất, so sánh và viết lại là điểm kinh nghiệm; người chơi cần xác nhận trong danh sách |
| Cấp độ tiếp theo là cấp độ đặc biệt "Đồng chí mới" giới thiệu các đơn vị mới, sẽ thay đổi theo số lần mở | Nhất quán. "Đồng chí mới" chỉ là tựa đề khi ba trò chơi hoàn thành. Các kết hợp khác là F91発jin, ゴーショーグン発jinせよ!, ザンボット3 xuất hiện!, Confluence, 2つの大きな力; còn có hai phiên bản mặt đất và không gian |
| Trình điều khiển mới được thêm vào được điều chỉnh theo mức lực trung bình | Bản ghi triển khai có trường "bù mức" (0/1) và việc tính toán mức trung bình không được theo dõi trong vòng này |
| BGM và karaoke của các tác phẩm này có thể được sử dụng sau khi mở khóa | Không theo dõi vòng này |

## 8. Yêu cầu chạy hoặc dữ liệu ngoài để xác nhận

- Địa hình thực tế ở cả phiên bản mặt đất và không gian.
- Dòng chữ trên màn hình khi chọn liên kết và nhắc nhở tương ứng với mã lỗi 2, 3, 5.
- 64 "Đã sở hữu" ở đây chỉ nhận biết số máy 42/289/184/206. Nếu tất cả các đơn vị này được bán hoặc rời khỏi nhóm, liệu chúng có được vào lại cấp độ liên kết nếu được liên kết lại không? Liệu Steady 3 có luôn tồn tại dưới dạng phiên bản số 206 trong quá trình bảo trì (thay vì ba thiết bị sau khi tách ra).
- Bản lưu Link Battler có thực sự nằm trong ngân hàng RAM 5 hay không và số lượng bitmap nội dung `+0x2D` hay không. Những thứ này yêu cầu ROM Link Battler hoặc lưu.
- Máy chủ gốc ban đầu không có Transfer Pak và một số quy trình SI/ContRam mà `osGbpakInit` phụ thuộc vào có bẫy hủy bỏ rõ ràng (`funcs_unsupported.c`) trong mã được tạo. Việc chọn chế độ xem tĩnh liên kết sẽ khiến máy chủ hủy bỏ. Hộp mực ảo của Phần 10 thay thế toàn bộ lớp trình điều khiển và các quy trình này không còn được gọi nữa.

`801DA52C..801DAA28` cũng có một bộ chức năng đọc, xác minh và ghi lại thẻ, được điều khiển bởi `801DABE4` thông qua bảng chức năng `D_801DCB10`. Không thể tìm thấy tham chiếu cuộc gọi hoặc địa chỉ tới `801DABE4` trong ROM đầy đủ. Nó có thể là một mục kiểm tra không được kết nối và không được đưa vào quy trình trong bài viết này.

## 9. Ý nghĩa của M2 (khi quy hoạch)

M2 tương ứng với [giải pháp nâng cao gốc](../design/native-enhancements-plan.md):

- **MODEN NỘI DUNG TÙY CHỌN**: Các tập lệnh, triển khai, bản đồ và hội thoại bắt buộc đều có trong ROM, không phụ thuộc vào GB dữ liệu. Ở màn hình chuẩn bị ghi `8010F5F2`/`8010F5F0` theo quy định ở Mục 4 sẽ được xếp vào hàng liên kết. Sau đó, script gốc sẽ hoàn thành việc cộng, ghi các biến và quay về dòng chính. Cách tiếp cận này không liên quan đến giao thức Transfer Pak và sẽ không có sự liên kết cấp độ cũng như khả năng ghi lại 64 → GB.
- **Tương thích với liên kết ban đầu**: Máy chủ cần cung cấp Transfer Pak và mô phỏng `osGbpak*` đọc và ghi SI lớp dưới; lớp dữ liệu chỉ liên quan đến khối dữ liệu 4 KB trong bảng trên, hai số ma thuật và tổng kiểm tra khi ghi lại.

Cuối cùng, cách tiếp cận được áp dụng ở Phần 10 là giữ lại màn hình liên kết ban đầu và chỉ thay thế việc đọc thẻ bằng séc của người chơi.

## 10. Xử lý phiên bản gốc

Được triển khai vào ngày 19-09-2026, biên soạn và vượt qua bài kiểm tra đơn vị, đồng thời kiểm tra trang liên kết, màn hình gốc và quay lại bằng giao diện gỡ lỗi trong cùng ngày (xem phần cuối của phần này).

**Quy trình**: Chọn "リンク" trong menu bảo trì → Trang liên kết gốc (bố cục giống như trang chọn nhân vật chính) → Người chơi chọn tác phẩm → "Nhập liên kết" rồi chạy màn hình liên kết ban đầu (có tổng cộng danh sách trình điều khiển, オートリンク) → B Quay lại menu. Chèn cấp độ liên kết tương ứng trước trận chiến tiếp theo và quay lại dòng chính sau trận chiến, phù hợp với phiên bản gốc. "Trở về" Nhấn đường dẫn của phím B ban đầu để quay lại menu chuẩn bị mà không thay đổi cấp độ tiếp theo.

**Trang liên kết** (`link_page.cpp`, trang RmlUi nằm trong `src/native/ui/frontend.cpp`): ba thẻ công việc, lần lượt hiển thị hình đại diện lớn, tên công việc, cơ thể và hình đại diện nhỏ của phi công đồng hành. ←→ Chuyển đổi, dấu cách/Z hoặc nhấp vào thẻ để kiểm tra, Enter để tiếp tục, Esc/X để quay lại. Thẻ có ba trạng thái:

| Trạng thái | Phán quyết | Hiển thị |
| --- | --- | --- |
| Đã thêm | Biến (48/49/50) là 0, hoặc chúng ta có phần nội dung của tác phẩm này | Nó chuyển sang màu xám và không thể kiểm tra được |
| Đã lên lịch | Cấp độ tiếp theo đã là cấp độ liên kết chứa tác phẩm này | Đã khóa khi đã chọn |
| Tùy chọn | Phần còn lại | Có thể kiểm tra |

"Đã tham gia" xem xét một biến số nhiều hơn phiên bản gốc: phiên bản gốc chỉ nhìn vào phần thân. Sau khi cơ thể được bán và liên kết lại, nó sẽ được nhập lại vào cấp độ liên kết; ở đây, biến sẽ chiếm ưu thế và sẽ không được thêm vào nhiều lần. Avatar của `name_assets.py` từ ROM Bảng avatar (theo số ký tự) đã được giải: シーブック, セシリー, Shingo, キリー, レミー, Shengping, Cosmo Tai, Keiko, trong đó シーブック vàセシリー là 97×97.

**Thời gian**: Việc khởi tạo màn hình liên kết `801D6FF4` sẽ đọc thẻ. Móc không thực thi nó trước tiên mà mở trang liên kết, cập nhật `801D70FC` mọi khung hình và bỏ qua nó trong thời gian chờ đợi. Sau khi người chơi xác nhận, khối dữ liệu sẽ được tạo và sau đó quá trình khởi tạo ban đầu được gọi. Khi hủy, hãy làm theo quy trình xử lý phím B của `801D7148`: phát hiệu ứng âm thanh `0xB8`, viết `801DECB8` thành 0 và gọi `80099814(5,1,2)` để chuyển trở lại menu.

**Cát ảo** (`link_battler.hpp`, `game_hooks.cpp`): 6 chức năng của trình điều khiển thường trú được thay thế: `80090F44` khởi tạo, trạng thái `80090FA0`, `80090FC4` nguồn, `800910C4` so sánh thẻ, `80091120` RAM mở, tất cả đều trả về 0 trực tiếp; việc đọc và ghi `80091284` rơi vào khối dữ liệu 4 KB trong bộ nhớ máy chủ. Nội dung khối dữ liệu:

- Hai con số kỳ diệu ở đầu và cuối;
- Bitmap trình điều khiển và điểm kinh nghiệm phản ánh trình điều khiển của chính người chơi (theo quy tắc khớp của `801D975C`, bao gồm アムロ, ゼクスbí danh), nên danh sách ban đầu xuất hiện như bình thường và căn chỉnh cấp độ sẽ không thay đổi bất kỳ ai;
- Đối với những tác phẩm được kiểm tra nhưng chưa bổ sung, đặt vị trí hoa tiêu chính của chúng (Shingo 23, Shingo 55, Katsuhira 59) và giao lại phiên bản gốc `801D9F80` để phán đoán và định tuyến lại;
- Bốn bit chính của tác phẩm (23, 80, 55, 59) không tham gia phản chiếu và các bitmap nội dung đều bằng 0.

Ghi lại (đăng ký 64 → GB, căn chỉnh mức) chỉ vào bộ nhớ này và không ghi vào đĩa. Máy chủ chẩn đoán không có giao diện gốc (`srw64-host`) chạy theo quy trình ban đầu và khối dữ liệu không chứa bất kỳ bit công việc nào.

**Xác minh máy thật** (2026-09-19, kho lưu trữ giải phóng tập đầu tiên, tuyến Malino, tiếng Trung giản thể): Tải tệp cần chuẩn bị, chọn "リンク" và một trang liên kết sẽ xuất hiện. Cả ba trò chơi đều là tùy chọn. Sau khi kiểm tra F91 và ザンボット3, tiếp tục, màn hình "GB リンク" ban đầu xuất hiện, liệt kê Wanzhang, シモーヌ, マナミ, N64 và GB cả hai bên đều có cấp độ và giá trị kinh nghiệm như nhau; nhật ký sự kiện `linked` dòng `next_scene` từ 4 trở thành 117 ("Confluence" phiên bản mặt đất), `story_scene` là 4. B Quay lại menu và sau đó nhập "リンク", F91 và ザンボット3 hiển thị "đã lên lịch", tiêu điểm đang bậtゴーショーグン; Esc quay lại, quay lại menu bảo trì và con trỏ vẫn ở "リンク", `next_scene` vẫn ở mức 117.

**Đã liên kết xác minh máy thật** (chạy lần thứ hai trong cùng ngày, chạy giới hạn với giao diện gỡ lỗi và chèn tập lệnh được bật cùng lúc): Kiểm tra F91 và ザンボット3, sau đó chọn "Chủ đề" và nhập "Tập 2 "Hợp lưu"" (Cảnh 117, Bản đồ 52 Mặt đất). Sau đoạn hội thoại mở đầu, F91, ビギナ・ギナ và ザンバード/ザンブル/ザンベース xuất hiện về phía chúng tôi và hợp nhất thành ザンボット3 (3 đơn vị bạn, 14 đơn vị địch). Trong giai đoạn của chúng tôi, `3D4E 3D4A` giống như sự kiện tiêu diệt kẻ thù ban đầu được đưa vào. Trận chiến bị bỏ qua và sự kiện kết thúc ban đầu tiếp tục. Sau "…なんとかEndわったようね", người chơi quay lại chuẩn bị và "Tập 2: Hội tụ,クリア" được hiển thị. Tại thời điểm này, các bản ghi sự kiện của trang liên kết `joined=5`, `next_scene=4`, tức là var48 và var50 đã được ghi bằng 0 và cấp độ tiếp theo đã được khôi phục; hai trò chơi trên trang hiển thị "Đã tham gia". "Khả năng luyện tập" liệt kê シーブック (F91, Lv4), セシリー (ビギナ・ギナ, L v3), Kappei (ザンボット3), Kokunta (ザンブル) và Keiko (ザンベース), ba phần sau đều là Cấp 4. "Lần thứ hai" bước vào cảnh 4, và câu mở đầu là "発多はコロニー国であった...", phù hợp với kịch bản của cảnh 4. Cuộc chạy diễn ra bình thường mà không kích hoạt bẫy phá thai.

**Vẫn đang được xác nhận bằng máy thực tế**: Địa hình của phiên bản vũ trụ (cảnh sau); lưu và sau đó tải tệp sau khi lên lịch mức liên kết, xem có nên giữ lại `8010F5F2` hay không; kết quả của trận chiến thực sự đã hoàn tất (chứ không phải là tiêm nhiễm chiến thắng). Xác minh các giao diện gỡ lỗi có sẵn: `srw64ctl wait --link-page`, `status.link_page`, nhật ký sự kiện `link` (`open`, `confirmed`, `linked`, `back`, mỗi dòng có `next_scene` và `story_scene`).

[wiki]: https://akurasu.net/wiki/Super_Robot_Wars/64/Link_Battler_Units