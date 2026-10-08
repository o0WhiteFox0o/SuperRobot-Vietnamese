> **Ngôn ngữ / Language:** [Tiếng Việt](save-slots-autosave.vi.md) · [English](save-slots-autosave.en.md) · [中文](save-slots-autosave.md)

# Cột đa lưu trữ, lưu trữ tự động và khả năng tương tác lưu trữ mô phỏng

2026-10-01. Tương ứng với [Lộ trình](mod-roadmap.md) B04 (nhiều vị trí thủ công, lưu tự động nút an toàn, sao lưu luân phiên). Bài viết này chỉ đề cập đến việc lập kế hoạch: Phần 1 là kết luận của phân tích tĩnh (tháo gỡ, các tệp SRAM hiện có và mã nguồn trình mô phỏng, không có đầu dò mới nào được thêm vào và không có hoạt động máy thực tế nào được thực hiện) và Phần 2 bắt đầu với kế hoạch. Các hạng mục xác minh trước khi thi công liệt kê trong Phần 3 đã được hoàn thành tĩnh trong cùng ngày và kết luận được ghi lại vào Phần 1.

Ba mục tiêu:

1. Kho lưu trữ băng cassette của máy chủ và kho lưu trữ của trình giả lập N64 có thể tương tác với nhau: bạn có thể đọc chúng khi sao chép chúng về quá khứ và bạn có thể đọc chúng khi sao chép lại.
2. Các khe lưu trữ không bị giới hạn ở hai khe trong phiên bản gốc.
3. Tự động lưu trữ khi phiên bản gốc đã được lưu trữ và luân chuyển nhiều bản sao.

Giải pháp một câu: Tệp băng cassette **32 KiB được giữ nguyên như một tệp để có khả năng tương tác; các cột mới được thêm vào và các kho lưu trữ tự động được lưu trữ trong tệp máy chủ và mỗi bản sao chứa các byte được phiên bản gốc ghi vào một cột lưu trữ (hoặc vùng ngắt). ** Khi đọc và ghi, máy chủ chỉ chuyển SRAM gốc sang các tệp khác và tất cả việc tuần tự hóa, xác minh và khôi phục đều tuân theo mã gốc.

## 1. Sự thật về kho lưu trữ gốc

### Bố cục SRAM 1.1 (32 KiB, địa chỉ liên quan đến điểm bắt đầu SRAM `0x08000000`)

| bù đắp | kích thước | nội dung | viết/đọc |
| --- | --- | --- | --- |
| `0x0000` | 0x10 | Tiêu đề tệp: số ma thuật 7 byte đầu tiên `SRW64V3` (bảng `800C6AE4`), +7 là byte cài đặt (`80162DA8`, bit0 gửi `80076D90`, giống như chế độ âm thanh) | Khởi động `8009171C` đọc; titleオプション Được sửa đổi bởi `8009187C` và viết lại +7 |
| `0x0010` | 0x1F00 | Lưu trữ cột 1 | `80092678(0)` viết, `80092744(0)` đọc |
| `0x1F10` | 0x1F00 | Lưu trữ Cột 2 | `80092678(1)`, `80092744(1)` |
| `0x3E10` | 0x3AE0 | Lưu trữ bản đồ ngắt (chỉ một bản sao) | `80093278(1)` viết; `8009365C` đọc tất cả, `80093610` chỉ đọc 0x20 byte đầu tiên tùy thuộc vào việc có cần thiết hay không |
| `0x78F0` | 0xA0 | Bitmap "đã xem" được chia sẻ bởi tất cả các băng cassette, từ RAM `8010F4D0`, xem §1.6 | **Mọi** lưu trữ cột và lưu trữ ngắt được viết trước tiên bởi `800916EC`; khởi động `8009171C` để đọc lại |
| `0x7990` | 0x670 | Không sử dụng (tệp hiện có chứa tất cả số không) | — |

- **Định dạng khởi động**: `8009171C` So sánh 7 byte đầu tiên của tiêu đề tệp. Nếu nó không khớp với số ma thuật, hãy xóa toàn bộ 32 KiB, sau đó ghi số ma thuật và byte cài đặt mặc định. Vì vậy, số ma thuật phải ở đúng vị trí khi nhập vào, nếu không trò chơi sẽ xóa toàn bộ lá bài.
- **Chuyển SRAM**: Tất cả đều đi qua `80090E5C(方向, SRAM 地址, RAM 缓冲, 长度)`, ghi hướng 1, đọc 0 (các tham số được chuyển giao cho PI DMA `800AE4A0` như cũ). Phía máy chủ rơi vào `save_write`/`save_read` của librecomp.

### 1.2 Bản ghi cột lưu trữ (0x1F00)

- Được tuần tự hóa từ `800924D8` tới bộ đệm `801C2600–801C44FF` (khung máy bay 0x2BC, trình điều khiển, các bộ phận được nén theo vật phẩm, quỹ, v.v.). Bộ nhớ này chỉ trống khi lớp phủ liên trường (`load_0008F4B0`, bắt đầu từ `801C4500`) được cài đặt; cả lớp phủ chiến thuật và lớp phủ chiến đấu đều bắt đầu từ `801C2600`, vì vậy định dạng cột chỉ có thể được ghi giữa các trường**.
- **+0 u16**: bit15 = đã sử dụng; 8 bit thấp hơn = tổng kiểm tra, bằng 8 bit thấp hơn của tổng 0x1F00 byte liên tiếp bắt đầu từ +2. Các byte 0x1F00 này cách cuối bản ghi 2 byte và được đọc vào `801C4500–801C4501`, đây là hai byte đầu tiên của lớp phủ liên trường. ROM `0x8F4B0` được cố định thành `00 00`. Vì vậy **bạn có thể tính tổng kiểm tra chỉ bằng cách nhìn vào tệp**: Cột 1 và vùng ngắt của ba tệp SRAM hiện có đều nhất quán.
- Viết `80092678`: ghi → đọc lại tại chỗ → tính toán lại so sánh tổng kiểm tra và trả về thành công hay thất bại.
- **Đọc không xác minh**: `80092744` và `80085CD4` (đọc 2 tiêu đề cột) chỉ nhìn bit15; tệp đã đọc `80092C70` của tiêu đề ロード cũng được khôi phục bởi `800927A4` nếu bit15 là 1.
- Các trường sử dụng cho danh sách đều có trong bản ghi (so với điểm bắt đầu của bộ đệm): +0x4C tổng vòng u16, +0x4F số từ, +0x51 số tiêu đề chương, +0x54 quỹ u32, +0x98 và sáu mã glyph tên; danh mục nhân vật chính bắt đầu từ +0x9D0 trong bảng nội dung (12 byte cho mỗi mục) và có được bằng cách tra cứu nội dung ban đầu 0x19–0x1C; mức mà `800A630C` đạt được được tính toán dựa trên dữ liệu trình điều khiển, do đó máy chủ không tự tính toán, xem §2.3.

