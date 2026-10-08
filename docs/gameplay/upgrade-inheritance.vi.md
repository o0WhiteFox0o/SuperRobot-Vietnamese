> **Ngôn ngữ / Language:** [Tiếng Việt](upgrade-inheritance.vi.md) · [English](upgrade-inheritance.en.md) · [中文](upgrade-inheritance.md)

# Kế thừa chuyển đổi: Cách chuyển số kỳ thay thế và mục nào thực sự bị thiếu

Ngày: 2026-09-18. Phạm vi: ROM Rev 0 tiếng Nhật và tháo gỡ tĩnh của dự án này (`build/recomp/cpu-scan`), trích xuất thư mục cơ thể/vũ khí (`assets/original-data/records`). **Tất cả kết luận trong bài viết này đều đến từ phân tích tĩnh và không có trò chơi đang chạy nào để tái tạo**; các mục cần chạy để đưa ra kết luận được liệt kê trong Phần 7. So sánh BUG07/BUG08/LEAD01/WATCH01/WATCH02 của [Đăng ký lỗi gốc](original-bug-register.md).

2026-10-01 Đã thêm: `3D5A` Tham số thứ tư của 2000/3000/4000, thời gian gọi thay đổi thiết bị EW, sửa tên vũ khí bị thiếu của アースゲイン và Phần 10 (bổ sung triển khai không được kế thừa, số lượng phân đoạn quay trở lại của dòng W năm người theo lộ trình, `3D6C` toàn bộ Điều 38).

## 1. Tóm tắt kết luận

| Kết luận | Cơ sở |
| --- | --- |
| Việc "kế thừa" của việc thay đổi máy bay được điều khiển hoàn toàn bởi hai bảng cố định ROM: bảng tiền thân `D_800CA3A0` (30 cặp) xác định thân nào sẽ kế thừa và bảng ánh xạ vũ khí `D_800CB5E8` (114 mục) xác định số phân đoạn của vũ khí nào được chuyển sang vũ khí nào | `800AA814`, `800AA8F4` |
| Nguồn kế thừa không phải là số máy cũ được ghi trong script. Máy bay cũ trong kịch bản chỉ được sử dụng để xóa; nguồn kế thừa là nguồn được tìm thấy bằng cách nhấn **New Body** trên bảng tiền nhiệm và nó vẫn phải có trong danh sách vào lúc này | `800AAD28` Bước 4 và 5 |
| Năm phần của cơ thể được sao chép trong một khối và được truyền sang các dạng biến đổi/kết hợp khác | `800AA8C0`, `800AAB5C` |
| Các phân đoạn vũ khí được di chuyển từng mảnh theo bảng ánh xạ; vũ khí không có mục trong bảng sẽ luôn dừng ở 0, ngay cả khi máy mới có vũ khí kế nhiệm có cùng tên và cùng giá trị | `800AA8F4` chu kỳ vũ khí |
| Ba nghi ngờ thiếu sót dữ liệu: Bộ tản nhiệt ngọn lửa của Lenovo và bộ phát lửa của Goreドラゴンファイヤー (EW Dressup). Những vũ khí này của máy cũ và mới đều có cùng tên và tất cả các giá trị đều giống nhau ngoại trừ sức tấn công cơ bản, nhưng không có mục bản đồ | Phần 4 |
| `800AA8C0` được sao chép cùng với giới hạn trên sửa đổi (`+0x51`), nhưng `800AAB5C → 800A5254` tiếp theo sẽ tải lại bản ghi ROM của chính máy mới và ghi lại giới hạn trên, **không có tác động thực sự**; cuộc gọi tương tự cũng tính toán lại năm giá trị và sức mạnh của từng loại vũ khí theo số lượng phân đoạn được kế thừa | Phần 5 |
| Hầu hết các mục trong "Nâng cấp bị mất" của Akurasu không phải là vấn đề về mã kế thừa: tập lệnh trước tiên bị xóa bằng `3D5A …,4000`, cả con người và máy, sau đó được đăng ký lại khi quay lại. Người tiền nhiệm không còn nên đương nhiên không có người thừa kế | Phần 6 |

## 2. Đường dẫn mã

### 2.1 Lối vào

| kích hoạt | vị trí | mẫu cuộc gọi |
| --- | --- | --- |
| Script `3D5A` (tham số thứ 4 < 2000, trong đó có 500 dành cho "không xóa máy cũ"; ≥ 2000 để xóa, xem 2.4) | `800A0BA8` → `800AAD28` | `(角色, 参数, 新机, 旧机)` |
| Thay đổi thiết bị tự động Waltz vô tận | `load_0008F4B0:801CF85C` (điểm gọi duy nhất `801D0028`, tức là màn hình chuyển đổi **sau khi xác nhận năm lần chuyển đổi**) bảng vòng lặp `D_801DC6E4` (5 cặp), khi năm số phân đoạn **tất cả** đạt đến phiên bản `+0x51`; không tài xế nào cũng có thể thay đổi, và số phân khúc vũ khí không tham gia | `800AAD28(驾驶员或 999, 目标机, 0, 旧机)`, máy cũ là máy tiền nhiệm và phải kế thừa |
| Trường hợp đặc biệt của ガンダムmkⅡ 343 → 56 | `load_000AB160:802116CC` | Chức năng tương tự |
| Chỉ đăng ký máy bay (vai trò 999) | `800AAD28` → `800A9A70` | Logic lưu/ghi lại giống như đường dẫn chính |

`D_801DC6E4`(5 Có, nó phù hợp với bản ghi hướng dẫn):ウイングゼロ→ウイングゼロカスタム、ヘビーアームズ开→ヘビーアームズカスタム、デスサイズH→デスサイズHカスタム、アルトロン→アルトロンカスタム、サンドロック开→サンドロックカスタム. Điều kiện kích hoạt chỉ nhìn vào năm biến thể cơ thể, không nhìn vào sửa đổi vũ khí.

### 2.2 Trình tự thực thi `800AAD28`

