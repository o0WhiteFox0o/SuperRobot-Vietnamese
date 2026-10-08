> **Ngôn ngữ / Language:** [Tiếng Việt](upgrade-limits.vi.md) · [English](upgrade-limits.en.md) · [中文](upgrade-limits.md)

# Số lượng giai đoạn biến hình và giới hạn trên của "vịt con xấu xí": tăng từng giai đoạn, giá cả, cài đặt cơ thể và thiết kế MOD

Ngày: 2026-09-18. Phạm vi: ROM Rev 0 tiếng Nhật và tháo gỡ tĩnh của dự án này (`build/recomp/cpu-scan`), trích xuất thư mục cơ thể/vũ khí (`assets/original-data/records`). Phần 1 đến 6 là phân tích tĩnh; MOD giai đoạn đầu trong Phần 7 (các giá trị có thể định cấu hình, giới hạn trên vượt quá 15 và màn hình chuyển đổi hiển thị giới hạn trên ban đầu) đã được triển khai và màn hình chuyển đổi đã được kiểm tra với hai lần chạy giới hạn vào ngày 2026-09-18 (Phần 7.5); các mục nhập chưa được xác nhận trên máy thực tế nằm trong Phần 8. Để biết cách xử lý số khoảng thời gian thay thế, hãy xem [Phân tích kế thừa chuyển đổi](upgrade-inheritance.md), phần này sẽ không được lặp lại trong bài viết này.

"Vịt con xấu xí" trong bài viết này đề cập đến giới hạn trên của việc sửa đổi thân máy SRW64 thay đổi tùy theo máy: máy mạnh chỉ có thể sửa đổi thành 7 công đoạn, trong khi máy yếu và máy sản xuất hàng loạt có thể sửa đổi thành 13 đến 15 công đoạn. Sau khi sửa đổi hoàn toàn, họ có thể vượt qua máy bay có điểm xuất phát cao hơn.

## 1. Tóm tắt kết luận

| Kết luận | Cơ sở |
| --- | --- |
| Toàn bộ hệ thống "vịt con xấu xí" chỉ được xác định bởi **một byte trên mỗi nội dung**: ROM nội dung ghi lại giới hạn sửa đổi trên của `+0x20` (giá trị ban đầu là 6~15). Năm khả năng và **mỗi loại vũ khí** của mecha đều có chung giới hạn trên này | `800A5330` Viết ví dụ `+0x51`; Màn hình chuyển đổi `801CFA78` (năm vật phẩm), `801D1318` (vũ khí) |
| Mỗi mức tăng **không liên quan** đến máy bay: một đường cong 15 đoạn cho mỗi mục trong số năm mục, được chia sẻ bởi toàn bộ máy bay. Máy có giới hạn trên cao chỉ có thể đi xa hơn theo cùng một đường cong | Năm chu kỳ tích lũy `800A5254`, bảng `D_800CA4F0`~`D_800CA570` |
| Giá từng phân khúc không liên quan gì đến phần thân và giới hạn trên: chỉ cần nhìn "mặt hàng này hiện thuộc phân khúc nào" | Kiểm tra theo số phân đoạn trong `801CF988``D_801DC36C` và năm bảng khác |
| Vũ khí được chia thành 5 loại theo **loại sửa đổi** (bản ghi ROM vũ khí `+0x0E`): Loại 1 đến 4 đều có đường cong tăng dần và bảng giá, loại 0 không thể sửa đổi (tất cả các loại tăng là 0, giá là 0) | Tìm kiếm theo chu kỳ bắt đầu từ mức tăng `800A55F4``D_800CA590`; giá `801D0C7C` theo ví dụ `+0x15` chi nhánh |
| Có **hai bản sao** của bảng tăng: bảng thường trú được sử dụng cho khả năng tính toán lại và cũng có bảng "xem trước" trong lớp phủ của màn hình sửa đổi. Khi xác nhận sửa đổi, giá trị xem trước sẽ được thêm trực tiếp vào nội dung hiện tại. Hai phiên bản gốc có cùng giá trị và việc thay đổi một trong số chúng sẽ gây ra sự không nhất quán | Thêm `D_801DC4AC[段数]` vào `801CFD1C` và các địa điểm khác; sử dụng `D_800CA4F0` cho `800A5254` |
| Tất cả các bảng chỉ có 15 đoạn (mục thứ 16 trong bảng giá là Sentinel 99999), và chuỗi thanh tỷ lệ chỉ có 11 giới hạn trên, dao động từ 5 đến 15. **Chỉ điều chỉnh giới hạn trên dưới 15, không cần dữ liệu mới**; nếu vượt quá 15, chủ nhà phải tiếp quản giá trị, giá cả, bản xem trước và tỷ lệ | Phần 3, 5 |
| Giới hạn trên cũng xác định: kích hoạt thay đổi thiết bị EW, vũ khí bổ sung được sửa đổi hoàn toàn, giá bán thân máy và giới hạn ghi trên là `3D6C`. Khi thực hiện "Phá vỡ giới hạn trên", những điều này phải được đánh giá theo **giới hạn trên ban đầu** | Phần 5 |
| Kho lưu trữ lưu trữ từng phân đoạn trong số năm phân đoạn và số phân đoạn của mỗi loại vũ khí ở dạng **4 chữ số**. Giới hạn trên là 15 cũng là giới hạn trên của định dạng lưu trữ; byte giới hạn trên `+0x51` không được lưu trữ và sẽ được ROM tính toán lại sau khi đọc tệp | `80092240` (cơ thể), `80092498` (vũ khí), xem Phần 4.3 |
| So sánh với chi phí sửa đổi của Akurasu: Fukuro của ν là 140.000, Z(JS) của Makuzu là ロケットパンチ 364.000. Nó hoàn toàn phù hợp với mô hình trong bài viết này; Hướng dẫn ウイングゼロ của ツインバスターライフルMAP ghi 110.000 và mô hình tính toán 140.000, điều này không nhất quán | Mục 3.3 |

## 2. Mỗi phần cải thiện bao nhiêu (Câu hỏi 1)

### 2.1 Ngũ vật của thân

`800A5254(机体实例, 模式)` là chức năng tính toán lại khả năng duy nhất trong toàn bộ trò chơi: giá trị cơ bản được đọc lại từ bản ghi ROM nội dung và sau đó bảng tăng dần được tích lũy theo từng phân đoạn theo năm số phân đoạn của phiên bản `+0x4C..+0x50`. Mục thứ 0 được cố định thành 0 và số phân đoạn L được thêm vào mục đầu tiên trong L.

