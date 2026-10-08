> **Ngôn ngữ / Language:** [Tiếng Việt](native-ship-model.vi.md) · [English](native-ship-model.en.md) · [中文](native-ship-model.md)

# Mô hình cắt cảnh bản đồ thế giới HD: tàu, cột mốc và đường đi

24-09-2026. Trên bản đồ thế giới giữa các ô, những con tàu được vẽ ở đầu đường khi đoàn quân ra khơi, các mốc đặt theo khung cảnh và đường ray màu xanh trắng đều được thay thế bằng phiên bản có độ chính xác cao do GPU chủ vẽ. 15 mẫu đã được làm lại theo cài đặt chính thức (08–21.000 mặt mỗi mẫu, phiên bản gốc 4–330 mặt), các đường ray đã được thay thế bằng các dải ánh sáng mượt mà và bảng tên katakana hiển thị tiếng Nhật/tiếng Trung/tiếng Anh theo ngôn ngữ đọc. Trò chơi tiếp tục cung cấp vị trí, định hướng, camera và thời gian thực hiện mà không cần thay đổi ROM hoặc ghi RDRAM; F6 chuyển về màn hình gốc, F7 chuyển ngôn ngữ thương hiệu.

## Vẽ gì trên bản đồ thế giới

Bảng đối tượng mô hình `801C5670` (ROM `0xAAF30`) của lớp phủ bản đồ thế giới `load_000A7EC0` thu thập tất cả các tài nguyên ba chiều xuất hiện ở đây: tàu, 5600 điểm đánh dấu và bề mặt của từng khu vực. Lần này, ba đường dẫn sử dụng đã được đọc từ mã và được xác nhận ở cấp độ nhỏ thực tế:

1. **Tàu buồm**: `3D33` lấy `D_801C5644` với `engine+0x990` (`3D72 n` được viết là `n mod 15`) làm chỉ số phụ. Giá trị là **chỉ số dưới của bảng mô hình**, không phải số ký tự (phần giải thích trước đó về khóa bố cục đã được sửa tại chỗ). Khi `n = 0` được sử dụng, hãy lấy phần thân mà ブライト (46) đang cưỡi và thay đổi nó thành chỉ số dưới thông qua phần thân → bảng khớp mẫu `801C560C`; nếu không tìm thấy, hãy sử dụng 24.
2. **Các mốc được đặt theo cảnh**: Khi vào bản đồ thế giới `801C310C` kiểm tra 17 cảnh của `801C5728` theo số cảnh hiện tại, sau đó lấy danh sách (tài nguyên, vị trí) từ `801C57B0` và đặt chúng vào.
3. **Dấu**: `801C2E30` Tạo dấu vàng 5600 (khe `0x9C` trở đi); quá trình bình thường chỉ vượt qua k = 0.

| Đăng ký | Tài nguyên | Người mẫu | Ngoại hình | Lần này |
| --- | --- | --- | --- | --- |
| 0 | 5584 | アルビオン | Bộ bàn ghép 53; `3D72 11` | HD |
| 1 | 5585 | アーガマ | Đơn vị 51; `3D72 12` | HD |
| 2 | 5586 | アウドムラ | Đơn vị 52; `3D72 10` | HD |
| 3 | 5587 | ミデア | Đơn vị 64; `3D72 9` | HD |
| 4 | 5588 | ネェル・アーガマ | Đơn vị 63; `3D72 13` | HD |
| 5 | 5589 | ピースミリオン (Gundam W, khu vực) | `3D72 7` (tập lệnh gốc không được sử dụng) | HD |
| 6 | 5590 | リーブラ(có thẻ tên) | `3D72 6`; cảnh 84 địa danh | HD, bảng tên vẽ lại theo ngôn ngữ |
| 7 | 5591 | ラー・カイラム | Đơn vị 69; `3D72 14` | HD |
| 8 | 5592 | ラビアンローズ (có gắn thẻ tên) | Đơn vị 70; `3D72 4` | HD, bảng tên vẽ lại theo ngôn ngữ |
| 9 | 5593 | ゴラオン | Đơn vị 244; `3D72 2` | HD |
| 10 | 5594 | グラン・ガラン | Đơn vị 243; `3D72 1` | HD |
| 11 | 5595 | ガンドール (Siêu Thần Máy Thần ダンクーガ) | Đơn vị 222; `3D72 3` | HD |
| 12 | 5596 | バルジ(có thẻ tên) | `3D72 5` | HD, bảng tên vẽ lại theo ngôn ngữ |
| 15 | 5600 | dấu vàng | luôn | [thả bản địa](native-model-replacement.md) |
| 16 | 5601 | Cờ đỏ | Tạo không có mã | Chưa được xử lý |
| 21 | 5597 | デビルアクシズ (có gắn thẻ tên) | Không có vị trí cảnh | Chưa được xử lý |
| 22 | 5598 | アクシズ (ảnh bảng thông báo + thẻ tên) | Địa danh trong 13 cảnh | HD, thẻ tên vẽ lại theo ngôn ngữ |
| 23 | 5607 | フィフス・ルナ(có bảng tên) | Cảnh 103 Landmark | HD, bảng tên vẽ lại theo ngôn ngữ |
| 24 | 5587 | (Mặt hàng thứ hai của Micro) | `3D72 8`, dự phòng mặc định | Phiên bản gốc sẽ không được hiển thị, giữ |

