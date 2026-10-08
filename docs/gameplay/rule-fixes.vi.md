> **Ngôn ngữ / Language:** [Tiếng Việt](rule-fixes.vi.md) · [English](rule-fixes.en.md) · [中文](rule-fixes.md)

# Quy tắc tùy chọn: sửa chữa và điều chỉnh độ khó

Ngày: 17-09-2026 (2026-09-18 thêm tính năng chuyển đổi thời gian thực vào thanh menu, bật danh mục chỉnh sửa theo mặc định trong bản dùng thử, thêm các điều chỉnh độ khó cho hình đại diện của trùm và giới hạn biến đổi trên, thêm sức mạnh của vũ khí của Holy Warrior Aura và thêm tiền hoàn lại khi rời khỏi đội). BUG01–04 và BUG08 tương ứng với [Đăng ký lỗi gốc](original-bug-register.md); BUG05 (Năm cơ thể giả bay) đã được đặt là [Sửa chữa cơ bản](base-fixes.md) có hiệu lực theo mặc định và không có công tắc cũng như không có trên trang này. Tổng cộng có bảy công tắc độc lập đã được sửa chữa (sự kế thừa vũ khí của BUG08 chưa được xác minh trong thời gian thực) và cũng có một số điều chỉnh độ khó (xem bảng §1); **Khi lối vào dùng thử được khởi chạy lần đầu tiên, tất cả các chỉnh sửa sẽ được bật và các điều chỉnh độ khó sẽ bị tắt theo mặc định**. Khi tắt bất kỳ chức năng nào, máy chủ chỉ gọi chức năng gốc và hoạt động phù hợp với phiên bản gốc.

## 1. Sử dụng

Mặc định: `scripts/Play SRW64 Native.command` Khi bắt đầu lần đầu tiên, **Tính năng chỉnh sửa được bật hoàn toàn và tính năng điều chỉnh độ khó bị tắt hoàn toàn**. Có hai lối vào khi trò chơi đang chạy. Họ chia sẻ các cài đặt giống nhau và đồng bộ hóa với nhau trong thời gian thực:

- Thanh menu **"Tùy chọn → Điều chỉnh lối chơi"**: "Sửa đổi" và "Điều chỉnh độ khó" hai bộ tùy chọn kiểm tra (tên nhóm là tiêu đề không thể nhấp vào), bên dưới là ba mặc định là "Khôi phục mặc định (Bật sửa đổi, Tắt độ khó)", "Tắt tất cả (Quy tắc gốc)" và "Bật tất cả".
- **"Tùy chọn → Cài đặt..." (⌘,)**: Cửa sổ cài đặt, bao gồm các công tắc quy tắc giống nhau và ba cài đặt trước, cũng như ngôn ngữ (ja/zh-Hans/en) và màn hình (Bản gốc/HD). Trò chơi không thể nhận dữ liệu nhập từ bàn phím khi cửa sổ đang mở và sẽ không tiếp tục cho đến khi tất cả các phím được nhả sau khi đóng.

Các thay đổi có hiệu lực ngay lập tức và cài đặt được ghi lại. Tiêu đề của menu và cửa sổ tuân theo ngôn ngữ hiện tại và ngôn ngữ mới sẽ được sử dụng ngay sau F7 hoặc chuyển đổi ngôn ngữ trong cửa sổ.

Bạn cũng có thể chọn khi khởi động:

```sh
./Play\ SRW64\ Native.command --rules fixed          # 全部修正（难度调整仍关闭）
./Play\ SRW64\ Native.command --rules all            # 修正 + 难度调整
./Play\ SRW64\ Native.command --rules original       # 原版规则
./Play\ SRW64\ Native.command --rule-fixes esp-level,limit-cap   # 自选
./Play\ SRW64\ Native.command --rule-fixes ''        # 自选为空，等同 original
```

| ID | Nội dung |
| --- | --- |
| `esp-level` | Hiệu chỉnh đòn đánh/né siêu năng lực dựa trên cấp độ kỹ năng, phiên bản gốc được cố định ở mức 64 |
| `seisenshi-level` | Chỉnh sửa né tránh của chiến binh thánh dựa trên cấp độ kỹ năng, phiên bản gốc được cố định ở mức 32 |
| `limit-cap` | Tổng số lần va chạm/tránh của người lái xe và khả năng di chuyển của cơ thể không vượt quá giới hạn của cơ thể. Phiên bản gốc không có giới hạn |
| `potential-bands` | Sức mạnh cơ bản được căn chỉnh theo cấp độ HP: không có phần thưởng trên 90% và đạt mức cao nhất khi dưới 10%; phiên bản gốc đi trước một bậc so với kế hoạch |
| `potential-half` | Hiệu chỉnh đòn đánh/tránh cơ bản giảm một nửa và tỷ lệ trúng đòn chí mạng không đổi |
| `weapon-inherit-map` | Ba vũ khí còn thiếu đã được thêm vào di sản khi thay đổi cỗ máy: bộ phát lửa của レイズナー và グレネードランチャー, アルトロンドラゴンファイヤー (vì lý do và cơ sở, vui lòng xem [Phân tích kế thừa chuyển đổi](upgrade-inheritance.md); nó chưa được xác minh trên máy thực tế) |
| `aura-slash-power` | Holy Warrior: Vũ khí dòng ハイパーオーラ được mở khóa ở L3 tăng sức mạnh thêm +200...+1500 theo cấp độ kỹ năng (phiên bản gốc hoàn toàn bị thiếu), xem §2.2 |

Sáu mục trên là **Chỉnh sửa**: mã gốc không nhất quán với dữ liệu hoặc giao diện của chính nó, nó được bật theo mặc định, `--rules fixed` đề cập đến sáu mục này. `weapon-inherit-map` khác với năm mục còn lại. Nó ghi số phân đoạn vào danh sách tại thời điểm thay đổi máy. Đó là một trạng thái liên tục: việc tắt công tắc sẽ không bị rút lại và việc bật nó lên sẽ không bù đắp cho thay đổi đã xảy ra trước đó. Bốn mục sau đây là **Điều chỉnh độ khó**: Bản thân hành vi ban đầu là bình thường, nó chỉ cho phép người chơi lựa chọn sức mạnh. Nó được tắt theo mặc định. Để bật tính năng này, bạn cần `--rules all` hoặc chỉ định từng mục.

