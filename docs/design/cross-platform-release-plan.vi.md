> **Ngôn ngữ / Language:** [Tiếng Việt](cross-platform-release-plan.vi.md) · [English](cross-platform-release-plan.en.md) · [中文](cross-platform-release-plan.md)

# Chuyển đổi xuất bản đa nền tảng: lập kế hoạch và triển khai lần đầu

Đường cơ sở: `22706a4294f7e0ddee40563e7c6e4972376811f9` (19-09-2026).

> 24-09-2026: Thứ tự và ngưỡng của P2–P4 bên dưới đã được thay thế bằng [Kế hoạch chuyển ba nền tảng](three-platform-port.md); các mục tiêu, ranh giới và ràng buộc ủy quyền của trang này vẫn hợp lệ.

**Lô này là một cổng chạy độc lập và lớp ứng dụng di động, không phải là trò chơi ghép nối Windows/Linux. **
Máy chủ đồ họa vẫn sử dụng Metal; hội thoại đã được chuyển sang FreeType/HarfBuzz/ICU; trang trò chơi mặc định đã được thay đổi thành SDL/RmlUi, bộ chọn ROM trên máy tính để bàn vẫn sử dụng AppKit; `src/host/CMakeLists.txt`
Việc từ chối nền tảng không phải của Apple được giữ lại một cách có chủ ý. Thử nghiệm thành phần ba nền tảng trước đó bao gồm logic khởi chạy/lưu trữ ứng dụng (hiện chỉ chạy cục bộ),
Không phải trò chơi gốc, GPU, phương thức nhập liệu hoặc cấp độ đầy đủ.

## Mục tiêu và ranh giới

Quá trình chơi cuối cùng: Tải xuống chương trình cho nền tảng tương ứng → Chọn ROM phù hợp mà bạn có lần đầu tiên → Nhập cục bộ → Bắt đầu trò chơi.
Người chơi không cài đặt Python, Git, CMake, Ninja, trình biên dịch hoặc các công cụ biên dịch lại. Python vẫn đang được phát triển,
Phân tích ROM, tạo mã, dịch và biên dịch, xử lý nghệ thuật và QA; không viết lại toàn bộ bộ công cụ này.

Việc thực thi trò chơi gốc, sửa lỗi trò chơi, thư mục ngôn ngữ/khóa văn bản, trạng thái đọc và hành vi thoát chuỗi đã được xác minh đều được giữ nguyên.
Không thông báo hoàn thành trên nhiều nền tảng bằng cách xóa đoạn hội thoại gốc, trang tên, trang Link Battler hoặc cài đặt.
Các bản trình diễn, thăm dò, MCP và `build/recomp/profile-play``.command`/Python hiện có không được tự động di chuyển hoặc xóa.

## Đợt đầu tiên: mã đã triển khai

| Tài liệu | Trách nhiệm |
| --- | --- |
| `src/native/app/runtime.*` | Tham số, thư mục dữ liệu người dùng, khóa tệp Windows/POSIX, phiên độc lập, sao chép kho lưu trữ và kiểm tra tính toàn vẹn |
| `src/native/app/sha256.hpp` | Truyền phát bản tóm tắt ROM/nội dung/SRAM; thông báo không đồng nghĩa với việc nguồn được tin cậy hoặc được ủy quyền |
| `src/native/app/launch.*` | Đọc thư mục nội dung có thể di chuyển, khôi phục ngôn ngữ/quy tắc, xóa các biến môi trường phát triển và gọi trực tiếp máy chủ đã biên dịch |
| `src/host/host.cpp` | Đã thêm `--play`; đầu dò vị trí ban đầu ABI được giữ lại; không thay đổi vòng lặp trò chơi |
| `tools/release/export_content.py` | Xuất hồ sơ đã chuẩn bị hiện có dưới dạng thư mục nội dung đường dẫn tương đối để sử dụng cục bộ |
| Gốc `CMakeLists.txt` | Mục kiểm tra cơ bản không dựa vào trình kết xuất ROM, SDL, RT64 và Python; không phải là một mục xây dựng trò chơi |
| `tests/native_launch.cpp` | Thử nghiệm ứng dụng gốc không có ROM; xây dựng và thực thi cục bộ thông qua root CMake |

