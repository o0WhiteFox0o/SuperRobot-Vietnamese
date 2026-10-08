> **Ngôn ngữ / Language:** [Tiếng Việt](macos-release.vi.md) · [English](macos-release.en.md) · [中文](macos-release.md)

# bản dựng tương thích gốc macOS

Phát hành mục tiêu xây dựng Apple Silicon, macOS 14.0. Mục tiêu này phải được sử dụng cho máy chủ và tất cả các phần phụ thuộc trong thời gian chạy;
Không thể đạt được khả năng tương thích bằng cách hạ thấp Info.plist hoặc ghi đè trường phiên bản của dylib được tạo sẵn.
Việc xây dựng, kiểm tra Mach-O và chạy trò chơi trên hệ thống mới chỉ có thể chứng minh kết quả của quá trình xây dựng và chạy trên máy hiện tại;
Quá trình khởi động và chơi game thực tế của macOS 14/15 vẫn cần được hệ thống tương ứng chấp nhận.

## Sự phụ thuộc

`config/recomp/macos-dependencies.json` Đã sửa lỗi SDL3, tương thích SDL2, FreeType, HarfBuzz, ICU
URL mã nguồn và SHA-256. `tools/release/build_macos_dependencies.py` được tải xuống, xác minh và xây dựng từ mã nguồn.
Cài đặt vào `build/macos-deps/14.0-arm64/prefix` mà không thay đổi thư mục hệ thống hoặc Homebrew.
Công cụ xây dựng vẫn có thể đến từ Homebrew; các thư viện thời gian chạy không được liên kết với đường dẫn Homebrew.

Giữ đường dẫn API SDL2 → SDL2-compat → SDL3 hiện có. Văn bản sử dụng OpenType của FreeType + HarfBuzz
Sắp chữ và phân đoạn ICU; tắt HarfBuzz CoreText, GLib, Graphite2, các công cụ trợ năng và FreeType
PNG/Brotli/BZip2 và các phần phụ thuộc khác không được văn bản TTF/TTC hiện tại sử dụng. Gói ứng dụng đi kèm với các phông chữ được chuẩn bị bởi `tools/content/prepare_fonts.py` (HarmonyOS Sans 2.040 nguyên bản với toàn bộ văn bản của giấy phép và các phông chữ có chữ ký).

Chuẩn bị chuỗi công cụ cố định và mã được tạo của dự án ban đầu và chạy:

```sh
.venv/bin/python tools/release/build_macos_dependencies.py --jobs 8

release_deps="$PWD/build/macos-deps/14.0-arm64/prefix"
cmake -S src/host -B build/recomp/macos14-app-build -G Ninja \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_C_COMPILER=/usr/bin/clang -DCMAKE_CXX_COMPILER=/usr/bin/clang++ \
  -DCMAKE_OSX_DEPLOYMENT_TARGET=14.0 -DCMAKE_OSX_ARCHITECTURES=arm64 \
  -DCMAKE_PREFIX_PATH="$release_deps" \
  '-DCMAKE_IGNORE_PREFIX_PATH=/opt/homebrew;/usr/local' \
  -DSDL2_DIR="$release_deps/lib/cmake/SDL2" \
  -DICU_ROOT="$release_deps" \
  -Dharfbuzz_DIR="$release_deps/lib/cmake/harfbuzz" \
  -DSRW64_ENABLE_RT64=ON -DSRW64_METAL_SOURCE_SHADERS=ON \
  -DPython3_EXECUTABLE="$PWD/.venv/bin/python"
cmake --build build/recomp/macos14-app-build --target srw64-gfx-host --parallel 8

.venv/bin/python tools/release/package_macos.py \
  --binary build/recomp/macos14-app-build/srw64-gfx-host \
  --output "dist/Marchwind64-macos14-arm64/Marchwind64.app" \
  --minimum-macos 14.0 --search-dir "$release_deps/lib" \
  --runtime-library "$release_deps/lib/libSDL3.dylib"
```

Sử dụng thư mục bản dựng mới để tránh sử dụng lại bộ đệm CMake chứa đường dẫn thư viện Homebrew. Trình đóng gói từ chối ghi đè đầu ra hiện có;
Thay đổi thư mục đầu ra khi đóng gói nhiều lần. SDL3 được lớp tương thích tải động và phải được chuyển rõ ràng tới trình đóng gói.
Báo cáo xây dựng phần phụ thuộc trong `build/macos-deps/14.0-arm64/dependencies.json`; người đóng gói kiểm tra tất cả
Phiên bản hệ thống tối thiểu, đường dẫn phụ thuộc và chữ ký cho Mach-O. Toàn bộ quá trình chỉ chạy cục bộ và không sử dụng Tác vụ GitHub.

Sản phẩm chỉ được ký đặc biệt cục bộ và không có công chứng ID nhà phát triển. Bạn nên mang theo hướng dẫn cấp phép cho từng phần phụ thuộc trước khi phân phối nó ra bên ngoài.

## Gói cá nhân Full HD

Gói được sản xuất theo mặc định chỉ có màn hình gốc. Để đóng gói một gói cho phép tất cả HD theo mặc định, trước tiên hãy chuẩn bị thư mục HD rồi chuyển `--hd` khi đóng gói:

```sh
.venv/bin/python tools/release/prepare_hd_bundle.py --output build/release/hd-$(date +%F)
.venv/bin/python tools/release/package_macos.py ...（同上） --hd build/release/hd-$(date +%F)
```

- `prepare_hd_bundle.py` biên soạn danh sách nghệ thuật `content/art/stage1-hd.json` từ máy cục bộ `assets/`: bề mặt bản đồ thế giới,
Có 270 kết cấu thay thế RT64 cho các vật thể không gian, hộp thoại và đường viền HUD chiến đấu, 304 hình đại diện đầy đủ, 17 hình nền liên trường và 19 hình ảnh tiêu đề.
Sau đó, hình đại diện và hình nền được chuyển đổi thành JPEG (chất lượng 95, không lấy mẫu sắc độ) bởi [`compress_hd.py`](../../tools/release/compress_hd.py):
Màu của hình đại diện được lưu dưới dạng `.jpg` và độ trong suốt được lưu dưới dạng `.alpha.png` (thang độ xám cộng với độ trong suốt, thang độ xám là màu hình bóng). Cả hai được hợp nhất khi trò chơi được tải;
Nền mờ và chỉ có một `.jpg` được lưu trữ. PSNR đo được của hình đại diện không nhỏ hơn 44,6 dB, trung vị là 47,4 dB và độ trong suốt không thay đổi từng pixel;
PSNR nền không nhỏ hơn 46,9 dB. Hoạ tiết và hình ảnh tiêu đề RT64 vẫn là PNG.
Nó cũng xây dựng chỉ mục cho hình đại diện của trang gốc (hình ảnh, bảng màu) và hình bóng trực tiếp sử dụng `.alpha.png` của hình đại diện; sau đó xác minh và sao chép
Gói bản đồ thế giới về tàu và cột mốc (`build/recomp/native-models/assets`) và gói 5600 điểm đánh dấu
(`build/recomp/native-marker/assets`). Bản đồ chiến thuật được nhập vào `art/maps` cùng với danh sách nghệ thuật và bản đồ cơ sở được chuyển đổi thành JPEG, khoảng 350 MB.
Phần nghệ thuật đã giảm từ khoảng 315 MB xuống còn khoảng 151 MB: hình đại diện 182 → 60 MB, nền 45 → 10 MB và hình bóng 7 MB không còn được lưu trữ riêng.
- Khi trình khởi chạy nhìn thấy `Contents/Resources/hd/art`, hãy đặt `SRW64_ART_PACK` để bắt đầu bằng HD (`SRW64_IMAGE_MODE=hd`),
Kết nối hình ảnh HD với hình đại diện trên trang tên, trang xác nhận trước chiến tranh, trang lưu trữ và liên kết, đồng thời đặt lại chúng khi có hai gói mô hình.
`SRW64_NATIVE_MARKER`, `SRW64_NATIVE_MODELS`. F6 hoặc cửa sổ cài đặt có thể chuyển về phiên bản gốc và chọn không ghi file cài đặt.
- Lần nhập đầu tiên vẫn chỉ tạo nội dung gốc từ ROM; nhà nhập khẩu phiên bản 3 ghi chú hình đại diện chiến đấu (hình ảnh, bảng màu) và bộ đệm cũ sẽ được nhập lại một lần.
- Loại gói này chỉ dành cho mục đích sử dụng riêng của nhà đóng gói: giấy phép phân phối của AI Art chưa được xem xét và hai gói mô hình đều chứa các byte tham chiếu được sao chép từ ROM.
`Distribution.txt` sẽ biểu thị không phân phối.
Tối thiểu 27 gói kế thừa hiện có đến từ các mục tiêu triển khai cho các tệp nhị phân Homebrew gốc, không phải các yêu cầu về mã nguồn cho SDL hoặc các thành phần chữ.

## Xác minh cục bộ (2026-09-20)

`build/recomp/macos14-game-01/bundle-verification.json` ghi lại 8 Mach-O cho các gói mới
(Chương trình chính và 7 dylib) Tất cả được khai báo tối thiểu 14.0. Khởi chạy trò chơi thực từ `/tmp`, giảm PATH,
Nhật ký tải động không có Homebrew hoặc thư mục bản dựng phụ thuộc, SDL3 từ gói ứng dụng, mã thoát 0, kiểm tra chữ ký đã vượt qua.
Xác thực giao diện người dùng được chia sẻ trong cùng thư mục bao gồm các menu ứng dụng, phím tắt, ghi lại tên và chia tỷ lệ cửa sổ Retina; ghi đè xác thực đối thoại
Tiếng Trung, tiếng Nhật và tiếng Anh, cỡ chữ, lịch sử và lật trang, tổng cộng 18 ảnh chụp màn hình GPU. 4 bước kiểm tra văn bản/hộp thoại C++ tương ứng với phần phụ thuộc mới được thông qua.

Máy chạy trên là macOS 27; chúng tôi không thể khẳng định rằng macOS 14/15 đã hoàn thành quá trình chấp nhận máy thực tế dựa trên điều này.