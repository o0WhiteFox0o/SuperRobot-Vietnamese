> **Ngôn ngữ / Language:** [Tiếng Việt](custom-campaign.vi.md) · [English](custom-campaign.en.md) · [中文](custom-campaign.md)

# Chiến dịch tùy chỉnh: chuỗi đa cấp, hộp thoại mới và bản đồ hoàn toàn mới được vẽ

2026-10-01. Mục tiêu do người dùng đặt ra: Bản mod có thể kết nối nhiều cấp độ tùy chỉnh vào một chiến dịch; bản đồ mới dựa trên "bản vẽ tự do của toàn bộ bản đồ": ở chế độ HD, toàn bộ bản đồ được tác giả vẽ và ở chế độ gốc, nó hiển thị một phiên bản gần đúng được nhồi vào định dạng ban đầu. Bài viết này là **phân tích tĩnh** (đọc mã được tạo, ROM và nguyên mẫu Python) và chưa được chạy trên máy chủ; địa chỉ dựa trên mã được tạo của 94f110b chính. Các mục được đánh dấu [máy thực tế] có hồ sơ hoạt động trước đó và phần còn lại sẽ được xác minh bởi máy thực tế. Để biết cách lập kế hoạch cấp cao hơn, hãy xem [lộ trình sửa đổi](mod-roadmap.md) và [kiến trúc mở rộng](native-extensibility-architecture.md) §6.

## 1. Đã có nền tảng

- **Cấp đơn**: [Cấp nhỏ](../script/mini-stage.md) Sử dụng JSON để viết bản đồ, sự kiện, triển khai và tài nguyên ban đầu. Sau khi biên dịch, thay thế một cảnh trong bộ nhớ. Quá trình hoàn chỉnh (khai mạc, tấn công, sự kiện vòng đấu, chiến thắng, kết thúc, lưu trữ giải quyết) [máy thực tế] chạy qua. Tất cả 1812 sự kiện trong tập lệnh đã được giải đến ký hiệu kết thúc và 73 hướng dẫn thông thường đã được khớp với mã ([Khám phá tập lệnh](../script/stage-script-exploration.md)).
- **Bản ghi văn bản giả**: Máy chủ đã cung cấp cho trò chơi các bản ghi văn bản không có trong ROM. Đây là cách sửa đổi văn bản vị trí của màn hình: `host.cpp` kết thúc việc tra cứu bản ghi `8008C510` và ROM đọc `8007F704`, `upgrade_rules.hpp:415-451` trỏ bộ mô tả tới vùng ROM giả (`0x03000000 + id×0x40`) rồi cung cấp byte. Các dòng mới theo cách tiếp cận này (§5).
- **Bản đồ vẽ toàn bộ**: Bản đồ chiến thuật HD đã được chủ nhà vẽ toàn bộ theo số bố cục (`native_map.cpp`, 131 bản đồ).
- **Thanh đa lưu và tự động lưu**: Thư viện `saves/` và tính năng tự động lưu có sẵn bên cạnh `.json` ([Thanh đa lưu](save-slots-autosave.md)).

## 2. Cách chuyển giữa các cấp độ trong phiên bản gốc

| Bước | Mã | Phải làm gì |
| --- | --- | --- |
| Vượt qua | `3D4A` → `8020DB08` | Xóa các giai đoạn và vòng (F5E8/F5EA), tổng số vòng tích lũy (F5EC), thêm một vào số từ `8010F5EF`, sao chép cảnh hiện tại F5F0 sang F5F1 (cảnh đã qua), chuyển sang chế độ 0x24; sau đó chạy sự kiện kết thúc (loại 14) trên bản đồ thế giới |
| Chỉ định cấp độ tiếp theo | `3D4B n` → `800A0260` | `F5F0 = F5F2 = n`; khi n=500, sao chép F5F2 trở lại F5F0. Vì vậy F5F2 luôn là mục tiêu được chỉ định rõ ràng cuối cùng |
| Giữa cảnh | Sau khi sự kiện kết thúc, `8009EDB8` được đặt ở chế độ 4 → `801D8F74(0)` | Sau khi vượt qua cấp độ, hãy yêu cầu lưu tệp trước (ảnh chụp màn hình [máy thực] "Tập 1...クリア"), "Tiếp theo のマップへ" của `801D8D20` → Chế độ 0xC → `801C2B9C(0)` |
| Tải cấp độ tiếp theo | `801C2B9C(0)` → `8009DD58(F5F0, 0)` → `8009DE7C` | F5F1 = F5F0; **Khi F5EF bằng 0, biến tuyến đường `801602EE` được sử dụng để khởi chạy số cảnh**; Triển khai DMA và các sự kiện theo cảnh |
| Cốt truyện bản đồ thế giới | Sự kiện khai mạc cấp độ riêng (loại 12) | Trận mở màn chạy trên bản đồ thế giới (`3D32`/`3D33`, `3D3A` phát nhạc), `3D4D` chuyển sang bản đồ chiến thuật; không có "bảng cảnh bản đồ thế giới" riêng biệt |

Bảng được kiểm tra theo số cảnh: bản đồ `802195B0[场景×2]` (`80209D6C` viết vào F5EE), thẻ tiêu đề `802195B1[场景×2]` (`801C72C8`), văn bản tiêu đề 281+F5F1 (giữa các cảnh `801CE0F8`, danh sách lưu trữ `801C6944`/`801C754C`), menu xen kẽ chỉ có các mục "Lưu/Cấp tiếp theo" bên trái (F5F1 trong `D_801DC6D4`: 13 cảnh "(trước)" cộng với 132), cấp độ Rinku 109–122 (`D_801DCABC`), bảng cảnh vũ trụ `D_801DCAD8`.

