# Đầu vào cục bộ và ghi chép nguồn

Tệp này ghi các đầu vào cần để tái hiện thí nghiệm nhưng **không thể commit**. Hash là *cổng danh tính*; chúng không có nghĩa các tệp này được phép phân phối lại.

## {{Đầu vào chính}}

- Vị trí: `{{đường dẫn cục bộ}}`, không commit.
- Kích thước: {{n}} byte.
- SHA-256: `{{hash}}`.
- Phiên bản/định danh: {{…}}.

## {{Dữ liệu tham khảo lưu trong repo}}

- Vị trí: `reference/{{file}}`; khoá danh tính độc lập: `config/data/{{file}}.json`.
- Nguồn: [{{tên}}]({{url}}), commit `{{hash}}`.
- Tệp gốc ở nguồn: `{{đường dẫn}}`, SHA-256 `{{hash}}`.
- Mục đích: {{dùng để làm gì}}.

### Độ lệch so với nguồn ({{ngày}}, kiểm theo {{phương pháp}})

- Phát hiện: {{n}} mục khác nguồn.
- Cách kiểm: 1) … 2) … 3) …
- Kết quả và quyết định: …

## Chuỗi công cụ cố định

| Công cụ | Phiên bản khoá | Nguồn |
| --- | --- | --- |

## Tài liệu tham khảo
- [{{tên}}]({{url}}) — dùng cho …
