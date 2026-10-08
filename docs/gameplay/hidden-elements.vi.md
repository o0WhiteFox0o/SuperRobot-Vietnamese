> **Ngôn ngữ / Language:** [Tiếng Việt](hidden-elements.vi.md) · [English](hidden-elements.en.md) · [中文](hidden-elements.md)

# Yếu tố tiềm ẩn, tính thuyết phục và sự khác biệt về lộ trình: triển khai tập lệnh và mã

2026-10-01, vòng xác minh tĩnh toàn diện thứ hai. Đối tượng bị khóa phiên bản tiếng Nhật Rev 0 `rom.z64`: **tất cả 1.812 sự kiện** của tập lệnh IR (`assets/original-data/records/stage_events.jsonl`) được quét lần lượt (khối điều kiện, phân đoạn nhân vật chính và bộ phận, chọn chi, ngưỡng tiêu đề loại 2/7/9) và các quyết định liên quan được đọc vào mã thường trú (`build/recomp/cpu-scan/resident/`) và lớp phủ (chiến thuật `load_000AB160`, chiến đấu `load_00121560`, giữa các cảnh `load_0008F4B0`, bản đồ thế giới `load_000A7EC0`, lựa chọn nhân vật chính `load_001090A0`). Những phần "chưa thấy trước", "không được kiểm tra" và "suy ra" còn sót lại từ vòng đầu tiên (17/09/2026) đều đã được đổi thành kết luận mã hoặc kịch bản. **Trò chơi chưa được chạy trong vòng này và cũng chưa được ghi lại vào ROM**; kết luận đã được quyết định nhưng những điểm đáng xem xét lưu lại đều tập trung ở Mục 10.

Hướng dẫn cộng đồng [Akurasu Wiki: Super Robot Wars/64/Secrets][wiki] chỉ được sử dụng để so sánh chứ không phải là cơ sở cho Sơ đồ quy trình của nó. Phần 6 xác định **Nhất quán**, **Khác biệt**, **Không bao gồm Akurasu** theo từng mục; Phần 7 và 8 lần lượt tóm tắt hai loại sau.

Quy ước viết:

- `S49` là số cảnh (id tiêu đề cấp − 281) và tên cấp là tên tiếng Nhật gốc được ROM giải mã, giúp bạn dễ dàng tìm kiếm trên trình duyệt dữ liệu.
- Địa chỉ sự kiện là offset ROM (chẳng hạn như `001bf55c`), `@520` là offset lệnh trong sự kiện.
- **Các vòng đấu luôn được ghi dưới dạng vòng màn hình** (các con số trên HUD của trò chơi). Giá trị gốc trong script bắt đầu từ 0, xoay màn hình = giá trị gốc + 1, xem Mục 4.1.
- `varN` đề cập đến biến tập lệnh 2 bit N.

## 1. Tóm tắt kết luận

- Trò chơi không có hệ thống phần tử ẩn chuyên dụng. Tất cả các điều kiện được triển khai bằng cách sử dụng 200 biến tập lệnh 2 bit (`8015E818`): 0–54 được lưu theo các cấp độ, là tiến trình của các tính năng và tuyến đường ẩn; 100–139 là các biến tạm thời một cấp. **Trong trò chơi mới, tất cả 200 biến được đặt thành 3** (`800A4790`, mã thực tế), vì vậy 3 thường có nghĩa là "chưa bắt đầu/không thành công".
- **Điều kiện thuyết phục được ghi trong tiêu đề sự kiện loại 9**: `[9, 说服者, 对象, 门槛变量, 门槛值]`, `FFF8` nghĩa là không có ngưỡng. Hàm thường trú `800A4634` có nhiệm vụ kiểm tra, lựa chọn: người thuyết phục là người điều khiển chính của đơn vị hành động, sự việc chưa được thực hiện, đã đạt ngưỡng, hai bên liền kề lên, xuống, trái, phải và bên thứ nhất được lấy theo thứ tự đăng ký. Chuỗi ngưỡng cho tất cả 71 sự kiện thuyết phục được đọc ra (Phần 3).
- Các biến ngưỡng loại 2 (bị đánh bại) và loại 7 (số người sống sót) **không được kích hoạt** khi bằng 3; từ đầu tiên trong tiêu đề loại 6 (tiêu diệt tất cả kẻ thù) là vòng **mới nhất**; `3E04 n` bằng "vòng màn hình ≤ n" (phần 4).
- Bảng biến hoàn chỉnh đến 0-54 với đầy đủ các điểm ghi và hiệu ứng đọc của từng biến; 45, 53 và 54 được đọc bằng mã gốc (Màn hình gương Shisui, cột mốc Pháo đài バルジ, đường hạ gục hạm), 46 không có tác dụng thực tế (phần 5).
- So sánh từng mục của khoảng 60 mục trên trang Bí mật Akurasu (Phần 6): 30 điểm khác biệt trong kết luận (Phần 7), và hơn 40 điều kiện, bất đồng và kết quả không có trong Akurasu (Phần 8, bao gồm cả những khám phá mới N1–N17 từ bản quét toàn bộ).
- Kỹ năng kết hợp không được mở khóa thông qua cốt truyện: `8020178C` Mỗi khi một loại vũ khí được liệt kê, vị trí khóa của kỹ năng kết hợp sẽ được viết lại. `3D6F 1215` (Đôi ngón tay của Chúa) không có tác dụng lâu dài; Sky Shocking Fist của Ishiba cũng yêu cầu Ishiba's Shocking Fist đã được mở khóa (phần 6.5).
- Hai mục duy nhất còn lại thực sự không có tính thuyết phục về mặt tĩnh học (Phần 10.1).

## 2. Cơ chế thực hiện

### 2.1 Biến

| Lệnh | Chức năng |
| --- | --- |
| `3E13 变量, 值` | Viết |
| `3E0E` / `3E0F` | Cộng 1 / Trừ 1 (modulo 4), dùng làm bộ đếm |
| `3E03 变量, 值[, v]` / `3E02 变量, 值` | Nhập khối điều kiện khi bằng/không bằng |
| `3E10`–`3E12` | Nhấn thanh ghi lựa chọn (mục 1/2/3) để vào khối điều kiện |

Biến chỉ có 2 bit và một thừa số có thể có tối đa bốn vị trí. Cách sử dụng phổ biến: `0`, `1`, `2` biểu thị tiến trình, `3` biểu thị chưa bắt đầu hoặc không thành công.

**Giá trị ban đầu (mã thực tế)**: Nhân vật chính chọn `load_001090A0:801C69D0` để gọi `800A4790`, viết 26 nửa từ bắt đầu từ `8015E818``0xFFFF` (`800A479C`–`800A47C4`) và tất cả 200 biến đều là 3.

**Đặt lại sau khi nhập** (`8009DE7C`):

| Đối tượng | Đang xử lý | Bằng chứng |
| --- | --- | --- |
| var100–114, var128–139 | Đặt thành 3 | Vòng lặp `8009E06C`/`8009E09C` |
| var54 | Đặt thành 1 | `8009E0C4` |
| Chọn đăng ký `engine+0x994` | Đặt `3DD9` (mục 1) | `8009E04C` |
| Số slot thuyết phục `engine+0x992` | Đặt thành −1 | `8009E020` |
| 12 nhóm sự kiện | Xóa và đăng ký lại | `8009DEC4`–`8009DEFC`, `8009DF3C` trở đi |

var115–127 không nằm trong phạm vi đặt lại và các tập lệnh không bao giờ đọc hoặc ghi vào chúng (var117–122 cũng được sử dụng bởi mã gốc, xem Phần 5.2). var55–99, var140–199 không có lần đọc hoặc ghi nào trong tất cả 1.812 sự kiện.

**Chọn thanh ghi**: Trong mã lưu trú, chỉ `3D44` được viết lại thành `engine+0x994`, được giữ lại trong một cấp độ và được lưu trữ trong kho lưu trữ ngắt (`800A47D4`) cùng với các biến. Vì vậy, khi chỉ có một mở đầu `3D44` trong một cấp độ, `3E10`/`3E11` của sự kiện ở cuối cấp đọc lựa chọn mở đầu (ví dụ: S138 Cardo rời đội, S32 hoàn toàn yên bình).

### 2.2 Nguồn phán đoán

| Nguồn | Thực hiện | Ví dụ điển hình |
| --- | --- | --- |
| Thuyết phục | Sự kiện loại 9, tiêu đề có ngưỡng; biến tiến trình được ghi trong sự kiện | アイナ, フォウ, プルツー |
| Chọn chân tay | `3D44` rồi sử dụng các nhánh `3E10`–`3E12` | シーラ／エレ、エリカ、ナイーダ |
| Hạ gục được chỉ định | Kích hoạt đánh bại loại 2 + `3E16` (ACC = phía bên kia của trận chiến) + `3E08 角色` | カーツ（ブラッド）、キラル（ドモン） |
| Số lần tiêu diệt/cấp độ | `3E0D` (số lần tiêu diệt), `3E06` (so sánh cấp độ) theo sau là `3E09`/`3E0B`/`3E0C` | Ginling, シルキー, フォウ |
| Tương tác | Loại 4/5 (sau/trước trận); `3E17` Đọc "Chúng ta có nên hành động trong trận chiến này không?" | アイナ (tham gia trước), ガラリア (hủy) |
| Hiện tại | `3E1B`: 1 trên bản đồ, 0 bị bắn hạ, 3 không hiện diện hoặc còn sót lại | ロザミア, プル, シュバルツ |
| Sinh tồn, khu vực, rẽ, HP | Loại 7, Loại 8, Loại 0/`3E04`, Loại 3 | アイシャ, ガトー, trò chơi đột phá quyết tử |

Xem Phần 4 để biết ngữ nghĩa chính xác của từng loại kích hoạt và lệnh có điều kiện.

### 2.3 Sự kiện thuyết phục (loại 9)

Loại 9 thiên về thuyết phục. Hai từ cuối cùng của tiêu đề sự kiện `[9, 说服者, 对象, 门槛变量, 门槛值]` là điều kiện tiên quyết (thư mục `trigger.fields` đánh dấu tất cả bốn từ là "dành riêng" nên chúng không được nhận dạng ở vòng đầu tiên). Việc kiểm tra và lựa chọn được thực hiện bởi cư dân `800A4634`, được gọi bởi lớp phủ chiến thuật ở hai nơi: xây dựng menu lệnh (`801C9DFC`) và thực thi "say it" (`801DECE8`). Quá trình thực thi được hoàn thành trước `8009EC3C` trong giai đoạn thăm dò sự kiện 6. Sau khi thực thi, trạng thái vị trí thay đổi thành `0x2000` và cấp độ này không còn khớp nữa; dấu thực thi được lưu cùng với kho lưu trữ ngắt. Cấp độ chéo "Bước thứ N yêu cầu bước N-1" được thực hiện hoàn toàn bằng biến ngưỡng. Xem Phần 3 để biết cơ chế hoàn chỉnh.

### 2.4 Trường bản ghi trình điều khiển

| Lĩnh vực | Kết luận | Cơ sở |
| --- | --- | --- |
| `+5` | Cấp độ | `3E06` → `800A22CC` (ACC = !(Cấp A < cấp B)) → `800A32C0`／`800A32EC` Tìm cái đầu tiên trong ba bảng trình điều khiển theo số vai trò, lấy `+5` |
| `+0x14` | Số lần tiêu diệt | `3E0D` Tổng cộng có 6 vị trí, bài đọc là kiệt tác ×2, Malik ×2, ブラッド, ngựa báo; tiền thưởng quỹ tiêu diệt `801F66C8` cũng sử dụng `+0x14 ≥ 20` làm số lần tiêu diệt |

Hai mục này trong khóa bố cục `conditions` vẫn được viết là "Danh sách [vai trò]+0x14/+5" và sẽ được đổi tên riêng.

### 2.5 Tham gia, rời đi và chuyển giao

| Chỉ thị | Ngữ nghĩa | Bằng chứng |
| --- | --- | --- |
| `3D5A 角色, 参数, 机体, 模式` | Đăng ký chế độ 500; `< 2000` thể hiện số máy bay cũ, tức là chuyển nhượng; 2000 chỉ xóa driver; 3000 chỉ xóa máy bay; 4000 xóa cả hai. Khung máy bay 999 = Chỉ có phi công được đăng ký; Ký tự 999 = Chỉ đăng ký khung máy bay, bỏ qua khi xóa. Không làm gì nếu cùng một phi công đã ở trên cùng một máy bay (không có hại gì khi đăng ký hai lần). 3000 trong kịch bản gốc đều được gọi với vai trò 999, tất cả đều không hoạt động | `800A0B3C`, `800AAD28`, `800A3540` |
| `3D58 角色, 阵营` | Chuyển các đơn vị có mặt đến trại được chỉ định và tham gia cùng họ ngay tại chỗ (ガラリア, ヒルデ, アイシャ); các bộ phận rơi ra ở ô mới sẽ bị xóa khi chuyển trại | `80210758` → `802106FC` |
| `3D45 组` | Triển khai nhóm ghi chép hỗ trợ xuất kích. Ghi lại giá trị trại 0/3 rơi vào nhóm của chúng tôi và người lái xe sẽ tham gia trực tiếp vào nhóm nếu < 287 (các cấp độ đầu không có `3D5A`); 2/4 là bên thứ ba | `8020ABB4`, `8020B154` |
| `3D59 角色` | Không được phép tấn công ở cấp độ này | |
| `3D6B 角色, 机体, 1／0` | Đặt/xóa dấu "không tấn công"; `3D73 n` được đặt theo đợt theo danh sách cư dân, `3D74` bị xóa tất cả | `801C78A0` |
| `3D6C 机体, N` | Năm vật phẩm và tất cả vũ khí của đơn vị đầu tiên trong nhóm của chúng tôi được đặt thành `min(N, 上限)` | `800ACA1C` |
| `3D64 500, 500` | Đặt nhân vật làm phi công thứ hai của cỗ máy hiện tại (アイシャ thay thế ローレンス) | `800AB96C` |
| `3D70 主驾驶, 同乘者` | Đi chung (`3D70 186,182`: シルキー được gắn vào máy トッド) | |
| `3D6F 武器` | Xóa phiên bản vũ khí `+0x22` bit 2 (đã mở khóa); không có tác dụng lâu dài đối với các kỹ năng kết hợp, xem phần 6.5 | |
| `3D5B n` | Vốn + n×1000 | |

## 3. Cơ chế thuyết phục

### 3.1 Điều kiện để "Shuoda" xuất hiện trong menu lệnh

**Trình điều khiển chính** của đơn vị con trỏ cũng có số lượng hành động (trình điều khiển `+0x35 ≠ 0`; di chuyển nó là được) và một loại 9 vị trí nhất định được đăng ký ở cấp độ này cũng đáp ứng:

1. Ký tự đầu tiên trong tiêu đề (người thuyết phục) bằng mã số vai trò của phi công chính của đơn vị;
2. Vị trí không được thực thi (trạng thái `< 0x2000`) và hiện không có sự kiện nào đang thực thi (`engine+0x97C < 0x2000`);
3. Đạt ngưỡng: từ thứ ba là `FFF8` hoặc `var[第 3 字] == 第 4 字`;
4. Đơn vị có từ thứ 2 (đối tượng) nằm trên bản đồ (bất kỳ trại nào cũng được, chỉ cần khớp với bất kỳ người lái xe nào trên đơn vị đối tượng) và liền kề với người thuyết phục **lên, xuống, trái và phải** (khoảng cách Manhattan chính xác là 1, các hướng chéo không được tính).

Bằng chứng: Xây dựng menu `load_000AB160:801C9DFC`. `801C9EB8`–`801C9EC8` Viết số vai trò lái xe chính vào `engine+0x9A8` (`D_801602F8`) và gọi `800A4634`; khi giá trị trả về là ≠ −1 và số lượng hành động còn lại là ≠ 0, hãy thêm mục menu `D_8021DD88` (lệnh 1, văn bản `0x1FF` "nói tốt"). Mục `移動` cũng yêu cầu nó chưa được di chuyển, vì vậy bạn đừng xem nó.

### 3.2 Lựa chọn `800A4634`

Gói loại 9 có tại `engine+0x6F8` (cơ sở gói `engine + 0x14 + 类型×0xC4`). Trong nhóm: `+0` số mục; `+4` 16 con trỏ sự kiện; đối tượng `+0x44[i]`; người thuyết phục `+0x64[i]` (đổi thành `0x2000` sau khi thực hiện); `+0x84[i]` biến ngưỡng; Giá trị ngưỡng `+0xA4[i]` (đăng ký `8009DFA0`–`8009DFE8`).

