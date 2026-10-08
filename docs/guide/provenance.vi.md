> **Ngôn ngữ / Language:** [Tiếng Việt](provenance.vi.md) · [English](provenance.en.md) · [中文](provenance.md)

# Bản ghi nguồn và đầu vào cục bộ

Tệp này ghi lại thông tin đầu vào cần thiết để tái tạo thử nghiệm nhưng không thể gửi tới Git. Băm là cổng nhận dạng, chúng không đại diện
Những tập tin này có thể được phân phối lại.

##ROM tiếng Nhật

- Vị trí tệp: `rom.z64` cục bộ, chưa được gửi;
- Kích thước: 33.554.432 byte;
- SHA-256: `ee5f4a21d8e5f7827d21199e27800edf250df9a8e4d10befb1a6992df597b13e`;
- Phép thuật Endian: `80371240`;
- Mã trò chơi/bản sửa đổi: `NS4J`, Rev 0;
- CRC tiêu đề: `1649d810 f73ad6d2`.

## Bản đồ glyph gốc tiếng Nhật

- Vị trí kho: `reference/original-glyph-map.csv`;
- Khóa nhận dạng độc lập: `config/data/original-glyph-map.json`, ghi lại SHA-256 hiện tại (lệch so với ngược dòng, xem phần tiếp theo);
- Nguồn: [Bản địa hóa](https://github.com/snowyegret23/Localize), cam kết `91e0c15b76b44c302f29ddebc1c45e61f1828cd0`;
- Tệp ngược dòng: `SRW N64/reference/srw64_glyph_map_seed.csv`, SHA-256
`f9e98bfca8ba13e5b37287bad5c795d57dd3f48b9e0d7865b330a5d5c1bd3567`;
- Mục đích: Giải mã văn bản từ ROM gốc tiếng Nhật để sử dụng trong các danh mục ngôn ngữ bản địa, duyệt dữ liệu và thử nghiệm phông chữ.

Ánh xạ ban đầu được di chuyển không thay đổi so với bản sao tham chiếu cũ; bản dựng không còn dựa vào toàn bộ kho tham chiếu nữa.
Việc nhận dạng ROM, bảng văn bản và phân tích tài nguyên được thực hiện độc lập bởi `src/srw64_rom/`.

### Độ lệch so với hạt giống ngược dòng (2026-09-17/18, được kiểm tra theo bitmap phông chữ)

1.936 dòng của hạt giống ngược dòng đều được gắn nhãn `confirmed`, nhưng 109 dòng trong số đó được ánh xạ bởi nhiều ID hình tượng.
Mỗi ô trong thư viện phông chữ là một glyph độc lập. Nếu hai ô có bitmap khác nhau nhưng diễn giải cùng một ký tự, thì một trong số chúng có thể bị đọc sai:
Trong số 109 nhóm, chỉ có 1 nhóm (khối đuôi khối tổng hợp) có bitmap giống hệt nhau. Sau khi so sánh lần lượt 108 nhóm còn lại, hầu hết nhóm nào cũng có một
Đó là một từ hoàn toàn khác. Việc đọc sai không chỉ giới hạn ở các hàng trùng lặp, vì vậy hãy kiểm tra lại toàn bộ bảng.

Phương pháp kiểm tra:

1. Trích xuất bitmap phông chữ từ tài nguyên ROM 0/1 (I4, 504×504 và 504×252; nửa chiều rộng 8×14 tương ứng với ID 0–314,
Toàn bộ chiều rộng 14×14 từ `0x13B` và tài nguyên 1 từ `0x597` và
`src/srw64_native/battle_assets.py` của cùng một bộ `font_tile`), cắt từng ô theo ID;
2. Hiển thị tất cả 7.335 ký tự CP932 bằng phông chữ tiếng Nhật của hệ thống và sắp xếp từng ô theo hình dạng: ánh xạ các ký tự đầu tiên và
1.149 dòng hàng đầu được đánh giá là phù hợp với ảnh bitmap (72 dòng được chọn ngẫu nhiên để xem xét thủ công và tất cả đều chính xác);
3. 602 ô có chiều rộng đầy đủ còn lại và tất cả 315 ô có chiều rộng nửa chiều rộng được so sánh và phóng to từng ô một theo cách thủ công và được xem xét với ngữ cảnh văn bản đã sửa
(Ví dụ: 1758+1774 đọc là "chạng vạng", 1504+1845 đọc là "Jiaozuo", 442+488+441 đọc là "bò đói ma");
So sánh các ký tự hiếm theo từng phần với các ký tự hiện có trong thư viện ký tự (ví dụ: “ác” của 1318 với “can” 356, “ge” thành “戦” 428,
đôi đen 1919 434, bán đôi + mua 1175);
4. Hầu hết các phần của thư viện ký tự được sắp xếp theo cách phát âm tiếng Nhật (năm mươi âm tiết), có thể được sử dụng làm bằng chứng tình tiết độc lập: 878 Zuo, 879 Zuo Fall
"Cuộc hôn nhân rắc rối và hận thù ngày nay → Zuo Zuo Cha Cha → Cai Bei", 1401 ấn, 1402 phải mở phần "Âm quyền Áo lỏng Âm đi Hà Lan",
1109 Zhi ở trong "Zhang Yu Town View → Zhi → Shen Zhen", 1200 Cha ở trong "Fu pair Bupu → Father → Fu Fufu",
1094 nghỉ ở "団 → nghỉ → nam nói chuyện", 722 gian hàng ở "chắc chắn so sánh → gian hàng → xue 楽", 912 video ở "riêng tư → video → kiểm tra",
1516 sụp đổ theo cách đọc huấn luyện つい(える) rơi vào "rent → sụp đổ → dừng lại", 1004 mới cứng rắn (ジン), 1562 悛(シュン)
Nó cũng rơi vào giữa "end → ? →図" và "粛 → ? → pure"; giá trị ban đầu của hạt giống (phải, đuổi, chị, 対, cung điện, thuộc tính, ôm)
Nó không thể được đọc ở những vị trí này. Tên nhân vật, chỉ dẫn tinh thần, địa hình và các phần khác cũng như các từ bổ sung sau một số đoạn văn không được sắp xếp theo cách phát âm.

Kết quả (hiện có 2.020 hàng, tất cả `confirmed`):

- Đã sửa **Dòng 147**: Dòng 112 bị nhận dạng sai thành các ký tự tiếng Trung khác (457 闘→ship, 1635 dark→wipe, 912 thuộc tính→sight, 1109 đuổi→thẳng, v.v.),
Dòng 24 là một khối phức hợp (1815+1816 kết hợp→パーツ, 1923–1953 được chia lại, 2047–2049 cựu→(phía trước),
1478beeの巣→xám), 6 dòng là ký hiệu và biểu tượng (212 $→±, 217 p→%, 218 _→~, 226 Ⅱ→Ⅲ,
258 f→🔧 Cờ lê sửa chữa, 259 c→E nhỏ), 2 cặp tổng thể có thể hoán đổi cho nhau (471/878 Zuo↔wei, 879/1402 trái↔phải),
1 dòng ký tự biến thể (1920 xa → xa, phân biệt với hình tượng mới năm 1872).
- Đã thêm **84 dòng**: các ô có hạt chưa được ánh xạ nhưng có thể nhìn thấy bitmap, bao gồm cả nửa chiều rộng `,゛゜#*@©▷◀▶$☆●vxqw`,
Full-width 絵博齢囮Gu Taipin Yinglongqi phi tần 撹看đào cứng tảo 沢沴洴袴恁恁恁狠 tất cả những kẻ ngốc vẫn đang nói về việc Ninh Phi sợ đổ mồ hôi và vặn rắn cần Thư Tấn Cơ 聡 đi cùng lông mày và đứng trước danh sách vùng ngoại ô và phòng trưng bày Nuojing, v.v.,
Ký tự không phổ biến: Ren(1004), 悂(1562), 歼(1318), 黩(1919), nét W(1460),
Và khối ghép 1462–1464 `真・天馬翔覇` (1462 là đúng +・, cấu trúc giống như 1888 "mảng・"; 1463 là Tian + ngựa;
Nửa bên trái của 1464 được nén Xiang, nửa bên phải được nén Ba, tương ứng với 1453 và 1166 từng phần).
- Mỗi dòng `note` bắt đầu bằng `bitmap-corrected`, `bitmap-identified` hoặc `bitmap-checked`, ghi lại giá trị gốc và bằng chứng.
- Tác động: So với hạt giống ngược dòng, kết quả giải mã của 3.908 trên 51.174 văn bản ROM là khác nhau và tổng số 5.851 cách đọc glyph là khác nhau.
(Bao gồm các ô mới và phân chia lại các khối composite); tần suất cao nhất là 457 "tàu" tại 1.081 địa điểm (lựa chọn đội tàu tiên tiến/tàu chiến khởi hành/対车ミサイル).

`FUN_8008d1d8` ghi lại **ký tự ASCII được trò chơi nhập** thay vì nội dung ô: mã `'p'`→217, `'$'`→212,
`'_'`→218, như `'('`→224, là giá trị thay thế; bản vẽ thực tế của ba ô này là `%`, `±` và `～`.

#### Thang biểu tượng (cột `form`)

Phông chữ gốc có bốn tỷ lệ và một cột `form` mới được thêm vào bảng mã để phân biệt chúng (trình tải chỉ đọc `glyph_id` và `char`,
Các cột bổ sung không ảnh hưởng đến việc giải mã):

| hình thức | gạch | số lượng | nội dung |
| --- | --- | --- | --- |
| `half` | 8×14 | 270 | Số, chữ cái Latinh, chữ hiragana, katakana, dấu câu |
| `full` | 14×14 | 1.692 | Ký tự tiếng Trung và ký hiệu có độ rộng đầy đủ |
| `compound` | 14×14 | 49 | Khối tổng hợp ép hai hoặc ba ký tự vào một lưới để kiểm soát khoảng cách |
| `icon` | 8×14 hoặc 14×14 | 9 | Biểu tượng không phải văn bản, được thay thế bằng văn bản hoặc ký hiệu |

Việc cùng một ký tự xuất hiện ở các thang âm khác nhau là điều bình thường: Katakana バ có phiên bản nén ở nửa độ rộng 187 và khối ghép 1936,
B và P có các chữ cái có độ rộng nửa 12, 26 và các biểu tượng hình tròn 242, 241. Bắn súng và lưới có các ký tự tiếng Trung có độ rộng đầy đủ 612, 622 và các biểu tượng kiểu tấn công 243, 244.
E có chữ nửa chiều rộng 15 và chữ E 259 nhỏ bên cạnh đồng hồ, ► có nửa chiều rộng 246, toàn chiều rộng 576 và thanh đánh giá 291.
Chỉ có 6 bộ lặp lại theo tỷ lệ giống nhau, tất cả đều là lặp lại đúng: Full-width Jun (710/1823), Discussion (1144/1853), Huân (1597/1826)
Đó là cùng một ký tự được vẽ hai lần trong thư viện ký tự (sự khác biệt giữa các nét chính lần lượt chỉ là 3, 1 và 26 pixel); khối tổng hợp ダブ(1944/1949),
イン) (1937/1940/1943) có các pixel giống hệt nhau, và ニン (1946/1951) đều có ニン được vẽ trên đó, nhưng có tàn tích của các ký tự liền kề khác nhau ở các cạnh.
Không có danh mục "ký tự tiếng Trung thu hẹp" riêng biệt: các ký tự có chiều rộng đầy đủ hầu như luôn có chiều rộng nét chính là 12–14 pixel.
Cái hẹp nhất chỉ là phông chữ.