Khi bắt đầu cấp độ, `8009DE7C` đặt lại các biến 100–114 và 128–139 thành 3 và biến 54 thành 1; khi kết thúc phần mở đầu, `80093278(0)` chụp ảnh nhanh trong bộ nhớ (`800FBEF0`) và thử lại sau khi trò chơi kết thúc để tiếp tục từ đây.

## 3. Gói chiến dịch

```text
mods/<战役>/
  mod.json              名字、作者、版本
  campaign.json         关卡表、开局、标题、所借场景号
  stages/<关>.json      迷你关卡格式（srw64.mini-stage.v1）
  text/<语言>.txt       新台词，台词文本格式，记录号用 mod 段（§5）
  maps/<图>/            新地图：整张底图、地形格、可选水面色号图（§6）
```

`campaign.json` biểu thị:

```json
{
  "schema": "srw64.campaign.v1",
  "start": "prologue",
  "stages": {
    "prologue": {"scene": 1, "file": "stages/prologue.json", "title": "序章　新しい風"},
    "ch2":      {"scene": 2, "file": "stages/ch2.json",      "title": "第2話"}
  }
}
```

Kết nối giữa các cấp được ghi trong sự kiện kết thúc của mỗi cấp (`3D4B <下一关借的场景号>`) và các nhánh sử dụng các khối điều kiện và biến biểu đồ, giống như phiên bản gốc; `campaign.json` chỉ đăng ký "số cảnh nào tương ứng với cấp độ nào".

## 4. Chủ nhà phải làm gì

### 4.1 Mượn số cảnh

- **Mượn số cảnh gốc khác nhau (0–142) cho mỗi cấp độ**. Phiên bản gốc các sự kiện và triển khai DMA đầu tiên theo số cảnh và máy chủ được thay đổi trong `8009DE7C`, vì vậy số được mượn phải thực sự tồn tại; nếu các số khác nhau được mượn cho mỗi cấp độ thì các byte cảnh trong kho lưu trữ có thể trỏ ngược lại cấp độ đó một cách duy nhất.
- **Tránh**: cảnh "(Trước)" và 132 (sẽ có ít mục hơn trong menu giữa các cảnh), Rinko cấp 109–122 (trang Rinko sẽ bị lộn xộn).
- **Thay đổi máy chủ**: `mini_stage.hpp` hiện chỉ có một `Image`, khóa cảnh đã đăng ký đầu tiên. Các cảnh khác được đánh dấu là "bỏ qua" và chỉ có thể tải trong menu tiêu đề. Thay đổi thành bảng "Số cảnh → Hình ảnh", `register_hook` và `map_hook` được `8010F5F0` thu được. Bàn đã cố định với trận chiến: コンティニュー, thử lại khi kết thúc trò chơi và nửa chặng quay về bản đồ sẽ được đăng ký lại (`8009DD58(场景, 1/2)`, điểm gọi `800803D4`/`8008046C`/`80080594`) và cặp đôi phải được thay đổi tại thời điểm này.
- **リンク Menu** sẽ ghi đè F5F0/F5F2 và sẽ bị vô hiệu hóa hoặc chặn trong chiến dịch.

### 4.2 Bắt đầu và kết thúc

- **Bắt đầu**: Nhập trực tiếp (ghi F5F0 và F5EF=1 sau `800A5138`) [máy thật]. `800A5138` xóa F5EF–F5F2 qua `800814F0` và xóa danh sách qua `800A4F94`, do đó, điểm bắt đầu là một danh sách trống, không có tên và không có biến lộ trình. **F5EF phải khác 0**, nếu không cấp độ tiếp theo sẽ được lấy từ biến tuyến đường (nếu nhập trực tiếp, bạn sẽ nhận được cảnh 253 mà không cần đặt thời gian).
- **Lực lượng ban đầu**: Trong sự kiện khai trương, sử dụng `3D5A 驾驶员,0,机体,500` để đăng ký (đơn vị 999 = chỉ đăng ký trình điều khiển) [máy thật], `3D5B` để nạp tiền, `3E13` để đặt biến; Bản thân hồ sơ triển khai của người chơi cũng sẽ được thêm vĩnh viễn vào nhóm (đây là cách mọi người được thêm vào cấp độ Rinku) [máy thực tế]. Cạm bẫy: `3D5A … 4000` sẽ để lại danh sách lủng lẳng cho các đơn vị vẫn còn trên bản đồ. Sau SIGBUS, trước tiên bạn phải `3D46` [máy thực tế]; `3D49` gặp sự cố khi ký tự không có trên bản đồ [máy thật]. `SRW64_STATE_FIXTURE` chỉ căn chỉnh các số ngẫu nhiên và không thể tạo chiến dịch. Mã lưu trữ (`load_000856D0:801C39C4…`) của menu gỡ lỗi "SAMPLE DATA" có thể được sử dụng làm tài liệu tham khảo.
- **Kết thúc**: `3D71` Phải chạy trên lớp phủ bản đồ thế giới (chạy trên bản đồ chiến thuật sẽ khiến máy chủ hủy) [máy thực tế]. Lớp phủ kết thúc đặt bit giải phóng mặt bằng (`8015DDA8` bit 3), ghi tiêu đề lưu trữ và trả về tiêu đề. Đặt `3D71` vào sự kiện kết thúc ở cấp độ cuối cùng của chiến dịch.
- **Kết thúc trò chơi**: `3D4C` → TRÒ CHƠI TRÒ CHƠI → Khôi phục ảnh chụp nhanh sau khi mở và đăng ký lại cảnh tương đương với việc chơi lại cấp độ; không có ảnh chụp nhanh nào tại `3D4C` trong nửa thời gian mở và cảnh 0 [máy thật] sẽ được đăng ký.

