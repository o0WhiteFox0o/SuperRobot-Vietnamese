> **Ngôn ngữ / Language:** [Tiếng Việt](stage-script-exploration.vi.md) · [English](stage-script-exploration.en.md) · [中文](stage-script-exploration.md)

# Kịch bản cấp độ: phân tích lệnh hoàn chỉnh

2026-09-12. Vòng thứ hai đã hoàn thành phân tích tĩnh của máy ảo tập lệnh sự kiện trên phiên bản tiếng Nhật bị khóa của `rom.z64` gốc: độ dài tham số và mối quan hệ phân phối của tất cả 73 vị trí lệnh thông thường, 30 lệnh có điều kiện, 12 điểm đánh dấu ngữ cảnh và 15 loại đăng ký sự kiện đã được so sánh lần lượt với mã máy ROM. Tất cả 1.812 mục nhập sự kiện đã được đọc từ đầu đến dấu kết thúc `FFFF` và không còn sự kiện "dừng ở hướng dẫn không xác định" nào nữa. Người phát ngôn, nhánh tuyến, bản ghi tấn công và điều kiện kích hoạt sự kiện đã được nhập vào thư mục chỉ đọc. **Những điều chưa được thực hiện**: Không có đường dẫn thực thi thực tế của tập lệnh mô phỏng, không có tập lệnh nào được viết lại và không có trò chơi nào bắt đầu với đợt phân tích này để chấp nhận vận hành; hiệu ứng trò chơi của một số hướng dẫn chỉ giữ lại tên kỹ thuật của chuỗi cuộc gọi.

Vòng bằng chứng cấu trúc đầu tiên (con trỏ hai cấp của thư viện sự kiện, cửa sổ DMA, năm từ đầu tiên của sự kiện, `3D45` hỗ trợ chuỗi tiêu thụ bản ghi) tiếp tục hợp lệ và chỉ các phần mới và phần sửa đổi mới được ghi lại ở đây.

## Trích xuất kết quả và đếm

| Cấu trúc | Số lượng | Ý nghĩa |
| --- | ---: | --- |
| Chỉ mục cảnh thư viện sự kiện / Bảng nhập độc lập / Sự kiện độc lập | 142 / 131 / 1.812 | Tương tự như vòng đầu tiên; không phải số cấp độ có thể chơi được |
| Sự kiện trong đó `FFFF` đã được đọc | 1.812 | Chỉ còn lại 0 hoặc 2 byte đệm căn chỉnh sau bộ kết thúc (790/1.022 sự kiện) |
| Hướng dẫn giải mã | 67.160 | Chứa 1.812 đầu cuối; hướng dẫn chưa biết 0 |
| Trích dẫn đối thoại | 33.582 | Số lượng trích dẫn; 30.154 được phân tích trực tiếp bởi người nói, 2.983 được phân tích theo đoạn nhân vật chính và 445 vẫn liên quan đến tuyến đường |
| Khối có điều kiện | 2.678 | Lên đến 5 cấp độ sâu; 29 khối kết thúc bằng `FFFF` thay vì `3E1D`, 15 khối dự phòng `3E1D` |
| Quét sự khác biệt | 0 | Quá trình quét từng từ và phân tích cấu trúc của chương trình gốc có cùng điểm đích (xem các quy tắc nguy hiểm bên dưới) |
| Hồ sơ đồng hành (hồ sơ xuất kích) | 6.223 | 138 khối vật lý, 13 khối không được căn chỉnh trước giới hạn trên 999, byte gốc được giữ nguyên |
| Cảnh dòng chảy cạnh | 148 | Nhận được từ tham số chỉ mục cảnh của `3D4B`, không bao gồm các điều kiện thời gian chạy |
| Cửa sổ bằng chứng mã máy | 80 | Có 22 mặt hàng mới trong đợt này, nằm ở `evidence` của `config/data/original-jp-v1.json` |

Thống kê có thể được tái tạo từ `script_coverage` trong số `assets/original-data/manifest.json`. Các hướng dẫn ROM không bao giờ xuất hiện trong tập lệnh: `3D31`, `3D41`, `3D76`–`3D79`, `3DD8`–`3DDB`, __ INL_CODE_18__, `3E01`, `3E05`, `3E07`, `3E19`, `3E1A`, `3E1C`.

## Cấu trúc máy ảo

Cấu trúc công cụ nằm trong `8015F950` và ngữ cảnh sự kiện được nhúng trong `+0x948` (tập lệnh PC là `+0x964`). Tách biệt việc tìm nạp và thực thi lệnh: `8009EED0` chỉ tăng 2 byte sau khi đọc lệnh 16 bit và ghi hàm xử lý vào `+0x30`. Hàm xử lý được `8009EFDC` gọi lặp đi lặp lại trong mỗi khung hình cho đến khi nó trả trạng thái lệnh `+0x96C` về 0 và đẩy PC thông qua các tham số của chính nó. Do đó, độ dài tham số của mỗi lệnh thông thường là số gia của PC khi chức năng xử lý của nó hoàn thành; lô này được xác nhận chức năng theo chức năng. Nhánh mặc định của bảng phân phối trả về hàm xử lý trống và `3D76/3D77` sẽ tạm dừng sự kiện; mặc dù `3D78/3D79` nằm trong bảng phân phối, nhưng vòng lặp đánh dấu `8009F0E8` sẽ không cho phép các từ của `≥ 3D77` tiếp cận phân phối.

