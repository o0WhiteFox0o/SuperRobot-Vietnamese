> **Ngôn ngữ / Language:** [Tiếng Việt](native-model-replacement.vi.md) · [English](native-model-replacement.en.md) · [中文](native-model-replacement.md)

# Thay thế mô hình 3D gốc: 5600 điểm

Quyền truy cập tương tự sau đó đã được mở rộng cho các con tàu, địa danh và dấu vết trong các đoạn cắt cảnh trên bản đồ thế giới, xem [Mô hình cắt cảnh bản đồ thế giới HD](native-ship-model.md).

## 2026-09-24: Bảo quản dấu HD gốc

Hình dạng HD được thay đổi từ hình dạng giọt nước tròn trở lại hình dạng ban đầu. 5600 ban đầu là một hình chóp tứ giác đôi có đỉnh ngắn và đáy dài: vòng vuông ở thắt lưng ở Y = 6, bốn góc là (±5, 6, ±5); đầu trên ở Y = 12 và đầu dưới ở Y = −12, với tổng số 8 mặt, được giải bằng hai `G_VTX` và tám `TRI1` của tài nguyên ROM.

- **Lưới**: được tạo bởi [`prepare_native_marker.py`](../../tools/recomp/model5600/prepare_native_marker.py). Phương pháp này là dịch mỗi cạnh của bicon vào trong 0,5 đơn vị, sau đó thực hiện phép tính tổng Minkowski với một quả cầu có bán kính 0,5:
- 8 mặt vẫn là mặt phẳng ban đầu, đã được tô màu;
- 12 cạnh trở thành mặt trụ, 6 góc nhọn trở thành mặt cầu, pháp tuyến là liên tục;
- Hai múi hướng ra ngoài bù cho lượng vết lõm của fillet nên Y vẫn là −12…12 và X/Z nằm trong phạm vi ±5;
- Tổng cộng có 510 đỉnh, 1.016 hình tam giác và là một mặt kín.
- **Chất liệu** (bộ đổ bóng phân đoạn 5600 `src/host/shaders/HdMarkerPS.hlsl`):
- Màu nền được thay đổi từ vàng cam (1,0, 0,57, 0,045) sang gần với màu vàng sáng ban đầu (1,0, 0,82, 0,16), và độ phản xạ khuếch tán bị suy yếu;
- Chọn màu giữa giếng trời (1,0, 0,96, 0,80) và mặt đất ấm (0,55, 0,38, 0,08) theo hướng phản chiếu và thêm dải nổi bật đường chân trời;
- Mặt phẳng sáng tối rõ ràng theo hướng của nó. Khi trò chơi xoay nó, dải sáng sẽ lần lượt quét qua từng mặt và vát cạnh.
- **Máy thật** (Bản đồ thế giới mini cấp độ tập 8, chế độ HD): Hình bát diện bằng vàng với các đường vân sáng bóng; F6 vẫn có thể chuyển về hình dạng kim cương ban đầu.
- Các gói tài nguyên được tạo lại trong `build/recomp/native-marker/assets` và các gói giọt nước cũ được chuyển sang `assets-waterdrop-20260910`. Trình xem mô hình hiển thị "Native HD · 1.016 mặt". Bằng chứng chấp nhận ban đầu đã được ghi lại cho Shuidi và sẽ không còn được hiển thị nếu bản tóm tắt dạng lưới không khớp.
- Giá trị của profile vẫn được gọi là `model_5600: waterdrop` nhưng tên vẫn được sử dụng và dấu cạnh này thực sự được vẽ.

Sau đây là kỷ lục của phiên bản đầu tiên (giọt nước).

Phiên bản đầu tiên vào ngày 10-09-2026 đã thay thế những viên kim cương màu vàng trên bản đồ cốt truyện bằng những giọt nước tròn trịa màu vàng. Lưới, thông thường và vật liệu được GPU chủ hiển thị và trò chơi gốc tiếp tục cung cấp vị trí, góc quay, camera và thời gian câu chuyện. Sử dụng rom gốc tiếng Nhật. Một thử nghiệm ROM ban đầu để biên dịch lưới 96 mặt vào tài nguyên đã bị xóa vào ngày 24-09-2026.

## Hãy dùng thử

**F6** của lối vào hợp nhất `scripts/Play SRW64 Native.command` đã hỗ trợ chuyển đổi giữa hình ảnh và kiểu máy 5600: HD là dấu HD gốc (giọt nước trước ngày 24-09-2026) và Bản gốc khôi phục hình thoi tám cạnh ban đầu; nó có thể được chuyển đổi qua lại trong cốt truyện. Nếu `presentation.model_5600` của cấu hình được đặt thành `original` thì mô hình gốc cũng sẽ được duy trì ở chế độ HD.

