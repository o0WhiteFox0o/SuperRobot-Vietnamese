> **Ngôn ngữ / Language:** [Tiếng Việt](native-rom-importer.vi.md) · [English](native-rom-importer.en.md) · [中文](native-rom-importer.md)

# Nhập lần đầu ROM gốc (giai đoạn nhập P1)

2026-09-20. Tiếp tục [Kế hoạch phát hành P0](cross-platform-release-plan.md). Trang này cập nhật trạng thái "Nhập lần đầu tiên chưa được triển khai": mã nhập, hệ thống dây khởi động và kiểm tra kiểm soát không có ROM đã được thêm vào; Việc phân phối ứng dụng macOS đầy đủ vẫn chưa hoàn tất. Host đồ họa vẫn chỉ hỗ trợ macOS, điều đó không có nghĩa là Win/Linux có thể chạy game.

## Lối vào hiện tại

Sau khi nhánh này được xây dựng theo `make` ban đầu, hãy chạy trực tiếp:

```sh
./build/recomp/gfx-build/srw64-gfx-host --play \
  --rom "$PWD/rom.z64" --language zh-Hans
```

`compile_profile.py`, `export_content.py` hoặc `--content` không còn cần thiết nữa. Lần đầu tiên C++ trích xuất nội dung từ ROM Rev 0 Nhật Bản phù hợp, sau đó xác minh và sử dụng lại bộ đệm. `--content` vẫn giữ khả năng cung cấp rõ ràng đường dẫn đến nội dung cục bộ hiện có cho nhà phát triển và không xóa phương pháp gỡ lỗi của P0.

Các bản dựng vẫn sử dụng Python; lần nhập đầu tiên và các lần chạy tiếp theo không khởi động Python, Git, CMake, Ninja hoặc trình biên dịch lại. CLI trò chơi không có tùy chọn để bỏ qua các bản tóm tắt ROM, ghi đè các cấu hình đã nhập hoặc chấp nhận các đường cơ sở tùy ý.

## Ranh giới trách nhiệm và nguồn lực

| Tài liệu | Trách nhiệm |
| --- | --- |
| `tools/release/build_import_spec.py` | Đọc bố cục được lưu trữ, ánh xạ glyph và thư mục ngôn ngữ khi xây dựng, xác minh khóa nguồn và tạo siêu dữ liệu được nhúng; không đọc ROM, không trích xuất tài nguyên game |
| `src/native/app/rom_import_codec.hpp` | Bảng văn bản được giới hạn, bộ đệm vòng LZ, bộ mô tả tài nguyên, giải mã hình đại diện 96/97 pixel |
| `src/native/app/portrait_png.hpp` | Đầu ra PNG hình đại diện RGBA8 nhỏ; kiểu lưu trữ DEFLATE, không phụ thuộc vào thư viện nén mới |
| `src/native/app/rom_import.cpp` | Xác minh danh tính, liên kết văn bản và bản dịch gốc, tạo hình đại diện, xác minh bộ đệm và phát hành cùng một bộ đệm byte ROM |
| `src/native/app/launch.cpp` | Nhập sau khi giữ khóa thư mục người dùng, sau đó sử dụng bootstrap gốc; không cập nhật được con trỏ lưu trữ |
| `tests/test_native_import.py` | So sánh với bộ giải mã Python hiện có, trình kiểm tra dịch, đầu ra pixel Gối |

Được nhúng trong chương trình là bố cục, ánh xạ ký tự Unicode, các bản dịch được lưu trữ và sao chép giao diện người dùng; bản ghi gốc tiếng Nhật và hình đại diện nhân vật đến từ ROM cục bộ của người chơi. Bộ nhớ đệm chứa nội dung bắt nguồn từ ROM và không được tải lên dưới dạng tài nguyên phát hành công khai. Đầu dò nhập khẩu chỉ được sử dụng để thử nghiệm và không được phân phối cùng với các chương trình trình phát.

Mã hóa nén PNG của đầu ra hình đại diện có thể khác với Gối; so sánh chấp nhận so sánh các pixel RGBA đã giải mã và không yêu cầu bản tóm tắt tệp PNG phải giống nhau. Các nội dung tóm tắt trong mục lục được tính toán dựa trên sản lượng thực tế tương ứng.

## Bộ nhớ đệm và xử lý lỗi

