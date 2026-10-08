> **Ngôn ngữ / Language:** [Tiếng Việt](native-battle-ui.vi.md) · [English](native-battle-ui.en.md) · [中文](native-battle-ui.md)

# Xác nhận giao diện người dùng trước trận chiến

Ngày: 20-09-2026. Chạy hồ sơ gốc hiển thị trang xác nhận trước trận chiến SDL/RmlUi theo mặc định sau khi chọn vũ khí và mục tiêu. Sử dụng cùng một trang để chọn phản công, né tránh hoặc phòng thủ khi kẻ địch tấn công. Cảnh này là cấp độ nhỏ `battle-ui` tự tạo, không phải là nguyên mẫu web độc lập.

Để biết sơ đồ tấn công/phản công thực tế, mục tiêu thiết kế và yêu cầu chức năng, vui lòng xem [Mô tả thiết kế giao diện người dùng trước chiến tranh](battle-ui-design-brief.md).

## Trang và thao tác

Lá bài của cả hai bên được bố trí dọc theo nền xanh đậm ban đầu và đường viền góc vuông màu lục lam, đồng thời giữ lại bản đồ chiến trường. Tham khảo ảnh chụp màn hình của máy bay chiến đấu Y do người dùng cung cấp và điều chỉnh chúng cho chiều rộng, chiều cao bằng nhau, phản chiếu trái và phải; Kẻ thù ở bên trái, chúng ta ở bên phải, hình ảnh lớn của máy bay hướng vào nhau và hình đại diện của người lái xe không được phản chiếu. HP/EN còn lại có màu xanh, phần bị mất có màu đỏ, thanh tài nguyên bên phải được điền ngược lại. Hiển thị cấp độ, năng lượng, SP, trạng thái tinh thần, vũ khí và mức tiêu thụ, tỷ lệ trúng đích, tỷ lệ trúng đòn chí mạng, thiệt hại ước tính và xác suất cả hai bên cắt giảm/che chắn/nhân bản. ** Công cụ sửa đổi đòn đánh vũ khí và công cụ sửa đổi đòn đánh chí mạng được liệt kê riêng; những sửa đổi này đã được đưa vào xác suất cuối cùng. ** Khi không có vũ khí phản công, giá trị tấn công của nhóm sẽ không được hiển thị và chiều cao bố cục tương tự sẽ được giữ nguyên.