Thực thi trong thư mục gốc của kho:

```sh
.venv/bin/python tools/recomp/run/play_native.py --native-waterdrop --new-game
```

Chọn Trò chơi mới → Siêu nhân nữ và nhập phần mở đầu của tập đầu tiên với tên mặc định. Các phím mũi tên di chuyển, Z xác nhận, X hủy, Enter bắt đầu và Esc đóng cửa sổ. Mục này sử dụng bản ghi và lưu trữ dùng thử độc lập theo `build/recomp/native-marker/play/`; lần chạy đầu tiên sẽ tạo ra lưới thả khi thiếu gói tài nguyên. Sử dụng các lối vào dùng thử khác để quay lại phiên bản gốc.

Trang tài nguyên cục bộ 5600 hỗ trợ 2 lựa chọn: bản gốc 8 mặt và bản địa thả nước 3.968 mặt. Trang này sử dụng cùng một hình học và các chuẩn mực liên tục, đồng thời vật liệu vàng được trang web gần đúng; ánh sáng trong trò chơi tuân theo biểu đồ so sánh GPU.

## Quyền truy cập kết xuất

`tools/recomp/toolchain/native_model_hook_patches.py` Áp dụng bản vá hẹp cho phiên bản RT64 bị khóa thông qua `prepare_rt64.py`:

1. Bộ xử lý TRI1 của F3DEX2 gọi chức năng nhận dạng máy chủ. Xác định phân đoạn 4 hiện tại làm địa chỉ cơ sở, kiểm tra tài nguyên 5600 gốc hoàn chỉnh 7.048 byte và kiểm tra độ lệch của tám lệnh tam giác đặc. Những thay đổi về địa chỉ vùng heap không ảnh hưởng đến việc nhận dạng và các vòng chấm không được đánh dấu.
2. Tám lệnh của phần thân ban đầu tạo thành các lệnh rút thăm độc lập. Cái đầu tiên mang các điểm đánh dấu bản vẽ gốc và bảy cái còn lại mang các điểm đánh dấu bị loại bỏ. Điểm đánh dấu được sao chép vào Khối lượng công việc bất biến bằng lệnh gọi rút thăm.
3. Khi RT64 gửi bản vẽ raster, nó gọi trình kết xuất máy chủ và nhận được chuyển đổi thế giới, hình chiếu khung nhìn, khung nhìn RSP, hình cắt kéo và tỷ lệ màn hình từ Khối lượng công việc tương ứng. Lệnh gọi lại GPU không đọc RDRAM của khung hình mới nhất.
4. `src/host/native_marker.cpp` Trong cùng một bộ đệm lệnh, sử dụng tệp đính kèm màu/độ sâu của cảnh hiện tại ở chế độ Tải/Cửa hàng để vẽ lưới dấu phẩy động, tuân theo cài đặt ghi và so sánh độ sâu của bản vẽ ban đầu. Sau đó khôi phục trạng thái đồ họa của RT64 và tiếp tục vẽ cảnh, hình đại diện và văn bản.

Phần thả chứa 1.986 đỉnh, 3.968 hình tam giác, sử dụng chỉ mục 32 bit. CPU tải lên bộ đệm máy chủ khi khởi động mà không cần thông qua bộ đệm đỉnh N64 hoặc định dạng đỉnh số nguyên. Chiều cao cục bộ vẫn là Y = −12…12 và bán kính xung quanh tối đa là khoảng 5,5; vòng nét đứt vẫn sử dụng hình học và kết cấu ban đầu.

Vật liệu được ước tính gần đúng bằng cách sử dụng phép nội suy thông thường trên mỗi pixel, ánh sáng phím mềm, ánh sáng lấp đầy, phản xạ gương và cạnh. Vàng mờ hiện tại và không bao gồm khúc xạ, bóng động hoặc phản xạ môi trường thực. Giọt nước đối xứng quanh trục của nó nên dù có kế thừa chuyển động quay ban đầu thì hình dạng cũng sẽ không thay đổi đáng kể như hình thoi.

## Bằng chứng xác minh

Chấp nhận liên kết chế độ vào ngày 11 tháng 9 năm 2026 là `build/recomp/model-mode-check/acceptance.json`: Bốn lần phát lại GPU của cùng một tác vụ đã xác nhận rằng Original đã tải gói giọt nước và hoàn toàn không tải gói mô hình và sự khác biệt về mô hình của HD chỉ nằm trong khu vực được đánh dấu `[461,320,500,363]`; cùng một trò chơi gốc đã được chạy để hoàn thành Bản gốc → HD → Bản gốc → HD, trạng thái hội thoại vẫn nhất quán và chuyến đi vòng quanh khu vực tĩnh của hình đại diện/bản đồ được khôi phục từng pixel. Kiểm tra đồ họa và nội dung, 60 bài kiểm tra Python đã được thông qua và bài kiểm tra máy thực tế diễn ra im lặng trong suốt quá trình. Gói mô hình vẫn nằm trong GPU và chỉ được thay thế tùy chọn khi xây dựng một tác vụ mới.

