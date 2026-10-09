# Kế hoạch phát hành: {{sản phẩm}} {{phiên bản}}

Ngày: {{YYYY-MM-DD}}. Trạng thái: **Kế hoạch**.

## Gói phát hành

| Gói | Nền tảng | Nội dung | Cách tạo | Kích thước |
| --- | --- | --- | --- | --- |

Gói lớn tuỳ chọn (ví dụ tài nguyên HD) tách riêng, có **hướng dẫn cài và tuyên bố** rõ ràng.

## Quy tắc pháp lý và nguồn gốc
- Không phân phối: {{đầu vào có bản quyền}}. Người dùng tự cung cấp, kiểm tra bằng hash.
- Giấy phép bên thứ ba: {{bảng}}.

## Điều kiện cổng (tất cả phải đạt)
- [ ] Toàn bộ test xanh trên commit phát hành.
- [ ] Biên bản kiểm chứng cho từng nền tảng được công bố (có ghi giới hạn).
- [ ] Tài liệu liên quan đã đổi nhãn trạng thái.
- [ ] Ghi rõ phần **chưa** kiểm chứng trong ghi chú phát hành.

## Quy trình

1. Tạo bản dựng từ **một commit** (tag).
2. Chạy kiểm tra gói (liên kết động, phụ thuộc kèm, chữ ký).
3. Kiểm thủ công theo checklist.
4. Phát hành thủ công/CI → kênh {{…}}.
5. Cập nhật {{trang web / latest.json}}.

## Kiểm tra cập nhật
Cơ chế, tần suất, riêng tư, **không tải/cài tự động** (nếu có).

## Hỗ trợ và báo lỗi
Cách người dùng xuất báo cáo (không kèm dữ liệu riêng tư/đầu vào có bản quyền).
