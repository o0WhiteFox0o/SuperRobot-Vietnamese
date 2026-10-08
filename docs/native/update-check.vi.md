> **Ngôn ngữ / Language:** [Tiếng Việt](update-check.vi.md) · [English](update-check.en.md) · [中文](update-check.md)

# Kiểm tra cập nhật

2026-10-06. Kiểm tra cập nhật trong trò chơi dành cho ba nền tảng máy tính để bàn (macOS, Windows, Linux/Steam Deck): Trò chơi chỉ đọc `/latest.json` từ trang web chính thức mà không cần nhận dạng và không cần tải xuống; người chơi sẽ được hỏi trước khi kết nối Internet lần đầu tiên và có thể tắt trong cài đặt sau này. Android không làm được điều đó (`update::supported()` là sai, trang "Giới thiệu" chỉ có một dòng liên kết).

## Nên làm gì và không nên làm gì

- Đọc `https://srw64.dreamquest.club/latest.json` của trang web chính thức (được tạo bởi trang web `web/src/pages/latest.json.ts`, `schema` là `srw64.latest.v1`) và so sánh `version` với `SRW64_VERSION` của chương trình này.
- Yêu cầu không mang theo bất kỳ thông tin nhận dạng nào (không có mã thông báo, không có thông tin thiết bị) và chỉ có một GET.
- Không tải xuống, không cài đặt: Khi có phiên bản mới, chỉ cung cấp phiên bản và ngày tháng, đồng thời nút sẽ mở trang tải xuống (`download.<zh|en|ja>`) và hướng dẫn cập nhật (`notes.<语言>`) bằng ngôn ngữ tương ứng trong trình duyệt hệ thống. Các phương pháp cài đặt macOS Signature, Deck và Windows khác nhau nên ban đầu chỉ nhắc nhở.

## Phiên bản gói HD

Bắt đầu từ 2026-10-07, gói HD có số phiên bản riêng và được phát hành riêng biệt với ứng dụng:

- Số phiên bản giống với số của ứng dụng (số đầu tiên là `1.0`, sau đó chữ số cuối cùng được tăng thêm một theo mặc định: `1.1`, `1.2`...; sử dụng `--hd-version 2.0` để chỉ định khi thực hiện các thay đổi lớn), được viết trong gói `hd.json`'s `version`; `hd.json` và các tệp khác `content_sha256` là bản tóm tắt (`prepare_hd_bundle.py`) của tất cả các tệp (đường dẫn + nội dung, ngoại trừ `hd.json`, `NOTICE.txt`) trong gói. Gói HD có thể được sao chép: cùng một tài liệu được tạo hai lần và các tệp 6644 có cùng một byte.
- `build_release.py` Tạo gói HD mỗi lần, so sánh bản tóm tắt với `hd.content_sha256` của `web/src/data/release.json` trong bản gửi được tạo: nếu chúng giống nhau, hãy sử dụng phiên bản đó mà không cần đóng gói; nếu chúng khác nhau, hãy lấy số phiên bản mới (chữ số cuối cùng mặc định cộng với một, có thể chỉ định `--hd-version`), nhập `Marchwind64-HD-<版本>.zip`, `release.json` Có thêm `publish_hd` (thẻ `hd-<版本>`, `--latest=false`, được phát hành trước ứng dụng) và một `hd-release-notes.md` khác. Ghi chú phát hành của ứng dụng chỉ liên kết đến trang phát hành của gói HD hiện tại.
- Sau khi phát hành, `web/scripts/sync-release.mjs` viết `hd` vào `release.json` trên trang web chính thức; `hd` của `/latest.json` cung cấp phiên bản, từng trang tải xuống ngôn ngữ (trang cài đặt `#hd`), tệp và kiểm tra giá trị. Các gói cũ hơn không có số phiên bản (các gói được phát hành cùng ứng dụng ở phiên bản 0.3.5) sẽ không xuất hiện trong `latest.json`.
- Trò chơi đọc các gói đã cài đặt: `SRW64_ART_PACK` (`hd/art`) bên cạnh `hd/hd.json`. Thư mục nghệ thuật để phát triển và chạy không có `hd.json` nên chưa được cài đặt. `hd_newer()` (`update_version.hpp`): Điều này sẽ chỉ nhắc nếu gói được cài đặt, phiên bản trên trang web chính thức mới hơn hoặc gói đã cài đặt không có số phiên bản; người chơi chưa cài đặt HD sẽ không được nhắc.