Hàm lặp theo thứ tự đăng ký, lấy vị trí đầu tiên đáp ứng các điều kiện của 3.1, ghi số vị trí vào `engine+0x992` và trả về số vai trò của trình điều khiển chính của đối tượng; nếu không có, hãy viết −1 (`800A475C`). Biến đọc ngưỡng chuyển sang `800A2A84 → 800A496C` (chỉ số dưới ≥ 0xC9 trả về −1); các mục trong danh sách của cả hai bên được tra cứu bởi `800A2BF4 → 800A2C18` (vị trí ở trạng thái 2 của chúng tôi bị bỏ qua); so sánh liền kề nằm trong `800A4704`–`800A4738`.

Vì vậy, đối tượng thuyết phục được xác định bởi chương trình và người chơi không thể lựa chọn: khi cùng một người thuyết phục dính vào hai đối tượng có thể thuyết phục cùng một lúc, anh ta sẽ chỉ thuyết phục được đối tượng đứng đầu danh sách. Ví dụ: Trong Common Battle Line (S61)/Brothers and Brothers (S76), khi Yukari bám theo cả Matsuda và Matsuda cùng lúc, anh ta sẽ chỉ thuyết phục được Matsugat; Trong アクシズの Tấn công và Phòng thủ (Trước) (S88), khi ジュドー được gắn vào cả マシュマー và キャラ, nó sẽ chỉ thuyết phục được マシュマー.

### 3.3 Trường tiêu đề sự kiện

| từ | trường trong nhóm | ý nghĩa |
| --- | --- | --- |
| w1 | `+0x64` | Mã số vai trò thuyết phục (phải là động lực chính của đơn vị hành động); sau khi thực thi sẽ đổi thành `0x2000` |
| w2 | `+0x44` | Số vai trò đối tượng |
| w3 | `+0x84` | Số biến ngưỡng; `0xFFF8` (−8) nghĩa là không có ngưỡng |
| w4 | `+0xA4` | Giá trị ngưỡng: biến == giá trị chỉ xuất hiện "đã nói" |

Trong số 71 sự kiện, có 24 sự kiện không có ngưỡng và 47 sự kiện có ngưỡng. Các biến ngưỡng 2, 3, 6, 9, 11, 12, 13, 14, 15, 18, 22, 24, 26, 27, 29, 30, 32 được sử dụng, cũng như các biến cấp đơn 128 và 129.

### 3.4 Quá trình thực thi và tiêu thụ hành động

1. Lệnh menu 1 → `801DECE8`: điều chỉnh lại `800A4634`, viết `+0x992`, chọn hiệu ứng đặc biệt 0x35/0x36 theo tọa độ của cả hai bên, `801EE838` phát hiệu ứng đặc biệt định hướng và trạng thái được đặt thành 0x52.
2. `801DF22C` Đợi cho đến khi hiệu ứng đặc biệt kết thúc → `801DEBF4`: Trạng thái được đặt thành 0x53, `D_80172F0A = 1`, giai đoạn bỏ phiếu `engine+0x9AA` (`D_801602FA`) = **6**, ghi tay cầm thuyết phục.
3. Kiểm tra vòng sự kiện `8009E180` sử dụng `8009E3B0(8,10)` trong các giai đoạn 0, 6, 1 và 2 cho loại bỏ phiếu 8 và 9. Chức năng xử lý loại 9 `8009EC3C` (`jtbl_800D0610[9]`) chỉ được thực thi khi `+0x992 ≠ −1` và `+0x9AA == 6`: trạng thái vị trí được thay đổi thành `0x2000`, `+0x97C = 0x2000`, `8009EE98` Trong sự kiện khởi động, `+0x992` được đặt lại về −1.
4. Sau sự kiện, quá trình kiểm tra `801DFF40`–`801DFF7C` hoàn tất và `801DEC68` được gọi: `+0x9AA` trở về 0, `801C29DC(说服者)` trừ một hành động và quay lại bản đồ.

Một lần thuyết phục tiêu tốn một hành động của người thuyết phục, bất kể nội dung sự kiện có hiệu quả hay không.

### 3.5 Thuyết phục nhiều bước, xuyên cấp và lưu trữ

- **Cấp độ bên trong**: Các slot đã thực hiện không còn trùng khớp nữa, lần thuyết phục tiếp theo của cùng một cặp nhân vật sẽ tự nhiên rơi vào slot tiếp theo đạt ngưỡng. Biến ngưỡng của bước thứ hai được viết bởi sự kiện của bước đầu tiên. Ví dụ: Nỗi buồn しみのホンコンシティ フォウ ×2, 戦いの意は ミネルバX ×2, ランタオ岛／Tuyệt vọngドモン→レイン.
- **Cấp chéo**: Đăng ký lại khi bắt đầu mỗi cấp, dấu thực thi sẽ không vượt cấp. Giới từ cấp độ chéo chỉ dựa vào các biến ngưỡng (var0–54).
- **Lưu trữ bị gián đoạn**: `80093278 → 80091ED0 → 800A4148` lưu trữ các vị trí có trạng thái `0x2000` trong 12 nhóm vào `D_8016A1F0` từng chút một. Việc thuyết phục đã được thực hiện sau khi tiếp tục trò chơi vẫn được coi là đã được thực hiện.
- Mỗi nhóm có tối đa 16 slot (`8009DF8C`); cảnh có sự kiện thuyết phục nhất (S57, S66) chỉ có 4.

### 3.6 Việc kiểm tra không thành công cũng sẽ tiêu tốn: sự thuyết phục một lần

`8009EC3C` đánh dấu vị trí là `0x2000` trước khi thực thi và khối điều kiện trong sự kiện chỉ xác định hướng dẫn nào sẽ thực thi. Vì vậy:

| Sự kiện | Điều kiện thất bại | Hậu quả |
| --- | --- | --- |
| ロザミア（S41 `001b15cc`） | ゲーツ vẫn còn đó (`3E1B ゲーツ` = 1) | Chỉ có đoạn hội thoại được phát và vị trí duy nhất ở cấp độ này được sử dụng |
| プル（S85 `001cff84`） | グレミー có mặt (chỉ tham gia sau ≠ 1) | Chỉ đối thoại |
| プル（S98 `001dad58`） | グレミー chưa bị bắn hạ (chỉ tham gia sau == 0) | Chỉ phát đoạn hội thoại |
| プルツー（S132 `001d47fc`） | グレミー** không có trong ** (chỉ đăng ký nếu == 1) | Chỉ đối thoại |
| Sự kiện trống bên ngoài đoạn tuyến đường | Nội dung sự kiện chỉ được viết ở một phân đoạn nhân vật chính/bộ phận nhất định và vẫn có thể được bắt đầu ở phía bên kia | Vị trí đã được sử dụng và không có gì được thực thi (`8009F0E8` bỏ qua các phân đoạn không khớp) |

Các sự kiện trống bên ngoài các đoạn tuyến đường: エマ `001a2124` (siêu đoạn), キリマンジャロ フォウ`001c7768`／`001c7790` (đoạn thực),キリカ（マリア）`001cc108`／`001d6374` (siêu phân đoạn), エルリッヒ`001b1514`／`001b6ba4`（アークphần）、アイシャ`001ad258`／`001b6464`／`001b6c40`（マナミphần）、リッシュ`001b8928` (phần セレイン). Bản thân người thuyết phục chỉ giới hạn ở nhân vật chính và không có tác dụng thực sự; "Nói" sẽ xuất hiện ở ba nơi: クワトロ→エマ(hệ thống thực), カミーユ→フォウ(siêu hệ thống S57), và Marika → キリカ (hệ thống thực), nhưng sẽ không có tác dụng sau khi thuyết phục.

### 3.7 Không có tác dụng thuyết phục ở cấp độ code

`800A4634`, `801DECE8`, `801DEBF4`, `8009EC3C`, `801DEC68` không ghi trạng thái trại, danh sách hoặc cấp độ của đơn vị mục tiêu. Thoát (`3D46`), vượt qua thành tích (`3D4F`), chuyển về phía chúng tôi (`3D58`), đăng ký (`3D5A`) và chiến thắng cấp độ (`3D4A`) đều được hoàn thành bằng kịch bản sự kiện. Trong số tất cả 71 sự kiện, chỉ có một sự kiện trực tiếp kết thúc cấp độ: Hazama Yuu của Biển và Đất (S20) Bước thứ ba của フォウ `001a4420@512 3D4A`.

### 3.8 Tất cả các chuỗi thuyết phục

"Ngưỡng" là tiêu đề w3/w4; phần "ghi" chỉ liệt kê các biến và hướng dẫn để thay đổi tình huống.

| chuỗi | sự kiện (kịch bản): ngưỡng → viết |
| --- | --- |
| アイナ | `0019f2cc` (S11): var128==0 → var12=0, exit (var128 chỉ được viết 0 bởi sự kiện trận chiến loại 5 `0019f2a8` giữa シロー và アイナ) → `001a6368` (S24): var12==0 → var12=2, exit |
| ゲイル | `0019fc28` (S12): Không có → Phá vỡ hiệu suất, var0=0 |
| エマ | `001a2124` (S16): Không → Siêu phân đoạn var1=0, thoát |
| フォウ | `001a344c` (S18): Không → var2=0; `001a347c` (S18): var2==0 → var2=1, thoát; `001a43f4` (S20): var2==0 → Chỉ đối thoại; `001a4420` (S20): var2==1 → var2=2, `3D4A`; `001b4b58` (S128): var2==2 → Khe trễ khởi động 3 (so sánh mức, ghi var17); `001c7708` (S57): var2==2 → Phá vỡ hiệu suất, var17=0; `001c7768`/`001c7790` (S57): var2==0/1 → đoạn thực var128=0 |
| アレンビー | `001a34e8` (S18)/`001a3cac` (S19): Không → Thoát, nhóm 8, var3=0; `001b4cfc` (S128)/`001c7884` (S57): var3==0 → Thoát, var3=1; `001d32dc` (S129 ドモン): var128==0 → var128=1; `001d32fc` (S129 レイン): var128==1 → trận chiến kịch bản, var128=2; `001d7cac` (S137ドモン): var129==0 → 1; `001d7ccc` (S137 レイン): var129==1 → Thoát, var129=2 |
| トッド | `001a6ad4` (S25): Không → var6=0; `001ac1a8` (S33)/`001bd924` (S47)/`001acc08` (S62): var6==0 → var6=1 |
| アイシャ | `001ad258` (S34): Không → var13=0; `001af7e8` (S38): var13==0 → 2; `001b6464` (S65): Không → 0; `001b6c40` (S66): var13==0 → 1; `001c6134` (S56): var13==0 → 2 |
| ヒルデ | `001af71c` (S38): Không có → `3D58` chuyển về phía chúng tôi, var16=0 |
| リッシュ | `001af760`（S38）／`001b8928`（S69）：var14==1 → var14=2 |
| エルリッヒ | `001b1514` (S41): var9==0 → var18=2; `001b6ba4` (S66): Không → `3D58` chuyển cho chúng tôi, var18=2; `001bfaf0` (S49): Không → Thoát, var18=0; `001c6094` (S56): var18==1 → Thoát, var18=2 |
| ロザミア | `001b15cc` (S41): var15==0 → Thoát, đăng ký, var15=1 khi không có ゲーツ |
| マーグ | `001b42b8`（S45）／`001c8384`（S59）／`001bb31c`（S75）／`001bbfdc`（S136）：Không có → var22=0; `001c94e4` (S61)/`001b7af0` (S76): var22==0 → var22=1; `001cb548` (S77): var22==0 → var25=0 |
| ロゼ | `001c9878` (S61)/`001b7e38` (S76)/`001cb870` (S77): var26==0 → var26=1; `001d5ba4` (S91)/`001d3dd8` (S130): var26==1 → Thoát, var26=2 |
| ナイーダ | `001b4370`（S45）／`001c9938`（S61）／`001b7e60`（S76）：Không → Thoát, var23=0 |
| キリカ | `001cc0d8`（S78）／`001d6344`（S92）デューク：Không → var24=0；`001cc108`（S78）／`001d6374`（S92）マリア：var24==0 → Siêu hiệu suất phá vỡ phân đoạn, var24=1 |
| ミネルバX | `001b68f8` (S66): Không → var128=0; `001b6928` (S66): var128==0 → AI thoát, var128=1 |
| プル | `001cf998` (S84): Không → Thoát, var27=0; `001cff84` (S85): var27==0 → Khi không có グレミー `3D58`, var27=1; `001dad58` (S98): Không → Khi グレミー bị bắn hạ var27=1, `3D58` |
| プルツー | `001d0e84`（S141）／`001db848`（S99）：var27==1 → var30=0；`001d1438`（S87）／`001dc174`（S100）：var30==0 → var30=1; `001d47fc` (S132): var30==1 → đánh bại màn trình diễn khi có グレミー, đăng ký, var30=2; `001dc7a4` (S101): var30==1 → var30=2, thi đấu thất bại, đăng ký |
| マシュマー／キャラ | `001d17c0` (S88): var29==0 → var32==0, var29=1, var32=3; `001d17ec` (S88): var32==0 → var29==0, var32=1, var29=3 |
| ミリアルド | `001cf654` (S84): Không; `001dfa00` (S103): var11==0. Cả hai chỉ có lời thoại |

Tổng cộng có 71 sự kiện; để biết danh sách từng mục (bao gồm các đoạn văn và bản tóm tắt của tất cả hướng dẫn trong sự kiện), hãy xem bản thảo xác minh vòng hai `persuade.md`.

## 4. Ngưỡng kích hoạt và vòng

### 4.1 Đếm vòng

`D_8010F5EA` là số vòng, **bắt đầu từ 0**: thêm 1 khi HUD chiến thuật được hiển thị (`load_000AB160:801D1324`/`801D1338` gọi `sprintf` sau `addiu a2,a2,1`); `801DF994`/`801DF9A4` sao chép nó vào `engine+0x9AC`; `801FA9D8` Thêm 1 vào cuối lượt. Bản ghi thực tế của máy `docs/script/mini-stage.md` cũng xác nhận là 0 ở vòng đầu tiên.

**Lật màn hình = giá trị gốc + 1**. "Số vòng = N" được trình đọc tập lệnh in luôn tăng thêm 1.

### 4.2 Ngữ nghĩa tiêu đề của loại trình kích hoạt

| Loại | Tên | Tiêu đề và phán đoán | Mã |
| --- | --- | --- | --- |
| 0 | Bắt đầu vòng đấu | `[0, 回合, 阶段]`: `engine+0x9AC ≥ 回合` và các pha bằng nhau. Giá trị gốc N = **Bật N+1 của màn hình** | `8009E598` |
| 1 | Đếm độ trễ | Bắt đầu bởi `3D52 槽, N, 阶段`: số đếm được đặt thành N và vòng cuối cùng được ghi là `0xFD`; cuộc thăm dò đầu tiên chỉ ghi lại vòng hiện tại và được giảm đi 1 cho mỗi vòng tiếp theo và được thực thi khi nó bằng 0 và các giai đoạn khớp với nhau (4 = tùy ý). Chỉ thăm dò ý kiến ​​tại `engine+0x9AA == 0` (bắt đầu giai đoạn, kết thúc mỗi hành động và quay về trạng thái không hoạt động). Số vị trí = chuỗi đăng ký của các sự kiện loại 1 ở cấp độ này. Số đếm bắt đầu trong sự kiện khai mạc, sau N vòng thay đổi, là **Lượt N+1 của màn hình** | `800A05D0`, `8009EB5C`, `8009E180` |
| 2 | Đánh bại/rút lui | `[2, 门槛变量, 角色]`. Biến ngưỡng không kích hoạt khi 100–115 và giá trị == 3; 0 = không có ngưỡng | `8009E604` |
| 3 | HP bên dưới | `HP/最大HP×100` (thả nổi, giới hạn dưới 1) **λ** có ngưỡng và đơn vị | `8009E6E4` |
| 4/5 | Sau/Trước trận chiến | Hai nhân vật được ghép với kẻ tấn công hoặc người phòng thủ (0 = bất kỳ), thứ tự tấn công và phòng thủ không liên quan gì; vũ khí bản đồ không kích hoạt (con trỏ phòng thủ là 0) | `8009E9B4`, `8009EA88` |
| 6 | Tất cả kẻ thù đều bị tiêu diệt | Từ đầu tiên trong tiêu đề là vòng **mới nhất**: giá trị ban đầu < vòng hiện tại không được kích hoạt; 254 có nghĩa là không có giới hạn. Full ROM chỉ S45 `001b42e4` dùng 4 (trong vòng 5 màn) | `8009E834` |
| 7 | Tàn dư phe phái | `[7, 阵营选择, 上限, 阶段, 门槛变量]`: Chọn phe 2 = bên thứ ba (`+0x9B2`), nếu không thì là kẻ thù (`+0x9B1`); **được kích hoạt khi số người sống sót ≤ giới hạn trên**; không được kích hoạt khi giá trị biến ngưỡng == 3 | `8009E8B4` |
| 8 | Khu vực đến | Mã tọa độ `x0 = 值/10`, chiều rộng = `值%10`, phạm vi `[x0, x0+宽)`, y giống nhau. Mục tiêu 21 = người chơi đầu tiên trong danh sách đội trưởng `D_800C9A08` (chủ lực của chúng tôi), 500 = bất kỳ đơn vị nào của chúng tôi. Chế độ `FF`: Được kích hoạt khi có đơn vị tiến vào; Chế độ `FE`: Mỗi đơn vị tham gia sẽ rút lui khỏi bản đồ ngay lập tức và nó chỉ được kích hoạt khi tất cả trại 0 rút lui | `800A4288` |
| 9 | Thuyết phục | Xem Phần 3 | `8009EC3C` |
| 12／14 | Mở đầu/kết thúc chương | | |

