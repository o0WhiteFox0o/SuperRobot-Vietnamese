> **Ngôn ngữ / Language:** [Tiếng Việt](battle-viewer.vi.md) · [English](battle-viewer.en.md) · [中文](battle-viewer.md)

# Nghiên cứu thiết kế Battle Viewer

2026-10-03. Phân tích tĩnh thuần túy (tháo gỡ `build/recomp/cpu-scan/*/rom_*.text.s`, dữ liệu ROM), **không chạy trò chơi, không xây dựng**. Mục tiêu: Thêm mục "Đánh giá trận chiến" bên cạnh "Thư viện" và "MOD" trên màn hình tiêu đề (tham khảo Battle Viewer của SRW Z スペシャルディスク), người chơi chọn đơn vị tấn công + phi công, vũ khí, đơn vị phòng thủ + phi công, vũ khí phản công và phản công, phản ứng phòng thủ của người phòng thủ (đánh/tránh/nhân bản/cắt/S phòng thủ/khiên), sát thương số lượng, có bắn hạ hay không, nền chiến đấu của cả hai bên, BGM, sau đó sử dụng lớp phủ hiệu suất ban đầu `load_00121560` để chơi và quay lại trang đánh giá sau khi kết thúc. Nó cũng phục vụ như một công cụ thử nghiệm cho màn trình diễn của chúng ta.

Ai viết "suy luận" là chưa kiểm tra bằng máy thực tế; số dòng đề cập đến văn bản được tháo rời trong `build/recomp/cpu-scan/` (`resident/rom_80076610.text.s` được gọi là cư dân, `load_00121560/rom_801C2600.text.s` được gọi là trận chiến, `load_000AB160/rom_801C2600.text.s` được gọi là bản đồ và `load_0010DA50/rom_801C4500.text.s` được gọi là tiêu đề).

Tài liệu liên quan: [Cơ chế kết xuất trận chiến](battle-animation-rendering.md), [Thoát trận đấu giữa chừng](../native/battle-animation-skip.md), [Tính toán trận chiến](../gameplay/battle-formulas.md), [Thư viện](../native/library.md), [Menu tiêu đề](../native/native-title-menus.md).

## 0. Kết luận đầu tiên

**Bản thân phiên bản gốc có đường dẫn đến "chơi show mà không cần vào cấp độ"**: trận chiến trình diễn chế độ chờ danh hiệu (chế độ trò chơi `0x1C`) và trận chiến nền カラオケモード (chế độ `0x1A`). Cả hai đều chỉ cài đặt lớp phủ hiệu suất. Hàm thường trú **`8009C2DC`** điền trực tiếp vào hồ sơ chiến đấu `D_800F97E0 + side×0x1074` ở cả hai bên theo bản ghi trình diễn 32 byte trong ROM (ROM `0x83110` trở lên). Không cần lớp phủ bản đồ, danh sách, cấp độ hoặc kho lưu trữ. Sau khi phát, vòng lặp chương trình chính sẽ chuyển về lớp phủ tiêu đề.

Do đó, không cần phải tạo các cấp độ nhỏ ẩn hoặc các khu định cư trên bản đồ giả để đánh giá trận chiến: **Việc vào và quay lại chế độ `0x1C` được thực hiện, máy chủ móc vào `8009C2DC` và hồ sơ tham gia trận chiến được viết lại theo lựa chọn trên trang đánh giá**. Đánh/tránh/nhân bản/cắt/S phòng thủ/lá chắn, lượng sát thương và hạ gục đều được xác định bởi một số trường trong hồ sơ trận chiến. Lớp phủ hiệu suất không tung bất kỳ viên xúc xắc nào để xác định kết quả (phép tính nằm trong lớp phủ bản đồ và đường dẫn này hoàn toàn không chạy).

## 1. Quy trình thông thường: Bản đồ → Hiển thị → Bản đồ

| Bước | Vị trí | Sự kiện |
| --- | --- | --- |
| Quá trình tấn công | bản đồ trạng thái 24 `801D6534`, bảng trạng thái phụ `D_80217CC4` | bảng tham gia xây dựng tiểu bang 0 `8018B6E8` (kích thước bước 0x5C), giải quyết 2/3 `801F7D6C`, 8 nhánh yêu cầu qua `801DF96C` (xem chi tiết [battle-animation-skip.md](../native/battle-animation-skip.md)) |
| Điền vào hồ sơ tham gia biểu diễn | bản đồ `801F3578` (bản đồ:55379) | Viết `D_800F97E0`/`D_800F97E0+0x1074` từ hai mục trong bảng tham gia, xem §2 để biết các trường |
| cái nĩa | bản đồ `801D4E6C` (bản đồ:20953) | `8015DDA8 & 4` xóa (bật hoạt ảnh) → `8009DB8C()`, `80080188(2)`, `80099814(5,1,2)` mờ dần |
| Thay đổi lớp phủ | cư dân `800801A4` (cư dân:11582), bảng nhảy `jtbl_800CFEC8` (chỉ số dưới = chế độ − 1) | Chế độ 2 → `8007FF4C` (cư trú:11372) cài ROM `0x121560..0x184730` vào `801C2600`, cài riêng `0x217FD0..0x22CFD0` vào `80400000`; thì `8007F510(801C9BD4,0,0)` |
| Lối vào biểu diễn | trận `801C9BD4` (trận:8698) | Sử dụng số lượng khung hình chung `D_8010E09C` để nối lại `800821B0`; giá trị ban đầu của ống kính và ánh sáng; `80084A54` xóa trạng thái nền; `801C2C3C` mặt nạ; chế độ điều chỉnh 0x1A `8009C1DC`+`8009C2DC(0)`, chế độ gọi 0x1C `8009C2DC(1)`; đăng ký từng khung `801C9710`/rút `801C96F4` |
| mỗi khung hình | trận `801C9710` (trận:8367) | trạng thái `D_80250000`, bảng nhảy `D_80222DD4` (25 mục, xem đoạn dữ liệu trận chiến `rom_80222D44.data.s:87`) |
| Kết thúc | trận chiến `801C9854..801C99F0` | Sau khi quá trình làm mờ hoàn tất `800B6620(1)`, `8009ABCC`, `800997D0`, `8008B950` (giải phóng 300 khe Elf), `8008DB2C`, `8008AC78(4)`; nhấn chế độ để chọn chế độ tiếp theo (§4), `8007F510(800801A4,0,1)` Trở về nhà phân phối |
| Quay lại bản đồ | Chế độ 0xB (khi chế độ trước đó là `D_8015DD60 == 3`) nếu không thì 0x10 | Bản đồ ở trạng thái 24 trạng thái phụ 4 bởi `801FCA78` và ghi kết quả vào danh sách |

Những điểm chính: **Lớp phủ hiệu suất chỉ đọc hồ sơ trận chiến `D_800F97E0`**, không bao giờ ghi danh sách; khu định cư `801F7D6C` đã được chạy qua lớp phủ bản đồ trước khi được tải. Các lần rút ngẫu nhiên trong chương trình chỉ bao gồm chọn đường (`80222B14` hai lần `80082334`) và tư thế hành động vũ khí phổ thông-0 một lần (`801E3BA0`), điều này không ảnh hưởng đến kết quả.

Số trạng thái và quy trình (`D_80222DD4`): đặt lại 0 `801C6FE8`, 1 `801C70A8` tải, 2/7/13/18 `801C840C` dòng, 3 `801C7494` tiếp cận, 15/4 `801C75D0`, 16/5 `801C76A0` Bắn (chuyển sang nền phòng thủ), 17/6 `801C7890`, 19/8 `801C78DC`, 20/9 `801C7960` Hút máu để kết thúc, 10 `801C7BC0` Chuẩn bị phản công, 11 `801C7E1C` Đổi bên, 12 `801C7F18`, 14 `801C7FC4`, 21 `801C80C0` Đóng cửa, 22 `801C818C` Xuống, 23 `801C83CC`, 24 `801C7448`.

## 2. Thành tích tham chiến `D_800F97E0 + side × 0x1074`

`side` 0/1; chỉ số tấn công là `D_80178C78`, chỉ số phòng thủ là `D_80178B50` (s16, đổi bên và `801C7E1C` được hoán đổi cho nhau). Bảng "Người viết" sau liệt kê nội dung mà đường dẫn bản đồ `801F3578` và đường dẫn demo `8009C2DC` ghi.