Các chỉ số 13, 14, 17–20 là bề mặt của từng khu vực (14 = 5599 vũ trụ; 18/19 = 5604/5605 trái đất), là các kết cấu có độ phân giải cao và không nằm trong phạm vi của trang này. Các tham số `3D72` thực tế được tập lệnh gốc sử dụng chỉ là 0, 3, 8, 10, 12 và 14; những con tàu khác xuất hiện hoặc không bao giờ xuất hiện khi ブライト tình cờ có mặt trên tàu, nhưng chúng cũng được thay thế và hoạt động tương tự.

Danh sách mốc: アクシズXuất hiện trước và sau "Cuộc tấn công và phòng thủ của Ana", trước và sau "Nắm đấm của nỗi buồn tuyệt vọng", "Bóng tối của Ama", "Cuộc nổi loạn của Asa" và "Khủng bố! Ama bắt đầu hành động!" Trước và sau, "Vũ trụ la hét" và "Vũ trụ quyết định" trước và sau, "駆り立てるAmbition", "Life, Sanって", "Haruka Nana Gamble", "Awakening Nana Dream"; Furuta Chỉ có trong "シャアの nổi loạn"; Ruri trong "Cuộc chiến của Victor". Các cảnh trong "Agarashi Begins" cũng có Agarashi bình thường nên 5597 không có cơ hội xuất hiện.

Có hai danh sách hiển thị cho các tài nguyên có bảng tên: thân tàu (loại 0) và bảng tên (loại 5). Bản vẽ thành phần `8008A914` vẽ loại 5 làm bảng thông báo luôn hướng về phía camera; nội dung chính của アクシズ cũng là hình ảnh loại 5. Khi thay vỏ, chỉ di chuyển tấm có thân (cái có hình được thay bằng アクシズ), và bảng tên được vẽ lại theo ngôn ngữ (xem phần "Tên thương hiệu"). Cả hai có cùng nguồn gốc; Mẫu HD của アクシズ áp dụng ma trận bảng thông báo giống nhau nên được mô phỏng theo tư thế của ảnh, luôn hướng về phía camera.

## Thiết lập và tạo mô hình

Mô hình được xây dựng cục bộ bằng Blender và xuất sang `assets/models/<key>/mesh.json`; kho chỉ chứa chương trình đóng gói [`build_native_models.py`](../../tools/models/build_native_models.py). Tất cả các tập lệnh, tài liệu tham chiếu và bản ghi tài liệu để tạo mô hình đều được lưu trữ trong `assets/models/generators/` cục bộ và không được nhập vào kho (2026-10-06 do người dùng xác định: chỉ đóng gói mô hình vào gói HD). Hình ảnh tham khảo chỉ có thể xem được trong trình duyệt.