| Phân đoạn | 1 đến 5 đoạn cho mỗi đoạn | 6 đến 15 đoạn cho mỗi đoạn | Trường mẫu | Bảng tăng thường trú (ROM) |
| --- | --- | --- | --- | --- |
| HP | +200 | +200 | HP tối đa `+0x06` | `D_800CA4F0` (`0x54EE0`) |
| VN | +10 | +20 | EN tối đa `+0x0A` | `D_800CA510` (`0x54F00`) |
| Phong trào | +5 | +10 | `+0x10` | `D_800CA530` (`0x54F20`) |
| Giáp | +100 | +150 | `+0x12` | `D_800CA550` (`0x54F40`) |
| Giới hạn | +10 | +20 | `+0x14` | `D_800CA570` (`0x54F60`) |

Cải thiện tích lũy ở cấp độ đầy đủ dựa trên giới hạn trên (giới hạn trên xuất hiện trong phiên bản gốc):

| Mũ | HP | VN | Tính cơ động | Giáp | Giới hạn |
| --- | --- | --- | --- | --- | --- |
| 6 | +1200 | +70 | +35 | +650 | +70 |
| 7 | +1400 | +90 | +45 | +800 | +90 |
| 8 | +1600 | +110 | +55 | +950 | +110 |
| 9 | +1800 | +130 | +65 | +1100 | +130 |
| 10 | +2000 | +150 | +75 | +1250 | +150 |
| 11 | +2200 | +170 | +85 | +1400 | +170 |
| 12 | +2400 | +190 | +95 | +1550 | +190 |
| 13 | +2600 | +210 | +105 | +1700 | +210 |
| 15 | +3000 | +250 | +125 | +2000 | +250 |

Độ lớn của "vịt con xấu xí" nằm trong bảng này: đơn vị có mũ 15 được phát huy tối đa, khả năng cơ động của nó cao hơn +80 so với đơn vị có mũ 7 và giáp của nó là +1200.

### 2.2 Sức mạnh vũ khí

Sức mạnh của phiên bản vũ khí (bước 0x24, phiên bản cơ thể `+0x2C` miếng, con trỏ `+0x30`) `+0x06` = bản ghi ROM vũ khí `+0x01` × 100 + tổng L mục đầu tiên của bảng tăng dần, L là số phân đoạn của phiên bản vũ khí `+0x16`. Bảng tăng dần chọn các hàng theo phiên bản vũ khí `+0x15` (loại sửa đổi, được sao chép từ bản ghi ROM vũ khí `+0x0E` bởi `800A6A98`), 15 mục mỗi hàng, bảng `D_800CA590` (ROM `0x54F80`, 5 hàng × 15 mục u16, số 0 ở cuối).

| Loại | Tăng dần cho từng giai đoạn từ giai đoạn 1 đến giai đoạn 15 | Tích lũy sau 15 chặng | Số lượng vũ khí gốc |
| --- | --- | --- | --- |
| 0 | Tất cả số 0 (không thể sửa đổi, xem Phần 6.1) | 0 | 102 |
| 1 | 100,100,150,150,200,200,200,200,200,250,250,250,250,250,300 | +3050 | 541 |
| 2 | 100,100,150,150,150,150,200,200,200,200,250,250,250,250,300 | +2900 | 616 |
| 3 | Tương tự như loại 2 | +2900 | 3 (Pháo 120mm キャノン, ミサイルランチャー, スペシャルボロットパンチ) |
| 4 | 100,100,150,150,150,150,150,150,200,200,200,200,200,200,300 | +2600 | 67 (バルカンđại bác, súng máy trên không, v.v.) |

Loại 2 có đường cong công suất giống hệt Loại 3, chỉ có giá khác nhau (Mục 3.2). Công suất tích lũy toàn giai đoạn theo giới hạn trên: giới hạn trên 7 là loại 1 +1100/loại 2, 3 +1000/loại 4 +950; giới hạn trên 9 là +1500/+1400/+1300; giới hạn trên 13 là +2500/+2350/+2100; giới hạn trên 15 là +3050/+2900/+2600.

Loại 0 bao gồm: Kỹ thuật dung hợp (ツインビーム, ダブルゴッドフィンガー, v.v.), thiết bị sửa chữa/thiết bị cung cấp, シャッフル Liên minh và ゴッドガンダムH Đặc biệt của anh ấy di chuyển, パンチ/キック/rush của ドモン và một loạt vũ khí dành riêng cho kẻ thù.

## 3. Mỗi phân khúc tiêu thụ bao nhiêu tiền (Câu hỏi 2)

Bảng giá đang tu sửa lớp phủ màn hình `load_0008F4B0` (ROM `0x8F4B0`, VRAM `801C4500`; ROM offset của bảng = VRAM − `0x801C4500` + `0x8F4B0`), 16 u32/tấm, giá lấy theo **số phân đoạn hiện tại** (mục 0 là giá phân đoạn 0→1), mục 16 cố định tại 99999. Số tiền là `D_8010F5F4` (u32); không đủ tiền hiển thị văn bản 4144 "Tiền đủ" và số lượng phân đoạn đã đạt đến giới hạn trên hiển thị văn bản 4143 "これ上の cải cáchはできません". Khi giá là 0 hoặc 99999, giao diện gồm năm mục hiển thị `-----`.

### 3.1 Ngũ vật của thân

| Đoạn hiện tại → Đoạn tiếp theo | 0→1 | 1→2 | 2→3 | 3→4 | 4→5 | 5→6 | 6→7 | 7→8 | 8→9 | 9→10 | 10→11 | 11→12 | 12→13 | 13→14 | 14→15 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HP `D_801DC36C` | 2000 | 4000 | 6000 | 8000 | 10000 | 12000 | 14000 | 16000 | 18000 | 20000 | 22000 | 24000 | 26000 | 28000 | 30000 |
| VI `D_801DC3AC` | 1000 | 1500 | 1500 | 2000 | 2000 | 3000 | 3000 | 4000 | 4000 | 5000 | 5000 | 6000 | 6000 | 7000 | 7000 |
| Chuyển động `D_801DC3EC` | 5000 | 8000 | 10000 | 12000 | 15000 | 20000 | 25000 | 30000 | 35000 | 40000 | 45000 | 50000 | 55000 | 60000 | 65000 |
| Giáp `D_801DC42C` | 3000 | 5000 | 8000 | 10000 | 15000 | 20000 | 25000 | 30000 | 35000 | 40000 | 45000 | 50000 | 55000 | 60000 | 65000 |
| Giới hạn `D_801DC46C` | Tương tự như EN |

