> **Ngôn ngữ / Language:** [Tiếng Việt](original-data-catalog.vi.md) · [English](original-data-catalog.en.md) · [中文](original-data-catalog.md)

# Thư mục dữ liệu trò chơi gốc và tiến trình phân tích cú pháp

Cập nhật: 2026-09-12.

Lô triển khai này chuyển đổi ROM gốc tiếng Nhật thành thư mục chỉ đọc có thể tái tạo và theo dõi để phân tích cấp độ, Mod dữ liệu và đa ngôn ngữ tiếp theo. Đầu ra chứa byte thô, nhận dạng ổn định, địa chỉ nguồn, hàm băm, tham chiếu bảng chéo và độ tin cậy của trường. **Đây chưa phải là ABI dữ liệu trò chơi có thể ghi được; tập lệnh cấp độ đã hoàn thành việc phân tích cú pháp lệnh tĩnh nhưng chưa thực hiện so sánh lần chạy và ghi lại. **

## Chạy

Thực thi trong thư mục gốc của kho:

```sh
.venv/bin/python -B tools/content/extract_original.py
python3 -B tools/data_viewer/serve.py --port 59110
```

Duyệt `http://127.0.0.1:59110/`. Máy chủ chỉ nghe loopback và chỉ cung cấp `assets/original-data/`, không ghi API. Dừng thiết bị đầu cuối để tắt dịch vụ. `story.html` trong cùng thư mục là trình xem cốt truyện đọc văn bản gốc tiếng Nhật theo chương. Dữ liệu đến từ `story/index.json` và `story/NNNN.json`. Xem [Phân tích hoàn chỉnh kịch bản cấp độ](../script/stage-script-exploration.md#剧情查看器).

Tùy chọn thêm ảnh chụp nhanh chương đầu tiên của siêu phẩm nữ hiện có:

```sh
.venv/bin/python -B tools/content/extract_original.py \
  --snapshot build/recomp/gfx-probes/female-map-audio-1/latest-gfx-rdram.bin
```

Khi ảnh chụp nhanh không được cung cấp, quá trình trích xuất không dựa vào thư mục đang chạy lịch sử và danh mục "quan sát tập đầu tiên" sẽ không được tạo. Khi cung cấp ảnh chụp nhanh, bắt buộc phải có `report.json` và `scene-evidence.json` trong cùng một thư mục, đồng thời kiểm tra nhận dạng ROM gốc và ID cảnh. Các quan sát trong thư mục lưu lại các bản băm của ảnh chụp nhanh, báo cáo và mô tả kịch bản. Ảnh chụp màn hình mô tả cảnh không nhất thiết phải giống khung với RDRAM cuối cùng; số khung ảnh chụp màn hình không thể được gán cho ảnh chụp nhanh.

## Phạm vi trích xuất lần này

| Danh mục | Số lượng | Bằng chứng và phạm vi |
| --- | ---: | --- |
| Bản ghi văn bản | 51.174 / 20 bàn | Sử dụng phân tích văn bản ROM gốc độc lập; giữ lại tiêu đề 8 byte, từ điều khiển, trình giữ chỗ tên động và TextKey. Bảng 0 có 50.975 mục và các bảng còn lại có tổng cộng 199 mục. Không phải tất cả văn bản hình ảnh đều hiển thị. |
| Khối tài nguyên | 6.436 | Phân tích cú pháp mô tả, giữ lại khoảng/phần đệm đã nén ban đầu, giải nén tất cả và xuất SHA-256. Giải nén thành công không có nghĩa là mục đích hoặc định dạng hình ảnh đã được xác nhận. |
| Kỷ lục cơ bản về khung máy bay | 363 | Xác nhận đọc bước kích thước 36; số này là bản ghi hoàn chỉnh dựa trên ranh giới của bảng tiếp theo, có khoảng cách 4 byte ở cuối. Tên `527 + unit_id` được xác nhận bằng mã menu, HP, EN, Tính cơ động, Tính cơ động, Giáp, Giới hạn và Chi phí Sửa chữa được xác nhận bằng mã tải và hiển thị. |
| Hồ sơ cơ bản về vũ khí | 1.329 | Xác nhận bước đọc kích thước 16; tên thuần `1370 + weapon_id`, tên menu `2699 + weapon_id`, cả hai đều có cơ sở mã hiển thị. Sức mạnh tấn công, tầm bắn, hiệu chỉnh đòn đánh, số lượng đạn, EN, yêu cầu năng lượng và hiệu chỉnh đòn chí mạng đã được xác nhận; số được xác định bởi ranh giới vật lý và không bằng số lượng tên sau khi loại bỏ trùng lặp. |
| Tên nhân vật và danh tính | 361 | Chữ viết tắt của `4382 + actor_id`, tên đầy đủ của `4743 + actor_id`, được chứng minh bằng hai lần nạp `80081130`. |
| Tính cách→Bản đồ cơ bản/tâm linh | 360 mỗi | Hai bảng thường trú liên tiếp `s16`, mỗi bảng 720 byte. Các giá trị âm được lưu nguyên trạng. |
| Hồ sơ cơ sở tài xế | 257 | Được bao phủ bởi chỉ số không âm trong bản đồ `0..256`, kích thước bậc 16. Sáu khả năng cơ bản, điểm tinh thần, mức tăng trưởng ở mỗi cấp độ và bảy điểm kỹ năng đã có bằng chứng của người tiêu dùng. |
| Kỷ lục ngưỡng kỹ năng | 256 | Bước cỡ 30, khoảng cách vật lý nằm trước thước đo tinh thần. Mỗi nhóm trong số ba nhóm chiếm 10 byte và mỗi vòng lặp cấp độ sẽ đọc 9 byte đầu tiên; việc phân nhóm và lựa chọn tên của các khả năng đặc biệt, cắt り払い và phòng thủ S đã được xác nhận. |
| Hồ sơ mua lại tinh thần | 148 | Chỉ mục ánh xạ `0..147`, kích thước bước 12. Mỗi nhóm sáu `(习得等级, 指令编号)`; tên `969 + command_id` đã được xác nhận và bảng gốc bao gồm 30 hướng dẫn. |
| Cảnh→Bản đồ | 144 khe 2 byte vật lý | Byte đầu tiên là số bản đồ ban đầu; khe hoàn toàn bằng 0 ở cuối có thể được lấp đầy căn chỉnh và mục đích của byte thứ hai là được theo dõi. Không phải số lượng cấp độ có thể chơi được. |
| Bản ghi tài nguyên bản đồ | 158 | Bước kích thước 12; ba vị trí đầu tiên là bố cục, tập bản đồ và bảng màu, và bản đồ cơ sở chiến trường tĩnh đã được tập hợp; nguồn lực phụ trợ sẽ được phân tích sâu hơn. |
| Ứng cử viên tiêu đề chương | 143 | `281..423` trong Bảng 0, bao gồm các tiêu đề trùng lặp/được bảo lưu; không phải là kết luận rằng "trò chơi có tổng cộng 143 cấp độ". |
| Kịch bản cảnh/mục sự kiện | 142 vị trí / 1.812 mục | 131 bảng nhập độc lập; tất cả 1.812 sự kiện được đọc đến ký tự cuối, tổng cộng 67.160 hướng dẫn, 33.582 tham chiếu hội thoại (bao gồm cả người nói), 2.678 khối điều kiện; 73 khe lệnh, 30 hướng dẫn có điều kiện, 12 điểm đánh dấu ngữ cảnh và 15 loại kích hoạt được so sánh lần lượt với mã máy. Xem [Phân tích hoàn chỉnh kịch bản cấp độ](../script/stage-script-exploration.md). |
| Tập lệnh hỗ trợ dữ liệu/bản ghi xuất kích | 138 khối / 6.223 mục | Chỉ mục phù hợp có 144 vị trí; được phân tích cú pháp thành 999 trong 14 nửa từ, các trường từ thứ tự đọc 8020ABB4; 13 khối không được căn chỉnh thành 999, byte gốc được giữ lại. |

Trong bảng vũ khí khung máy bay, 363 con trỏ khung máy bay tương ứng với 266 địa chỉ danh sách khác nhau, tham chiếu 1.182 số vũ khí khác nhau, tối đa là 1.327. Bạn không thể xóa một bản ghi vũ khí khác chỉ vì nó không được tham chiếu trong bộ danh sách này.

## Bằng chứng cấu trúc

Khóa byte bố cục và bằng chứng: `config/data/original-jp-v1.json`. Mối quan hệ giữa địa chỉ thường trú và địa chỉ ROM là `ROM = VRAM - 0x80075610`. Lớp phủ phải được chuyển đổi theo phân đoạn tải tương ứng trong `config/recomp/code-sections.json` và không thể áp dụng phần bù cư trú. Trang duyệt "Bằng chứng phân tích" chứa tên phân đoạn, địa chỉ, byte và hàm băm cho 58 cửa sổ mã/dữ liệu; tháo gỡ thường trú ở `build/recomp/disasm/cpu-main/rom_80076610.text.s` và tháo gỡ lớp phủ ở `build/recomp/cpu-scan/<section>/`.

| Dữ liệu | Điểm bắt đầu của ROM | Đang tải/tiêu thụ mã | Giải thích |
| --- | --- | --- | --- |
| Thân hình | `0x71B80` | `800A6E68`, cuộc gọi đọc ROM `800A6FB8` | Chỉ số nhân với 36, đọc `0x24`. Bản ghi gốc +0/+2 được sao chép sang thời gian chạy +4/+6 và +8/+10; sau đó hiển thị sau bộ đệm `load_0008F4B0:801C4DE4` và `801C6E64`, xác nhận HP/EN. |
| Vũ khí | `0x74E90` | `800A642C`, được gọi là `800A6448` | Chỉ mục nhân với 16. `800A6A18..800A6A30` Nhân +1 byte ban đầu với 100 và ghi thời gian chạy +6; trang trạng thái `load_000AB160:801E6410` hiển thị giá trị này theo nhãn sức mạnh tấn công. |
| Kiến thức cơ bản về trình điều khiển | `0x7A1A0` | `800A6398` | Diễn viên được ánh xạ bởi `s16[800CA9C4 + actor*2]` và nhân với 16. Sáu byte +1..+6 được ghi vào sáu trường u16 trong thời gian chạy, thứ tự được xác nhận: chiến đấu, bắn, tránh, đánh, phản ứng, kỹ năng. |
| Ngưỡng kỹ năng | `0x7B1B0` | `800A6340` | Sử dụng cùng một ánh xạ bản ghi cơ sở, sau đó nhân với 30; tính tiếp theo theo cấp độ. |
| Tiếp thu tinh thần | `0x7CFB0` | `800A63E0`, `800A8098` trở đi | diễn viên được ánh xạ bởi `s16[800CA6F4 + actor*2]`; các giá trị âm bị bỏ qua. Sáu bộ bản ghi so sánh mức hiện tại và nối thêm số lệnh. |
| Danh sách vũ khí máy bay | `0x7E210` | `800A67C8`, `800A68BC` | `base + u32[base + unit*4]` trỏ tới luồng bản ghi 12 byte; u16 đầu tiên là ID vũ khí và năm u16 còn lại phù hợp với các khe dạng khung máy bay. Toàn bộ bản ghi có trường đầu tiên FFFF là mục kết thúc. |

Năm vị trí biểu mẫu được sao chép từ `800A6AC8..800A6AE0` sang vũ khí thời gian chạy +0x18..+0x20. `load_0008F4B0:801C72C0..801C7314` được so sánh từng mục với ID cơ thể hiện tại, sau đó cũng kiểm tra cờ `0x600` của vũ khí thời gian chạy +0x22. Trình phân tích cú pháp thêm `eligible_unit_ids` (lọc FFFF), giữ lại `remaining_u16` năm vị trí ban đầu và byte hoàn chỉnh; kết hợp hình thái không phải là một vũ khí hoàn chỉnh có sẵn để xác định. Bản thân danh sách này có thể bao gồm các loại vũ khí được sử dụng dưới các hình thức khác. Trang này cho biết "Vũ khí có thể tải được (bao gồm cả các biểu mẫu dùng chung)" và không thể được sử dụng trực tiếp làm danh sách vũ khí trong menu biểu mẫu hiện tại.

Lô bằng chứng ngữ nghĩa mới thứ hai:

| Hiệp hội/lĩnh vực | Đang tải phân đoạn và địa chỉ chính | Chuỗi bằng chứng |
| --- | --- | --- |
| Tên cơ thể | `load_0008F4B0:801C6DD0..801C6DEC` | Bản ghi nội dung thời gian chạy 84 byte +2 → Thêm `0x20F` → Hiển thị văn bản `8008D0E8`. |
| Tên thuần vũ khí | `load_00216730:801C2928..801C2A30` | U16 đầu tiên trong danh sách vũ khí cơ thể ban đầu → thêm `0x55A` → hiển thị văn bản. `load_000AB160:801E7B44..801E7BA4` cũng sử dụng công thức này. |
| Tên menu vũ khí | `load_0008F4B0:801C76B8..801C77BC` | Mảng vũ khí thân +0x30, kích thước bước 36, bản ghi +2 → thêm `0xA8B` → hiển thị văn bản. Giữ nguyên các dấu hiệu ban đầu như lưới/bắn/P và không suy ra hành vi của vũ khí từ tên. |
| Tên thần | `load_0008F4B0:801C9D84..801C9DB4` | Bước trình điều khiển kích thước 76, khe linh hồn bắt đầu từ +0x0B → số lệnh cộng với `0x3C9` → hiển thị văn bản. Số 0 là tự hủy, 29 là hồi sinh. |
| Chi phí sửa chữa | `load_000AB160:8020D894..8020D8DC` | Văn bản 933 "Chi phí sửa chữa" hiển thị nội dung thời gian chạy +0x1C bên cạnh nó; `800A709C..800A70A8` sao chép u16 từ bản ghi gốc +0x14. |

Lô ngữ nghĩa và mã hóa số thứ ba:

| Bảng | Loại và độ lệch bản ghi gốc | Lời giải thích được xác nhận |
| --- | --- | --- |
| Đơn vị | `+0 u16`, `+2 u16`, `+6 u8`, `+8 u16`, `+A u16`, `+C u16`, `+14 u16` | HP, EN, tính cơ động, tính cơ động, áo giáp, giới hạn, chi phí sửa chữa. Tất cả đều là những giá trị cơ bản, trang bị, trạng thái tinh thần và những sửa đổi được bao gồm riêng biệt. |
| Vũ khí | `+1 u8 × 100`, `+2/+3 u8`, `+4 s8`, `+5 s8`, `+6/+7 u8`, `+D s8` | Sức tấn công, phạm vi tối thiểu/tối đa, hiệu chỉnh đòn đánh, số lượng đạn, mức tiêu thụ EN/năng lượng yêu cầu, hiệu chỉnh đòn chí mạng. Số lượng đạn `FF` được dành riêng cho cờ giới hạn không có bom của `-1`. |
| Tài xế | `+1..+6 u8`, `+C u8` | Chiến đấu, bắn súng, né tránh, đánh, phản ứng, kỹ năng, điểm tinh thần tối đa. Bắt đầu từ cấp độ 1, chiến đấu/bắn súng/phản ứng/kỹ năng +1 mỗi cấp độ, né tránh/đánh/điểm tinh thần tối đa +2 mỗi cấp độ. |

Cơ sở không phải là giá trị số có vẻ hợp lý mà là mối quan hệ giữa bản ghi gốc → trường thời gian chạy → tọa độ hiển thị và nhãn văn bản. Các bảng thẻ thường trú ROM `0x518C0` (máy bay), `0x51968` (phi công), `0x51A80` (vũ khí) đều giữ lại khóa byte. Trạng thái cho thấy người tiêu dùng đang ở `load_000AB160:801E517C / 801E6410 / 801E6C5C`; chu kỳ tăng trưởng diễn ra trong `800A6238`. Cú đánh/tránh cơ bản của người lái xe và tổng giá trị giao diện phải được tách biệt và giao diện cũng sẽ thêm giá trị nội dung.

Có bảy ô kỹ năng được giải thích dành cho người lái xe `+F`: `01` Cắt り払い, `02` Phòng thủ S, `04` Sức mạnh cơ bản, `08` NT, `10` Tăng cường thế giới, `20` Chiến binh thần thánh, `40` siêu năng lực; `80` không giải thích được. Ba nhóm ngưỡng kỹ năng, mỗi nhóm chiếm 10 byte, nhưng `800A80F0` chỉ đọc 9 mục đầu tiên trong mỗi nhóm và đếm số mục đáp ứng `0 < 阈值 <= 当前等级`. Nhóm đầu tiên tương ứng với mặt nạ `7C` và tên được chọn theo mức độ ưu tiên của `04→08→10→20→40`; nhóm thứ hai và thứ ba tương ứng với `01`, `02`. Byte cuối cùng của mỗi nhóm là 0 trong tất cả 256 bản ghi gốc, công cụ này giữ lại và không thể hiểu là cấp 10. Liên kết văn bản gốc của tên giữ lại kết quả giải mã của danh sách ký tự hiện có; các ký tự bị nghi ngờ bị nhận dạng sai trong danh sách ký tự chưa được viết lại mà không được phép trong đợt này.

Lô cảnh thứ ba được liên kết với bản đồ:

- `load_000AB160:80209D6C` đọc ROM `0x102110` với chỉ mục cảnh là `8010F5F0`, kích thước bước 2 và ghi byte đầu tiên vào chỉ mục bản đồ hiện tại `8010F5EE`. Ranh giới ký hiệu liền kề chứa 144 vị trí; đuôi `00 00` có thể là phần đệm và không thể được sử dụng để yêu cầu 144 cấp độ.
- `load_000AB160:801C6EFC` đọc ROM `0x10267C` với chỉ mục bản đồ, kích thước bước 12, đến `0x102DE4`, tổng cộng 158 mục. Năm u16 được chuỗi tải tài nguyên tiêu thụ và hai chiếc bị bỏ qua khi số phụ là 0; ý nghĩa đầy đủ của hai byte đuôi vẫn chưa được giải thích.
- Chỉ số cảnh của ảnh chụp lịch sử tập đầu tiên của Phụ Nữ là 1, chỉ số bản đồ là 20; các tài nguyên tương ứng là **6284, 6228, 6243, 6422, 6429**. Toàn bộ bảng tài nguyên bản đồ trong ảnh chụp nhanh nhất quán với các byte ROM. Điều này xác nhận mối quan hệ chỉ mục và tài nguyên, nhưng không phải là lời giải thích đầy đủ về lưới bản đồ, sự kiện và tổ chức.
- Lối vào hiện trường chiến thuật là do cư dân `800801A4` chọn `801E022C / 801E0268 / 801E028C / 801E0350` trong `load_000AB160`, rồi nhập `801E00AC`. Ngoài ra, cư dân `8009DD58 → 8009DBE4 / 8009DC58` tải dữ liệu của ROM `0x1E3FE0` và `0x19BF10`, được dành riêng làm điểm vào cho bước phân tích luồng sự kiện tiếp theo và chưa được xuất ra dưới dạng tập lệnh được dịch ngược.

Hiện tại, vẫn còn tồn tại ba loại vấn đề ranh giới:

1. Vùng tên có 361 mục và hai bảng ánh xạ, mỗi bảng có 360 mục. Tên của ký tự 360 có thể được hiển thị nhưng bảng tiếp theo sẽ không được đọc ngoài giới hạn để làm giả dữ liệu trình điều khiển.
2. Bản ghi cơ sở ánh xạ Người 284 256. Công thức tải ngưỡng `0x7B1B0 + 256*30` rơi ngay vào bảng tinh thần `0x7CFB0`. Giữ ngoại lệ này; bạn cần theo dõi luồng điều khiển sau để xác nhận xem đường dẫn có thể truy cập được hay không. Bạn không thể chỉ kết luận rằng trò chơi gốc có lỗi dựa trên điều này.
2026-10-01 Xác nhận tĩnh **có thể truy cập**, đang chờ máy thật: ký tự 284 là クェス của chúng tôi (`3D5A` được đăng ký là 284; kẻ thù クェス là ký tự 55, sử dụng dòng thông thường 42), `800A7F8C`/`800A80F0` Không có kiểm tra ranh giới khi đọc ngưỡng và byte ở đầu bảng thu thập tinh thần được đọc. Cấp độ kỹ năng = số `0 < 阈值 ≤ 当前等级` trong 9 ngưỡng, được tính dựa trên các byte sau: NT `1,11,4,5,7,18,9,23,12` → Cấp 1 L1, Cấp 23 L9; Cắt `32,22,1,11,2,5,10,12,21` → Cấp 32 L9; Phòng thủ S `26,4,48,25,1,7,9,25,18` → Cấp 48 L9. Xác nhận máy thực tế tối thiểu: Sau khi クェス tham gia, hãy kiểm tra xem trang trạng thái có hiển thị NT L9 ở cấp 23 hay không.
3. Khoảng cách từ khu vực con trỏ vũ khí đến trọng tải đầu tiên là `0x5B0`, tương đương với 364 u32. Hiện tại, 363 thi thể đã được đọc; Từ ranh giới cuối cùng và khoảng trống ở cuối bảng nội dung vẫn chưa được giải thích và số lượng bản ghi là kết quả của sự phân chia khoảng vật lý hiện tại.

## Nữ Siêu Series Chương 1 Quan Sát

JP ROM RDRAM gốc của `female-map-audio-1` đã được sử dụng và quá trình giải nén hiện tại không khởi động trò chơi. Trạng thái cuối cùng của báo cáo lịch sử là `native-run-failed`, mã thoát `-10`; nó có thể được sử dụng để nghiên cứu bộ nhớ đã lưu và không thể được sử dụng để khẳng định rằng phiên bản hiện tại đã được chấp nhận để chạy hoặc thoát.

Điểm bắt đầu của mảng khi máy đang chạy là `0x8016A210`, mỗi thanh là 84 byte, mỗi dãy có 140 slot. Đọc bản ghi được phân bổ với trạng thái 1, số lượng trình điều khiển dọc theo +0x34 và con trỏ từ +0x38 được liên kết với bản ghi trình điều khiển 76 byte. Liên kết này có cơ sở mã trong `800A7C08` và đường dẫn gọi của nó.

| ID máy bay được chỉ định | Tên | ID diễn viên thí điểm |
| --- | --- | --- |
| 36 | スイームルグ | 28 マナミ、24 ローレンス |
| 216 | ダイターン3 | 165 nghìn feet |
| 218 | ダイファイター | 1,65 triệu feet, dùng chung con trỏ điều khiển |
| 217 | ダイタンク | 1,65 triệu, dùng chung con trỏ driver |

Bốn bản ghi phân bổ này không bằng bốn đơn vị tấn công bản đồ. Có 12 bản ghi khung máy bay ngân hàng 1 khác trong ảnh chụp nhanh; chúng cũng chỉ được chỉ định trạng thái tại thời điểm này và không thể thay thế các trình kích hoạt sự kiện, quân tiếp viện hoặc tập lệnh của kẻ thù.

`unit 36 → weapons 160..163`; `actor 28 → pilot_stats 18 → thresholds 18` và `actor 28 → spirits 13` có thể chuyển từng mục trên trang. Các danh tính như nhân vật, vũ khí vẫn giữ nguyên số gốc và không thể sao chép hoặc đánh số lại theo tên đã dịch.

## Tệp tích hợp khung máy bay/phi công

Khi duyệt trang chủ, "Đơn vị" và "Thí điểm" là các lối vào chính; cảnh, tài nguyên và mỗi bảng gốc được lưu trữ trong các danh mục phụ trợ có thể mở rộng. Các liên kết sâu `base:units:NNNN`, `base:actors:NNNN` hiện có và bảng gốc vẫn hợp lệ.

- **Tệp đơn vị**: Thẻ khả năng cơ bản, bảng vũ khí có tên và thông số cũng như các biểu mẫu liên quan trong danh sách vũ khí dùng chung. Phân biệt vũ khí phù hợp với hình thức hiện tại với vũ khí hình thức khác theo năm vị trí hình thức ban đầu; cái sau được gấp lại và hiển thị. Phù hợp vẫn không có nghĩa là đáp ứng mọi điều kiện sử dụng.
- **Hồ sơ thí điểm**: tên viết tắt/tên đầy đủ, sáu khả năng và điểm tinh thần, mức tăng trưởng ở mỗi cấp độ, sáu tiếp thu tinh thần và cấp độ tiếp thu L1-L9 của từng kỹ năng được kích hoạt. Các nhân vật liên kết các bản ghi cơ sở, tinh thần và ngưỡng thông qua ánh xạ của riêng họ và ID tác nhân không thể được sử dụng trực tiếp làm chỉ mục trong các bảng này.
- **Cùng tên và ánh xạ trống**: 361 danh tính tên được bảo lưu tương ứng; 264 trong số chúng được liên kết với các bản ghi khả năng cố định, có thể được lọc theo "Chỉ hiển thị các phi công có khả năng liên quan". Ánh xạ của các số âm, các dị thường về ranh giới ngưỡng cho người 284 và ánh xạ bị thiếu cho người 360 vẫn được bảo tồn rõ ràng mà không có khả năng đoán hoặc đệm bằng 0.
- **Tìm kiếm**: Máy bay hỗ trợ tìm kiếm theo tên vũ khí và tên mẫu tham chiếu; Phi công hỗ trợ tên đầy đủ, tên tinh thần và tên kỹ năng. Vẫn có thể tìm kiếm theo ID ổn định.
- **Cơ sở gốc**: Mục nhập bảng gốc được giữ lại bên dưới mỗi tệp tích hợp và các trường, byte và bằng chứng chi tiết được thu gọn theo mặc định. Các bảng ban đầu về vũ khí/tinh thần/khả năng/ngưỡng, v.v. cũng cung cấp các liên kết quay lại các tệp tích hợp có liên quan.
- **Mối quan hệ chuyến bay**: Chỉ tóm tắt mối quan hệ hai chiều giữa máy bay/phi công khi cung cấp ảnh chụp nhanh lịch sử, đánh dấu rõ ràng quan sát tại thời điểm đó và liên kết nguồn của ảnh chụp nhanh; nó không được coi là quy tắc ghép nối cố định cho toàn bộ trò chơi.

Việc tích hợp được tạo bởi `src/srw64_native/original_profiles.py` và kết quả được đính kèm với `profile` của bản ghi gốc. Đây là dữ liệu hiển thị chỉ đọc và không thay đổi `fields`, `raw_hex`, ánh xạ và nhận dạng ban đầu. `search_terms`, `summary`, `has_stats` nhập chỉ mục hạng nhẹ và trang không cần yêu cầu lần lượt các bảng dữ liệu khác để ghép các tệp. Tạo mã để tham gia khóa byte của nhà sản xuất của tệp kê khai.

Cấp độ kỹ năng không chỉ đơn giản được đánh dấu theo các ô trong mảng ban đầu. Chương trình ban đầu đếm tất cả các mục đáp ứng `0 < 阈值 <= 当前等级`; nó sắp xếp các ngưỡng hợp lệ trong số chín mục trong khi hiển thị, do đó, nó có thể xử lý chính xác các ô số 0 không hợp lệ, các ngưỡng không tăng và đồng thời bổ sung nhiều cấp độ kỹ năng vào cùng một cấp độ. Thứ tự ban đầu vẫn còn trong bản ghi ngưỡng.

## Tất cả các khả năng đặc biệt và kỹ năng đặc biệt

Hai mục mới đã được thêm vào trình duyệt: "Khả năng đặc biệt của máy" và "Kỹ năng đặc biệt của nhân vật". Mỗi mục nhập liệt kê tất cả chủ sở hữu ban đầu và cho phép bạn quay lại tệp. Thẻ khả năng và tên kỹ năng trong hồ sơ được liên kết trở lại bản tóm tắt. Hỗ trợ tìm kiếm theo tên tiếng Nhật, định nghĩa tiếng Trung, phân loại hoặc tên chủ sở hữu. Định nghĩa tiếng Trung chỉ là công cụ hỗ trợ tìm kiếm/hiển thị cho danh mục và không viết lại văn bản gốc.

Quá trình quét cơ thể bao gồm tất cả **363** bản ghi gốc: `+0x1C u32` bit khả năng đặc biệt và `+0x18 u8` bit thiết bị, tổng cộng **22** danh mục, **429** liên kết giữ bản ghi; 109 bản ghi không có hai cờ tổ chức này. Sự xuất hiện thực sự của các bit trong bản ghi gốc sẽ bị ghi đè; điều này không có nghĩa là hành vi hoàn chỉnh của tất cả các trường khác, phần bổ sung sự kiện và các chức năng đặc biệt đã được giải quyết.

| Phân loại | Các mục có tổ chức (dấu ngoặc đơn là số nội dung/biểu mẫu gốc) |
| --- | --- |
| Mẫu | Thay đổi hình dạng (60), tách (11), kết hợp (27) |
| Trả lời | Hồi HP 10% (10), Hồi HP 20% (4) |
| Tránh né | Bản sao (26), マッハスペシャル (1), thật マッハスペシャル (1), ゴッドシャドー(2), ゲッタービジョン(1), Shunphanzu(3), ハイパージャマー(3) |
| Khiên | Tôiフィールド(11), ビームコート(7), プラネイトディフェンサー(3), オーラバリア(23) |
| Hỗ trợ và tải | Thiết bị sửa chữa (10), thiết bị cung cấp (3), chức năng làm mẹ/tải (11) |
| Tăng cường | Tăng cường sức mạnh (4): Việc xác định và tăng mã đã được xác nhận; Sự tương ứng với tên dòng V-MAX vẫn được đánh dấu rõ ràng là một ứng cử viên |
| Điều kiện thiết bị | Cắt trang bị tương ứng (147), trang bị lá chắn (61) |

Bằng chứng đặt tên xuất phát từ bảng hiển thị 16 mục của `load_000AB160:8021818C` (ROM `0x100CEC`, mỗi mục trong số `u32 mask / u16 text_id / u8 width / u8 reserved`). Trang trạng thái `801E5400..801E5480` sử dụng nội dung thời gian chạy `+0x28` và mặt nạ, sau đó hiển thị văn bản; cư dân `800A70EC..800A70F8` sao chép nội dung gốc `+0x1C` vào trường này. Một trường thiết bị khác được sao chép từ bản ghi gốc `+0x18` sang thời gian chạy `+0x20` thông qua `800A70BC..800A70C8`. Định nghĩa dựa trên vị trí/mặt nạ đánh dấu và không đoán khả năng từ tên của máy bay.

- **Trả lời của HP**: Bit `0x4` và `0x8` chia sẻ văn bản giao diện gốc 1027, nhưng `801FA544..801FA57C` lần lượt được chuyển vào 10.0 và 20.0; `801FA324..801FA3D8` xác nhận phản hồi theo tỷ lệ phần trăm của HP tối đa và cắt bớt phần ghi lại sau khi giới hạn. Khi cả hai được đặt cùng lúc, mức độ ưu tiên của nhánh là 10%. Tập hợp giữ lại các chủ sở hữu khác nhau và không được hợp nhất thành một mục "trả lời" không phân biệt.
- **Lớp tránh**: Mặt nạ dùng chung của `801F6C44` là `0x163011`; sau khi sức mạnh của phi công chính đạt tới 130, cần xác định ngẫu nhiên để đáp ứng điều kiện. Bản tóm tắt trình bày vị trí nắm giữ ban đầu, không mô phỏng xem mỗi trận chiến có được kích hoạt hay không, cũng không chỉ đơn giản là áp đặt nhiều bản sao.
- **Sửa chữa/Cung cấp**: Bit `0x400 / 0x8000` được truy vấn bởi `801F07A8 / 801F044C` tương ứng, menu `801CA394..801CA444` được liên kết với văn bản 518/519 của ROM `0x106918 / 0x10691C`. Các lệnh thực tế vẫn bị giới hạn bởi trạng thái mục tiêu và hành động.
- **Cải thiện sức sống**: Khi bit `0x10000`, sức sống >=130 và không có trạng thái nâng cao, hãy gọi `801FE9CC` qua `801FF2A0..801FF2F8`, đặt trạng thái và thêm chuyển động 1, độ linh động 20, giới hạn 100 và thêm lớp phủ tia `0x200`. 7 giá đỡ lớp phủ dầm ban đầu trong bản tóm tắt không bao gồm các bộ phận được thêm vào trong quá trình vận hành. Tên dòng V-MAX là một sự tương ứng phù hợp và không thể được coi là sự xác nhận về mặt ngữ nghĩa rằng tất cả các biến thể có liên quan đã được hoàn thiện.
- **Làm mẹ**: Bằng chứng đăng ký và tải danh sách sử dụng của vị trí `0x80000` lần lượt ở `801DC170..801DC1CC` và `8020C664`; ở đây chỉ xác nhận phân loại chức năng và không suy ra khả năng tải hoặc danh sách tải hoàn chỉnh.
- **Tách trang bị và kỹ năng**: Việc cắt đứt yêu cầu ô trang bị máy móc 1, ô kỹ năng phi công 1, cấp độ kỹ năng khác 0 và điều kiện loại tấn công (`801F6D5C..801F6DB4`); phòng thủ bằng lá chắn yêu cầu ô trang bị máy 2, ô kỹ năng phi công 2 và cấp độ khác 0 (`801F7020..801F7068`). Ví dụ: thân 216 có tấm chắn nhưng máy bay mẫu 218 thì không. Thiết bị không thể được kế thừa tự động giữa các biểu mẫu được chia sẻ.

Bản tóm tắt nhân vật giữ lại tất cả **361** danh tính, trong đó 264 danh tính được liên kết với các khả năng cố định; 97 không liên kết và không được tính là "không có kỹ năng". Trong số 264 danh tính có khả năng được ghi lại, 99 danh tính không có bộ cờ kỹ năng bảy loại. Tổng cộng **314** kỹ năng được liên kết; danh tính của các bản ghi có cùng tên hoặc giá trị chung được giữ lại riêng và số lượng bản ghi giá trị độc lập được liệt kê riêng trên trang.

| Kỹ năng | Cờ Giữ Bản Sắc | Có ngưỡng hợp lệ | Tất cả ngưỡng 0 | Ngưỡng Không Liên Kết |
| --- | ---: | ---: | ---: | ---: |
| 杀り払い | 140 | 138 | 1 | 1 |
| Phòng thủ S | 91 | 87 | 3 | 1 |
| Sức mạnh đáy | 23 | 23 | 0 | 0 |
| NT | 27 | 26 | 0 | 1 |
| Tăng cường thế giới | 15 | 15 | 0 | 0 |
| Thánh chiến binh | 10 | 10 | 0 | 0 |
| Siêu năng lực | 8 | 8 | 0 | 0 |

Ba "ngưỡng không tương quan" đều thuộc cùng một dị thường ranh giới của ký tự 284 chứ không phải ba ký tự khác nhau. Ưu tiên tên cho bộ kỹ năng đầu tiên được giữ lại; ngưỡng dương tính mức thu thập đầu tiên và mức cao nhất với ngữ nghĩa đếm và các ngưỡng hoàn toàn bằng 0 không có vẻ là có thể học được. Bit kỹ năng `0x80` không xuất hiện trong bản ghi cơ sở gốc hiện tại và trình phân tích cú pháp vẫn giữ lại bit không xác định này.

`original_abilities.py` Thêm các phép chiếu chỉ đọc sau khi tạo tệp: `profile.abilities / ability_flags`, `definition_key / equipment_note` của kỹ năng và `unit_abilities / pilot_skills` hai thư mục. Các byte, trường, tên hoặc ánh xạ của bản ghi gốc không bị ghi đè. Xác định bảng hiển thị/khoảng mã ban đầu và liên kết bằng chứng mà mục nhập được giữ lại, `manifest.ability_coverage` liệt kê số lần quét đầy đủ và các nhận dạng bit không được liên kết, bỏ gắn cờ, không xác định. Nó không thuộc về lược đồ Mod Write thời gian chạy.

## Đầu ra, mô-đun và kiến trúc tiếp theo

- `src/srw64_native/original_data.py`: phân tích bảng ROM, kiểm tra ranh giới, các mối quan hệ tham chiếu và quan sát ảnh chụp nhanh tùy chọn; không ghi ROM, không nhập UI.
- `src/srw64_native/original_abilities.py`: Định nghĩa về khả năng/trang bị cơ thể, chỉ số nắm giữ kỹ năng nhân vật, liên kết tệp hai chiều và kiểm tra phạm vi phủ sóng hoàn chỉnh; các bit chưa biết sẽ không bị loại bỏ.
- `tools/content/extract_original.py`: xác minh khóa, tạo thư mục hợp nhất, giải nén tài nguyên gốc, kiểm tra tham chiếu đầy đủ.
- `tools/data_viewer/web/`: HTML/CSS/JS chỉ đọc mà không phụ thuộc vào mạng của bên thứ ba; `app.js` quản lý các danh mục và điều hướng, `profiles.js` hiển thị các tệp tích hợp, `ui.js` cung cấp các thành phần DOM bảo mật được chia sẻ. Hỗ trợ tìm kiếm, lọc khả năng, phân trang, bản ghi liền kề, liên kết băm ổn định và tải xuống tài nguyên.
- `tools/data_viewer/web/abilities.js`: Tất cả những người nắm giữ khả năng/kỹ năng, phân loại tiếp nhận và mô tả phạm vi bảo hiểm.
- `assets/original-data/manifest.json`: ROM nguồn, bố cục, mã sản xuất và băm tệp đầu ra, số lượng, phạm vi kiểm tra và các mục chưa được xác nhận.
- `records/*.jsonl`: bản ghi đầy đủ về mức tiêu thụ dụng cụ; văn bản `text_ir` giữ nguyên lược đồ bản ghi không mất dữ liệu. `indexes/` và `details/` cứ 256 mục nhập là định dạng bộ đệm trang.
- `raw/resources/*.bin`: Toàn bộ dữ liệu đã giải nén. `raw/resource-spans.bin`: Ghép tuần tự các nhịp đã nén ban đầu; mỗi bản ghi tài nguyên giữ lại phần bù gói, độ dài nhịp và địa chỉ ROM gốc.

Thư mục bản dựng chỉ được phép nằm trong thư mục con `build/` riêng biệt. Các thư mục hiện tại phải có lược đồ tệp kê khai phù hợp trước khi có thể thay thế chúng; hoàn thành việc phân tích cú pháp và kiểm tra tham chiếu trước khi xuất bản kết quả đầu ra. Nội dung gốc vẫn còn trong thư mục bản dựng, bị Git bỏ qua.

Lớp Mod tiếp theo sẽ sử dụng một lược đồ định nghĩa được xác nhận về mặt ngữ nghĩa khác; không sử dụng trực tiếp trường `raw_hex` này hoặc trường ứng viên làm cấu hình có thể ghi. Thứ tự đề xuất:

1. Tiếp tục xác nhận khả năng thích ứng với địa hình, đánh dấu vị trí, điều kiện đặc biệt để phát triển, sửa đổi/chuyển hóa và điều kiện sẵn có của vũ khí; Loạt giải thích về các giá trị số chính và chuyển đổi đơn vị này đã được hoàn thành.
2. Cấp độ IR đã được đọc hoàn toàn (luồng sự kiện, tham chiếu văn bản, nhóm tăng cường, chiến thắng và thất bại và các lệnh tuyến đường đều có giải thích tĩnh); Bước tiếp theo là so sánh việc theo dõi tập lệnh thời gian chạy với diễn giải tĩnh, cũng như cấu trúc bên trong của bản đồ (địa hình, các lớp phụ trợ).
3. Sử dụng một tham số cơ thể, một mức độ tiếp thu tinh thần và một sự kiện để thực hiện thay thế có thể phục hồi tối thiểu, kiểm tra nó trong quá trình chạy tự nhiên im lặng; mở lược đồ Mod tương ứng sau khi chuyển nó.

Gói ngôn ngữ tiếp tục sử dụng `base:tNN_NNNNN` và hàm băm văn bản gốc, đồng thời định nghĩa ký tự/nội dung đề cập đến tên thông qua TextKey. Hình ảnh và sự thay thế 3D thuộc về các trục tài nguyên độc lập và ngôn ngữ, chuyển đổi chất lượng hình ảnh và giá trị trò chơi không bị ràng buộc với nhau.

## Phạm vi chấp nhận "phân tích cú pháp đã hoàn thành"

Mục tiêu là làm cho nội dung gốc có thể tái tạo, dịch được và có thể sửa đổi ký tự/máy/cấp độ. recomp giữ lại logic thực thi của chương trình gốc và có thể cung cấp bằng chứng tải và tiêu thụ, nhưng không tự động khôi phục ý nghĩa của tên trường, mô hình dữ liệu hoặc hướng dẫn sự kiện.

| Lĩnh vực | Đã có nền tảng | Phải hoàn thành trước khi hoàn thành |
| --- | --- | --- |
| Văn bản và ngôn ngữ | 20 bảng văn bản không mất dữ liệu IR, tên liên kết TextKey | Kiểm soát phạm vi ngữ cảnh từ và cuộc gọi, thư viện phông chữ và danh sách văn bản hình ảnh, chuyển đổi tiếng Nhật/tiếng Trung và chấp nhận cảnh dự phòng. Trích xuất văn bản gốc không có nghĩa là hoàn thành bản dịch. |
| Nhân vật, cơ thể, vũ khí, tinh thần | Đã sửa bảng, tên, giá trị cơ bản chính, tăng cấp độ tuyến tính, nhóm kỹ năng và mối quan hệ giữa các bảng | Các trường và cờ bit còn lại, các điều kiện tăng trưởng/chuyển đổi/biến dạng đặc biệt, giá trị âm và luồng kiểm soát chỉ mục bất thường tạo thành một mục định nghĩa có thể ghi theo từng mục. |
| Cấp độ | Ứng cử viên tiêu đề chương, cảnh → bản đồ → tài nguyên, bản đồ cơ sở chiến trường tĩnh, mối quan hệ ký ức lịch sử của tập đầu tiên, lệnh sự kiện hoàn chỉnh IR (khối điều kiện, đoạn nhân vật chính, người nói, loại kích hoạt, luồng lộ trình `3D4B`, bản ghi xuất kích) | Sự tương ứng hoàn chỉnh giữa tiêu đề và ID cảnh, thuộc tính địa hình và các lớp phụ trợ, hiệu ứng trò chơi của các lệnh hiệu suất bản đồ, so sánh theo dõi tập lệnh thời gian chạy và diễn giải tĩnh, tái thiết chưa sửa đổi và xác minh thay thế sự kiện đơn lẻ. |
| Hình ảnh, mô hình và các tài nguyên khác | bộ mô tả, giải nén hoàn toàn và khóa byte, hình đại diện 361 ký tự/363 biểu tượng bản đồ cơ thể/158 liên kết bản đồ cơ sở | Bản đồ chiến đấu và các loại tài nguyên cũng như vị trí sử dụng khác, thông số kỹ thuật thay thế và xác minh chuyển đổi nguồn gốc/HD. |
| Liên kết viết mod | Thư mục chỉ đọc và danh tính ổn định | Xác định lược đồ, kiểm tra tham chiếu và phạm vi, tính nhất quán khi ghi lại chưa sửa đổi, sửa đổi và khôi phục đơn lẻ, xác minh trò chơi im lặng. |

Mỗi miền được chấp nhận theo "trích xuất không mất dữ liệu → giải thích trường và hướng dẫn → đóng tham chiếu → xây dựng lại mà không thay đổi → sửa đổi và chạy xác minh". Các byte/opcode không xác định phải được bảo tồn và đánh dấu rõ ràng; chúng không thể được ngụy trang thành các trường được phân tích cú pháp. Vẫn còn nhiều công việc đáng kể về các tập lệnh cấp độ và ngữ nghĩa trường còn lại; Việc phân tích cú pháp toàn bộ trò chơi không thể được coi là hoàn chỉnh vào thời điểm này và tiến trình cũng không được báo cáo dưới dạng phần trăm mà không có mẫu số.

## xác minh

```sh
.venv/bin/python -B -m unittest discover -s tests -p test_original_data.py -v
PYTHONDONTWRITEBYTECODE=1 make check
```

Phạm vi kiểm tra: vượt quá giới hạn, con trỏ xấu, không có mục kết thúc, vũ khí/ID biểu mẫu lơ lửng, trôi dạt bằng chứng ROM/bố cục/mã, sắp xếp lại từng byte của tất cả các bảng cố định, danh sách chung và sự khác biệt về biểu mẫu, trọng điểm phủ định, hai ngoại lệ ánh xạ, tham chiếu bảng chéo tập 1 và ảnh chụp nhanh lịch sử con trỏ trình điều khiển được chia sẻ. Lô thứ hai bổ sung thêm các kiểm tra lệnh hiển thị độc lập, ranh giới đầu tiên và cuối cùng của tên vũ khí, số linh hồn 0 và 29, chi phí sửa chữa và kiểm tra quyền sở hữu địa chỉ lớp phủ. Bản dựng đầy đủ cũng kiểm tra xem 51.174 đoạn văn bản có được tập hợp lại theo byte thô hay không, 6.436 khối tài nguyên được giải nén và tất cả các liên kết thư mục đều có thể phân giải được. Việc giải nén tài nguyên không phải là bằng chứng về sự khác biệt để chạy lại bãi đáp gốc ở vòng này.

11-09-2026 Đợt kết quả đầu tiên: Tất cả 67 bài kiểm tra của `make check` đều đạt; cùng một tệp kê khai được tạo hai lần liên tiếp với cùng một đầu vào và tất cả 6.714 hàm băm tệp đầu ra trong tệp kê khai đều được chuyển; 6.436 phân đoạn của gói nhịp nén ban đầu nhất quán với từng byte ROM gốc. Xem `build/original-data-qa/verification.json` để biết hồ sơ và `build/original-data-qa/logs/original-data-check.log` để biết nhật ký kiểm tra.

Đợt kết quả thứ hai trong cùng ngày: tất cả 70 bài kiểm tra của `make check` đều đạt; sau khi tạo lại thư mục, kích thước và SHA-256 của 6.714 tệp đầu ra, 61.200 danh tính duy nhất và 17.867 liên kết liên quan đều được thông qua. Xem `build/original-data-qa/verification-pass2.json` để biết hồ sơ và `build/original-data-qa/logs/original-data-check-pass2.log` để biết nhật ký kiểm tra. Trình duyệt xác nhận chi phí sửa chữa, mối quan hệ hình thức, đơn vị → nhảy vũ khí, tìm kiếm tên vũ khí Nhật Bản, tên thuần túy/tên menu và sáu liên kết tên cho Bảng Thần 13. Trò chơi chưa được ra mắt trong đợt này; chạy xác minh sau khi sửa đổi trường vẫn đang được hoàn thành.

Lô kết quả thứ ba trong cùng ngày: tất cả 76 bài kiểm tra của `make check` đều đạt và bài kiểm tra phụ thuộc đã đạt. Các xác minh mới bao gồm các công cụ sửa đổi đã ký, hệ số nhân sức tấn công và lính canh bom, mức độ ưu tiên của khe kỹ năng, chín ngưỡng và byte dành riêng, tọa độ nhãn UI độc lập, cảnh → bản đồ → tài nguyên và tính nhất quán của byte bảng ảnh chụp nhanh lịch sử. Xác minh sau thế hệ của 6.720 kích thước tệp và hàm băm, 61.519 danh tính duy nhất, 39.014 liên kết có thể phân giải và tính nhất quán từng byte của 6.436 nhịp tài nguyên nén thô. Kết quả được hiển thị trong `build/original-data-qa/verification-pass3.json`, còn nhật ký kiểm tra và trích xuất lần lượt là `build/original-data-qa/logs/original-data-check-pass3.log` và `build/original-data-qa/logs/original-data-extract-pass3.log`. Trình duyệt đã xác nhận thân máy 36, vũ khí 160, giá trị phi công 18, ngưỡng kỹ năng 18 và mục nhảy và tải xuống cho cảnh 1→bản đồ 20→tài nguyên 6284. Lô này chỉ thực hiện trích xuất tĩnh, đọc ảnh chụp nhanh lịch sử và xác minh trang phát triển và không khởi động trò chơi hoặc viết Mod.

Trình duyệt đã kiểm tra danh mục phù hợp, phân trang, các bản ghi liền kề, lựa chọn lặp lại danh mục hiện tại, tìm kiếm văn bản gốc, ranh giới kết quả trống, liên kết tải xuống tài nguyên 5600 và nhảy Chương 1→Manami→Spirit Table và kiểm tra hiển thị thực tế của trang. Mục này là sự chấp nhận của trang công cụ phát triển; trò chơi gốc chưa được ra mắt trong vòng này.

Xác minh tệp tích hợp: 82 bài kiểm tra `make check` đã vượt qua; đặc biệt bao gồm tóm tắt ánh xạ tác nhân, sự khác biệt về hình thái trong danh sách vũ khí dùng chung, ngữ nghĩa về ngưỡng kỹ năng, ánh xạ giá trị âm/thiếu/ngoài giới hạn, byte gốc và danh tính không thay đổi, liên kết hai chiều của các mối quan hệ đi xe lịch sử và tính nhất quán của thế hệ lặp lại. Kích thước và giá trị băm của 6.722 tệp được tạo, 48.458 liên kết thư mục và 57.622 tham chiếu trong tệp đều đã được kiểm tra. Trình duyệt đã kiểm tra hồ sơ đầy đủ của phi công, lọc khả năng, tìm kiếm tên linh hồn, hình dạng cơ thể và vũ khí gấp, hồ sơ trả lại bảng linh hồn cũ, điều hướng lân cận và tìm kiếm trống; trò chơi chưa được bắt đầu. Nhật ký là `build/original-data-qa/logs/original-data-check-profiles.log` và bảng kê khai xác minh là `build/original-data-qa/verification-profiles.json`.

Xác minh Năng lực/Kỹ năng Tổng thể: **88** bài kiểm tra của `make check` đã vượt qua, các bài kiểm tra phụ thuộc đã vượt qua. Một thử nghiệm mới được thêm vào để kiểm tra độc lập bảng hiển thị khả năng ban đầu, hướng dẫn sao chép trường và hằng số phục hồi HP; tất cả các cài đặt khả năng/thiết bị đều được sắp xếp lại lần lượt để xác minh sự khác biệt về hình thức, sự khác biệt giữa việc nắm giữ kỹ năng và tiếp thu hiệu quả, việc lưu giữ các bit chưa biết, bản ghi gốc không thay đổi và tính nhất quán của các phép chiếu lặp lại. Thư mục được tạo chứa tổng cộng 6.729 tệp, 61.564 danh tính, 50.119 liên kết thư mục và 59.733 tham chiếu trong định nghĩa tệp/khả năng. Băm tệp và tham chiếu đều vượt qua kiểm tra. Nhật ký kiểm tra là `build/original-data-qa/logs/original-data-check-abilities.log` và nhật ký tạo là `build/original-data-qa/logs/original-data-extract-abilities.log`; hãy xem `build/original-data-qa/verification-abilities.json` để biết danh sách phù hợp và kết quả xác minh trình duyệt. Trò chơi chưa được bắt đầu trong đợt này và chưa có Mod nào được viết.

Xác thực dấu hiệu vũ khí và hình ảnh: **103** thử nghiệm `make check` đã vượt qua, vượt qua kiểm tra phụ thuộc. 361 hình đại diện liên quan đến danh tính, 363 biểu tượng bản đồ liên quan đến nội dung/biểu mẫu và 158 bản đồ nền được khâu bản đồ; bản xem trước độc lập là 338 hình đại diện, 320 biểu tượng và 157 bản đồ, tổng cộng 815 hình ảnh và tổng cộng 972 PNG sau khi thêm hình thu nhỏ của bản đồ. Tất cả 7.725 tệp được tạo đã được kiểm tra kích thước và kiểm tra SHA-256, 74.861 liên kết thư mục đều bị đóng và 1.329 chuỗi menu thô của vũ khí đều được khớp để đánh dấu sự phân chia. Để biết chi tiết, hãy xem [Hình ảnh gốc và dấu vết vũ khí](original-images.md); danh sách xác minh là `build/original-data-qa/verification-images.json`. Lô này là giải mã tĩnh và xác minh trình duyệt, và trò chơi chưa được bắt đầu.