### 1.3 Lưu trữ ngắt (0x3AE0)

- Menu bản đồ Ngắt → はい: Lớp phủ chiến thuật `load_000AB160` của `801D21D0` trước tiên ghi `80172EB2 = 8`, sau đó điều chỉnh `80093278(1)`, sau đó ghi `80172F09 = 1`, điều chỉnh `801D1534(4,0)` để trở về tiêu đề.
- `80172EB0`/`80172EB2` là trạng thái chính/trạng thái phụ của giao diện bản đồ, **không có trong bản ghi ngắt** (quy trình khôi phục chỉ khôi phục phần thân, trình điều khiển, các thành phần, khối tải và tiến trình làm mẹ). Viết 8 chỉ đi xuống máy trạng thái của menu xác nhận này.
- `80172F09` là cờ "vừa bị gián đoạn": nhà phân phối bản đồ `801DFCCC` quyết định trả lại tiêu đề sau khi rời khỏi bản đồ tương ứng; `800840C0`, `801E0350` sẽ xóa nó. Nó cũng không có trong hồ sơ.
- Vì vậy Host tự điều chỉnh `80093278(1)` và không cần bắt chước 2 lần ghi này.
- Bộ đệm `800FBEF0` (phân đoạn thường trú), +0 u16 cũng là tổng kiểm tra bit15+, chỉ bao gồm 0x1F00 byte đầu tiên.
- `80093278(0)` chỉ tuần tự hóa vào bộ đệm này và không ghi vào SRAM. `8009EDB8` Thực hiện việc này một lần trước khi chuyển sang màn hình khác ở giữa bản đồ. Khi bạn quay lại, hãy sử dụng chế độ 0x16 (`800801A4` mục 21) hoặc 0x22 (mục 33) để điều chỉnh `800936A0(0)` trực tiếp từ bộ đệm. Ảnh chụp nhanh được sử dụng khi bản đồ được trả về, do đó việc ghi đè bộ đệm khi bản đồ ở chế độ rảnh sẽ không có hiệu lực.
- Serializer chỉ ghi bộ đệm riêng của nó. Lệnh gọi bỏ qua duy nhất tới `800A4148` sẽ tính toán lại bitmap tóm tắt của `8016A1F0` theo trạng thái hiện có của nó mà kết quả không thay đổi.
- Tiêu đề コンティニュー (trạng thái chính 6) điều chỉnh `8009365C`: nếu bit15 là 1 thì chuyển sang chế độ 0x11 và quay lại bản đồ, nếu không sẽ bị ù. **Không bị xóa sau khi đọc**, kho lưu trữ ngắt sẽ được lưu giữ cho đến khi ghi đè ngắt tiếp theo.
- Kho lưu trữ ngắt ban đầu không lưu trạng thái số ngẫu nhiên bắt đầu từ `800D49D0` 0x834 byte (đây là nội dung của README "Khôi phục trạng thái ngẫu nhiên chưa hoàn chỉnh"). Không những vậy, mỗi khi lớp phủ chiến thuật được bắt đầu, `801E00AC` được dùng để đếm `8015DC50` và `800821B0` được gieo hạt lại nên phiên bản gốc đọc cùng một tệp ngắt và kết quả của trận chiến sau đó không được sửa.

### 1.4 Thứ tự byte của tệp

- `save_write` của librecomp được ghi từng byte theo địa chỉ byte N64 nên tệp máy chủ theo thứ tự gốc lớn và `SRW64V3` có thể đọc trực tiếp từ đầu (`build/recomp/save-recovery-check/intermission-cold-1.source.sram` đã được kiểm tra).
Thứ tự byte được xác định bởi trình mô phỏng và không liên quan gì đến trò chơi, vì vậy hãy đọc trực tiếp mã nguồn của từng trình mô phỏng (2026-10-01):

| giả lập | tập tin | độ bền | cơ sở |
| --- | --- | --- | --- |
| Máy chủ này (librecomp) | `<id>.bin`, 32 KiB | Đơn hàng thô lớn cuối | `pi.cpp``save_write` được viết từng byte dưới dạng `MEM_B` |
| Ares | `save.ram`, 32 KiB | **Big endian, giống như chủ nhà** | `n64/memory/lsb/writable.hpp` sử dụng `readm/writem(4)` để đọc và viết từng từ dưới dạng chữ lớn; 2026-09-30 ares thực sự đọc qua sau khi tệp máy chủ được đổi tên |
| Dự án64 | `.sra`, 32 KiB | Thứ tự đảo ngược từ 32 bit | `SaveType/Sram.cpp``DmaToSram` Viết trực tiếp RDRAM (PJ64 được lưu trữ nội bộ dưới dạng endian nhỏ) vào tệp và khi không căn chỉnh, hãy nhấn `^3` từng byte |
| mupen64plus | `.sra`, 32 KiB | Các từ 32 bit theo thứ tự ngược lại | `device/cart/sram.c`: `mem[(cart_addr+i)^S8]`, S8=3 trên máy chủ endian nhỏ, tệp là bộ nhớ |
| RetroArch mupen64plus-next | `.srm`, 0x48800 | Phân đoạn SRAM trong vùng chứa giống như mupen64plus | `libretro_memory.h`: EEPROM 0x800＋4×gói xử lý 0x8000＋SRAM 0x8000＋FlashRAM 0x20000, phân đoạn SRAM nằm trong 0x20800 |

ParaLLEl-N64 và các lõi khác không được kiểm tra. Nếu bạn gặp nó trong quá trình nhập, chỉ cần sử dụng số ma thuật để xác định nó (§2.5). Việc nhận dạng không dựa vào bảng trên: số ma thuật `SRW64V3` trong tiêu đề tệp được cố định theo nhiều thứ tự byte khác nhau.

### 1.5 Trạng thái liên quan đến thời gian lưu trữ