| Bù đắp | Loại | Ý nghĩa | Nguồn đường dẫn bản đồ (mục chiến đấu + bù đắp) | Đường dẫn trình diễn `8009C2DC` | Đọc hiệu suất |
| --- | --- | --- | --- | --- | --- |
| +0x00 | s8 | Kỷ lục này là kẻ tấn công 0/người phòng thủ 1 | hằng số | ghi lại chỉ số | mọi nơi |
| +0x02 | u16 | Trình điều khiển **Số bản ghi khả năng** = `D_800CA9C4[人物号]` | Phiên bản trình điều khiển +2 → Bảng tra cứu | Trường minh họa 1 → Bảng tra cứu | Dòng `80222B14`, `8022245C` (danh sách dòng ROM `0x1161C0`, kích thước bước 0x24) |
| +0x04 | u16 | Số khung máy bay | Ví dụ máy bay +2 | Trường trình diễn 0 | Sprite, chia tỷ lệ `801C34D8`, `801C3F44` |
| +0x06 | s16 | **Số hiệu suất vũ khí** (chỉ số đăng ký thư viện vũ khí) | `801F3554` = `800AB470(机体, 武器)`; khi không có vũ khí thì đó là mã lý do `+0x11` | Trường trình diễn 3 | `801C410C` → `801C3D38(+6, +0x2C, 0)` Tải khối tấn công |
| +0x08 | s16 | **Mã phản ứng của người phòng thủ** (chỉ số thư viện phản ứng, −1 = đòn đánh bình thường) | `+0x26` được viết trong quyết toán; 0x14 trong quá trình cứu hộ | Trường trình diễn 4 | `801C410C` → `801C3D38(+8, +0x848, 1)` Tải khối phản ứng; `801C3E7C` xác định có nên trừ máu hay không |
| +0x0A | u8 | bản ghi lý lịch b (địa hình) | `+0x27` | trường demo 6 | `80084A78(+0xB, +0xA, side)` |
| +0x0B | u8 | bản ghi nền a (nhóm qua `D_800C5940[a]`) | `+0x28` | trường demo 5 | Tương tự như trên |
| +0x0C | u8 | Suy luận: vị trí thái độ trên không/mặt đất (chủ yếu là 1 khi +0xA=100 trong phần trình diễn) | `+0x29` | Trường trình diễn 7 | `801C4920`/`801C4940` (định vị `801C39B0`, nội dung `801C4160`) |
| +0x0D | u8 | Kích thước tệp 0–4 | `+0x2A` | Chuyển đổi bit kích thước +4 được ghi lại bởi thân ROM | Lựa chọn kịch bản quay `801C49A0` |
| +0x0E | u8 | Chia tỷ lệ Sprite (hiển thị do tôi viết) | 0 | 0 | `801C3F44` đã viết |
| +0x12/+0x16 | | Biên bản chiến đấu vũ khí cột 6/cột 3 (viết theo diễn xuất) | | | `801C3F44` |
| +0x17 | s8 | Bảng tham gia `+0x16` | | | `801C87C8`, `801C91C0` |
| +0x18 | s8 | **Lệnh Phòng thủ**: 0 Phản công, 1 Phòng thủ, 2 Né tránh (không phải 0 = không phản công) | Người bảo vệ được chuyển đổi bởi `D_8018B754`; Kẻ tấn công 0 | 0 | Trạng thái 20/9 `801C7B5C`: Không 0 → Trạng thái 21 Không có vòng phản công; Nhãn HUD `801C2FDC` (0x482/0x483/0x484) |
| +0x1A | u16 | **Thiệt hại do phía chúng tôi gây ra** | Bàn chiến `+0x14` | Khi cờ "Hạ" của đối thủ được đặt = HP của đối thủ, nếu không thì `rand(对方HP−20)+10` | `801C3E7C` |
| +0x1C | u16 | Thiệt hại mà phía chúng tôi phải gánh chịu (hiệu quả do bạn tự tính toán) | — | 10 | `801C3F44` viết = `801C3E7C(side)`; hàng trừ máu `801C8A58` đọc của người phòng thủ |
| +0x1E | u16 | Bảng tham gia `+0x18` | | 0 | |
| +0x20/+0x22 | u16 | HP tối đa/HP hiện tại | Đơn vị +6/+4 | Cả hai bản ghi đơn vị ROM +0 | Cửa sổ HP `801C2C98`; `+0x22 == 0` → Bị hạ `801C5AF4` |
| +0x24/+0x26 | u16 | EN tối đa/EN hiện tại | Phiên bản đơn vị +0xA/+8 | Cả hai bản ghi đơn vị ROM +2 | Cửa sổ HP |
| +0x28 | s8 | Khối tấn công hiện tại 0/khối phòng thủ 1 | Tấn công 0, phòng thủ 1 | Tấn công 0, phòng thủ 1 | `80222C5C` |
| +0x2C / +0x848 | 0x81C×2 | Khối hoạt ảnh tấn công/khối hoạt ảnh phản ứng (tự điền vào để biểu diễn) | | | |
| +0x1064 | u32 | Con trỏ phiên bản khung máy bay | Bảng tham gia `+4` | `&D_8016A210` (giữ chỗ) | `801E40B0` (trao đổi HP cứu hộ), `8022245C` (chỉ khi chế độ trước đó = 3) |
| +0x1068 | u16 | Bảng tham gia `+0x2C` | | 0 | `801C4A08` |
| +0x106C | u32 | Con trỏ phiên bản nội dung dành cho người chăm sóc/hình nộm | Người bảo vệ hoặc tự hoặc 0 | `&D_8016A210` | Chi nhánh hỗ trợ `801C3E7C`, `801C4AEC`, `80222B14` |
| +0x1070 | s16 | Mã phản hồi của người phản hồi, −1 Không có | | −1 | `801C3E7C`, `801C4808` |

Đường dẫn trình diễn cũng được viết là `D_80178C78 = 0`, `D_80178B50 = 1`, `D_800F9808 = 0`, `D_800FA87C = 1` (thường trú `8009C63C..8009C660`).

### 2.1 Số hiệu suất vũ khí

- `800AB470(机体号, 武器号)` (cư dân: 61973): Kiểm tra bảng thường trú `D_800CB7BC` (ROM `0x561AC`, 89 mục {weapon, body, performance number}, kết thúc bằng {0,0,0}), nếu trúng thì lấy số hiệu suất trong bảng, ngược lại **số hiệu suất = số vũ khí**. Ví dụ: (34, 7) → 38, (130, 308) → 1191. Bạn phải xem qua bảng này khi đánh giá vũ khí trên trang, nếu không vũ khí có cùng tên sẽ có hoạt ảnh sai trên một máy cụ thể.
- `801C3C9C(id, kind)` (trận chiến:1674): loại 0 → `id == 0x1000` ghi `D_80250010` bằng bộ nhớ, `id ∈ {−2, −3}` ghi `D_80222D40` bằng null và phần còn lại `801C3128(id)` (thư viện vũ khí, ROM `0x11FC80` Bảng offset + `0x184990`); loại 1 → thư viện phản ứng `801C3230`; loại 3 → thư viện nhấn `801C31E8`. `801C3D38` không được tải trực tiếp khi id == −1.
- Nội dung tên vũ khí `1370 + 武器号`, tên máy `527 + 机体号`, tên nhân vật `4382 + 人物号` (`src/host/battle_page.cpp:194-196`).

### 2.2 Mã phản ứng của hậu vệ (xác định hiệu suất của hậu vệ)

Khu định cư `801F7204` (bản đồ:59633) Nhấn "Đánh → Nhân bản → Cắt り払い → Nội dung giả → Lá chắn → Phòng thủ S" để viết biểu mẫu tham gia `+0x26` và chuyển nó vào `+8` như hiện tại. Giá trị xác nhận mã:

| Mã | Ý nghĩa | Nguồn quyết toán | bản ghi thư viện phản ứng (`assets/original-graphics/animations.json`) | Khấu trừ máu của hậu vệ |
| --- | --- | --- | --- | --- |
| −1 | Đánh thường | Mặc định | Không nạp đạn, người phòng thủ sử dụng hành động đánh mặc định là `801C49D8` | Khóa |
| 2/3/5 | I Trường lực/Lớp phủ chùm tia/Phòng thủ hành tinh **Khối** | `801F6F3C` (bản đồ:59421) | 0x2164CC (Hành vi 375 BeamShield) | Không khấu trừ |
| 4 | Bị chặn bởi rào cản hào quang | `801F7590` | Tương tự như trên | Không khấu trừ |
| 6–0xC | Bản sao: 0x20000 Getter Phantom 6, 0x1000 Mach Đặc biệt 7, 0x2000 True Mach Đặc biệt 8, 0x1 Bản sao của Chúa 9, 0x40000 Chân Phantom tức thì 0xA, 0x100000 Super Jammer 0xB, 0x10 Bản sao 0xC | `801F6C44` (bản đồ:59196) | Tất cả đều giống nhau 0x2163D0 (dư ảnh hành vi 272) | Không khấu trừ |
| 0xD / 0xE / 0x10 | I Trường lực/Lớp phủ chùm tia/Phòng thủ hành tinh **Giảm sát thương do xuyên thấu** | `801F768C..801F76C4` | 0x2164CC | Khóa |
| 0xF | Rào cản hào quang bị xuyên thủng | `801F7568` | 0x2164CC | Khóa |
| 0x11 | S Defense (Khiên) | `801F6FDC` (bản đồ:59472) | 0x2164FC (Khiên hành vi 362) | Khóa |
| 0x12 / 0x13 | Cắt り払い (vũ khí của kẻ tấn công `+0x22 & 1` được đặt thành 0x13) | `801F6D10` (bản đồ:59255) | 0x216538/0x216518 (hành vi 377, hành động 10/11) | Không khấu trừ |
| 0x14 | Hỗ trợ phòng thủ | `801F3974` | 0x2164A0 (Hành vi 367 CoverDiffence) | Người bảo vệ giam giữ (đọc `+0x106C`) |
| 0x15 | giả mạo | `801F6E3C` | 0x216568 (đăng ký 969, hành vi 103) | đã đọc `+0x106C` |
| 0x16 | Bỏ lỡ (tránh) | `801F732C` | 0x216558 (không có diễn viên, hành động phòng thủ 15) | Không khấu trừ |

Trong số 28 mục trong thư viện phản ứng, 0, 1 và 13–16 chia sẻ BeamShield, còn 0x17–0x1B và 6–0xC chia sẻ các bản ghi dư ảnh, vì vậy các loại trên màn hình thực tế chỉ có: đánh, khiên, sao chép dư ảnh, cắt × 2, khiên, hỗ trợ, cơ thể giả và tránh**.

Việc trừ máu được xác định bởi `801C3E7C` (trận chiến:1813): khi mã phản ứng là −1 hoặc 0xD..0x11, sát thương mà bên phải chịu = `min(对方 +0x1A, 本方 +0x22)`, nếu không thì là 0; 0x14/0x15 thay đổi đối với HP của cơ thể được chỉ định bởi `+0x1070` và `+0x106C`. Kết quả được `801C3F44` ghi vào `801C3F44` ở trạng thái 1 và hàng khấu trừ HP `801C8A58` (trận chiến:7385) được liệt kê theo bản ghi chiến đấu bằng vũ khí 5. Kiểm tra `D_80222E50` và chia thành nhiều nhịp. `801C8D6C` được ghi vào HP `+0x22` cho mỗi nhịp.

### 2.3 Hạ gục

Trạng thái 20/9 `801C7960` (trận chiến:6180) điều chỉnh `801C5AF4(守方, 0xA)` (trận chiến:3974) sau khi hàng trừ máu được giải phóng: khi người phòng thủ đạt tới `+0x22 == 0`, số hiệu suất vũ khí của kẻ tấn công == `0x4A6` → trạng thái 21 (không nổ), nếu không thì → **trạng thái 22 Hạ gục**; khi người phòng thủ còn sống, `+0x18 != 0` → trạng thái 21, nếu không thì vào vòng phản công (trạng thái 10). Trạng thái 22 `801C818C` Theo hồ sơ chiến đấu của máy bay cột 6 == 2, chọn đánh 156, nếu không thì kích thước `+0xD == 2` chọn 157, nếu không thì 158.

