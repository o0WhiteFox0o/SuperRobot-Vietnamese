> **Ngôn ngữ / Language:** [Tiếng Việt](battle-animation.vi.md) · [English](battle-animation.en.md) · [中文](battle-animation.md)

# Logic xử lý hoạt ảnh chiến đấu và tính khả thi của việc tùy chỉnh cơ thể/vũ khí

Cập nhật: 2026-09-19. Phân tích tĩnh (tháo gỡ và dữ liệu ROM) mà không cần chạy trò chơi. Để biết tài nguyên hình ảnh, định dạng cảnh và xuất, hãy xem [Hình ảnh trận chiến](battle-graphics.md). "Xác nhận mã" đề cập đến việc đọc hướng dẫn đọc/sử dụng dữ liệu; "suy luận tĩnh" là ý nghĩa được suy ra từ phương pháp sử dụng, vẫn cần được xác minh trên máy thực tế.

## Kết luận

1. **Hoạt ảnh chiến đấu không phải là tập lệnh mã byte. ** Mỗi loại vũ khí tương ứng với một bản ghi có bố cục cố định: 4 trường tiêu đề, tối đa 8 hiệu ứng âm thanh, tối đa 24 diễn viên. Mỗi diễn viên được chỉ định một cảnh chiến đấu (hình ảnh), một tập hợp tọa độ và **số quy trình hành vi**. Tất cả logic thời gian đều được viết bằng khoảng 270 quy trình gốc trong lớp phủ chiến đấu và các diễn viên cộng tác trên một byte "pha" chung.
2. **Hoạt hình vũ khí tùy chỉnh có thể được thực hiện chỉ bằng dữ liệu**: Các bản ghi mới sử dụng lại các quy trình hành vi hiện có và hướng diễn viên đến các cảnh mới hoặc cảnh hiện có. Chỉ logic hiệu suất mới (các hành động mà các quy trình hiện có không thể thực hiện) mới yêu cầu viết các quy trình gốc C++.
3. **Định dạng của nghệ thuật tùy chỉnh đã được đọc qua hoàn toàn. ** Bản đồ nội dung, bảng màu và cảnh (các bộ phận + đỉnh + bảng bước) đều có thể được tạo ngược lại bằng công cụ (PNG → Atlas/Palette/Scene) và việc thay thế HD tuân theo cơ chế băm theo kết cấu hiện có.
4. **Khó khăn khi thêm máy bay/vũ khí là ID chứ không phải hình ảnh. ** Tất cả các bảng đều là các bảng có độ dài cố định được kết nối từ đầu đến cuối và địa chỉ cơ sở bảng cũng như giới hạn trên của hai ID được mã hóa cứng trong mã.
- **Chiếm các phần giữ chỗ hiện có hoặc các vị trí trùng lặp**: Chỉ cần có phạm vi bao phủ dữ liệu và dịch vụ tài nguyên của lớp máy chủ và không cần phải tạo lại mã biên dịch lại, đây là cách ngắn nhất.
- **ID thực sự mới**: Để kết nối với nhiều chức năng đọc, tạo lại mã và xử lý khả năng tương thích của kho lưu trữ.

## Luồng dữ liệu của một cuộc tấn công

```text
武器 ID ─→ ROM 0x11FC80[id] (u32 偏移) ─→ 动画库 0x184990 + 偏移，DMA 0x3C0 字节
          │                                   │
          │                                   ├─ 头部：镜头模式、命中特效号、攻方动作、守方动作
          │                                   ├─ 音效表（≤8）
          │                                   └─ actor（≤24）：registry, x, y, z, h4, h5, h6, behavior
          │                                        │
          │                                        └─ 0x11E3D0[registry] = (场景, 图集, 调色板) ─→ 资源加载 ─→ 精灵槽
          ├─ ROM 0x119970[id]：规范武器 ID（机师台词用）、接触标志、伤害节拍模式、相位码
          └─ 命中特效号 ─→ 0x216150 / 0x2129F0（同格式，159 条；156–158 为击毁）
守方：反应代码 ─→ 0x216630 / 0x2163D0（同格式，28 条）；盾牌图 0x2166A0（24 条）或机体战斗记录
双方基本姿势：0x84E40[机体 ID]；机体战斗记录：0x118610[机体 ID]
```

