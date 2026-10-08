> **Ngôn ngữ / Language:** [Tiếng Việt](native-content-foundation.vi.md) · [English](native-content-foundation.en.md) · [中文](native-content-foundation.md)

# Kiến trúc nội dung gốc: đợt triển khai đầu tiên

Cập nhật phạm vi 12-09-2026: Chúng tôi sẽ tiếp tục quảng bá các mô-đun chức năng của riêng mình theo [Lộ trình MOD tích hợp](../design/mod-roadmap.md); việc đăng ký các loại nội dung bên ngoài, các gói phụ thuộc và quyền truy cập SDK công khai trong "lô công việc tiếp theo" trong bài viết này đang tạm thời bị đình chỉ. Các thư mục, hồ sơ, chuyển đổi ngôn ngữ và nghệ thuật hiện có tiếp tục được sử dụng lại.

2026-09-11 Sửa lỗi thời gian: Đã khắc phục sự cố ảnh chụp nhanh hội thoại của khung tiếp theo bị xóa do nhầm lẫn; bản dùng thử thông thường sẽ tắt ảnh chụp màn hình định kỳ và xuất bộ nhớ theo mặc định và bản thăm dò hoàn chỉnh vẫn có sẵn. Xem [Sửa lỗi nhấp nháy đối thoại](native-dialogue-flicker.md) để biết chi tiết.

Ngày: 2026-09-11. Lô này kết nối đường cơ sở JP thống nhất, thư mục ngôn ngữ bên ngoài, gói nghệ thuật độc lập và chuyển đổi hình ảnh sang máy chủ thực. Xem [sơ đồ kiến ​​trúc](../design/native-extensibility-architecture.md) để biết thiết kế tổng thể.

## Mục nhập có thể chạy được

Nhấp đúp vào `scripts/Play SRW64 Native.command` trong thư mục gốc của kho lưu trữ hoặc:

```sh
.venv/bin/python tools/recomp/run/play_native.py \
  --profile config/recomp/profiles/play-profile.json --new-game

# 同一个原始 ROM、同一个存档目录；启动时选择日文和原图。
.venv/bin/python tools/recomp/run/play_native.py \
  --profile config/recomp/profiles/play-profile.json --language ja --images original --new-game
```

Cấu hình mặc định là hội thoại tiếng Trung, hình ảnh độ phân giải cao, giọt nước nguyên bản và độ phân giải hiển thị bên trong gấp 4 lần. Nhấn **F6** trong khi thao tác để chuyển đổi qua lại giữa Gốc và HD và tiêu đề cửa sổ sẽ hiển thị chế độ hiện tại. Bắt đầu từ ngày 11-09-2026, mẫu 5600 cũng chuyển đổi: Original sử dụng hình dạng kim cương nguyên bản, còn HD sử dụng mẫu được chọn theo cấu hình. `presentation.model_5600: waterdrop` nghĩa là chế độ HD kích hoạt các giọt nước; khi được đặt thành `original`, cả hai chế độ đều duy trì kiểu gốc. F6 chỉ thay đổi lần chạy này; nhấn chọn hồ sơ/dòng lệnh cho lần khởi động tiếp theo. Ngôn ngữ, phông chữ gốc và độ phân giải hiển thị không thay đổi với nút chuyển này.

Lịch sử lưu của mục mới được thống nhất trong `build/recomp/profile-play/sessions/` và chế độ tiếng Nhật, tiếng Trung và hai chế độ hình ảnh có chung đặc điểm nhận dạng trò chơi JP. Bắt đầu từ ngày 12 tháng 9 năm 2026, khi `--new-game` không được chỉ định và lần lưu có thể xác minh gần đây nhất được chọn theo báo cáo chạy hoàn thành, nhận dạng ROM và bản tóm tắt cuối cùng, các bản sao bị lỗi sẽ được báo cáo và khôi phục; lần đầu tiên sử dụng bản sao lưu trữ phát lại tập JP gốc, bị khóa. Hỗ trợ lịch sử danh sách và lựa chọn rõ ràng, xem [Khôi phục lưu trữ](../guide/native-save-recovery.md) để biết chi tiết. Mục nhập ROM bản vá cũ đã bị xóa và các kho lưu trữ lịch sử sẽ không được tự động di chuyển.

