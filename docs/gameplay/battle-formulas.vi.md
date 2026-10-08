> **Ngôn ngữ / Language:** [Tiếng Việt](battle-formulas.vi.md) · [English](battle-formulas.en.md) · [中文](battle-formulas.md)

# Tính toán chiến đấu: sát thương, đòn đánh, đòn chí mạng, quyết tâm phòng thủ và chỉ huy tinh thần

Ngày: 20-09-2026. Bài viết này ghi lại tất cả các tính toán mà trò chơi thực sự thực hiện trong một trận chiến: công thức sát thương và đòn đánh, đòn chí mạng, năm loại quyết định phòng thủ, ba lệnh của người phòng thủ và cách các lệnh tinh thần viết lại những giá trị này. **Trừ khi có ghi chú khác, kết luận là xác nhận mã tĩnh** (đã được tháo rời `build/recomp/cpu-scan/load_000AB160/rom_801C2600.text.s`, giá trị bảng được đọc trực tiếp từ `rom.z64`); công thức thiệt hại phù hợp với 24 dòng dữ liệu đang chạy. Để biết hiệu suất (hoạt hình), vui lòng xem [Hoạt hình chiến đấu và Máy bay tùy chỉnh](../data/battle-animation.md) và để biết tài nguyên hình ảnh, vui lòng xem [Hình ảnh chiến đấu](../data/battle-graphics.md).

2026-10-01 Theo xác minh tĩnh trên trang dữ liệu chiến lược, khoảng cách hiệu chỉnh tình yêu, thứ tự byte địa hình, phạm vi bỏ qua phải đánh, tình trạng vũ khí của lá chắn/EN/phòng thủ tăng gấp đôi/đặt lại về 0, lượng so sánh và thời lượng tinh thần của てかげん đã được sửa, đồng thời thêm phần giải quyết bắt đầu vòng đấu, V-MAX, siêu chế độ và tiền thưởng quỹ hạ gục (§7); ngày tháng và địa chỉ được ghi chú khắp nơi.

Động lực trực tiếp để viết tài liệu này là giao diện trước chiến tranh: phiên bản gốc chỉ hiển thị tỷ lệ trúng đích. Người chơi không thể nhìn thấy sát thương, tỷ lệ chí mạng, xác suất phân thân/cắt/che chắn của đối thủ cũng như số lượng phân thân còn lại. Để bù đắp những điều này, trước tiên bạn phải xác nhận công thức ở mức độ mà bạn có thể tự tính toán lại.

## 0. Thứ tự thi hành trận đánh

```
801F7D6C  结算驱动（命中 801F4384 与伤害 801F5628 各三次：攻击／反击／二次攻击）
  └ 801F7204  判定顺序：命中掷骰 → 分身 → 切り払い → 假身 → 护罩 → S防御
```

Tất cả cuộc gọi bên trong `801F7D6C` đều nằm trong vùng logic `801E*`/`801F*`. Không có lệnh gọi đến đồ họa thường trú/các quy trình chờ và không có tính năng chặn nguyên thủy. Trong dữ liệu đang chạy, đòn tấn công và phản công của một hiệp chiến đấu được ghi trong cùng một VI (5316/6956/8336 của `rules-battle-1`). Dựa trên điều này, có thể suy ra rằng việc giải quyết và hiệu suất được tách biệt và một vòng giải quyết là không thể tách rời - nhưng hoạt ảnh trận chiến không được phát trong lần chạy này, vì vậy "việc giải quyết trước hiệu suất" chưa được đề cập trực tiếp trong bằng chứng chạy. Bằng chứng ở phía bên kia là **mã phản ứng phòng thủ** được đặt trong `801F7204` chính xác là những gì được đọc khi hoạt ảnh được phát (xem bảng mã phản ứng của [Hoạt hình chiến đấu](../data/battle-animation.md)) và cả hai tương ứng một.

## 1. Thiệt hại

Điểm nổi có độ chính xác đơn của IEEE xuyên suốt và cuối cùng được làm tròn `trunc.w.s`. `80203418` là phiên bản ước tính không tạo ra các đòn chí mạng (**không tiêu thụ số ngẫu nhiên** và có thể được gọi một cách an toàn trong giao diện trước chiến tranh), `801F5628` là phiên bản chiến đấu thực sự và cả **cho đến khi sửa lỗi tình yêu và giới hạn dưới 10** đều giống nhau theo hướng dẫn (phiên bản ước tính cũng áp dụng sửa lỗi tình yêu nhưng không tạo ra các đòn chí mạng; đánh giá tháo gỡ ngày 22-09-2026 `802035C8..80203644` và `801F5884..801F5928`).

```
stat = (武器[+0x04] & 0x80) ? 驾驶员[+0x22] 格斗 : 驾驶员[+0x24] 射击

A = 武器攻击力 × 武器地形适应 × stat/100 × 攻方气力/100 × 机体地形适应
D = 装甲 × (鉄壁 ? 2 : 1) × 守方气力/100 × 守方机体地形适应
R = (A − D) × 地形效果                    # 地形效果 = (100 − 地块防御)/100
R = R + (爱A ? R×0.3 : 0) − (爱D ? R×0.3 : 0)
R = max(R, 10)                            # 下限 10
if 攻方精神 魂:   R ×= 3
elif 攻方精神 熱血: R ×= 2
else【仅实战】暴击命中: R ×= 1.5
【仅实战】防御指令: R ÷= 2
【仅实战】守方机体 id == 149 → R 固定 10；R = min(R, 65535)
```

Những điểm chính:

- **Sức sống** nhân một lần cho mỗi bên tấn công và phòng thủ (`80203528` đối với người tấn công, `lhu 0x20($s2)`, `80203578` đối với người phòng thủ), với cơ số là 100.
- **Khả năng thích ứng với địa hình có tính chất nhân lên chứ không phải cộng tính**. Các bảng phóng đại `D_80218744` (ROM `0x1012A4`) và `D_8021874C` (`0x1012AC`) đều là `{0, 60, 80, 100, 120}`, tức là `-`/D/C/B/A → 0/60/80/100/120%. Vũ khí A + Máy Tổng cộng **1,44 lần**.
- **Về phía máy bay, lấy tổng thứ hạng máy bay và cấp phi công rồi chia thành các hạng khác nhau** (`800A6194`: tổng 0→0%, 1–3→60%, 4–5→80%, 6–7→100%, ** ≥8→120%**); bên vũ khí là một thứ hạng duy nhất (`801F40A4`).
- **Kênh địa hình được xác định bởi phần tay cầm của cơ thể**, không đọc bảng chiến đấu `+0x10`: `801F3FA8`, đánh giá theo thứ tự: toàn bộ bản đồ vũ trụ → không gian, loại độ cao = 1 → không khí, khối nước → biển, ngược lại → đất liền.
- **Kích thước không được tính vào công thức tính sát thương**. Kích thước (0/80/100/120/140) chỉ là hệ số nhân thực trong hàm tỷ lệ trúng `801F4568`/`801F4580`; chỉ có một nhánh thoái hóa trong sát thương sẽ không bao giờ gây ra trên cơ thể thật.
- **Chỉnh sửa tình yêu/tình bạn ±30%** (`801F4908`). Kẻ tấn công giữ +30% và người phòng thủ giữ -30%, chỉ ảnh hưởng đến sát thương và không ảnh hưởng đến đòn đánh; khi đối tác đầu tiên được tìm thấy, 1 sẽ được trả lại mà không cần xếp chồng.
- **Khoảng cách là tổng của khoảng cách ngang và dọc 2** (bao gồm các khoảng cách liền kề theo đường chéo, tổng cộng 13 lưới): `801F4A2C..801F4B7C` đánh dấu chiều rộng hàng 1/3/5/3/1 trong lưới 31×31 với **giá đỡ** làm hình thoi ở giữa, mỗi lưới sau đó sẽ vượt qua bước kiểm tra "lưới trong bản đồ" (`x ≥ 原点+32`, `x ≤ 原点+地图宽−48`, `D_80172EC4` được viết bởi `801C6394`, phán đoán tương tự như phạm vi chuyển động `801C44D4`/`801F2B24`), sau đó quét phần xử lý của chúng tôi 0x42–0x5F Đối tác trong ảnh. Bất kể phạm vi hiển thị của màn hình. (Sửa vào ngày 2026-10-01: Trước đây nó được viết là "cửa sổ 31×31 được cố định bởi ống kính và sau đó được cắt thành khung nhìn".)
- Chỉ dành cho phía chúng tôi: `801E510C` trả về 0 nếu trại khác 0 (`801F49FC`); danh sách `+0x101 & 0x80` cũng trả về 0 nếu được đặt. Trong cảnh 4–9, nhân vật 196 Kagu và 197 Yuko không được chỉnh sửa với tư cách là người nắm giữ (`801F4988..801F49C4`).
- Bảng ghép nối `D_80218754` (ROM `0x1012B4`), 47 dòng × 8 byte: `+2` số vai trò chủ sở hữu, `+4`/`+6` đối tác 1/2 (−1 Không có), `+0` mã không được đọc. Cả hai cột đối tác đều được so sánh (`801F4C64`/`801F4C78`), vì vậy hàng 24 デューク←ひかる,ナイーダ và hàng 27 デューク←ひかる,ナイーダ được so sánh với hàng 27 锅←さやか,マリアVới các hàng đảo ngược tương ứng, cả hai đều **hai chiều** (được kiểm tra vào ngày 2026-10-01).

### Vị trí byte xếp hạng

| | Bảng ROM | sải bước | bù đắp nội tuyến | đặt hàng |
| --- | ---: | ---: | --- | --- |
| Máy bay | 465792 | 36 | **14–17** | Không/Đất/Biển/Không gian |
| Vũ khí | 478864 | 16 | **9–12** | Tương tự như trên |

2026-10-01 Lệnh sửa đổi (trước đây được viết là "Biển/Không/Đất/Không gian"): Máy bay Minovsky của `800A5254` được phân nhánh thành loại di động `0x02` và phiên bản thân văn bản `+0x16 = 4`, phiên bản vũ khí `+0x10 = 4` (nghĩa là byte đầu tiên trống), siêu chế độ `801FE96C` Chỉ thay đổi vũ khí `+0x11..+0x13` (đất/biển/không gian); Dữ liệu ROM アーガマ `[A,-,-,A]`, ゲッター3 `[-,A,A,B]` nhất quán.

Các trường khác trong cùng một bảng: khung máy bay `armor` nằm ở vị trí bù 10 (u16) trong hàng; vũ khí `power` ở mức 1 (×100), `hit_modifier` ở mức 4 (**đã ký**), `en_cost` ở mức 6, `will_required` ở mức 7, `critical_modifier` ở mức 13 (đã ký). Lưu ý rằng phần bù `numeric_fields` của `config/data/original-jp-v1.json` là phần bù trong bảng ROM, không phải phần bù bản ghi thời gian chạy - việc đọc ở phần bù thời gian chạy sẽ nhận được các trường không liên quan.

### Chạy xác minh

24 dòng `build/recomp/mini-stage/rules-aura-1/rule-probe.jsonl``damage` (máy dò gọi `80203418` thật) khớp chính xác với **24/24** sau khi được thay thế vào công thức trên và số dư là 0. Địa hình của cấp độ này trống rỗng và sức mạnh của cả hai bên không đổi 100.