1. Đã có "nhân vật này + nội dung này" trong danh sách → quay lại trực tiếp (các cuộc gọi lặp lại là bình thường và tập lệnh gốc dựa vào bước này để đăng ký lặp lại ở nhiều nơi).
2. Máy mới là 224 ダンクーガ → Giao cho `800ACB74`: Thay đổi số của instance 223 đang sử dụng thành 224 và loại bỏ tất cả các thành phần. Sau khi trả về giá trị khác 0, hàm main sẽ kết thúc trực tiếp. Vì thế Dancouga không bị xếp vào bảng thừa kế.
3. Ký tự 999 (chỉ đăng ký tàu bay) hoặc tàu bay 999 (chỉ đăng ký phi công) mỗi ký tự có một nhánh duy nhất.
4. **Lấy phiên bản tiền thân**: `800AA814` sử dụng số nội dung mới để tìm số nội dung tiền thân trong `D_800CA3A0`, sau đó quét 140 bảng phiên bản nội dung, lấy phiên bản hoạt động **đầu tiên** của số này (không kiểm tra xem ai là người điều khiển) và lưu trữ `+0x4C..+0x51` sáu byte và tất cả vũ khí (số, số phân đoạn, bộ ba cờ) trên ngăn xếp. Không thể tìm thấy người tiền nhiệm → Việc kế thừa sẽ không được thực hiện sau này.
5. `800AA464(角色, 新机, 脚本给的旧机)`: Hủy bỏ mối quan hệ giữa phi công và máy hiện tại và xóa phiên bản có số bằng **Script Old Machine**. Ở chế độ 500, số máy cũ là 500 nên máy cũ sẽ **giữ nguyên trong danh sách và trở thành máy bay không người lái**.
6. Phiên bản máy mới: Nếu đã có trong danh sách, hãy sử dụng lại (nếu có trình điều khiển trên đó, hãy xóa nó trước), nếu không thì tạo một phiên bản mới theo bảng trình điều khiển mặc định `D_800CA418`.
7. Nếu lấy được phần trước ở bước 4: `800A5C18` Tính lại giá trị cơ bản → `800AA8F4` Viết lại tính kế thừa → `800AAB5C` Truyền bá số năm đoạn sang các dạng biến dạng/kết hợp khác.

Bước 4 nằm trước bước 5 và 6, do đó, thứ tự "lưu trước rồi xóa" không có vấn đề gì; vấn đề là phần trước đã bị xóa trong một sự kiện tập lệnh trước đó (phần 6).

### 2.3 `800AA8F4`: Tất cả các quy tắc kế thừa

- `800AA8C0`: Ghi sáu byte đã lưu trở lại máy mới `+0x4C..+0x51`, tức là năm số phân đoạn** và giới hạn trên sửa đổi**.
- Các dạng khác trong họ biến dạng (`D_800CB40C`/`D_800CB5A4`) và họ kết hợp (`D_800CAC94`/`D_800CAEF0`) cũng được viết trong cùng một khối sáu byte.
- Vũ khí: Với mỗi vũ khí đã lưu, hãy tra cứu "số vũ khí cũ" trong `D_800CB5E8`. Sau một đòn đánh, hãy tìm "số vũ khí mới" trong mảng phiên bản vũ khí mới (`+0x2C` số lượng, con trỏ `+0x30`, bước 0x24) và ghi số phân đoạn vào `+0x16`. Không thể tìm thấy nó trong bảng hoặc máy mới không có vũ khí mục tiêu → máy mới sẽ để vũ khí này ở mức 0.
- Bảng này mang tính toàn cầu, không phân biệt các cặp tàu bay; sau khi nhấn cái đầu tiên, bạn sẽ không tìm kiếm thêm nữa. Không có số nguồn trùng lặp trong số 114 mặt hàng hiện tại, vì vậy việc "chỉ lấy mặt hàng đầu tiên" này sẽ không có bất kỳ tác động nào trong thời điểm hiện tại.
- Xử lý bổ sung duy nhất: Weapon 314 ファンネルMAP sẽ kế thừa bit 2 (bit mở khóa) của `+0x22`.

### 2.4 Hướng dẫn liên quan và bỏ qua

| Mục | Hành vi |
| --- | --- |
| `3D6C` (`800ACA1C`) | Chỉ tìm phiên bản đầu tiên của số này trong nhóm của chúng tôi (không làm gì nếu không tìm thấy nó). Năm mục được viết là `min(段数, 上限)`, sau đó `800A95DC` ghi số lượng phân đoạn của tất cả vũ khí trên máy bay có cùng giá trị. Ghi đè vô điều kiện có thể làm giảm số lượng phân đoạn được kế thừa. Kịch bản gốc 38, xem phần 10 |
| `3D5A` Tham số thứ 4 ≥ 2000 | `800A3540`: **2000 chỉ xóa trình điều khiển, 3000 chỉ xóa phần nội dung và 4000 xóa cả trình điều khiển và nội dung**; bỏ qua việc xóa khi ký tự đạt 999 (`800A355C`–`800A35CC`, `xori 0xFA0／0xBB8／0x7D0`), tập lệnh gốc 3000 đều được gọi với vai trò 999, không hợp lệ. Bất kỳ "máy mới đã đăng ký" nào sau 4000 sẽ không còn được kế thừa (2026-10-01 bổ sung 2000/3000) |
| `3D5A` Chế độ 500 | Máy cũ không bị xóa và vẫn nằm trong danh sách lái xe không người lái |
| `3D6A` Chế độ 3 (`800AB808`) | ゴッドマーズ Fusion: xóa phiên bản ガイヤー, thay đổi con trỏ trình điều khiển, **không có số phân đoạn nào được sao chép** |
| Màn hình chuyển đổi (`load_0008F4B0`) | Năm vật phẩm (`801CFA78`) và mỗi vũ khí (`801D130C`) có giới hạn ở cùng `+0x51` và mỗi vũ khí +1 +1 |
| Nguồn của phiên bản máy bay `+0x51` | Bản ghi ROM máy bay `+0x20` (`800A5330`). Đây là giới hạn sửa đổi trên cho từng thân máy |

## 3. Bảng tiền nhiệm `D_800CA3A0` (30 cặp) so với giới hạn trên

Giới hạn trên được lấy từ bản ghi ROM nội dung `+0x20`. Giới hạn trên được liệt kê để ghi lại hai trường hợp riêng biệt (サンドロック 6, マジンガーZ 12); như đã đề cập ở Phần 5, bản thân giới hạn trên không bị tính kế thừa lấy đi.

| Người tiền nhiệm | Giới hạn trên | Máy Mới | Giới hạn trên |
| --- | --- | --- | --- |
| 3 シャイニングガンダム | 9 | 1 ゴッドガンダム | 9 |
| 53 アルビオン | 13 | 51 アーガマ | 13 |
| 51 アーガマ | 13 | 63 ネェル・アーガマ | 13 |
| 63 ネェル・アーガマ | 13 | 69 ラー・カイラム | 13 |
| 119 ウイングゼロ | 7 | 121 ウイングゼロカスタム | 7 |
| **124 ガンダムサンドロック** | **6** | **126 ガンダムサンドロックthay đổi** | **7** |
| 126 Kai | 7 | 125 サンドロックカスタム | 7 |
| 127 ガンダムデスサイズ | 7 | 128 ガンダムデスサイズH | 7 |
| 128 ガンダムデスサイズH | 7 | 129 デスサイズHカスタム | 7 |
| 130 ガンダムヘビーアームズ | 7 | 132 sửa đổi | 7 |
| 132 ガンダムヘビーアームズ Kai | 7 | 131 ヘビーアームズカスタム | 7 |
| 133 シェンロンガンダム | 7 | 115 アルトロンガンダム | 7 |
| 115 アルトロンガンダム | 7 | 116 アルトロンカスタム | 7 |
| 171/172/173 ゲッター1/2/3 | 7 | 174/176/175 ドラゴン/ライガー/ポセイドン | 7 |
| 174/176/175 | 7 | 177/178/179 真・ゲッター1/2/3 | 7 |
| 223 ダンクーガ | 9 | 224 ダンクーガ | 9 |
| **262 マジンガーZ** | **12** | **263 マジンガーZ(JS)** | **13** |
| 273 レイズナー | 9 | 270 ニューレイズナー | 9 |
| 30 phút | 9 | 31 アシュクリーフ | 9 |
| 32 スヴァンヒルド | 9 | 33 ラーズグリーズ | 9 |
| 34 アースゲイン | 11 | 306 スーパーアースゲイン | 11 |
| 36 スイームルグ | 11 | 307 スイームルグS | 11 |
| 259 アフロダイA | 15 | 260 ダイアナンA | 15 |
| 65 メタス | 11 | 67 メタス开 | 11 |
| 73 100 Shiki | 9 | 295 フルアーマーHundred Shiki Kai | 9 |
| 77 キュベレイmkⅡ | 9 | 323 キュベレイmkⅡ | 9 |

