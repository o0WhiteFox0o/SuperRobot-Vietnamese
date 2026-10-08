> **Ngôn ngữ / Language:** [Tiếng Việt](settings-window.vi.md) · [English](settings-window.en.md) · [中文](settings-window.md)

# Cửa sổ cài đặt: Từ phím nóng và menu đến "Tùy chọn"

Ngày: 2026-09-18. **Phiên bản đầu tiên đã được triển khai, xem §6; vào ngày 27-09-2026, nó được đổi thành một bảng phân trang được đặt chồng lên trong trò chơi, xem §7; phần còn lại vẫn đang được lên kế hoạch. ** Hiện tại, những thứ mà người chơi có thể điều chỉnh nằm rải rác trong các phím nóng (hình ảnh F6, ngôn ngữ F7), menu "Quy tắc" trên thanh menu, thông số khởi động và tệp hồ sơ; đã có bảy quy tắc và sẽ có nhiều quy tắc hơn trong tương lai, yêu cầu lối vào tập trung. Bài viết quy định về cơ cấu đầu vào, phân loại, thời gian hiệu lực và yêu cầu nghiệm thu đối với từng hạng mục và việc triển khai cụ thể sẽ được bố trí riêng.

## 1. Kiểm kê hiện trạng

| Lối vào hiện tại | Bảo hiểm | Câu hỏi |
| --- | --- | --- |
| F6 | Hình ảnh gốc / HD | Chỉ chuyển đổi chu kỳ, không thể thấy giá trị hiện tại và giá trị tùy chọn |
| F7 | ja / zh-Hans / en loop | Tương tự như trên |
| Thanh menu "Quy tắc" | Hai loại quy tắc và cài đặt trước, cụ thể là điều chỉnh độ khó và điều chỉnh độ khó, có hiệu lực trong thời gian thực và được ghi lại vào `rules.json` (mục nhập trong quá trình lập kế hoạch đã được thay thế bằng "Tùy chọn" trong §6) | Các mục sẽ dài hơn khi các quy tắc tăng lên mà không có văn bản nhóm và giải thích |
| Thông số khởi động | `--rules`/`--rule-fixes`, `--language`, `--images`, `--resolution-scale`, `--font-size`, v.v. | Chỉ khả dụng khi khởi động, người chơi bình thường sẽ không sử dụng dòng lệnh |
| hồ sơ/cài đặt | `presentation` trong số `play-profile.json` (ngôn ngữ, hình ảnh, model_5600, độ phân giải_scale, cỡ chữ), `rules.json` trong thư mục dùng thử | Chỉnh sửa thủ công, không có giao diện |

## 2. Lối vào và cấu trúc

Thanh menu được thay đổi thành **"Tùy chọn"** một menu cấp cao nhất, với các menu con được cung cấp bên dưới theo danh mục và "Cài đặt..." để mở cửa sổ bật lên. Windows và các menu chia sẻ cùng một mô hình cài đặt và mọi thay đổi trong một mô hình sẽ được phản ánh ngay lập tức trong mô hình kia.

```
选项
├─ 游戏性调整…      规则修正、难度调整（现在的「规则」菜单内容）
├─ 显示…            Original / HD、分辨率缩放、字号、减少闪白
├─ 语言与文本…      界面与剧情语言、阅读速度、已读跳过
├─ 存档…            历史会话、自动保存节点（M1 落地后）
└─ 设置…            打开完整设置窗口（以上分类为标签页）
```

- **"Tùy chọn → Điều chỉnh lối chơi" là con đường được xác định trong vòng này**: Toàn bộ menu "Quy tắc" hiện tại đã được chuyển đến đây và được chia thành hai nhóm: "Chỉnh sửa" (được bật theo mặc định, khắc phục những mâu thuẫn trong phiên bản gốc) và "Điều chỉnh độ khó" (mặc định bị tắt, thay đổi cường độ). Tên nhóm được phân tách bằng các dòng phân chia và các mục mô tả không thể nhấp vào.
- [Sửa chữa cơ bản](../gameplay/base-fixes.md), có hiệu lực theo mặc định và không có công tắc, không vào giao diện cài đặt và chỉ được giải thích trong tài liệu và phần "Giới thiệu".
- Cửa sổ sử dụng các tab để lưu trữ các danh mục giống nhau, mỗi danh mục có mô tả một dòng, giá trị hiện tại, giá trị mặc định và "Khôi phục mặc định".

