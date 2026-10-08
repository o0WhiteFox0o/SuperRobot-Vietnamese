> **Ngôn ngữ / Language:** [Tiếng Việt](fixed-unit-name.vi.md) · [English](fixed-unit-name.en.md) · [中文](fixed-unit-name.md)

# Tên quân được cố định theo tên mặc định (3D5E)

27-09-2026 Do người dùng xác định: Người chơi không được phép thay đổi tên cá nhân và tên đơn vị và trang gốc sẽ không được mở (áp dụng tương tự khi chọn phiên bản gốc trong cài đặt). Vì vậy, tên đơn vị luôn là mặc định của trò chơi là "Gió tháng Ba". Khi hiển thị sẽ đổi thành "Gió tháng ba" theo ngôn ngữ đọc. Để biết tên mặc định của nhân vật và thay thế hiển thị, hãy xem [Tên mặc định Hiển thị ba ngôn ngữ](default-names.md). Chỉ có tên đơn vị được ghi ở đây.

## Hành vi

- Ở đầu cảnh 33, 46/58 và 62, lựa chọn "それでかまわない／気に入らない" sau khi Amino đề xuất "マーチウィンド" sẽ không xuất hiện nữa, chỉ cần nhấn số 1 "マーチウィンドか...いいんじゃないか", theo sau là "ブライト". Nhánh "気に入らない" (nhân vật chính không thích tên, アムロ hỏi tên nó là gì, `3D5E` mở đầu vào tên đơn vị, nhân vật chính đề xuất tên mới) không còn được thực thi.
- Nếu `3D5E` được thực thi (cấp độ nhỏ, tập lệnh gỡ lỗi), không làm gì cả: không chuyển sang chế độ 6, không mở bất kỳ trang nào, để nguyên `8010F698` và tập lệnh sẽ tiếp tục ngay lập tức.
- Bộ đệm tên quân đội chỉ lưu trữ các ký tự gốc. Tên mặc định để đăng ký ba ngôn ngữ là `Field::Unit`: `ja` là マーチウィンド, còn các ngôn ngữ khác ​​lấy `unit_default_name` của thư mục ngôn ngữ (zh-Hans "March Wind", en "March Wind", nhất quán với `content/translation/story-terms.json`). Trong đoạn hội thoại, `<G:012C>` (tệp hội thoại được viết là `{HeroMech}`, tên sai, thực chất là tên đơn vị) được hiển thị theo ngôn ngữ và tên mặc định bên ba ngôn ngữ được kết nối với nơi mở rộng hội thoại. Các kho lưu trữ đã được đổi tên trong phiên bản cũ sẽ xuất hiện như cũ.
- Chỉ có hiệu lực trên máy chủ trò chơi có RT64; Máy chủ chẩn đoán khung cố định và chỉ CPU không cài đặt hai lệnh gọi lại này và duy trì quy trình ban đầu.

## Quy trình gốc (phân tích tĩnh)

