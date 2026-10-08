> **Ngôn ngữ / Language:** [Tiếng Việt](mod-packages.vi.md) · [English](mod-packages.en.md) · [中文](mod-packages.md)

# Gói MOD: định dạng, phụ thuộc, phân loại và phần thưởng thử thách

2026-10-03. Bài viết này tóm tắt hướng MOD được xác định thông qua thảo luận với người dùng. Đó là một thiết kế và chưa được thực hiện (ngoại trừ những phần được đánh dấu là "đã"). Nó thành công với giới hạn phạm vi khi bắt đầu [Lộ trình MOD tích hợp](mod-roadmap.md) "Hiện tại không có MOD bên ngoài nào được kết nối và không có trình tải gói và phần phụ thuộc nào được tạo." Hiện tại nó hỗ trợ người chơi cài đặt các gói MOD của bên thứ ba nhưng chỉ có dữ liệu và không có mã. Để biết thông tin cơ bản hiện có, hãy xem [Chiến dịch tùy chỉnh](custom-campaign.md) (chi phí bổ sung, quản lý MOD, lưu trữ độc lập) và [Giới hạn sửa đổi](../gameplay/upgrade-limits.md) §7 (tệp quy tắc sửa đổi).

## 1. Nguyên tắc xác lập

- **Phiên bản gốc không có trong danh sách MOD**. Cốt truyện và dữ liệu ban đầu chính là trò chơi; MOD chỉ là những thay đổi và nếu không có phạm vi phủ sóng của gói, mọi thứ sẽ chuyển sang ROM.
- **Nội dung tích hợp của chúng tôi được cung cấp theo gói**, được liệt kê bên dưới các gói dành cho người dùng: gói HD `srw64.hd`, bản dịch của chúng tôi. Chúng được đánh dấu là "tích hợp" trong quản lý MOD và không thể xóa được; Gói HD và chuyển đổi chế độ hình ảnh, bản dịch và cài đặt ngôn ngữ.
- **Gói chỉ chứa dữ liệu, không có mã**. Chỉ có thể thực hiện thay đổi quy tắc bằng cách mở quy tắc riêng của máy chủ và điền các tham số (§6). Mã MOD (ngược dòng `.nrm`) sẽ thực sự cần được tạo riêng trong tương lai.
- **Không có kho trực tuyến và tải xuống tự động**. Khi thiếu phần phụ thuộc, hãy cho biết phần nào còn thiếu và người chơi có quyền cài đặt nó.

## 2. Định dạng gói v1

Gói là một thư mục hoặc zip (tiện ích mở rộng `.srw64mod`). Sử dụng thư mục khi tạo, sử dụng zip khi xuất bản, kéo nó vào quản lý MOD và cài đặt vào thư mục người dùng `mods/`.

```text
mod.json
campaign/   追加剧本（现在 campaigns/<id>/ 的内容）
challenge/  单关挑战（§8）
story/      改主线关卡（§7）
data/       数值（§5）
rules.json  打开宿主规则（§6）
art/        美术（§4）
dialogue/   台词与语言
audio/      音乐与语音
```

Chỉ những thư mục cần được sử dụng. `mod.json`:

```json
{
  "schema": "srw64.mod.v1",
  "id": "example.gaiden",
  "version": "1.2.0",
  "name": { "ja": "外伝", "zh-Hans": "外传", "en": "Gaiden" },
  "description": { "zh-Hans": "…" },
  "authors": ["example"],
  "game": ">=0.4",
  "requires": { "example.newpilots": ">=1.0" },
  "optional": { "srw64.hd": ">=1.0" },
  "conflicts": { "someone.oldgaiden": "*" }
}
```

- `id` sẽ không bị thay đổi sau khi phát hành, hãy sử dụng "author.name" để tránh xung đột tên; phiên bản `主.次.修`.
- `game` là yêu cầu về phiên bản máy chủ.
- Sau khi đặt v1, chỉ các trường sẽ được thêm vào, ý nghĩa của các trường hiện có sẽ không bị thay đổi và sẽ báo lỗi đối với các trường không xác định (nghiêm ngặt tương tự như việc sửa đổi tệp quy tắc).

## 3. Phụ thuộc và thứ tự tải