- **Hệ tọa độ**: Tọa độ cục bộ của từng tài nguyên ban đầu được sử dụng, +Y hướng lên trên, hướng mũi tàu phù hợp với phiên bản gốc (lô này là +Z), kích thước dựa trên hộp giới hạn ban đầu và tỷ lệ theo cài đặt chính thức. Theo tỷ lệ khung hình chính thức, アウドムラ và ミデア ngắn hơn 16–21% so với phiên bản gốc; sự khác biệt trục chính còn lại nằm trong khoảng ± 4%.
- **Đầu ra**: `assets/models/<key>/mesh.json` (vị trí, bình thường theo góc, màu đỉnh sRGB, alpha < 128 đối với lỗ thông hơi tự phát sáng), `model.glb`, xem trước và `compare.png`. Lưới, giống như các nội dung HD khác, chỉ cục bộ đối với `assets/` và không được phân phối cùng với mã nguồn.
- **Sự cân bằng đã biết**: Việc kết hợp màu sắc dựa trên mẫu ban đầu (2026-10-05 do người dùng xác định): ゴラオン sử dụng màu xanh lam nguyên bản (các sản phẩm ngoại vi có màu xanh xám đậm), アウドムラ sử dụng màu cam đất son nguyên bản (cài đặt TV có màu hồng cam); ピースミリオンChỉ có hình ảnh màu phối cảnh và tỷ lệ mặt phẳng tuân theo phiên bản gốc;ネェル・アーガマ dựa trên tỷ lệ phiên bản UC; dạng rồng ガンドール dùng để chỉ nguyên mẫu của các sản phẩm hiện đại. Tập lệnh xây dựng (cục bộ) cho từng mô hình liệt kê các thiếu sót còn lại.