> **Cảnh báo về phương pháp. ** Cùng một dữ liệu được gắn "`1.2 × (攻击力 − 装甲) + 每攻方常数`" ** cũng chính xác 24/24**, nhưng cấu trúc hoàn toàn sai - vì trong tập dữ liệu này, sức mạnh luôn là 100 và khả năng thích ứng địa hình vũ khí của kẻ tấn công luôn là A, cả hai biến đều được hấp thụ vào hằng số hạn.真实形式是纯乘法后相减，没有任何加性常数。 **Khớp và đồng ý không có nghĩa là công thức đúng**; các biến phải được thay đổi thực sự hoặc được xác thực chéo bằng mã/chiến lược.

Cho đến nay, mục lực lượng chưa được bao gồm trong dữ liệu vận hành (lực lượng của tất cả các bộ dữ liệu hiện có là không đổi 100). [`config/recomp/mini-stages/damage-morale.json`](../../config/recomp/mini-stages/damage-morale.json) đã được chuẩn bị cho việc này: một lệnh thay đổi thành `rules.json`, chèn `3D5F` (cường độ tổng thể 100→70) trước `3D38` đầu tiên. Việc so sánh giữa giá trị dự đoán và phép đo thực tế vẫn chưa được hoàn thành.

## 2. Tỉ lệ trúng

```
base = (攻方命中 + 攻方反应 + 武器命中修正 + 100 + 攻方运动性)
     − (守方回避 + 守方反应 + 守方运动性)
       再乘尺寸与地形倍率（801F4568 / 801F4580）
```

短路与修正（`801F4384`，按代码出现顺序）：

| Tình trạng | Hiệu ứng | Vị trí |
| --- | --- | --- |
| **Phòng thủ** Tinh thần ひらめき（`+0x1C & 0x20`） | **Trả về 0** trực tiếp và đặt tùy chọn "Tránh!" cờ nhắc | `801F4460` |
| **Tấn công** Tinh thần phải đánh (`& 0x80`) | **Trả trực tiếp 100** (Khe trễ `addiu $v0,$zero,0x64`) | `801F44A0` |
| **Tấn công** Tập trung tinh thần (`& 0x10`) | `hit += 30` | `801F4584` |
| **Hậu vệ** Tập trung tinh thần | `hit −= 30` | `801F45A4` |
| **Tấn công** `+0x1C & 0x800000` (Spirit id 23, hỗn loạn, được thêm vào từng đơn vị kẻ thù/bên thứ ba bởi người điều khiển `801D9F94`) | `hit ÷= 2` | `801F472C` |
| **Tránh lệnh** (tham số một nửa) | `hit ÷= 2` | `801F4750` |

Hai mục cuối cùng **độc lập và có thể xếp chồng** (tối đa 4). Lưu ý khe trễ MIPS: `andi $v0,$s7,0xFF` của `801F473C` được thực thi trước khi nhánh trước có hiệu lực, do đó, phán quyết thứ hai sử dụng các tham số thay vì các bit tinh thần.

Tiếp tục `801F7204`: `hit` kẹp 0–100, `r = rand(99)+1` (**1..99**), `hit >= r` trúng.因此**命中率 99 与 100 效果相同**,命中率 0永不命中。

> Công thức này chỉ khớp chính xác 2 trong số 24 dòng `rules-aura-1` và phần dư thay đổi một cách có hệ thống tùy theo vũ khí và cơ thể của người phòng thủ - phương pháp cụ thể để chọn hệ số kích thước/địa hình chưa được xác nhận từng mục. **Giao diện trước chiến tranh nên gọi trực tiếp hàm ước tính của trò chơi `80204254`** (cũng không sử dụng số ngẫu nhiên, `rule_probe.hpp` đã đóng gói lưu/khôi phục bàn chiến đấu), thay vì tự tính toán lại.

## 3. Đòn chí mạng

`801F47B0`:

```
rate = 攻方技量[+0x2C] − 守方技量 + 武器暴击修正[行内偏移 13, 有符号]
阵营 0（我方）：rate += 底力补正（801E1D64，0–90）
阵营 1、2（敌／第三方）：rate /= 4        ← 且不加底力
rate = max(rate, 1)
暴击 = rand(100) < rate     →  伤害 ×1.5
```

Trại được xác định bởi tay cầm của kẻ tấn công: `801E510C` được chia thành ba loại theo `<0x60 / <0x7E / 其他` và mã tay cầm là `0x42/0x60/0x7E + 槽位` tương ứng với trại 0/1/2 (xem `src/host/rule_probe.hpp:27`).

**Kẻ địch gần như không bao giờ nhận được đòn chí mạng. ** Chỉ có tám loại hiệu chỉnh đòn chí mạng của vũ khí trong bảng: `-20/-10/-5/0/10/15/20/30`; kỹ năng cơ bản của trùm là 95–117 và chống lại đồng minh có khoảng 120 kỹ năng:

| Kẻ thù | Kỹ năng cơ bản | Vũ khí +0 | +20 | +30 |
| --- | ---: | ---: | ---: | ---: |
| ギュネイ | 117 | 1% | 4% | 6% |
| ガトー | 110 | 1% | 2% | 4% |
| ハマーン | 108 | 1% | 1% | 4% |
| シャア／シロッコ | 105 | 1% | 1% | 3% |
| キラル・メキレル | **155** | 8% | 13% | 16% |

Trong số 257 phi công, người có kỹ năng cơ bản cao nhất là Kirara (155), chỉ đạt 16% ngay cả khi có +30 vũ khí. Trong cùng điều kiện, chúng ta có thể đạt tới 29–32%.

**Không có đòn chí mạng nào được tung ra khi máu/linh hồn có hiệu lực**: `801F5A14` chỉ được gọi khi cả hai bit đều không được đặt, nếu không, cờ chí mạng bị buộc về 0. Nghĩa là, "Hot Blood ×2" và "Crit ×1.5" **không thể cùng tồn tại**.

## 4. Phán quyết phòng thủ (sau khi đánh, loạt thoát sớm)

