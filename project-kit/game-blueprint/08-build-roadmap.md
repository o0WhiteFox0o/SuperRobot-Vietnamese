# 08 — Lộ trình xây dựng game có chiều sâu

| Mốc | Mục tiêu | Ngưỡng đo được |
|---|---|---|
| G0 | Mô hình dữ liệu + validator | `validate_content.py` chạy sạch trên `examples/content`; test xanh |
| G1 | Lát cắt dọc: 1 scene, 3 đơn vị, 1 trận | Chơi từ opening tới victory; 0 lỗi tham chiếu |
| G2 | Pipeline nội dung | Thêm 1 nhân vật bằng JSON, không sửa code |
| G3 | Cốt truyện/sự kiện | ≥3 scene nối `next_scene`, 1 lựa chọn rẽ nhánh, đồ thị tới được |
| G4 | Bản địa hoá | 2 ngôn ngữ, fallback hoạt động, placeholder được kiểm |
| G5 | Pipeline ảnh | art manifest, mọi portrait/sprite có trong manifest, kiểm trong suốt |
| G6 | Mod/campaign | `mod.json` nạp được, campaign ngoài chạy không sửa lõi |

## Checklist "chiều sâu"
- [ ] ID ổn định, không dùng chỉ số mảng làm khoá công khai
- [ ] Bản ghi tĩnh tách khỏi trạng thái runtime; save chỉ lưu phần thay đổi
- [ ] Mỗi file JSON có `schema` + phiên bản
- [ ] Validator chặn trường lạ, ID trùng, tham chiếu gãy
- [ ] Nhiều tuyến truyện, biến có tên và phạm vi
- [ ] Lời thoại chiến đấu có điều kiện + ưu tiên
- [ ] Hệ số địa hình, nâng cấp, sĩ khí là dữ liệu
- [ ] Locale fallback + báo cáo lỗi thoại
- [ ] Art pack có manifest + hash
- [ ] Luật tuỳ chọn tách khỏi sửa nền

## Liên kết
Quy trình chung, template và scaffold: [`../README.md`](../README.md), [`../guide/`](../guide/). Bắt đầu nhanh: copy `examples/content`, chạy
`python tools/validate_content.py examples/content`.
