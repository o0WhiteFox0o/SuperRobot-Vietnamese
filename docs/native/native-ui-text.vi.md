> **Ngôn ngữ / Language:** [Tiếng Việt](native-ui-text.vi.md) · [English](native-ui-text.en.md) · [中文](native-ui-text.md)

# Văn bản giao diện gốc: hiển thị gốc độ phân giải cao và đa ngôn ngữ

Ngày: 25-09-2026. Không có giao diện gốc cho các trang gốc, bao gồm bản đồ chiến thuật, màn hình chiến đấu và nhiều cửa sổ bật lên khác nhau. Ban đầu họ sử dụng phông chữ 14 pixel của ROM để vẽ ký tự, giao diện tiếng Trung và tiếng Anh vẫn bằng tiếng Nhật. Bây giờ được máy chủ vẽ lại trong HarmonyOS Sans tại chỗ và hiển thị bằng ngôn ngữ đọc. Bố cục, luồng, con trỏ và màu sắc phù hợp của phiên bản gốc không thay đổi và logic trò chơi không bị ảnh hưởng. Các màn hình đã có trang gốc (giữa các trò chơi, menu tiêu đề, xác nhận trước trận chiến, trang tên) sẽ không đi qua đây.

- **Công cụ văn bản**: Các nhãn một dòng, cửa sổ văn bản và nhóm số đều được tiếp quản, xem §2.
- **HUD chiến đấu**: Huy hiệu Phản công/Phòng thủ/Hồi phục và biểu ngữ kỹ năng được thay đổi thành văn bản gốc và đường viền HUD được vẽ lại thành các lát có độ phân giải cao theo thiết kế ban đầu, xem §3.
- **Đường viền cửa sổ và tam giác lật trang**: Hình ảnh số màu độ phân giải cao được thêm vào bảng khung và các đường khung nhấp nháy như bình thường, xem §4; để biết số lượng thiệt hại của các trận chiến trên bản đồ, xem §5; đối với những việc chưa được thực hiện, hãy xem §7.

## 1. Cách vẽ ký tự ở phiên bản gốc (phân tích tĩnh)

Tất cả văn bản gốc đều đi qua công cụ văn bản thường trú, được vẽ thành hai lần trên mỗi khung. Cơ sở là việc tháo rời `8008DC40`, `8008EB5C`, tọa độ đều là 320×240.

| Bể bơi | Vị trí | Kỷ lục | Vẽ bởi Ai |
| --- | --- | --- | --- |
| Nhãn dòng đơn | `8015CB00`, 60 vị trí, 0x34 byte mỗi vị trí | Số bản ghi văn bản +0 (văn bản in là 0); +2 loại (1 rút thăm ở chuyến A, 2 rút thăm chuyến B, 3 rút thăm cả hai lượt); +3 số bảng màu; +4/+8 là x/y; +0xC bắt đầu bằng mã glyph và kết thúc bằng 0xFFFF. Hàm tìm nạp từ `8008CF14` không kiểm tra độ dài, nhãn dài sẽ ghi vào ô tiếp theo | Chuyến đi `8008DC40` (cấp 0x8A), chuyến đi B `8008EB5C` (cấp 0x86, được vẽ trên cửa sổ bật lên) |
| văn bản | `800FBAB0`, 2 vị trí, 0x218 byte mỗi vị trí | Đối thoại, mục đích chiến đấu, lựa chọn tay chân. +0x214 là số trang, +0x215 là trang hiện tại; vẽ trang hiện tại, khoảng cách dòng 16 | Một chuyến đi được rút ra đầu tiên |
| Số | `801613E0`, 20 vị trí, 8 byte mỗi vị trí | Loại, giá trị, x, y. Mỗi khung hình được định dạng lại bằng sprintf (`+%d`, `-%d`, `%5d`, `?????`, `%3d`), glyph được lấy từ lưới tài nguyên 8×8 1159 | Loại 1–6 ở pass A, 7 trở lên ở pass B |

