> **Ngôn ngữ / Language:** [Tiếng Việt](debug-interface.vi.md) · [English](debug-interface.en.md) · [中文](debug-interface.md)

> **Ngôn ngữ / Ngôn ngữ:** [中文](debug-interface.md) · [Tiếng Việt](debug-interface.vi.md) · [English](debug-interface.en.md)

# Giao diện gỡ lỗi và MCP

Ngày: 20-09-2026. Lối vào gỡ lỗi trên máy thực được các nhà phát triển và Claude chia sẻ: bắt đầu một phiên gỡ lỗi riêng biệt, nhấn phím, chụp ảnh màn hình, đọc trạng thái, vận hành giao diện gốc và thoát ra đều được hoàn thành thông qua cùng một giao diện. Không cần phải dựa vào thao tác gõ phím thủ công hoặc các file điều khiển riêng biệt.

## Cấu trúc

| Lớp | Vị trí | Chức năng |
| --- | --- | --- |
| Dịch vụ gỡ lỗi máy chủ | `src/host/debug_server.cpp`, `debug_transport.cpp`, chuyển `SRW64_DEBUG=1` | Giám sát TCP vòng lặp cục bộ (`127.0.0.1`, cổng do hệ thống chỉ định), một yêu cầu/phản hồi JSON-RPC 2.0 trên mỗi dòng; cổng và mã thông báo được ghi bằng `debug.json` của thư mục đang chạy (xem "Phương thức kết nối" bên dưới). Chơi thử bình thường không được kích hoạt. Các hoạt động yêu cầu SDL/RmlUi được xếp hàng vào luồng cửa sổ để thực thi. |
| Lớp bàn phím trò chơi | `src/host/debug_protocol.hpp`, `graphics.cpp` | Các phím ảo có đường đọc giống như phím thật: gắn với mã quét cùng tên, cạnh nhấn F6/F7/F8/Esc đi qua cùng một trang tên và điều khiển cổng chuyển đổi ngôn ngữ; việc kiểm tra phát hành sau khi đóng trang tên cũng được tính vào các phím ảo. Các phím ảo không yêu cầu tiêu điểm cửa sổ và trò chơi có thể được chạy ở chế độ nền. |
| Lớp giao diện gốc | `src/host/debug_ui.hpp`, `src/native/ui/frontend.cpp` | Trang SDL/RmlUi được chia sẻ cung cấp cây giao diện, ID/văn bản/tọa độ nhấp chuột ổn định, văn bản đầu vào và khóa; cài đặt và thông báo đều có trong bề mặt trò chơi. |
| Phiên và khách hàng | `tools/recomp/debug/session.py` | Bắt đầu phiên (thông qua `run_host_probe.py --graphics --interactive`, xuất ra `build/recomp/debug/<时间戳>/`, không chạm vào kho lưu trữ và tùy chọn của `profile-play`), kết nối ứng dụng khách (`Client(运行目录)`), điều kiện chờ, đọc nhật ký sự kiện tăng dần. |
| Dòng lệnh | `tools/recomp/debug/srw64ctl.py` | Cùng một tập hợp các hoạt động cho con người sử dụng. |
| Máy chủ MCP | `tools/recomp/debug/mcp_server.py`, kho gốc `.mcp.json` | stdio MCP được thư viện chuẩn triển khai (môi trường dự án không có gói `mcp`), Claude Code có thể gọi công cụ `srw64_*` sau khi phê duyệt MCP dự án và mở lại phiên. |

## Bảo hiểm

Mục tiêu là mọi thông tin đầu vào mà trò chơi nhận được đều có thể được gửi qua giao diện và cố gắng đi theo cùng một đường dẫn mã như người chơi:

| Đầu vào mà trò chơi nhận được | Nguồn người chơi | Giao diện |
| --- | --- | --- |
| 18 phím game (14 phím N64 tương ứng với joystick WASD) | Trạng thái bàn phím SDL | `keys`: Hợp nhất bảng bàn phím cũ (`input::classic_keys`: Z=A,
| Màn hình F6, cấp độ F8 mini, lối thoát Esc | Sự kiện quan trọng SDL | `keys`: Cạnh nhấn ảo đi qua cùng trang tên và cổng chuyển ngôn ngữ với phím thật |
| Ngôn ngữ F7 | sự kiện bàn phím SDL, được chuyển giao cho phương thức nhập trong quá trình nhóm từ | `keys f7`: Nhập cùng nhóm từ SDL/điều khiển cổng lặp lại |
| Tay cầm N64 (bỏ qua lớp bàn phím) | Không có (để chẩn đoán) | `buttons` |
| Trang lựa chọn nhân vật chính: bốn lá bài, ←→, Enter／Z | Chuột và bàn phím SDL | `ui.click --text <主角全名>` (đánh dấu và nhấn Tiếp tục hoặc Enter), `ui.key right`/`return`; `status.name_page` cung cấp `route` và bốn tùy chọn |
| Menu chính giữa các cảnh: chín mục (hai mục sau cảnh "(trước)"), menu phụ のりかえ | Chuột và bàn phím SDL | `ui.click --text intermission:N` (hoặc văn bản hiển thị) Xác nhận mục thứ N, `intermission-swap:0|1` Chọn trình điều khiển/yêu tinh; `ui.key up`/`down`/`return`/`escape`; `status.intermission_page` tặng `cursor`, `submenu`, `swap_refused`, số vòng và số tiền |
| Màn hình sửa đổi: danh sách nội dung, năm sửa đổi, cửa sổ xác nhận và thông báo | Chuột và bàn phím SDL | `ui.click --text upgrade:N` (xác nhận dòng hiện tại, chuyển động của các dòng khác), `upgrade-confirm`/`upgrade-cancel`/`upgrade-dismiss`; `ui.key up`/_ _INL_CODE_44__／`left`／`right`／`return`／`escape`；`status.upgrade_page` Đã cho `screen`, `rows`, `window`, `funds`; sửa đổi trực tiếp quỹ: `ui.click --text upgrade-funds` (menu chính `intermission-funds`), `ui.type <数字>`, `ui.key return` |
| Trang liên kết: ba thẻ công việc, ←→, dấu cách/Z, Enter, Esc/X | Chuột và bàn phím SDL | `ui.click --text <作品名>` (kiểm tra từng công tắc), `ui.click --text <继续按钮>`, `ui.key right`/`space`/`return`; `status.link_page` được tặng `joined` và `scheduled` |
| Trang truyền và xác nhận: thẻ, nút, ←→/Enter/Esc | Chuột và bàn phím SDL | `ui.click`, `ui.key`; `status.name_page` đưa ra bốn lộ trình tới `person` (3 lần truyền, 2 xác nhận) và các trang truyền |
| Trang xác nhận trước trận chiến: Xác suất của cả hai bên, phản ứng, hoạt ảnh, bắt đầu/quay lại; các phím giống như trò chơi (Z/Enter, X/Esc, phím điều hướng/WASD, Q, E, K) và bộ điều khiển | SDL/RmlUi | `ui.click --id battle-confirm`, `battle-weapon`, `battle-counter`, `battle-evade`, `battle-defend`, `battle-spirits`, `battle-animation`, `battle-back`; `status.battle_page` là ảnh chụp nhanh được phát hành bởi chủ đề trò chơi |
| Tải tệp cấp độ trong thời gian chạy | Khi giao diện gỡ lỗi mở, hãy kéo tệp vào cửa sổ trong menu tiêu đề | `mini_stage.load {"path": <镜像或关卡源文件>}`; nhập trực tiếp mà không chỉ định cấp độ khi khởi động, xem [Cấp độ nhỏ](../script/mini-stage.md) |
| Menu chính lối vào cấp nhỏ | Nút RmlUi/F8 | `ui.click --id mini-enter` hoặc `keys f8` sau khi bắt đầu với giai đoạn nhỏ; đợi `status.mini_stage.ready`. Tự động hoàn tất quá trình khởi tạo ký tự mặc định, không thay đổi đối với các game mới thông thường |
| Cài đặt quy tắc và "tùy chọn" trong trò chơi | Kiểm soát RmlUi, Ctrl/Cmd+, | `ui.click`, `ui.key`; `menu` duy trì khả năng chuyển tiếp tương thích của tiêu đề quy tắc được bản địa hóa |
| Trang パーツ nâng cao Interfield: Danh sách đơn vị, ô/kho, người giữ | Trang RmlUi | `ui.click --id parts:N`/`parts-slot:N` hoặc các phím mũi tên của `keys`, Z/X; `status.parts_page`, điều kiện chờ `parts_page`, nhật ký sự kiện `parts` |
| Trang khả năng của Interfield ユニット/パイロット | Trang RmlUi | Các phím định hướng của `ui.click --id ability:N` hoặc `keys`, Z/X, Q/E; `status.ability_page`, điều kiện chờ `ability_page`, nhật ký sự kiện `ability` |
| Trang のりかえ: danh sách phi công/yêu tinh, danh sách mục tiêu, xác nhận | Trang RmlUi | `ui.click --id swap:N`／`swap-yes`／`swap-no` hoặc `keys`; `status.swap_page`, điều kiện chờ `swap_page`, nhật ký sự kiện `swap` |
| Trang Interfield データセーブ: lựa chọn phương tiện, thanh lưu trữ, xác nhận ghi đè, dấu nhắc Pak | Trang RmlUi | `ui.click --id save:N`／`save-yes`／`save-no` hoặc `keys`; `status.save_page`, điều kiện chờ `save_page`, nhật ký sự kiện `save` |
| Cài đặt chia sẻ: quy tắc, mặc định, ngôn ngữ, màn hình, tỷ lệ màn hình, kích thước giao diện, giao diện xác nhận trước trận chiến, màn hình giữa các cảnh, chọn nhân vật chính, màn hình menu tiêu đề (chia thành năm trang, nhấp theo id để chuyển sang trang đầu tiên) | Trang RmlUi | `ui.click`/`ui.tree`/Mặc định `screenshot`; hoặc sử dụng `settings` Cài đặt trực tiếp (`rules`/`images`/`aspect` (`auto`/`4:3`)/__INL _CODE_120__／`battle_ui`／`ui_size`／`intermission_ui`／`name_entry_ui`／`title_ui`） |
| Cửa sổ trò chơi: kích thước, tiền cảnh, nút đóng | Quản lý cửa sổ | `window` (`width`/`height`, `front`, `close`) |
| Thoát bình thường | Esc, đóng cửa sổ, ⌘Q | `quit` hoặc `keys escape`, `window close` |

`tests/test_debug_coverage.py` kiểm tra tĩnh tiền đề của bảng này. Thiếu giao diện khi thêm khóa hoặc phương thức sẽ khiến quá trình kiểm tra không thành công: mỗi mã quét SDL được máy chủ đọc có một khóa ảo có cùng tên; F6/F8/Esc có cạnh bấm ảo, F7 có phím ảo tương ứng; bảng nút của `buttons` nhất quán với trình biên dịch đầu vào (`native_inputs.BUTTONS`); MCP Tên khóa của mô tả công cụ nhất quán với máy chủ; có một công cụ MCP cho mỗi phương thức lưu trữ.

## Phương thức lưu trữ

| Phương pháp | Thông số | Mô tả |
| --- | --- | --- |
| `status` | `history` | VI, thư mục đang chạy, tiêu điểm và kích thước cửa sổ, ngôn ngữ, chế độ màn hình, quy tắc, trạng thái mở (`title_major` 3 là menu chính, `step` là trang hiện tại), trình đọc hội thoại (trang, cỡ chữ, tốc độ, tự động, xem lại, bỏ qua, từng văn bản hộp thoại), yêu cầu trang tên, trang liên kết (`link_page`), menu chính giữa các cảnh (`intermission_page`), màn hình chuyển đổi (__INL_CODE) _143__), trang xác nhận trước chiến tranh (`battle_page`), trạng thái cấp độ nhỏ (`mini_stage.available/entering/active/ready`), thanh nhắc nhở gốc gần đây (`notices`, hoàn tiền nếu bạn rời khỏi nhóm), cửa sổ và tiêu điểm gốc, nhấn phím ảo |
| `keys` | `press`+`hold_ms` / `down` / `up` / `release_all` | Bàn phím trò chơi; tên khóa `z x space return up down left right q e i k j l w a s d escape f6 f7 f8 f5` (F5 tải lại văn bản dòng), được sử dụng kết hợp `+`, chẳng hạn như `e+return` |
| `pad` | `press`+`hold_ms` / `down` / `up` / `release_all` | Bộ điều khiển ảo, mỗi khung được hợp nhất vào trạng thái của bộ điều khiển thực (lời nhắc của bộ điều khiển, trang, L2/R2 và các khóa máy chủ khác được coi là bộ điều khiển thực); tên khóa theo Steam Deck: `a b x y menu view l1 r1 l2 r2 up down left right ls_up… rs_down…`, kết hợp với `+`. Dòng lệnh `srw64ctl.py pad r2 l2:600 wait:300` |
| `buttons` | `buttons`, `vis` | Các phím của lớp bộ điều khiển N64 (`a b z start up down left right l r c_up c_down c_left c_right`), có hiệu lực ngay lập tức mà không cần thông qua lớp bàn phím |
| `screenshot` | `path`, `overlays`, `window`, `timeout_ms` | Lấy thông tin đọc lại GPU của lần kết xuất tiếp theo, bao gồm cả giao diện người dùng được chia sẻ. `window` Sử dụng cửa sổ trò chơi mặc định; không còn cung cấp cửa sổ cài đặt độc lập hoặc tổng hợp AppKit. |
| `ui.tree` | `window` | Cây phần tử RmlUi: tag, `id`, `frame` (tọa độ điểm cửa sổ), văn bản, có sẵn, tiêu điểm; pixel = điểm × `scale`. |
| `ui.click` | `text` hoặc `id` hoặc `x`/`y`, `button`, `count` | Sau khi ID ổn định hoặc khớp văn bản hiển thị, thông qua các lần nhấp thử nghiệm bằng chuột RmlUi; sử dụng cùng một đường dẫn cho cả mặt trước và mặt sau. |
| `ui.key` | `key`, `modifiers` | Tên khóa SDL: return, tab, escape, delete, phím mũi tên, a–z, 0–9, f1–f12; macOS `key_code` không còn được sử dụng nữa. |
| `ui.type` | `text`, `marked`, `unmark`, `window` | Chèn văn bản vào hộp nhập tiêu điểm, tương đương với việc gõ phím; `marked: true` được dành riêng cho nhóm phương thức nhập (gạch chân, không gửi), `unmark: true` Gửi từ nhóm; phản hồi `marked` cho biết có nên thêm từ nhóm vào lần này hay không |
| `menu` | `path` | Tiêu đề được bản địa hóa tương thích với các quy tắc và cài đặt chuyển tiếp; Menu hệ điều hành không còn được liệt kê. |
| `settings` | `rules` (tên mặc định hoặc danh sách ID), `locale`, `images` | Trực tiếp thay đổi quy tắc, ngôn ngữ, màn hình |
| `window` | `width`/`height`, `front`, `close` | Thay đổi kích thước cửa sổ trò chơi (nhấp chuột 640–2560 × 480–1600), đưa lên nền trước (chỉ bắt buộc khi bạn muốn xác minh tiêu điểm thực hoặc sự kiện chuột thực), nhấn nút đóng (`SDL_WINDOWEVENT_CLOSE`); phản hồi trạng thái cửa sổ |
| `wait_vi` | `vi`, `timeout_ms` | Đợi đến khi được chỉ định VI |
| `memory.read` | `address`, `size` (≤ 0x10000) | Đọc bộ nhớ đối tượng và trả về hệ thập lục phân; đừng tạm dừng trò chơi, đây là chế độ xem gỡ lỗi thay vì ảnh chụp nhanh ([Bỏ qua ngắn] (../native/script-skip.md) sử dụng nó để kiểm soát trạng thái) |
| `memory.write` | `address`, `hex` (byte số nguyên, 4096 byte) | Ghi bộ nhớ đối tượng (đối với các đầu dò, chẳng hạn như nền chiến đấu cưỡng bức; chỉ trong các phiên gỡ lỗi) |
| `record.start`, `record.stop` | `width` (mặc định 960) | Ghi: sau khi bắt đầu, mỗi kết xuất sẽ được đọc lại, rút ​​ngắn thành `width` và được thêm vào khung và thời gian ban đầu của `record-<VI>/` trong thư mục đang chạy. Âm thanh trò chơi được ghi khi gửi đến thiết bị đầu ra. `audio.s16` (âm thanh nổi s16le); trả về số khung và kích thước khi dừng, cũng như `audio_frames`, `audio_rate` và `audio_start` (số giây kể từ khi đoạn âm thanh đầu tiên bắt đầu ghi). `Session.record(秒数)` (hoặc `record_start`... `record_stop(path)`, bạn có thể vận hành trò chơi ở giữa) sắp xếp màn hình thành dòng thời gian 30 khung hình cố định (mỗi thời điểm hiển thị khung hình mới nhất tại thời điểm đó và vị trí bị kẹt là khung hình cố định), nhấn `audio_start` để căn chỉnh và trộn vào đoạn âm thanh AAC và sử dụng ffmpeg để biên dịch thành MP4 và xóa tệp gốc; MCP là `srw64_record`, `srw64_record_start`/`srw64_record_stop` (có thể cung cấp `path`, thư mục sẽ được tạo nếu chưa tồn tại). Phiên gỡ lỗi bị tắt tiếng theo mặc định. Nếu bạn muốn có âm thanh, bạn cần `srw64_launch(audio=true)`; bản thân trò chơi không có âm thanh trong khoảng 27 giây trước khi khởi động (logo và phần mở đầu). Màn hình tiêu đề đo thực tế được ghi trong 8 giây với 240 khung hình và khoảng thời gian dài nhất là 40 ms. Bản thân quá trình ghi gần như không bị chậm lại |
| `quit` | — | Thoát bình thường, được báo cáo là thoát có kiểm soát |
| `methods` | — | Liệt kê các phương thức được máy chủ hỗ trợ |

Tất cả các trang trò chơi hiện chia sẻ một cửa sổ SDL duy nhất; ảnh chụp màn hình sử dụng cửa sổ mặc định hoặc `"game"`.

##Dòng lệnh

```sh
.venv/bin/python tools/recomp/debug/srw64ctl.py launch --language zh-Hans   # 构建并启动，打印运行目录
.venv/bin/python tools/recomp/debug/srw64ctl.py wait --title-menu
.venv/bin/python tools/recomp/debug/srw64ctl.py keys return                  # 主菜单确认
.venv/bin/python tools/recomp/debug/srw64ctl.py keys e+return:200            # 跳过序章
.venv/bin/python tools/recomp/debug/srw64ctl.py click --text 继续            # 姓名页按钮
.venv/bin/python tools/recomp/debug/srw64ctl.py type ナナ --marked            # 输入法组字；type --unmark 提交
.venv/bin/python tools/recomp/debug/srw64ctl.py keys i i k e+z:1500          # 字号、快进
.venv/bin/python tools/recomp/debug/srw64ctl.py shot                         # 截图路径与元数据
.venv/bin/python tools/recomp/debug/srw64ctl.py window --size 1280 960
.venv/bin/python tools/recomp/debug/srw64ctl.py events dialogue --kind font
.venv/bin/python tools/recomp/debug/srw64ctl.py quit
```

Mỗi mục của `keys` là một tổ hợp phím và có thể thêm `:按住毫秒`; `wait:500` chỉ là sự tạm dừng. Các lệnh không phải `launch` được mặc định là phiên bắt đầu gần đây nhất (`build/recomp/debug/current`), cũng có thể được chỉ định bằng `--run`. `--reuse-build` Bỏ qua việc xây dựng lại khi mã nguồn không thay đổi.

Tuổi thọ phiên: Trò chơi được bắt đầu bởi `Session.launch` trong tập lệnh sẽ chỉ tồn tại cho đến khi quá trình bắt đầu kết thúc - quá trình kiểm tra được chạy, xác nhận không thành công và hết thời gian chờ (bao gồm `kill -9`) sẽ khiến `run_host_probe.py` gửi `quit` để tắt trò chơi (SIGTERM khi không có ổ cắm) và báo cáo sẽ ghi lại `ended_with_owner`; Nếu tập lệnh bị mất trong quá trình xây dựng, trò chơi sẽ không được khởi chạy nữa. Cơ chế này là một ống dẫn (`SRW64_DEBUG_OWNER_FD`) trong đó chỉ có quá trình khởi tạo mới giữ được kết thúc ghi. Phiên `srw64ctl.py launch` phải được dành riêng cho các lệnh tiếp theo và không tuân theo hạn chế này. Khi sử dụng hết, phải sử dụng `quit`; phiên bắt đầu bởi MCP sẽ thoát khỏi máy chủ MCP. Sau khi tập lệnh kết thúc, nếu bạn muốn để cửa sổ mở cho người khác xem, hãy chuyển `Session.launch(detach=True)`.

##Công cụ MCP

`srw64_launch`, `srw64_attach`, `srw64_status`, `srw64_keys`, `srw64_buttons`, `srw64_screenshot` (trực tiếp quay lại hình ảnh), `srw64_record` (quay video có âm thanh MP4, đường dẫn quay lại), `srw64_record_start`/`srw64_record_stop`, `srw64_ui_tree`, `srw64_click`, `srw64_type`, `srw64_ui_key`, `srw64_menu`, `srw64_window`, __INL_CODE_272_ _, `srw64_mini_stage_load`, `srw64_memory`, `srw64_wait` (`vi`, `dialogue_active`, `intro_active`, `name_page`, `link_page`, `intermission_page`, __INL_ CODE_282__, `title_major`, `text`, `event`), `srw64_events` (nhật ký: `dialogue`, `intro`, `name`, `rules`, __INL_CODE _291__, `control`, `script`, `mini_stage`, `settings`, `refunds`, `link`, `intermission`, `unit_name`), `srw64_quit`. Lỗi công cụ được trả về dưới dạng `isError` và không làm gián đoạn máy chủ. Máy chủ không còn chụp ảnh màn hình hoặc xuất bộ nhớ thông thường nữa (2026-10-01 đã xóa "Chẩn đoán hoàn chỉnh": chụp ảnh màn hình toàn bộ cửa sổ cứ sau hai giây hoặc lâu hơn, xuất 8 MiB bộ nhớ và ngọn lửa tiêu đề sẽ giảm từ 30 khung hình xuống 18); nếu bạn muốn có hình ảnh, hãy sử dụng `srw64_screenshot`, nếu bạn muốn có quy trình, hãy sử dụng video.

## Phương thức kết nối

Bắt đầu từ ngày 06 tháng 10 năm 2026, ba nền tảng máy tính để bàn (macOS, Linux và Windows) sẽ sử dụng TCP loopback gốc để thay thế ổ cắm Unix ban đầu (`debug.sock`). Nguyên nhân là do phiên bản CPython trên Windows không có `socket.AF_UNIX`; tình cờ, giới hạn trên về độ dài của đường dẫn ổ cắm bị xóa (macOS 104 byte).

- Host lắng nghe `127.0.0.1:0`, cổng do hệ thống chỉ định; thêm `SO_EXCLUSIVEADDRUSE` trên Windows.
- `debug.json` (`srw64.debug-endpoint.v2`) của thư mục chạy ghi `transport: "tcp"`, `host`, `port`, `token` (số ngẫu nhiên 256 bit, thập lục phân) và `pid`. Tệp được tạo lần đầu tiên và chỉ chủ sở hữu mới có thể đọc và ghi, sau đó mã thông báo sẽ được ghi. Sau khi viết và đổi tên, client sẽ không đọc được một nửa; nó sẽ bị xóa khi trò chơi thoát.
- Dòng đầu tiên của mỗi kết nối phải là `{"jsonrpc":"2.0","id":0,"method":"auth","params":{"token":"…"}}`, token được so sánh theo thời gian không đổi. Nếu sai hoặc thiếu, trả về lỗi và ngắt kết nối; bộ nhớ đệm lên tới 4 KiB trước khi bắt tay.
- Token thay thế vai trò của file socket gốc 0600: mọi tiến trình trên máy cục bộ đều có thể kết nối với cổng loopback và chỉ người chơi mới có thể đọc `debug.json`.
- Máy khách `Client(运行目录)` đọc `debug.json` trước; nếu không, hãy tìm `debug.tcp` (Android: cổng cục bộ được chuyển tiếp bởi adb, không có mã thông báo). `Session.launch` và `Session.attach` đều sử dụng "liệu hai tệp này có tồn tại hay không" để xác định xem phiên có đang chạy hay không.
- Android không thay đổi: vẫn là ổ cắm trừu tượng `@srw64-debug`, chỉ chuyển tiếp adb mới có thể tiếp cận nó. Việc thay đổi sang TCP và thêm mã thông báo không hoạt động: không thể gỡ lỗi phiên bản phát hành của APK và adb không thể đọc mã thông báo trong thư mục riêng của ứng dụng.
- Không tương thích giữa cũ và mới: Phiên bản mới của client không thể kết nối với game trước ngày 2026-10-06 và ngược lại.

## Cách mở: chuyển đổi tùy chọn

Người chơi không cần dòng lệnh: "Tùy chọn → Giới thiệu → Giao diện gỡ lỗi AI (MCP)" (`debug_interface` của `presentation.json`, mặc định là tắt). Chuỗi cửa sổ so sánh trạng thái chuyển đổi và nghe ở mỗi khung hình (`debug::service_main`):

- Mở: Nghe ngay (từng port mới, token mới), và đăng lời nhắc (`debug_interface_notice`); nếu công tắc được lưu, nó sẽ lắng nghe và nhắc nhở mỗi lần khởi động.
- Đóng: `transport::stop()` ngừng nhận kết nối, ngắt kết nối hiện có, xóa `debug.json`; các yêu cầu chuỗi cửa sổ được xếp hàng đợi trả về có lỗi.
- `--debug` (`SRW64_DEBUG=1`) vẫn giám sát trước khi cửa sổ được mở và không đăng lời nhắc; công tắc được hiển thị là "bật" và không thể nhấp vào cũng như không thể tắt trong quá trình chạy này. Các phiên phát triển (`Session.launch`) đều diễn ra theo cách này.
- Khi mở trang About sẽ hiển thị địa chỉ nghe và thư mục đang chạy (thư mục chính ghi là `~`, dài quá thì chỉ hiển thị phần cuối), “Copy Running Directory” sao chép đường dẫn đầy đủ. Trạng thái trong cài đặt được chuyển tới trang thông qua `settings::set_debug_endpoint`.

Khi giám sát không thành công (ví dụ: không thể ghi `debug.json`), nhật ký sẽ ghi lại `SRW64_DEBUG_FAILED` và sẽ không thử lại cho đến khi công tắc thay đổi lần nữa.

## đính kèm không có tham số

`Session.attach()` (`srw64_attach` của MCP không có `run`) Nhấn `running_games()` để tìm: `build/recomp/debug/current` (gần đây nhất `srw64ctl launch` hoặc `attach.py`) cùng với tất cả `sessions/*/run/debug.json` trong thư mục người dùng trình phát cục bộ (`player_data()`: macOS `~/Library/Application Support/SRW64Recomp`, Windows `%LOCALAPPDATA%\SRW64Recomp`, Linux `$XDG_DATA_HOME/srw64-recomp`), hãy thử kết nối từng tệp một từ thời gian tệp mới nhất đến tệp cũ nhất (Hết thời gian chờ 3 giây, `methods`), tệp đầu tiên có thể phản hồi là. `debug.json` do sự cố để lại không thể kết nối được và sẽ bị bỏ qua một cách tự nhiên.

## Tệp trên máy khác

Ảnh chụp màn hình, khung video và nhật ký sự kiện là các tệp được máy chủ ghi trên máy của chính nó. Máy chủ có hai phương thức được giới hạn trong thư mục đang chạy: `file.read {path, offset, size}` (tối đa 4 MiB cùng một lúc, base64, trả về tổng chiều dài tệp và `eof`) và `file.remove {path}` (không thể xóa chính thư mục đang chạy). Khi `Session.local()` sai (có `remote.json` hoặc `debug.tcp` trong thư mục đang chạy, nghĩa là Bộ bài hoặc điện thoại di động), `Session.local_file()` được truy xuất theo từng khối có `file.read` và `Session.record()` được sử dụng. `file.remove` xóa thư mục khung ở phía máy chủ, `Session.events()` nhấn `status.run` để lấy nhật ký từ xa. Deck không còn yêu cầu scp nữa và Android cũng có thể chụp ảnh màn hình và quay video.

## Trên Steam Deck (hoặc máy Linux khác)

`--play` của gói phát hành sẽ xóa tất cả các biến môi trường `SRW64_*` và `SRW64_DEBUG=1` sẽ không hoạt động ở đó; để mở giao diện gỡ lỗi, hãy chuyển `--debug` vào trò chơi. `debug.json` được ghi vào thư mục đang chạy của phiên này (`~/.local/share/srw64-recomp/sessions/<id>/run/`). Không có `--debug` thì nó hoàn toàn giống như trước. Trên Windows, `--debug` (`Marchwind64.cmd --debug`) cũng được tải lên và thư mục đang chạy nằm trong `%LOCALAPPDATA%\SRW64Recomp\sessions\<id>\run\`.

1. Trên boong: Viết `%command% --debug` vào "Thuộc tính → Tùy chọn khởi chạy" của phím tắt này trong Steam, sau đó chơi bằng bộ điều khiển thông thường. Không cần phải bỏ cuộc khi có sự cố xảy ra.
2. Trên Mac: `.venv/bin/python tools/release/linux/attach.py` (máy chủ ssh mặc định `Deck`, `--host` có thể thay đổi). Nó đọc `debug.json` của trò chơi đang chạy với giao diện gỡ lỗi được bật (công tắc trong tùy chọn hoặc `--debug`) thông qua ssh, chọn một cổng trống cục bộ và chuyển tiếp nó tới cổng từ xa bằng cách sử dụng `ssh -L`, ghi cổng cục bộ và mã thông báo gốc (quyền 0600) trong `build/recomp/debug/deck-<时间>/debug.json` và đặt nó làm phiên hiện tại; thì `srw64ctl.py`, `Session.attach()`, `srw64_attach` của MCP đều có sẵn trực tiếp.
3. Khi bạn không muốn thay đổi cài đặt Steam, `attach.py --start` sẽ bắt đầu trò chơi thông qua ssh với `--debug` (chế độ trò chơi ở Xwayland `:1`, chế độ máy tính để bàn là `--display :0`). Việc thêm `--data-dir ~/srw64-debug` sử dụng một tập hợp thư mục dữ liệu riêng biệt: gói ROM và HD là các liên kết mềm, các kho lưu trữ và cài đặt được sao chép, đồng thời việc gỡ lỗi sẽ không ghi vào kho lưu trữ của riêng người chơi. Thông số trò chơi được viết sau `--`.

`remote.json` trong thư mục đang chạy ghi nhớ máy chủ, thư mục chạy từ xa và quá trình chuyển tiếp. Ảnh chụp màn hình, video (`srw64_record`) và nhật ký sự kiện (`srw64_events`, `event` điều kiện của `wait`) là các tệp được máy chủ ghi trên Bộ bài và `Session.local_file()` được truy xuất về `remote-files/` thông qua cùng một kết nối (`file.read`). `quit` sẽ tắt trò chơi và chuyển tiếp cục bộ, để lại báo cáo trên Bộ bài. Lỗi tiêu chuẩn của trò chơi là `journalctl --user` (được ghi dưới tên của quy trình steam) khi khởi động Steam. Khi `--start`, trò chơi được chạy dưới dạng đơn vị tạm thời của hệ thống người dùng `srw64-debug` (SteamOS được bật `KillUserProcesses=True` và quá trình còn lại trong phiên đăng nhập ssh sẽ bị xóa khi ssh bị ngắt kết nối). Xem đầu ra. `journalctl --user -u srw64-debug`.

## Mối quan hệ với các tệp điều khiển hiện có

`control.txt`, `script-inject.txt` và các điều khiển cửa sổ/ngôn ngữ SDL được giữ lại. Tệp kiểm soát quy tắc/tên AppKit cũ
Thuộc chương trình phụ trợ cũ, giao diện người dùng được chia sẻ sử dụng JSON-RPC và chấp nhận `tools/recomp/verify/verify_shared_ui.py`.
`control.txt` chỉ thêm trạng thái xử lý; `ui.*` là bắt buộc để nhóm từ, nhấp chuột vào trang và tập trung vào cửa sổ.

## Đo lường lịch sử: phần phụ trợ AppKit cũ (`build/recomp/debug/20260918T090743.895227Z`)

Toàn bộ quá trình từ khởi động nguội được điều khiển bởi giao diện, không có phím thủ công: Enter để quay lại tiêu đề và chọn "スタート" trong menu chuông, E+Enter để bỏ qua phần mở đầu công khai (VI 12826), Z để chọn nhân vật nam siêu nhân vật chính và xác nhận, sử dụng `click --text` trên trang tên hiện đại và nhấn "Tiếp tục: Đối tác", "Tiếp tục: Xác nhận" và "Bắt đầu câu chuyện" theo trình tự (ứng dụng ở chế độ nền, nút đã được `performClick:`), nhấn E+Enter trong đoạn mở đầu lộ trình của nhân vật nam chính để bỏ qua VI 18154 (nhóm 1); sau khi vào đoạn hội thoại, I, I, K thay đổi cỡ chữ thành 13→14→15→14 (cả ba lần đều có hiệu lực) và khi nhấn E+Z, 14 VI sẽ đẩy liên tiếp 3 đoạn văn; ảnh chụp màn hình được xếp chồng lên lớp phủ trang tên; mở cửa sổ cài đặt thông qua menu "Tùy chọn → Cài đặt..." và chụp ảnh màn hình, sử dụng `click --text` Kiểm tra và hủy "Sếp giả: giảm một nửa", các quy tắc và nhật ký sự kiện sẽ đồng thời thay đổi; `quit` mã thoát 0, ổ cắm sẽ bị xóa.

Một phiên khác trong cùng ngày (khi khởi động `--reuse-build`): `window --size 1280 960` theo sau là `status` và cả ảnh chụp màn hình đều báo cáo 1280×960; trên trang tên `type なな --marked` trả về `composing: true`, ảnh chụp màn hình hiển thị "なな" với phương thức nhập được tô sáng trong cột tên, `type --unmark` theo sau là `composing: false`; `quit` mã thoát 0. `window --close` Cửa sổ tái sử dụng QA đã xác minh đường dẫn `performClose:`, chỉ kiểm tra biên dịch đã được thực hiện.

Điều này cũng kiểm tra lại bản sửa lỗi trang tên vào ngày 18 tháng 9 năm 2026: trước khi sửa lỗi, các phím trò chơi được nhấn sau khi đóng trang tên đều bị nuốt và bỏ qua phần mở đầu tuyến đường, kích thước phông chữ và chuyển tiếp nhanh đều không hợp lệ.

## Hạn chế

- Không nhấn Enter (START) sau khi khởi động cho đến khi màn hình tiêu đề xuất hiện: Phiên bản gốc phát hiện nhấn START sẽ vào màn hình quản lý Controller Pak khi khởi động, trong đó `osPfsIsPlug` được gọi hiện đang bị chặn bởi mã được tạo và máy chủ sẽ hủy bỏ. `wait --vi 600` đầu tiên sau khi khởi động.
- Ảnh chụp màn hình phụ thuộc vào trò chơi được hiển thị; nó sẽ hết thời gian chờ khi cửa sổ được thu nhỏ hoặc trò chơi bị tạm dừng.
- Lớp giao diện gốc chỉ bao phủ cửa sổ riêng của chương trình; hộp thoại hệ thống và cửa sổ đề xuất phương thức nhập không nằm trong phạm vi (bản thân từ nhóm được mô phỏng bằng `marked` của `ui.type`).
- `status.ui.focus` là thành phần tiêu điểm của RmlUi và `active` cho biết riêng biệt liệu cửa sổ SDL có tiêu điểm bàn phím hệ thống hay không.
- Các mục menu được khớp theo tiêu đề và tiêu đề thay đổi theo ngôn ngữ giao diện.
- Đầu vào của bộ điều khiển thực không đi qua giao diện; giao diện có bộ điều khiển ảo riêng (`pad`/`srw64_pad`), được hợp nhất với đầu vào của bộ điều khiển thực.
- Giao diện được triển khai trên Windows (loopback TCP). 06-10-2026 Đã kết nối với máy thật AWS (Windows Server 2022, Tesla T4, D3D12): Trò chơi được bắt đầu với `Marchwind64.cmd --debug`, `ssh -L` trên máy Mac sẽ chuyển tiếp cổng trong `debug.json` và thư mục chạy cục bộ ghi `debug.json` (cổng, mã thông báo gốc) được chuyển tiếp và `remote.json`, `srw64_attach` (có chạy), trạng thái, ảnh chụp màn hình, phím, pad, ui.tree, ui.click, cài đặt, cửa sổ và chờ đều bình thường; ảnh chụp màn hình được truy xuất thông qua `file.read` (`local_file` lấy tên tệp theo đường dẫn Windows). Những cạm bẫy đã được khắc phục tại thời điểm đó: D3D12 `copyTextureRegion` của Plume xác nhận kết cấu trống khi sao chép vào bộ đệm và trò chơi đã bị hủy sau khi chụp ảnh màn hình đầu tiên (bản vá `prepare_rt64.py`). `Session.launch` (`srw64ctl launch`, `srw64_launch` của MCP) vẫn không khả dụng trên Windows: nó sử dụng `os.pipe` cộng với `pass_fds` để thoát trò chơi trong quá trình khởi động; đường dẫn người chơi (công tắc trong tùy chọn hoặc `--debug`, cộng với `srw64_attach`) không bị ảnh hưởng.

Việc quay lại trang trước chiến tranh có thể chạy `.venv/bin/python tools/recomp/debug/check_battle_ui.py`; quá trình phản công tinh thần và chủ động có thể chạy `.venv/bin/python tools/recomp/debug/check_battle_spirits.py`. Cả hai đều xây dựng máy chủ gốc hiện tại, truy cập thông qua menu chính `mini-enter` và không bật tính năng chọn ký tự cũ. `status.mini_stage.waiting_reason` chẩn đoán lý do cấp độ chưa sẵn sàng; chỉ `ready=true` bắt đầu hoạt động bản đồ. Ảnh chụp màn hình và kết quả xác nhận được lưu trong thư mục phiên gỡ lỗi tương ứng.

Việc thay đổi vũ khí trước trận chiến và niệm hồn ngay tại chỗ đều có thể thực hiện được. `.venv/bin/python tools/recomp/debug/check_battle_actions.py`: Nhập cấp độ nhỏ từ đầu để xác minh việc thay đổi vũ khí tấn công đang hoạt động, khấu trừ SP thực tế, làm mới hiệu ứng tinh thần, giữ lại lựa chọn phản công/né tránh, SP đồng điều khiển và bố cục gương trái và phải tiếng Trung/Nhật/Anh. Được thực thi thông qua `ui.click`, `ui.key`, `status.battle_page` và ảnh chụp màn hình GPU mà không ghi đè ảnh chụp nhanh trận chiến.