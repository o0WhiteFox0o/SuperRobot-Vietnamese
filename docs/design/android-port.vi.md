> **Ngôn ngữ / Language:** [Tiếng Việt](android-port.vi.md) · [English](android-port.en.md) · [中文](android-port.md)

# Kế hoạch chuyển Android (nghiên cứu)

2026-10-01. Tiếp tục [Kế hoạch chuyển ba nền tảng](three-platform-port.md). Trang này là kết luận nghiên cứu và kế hoạch đề xuất, dựa trên ba phần:

- Kiểm tra tĩnh mã máy chủ của kho này, số dòng dựa trên `c480cfe` chính;
- Đã kiểm tra mã nguồn do `config/recomp/toolchain.json` gửi đã sửa lỗi RT64 (bao gồm cả mô-đun con Plume), N64ModernRuntime và Zelda64Recomp, đồng thời biên dịch tất cả các trình đổ bóng SPIR-V của RT64 với phiên bản DXC cố định;
- Cổng Android N64Recomp đã có sẵn trong cộng đồng: Tôi đã đọc mã nguồn và tài liệu nhưng không biên dịch hoặc chạy nó.

**Dự án này chưa được xây dựng bằng NDK và cũng chưa được chạy trên thiết bị Android. ** Những từ được đánh dấu là "suy luận" trong bài viết là những nhận định kỹ thuật chứ không phải số đo thực tế.

## Kết luận

- **Có thể thực hiện được, hầu hết các vấn đề đều đã được người khác giải quyết. ** Có ít nhất năm cổng Android của trò chơi N64Recomp trong cộng đồng, tất cả đều là "mã do người xây dựng tạo → tải qua APK → người chơi chọn ROM của riêng họ" và tất cả đều sử dụng RT64 Vulkan đã vá để kết xuất. RT64 ngược dòng, N64Recomp và Zelda64Recomp không có hỗ trợ Android chính thức và các bản vá cộng đồng chưa được tích hợp trở lại ngược dòng.
- **Tuyến đường:** SDL + RT64 Vulkan, chỉ arm64-v8a. Các lớp HD, tổng hợp hội thoại và RmlUi đã được dựa trên Plume và được nhúng với SPIR-V (gói ba nền tảng X1), vì vậy Android và Linux chia sẻ cùng một bộ mã đồ họa mà không cần viết phần phụ trợ riêng.
- **Đầu tiên làm thiết bị cầm tay Android, sau đó làm màn hình cảm ứng cho điện thoại di động. **Bảng điều khiển cầm tay có bộ điều khiển, màn hình 16:9 và chủ yếu là GPU Qualcomm Adreno. Các phím điều khiển Deck, lời nhắc chính và hình ảnh 16:9 hiện có có thể được sử dụng trực tiếp, trong khi màn hình cảm ứng và giao diện điện thoại di động đang ở một giai đoạn khác. Điều này phù hợp với thứ tự "bộ bài đầu tiên".
- **Phân phối:** APK chứa mã được biên dịch do ROM tạo ra, giống như gói Deck. Do đó, chúng tôi chỉ tạo các gói sideload để sử dụng cho riêng mình và không có sẵn trên Google Play.
- **Khối lượng công việc chính (suy ra):**
1. Các bản vá Android cho RT64/plume/N64ModernRuntime, khoảng mười mục và nhánh cộng đồng có triển khai tham chiếu;
2. Vòng đời ứng dụng của máy chủ chủ yếu có nghĩa là các tập tin không thể bị mất khi quá trình này bị tắt ở chế độ nền;
3. Biên dịch chéo và xây dựng;
4. Màn hình cảm ứng và giao diện điện thoại di động.

## Mục tiêu và phạm vi

