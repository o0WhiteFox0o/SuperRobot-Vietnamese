> **Ngôn ngữ / Language:** [Tiếng Việt](portable-text.vi.md) · [English](portable-text.en.md) · [中文](portable-text.md)

# Đối thoại văn bản và trò chơi đa nền tảng tiếng Trung, tiếng Nhật và tiếng Anh

2026-09-20. Văn bản, tên, lời nhắc phân trang, tiến trình đọc, thanh dưới cùng và đánh giá về trò chơi thực tế hiện được sử dụng theo mặc định.
FreeType + HarfBuzz + ICU, pixel được chuyển giao cho [bộ tổng hợp Plume](plume-pixel-compositor.md).
Đối thoại không còn được liên kết với CoreText/CoreGraphics và không có tùy chọn để chuyển sang phần phụ trợ cũ. Phạm vi được hỗ trợ là `zh-Hans`, `ja`, `en`.
Menu, tên và cài đặt tiếp tục sử dụng SDL/RmlUi; ảnh chụp màn hình và lớp HD cũng đã được đổi thành Plume, hãy xem [Chuyển ba nền tảng](../design/three-platform-port.md).

## Đường dẫn thực tế

`src/host/dialogue_scene.cpp` triển khai `typeset()` và `rasterize_frame()` bằng cách sử dụng
`src/native/text/portable_text.*` sắp chữ và vẽ; `src/native/text/game_fonts.*` chịu trách nhiệm chọn phông chữ.
`src/host/dialogue_layout_adapter.hpp` Cung cấp phạm vi dòng/trang cho Trình đọc gốc và lưu nó trong Bố cục
TextLayout bất biến. Sau đó, khung trò chơi giữ vị trí glyph và byte phông chữ, đồng thời hiển thị từng từ chỉ thay đổi phạm vi hiển thị mà không cần sắp xếp lại.
Logic lật trang, đọc tự động, xem lại, chuyển đổi ngôn ngữ và xác nhận khách của Reader gốc vẫn không thay đổi.

2026-10-02 Cảnh đầu tiên được ghi lại dưới dạng một loạt các bước vẽ (điền hoặc một dòng văn bản), mỗi bước có một khóa (vẽ cái gì, ở đâu) và phạm vi pixel.
`rasterize_frame()` vẽ tất cả các bước theo trình tự; `IncrementalRaster` dùng để trình chiếu được so sánh với khung trước đó, chỉ tăng hoặc giảm là
Hình chữ nhật của bước này được vẽ lại và tải lên (khung vẽ thường trú của [Plume Compositor](plume-pixel-compositor.md)). Chỉ hiển thị nguyên văn từng bước
Vẽ lại vùng sọc của một dòng và thanh tiến trình đọc tự động chỉ vẽ lại thanh tiến trình; trước đây, mỗi khi trạng thái thay đổi, toàn bộ cửa sổ raster CPU và mới
Toàn bộ kết cấu cửa sổ được tải lên lại (16 MB mỗi khung hình ở 2560×1600, hiện tại là khoảng 1 MB, CPU 2,2 ms → 0,5 ms).
`tests/native_dialogue_raster.cpp` Bản vá xác minh từng khung hình sẽ giống như toàn bộ raster khung hình theo từng pixel sau khi được dán lại.

Quy tắc làm tối văn bản giống như phiên bản gốc: chỉ nhìn vào các byte bảng màu của slot văn bản +3 (`8008C5E4` điền vào bảng: 0 trắng = tài nguyên 2,
2 tối = tài nguyên 4). Khi cốt truyện chuyển sang hướng bên kia và cuộc trò chuyện là `8008FD40`, hãy viết vào ô cũ là 2; chiến tuyến là `8008FFAC`,
Không bao giờ viết số 2, vì vậy nó sẽ giữ nguyên màu trắng cho đến khi hộp biến mất. Dù đã đọc hay chưa (trạng thái +2: 1 lần đọc, 3 vẫn hiển thị sau khi đọc) không ảnh hưởng đến màu sắc.