- **Phòng vào**: `801D8F74(参数)`. Tham số 0 = mục nhập bình thường (sau khi vượt qua cấp độ, cốt truyện sẽ được chuyển); 1, 2 = tiêu đề ロード đọc cột 0, 1 (gọi `80092C70(参数−1)`); 3 trở lên là コントローラパック.
- **时のマップへ**: Mỗi khung hình trong menu chính của trò chơi (`801CE19C`, đã được đóng gói dưới dạng `srw64_original_intermission_menu_step`). Khi nhấn A ở mục thứ 9, viết mã thoát `D_801DD540 = 2` và mờ dần; lập lịch màn hình `801D8D20` sẽ mở trò chơi sau khi nhìn thấy 2 và vào bản đồ tiếp theo.
- **Lượt của chúng tôi không hoạt động**: Tập lệnh đưa vào xác định nhàn rỗi hiện có (`docs/script/script-debug-injection.md`) - công cụ sự kiện không hoạt động, `8010F5E8 = 1` (giai đoạn của chúng tôi), `8010F6B0 = 0` (không có quy trình đánh bại), `8015DA02 ∈ {3, 0xB}` (bản đồ chiến thuật) - cùng với trạng thái bản đồ chính `80172EB0 = 5` (con trỏ nhàn rỗi, mỗi chức năng khung) `801C8B04`, được bao bọc dưới dạng `srw64_original_map_idle`). Vòng hiện tại `8010F5EA` bắt đầu từ 0.

### 1.6 Khối chia sẻ: hai ảnh bitmap "đã xem"

Bắt đầu từ `8010F4D0`, byte 0xA0 là hai bitmap 0x50 byte (640 bit), chỉ được đặt và không bao giờ bị xóa (chỉ bị xóa trong quá trình định dạng khởi động `80091470`):

| bitmap | đặt | đọc |
| --- | --- | --- |
| `8010F4D0` ký tự | `800914F4(人物号<287)`, qua bảng bí danh `800C6A08`; được gọi khi tải hình đại diện hội thoại `8008F970` và tạo bản ghi trình điều khiển mới `800A84F8` | lớp phủ tiêu đề `801C8AF8` (`80091574`) |
| `8010F520` đơn vị | `800915F0`; được gọi khi gán phiên bản đơn vị `800A6E68` | Đánh giá tiêu đề Âm nhạc/Mở khóa カラオケ (`80091670`, xem tài liệu menu tiêu đề) |

Bạn có thể làm được điều đó. Bạn có thể làm được điều đó. §2.5。

### 1.7 Trạng thái máy chủ

- 独立应用（`src/native/app/runtime.cpp`）：每次运行把上一次的 `sessions/<id>/save.bin` 拷进新会话，宿主运行中写 `runtime-data/saves/<id>.bin`。 **Gửi chỉ sau khi thoát bình thường** vào `save.bin` của phiên mới và cập nhật `last-session.txt`; kho lưu trữ của lần chạy này sẽ không được gửi khi nó gặp sự cố.
- Màn hình lưu trữ (`src/host/save_page.cpp`) và tiêu đề ロード đã được trang RmlUi tiếp quản. Cuộc gọi ghi là `80092678`, đầu đọc được gọi là `80085CD4` và quá trình đọc tệp được chuyển sang chế độ tải ban đầu `0x12 + 栏`.
- `800924D8`, `80093278`, `800927A4`, `800936A0` đã có hook (`game_hooks.cpp`), hiện chỉ được `state_probe` sử dụng.
- 宿主没有コントローラパック,Pak 路径固定走提示,本方案不涉及。

## 2. Kế hoạch

### 2.1 存档库（用户目录 `saves/`）

```
saves/
  cartridge.sram            32 KiB 卡带，大端，和 ares 的 .ram 同一份字节
  cartridge.sram.prev       上一代，发布新代前保留
  slots/007.rec  007.json   扩展栏：0x1F00 记录 + 旁注
  auto/inter-0.rec  .json   场间自动存档（栏格式），轮转
  auto/turn-0.sus   .json   回合自动存档（中断格式 0x3AE0），轮转
  imports/<时间>.sram        每次导入前的卡带备份
  trash/                    删掉的栏先挪到这里
```

- **栏号对用户连续编号**：栏 1、2 就是卡带里的两个物理栏，界面上标 「卡带」；栏 3起是扩展栏。
- **旁注 json**: 记录的SHA-256、写入时间、游玩时长、缓存的存档头（§2.3），以及可选的随机状态（§2.6）。 (Nhận xét ban đầu được lên kế hoạch nhưng đã bị ngừng theo yêu cầu của người dùng, xem §8.) Các ghi chú bên lề bị hỏng hoặc bị thiếu chỉ ảnh hưởng đến việc hiển thị và trạng thái ngẫu nhiên, nhưng không ảnh hưởng đến việc đọc tệp; bản thân bản ghi chỉ có giá trị dựa trên bit15 và phán đoán tóm tắt.
- **写入**：一律 「临时文件 → 刷盘 → 改名」。 Tệp cassette được phát hành ngay sau khi hoàn thành mỗi thao tác lưu trữ ban đầu (lưu trữ cột, gián đoạn, tùy chọn), không còn chờ thoát bình thường; `sessions/` vẫn tạo bản sao lịch sử và kiểm tra.
- **Di chuyển**: Khi phiên bản mới được khởi động lần đầu tiên, `save.bin` được trỏ bởi `last-session.txt` được xác minh và sao chép sang `cartridge.sram` và phiên cũ vẫn không thay đổi. `--import-save` 改为导入到卡带（走 §2.5）。
- **Cách ly**: Các phiên gỡ lỗi (srw64ctl/MCP) vẫn sử dụng thư mục đang chạy của riêng chúng. Đường dẫn lưu trữ được đưa ra bởi biến môi trường. Theo mặc định, nó trỏ đến bản sao trong thư mục đang chạy và không chạm vào kho lưu trữ trình phát.

### 2.2 Cột ảo: Chỉ thay đổi hướng truyền SRAM

Đóng gói `80090E5C`. Máy chủ duy trì hai ánh xạ:

- `slot_window[2]`: Cột vật lý 0 và 1 tương ứng với băng cassette hoặc tệp mở rộng. Mặc định là băng cassette.
- `suspend_target`：中断区对应卡带还是哪个自动存档文件。

只有地址和长度精确匹配下面三种传输时才改道:

| Vận tải | Phù hợp | Thực hành chuyển hướng |
| --- | --- | --- |
| Cột đọc và viết | `0x10` hoặc `0x1F10`, độ dài 0x1F00 | Đọc: ghi nội dung của file đích vào RAM ở định dạng big-endian; write: đầu tiên hãy đặt nó vào bộ đệm để gửi |
| Ngắt đọc và viết | `0x3E10`, độ dài 0x3AE0 | Tương tự như trên |
| 中断探测 | `0x3E10`,长度 0x20 | 读目标文件前 0x20 字节 |