| Địa chỉ | Chức năng |
| --- | --- |
| Sự kiện `001AB86C` (cảnh 33), `001AC6F0` (62), `001BC304` (46/58) | Sự kiện khai mạc `3D44 0,2,<文本>` (khe cửa sổ 0, 2 mục, văn bản 24045/24417/32003, cả hai đều là "それでかまわない／気に入らない"), sau đó `3E10` (mục 1) nhánh và `3E11` (mục 2) chi nhánh; `3D5E` chỉ có ở mục 24045/24417/32003 2 nhánh. |
| `8009FA94` | `3D44` hàm xử lý, tham số là script VM context: `+0x1C` là PC vượt quá opcode (ba tham số), `+0x26` Khung đầu tiên là 0 (khung đầu tiên được cửa sổ và đặt thành 1), `+0x24` là cờ bận (VM Hàm xử lý được gọi ở mọi khung cho đến khi nó bị xóa), `+0xC` trỏ đến động cơ `+0x994`. Giải phóng cửa sổ sprite 0x23, `+0x24=0`, PC+6, `*(+0xC)=0x3DD9+光标` khi được xác định. `3E10`/`3E11` so sánh giá trị này. |
| `800A1050` | Quá trình xử lý thường trú của `3D5E`: gọi `801C517C` của lớp phủ bản đồ thế giới, theo sau là `+0x24=0` để hoàn thành lệnh. |
| `load_000A7EC0:801C517C` | `801C58C4=2`, `80080188(6)` chuyển sang chế độ 6, `80099814(5,1,2)` mờ dần. |
| `800801A4` → `800CFEC8[模式-1]` | Chế độ 6 Vào `8008032C`: `80080038` Cài đặt ROM `0x1090A0–0x10DA50` thành `801C2600` (lớp phủ giống như trang chọn nhân vật chính và tên), đăng ký `801C69B4` → `801C6814(1)`. |
| `801C6814(a0)` | Khởi tạo công khai; `a0=0` là tên của trò chơi mới (trạng thái 0, `801C5004`), `a0=1` đặt trạng thái `801C6FB0`/`801C7144` thành 4 và gọi `801C6034`. Mỗi tác vụ khung `801C657C` kiểm tra bảng {khởi tạo, từng khung} của `801C6F74` theo trạng thái. Trạng thái 4 là `801C6034`/`801C62D8`. |
| `801C6034` | Vẽ bảng chọn ký tự kana; sau khi xóa `801C71E0` trong vùng chỉnh sửa, điền vào 7 khoảng trống đầu tiên bằng ký tự `801C6F54` (マーチウィンド) và hiển thị bảng chọn ký tự TEXT id của `801C6F64` (giống nhưマーチウィンド); ô con trỏ `801C7228`, vị trí chèn `801C721C`. |
| `801C62D8` | Mỗi khung: Gọi `801C4C40` khi A nằm trên lưới "quyết định" (0x7D). Nếu không phải là 0, cửa sổ bật lên 0x92, `801C71DC=1`, v.v. sẽ được nhấn lại; nếu là 0, `801C70F4=2` sẽ mờ dần. Ở các ô khác, phím A `801C4308` viết một từ (dừng ở ô thứ 10 sau khi điền vào ô thứ 10) và phím B `801C465C` xóa ô hiện tại và di chuyển sang trái. |
| `801C4C40` | Xác nhận: Sao chép tối đa 10 glyph của `801C71E0` vào `8010F698` (khoảng trắng ở cuối là glyph 0 và không được sao chép, từ ở giữa được tính) và không có từ nào được trả về là 1; sau đó thêm lần lượt 10 nửa từ của `8010F698` vào 6 của `801C6EC8` So sánh các tên dành riêng (mỗi tên 10 nửa từ) - OZ, オズ, スペシャルズ, ホワイトファング,アクシズ, ネオジオン - đồng dư và trả về 1; nếu không thì viết sau tên `0xFFFF` trả về 0. |
| `801C657C` Biến mất | `801C70F4==2`: Chế độ 5 (trò chơi mới) `801C69D0` Đặt tập đầu tiên, chế độ 0x1F, `801C5FCC` Viết tên đơn vị mặc định (`801C6F54`, 7 ký tự cộng với `0xFFFF`) `8010F698`; Trong các trường hợp khác (trang tên quân), chuyển sang chế độ 0xD và quay lại bản đồ thế giới. |

- `8010F698` có tổng cộng 12 nửa từ (`801C5FCC` xóa 12). Tên có thể dài tối đa 10 ký tự cộng với dấu kết thúc; đoạn hội thoại sử dụng glyph `0x12C` để tham chiếu nó.
- Lỗi gốc so sánh tên dự trữ: `801C4C40` không xóa nội dung cũ sau tên khi sao chép mà so sánh cả 10 nửa từ. Vùng đệm sau trò chơi mới là マーチウィンド＋`0xFFFF` nên chỉ những tên dành riêng có trên 8 ký tự (ホワイトファング) mới bị từ chối. Những tên ngắn như "OZ" và "アクシズ" có thể được chấp nhận. Bây giờ người chơi không thể truy cập trang này, hãy để nó được ghi lại.
- Có một `801C3634(801C6F64[i]+0x14D0, i, 0)` khác trong `801C6034`. Nếu bạn viết `801C71E0[i]` theo id TEXT không liên quan, nó sẽ bị ghi đè bằng hình tượng của `801C6F54`, điều này sẽ không ảnh hưởng đến kết quả.