## 3. Siêu dữ liệu được ghi cho từng cài đặt

Theo cách tiếp cận thư mục quy tắc, cài đặt được xác định là dữ liệu và giao diện được tạo từ dữ liệu đó. Việc thêm một mục mới không làm thay đổi mã UI:

| Lĩnh vực | Mục đích |
| --- | --- |
| id, phân loại | Nhận dạng và phân loại ổn định |
| Loại điều khiển | Chuyển đổi, lựa chọn radio (nhóm loại trừ lẫn nhau của bản gốc/giảm một nửa/đóng), giá trị số, thả xuống |
| Khóa thẻ | Khóa giao diện người dùng của `content/locales/*.json`, phải hoàn chỉnh ba ngôn ngữ (`UI_KEYS` của `profile.py` đã được lấy theo thư mục quy tắc, nếu thiếu một ngôn ngữ, quá trình khởi động sẽ bị từ chối) |
| Giá trị mặc định | Giá trị cho lần khởi động đầu tiên; loại sửa được bật theo mặc định, loại độ khó bị tắt theo mặc định |
| Thời gian có hiệu lực | Ngay lập tức/lần giải quyết tiếp theo/lần xuất hiện tiếp theo/mục nhập tiếp theo/bắt đầu tiếp theo - quy tắc hiện tại là "lần giải quyết tiếp theo" và hình đại diện của ông chủ là "lần xuất hiện tiếp theo". Những khác biệt đó phải được hiển thị trên giao diện |
| Viết vị trí | `rules.json`, cài đặt bản trình bày hoặc hồ sơ |
| Lưu trữ tác động | Có thay đổi trạng thái chơi liên tục hay không; những thay đổi phải được nhập vào danh sách tương thích của kho lưu trữ |

Các nhóm loại trừ lẫn nhau (chẳng hạn như phiên bản gốc của hình đại diện/giảm một nửa/tắt hình đại diện của ông chủ) vẫn có thể là hai công tắc Boolean trong lớp dữ liệu, nhưng giao diện được trình bày dưới dạng một lựa chọn duy nhất, tránh trạng thái hiện tại là "hủy khi cả hai đều được chọn" yêu cầu giải thích.

## 4. Giải pháp kỹ thuật

- Phiên bản đầu tiên tạo **Cửa sổ bật lên AppKit**, nằm trên cùng lớp với mã vạch menu vào thời điểm đó và có thể sử dụng lại trực tiếp các thẻ ngôn ngữ và cơ chế chuyển đổi thời gian thực mà không ảnh hưởng đến kết xuất trò chơi. (Sau này toàn bộ trang đã được đổi thành trang RmlUi, xem cuối bài nhé.)
- Giao diện người dùng lớp phủ trong trò chơi (lớp RT64) được giữ lại cho đến khi cần hoạt động của bộ điều khiển hoặc đa nền tảng; tại thời điểm đó, cài đặt mô hình không thay đổi và chỉ thay đổi lớp trình bày.
- Đặt model trong file header của máy chủ (tương tự `rule_fixes.hpp` và `catalog`). Phía Python tiếp tục rút ra các tham số khởi động và xác minh từ cùng một định nghĩa để đảm bảo cả hai bên sẽ không bị trôi.

## 5. Yêu cầu chấp nhận

- Mỗi danh mục và mỗi điều khiển có tiêu đề và mô tả bằng ba ngôn ngữ; khi chuyển ngôn ngữ thì cửa sổ và menu được vẽ lại cùng lúc (menu đã có cái này thì cửa sổ sẽ sử dụng).
- Các thay đổi được ghi vào tệp tương ứng và được thêm vào nhật ký sự kiện (hiện tại là phương thức `rule-fixes-events.jsonl`) và báo cáo lần chạy có thể khôi phục "cài đặt nào đã được sử dụng cho lần chạy này".
- Cung cấp móc kiểm soát QA: nhấn mục như `rule-control.json` để ghi trạng thái kiểm soát để xác minh chạy giới hạn.
- Các cài đặt trước "Khôi phục về mặc định" và "Bản gốc" được tách riêng: cài đặt trước trở về giá trị mặc định (bật sửa, tắt độ khó), trong khi cài đặt sau là tắt tất cả các hành vi ban đầu.
- Cần xác định rõ trò chơi có bị tạm dừng khi mở cửa sổ hay không; thời điểm các thay đổi có hiệu lực được hiển thị trong §3 và người chơi không thể nghĩ rằng việc chuyển đổi giữa trận chiến sẽ ảnh hưởng đến việc giải quyết lần này.

