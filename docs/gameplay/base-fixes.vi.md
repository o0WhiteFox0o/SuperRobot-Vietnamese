> **Ngôn ngữ / Language:** [Tiếng Việt](base-fixes.vi.md) · [English](base-fixes.en.md) · [中文](base-fixes.md)

# Sửa chữa cơ bản: mặc định có hiệu lực, không cần chuyển đổi

Ngày: 2026-09-18. Đây là bản ghi về bản sửa lỗi ban đầu có hiệu lực theo mặc định: trò chơi không nhất quán với dữ liệu của chính nó và không có lối chơi gốc nào được thay đổi sau khi sửa, vì vậy nó không được tạo thành tùy chọn của người chơi. Những thay đổi yêu cầu người chơi quyết định điểm mạnh và điểm yếu của mình nằm trong [Sửa đổi quy tắc tùy chọn](rule-fixes.md) và manh mối ban đầu cho các báo cáo bên ngoài nằm trong [Đăng ký lỗi gốc](original-bug-register.md).

| ID | Sửa chữa | Thực hiện |
| --- | --- | --- |
| LỖI05 | Wu Fei và các phi công W khác không còn mang xác giả khi thù địch | Gói máy chủ `resident_func_800A5054` (`src/host/base_fixes.hpp`, `game_hooks.cpp`), có hiệu lực vô điều kiện |

Tiêu chí phán đoán: Hồ sơ triển khai ban đầu nêu rõ rằng các đơn vị này không có thi thể giả (bit hành vi 14 không được đặt và giá trị bổ sung là 0), nhưng mã bao gồm số lần tiêu diệt của chúng tôi do thiếu phán đoán của trại. Việc khôi phục về trạng thái mà bản thân bản ghi yêu cầu không yêu cầu người chơi lựa chọn và không thay đổi số lần cải trang ban đầu cho bất kỳ ông chủ nào.

## 1. BUG05: Khi Wu Fei thù địch, số lần giả mạo của anh ta bằng với số lần giết được bên phía chúng ta.

Các địa chỉ được phân phối dưới dạng mã cư trú (`800A…`, `8009…`) và lớp phủ chiến thuật (`801E…`–`8020…`).

**Cơ chế cơ thể giả nguyên bản**

- `801E0410` Khi đặt quân, vị trí danh sách của phe 1 và 2 (`8015E100 + 阵营×0x258 + 槽×0x14`) `+1` được đặt thành `0x80`; khi trại ban đầu của bản ghi triển khai khác 0 (bao gồm giá trị bản ghi 3 được đặt về phía chúng tôi), `8020B324`/`8020BE34` cũng sẽ được đặt. Nó có nghĩa là "điều khiển không phải của người chơi".
- Đối với loại đơn vị này, bản ghi trình điều khiển `+0x14` (u16) là số lượng bản sao**; trường tương tự dành cho các đơn vị của chúng tôi là số lần tiêu diệt, `801FB374` chỉ được thêm 1 (tối đa 999) khi trại 0 và danh sách không có `0x80`.
- Khi từ hành vi của bản ghi triển khai (28 byte) `+0x16` bit 14 được đặt và trại khác 0, `8020ABB4` ghi `+0x18` vào `+0x14`. Phiên bản gốc có tổng cộng 42 bản ghi như vậy, tất cả đều thuộc về ハマーン, シャア, シロッコ, グレミー, ミリアルド, ギュネイ, ガトー,ル・カイン. 2, 3, 5, 7.
- Lệnh giải quyết (`801F7204`): Đầu tiên nhấn tỷ lệ đánh `+0x12` trong bảng chiến đấu (kẹp 0–100) và 1–100 Nếu tung số ngẫu nhiên trúng, **chỉ đòn đánh lẽ ra trúng** mới kiểm tra khả năng phân thân (`801F6C44`), cắt り払い (`801F6D10`) và thân giả (`801F6E3C`) theo thứ tự. Điều kiện của cơ thể giả là trại không phải là 0, danh sách `0x80` được thiết lập và `+0x14 ≠ 0` được thiết lập. Khi được thiết lập, kết quả là `0x15`, đòn tấn công không hợp lệ và sau đó `801FCA78` (chiến đấu bình thường) hoặc `801FE068` (vũ khí bản đồ) giảm `+0x14` đi 1. Thời gian còn lại không được hiển thị trong trò chơi.

**lý do**