**Hiển thị danh sách**:
- Mỗi bản ghi được tải bằng bảng màu trước: `FD10` Thêm 5 lệnh và tải dữ liệu tương ứng với tay cầm bảng `D_80178B52[色号]`.
- 11 lệnh cho mỗi hình tượng không phải dấu cách, kết thúc bằng `F2 F2 E4 E1 F1`: hình tượng 8×14 (hẹp) hoặc 14×14 (rộng), 1:1.
- Nhóm số chỉ chứa toàn bộ bảng màu một lần và mỗi ký tự (bao gồm cả dấu cách) chiếm một hình chữ nhật 8 × 8.
- Đầu ra hoàn toàn xác định và nội dung nhóm không thay đổi khi hàm trả về lần đầu tiên, do đó máy chủ có thể ánh xạ từng hình chữ nhật trở lại vị trí nhóm tương ứng.

**Màu sắc**: Chỉ có màu số 1 của font là chữ, còn màu số 2-10 là khử răng cưa về phía nền tối, không nét. Tám bảng màu là: tài nguyên 2 trắng, 3 đỏ, 4 xám (không có), 8, 7, 5 vàng, 6 xanh, 1160.

## 2. Phương thức tiếp quản

Mã nguồn: [`ui_text.cpp`](../../src/host/ui_text.cpp), vẽ `place_texts` của trình kết xuất sprite cảnh được sử dụng lại [`native_sprite.cpp`](../../src/host/native_sprite.cpp) và văn bản được rasterized trong [`sprite_text.cpp`](../../src/host/sprite_text.cpp).