Giới hạn trên của vòng tra cứu bảng là 30 mục (`800AA814`: `sltiu v0,v1,0x1E`) và mục thứ 31 `247/181` ngay sau trong ROM là dữ liệu bên ngoài bảng và sẽ không bao giờ được đọc. Trong tập lệnh gốc, ba cặp 127→128, 130→132 và 133→115 sẽ không bao giờ được kích hoạt (máy cũ đã bị `4000` xóa khi máy mới được đăng ký) và 124→126 chỉ thực sự được kế thừa trên con đường hoàn toàn yên bình (Mục 10, 2026-10-01).

Có **trao đổi không có** trong bảng:ミデア→アウドムラ、アウドムラ→アルビオン、ウイングガンダム→ウイング, Chờ đã. Những nâng cấp này không được kế thừa, phù hợp với "Nâng cấp bị mất" của Akurasu.

## 4. Kết quả bảng ánh xạ vũ khí theo từng cặp `D_800CB5E8` (114 mục)

"Mất" có nghĩa là số giai đoạn sửa đổi của vũ khí được đặt lại về 0 sau khi vũ khí được thay thế. Bảng sau chỉ liệt kê các mục còn thiếu; Dancouga không được áp dụng do lộ trình thay đổi số tại chỗ.

| Đổi điện thoại | Mất vũ khí | Điện thoại mới có vũ khí tương ứng |
| --- | --- | --- |
| シャイニングガンダム→ゴッドガンダム|シャイニングショット、シャイニングフィンガー、シャイニングフィンガーソード | Máy mới không có vũ khí cùng tên (vũ khí được thay thế toàn bộ) |
| アーガマ→ネェル・アーガマ | Pháo trên không | Không có |
| サンドロック→Thay đổi | クロスクラッシャー | Không có (mục này không thay đổi) |
| サンドロック开→カスタム | ホーミングミサイル、シールドフラッシュ、ビームマシンガン | Không có (phù hợp với việc giảm vũ khí tác chiến điện tử được ghi trong hướng dẫn) |
| デスサイズ→H | マシンキャノン | Không có |
| デスサイズH→カスタム | バスターシールド | Không có |
| ヘビーアームズ开→カスタム | アーミーナイフ | Không có |
| アルトロン→カスタム | ビームキャノン | Không có |
| **アルトロン→カスタム** | **ドラゴンファイヤー（470)** | **Có: 1291 ドラゴンファイヤー, sức tấn công 2000→2400, các giá trị khác giữ nguyên** |
| ゲッター1/2/3→ドラゴン, v.v. | ゲッターアーム, ドリルストーム, ドリルパンチ | Không trùng tên |
| Tương tự như trên | **ツインビーム（1228）** | **Có: 1244 ツインビーム, hồ sơ hoàn toàn giống nhau (kỹ năng kết hợp, xem phần 7)** |
| ドラゴンン→真・ゲッター|スピンカッター、ゲッターサイクロン、チェーンアタック、ツインビーム(1244) | Không trùng tên |
| **レイズナー→ニューレイズナー** | **Bộ tản nhiệt chữa cháy (1070), グレネードランチャー (1072)** | **Có: 1057 Bộ tản lửa (sức tấn công) 1200→1400), 1059 グレネードランチャー (1400→1600), các giá trị khác giữ nguyên** |
| スヴァンヒルド→ラーズグリーズ | グレネードランチャー | Không có |
| アースゲイン→スーパー | Vuốt Sói (147), Nanh Sói (149) | Không trùng tên (siêu mẫu đổi vũ khí). 2026-10-01 Sửa tên vũ khí (trước đây viết là "Mắt, Hai Móng, Hai Răng"); Thiên Long Diệt Quỷ Trận (1219) là một kỹ năng tổng hợp không thể sửa đổi một mình nên không bị mất |
| アフロダイA→ダイアナンA | Sửa chữa thiết bị (1009) | Có: 1012 thiết bị sửa chữa, hồ sơ giống nhau (xem Mục 7 để biết có thể sửa đổi được không) |
| メタス→メタス开 | Sửa Chữa Thiết Bị (269) | Có: 274 Thiết bị sửa chữa, giống như trên |
| 100-Shiki→Haku-shiki Kai | Pháo 60mm バルカン, クレイバズーカ | Không có |

Có một **mục nhập chết** khác: `1021 ドリルミサイル → 1028 ドリルミサイル`. 1021 không có trong bất kỳ danh sách vũ khí nào của máy (Megatron Z không có vũ khí này trong tay), vì vậy bản đồ này sẽ không bao giờ trúng.

Một mục có vẻ sai về tên nhưng có vẻ hợp lý về giá trị: `219 対空レーザー砲 → 210 対空機関砲` của アーガマ có một `211 対空レーザー砲` khác có cùng tên. Tất cả các giá trị của 219 và 210 đều hoàn toàn giống nhau và 211 mạnh hơn nên mục này khớp theo giá trị chứ không phải theo tên. Bài viết này không đánh giá nó là mục còn thiếu, nhưng khi thay đổi bảng ánh xạ, hãy cẩn thận để không “sửa dễ dàng”.

## 5. Giới hạn trên của sửa đổi: sao chép, nhưng sau đó đặt lại

`800AA8C0` sao chép sáu byte và byte thứ sáu là giới hạn trên `+0x51`; đường dẫn đơn phương của `800A9A70` cũng ghi giới hạn trên của máy tiền nhiệm vào máy mới trước tiên. **Nhưng sau đó, cả hai đường dẫn sẽ gọi `800AAB5C`** và điều đầu tiên `800AAB5C` thực hiện là `800A5254(新机, 1)`: hàm này đọc lại bản ghi ROM 36 byte của chính nó với số máy bay, ghi `+0x20` vào `+0x51` (`800A5330`) và nhấn `+0x4C..+0x50` tính toán lại HP/EN/Tính cơ động/Giáp/Giới hạn và tính toán lại sức mạnh của vũ khí từng phần (vòng lặp bắt đầu từ `800A55F4`: đọc lại bản ghi ROM vũ khí để lấy sức tấn công cơ bản, sau đó cộng nó từ `D_800CA590` theo số phân đoạn `+0x16` của vũ khí). Vòng lặp truyền mẫu của `800AAB5C` cũng gọi `800A5254` cho mỗi mẫu đang hoạt động.