## Lối vào

| Lối vào | Hành vi |
| --- | --- |
| Thiết lập trang "Giới thiệu" | Các dòng liên kết: trang web chính thức (`/<语言>/`), mã nguồn, đưa ra phản hồi (vấn đề về GitHub). Hàng cập nhật: Nút và kết quả "Kiểm tra cập nhật" (chưa được kiểm tra/đang kiểm tra/đã có phiên bản mới nhất/mới "Kiểm tra cập nhật khi khởi động". |
| Menu ứng dụng macOS | "Giới thiệu về Marchwind64" đã được thay đổi để mở trang cài đặt "Giới thiệu" (thay thế bảng điều khiển hệ thống của SDL); sau đó "Kiểm tra cập nhật..." đã được thêm vào: mở trang "Giới thiệu" và kiểm tra ngay bây giờ. Windows/Linux không có thanh menu, hãy sử dụng trang "Giới thiệu" trong cài đặt. |
| Màn hình tiêu đề | Khi bạn dừng lại ở tiêu đề (`intro::title_waiting()`) lần đầu tiên, hãy hỏi "Bạn có muốn kiểm tra xem có phiên bản mới khi khởi động không?" trong hộp của bảng cài đặt: "Kiểm tra" hoặc "Không kiểm tra". Đóng (B/Esc) được tính là "Không kiểm tra". Sau đó thay đổi nó trên trang "Giới thiệu". Các phiên gỡ lỗi (`SRW64_DEBUG`), các lần chạy cửa sổ ẩn (`SRW64_BACKGROUND`) và các lần chạy không có thư mục người dùng đều bị bỏ qua. |
| Trang “Giới thiệu” dòng gói HD | Các phiên bản HD đã cài đặt (gói cũ không có số phiên bản và gói đã gỡ cài đặt mỗi gói có một câu). Khi có phiên bản cập nhật trên website chính thức còn có thêm câu "Có phiên bản HD X mới". Nút "Tải xuống gói HD" sẽ mở phần HD của trang cài đặt. |
| Góc dưới bên trái của tiêu đề | Sau khi tìm thấy phiên bản mới trong quá trình kiểm tra, "Phiên bản X mới" màu vàng sẽ xuất hiện phía trên số phiên bản. Nhấp vào nó để mở trang "Giới thiệu" và tập trung vào "Trang tải xuống". Chương trình này sẽ tự động biến mất sau khi được nâng cấp lên phiên bản này hoặc cập nhật. Khi ứng dụng đã được cập nhật và có phiên bản mới của gói HD, "Gói HD phiên bản mới X" được hiển thị và tiêu điểm nằm ở "Tải xuống gói HD". |

## Trạng thái và tập tin

`update.json` (thư mục người dùng, trình khởi chạy được chuyển qua `SRW64_UPDATE_STATE`, cùng thư mục với `presentation.json`):

```json
{"schema": "srw64.update-check.v1", "automatic": true, "checked_at": 1791262005, "latest": { …上次读到的 latest.json… }}
```

- `automatic` Mặc định = Chưa trả lời (sẽ hỏi trong tiêu đề).
- Khi bật, nó sẽ được kiểm tra sau một ngày kể từ `checked_at` sau khi khởi động (khi giao diện được khởi tạo); sẽ không có lỗi nào được hiển thị nếu việc kiểm tra tự động không thành công và kết quả cuối cùng sẽ được giữ lại. Kiểm tra thủ công bỏ qua khoảng thời gian và hiển thị lý do thất bại.
- Đã lưu `latest` để có thể hiển thị gợi ý tiêu đề ngay cả khi ngoại tuyến.

## Triển khai

| Tài liệu | Nội dung |
| --- | --- |
| `src/host/update_check.{hpp,cpp}` | Trạng thái, luồng nền (luồng tách rời, đối tượng trạng thái không được phát hành), `update.json` đọc và viết, `latest.json` phân tích cú pháp, `SDL_OpenURL` |
| `src/host/update_version.hpp` | So sánh phiên bản `newer` (trường số, `0.3.10 > 0.3.9`, hậu tố bị bỏ qua) với ngôn ngữ trang web; `tests/native_update.cpp` Kiểm tra |
| `src/host/update_http.cpp` | Windows: WinHTTP (liên kết `winhttp`); Linux/Deck: thời gian chạy `dlopen``libcurl.so.4` của hệ thống (không nhập phần đóng gói, nếu thiếu, nó chỉ không kiểm tra được); Android: sơ khai |
| `src/host/macos/update_http_macos.mm` | macOS: `NSURLSession` (không có giao diện) |
| `src/native/ui/frontend.cpp` | `about_rows`, `update_ask_panel`, `open_about`, lời nhắc tiêu đề `home-update`, nút `update-*`/`about-link:*` |
| `src/host/macos/app_menu.mm` | Chuyển hướng "Giới thiệu" và "Kiểm tra cập nhật..." |

Thời gian chờ 15 giây cho tất cả các yêu cầu, giới hạn phản hồi 1 MB. Các phím văn bản giao diện nằm trong UI_KEYS của `src/srw64_native/profile.py` (`update_*`, `update_hd_*`, `settings_update*`, `about_link_*`, `menu_about`, `menu_check_updates`).

## Xác minh

- `tests/native_update.cpp` (root CMake's `native-update`): so sánh phiên bản, ngôn ngữ trang web so với `hd_newer`. `HdVersionTests` của `tests/test_hd_release.py`: Phần tóm tắt chỉ thay đổi theo nội dung và chữ số cuối cùng của số phiên bản được tăng thêm một.
- 2026-10-07 Sử dụng một chương trình nhỏ độc lập (`update_check.cpp`＋`update_http_macos.mm`, `SRW64_UPDATE_URL` trỏ tới `latest.json` cục bộ, `SRW64_ART_PACK` trỏ tới `hd/art` giả) để xác minh bốn tình huống: gói không có số phiên bản, lời nhắc gói cũ hơn, cùng một phiên bản và không cài đặt HD Không có lời nhắc.
- Sử dụng `SRW64_UPDATE_URL` để trỏ đến nơi khác (`file://` cục bộ hoặc máy chủ cục bộ) khi kiểm tra; trình khởi chạy sẽ giữ lại biến này. 2026-10-06 Sử dụng một chương trình nhỏ độc lập (chỉ liên kết `update_check.cpp`, `update_http_macos.mm`) để xác minh trên macOS: local 0.3.6 báo cáo phiên bản mới thành 0.3.5, báo cáo 0.3.6 đã là phiên bản mới nhất, liên kết được lấy theo ngôn ngữ, `update.json` được viết; trang web chính thức chưa được triển khai và báo cáo "HTTP 404"; không phải- Phản hồi 200 của `latest.json` báo cáo "không phải mô tả bản phát hành".
- Bố cục trang "Giới thiệu": `tools/recomp/ui_audit/run_audit.py --only about`, ba ngôn ngữ và bốn kích thước không bị tràn.
- HTTP cho Windows và Linux chỉ được kiểm tra ở cấp độ biên dịch (nhánh Linux là `-fsyntax-only` trên macOS), phải được xác nhận trên sản phẩm CI hoặc máy thật.