Trình tự: **Nhân bản → Cắt → Sai → Khiên → Phòng thủ S**. Mỗi vật phẩm chỉ có tác dụng đối với các đòn tấn công "đáng lẽ phải trúng", vì vậy khi các xác suất được hiển thị, chúng là **xác suất có điều kiện**. Khi `+0x1C & 0x80` (phải đánh) của phi công tấn công được đặt, **chỉ bỏ qua bản sao và cắt り払い**: `801F7204` chỉ kiểm tra một lần sau hai mục này xem có chắc chắn trúng không (`801F7384`, `801F73D8`), `801F6E3C` giả và vị trí tiêu thụ của nó `801FCC28` Bất kể cái gì, lá chắn và phòng thủ S đều giống nhau. (Sửa lại 01-10-2026: Trước đây nó được viết là "bỏ qua ba mục đầu tiên".)

| Phán quyết | Xác suất/Hiệu ứng | Tình trạng | Vị trí |
| --- | --- | --- | --- |
| **Bản sao** | **Đã sửa 50%** | Cơ thể `+0x28 & 0x163011` và sức mạnh phi công `+0x20 ≥ 130` | `801F6C44` |
| **cắtり払い** | `等级 / (16 × scale) × 100%`: `scale` Tay cầm **người phòng thủ** đi qua `801E510C` để lấy trại, phe ta (0) là 1, địch và bên thứ ba là 2, tức là L9 của ta = 57% (ném 0–99 nhỏ hơn 56,25 để thành công), L9 của địch = 29% | Phiên bản vũ khí hiện tại của kẻ tấn công `+0x04 & 0x08` bit ("có thể cắt", từ byte 0 của bản ghi ROM vũ khí), phần thân `+0x20 & 0x01` (được trang bị kiếm), phi công `+0x36 & 0x01`, cấp độ `+0x07` khác 0. Khi thành công nhấn vũ khí tấn công `+0x22 & 1` để trả về 0x13 hoặc 0x12 là hai kết quả | `801F6D10` |
| **Giả** | Xác định, không tung xúc xắc | Phe không phải là 0, đã đặt đội hình `0x80`, tài xế `+0x14 ≠ 0`; sau khi có hiệu lực, trường này là −1 | `801F6E3C` |
| **Rào chắn hào quang** | **Ngưỡng hấp thụ**: Ngưỡng `3000 + 表[主驾驶员圣战士等级]`, **Khi người phòng thủ chọn phòng thủ ×2**. Thiệt hại ≤ ngưỡng → **Đặt lại về 0**, mức tiêu thụ EN +5; > Ngưỡng → **Vượt qua** (kết quả 0xF), sau đó **Không còn xác định lá chắn phổ thông và phòng thủ S** | Nội dung `+0x28 & 0x4000`; Vũ khí của kẻ tấn công là bắn tia; EN của hậu vệ là 5 | `801F6ED0`/`801F6EE0`, `801F7520..801F75C0` |
| **Khiên đa năng** | **Trừ và chồng**: `2000·[0x800 行星防御] + 2000·[0x20 I力场] + 1000·[0x200 光束涂层]`, **Trong khi phòng thủ ×2**; Lá chắn ≥ sát thương → **Sát thương 0** (`801F7704`), nếu không thì `max(伤害 − 护罩, 10)`; Trong cả hai trường hợp, mức tiêu thụ EN là +5 | Vị trí tương ứng của phần thân `+0x28`; Vũ khí của kẻ tấn công là bắn tia; Chân EN của hậu vệ 5 | `801F6F3C`, `801F7668..801F7740` |
| **Phòng thủ S** | Xác suất là như nhau và cũng được chia theo trại 16/32 của người phòng thủ (sử dụng trình điều khiển `+0x08` cấp độ / vị trí kỹ năng `0x02` / vị trí trang bị cơ thể `0x02`; bất kể vũ khí của kẻ tấn công); hiệu quả là thiệt hại giảm đi một nửa và làm tròn xuống bội số của 10, tối thiểu là 10**, thiệt hại < 20 không được xử lý | Tương tự như trên | `801F6FDC` |

Mặt nạ nhân bản `0x163011` đã được kiểm tra với họ "tránh" `unit_abilities` bảy mục của `config/data/original-jp-v1.json`: bản sao `0x10`, Mach đặc biệt `0x1000`, Mach thực sự đặc biệt `0x2000`, bản sao của Chúa `0x1`, Getter Phantom `0x20000`, Chân kính thiên văn `0x40000`, Máy gây nhiễu siêu âm `0x100000` và sự kết hợp **chính xác** `0x163011`. Bảng rào cản hào quang `80218930` (ROM `0xab160 + 0x80218930 − 0x801c2600`) đã được đọc từ ROM: `0, 200, 400, 600, 800, 1000, 1200, 1300, 1400, 1500`.

Một số điểm đáng lưu ý:

- **Bản sao không liên quan gì đến cấp độ hay kỹ năng**, nó chỉ phụ thuộc vào việc sức mạnh có đạt tới 130 hay không.
- **Rào chắn hào quang là hiệu ứng vách đá**: gần như không bị xuyên thủng sẽ hoàn toàn không có tác dụng, nếu bị xuyên thủng sẽ hoàn toàn vượt qua. Giao diện trước trận chiến hiển thị "Thêm N sát thương để xuyên thủng" rất có giá trị.
- **Số lượng hình đại diện còn lại không được hiển thị trong trò chơi gốc** (xem [Sửa chữa cơ bản](base-fixes.md)).
- Lá chắn được đánh giá **sau khi tính toán sát thương** nên để dự đoán kết quả của lá chắn thì sát thương cũng phải được tính toán.