Do đó, bản sao giới hạn trên chỉ mang tính tạm thời: không có mã nào đọc `+0x51` từ `800AA8C0` đến `800AAB5C` và cuối cùng mỗi máy sử dụng giới hạn trên trong bản ghi ROM của chính nó. **Đây không phải là lỗi và không cần chỉnh sửa. **

Nhân tiện, hai trường hợp mồ côi dữ liệu được giữ lại (không liên quan đến kế thừa, chỉ ảnh hưởng đến chính máy): trong số 363 máy trong toàn bộ bảng, chỉ có một 124 ガンダムサンドロック có giới hạn trên là 6 và chỉ một 262 マジンガーZ có giới hạn trên là 12; người kế vị của họ lần lượt là 7 người. và 13, và các thiết bị TV dòng W khác đều là 7. Giới hạn trên đồng thời hạn chế năm vật phẩm và mỗi loại vũ khí (`801CFA78`, `801D130C`), đồng thời xác định điểm kích hoạt thay đổi EW (từ `801CF8AC`, so sánh từng vật phẩm với `+0x51`).

Phần này cũng giải thích điểm sửa khi kế thừa các vật phẩm bị thiếu: sau khi số đoạn được ghi vào `+0x16`, sức mạnh được chính trò chơi tính toán lại trong `800AAB5C` nên việc sửa phải diễn ra sau khi `800AA8F4` trả về và trước `800AAB5C`.

## 6. So sánh hai bảng Akurasu

| Vật phẩm chiến lược | Các cơ chế được tìm thấy trong dự án này | Phán quyết |
| --- | --- | --- |
| Medea→Audhumla, Audhumla→Biến đổi Albion bị mất | Không có hai cặp trong bảng trước đó; tập lệnh `3D5A 46,4,52,64`/`…,53,52` chỉ là sự thay đổi của máy, không được kế thừa | Đây là quy tắc, không phải lỗi mã |
| Gaia→Godmars bị mất | Vào `3D6A` chế độ 3, `800AB808` chỉ xóa ガイヤー và thay đổi con trỏ, không copy | Các quy tắc là như thế này |
| Cỗ máy thuộc dòng W (Sandrock→Kai, Deathscythe→H, Heavyarms→Kai, Shenlong→Altron) đã bị mất, nhưng cỗ máy mới có 3 phân đoạn | Tập lệnh sẽ bị xóa với `3D5A …,4000` trong trường hợp rời khỏi nhóm (chẳng hạn như cảnh 032/036/046) và khi quay lại, hãy sử dụng chế độ 500 để đăng ký hoặc tham gia với các bản ghi triển khai. Người tiền nhiệm không còn tồn tại → không có quyền thừa kế. Số lượng đoạn hồi quy **khác nhau tùy theo lộ trình**: có 0, 3 và 5 đoạn chứ không phải cả 3 đoạn (Section 10, 2026-10-01) | Luồng tập lệnh, lỗi mã không được kế thừa. Sự mất mát thực chất xảy ra ở đoạn **rời nhóm** chứ không phải ở đoạn đổi điện thoại |
| Wing Zero (Hiro) bị mất tích ở OZ 36 | `3D5A 95,0,119,4000` đã bị xóa ở cuối cảnh 057 và `…,119,500` đã được tạo ở cảnh 073; và 117→119 không có trong danh sách tiền thân. Bổ sung 2026-10-01: Thứ đã bị xóa ở cuối OZ Chương 33 là chiếc Zero có cánh bay tạm thời do Jacks điều khiển (nhóm triển khai 3, giai đoạn 0); gundam thế hệ tiếp theo được Hero sử dụng trước đây đã được trao cho Jack theo cách tái sử dụng cùng với các sửa đổi (`001C7984@248`), do đó không có sửa đổi nào bị mất trong tuyến đường OZ | Tương tự như trên |
| Chuyển đổi và thiết lập lại sau khi Spiegel rời đội và sau đó gia nhập lại (BUG07) | Trong nhiều trường hợp rời khỏi đội, `3D5A 3,0,0,4000` (xóa toàn bộ nội dung) đã được sử dụng và khi gia nhập lại, anh ấy đã sử dụng chế độ 500 để tạo một chế độ mới; máy bay không có trong danh sách của người tiền nhiệm | Tập lệnh sử dụng "Xóa toàn bộ nội dung" thay vì chế độ 2000, chỉ xóa phần thí điểm; cho dù đó là sự lựa chọn thiết kế hay sự thiếu sót đều cần có cơ sở cốt truyện |
| レイズナー→ニューレイズナー Thiếu sửa đổi súng phun lửa (BUG08) | Bảng ánh xạ bị thiếu 1070→1057, **cũng thiếu 1072→1059** | Nghi ngờ thiếu dữ liệu, hướng dẫn chỉ đề cập đến một trong số đó |
| Một số vũ khí trong phiên bản EW không được kế thừa chính xác (LEAD01) | Sự biến mất của vũ khí Sa mạc/Máy gặt/Vũ khí hạng nặng thuộc về việc bản thân vũ khí đó bị hủy bỏ; nhưng アルトロンカスタム của ドラゴンファイヤー có tồn tại (1291) nhưng không có bản đồ |アルトロンドラゴンファイヤー hiện là ứng cử viên cụ thể duy nhất phù hợp với LEAD01 |
| Linh kiện bị loại bỏ khi thay máy và tự động tấn công | `800ACB74` (ダンクーガ) được gọi rõ ràng là `800A9D60` để loại bỏ các thành phần; việc xử lý thành phần của các đường dẫn khác chưa được kiểm tra trong vòng này | Chưa được xác minh, dành riêng để theo dõi |

## 7. Các mục chưa được xác minh

Tất cả những điều sau đây cần phải chạy trò chơi để đưa ra kết luận. Vòng này chưa được chạy. `config/recomp/mini-stages/inherit.json` đã chuẩn bị bốn trường hợp sử dụng (Layzner, Altron→Custom, Albion→Argama và "việc đăng ký lại khi máy cũ vẫn còn trong danh sách có bao gồm số lượng phân đoạn máy mới") theo phương pháp viết của [cấp độ nhỏ](../script/mini-stage.md). Nó có thể được biên dịch và chạy trực tiếp; Cách sử dụng trước tiên là ghi `3D6C 机体,N` để ghi tất cả vũ khí của máy cũ vào cùng một số phân đoạn, sau đó nó sẽ luôn bằng 0 sau khi thay đổi máy. vũ khí không được thừa kế.

