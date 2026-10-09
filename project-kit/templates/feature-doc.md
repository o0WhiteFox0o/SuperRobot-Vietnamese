# {{Tính năng}}: {{hành vi gốc}} và cách tiếp quản

Ngày: {{YYYY-MM-DD}}. Trạng thái: **Đã cài – kiểm chứng một phần**: {{đã chứng minh gì; chưa chạy gì}} (xem §9). §1–3 là phân tích tĩnh; từ §4 là phương án.
Đường chuẩn so sánh: {{ảnh chụp/log gốc, nơi lưu, có commit hay không}}.

## 1. Hành vi gốc

Mô tả bằng **số liệu**, không hình dung: kích thước, toạ độ, thứ tự, trạng thái.

| Thành phần | Vị trí/kích thước | Nội dung |
| --- | --- | --- |

## 2. Khung điều phối của hệ thống gốc

- Điểm vào `{{hàm/endpoint}}`: làm gì, đọc/ghi trạng thái nào.
- Bảng trạng thái/chuyển cảnh: {{mô tả}}.
- Mọi lời gọi có **tác dụng phụ** (tiêu thụ RNG, ghi bộ nhớ, âm thanh) phải nêu rõ.

## 3. Điểm ràng buộc phương án tiếp quản

1. {{lời gọi không được bỏ vì có tác dụng phụ}}
2. {{hàm chỉ ghi bảng, có thể gọi cục bộ}}

## 4. Thiết kế tiếp quản

- Giữ nguyên **bố cục/luồng** gốc; thay phần {{trình bày}}.
- Ranh giới luồng/khoá: ai ghi, ai đọc, khi nào an toàn.
- Công tắc: `{{tên}}`, mặc định {{tắt}}, ảnh hưởng tương thích: {{…}}.

## 5. Dữ liệu và tương thích lưu trữ

| Dữ liệu | Định dạng | Tương thích ngược | Ghi chú |
| --- | --- | --- | --- |

## 6. Cài đặt

| Tệp | Trách nhiệm |
| --- | --- |
| `src/…` | |

## 7. Kiểm thử tự động

- Test thành phần: `tests/…`
- Màn tối thiểu/kịch bản: `config/…`

## 8. Cách chạy lại kiểm chứng

```text
{{lệnh/biến môi trường}}
```

## 9. Thực tế đã kiểm chứng

| # | Điểm | Cách kiểm | Kết quả | Bằng chứng |
| ---: | --- | --- | --- | --- |
| 1 | | | ✔ | `build/…` |

## 10. Chưa xác minh

- [ ] {{tình huống chưa chạy}}
- [ ] {{giới hạn/giả định đã biết}}

## 11. Liên quan
[A](a.md) · [B](../design/b.md)