- **Cut り払い chỉ có tác dụng với vũ khí có bit "cutable"** (Bản ghi ROM vũ khí byte thứ 0 `& 0x08`, `800A6A44` được sao chép vào phiên bản `+0x04`). Trong tổng số 1.329 vũ khí, 574 chiếc có phần này: 183 chiếc dành cho tên lửa, ngư lôi, lựu đạn và các loại vũ khí bắn đạn thật khác, và 391 chiếc dành cho vũ khí chiến đấu; không có nó cho dầm và súng máy. Đó cũng không phải là tất cả về chiến đấu: 192 mảnh chiến đấu, bao gồm Nắm đấm kinh thiên động địa, Ngón tay của Chúa và Quyền anh, không thể bị cắt bỏ.
- **Xác suất cắt và phòng thủ S được chia theo phe phòng thủ**: phe ta `等级/16`, phe địch và bên thứ ba `等级/32`. Sửa chữa 01-10-2026: Trước đây, bảng này viết điều kiện là "id vũ khí < 0x60". Tham số thực tế của `801E510C` là tay cầm của người phòng thủ; trang trước chiến tranh của máy chủ `src/host/defense_preview.hpp` luôn được tính toán theo trại và thăm dò tùy chọn `battle_ui_probe.hpp` giống với chức năng ban đầu 32/32 nhất quán([trang gốc trước chiến tranh](../native/native-battle-ui.md)).

2026-10-01 Sửa bốn điều kiện cho khiên (rào chắn năng lượng tâm linh và khiên phổ quát). Phần này chưa được viết trước đây hoặc được viết sai:

| Mặt hàng | Sự kiện mã | Địa điểm |
| --- | --- | --- |
| Chỉ bắn vào chùm tia | Nếu phiên bản vũ khí của kẻ tấn công `+0x04 & 0x02` (byte ROM vũ khí 0) không được đặt, toàn bộ phần sẽ bị bỏ qua. 225 trong tổng số 1329 mảnh có bit này, tất cả đều là bắn và không có giao điểm với "cutable" `0x08`; kiếm tia, pháo nổi/pháo nổi vây, chùm Getter, tia lực photon và pháo Aura không được trang bị nó | `801F7470` |
| "×2" là lệnh phòng thủ | "Địa hình 2" đến thực tế là `+0x10` (`D_8018B6F8`, kích thước bước 0x5C) của từng mục trong bảng chiến đấu; mục đầu tiên là byte lệnh `D_8018B754` của §5, giá trị 2 = phòng thủ. Mục 0 (kẻ tấn công ban đầu) được đặt thành −1 trong `801F7B54`, vì vậy kẻ tấn công ban đầu không thể nhận được ×2 trong khi phản công | `801F6F20`, `801F6FB4` |
| Yêu cầu và tiêu thụ EN 5 | `EN − 反击武器 EN ≥ 5` là bắt buộc khi người phòng thủ chọn phản công, nếu không thì bắt buộc phải có `EN ≥ 5`; `D_8018B6FF` (Tiêu thụ EN) +5 được cấp để chặn hoặc giảm sát thương | `801F70DC`, `801F74E8`, `801F7704` |
| Lá chắn ≥ Sát thương trở về 0 | Chỉ "Sát thương > Lá chắn" mới có `max(伤害 − 护罩, 10)`; sau khi hàng rào hào quang bị xuyên thủng, đoạn khiên sẽ trực tiếp kết thúc và phòng thủ S sẽ không tiến vào | `801F7704`, `801F7520..801F75C0` |

Chưa giải quyết: Việc ánh xạ lại mã thông báo của lá chắn có một nhánh không thể truy cập được; hai kết quả 0x12/0x13 được trả về khi cắt thành công (theo vũ khí của kẻ tấn công `+0x22 & 1`, bit này được đặt trên vũ khí đấu kiếm) không được kiểm tra xem chúng tương ứng với hiệu suất nào. Không ảnh hưởng đến số học thiệt hại.

## 5. Ba lời chỉ dẫn cho người phòng thủ

Bộ chọn là **byte đã ký `D_8018B754`**: `-1` không được chọn, `0` phản công, `1` tránh, `2` phòng thủ.
(`D_8018B74C` là **con trỏ vũ khí phản công**, 0 có nghĩa là không phản công, không phải là bộ chọn lệnh.)

`801F84D4``bnez $v1` bị tắt và khe trễ được đặt `$v0` thành 1 làm giá trị so sánh:

| Lệnh | Tỷ lệ trúng | Thiệt hại | Phản công |
| --- | --- | --- | --- |
| **Phản công** (0) | Giá trị gốc | Giá trị gốc | ✓ (`801F69D8` chọn vũ khí) |
| **Tránh**(1) | ** 2** | Giá trị gốc | ✗ |
| **Phòng thủ** (2) | Giá trị gốc | ** 2** | ✗ |

Phòng thủ cũng tăng giá trị lá chắn và ngưỡng rào cản hào quang lên ×2 (§4, được bổ sung vào ngày 01-10-2026).

Nhánh tránh (`.L801F86DC`)** chỉ gọi `801F4384`**, nhánh phòng thủ (`.L801F870C`)** chỉ gọi `801F5628`** - mỗi nhánh không chạm vào chức năng kia. Cả hai đều đặt `D_8018B74C` thành 0 để hủy phản công.

Tham số thứ ba của chính `801F7D6C``$s7` chỉ xuất hiện 6 lần trong toàn bộ hàm và không bao giờ được chuyển dưới dạng tham số cho đòn đánh/sát thương; `a2` trong số sáu điểm gọi đều là các chữ được mã hóa cứng và chỉ các nhánh tránh/phòng thủ vượt qua 1.

**Lựa chọn tự động AI** (`801F7B34`): `slti 0x15` - tỷ lệ trúng dự đoán **< 21, chọn tránh, nếu không thì chọn phòng thủ**; Ngoài ra, trong `801F849C`, nếu bạn vẫn bị bắn hạ sau khi phòng thủ (`伤害>>1 ≥ 攻方武器+4`), **chuyển sang tránh**.

