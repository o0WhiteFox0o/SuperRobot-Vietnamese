> **Ngôn ngữ / Language:** [Tiếng Việt](native-dialogue-runtime-hd.vi.md) · [English](native-dialogue-runtime-hd.en.md) · [中文](native-dialogue-runtime-hd.md)

# Hộp thoại viền HD

Ấn bản đầu tiên vào ngày 2026-09-09, được vẽ lại theo thiết kế ban đầu vào ngày 24-09-2026. Đường viền của các hộp thoại cốt truyện được thay đổi thành các lát cắt có độ phân giải cao, vẫn được thay thế bằng hàm băm kết cấu RT64. Vị trí của hộp, độ trong suốt của tấm đáy văn bản và thứ tự vẽ văn bản đều giống như trong trò chơi.

Trang này ban đầu ghi lại hai thử nghiệm ban đầu không còn nằm trong lộ trình triển khai hiện tại:

- Nền độ phân giải cao của bản đồ Châu Âu trong Chương 1 (57 ô tài nguyên 5604): hiện tại toàn bộ khu vực được bao phủ bởi [Story World Map HD](native-worldmap-regions-hd.md), hãy xem [World Map HD](native-worldmap-hd.md) để biết phương pháp.
- Biểu tượng màu xanh lam của tên: Đường dẫn hội thoại biểu tượng cũ đã bị xóa vào ngày 24-09-2026. Hội thoại hiện tại được vẽ bởi lớp văn bản gốc, xem [Giao diện người dùng đối thoại](native-dialogue-ui.md).

## Tài nguyên biên giới HD

Mục tiêu là ROM **Tài nguyên 1296**, 4.104 byte, tiêu đề là dải CI4 / 512×16. Dữ liệu được giải nén hoàn chỉnh khớp duy nhất với RDRAM chụp hiện tại `0x2B8598`. Hộp thoại sử dụng 13 lát cắt 16×16 khác nhau, được sắp xếp liên tục thành một cửa sổ logic 192×64.

[`dialogue_frame_asset.py`](../../tools/hd_ai/dialogue_frame_asset.py) được vẽ lại theo thiết kế ban đầu và mỗi lát được thay đổi thành 64×64; tất cả 13 giá trị băm RT64 v5 được tính toán đều bằng kết xuất TMEM thực (được kiểm tra từng cái một khi đưa ra `--capture`, thường được tính trực tiếp từ dữ liệu ROM và bảng màu cố định).

- **Dải băng màu**: Khung ban đầu là dải băng bốn lớp bên ngoài hình chữ nhật bo tròn. Ánh sáng đến từ phía trên bên trái: màu trắng, bạc, xám ở phía trên và bên trái, xám nhạt, xám, xám đậm ở phía dưới và bên phải, và một đường màu xanh đậm ở phần trong cùng. Khi vẽ lại, toàn bộ khung hình được vẽ một lần theo hình học, các bước pixel được thay đổi thành các góc được bo tròn mịn, các ranh giới sáng và tối được chuyển dọc theo các đường chéo của bốn góc, sau đó được cắt theo vị trí ban đầu.
- **Các miếng nhô ra và dải đèn xanh**: Phiên bản gốc có một số miếng nhô lên nhỏ ở viền trên và dưới, có gắn dải đèn xanh bên trong; có dải đèn dọc ở góc dưới bên trái và góc trên bên phải. Các lát cắt trên và dưới khác nhau chỉ khác nhau ở vị trí của các đồ trang trí này. Khi vẽ lại, hãy đọc các phần nhô ra và thanh ánh sáng từ các hàng của mỗi lát cắt ban đầu và vẽ chúng thành các thanh ánh sáng thủy tinh với các vòng ngoài, độ dốc và điểm nổi bật màu xanh đậm; các thanh ánh sáng trên các lát cắt được tiếp tục ở cả hai bên.
- 24-09-2026 Phiên bản trước đó là đường viền vát màu bạc được sơn mã với một vòng tròn đầy đủ các đường bên trong màu xanh coban, bốn góc được cắt thành 45° và tất cả các lát cắt cạnh trên đều sử dụng cùng một hình vẽ. Người dùng cho rằng "vát màu xanh" thật lạ và đã thay đổi nó thành như bây giờ. Các ảnh cũ được để lại ở `assets/hd-ai/dialogue-runtime/v3/`, còn bản ghi bản dựng và bản xem trước phiên bản mới nằm ở `v4/`.
- Dấu bốn góc màu lục lam của hộp trò chuyện hiện tại (được vẽ trên lớp văn bản gốc, xem [Dấu đọc](native-reading-indicators.md)) cũng được thay đổi từ góc xiên 45° thành góc tròn phù hợp với đường viền.

Vị trí hình học của các tài nguyên đường viền, độ trong suốt của nền văn bản và thứ tự vẽ văn bản tuân theo trò chơi. Nó được vẽ riêng biệt với bản đồ nền và văn bản mà không sử dụng toàn bộ ảnh chụp màn hình để bao phủ trò chơi. Phạm vi xác minh là cuộc đối thoại mở đầu hiện tại; việc sử dụng các tài nguyên này trong các giao diện khác chưa được kiểm tra từng cái một.

## Xây dựng lại

13 lát cắt được ghi vào gói bản đồ thế giới `worldmap-surfaces/pack-v5`, `--art` và SHA-256 của 13 mục này trong danh sách nghệ thuật được cập nhật cùng lúc; khi cung cấp `--capture`, tải TMEM thực được sử dụng để kiểm tra từng giá trị băm:

```sh
PYTHONPATH=src:. .venv/bin/python -B tools/hd_ai/dialogue_frame_asset.py \
  --pack assets/hd-ai/worldmap-surfaces/pack-v5 --output build/hd-ai/dialogue-frame \
  --art content/art/stage1-hd.json
```

Các bản xem trước và bản dựng của phiên bản hiện tại được ghi lại trong `assets/hd-ai/dialogue-runtime/v4/`.