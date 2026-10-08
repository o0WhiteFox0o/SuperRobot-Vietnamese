> **Ngôn ngữ / Language:** [Tiếng Việt](plume-pixel-compositor.vi.md) · [English](plume-pixel-compositor.en.md) · [中文](plume-pixel-compositor.md)

# Tổng hợp pixel Plume phổ quát (P2b)

2026-09-20. Tiếp tục từ [phân chia phụ trợ CPU/GPU](shared-game-ui.md). Trình tải lên pixel và bộ tổng hợp GPU hiện là đường dẫn hội thoại mặc định, hoạt động với [văn bản đa nền tảng tiếng Trung, tiếng Nhật và tiếng Anh](portable-text.md).
Quá trình di chuyển bề mặt ba nền tảng của toàn bộ trò chơi vẫn chưa hoàn tất.

## Ranh giới trách nhiệm

`src/native/presentation/pixel_compositor.*` chỉ sử dụng giao diện công cộng Plume; đầu vào là
Các pixel riêng của `Bgra8Surface`, đầu ra là lệnh vẽ được ghi vào danh sách lệnh của người gọi.
Nó không tạo cửa sổ, gửi hàng đợi, đợi GPU hoặc đọc thư mục ngôn ngữ, ROM hoặc trạng thái trò chơi.
`cmake/PixelCompositor.cmake` được chia sẻ bởi trò chơi và các bài kiểm tra độc lập; cùng một cặp HLSL được biên dịch riêng biệt như
SPIR-V, DXIL và Kim loại. Việc kết hợp toàn bộ pixel đơn giản sử dụng SM6.0, không yêu cầu SM6.3 mà không có lý do; Máy chủ Windows 2022
Việc xác thực trình điều khiển phần mềm đã chứng minh rằng các phiên bản mới hơn có thể khiến quá trình tạo đường ống không thành công. Công cụ tạo chỉ được sử dụng để xây dựng và không đưa vào chuỗi khởi động người chơi.

Các quy ước về pixel vẫn giữ nguyên: BGRA8 chặt chẽ từ trên xuống, alpha được nhân trước, nhắm mục tiêu BGRA8/RGBA8 UNORM mẫu đơn.
Tải lên được sao chép với căn chỉnh dòng 256 byte; trình đổ bóng đọc ở tọa độ đoạn nguyên mà không cần thêm tính năng lọc, chia tỷ lệ hoặc
chuyển đổi sRGB. Trộn màu sử dụng ONE/ONE_MINUS_SRC_ALPHA và không thể nhân alpha nguồn lại.
Hình ảnh có định dạng không xác định, HDR, kích thước không nhất quán, hình ảnh trống và các thành phần tổng hợp khác sẽ bị từ chối.

Mỗi lần tải lên sẽ tạo ra các kết cấu độc lập, bộ đệm và bộ mô tả theo giai đoạn, đồng thời không thể cập nhật các kết cấu vẫn được GPU sử dụng.
`Retention` được `Image` trả về và `draw()` giữ cho các tài nguyên này cũng như quy trình/bố cục/trình đổ bóng của chúng luôn tồn tại.
Người gọi phải được giữ lại cho đến khi GPU tương ứng hoàn thành; riêng các bản ghi tải lên không vẽ cũng phải giữ lại Hình ảnh.
Hình ảnh chỉ được sử dụng trong cùng một hàng đợi đồ họa có thứ tự và danh sách lệnh dựa trên việc tải lên phải được gửi trước; nếu danh sách tải lên bị hủy,
Hình ảnh tương ứng phải bị loại bỏ và không thể sử dụng làm bộ đệm có thể sử dụng được. Thiết bị kết xuất phải bị hủy muộn hơn bất kỳ tài nguyên đang truyền nào.

