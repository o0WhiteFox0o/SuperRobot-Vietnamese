# Kế hoạch chuyển {{nền tảng/công nghệ}}: {{A}} → {{B}}

Ngày: {{YYYY-MM-DD}}. Trạng thái: **Kế hoạch**. Tiếp nối [{{kế hoạch phát hành}}](release-plan.md).
Kết luận đến từ **kiểm toán tĩnh** mã nguồn, chuỗi dựng và phụ thuộc ngày {{ngày}}, **chưa dựng/chạy thật trên {{B}}**.

## Nền tảng mục tiêu

| Nền tảng | Backend | Trình biên dịch | Gói đầu tiên | Máy nghiệm thu |
| --- | --- | --- | --- | --- |

Nguyên tắc chọn: theo upstream/chuẩn sẵn có, **không tự viết logic chọn**; phần vẽ/IO tự viết đi qua **một giao diện chung**; không giữ hai bộ mã song song.

## Hiện trạng

**Đã khả chuyển:** …

**Mục chặn, xếp theo khối lượng công việc:**
1. {{mục}} — vị trí `file:dòng`, quy mô (số dòng/chỗ), cách xử lý đề xuất
2. …

## Giai đoạn

### X0 Nền tảng khả chuyển (làm trên máy hiện tại, hành vi **không đổi**)
- Dựng: preset theo nền tảng, bỏ cứng trình biên dịch khỏi script.
- Mã: thay API đặc thù nền tảng bằng lớp trừu tượng; chuẩn hoá đường dẫn/encoding.
- Công cụ: ép UTF-8, giữ newline `\n`, helper cho đường dẫn/hậu tố.
- Nghiệm thu: mọi kiểm tra hiện có vẫn xanh; biên dịch được phần CPU-only trong container.

### X1 {{Đổi lớp trọng tâm}} (nghiệm thu ở nền tảng gốc trước)
### X2 {{Nền tảng thứ hai}}
### X3 {{Nền tảng thứ ba}}
### X4 Phát hành

| Giai đoạn | Ngưỡng nghiệm thu |
| --- | --- |

## Phân công bước dựng
| Bước | Chạy ở đâu | Công cụ |
| --- | --- | --- |

## Chưa xác minh
- [ ] …