- Ba mối quan hệ: **Bắt buộc** (thiếu không thể kích hoạt, cho biết cái nào còn thiếu và phiên bản nào là bắt buộc), **Tùy chọn** (nếu có sẽ xếp sau, không có thì dùng), **Xung đột** (không thể kích hoạt cùng lúc).
- Mỗi `id` chỉ cài một bản nên chỉ kiểm tra xem phiên bản có hài lòng không và không giải quyết được phiên bản.
- **Tính toán đơn hàng tự động**: các gói phụ thuộc ở dưới cùng và các gói tích hợp ở dưới cùng; người chơi chỉ có thể điều chỉnh thứ tự các gói không liên quan. Phụ thuộc vào vòng lặp để báo cáo lỗi.
- Khi một gói bị vô hiệu hóa, nó sẽ nhắc rằng các gói phụ thuộc vào gói đó sẽ bị vô hiệu hóa cùng nhau.
- Quản lý MOD cộng với danh sách tóm tắt "đã cài đặt": danh mục của từng gói, phụ thuộc, xung đột, số lượng mục được bao gồm và thứ tự. Bốn trang danh mục (Kịch bản/nghệ thuật/dòng bổ sung và ngôn ngữ/âm nhạc và giọng nói) liệt kê các gói có chứa nội dung thuộc loại này.
- **Xác minh trước khi bắt đầu**: Các công cụ và máy chủ Python chia sẻ một bộ quy tắc, các gói lỗi không được bật và các lỗi được báo cáo với các tệp, trường và lý do.

## 4. Kiểu hiển thị: lớp phủ nút

Thứ tự là phiên bản gốc → gói tích hợp → gói người dùng (theo thứ tự §3) → sửa đổi của chính người chơi trong thư mục người dùng; người đứng sau cùng một khóa sẽ thắng và khóa không được cung cấp sẽ được tìm thấy ở lớp bên dưới.

| nội dung | chìa khóa |
| --- | --- |
| Hình đại diện | Số bảng màu tài nguyên hình ảnh |
| Tranh ba chiều trên cơ thể | Cảnh-Atlas-Bảng màu |
| Bản đồ chiến thuật | Số bản đồ (toàn tờ) |
| Hình nền và cốt truyện | Số tài nguyên |
| Các biểu tượng, bản đồ thế giới, đường viền, v.v. Họa tiết RT64 | Băm kết cấu; thư viện thời gian chạy tải nhiều thư mục thay thế theo thứ tự và những thư mục sau sẽ ghi đè lên những thư mục trước đó |
| Dòng | Số bản ghi (`@17410`), tức là phương thức ghi đè thư mục người dùng hiện tại được mở rộng thành nhiều lớp |
| Âm nhạc | Số theo dõi |
| Âm mưu, giọng nói chiến đấu | Số bản ghi dòng; Số dòng chiến đấu |

Các tài nguyên mới được thêm vào (không phải tài nguyên ban đầu) có tên gói, chẳng hạn như `example.newpilots:portraits/ryu.png`, sẽ không bao gồm nhau; các gói khác sử dụng tên này để tham chiếu đến nó, đó là mục đích chính của sự phụ thuộc.

Hiện tại tất cả các loại mã tải chỉ nhận dạng một `hd/`. Nó cần phải được thay đổi để hợp nhất tất cả các gói thành một bảng "khóa → tệp" theo thứ tự, sau đó chuyển nó cho mã bản vẽ. Công cụ hỗ trợ xuất: Xuất ảnh gốc và ảnh HD theo thể loại, tên file là key.

## 5. Lớp số

Các bảng có thể thay đổi đã được phân tích cú pháp ([thư mục dữ liệu gốc](../data/original-data-catalog.md)): 363 máy bay, 1329 vũ khí, 361 ký tự (257 hồ sơ khả năng, ngưỡng kỹ năng, tiếp thu tinh thần), mức tăng và giá sửa đổi, giới hạn trên của việc sửa đổi máy bay và các loại sửa đổi vũ khí.

```json
// data/units.json：按机体号逐字段覆盖，没写的保持原版
{ "36":  { "hp": 4500, "armor": 1300, "upgrade_cap": 12 } }
// data/weapons.json
{ "160": { "power": 2600, "upgrade_type": 2 } }
// data/pilots.json：按人物号
{ "28":  { "skills": { "NT": [1,4,8,12,18,24,30,38,45] }, "spirits": ["熱血", "必中", "ひらめき"] } }
// data/rules.json：批量规则，逐条覆盖优先
[{ "select": { "faction": "enemy" }, "set": { "hp": "×1.3", "armor": "+200" } }]
```