## 6. Triển khai phiên bản đầu tiên (2026-09-18)

| Phần | Trạng thái |
| --- | --- |
| Thanh menu "Tùy chọn" | Phiên bản đầu tiên: menu con "Điều chỉnh lối chơi" và "Cài đặt..." (⌘,), AppKit. Bây giờ chỉ có mục nhập thanh menu (`macos/app_menu.mm`) được giữ lại. |
| Cửa sổ cài đặt | Phiên bản đầu tiên: quy tắc (nhóm), ba cài đặt trước, lựa chọn radio ngôn ngữ, lựa chọn radio hình ảnh (chuyển sang màu xám khi không có HD), một dòng mô tả cho mỗi nhóm, AppKit. Hiện tại đây là trang cài đặt RmlUi của `src/native/ui/frontend.cpp`, cũng bao gồm hai phiên bản mới/gốc của "Giao diện xác nhận trước chiến tranh" và "Màn hình liên trò chơi" (phiên bản sau được thêm vào ngày 23-09-2026, bao gồm menu chính và màn hình chuyển đổi, đồng thời sẽ có hiệu lực vào lần tiếp theo bạn mở màn hình, ghi `intermission_ui` của `presentation.json`). |
| Đồng bộ hóa | Cửa sổ, menu, F6/F7 và móc QA có cùng trạng thái; cửa sổ đọc lại giá trị hiện tại ở mỗi khung hình và truy xuất tất cả tiêu đề khi ngôn ngữ thay đổi. |
| Đầu vào | Trò chơi không thể nhận dữ liệu nhập từ bàn phím khi cửa sổ đang mở. Đợi cho đến khi tất cả các phím được giải phóng sau khi đóng (`ModalInputRelease`). **Trò chơi không tạm dừng. ** |
| Viết lại | Quy tắc được viết là `rules.json`; ngôn ngữ tuân theo cài đặt bản trình bày ban đầu (được viết là `presentation.json`); màn hình không ghi file và chỉ ảnh hưởng đến lần chạy này. |
| Nguồn nhóm | Mỗi mục trong thư mục quy tắc có `Kind` (`correction`/`difficulty`), từ đó các menu, cửa sổ và bộ sưu tập mặc định được tạo ra; `tests/test_rule_fixes.py` Kiểm tra xem nó có nhất quán với `rule_settings.CORRECTIONS`/`DIFFICULTY` hay không. |
| Móc QA | `SRW64_WINDOW_CONTROL=1`: `settings-control.json` (lược đồ `srw64.settings-control.v1`, `action` dưới dạng `open`/`close`/`press`, `id` dưới dạng `rule:limit-cap`, `preset:rules_defaults`, `locale:zh-Hans`, `images:original`), kết quả và tất cả trạng thái kiểm soát được ghi vào `settings-window-events.jsonl`. |

Đo thực tế (`build/recomp/profile-play/sessions/20260918T023907.954768Z`): Sau khi chọn tiếng Trung trong cửa sổ, ngôn ngữ trò chơi sẽ thay đổi từ ja sang zh-Hans và tiêu đề cửa sổ được đồng bộ hóa sang tiếng Trung; chọn chuyển đổi màn hình kích hoạt Gốc và HD ở VI 638/820 tương ứng (`image-mode-events.jsonl`); "Khôi phục về mặc định" loại bỏ mục độ khó và giữ lại sáu sửa đổi; đóng cửa sổ và thoát bình thường (`native-graphics-run-completed`, mã thoát 0). Để biết số đo thực tế của việc nhóm menu, hãy xem `20260918T023623.862474Z` (tiêu đề ja, "Kế thừa vũ khí" được bao gồm trong nhóm chỉnh sửa).

Chiều rộng cửa sổ tối thiểu phải là 460 điểm và phải được mở rộng theo dòng dài nhất: ba nút mặc định tiếng Anh rộng hơn một dòng so với 460 điểm và nút cuối cùng đã bị cắt; bây giờ chiều rộng được tính toán lại dựa trên nội dung và dòng mặc định (bao gồm cả lề ở cả hai bên) sau khi xây dựng cửa sổ và mỗi lần thay đổi ngôn ngữ (`fit`, 2026-09-18).