- Cuộc tấn công tích cực của chúng tôi: bắt đầu chiến đấu, chọn vũ khí, tinh thần, quay lại lựa chọn mục tiêu, chuyển đổi hoạt ảnh chiến đấu. Chọn vũ khí trực tiếp sẽ mở danh sách vũ khí tấn công ban đầu; phiên bản B ban đầu chỉ trả về mục tiêu đã chọn, do đó bộ điều hợp thực hiện tuần tự hai lối vào: trả về xác nhận ban đầu và trả về mục tiêu ban đầu.
- Tấn công kẻ thù: chọn vũ khí phản công, tinh thần, né tránh, phòng thủ, chuyển đổi hoạt ảnh chiến đấu và bắt đầu trận chiến. Sau khi chuyển đổi phản hồi, đăng lại ảnh chụp nhanh của cả hai bên, chọn vũ khí để vào danh sách vũ khí trò chơi gốc, sau đó quay lại trang mới.
- Chuột, ↑↓ hoặc nút chọn Tab, Enter/Z để thực hiện; Esc/X để quay lại khi phe ta chủ động tấn công. Chặn đầu vào trò chơi cơ bản trong khoảng thời gian theo chế độ và đợi khóa được giải phóng sau khi đóng để tránh sự xâm nhập của khóa xác nhận.
- Bản sao chép sử dụng danh mục tiếng Trung/Nhật/Anh hiện có và tên chưa dịch của máy bay, phi công và vũ khí được trả về tiếng Nhật; tên nhân vật chính năng động được mở rộng theo tên hiện có.
- "Giao diện xác nhận trước chiến tranh" của trang cài đặt ("Giao diện" của cửa sổ cài đặt) có ba cấp độ: **Phiên bản mới** (trang này), **HD gốc** (vẽ lại bằng RmlUi theo bố cục ban đầu), **Bản gốc** (màn hình trò chơi gốc, văn bản được dịch như bình thường và khung cửa sổ sử dụng hình ảnh gốc), xem [Ba giao diện](#三种界面2026-09-27). `battle_ui` (`native`/`hd`/`original`) được lưu vào `presentation.json` sẽ có hiệu lực sau lần xác nhận tiếp theo trước chiến tranh; giao diện gỡ lỗi là `settings {"battle_ui": ...}`. K/C▼ có thể được sử dụng để chuyển đổi hoạt ảnh chiến đấu (`8015DDA8 & 4`) ở cả ba bánh răng và quá trình xử lý A/B/menu ban đầu vẫn không thay đổi.
- `SRW64_NATIVE_BATTLE_UI=0` buộc toàn bộ quá trình chạy phải sử dụng giao diện xác nhận ban đầu; các mục cũ không tải profile cũng giữ nguyên giao diện gốc. Kịch bản chiến đấu cưỡng bức và các cuộc giao tranh giữa AI và AI không xuất hiện trên trang này.

## Sử dụng tinh thần trước chiến tranh

Cả tấn công và phản công đều cung cấp trang lựa chọn trong đầu cho các máy bay tham gia của chúng tôi, bao gồm các lệnh và SP độc lập mà các phi công phụ đã học. Lưới trạng thái tóm tắt tinh thần mà máy đã học và hiện đang có hiệu lực: màu xám nghĩa là không có hiệu lực, nổi bật màu cam/xanh nghĩa là bit hiệu ứng thực tế đã được bật; các lệnh khôi phục tức thời như bản chất gốc không được ngụy trang dưới dạng các phép bổ trợ liên tục.

Số lượng đã học và trình điều khiển đọc lệnh `+0x0A`, `+0x0B`, SP hiện tại/tối đa là `+0x16/+0x18` và mức tiêu thụ đọc bảng chạy ROM `80217F70`. Nếu có `801F18A0(handle,id)` gốc thì việc kiểm tra danh sách sẽ được thực hiện trên bản sao RAM và được xác minh lại sau khi chọn. SP hiệu quả, không đủ và cần sử dụng trên bản đồ sẽ được đánh dấu riêng; các lệnh yêu cầu mục tiêu bản đồ, tự hủy và hồi sinh vẫn giữ nguyên lối vào bản đồ và không tự động chỉ định đối tượng cho người dùng.

Sau khi chọn lệnh có sẵn, hãy gọi `801D6A68` ban đầu, hiệu ứng và quá trình thực hiện ban đầu sẽ chịu trách nhiệm về tinh thần, HP, sức mạnh, số lần hành động và khấu trừ SP (`801E195C`). Chỉ chặn `801C8AB4` quay trở lại bản đồ một cách bình thường trong khoảng thời gian truyền trước chiến tranh này: khôi phục menu/con trỏ/bảng chiến đấu đã lưu, gọi lại tính toán lần truy cập ban đầu và bộ đệm hiển thị trận chiến, sau đó mở trang tinh thần trước chiến tranh. Không có dữ liệu đơn vị, trình điều khiển, mục, pha hoặc RNG nào được khôi phục, do đó chi phí và hiệu ứng thực tế không được hoàn tác khi trả lại.

Esc đóng trang tinh thần và quay lại trận chiến hiện tại; sau đó Esc lại hủy bỏ cuộc tấn công chủ động ban đầu. Các lựa chọn Né tránh/Phòng thủ và vũ khí hiện tại được giữ lại trong quá trình sử dụng; không thể bỏ qua các tùy chọn không đủ SP bằng các lần nhấp nối tiếp hoặc lặp lại cũ. Nút chiến đấu nền bị tắt khi trang linh hồn được mở và D-pad và Tab chọn giữa các lệnh có sẵn và nút quay lại.

## Tầm cỡ dữ liệu

| Dự án | Nguồn và Xử lý |
| --- | --- |
| Tỷ lệ trúng | Bảng tham gia được tính toán của trò chơi ban đầu `8018B6E8 + slot*0x5C + 0x12`, giới hạn ở 0–100; bao gồm giảm một nửa sự trốn tránh và ảnh hưởng tinh thần của việc đáp ứng các hướng dẫn. Chất lượng hiển thị nhất quán với trò chơi gốc và các điểm cuối số ngẫu nhiên của nó không được diễn giải lại. |
| Hiệu chỉnh đòn tấn công của vũ khí | Bản ghi vũ khí thời gian chạy `+0x0A`, byte đã ký; Hàng bảng ROM `+4`. |
| Điều chỉnh đòn đánh chí mạng của vũ khí | Bản ghi vũ khí thời gian chạy `+0x14`, byte có chữ ký; Hàng bảng ROM `+13`. |
| Tỷ lệ trúng đòn chí mạng | Hàm thuần túy tính toán lại ngưỡng `801F47B0`. Về phía mình là chênh lệch kỹ năng + hiệu chỉnh vũ khí + sức mạnh cơ bản; kẻ thù/bên thứ ba là (chênh lệch kỹ năng + chỉnh sửa vũ khí) ÷ 4. Giới hạn dưới là 1, sau đó nhấn số nguyên ngẫu nhiên 0-99 để hiển thị số thành công: `clamp(ceil(threshold),0,100)`. 0 khi máu/linh hồn có hiệu lực. |
| Thiệt hại ước tính | Gọi `801F5628` trong bản sao ngữ cảnh/RDRAM hoàn chỉnh, chọn nhánh không quan trọng/quan trọng tương ứng; kết hợp tinh thần, hướng dẫn phòng thủ, lá chắn và cuối cùng vượt qua giới hạn cộng/trừ/sống sót của ván bài là `801F5B78`. Các số ngẫu nhiên chỉ được cố định trong các bản sao riêng biệt và không tiêu tốn RNG chiến đấu thực sự. Hiển thị sát thương khi đánh mà không có biện pháp né tránh đặc biệt, không phải mức trung bình có trọng số xác suất. |
| Cắt đứt/Khiên phòng thủ | Các kỹ năng phi công, trình độ và thiết bị máy móc đều phải được đáp ứng. Cắt cũng kiểm tra vũ khí hiện tại của đối thủ `+4 & 8`; không đoán tên vũ khí. Cơ hội là `ceil(level*100/16)` cho chính chúng ta và `ceil(level*100/32)` cho kẻ thù/bên thứ ba, giới hạn ở mức 100%. |
| Danh mục nhân bản | 50% khi khả năng tương ứng của cơ thể và sức mạnh của phi công chính ≥130; đối thủ sẽ bắn trúng mục tiêu khiến việc cắt và phân thân không thành công. Mỗi xác suất là xác suất có điều kiện khi đưa ra phán quyết bào chữa và không thể cộng lại với nhau. |
| Tinh thần và hình ảnh | Linh hồn đọc bit trạng thái phi công chính và tên sẽ được đưa vào thư mục ngôn ngữ; tư thế không trống đầu tiên của cơ thể và hình đại diện của người lái xe được nhập từ ROM cục bộ. 363 liên kết hợp lệ và 361 liên kết hình đại diện trong số 365 liên kết tư thế có kiểm tra tính nhất quán của pixel Python/C++. |

Một đòn chí mạng là **xác suất có điều kiện** sau khi trúng đòn. Ví dụ: nếu ngưỡng của kẻ thù là `21/4 = 5.25`, tất cả các số nguyên từ 0 đến 5 đều thành công và **6%** được hiển thị. Nó không thể được cắt trực tiếp đến 5%. Đòn tấn công bằng vũ khí `+20` không nhất thiết phải tăng đòn đánh cuối cùng thêm 20 điểm phần trăm vì hệ số nhân địa hình/kích thước sau đó sẽ được nhân lên.

Trang này không hiển thị các điểm đánh chí mạng hoặc kết quả đánh được cuộn sẵn, cũng như không kết hợp các biện pháp phòng thủ đặc biệt thành "xác suất thiệt hại thực tế". Số lần cải trang được hiển thị trong vùng khả năng và đòn tấn công phụ không được hiển thị riêng. Để nghiên cứu công thức, hãy xem [Tính toán chiến đấu](../gameplay/battle-formulas.md).

## Khiên tầm cỡ

`801F7204` của trận chiến thông thường hiện tại cần ít nhất 5 EN sau khi kiểm tra vũ khí tấn công `+4 & 2` ở lối vào nhánh lá chắn và giữ lại EN của vũ khí phản công đã chọn. Bốn loại khiên trong tác phẩm này đều đi qua lối vào này; tên chứa "ビーム" không có nghĩa là vũ khí có bộ bit này. Ví dụ: thuộc tính ban đầu của ベガトロンビーム (678) của cấp độ nhỏ là `0x40`, thuộc tính này sẽ không kích hoạt nhánh này.

- I Force Field 2000, Planetary Defense 2000, Beam Coating 1000, có thể tích lũy; nếu sát thương không vượt quá cường độ sẽ không có hiệu quả. Nếu vượt quá, cường độ sẽ bị trừ và giá trị tối thiểu còn lại sẽ là 10.
- Rào chắn hào quang là 3000 + phần thưởng của bảng cấp chiến binh thánh; nếu không vượt quá ngưỡng sẽ không có hiệu quả; nếu vượt quá ngưỡng, nó sẽ bị xuyên thủng hoàn toàn mà không bị trừ bớt.
- Lệnh phòng thủ (bảng tham gia `+0x10 == 2`) sẽ tăng gấp đôi sức mạnh của khiên. Đây không phải là "Địa hình 2."
- Việc vô hiệu hóa/giảm sát thương thành công tiêu tốn 5 EN; sự xâm nhập của hàng rào hào quang không tiêu tốn 5 EN này. Sau khi phản ứng khiên xảy ra, khả năng phòng thủ của khiên sẽ không còn được đánh giá, kể cả nhánh xuyên rào cản hào quang.
- Khi phòng thủ bằng khiên thành công, sát thương ≥20 sẽ được làm tròn đến số 10 gần nhất và giảm một nửa theo phiên bản gốc; sát thương do lá chắn phòng thủ của đối thủ gây ra sẽ được liệt kê riêng trên giao diện.

Phần trên bao gồm 616 bộ so sánh chức năng giải quyết ban đầu bao gồm bốn loại và kết hợp, sự hiện diện/vắng mặt của dấu tia, ranh giới EN 4/5, dự trữ EN vũ khí phản công, chỉ huy phòng thủ và ngưỡng sát thương. Phạm vi là chiến đấu thông thường trong tác phẩm này; nó thường không đề cập đến tất cả các khả năng được gọi là "khiên" trong các tác phẩm khác.

## Phương thức truy cập

`battle_page.cpp` đọc các bên tham gia trong chuỗi trò chơi và xuất bản ảnh chụp nhanh JSON; `frontend.cpp` chỉ đọc ảnh chụp nhanh, gửi các hành động ngữ nghĩa nối tiếp tới lớp thích ứng và không đọc RDRAM. Hàm ước tính ban đầu được viết trong bản xem trước sẽ không đi vào tình huống chiến đấu thực sự.

Gói `801D5064` (xác nhận chính) và `801D5294` (phản hồi của kẻ thù) vẫn ở trạng thái đầu vào ban đầu. Khi người dùng xác nhận, các tùy chọn cạnh A/B và menu gốc chỉ được cung cấp một lần cho chức năng ban đầu. Chức năng ban đầu tiếp tục chịu trách nhiệm về tính hợp pháp của vũ khí, các sự kiện trước trận chiến và quy trình chiến đấu. Công tắc hoạt ảnh tuân theo `8015DDA8 & 4` (được đặt thành tắt).

Việc chuyển đổi ngôn ngữ chỉ cập nhật tên ảnh chụp nhanh; cài đặt mở sẽ không kết hợp các quy tắc mới vào ảnh chụp nhanh chiến đấu đã được chuẩn bị sẵn. Lần tiếp theo trò chơi gốc tính toán lại trận chiến, các quy tắc hiện tại sẽ được sử dụng.

Mã nguồn:

- [`battle_page.cpp`](../../src/host/battle_page.cpp): điều chỉnh trạng thái, lệnh gọi quy trình ban đầu và quyền sở hữu đầu vào.
- [`combat_preview.hpp`](../../src/host/combat_preview.hpp), [`critical_probability.hpp`](../../src/host/critical_probability.hpp): Xem trước và xác suất chí mạng riêng biệt.
- [`frontend.cpp`](../../src/native/ui/frontend.cpp): Bố cục, thao tác và đa ngôn ngữ được chia sẻ RmlUi.
- [`battle_ui_probe.hpp`](../../src/host/battle_ui_probe.hpp): Thăm dò đang chạy tùy chọn, chỉ được thực thi khi `SRW64_BATTLE_UI_PROBE=1`; giá trị cố định số ngẫu nhiên chỉ hoạt động trên cuộc gọi sao chép riêng biệt của chuỗi này.

## Xác minh và tái tạo cấp độ nhỏ

**Lối vào hiện tại: Bản dựng gốc mới → Menu chính "Vào cấp độ nhỏ" (hoặc F8) → Cấp độ đã sẵn sàng. ** Giữ bộ điều hợp tên/ký tự gốc, tự động khởi tạo với tuyến và tên mặc định; không sử dụng `--original-name-entry`, không phát lại tập lệnh chọn ký tự cũ của VI cố định. Các trò chơi mới thông thường vẫn hiển thị trang tên và trình phát gốc.

`Session.enter_mini_stage()` Kiểm tra mục nhập bằng `status`, `ui.click` và ảnh chụp màn hình GPU. `status.mini_stage` cung cấp lý do có sẵn, đang nhập, đang hoạt động, sẵn sàng, đang chờ; sẵn sàng sử dụng lại cổng nhàn rỗi được chèn bởi tập lệnh hiện có ở ranh giới khung trò chơi: màn chơi của chúng tôi, bản đồ chiến thuật, không có quá trình sự kiện/chuyển tiếp/thất bại nào được thực hiện; `3D48` chỉ đóng đoạn hội thoại và không có nghĩa là bản đồ đã nhận được thao tác. Các cạnh xác nhận sau khi phát hành được thử lại trong quá trình hiển thị dần dần menu cho đến khi trạng thái trò chơi rời khỏi menu chính.

[`battle-ui.json`](../../config/recomp/mini-stages/battle-ui.json) Triển khai bốn đơn vị thiện chiến và ba kẻ thù lân cận. Các quy tắc ban đầu và tất cả các quy tắc được sửa đổi để kiểm tra cả hai bên, 100%/5% HP, hiệu chỉnh vũ khí -20/0/+20/+30, tổng cộng **32 nhóm**; mỗi nhóm sử dụng `801F47B0` thực để trích xuất triệt để 100 giá trị số ngẫu nhiên, tổng cộng **3.200 lần**. Giá trị được hiển thị của ước tính lần truy cập `80204254` và `801F4384` được tính toán thực tế cũng được kiểm tra trên cơ sở từng nhóm.

Quy tắc ban đầu, dữ liệu được kiểm soát về sức khỏe đầy đủ của chúng tôi:

| Chỉnh sửa vũ khí (cả hai vật phẩm đều được đặt thành giá trị này cùng lúc) | Đánh | Đòn chí mạng |
| ---: | ---: | ---: |
| −20 | 27 | 1% |
| 0 | 51 | 21% |
| +20 | 75 | 41% |
| +30 | 87 | 51% |

Thư mục bằng chứng địa phương: `build/recomp/mini-stage/battle-ui-final/`.

- `battle-ui-probe.json`: nhất quán 32/32, khu vực logic game, bàn chiến đấu, bối cảnh CPU và RNG không thay đổi và RNG của từng nhóm bản không thay đổi. Việc so sánh cho toàn bộ khối 8 MB vẫn ghi sai vì có những thay đổi bộ nhớ khác trong quá trình hiển thị đồng thời; nó không phải là bằng chứng "bộ nhớ đầy đủ không thay đổi".
- `ui-checks.json`: Đã thông qua 11 thao tác giao diện, bao gồm chuyển đổi hoạt ảnh, tính toán lại tránh né, cấm phản công, phòng thủ, quay trở lại sau khi chọn vũ khí ban đầu, ba ngôn ngữ và kích thước cửa sổ, đóng sau khi xác nhận và giao chiến tiếp theo.
- `player-ui-checks.json`: Trên trang tấn công đang hoạt động, sử dụng Esc để quay lại mục tiêu đã chọn, chỉ định lại mục tiêu và khôi phục trang, nhấn và giữ Z để xác nhận đóng; `player-confirm.png` và `player-back-to-target.png` có ảnh chụp màn hình GPU.
- `battle-zh-Hans.png`, `battle-en.png`, `battle-ja.png`: Ảnh chụp màn hình GPU thực, kiểm tra các cửa sổ logic 960×720, 800×600, 1100×760 tương ứng; không có nút hoặc đoạn văn bản nào được nhìn thấy.
- Sau khi đổi sang Wire Claw trong nhóm phản công thực tế đầu tiên, hiệu chỉnh đòn đánh của vũ khí +30, hiệu chỉnh đòn chí mạng +10, đòn cuối cùng là 100% và sát thương chí mạng là 26%. Khi chọn né, địch đánh 7→3, vũ khí phản công của ta bị tiêu diệt.

```sh
# 构建并启动当前 native UI，通过调试接口从主菜单进入并检查战前页。
SRW64_BATTLE_UI_PROBE=1 .venv/bin/python tools/recomp/debug/check_battle_ui.py

# 手动试玩同一关卡：主菜单点“进入迷你关卡”或按 F8。
scripts/Play\ SRW64\ Native.command --new-game \
  --mini-stage config/recomp/mini-stages/battle-ui.json
```

Cấp độ hiển thị linh hồn là `config/recomp/mini-stages/battle-ui-spirits.json`, hãy sử dụng `3D55` thật để niệm hồn, bao gồm cả việc cải thiện sức mạnh. Bằng chứng mục nhập gốc mới, hãy xem `build/recomp/debug/20260920T150549.479573Z/`: `direct-entry.json`, `spirit-checks.json`, `mini-menu.png`, `spirits-player.png`, mã thoát 0. `battle-ui-final` trước đó là bằng chứng lịch sử về các tương tác và công thức ban đầu và không còn được sử dụng làm mục nhập chấp nhận cho quy trình khởi động hiện tại.

Xác minh thành phần: `make recomp-native-check` (bao gồm cả việc cạn kiệt miền số nguyên quan trọng ASan/UBSan) đã đạt; `make check` 262 bài kiểm tra (11 trong số đó đã bị bỏ qua), đã vượt qua kiểm tra phụ thuộc; quá trình xây dựng máy chủ đồ họa đã được thông qua. Những bằng chứng này bao gồm quá trình chiến đấu bình thường ở cấp độ nhỏ này và không có nghĩa là sự trở lại của toàn bộ cốt truyện, tất cả vũ khí đặc biệt và các trận chiến theo kịch bản.

Bản ghi chấp nhận mục nhập menu chính hiện tại và giao diện người dùng trước chiến tranh: `build/recomp/debug/20260920T151636.072446Z/`, mã thoát 0.

- `direct-entry.json`: Trang ký tự gốc không được hiển thị và dữ liệu nhập vào bản đồ được gửi sau các cấp độ nhỏ `ready=true` và `waiting_reason=""`.
- `ui-checks.json`: 13 đường chuyền, bao gồm cả trường hình ảnh/phòng thủ của cả hai bên, điểm đánh dấu không phải tia không vô tình kích hoạt rào cản hào quang, cũng như phản đòn, hoán đổi vũ khí, ngôn ngữ/cửa sổ và giao chiến liên tục.
- `battle-ui-probe.json`: 32 nhóm tấn công/chí mạng, 24 nhóm chém/phòng thủ bằng khiên/nhân bản và 616 nhóm kiểm soát khiên đều đã vượt qua; thử nghiệm cách ly giữ cho logic trò chơi và RNG không thay đổi.
- `battle-zh-Hans.png`, `battle-en.png`, `battle-ja.png`: ảnh chụp màn hình GPU gốc hiện tại, giữ lại bản đồ chiến trường.
- `make check`: 262 đã đạt (bỏ qua 11); Kiểm tra thành phần ASan/UBSan đã được thông qua về tên, cổng sẵn sàng cấp độ nhỏ, bản xem trước trận chiến.
- nhà nhập khẩu độc lập CTest 6/6 đã vượt qua, oracle ROM thực bao gồm tất cả các pixel nội dung/hình đại diện hợp lệ. Điều này thể hiện tính nhất quán của việc nhập nội dung và không thay thế bản dùng thử đầy đủ của gói phát hành độc lập.

Chấp nhận hiện tại đối với các cuộc tấn công tinh thần và chủ động: `build/recomp/debug/20260920T151928.251713Z/`, 6 lần kiểm tra đã vượt qua, mã thoát 0. Tinh thần của cả hai bên thực sự được giải phóng, đòn đánh chắc chắn 100%, đòn chí mạng 0% khi máu nóng, nhân bản 50% sau 130 sức mạnh và Esc để quay lại lựa chọn mục tiêu, chỉ định lại mục tiêu và xác nhận bàn phím đều được thông qua; `spirits-player.png` là ảnh chụp màn hình của GPU gốc hiện tại. Có thể sao chép bằng `.venv/bin/python tools/recomp/debug/check_battle_spirits.py`.

## Chưa xác minh đầy đủ HP/EN (21-09-2026)

`battle-ui-resources.json` Sử dụng kịch bản gốc để sử dụng Must Hit/Iron Wall ngay từ đầu, cho phép cả hai bên thực sự chiến đấu và sống sót. Bên mình chọn オーラzanり tiêu tốn 10 EN; Sau khi bước vào giai đoạn của kẻ thù, trang trước trận chiến gốc tiếp theo sẽ đọc kết quả: HP của kẻ thù 3000→1941, HP của chúng ta 2800→1562, EN 80→70, giới hạn trên không thay đổi, phù hợp với mức sát thương ở vòng đầu tiên là 1059/1238 và mức tiêu thụ EN là 10 tương ứng.

Thư mục bằng chứng `build/recomp/debug/20260921T011025.169262Z/`: `resource-before.json`, `resource-bars.json` (trạng thái và kích thước bố cục thực tế của ui.tree), `resource-checks.json` (6 lượt), `resource-partial.png` (ảnh chụp màn hình GPU), mã thoát thông thường 0. Không có sửa đổi trực tiếp HP/EN hoặc đưa dữ liệu hiển thị vào.

Các giá trị số được hiển thị dưới dạng số nguyên thực tế; nhấn và giữ thanh hiện tại để làm tròn phần trăm số nguyên. HP thực tế đo được của kẻ thù là 64%, HP của chúng tôi là 55% và EN của chúng tôi là 87%. Vậy chiều dài thanh 70/80 là 87% chứ không hẳn là 87,5%; đây là giới hạn độ chính xác của thanh, không phải là giá trị tài nguyên không được cập nhật. Lần này, các màn hình ranh giới có 0 EN hoặc HP cực thấp sẽ không được đề cập.

## Hiệu ứng khả năng và sức mạnh cơ bản của cả hai bên (21-09-2026)

Một khu vực "Hiệu ứng Khả năng" có thể cuộn mới đã được thêm vào thẻ của cả hai bên, nơi đọc các kỹ năng phi công thực tế, cấp độ kỹ năng, HP hiện tại và khả năng của máy. Giá trị hiệu chỉnh là một mục công thức đã được đưa vào ước tính lần truy cập/lần truy cập quan trọng và sẽ không được áp dụng lại; Những đòn bảo vệ cuối cùng như chắc chắn, né chắc, v.v. vẫn sẽ được ưu tiên. Nếu kỹ năng tồn tại nhưng không đáp ứng các điều kiện lần này, hãy giữ lại mục nhập và giải thích lý do.

| Khả năng | Trình diễn tầm cỡ |
| --- | --- |
| Nhân loại mới/Thế giới con người nâng cao | Chỉnh sửa cấp độ kỹ năng, đánh và tránh. Tính toán ban đầu được xử lý theo cùng một nhóm dấu kỹ năng và không có sự chồng chất lặp lại. |
| Sức mạnh cơ bản | Cấp độ, liệu nó có hiệu lực hay không, hiệu chỉnh đòn đánh/tránh/chí mạng hiện tại và ngưỡng kích hoạt HP của cấp độ này. **Trò chơi này không thêm áo giáp**. Kẻ thù/bên thứ ba không tăng thêm sức mạnh cơ bản cho các đòn chí mạng; nhóm của chúng tôi cũng được nhắc nhở rằng không thể thực hiện các đòn chí mạng trong thời gian máu/linh hồn. |
| Thánh chiến binh | Điều chỉnh tránh né; cách tính đòn đánh ban đầu không bao gồm việc kêu gọi Thánh chiến binh đang tấn công thêm điểm đánh. Cấp độ cũng ảnh hưởng đến sức mạnh của rào cản hào quang. |
| Siêu năng lực | Nhấn và tránh sửa chữa. |
| Cắt đứt/Khiên phòng thủ | Cấp độ kỹ năng tương ứng, xác suất của thời điểm này và các lý do như không có trang bị, không đủ cấp độ, vũ khí không thể cắt đứt, phải ưu tiên đánh hoặc che chắn. |
| Khả năng nhân bản giống như máy | Clone, Mach Special, True Mach Special, God's Clone, Getta Phantom, Instant Phantom Foot, Super Disruptor, hiển thị tên tương ứng của chúng và xác suất/lý do không được kích hoạt. |
| Khiên | Rào chắn hào quang, trường lực I, lớp phủ chùm tia, phòng thủ hành tinh, lần lượt được liệt kê trong sức mạnh cơ bản và trạng thái hiện tại. Sức mạnh kết hợp cuối cùng, lệnh phòng thủ và mức tiêu thụ EN vẫn được xử lý bằng tính toán lá chắn ở trên. |
| Phòng thủ đặc biệt khác | Số lần giả còn lại; áo giáp sát thương cố định của một cơ thể cụ thể. Cơ thể giả không được chuyển đổi thành xác suất, cũng như không biến thiệt hại có điều kiện thành thiệt hại theo xác suất. |

Theo quy tắc sửa đổi mặc định hiện tại, sức mạnh cơ bản L4 có hiệu lực khi **HP < 40%**. 1050/3000 (35%) tương ứng với giá trị cơ bản của ROM bảng 10: đánh +5, tránh +5, đánh chí mạng đồng minh +10; chính xác 40% không có hiệu lực. HP càng thấp thì nhấn các bánh răng tiếp theo càng cao. Khi tắt tính năng hiệu chỉnh bánh răng, phiên bản gốc sẽ được nâng cao toàn bộ bằng một bánh răng; khi tính năng điều chỉnh giảm một nửa bị tắt, lần đánh/tránh sử dụng giá trị cơ bản đầy đủ và lần đánh chí mạng không thay đổi. Giao diện tuân theo các quy tắc được đặt ra khi trận chiến được mở ra.

Cơ chế này dựa trên chức năng gốc cục bộ và bảng ROM: chuỗi cuộc gọi xung quanh `801F45C4`, sức mạnh cơ bản `801E1D64`/`80217F90`, con người mới `801E1EDC`, chiến binh thần thánh `801E1F08`, siêu năng lực `801E1F10` và đòn chí mạng `801F47B0`. Chức năng trống của chiến binh/siêu năng lực thánh ban đầu vẫn giữ lại mặt nạ kỹ năng của người gọi và thực sự nhận được khả năng né tránh +32 và đánh/né tránh +64; các giá trị được tính theo bảng cấp độ sau khi bật hiệu chỉnh cấp độ. Không có sự hiểu sai nào về hàm rỗng là phép cộng bằng 0.

Đã thêm trường khả năng tạo hợp nhất [`battle_effects.hpp`](../../src/host/battle_effects.hpp). Đầu dò hoạt động cách ly bao gồm **2.400 nhóm**: 4 tổ hợp hiệu chỉnh sức mạnh cơ bản × 5 kỹ năng × 4 cấp độ × 10 giá trị ranh giới HP × 3 phe. Khi so sánh với từng kết quả của hàm gốc/quy tắc hiện tại, tất cả đều nhất quán; 32 nhóm đòn đánh/chí mạng ban đầu, 24 nhóm xác suất phòng thủ và 616 nhóm lá chắn cũng đều đã vượt qua. Logic trò chơi và RNG không bị thay đổi bởi các đầu dò; không có tuyên bố nào được đưa ra rằng bộ nhớ đầy đủ không thay đổi trong quá trình hiển thị đồng thời.

Cấp độ mới [`battle-ui-skills.json`](../../config/recomp/mini-stages/battle-ui-skills.json) sử dụng `initial_resources` rõ ràng để đặt HP/EN của đơn vị thực một lần khi bản đồ sẵn sàng lần đầu tiên, được sử dụng để tái tạo ổn định thanh nguồn và tài nguyên cơ bản. Trường này chỉ chấp nhận phe phái, vị trí triển khai và tỷ lệ phần trăm giới hạn; nó không được ghi vào bất kỳ địa chỉ nào, cũng như không sửa đổi ảnh chụp màn hình. Tập hợp các trạng thái ban đầu được kiểm soát này được ghi lại tách biệt với bằng chứng nêu trên về lượng máu mất/tiêu thụ EN trong các trận chiến thực tế.

```sh
SRW64_BATTLE_UI_PROBE=1 .venv/bin/python tools/recomp/debug/check_battle_skills.py
```

Thư mục bằng chứng gốc hiện tại: `build/recomp/debug/20260921T012634.998258Z/`, mã thoát thông thường 0. `skill-checks.json` 15 lượt, bao gồm cơ sở/siêu năng lực của cả hai bên, hạn chế về thiết bị, văn bản hiển thị và đường viền nút bằng ba ngôn ngữ, kiểm tra điểm ảnh màu đỏ GPU để tìm mất bốn thanh HP/EN và thăm dò chức năng nguyên thủy. `skill-zh-Hans.png`, `skill-en.png`, `skill-ja.png` lần lượt là các ảnh chụp màn hình cửa sổ logic 960×720, 800×600, 1100×760. Chúng đã được xem thủ công. Bản đồ chiến trường và menu xác nhận vẫn hiển thị.

Xây dựng, quy tắc và kiểm tra ASan/UBSan cấp độ nhỏ đã được thông qua; `make check` 263 mục đã vượt qua (11 mục bị bỏ qua), đã vượt qua kiểm tra phụ thuộc. Có các thử nghiệm đặc biệt để loại bỏ ranh giới cài đặt tài nguyên và chỉ khởi tạo một lần hành vi. Những xác minh này không thay thế sự trở lại của các trận chiến đặc biệt đầy đủ câu chuyện.

Tập lệnh đã lưu sẽ bắt đầu lại từ bản dựng mới và chuyển thẳng đến cấp độ nhỏ, với thư mục bằng chứng `build/recomp/debug/20260921T013311.920719Z/`: tất cả 15 mục đã được thông qua; không chỉ gắn liền với trang mở trước chiến tranh. Mã thoát 0.

## Thay vũ khí, chấp nhận bố trí gương và tinh thần tiền chiến (21-09-2026)

Thư mục bằng chứng bản dựng gốc hiện tại: `build/recomp/debug/20260921T041103.588214Z/`, nhị phân SHA-256 `e9e907b530dc90942cee1acbcc8c3b3b0b282f0314515002e5f45a3c2aeab01e`. Nhập `battle-ui-skills` trực tiếp từ menu chính; `action-checks.json` Đã vượt qua 23 mục và mã thoát cuối cùng là 0.

- Tấn công tích cực: Vũ khí 677→678, nhập danh sách vũ khí ban đầu, chỉ định lại mục tiêu, sau đó quay lại trang xác nhận gốc và thực sự tham gia chiến đấu. Cây cầu gọi lệnh hủy xác nhận ban đầu và hủy mục tiêu `801D3010`, giữ nguyên kiểm tra tính hợp pháp của vũ khí ban đầu.
- Tinh thần tấn công: đảm bảo đánh SP 83→58, đánh 100%, vô hiệu hóa phép lặp lại; gốc lớn SP 58→18, HP 1050→3000, sức mạnh cơ bản sẽ không được kích hoạt khi phục hồi; máu nóng bị vô hiệu hóa do không đủ SP.
- Tinh thần phản công: Xiang sử dụng gia tốc SP 62→52, giữ nguyên vũ khí phản công và phi công phụ SP 32 không thay đổi. Trong trận chiến tiếp theo, Wan Zhang chọn cách né tránh trước, sau đó sử dụng SP 18→3 phải né; lựa chọn né tránh và trạng thái vũ khí không phản công được giữ nguyên và tỷ lệ trúng đích của kẻ địch trở thành 0%.
- Phản công và thay đổi vũ khí: Giữ mức né tránh cần thiết và SP còn lại, chọn lại vũ khí hợp pháp và tiếp tục phản công. Vũ khí đầu tiên nằm ngoài tầm bắn và bị danh sách ban đầu từ chối chính xác; vòng kiểm tra này sẽ gửi `down,a` thông qua giao diện gỡ lỗi để chọn vũ khí thứ hai. Tập lệnh đã lưu đã chứa tùy chọn không coi xác nhận bị từ chối đầu tiên là thành công.
- Menu tinh thần Chu kỳ tập trung vào tab và trả về Esc được thông qua; lưới tinh thần không hoạt động/được đánh dấu màu xám, các thẻ có chiều rộng và chiều cao bằng nhau bằng ba ngôn ngữ và ranh giới của khu vực xác nhận đã được thông qua. `actions-zh-Hans.png`, `actions-en.png`, `actions-ja.png`, `spirits-menu.png`, `counter-flash.png`, `counter-ready.png` là ảnh chụp màn hình GPU thực tế.
- 32 bộ đòn đánh/chí mạng của đầu dò cách ly chức năng ban đầu, 24 bộ phòng thủ đặc biệt, 616 bộ lá chắn và 2.400 bộ điều chỉnh khả năng đều đã vượt qua mà không thay đổi lối chơi/RNG thực tế.

`make host recomp-native-check` (bao gồm Asan/UBSan) đã đậu; quá trình điều chỉnh tiêu điểm bàn phím cuối cùng đã được xây dựng lại và quá trình xác minh đang chạy ở trên đã được hoàn tất. `make check` 263 mục (11 mục bị bỏ qua) đã được thông qua. Mục nhập lặp lại: `SRW64_BATTLE_UI_PROBE=1 .venv/bin/python tools/recomp/debug/check_battle_actions.py`.

Phiên chấp nhận không phải phiên cuối cùng cũng được ghi lại `20260921T040904.424564Z` Sự cố cacao khi tắt máy (mã thoát -11): chẩn đoán `srw64-gfx-host-2026-09-21-121108.ips`, khối không đồng bộ với ngăn xếp tại `CocoaWindow::updateWindowAttributesInternal`, truy cập vào đối tượng không hợp lệ trong `SDL_Quit`. Đường dẫn phá hủy cửa sổ chưa được sửa đổi trong vòng này; cuối cùng, phiên chiến đấu hoàn chỉnh đã diễn ra bình thường và chúng tôi không khẳng định rằng sự cố thoát không liên tục đã được khắc phục.

## Bố cục phân vùng mở (2026-09-21)

Trang trước chiến tranh của `frontend.cpp` được sắp xếp lại theo sơ đồ 1b được lựa chọn bởi dự án "Battle Preview" của dự án Claude Design (`BattleOpen.dc.html`, canvas 1920×1080 được chuyển đổi thành dp ở mức 0,5); các trường ảnh chụp nhanh, lệnh gọi quy trình ban đầu và cỡ dữ liệu không thay đổi.

- **Ba hàng và ba cột. ** Phía trên là biểu ngữ máy bay của cả hai bên (tên đơn vị, nhãn thứ nhất/phụ, vũ khí, hình ảnh phản chiếu HP/EN, mức tiêu thụ và hiệu chỉnh vũ khí); hai bên phần giữa là hình ảnh lớn của máy bay đối diện. Khu vực va chạm trung tâm được đặt cạnh số lượng lớn "sát thương trúng đích" của cả hai bên, mũi tên di chuyển đầu tiên, cũng như đường so sánh tỷ lệ trúng đích/tỷ lệ trúng đòn chí mạng và sát thương/sát thương chí mạng trong quá trình phòng thủ lá chắn/chi tiết lá chắn; cả hai bên phía dưới là bảng điều khiển (avatar, cấp độ, sức mạnh, SP, lưới trạng thái tinh thần, cắt/lá chắn phòng thủ/nhân bản và hiệu ứng kỹ năng), và trung tâm là khu vực hoạt động. Kẻ địch có màu hồng `#ff6fa8`, đội của chúng ta có màu lục lam `#3fd0ff` và giá trị chính là vàng `#ffd75e`.
- **Mô tả thiệt hại có điều kiện gần bằng giá trị số. ** "Sát thương khi đánh" được đánh dấu ngay dưới số lớn; bên không tấn công đều hiển thị "-", và vị trí của mỗi hàng không thay đổi.
- **Đối phó với các điều khiển được phân đoạn. ** Khi kẻ địch tấn công, "Phản công | Tránh né | Phòng thủ" được hiển thị. Phản hồi hiện tại được đánh dấu và hiển thị liên tục bên dưới khu vực va chạm và trên nhãn biểu ngữ của chúng tôi. Phần "Phản công" gửi một hành động mới `counter`: chỉ khi nó hiện đang tránh/phòng thủ, nó sẽ được chuyển đổi sang danh sách vũ khí ban đầu (cùng đường dẫn với `weapon` và kiểm tra tính hợp pháp ban đầu sẽ được sử dụng). Không có hoạt động nào khi nó đã phản công.
- **Ràng buộc đầu vào (phù hợp với bảng phím trò chơi, bàn phím/bộ điều khiển là cùng một bộ). ** Phím định hướng/WASD (phím chéo/phím điều khiển bên trái) di chuyển tiêu điểm, Z/Enter (A/Start) thực hiện mục tiêu điểm, X/Esc (B) quay lại, Q (L) chọn vũ khí, tinh thần E (R), hoạt hình chiến đấu K (C▼); Tab/Shift+Tab vẫn có thể quay vòng. Các phím nóng Space/W/G/A ban đầu đã bị xóa (W, Xung đột với các phím cần điều khiển). Bàn phím sử dụng `dispatch()` của `frontend.cpp`, bộ điều khiển sử dụng `graphics.cpp` và SDL GameController mới được thêm vào sẽ ánh xạ nó tới cùng một mặt nạ phím N64 (có sẵn trong tất cả các trò chơi). Trang sử dụng `srw64_pad_state()` để chiếm cạnh tăng và cả hai được hợp nhất thành cùng một `battle_buttons()`. Đường dẫn bộ điều khiển chưa được thử nghiệm với bộ điều khiển vật lý; trang liên kết, trang tên và trang liên trường chưa được kết nối với bộ điều khiển.
- **Trang tinh thần. ** Đã thay đổi thành danh sách dòng: tên, mức tiêu thụ SP, trình điều khiển và SP, trạng thái; các lệnh hiệu quả được đánh dấu bằng màu vàng.
- **Khác biệt so với dự thảo thiết kế. ** RmlUi Không có `clip-path`/`filter`/Lưới CSS: Các cạnh vát được thay đổi thành đường viền góc phải, ánh sáng nội dung và độ mờ bản đồ bị bỏ qua và chỉ giữ lại độ chuyển màu trong mờ và chuyển màu trại trái và phải. Lưới trạng thái tinh thần giữ lại tên đầy đủ thay vì các từ đơn lẻ để đáp ứng yêu cầu của giao diện tiếng Anh và “không chỉ dựa vào cách thể hiện màu sắc”. Menu con vũ khí với ước tính từng loại vũ khí trong bản phác thảo thiết kế chưa được triển khai và vũ khí đã chọn vẫn nằm trong danh sách vũ khí trò chơi gốc. Nhãn danh mục vũ khí (Chiến đấu/Bắn súng) không có trong ảnh chụp nhanh và không được hiển thị.
- ** Di chuyển và tránh/phòng thủ các phím chuyển đổi theo hàng (2026-10-04). ** Người dùng yêu cầu có phím để chuyển trực tiếp phòng thủ/né tránh (tham khảo chiến đấu bằng máy hiện đại) và nhấn vào hàng phản công/né tránh/phòng thủ trực tiếp sẽ quay lại bắt đầu tấn công. Các phím điều hướng không còn nhấn một dòng để quay vòng mà nhấn ba để đi bộ: bắt đầu tấn công | phản công, né tránh, phòng thủ (khi kẻ địch tấn công) | thay đổi vũ khí, tinh thần, hoạt hình và quay trở lại. Quấn lên xuống, không quấn quanh, di chuyển sang trái và phải trong đường; nhấn lên để quay lại đòn tấn công bắt đầu từ bất kỳ mục nào trong dòng phản ứng, nhấn để vào dòng phản ứng và rơi vào mục hiện được chọn. Tab/Shift+Tab vẫn duyệt qua tất cả các nút theo thứ tự ban đầu và trang tinh thần vẫn ở dạng tuyến tính. C◀ (Phần dưới cùng của Bộ bài nhắc nhở rằng khi kẻ địch tấn công, sẽ có thêm một `{CLeft}` tránh/phòng thủ (mục `battle_guard_switch`, đã đăng ký `UI_KEYS`). Khi vẽ lại trang trong cùng một trận chiến (nhấn bộ điều khiển lần đầu tiên, nhắc chuyển sang biểu tượng bộ điều khiển, thay đổi ngôn ngữ, thay đổi cửa sổ), tiêu điểm vẫn ở nút gốc; vì vậy, nó sẽ được đặt lại để bắt đầu tấn công trước đó phím mũi tên đầu tiên được nhấn khi chuyển từ bàn phím sang bộ điều khiển sẽ bị mất. Nó vẫn trở về nút mặc định khi tham gia trận chiến mới, thay đổi phản hồi hoặc chuyển trang tinh thần. Phiên bản gốc có độ phân giải cao và bố cục màn hình cảm ứng vẫn không thay đổi trên trang tấn công của kẻ thù. 2026-10-04, tất cả 32 mục đã vượt qua và mã thoát của máy chủ là 0.
- **Kiểm tra kịch bản. ** `battle-card-left/right` hiện đề cập đến biểu ngữ trên cùng và `battle-pilot-left/right` được thêm vào; kiểm tra nhân bản của `check_battle_actions.py` bao gồm cả hai cùng một lúc và vị trí thanh tài nguyên của `check_battle_skills.py` được thay đổi theo thứ tự "khóa | thanh | giá trị".

- **Văn bản mô tả. ** Bốn mô tả tầm cỡ mờ (sát thương/chí mạng/phòng thủ/chỉnh sửa) ban đầu được căn giữa ở giữa đã bị xóa khỏi trang; các nhãn như "sát thương khi đánh" được dán trực tiếp bên cạnh các giá trị. Phím ngôn ngữ tương ứng không thay đổi.

- **Văn bản được sắp xếp hợp lý (sau khi người dùng xem xét). ** "Chuẩn bị chiến đấu" không còn hiển thị ở trên cùng; dòng chữ nhỏ "Ai → Ai" phía trên số lượng thiệt hại lớn sẽ bị loại bỏ; dòng chữ "Sửa vũ khí" bị xóa khỏi dòng tiêu thụ biểu ngữ; "Đòn đánh/Né tránh/Chỉnh chí mạng" trong ba ngôn ngữ được rút gọn thành "Đòn đánh/Né tránh/Chí mạng"; dòng khả năng được nén thành một dòng (chỉ ghi lý do khi nó không hiệu quả và ngưỡng HP được ghi ở phía dưới), và không còn tiêu đề "Hiệu ứng khả năng". Cut/Shield Defense/Clone chỉ hiển thị các vật phẩm mà cơ thể thực sự có (không thiếu trang bị hoặc kỹ năng), danh mục nhân bản sử dụng tên khả năng của chính cơ thể và hai hàng chiều cao cố định được để trống; ba loại này không còn được lặp lại trong danh sách khả năng. Thân giả được hiển thị là "Fake Body × N", chỉ hiển thị khi số lần còn lại lớn hơn 0.
- **Tinh chỉnh tiếp theo. ** Khối nhãn tỷ lệ trúng/tỷ lệ chí mạng được mở rộng ("クリティカル Rate" của Nhật Bản không còn đầy đủ); cột nhãn chi tiết được mở rộng ("Sát thương nếu lá chắn mục tiêu" bằng tiếng Anh không được bao bọc); hàng lá chắn chỉ hiển thị "Sát thương gốc → Thiệt hại thực tế" khi vô hiệu/giảm sát thương, không áp dụng/EN không đủ/xuyên thủng chỉ hiển thị trạng thái; vùng hiệu ứng kỹ năng được tăng lên 108dp, thanh cuộn không còn xuất hiện trên nội dung thông thường.

- **Tab Các cạnh vát và các giai đoạn (26/09/2026, sau khi người dùng xem xét). ** Giữ lại cạnh huyền theo bản phác thảo thiết kế: Thêm công cụ trang trí tùy chỉnh RmlUi `slant` ([`slant_decorator.hpp`](../../src/native/ui/slant_decorator.hpp), `decorator:slant(填充 边色 边宽 顶条 左上 右上 左下 右下)`, bốn chiều dài thụt ngang của mỗi góc, hình học thuần túy, viền ngoài của cạnh 1 px, bản thân phần tử không còn có nền và đường viền). Mặt trong của biểu ngữ, khu vực va chạm trung tâm (hình thang hẹp phía dưới), hàng tỷ lệ trúng/tỷ lệ trúng đích quan trọng (hình bình hành) và nhãn của nó (hình thang) và nút bắt đầu chiến đấu (hình thang rộng phía dưới) đều được vẽ bằng nó; bảng điều khiển được giữ vuông góc theo bản vẽ thiết kế. Tab hai khung "Tấn công của kẻ thù | Cuộc tấn công của chúng ta" của bản phác thảo thiết kế được khôi phục ở giữa trên cùng và giai đoạn hiện tại được đánh dấu theo màu trại (các mục `battle_phase_enemy`/`battle_phase_player`, `UI_KEYS` được đồng bộ hóa). Hình ảnh lớn của máy bay trước tiên được cắt alpha thành pixel thực tế (thuộc tính `rect`), sau đó được phóng to theo chiều cao còn lại giữa chiều rộng cột và bảng biểu ngữ/phi công, tối đa 6 lần; tem chụp nhanh được thêm vào kích thước cửa sổ và được sắp xếp lại sau khi thay đổi cửa sổ. Kích thước phông chữ tổng thể của khu vực thí điểm đã được tăng lên (tên 17, sức mạnh/SP 13, lưới tinh thần và dòng khả năng 12, cắt/khiên phòng thủ/nhân bản 13) và khu vực lưới tinh thần 46dp có thể chứa hai dòng. Hình đại diện của người lái xe là 96dp (ban đầu là 62dp, người dùng 2026-09-26 yêu cầu kích thước lớn hơn), có cùng chiều cao với ba dòng tên, sức mạnh/SP và tinh thần. Ảnh lớn của cơ thể được chụp từ toàn bộ tư thế HD (`docs/design/unit-pose-hd.md`) ở chế độ HD. Giới hạn phóng to trên được tính toán dựa trên pixel ROM. Hình ảnh không được lấy mẫu lại và ranh giới chỉ tính các pixel có alpha ≥ 16. Chuyển đổi phiên bản gốc/phiên bản mới ("Giao diện xác nhận trước chiến tranh" trên trang cài đặt) và công tắc hoạt ảnh K/C▼ trên giao diện gốc vẫn không thay đổi và `check_battle_ui_switch.py` 6 mục đã vượt qua.
- **Màn hình nhỏ và bảng điều khiển được để trống (28/09/2026, Steam Deck). ** Kích thước giao diện (trang "Giao diện" của cửa sổ cài đặt, Deck cực lớn theo mặc định, xem [Cửa sổ cài đặt](settings-window.md#界面大小)) Sau khi phóng to, trang chỉ có kích thước khoảng 864×540 dp. Khi chiều rộng trang nhỏ hơn 1000 dp, hãy thêm `narrow`: hình đại diện 64 dp, lề bên trong của nút trở nên nhỏ hơn, nguồn/SP không ngắt dòng, văn bản nhỏ được phóng to (nhãn đầu tiên cuối cùng 10, dòng tiêu thụ 11, mô tả và chi tiết khu vực va chạm 11, mũi tên chuyển động đầu tiên 10). Thay vào đó, lời nhắc dưới cùng sử dụng các ký hiệu phím (`{A}``{L}``{R}``{Anim}``{B}`). Bàn phím hiển thị các phím liên kết và tay cầm hiển thị biểu tượng. Bảng điều khiển ban đầu có hai hàng dành cho lưới tinh thần (46 dp), một hàng để cắt/phòng thủ lá chắn/nhân bản (18 dp) và khoảng hai hàng rưỡi cho các khả năng (44 dp), trống không có nội dung; người dùng có thể xem Bộ bài Ảnh chụp màn hình hỏi tại sao còn lại nhiều bộ bài - bây giờ giữ nguyên số lượng mà cả hai bên yêu cầu trong trận chiến này (`PilotRoom`): số lượng hàng lưới tinh thần được tính toán dựa trên nhãn ở cả hai bên, tùy theo số nào lớn hơn. Hàng cắt/lá chắn phòng thủ/nhân bản chỉ được giữ lại khi một trong hai bên **sở hữu** khả năng (liệu nó có thể áp dụng dựa trên quyền sở hữu chứ không phải vũ khí hiện tại hay không và trang thay đổi vũ khí không nhảy). Hàng khả năng dựa trên số lượng ở cả hai bên, tùy theo số nào lớn hơn; hai bên vẫn có chiều cao bằng nhau và các đường phân chia được căn chỉnh. Chiều cao còn lại ước tính (bản gốc `logical_h-436`) không còn được sử dụng cho ảnh có thân hình lớn. Sau khi sắp chữ, chiều cao thực tế của hàng giữa `battle-mid` được đo rồi thay đổi kích thước (`battle_fit_units`, giới hạn trên vẫn là 360 dp, gấp 6 lần pixel ROM). Hình dáng của máy bay trong cùng một cảnh cao hơn khoảng 60% khi boong tàu cực lớn. `check_battle_ui.py` 13 đường chuyền.

Chạy chấp nhận (cùng bản dựng, trực tiếp vào cấp độ nhỏ):

| Kịch bản | Kết quả | Thư mục Bằng chứng `build/recomp/debug/` |
| --- | --- | --- |
| `check_battle_actions.py` | 25 lượt, mã thoát 0 | `20260921T111932.966579Z` |
| `check_battle_skills.py` | 15 lượt (ba ngôn ngữ/cửa sổ, bốn pixel màu đỏ trên thanh tài nguyên, 2.400 bộ thăm dò khả năng) | `20260921T111719.596115Z` |
| `check_battle_ui.py` | 13 lượt đi | `20260921T112117.478933Z` |
| `check_battle_spirits.py` | 6 lượt, mã thoát 0 | `20260921T111816.467122Z` |

`check_battle_spirits.py` Lớp bàn phím gốc mất 100 mili giây để nhấp vào. Thỉnh thoảng mất phím xảy ra khi menu bản đồ được mở rộng (tái phát ở cả đường dẫn vào cũ và mới). Nó đã được thay đổi thành lớp xử lý giống như các tập lệnh khác `buttons` (được tính giờ bởi VI); phần phản công của `check_battle_actions.py` được phân nhánh theo người phòng thủ thực tế (việc truy cập trực tiếp sẽ thay đổi Trạng thái RNG, xem [Cấp độ nhỏ](../script/mini-stage.md)). Lần chạy `20260921T071023.404326Z` trước đó đã vượt qua tất cả các bước kiểm tra nhưng sự cố thoát khỏi Cocoa không liên tục (-11) được ghi ở trên đã xảy ra khi đóng. Sau đó, mỗi lần chạy đều thoát bình thường. `make check` không chạy vòng này.

## Ba giao diện (2026-09-27)

Người dùng 2026-09-27 đã yêu cầu giao diện xác nhận trước chiến tranh có ba cấp độ: phiên bản sửa đổi/phiên bản HD/phiên bản gốc của chúng tôi. Ý nghĩa được người dùng xác nhận: "HD" được làm lại từng cái một bằng RmlUi theo bố cục và màu sắc phù hợp của phiên bản gốc; "Bản gốc" là màn hình gốc do chính trò chơi vẽ ra, văn bản vẫn được dịch theo ngôn ngữ đọc và chỉ có hình ảnh được thay thế bằng hình ảnh gốc.

| Tập tin | `battle_ui` | Màn hình | Hoạt động |
| --- | --- | --- | --- |
| Phiên bản mới | `native` | Trang hiện đại của các phần trước trong bài viết này | Các phần trước trong bài viết này |
| Bản gốc độ nét cao | `hd` | RmlUi vẽ lại theo tọa độ 320×240 gốc, phóng to màn hình 4:3 trong cửa sổ, cách thực hiện tương tự như màn hình liên trường | Giống như ban đầu: A xuất phát, B quay lại chọn mục tiêu; khi kẻ địch tấn công, có menu gồm bốn món, B mở danh sách vũ khí. K／C▼ Cắt hoạt hình |
| Bản gốc | `original` | Màn hình trò chơi gốc; khung cửa sổ 1196/1197 sử dụng ảnh gốc, văn bản được xử lý theo chế độ ảnh gốc | Nguyên bản; cộng với hoạt hình cắt K/C▼ |

**Thiết lập và di chuyển. ** `settings::battle_ui()` đã thay đổi từ bool thành liệt kê `BattleUi {Native,HD,Original}`, [`presentation_settings.hpp`](../../src/host/presentation_settings.hpp). Ý nghĩa của `native` và `original` trong `presentation.json` cũ vẫn không thay đổi và sẽ được sử dụng trực tiếp; các giá trị không được nhận dạng được coi là `native`. Khi phiên bản cũ của chương trình ghi `hd`, nó cũng sẽ được coi là phiên bản mới. Trình khởi chạy (`launch.cpp`) phiên âm giá trị này không thay đổi. Cả giao diện gỡ lỗi và `battle_ui` của MCP đều chấp nhận `native`/`hd`/`original`. Hàng cài đặt được đặt trên trang "Giao diện" theo phương pháp phân trang của cửa sổ cài đặt. Mục nhập `settings_battle_ui_{native,hd,original,note}` hoàn chỉnh bằng ba ngôn ngữ và đã được đăng ký bằng `UI_KEYS`.

### Màn hình gốc (phân tích tĩnh)

Cơ sở là việc tháo gỡ `801D4CCC`, `801D4660`, `801E7A28`, `801D51A8`; tọa độ đều là 320×240. Màn hình gốc không có avatar, hình ảnh cơ thể, sát thương, đòn chí mạng và linh hồn.

- **Xây dựng và bước**:
- Gọi `801D4CCC(arg)` 1 lần khi vào để tạo màn hình: arg 0 là đòn tấn công của ta, arg 2 là đòn tấn công của địch, arg 1 là làm mới sau khi chọn tránh/phòng thủ.
- Cửa sổ có bố cục `0x45` (hộp 1196, thư viện 1295, bảng màu 1297, bộ truyền phát 1017), có khe sprite 0x2E.
- `801D4660` vẽ hai bảng; đối với arg 2, menu được tạo bởi `801D51A8` (bố cục `0x46`, ô 1197).
- Hàm bước `801D5064`/`801D5294` chỉ xử lý đầu vào và không vẽ gì cả.
- **Trái và Phải**: Đội ta luôn ở bên phải (bảng 0 của `801E7A28`, text x=168), còn địch ở bên trái (bảng 1, x=24).
- **Bảng**: Phần dưới cùng bên trong của bảng bên trái (21,21)–(155,139), RGBA (0,0,32,0xC0); đường màu xanh của khung bên ngoài là x=19/156, y=19/140 và đường màu tối bên trong (16,16,32); y=51/52 là đường phân chia. Bảng bên phải được dịch chuyển toàn bộ 144 sang bên phải.
- **HP／EN**:
- “HP”, “EN” và dấu gạch chéo là ký tự màu vàng và trắng trong sơ đồ khối.
- Nhóm số đi bộ (8×8, chữ màu trắng và bóng xám). HP sử dụng `%5d`, giá trị hiện tại là (53,26) và giới hạn trên là (102,26); EN sử dụng `%3d`, tại (53,39)/(86,39).
- Hiển thị `?????`/`???` khi chưa xác định được kẻ địch. Điều kiện phán đoán: Phía chúng tôi hoặc máy bay +0x38 bit 0x40 của byte 0 của phi công đã được đặt.
- Thanh máu ở (52,35), 88×2; Thanh EN tại (112,42), 28×2. Luôn vẽ toàn bộ đường màu đỏ trước, sau đó nhấn `trunc(值×宽／上限)` để xếp màu xanh lá cây; cũng rút ra khi kẻ thù không rõ.
- **Dòng văn bản** (ROM cao 14 ký tự, giãn dòng 16):

| Vị trí (bảng bên trái) | Nội dung |
| --- | --- |
| (24,56) | Tên máy bay (bản ghi 527 + số máy bay) |
| (24,72); (112,72); (137,72) | Tên trình điều khiển (4382+); "レベル" 898; Cấp độ `%2d`, không xác định là `??` |
| (24,88) | Tên vũ khí (1370+). Nếu không có vũ khí thì viết 1109 và không thể phản công được; nếu người phòng thủ chọn né/phòng thủ thì viết 927 tránh/890 phòng thủ |
| (24.104); (56,104) | 「気力」908; Sức mạnh `%3d` |
| (24.122); (72,122) | "Tỷ lệ trúng %" 1014; đánh `%3d` (bàn chiến đấu +0x12, giới hạn 0–100), không có vũ khí ghi `---` |

- **Menu tấn công kẻ thù**:
- Đế (125,149)–(195,219).
- Bốn vật phẩm là Phản công Bắt đầu 1015, Vũ khí 1016, Tránh né 927, Phòng thủ 1017, tọa lạc tại (128,152+16n).
- Con trỏ là khối màu xanh mờ có kích thước 71×17 bắt đầu từ (124,150+16·sel); tùy chọn tồn tại `80227A81`, lặp lên và xuống.
- A chọn phản công để bắt đầu trận chiến, chọn vũ khí hoặc nhấn B để mở danh sách vũ khí. Việc chọn tránh/phòng thủ sẽ được tính toán lại với vũ khí 0, sau đó được làm mới bằng `801D4CCC(1)` và con trỏ sẽ quay lại mục đầu tiên.
- **Cuộc tấn công của chúng tôi**: Chỉ có hai bảng. Giai đoạn B của chúng tôi quay lại lựa chọn mục tiêu; khi đó không phải là giai đoạn của chúng tôi hoặc là trận chiến bắt buộc, nó sẽ tự động bắt đầu sau khoảng 61 bước.

Ảnh chụp màn hình tham khảo máy thực tế (bản gốc thuần túy, 3 lần): Thanh toán chính `build/recomp/mini-stage/duel-3/present-2311.png` (cuộc tấn công của chúng tôi), `build/recomp/mini-stage/rules-battle-1/present-3540.png` (menu tấn công của kẻ thù, kẻ thù bên trái không xác định được). Ảnh chụp màn hình dưới `build/` có thể được xóa bất kỳ lúc nào.

### HD bản gốc

Mã nguồn: `battle_hd_page`/`battle_hd_buttons` của [`frontend.cpp`](../../src/native/ui/frontend.cpp), CSS là `.bh-*`.

- **Dữ liệu**:
- Thực hiện cùng một bộ ảnh chụp nhanh và hành động ([`battle_page.cpp`](../../src/host/battle_page.cpp)) trên trang mới. Lưu ý `style` của ảnh chụp nhanh ở vị trí mở.
- Thêm 3 mục nữa: `words` (các bản ghi trong bảng trên là `dialogue::ui_text` để lấy văn bản ngôn ngữ đọc có cùng nguồn gốc với lớp phủ văn bản của màn hình gốc), `known`/`level_known` của mỗi bên và phán quyết `???` ở trên.
- Màn hình gốc bị xóa `8009DB8C` (giống như trang mới) và bản đồ hiển thị như bình thường mà không bị tối.
- **Sắp chữ**:
- Tất cả các vị trí như bảng trên, tỷ lệ u=min (chiều rộng cửa sổ/320, chiều cao cửa sổ/240). Chiều rộng đường viền là một pixel gốc và rộng ít nhất một pixel màn hình.
- Văn bản được căn chỉnh sang trái tại điểm bắt đầu của lưới ban đầu và giá trị căn phải được căn chỉnh về đầu bên phải của lưới ban đầu.
- ROM kana nửa chiều rộng, phông chữ toàn chiều rộng nên dòng quá dài trước tiên sẽ được nén theo chiều ngang (70% đối với tiếng Trung và tiếng Nhật, 80% đối với tiếng Anh, giống như `ui_text.cpp`), sau đó giảm kích thước phông chữ nếu không vừa.
- “Tỷ lệ trúng %” được chia theo vị trí của hai hoặc nhiều khoảng trắng liên tiếp trong bản dịch và các con số được điền vào các khoảng trống nên trật tự từ của bản dịch không bị ảnh hưởng.
- Các giá trị trong nhóm kỹ thuật số có cỡ chữ thông thường là 10,5, với văn bản màu trắng cộng với bóng màu xám của pixel gốc.
- Vị trí của “レベル” đã được chuyển từ 112 sang 135 căn phải, chừa thêm một chút chiều rộng cho tên tài xế.
- **Thao tác** (`battle_hd_buttons`, được chia sẻ bởi bàn phím và bộ điều khiển):
- A/BẮT ĐẦU: Bắt đầu trận chiến khi đội ta tấn công; thực hiện mục ở vị trí con trỏ khi kẻ địch tấn công.
- B: Quay lại lựa chọn mục tiêu khi chúng ta tấn công (chỉ `can_cancel`); mở danh sách vũ khí khi kẻ địch tấn công, phù hợp với phiên bản gốc.
- Lên xuống (trái và phải, cũng có thể sử dụng rocker): Di chuyển con trỏ menu theo vòng tròn.
- K／C▼: Chuyển đổi hình ảnh động. Nhãn nhỏ ở phía dưới giống như trên màn hình gốc.
- Không có phím tắt để thay đổi linh hồn và vũ khí và chúng không có sẵn trên màn hình gốc.
- Các mục menu có thể được nhấp bằng chuột.
- Khi trận chiến được vẽ lại, con trỏ vẫn giữ nguyên vị trí; đối với các trận chiến mới và làm mới sau khi tránh/phòng thủ, con trỏ sẽ quay lại mục đầu tiên (điều này cũng đúng với phiên bản gốc).
- **Khác biệt so với phiên bản gốc**:
- Việc truyền dòng khung không được thực hiện và sử dụng màu cơ bản tĩnh; góc khung là một góc vuông.
- Khi không phải giai đoạn của chúng tôi, nó sẽ không tự động bắt đầu sau khoảng 61 bước. Giống như trang mới, bạn phải nhấn A.
- Chiến đấu cưỡng bức và AI so với AI vẫn có đồ họa thông thường (`step` được trả về trước khi đánh giá trang bị).

### Ảnh gốc gốc

- **Hộp cửa sổ**: `native_map.cpp` Đã thêm móc `set_original_frames` (`srw64-frame-host` không liên kết đến `battle_page` nên hãy sử dụng móc thay vì gọi trực tiếp), cài đặt `battle_page::configure`. Khi thiết bị còn nguyên bản, khung hình 1196/1197 sẽ không được vẽ lại ở chế độ HD, ngay cả khi chế độ hình ảnh là HD. Hai khung hình này chỉ được màn hình này sử dụng nên được đánh giá theo số cảnh và không cần tính thời gian.
- **Văn bản**: `battle_page::original_screen()` đúng trong vòng 3 VI của mỗi bước khung hình của màn hình xác nhận ban đầu (chiến đấu cưỡng bức cũng được tính) hoặc rút ra 1196/1197. `ui_text.cpp` Lúc này nó được xử lý theo chế độ ảnh gốc: tiếng Trung và tiếng Anh được dịch và vẽ nguyên bản như bình thường, còn tiếng Nhật là ký tự ROM gốc.
- **TÌNH TRẠNG**: `status.battle_page.original_images` phản ánh trạng thái này.
- Nếu văn bản ở khung đầu tiên được vẽ trước khung và bước thì có thể có 1 khung văn bản tiếng Nhật có độ phân giải cao chưa được xác nhận trên máy thực tế.

### Xác minh

[`check_battle_ui_switch.py`](../../tools/recomp/debug/check_battle_ui_switch.py) đã được mở rộng thành ba cấp độ:
- Phiên bản gốc: không có trang gốc, `original_images` là đúng, C▼ cắt hoạt ảnh và khôi phục sau khi thoát;
- Phiên bản mới: Hoạt hình cắt C▼;
- Bản gốc độ nét cao: C▼ cắt hoạt ảnh, B quay lại, A bắt đầu chiến đấu; sau khi hiệp đấu kết thúc, kẻ địch tấn công, kiểm tra con trỏ menu ban đầu đang bắt đầu phản công, đi xuống ba lần để phòng thủ, chọn phòng thủ và sau đó bảng điều khiển làm mới (`response`=2, vũ khí −1) và con trỏ quay trở lại mục đầu tiên, B mở bảng vũ khí, chọn vũ khí và quay lại trang gốc có độ phân giải cao;
- Kiểm tra tính bền vững của cài đặt cho từng thiết bị.

Ảnh chụp màn hình được lưu trữ trong thư mục đang chạy: `original-confirm.png`, `native-confirm.png`, `hd-confirm.png`, `hd-menu.png`, `hd-defend.png`, `hd-counter.png`.

**Chưa chạy trên máy thật** (phải mất vài phút để chạy máy chủ gốc và nó sẽ cạnh tranh với các phiên khác để xây dựng). Bây giờ chỉ kiểm tra biên dịch `-fsyntax-only` được thực hiện trên các tệp đã thay đổi trong cấu hình bản dựng thanh toán chính.