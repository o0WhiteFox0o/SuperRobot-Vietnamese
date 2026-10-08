> **Ngôn ngữ / Language:** [Tiếng Việt](mini-stage.vi.md) · [English](mini-stage.en.md) · [中文](mini-stage.md)

# Cấp độ nhỏ: cấp độ tự tạo với tư cách là người vận chuyển xác minh hướng dẫn

Cập nhật: 2026-09-16. Mục đích là sử dụng cấp độ nhỏ tự viết (mở đầu, đối thoại, chiến trường, sự kiện chiến trường, kết thúc) để xác minh các hướng dẫn kịch bản còn lại trong quá trình trò chơi thực. Trang này ghi lại phiên bản đầu tiên: người chủ thay thế hình ảnh cấp độ đã biên dịch bằng công cụ gốc, nhấn F8 từ menu chính tiêu đề và đi theo đường dẫn "Trò chơi mới → Lựa chọn nhân vật chính → Tên → Mở" ban đầu để vào.

## Cách bắt đầu chương gốc

- Lớp phủ bản đồ thế giới `load_000A7EC0:801C2B9C` hoặc đường dẫn đọc (ba vị trí trong `800801A4`) tính toán chỉ số cảnh `8010F5F0` và gọi cư dân `8009DD58(场景, 加载模式)`.
- `8009DD58` → `8009DBE4(场景)` DMA khối bản ghi xuất kích của cảnh này (≤ 0x2000 byte) đến `80199400`; `8009DC58(栈表, 场景)` DMA các sự kiện của cảnh này (≤ 0x1A00 byte) thành `8019B400` và ghi bảng con trỏ sự kiện vào `8009DD58` Bộ đệm ngăn xếp (0x100 byte, kết thúc bằng −1).
- `8009DE7C(模式, 引擎, 指针表, 出击记录块)` xóa 12 nhóm × 16 vị trí, đăng ký 0–11 theo loại từ thứ 0 của tiêu đề sự kiện, lưu loại 12–14 trong `engine+8/+C/+10` và lưu con trỏ khối bản ghi sắp xếp trong `engine+0` (`3D45` quét 14 nửa từ từ đây).
- Lớp phủ chiến thuật `load_000AB160:80209D6C` sử dụng `8010F5F0` tra cứu bảng `802195B0` để lấy chỉ mục bản đồ và ghi vào `8010F5EE`.

Do đó, việc thay thế chỉ yêu cầu thay thế bảng con trỏ và nội dung của hai bộ đệm tại mục `8009DE7C` và viết lại chỉ mục bản đồ sau `80209D6C`. ROM, dữ liệu thư mục và các cảnh khác không được di chuyển.

## Định nghĩa và biên dịch cấp độ

`config/recomp/mini-stages/*.json` (lược đồ `srw64.mini-stage.v1`):

