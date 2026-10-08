> **Ngôn ngữ / Language:** [Tiếng Việt](default-names.vi.md) · [English](default-names.en.md) · [中文](default-names.md)

# Hiển thị ba ngôn ngữ tên mặc định

27-09-2026. Người dùng xác định rằng tên của nhân vật chính, đối tác và quân đội **người chơi không được phép thay đổi**. Tên mặc định được hiển thị bằng tiếng Trung, tiếng Anh hoặc tiếng Nhật tùy theo ngôn ngữ đọc. Đối với một nửa tên đơn vị (bỏ qua lựa chọn đặt tên trong Chương 33, `3D5E` là dòng dưới cùng), hãy xem [Tên đơn vị cố định](fixed-unit-name.md).

## Luyện tập

** Dung lượng lưu trữ không thay đổi. ** Vùng tên (từ `8010F5F8`, xem [Trang xác nhận và lựa chọn nhân vật chính](native-name-entry.md)) và tên đơn vị `8010F698` chỉ lưu trữ glyph gốc, là phiên bản tiếng Nhật của tên mặc định ROM. Định dạng lưu trữ không thay đổi và cũng có thể đọc được bản lưu trữ gốc được viết bởi phiên bản được chuyển này. Thư viện phông chữ ROM chỉ có khoảng 2.000 ký tự tiếng Nhật và không thể lưu trữ các tên tiếng Trung như "Brad" trong đó. Sau khi không được phép thay đổi tên, thư viện phông chữ không cần phải mở rộng.

**Thay thế khi được hiển thị. **[`default_names.hpp`](../../src/native/game_adapter/default_names.hpp) `DefaultNames` xác định xem một trường có còn là tên mặc định hay không:

- Nếu nội dung tiếng Nhật trùng với một tên mặc định nào đó (không tính dấu cách ở đầu và cuối) thì hiển thị tên dịch sang ngôn ngữ đọc;
- Các nội dung khác được hiển thị nguyên trạng, giống nhau ở cả 3 ngôn ngữ. Điều này bao gồm tên được người chơi nhập trong phiên bản cũ cũng như các kho lưu trữ có tên đã được thay đổi trong trò chơi gốc;
- Họ, tên, biệt danh, tên đơn vị được đánh giá riêng biệt và chỉ so sánh các trường cùng loại;
- Tên đầy đủ được chia thành hai đoạn theo điểm giữa ban đầu "・" (glyph `0xE7`), được đánh giá riêng biệt và sau đó được kết nối bằng dấu phân cách của ngôn ngữ: Tiếng Trung "·", dấu cách tiếng Anh, tiếng Nhật "・". Do đó, tệp lưu cũ chỉ thay đổi họ sẽ được hiển thị là "Brad·ヒカリ";
- Văn bản tiếng Nhật sẽ luôn được trả về nguyên trạng, giống hệt từng chữ với văn bản gốc được vẽ trên màn hình trò chơi và bộ điều hợp hội thoại sẽ sử dụng nó để so sánh.

**Dữ liệu chỉ tồn tại ở một nơi. ** Tên dịch của tám người được lấy trực tiếp từ phân vùng `default_names` của [entry table](localization-terms.md) mà không cần tạo bảng khác: Bản ghi ROM 487–494 là tên viết tắt và biệt danh mặc định (`801C3744` được chặn từ tên: thường là 5 ô, アークライト 3 ô, getアーク); 495–502 là tên đầy đủ, với họ và tên được phân tách khỏi tên đầy đủ bằng dấu phân cách ngôn ngữ. `add_people()` được đăng ký từ thư mục ngôn ngữ trong `dialogue::configure`. Nó sẽ có hiệu lực sau khi thay đổi bảng nhập và chạy lại `apply_terms`. Khi tên đầy đủ của một ngôn ngữ nhất định không thể chia thành hai phần, họ và tên của ngôn ngữ này sẽ được hiển thị bằng tiếng Nhật và `default_names_unsplit` được ghi lại trong nhật ký sự kiện. Tên đơn vị マーチウィンド được đăng ký bởi `unit_name.cpp` và mục nhập giao diện là `unit_default_name`.