- Ngoài ra còn có bảng hạ gục lâu dài dành cho 5 thành viên dòng W `801614E0` (5 u16), với các chỉ số dưới 0 ヒイロ (ký tự 95), 1 デュオ (92), 2 トロワ (93), 3 カトル (89), 4 Wufei (91). `801FB374` được gọi sau khi thêm tiêu diệt vào bản ghi của chúng tôi. `800A4FBC` được thêm đồng bộ 1; `80091ED0`/`800920B4` được lưu và đọc bằng kho lưu trữ trung gian và `800A4F94` bị xóa trong trò chơi mới.
- `3D5A … 4000` Khi rời đội, `800AA62C` gọi `800A7E88` để xóa toàn bộ hồ sơ lái xe và `+0x14` được đặt lại về 0; khi đăng ký lại, `800A84F8` tạo một bản ghi mới và `800A5054` nâng `+0x14` trở lại giá trị trong bảng. Điều này được chuẩn bị cho việc "rời đội và tái gia nhập để giữ lại số lần tiêu diệt".
- Nhưng `800A84F8` sẽ gọi `800A5054` khi tạo một phi công có tên mới (số ký tự < 287) cho **bất kỳ phe phái nào**, trong khi `800A5054` chỉ nhìn vào số ký tự chứ không nhìn vào phe phái. Bản thân hai bản ghi kẻ thù của Wu Fei không có hình đại diện: "Trước trận chiến quyết định trong miền không gian" `00202a0c` (trại 1) và "Sự sống và cái chết trong tương lai" `00208568` (trại 2) có cả từ hành vi và giá trị cộng thêm là 0. Vì vậy, khi anh ta tạo bản ghi mới là kẻ thù, `+0x14` được viết là số lần tiêu diệt trước đó của bên ta và đơn vị địch đọc trường này là số hàng giả.
- Bản sao dự phòng sẽ không tăng thêm sau khi rời đội nên số lần phân thân bằng với số lần tiêu diệt cộng dồn cho đến khi rời đội (giới hạn trên là 999 chứ không phải cố định 21. Việc tiêu thụ avatar chỉ thay đổi thành tích của địch chứ không thay đổi bản dự phòng nên số lần tiêu diệt được sẽ khôi phục như bình thường khi hắn tái gia nhập (`3D5A 91,0,115,500`).
- Bốn người còn lại đi cùng con đường. Hino xuất hiện với tư cách là bên thứ ba (giá trị kỷ lục 4) trong "OZ Split Before", "Nana Nasana" và "Toro Assassination Order". Nếu trước đây anh ta bị phe chúng ta bắn hạ, anh ta cũng sẽ mặc xác giả. Liệu các cấp độ này có được xếp hạng sau khi anh ấy sa sút ở mỗi chặng hay không vẫn chưa được xác minh trong vòng này.

### Sửa

`800A5054` được thay đổi thành chỉ thực thi khi bản ghi trình điều khiển có trong bảng của chúng tôi (`80172F40`–`80174CEF`, 100 mục × 0x4C). Kỷ lục mới của địch và bên thứ 3 sẽ giữ nguyên giá trị khi triển khai (năm bay 0, boss vẫn ép số lần đã ghi), và hành vi rời đội rồi gia nhập lại để khôi phục số kill không thay đổi. Một người gọi khác của `800A5054`, `80210758` (đơn vị hiện tại được chuyển đổi sang phía chúng tôi), chỉ được gọi khi trại mục tiêu là 0 và con trỏ trong bảng của chúng tôi cũng được chuyển vào, điều này không bị ảnh hưởng.

## 2. Tái tạo và so sánh máy thật

Quá trình của phiên bản gốc kéo dài nhiều tập (Tham gia → Bắn hạ → Rời khỏi → Thù địch → Tham gia lại), vì vậy tôi đã tạo một cấp độ nhỏ nén nó thành một cấp độ [`wufei-dummy.json`](../../config/recomp/mini-stages/wufei-dummy.json), tập lệnh nhập `wufei-dummy-input.json`, chế độ chạy (Tiếng Nhật, Bản gốc, `--original-name-entry`, tắt tiếng, `SRW64_STATE_PROBE=1` và `SRW64_MINI_STAGE_CAPTURE=1`), 20.000 VI.

Cài đặt quy trình và so sánh cấp độ:

- Vòng 1: Wu Fei (アルトロンガンダム, cấp độ bù 60) đứng về phía chúng ta, với ba chiếc Dozer xung quanh anh ta; sau khi kết thúc lượt của chúng tôi, anh ta phản công và hạ gục ba đơn vị này trong giai đoạn của kẻ thù. Kaoru (cùng mức offset 60) đứng ở phía xa làm điểm neo của camera và cũng là người tấn công Wu Fei từ phía sau.
- Sự kiện vòng 2: `3D46 91,1` khiến anh ta nghỉ hưu, `3D5A 91,0,115,4000` xóa hồ sơ phi công và máy bay, sau đó sử dụng `3D45 2` để nhấn bản ghi "trước trận chiến quyết định trong miền không gian" của chính mình (trại 1, từ hành vi 0, giá trị bổ sung 0) Xuất hiện với tư cách là kẻ thù; trong cùng nhóm còn có bản ghi "アクシズのATTACK BEFORE" (từ hành động `0x4000`, giá trị bổ sung 3) của グレミー dưới dạng **so sánh giá trị thiết kế**.
- Giai đoạn địch sau khi kết thúc hiệp 2: Thực hiện đòn tấn công năm cánh của địch và tiến hành phản công.
- Sự kiện vòng 3: Sau khi đọc `3D5A 91,0,115,500`, yêu cầu anh ta tham gia lại, đọc lại và kiểm tra xem phần sửa chưa bị hủy "tham gia lại để giữ lại số lần tiêu diệt".

Mỗi điểm quan sát được cung cấp bằng ảnh chụp nhanh ranh giới lệnh sau `3D38`, ảnh này đọc vị trí danh sách (`8015E100`), phiên bản khung máy bay (`8016A210`) và phiên bản phi công (`80172F40`).

### Hai vòng so sánh (`wufei-dummy-original-5` và `wufei-dummy-fixed-1`, mỗi vòng 20.000 VI)

Khi việc chỉnh sửa vẫn là một công tắc tùy chọn, hai lần chạy được phân biệt bằng `SRW64_RULE_FIXES`; sau khi được đặt là sửa chữa cơ bản, công tắc đã được gỡ bỏ. Cột bên phải là hành vi hiện tại của mỗi lần chạy và cột bên trái là phiên bản gốc.

Hai vòng giống hệt nhau ngoại trừ công tắc này (nhật ký máy chủ in lần lượt là `SRW64_RULE_FIXES none` và `wing-kill-dummy`), cùng một tệp nhị phân, cùng một hình ảnh và cùng một tập lệnh đầu vào; chúng nhất quán từng khung hình cho đến khi việc chỉnh sửa có hiệu lực.

| Điểm quan sát (Ảnh chụp nhanh ranh giới lệnh) | Bản gốc | Đã sửa (hành vi mặc định hiện tại) |
| --- | --- | --- |
| Bắt đầu Hiệp 2: Số lần diệt được 5 con ruồi (bên ta) | VI 11817: +0x14=3 | VI 11817: +0x14=3 |
| `3D46 91,1` Sau khi thoát | VI 11905: Bản ghi vẫn còn đó, +0x14=3 | Tương tự như bên trái |
| Sau `3D5A 91,0,115,4000` | VI 11907: Hồ sơ lái xe biến mất | Tương tự như bên trái |
| `3D45 2` Sau khi xuất hiện theo hồ sơ kẻ thù của chính mình | VI 12273: **五飞 (trại 1) +0x14=3**; グレミー +0x14=3 | VI 12273: **五飞 (trại 1) +0x14=0**; グレミー +0x14=3 |
| Sau pha địch thứ hai (タケル phản công) | VI 15293: Wufei +0x14=**2**, HP vẫn là 5700/5700 | VI 15623: Wufei đã bị đánh bại, グレミー +0x14=3 không thay đổi |
| `3D5A 91,0,115,500` Sau khi tham gia lại | VI 15355: Năm người bay (Faction 0) +0x14=3 | VI 15685: Năm người bay (Faction 0) +0x14=3 |

- Ở phiên bản gốc, số lượng phân thân của Gofei địch chính xác bằng 3 lần tiêu diệt hắn khi ở bên ta, và hồ sơ triển khai của hắn không có vị trí phân thân; グレミー 3 lần đều đến từ chính bản ghi và hai nguồn xuất hiện cùng lúc ở cùng cấp độ.
- Cuộc phản công tương tự diễn ra trong cùng một khung trong hai hiệp (`present-7380.png`, VI 14754/14766): phiên bản gốc hiển thị "ダミー" màu xanh lá cây và năm HP bay không thay đổi; phiên bản sửa lỗi hiển thị "クリティカル 5700", HP trở về 0 và bị đánh bại. Đây chính là nguyên nhân trực tiếp khiến người chơi cảm thấy “không chơi nổi”.
- Sau hai lượt tái gia nhập, đội ta đã đạt được thành tích +0x14=3, chứng tỏ việc chỉnh sửa không ảnh hưởng đến mục đích ban đầu là "rời đội và tái gia nhập để giữ lại số mạng tiêu diệt".
- Còn ba vòng quy trình đang chạy: `original-2` sử dụng nhị phân trước khi thêm hook và vẫn chưa đạt đến cấp độ. `3D46` thoát khỏi màn chơi, nhưng điểm quan sát chung (bên ta bắn hạ 3 → địch tiến vào xác giả 3, グレミー3) Phù hợp với các hiệp tiếp theo; `original-3`/`original-4` (bao gồm móc, đóng quy tắc) và `original-5` giống nhau theo từng khung hình ở tất cả các điểm quan sát. Nói cách khác, việc thêm hàm bao bọc không làm thay đổi hành vi ban đầu. `original-3` cũng bộc lộ cạm bẫy của chính cấp độ nhỏ: trực tiếp `3D5A … 4000` đối với một đơn vị vẫn còn trên bản đồ sẽ để lại một vị trí danh sách lơ lửng và SIGBUS sau khi quay lại hoạt động, vì vậy cấp độ đầu tiên sử dụng `3D46` để thoát ra, xem [Cấp độ nhỏ](../script/mini-stage.md).

## 3. Không được che chắn

- Không có sự chạy thực tế ở các cấp độ ban đầu (Quân đội Độc lập "Trước trận chiến vũ trụ", OZ "Tương lai của sự sống và cái chết"), các cấp độ nhỏ chỉ đưa các hướng dẫn và hồ sơ tương tự vào một cấp độ; việc so sánh liên tục các số lần tiêu diệt khác nhau, sự khác biệt giữa hai tuyến đường và việc trả lại dữ liệu lưu sau khi tham gia lại vẫn chưa được thực hiện.
- Hiệu suất thực tế của bốn phi công W còn lại xuất hiện với tư cách là bên thứ ba chưa được kiểm tra; Người ta vẫn chưa xác minh được liệu ba hồ sơ về ヒイロ có được xếp hạng sau vụ tai nạn của anh ta hay không.
- Việc hiển thị số hình nộm còn lại (Roadmap QOL02) không liên quan gì đến việc chỉnh sửa này và không liên quan đến vòng này.

## 4. Thực hiện và xác minh

| Vị trí | Nội dung |
| --- | --- |
| `tools/recomp/toolchain/generate_cpu.py` | `NATIVE_HOOKS` Đổi tên cư dân `800A5054` thành `srw64_original_wing_kill_restore`; `make recomp-cpu` là bắt buộc sau khi thay đổi. |
| `src/host/base_fixes.hpp` | Bảng thử nghiệm của chúng tôi có phạm vi `player_pilot` và cơ sở cho việc khắc phục này. |
| `src/host/game_hooks.cpp` | `resident_func_800A5054`: Trả về trực tiếp khi bản ghi không có trong bảng của chúng tôi mà không cần kiểm tra bất kỳ chuyển đổi quy tắc nào. |
| `config/recomp/mini-stages/wufei-dummy.json` | Để tái tạo cấp độ, xem §2. `tools/recomp/gameplay/wing_kill_save.py` cũng cung cấp một phương pháp có kiểm soát để ghi đè bản sao lưu sự cố trong kho lưu trữ và tính toán lại tổng kiểm tra, phương pháp này chỉ hiệu quả đối với các kho lưu trữ mà trò chơi thực sự đọc. |

- `make recomp-base-fixes-test` (được sáp nhập vào `recomp-native-check`): Xác định ranh giới của phạm vi bảng thí điểm của chúng tôi.
- `tests/test_wing_kill_dummy.py`: Hook được đổi tên, hàm bao bọc có hiệu lực vô điều kiện và không tham chiếu đến thư mục quy tắc. Mục này không còn trong các quy tắc tùy chọn và bản sao menu bằng ba ngôn ngữ; Sự kiện ROM của BUG05 (bảng dự phòng ghi cùng lúc khi bắn hạ, điểm gọi `800A84F8`, `800A5054` số ký tự chỉ đọc, bảng nhảy từ ký tự sang chỉ số dự phòng và phán đoán bút danh `+0x14`, cài đặt danh sách `0x80`, từ hành vi của hai bản ghi địch là 0); và xử lý tổng kiểm tra của công cụ lưu trữ.