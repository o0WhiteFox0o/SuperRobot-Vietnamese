> **Ngôn ngữ / Language:** [Tiếng Việt](release.vi.md) · [English](release.en.md) · [中文](release.md)

# Phát hành bản dựng

Có hai tệp tải xuống để phát hành công khai: nội dung ứng dụng (màn hình gốc) và gói hình ảnh HD có thể tải xuống riêng.
Cả hai đều được xây dựng từ một cam kết duy nhất của `tools/release/build_release.py` và không bị ảnh hưởng bởi những thay đổi không được cam kết từ các phiên khác trong không gian làm việc chung.
Kịch bản chỉ chịu trách nhiệm xây dựng chứ không chịu trách nhiệm xuất bản; xuất bản là một bước thủ công khác.

## Xây dựng một lần

```sh
.venv/bin/python tools/release/build_release.py --commit HEAD --version 0.4.2
```

- Thư mục đầu ra mặc định là `build/release/<版本>-<短提交号>` và từ chối ghi đè nếu nó đã tồn tại. Bạn có thể sử dụng `--output` để chỉ định và `--keep-source` để giữ lại thư mục thanh toán và các sản phẩm đã tổng hợp.
- Điều kiện tiên quyết: Không gian làm việc chính đã có `build/recomp/{upstream,tool-build,cpu-scan}` được tạo bởi `rom.z64`, `assets/`, `make all` và
[các phần phụ thuộc của macOS](../native/macos-release.md)(`build/macos-deps/14.0-arm64/prefix`).

Các bước:

1. Sử dụng `git worktree add --detach` để kiểm tra cam kết `输出目录/src`.
2. Liên kết ROM vào; `hd-ai`, `fonts`, `models` trong `assets/` được sao chép bằng cách sao chép khi ghi (biên dịch nghệ thuật không chấp nhận các đường dẫn trỏ ra ngoài thư mục thanh toán) và phần còn lại được liên kết.
3. Sao chép mã nguồn ngược dòng và các công cụ đã biên dịch của chuỗi công cụ cố định, khôi phục RT64 (bao gồm các mô-đun con) về trạng thái ban đầu bị khóa (các thay đổi RT64 không được cam kết từ các phiên khác trong không gian làm việc chính sẽ không trộn lẫn và sẽ không bị `prepare_rt64.py` từ chối), sau đó chỉ tạo lại mã đã gửi: mã CPU, bản vá RT64, lớp thích ứng giao diện người dùng, vi mã âm thanh, phông chữ.
4. Chạy tất cả các bài kiểm tra Python.
5. Biên dịch từ đầu trên macOS 14/arm64 và tạo gói ứng dụng.
6. Xây dựng lại gói mô hình tàu và gói 5600 mark, tạo gói HD và đính kèm `tools/release/hd-notice.txt` (phương pháp cài đặt, nguồn tạo AI, tuyên bố không chính thức).
7. Hai tệp được nén bằng `ditto --norsrc --noextattr`: không có `__MACOSX` và các thuộc tính mở rộng như cách ly và nguồn, chúng vẫn hợp lệ sau khi giải nén bằng cách áp dụng chữ ký.
8. Viết ra `release.json` (cam kết, phiên bản, kích thước của hai tệp và SHA-256, `hd.json` đối với gói HD, lệnh phát hành)
và ghi chú phát hành được điền theo `tools/release/release-notes.md`.

Toàn bộ quá trình thực sự mất khoảng 3 phút: chưa đầy một phút để biên dịch 942 bước từ đầu và khoảng 40 giây để kiểm tra.

### Phiên bản beta nội bộ (có ROM và HD, không phân phối bên ngoài)

29-09-2026 Người dùng muốn có phiên bản beta nội bộ có cài đặt ROM. Đầu tiên thêm `--keep-source` để build như trên, sau đó đưa chương trình đã biên dịch, `pack/hd` và ROM vào ứng dụng:

```sh
cd build/release/<版本>-<提交>/src
PYTHONPATH=src:tools ../../../../.venv/bin/python tools/release/package_macos.py \
  --binary build/recomp/macos14-app-build/srw64-gfx-host --output "../app-internal/Marchwind64.app" \
  --version <版本> --minimum-macos 14.0 --search-dir ../../../macos-deps/14.0-arm64/prefix/lib \
  --runtime-library ../../../macos-deps/14.0-arm64/prefix/lib/libSDL3.dylib \
  --fonts build/fonts --dialogue content/dialogue --hd ../pack/hd --rom rom.z64
```

- `--rom` Đầu tiên nhấn `config/recomp/rom-variants.json` để kiểm tra SHA-256, chỉ chấp nhận phiên bản tiếng Nhật Rev 0; ROM được đưa vào `Contents/Resources/rom.z64`, `Distribution.txt` Dòng đầu tiên ghi là bản thử nghiệm nội bộ, chứa ROM và không được phép xuất.
- ROM được đóng gói khi khởi động (`src/host/host.cpp`) thay thế hộp chọn ROM bật lên lần đầu: máy Mac này vẫn sử dụng ROM đã ghi nhớ khi ghi nhớ các ROM khác; nhấn giữ Tùy chọn hoặc `--choose-rom` và hộp chọn vẫn bật lên.
- Ứng dụng này không nhập `release.json` và cũng không được nén thành tệp phân phối; Bản thân `build_release.py` không bao giờ đi kèm với ROM.

### Đính kèm gói cho nền tảng khác

Các gói Linux và gói Windows được xây dựng theo quy trình làm việc `build` của GitHub Actions (`.github/workflows/build.yml`; đẩy thẻ chính, đẩy thẻ `v*` hoặc kích hoạt thủ công):
Trên Ubuntu, mã trò chơi được tạo từ ROM của kho lưu trữ riêng `dyzz/srw64-ci-inputs`, được mã hóa và chuyển giao cho Windows (clang-cl) và Linux (với `tools/release/linux/build.sh`
Cùng một bộ chứa Ubuntu 22.04) hai tác vụ; thành phẩm cũng được mã hóa và tải lên (bất kỳ ai cũng có thể tải xuống sản phẩm trong kho công cộng) và sử dụng `~/.config/srw64/ci-artifact-key` cục bộ để mở khóa:

```sh
gh run download <运行号> --repo dyzz/srw64-recomp -n Marchwind64-linux-x64-encrypted
openssl enc -d -aes-256-cbc -pbkdf2 -iter 200000 -pass file:$HOME/.config/srw64/ci-artifact-key -in Marchwind64-linux-x64.tar.gz.enc -out Marchwind64-linux-x64.tar.gz
```

Gói Windows cũng được tải xuống dưới dạng `Marchwind64-windows-x64-encrypted`. Sau khi giải nén sẽ là thư mục `Marchwind64-windows-x64`, nén thành zip và đính kèm.
Tải xuống gói Android `SRW64-android-arm64-encrypted` và sau khi giải nén là APK (CI được ký bằng khóa phát hành trong kho, có thể ghi đè và cài đặt phiên bản cũ và giữ lại kho lưu trữ);
`android:versionName` và `versionCode` nằm trong `tools/release/android/app/AndroidManifest.xml`, sẽ được thay đổi cùng với thư mục gốc `CMakeLists.txt` khi phát hành phiên bản.
(versionCode = phiên bản chính × 10000 + phiên bản phụ × 100 + số sửa đổi, 0.4.0 là 400 và chỉ có thể được phóng to hơn; `tests/test_release_version.py` Kiểm tra xem ba vị trí có nhất quán không). Hình ảnh bìa hơi nước `tools/release/linux/steam-art/` trong kho
(`steam_art.py` được tạo từ hình ảnh tiêu đề HD. Nếu bạn thay đổi hình ảnh tiêu đề, hãy tạo lại và gửi nó). Gói Linux do CI xây dựng cũng có vỏ bọc.

Các gói Linux vẫn có thể được xây dựng nguyên bản (`tools/release/linux/build.sh` hoặc `build_linux.py` khi kiểm tra sạch), các gói Windows chỉ được tạo bởi Hành động,
Chuyển `--attach` cho cùng `build_release.py` và đặt nó vào cùng bản phát hành với gói Mac và gói HD:

```sh
.venv/bin/python tools/release/build_release.py --commit HEAD --version 0.4.2 \
  --attach linux=build/deck/<提交>/src/build/linux-x64/Marchwind64-SteamDeck-0.4.2-<日期>-<提交>.tar.gz \
  --attach windows=build/windows/<提交>/Marchwind64-0.4.2-windows-x64.zip \
  --attach android=build/android/<提交>/SRW64-android-arm64-<提交>.apk
```

Các tệp đính kèm được đổi tên thành `Marchwind64-<版本>-linux-x64.tar.gz`, `Marchwind64-<版本>-windows-x64.zip`, `Marchwind64-<版本>-android-arm64.apk`, bảng tải xuống, ba vị trí cài đặt nền tảng của gói HD, giá trị kiểm tra và
Các lệnh phát hành của `release.json` được tạo theo gói đính kèm. Cả ba nền tảng đều có chung gói HD; nó chỉ có thể được xây dựng nguyên bản (tài sản không được đưa vào kho), vì vậy nó luôn được tạo ra từ bước này.
Các gói đính kèm phải đến từ cùng một nội dung gửi: Các gói HD chỉ khớp với cùng một phiên bản của ứng dụng.

## Xuất bản

Sau khi xác nhận `release-notes.md` và hai tệp, hãy thực thi lệnh `gh release create` được ghi chú trong `release.json` trong `publish`.
Thẻ được ghim vào cam kết tại thời điểm xây dựng bằng `--target`. GitHub có giới hạn 2 GB cho một tệp đính kèm và cả hai tệp đều nhỏ hơn đáng kể so với giới hạn đó.

## Nội dung và ràng buộc của gói HD

- Nghệ thuật đến từ nội dung gốc được tham chiếu bởi `content/art/stage1-hd.json`; gói và gói mã thông báo được xây dựng lại từ các tập lệnh trong cam kết, ngoại trừ byte ROM.
- Các biểu đồ AI trong gói không ghi siêu dữ liệu AIGC mà chỉ được khai báo bằng văn bản trong mô tả gói và ghi chú phát hành.
- Gói HD công khai là một thư mục HD hoàn chỉnh, giống như thư mục dành cho mục đích sử dụng cá nhân (28/09/2026 do người dùng xác định): kết xuất nội dung, biểu tượng nội dung bản đồ và
Bản đồ chiến thuật HD (bao gồm cả hình ảnh được mã hóa màu) được bao gồm trong gói và THÔNG BÁO cũng như ghi chú phát hành cho biết rằng chúng được phóng to pixel so với bản gốc. Gói công khai trước đó đã xóa bản đồ và biểu tượng chiến thuật (`ROM_DERIVED*`) và đã bị hủy.
- Logo BANPRESTO và GAME OVER ở viền cửa sổ HD và hình ảnh tiêu đề được trò chơi tạo ra từ ROM riêng của người chơi khi chạy (99d5cb2, 7b0d7f5),
Họ không có trong danh sách nghệ thuật.
- Trình phát đưa thư mục `hd` đã giải nén vào thư mục người dùng (`~/Library/Application Support/SRW64Recomp/hd` đối với macOS),
Hoặc đặt nó vào thư mục chứa trò chơi (bên cạnh `Marchwind64.app`, `marchwind64.sh`, `Marchwind64.exe`, `beside_game`),
Trình khởi chạy bắt đầu ở chế độ HD. Thứ tự tìm kiếm: Danh mục người dùng → Bên cạnh trò chơi → Đi kèm với ứng dụng (`Contents/Resources/hd`);
Nếu thư mục không đầy đủ hoặc phiên bản không chính xác thì lỗi sẽ được báo cáo và phiên bản gốc (`src/native/app/launch.cpp`) sẽ không được trả về một cách lặng lẽ. Trên macOS chưa được di chuyển trong Finder
Ứng dụng đã tải xuống sẽ được hệ thống chuyển sang bản chỉ đọc (App Translocation). Tại thời điểm này, không thể nhìn thấy `hd` bên cạnh; Android không có thư mục game và chỉ nhận dạng thư mục người dùng.
- Gói HD chỉ đi kèm với các ứng dụng cùng phiên bản. Lược đồ hoặc định dạng dữ liệu HD của `hd.json` đã thay đổi và các ứng dụng mới cũng như gói HD mới phải được gửi cùng lúc.
- Tập (`tools/release/compress_hd.py`, 2026-09-28): Toàn bộ ảnh được lưu ở chất lượng JPEG 92, 4:2:0, nếu trong suốt thì lưu ở thang độ xám và PNG trong suốt.
Kết xuất phần thân giảm từ 8x xuống 6x pixel ROM và cạnh dài không vượt quá 1024 px; trang xác nhận trước chiến tranh chỉ hiển thị tối đa khoảng 830 px (mật độ 2) hoặc 980 px (mật độ 3).
Hình đại diện vẫn ở mức 768 px và bản đồ chiến thuật vẫn ở mức 4x vì chúng không đủ lớn ở chế độ toàn màn hình. Hoạ tiết RT64 chỉ có thể là PNG hoặc DDS,
Vì vậy, chỉ loại bỏ kênh trong suốt khỏi kênh mờ đục; BC7 sẽ phóng to hình ảnh cận cảnh của bản đồ thế giới thành dạng khối nên không được sử dụng. Kết quả: Full HD giảm từ 708 MB xuống 409 MB (~400 MB sau khi nén),
Gói công khai bây giờ giống nhau; PSNR được lấy mẫu là 44 cho ảnh chân dung, 42 cho hình đại diện và 41 dB cho bản đồ.
- **Gói HD phiên bản cầm tay: đã nghiên cứu, chưa làm** (29/09/2026 user: "Để nghiên cứu nhé, tạm thời sẽ full HD"). Ý tưởng là cung cấp gói độ phân giải thấp cho các máy chơi game cầm tay 1280×800 như Steam Deck, trong khi máy tính để bàn vẫn giữ nguyên như cũ.
Dựa trên việc lấy mẫu theo từng lớp và ước tính độ nén nặng của gói 0.3.0 HD (385 MB zip), gói này chỉ có thể tiết kiệm khoảng 30%, xuống còn khoảng 265 MB:

| Phần | Bây giờ | Ước tính phiên bản cầm tay | Mô tả |
| --- | --- | --- | --- |
| Bản đồ chiến thuật | 219 MB | Khoảng 140 MB | Ban đầu chỉ gấp 4 lần phiên bản gốc, nó được hiển thị trên Bộ bài 3,33 lần. Việc giảm kích thước tiết kiệm được rất ít, chủ yếu dựa vào JPEG 92→85; bản đồ màu có dung lượng khoảng 39 MB và không thể di chuyển được (hàng xóm gần nhất được sử dụng để thu phóng và phép nội suy tuyến tính làm cho nó lớn hơn) |
| Bản đồ thế giới (kết cấu RT64 512²) | 83 MB | 83 MB | Góc nhìn cận cảnh trên Deck yêu cầu 10–17x, 8x là chưa đủ và không thể giảm |
| Hình đại diện | 38 MB | Khoảng 13 MB | 768→384 px; Hình đại diện đối thoại trên boong cao khoảng 320 px |
| Kết xuất ba chiều của thân máy bay | 26 MB | Khoảng 14 MB | 576→384 px; Trang trước chiến tranh tối đa khoảng 300 px |
| Bối cảnh | 6 MB | Khoảng 3 MB | 1920×1440→1280×960 |
| Khác | 13 MB | 13 MB | Lô, mô hình, biểu tượng |

Giá cả: Phiên bản cầm tay yếu hơn đáng kể khi Deck được kết nối với TV hoặc màn hình (bản đồ chiến thuật đắt hơn khoảng 4,5 lần ở 1080p); thêm một gói nữa để xây dựng, kiểm tra và viết hướng dẫn.
Nếu thực sự muốn làm điều đó, bạn chỉ cần thêm thiết bị mục tiêu (kích thước tối đa và chất lượng JPEG) vào `compress_hd.py`. Bạn không cần phải thay đổi mặt tải, việc này mất khoảng nửa ngày.