Hỗ trợ chiến lược: Wiki dòng SRW tuyên bố rằng "tỷ lệ trúng giảm một nửa theo lệnh tránh", điều này phù hợp với mã. Không có hồ sơ nào về các giá trị số cụ thể về khả năng phòng thủ của SRW64 nên mã sẽ được ưu tiên áp dụng.

## 6. Hướng dẫn tâm linh

Bản ghi hoạt động của người lái xe `+0x1C` (word) là bitmap hiệu ứng tinh thần, **id tinh thần là số bit** (`bit = 1 << id`, do `801E0E6C(id, unit)` đặt, luôn ghi phi công đầu tiên của máy bay `+0x38`, do đó, trạng thái tinh thần do phi công phụ tạo ra cũng ảnh hưởng đến toàn bộ máy bay; thân hệ thống tháp 171–179 Sau đó sao chép nó cho hai người khác). tên tinh thần = văn bản 969+id. 31 mục trong `jtbl_8021ED08` là quyết định "có thể sử dụng ngay bây giờ không", chứ không phải bản thân diễn viên; nhiệm vụ casting là `801D6A68(id, 免费)` → trạng thái chiến thuật `0x1A + id`.

| id | chút | tinh thần | hiệu ứng | địa điểm đọc |
| ---: | --- | --- | --- | --- |
| 2 | `0x4` | Tăng tốc | Chuyển động +3 | `801CBA60`, `80201D14` |
| 3 | `0x8` | てかげん | Khi HP mục tiêu ≥ 20 và kỹ năng của kẻ tấn công (`+0x2C`) lớn hơn kỹ năng của người phòng thủ**, sát thương sẽ bị hạn chế và mục tiêu sẽ có 10 HP; vũ khí tấn công, phản công và bản đồ đều sẽ được đánh giá | `801F5B78` (`sltiu HP,0x14`, `sltu 守技量,攻技量`); gọi `801F875C`/`801F8774`/`801FE330` |
| 4 | `0x10` | Nồng độ | Đòn đánh của kẻ tấn công +30/Đòn đánh của người phòng thủ −30 (đối xứng) | `801F4584`/`801F45A4` |
| 5 | `0x20` | ひらめき | do người phòng thủ nắm giữ → tỷ lệ đánh** trả về 0** (phải đánh trước) | `801F4460` |
| 7 | `0x80` | Phải đánh | Kẻ tấn công giữ → Tỷ lệ trúng** trả về 100** và bỏ qua việc sao chép/cắt; **không bỏ qua bản sao** | `801F44A0`, `801F7384`/`801F73D8` |
| 9 | `0x200` | Tường Sắt | Hậu vệ **Giáp ×2** | `801F57D8` |
| 10 | `0x400` | みがわり | Khi đồng minh được bảo vệ là người phòng thủ, người thực hiện sẽ chiến đấu thay thế và sau đó xóa vị trí; nó sẽ không được thay thế khi đồng minh được bảo vệ có ひらめき | `801F7844` (`+0x1C & 0x420 == 0x400`) |
| 11 | `0x800` | Máu nóng | Thiệt hại ×2 | `801F59CC` |
| 14 | `0x4000` | May mắn | Quỹ ×2 | `801F673C` |
| 16 | `0x10000` | Nỗ lực | Kinh nghiệm ×2 | `801F635C` |
| 17 | `0x20000` | Linh hồn | hư hại |
| 18 | `0x40000` | Gakushen | Vũ khí của kẻ thù không thể nhắm mục tiêu vào nó và nó không bị ảnh hưởng bởi khả năng tự hủy | `801F89E4`, `801EFA14` |
| 21 | `0x200000` | Thử thách | AI của kẻ thù bị khiêu khích chỉ nhắm vào người thực hiện | `80203F24` |
| 23 | `0x800000` | かくRAN | Được thêm vào **mỗi** đơn vị kẻ thù/bên thứ ba khi sử dụng; khi người dẫn đầu tấn công (bao gồm cả phản công), tỷ lệ trúng đích của chính nó ÷2 | `801D9F94`, `801F472C` |

Sửa chữa 01-10-2026: id 3 trước đây được viết là "Tấn công HP > Người bảo vệ" và địa chỉ được viết là `801F5BB4` trong hàm; kỹ năng so sánh thực tế là `801F5B78`. Có một nhánh khác có chức năng tương tự không liên quan gì đến tinh thần: cơ thể của người phòng thủ `0xB9` (ガイヤー) giữ lại 10 HP một cách vô điều kiện. id 7 trước đây được viết là "bỏ qua phần thân giả", xem §4.

**Thời lượng** (`801E0F9C`/`801E1070` xóa các bit theo bảng mặt nạ):

- Xóa sau một nước đi: `0x4` tăng tốc (`D_80218054`, được gọi từ `801C2A2C`/`801CCC70`/`801CD28C` khi kết thúc nước đi, chỉ xóa đơn vị này)
- **Khi số vòng là +1, tiêu diệt tất cả các đơn vị có mặt trong ba phe**: `0x10` Tập trung, `0x200` Tường sắt, `0x80` Phải đánh, `0x800000` Hỗn loạn, `0x40000` Gakushen (`D_80218058`; `801FA88C` Thêm 1 vào số số vòng `D_8010F5EA` và điều chỉnh giới hạn trên thành 250 đến `801E1070(0)`). Vì vậy, những hiệu ứng này được thực hiện trong giai đoạn người chơi có hiệu lực trong suốt giai đoạn của kẻ thù. (Sửa lại 01-10-2026: Trước đây được viết là "kết thúc vòng đấu".)
- **Sau một trận** Rõ ràng: `0x800` máu, `0x20000` linh hồn, `0x4000` may mắn, `0x10000` nỗ lực, `0x8` てかげん(`D_8021806C`); trận chiến thông thường `801FCA78` Xóa một lần cho cả bên tấn công và phòng thủ. Vũ khí bản đồ `801FE068` chỉ tiêu diệt phe tấn công.
- Not in any mask: `0x20` ひらめき is set to `D_8018B72B[侧]` when triggered, cleared by `801FB460` (normal combat settlement) / `801FE068` (map weapon), and will be kept until triggered; `0x400` みがわり nằm trong `801F7844` sẽ bị xóa sau khi thay thế; `0x200000` Challenge is only cleared when the linked object is removed (`801E11B0`), mounted/integrated/separated command sub-state or resurrection reset (`801F13C4`), there is no round limit