Cơ sở thiết lập của Rare và Garra: Lớp "Phản công" Rare và Rare, tổng chiều dài 487 m, tổng chiều rộng 165 m, Rare Rare Masao Shoichi; được trang bị 4 pháo hạt miga (3 ở phía trước và 1 ở phía sau), 6 tên lửa cung và 22 súng phòng không Căn cứ, sàn phóng bên trái và bên phải và sàn đáp phía sau, cầu đôi, khối động cơ với tấm tản nhiệt dài ([ガンダムチャンネル](https://www.gundam-c.com/manual/mechanic/counter/ra-cailum.html), [ガンダムWiki](https://gundam.wiki.cre.jp/wiki/%E3%83%A9%E3%83%BC%E3%83%BB%E3%82%AB%E3%82%A4%E3%83%A9%E3%83%A0%E7%B4%9A)), ngoại hình được so sánh với [Cosmo Fleet Special](https://www.megahobby.jp/products/item/1437/).

## Theo dõi

Bản nhạc gốc được phát hành dần dần bởi `801C4960` mỗi khung hình: một `G_QUAD` ở mỗi bước, các đỉnh được lấy từ bộ đệm `801C97C0` (`801C3694` được thêm vào mẫu dịch ở mỗi bước) và c của màu PRIM `(c, c, 255)` được thay đổi dần từ 0 thành `801C3958` theo tổng số bước. 255. Mẫu khu vực Trái đất có kích thước 10×10 khối, cứ 8 đơn vị một bước; diện tích vũ trụ là 6×6, cứ 4 đơn vị, chiều cao −10. Các khối được căn chỉnh trên trục của chúng và xếp chồng lên nhau thành từng bậc răng cưa khi di chuyển theo đường chéo. Bản đồ thế giới chỉ có loại đường đi này và điểm khác biệt duy nhất giữa hai kiểu là mẫu.

Khi máy chủ nhận ra bộ lệnh này (chuỗi cố định `FA`/`E7`/`G_VTX 8`/`G_QUAD`, địa chỉ đỉnh nằm trong bộ đệm và mã `801C4960` thường trú nhất quán với ROM), nó sẽ lấy trung tâm, chiều rộng và màu sắc của tất cả các bước trên khối đầu tiên và chặn các khối còn lại. Điểm trung tâm là một tọa độ nguyên. Đầu tiên hãy tính trung bình động của các điểm cuối; sau đó vẽ một dải hình tam giác: chiều rộng bằng hình vuông ban đầu, cộng thêm quầng sáng 45%, kéo dài nửa hình vuông ở hai đầu, khử răng cưa các cạnh theo `fwidth` và màu sắc được nội suy dần từ `(c, c, 255)` ban đầu. So sánh độ sâu theo bản vẽ ban đầu, không ghi độ sâu và thực hiện bản vẽ hỗn hợp.

## Thẻ: đèn hiệu vàng

Vòng màu vàng nét đứt bên ngoài dấu 5600 là hình vuông nằm ngang 28×28 (y = 4) với bản đồ trong suốt 64×64, 1-bit: 12 dấu gạch ngang, tập trung tại atan2(−z, x) = 20,2° + 30°k, mỗi dấu gạch dài khoảng 10,5° và có bán kính 0,87–0,955 nửa chiều rộng; bù đắp bằng cách Vẽ bốn dải TRI2 `0x1A08`–`0x1A20` (cả hai bên). Máy chủ nhận ra bốn điều này khi xác định 5600: phần đầu tiên được thay thế bằng một mảnh hình vuông có cùng kích thước và một đoạn cung tròn được vẽ trong trình đổ bóng mảnh theo góc và bán kính trên (cạnh được khử răng cưa theo `fwidth`, cộng với một cạnh sáng và tối, rõ ràng hơn trên vùng đất sáng màu) và phần còn lại bị triệt tiêu; màu sắc là màu vàng ban đầu. Giống như thân 5600, nó chỉ có hiệu lực khi màn hình HD được tải và gói tài nguyên 5600 được tải.

Trên cơ sở đó, một "đèn hiệu vàng" được tạo ra (người dùng chọn từ ba hướng): người dẫn chương trình sử dụng đồng hồ riêng để điều khiển hoạt ảnh, còn vị trí, ống kính và thời gian xuất hiện vẫn do trò chơi xác định.

- **Xuất hiện**: Nếu dấu chưa được rút quá 0,25 giây thì coi như vừa xuất hiện; thân và vòng sẽ bật lại và phóng to (ease-out-back) trong vòng 0,55 giây, đồng thời phát ra gợn sóng sáng hơn từ trung tâm (bán kính 4 → 16 đơn vị trong vòng 0,8 giây). Mở dần dần, được kích hoạt mỗi khi `3D33` xuất hiện.
- **Ở lại**: Cơ thể nổi lên xuống ±1,2 đơn vị dọc theo Y cục bộ với thời gian 2,8 giây (nhân với phép biến đổi cục bộ trước ma trận thế giới của trò chơi mà không làm thay đổi dữ liệu trò chơi); 12 đoạn của vòng chấm chấm quay 18° mỗi giây; khung gầm tối màu ở giữa (bán kính khoảng 8,5 đơn vị, trong đường chấm) làm tăng độ tương phản trên mặt đất; một vòng tròn gợn sóng mờ dần mở rộng từ bán kính 5 lên 15 cứ sau 2,4 giây, biến mất ngay sau khi vượt qua đường chấm (bán kính khoảng 12,8). Tất cả các hiệu ứng được thu thập gần vòng chấm ban đầu (±14), không lớn hơn dấu ban đầu; mảnh hình vuông hình vòng chỉ được mở rộng đến ± 17 đơn vị để cho gợn sóng mờ dần.
- **Mô hình hóa bản thể** không có ở đây: gói tài nguyên 5600 được duy trì bởi một dòng công việc khác, hiện tại nó là khối đa diện vàng; đèn hiệu chỉ thêm tỷ lệ nổi và lối vào.

## Thương hiệu nổi tiếng

Các thẻ tên của リーブラ, ラビアンローズ, バルジ, アクシズ, và フィフス・ルナ là các biển hiệu nền đen đóng khung màu xanh lá cây có kích thước 200×30 (khung màu xanh lá cây rộng 2 đơn vị, mỗi tấm có một biển báo hai mặt trong) bản đồ katakana 64×64), được vẽ phía trên cùng gốc của tàu hoặc mốc. Văn bản nằm trong kết cấu và không đi qua hệ thống văn bản nên được xử lý riêng:

- **Tên**: Tiếng Nhật sử dụng nguyên văn trên bảng tên; đối với tiếng Trung và tiếng Anh lấy bảng nhập vùng dữ liệu `content/locales/terms/`. Nếu không, hãy kiểm tra danh sách tên dòng (フィフス・ルナ → Luna 5 / Fifth Luna, tiếng Trung phù hợp với tên địa hình vùng dữ liệu "5th ルナ"). Hiện tại là Libra, La Vie en Rose, Barge, Axis và Fifth Luna. Chỉ cần đóng gói lại danh sách mục sau khi thay đổi nó.
- **Kết cấu**: vẽ lại theo phong cách thương hiệu ban đầu khi đóng gói (8 pixel mỗi đơn vị, 1600×240; nét đậm HarmonyOS Sans, độ nghiêng phải 0,22, cộng với bóng tối), một cho mỗi ngôn ngữ; mipmap được tạo sau khi máy chủ tải.
- **Bản vẽ**: Danh sách hiển thị bảng tên (loại 5) cũng được xác định bằng lệnh offset. Hình đầu tiên được thay thế bằng hình tứ giác có kết cấu 200×30 và phần còn lại bị loại bỏ. Ngôn ngữ lấy thư mục hiện tại (`localization::snapshot()`) khi phân loại và biên dịch id bản vẽ. Hai mục tiêu hiển thị trong cùng một khung hình đều nhất quán; F7 có hiệu lực ngay lập tức.
- **Chế độ màn hình**: Bảng tên là văn bản nên ở màn hình gốc chỉ có bản tiếng Nhật giữ nguyên kết cấu gốc, còn tiếng Trung và tiếng Anh vẫn hiển thị tên dịch; ở màn hình HD, cả ba ngôn ngữ đều sử dụng nhãn hiệu được vẽ lại.
- **Thẻ tên vùng không gian**: Bản thân bề mặt không gian 5599 mang 7 nhãn hiệu giống hệt nhau (danh sách hiển thị loại 5 6–12: サイド1/2/3/5/6/7, スウィートウォーター). Chúng không thay đổi lưới và chỉ có các mục nhập tên thương hiệu trong gói tài nguyên (danh sách `plates`, `BOARDS` của tập lệnh đóng gói). Host vẫn nhận dạng bằng lệnh offset và vẽ bằng ngôn ngữ. Tiếng Trung và tiếng Anh là Mặt 1…Mặt 7 (bản dịch dòng) và Sweetwater. Xem [Bản đồ thế giới phim truyền hình HD](native-worldmap-regions-hd.md).

Máy thực tế: Cấp độ tương tự được bắt đầu bằng tiếng Nhật, tiếng Trung và tiếng Anh tương ứng. Hai cột mốc và bảng tên của ba con tàu nổi tiếng được hiển thị theo ngôn ngữ và hướng phù hợp với phiên bản gốc (biển tên quay theo hướng và đảo ngược khi bay sang trái, đó là hành vi ban đầu); nhấn F7 liên tục trong khi chạy và bảng tên Axis thay đổi thành tiếng Nhật → tiếng Trung → tiếng Anh; trong màn hình gốc, văn bản tiếng Nhật vẫn giữ nguyên kết cấu ban đầu và bản dịch tiếng Trung và tiếng Anh được hiển thị.

Phiên bản tiếng Trung của "ラビアンローズ" đã được thống nhất thành "La Vie en Rose" theo quyết định của người dùng (danh sách mục trong vùng dữ liệu phù hợp với danh sách tên dòng). Tên tiếng Trung của バルジ được người dùng xác định là "Pháo đài Baruchi" (tên đầy đủ của tên địa hình và bảng tên được sử dụng, các từ xuất hiện riêng trong dòng được đổi thành "Baruchi"). Tên tiếng Anh được thống nhất là Barge (dòng "バルジ pháo đài" là Pháo đài Barge).

## Quyền truy cập máy chủ

Đi theo con đường của [5600 giọt nước bản địa](native-model-replacement.md):

- [`native_model_hook_patches.py`](../../tools/recomp/toolchain/native_model_hook_patches.py) Hãy để `TRI2` của RT64 (`G_QUAD` cũng vào đây) gọi hook phân loại; tàu DL chủ yếu là `TRI2`.
- [`native_marker.cpp`](../../src/host/native_marker.cpp) Kiểm tra từng byte tài nguyên gốc hoàn chỉnh tại địa chỉ cơ sở phân đoạn 4. Lệnh offset rơi vào bảng lệnh hình tam giác của danh sách hiển thị được thay thế trước khi nhấn; cái đầu tiên có dấu bản vẽ gốc, phần còn lại bị loại bỏ (đoạn id `0x534D`) và đoạn id rãnh ghi `0x5452`. Sự chuyển đổi xuất phát từ khối lượng công việc bất biến tại nơi đặt bản vẽ và cài đặt độ sâu tuân theo bản vẽ ban đầu; Bóng tàu là màu đỉnh cộng với ánh sáng chính, ánh sáng lấp đầy, ánh sáng nổi bật và ánh sáng cạnh.
- [`build_native_models.py`](../../tools/models/build_native_models.py) Truy xuất từng tài nguyên từ ROM (kiểm tra SHA-256), phân tích lệnh tam giác của danh sách hiển thị được thay thế (từ chối thay đổi ma trận và lệnh gọi danh sách phụ) và viết `build/recomp/native-models/assets/` cùng với lưới; Thuyền buồm được phóng to 1,3 lần khi đóng gói (trình bày lựa chọn, lưới vẫn theo tỷ lệ đã đặt), biển tên, cột mốc không được phóng to. Tệp kê khai ghi lại vị trí ROM và dấu vân tay của mã theo dõi, cũng như các mắt lưới bị thiếu và tài nguyên chưa được xử lý.
- **Gói tài nguyên không chứa dữ liệu ROM** (từ 2026-09-25, tệp kê khai `srw64.native-models.v2`, `srw64.native-marker.v2`): Tài nguyên gốc chỉ được ghi trong tệp kê khai với số tài nguyên, số byte được giải mã và SHA-256, đồng thời mã bản nhạc được ghi với độ lệch ROM, độ dài và SHA-256. Máy chủ giải mã các bản gốc này (`src/native/app/rom_import_codec.hpp`, cùng bộ với bộ nhập) từ ROM của trình phát khi nó nhận dạng danh sách hiển thị lần đầu tiên, kiểm tra bản tóm tắt và lưu nó theo thứ tự từ RDRAM, sau đó so sánh từng byte. Trò chơi chưa được tải vào ROM khi tạo trình kết xuất nên nó được thực hiện trong lần nhận dạng đầu tiên; nếu bản tóm tắt không khớp thì bản tóm tắt đó sẽ không được thay thế và `SRW64 native models disabled` sẽ được ghi vào nhật ký. Chỉ phát lại phần thăm dò khung của danh sách hiển thị mà không tải trò chơi, sử dụng `SRW64_ROM_PATH` để trỏ đến `.z64`. Các tệp còn lại trong gói đều được tạo mới: lưới lấy từ mô hình Blender (mô hình ban đầu chỉ được sử dụng để hiển thị so sánh), bảng tên được tạo từ HarmonyOS Sans và các đường viền được vẽ (tiếng Nhật cũng được gõ lại) và lưới 5600 được tạo ở kích thước lưỡng cực ban đầu. `validate()` yêu cầu mọi tệp trong thư mục phải có trong danh sách và các tệp bổ sung (chẳng hạn như phiên bản cũ của `*.reference.bin`) sẽ trực tiếp báo lỗi.
- Khử răng cưa: Máy chủ mặc định cho phép RT64 vẽ toàn bộ khung cảnh ở tốc độ 4x MSAA (`SRW64_MSAA`, xem [Hướng dẫn phát triển](../guide/native-development.md)). Các đường ống bản địa này được xây dựng theo số lượng mẫu của mục tiêu cảnh nên các cạnh của tàu và các thương hiệu nổi tiếng cũng được khử răng cưa; đường ống giọt nước 5600 cũng được thay đổi để được lưu vào bộ đệm theo định dạng đích để tránh việc biên dịch lặp lại khi kích thước ban đầu và mục tiêu mở rộng xen kẽ nhau. Máy thực tế đã so sánh toàn bộ quy trình cấp độ nhỏ với đoạn hội thoại (bản đồ thế giới, bản đồ chiến thuật, các trang liên trường và kho lưu trữ) với so sánh từng khung hình khi MSAA bị tắt. Nội dung của màn hình nhất quán và không bị thiếu hoặc đặt sai vị trí (các pixel cạnh khác nhau); các thanh ngang trong quá trình chuyển đổi giống nhau và là hiệu ứng đường quét riêng của trò chơi.
- Chuyển đổi: `SRW64_NATIVE_MODELS=<资源包>` hoặc `run_host_probe.py --native-models`; hành vi của máy chủ không thay đổi khi không được đặt. Được liên kết với chế độ hình ảnh, Original giữ lại tất cả các hình tam giác và rãnh gốc ban đầu (xem phần trước để biết quy tắc về bảng tên).

## xác minh

Hai cấp độ nhỏ:

- [`worldmap-models.json`](../../config/recomp/mini-stages/worldmap-models.json): Gắn cảnh 103, bản đồ thế giới tự động hiển thị アクシズ và フィフス・ルナ; sau khi định vị hai điểm mốc theo trình tự, `3D72 1`–`14` mỗi điểm thực hiện một chuyến đi ngắn trong khu vực vũ trụ `3D33`.
- [`worldmap-libra.json`](../../config/recomp/mini-stages/worldmap-libra.json): Gắn cảnh 84, dừng lại ở mốc リーブラ.
- [`ra-cailum.json`](../../config/recomp/mini-stages/ra-cailum.json) để hiển thị một con tàu: mỗi chuyến có hai chuyến đi trong khu vực Trái đất và không gian.

```sh
.venv/bin/python tools/models/build_native_models.py
SRW64_NATIVE_MODELS=build/recomp/native-models/assets .venv/bin/python tools/recomp/debug/srw64ctl.py \
  launch --mini-stage config/recomp/mini-stages/worldmap-models.json --images hd
```

24-09-2026 Kết quả thực tế của máy:

- `worldmap-models` Trong một lần chạy, tất cả 15 mô hình đều được vẽ nguyên bản (khoảng 260-300 lần cho mỗi mô hình cho chiếc thuyền buồm và 5.704 lần cho mỗi mô hình cho hai cột mốc). Nhấn F6 để lấy khung gốc và mỗi khung đều có hình vẽ gốc, `rdram_modified: false`; 1.417 ảnh chụp nhanh của đường đua, 2.834 bản vẽ gốc và không có ảnh chụp nhanh nào hết hạn.
- Chạy cùng cấp độ một lần ở chế độ HD và Nguyên bản, đồng thời chụp ảnh màn hình điểm cố định sau mỗi 50 VI kể từ khi vào; thời gian của cấp độ được xác định và vị trí của các tàu trong cùng một khung là nhất quán và chúng được so sánh từng cái một. All ship bows are facing the sailing direction, and the occlusion relationship between the nameplate and the ship body is consistent with the original version; `3D72 8` (chỉ số 24) chỉ có đường ray và không có tàu ở cả hai bên, phù hợp với phiên bản gốc.
- Ảnh chụp màn hình điểm cố định gốc/HD của `worldmap-libra`: リーブラ Các cột mốc được thay thế, bảng tên và dấu hiệu được xếp chồng lên nhau như bình thường.
- `tests/test_native_models.py`: Đọc hai bảng từ ROM để xác nhận rằng `3D72 14` và nội dung 69 đều trỏ đến 5591; lệnh và số tam giác 5591; gói tài nguyên khứ hồi, phát hiện giả mạo, loại bỏ lưới xấu; đặt tên thương hiệu, phong cách và bao bì của các nguồn lực có thương hiệu.

## Hạn chế và theo dõi

- 5597 (デビルアクシズ) và 5601 (dấu đỏ) không có đường thoát và tạm thời không được xử lý; bề mặt bản đồ sẽ được xử lý ở dạng họa tiết có độ nét cao.
- Bản thân bối cảnh cốt truyện gốc chưa được diễn trên máy thật; việc xác minh dựa trên lớp phủ bản đồ thế giới ban đầu, `3D72`/`3D33` ban đầu và khởi tạo mốc cảnh.
- Ánh sáng là sự gần đúng của không gian thị giác cố định, không có bóng hoặc phản xạ môi trường; tự chiếu sáng vòi phun và quầng sáng theo dõi là những tính năng mới.
- Tương tự như 5600, chỉ truy cập vào đường dẫn macOS Metal. Nội dung lưới (`assets/models/`) chỉ mang tính cục bộ; gói tài nguyên không chứa dữ liệu ROM và có thể được phân phối riêng với gói HD.