Độ lệch ROM của năm bảng là `0xA731C`, `0xA735C`, `0xA739C`, `0xA73DC`, `0xA741C`.

Tổng giá dựa trên giới hạn trên:

| Mũ | HP | VN | Tính cơ động | Giáp | Giới hạn | Năm Tổng |
| --- | --- | --- | --- | --- | --- | --- |
| 6 | 42.000 | 11.000 | 70.000 | 61.000 | 11.000 | 195.000 |
| 7 | 56.000 | 14.000 | 95.000 | 86.000 | 14.000 | 265.000 |
| 9 | 90.000 | 22.000 | 160.000 | 151.000 | 22.000 | 445.000 |
| 11 | 132.000 | 32.000 | 245.000 | 236.000 | 32.000 | 677.000 |
| 13 | 182.000 | 44.000 | 350.000 | 341.000 | 44.000 | 961.000 |
| 15 | 240.000 | 58.000 | 475.000 | 466.000 | 58.000 | 1.297.000 |

### 3.2 Vũ khí

Giá của vũ khí cũng chỉ phụ thuộc vào loại và số giai đoạn hiện tại, không liên quan gì đến giới hạn trên của thân máy. Giá của mỗi giai đoạn là một dãy số học:

| Loại | Giá cho đoạn thứ n (từ 0) | Bảng giá (ROM) | Đầy đủ 7 đoạn | Đầy đủ 9 đoạn | Đầy đủ 13 đoạn | Đầy đủ 15 đoạn |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 5000 × (n+1) | `D_801DC7BC` (`0xA776C`) | 140.000 | 225.000 | 455.000 | 600.000 |
| 2 | 4000 × (n+1) | `D_801DC77C` (`0xA772C`) | 112.000 | 180.000 | 364.000 | 480.000 |
| 3 | 3000 × (n+1) | `D_801DC73C` (`0xA76EC`) | 84.000 | 135.000 | 273.000 | 360.000 |
| 4 | 2000 × (n+1) | `D_801DC6FC` (`0xA76AC`) | 56.000 | 90.000 | 182.000 | 240.000 |
| 0 | Không cần tra bảng thì giá 0 | — | — | — | — | — |

### 3.3 So sánh với các số chiến lược

Trang "Nâng cấp đơn vị" của Akurasu liệt kê chi phí tích lũy của ba loại vũ khí bổ sung được nâng cấp đầy đủ:

| Vũ khí | Chiến lược | Mô hình của bài viết này | Kết quả |
| --- | --- | --- | --- |
| νガンダム フィンファンネル (giới hạn trên 7, loại 1) | 140.000 | 5000 × (1+…+7) = 140.000 | Nhất quán |
| マジンガーZ(JS) ロケットパンチ (giới hạn 13, loại 2) | 364.000 | 4000 × (1+…+13) = 364.000 | Nhất quán |
| ウイングゼロ ツインバスターライフルMAP (giới hạn trên 7, loại 1) | 110.000 | 140.000 | Không nhất quán; giá tích lũy của bất kỳ loại nào hoặc giới hạn trên không bằng 110.000, bị nghi ngờ là lỗi văn thư trong chiến lược, sẽ được xác nhận trên máy thực tế |

## 4. Cài đặt cho các body khác nhau ở đâu (Câu hỏi 3)

### 4.1 Trường và bảng

| Cài đặt | Vị trí | Thời gian chạy | Mô tả |
| --- | --- | --- | --- |
| Giới hạn trên của sửa đổi cơ thể | Bản ghi ROM nội dung `+0x20` (bảng ghi ROM `0x71B80` + số nội dung × 36) | Ví dụ `+0x51` | Được viết khi tạo một phiên bản mới (`800A7100`, `800A8DF0`), được viết lại từ ROM mỗi lần `800A5254` được tính toán lại |
| Năm phân đoạn | — | Ví dụ `+0x4C` HP, `+0x4D` EN, `+0x4E` Tính cơ động, `+0x4F` Giáp, `+0x50` Giới hạn | Bảng phiên bản khung máy bay `D_8016A210`, 140 mục × 0x54 |
| Loại sửa đổi vũ khí | Bản ghi ROM vũ khí `+0x0E` (bảng ghi ROM `0x74E90` + số vũ khí × 16) | Ví dụ về vũ khí `+0x15` | Chỉ sao chép khi tạo phiên bản vũ khí (`800A6A98`) |
| Số phân khúc vũ khí | — | Ví dụ về vũ khí `+0x16` | Độc lập từng phần; giới hạn trên là `+0x51` của máy chủ |
| Năm mức tăng (để tính công suất) | `D_800CA4F0`～`D_800CA570`, ROM bắt đầu từ `0x54EE0`, 5 × 16 u16 | RDRAM thường trú | Mục thứ 0 là 0 |
| Năm mức tăng (để xem trước và xác nhận giao diện) | `D_801DC4AC`～`D_801DC52C`, bắt đầu từ ROM `0xA745C`, 5 × 16 u16 | lớp phủ | mục thứ n = số gia của n+1 đoạn, mục cuối cùng 0 |
| Tăng vũ khí (để tính sức mạnh) | `D_800CA590`, ROM `0x54F80` | Thường trú | Loại × 15 mục |
| Tăng vũ khí (xem trước giao diện) | `D_801DC85C` (loại 1), `D_801DC83C` (2), `D_801DC81C` (3), `D_801DC7FC` (4), ROM `0xA780C`／`0xA77EC`／`0xA77CC`／`0xA77AC` | lớp phủ | phù hợp với bảng thường trú từng mục |
| Giá vũ khí và Pentathon | Phần 3 | lớp phủ | — |
| Thanh tỷ lệ | `D_801DC340` (ROM `0xA72F0`): 11 con trỏ, nhấn "giới hạn trên − 5" để chọn một nhóm số văn bản, sau đó lấy một nhóm theo số đoạn hiện tại | lớp phủ | văn bản 4145~4267, chẳng hạn như phân đoạn thứ 3 của giới hạn trên 7 là "xxxxxxxxx▷▷▷▷"; giới hạn trên 5 và 14 Hai bánh răng có dây nhưng không có thân để sử dụng |
| Vũ khí bổ sung được sửa đổi hoàn toàn | `D_801DC87C` (ROM `0xA782C`), 18 vật phẩm (thân hình, vũ khí đã được sửa đổi hoàn toàn, vũ khí đã mở khóa), 999 kết thúc | lớp phủ | Xem Phần 5 |
| Lớp phủ EW | `D_801DC6E4` (ROM `0xA7694`), 5 đôi | lớp phủ | Xem [Phân tích kế thừa chuyển đổi](upgrade-inheritance.md) Phần 2.1 |
| Số phân khúc địch | Bản ghi triển khai `+12` (chỉ mục nâng cao) → `D_800CB5DC` (ROM `0x55FCC`): 0,1,3,5,7,9,11,13,15 | Viết năm mục khi triển khai và ghi cùng một giá trị cho tất cả vũ khí khi tạo phiên bản mới | Phiên bản gốc chỉ sử dụng chỉ số 0~5 (số đoạn 0~9), tất cả đều không vượt quá giới hạn trên của phần thân |