`srw64_app` chỉ dựa vào thư viện chuẩn C++20 và một lượng nhỏ API khóa tệp hệ điều hành.
`srw64_launch` sử dụng lại tệp tiêu đề đơn JSON trong RT64 đã sửa và không liên kết trình kết xuất RT64.
Lớp ứng dụng không chứa các tệp tiêu đề Metal/AppKit/CoreText và không thực thi các quy trình bên ngoài.
Thư mục quy tắc trò chơi được truyền vào từ máy chủ để tránh sao chép một tập hợp ID quy tắc/giá trị mặc định sẽ trôi dạt trong mục nhập mới.

### Lối vào mới dành cho nhà phát triển dùng thử (hiện tại vẫn chỉ dành cho máy chủ đồ họa macOS)

Thực thi trong thư mục gốc của kho chứa `rom.z64` và môi trường phát triển:

```sh
# 原有构建入口保留。构建过程中仍然会使用 Python。
make

# 一次性本地内容准备；两个输出目录均须不存在。
.venv/bin/python tools/content/compile_profile.py \
  --images original --output build/standalone-prepared
.venv/bin/python tools/release/export_content.py \
  --prepared build/standalone-prepared --output build/standalone-content

# 运行阶段直接调用 native binary，不经过 Python/build/probe launcher。
./build/recomp/gfx-build/srw64-gfx-host --play \
  --rom "$PWD/rom.z64" --content "$PWD/build/standalone-content" \
  --language zh-Hans
```

`--user-dir PATH` chỉ định một thư mục người dùng độc lập; `--new-game` bắt đầu từ hộp mực trống;
`--import-save PATH` Nhập kho lưu trữ trình mô phỏng dưới dạng băng cassette (xem "Nội dung và kho lưu trữ" bên dưới);
`--export-save PATH [--export-format ares|project64|mupen64plus|retroarch]` Chỉ xuất băng cassette và không bắt đầu trò chơi;
`--mute` tắt tiếng; `--rules original|fixed|all` chọn và ghi nhớ các quy tắc đặt trước;
`--resolution-scale 1..8` chỉ định độ phân giải này. Ngôn ngữ có thể được chuyển đổi trong trò chơi và khôi phục vào lần tiếp theo.

Đường dẫn đến ROM, nội dung và tệp nhị phân có thể nằm ngoài thư mục nguồn. Bản thân mục nhập mới không truy vấn mã nguồn, `.git`,
Tạo báo cáo mã hoặc chuỗi công cụ; tuy nhiên, điều này không có nghĩa là quá trình thu thập, ký và phân phối thư viện động của macOS `.app` đã hoàn tất.
Lô đầu tiên không có trình chọn tệp hoặc giao diện người dùng khởi chạy nhấp đúp. Khi thư mục nội dung không được chuẩn bị, lỗi sẽ được báo cáo rõ ràng và Python sẽ không được gọi một cách bí mật.

### Nội dung và Lưu trữ

Thư mục xuất chứa văn bản/hình đại diện tiếng Nhật có nguồn gốc từ ROM gốc và không được tải lên dưới dạng tạo phẩm phát hành công khai cho dự án này.
Việc xuất hiện tại chỉ bao gồm Chế độ gốc, đa ngôn ngữ gốc và tên/hình đại diện được liên kết; việc di chuyển các gói mô hình và hình ảnh HD sẽ được thực hiện trong các giai đoạn tiếp theo.
Chức năng HD của lối vào dùng thử ban đầu không bị ảnh hưởng bởi đợt này. Nhà xuất khẩu không sao chép ROM, phông chữ, mã nguồn, kho lưu trữ hoặc toàn bộ `assets/`.
Tệp kê khai liệt kê các tệp được phép đọc bằng SHA-256; thời gian chạy từ chối các đường dẫn ngoài giới hạn, liên kết tượng trưng bên ngoài và thông báo sự không nhất quán.

Đợt đầu tiên vẫn yêu cầu chuẩn bị nội dung bằng các công cụ phát triển. **"ROM gốc không yêu cầu Python khi nhập lần đầu" chưa được triển khai**,
Trình nhập gốc phải được hoàn thành trước khi phát hành ra công chúng và lô thư mục nội dung địa phương này không thể được sử dụng để thay thế có thể phân phối công khai.

Thư mục người dùng mặc định:

| Nền tảng | Đường dẫn |
| --- | --- |
| Windows | `%LOCALAPPDATA%/SRW64Recomp` |
| macOS | `~/Library/Application Support/SRW64Recomp` |
| Linux | `$XDG_DATA_HOME/srw64-recomp`; `~/.local/share/srw64-recomp` khi không có đường dẫn tuyệt đối hợp lệ nào được đặt |

