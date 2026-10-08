> **Ngôn ngữ / Language:** [Tiếng Việt](ui-layout-audit.vi.md) · [English](ui-layout-audit.en.md) · [中文](ui-layout-audit.md)

# Kiểm tra ngoại tuyến bố cục giao diện

Ngày: 29-09-2026. Không cần khởi động trò chơi hoặc đọc ROM và chạy nó, bạn cũng có thể kiểm tra xem văn bản trong giao diện dùng chung (màn hình liên trò chơi được vẽ bởi `src/native/ui/frontend.cpp`, xác nhận trước trận chiến, menu tiêu đề, cửa sổ cài đặt, trang liên kết) có vượt quá khung và đường khung có mở rộng ra ngoài khung ở từng ngôn ngữ và từng kích thước cửa sổ hay không.

```bash
.venv/bin/python tools/recomp/ui_audit/run_audit.py                 # 四种尺寸 × 三种语言，约 3 分钟
.venv/bin/python tools/recomp/ui_audit/run_audit.py --sizes deck --only 'zh-Hans$'
```

Điều kiện tiên quyết: Đã có bản dựng máy chủ đồ họa (`build/recomp/gfx-build`, sử dụng các tham số biên dịch và RmlUi, RT64, thư viện tĩnh Plume) và phông chữ trong `build/fonts`, đồng thời có `rom.z64` (bảng văn bản chỉ đọc) cục bộ. Khi chạy sẽ mở một cửa sổ nhỏ để vẽ trang, không chạm vào kho lưu trữ và không khởi động máy chủ nên sẽ không xảy ra xung đột với máy chủ của các phiên khác.

## Luyện tập

