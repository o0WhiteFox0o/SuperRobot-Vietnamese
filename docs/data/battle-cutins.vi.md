> **Ngôn ngữ / Language:** [Tiếng Việt](battle-cutins.vi.md) · [English](battle-cutins.en.md) · [中文](battle-cutins.md)

# danh sách tóm tắt cut-in chiến đấu

2026-09-30 Đã tổ chức. Có 55 cảnh cắt cảnh trong màn chiến đấu, tất cả đều nằm trong mục 984–1038 của bảng đăng ký cảnh trận chiến (ROM `0x11E3D0`). Bài viết này liệt kê những gì mỗi vật phẩm rút ra khi di chuyển, kích thước và số khung của nó cũng như loại vũ khí và cách sử dụng nó. Để biết định dạng và giải mã, hãy xem [Hình ảnh trận chiến](battle-graphics.md) và để biết cơ chế kết xuất, khung che và tuyến HD, hãy xem [Cơ chế kết xuất hiệu suất trận chiến](../design/battle-animation-rendering.md) §6.3/§7.

Dữ liệu được đọc trực tiếp từ ROM bởi `read_triplets`, `read_animation_bank` và `parse_scene` của `battle_graphics.py`; cột "Nội dung" được viết dựa trên hình ảnh được xuất (`assets/original-graphics/cutins/`). Ý nghĩa của trường tác nhân chỉ có cơ sở tĩnh và không có xác minh thực tế nào cho trường "suy ra".

## 1. Quy mô

| Mục | Số lượng |
| --- | --- |
| Mục đã đăng ký | 55 (984–1038), 46 được trích dẫn trong hồ sơ vũ khí và 9 không có trích dẫn nào |
| Album | 27 ảnh (1337, 1339–1364): tập bản đồ lớn CI8 14 ảnh (tối đa 512×512), tập bản đồ nền CI4 13 ảnh |
| Khung | 308 khung hình, trong đó có 26 khung hình lớp nền |
| Các phần khác nhau lát | 1736 miếng |
| Vũ khí được sử dụng | 14 số vũ khí, 10 nước đi thực tế (24/29, 874/881, 1062/1075 là hai kỷ lục của cùng một nước đi; 18 và 1216 chia sẻ ドモン cận cảnh) |
| Công việc liên quan | G ガンダム（7 số vũ khí), ダンクーガ, レイズナー, ジャイアントロボ, ゴッドマーズ,コン・バトラーV |

Cả phần cắt tham chiếu `hit` và `reaction` đều không; tất cả các vết cắt đều có trong hồ sơ vũ khí của kẻ tấn công. Tất cả các cảnh đều là đỉnh_mode 1 (không có nhóm đỉnh phản chiếu, kẻ thù và bạn bè được vẽ giống nhau), chỉ có 1025/1026 là chế độ 2.

## 2. Thành phần của phần cut-in

Mỗi phân đoạn bao gồm 2-3 tác nhân xếp chồng lên nhau, được xây dựng theo thứ tự các tác nhân và được vẽ theo mức độ ưu tiên của nút:

1. **Nền**: Hoạ tiết 128×96 (đường tốc độ, đám mây, dải ánh sáng) trên tập bản đồ CI4, 1–3 khung hình. Thường có cờ cao h4 `0x8000` hoặc `0x4000`.
2. **Hình ảnh chính**: Cận cảnh một nhân vật/máy trong tập bản đồ lớn CI8. Canvas chủ yếu có kích thước 128 × 96 và tất cả hoạt ảnh đều nằm trong khung (không có mã trượt).
3. **Lớp phủ**: huy hiệu, bức xạ, hình bóng, tia sét, v.v., h5 chủ yếu là 140–190 (được suy ra là trong mờ, 255 là mờ đục).

Trường tác nhân: byte thấp h4 là pha kích hoạt (`0x44`/`0x50`–`0x57`), `0xFFFF` và một chữ số là số thứ tự trong cùng một phân đoạn; hành vi 240 là cảnh giới thiệu tiêu chuẩn, 350 là シャイニング／ゴッド Cận cảnh phần mở đầu của Sở, 351 là chế độ xem dài theo chiều ngang của Structural Fist, 352 là một phần nhỏ có độ lệch x/y (huy hiệu, logo), 373 là diễn viên được điều khiển với h6 = 2. Màn hình được chia tỷ lệ 1,29, tập trung vào màn hình và y = 47, do đó canvas 128×96 chiếm khoảng 165×124 pixel màn hình; một diễn viên có z == 1 sẽ treo mặt nạ `800C6D00` (để lại cửa sổ 140×120).