### 4.3 Lệnh có điều kiện

| Chỉ thị | Ngữ nghĩa | Mã |
| --- | --- | --- |
| `3E04 n` | `D_8010F5EA < n`, tức là ** vòng màn hình ≤ n** | `800A2344` |
| `3E1B 角色` | 1 = trên bản đồ; 0 = bị bắn hạ; 3 = không có mặt tại hiện trường hoặc đã rời khỏi bản đồ (rút lui, trốn thoát). Bảng trạng thái `D_8015DE90`: Ghi 0 cho đường va chạm `801FAFFC`, ghi 2 cho đường xuất phát `8020C664`/`8020CA80`/`8020CFF8` (đọc là 3), giá trị ban đầu −1 (đọc là 3). Số "0 vắng mặt/3 đã thoát" ghi trong thư mục là không chính xác | `800A1F7C → 800A3990 → 800A293C` |
| `3E16 角色` | ACC = số ký tự của bên kia | |
| `3E17` | ACC = `engine+0x9B6`: Bên tấn công là phe ta → 1; bên phòng thủ là phe của chúng ta và phản ứng không phải là phòng thủ/né tránh → 1; nếu không thì 0. Cũng viết 1 khi bên tấn công của vũ khí trên bản đồ là bên của chúng ta | Viết `801F3F88`, `801FE794` |
| `3E15 阵营` | ACC = số đơn vị trong trại này | |
| `3E0D 角色`／`3E06 A, B` | Số lần tiêu diệt/so sánh cấp độ, xem phần 2.4 | `800A22CC` |

Phương pháp viết thành ngữ: `3E14 v` hoặc `3E03 变量, 值, v` trong khối đặt ACC làm dấu hiệu "khối này đã được thực thi" và `3E0A v`/`3E08 v` tiếp theo là "else"/"then" của khối này.

### 4.4 Quy ước chuyển đổi các biến ngưỡng

100–114 được đặt thành 3 khi nhập cấp độ, do đó, loại ngưỡng 2/7 sẽ kích hoạt **đóng theo mặc định** và tập lệnh sử dụng `3E13 10x, 0` để mở và `3E13 10x, 3` để đóng. Ví dụ: Nắm đấm tuyệt vọng và nỗi buồn (Sau) (S137) `001d7c94` Sau khi viết var100=0, `001d7da8` có thể được kích hoạt khi giá trị còn lại ≤ 10; Tuyệt đẹp なるル・カイン (S14) Viết đầu tiên khi quân du kích đến khu vực trốn thoát var100–102=3 Tắt cò súng của chính bạn trước khi thoát ra. Thư mục (`trigger.fields`) ngược lại với "biến ngưỡng phải là 3" được đánh dấu trong tập lệnh đọc cũ.

### 4.5 Điều kiện thắng thua

`3D65 胜, 败` viết `engine+0x996` và người đọc duy nhất của `load_000AB160:801C68F0` (thông qua `800A3524`) được hiển thị là "win = text 5567+v, loss = text 5593+d". Nó chỉ hiển thị: vượt qua phụ thuộc vào tập lệnh `3D4A`, thất bại phụ thuộc vào tập lệnh `3D4C` hoặc phán đoán phá hủy hoàn toàn của chính động cơ (`801FF934`, `3D61` có thể bị tạm dừng).

## 5. Bảng biến tiến trình

### 5.1 Các biến cấp độ chéo 0–54

“Viết” theo thứ tự xuất hiện; "Đọc và hiệu ứng" chỉ liệt kê các lần đọc làm thay đổi sự hình thành, hình thành, tấn công, xử lý hoặc hành vi bản địa. Đối với các điểm đọc chỉ thay đổi dòng, xem Phần 5.3.

| Biến | Mục đích | Viết | Đọc và hiệu ứng |
| --- | --- | --- | --- |
| 0 | ゲイル | Thuyết phục S12 `0019fc28@170` → 0 | 0 → S32 Đăng ký phân đoạn thực ở cuối cấp ゲイル＋グライムカイザル (`3D6C` 3 phân đoạn); Mở S52/S53 Đăng ký giai đoạn thực ở cuối đường chuyền (4 giai đoạn); S83/S93 đăng ký lại và cấm tấn công; S83/S131/S93/S94 đổi thành Yuru làm hộ tống (N5) |
| 1 | エマ | S16 đoạn thực mở → 0; Thuyết phục S16 (siêu phân khúc) → 0; Mở S43/S44, S46 cuối cấp độ thực → 0 (lặp lại) | 0 → Khe trễ S16 Đăng ký siêu phân đoạn 1 エマ＋ガンダムmkⅡ; S17 Đoạn thực mở đầu được đăng ký là エマ＋ジェガン (1 đoạn); S26 siêu loại ==3 khi カミーユ cưỡi mkⅡ xuất hiện |
| 2 | フォウPhần đầu | S18 Thuyết phục → 0 → 1; Thuyết phục S20 → 2 | Ngưỡng thuyết phục (S18/20/128/57); 2 → S128 Khai cuộc カミーユ không thể tấn công (ở hiệp 3 màn hình hoặc khi địch ≤8 thì lấy Z đến), S57カミーユ không thể tấn công; Nhóm tăng cường địch S57 nhấn ==2 để chọn |
| 3 | アレンビー | thuyết phục S18/S19 → 0; thuyết phục S128/S57 → 1; S129 cuối pass var128==2 → 2; S137 hết đèo → 1 (được giải cứu) hoặc 3 | Ngưỡng thuyết phục; 1 → S128/S57 Khi kết thúc cấp độ, đăng ký アレンビー＋ノーベルガンダム; S129/S137 mở ra sự thuyết phục khi ∈{0,1}; S137 ≠1 khi kẻ điên cuồng xuất hiện; S41 hết cấp ==1 → `3D6F 1215` (không có tác dụng lâu dài) |
| 4 | ガラリア | Khe trễ S20 1 `001a41a4@136` → 0 (đồng thời `3D58`) | 0 → S33/S48/S63 Mở đăng ký lại "Đảm bảo lập trình" (không có hiệu lực khi đã lập trình); シルキー điều kiện; S20フォウ thoát ở bước thứ ba |
| 5 | エリカ | S23 Lựa chọn cuối cùng Mục 1 → 0 (mỗi cái một cho ブラッドdan và マナミdan) | Chỉ thay đổi dòng |
| 6 | トッド | thuyết phục S25 → 0; thuyết phục S33/S47/S62 → 1; S81/S92 bị bắn hạ → 3; S81/S92 không xuất hiện ở cuối cấp → 3 | Ngưỡng thuyết phục; 1 → S81/S92 Bên ta triển khai トッド ở vòng 3 màn hình |
| 7 | シーラ／エレ | S26 Chọn 1 → 0 ở đầu, chọn 2 → 1 | Bản đồ S26 và đội ngũ của chúng tôi; S33 (IA) Bên không được chọn xuất hiện giữa chừng và bị loại khỏi cùng cấp; S62 Đăng ký ở đầu, S63 bị loại bỏ ở cuối cấp (CP); S48 xuất hiện, bị loại khỏi mức tương đương (OZ); 100 dòng còn lại |
| 8 | Rura (phía trước) | S27 Ba lựa chọn mở → 0/1/2 (hệ thống thực) | S30 Quyết định khai mạc var9 |
| 9 | chi nhánh レラ | Mở S30 → 0/1 (xem phần 6.1); Mở S63 ==0 → 3 | S42 Mối quan hệ thực sự ở cuối đường chuyền ==0 → S43; S41 エルリッヒ ngưỡng thuyết phục; Lô mở S140; hơn mười câu thoại |
| 10 | phía OZ | S30 kết thúc màn, chọn 1 → 1, chọn 2 → 0 | S123/S124 ==1 → S57; S137 kết thúc giai đoạn ==1 → chọn một trong những νガンダム được sản xuất hàng loạt; Nhóm địch S103/S104/S105 |
| 11 | Hòa bình trọn vẹn | S32 Chọn mục 3 ở đầu → 0 (một cho mỗi nhân vật trong số bốn nhân vật chính); S32 Chọn 3 ở cuối cấp độ rồi chọn 2 → 1, nếu không → 0 | S32 Hết cấp ==1 → S62; S123/S124 ==0 → S42; FA Trăm Shika Kai; S103 hết cấp ==0 → ノイエ・ジール; Khai mạc S84 ==1 → ドロシー nhóm 14; S103 thuyết phục ngưỡng ミリアルド; Nhóm địch S103/S104/S105. OZ không qua S32, giữ 3 |
| 12 | アイナ | thuyết phục S11 → 0; S24 siêu đoạn mở → 0; Thuyết phục S24 → 2 | ngưỡng thuyết phục; 2 → S24 kết thúc đăng ký vượt qua アイナ＋アプサラス |
| 13 | アイシャ | IA: Thuyết phục S34 → 0, Thuyết phục S38 → 2, S40 còn lại ≤9 khi Marino không có mặt → 3; CP: S65 → 0, S66 → 1, S69 → 2; OZ: S49 chọn 1/2 → 0, S50 chọn 1 ở cuối pass → 0, S56 Thuyết phục → 2 | Ngưỡng thuyết phục; 2 → S40 `3D58` (IA), S69 `3D58` (CP), S57 Đăng ký đăng ký (OZ); スイームルグS thời gian chuyển giao; S57 マナミ không thể tấn công |
| 14 | リッシュ | S35/S65 Trước trận đấu, chọn 1 → 0, chọn 2/3 → 1; Thuyết phục S38/S69 → 2; S49 Chọn "Trả lời" → 1; S50 Khi kết thúc cấp độ, chọn 1 → 2; S51/S108 Mở 1 → 2 | Ngưỡng thuyết phục; Khai trương IA S40 ==2 Đăng ký; CP S70 Kết thúc đăng ký cấp độ; Đăng ký mở OZ S51/S108 (3 đoạn); Mở đầu S38 ==1 Thêm một lời tỏ tình |
| 15 | ロザミア | S37 Khi làn sóng thứ hai xuất hiện, カミーユ không có ở đó → 3; ゲーツ bị bắn hạ và ロザミア có mặt → 0; ロザミア bị bắn hạ → 3; S41 bị thuyết phục và ゲーツ không có mặt → 1 | Ngưỡng thuyết phục S41 |
| 16 | ヒルデ | S38 Thuyết phục → 0; S38 ヒルデ bị bắn rơi → 3 | 0 → S38 Sekimo đổi thành số đăng ký số 266 ヒルデ＋トーラス; S45 Khi ノイン gia nhập đội ==0 Chỉ đăng ký tài xế, nếu không thì mang theo Torosu |
| 17 | Chương thứ hai của Fukuru | S128 So sánh mức 3 khe trễ được thiết lập → 0, không được thiết lập → 1; S57 Thuyết phục → 0; S57 Fukuru bị bắn hạ → 1/3 | 0 → S128/S57 Fukuru đăng ký ở cuối thẻ (thân vô cơ) |
| 18 | エルリッヒ | S41 Thuyết phục → 2; S41/S56 Kết thúc chặng 1 → 3; S66 Thuyết phục → 2; S49 Thuyết phục → 0; S56 Tỷ lệ sống sót 13 Khi có Aiko → 1; S56 Thuyết Phục → 2 | Ngưỡng thuyết phục; S41/S56 Hết thẻ ==2 Chỉ có một trong hai lựa chọn, chọn 2 → var128=1 → S123; S66 Đăng ký ở cuối thẻ |
| 19 | キラル | S41／S56 キラル bị bắn hạ bởi ドモン → 0 | S104 Khi đợt đầu tiên bị xóa sổ hoàn toàn ==0 → キラル xuất hiện cùng đội 6 |
| 20 | カーツ đếm | 8 cấp độ của sự kiện đánh bại カーツ: カラッド giảm → +1, xuống 2, nhấn lùi về 1 | Ba cấp độ khác nhau ==1 → var21=0; S102 cuối cấp (sai sót ban đầu, xem phần 6.1) |
| 21 | カーツ kết quả | Sự kiện thất bại S41/S56/S66 → 0; S66 hết cấp 0 → 2; S124 hết cấp → 1 (không đủ tiêu diệt)/2 | S41/S56 hết cấp ==0 → S124, ==3 → Khi chuyển đổi hoàn tất, chức năng chuyển giao; Mở S42/S57 ==1 → Chuyển; ==2 7 dòng switch |
| 22 | マーグThuyết phục | Thuyết phục S45/S59/S75/S136 → 0; Thuyết phục S61/S76 → 1 | Ngưỡng thuyết phục; chỉ ảnh hưởng đến dòng |
| 23 | ナイーダ | S45／S61／S76 Thuyết phục → 0; S77 lựa chọn mở đầu 2 → 2; S91 mở đầu lựa chọn 1 → 1, lựa chọn 2 → 2 | Lựa chọn mở đầu S77／S91 ==0 chỉ lựa chọn: chọn 1 Đăng ký ナイーダ＋ダブルスペイザー; chọn 2 và cô ấy sẽ tự hủy, và デューク không thể tấn công; S91 Khi chọn 2, nhóm địch sẽ chuyển sang nhóm 6 |
| 24 | キリカ | S78／S92 デュークThuyết phục → 0; マリアThuyết phục → 1 (Siêu phân đoạn) | Ngưỡng thuyết phục; 1 → Đăng ký kiểm tra キリカ (chỉ dành cho tài xế) |
| 25 | Đường chạy Marathon | S77 thuyết phục Marathon → 0; S61/S76 Marathon bị Marty bắn hạ và var22==1 → 1; S77 Điều kiện tương tự và var25==0 → 1 | Chỉ chọn lối ra của Marathon và các dòng tiếp theo |
| 26 | ロゼ | S61／S76／S77 マーグ bị タケル bắn hạ và ロゼ có mặt → 0 (không nhìn vào var22／25); thuyết phục ロゼ → 1; S91／S130 thuyết phục → 2 | ngưỡng thuyết phục; 2 → S91／S130 Đăng ký Sekimo ロゼ＋ゼーロン (3 đoạn) |
| 27 | プル | thuyết phục S84 → 0; Sự thuyết phục S85 và グレミー không có mặt → 1; Sự thuyết phục của S98 và グレミー bị bắn hạ → 1 | ngưỡng プルツー; キュベレイmkⅡ điều kiện thay đổi màu sắc |
| 28 | ルー | S85 Khi Hoàng đế ルー bị đánh bại, ルー có mặt → 0 | Chỉ có dòng thay đổi (S85/S86/S132) |
| 29 | CHỦ | Sự hiện diện của S86 khi khe trễ là 1 → 0; Sự thuyết phục S88 → 1, sự thuyết phục キャラ → 3; Quân tiếp viện S103 cuối cấp không xuất hiện → 3 | ngưỡng thuyết phục; 1 → S103 giai đoạn triển khai nhóm 4 của chúng tôi ở vòng 8 màn hình |
| 30 | プルツー | S141／S99 → 0; S87／S100 → 1; S132 (グレミー hiện diện)／S101 → 2 | Ngưỡng thuyết phục; 2 → Điều kiện thay đổi màu sắc |
| 31 | ムゲ／Vòng Trái Đất | S89／S139 Khi kết thúc cấp độ, chọn 1 → 0, chọn 2 → 1 | Khi ==1, việc lựa chọn thay đổi màu sắc xảy ra trong cùng một sự kiện; dòng S104 |
| 32 | キャラ | Đối xứng với var29 | 1 → S103 Màn hình Vòng 8 Nhóm triển khai 5 |
| 33, 34 | — | Không được sử dụng | — |
| 35 | Chuông Bạc | S32 Kiệt tác cuối cùng bị bắn hạ ≥20 → 0; S107 Khai mạc ≥30 → 0 (đăng ký cùng lúc) | Chỉ có dòng được thay đổi; S103 Không được phép tấn công |
| 36 | Căn cứ chiến đấu quái thú | S78 Hết màn chọn 2 → 0, chọn 3 → 1 (chọn 1, không viết, giữ 3) | Cốt truyện mở đầu S81; `3E02 36,0` → `3D6F 19` (Shipotian Jingquan) |
| 37 | ガトー | Khu vực S49: hạm → 0, シロッコ → 1, バスク → 3; bên thứ ba bị tiêu diệt hoàn toàn (sau khi mở var101) → 0; đóng cuối 1 → 3 | S49 đóng cuối 0 → đăng ký và đi tới S51, 3 → S108; Đội hình S54/S60/S98; S97/S138 rời đội |
| 38 | ロームフェラ | S107 Chọn 1 → 0 ở cuối cấp độ, chọn 2 → 1 | S107 Đi đâu; điều kiện S56 エルリッヒ |
| 39 | Ma đói Niu | S25 Niu Hungry Ghost bị đánh bại `001a6944` → 0 | S26 Khi tất cả kẻ thù bị tiêu diệt ==0 → Nhóm 11 Niu Hungry Ghost (mang áo giáp composite) tiếp viện |
| 40 | シルキー | Màn S81／S92 Vòng 3: var6==1, var4==0, Malta bị bắn hạ ≥30 → 0; Tota bị bắn hạ → 3 | 0 → Đăng ký シルキー và `3D70` Đi xe cùng Toto |
| 41 | — | Không được sử dụng | — |
| 42 | Thanh lọc thành phần kẻ thù | S62 Furuya HP 30% `001acc24`: Viết 3 trước; Furu hiện diện → 0; Ani có mặt → 1 (Furu không có ở đó)/2 (Furu cũng ở đó) | S63 Mở nhóm triển khai dựa trên giá trị 0–3 (Ai là kẻ thù giữa アレン và フェイ) |
| 43 | ハマーン | S138 Chọn 1 → 0 ở phần mở đầu, chọn 2 → 1; S100 chọn 1 → 0 ở phần mở đầu, chọn 2 → 1 | S97 hết đường chuyền var37==0 ∧ var43==0 → ガトーRời đội; Đường mở S101 |
| 44 | Thuộc bên | S34 kết thúc lượt → 0 (IA); S136 kết thúc lượt → 0 (CP chiến đấu một mình); S76 hết pass → 1 (CP theo sau Toro); S46 hết chặng → 1 (OZ) | S103 ==1 → ノイン không thể tấn công; S103–S105 70 dòng |
| 45 | Shimizu Shisui | S39 Sống sót 10, S55 Sống sót 10, S70 Khe trễ 0 → 0 | **Đọc gốc**: `800A4BB8` trả về var45==0; liên trường `load_0008F4B0:801CA27C`, chiến thuật `801E59D0`／`801E5BE8` Đã thêm "Mirror Shisui" (Văn bản 241) vào cột kỹ năng ドモン; danh sách đường chiến đấu `D_80222F20` Nhấn ==0／==3 để chọn bộ đường cho mỗi quân trong số 5 quân của liên minh tiêu diệt đặc biệt シャッフル |
| 46 | シュバルツ | S137 hết pass var130==0 → 0 | Chỉ đọc các dòng đã chọn một lần trong cùng một sự kiện; danh sách dòng `D_80222F20` có một dòng trỏ đến nó, nhưng `80222664` thực sự so sánh var45 của dòng tiếp theo và giá trị bị loại bỏ. **KHÔNG CÓ TÁC DỤNG KHÁC** |
| 47 | クェス | S105 シャア bị bắn hạ bởi アムロ, var130==3, クェス đã có mặt → 0 | 0 → Đăng ký ở cuối thẻ クェス＋ヤクト・ドーガ (6 đoạn) |
| 48–50 | Liên kết Battler | Kết thúc cấp độ liên kết: 48 (S109/115/117/121), 49 (S111/115/119/121), 50 (S113/117/119/121) → 0 | Nhấp vào đây để tham gia nhóm ngay từ đầu ([Liên kết Link Battler](link-battler.md)); tuyến chính 23 tuyến |
| 51 | ちずる | S138 Ngựa báo bị bắn hạ ở cuối đèo ≥15 → 0; S97 Ngựa báo có mặt ở đầu → 1; S97 Kết thúc đường chuyền 0 → 1 | S99 Khai cuộc ==1 → `3D59 145` (ngựa báo không thể tấn công); Lô đất S97/S98/S99 |
| 52 | Phân kỳ thời gian có giới hạn | S81 mở → 3; S81 khi vượt qua cấp độ (khu vực FE hoặc tiêu diệt toàn bộ kẻ địch), lượt màn là ≤10 → 0 | S130 khi vượt qua cấp độ ==0 và lượt quay màn hình là ≤10 → var128=0 → S82 |
| 53 | Pháo đài バルジ | S45/S72/S97 hết cấp (đánh bại バルジ) → 0 | **Tải gốc**: Bản đồ thế giới `load_000A7EC0:801C3390 → 800A4B8C`, khi ==3, đặt tài nguyên 5596 (バルジ, có thẻ tên) vào vị trí 0xB |
| 54 | Flagship xuống dòng | Nhập → 1 (`8009E0C4`); S48 ドレイク bị đánh bại, S63 ドレイク／ショット bị đánh bại → 3 | **Đọc và viết gốc**: `800A26DC` (sự kiện bỏ phiếu `8009E194` gọi) viết 2, đọc, viết 0, sắp xếp các dòng hạ hạm theo danh sách thuyền trưởng `D_800C9A08` (từ văn bản 5799); đóng khi ==3; `800A3F7C` được sao chép vào `D_8010F6B4`. Không liên quan đến tính năng ẩn |