### 4.2 Phân bố giới hạn trên ban đầu

Hồ sơ máy bay 363: giới hạn trên: 6 một đơn vị, 7 bốn mươi đơn vị, 8 năm đơn vị, 9 năm mươi mốt đơn vị, 10 mười tám đơn vị, 11 ba mươi bốn đơn vị, 12 một đơn vị, 13 hai mươi tám đơn vị, 15 một trăm tám mươi lăm đơn vị (chủ yếu là các đơn vị địch). Giới hạn trên được đặt thủ công từng cái một và không được tính toán từ khả năng cơ bản, nhưng xu hướng rất rõ ràng: máy mạnh thì thấp, máy yếu thì cao. Ví dụ về máy bay thường được sử dụng của chúng tôi (tập lệnh gốc sử dụng `3D5A` để đăng ký phần thân và dạng kết hợp):

| Giới hạn trên | Thân hình |
| --- | --- |
| 6 | ガンダムサンドロック (người duy nhất trong toàn bộ danh sách) |
| 7 | νガンダム, sản xuất hàng loạt νガンダムF, phiên bản truyền hình dòng W và phiên bản EW (thế hệ đầu tiên ガンダムサンドロックLoại trừ: Serotype, ゼロ, デスサイズ series, loạt ヘビーアームズ, loạt シェンロン/アルトロン, サンドロック Kai ／カスタム、エピオン）、ゲッター1／ドラゴン／真・ゲッター、ダイターン3、ゴッドマーズ、ドモンSinh học |
| 8 | ザンボット3 series (ザンバード, ザンブル, ザンベース, ザンボエース) |
| 9 |ゴッド／シャイニングガンダム, シャッフルAlliance Four Machines, ZZ, mkⅢ, 100 Shiki, フルアーマーHyakushikai,キュベレイmkⅡ, ヤクト・ドーガ, トールギスⅢ, ダンクーガ, グレンダイザーMỗi dạng,スペイザー, レイズナー, ニューレイズナー,サーバイン、ビルバイン、ズワウス、アシュクリーフ、ラーズグリーズ|
| 10 | コン・バトラーV và Năm cỗ máy, ダンクーガBốn cỗ máy (イーグルファイター, ビッグモス, ランドクーガー,ランドライガー) |
| 11 | Zガンダム、スーパーガンダム、ディジェSE-R、メタス开、リ・ガズィ(BWS ), loại sản xuất hàng loạt νガンダムI, GP03,ノイエ・ジール, トールギス, ピースミリオン, グレートマジンガー, loại sản xuất hàng loạt グレート,シュピーゲル, ノーベル, ライジング,ゼーロン、ヴァイローズ、スーパーアースゲイン、スイームルグS、バルディ、ベイブル|
| 12 | マジンガーZ (phiên bản duy nhất trong toàn bộ danh sách; phiên bản JS là 13) |
| 13 | Mỗi tình mẫu tử (アーガマ, ネェル・アーガマ, ラー・カイラム, アルビオン, アウドムラ,ラビアンローズ、グラン・ガラン、ゴラオン）、ガンダムmkⅡ、マジンガーZ(JS)、ビューナスA、ダブル／ドリル／マリンスペイザー、ジャイアント・ロボ、ブラックウイング、ダンバイン、バストール、グライムカイザル、ガイヤー、トーラス、ノウルーズ、シグルーン|
| 15 |ガンダム、ガンキャノン、ガンタンク、ジェガン、シュツルム・ディアス、ガンダムEz 8、Gディフェンサー、ダイアナンA、ボスボロット、ミネルバX、ボチューン、ドール,コスモクラッシャー, Ginlingrobo, エルブルス, シャトル号|

Giới hạn trên trong cùng một họ kết hợp/chuyển đổi không nhất thiết phải giống nhau: ガンダムmkⅡ 13 và スーパーガンダム 11, ダンクーガ bốn máy 10 và ダンクーガ9,スペイザー nhiều loại 13 và グレンダイザー 9, ガイヤー 13 và ゴッドマーズ 7. Trong số đó, mkⅡ→スーパーガンダム sẽ kích hoạt số lượng phân đoạn vượt quá giới hạn, xem Phần 6.3.

### 4.3 Số lượng phân đoạn trong kho lưu trữ

Kho lưu trữ ngắt (`800924D8` được ghi vào bộ đệm `801C2600`, bắt đầu từ SRAM `0x10`) không lưu phiên bản máy bay như hiện tại mà được nén thành 16 byte (`80092240`) từng cái một: `+0` là số máy bay <<6 | Số lượng vũ khí, `+2` là HP<<4 | VN, `+3` là tính di động <<4 | Giáp, `+4` là cờ (cao 2 bit) | giới hạn, `+0xE` là số sê-ri của vũ khí đầu tiên của máy bay. 6 byte cho mỗi vũ khí (`80092498`): số lượng, dạng có sẵn, số lượng phân đoạn <<4 | cờ 4 bit thấp. Số tiền là u32 (`800918DC`) trong khối `+0x54`.

Do đó, số phân đoạn năm môn phối hợp và vũ khí trong kho lưu trữ chỉ có 4 chữ số và **15 là giới hạn trên của chính định dạng lưu trữ**; byte giới hạn trên `+0x51` và các giá trị khả năng không được lưu và sẽ được tính toán lại theo số phân đoạn sau khi đọc tệp. Điều này xác định ranh giới của MOD: nếu số vượt quá 15, định dạng lưu trữ sẽ không được chạm vào và nếu số vượt quá 15, một số phân đoạn khác phải được lưu (Phần 7.6). `tools/recomp/gameplay/upgrade_save.py` Sử dụng định dạng này để thực hiện chỉnh sửa kho lưu trữ có kiểm soát (kinh phí, số đoạn), chỉ nhằm mục đích xác minh.

## 5. Tất cả người đọc giới hạn trên

Đọc tất cả các mã của `+0x51` (hoặc `D_8016A261` + offset phiên bản), chia theo mục đích:

| Mục đích | Vị trí | Nội quy |
| --- | --- | --- |
| Năm mục có thể thay đổi | `801CFA78` trong phạm vi `801CF988`; Xác nhận từ `801CFCA4` | Chỉ có thể thay đổi khi số lượng phân đoạn < giới hạn trên; Khi xác nhận, trước tiên hãy khấu trừ tiền, thêm mức tăng xem trước và sau đó +1 khi < giới hạn trên |
| Năm mặt hàng hiển thị giá | `801CF988` bắt đầu từ `801D0168` | Chỉ kiểm tra giá khi số đoạn < giới hạn trên, nếu không sẽ hiển thị `-----` |
| Năm mục xem trước và chia tỷ lệ | `801C80E0` (`801C8194` lấy tỷ lệ, `801C8224` lấy bản xem trước) | Khi số lượng phân đoạn = giới hạn trên, nó sẽ hiển thị `-----`; thang đo `D_801DC340[上限−5][段数]` |
| Giá vũ khí, xem trước và cân | `801D0C7C` | Số giai đoạn = Giới hạn trên sẽ hiển thị "これ上の综合はできません" |
| Xác nhận vũ khí | `801D1100` (`801D1318`, `801D1384`) | Khấu trừ và lũy thừa được viết dưới dạng giá trị xem trước; số giai đoạn < giới hạn trên là +1; thì `801D0AE4` được gọi khi số giai đoạn **= giới hạn trên** để mở khóa vũ khí bổ sung |
| Vũ khí bổ sung được sửa đổi hoàn toàn | `801D0AE4`, bảng `D_801DC87C` | Khi số trên cơ thể khớp với số vũ khí mới được sửa đổi, hãy xóa bit 2 (bit đã mở khóa) của vũ khí mục tiêu `+0x22`. Ví dụ: νフィンファンネル→フィンファンネルMAP、mkⅡ／スーパーガンダム拡sanバズーカ→MAP、キュベレイmkⅡファンネル→MAP、ゼロツインバスターライフルMAP→2MAP, ヘビーアームズ开ダブルガトリングガン→全弾発bắn MAP, グレートブレストバーン→MAP, マジンガーZ(JS)ロケットパンチ→Bánh xe lớn ロケットパンチ và 18 vật phẩm khác |
| EW Thay đổi thiết bị | `801CF85C` | Năm phân đoạn**Tất cả ≥** Được gọi ở giới hạn trên `800AAD28` Thay đổi thiết bị; đừng nhìn vào vũ khí |
| Tập lệnh `3D6C` | `800ACA1C` (`800ACA74`) | Năm mục được viết là min(N, giới hạn trên) và tất cả vũ khí đều được viết có cùng giá trị |
| Giá bán khung máy bay | Lớp phủ màn hình bán hàng `load_00107BF0` (ROM `0x107BF0`) `801C2600` | Giá = giá cơ bản + 20000 × (số năm giai đoạn + số lượng tất cả các giai đoạn vũ khí) ÷ (giới hạn trên × (số lượng vũ khí + 5)); bảng giá cơ bản `D_801C3A40` (ROM `0x109030`), trong bảng có 12 số máy, có 9 loại máy sản xuất hàng loạt đang được rao bán (ガンキャノン 11000, ガンダム 12000, ガンタンク10000, ジェガン13000, シュツルム・ディアス 13000, リ・ガズィ(BWS) 15000, Ez8 11000, ドール 10000, v.v.); phần tỷ lệ được làm tròn |
| Chuyển đổi kế thừa | `800AAD28`, `800A9A70`, `800AA8C0` | Giới hạn trên được đặt lại trước `800A5254` sau khi sao chép mà không có tác động thực tế ([Phân tích kế thừa chuyển đổi](upgrade-inheritance.md) Phần 5) |
| Sao lưu toàn bộ khối ví dụ | `800ACD5C` | Sao chép cùng với giới hạn trên, không đưa ra phán quyết |

Sau khi sửa đổi vũ khí thành công, `800A5F84` sẽ đồng bộ hóa sức mạnh và số phân đoạn với "vũ khí song sinh" trên cùng một cơ thể: `232 ↔ 254`ビームサーベル（ガンダムmkⅡ／スーパーガンダム）, `873 ↔ 880` 空剣（ダンクーガ hai số). Sau khi năm lần chuyển đổi thành công, `800A5924` sao chép năm phân đoạn sang các biểu mẫu hiện có trong họ kết hợp và họ bị biến dạng, đồng thời gọi `800A5254` cho mỗi biểu mẫu để tính toán lại.

## 6. Bằng chứng gián tiếp và các vấn đề tiềm ẩn

### 6.1 Vũ khí loại 0: Chỉ chặn những vũ khí có sức mạnh 0

Danh sách sửa đổi vũ khí (`801C7254`) chỉ loại trừ vũ khí có bộ `+0x22` bit 1 hoặc 2 (kỹ năng kết hợp có bit 1, bit 2 không được mở khóa); trước khi nhập xác nhận (`801D0970` của `801D087C`), chỉ những vũ khí có **sức mạnh 0** mới bị từ chối. Vì vậy:

- Thiết bị sửa chữa và thiết bị cấp nguồn (nguồn 0) chỉ có âm thanh nhắc nhở khi bấm vào và không thể sửa đổi được;
- Các kỹ năng kết hợp như ツインビーム (vị trí 1) hoàn toàn không có trong danh sách;
- Nhưng vũ khí Loại 0 có sức mạnh lớn hơn 0 không bị chặn. Theo mã, giá là 0 khi được xác nhận, công suất được ghi là giá trị xem trước 0 và số lượng phân đoạn +1. Nguồn điện ban đầu sẽ không được khôi phục cho đến lần tính toán lại `800A5254` tiếp theo.

Loại vũ khí này chỉ xuất hiện bên phía chúng ta ở dạng S của S-Form H, bốn dạng S của Structural Alliance và Bioman. Danh sách lọc vũ khí theo "số máy dạng hiện tại", do đó, miễn là những máy này ở dạng cơ bản trong quá trình chuẩn bị, đường dẫn này sẽ không khả dụng. **Đây là sự cố tiềm ẩn với suy luận tĩnh**, được đăng ký là [WATCH05](original-bug-register.md); MOD nên xử lý rõ ràng loại 0 là "không thể biến đổi" khi tiếp quản logic sửa đổi.

### 6.2 Sửa đổi tài liệu trước đó

[Phân tích kế thừa sửa đổi](upgrade-inheritance.md) Văn bản gốc của Mục 8.3 là "`D_801DC340[上限−5]` Chọn bảng cấp thiết bị của máy bay, sau đó lấy giá theo loại vũ khí." `D_801DC340` thực tế là một bảng chuỗi thanh tỷ lệ. Giá vũ khí chỉ được xác định bởi loại sửa đổi và số lượng phân đoạn hiện tại, và không liên quan gì đến giới hạn trên của cơ thể; "trường danh mục vũ khí" là bản ghi vũ khí `+0x0E`. Mục 3 và 4 của Mục 7 của bài viết này cũng có thể được giải quyết tĩnh bằng bài viết này: Skybreaker 873/880 được đồng bộ hóa bởi `800A5F84` mỗi khi sửa đổi; sức mạnh của thiết bị sửa chữa là 0, và ツインビーム với các kỹ năng kết hợp không thể được sửa đổi một mình và sự vắng mặt của chúng trong bảng bản đồ sẽ không gây ra tổn thất thực tế. Ba sửa đổi đã được thực hiện đối với văn bản gốc.

### 6.3 Số lượng đoạn của ガンダムmkⅡ → スーパーガンダム vượt quá giới hạn

`800A5924` Hai nhóm truyền được mã hóa cứng ở cuối: thân nguồn 56 ガンダムmkⅡ → 61 スーパーガンダム, thân nguồn 158 グレンダイザー → 159~161 mỗi dạng. Giới hạn trên của mkⅡ là 13 và giới hạn trên của スーパーガンダム là 11, vì vậy sau khi mkⅡ được thay đổi thành 12 và 13 cấp, số lượng năm cấp của スーパーガンダム vượt quá giới hạn trên của nó: khả năng là 13 bảng đủ dài và các giá trị bình thường) và không thể thay đổi màn hình. Nếu thang đo được đọc vào chuỗi cấp tiếp theo (giới hạn trên 12) theo `D_801DC340[6][13]` thì sẽ có thang đo bị lệch trên màn hình. Bản thân việc vi phạm giới hạn có thể được xác định một cách tĩnh; hình ảnh thực tế của cân cần được xác nhận bằng máy thật. **Điều này cho thấy phiên bản gốc có trạng thái "số lượng phân đoạn vượt quá giới hạn trên". Các MOD vượt quá giới hạn trên sẽ gặp trạng thái tương tự sau khi tắt công tắc và phương pháp xử lý cũng giống nhau. **