Vậy "Tiêu diệt" = `+0x1A ≥ 守方 +0x22` của kẻ tấn công và mã phản ứng thuộc loại trừ máu. Điều kiện nhánh "0x14 và 0x15" trong `801C5AF4` luôn sai, đó là mã chết.

### 2.4 Bối cảnh

`80084A78(a, b, side)` (thường trú:16807): Số bản ghi lý lịch = `D_800C5940[a] × 101 + b` (ROM `0x5BC30`, 0x26 byte), a = bản ghi tham gia chiến tranh `+0xB`, b = `+0xA`. Trạng thái 0 `801C6FE8` sử dụng phần chia của **bên tấn công**; trạng thái bắn 16/5 `801C76A0` được thay thế bằng `801C2AD0(side)` (trận chiến:343) với phần chia sẻ của **phía bên kia. Nói cách khác, **SRW64 ban đầu có một nền cho mỗi bên**, được chuyển đổi khi đòn tấn công bay sang phía đối diện, khớp với một hàng địa hình ở mỗi bên của trang đánh giá Z.

## 3. Lối vào hiệu suất độc lập ban đầu: chế độ 0x1A / 0x1C

| Chế độ | Ai đặt | Tải | Cuộc gọi đầu vào | Hành vi đặc biệt |
| --- | --- | --- | --- | --- |
| 0x1A カラオケ | tiêu đề `801C9904` (tiêu đề:6181) Nhấn A: `D_80172D08 = 歌号`, `80080188(0x1A)`, `80099814(5,1,2)` | `8007FF9C` (chỉ cài đặt `0x121560`) | `8009C1DC` (danh sách tĩnh + `80090128(歌)` bắt đầu hát karaoke), `8009C2DC(0)` | Không xây dựng cửa sổ HP và HUD (`801C7268`), không vẽ mặt nạ; vẽ lời bài hát cho từng khung hình `8009055C`; B Nhỏ dần sau khi phím hoặc bài hát được chơi; **Bắt đầu lại** khi phần biểu diễn kết thúc trong khi `D_80161310 == 1` (bài hát vẫn đang phát): `D_801613DA = (+1) mod 6` Chuyển sang bản ghi tiếp theo, `8009C2DC(0)`, trạng thái 0 |
| Trình diễn tiêu đề 0x1C | tiêu đề `801CA1C0` (tiêu đề:6805) 180 khung hình chờ: `80080188(0x1C)`, `D_80161310 = 1`, `80099814(5,1,2)` | `8007FFD0` (chỉ cài đặt `0x121560`) | `8009C2DC(1)`, bản ghi được chọn bởi `D_8018B87C` | HUD bình thường; `D_80178A08` (nhấn từ) bất kỳ phím nào khác 0 sẽ mờ dần |

(Chế độ 2 cũng cài đặt thêm ROM `0x217FD0` cho `80400000`, nhưng không có lệnh gọi trực tiếp tới `804xxxxx` trong lớp phủ hiệu suất, thường trú hoặc bản đồ. Hai chế độ demo có thể được phát mà không cần cài đặt nên có thể suy ra rằng nó không liên quan gì đến hiệu suất.)

**Bản ghi DEMO**: ROM `0x83110` bắt đầu với 42 u32 offset (19 đầu tiên = 6 cho mỗi bài カラオケ 19 bài hát, 23 cuối = 1 cho mỗi bài cho bản demo tiêu đề), mỗi bài 32 byte = 8 s16 ở mỗi bên:

```
[机体号, 人物号, 被击坠标志, 武器演出号, 反应码, 背景 a(+0xB), 背景 b(+0xA), +0xC]
```

Ví dụ: Minh họa Tiêu đề #29 `(196,145,0,778,−1,0,100,1) / (300,150,1,1165,−1,0,100,1)` Hậu vệ bị bắn hạ; #24 Mã phản ứng của người phòng thủ là 18 (cắt り払い); #26 Hậu vệ 13 tuổi (lá chắn bị xuyên thủng). Biểu tượng bị rơi được viết bằng §2 +0x1A.

Tất cả hành động dành cho `8009C2DC(arg)` (cư trú:43956): Phân bổ bộ đệm tạm thời `80089970`, ghi bản demo DMA; cho mỗi bên `8009C218` (cư trú:43902) Ghi giá trị mặc định (+0x18=0, +0x1A=`rand(3000)+10`, +0x20/+0x22=5000, +0x1070=−1, +0x1064/+0x106C=`&D_8016A210`, v.v.), DMA ROM Dành cho bản ghi máy bay (`0x71B80 + 机体×0x24`), viết các trường theo bảng §2; sau đó nhấn cờ hạ để đặt +0x1A; cuối cùng viết chỉ số tấn công và phòng thủ. **Nó không đọc danh sách, không đọc lưu, không yêu cầu bản đồ**.

**Trở về** (trận `801C98CC..801C99D8`):

- Chế độ 0x1C: `D_80161566++`, `D_801614EA++`; nếu `D_801614EA == 5` và `D_80161310 == 1` → xóa, `8007E87C(0xB4)`, **Chế độ 7 (màn hình khởi động lại)**; nếu không thì `D_80161310 != 0` → Xóa, `8007E87C(0xB4)`, chế độ 0x1E; `== 0` → `D_801614EA = 0`, `8007E87C(0xB4)`, **chế độ 0x1D**.
- Mẫu 0x1A: Bài hát kết thúc → Mẫu 0x1B.
- 0x1B/0x1D/0x1E đều nhập lớp phủ tiêu đề `801CAB50(kind)` (tiêu đề:7511), loại = 1/2/3: 1 trả về danh sách karaoke, 2 cuộc gọi `801C5F04(0)` (tiêu đề), 3 cuộc gọi `801CA27C` (suy luận: đoạn cắt cảnh trước phần trình diễn tiếp theo).

**Hủy nhấn phím**: Vòng lặp chính `801C9754..801C97B0`: mẫu 0x1A và `D_80161310==1` và `D_80178A08 & 0x4000` (B) → mờ dần; mẫu 0x1A và `D_80161310==0` → mờ dần ngay lập tức; mẫu 0x1C và `D_80178A08 != 0` → mờ dần. Đã hủy vào `D_80161310 = 0`.

## 4. Mục mở rộng hiện có cho màn hình tiêu đề

- Library/MOD là nút RmlUi của máy chủ, không phải mục menu gốc: `src/native/ui/frontend.cpp:2419``home_sync()` Ở trạng thái chính của tiêu đề 2 (PRESS START) và 3 (ring menu), vẽ `library-open`/`mod-open` (`frontend.cpp:2434`) ở góc dưới bên phải, nhấp vào Xử lý `frontend.cpp:2618/2621`, bảng được treo trên khung cửa sổ cài đặt (`library_panel()`, `frontend.cpp:1110`) và việc tiếp quản đầu vào giống như cửa sổ cài đặt. Dữ liệu được đọc từ ROM bởi `src/host/library.cpp` (bảng khung máy bay `0x71B80`, vũ khí `0x74E90`, danh sách vũ khí khung máy bay `0x7E210`, khả năng của nhân vật `D_800CA9C4`, v.v.) và các menu trên trang đánh giá cao có thể được sử dụng lại trực tiếp.
- Tiền lệ chủ nhà chuyển sang chế độ chơi từ tiêu đề: cấp độ mini được nhập trực tiếp, `src/host/game_hooks.cpp:85-98` được điều chỉnh trong ranh giới khung `resident_func_80085F30`, `800836CC(0)`, `800A5138()` và ghi số cảnh `80080188(0xC)`, `8007F510(0x800801A4,0,1)`.
- Lối ra riêng của lớp phủ tiêu đề: mỗi khung hình `801CA9CC` (title:7403) thấy quá trình mờ dần hoàn tất (`80099B30() == 3`) và thực hiện `800B6620(1)`, `800997D0`, `8008B950`, `8008DB2C`, `8008AC78(4)`, nếu `D_801CC3A3` (bắt đầu trò chơi) sau đó `800836CC(0)`, `800A5138` và chọn chế độ 7/0x11, cuối cùng là `8007F510(800801A4,0,1)`. Mô tả của カラオケ và tiêu đề là "Đầu tiên là `80080188(模式)`, sau đó là `80099814(5,1,2)`, đợi kết thúc ở đây nhé", **không điều chỉnh `800A5138`**.

## 5. Giải pháp đề xuất

**Đi theo toàn bộ đường dẫn của bản demo tiêu đề (chế độ 0x1C) và chỉ thay thế dữ liệu của `8009C2DC` bằng lựa chọn trang đánh giá cao. **