Được lưu trữ trong `saves/` trong thư mục người dùng (từ 2026-10-01, xem [Nhiều cột lưu trữ và lưu trữ tự động](save-slots-autosave.md) để biết thiết kế):

| Tài liệu | Nội dung |
| --- | --- |
| `saves/cartridge.sram` | Hộp mực 32 KiB, từng byte giống hệt ares' `save.ram` |
| `saves/cartridge.sram.prev` | Cassette trước khi phát hành lần cuối |
| `saves/slots/NNN.rec` | Cột mở rộng 3–99: Trò chơi ghi 0x1F00 byte vào cột lưu |
| `saves/imports/` | Nhập băng cassette cũ được thay thế mỗi lần |

Mỗi lần chạy chiếm một phiên độc lập và máy chủ chỉ sửa đổi bản sao SRAM này.
(Để lại băng cassette cũ là `.prev`) và sao chép vào `sessions/<id>/save.bin`, viết tóm tắt và thay thế `last-session.txt` như bình thường.
Không có bản lưu trữ, trả lại lỗi hoặc chấm dứt bất thường sẽ không được công bố. Băng cassette phải có tổng kiểm tra tiêu đề tệp `SRW64V3`, trường đã sử dụng và vùng ngắt
Nó phải chính xác, nếu không nó sẽ từ chối khởi động và sẽ không lặng lẽ quay lại hoặc mở một tệp mới.

- `--import-save`: nhận dạng 32 KiB SRAM (Big Endian/Đảo ngược từ 32-bit/Đảo ngược 16-bit) và RetroArch `.srm` (phân đoạn SRAM ở 0x20800),
按文件头魔数判断，不认扩展名。 Trước tiên, băng cassette cũ được lưu vào `imports/` và các kho lưu trữ ở cột 1 và 2 cũ khác với thẻ mới sẽ được chuyển sang cột mở rộng.
两边的 「见过」位图合并。
- `--import-save` không có `--rom`: chỉ nhập và không bắt đầu trò chơi; thư mục người dùng bị khóa khi trò chơi đang chạy và sẽ bị từ chối.
- `--export-save`: Định dạng được tiện ích mở rộng chọn theo mặc định (`.ram`/`.sav` ares, `.sra` Project64, `.srm` RetroArch),
`--export-format` 可指定。 Nếu mục tiêu đã tồn tại, trước tiên hãy sao chép nó vào `*.before-srw64`; giữ các bản lưu trữ khác trong đó khi ghi vào RetroArch `.srm`.
- `--new-game`: Bắt đầu từ băng cassette trống; khi thoát ra, các kho lưu trữ còn nguyên vẹn ở khe băng cassette cũ 1 và 2 sẽ được chuyển sang khe mở rộng và không bị mất (băng cassette cũ sẽ khởi động như bình thường nếu bị hỏng).
- Phiên bản cũ chỉ có `sessions/`: Khi khởi động lần đầu tiên, `save.bin` được trỏ tới bởi `last-session.txt` và có thông báo phù hợp sẽ được chuyển vào băng cassette.

Ảnh chụp nhanh lịch sử vẫn ở `sessions/<id>/save.bin`, hãy trỏ tới nó bằng `--import-save` khi cần.
Khi nhập lịch sử dùng thử Python gốc, hãy chọn rõ ràng `runtime-data/saves/*.bin` cho phiên đó.

Không có lịch sử dọn dẹp tự động; nhật ký và dữ liệu thời gian chạy của máy chủ này cũng sẽ được giữ lại, có thể bao gồm ROM bộ đệm.
Các thư mục này là dữ liệu thời gian chạy riêng tư, không phải là gói báo cáo lỗi có thể chia sẻ. Thư mục ROM/cache được chia sẻ và tính năng giải mẫn cảm nhật ký sẽ được thêm vào trong tương lai
Thay thế nguyên tử hiện ngăn chặn việc đọc từ các con trỏ được viết nửa chừng và không yêu cầu độ bền của giao dịch khi tắt nguồn.

## 后续实施顺序及验收门槛

### P1: Nhập lần đầu so với phân phối macOS đầy đủ

