> **Ngôn ngữ / Language:** [Tiếng Việt](README.vi.md) · [English](README.en.md) · [中文](README.md)

# Cẩm nang Hướng dẫn Tiến trình & Yếu tố Ẩn

`srw64-flow-guide.html` là cẩm nang hướng dẫn ngoại tuyến tệp đơn dành cho người chơi. Tệp hỗ trợ đa ngôn ngữ: có thể chuyển đổi ngôn ngữ ở góc trên bên phải thanh thẻ tab; ngôn ngữ mặc định lưu theo lựa chọn trước hoặc ngôn ngữ trình duyệt, cũng có thể truyền tham số URL `?lang=vi|zh-Hans|ja|en`.

Nội dung bao gồm: Sơ đồ tiến trình, yếu tố ẩn, bảng lệnh tinh thần, kỹ năng phi công, năng lực robot, linh kiện cường hóa, hiệu ứng tình yêu, nâng cấp & kế thừa, vũ khí bổ sung, đòn tấn công hợp thể, liên kết Game Boy Link Battler... Trang web đã nhúng sẵn style và mã script, không phụ thuộc vào internet, mở trực tiếp bằng trình duyệt.

## Căn cứ dữ liệu

Mọi nội dung đều được phân tích trực tiếp từ kịch bản màn chơi và mã nguồn ROM tiếng Nhật của trò chơi; thông tin cộng đồng Akurasu Wiki chỉ dùng để tham khảo đối chiếu.
Nội dung văn bản sử dụng 3 biểu tượng đánh dấu: "Khác với Akurasu", "Akurasu chưa ghi nhận", "Chưa kiểm chứng trên máy thật" (trong dữ liệu ký hiệu là `{≠}`, `{+}`, `{?}`). Căn cứ kỹ thuật xem tại:

- [Yếu tố ẩn, thuyết phục & phân nhánh lộ trình](../docs/gameplay/hidden-elements.md)
- [Công thức tính toán trận đấu](../docs/gameplay/battle-formulas.md), [Kế thừa nâng cấp](../docs/gameplay/upgrade-inheritance.md), [Giới hạn nâng cấp](../docs/gameplay/upgrade-limits.md), [Liên kết Link Battler](../docs/gameplay/link-battler.md)
- [Lệnh kịch bản màn chơi](../docs/script/stage-script-exploration.md)

## Dữ liệu

Nằm trong thư mục `data/<ngôn ngữ>/` với 3 tệp tin, cấu trúc và ID đồng nhất:

- `progression.json`: Thẻ màn chơi trong sơ đồ tiến trình
- `hidden-elements.json`: Yếu tố ẩn, phân nhánh lộ trình và quy tắc thuyết phục
- `reference.json`: Thẻ dữ liệu tra cứu

Tên nhân vật, robot, vũ khí, linh kiện, tinh thần lấy từ thư mục ngôn ngữ (`content/locales/`).

Sau khi chỉnh sửa dữ liệu, tạo lại trang bằng lệnh:

```bash
python3 tools/content/build_guide.py
```