Phần còn lại của quá trình truyền diễn ra như bình thường: mọi thứ ngoại trừ tiêu đề tệp, `0x78F0` khối chia sẻ và vùng ngắt sẽ rơi vào hộp mực.

Những điểm chính:

- `80092678` sẽ được đọc lại để so sánh ngay sau khi viết. Việc đọc lại phải truy xuất bộ đệm chưa được cam kết vừa nhận được, nếu không việc ghi sẽ bị đánh giá là không thành công. Sau khi hàm ban đầu trả về thành công, máy chủ sẽ xuất bản tệp một cách nguyên tử.
- Việc ánh xạ chỉ có hiệu lực trong một thao tác do trang bắt đầu: viết một cột, đọc một cột, đọc một loạt tiêu đề. Mặc định sẽ được khôi phục sau khi thao tác hoàn tất. Vì vậy, chế độ giao diện vanilla và bất kỳ đường dẫn nào không được tiếp quản sẽ chỉ chạm vào hộp mực và hoạt động giống hệt như vanilla.
- Không thay đổi librecomp. Việc chuyển hướng xảy ra ở lớp chức năng trò chơi và tệp máy chủ chỉ được đặt sau khi cuộc gọi ban đầu quay trở lại.

### 2.3 Đọc, viết và liệt kê nhiều cột

- **Ghi vào cột mở rộng k**: Ánh xạ cột vật lý 0 → k, điều chỉnh `80092678(0)` và quá trình xác minh tuần tự hóa, ghi và đọc lại ban đầu sẽ diễn ra như bình thường.
- **Đọc cột mở rộng k**: ánh xạ cột vật lý 0 → k, sau đó sử dụng chế độ tải ban đầu `0x12 + 0` và điều chỉnh `80092C70(0)` bằng lớp phủ liên trường.
- **Danh sách**: Mỗi lần ánh xạ hai cột mở rộng vào cột vật lý 0 và 1, điều chỉnh `80085CD4` một lần và lấy tiêu đề lưu trữ hai cột (bao gồm cả cấp độ). Các kết quả được lưu vào bộ đệm cùng với bản tóm tắt bản ghi và không được tính toán lại nếu bản tóm tắt không thay đổi. Bằng cách này, cấp độ và hình đại diện của nhân vật chính đều được đưa ra bởi logic ban đầu và máy chủ không phải tự phân tích dữ liệu trình điều khiển.
- **Chế độ giao diện gốc**: Chỉ hiển thị hai cột băng cassette, giống hệt như phiên bản gốc. Thanh mở rộng và tính năng tự động lưu chỉ xuất hiện trên các trang hiện đại.

### 2.4 Lưu trữ tự động

Có hai loại nút, mỗi loại sử dụng định dạng ban đầu và xoay vòng tương ứng (mặc định 3 bản sao giữa các trò chơi và 5 bản sao mỗi vòng, có thể thay đổi hoặc tắt trong cài đặt).

**A. Giữa các trường (Định dạng cột)**

- Nút 1 (vào trang): gói `801D8F74`, ghi "để tự động lưu trữ" khi tham số bằng 0; xây dựng menu chính giữa các trang web (`801CDFB0`, trang gốc đã được tiếp quản) và thực thi cũng như xóa cờ khi chạy lần đầu tiên. Việc đọc tệp và nhập trường (bắt đầu từ tham số 1) không được ghi nhớ.
- Nút 2 (trước khi tấn công): Gói `801D8D20`, xem `D_801DD540 == 2`, khi sắp tháo dỡ thì lưu trước rồi mới gọi hàm ban đầu. Cái này chứa tất cả những thay đổi mà người chơi đã thực hiện lần này.
- Cách thức: Ánh xạ cột vật lý 0 → `auto/inter-n.rec`, điều chỉnh `80092678(0)`. Đây cũng là con đường mà người chơi phải đi khi lưu vào データセーブ; khi cả hai nút được trang bị lớp phủ liên trường, bộ đệm `801C2600` không hoạt động (§1.2).
- Loại lưu trữ này là bản ghi cột thông thường, có thể sao chép sang cột cassette 1 và 2 cho trình mô phỏng.

**B. Lượt của chúng ta bắt đầu (dạng gián đoạn)**

- Nút: Trong gói `srw64_original_map_idle` (chức năng mỗi khung hình của trạng thái chính 5), nếu đáp ứng điều kiện không hoạt động của lượt của chúng tôi trong §1.5 và `8010F5EA` (lượt) khác với lưu trữ tự động của lượt cuối cùng, chức năng ban đầu sẽ được lưu trước rồi gọi. Nó chỉ được lưu một lần mỗi vòng; nó sẽ không trở về trạng thái chờ cho đến khi sự kiện ở đầu vòng được thực hiện, vì vậy nó đương nhiên được xếp hạng sau sự kiện.
- Phương pháp: Định tuyến lại vùng ngắt về `auto/turn-n.sus` và điều chỉnh `80093278(1)`. Không viết `80172EB2`, `80172F09` cũng như không trả lại tiêu đề: chúng không có trong bản ghi (§1.3). Việc tuần tự hóa sẽ ghi đè lên bộ đệm thường trú `800FBEF0`. Tại thời điểm này, ảnh chụp nhanh giữa chừng đã được sử dụng và không có tác động.
- Đọc: Vùng gián đoạn được chuyển hướng đến tệp đã chọn, sau đó lấy đường dẫn ban đầu của tiêu đề コンティニュー (trạng thái chính 6).
- Nếu người chơi chọn Ngắt trong menu bản đồ, vùng gián đoạn băng cassette vẫn được ghi để đảm bảo rằng trình mô phỏng có thể tiếp tục phát.

**Xử lý khối chia sẻ**: Cả hai kho lưu trữ tự động sẽ ghi khối chia sẻ `0x78F0` vào băng cassette theo phiên bản gốc. Đó là bitmap "đã nhìn thấy" (§1.6) chỉ tăng chứ không giảm. Viết nó vào có tác dụng tương tự như kho lưu trữ thủ công của trình phát; cột 1, 2 và vùng gián đoạn băng cassette sẽ không được lưu trữ tự động thay đổi.

### 2.5 Khả năng tương tác với trình mô phỏng

**Xuất**: Bản thân tệp cassette có định dạng ares và có thể được sao chép trực tiếp sang ares để sử dụng.