Lớp đối thoại cũng được che phủ trong quá trình chuyển đổi: tác vụ chuyển tiếp `80099508` vẽ một hình chữ nhật có màu đen mờ cho mỗi dòng trong số 240 dòng trong mỗi khung, có đầu bên trái và bên phải
Các số dấu phẩy động theo từng dòng bắt đầu từ `0x8015E9C8`/`0x8015ED88` (các thao tác xóa và làm mờ khác nhau chỉ cập nhật hai bộ số này). Nhiệm vụ luôn tồn tại sau khi nó được tạo lần đầu tiên.
(xử lý `D_8015E9C0`), hai cột [0,1) và [319.320) vẫn được vẽ khi không hoạt động. Máy chủ đọc thanh màu đen của khung này khi gửi danh sách hiển thị,
Bị cắt bớt theo số nguyên của tác vụ, ánh xạ `wide_map::wipe_end` trên màn hình rộng (đầu bên trái 1 căn chỉnh với cạnh trái của màn hình, đầu bên phải ≥319 căn chỉnh với cạnh phải,
Phần còn lại được chia tỷ lệ theo chiều rộng của khung) và được vẽ vào lớp đối thoại như bước "xóa" cuối cùng. Trước đây, các từ sẽ trôi nổi trên cánh đồng mù màu đen, nơi các trận chiến xen kẽ giữa tấn công và phòng thủ.
2026-10-02 Mảng đo (`build/recomp/debug/20261002T120943.791168Z/cover-dump.json`): Mỗi hàng xen kẽ khi toàn màu đen
[0,319)/[1,320). Tôi đã từng mở rộng nhầm "từ 0" sang cạnh cửa sổ và [0,1) miễn phí đã xóa hộp thoại mở rộng bên ngoài 4:3 của chúng tôi.

Hình tượng của chính bản gốc sẽ bị xóa khỏi bản sao đã gửi của danh sách hiển thị bởi `take_frame` (hình chữ nhật E4 được vẽ bằng kết cấu phông chữ trong hộp thoại).
Mỗi glyph trong trò chơi có một kết cấu riêng biệt (`FD4800FB`): kích thước glyph < 0x597 sử dụng tài nguyên 0 (504×504), ≥ 0x597 sử dụng tài nguyên 0
Tài nguyên 1 (504×252, các ký tự tiếng Trung ít phổ biến hơn, chẳng hạn như xúc phạm hối hận; `sltiu 0x597` trong số `8008EE64`). Hai ảnh có cùng chiều rộng, chỉ có ảnh có tiêu đề họa tiết
Chiều cao khác nhau (`01F8`/`00FC`). Trước ngày 03 tháng 10 năm 2026, chỉ tài nguyên 0 được nhận dạng và hình tượng ban đầu của tài nguyên 1 vẫn còn trên màn hình với kích thước 1x pixel.
Chữ kanji tiếng Nhật được đặt chồng lên bản dịch ("Xúc phạm/Hối tiếc" cho "ブライ大帝", "Ran" cho "Ryuイン" trong trận chiến chứng minh danh hiệu); điều này không liên quan gì đến việc vẽ lại tăng dần.

ICU xử lý các ranh giới đồ thị và các lệnh cấm của Trung Quốc và Nhật Bản, định hình HarfBuzz và phạm vi bao phủ thang độ xám đầu ra FreeType.
Phần bù sử dụng đơn vị mã UTF-16; trình tự kết hợp, dòng mới rõ ràng và dòng trống được giữ nguyên. Bố cục được tạo một lần và được vẽ theo các hàng đã chọn
và hiển thị phạm vi đồ thị; khi độ rộng đường không đủ, chỉ xảy ra hiện tượng ngắt dòng khẩn cấp ở ranh giới đồ thị. Văn bản chính được cắt xén vào hộp thoại, nhãn và vùng đánh giá đều có vùng cắt xén.
Các pixel là BGRA8 từ trên xuống, được nhân trước alpha; ảnh chụp nhanh bố cục vẫn hợp lệ trên các kích thước ngôn ngữ/phông chữ và kết xuất GPU không đồng bộ.
Không có cam kết về tính năng khử răng cưa CoreText tương đương từng pixel hoặc hỗ trợ sản phẩm mở rộng cho tiếng Ả Rập, biểu tượng cảm xúc màu hoặc các ngôn ngữ khác.