## 7. MOD: Giá trị có thể cài đặt và "Đột phá giới hạn trên" (thực hiện trong giai đoạn đầu)

### 7.1 Cách sử dụng

Hai phần này độc lập với nhau và có thể được sử dụng riêng biệt hoặc đồng thời:

| Phần | Cách mở | Phạm vi hành động |
| --- | --- | --- |
| Đột phá giới hạn trên `upgrade-cap-break` | "Điều chỉnh độ khó" của [quy tắc tùy chọn](rule-fixes.md), bị tắt theo mặc định. Chuyển đổi ngay lập tức "Tùy chọn → Điều chỉnh lối chơi" trong trò chơi hoặc `play_native.py --rule-fixes upgrade-cap-break` | Chỉ màn hình sửa đổi: tất cả các đơn vị có thể được thay đổi thành phân đoạn 15 |
| Nâng cấp tệp quy tắc | `play_native.py --upgrade-rules FILE` (được chỉ định mỗi lần, không được ghi nhớ); lớp dưới cùng là biến môi trường `SRW64_UPGRADE_RULES` | Mỗi mức tăng và giá của năm vật phẩm và bốn loại vũ khí, giới hạn trên ban đầu của bất kỳ thân máy nào và loại sửa đổi của bất kỳ vũ khí nào |