| ID | Nội dung |
| --- | --- |
| `boss-dummy-half` | Số lần cải trang trùm giảm một nửa, giữ ít nhất 1 |
| `boss-dummy-none` | Ông chủ không còn thân giả nữa; khi được kiểm tra cùng lúc với việc giảm một nửa, mục này sẽ được ưu tiên |
| `upgrade-cap-break` | Đột phá giới hạn trên của sửa đổi: Tất cả máy bay trong màn hình sửa đổi có thể được thay đổi thành 15 giai đoạn (tác phẩm gốc dựa trên máy bay 6 đến 15) và thang đo sử dụng ●/☆ để đánh dấu các lưới vượt quá giới hạn trên của tác phẩm gốc; Thay đổi thiết bị EW, vũ khí bổ sung sau khi sửa đổi hoàn toàn và giá bán vẫn dựa trên giới hạn trên của tác phẩm gốc. Số phân đoạn đã thay đổi là trạng thái liên tục và sẽ được giữ lại sau khi tắt máy nhưng không thể thay đổi lại. Để biết chi tiết, hãy xem Phần 7 của [Giai đoạn sửa đổi và giới hạn trên](upgrade-limits.md). Trên cùng một trang, có tệp quy tắc nâng cấp (`--upgrade-rules`) có thể thay đổi mức tăng, giá, giới hạn trên và loại vũ khí của từng giai đoạn. |
| `upgrade-refund` | Hoàn tiền sau khi rời đội: Khi cốt truyện khiến máy bay rời quân đội (rời đội, xóa máy bay cũ sau khi chuyển giao hoặc sáp nhập máy bay), số tiền sửa đổi của người chơi đã chi cho máy bay sẽ được hoàn trả theo giá hiện tại và một lời nhắc sẽ hiển thị ở đầu màn hình và trong phần xem lại đoạn hội thoại; số chặng được máy bay thay thế kế thừa và số chặng do lô đất tặng bằng cách sử dụng `3D6C` sẽ không được hoàn trả. Xem §2.6 |
| `parts-carry-over` | Linh kiện đi cùng bạn: Khi đổi máy, hãy lắp trực tiếp các bộ phận nâng cao đã lắp ở thân máy cũ lên thân máy mới (bản gốc sẽ được dỡ về kho và phải chờ đợt đại tu tiếp theo mới lắp lại); nếu thân mới không còn đủ khe thì các bộ phận thừa vẫn sẽ được để lại trong kho. Xem §2.7 |

- Chọn `rules.json` được ghi trong thư mục dùng thử (mục hồ sơ hợp nhất là `build/recomp/profile-play/rules.json`, lược đồ `srw64.rule-settings.v1`) và nó sẽ được sử dụng khi bắt đầu mà không có tham số. **Nếu không có tệp đó, hãy mở nó theo mặc định**; danh sách trống trong tệp có nghĩa là các quy tắc ban đầu đã được chọn rõ ràng và sẽ không bị coi là "không được chọn". Thiết bị đầu cuối in các quy tắc hiện tại khi khởi động.
- Máy chủ chẩn đoán/thăm dò không có cửa sổ không rời khỏi trình khởi chạy: không có `SRW64_RULE_FIXES` khi chạy trực tiếp `run_host_probe.py`, đây là quy tắc ban đầu, đảm bảo rằng bằng chứng về hoạt động bị chặn có thể được sao chép.
- Các thay đổi trong menu ngay lập tức được ghi vào cùng `rules.json` và `rule-fixes-events.jsonl` (lược đồ `srw64.rule-fixes-change.v1`, bao gồm VI) được thêm vào thư mục đang chạy. Báo cáo đang chạy là `rule_fix_changes`.
- Việc chuyển đổi sẽ có hiệu lực ở **lần quyết định tiếp theo**: trận chiến đã tính tỷ lệ trúng đích sẽ không bị ảnh hưởng và việc chuyển đổi trong quá trình thực hiện trận chiến sẽ không làm thay đổi kết quả của lần này.
- Việc sửa chỉ thay đổi giá trị đọc trong quá trình giải quyết, không ghi vào kho lưu trữ, cũng không thay đổi định dạng lưu trữ. Bạn có thể trực tiếp thay đổi các quy tắc để tiếp tục nếu bạn đã tiến bộ. `report.json` của mỗi phiên ghi lại `rule_fixes` (`rules_version` với các mục đã bật), máy chủ ghi một `rule-fixes.json` khác và in `SRW64_RULE_FIXES` vào nhật ký. Khi tiếp tục lưu từ một phiên, trình khởi chạy sẽ nhắc xem lần trước nó có được phát theo các quy tắc khác hay không. Đóng băng bản sao lưu ban đầu và các phiên trước chức năng này được tính theo quy tắc ban đầu.
- Trang cài đặt chỉ xuất hiện ở các máy có giao diện (áp dụng "Settings..." trên thanh menu hoặc Ctrl/Cmd+, mở trang RmlUi). Máy chủ chẩn đoán không có cửa sổ vẫn chỉ sử dụng các tham số khởi động.
- Việc sửa lỗi cũng có hiệu quả cho cả địch và ta, đồng thời phù hợp với cách gọi của mã gốc: siêu năng lực của địch, chiến binh thần thánh và phi công năng lượng thấp cũng được tính theo quy định mới.
- Công tắc cơ bản là biến môi trường `SRW64_RULE_FIXES=<逗号分隔的 ID>`; `run_host_probe.py` sẽ xác minh ID và ID không xác định sẽ trực tiếp khiến quá trình khởi động bị lỗi.

## 2. Mã gốc và các chỉnh sửa

Tất cả các địa chỉ đều nằm trong lớp phủ chiến thuật `load_000AB160` (VRAM `801C2600` trở đi, ROM `0xAB160` trở đi).

### 2.1 Tỷ lệ trúng thực tế

Các công thức `801F4384` (thực chiến, kết quả ghi lại vào bảng chiến đấu `8018B6E8` cho từng mục `+0x12`) và `80204254` (ước tính khi chọn mục tiêu và vũ khí, được gọi bởi `80201D98`, `80204564`, `8020500C`) giống nhau:

```
(命中a + 反应a + 武器命中补正 + 100 + 运动性a) − (回避d + 反应d + 运动性d)
  × 地形补正 × 机体尺寸补正
  ± 集中类状态 30
  + NT/强化(a) − NT/强化(d)          801E1EDC，表 80218080，L1–L9 为 10,14,18,21,24,26,28,29,30
  + 底力(a) − 底力(d)                801E1D64
  − 圣战士(d)                        801E1F08（只有防守方的调用）
  + 超能力(a) − 超能力(d)            801E1F10
  → 之后才处理两种减半条件；80204254 另外把负值钳到 0
```

Kỷ lục chạy của người lái xe (kích thước bước 0x4C): `+05` cấp độ, `+06` cấp độ kỹ năng đặc biệt (chia sẻ với NT, thế giới con người nâng cao, sức mạnh cơ bản, chiến binh thánh thiện, siêu năng lực), `+26` né tránh, `+28` đánh, `+2A` phản ứng, `+2C` Kỹ năng, `+36` dấu kỹ năng (`04` sức mạnh cơ bản, `08` NT, `10` củng cố thế giới, `20` chiến binh thánh thiện, `40` siêu năng lực). Bản ghi hoạt động của cơ thể (kích thước bước 0x54): `+04/+06` HP và HP tối đa, `+10` khả năng di chuyển, giới hạn `+14`.

### 2.2 Siêu năng lực, thánh chiến binh: hàm trống (`esp-level`, `seisenshi-level`)

Phần thân hàm của `801E1F08` và `801E1F10` chỉ có `jr $ra; nop` và `$v0` không được viết. `andi v0, v0, 0x20` (hoặc `0x40`) vừa được thực thi trước cuộc gọi, vì vậy "sự sửa đổi" mà người gọi nhận được chính là dấu kỹ năng:

- Siêu năng lực: Đánh +64 khi tấn công, địch đánh −64 khi tấn công;
- Thánh Chiến Binh: Chỉ khiến địch đánh -32 khi tấn công, và không có hiệu chỉnh khi tấn công;
- Cả hai chỉ xét cờ chứ không xét cấp độ. Nó cũng có hiệu lực khi cấp độ kỹ năng là 0. Ví dụ: nếu Garuri ở phía trước người lái xe Lv7, còn Hazel và Black Knight ở phía trước Lv6, trang trạng thái sẽ không hiển thị chiến binh thánh nhưng vẫn có −32.

Sau khi sửa, hai chức năng được thay đổi để kiểm tra bảng cấp NT theo `+06` (`801E1EDC` sử dụng `80218080`), tức là L1–L9 là 10…30 và L0 là 0. Vị trí gọi không thay đổi: siêu năng lực vẫn ở cả hai bên tấn công và phòng thủ, còn thánh chiến binh vẫn chỉ ở bên phòng thủ.

Cơ sở chọn bảng này: hàng trúng và hàng tránh của bảng NT giống nhau; ba hàng của bảng `802180B4` ngay sau đó mà không có bất kỳ tham chiếu mã nào có cùng một đường cong ở hai hàng đầu tiên và hàng thứ ba 0,20,40…150 chính xác bằng một phần mười của bảng rào cản Aura `80218930` (0,200…1500), giống như dữ liệu không được kết nối sau khi chuẩn bị cho các chiến binh thánh thiện. Không còn bằng chứng trực tiếp nào về các giá trị số mà tác phẩm gốc dự định.

**Đã sửa và bổ sung vào ngày 18-09-2026 (`aura-slash-power`). ** Vật phẩm còn thiếu được đề cập trong dữ liệu: Các chiến binh thánh nên tăng sức mạnh của vũ khí Aura như **Kiếm của Hurra**, và siêu năng lực nên tăng sức tấn công của tất cả các loại vũ khí. Chỉ có 5 nơi cờ Thánh chiến binh được kiểm tra trong toàn bộ ROM (hai điều kiện mở khóa vũ khí, hai tỷ lệ trúng đích và Ora Barrier), và chỉ có 4 nơi cờ siêu năng lực được kiểm tra trong chức năng tỷ lệ trúng đích; cả thiệt hại chiến đấu thực tế `801F5628` cũng như ước tính thiệt hại AI `80203418` đều không đọc cờ kỹ năng của người lái xe (`tests/test_rule_fixes.py` được xác nhận bằng byte). Vì vậy **hai phần thưởng sức mạnh tấn công hoàn toàn không tồn tại trong mã gốc**, đó không phải là lỗi số.

Cơ sở giá trị: ゲームカタログ@Wiki trích dẫn "バグがなかった dịp, đòn đánh của L9, né tránh +30, sức tấn công +1500". Các hàng dữ liệu chưa đọc ở phía sau bảng NT trong ROM tương ứng chính xác với:

| Hàng bảng | L0–L9 | Thư từ |
| --- | --- | --- |
| `80218080` dòng 0–2, `802180B4` dòng 0–1 | 0,10,14,18,21,24,26,28,29,30 | Đánh/Tránh, L9 = +30 |
| `8021809E`, `802180C8` | 0,20,40,60,80,100,120,130,140,150 | ×10 = Sức tấn công +200…+1500, L9 = +1500 |
| `802180A8` | 0,20,30,40,50,60,70,80,90,100 | ×10 = +200…+1000, phù hợp với giá trị rào cản của phốt dẫn hướng |

`aura-slash-power` Trong thời gian gọi `801F5628` và `80203418`, sức mạnh vũ khí của kẻ tấn công (bản ghi hoạt động vũ khí `+0x06`, cùng đơn vị với màn hình giao diện) tạm thời được thêm vào `802180C8`[cấp độ kỹ năng]×10 và được khôi phục sau cuộc gọi. Chỉ ảnh hưởng đến **tình trạng vũ khí 15** được sử dụng bởi **Phi công Jihadi** (yêu cầu Holy Warrior L3) Vũ khí: Hazel, Hazel , ハイパーオーラショットアーム, ツインオーラアタック, tổng cộng 20 hồ sơ vũ khí; không được thêm vào オーラzanり thông thường (điều kiện 14). Bản thân điều kiện 15 yêu cầu L3, vì vậy phần thưởng thực tế là L3 +600 đến L9 +1500. Số sức mạnh vũ khí trên giao diện không thay đổi và phần thưởng được phản ánh trong phần xem trước và giải quyết trận chiến.

Phần thưởng sức mạnh tấn công bằng tất cả vũ khí của siêu năng lực cũng bị thiếu, có thể được bù đắp bằng cách sử dụng cùng một đường cong. **Người dùng không yêu cầu và không có công tắc nào được thêm vào vòng này**.

Aura Barrier: Giá trị thực tế được sử dụng trong trò chơi là +200...+1500 (`80218930`, là đường cong sức tấn công) và sách hướng dẫn in +200...+1000 (hàng cuối cùng trong bảng trên). Người dùng quyết định **giữ phiên bản gốc**. Sẽ được coi là sách hướng dẫn không chính xác và sẽ không có sự chuyển đổi nào được thực hiện.

Cấp độ Holy Warrior trong phiên bản gốc cũng ảnh hưởng: điều kiện vũ khí 14/15 (`801E6214`) yêu cầu L1/L3 tương ứng; Giá trị rào cản hào quang là 3000 + `80218930`[cấp] (`801F6EE0`).

### 2.3 Giới hạn: quyết toán không được đọc (`limit-cap`)

Trang trạng thái của người lái xe (`801E6C5C`, `801E7174`/`801E71C8`) hiển thị việc tránh và va chạm dưới dạng `%3d+%3d` (giá trị thí điểm + chuyển động của cơ thể) và vẽ các màu cảnh báo khi vượt quá giới hạn. Tuy nhiên, công thức truy cập ở trên được thêm trực tiếp và ROM đầy đủ chỉ đọc các trường giới hạn để hiển thị, tải bản sao, sửa đổi và bổ sung thành phần (`800A5254`, mỗi phân đoạn sửa đổi giới hạn +10/+20) và phần thưởng chế độ đặc biệt (`801FE9CC`, v.v.). Ở phiên bản gốc, giới hạn sửa đổi và giới hạn trang bị không có tác dụng gì trong chiến đấu.

Sau khi điều chỉnh, trong khi gọi hai chức năng tấn công, "đòn đánh + khả năng cơ động" của kẻ tấn công và "né tránh + khả năng di chuyển" của người phòng thủ đều không vượt quá giới hạn của máy bay đang bay và phản ứng không được đưa vào giới hạn trên, phù hợp với tầm cỡ so sánh trên trang trạng thái. Phương pháp thực hiện là tạm thời giảm hai trường này trong quá trình gọi hàm ban đầu (đầu tiên giảm giá trị trình điều khiển để không vượt quá giới hạn, sau đó để độ linh động bổ sung cho giới hạn), sau đó khôi phục nó về trạng thái ban đầu sau lệnh gọi, và phần còn lại của công thức ban đầu vẫn hoàn toàn không thay đổi.