Trước khi tìm nạp, `8009F0E8` trước tiên xử lý hai loại từ cấu trúc:

- **Hướng dẫn có điều kiện `3E00`–`3E1D`** (`8009F228 → 8009F288 → 800A1D68`): `800A1D68` Nhấn `jtbl_800D0890` để gọi hàm điều kiện và hàm này sẽ tự nâng cấp các tham số. Khi nó đúng, hãy tiếp tục; khi giá trị này sai, `8009F288` sẽ quét từng từ từ tham số sau tham số. Lệnh trỏ đến `8009F354` trong `jtbl_800D0638` làm cho lớp lồng +1, `3E1C` cũng +1, `3E1D` tạo lớp lồng −1 và sau khi số lớp được đặt lại về 0, nó sẽ vượt qua `3E1D` và tiếp tục; gặp phải trong quá trình quét `FFFF` thì sự kiện kết thúc. `3E1D` gặp phải trong quá trình thực thi luôn đúng.
- **Thẻ ngữ cảnh `3DD0`–`3DDB`**: với `0x3DD0`, thẻ nhân vật chính hiện tại `+0x99E`, `3DD5/3DD6` bắt nguồn từ nó và `3DD7/3DD8`, kết quả chi được chọn `+0x994` Nếu một trong hai thẻ bằng nhau, bỏ qua và tiếp tục thực hiện; nếu không, hãy quét ngược nguyên văn tới mã thông báo phù hợp hoặc `FFFF`.

Cả quá trình quét đều không biết độ dài tham số. Trong đợt này, các điểm vị trí quét của chương trình gốc được so sánh với từng khối phân tích cấu trúc. Nếu các điểm vị trí khác nhau thì sự khác biệt `skip-scan` sẽ được ghi lại; các tham số nằm trong phần không phổ biến và có giá trị nằm trong `3DD0`–`3DDB`, `3E00`–`3E1D` hoặc `FFFF` được ghi lại `marker-scan-control-word`. Cả hai đều bằng 0 trong tập lệnh ROM. Chín `3D39 FFFF` (dừng hiệu ứng âm thanh) nằm trong phần chung `3DD0` và quá trình quét dấu sẽ không đi qua chúng.

### Thẻ ngữ cảnh

| Đánh dấu | Ý nghĩa | Cơ sở |
| --- | --- | --- |
| `3DD0` | Phần chung, ngữ cảnh nào phù hợp | `s4` trong số `8009F0E8` |
| `3DD1`–`3DD4` | Tuyến Mahmoru | `load_001090A0:801C69D0` Chọn theo nhân vật chính 2/3/0/1 Viết `+0x99E` |
| `3DD5` / `3DD6` | hệ thống リアル (`3DD1/3DD2`) / hệ thống スーパー (`3DD3/3DD4`) | `+0x99E < 0x3DD3` có nguồn gốc |
| `3DD7` / `3DD8` | Nam (`3DD1/3DD3`) / Nữ (`3DD2/3DD4`) | Bắt nguồn từ `3DD8` khi `+0x99E` là `3DD2/3DD4` |
| `3DD9`–`3DDB` | Chọn các mục chi 1–3 | `3D44` Viết `+0x994 = 0x3DD9 + 序号` |

Chức năng tương tự cũng giải thích cho người nói: ba chữ số thập phân đầu tiên của tiêu đề 8 byte của mục nhập văn bản là số ký tự của người nói (`8008CE54`), `25` và `29` được bù lần lượt bởi `+0x99E − 0x3DD1`, tức là "nhân vật chính" và "nhân vật phản diện" thay đổi theo lộ trình: 25 アーク, 26セレイン, 27 ブラッド, 28 マナミ; 29エルリッヒ, 30リッシュ, 31カーツ, 32アイシャ. Những người nói tương đối trong thư mục nằm trong phân đoạn `3DD1`–`3DD4` đã được đặt tên theo các đoạn văn. Hai ứng cử viên được dành riêng cho những người nằm trong phân đoạn `3DD5`–`3DD8` và bốn ứng cử viên được dành riêng cho những người khác. Các chữ số còn lại trong tiêu đề chưa được giải thích bởi bất kỳ chức năng đọc nào và chỉ được giữ lại với văn bản gốc.

### Lệnh có điều kiện

`+0x99C` là thanh ghi so sánh duy nhất (ACC). Lớp câu lệnh luôn đúng và khối không được mở; khi lớp khối là sai, nó sẽ nhảy tới `3E1D` của cùng một lớp.