### 5.2 Biến đơn cấp 100–139

| Biến | Đang vào | Cách sử dụng |
| --- | --- | --- |
| 100–103 | Tập 3 | Loại công tắc ngưỡng 2/7 (mục 4.4), còn dùng làm biển báo bên trong cổng. Viết/đọc: 100 là 95/81 vị trí, 101 là 53/31, 102 là 19/11, 103 là 7/9 |
| 104, 105 | Đặt thành 3 | Chỉ viết ở S26, không bao giờ đọc |
| 106–114 | Đặt thành 3 | Tập lệnh không được sử dụng |
| 115–127 | Không cần đặt lại (3 cho trò chơi mới) | Kịch bản không được sử dụng. var117–122 được truy cập bằng lớp phủ chiến thuật `801CF420`/`801CF884` dưới dạng `127 − D_80217AC5[驾驶员]`: Khi máy bay của phi công là 171–176, nếu biến này == 3, hãy viết 0 và gọi `802176A8`. Vì nó không được đặt lại nên đây là cờ một lần cho mỗi trình điều khiển; xem Phần 10.1 để biết cách sử dụng |
| 128–136 | Đặt thành 3 | Các trạng thái bên trong cấp độ, mỗi cấp độ có ý nghĩa khác nhau (128: 212 viết 248 Đọc; 129: 134/120; 130: 74/64; 131: 42/52; 132: 31/39; 133: 28/36; 134: 27/43; 135: 10/15; 136: 2/3). Liên quan đến bài viết này: Số lượng hộ tống S14 (128) và ba đơn vị (129–131); S41/S56 Kanmo var128==1 → S123; S66 ミネルバX; S129 var128, S137 var128/129 アレンビー; S130 var128 điểm đến có thời gian giới hạn; Đích phân đội S89 var130, S139 var129; quân tiếp viện S103 var129 マシュマー／キャラ; S105 var129／130／136 クェス; S129 var131, S137 var133 Dòng bất khả chiến bại Đông Phương |
| 137–139 | Đặt thành 3 | Tập lệnh không được sử dụng |

### 5.3 Chỉ thay đổi điểm đọc dòng

| Biến | Kịch bản |
| --- | --- |
| 0 | S12, S81, S82, S93, S94, S101, S131 |
| 1 | S16, S17, S20, S23, S24, S30, S37, S40, S43, S44, S45, S46, S57, S61, S77, S99, S107, S137 |
| 2 | S20, S38, S57, S128 |
| 3 | S41, S57, S59, S129 |
| 4 | S20, S33, S42, S81, S91, S92, S140, S141 |
| 5 | S43, S44, S56, S70, S77, S91 |
| 6 | S48, S63, S96, S100 |
| 7 | S26–S33, S42, S47, S50, S54, S55, S61, S81, S85, S89, S90, S92, S98, S100, S102, S103, S106, S132, S138–S140 |
| 9 | S31, S33, S39, S45–S49, S55, S77, S91, S101, S106, S107, S140 |
| 10 | S91, S93, S99, S103–S105, S139 |
| 11 | S77, S78, S84, S85, S89, S97, S98, S103–S105 |
| 12 | S11, S24, S108, S137 |
| 13 | S38, S44, S56, S57, S66, S85, S89, S90, S100, S102, S103, S139 |
| 14 | S38, S40, S43, S44, S51, S55, S69, S85, S89–S91, S100–S103, S108, S136, S139 |
| 15 | S141 |
| 16 | S38, S84, S85, S89 |
| 17 | S39, S45, S57, S59, S98, S128, S137, S141 |
| 18 | S41, S43, S44, S56, S66, S77, S85, S89–S91, S100–S103, S139 |
| 19, 20 | S104; S102 |
| 21 | S44, S85, S89, S90, S100, S103, S139 |
| 23 | S45, S61, S76, S77, S80, S91, S92, S98, S138, S141 |
| 24 | S85, S96, S133 |
| 25 | S61, S76, S77, S91, S99, S130 |
| 26 | S61, S76, S77, S82, S85, S94, S96, S99, S101, S130, S131 |
| 27 | S85, S87, S98, S99, S101, S132, S141 |
| 28 | S85, S86, S132 |
| 29–32 | S88, S105; S101; S104; S105 |
| 36 | S81 |
| 37 | S54, S55, S59, S60, S91, S97–S99, S101, S103 |
| 38, 39, 40 | S56; S25; S81, S92 |
| 43 | S97, S100, S101 |
| 44 | S103–S105 |
| 46 | S137 |
| 48–50 | Tuyến chính 23 địa điểm |
| 51 | S97–S99 |

## 6. So sánh từng mục

Cột "Kết luận": **Nhất quán** có nghĩa là kết luận của kịch bản phù hợp với Akurasu; **Khác** có nghĩa là các điều kiện, giá trị hoặc kết quả không nhất quán với Akurasu (xem Phần 7 để biết chi tiết); **Không bao gồm Akurasu** có nghĩa là Akurasu không có mặt hàng này hoặc các điểm chính nhất quán nhưng các điều kiện chính chỉ thuộc về chúng tôi (xem Phần 8 để biết chi tiết).

### 6.1 Nhân vật chính độc quyền

| Yếu tố ẩn | Akurasu (Tóm tắt) | Kết luận kịch bản | Kết luận |
| --- | --- | --- | --- |
| カーツ＋ヴァイローズ（ブラッド） | Trước mức độ phân kỳ, カラッド đã bắn hạ カーツ hai lần; trước khi kết thúc Vòng tròn Trái đất hỗn loạn, anh ta đã bắn hạ ≥100; khi hết cấp hãy chọn mục thứ 3 | Karna xuất hiện như một kẻ thù ở 9 cấp độ (S16, S25, S34, S41, S46, S56, S64, S66, S124). S25/S46/S64 ngay lập tức rút lui khi Karra không có mặt. Trong trường hợp thất bại ở mỗi cấp độ, bên chiến đấu bên kia là ブラッド (phản công cũng được tính) → var20+1, khi đạt 2 sẽ bị đẩy về 1 (3→0→1). Ở cấp độ phân kỳ (S41, S56, S66), cùng một sự kiện được tính trước rồi đánh giá var20==1 → var21=0, vì vậy ** mức độ phân kỳ phải bị ブラッド bắn hạ và được tính hai lần**. Không có nhánh lựa chọn ブラッド ở cấp độ phân kỳ (S41 `001b181c` là `3D44` duy nhất trong phần アーク), var21==0 tự động bước vào thời gian quyết định S124. S124 Chỉ tấn công ブラッド và trò chơi kết thúc khi ブラッド bị đánh bại; thời điểm カーツ bị đánh bại `001e31b0`: `3E0D ブラッド`, `3E0C 100` → Dưới 100, ghi var128=1. Guanmo ≥100 → Đăng ký カーツ＋ヴァイローズ, `3D6C 35,3`, var21=2; không đủ → var21=1. Trả về var11==0 → S42, var10==1 → S57 | khác nhau |
| スーパーアースゲイン | Nâng cấp khi không dùng カーツ | Tất cả đều là `3D5A 27,0,306,34`: IA Chaos Earth Circle End of Pass (var21==3), OZ トレーズ lệnh xóa Kết thúc cấp độ (var21==3); thời điểm quyết định không thành công → cấp độ tiếp theo (S42/S57) mở ra; CP 戦いのnghĩaは Tất cả các lần chuyển giao ở cuối cấp (`001b6ccc`, var21==0 Khi Karra sống sót, anh ấy tích cực đóng góp cho Rakura, nhưng không tham gia vào đội); nếu Karra được tuyển dụng, anh ấy sẽ không bao giờ chuyển nhượng | Nhất quán |
| アイシャ＋エルブルス（マナミ） | IA/CP/OZ đều có các bước; "ít hơn 9/7 đơn vị"; CP “vòng 2”; OZ S57 tham gia ngay từ đầu | IA: Thuyết phục S34 → Thuyết phục S38 (var13==0) → S40 `001b0990` Khi kẻ địch còn lại **≤9**, nếu var13==2: Malino có mặt → Nhóm 8, `3D58 32,0`; không có → var13=3, hỏng vĩnh viễn. CP: S65 → S66 (var13==0 → 1) → S69 Sau khi Malin bị đánh bại trong trận chiến kịch bản mở đầu, **Giai đoạn của chúng ta ở hiệp 3 màn chơi** (`3D52 0,2,1`) hoặc kẻ địch còn lại **≤7**, tùy theo điều kiện nào đến trước sẽ kích hoạt một lần và Malin phải có mặt. OZ: Trong S49, khi tỷ lệ sống sót của bên thứ ba là 10, Mali sẽ chỉ đưa ra ba lựa chọn khi anh ta có mặt (hai lựa chọn đầu tiên → 0), hoặc khi kết thúc S50, anh ta chọn "びとめる" → 0; thuyết phục S56 (var13==0 → 2); Mở S57 `3D59 28` Malani không thể tấn công và đăng ký khi kết thúc **vượt qua**. Sau khi tham gia, `3D64 500,500` thay thế ローレンス làm phi công phụ | khác nhau |
| スイームルグS | Đạt được cùng cấp bất kể có được tuyển dụng hay không | Đã được tuyển dụng: Cuối cấp S40 (IA)/S69 cuối cấp (CP)/S57 cuối cấp (OZ); không được tuyển dụng: khai mạc S41 (IA)/S69 cuối cấp (CP)/mở S57 (OZ). Khi nó không được tuyển dụng, `3D5A 999,0,37,3000` của エルブルス là không hoạt động | khác nhau |
| エルリッヒ＋ノウルーズ（アーク） | IA: Lý tưởng, Thu gọn, chọn phương án thứ 2, Vòng tròn Trái đất hỗn loạn, Thuyết phục, Guanmo 2; CP: Thuyết phục; OZ: Chắc hẳn là ở phía ロームフェラ, mặt trăng là địa ngục! và トレーズ thuyết phục hai lần | IA: Ngưỡng thuyết phục S41 **var9==0** (nhánh レラ đã được thành lập, xem dòng nhánh レラ trong bảng này) → var18=2; chọn một trong hai ở cuối thẻ Chỉ xuất hiện khi var18==2, chọn 2 "わかりません..." → S123, chọn 1 → var18=3 và nó sẽ bị mất vĩnh viễn. CP: S66 Không có ngưỡng thuyết phục, `3D58` sẽ được chuyển cho chúng tôi ngay tại chỗ và việc đăng ký sẽ hoàn tất (không sửa đổi). OZ: Thuyết phục S49 → var18=0; S56 **アーク hiện diện** khi kẻ địch còn lại 13**: var38==0 yêu cầu var18==0, var38==1 không cần điều kiện tiên quyết → var18=1; Thuyết phục (var18==1) → 2; Guanmo cũng giống như IA. S123 Chỉ tấn công アーク. Nếu máy bay địch đi vào tòa nhà mục tiêu hoặc アーク bị phá hủy, trò chơi kết thúc; đăng ký thông quan, `3D6C 327,4` | Khác nhau |
| リッシュ＋シグルーン（セレイン） | IA chọn "姧様の笑言は..."; CP chọn hai cái còn lại; CP tham gia trước khi bắt đầu S70; OZ Chọn "Trả lời する" hoặc "もう một lần âm thanh をかける" | S35/S65 Ba lựa chọn trước trận chiến: Mục 1 → var14=0 (**Không thể thuyết phục sau**), Mục 2 và 3 → 1; S38/S69 Các ngưỡng thuyết phục đều là var14==1. IA được đăng ký ở đầu S40 và CP được đăng ký ở cuối S70 **Guanmo**, cả hai đều không có sửa đổi. OZ: Trong S49, khi リッシュ xuất hiện, lựa chọn thứ hai chỉ được đưa ra khi có セレイン, "Trả lời する" → 1 → đăng ký mở S51/S108; S50 kết thúc cấp độ "もう一声をかける" → 2 → Đăng ký mở S108; OZ cả `3D6C 328,3` | Khác nhau |
| nhánh レラ (var8/var9) | Lý tưởng, sụp đổ, chọn mục 2 | Chỉ dành cho hệ thống thực. Sau khi mở S30 "レラに声をかける": S27 chọn mục 1 và 2 → var9=0; chọn mục thứ 3 "Bỏ qua する" → sau đó chọn (アーク mục thứ 1, セレイン mục thứ 2 → 0). S30 Chọn "đặt" → var9=1. Ảnh hưởng: S42 Hệ thống thực ở cuối cấp var9==0 → S43 (Vai trò chết trong trận chiến), nếu không thì S44; Ngưỡng kỷ nguyên S41; S63 mở CP Rila rời đội (var9=3); Lô S140 (gồm cả hai mặt giống nhau); hơn mười cấp độ của dòng. S43 và S44 thu được ở cuối cấp độ giống nhau | khác nhau |
| アシュクリーフ（アーク） | Hạm đội tiến công của Quân đội Đế chế Thiên hà | Vô điều kiện `3D5A 25,0,31,30`: Khai cuộc S77 (IA, CP đánh một mình), khai cuộc S91 (OZ, CP với Toro) | Nhất quán |
| ラーズグリーズ（セレイン） | Hạm đội tiến công của Quân đội Đế chế Thiên hà | Vô điều kiện `3D5A 26,0,33,32`: IA S40 **Hết thẻ**; CP chiến đấu một mình S136 cuối đèo; OZ/CP có mở Toro S91 | Khác nhau |