| Bảng | ROM | Nhập cảnh | Chỉ mục | Đọc | Sự Tự Tin |
| --- | --- | ---: | --- | --- | --- |
| Phần bù hoạt ảnh vũ khí → Thư viện hoạt ảnh | `0x11FC80` → `0x184990` | 1.329 (1.115 hồ sơ khác nhau) | ID vũ khí | `801C3128` ← `801C3C9C` | Xác nhận mã: `801C3C9C` Chuyển ID vũ khí trực tiếp đến chức năng đọc, hồ sơ của vũ khí 29 và 24 là khác nhau |
| Thư viện hiệu ứng nhấn | `0x216150` → `0x2129F0` | 159 | Đầu vũ khí hit_script; 156–158 hủy diệt | `801C31E8` | Xác nhận mã |
| Thư viện phản ứng quốc phòng | `0x216630` → `0x2163D0` | 28 vị trí (8 vị trí khác nhau) | Mã phản ứng | `801C3230` | Xác nhận mã |
| Danh sách tóm tắt cảnh chiến đấu | `0x11E3D0` | 1.051 | diễn viên.registry | `801C3170` ← `801C50D8` | Xác nhận mã |
| Pháp sư phòng thủ | `0x2166A0` | 24 | Mã phản hồi | `801C31AC` ← `801C4574` | Xác nhận mã |
| Nhật ký chiến đấu vũ khí | `0x119970` | 1.329 × 7 giây16 | ID vũ khí | `801C3278` | [0] Xác nhận mã ID vũ khí Canonical (`8022241C` kiểm tra `< 0x531`); [3] Liên hệ, [5] Nhịp sát thương, [6] Mã pha được suy ra tĩnh |
| Kỷ lục chiến đấu của máy bay | `0x118610` | **354** × 7 s16 | ID máy bay | `801C30D0` | [1] Tỷ lệ Sprite %, [2..4] Hình ảnh khiên, [5] Cảnh bổ sung, [6]=2 Chọn bị phá hủy 156, suy luận tĩnh |
| Mẫu nhịp sát thương | `0x181DB0` (`D_80222E50`) | 25 × 8 | Hồ sơ vũ khí [5] | `801C8A58` | Suy luận tĩnh |

- Hầu hết các hình ảnh được kẻ tấn công sử dụng đều có trên bản đồ chiến đấu của chính kẻ tấn công (ví dụ: sổ đăng ký 297 = ガンダムシュピーゲル (2477, 1612, 1908)); chùm tia, vụ nổ, v.v. đều có trên tập bản đồ hiệu ứng đặc biệt.
- Các dòng thí điểm được `80222050` chọn riêng theo phi công, ID vũ khí tiêu chuẩn và phản ứng và không được ghi trong bản ghi hoạt ảnh.
- Có một bản sao khác của chức năng đọc tương tự trong `load_00216730` (`801C2634`–`801C27DC`); khi di chuyển bất kỳ bảng nào, cả hai vị trí đều phải được sửa đổi cùng nhau.
- Theo sau mỗi thư viện hoạt ảnh là một bản sao của bảng offset chưa sử dụng (`0x19AA40`, `0x215ED0`, `0x2165B8`).

## Định dạng bản ghi hoạt hình

Trình phân tích cú pháp `801C3D38`/`801C4EF0`; trình chỉnh sửa dành cho nhà phát triển còn lại (xem phần cuối bài viết) được biên soạn theo cùng định dạng, có thể được sử dụng làm bằng chứng tình huống.

```text
u16 camera          镜头／站位模式 0–3（801C67EC 选择每帧处理 801C63BC/64D8/6584/6678）
u16 hit_script      命中特效库条目
u16 action          攻方主精灵动作号（0–188，跳转表 0x80223990，经 801E4668）
u16 defender_action 普通命中时守方的动作号
s16 sounds[≤8], 0xFFFF     行为例程用 801C355C(n) 播放第 n 个；−2 = 静音
actor[≤24] { u16 registry; s16 x, y, z; u16 h4, h5, h6; s16 behavior }, 0xFFFF
```