| Lệnh | Thông số | Ngữ nghĩa |
| --- | ---: | --- |
| `3E00` | 0 | ACC = 0 |
| `3E01` | 3 | Nếu ký tự HP% < ngưỡng và hiện tại, ACC = giá trị (khối mở) |
| `3E02` / `3E03` | 2/3 | Nếu biến ≠ giá trị / Nếu biến = giá trị thì ACC = giá trị 2 (khối mở) |
| `3E04` | 2 | Nếu vòng hiện tại `8010F5EA` < số vòng thì ACC = value (khối mở). Số vòng bắt đầu từ 0 (+1 khi `801D1324` được hiển thị), vì vậy `3E04 N` là đúng ⇔ số vòng màn hình ≤ N (2026-10-01) |
| `3E05` / `3E07` | 0 | Hằng số (bảng nhảy nằm trong dòng −1; khối mở) |
| `3E06` / `3E0D` | 2/1 | ACC được lấy từ danh sách `80172F40` so sánh mục nhập +5 / +0x14; ý nghĩa trường chưa được xác nhận |
| `3E08` / `3E09` / `3E0A` / `3E0B` / `3E0C` | 1 | ACC = / ≥ / ≠ / ≥ / < giá trị (khối mở) |
| `3E0E` / `3E0F` | 1 | biến = (biến ± 1) mod 4 |
| `3E10`–`3E12` | 0 | Chọn kết quả chi = mục 1/2/3 (khối mở) |
| `3E13` / `3E14` | 2/1 | biến = giá trị / ACC = giá trị |
| `3E15` | 1 | ACC = số đơn vị trại (`+0x9B0`–`+0x9B2`, `802018C4` làm mới) |
| `3E16` | 1 | ACC = nhân vật của bên kia cuộc chiến (không bao gồm các ký tự tham số) |
| `3E17`–`3E1A` | 0 | ACC hoặc `+0x998` được lấy từ các trường công cụ, nghĩa là chưa được xác nhận |
| `3E1B` | 1 | ACC = Trạng thái hiện diện của nhân vật: 1 trên bản đồ / 0 bị bắn hạ / 3 không có mặt tại hiện trường hoặc đã rời khỏi bản đồ (rút lui, trốn thoát). `800A1F7C → 800A3990 → 800A293C` Đọc bảng trạng thái `D_8015DE90`: giá trị 0 → 0, giá trị 1 → HP% (1–100 được phân loại là 1), phần còn lại (giá trị ban đầu −1, khởi hành 2) → 3; đường va chạm `801FAFFC` ghi 0, đường khởi hành `8020C664`／`8020CA80`／`8020CFF8` Viết 2 (sửa đổi ngày 2026-10-01, trước đây viết "0 không có ở đây / 3 đã thoát") |
| `3E1C` / `3E1D` | 0 | Bắt đầu khối vô điều kiện / kết thúc khối |

Các biến là 200 giá trị 2 bit (`8015E818`, `800A496C/800A4888`). Khi chơi trò chơi mới, nhân vật chính chọn lớp phủ để điều chỉnh `800A4790` và viết tất cả 26 nửa từ vào `FFFF`, tức là tất cả 200 biến đều là 3 (`load_001090A0:801C69E4`); khi một cấp độ mới bắt đầu, `8009DE7C` đặt 100–114, 128–139 thành 3 và 54 thành 3. 1. Đặt thanh ghi lựa chọn `+0x994` thành `3DD9` (mục 1). `+0x994` chỉ được viết lại bởi `3D44` và được giữ lại trong các sự kiện cho đến hết cấp độ, do đó, khi không có `3D44` thứ hai trong cấp độ, `3E10`/`3E11` kết thúc sự kiện sẽ đọc lựa chọn mở đầu (Được bổ sung vào ngày 01-10-2026).

### Các lệnh thông dụng

Độ dài tham số, chức năng xử lý và cơ sở của 73 vị trí đều được ghi lại trong `commands` của khóa bố cục và trang thư mục `script_opcodes` có thể được kiểm tra từng mục. Các lệnh cốt lõi với ý nghĩa trò chơi đã được xác nhận:

| Lệnh | Thông số | Ý nghĩa |
| --- | ---: | --- |
| `3D38` / `3D39` / `3D3A` / `3D3B` | 1 | Chờ số khung hình / Phát hiệu ứng âm thanh (`FFFF` điểm dừng) / Phát nhạc nền (0 điểm dừng) / Làm mờ hình ảnh |
| `3D3E`–`3D43` | 1 | Đối thoại, sáu chế độ hiển thị; loa đến từ tiêu đề văn bản |
| `3D44` | 3 | Chọn chi (khe cửa sổ, số lượng tùy chọn, văn bản tùy chọn), kết quả nhập `+0x994`; được ghi chú trước đó là "văn bản, số lượng tùy chọn, tham số cửa sổ", đã sửa, xem bên dưới |
| `3D45` | 1 | Triển khai nhóm thu âm hỗ trợ (ra mắt); `8020B154 → 8020ABB4` tạo phần thân và phần thí điểm từ các bản ghi 28 byte |
| `3D46` / `3D4F` | 2/1 | Hiệu suất danh sách đơn vị A/B: Tham số < 500 là vai trò, ≥ 500 là nhóm hỗ trợ (giá trị −500); A được gọi với quá trình xử lý thoát của khu vực đến |
| `3D47` / `3D48` / `3D4E` | 0 | Đóng cửa sổ hội thoại (đợi 32 khung hình/lập tức/nhường 1 khung hình tương ứng) |
| `3D4A` / `3D4B` / `3D4C` | 0 / 1 / 0 | Giải quyết chiến thắng theo cấp độ (→ Màn C3) / Đặt chỉ số cảnh tiếp theo (500 = hồi phục) / Trò chơi kết thúc |
| `3D52` / `3D53` | 3/1 | Bật/tắt các sự kiện đếm độ trễ loại 1 (khe, lượt, chặng) |
| `3D54` / `3D35` / `3D34` | 1/2/4 | Ghi nhớ vị trí ký tự/cuộn đến vị trí (`0x40`–`0x44` liên quan đến vị trí đã nhớ)/chuyển bản đồ và cuộn đến vị trí (số bản đồ, x, y, loại; xác nhận chạy tiêm) |
| `3D57` | 2 | Kích hoạt khe sự kiện đến khu vực loại 8 |
| `3D5B` / `3D62` / `3D6C` | 1/2/2 | Quỹ + Tham số × 1000 / Thay đổi danh tính nhân vật / Đặt số giai đoạn sửa đổi cơ thể (`800ACA1C`: Chỉ tìm phiên bản đầu tiên của số này trong nhóm của chúng tôi, năm vật phẩm và tất cả vũ khí đều được viết `min(N, 上限)`, không hợp lệ nếu không tìm thấy) |
| `3D60` | 3 | Quân ta được bố trí, triển khai theo lưới |
| `3D6D` | 1 | Giai đoạn hiện tại được đặt về phía chúng ta (`8010F5E8 = 1`; giai đoạn số 1 của phe chúng ta / 2 kẻ thù / 3 bên thứ ba, giữa các cấp độ là 0) |
| `3D5A` | 4 | Nhập/xóa danh sách (vai trò, tham số, đơn vị mới, từ 4). Từ 4 `< 2000` → `800AAD28` Đăng ký: Nếu cùng một phi công đã ở trên cùng một máy bay được đánh số, thì không làm gì cả (`3D5A …,500` đăng ký nhiều lần là vô hại); tàu bay 999 chỉ đăng ký phi công (`800A9CF0`), phi công 999 chỉ đăng ký tàu bay; khi có cả hai và danh sách đã có số máy bay `800A9DCC` Xóa phi công ban đầu và để phi công mới tiếp quản, nếu không thì tạo phi công mới; khi ký tự thứ 4 là máy bay cũ sẽ được kế thừa và chuyển đổi theo bảng tiền nhiệm (xem [Kế thừa chuyển đổi](../gameplay/upgrade-inheritance.md)), 500 = Không xóa máy bay cũ. Word 4 `≥ 2000` → `800A3540` Xóa: **2000 chỉ xóa phần thử nghiệm, 3000 chỉ xóa phần nội dung, 4000 xóa cả hai**, bỏ qua xóa khi ký tự là 999 (`800A355C`–`800A35CC`); tất cả 3000 trong tập lệnh gốc được sử dụng làm ký tự Cuộc gọi 999, bằng không hợp lệ (2026-10-01, `800A0B3C`) |
| `3D65` | 2 | Đặt hiển thị điều kiện thắng thua (số chiến thắng, số thất bại) → `engine+0x996`; người đọc duy nhất `load_000AB160:801C68F0` (thông qua `800A3524`) rút ra văn bản **5567 + số chiến thắng** (`801C6918 addiu 0x15BF`) và **5593 + số thua** (`801C6954 addiu 0x15D9`). Chỉ dùng để hiển thị: vượt qua phụ thuộc vào `3D4A`, thất bại phụ thuộc vào `3D4C` hoặc phán đoán phá hủy hoàn toàn của động cơ `801FF934` (2026-10-01) |
| `3D6B` / `3D73` / `3D74` | 3/1/0 | Dấu tách rời: `3D6B 角色,机体,1` Đặt phi công +0 bit 7 và phần thân +0xC bit 6, `…,0` xóa; `3D73 n` đã vượt qua `800AD990` đánh dấu toàn bộ lô theo danh sách đặt trước (n≠0 danh sách A `D_800D06A8`, n=0 danh sách B `D_800D06E4`); `3D74` xóa tất cả. Danh sách ứng cử viên xuất kích `801EBBA8` (được gọi bởi `801C78A0`) bỏ qua các đơn vị của `+0xC & 0x40` (`801EBEDC`–`801EBEE8`), vì vậy người được đánh dấu **tạm thời không thể xuất kích** (ví dụ: cảnh 23 `3D6B` Wan Zhang), được khôi phục sau khi xóa (2026-10-01) |
| `3D6F` | 1 | Mở khóa vũ khí (số vũ khí) |

**`3D44` Sửa thứ tự tham số (17-09-2026). ** Trước đó, tham số 1 được coi là văn bản tùy chọn, do đó thư mục đã liên kết tất cả 46 nhánh lựa chọn với `t00_00000`/`t00_00001` và trang cốt truyện được hiển thị là "đồng bằng/rừng/rừng". Cơ sở mã máy: `8009EED0` Sau khi tìm nạp lệnh, PC đã truyền từ lệnh. Trong khung đầu tiên của `8009FA94`, `lh 0(PC)` (tham số 1) được sử dụng để gọi `8008FF34`. Cái sau lấy tọa độ cửa sổ từ `800C6994`/`800C6996` theo tham số 1×12; sau đó `a0 = lh 0(PC)`, `a1 = lhu 4(PC)` (tham số 3) gọi `8008FF04 → 8008F648(槽位, 文本, 模式 2)`. `8008F648` lưu `a1` vào `s6` và đưa cho `8008CD8C` để vẽ, đường dẫn này giống như đường dẫn xử lý hội thoại `8009F4B4` đi qua `lhu 0(PC)` qua `8008FED4` (chế độ 1); tham số 2 (`lh 2(PC)`) được chuyển tới `8009F3A8` làm giới hạn trên của con trỏ. Kiểm tra dữ liệu: trong 46 vị trí, tham số 1 chỉ có 0 (44 vị trí) và 1 (2 vị trí). Tham số 3 tiếp tục các số hội thoại trước và sau (chẳng hạn như sự kiện cảnh 026 `001A6DE8`: hội thoại 21812–21814 theo sau là `3D44 [0, 2, 21815]`, `t00_21815` là "シーラのsquare へdirectional かう / エレのsquare へdirectionalかう") và số `<BR>` dòng của 46 văn bản bằng tham số 2. Văn bản tùy chọn là văn bản được phân nhánh bởi `<BR>`, không phải nhiều ID văn bản liên tiếp; mục lục và trang cốt truyện đã được xây dựng lại cho phù hợp.

