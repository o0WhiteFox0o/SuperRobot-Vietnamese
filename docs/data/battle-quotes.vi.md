> **Ngôn ngữ / Language:** [Tiếng Việt](battle-quotes.vi.md) · [English](battle-quotes.en.md) · [中文](battle-quotes.md)

# Danh sách lựa chọn chiến tuyến: nên nói lời nào khi

Ngày: 27-09-2026. Lớp phủ chiến đấu (ROM `0x121560`, bắt đầu từ mã `0x801C2600`) chuẩn bị hai khe dòng cho mỗi chiến binh (ghi `+0x2C` để nói khi tấn công, `+0x848` để nói khi bị đánh/tránh), được điền bởi `func_80222050`. Phương pháp làm đầy được chia thành hai cấp độ. Trước tiên, hãy kiểm tra **danh sách dòng có điều kiện**, sau đó rút ra từ **các đoạn dòng chung** tùy theo tình huống. Quá trình giải mã được triển khai trong `src/srw64_native/battle_quotes.py` và xuất (`tools/content/export_text.py`) ghi kết quả vào `assets/text-export/records.jsonl``context.triggers` cho mỗi dòng chiến đấu và tóm tắt chúng bằng giọng nói vào `assets/text-export/battle/triggers.json`; nhận xét `# 触发：` phía trên mỗi dòng trong tệp vận chuyển `content/dialogue/<locale>/battle/` cũng xuất phát từ đây.

## Giọng nói

Trình điều khiển tra bảng không phải theo số ký tự mà theo **số giọng nói**: `D_800CA9C4[人物号] = 声部号` (-1 nghĩa là không có dòng). Hầu hết các nhân vật đều có giọng nói riêng; các nhân vật nhân bản trong cốt truyện (Dumbron 273/274, bản sao của bốn thành viên của Liên minh Cấu trúc) chia sẻ giọng nói với nhân vật gốc, và ウォン và コンピュータ chia sẻ số 9. 257 giọng nói, 160 dòng có điều kiện.

## Các đoạn đường chung (bản ghi 5813–14226)

Bảng `ROM 0x1161C0`, 36 byte mỗi giọng nói: chín cặp (độ lệch bắt đầu, số ô nhịp), số bản ghi = 5813 + độ lệch. Chín tình huống được đánh số theo số được người gọi chuyển vào:

| Số | Tình huống | Quyết tâm (`func_80222050`) |
| --- | --- | --- |
| 0 | Tấn công | Phía chúng tôi hành động |
| 1 | Bị đánh gục | HP còn lại sau khi đánh là 0 |
| 2 | Bị thương nặng | HP còn lại dưới 30% |
| 3 | Sát thương trung bình | HP còn lại 30–90% |
| 4 | Chấn thương nhẹ | Còn lại hơn 90% HP |
| 5 | Tránh né | Mã kết quả 21, 22; tránh đặc biệt như bản sao (mã kết quả 6–12) cũng có cơ sở mã điều kiện là 27500 và tình huống này vẫn được sử dụng trong phần chung |
| 6 | Tấn công không hợp lệ | Mã kết quả 2–5 (khiên, hấp thụ giáp) |
| 7 | Không đủ đạn/EN | Vũ khí số -2: Không thể phản công |
| 8 | Ngoài phạm vi | Vũ khí số -3: Không thể phản công |

`func_80222B14` Chọn ngẫu nhiên một mã trong phân đoạn. Khi số bằng 0, nếu ô vẫn trống thì điền 5813 (câu đầu tiên của コウ) làm manh mối.

## Danh sách hội thoại có điều kiện (bản ghi 14227–17346)

Chỉ mục `ROM 0x121150` (một độ lệch u32 cho mỗi giọng nói), dữ liệu `ROM 0x20F250 + 偏移`, hai u16 cho mỗi mục: mã điều kiện, độ lệch văn bản (số bản ghi = 14227 + độ lệch), kết thúc `0xFFFF`. Mã điều kiện 40000/40001 có nghĩa là "tiếp tục điều kiện trước đó". Một nhóm các mục liên tiếp tạo thành một cuộc trò chuyện nhiều người được kích hoạt và hiển thị theo trình tự (người nói của mỗi câu được xác định bởi ba ký tự đầu tiên của tiêu đề văn bản). `func_8022245C` Chia các mục trúng thành ba nhóm ưu tiên và chỉ chọn ngẫu nhiên một mục từ nhóm cao nhất:

| Nhóm | Nguồn |
| --- | --- |
| 0 (cao nhất) | Đối thoại kỹ năng kết hợp (sê-ri 8000) |
| 1 | Dòng vũ khí 2600, dòng tình huống 10000 với các điều kiện đối thủ/phi công phụ trong các dòng, dấu cốt truyện hoặc điều kiện đồng phi công trong bảng điều kiện |
| 2 (tối thiểu) | Dòng dành cho vũ khí dòng 900, dòng tình huống để lái một chiếc máy bay cụ thể, đối thủ là nữ và bảng điều kiện dựa trên điện thoại di động/phi công của đối phương |

