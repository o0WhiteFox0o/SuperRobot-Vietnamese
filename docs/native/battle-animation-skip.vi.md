> **Ngôn ngữ / Language:** [Tiếng Việt](battle-animation-skip.vi.md) · [English](battle-animation-skip.en.md) · [中文](battle-animation-skip.md)

# Thoát khỏi màn trình diễn chiến đấu (nhấn X)

2026-09-25. Sau khi vào trận bấm **X** (Bàn phím được bật theo mặc định và không có cài đặt.

Được triển khai trong [`battle_animation_probe.hpp`](../../src/host/battle_animation_probe.hpp), được treo trong `load_00121560_func_801C9710` (hiển thị vòng lặp chính) và `load_000AB160_func_801DFBD0` (bộ điều phối bản đồ trên mỗi khung). Địa chỉ đến từ phân tích tĩnh và xác minh máy thực và bản ghi đang chạy nằm trong `build/recomp/debug/`.

**26-09-2026: Cả hai phần đều đã được hoàn thiện và xác minh trên máy thật** - Sau khi hủy và quay lại bản đồ, bản đồ tuân theo quy trình ban đầu là "tắt hoạt ảnh" để tính sát thương, rút số và thanh HP, trừ máu và trao phần thưởng. Để biết phương pháp, hãy xem [Quay lại nhánh hoạt ảnh gốc](#交还给原版的关动画分支).

## Đã thực hiện: Hủy bỏ

Máy trạng thái hiệu suất ở `D_80250000` và vòng lặp chính ở `801C9710`. Khi nhấn X:

1. Byte trạng thái được ghi vào 21 (trạng thái kết thúc) và số khung `D_8025020C` bị xóa.
2. Gửi trực tiếp yêu cầu mờ dần `80099814(5, 1, 2)` cho yêu cầu đó và đặt `D_80250205` thành 1 để tránh gửi lại trạng thái 21.
3. Trạng thái 0..20 đều được chấp nhận, vì vậy bạn có thể nhấn nó trong khung đầu tiên của trận chiến; trạng thái 21 trở lên bị loại trừ và phần kết đã mờ dần.

**Không thể sử dụng chức năng hủy bỏ Z+Start ban đầu**. Đường dẫn đó được đặt thành `D_80225810`, nhánh của `801C97E4` sẽ được điều chỉnh thành `800A5138` và sau đó chọn chế độ trò chơi 7 hoặc 0x11 - là lộ trình đặt lại tiêu đề/đặt lại. Trong thử nghiệm thực tế, cấp độ được đưa thẳng trở lại màn hình tiêu đề (`build/recomp/debug/20260925T023507.767082Z`). Ngữ nghĩa của nó là "thoát khỏi cấp độ chiến đấu này" chứ không phải "bỏ qua hoạt ảnh này".

Trạng thái 21 ban đầu phải đợi cho đến khi `801C9DD0` báo cáo rằng ống kính ổn định và số khung hình vượt quá 10 (`slti 0xA` của `801C813C`) trước khi tự mờ dần. Thời gian kết thúc đo được thực tế là 7,8–8,8 giây. Vì người chơi đã bày tỏ không muốn xem nên cứ gửi trực tiếp.

**TẠI SAO AN TOÀN**: Quá trình dọn dẹp thực sự phức tạp (`8008B950` giải phóng tất cả 300 vị trí sprite, `8008DB2C`, `8008AC78(4)`) chạy phân đoạn kết thúc được chia sẻ **sau** mờ dần trong `801C9710`, không ở trạng thái bị bỏ qua.

**Không có chức năng "nhảy để phản công"**. Đẩy máy trạng thái về phía trước (4 → 10) và nó trông ngay trên rãnh trạng thái. Hình ảnh rất tệ: trạng thái 3..9 là nơi tải các dòng sprite, atlas và trình điều khiển cho vòng này. Trạng thái 9 (`801C7960`) cũng cần tiến hành dọn dẹp riêng, trong khi trạng thái 10 (`801C7BC0`) chỉ di chuyển camera. Sau khi bỏ qua, bên phản công không xuất hiện và các hộp thoại được xếp chồng lên nhau. Bị bỏ rơi.

## Hai đường dẫn của phiên bản gốc

Phần này sửa lại tuyên bố trước đó trong bài viết này ("Thiệt hại được tính từ trạng thái phụ 2 của chuỗi 0x4B"). Tiểu bang 2 là bước "vòng tiếp theo". Việc đọc bảng của vòng trước được dùng làm đầu vào chứ không phải đầu vào; thiệt hại thực sự được giải quyết trước khi biểu diễn.

**Trạng thái 24 (`801D6534`) là toàn bộ quá trình tấn công**, bảng trạng thái phụ `D_80217CC4`:

| tiểu bang | Chức năng | Hiệu ứng |
| --- | --- | --- |
| 0 | `801D4794` | Tạo bàn chiến đấu `8018B6E8` (kích thước bước `0x5C`: +0 tay cầm, +4 bản ghi đơn vị, +8 vũ khí, +0x14 sát thương gây ra, +0x26 mã phản ứng) |
| 1 | `801D5064` | Trang xác nhận cuộc tấn công của chúng tôi (`battle_confirm_step` của máy chủ) |
| 2/3 | `801D5294` / `801D5404` | **Giải quyết `801F7D6C`**: Số lần đánh/sát thương đều được tính và ghi vào bảng chiến đấu; khi địch tấn công, 2 là trang phản ứng của người phòng thủ |
| 8 | `801D5898` | `801DF96C`: `D_801602FA = 4`, trạng thái chuyển thành `0x4F` (không tải), bộ phân phối khung tiếp theo sẽ điều chỉnh `801D4E6C` |
| 4 | `801D5498` | **Điểm hạ cánh sau khi bật hoạt ảnh**: `801FCA78` Âm thầm áp dụng kết quả rồi 9 |
| 9 | `801D5E88` | `801FC160` Gửi khung kinh nghiệm và quỹ |

**Nĩa `801D4E6C`** Đầu tiên điều chỉnh `801FC994` (chỉ cần hỏi "Người phòng thủ có bị bắn hạ không", không thay đổi gì cả), sau đó nhìn vào công tắc `8015DDA8 & 4` (đặt = tắt hoạt ảnh):

```
动画开：80080188(2) 装战斗 overlay，80099814(5,1,2) 淡出。
        战斗 overlay 是纯演出，读 801F3578 填好的演出方块 800F97E0，从不写名册。
        回来时 801C7168（D_8022722C==1）把地图放回状态 24 子状态 4：
          801FCA78 → 801FB460：开关位清零 → 把 HP 直接写进名册、不排回合
                   → 801FC83C 扣 EN／弹药、气力 +5、清精神位
          然后子状态 9 发奖励。玩家看不到任何数字——动画已经演过了。
动画关：D_80228528 = 0；8009DB8C()；
        （D_8022796C==1 时：8008B888(0x9C) 释放，镜头对准守方格，801CBEB8）
        同一个 801FCA78 → 801FB460：开关位置位 → 不动名册，
                   把每一回合排进表：D_802277E8 回合数、D_802277E9[] 目标句柄、D_80227862[] 伤害
        回合数为 0 → 801C29DC(D_80172EE4) + 801C8AB4；否则 D_80172EB0 = 0x4B、D_80172EB2 = 3
        D_8022731C = 0、D_8021F464 = 0；最后给两个参战单位打「已行动」位 0x40
```

**Trạng thái 0x4B (`801D92B0`) chỉ là biểu diễn**, bảng trạng thái phụ `D_80217D4C`: 3 lấy mục tiêu và sát thương của vòng này, 4 đợi 20 khung để tạo hiệu ứng trúng đòn `801E3AE4`, 5 trừ HP khỏi đội hình theo từng khung và sử dụng `801FCC6C` để gieo số, 6 số trôi nổi, 7..10 Lượt tiếp theo hoặc kết thúc - kết thúc là quay trở lại ** trạng thái 24 trạng thái phụ 9**, nơi nó hợp nhất với đường dẫn của hoạt ảnh.

Vì vậy, sự khác biệt giữa hai đường dẫn chỉ là một nhánh của `801FB460`: vị trí chuyển đổi xác định nên "ghi danh sách ngay lập tức" hay "sắp xếp các vòng và để chuỗi 0x4B bị trừ từ từ".

## Quay lại nhánh hoạt hình gốc của Guan

Sau khi nhấn X để hủy, bản đồ sẽ vẫn ở trạng thái 24 trạng thái con 4 khi quay trở lại. Máy chủ nhìn thấy `D_80172EB0 == 24 && D_80172EB2 == 4` trong móc điều phối (trước `801DFBD0`) và cần hiển thị kết quả, do đó, nó thay thế trạng thái phụ 4 và chạy nhánh hoạt ảnh phân nhánh (`801D4E6C` từ `.L801D4EE0`, `replay_animation_off`):

1. `D_80228528 = 0`, `8009DB8C()`
2. Viết lại `D_8022796C` và `D_80227250/54` được ghi trong khung rẽ nhánh (chúng nằm trong khu vực được bao phủ bởi lớp phủ chiến đấu; khung rẽ nhánh là khung mà nhà phân phối nhìn thấy `D_801602FA == 4` và bit chuyển đổi bị xóa. Móc chạy trước nhà phân phối và chỉ có thể đọc được)
3. Đặt tạm thời bit 4 của `8015DDA8`, điều chỉnh `801FCA78`, sau đó khôi phục nó - chỉ `801FB460` đọc bit này, bit này sẽ xác định nên lên lịch vòng thi hay viết danh sách
4. Số vòng là 0, đi `801C29DC` + `801C8AB4`, nếu không thì trạng thái là 0x4B trạng thái phụ 3; xóa `D_8022731C`, `D_8021F464`

Không cần nhập thông tin: bàn chiến đấu, danh sách và `D_80172EE2` đều nằm dưới lớp phủ. Lớp phủ trận chiến chỉ đọc bảng chiến đấu (`80221B5C` ở một nơi); danh sách HP vẫn có giá trị trước chiến tranh vì trạng thái phụ 4 chưa chạy; `801FC994` và vị trí được thực hiện đã được thực hiện khi phân nhánh nên không có sự trùng lặp. Sau đó, chuỗi 0x4B sẽ tự tính toán, thực hiện và khóa. Nhịp điệu, hiệu ứng âm thanh và xử lý tràn sự cố đều nguyên bản. Kết thúc như thường lệ với 9 vòng thưởng.

**RNG**: `801FCA78` ban đầu sẽ chạy ở trạng thái phụ 4 và sẽ không có phát lại bổ sung; phần còn lại là hiệu suất của chuỗi 0x4B, phù hợp với hoạt ảnh tắt.

**Kết quả máy thật** (`build/recomp/debug/20260926T014604.081648Z`, địch ムゲ兵 3000, tấn công ミニフォー 2800, trạng thái 3 nhấn X):

```
replay-animation-off  hp_before [3000, 2800]  rounds [{target 98, damage 1029}]
chain-done            hp_after  [1971, 2800]
ui-text.jsonl         " -1029" 逐位浮现，map_state 75 sub 6
```

`anim-abort-t4.png` là cảnh hoạt ảnh: bên cạnh đơn vị bị tấn công, `-1029` viền dòng chữ màu trắng và thanh HP khung màu xanh lam; `t5` là trang phản hồi cho trò chơi tiếp theo. 3000→1971 phù hợp với đường cơ sở của toàn bộ chương trình.

Hai tình huống còn lại cũng được thông qua (ô 0 trong bảng chiến đấu là quân tấn công, ô 1 là quân phòng thủ):

| Tình huống | Chạy | Vòng | Danh sách |
| --- | --- | --- | --- |
| Trạng thái đợt tấn công, phản công của địch 12 Nhấn X | `20260926T015443.874339Z` | `{98, 1544}` | 3000→1456 |
| Cuộc tấn công của chúng tôi (`--player`), trạng thái 3 nhấn X | `20260926T020357.464905Z` | `{98, 1609}` | 3000→1391 |

### Đã thực hiện đường vòng

- **Máy chủ tự rút số** (`801FCC6C` + `801FCF00` mỗi khung) có thể rút và `-200` đo được xuất hiện bình thường. Nhưng không có giá trị thiệt hại nào vào thời điểm đó - danh sách vẫn là HP trước chiến tranh và "Performance Cube − Roster" không phải là thiệt hại; và các vị trí trong bảng chiến đấu được coi là chỉ số dưới của khối hiệu suất và phép đo thực tế cho thấy `hp=3000/2800` (thanh máu cực dài vượt quá giới hạn trên).
- **Nhập chuỗi 0x4B từ trạng thái phụ 0** bị lỗi ba lần liên tiếp: `D_802284DC` con trỏ null (`801FCA78` là trình ghi duy nhất thông qua `801FC110/801FC45C`), `D_802277E9[0]` bị xóa về 0 và mã điều khiển hợp pháp bắt đầu từ `0x42`, `801FB8B4` Tham số con trỏ là giá trị hoang dã. Nguyên nhân sâu xa là trạng thái phụ 2 không phải là mục nhập - đó là "lượt tiếp theo", đọc bảng của lượt trước. Mục nhập đúng chính là nhánh nhánh: `801FCA78` rồi nhập trực tiếp vào trạng thái phụ 3.
- **Điền `D_80228530` sáu ô theo cách thủ công** Không thể vẽ bất cứ thứ gì: `80209900` chỉ được tham chiếu một lần trong toàn bộ lớp phủ bản đồ, đó là `801FCC6C`. Cuối cùng, nó được đăng ký thành `8008B4F4` khi sprite được gọi lại.
- Giá trị trả về của **`801FCF00` là nghịch đảo**: 1 chỉ được trả về sau khi cả sáu ô đều đạt trạng thái 3, khác 0 = **Kết thúc**.
- **Kích thước bước của bảng tọa độ lưới là `0xC4`** (được lập chỉ mục bằng bộ điều khiển), không phải `0x34`.
- **`8008B888(id)` được giải phóng, chưa được tải**: Chỉ khi `D_800FFA71[id]` khác 0 thì ba vị trí mới được giải phóng và `8008198C` được điều chỉnh. `8008B888(0x9C)` trong ngã ba nhằm mục đích tiêu diệt các yêu tinh trong giai đoạn nhắm mục tiêu.

## Xác minh

[`check_battle_animation.py`](../../tools/recomp/debug/check_battle_animation.py), cấp độ nhỏ `config/recomp/mini-stages/battle-ui.json`:

```bash
SRW64_BATTLE_ANIMATION_PROBE=1 .venv/bin/python tools/recomp/debug/check_battle_animation.py --mode abort --at 3
```

- Theo mặc định, pha kết thúc trong khoảng trống, cho phép kẻ địch tấn công và xác nhận trên trang phản hồi; `--player` được thay đổi thành đòn tấn công chủ động của chúng tôi (Menu Đơn vị → Tấn công → Vũ khí đầu tiên → Mục tiêu đầu tiên), bao trùm một người gọi fork khác
- `--mode baseline` ghi lại chuỗi trạng thái mà không cần nhấn nút; `--no-anim` ghi lại hiệu suất của bản đồ khi ghi lại hoạt ảnh cấp độ để so sánh.
- `--pad` sử dụng tay cầm R2 thay vì bàn phím
- Khẳng định: `jumped-to-winddown`, `replayed-animation-off` (khung mà hook chiếm trạng thái phụ 4), `rounds-queued`, `roster-untouched-by-animation` (HP danh sách khi fork giống như khi chơi lại), `chain-done`, **`hp-settled-like-animation-off`** (HP cuối cùng của mỗi đơn vị tham gia = HP trước trận − Thiệt hại được đưa vào bảng, được kẹp bằng 0), `damage-redrawn` (các số thực sự xuất hiện trong `ui-text.jsonl`)
- Khi thoát script sẽ luôn là `Session.quit()`; điều kiện chính là `state >= --at` thay vì bằng nhau, vì việc thăm dò tệp theo dõi sẽ chạy đua với máy trạng thái

## Không thể nhấn và giữ X trước

X là "Hủy" trên trang xác nhận trước trận chiến (`battle_page.cpp` ánh xạ trở lại `0x4000`). Nhấn và giữ nó để xác nhận sẽ ngăn trận chiến bắt đầu. Đây là xung đột ngữ nghĩa, không phải lỗi.