| lĩnh vực diễn viên | ý nghĩa | uy tín |
| --- | --- | --- |
| đăng ký | Chỉ mục bảng chung của cảnh chiến đấu, được tải vào khe yêu tinh xoay (`801C50D8`); x ở bên phòng thủ bị đảo ngược | Xác nhận mã |
| x, y, z | Bù đắp so với cơ thể của chính mình; một số thủ tục sử dụng chúng làm tham số | Xác nhận mã |
| h4 | Được giải thích theo quy trình, chủ yếu là số khung hoặc số ký tự trễ bắt đầu; bit15 là cờ | Xác nhận một phần |
| h5 | Mỗi khung hình được sao chép sang elf byte +0x35 (chủ yếu là 0xFF, quy trình sẽ chuyển màu cho khung hình đó, có lẽ là để tạo độ mờ) | Copy đoạn code xác nhận, suy ra nghĩa |
| h6 | Chế độ hiển thị: 1 = không bao giờ tự động ẩn, 2 = không bao giờ tự động hiển thị (tác nhân điều khiển) | Xác nhận mã |
| hành vi | Quy trình hành vi 3–382, bảng con trỏ hàm `0x80225030` (thông qua `80220C0C`); 4, 5, 370, 371, 380, 381 trống | Xác nhận mã |

Tất cả các bản ghi 1.329 + 159 + 28 đều được phân tích cú pháp theo định dạng này: tối đa 406 byte, tồn tại chính xác 24 bản ghi tác nhân, đăng ký tối đa 1045, tất cả các hành vi đều nằm trong 3–382.

### Ví dụ

| Vũ khí | Đầu (máy ảnh, hiệu ứng đánh, kẻ tấn công, người phòng thủ) | diễn viên |
| --- | --- | --- |
| 0 アイアンネット（シュピーゲル） | (1, 0, 88, 128), hiệu ứng âm thanh 3, 58, 250 | đăng ký 222 "WepIanNet" tại (0, 36), hành vi 28 (pha bằng 0x44/0x46, ghi 0x43/0x45) |
| 3 シュピーゲルブレード | (0, 33, 23, 148) | đăng ký 297 (tư thế bản địa) hành vi 43; đăng ký 250 hành vi "WepDoubleCut" 44 |
| 228 ビームライフル（ガンダム） | (1, 6, 113, 125), hiệu ứng âm thanh −2, 1, 5, 8 | đăng ký 121 hành vi tư thế chụp 359 (hiển thị ở 0x44, h4 xác định có ẩn cơ thể, phát hiệu ứng âm thanh và đèn flash); đăng ký 0 Hành vi hẹn giờ ẩn 124 (ghi 0x50 20 khung sau 0x44); đăng ký 56 "WepBeamRed00" tại (−65, 28) hành vi 118 |
| 29 シャイニングフィンガー | — | Các trích dẫn không phải phần bản địa cắt ghép 1009–1016: ドモン cận cảnh, シャイニング cận cảnh, huy hiệu King of Hearts, v.v. |

Kết quả phân tích cú pháp cho tất cả vũ khí được xuất trong `animations.json` và cho mỗi máy bay trong `unit.json` (các diễn viên được liên kết trực tiếp với tệp hình ảnh).

## Các thủ tục hành vi và byte pha (chủ yếu là suy luận tĩnh)