Lưu ý: Giới hạn của hầu hết các thiết bị di động cao hơn 100 so với độ cơ động, nhưng rất dễ bị vượt qua bởi các robot cấp thấp (chẳng hạn như Mitsubishi: khả năng di chuyển 95, giới hạn 140) hoặc phi công cấp cao và khả năng trúng/né của các kết hợp này sẽ giảm đáng kể khi bật.

### 2.4 Lực đáy: Bánh răng tiến lên một bánh, ba công dụng có cùng giá trị (`potential-bands`, `potential-half`)

`801E1D64(用途, 驾驶员, 机体)` Kiểm tra bảng 10×10 của `80217F90`: hàng là cấp độ kỹ năng, cột là cấp HP, hàng L và cột c là max(0, c+L−9)×10, L9 là cao nhất 90. Cấp trang bị được xác định theo HP/HP tối đa×100:

| HP | Thiết bị gốc | Thiết bị sửa chữa |
| --- | ---: | ---: |
| Hơn 90% | 1 | 0 |
| 80–90% | 2 | 1 |
| … | … | … |
| 20–30% | 8 | 7 |
| 10–20% | 9 | 8 |
| Dưới 10% | 9 | 9 |

Lần so sánh đầu tiên với phiên bản gốc ghi hơn 90% là bánh răng 1 và cột 0 không bao giờ đọc được nên L9 có +10 máu đầy đủ và giá trị cao nhất xảy ra khi HP dưới 20%. Cả 2 tài liệu (S-RPG navi, Akurasu) đều ghi mức HP cao nhất dưới 10%, và cột 0 của bảng đều là 0, tương ứng với “hết máu đầy đủ, không có thưởng” nên đánh giá là còn thiếu một phần bù. `potential-bands` thay vào đó sử dụng các bánh răng ở cột bên phải (so sánh vẫn sử dụng thao tác có độ chính xác tương tự).

Ba điểm gọi lần lượt vượt qua trong các lần sử dụng 2 (đòn tấn công của kẻ tấn công), 1 (người phòng thủ tránh) và 0 (tỷ lệ chí mạng, chỉ được gọi khi đội của chúng ta tấn công và đòn chí mạng của kẻ địch được chia cho 4), nhưng tham số này được ghi đè vào một địa chỉ bảng ở đầu hàm và ba lần sử dụng có cùng giá trị. Cả hai nguồn đều nói rằng hiệu chỉnh đánh/né đòn của sức mạnh cơ bản là "cao hơn so với bản gốc", trong đó Akurasu cho biết là gấp đôi. `potential-half` Giảm một nửa kết quả của lần sử dụng 1 và 2, giữ nguyên tỷ lệ trúng đòn chí mạng. **Mục này chỉ dựa trên dữ liệu cộng đồng và các thông số không được sử dụng và bằng chứng yếu hơn các mục khác**; các con số cụ thể do dữ liệu đưa ra ("L9, HP dưới 10% phải là +50, +100 thực tế") không khớp với giá trị tối đa của mã là 90.

### 2,5 Số lần cải trang trùm (`boss-dummy-half`, `boss-dummy-none`)

Mục này không phải là một bản sửa lỗi. Bản thân cơ chế ban đầu là bình thường: khi bit 14 của từ hành vi của bản ghi triển khai (28 byte) `+0x16` được đặt và trại không phải của chúng tôi, `8020ABB4` ghi `+0x18` vào `+0x14` của bản ghi trình điều khiển mới. Trong khi chiến đấu, `801F6E3C` được sử dụng. Phán quyết, `801FCA78`/`801FE068` được tiêu thụ từng cái một và thời gian còn lại không được hiển thị trong trò chơi. Phiên bản gốc tổng cộng 42 Các bản ghi có bit này đều thuộc về ハマーン, シャア, シロッコ, グレミー, ミリアルド, ギュネイ, ガトー,ル・カイン và giá trị 2, 3, 5, 7. Để biết mô tả đầy đủ về các trường và phán đoán, hãy xem [Sửa chữa cơ bản](base-fixes.md) (vấn đề liên quan đến số lần Wufei bị viết nhầm, không liên quan gì đến mục này).

Phương pháp sửa là viết lại `+0x18` trong khi `8020ABB4` đang xử lý **bản ghi này** và khôi phục nó về trạng thái ban đầu sau khi cuộc gọi hoàn tất:

| Nội quy | 2 | 3 | 5 | 7 |
| --- | ---: | ---: | ---: | ---: |
| Bản gốc | 2 | 3 | 5 | 7 |
| `boss-dummy-half` | 1 | 1 | 2 | 3 |
| `boss-dummy-none` | 0 | 0 | 0 | 0 |

Sau khi chia đôi và làm tròn, hãy giữ ít nhất 1 lần để cơ chế vẫn xuất hiện; khi cả hai được kích hoạt cùng lúc, việc hủy bỏ sẽ được áp dụng. Việc ghi lại chỉ áp dụng cho bản ghi triển khai của **bản sao cấp độ này** được ghi trong `80199400`. Không có ROM hoặc kho lưu trữ nào được ghi. Việc chuyển đổi quy tắc sau khi xuất hiện sẽ không thay đổi số lượng đơn vị còn lại đã có - lần tiếp theo chúng xuất hiện, chúng sẽ được tạo theo quy tắc mới. Các hồ sơ không có danh tính giả (ví dụ: hai hồ sơ khi Wu Fei thù địch) sẽ không bị ảnh hưởng chút nào.

### 2.6 Hoàn tiền sau khi rời đội (`upgrade-refund`)

Kịch bản gốc sử dụng `3D5A …,4000` (hoặc 3000) để xóa máy bay đã rời đội, xóa máy bay cũ khi chuyển giao và xóa ゴッドマーズ khi ゴッドマーズ hợp nhất; phiên bản máy bay biến mất cùng với tất cả các sửa đổi và số tiền mà người chơi đầu tư cũng không còn nữa. [Phân tích kế thừa chuyển đổi](upgrade-inheritance.md) Phần 6, 8.3 liệt kê "tổn thất chuyển đổi" thuộc danh mục này. Trong mục này, trước khi xảy ra việc xóa, việc sửa đổi thân máy này sẽ được hoàn trả theo giá hiện tại và sức mạnh của bất kỳ thân máy nào sẽ không bị thay đổi.

**Khi nào nên thoát**: Chỉ xóa trong quy trình cốt truyện. Máy chủ bao gồm bốn chức năng:

| chức năng | vai trò | bao bì |
| --- | --- | --- |
| `800AA464` | Phi công rời khỏi body và xóa instance có số bằng tham số (`3D5A` chế độ 3000/4000 được gọi bởi `800A3540`; xóa máy cũ do script đưa ra khi đăng ký máy mới) | Đánh dấu phạm vi "xóa cốt truyện" |
| `800AB808` | `3D6A` Chế độ 3, ゴッドマーズxóa kết hợpガイヤー | Đánh dấu phạm vi "kết hợp" |
| `800AAD28` | Đăng ký máy mới; Bước 4: Lấy phiên bản hoạt động đầu tiên tương ứng với bảng tiền nhiệm (`D_800CA3A0`, thông qua `800AA814`) và lưu số phân đoạn của nó | Trước tiên hãy tìm trường hợp này theo các quy tắc tương tự và ghi nó là "được kế thừa" |
| `800AA3C4` | Giải phóng phiên bản nội dung (tất cả thao tác xóa đều được thực hiện tại đây) | Trong phạm vi trên, máy chủ giải quyết theo bảng, sau đó gọi hàm ban đầu |

Giảm giá (màn hình bán hàng `801C3678`, đi kèm giá bán bao gồm sửa đổi) và xóa trên bản đồ chiến thuật (`800A7DEC`) cũng gọi `800AA3C4`, nhưng không nằm trong các phạm vi này và không được hoàn lại tiền. Chỉ nhóm phiên bản của chúng tôi (140 đơn vị từ `8016A210`, nhóm 0 với bộ cấp phát `800A6E68`) mới được xử lý, các phiên bản từ các nhóm khác sẽ không được hoàn lại tiền.

**Hoàn lại bao nhiêu**: Năm mặt hàng dựa trên bảng giá tương ứng và vũ khí dựa trên bảng giá của loại sửa đổi (ví dụ `+0x15`, loại 0 không thể sửa đổi và không được tính) và đơn giá là 0...số phân khúc hiện tại −1 được cộng lại; giá được lấy từ bảng hiện có hiệu lực nên khi bao gồm `--upgrade-rules`, giá này sẽ dựa trên giá của tệp quy tắc. Phần không hoàn lại:

- **Phiên bản kế thừa**: Các phân đoạn của phiên bản tiền nhiệm đã được chuyển sang máy mới khi thay đổi thiết bị (chẳng hạn như サンドロック→Thay đổi) và việc xóa phiên bản tiền nhiệm không được tính là thua.
- **Số lượng phân đoạn được cung cấp bởi cốt truyện**: 26 đơn vị sẽ được ghi trực tiếp dưới dạng N phân đoạn bởi `3D6C` trong tập lệnh gốc (38 lệnh, tối đa 8 phân đoạn, được liệt kê trong `upgrade_refund.hpp`, `tests/test_upgrade_refund.py` được kiểm tra đối với ROM). `3D6C` Viết 5 vật phẩm và tất cả vũ khí có giá trị như nhau (không vượt quá giới hạn trên của máy), để instance nhận quà không có vật phẩm biến hình nào thấp hơn N: Host chỉ tính N đoạn này là miễn phí khi cả 5 vật phẩm và vũ khí biến hình đều ≥ N. Chỉ cần 1 vật phẩm thấp hơn N tức là instance đó không nhận được quà (tuyến khác, hoặc các đoạn được kế thừa từ phần trước, hoặc mua trên phần trước) và tất cả các vật phẩm sẽ bị loại hoàn lại tiền. Cùng một máy có thể nhận hoặc không nhận quà theo các tuyến khác nhau (chẳng hạn như ウイングゼロ); tình huống duy nhất sẽ có ít tiền hoàn lại hơn là nếu không nhận được quà và người chơi đổi từng vật phẩm thành N trở lên. Trong trường hợp này, N chặng đầu tiên sẽ không được hoàn tiền.

Tiền (`D_8010F5F4`, u32) cộng với tiền hoàn lại, dừng ở mức tối đa khi tràn. Không có giới hạn trên cho phương thức thêm tiền ban đầu (`3D5B`, thu nhập chiến đấu) và không có giới hạn bổ sung cho mục này.

**Mẹo**: Khi số tiền hoàn lại không bằng 0, một thanh nhắc nhở (bằng ngôn ngữ hiện tại) sẽ xuất hiện ở đầu cửa sổ trò chơi trong khoảng 6 giây và một dòng sẽ được thêm vào đoạn hội thoại phát lại (cả ba ngôn ngữ sẽ được lưu và sẽ thay đổi sau khi chuyển đổi bằng F7), ví dụ: "サンドロック đã rời quân đội và quỹ chuyển đổi 17.000 sẽ được trả lại." Tên máy bay vẫn là tên gốc tiếng Nhật. Lời nhắc dựa trên mô-đun hội thoại gốc và chỉ xuất hiện ở lối vào hồ sơ hợp nhất; máy chủ không có cửa sổ sẽ vẫn được hoàn tiền và chỉ ghi nhật ký.

**Kiên trì**: Số tiền hoàn lại sẽ được ghi vào quỹ và được lưu vào kho lưu trữ trò chơi; việc đóng mục này sẽ không lấy lại mục đó và việc mở nó sẽ không xóa mục đã xảy ra trước đó. Trong thời gian khởi động, mọi thao tác xóa cốt truyện (bao gồm cả việc xóa không hoàn lại) sẽ thêm `upgrade-refund-events.jsonl` (sơ đồ `srw64.upgrade-refund.v1`: nội dung, nguồn, liệu nó có được kế thừa hay không, phân đoạn miễn phí, năm vật phẩm và số lượng vũ khí cũng như quỹ trước và sau) vào thư mục đang chạy. Giao diện gỡ lỗi có thể được đọc bằng `srw64ctl events refunds`.

### 2.7 Các bộ phận đi kèm (`parts-carry-over`)

Khi phiên bản gốc phát hành phiên bản máy, tất cả các cải tiến của nó sẽ bị xóa: `800AA3C4` → `800A9DCC(.., 0, 1)` → `800A9D60` Ghi −1 vào khe, xóa số lượng thiết bị của thân máy và giảm số lượng thiết bị trong bản ghi kiểm kê (`D_8015E990`, mỗi phần u16: số byte sở hữu cao, số byte thấp của thiết bị) 1. **Số lượng nắm giữ không thay đổi, do đó các bộ phận sẽ không biến mất**. Bạn chỉ cần quay lại nhà kho và phải đợi lần bảo trì tiếp theo trước khi cài đặt lại - bạn chỉ có thể chơi cấp độ mà bạn tự động tấn công ngay sau khi thay đổi máy. Bản nâng cấp tại chỗ của ダンクーガ (`800ACB74`) cũng loại bỏ các bộ phận của chính nó và máy bay chiến đấu của từng quái thú.

Sau khi bật mục này, gói `800AAD28` ghi lại các thành phần của phần thân hiện tại của trình điều khiển trước chức năng ban đầu. Sau khi chức năng ban đầu trở lại, hãy cài đặt chúng vào các ô trống của cơ thể mới theo thứ tự ban đầu và thêm lại số lượng trang bị trong kho. Cuối cùng, điều chỉnh mức độ lan truyền `800A5924(机体, 1)` như trong màn hình bảo trì. Những thứ không thể nạp được sẽ để lại trong kho: Wutai EWタム, ヘビーアームズカスタム, アルトロンカスタム) và slot của Santai Makoto đều là 1, trong khi người tiền nhiệm của nó là 2, vì vậy những lần hoán đổi này sẽ để lại một mảnh mỗi cái thời gian.