Mục nhập này vẫn sử dụng `rom.z64` gốc cục bộ, bản dựng lại được tạo và tệp nghệ thuật đã được xác minh. RT64 sử dụng hình ảnh gốc khi tài nguyên thiếu một hình ảnh thay thế; bắt đầu từ ngày 12 tháng 9 năm 2026, Bản gốc có thể tiếp tục khởi động khi gặp gói HD/tệp hình đại diện bị thiếu và hiển thị rằng HD không khả dụng; lỗi vẫn được báo cáo nếu HD rõ ràng hoặc tóm tắt không khớp. Xem [Dự phòng gốc](native-original-fallback.md) để biết chi tiết. Phân phối gói cho các bản phát hành vẫn chưa được triển khai.

## Loại bỏ trách nhiệm

| Mô-đun | Trách nhiệm thực tế ở giai đoạn này |
| --- | --- |
| `src/srw64_native/catalog.py` | Tạo thư mục nguồn cục bộ từ ROM gốc cố định với bản đồ glyph; TextKey, đoạn trích văn bản nguồn, rào cản tập lệnh và xác thực tham số |
| `src/srw64_native/profile.py` | Phân tích ngôn ngữ, hình ảnh, mô hình, phông chữ và độ phân giải tương ứng; biên dịch cấu hình chạy bất biến |
| `src/srw64_native/assets.py` | Xác minh danh sách nghệ thuật thuần túy được phép và từng bản tóm tắt tệp, đồng thời xuất ra gói RT64 độc lập |
| `src/native/localization/` | Tìm kiếm TextKey trên máy chủ, dự phòng văn bản nguồn tương ứng, chuỗi giao diện người dùng phông chữ/ngôn ngữ/gốc |
| `src/native/game_adapter/dialogue_source.hpp` | Làm rõ rằng đoạn hội thoại tiêu chuẩn xuất phát từ bảng 0; xác định tập bản đồ phông chữ ràng buộc thực tế khi vẽ |
| `src/native/presentation/image_mode.hpp` | Chuỗi cửa sổ chỉ gửi yêu cầu chế độ hình ảnh và chuỗi kết xuất xác nhận ứng dụng |
| `src/host/` | Tiếp tục thực hiện cầu nối trò chơi hiện có, kiểm soát đọc và phụ trợ nền tảng; di dời dần, giữ lại cổng tiếp nhận hiện có |

Các tệp C biên dịch lại được tạo tự động không được di chuyển và trình tải mod mã thứ hai không được giới thiệu. `gameplay_mods` phải trống trong lô này để ngăn cấu hình có vẻ chấp nhận một mod trò chơi chưa thực sự được tải.

## Nội dung đa ngôn ngữ

Văn bản trò chơi gốc được tạo từ ROM cục bộ của người dùng. Bản dịch được chia thành hai phần, đều sử dụng Unicode và không chiếm hay mở rộng thư viện phông chữ N64:
- **Văn bản dữ liệu** (tên, nhãn, lời nhắc, bản ghi 0–5643): được mở rộng từ bảng nhập `content/locales/terms/` đến `tools/content/apply_terms.py` đến `content/locales/<语言>.json`, 4.712 mục nhập bằng tiếng Trung và tiếng Anh, xem [bảng nhập văn bản dữ liệu](localization-terms.md).
- **Cốt truyện và dòng chiến đấu**: Tệp văn bản dòng có thể thay đổi của người chơi `content/dialogue/<语言>/`, xem [Tệp văn bản dòng](../guide/dialogue-text.md).

Khi thiếu bản dịch, nhấn TextKey hoàn chỉnh để quay lại bản ghi nguồn tiếng Nhật tương ứng.

Ví dụ về TextKey là `base:t00_17412`; `base:t01_17412` của bảng khác là một bản ghi khác. Bộ điều hợp hội thoại tiêu chuẩn hiện tại xuất phát từ hàm ban đầu `8008C9C0` và lệnh gọi `8008CA5C..8008CA6C` của nó luôn chuyển vào bảng 0. Các trình sử dụng giao diện người dùng/văn bản khác vẫn phải điều chỉnh từng cái một và không thể tuyên bố là đã được Trung Quốc hóa chỉ vì thư mục chứa các bản ghi của họ.

Bản dịch cho phép thay đổi độ dài, ngắt dòng và phân trang đọc gốc. Thứ tự STOP/END phải được giữ nguyên, cũng như tên động/mã hình tượng đặc biệt trong mỗi đoạn. Những thay đổi trong tóm tắt văn bản gốc, khóa trùng lặp, khóa không xác định hoặc ký tự điều khiển không hợp lệ sẽ ngăn tải. Biên dịch nội dung chỉ đọc ROM gốc; không có thao tác chèn văn bản ROM nào được thực hiện.