- `801C5BAC` Các quy trình của tất cả các tác nhân đang hoạt động được gọi theo trình tự trong mỗi khung hình khi byte pha khối (B+0x25) có 0x40; nhân vật chính chia sẻ byte này với tất cả các tác nhân (E+0x48 trỏ tới nó).
- Mã pha nhìn thấy: 0x41–0x46, 0x48, 0x49, 0x4B, 0x4C, 0x50–0x57, 0x5A. 0x44 = "Fire": Hành động 88 yêu cầu kẻ tấn công lao về phía trước trong 21 khung hình trước khi ghi 0x44, 142 quy trình đang chờ nó. 0x49 sẽ tắt tác nhân. 0x50–0x57 là các bước phụ được nối giữa các tác nhân (ví dụ: bộ đếm thời gian 124 ghi 0x50 sau khung h4). Ý nghĩa của 0x43, 0x45 và 0x46 là suy luận.
- Các thao tác cơ bản có sẵn cho quy trình: thay đổi cảnh/atlas/bảng màu (`801C5700`, `80098204`, `80098590`, `80098604`), hiển thị/ẩn ( `801C3840`/`801C37FC`), phát hiệu ứng âm thanh (`801C355C`), đèn nháy toàn màn hình trắng/đen (`801C9520`, `801C95CC` → `8009AC84`), 10 hiệu ứng bảng màu sprite (`801C963C` → `80099C88`), theo dõi camera (`801C637C`/`801C63A8`), tăng nhịp độ sát thương (`801C8DFC`), nạp yêu tinh phòng thủ (__INL_C ODE_56__), ẩn/khôi phục nền (`801C3C40`/`801C3C64`, chưa được xác nhận), các chương trình con dẫn xuất (`80220C0C`, `801E4668`).
- Trạng thái mỗi bên `0x800F97E0 + side × 0x1074`, bao gồm mỗi byte 0x81C cho khối vũ khí (+0x2C) và khối phản ứng (+0x848): tiêu đề 0x4C, diễn viên giả sprite chính, 24 diễn viên 0x50 byte.
- Các khe sprite hiệu ứng 0xAA–0x107 (94) được sử dụng để xoay, không kiểm tra tràn; ba khối × 24 diễn viên có thể phù hợp.
- ID vũ khí đặc biệt (`801C3C9C`): −1 không có hoạt ảnh; nhật ký −2/−3 (phòng thủ/né tránh thay vì phản công) có tích hợp null `D_80222D40`; `0x1000` đọc RAM `0x80250010` (nơi biên tập viên của nhà phát triển ghi).

### Mã phản ứng phòng thủ (cài đặt `load_000AB160:801F7204`, suy luận tĩnh)

| Mã | Ý nghĩa |
| --- | --- |
| −1 | Đòn đánh thường: Người phòng thủ thực hiện hành động phòng thủ trên đầu vũ khí |
| 0 | Không bị tấn công |
| 22 | Né tránh (Hành động 15) |
| 6–12 |ゲッタービジョン、マッハスペシャル、真マッハスペシャル, ゴッドシャドー, chân ảo tức thời,ハイパージャマー, bản sao |
| 2→13, 3→14, 4→15, 5→16 | Iフィールド,ビームコート,オーラバリア,プラネットディフェンサー: Cái trước bị chặn hoàn toàn, cái sau bị xuyên thủng |
| 17 | Khiên phòng thủ |
| 18／19 | Cắt り払い, phân biệt theo thời gian hoạt động của vũ khí tấn công |
| 20 | Hỗ trợ phòng thủ (máy khác ra đòn thay bạn) |
| 21 | Không xác định (liên quan đến cờ lưới bản đồ 0x80) |

## Tải tài nguyên và bộ nhớ

- Bảng tài nguyên trong ROM `0xA20BD0`: số u32 (6.436) + bộ mô tả 8 byte; mỗi mục có độ dài giải nén u32 + LZSS (`src/srw64_rom/resources.py`).
- Hàm nạp `80089E9C(id)`:
- `sltiu 0x1924` của `80089EAC` là giới hạn ID tài nguyên duy nhất (xác nhận mã).
- Các tài nguyên được tải chỉ được tính tham chiếu; bảng vị trí `D_80160340` có 200 mục nhập và được phân bổ cho lần điều chỉnh đầu tiên.
- Phần mô tả được đọc trực tiếp từ `osEPiStartDma` bởi `80089BBC` mà không cần thông qua `8007F704` mà máy chủ đã nối; quá trình giải nén dữ liệu trải qua `8007F704`.
- Vùng heap là `0x80277800–0x80400000` (1.607.680 byte), tất cả tài nguyên đã tải đều được chia sẻ và không có giới hạn bổ sung cho các sự kiện riêng lẻ hoặc trận chiến đơn lẻ.
- Lỗi phân bổ sẽ in "ALOCATE ERROR", trả về −1 và người gọi sau đó sẽ nhận được một con trỏ rỗng.
- Tài nguyên tối đa 263.177 byte (1349), atlas khung máy bay tối đa 201.609 byte. Bản đồ chiến đấu của khung máy bay là 3 tài nguyên (cảnh khoảng 1,4 KB, thư viện, bảng màu 264 byte).
- Biên độ thực tế trong chiến đấu chưa được kiểm chứng.
- recomp chạy với 8 MiB RAM, trò chơi chỉ sử dụng hơn 4 MiB của `0x80400000–0x804152F0` (trình chỉnh sửa của nhà phát triển) và khu vực tiêm tập lệnh máy chủ `0x807F0000`, để lại khoảng 3,9 MiB trống ở giữa.
- Hạn chế về hình ảnh: Hầu hết các phần có kích thước 32×32 (tối đa 48×32, 40×40), CI8 có tối đa 2.048 texels mỗi phần trong 2 KB TMEM; kích thước tập bản đồ là 32k+1 (để lại 1 cạnh pixel cho lọc song tuyến tính); một khung hình có thể xem tới 123 phần; Bảng màu CI8 256 màu.