## Triển khai

- `src/host/unit_name.hpp`/`unit_name.cpp`, được định cấu hình bởi `host.cpp` sau khi tải thư mục hội thoại (`dialogue::configure`):
- `answer_choice`: Trong khung đầu tiên của `3D44` (`+0x26==0`), gặp phải hai lựa chọn có văn bản 24045/24417/32003. Viết `0x3DD9`, PC+6, `+0x24=0` theo đường dẫn ban đầu. Chức năng xử lý ban đầu không chạy và cửa sổ không mở. Được gọi qua `srw64_game_hooks.choice_step` bởi trình bao bọc `resident_func_8009FA94` của `game_hooks.cpp`.
- `3D5E`: `NATIVE_HOOKS` trong số `generate_cpu.py` đổi tên `load_000A7EC0_func_801C517C` thành `srw64_original_unit_name_command` và gói hàng được trả lại trực tiếp thông qua `srw64_game_hooks.unit_name_page`. Sau khi thay đổi `NATIVE_HOOKS`, bạn cần chạy lại `generate_cpu.py` theo cách thủ công.
- `add_default`: Lấy tên từ `unit_default_name` của từng thư mục ngôn ngữ và đăng ký vào `names::default_names()`; bất kể chuyển đổi trang tên, đoạn hội thoại cũng sẽ được hiển thị theo ngôn ngữ khi đặt `SRW64_NATIVE_NAME_ENTRY=0`.
- Nhật ký sự kiện `unit-name-events.jsonl` (giao diện gỡ lỗi `events unit_name`): `default` (tên đăng ký của từng ngôn ngữ), `choice-answered` (văn bản, mục 1), `page-skipped`.

## Xác minh

- Kiểm tra thành phần `make recomp-unit-name-test` (`tests/native_unit_name.cpp`, Asan+UBSan): trả lời câu 1 ở cả 3 phương án và hoàn thành câu lệnh; các tùy chọn khác, không phải mục 2, không phải khung đầu tiên, con trỏ xấu không di chuyển bộ nhớ; móc và nhật ký sự kiện; đăng ký tên mặc định và hiển thị bằng từng ngôn ngữ. `make recomp-name-entry-test` Ngẫu nhiên, sơ khai chức năng kiểm tra bị thiếu đã được thêm vào (mục tiêu này luôn không kết nối được sau khi thêm công tắc trang tên vào ngày 23-09-2026).
- `tests/test_unit_name.py`: nối dây, chỉ được cấu hình trong máy chủ trò chơi và sau thư mục hội thoại, tên mặc định bằng ba ngôn ngữ; khi có ROM, hãy kiểm tra các byte lệnh và văn bản tùy chọn được chọn ở ba vị trí, `3D5E` chỉ được phân nhánh ở mục thứ hai, đường dẫn được xác định của `8009FA94`, quá trình xử lý `3D5E` và định dạng tên mặc định.
- Máy thực tế: Cấp độ nhỏ `config/recomp/mini-stages/unit-name.json` (phát lại phần lựa chọn và hai nhánh của cảnh thứ 33, đồng thời thực hiện lại `3D5E` riêng biệt, sau đó dòng "Ninja" in tên đơn vị), kiểm tra tập lệnh `tools/recomp/debug/check_unit_name.py`. **Chưa hoạt động. **

Ngoài ra: Trong phần [Cấp độ nhỏ](../script/mini-stage.md), trước đây tôi đã lưu ý rằng giá trị điền sẵn là "アーチウィンド". Theo ROM, cả hai bảng đều là "マーチウィンド", đã được sửa.