- **Phương pháp hiệu quả**: Máy chủ thay đổi byte tương ứng của dữ liệu ROM trong tay trước khi bắt đầu trò chơi. Logic ban đầu, trang trạng thái của chúng tôi và trang sửa đổi, sách minh họa và trình xem trận chiến đọc cùng một số và sẽ không có "một số trên giao diện, một số khác trên phần giải quyết". Tệp quy tắc chuyển đổi (`srw64.upgrade-rules.v1`, hiện có) được hợp nhất không thay đổi thành `data/`.
- **Thời gian hiệu quả được đánh dấu theo trường**, hiển thị trong quản lý MOD:
- Mỗi lần đọc hiện tại: giá trị cơ bản của nội dung (khả năng được tính toán lại `800A5254` mỗi lần đọc lại từ bản ghi ROM) và kho lưu trữ cũ có hiệu lực ngay lập tức;
- Sao chép một lần khi tạo vũ khí mới: loại sửa đổi vũ khí (`800A6A98` chỉ được sao chép khi tạo phiên bản vũ khí) và những loại hiện có trong danh sách không thay đổi;
- Cần được xác minh: Khả năng của phi công có được tải và tính toán lại hay được lưu trữ trong kho lưu trữ hay không.
- **Bản ghi chung**: Nhiều nhân vật chia sẻ một bản ghi khả năng và việc thay đổi một bản ghi sẽ ảnh hưởng đến những nhân vật khác. Công cụ chỉnh sửa sẽ nhắc người đồng chia sẻ; nếu một người thực hiện sửa đổi một mình, anh ta cần thay đổi ánh xạ của mình sang một bản ghi khác và cần phải kiểm tra xem có bao nhiêu bản ghi trống.
- **Công cụ chỉnh sửa**: Thêm "Thay đổi mục này" vào trang duyệt dữ liệu/sách ảnh gốc và xuất nó sang `data/*.json`. Người chơi bình thường không cần phải viết số bằng tay.

Chấp nhận: Thay đổi cơ thể, vũ khí và trường thí điểm, đồng thời kiểm tra xem trang trạng thái ban đầu, trang của chúng tôi, giải quyết trận chiến thực tế cũng như các tệp lưu và tải đều nhất quán.

## 6. Lớp quy tắc

Các thay đổi logic như hệ số kinh nghiệm, hệ số quỹ và tiền thưởng cấp độ kẻ thù được máy chủ triển khai thành các quy tắc (sử dụng [quy tắc tùy chọn] hiện có (../gameplay/rule-fixes.md)). `rules.json` trong gói chỉ có nhiệm vụ mở và đưa ra thông số. Các gói không thể mang lại logic mới.

## 7. Drama: Thay đổi cốt truyện chính

Nhấn **event** để thay đổi, không nhấn toàn bộ cấp độ:

- **Sự kiện bổ sung**: Các sự kiện được thêm bởi một số gói ở cùng cấp độ có thể được hợp nhất; nếu vượt quá hơn 63 sự kiện cho mỗi cấp độ, lỗi 0x1A00 byte sẽ được báo cáo.
- **Thay thế/Xóa sự kiện gốc**: Khi hai gói di chuyển cùng một sự kiện, gói sau sẽ có hiệu lực theo thứ tự và sẽ xuất hiện xung đột.
- **Triển khai tấn công**: Thay đổi theo số bản ghi (thay đổi nội dung, thay đổi cấp độ).
- Các sự kiện chưa được thay đổi, hãy sử dụng `copy_from: base:stage_events:*` để tham chiếu phiên bản gốc và các tập lệnh lấy ra khỏi ROM sẽ không được bao gồm trong gói.

Ví dụ: "Cho phép một kẻ thù nhất định tham gia" = Thêm một sự kiện vào một cấp độ nhất định và đăng ký nó trong `3D5A 机师,0,机体,500` khi đáp ứng các điều kiện; đồng thời thêm tinh thần và kỹ năng của người đó vào `data/`, đồng thời thêm giới hạn trên của sửa đổi cơ thể và loại sửa đổi vũ khí. Đang chờ máy thực tế: giới hạn danh sách (140 trường hợp máy), biểu tượng bản đồ (bao gồm biểu tượng HD) sau khi máy địch bị thay thế bởi trại của chúng tôi và danh sách のりかえ.