Mẫu tệp quy tắc:

```sh
.venv/bin/python tools/recomp/gameplay/upgrade_rules.py export my-rules.json --units --weapons
.venv/bin/python tools/recomp/gameplay/upgrade_rules.py check my-rules.json
```

`export` Viết ra giá trị ban đầu (`--units`/`--weapons` cũng được gắn với giới hạn trên của tất cả 363 đơn vị và các loại vũ khí 1329, có tên), thay đổi các mục bắt buộc và xóa phần còn lại; mỗi phần và trường có thể được bỏ qua và phiên bản gốc sẽ được sử dụng nếu bị bỏ qua. Định dạng (lược đồ `srw64.upgrade-rules.v1`):

```json
{
  "schema": "srw64.upgrade-rules.v1",
  "stats": {"hp": {"increments": [15 个], "prices": [15 个]}, "en": ..., "mobility": ..., "armor": ..., "limit": ...},
  "weapon_types": {"1": {"increments": [...], "prices": [...]}, "2": ..., "3": ..., "4": ...},
  "unit_caps": [{"id": 124, "name": "ガンダムサンドロック", "cap": 7}],
  "weapon_type_overrides": [{"id": 19, "type": 2}]
}
```

Xác minh (Python giống như máy chủ, các tệp xấu bị từ chối trước khi bắt đầu): Đường cong có đúng 15 mục; mỗi phân đoạn tăng dần từ 0 đến 9999 và tổng của 15 phân đoạn không vượt quá 30000 (giá trị khả năng là u16); giá từ 1 đến 99998 (0 và 99999 là `-----` trọng điểm của giao diện); giới hạn trên 5 đến 15 (thang đo chỉ có 11 tệp này); loại vũ khí 0~4; các trường không xác định sẽ luôn báo lỗi. `increments[n]` là mức tăng của phân khúc n+1 và `prices[n]` là giá từ phân khúc n đến phân khúc n+1.

### 7.2 Hai giới hạn trên

