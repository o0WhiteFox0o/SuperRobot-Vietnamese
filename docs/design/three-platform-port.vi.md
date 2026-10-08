> **Ngôn ngữ / Language:** [Tiếng Việt](three-platform-port.vi.md) · [English](three-platform-port.en.md) · [中文](three-platform-port.md)

# Gói chuyển ba nền tảng: Windows/Linux/macOS

24-09-2026. Tiếp tục [Kế hoạch phát hành P0](cross-platform-release-plan.md) và [Nhập gốc P1](native-rom-importer.md).
Trang này thay thế thứ tự và ngưỡng của P2–P4 trong P0; Các mục tiêu, luồng người chơi, ranh giới ủy quyền và các ràng buộc "không xóa các tính năng để tuyên bố hoàn thành" của P0 vẫn hợp lệ.
Kết luận đến từ quá trình kiểm tra tĩnh đối với máy chủ C++, xây dựng chuỗi công cụ và RT64/plume/N64ModernRuntime ngược dòng vào ngày hôm đó, **không thực sự được xây dựng hoặc chạy trên Windows/Linux**.

## Nền tảng mục tiêu

| Nền tảng | Phần cuối đồ họa | Trình biên dịch | Gói đầu tiên | Máy Chấp Nhận |
| --- | --- | --- | --- | --- |
| macOS arm64 | Kim loại (thông qua chùm tia) | Tiếng táo | `.app` mã zip | Máy phát triển hiện tại |
| Linux x64 (có Steam Deck) | Vulkan (Cửa sổ SDL Vulkan) | kêu vang | tar.gz, đường cơ sở glibc 2.35 | Máy hoặc Deck Linux x64 |
| Windows x64 | Mặc định D3D12, dự phòng Vulkan | clang-cl + Ninja | zip | Máy Windows x64 |

- **Lựa chọn phụ trợ. ** Thực hiện theo `GraphicsAPI::Automatic` của RT64, không tự viết logic lựa chọn. Quy tắc của nó là: sử dụng D3D12 cho Windows, sử dụng Vulkan trong Wine hoặc khi gặp phải các trình điều khiển xấu đã biết; sử dụng Metal cho Apple; sử dụng Vulkan (`rt64_user_configuration.cpp:142`, `rt64_application.cpp:133-289`) cho các nền tảng khác.
- **Mã GPU tự vẽ. ** Tất cả đều sử dụng giao diện chung của Plume (`RenderDevice`/`RenderCommandList`). Trình đổ bóng được viết bằng HLSL, được biên dịch trước thành SPIR-V, DXIL (chỉ dành cho Windows) và MSL khi xây dựng và được nhúng vào chương trình, theo `cmake/PixelCompositor.cmake`. Mã nguồn MSL không còn được biên dịch khi chạy.
- **macOS cũng đã chuyển sang cách triển khai tương tự. ** Hai bộ mã lớp HD không được giữ lại.
- ** Trình biên dịch. ** clang-cl phù hợp với Windows CI của RT64 và Zelda64Recomp; C được tạo bằng cách biên dịch lại đã tương thích với MSVC, clang và gcc trong `recomp.h`.

## Tình hình hiện tại

**ĐÃ CÓ THỂ DI ĐỘNG:**

- **Ngược dòng:** RT64 có thể lập trình được với ba phần phụ trợ: D3D12, Vulkan và Metal. N64ModernRuntime có sẵn trên Windows/Linux.
- **Biên dịch lại đầu ra:** `funcs_*.c` được tạo độc lập với nền tảng, không chứa đường dẫn máy chủ và không có điều kiện hệ điều hành.
- **Đối thoại và giao diện:** Sử dụng `PixelCompositor` cho hội thoại và FreeType/HarfBuzz/ICU cho văn bản. Giao diện RmlUi đã có ba nhánh: SPIR-V/DXIL/MSL.
- **Đầu vào & Âm thanh:** Đầu vào bàn phím và gamepad SDL (`graphics.cpp:520-620`), âm thanh SDL.
- **Lớp ứng dụng:** `src/native/app` đã được tách thành các đường dẫn Windows và POSIX, bao gồm các khóa tệp, thay thế nguyên tử, thư mục người dùng và đường dẫn tệp thực thi.
- **Móc:** Các móc lưới gốc và các móc hiện tại của RT64 không phụ thuộc vào phụ trợ. Kho lưu trữ này chỉ sử dụng loại Plume cho các bản vá hook cho RT64.

**Chặn các mục, xếp hạng theo khối lượng công việc:**