Ảnh chụp màn hình đang chạy thực tế: [Bản gốc](../../build/recomp/model-mode-check/live-1/profile-checks/original.png), [HD](../../build/recomp/model-mode-check/live-1/profile-checks/hd.png). Đầu vào cho kiểm tra liên kết sử dụng cùng đường dẫn yêu cầu như F6; phím F6 vật lý không được mô phỏng. Bạn có thể thực hiện kiểm tra lại `verify_profile_images.py RUN_DIRECTORY --start-vi 3400 --model-5600` trong lần chạy mới với `SRW64_WINDOW_CONTROL=1`, `--original-name-entry` và `intro-skip-female.json`.

`build/recomp/native-marker/acceptance.json` được kiểm tra và tạo bởi `tools/recomp/model5600/verify_native_marker.py`, đồng thời gói tài nguyên và hàm băm tệp bằng chứng được xác minh lại khi trang tài nguyên được tạo.

- **So sánh chuyển đổi tác vụ giống nhau**: `replay-original-2` và `replay-3` sử dụng cùng một chương trình và ảnh chụp nhanh tác vụ ban đầu. Sự khác biệt chỉ nằm ở phần thân của 5600, với bản đồ, các vòng chấm, hình đại diện và văn bản vẫn nhất quán.
- **Dự phòng lỗi nhận dạng**: `replay-rejected-1` chỉ thay đổi một byte siêu dữ liệu chưa được thực thi ở cuối tài nguyên, quá trình kiểm tra nhận dạng tài nguyên hoàn chỉnh không thành công; số bản vẽ gốc bằng 0 và đầu ra GPU phù hợp với phiên bản gốc.
- **Kiểm soát tắc nghẽn**: `replay-visible-control-1` Di chuyển hình dạng máy chủ phía trên hình đại diện và các giọt nước sẽ hiển thị; `replay-occluded-1` Di chuyển nó ra phía sau hình đại diện mờ đục và các giọt nước sẽ bị che khuất. Đây là một thử nghiệm trực tiếp của nhiệm vụ chụp.
- **Chạy trò chơi thực tế**: `live-1` đã chạy 16.800 VI từ SRAM trống bằng cách sử dụng đầu vào `female-to-map.json`, khoảng 280,8 giây, thoát bình thường, vượt qua lục địa Châu Âu, âm mưu Sardinia và bước vào bản đồ chiến thuật tập đầu tiên. Ghi lại 5.882 bản vẽ gốc và 26 phép biến đổi lấy mẫu; RT64 vẽ hình ảnh có độ phân giải gốc và hình ảnh phóng to tương ứng, số lượng hình vẽ không bằng số khung hình game. Trường đầu `world` của nhật ký chẩn đoán thực sự lưu trữ `world * viewProj`.
- **Kiểm tra gói tài nguyên**: Bộ sưu tập tệp hoàn chỉnh, nhận dạng tài nguyên gốc, tính nhất quán hình học của lưới nhị phân và trang web, giá trị dấu phẩy động hữu hạn, chuẩn đơn vị và phạm vi chỉ mục đều được kiểm tra trước khi khởi động. Bắt đầu từ ngày 25-09-2026, gói tài nguyên không còn chứa `reference.bin`: danh sách chỉ nhớ SHA-256 của 5600 và máy chủ lấy tài nguyên gốc từ ROM của người chơi (xem phần truy cập máy chủ của [Mô hình cắt cảnh bản đồ thế giới HD](native-ship-model.md)).

Chạy lại xác minh:

```sh
.venv/bin/python -m unittest discover -s tests -p 'test_native_marker.py'
.venv/bin/python tools/recomp/model5600/verify_native_marker.py
.venv/bin/python tools/model_viewer/build.py
```

SHA-256 của ROM gốc là `ee5f4a21d8e5f7827d21199e27800edf250df9a8e4d10befb1a6992df597b13e`. Chế độ HD mặc định của cấu hình hợp nhất cho phép hiển thị các giọt nước; các thử nghiệm mô hình độc lập ở trên vẫn dựa vào lựa chọn gói tài nguyên rõ ràng và không dựa vào chuyển đổi hình ảnh. Vẽ Plume, Metal và Vulkan (MoltenVK trên Mac) đã được xác minh và phạm vi xác minh là phần mở đầu của nữ chính và bản đồ chiến thuật của tập đầu tiên. Các tài nguyên khác, hoạt ảnh nhiều phần và tài liệu minh bạch vẫn cần được truy cập và xác minh riêng.