1. Hiệu suất thực tế của ba thiếu sót đáng ngờ (1070/1072/470) trên máy thật.
2. Số lượng phân đoạn vũ khí của phiên bản máy mới được tạo bắt đầu từ 0 (về mặt cấu trúc, điều này đúng, nhưng `800A6B30` được sao chép từ bản ghi mẫu khi bảng được tạo và không được xác nhận từng khung).
3. ~~ダンクーガ's 対空剣: Mẫu 223 sử dụng 873, mẫu 224 sử dụng 880, cả hai đều là các trường hợp vũ khí khác nhau và hướng `880 → 873` trong bảng ánh xạ ngược lại với tất cả các mục khác (nguồn chỉ dành cho máy mới và mục tiêu là dành cho máy cũ). Vì đường dẫn thay đổi số tại chỗ hoàn toàn không kiểm tra bảng nên bạn cần xác nhận xem biến đổi 対空剣 trên 223 có còn ở 224 hay không. ~~ 2026-09-18 Giải pháp tĩnh: Tên vũ khí là Sky Sword; ダンクーガ. Danh sách vũ khí của cả nhà có 873 và 880 cùng lúc. Sau mỗi lần sửa đổi màn hình sửa đổi, `800A5F84` sẽ đồng bộ hóa nguồn và số đoạn với mục khác. Số được thay đổi tại chỗ mà không cần di chuyển mảng vũ khí nên sẽ không bị mất ([Số phân đoạn chuyển đổi](upgrade-limits.md) Phần 5).
4. ~~Có thể sửa đổi các thiết bị sửa chữa (1009→1012, 269→274) và các kỹ năng kết hợp (1228→1244) một cách độc lập không? Nếu không, hai loại “tổn thất” này không có tác động thực tế. ~~ 2026-09-18 Giải pháp tĩnh: Cả hai loại đều là loại chuyển đổi 0; thiết bị sửa chữa có sức mạnh bằng 0 và bị từ chối trước khi nhập xác nhận (`801D0970`), còn ツインビーム có vị trí kỹ năng tổng hợp và không vào danh sách chuyển đổi (`801C7254`). Không có phân đoạn nào trong số chúng có thể được sửa đổi riêng lẻ và việc thiếu các mục này trong bảng ánh xạ không có tác động thực tế ([Số lượng phân đoạn được sửa đổi](upgrade-limits.md) Phần 6.1).
5. MaジンガーZ no Maドリルミサイル (1021 không có trong bất kỳ danh sách vũ khí nào) có phù hợp với chiến lược không?
6. Liệu máy bay không người lái cũ bị bỏ lại ở Chế độ 500 có thực sự xuất hiện trên màn hình danh sách/bảo trì trong quy trình ban đầu không?
7. Nguy cơ ghi đè "kế thừa lại khi sử dụng lại máy hiện có": Nếu máy tiền nhiệm và máy kế nhiệm cùng nằm trong danh sách, việc đăng ký lại sẽ ghi đè máy kế thừa bằng số phân đoạn của máy tiền nhiệm (`800AAD28` bước 6 và 7). Liệu sự kết hợp tuyến đường như vậy có tồn tại trong kịch bản gốc hay không vẫn chưa được điều tra từng cái một.

## 8. Phương án điều chỉnh tùy chọn (8.1, B0 và 8.5 đã triển khai, còn lại chưa triển khai)

Nguyên nhân của ba loại vấn đề này là khác nhau và những thay đổi về luật pháp cũng như chi phí cũng rất khác nhau. Các chi phí được liệt kê từ nhỏ đến lớn. Tiền đề chung: Theo thỏa thuận của [Sửa đổi quy tắc tùy chọn](rule-fixes.md), danh mục sửa đổi được bật theo mặc định và danh mục độ khó bị tắt theo mặc định. Khi đóng, máy chủ chỉ gọi hàm ban đầu; ROM và định dạng lưu trữ không thay đổi.

### 8.1 Chỉnh sửa A: Thêm ba ánh xạ vũ khí (được triển khai vào ngày 18-09-2026, chưa được xác minh trên máy thực tế)

Tương ứng với BUG08 và LEAD01, bề mặt sửa đổi là nhỏ nhất và ranh giới rõ ràng nhất. Công tắc `weapon-inherit-map` được phân loại vào danh mục chỉnh sửa (nó được bật theo mặc định và có thể tắt trong trò chơi "Tùy chọn → Điều chỉnh lối chơi"); để triển khai, hãy xem `inherit_missing_weapons` của `src/host/rule_fixes.hpp` và `resident_func_800AA8F4` của `game_hooks.cpp`. Bài kiểm tra đơn vị nằm trong `tests/native_rule_fixes.cpp`. **Chưa chạy trong trò chơi**, việc xác minh Phần 7 vẫn cần được thực hiện.

| Mục | Nội dung |
| --- | --- |
| id | `weapon-inherit-map` |
| ràng buộc | `NATIVE_HOOKS` trong số `tools/recomp/toolchain/generate_cpu.py` tăng lên `"resident_func_800AA8F4": "srw64_original_weapon_inherit"`, sau đó là `make recomp-cpu` |
| Địa điểm đóng gói | Đã thêm `resident_func_800AA8F4` trong `src/host/game_hooks.cpp`: gọi hàm ban đầu trước rồi viết ba cặp ánh xạ |
| Thông số | `a0` = phiên bản máy mới; `a1` = mảng vũ khí máy cũ đã lưu (4 byte mỗi mảnh: số u16, số phân đoạn u8, cờ u8); `a2` = số mảnh; `a3` = số phân đoạn 6 byte đã lưu |
| Bảng bổ trợ | `{1070→1057}` (bộ phát lửa), `{1072→1059}` (グレネードランチャー), `{470→1291}` (ドラゴンファイヤー) |
| Viết gì | Tìm số cũ trong `a1` và lấy số phân đoạn của nó. Tìm số mới trong mảng vũ khí mới (`+0x2C` số mảnh, `+0x30` con trỏ, bước 0x24, `+2` số) và viết `+0x16`. **Không sử dụng nguồn**: Hai điểm gọi `800AA8F4` (`800AB2F8`, `800A9CB0`) được theo sau bởi `800AAB5C → 800A5254` và công suất sẽ được tính lại theo số đoạn (phần 5) |
| Phạm vi tác dụng | Chỉ ba cặp trao đổi máy bay này mới có hiệu lực và chúng sẽ chỉ có hiệu lực đối với việc trao đổi máy bay mà “người tiền nhiệm vẫn còn trong danh sách”; các máy bay khác và các đường bay khác hoàn toàn không thay đổi |
| Lưu trữ Tác động | Số lượng phân đoạn được ghi vào danh sách là liên tục. Công tắc chỉ hoạt động tại thời điểm thay thế xảy ra. Việc bật hoặc tắt sẽ không làm hỏng bánh răng cũ nhưng việc thay thế đã xảy ra sẽ không được đền bù hồi tố |

~~Sau khi Xác nhận Mục 7, Mục 4, ba ứng cử viên nữa có thể được xem xét: `1228→1244` (Kỹ thuật hợp nhất), `1009→1012` và `269→274` (Thiết bị sửa chữa). ~~ Mục 7, Mục 4 đã xác nhận tĩnh rằng những vũ khí này không thể sửa đổi riêng lẻ và không cần phải sửa chữa.