Biểu tượng (`icon`): 241/242 là hình tròn Ⓟ (có sau khi di chuyển) và Ⓑ (chùm tia) ở cuối tên vũ khí, 243/244 ở trước tên vũ khí
Biểu tượng chụp và lưới, hình đại diện văn bản P/B/bắn/lưới được giữ lại vì `src/srw64_native/weapon_traits.py` dựa vào những điều này
mã thông báo là dấu hiệu vũ khí; 575 là biểu tượng vũ khí MAP; 258 (🔧) và 259 (E nhỏ) là các dấu ở cả hai bên của lưới dụng cụ;
219/291 là khoảng trống và khoảng trống đầy đủ (▷／±) của thanh xếp hạng.

#### Khối ghép

1923–1953 là các khối tổng hợp ban đầu được cắt đặc biệt để kiểm soát khoảng cách: toàn bộ chuỗi tên nước đi đặc biệt được nén và sau đó cắt thành nhiều khối ở 14 pixel.
Thường có hai hoặc ba bút danh trong một khối và thường có các bút danh xuyên suốt các ranh giới khối. Quy tắc phân đoạn: pixel kana xuyên biên giới được gán cho nét chính (chỉ số bảng 1)
Bên có số lớn hơn sẽ là quân cuối cùng nếu hoàn toàn bằng nhau; mỗi bộ kết quả ghép được so sánh với văn bản thực sự sử dụng nó.