- Các trình mô phỏng khác chuyển đổi và xuất theo định dạng §1.4: `.sra` của Project64 và mupen64plus là từ 32 bit theo thứ tự ngược lại. `.srm` của RetroArch cũng theo thứ tự byte này, nhưng nó cần được ghi vào vùng chứa hợp nhất: nếu người dùng cung cấp `.srm` hiện có, thì chỉ phân đoạn SRAM trong đó sẽ được thay thế; nếu không được cung cấp, nó sẽ được tạo mới và các phân đoạn còn lại sẽ được điền bằng số không.
- Nếu bạn muốn mang thanh mở rộng hoặc tự động lưu vào trình giả lập: "Sao chép vào thanh cassette 1/2" được cung cấp trên giao diện. Xác nhận trước khi ghi đè. Thanh cũ bị ghi đè sẽ tự động được chuyển sang thanh mở rộng.

**Nhập khẩu** được chia thành hai loại:

- **Nhập toàn bộ thẻ**: Chuyển đổi tệp giả lập thành tệp băng cassette mới. Trước tiên, băng gốc được sao lưu vào `imports/` và các kho lưu trữ gốc trong cột băng 1 và 2 sẽ tự động được sao chép sang cột mở rộng và sẽ không bị mất; các bitmap "đã nhìn thấy" ở cả hai bên được ORed theo bit (§1.6) và tiến trình thu thập sẽ không bị mất.
- **Nhập một cột**: Chỉ lấy ra một cột hoặc vùng gián đoạn nhất định trong tệp giả lập và đưa nó vào cột mở rộng hoặc kho lưu trữ tự động. Thẻ sẽ không di chuyển.

**Nhận dạng định dạng** theo kích thước tệp và số ma thuật:

- 32 KiB: Thử thứ tự gốc, thứ tự đảo ngược từ 32 bit và thứ tự đảo ngược 16 bit để xem offset 0 có đọc được `SRW64V3` hay không;
- 0x48800 (Kho lưu trữ hợp nhất RetroArch): Tìm số ma thuật trong đoạn SRAM 0x20800 theo cách tương tự;
- Không khớp: từ chối nhập và không đoán. Trò chơi sẽ xóa tất cả các hộp mực không khớp với số ma thuật (§1.1), do đó việc nhập sai phải bị chặn ở cấp độ máy chủ.

**Tính hợp lệ**: Tệp đã đọc gốc chưa được xác minh nhưng tổng kiểm tra có thể được tính từ tệp (§1.2). Khi nhập, hãy kiểm tra xem số ma thuật, bit15 của mỗi cột, tổng kiểm tra và các trường tiêu đề lưu trữ có nằm trong phạm vi hợp lý hay không (số từ, số tiêu đề, vòng). Các cột có tổng kiểm tra không nhất quán sẽ được đánh dấu và người dùng có quyền quyết định có nên nhập chúng hay không.

### 2.6 Ghi chú trạng thái ngẫu nhiên (chỉ định dạng ngắt, không ảnh hưởng đến khả năng tương tác)

Chỉ cần tự động lưu vòng (và ngắt bản đồ của người chơi, nếu muốn). Không cần lưu giữa các trò chơi: khi bản đồ tiếp theo bắt đầu, `801E00AC` sẽ luôn được gieo hạt lại với số lượng `8015DC50` và trạng thái ngẫu nhiên giữa các trò chơi sẽ không bị lưu lại trên bản đồ (§1.3).

- Lưu trạng thái số ngẫu nhiên `800D49D0` (0x834 byte) và ghi tóm tắt vào ghi chú bên lề khi lưu trữ.
- Khi đọc file, phần tóm tắt bản ghi được đọc lại bởi `800936A0(1)` trùng khớp với ghi chú bên lề nên ghi "để viết lại".
- Điểm ghi lại được đặt trong gói gieo hạt hiện có `resident_func_800821B0`: khi lớp phủ chiến thuật được bắt đầu, `801E00AC` được gieo hạt. Sau khi hàm ban đầu trả về, các byte 0x834 được ghi lại và cờ sẽ bị xóa ngay lập tức. Lần đầu tiên số ngẫu nhiên được lấy sau đó, trạng thái tại thời điểm lưu trữ sẽ được sử dụng.

Bằng cách này, việc lưu trữ tự động vòng đọc trong máy chủ có thể tái tạo hoàn toàn khoảnh khắc lưu trữ, đáp ứng yêu cầu của lộ trình “phải ghi đè tính ngẫu nhiên cần thiết để khôi phục”; cùng một bản ghi sẽ không có chú thích trong trình mô phỏng và hiệu suất sẽ giống như phiên bản gốc.

### 2.7 Giao diện và cài đặt

- **データセーブ** (Giao diện hiện đại): Danh sách các cột có thể cuộn, phân trang, cột 1 và 2 được đánh dấu bằng băng cassette và "Cột mới" ở cuối. Mỗi cột có thể bị xóa (được chuyển vào `trash/`). Xác nhận bảo hiểm vẫn sử dụng hai câu gốc.
- **Tiêu đề ロード**: Tab được chia thành "thủ công/tự động". Tab tự động liệt kê hai kho lưu trữ tự động giữa các trò chơi và vòng chơi, với số lượng từ, vòng chơi và thời gian được đánh dấu.
- **Bảng điều khiển lớp phủ cài đặt**: công tắc lưu trữ tự động, hai loại bản sao xoay và lối vào nhập và xuất.
- Tất cả các ký tự mới được thêm vào danh sách nhập và cả ba ngôn ngữ đều có sẵn.

## 3. Các mục xác minh trước khi bắt đầu công việc (hoàn thành tĩnh vào ngày 2026-10-01)

| Mục | Kết luận | Xem |
| --- | --- | --- |
| `80172EB2 = 8`, `80172F09 = 1` | Trạng thái phụ của giao diện bản đồ và cờ "vừa bị gián đoạn" không được ghi lại và không cần phải bắt chước lưu trữ vòng tự động | §1.3 |
| `0x78F0` Khối chia sẻ | Hai bitmap "đã nhìn thấy" bổ sung cho các ký tự và máy, bất kể cột | §1.6 |
| Nút liên trường | `801D8F74(0)` Đang nhập trường liên thông; `801D8D20` Xem mã thoát 2 xuất kích | §1.5, §2.4 |
| Nút tròn | Tình trạng không hoạt động được đưa vào bởi tập lệnh + trạng thái chính 5 + thay đổi số vòng, treo trong `srw64_original_map_idle` | §1.5, §2.4 |
| Viết lại trạng thái ngẫu nhiên | Lớp phủ chiến thuật phải được gieo hạt lại khi bắt đầu; writeback được đặt sau khi đóng gói hạt giống; không cần giữa các trường | §1.3, §2.6 |
| Định dạng mô phỏng | Được xác định từ mã nguồn, không cần tệp mẫu | §1.4 |
| Tổng kiểm tra | 2 byte ngoài giới hạn là `00 00` trong tiêu đề lớp phủ liên trường, có thể được tính từ tệp | §1.2 |