- **Móc**:
- Trình bao bọc cho `8008DC40` gọi `ui_text_drawn(..., false)` sau mô-đun hội thoại.
- `8008EB5C` được đổi tên thành `srw64_original_text_front_draw` trong `NATIVE_HOOKS` của `generate_cpu.py` và được gọi là `ui_text_drawn(..., true)` sau khi đóng gói.
- **KIỂM TRA**:
- Đọc lại nhóm theo thứ tự công cụ mỗi lần (văn bản → thẻ theo số vị trí → số) và kiểm tra từng cái một với danh sách hiển thị: số lượng bản ghi, địa chỉ bảng màu của từng mục cũng như số lượng glyph và vị trí ký tự đầu tiên được tính cho mỗi thẻ theo "hẹp 8, rộng 14, khoảng cách 8, dòng mới + 14".
- Nếu có phần nào không khớp, hãy giữ nguyên toàn bộ chuyến đi và ghi lại vào `ui-text.jsonl`.
- **Bản vẽ gốc trong một lần**:
- Tất cả các hình chữ nhật glyph đã chiếm sẽ bị xóa, chỉ để lại hình đầu tiên làm dấu và hình trước đó `F2` được thay thế bằng nhãn.
- RT64 gọi lại máy chủ tại điểm đánh dấu và máy chủ vẽ tất cả văn bản cho chuyến đi này trong cùng một lượt hiển thị. Thứ tự vẽ giống như phiên bản gốc và các cửa sổ bật lên, chuyển tiếp và dư ảnh vẫn được che phủ ở trên cùng.
- **Dịch**:
- Khi nhãn vẫn hiển thị tiếng Nhật của bản ghi thì sử dụng bản dịch trong thư mục ngôn ngữ và quy tắc giống như người nói của đoạn hội thoại (`dialogue::label_text`).
- Tên do người chơi nhập và văn bản in (bản ghi số 0) được vẽ ở độ phân giải cao.
- Thay lưới/bắn/P/B/MAP trước và sau tên danh sách vũ khí bằng biểu tượng gốc ở phông chữ ký hiệu (cỡ chữ U+E000+).
- Hình tượng biểu tượng không có tên trong bảng hình tượng (dấu hiệu máy bay và biểu tượng bản đồ trong bảng đơn vị) vẫn giữ nguyên hình ảnh ban đầu của chúng.
- **Vị trí**:
- Nhãn (number, sprintf) có bản ghi số 0 được vẽ theo từng lưới, mỗi ký tự được căn giữa ở lưới ban đầu nên việc căn chỉnh cột không thay đổi.
- Ngoại lệ là các lưới liên tục có phông chữ không vừa: ROM Kana có chiều rộng một nửa là 8 pixel và phông chữ có chiều rộng tối đa. Mỗi từ trong lời bài hát của カラオケ đều có nhãn (khoảng cách giữa các ký tự tiếng Trung là 16 và kana là 8) và các từ có thể được chồng lên nhau trong các bản vẽ theo từng khung hình (được phát hiện bởi người dùng 2026-09-25). Các lưới liền kề (cách nhau ít hơn 8 pixel) được kết nối thành một phần. Khi tổng chiều rộng phông chữ vượt quá chiều rộng ban đầu của phần này thì chiều rộng của phần này được chia theo độ rộng phông chữ của mỗi từ. Các từ trong cùng một phần được thu hẹp đồng đều và cỡ chữ không thay đổi; mỗi từ vẫn sử dụng màu nhãn riêng nên lời bài hát đổi màu như bình thường. Các đoạn văn cách nhau bởi dấu cách sẽ được xử lý riêng biệt; chỉ có thể đặt các đoạn văn có số và chữ cái và chúng vẫn được vẽ từng đoạn một.
- Các nhãn khác căn trái tại nhãn gốc. Hai hoặc nhiều khoảng trắng liên tiếp trong văn bản gốc là khoảng trắng dành riêng cho số: mỗi đoạn văn bản được đưa về điểm bắt đầu của đoạn văn gốc.
- Khi thứ tự từ của bản dịch khác nhau (ví dụ: “Thao tác đã kết thúc”), di chuyển số rút ra ở chỗ trống vào câu đã dịch và ghép cả câu lại với nhau: Còn 4 máy chưa hoàn thành thao tác.
- **Chiều rộng**:
- Mỗi đoạn văn bản có thể sử dụng 4 pixel trước phần tiếp theo trên cùng một dòng (các nhãn khác, số, mục nhập nhóm số).
- Văn bản (tiếng Nhật) hiển thị nguyên gốc không vượt quá chiều rộng ban đầu vì kana của ROM có chiều rộng bằng một nửa. Bản dịch có thể được sử dụng thêm khoảng 35% khi không có gì đằng sau nó.
- Khi vượt quá giới hạn, trước tiên hãy nén theo chiều ngang: tối đa 70% đối với tiếng Trung và tiếng Nhật, và 80% đối với tiếng Anh. Nếu chưa đủ, hãy giảm cỡ chữ, tối đa 1,5 điểm. Do đó, kích thước phông chữ trong cùng một ngôn ngữ vẫn nhất quán.
- **Cỡ chữ**: Tiếng Trung và tiếng Nhật 12.5, tiếng Anh 12 (dùng dạng rút gọn trước); các số và chữ cái được vẽ bởi lưới sử dụng SC có độ rộng thông thường trong tất cả các ngôn ngữ.
- **Cửa sổ văn bản**: Hộp thoại được mô-đun hội thoại vẽ ra và không được chạm vào đây. Sau khi rút hết văn bản trên trang hiện tại (chẳng hạn như văn bản bên ngoài hộp thoại (thành phần, văn bản lựa chọn)) và các từ khác trên trang hiện tại, hãy vẽ toàn bộ trang với khoảng cách dòng là 16 và chiều rộng là dòng dài nhất của văn bản gốc.
- **Nhóm số**:
- Sau khi định dạng theo kiểu, vẽ từng lưới, giữ nguyên lưới ban đầu.
- Hai bộ ký hiệu lần lượt tương ứng với “chữ trắng viền đen” ban đầu (loại 1, 2, 7 và 8) và “chữ trắng viền đen”.
- **Khi nào nó có hiệu lực**:
- Hợp lệ khi mô-đun hội thoại được cấu hình. Khi tắt chế độ ảnh gốc Nhật Bản cộng với ảnh gốc, đó là ảnh gốc. Các ngôn ngữ khác vẫn sẽ được dịch ở chế độ hình ảnh gốc, phù hợp với quy ước kiểm kê nội dung HD.
- Khi chọn "Bản gốc" trên giao diện xác nhận trước chiến tranh (`battle_ui` là `original`), màn hình đó được xử lý ở chế độ ảnh gốc: tiếng Trung và tiếng Anh được dịch như bình thường, còn tiếng Nhật là ký tự ROM gốc; khung cửa sổ 1196/1197 của nó cũng sử dụng hình ảnh gốc. Xem [Giao diện người dùng xác nhận trước trận chiến](native-battle-ui.md#三种界面2026-09-27).
- Có thể tắt `SRW64_NATIVE_UI_TEXT=0` trong toàn bộ quá trình chạy.

**Ảnh chụp nhanh**: `status.ui_text` chứa:
- Đếm: `passes`, `drawn`, `mismatched`, `labels`, `translated`, `glyphs`, `numbers`, `reader_owned`, `items_placed`, `items_waiting`.
- Nội dung của 2 chuyến đi gần nhất: `back`/`front`, mỗi mục là một nhãn (`slot`, `record`, `x`, __INL _CODE_49__, `text`, `translated`, `consumed`), văn bản (`body`), hoặc số (`number`).

## 3. HUD chiến đấu

**Huy hiệu và Biểu ngữ kỹ năng**: Cảnh Chế độ 9 (được vẽ bởi `800945D4`, Atlas 1159, Palette 1160). Trước tiên hãy điều chỉnh `sprites::rewrite_grid` trong `map_drawn` của `host.cpp`. Sau khi nhận ra số cảnh, nó sẽ xóa lưới ban đầu và vẽ văn bản gốc vào cùng một vị trí.

| Cảnh | Bản gốc | Hiển thị |
| --- | --- | --- |
| 1142–1149, 1152, 1153, 1157 | Tôi là ai? ,真ッハスペシャル, bản sao, ゲッタービジョン, chân ma tức thì, ハイパージャマー| Dịch hồ sơ tên khả năng 1020, 1019, 1026, 1022, 1021, 1024, 1025, 1023, 1100, 1101, 1116 |
| 1150, 1151 | シールド Phòng thủ, クリティカル | Thẻ giao diện `hud_shield_defense`, `hud_critical` |
| 1154–1156 | Huy hiệu phản công, phòng thủ, trả lại | `hud_counter`/`hud_defend`/`hud_evade`: Phản/ngăn chặn/né tránh tiếng Trung (từ "return" không giống tránh né trong tiếng Trung), tiếng Anh CTR/DEF/EVA |

Biểu ngữ có nền màu xanh đậm với các ký tự chuyển màu xanh lục; huy hiệu có nền màu xanh lam với các ký tự màu vàng trong khung màu vàng, 16×16.

**Biên giới HUD** (Cảnh 1193): Hai bảng 288×32 HP/EN bao gồm 19 lát từ Tài nguyên 1296, Bảng màu 1301. Hộp thoại cũng sử dụng dải này ([Dialog HD Border](native-dialogue-runtime-hd.md)), trong đó các lát thẳng trên và dưới (nguồn x 48, 208) được chia sẻ trên cả hai mặt và vẫn được vẽ bằng công cụ hộp thoại. 17 hình còn lại được vẽ lại bởi [`hud_frame_asset.py`](../../tools/hd_ai/hud_frame_asset.py):

- Vị trí của dải băng được hiển thị trong ROM và màu sắc giống nhau khi vẽ lại bằng khung hội thoại: sáng ở trên và bên trái, tối ở dưới và phải và một đường màu xanh đậm ở phần trong cùng. Nhấn 4x để phóng to và giữ độ sắc nét.
- Thanh đèn xanh được sơn giống thanh đèn thủy tinh giống khung hội thoại.
- HP／EN sử dụng HarmonyOS Sans Bold, các ký tự màu vàng trong ROM được làm đậm bằng bóng màu vàng; các dấu gạch chéo được vẽ dưới dạng các đường thẳng khử răng cưa.
- Cắt từng lát theo vị trí của nó trong HUD, ghi vào `worldmap-surfaces/pack-v2` và thay thế bằng RT64 bằng hàm băm kết cấu. `--art` sẽ đăng ký họ vào `content/art/stage1-hd.json`.

```sh
PYTHONPATH=src:. .venv/bin/python -B tools/hd_ai/hud_frame_asset.py \
  --pack assets/hd-ai/worldmap-surfaces/pack-v2 --output build/hd-ai/hud-frame \
  --art content/art/stage1-hd.json
```

## 4. Viền cửa sổ

Đường viền của cửa sổ gốc là cảnh lưới chế độ 9 (được vẽ bởi `800945D4`): lưới phân đoạn đường 16×16 của tập bản đồ 1295, một số được lật theo chiều ngang, được chỉ định bởi bảng bố cục `D_800C8BB8` hoặc được xác định bởi lớp phủ chiến thuật được chọn trong thời gian chạy (1165, 1172, 1173, 1014 và số dòng menu) 1198, 1199, v.v.). Hình tam giác màu đỏ khi lật trang là cảnh tương tự như Album 1302. Một số bảng màu đang quay vòng (1016–1019, 1304) và các đường viền sẽ nhấp nháy, do đó, việc thay thế RT64 bằng hàm băm kết cấu chỉ có thể khớp với khung trước đó.