| Nhóm | Mỗi phần nội dung | Được sử dụng cho |
| --- | --- | --- |
| 1815–1816 | パ／ーツ | t00_00517 |
| 1923–1925 | (số lượng／グレ／ート) | t00_02609, 02610 |
| 1926–1928 | (グ／レー／ト) | t00_02592, 02613 |
| 1929–1931 | （マ／ジン／ガー） | t00_02607 |
| 1932–1934 | (ミ／ネル／バ) | t00_02608 |
| 1935–1937 | (ビル／バ／イン) | t00_02600 |
| 1938–1940 | (ダ／ンバ／イン) | t00_02611 |
| 1941–1943 | (サ／ーバ／イン) | t00_02612 |
| 1944–1948 | ダブ／ルバー／ニン／グファ／イヤー | t00_02592、02607–02609 |
| 1949–1953 | ダブ／ルライト／ニン／グバ／スター | t00_02593, 02610, 02613 |

(Ngoài ra còn có văn bản menu "Lưới...P" tương ứng.) Phân đoạn 1945–1953 của hạt giống ngược dòng có bút danh.
(chẳng hạn như ーニ／ング／ファイヤー、ルラ／イト／ニング／バスター), kết quả nối là chính xác;
Hạt giống năm 1934 được viết là `バＸ）`, nhưng các ô chỉ vẽ バ, ゛ và ) và trò chơi thực sự hiển thị "(ミネルバ)",
Không có chữ X trong tên máy MireraX. Các khối ghép còn lại là các ký tự Trung Quốc được nén theo cặp: 1454–1456 锔 dance/tái hiện/江湖,
1457–1459 Trường phái/Miền Đông/Bất bại, 1462–1464 Zhen・/Tianma/Xiangba, 1886–1888 Mantuo/Rayen/Zhen・,
Ngoài ra còn có 632 khả năng, 2047–2049 (phía trước) (giữa) (phía sau).