1. **Năm lớp HD gọi trực tiếp đến Metal. ** Liên quan đến `native_marker/map/portrait/background/sprite.cpp`: khoảng 250 dòng MSL, khoảng 380 dòng Metal API. Họ trực tiếp lấy đối tượng cơ bản `plume::Metal*`, tự kết thúc bộ mã hóa RT64, mở thẻ kết xuất mới, sử dụng `setVertexBytes` để nhồi các hằng số (tối đa 4 KiB), sử dụng `replaceRegion` để tải họa tiết lên và hoàn tất bằng lệnh gọi lại hoàn thành của Metal. Khoảng 60% còn lại là logic như nhận dạng RDRAM và JSON, có thể được tái sử dụng trực tiếp.
2. **Ba khoảng trống trong chùm lông:**
- Không có kết cấu→bản sao đệm trên Vulkan và Metal và không thể đọc ảnh chụp màn hình.
- Hình ảnh chuỗi trao đổi Vulkan không có cờ `TRANSFER_SRC` và không thể sử dụng làm nguồn sao chép.
- Không có lệnh gọi lại hoàn thành GPU: `graphics.cpp:94,161` không có giao diện tương ứng với `addCompletedHandler` của `dialogue_plume.cpp:51,59`.
3. **Trình biên dịch và CMake:**
- Trực tiếp các nền tảng không phải của Apple `FATAL_ERROR` (`src/host/CMakeLists.txt:59`).
- Sử dụng vô điều kiện `-framework`, `-fblocks`, OBJCXX; `-include stdlib.h` sẽ không biên dịch được theo clang-cl.
- `flockfile` (`script_trace.hpp:49`) qua `state_probe.hpp` được bao gồm trong hầu hết các tệp nguồn máy chủ và sẽ chặn trực tiếp quá trình biên dịch Windows.
- `path::c_str()` là `wchar_t` trên Windows, được chuyển tới `stbi_*` hoặc `%s` ở khoảng 12 vị trí.
- Thiếu định nghĩa `/utf-8` và `M_PI`.
4. **Chuỗi công cụ Python:**
- Đường dẫn `venv/bin/python` và tên tệp thực thi không có `.exe` được mã hóa cứng.
- `bootstrap.py:55` và `run_host_probe.py:206` tiếng vang lực + Ninja.
- Tại khoảng 264 vị trí `read_text`/`write_text` không có mã hóa nào được chỉ định. Trong số đó, `build_import_spec.py` được gọi trong quá trình định cấu hình CMake sẽ ghi bản sao giao diện thành các ký tự bị cắt xén theo mã hóa cục bộ của Windows.
- `fcntl` được nhập ở cấp cao nhất của mô-đun.
5. **Giao diện gỡ lỗi:** sử dụng ổ cắm AF_UNIX (`debug_server.cpp:297`, `session.py:48`). Các cấp độ nhỏ được biên soạn bằng dấu ngoặc kép POSIX `std::system` (`mini_stage.hpp:274`). Stdio của MCP không có UTF-8 cố định.
6. **Giao diện cửa sổ và nền tảng:**
- Cửa sổ: `SDL_WINDOW_METAL` + Tay cầm cacao (`graphics.cpp:466-480`).
- Lựa chọn ROM và hộp báo lỗi sử dụng AppKit (`macos/desktop_macos.mm`). Thanh menu `app_menu.mm` có các phần triển khai trống và các đường dẫn thay thế RmlUi trên các nền tảng khác.
7. **Phụ thuộc và môi trường xây dựng:**
- Linux biên dịch sẵn `dxc-linux` yêu cầu glibc 2.34.
- ICU của Debian 11/Steam Runtime Sniper (67) và HarfBuzz (2.7.4) dưới yêu cầu ( ≥70, ≥2,8).
- SDL2 2.26.3 đi kèm với RT64 trên Windows xung đột với máy chủ `find_package(SDL2)`.

## Sân khấu

### X0 Portable Base (thực hiện trên Mac, hoạt động tương tự)

Không cần máy móc mới. Mục tiêu là có mã biên dịch trên cả ba nền tảng nhưng hoạt động giống hệt nhau trên Mac.