1. **Trang đánh giá cao**: Bảng RmlUi, lối vào ở cùng vị trí với Thư viện (thêm nút vào góc `home_sync` và thêm một dòng vào trang cài đặt "Chung"). Tất cả dữ liệu được đọc từ ROM và được sử dụng lại trong `library.cpp`.
2. **Bắt đầu**: Tại một khung nhất định trong khi tiêu đề vẫn đang chạy (móc ranh giới khung, cùng vị trí với cấp độ nhỏ):
- Nhạc nền tùy chọn: `8007E810(歌号)` (§6.6)
- `D_80161310 = 0`, `D_801614EA = 0`, `D_801CC3A3 = 0`
- `80080188(0x1C)`, `80099814(5,1,2)`, để `801CA9CC` của lớp phủ tiêu đề được hoàn thiện như bản gốc và bàn giao cho nhà phân phối (phương thức tương tự `801CA230..801CA250`);
- Máy chủ đặt dấu "đang đánh giá", bảng đánh giá sẽ đóng và dữ liệu đầu vào được trả về.
3. **Điền vào bản ghi tham gia chiến tranh**: Thêm gói máy chủ vào `resident_func_8009C2DC` (thêm một mục vào `NATIVE_HOOKS`, thay đổi thành `make recomp-cpu` theo cách thủ công). Khi đánh giá cao: trước tiên hãy điều chỉnh hàm ban đầu (đặt `D_8018B87C` thành 0, đảm bảo rằng nó đi qua giá trị mặc định là `8009C218`, ghi chỉ số tấn công và phòng thủ cũng như con trỏ giữ chỗ), sau đó nhấn chọn để ghi đè:
- Cả hai bên `+2 = D_800CA9C4[人物]`, `+4 = 机体`, `+0xD` theo bản ghi thân ROM +4 kích thước được chuyển đổi (giống như chức năng ban đầu `8009C490..8009C4E4`)
- `+0x20/+0x22`, `+0x24/+0x26`: ROM body HP/EN, hoặc trang đánh giá HP tùy chỉnh
- Kẻ tấn công `+6 = 800AB470 规则下的演出号`; Hậu vệ `+6` = Số hiệu suất vũ khí phản công (chỉ cần đặt bất kỳ giá trị pháp lý nào khi không phản công)
- Defender `+8` = mã phản ứng trong §2.2; Kẻ tấn công `+8` = mã phản ứng của kẻ tấn công ban đầu trong vòng phản công (−1 khi không phản công)
- Hậu vệ `+0x18`: Phản công 0; khi không phản công, 1 (HUD hiển thị "Phòng thủ") hoặc 2 ("Né tránh")
- `+0x1A` = sát thương của kẻ tấn công; bị hạ gục, ≥ `+0x22` của người bảo vệ, nếu không bị hạ gục, < it; `+0x1A` của người phòng thủ = sát thương phản công, nguyên tắc tương tự xác định xem kẻ tấn công ban đầu có bị hạ gục hay không.
- Cả hai bên `+0xB/+0xA/+0xC` = nền (§6.5)
- Bản trình diễn đã được gieo hạt lại trước khi gọi `8009C2DC(1)`. Nếu bạn muốn các dòng giống nhau mỗi lần, bạn có thể sử dụng một hạt giống cố định ở cuối gói để gieo hạt lại `800821B0`.
4. **Trở lại**: `D_80161310 == 0`, sau chế độ biểu diễn 0x1D → `801CAB50(2)` quay lại tiêu đề; người dẫn chương trình nhìn thấy dấu "Đánh giá cao" và trạng thái chính của tiêu đề quay trở lại mốc thời gian rõ ràng 2/3 và mở lại bảng đánh giá cao (giữ lại lựa chọn cuối cùng).
5. **Hủy**: Bất kỳ phím nào (`D_80178A08 != 0`) ở chế độ 0x1C sẽ mờ dần, giống như "nhấn phím bất kỳ để quay lại". Việc hủy bỏ X hiện tại (`battle_animation_probe.hpp`, được đặt ở trạng thái 21) cũng sẽ hoạt động; Tính năng phát lại phía bản đồ của nó (trạng thái 24 trạng thái phụ 4) sẽ không được kích hoạt do không có lớp phủ bản đồ. Nếu muốn cho phép nhấn A để tiến dòng mà không thoát ra, bạn cần chặn phán đoán 0x1C+ trong gói `801C9710` (ví dụ: chỉ xóa tạm thời `D_80178A08` trước khi gọi phần `801C9778`) và đợi máy thực tế xác nhận từ nào được đọc khi A tiến dòng.

**Tại sao không sử dụng các phương pháp khác**:

- Cấp độ nhỏ ẩn: Bạn cần cài đặt bản đồ, đơn vị và tập lệnh, đồng thời bạn cũng cần chạy giải quyết bản đồ và `801FCA78` để viết danh sách. Cuối cùng, bạn phải ghi đè lên thỏa thuận giải quyết để buộc nó thực hiện; và phải mất hơn mười giây để vào và ra.
- Chuyển trực tiếp sang chế độ 2: Sử dụng được nhưng `801C9BD4` không điền vào hồ sơ tham chiến ở chế độ 2 (chủ nhà phải ghi trước khi chuyển đổi). Cuối cùng, nhấn `D_8015DD60` để chọn 0xB/0x10 (quay lại bản đồ). Bạn phải sử dụng một hook khác để thay đổi chế độ quay lại; Việc hủy bỏ Z+START sẽ chuyển sang `800A5138` → Chế độ 7/0x11. Đường dẫn trở lại cho 0x1C đã sẵn sàng.
- Chế độ カラオケ 0x1A: Không có cửa sổ HP và HUD, ngoài ra còn có thể vẽ lời bài hát và chơi karaoke nên không phù hợp.

**Các kho lưu trữ và bảng phân công sẽ không được chạm vào**: Đường dẫn này không điều chỉnh `800A5138`, không chạy bản đồ và không điều chỉnh bất kỳ quy trình ghi SRAM nào; màn trình diễn chỉ ghi vùng hồ sơ chiến đấu và BSS của riêng nó. Chỉ `800F97E0..800FA868` được máy chủ viết lại.

## 6. So sánh trang đánh giá Z (`assets/reference/battle-viewer-zsp.jpg`)

Hình ảnh tham khảo: "phản công" bên trái (phản công/hậu vệ), "tấn công" bên phải, hoán đổi △ ở giữa; mỗi bên: hình lớn của máy + hình đại diện, tên máy, tên phi công, tên vũ khí (có thẻ như TẤT CẢ), "HIT: Screen Through Defense ＜★★＞", hàng địa hình "Track Elevator (4)"; dưới cùng ♪ Hàng BGM, thanh giải thích, nút "Bắt đầu trận chiến"; menu bật lên Cài đặt dự án/Cài đặt BGM/Rung/Kết thúc.

| Kiểm soát Z | SRW64 có | Làm thế nào để |
| --- | --- | --- |
| Tấn công/Đảo ngược, △ hoán đổi | Có: hai kỷ lục trận chiến, `D_80178C78`/`D_80178B50` xác định ai tấn công trước | Hoán đổi = hoán đổi lựa chọn của cả hai bên, bên tấn công được cố định ở bên 0 khi ghi biên bản |
| Cơ thể, phi công | Có: `+4`, `+2` (số bản ghi khả năng). Driver chỉ ảnh hưởng đến các dòng (`80222B14`, kiểm tra ROM `0x1161C0` theo số bản ghi khả năng) và HUD | Có thể chơi bất kỳ sự kết hợp nào; những dòng không khớp với tổ hợp ban đầu vẫn là dòng chung của tài xế |
| Vũ khí (thẻ như TẤT CẢ) | Có: `+6`. SRW64 không có TẤT CẢ đòn tấn công/hỗ trợ tấn công (chỉ hỗ trợ phòng thủ) | Danh sách dựa trên bảng vũ khí cơ thể; các thẻ có thể tiếp tục sử dụng thẻ lưới/chụp/P/B/MAP của Thư viện. TBD nếu chương trình của MAP Arms sẽ được phát trực tuyến tại đây |
| Vũ khí của bên phản công, có nên phản công | Có: Hậu vệ `+6`, `+0x18` | Khi "Không phản công" `+0x18` Chọn 1 (phòng thủ) hoặc 2 (né tránh), chỉ thay đổi nhãn HUD |
| Dòng HIT "Phòng thủ thâm nhập màn hình" | Tương ứng một phần: màn hình = lá chắn bị chặn (mã 2/3/4/5); Xuyên giáp = lá chắn bị xuyên thủng để giảm sát thương (0xD/0xE/0xF/0x10); Phòng thủ = Phòng thủ S (0x11, lá chắn). Ngoài ra còn có những thứ không được liệt kê trong Z: miss (0x16), dư ảnh nhân bản (0xC), bị cắt ra (0x12/0x13), viện trợ (0x14), thân giả (0x15) | Thực hiện một lựa chọn duy nhất "Phản ứng của người phòng thủ": đánh/tránh/nhân bản/cắt/khiên/chặn khiên/phá vỡ khiên; hỗ trợ và avatar yêu cầu máy chủ tạo một phiên bản khác của máy, vì vậy đừng làm điều đó (§7) |
| Thiệt hại ＜★★＞ | SRW64 không có phân loại, sát thương là con số: `+0x1A` cho kẻ tấn công và lượng máu trừ đi chia theo vũ khí | Thay đổi nó thành một giá trị bằng số hoặc ba cấp độ "chấn thương nhẹ/chấn thương nặng/suy nhược" (chuyển đổi theo HP của người phòng thủ); một công tắc riêng cho "xuống" trực quan hơn |
| Có nên bắn hạ | Có: `+0x1A ≥ 对方 +0x22` → Trạng thái 22, kịch bản vụ nổ 156/157/158 Chọn theo nội dung | Công tắc; vũ khí 0x4A6 Không bao giờ phát nổ (quy tắc gốc) |
| Địa hình "Đường thang máy (4)" mỗi bên | Có: `+0xB/+0xA` (+0xC) mỗi bên, chuyển sang bên kia khi bắn | Một menu nền ở mỗi bên; xem tên bên dưới |
| ♪ Nhạc nền | Lớp phủ hiệu suất không chọn bài hát: lớp phủ toàn bộ không gọi `8007E810`, chỉ gọi `8009003C(0/1)` (suy ra rằng các kênh hiệu ứng âm thanh ở cả hai bên đều bị dừng). Trong game bình thường, bài hát được phát trong trận chiến là bài hát được phát trước khi vào trận (được coi là bài hát cấp độ) | Người chủ trì chơi `8007E810(歌号)` trước trận chiến; danh sách bài hát sử dụng 49 bài hát với tựa đề サウンドセレクト (`D_801CB290`) và tên bài hát vẫn bằng tiếng Nhật |
| Rung | Hỗ trợ gói rung cho SRW64 chưa được nghiên cứu | Chưa xong |
| Cài đặt dự án/Kết thúc | Phía chủ nhà | Menu RmlUi |
| Cột mô tả, bắt đầu trận chiến | Bên chủ nhà | |

### 6.5 Cách chọn nền

Có khoảng 2366 bản ghi nền hợp lệ (`D_800C5940` 32 nhóm × 101) và không có tên nào được tạo sẵn. Gợi ý: ① Sử dụng `check_battle_backgrounds.py` ngoại tuyến để hiển thị hình thu nhỏ cho mỗi mục được sử dụng (a, b); ② Đặt tên cho bản đồ “chương nào sử dụng” - `+0xA/+0xB`. Đường dẫn bản đồ xuất phát từ bàn chiến đấu. `+0x27/+0x28`, được viết theo cốt truyện, có thể được suy ra tĩnh từ dữ liệu bản đồ của từng tập (cần thực hiện); ③ Đầu tiên, đưa ra một bảng chung được chọn thủ công (vũ trụ, thành phố, biển, căn cứ, không khí b=100, v.v.) và đặt tất cả các danh sách vào "Thêm".