- `map`: chỉ mục bản đồ (`base:map_assets`); `slot`: chỉ mục cảnh thay thế cố định, tùy chọn; theo mặc định, nó sẽ thay thế tập đầu tiên được đăng ký sau khi máy chủ được bật.
- `events`: danh sách sự kiện, mỗi mục là `type` (0–14), `header` (bốn tham số, xem [Loại đăng ký sự kiện](stage-script-exploration.md#事件登记类型与触发条件) để biết ý nghĩa) và `commands` (phương pháp viết hướng dẫn tương tự như [Gỡ lỗi chèn tập lệnh](script-debug-injection.md)). Bạn cũng có thể viết `copy_from` (`base:stage_events:*`) để sao chép một sự kiện gốc theo luồng lệnh cho đến ký tự kết thúc; đồng thời, khi đưa ra `header`, chỉ có bốn tham số kích hoạt được thay thế và các byte lệnh không thay đổi. Điều này được sử dụng để kích hoạt các điều kiện kích hoạt (vòng muộn, số lượng khoảng trống) không thể đạt được bằng hoạt động giới hạn.
- `deployments_from`: Sao chép toàn bộ khối bản ghi xuất kích ban đầu (`base:stage_auxiliary:*`, tối đa 999); `deployments`: Bản ghi 28 byte bổ sung, tên trường `group/x/y/actor/level_offset/unit/upgrade/faction/behavior/extra`, sử dụng byte không được giải thích `byte8/raw14/raw16/raw18/raw26`, có sẵn `template` Chỉ định bản ghi gốc (`base:stage_deployments:*`) làm tấm cơ sở.

`tools/recomp/script_lab/mini_stage.py compile 关卡.json --out 镜像.json` tạo `srw64.mini-stage-image.v1`: các sự kiện được ghép theo căn chỉnh 4 byte (con trỏ = `8019B400` + offset) và `03E7 0000` được thêm vào cuối khối bản ghi sắp xếp; hơn 63 sự kiện, sự kiện 0x1A00 byte hoặc bản ghi 0x2000 byte bị từ chối.

## Phía chủ nhà

- Công tắc `SRW64_MINI_STAGE=<镜像路径>`; `src/host/mini_stage.hpp`, được gọi bằng hai trình bao bọc của `game_hooks.cpp`: `resident_func_8009DE7C` (thay thế trước rồi gọi hàm ban đầu) và `load_000AB160_func_80209D6C` (hàm ban đầu sau đó được ghi đè `8010F5EE`). Cả hai móc đều được liên kết thông qua `NATIVE_HOOKS` của `generate_cpu.py` và yêu cầu `make recomp-cpu` được tạo lại.
- Đọc hình ảnh và xác minh (lược đồ, độ dài, căn chỉnh, số lượng sự kiện) trong quá trình khởi động; hình ảnh không hợp lệ sẽ trực tiếp khiến máy chủ bị lỗi.
- Tệp sự kiện `mini-stage-events.jsonl` (lược đồ `srw64.mini-stage-event.v1`): `loaded / applied / skipped / map`, `applied` ghi lại chỉ mục cảnh, chế độ tải, địa chỉ bảng con trỏ và địa chỉ khối bản ghi xuất kích ban đầu.
- `run_host_probe.py` yêu cầu hồ sơ phiên bản tiếng Nhật và `--graphics`; hoạt động giới hạn yêu cầu `SRW64_SCRIPT_TRACE=1` và hoạt động giới hạn với `--audio` phải sử dụng `SRW64_AUDIO_CAPTURE_FROM/_TO` để cung cấp cửa sổ thu thập; `--interactive` không phải tuân theo hai hạn chế này. Viết báo cáo `mini_stage`.
- `mini_stage.py report 运行目录 --image 镜像.json` liên kết việc kiểm tra tập lệnh của PC với từng sự kiện: có kích hoạt hay không, VI đầu tiên và cuối cùng, điểm bắt đầu/kết thúc của mỗi lệnh VI và khung lấy mẫu cũng như các lệnh chưa được thực hiện.

## Mục menu chính

- Dùng thử tương tác: `play_native.py --profile … --mini-stage config/recomp/mini-stages/flow.json` Biên dịch hình ảnh và đưa đường dẫn đến máy chủ; thêm "F8: mini stage <name>" vào tiêu đề cửa sổ. Nhấn **F8** trong menu chính của tiêu đề (mở lớp phủ trạng thái 3, nghĩa là "ニューゲーム／コンティニュー..." menu): Người chủ trì nhấn BẮT ĐẦU để chọn trò chơi mới cho người chơi và tự động yêu cầu bỏ qua gốc khi chuỗi văn bản mở đầu xuất hiện (tương đương với R+Start), việc lựa chọn nhân vật chính và trang tên được người chơi vận hành như bình thường; khi đăng ký tập đầu tiên, nó được thay thế bằng cấp độ nhỏ, được ghi `armed / skip-requested / entered`. Nhấn F8 khi không có trong menu chính chỉ ghi `hotkey-ignored`. Mã menu gốc và các mục menu không thay đổi.
- Xác minh giới hạn: `SRW64_MINI_STAGE_ARM_VI=<vi>` cho phép máy chủ tự động được trang bị vũ khí ngay khi đến menu chính sau VI này. Việc nhập tập lệnh chỉ cần BẮT ĐẦU hai lần để đến menu chính, sau đó cung cấp các nút để chọn và tên nhân vật chính (`entry-input.json`).
- Kiểm tra đơn vị `tests/native_mini_stage.cpp` (`make recomp-mini-stage-test`, được sáp nhập vào `recomp-native-check`): xác minh hình ảnh, thay thế đăng ký, móc bản đồ chỉ hoạt động trên các cảnh liên kết, phím nóng chỉ được trang bị trong menu chính, START duy trì bốn cuộc thăm dò, số lần bỏ qua phần mở đầu và bản ghi mục nhập.

## Mức độ khói `smoke.json`

Lấy tập đầu tiên (mục lục cảnh 1 "Departure! スイームルグ") làm cơ sở: cùng một bản đồ (20), một bản sao hoàn chỉnh về hồ sơ tấn công của nó (20 mục, 5 nhóm), sự kiện mở đầu được cắt thành 6 dòng hội thoại và tất cả các lệnh cấu trúc (BGM, bản đồ thế giới `3D32`, tăng dần và giảm dần, `3D4D` Chuyển đổi chiến trường, `3D65`, ba nhóm `3D45` xuất hiện, `3D35` cuộn), thêm sự kiện "Vòng đầu tiên bắt đầu giai đoạn của chúng ta" không có trong câu chuyện gốc (loại 0), giữ lại quân tiếp viện (loại 7, kẻ thù 6), chiến thắng (loại 7, kẻ thù = 0 → `3D4A`), thất bại (loại 2, Malina bị đánh bại → `3D4C`) và sự kiện kết thúc (nhập 14 → `3D4B 4`).

Nhập script `smoke-input.json`: khởi động nguội bỏ qua đoạn mở đầu chung, tên siêu mặc định nữ, bỏ qua đoạn mở đầu lộ trình, sau đó nhấn A cứ sau 120 VI.

## Kết quả chạy

### khói-1 (`build/recomp/mini-stage/smoke-1`, 14.400 VI, im lặng)

- Máy chủ áp dụng hình ảnh (`mini-stage-events.jsonl`: `applied`) trong chỉ mục cảnh VI 3137 1, chế độ tải 0 và bảng con trỏ nằm trong bộ đệm ngăn xếp của `8009DD58`; sau VI 4669 `80209D6C` thì chỉ số bản đồ được viết là 20 (giống như các từ gốc, dùng để chứng minh hook có tác dụng).
- Tất cả 27 lệnh trong sự kiện khai mạc đều được thực thi theo thứ tự (`mini-stage-report.json`): `3D32 4` được hoàn thành ngay lập tức, `3D32 0` 114 VI (định vị bản đồ thế giới), nút chờ hội thoại, `3D4D` Cuộc bỏ phiếu này hoàn tất nhưng cuộc bỏ phiếu tiếp theo `3D65` được bắt đầu sau 612 VI (Chuyển đổi lớp phủ, tải bản đồ và màn hình tiêu đề), ba nhóm gồm `3D45` mỗi 422/292/312 VI, `3D35` đều được hoàn thành ngay lập tức. Khung lấy mẫu: Điểm nổi bật trên bản đồ thế giới (`stage-0-3D32-end_vi-3293.png`), chiến trường trống sau khi chuyển đổi (`stage-0-3D65-end_vi-5245.png`), ba nhóm đơn vị địch và quân bạn sau khi xuất hiện (`stage-0-3D45-end_vi-6881.png`).
- Sự kiện đối thoại chỉ hiện 6 số văn bản trong gương (17410, 17411, 17436, 17460, 17461, 17464) và không xuất hiện những dòng có chữ gốc bị cắt đi.
- Sự kiện cấu hình ban đầu loại 13 không được kích hoạt: tập mới được thực thi bởi chính sự kiện mở đầu `3D45`, loại 13 chỉ được sử dụng trong đường dẫn C2, nhất quán với tập gốc.
- Sự kiện "Turn ≥ 1, Our Phase" loại 0 không kích hoạt: số vòng quay động cơ `+0x9AC` là 0 ở lượt 1 (phù hợp với ảnh chụp nhanh quá trình chạy tiêm), do đó, tham số lượt của sự kiện lượt 1 phải được ghi bằng 0. `flow.json` đã được sửa như vậy.
- Loại số lượng kẻ thù, loại tiêu diệt và sự kiện kết thúc không được kích hoạt (không có trận chiến trong vòng này), `commands_not_executed` liệt kê tất cả các lệnh của chúng.

### flow-1 (`build/recomp/mini-stage/flow-1`, 16.000 VI, tắt tiếng)

`flow.json` chỉ thay đổi sự kiện vòng đầu tiên thành "Hai dòng hội thoại, chờ 30, `3D4A`" và ghi 0 cho tham số vòng. Kết quả là toàn bộ quá trình lên cấp được hoàn thành tự động mà không cần phải đấu tranh:

- 27 lệnh mở đầu giống như smoke-1; ở vòng đầu tiên, sự kiện giai đoạn của chúng tôi được kích hoạt tại VI 7349 (2 VI sau khi kết thúc phần mở đầu), `3D3E` 114 VI, `3D3F` 478 VI (nút chờ), `3D48`, `3D38 30` 60 VI, `3D4A` 20 VI.
- 38 VI sau `3D4A`, gõ 14 sự kiện kết thúc cháy: `3D3A`, `3D32 1`, `3D33 2` (340 VI, chuyển động của tàu vũ trụ trên bản đồ thế giới, `stage-6-3D33-end_vi-8447.png`), `3D3B`, đối thoại, `3D47`, `3D4B 4`, tất cả 8 lệnh được thực thi.
- Sau đó vào quy trình thông quan ban đầu: Ảnh chụp màn hình GPU của VI 15973 `present-7980.png` là màn hình lưu trữ, hiển thị "Tập 1...スイームルグ クリア総ターン Number 1 Funds 0" và "Ghi lạiをCập nhậtします.よろしいですか?". Tập tiếp theo (cảnh 4) vẫn chưa được đăng ký trong giới hạn VI của vòng này nên chưa có bản ghi `skipped`.
- Các sự kiện tăng cường, chiến thắng (địch = 0) và thất bại không được kích hoạt: không có trận chiến nào trong vòng này và không có thay đổi về số lượng quân địch.

## Cấp độ xác minh lệnh

Mục 3, "Xác minh từng hướng dẫn còn lại ở cấp độ nhỏ" đã bắt đầu. Hai cấp độ phân chia công việc theo lớp phủ mà lệnh yêu cầu và tất cả các tham số đều được lấy từ phiên bản tập lệnh gốc; Sau mỗi đầu dò là một thời gian chờ `3D38` để khung lấy mẫu và ảnh chụp nhanh trạng thái có thể được quy cho một lệnh duy nhất.

### Ảnh chụp nhanh trạng thái lệnh từng cái một

Chuyển `SRW64_MINI_STAGE_CAPTURE=1` (cũng yêu cầu `SRW64_STATE_PROBE=1`). `poll_hook` của `mini_stage.hpp` được gọi bằng trình bao bọc kiểm tra tập lệnh của `game_hooks.cpp`: khi tập lệnh PC nằm trong khối sự kiện được thay thế và khác với lần trước, nó sẽ lưu ảnh chụp nhanh vùng `state-N-mini-stage-command.json`, `argument` là phần bù của PC so với khối sự kiện và ghi lại sự kiện `capture`. 0 VI đã hoàn thiện và không có sự so sánh trước và sau đối với hướng dẫn ghi trường mà không có thay đổi màn hình. Máy chủ chỉ đọc từ PC và không ghi lại bất cứ điều gì.

### `worldmap.json` — Lớp phủ bản đồ thế giới

Sự kiện khai mạc diễn ra trước `3D4D` và là bối cảnh duy nhất có thể tiếp cận được của lớp phủ bản đồ thế giới `load_000A7EC0`; phán đoán nhàn rỗi do kịch bản đưa vào cần có bản đồ chiến thuật và không thể đến được đây. Xem [kết quả chạy worldmap-1](#worldmap-1buildrecompmini-stageworldmap-119000-vi静音).

### `tactical.json` — lớp phủ bản đồ chiến thuật

Tất cả các cuộc thăm dò được đặt sau `3D4D` và `3D45` trong sự kiện khai mạc. Ở vòng đầu tiên, `tactical-1` đã đặt đầu dò vào sự kiện "Turn 1 Our Phase", nhưng nó không được kích hoạt trong cả vòng: sự kiện này yêu cầu người chơi phải hoàn thành một vòng, nhưng tập lệnh nhập giới hạn chỉ nhấn A và thao tác luôn dừng ở giao diện chọn đơn vị. Sự kiện khai mạc không yêu cầu người chơi thăng tiến và là vị trí đáng tin cậy duy nhất trong các hoạt động giới hạn.

`3D49` bị bỏ lại một mình trong `duel.json`: nó bắt đầu một trận chiến theo kịch bản có thể tiêu tốn toàn bộ ngân sách VI. Kết quả thực tế được hiển thị dưới đây.

## Kết quả chạy (xác minh lệnh)

### worldmap-1 (`build/recomp/mini-stage/worldmap-1`, 19.000 VI, im lặng)

- `3D32` là **Định vị bản đồ thế giới**: điểm đánh dấu luôn ở giữa màn hình và toàn bộ bản đồ sẽ di chuyển đến vị trí của mục trong bảng `801C5310`; khi nửa từ thứ 0 của mục trong bảng khác thì toàn bộ bề mặt của vùng đất được thay thế (Mục 2 Biển Địa Trung Hải, Mục 19 Bờ biển, Mục 46 Núi Tuyết, Mục 63 Sa mạc). Ngoại trừ cuộc gọi đầu tiên tại vị trí này (0 VI), 106 VI được cố định mỗi lần, bất kể khoảng cách và là các chuyển mạch có độ dài cố định.
- `3D31` (tập lệnh gốc không có phiên bản) chia sẻ `800A0E64` với `3D32`: `3D31 4` có cùng màn hình với đường cơ sở `3D32 4` và giống 106 VI.
- `3D33` là **chuyển động của bản đồ thế giới**: vẽ một đường màu xanh và trắng di chuyển từ vị trí hiện tại đến mục tiêu, `3D33 2` và `3D33 69` lần lượt là 316/566 VI, **thay đổi theo khoảng cách**. Đây chính xác là sự phân công lao động với `3D32`: `3D32` thay đổi địa điểm và `3D33` thực hiện quá trình di chuyển.
- `3D5E` 0 VI hoàn thành ngay lập tức mà không có thay đổi nào đối với khu vực thăm dò.
- `3D68` tại đây **không bao giờ hoàn thành**, sự kiện dừng ở thanh này: `80212780`/`80212898` của nó nằm trong lớp phủ chiến thuật `load_000AB160`, VRAM dưới bản đồ thế giới không phải là hai chức năng này và máy trạng thái chờ không bao giờ tiến bộ. Đã xóa khỏi cấp độ này và đổi thành `tactical.json` để xác minh (87 VI hoàn thành bình thường). Đây là lỗi của thiết kế cấp độ, không phải lỗi của trò chơi.

Bảng `801C5310` có tổng cộng 127 mục (0-126), mỗi mục có ba nửa từ có dấu `(地表, x, y)` và giá trị bề mặt là 13/14/17/18/19/20; cấu trúc thay đổi từ mục 127 trở đi và bảng kết thúc tại đây.

### chiến thuật-3 (`build/recomp/mini-stage/tactical-3`, 19.000 VI, tắt tiếng, chụp từng ảnh một)

Tất cả 56 lệnh trong chuỗi mở đầu đã được thực thi; 96 ảnh chụp nhanh từng bước. Tất cả 12 bản ghi xuất kích tự tạo đều xuất hiện trên bản đồ.

| Lệnh | Thông số | Cách sử dụng | Quan sát |
| --- | --- | ---: | --- |
| `3D50` | 95,118,117 / 238,49,48 | 66/66 VI | **Biến dạng đơn vị**: Con trỏ đơn vị vị trí danh sách di chuyển về phía trước một bản ghi (0x54), tọa độ lưới không thay đổi, số phiên bản đơn vị +2 là 118 → 117, 49 → 48, HP 4300/3800 không thay đổi |
| `3D58` | 31,1 | 0 VI | **Chuyển trại**: Đã xóa ô 0/9, cùng tọa độ (8,14) xuất hiện ở 1/1, số cạnh 11/1 → 10/2, trường hợp phi công và máy đã được xóa và xây dựng lại |
| `3D58` | 59,0 | 0 VI | ロザミア đã ở slot 0/10 (mặt 0), ghi mặt hiện tại → Không thay đổi: **idempotent** |
| `3D5C` | 145,1 | 18 VI | Đã kết hợp → Không thay đổi danh sách |
| `3D5C` | 145,0 | 48VI | **Tách**: Danh sách của chúng tôi có 10 → 14 vị trí, con trỏ nội dung 0/6 của vị trí ban đầu đã thay đổi, bốn vị trí mới xuất hiện trong lưới liền kề (9,12)/(8,13)/(7,12)/(8,11), tức là コン・バトラーV được chia thành năm máy |
| `3D6E` | 179 | 0 VI | **Đơn vị thoát**: Đã xóa khe 0/4, phi công +0x130 1 → 65, thân +0x2F8 17 → 58 |
| `3D55` | 4,30 / 31,9 | 424／68 VI | Cái trước di chuyển camera đến thiết bị và chọn nó (khung màu trắng); cái sau làm cho thiết bị hiển thị hiệu ứng đặc biệt như kim cương phát sáng. Tham số thứ hai được hiển thị trong bảng `80217D20` Chọn hiệu suất sẽ được thêm vào thiết bị, không chỉ camera chuyển động |
| `3D36` | 5/6 | 22/18 | Chuyển đổi khung nhìn với viền đen, không có thay đổi về danh sách và phiên bản; hai giá trị xuất hiện theo cặp (kịch bản gốc 85/76 lần) |
| `3D63` | 145 | 22 VI | Chỉ thay đổi danh sách 1 byte |
| `3D75` | 179/999 | 188/188 VI | Thời gian tiêu thụ hoàn toàn giống nhau và không có thay đổi trạng thái: 999 đi theo cùng một đường dẫn với nhân vật thực tế, đó là hiệu suất thuần túy |
| `3D67` | 1/4 | 654/896 VI | Hai màn biểu diễn dài nhất, không có sự thay đổi trạng thái; chạy im lặng không thể kiểm tra chuyển mạch BGM |
| `3D68` | — | 87VI | Hoàn thành bình thường trên bản đồ chiến thuật, không thay đổi trạng thái |
| `3D6B` | 165,216,0 / ,1 | 0 VI | Cờ 0 không có thay đổi; cờ 1 được đặt thành trình điều khiển +0 bit 7 và +0x0C của phiên bản nội dung 0/1/2 được đặt thành 0x40 |
| `3D69` | 4,1 / 4,0 | 0 VI | `4,1` Không thay đổi (ドモン nằm ở vị trí 0/8, hai trường đã giống nhau dưới giá trị này, idempotent); `4,0` đặt danh sách +0xAB bit 7 và thay đổi +0x35** của **bản ghi trình điều khiển 12** thành 1 Đã xóa thành 0, đây là trường được dự đoán bởi phân tích tĩnh |
| `3D70` | 181.183 | 0 VI | ショウ đã được triển khai (khe 0/3), nhưng ký tự 183 チャム ​​không xuất hiện trong tất cả 6.223 bản ghi xuất kích ban đầu** và không bao giờ xuất hiện dưới dạng đơn vị bản đồ; ủng hộ hướng "có vai trò không liên quan" (đồng phi công/đối tác), không có bằng chứng trực tiếp vòng này |
| `3D6F` | 53/874 | 0 VI | Không có bản ghi bộ phận nào có số khớp ở cấp độ này → Không hoạt động |

`3D32`／`3D31`／`3D33`／`3D50`／`3D58`／`3D5C`／`3D6E` đã được thăng cấp thành `code-confirmed` và được đổi tên. Cùng với `3D49`/`3D6F`/`3D70` tiếp theo, các hướng dẫn thông thường thay đổi từ 33 mục `code-confirmed`, 19 mục `unknown` thành **43 mục `code-confirmed`, 22 mục `structure-confirmed`, 8 mục `unknown`**.

### Duel-2 → Duel-3: `3D49` yêu cầu nhân vật phải có mặt và không cần vào trận

`3D49 15,16` trong cuộc đấu tay đôi-2 Máy chủ gặp sự cố ngay khi bắt đầu (`native-run-failed`, mã thoát −10). Báo cáo sự cố hệ thống cung cấp vị trí chính xác: luồng lỗi dừng ở `load_000AB160_func_80211BD0`, được gọi bởi `80211DA4` (chức năng xử lý `3D49`), `EXC_BAD_ACCESS / SIGBUS`, địa chỉ `0x708000002F`.

Việc đọc `80211BD0` cho biết lý do: nó lấy con trỏ phiên bản máy bay của vị trí danh sách (địa chỉ cơ sở `8015E10C`, bước bên `0x258`, bước vị trí `0x14`, trường `+0x0C`), sau đó nhấn `+0x2C` Số lượng/`+0x30` con trỏ, bước `0x24` Traverse danh sách các đơn vị mà không cần xác minh con trỏ. Duel-2 sử dụng khối bản ghi xuất kích ban đầu.レイン và アレンビー có tên trong bảng `800C9A18` mục 15/16 không có trong danh sách và nó bị treo sau khi đọc con trỏ chưa được khởi tạo.

**Kết luận: `3D49` Hai nhân vật cần xuất hiện trên danh sách bản đồ và không cần tham gia quá trình chiến đấu trước. ** đấu tay đôi-3 Sau khi triển khai hai nhóm gồm bốn ký tự, hai `3D49` được hoàn thành bình thường với 1572/972 VI tương ứng và `exit 0`.

### đấu tay đôi-3 (`build/recomp/mini-stage/duel-3`): `3D49` là một trận chiến có kịch bản

Một trận chiến hoàn chỉnh xuất hiện trên màn hình: thanh HP/EN của cả hai bên, hình đại diện người lái, lời thoại và hoạt ảnh tấn công - レイン 「いくわよっ!!」→ アレンビー 「ぎゃあああああっ!!」. Nhóm thứ hai là ドモン vs. ゾンビ兵. Kết quả sẽ được ghi lại: trạng thái của ô danh sách `0/1` của một bên trong mục 16 thay đổi từ 1 thành 2 (không thành công/không thể di chuyển) và HP của phiên bản máy bay `+0x58/+0x59` của nó được đặt lại từ 8000 về 0, phù hợp với màn hình `0/8000`; phi công `+0x35` của một bên trong mục 3 đã bị xóa.

Nửa từ thứ 4 của mục không phải là màn hình HP (màn hình 8000/5000, bảng 32760/10) và ý nghĩa của nó vẫn chưa được xác nhận. `3D49` đã được nâng cấp lên `code-confirmed` và được đổi tên thành "Hiệu suất chiến đấu theo kịch bản (Mục danh sách chiến đấu A, Mục danh sách chiến đấu B)".

### target-1 (`build/recomp/mini-stage/targets-1`): Thêm đối tượng hành động vào thao tác không

Cùng một dòng suy nghĩ ("Không thao tác = thiếu đồ vật") thúc đẩy ba dòng suy nghĩ khác. Các cấp độ [`targets.json`](../../config/recomp/mini-stages/targets.json) có mục tiêu dành riêng cho chúng.

- **`3D6F`** đã được nâng cấp lên `code-confirmed`. Thay vào đó, hãy sử dụng các tham số tập lệnh gốc thực sự tồn tại và đã được đặt trong bảng phần của cấp độ này (19/773/775, được chọn ra bởi ảnh chụp nhanh `part_instances` của chiến thuật-3; 53/874 được sử dụng trước đó hoàn toàn không có trong bảng): `3D6F 773`/`3D6F 775`. Ghi lại `+0x22` ngày 31/32 của `0x0C` được đổi thành `0x08`, xóa bit 2, hoàn toàn nhất quán với phân tích tĩnh `800ACF44`. Nội dung trùng khớp là số lượng bản ghi `+2` chứ không phải chỉ mục.
- **`3D70`** đã được nâng cấp lên `code-confirmed` và được đổi tên thành "Vai trò Người đồng hành được gắn kết". Trong 10 phiên bản của tập lệnh gốc, tất cả đều tuân theo `3D5A`, trong khi ký tự đồng hành khách (183 チャム/182 シルキー) không xuất hiện trong tất cả 6.223 bản ghi xuất kích và được đăng ký với `3D5A` với nội dung 999. Theo phương pháp viết này, trước tiên `3D5A 183,0,999,500` tạo bản ghi trình điều khiển 7 và sau đó `3D70 181,183`: bản ghi `+0x37` được đặt thành 1, `+0x38` được ghi vào con trỏ phiên bản nội dung; đồng thời **ビルバイン do ショウ`+0x34` điều khiển thay đổi từ 1 thành 2, `+0x3C` ghi địa chỉ hồ sơ lái xe 7** - tức là `+0x34` là số lượng hành khách, và `+0x38` là mảng con trỏ tài xế (phù hợp với cơ sở `3D55`).
- **`3D69`** vẫn là `unknown`, nhưng phạm vi tác dụng đã được xác nhận: ở cấp độ mà Leopard Horse tấn công, `3D69 145,0` ghi ** tài xế 1–5 là `+0x35` Xóa tất cả**, tức là tất cả các phi công phụ của đơn vị do nhân vật điều khiển (năm người từコン・バトラーV), không một bản ghi nào. Tất cả những gì còn thiếu là tên trò chơi trong hai trường này.

## Kích hoạt hoạt động âm thanh (audio-1 / audio-2)

Ngữ nghĩa của `3D67` có thể nghe được nhưng không vô hình, do đó, yêu cầu về sự im lặng của cấp độ nhỏ được nới lỏng: chạy giới hạn vẫn yêu cầu bật dấu vết tập lệnh nhưng có thể thêm `--audio` và `SRW64_AUDIO_CAPTURE_FROM/_TO` phải được sử dụng để chỉ định cửa sổ VI cho bộ sưu tập. Bộ sưu tập gốc được cố định giữ lại 30 giây đầu tiên sau khi bật âm thanh và lệnh nghe thường xuất hiện sau khi chạy được vài phút; logic cửa sổ vẽ `Srw64AudioCaptureWindow` của `audio_timing.hpp`, được ghi đè bởi `tests/native_audio_queue.cpp` (bỏ qua trước cửa sổ, ghi vào cửa sổ, đóng một lần khi vượt qua ranh giới và không ghi nữa sau đó, và `to <= from` Cửa sổ xuống cấp được coi là "không có cửa sổ" để tránh gõ nhầm ranh giới và khiến toàn bộ quá trình thu thập bị mất).

Cấp [`audio.json`](../../config/recomp/mini-stages/audio.json) Kẹp từng đầu dò vào giữa `3D3A 0` (dừng BGM), sử dụng `3D3A 49` ở đầu làm đối chứng dương; [`audio-tail.json`](../../config/recomp/mini-stages/audio-tail.json) chỉ cần nâng cao một số thăm dò cuối cùng để chúng rơi vào cùng một cửa sổ.

### `3D67` là màn trình diễn cut-in đầu tay (được thăng cấp lên `code-confirmed`)

Bốn giá trị tập lệnh gốc đều được phát âm thanh, RMS 2301–3092, giá trị cao nhất 15.000–18.000, trong khi đoạn im lặng liền kề chỉ là RMS 84–139 và to hơn BGM điều khiển (RMS 1328). Hình ảnh mang lại ý nghĩa chính xác: một vật thể xuất hiện ở giữa màn hình đi qua cùng một nền đường hầm tốc độ ánh sáng - 0 là mô hình màu xanh lam và đỏ, 1 là xám và đỏ, 3 là xanh lục, 4 là cam và đỏ, **khác**.

Phổ của 1/3/4 rất giống với đường bao (cosine 0,96–0,99, tương quan đường bao 0,93–0,99, do nền đường hầm dùng chung), nhưng mức tương quan mức mẫu chỉ **+0,007** và không thể tìm thấy sự dịch chuyển căn chỉnh, đó là âm thanh khác nhau đối với các máy bay khác nhau; thời lượng 10,87/13,93/14,93 giây. 0 có phổ khác biệt đáng kể (cosine 0,42–0,46 so với ba phổ còn lại), không có khúc dạo đầu 0,75 giây và thời lượng 16,03 giây.

Điều này hoàn toàn phù hợp với hai cách viết duy nhất trong chữ viết gốc: `3D4E → 3D67 n → 3D38 → 3D45 <组>` (trước khi quân tiếp viện xuất hiện) và `3D54 145 → 3D35 → 3D67 0 → 3D5C 145,1` (trước khi tích hợp).

### Bốn cái còn lại: ba được xác nhận là im lặng và một có hiệu ứng âm thanh.

| Lệnh | RMS (trong cửa sổ) | Kết luận |
| --- | ---: | --- |
| Điều khiển nhạc nền `3D3A 49` | 1328 | Kiểm soát tích cực, chứng minh việc thu thập có hiệu quả |
| Đoạn im lặng | 3.0 | Sàn tiếng ồn kỹ thuật số im lặng |
| `3D75 145` | 3.0 | **Hoàn toàn im lặng**, không có trạng thái, không có thay đổi rõ ràng |
| `3D68` | 3.0 | **Hoàn toàn im lặng** |
| `3D36 5+6` | 3.0 | **Hoàn toàn im lặng** |
| `3D63 145` | 48 (đỉnh 541) | **Với hiệu ứng âm thanh**, cao hơn đáng kể so với mức tiếng ồn nhưng thấp hơn nhiều so với BGM |

`3D68` đã được hoàn thiện bằng cách so sánh từng khung hình và nâng cấp lên `code-confirmed`: trước khi thực hiện, màn hình bị lệch, có viền đen và con trỏ dừng ở đơn vị địch ở xa; sau khi thực hiện, màn hình được căn giữa về đơn vị đã chọn, xuất hiện hộp chọn màu trắng và viền đen biến mất - **Camera kéo về đơn vị đã chọn**.

`3D63` được đặt thành hoạt ảnh đơn vị ngắn có hiệu ứng âm thanh: `+1` byte của vùng phân công `0/0` là 2 → 5 → 1 trong lệnh và là trạng thái của hoạt ảnh đang thực thi chứ không phải là cờ liên tục.

`3D75` Thời gian chạy ba vòng luôn là 188 VI, không có trạng thái nào được ghi, không có âm thanh được tạo ra và không thể nhìn thấy thay đổi màn hình nào ở cấp độ này, nó vẫn là `unknown` - nó có thể yêu cầu một trạng thái đơn vị cụ thể để xuất hiện. (Sau này chốt lại: tàu mẹ cần có thiết bị chở, xem phần "`3D75`: Giải phóng thiết bị chở khỏi tàu mẹ".)

## Ngược lại từ điểm gọi ban đầu (stage_script.py)

Vòng hiệu quả nhất không phải là dựng cảnh mà là đọc và sử dụng kịch bản gốc. `tools/recomp/script_lab/stage_script.py` có hai lệnh phụ: `show <场景>` in tất cả các sự kiện của một tập theo thứ tự đọc (các lệnh, tham số, văn bản hội thoại và người phát biểu đã được phân tích cú pháp), `usage <操作码>` liệt kê trong đó lệnh được gọi trong tất cả 1.812 sự kiện với ba ngữ cảnh trước và sau. Việc sao chép theo điểm gọi thực tế đáng tin cậy hơn nhiều so với các thông số tự tạo - đây là cách hoàn thiện năm mục sau đây.

### `3D5E` = Mở giao diện nhập tên đơn vị

3 hình thức gọi trong kịch bản gốc hoàn toàn giống nhau: マナミ nói "マーチウィンド? うーん, もう小し比の名がいいわね", アムロHỏi "なら,君はどんな久名がいいんだい?", rồi `3D5E`. Sau khi sao chép theo cách này, khung lấy mẫu trực tiếp đưa ra câu trả lời - màn hình là "Tên đơn vị là してください", cột tên đơn vị được điền sẵn tên mặc định và bên dưới là bảng nhập kana và "Quyết định". Sự kiện này bị tạm dừng ở đây để chờ người chơi nhập liệu. Hoạt động bị giới hạn không có đầu vào và sẽ không bao giờ tiếp tục. (Ghi chú ban đầu ở đây được điền sẵn là "アーチウィンド"; vào ngày 27-09-2026, theo mẫu tên mặc định `801C6F54` và id danh sách chọn từ `801C6F64` của ROM, đã được sửa thànhマーチウィンド. Để biết toàn bộ quá trình, hãy xem [Đã sửa Tên đội](../native/fixed-unit-name.md): Trang này không còn mở trên máy chủ trò chơi nữa, `3D5E` không làm gì cả, cấp độ kiểm tra `config/recomp/mini-stages/unit-name.json`).

**Đồng thời, một kết luận cũ được sửa lại**: Kỷ lục trước đó "`3D68` sẽ không bao giờ hoàn thành theo bản đồ thế giới" là không đúng sự thật. Sự kiện mở đầu của worldmap-1 thực sự dừng lại ở `3D5E` trước đó (giao diện được đặt tên bị treo) và `3D68` hoàn toàn không được thực thi.

### `3D69` = Đặt trạng thái hành động của đơn vị

Điểm gọi đầu tiên đưa ra hướng đi: giá trị 0 xuất hiện trong cảnh Báo Ngựa bị khống chế (ngay sau dòng "うぅ...しまった...体が..." và kẻ địch "とどめを, さしておやり!!") và NPC được di chuyển đến vị trí và ổn định bằng cách sử dụng `3D3C`; giá trị 1 Xuất hiện sau khi ヒイロ sắp kích hoạt linh hồn của anh ấy và kiệt tác của anh ấy thoát ra.

Ống kính được khóa trên thiết bị và đo từng pixel để đưa ra kết luận cuối cùng: độ sáng của vùng 12×12 nơi đặt sprite là **97,12 → (giá trị 0) 91,23 → (giá trị 1) 97,12**, mỗi trạng thái kéo dài trong 12 khung hình liên tiếp tối thiểu = tối đa (không có nhiễu hoạt ảnh ở chế độ chờ) và độ sáng toàn khung hình gần như không thay đổi - sự thay đổi được giới hạn ở đơn vị sprite, tức là hiệu suất làm tối của "đã diễn" đơn vị trong trò chơi này. Đồng thời, danh sách `+0x0B` được đặt ở vị trí 7 và người lái xe `+0x35` bị xóa, điều này ảnh hưởng đến tất cả những người đồng lái xe trong đơn vị.

### `3D36` = Rung màn hình

Hoàn tất lấy mẫu theo từng khung hình: `mean_delta` nhảy từ 0 đến 23,65 trong khi thực hiện lệnh và không đổi, trong khi `mean_rgb` luân phiên từng khung hình trong khoảng từ 56,53 đến 50,37 (54,23 khi ở trạng thái nghỉ, tức là lắc lư ở hai bên của bit còn lại). Sự chênh lệch giữa các khung không đổi được kết hợp với sự xen kẽ của hai giá trị, có nghĩa là hình ảnh chuyển động qua lại giữa hai vị trí theo từng khung hình. Hầu như tất cả 196 vị trí trong kịch bản gốc đều là "`3D39` hiệu ứng âm thanh → `3D36 n` → dòng bất ngờ của nhân vật". Các tham số xác định thời lượng: 5 → 18 VI, 6 → 22 VI, cả hai đều chiếm 161 lần.

### `3D6B` = Chọn công tắc đánh dấu

Sao chép theo điểm gọi ban đầu (sự kiện 001AB86C: `3D6B 124,171,0` ngay sau `3D5A 124,0,174,171`, リョウ được chuyển từ ゲッター1 sang ゲッタードラゴン). Ảnh chụp nhanh đưa ra sự phân công lao động từng cái một: Sau khi thực hiện `3D6B`, số máy bay trong danh sách ** không thay đổi ** và việc chuyển giao hoàn tất trước `3D5A` tiếp theo; tương tự, sau `3D6B 165,216,1`, Wan Zhang vẫn có tên trong danh sách và chính `3D46` tiếp theo đã khiến anh ấy biến mất.

Người tiêu dùng hoàn thành tham chiếu chéo tĩnh: `resident_func_800AD990` - chức năng tương tự được gọi bởi `3D73` "Nhóm theo danh sách vai trò cố định" - duyệt qua đầu tiên và xóa bit 7 (`andi 0x7F`) và bit 6 (`andi 0xBF`) của trình điều khiển `+0`, sau đó đặt các mục nhập có số trùng khớp trong danh sách 7(`ori 0x80`). Cặp này là cờ "đã chọn/đăng ký": `3D73` cho toàn bộ lô, `3D6B` cho các kết hợp riêng lẻ được đặt hoặc xóa.

### Loại trừ

`3D69` không phải là sự kết hợp và tách biệt: cùng một nhân vật và cùng một cảnh quay được thực hiện quay lưng lại, `3D69 145,0` Số lượng khe phía trước và phía sau của chúng tôi không thay đổi (2 → 2) và `3D5C 145,0` tiếp theo cho phép bốn đơn vị riêng biệt xuất hiện xung quanh thân chính (2 → 6). Đó cũng không phải là một sự thay đổi nội dung: sau năm cuộc gọi đến Aアルベルト/シュバルツ (cả hai đều có các mục nội dung khác được đặt theo tên của họ), không một số nội dung nào trong danh sách thay đổi.

## Cải thiện hiệu quả thử nghiệm

Hai khoản chi phí trước đây chiếm giữ ở mỗi vòng: trải qua quá trình xác lập quyền sở hữu và chạy qua toàn bộ ngân sách VI.

### Nhập không có tiêu đề F8 (`--save-from` không đọc file)

Không cần nhấn F8 ở tiêu đề để bỏ qua phần mở đầu. Chạy với `--save-from` và tập lệnh đầu vào, cấp độ nhỏ vẫn sẽ được thay thế khi đăng ký cảnh lần đầu tiên:

```sh
SRW64_MINI_STAGE=<镜像> SRW64_SCRIPT_TRACE=1 \
  .venv/bin/python tools/recomp/run/run_host_probe.py --graphics --profile config/recomp/profiles/play-profile.json \
  --language ja --images original --resolution-scale 2 --original-name-entry --input <输入脚本> \
  --save-from build/recomp/save-recovery-check/intermission-cold-1.source.sram \
  --save-sha256 0c6ded15fdf60c6b0064b2260a335d17a4ff77386d14d634bfd7d3bcb8de7484 \
  --output <运行目录> --vis 19000
```

Việc này không yêu cầu `SRW64_MINI_STAGE_ARM_VI` và `armed`/`skip-requested`/`entered` sẽ không xuất hiện trong tệp sự kiện. Ưu điểm chỉ là bỏ qua tiêu đề F8 và phần mở đầu:

- Đường dẫn này **không đọc kho lưu trữ** (Đã sửa vào ngày 18-09-2026; trước đó tôi nghĩ nó sẽ đọc kho lưu trữ và bỏ qua việc đặt tên), `--save-from` chỉ sao chép SRAM vào thư mục đang chạy. Nút tiêu đề của `dense-input.json` là ニューゲーム và nút thay thế là **Cảnh 1** (nếu bạn thực sự đọc tập đầu tiên thì tập tiếp theo sẽ là Cảnh 4) và ảnh chụp nhanh trạng thái `intermission-restored`/`tactical-restored` sẽ không xuất hiện trong quá trình hoạt động.
- Thao tác vẫn sẽ đi qua trang tên. Các tập lệnh hiện có như `dense-input.json` dựa vào khóa của đĩa kana gốc để truyền nó, vì vậy phải thêm `--original-name-entry`. Nếu không thêm thời gian để trang tên hiện đại tiếp quản dữ liệu đầu vào, quá trình thực thi sẽ luôn dừng trên lớp phủ tên (`001090A0`) và cảnh sẽ không được đăng ký (đây là trường hợp của quy tắc-2).
- **Dữ liệu liên tục trong kho lưu trữ (số lần tiêu diệt, cờ, quỹ, thành phần) là các giá trị ban đầu của trò chơi mới trong lần chạy này**: Trò chơi mới sẽ gọi `800A4F94` và các lần khởi tạo khác, `wufei-dummy-original-1` giống như thế này và kho lưu trữ sao lưu đã sửa đổi sẽ hoàn toàn không có hiệu lực. Khi cần lưu trữ nội dung, bạn cần sử dụng tập lệnh đầu vào thực sự đi tới menu Tải (chẳng hạn như đường dẫn của `config/recomp/inputs/load-intermission-check.json`) hoặc tự tạo trạng thái bắt buộc ở cấp độ như `wufei-dummy.json`.

### Thoát sau khi lệnh được kích hoạt

`SRW64_MINI_STAGE_EXIT_AFTER=<操作码>` (hex) Thực thi `SRW64_MINI_STAGE_EXIT_GRACE` VI (mặc định là 300) sau khi đạt được mã opcode này. Thời gian gia hạn là để cho phép các hiệu ứng của lệnh và các khung tiếp theo vẫn được ghi lại.

Đo lường thực tế: xác minh mức độ cảnh78 lần lượt `3D75`/`3D46`, ban đầu chạy tới 19.000 VI, đổi thành `EXIT_AFTER=3D46 EXIT_GRACE=400` và kết thúc ở **7.416 VI** (tệp sự kiện ghi `exit-armed` trong VI 7016, `exit` năm 7416), chạy ít hơn 61%. Báo cáo được tạo như bình thường, ngoại trừ các hướng dẫn chưa được thực hiện tiếp theo sẽ được liệt kê trung thực trong `commands_not_executed`.

Việc thoát quan sát và chụp ảnh nhanh từng cái một không phụ thuộc vào việc loại bỏ trùng lặp: người quan sát sử dụng `exit_seen` để tự khóa và không chia sẻ ranh giới bộ sưu tập để loại bỏ trùng lặp - nếu không, việc mở bộ sưu tập giữa chừng sẽ làm mất ranh giới mà người quan sát đã vượt qua. Các bài kiểm tra đơn vị bao gồm điều này, cũng như "chỉ thoát trên opcode đã chỉ định" và "chỉ kích hoạt một lần".

### Thêm đầu dò vào khối động cơ

Đầu dò trạng thái ban đầu bao gồm các khu vực như danh sách, phi công, khung máy bay, bộ phận, v.v. nhưng khối động cơ không nằm trong số đó - nó nằm ngay trong khoảng trống giữa danh sách (đến `0x8015E808`) và phiên bản khung máy bay (từ `0x8016A210`). Vì vậy, lệnh chỉ ghi trường động cơ không có dấu vết trong tất cả các ảnh chụp nhanh và có vẻ như không làm gì cả.

Sau khi thêm `script_engine` (`0x8015F950`, 0xA00 byte), `3D66` ngay lập tức xuất hiện: `3D66 1` thay đổi `engine+0x997` từ `0x1F` thành `0x9F` (đặt bit 7), `3D66 0` đổi lại thành `0x1F`, hoàn toàn đối xứng và nhất quán với mô tả tĩnh. Có 6 byte khác thay đổi cùng lúc nhưng hai chuyển đổi này hoàn toàn giống nhau. Đó là sổ sách kế toán bỏ phiếu được kích hoạt bởi mọi lệnh của động cơ.

Sử dụng biểu đồ chênh lệch khu vực ở phía màn hình để xác minh: chênh lệch giữa "tắt → bật" và nhóm điều khiển "tắt → tắt lại" là 2,8/3,1 (cùng một dải chéo, là nhiễu hoạt ảnh ở chế độ chờ), tức là bản thân công tắc không thay đổi màn hình. Người sử dụng bit này vẫn chưa được xác nhận nên nó vẫn còn `structure-confirmed`.

Điểm mù này cũng có nghĩa là tất cả các kết luận trước đó về "không thay đổi trong toàn bộ khu vực thăm dò" đều không hợp lệ đối với lệnh **chỉ ghi trường động cơ**, vì vậy nó đã được đọc lại.

#### Phân biệt tác dụng ghi sổ và chỉ dẫn

Có một phần trong khối động cơ (khoảng `+0x966`–`+0x97B`) đó là trạng thái hoạt động của chính máy ảo script. Hầu hết mọi lệnh sẽ thay đổi: `+0x967` đã thay đổi 100%, `+0x96D` 74% và `+0x97A/+0x97B` trong số 90 chuyển đổi trong cảnh78t-3. 51%. Loại trừ "byte có tỷ lệ xuất hiện trên 20%" làm sổ sách kế toán và phần còn lại là hiệu ứng hướng dẫn. Tiêu chí này có xác thực chéo: `+0x997` (bit 7 của `3D66`) chỉ thay đổi 5 lần trong cùng một vòng, chính xác là vị trí `3D66` có trong cảnh; `+0x9B0` chỉ thay đổi 4 lần, tức là số đơn vị `3D46` giảm dần - vừa hiếm vừa cụ thể.

#### Kết quả thi lại

- `3D75` (scene78t-3, bối cảnh thực): Khối động cơ chỉ di chuyển `+0x96D` (74% sổ sách kế toán) trong suốt khoảng thời gian. **Sau khi bao quát tất cả các lĩnh vực, vẫn không có phần viết độc quyền**, và kết quả của sáu vòng đầu tiên đã được xác lập.
- `3D63` (scene80-2, bối cảnh thực): Ghi độc quyền duy nhất vẫn là vị trí bảng phân công `+0x001` (2 → 5 → 1), không thay đổi khối động cơ. Tác dụng phụ của động cơ ẩn được loại trừ.
- `3D69 145,0` sau đây trong cùng một vòng được viết lại phù hợp với màn 1, có thể được sử dụng để xác thực chéo.

## Cấu trúc được xác nhận → Mã được xác nhận (2026-09-17)

Kiểm tra bổ sung từng hướng dẫn của `structure-confirmed`. Phương pháp này vẫn giống như trước: trước tiên hãy sử dụng `stage_script.py usage` để đọc điểm gọi ban đầu, sau đó sao chép nó theo trình tự ban đầu. Sử dụng ảnh chụp nhanh từng cái một, lấy mẫu từng khung hình và đọc mã tĩnh để xác nhận lẫn nhau. Tất cả 21 bài viết đã được hoàn thiện:

| Chỉ thị | Hiệu ứng | Bằng chứng quyết định |
| --- | --- | --- |
| `3D65` | Đặt điều kiện thắng/thua | Hai trường 7 bit là số văn bản (0x15BF+cao, 0x15D9+thấp), 17 = "Sự hủy diệt hoàn toàn của kẻ thù", 31 = "Máy của nhân vật chính bị phá hủy"; đọc 17/31 khi chạy |
| `3D72` | Đặt xe du lịch bản đồ thế giới | `engine+0x990` = tham số mod 15 và bảng `D_801C5644` có đúng 15 mục; giá trị bảng là chỉ số dưới của bảng mô hình bản đồ thế giới `801C5670` (14 →ラー・カイラム, xem [Mô hình cắt cảnh bản đồ thế giới HD](../native/native-ship-model.md)), không phải số ký tự |
| `3D73` | Phân đội: Chọn theo danh sách mặc định | 3D73 1 Chỉ chọn Wan Zhang và Hura trong danh sách A, không chọn Kura - phù hợp với dòng "Kara sẽ ở lại" |
| `3D74` | Xóa tất cả các dấu lựa chọn đội | Xóa dấu vết của bốn người trong cả hai vụ hành quyết |
| `3D37` | Bản đồ lớp phủ hiệu ứng đặc biệt | Ảnh chụp màn hình: Vụ nổ lớn số 0, 1 tia lửa bom, 11 vầng sáng khiên xanh |
| `3D4F` | Đơn vị bị tiêu diệt | HP 7800→0, trạng thái danh sách 1→2, đơn vị vẫn còn trong danh sách; so với 3D46 thì xóa toàn bộ dòng |
| `3D60` | Quân đội của chúng ta đang hình thành | Bốn đơn vị rải rác tập hợp thành đội hình so le ở (5,5), địch đứng yên |
| `3D56` | Khu vực mục tiêu màu xanh lá cây nổi bật | Ảnh chụp màn hình: Hình chữ nhật màu xanh lá cây nhấp nháy, có chữ "グリーンエリア" trong trạng thái chiến thắng |
| `3D35` | Cuộn ống kính (vị trí, cờ chờ) | Từ đầu tiên là cờ chờ, không phải tốc độ; tương ứng với 3 khung hình trên/dưới/trái mỗi khung hình |
| `3D5A` | Đội hình (năm chế độ) | 500 đăng ký, <2000 chuyển nhượng, 2000 xóa tài xế, 4000 xóa cùng nhau; 3000 đều là các cuộc gọi không hợp lệ trong tập lệnh gốc |
| `3D4D` | Chuyển từ bản đồ thế giới sang chiến trường | `engine+4` thay đổi từ 0xC1 thành 0x03 và sau đó khoảng 612 VI chuyển sang lớp phủ |
| `3D64` | Loại bỏ đồng tài xế | 500.500 Trường hợp đặc biệt: Liên kết アイシャ với マナミ's スイームルグS, thay thế ローレンス |
| `3D5D` | Đặt hình dạng của robot kết hợp | Ký tự đầu tiên chọn gia đình (ダンクーガ／コン・バトラーV), ký tự thứ 0 chọn hợp nhất hoặc tách biệt, cả hai loại trừ lẫn nhau |
| `3D6A` | ゴッドマーズ Xử lý kết hợp | Chế độ 3 xóa ガイヤー, đổi tên thành ゴッドマーズ; hoạt ảnh kết hợp sẽ chỉ phát khi ガイヤー HP < 11 |
| `3D51` | Khởi động vũ khí MAP | Tên ban đầu "Di chuyển đến tọa độ" sai: từ thứ hai đều là vũ khí MAP (バスターライフルMAP, v.v.); ảnh chụp màn hình cho thấy việc phóng quả cầu năng lượng |
| `3D3C` | Đơn vị di chuyển đến vị trí | Đo bổ sung vị trí tương đối: Bên phải 2, Bên dưới 2 và cùng một vị trí đều chính xác |
| `3D71` | Bước vào đoạn kết | Ảnh chụp màn hình là văn bản kết thúc; phải bị xử tử trên bản đồ thế giới |
| `3D61` | Tạm dừng nhận định “tất cả các đơn vị của chúng ta đều bị tiêu diệt hoặc bị đánh bại” | Chỉ so sánh tham số: khi giá trị bằng 0, GAME OVER sẽ xuất hiện sau khi đơn vị đồng minh duy nhất bị đánh bại, khi giá trị bằng 1, sự kiện sẽ được thực hiện như bình thường và sẽ vào lượt của chúng ta |
| `3D66` | Không tự động di chuyển camera đến loa trong khi hội thoại | Sự khác biệt duy nhất là so sánh thông số: khi giá trị bằng 0, camera sẽ chuyển sang hai loa trước hai dòng hội thoại và khi giá trị bằng 1, camera sẽ dừng ở vị trí cũ |
| `3D3D` | Xuất kích (0 đơn vị chọn mẹ/200 tự động/phần còn lại mở giao diện chọn xuất kích) | Ba cấp độ xác minh: giao diện, chọn tàu mẹ, xuất kích tự động đều xuất hiện theo thông số, đơn vị rơi gần nhóm căn cứ |
| `3D59` | Không được phép tấn công (danh sách loại trừ) | Chỉ so sánh tham số: ai bị loại sẽ biến mất khỏi danh sách tấn công |

Hai điểm xứng đáng được giải thích riêng biệt:

- **`3D5A` Chế độ 3000 là cuộc gọi đến bản gốc không hợp lệ**. Hàm điều phối bỏ qua hai cuộc gọi loại bỏ khi vai trò là 999. Tuy nhiên, tất cả năm cuộc gọi 3000 trong tập lệnh gốc đều được gọi với vai trò 999. Danh sách vẫn hoàn toàn không thay đổi trước và sau phép đo thực tế.
- **`3D56` không được vẽ trong lần đầu tiên** vì vị trí của hình chữ nhật phụ thuộc vào ống kính; theo tập lệnh gốc, trước tiên hãy sử dụng `3D35` để cuộn ống kính vào vị trí và sau đó ống kính sẽ được hiển thị. **Khi xác minh hướng dẫn thực hiện, phải sao chép cài đặt ống kính trước đó. **
- Tên ban đầu của **`3D51` sai**. Lớp cấu trúc chỉ thấy là "tìm slot bản đồ của nhân vật + cơ thể và điều khiển chuyển động", nhưng khi kiểm tra giá trị của từ thứ hai trong bảng vũ khí thì tất cả đều là vũ khí MAP.
- **`3D71` Lớp phủ đặt sai vị trí sẽ khiến máy chủ hủy bỏ**. `801C51B4` mà nó gọi chỉ tồn tại trong lớp phủ bản đồ thế giới và việc tra cứu chức năng không thành công (xác nhận `get_function`) khi được thực thi trên bản đồ chiến thuật. Đây là tình huống tương tự như `3D68` trước đó: lệnh được kiểm tra trong lớp phủ chứa lệnh đó.

### `3D61`: Tìm đầu đọc và so sánh chỉ với một tham số khác nhau

Nội dung viết đã được xác nhận (`engine+0x996` bit 15), tất cả những gì còn thiếu là ai đọc nó. Đang tìm kiếm `0x2E6(`/`0x996(` trong C được biên dịch lại, chỉ có bốn điểm đọc: `800A3524` cho điều kiện thắng và thua (mặt nạ `0x7F7F` loại trừ bit 15 và bit 7), trình kích hoạt vùng `800A4288` (bộ 15), hiển thị gỡ lỗi `80208D80` và `801FF934` cho lớp phủ chiến thuật:

```c
// load_000AB160_func_801FF934(kind, unit)
if (kind == 0) {                       // 全灭判定
    if (unit_count[side 0] /*0x80172EDC*/ != 0) return 0;
    return (engine[0x996] & 0x8000) == 0;   // 位 15 置位时不算全灭
}
/* kind != 0：逐台「须保护的机体」被击破判定，与位 15 无关 */
```

`801D5898`/`801D90C4` được gọi khi `801FF934(0)` đúng: BGM bị dừng và trạng thái chiến thuật `0x80172EB0` được đặt thành `0x54`, đây là quá trình đánh bại. Dựa vào đó, allost-0/allost-1 đã xong: đội ta chỉ triển khai アレンビー, レイン của địch, điều kiện bại trận được đặt thành "Tiêu diệt toàn bộ Ajika", `3D61 x` rồi dùng kịch bản chiến đấu `3D49 15,16` để アレンビーBị đánh bại, sự khác biệt giữa hai cấp độ chỉ là x.

| 3D61 | Số lượng đơn vị của chúng tôi | Trạng thái chiến thuật | Màn hình | Khai mạc thực hiện |
| --- | --- | --- | --- | --- |
| 0 | 1 → 0 | `0x05` → `0x54` | Ánh chớp trắng, luồng sao, "GAME OVER", rồi rời khỏi cấp độ | 9 trên 11, sau đó bị gián đoạn bởi quá trình thất bại |
| 1 | 1 → 0 | Giữ `0x05` | Sau khi sự kiện được thực hiện, hãy vào lượt của chúng tôi (menu ("フェイズEnd") | Tất cả 11 mặt hàng |

Vì vậy `3D61 1` đang "đình chỉ phán quyết tiêu diệt toàn bộ đội của chúng tôi". 7 cách sử dụng của kịch bản gốc đều đúng: Cảnh 32 sử dụng 1/0 để trình bày trận chiến theo kịch bản giữa kẻ thù; Cảnh 78 được đặt ở phần mở đầu trước khi phe ta tấn công, và được xóa ở cuối phần mở đầu; Cảnh 11 (phía chúng ta không có đơn vị nào trong phần mở đầu) được đặt trong phần mở đầu và bị xóa trước `3D4C` (kết thúc trò chơi). Trình kích hoạt khu vực `800A4288` cũng đặt vị trí khi đơn vị của chúng tôi rời khỏi hiện trường. Lý do là như nhau - đơn vị sơ tán cuối cùng không được tính là bị tiêu diệt hoàn toàn.

### `3D66`: Trình đọc bị ẩn trong con trỏ của bối cảnh máy ảo

Tìm kiếm trực tiếp phần bù `0x996` không thể tìm thấy đầu đọc của bit 7. Lý do là bối cảnh máy ảo tập lệnh `+0xC` lưu trữ `&engine+0x994` và đọc `(ctx->[+0xC])[+2]`. Tìm kiếm theo hình này và nhận được `800A3530` (trả về `& 0x80`). Người gọi duy nhất là bước trước `8009F4B4` của hướng dẫn đối thoại `3D3E`/`3D40`:

```c
// resident_func_8009F4B4(ctx, window)，3D3E = window 0，3D40 = window 1
if (first_frame && on_tactical_map) {
    speaker = text_speaker(text_id);                  // 8008CE54
    slot = find_unit_slot(speaker, engine[0x996] & 0x80);   // 800A2C18
    if (slot)            camera_target = slot->x, slot->y;
    else if (mode == 0)  camera_target = fallback_position(speaker);  // 800A3854
}
if (camera_target set) { if (scroll_camera_to(target)) clear target; }   // 80209DAC
else if (show_dialogue(window, text_id) == done) pc += 2;              // 8008FED4
```

`800A2C18` luôn trả về 0 khi sử dụng `0x80` làm chế độ, vì vậy việc đặt bit 7 có nghĩa là "đoạn hội thoại không theo người nói". focus-0/focus-1 chỉ thiếu thông số `3D66`: hai loa nằm ở phía trên bên trái và phía dưới bên phải của bản đồ và camera đầu tiên dừng lại giữa chúng.

| 3D66 | アレンビー Trước khi nói | レイン Trước khi nói | Dịch chuyển từng khung hình |
| --- | --- | --- | --- |
| 0 | Camera nhảy tới thiết bị của cô ấy ở góc trên bên trái | Camera nhảy tới thiết bị của cô ấy ở góc dưới bên phải | Hai lần nhảy toàn khung hình (VI 4907, 5094) |
| 1 | Camera không di chuyển | Camera không di chuyển | 0 |

Trong kịch bản gốc, `3D66 1`/`0` được ghép nối nghiêm ngặt, luôn bao gồm "`3D35` cuộn + hội thoại" - trước tiên hãy đặt camera đến vị trí hiển thị, sau đó để các nhân vật bên ngoài màn hình nói mà không bị kéo ra xa. Thí nghiệm biệt lập trước đó không có đối thoại ở giữa nên không thấy được sự thay đổi nào. ** Chỉ viết công tắc trường động cơ, bạn cần tìm đầu đọc của nó, sau đó đặt bối cảnh mà người đọc yêu cầu (ở đây là hội thoại) vào cấp độ, sau đó sẽ thấy hiệu ứng. **

### `3D59`／`3D3D`: Lựa chọn tấn công

Sau khi thêm `8015F700` vào thăm dò, được biết `3D59` thêm các ký tự vào danh sách và `3D3D` được đọc và xóa, nhưng scene8-2 không bao giờ vào giao diện lựa chọn tấn công. Đọc `3D3D` (`800A09D0`) và `801C78A0` nó gọi để tìm ra lý do:

```c
// 3D3D w0,w1,w2,w3,w4
wait(10);
base = first deployment record whose group == w4;       // w0/w1 不读，原脚本抄的是基准坐标
n = (w3 != 0 && w3 != 200 && w3 >= 16) ? 15 : w3;        // 100 实为 15
801C78A0(base.x, base.y, w2, n, w4);
if (w3) unit_list_8015F700 = {-1};

// 801C78A0：候选 = 我方机体库里 +0xC 有 0x80、驾驶员不在场、且不在 8015F700 名单里的机体
if (candidates == 0)      state = 5;                     // 什么都不做
else if (n == 0)          pick_mothership();             // 只看 +0x28 0x80000；唯一候选直接定
else if (n == 200)        select_all(); deploy();         // 不开界面
else                      open_sortie_screen(min(candidates, n));   // 战术状态 2
```

Trong trạng thái 2 (giao diện lựa chọn) và trạng thái 3 (chuyển từng giai đoạn), vòng lặp chính chiến thuật không chuyển tiếp tập lệnh và quay lại trạng thái 5 trước khi tiếp tục - bản thân `3D3D` không bị chặn nhưng toàn bộ tập lệnh bị đóng băng. Danh sách cảnh8 là `3D59 46`. Lúc đó thư viện máy bay của chúng ta chỉ có tàu mẹ ブライト, số lượng ứng viên là 0 nên không có chuyện gì xảy ra. **`8015F700` là danh sách loại trừ: `3D59` là "không được phép tấn công", không phải "phải tấn công". **

Ba cấp độ được sử dụng để xác minh. Lúc đầu, `3D5A` được dùng để đăng ký cho hai ứng viên ドモン và ヒイロ:

| Cấp độ | Lệnh | Kết quả |
| --- | --- | --- |
| xuất kích-a | `3D59 95`, `3D3D 8,8,0,1,2` | Chỉ có ドモン trong danh sách "これでよろしいですか?" → (8,8) Dịch chuyển xuất hiện, kịch bản Tiếp tục sau 384 VI |
| xuất kích-b | Chỉ cần thay đổi `3D59` thành 4 | Trong danh sách chỉ có ウイングゼロ của ヒイロ và người xuất hiện là ヒイロ |
| xuất kích-c | `3D5A 46,0,52,500`, `3D3D 5,10,0,0,3`, `3D3D 8,8,0,200,2` | Không thoát khỏi giao diện theo 2 bước: アウドムラ vào bảng tình mẫu tử và xuất hiện ở (5,10); thì ドモン và ヒイロ xuất hiện ở (8,8)/(8,6) Tự động xuất hiện |

Chuỗi trạng thái được cung cấp bởi các ảnh chụp nhanh lần lượt nhất quán với mã: a/b là `05 → 02 → 05`, c là `05 → 03 → 05` hai lần; vị trí bản đồ `+0xB` của đơn vị xuất hiện bằng số nhóm cơ sở và trạng thái hiện diện của người lái xe `8015DE90[角色]` thay đổi từ -1 thành 1.

Có 216 `3D3D` trong tập lệnh gốc, 193 trong số đó nằm ở phần mở đầu, tất cả đều nằm sau `3D4D`; trong từ thứ ba, có 85 vị trí cho 0, 100 cho 100 và 21 cho 200 (cảnh 4–10). Phổ biến nhất là 0 trước rồi 100. Sử dụng cả hai cùng nhau: chọn tàu mẹ trước, sau đó chọn đơn vị tấn công.

Cuộc thăm dò bổ sung thêm năm khu vực nữa cho mục đích này: `sortie_candidates` (`0x8015DA08`, danh sách ứng cử viên và số lượng ứng cử viên), `pilot_map_state` (`0x8015DE90`, mỗi ký tự -1 không có mặt/1 có mặt/2 Rút lui), `ship_table` (`0x8015E850`), `sortie_selection` (`0x80223538`, cờ đã chọn, con trỏ, giới hạn trên và số đã chọn), `sortie_base` (`0x802279E8`, điểm tham chiếu).

Nhân tiện, khi đọc mã, tôi phát hiện ra: `8009EDB8` chạy các sự kiện loại 13 khi `engine+4 == 0xC2`, nhưng không tìm thấy chỗ nào `0xC2` trong mã được tạo. 7 sự kiện thuộc loại 13 (tất cả `3D45`) có thể sẽ không được thực thi trong quy trình chính thức. Chỉ có bằng chứng tĩnh về điều này.

Tại thời điểm này, tất cả 21 `structure-confirmed` hướng dẫn chung đã được hoàn thiện.

## `3D75`: Thả thiết bị được gắn ra khỏi tàu mẹ (2026-09-17)

Bảy vòng đầu tiên đã không thể đo lường được hiệu quả. Sau khi đọc `80213758`/`80213AAC` bạn sẽ biết lý do: nó đề cập đến các đơn vị mang theo trong tàu mẹ, và các tàu mẹ trong bảy vòng đầu tiên không có đơn vị nào.

```c
// 3D75 actor
if (actor == 999) actor = 46;
if (actor in captains /*8021E398: ブライト シーラ エレ 葉月博士 エマリー ヘンケン ハワード*/)
    select every unit aboard that captain's ship;          // 母舰表 8015E85C/60，搭载表 8015E864
else
    select the actor's unit if it is aboard either ship;   // 否则什么也不做
every 4 frames: place one selected unit next to the ship, remove it from the aboard list,
                play SE 0xD1, player unit count += 1;        // 80213AAC
```

Việc tải chỉ được thực hiện bằng lệnh di chuyển của người chơi (`801CD0E4 → 801EAF88`). Không có lệnh tập lệnh nào cho phép các đơn vị lên tàu, vì vậy, launch-1 sử dụng các nút để điều khiển hoạt động của người chơi lần đầu tiên (`config/recomp/inputs/mini-stages/launch-input.json`):

1. Mở: `3D5A` đăng ký ブライト＋アウドムラ và ドモン, `3D3D …,0,3` cho アウドムラ vào bảng tình mẫu tử và xuất hiện trên (5,10), `3D3D …,200,2` Hãyドモン đứng bên phải nó.
2. Giai đoạn của chúng ta: Di chuyển con trỏ sang phải để chọn ドモン → "Di chuyển" → Di chuyển sang trái vào lưới tàu mẹ → Dấu nhắc "Mount" sẽ xuất hiện (khi con trỏ ở trên lưới tàu ở trạng thái chọn di chuyển, `0x80172EB2 == 4` không phải là mục menu) → Xác nhận.ドモン biến mất khỏi bản đồ, số lượng mang `8015E858` 0 → 1.
3. Menu bản đồ "フェイズEnd" → "はい".
4. Sự kiện đầu giai đoạn địch lượt 1 (loại 0, đầu `[0,2]`) thực hiện `3D75 999`.

| | Trước khi thực hiện (VI 6495) | Sau khi thực hiện (VI 6751) |
| --- | --- | --- |
| Khe bản đồ của chúng tôi | Chỉ アウドムラ (5,10) | Extra ドモン (5,8), nhóm số 2 |
| Số lượng mang theo | 1 | 0 |
| Số lượng đơn vị của chúng tôi | 1 | 2 |
| Màn hình | — | Máy ảnh di chuyển đến tàu mẹ, hiệu ứng chuyển tiếp màu tím xuất hiện phía trên nó và ドモン xuất hiện phía trên tàu mẹ |

Trong kịch bản gốc, `3D75` luôn xuất hiện trước khi thuyền trưởng hoặc nhân vật rời đi: シーラ, エレ quay trở lại バイストンウェル, ブライトTrước khi rời Rura, trước tiên bạn phải thả các đơn vị trên tàu để không rời đi cùng tàu mẹ. Tiếp theo dòng chữ "biến mất, rời khỏi chiến trường" trong video thực tế là `3D46`; khi không có đơn vị nào trên tàu hoặc các nhân vật không phải thuyền trưởng không được đưa lên tàu mẹ, `3D75` sẽ không làm gì cả - đây là trường hợp xảy ra trong bảy hiệp đầu tiên và trong hầu hết các video.

Nhân tiện, hai cạm bẫy đã được làm rõ:

- **Số lượt của tiêu đề sự kiện loại 0 được so sánh với `8010F5EA`, bắt đầu từ 0**: lượt đầu tiên là 0 và "ターン số 2" trên màn hình là 1. Đầu `[1,2]` (pha địch ở vòng 2) và `[2,1]` (giai đoạn giao hữu ở vòng 3) sẽ không được kích hoạt ở vòng 1 và 2.
- ** (Được bổ sung vào ngày 18 tháng 9 năm 2026) Trực tiếp `3D5A … 4000`** đối với các đơn vị vẫn còn trên bản đồ: hồ sơ phi công và máy bay đã bị xóa, nhưng các vị trí trong danh sách vẫn trỏ đến họ; nếu cấp độ này tiếp tục được trao cho người chơi, SIGBUS sẽ xảy ra khi vượt qua danh sách (`801FD020`→`801EB344`, xem `wufei-dummy-original-3`). Trước tiên hãy sử dụng `3D46 角色,1` để thoát và sau đó `4000`. Trong tập lệnh gốc, việc xóa như vậy xảy ra ở cuối hoặc ở đầu sự kiện cấp độ và sẽ không trở lại trạng thái hoạt động ở cùng cấp độ.
- **Lý do thực sự khiến trước đây "sự kiện lượt không được kích hoạt trong các lần chạy giới hạn"**: Tiêu đề của sự kiện lượt của các cấp độ đó được viết bằng `[0,0,0,0]` và giai đoạn 0 không bao giờ bằng 1/2. Cảnh 78 Sau khi vòng đó được đổi thành `[0,1]`, nó được kích hoạt ở vòng đầu tiên trong giai đoạn của chúng tôi.

## `3D63`: Chuyển đổi hạ cánh/chuyến bay (17-09-2026)

Toàn bộ trò chơi chỉ có một cảnh 80: `3D37 0` (vụ nổ trên ngựa báo) → `3D63 145` → `3D69 145,0` → "うぅ...しまった...体が...". Có vẻ như "bất động", nhưng đó chính là điều `3D69` thực hiện. Để xem riêng, tôi đã tạo một cấp độ có thể chơi thủ công `hyoma-3d63`: chỉ triển khai ngựa báo (bản ghi riêng của cảnh 80, バトルジェット) và mỗi lần nhấn "フェイズEnd", một bước sẽ được thực hiện ở đầu vòng tiếp theo.

| Vòng | Thi hành | Danh sách `+1` | Màn hình | Có thể hành động |
| --- | --- | --- | --- | --- |
| 1 (sau khi triển khai) | — | 2 | Treo lơ lửng trên không, có bóng bên dưới | Có thể |
| 2 | `3D63 145` | 2 → (5) → 1 | Rơi xuống đất, bóng tối biến mất | Khả năng (nhấn A để nhập "Chuyển động/Tinh thần/Khả năng") |
| 3 | `3D63 145` | 1 → (7) → 2 | Nâng trở lại không trung | Có thể |
| 4 | Trình tự gốc (vụ nổ, `3D63`, `3D69 145,0`, dòng) | 2 → (5) → 1 | Hạ cánh | Không thể (nhấn A để chỉ xem khả năng) |
| 5 | `3D69 145,1` | — | — | Khôi phục |

Mã khớp: `80212290` đọc chiều cao của mô hình 3D đơn vị. Khi bằng 5.0 (treo), hoạt ảnh hạ cánh của chế độ 5/9 được phát theo địa hình. Nếu không, hoạt ảnh cất cánh ở chế độ 7/0xA sẽ được phát, sử dụng cùng chức năng hoạt ảnh `801F1C48` cho lệnh bay/hạ cánh của người chơi. Vì vậy, cảnh 80 là một quá trình gồm hai bước "bắn hạ → không thể di chuyển".

Chơi tương tác:

```sh
.venv/bin/python tools/recomp/run/play_native.py --profile config/recomp/profiles/play-profile.json --language ja --images original --mini-stage config/recomp/mini-stages/hyoma-3d63.json
```

Nhấn F8 để vào menu chính; nhấn Z ở vùng trống trên bản đồ để mở menu → "フェイズEnd" → "はい". Sử dụng `hyoma-3d63-input.json` để xác minh giới hạn (nhấn phím sau vòng thứ 4 sẽ dừng ở màn hình khả năng và vòng thứ 5 sẽ chỉ được xác minh thủ công).

Cho đến nay, tất cả 73 lệnh thông thường đều là `code-confirmed`.

## Bước tiếp theo

1. Các mục menu hiển thị của menu chính: Lối vào hiện tại là phím nóng F8 trên menu chính và lời nhắc tiêu đề cửa sổ; vẽ các mục menu gốc trên màn hình tiêu đề yêu cầu đường dẫn vẽ gốc bên ngoài lớp hội thoại.
2. Tiêu đề chương và văn bản tùy chỉnh: Tiêu đề là văn bản `281 + 场景索引` và đoạn hội thoại chỉ có thể tham chiếu số văn bản hiện có; văn bản tùy chỉnh yêu cầu mục nhập lớp phủ của lớp văn bản máy chủ.
3. Các lệnh thông dụng không còn `unknown`; `3D69`/`3D6B`. Các trường chính xác (thí điểm `+0x34/+0x35`, thân máy `+0x0C`) đã được định vị. Điều còn thiếu là người tiêu dùng đang theo đuổi những bit này - hai bit này là các tham chiếu chéo tĩnh và cấp độ nhỏ đã đưa ra tất cả những gì nó có thể cung cấp.
4. Sự tương ứng từng mục giữa tham số thứ hai của `3D55` và bảng `80217D20` cũng như lớp giao diện mở và đóng của `3D36` vẫn yêu cầu các thử nghiệm đặc biệt.

## Tải mục nhập trực tiếp và thời gian chạy (21-09-2026)

Các cấp độ nhỏ là phương tiện gỡ lỗi và không còn trải qua quá trình trò chơi mới nữa. Sau khi bật menu chính (nút, F8, `SRW64_MINI_STAGE_ARM_VI` hoặc tải thời gian chạy), máy chủ sẽ trả lại quyền kiểm soát ở ranh giới khung của luồng trò chơi (`80085F30` trình bao bọc) theo trình tự thoát của chính lớp phủ tiêu đề: `800836CC(0)` → `800A5138()` (đặt lại trạng thái trò chơi khi quay lại tiêu đề, nội bộ `800814F0` Sẽ xóa số cảnh) → viết `8010F5F0 = 场景`, `8010F5EF = 1` → `80080188(0xC)` → `8007F510(0x800801A4, 0, 1)`. Điều này giống với lối ra "cấp tiếp theo" liên trường `801D8D20` (`801D8D94` tại `set_mode(0xC)`): nhà phân phối hàng đầu `800801A4` nhấn `8015DA02 - 1` tra cứu bảng, chế độ 12 vào `801C2D30 → 801C2B9C(0)`; `8010F5EF` non-0 Khi `801C2B9C` được sử dụng trực tiếp, `8010F5F0` không còn được sử dụng để tính toán cảnh (kịch bản 253 sẽ thu được khi không được khởi tạo). Sau đó `8009DD58 → 8009DE7C` đăng ký cảnh và hình ảnh được thay thế như bình thường.

Đo thực tế (`battle-ui-skills`, 60 VI/s): Nhấp vào ứng dụng nhân bản 6 VI, bản đồ xuất hiện trong khoảng 1,4 giây và màn hình mặt nạ đen mất khoảng 0,3 giây; đường dẫn cũ (trò chơi mới → Lời mở đầu A → Nhân vật chính/Tên → Lời mở đầu B) là 688 VI, khoảng 12 giây. Tập lệnh mở đầu của cấp độ (`3D4D` khoảng 612 VI, hai `3D45` khoảng 292 VI mỗi cấp, v.v.) vẫn không thay đổi và mất khoảng 26 giây để sẵn sàng khi được nhấp vào (38 giây ban đầu). `SRW64_MINI_STAGE_DIRECT=0` Giữ nguyên đường dẫn cũ. Không cần xem qua trang tên, các biến tên và tuyến đường của nhân vật chính vẫn trống sau khi đặt lại; các cấp độ yêu cầu chúng phải được thiết lập bằng tập lệnh của riêng chúng hoặc sử dụng đường dẫn cũ.

Tăng thời gian vào khoảng 700 VI sẽ thay đổi trạng thái RNG, mục tiêu và thứ tự tấn công của kẻ thù sẽ thay đổi tương ứng; phần phản công của `check_battle_actions.py` đã được thay đổi để thực hiện kiểm tra tương ứng dựa trên người phòng thủ thực tế (25 mục đã vượt qua, mã thoát 0, `build/recomp/debug/20260921T083602.242953Z/`).

**Tải bất kỳ tệp cấp cục bộ nào trong thời gian chạy**: Khi menu chính tiêu đề được hiển thị,
- Giao diện gỡ lỗi `mini_stage.load {"path": ...}` (`srw64_mini_stage_load` cho MCP), hoặc
- Khi bật giao diện gỡ lỗi (`--debug` hoặc đặt công tắc giao diện gỡ lỗi trên trang "Giới thiệu"), hãy kéo tệp cấp độ vào cửa sổ trò chơi (sự kiện kéo và thả SDL; thành công hay thất bại được hiển thị trên thanh thông báo).

Không có lối vào cấp độ nhỏ khi chơi bình thường (2026-10-06 do người dùng xác định): Kéo và thả không tải khi đóng giao diện gỡ lỗi; F8 và "Nhập cấp độ nhỏ" trên tiêu đề chỉ xuất hiện khi cấp độ đã được tải và cấp độ chỉ có thể được tải thông qua giao diện gỡ lỗi hoặc các công cụ phát triển (`play_native.py --mini-stage`, `srw64ctl launch --mini-stage`).

Hình ảnh đã biên dịch (`srw64.mini-stage-image.v1`) được tải trực tiếp; tệp nguồn cấp độ (`srw64.mini-stage.v1`) lần đầu tiên được biên dịch thành `runtime-mini-stage-N.json` trong thư mục đang chạy thông qua `SRW64_MINI_STAGE_COMPILER` (trình khởi chạy được đặt thành thoát shell `python tools/recomp/script_lab/mini_stage.py`) và đầu ra biên dịch có dạng `runtime-mini-stage-compile.log`. Đang tải sẽ thay thế hình ảnh hiện tại, đặt lại các ràng buộc và nhập vũ khí ngay lập tức; không cần bắt đầu bằng `SRW64_MINI_STAGE`. Các menu không có tiêu đề, tệp không thể đọc được và lỗi biên dịch đều bị từ chối và lý do được đưa ra. Xác minh: Khởi chạy không có cấp độ, tải menu trước tiêu đề bị từ chối, tệp bị thiếu bị từ chối, sẵn sàng 26,1 giây sau khi tải tệp nguồn `battle-ui.json`, mã thoát 0 (`build/recomp/debug/20260921T083917.598168Z/`). Đường dẫn kéo và thả chia sẻ `mini_stage::load_file` với lệnh gỡ lỗi và bản thân sự kiện kéo và thả không được xác minh tự động.