## Phông chữ và phần phụ thuộc

Bản dựng phụ thuộc vào FreeType >= 2.10, HarfBuzz >= 2.8, ICU >= 70. Có sẵn trên macOS:

```sh
brew install freetype harfbuzz icu4c
```

Có thể cài đặt Linux `libfreetype6-dev libharfbuzz-dev libicu-dev fonts-noto-cjk`; xây dựng thành phần gốc cho Windows
Hiện đã có sẵn các chuỗi công cụ CMake (chẳng hạn như UCRT64) cung cấp ba thư viện được đề cập ở trên, nhưng bản dựng trò chơi Windows đầy đủ vẫn chưa có sẵn.

Bắt đầu từ ngày 23-09-2026, trò chơi sử dụng các phông chữ đóng gói: điểm trình khởi chạy `SRW64_FONT_DIR` đến `tools/content/prepare_fonts.py`
Các thư mục đã chuẩn bị sẵn (`build/fonts/` để chạy phát triển, `Contents/Resources/fonts/` cho các gói ứng dụng). Chuỗi phông chữ: tiếng Trung và tiếng Nhật
HarmonyOS Sans SC → Phông chữ ký hiệu `SRW64Symbols.ttf` → Biểu tượng nút `SRW64Prompts.ttf`; Tiếng Anh là HarmonyOS Sans Condensed → SC → Phông chữ biểu tượng → Biểu tượng nút. Ngoài ra còn có các biểu tượng dấu vũ khí trong phông chữ biểu tượng (cỡ chữ gốc U+E000+, xem [Màn hình sửa đổi](native-upgrade-screens.md)).
Gói phông chữ bắt đầu từ ngày 24-09-2026 là HarmonyOS Sans 2.040: `HarmonyOS_Sans_SC.ttf` (20,6 MB) và `HarmonyOS_Sans_Condensed.ttf` (0,3 MB) đều là các phông chữ có thể thay đổi (wght 40–900),
Mỗi tập tin chứa tất cả các trọng số. Khi `FontSource::weight` bằng 0, hãy sử dụng phiên bản mặc định của tệp Thông thường (400); các giá trị khác sử dụng phiên bản được đặt tên gần nhất trên trục wght,
Cả việc định hình và rasterization đều sử dụng trường hợp này. Menu tiêu đề và thẻ tiêu đề chương sử dụng `game_font_sources(locale, 700)`, là phiên bản Bold (706); phông chữ biểu tượng chỉ có một trọng lượng và không bị ảnh hưởng.
RmlUi tải lại phiên bản có cùng tên (Bình thường, Thông thường) theo từ được đưa ra bởi `LoadFontFace`. So với 1.0 Regular, kiểu chữ chỉ khác một chút:
"——" được nối thành chữ ghép, chữ ghép "Th" trong tiếng Anh và dấu ngoặc kép xoăn của tiếng Trung có độ rộng chênh lệch là 0,03 em; ngắt dòng và lật trang của 30 trường hợp sử dụng chung không thay đổi.
Khi thiếu tệp trong thư mục, lỗi sẽ được báo cáo rõ ràng và phông chữ hệ thống sẽ không được trả về. Vẫn đang tìm kiếm máy cục bộ khi không có `SRW64_FONT_DIR` (kiểm tra đơn vị, thăm dò cũ)
Noto Sans CJK (Linux), Arial Unicode (macOS), Microsoft Yahei (Windows); Noto chuẩn TTC chọn khuôn mặt tương ứng theo tiếng Trung/Nhật.
Có sẵn để phát triển và thử nghiệm `SRW64_TEXT_FONT` chỉ định tệp TTF/OTF/TTC rõ ràng; không tìm kiếm thư mục hiện tại hoặc tải xuống từ Internet.
Phông chữ được giữ theo bố cục sau khi được đọc. Tên phông chữ PostScript của macOS trong gói nội dung cũ không còn xác định phông chữ hội thoại và không cần phải nhập lại gói nội dung.
Gói ứng dụng phân phối gói phông chữ và giấy phép (`tools/release/package_macos.py`) với `Contents/Resources/fonts/`.