Phương pháp này giống như bản đồ chiến thuật HD: bản đồ số màu độ phân giải cao cộng với bảng màu khung. Đường viền được chúng tôi vẽ lại bằng mã (kiểu A được người dùng chọn vào ngày 25/09/2026: theo vị trí đường ban đầu, đường đôi, đầu tròn, nhẵn). Nó được tạo bởi ROM riêng của người chơi khi trò chơi đang chạy. Những hình ảnh này không được bao gồm trong gói HD và nó không chứa các pixel gốc.

- **Tạo** ([`rom_art.cpp`](../../src/host/rom_art.cpp), chỉ CPU):
- `on_init` của `host.cpp` cung cấp ROM cho nó. Nó đọc bảng bố cục, các cảnh được lớp phủ chiến thuật sử dụng và các cảnh lưới còn lại trong năm 1165–1330 và xây dựng bảng "Cảnh → Atlas, Bảng màu", tổng cộng là 146.
- Khi xuất hiện một đường viền nào đó lần đầu tiên thì thực hiện trên luồng giải mã:
1. Đánh vần biểu đồ số màu 1× từ ROM, chỉ để biết các đường kẻ ở đâu;
2. Theo độ sáng của bảng màu, nó được chia thành hai loại: đường màu xanh và bóng tối;
3. Vẽ lại với độ phân giải gấp 4 lần: mỗi pixel là một nét tròn có bán kính 0,5, được kết nối với các lân cận lên, xuống, trái, phải và chéo (không có đường chéo khi có các lân cận góc phải để tránh lấp đầy góc), các cạnh được khử răng cưa và đường màu xanh lam che bóng tối;
4. Mỗi texel trên nét lấy số màu của pixel gốc gần nhất. Phiên bản gốc dựa vào chu kỳ bảng màu để cho phép ánh sáng truyền dọc theo khung và tính năng này vẫn hoạt động.
- Tệp tương tự cũng tạo ra hình ảnh độ phân giải cao toàn khung hình của logo BANPRESTO và GAME OVER, xem [Màn hình tiêu đề và hình ảnh văn bản lô](native-title-and-story-images.md).
- **KIỂM TRA**: `make recomp-rom-art-test` Kiểm tra ba mục sau. [`frame_hd.py`](../../tools/hd_ai/frame_hd.py) Sử dụng cùng một bảng cảnh và cắt xén để ghi thư mục so sánh `assets/hd-ai/frames/v1` (chỉ có trên máy này, không có trong gói HD).
- Bảng, cây trồng, bảng tham chiếu cho 146 cảnh phù hợp với `frame_hd.py`;
- Tâm của mỗi pixel dòng gốc được bao phủ bởi nét;
- Các nét chỉ sử dụng số màu có trong cảnh gốc.
- **Thời gian chạy** ([`native_map.cpp`](../../src/host/native_map.cpp)):
- +4 được sprite ghi ở chế độ 9 là số cảnh (1198, 1199, 1227 được xác nhận trên máy thực tế) và `host.cpp` hiện có được sử dụng để tìm tài nguyên.
- Đường viền chỉ được tạo khi có gói nghệ thuật HD (`SRW64_ART_PACK` được đặt) và nó chỉ được vẽ ở chế độ hình ảnh HD.
- Thêm bảng tài nguyên vào bảng tài nguyên khi mỗi đường viền xuất hiện lần đầu tiên. Hình ảnh gốc vẫn sẽ được vẽ ở khung này, còn ảnh có độ phân giải cao sẽ được vẽ ở khung tiếp theo. Độ trong suốt của bản đồ cơ sở bằng độ trong suốt của bảng màu nhân với độ bao phủ nét vẽ.
- uv được chuyển đổi theo điểm bắt đầu cắt xén. Độ trong suốt được trộn với tính năng nhân trước và các khác biệt về bảng màu được thêm vào trong không gian truyền qua, được thêm vào bởi phiên Steam Deck trong cổng Plume (05f339c).
- Mỗi lưới của cửa sổ nhỏ được kết cấu lại và luôn có lệnh tải giữa hai hình chữ nhật liền kề. Vì vậy, dấu cũng có thể được đặt bên cạnh SETTILESIZE: hình chữ nhật được vẽ lần này sẽ được thay thế, việc thay đổi nó không có tác dụng.