Không cài đặt lặp lại: Nếu chức năng ban đầu trả về sớm vì "máy này đã có driver" và không có bộ phận nào bị tháo bỏ, gói sẽ thấy số lượng thiết bị trên máy cũ không thay đổi và bỏ qua. Nó cũng sẽ bị bỏ qua nếu số lượng tài sản ít hơn số lượng thiết bị, không còn chỗ trống và không tìm thấy phiên bản máy mới nào. Mỗi lần nó được vận chuyển thành công, `parts-carry-events.jsonl` (sơ đồ `srw64.parts-carry.v1`: số thân trước và sau, các bộ phận được vận chuyển, các bộ phận còn lại trong kho) sẽ được thêm vào thư mục đang chạy.

## 3. Thực hiện

| Vị trí | Nội dung |
| --- | --- |
| `tools/recomp/toolchain/generate_cpu.py` | `NATIVE_HOOKS` Tám tên mới đã được thêm: `801E1D64`, `801E1F08`, `801E1F10`, `801F4384`, `80204254`, `8020ABB4`, `801F5628`, `80203418`. Các chức năng ban đầu đã được đổi tên tương ứng. `srw64_original_potential_bonus`, `_seisenshi_bonus`, `_esp_bonus`, `_battle_hit_rate`, `_hit_estimate`, `_deploy_record`, `_battle_damage`, `_damage_estimate`. Yêu cầu `make recomp-cpu` được tạo lại. |
| `src/host/rule_fixes.hpp` | Thư mục và phân tích quy tắc, báo cáo khởi động, đọc bảng cấp độ, mức công suất cơ bản, `StatCap` (giới hạn tạm thời của giới hạn), `DummyScale` (tạm thời viết lại số lượng hàng giả trong hồ sơ triển khai). |
| `src/host/game_hooks.cpp` | Tám chức năng trình bao bọc: Khi quy tắc không được bật, chỉ chức năng ban đầu được gọi (khi bật thăm dò, các lệnh gọi đến hai chức năng tốc độ trúng cũng ở dạng chỉ đọc và ghi lại). |
| `src/host/rule_probe.hpp` | Đầu dò máy thực tế, xem phần tiếp theo. |
| `src/native/ui/frontend.cpp` (trang cài đặt), `macos/app_menu.mm` (mục nhập thanh menu) | [Trang cài đặt](../native/settings-window.md) tạo các nút quy tắc, kiểm tra trạng thái và ba cài đặt trước (`rules::presets`) được nhóm theo thư mục và đặt lại tiêu đề theo ngôn ngữ. |
| `src/host/graphics.cpp` | Cài đặt menu sau khi cửa sổ được tạo (thử lại mọi khung hình nếu thanh menu xuất hiện muộn) và xóa nó khi cửa sổ đóng. |
| `content/locales/*.json`, `src/srw64_native/profile.py` | Sao chép thực đơn; `UI_KEYS` được tự động lấy theo thư mục quy tắc. Quy định mới phải bổ sung tiêu đề bằng 3 thứ tiếng. |
| `src/srw64_native/rule_settings.py` | Thư mục quy tắc, lưu và đọc bản ghi phiên được chia sẻ bởi tập lệnh khởi chạy và thăm dò; `CORRECTIONS`/`DIFFICULTY` xác định cái nào được mở theo mặc định ở lần khởi động đầu tiên. |
| `tools/recomp/run/play_native.py`, `run_host_probe.py` | `--rules`/`--rule-fixes`; trường báo cáo `rule_fixes`, `rule_probe_enabled`. |
| `src/host/upgrade_refund.hpp` | Hoàn tiền khởi hành: bốn phạm vi đóng gói, tìm kiếm phiên bản tiền nhiệm, chi phí chuyển đổi và phân đoạn miễn phí, ghi và ghi quỹ, đọc tên máy (bảng văn bản 0, bắt đầu từ id 527). `generate_cpu.py` thêm bốn lần đổi tên nữa (`srw64_original_unit_register`, `_unit_remove`, `_unit_merge`, `_unit_delete`) thành `800AAD28`, `800AA464`, `800AB808`, `800AA3C4`. |
| `src/host/parts_carry.hpp` | Các thành phần khi đang di chuyển: Chụp các bộ phận của thân máy cũ, xác định xem chức năng ban đầu đã thực sự bị loại bỏ hay chưa, lắp vào thân máy mới theo khe trống, thêm nhiều lần vào thiết bị kho đồ và ghi nhật ký. Sử dụng lại trình bao bọc đã đổi tên hiện có của `800AAD28`. |
| `src/host/native_dialogue.cpp`, `dialogue_model.hpp`, `native_dialogue_text.cpp` | Mẹo hoàn tiền: viết quảng cáo bằng ba ngôn ngữ (`refund_notice`), dòng nhắc nhở đang xem xét (`Entry::notice`, không tham gia khớp màu loa, được chèn trước khi đoạn được đọc). |
| `src/host/notices.hpp` (được triển khai trong `src/native/ui/frontend.cpp`) | Bạn có thể nhìn thấy thanh nhắc nhở ở đầu cửa sổ trò chơi (RmlUi, bất kỳ phân phối chuỗi nào, hiển thị chuỗi cửa sổ), `status.notices` của giao diện gỡ lỗi và ảnh chụp màn hình. |

Tất cả người gọi đều đi qua bảng hàm lớp phủ (`LOOKUP_FUNC`), do đó, chiến đấu thực tế, ước tính AI và thăm dò đều sử dụng cùng một bộ hàm bao bọc.

## 4. Xác minh