### 6,6 Nhạc nền

`8007E810(歌)` bắt đầu phát nhạc (karaoke của `80090128` cũng được truyền qua đó); chế độ 0x1C trở lại khi `8007E87C(0xB4)` (suy luận: tắt dần nhạc). Do đó, bài hát đã chọn sẽ được phát trước khi trận chiến đánh giá cao bắt đầu và phiên bản gốc sẽ mờ dần khi quay lại tiêu đề.

### 6.7 Điều kiện vũ khí BGM chiến đấu nguyên bản và gương Shisui (tĩnh)

2026-10-03 Phân tích tĩnh (tháo gỡ `build/recomp/cpu-scan/load_000AB160/rom_801C2600.text.s`, thường trú `build/recomp/disasm/cpu-main`, bảng được giải mã trực tiếp bằng ROM), không phải máy thực. "Xác nhận" = mã và dữ liệu đã được đọc; "suy luận" = ngữ nghĩa hoặc thời gian chưa được tuân theo.

**Sửa §6 bảng ♪ Hàng BGM**: Bài hát chiến đấu không phải là "bài hát cấp trước khi vào trận". Đúng là lớp phủ biểu diễn không chọn bài hát, nhưng lớp phủ bản đồ đã thay đổi bài hát chiến đấu sau khi trận chiến kết thúc và trước khi chuyển sang biểu diễn (đã xác nhận).

#### Chức năng phát và chọn bài hát

- `8007E810(歌号)` (xác nhận): không làm gì khi số bài hát bằng bài hát hiện tại `D_800FFA6C` (bài hát tương tự sẽ không được khởi động lại); số âm → `80077B38` dừng, `D_800FFA6C = -1`; nếu không thì `80077868` bắt đầu và được ghi vào `D_800FFA6C`.
- **Lựa chọn trận chiến = `801E085C(句柄A, 句柄B, 单方)`** (đã xác nhận). Tay cầm được chia thành (trại, slot) thông qua `801E510C`: `0x42–0x5F` phe ta 0, `0x60–0x7D` địch 1, `0x7E` bắt đầu từ bên thứ ba 2; Phiên bản nội dung = `D_8015E10C[阵营×0x258 + 槽×0x14]`, số nội dung = phiên bản `+2`, phiên bản chính = phiên bản `+0x38`, số ký tự = trình điều khiển `+2`. Cuối cùng, `801E07C4(ROM 地址, 模式)`: Chế độ 0 sử dụng `80089970` để mượn bộ đệm, `8007F704` đọc 2 byte từ ROM làm số bài hát; chế độ 1/2/3 đặt trực tiếp `0xD`/`0xB`/`0xA`.
- Người gọi (xác nhận): `801C90F4` (`801F7D6C(攻, 守)` ngay sau khi giải quyết `801E085C(攻, 守, 0)`; được gọi bởi `801C9604`, `801CD664`), `801D3140` (`801D3240`: `D_80172EE2` Đơn vị hành động so với mục tiêu, một bên = 0), `80211DA4` (tập lệnh `3D49` chiến đấu cưỡng bức, `80212154`, một bên = 0), `801D3278` (`801D33A0`, một bên = 1, chức năng tương tự như giải quyết một lần `801FE068`, được suy ra là Vũ khí MAP/hành động đơn phương), `8020ECE0` (`8020EE3C`, đơn phương = 1, không theo đuổi mục đích). Vì bài hát được chọn trong quá trình lập bản đồ nên bài hát cũng sẽ bị thay đổi khi tắt hoạt ảnh trận chiến (suy luận, không thực tế).

#### Quy tắc (xác nhận)

Chế độ hai bên (một bên = 0), theo thứ tự:

1. Số ký tự thí điểm chính của A hoặc B là **33–35 (0x21–0x23: ヴァル＝ア, アヴィ＝ルー, ジェイ＝レン)** → Bài hát `0x22` "Chiến binh đói khát điên cuồng", bất kể các điều kiện khác.
2. Ngược lại **A là phe của chúng tôi** → sử dụng A; **nếu không B là phe của chúng tôi** → sử dụng B. Tức là, chỉ cần một trong các bên là phe của chúng tôi, bài hát của đài chúng tôi sẽ được phát, bất kể tấn công hay phòng thủ - các đơn vị của chúng tôi bị đánh bại trong giai đoạn địch vẫn sẽ phát bài hát chủ đề của riêng họ.
3. Không bên nào là phe ta (địch vs bên thứ ba) → Sử dụng bài hát **bề mặt** của A.

Chế độ đơn phương (Đơn phương = 1) chỉ nhìn vào A, không có bước 1: Bên ta → Bên ta quy định bên dưới; Không phải phe chúng tôi → Bảng đơn vị.

**Bài hát của đơn vị chúng tôi**: Đọc thí điểm chính `+0x1C` (bitmap tinh thần, bit 30/31 = Trạng thái Siêu chế độ/Shisui/V-MAX, xem phần [battle-formulas.md](../gameplay/battle-formulas.md) Siêu chế độ).

- `+0x1C & 0xC0000000` là 0 → **Bảng ký tự** (theo số ký tự).
- Mã cứng số máy khi cài đặt: Máy 2 (ゴッドガンダムH)→ `0xA` "Mikyo Shisui"; 4/10/12/14/16 (シャイニング／マックスター／ローズ／ドラゴン／ボルト dạng S)→ `0xB` 「đốt phần trên của câu chuyện」; 270/273/2 77／278（ニューレイズナー、レイズナー、ガッシュラン、ザカール）→ `0xD` "V-MAX"; các đơn vị khác (chẳng hạn như Maxi S 28, ノーベルガンダムB 7, hạm đội thiết giáp hạm và chuông bạc chỉ đặt ở mức 30) → vẫn sử dụng bảng ký tự.
- Chúng tôi không bao giờ kiểm tra bàn máy; kẻ thù và bên thứ ba không bao giờ kiểm tra bảng ký tự.

**Không** nhánh dựa trên các biến cốt truyện, cấp độ và dấu hiệu Boss (`801E085C` chỉ đọc các trường trên); biến Mingjing Zhishui 45 không ảnh hưởng đến việc chọn bài hát và bài hát "Mingjing Zhishui" chỉ theo dạng H (bit 30).

#### Hai bảng (xác nhận)

| bàn | ROM | chỉ mục | mục | mô tả |
| --- | --- | --- | --- | --- |
| Bài hát nhân vật | `0x7D6A0` | Số ký tự 0–360 | s16 × 361, đến `0x7D971`, theo sau là 0 | 63 vật phẩm là −1 (lính, NPC, nhân vật không sử dụng; đặt −1 = dừng chơi). Phạm vi giá trị −1, 1–9, 12, 14–29, 34, 37 |
| Bài hát khung máy bay | `0x7DF30` | Số máy bay 0–362 | s16 × 363, tới `0x7E205` thì 10 byte 0, `0x7E210` trở đi là bảng vũ khí khung máy bay | Không −1. Phạm vi giá trị 1–12, 14–23, 25–29, 34 |

Ví dụ về đặc điểm kỹ thuật:

| Đối tượng | Bảng | Số bài hát | サウンドセレクト Hàng: Tên bài hát |
| --- | --- | --- | --- |
| Đơn vị 1 ゴッドガンダム | Đơn vị | 4 | 3：BAY TRÊN BẦU TRỜI |
| Cơ thể 2 ゴッドガンダムH | Nội dung (bên mình sử dụng mã cứng, giá trị như nhau) | 10 | 9: Gương Shisui |
| Cơ Chế 97 ザクⅡ | Cơ chế | 1 | 0: 兰の中で光いて |
| Đơn vị 196 コン・バトラーV | Đơn vị | 20 | 19:コン・バトラーVのテーマ |
| Đơn vị 50 νガンダム | Đơn vị | 7 | 6：メインテーマ |
| Nhân vật 4 ドモン | Nhân vật | 4 | 3: BAY TRÊN BẦU TRỜI (đổi thành `0xA` khi ở dạng H, `0xB` khi ở dạng S) |
|Nhân vật 36 アムロ|Nhân vật|7|6：メインテーマ|
|Nhân vật 70 シャア |Nhân vật | 7 | 6：メインテーマ |

Do đó, "アムロ của chúng ta chiến đấu với ザクⅡ của kẻ thù" và "ザクⅡ của kẻ thù chiến đấu với アムロ của chúng ta" đều đặt メインテーマ; khi ザクⅡ của địch chiến đấu với bên thứ ba, hãy đặt "岚の中で光いて". Được nhóm theo tác phẩm: bảng ký tự 2 = dòng Z, 3 = dòng ZZ, 8 = dòng W, 37 = "Bạn đi đâu từ đây?" (レジスタンス, ゲリラ, v.v.); bảng body 12 = tất cả các dòng レイズナー (bao gồm cả máy bay địch), v.v., có thể được giải mã trực tiếp theo bảng trên.

#### Số bài hát → サウンドセレクト OK (xác nhận)

Lớp phủ tiêu đề `load_0010DA50` (VRAM `801C4500` = ROM `0x10DA50`) của `D_801CB290` trong ROM `0x1147E0`, 49 × {văn bản số u16, số bài hát u16}; số văn bản 232–280 liên tiếp, tên bài hát = văn bản 232 + Số dòng. Số bài hát và số dòng:

- bài hát `0x01–0x20` → hàng = số bài hát − 1 (hàng 0–31);
- Bài hát `0x30`, `0x31` → Dòng 32, 33 (日こそ我が时、明あるlimitり);
- bài hát `0x21–0x2F` → hàng = số bài hát + 1 (dòng 34–48).

Mỗi số bài hát xuất hiện trong hai bảng chiến đấu đều nằm trong 49 hàng này nên trang đánh giá có thể trực tiếp dùng bảng này để làm tên bài hát (tìm kiếm ngược: tìm kiếm các hàng trong bảng theo số bài hát). Bảng カラオケ `D_801CB354` (ROM `0x1148A4`, 19 mục) là một tập hợp con.