Phiên bản được chia sẻ là `names::default_names()` ([`native_name_entry.hpp`](../../src/host/native_name_entry.hpp)): được viết khi khởi động, ở chế độ chỉ đọc cho cả chuỗi trò chơi và chuỗi giao diện sau đó.

## Điểm truy cập

| Hiển thị vị trí | Cách đặt tên |
| --- | --- |
| Các phần giữ chỗ như `{HeroName}` trong các dòng (`<G:0124>`–`<G:012C>`) | `expand(ram, text, locale)` của `native_dialogue.cpp` được đọc và hiển thị theo ngôn ngữ thông qua `shown_name` |
| Diễn giả đối thoại, phê bình, chiến tuyến | `speaker_name`. Khi nhìn lại, mỗi ngôn ngữ lưu một bản và mỗi bản sử dụng tên mặc định của ngôn ngữ riêng |
| Tên trình điều khiển trên trang gốc: xác nhận trước chiến tranh, khả năng, のりかえ, tăng cường パーツ, biến đổi | `ui_text` → `record_text`: Chức năng trích xuất từ ​​gốc `8008CF14` thay thế các bản ghi 4407–4414, 4768–4775 bằng trường tên, máy chủ thực hiện tương tự rồi hiển thị theo ngôn ngữ |
| Lớp phủ văn bản của giao diện gốc (bản đồ chiến thuật, nhãn màn hình chiến đấu) | `label_text`, giống như trên |
| Trang lưu trữ và danh sách tải màn hình tiêu đề | `save_page.cpp`'s `slot_json`: Tiêu đề lưu trữ lưu trữ biệt hiệu của nhân vật chính |
| Đúc thẻ và trang xác nhận | `frontend.cpp` của `sync()` Thay đổi ngôn ngữ đọc trước khi bàn giao trang |

**Chuyển ngôn ngữ** (F7 hoặc Cài đặt) có hiệu lực ngay lập tức: các hộp thoại và phần phát lại được sắp xếp lại theo ngôn ngữ mới, mỗi trang gốc được xây dựng lại theo `relocalize` ban đầu và danh sách lưu trữ được xây dựng lại cùng với trang.

## Quá trình đúc

- **Phiên bản mới** (mặc định): Chọn nhân vật chính → Xác nhận → Bắt đầu câu chuyện, nhấp vào "Quay lại lựa chọn nhân vật" trên trang xác nhận để quay lại trang casting. Khi chọn một tuyến đường, máy chủ ghi tên mặc định của hai người giống như cách gửi tên ban đầu: đặt tên, họ và biệt hiệu vào bộ đệm chỉnh sửa `801C71E0`, sau đó điều chỉnh chức năng xác minh ban đầu `801C474C` cho nhân vật chính và đối tác, đồng thời sử dụng nó để viết ra bốn trường tên, họ, biệt hiệu và tên đầy đủ. Việc xác minh sẽ không từ chối tên mặc định; nếu bị từ chối, trang tên ban đầu sẽ được trả về và nhật ký sẽ ghi `defaults-rejected`.
- **Bản gốc** (Đặt "Lựa chọn nhân vật chính" để chọn phiên bản gốc): Sau "はい" ở trang casting gốc cũng ghi tên mặc định và `801C70F4 = 2`. Sau khi mờ dần, hãy chuyển thẳng đến phần mở đầu tuyến đường mà không cần vào trang chọn ký tự gốc. Đang ghi nhật ký `original-started`.
- `SRW64_NATIVE_NAME_ENTRY=0`: Giữ lại tất cả các trang của phiên bản gốc trong toàn bộ quá trình chạy, bao gồm cả những thay đổi về tên và chỉ được sử dụng để tái tạo đường cơ sở cũ.