Mã bổ sung (`campaign/`) vẫn nhấp vào [Chiến dịch tùy chỉnh](custom-campaign.md): hoàn thành các cấp độ, mượn số cảnh và lưu độc lập.

## 8. Thử thách và phần thưởng cấp độ đơn

Thử thách là cấp độ nhỏ với đội quân được cài sẵn và kết quả như số vòng đấu sẽ được hiển thị sau khi trò chơi hoàn thành. Phần thưởng có thể được đưa trở lại dòng chính.

### 8.1 Hai cách vào

- **Hộp thưởng thử thách độc lập (làm trước)**: Nhập từ tiêu đề hoặc quản lý MOD, với quân cài sẵn, độc lập với tuyến chính. Sau khi vượt qua cấp độ, phần thưởng sẽ được đưa vào hộp phần thưởng; Khi chơi tuyến chính và vào liên game, menu liên game sẽ nhắc "Có phần thưởng thử thách để nhận", sau khi nhận sẽ được ghi vào game hiện tại. Phần thưởng hoàn thành cấp độ cho các chi phí bổ sung cũng được chuyển vào hộp phần thưởng tương tự.
- **Vào từ sân (chơi sau)**: Giống như cấp độ DLC của Machine Combat V/X/T, sử dụng quân hiện tại để chiến đấu và quay lại sân sau trận đấu, tiền, kinh nghiệm và các bộ phận sẽ tự nhiên bị bỏ lại. Trước khi bước vào thử thách, người dẫn chương trình ghi lại diễn biến của câu chuyện chính (số từ `8010F5EF`, cảnh `F5F0`–`F5F2`, tổng vòng `F5EC`, các biến 100–114 và 128–139 sẽ được đặt lại khi bắt đầu cấp độ) và phục hồi sau khi hoàn thành thử thách. Những gì sẽ thay đổi trong quy trình thông quan (`3D4A`) trước tiên phải được xác minh trên máy thực tế và không được bỏ sót một mặt hàng nào.

### 8.2 Phần thưởng có thể được trao (người dùng quyết định vào ngày 2026-10-03: chỉ đưa ra ba loại này)

| Phần thưởng | Viết ở đâu | Lưu ý |
| --- | --- | --- |
| Quỹ | `D_8010F5F4` (u32) | Tiền có thể được thay đổi trực tiếp trên màn hình liên trường |
| Các bộ phận nâng cao | Hàng tồn kho `D_8015E990`, mỗi phần có một u16, số giữ byte cao, số giữ byte thấp | Số giữ là một byte, hãy kiểm tra giới hạn trên trước khi thêm |
| Giai đoạn chuyển đổi, cấp độ/kinh nghiệm thí điểm | Phiên bản khung máy bay `D_8016A210` (140 × 0x54) `+0x4C..+0x50` Năm giai đoạn, phiên bản vũ khí `+0x16`; Hồ sơ phi công `80172F40` (0x4C một) cấp độ `+0x05`, `+0x12` kinh nghiệm | Sau khi thay đổi số lượng phân đoạn, khả năng có thể được tính toán lại thành `800A5254`, sẽ không vượt quá giới hạn trên của thân máy `+0x51`. Việc thay đổi cấp độ sẽ không tự động tăng khả năng. Bạn cần tuân theo quy trình tăng trưởng ban đầu (chu kỳ tăng trưởng `800A6238`). Phương thức gọi cụ thể cần được xác minh; đầu tiên làm kinh nghiệm hoặc số giai đoạn |

Không có khung máy bay/phi công nào được phép tham gia nhóm và không được phép thay đổi cốt truyện hoặc các yếu tố ẩn (điều này sẽ làm gián đoạn việc phán đoán tuyến đường chính).

### 8.3 Quy tắc

- Phần thưởng được ghi bằng `mod.json` của gói thử thách và được hiển thị trước khi trò chơi bắt đầu.
- **Chỉ thay đổi bộ nhớ, không thay đổi tệp lưu trữ**: Máy chủ ghi bộ nhớ giữa các cảnh và người chơi lưu nó như bình thường; phiên bản gốc vẫn chịu trách nhiệm về định dạng lưu trữ và xác minh.
- **Mỗi thử thách chỉ có thể được xác nhận một lần cho mỗi lần lưu dòng chính** và bản ghi xác nhận quyền sở hữu được đặt bên cạnh tệp lưu cùng với thông tin bổ sung. `saves/` Thư viện đã có tệp thông tin bổ sung nhưng cột băng cassette thì không. Nó cần phải được lấp đầy. Ngoài ra còn có "Cho phép thu thập lặp lại" trong cài đặt, tính năng này bị tắt theo mặc định.
- Đối với các kho lưu trữ đã nhận được phần thưởng, hãy ghi lại nguồn trong thông tin bổ sung và đặt chúng cùng với các bản ghi MOD trò chơi (§9).