#### Các điểm thay đổi đường cong khác trên bản đồ (đã xác nhận, sử dụng phần suy luận)

- **Bài hát cấp = bản ghi tài nguyên bản đồ `+0xB`**: `D_80219B27 + 地图号×12`, tức là ROM `0x10267C + 地图号×12 + 0xB` (bản ghi có "byte cuối cùng được diễn giải" trong [thư mục dữ liệu gốc](../data/original-data-catalog.md)). 158 ảnh chỉ sử dụng `0x23`, `0x2A–0x2F`. Đặt ở đâu: Mục nhập chiến thuật `801E028C` (chế độ 0x11, v.v.) / `801E0350` (chế độ 0x16), **Bắt đầu mỗi giai đoạn** `801FA88C`, `801C7798` (sau khi chờ 60 khung hình cho một trạng thái nhất định), `801E076C` (xem bên dưới).
- **Các bài hát cấp độ sẽ không được khôi phục sau chiến tranh**: Bản đồ trả lại hiệu suất ở chế độ 0xB → `8008029C` → `801E0268` → `801E00AC(1)` và toàn bộ quá trình sẽ không điều chỉnh `8007E810`. Do đó, bài hát chiến đấu vẫn còn trên bản đồ cho đến khi bắt đầu màn tiếp theo (`801FA88C`) hoặc bài hát được thay đổi trong trận chiến tiếp theo (suy ra nhận thức về cơ thể của người chơi, xác nhận đường dẫn mã).
- Tập lệnh `3D3A` đặt BGM (`8009F9D0`: tham số 0 → `8007E87C(0xA)` mờ dần, nếu không thì `8007E810`).
- `3D45` xuất hiện `8020C524(0)`: không phải lượt đầu tiên, `D_802237F5 ≥ 2` (nghĩa là không bị truy đuổi), tay cầm ngoại hình hiện tại `D_802272E0` được thả ra khi nó thuộc về kẻ địch `0x26` 「これが実力か」(suy ra là tiếng leng keng tiếp viện của địch); mọi khung hình `801E076C` nhận thấy rằng bài hát hiện tại là `0x26` và `80077AD0()` trả về 0 (suy luận: bài hát đã được phát) rồi chuyển về bài hát cấp độ.
- Các bài hát cố định khác: `801C72C8` phát `0x27` "いざ戦わん" (suy ra sự chuẩn bị xuất kích); `801DF444``0x28`, `801DF8A8``0x18`, `801DF280`/`801DF5BC`/`801DFD04``8007E810(-1)` đầu tiên dừng (kết thúc/kết thúc trò chơi, không theo đuổi); `802176A8(k)` nhấn k để phát `0x14`／`6`／`0xE`／`0x17` Sau khi cắt chế độ 6, `80212CC0` mờ dần hoặc phát `0x17` theo thông số (không theo đuổi mục đích).

**Gợi ý sử dụng trang đánh giá**: Bài hát mặc định được tính theo quy tắc ban đầu - nếu có người chơi thân thiện thì lấy bài hát của nhân vật phi công chính của đơn vị chúng tôi (nếu chọn dạng H/S/V-MAX thì dùng bài hát mã cứng ở trên), nếu không thì lấy bài hát cơ thể của kẻ tấn công; nếu có ba người có mặt thì bài hát mặc định sẽ là `0x22`.

#### Ý nghĩa ROM vũ khí `+8` (kỹ năng bắt buộc) = 2 (đã xác nhận)

- Copy: `800A6A68` Ghi bản ghi ROM vũ khí `+8` vào instance vũ khí **`+0xF`** (kích thước bước instance 0x24; ROM `+0xF` byte gắn cờ vào instance `+0x22`, không trộn lẫn cả hai).
- Nhận định: **`801E6214(阵营, 主驾驶员, 武器实例, 机体实例, 跳过消耗检查)`** trả về 0 sẵn có, 1 kỹ năng cần thiết chưa đạt, 2 không đủ năng lượng (`+0xE` > phi công `+0x20`), 3 không đủ EN (`+0xD` > cơ thể `+8`), 4 số đạn. 0 (`+0xC ≠ −1` và `+0xB == 0`); kỹ năng cần thiết được đánh giá đầu tiên. Người gọi `801E6410` (danh sách vũ khí trang trạng thái `801E6650`, chi tiết `801E6B0C`), `801F8B38`/`801F8DB0` (`801F8BA0`/`801F8EB8`), `80200530` (`802008E0`), `80201D98` (`80201E68`), tất cả được truyền vào phần thân `+0x38` là **trình điều khiển chính**.
- `+0xF` Nhấn bảng nhảy `jtbl_8021EBF0` (17 mục, giá trị chỉ số −1):

| Giá trị | Điều kiện (trả về 1 nếu không đáp ứng) | Hiển thị văn bản (0xFBA + giá trị) | Vũ khí sử dụng trong ROM |
| --- | --- | --- | --- |
| 0 | Không có | — | Hầu hết |
| 1 | Phe = 0 (chỉ có chúng tôi mới có thể sử dụng) | Không hiển thị (chi tiết sẽ chỉ được hiển thị khi ≥2) | 79 Mandala Formation·Jiyue Rebirth |
| **2** | **Phi công chính `+0x1C` bit 30 (`0x40000000`) đã được đặt** | "Đinh Kinh" | **15–19** |
| 3 | Tương tự như 2 | "HP" | Không có |
| 4 | Tương tự như 2 | "Sモード" | 30, 53, 62, 71, 76 (Dạng liên minh 4 cỗ máy S giữa liên minh SャャイニングS và liên minh Sシャッフル) |
| 5–11 | Trình độ lái xe `+5` ≥ 10/15/20/25/30/35/45 | 「LV10」… 「LV45」 | 150–159, 1177–1183, 1219, v.v. |
| 12／13 | Kỹ năng `+0x36 & 0x18` (NT hoặc Thế giới con người nâng cao) và cấp độ `+6` ≥ 1/4 | "NT1" "NT4" | ファンネル danh mục／ファンネルDanh mục MAP |
| 15/14 |
| 16 | Bit 30 | "V-MAX" | Không có |
| 17 | Vị trí 31 (V-MAX Red Power) | "V-MAX" | Không có |

- **Vậy `+8 = 2` chỉ yêu cầu bit trạng thái của trình điều khiển chính là 30**, mã giống hệt như `4` (Sモード), `16` (V-MAX), "Dingjing" chỉ hiển thị văn bản. **Không đọc** Vẽ biến số 45. Không đọc `800A4BB8`, và không nhìn vào sức mạnh hay kỹ năng. `800A4BB8` Chỉ có ba người gọi trong ROM đầy đủ, `load_0008F4B0:801CA27C`, `801E59D0` và `801E5BE8`, tất cả đều chỉ thêm dòng chữ "Ding Jing Shisui" vào thanh kỹ năng ドモン; không có biến nào để đọc trong `801FF1BC`/`801FEDF4`.
- Nguồn bit 30: `801FF1BC` (được gọi bởi `801D61C8`, `801D92E4`) cho ドモン (vàアルゴ, サイ・サイシー, ジョルジュ,チボデー; Eastern Undefeated Any camp) Vigor ≥ 130 → `801FEDF4`: Trong bảng biểu mẫu `D_80218A34` (ROM `0x101594`, dòng 0 = {1, 2}) tìm phần thân hiện tại, thay đổi số phần thân thành dạng nâng cao và đặt bit 30. Đối với Vì vậy, bước này là 1 → 2 (H). Bit 30 chỉ bị xóa trong quá trình xử lý sự cố `801FF4E0` và không bị xóa trở lại khi có lực tác dụng.
- Ngoài ra, các ô mẫu vũ khí 15–19 trong bảng vũ khí cơ thể (`0x7E210`) chỉ dành cho cơ thể 2 và danh sách cơ thể 1 ban đầu không chứa 5 vật phẩm này; vị trí 30 là cửa thứ hai. Tác dụng thực tế: **Khả năng lái và sức mạnh của **ドモン chỉ có thể được sử dụng sau khi nó tự động chuyển thành H**, và không liên quan gì đến biến cốt truyện "Shisui Shisui" 45 (45 chỉ xác định văn bản trên thanh kỹ năng và dòng sát thủ của Liên minh シャッフフル, xem [hidden-elements.md](../gameplay/hidden-elements.md) §5.1). Các ngưỡng sức mạnh tiếp theo như thường lệ: 15 không, 16/17 ≥ 110, 18 ≥ 130, 19 ≥ 150 (ROM `+7`).
- Đối với trang đánh giá cao: đường dẫn hiệu suất không được điều chỉnh thành `801E6214`. Bạn có thể điền trực tiếp vào ô 15-19 cho bản ghi tham chiến mà không cần lo lắng về vị trí 30 (suy luận: lớp phủ hiệu suất không đọc trường này).

## 7. Rủi ro và hạn chế