Các lệnh còn lại (`3D31`–`3D33` Hiển thị bản đồ thế giới, `3D36`/`3D49`/`3D50`/`3D55`/__INL_CODE_26 0__/`3D5C`/`3D63`/`3D67`/`3D68`/`3D75` Đang chờ hiệu suất bản đồ, `3D5D`/`3D70` và các hoạt động danh sách khác; `3D5A`, `3D6B`/`3D73`/`3D74` được liệt kê trong bảng trên) Độ dài tham số và mục tiêu cuộc gọi đã được xác nhận, `semantic_confidence` được đánh dấu là `structure-confirmed` hoặc `unknown`, tên dành riêng cho mô tả kỹ thuật. Hai trong số năm tham số đầu tiên của `3D3D` không được đọc bởi mã thường trú, tham số thứ ba của `3D56` không được đọc và tham số của `3D5F`/`3D6D` không được đọc nhưng vẫn chiếm 2 byte.

Phần bổ sung đang chạy: `3D3C` đã được sửa thành "Đơn vị di chuyển đến vị trí(người lái, vị trí)", tham số đầu tiên được liên kết với hồ sơ người lái xe và mức độ tin cậy là `structure-confirmed`. Năm lệnh gọi mở đầu của siêu hệ thống nam được hiển thị trong [Quan sát thông số gốc](script-3d3c-runtime.md); [Kiểm soát tham số đơn](script-3d3c-experiment.md) tiếp theo xác nhận sự thay đổi mục tiêu tuyệt đối và tọa độ bảng phân công ghi lại. Các ranh giới như vị trí tương đối, va chạm và nhiều đơn vị có cùng số lượng vẫn được chấp nhận.

## Các loại đăng ký sự kiện và điều kiện kích hoạt

`8009DE7C` đăng ký loại 0–11 thành 12 nhóm phân loại (mỗi nhóm 16 mục) và 12–14 vào `engine+0x8/0xC/0x10`. `8009E180` gọi `8009E3B0` theo giai đoạn thăm dò `+0x9AA` khi trạng thái sự kiện không hoạt động và `engine+4 = 0xC0`, đồng thời mỗi nhóm hàm kích hoạt được cung cấp bởi `jtbl_800D0610` (`8009E308`). Ý nghĩa của các từ 2–5 trong tiêu đề sự kiện được giải thích theo loại:

| Loại | Điều kiện kích hoạt | Thông số tiêu đề | Bỏ phiếu |
| ---: | --- | --- | --- |
| 0 | Bắt đầu vòng đấu | Số vòng (vòng hiện tại ≥; giá trị ban đầu tính từ 0, vòng màn hình = giá trị gốc + 1), giai đoạn (= `8010F5E8`) | Giai đoạn 0 |
| 1 | Số lần trễ (bắt đầu bằng `3D52`, giảm dần `+0x97E[槽]` mỗi vòng) | Ghi đè thời gian chạy | Giai đoạn 0 |
| 2 | Đơn vị do nhân vật điều khiển bị đánh bại/rút lui | Biến ngưỡng (không được kích hoạt khi 100–115 và bằng 3; được đặt thành 3 ở đầu mỗi cấp từ 100–114 và được bật bằng cách viết 0 trong tập lệnh), ký tự | luôn |
| 3 | Nhân vật HP% ≤ ngưỡng | Ký tự (138 trường hợp đặc biệt: HP < 11), phần trăm | Luôn luôn |
| 4 | Sự kiện đính hôn (sau trận chiến) | Ký tự A, Ký tự B (0 = bất kỳ) | Giai đoạn 7, mã trạng thái `0x2002` |
| 5 | Sự kiện đính hôn (trước trận chiến) | Nhân vật A, Nhân vật B | Giai đoạn 4, mã trạng thái `0x2001` |
| 6 | Tất cả kẻ thù đều bị tiêu diệt (`+0x9B1 = 0`) | Vòng mới nhất (vòng hiện tại được kích hoạt khi ≤ giá trị này; vòng bắt đầu từ 0, vòng màn hình = giá trị + 1; 254 = không giới hạn; `8009E834`; trong ROM đầy đủ, chỉ `001B42E4` của cảnh 45 sử dụng 4), giai đoạn (4 = bất kỳ) | Luôn luôn |
| 7 | Số phe còn lại ≤ N | Lựa chọn phe phái (2 = bên thứ ba, nếu không là kẻ thù), N, giai đoạn, biến ngưỡng (quy tắc tương tự như 2) | Luôn luôn |
| 8 | Khu vực đến (yêu cầu bật `3D57`) | Vòng hoặc chế độ (`FF` kích hoạt khi vào; `FE` Mỗi người tham gia sẽ rút khỏi bản đồ ngay lập tức và trại 0 sẽ chỉ kích hoạt khi tất cả trại 0 rút lui), N×1000+mục tiêu, x0×10+chiều rộng, y0×10+chiều cao (phạm vi `[x0, x0+宽)`, xem bên dưới) | Giai đoạn 0/1/2/6 |
| 9 | Thuyết phục: `800A4634` Vị trí đã chọn được ghi vào `+0x992` | Người thuyết phục, đối tượng, biến ngưỡng (`FFF8` không có ngưỡng) và giá trị ngưỡng; người thuyết phục cũng có số hành động, slot chưa thực hiện, đã đạt ngưỡng, “đã nói” chỉ xuất hiện khi cả hai bên đứng cạnh nhau trên, dưới, trái, phải và người đầu tiên được lấy theo thứ tự đăng ký; khi thực thi, `8009EC3C` thay đổi vị trí thành `0x2000`, cấp độ này không còn khớp | Chức năng xử lý được gọi ở giai đoạn 0/1/2/6 và chỉ được thực thi ở giai đoạn 6 (được đặt bởi lệnh "Shuode" `801DEBF4`) |
| 10/11 | Đăng ký nhưng không bình chọn | — | Không có |
| 13/12/14 | Mở (C1)/Cấu hình ban đầu (C2)/Kết thúc (C3, sau `3D4A`) | — | `8009EDB8` |