### 6.2 Chung

| Yếu tố ẩn | Akurasu (Tóm tắt) | Kết luận kịch bản | Kết luận |
| --- | --- | --- | --- |
| アイナ＋アプサラス | 时は流れた、撃のビクトリア thuyết phục hai lần; siêu loại chỉ cần lần thứ 2 | Ngưỡng thuyết phục S11 var128==0, var128 Chỉ có sự kiện `0019f2a8` trước trận chiến giữa Siro và Aina được ghi là 0 nên **phải đánh một lần** (ai đánh trước thì được). S24 アイナ xuất hiện sau đợt thứ hai (vòng thứ 5 của màn hình khi đội của chúng ta hoặc kẻ địch là 8) và khi kẻ địch là 10; thuyết phục (var12==0) → 2; đăng ký ở cuối cấp độ. Đối với siêu loại S24, viết trực tiếp var12=0 ở đầu; エイジ không thể tấn công ở cấp độ này | Akurasu dỡ hàng |
| アレンビー＋ノーベルガンダム | Hai sự thuyết phục; ở giai đoạn sau, ドモン và レイン phải bị thuyết phục trong cùng một hiệp, ランタオ trong vòng 4 hiệp, tuyệt vọng. Có ít hơn 10 kẻ thù trước đó; những người chưa bao giờ được tuyển dụng không thể bị thuyết phục | Bước 1 Trong S18/S19, nó sẽ xuất hiện khi số lượng kẻ thù là 5 và không có ngưỡng; ở S19, cấp độ sẽ tự động bị xóa khi bắt đầu giai đoạn địch ở vòng thứ 9. Bước 2 Ngưỡng S128/S57 var3==0. S129: var3∈{0,1} có thể bị thuyết phục; phiên bản điên cuồng xuất hiện trong pha địch ở vòng 2 màn hình hoặc khi địch ≤15; **Đầu tiên là ドモン và sau đó là レイン, không cần phải vào cùng một vòng** (không có sự kiện reset var128/var129 theo vòng ở cả hai cấp độ); Màn hình 5 Cô rút lui vào đầu lượt của kẻ địch (trước khi bị đánh bại). Lưu → var3=2 và đăng ký (**tham gia nhóm ngay cả khi bạn chỉ mới thực hiện bước 1**); nếu không được lưu, bạn sẽ trở thành cốt lõi của デビルガンダム, và `3D5A 9,0,6,4000` sẽ bị xóa khi bị đánh bại. S137 cũng vậy: địch thu hút 12 quân tiếp viện khi đạt 10 lần đầu và rút lui khi đạt 10 lần nữa; người chơi tham gia đội nhưng không tấn công sẽ không thể nhìn thấy cô ấy ở cấp độ này và sẽ không mất cô ấy | Khác nhau |
| ガラリア＋バストール | Không tấn công hoặc phản công trong vòng 4 hiệp | Khe trễ mở màn S20 0 (vòng 2 màn) → khe 1, **Khi pha địch bắt đầu ở vòng 4 màn** `3D58 185,0`, var4=0. Chỉ có hai lần hủy bỏ: cô ấy bị bắn hạ; trận chiến giữa Xiang và cô ấy (6 sự kiện Loại 4, bắt đầu bằng `[185,181]`) có `3E17`==1, tức là Xiang tấn công cô ấy hoặc cô ấy tấn công Xiang và Xiang chọn đánh trả. Cô ấy không hủy bỏ các cuộc tấn công của các sinh vật khác | Khác nhau |
| シーラ＋グラン・ガラン／エレ＋ゴラオン | Chọn 1 Sheela mở đầu, chọn 2 Airei | S26 Lựa chọn mở đầu xác định bản đồ của cấp độ này (62/9), giống như đội 0/1 của chúng tôi và đội địch. Bên không được chọn: IA S33 xuất hiện với tư cách là phe của chúng tôi ở giữa và bị loại bỏ ở cuối cùng cấp. `4000` đã bị xóa ở cuối cấp độ tương tự. CP S62 đã được đăng ký ngay từ đầu và bị xóa ở cuối cấp độ ở S63. OZ S48 xuất hiện và bị loại bỏ ở cuối màn chơi. | Nhất quán |
| Cơ thể Waltz bất tận | Tự động thay đổi thành Tùy chỉnh sau khi sửa đổi năm mục | Bảo trì `load_0008F4B0:801CF85C` (điểm gọi duy nhất `801D0028`, đường dẫn xác nhận sửa đổi): `D_801DC6E4` Số lượng năm phân đoạn trong năm cặp là ≥ giới hạn trên của phiên bản `+0x51` (năm đơn vị này là 7), sau đó `800AAD28` Thay quần áo; đừng nhìn vào vũ khí Để biết về tính kế thừa, hãy xem [Kế thừa chuyển đổi](upgrade-inheritance.md) | Nhất quán |

### Dòng 6.3 Độc quyền

| Yếu tố ẩn | Akurasu (Tóm tắt) | Kết luận kịch bản | Kết luận |
| --- | --- | --- | --- |
| エマ (siêu loại) | クワトロ thuyết phục, tham gia sau cấp độ | S16 エマ xuất hiện ở lượt thứ 3 của màn hình khi giai đoạn của chúng ta hoặc kẻ địch là 12; không có ngưỡng thuyết phục → var1=0; tôn trọng (デビルガンダム) HP 50% Hoặc thuyết phục trước khi bị đánh bại, ngay lúc đó khe trễ 1 đăng ký エマ＋mkⅡ và vượt qua cấp độ với `3D4A`. Hệ thống thật được Sugaru thêm vào cảnh mở đầu S17 (Phần 1) | Nhất quán |
| エリカ (siêu loại) | Rikiri no Town, lựa chọn cuối cùng 1 | Lựa chọn cuối cùng của S23 1 → `3D5A 199,0,999,999` (chỉ trình điều khiển), var5=0 | nhất quán |
| ナイーダ (Siêu loại) | デューク Thuyết phục, chọn 1 ở cấp độ tiếp theo; không có sự thuyết phục, デューク không thể tấn công | Không có ngưỡng thuyết phục (chỉ triển khai ở cấp độ siêu cao). S77/S91 Khi var23==0 mở ra, lựa chọn được thực hiện: mục đầu tiên là đăng ký ナイーダ＋ダブルスペイザー; mục thứ 2 là cô ấy tự hủy (`3D4F`), **デュークkhông thể tấn công ở cấp độ này**, S91 nhóm địch bị đổi sang nhóm khác 6. Khi không thuyết phục được thì chỉ có S77 Kamitu và Sho không thể tấn công, S91 không giới hạn | nhất quán |
| Karika (siêu mẫu) | デューク, Malika lần lượt thuyết phục | S78 Hiệp 3 pha giao hữu, S92 xuất hiện khi địch ≤15; Ngưỡng Malika var24==0; chỉ có người lái xe ở cuối cấp độ | Nhất quán |
| アポリー, ロベルト (hệ thống thực) | Tự động tham gia | Không `3D5A`: S2 (giai đoạn địch ở vòng 2 hoặc tất cả kẻ địch bị tiêu diệt)/S3 (địch 10 sau đợt thứ hai) triển khai đội 4 của chúng tôi (クワトロ, アポリー, ロベルト＋2台リック・ディアス), tham gia trực tiếp vào đội | nhất trí |
| ゲイル＋グライムカイザル (loại thật) | エイジThuyết phục, thêm 4 giai đoạn biến hóa | S12 Không có ngưỡng cho sự thuyết phục. Thanh ghi IA/CP ở cuối cấp S32, **3 giai đoạn**; OZ đăng ký ở đầu S52 (S49 chiêu mộ ガトー → S51 → S52) hoặc cuối cấp S53 (không chiêu mộ hoặc di chuyển ムーンアタック → S108 → S53), 4 giai đoạn | khác nhau |
| ガンダム, ガンキャノン, ガンタンク (hệ thống thực) | Giữ ba đơn vị và bạn sẽ nhận được | S14 Mỗi đơn vị trong số ba đơn vị sẽ bị phán xét: nếu vào khu vực xanh sẽ được sơ tán và tính là được cứu; nếu chúng bị bắn hạ, var128+1, tương ứng var129/130/131=3; Raku・カイン sẽ vượt qua cấp độ ngay lập tức khi HP 50% và những người chưa bị bắn hạ vào thời điểm này cũng được cứu. Khi kết thúc lượt (không phải thua toàn bộ), mỗi đơn vị sẽ được đăng ký và chuyển đổi trong một giai đoạn và sẽ được thưởng (N3) dựa trên số lượng đơn vị bị mất | Khác nhau |
| フォウ (hệ thống thực) | ホンコン hai lần, biển và đất một lần, cấp độ IA カミーユ ≥ ジェリド (trung bình +3 cho tất cả các thành viên), thuyết phục OZ | Chuỗi ngưỡng var2: Không → 0 → 1 → 2. Trong S20, khi bạn chỉ thuyết phục ホンコン một lần thì ở đây chỉ có hội thoại; bước thuyết phục thứ ba đã được thông qua trực tiếp với `3D4A`. S128: カミーユ không thể tấn công ngay từ đầu. Ở lượt thứ 3 của màn, khi pha của ta hoặc cấp của địch ≤8 thì lấy Z để đến; ngay sau khi thuyết phục, `3E06 38,69`, **カミーユ cấp độ hiện tại ≥ Nếu cấp độ ジェリド** thành công (var17=0), nếu thất bại, cấp độ フォウ sẽ bị đánh bại (var17=1).ジェリド cấp độ = `D_8010F5F3`＋3, `800A4BE0` Được tính khi vào bản đồ chiến thuật: mức trung bình của 15 cấp độ cao nhất của các phi công của chúng tôi đã lên máy bay (làm tròn số thập phân), kẹp giữa 1 và phút(99, số phiên đã xóa + 40, 95). S57 Thuyết phục không cần điều kiện cấp độ | Khác nhau |

### 6.4 Tuyến đường độc quyền

