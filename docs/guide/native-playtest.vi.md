> **Ngôn ngữ / Language:** [Tiếng Việt](native-playtest.vi.md) · [English](native-playtest.en.md) · [中文](native-playtest.md)

# bản dùng thử bản địa

Cập nhật: 2026-09-18. Chỉ được hỗ trợ trên macOS (Apple Silicon, Metal). Để chuẩn bị xây dựng, hãy xem [Native Development Guide](native-development.md).

## Bắt đầu

Trước tiên hãy chạy `make` một lần trong thư mục kho (xem [Hướng dẫn phát triển bản địa](native-development.md#Building and Daily Checking)), sau đó nhấp đúp vào `scripts/Play SRW64 Native.command` hoặc chạy trong thiết bị đầu cuối:

```sh
scripts/Play\ SRW64\ Native.command --language zh-Hans
```

Tập lệnh là `tools/recomp/run/play_native.py --profile config/recomp/profiles/play-profile.json` và các tham số tiếp theo được truyền vào như cũ. Chương trình sẽ kiểm tra ROM và nhận dạng mã được tạo, biên dịch lại máy chủ nếu mã nguồn thay đổi, sau đó mở cửa sổ macOS Metal. Khi không có phiên dùng thử (và không có bản sao lưu bị đóng băng), hãy bắt đầu trò chơi mới ngay từ cảnh mở đầu; sau đó, tự động đọc SRAM của phiên dùng thử có thể kiểm chứng và thoát thông thường cuối cùng, `--new-game` rồi bắt đầu lại. Nếu đã có phiên nhưng không thể xác minh tất cả, lỗi sẽ được báo cáo và dừng và trò chơi sẽ không được lặng lẽ chuyển sang trò chơi mới.

| Thông số | Chức năng |
| --- | --- |
| `--language ja｜zh-Hans｜en` | Ngôn ngữ ban đầu; F7 chuyển đổi trong game, lựa chọn sẽ được ghi nhớ |
| `--images original｜hd` | Màn hình ban đầu; HD yêu cầu tài liệu thử nghiệm ở `assets/` cục bộ, công tắc F6 |
| `--rules original｜fixed｜all`, `--rule-fixes IDS` | Quy tắc ban đầu, sửa lỗi (mặc định lần đầu tiên) hoặc điều chỉnh độ khó; sẽ được ghi nhớ, hãy xem [Sửa quy tắc tùy chọn](../gameplay/rule-fixes.md) |
| `--upgrade-rules PATH` | Để biết tệp quy tắc về mức tăng sửa đổi, giá và giới hạn trên, hãy xem [Số giai đoạn sửa đổi và giới hạn trên](../gameplay/upgrade-limits.md) |
| `--resolution-scale 1..8` | Nhiều độ phân giải bên trong, kích thước phông chữ và bố cục không thay đổi |
| `--mute` | Tắt âm thanh |
| `--list-saves`, `--restore-session ID` | Xem hoặc chỉ định các phiên dùng thử được khôi phục |
| `--mini-stage FILE` | Thay thế tập đầu tiên bằng một sân khấu mini tự tạo. Nhấp vào "Enter Mini Stage" trên menu chính hoặc nhấn F8 để truy cập trực tiếp. Việc khởi tạo ký tự mặc định được tự động hoàn thành. Xem [Sân khấu nhỏ](../script/mini-stage.md) |

`scripts/Play SRW64.command` (không có `--profile`) là mục dùng thử sớm: thư mục ngôn ngữ và hồ sơ không được tải, lịch sử lưu trữ nằm ở `build/recomp/play/` và lần chạy đầu tiên phụ thuộc vào tệp phê duyệt tập đầu tiên được cố định cục bộ của nhà phát triển và không thể sử dụng trực tiếp bản sao mới.

Nút ##

Các phím chữ cái được ánh xạ tới các phím vật lý. Nhả tất cả các phím khi cửa sổ mất tiêu điểm; các phím tắt hệ thống với Lệnh, Tùy chọn hoặc Điều khiển không được đưa vào trò chơi. Tay cầm chơi game ngoài bàn phím vẫn chưa được kết nối.

| Bàn phím | Đầu vào/Cách sử dụng N64 |
| --- | --- |
| Phím định hướng | Phím chéo: con trỏ, menu; menu vòng tiêu đề để xoay trái và phải |
| Z | A: Khẳng định và thúc đẩy đối thoại |
| X | B: Hủy, trả lại |
| Nhập | BẮT ĐẦU; Xác nhận menu tiêu đề bằng Enter |
| Hỏi/Đáp | Trái/R; bạn có thể chuyển đổi máy bay của chúng tôi trên bản đồ |
| Không gian | Kích hoạt Z |
| Tôi/K/J/L | C Lên/Xuống/Trái/Phải |
| W/S/A/D | Cần analog lên/xuống/trái/phải |
| F5 | Tải lại tệp văn bản hội thoại (các sửa đổi trong `build/recomp/profile-play/dialogue/<语言>/` ghi đè từng bản dịch đi kèm, xem [Tệp văn bản dòng](dialogue-text.md)); menu ứng dụng "Tải lại dòng" cũng có tác dụng tương tự |
| F6 | Chuyển Bản gốc/HD (yêu cầu tài liệu HD cục bộ) |
| F7 | Tiếng Nhật → Tiếng Trung → Tiếng Anh chuyển đổi ngôn ngữ theo chu kỳ, không có cửa sổ bật lên, không khởi động lại |
| F8 | Nhập cấp độ nhỏ trong menu chính với `--mini-stage` |
| Nút Esc hoặc đóng cửa sổ | Thoát khỏi chương trình |

Không giữ Enter cho đến khi màn hình khởi động xuất hiện: phiên bản gốc sẽ vào màn hình quản lý Controller Pak, trong đó `osPfsIsPlug` chưa được triển khai và máy chủ sẽ hủy bỏ.

Các thao tác đọc đối thoại và mở đầu cốt truyện (xem [Giao diện người dùng đối thoại](../native/native-dialogue-ui.md) để biết chi tiết):

| Hoạt động | Bàn phím |
| --- | --- |
| Trang đọc tiếp theo | Z |
| Tự động tăng/giảm tốc độ đọc (0 có nghĩa là thủ công) | ↑ / ↓ |
| Tắt tính năng đọc tự động và hủy bỏ qua | X |
| Nhấn và giữ để tua đi, thả ra để dừng | E + Z |
| Bỏ qua đoạn script hiện tại; văn bản thu phóng mở và đoạn mở đầu tuyến đường cũng được áp dụng | E + Nhập |
| Bật/tắt phát lại; Đang phát lại ↑↓ Cuộn | Q |
| Cỡ văn bản 10–18 (mặc định 13) | Tôi/K |

## Giao diện gốc

- **Trang lựa chọn nhân vật chính**: Trò chơi mới xuất hiện sau khi bỏ qua phần mở đầu công khai, với bốn lá bài (siêu loại/loại thật × nam/nữ) cạnh nhau; ←→ chuyển đổi, Enter/Z để xác nhận hoặc nhấp vào thẻ.
- **Trang xác nhận**: Sau khi chọn nhân vật chính, tên của nhân vật chính và đối tác sẽ được hiển thị. Enter/Z bắt đầu câu chuyện và Esc quay lại phần lựa chọn diễn viên. Tên không thể thay đổi và được hiển thị theo ngôn ngữ đọc. Xem [Trang xác nhận và lựa chọn nhân vật chính] (../native/native-name-entry.md).
- **Trang liên kết**: Xuất hiện khi chọn "リンク" trên màn hình chuẩn bị. Không cần hộp mực Transfer Pak và Link Battler. Ba thẻ công việc (ガンダムF91, ゴーショーグン, ザンボット3) nằm cạnh nhau, ←→ chuyển đổi, dấu cách/Z hoặc nhấp vào thẻ để kiểm tra, Enter để tiếp tục đến màn hình liên kết ban đầu, Esc/X để quay lại menu chuẩn bị. Các tác phẩm đã được kiểm tra sẽ được thêm vào dưới dạng cấp độ đặc biệt trước trận chiến tiếp theo; các tác phẩm đã được thêm sẽ có màu xám và các khóa đã lên lịch sẽ được kiểm tra. Xem [Liên kết Link Battler](../gameplay/link-battler.md) §10.
- **Trang xác nhận trước trận chiến**: Sau khi chọn vũ khí và mục tiêu, HP/EN, năng lượng, vũ khí, tỷ lệ đánh cuối cùng và tỷ lệ đánh chí mạng của cả hai bên sẽ được hiển thị, cũng như hiệu chỉnh vũ khí một cột và sát thương ước tính bao gồm tinh thần, phòng thủ và lá chắn. Khi kẻ địch tấn công, bạn có thể chọn vũ khí phản công, né tránh hoặc phòng thủ; nhấn nút chuột hoặc nút Tab để chọn, Enter/Z để thực thi và khi nhóm của bạn tấn công, nhấn Esc/X để quay lại lựa chọn mục tiêu. Các công tắc hoạt ảnh tuân theo cài đặt trò chơi gốc. Xem [Giao diện người dùng xác nhận trước trận chiến](../native/native-battle-ui.md).
- **Thanh menu "Tùy chọn"**: "Điều chỉnh lối chơi" chuyển đổi từng quy tắc tùy chọn. "Cài đặt..." (⌘,) mở cửa sổ cài đặt để chuyển đổi quy tắc, ngôn ngữ và màn hình. Nó sẽ có hiệu lực ngay lập tức và được ghi nhớ. Xem [Cửa sổ cài đặt] (../native/settings-window.md).
- **Thanh nhắc nhở**: Sau khi bật điều chỉnh độ khó "Hoàn tiền hàng đầu", cốt truyện sẽ yêu cầu máy hoàn lại số tiền sửa đổi khi xuất ngũ. Lời nhắc sẽ hiển thị ở đầu cửa sổ trong khoảng 6 giây và sẽ để lại một dòng trong phần xem lại đoạn hội thoại. Xem [Sửa quy tắc tùy chọn] (../gameplay/rule-fixes.md) §2.6.

## Lưu trữ

Lưu trò chơi và sau đó thoát. Mỗi lần chạy được ghi vào một thư mục phiên riêng biệt (`build/recomp/profile-play/sessions/`), với các lần chạy tiếp theo sẽ lọc bản sao có thể xác minh gần đây nhất theo nhận dạng ROM được báo cáo bởi lần chạy, thoát bình thường và tóm tắt cuối cùng; các phiên bị lỗi sẽ báo cáo nguyên nhân và phương án dự phòng cho một bản sao có thể kiểm chứng trước đó. Có sẵn `--list-saves` để xem, `--restore-session SESSION_ID` để chỉ định khôi phục. Tính toàn vẹn của tệp và tính hợp lệ của vị trí trong trò chơi được đánh giá riêng biệt, xem [Save Recovery](native-save-recovery.md) để biết chi tiết. Cửa sổ không có giới hạn thời gian thoát tự động và trò chơi sẽ không tự động hoạt động. Chế độ dùng thử chỉ giữ lại ảnh chụp màn hình GPU mới nhất và siêu dữ liệu tương ứng, đồng thời chẩn đoán âm thanh và điều khiển được lưu trong thư mục con này.

## Trạng thái xác minh

Cách khắc phục âm thanh hiện tại là hàng đợi thiết bị đã được xác minh sẽ không tiếp tục tích lũy trong các trận chiến đã thử nghiệm và đồng bộ hóa âm thanh và video trên loa thực tế vẫn yêu cầu nghe thủ công. 2026-09-12 Khôi phục từ khởi đầu nguội của lối chơi bị đóng băng đến bảo trì, kiểm tra tổng vòng 7, quỹ 14.500 và Manami cấp 2 / SP 102/102; không vào tập thứ hai. 2026-09-18 Sử dụng [Giao diện gỡ lỗi] (debug-interface.md) từ trình điều khiển khởi động nguội đến đoạn hội thoại lộ trình của nhân vật nam chính và xem lại đoạn mở đầu bị bỏ qua, cỡ chữ, tua đi nhanh và trang tên.