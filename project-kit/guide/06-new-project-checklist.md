# 06 — Checklist dự án mới

## Ngày 0 — Khởi tạo
- [ ] Chạy `init_project.py` để có khung thư mục + mẫu + `test_docs.py`.
- [ ] Điền `README.md` gốc: dự án là gì, **không phải là gì**, đường vào nhanh.
- [ ] Viết [roadmap](../templates/roadmap.md) bản đầu: **ưu tiên hiện tại** và **ngoài phạm vi**.
- [ ] Tạo [provenance](../templates/provenance.md): mọi đầu vào ngoài repo (hash, phiên bản, nguồn).
- [ ] Một lệnh dựng (`make`/`just`) chạy từ clone mới; CI chạy đúng lệnh đó.
- [ ] Bật `test_docs` trong CI.

## Tuần 1 — Hiểu trước, làm sau
- [ ] 2–5 tài liệu `analysis/` về hệ thống/dữ liệu nền (có vị trí/ID/địa chỉ cụ thể).
- [ ] 1 [research-spike](../templates/research-spike.md) cho rủi ro lớn nhất.
- [ ] ADR cho 3 quyết định kiến trúc đầu tiên (ngôn ngữ, khung, lưu trữ).
- [ ] Chọn **2–3 lát dọc** để chứng minh luồng xuyên suốt.
- [ ] Giao diện gỡ lỗi/ghi nhận trạng thái tối thiểu để có thể kiểm chứng tự động.

## Mỗi tính năng
- [ ] ID trong roadmap + dòng "Hành vi phải chứng minh".
- [ ] Tài liệu `features/` từ [feature-doc](../templates/feature-doc.md): phân tích → thiết kế → xác minh → **chưa xác minh**.
- [ ] Có công tắc nếu đổi hành vi gốc; mặc định tắt; ghi ảnh hưởng tương thích dữ liệu.
- [ ] Test thành phần + (nếu được) kịch bản chạy thật có điều khiển bằng script.
- [ ] Cập nhật chỉ mục `docs/README.md`; `test_docs` xanh.

## Mỗi lỗi
- [ ] Vào [bug-register](../templates/bug-register.md): nguồn tin, mức chắc chắn, cách tái hiện.
- [ ] Nguyên nhân gốc xác nhận bằng bằng chứng, không đoán.
- [ ] Sửa → bảng so sánh gốc vs sửa → chuyển thành "sửa cơ bản" hoặc "tuỳ chọn" theo ảnh hưởng.

## Mỗi bản phát hành
- [ ] [release-plan](../templates/release-plan.md): gói, kênh, điều kiện cổng, quy trình thủ công.
- [ ] Ghi rõ **phần đã/ chưa** được kiểm chứng; không ghi quá mức.
- [ ] Nhãn trạng thái của các tài liệu liên quan được cập nhật.
- [ ] Bản dịch (nếu có) được đồng bộ hoặc đánh dấu lỗi thời.

## Hằng tháng — Vệ sinh tri thức
- [ ] Rà `Ngày/Trạng thái` của tài liệu cũ: chuyển `Lịch sử` nếu không còn đúng.
- [ ] Rà danh sách "chưa xác minh": mục nào đã có bằng chứng → đóng; mục nào mới → thêm.
- [ ] Rà `docs/README.md`: mục đích → tài liệu còn đúng không?