Máy thật: `check_ui_text.py` (tiếng Trung) đang chạy `build/recomp/debug/20260925T060748.275759Z/`, vượt qua 12 mục. `hd-map-summary.json` hiển thị 11 đường viền được vẽ, 888 đường viền bị ghi đè và không tìm thấy điểm đánh dấu nào. Các đường viền của menu lệnh, bảng quân, bảng vũ khí mượt mà, các góc được vát cong giống phiên bản gốc, vị trí và màu sắc nhất quán với phiên bản gốc.

## 5. Số sát thương cho trận chiến bản đồ

Khi hoạt ảnh chiến đấu không phát, số sát thương/hồi phục bật lên trên bản đồ được vẽ bởi `80209900` của lớp phủ chiến thuật.

- Tối đa 6 ô, dữ liệu ở ba nơi:
- Số lưới 1159 của mỗi lưới nằm trong `80228530`, trong đó 0 trống, 1 là `+`, 2 là `-`, 3–12 là số màu trắng viền đen và 13–22 là số màu trắng có bóng xám;
- Hiển thị cờ ở `80228536`;
- x, y nằm trong `80228548`.
- Danh sách hiển thị có hình dạng giống như công cụ văn bản: một bảng màu, sau đó là một hình chữ nhật trên mỗi lưới.
- `80209900` được đổi tên thành `srw64_original_map_damage_draw` trong `NATIVE_HOOKS` và được gọi là `damage_drawn` sau khi đóng gói. `ui_text.cpp` Sau khi kiểm tra số lượng và vị trí của các ô, hãy vẽ từng hình có độ phân giải cao.