Di chuyển `source_catalog`, **tập hợp con thời gian chạy** cần thiết để giải mã ROM/ánh xạ hình tượng ban đầu, tên và trích xuất hình đại diện được liên kết sang C++.
Việc triển khai Python vẫn ở dạng oracle, với ROM cố định và các thiết bị cố định tổng hợp thực hiện so sánh từng byte/bản ghi theo bản ghi.
Bộ đệm nhập được đánh dấu bằng `(ROM hash, importer version, locale/content schema)`; sau khi nhập thành công, nó sẽ được xuất bản nguyên tử.
Lỗi không phá hủy bộ đệm hiện có. Không biên dịch C/C++ khi khởi động lần đầu.

Đã thêm lựa chọn tệp, xóa lời nhắc lỗi, tài nguyên chỉ đọc/thư mục người dùng có thể ghi độc lập và bộ sưu tập thư viện động của các gói macOS.
Các tệp nhị phân, sơ đồ phông chữ UI gốc, gói ngôn ngữ và tài nguyên có thể phân phối cần phải được kiểm kê rõ ràng.

**Điều kiện hoàn thành:** Môi trường người dùng macOS sạch sẽ, không có Python/Git/Homebrew/Xcode, các chương trình và ROM nằm ngoài thư mục mã nguồn;
Nhập lần đầu, chuyển đổi giữa tiếng Nhật, tiếng Trung và tiếng Anh, lưu/thoát/khởi động lại bình thường, ROM xấu, thiếu tài nguyên, thư mục ứng dụng chỉ đọc đều vượt qua.

### P2: Tách rời phần phụ trợ đồ họa và văn bản

Phụ thuộc trực tiếp vào `graphics.cpp`, `native_dialogue_text.cpp`, `native_marker.cpp`
Các phần `MTL::*`, `plume::Metal*`, `SDL_MetalView` được chuyển ra khỏi mã chia sẻ.
Giữ RT64/Plume: macOS Metal, Linux Vulkan, Windows. Trước tiên, hãy chọn đường dẫn được hỗ trợ (Vulkan hoặc D3D12) và chạy qua nó.
Ảnh chụp màn hình/đọc lại, chặn trang được đặt tên và hoàn thành hiện tại cũng phải được trừu tượng hóa và không thể thay thế việc khởi tạo cửa sổ.

Mô hình đối thoại, trạng thái phân trang/nguyên văn/đọc và kết xuất ảnh chụp nhanh được giữ lại; định hình văn bản/raster và phân lớp tổng hợp GPU.
Đánh giá các sơ đồ phân loại phông chữ được chia sẻ và các phông chữ có thể phân phối lại mà không cần mã hóa tên phông chữ PostScript của macOS trên Windows/Linux.

**Không thể phá vỡ:** Giao diện người dùng phải phù hợp với khối lượng công việc đang được hiển thị và không thể đọc "RDRAM mới nhất" cũng như ghi đè các khung hình cũ;
Thay đổi kích thước, lệnh gọi lại hoàn thành GPU không đồng bộ, số liệu phông chữ, quy tắc cuối dòng và chuyển đổi ngôn ngữ không thể nâng cao tập lệnh gốc.

**Điều kiện đầy đủ:** Đối với mỗi nền tảng, ít nhất phải vượt qua phần mở→tên→tập đầu tiên→khởi động nguội kho lưu trữ, bao gồm chia tỷ lệ cửa sổ, F6/F7,
Đối thoại tắc/nhấp nháy và thoát ra an toàn; giữ cổng sân ga trước khi đi qua, không yêu cầu hỗ trợ đầy đủ.

### P3: Giao diện người dùng và đầu vào được chia sẻ

2026-09-20 Trang trò chơi mặc định đã được chuyển sang [SDL/RmlUi](../native/shared-game-ui.md): lựa chọn nhân vật chính, tên,
Xác nhận, cài đặt, Link Battler, thông báo và gỡ lỗi các sự kiện chia sẻ giao diện người dùng cũng như đường dẫn hiển thị và trang trò chơi AppKit gốc không còn được biên dịch.
[Thăm dò trang tên độc lập](../native/shared-name-page-probe.md) được dành riêng cho việc nhóm từ và hồi quy bố cục.
Việc đặt tên và viết lại trò chơi thực sự đã được xác minh; Cửa sổ đề xuất phương thức nhập hệ điều hành, bộ điều khiển, bề mặt đa nền tảng và tập đầu tiên/khởi động nguội vẫn được chấp nhận.
Mã nguồn AppKit cũ tạm thời được sử dụng làm tham chiếu hồi quy; đoạn hội thoại đã được chuyển sang [Thành phần văn bản đa nền tảng](../native/portable-text.md).