- `make recomp-rule-fixes-test` (được sáp nhập vào `recomp-native-check`): Phân tích cú pháp và báo cáo ID, bao phủ tạm thời các đầu dò, đọc bảng cấp độ, giới hạn và khôi phục giới hạn (bao gồm lồng, con trỏ không hợp lệ, giới hạn thấp hơn giá trị trình điều khiển), hai bộ ranh giới thiết bị công suất dưới cùng (bao gồm cả trường hợp inf/NaN trong đó HP là 0), số lần chuyển đổi giả mạo và `DummyScale` Viết lại/khôi phục (bao gồm cả hồ sơ và hồ sơ không có danh tính giả của chúng tôi sẽ không bị ảnh hưởng).
- `tests/test_rule_fixes.py`: Lưu và đọc cài đặt, ghi phiên, điều chỉnh độ khó bị tắt theo mặc định, thư mục máy chủ và Python nhất quán, có đổi tên hook và đóng gói; Thông tin về ROM (hai hàm trống, byte nhập móc, bảng NT và bảng không được tham chiếu nằm trên cùng một đường cong, bảng rào cản gấp 10 lần, hình dạng bảng lực đáy và bánh răng đầu tiên là 1, tham số sử dụng bị ghi đè, so sánh giới hạn của trang trạng thái).
- Menu: `SRW64_WINDOW_CONTROL=1` được viết khi `rule-control.json` (lược đồ `srw64.rule-control.v1`, trường `sequence` và `item`, `item` là ID quy tắc, `original` hoặc `all`), chủ nhà nhấn mục thông qua menu của chính nó `performActionForItemAtIndex:` và ghi kết quả cấp bách, tất cả tiêu đề mục và kiểm tra trạng thái vào `rule-menu-events.jsonl`. Xem phần cuối của §5 để biết số đo thực tế.
- `make recomp-upgrade-refund-test` (được hợp nhất thành `recomp-native-check`): tích lũy giá, số lượng phân đoạn miễn phí (có được/không nhận được dưới dạng quà tặng), đóng quy tắc và không hoàn lại tiền ngoài phạm vi, các phiên bản kế thừa sẽ không được hoàn trả nhưng đã được ghi lại, các nhóm khác và địa chỉ không liên kết, giới hạn quỹ, trường nhật ký, đọc tên máy. Xem lại thứ tự, màu sắc và chuyển đổi ngôn ngữ của dòng nhắc trong `tests/native_dialogue.cpp`.
- `make recomp-parts-carry-test` (được sáp nhập vào `recomp-native-check`): Không chụp khi tắt quy tắc, chỉ cái có thể vừa khi khe không đủ, cài đặt đầy đủ khi khe đủ, không cài đặt lặp lại khi chức năng ban đầu không bị xóa, trường bộ nhớ và nhật ký không được ghi khi số lượng sở hữu không đủ/phần thân mới không có trong danh sách/không có trình điều khiển.
- `tests/test_upgrade_refund.py`: Bốn lần đổi tên và đóng gói, các nhóm độ khó và ba ngôn ngữ copywriting; Sự kiện ROM (`3D6C`, tổng cộng 38 mục, bảng quà tặng nhất quán theo từng mục, điểm bắt đầu của id tên nội dung là 527, nội dung của bảng tiền thân và lệnh tra cứu của `800AA814`).
- Đầu dò máy thật: xem §5.

## 5. Đầu dò máy thật

Khi `SRW64_RULE_PROBE=1`:

- Khi kịch bản dừng ở `3D38` lần đầu tiên và cả địch lẫn địch đều có đơn vị, chủ nhà sẽ gọi `801F4384` và `80204254` cho từng cặp đơn vị bạn/địch (cả hai hướng) và bốn loại HP (100/85/15/5%). Mỗi lần, phiên bản gốc, từng mục riêng lẻ và tất cả các chỉnh sửa lần lượt được sử dụng và kết quả được ghi vào `rule-probe.jsonl` (lược đồ `srw64.rule-probe.v1`). Bàn chiến đấu, HP và sổ đăng ký đều sẽ được khôi phục. Hàm tấn công quan trọng sử dụng các số ngẫu nhiên và không được gọi trong đầu dò.
- Mỗi lệnh gọi đến hai chức năng này (bao gồm cả mức độ tương tác của chính trò chơi và ước tính AI) cũng được ghi có vào `rule-calls.jsonl` (lược đồ `srw64.rule-call.v1`, `source` phân biệt `probe` với `game`).

Các đòn tấn công ở hai cấp độ nhỏ đều giống nhau: タケル (siêu năng lực L1) của đồng minh chúng ta, của Mari (siêu năng lực L2), ショウ (thánh chiến binh L3) và Manzhang trên ミニフォー (sức mạnh cơ bản L4, đánh/tránh + khả năng di chuyển vượt quá giới hạn 63);ロゼ (siêu năng lực) L2 của kẻ thù), ガラリア (dấu hiệu chiến binh thánh, cấp kỹ năng 0), ムニフォームゲ兵 (vượt quá giới hạn 50/55). Cả hai đều được nhập từ kho lưu trữ bảo trì đông lạnh, `--original-name-entry` và có thể tìm thấy tập lệnh đầu vào trong các tệp tương ứng.

### quy tắc-3 (`build/recomp/mini-stage/rules-3`, [`rules.json`](../../config/recomp/mini-stages/rules.json), 4.655 VI kết thúc bởi `EXIT_AFTER=3D47`)

Tất cả năm mục của `SRW64_RULE_FIXES` đều được in khi máy chủ khởi động; đầu dò được kích hoạt trong VI 4473 (`3D38` lúc đầu), `players=4 enemies=3`, tổng cộng 192 dòng (12 cặp × 2 hướng × 4 HP × 2 chức năng), 7 bộ quy tắc trên mỗi dòng. Kiểm tra từng dòng một (tập lệnh kiểm tra tính toán kỳ vọng theo công thức sau):

| Nội quy | Những thay đổi dự kiến ​​| Kết quả |
| --- | --- | --- |
| `esp-level` | +[Siêu sức mạnh của kẻ tấn công] (Bảng cấp − 64) −[Siêu sức mạnh của người phòng thủ] (Bảng cấp − 64) | 192/192 nhất quán |
| `seisenshi-level` | −[Thánh chiến binh phòng thủ] (Bảng cấp − 32) | 192/192 nhất quán; Tỷ lệ trúng đòn của Guraira (cấp độ 0) tăng từ 40 lên 72 khi bị tấn công, xác nhận rằng phiên bản gốc cũng cho 32 ở cấp 0 |
| `potential-bands` | Sự khác biệt giữa các giá trị sức mạnh cơ bản tấn công và phòng thủ từ trang bị ban đầu đến trang bị đã sửa đổi | 192/192 nhất quán; giá trị ban đầu/đã sửa của Wan Zhang (L4) ở mức 100/85/15/5% HP là 0/0, 0/0, 40/30, 40/40 |
| `potential-half` | Sự khác biệt giữa sức mạnh cơ bản của bên tấn công và phòng thủ giảm đi một nửa | 192/192 nhất quán; ví dụ Wan Zhang 5% HP tấn công Gaara 80 → 60 |
| `limit-cap` | Số lượng vượt quá × độ phóng đại địa hình và kích thước | Các kết hợp vượt quá 0 là không thay đổi; sự kết hợp với những thay đổi vượt mức phù hợp với độ phóng đại 0,8, 1,0, 1,2 (ví dụ: ムゲ兵tấn côngタケル−50, tấn công ショウ −39; tấn công Wanzhang ロゼ −75); hàm ước lượng là 6 Hàng thay đổi ít hơn do kẹp về 0 |
| Tất cả | Tổng các số hạng riêng lẻ | 186 hàng (không bao gồm 6 hàng có kẹp chức năng ước lượng) lỗi không vượt quá 1 (cắt ngắn) |

### quy tắc-battle-1 (`build/recomp/mini-stage/rules-battle-1`, [`rules-battle.json`](../../config/recomp/mini-stages/rules-battle.json), 12.000 VI)

Kẻ địch đang ở gần chúng ta, mọi sự điều chỉnh đều được kích hoạt, lượt của chúng ta kết thúc sau khi khai cuộc và cứ 90 VI trong lượt của kẻ thù nhấn A để chấp nhận phản công. Các lệnh gọi của chính trò chơi trong `rule-calls.jsonl`: AI ước tính 14 lần, trận chiến thực tế 6 lần (VI 5316 ムゲ兵→ショウ và phản công, VI 6956 ガラリア→Wanzhang và phản công, VI 8336ロゼ → Wan Zhang và Phản đòn), cặp phi công/máy móc trong lệnh gọi các tham số là chính xác, cho biết các thanh ghi gọi thực tế phù hợp với bố cục và đầu dò tham số ngăn xếp. Hoạt động đạt đến giới hạn trên của VI và kết thúc bình thường mà không có lỗi máy chủ; ảnh chụp màn hình bản đồ `present-2700.png` và `present-4200.png` hiển thị các đơn vị ở cả hai bên và máy bay địch màu xám sau hành động.