## 3. Nhấn di chuyển

"Khung/thời lượng" là tổng số tích tắc trong các khung/bước khác nhau. Kích thước là hộp giới hạn của tất cả các khung.

### 3.1 Siêu điện từ スピン (vũ khí 778, コン・バトラーV)

| Đăng ký | Cảnh/Album/Bảng màu | Kích thước | Khung hình/Thời lượng | Hành vi | h4/h5/z | Nội dung |
| --- | --- | --- | --- | --- | --- | --- |
| 985 | 1406/1342/1372 | 128×96 | 1/1 | 240 | 8053/255/0 | Bối cảnh: mây tím |
| 984 | 1405/1341/1371 | 128×96 | 15／90 | 240 | 53/255/0 | コン・バトラーV Tư thế, nhiễm điện, gấp thành máy khoan và xoay |

h6 = 2 cho cả hai tác nhân.

### 3.2 ファイナルゴッドマーズ (Vũ khí 742, ゴッドマーズ／ガイヤー)

| Đăng ký | Cảnh/Album/Bảng màu | Kích thước | Khung hình/Thời lượng | Hành vi | h4/h5/z | Nội dung |
| --- | --- | --- | --- | --- | --- | --- |
| 988 | 1409/1344/1374 | 128×96 | 2／107 | 240 | 8057/255/0 | Bối cảnh: đám mây năng lượng xanh, khung thứ hai toàn màu đen |
| 986 | 1407/1343/1373 | 160×144 | 8／107 | 240 | 57/255/1 | ゴッドマーズ Giương kiếm, sét đánh, cận cảnh mũi kiếm |
| 989 | 1410/1343/1373 | 32×32 | 1/107 | 352 | 57/255/2 | Dấu "M" ở ngực, độ lệch (−53, 30) |
| 987 | 1408/1343/1373 | 128×96 | 7／107 | 240 | 50/255/0 | Đường gạch chéo màu trắng và đèn flash chéo |

### 3.3 ジャイアントロボ (vũ khí 820 ロケットバズーカ, 821 ロケットミサイル)

| Đăng ký | Vũ khí | Cảnh/Album/Bảng màu | Kích thước | Khung hình/Thời lượng | Hành vi | h4/h5/z | Nội dung |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 991 | 821 | 1421/1350/1380 | 128×96 | 1/1 | 240 | 8044/255/0 | Bối cảnh: đường xiên tốc độ màu xanh |
| 990 | 821 | 1420/1349/1379 | 144×96 | 9／80 | 240 | 44/255/0 | Ống tên lửa trên vai được nâng lên và bắn, và cận cảnh cuối cùng của khuôn mặt |
| 994 | 820 | 1424/1350/1380 | 128×96 | 1/1 | 240 | 8052/255/0 | Bối cảnh: vạch tốc độ ngang màu xanh |
| 992 | 820 | 1422/1349/1379 | 128×104 | 7／54 | 240 | 52/255/0 | Đầu nòng súng phóng tên lửa kéo dài, cận cảnh cuối cùng của khuôn mặt |
| 993 | 820 | 1423/1349/1379 | 72×64 | 6／54 | 240 | 52/255/0 | Khói mõm |

### 3.4 V-MAX (Vũ khí 1075 レイズナー, 1062 ニューレイズナー)

| Đăng ký | Vũ khí | Cảnh/Album/Bảng màu | Kích thước | Khung hình/Thời lượng | Hành vi | h4/h5/z | Nội dung |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 997 | Cả hai | 1434/1356/1384 | 128×96 | 2／88 | 240 | 53/255/0 | Nền: các đường dọc màu xanh đậm, khung thứ hai toàn màu trắng |
| 995 | 1075 | 1432/1355/1383 | 128×96 | 7／88 | 240 | 53/255/0 | レイズナー cận cảnh đầu, toàn thân biến thành hình bóng màu xanh lam |
| 996 | 1075 | 1433/1355/1383 | 128×96 | 6／88 | 240 | 53/180/0 | Mắt ánh sáng vàng, bức xạ, bóng xanh nhạt |
| 998 | 1062 | 1435/1355/1383 | 128×96 | 7／88 | 240 | 53/255/0 | Giống như 995, phần thân được đổi thành ニューレイズナー |
| 999 | 1062 | 1436/1355/1383 | 128×96 | 6/88 | 240 | 53/180/0 | Tương tự như 996 |