| Yếu tố ẩn | Akurasu (Tóm tắt) | Kết luận kịch bản | Kết luận |
| --- | --- | --- | --- |
| Chuông Bạc + Chuông Bạc ロボ | Kiệt tác IA/CP giết chết hơn 20 người; OZ hơn 30, tất cả đều trước khi kết thúc cấp độ này | S32 **Kết thúc cấp độ** (sau `3D4A`) `3E0D 156`, `3E09 20` → ** ≥20**; OZ S107 **Mở** `3E0B 30` → ≥30, rớt ở cấp độ này không được tính | Khác nhau |
| ロザミア | Đánh bại ゲーツ mà không đánh bại cô ấy, sau đó thuyết phục カミーユ và tham gia sau cấp độ | S37 Đợt thứ hai (đội của chúng ta sẽ bị tiêu diệt hoàn toàn ở đầu màn thứ 5 hoặc sớm hơn) **Kuカミーユ phải có mặt** khi nó xuất hiện**, nếu không cả hai sẽ rút lui ngay tại chỗ, var15=3; cô ấy sẽ bị giết sau khi xuất hiện cùng với hồ sơ của chúng tôi `3D58` Trở thành kẻ thù (xóa các giọt); sau đó hạ gục ゲーツ → cô ấy rời sân, var15=0. S41 Cô ấy và ゲーツ xuất hiện khi バレン bị đánh bại; **phải **giết ゲーツ trước khi thuyết phục**, nếu không sẽ vô hiệu; **đăng ký tận nơi** khi thuyết phục (chỉ có tài xế) | Khác nhau |
| ヒルデ＋トーラス | デュオ bị thuyết phục và sẽ không bị bắn hạ; các tuyến khác sẽ tự động tham gia | Thuyết phục IA S38 → `3D58` Chuyển sang phe chúng tôi ngay tại chỗ; nếu anh ta bị bắn hạ sau đó, トーラス sẽ bị loại bỏ. OZ S59, CP Sui Toru S75 Đăng ký vô điều kiện số 266 khi hết cấp, **chỉ có tài xế**; CP không thể đạt được khi chiến đấu một mình | khác nhau |
| ガンダムmkⅢ, メタス开 | IA Thu được sau khi hoàn thành マーズとマーグ | S42 Vô điều kiện khi kết thúc cấp độ: `3D5A 999,0,57,500`, `3D5A 999,0,67,65` | Nhất quán |
| Mireba |
| ゼクス＋エピオン | Phi công OZ ウイングゼロ ở cấp độ này, trao đổi sau cấp độ; トレーズ anh trai chi nhánhと | OZ S57 hết cấp `3D5A 286,0,123,500`, trong khi ヒイロ连ウイングゼロ rời đội (`3D5A 95,0,119,4000`); CP mở đầu bằng トレーズ S76 | Nhất quán |
| Sản xuất hàng loạt グレートマジンガー (CP) | Có được bằng cách làm thủ tục hải quan | S135 Đăng ký vô điều kiện khi hết cấp, cấp 3 | Nhất quán |
| ガトー＋GP02A (OZ) | トールギス壊 Chọn 1, 月はĐịa ngụcだ! Đừng để đơn vị màu vàng chạm tới chân đế | Diện tích cơ sở x10–11, y4–5. **Chiến hạm của chúng ta vào cuộc trước** → var37=0 chiến thắng ngay lập tức; シロッコ vào đầu tiên → 1 (sửa đổi thành 3 ở cuối cấp); バスク vào trước → 3; các đơn vị màu vàng khác vào trước và không có hiệu lực. Bạn cũng có thể tiêu diệt tất cả kẻ thù trước (lần tiêu diệt đầu tiên sẽ mang đến シャピロ nhóm tiếp viện 13, sau đó var101=0 sau khi tiêu diệt), sau đó tiêu diệt bên thứ ba → var37=0. Sekimo 0 → Đăng ký Gaito＋GP02A (3 giai đoạn), Z, GP03, Re-GZ, đến S51; 3 → Tới mục S108 | Khác nhau |
| ガトーRời khỏi đội | Bí mật: Tương lai của sự sống và cái chết. Sau khi rời đội, chọn hợp tác để thăng cấp một cấp; Sơ đồ luồng: Chọn 1 ở cuối cấp độ tiếp theo, chọn 2 ở cuối cấp độ này | S138 Khai mạc "Hợp tác するべきだ" → var43=0 → S97 Rời đội khi kết thúc cấp độ; "すべきではない" → 1 → **S138 Rời khỏi đội ở cuối cấp độ, và để lại bản đồ tại chỗ khi Harumon ngã ra trong cuộc tấn công ở cấp độ này | Khác nhau |
| FA Huyndai Kai | nâng cấp OZ khi đạt cấp độ này | S59 mở vô điều kiện `3D5A 999,0,295,73` (đồng thời hạm đổi thành ネェル・アーガマ) | Nhất quán |
| トッド | Tuyển ガラリア trước, sau đó thuyết phục ba lần; IA đột phá quyết định (Phần 1) tiếp viện, OZ xem えないNgày mai khai mạc | Chỉ nhìn vào var6==1: S81/S92 **Giai đoạn của chúng tôi ở vòng thứ ba của màn hình** (loại 0 giá trị gốc 2) triển khai; cấp độ này bị bắn hạ và mất vĩnh viễn. Không thuyết phục cũng không tham gia kiểm tra var4 | khác nhau |
| シルキー | マーベル Bị hạ gục trước khi bắt đầu cấp độ này ≥30 | Phán quyết cùng sự kiện với トッド: var6==1, var4==0, マーベベル Hạ gục ≥30 → Đăng ký và cùng đi xe; Số lần hạ gục ở hiệp 1 và 2 màn chơi cũng được tính | Khác nhau |
| ロゼ＋ゼーロン | Thuyết phục マーグ → Thuyết phục và đánh bại マーグ, sau đó thuyết phục ロゼ → Thuyết phục lại ロゼ | Tất cả những gì cần thiết là: cấp độ thứ hai (S61/S76/S77) **Tiêu diệt Malik bằng タケル khi có ロゼ** (var26=0, đừng nhìn vào var22/25) → thuyết phục ロゼ → cấp độ thứ ba (S91/S130) rồi thuyết phục → đăng ký ở cuối cấp độ (3 giai đoạn). Thuyết phục Maris chỉ thay đổi lời thoại | Khác nhau |
| プル | IA thuyết phục hai lần, lần thứ hai sau khi bắn hạ グレミー; OZ bị thuyết phục sau khi bắn hạ グレミー | Thuyết phục IA S84 → S85 khi thuyết phục, グレミー không được còn trên bản đồ; OZ S98グレミーnên ** bị bắn hạ ** (`3E1B`==0). Thuyết phục đầu tiên là không hợp lệ (phần 3.6) | Tính nhất quán |
| プルツー | Hãy chiêu mộ プル trước, thuyết phục lần lượt trước khi bắn hạ グレミー | Chuỗi ngưỡng var27==1 → var30 0 → 1 → 2. IA S132 グレミー vẫn phải có mặt** khi thuyết phục; OZ S100 Khi HP của グレミー 30%, nó sẽ rút lui theo プルツー và phải được thuyết phục trước; S101 Không có điều kiện グレミー | Nhất quán |
| MASTER hoặc キャラ | Cả hai đều sống sót, chỉ thuyết phục được một người, ước mơ, trở lại, chọn 2, quân tiếp viện ở vòng 8 | S86 Cả hai đều phải có mặt trên bản đồ khi sự kiện kết thúc ở cuối cấp độ; S88 chỉ có thể thuyết phục được một trong số họ; S103 **Quân tiếp viện xuất hiện ở vòng thứ 8 của màn hình** quân tiếp viện, cấp độ trước đó là var29/var32=3 Mất vĩnh viễn | Nhất quán |
| ノイエ・ジール | Hãy mơ, quay lại, chọn 2 và nhận được nó sau cấp độ tiếp theo | S103 Chỉ đăng ký sau var11==0 ở cuối cấp độ (giai đoạn 3). var11 chỉ được viết bằng S32, vì vậy chỉ những người chơi độc lập chưa bao giờ đi đến hòa bình hoàn toàn mới có thể có được nó; OZ giữ 3 mà không lấy được | Akurasu dỡ hàng |
| キュベレイmkⅡ Đổi màu | Hãy chiêu mộ プル, プルツー và mơ lại lần nữa. Chọn 2, sau đó chọn 2 trước khi bắt đầu cấp độ tiếp theo | Trong cùng một sự kiện cuối cấp ở S89/S139, nếu bạn chọn "Vòng tròn Trái đất" var27==1, var30==2, thì hãy chọn một trong hai; chọn 2 `3D5A 57,0,323,77`, đổi sang bản màu đỏ và đưa cho プルツー | Nhất quán |
| Loại sản xuất hàng loạt νガンダム | Chỉ chọn OZ sau lần chênh lệch đầu tiên; chọn một trong hai thiết bị | S137 Ở cuối cấp độ, khi var10==1, "ファンネル loại trang bị/インコム loại trang bị" → Số 294/296 | Nhất quán |
| Sabre Survival (OZ) | Hãy để Saber thật tấn công; có quay lại hay không là điều không chắc chắn | S137 Sau khi xuất kích mở màn, **Riber (phi công, cơ thể không giới hạn)** có trên bản đồ → var130=0. Trong hai sự kiện giải quyết, `3D5A 3,0,0,4000` chỉ được thực thi khi var130 ≠ 0, vì vậy anh ấy và ガンダムシュピーゲル** vẫn còn trong danh sách**; một đoạn hội thoại khác của "Sống sót trên đường ゲッター" được phát ở cuối cấp độ | Khác nhau |
| トールギスⅢ | ハマーンの影 Chọn 2 | S99 Chung kết Chọn 2 → `3D5A 286,0,136,123` | Nhất quán |
| Kirara＋Marinaダラガンダム | Kirara đánh bại Kirara (xuất hiện ở vòng 5), rồi gia nhập Kurara (phía trước) | S41／S56 Korra bị Dumran bắn hạ → var19=0. Ngoại hình: Khe trì hoãn S41 2 được kích hoạt khi バレン bị đánh bại. バレン bị đánh bại trong trận chiến kịch bản mở đầu nên là pha đối đầu ở hiệp thứ 5 của màn; S56 là giai đoạn thân thiện tiếp theo sau khi đợt đầu tiên bị tiêu diệt hoàn toàn. S104 Khi đợt đầu tiên bị xóa sổ hoàn toàn, var19==0 → Kirara xuất hiện với tư cách là đội 6 của chúng tôi, **vẫn hiện diện khi đợt cuối cùng bị xóa sổ** trước khi `3D58` tham gia | khác nhau |
| クェス＋ヤクト・ドーガ | ラー・カイラム アクシズ trong vòng 2 lượt (hoặc trước đó) アムロ hạ gục シャア | S105: Viết var130=0 trong hiệp giao hữu thứ 2 `001e12e0` sau khi ラー・カイラム tiến vào khu vực (giai đoạn đẩy lùi bắt đầu).シャア bị アムロ bắn hạ và var130 vẫn là 3 → trốn thoát, クェス có mặt → var47=0. Ngoài ra: Khi bắt đầu giai đoạn của chúng ta ở vòng 8 màn, cả var130 và var136 đều là 3 → Game over | Nhất quán |
| Trận chiến đột phá 10 hiệp | Cả hai cấp độ đều được hoàn thành trong vòng 10 vòng → Một bên | `3E04 10`: Các chương trên và dưới được hoàn thành trong ** vòng thứ 10 của màn hình (bao gồm)**; cả hai chương đều đã hoàn thành → S82 | Nhất quán |
| Một trận đột phá mang tính quyết định. Phương pháp chiến thắng | Đơn vị nào đến địa điểm được chỉ định | chữ thắng “Nhập máy đầy đủ hương vị”; chế độ khu vực FE, thoát ra ngay sau khi vào, **Tất cả nhân sự rút lui** (hoặc tiêu diệt toàn bộ kẻ thù) để vượt qua cấp độ | Khác nhau |
| Ba sự lựa chọn cho căn cứ cỗ máy chiến tranh cung hoàng đạo | Dòng Garnera: Kontra V bốn vũ khí; Dòng Rakuten: Shipotian Jingquan | Chọn 1/2/3 → S81/S79/S80. Bốn mảnh コンバトラーV (770/773/775/777) được mở khóa **vô điều kiện** khi bắt đầu S81 (OZ bắt đầu từ S93); dòng Shipotian Jingquan ランタオ nằm ở cuối S79, hai dòng còn lại nằm ở đầu S81 (var36≠0, giữ nguyên giá trị ban đầu khi chọn 1 3), OZ ở cuối cấp S95 | khác nhau |
| ムゲ／Đội Vòng Trái Đất | Chọn 1 để đến ムゲ Universe, chọn 2 để ở lại; hoạt động có sẵn ở cả hai bên | S89／S139 Lựa chọn cuối cấp → `3D73`: Chọn ムゲ Vũ trụ và đặt danh sách B (`D_800D06E4`, 61 người) là không thể tấn công, để lại danh sách Vòng tròn Trái đất A (`D_800D06A8`, 29 người) được đặt là không thể tấn công; Việc mở S104 `3D74` bị xóa. Có hai danh sách Gura và không có danh sách nào; Nhân vật Link Battler không có trong danh sách | Nhất quán |
| ミリアルド（ノインthuyết phục) | Có thể bị thuyết phục bởi ノイン | S84 không có ngưỡng, ngưỡng S103 var11==0; cả hai nơi chỉ có hội thoại, không có biến | nhất quán |
| Đã mở khóa vũ khí được sửa đổi hoàn toàn | Mở khóa sau khi sửa đổi hoàn toàn | Xác nhận sửa đổi `801D1100` → `801D0AE4`: Bảng `D_801DC87C` 18 vật phẩm (số cơ thể, số vũ khí đã sửa đổi hoàn toàn, số vũ khí đã mở khóa) | Nhất quán |

### 6.5 Mở khóa vũ khí và kỹ năng kết hợp trong cốt truyện

| Dự án | Akurasu (Tóm tắt) | Kết luận (Kịch bản & Mã) | Kết luận |
| --- | --- | --- | --- |
| シャッフルLiên minh bốn máy chắc chắn giết (53/62/71/76) | — | `3D6F`: S39 khai cuộc (IA), S55 khai cuộc (OZ), S70 địch bị tiêu diệt hoàn toàn hoặc hiệp thứ 15 giai đoạn ta đến trước (CP); viết var45=0 cho cùng một loạt sự kiện | Akurasu Không bao gồm |
| Đoan Không Quảng Phương Kiếm (874) | S81 | S78 Guanmo (IA), S92 Guanmo (OZ) | Khác nhau |
| Nắm đấm chấn động Shi Potian (19) | Độc quyền cho dòng Raku | Đầu S79, đầu S81 (var36≠0), đầu S95, cả ba dòng sẽ nhận được | Khác nhau |
| コンバトラーV bốn mảnh | dòng ジャネラ | mở S81, mở S93; S80 số `3D6F` | Khác nhau |
| Sự xuất hiện của kỹ năng kết hợp | — | Mỗi lần mở danh sách vũ khí `8020178C` (điểm gọi `801CD798`, `801F8FE4`), hãy gọi hàm phán đoán cho từng kỹ năng kết hợp: trả về 0 và đặt bit khóa (`+0x22` bit 0x04), nếu không thì xóa khóa và ghi nguồn. Người tham gia phải tìm đơn vị có mặt đầu tiên trong cùng một trại và **kết nối với nhau** (đếm theo đường chéo, ba đơn vị trở lên không cần liền kề nhau 2 x 2; `80200530`, `801E966C`, `801E95DC`), số EN, sức mạnh và số điều kiện của mỗi người đều đạt tiêu chuẩn | Akurasu Không bao gồm |
| ダブルゴッドフィンガー (1215) | Chỉ có trong Quân đội Độc lập (Thẻ xử lý) | `3D6F 1215` duy nhất trong toàn bộ ROM nằm ở cuối S41 (var3==1), nhưng bit khóa sẽ bị ghi đè bởi `8020178C`, **Lệnh này không có hiệu lực lâu dài**. Bạn có thể sử dụng bất kỳ tuyến đường nào miễn là thần ガンダムH (ドモンki ≥130 tự động chuyển đổi, `801FF1BC → 801FEDF4`) ở liền kề với ノーベルガンダム của chúng tôi, mỗi tuyến có EN ≥60 và ki ≥130 | Khác nhau |
| Nắm đấm Ishiba Tenjin | OZ 42, ドモン nhánh 38, nhánh khác 53 | Chức năng xác định `80200B1C` cũng yêu cầu phiên bản đầu tiên số 19 trong nhóm vũ khí `D_80178F80` phải được mở khóa, vì vậy `3D6F 19` theo sau Ishiba Tenjin Fist Go: Kết thúc cấp độ S79/Mở đầu S81/Kết thúc cấp độ S95 | khác nhau |
| Cấu trúc nắm đấm đồng minh | Nắm đấm chiến thuật (Sau) được thêm vào | Không mở khóa cốt truyện; Thần S-form H và bốn dạng S được kết nối với nhau, mỗi dạng EN ≥100, power ≥130 | Khác nhau |

## 7. Khác biệt với Akurasu

Dưới đây là tất cả những “sự khác biệt” đã được xác nhận ở vòng này.

