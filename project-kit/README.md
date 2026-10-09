# Project Kit — Bộ khung thiết kế dự án có chiều sâu

Bộ khung này được **rút ra từ cách dự án SuperRobot (srw64-recomp) thực sự được làm**: 111 tài liệu kỹ thuật, ~445 test, mọi kết luận đều có bằng chứng, ngày tháng và trạng thái. Mục tiêu: dự án mới nào cũng khởi đầu với cùng kỷ luật đó, thay vì phải học lại từ đầu.

## Dùng như thế nào

```powershell
# Tạo khung cho dự án mới (sao chép cấu trúc, mẫu tài liệu, test kiểm tra docs)
python project-kit/scaffold/init_project.py D:\Projects\MyNewProject --name "My New Project"
```

Sau đó đọc theo thứ tự:

| # | Tài liệu | Trả lời câu hỏi |
| --- | --- | --- |
| 1 | [guide/01-principles.md](guide/01-principles.md) | Vì sao dự án này "sâu"? 10 nguyên tắc cốt lõi |
| 2 | [guide/02-repo-structure.md](guide/02-repo-structure.md) | Thư mục nào chứa gì |
| 3 | [guide/03-doc-system.md](guide/03-doc-system.md) | Hệ thống tài liệu, chỉ mục, nhãn trạng thái, đa ngôn ngữ |
| 4 | [guide/04-phases-and-gates.md](guide/04-phases-and-gates.md) | Chia giai đoạn, cổng nghiệm thu |
| 5 | [guide/05-verification-ladder.md](guide/05-verification-ladder.md) | Thang kiểm chứng: tĩnh → test → chạy thật |
| 6 | [guide/06-new-project-checklist.md](guide/06-new-project-checklist.md) | Checklist ngày 0, tuần 1, mỗi tính năng, mỗi bản phát hành |

## Mẫu tài liệu (`templates/`)

| Mẫu | Dùng khi |
| --- | --- |
| [design-doc.md](templates/design-doc.md) | Một thiết kế/kế hoạch có phạm vi, giai đoạn, ngưỡng nghiệm thu |
| [roadmap.md](templates/roadmap.md) | Lộ trình sản phẩm M0–Mn, ưu tiên hiện tại, ngoài phạm vi |
| [feature-doc.md](templates/feature-doc.md) | Tính năng đã/đang cài: phân tích → thiết kế → xác minh → chưa xác minh |
| [analysis-doc.md](templates/analysis-doc.md) | Phân tích tĩnh một hệ thống/định dạng/dữ liệu có sẵn |
| [research-spike.md](templates/research-spike.md) | Khảo sát khả thi có giới hạn thời gian, kết luận rõ |
| [decision-record.md](templates/decision-record.md) | Ghi quyết định kiến trúc (ADR) và lý do |
| [bug-register.md](templates/bug-register.md) | Sổ lỗi: nguồn tin, nguyên nhân đã xác nhận, cách tái hiện |
| [verification-record.md](templates/verification-record.md) | Biên bản kiểm chứng: cấu hình, bằng chứng, giới hạn |
| [provenance.md](templates/provenance.md) | Đầu vào cục bộ, hash, nguồn tham khảo, độ lệch so với nguồn |
| [port-plan.md](templates/port-plan.md) | Chuyển nền tảng/công nghệ: khảo sát chặn, giai đoạn X0–Xn |
| [release-plan.md](templates/release-plan.md) | Phát hành: gói, kênh, điều kiện, quy trình |
| [docs-index.md](templates/docs-index.md) | `docs/README.md` — chỉ mục trung tâm |

> [!NOTE]
> Bộ khung **không phụ thuộc** vào chủ đề recomp/game. Các ví dụ lấy từ SuperRobot chỉ để minh hoạ; thay bằng lĩnh vực của bạn.