Nguồn giai đoạn: `load_000AB160:801DF96C` ghi số vòng, giai đoạn và đơn vị của ba phe vào công cụ trước trận chiến và đặt giai đoạn 4, `801DF9F8` đặt 7 sau trận chiến, `801DEBF4` đặt 6, `8020DB08` đặt lại vòng về 0 khi vượt qua cấp độ và đặt `engine+4` thành C3. Trình tự loại 4/5 được đánh giá theo thứ tự mã trạng thái được xử lý bởi `801DFEA8`, được đánh dấu là xác nhận cấu trúc; mã nhập C2 vẫn chưa được xác định, nhưng nội dung của bảy sự kiện loại 13 đều là những triển khai ban đầu của `3D45`. Khớp khu vực loại 8 nằm trong `800A4288`: mục tiêu < 500 cho nhân vật, hơn 500 trại cho bất kỳ đơn vị nào của trại đó, 21 cho danh sách đội trưởng `D_800C9A08` (ブライト, シーラ, エレ, Tiến sĩ Hazuki, エマリー,ヘンケン...) là người đầu tiên có mặt, tức là hạm trưởng của chúng tôi. Mã hóa của từ vùng là `x0 = 值 / 10`, chiều rộng = `值 % 10`, bao trùm `[x0, x0 + 宽)`, y giống nhau; ở chế độ `FE`, các đơn vị vào khu vực sẽ được rút theo hiệu suất thoát ra và sự kiện sẽ chỉ được thực hiện khi tất cả trại 0 rút lui (bổ sung 2026-10-01, chức năng tương tự).

Tập đầu tiên của Siêu Nhân Nữ (Chỉ số Cảnh 1) được hiểu như sau: Đối thoại mở đầu Loại 12 → Nhóm Triển khai Loại 13 0–2 → Tiếp viện khi địch còn ≤ 8 / ≤ 6 (Nhóm 3, Nhóm 4) → Kết thúc đối thoại khi địch còn 0 → Loại 2 (Malna bị đánh bại) → Sự kiện Kết thúc Loại 14; `3D4B` Chỉ vào cảnh 4. Đây là cách giải thích tĩnh, phù hợp với bằng chứng chạy gốc hiện có (xóa tập đầu tiên), nhưng trò chơi chưa được ra mắt trong đợt này.

2026-09-12 Phụ lục đang chạy: Trò chơi siêu loại dành cho nữ mới thực sự thực hiện các nhóm triển khai 0–2 trong sự kiện khai mạc `0019C1B0` và không quan sát thấy việc thực thi riêng biệt các sự kiện loại 13. Mối quan hệ sự kiện trong đoạn trên là một suy luận tĩnh và không thể được coi là một chuỗi đo lường thực tế. Bạn có thể tìm thấy kết quả tương ứng đầy đủ của 123 lệnh thông thường/đối thoại trong [Quan sát hoạt động im lặng](script-runtime-observation.md).

## Hồ sơ hỗ trợ (hồ sơ tấn công)