- [`layout_audit.cpp`](../../tools/recomp/ui_audit/layout_audit.cpp) liên kết `frontend.cpp` thực, thư mục ngôn ngữ và trình kết xuất RmlUi; bộ điều hợp trang (`battle_page::state()`, v.v.), cài đặt và trạng thái bộ điều khiển ở phía trò chơi được thay thế bằng hình đại diện và trạng thái trang trong lịch thi đấu được trả về trực tiếp. Sau mỗi thiết bị sắp chữ một vài khung hình, hãy chụp ảnh màn hình rồi duyệt qua các phần tử:
- `text-past-box`/`text-past-item`: Văn bản không ngắt dòng vượt quá khối hoặc khối nội tuyến hoặc mục linh hoạt.
- `run-wider-than-block`: Trong văn bản sẽ ngắt dòng, phần giữa hai dấu cách rộng hơn khối. RmlUi chỉ ngắt dòng ở khoảng trắng và các câu tiếng Trung và tiếng Nhật dài bị tràn (xem [RmlUi ngắt dòng bằng tiếng Trung và tiếng Nhật](../native/settings-window.md)).
- `box-past-parent`: Hộp có viền mở rộng ra ngoài đường viền của phần tử cha, ví dụ dải phân cách dài hơn khung bên ngoài.
- `text-clipped`/`text-cut-below`: Một dòng văn bản vượt quá cạnh phải của bảng nơi bị cắt hoặc quá một nửa nằm ngoài cạnh dưới của bảng (dòng này tương đương với việc bị mất).
- `text-overlap`: Hai lưới được định vị tuyệt đối trong cùng một bảng ép vào nhau. Chiều rộng lưới của trang 320×240 ban đầu tuân theo văn bản và nó sẽ không tràn mà chỉ chạm vào lưới liền kề. Các dòng đã được nén theo chiều ngang (`transform`) và các số được đặt theo lưới trên trang gốc trước chiến tranh có độ phân giải cao theo nhóm số ban đầu không được đưa vào so sánh; các từ trong hộp định vị tuyệt đối có màu nền (hộp lựa chọn đánh giá cao khả năng chiến đấu `#vw-pop`) trên trang chỉ được so sánh với các từ trong hộp.
- `nowrap` Kích thước của văn bản như khi sắp chữ: các khoảng trắng liên tiếp được tính là một (dấu nhắc phím "Chọn · ..." sẽ tăng kích thước ban đầu lên 36 dp). Danh sách chỉ cuộn theo chiều dọc (`overflow-y:auto`) cũng được coi là bảng cắt xén và việc cuộn ra một nửa số dòng không tính các từ nằm ngoài danh sách.
- Sai số nhỏ hơn 1,2 dp sẽ được coi là sai số làm tròn và không được báo cáo; sự trùng lặp trong vòng 3 dp sẽ không được báo cáo nếu các cạnh bên ngoài của hình chạm vào nhau.
- [`run_audit.py`](../../tools/recomp/ui_audit/run_audit.py) Biên dịch bằng cách sử dụng các tham số của lệnh biên dịch `frontend.cpp` trong bản dựng máy chủ. Chỉ biên dịch lại sau khi tệp nguồn hoặc tệp tiêu đề được cập nhật. Lịch thi đấu đến từ [`states.json`](../../tools/recomp/ui_audit/states.json): Kiểm tra trang liên trường 9-23, kiểm tra menu tiêu đề 9-24, kiểm tra xác nhận trước chiến tranh 9-28 và trạng thái trang được ghi lại (đường dẫn hình ảnh đã bị xóa, không ảnh hưởng đến bố cục văn bản). Mỗi chuỗi được trả về số bản ghi thông qua bảng văn bản ROM, sau đó được đổi thành ký tự tiếng Trung, tiếng Anh và tiếng Nhật; khi màn hình đã sửa đổi và danh sách bài hát không được ghi lại, chúng sẽ được đánh vần theo các trường `upgrade_page.cpp` và `title_page.cpp`. Cộng với trường hợp xấu nhất: 7 tên máy bay rộng nhất, tên phi công, tên danh sách vũ khí, tên cấp độ, sát thương 4 chữ số và 5 chữ số, và 99999 HP được đo bằng phông chữ thực tế.
- Đánh giá chiến đấu: Với vật cố định `clicks` (nhấn điều khiển điểm id, cùng đường dẫn với `srw64_click` của giao diện gỡ lỗi), mở toàn bộ trang từ trang "Chung" `viewer-open`, sau đó nhấp vào từng ô của khung máy bay, phi công, vũ khí, vũ khí phản công, kết quả, cảnh và BGM của cả hai bên. Dữ liệu minh họa (`library::contents()`) được đánh vần từ `run_audit.py` theo các trường của `library.cpp`: đối với máy bay 0 (`battle_viewer_pilots.inc` có số lượng hành khách lớn nhất, 13 người), đối với máy bay 28, tên, mẫu, tên công việc, kỹ năng và tên vũ khí đều rộng nhất; các bản nhạc được lấy từ bản ghi ROM 232–280. Hình thu nhỏ và hình đại diện của cảnh không được vẽ (hình đại diện sẽ trống).
- Kích thước: `deck` 1280×800 điểm, kích thước giao diện "cực lớn" (Mặc định Steam Deck, cũng là cơ sở để xác định kích thước phông chữ); `deck-standard` giống với cửa sổ "tiêu chuẩn"; `wide` 1920×1080; `smallest` 960×720; `deck-4:3` giống `deck` nhưng tỷ lệ màn hình là 4:3 (trang chỉ được sắp chữ ở màn hình 1067×800, tên thư mục `deck-4x3`). Ảnh chụp màn hình và `audit.json` trong `build/recomp/ui-audit/<尺寸>/`.
- Thoát mã 1 khi có sự cố.
- Báo cáo viết tắt: lớp `fit` sẽ ghi lại cỡ chữ gốc (`data-fit-from`) trên phần tử khi nó làm giảm phần văn bản không vừa. Quá trình kiểm tra sẽ ghi từng phần tử viết tắt cùng với kích thước phông chữ ban đầu, kích thước phông chữ hiện tại, tỷ lệ và văn bản vào `shrunk` của `audit.json` và `run_audit.py` sẽ liệt kê các mục bên dưới theo thứ tự tỷ lệ tăng dần. Giá trị của `--shrunk` (mặc định là 0,85). Việc giảm ký tự không được coi là thất bại - `fit` được sử dụng để giảm - nhưng các dòng bị giảm nghiêm trọng nhất cho biết nơi kích thước phông chữ được đặt thành lớn hơn và cột nào được đặt thành hẹp hơn. Hãy xem nó trước khi thay đổi kích thước phông chữ. `--shrunk 1` liệt kê tất cả, `--shrunk 0` thì không.

## Lớp phủ văn bản màn hình gốc