- **Aid (0x14) và False Body (0x15)**: `801C3E7C`, `80222B14`, `801E40B0` sẽ đọc phiên bản khung máy bay thực thông qua `+0x106C` (và con trỏ phi công `+0x38` của nó); trong bản demo, hai con trỏ này trỏ tới phần giữ chỗ `D_8016A210`, nội dung không được đảm bảo là hợp lệ. Để thực hiện việc này, máy chủ phải tạo một phiên bản nội dung trong bộ nhớ trống (+4/+6 HP, +8/+A EN, +0x38 điểm cho phiên bản trình điều khiển đã tạo, trình điều khiển +2 = số ký tự). Không có sẵn trong phiên bản đầu tiên.
- **`8022245C`dòng điều kiện**: 0x1388–0x2710 Phần này (cụ thể theo cấp độ, người yêu thích, v.v.) chỉ được đánh giá ở chế độ trước `D_8015DD60 == 3` (bản đồ) và sẽ được hiểu là `+0x1064 → +0x38`; khi xem chế độ tiêu đề, phần này bị bỏ qua và chỉ hiển thị những dòng chung - an toàn, nhưng không hoàn toàn giống với những dòng trong câu chuyện chính.
- **Bản đồ chống đỡ của Khiên và Kiriruり払い**: Bản ghi phản hồi cho thấy số đăng ký diễn viên vào ngày 18/17/19 là 17 (có thể suy ra rằng các bộ phận khiên/kiếm được lấy dựa trên tập bản đồ địa phương). Việc chọn hai vật phẩm này cho máy không có khiên/kiếm có thể dẫn đến các bộ phận trống hoặc sai. Trang đánh giá chỉ nên được cung cấp khi máy bay có khe cắm thiết bị tương ứng (bản ghi ROM máy bay +0x18 khe cắm thiết bị, Thư viện đã giải quyết "lá chắn").
- **Phím**: Chế độ 0x1C, bất kỳ phím nào bị hủy; chạm vào joystick trên Deck không tính, tùy vào nguồn `D_80178A08`, đợi máy thực tế xem nhé.
- **RNG**: Đánh giá không ảnh hưởng đến bất kỳ nội dung lưu nào; lựa chọn dòng thay đổi theo số khung, cố định hạt giống nếu cần thiết (§5 bước 3).
- **Cùng tồn tại với X abort hook**: `battle_animation_probe.hpp` bị treo trong `801C9710`, việc đánh giá cao không cần logic phía bản đồ của nó; xác nhận rằng nó không đọc các biến bản đồ như `D_80172EB0` khi không có lớp phủ bản đồ.
- **Thay thế HD**: Các cảnh biểu diễn được vẽ trong cùng bối cảnh với câu chuyện chính và việc thay thế HD của kết cấu phần thân, phần cắt và kết cấu mặt đất sẽ có hiệu lực một cách tự nhiên.
- **Màn hình rộng**: `battle_hud.cpp` Logic lớp phủ có hiệu lực theo lớp phủ hiệu suất, không phụ thuộc vào bản đồ và không cần thay đổi suy luận.

## 8. Xác nhận và suy luận mã

Xác nhận mã:

- Bảng chế độ, chức năng tải và vào chế độ 2/0x1A/0x1C (cư trú:11582, `jtbl_800CFEC8`)
- `8009C2DC`/`8009C218` Điền vào tất cả các trường của bản ghi và thể hiện định dạng bản ghi (cư trú: 43902-44200, ROM `0x83110` đã giải được 19×6 + 23 mục)
- Cài đặt tiêu đề 0x1A (title:6181) và 0x1C (title:6805), thoát tiêu đề (title:7403), quay lại mục `801CAB50` (title:7511)
- Đọc hiệu suất `+6/+8` hoạt ảnh đã chọn (trận chiến:2011 `801C410C`), chuyển hướng `801C3C9C`, ánh xạ số hiệu suất của `800AB470` và bảng `D_800CB7BC`
- Bảng đầy đủ các mã phản ứng và nguồn giải quyết (bản đồ:59196–59633), điều kiện trừ máu của `801C3E7C`, nhánh hạ gục của `801C5AF4`, điều kiện phản công của `801C7B5C`
- Chuyển đổi nền theo bên (`801C6FE8`, `801C76A0` → `801C2AD0`)
- Lớp phủ hiệu suất không được điều chỉnh `8007E810`

Suy luận:

- Ý nghĩa của `+0xC` (bit trống), mục đích của `+0x17/+0x1E/+0x1068`
- `801CAB50(2)` là quay lại menu PRESS START/ring; `8007E87C(0xB4)` là làm nhỏ dần nhạc; `8009003C` là dừng kênh hiệu ứng âm thanh
- Khiên/cắt, diễn viên ép máy để lấy phần chống đỡ
- Nhạc nền trong trận chiến thường là bài hát trước khi vào trận.
- Lớp phủ bổ sung cho `80400000` không liên quan gì đến chương trình

## 9. Được xác minh trên máy thật

1. Ở trạng thái chính của tiêu đề 2/3, máy chủ sẽ gọi `80080188(0x1C)` + `80099814(5,1,2)` xem hiệu suất có thể được nhập rõ ràng hay không (liệu trạng thái phụ tiêu đề có nên nâng cao như `801CA254` hay không, nếu không, tiêu đề vẫn sẽ phản hồi với đầu vào trong khoảng thời gian mờ dần).
2. Sau khi gói `8009C2DC` bị ghi đè, mọi tổ hợp (khung máy bay, trình điều khiển, vũ khí) có thể chơi bình thường không? Chọn một số vũ khí thuộc phạm vi `D_800CB7BC` để kiểm tra hoạt ảnh.
3. Màn hình hiển thị từng mã phản ứng: nhấn, 0x16, 0xC, 0x12, 0x13, 0x11, 2/4 (chặn), 0xD/0xF (xuyên); đối với máy không có khiên/kiếm, hãy chọn 0x11/0x12.
4. Đã bị hạ: `+0x1A ≥ +0x22` Trạng thái tăng thời gian 22, ba kịch bản vụ nổ; vũ khí 0x4A6 không nổ.
5. Vòng phản công: Khi phản công, `+0x18 = 0`, `+8` của người tấn công ban đầu và `+0x1A` của người phòng thủ đúng như mong đợi; khi `+0x18 = 1/2`, nhãn HUD.
6. Chuyển đổi thời gian giữa các nền khác nhau ở cả hai bên.
7. Bạn sẽ dừng lại ở màn hình tiêu đề nào sau khi quay lại chế độ chạy 0x1D? Chủ nhà có thể mở lại trang đánh giá ở đó không? Có bất kỳ rò rỉ tài nguyên nào (khe elf, thẻ heap 4) khi chơi hơn mười trò chơi liên tiếp không?
8. BGM: Bài hát `8007E810` trước chiến tranh có được phát liên tục trong suốt buổi biểu diễn hay không và có bị nhỏ dần khi quay lại hay không; liệu kênh hiệu ứng âm thanh trong quá trình biểu diễn có làm gián đoạn âm nhạc hay không.
9. Việc nhấn A để chuyển tiếp dòng ở chế độ 0x1C có tương đương với việc hủy bỏ hay không; X/R2 hủy bỏ hiệu suất của hook trong đường dẫn này.
10. Màn hình rộng, thay thế HD và lớp phủ văn bản giao diện (tên nội dung cửa sổ HP) có bình thường trong đường dẫn demo không?

### 9.1 Thử nghiệm thực tế nguyên mẫu (2026-10-03)

Nguyên mẫu máy chủ đã được kết nối: `resident_func_8009C2DC` bao bì (`NATIVE_HOOKS` → `srw64_original_demo_battle_fill`, `game_hooks.cpp`), móc ranh giới khung `viewer_start`, `src/host/battle_viewer.cpp` (lệnh gỡ lỗi `viewer.start`: các trường ban đầu của hồ sơ chiến đấu ở cả hai bên được ghi, trạng thái là `status.battle_viewer`). Tập lệnh kiểm tra ghi lại (ROM `0x71B80 + 机体×0x24`: HP, EN, bit kích thước) và các trường tính toán `D_800CA9C4[人物]` theo nội dung. Kết luận:

- Mục 1, 2 và 7 đã đạt: menu vòng tiêu đề không hoạt động (giới thiệu chính 3 / trạng thái phụ 2, `D_801CC3A6` 2/3) chế độ chuyển đổi thời gian mục nhập sạch 0x1C; ghi đè có hiệu lực sau khi phiên bản gốc được điền vào (ゴッドガンダム "石波ラブラブ天星剑" 1216 Play ザクⅡ, cut-in 1023, HD frame normal); sau khi biểu diễn quay lại màn hình tiêu đề "Vui lòng nhấn phím START" (không phải menu chuông), không có bất thường nào trong 9 trường liên tiếp và sau đó `previous_mode` là 0x1D. Sau khi quay lại tiêu đề, hãy để tiêu đề đó trong khoảng 6 giây và phiên bản gốc sẽ tự bắt đầu trình diễn ở chế độ chờ. Vui lòng chặn nó khi trang đánh giá cao được mở.
- Mục 3 và 4: Đánh (sát thương chia theo điểm máu), tránh 0x16, phân thân 0xC văn bản ("Bản sao" + dư ảnh), Phòng thủ S 0x11 ("Khiên phòng thủ", α・アジール không có khiên cũng được hiển thị), khiên chặn 2 ("I trường lực", không trừ máu), khiên xuyên 0xD ("I trường lực" + khấu trừ máu), hạ gục (sát thương ≥ HP, nổ) đều được chơi theo kỷ lục. Cắt り払い 0x12 Đối với α・アジール không có kiếm, nó chỉ không hút máu, không cầm kiếm và không có từ - phiên bản đầu tiên chỉ dành cho các mecha cầm kiếm.
- Mục 5: Khi người phòng thủ đạt đến `+0x18 = 0`, HUD hiển thị "Phản công", và bản thân vòng phản công không bị chặn và cần phải được lấp đầy.
- Ngoài ra còn có vấn đề chồng chữ và dư từ trong màn hiển thị dòng (có thể xảy ra ở cả đường trình diễn và trận đánh thông thường), liên quan đến việc vẽ lại dần dần các đoạn hội thoại. Chúng phải được kiểm tra riêng và không phải là một phần của chức năng này.

### 9.2 Hoàn thiện trang đánh giá (2026-10-03)