Nhật ký chiến đấu của cả hai loại vũ khí đều chỉ ra vũ khí đối thoại là 1062.

### 3.5 ドモン cận cảnh mở đầu (được chia sẻ bởi vũ khí 18, 24, 29, 1216)

| Đăng ký | Cảnh/Album/Bảng màu | Kích thước | Khung hình/Thời lượng | Hành vi | h4/h5/z | Nội dung |
| --- | --- | --- | --- | --- | --- | --- |
| 1011 | 1404/1340/1396 | 128×96 | 1/69 | 350 | 255/2/0 | Nền: đường thẳng đứng màu xanh |
| 1009 | 1402/1339/1395 | 128×112 | 8／69 | 350 | 1/255/0 | ドモン, giơ tay phải lên để lộ mu bàn tay |
| 1010 | 1403/1339/1395 | 69×66 | 1/69 | 350 | 1/150/0 | Huy hiệu King of Hearts trên mu bàn tay |

H4 của ba vật phẩm trong vũ khí 1216 đều bằng 0 và z của 1010 là 1.

### 3,6 シャイニングフィンガー（Vũ khí 29 シャイニングガンダム; 24 là kỷ lục của cùng một động tác không có trang bị trên người)

Chơi 3.5 trước rồi:

| Đăng ký | Cảnh/Album/Bảng màu | Kích thước | Khung hình/Thời lượng | Hành vi | h4/h5/z | Nội dung |
| --- | --- | --- | --- | --- | --- | --- |
| 1014 | 1429/1353/1397 | 128×96 | 22/1 | 350 | FFFF / 255 / 0 | シャイニングガンダム Mặt và nắm đấm, vẫn |
| 1015 | 1430/1353/1397 | 64×64 | 22/1 | 350 | FFFF / 153 / 1 | Đèn hồ quang màu đỏ |
| 1013 | 1428/1354/1398 | 128×96 | 1/65 | 373 | FFFF / 255 / 0 | Bối cảnh: dải đèn màu tím |
| 1012 |
| 1016 | 1431/1354/1398 | 128×96 | 22/1 | — | — | Toàn nền đen, **không có dấu ngoặc kép** |

### 3.7 Nhiệt độ bùng nổ ゴッドフィンガー (Vũ khí 18, ゴッドガンダム)

Chơi 3.5 trước, sau đó là hai đoạn và cuối cùng theo dõi ba đoạn của Mingjing Shisui (h4 `4053`/`53`) của 3.8:

| Đăng ký | Cảnh/Album/Bảng màu | Kích thước | Khung hình/Thời lượng | Hành vi | h4/h5/z | Nội dung |
| --- | --- | --- | --- | --- | --- | --- |
| 1007 | 1414/1345/1375 | 128×96 | 22/1 | 350 | FFFF / 255 / 0 | ゴッドガンダム mặt và nắm đấm, vẫn |
| 1008 | 1415/1345/1375 | 64×64 | 22/1 | 350 | FFFF / 153 / 2 | Đèn hồ quang màu đỏ |
| 1004 | 1411/1345/1375 | 128×96 | 8／47 | 373 | 0/255/0 | Lòng bàn tay mở ra, áo giáp mở ra, phát sáng |
| 1005 | 1412/1345/1375 | 128×96 | 5／47 | 373 | FFFF / 150 / 0 | Hình bóng màu đỏ (ngọn lửa) |
| 1006 | 1413/1346/1376 | 128×96 | 2/74 | — | — | Nền: toàn màu đen, ánh sáng xiên vàng, **không có dấu ngoặc kép** |

### 3.8 Mingjing Shisui (vũ khí 18: Nắm đấm nhiệt nổ, 19: Nắm đấm phá đá)

| Đăng ký | Cảnh/Album/Bảng màu | Kích thước | Khung hình/Thời lượng | Hành vi | h4/h5/z | Nội dung |
| --- | --- | --- | --- | --- | --- | --- |
| 1002 |
| 1000 | 1416/1347/1377 | 128×96 | 120/11 | 240 | 4053 (4044) / 255 / 0 | Golden ドモン gassho, ゴッドガンダム ngực, cánh sau xòe |
| 1001 |
| 1003 | 1419/1347/1377 | 64×64 | 1/120 | — | — | Chỉ có quốc huy, **không trích dẫn** |