Dữ liệu hỗ trợ mà `3D45` sử dụng là luồng bản ghi 28 byte (14 nửa từ), kết thúc bằng từ đầu tiên 999. Thứ tự đọc của `8020ABB4` cung cấp các trường: số nhóm +0, tọa độ lưới +2/+4 (`3D3D → 801C78A0` xoay màn hình ở ×16+32), +6 vai trò phi công (sử dụng lại khung máy bay đã được chỉ định trong danh sách khi < 287), +9 mức bù (mức = `8010F5F3` + offset), +A khung máy bay, +C Chỉ số gia cố (`800CB5DC` → năm giai đoạn chuyển đổi), căn chỉnh +14 (3 → 0, 4 → 2), +16/+18 tham số hành vi (+18 ghi trình điều khiển +0x14 khi bit 14 được đặt). +8, +E–+13, +1A Không giải thích được. Chuỗi ghi vị trí xuất kích đã được xác nhận bởi cấp nhỏ (2026-09-17, xem [cấp nhỏ](mini-stage.md)): `3D3D` lấy tọa độ lưới của bản ghi đầu tiên của nhóm làm điểm tham chiếu và đơn vị được chọn để xuất kích hoặc xuất kích tự động được đưa vào ô bản đồ trống gần điểm tham chiếu bởi `801C835C`, khe `+0xB` Lưu ý nhóm số.

Một danh mục `stage_deployments` mới (6.223 mục) đã được thêm vào thư mục, mỗi mục liên kết nội dung, ký tự và khối tương ứng; trang cảnh liệt kê các nhóm và bản ghi tương ứng được tham chiếu bởi tập lệnh. 13 khối không có căn chỉnh 999 được cắt bớt ở giới hạn trên và không thêm dấu kết thúc.

## Tiêu đề chương và trình xem cốt truyện

Nâng cấp trình đọc 12-09-2026: Đã thêm tính năng tìm kiếm toàn văn bản, liên kết sâu theo từng câu, đoạn hội thoại nhỏ gọn, khả năng phân biệt người nói màu xanh/cam, tùy chọn đọc và xử lý hình đại diện tương ứng với tuyến đường. Bạn có thể tìm thấy mức sử dụng, phạm vi dữ liệu và các bước kiểm tra hiện tại trong [Trạm đánh giá kịch](story-reader.md) và quy trình xác nhận từng mục cho các lệnh còn lại có thể được tìm thấy trong [Kế hoạch xác nhận ngữ nghĩa](script-semantics-confirmation.md). Bản ghi xác minh lịch sử và triển khai phiên bản đầu tiên được giữ lại bên dưới.

Màn hình chuẩn bị `load_0008F4B0:801CE0F8` sử dụng chỉ mục cảnh vừa xóa `8010F5F1` cộng với 281 làm số văn bản để hiển thị tiêu đề chương và danh sách lưu trữ `801C6944/801C754C` sử dụng cùng một công thức cho byte cảnh đã lưu (bằng chứng `stage_title_display`). Do đó, tiêu đề của chỉ số cảnh n là văn bản `281 + n`: Cảnh 0 "戦え!热き血のファイターたち", 1 "出撃!スイームルグ", 4 "Tức giận"りの甲児魔神立つ!"... Số 143 ứng cử viên danh hiệu (423) không có cảnh tương ứng và vẫn được đánh dấu là ứng cử viên. Tiêu đề cảnh và chương trong Mục lục hiện được liên kết với nhau.

`tools/data_viewer/web/story.html` sử dụng những dữ liệu này để tạo trình xem cốt truyện: cột bên trái liệt kê tiêu đề chương và số câu theo chỉ mục cảnh, còn cột chính mở rộng phần mở đầu, cấu hình ban đầu, sự kiện chiến trường (với bản tóm tắt các điều kiện kích hoạt) và sự kiện kết thúc theo thứ tự nhập sự kiện; mỗi dòng hội thoại hiển thị người nói, hình đại diện gốc 96×96 và văn bản gốc tiếng Nhật (`<BR>` ngắt dòng, `<STOP>` Hiển thị dưới dạng dấu chuyển trang) và số văn bản; các đoạn tuyến đường của nhân vật chính được hiển thị dưới dạng nhãn đoạn văn, bốn nhân vật chính có thể lọc; Các lời nhắc của hệ thống như khối điều kiện, các chi đã chọn, nhóm xuất hiện và BGM có thể bị ẩn. Mã thông báo tên động được thu gọn thành phần giữ chỗ (chẳng hạn như [Tên nhân vật chính], [Biệt hiệu đối tác]). Dữ liệu được ghi bởi `src/srw64_native/original_story.py` tới `story/index.json` và `story/NNNN.json` trong quá trình trích xuất; nó chỉ chứa văn bản gốc tiếng Nhật và các đoạn tuyến đường cũng như khối điều kiện không được đánh giá, do đó, một cảnh sẽ liệt kê văn bản nhánh của bốn tuyến đường cùng một lúc mà không lọc theo đường dẫn trò chơi thực tế.

## Triển khai và tái tạo

