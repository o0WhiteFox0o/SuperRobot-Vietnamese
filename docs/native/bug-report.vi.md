> **Ngôn ngữ / Language:** [Tiếng Việt](bug-report.vi.md) · [English](bug-report.en.md) · [中文](bug-report.md)

# báo cáo vấn đề

2026-10-07. Trang "Phản hồi" của cửa sổ cài đặt (`frontend.cpp feedback_page`, giữa "Hành động" và "Giới thiệu") có ba dòng:

- **Thông tin nền tảng**: "Sao chép thông tin nền tảng" đặt một vài dòng văn bản vào khay nhớ tạm (`bug_report::summary`: phiên bản, bản gốc/HD, phiên bản gói HD; hệ thống, kiểu máy, bộ xử lý, kiến trúc, bộ nhớ; API đồ họa và card đồ họa; kích thước cửa sổ và pixel, kích thước giao diện, ngôn ngữ, màn hình rộng, bộ lọc và khung; bộ điều khiển, màn hình cảm ứng, thiết bị cầm tay; số lần chỉnh sửa mở và gian lận). Trang này cũng sẽ hiển thị những gì được sao chép và người chơi sẽ dán nó vào Vấn đề.
- **Báo cáo vấn đề**: Viết zip cho "Báo cáo vấn đề xuất khẩu" và đính kèm khi nêu vấn đề trên GitHub (Mẫu vấn đề `.github/ISSUE_TEMPLATE/bug.yml` vui lòng yêu cầu họ đính kèm).
- **Nơi đưa ra phản hồi**: "Phản hồi trên GitHub" mở trang chọn biểu mẫu của Sự cố; "Trang web chính thức cung cấp nhận xét văn bản" mở trang câu chuyện chính thức của trang web bằng ngôn ngữ hiện tại.

Có sẵn trên tất cả các nền tảng, bao gồm cả Android và Steam Deck. 8 tab được nén thành một dòng, lề trong bên trái và bên phải của các tab được giảm từ 10dp xuống 6dp và tên trang tiếng Anh sử dụng Báo cáo (`test_settings_window` được kiểm tra theo chiều rộng).

## Xuất cái gì

`<用户目录>/reports/Marchwind64-report-<日期>-<时间>.zip` (`src/host/bug_report.cpp`):

| Tài liệu | Nội dung |
| --- | --- |
| `report.json` | `srw64.bug-report.v1`: `system` (nền tảng, phiên bản hệ thống và số bản dựng, model, bộ xử lý, số lõi, bộ nhớ, cho dù đó là Steam Deck; Linux cũng có phiên bản phát hành, kernel, máy tính để bàn và loại phiên, Windows có số phiên bản và RtlGetVersion Wine, Android có phiên bản hệ thống, SDK, model của nhà sản xuất, chip); `game` (`frontend.cpp report_facts`: phiên bản, ngôn ngữ, kích thước giao diện, bản gốc/HD, gói HD có được cài đặt với phiên bản hay không, màn hình rộng, tên tệp khung và bộ lọc, sửa và gian lận quy tắc mở, tên bộ điều khiển, màn hình cảm ứng, thiết bị cầm tay, giao diện gỡ lỗi, kích thước cửa sổ, API đồ họa và tên/nhà sản xuất/trình điều khiển/bộ nhớ video `srw64_graphics_info`); `files` (các tệp khác ở dạng zip) |
| `settings/*.json` | `presentation.json`, `input.json`, `rules.json`, `update.json`, `saves/settings.json`, `hd/hd.json` trong thư mục người dùng (tùy theo cái nào đi kèm với cái nào) |
| `sessions/<编号>/launch.json`, `sessions/<编号>/run/*` | 3 lần chạy cuối cùng được giữ trong thư mục người dùng (lần chạy này xếp hạng đầu tiên): `launch.json` và `.json`, `.jsonl`, `.log`, `.txt` không trống trong thư mục chạy, bao gồm `console.log` |

Không bao gồm: ROM và bản sao ROM trong thư mục đang chạy (`runtime-data/`), lưu trữ, âm thanh đã ghi (`audio-output.s16`), ảnh chụp màn hình, `debug.json` (mã thông báo cho giao diện gỡ lỗi), `last-rom.txt`. Thư mục chính trong mỗi tệp văn bản được viết dưới dạng `~` (ngay cả `C:\\Users\\…` thoát JSON và ghi dấu gạch chéo chuyển tiếp trên Windows cũng được thay đổi). Nếu một tệp vượt quá 4 MiB thì chỉ 4 MiB cuối cùng được giữ lại. zip được ghi vào bộ nhớ bằng miniz (librecomp đã được liên kết), sau đó được ghi ra bằng đường dẫn `std::filesystem`, do đó, tên người dùng trên Windows có thể được ghi ngay cả khi tên người dùng không phải là ASCII.

Sau khi xuất, dòng này hiển thị vị trí tệp; đối với các nền tảng có thể mở thư mục (máy tính để bàn và Android), hãy nhấp vào "Mở thư mục chứa nó"; đối với Android, hãy mở thư mục `reports` trong Ứng dụng "Tệp"; đối với chế độ trò chơi Steam Deck, màn hình cảm ứng và thiết bị cầm tay, hãy nhấp vào "Sao chép đường dẫn tệp".

## console.log

Trước đây không có tệp nhật ký nào ở phía trình phát: dòng `SRW64_*` của máy chủ và đầu ra RT64 chỉ dành cho thiết bị lỗi chuẩn, macOS bị loại bỏ trực tiếp khi mở từ công cụ tìm và Windows chỉ có trong cửa sổ bảng điều khiển. Bây giờ `main` ban đầu gọi `console_log::start()` (`src/host/console_log.cpp`): thiết bị xuất chuẩn và thiết bị xuất chuẩn được kết nối với một đường ống và nội dung đã đọc được ghi trở lại vị trí ban đầu (thiết bị đầu cuối; Android chuyển sang logcat, thay thế `forward_output_to_logcat` ban đầu), đồng thời, nó được ghi vào `console.log` trong thư mục đang chạy hiện tại. Thư mục đang chạy chỉ được biết đến trong `run_host` (`console_log::attach`). Đầu ra trước đó lần đầu tiên được lưu trong bộ nhớ (tối đa 1 MiB) và được ghi đầu tiên sau khi được kết nối. Đợi tối đa 0,2 giây để đường ống thoát nước khi thoát ra. Ngoài stderr, tính năng xử lý sự cố của Linux (`crash_backtrace`) cũng ghi truy nguyên trực tiếp vào `console.log`, vì hệ thống có thể không được đọc khi quá trình này gặp sự cố.

Do đó, sau khi gặp sự cố hoặc treo máy, nếu người chơi mở lại trò chơi và xuất game thì `console.log` của lần chạy cuối cùng cũng sẽ có trong báo cáo (thư mục người dùng sẽ giữ lại 3 lần gần nhất).