## 9. Lưu trữ

- Thông tin bổ sung về kho lưu trữ dòng chính ghi lại các lớp số, lớp quy tắc được kích hoạt tại thời điểm đó, các gói và phiên bản của các thay đổi của dòng chính, cũng như phần thưởng thử thách nhận được. Nếu không thể đọc được tệp, một lời nhắc nhở về sự khác biệt sẽ được liệt kê, nhưng tệp vẫn sẽ được đọc (việc cài đặt bản vá cân bằng giữa chừng là điều bình thường).
- Hạng mục ngoại hình không được ghi lại.
- Sử dụng các kho lưu trữ riêng cho các tập lệnh bổ sung và các thử thách độc lập (phương pháp phân tách hiện có).

## 10. Trình tự

1. Định dạng gói v1, thư mục `mods/`, kiểm tra phụ thuộc và trang "Đã cài đặt"; di chuyển chiến dịch mẫu, gói HD và tệp quy tắc chuyển đổi thành các gói.
2. Chấp nhận các lớp số (bao gồm cả quy tắc hàng loạt) và §5.
3. Chuyển đổi quy tắc.
4. Thử thách độc lập cộng với hộp phần thưởng (quỹ, bộ phận, cấp độ/kinh nghiệm).
5. Xuất hiện các công cụ xuất và lớp phủ nhiều lớp; lồng tiếng và thay thế BGM.
6. Thay đổi sửa đổi cấp độ sự kiện của cốt truyện chính; bước vào thử thách từ giai đoạn can thiệp.
7. Bản đồ mới, nhân vật mới và máy bay mới (chiến dịch tùy chỉnh C3, C4).

## 11. Cần được xác minh

- Khả năng của phi công có được tính toán lại khi tải tệp hoặc được lưu trữ trong kho lưu trữ hay không (xác định xem giá trị MOD có hiệu lực trên kho lưu trữ cũ hay không).
- Có thể được sử dụng để thay đổi riêng số lượng bản ghi khả năng nhàn rỗi mà một người có.
- Cách sử dụng quy trình tăng trưởng ban đầu khi thay đổi cấp độ thí điểm.
- Tất cả các trường tiến trình chính đã được thay đổi trong quá trình vượt qua (để tham gia các thử thách giữa các trò chơi).
- Danh sách các biểu tượng trại và のりかえ sau khi máy của kẻ thù được thêm vào.

## 12. Phương pháp tham khảo

| Sinh thái | Gói và phụ thuộc | Tham khảo |
| --- | --- | --- |
| N64Recomp (Zelda64Recomp, v.v.) | `.nrm` zip `mod.json`, `id:版本` danh sách được chia thành bắt buộc và tùy chọn | Thư viện thời gian chạy giống nhau, tên trường giống nhau |
| Yếu tố | `info.json`, mỗi dòng một dòng: `base >= 1.1`, `? 可选`, `! 冲突` | Tùy thuộc vào sự phân chia của ba mối quan hệ |
| RimWorld | `About.xml`: `modDependencies` được tách khỏi `loadAfter`/`loadBefore` | "Phụ thuộc" được tách ra khỏi "Chỉ ảnh hưởng đến trật tự" |
| Thung lũng Stardew SMAPI | `manifest.json`: `UniqueID`, `MinimumVersion`, `IsRequired` | Khi thiếu phần phụ thuộc, hãy nêu rõ phần nào bị thiếu và phiên bản nào là bắt buộc |
| Bethesda (The Elder Scrolls, Fallout) | Thứ tự của các plug-in được người chơi sắp xếp thủ công và được khắc phục bằng các công cụ của bên thứ ba như LOOT | Ví dụ tiêu cực: thứ tự được tính toán tự động bởi các phụ thuộc |
| RimWorld, Bethesda đang tải tập tin | Lưu trữ danh sách MOD bản ghi, nhắc nhở so sánh khi tải file | Lưu trữ hồ sơ của §9 |