- Khóa bố cục và bằng chứng: `stage_scripts` (lược đồ `srw64.stage-script-layout.v2`) của `config/data/original-jp-v1.json` và 22 bằng chứng mới; Khi giải nén `verify_vm_tables` kiểm tra lần lượt mã máy của bảng phân phối, bảng nhảy có điều kiện, bảng quét và bảng kích hoạt. Nếu bất kỳ chức năng xử lý nào không khớp, thế hệ sẽ bị từ chối.
- Trình phân tích cú pháp: `src/srw64_native/original_scripts.py`, được gọi bởi `tools/content/extract_original.py`; tiêu đề văn bản được cung cấp bởi `srw64_native.catalog.text_headers`. Chế độ xem câu chuyện: `src/srw64_native/original_story.py`, kiểm tra `tests/test_original_story.py`.
- Trang: `tools/data_viewer/web/scripts.js`. Danh mục mới `stage_deployments`, `script_conditions`, `script_markers`, `script_event_types`; các trang sự kiện được thụt lề theo mức độ lồng nhau, các điểm đánh dấu được hiển thị dưới dạng đoạn văn, các diễn giả hiển thị hộp thoại và các trang cảnh hiển thị các thông số kích hoạt, luồng tuyến đường và các nhóm tấn công.
- Kiểm tra: `tests/test_original_scripts.py`, bao gồm việc không đồng bộ hóa lệnh không xác định, vượt quá giới hạn tham số, khối và điểm đánh dấu có điều kiện, phát hiện sự khác biệt khi quét, quy tắc của loa, từ chối giả mạo mã máy, sắp xếp lại tất cả byte sự kiện, điều kiện kích hoạt tập đầu tiên và liên kết vị trí cũng như tính nhất quán của byte bản ghi tấn công.

```sh
PYTHONDONTWRITEBYTECODE=1 make check
.venv/bin/python -B tools/content/extract_original.py
python3 -B tools/data_viewer/serve.py --port 59110
```

Lô `make check` này đã vượt qua 90 bài kiểm tra, kiểm tra tổng hợp và kiểm tra phần phụ thuộc (`build/original-data-qa/logs/original-data-check-scripts2.log`). Sau khi tạo lại thư mục, hãy kiểm tra kích thước của 7.758 tệp đầu ra với SHA-256, 70.043 danh tính duy nhất và 202.670 liên kết thư mục, tất cả đều đã đóng (`build/original-data-qa/verification-scripts-v2.json`, nhật ký bản dựng `build/original-data-qa/logs/original-data-extract-scripts2.log`). Trình duyệt đã kiểm tra chỉ số cảnh 1, sự kiện 0019C3BC, lệnh có điều kiện 3E03 và trang bản ghi xuất kích: các tham số kích hoạt, chuỗi lệnh thụt lề, liên kết loa, luồng tuyến và các nhóm xuất kích đều hiển thị như mong đợi và không có lỗi trong bảng điều khiển. Lô này là trích xuất tĩnh và xác minh trang phát triển và trò chơi chưa được bắt đầu.

Sau khi thêm trình xem cốt truyện và tiêu đề chương: `make check` vượt qua 95 bài kiểm tra (`build/original-data-qa/logs/original-data-check-story.log`); thư mục được tạo lại có tổng cộng 7.904 tệp, 70.044 danh tính và 203.238 liên kết đều đã được kiểm tra và thông qua, `story/` có 143 tệp; 142 cảnh đều có tiêu đề và chế độ xem cốt truyện có tổng cộng 7.904 tệp, 70.044 danh tính và 203.238 liên kết. Có 34.369 dòng hội thoại (các cảnh có kịch bản chia sẻ được tính riêng), 30.753 dòng được người nói phân tích trực tiếp, 3.058 dòng được phân tích theo đoạn văn, 123 dòng được phân chia theo nhân vật chính của tập đầu tiên và 435 dòng vẫn liên quan đến lộ trình. Tất cả các đoạn hội thoại của người nói được phân tích cú pháp đều có tệp hình đại diện. Kiểm tra trình duyệt `story.html` Cảnh 1: Tiêu đề "DEPU! スイームルグ", tập tiếp theo, nhân vật chính của tập này, hình đại diện, diễn giả, trình lật trang và lời nhắc BGM đều được hiển thị chính xác và không có lỗi trong bảng điều khiển (`build/original-data-qa/verification-scripts-v2.json`).

## Chưa hoàn thành

1. Xác minh chạy: Thêm theo dõi tập lệnh im lặng (chỉ mục cảnh, mục nhập sự kiện, PC, hướng dẫn thực hiện thực tế) vào tập đầu tiên và so sánh nó với diễn giải tĩnh của lô này; đây là ngưỡng trước khi kết quả phân tích có thể được sử dụng để thay thế một sự kiện duy nhất có thể phục hồi được.
2. Các lệnh có ngữ nghĩa cần được phân tích cú pháp: chức năng lớp phủ lớp hiệu suất bản đồ (máy trạng thái sau `80209DAC`), thao tác bảng phân công `800AA464/800AA62C/800AAD28`, `3E06/3E0D/3E17`–`3E1A`, trường công cụ và trường bảng phân công được tham chiếu.
3. Đường dẫn vào sự kiện loại 13 (điểm ghi của `engine+4 = 0xC2`). (Điểm ghi của chỉ mục loại 9 `+0x992` đã được giải quyết: `800A4634`, được gọi bằng cách xây dựng menu `801C9DFC` và thực thi "Đã nói" `801DECE8`, 2026-10-01.)
4. Mục đích của năm chữ số sau tiêu đề văn bản và giá trị thực tế của tuyến đường liên quan đến người nói trong phân khúc chung (yêu cầu thời gian chạy `+0x99E`).
5. Sơ đồ luồng cảnh chỉ phản ánh tham số `3D4B` và không bao gồm nguồn thời gian chạy của `500` (khôi phục); trình xem cốt truyện chưa thể xếp nhánh theo lộ trình thực tế và không có bản dịch tiếng Trung.