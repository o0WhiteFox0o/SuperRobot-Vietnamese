# Chỉ mục tài liệu kỹ thuật

Cập nhật: {{YYYY-MM-DD}}. {{Một đoạn: dự án đang ở đâu, cái gì đã/ chưa xong, nền tảng được hỗ trợ.}} Tài liệu chia theo chủ đề; tài liệu có ngày ghi **kết luận tại thời điểm đó**; link tới `build/` chỉ tồn tại cục bộ.

| Thư mục | Nội dung |
| --- | --- |
| [`guide/`](#sử-dụng-và-phát-triển-guide) | Dùng, dựng, phát triển, gỡ lỗi, nguồn gốc đầu vào |
| [`design/`](#kế-hoạch-và-thử-nghiệm-design) | Lộ trình, kiến trúc, khảo sát, chuyển nền tảng |
| [`analysis/`](#phân-tích-hệ-thống-gốc-analysis) | Phân tích tĩnh hệ thống/định dạng/dữ liệu |
| [`features/`](#tính-năng-features) | Tính năng đã/đang cài kèm xác minh |
| [`quality/`](#chất-lượng-quality) | Sổ lỗi, sửa lỗi, biên bản kiểm chứng |
| [`decisions/`](#quyết-định-decisions) | ADR |

## Bắt đầu từ đây

| Mục đích | Tài liệu |
| --- | --- |
| Chạy thử, phím, thao tác | [{{…}}](guide/{{…}}.md) |
| Dựng, trách nhiệm mã nguồn, kiểm tra | [{{…}}](guide/{{…}}.md) |
| Đã biết lỗi gì, sửa gì, bật tắt thế nào | [{{sổ lỗi}}](quality/{{…}}.md) → [{{sửa}}](quality/{{…}}.md) |
| Phạm vi hiện tại và sắp tới | [{{lộ trình}}](design/{{…}}.md) |

## Sử dụng và phát triển (guide/)

| Tài liệu | Nội dung |
| --- | --- |
| [{{…}}](guide/{{…}}.md) | |

## Kế hoạch và thử nghiệm (design/)

Các tài liệu này ghi cấu hình và nghiệm thu tại thời điểm đó; không thay thế kết quả hiện tại.

| Tài liệu | Nội dung |
| --- | --- |

## Phân tích hệ thống gốc (analysis/)

| Tài liệu | Nội dung |
| --- | --- |

## Tính năng (features/)

| Tài liệu | Nội dung |
| --- | --- |

## Chất lượng (quality/)

| Tài liệu | Nội dung |
| --- | --- |

## Quyết định (decisions/)

| Tài liệu | Nội dung |
| --- | --- |

## Tầng kiểm chứng

Kiểm tra tĩnh, test thành phần, replay cố định, chạy sản phẩm thật, chạy trên hệ thống tham chiếu và kiểm tra thủ công **có phạm vi riêng**. "Có ảnh chụp" hoặc "exit code 0" không tự động nghĩa là cả quy trình đã nghiệm thu. `tests/test_docs.py` kiểm tra mọi link Markdown và mọi đường dẫn repo được nhắc tới.