- Bố cục được thiết kế theo canvas (Tạo tác thiết kế "Thiết kế giao diện đánh giá chiến đấu"): "Đảo ngược" ở bên trái (sơ đồ cơ thể và hình đại diện được lật ngang sang phải), hai thẻ dành cho "Tấn công" ở bên phải, ba hàng lưới và hai khu vực kết quả "Đảo ngược và bị tấn công / Tấn công và phản công" bên dưới; chiều cao của thẻ được tính theo cửa sổ (bảng 94% giảm 270 dp, 150–400 dp). `viewer_*` trong tổng số `src/native/ui/frontend.cpp`.
- Phản ứng mở theo điều kiện ban đầu (`viewer_gate`, dựa trên battle-formulas.md): lá chắn = trang bị trên người 2 + phòng thủ của phi công S; bị cắt = trang bị 1 + vết cắt của phi công り払い + vũ khí đang tới `& 0x08`; lá chắn = hào quang (yêu cầu chiến binh thánh thiện) hoặc tôi buộc trường/lớp phủ tia/phòng thủ hành tinh (vũ khí tới) `& 0x02`); bản sao = khả năng `0x163011`. Sát thương lá chắn bằng 0 có nghĩa là chặn (mã 2/3/4/5) và lớn hơn 0 có nghĩa là xuyên thủng (0xD/0xE/0xF/0x10); mã nhân bản là 6-0xC tùy theo cấp độ khả năng. Dữ liệu Thư viện đã được bổ sung `equipment_bits`, `ability_bits`, vũ khí `flags` và phi công `skill_bits`, đồng thời các vũ khí bổ sung (486 trên 120 đơn vị) chỉ có trong bảng sửa đổi đã được thêm vào danh sách vũ khí. Danh sách vũ khí đã loại bỏ vũ khí MAP.
- Sát thương sẽ khiến đối thủ có 10 HP theo mặc định; phản công được bật theo mặc định, vũ khí phản công của người phòng thủ mặc định là vũ khí mạnh nhất và kẻ tấn công mặc định là vũ khí cuối cùng. Mã phản ứng của người tấn công trong vòng phản công được viết là `+8`.
- Phi công chỉ liệt kê những người có thể điều khiển máy (`tools/content/battle_viewer_pilots.py` tạo `src/host/battle_viewer_pilots.inc`: bản ghi triển khai cấp độ (loại bỏ bản ghi dự phòng có giá trị bản ghi là 3), loại のりかえ, dạng bảng vũ khí giống nhau và bảng siêu chế độ), đảm bảo các dòng được viết ban đầu cho cặp này.
- BGM mặc định theo quy định ban đầu của §6.7 để lấy bài hát phụ tấn công (bảng thí điểm, dạng H/S/V-MAX được mã hóa cứng và bảng nội dung được sử dụng khi không có bài hát thí điểm).
- Hiệu chỉnh ngẫu nhiên được xác minh bằng máy thực tế: trên màn hình rộng, các khối bên trái và bên phải của khung đen cắt sẵn chỉ chiếm tỷ lệ 4:3, thay vào đó phân nhánh `800C6D00` thành bản sao `807FFF00` trong mỗi khung và sử dụng căn chỉnh hình chữ nhật gEX để mở rộng các khối bên trái và bên phải đến cạnh màn hình (`battle_hud.cpp`; vùng tạm thời chèn tập lệnh được thu nhỏ xuống 0xFF00). Hình ảnh full-frame HD tuân theo hiệu ứng bảng màu tại chỗ ban đầu (Shisui Gold, Flash on Hit): nếu bảng màu khác với ROM thì hai bộ bảng màu (tối đa 256 màu) được sử dụng để đổi màu bảng tra cứu từng pixel và một biến thể được lưu vào bộ đệm trong bảng nội dung. Khi chưa sẵn sàng, sprite ban đầu (`native_sprite.cpp``recolor_pixels`, giới hạn trên 256 bộ) sẽ được hiển thị.

### Trang tuyển chọn 9.3 (2026-10-03, được thay thế bởi 9.4)

Trong phiên bản đầu tiên, máy bay, phi công, BGM và các cảnh đều được tạo thành một lưới thẻ toàn trang; trang thí điểm cũng có tab "Tất cả phi công". Nếu bạn chọn một phi công không thể kích hoạt máy bay hiện tại, bạn có thể thay thế nó bằng máy bay mặc định của anh ta. 2026-10-04 Đã thay đổi cách tiếp cận một trang của phiên bản 9.4 và hai điểm này đã bị xóa. Các thực hành sau đây được chuyển sang phiên bản 9.4:

- Phi công mặc định: Lấy tổ hợp xuất hiện nhiều nhất trong cấp độ triển khai (`battle_viewer_pilots.inc`).
- BGM được nhóm và thử giọng theo tác phẩm.
- Hình thu nhỏ cảnh: Nhập phần `scenes` (`cutin_hd.py scenes --bind`) của gói HD `battle_sprites` và chủ nhà sử dụng `sprites::viewer_scene_image` để lấy hình ảnh.
- Tiêu đề có hai bộ hẹn giờ chờ, được đặt lại khi trang được mở hoặc khi trận chiến đang chờ:
- `D_801CC390`: Vào trận trình diễn sau 180 khung hình chờ;
- `D_801CC3A4` (u16): "Hãy nhấn BẮT ĐẦU" và thời gian chờ trên menu chuông vượt quá 0x385 khung hình và chuyển sang cảnh mở đầu trạng thái chính 12 đến `801C9BF8`.

### 9.4 trang đơn (2026-10-04, đánh giá cao Z giả)

"Giải pháp một trang" canvas đã được tích hợp vào trò chơi (`viewer_*` trong tổng số `frontend.cpp`).

- **Một trang**: Có một thẻ và năm hàng lưới ở bên trái "Bộ đếm" và bên phải là "Tấn công".
- Trên thẻ có sơ đồ cơ thể, hình đại diện, HP → HP còn lại và hình thu nhỏ của cảnh bên này được bày ở mặt sau.
- Ngũ hành là thân thể, người phi công, vũ khí (đối phương là vũ khí phản công), kết quả của đòn tấn công và cảnh vật.
- Dòng kết quả đòn đánh được viết là "Đánh > Bình thường·Sát thương 6690 (còn lại 10)", và ba dấu nhỏ "Khiên/Che/Cắt" phía sau sẽ sáng lên khi bên này có sẵn ("Screen Through Defense" của Z).
- Bên dưới là dòng BGM; dòng dưới cùng giải thích lựa chọn hiện tại và bên phải là kết thúc và bắt đầu chiến đấu.
- **Hộp lựa chọn**: Bấm vào một dòng, hộp lựa chọn sẽ bao phủ nửa còn lại (hộp BGM bao phủ phía đối diện) và bên này vẫn hiển thị.
- Con trỏ dừng ở mục nào thì ngay lập tức chuyển sang mục đó: dòng thẻ, lưới, BGM sẽ thay đổi tương ứng và thẻ sẽ được đánh dấu "Đang xem trước".
- Lưu một bản sao của trạng thái hiện tại khi mở hộp lựa chọn: "Return"/B để đặt lại bản sao đó, "Quyết định", A hoặc nhấp vào cùng mục đó một lần nữa để giữ lại.
- Danh sách duy trì vị trí cuộn khi làm mới trang.
- **Chọn máy bay trước rồi chọn phi công** (thứ tự Z):
- Khung thân được phân trang theo tác phẩm ("◀ Work n/N ▶" ở đầu khung, dùng L/R hoặc phím trái phải để lật trang, lật trang sẽ xem trước trang đầu tiên của trang mới).
- Đối với máy bay đã chọn, nếu phi công được chọn khi mở hộp chọn có thể sử dụng được thì sẽ được giữ lại. Nếu không sử dụng được sẽ được thay thế bằng phi công mặc định của đơn vị này.
- Ô thí điểm chỉ liệt kê những người có thể điều khiển máy hiện tại, có đánh dấu "hiện tại" và "mặc định".
- Việc chọn phi công không làm thay đổi máy bay nên "máy bay mặc định cho mỗi phi công" không còn cần thiết nữa, `battle_viewer_units.inc` và phần mã tạo ra nó đã bị xóa.
- **Hộp kết quả nhấn**: Theo Z chia làm 2 cột.
- Cột bên trái là kết quả: đánh > bình thường/lá chắn/lá chắn, trượt > tránh/clone/cắt đứt, ghi lý do không dùng được; cũng có "không có phản công / phản công" ở phía trên của bên tấn công.
- Cột bên phải là sát thương: 10 trái (mặc định), lớn/trung bình/nhỏ (25%/50%/75% trái), hạ gục, cộng thêm tinh chỉnh ±100/±1000.
- **Khung cảnh**: Được chia thành 4 tab: "Tất cả/Mặt đất/Không khí/Vũ trụ" (không khí=không khí, không gian khác nhau, vũ trụ=vũ trụ, mặt trăng). Khi thay đổi tab, cảnh hiện tại sẽ không di chuyển trong tab mới và sẽ xem trước cảnh đầu tiên trong tab mới.
- **Hộp BGM**: Các bài hát tấn công nằm trên cùng, được nhóm theo các tác phẩm bên dưới; nhấn C← để thử giọng (phím X trên Bộ bài) và di chuyển con trỏ trong khi thử giọng sẽ thay đổi bài hát.
- **Thao tác**: Nhấn các phím điều hướng để di chuyển đến nút gần nhất và trái và phải chỉ di chuyển trên cùng một dòng; khi hộp lựa chọn mở, chỉ di chuyển trong hộp.
- **Xác minh máy thật** (cửa sổ 1280×800, giao diện cực lớn):
- Xem trước khung cơ thể: God Gun → Extreme Star Granada, phi công được thay thế bởi Chipodi, vũ khí được thay thế bằng một khẩu súng khổng lồ và "khiên" sáng lên; toàn bộ trang được khôi phục sau B.
- R Chuyển sang Mobile Suit Gunma W mới, xem trước Wing Gun và Hiro, dòng BGM sẽ chuyển sang bài hát tấn công.
- Chọn "Sát thương nhỏ" do đòn tấn công gây ra, HP hiển thị sẽ là 6700 → 5025.
- Tab trên không của khung cảnh và nhóm khung BGM theo tác phẩm là bình thường.
- Sau khi trận chiến bắt đầu, Wing Gun và Hero đã được sử dụng.

## 10. Giao diện

Trang đánh giá cao chỉ sử dụng RmlUi (`src/native/ui/frontend.cpp`, bộ công cụ giao diện người dùng duy nhất cho dự án; các giao diện hệ thống như AppKit không được sử dụng). Bố cục đề cập đến các cột bên trái và bên phải của Z. Phong cách tuân theo bản phác thảo cuối cùng của trang xác nhận trước chiến tranh: cạnh vát (trang trí `slant`), nhãn trang trên cùng, sơ đồ nội dung lớn và cỡ chữ lớn; bố cục dựa trên giao diện "cực lớn" của Steam Deck (giống như Thư viện) và kiểm tra ngoại tuyến `run_audit.py` cần bao trùm trang mới. Các mục mới nhập `content/locales/*.json` và đăng ký `UI_KEYS` trong tổng số `src/srw64_native/profile.py`. Giao diện gỡ lỗi tuân theo `ui.click --id …`.