## Thêm cơ thể và vũ khí tùy chỉnh

### Các bảng liên quan đến phần thân

| bàn | vị trí | kích thước | phương pháp đọc |
| --- | --- | --- | --- |
| Giá trị cơ bản | ROM `0x71B80` | 363 × 36 | `800A6E68`, `800A5254`, `800A8CE8`, `8009C2DC`, qua `8007F704` |
| Danh sách vũ khí | Con trỏ ROM `0x7E210` → hàng 12 byte | 363+1 trống; `0x82E40–0x83110` có khoảng cách 0xFF 720 byte | `800A67C8`, `800A68BC` |
| Tên | Văn bản 527 + ID đơn vị | — | `801C6DD0` v.v. qua `8008C510` |
| Bù màn hình trạng thái | ROM `0x7D980` | 363 × 4 | `8009C6E4` |
| Các tư thế chiến đấu cơ bản | ROM `0x84E40` | 365 khe | `8009C864` (chiến đấu `801C5328`, `801C5808`, `8021FB4C`) |
| Kỷ lục chiến đấu trên khung máy bay | ROM `0x118610` | **354** × 14; ID ≥ 354 sẽ đọc bảng chiến đấu vũ khí tiếp theo | `801C30D0` |
| biểu tượng bản đồ | lớp phủ RAM `0x80218218` (ROM `0x100D78`) | 363 × 2, không có khoảng trống | 5 dòng nội tuyến `lhu`: `801C5F14`, `801C60BC`, `801C84F4`, `801CCD38`, `801CE818` |
| Tùy chọn | Chuyển đổi `D_800CB40C`/`B5A4`, Kết hợp `D_800CAC94`/`AEF0`, Kế thừa `D_800CA3A0`, Phi hành đoàn `D_800CA418`, Đã xem bộ bit (ID < 354) | — | Thường trú/lớp phủ |

Vũ khí: giá trị cơ bản ROM `0x74E90` (1.329 × 16, `800A642C`); tên văn bản 1370＋ID và tên menu 2699＋ID; kỷ lục chiến đấu bằng vũ khí `0x119970`; phần bù hoạt ảnh `0x11FC80`; xuất hiện trong dòng danh sách vũ khí của một máy bay nhất định; ánh xạ kế thừa sửa đổi tùy chọn `D_800CB5E8`.

Giới hạn trên: Vũ khí chỉ có `< 0x531` trong số `8022241C` (còn một vị trí khác trong mô-đun gỡ lỗi); phần thân không kiểm tra 363 trong logic trò chơi và nếu vượt quá giới hạn, nó sẽ âm thầm đọc sang bảng tiếp theo. Chỉ còn 2 ô trống trong bảng cảnh chiến đấu và không có giới hạn kiểm tra khả năng đọc.

### Route A: Chiếm các slot hiện có (nên làm trước)