Thêm ngôn ngữ: Thêm danh sách từ có cùng khóa với tiếng Trung và tiếng Anh trong `content/locales/terms/` và chạy `apply_terms.py`, đặt tệp dòng vào `content/dialogue/<语言>/`, đăng ký nó trong `locales` của cấu hình và bắt đầu với `--language <语言>`. Không có bảng liệt kê C++ cho thẻ ngôn ngữ nên không cần lập trình lại máy chủ cho các ngôn ngữ mới.

Bạn có thể biên dịch và xác minh trước mà không cần bắt đầu:

```sh
.venv/bin/python tools/content/compile_profile.py \
  --language zh-Hans --images original \
  --output build/recomp/content-preview
```

Đầu ra phải là một thư mục mới ghi lại ROM gốc, thư mục của tất cả các ngôn ngữ đã đăng ký, danh sách nghệ thuật và bản tóm tắt các tệp bản dựng. Thư mục đăng ký được xác minh và đóng băng trước khi khởi động; **F7 chuyển đổi ngôn ngữ nóng trong khi chạy, F6 chuyển đổi hình ảnh với 5600 model**. Chuyển đổi nóng sử dụng các thư mục bất biến và tham chiếu từng khung hình, đồng thời đoạn hội thoại hiện tại không chuyển sang clip tiếp theo. Xem [Ba lần xác minh cơ sở](native-foundations-verification.md) để biết cách thiết lập, báo cáo mức độ phù hợp và xác minh thực tế.

Hiện đang truy cập: đối thoại cốt truyện và trận chiến (UI đọc gốc) và tất cả các trang gốc (màn hình liên trò chơi, trang trước trận chiến, trang tên, cài đặt). Menu gốc, văn bản hình ảnh mở đầu và kết thúc, v.v. vẫn hiển thị hình ảnh gốc. Tên của nhân vật chính và đối tác không thể thay đổi. Tên mặc định được hiển thị theo ngôn ngữ đọc. Xem [Hiển thị tên mặc định bằng ba ngôn ngữ](default-names.md).

## Hình ảnh gốc và HD

`content/art/stage1-hd.json` liệt kê hai danh mục nghệ thuật HD (24-09-2026):

- **Thay thế hàm băm kết cấu RT64, 270 mục**: 213 cho bề mặt bản đồ thế giới câu chuyện (tài nguyên 5602–5606), 27 cho các vật thể vũ trụ, 30 cho các lát viền (13 cho hộp thoại, 17 cho HUD chiến đấu). Gói nguồn là `assets/hd-ai/worldmap-surfaces/pack-v5`. Hình ảnh phông chữ và các kết cấu khác trong gói không có trong danh sách và sẽ không được đưa vào trong quá trình biên dịch; quá trình lọc được hoàn thành trong quá trình biên dịch ngoại tuyến và danh mục tài nguyên không được đoán dựa trên tên tệp trong thời gian chạy.
- **Máy chủ vẽ toàn bộ bức tranh**: hình đại diện (phân đoạn`portraits`, xem [Hình đại diện nhân vật HD](native-portraits-hd.md)), nền liên trường (`backgrounds`, xem [Nền liên trường HD](native-backgrounds-hd.md)), Logo tiêu đề và ngọn lửa (`scene_images`, xem [màn hình tiêu đề và hình ảnh văn bản cốt truyện](native-title-and-story-images.md)). Cờ BANPRESTO, GAME OVER và đường viền cửa sổ không có trong gói và được tạo từ ROM khi trò chơi chạy (`src/host/rom_art.cpp`).

Cấu hình mặc định là `images: original`; bắt đầu bằng `--images hd` hoặc nhấn F6 trong trò chơi để sử dụng HD.

23-09-2026 Người ta phát hiện ra rằng quá trình xử lý độ trong suốt sớm nhất của hình đại diện có ba sai sót. Sau khi thay ảnh gốc thì bị lỗi viền avatar:

- Màu của các pixel trong suốt được lưu thành màu đen. Cả hai trang RT64 và RmlUi đều thực hiện lấy mẫu song tuyến tính dựa trên Alpha không được nhân trước, do đó các cạnh tối xuất hiện ở mép ngoài của đường viền.
- Đầu ra mô hình được offset và chia tỷ lệ tương ứng với ảnh gốc (Laurence được offset sang phải khoảng 1,5 pixel gốc, Manami được giảm khoảng 1%) và mặt nạ tuân theo đường viền offset. Kết quả là một mặt bị ăn mất, mặt còn lại mở rộng và 13–519 pixel truyền ánh sáng xuất hiện trong 2 pixel gốc bên trong đường viền.
- Nền xám tràn ngập khắp bốn phía của ảnh, đồng thời xuất hiện các điểm truyền ánh sáng trên quần áo và tóc bị cắt bởi khung (cạnh dưới và trên).

Sửa đổi [`portrait_matte.py`](../../tools/hd_ai/portrait_matte.py):

- Đầu tiên đăng ký đầu ra mô hình vào ảnh gốc;
- Đường viền chỉ được phép di chuyển trong phạm vi ±1,5 pixel gốc của mặt nạ ảnh gốc;
- Nền xám chỉ tràn ngập các pixel trong suốt của ảnh gốc;
- Các pixel trong suốt được lấp đầy bằng màu đồng nhất gần nhất;
- Tách riêng việc lấy mẫu lại màu và alpha khi thu nhỏ kích thước.

Đường viền IoU của bốn hình đại diện được sửa đổi là 0,984–0,994, đường cắt khung mờ 100% và số lượng pixel trong suốt trong đường viền là 0–3 (Đổ chuông Lanczos, Alpha ≥ 245). Sau khi khuếch đại song tuyến tính không nhân trước gấp 3 lần được mô phỏng, các pixel có độ lệch cạnh vượt quá 16 mức giảm từ 203/74/97/0 xuống 0. Những sửa đổi này hiện được sử dụng bởi toàn bộ quy trình hình đại diện và bạn có thể tìm thấy phương pháp tái tạo trong [Hình đại diện nhân vật HD](native-portraits-hd.md).

F6 không tải các kết cấu được GPU sử dụng. Chuỗi cửa sổ gửi yêu cầu; luồng gửi kết xuất chờ khối lượng công việc/hiện tại đã gửi hoàn thành và không hoạt động, sau đó thay đổi công tắc thay thế trong mutex bản đồ kết cấu của RT64. Bằng cách này, các bộ mô tả kết cấu và tỷ lệ UV được xây dựng ở cùng một chế độ; kết cấu vẫn được quản lý bởi RT64. Các điểm đánh dấu thay thế gốc của 5600 cũng được xây dựng theo chế độ được áp dụng: Bản gốc không thêm các điểm đánh dấu vẽ/triệt tiêu gốc và giữ lại đầy đủ tám mặt phẳng ban đầu; HD chỉ đánh dấu thay thế giọt nước. Công tắc này hiện hoạt động trên các gói nghệ thuật thuần túy và 5600 và không thể sử dụng trực tiếp khi kết nối bản đồ ngôn ngữ trong tương lai.

`image-mode.json` ghi lại chế độ được áp dụng và công tắc ghi `model_5600`, `image-mode-events.jsonl` thực tế; Siêu dữ liệu ảnh chụp màn hình GPU cho chế độ chẩn đoán đầy đủ bao gồm chế độ được áp dụng. Yêu cầu tệp `SRW64_WINDOW_CONTROL=1` để thử nghiệm có chung đường dẫn yêu cầu/ứng dụng như F6 và không sửa đổi bộ nhớ hoặc kho lưu trữ trò chơi.

## Ranh giới xác thực và theo dõi

Xác thực Python, kiểm tra yêu cầu chế độ/khóa văn bản C++/dự phòng và kiểm tra định dạng Văn bản cốt lõi thực tế được chạy riêng. Tập lệnh xác minh chuyến đi khứ hồi hình đại diện (`verify_profile_images.py`, đã xóa trong 5b997c7 với chế độ chẩn đoán đầy đủ vào ngày 2026-10-01) đã đạt đến cùng một phần của `base:t00_17412` trong câu chuyện trò chơi mới có thật vào thời điểm đó, thực thi hình ảnh gốc→HD→hình ảnh gốc→HD và kiểm tra xem trạng thái hội thoại vẫn không thay đổi và các pixel khứ hồi hình đại diện/khu vực bản đồ tĩnh nhất quán. Kết quả vận hành thực tế được thể hiện trong biên bản nghiệm thu ở cuối tài liệu này.

Đợt công việc tiếp theo:

1. Tiếp tục đưa các ứng dụng tiêu dùng như tên và menu vào dịch vụ TextKey; tên hiển thị mặc định và tên tùy chỉnh được xử lý riêng biệt để hoàn thiện giao diện người dùng lựa chọn ngôn ngữ tiếng Nhật và tiếng Trung.
2. Đăng ký loại nội dung SRW64 của N64ModernRuntime, các phụ thuộc gói bổ sung, xung đột phiên bản và tải; JSON bên ngoài hiện tại dành cho đầu vào phát triển và chưa phải là `.nrm`/SDK công khai.
3. Trích xuất lược đồ trường đã biết về cơ thể, nhân vật và vũ khí. Đầu tiên, quay đi quay lại mà không sửa đổi, sau đó chọn một trường để xác minh rằng trang dữ liệu, quyết toán thực tế và lưu là nhất quán.
4. Việc triển khai cấp độ và các sự kiện trước tiên được xử lý thông qua trích xuất/khứ hồi có cấu trúc; các đơn vị hoặc cấp độ mới được thêm vào yêu cầu xác minh dung lượng và lập bản đồ lưu trữ trước khi mở.


## 2026-09-11 Chấp nhận thực tế

- `make check`: 60 bài kiểm tra Python, biên dịch tất cả, kiểm tra phụ thuộc đã vượt qua; `make recomp-content-test`: Các bài kiểm tra khả năng thích ứng/nội dung C++ và các bài kiểm tra kiểm soát đọc/định dạng hội thoại Văn bản Cốt lõi thực tế đã vượt qua.
- Bốn cấu hình khởi động (tiếng Nhật/tiếng Trung × ảnh gốc/HD) được biên dịch và thông qua, tất cả đều là JP ROM bị khóa giống nhau. Bản tóm tắt mã nguồn máy chủ viết tay của hai máy thật nhất quán và ngôn ngữ được chọn thông qua dữ liệu.
- `build/recomp/profile-check/live-zh-3/`: 7848 VI thoát bình thường; `live-ja-3/`: 8064 VI thoát bình thường. Cả hai đều chạy từ trò chơi mới đến phân đoạn 1 của `base:t00_17412`.
- Mỗi ngôn ngữ thực sự ghi lại bốn khung hình ảnh gốc → độ phân giải cao → ảnh gốc → độ phân giải cao. ROI hình đại diện `[48,45,330,335]` có 70680 thay đổi pixel và ROI bản đồ `[0,0,100,45]` có 4500 thay đổi pixel; cả hai khu vực đều nhất quán từng pixel khi chuyển về ảnh gốc và độ phân giải cao. Diễn biến hội thoại, chủ nhân, số trang, diễn biến tiết lộ và nội dung không thay đổi trong quá trình cắt.
- 57 họa tiết bản đồ thế giới đã được xác nhận bằng cả hai ngôn ngữ để đạt kích thước 512×512 trong bộ đệm thực tế RT64, tỷ lệ UV 8x; các giọt bản địa được rút ra tương ứng 1398/1608 lần. Kiểm tra thủ công các ảnh chụp màn hình GPU đã hoàn thành để xác nhận rằng các mẫu Trung Quốc/Nhật Bản, nguyên bản/HD và hiện đại đều hợp lệ cùng một lúc.
- Đã xác nhận rằng phông chữ trong bản vẽ là tập bản đồ thời gian chạy 504×504; Không thể sử dụng trực tiếp tiêu đề tệp 504×252 của tài nguyên ROM gốc 1 làm điều kiện phán đoán để vẽ liên kết. Lớp thích ứng được xác định theo tập bản đồ thực tế. (Sửa vào ngày 2026-10-03: Các ký tự tiếng Trung hiếm có cỡ chữ ≥ 0x597 thực sự được lấy từ hình ảnh 504×252 của tài nguyên 1 và lớp thích ứng nhận dạng cả hai, xem [portable-text.md](portable-text.md).)

Bằng chứng tổng hợp: [acceptance.json](../../build/recomp/profile-check/acceptance.json). Ảnh chụp màn hình: [Hình ảnh gốc tiếng Trung](../../build/recomp/profile-check/live-zh-3/profile-checks/original.png), [HD tiếng Trung](../../build/recomp/profile-check/live-zh-3/profile-checks/hd.png), [HD tiếng Nhật](../../build/recomp/profile-check/live-ja-3/profile-checks/hd.png). Lần này không bao gồm toàn bộ trò chơi, di chuyển lưu tiếng Trung cổ hoặc tự động hóa bàn phím vật lý; F6 và các yêu cầu kiểm tra có chung đường dẫn ứng dụng.