## 6. Xác thực máy thật

```sh
.venv/bin/python tools/recomp/debug/check_ui_text.py --language zh-Hans   # 也可以 en、ja
```

Cấp độ kiểm tra `battle-ui.json`: Menu lệnh đơn vị → Menu lượt → Bảng quân đội → Mục đích chiến đấu → Xác nhận kết thúc vòng đấu → Lượt địch → Bảng vũ khí gốc → Trận chiến.

| Ngôn ngữ | Chạy | Kết quả |
| --- | --- | --- |
| Tiếng Trung | `build/recomp/debug/20260925T023727.281197Z/` | 11 lượt: menu, danh sách đơn vị, mục tiêu chiến đấu và hai dòng chữ, "Vẫn còn 4 khung máy bay chưa hoàn thành hoạt động" (chữ số đã được dịch), biểu tượng vũ khí, số HUD, huy hiệu chống, không có chuyến xác minh thất bại |
| Tiếng Anh | `build/recomp/debug/20260925T023850.869823Z/` | 11 lượt (“4 đơn vị chưa hành động.”) |
| Tiếng Nhật | `build/recomp/debug/20260925T023546.815759Z/` | 10 lượt (Người Nhật không di chuyển số, không có ai); "Hành động đã kết thúc" bị thu hẹp trong phạm vi chiều rộng ban đầu và không còn bao phủ các con số |

Xem từng ảnh chụp màn hình:
- Menu tròn tiếng Trung, danh sách quân (cùng cỡ chữ), cửa sổ xác nhận, mục tiêu chiến đấu và danh sách vũ khí.
- Menu lệnh tiếng Anh, danh sách quân, cửa sổ xác nhận và danh sách vũ khí.
- Cửa sổ xác nhận tiếng Nhật, danh sách quân đội và danh sách vũ khí.
- Chống lại các huy hiệu HP/EN, chém, viền và chống của HUD.

## 7. Chưa thực hiện và bị hạn chế

- **Văn bản rải rác chưa được trả lời**:
- Biểu ngữ khả năng vẽ chế độ 10: `8009504C` không có móc.
- Biểu ngữ sân khấu: Tài nguyên đang chờ xử lý.
- **Cửa sổ chọn nhánh**: Lấy cùng đường dẫn văn bản nhưng không có máy thật để vào nhánh đã chọn.
- **Văn bản ngoài hộp thoại của trang gốc**: Nó chỉ được tiếp quản sau khi trang hiện tại được hiển thị đầy đủ; một số khung có văn bản xuất hiện nguyên văn vẫn là văn bản gốc.
- **Khung hình đầu tiên**: Văn bản mới phải được rasterized trong chuỗi nền. Khi nó xuất hiện lần đầu, văn bản sẽ trống trong một hoặc hai khung và sẽ được lưu vào bộ đệm sau đó.
- **Nền tảng**: Móc kéo gốc hiện chỉ có Kim loại.