### 8.2 Không cần thay đổi: giới hạn trên của phép biến đổi

Mục 5 đã xác nhận rằng giới hạn sao chép `800AA8C0` được đặt lại bởi `800A5254`, khiến cho việc chuyển đổi `upgrade-cap-keep` ban đầu trở nên không cần thiết.

### 8.3 Fix B: Thiếu cấp độ script

Hầu hết các "Nâng cấp bị mất" trong Akurasu (máy chơi game giữa dòng W, Spiegel, Mizuno, Ayaru và Gyro) không phải là vấn đề với bảng, mà là do tập lệnh sử dụng `3D5A …,4000` để xóa cả người chơi và máy, đồng thời số tiền mà người chơi đầu tư sẽ biến mất cùng với phần thân ngẫu nhiên. Trong ba phương pháp sửa đổi, **hoàn tiền là phương pháp hạn chế nhất**:

#### B0: Hoàn lại tiền chuyển đổi khi bị xóa (được triển khai dưới dạng điều chỉnh độ khó `upgrade-refund` vào ngày 18 tháng 9 năm 2026, xem [Sửa đổi quy tắc tùy chọn](rule-fixes.md) §2.6)

Nó không thay đổi đường cong sức mạnh của bất kỳ máy bay nào, cũng như không cho phép kích hoạt trước việc thay đổi thiết bị EW. Nó chỉ trả lại số tiền "lãng phí" và người chơi có thể quyết định lại nên đầu tư vào máy bay nào. Tính khả thi đã được kiểm tra trong mô hình giá:

| Mục | Dữ liệu gốc |
| --- | --- |
| Năm đơn giá cơ thể | Năm bảng 15 đoạn `D_801DC36C`(HP)/`3AC`(EN)/`3EC`(di chuyển)/`42C`(áo giáp)/`46C`(giới hạn), giá dựa trên **số lượng phân đoạn hiện tại**, **không liên quan đến cơ thể**. Ví dụ: HP mỗi phần 2000, 4000… 30000; Chuyển động 5000, 8000… 65000 |
| Đơn giá vũ khí | Chọn một trong bốn bảng gồm 16 mục theo loại sửa đổi vũ khí (bản ghi vũ khí `+0x0E` → ví dụ `+0x15`), sau đó lấy giá theo số phân đoạn hiện tại (ví dụ: loại 4 sử dụng `D_801DC6FC[段数]`), **không liên quan gì đến giới hạn trên của thân máy**. 18-09-2026 Sửa lại: `D_801DC340[上限−5]` viết trong văn bản gốc là bảng chuỗi thanh tỷ lệ, không phải bảng giá. Xem [Cải tạo các phân đoạn](upgrade-limits.md) Phần 3 |
| Số tiền chi tiêu | Đối với mỗi vật phẩm/vũ khí, chỉ cần tổng hợp đơn giá bằng 0...số giai đoạn hiện tại - 1, chủ nhà có thể tính toán hoàn toàn |
| Tài trợ | `D_8010F5F4`(u32) |

Ba điều cần giải quyết khi hạ cánh (để biết chi tiết triển khai, hãy xem [Sửa đổi quy tắc tùy chọn](rule-fixes.md) §2.6):

1. **Những thao tác xóa nào sẽ được khôi phục**: Chỉ những thao tác xóa "sẽ không được kế thừa" mới được khôi phục. `800AA3C4` là lối thoát duy nhất để xóa phiên bản sinh vật (người gọi `800AA464` hai lần, `800AB808`, `800A7DEC` và màn hình bán hàng `801C3678`), nhưng bản thân nó không biết ngữ cảnh cuộc gọi. Quá trình triển khai bao gồm `800AA464` và `800AB808` dưới dạng phạm vi hoàn tiền (`800A7DEC` và doanh số bán hàng không nằm trong số đó) và bao gồm `800AAD28`: Tìm phiên bản sẽ được kế thừa lần này theo bảng trước đó. Nếu trường hợp này bị xóa, bạn sẽ không được hoàn lại tiền. Ngoài ra, chỉ nhóm phiên bản của chúng tôi (nhóm thứ 0 của `800A6E68`) mới được hoàn tiền và các giai đoạn `3D6C` được đưa ra trong cốt truyện sẽ không được hoàn tiền.
2. ~~**Trường danh mục vũ khí**: Bảng giá vũ khí được phân nhánh theo danh mục và byte của bản ghi vũ khí mà danh mục được lấy từ đó vẫn chưa được xác nhận. ~~ Đã xác nhận là kỷ lục vũ khí `+0x0E` (18-09-2026).
3. **Phân công lao động với 8.1**: Những món đồ còn thiếu của mỗi loại vũ khí sẽ được 8.1 sửa chữa chính xác; việc hoàn lại tiền sẽ chỉ chịu trách nhiệm đối với những tổn thất nhỏ như xóa toàn bộ máy và cả hai không trùng nhau.

#### B1/B2: Dự trữ hoặc lấp đầy số lượng phân đoạn chuyển đổi (đắt hơn)

- **Kế hoạch B1 (Thu hẹp)**: Đối với nhân vật + máy bay + danh sách hiện trường được chỉ định "trở về sau khi khởi hành tạm thời", hãy hạ cấp `4000` xuống `2000` (chỉ xóa phi công, máy bay vẫn còn trong danh sách). Những thay đổi đều tập trung, nhưng cần phải xác nhận từng cái một rằng cơ khí nên được giữ lại trong cốt truyện, nếu không sẽ để lại một cơ máy trong danh sách lẽ ra đã biến mất; và `3D5A …,500` trả về sẽ sử dụng lại phiên bản cũ bị bỏ lại và `3D6C 机体,3` tiếp theo sẽ vẫn **ghi đè** số lượng giai đoạn.
- **Kế hoạch B2 (rộng)**: Về phía chủ nhà, ghi nhớ năm phân đoạn và số phân đoạn của từng loại vũ khí của phiên bản đã xóa theo số cơ thể và điền lại khi đăng ký lại cùng số cơ thể. Cấu trúc ban đầu không bị thay đổi, nhưng bộ nhớ này phải được nhập vào bộ sưu tập lưu ([Roadmap](../design/mod-roadmap.md) M2), nếu không việc đọc tệp sẽ không hợp lệ; và phải quyết định xem phạm vi bao phủ của `3D6C` sẽ vẫn như bình thường hay được thay đổi thành giá trị lớn hơn - nếu nó vẫn giữ nguyên thì khoảng tầm trung của hệ thống W vẫn được cố định ở 3 phân đoạn và việc chèn lấp là vô ích.
- Cả hai giải pháp rõ ràng đều làm thay đổi nguồn lực và sức mạnh. Chúng thuộc về gói quy tắc chứ không phải QoL. Chúng yêu cầu mô tả hiệu ứng riêng biệt và chấp nhận khả năng tương thích với các tệp cũ.

