> **Ngôn ngữ / Language:** [Tiếng Việt](tactical-maps.vi.md) · [English](tactical-maps.en.md) · [中文](tactical-maps.md)

# Danh sách bản đồ chiến thuật và hiệu ứng động

Ngày: 23-09-2026. Bài viết này liệt kê lần lượt tất cả các bản đồ chiến thuật và động thái thời gian chạy của chúng cho [HD Planning §3](../design/hd-pipeline-plan.md#3-战术地图). Bạn có thể tìm thấy mô tả về cơ chế (định dạng dữ liệu cho chu kỳ bảng màu, khung thuộc địa, hoán đổi 3D34) trong [Kho nội dung HD §3](hd-asset-inventory.md#3-战术地图的动态效果).

Dữ liệu được tính toán từ ROM bởi [`map_dynamics.py`](../../tools/content/map_dynamics.py) và được ghi vào `build/content/map-dynamics.json`; việc thêm tham số `--markdown` sẽ xuất ra bảng trong Phần 6 cùng một lúc.

Hai mục "Cảnh ban đầu" và "3D34 Cut-in" đọc thư mục cốt truyện tự xuất `assets/original-data`, còn các mục còn lại chỉ đọc ROM. Kiểm tra tương ứng là [`test_map_dynamics.py`](../../tests/test_map_dynamics.py). Mọi kết luận đều đến từ việc phân tích tĩnh chứ không phải việc chạy game.

"Pixels" đề cập đến số lượng pixel của hình ảnh gốc nằm trong phạm vi màu chu kỳ sau khi toàn bộ bản đồ được tập hợp theo bố cục, đây là khu vực chuyển động thực tế trên màn hình.

## 1. Tổng quan

- **Tỷ lệ**: 158 bản ghi bản đồ, 154 bố cục khác nhau, chia sẻ 8 tập bản đồ địa hình:
- 6229 vũ trụ, 79 bản đồ;
- 6228 mặt đất, 64 hình ảnh;
- 6230, 6 ảnh;
- 6231, 4 ảnh;
- 6233, 2 ảnh;
- 6232, 6234, 6236, mỗi cái 1 cái.
- **Chuyển động**: 104 ảnh có chuyển động rõ ràng, 54 ảnh hoàn toàn tĩnh.
- **Tài liệu tham khảo**: 97 là bản đồ ban đầu của một cảnh nhất định, 37 sẽ được chuyển đổi bằng kịch bản cốt truyện 3D34 và 25 không tìm thấy tài liệu tham khảo tĩnh (Phần 5).
- **Bản đồ một màn hình**: 11 bản đồ chỉ có kích thước 320×240, bằng kích thước của một màn hình: 34, 65, 66, 70, 73, 74, 81, 116, 117, 119, 157.

| Năng động | Số lượng bản đồ | Mô tả |
| --- | ---: | --- |
| Chu kỳ bảng màu (hiển thị) | 67 | 36 nước, 34 chu trình khác (3 có cả nước và các chu trình khác) |
| Xoay thuộc địa | 39 ảnh có ví dụ, tổng cộng 53 | 38 bản đồ vũ trụ khác có các thuộc địa được mở theo byte mẫu, nhưng không có thuộc địa nào trên màn hình |
| thay thế bản đồ 3D34 | 37 hình ảnh được cắt ghép | chuỗi truyện tranh, biến thể một phần, toàn bộ bản đồ được thay thế bằng bản đồ khác |
| Bố cục giống nhau nhưng thay đổi bảng màu | 3 nhóm | 0/138/139; 60/64; 66/157 (toàn màu đen) |
| Tham chiếu vòng tròn không hợp lệ | 28 hình ảnh | Tài nguyên hình tròn được tham chiếu nhưng không có pixel nào có số màu tương ứng trong tập bản đồ và màn hình sẽ không di chuyển |

## 2. Các kiểu luân chuyển bảng màu

17 tài nguyên tái chế. Chỉ có mặt nước được xác nhận trên màn hình (sông trên bản đồ 20); những cái tên còn lại được suy ra theo màu sắc và sử dụng bản đồ.

| Tài nguyên | Tên | Phạm vi màu | Màu × Khung | Số bước nhảy | Bản đồ có thể nhìn thấy |
| --- | --- | --- | --- | ---: | --- |
| 6419 | Mặt nước (màu xanh) | 0xC0–0xD0 | 17 × 9 | 81 | 2, 3, 5, 8, 9, 12, 13, 21, 22, 32, 38, 40, 53, 55, 57 |
| 6420 | Mặt nước (xám tím) | Tương tự như trên | Tương tự như trên | 81 | 11, 17, 56, 68 |
| 6421 | Mặt nước (xanh đậm, nghi là cảnh đêm) | Tương tự như trên | Tương tự như trên | 81 | 15, 63 |
| 6422 | Mặt nước (xám) | Tương tự như trên | Tương tự như trên | 81 | 14, 20 |
| 6423 | Mặt nước (màu xanh sáng) | Tương tự như trên | Tương tự như trên | 81 | 10, 16, 41, 43, 46 |
| 6424 | Mặt nước (ngọc lam) | Tương tự như trên | Tương tự như trên | 81 | 6, 30, 31, 45, 58, 59, 61, 73 |
| 6425 | Mặt nước (màu xanh) | Tương tự như trên | Tương tự như trên | 81 | Không được sử dụng |
| 6426 | Chu kỳ xanh đậm | 0xB0–0xBE | 15 × 8 | 64 | 35, 37, 39, 44, 72 |
| 6427 | Vòng chậm màu xanh lá cây | 0xA0–0xA8 | 9 × 32 | 192 | 7 |
| 6428 | Chu kỳ nâu cam | 0x10–0x14 | 5 × 10 | 90 | 3, 11 |
| 6429/6430 | Xung đỏ | 0x15–0x17 | 3 × 8 | 67 | 19, 20/0 |
| 6431 | Đèn flash màu xanh đậm (một khung hình mỗi lần nhảy) | 0xD0–0xDA | 11 × 11 | 11 | 109, 120–135 |
| 6432 | Vòng màu vàng | 0xDC–0xE0 | 5 × 8 | 48 | 78, 88 (mỗi cái 10 pixel) |
| 6433 | Vòng nhanh màu nâu đỏ | 0xF8–0xFF | 8 × 7 | 14 | 156 |
| 6434 | Vòng màu nâu đỏ | 0xF0–0xFF | 16 × 15 | 30 | 136 |
| 6435 | Vòng màu cam | 0xE0–0xE2 | 3 × 8 | 48 | 49, 50 |

**Diện tích mặt nước**: 36 bản đồ, sắp xếp từ nhiều đến ít theo số lượng pixel chuyển động:

- 56: 204.824; 13: 196.030; 16: 162.164; 46: 152.410; 15: 114.147
- 58: 99.320; 40: 90.252; 14: 84.949; 55: 78.347; 53: 74.685
- 11: 70.340; 6: 67.257; 5: 66.224; 45: 65.027; 8: 63.311; 63: 61.664
- 31:59.651; 12:58,156; 10:52.639; 30:48,755; 17:48,018; 41:42,421
- 9: 38.472; 43: 30.834; 68: 29.423; 2: 29.209; 59: 25.097; 38: 18.890
- 73: 16.423; 3: 13.740; 20: 13.010; 21: 8.091; 22: 6.852; 61: 5.992; 57: 5.834; 32: 5,669

Mặt nước trong 5 bức ảnh đầu tiên vượt quá 110.000 pixel, gần bằng một nửa bức ảnh.

## 3. Thuộc địa

77 bản đồ vũ trụ có byte chế độ là 1 sẽ chuyển sang bản đồ thuộc địa cứ sau 27 khung hình. 39 khung hình thực sự có khuẩn lạc trên đó:

| Số thuộc địa | Bản đồ |
| --- | --- |
| 5 | 90 |
| 4 | 77, 118 |
| 3 | 100 |
| 2 | 92, 98 |
| 1 | 79, 81, 86–89, 95, 96, 99, 103, 106, 107, 110, 111, 113, 116 và 140–156 |

38 còn lại có hình ảnh động thuộc địa nhưng không có lưới thuộc địa và không di chuyển trên màn hình: 75, 76, 78, 80, 82–85, 91, 93, 94, 97, 101, 102, 104, 105, 108, 109, 114, 115, 117, 120–136.

## 4. Thay đổi hình ảnh 3D34

| Loại | Kịch bản | Thay đổi bản đồ |
| --- | --- | --- |
| Chuỗi truyện tranh | 103 | 109 → 121, 123 … 135 → 136, mỗi bước là 38–46 khác với 109 |
| Chuỗi truyện tranh | 105 | 111 → 141, 143… 155 → 156, mỗi bước là 28–43 khác với 111 |
| Biến thể địa phương | 134 | 37 → 39 (5 ​​ô) |
| biến thể địa phương | 38 | 116 → 117 (17 ô) |
| Biến thể địa phương | 54 | 90 → 118 (22 ô) |
| Biến thể địa phương | 97 | 104 → 137 (17 ô) |
| Thay đổi bảng màu có cùng bố cục | 90, 102 | Chuyển từ 99 sang 60, 64 (cùng bố cục, hai bộ bảng màu đỏ và đen) và 157 (toàn màu đen), thứ tự cần kiểm tra |
| Thay thế toàn bộ bản đồ bằng bản đồ khác | 5, 7, 12, 16, 17, 26, 36, 38, 43, 44, 53, 100 | Ví dụ: cảnh 26 chuyển từ 9 sang 62; cảnh 16 chuyển sang màn hình đơn 74 |

Số ô trong bảng là chênh lệch so với bản đồ ban đầu của cảnh chứ không phải so với bước trước. Chỉ những số lẻ trong chuỗi truyện tranh mới được cắt thẳng vào kịch bản; các số chẵn 120-134 và 140-154 thuộc về "không tìm thấy tham chiếu tĩnh" trong Phần 5.

## 5. Không tìm thấy 25 tài liệu tham khảo tĩnh

28, 34, 70, 79, 80, 103, 106, 120, 122, 124, 126, 128, 130, 132, 134, 138, 139, 140, 142, 144, 146, 148, 150, 152, 154

Chúng có thể được truy cập gián tiếp thông qua bảng trạng thái 3D34 loại 0 (`8021E240`) hoặc hoàn toàn không thể sử dụng chúng. 138/139 có bố cục giống như bản đồ 0. Theo [HD Asset Inventory §3.3](hd-asset-inventory.md#33-其他动态), đó là biến thể cảnh đêm và ban ngày, cho thấy rằng thực sự có một đường dẫn chuyển đổi chưa được giải quyết. 25 ảnh này sẽ không được đưa vào sản xuất HD cho đến khi việc sử dụng được xác nhận.

## 6. Liệt kê từng cái một

Cột động:
- "Vòng lặp không hợp lệ": tài nguyên vòng lặp được tham chiếu không có pixel trong tập bản đồ;
- "Thuộc địa (không có phiên bản)": Hoạt ảnh thuộc địa được bật nhưng không có thuộc địa nào trên màn hình;
- "Same Layout": Liệt kê các bản đồ khác có cùng bố cục.

| Bản đồ | Kích thước | Thư viện ảnh | Bảng Màu | Cảnh đầu tiên | Động lực |
| ---: | --- | --- | --- | --- | --- |
| 0 | 608×512 | 6228 | 6239 | 3 Gunsmoke の中で và 5 khác | Xung đỏ 375 px; bố cục tương tự 138/139 |
| 1 | 592×384 | 6228 | 6237 | 11 时は流れた | tĩnh |
| 2 | 560×512 | 6228 | 6237 | 13 黑いガンダム | Mặt nước 29.209 px |
| 3 | 592×640 | 6228 | 6237 | 15 Kuしみの刀 | Mặt nước 13.740 px; chu kỳ màu nâu cam 91 px |
| 4 | 496×608 | 6228 | 6243 | 10 Nhóm Máy Giết Người | Vòng lặp không hợp lệ 6422 |
| 5 | 672×560 | 6228 | 6237 | 0 戦え!热き血のファイターたち | Mặt nước 66.224 px |
| 6 | 624×512 | 6228 | 6249 | 30 オペレーション・デイブレイク và 3 khác | Mặt nước 67.257 px |
| 7 | 864×800 | 6230 | 6256 | 82 ゆがむCosmos và 3 khác | Vòng lặp chậm màu xanh lá cây 322 px |
| 8 | 704×608 | 6228 | 6237 | 24 撃撃のビクトリア và 2 khác | Mặt nước 63.311 px |
| 9 | 560×800 | 6228 | 6237 | | Nước 38.472 px; Cắt 3D34 (Cảnh 26) |
| 10 | 624×512 | 6228 | 6247 | | Nước 52.639 px; Cắt 3D34 (Cảnh 12) |
| 11 | 864×544 | 6228 | 6238 | 18 Buồn しみのホンコンシティ và 2 khác | Mặt nước 70.340 px; Chu kỳ màu nâu cam 956 px |
| 12 | 704×592 | 6228 | 6237 | 23 Thị trấn Rikiri no | Mặt nước 58.156 px |
| 13 | 704×640 | 6228 | 6237 | 16 杀を道くガンダム | Mặt nước 196.030 px |
| 14 | 672×608 | 6228 | 6243 | 28 Tạm biệt, tôi là giáo viên, v.v. 2 | Mặt nước 84.949 px |
| 15 | 752×432 | 6228 | 6239 | 21 Misato Fate và 2 người khác | Mặt nước 114.147 px |
| 16 | 720×592 | 6228 | 6246 | 31 さらば戦士よ | Mặt nước 162.164 px |
| 17 | 672×592 | 6228 | 6238 | 32 Liangshan Bo's の戦い và 2 người khác | Mặt nước 48.018 px |
| 18 | 576×512 | 6228 | 6243 | | Cut-in 3D34 (Cảnh 17) |
| 19 | 480×400 | 6228 | 6237 | 2 dòng chảy | xung đỏ 423 px |
| 20 | 448×512 | 6228 | 6243 | 1 出撃!スイームルグ | Mặt nước 13.010 px; Xung đỏ 69 px |
| 21 | 496×400 | 6228 | 6237 | 4 Tức giận りの家児魔神立つ! | Mặt nước 8.091 px |
| 22 | 672×496 | 6228 | 6237 | 5 ミケーネと百鬼 và 2 khác | Mặt nước 6.852 px; Cắt 3D34 (cảnh 5) |
| 23 | 544×432 | 6228 | 6237 | 14 Naru xinh đẹp・カイン | Vòng lặp không hợp lệ 6419 |
| 24 | 704×800 | 6228 | 6237 | 63 thanh trừng | tĩnh |
| 25 | 608×768 | 6228 | 6237 | 33 Âm thanh của vũ trụ | tĩnh |
| 26 | 544×432 | 6228 | 6243 | 9 Dám thua! ル・カインのThử thách | Tĩnh |
| 27 | 560×544 | 6228 | 6252 | | Cut-in 3D34 (Cảnh 7) |
| 28 | 624×672 | 6228 | 6238 | | Không tìm thấy tham chiếu tĩnh |
| 29 | 544×704 | 6228 | 6252 | 20 Hazama Yuu của biển và đất | Tĩnh |
| 30 | 704×592 | 6228 | 6245 | 27 lý tưởng, sụp đổ | mặt nước 48.755 px |
| 31 | 864×640 | 6228 | 6250 | 39 Minh Tinh Thủy Thủy | Mặt nước 59.651 px |
| 32 | 768×672 | 6228 | 6237 | 40 その名はエピオン và 2 khác | Mặt nước 5.669 px |
| 33 | 672×592 | 6228 | 6237 | 42 マーズとマーグ | tĩnh |
| 34 | 320×240 | 6228 | 6237 | | Không tìm thấy tham chiếu tĩnh |
| 35 | 864×672 | 6230 | 6262 | | Vòng lặp màu xanh đậm 173 px; Đoạn cắt 3D34 (cảnh 43/44) |
| 36 | 704×592 | 6232 | 6254 | 25 シャピロ、転生! | Tĩnh |
| 37 | 528×1024 | 6230 | 6261 | 134 Kinh hoàng!デビルアクシズ bắt đầu di chuyển! (Quay lại) | Chu kỳ màu xanh đậm 132 px |
| 38 | 640×560 | 6228 | 6242 | 65 Đốt Đốt Sao Băng | Mặt nước 18.890 px |
| 39 | 528×1024 | 6230 | 6261 | | Vòng lặp màu xanh đậm 132 px; Đoạn cắt 3D34 (cảnh 134) |
| 40 | 704×608 | 6228 | 6237 | 68 đột nhập! Pháo đài di động をphá vỡ 壊せよ! (phía trước) | Mặt nước 90.252 px |
| 41 | 704×544 | 6228 | 6246 | 64 xa き平和 | mặt nước 42.421 px |
| 42 | 704×544 | 6228 | 6237 | 66 戦いの意は | Tĩnh |
| 43 | 704×624 | 6228 | 6246 | 67 サンクキングダム、Beng Lei | Mặt nước 30.834 px |
| 44 | 960×704 | 6230 | 6261 | Chương 135 xông vào! Pháo đài di động をbreaker壊せよ! (Quay lại) | Chu kỳ màu xanh đậm 301 px |
| 45 | 608×704 | 6228 | 6249 | 69 vòng tròn trái đất bị mây đen bao phủ | mặt nước 65.027 px |
| 46 | 784×640 | 6228 | 6247 | 47 Sự thống nhất của vòng tròn trái đất | Mặt nước 152.410 px |
| 47 | 752×608 | 6228 | 6245 | 46 新しき道 | tĩnh |
| 48 | 640×880 | 6228 | 6245 | 48 Humanity's Victory, Hikari... (phía trước) và 2 cái khác | Tĩnh |
| 49 | 608×816 | 6231 | 6253 | 36 Sự kết thúc của tham vọng và 2 điều nữa | Vòng cam 45 px |
| 50 | 736×688 | 6231 | 6253 | 50 ムーンアタック và 3 khác | Vòng màu cam 45 px |
| 51 | 832×640 | 6228 | 6255 | 57 キリマンジャロの兰 | tĩnh |
| 52 | 800×672 | 6228 | 6237 | 58 Eternal のフォウ(ボツ) và 8 khác | Tĩnh |
| 53 | 608×800 | 6228 | 6237 | 55 その风に心素して | Mặt nước 74.685 px |
| 54 | 432×544 | 6228 | 6238 | 8 ngày!? 比比のとき | Tĩnh |
| 55 | 800×560 | 6228 | 6237 | 78 Căn cứ máy bay chiến đấu quái thú Hui tấn công | Mặt nước 78.347 px |
| 56 | 864×800 | 6228 | 6238 | 129 Cổng Tử Thần! Trận chiến đảo Ruga (Sau) và 2 trận nữa | Mặt nước 204.824 px |
| 57 | 640×560 | 6228 | 6237 | 80 Hoàng hậu ジャネラの人人杀り | Mặt nước 5.834 px |
| 58 | 560×640 | 6228 | 6249 | 81 Trận đột phá quyết định (mặt trận) | Mặt nước 99.320 px |
| 59 | 720×672 | 6228 | 6249 | 83 それでもあきらめずに (phía trước) và 2 khác | Mặt nước 25.097 px |
| 60 | 800×640 | 6231 | 6259 | | Bố cục tương tự như 64; Đoạn cắt 3D34 (cảnh 90/102) |
| 61 | 784×656 | 6228 | 6245 | 92 见えないNgày mai | Mặt nước 5.992 px |
| 62 | 576×800 | 6228 | 6255 | | Cut-in 3D34 (Cảnh 26) |
| 63 | 864×544 | 6228 | 6239 | 79 Cổng Tử Thần! Trận chiến đảo Ruga (phía trước) và 2 trận khác | Mặt nước 61.664 px |
| 64 | 800×640 | 6231 | 6251 | | Bố cục tương tự như 60; Đoạn cắt 3D34 (cảnh 90/102) |
| 65 | 320×240 | 6228 | 6252 | 7 Sao băng がrơiちた日 | Vòng lặp không hợp lệ 6429 |
| 66 | 320×240 | 6233 | 6257 | 12 Sao Băng Thiếu Nữ | Bố cục tương tự 157 |
| 67 | 480×416 | 6228 | 6243 | 17 爱・戦士たち | tĩnh |
| 68 | 512×416 | 6228 | 6238 | 124 thời gian xác định | mặt nước 29.423 px |
| 69 | 704×608 | 6228 | 6237 | 123 ここより公に | tĩnh |
| 70 | 320×240 | 6229 | 6258 | | Không tìm thấy tham chiếu tĩnh |
| 71 | 640×896 | 6228 | 6237 | 130 Trận chiến đột phá quyết định (Sau) | Tĩnh |
| 72 | 960×704 | 6230 | 6261 | 132 アクシズのtấn công và phòng thủ (trung bình) | Chu kỳ màu xanh đậm 243 px |
| 73 | 320×240 | 6228 | 6250 | 43 その tương lai nổi bật は影ることなく và 2 khác | mặt nước 16.423 px |
| 74 | 320×240 | 6236 | 6244 | | Cut-in 3D34 (Cảnh 16) |
| 75 | 880×672 | 6229 | 6258 | 34 giảりの平和 | Thuộc địa (không có ví dụ) |
| 76 | 880×672 | 6229 | 6258 | 35 热闘!ラビアンローズ | Thuộc địa (không có ví dụ) |
| 77 | 880×672 | 6229 | 6258 | 37 スウィートウォーターChiến tranh phòng thủ | Thuộc địa ×4 |
| 78 | 800×640 | 6229 | 6258 | | Vòng màu vàng 10 px; Thuộc địa (không có trường hợp); Cắt 3D34 (Cảnh 36) |
| 79 | 800×704 | 6229 | 6258 | | Thuộc địa ×1; không tìm thấy tham chiếu tĩnh |
| 80 | 800×640 | 6229 | 6258 | | Thuộc địa (không có trường hợp); không tìm thấy tham chiếu tĩnh |
| 81 | 320×240 | 6229 | 6258 | 100 駆り立てるTham vọng | Thuộc địa ×1 |
| 82 | 880×720 | 6229 | 6258 | 107 トールギス壊 | Thuộc địa (không có ví dụ) |
| 83 | 832×752 | 6229 | 6258 | 76 anh em | Thuộc địa (không có ví dụ) |
| 84 | 816×736 | 6229 | 6258 | 71 Mối đe dọa của Đế chế Thiên hà và 3 mối đe dọa khác | Thuộc địa (không có ví dụ) |
| 85 | 880×800 | 6229 | 6258 | 72 ホワイトファング | Thuộc địa (không có ví dụ) |
| 86 | 784×704 | 6229 | 6258 | 75 Sao Mộc 帰りの男 | Thuộc địa ×1 |
| 87 | 720×560 | 6229 | 6258 | 53 Sự Kết Thúc Của Hỗn Loạn | Thuộc địa ×1 |
| 88 | 736×784 | 6229 | 6258 | 51 Tham vọng không có đường lối, không có kết quả, v.v. 2 | Vòng màu vàng 10 px; Thuộc địa ×1 |
| 89 | 880×704 | 6229 | 6258 | 61 Mặt Trận Chung | Thuộc địa ×1 |
| 90 | 784×704 | 6229 | 6258 | 54 真粋であるがゆえに | Thuộc địa ×5 |
| 91 | 848×752 | 6229 | 6258 | 59 アクシズからの Messenger | Thuộc địa (không có ví dụ) |
| 92 | 864×704 | 6229 | 6258 | 60 シロッコ立つ | Thuộc địa ×2 |
| 93 | 704×624 | 6229 | 6258 | | Thuộc địa (không có trường hợp); Cut-in 3D34 (Cảnh 38) |
| 94 | 768×704 | 6229 | 6258 | Hạm đội tiến công của quân đội đế quốc thiên hà 77 | Thuộc địa (không có ví dụ) |
| 95 | 880×704 | 6229 | 6258 | 84 Chiến thắng | Thuộc địa ×1 |
| 96 | 880×640 | 6229 | 6258 | 85 Áp Lực Vòng Trái Đất | Thuộc địa ×1 |
| 97 | 560×960 | 6229 | 6258 | 86 Battlefield (cũ) và 3 khác | Thuộc địa (không có ví dụ) |
| 98 | 880×704 | 6229 | 6258 | 87 Tham vọng | Thuộc địa ×2 |
| 99 | 880×704 | 6229 | 6258 | 89 Giấc mơ, Zai Lai, v.v. 4 | Thuộc địa ×1 |
| 100 | 960×720 | 6229 | 6258 | 88 アクシズのtấn công và phòng thủ (phía trước) và 3 khác | Thuộc địa ×3 |
| 101 | 800×704 | 6229 | 6258 | 91 Khúc mở màn cho sự hủy diệt | Thuộc địa (không có ví dụ) |
| 102 | 880×720 | 6229 | 6258 | 96 Trận chiến! Trận chiến của hoàng đế! (Trước) | Thuộc địa (không có ví dụ) |
| 103 | 800×640 | 6229 | 6258 | | Thuộc địa ×1; không tìm thấy tham chiếu tĩnh |
| 104 | 864×640 | 6229 | 6258 | 97 Tương lai của sự sống và cái chết | Vòng lặp 6432 không hợp lệ; Thuộc địa (không có ví dụ) |
| 105 | 880×624 | 6229 | 6258 | 73 tranh giành thế giới (trước đây) và 2 cái nữa | Thuộc địa (không có ví dụ) |
| 106 | 880×720 | 6229 | 6258 | | Thuộc địa ×1; không tìm thấy tham chiếu tĩnh |
| 107 | 880×704 | 6229 | 6258 | | Thuộc địa ×1; Cắt 3D34 (Cảnh 100) |
| 108 | 960×720 | 6229 | 6258 | 101 cuộc đời, Sanって | Thuộc địa (không có ví dụ) |
| 109 |
| 110 | 800×640 | 6229 | 6258 | 104 Kinh hoàng!デビルアクシズ bắt đầu! (Trước) | Thuộc địa ×1 |
| 111 | 800×640 | 6229 | 6258 | 105 Vũ Trụ La Hét | Vòng lặp 6431 không hợp lệ; Thuộc địa ×1 |
| 112 | 736×544 | 6234 | 6260 | 106 Tương Lai をこの手に | Tĩnh |
| 113 | 800×704 | 6229 | 6258 | 45 Hunmiへの出撃 | Vòng lặp 6431 không hợp lệ; Thuộc địa ×1 |
| 114 | 896×800 | 6229 | 6258 | 110 F91 Jin và 7 người khác | Vòng lặp 6431 không hợp lệ; Thuộc địa (không có ví dụ) |
| 115 | 864×768 | 6229 | 6258 | | Vòng lặp 6431 không hợp lệ; Thuộc địa (không có trường hợp); Cắt 3D34 (cảnh 53) |
| 116 | 320×240 | 6229 | 6258 | Chia 38 OZ (trước đây) | Chu kỳ 6431 không hợp lệ; Thuộc địa ×1 |
| 117 | 320×240 | 6229 | 6258 | | Vòng lặp 6431 không hợp lệ; Thuộc địa (không có trường hợp); Cắt 3D34 (cảnh 38) |
| 118 | 784×704 | 6229 | 6258 | | Vòng lặp 6431 không hợp lệ; Thuộc địa ×4; Cắt 3D34 (Cảnh 54) |
| 119 | 320×240 | 6228 | 6237 | 26 Đường Sơn Máu | Tĩnh |
| 120 | 880×720 | 6229 | 6258 | | đèn flash màu xanh đậm 1.009 px; thuộc địa (không có trường hợp); không tìm thấy tham chiếu tĩnh |
| 121 | 880×720 | 6229 | 6258 | | Đèn flash màu xanh đậm 1.009 px; thuộc địa (không có trường hợp); Đoạn cắt 3D34 (cảnh 103) |
| 122 | 880×720 | 6229 | 6258 | | đèn flash màu xanh đậm 1.009 px; thuộc địa (không có trường hợp); không tìm thấy tham chiếu tĩnh |
| 123 | 880×720 | 6229 | 6258 | | Đèn flash màu xanh đậm 1.009 px; thuộc địa (không có trường hợp); Đoạn cắt 3D34 (cảnh 103) |
| 124 | 880×720 | 6229 | 6258 | | đèn flash màu xanh đậm 1.009 px; thuộc địa (không có trường hợp); không tìm thấy tham chiếu tĩnh |
| 125 | 880×720 | 6229 | 6258 | | Đèn flash màu xanh đậm 1.009 px; thuộc địa (không có trường hợp); Đoạn cắt 3D34 (cảnh 103) |
| 126 | 880×720 | 6229 | 6258 | | đèn flash màu xanh đậm 1.009 px; thuộc địa (không có trường hợp); không tìm thấy tham chiếu tĩnh |
| 127 | 880×720 | 6229 | 6258 | | Đèn flash màu xanh đậm 1.009 px; thuộc địa (không có trường hợp); Đoạn cắt 3D34 (cảnh 103) |
| 128 | 880×720 | 6229 | 6258 | | đèn flash màu xanh đậm 1.009 px; thuộc địa (không có trường hợp); không tìm thấy tham chiếu tĩnh |
| 129 | 880×720 | 6229 | 6258 | | Đèn flash màu xanh đậm 1.009 px; thuộc địa (không có trường hợp); Đoạn cắt 3D34 (cảnh 103) |
| 130 | 880×720 | 6229 | 6258 | | đèn flash màu xanh đậm 1.009 px; thuộc địa (không có trường hợp); không tìm thấy tham chiếu tĩnh |
| 131 | 880×720 | 6229 | 6258 | | Đèn flash màu xanh đậm 1.009 px; thuộc địa (không có trường hợp); Đoạn cắt 3D34 (cảnh 103) |
| 132 | 880×720 | 6229 | 6258 | | đèn flash màu xanh đậm 1.009 px; thuộc địa (không có trường hợp); không tìm thấy tham chiếu tĩnh |
| 133 | 880×720 | 6229 | 6258 | | Đèn flash màu xanh đậm 1.009 px; thuộc địa (không có trường hợp); Đoạn cắt 3D34 (cảnh 103) |
| 134 | 880×720 | 6229 | 6258 | | đèn flash màu xanh đậm 1.009 px; thuộc địa (không có trường hợp); không tìm thấy tham chiếu tĩnh |
| 135 | 880×720 | 6229 | 6258 | | Đèn flash màu xanh đậm 1.009 px; thuộc địa (không có trường hợp); Đoạn cắt 3D34 (cảnh 103) |
| 136 | 880×720 | 6229 | 6258 | | vòng màu nâu đỏ 699 px; thuộc địa (không có trường hợp); Đoạn cắt 3D34 (cảnh 103) |
| 137 | 864×640 | 6229 | 6258 | | Vòng lặp 6434 không hợp lệ; Cắt 3D34 (cảnh 97) |
| 138 | 608×512 | 6228 | 6237 | | Bố cục tương tự 0/139; không tìm thấy tham chiếu tĩnh |
| 139 | 608×512 | 6228 | 6237 | | Bố cục tương tự 0/138; không tìm thấy tham chiếu tĩnh |
| 140 | 800×640 | 6229 | 6258 | | Vòng lặp 6433 không hợp lệ; Thuộc địa ×1; Không tìm thấy tham chiếu tĩnh |
| 141 | 800×640 | 6229 | 6258 | | Vòng lặp 6433 không hợp lệ; Thuộc địa ×1; Cắt 3D34 (cảnh 105) |
| 142 | 800×640 | 6229 | 6258 | | Vòng lặp 6433 không hợp lệ; Thuộc địa ×1; Không tìm thấy tham chiếu tĩnh |
| 143 | 800×640 | 6229 | 6258 | | Vòng lặp 6433 không hợp lệ; Thuộc địa ×1; Cắt 3D34 (cảnh 105) |
| 144 | 800×640 | 6229 | 6258 | | Vòng lặp 6433 không hợp lệ; Thuộc địa ×1; Không tìm thấy tham chiếu tĩnh |
| 145 | 800×640 | 6229 | 6258 | | Vòng lặp 6433 không hợp lệ; Thuộc địa ×1; Cắt 3D34 (cảnh 105) |
| 146 | 800×640 | 6229 | 6258 | | Vòng lặp 6433 không hợp lệ; Thuộc địa ×1; Không tìm thấy tham chiếu tĩnh |
| 147 | 800×640 | 6229 | 6258 | | Vòng lặp 6433 không hợp lệ; Thuộc địa ×1; Cắt 3D34 (cảnh 105) |
| 148 | 800×640 | 6229 | 6258 | | Vòng lặp 6433 không hợp lệ; Thuộc địa ×1; Không tìm thấy tham chiếu tĩnh |
| 149 | 800×640 | 6229 | 6258 | | Vòng lặp 6433 không hợp lệ; Thuộc địa ×1; Cắt 3D34 (cảnh 105) |
| 150 | 800×640 | 6229 | 6258 | | Vòng lặp 6433 không hợp lệ; Thuộc địa ×1; Không tìm thấy tham chiếu tĩnh |
| 151 | 800×640 | 6229 | 6258 | | Vòng lặp 6433 không hợp lệ; Thuộc địa ×1; Cắt 3D34 (cảnh 105) |
| 152 | 800×640 | 6229 | 6258 | | Vòng lặp 6433 không hợp lệ; Thuộc địa ×1; Không tìm thấy tham chiếu tĩnh |
| 153 | 800×640 | 6229 | 6258 | | Vòng lặp 6433 không hợp lệ; Thuộc địa ×1; Cắt 3D34 (cảnh 105) |
| 154 | 800×640 | 6229 | 6258 | | Vòng lặp 6433 không hợp lệ; Thuộc địa ×1; Không tìm thấy tham chiếu tĩnh |
| 155 | 800×640 | 6229 | 6258 | | Vòng lặp 6433 không hợp lệ; Thuộc địa ×1; Cắt 3D34 (cảnh 105) |
| 156 | 800×640 | 6229 | 6258 | | Vòng lặp nhanh màu nâu đỏ 134 px; Thuộc địa ×1; Cắt 3D34 (Cảnh 105) |
| 157 | 320×240 | 6233 | 6263 | | Tương tự như bố cục 66; Đoạn cắt 3D34 (cảnh 90/102) |