#### Đồ họa chưa được ánh xạ

Chỉ còn lại 257 (như Д, văn bản không được sử dụng) và công cụ đo lường 260–272, được giải mã là `<G:…>`. 260–270 đều có hình dạng thanh dọc giống nhau
11 cấp độ tô màu (chỉ số bảng màu thay đổi màu theo từng dòng từ dưới lên trên, 260 trống, 270 đầy), 271/272 là phiên bản hai màu không có nét.
Chúng chỉ xuất hiện trong 46 văn bản đơn ô t00_05104–05149: tùy chọn 258 trước thanh (🔧 Sửa cờ lê),
Sau thanh, bạn có thể chọn 259 (E nhỏ), 11 cấp độ × 4 kết hợp, cộng thêm một trong số 271 và 272. Cờ lê có gợi ý và sửa chữa E,
EN có liên quan, nhưng giao diện cụ thể chưa được xác nhận bằng hoạt động.

Phông chữ gốc là HarmonyOS Sans 2.040 (các tệp và giao thức gốc trong gói chính thức của Huawei được đặt trong `content/fonts/`, giấy phép cho phép phân phối lại với phần mềm như hiện tại và không được phép phân phối hoặc sửa đổi riêng biệt; `tools/content/prepare_fonts.py` được kiểm tra bằng hàm băm và đưa vào gói ứng dụng) và phông chữ biểu tượng trong kho là `content/fonts/SRW64Symbols.ttf` và phông chữ biểu tượng nút là `content/fonts/SRW64Prompts.ttf` (Bản chuyển thể Yukari của NhắcFont của "Shinmera" Hafner, SIL OFL 1.1, được cấp phép và ghi lại trong `content/fonts/LICENSE-SRW64Prompts.txt`, được tạo bởi `tools/content/build_prompt_font.py` từ NhắcFont với Zelda64Recomp). Gói chính thức đến từ [Trang tài nguyên thiết kế dành cho nhà phát triển Huawei](https://developer.huawei.com/consumer/cn/design/resource/), bản sao cục bộ được đặt trong `assets/fonts/HarmonyOS-Sans-2.040.zip` và SHA-256 được ghi trong `content/fonts/harmonyos-sans.json`.

## Lõi Libretro

Công cụ so sánh SRAM gốc sử dụng tính năng gửi báo cáo cốt lõi `98c1b0d` tương ứng với bố cục khu vực lưu tổng hợp đánh giá mã nguồn:
[libretro_memory.h](https://github.com/libretro/mupen64plus-libretro-nx/blob/98c1b0d/libretro/libretro_memory.h)
và [sram.c](https://github.com/libretro/mupen64plus-libretro-nx/blob/98c1b0d/mupen64plus-core/src/device/cart/sram.c).
Bản sao cục bộ được đặt tại `build/recomp/reference-sram-source/` và SHA-256 của hai tệp là
`4d89673af5424d31b391e6afcdaeaaca9fcf73d062637d32c9090906a428582e`
và `609e1b94dd03384128c579abf0a90faeefea8c1f8a095f65a80a7cd68bdbe0fb`.
Công cụ này cũng khóa toàn bộ SHA-256 và kích thước lưu tổng hợp thời gian chạy của các lõi được chấp nhận được liệt kê bên dưới, trước và sau khi nhập
Xác minh rằng các byte không phải SRAM không thay đổi. Việc xem xét mã nguồn và kết quả đọc tệp thực tế của trình mô phỏng tham chiếu được lưu giữ riêng biệt.

- Cốt lõi: Mupen64Plus-Next arm64;
- Ngày mua lại: 02/08/2026;
- Nguồn: `https://buildbot.libretro.com/nightly/apple/osx/arm64/latest/mupen64plus_next_libretro.dylib.zip`;
- dylib SHA-256:
`8cd7541261b06b89c18189d7621b825e4e6f906b64f4449056a40d0647a6f58d`;
- Vị trí địa phương: `build/libretro/cores/mupen64plus_next_libretro.dylib`.

Địa chỉ `latest` sẽ trôi đi; mọi giá trị băm khác phải được xác nhận lại dưới dạng môi trường thời gian chạy mới và không thể kế thừa
Ảnh chụp màn hình hiện tại hoặc kết luận được lưu trữ.

## Biên dịch lại các công cụ và thời gian chạy tham chiếu

Đầu vào đã sửa lỗi xem `config/recomp/toolchain.json` và `config/recomp/requirements.lock`,
Bản sao nguồn, mã được tạo và tệp nhị phân được đặt trong `build/recomp/` bị bỏ qua.

| Đầu vào | Đã sửa lỗi cam kết/phiên bản | Mức sử dụng hiện tại |
| --- | --- | --- |
| [N64Recomp / RSPRecomp](https://github.com/N64Recomp/N64Recomp) | `ffb39cdad1da5de07eaaa48bd1db4a89a7986771` | Tạo mã CPU và RSP MIPS; phụ thuộc đệ quy được cố định bởi cam kết cha mẹ |
| [n64sym](https://github.com/shygoo/n64sym) | `ccf4600f3389f1a84bde23339225cf372fdf7712` | ứng cử viên chữ ký libultra; không được coi trực tiếp là một ràng buộc hệ thống được xác nhận. Đầu ra của ROM này (`n64sym rom.z64 -s -f splat`) được lưu trữ dưới dạng `config/recomp/n64sym-symbols.txt` và bản dựng không còn được tạo tại chỗ |
| [N64ModernRuntime](https://github.com/N64Recomp/N64ModernRuntime) | `cdf5abbd5026fef5c364c676e4667c45e42b6863` | Một thư viện thời gian chạy tĩnh hoàn chỉnh đã được xây dựng, kết nối với máy chủ chẩn đoán CPU và tác vụ âm thanh RSP |
| [stimdisasm](https://github.com/Decompollaborate/stimdisasm) | `1.42.4` | Phân đoạn tháo gỡ và ứng cử viên chức năng |
| [splat](https://github.com/ethteck/splat) | `splat64==0.50.0` | Công cụ phân đoạn đã được chuẩn bị sẵn, quá trình quét hiện tại không dựa vào việc xuất của nó |
| [RT64](https://github.com/rt64/rt64) | `43373749dac9bbc1b653e6a02aed40a9e1783bed` | Kết xuất kim loại thực tế và đọc lại bộ đệm khung GPU; phụ thuộc đệ quy được cố định bởi cam kết cha mẹ |
| [Zelda64Recomp](https://github.com/Zelda64Recomp/Zelda64Recomp) | `1a9c26613c6e0906140dc8bcca7362cbe00bf1eb` | Đọc mã nguồn tham khảo về cách sử dụng cửa sổ máy chủ và giao diện RT64 |

Mô-đun con N64Recomp của N64ModernRuntime là
`81213c1831fab2521a6a5459c67b63437d67e253`, các phần phụ thuộc đệ quy đã được khởi tạo và biên dịch.
Phiên bản này được kiểm tra từng byte trước khi máy chủ được xây dựng giống với `recomp.h` của trình tạo độc lập để xác minh ngữ cảnh và
Giao diện của người trợ giúp; điều này không có nghĩa là tất cả giao diện bên trong của hai bài nộp đều giống nhau.
Trạng thái `compiled` của bootstrap có nghĩa là công cụ phân tích đã được biên dịch chứ không phải máy chủ trò chơi đã được biên dịch.

Các phần phụ thuộc đồ họa được `tools/recomp/toolchain/prepare_rt64.py` chuẩn bị riêng. Mô-đun con Plume được cố định trong
`d890ac899e505fb30040e037a4037cdeca68f033`. Máy hiện tại chỉ có Công cụ dòng lệnh,
Không có trình biên dịch Metal ngoại tuyến; thử nghiệm sử dụng tính năng nhúng mã nguồn MSL tùy chọn, thông qua thời gian chạy Metal
Giao diện biên dịch mã nguồn tải cùng một đầu ra SPIRV-Cross. Trình đổ bóng nội bộ ban đầu của chương trình phụ trợ cũng sử dụng giao diện này.
Hai bản điều chỉnh mã nguồn nằm trong các bản sao bị bỏ qua và mỗi bản chuẩn bị sẽ kiểm tra nội dung gốc, các cam kết cố định và phạm vi thay đổi,
Ghi `build/recomp/graphics-source-patches.json`; kho lưu kịch bản chuyển thể. của Plume
`CocoaWindow` cung cấp khối đọc kích thước cửa sổ từ luồng hiển thị đến hàng đợi chính và khối ban đầu sẽ chụp trực tiếp khối đó
`this`; Giải phóng chuỗi trao đổi trong luồng đồ họa khi RT64 kết thúc và chạy lại `Cocoa_VideoQuit` của SDL khi thoát
Trong vòng lặp chính, khối dư đọc đối tượng được giải phóng và gặp sự cố (xảy ra khi thoát sau khi điều chỉnh kích thước cửa sổ). vá hãy
Khối chia sẻ một dấu hiệu sinh tồn và quay trở lại ngay sau khi cửa sổ bị phá hủy. Cũng trong dự án này
CMake thêm tệp tiêu đề khai báo `labs` cho phiên bản hlsl++ cố định.

Hình ảnh GPU được máy chủ tạo ra bằng cách sử dụng hook vẽ của RT64, các lệnh gọi lại hoàn thành và kết cấu kim loại
Đọc lại và viết ra mà không cần dựa vào quyền chụp ảnh màn hình của hệ thống. Đầu ra thể hiện kết quả GPU thực tế và vẫn phải được kiểm tra tính chính xác
Các cảnh tương ứng và thiết bị đầu cuối tham chiếu không thể được suy ra từ sự tồn tại của các hình ảnh mà toàn bộ bộ trò chơi đã vượt qua.

Tài liệu tham khảo ares v148 có thể thực thi được tại `/Applications/ares.app/Contents/MacOS/ares`,
Lần này SHA-256 là
`7a49f00f96a691458461d7c9cf453d95c0f5c054389bbd87c253987b8b6fa345`.
Ghi lại thời gian chạy ghi lại đồng thời các nhận dạng ROM, are, phiên và bộ nhớ. Xem kết quả và ranh giới của họ
[recomp-progress.md](../design/recomp-progress.md).

## Phần phụ thuộc của giao diện người dùng được chia sẻ (2026-09-20)

Giao diện người dùng trò chơi mặc định và nguyên mẫu trang tên tùy chọn sử dụng [RecompFrontend](https://github.com/N64Recomp/RecompFrontend)
Cam kết `b1a1477c6556aeb7ed45defbfb5924f721efebc1`, trong đó mô-đun con RmlUi được cố định thành
`7a06f27db04fe5d13a5dacc19b2b4544673a4eca`. chế độ xem khóa độc lập
`config/recomp/frontend.json`, để biết phạm vi triển khai và xác minh, hãy xem [Giao diện trò chơi dùng chung](../native/shared-game-ui.md) và [Nguyên mẫu trang tên](../native/shared-name-page-probe.md).
Chỉ sử dụng lại trình kết xuất giao diện người dùng và RmlUi của nó, đồng thời ghi lại SHA-256 của tệp tiêu đề thích ứng và trình kết xuất kết xuất ban đầu khi chuẩn bị;
Không cập nhật RT64/N64ModernRuntime hiện có, không gửi mã nguồn phụ thuộc, phông chữ hoặc tạo trình đổ bóng.
Runtime FreeType xuất phát từ môi trường phát triển; đây không phải là bản phát hành có danh sách cấp phép phông chữ/phụ thuộc đầy đủ.