- **Vị trí cơ quan ứng cử viên**:
- 314 và 325 là các bản ghi νガンダム có cùng byte (chỉ khác vài byte so với số 50); 309 ゴッドガンダム chia sẻ danh sách vũ khí với 1 và 2. Không có tài liệu tham khảo nào về chúng trong bảng triển khai, sự kiện, biến đổi/kết hợp và chúng cần được kiểm tra từng cái một.
- 354–362 là các bản ghi giữ chỗ, nhưng không có dòng bản ghi chiến đấu trên khung máy bay (`0x118610` chỉ có 354 dòng). Để sử dụng chúng, trước tiên bạn phải giải quyết hồ sơ chiến đấu ngoài giới hạn để chúng phù hợp với lộ trình B.
- **Khe vũ khí ứng cử viên**: 147 ID vũ khí không có trong bất kỳ danh sách vũ khí nào của máy bay (ví dụ: 10–14, 1191–1198, 1328). Nhiều loại trong số này là vũ khí thật, chẳng hạn như 24 シャイニングフィンガー có hoạt ảnh cắt sẵn riêng, có thể được cấp bằng mã theo biểu mẫu. Nó chỉ có thể được sử dụng làm ứng cử viên và các tham chiếu mã phải được loại trừ từng cái một trước khi sử dụng.
- **Người dẫn chương trình phải làm gì**:
- **Lớp phủ dữ liệu**: Mở rộng bản vá byte `patch_copy` (`src/host/upgrade_rules.hpp`, hiện được sử dụng để sửa đổi các quy tắc sửa đổi cơ thể +0x20, vũ khí +0x0E) thành lớp phủ dữ liệu phổ quát. Tất cả các bảng ROM được đọc bởi `8007F704` đều có thể bị ghi đè, bao gồm tất cả các bảng biểu tượng bản đồ và dữ liệu được tải lớp phủ.
- **Danh sách vũ khí**: Danh sách mới được ghi vào khoảng trống 0xFF và con trỏ được thay đổi, giữ nguyên danh sách chia sẻ.
- **Bản ghi hoạt hình**: Độ lệch của `0x11FC80` là u32, các bản ghi mới có thể được đưa vào cửa sổ ROM ảo hiện có của máy chủ (cơ chế `0x02400000`, `0x03000000`).
- **HÌNH ẢNH MỚI**: Ghi đè `80089BBC` để làm cho bộ mô tả đọc trỏ đến tài nguyên mới trong cửa sổ ảo (hoặc sử dụng biến thể ROM dữ liệu như 5600); cơ chế tương tự cũng có thể thay thế các nguồn lực hiện có.
- **Tên**: Cung cấp một chuỗi chẳng hạn như 527+ID bằng đường dẫn văn bản giả hiện có. Menu chỉ có thể vẽ các phông chữ có trong thư viện phông chữ ROM và tên menu phải giữ lại dấu lưới/bắn/P.
- **Rủi ro**: Nếu bạn có một kho lưu trữ hiện có với ID này, nó sẽ được hiển thị dưới dạng nội dung mới (dự kiến các ứng cử viên trên sẽ không có sẵn); số lượng còn lại của đống chiến đấu chưa được đo lường.

### Route B: Thêm ID thật

- recomp cho phép máy chủ đảm nhận chức năng (`NATIVE_HOOKS` của `tools/recomp/toolchain/generate_cpu.py` đổi tên hàm được tạo và máy chủ cung cấp tên gốc trong `src/host/game_hooks.cpp`). N64Recomp cũng hỗ trợ vá hướng dẫn, nhưng `recomp.toml` hiện được tạo không hữu ích.
- **CẦN LÀM**:
- **Chức năng đọc**: Đảm nhiệm các chức năng đọc nhỏ (bản sao trong `8009C6E4`, `8009C864`, `801C30D0`, `801C3278`, `801C3128` và `load_00216730`).
- **Chức năng đọc bảng**: Sử dụng bản vá hướng dẫn để thay đổi địa chỉ cơ sở bảng của `800A6E68`, `800A5254`, `800A8CE8`, `800A642C`, `800A67C8`, `800A68BC` thành cửa sổ ảo chứa bảng gốc cùng với các hàng mới.
- **Biểu tượng bản đồ**: 5 lần đọc được thay đổi thành bảng mới trong RAM trống.
- **ID Cap**: Giải phóng `0x531` và `0x1924`.
- **Tên**: Nối điểm gọi tên, ánh xạ tới ID văn bản riêng.
- ** LƯU TRỮ**: Theo cách đọc mã tuần tự của kho lưu trữ của tác nhân phụ, ID khung máy bay được lưu dưới dạng 10 chữ số (`id << 6 | 武器数`), với tối đa 63 vũ khí trên mỗi đơn vị và mỗi kho lưu trữ có một nhóm gồm 140 khung máy bay, 100 phi công và 700 vũ khí (đang chờ xác minh). Do đó, ID nội dung mới phải ≤ 1022 và bản lưu trữ sẽ phụ thuộc vào MOD - tải mà không có MOD sẽ âm thầm đọc dữ liệu không chính xác, yêu cầu dấu vân tay hoặc tệp đi kèm và `src/srw64_native/checkpoints.py` hiện từ chối các trường bổ sung.
- Thiếu điểm đọc nào sẽ âm thầm đọc lỗi mà không báo lỗi. Đây là rủi ro chính của tuyến đường này.