Vẫn có những điều chỉ có thể được chứng minh bằng hiệu suất thực tế: màn hình phù hợp với các giá trị sau khi đọc lại lưu tự động, kết quả trận chiến được sao chép sau khi trạng thái ngẫu nhiên được ghi lại và các ares được đọc và ghi qua lại (S2–S5).

## 4. Các giai đoạn và nghiệm thu

| Sân khấu | Nội dung | Chấp nhận |
| --- | --- | --- |
| S0 | Hoàn thành tĩnh §3 | Đã hoàn thành (2026-10-01) |
| S1 | Lưu trữ thư viện, di chuyển, nhập và xuất toàn bộ thẻ và cột đơn, nhận dạng định dạng | Đã hoàn thành (2026-10-01), xem Phần 6 |
| S2 | `80090E5C` Định tuyến lại, lưu và đọc nhiều cột, xuất bản tức thì, trang hiện đại | Đã hoàn thành (2026-10-01), xem Phần 7 và [Tài liệu màn hình đã lưu trữ](../native/native-save-screens.md) Phần 4 |
| S3 | Tự động lưu trữ hai nút giữa các trang web, luân chuyển | Đã hoàn thành (2026-10-01), xem Phần 8 |
| S4 | Tự động lưu vòng, コンティニュー đọc chuyển hướng, ghi chú bên trạng thái ngẫu nhiên | Đã hoàn thành (2026-10-01), xem Phần 8 |
| S5 | và mô phỏng đo lường thực tế | Đã hoàn thành (2026-10-01), xem Phần 9 |

Để chạy máy thực S2 trở lên và chạy trình mô phỏng S5, vui lòng hỏi trước khi bắt đầu mỗi lần chạy.

## 5. Những việc không nên làm

- Không lưu trữ theo thời gian thực bất cứ lúc nào (xem lộ trình để biết lý do). Việc hoàn tác trong lượt được để lại cho M3.
- Định dạng lưu trữ ban đầu sẽ không bị thay đổi và không có dữ liệu riêng tư nào của máy chủ sẽ được ghi vào băng cassette; dữ liệu riêng tư của máy chủ sẽ chỉ được đặt trong ghi chú bên lề.
- Cannon Torotron không được hỗ trợ.

## 6. Hồ sơ thực hiện S1 (2026-10-01)

Mã:

- Lớp định dạng: [`src/native/app/sram.hpp`](../../src/native/app/sram.hpp)/`sram.cpp`, xử lý byte thuần túy, không chạm vào tệp.
- Thư viện lưu trữ: [`save_library.hpp`](../../src/native/app/save_library.hpp)/`save_library.cpp`.
- Bắt đầu truy cập phiên: `Session` trong số `runtime.cpp`.
- Dòng lệnh: `--export-save`, `--export-format` (`export_save` của `runtime.cpp`, `--play` nhánh của `host.cpp`).

Sự khác biệt so với §2:

- **Các băng cassette không được phát hành ngay** và vẫn được phát hành trước `Session::commit_save` khi máy chủ thoát ra bình thường (các hộp mực cũ hơn được để lại dưới dạng `.prev`). Để phát hành ngay lập tức, bạn cần biết trong chuỗi trò chơi rằng "thao tác lưu ban đầu đã hoàn tất" và thực hiện việc đó cùng với gói `80090E5C` của S2.
- **Ghi chú bên lề json được lưu cho S2**. Tệp bản ghi của S1 chỉ lưu trữ các byte gốc, tính toàn vẹn dựa trên bit15 và tổng kiểm tra có thể tính toán (§1.2) và việc ghi dựa vào việc đổi tên nguyên tử. Lưu ý phụ chỉ dành cho bộ đệm hiển thị và trạng thái ngẫu nhiên, được cấu hình bởi máy chủ có thể sử dụng nlohmann json.
- **Nhập dòng lệnh là nghiêm ngặt**: Nếu băng cassette thiếu số ma thuật hoặc tổng kiểm tra cột/vùng ngắt đã sử dụng không khớp, quá trình nhập sẽ bị từ chối. Tùy chọn "Nhập vẫn cần được nhập nếu tổng kiểm tra không khớp" được để lại cho giao diện S2.
- **`--new-game` Không mất cột**: Trước khi xuất bản một băng cassette mới, cột 1 và 2 còn nguyên trong băng cassette cũ được lưu vào cột mở rộng; các bản ghi có cùng byte sẽ không được lưu nhiều lần. Ngay cả khi băng cũ bị hỏng, nó sẽ không cản trở trò chơi mới. Chỉ những cột còn nguyên vẹn mới được giữ lại; các thư mục cũ chưa được di chuyển sẽ được di chuyển trước. Nếu quá trình di chuyển không thành công, trò chơi mới sẽ bắt đầu như bình thường.
- **Nhóm lưu trữ tự động** (`auto/`) và **Thùng rác** (`trash/`) được thêm vào S3, S4 và giao diện.

Kiểm tra (không cần ROM):

- `tests/native_save.cpp` (`native-save`): Chuyển đổi giữa bốn định dạng xuất và thứ tự đảo ngược 16 bit, bộ chứa RetroArch giữ lại các bản lưu trữ khác, hai ranh giới tổng kiểm tra (cột ngoài giới hạn 2 byte, chỉ đếm 0x1F00), trường tiêu đề lưu trữ, báo cáo tham nhũng, hợp nhất bitmap "đã nhìn thấy", lưu giữ bản phát hành `.prev`, nhập giữ lại các cột cũ và bản sao lưu, lặp lại nhập không trùng lặp cột, nhập cột đơn, sao lưu trước khi xuất, từ chối ghi đè các tệp lớn không liên quan, cột mở rộng 3-99 đã đầy.
- `tests/native_app.cpp`: phiên giải phóng hộp mực, từ chối kho lưu trữ máy chủ chưa được định dạng, từ chối khởi động nếu hộp mực bị hỏng và có thể `--import-save` khôi phục, `--new-game` giữ lại các cột cũ, `sessions/` cũ di chuyển, xuất tham số.
- Máy chủ giả mạo `native_launch.cpp` và `native_rom_import_probe.cpp` viết lại băng cassette bằng những con số ma thuật.
- Hiện tại có 3 SRAM thật (Đã xóa Chapter 1, gián đoạn Vòng 5, gián đoạn Vòng 1) đều được đánh giá là nguyên vẹn. Cột 1 ghi Chương 1, Vòng 7 và Quỹ 14500, nhất quán với [Tài liệu màn hình lưu trữ](../native/native-save-screens.md).