| Mục đích | Sử dụng giới hạn trên nào |
| --- | --- |
| Màn hình sửa đổi: có thể thay đổi lại hay không, giá cả, xem trước, tỷ lệ, "N giai đoạn tối đa" | **Giới hạn trên hiệu quả**: 15 khi kích hoạt đột phá, nếu không thì đó là giới hạn trên của tác phẩm gốc |
| Thay đổi thiết bị EW, vũ khí bổ sung được sửa đổi hoàn toàn, giá bán, `3D6C`, kế thừa thay thế máy | **Giới hạn trên ban đầu** (giá trị ROM hoặc giá trị của tệp quy tắc `unit_caps`) |

`unit_caps` tự thay đổi "giới hạn trên ban đầu", do đó, nó cũng sẽ thay đổi việc xác định EW, vũ khí bổ sung và giá bán; sự đột phá chỉ ảnh hưởng đến màn hình chuyển đổi.

### 7.3 Thực hiện

Mã nằm trong `src/host/upgrade_rules.hpp`, được gói trong `game_hooks.cpp` và được đóng trong `NATIVE_HOOKS` của `generate_cpu.py`.

- **Giá trị**: Sau khi đọc tệp quy tắc, tính toán từng byte khác với ROM (bảng tăng thường trú, bảng giá lớp phủ và bảng xem trước, bản ghi nội dung `+0x20`, bản ghi vũ khí `+0x0E`), vá sau mỗi bản sao ROM: phân đoạn thường trú khi khởi động, mỗi lần đọc `8007F704` (Tải lớp phủ sau khi xác minh byte, bản ghi khung máy bay và vũ khí được đọc). Trò chơi tiếp tục sử dụng bảng riêng, bảng xem trước và bảng thường trú được viết lại đồng thời nên được xác nhận rằng giá trị gia tăng trong quá trình sửa đổi phù hợp với giá trị được tính toán lại sau trong `800A5254`. Các phiên bản vũ khí chỉ sao chép các loại khi được tạo và trình bao bọc cho `800A5254` trước tiên sẽ làm mới `+0x15` theo tệp quy tắc. Khi không có tập tin, bảng vá sẽ trống và không có bộ nhớ nào được ghi.
- **Giới hạn trên**: Mỗi quy trình trong số sáu quy trình sửa đổi màn hình bao gồm một lớp phạm vi - `801CF680` (mở màn hình và in giới hạn trên), `801CF988` (chọn và xác nhận năm mục), nhấn "Có thể thay đổi được không", __INL_COD E_213__ (giá trị, bản xem trước và tỷ lệ của năm mục), nhấn "Hiển thị", `801D0C7C`/`801D1100` (xem trước và xác nhận vũ khí), nhấn "Vũ khí đã chọn", `801CF85C` (Phán quyết EW) theo giới hạn trên của tác phẩm gốc. Khi nhập, hãy ghi `+0x51` của tất cả các máy hiện có vào giới hạn trên của phạm vi và ghi lại khi thoát. Chỉ những byte khác với giá trị hiện tại mới được ghi; `800A5254` sẽ viết lại `+0x51` từ ROM và bao bì của nó sẽ bù đắp cho nó trong phạm vi. Các mã bên ngoài màn hình sẽ luôn chỉ nhìn thấy giới hạn trên của tác phẩm gốc và `+0x51` sẽ không được nhập vào kho lưu trữ (phần 4.3).
- **Vũ khí bổ sung được sửa đổi hoàn toàn**: `801D1100` gọi `800A5F84` sau số phân đoạn +1, rồi so sánh "số phân đoạn = `+0x51`". Bao bì của `800A5F84` điều chỉnh so sánh này khi vũ khí được chọn thuộc `D_801DC87C`: khi số giai đoạn vừa đạt đến giới hạn trên ban đầu, so sánh được coi là hợp lệ (vũ khí bổ sung được mở khóa theo thời gian ban đầu và lời nhắc vẫn như thường lệ), và khi đạt đến giới hạn trên sau khi đột phá, so sánh không hợp lệ (không mở khóa lặp lại).
- **Số đoạn đã vượt quá giới hạn trên**: Sau khi tắt tính năng đột phá, số đoạn đã thay đổi trước đó sẽ được giữ lại. Phạm vi hiển thị mở rộng tỷ lệ đến số phân đoạn hiện có để tránh lấy chuỗi dựa trên số phân đoạn. Phạm vi vũ khí cho phép vũ khí vượt quá giới hạn để xem số phân đoạn của riêng chúng. Màn hình trực tiếp nhắc "これ上の Modificationはできません" và số tiền sẽ không bị trừ trước khi thêm các phân đoạn như so sánh ban đầu. Phiên bản gốc của ガンダムmkⅡ→スーパーガンダム cũng đi theo đường dẫn này (phần 6.3), do đó thang đo không còn bị lệch nữa.
- **Giá bán**: Kết quả `801C2600` của `load_00107BF0` được gắn với "giá cơ sở + 20000", kết quả này sẽ không bao giờ được kích hoạt theo dữ liệu gốc.
- **Tỷ lệ**: Khi bao bì của `8008C510` (bộ mô tả văn bản) và `8007F704` nằm trong phạm vi hiển thị, giới hạn trên hiệu dụng của nội dung hiện tại hoặc số lượng phân đoạn hiện có vượt quá giới hạn trên của tác phẩm gốc, văn bản tỷ lệ được thay thế bằng một chuỗi được đánh vần theo giới hạn trên của tác phẩm gốc: hình tượng gốc ►/▷ được sử dụng trong giới hạn trên của tác phẩm gốc và ● (đã thay đổi) / ☆ (không thay đổi) được sử dụng cho phần vượt quá giới hạn trên của tác phẩm gốc. Khi kích hoạt đột phá, toàn bộ 15 lưới sẽ được rút ra; khi tính đột phá không được kích hoạt, chỉ các phân đoạn hiện có được rút ra.

### 7.4 Kiểm tra

- `make recomp-upgrade-rules-test` (được thêm vào `recomp-native-check`): Sử dụng ROM thực để kiểm tra bảng gốc, số văn bản tỷ lệ và giới hạn trên, xác minh tệp quy tắc bìa, vá byte (bao gồm sao chép một phần), phạm vi bản ghi, làm mới loại, giới hạn trên và lồng của từng phạm vi, `800A5254` điền sau, hai điều chỉnh cho vũ khí bổ sung, kẹp giá bán, hai độ rộng của chuỗi tỷ lệ.
- `tests/test_upgrade_rules.py`: Xác minh Python nhất quán với các hằng số máy chủ, các móc bị ràng buộc, các giá trị và phân phối gốc ROM, các mẫu đã hoàn tất và chỉnh sửa kho lưu trữ được kiểm soát.