- **CMake:**
- Thay thế "Máy chủ kim loại" bằng `SRW64_ENABLE_RT64`.
- Các tệp nguồn dành riêng cho Apple và các tùy chọn liên kết được bao gồm trong `if(APPLE)`, `-fblocks` chỉ dành cho các tệp vẫn tham chiếu các tệp tiêu đề Metal.
- `-include` được viết là `-include` hoặc `/FI` tùy theo trình biên dịch; Windows thêm `/utf-8`, `NOMINMAX`, `_USE_MATH_DEFINES`.
- Thêm `-msse4.1` vào mã vectơ RSP trên x64.
- Đã thêm `CMakePresets.json`, chia thành ba bộ: `macos-arm64`, `linux-x64`, `windows-x64-clangcl`. Trình biên dịch không còn được mã hóa cứng trong các tập lệnh nữa.
- **Mã nguồn:**
- `flockfile` được thay thế bằng `std::mutex` hoặc `_lock_file` trên Windows.
- Đường dẫn được thay đổi thống nhất thành `path.u8string()`, sau đó được chuyển đến `stbi_*` thông qua một chức năng công cụ nhỏ.
- Quá trình biên dịch cấp độ nhỏ được thay đổi để bắt đầu trực tiếp tiến trình con với danh sách argv.
- **Giao diện gỡ lỗi:** Đã thay đổi thành TCP loopback gốc: cổng được phân bổ tạm thời, mã thông báo được ghi vào `debug.json` hiện có. `srw64ctl`, MCP và các bài kiểm tra được điều chỉnh cùng nhau. Việc chấp nhận máy thực tế của ba nền tảng phải được thúc đẩy bởi nó, vì vậy nó được xếp vào đợt đầu tiên. (Hoàn thành vào ngày 06-10-2026, xem `src/host/debug_transport.cpp` và [Giao diện gỡ lỗi · Phương thức kết nối](../guide/debug-interface.md#连接方式); Máy Windows thật chưa được xác minh.)
- **Python:**
- Bộ `execute_process` của Makefile và CMake `PYTHONUTF8=1` và các chức năng công cụ dần dần thêm `encoding="utf-8"`.
- `fcntl` được thay thế bằng lớp tương thích (Windows sử dụng `msvcrt.locking`).
- Đường dẫn venv và hậu tố `.exe` được xử lý bởi một hàm trợ giúp chung.
- `generate_cpu.py` Đã sửa lỗi `newline="\n"` khi ghi tệp để đảm bảo rằng bản tóm tắt của sản phẩm được tạo nhất quán trên các nền tảng.
- **Chấp nhận:**
- `make`, `make recomp-native-check` và các tập lệnh kiểm tra hiện có đều được chuyển trên Mac.
- Khả năng biên dịch ít nhất các bài kiểm tra `srw64-host` chỉ dành cho CPU và CMake gốc trong các bộ chứa Linux. Docker được cài đặt trên máy này nhưng hiện chưa được khởi động.

### Lớp đồ họa X1 được đổi thành Plume (đã hoàn thành và được chấp nhận trên Mac)

**Tiến độ 25-09-2026:**

- **Các lớp phụ trợ:** `src/host/native_gpu.{hpp,cpp}`; trình đổ bóng là HLSL theo `src/host/shaders/`, được biên dịch từ `cmake/NativeGpu.cmake` thành SPIR-V, MSL (thông qua các công cụ chuyển đổi của RT64, `flip_vert_y` offset `-fvk-invert-y`) và DXIL.
- **Dữ liệu cho mỗi lần rút thăm:** Được ghi vào bộ đệm vòng `StructuredBuffer<float4>` dùng chung và chỉ số dưới được chuyển đến trình đổ bóng thông qua hằng số đẩy. RT64 đợi GPU hoàn thành sau khi mỗi khối lượng công việc được gửi (`rt64_workload_queue.cpp:843-844`), do đó, việc sử dụng lại khe vòng là an toàn; điều này cũng tránh được giới hạn dưới của hằng số đẩy 128 byte của Vulkan.
- **Bản vá RT64:** `NativeMeshDraw` lấy định dạng màu, định dạng độ sâu và số lượng mẫu của mục tiêu cảnh (`native_model_hook_patches.py`).
- **Năm lớp đã được cấy ghép (25-09-2026):** Bản đồ, nền, điểm đánh dấu (điểm đánh dấu vàng, quầng sáng, mô hình tàu và cột mốc, đường đi, bảng tên), họa tiết cảnh (thẻ tiêu đề, hình ảnh văn bản cốt truyện, văn bản giao diện người dùng gốc) và toàn bộ hình đại diện. Việc triển khai Linux null đã bị loại bỏ và tất cả các lớp được biên dịch trên cả ba nền tảng.
- **So sánh từng lớp trước và sau trên máy Mac** (cùng một cảnh, trước khi chuyển Metal và sau khi chuyển Plume):
- Nền giữa các cảnh: Sự khác biệt tối đa giữa các cảnh HD trong cùng một kho lưu trữ là 1 cấp độ.
- Thẻ: `ra-cailum`, `worldmap-libra` Các cấp độ nhỏ được rút ra với số lần giống nhau và các ảnh chụp màn hình chỉ khác nhau ở giai đoạn hoạt ảnh (do thời gian tổ chức điều khiển).
- Sprite: `act` thẻ tiêu đề, `ending` trang kết thúc đều nhất quán theo từng khung hình hoặc chỉ khác nhau ở khung chuyển tiếp.
- Hình đại diện: `scene8` Nhấn Z để chuyển sang đoạn hội thoại. Hình đại diện HD của Byoti, Jia'er, Wan Zhang và Garrison đều giống nhau.
- Bản đồ chiến thuật chỉ được bật khi `SRW64_HD_MAPS` được đặt và không được so sánh riêng lẻ.
- **Đường dẫn Vulkan (MoltenVK):** `SRW64_GRAPHICS_API=vulkan` (chỉ dành cho thử nghiệm) Cho phép RT64 trên Mac sử dụng phần phụ trợ Vulkan; vì lý do này, trình đổ bóng SPIR-V được nhúng trong tất cả các nền tảng, `graphics.cpp`, `dialogue_plume.cpp` Chọn các đường dẫn dành riêng cho Kim loại theo chương trình phụ trợ thực tế thay vì theo nền tảng. Bốn cảnh giống nhau cộng với các cảnh liên cảnh: Ảnh chụp màn hình Vulkan và Metal đều nhất quán, bao gồm các hộp thoại và trang RmlUi.
- **đọc lại ảnh chụp màn hình Vulkan/D3D12:** Phần phụ trợ Vulkan của Plume thêm kết cấu → bản sao bộ đệm, hình ảnh chuỗi trao đổi thêm `TRANSFER_SRC`, RT64 cung cấp kết cấu chuỗi trao đổi hiện tại (`GetRenderHookSwapChainTexture`) cho móc vẽ. Ảnh chụp màn hình của giao diện gỡ lỗi hiện có sẵn trên Vulkan.
- **Các sự cố RT64 được phát hiện và khắc phục trên Linux:**
- Bản vẽ gốc được đánh dấu bằng hình chữ nhật có họa tiết không có hình tam giác, các bản vá lỗi cũ có nội dung `faceIndices` nằm ngoài giới hạn. Nó không xảy ra lỗi trên Mac mà xảy ra lỗi phân tách trên Linux; bây giờ phải mất 0 khi vượt quá giới hạn.
- Khi không có bus phiên D-Bus, thư viện hộp thoại tệp của RT64 không khởi tạo được nhưng vẫn gọi `NFD_Quit` khi thoát và hủy bỏ; bây giờ nó chỉ được gọi khi khởi tạo thành công.
- **Ngăn xếp cuộc gọi gặp sự cố:** Máy chủ Linux in ngăn xếp cuộc gọi thành stderr (`host.cpp`) khi nhận được tín hiệu như SIGSEGV, được phân tích cú pháp bằng bản dựng không có sọc và `addr2line`.
- **Phương pháp so sánh trước và sau:** `srw64ctl launch --binary PATH` (tức là `run_host_probe.py --binary`) chạy chương trình đã chỉ định. Chương trình tiền di chuyển được xây dựng từ một cây công việc: mã nguồn hiện tại cộng với phiên bản HEAD của lớp sẽ được chuyển.

Đây là phần lớn nhất và toàn bộ quá trình có thể được xác minh trên Mac: phần phụ trợ Metal của Plume hiện là lớp dưới cùng.

- **Lớp phụ trợ dùng chung** (tên dự kiến `native_gpu`):
- Phím bộ đệm đường ống: định dạng màu, định dạng độ sâu, số lượng mẫu, chế độ độ sâu, chế độ hòa trộn. chùm khói tạo độ sâu và trạng thái trộn vào đường ống, vì vậy cả hai đều được khóa.
- Bộ đệm không đổi xoay trên mỗi khung hình, thay vì `set*Bytes`. 192 B đồng phục vượt quá giới hạn dưới 128 B được đảm bảo của Vulkan; 2–4 KiB của bảng màu và dữ liệu quad sẽ được lưu vào bộ đệm.
- Bộ đệm tải lên họa tiết + `copyTextureRegion` + rào cản; mipmap được tạo trên CPU.
- Trì hoãn giải phóng tài nguyên bằng hàng rào, thay thế cho giả định "giải phóng sau 20 giây không hoạt động" hiện tại.
- **Trình tự cấy ghép** (từ đơn giản đến phức tạp, mỗi bước được chấp nhận riêng): bản đồ → nền → dọc → sprite → điểm đánh dấu. Điểm đánh dấu có năm đường ống, bốn trạng thái độ sâu và bộ đệm theo dõi 4 MiB.
- **Vị trí vẽ:** Vẽ trực tiếp trong bộ đệm khung giới hạn RT64 mà không kết thúc bộ mã hóa và mở đường kết xuất mới. Sau khi hook quay trở lại, RT64 sẽ liên kết lại bố cục đường ống, bộ mô tả và khung nhìn (`rt64_framebuffer_renderer.cpp:477-488`), nhưng không đặt lại bộ đệm khung, do đó hook không thể thay thế nó.
- **`graphics.cpp`:**
- Tên trang bị tắc đã thay đổi thành `setFramebuffer` + `clearColor`.
- Truy vấn đọc lại ảnh chụp màn hình và định dạng bộ đệm khung được thay đổi thành chùm.
- Đã thay đổi `GraphicsAPI::Metal` thành `Automatic` ở hai vị trí.
- **Đối thoại:** `dialogue_plume.cpp` được chuyển ra khỏi `macos/`, mục nhập `metal_*` được đổi tên và định dạng đổ bóng được lấy từ `getCapabilities().shaderFormat`.
- **RT64/bản vá lỗi** (làm theo thay thế chuỗi danh sách trắng của `prepare_rt64.py`, không phân nhánh):
- Kết cấu bản vá Vulkan và Metal→bản sao bộ đệm.
- Hình ảnh chuỗi trao đổi Vulkan cộng với `TRANSFER_SRC`.
- `rt64_present_queue.cpp` gọi hook "hoàn thành kết xuất" sau `presentGraphicsWorker->wait()` với id khối lượng công việc để thay thế lệnh gọi lại hoàn thành Metal. Nó vẫn phải đáp ứng các ràng buộc của P0: giao diện chỉ tương ứng với khối lượng công việc được trình bày và không thể đọc "RDRAM mới nhất" và ghi đè lên các khung hình cũ.
- **Chấp nhận:**
- Sử dụng phương pháp chụp màn hình điểm cố định trong [Mô hình tàu](../native/native-ship-model.md) (cấp độ nhỏ với thời gian xác định, cứ 50 VI thì chụp một ảnh chụp màn hình), so sánh hình ảnh HD trước và sau khi ghép và kiểm tra từng lớp.
- Trang tên bị chặn không nhấp nháy; ảnh chụp màn hình và ảnh chụp màn hình giao diện gỡ lỗi là bình thường; F6/F7 và zoom bình thường.
- Tùy chọn: Máy này có cài đặt MoltenVK 1.4.1 của Homebrew. Nếu chương trình phụ trợ RT64 Vulkan có thể chạy trên máy Mac thì đường dẫn SPIR-V có thể được kiểm tra trước khi có máy Linux. ** Điều này chưa được xác minh. **

### X2 Linux x64 với Steam Deck

25-09-2026 Điều chỉnh thứ tự: Người dùng cần chơi trên Steam Deck trước nên X2 bắt đầu trước X1, theo hai bước:

- **Phiên bản màn hình gốc D1** (code đã được viết sẵn, vui lòng xem [Linux Build](../guide/linux-build.md) để biết cách xây dựng và hướng dẫn):
- Năm lớp HD trước tiên được thay thế bằng các triển khai trống trên nền tảng không phải của Apple và bàn giao cho RT64 vẽ theo danh sách hiển thị ban đầu (xóa sau khi X1 hoàn thành).
- Cửa sổ, lựa chọn phụ trợ, thông báo hoàn thành GPU (bản vá RT64 `RenderHookPresented`), chặn trang tên, tổng hợp hội thoại đều độc lập với phụ trợ.
- Gỡ lỗi ảnh chụp màn hình trả về lỗi trên Vulkan tại thời điểm đó (X1 đã được đệm tính năng đọc lại).
- Đã thêm bộ điều khiển → cầu nối phím vào giao diện dùng chung: Các trang gốc không phải trang chiến đấu ban đầu chỉ nhận dạng bàn phím. Bây giờ, nhấn bộ điều khiển sẽ chuyển đổi nó thành cùng một bộ phím (`frontend.cpp` và `pad_keys`). Deck cũng có thể vận hành trường, tiêu đề, kho lưu trữ và trang tên chỉ bằng bộ điều khiển.
- **Phiên bản D2 HD** (mã hoàn thành vào ngày 25-09-2026): Tất cả năm lớp HD đã được thay đổi thành chùm, phần triển khai trống đã bị xóa, Linux và Mac chia sẻ cùng một bộ triển khai; đường dẫn Vulkan đã được so sánh với MoltenVK và Metal trên Mac (xem X1). Sử dụng gói chất liệu HD trên Deck là phiên bản HD hoàn chỉnh, điều này vẫn đang được máy Deck thực tế xác nhận.

Đây là danh sách đầy đủ của X2:

- **Cửa sổ:** `SDL_WINDOW_VULKAN`, chuyển giao `SDL_Window*` cho RT64/ultramodern; `RT64_SDL_WINDOW_VULKAN` đã mở.
- **Phụ thuộc:**
- Tổng quát hóa `config/recomp/macos-dependencies.json` thành các khóa phụ thuộc được nhóm theo nền tảng, sử dụng cùng một lô gói nguồn SDL, FreeType, HarfBuzz, ICU và SHA-256.
- Link tĩnh trên Linux, hoặc tải cạnh chương trình bằng `$ORIGIN` rpath. Không dựa vào hệ thống hoặc ICU riêng của Steam Runtime.
- **Môi trường xây dựng:** Sử dụng bộ chứa Ubuntu 22.04 x64 (glibc 2.35), đáp ứng yêu cầu `dxc-linux` được biên dịch trước. CMake và Python 3.11 được sửa riêng lẻ.
- glibc của SteamOS mới hơn 2.35 và gói được tạo có thể chạy trực tiếp ở chế độ "trò chơi không phải Steam".
- Steam Runtime Sniper (glibc 2.31) dành cho phần sau: yêu cầu mã hóa DXC từ nguồn hoặc cung cấp các shader biên dịch sẵn từ nơi khác.
- **Sàn hơi:**
- Toàn màn hình 1280×800.
- Tất cả các trang RmlUi chỉ có thể được vận hành bằng bộ điều khiển; xem [Phím và biểu tượng nút Steam Deck](steam-deck-controls.md) để biết các vị trí chính, mục cài đặt và biểu tượng nút.
- Không có hộp thoại desktop trong chế độ game nên phần lựa chọn ROM và nhắc nhở lỗi được chuyển sang trang RmlUi, phù hợp với chính sách “chỉ sử dụng RmlUi cho giao diện”. Thay vào đó, macOS cũng nên sử dụng trang này và sau đó xóa `desktop_macos.mm`.
- Sử dụng phông chữ đi kèm với HarmonyOS; thêm đường dẫn `noto-cjk/` của Arch với danh sách phông chữ dự phòng `frontend.cpp:1449`.
- **Chấp nhận:** Chạy mỗi chế độ trò chơi trên máy tính để bàn và Bộ bài Linux một lần và chỉ sử dụng bộ điều khiển trên Bộ bài:
- Mở → Tên → Chương 1 → Khởi động nguội sau khi lưu;
- Zoom cửa sổ, F6/F7, chặn hội thoại và nhấp nháy, thoát hiểm an toàn;
- Giữ cổng sân ga trước khi đi qua, không tuyên bố hỗ trợ.

### X3 Windows x64 (được tinh chỉnh vào ngày 25-09-2026)

Windows và Linux chia sẻ những phần mà X2 đã thực hiện mà không liên quan gì đến phần phụ trợ: tay cầm cửa sổ, tự động chọn phần phụ trợ cho RT64, thông báo hoàn thành GPU và tổng hợp hội thoại. Nhánh cửa sổ của `_WIN32` trong `graphics.cpp` đã được viết nhưng chưa được biên dịch trên Windows. Phần còn lại chủ yếu là trình biên dịch, dịch vụ hệ thống và đóng gói.

**Môi trường xây dựng**

- Windows 10 22H2 hoặc 11, x64.
- Công cụ: Công cụ xây dựng VS 2022 cộng với “Công cụ C++ Clang dành cho Windows” (clang-cl), CMake ≥ 3.20, Ninja, Python 3.11 từ python.org. Git đặt `core.autocrlf=false` và `core.longpaths=true` để đảm bảo tính nhất quán từng byte trong kiểm tra thông báo ngược dòng.
- Chạy `tools/release/build_windows.py` trong dòng lệnh "x64 Native Tools" (để viết cấu trúc như sau: `build_linux.py`: Dependency → Host → Packaging → Link Check).
- Đầu vào độc lập với nền tảng được sao chép từ Mac, giống như Linux: `build/recomp/cpu-bound/`, `build/recomp/audio-probe/audio.cpp`, `build/fonts/`, đã vá `build/recomp/upstream/`.
- **Không biên dịch chéo trên Mac. ** Bản dựng RT64 chạy `dxc.exe` để tạo DXIL. Máy ảo ARM Windows 11 của Parallels có thể dựa vào mô phỏng x64 để kiểm tra biên dịch, nhưng không có D3D12 thì không thể chấp nhận máy thực tế.

**Thay đổi mã** (sắp xếp theo mức độ chặn)

1. **CMake:**
- Xả lũ WIN32.
- Trong clang-cl: `-include stdlib.h` được đổi thành `/FIstdlib.h`, `-march=x86-64-v2` được đổi thành `/clang:-march=x86-64-v2`.
- Đã thêm `/utf-8`, `NOMINMAX`, `_USE_MATH_DEFINES`.
- liên kết phát hành sử dụng `/SUBSYSTEM:WINDOWS` và `/OPT:NOICF`, giống như Zelda64Recomp.
2. **`flockfile`/`funlockfile`** (`script_trace.hpp:49,53`, `script_move_probe.hpp:34`) được thay thế bằng các gói di động, tương ứng với `_lock_file` trên Windows. Nó xâm nhập hầu hết tất cả các tệp nguồn máy chủ thông qua `state_probe.hpp` và là lỗi biên dịch đầu tiên.
3. **Đường dẫn ký tự rộng:** `path::c_str()` là `wchar_t` trên Windows. Các ảnh chụp màn hình liên quan đến `graphics.cpp` được viết bằng PNG, năm `native_*.cpp` và `frontend.cpp:270` của `stbi_load`, `debug_server.cpp` và tất cả đều được thay đổi thành một `u8string()` chức năng phụ trợ.
4. **SDL:**
- RT64 liên kết tới SDL2 2.26.3 tích hợp (RT64 `CMakeLists.txt:294-298`) trên WIN32. Máy chủ sử dụng `find_package(SDL2)` và cả hai sẽ xung đột.
- Sử dụng bản vá `prepare_rt64.py` để khiến RT64 cũng sử dụng `find_package` trên WIN32. Ba nền tảng sử dụng SDL3 + sdl2-compat bị khóa.
5. **Phụ thuộc:**
- SDL3, sdl2-compat, FreeType và HarfBuzz sử dụng cùng một loạt gói mã nguồn và được xây dựng bằng CMake.
- ICU sử dụng dự án MSBuild (`source/allinone/allinone.sln`) đi kèm với gói mã nguồn.
- Không giới thiệu vcpkg để tránh nguồn phiên bản thứ 2.
6. **Khởi động:**
- Khi bắt đầu không có tham số, trước tiên hãy tìm `rom.z64` trong thư mục người dùng (`%LOCALAPPDATA%\SRW64Recomp`) và chương trình; nếu không tìm thấy, hãy sử dụng `SDL_ShowSimpleMessageBox` để giải thích.
- Sẽ được thay thế bằng trang tuyển chọn RmlUi trong tương lai, chia sẻ với chế độ chơi Deck.
- Linux hiện thực hiện điều tương tự với `marchwind64.sh`, điều này cũng sẽ lấy lại C++.
7. **Đường dẫn Unicode:** Thêm bảng kê khai ứng dụng `activeCodePage=UTF-8` (được hỗ trợ từ Windows 10 1903). `launch.cpp` Đường dẫn đi qua các biến môi trường và argv sẽ không bị biến dạng khi gặp tên người dùng không phải ASCII (chẳng hạn như `C:\Users\太郎`).
8. **Giao diện gỡ lỗi:** ~~AF_UNIX (`debug_server.cpp`, `tools/recomp/debug/session.py:48`) đã được đổi thành loopback TCP + token~~, hoàn thành vào ngày 06/10/2026 (`debug_transport.cpp`), đồng thời đầu vào và đầu ra tiêu chuẩn của MCP cũng được cố định thành UTF-8. Đây là mặt hàng X0. Lý do là CPython không có `socket.AF_UNIX` trên Windows và việc máy Windows chấp nhận thực tế phụ thuộc vào trình điều khiển giao diện gỡ lỗi.
9. **Cấp độ nhỏ:** `std::system` của `mini_stage.hpp:274` sử dụng dấu ngoặc kép POSIX và thay vào đó bắt đầu trực tiếp quy trình con. Đây là một tính năng phát triển và có thể được tắt trên Windows trước.
10. **Ảnh chụp màn hình:** Phần phụ trợ D3D12 của Plume đã hỗ trợ kết cấu → bản sao bộ đệm (`plume_d3d12.cpp:2302`), vì vậy D3D12 của Windows có thể tiếp tục gỡ lỗi ảnh chụp màn hình trước Vulkan. Cũng cần kiểm tra xem chuỗi trao đổi có sử dụng COPY_SOURCE hay không.

**Đóng gói:** `package_windows.py` zip, nội dung như sau:

- Chương trình: exe, và `SDL3.dll`, `SDL2.dll`, `freetype.dll`, `harfbuzz.dll`, DLL của ICU, `dxcompiler.dll`, `dxil.dll`;
- Tài nguyên: `fonts/`, `dialogue/`, `licenses/`.

Kiểm tra bảng nhập bằng `llvm-readobj --coff-imports`, chỉ cho phép các DLL hệ thống (kernel32, user32, d3d12, dxgi, v.v.). Vulkan được tải động bởi volk và sẽ không xuất hiện trong bảng nhập.

**Chấp nhận:**

- Quy trình tương tự như X2;
- Chạy từng D3D12 và Vulkan (thêm công tắc `SRW64_GRAPHICS_API=d3d12|vulkan` chỉ để kiểm tra);
- Thư mục người dùng không phải ASCII;
- Thu phóng màn hình 150%.

**Đặt hàng:**

- Biên dịch W1 đạt: mục 1–5;
- W2 có thể vào game: vật phẩm 6 và 7;
- Giao diện gỡ lỗi W3 và ảnh chụp màn hình: mục 8 và 10;
- Đóng gói W4, nghiệm thu máy sạch.

### Gói phân phối X4 và ma trận xác minh cục bộ

- Thêm `package_windows.py` (thu thập DLL với `file(GET_RUNTIME_DEPENDENCIES)`) và `package_linux.py` (kiểm tra danh sách CẦN với đường cơ sở glibc) bên cạnh `package_macos.py`. Chỉ thu thập tệp theo danh sách, không bao giờ đóng gói toàn bộ `build/`.
- Hành động GitHub vẫn đóng. Gửi `bb3319d` Quy trình kiểm tra thành phần ba nền tảng đã xóa có thể được viết lại thành tập lệnh cục bộ dưới dạng kiểm tra thành phần cho từng máy.
- Mỗi nền tảng ghi hai bộ kết quả: kiểm tra thành phần và ROM giữ tiến trình máy thực tế, được ghi riêng.
- AppImage/Flatpak, trình cài đặt, chữ ký và công chứng được đặt sau đợt đầu tiên.

## Các bước xây dựng được thực hiện trên máy nào?

| Bước | Vị trí |
| --- | --- |
| Bố trí ROM, chức năng quét, tạo mã CPU (Python + N64Recomp) | Làm điều đó một lần trên bất kỳ máy nào, thường là Mac. Toàn bộ `build/recomp/cpu-bound/` cùng với `report.json` được sao chép nguyên vẹn sang byte máy khác (`run_host_probe.py:194` sẽ xác minh thông báo). Đây là một bản ROM phái sinh và không thể công khai |
| Đầu ra âm thanh RSPRecomp | Tương tự như trên; `run_host_probe.py:204` cần thêm nút chuyển "bỏ qua tái tạo" |
| Kéo mã nguồn ngược dòng, `prepare_rt64`/`prepare_frontend`/`build_import_spec` | Mỗi máy mục tiêu; `bootstrap.py` yêu cầu chế độ chỉ mã nguồn |
| Biên dịch Shader, biên dịch C/C++, phần phụ thuộc, đóng gói | Mỗi nền tảng mục tiêu; DXIL chỉ có thể được tạo trên Windows |

Không cần phải biên dịch N64Recomp, RSPRecomp, n64sym hay `build/recomp/venv` trên máy đích.

## TBD

- **Máy chấp nhận:** Bạn có máy Linux x64 (hoặc sử dụng distrobox trực tiếp trên Deck) và máy Windows x64 không. X0 và ​​X1 chỉ yêu cầu Mac; X2 và X3 không thể được chấp nhận nếu không có máy tương ứng.
- **Phụ trợ Windows:** Gói này mặc định là "D3D12 + Vulkan dự phòng". Chỉ sử dụng Vulkan sẽ loại bỏ nhu cầu xây dựng DXIL nhưng sẽ đi chệch khỏi lựa chọn mặc định là RT64 trên Windows.
- **Đường cơ sở của Linux:** Lô glibc 2.35 tar.gz đầu tiên; có vào vùng chứa Steam Runtime hay không.
- **Trang lựa chọn ROM:** Liệu macOS có nên được thay thế bằng trang RmlUi hay không.

## Không có trong kế hoạch này

Phương thức phân phối gói vật liệu HD (P1 vẫn chỉ bao gồm Chế độ gốc), ranh giới ủy quyền phân phối (xem P0), cửa sổ ứng cử viên IME (P3 đã được ghi lại). Những điều này không liên quan gì đến nền tảng và sẽ được lên kế hoạch riêng.