Thư mục bộ đệm nằm ở `content-cache/` của thư mục dữ liệu người dùng. Khóa là dấu vân tay SHA-256 đầy đủ của `(ROM SHA-256, importer version, embedded metadata SHA-256)`, giúp đường dẫn Windows không bị quá tải với hai thông báo dài. Cập nhật glyph, bản dịch hoặc trình nhập sẽ sử dụng thư mục mới và sẽ không ghi đè lên thư mục hợp lệ trước đó.

Khóa tệp hệ điều hành của cùng một thư mục người dùng luôn được giữ lại từ khi đọc và nhập cho đến khi kết thúc trò chơi. Đầu tiên hãy tạo một thư mục tạm thời độc lập trong cùng thư mục chính bộ đệm. Sau khi tất cả nội dung và bảng kê khai được viết và xác minh, hãy đổi tên nó thành thư mục chính thức. Các ngoại lệ sẽ xóa thư mục tạm thời hiện tại nhưng sẽ không xóa bộ đệm hoặc kho lưu trữ hiện có; thư mục `.tmp-` do quá trình này để lại sẽ không được coi là bộ đệm hợp lệ. Không có đảm bảo độ bền giao dịch ở mức độ mất điện.

ROM xấu, bộ mô tả ngoài giới hạn, cắt ngắn LZ, từ điều khiển không xác định, bản dịch lỗi thời, rào cản STOP/END hoặc tham số tên động được sửa đổi sẽ dừng quá trình nhập. Nếu bộ đệm xấu được báo cáo rõ ràng trong thư mục, bạn chỉ cần xóa thư mục con bộ đệm nơi lỗi được báo cáo sau khi đóng trò chơi, sau đó bắt đầu xây dựng lại. Không xóa toàn bộ thư mục người dùng hoặc `sessions/`.

## Xác minh

CI ba nền tảng công khai xây dựng lớp ứng dụng, nhà nhập khẩu và máy chủ giả mạo và không chạy trò chơi gốc. ROM tổng hợp không chứa mã trò chơi hoặc đồ họa trò chơi, bao gồm văn bản, thông số, 20 bảng siêu dữ liệu, chế độ LZ, 16 vị trí hình đại diện, 96/97 pixel, tái sử dụng/vô hiệu hóa bộ đệm, chuyển đổi dự phòng, khởi động lần đầu và khôi phục SRAM. Một trường hợp sử dụng khác xóa thư mục công cụ phát triển khỏi PATH để xác minh bootstrap gốc mà không cần gọi các công cụ bên ngoài.

Kiểm soát ROM thực là một thử nghiệm tùy chọn riêng biệt:

```sh
SRW64_TEST_ROM=/absolute/path/to/rom.z64 \
  ctest --test-dir build/native-app -C Release \
  -R native-import-oracle --output-on-failure
```

Điều này sẽ so sánh toàn bộ văn bản gốc, tất cả các bản dịch hợp lệ, bản đồ glyph và 16 pixel hình đại diện với cách triển khai Python hiện có. CI công khai không có ROM nên mục này rõ ràng bị bỏ qua; pass case sử dụng tổng hợp không bằng ROM thực hoặc quá trình trò chơi đã được chấp nhận.

## Vẫn còn thiếu

