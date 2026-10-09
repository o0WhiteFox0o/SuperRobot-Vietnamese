# 05 — Thang kiểm chứng (Verification Ladder)

Mỗi bậc có **phạm vi riêng**. Bậc cao hơn không tự suy ra từ bậc thấp, và "có ảnh chụp" hay "exit code 0" **không** nghĩa là cả quy trình đã nghiệm thu.

| Bậc | Tên | Cho biết | Không cho biết | Ví dụ |
| ---: | --- | --- | --- | --- |
| 1 | Kiểm tra tĩnh | Cấu trúc, định dạng, hợp lệ cú pháp, liên kết | Hành vi lúc chạy | lint, `test_docs`, kiểm định lược đồ |
| 2 | Test thành phần | Một module đúng với đầu vào cho trước | Tích hợp | unit test, test codec |
| 3 | Replay cố định | Cùng đầu vào → cùng đầu ra (tất định) | Đúng so với hệ thống gốc | replay N khung, so sánh hash |
| 4 | Chạy sản phẩm thật | Luồng thật hoạt động trên máy cụ thể | Máy/nền tảng khác | chạy với profile, điều khiển bằng script |
| 5 | Chạy trên hệ thống tham chiếu | Khớp với hành vi gốc | Mọi tình huống | so với trình mô phỏng/bản gốc |
| 6 | Kiểm tra thủ công có hướng dẫn | Trải nghiệm, bố cục, cảm nhận | Tái lập | checklist thủ công + ảnh |

## 5.1 Mỗi biên bản kiểm chứng phải ghi

Dùng [verification-record.md](../templates/verification-record.md): cấu hình (profile/phiên bản/máy), đầu vào cố định, **bằng chứng** (log/ảnh/hash/đường dẫn `build/…`), kết quả từng điểm quan sát, **giới hạn**, danh sách **chưa xác minh**.

## 5.2 Kỹ thuật so sánh "gốc vs sửa"

Khi sửa lỗi/thay logic: chạy **hai lượt giống hệt nhau trừ một công tắc** (cùng binary, cùng ảnh, cùng script đầu vào) và lập bảng:

| Điểm quan sát | Gốc | Sau sửa |
| --- | --- | --- |
| Trước điểm khác biệt | A | A (giống từng khung) |
| Sau điểm khác biệt | B | C ← khác biệt có chủ đích |

(Mẫu thực tế: `docs/gameplay/base-fixes.md` §2 — hai lượt `…-original-5` và `…-fixed-1`.)

## 5.3 Tạo điều kiện kiểm chứng ngay từ thiết kế

| Cơ sở hạ tầng | Lợi ích |
| --- | --- |
| Giao diện gỡ lỗi (JSON-RPC/CLI/MCP) | Tự động hoá chạy thật, không cần bấm tay |
| Snapshot trạng thái tại ranh giới lệnh | So sánh bằng chứng từng bước |
| Màn/"mini-stage" tối thiểu | Ép một quy trình dài vào một ca kiểm thử ngắn |
| Cờ môi trường kiểm chứng (`PROBE=1`, `CAPTURE=1`) | Bật bằng chứng khi cần, tắt trong sản phẩm |
| Kiểm tra layout offline | Phát hiện lỗi giao diện không cần khởi chạy |

> [!IMPORTANT]
> Quy tắc: **tính năng chưa có đường kiểm chứng tự động thì chưa tính là "đã cài"** — chỉ là "đã cài – chưa kiểm chứng".