## Xác minh cục bộ

Tác vụ GitHub đã bị đóng và kho lưu trữ không giữ lại quy trình làm việc từ xa. Các thử nghiệm sau đây được thực hiện cục bộ mà không phụ thuộc vào ROM hoặc GPU:

```sh
# 完整游戏对白场景、原 Reader 和 UTF 转换；只使用 RT64 的 JSON 头文件。
cmake -S tests/dialogue_cpu -B build/dialogue-portable -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DSRW64_RT64_HEADERS="$PWD/build/recomp/upstream/RT64"
cmake --build build/dialogue-portable --parallel 6
ctest --test-dir build/dialogue-portable --output-on-failure

# 独立排版组件。也可以给出自己的本地 CJK 字体，跳过字体准备。
python tests/portable_text/prepare_fonts.py build/text-fonts
cmake -S tests/portable_text -B build/text-cjk -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DSRW64_TEST_CJK_FONT="$PWD/build/text-fonts/NotoSansCJKsc-Regular.otf" \
  -DSRW64_TEST_VARIABLE_FONT="$PWD/build/fonts/HarmonyOS_Sans_SC.ttf"   # 可选：字重检查
cmake --build build/text-cjk --parallel 6
ctest --test-dir build/text-cjk --output-on-failure
```

Các bài kiểm tra sắp chữ độc lập bao gồm sắp chữ hỗn hợp tiếng Trung, tiếng Nhật và tiếng Anh, các lệnh cấm, ký tự kết hợp, văn bản dài, phân trang, cắt xén, chia tỷ lệ, alpha nhân trước,
Bố cục cũ và sắp xếp lại đồng thời sau khi xóa tệp phông chữ; thử nghiệm kịch bản trò chơi bao gồm các hộp đôi, tên, nguyên văn, đánh giá, cột dưới cùng, thay đổi ngôn ngữ và kích thước phông chữ.
`SRW64_TEST_CJK_FONT` cũng có thể được chuyển tới CMake để kiểm tra cảnh hội thoại nhằm chỉ định rõ ràng phông chữ kiểm tra.
Kiểm tra thành phần và ảnh chụp màn hình trò chơi thực được ghi lại riêng biệt và toàn bộ trò chơi có thể chơi được trên Windows/Linux mà không cần CPU.

## Sự chấp nhận này

`make check` cục bộ: 260 mục nhập, 249 mục nhập đã vượt qua, 11 mục nhập bị bỏ qua; 4 thẻ CTest dành cho các thành phần văn bản độc lập và CPU hội thoại đầy đủ.
Trong trò chơi macOS thực đang chạy `build/recomp/portable-dialogue-02/`, trước tiên hãy nhập hồi quy bằng cách chia sẻ giao diện người dùng/tên và cốt truyện,
Sau đó, sử dụng `tools/recomp/verify/verify_portable_dialogue.py` để chuyển đổi tiếng Trung, tiếng Nhật và tiếng Anh, cỡ chữ 13/10/18, xem lại,
Cửa sổ 800×600 và 1100×760, chỉ phân trang trên máy chủ là nâng cao và tập lệnh gốc không nâng cao. Tổng cộng có 18 ảnh chụp màn hình GPU được lưu.
Báo cáo `portable-dialogue-verification.json` cho thư mục này; test game mới im lặng, độc lập, thoát bình thường.
Kiểm tra ảnh chụp màn hình đã phát hiện và khắc phục sự cố "toàn bộ văn bản có thể vừa khít, nhưng ngắt dòng sớm vì điểm ngắt dòng của ICU có chứa ngắt dòng".
Kiểm tra thành phần giữ lại hồi quy này. Kịch bản mới hoặc trò chơi đầy đủ này chưa được thực thi trên Windows/Linux và không có thành phần cũ nào được sử dụng để thử nghiệm nhằm đưa ra tuyên bố này.