Các sự cố đã được khắc phục trong quá trình: các nút radio trong cùng một chế độ xem được AppKit coi là một nhóm, ngôn ngữ và màn hình triệt tiêu lẫn nhau và hiện được đặt trong các vùng chứa độc lập; phiên bản đầu tiên đã gặp sự cố một lần trong lệnh gọi lại thuộc tính cửa sổ của RT64/plume khi thoát (`EXC_BAD_ACCESS`, `CocoaWindow::updateWindowAttributesInternal`), việc phát hành bảng điều khiển đã được thay đổi để hoàn thành đồng bộ trước khi thoát SDL và đại biểu đã bị xóa trước tiên. Nó không xuất hiện lại, nhưng bản thân cuộc gọi lại thuộc về lớp đồ họa và không có sự tái diễn riêng biệt nào để xác nhận nguyên nhân gốc rễ.

Chưa hoàn thành: Hiển thị độ phân giải/kích thước phông chữ của lớp, phân loại lưu trữ và mô tả về thời gian hiệu quả của từng mục riêng lẻ (hiện tại là một dòng cho mỗi nhóm). Xem §7 để biết trang Giới thiệu.

22-09-2026: Giao diện gốc được hợp nhất vào trang SDL/RmlUi biên dịch lại và không có giao diện người dùng phụ thuộc vào hệ thống nào được tạo; phiên bản đầu tiên của các tệp AppKit ở trên (`settings_window_macos.mm`, `rule_menu_macos.mm`, `presentation_settings_macos.mm`, v.v.) đã bị xóa, `src/host/macos/` chỉ giữ lại mục nhập thanh menu ứng dụng `app_menu.mm` và `desktop_macos.mm`.

## 7. Bảng điều khiển lớp phủ phân trang (27-09-2026)

Người dùng 2026-09-25 đã báo cáo rằng trang "Tùy chọn" mờ đục toàn màn hình trông giống như một chương trình trên máy tính để bàn và yêu cầu bảng điều khiển "gọi ra khỏi trò chơi chỉ bằng một cú nhấp chuột" (xem [Bàn phím Steam Deck](../design/steam-deck-controls.md) "Bản sửa đổi giao diện cài đặt"). 27-09-2026 Đặt năm phân trang, bảng lớp phủ và ghi nhớ phân trang cuối cùng, được triển khai trong `settings_sync` của `src/native/ui/frontend.cpp`.

**Giao diện**: Màn hình trò chơi chạy như bình thường, tối màu (đáy trong mờ), có một bảng có cạnh thẳng ở giữa với cùng màu với trang xác nhận trước chiến tranh (Người dùng 2026-09-27: Khung không cần vát cạnh và các tab cũng là hình chữ nhật có cạnh thẳng): Tiêu đề trên cùng và bảy tab (2026-10-01 thêm trang "Lưu trữ", 2026-10-05 Thêm trang "gian lận"), ở giữa là trang hiện tại có thể cuộn và phía dưới là dấu nhắc phím và "Đóng". Kích thước logic của giao diện không nhỏ hơn 960×720 dp (khi kích thước giao diện được phóng to, nó không nhỏ hơn 800×540 dp, xem bên dưới), bảng điều khiển chiếm 88%, chiều rộng tối đa là 1040 dp và cửa sổ được chia tỷ lệ với nhau khi chia tỷ lệ. **Trò chơi không tạm dừng**, đầu vào vẫn bị chặn bởi `ModalInputRelease`.