### Số đo thực tế của menu (`build/recomp/profile-play/sessions/20260918T015241.213153Z`)

Bắt đầu với zh-Hans, tắt tất cả các quy tắc, sử dụng móc điều khiển để nhấn tuần tự bốn mục, log `SRW64_RULE_MENU installed items=11`:

| Quy tắc được kích hoạt sau khi nhấn | | Trạng thái đã kiểm tra |
| --- | --- | --- |
| Giới hạn | `limit-cap` | Giới hạn chỉ đánh dấu vào |
| Bật tất cả | Tất cả sáu mục | Kiểm tra tất cả sáu mục |
| Siêu năng lực (bấm lại) | Xóa `esp-level` | Bỏ chọn Siêu năng lực và giữ phần còn lại |
| Đóng tất cả (quy tắc ban đầu) | Không có | Bỏ chọn tất cả |

`rules.json` (cuối cùng là một mảng trống), `rule-fixes-events.jsonl` (VI 177/180/238/241) và các dòng nhật ký được ghi cho mỗi thay đổi. `rule_fix_changes` của báo cáo lần chạy chứa bốn thay đổi này. Tiêu đề bài viết là bản sao tiếng Trung trong ngôn ngữ hiện tại và không thể nhấp vào mô tả.

Vòng này diễn ra khi `wing-kill-dummy` vẫn là quy tắc tùy chọn, do đó có sáu mục trong "Mở tất cả", `installed items=11`; mục này sau đó được chỉ định là [Sửa chữa cơ bản](base-fixes.md) và bị xóa khỏi thư mục. Bây giờ có ít mục hơn trong menu và bản ghi không bị thay đổi.

### quy tắc-hào quang-1 (`build/recomp/mini-stage/rules-aura-1`, `aura-slash-power`)

Máy dò bổ sung thêm chức năng thứ ba: ước tính sát thương AI `80203418` (không ném đòn chí mạng, không di chuyển số ngẫu nhiên; sát thương chiến đấu thực tế `801F5628` sẽ ném đòn chí mạng và máy dò không gọi). Thay vào đó, các phi công chiến binh thần thánh sử dụng vũ khí Điều kiện 15 của riêng họ. Tổng cộng có 288 dòng.

| Tấn công → Phòng thủ | Phiên bản gốc | Sau khi mở | Nghèo |
| --- | ---: | ---: | ---: |
| ショウ (Thánh chiến binh L3, ハイパーオーラ杀り 2400, tiền thưởng +600) → ロゼ | 2367 | 3499 | +1132 |
| Tương tự → ガラリア | 3807 | 4939 | +1132 |
| Tương tự → ムゲ兵 | 2727 | 3859 | +1132 |

Mức tăng của ba mục tiêu là như nhau, nghĩa là chỉ có vật phẩm tấn công được khuếch đại (2400→3000 nhân với một bộ hệ số tương đương với khả năng chiến đấu, sức mạnh và khả năng thích ứng với địa hình) và vật phẩm phòng thủ không bị ảnh hưởng. Sát thương và tốc độ đánh của những kẻ tấn công còn lại không thay đổi. Việc đóng gói chức năng thiệt hại chiến đấu thực tế và chức năng ước tính sử dụng cùng một phần logic và được bao phủ bởi các bài kiểm tra đơn vị. Vòng này không có giá trị riêng trong thực chiến.

### hoàn tiền-2 (`build/recomp/debug/20260918T131851.399969Z`, [`refund.json`](../../config/recomp/mini-stages/refund.json), `upgrade-refund`)

Trình điều khiển giao diện gỡ lỗi: Nhấn F8 trên menu chính để vào cấp độ nhỏ và xóa các sự kiện mở đầu theo bốn cách. `upgrade-refund-events.jsonl` phù hợp với cách tính lại từng mục của bảng giá ROM:

| Xóa | Nguồn | Cấp độ miễn phí | Lầu Năm Góc | Vũ khí | Hoàn tiền |
| --- | --- | ---: | ---: | ---: | ---: |
| ヘビーアームズ 130 (`3D6C 130,4` sau `3D5A …,4000`) | loại bỏ | 0 | 93.000 | 260.000 | 353.000 |
| デスサイズ 127 (chuyển sang 128, tiền thân được kế thừa) | xóa, `inherited` | — | 0 | 0 | 0 |
| デスサイズH 128 (mua giá 127 thì `4000`) | loại bỏ | 0 | 32.000 | 30.000 | 62.000 |
| ウイングゼロ 119 (tặng 3, đổi tất cả thành 5) | loại bỏ | 3 | 78.000 | 198.000 | 276.000 |
| ガイヤー 185 (`3D6A 3` kết hợp) | hợp nhất | 0 | 32.000 | 87.000 | 119.000 |

Vốn 0 → 810.000. Bốn lời nhắc xuất hiện theo thứ tự (tối đa ba lời nhắc cùng lúc, lời nhắc thứ tư được xếp hàng đợi) và có bốn dòng lời nhắc phía trước đoạn hội thoại trong phần đánh giá; sau khi F7 chuyển sang tiếng Anh, các lời nhắc trong phần đánh giá sẽ đồng thời chuyển sang tiếng Anh. Ở vòng trước (hoàn tiền-1), theo quy tắc cũ "lấy số phân đoạn thấp nhất", cả 2 phân đoạn của デスサイズH đều được coi là quà tặng và số tiền hoàn lại là 0. Người ta cũng phát hiện ra rằng chiều rộng của thanh nhắc không đủ và phần cuối bị cắt bớt, cả hai đều đã được sửa.

### Không được che chắn

- Đường dẫn tốc độ tấn công tới hạn (`801F47B0` gọi lực cơ bản, mục đích 0) chỉ được bao gồm trong bài kiểm tra đơn vị và không lấy một giá trị riêng trong máy thực tế.
- Không kiểm tra xem tỷ lệ trúng hiển thị trên giao diện có phù hợp với quyết toán hay không và không có thời gian chơi thử dài hạn; sau khi bật `limit-cap`, ý nghĩa màu cảnh báo trên trang trạng thái sẽ chuyển thành "Đã đóng" và bản thân giao diện vẫn không thay đổi.
- Phần thưởng sức mạnh tấn công của siêu năng lực không được triển khai (nó không tồn tại trong mã gốc, xem §2.2); sức mạnh vũ khí Orla của Thánh chiến binh đã được bổ sung bởi `aura-slash-power`.
- Khoản tiền hoàn lại khi rời nhóm (§2.6) đã được xác minh bằng cấp độ nhỏ [`refund.json`](../../config/recomp/mini-stages/refund.json) (xem §5), nhưng nó vẫn chưa được kích hoạt trong sự kiện rời nhóm thực sự trong cốt truyện ban đầu.