### 7.5 Xác minh máy thật (18-09-2026, hoạt động giới hạn, tiếng Nhật, màn hình gốc)

Sử dụng `tools/recomp/gameplay/upgrade_save.py` để thực hiện **chỉnh sửa có kiểm soát** trên kho lưu trữ thẻ tập đầu tiên (quỹ 900000; ダイターン3 ba dạng giai đoạn HP, ダイターンザンバー giai đoạn) và thực hiện 9 giai đoạn đầu tiên trong số `load-intermission-check.json` Mỗi tệp đầu vào được đọc và bị gián đoạn, sau đó màn hình sẽ tắt được sửa đổi bằng thao tác từng phím. Bản thân thư mục chạy không được bảo tồn.

| Chạy | Điều kiện | Những gì bạn nhìn thấy trên màn hình |
| --- | --- | --- |
| `run-on-2` | Đột phá; ダイターン3 (giới hạn trên 7) HP 7 cấp, ザンバー 7 cấp | HP 9400 sau khi nạp (8000 + 7×200); Tiêu đề màn hình “Tối đa 15 cấp độ”; HP giá 16000, xem trước 9400→9600, chia 7 phân chia ► + 8 phân chia ☆. Sau khi xác nhận, HP 9600, vốn 900000→884000, giá kỳ tiếp theo 18000, tỷ lệ 7± + 1● + 7☆.ザンバー 2300 (1300 + loại 2 7 phân đoạn đầu tiên 1000), giá 32000, xem trước 2500, sau khi xác nhận 2500, tiền 852000, đoạn tiếp theo 36000, tỷ lệ 7III+ 1● + 7☆; bảng vũ khí 6 dòng mỗi trang, với `行 + 6×(页−1)` nhất quán |
| `run-off-3` | Đột phá; HP 9 cấp, EN 3 cấp, ザンバー 9 cấp; tệp quy tắc: HP giá 1234, áo giáp +500 mỗi cấp, スイームルグ giới hạn trên 11→13 (bản vá 91 byte) |ダイターン3 tiêu đề "Tối đa 7 giai đoạn", HP hiển thị `-----`, tỷ lệ 7± + 2●, thang EN vẫn giữ nguyên lưới 7 ban đầu; nhấn A trên HP để nhắc "これ上の综合はできません", số tiền không thay đổi; xem trước áo giáp 1800 → 2300, 2300 sau khi xác nhận, vốn −3000 (giá áo giáp ban đầu), vẫn là 2300 sau khi quay lại danh sách và tính toán lại; スイームルグ danh hiệu "Giai đoạn thứ 13 tối đa", HP có giá 1234, 13 ô vuông theo tỷ lệ glyph ban đầu; ザンバー (đoạn 9) trực tiếp nhắc "これ上の cải cáchはできません", quỹ luôn là 897000 |

Không có bản ghi lỗi nào khi chạy máy chủ hai lần (trạng thái `report.json``native-run-ended-by-control`, mã thoát 0) và bản ghi báo cáo lần chạy lần lượt là `rule_fixes` và `upgrade_rules` (đường dẫn tệp và tóm tắt). Lần thử đầu tiên `run-on-1` đã vào nhầm một trò chơi mới và bị loại bỏ.

### 7.6 Hạn chế và Giai đoạn II

- **Đoạn 15 là ranh giới cứng**: độ dài bảng, bảng đánh dấu và định dạng lưu trữ đều kết thúc ở 15. Vượt quá 15 yêu cầu máy chủ có khả năng tính toán lại, định giá, xem trước và chia tỷ lệ, đồng thời lưu các phân đoạn khác 4 chữ số vào bộ sưu tập lưu ([Roadmap](../design/mod-roadmap.md) giao thức lưu trữ của M2), điều này không nằm trong phạm vi của một vấn đề.
- Đột phá là một công tắc chứ không phải một giá trị: tất cả các đơn vị có thể đạt tới 15. Nếu bạn muốn "giới hạn trên ban đầu + N", chỉ cần thay đổi `allowed_cap()` để đọc cài đặt số và yêu cầu điều khiển số trên giao diện ([Cài đặt quy hoạch cửa sổ](../native/settings-window.md) đã được bảo lưu).
- Tệp quy tắc được đọc khi khởi động và không thể thay đổi trong quá trình hoạt động; công tắc đột phá có thể được chuyển đổi bất kỳ lúc nào và sẽ có hiệu lực vào lần tiếp theo bạn vào quy trình của màn hình chuyển đổi.
- Sức mạnh vũ khí được hiển thị bằng 4 chữ số và giá trị bằng 5 chữ số. Giao diện sẽ bị cắt bớt khi file quy tắc đặt giá trị quá lớn. Việc xác minh chỉ đảm bảo rằng nó không tràn u16/u32.

## 8. Những mục còn cần xác nhận bằng máy thật

1. Các vũ khí bổ sung đã được sửa đổi hoàn toàn vẫn được mở khóa ở giới hạn trên của trò chơi gốc khi mở đột phá, các lời nhắc vẫn bình thường và chúng không được lặp lại cho đến màn 15 (bài kiểm tra đơn vị đã bao quát logic; không có cơ khí nào có vũ khí bổ sung trong danh sách của tập đầu tiên và chưa đạt được vòng này).
2. Khi bật đột phá, trang phục EW vẫn được kích hoạt khi cả năm vật phẩm đều đạt đến giới hạn trên của tác phẩm gốc.
3. Liệu có thể đạt được đường dẫn chuyển đổi tự do cho vũ khí Loại 0 trong Mục 6.1 trong quy trình ban đầu không?
4. Bán màn hình kẹp giá sau khi đột phá.
5. Giá tích lũy thực tế của ウイングゼロ ツインバスターライフルMAP (mẫu 140.000, chiến lược 110.000).

Trả về: [Phân tích kế thừa sửa đổi](upgrade-inheritance.md) · [Đăng ký lỗi gốc](original-bug-register.md) · [Sửa quy tắc tùy chọn](rule-fixes.md) · [Lộ trình MOD tích hợp](../design/mod-roadmap.md) · [Chỉ mục tài liệu kỹ thuật](../README.md)