### 4.3 Vẽ biểu đồ các biến

200 biến hai bit trong `8015E818`, 26 nửa từ từ kho lưu trữ +0x2. 0–54 là số mà phiên bản gốc liên tục đọc và 100–114 và 128–139 được đặt lại ở đầu cấp. Cờ riêng của trận chiến phải sử dụng một biến không thể đọc và viết bằng chữ viết gốc. Cần phải tính khoảng thời gian rảnh cụ thể (quét `3E13` và các điều kiện trong tất cả các sự kiện).

### 4.4 Lưu trữ

- Bản ghi lưu trữ gốc (0x1F00, được viết bởi `800924D8`): +0x2 biến, +0x48 khối tiến trình (+0x4E bản đồ, +0x4F số tập, +0x50 cấp độ tiếp theo F5F0, +0x51 cảnh tiêu đề F5F1, +0x52 F5F2, +0x53 mức cơ sở, +0x54 quỹ), +0x110 nội dung, +0x9D0 thí điểm, các bộ phận +0xE80. Kho lưu trữ bị gián đoạn 0x3AE0 cũng chứa trạng thái bản đồ.
- **Nhận dạng kho lưu trữ chiến dịch**: Bản thân kho lưu trữ chỉ có số cảnh mượn. Máy chủ ghi một tệp bổ sung (id chiến dịch, phiên bản, bảng cảnh) bên cạnh nó và tải chiến dịch tương ứng khi đọc tệp; khi thiếu tệp bổ sung hoặc chiến dịch không được cài đặt, nó sẽ từ chối đọc tệp và giải thích, đồng thời không thể tải cảnh gốc một cách lặng lẽ.
- Điểm rớt: `saves/` Kho lưu trữ tự động trong thư viện đã có `.json` (`save_store.cpp`'s `sidecar()`); cột mở rộng thủ công và cột cassette 1/2 vẫn chưa có sẵn. Không có đường dẫn tệp khi ghi cột cassette trong giao diện gốc. Nhấn bản ghi SHA-256 làm khóa. Khuyến nghị mỗi chiến dịch nên có một thư viện lưu trữ độc lập, tách biệt với bài viết này.

### 4.5 Tiêu đề và văn bản giao diện

Thẻ tiêu đề (`sprite_text.cpp:365-391`), dòng chương liên cảnh (`intermission_page.cpp:30`) và danh sách lưu trữ (`save_page.cpp`) đều được truy xuất từ bảng mục nhập máy chủ mà không cần đọc ROM, do đó chúng có thể bị ghi đè bởi chiến dịch: máy chủ thêm bảng "số cảnh mượn → tiêu đề chiến dịch". Hình ảnh thẻ tiêu đề ở chế độ giao diện gốc được tính riêng (bảng thẻ tiêu đề `802195B1`).

## 5. Dòng mới

- **Đoạn số bản ghi**: Số văn bản trong tập lệnh là u16 và có 50.975 mục trong bảng 0 (tối đa `0xC71E`). Trò chơi không kiểm tra khi số lượng vượt quá giới hạn và sẽ đọc văn bản dưới dạng mô tả với độ dài ngẫu nhiên. **mod sử dụng `0xC800`–`0xFFFF`** và máy chủ sẽ bắt nó trước tại vị trí tìm kiếm. Bỏ qua đường dẫn và gọi trực tiếp `8008CE54` (`game_hooks.cpp:433`), đồng thời kết nối nó.
- **Nội dung máy chủ muốn giả mạo** (sử dụng vùng ROM ảo của màn hình đã sửa đổi, thay đổi địa chỉ và chỉ cho phép đọc 4 byte đầu tiên):
- Tiêu đề ASCII 8 byte: ba chữ số cho người nói (000–360, tức là số ký tự), một chữ số cho chế độ và bốn chữ số cho chờ;
- Khoảng cách văn bản: chính xác “số trang - 1” `0xFFFD`, kết thúc bằng `0xFFFF`, không quá 255 từ (bản gốc không có kiểm tra ranh giới);
- Trong bảng nhập có mục nhập cho từng ngôn ngữ, bao gồm `ja` và `<STOP>`. Số phù hợp với số trang (Host điều khiển trang lật theo số STOP của `ja`).
- **Đang tải lớp**: `dialogue_text::compile` Từ chối các bản ghi không có trong ROM và các dòng mod phải chuyển sang một lớp riêng (`Catalog::with_translations`).
- **Người nói và hình đại diện**: Hình đại diện được lấy từ tài khoản của người nói thông qua ROM `0x84220 + 人物×4`; bạn có thể mượn hình đại diện và tên của nhân vật hiện có theo ý muốn. Tên mới: Máy chủ thay thế số bản ghi bảng tên (`0x111E + 说话人`) bằng số ảo. Hình đại diện mới: Hình được vẽ trong trò chơi vẫn là hình được mượn và lớp HD (`native_portrait.cpp`, được xác định bằng hàm băm pixel và bảng màu) phải được ghi đè bởi loa mod hoặc số dòng; khuôn mặt mượn sẽ được hiển thị ở chế độ ảnh gốc.
- **Chọn chi**: `3D44 槽, 项数, 文本号`, tối đa 3 mục, kết quả ghi là `+0x994` để `3E10`–`3E12` phán xét. Khi được hiển thị, `ui_text.cpp:307` sẽ chỉ thay đổi bản dịch khi mục nhập `ja` bằng với hình tượng được trò chơi giải quyết. Số mod phải khớp với ký tự giữ chỗ hoặc thay đổi nó thành số mod tin cậy.
- **Chiến tuyến** (làm sau): Nhấn `D_800CA9C4[人物]` để lấy slot thoại có trong ROM `0x1161C0` và `0x121150`. Để gán dòng cho ký tự mới, hãy chấp nhận `800A3DD0` để trả về dòng ảo hoặc chấp nhận chức năng chọn `80222B14`/`80222050`; việc `5813 + 偏移` có thể đạt đến `0xC800` hay không vẫn chưa được xác nhận.

## 6. Bản đồ mới

### 6.1 Định dạng gốc (đã chọn)

- **Bản ghi bản đồ**: 158 mục × 12 byte, bảng trong `0x80219B1C` (ROM `0x10267C`): `u16 布局, 图集, 调色板, aux1, aux2; u8 模式; u8 BGM`. Đọc `8010F5EE` (số bản đồ) từ `801C6EFC` rồi tải: `80098158(0x3B, 0, 8, 0x93, 布局, 图集, 调色板, 0)`, aux vào kênh chu kỳ bảng màu và chế độ 1 sẽ cài đặt một khung thuộc địa khác. `3D34` Thay đổi ảnh (`8020A874`) và sử dụng cùng một bộ.
- **Bố cục**: Tiêu đề 8 byte `(7, 组数, 宽, 高)` (đơn vị 8 pixel), sau đó là 4 byte trên mỗi lưới 16×16: `u16 (翻转 0xE000 | 地形号)`, `u16 图块号`, sau đó là nhóm vẽ. Tất cả 154 bố cục và 285.974 ô đã được kiểm tra: số ô và bit lật của lưới phù hợp với nhóm vẽ. Atlas CI8 512×512, lên tới 1024 ô 16×16 (ô tọa độ 12 bit).
- **Địa hình**: Lấy +1 (8 bit thấp hơn) của bản ghi lưới chỉ đọc địa hình `801E213C(x格, y格, 0x3B, 0)`, không kiểm tra ngoài giới hạn. Bảng thuộc tính `0x802196D0` (ROM `0x102230`), 100 mục × 11 byte:

| Byte | Ý nghĩa | Người đọc |
| --- | --- | --- |
| +0 | Tên địa hình (Bảng 0 số văn bản 0–59) | Cửa sổ địa hình `801CABAC` |
| +1 | Phòng thủ: Sát thương ×(100 − giá trị)/100 | `801F424C` Chọn 0 (không đổi 100 khi bay) |
| +2 | Công cụ sửa đổi lượt truy cập, đã ký (chủ yếu là phủ định) | `801F424C` Chọn 1 |
| +3 / +4 | Bắt đầu lượt hồi phục HP/EN % | `801FA3DC` → `801FA260` |
| +5..+10 | Tiêu thụ chuyển động của sáu phương thức chuyển động, không thể truy cập 0xFF | `801C3E50` Sử dụng `801EEA14(单位)` để chọn cột; 0=mặt đất, 1=không khí, 3=nước, 5=không gian (suy luận), 2 và 4 chưa quyết định |

Địa hình 63 là bức tường (tất cả 0xFF, được đặt tên là "bức tường"), 99 là đường viền bên ngoài và 100 là địa hình giả "bầu trời" được sử dụng làm nền chiến đấu. Danh sách mã địa hình vùng nước `0x802180D4`: 31–36, 87–89, 91.
- **Bảng theo số bản đồ** (mỗi mục 158): Cờ vũ trụ `0x802180E0` (1=Quy tắc di chuyển của vũ trụ; thích ứng địa hình chiến đấu khi khác 0 được tính theo vũ trụ; 2 chỉ thay đổi byte môi trường chiến đấu, như "Bản đồ loại mặt đất trong vũ trụ", bản đồ 37, 39, 49, 50, 60, 64, 72); Màu đường lưới `0x80218510` (0 đen, 1 Xám, 0xFF Không có, đặt bit `8015DDA8 & 2` (được sử dụng khi mở lưới).
- **Nền chiến đấu được xác định bởi số bảng**: `801F68E8` Ghi địa hình lưới (100 khi bay) và byte môi trường vào bối cảnh chiến đấu. Các byte môi trường được lấy từ bảng tra cứu theo số tài nguyên bảng màu (`0x80218A57 + 调色板号`, bao gồm 6237–6263). Bản đồ mới sẽ mượn số bảng màu hiện có để chọn nền.

### 6.2 Kích thước

Kích thước bản đồ được xác định hoàn toàn bởi tiêu đề bố cục (`801C6394` ghi `80172EC4/EC8`) và không thể tìm thấy mảng có độ dài cố định được mở bằng lưới: phạm vi di chuyển là lưới cục bộ 31×31 được căn giữa trên đơn vị (`801C3E50`, giới hạn trên của phạm vi là 15 lưới) và tỷ lệ chiếm chỗ được quét theo tọa độ pixel đơn vị. Chỉ có ba hạn chế: không thể truy cập được đường viền 2 ô bên ngoài (phạm vi có thể chơi được x, y ∈ [32, W−48]); thu phóng tổng quan `800943E0` sẽ chia cho 0 khi nó rộng khoảng 4256 pixel và cao 3200 pixel; giới hạn trên của tập bản đồ là 1024 ô. Phiên bản gốc đạt tối đa 960×720.

### 6.3 Cài đặt vào game

- **Chỉ có một điểm vào để đọc tài nguyên**: `80089E9C(资源号) → 句柄`. Số ≥ `0x1924` bị từ chối trực tiếp; nếu cùng một số đã có trong bộ nhớ thì chỉ có số tham chiếu được thêm vào; nếu không thì `80089BBC` đọc phần mô tả và kích thước đã giải nén của ROM `0xA20BD4 + 号×8` và `800897AC` được giải nén từ ROM LZ vào vùng nhớ heap (vùng 6, `0x80277800`, khoảng 1,6 MB). Hai hàm nội bộ này chỉ được gọi bởi `80089E9C`.
- **Phương pháp**: Mượn số bản đồ của bản đồ gốc. Ở cấp độ chiến dịch, máy chủ thay thế bố cục, tập bản đồ và bảng màu bằng mod byte: tiếp quản `80089BBC` và báo cáo kích thước của mod, đồng thời thay đổi `800897AC` để sao chép (đánh giá xem nó dựa trên số tài nguyên vừa được ghi vào bảng điều khiển +2). Việc thay thế phải nhất quán trong khoảng thời gian đỗ cùng một số xe. Không thể sử dụng số tài nguyên mới ( ≥ `0x1924` bị từ chối), vì vậy số này chỉ có thể được mượn; Số lượng mượn được xác định bởi gói chiến dịch và số bảng màu cũng xác định bối cảnh trận chiến (§6.1). Các bảng BGM, logo vũ trụ, màu lưới theo số bản đồ cũng được viết lại theo số bản đồ mượn.
- **Xung đột HD**: Bản đồ HD được nhận dạng theo số bố cục (`find_asset` trong số `find_asset`) và số bố cục mượn sẽ được vẽ trên bản đồ nền HD của bản đồ gốc. Chủ nhà cần nhấp vào bản đồ mod để lấy bản đồ ở cấp độ chiến dịch.

### 6.4 Toàn bộ bản vẽ và phiên bản gốc đã hạ cấp

- **HD**: Tác giả vẽ bản đồ lớn gấp 4 lần kích thước ban đầu (giống bản đồ HD hiện có) và chủ nhà vẽ toàn bộ bản đồ. Nếu mặt nước muốn dịch chuyển thì cho thêm bản đồ mã màu khác để biểu thị diện tích mặt nước (bản đồ HD hiện có là bản đồ nền cộng với bản đồ mã màu).
- **Phiên bản hạ cấp gốc**: Công cụ giảm hình ảnh lớn về kích thước ban đầu, cắt thành lưới 16×16, sử dụng k-mean để tập hợp nó thành không quá 1024 ô (cho phép lật ngang và dọc và tái sử dụng), sau đó lượng tử hóa thành 256 màu để tạo bố cục, tập bản đồ và bảng màu. Nguyên mẫu (2026-10-01, Python script trong Scratchpad, không có trong kho) đã thử với bản đồ cơ sở HD của Bản đồ 56: 864×800, 2700 lưới được nén thành 1024 khối, so với bản đồ mục tiêu PSNR 35,8 dB (chỉ lượng tử hóa 256 màu là 42,4 dB). Địa hình, bờ biển, rừng và núi vẫn được bảo tồn và kết cấu của cỏ được làm mờ ở mức trung bình. Bản đồ nhỏ hơn 1024 ô (ví dụ: bản đồ 20.896 ô) không cần phân cụm.
- **Tái chế bề mặt nước**: Mặt nước ban đầu phụ thuộc vào quá trình tái chế bảng màu (số màu 0xC0–0xD0). Phiên bản hạ cấp cần ánh xạ màu của vùng mặt nước vào phần này và treo tài nguyên tái chế mặt nước trong aux.
- **Địa hình**: Tác giả cung cấp cho mỗi lưới một số địa hình (0–98 và vòng tròn bên ngoài được tự động điền 99) trong trình chỉnh sửa. Chỉ có 100 thuộc tính trong bảng thuộc tính và các loại địa hình mới chưa được hỗ trợ.

## 7. Theo từng giai đoạn

| Sân khấu | Nội dung | Chấp nhận |
| --- | --- | --- |
| Kết nối đa cấp C1 | `campaign.json`; máy chủ cấp nhỏ đã thay đổi thành danh sách số cảnh; bắt đầu, kết thúc; đánh chặn Rinko; ghi đè tiêu đề; lưu trữ file đính kèm và từ chối đọc file | Sử dụng bản đồ gốc và đường ban đầu để tạo chiến dịch nhỏ 3 cấp: tham gia nhóm ngay từ đầu, lưu cấp độ, tải tệp để tiếp tục chơi, thử lại khi kết thúc trò chơi, phân nhánh và quay lại tiêu đề ở cuối |
| Dòng mới C2 | đoạn văn bản mod `0xC800`+, bản ghi ảo, mục nhập ba thứ tiếng, chi tùy chọn, thẻ tên mới | Có các đoạn hội thoại mới và các chi tùy chọn trong chiến dịch và các trang được lật chính xác bằng ba ngôn ngữ; Tải lại nóng F5 |
| Bản đồ mới C3 | Thay thế tài nguyên, số bản đồ mượn và các bảng liên quan, thu thập bản đồ HD bằng mod, công cụ bản đồ (bản đồ lớn + lưới địa hình → bố cục/atlas/bảng màu + HD) | Bản đồ tự vẽ: tiêu hao di chuyển, phòng thủ và đánh địa hình, phục hồi, mặt nước, bối cảnh chiến đấu, tổng quan, cửa sổ địa hình đều chính xác; xem phiên bản hạ cấp của chế độ ảnh gốc |
| Nhân vật mới C4 | Hình đại diện mới (Ghi đè HD bằng loa mod), chiến tuyến | Cốt truyện hội thoại và chiến đấu cho nhân vật mới |

## 8. Triển khai C1 (2026-10-01, chiến dịch tùy chỉnh cây công việc)

Do người dùng xác định: Chỉ các tài nguyên hiện có (bản đồ gốc, dòng, ký tự, triển khai) mới được sử dụng cho chiến dịch thử nghiệm. Bản đồ mới, bối cảnh đối thoại cốt truyện, nhân vật mới và máy móc mới sẽ được nghiên cứu sau.

| Phần | Phương pháp |
| --- | --- |
| Nguồn chiến đấu | `config/recomp/campaigns/<名>/campaign.json` (`srw64.campaign.v1`): `id`, `start`, `stages` cho mỗi cấp độ `scene`, `file` (nguồn cấp độ nhỏ), `title` (chuỗi hoặc đối tượng theo ngôn ngữ) |
| Biên dịch | `mini_stage.py campaign <campaign.json> --out <image.json>` → `srw64.campaign-image.v1`. Biên dịch theo cấp độ, từ chối số cảnh không thể mượn ("(cũ)" 13 và 132, 109–122, >142), hai cấp độ mượn cùng một số cảnh, không thể tìm thấy cấp độ bắt đầu và `3D4B` chỉ vào các cảnh khác ngoài chiến dịch (500 trường hợp ngoại lệ) |
| Máy chủ | `campaign.hpp` ghi lại danh tính và tiêu đề của chiến dịch; `mini_stage.hpp` thêm bảng "số cảnh → hình ảnh cấp độ" mới: `SRW64_CAMPAIGN` để tải, `register_hook`, nhấn `8010F5F0` để lấy hình ảnh, `map_hook` Sử dụng bản đồ cấp độ; nếu không có số cảnh mượn từ cấp độ, nó sẽ tải đồng thời theo phiên bản gốc. Nhập trực tiếp số cảnh để ghi cấp độ; sau khi đăng ký cấp 1 xóa số từ `8010F5EF` về 0, để sau khi vượt qua cấp 1 thì tập đầu tiên |
| Tiêu đề | `dialogue::ui_text` Đối với hơn 281 số cảnh, hãy trả lại tiêu đề chiến dịch. Nó sẽ được sử dụng giữa các cảnh và danh sách lưu trữ; nó cũng sẽ được sử dụng nếu tiêu đề bị kẹt ở cấp chiến dịch |
| リンク | Khi mở trang リンク gốc trong thời gian diễn ra chiến dịch, bạn sẽ trực tiếp nhấn hủy để thoát và nhắc nhở (màn hình リンク ban đầu ban đầu là một khối trống) |
| Lưu trữ | Trình khởi chạy `--campaign <编译后的战役>`: Thư viện lưu trữ được đổi thành `用户目录/campaigns/<id>/saves`, tách biệt với bài viết này và không di chuyển các phiên cũ; loại trừ lẫn nhau với `--import-save`. Phiên gỡ lỗi `Session.launch(campaign=…)` biên dịch các tệp nguồn và thư viện lưu trữ được đặt trong thư mục đang chạy `campaign-saves` |
| Mẫu | `config/recomp/campaigns/sample`: Mở đầu (cảnh 1, bản đồ 20) → ngã ba đường (cảnh 2, bản đồ 19, chọn nhánh 18402) → kết thúc A (cảnh 3, bản đồ 0) hoặc kết thúc B (cảnh 4, bản đồ 21), tự động giành chiến thắng ở vòng đầu tiên của mỗi màn, sự kiện kết thúc của màn kết thúc chạy `3D71` |

**Máy thật** (`tools/recomp/debug/check_campaign.py`, đang chạy `build/recomp/debug/20261001T151257.210854Z`, đã vượt qua tất cả 12 mục): Chiến dịch đã được tải; sau khi vào trực tiếp, đoạn mở đầu được đăng ký ở cảnh 1; sau khi vượt qua cấp độ, "Mở đầu: Khởi hành" và tập 1 sẽ được hiển thị trong trò chơi; được lưu vào cột đầu tiên của băng cassette, danh sách lưu trữ hiển thị cùng tiêu đề; Rinku bị dừng lại; cấp độ tiếp theo là ngã ba đường (cảnh 2, bản đồ 19); Chọn tùy chọn đầu tiên để nhập phần kết thúc A và quay lại tiêu đề sau phần kết thúc; đọc cột đầu tiên của tiêu đề để quay lại cảnh sau khi vượt qua đoạn mở đầu, sau đó đi vào ngã ba đường, chọn phương án thứ hai để vào kết thúc B (Bản đồ 21), và quay lại tiêu đề sau khi kết thúc.

**Kiểm tra**: `tests/test_mini_stage.py` (tổng hợp mẫu, cảnh không thể mượn, cảnh lặp lại và ngoài giới hạn `3D4B`), `tests/native_mini_stage.cpp` (thay đổi hình ảnh và bản đồ theo số cảnh, cảnh chưa đăng ký, cảnh mở đầu và số chương, trận chiến bất hợp pháp; nhân tiện, đã sửa một chỗ mà thử nghiệm đã thất bại: phần menu chính kiểm tra đường dẫn trò chơi mới, trước tiên bạn phải đóng nó và nhập trực tiếp), `tests/native_app.cpp` (tham số `--campaign`).

**Thử lại khi kết thúc trò chơi** (02-10-2026, `tools/recomp/debug/check_campaign_retry.py`, đang chạy `build/recomp/debug/20261002T011836.386183Z`, đã vượt qua cả 4 mục): Chiến dịch thử nghiệm `config/recomp/campaigns/retry` chỉ có một cấp độ (mượn từ cảnh 5), tùy chọn đầu tiên của vòng 1 là `3D4C` và mục thứ hai là `3D4A`. Chọn tùy chọn đầu tiên → TRÒ CHƠI TRÒ CHƠI → Khi thử lại, bạn vẫn sẽ đăng ký lại ở cấp độ chiến đấu (cảnh 5, bản đồ 20, không quay lại cảnh 5 ban đầu); sau đó chọn phương án thứ hai để giành chiến thắng và quay lại danh hiệu sau khi kết thúc.

**Văn bản nhắc**: Khi Rinku bị dừng, hai dòng nhắc "Cảnh không thuộc về trận chiến" được nhập vào danh sách nhập (`campaign_link_blocked`, `campaign_scene_unmapped`, ba thứ tiếng).

### MOD Quản lý và Chi phí Bổ sung (2026-10-02)

Người dùng muốn "cảm giác về lối vào DLC, tương tự như Z SP", **Các cấp độ DLC là các kho lưu trữ riêng biệt**; sau đó, lối vào "MOD" được đặt trên màn hình tiêu đề và quản lý MOD tổng thể được nhập, phân loại theo chức năng (lựa chọn của người dùng: nút gốc ở góc dưới bên phải; bắt buộc phải có cả bốn danh mục). luyện tập:

- **Lối vào**: "MOD" ở góc dưới bên phải màn hình tiêu đề, hình ảnh chữ là mục trong menu vòng (cỡ chữ 14 pixel gốc của `menu_style`, nét tối 1 pixel, bóng 0,8 pixel, xám đậm và xanh lam khi không được chọn, xanh sáng khi trỏ chuột hoặc tay cầm được chọn), không có khung. Bốn góc của màn hình tiêu đề (do người dùng xác định): lối vào cài đặt phía trên bên trái, tốc độ khung hình phía trên bên phải, số phiên bản phía dưới bên trái, MOD phía dưới bên phải. Bộ điều khiển được nhập vào dòng "Quản lý MOD" trên trang "Chung" của cài đặt (có thể mở bất kỳ lúc nào). Không vào menu chuông gốc.
- **Quản lý MOD**: Chế độ xem chuyên dụng của bảng cài đặt, bốn tab riêng, thay đổi trang L/R hoặc Q/E:
- **Kịch bản bổ sung**: Một dòng cho mỗi chiến dịch: tên, giới thiệu, cấp độ, phiên bản, tác giả, có kho lưu trữ hay không và nút "Enter"; có một dòng bổ sung trong chiến dịch "Đang chơi: <tên>" và "Quay lại chương này", và nút bạn đang chơi sẽ hiển thị "Đang chơi" và có màu xám. Chuyển đổi chỉ khả dụng trên màn hình tiêu đề, nếu không, nút này sẽ chuyển sang màu xám và được giải thích. Tên và phần giới thiệu có thể viết bằng ngôn ngữ (`name`, `description` của `campaign.json`, đưa vào hình ảnh khi biên dịch).
- **Art**: nút chuyển gốc/HD (cùng nút chuyển với cài đặt), gói HD có được cài đặt hay không và thư mục chứa nó.
- **Dòng và ngôn ngữ**: Thư mục dòng của trình phát, "Tải lại dòng" (giống như F5) và số lượng dòng được tải trong mỗi ngôn ngữ, từ một số tệp và có bao nhiêu lỗi (`dialogue::text_summary()`).
- **Âm nhạc & Giọng nói**: Vẫn đang được phát triển, chỉ có mô tả.
- **Chuyển đổi mà không khởi động lại, chỉ thay đổi đường dẫn lưu trữ** (Người dùng: "Chúng tôi sẽ tách đường dẫn lưu trữ"; đã từng thực hiện một phiên bản khởi động lại và thay đổi đĩa đã bị xóa): Nhấp vào "Enter" trên menu vòng tiêu đề → `campaign_switch::enter`:
1. Sao chép `cartridge.sram` của thư viện lưu trữ chiến dịch sang `saves/campaigns/<id>/<游戏>.bin` của thư viện thời gian chạy (nếu không, hãy xóa nó và định dạng trò chơi dưới dạng băng cassette mới);
2. `ultramodern::change_save_file("campaigns/<id>", 游戏)`: Thư viện thời gian chạy trước tiên ghi SRAM hiện tại trở lại tệp của chương này, sau đó đọc nó vào chiến dịch;
3. `save_store::switch_library`: Cột lưu trữ, lưu trữ tự động và phát hành băng cassette đều được thay đổi thành `用户目录/campaigns/<id>/saves`;
4. `mini_stage::load_file(战役, enter=false)`: Chỉ cài đặt chiến dịch, quay lại tiêu đề và đợi "Bắt đầu chiến dịch" hoặc tải tệp.

"Quay lại bài viết này" ngược lại: `change_save_file("")` Đọc lại tệp SRAM của bài viết này (nó chưa được chạm vào sau khi cắt đi), thay thế thư viện lưu trữ bằng thư viện khi khởi động và gỡ cài đặt chiến dịch. Tệp thư viện thời gian chạy của chương này không được ghi trong chiến dịch, vì vậy trình khởi chạy vẫn gửi nó vào thư viện lưu trữ của chương này khi thoát; kho lưu trữ của chiến dịch đã được xuất bản lên thư viện riêng của chiến dịch mỗi khi băng cassette được viết trong trò chơi. Những người bắt đầu bằng `--campaign` không có bài viết này để quay lại và không cung cấp tính năng chuyển đổi.
- **Màn hình tiêu đề trong chiến dịch**: "Bắt đầu chiến dịch" và tên chiến dịch ở giữa; "Quay lại chương này" từ quản lý MOD.
- **Vị trí cài đặt**: `用户目录/campaigns/<id>/campaign.json` (chiến dịch đã biên soạn), `saves/` được lưu trữ trong cùng thư mục; cũng đọc `campaigns/` (`Resources/campaigns` của gói Mac) đi kèm với chương trình và cùng một ID tùy thuộc vào thư mục người dùng. Trình khởi chạy cung cấp cho máy chủ `SRW64_CAMPAIGN_DIRS`, `SRW64_CAMPAIGN_SAVES`.
- **Các vấn đề nhỏ đã biết**: Các tùy chọn để trò chơi đọc từ đầu SRAM vào bộ nhớ (âm thanh nổi/đơn âm, dấu giải phóng mặt bằng) và các bản ghi đã xem khi bắt đầu trò chơi sẽ không được đọc lại sau khi chuyển đổi. Lần lưu đầu tiên của chiến dịch sẽ được ghi vào hộp mực chiến dịch từ bộ nhớ.
- **Đã sửa bằng cách**: Tài liệu nơi đặt nút bắt đầu của cấp độ nhỏ/chiến dịch từng là "xóa tên lớp sau phương thức", `body` vẫn là `pointer-events:auto` và toàn bộ màn hình bị chiếm bởi các nhấp chuột; bây giờ chỉ có nút nhận được các nhấp chuột và các mục khác trên màn hình tiêu đề có thể được nhấp vào.

**Máy thật** (`tools/recomp/debug/check_mod.py`, `build/recomp/debug/20261002T033647.970249Z`, tất cả 13 mục đều đạt, hoàn thành trong một quy trình): Tiêu đề bài viết này có "MOD"; có bốn trang quản lý MOD (tập lệnh bổ sung liệt kê hai chiến dịch, nghệ thuật, lời thoại và ngôn ngữ, âm nhạc và giọng nói trong `config/recomp/campaigns`) bằng cả tiếng Trung và tiếng Anh; nhấp vào chiến dịch mẫu → Không thoát khỏi trò chơi, tiêu đề sẽ hiển thị "Bắt đầu chiến dịch"; bắt đầu chiến dịch, chuyển phần mở đầu và lưu nó vào cột đầu tiên của hộp mực (thư viện chiến dịch tạo `cartridge.sram`), chọn mục đầu tiên trên ngã ba, kết thúc A và quay lại tiêu đề; chiến dịch mẫu trong quản lý MOD hiển thị "Đang phát" và "Quay lại bài viết này"; sau khi quay lại bài viết này, cả hai cột của danh sách tải tệp đều trống (ảnh chụp màn hình `main-load-list.png`); nhập lại chiến dịch mẫu, Chương 1 Cột là "Mở đầu: Khởi hành" (`sample-load-list.png`) và tệp được tải để quay lại cảnh sau khi xóa đoạn mở đầu. Khi tôi chạy nó lần đầu tiên, tôi phát hiện ra: Tôi không nhận được SRAM nào từ một chiến dịch mà tôi chưa từng chơi trước đây. Phiên bản gốc chỉ được định dạng khi khởi động và mô-đun lưu trữ được ghi trong trò chơi đã từ chối phát hành. Bây giờ khi nhập, một thẻ trống được định dạng sẽ được phát hành vào thư viện chiến dịch (byte tùy chọn được lấy từ bài viết này).

**Chưa xong**: Lưu trữ các tệp bổ sung (mỗi chiến dịch có thư viện lưu trữ độc lập riêng và tải một chiến dịch khác trong cùng thư viện sẽ vẫn không từ chối đọc tệp). Nút "Bắt đầu" của menu chuông ban đầu trong trận chiến vẫn tuân theo quy trình trò chơi mới của bài viết này (người dùng xác định: không thay đổi).

## 9. Đang được xác minh

- Các kết luận mới nêu trên đều xuất phát từ phân tích tĩnh: việc thay thế tài nguyên, thay thế danh sách số cảnh, ghi dòng ảo và viết lại bản đồ phải được xác minh trên máy thực tế.
- Ý nghĩa cột 2 và cột 4 của chi phí di chuyển; mục đích đầy đủ của bảng số địa hình mặt nước; `3D34` bảng trạng thái `8021E240`.
- Vẽ các khoảng biến không được sử dụng trong tập lệnh gốc.
- Ngoài cảnh "(trước)", việc mượn số cảnh từ các cảnh khác có tác dụng phụ nào không (mục đích của bảng cảnh vũ trụ `D_801DCAD8`).
- Liệu các đường chiến đấu `5813 + 偏移` có thể rơi vào đoạn văn bản mod hay không.