Trang chỉnh sửa tên cũ, nhóm phương thức nhập, xác minh ký tự, `E000..` bản ghi văn bản giả và 23 mục nhập giao diện đã bị xóa.

## Lưu trữ tương thích

- **Old Archives**: Tên mặc định được tự động hiển thị theo ngôn ngữ đọc; tên đã thay đổi trước đó được hiển thị như hiện tại.
- **New Archive**: Nội dung nhất quán với bản gốc. Cả game gốc và phiên bản cũ đều có thể đọc được.
- **Giá**: Nếu tên viết tay ở phiên bản cũ giống hệt với tên mặc định thì cũng sẽ được coi là tên mặc định và sẽ được chuyển đổi theo ngôn ngữ.

## Dịch thuật

Từ danh sách tham gia (đã kiểm tra tên chính thức vào ngày 24/09/2026, tiếng Trung được viết ở Trung Quốc đại lục). Tám người này là 64 nhân vật gốc. Không có tên tiếng Trung phổ biến hoặc tiếng Trung giản thể chính thức và bản dịch hiện tại được giữ lại; những người nói tiếng Anh có cách viết thẻ chính thức năm 2001 (スクランブルギャザー) sử dụng cách viết chính thức và phần còn lại tuân theo bản dịch hiện tại.

| Tuyến đường | Nhân vật | Tiếng Nhật (tên, họ, biệt danh) | Tiếng Trung | Tiếng Anh |
| --- | --- | --- | --- | --- |
| Siêu nam | Nhân Vật Chính | ブラッド・スカイウィンド／ブラッド | Brad Skywind／Brad | Brad Skywind／Brad (chính thức) |
| | Đối tác | カーツ・フォルネウス／カーツ | Katz Forneus／Katz | Kurtz Forneus／Kurtz |
| Cô gái siêu nhân | Nhân Vật Chính | Manami Hamill／Manami (chính thức) | Manami Hamill／Manami (chính thức) |
| | Đối tác | Aisha Ridgemond／Aisha | Aisha Ridgemond／Aisha |
| Nam thật | Nhân Vật Chính | Arklight Blue／Ark (chính thức) | Arklight Blue／Ark (chính thức) |
| | Đối tác | Ehrlich Stasen／Ehrlich | Ehrlich Stasen／Ehrlich |
| Gái xinh | Nhân Vật Chính | Selain Meneth／Selain (chính thức) |
| | Đối tác | Rish Griswell／Rish | Rish Griswell／Rish |
| Tên quân | — | マーチウィンド | Gió Tháng Ba | Gió Tháng Ba |

## Xác minh

- **Kiểm tra thành phần:**
- `tests/native_content.cpp`: Khớp `DefaultNames` và `add_people`, dấu cách, tách tên đầy đủ, gốc tiếng Nhật, tên gốc không mặc định, thiếu bản dịch dự phòng.
- `tests/native_name_entry.cpp` (`make recomp-name-entry-test`): truyền văn bản và cắt bớt biệt hiệu, tải lại mẫu khi lộ trình thay đổi, quay lại trang gốc khi xác minh bị từ chối, quay lại trang xác nhận và bắt đầu, "はい" ban đầu bắt đầu trực tiếp.
- **Kịch bản máy thật:**
- `tools/recomp/verify/verify_shared_ui.py`: Xác nhận trang với tên song ngữ, cài đặt, thu phóng, quay lại casting, bắt đầu câu chuyện.
- `tools/recomp/debug/check_name_entry_ui_switch.py`: Ở phiên bản gốc "はい", nhập trực tiếp cốt truyện sau khi viết tên mặc định.
- `tools/recomp/debug/check_localization.py`: Tên mặc định trên các trang can thiệp thay đổi theo ngôn ngữ.
- **Chưa chạy trên máy thật. ** Ba tập lệnh trên chưa được chạy sau khi được viết lại vào ngày 27-09-2026.