**SP tiêu thụ**: u8 × 32 bảng `D_80217F70` (ROM `0x100AD0`), sắp xếp theo id: `1 1 10 10 15 15 20 25 30 30 35 40 40 40 45 50 20 60 60 60 65 35 70 70 70 90 90 100 100 120`, mục 31 (id 30) = 1. `801E195C` được trừ vào `+0x16` của phi công (tập lệnh `3D55` bị bỏ qua khi truyền miễn phí); `801F1B10` được `SP < 消耗` đánh giá là không đủ, vì vậy SP có thể được sử dụng ngay cả khi đã tiêu thụ. ID 30 không có tên và văn bản mô tả và không có trong 148 bảng học. Hiệu quả là toàn bộ sức mạnh của người lái xe +30 (`801E1380`: `id==30 ? 30 : 10`). AI của kẻ thù không có đường dẫn thi triển tự động: `801D6A68` chỉ có hai người gọi: menu tinh thần của người chơi `801D69EC` và tập lệnh `3D55` (`80210490`). (Được thêm vào ngày 2026-10-01, trước đây đã viết "vị trí chưa được xác định".)

Mô tả hiệu ứng và mức tiêu thụ SP được đưa ra trong hướng dẫn chiến lược (`srw.wiki.cre.jp`'s Spirit コマンド/64 trang) phù hợp với bảng trên: tăng tốc 10, nồng độ 15 (tránh đòn +30%), ひらめき 15 (tránh hoàn toàn một lần), root 20, chắc chắn trúng 25 (đòn 100%), tường sắt 30 (áo giáp) 2 lần), máu 40 (sát thương 2 lần), dung hợp 40 (sức mạnh +10), căn bản 40, linh hồn 60 (sát thương 3 lần).

Bảng `spirits` (ROM 511920, sải bước 12, dòng 148) không phải là bảng định nghĩa tinh thần mà là danh sách thu thập cho mỗi trình điều khiển: 6 bộ `(等级, 精神id)`. Cấp độ của tất cả các hàng 148 đều không giảm đơn điệu và các id đều nằm trong phạm vi 0-29, phù hợp với không gian id của bảng nhảy.

Hiệu ứng thi triển của tất cả 30 linh hồn (lựa chọn mục tiêu, tỷ lệ hồi phục, giới hạn sức mạnh trên và dưới, thứ tự diễn ra các phép màu, v.v.) được trình bày chi tiết trên trang thông tin chiến lược (tab Lệnh Linh Hồn của `guide/data/zh-Hans/reference.json`); phần này chỉ liệt kê các vị trí vào tính toán trận đánh.

## 7. Thanh toán khi bắt đầu vòng đấu, V-MAX, chế độ siêu và quỹ giảm giá (Bổ sung vào ngày 2026-10-01)

**Giải quyết đầu vòng** `801FA3DC`: Được `801FA88C` gọi sau số vòng +1, vượt qua 3 phe

| Mặt hàng | Nội quy | Địa điểm |
| --- | --- | --- |
| VN trả lời | EN +5 cho mỗi đơn vị (giá trị tuyệt đối, không vượt quá giới hạn trên) | `801FA450..801FA460` |
| Thu hồi đất | HP%/EN% theo loại đất (`D_802196D3/D4`) | Chức năng tương tự |
| Phục hồi HP | Bit khả năng `0x4` → HP tối đa 10%, nếu không `0x8` → 20%; `当前 + 上限/100 × 百分比`, bị cắt ngắn, không vượt quá giới hạn trên | `801FA550..801FA578`, `801FA260` |
| Bên trong tàu mẹ | Được trang bị HP và EN +25% của tàu hạng trung, bổ sung đạn dược; lần đầu tiên của mỗi đơn vị (không đặt cờ vị trí 0x80), điều chỉnh bổ sung `801F12B0(机体,10)`: cường độ thí điểm −10, giới hạn dưới 50 | `801FA5A4..801FA640` |

**V-MAX** (bit khả năng `0x10000`): `801FF1BC` đi ngang qua tay cầm 0x42–0x9B **tất cả các trại**, công suất của trình điều khiển chính là ≥ 130 và `+0x1C` bit 30 không được đặt → `801FE9CC(…,1)`: đầu tiên `800A5254` Tính toán lại theo giá trị ban đầu, sau đó di chuyển công suất +1, khả năng di chuyển +20, giới hạn +100 và cấp độ khả năng `|= 0x200` (lớp phủ chùm tia). **V-MAX Red Power**: Cơ thể 278 (ザカール), bộ vị trí 30, sức mạnh ≥ 140 → `801FEA70`: Sau khi tính toán lại, độ linh hoạt +2, độ linh hoạt **+40**, giới hạn **+200**, lớp phủ chùm tia, bộ vị trí 31; bởi vì việc tính toán lại trước tiên sẽ thay thế chứ không phải chồng lên V-MAX. Cả hai đều không được giải phóng bằng vũ lực và chỉ được giải phóng khi quá trình xử lý sự cố `801FF63C` → `801FF4E0` được thực hiện.

**Siêu Chế độ/Shisui Shisui/Berserker**: Giống như `801FF1BC`. ký tự 0x12 (Phương Đông bất bại) bất kỳ trại nào; 4, 8, 0xB, 0xC, 0xD (ドモン, アルゴ,サイ・サイシー、ジョルジュ、チボデー) chỉ về phía chúng tôi; 9 (アレンビー) chỉ vào kẻ thù; Strength ≥ 130 → `801FEDF4`: Tìm phần thân hiện tại trong bảng mẫu `D_80218A34` (dòng 9 [bình thường, nâng cao]). Nếu không tìm thấy, nó sẽ không được kích hoạt; nếu tìm thấy, nó sẽ được tính toán lại và đặt thành 30. HP tối đa +200/EN +50 (giá trị hiện tại được tăng lên), cơ thể `+0x17..+0x19` (đất/biển/không gian) = A (không thay đổi), khả năng di chuyển +10, giới hạn +10, số lượng cơ thể được thay đổi thành dạng S/H/B; GodGundam H cũng nhận được ô khả năng `0x1` (Shadow of God). `801FE96C` Thay đổi không-"-" của vũ khí đất/biển/yu thành A. `801FEB70` Chỉ dành cho 6 người đầu tiên: Sáu vật phẩm của người lái +10, địa hình của người lái đều là A và sức mạnh của 10 lần tiêu diệt đặc biệt (số vũ khí 0x0F–0x13, 0x1E, 0x35, 0x3E, 0x47, 0x4C) được **viết lại** dưới dạng sức mạnh tấn công cơ bản ROM + phần thưởng cấp độ (không tính số giai đoạn sửa đổi): 41–44 +100, 45–48 +200, 49–52 +350, 53–56 +500, 57–60 +700, 61–64 +900, 65–68 +1100, 69–72 +1400, 73–76 +1700, 77–79 +2000, **80 trở đi +2500** (`801FEC80..801FED64`). Berserker của Allenby chỉ có phần cơ thể. Ngoài ra còn có: Beast Fleet Sharo/Liang/Masato/Nin (0xA8–0xAB) và Silver Bell (0x9A) có sức mạnh ≥ 120. Chỉ đặt 30, không có giá trị gia tăng.

**Tiền thưởng quỹ bị giảm** `801F6588`: Tiền chỉ có nếu mục tiêu bị bắn hạ (máy bay mục tiêu `+0x1E`); Trại của kẻ tấn công 0, danh sách `+1 & 0x80` không được đặt, số lần hạ gục (thí điểm `+0x14`; cùng trường của đơn vị địch là số lượng bản sao, §4) ≥ 20 `资金 × D_80218908[min((击坠−20)/20, 9)] / 10` (Bảng 11…20, tức là ×1.1 ở 20–39…×2.0 từ 200, bị cắt bớt); rồi May mắn ×2 (căn chỉnh bất kỳ); cuối cùng được giữ ở mức 65.535 – giới hạn ở mức **trên mỗi đơn vị bị hỏng**. Kinh nghiệm `801F60D4` không có nhánh nào để đọc số lần tiêu diệt được.

## 8. Ý nghĩa của giao diện trước chiến tranh

Tất cả các đại lượng trên đều là **hàm thuần túy ở trạng thái có thể đọc được**. Giao diện trước chiến tranh có thể hiển thị chính xác mà không tốn số ngẫu nhiên - tiền đề là **tự tính toán lại công thức và không gọi trực tiếp hàm phán đoán**: `801F6C44` Lăn số ngẫu nhiên ngay khi vào cửa, bất kể mục tiêu có khả năng né tránh hay không. Sử dụng `80203418` để gây sát thương và `80204254` để đánh. Cả hai đều không tung ra đòn chí mạng và không di chuyển RNG.

Giao diện gốc chỉ đưa ra tỷ lệ trúng. Thông tin có thể được bổ sung: sát thương dự kiến ​​​​và sát thương chí mạng, tỷ lệ trúng đích chí mạng (phân biệt bạn/địch 4), xác suất phòng thủ phân thân/cắt/S, số lượng phân thân còn lại, sự khác biệt giữa ngưỡng khiên và khả năng xuyên giáp, lý do tại sao vũ khí không thể sử dụng được do không đủ sức mạnh cần thiết và tinh thần hiện đang hoạt động.

Bạn có thể tìm thấy bản phác thảo giao diện (theo bố cục bảng đôi ban đầu, nền và màu sắc chiến trường, bao gồm BẬT/TẮT hoạt ảnh chiến đấu và kết quả của ba lệnh cạnh nhau) trong tạo phẩm trong bản ghi phiên; khi triển khai, hướng thân nên sử dụng lại **nhóm gương đỉnh** ban đầu (`vertex_mode 0` 8 đỉnh mỗi phần, 4 đỉnh cuối cùng là nhóm gương đảo x, được chọn khi vẽ `+0x40`), nhấn bên Chỉ cần chọn nhóm, không cần nướng trước hai ảnh.

## Đính kèm: Bài viết này không đề cập đến

- Xác minh hoạt động của mục sức mạnh (cấp độ nhỏ đã sẵn sàng nhưng chưa được thực thi)
- Xác nhận hệ số kích thước/địa hình của mục công thức trúng theo từng mục
- `D_80219444[]` bảng con trỏ hàm theo id vũ khí (`801F8070`/`801F8618` lệnh gọi gián tiếp), có thể có các bản sửa lỗi bổ sung cho mỗi loại vũ khí
- Liệu các số ngẫu nhiên có được sử dụng trong quá trình biểu diễn hay không và liệu trình kích hoạt sự sụp đổ/kinh nghiệm/cốt truyện có bị bỏ lỡ hay không nếu màn biểu diễn bị buộc phải kết thúc (yêu cầu một trận chiến có hoạt ảnh được phát)

Trả về: [Sửa quy tắc tùy chọn](rule-fixes.md) · [Sửa lỗi cơ bản](base-fixes.md) · [Hoạt hình chiến đấu và đơn vị tùy chỉnh](../data/battle-animation.md) · [Chỉ mục tài liệu kỹ thuật](../README.md)