Kết nối bộ điều khiển và các nút có thể cấu hình; MCP/QA sử dụng các hành động ngữ nghĩa để tránh coi đường dẫn kiểm soát Cocoa là giao thức công khai.
Ổ cắm gỡ lỗi phải được loại trừ tại thời điểm xây dựng bản phát hành chứ không chỉ đóng khi chạy.

### P4: Xây dựng bản phát hành và tự động hóa

Lô mục tiêu đầu tiên được sửa ở Windows x64, Linux x64 và macOS arm64. Intel macOS, Windows ARM64,
Nhị phân phổ quát được chấp nhận độc lập với nhiều định dạng phân phối Linux hơn mà không cần sử dụng thẻ `*-latest` để ngầm mở rộng cam kết.

Tác vụ GitHub bị tắt và CI từ xa không được thêm vào. Việc kiểm tra thành phần mã nguồn và xác minh trò chơi chứa ROM được thực hiện cục bộ và được ghi lại riêng biệt.
Việc tạo mã được tách biệt khỏi quá trình biên dịch ba nền tảng và sản phẩm được tạo ghi lại bản tóm tắt ROM/toolchain/patch/schema.
Chỉ các tệp nhị phân, các phần phụ thuộc cần thiết và tài nguyên có thể phân phối mới được thu thập theo tệp kê khai khi xuất bản và toàn bộ `build/` hoặc thư mục người dùng không bao giờ được đóng gói.
Mã nguồn/mã được tạo/nhị phân, bản dịch, nghệ thuật và phông chữ được kiểm tra riêng biệt về ranh giới ủy quyền; kiểm tra này không được thay thế bằng "không có ROM".

Trước tiên hãy sử dụng Windows zip, Linux tar.gz để làm rõ đường cơ sở glibc, macOS `.app` zip;
Việc đóng thư viện động, chữ ký/công chứng Mac, chữ ký Windows và kiểm tra máy sạch sẽ được hoàn thành trước khi người chơi thông thường có thể tải xuống.
AppImage/Flatpak, trình cài đặt và cập nhật tự động không phải là nhiệm vụ tiên quyết đầu tiên.

## Mục xác minh và phạm vi bằng chứng

```sh
# 无 ROM、无 Python、无 renderer 依赖的原生基础测试。
cmake -S . -B build/native-app -DCMAKE_BUILD_TYPE=Release
cmake --build build/native-app --config Release
ctest --test-dir build/native-app -C Release --output-on-failure

# 加入完整 bootstrap 的合成内容 + fake-host 测试；只需要已固定的 JSON 头文件。
cmake -S . -B build/native-app \
  -DSRW64_APP_JSON_INCLUDE_DIR="$PWD/build/recomp/upstream/RT64/src/contrib"
cmake --build build/native-app --config Release
ctest --test-dir build/native-app -C Release --output-on-failure

python -m unittest discover -s tests -p test_release_content.py -v
```

Các bài kiểm tra cơ bản bao gồm các tham số/đường dẫn UTF-8, chiến lược thư mục cho từng nền tảng, khóa tệp, vectơ đã biết SHA-256 và đọc khối,
Cách ly lưu trữ, loại bỏ thiệt hại, phục hồi rõ ràng, thoát bất thường mà không gửi, đường dẫn ra khỏi giới hạn và làm sạch biến môi trường.
Thử nghiệm bootstrap đầy đủ bằng cách sử dụng ROM/avatar tổng hợp và máy chủ giả trong bộ nhớ, bao gồm di chuyển nội dung, cwd tùy ý,
Phục hồi ngôn ngữ/quy tắc và trả về lỗi; **không thay thế cho bản dựng máy chủ thực hoặc xác minh GPU/trò chơi**.

Trước khi hợp nhất đợt đầu tiên, một lối vào mới phải được xây dựng trong môi trường macOS + ROM phù hợp của nhà phát triển, chạy quy trình dùng thử thực tế ở trên và kiểm tra
Không còn đường quay lại lối vào cũ. Chỉ sau đó, chúng tôi mới bắt đầu chuyển sang trình nhập gốc và di chuyển đồ họa/giao diện người dùng nền tảng.