| Trang (giá trị `settings_page`) | Nội dung |
| --- | --- |
| Chung `general` | Ngôn ngữ (tiếng Nhật/tiếng Trung giản thể/tiếng Anh), hình ảnh (Bản gốc/HD, cả hai nút đều chuyển sang màu xám khi thiếu nội dung HD), tỷ lệ khung hình (tự động: với màn hình gốc 4:3–16:9/4:3, viết `presentation.json` cho `aspect`, xem [Màn hình rộng](../design/deck-16x10.md)), khung hình (chỉ 4:3), bộ lọc và số hàng bộ lọc (2026-10-05, xem [Khung và Bộ lọc](bezels-and-filters.md)); nền tảng máy tính để bàn cũng có các chế độ hiển thị khác (cửa sổ/toàn màn hình) và kích thước cửa sổ (1×–4×), xem §8 |
| Giao diện `interface` | Kích thước giao diện (tiêu chuẩn/lớn/cực lớn); giao diện xác nhận trước trận chiến (phiên bản mới/bản gốc HD/bản gốc), màn hình giữa các cảnh, lựa chọn nhân vật chính và nhập tên, màn hình menu tiêu đề, mỗi hàng một hàng nút phân đoạn; tốc độ khung hình hiển thị (tắt/bật, ghi `presentation.json` cho `show_fps`): góc trên bên phải cập nhật "Khung hình trò chơi trên giây · Khung hình dài nhất trong nửa giây này", dựa trên danh sách hiển thị được trò chơi chuyển cho luồng đồ họa (`src/host/frame_rate.hpp`) |
| Quy tắc `rules` | Ba mặc định và hướng dẫn hiệu quả ở trên cùng, hai nhóm bên dưới: "Sửa đổi (bật mặc định)" và "Độ khó (tắt mặc định)", mỗi quy tắc có một dòng công tắc |
| Gian lận `cheats` | 05/10/2026: Năm công tắc (tắt theo mặc định) và một hàng "Cấp thí điểm". Nhấp vào "Mở rộng" để liệt kê các phi công và nút để thay đổi cấp độ ([Goldfinger](../gameplay/cheats.md)). Sau khi thêm trang này, hãy thay đổi các tab tiếng Anh "Giao diện" và "Điều khiển" thành "Giao diện người dùng" và "Đầu vào", nếu không 7 tab sẽ không vừa với cửa sổ nhỏ nhất |
| Lưu trữ `saves` | 2026-10-01, xem [Nhiều cột lưu trữ và lưu trữ tự động](../design/save-slots-autosave.md) §8: Chuyển đổi lưu trữ tự động; giữ 1/3/5/10 bản sao của mỗi bản lưu trữ tự động giữa các trò chơi và vòng chơi; ghi băng cassette thành bốn tệp: ares, Project64, mupen64plus và RetroArch (thư viện lưu trữ) `export/`); Liệt kê các tệp mô phỏng trong thư viện lưu trữ `import/` và nhập chúng vào từng cột cột mở rộng (các cột có tổng kiểm tra không nhất quán phải được nhấp lại và nhập sau khi sửa chữa). Đặt `settings.json` tồn tại trong thư viện lưu trữ và không nhập `presentation.json`. Chỉ một dòng mô tả được hiển thị khi phiên gỡ lỗi không có thư viện lưu trữ |
| Hoạt động `controls` | Trang thay đổi phím (28-09-2026, xem [Thay đổi phím](controls-remapping.md)): Bộ điều khiển được nhận dạng, mô tả mặc định của bàn phím (bố cục PCSX2), bảng thay đổi phím được liệt kê theo chức năng (mỗi cột một cột cho bàn phím và bộ điều khiển, thay đổi bằng cách nhấn một phím mới sau khi chọn), các phím tắt cố định và khôi phục về mặc định |
| Phản hồi `feedback` (Báo cáo bằng tiếng Anh) | 07-10-2026: Sao chép thông tin nền tảng, xuất báo cáo sự cố, nơi gửi phản hồi (biểu mẫu GitHub, nhận xét văn bản trên trang web chính thức), xem [Báo cáo sự cố](bug-report.md) |
| Giới thiệu `about` | Tên ứng dụng Marchwind64, một câu giới thiệu, số phiên bản (lấy từ `project(... VERSION)` của thư mục gốc `CMakeLists.txt`, được biên dịch bằng `SRW64_VERSION` Incoming); dòng liên kết (trang web chính thức, mã nguồn, phản hồi sự cố, trình duyệt hệ thống đã mở); dòng cập nhật ("Kiểm tra bản cập nhật", kết quả, "Trang tải xuống" và "Hướng dẫn cập nhật" khi có phiên bản mới) và nút chuyển "Kiểm tra bản cập nhật khi khởi động" ([Kiểm tra cập nhật](update-check.md)); Công tắc "Giao diện gỡ lỗi AI (MCP)", khi được bật, sẽ hiển thị địa chỉ đang nghe, thư mục đang chạy và "Sao chép thư mục đang chạy" ([Giao diện gỡ lỗi](../guide/debug-interface.md#打开方式选项里的开关)); HarmonyOS Sans, NhắcFont, tuyên bố librashader |

Mỗi công tắc tạo ra một hàng từ `settings_choice(键, id 前缀, 模式列表, 当前模式)`: phía trên là `label(键)`, một chế độ và một nút ở bên phải, còn bên dưới toàn bộ hàng là `label(键+"_note")` có id `前缀:模式` (giống như §6, như `battle-ui:native`, `images:hd`). Để thêm nút chuyển phiên bản gốc/phiên bản mới, chỉ cần thêm một dòng để gọi nó trên trang "Giao diện", sau đó thêm giá trị hiện tại của nó vào tem làm mới.

**vận hành**

| Đầu vào | Bàn phím | Bộ điều khiển | Chuột/Chạm |
| --- | --- | --- | --- |
| Mở/Đóng | Ctrl/Cmd+, mở; Esc hoặc |
| Thay đổi trang | Q／E, PageUp／PageDown, Ctrl+Tab／Ctrl+Shift+Tab | L1／R1 | Bấm vào tab |
| Chọn | ↑↓ (hoặc W/S) để di chuyển giữa các hàng; ←→ (hoặc A/D) để di chuyển giữa các tùy chọn liên tiếp; khi tiêu điểm nằm trên tab ←→ trực tiếp thay đổi trang | Phím chéo/cần điều khiển bên trái, giống như bên trái | Điểm trực tiếp |
| được | Nhập, Z, Dấu cách | A, phím menu | — |

"Hàng" là thanh tab và từng cài đặt (phần tử có lớp `nav`); ↑↓ trên các trang không có tùy chọn (thao tác, giới thiệu) được chuyển thành cuộn. Sau khi thay đổi trang, tiêu điểm sẽ rơi vào cài đặt đầu tiên của trang mới (tiêu điểm vẫn nằm trên tab khi trang được thay đổi). Không hiển thị hộp tiêu điểm khi sử dụng chuột (`body.pointer`). Toàn bộ trang được xây dựng lại sau khi thay đổi giá trị, với tiêu điểm và vị trí cuộn được giữ nguyên.

**Ghi nhớ phân trang**: Viết `settings_page` (`settings::set_settings_page`) của `presentation.json` mỗi khi bạn thay đổi trang và quay lại trang này vào lần tiếp theo khi bạn mở trang (bao gồm cả sau khi khởi động lại). Khi trình khởi chạy ghi lại tệp này bằng `--language`, nó vẫn sẽ mang lại (`launch.cpp`).

**Giao diện gỡ lỗi**: `ui.click` Khi nhấp vào điều khiển cài đặt không có trên trang hiện tại theo id, trước tiên nó sẽ chuyển sang trang đó và sau đó nhấp vào trang đó (phù hợp với thao tác của người chơi), vì vậy `press` của `settings-control.json` và tập lệnh cũ được nhấp theo id không cần phải thay đổi; id của nhãn trang là `settings-page:<页>`. `ui.key` được sử dụng để gửi `q`/`e`/`pageup`, `pad` có thể được sử dụng để thay đổi trang nếu L1/R1 được gửi.

**Ngắt dòng tiếng Trung và tiếng Nhật**: RmlUi chỉ ngắt dòng trong khoảng trống ASCII. Các câu tiếng Trung và tiếng Nhật không có dấu cách là cả một đoạn văn và sẽ tràn nếu không vừa (máy thực tế 09-27: mô tả về màn hình "インターミッション" tiếng Nhật được nhấn dưới nút). Vì vậy, chỉ riêng văn bản mô tả đã chiếm toàn bộ chiều rộng của dòng. `word-break: break-word` có thể bị buộc phải ngắt kết nối nhưng điều này sẽ khiến vòng lặp ngắt dòng của RmlUi bị kẹt (`ElementText.cpp:508` xác nhận rằng màn hình sẽ được làm mới và chuỗi cửa sổ sẽ không phản hồi nữa). **Không sử dụng**. `tests/test_settings_window.py` Dựa trên cửa sổ nhỏ nhất, người ta ước tính rằng mỗi đoạn văn bản không có khoảng trắng (mô tả, tên quy tắc, hai cột của bảng khóa, nhãn trang, tên cộng với nút một hàng) có thể được cung cấp và nó sẽ được báo cáo khi một mục mới được thêm vào hoặc kéo dài.

**Kiểm tra**: `tests/test_settings_window.py` (hai danh sách trang và hàng khóa nhất quán, ba mục nhập ngôn ngữ đã hoàn chỉnh, mỗi cột không bị tràn theo ước tính cửa sổ tối thiểu, ghi lại phân trang và `--language` được giữ lại và vị trí chính để thay đổi trang được duy trì). Máy thực tế: `tools/recomp/debug/check_settings_pages.py` (Màn hình tiêu đề mở cài đặt; 5 trang tiếng Trung, tiếng Anh và tiếng Nhật được cắt ra ở độ phân giải 960×720; Q/E, PageDown và xử lý L1/R1 để chuyển trang, di chuyển và xác nhận giữa các dòng và trong dòng; quy tắc bấm trang theo id sẽ lật trang trước; đóng và mở lại để quay về trang cuối cùng; xử lý dấu nhắc, B đóng, bật phím xem; Ảnh chụp màn hình cửa sổ lớn 1600×1000), tất cả đều được thông qua vào ngày 27-09-2026, ảnh chụp màn hình nằm trong thư mục đang chạy.

Một cách khắc phục khác: phiên bản cũ của tem làm mới thiếu hai nút chuyển "Chọn nhân vật chính và Nhập tên" và "Màn hình menu tiêu đề". Sau khi nhấp vào, trạng thái đã chọn của nút sẽ không được cập nhật; bây giờ tem bao gồm tất cả các công tắc.

Trả về: [Quy tắc tùy chọn](../gameplay/rule-fixes.md) · [Sửa lỗi cơ bản](../gameplay/base-fixes.md) · [Lộ trình MOD tích hợp](../design/mod-roadmap.md)

## Kích thước giao diện

28-09-2026 Người dùng đã báo cáo trên Steam Deck: Lời nhắc thao tác phía dưới, lời nhắc phím cài đặt trên màn hình tiêu đề và phông chữ trên trang xác nhận trước chiến tranh đều quá nhỏ. Lý do: Đối với các giao diện gõ vào dp (cửa sổ cài đặt, xác nhận phiên bản mới trước chiến tranh, nút cài đặt ở góc dưới bên phải của tiêu đề, thông báo), dp là một điểm. Khi cửa sổ lớn hơn 960×720 điểm, nó chỉ có nhiều không gian hơn và không phóng to; dp trên màn hình 7 inch 1280×800 của Deck chỉ bằng một nửa kích thước của máy tính để bàn. Các trang được vẽ theo tỷ lệ 320×240 ban đầu (các trang liên trò chơi, các trang gốc trước chiến tranh có độ phân giải cao) sẽ chia tỷ lệ theo màn hình mà không bị ảnh hưởng.

- **Cài đặt**: "Kích thước giao diện" ở dòng đầu tiên của trang "Giao diện": Chuẩn/Lớn/Cực lớn=1/1,25/1,5 lần (`settings::UiSize`, được lưu dưới dạng `ui_size` của file slideshow.json, chỉ được viết sau khi người chơi đã chọn). Nếu không được chọn, Steam Deck (`SteamDeck=1` hoặc báo cáo chương trình cơ sở Valve Jupiter/Galileo, `src/host/steam_deck.hpp`) sẽ cực lớn và các phần khác là tiêu chuẩn.
- **Cách phóng to**: `sync` của `frontend.cpp`: dp đầu tiên được giữ như bình thường (thu nhỏ khi cửa sổ nhỏ hơn 960×720 điểm), sau đó nhân với kích thước giao diện, nhưng kích thước logic sau khi phóng to không nhỏ hơn 800×540 dp (lớn trên Deck = 1024×640, cực lớn ≈ 864×540). Theo đó, trang phải được sắp xếp dưới 800×540 dp: văn bản trong mỗi cột của cửa sổ cài đặt được kiểm tra theo chiều rộng 800 (`tests/test_settings_window.py`, tab tiếng Nhật "インターフェース" do đó đã được đổi thành "màn hình" và một khoảng trắng đã được thêm vào cho phần mô tả dài bằng tiếng Nhật để ngắt dòng); chiều rộng của trang xác nhận trước chiến tranh nhỏ hơn 1000 dp Khi thêm `narrow` (hình đại diện là 64 dp, lề trong của nút trở nên nhỏ hơn), các số không còn bao bọc nữa.
- **Thanh dưới cùng của hộp thoại** (host vẽ ở tọa độ 320×240): phóng to theo kích thước của giao diện (tối đa 1,4 lần, đến cạnh dưới của hộp thoại bên dưới), lời nhắc thao tác ở bên phải sẽ giảm cỡ chữ thay vì cắt bớt khi không vừa với chiều rộng còn lại.
- **Biểu tượng nút**: Các biểu tượng của SRW64Prompt ban đầu được chia tỷ lệ theo chiều cao của chữ in hoa Latinh và được đặt nhỏ hơn một kích thước bên cạnh các ký tự tiếng Trung, chỉ có một khe mỏng cho LB/RB; bây giờ mỗi biểu tượng được phóng to lên bằng chiều cao của một ký tự Trung Quốc (khoảng 930/1000, căn giữa là 380, phóng to lên tới 1,4 lần, xem `build_prompt_font.py`).
- **Mẹo đi kèm với thiết bị**: Không có mục nào cho phiên bản bộ điều khiển (`_pad`) và các ký hiệu hành động trong bộ điều khiển cũng hiển thị biểu tượng bộ điều khiển khi sử dụng bộ điều khiển (ban đầu tất cả các phím trên bàn phím đều được hiển thị); thay vào đó, phần cuối của trang xác nhận trước chiến tranh sẽ nhắc sử dụng các ký hiệu (ban đầu được mã hóa cứng `Z / A`, `K / C▼`).

Máy thực tế (Mac, cửa sổ 1280×800 chấm mô phỏng kích thước logic của Bộ bài, 28/09/2026): Theo tiêu chuẩn/lớn/cực lớn, tôi đã thấy tiêu đề, thanh hội thoại phía dưới, trang xác nhận trước chiến tranh, cửa sổ cài đặt và trang vận hành; ở mức cực lớn, các con số trên trang xác nhận trước chiến tranh không bao bọc, các nút nằm trên một hàng và lời nhắc là biểu tượng nút.

## 8. Toàn màn hình và kích thước cửa sổ (2026-09-29)

Nền tảng máy tính để bàn có thể chuyển sang chế độ toàn màn hình và đặt cửa sổ thành bội số nguyên của kích thước ban đầu; bảng điều khiển cầm tay (Steam Deck, được xác định bởi chương trình cơ sở, chế độ trò chơi hoặc chế độ máy tính để bàn đều được bao gồm) có thể chuyển sang chế độ toàn màn hình mà không cần hai tùy chọn này.

| Lối vào | Phương pháp |
| --- | --- |
| Thanh menu Mac "Hiển thị" | "Toàn màn hình" ⌃⌘F (kiểm tra = toàn màn hình hiện tại); "Kích thước cửa sổ 1×–4×" ⌘1–⌘4 (kiểm tra = cửa sổ có kích thước chính xác như thế này). SDL có cùng phím với tiếng Anh Toggle Full Screen trong menu Window, đã bị ẩn. `src/host/macos/app_menu.mm` chỉ ghi nhớ yêu cầu và chuỗi cửa sổ xử lý yêu cầu đó trong `frontend.cpp`. |
| Windows／Linux | F11 chuyển sang toàn màn hình (không có phím bổ trợ). Không Alt+Enter: Trò chơi nhấn mã quét để đọc bàn phím và Enter cũng sẽ nhấn BẮT ĐẦU. |
| Đặt trang "Chung" | Cửa sổ/toàn màn hình "Chế độ hiển thị", "Kích thước cửa sổ" 1×–4×, có sẵn trên tất cả các nền tảng máy tính để bàn. |

- Sử dụng `SDL_WINDOW_FULLSCREEN_DESKTOP` cho toàn màn hình (toàn màn hình gốc trên Mac là không gian độc lập).
- Kích thước cửa sổ n× = 240n điểm cao và chiều rộng bằng n lần chiều rộng màn hình theo tỷ lệ hiện tại (`frame::width`): 2× lúc 16:10 là 768×480, 2× lúc 16:9 là 853×480 và khi đặt thành 4:3, 2× là 640×480. Khi sang số, hãy giữ cố định tâm cửa sổ và giữ nó trong phạm vi có sẵn của màn hình; không thể đặt các bánh răng (bao gồm cả thanh tiêu đề) và tất cả các bánh răng ở chế độ toàn màn hình đều không thể chọn được.
- Trạng thái toàn màn hình không được lưu và mỗi lần khởi động là một cửa sổ.
- Giao diện gỡ lỗi: `menu path=["显示","窗口大小 2×"]` Nhấn mục menu; `status.window.fullscreen`.

Đo thực tế (`build/recomp/debug/20260929T132807.116292Z`, cửa sổ bắt đầu lúc 16:10): Menu 1×–4× lần lượt đạt được 384×240, 768×480, 1152×720, 1536×960; "Toàn màn hình" đạt được 2560×1440, trong khi bốn cấp độ chuyển sang màu xám và "Toàn màn hình" được chọn; nhấp vào "Cửa sổ" trên trang cài đặt để quay lại 1536×960, nhấp vào "2×" để quay lại 768×480; thoát ra bình thường.