1. **カーツ**: Trong giai đoạn phân kỳ, ブラッド phải bị ブラッド bắn hạ và được tính là "hai lần" (Akurasu: hai lần trước giai đoạn phân kỳ); không có nhánh lựa chọn của ブラッド trong giai đoạn phân kỳ (Biểu đồ dòng chảy Akurasu: chọn phương án thứ 3); 100 kill tại thời điểm quyết định. Phán quyết tại thời điểm đánh bại Akurasu (danh sách tóm tắt Akurasu: Trước khi kết thúc Vòng tròn Trái đất hỗn loạn; trang cá nhân cũng vậy).
2. **アイシャ**: Số người sống sót là ≤9/≤7 (Akurasu: dưới 9/7; Sơ đồ luồng: dưới 8/6 đơn vị); nhánh CP bị trì hoãn là vòng thứ 3 của màn trong giai đoạn của chúng ta (Akurasu: vòng thứ 2); Lựa chọn OZ S49 cần có sự góp mặt của Marino; OZ ở S57 **Kết thúc cấp độ** tham gia và Malani không thể tấn công ở cấp độ này (Akurasu: mở đầu).
3. **スイームルグS**: Khi Aアイシャ không được chiêu mộ, IA mở tại S41 và OZ chuyển giao khi mở S57 (Akurasu: cùng cấp).
4. **エルリッヒ IA**: Ngưỡng là var9==0 (nhánh レラ), lý tưởng, えて, mục 1 và 2 đều OK, key là オペレーション・デイブレイクChọn "レラに声をかける" (Akurasu: Sự sụp đổ lý tưởng, chọn mục 2).
5. **エルリッヒ OZ**: Không cần thiết phải sang bên ロームフェラ; トレーズ xóa mệnh lệnh và kẻ địch phải có mặt khi kẻ địch còn lại ≤13 (Akurasu: phải ở bên ロームフェラ, không đề cập đến sự hiện diện).
6. **リッシュ**: IA cũng phải chọn mục 2 hoặc 3, không thể thuyết phục được sau mục 1 (Akurasu: mục 1); CP tham gia vào cuối **Kanmen** trên chiến trường (Akurasu: trước khi bắt đầu).
7. **Nhánh Rura**: Xem phần 6.1 để biết các kết hợp (Akurasu: Chỉ cần viết Ideal Breaker và chọn mục 2).
8. **ラーズグリーズ**: IA ở phần cuối của Seki no Ming はエピオン, đầu tập 6 (Akurasu: Hạm đội Tiên phong của Quân đội Đế chế Thiên hà).
9. **アレンビー**: Hai cấp độ sau không nhất thiết phải ở cùng một vòng; người chơi chỉ mới thực hiện bước 1 cũng có thể được giải cứu và gia nhập đội; thời điểm rút lui của S129 là thời điểm bắt đầu pha địch ở hiệp 5 màn (Akurasu: cùng hiệp, trong vòng 4 hiệp; ai chưa chiêu mộ thì không thuyết phục được).
10. **ガラリア**: Chỉ trận chiến giữa Xiang và cô ấy sẽ bị hủy, các mecha khác có thể tấn công; thời điểm nhập cuộc là thời điểm bắt đầu pha địch ở hiệp thứ 4 của màn (Akurasu: không tấn công hoặc phản công trong vòng 4 hiệp).
11. **ゲイル**: IA/CP là phép biến đổi 3 giai đoạn, OZ là phép biến đổi 4 giai đoạn; ranh giới S52/S53 của OZ là việc ガトー có gia nhập đội hay không (Akurasu: 4 chặng, chia theo tuyến đường).
12. **ガンダム三机**: Phán xét từng cái một, giữ cái nào sẽ được cái nào (Akurasu: giữ ba).
13. **フォウ**: Cấp độ ジェリド là "trung bình của 15 người hàng đầu đã lên máy (làm tròn, giới hạn trên là 95) + 3", được tính khi vào cấp độ này (Bí mật Akurasu: điểm trung bình của tất cả các thành viên +3; "top 15" của Sơ đồ luồng là nhất quán).
14. **Chuông Bạc**: Ngưỡng chứa dấu bằng ( ≥20/ ≥30); OZ được đánh giá khi bắt đầu phần mở đầu Toruルギス và việc hạ gục cấp độ này không được tính (Akurasu: vượt quá, trước khi kết thúc cấp độ này).
15. **ロザミア**: Ở vòng thứ 5 của màn S37 (khi làn sóng thứ hai xuất hiện), カミーユ phải có mặt; ở S41, giết ゲーツ trước rồi mới thuyết phục, nếu không sẽ vô hiệu; thuyết phục gia nhập đội ngay tại chỗ (Akurasu: tham gia sau cấp độ, không cần điều kiện hiện diện).
16. **ヒルデ**: Chỉ có thể lấy được OZ và CP khi Toruzu làm người điều khiển, nhưng không thể lấy được CP bằng cách chiến đấu một mình (Akurasu: các tuyến khác được tự động thêm vào).
17. **ナイーダ**: Điều kiện để デューク không thể tấn công là đã bị thuyết phục và chọn mục 2; nó có thể tấn công mà không cần thuyết phục (Biểu đồ luồng Akurasu: nó không thể tấn công mà không thuyết phục).
18. **ガトーGia nhập đội**: Mục tiêu quyết tâm duy nhất là chính シロッコ và バスク; sẽ được coi là thành công nếu hạm của chúng tôi tiến vào căn cứ trước hoặc nếu cả hai giai đoạn đều bị tiêu diệt hoàn toàn (Akurasu: không có đơn vị màu vàng nào được phép vào).
19. **ガトーRời đội**: Chọn "Tham gia lực lượng するべきだ" để rời đội khi hết màn tiếp theo (S97), chọn "すべきではない" để rời đội khi kết thúc màn này (S138) (trang Akurasu Secrets ngược lại; Sơ đồ cũng như vậy).
20. **トッド**: Không có điều kiện tiên quyết nào cả; quân tiếp viện đang trong giai đoạn của chúng ta ở vòng thứ 3 của màn hình (Akurasu: chiêu mộ ガラリア trước; OZ tham gia ngay từ đầu).
21. **シルキー**: Được xác định cùng lúc với トッド, việc hạ gục ở hiệp 1 và hiệp 2 cũng được tính (Akurasu: trước khi bắt đầu cấp độ này).
22. **ロゼ**: Thuyết phục Malik không phải là điều kiện tiên quyết, mấu chốt là Malik bị Malik bắn hạ khi có mặt ロゼ (Akurasu: Đầu tiên bạn phải thuyết phục Malik ở cả ba cấp độ).
23. **シュバルツ**: Được đánh giá là phi công Riko; anh ta sẽ không bị xóa khỏi danh sách sau khi sống sót (Akurasu: True ゲッター, việc trở lại là không chắc chắn).
24. **キラル**: S104 phải đợi đến đợt hủy diệt hoàn toàn cuối cùng trước khi gia nhập; OZ xuất hiện trong màn giao hữu tiếp theo sau đợt hủy diệt toàn diện đầu tiên (Akurasu: xuất hiện ở vòng thứ 5, tự động tham gia ở giữa màn).
25. **Chiến lược đột phá tử thần**: Vượt qua màn yêu cầu tất cả thành viên phải vào khu vực xanh và rút lui (Akurasu: đơn vị nào đến).
26. **Ishipoten Shocking Fist, 4 mảnh Konnoli V và Thanh kiếm răng ánh sáng phá bầu trời**: Xem Phần 6.5 để biết các cấp độ mở khóa (Akurasu: thuộc dòng Rura, dòng ジャネラ, tương ứng là S81).
27. **Kỹ thuật hợp nhất**: ダブルゴッドフィンガー, シャッフルAllied Fist không cần phải mở khóa thông qua cốt truyện và cũng có sẵn trong dòng OZ; Ishiba ラブラブ天翖剑 nối tiếp Ishiba Thiên Tân Toàn (Akurasu: OZ 42, ドモン chi nhánh 38, những người khác 53).
28. **サンクキングダム, ミリアルド** của Collapse (S67): Khi pha của chúng ta bắt đầu ở vòng thứ ba của màn hình, ヒイロ không có mặt → đội của chúng ta tạm thời tham gia trận chiến, và có mặt → kẻ địch (Akurasu: Khi ヒイロ bị hạ gục trước đó xuất hiện).
29. **Humanity's Victory, Nana... (Sau) (S140)**: var9 chỉ thay đổi cốt truyện, và cách sắp xếp mở đầu hai bên giống nhau (bản thảo cũ của hướng dẫn nói rằng cách sắp xếp sẽ được thay đổi).
30. ** Sát cánh bên nhau từ nay (S123) **: Chỉ アーク mới vào được, OZ tập 31, Quân Đội Độc Lập tập 32 (Akurasu Flow Chart: 32/33 tập).

## 8. Không bao gồm Akurasu

### Cơ chế 8.1

| # | Nội dung | Cơ sở |
| --- | --- | --- |
| M1 | Thuyết phục chỉ xuất hiện khi liền kề lên, xuống, trái, phải. Người thuyết phục phải là người dẫn dắt chính và có số lượng hành động; nó cũng có thể được thực hiện sau khi di chuyển | Mục 3.1 |
| M2 | Khi cùng một người thuyết phục gắn liền với hai đối tượng, anh ta chỉ có thể thuyết phục được đối tượng đã đăng ký trước | Mục 3.2 |
| M3 | Các điều kiện tiên quyết của mỗi chuỗi thuyết phục được ghi trong ngưỡng tiêu đề sự kiện (tất cả 47 sự kiện đều có ngưỡng) | Mục 3.3, 3.8 |
| M4 | Một lần thuyết phục tiêu tốn một hành động và nếu kiểm tra không thành công, vị trí ở cấp độ này cũng sẽ bị vô hiệu (ロザミア, プル, プルツー (ở giữa), bên ngoài phần tuyến đường) | Mục 3.4, 3.6 |
| M5 | Các thành phần chỉ rơi ra khi đơn vị của chúng tôi bị bắn hạ trong trận chiến; `3D58` sẽ bị xóa khi đổi bên nên không lấy được cảm biến sinh học của S37 ロザミア | `801F6778`, `802106FC` |
| M6 | `3E1B` Phân biệt “Bị bắn hạ (0)” và “Rút lui, không lộ diện (3)”, プル (S98) yêu cầu bị bắn hạ | Mục 4.3 |

### 8.2 Những phát hiện mới từ quá trình quét toàn bộ N1–N17

| # | Nội dung | Bằng chứng |
| --- | --- | --- |
| N1 | ちずるĐường phẫu thuật: S138 Ngựa báo bị hạ gục ở cuối đường ≥15, ** hoặc ** S97 Để ngựa báo tấn công (bất kể số lần tiêu diệt được) và đường phẫu thuật sẽ được sử dụng (var51=1), S99 Mở đầu `3D59 145` Ngựa báo không thể tấn công; khi cả hai đều không hài lòng, コンバトラーV vẫn có sẵn như thường lệ | `001da000@532`, `001d8b64@976`, `001d9430@430`, `001db3d0@866`/`@882` |
| N2 | Lựa chọn mở đầu của chương Gunman Killing Machine (S10) アーク "もう小し考えさせてください" → `3D59 25`, アーク không thể tấn công ngay từ đầu; màn 4 Đến lượt, tất cả các pha của chúng ta hoặc kẻ thù sẽ bị tiêu diệt (`0019eb7c`/`0019ec90`), dẫn đầu đội ゲイル và viết var129=1, var101=0; sau đó, ở lượt thứ 6 của màn, các pha của chúng ta hoặc kẻ thù sẽ bị tiêu diệt. Khi ≤6 (`0019ec70`/`0019ecb8`), アーク lấy ソルディファー để đến nơi (`0019ece4@36 3D45 7`). Không có tác động xuyên biên giới | `0019e7e8@398`／`@732` |
| N3 | Naru tuyệt đẹp・カイン (S14) Phần thưởng hộ tống: Mất 0 đơn vị +35000, 1 đơn vị +20000, 2 đơn vị +10000, mất toàn bộ nghĩa là không có cơ thể cũng như tiền thưởng | `001a0e80@54`, `@158`/`@184`/`@210 3D5B 10/20/35` |
| N4 | Ushiugi bị đánh bại (S25) → var39=0 → Sơn máu られた道 (S26) Khi tất cả kẻ thù bị tiêu diệt, Ushiguki mang theo 2 quân tiếp viện và áo giáp tổng hợp; nếu không thì nó không xuất hiện | `001a6944@18`, `001a7564@34` |
| N5 | Khi Kaoru gia nhập đội, Kosugaru (Trước/Sau) (S83/S131), Tuyến phòng thủ Kusuko Jueku (Phía trước) ／Sau) (S93/S94) Nó được đổi thành Guara ở chế độ chờ và hộ tống, và điều kiện thắng thua đổi thành "Máy Jaru"; Yuru có thể tấn công vào lúc này | `001ce7ec@692`, `001d4018@56`/`@134`, `001d69f4@1226`, `001de548@116` |
| N6 | Chỉ có một `3D6F` Finger of the Dual God (S41), nhưng nó không có tác dụng lâu dài đối với các kỹ năng kết hợp, xem Phần 6.5 | `001b181c@814`, `8020178C` |
| N7 | Sẽ nhận được cả ba dòng Shi Potian Jing Fist | Mục 6.5 |
| N8 | コンバトラーV Bốn mục không liên quan gì đến dòng ジャネラ | Mục 6.5 |
| N9 | Nautilus: Điều kiện thực sự khiến Nautilus không thể tấn công | Mục 6.3 |
| N10 | Kẻ thù và bạn bè của S67 MIRARA được xác định bằng việc liệu ヒイロ có hiện diện ở đầu giai đoạn giao hữu ở vòng thứ 3 của màn hình hay không; S67 tự động chiến thắng ở vòng 10 giai đoạn giao hữu | `001b71ac@12`–`@50`, `001b734c@162` |
| N11 | Các tàu sân bay thành phần xuất hiện tùy theo hoạt động: S20 バーン (Được tham gia bởi ガラリア, hoặc bị bắn hạ bởi **Xiang**); Cỗ máy chiến đấu S51/S108 シャピロ (nin có mặt khi シャピロ bị bắn hạ); S56 ガイア三星(kẻ thù) 15 khi Haru có mặt); S97 Haruhiruビ・ジェリド (Maharu không có mặt khi bị bắn hạ); Máy đẩy lớn S63 (được Black Knight mang theo khi Black Knight bị Sho bắn hạ và Era có mặt); S35ガブスレイ・ジェリド (không có bộ phận) | `001a42a0@190`, `001c1798@38`, `001c6200@20`, `001d8fd8@120`, `001b53c4`, `001ad960@124` |
| N12 | Các hạn chế tấn công ẩn khác: S128 và S57 カミーユ không thể tấn công khi var2==2; S57 マナミ không thể tấn công khi var13==2 ở OZ マナミ; S103 ノイン không thể tấn công khi var44==1; S103 Toàn bộ tuyến đường Kaoru và Ginling không thể tấn công | `001b4638@440`, `001c6b90@1264`/`@1288`, `001decc0@1794`/`@1810` |
| N13 | ジャネラ Super Beast: Hai cơ thể mẹ AI #359/#313 chỉ được xác định khi có ジャネラ, và con nào bị đánh bại trước sẽ xác định var129 (con còn lại có mặt: #359 đầu tiên → 0, #313 đầu tiên → 1; con còn lại đã bị bắn hạ → 2), khe trễ 0 (Tất cả kẻ thù đều bị tiêu diệt hoặc pha của chúng ta đang ở vòng thứ 5 của màn hình) Nhấn 0/1/2 để tăng viện cho Surasu, Kaurai, Kaoru hoặc hai đơn vị (cả hai đều được trang bị động cơ đẩy); khi Sura có mặt, các đội bổ sung gồm Sirius và Karuno (ワキメデス mang áo giáp tổng hợp) sẽ được bổ sung. | `001cd350`, `001cd390`, `001cd48c@268`–`@560` |
| N14 | Chọn các chi chỉ thay đổi đường: S2 アーク Lựa chọn Chương 3, S16 マナミ Lựa chọn Chương 2, S46 セレイン Lựa chọn Chương 3; Lựa chọn thứ hai tên tàu S33/S62/S46 "Matsumoto" (mục thứ 2 mở đầu vào tên đơn vị `3D5E`, phiên bản đã chuyển cố định mục trả lời tự động 1) | `0019ca34@172`, `001a2068@146`, `001bcaa8@72`, `001ab86c@428` |
| N15 | Các biến cấp độ chéo chỉ thay đổi điểm đọc của dòng | Mục 5.3 |
| N16 | Dòng kết thúc của Dongfang Bubai: S129 (var131) / S137 (var133) Tùy thuộc vào việc anh ta đã từng chiến đấu với anh ta trước đây hay chưa, hai bộ dòng khác nhau sẽ được phát khi Domen đánh bại anh ta | `001d38c8`, `001d3acc@20`/`@132`; `001d8250`, `001d849c@42` |
| N17 | Lực lượng tiếp viện được xác định theo phán đoán hiện diện (không ảnh hưởng đến việc gia nhập đội): S15 Bên thứ ba ウイングガンダム khi ヒイロ không có mặt; S68 Dark General có mặt → グレート × 8, ボス được sản xuất hàng loạt → 戦阘獣 × 9; S75バスク có mặt → ビルゴ ×9; S136 ガンダル có mặt → ミニフォー ×9; S84 トレーズ có mặt → 五飞シェンロン, ハマーン có mặt →プルのキュベレイmkⅡ；S101 ガトー／キャラ là hiện tại → mỗi lần sẽ đổi máy và xuất hiện trở lại | `001a16e0@246`, `001b77f8`, `001bb25c@64`, `001bc058@20`, `001cf6d0@142`, `001cf878@20`, `001dc868` |

### 8.3 Chi tiết bổ sung cho từng phần tử