### Route C: Mở rộng ROM

Máy chủ đã hỗ trợ các biến thể ROM dữ liệu (`config/recomp/rom-variants.json`), với các ROM có sẵn tại `0x1D8C000–0x2000000` (2,45 MiB) và `0x86B000–0x89A000`. Tuy nhiên, kết nối đầu cuối của mỗi bảng, địa chỉ cơ sở và giới hạn trên đều là các hằng số mã. Bản thân việc mở rộng chỉ giúp chuyển hướng tài nguyên của tuyến A. Các byte mã lớp phủ phải nhất quán với mã gốc (từ đó mã biên dịch lại được tạo ra) và biến thể cũng mang đến các khóa lưu trữ và khóa băm riêng biệt, cần được phân phối dưới dạng một bản vá.

### Quy trình sản xuất nghệ thuật mới

1. Vẽ sơ đồ cơ thể (tư thế chiến đấu và các bộ phận tác dụng của vũ khí) và định lượng trong phạm vi 256 màu.
2. Công cụ đảo ngược cắt thành các phần 32×32, sắp xếp thành tập bản đồ kích thước 32k+1, tạo bảng màu và cảnh chế độ 0 (8 đỉnh cho mỗi phần, bộ thứ hai được phản chiếu). Định dạng đã được nhà xuất khẩu này xác minh từng bước và kiểm tra, công cụ này vẫn chưa được viết.
3. Viết mục tóm tắt cảnh và ghi lại diễn viên hoạt hình vũ khí cho mỗi hành động. Quy trình hành vi chọn hành vi tương ứng từ 270 hiện có (tư thế bắn 359, chùm 118, chém 43/44, v.v.). `animations.json` có thể được sử dụng làm thư viện tham khảo được tạo sẵn.
4. Phiên bản HD tiếp tục được thay thế bằng hàm băm kết cấu.

### Dự án yêu cầu xác minh máy thực tế

Số tiền thực tế còn lại của ngăn xếp trong trận chiến; số lượng VI tương ứng với một nhịp; ý nghĩa của mã pha 0x43/0x45/0x46; các trường `0x118610` và `0x7D980`; Route A thay thế một cơ thể và chiến đấu một trận hoàn chỉnh (tấn công, phản công, phòng thủ bằng khiên, hủy diệt). Theo thực tế dự án, những điều này được xác nhận trước khi chạy.

## Các công cụ phát triển còn lại

- **`load_00089EA0`: NGƯỜI XEM ROBO. ** Trình xem hình ảnh khung máy bay để gỡ lỗi đi kèm với bảng cảnh gồm 1.449 mục (ROM `0x8AB58`).
- **`load_00217FD0`: Trình chỉnh sửa hoạt ảnh chiến đấu. ** Tải `0x80400000`, ghi kết quả chỉnh sửa vào `0x80250010` và điều khiển với ID vũ khí đặc biệt `0x1000`.
- Bảng tên của nó (`0x80402E3C`) ghi tên các mục trong bảng tóm tắt cảnh chiến đấu, chẳng hạn như 222 "WepIanNet", 121 "WepGndm00", 602 "WepBSRedSwing1".
- Tên quy trình ở cuối bảng (BtlProcShield, BtlProcCoverDiffence, BtlProcBeamShield, v.v.) tương ứng với ID quy trình hành vi ở độ lệch 767.
- Hạn chế chỉnh sửa là sổ đăng ký < 0x41B, hành vi 0x17F, h6 ≤ 4.
- Những tên này là nguồn tốt nhất để đặt tên cảnh và quy trình hành vi, có thể được xuất cùng nhau trong bước tiếp theo.