Lô này chỉ bao gồm Kết xuất gốc và không di chuyển các gói HD; chức năng HD của lối vào dùng thử Python cũ được giữ lại. Bắt đầu từ ngày 24 tháng 9 năm 2026, bạn có thể tạo gói ứng dụng HD đầy đủ để sử dụng cho riêng mình ([bản dựng tương thích cục bộ macOS](../native/macos-release.md#全-hd-自用包)): Tài liệu HD được đưa vào `Contents/Resources/hd` khi đóng gói và chỉ nội dung gốc mới được tạo từ ROM cho lần nhập đầu tiên. Lựa chọn tệp trên máy tính để bàn và bộ sưu tập dàn/phụ thuộc `.app` đã được thêm vào, hãy xem phần tiếp theo; Việc công chứng ID nhà phát triển, trò chơi thực và việc chấp nhận máy sạch vẫn chưa hoàn tất. Việc tách rời Metal/CoreText/AppKit, đồ họa Win/Linux, IME và gamepad vẫn đang trong giai đoạn sắp tới.

## P1b: cổng thông tin máy tính để bàn macOS và gói ứng dụng

P0/P1 đã được sáp nhập vào nhánh chính thông qua PR #2. Cổng máy tính để bàn chạy trong máy chủ đồ họa hiện có mà không cần thêm lớp khác.
Trình khởi chạy Python hoặc quy trình con. Bắt đầu sử dụng hộp chọn ROM hệ thống không có tham số; đọc thư mục người dùng vào lần sau
`last-rom.txt` và kiểm tra lại ROM. Khởi chạy bằng Tùy chọn hoặc khởi chạy bằng `--choose-rom`,
Bạn có thể chọn lại ROM. `--play` và các tham số thăm dò vị trí cũ không bật lên cửa sổ và tiếp tục được sử dụng để tự động hóa.

Chọn hộp sử dụng AppKit `NSOpenPanel`; sử dụng sai `NSAlert`. Không tiếp quản đại biểu ứng dụng của SDL,
Không mở một luồng GUI khác. Chỉ sau khi bootstrap gốc xác minh nội dung và kho lưu trữ, đồng thời giữ Khóa phiên, nó mới được lưu nguyên tử.
Đường dẫn ROM đã chọn. Hủy không tạo thư mục người dùng; ROM xấu có thể được chọn lại; cache, archive hay lỗi game chỉ báo lỗi và thoát.
Không khởi động lại trò chơi đã khởi tạo trong cùng một quy trình và không âm thầm mở các kho lưu trữ mới. Gói ứng dụng vẫn ở chế độ chỉ đọc.

Mã nằm ở `src/native/app/desktop.cpp`, `src/host/macos/desktop_macos.mm`; cái trước không có phụ thuộc GUI,
Cái sau là một bộ chuyển đổi Cocoa độc lập. Windows/Linux chỉ kiểm tra logic điều khiển chung và không có GUI cho hai hệ thống đó trong đợt này.

### Nhà phát triển tạo các gói ứng dụng cục bộ

Trước tiên, hãy hoàn thành bản dựng trò chơi theo `make` ban đầu, sau đó chỉ định rõ ràng mục tiêu macOS tối thiểu và xây dựng lại:

```sh
cmake -S src/host -B build/recomp/gfx-build -DCMAKE_OSX_DEPLOYMENT_TARGET=14.0
cmake --build build/recomp/gfx-build --target srw64-gfx-host --parallel 6
.venv/bin/python tools/release/package_macos.py \
  --binary build/recomp/gfx-build/srw64-gfx-host \
  --output "dist/SRW64 Recompiled.app" --minimum-macos 14.0
```

Thư mục đầu ra không được tồn tại. `tools/release/package_macos.py` là công cụ đóng gói và phát triển cục bộ và không được phân phối cùng với ứng dụng;
Nó sao chép rõ ràng tệp thực thi, phần phụ thuộc liên kết và quyền văn bản thuần túy được chỉ định qua `--license-file` mà không cần quét hoặc sao chép
Toàn bộ kho lưu trữ, ROM, lưu trữ, nhập bộ đệm hoặc phông chữ. Tạo `Info.plist`, gọi CMake BundleUtilities
Thu thập và định vị lại các phần phụ thuộc, xóa RPATH của máy xây dựng, sau đó xác minh các phần phụ thuộc và phiên bản hệ thống tối thiểu, rồi cuối cùng đăng nhập từ trong ra ngoài.

Phiên bản macOS tối thiểu là một ràng buộc đóng gói có thể kiểm chứng được, không phải là một tuyên bố tương thích chỉ sửa đổi phần chính. Bất kỳ lát Mach-O nào
Hoặc phiên bản tối thiểu của khai báo phụ thuộc cao hơn `--minimum-macos` sẽ không thành công; bạn cần biên dịch lại phần phụ thuộc hoặc chọn mức cao hơn và vượt qua
Phiên bản thấp nhất thực sự được xác minh. Lỗi không để lại nửa gói đã xuất bản cũng như không ghi đè lên `.app` cũ.

Chữ ký đặc biệt được sử dụng theo mặc định và chỉ được sử dụng để thử nghiệm cục bộ. Nó không bằng với bản phát hành ID nhà phát triển hoặc Gatekeeper.
`--sign-identity` có thể chỉ định danh tính ký tên của chính nhà phát triển; tập lệnh không lấy được thông tin xác thực, gửi để công chứng hoặc tải lên bản phát hành.
Giấy phép phụ thuộc hoàn chỉnh, chữ ký/công chứng và các yêu cầu về thời gian chạy cứng vẫn phải được xác minh trước khi phát hành. Gói ứng dụng với phông chữ đóng gói
HarmonyOS Sans (có giấy phép đầy đủ) và phông chữ ký hiệu.

### Đã thêm mức chấp nhận và ngưỡng còn lại

`tests/native_desktop.cpp` Hủy kiểm tra, đường dẫn ROM sai/thiếu/Unicode, ghi nhớ lựa chọn, không khởi động lại máy chủ,
Các kho lưu trữ lỗi không được đặt lại, khóa phiên thực và các thư mục làm việc không liên quan. `tests/test_macos_package.py` Danh sách trắng tệp thử nghiệm,
Không ghi đè, dọn dẹp ngoại lệ, ràng buộc phiên bản, RPATH và thứ tự lệnh gọi chữ ký.

macOS CI biên dịch bộ điều hợp Cocoa thực và đóng gói nó bằng một tệp thực thi không chứa mã trò chơi và kiểm tra thư viện động.
`tests/check_macos_bundle.py` ẩn thư mục thư viện nhị phân/thư viện động ban đầu và di chuyển `.app` tới đường dẫn chứa các ký tự tiếng Trung và dấu cách.
Đặt nó ở chế độ chỉ đọc, chạy và xem lại chữ ký trong môi trường đã loại bỏ các công cụ phát triển và biến ghi đè DYLD. Nó xác minh việc đóng phụ thuộc Mach-O thực tế,
Không mở hộp chọn modal, không chạy ROM, SDL hay GPU không có nghĩa là Finder → Import → Game đã được máy thực tế chấp nhận.

Việc chấp nhận macOS thực sự cũng yêu cầu: Nhấp đúp vào Finder, hủy, ROM lỗi, nhập lần đầu, khởi động lần thứ hai, chọn lại tùy chọn,
F7, nhập tên, lưu/thoát/khởi động lại, di chuyển ứng dụng, dọn dẹp máy mà không cần Homebrew/Xcode.
Lỗi nhanh `abort`/sự cố quy trình hiện tại không đảm bảo rằng hộp lỗi sẽ bật lên. Hộp thoại lỗi hiện tại bao gồm các lỗi khởi động có thể ghi lại và mã trả về.
Quá trình di chuyển màn hình trò chơi Metal/CoreText/AppKit vẫn đang trong giai đoạn tiếp theo và khả năng chơi trên Win/Linux chưa được công bố vào thời điểm này.

Tham khảo: [BundleUtilities](https://cmake.org/cmake/help/latest/module/BundleUtilities.html) chính thức của CMake,
[Câu hỏi thường gặp về công chứng] chính thức của Apple (https://developer.apple.com/documentation/security/resolving-common-notarization-issues).

### ICU và thư viện tải động

Trình đóng gói có thể liên tục chuyển `--search-dir` cho CMake để phân tích cú pháp các phần phụ thuộc `@loader_path` của các thư viện như ICU trên máy xây dựng.
Tương thích SDL2 tải SDL3 thông qua `dlopen`, không xuất hiện trong các phần phụ thuộc liên kết thông thường của SDL2; nó phải được sử dụng khi sử dụng lớp tương thích
Nhập `--runtime-library /path/to/libSDL3.dylib` một cách rõ ràng. Trình đóng gói sao chép dylib Mach-O theo tên được chỉ định,
Sau đó tập hợp các phần phụ thuộc của nó lại với nhau, kiểm tra phiên bản hệ thống tối thiểu, sửa đường dẫn và ký tên; toàn bộ thư mục phụ thuộc sẽ không được sao chép theo đợt.

Dưới đây là ví dụ về bản dựng lịch sử sử dụng thư viện Homebrew gốc. Vui lòng sử dụng phiên bản hệ thống thấp hơn
[Bản dựng tương thích gốc macOS](../native/macos-release.md), tái cấu trúc thư viện máy chủ và thời gian chạy từ nguồn cố định.

```sh
.venv/bin/python tools/release/package_macos.py \
  --binary build/recomp/macos-app-build/srw64-gfx-host \
  --output "dist/SRW64-237b629-macos-arm64/SRW64 Recompiled.app" \
  --minimum-macos 27.0 \
  --search-dir /opt/homebrew/opt/icu4c/lib \
  --runtime-library /opt/homebrew/opt/sdl3/lib/libSDL3.dylib
```

20-09-2020 Các yêu cầu bồi thường Mach-O cho SDL3 gốc ít nhất là macOS 27, ngay cả khi máy chủ được xây dựng bằng 26 thì toàn bộ gói phải yêu cầu 27.
Các gói dành cho hệ thống cũ hơn yêu cầu các bản dựng phụ thuộc phù hợp và không thể thay đổi Info.plist. Gói ứng dụng chỉ được ký đặc biệt tại địa phương và không được công chứng.