Bắt đầu từ ngày 02 tháng 10 năm 2026, sẽ có canvas cố định: `canvas(w, h)` tạo họa tiết giữ lại nội dung trên các khung, `update()` tạo một
`Bgra8Surface` (x, y) đã tải lên khung vẽ, được ghi trên cùng một hàng đợi theo thứ tự, được xếp hạng sau bản vẽ trước đó của khung vẽ đó; trả lại
Staging cũng được giữ cho đến khi GPU hoàn thiện. `draw()` có thể được sử dụng bằng kéo để chỉ vẽ phần thực sự bị hình ảnh che phủ. Nội dung canvas đang được tải lên
Ghi đè trước đây không được xác định.

## Nối dây trò chơi

`src/host/dialogue_plume.cpp` là lớp thích ứng mỏng của máy chủ, được Metal và Vulkan chia sẻ: Tìm khối lượng công việc phù hợp
Khung đối thoại bất biến, sử dụng `IncrementalRaster` để chỉ vẽ lại hình chữ nhật đã thay đổi và tải nó lên khung vẽ thường trú của kích thước cửa sổ, đồng thời sử dụng `srw64_after_gpu` để giữ lại tham chiếu tài nguyên cho GPU để hoàn thành
(Metal sử dụng trình xử lý hoàn thành của bộ đệm lệnh và các phần phụ trợ khác sử dụng RT64 để hiển thị hàng rào hàng đợi sau khi chờ đợi.
`RenderHookPresented`). Định dạng đổ bóng được lấy từ khả năng của `RenderInterface`. Các mục tiêu vẫn chỉ được truy vấn trên Metal
Định dạng của tệp đính kèm; đã sửa lỗi chuỗi trao đổi B8G8R8A8 nhắm mục tiêu RT64 trên Vulkan (25/09/2026, [Linux Build](../guide/linux-build.md)).

Trò chơi biên dịch trực tiếp bằng bộ điều hợp hội thoại Plume; hộp thoại cũ Công tắc tổng hợp kim loại và bộ chọn phụ trợ đã bị loại bỏ.
Cảnh CPU sử dụng FreeType/HarfBuzz/ICU, giữ lại trình đọc gốc, phân trang, đánh giá và ảnh chụp nhanh ngôn ngữ.

Trong môi trường nơi bạn đã có ROM cục bộ/các phần phụ thuộc phát triển đầy đủ, hãy thử nghiệm các bản dựng độc lập và thư mục người dùng:

```sh
make host
cmake -S src/host -B build/recomp/gfx-plume-build \
  -DSRW64_ENABLE_RT64=ON \
  -DPython3_EXECUTABLE="$PWD/.venv/bin/python"
cmake --build build/recomp/gfx-plume-build --target srw64-gfx-host --parallel 6
./build/recomp/gfx-plume-build/srw64-gfx-host --play \
  --rom "$PWD/rom.z64" --user-dir "$PWD/build/recomp/plume-play" --new-game
```

Không ghi đè thư mục dữ liệu người chơi bằng thư mục dùng thử trò chơi mới. Quá trình chơi game trên cần được xác minh trên máy thực tế và không thể suy ra từ CI thành phần.

## Xác minh độc lập

`tests/pixel_compositor/` không liên kết tới SDL, mã trò chơi hoặc CoreText; sử dụng các bản đồ pixmap bất đối xứng tổng hợp,
So sánh kết quả vẽ GPU thực tế, hoàn thành hàng rào và đọc lại với công thức trộn được nhân trước của CPU. Bao gồm 1×1, 3×5,
Chuyển đổi mục tiêu 65×17, 321×241, 800×600, 1100×760, BGRA/RGBA, trộn hai lớp và trong suốt/mờ/đục
Pixel và tải lên đầy đủ cộng với cập nhật cục bộ của canvas thường trú, tổng cộng 60 lần đọc lại; cho phép làm tròn sai số 1 đơn vị lượng tử hóa trên mỗi kênh.