## 7. Hồ sơ thực hiện S2 (2026-10-01)

Cách thực hành và kết quả thực tế được nêu trong Phần 4 của [Tài liệu màn hình được lưu trữ](../native/native-save-screens.md). Chỉ những khác biệt và phần còn lại từ §2 được ghi lại ở đây:

- **Việc phát hành băng cassette ngay lập tức đã được thực hiện**: Máy chủ theo dõi mọi thao tác ghi vào băng cassette và phát hành nó khi có băng cassette; `Session::commit_save` phát hành lại khi thoát (nội dung sẽ không thay đổi nếu nội dung giống nhau). Khi bắt đầu trò chơi mới, hãy di chuyển cột của hộp mực cũ vào cột mở rộng (khi xây dựng `Session`), vì hộp mực trống sẽ được giải phóng sau khi trò chơi được định dạng.
- **Danh sách không được lưu vào bộ nhớ đệm**: Tiêu đề lưu trữ cột mở rộng được đọc lại bằng `80085CD4` mỗi khi danh sách cột được mở. Cột 99 chỉ có chục bản bộ nhớ nên việc lưu trữ tiêu đề cache ở ghi chú bên cạnh chưa được thực hiện; ghi chú phụ json sẽ được thêm vào khi có trạng thái ngẫu nhiên (S4).
- Cột xóa, nhập xuất trong giao diện và "Nhập vẫn cần nhập nếu tổng kiểm tra không khớp" chưa tồn tại tại thời điểm đó đã được hoàn thành trong §8. Giao diện gốc (chuyển về màn hình liên trường ban đầu và màn hình tiêu đề trong cài đặt) chỉ có hai cột cho băng cassette như ở phiên bản gốc. Đây là cố ý: chế độ gốc không thêm bất cứ thứ gì mà phiên bản gốc không có; cột mở rộng và kho lưu trữ tự động có thể được đọc và ghi trong giao diện phiên bản mới.

## 8. S3, S4 và giao diện trong game (2026-10-01)

### Lưu trữ tự động (`src/host/autosave.cpp`)

Chỉ được bật khi có thư viện lưu trữ (ứng dụng độc lập; phiên gỡ lỗi cần vượt qua `SRW64_SAVE_LIBRARY`).

| Nút | Móc | Phương pháp viết |
| --- | --- | --- |
| Vào sân liên trường | `801D8F74` bao bì (mới được đổi tên thành `srw64_original_intermission_enter`) được ghi lại khi tham số bằng 0 và được lưu mọi khung hình của menu liên trường tiếp theo (sau `801CE19C`) | `save_store::Window(0, 新文件)` xuống `80092678(0)` |
| Trước khi tấn công | Bạn sẽ thấy `D_801DD540 == 2` sau mỗi khung hình trong menu liên trò chơi (cùng một trò chơi chỉ được lưu một lần) | Tương tự như trên |
| Bắt đầu vòng đấu | Bản đồ không hoạt động ở mọi khung hình `801C8B04` Trước: Trạng thái chính 5. Các điều kiện nhàn rỗi được đưa vào bởi tập lệnh, (số tiêu đề, vòng) khác với lần trước | `save_store::SuspendWindow(新文件)` Đã hạ cấp `80093278(1)` |

- File: `auto/inter-NNNNNN.rec` (dạng cột), `auto/turn-NNNNNN.sus` (dạng gián đoạn), cả hai đều có chung số serial tăng dần, càng mới càng lớn. `.json` bên cạnh ghi lại nút, thời gian, số tiêu đề, vòng và số tiền; kho lưu trữ tròn cũng ghi lại số ngẫu nhiên 0x834 byte (thập lục phân) và SHA-256 được ghi lại.
- Rotation: Sau khi viết, chỉ có N bản mới nhất được giữ lại theo loại (mặc định là 3 ván, 5 vòng; tùy chọn 1/3/5/10 trên trang cài đặt), những bản thừa sẽ bị xóa cùng với phần lề. Thanh và cassette bằng tay không bị ảnh hưởng.
- Dấu "mỗi hiệp một lần" được đặt lại giữa lúc vào sân, tấn công và khi bản đồ được khôi phục: đọc lưu một hiệp và quay lại cùng một hiệp sẽ không lưu ngay một bản sao khác.

### Đọc kho lưu trữ tự động

- Danh sách tiêu đề ロード liệt kê tất cả các bản lưu tự động sau thanh mở rộng, với những cái mới hơn trước. Kho lưu trữ giữa các phiên sử dụng cùng một "chuyển hướng một lần để tải cột 0" làm cột mở rộng.
- Lưu trữ vòng: Sau khi xác nhận `arm_suspend(文件)`, ghi trạng thái chính của tiêu đề là 6 (コンティニュー), trạng thái phụ 0 và giao cho phiên bản gốc: `801C6D1C`, kiểm tra vùng gián đoạn đọc, chuyển chế độ 0x11, `800936A0(1)`, đọc lại và khôi phục bản đồ. Cả hai lần đọc đều từ tệp này; quá trình khôi phục hoàn tất (sau khi đóng gói `800936A0`) và chuyển hướng được giải phóng. Ban đầu, gọi trực tiếp `801C6D1C` sẽ ghi mức tăng của trạng thái phụ thêm 1 vào trạng thái phụ ロード và màn hình sẽ dừng ở hộp xác nhận nên chuyển sang trạng thái chính 6.
- Số ngẫu nhiên: Khi khôi phục xong, nếu file tóm tắt trùng khớp với lề thì ghi ra để viết lại; khi lớp phủ bản đồ được bắt đầu, `801E00AC` được tạo hạt giống (sau khi đóng gói `800821B0`) và 0x834 byte được ghi lại ngay lập tức. Sau đó, số ngẫu nhiên vẫn sẽ được nâng cao từng khung hình theo phiên bản gốc và một số khác `8010E09C` sẽ được gieo lại khi bắt đầu trận chiến, do đó kết quả sẽ khác nếu nhịp hoạt động của người chơi khác nhau; việc ghi lại chỉ đảm bảo rằng trạng thái ngẫu nhiên tại thời điểm tải giống như khi lưu. Hai số đếm này có thể có mục đích tính thời gian khác và chưa được động tới.