### 8.5 Các bộ phận đi kèm (được thực hiện dưới dạng điều chỉnh độ khó `parts-carry-over` vào ngày 24-09-2026)

Khi đổi máy, toàn bộ phần nâng cao của máy cũ sẽ bị loại bỏ (`800AA3C4` → `800A9DCC` → `800A9D60`). Đang tải ** không phá hủy **: Bản ghi hàng tồn kho `D_8015E990` Mỗi thành phần có u16, số giữ byte cao và số thiết bị byte thấp. Việc dỡ hàng chỉ làm giảm số lượng thiết bị nên linh kiện được trả về kho nhưng thân mới trống rỗng và không thể lắp lại cho đến lần bảo trì tiếp theo. Sau khi mở `parts-carry-over`, việc đóng gói `800AAD28` sẽ tiếp quản trước và sau chức năng ban đầu, đồng thời cài đặt các thành phần vào các khe trống của phần thân mới theo thứ tự ban đầu.

Số lượng vị trí được lấy từ bản ghi máy bay `+0x19` (ví dụ `+0x21`). Chỉ có tám trong số 30 bộ thay thế sẽ được giảm bớt, tất cả đều là 2 → 1: năm EW và ba Shineゲッター; một trong những sản phẩm thay thế này sẽ được để lại trong kho tại một thời điểm. Còn lại (bao gồm 3 slot của Maxion Z và 1 slot của tàu) đều phù hợp. Xem [Sửa đổi quy tắc không bắt buộc](rule-fixes.md) §2.7 để biết thông tin chi tiết và xác minh.

### 8.4 Trình tự hạ cánh

1. 8.1 đã được triển khai và vượt qua bài kiểm tra đơn vị; nó vẫn cần chạy xác minh Mục 7 (`config/recomp/mini-stages/inherit.json` đã sẵn sàng) để xác nhận ba mục bị thiếu và "số lượng phân đoạn phiên bản mới bắt đầu từ 0".
2. Hoàn tiền B0 đã được triển khai (`upgrade-refund`, đóng theo mặc định), với lời nhắc trên màn hình và hồ sơ đánh giá; xác minh vẫn chưa được kích hoạt trong cốt truyện thực tế.
3. Nếu thực hiện B1/B2, công việc chuẩn bị là hoàn thiện cốt truyện “việc rời nhóm là tạm thời”.

## 9. Chứng cứ gián tiếp và các phát hiện khác

- **`3D6F` là "mở khóa vũ khí", không phải là thao tác thành phần**: nó xóa bit 2 của phiên bản vũ khí `+0x22`. 11 tham số của kịch bản gốc đều là số vũ khí đặc biệt được mở khóa trong cốt truyện (19 Cú đấm phá đá, 1215ダブルゴッドフィンガー, 53/62/71/76 シャッフルMáy liên minh, 770/773/775/777コン・バトラーV, 874 対空光剣). Bit này chính xác là bit trong `800AA8F4` được kế thừa đặc biệt bởi 314 ファンネルMAP. Mục nhập `3d6f` cho khóa bố cục `config/data/original-jp-v1.json` đã được sửa tại chỗ với phân tích này (là "Xóa cờ bản ghi phần (Số phần)").
- Do đó, 700 mục đầu tiên × 36 byte của vùng có tên `part_instances` (từ `0x80178F80`) trong thăm dò trạng thái `src/host/state_probe.hpp` là **nhóm phiên bản vũ khí**: phiên bản nội dung `+0x30` trỏ tới nó và `+0x2C` là số phần. Các thành phần gia cố là một tập hợp cấu trúc khác (phiên bản máy bay `+0x21`/`+0x23` khe và `D_8015E990` kho lưu trữ, xem `800A9D60`). Tên của khu vực vẫn chưa được sửa đổi.
- Tìm kiếm tiền thân không nhìn vào trình điều khiển mà chỉ lấy phiên bản hoạt động đầu tiên có số trùng khớp.
- Bộ đệm ngăn xếp dùng để lưu vũ khí là 50 vật phẩm và số lượng vũ khí tối đa trong toàn bàn là 28 (ランドライガーH), sẽ không bị tràn.
- Các dạng biến đổi có chung mảng phiên bản vũ khí (ví dụ: ゲッター1/2/3 chia sẻ 12 mảnh), do đó, việc sửa đổi vũ khí của mỗi dạng là cùng một dữ liệu.

## 10. Tham gia triển khai, `3D6C` bảng đầy đủ và chuỗi W theo số đoạn của tuyến đường (Bổ sung ngày 2026-10-01)

Tất cả đều là kết luận tĩnh (tháo gỡ + `stage_events.jsonl`/`stage_deployments.jsonl` quét toàn bộ tập lệnh), không phải máy thật.

### 10.1 Tham gia triển khai không kế thừa

`3D45` Bản ghi triển khai trại 0 (và giá trị bản ghi 3) rơi vào nhóm 0 (phía chúng tôi). `8020ABB4`: Khi số phi công < 287, trước tiên hãy tìm máy bay có phi công trong danh sách **tái sử dụng** (lúc này, bỏ qua số máy bay và chỉ số nâng cao trong bản ghi, `8020AC38`–`8020AD58`); nếu không tìm thấy thì tạo mới và ghi năm mục là `D_800CB5DC[强化索引]` (ROM `0x55FCC`: `0,1,3,5,7,9,11,13,15`), tất cả vũ khí của máy kết hợp không biến hình (`800A79EC` trả về 0) cũng được ghi có cùng giá trị (`800A95DC`; `8020AFB4`–`8020B044`). Việc triển khai và tham gia không thông qua `800AAD28` và **không tạo ra bất kỳ sự kế thừa nào**.

`80211680` (được gọi theo quá trình thoát bản đồ chiến thuật `801DFD14`) mkⅡ 343→56 thay đổi số: 343 chỉ xuất hiện trong hệ thống thực tập 5 nhóm triển khai "Black Gun" 3 (`001E6E04`). Nó đã không được duy trì khi thay đổi số và không có sự sửa đổi nào để vứt đi.

### 10.2 Số màn khi 5 thành viên của dòng W trở lại (theo lộ trình)

Rời đội là `3D5A …,4000`: Cánh bay/Trang bị hạng nặng/Cái chết/Sa mạc ở đầu OZ Chương 21 (`001BC304`), kết thúc Chương 22 của Quân đội Độc lập và Hòa bình Trọn vẹn (`001AB4A0`); Shenlong chọn OZ ở cuối Chương 20 (`001A9E0C@804`) hoặc Chương 22 Kết thúc câu chuyện.