Sau khi lấy được nhóm dòng thứ hai, dòng chung vẫn sẽ được rút lại và sẽ bị từ chối với xác suất hai phần ba (`func_80222B14`: khi đã có dòng, hãy tung xúc xắc gấp 1,5 lần số dòng và chỉ thay thế khi số dòng được tung ra). Vì vậy, các dòng vũ khí dòng 900 (バルカン, ゴッドフィールドダッシュ, v.v.) chỉ là "đôi khi được nói".

Ý nghĩa của mã điều kiện:

| Mã điều kiện | Ý nghĩa |
| --- | --- |
| 0–90 | Một hàng (c, w) của bảng điều kiện `D_80222F20`: c được hiển thị trong bảng bên dưới, w là vũ khí (-1 Không có, 900+số vũ khí, 2600+số vũ khí). c Khi 700–879, dòng tiếp theo là kiểm tra cờ cốt truyện (số cờ, giá trị), ví dụ: シャイニングフィンガーソード của ドモン được chia thành hai nhóm "cờ 45 = 0" và "= 3" |
| 900 + số vũ khí | Sử dụng vũ khí này (Nhóm 2) |
| 2600 + số vũ khí | Sử dụng vũ khí này (Nhóm 1) |
| 5000 | Tay đua đối thủ là nữ (vị trí số 1 với thành tích tay đua +4) |
| 8000 + n | Kỹ năng kết hợp. Trường bản ghi vũ khí 0 1222–1229 tương ứng với số cơ sở 8000–8700 (ダブルバーニングファイヤー、ダブルライトニングバスター、ツインビーム、マジ. Được phát hiện từ bảng đối tác `[主驾驶][搭档]` (`func_80221CF8`/`func_80221ACC`), chỉ có tác dụng ở chế độ chiến đấu 3 |
| 10000 + 2500·s + k | Tình huống s (cơ sở 10000 bị bắn hạ, 12500 bị thương nặng, 15000 bị thương vừa, 17500 bị thương nhẹ, 20000 tấn công, 22500 tấn công không hợp lệ, 25000 tránh, 27500 tránh phân thân, 30000 hết đạn, 32500 Ngoài phạm vi) cộng với điều kiện k: k < 400 thân cưỡi k; 400–999 giống như c trong bảng bên dưới |

Ý nghĩa của c (`func_80221F5C`):

| c | ý nghĩa |
| --- | --- |
| 0–399 | Số điện thoại |
| 400–699 | Số giọng đối phương + 400 |
| 700–879 | Giá trị của cờ lô (c − 700) (`func_800A496C`, 2 bit mỗi cờ) |
| 880–889 | Phi công phụ (`func_801C4A08`): 880 チャム, 881 シルキー, 882 ローレンス, 883 アイシャ, 884 甲児, 885ひかる、886マリア、887 鄄也、888 ジュン、889 ナイーダ |

Vũ khí được so sánh theo trường thứ 0 của bản ghi vũ khí (`ROM 0x119970`, mỗi 14 byte), vì vậy vũ khí có cùng tên trên các thân khác nhau (các loại バルカンđại bác, ロケットパンチ) được coi là giống nhau; `desc` trong số `triggers.json` sẽ liệt kê tất cả tên của cùng một nhóm.

## Những dòng không đọc được ở bản gốc

- Bảng điều kiện chỉ đọc `0x1E0` byte (120 mục) cho mỗi giọng nói. Các bảng デューク (tiếng nói 90.448 mục), ボス (164.274 mục) và Jiafu (165.298 mục) vượt quá giới hạn trên và phiên bản gốc của 150 câu tiếp theo (bản ghi 15420–15523, 15925–15953, 16242–16258) sẽ không bao giờ được hiển thị; xuất thẻ `unreachable`, nhận xét có nội dung "vượt quá giới hạn đọc ban đầu".
- 39 câu không có bảng trích dẫn: 7343, 8105, 10481–10483, 10702–10731, 14527–14530. Chứng từ vận chuyển được đặt trong `battle/other.txt`.
- 5799–5812 (`battle.special`) không có trong hai bảng này: chương trình chính `800A2890` nhấn `D_800C9A08` khi soái hạm bị bắn hạ. Chọn một trong số các thuyền trưởng theo thứ tự (Haruto, Seru, Ere, Dr. Hazuki, Erma, Toro và Hare).

## Chưa nghiên cứu chi tiết

- Khi bản ghi hiếu chiến `+0x8` là `0x14`, giọng nói phi công chính được trỏ bởi `+0x106C` sẽ được sử dụng thay thế và tỷ lệ thiệt hại được tính theo trường HP của nó (có lẽ đó là thân tàu/phần nhiều người chơi), không ảnh hưởng đến việc phân bổ dòng.
- Hai dòng (49, 51) trong bảng điều kiện có c nằm trong khoảng từ 700-879 và w < 900 sẽ lấy c làm số hiệu vũ khí để so sánh theo mã và có khả năng không bao giờ bắn trúng; nó chỉ ảnh hưởng đến ba câu "ゲイル sự trả thù của trung úy" của カルラ.
- Ngữ nghĩa của các điểm đánh dấu cốt truyện 45–49 (một trạng thái nhất định của năm thành viên của Liên minh Kết cấu).