### Giao diện trong game

- **REMOVED** (R): Thanh mở rộng và tự động lưu. Cửa sổ xác nhận kế thừa vị trí của cửa sổ lớp phủ (chế độ 3, "データを気ます.よろしいですか?", mặc định là "いいえ"); "はい" di chuyển bản ghi và phần lề vào `trash/`. Không thể xóa khe cassette 1 và 2.
- Lưu trữ tự động hiển thị thời gian lưu trữ ở phía bên phải của “Tập N”. Nhận xét cột (L nhập tại chỗ) đã được thực hiện trước đó, bị xóa theo yêu cầu của người dùng vào ngày 2026-10-01: Không có chức năng nhận xét và L không hoạt động trên trang lưu trữ.
- **Trang cài đặt lưu trữ** (trang mới của cửa sổ cài đặt "Lưu trữ", `saves_page` của `frontend.cpp`): tự động chuyển đổi lưu trữ và số lượng bản sao, xuất, nhập, xem [Cửa sổ cài đặt](../native/settings-window.md). Xuất ghi `export/srw64-ares.ram`, `srw64-project64.sra`, `srw64-mupen64plus.sra`, `srw64-retroarch.srm`, mỗi lần ghi đè lên bản trước đó. Quét nhập `import/`, mỗi tệp liệt kê các cột được sử dụng; các cột không khớp với tổng kiểm tra sẽ được nhắc trước tiên, hãy nhấp lại để nhập với tổng kiểm tra đã sửa (`SaveLibrary::import_slot(…, repair)`). Việc nhập toàn bộ thẻ vẫn chỉ thông qua dòng lệnh `--import-save`: thay thế băng cassette trong khi trò chơi đang chạy sẽ không khớp với băng cassette trong bộ nhớ trò chơi.
- Đưa cột mở rộng hoặc lưu tự động vào giả lập: đọc file xong lưu vào cột 1 hoặc 2 rồi xuất.

### Xác minh

- Ngoại tuyến: `native-save` 71 mục (số sê-ri lưu trữ tự động mới, xoay theo danh mục với lề, xóa vào thùng rác, nhập sửa chữa một cột, quét); kiểm tra bố cục đã thêm các mẫu lưu trữ tự động, cột mở rộng, cửa sổ xóa và trang cài đặt lưu trữ (bao gồm danh sách nhập), bốn kích thước cửa sổ và ba vấn đề về ngôn ngữ.
- Máy thực tế: `tools/recomp/debug/check_autosave.py` được chạy trong năm lần (luồng cấp độ nhỏ, vượt qua cấp độ và vào sân và tấn công, bắt đầu vòng bản đồ theo chu kỳ của kẻ thù, lưu vòng đọc tiêu đề, đọc tiêu đề, lưu tấn công và lưu vào cột 3 (L không hoạt động), xóa kho lưu trữ tự động cũ nhất); `check_save_settings.py` (Trang cài đặt lưu trữ: chuyển đổi, số lượng bản sao, xuất bốn tệp, kiểm tra từng byte, nhập, tổng kiểm tra các cột không nhất quán bị từ chối trước rồi sửa đổi) 8 mục đã vượt qua.
- Ba vấn đề được tìm thấy và khắc phục trong trò chơi thực tế: Gọi trực tiếp `801C6D1C` trong vòng lưu sẽ bị kẹt trong hộp xác nhận (xem ở trên); trang tiêu đề sẽ điều chỉnh bước trang trong mỗi khung hình và các hành động trống được coi là "hủy" và cửa sổ xóa sẽ đóng ngay lập tức.

## 9. S5: đo thực tế bằng mô phỏng (2026-10-01)

`tools/recomp/debug/check_emulator_interop.py`, 7 mục đã được thông qua; không có cửa sổ trò chơi nào được mở, máy chủ chỉ được sử dụng để xuất và nhập.

- **Chỉ nhập dòng lệnh**: `srw64-gfx-host --play --import-save 文件 [--user-dir 目录]`, không có `--rom`, chỉ nhập tệp vào băng cassette, không khởi động trò chơi (`import_save` của `runtime.cpp`) và giữ cùng khóa thư mục người dùng như trò chơi (`UserLock`, bị từ chối khi trò chơi đang chạy).
- **RetroArch (mupen64plus-next core, phiên bản cố định trong `build/libretro/cores`, headless driver)**: Đặt toàn bộ `.srm` được viết bởi `--export-save` vào bộ nhớ lưu trữ của lõi (cách RetroArch đọc `.srm`); đầu vào tập lệnh là từ tiêu đềロード Đọc cột 1. Sau khi nhập vào trường này, データセーブ được lưu trong cột 2; ghi bộ nhớ lưu trữ lõi trở lại `.srm` và sau đó `--import-save`: được nhận dạng là RetroArch/thứ tự đảo ngược từ 32-bit, cột 2 Nó được viết bởi lõi, tổng kiểm tra là chính xác và tiêu đề lưu trữ (số từ, vòng, quỹ, tên) giống với cột 1. Ảnh chụp màn hình: danh sách tải, giữa các trò chơi, sau khi lưu.
- **ares(`/Applications/ares.app`, dịch vụ GDB đọc bộ nhớ)**:
- Đọc: Cassette được đọc là `save.ram`. Sau khi khởi động, bitmap "đã nhìn thấy" của `8010F4D0` có cùng byte với byte như `0x78F0` của băng cassette. So sánh: Hộp mực tương tự được cung cấp cho các ares theo thứ tự ngược lại của các từ 32 bit và bitmap hoàn toàn bằng 0 (trò chơi xử lý nó như thể hộp mực chưa được định dạng), cho biết rằng kiểm tra này có thể phân biệt thứ tự byte.
- Ghi: Không có kho lưu trữ nào được cung cấp, trò chơi định dạng băng cassette theo ares, bộ nhớ riêng của ares sẽ tự động được lưu (cứ sau 30 giây) và ghi ra `save.ram`; `--import-save` được công nhận là big endian và băng đã nhập giống với từng byte của tệp ares.
- **Việc chưa làm**: Ares không điều khiển game lưu một cột nhất định (ares chỉ nhận diện bàn phím của cửa sổ focus, test không lấy quầy lễ tân); Việc ghi trong trò chơi ở cấp độ cột được bao phủ bởi lõi RetroArch ở trên và thứ tự byte tệp của ares được xác định bằng cả việc đọc và ghi. Project64 không có phiên bản macOS. Theo mã nguồn, nó có cùng thứ tự với mupen64plus (§1.4) và chỉ được kiểm tra định dạng S1.