Khả năng của máy bay, khả năng của phi công, danh sách vũ khí, menu lệnh, v.v. của bản đồ chiến thuật là màn hình gốc và văn bản được bao phủ bởi [`ui_text.cpp`](../../src/host/ui_text.cpp) ([Lớp phủ văn bản giao diện gốc](../native/native-ui-text.md)). Quy tắc về độ rộng hàng của nó là nhất định, vì vậy [`overlay_fit.py`](../../tools/recomp/ui_audit/overlay_fit.py) có thể đánh giá tất cả văn bản dữ liệu (bản ghi 0–5643) ngoại tuyến:

```bash
.venv/bin/python tools/recomp/ui_audit/overlay_fit.py                # 中英日；中文有「一定放不下」时退出码 1
```

- Chiều rộng ban đầu được tính theo định dạng phông chữ ROM: mã 0 và 0x13B trở xuống là 8 hẹp, còn lại là rộng 14. Chiều rộng ban đầu có thể được sử dụng để dịch và tối đa 1,35 lần + 4 được sử dụng khi không có gì đằng sau nó; đầu tiên hãy thu hẹp nó (70% đối với tiếng Trung và tiếng Nhật, 80% đối với tiếng Anh), sau đó giảm tối đa xuống còn 1,5 điểm.
- `overflows`: Không thể đặt được ngay cả khi mặt sau trống; `depends`: Chỉ có thể đặt nó khi không có bất kỳ mục nào khác theo sau.
- Các dòng chứa nhiều hơn hai khoảng trắng liên tiếp (để chừa khoảng trống cho số) có thể đặt theo từng đoạn hoặc có thể đặt số sau khi di chuyển chúng vào toàn bộ câu, phù hợp với cách tiếp cận của `ui_text`.
- Tiếng Nhật là nhóm đối chứng: văn bản ROM hiển thị đúng quy định và kết quả là 0.
- Chúng ta chỉ biết chiều rộng của mỗi bản ghi chứ không biết những gì theo cùng một dòng; mục nhập `depends` tùy thuộc vào màn hình cụ thể.

## Không được che chắn

- Không tìm thấy hộp thoại, thanh dưới cùng (`dialogue_scene.cpp`) và huy hiệu HUD trong RmlUi và không thể tìm thấy ở đây; chúng được kiểm tra bằng máy thực tế (`check_dialogue.py`, `check_ui_text.py`). Lớp phủ hình ảnh gốc chỉ có thể được đánh giá bằng các bản ghi, xem phần trước.
- Trang tên có thăm dò riêng (`srw64-ui-probe`).
- Chỉ kiểm tra tràn theo phương ngang; hộp nội tuyến cao hơn một chút so với chiều cao hàng (hàng danh sách 16 đơn vị) là rất phổ biến và không thể nhìn thấy nên không được báo cáo.
- Trận đấu là trạng thái được ghi lại cộng với trường hợp xấu nhất chứ không phải toàn bộ trạng thái của trận đấu; đối với các trang mới hoặc trường mới, trạng thái phải được thêm vào `states.json` hoặc được đánh vần bằng `run_audit.py`.

##2026-09-29 Đã sửa chữa trong lần kiểm tra đầu tiên

Hai lần chạy sau khi kiểm tra video bộ bài (hiện có kích thước 159 trang × 4, cộng với kiểm tra lớp phủ) đã được tìm thấy và cắt bớt:

| Trang | Câu hỏi | Thay đổi luật |
| --- | --- | --- |
| Khẳng định trước chiến tranh (phiên bản mới) | Nhấn "100/100" ở bên phải bảng điều khiển để giữ "SP" | Hai lưới sức mạnh và SP được chia thành các chiều rộng tùy theo nội dung, để lại khoảng cách 6 dp trong lưới |
| Xác nhận trước trận chiến (phiên bản mới) | Sát thương 4 chữ số (chẳng hạn như 2390) vượt quá 11 dp ở nửa cột giữa và tập trung cùng với các mũi tên và "kẻ tấn công đầu tiên của kẻ thù" | Số 4 chữ số và 5 chữ số giảm cỡ chữ theo chữ số |
| Xác nhận trước chiến tranh (phiên bản mới, phiên bản gốc độ nét cao) | Tên máy dài tiếng Anh và tiếng Nhật, tên vũ khí và dòng điều kiện phòng thủ bị cắt ngắn | Lớp `fit` phổ quát: Sau khi sắp chữ, phần văn bản thừa được giảm tương ứng, lên tới 60% |
| Sửa đổi vũ khí, hiệu suất vũ khí | Tên vũ khí dài được cắt ngắn theo chiều rộng cột, cùng với biểu tượng P/B/MAP phía sau | Tên bị giới hạn ở chiều rộng mà biểu tượng để lại và được giảm `fit` (tối đa 50%) |
| Mỗi trang danh sách giữa các trường | Đường phân chia của hàng "Elf" và "Pilot" ở phía dưới dài hơn khung bên ngoài khoảng 2,5 pixel gốc | Hàng này được đổi thành `box-sizing:border-box` |
| Tiêu đề "Tùy chọn" | "Âm thanh nổi" vượt quá cột giá trị 7 dp | Tên và giá trị phải có kích thước phông chữ theo độ rộng cột riêng của chúng |
| 320×240 trang giữa các trường | Tên dài và nhãn tiếng Anh và tiếng Nhật bị cắt ngắn | Các ô `span()` của các trang này đều có `fit` |
| Khả năng cơ thể (giữa các lĩnh vực) | Khả năng đặc biệt được xếp thành một dòng và chỉ có thể xếp thành hai dòng. Cái thứ ba của loại mecha này có ba khả năng (biến hình, nhân bản và rào chắn Aura) đã bị cắt | Theo phiên bản gốc, nó được sắp xếp theo chiều ngang từ (25,188) và không thể đặt ở dòng tiếp theo; khi có nhiều hơn hai dòng, toàn bộ cỡ chữ của cột và chiều cao của dòng đều giảm cùng nhau |
| Khả năng cơ thể (giữa các lĩnh vực) | Loại chuyển động tiếng Anh được viết là "LndAirSea" | Tiếng Anh được phân tách bằng "/" và cột được giảm bớt `fit` |
| Khả năng phi công (liên lĩnh vực) | Kỹ năng tiếng Anh "Thánh chiến binh L3" và tinh thần Nhật Bản "ひらめき" bị cắt khỏi bảng; người Nhật "レベル" trấn áp đẳng cấp | Lưới tinh thần và kỹ năng được cung cấp chiều rộng theo lưới ban đầu (cột cuối cùng của tinh thần chỉ là 36) và chiều rộng nhãn bị giới hạn, cả hai đều có `fit` |
| Giải thích lệnh phản công (màn hình gốc) | Chia một câu thành ba bản ghi. Trong tiếng Trung, hãy đặt “tránh hoặc phòng thủ” vào đoạn văn ban đầu chỉ rộng “檒し”. Điều tương tự cũng đúng trong tiếng Anh | Phân phối lại ba đoạn: "Tránh hoặc phòng thủ khi cấp độ của kẻ thù thấp hơn mình", "Nếu không" và "Phản công". |
| Tên địa hình (màn hình gốc) | "Pháo đài Baruch" không thể vừa với "バルジ" trong lưới | Tên địa hình là "Baruch" ("Pháo đài Baruch" trong các dòng không thay đổi) |

`fit` được xử lý thống nhất trong `document()` của `frontend.cpp` (`fit_lines`): các phần tử không đủ rộng sau khi sắp chữ sẽ bị giảm kích thước tương ứng và được xem lại trong hàng linh hoạt; các phần tử có thể sử dụng `data-fit-min` để đặt giới hạn dưới của riêng chúng.

## 2026-09-30 Điều chỉnh theo báo cáo viết tắt

Nhìn vào báo cáo viết tắt dựa trên Deck (1280×800, cực lớn), tình hình tên máy và tên vũ khí: Tiếng Trung duy trì ít nhất 88% cỡ chữ gốc trên tất cả các trang (hẹp nhất là "Double Burning Flame (Great Demon sản xuất hàng loạt)" trong danh sách vũ khí), tiếng Anh là 75% (danh sách vũ khí "Pháo hạt tích điện tập trung", danh sách thí điểm "Byston Well Soldier"), phông chữ tiếng Nhật có chiều rộng đầy đủ và ROM Kana là một nửa chiều rộng và 21 ký tự "ダブルバーニングファイヤー (マジンガー)" trong danh sách vũ khí chỉ chiếm 57% (giới hạn dưới 50%), chưa được xử lý. Đã thay đổi:

| Trang | Câu hỏi | Thay đổi luật |
| --- | --- | --- |
| Mỗi trang danh sách giữa các trường (chuyển giao, khả năng, phần nâng cao, sửa đổi, lưu trữ) | Tên được rút gọn chỉ để điền vào cột riêng và được kết nối với cột bên phải: "Byston Well Soldier Wing (dạng chim)" "Byston Well SoldierHP" | Ô tên không có lớp nhường 4 đơn vị ở lề phải (`span()`), `fit` được giảm bớt theo chiều rộng còn lại; ô nhãn và ô số căn phải không thay đổi |
| Xác nhận trước trận chiến (phiên bản mới) | Sát thương 5 chữ số trên Bộ bài chỉ là 31 dp, 4 chữ số là 38 dp, để trống 22 dp ở hai bên cột giữa | Lề trong bên trái và bên phải của phiên bản hẹp (<1000 dp) của hộp thiệt hại là 22→14 dp, 36 dp 5 chữ số, 4 chữ số 42 dp; phiên bản rộng 5 chữ số 36→42 dp; các số cũng có `fit`, nếu độ rộng số của phông chữ khác nhau thì chỉ co lại chứ không tràn |
| Tất cả các trang 320×240 trong trường (menu, chuyển đổi, phần nâng cao, chuyển giao, lưu trữ, khả năng) | Ảnh chụp màn hình người dùng xem danh sách chuyển: cỡ chữ cơ bản quá lớn | Toàn bộ dòng đã được giảm đi một kích thước: các hàng danh sách và nhãn nội tuyến được hợp nhất `face`=10,5 đơn vị (11,5 ban đầu, nhãn vẫn có thể đạt tới 12,5) và các bảng khác 12→11, 11,5→10,5, 11→10, `fit` Giới hạn trên là 12,5→11,5; danh sách vũ khí và thanh khả năng ban đầu là 10,5 không thay đổi |

## 2026-10-04 Trang đánh giá trận chiến đã được kiểm duyệt.

`frontend.cpp` Các chức năng máy chủ mới được sử dụng (đánh giá chiến đấu, sách ảnh, chuyển đổi MOD, thư mục ghi đè dòng, chờ tiêu đề) đã được thay thế trong `layout_audit.cpp` và quá trình kiểm tra có thể được liên kết lại; 27 đồ đạc đánh giá trận chiến (9 màn hình × 3 ngôn ngữ) đã được thêm vào và hiện tại kích thước 204 trang × 4 đều đã được thông qua. Nhân tiện, tôi đã sửa hai kết quả dương tính giả trong quá trình kiểm tra của mình (xem khoảng trắng và danh sách cuộn trong phần "Cách thực hiện").

Đã sửa đổi (cùng ngày): `viewer_sync` và trang minh họa lại được điều chỉnh thành `fit_lines` sau `document()`. Ban đầu, lần vượt qua thứ hai đã tính toán giới hạn thấp hơn 60% từ kích thước phông chữ giảm (tệ nhất là khoảng 36%). `data-fit-from` cũng đã được thay đổi thành kích thước phông chữ giảm và báo cáo viết tắt sẽ bị đánh giá thấp. Bây giờ `fit_lines` có `data-fit-from`, do đó phép tính bắt đầu từ nó và giới hạn dưới tương ứng với nó; lệnh gọi dự phòng tới `viewer_sync` sẽ bị xóa (sau `document()`, chỉ màu nền của `.modal` được thay đổi, không ảnh hưởng đến việc sắp chữ; trang minh họa cần được giữ lại và vùng chi tiết được vẽ lại). Tác dụng phụ: Dòng đầu tiên của hộp thí điểm tiếng Anh/Nhật trên Bộ bài, "Byston Well Soldier", ban đầu được thu nhỏ xuống còn 6,7 dp (52%) và vừa bị loại bỏ, nhưng giờ nó dừng ở mức 13 → 7,8 dp (60%). Dòng có huy hiệu "Hiện hành" vẫn vượt mức 9,0 / 4,6 dp và quá trình kiểm tra đã báo cáo hai vị trí bị cắt bớt văn bản. 10-07 Đã thay đổi để nhường chỗ cho phụ đề: tên của hàng danh sách (`.n`) và phụ đề (`.s`, kỹ năng của phi công) đều được thu hẹp tương ứng với chiều rộng tự nhiên và cả hai đều có `fit`. Tên của hàng này trên Bộ bài là 83%, kỹ năng là 79% và có 0 vấn đề ở mỗi kích cỡ.