| Máy bay | OZ | Hòa bình trọn vẹn → Sutelles | Hòa bình trọn vẹn → Chiến đấu một mình | Quân Đội Độc Lập |
| --- | --- | --- | --- | --- |
| Sa mạcGundam Kai (カトル) | Triển khai ở tập 33 (`001C71BC` nhóm 3, chỉ số 0) → **0** | Tập 28 mở đầu với sự trở lại của Desert Gund (`001B6FA0@68` + `3D6C 124,3`) → 3; cuối tập 32 `3D5A 89,0,126,124` Chuyển **True Inheritance** (Only Lost クロスクラッシャー) | Tương tự như Trái | Chương 36 Mở đầu `001B3F30@780` + `3D6C 126,3` → **3** |
| Hell Death Gundam (デュオ) | Chương 34 Triển khai trong Pass (`001C8240` Nhóm 4, Mục lục 3) → **5** (Năm vật phẩm và vũ khí) | Chương 34 Triển khai trong Pass (`001BB348` Nhóm 7) → 3 | Bắt đầu Chương 35 `3D5A …,500` (`001BA234@186`), không có `3D6C` → **0** | Triển khai ở tập 28 (`001AF65C` nhóm 6) → 3; nếu không được kích hoạt thì kết thúc tập `3D5A` + `3D6C 128,3` (`001AF8E8@82/92`) → 3 |
| Flying Wing Zero (ヒイロ) | Chương 36 Triển khai ở Quan Trung (`001C98F0` Nhóm 6) → **0** | Chương 35 Triển khai (`001B7E94` Nhóm 6, Mục 2) → 3 | Chương 35 Mở đầu `3D5A …,500` (`001BA234@166/514`) → **0** | Mở đầu tập 36 `001B3F30@770` + `3D6C 119,3` → 3 |
| Heavy Gun Kai (Toro) | Hết Chương 45 `001D9430@310/320` → 3 | Tương tự như OZ | Mở đầu Chương 42 `001CEC70@1138/1148` → 3 | Tương tự như bên trái |
| Rồng hai đầu (Năm bay) | Hết Chương 45 `001D9430@294/304` → 3 | Tương tự như OZ | Hết Chương 45 `001D0FEC@402/412` → 3 | Tương tự như Zuo |

Do đó, các tiền tố 127→128, 130→132, 133→115 không bao giờ được kích hoạt trong kịch bản ban đầu; 124→126 chỉ được kích hoạt trên con đường hoàn toàn yên bình.

### 10,3 `3D6C` Tất cả 38 mặt hàng (26 đơn vị)

Số phân đoạn thực tế = `min(N, 该机上限)`, chỉ áp dụng cho đơn vị đầu tiên trong nhóm của chúng tôi.

| Cấp độ (sự kiện) | Thân hình | N | Điều kiện |
| --- | --- | ---: | --- |
| Kết Thúc Tập 3 Thực Sự (`0019F6D0@446`) | Gundam Ez8 | 1 | シロー Tham gia |
| Hết chương 6 của bộ truyện thực tế (`001A0E80@98/124/150`) | Guntank/Gundam/Gundam | mỗi cái 1 | var128≠3 và giữ từng cái (var129/130/131=0) |
| Mở đầu tập 9, hệ thống thực (`001A278C@508`) | Jie Gang | 1 | エマ tham gia |
| Mở đầu tập 10 của Real Series (`001A2F9C@592`) | Dole (シモーヌ) | 3 | — |
| Hết Chương 11, Siêu Loại (`001A4680@346`) | Gundam Ez8 | 3 | シロー Tham gia |
| Quân đội Độc lập/Hòa bình hoàn toàn Mở đầu Chương 22 (`001AADDC@232/238`) | Baldi, Beble | 3 mỗi cái | — |
| Quân đội độc lập/Hòa bình hoàn toàn Chương 22 Kết thúc, Hiện thực (`001AB4A0@310`) | Graeme Caesar | 3 | var0=0 |
| Quân Độc Lập Chương 28 Hết đèo (`001AF8E8@92`) | Địa Ngục Cái Chết Địa Ngục | 3 | var129≠1 |
| Mở đầu Chương 36 Quân Độc Lập (`001B3F30@790/796`) | Flying Wing Zero, Sa mạcGundam Kai | 3 mỗi cái | — |
| Complete Peace Chương 26 Kết thúc đèo (`001B6534@172`) | Full Giáp Trăm Phong Cách Thay Đổi | 8 | **Không thành công**: Không có 295 trong danh sách tuyến đường này |
| Complete Peace Chương 27 Kết thúc (`001B6CCC@172`) | MinervaX | 5 | var128=1 |
| Complete Peace Chương 28 Mở đầu (`001B6FA0@78`) | Sa mạcGundam | 3 (tối đa 6) | — |
| Complete Peace Chương 30 Hết đèo (`001BBD3C@346`) | Đại Quỷ Thần sản xuất hàng loạt | 3 | — |
| Complete Peace (Suiteles) Chương 35 Khai mạc (`001B7918@298`) | Thế hệ tiếp theo (ゼクス) | 3 | — |
| OZ Tập 22 Mở đầu (`001BCEA8@1540/1546`) | Baldi, Beble | 3 mỗi cái | — |
| Hết Chương 26 của OZ (`001BFF5C@686/1362`) | GP02A | 3 | var37=0; nhánh var37=3 chưa được đăng ký GP02A, **thất bại** |
| OZ Tập 27 Mở đầu (`001C10F8@1076`, `001C1B94@1448/1636`) | Sigurun | 3 | var14 |
| OZ Chương 28 (`001C283C@252`, `001C3658@662`) | Graeme Caesar | 4 | var0=0 |
| OZ Tập 31 Khi Tất Cả Kẻ Thù Bị Tiêu Diệt (`001C62AC@44`) | Thế hệ tiếp theo (ヒイロ) | 3 | — |
| "Từ nay sát cánh bên nhau" Guanmo (`001E2F44@118`) | Nowruz | 4 | — |
| "Ngày tận thế" Quan Mạt (`001E31FC@354`) | Vairos | 3 | var128=0 |
| Hết OZ Chap 37 (`001D5C48@502`) / Hết Chapter 40 Quân Đội Độc Lập (`001D3EB4@294`) | Zelong | 3 | var26=2 |
| Mở đầu Chương 42 Quân Độc Lập (`001CEC70@1148`) | Heavy Gun Kai | 3 | — |
| Quân Đội Độc Lập Chương 45 Hết đèo (`001D0FEC@412`) | Rồng hai đầuGundam | 3 | — |
| OZ Chương 45 Kết thúc (`001D9430@304/320`) | Robot rồng hai đầu, Heavy Gear Gundunda Kai | 3 mỗi cái | — |
| Hết Chương 51 (`001DFB88@644`) | Noye Gill | 3 | var11=0 |
| Hết Chương 54 (`001E1B18@1210`) | Acto Deka | 6 | var47=0 |

Chờ máy thật: Triển khai xem các phiên bản được thêm vào của nhóm chúng tôi có được giữ lại ở cuối cấp hay không (10.2 tùy thuộc vào điều này; xác nhận tối thiểu là để xem Hell Death có 5 màn sau OZ Chương 34); hai lỗi `3D6C`; số màn chơi sau khi Vua Sấm được kết hợp.

Trả về: [Đăng ký lỗi gốc](original-bug-register.md) · [Lộ trình MOD tích hợp](../design/mod-roadmap.md) · [Chỉ mục tài liệu kỹ thuật](../README.md)