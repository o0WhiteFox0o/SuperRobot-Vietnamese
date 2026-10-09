# 01 — 10 nguyên tắc tạo nên chiều sâu

Mỗi nguyên tắc dưới đây được quan sát trực tiếp trong SuperRobot, kèm "bằng chứng trong repo" để bạn thấy nó không phải lý thuyết.

## 1. Mọi kết luận gắn với bằng chứng và phạm vi bằng chứng
Không viết "đã chạy tốt". Viết **đã kiểm chứng cái gì, bằng cách nào, trên máy nào, ở phiên bản nào**.
- Mẫu câu: *"kết luận này đến từ kiểm tra tĩnh ngày X, **chưa chạy thật** trên nền tảng Y."*
- Repo: `docs/design/three-platform-port.md` mở đầu bằng đúng câu này.

## 2. Mỗi tài liệu có Ngày + Trạng thái
Tài liệu ghi *kết luận tại thời điểm đó*, không thay thế kết quả hiện tại. Nhãn chuẩn xem [03-doc-system.md](03-doc-system.md).
- Repo: dòng đầu `Date: 2026-09-21. Status: Implemented, ... two menus not yet verified`.

## 3. Luôn có mục "Chưa xác minh / Còn thiếu"
Phần này quý hơn phần "đã xong": nó là danh sách việc thật. Không được xoá để "trông hoàn chỉnh".
- Repo: hầu hết `native/*` kết thúc bằng "thực tế đã kiểm chứng + danh sách chưa kiểm chứng".

## 4. Phân tích tĩnh trước, chạm vào hệ thống sau
Hiểu hệ thống gốc (định dạng, luồng, bảng dữ liệu) bằng đọc/disassemble/đo đạc → mới thiết kế "tiếp quản". Ghi **địa chỉ/vị trí/ID cụ thể** để người sau tái kiểm được.
- Repo: `native-intermission-menu.md` §1–3 phân tích gốc, §4+ mới là phương án thay thế.

## 5. Giữ một đường xử lý có thẩm quyền (authoritative path)
Tăng tốc/rút gọn chỉ ở ranh giới đã chứng minh an toàn; không tự mô phỏng lại logic nghiệp vụ "cho nhanh". Khi so sánh, so từng trường trạng thái từ cùng checkpoint, liệt kê trường bị loại trừ.
- Repo: `mod-roadmap.md` — "Implementation constraints of combat and speed".

## 6. Mặc định bảo thủ, tuỳ chọn tách bạch
Bản cơ bản không đổi hành vi gốc. Mỗi sửa đổi là một công tắc độc lập, mặc định tắt, có ghi rõ ảnh hưởng tương thích dữ liệu/lưu trữ.
- Repo: "Original / Enhanced / Customized" và `base-fixes` (không có công tắc) vs `rule-fixes` (có công tắc).

## 7. Không "xoá tính năng để tuyên bố xong"
Điều kiện hoàn thành không được hạ để kịp tiến độ. Phần chưa an toàn được **liệt kê là chưa làm**.
- Repo: ràng buộc P0 "no deletion of features to declare completion".

## 8. Truy nguyên nguồn (provenance) và khoá danh tính đầu vào
Mọi đầu vào ngoài repo: ghi kích thước, hash, phiên bản, nguồn, và **độ lệch so với nguồn gốc** cùng cách đã kiểm.
- Repo: `docs/guide/provenance.md` (SHA-256, commit nguồn, 109 nhóm ánh xạ lệch đã đối chiếu từng cái).

## 9. Test bảo vệ chính tài liệu
Link tương đối phải phân giải được, đường dẫn trong backtick phải tồn tại, mọi doc phải có trong chỉ mục. Tài liệu cũng là mã cần CI.
- Repo: `tests/test_docs.py` (3 test). Kit có bản tổng quát: [scaffold/tests/test_docs.py](../scaffold/tests/test_docs.py).

## 10. Giai đoạn có ngưỡng nghiệm thu, không có lịch ảo
Mỗi giai đoạn (M0, M1, X0…) có **bảng gói công việc ↔ ngưỡng hoàn thành**. Chưa đo được thì nói chưa ước lượng thời gian; làm vài "lát dọc" (vertical prototype) trước rồi mới ước.
- Repo: `mod-roadmap.md` §3 — "calendar construction period will not be reported for the time being".

---

> [!IMPORTANT]
> Quy tắc vàng: **nếu một câu trong tài liệu không thể trả lời "bằng chứng ở đâu?", hãy hạ nó thành giả thuyết hoặc đưa vào danh sách chưa xác minh.**