### 3.9 Cú sốc thuốc đá (Vũ khí 19, ゴッドガンダム)

Sau 3,8:

| Đăng ký | Cảnh/Album/Bảng màu | Kích thước | Khung hình/Thời lượng | Hành vi | h4/h5/z | Nội dung |
| --- | --- | --- | --- | --- | --- | --- |
| 1036 | 1453/1364/1392 | 128×96 | 28/1 | 240 | 51/255/0 | Bối cảnh: mưa nhẹ xiên xanh trắng |
| 1034 | 1451/1363/1391 | 128×96 | 3／28 | 240 | 51/255/0 | Mặt vàng ドモン, phóng đôi lòng bàn tay |
| 1035 | 1452/1363/1391 | 128×96 | 2／28 | 240 | 51/190/0 | quầng đỏ |

### 3.10 Cú đấm phá đá (Vũ khí 1216, ゴッドガンダム＋ライジングガンダム)

Chơi 3.5 trước rồi:

| Đăng ký | Cảnh/Album/Bảng màu | Kích thước | Khung hình/Thời lượng | Hành vi | h4/h5/z | Nội dung |
| --- | --- | --- | --- | --- | --- | --- |
| 1024 | 1448/1362/1388 | 128×96 | 2／175 | 240 | 54/255/0 | Bối cảnh: dải đèn vàng, chấm sao xanh |
| 1023 | 1447/1361/1387 | 144×96 | 18／175 | 240 | 54/255/0 | ドモン và レイン: ôm nhau dưới ánh trăng trắng, nắm tay nhau, nắm tay nhau |
| 1020 | 1444/1360/1386 | 128×96 | 3/108 | 240 | 56/255/0 | Bối cảnh: Năng lượng bức xạ màu xanh cam |
| 1022 |
| 1021 | 1445/1359/1385 | 64×64 | 1/108 | 352 | 56/255/3 | King of Hearts Huy hiệu, Offset (20, 17) |
| 1025 | 1449/1361/1387 | 128×96 | 1/1 | — | — | Đoạn một phần của 1023 (chế độ 2), **không có tài liệu tham khảo** |
| 1026 | 1450/1361/1387 | 128×96 | 1/1 | — | — | Tương tự như trên, **không trích dẫn** |

### 3.11 Nắm đấm liên minh kết cấu (Vũ khí 1217, Nắm đấm kết cấu)

| Đăng ký | Cảnh/Album/Bảng màu | Kích thước | Khung hình/Thời lượng | Hành vi | h4/h5/z | Nội dung |
| --- | --- | --- | --- | --- | --- | --- |
| 1031 | 1441/1358/1390 | 128×96 | 1/52 | 351 | 4/255/0 | Bối cảnh: dải đèn vàng nhạt |
| 1027 | 1437/1357/1389 | 528×96 | 26／52 | 351 | 0/255/0 | Năm tượng bán thân bằng vàng trượt vào và xếp hàng từ phải sang trái |
| 1028 | 1438/1357/1389 | 434×51 | 26／52 | 351 | 1/140/0 | Năm điểm đèn đỏ (quốc huy trên mu bàn tay mỗi người) |
| 1029 |
| 10:30 | 1440/1358/1390 | 128×96 | 1/98 | — | — | Dải đèn nền (giống hình 1031), **Không tham khảo** |
| 1032 | 1442/1357/1389 | 160×168 | 4／37 | — | — | Năm quốc huy hợp lại thành một, **Không trích dẫn** |
| 1033 | 1443/1358/1390 | 128×96 | 3／37 | — | — | Toàn màu đen, nhấp nháy, toàn màu trắng, **không có dấu ngoặc kép** |

1027–1029 là những cảnh duy nhất vượt quá cửa sổ mờ 140×120 và dựa vào sự dịch chuyển trong khung để di chuyển theo chiều ngang; ba mục này cần được xem nhất trong thời gian thực trên màn ảnh rộng.

### 3.12 Thanh kiếm Light Fang phá trời (vũ khí 874 ダンクーガ và nhiều chiến binh quái thú khác nhau; 881 là kỷ lục của cùng một chiêu thức không có trang bị trên người)

