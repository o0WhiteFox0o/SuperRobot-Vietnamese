> **Ngôn ngữ / Language:** [Tiếng Việt](story-reader.vi.md) · [English](story-reader.en.md) · [中文](story-reader.md)

# trạm xem xét lô đất

2026-09-12. Theo phương pháp đối thoại liên tục, hình đại diện nhân vật, điều hướng chương, tìm kiếm toàn văn bản và định vị từng câu của trạm đánh giá Z, tập lệnh gốc được trích xuất bởi SRW64 được sử dụng để tạo trang chỉ đọc.

## Bắt đầu và đọc

```sh
.venv/bin/python -B tools/content/extract_original.py
python3 -B tools/data_viewer/serve.py --port 59110
```

Mở <http://127.0.0.1:59110/story.html#scene=1>. Danh mục bao gồm 142 cảnh và 34.369 câu thoại; các kịch bản được chia sẻ được tính riêng trong mỗi cảnh và không bằng số lượng văn bản độc lập hoặc số cấp độ có thể chơi được.

- Tìm kiếm theo tiêu đề hoặc số cảnh ở cột bên trái; chương trước/tiếp theo di chuyển theo chỉ mục cảnh và liên kết "Từ/Chuyển tới" bên dưới tiêu đề xuất phát từ tập lệnh gốc `3D4B`.
- Tìm kiếm toàn văn hỗ trợ văn bản tiếng Nhật, người nói và số văn bản, ít nhất hai ký tự; có thể được giới hạn trong chương này. Nếu có hơn 200 mục, tổng số sẽ được hiển thị và nhắc thu hẹp phạm vi. Số bị cắt sẽ không được coi là tổng số.
- Nhấp vào "Đi" bên cạnh kết quả tìm kiếm hoặc câu để nhận liên kết có thể sao chép, chẳng hạn như `#scene=1&line=0019c1b0-1c`. Danh tính bao gồm cảnh, địa chỉ ROM sự kiện, độ lệch lệnh và không dựa vào số dòng danh sách.
- Bạn có thể lọc theo phần mở đầu, cấu hình ban đầu, sự kiện chiến trường, kết thúc và chuyển thẳng đến các sự kiện trong chương này. Tiêu đề sự kiện chứa bản tóm tắt các điều kiện kích hoạt.
- Việc lọc lộ trình của bốn nhân vật chính chỉ kiểm soát các đoạn văn của nhân vật chính. Các đoạn thông thường và các chi đã chọn vẫn được giữ lại; Người nói tương đối có lộ trình chưa được xác định sẽ hiển thị danh sách ứng cử viên và dấu chấm hỏi theo mặc định và hình đại diện tương ứng chỉ được hiển thị sau khi chọn lộ trình tương thích.
- Tên xen kẽ giữa màu xanh và màu cam khi người nói thay đổi. Có thể điều chỉnh hình đại diện, điều kiện và mẹo thực hiện, số gốc và kích thước phông chữ; trình duyệt lưu tùy chọn đọc và vị trí cuối cùng.

Các ngắt dòng văn bản gốc được giữ lại và việc lật trang được đánh dấu bằng `▸`; tên động sử dụng phần giữ chỗ.

Bắt đầu từ 23/09/2026, bạn có thể chọn tiếng Trung, tiếng Anh hoặc cả hai trong phần "Dịch", bản dịch sẽ hiển thị dưới mỗi câu gốc và bản dịch sẽ hiển thị dưới tiêu đề chương. Nguồn được đánh dấu trước mỗi bản dịch: nhập, viết tay, dịch máy, duyệt lại, không đạt; lý do cần xem xét và câu hỏi dịch máy được đặt trong dấu nhắc di chuột. Dữ liệu dịch được ghi từ `tools/translation/export_review.py` tới `assets/original-data/translations/<locale>.json`. Bản nháp cũng có thể được đọc và dịch trước khi được sáp nhập vào thư mục ngôn ngữ. Để biết quy trình, hãy xem [Kế hoạch Trung Quốc hóa toàn văn](../design/translation-plan.md). Việc chạy lại `extract_original.py` sẽ thay thế hoàn toàn `assets/original-data/` và sau đó bạn cần chạy lại `export_review.py`. Trang này chỉ có thể được đọc và không thể sửa đổi hoặc gửi để xem xét trực tuyến. Không có hệ thống tài khoản.

## Ranh giới đọc

Các sự kiện diễn ra theo thứ tự đầu vào và đường dẫn thực hiện thực tế của trò chơi vẫn chưa được tính toán. Các lượt, thất bại, biến số và kết quả lựa chọn có thể loại trừ lẫn nhau và trang sẽ giữ lại chúng cùng một lúc. Lựa chọn tuyến đường cũng không có nghĩa là tất cả các điều kiện cấp độ đã được mô phỏng. Khi định vị một câu bị ẩn trên tuyến đường hiện tại, trang sẽ khôi phục tất cả các đoạn tuyến đường và lời nhắc.

Nhân vật chính đã được xác định dựa trên cơ sở tĩnh trong tập này sẽ không được đổi tên bằng tùy chọn tuyến đường dành cho người đọc; tuyến đường đã chọn chỉ được sử dụng cho danh tính tương đối chưa được xác định. Hướng dẫn đầy đủ, văn bản gốc và bản đồ có thể được nhập vào bản đồ dữ liệu để xác minh từ trang.

## Thực hiện và kiểm tra

- `src/srw64_native/original_story.py`: Xây dựng các sơ đồ và dòng tìm kiếm theo từng cảnh, bảo toàn danh tính nguồn và các ứng cử viên của diễn giả.
- `tools/content/extract_original.py`: Tạo `story/index.json`, 142 cảnh JSON, `story/search.json`; dữ liệu tìm kiếm có dung lượng khoảng 5 MB, được tải và lưu vào bộ nhớ đệm trong lần tìm kiếm đầu tiên.
- `tools/data_viewer/web/story.html`, `story.css`, `story.js`: Đọc trang. `story-state.js` Các hàm thuần túy cung cấp tuyến đường, người nói, điểm cố định và tìm kiếm.
- `tests/test_original_story.py`: Kiểm tra ánh xạ nguồn đầy đủ của ROM thực, loa, tên động và chỉ mục tìm kiếm.
- `tests/story_reader.mjs`: liên kết ổn định, hình đại diện tương đối của tuyến đường, ranh giới bộ lọc, phạm vi tìm kiếm và số lần cắt bớt.

```sh
PYTHONDONTWRITEBYTECODE=1 make check
node --test tests/story_reader.mjs
```

Kiểm tra tĩnh và xác minh trình duyệt chỉ chứng minh rằng trang được trích xuất và đọc chứ không tương đương với việc xác minh việc thực thi tập lệnh trò chơi. Để biết phương pháp cụ thể của giai đoạn tiếp theo, hãy xem [Xác nhận ngữ nghĩa hướng dẫn còn lại](script-semantics-confirmation.md).