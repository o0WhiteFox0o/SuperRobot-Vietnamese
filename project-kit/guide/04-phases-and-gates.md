# 04 — Giai đoạn và cổng nghiệm thu

## 4.1 Mô hình giai đoạn

| Loại | Dùng cho | Đặt tên | Ví dụ ở SuperRobot |
| --- | --- | --- | --- |
| Sản phẩm | Lộ trình phát hành | `M0…Mn` | M0 nền tảng tin cậy → M1 gói cơ bản đầu tiên → M2 truy vấn → M3 luật & hỗ trợ → M4 mở rộng nội dung |
| Phát hành/nền tảng | Chuyển nền tảng, phát hành | `P0…Pn` | P0 kế hoạch phát hành, P1 nhập ROM gốc |
| Chuyển đổi | Port sang môi trường mới | `X0…Xn` | X0 nền tảng khả chuyển → X1 đổi lớp đồ hoạ → X2 Linux … |
| Khảo sát | Nghiên cứu khả thi | `S1…` | các tài liệu 60fps, android-port |

## 4.2 Bảng giai đoạn (bắt buộc dạng này)

| Giai đoạn | Gói công việc | Ngưỡng hoàn thành (đo được) |
| --- | --- | --- |
| M0: Nền tảng tin cậy | vòng đời thoát/luồng, snapshot trạng thái, thiết kế lưu trữ | Tắt mọi tuỳ chọn vẫn chạy; cấu hình không chồng chéo; có bằng chứng cho nút an toàn |
| M1: … | … | … |

Quy tắc:
- Ngưỡng là **hành vi chứng minh được**, không phải "xong code".
- Mỗi giai đoạn nói rõ **phụ thuộc** và cái gì **được điều tra trước** (không phát hành trước giai đoạn nền).
- **Không hạ ngưỡng** để kịp tiến độ. Chưa an toàn → đưa vào "chưa hoàn thành".
- Ghi **ngoài phạm vi** tường minh (ví dụ: "chưa có MOD ngoài, chưa có SDK công khai").

## 4.3 Mẫu "Mục tiêu / ID / Ranh giới / Hành vi phải chứng minh"

| ID/Module | Ranh giới triển khai | Hành vi phải chứng minh |
| --- | --- | --- |
| B01 … | Cái được phép làm, cái không | Kịch bản kiểm chứng cụ thể, kết quả mong đợi |

Mỗi ID có đúng một dòng ngưỡng; tài liệu tính năng tương ứng đặt trong `features/`.

## 4.4 Ba "lát dọc" trước khi ước lượng thời gian

Trước khi cam kết lịch, làm 2–3 **vertical prototype** xuyên suốt (ví dụ: *chiến đấu – lưu – trạng thái đơn vị*), đo khoảng cách thực, rồi mới ước lượng. Khi chưa đủ dữ liệu: ghi **"chưa báo lịch xây dựng"**.

## 4.5 Cổng phát hành (release gate)

Một bản beta được phép khi: phạm vi **ghi rõ phần đã/ chưa** phủ; bản demo một phần **không** được gọi là bản hoàn chỉnh. Bản đầy đủ cần danh sách riêng về các tuyến, rẽ nhánh, kết thúc… (tuỳ lĩnh vực: cấu hình, vai trò, nền tảng, ngôn ngữ).

## 4.6 Kỷ luật xử lý lỗi xuyên giai đoạn

Tái hiện lỗi chạy suốt các giai đoạn; **lỗi ảnh hưởng quy trình nền được sửa trước**, không chờ giai đoạn sau. Mỗi lỗi xuống [bug-register](../templates/bug-register.md).