| Yếu tố | Nội dung | Cơ sở |
| --- | --- | --- |
| カーツ | Nội dung đoạn kết, 3 giai đoạn chuyển hóa, điều kiện thất bại và đích đến trở về; Chi nhánh CP "カーツ sống sót, tình nguyện ヴァイローズ" | `001e31fc`, `001b6ccc@462` |
| カーツ (Lỗi ban đầu) | Chi nhánh CP sống sót cũng viết var21=2, và 7 cấp sau khi sáp nhập vào quân đội độc lập, các dòng coi anh ta như là người trong đội; ở cuối S102, var20 được sử dụng (khối `3E03 20,2` trống) và các dòng của カーツ sẽ được phát bất kể anh ấy có ở trong đội hay không | `001dd890@134`／`@152` |
| アイシャ | Khi IA tuyển dụng không thành công, cô ấy bị thương nặng và trở về nhà, còn エルブルス được giao cho Malima | `001b0be4` |
| エルリッヒ | S41 Giới hạn thời gian: Ở lượt thứ 11 của màn, pha của chúng ta sẽ bị mất (tất cả kẻ địch sẽ bị tiêu diệt trong vòng 10 lượt); từ đó trở đi, giai đoạn biến hình thứ 4 sẽ được thực hiện song song và máy bay địch sẽ thất bại khi đi vào tòa nhà mục tiêu | `001b174c`, `001e2efc` |
| リッシュ | Việc lựa chọn OZ S49 cần có sự hiện diện của セレイン; OZ đều tham gia với cấp 3 | `001bfa04@122` |
| レラ | Khi var9==0, CP rời đội trong quá trình thanh tẩy (S63), và OZ hy sinh trong chiến thắng của Nhân loại (sau) (S140); ở cuối S43 và S44, cả hai đều nhận được ダブルスペイザー, ドリルスペイザー, và マリア| `001b4fc4@254`, `001ca8b8@22`, `001b30b4`, `001b3dd4` |
| フォウ | S20 Bước thuyết phục thứ ba trực tiếp kết thúc cấp độ; S128 nếu so sánh cấp độ không thành công, フォウ sẽ bị đánh bại và thua vĩnh viễn | `001a4420@512`, `001b4b8c` |
| アイナ | Đăng ký S11 Kanmo Sugaru＋Ez8 (đoạn 1) | `0019f6d0@436` |
| ガラリア | Khi bị bắn hạ bởi một cỗ máy không phải Sho, làn sóng thứ hai (バーン) sẽ không xuất hiện. Sau khi tiêu diệt hết kẻ thù, nó sẽ trực tiếp tiến vào làn sóng フォウ | `001a42a0@30`–`@264` |
| エマ(Siêu loại) | Khi không được tuyển dụng, S26 カミーユ xuất hiện trên mkⅡ; khi được tuyển dụng chỉ đăng ký カミーユ và đăng ký Gディフェンサー | `001a7494`, `001a765c@142` |
| ゲイル | S83/S93 đăng ký lại và cấm tấn công | `001ce7ec@716`, `001d69f4@1244` |
| ガトー | Quyết định ở lại hay đi S54 mở đăng ký, quân tiếp viện S60 của địch (Nhóm 5, trong đó ガトー lái GP02A), S98 dù anh ta lái GP02A hay ノイエ・ジール | `001c39a4@1602`–`@1714`, `001c8d04`, `001da3b8@1130` |
| クワトロ | S98 trở lại làm quân tiếp viện và không thể tấn công; var11==1 điều khiển một trăm kiểu, nếu không FA một trăm kiểu sẽ bị thay đổi; người lái xe lại rời đội khi kết thúc cấp độ | `001da3b8@1168`–`@1220`, `001db0f0@562` |
| S100 Lựa chọn thứ hai khi mở đầu: "Dekata See" chỉ yêu cầu tiêu diệt hoàn toàn quân グレミー, còn "両方を相手にする" yêu cầu cả hai quân đều phải bị tiêu diệt hoàn toàn; S138 Lựa chọn thứ hai khi mở màn: Ở màn hợp tác thứ hai, Haruman và những người khác xuất hiện với tư cách là bên thứ ba | `001dbacc@1156`, `001d992c` |
| クェス | Điểm 0 duy nhất được ghi bằng var130 là `001e12e0` (vòng giao hữu thứ hai sau sự xuất hiện của ラー・カイラム) | `001e12e0@920`／`@964` |
| ノイエ・ジール | Không thể lấy được OZ (var11 duy trì 3) | Mục 6.4 |
| Bên trại var44 | IA/CP chiến đấu một mình là 0, OZ/CP với Tororo là 1 | Mục 5.1 |
| Các biến được đọc nguyên bản | var45 Đường biểu diễn và sát thủ của var45 Shisui Shisui, Pháo đài var53 バルジ, đường hạ gục var54 Flagship | Mục 5.1 |
| Thanh lọc thành phần kẻ thù | S62 ドレイク Khi HP ≤30%, hiện tại アレン/フェイ sẽ xuất hiện trở lại vào đầu S63 | var42 |

## 9. Mức độ chảy với các điều kiện khác nhau

`3D4B` chỉ chiếm phần rìa giữa phân đoạn chung và phân đoạn nhân vật chính; `3D4B 500` (trở về từ liên kết) không tính số từ.

| Cấp nguồn (cuối cấp) | Điều kiện → Cấp độ tiếp theo |
| --- | --- |
| S5 ミケーネと百鬼 | ブラッド → S7; マナミ → S6 |
| S7 Ngày sao băng rơi | ブラッド → S8; マナミ → S9 |
| S17 Ai・戦士たち | Loại thực → S18; Siêu loại → S19 |
| S20 Hazama Yuu của biển và đất | Loại thực → S21; Siêu loại → S22 |
| S30 オペレーション・デイブレイク | Chọn 1 "OZ に入り, khôi phục đơn hàng にNU める" (var10=1) → S46 Đường Mới (OZ); chọn 2 (var10=0) → S31さらば戦士よ(Quân đội Độc lập) |
| S32 Liangshan Bo's の戦い | var11==1 → S62 広がっていく悪义 (hòa bình hoàn toàn); ngược lại → S33 |
| S41 Vòng tròn hỗn loạn của Trái đất | ブラッドphần var21==0 → S124 Giờ quyết định; アークphần var128==1 → S123 ここより公に; ngược lại → S42 |
| Lệnh xóa S56 トレーズ | Tương tự như trên, còn lại → S57 |
| S123／S124 | var11==0 → S42; var10==1 → S57 |
| S42 マーズとマーグ | Hệ thống thực và var9==0 → S43; ngược lại → S44 |
| S107 トールギス壊 | Chọn 1 “ロームフェラには従えない” (var38=0) → S49; Chọn 2 「あくまでもOZとして动く」（var38=1)→ S50 |
| S49 Địa ngục mặt trăng! | var37==0 → S51 → S52; var37==3 → S108 → S53 (S50 cũng → S108) |
| Chiến trường chiến tranh S70 | Chọn 1 (Theo Toru) → S74 → S75 → S76 → S91 (Kết hợp vào phần sau của OZ); Chọn 2 (Chiến đấu một mình) → S71 → S72 → S73 → S136 → S77 (Kết hợp vào phần sau của Quân đội Độc lập) |
| Tấn công căn cứ thiết giáp hạm S78 | Chọn 1 → S81; Chọn 2 (var36=0) → S79 → S129 → S81; Chọn 3 (var36=1) → S80 → S81 |
| S130 Trận đột phá quyết định (Phần 2) | var128==0 (cả hai phần đều ở vòng 10 của màn) → S82 → S84; ngược lại → S83 → S131 → S84 |
| S89 Đang mơ, lại đến | Chọn ムゲuniverse (var130==0) → S90 → S104; ngược lại → S103 → S104 |
| S139 Thức Tỉnh Giấc Mơ | Chọn vũ trụ (var129==0) → S102 → S104; ngược lại → S103 → S104 |

Khung lộ trình: điểm bắt đầu アーク S2, セレイン S3, ブラッド S0, マナミ S1 (`load_001090A0:801C69D0` viết `+0x99E`). Quân đội độc lập S31 → … → S38 → S128 → S39 → S40 → S41; OZ S46 → S47 → S48 → S140 → S107 → S49/S50; Quân đội Độc lập và CP chia sẻ S77–S90, S129–S133, S141 trong chiến đấu độc lập; OZ và CP chia sẻ với Toro S91–S101, S137–S139; S102 chỉ vào được qua S139, S90 chỉ vào được qua S89; S103–S106, S134 được dùng chung cho tất cả các tuyến.

**Số từ**: Từ bây giờ chỉ アーク/ブラッド mới được vào khi đủ điều kiện. Số từ dành cho người chơi khác sau đó ít hơn 1 (loại siêu) hoặc 2 (loại thật) so với thẻ Akurasu; "ここより公に" là tập thứ 31 của OZ và là tập thứ 32 của "Đội quân Độc lập". Bạn có thể tìm thấy số lượng từ được tính cho từng cảnh theo nhân vật chính và tuyến đường trong Phần 6 của bản thảo xác minh quy trình `flow-audit.md`.

**Trường hợp không thể truy cập**: Link Battler 109–122 chỉ được chèn thông qua mã gốc (xem [Liên kết Link Battler](link-battler.md)), mà không trỏ `3D4B`; dự trữ 125–127 sự kiện cổ phiếu với S0; S58 "Eternal のフォウ(ボツ)" và S46 Sự kiện được chia sẻ, phần cuối cũng chuyển sang S47; 142 chỉ có tiêu đề chương.

## 10. Vẫn chưa giải quyết được và xác nhận bằng máy thực tế

### 10.1 vẫn chưa được giải quyết

| Dự án | Nó bị kẹt ở đâu | Phương pháp xác nhận tối thiểu |
| --- | --- | --- |
| Sự khác biệt giữa giá trị trại hồ sơ triển khai 4 và 2 | Hàm tấn công `8020ABB4` ánh xạ cả hai vào trại 2; liệu giá trị 4 có được lưu và ảnh hưởng đến AI hay không (ví dụ: không tấn công phe của chúng tôi) cũng không được theo đuổi. Bạn cần kiểm tra việc sử dụng `800A6E68`/`800A84F8` cho `sp+0x2E` | S138 Chọn "Hợp tác" ở ván mở đầu để xem quân ハマーン có tấn công mình không |
| Mục đích của var117–122 | Lớp phủ chiến thuật `801CF2EC` (được gọi bởi `801CA97C`) thay đổi biến tương ứng từ 3 thành 0 trên phi công của máy bay 171–176 và gọi `802176A8` (chuyển chế độ hiển thị); bởi vì nó không được thiết lập lại khi nhập cảnh nên nó chỉ xảy ra một lần cho mỗi người. `801CF2EC` ​​tương ứng với hoạt động của người chơi nào chưa được theo dõi | Giám sát các bit var117–122 trong `8015E818` trong trò chơi mới và ghi lại thao tác khi nó thay đổi từ 3 thành 0 |

### 10.2 Đã rút ra kết luận và nên tiến hành đánh giá máy thật

| Dự án | Phương thức xác nhận tối thiểu |
| --- | --- |
| Quy tắc thuyết phục liền kề (3.1) | Người thuyết phục dựa vào đối tượng và không có "có thể nói" trong menu |
| アイナ điều kiện tiên quyết để chiến đấu | S11 Để シロー bám vào アイナ không đánh nhau xem có hợp lý không |
| アレンビー không nhất thiết phải vào cùng một vòng | S129 Sau khi ドモン thuyết phục, hiệp đấu kết thúc. Ở vòng tiếp theo, レイン thuyết phục và đội sẽ nhập đội khi hết đường chuyền |
| アレンビー S137 Thời gian rút lui | Ghi lại số lượng địch lúc cô rút lui sau khi 12 quân tiếp viện xuất hiện |
| ガラリア Điều kiện hủy bỏ | S20 Để các mecha khác đánh cô ấy cho đến hiệp thứ 4, xem cô ấy còn quay về phía chúng ta hay không; lần khác, hãy để Xiang chọn cách phản công khi cô ấy bị tấn công, và xem liệu cô ấy có chuyển đổi lần nữa không |
| ガラリア sẽ được chỉnh sửa sau khi chuyển sang bên chúng tôi | Kiểm tra danh sách trên màn hình chuẩn bị sau khi vượt qua cấp độ |
| フォウ Điểm chuẩn cấp độ | S128 Bài đọc mở đầu `D_8010F5F3` Kiểm tra trình độ với top 15 của chúng tôi |
| フォウ Bước 3 | S20 Thuyết phục フォウ trong file save của var2==1 và thấy rằng bạn sẽ vào phần quyết định chiến thắng ngay lập tức |
| リッシュ Tùy chọn IA | Chọn mục 1 ở S35, sang S38 và để セレイン dính vào リッシュ xem có hợp lý không |
| エルリッヒ Ngưỡng IA | Chọn mục 2 ở S27, chọn “Bỏ nó ra” ở S30, xem ở S41 có “âm thanh” không |
| ロゼ Không cần phải thuyết phục Maマーグ | S61 Không cần phải thuyết phục Maマーグ, khi ロゼ có mặt hãy dùng タケル hạ gục マーグ và xem ロゼ xuất hiện "Đang nói" |
| トッド, シルキー | Nếu chưa chiêu mộ được Kirara và đã bị thuyết phục 3 lần thì vào file save ở S92 và nhìn vào màn hình tìm quân tiếp viện ở vòng 3 (không phải vòng 2) |
| カーツ 100 bị bắn hạ | ブラッド 99 bắn hạ vào S124, bắn xong カーツ xem có được vào đội không |
| アイシャ CP chậm chi nhánh | S69 Nếu không áp đảo được số lượng kẻ địch, hãy xem アイシャ xuất hiện bên phe ta ở vòng thứ 3 màn hình |
| Sau khi アイシャ tham gia エルブルス | Sau khi tham gia mở danh sách đơn vị xem phi công エルブルス còn đó không |
| ガトー Tham gia nhóm | S49 Hãy để căn cứ nâng cao バスク và căn cứ nâng cao hàng đầu được lưu một lần để xem liệu bạn có thể nhận được GP02A sau khi lên cấp hay không |
| ガトー Rời đội | S138 Chọn "すべきではない" và sau khi vượt qua cấp độ hãy kiểm tra xem GP02A đã rời khỏi đội chưa |
| シュバルツ Ở lại trong đội | S137 Để Riko tấn công và vượt màn ngay từ đầu, xem シュバルツ trên màn hình chuẩn bị |
| Korra OZ xuất hiện | S56 ghi lại màn hình Korra thực sự xuất hiện |
| クェス cửa sổ thời gian | Đừng đánh シャア ở hiệp khi クェスム đến mà dùng アムロ để hạ gục nó ở hiệp tiếp theo để xem nó có gia nhập đội không |
| MASHIMARAー／キャラ Quân tiếp viện | S103 Xem quân tiếp viện cuối hiệp 7 và đầu hiệp 8 |
| Một trận chiến đột phá tuyệt vọng | Vượt qua cấp độ trong vòng thứ 10 để xem có vào S82 hay không; chỉ cho hạm vào vùng xanh xem có vượt qua không |
| ちずる dây chuyền phẫu thuật (N1) | S97 không tấn công コンバトラーV, ngựa báo bắn hạ <15, xem S99 có tấn công được không |
| Ma Dao Bò (N4) | S25 Hãy để ドレイク rút lui trước mà không đánh vào Ma Bò Đói (nó rút lui theo kịch bản), và xem Ma Dao Bò có xuất hiện ở cuối S26 hay không (xác nhận xem loại 2 có được kích hoạt bởi `3D46`) |
| ロザミア bị rớt | S37 Bắn hạ ロザミア mà thấy không có thông tin bộ phận nào (sẽ mất cơ hội tuyển dụng) |
| ダブルゴッドフィンガー OZ Line | OZ Line アレンビー Sau khi vào đội, để hai người ở cạnh nhau và có sức mạnh 130. Nhìn vào danh sách vũ khí Thần ガンダムH |
| Danh sách đội hình | Chọn vũ trụ ムゲ và vòng tròn trái đất một lần và xem liệu cả hai đều có sẵn hay không |

### 10.3 Phạm vi và sự lặp lại

- Không có trong kịch bản, bài viết này chỉ trích dẫn kết luận: Mở khóa trang phục EW và sửa đổi hoàn toàn ([Kế thừa biến hình](upgrade-inheritance.md)), Link Battler gia nhập đội ([Liên kết Link Battler](link-battler.md)), rớt thành phần và xác định kỹ năng tổng hợp (xem văn bản để biết địa chỉ mã).
- Tái tạo: Đầu vào là sự tháo rời của `stage_events.jsonl`, `stage_deployments.jsonl`, `stage_auxiliary.jsonl`, `actors.jsonl`, `units.jsonl`, `texts.jsonl` và `build/recomp/cpu-scan/` do `make recomp-data` sản xuất. Vòng thứ hai quét kịch bản và bản thảo từng mục (thuyết phục, nhân vật chính, đầu, giữa, cuối, quét toàn bộ, xử lý, thành phần, trang dữ liệu) là sản phẩm phân tích một lần và không được lưu trữ trong cơ sở dữ liệu; tất cả các địa chỉ sự kiện trong văn bản có thể được mở và xem trong trình duyệt dữ liệu.
- Để hỗ trợ "theo dõi tình trạng ẩn" của [Roadmap](../design/mod-roadmap.md) M3, bảng biến trong Mục 5.1 phải được củng cố thành dữ liệu khóa bố cục và được thử nghiệm; loại 9 "dành riêng" và loại 2/7 "phải là 3" trong thư mục `trigger.fields` cũng cần được sửa theo mục 3 và 4.

[wiki]: https://akurasu.net/wiki/Super_Robot_Wars/64/Secrets