| Mục | Lựa chọn | Lý do |
| --- | --- | --- |
| ABI | Chỉ arm64-v8a | Mã được tạo có dạng ABI giống như macOS arm64: little endian, LP64, RSP vector unit via sse2neon (`src/host/CMakeLists.txt:7`) |
| Đồ họa | Vulkan qua chùm | RT64 không có phụ trợ GLES. ghép hệ thống libultraship (Ship of Harkinian, v.v.) bằng GLES, không liên quan gì đến dự án này |
| Cửa sổ, đầu vào, âm thanh | SDL, thông qua SDLActivity | Máy chủ sử dụng SDL xuyên suốt. Thay vào đó hãy sử dụng AGDK GameActivity. Để viết lại lớp này, không sử dụng |
| minSdk | Dự kiến ​​28 (Android 9) | Tương tự như Goemon64Recomp-Android. ICU được bao gồm trong gói và không tuân theo yêu cầu API 31 của hệ thống NDK về ICU, xem bên dưới. Ngưỡng thực tế được xác định bởi đặc điểm GPU |
| Lô thiết bị nghiệm thu đầu tiên | Máy chơi game cầm tay Android của Qualcomm Adreno (như AYN Odin, dòng Retroid Pocket) | Bộ điều khiển, 16:9, Trải nghiệm cộng đồng dựa trên Adreno nhiều nhất |
| Phân phối | APK tự tải | Xem [Phân phối](#分发与-rom-派生代码) |

## Đã có tiền lệ

Các dự án sau đây là những cấy ghép không chính thức từ cộng đồng, được xác minh vào ngày 2026-10-01:

| Dự án | Những điểm chính |
| --- | --- |
| [Goemon64Recomp-Android](https://github.com/ogdanimal/Goemon64Recomp-Android) | ** Giá trị tham chiếu là lớn nhất. ** v1.0.7, cam kết cuối cùng 2026-09-01, minSdk 28, NDK 27.1, được căn chỉnh theo các trang 16 KB. Các thư viện RT64, Plume và thời gian chạy đã được phân nhánh. Hầu hết các mục chặn bên dưới có thể được tìm thấy trong các nhánh này và có thể tìm thấy các bản sửa lỗi tương ứng của chúng. ROM được chọn bằng Khung truy cập lưu trữ (SAF) và được sao chép vào thư mục riêng của ứng dụng. Bạn có thể tùy ý sử dụng libadrenotools để tải trình điều khiển củ cải |
| [Zelda64Recomp-Android](https://github.com/linkzenic/Zelda64Recomp-Android) | minSdk 24, NDK 26. Việc sử dụng `MANAGE_EXTERNAL_STORAGE` để đọc và ghi các thư mục công cộng không tuân thủ chính sách bộ nhớ của Play. Chủ yếu được thử nghiệm trên Adreno; Các thiết bị Samsung được đề cập trong phần mô tả sẽ không hoạt động |
| [HarvestMoon64Recomp](https://github.com/igawa6/HarvestMoon64Recomp) | Android 9+, Vulkan 1.1, ROM copy vào thư mục riêng, không cần cấp phép |
| [dk64-recomp-android](https://github.com/deivid22srk/dk64-recomp-android) | Báo cáo lỗi phân đoạn Adreno 619 trong `vkGetRefreshCycleDurationGOOGLE`. RT64 ngược dòng gọi điều này trên mỗi kết xuất |
| [BanjoRecomp-Android](https://github.com/AurelioB/BanjoRecomp-Android) | Đã thử nghiệm trên bảng điều khiển cầm tay AYN Thor |

Thực tiễn phổ biến:

- Mã CPU được tạo từ ROM trên máy build và APK chứa mã được biên dịch không có dữ liệu ROM;
- Tất cả đều sử dụng keo Android đi kèm với SDL2 2.32 và không có loại nào sử dụng SDL3 hoặc sdl2-compat.

**Đo hiệu năng thực tế của Goemon trên Snapdragon 865 (Adreno 650)** (xem bản ghi hiệu năng Android của kho lưu trữ này):

- Khi độ phân giải là 4x và tắt MSAA, trò chơi sẽ chạy ở tốc độ gốc 30 FPS; độ phân giải 8x chỉ là 30 FPS và độ phân giải 4x là 52 FPS; MSAA mất khoảng 20%.
- Menu tệ nhất khoảng 14 FPS. Lý do là với 20 hàng rào trên mỗi khung hình, tần số GPU được lên kế hoạch là 305–400 MHz.
- Kết luận: Phiên bản Android mặc định độ phân giải 4x và tắt MSAA.

Chính thức: [#45 "Hỗ trợ Android?"](https://github.com/Mr-Wiseguy/Zelda64Recomp/issues/45) của Zelda64Recomp đã bị đóng do "không có kế hoạch". Không tìm thấy nhận xét nào từ các nhà bảo trì RT64 hoặc N64Recomp về Android.

## Trạng thái ngược dòng (cam kết cố định)

### RT64 có chùm lông

Plume duy trì bộ xương Android:

- `VK_USE_PLATFORM_ANDROID_KHR`;
- `RenderWindow` được định nghĩa là `ANativeWindow*`;
- Tạo bề mặt với `vkCreateAndroidSurfaceKHR`.

Bộ mã này xuất phát từ các cam kết ban đầu của RT64 (2024-04) và Plume (2025-02) và kể từ đó, không có cam kết nào đề cập đến Android. **Tôi không thể biên dịch nó như hiện tại và nó không vẽ chính xác:**

| Vấn đề | Vị trí (thượng nguồn) | Hậu quả |
| --- | --- | --- |
| `static_assert(false && "Android unimplemented")` | `rt64_application_window.cpp:107,151` | Biên dịch không thành công |
| Nativefiledialog được liên kết vô điều kiện; CMake của nó coi Android như Linux | RT64 `CMakeLists.txt:74,444` | Cần có GTK3 trong quá trình cấu hình, CMake bị lỗi |
| DXC và `file_to_c` được chọn bởi nền tảng đích | RT64 `CMakeLists.txt:61-65,72` | Chạy các chương trình arm64 trên máy dựng khi biên dịch chéo |
| Chuỗi trao đổi chỉ nhận ra `B8G8R8A8_UNORM` | `rt64_application.cpp:328`, `plume_vulkan.cpp:2207-2209` | Bề mặt Android thường chỉ cung cấp `R8G8B8A8` và việc tạo chuỗi trao đổi không thành công |
| Bề mặt chỉ được tạo một lần | phụ trợ Vulkan | Android sẽ hủy `ANativeWindow` khi chuyển sang nền và không thể xây dựng lại khi quay lại nền trước. 07-10-2026 Đã sửa: `rt64_android_patches.py` cho phép `VulkanSwapChain::resize()` sử dụng cửa sổ hiện tại do máy chủ cung cấp (`graphics.cpp` được lấy từ SDL, nếu nó trống ở chế độ nền, v.v.) để xây dựng lại bề mặt khi bề mặt bị mất hoặc cửa sổ bị thay đổi; nó sẽ được khôi phục bằng cách đi tới Trang chủ trên Seeker, chuyển sang Ứng dụng "Tệp" rồi quay lại. Khóa màn hình/mở khóa mà không thay đổi cửa sổ, trước đây chuyện đó là bình thường |
| `preTransform` được cố định thành IDENTITY | `plume_vulkan.cpp:2343` | Các thiết bị có hướng màn hình gốc sẽ có thêm một vòng xoay hệ thống trên mỗi khung hình, khoảng 1–3 mili giây và trả về SUBOPTIMAL ([xoay trước Android](https://developer.android.com/games/optimize/vulkan-prerotation)) |
| `SRC1_ALPHA` (dualSrcBlend) được sử dụng để trộn cố định và không kiểm tra xem thiết bị có hỗ trợ | `rt64_raster_shader.cpp:336-337` | **Tất cả Mali đều không có tính năng này**, driver vẫn trả về thành công và màn hình trắng xóa hoàn toàn (Goemon đã thử nghiệm trên Mali-G57) |
| `preferHDR`: Điều này đúng khi bộ nhớ cục bộ của thiết bị lớn hơn 512 MB | `plume_vulkan.cpp:4136` | Điện thoại di động có bộ nhớ hợp nhất và luôn sử dụng mục tiêu kết xuất RGBA16, tiêu tốn nhiều băng thông hơn trên khối GPU (suy luận) |
| Luồng nhàn rỗi gửi các tác vụ tính toán khoảng 1 mili giây một lần để duy trì tần số GPU | `rt64_workload_queue.cpp:1179-1222` | Tiêu thụ điện năng, sinh nhiệt (suy luận) |
| Không `VkPipelineCache` và không có bộ đệm trên đĩa | `plume_vulkan.cpp:1393,1652` | Biên dịch lại đường dẫn trên mỗi lần khởi động |

**Các tính năng của Vulkan mà RT64 thực sự phụ thuộc nhưng không kiểm tra:**

- **lập chỉ mục mô tả:** Bảng kết cấu 8192 mục nhập sử dụng lập chỉ mục mẫu không đồng nhất, cập nhật sau khi liên kết, giới hạn một phần, số lượng biến và mảng thời gian chạy.
- **srcBlend kép. **
- **Kẹp độ sâu. **

Hồ sơ Vulkan dành cho Android 2022, 15 và 16 không yêu cầu ba mục này. Chỉ cấu hình Android 17 (VRA17, Vulkan 1.4) mới yêu cầu lập chỉ mục DualSrcBlend và bộ mô tả, đồng thời chỉ dành cho các chip đi kèm Android 17.

**Không bắt buộc:** semaphore dòng thời gian, hiển thị động, Int64, Float16, trình đổ bóng hình học, đổ bóng tốc độ mẫu. SPIR-V đã biên dịch chỉ có Shader, Sampled1D, SampledBuffer, ImageBuffer và các khả năng lập chỉ mục không đồng nhất.

**Shader:** Sử dụng DXC để biên dịch HLSL thành SPIR-V trong quá trình xây dựng và sau đó nhúng nó vào chương trình. HLSL sẽ không được biên dịch khi chạy trên nền tảng không phải Windows. Mã dành riêng cho x86 duy nhất là hlsl++, mã này tự động sử dụng NEON trên arm64.

### N64ModernRuntime

- **Loại tay cầm cửa sổ không khớp:** `renderer_context.hpp` Trên Android, `WindowHandle` được xác định là `SDL_Window*`, với TODO bên cạnh, trong khi đường dẫn Android Plume yêu cầu `ANativeWindow*`.
- **Chủ đề:** Mức độ ưu tiên không được triển khai trên Linux và Android (TODO).
- **Bỏ phiếu:** Cả luồng đồ họa và vòng thăm dò chính cứ sau 1 mili giây. Ngã ba của Linkzenic thay đổi khoảng thời gian vòng lặp chính của Android thành 16 mili giây.
- **Mặt trước và mặt sau:** Không có cơ chế tạm dừng. Goemon thêm `set_app_paused` và cổng tạm dừng cho luồng VI.
- **Bộ nhớ:** Dự trữ 4 GiB `PROT_NONE` trước, sau đó làm cho 512 MiB có thể đọc và ghi được, không có kích thước trang chết và không có vấn đề gì với các trang 16 KB. Bản thân macOS arm64 là một trang 16 KB.
- **ROM và kho lưu trữ:** `select_rom` chỉ chấp nhận đường dẫn hệ thống tệp và sao chép ROM vào thư mục cấu hình; kho lưu trữ được ghi bằng một tệp tạm thời và được đổi tên. `create_directories` có thể đưa ra một ngoại lệ, khiến Goemon gặp sự cố khi tháo thẻ SD.
- **Thông báo lỗi:** Hộp lỗi chỉ chạm vào stderr và Android sẽ loại bỏ stderr.

## Ngưỡng thiết bị (suy luận)

| GPU | Phán quyết |
| --- | --- |
| Adreno 6xx trở lên (Snapdragon 845 trở lên) | Sự lựa chọn đầu tiên. hỗ trợ képSrcBlend. Các vấn đề về trình điều khiển chính thức mà Goemon gặp phải: Lỗi liên kết đổ bóng Adreno 6xx (trình điều khiển 0746), con trỏ rỗng Adreno 630 trong tính toán gửi bản sao bộ đệm khung. Có nhiều cách xung quanh nó |
| Mali G7x trở lên | Yêu cầu dự phòng cho DualSrcBlend (Goemon 1.0.3 sử dụng phép tính gần đúng pha trộn một nguồn). nullDescriptor cũng có thể bị thiếu |
| PowerVR, Samsung Xclipse | Không có dữ liệu |

Việc lập chỉ mục mô tả và độ sâuClamp phải được kiểm tra khi khởi động. Nếu không hài lòng, hãy sử dụng hộp thoại để giải thích và tránh màn hình trống hoặc bị treo. Sau khi kiểm tra từng model thì dùng gpuinfo.org để làm, **lần này chưa xong**.

## Mã phân phối và dẫn xuất ROM

`libmain.so` của APK phải được liên kết với hai mã do ROM tạo: `build/recomp/cpu-bound/generated/funcs_*.c` và `build/recomp/audio-probe/audio.cpp` do RSPRecomp tạo. Trình nhập gốc ([P1](native-rom-importer.md)) chỉ tạo văn bản, hình đại diện và nghệ thuật chiến đấu trong thời gian chạy, nhưng không thể tạo hai mã này.

| Kế hoạch | Mô tả | Kết luận |
| --- | --- | --- |
| Một. Xây dựng APK đầu ra của máy và sideload | Định vị “tự sử dụng, không phân phối lại” giống như gói Deck | **Khuyến khích. ** Đây cũng là tiền lệ cho mọi cộng đồng |
| b. Người chơi tự xây dựng nó | `make` trên máy tính, sau đó chạy bản dựng Android và cuối cùng là `adb install` | Mâu thuẫn với mục tiêu của P0 "Người chơi không cài đặt Python/trình biên dịch" |
| c. APK không có mã lấy từ ROM, tạo mã trên thiết bị | Cách tiếp cận khả thi là trình biên dịch lại đúng lúc của N64Recomp (sljit, hỗ trợ ARM64) | Không bao gồm trong kế hoạch này. `generate_cpu.py` Việc viết lại mã đã tạo (khoảng 150 `NATIVE_HOOKS` đổi tên, tra cứu lớp phủ, ký tự chiều rộng bản đồ) và âm thanh RSPRecomp phải được thay đổi để triển khai thời gian chạy, việc này tốn rất nhiều công sức |

Cần lưu ý hai điểm:

- **Định vị của dự án về phân phối nhị phân không nhất quán. ** `tools/release/build_release.py` Chuẩn bị gói macOS để phát hành công khai trên GitHub, nhưng gói Linux lại ghi "tự sử dụng". APK tuân theo quyết định cuối cùng của người bảo trì, xem "TBD".
- **Xác minh nhà phát triển Android. ** Nó sẽ được ra mắt ở Brazil, Indonesia, Singapore và Thái Lan bắt đầu từ ngày 30 tháng 9 năm 2026 và sẽ được quảng bá ra thế giới vào năm 2027. Vào thời điểm đó, các APK đã tải sẵn sẽ cần phải có chữ ký của nhà phát triển đã được xác minh, nếu không, chúng sẽ phải trải qua "quy trình nâng cao" hoặc sử dụng phân phối giới hạn cho tối đa 20 thiết bị ([Mô tả](https://developer.android.com/developer-verification)). Điều này ảnh hưởng đến kiểu tải bên và cần được chú ý liên tục.

Máy xây dựng Android giống với máy xây dựng Linux. Nó chỉ yêu cầu bốn đầu vào. Xem "Các bước xây dựng nên được thực hiện trên máy nào" trong gói ba nền tảng:

- `build/recomp/cpu-bound/`
- `build/recomp/audio-probe/audio.cpp`
- đã vá `build/recomp/upstream/`
- `build/fonts/`

## Thay đổi danh sách

Mức độ nghiêm trọng: **Chặn** có nghĩa là không thể biên dịch hoặc không thể chạy; **Bắt buộc** có nghĩa là nó có thể chạy nhưng bị lỗi hoặc không sử dụng được trên Android; **Nhỏ** có nghĩa là hiệu suất, kinh nghiệm hoặc chỉ ảnh hưởng đến chức năng phát triển.

### 1. Xây dựng (chặn)

- **Cổng CMake:** `src/host/CMakeLists.txt:62-64` chỉ phát hành Apple và Linux, `CMAKE_SYSTEM_NAME` của Android là `Android`.
- **Mẫu sản phẩm:** Trò chơi nên đổi thành `add_library(main SHARED …)`, thêm `SDL_main` và liên kết `android` và `log`. `srw64-frame-host` và mỗi chương trình thử nghiệm không được đưa vào bản dựng Android.
- **Công cụ xây dựng:** `cmake/NativeGpu.cmake`, `cmake/PixelCompositor.cmake`, `src/native/ui/CMakeLists.txt` và RT64 đều chọn DXC và biên dịch `file_to_c` theo nền tảng đích. Thay đổi thành:
- Nhấn `CMAKE_HOST_SYSTEM_NAME`/`CMAKE_HOST_SYSTEM_PROCESSOR` để chọn DXC;
- `file_to_c` được biên dịch riêng trên máy xây dựng và sau đó được nhập. Cách tiếp cận của Goemon là vượt qua `-DRT64_FILE_TO_C`.
- **Ngăn xếp cuộc gọi sự cố:** `src/host/host.cpp:511-535` sử dụng `execinfo.h` trong `__linux__` và Android cũng xác định `__linux__`. bionic chỉ có `backtrace` kể từ API 33 và việc thay thế việc xử lý tín hiệu sẽ chặn bia mộ của trình gỡ lỗi hệ thống. Điều kiện được thay đổi để loại trừ `__ANDROID__`.
- **Phụ thuộc:**
- FreeType, HarfBuzz và ICU được thay đổi thành liên kết tĩnh vì APK không thể chứa các thư viện dùng chung có số phiên bản như `libicuuc.so.78`.
- ICU sử dụng tính năng lọc dữ liệu để chỉ giữ lại các ngắt dòng, văn bản hai chiều và dữ liệu hệ thống văn bản, khoảng 1–3 MB; dữ liệu đầy đủ là khoảng 30 MB. Chỉ `src/native/text/portable_text.cpp` sử dụng ICU và không có giao diện sử dụng thư viện i18n. `cmake/PortableText.cmake` có thể xóa `ICU::i18n`.
- Dự phòng pkg-config của HarfBuzz sẽ tìm thấy các thư viện của máy xây dựng khi biên dịch chéo và sẽ bị tắt trên Android.
- Lựa chọn SDL được hiển thị trong "TBD".
- **NDK và kích thước trang:** Với NDK r28 trở lên, mặc định là căn chỉnh trang 16 KB.
- **Tập lệnh xây dựng:** Tạo thư mục bản dựng Android mới và `build_android.py` (sẽ được viết), với cấu trúc là `tools/release/build_linux.py` và `tools/release/linux/Dockerfile`: NDK, JDK và Gradle được cài đặt trong vùng chứa. Quá trình kiểm tra thông báo đầu vào sẽ được chuyển tiếp, các kiểm tra liên quan đến glibc và `$ORIGIN` sẽ không được áp dụng.

### 2. Bản vá ngược dòng (chặn)

Sử dụng chuỗi danh sách trắng thay thế `tools/recomp/toolchain/prepare_rt64.py` mà không cần phân nhánh. Mỗi mục sau đây có thể được tham chiếu trong fork của Goemon; RT64 được cấp phép theo giấy phép MIT và nguồn phải được ghi chú trong `docs/guide/provenance.md` khi áp dụng nó.

1. **Có thể biên dịch:** Xóa `static_assert`; không xây dựng localfiledialog trên Android; xử lý các vấn đề về công cụ máy xây dựng của DXC và `file_to_c` (xem phần trước).
2. **Định dạng chuỗi hoán đổi:**
- Sử dụng `R8G8B8A8` trên Android và chuyển định dạng thực tế tới máy chủ thông qua `GetRenderHookSwapChainTexture` hiện có.
- Có hai phần của BGRA được mã hóa cứng trong kho lưu trữ này: đọc lại ảnh chụp màn hình (`src/host/graphics.cpp:209,239`) và quy trình tổng hợp hội thoại (`src/host/dialogue_plume.cpp:39-41`).
- Ngoài ra, hãy kiểm tra trình kết xuất giao diện của RecompFrontend.
3. **Cửa sổ và bề mặt:**
- `src/host/graphics.cpp` Thêm nhánh Android, nhận `ANativeWindow*` từ SDL;
- Thống nhất kiểu `WindowHandle` cực chất;
- Plume thêm `setRenderWindow`, xây dựng lại bề mặt và trao đổi chuỗi khi quay lại nền trước (Goemon 4c087b7, c69ce04).
4. **Tương thích GPU:**
- Dự phòng DualSrcBlend của Mali;
- Tính năng kiểm tra và báo lỗi khi khởi động;
- Tắt `preferHDR` và các luồng tính toán không hoạt động trên Android;
- Bảo vệ `vkGetRefreshCycleDurationGOOGLE`;
- Xử lý các vấn đề liên kết shader Adreno 6xx (Goemon 25fa568: spirv-opt inline, rewrite `EndianSwapUINT16`);
- Công tắc "Tắt hiệu ứng bộ đệm khung" để khắc phục sự cố Adreno 630.
5. **Thư viện thời gian chạy:**
- Luồng VI thêm các cổng tạm dừng trước và sau và đặt phiên bản viết lại được tạo bởi `tools/recomp/toolchain/prepare_runtime_lifecycle.py`;
- `create_directories` is changed to not throwing exception;
- Hộp lỗi sử dụng `SDL_ShowSimpleMessageBox` thay thế;
- Vòng lặp chính giúp thư giãn khoảng thời gian bỏ phiếu trên Android.
6. **Thực hiện việc này sau:** Xoay trước, `VkPipelineCache` bộ đệm đĩa.

### 3. Host: lối vào, đường dẫn, tài nguyên (chặn)

- **User Directory:** `default_user_dir` (`src/native/app/runtime.cpp:103-123`) fell into the Linux branch on Android, requiring `HOME` or `XDG_DATA_HOME`, both of which are not available on Android. Add `Platform::Android` to use the application internal storage path provided by SDL.
- **Tài nguyên gói:** `bundled_resource` đọc `/proc/self/exe` (`runtime.cpp:180-194`) và nhận `app_process64` trên Android. Vì vậy, không thể tìm thấy phông chữ, văn bản hội thoại và HD và giao diện chia sẻ sẽ hiển thị "Giao diện người dùng được chia sẻ cần phông chữ CJK".
- **Method:** Put `fonts/`, `dialogue/` (786 txt, about 21 MB) and `licenses/` into the APK resource, press versionCode to extract to the private directory when starting for the first time, and then point the resource root directory there.
- **Why it is necessary to solve:** Dialogue loading uses `recursive_directory_iterator` to traverse the directory, and Android's `AAssetDir` cannot list subdirectories.
- **Lối vào khởi nghiệp:**
- Hiện chỉ có Apple mới có mục đồ họa không tham số (`src/host/host.cpp`). The Android portal uses SAF (`ACTION_OPEN_DOCUMENT`) to select the ROM on the Java side, copies it to `rom.z64` in the private directory, and then gives the path to C++ to assemble `Options`.
- Phải sao chép vì `select_rom`, `sha256_file` và `fs::canonical` đều có đường dẫn thực.
- Logic của `srw64.sh` (tìm ROM, ngôn ngữ khởi động đầu tiên) cũng đã được chuyển sang C++, vốn ban đầu được lên kế hoạch cho Windows.
- **Gói HD:**
- Thư mục khoảng 700 MB không có APK. Máy chủ tìm kiếm nó (`launch.cpp`) trong thư mục người dùng `files/user/hd`, giống như `Marchwind64-HD-<HD 版本>.zip` trên máy tính.
- Mỗi lớp HD sử dụng `directory_iterator` để đọc thư mục nên phải là thư mục đã được giải nén.
- Done (2026-10-05, `SetupActivity.importHd`): Use SAF to read the zip on the startup page, only decode the entries under `hd/` to `files/user/hd.new`, and exchange with the old directory only if `hd.json` exists. Lỗi hoặc gián đoạn sẽ không di chuyển gói đã cài đặt; hiển thị phần trăm theo byte nén và kiểm tra dung lượng còn lại trước. Ba lối vào: hỏi một lần sau khi chọn ROM lần đầu tiên; nhấn và giữ phím tắt tĩnh của biểu tượng "Nhập gói HD" (`res/xml/shortcuts.xml`, hành động `org.srw64.game.IMPORT_HD`); sử dụng ứng dụng này để mở/chia sẻ zip trong trình quản lý tệp hoặc trình duyệt. Trò chơi không được nhập khi đang chạy (máy chủ không được đăng nhập lại, `SRW64Activity.running`) và bạn được nhắc đóng trò chơi trước. Bạn vẫn có thể đặt `adb push` + `run-as` trong quá trình phát triển.
- Tôi chưa thực hiện quá trình nhập trên thiết bị thực.
- **Nhật ký và báo cáo lỗi:**
- stderr vào logcat và ghi tệp nhật ký phiên.
- Hướng đến người chơi `std::abort()` (`graphics.cpp`, `src/host/audio.cpp`, `host.cpp`) trước tiên được đổi thành `SDL_ShowSimpleMessageBox`.

### 4. Vòng đời và lưu trữ (chặn, quan trọng nhất)

- **Thời gian nộp hồ sơ lưu trữ:**
- Hiện tại, các bản lưu trữ chỉ được cam kết nếu máy chủ trả về 0 (`src/native/app/launch.cpp:204-205`). Android thường tắt các tiến trình ngay trong nền (bộ nhớ thấp hoặc trình phát bị gạch bỏ). Tiến trình của toàn bộ trò chơi sẽ không trở thành "phiên cuối cùng" và lần lưu trước đó sẽ được tiếp tục một cách lặng lẽ vào lần bắt đầu tiếp theo.
- Để thay đổi thành điểm kiểm tra nguyên tử có thể được gửi nhiều lần: nhập nền (`SDL_APP_WILLENTERBACKGROUND`), `SDL_APP_TERMINATING` và gửi một lần sau mỗi đĩa SRAM.
- Điều này sẽ thay đổi quy tắc P0 "Chấm dứt bất thường không được sử dụng làm nguồn khôi phục" và yêu cầu xác nhận từ nhà bảo trì.
- **Chuyển đổi nền trước và nền sau:** Bây giờ, sự kiện `SDL_APP_*` hoàn toàn không được xử lý.
- Nhập nền: tạm dừng khách và VI, tạm dừng âm thanh, dừng kết xuất RT64, gửi bản lưu trữ.
- Quay lại nền trước: Xây dựng lại bề mặt và chuỗi trao đổi, sau đó khôi phục.
- **Nguy cơ bị kẹt:** `lock_ui()` trong số `src/native/ui/frontend.cpp` phải đợi cho đến khi lệnh gọi lại bản trình bày xóa `in_flight` trước khi quay lại và `apply_images` cũng sẽ tiếp tục chờ. Khi bề mặt bị mất và quá trình hiển thị bị đình trệ, luồng chính sẽ bị chặn vĩnh viễn và Android sẽ báo cáo ANR. Chuyển sang chế độ chờ có thời hạn và chủ động dọn sạch bề mặt khi bị mất.
- **Đăng ký lại `SDL_main`:** Cả thời gian chạy và máy chủ đều không được đăng ký lại. Khi Hoạt động bị hủy, quá trình sẽ kết thúc trực tiếp. `configChanges` được khai báo trong tệp kê khai và màn hình ngang được cố định.
- **Ngày càng bị chiếm dụng nhiều hơn:** Tạo một thư mục phiên mới mỗi khi nó được bắt đầu, với bản sao `dialogue.json`; cũng như 30 giây ghi âm đầu tiên và JSON trực tiếp được viết lại mỗi giây. Tắt tính năng ghi và JSON trực tiếp trên Android, đồng thời dọn sạch các phiên cũ. `content-cache/`, `sessions/` và ROM bị loại khỏi quá trình sao lưu tự động của Android: chúng là các phiên bản ROM phái sinh và kích thước của chúng vượt quá hạn mức sao lưu.

### 5. Màn hình, bộ nhớ và hiệu năng (phải thay đổi)

- **Mặc định chất lượng:** Hiện mặc định là 4x MSAA cộng với độ phân giải 4x. Mặc định Android tắt MSAA và tăng độ phân giải gấp 3-4 lần, tham khảo số đo thực tế của Goemon.
- **Bộ nhớ HD:**
- Tất cả RGBA8 không nén với chuỗi mip đầy đủ, nền tối đa 1920×1440.
- Bộ nhớ đệm hình ảnh của RmlUi không bao giờ bị loại bỏ (`frontend.cpp`) và phải thêm LRU.
- Phông chữ HarmonyOS SC 20,6 MB, mỗi phông chữ `FontSet` đọc một bản sao, tệ nhất là từ năm đến mười bản và cần phải thay đổi để chia sẻ bộ đệm.
- Giải phóng bộ nhớ đệm khi nhận được `SDL_APP_LOWMEMORY`.
- **Mức độ chẩn đoán:** Khi biến môi trường không được đặt, mặc định là chẩn đoán đầy đủ (kết xuất RDRAM thông thường, đọc lại toàn bộ khung và mã hóa PNG); chẩn đoán đầy đủ đã bị xóa khỏi máy chủ và không cần thiết lập lại cổng Android.
- **Tốc độ làm mới:** 90/120 Hz trên điện thoại di động yêu cầu 60 Hz để tránh hiện tượng giật hình thời gian kết xuất.

### 6. Đầu vào và giao diện

**Bàn soi cầm tay (bắt buộc phải thay đổi, số lượng ít):**

- Bộ điều khiển có sẵn như sau: liên kết, sửa đổi khóa, bộ điều khiển → cầu nối nút trang và lời nhắc NhắcFont.
- Chặn phím quay lại của Android và ánh xạ tới B.
- Thêm phán đoán "cầm tay" bên cạnh `src/host/steam_deck.hpp` cho trang cài đặt để ẩn kích thước cửa sổ và dòng toàn màn hình.

**Giai đoạn điện thoại di động (bắt buộc phải sửa đổi, số lượng lớn):**

- **Bộ điều khiển ảo màn hình cảm ứng:** Bao gồm các phím N64 và phím chủ (L2, R2, phím xem, v.v.). Nút được gửi qua cổng chèn đầu vào (`src/host/debug_protocol.hpp`) của giao diện gỡ lỗi và lời nhắc về trang và nút sẽ coi nút đó như một tay cầm.
- **Mật độ giao diện:**
- `sync()` trong số `frontend.cpp` coi dp là điểm SDL. Tỷ lệ pixel trên Android là 1. Trên điện thoại di động 2400×1080, phông chữ 17 dp chỉ cao khoảng 1,5 mm.
- Thay vào đó, hãy sử dụng hệ số tỷ lệ hoặc mức độ phân giải của màn hình.
- Màn hình ngang trên thiết bị di động chỉ có độ cao khoảng 360–430 dp và các trang hiện tại được thiết kế ở độ phân giải 540–720 dp, yêu cầu bố cục di động hoặc kích thước vật lý tối thiểu.
- **Vùng an toàn:**
- Màn hình game rộng nhất tới 16:9 theo `src/host/game_frame.hpp`, để lại màu đen 2 bên màn hình 20:9 và không bị ảnh hưởng bởi tiếng nổ.
- Trang RmlUi che toàn bộ cửa sổ nên tránh hiện tượng bang và thanh cử chỉ.
- **Chi tiết màn hình cảm ứng:**
- Thêm văn bản nhắc nhở cho màn hình cảm ứng;
- Thêm nút quay lại và lật trang về trang gốc;
- Hỗ trợ kéo và cuộn;
- Giải quyết vấn đề điểm nổi bật khi di chuột không biến mất sau khi chạm vào;
- Hợp nhất các sự kiện di chuyển bằng cách chạm, mỗi sự kiện hiện chờ `lock_ui()` một lần.
- **Phương thức nhập:** Sử dụng bàn phím số cho ô nhập quỹ. `src/native/ui/text_input.cpp` được gọi một lần trên mỗi khung. `SDL_SetTextInputRect` được gọi mọi lúc trên Android. Nó chỉ được gọi khi vị trí thay đổi.

### 7. Giao diện gỡ lỗi (phải thay đổi)

- Ổ cắm AF_UNIX hiện tại được đặt trong thư mục riêng của ứng dụng và `adb forward` không thể truy cập được, đồng thời độ dài đường dẫn gần với giới hạn trên 108 byte của `sun_path` (`src/host/debug_server.cpp`).
- Chuyển sang TCP loopback theo kế hoạch của gói ba nền tảng X0 và thêm mã thông báo, sau đó kết nối qua `adb forward tcp:`. `srw64ctl` và MCP không cần phải viết riêng cho Android.
- Cách tiếp cận thực tế (đã triển khai): Android sử dụng các ổ cắm trừu tượng `@srw64-debug`, `adb forward tcp:0 localabstract:srw64-debug` để kết nối mà không cần mã thông báo. Nền tảng ba máy tính để bàn 2026-10-06 đã thay đổi thành mã thông báo loopback TCP plus, xem [Giao diện gỡ lỗi · Phương thức kết nối](../guide/debug-interface.md#连接方式).
- Bản phát hành phải có khả năng loại bỏ giao diện gỡ lỗi trong quá trình biên dịch.

### Đã có sẵn, không cần thay đổi

- **Đồ họa:** Các lớp HD, tổng hợp hội thoại, RmlUi đều hoạt động tốt và nhúng SPIR-V. Bộ đệm không đổi vòng, hằng số đẩy 16 byte và quy trình dành riêng cho định dạng của `native_gpu` đều phù hợp với GPU di động.
- **Độ chính xác của ARM:** Thứ tự bộ nhớ yếu, trang 16 KB và giả định về cuối nhỏ, tất cả đều được xác minh trên macOS arm64.
- **Văn bản và Nghệ thuật:** Ngăn xếp văn bản đều là giao diện C và phông chữ được tải từ bộ nhớ. Tỷ lệ khung hình thích ứng từ 4:3 đến 16:9.
- **Phần POSIX của lớp ứng dụng:** `flock`, đổi tên nguyên tử và `std::filesystem` đều hoạt động trên bionic.
- **Công cụ gỡ lỗi:** Nhiều công cụ thăm dò và QA khác nhau được bật bởi các biến môi trường và không có hiệu lực theo mặc định.

## Sân khấu

### Xác minh tính khả thi A0 (không cần ROM)

- Biên dịch chéo lớp ứng dụng và trình nhập của CMake gốc với các bài kiểm tra bằng NDK và chạy trên thiết bị có `adb shell`.
- Bản vá 1 cho RT64 và Plume, biên dịch phiên bản Android; xây dựng cửa sổ bằng SDL và xóa màn hình một khung hình thông qua chùm tia.
- Đặt tuyến đường SDL (TBD 1).

**Chấp nhận:** Tất cả các thử nghiệm trên thiết bị đều đạt; Thiết bị Adreno có thể hiển thị ổn định màu sắc màn hình rõ ràng, không bị treo sau khi chuyển sang chế độ nền và quay lại.

### Máy chơi game cầm tay Android A1, màn hình nguyên bản

- Tập lệnh xây dựng Android, dự án Gradle và `libmain.so`;
- Lối vào Android, khai thác tài nguyên, ROM chọn SAF;
- Kiểm tra tính năng ở các bản vá 2, 3, 5 và 4 ngược dòng;
- Điểm dừng và điểm kiểm tra lưu trữ trước và sau;
- Nhật ký đi tới logcat.

**Chấp nhận (Bảng điều khiển cầm tay Adreno, chỉ có tay cầm):**

- Mở đầu → Tên → Chương 1 → Lưu trữ;
- Cắt nền trong 5 phút rồi quay lại tiếp tục;
- Khởi động nguội sau khi bỏ qua quy trình và có thể được khôi phục từ điểm kiểm tra lý lịch;
- L3/R3 chuyển ngôn ngữ và màn hình;
- Cửa sổ cài đặt có thể được mở.

### GPU A2 tương thích HD

- Khôi phục Mali, bỏ qua Adreno khác nhau và mặc định chất lượng hình ảnh;
- Nhập gói HD và thắt chặt giới hạn bộ nhớ theo Android;
- Tùy chọn: xoay trước.

**Chấp nhận:**

- Thêm điện thoại Adreno vào điện thoại Mali, kết nối bộ điều khiển, bật HD và chạy quy trình tương tự;
- Bộ nhớ không tiếp tục tăng trong 30 phút liên tục;
- Ghi lại tốc độ khung hình và sinh nhiệt.

### Màn hình cảm ứng điện thoại di động A3

- Bộ điều khiển ảo màn hình cảm ứng, dpi, vùng an toàn, bố cục phiên bản di động, lời nhắc trên màn hình cảm ứng và phím quay lại.

**Chấp nhận:** 20:9 Chỉ sử dụng màn hình cảm ứng trên điện thoại di động của bạn để hoàn thành phần mở đầu → Tập 1 → Trận chiến → Lưu trữ.

### Bao bì A4

- **Chữ ký và tên file:** Sử dụng key tự ký, tên file tuân theo quy định của gói Deck: `SRW64-Android-<版本>-<提交日期>-<提交>.apk`.
- **Hoàn thiện tệp giấy phép:** Các gói Linux hiện cũng thiếu giấy phép cho RT64, N64ModernRuntime, RmlUi, RecompFrontend, volk, v.v.
- **Phông chữ HarmonyOS:** Giấy phép chỉ cho phép phân phối cùng với phần mềm mà không sửa đổi nên không thể cài đặt lại để thu nhỏ APK.
- **MÔ TẢ:** Viết hướng dẫn README và sideload.

## TBD

1. **Tuyến SDL:**
- a. Sử dụng SDL3 + sdl2-compat như máy tính để bàn. Khóa phiên bản giống nhau. Keo Java của SDL3 đi kèm với hỗ trợ SAF và `content://` nhưng chưa có cổng chuyển nào xác minh rằng sdl2-compat có thể được sử dụng trên Android.
- b. Sử dụng keo Android đi kèm với SDL2 2.32. Tất cả các tiền lệ của cộng đồng đều thực hiện điều này với chi phí là nguồn phiên bản SDL thứ hai.
- c. Máy chủ trực tiếp sử dụng giao diện SDL3. Ngoài ra, việc giải quyết sự phụ thuộc của RT64 vào SDL2 là thay đổi lớn nhất.

Bạn nên thử a trên A0 trước, nếu không được thì quay lại b.
2. **Quy tắc lưu trữ trên Android:** Liệu các điểm kiểm tra lý lịch có được tính là các lần xác nhận thông thường hay không (xem Phần 4).
3. **Định vị phân phối:** Android được thiết lập ở chế độ sideload để tự sử dụng như Linux hoặc sẽ theo sau bản phát hành công khai của macOS. Đây là vấn đề toàn dự án, không chỉ liên quan đến Android.
4. **Thiết bị chấp nhận:** Bạn có thiết bị cầm tay hoặc điện thoại di động Android trong tay không? A1 trở lên yêu cầu ít nhất một thiết bị Adreno, A2 cũng yêu cầu thiết bị Mali.
5. **minSdk:** Đặt 28 hoặc cao hơn.
6. **libadrenotools/Turnip:** Không nên thực hiện việc này trong đợt đầu tiên và việc này sẽ là tùy chọn trong tương lai.

## Không có trong kế hoạch này

- Được liệt kê trên Google Play;
- APK không có mã dẫn xuất ROM (biên dịch lại trên thiết bị);
- x86_64 và ABI 32-bit;
- Bố cục màn hình dọc;
- Lưu đám mây.