| Đăng ký | Cảnh/Album/Bảng màu | Kích thước | Khung hình/Thời lượng | Hành vi | h4/h5/z | Nội dung |
| --- | --- | --- | --- | --- | --- | --- |
| 1038 | 1426/1352/1382 | 128×96 | 1/90 | 240 | 4044/255/1 | Nền: đường thẳng đứng màu xanh |
| 1037 | 1425/1351/1381 | 128×120 | 4／90 | 240 | 4044/255/0 | Ren hét lên, và sau đó các thanh mắt của Sara, Masato và Ryo lần lượt được xếp chồng lên nhau |
| 1017 | 1399/1337/1369 | 112×288 | 14／110 | 240 | 54/255/1 | Thanh kiếm trống rút từ trên xuống dưới, ダンクーガ cầm kiếm khắp nơi |
| 1018 | 1400/1337/1369 | 144×96 | 11／110 | 240 | 54/140/0 | Cột năng lượng màu cam, đỏ tươi và đèn hồ quang chém |
| 1019 | 1401/1337/1369 | 128×96 | 3／110 | 240 | 54/140/0 | Tia sét xanh |

## 4. 9 mục không có trích dẫn

1003, 1006, 1016, 1025, 1026, 1029, 1030, 1032, 1033. Chúng đều nằm trong cùng một album ảnh của cảnh được trích dẫn và là những bức ảnh dự phòng hoặc bị loại bỏ của cùng một chiêu thức: Nắm đấm Liên minh Kết cấu thiếu ba bức ảnh "toàn thân lòng bàn tay", "tập hợp huy hiệu" và "tia sáng nổ" (1029-1033), và Nắm đấm nông thôn Ishiba còn lại hai mảnh chế độ 2. Các quy trình hành vi cũng có thể sử dụng `801C5700` để thay đổi cảnh, vì vậy "bản ghi vũ khí không được tham chiếu" không có nghĩa là "không được xuất hiện trong thời gian chạy" - để xác nhận, hãy thêm đầu dò chỉ đọc theo số đăng ký trên `801C3170`.

## 5. Phân nhóm khi làm HD

Sau khi ghép theo album có 13 nhóm ảnh chính + hình nền tương ứng, HD theo nhóm:

| Nhóm | Album Chính (CI8) | Album Nền (CI4) | Mục đăng ký |
| --- | --- | --- | --- |
| コン・バトラーV | 1341 | 1342 | 984–985 |
| ゴッドマーズ | 1343 | 1344 | 986–989 |
| ジャイアントロボ | 1349 | 1350 | 990–994 |
| レイズナー | 1355 | 1356 | 995–999 |
| ゴッド Ming Jing Shisui | 1347 | 1348 | 1000–1003 |
| ゴッドフィンガー | 1345 | 1346 | 1004–1008 |
| ドモン cận cảnh | 1339 | 1340 | 1009–1011 |
| シャイニングフィンガー | 1353 | 1354 | 1012–1016 |
| ダンクーガ 空剣 | 1337 | — | 1017–1019 |
| ダンクーガ bốn người | 1351 | 1352 | 1037–1038 |
| Sky Fist hiếm | 1359, 1361 | 1360, 1362 | 1020–1026 |
| シャッフル Alliance Boxing | 1357 | 1358 | 1027–1033 |
| Nắm đấm sốc Shi Potian | 1363 | 1364 | 1034–1036 |

- Cận cảnh nhân vật (1000, 1009, 1022, 1023, 1027, 1034, 1037) là phần có chất lượng hình ảnh đạt được cao nhất. Bạn có thể sử dụng hình đại diện HD đã được phê duyệt làm tài liệu tham khảo nhận dạng.
- Bóng đồng màu, đường xuyên tâm, đường gạch chéo và tia chớp (987, 996/999, 1005, 1018, 1019, 1028, 1035) là các khối màu phẳng, có thể được vector hóa hoặc phóng to trực tiếp mà không cần tạo mô hình.
- 13 ảnh nền đều là họa tiết nhỏ 128×96, phóng to toàn bộ ảnh.
- Tất cả vertex_mode 1. Không cần lo lắng về hiệu ứng bảng màu và phù hợp để chủ nhà vẽ toàn bộ khung (Tài liệu cơ chế kết xuất §7.2); điều quan trọng là (cảnh, tập bản đồ, bảng màu, số khung), tổng cộng có 308 khung hình.