Quá trình kiểm tra cũng giải phóng bộ tổng hợp và bộ đệm trước khi gửi, chỉ để lại tham chiếu hoàn thành; vẽ hình ảnh cũ, hình ảnh mới và
Sử dụng lại hình ảnh cũ, kiểm tra việc phát hành tài nguyên sớm, nội dung có bị ghi đè và rò rỉ tham chiếu sau khi hoàn thành hay không. Việc kiểm tra các tham số không hợp lệ vẫn tiếp tục.

Đã sửa lỗi hướng đọc lại từ kết cấu đến bộ đệm của Plume có khoảng cách độc lập: Metal/Vulkan không được triển khai; D3D12 vô điều kiện
Đặt vị trí mẫu cho mỗi kết cấu mục tiêu, hủy tham chiếu con trỏ null tới mục tiêu bộ đệm. Vì vậy, các lần đọc lại cho bài kiểm tra tương ứng được sử dụng
Metal blit, vkCmdCopyImageToBuffer và D3D12 CopyTextureRegion; Vulkan cũng có rào cản máy chủ,
phân bổ vô hiệu sau hàng rào. Chúng nằm trong lớp thích ứng thử nghiệm và không sửa đổi hoặc thay thế bản tải lên/bản vẽ công khai đang được thử nghiệm.
Điều đó không có nghĩa là phần phụ trợ ảnh chụp màn hình sản xuất đã được di chuyển.

`SRW64_PIXEL_TEST_WARP` dành cho Windows Chỉ dành cho thử nghiệm độc lập: xác minh đã sửa bản tóm tắt mã nguồn Plume, trong
Thư mục bản dựng tạo ra một bản sao cho phép liệt kê bộ điều hợp phần mềm, chẩn đoán lỗi nâng cao và không thay đổi các phần phụ thuộc vào quá trình thanh toán hoặc phần phụ trợ trò chơi.
Kết quả Vulkan của phần mềm WARP và Linux Mesa là bằng chứng về việc thực thi API/trình điều khiển thực tế chứ không phải hiệu suất GPU vật lý hoặc
Bảo hiểm trình điều khiển nhà cung cấp. Trình điều khiển ảo CI cho macOS 14 thiếu lệnh gọi bộ mã hóa đối số được Plume sử dụng; macOS 15
Thử nghiệm này có thể được thực hiện. Lô này sử dụng macOS 15 GPU CI, điều này không có nghĩa là tất cả các máy macOS 14 vật lý đều không được hỗ trợ.

```sh
cmake -S tests/pixel_compositor -B build/pixel-gpu \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DSRW64_RT64_HEADERS="$PWD/build/recomp/upstream/RT64"
cmake --build build/pixel-gpu --config RelWithDebInfo --parallel 2
ctest --test-dir build/pixel-gpu -C RelWithDebInfo --output-on-failure --verbose
```

Tác vụ GitHub đã bị đóng và các bài kiểm tra GPU có thể được thực thi cục bộ bằng lệnh trên. Đọc lại tổng hợp không thay thế GPU cho các trò chơi thực
khối lượng công việc/mở rộng cửa sổ/chuyển đổi ngôn ngữ/hồi quy thoát. Hiện tại, bề mặt cửa sổ, đọc lại ảnh chụp màn hình và
Điểm đánh dấu, phương thức nhập hệ điều hành và chấp nhận khởi động nguội trò chơi trên ba nền tảng. Xác minh thiết bị vật lý Vulkan cũng phải bao gồm cả việc xác minh không mạch lạc
Tải lên bộ nhớ: Đã sửa lỗi bản đồ/không bản đồ của Plume chưa được thực thi rõ ràng/không hợp lệ và trình điều khiển phần mềm không thể thay thế nó.
Sửa đổi và xác minh hợp đồng hiển thị bộ nhớ này. Không có trò chơi, ROM hoặc tiện ích bổ sung phông chữ nào được phát hành.