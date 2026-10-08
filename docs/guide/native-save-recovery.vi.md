> **Ngôn ngữ / Language:** [Tiếng Việt](native-save-recovery.vi.md) · [English](native-save-recovery.en.md) · [中文](native-save-recovery.md)

# Lựa chọn lịch sử lưu trữ gốc và khôi phục tệp giải phóng mặt bằng

2026-09-12. Vòng này thực hiện những gì là sàng lọc tính toàn vẹn, khôi phục rõ ràng và xác minh việc đọc các bản sao SRAM lịch sử; nó không phải là một định dạng lưu trữ trò chơi mới cũng như không tự động lưu các nút an toàn hoặc lưu trữ tức thời bất cứ lúc nào.

## Lối vào của người chơi

```sh
# 列出统一原生入口的历史副本和冻结初始备份；不启动游戏、不创建试玩目录。
.venv/bin/python tools/recomp/run/play_native.py \
  --profile config/recomp/profiles/play-profile.json --list-saves

# 恢复指定会话。ID 使用上一步列出的完整时间戳。
.venv/bin/python tools/recomp/run/play_native.py \
  --profile config/recomp/profiles/play-profile.json --restore-session SESSION_ID

# 显式回到冻结的第一话通关备份。
.venv/bin/python tools/recomp/run/play_native.py \
  --profile config/recomp/profiles/play-profile.json --restore-session initial
```

`--new-game`, `--restore-session`, `--list-saves` loại trừ lẫn nhau. Nếu không được chỉ định, bản sao lịch sử đầu tiên vượt qua quá trình kiểm tra tính toàn vẹn sẽ được chọn từ mới nhất đến cũ nhất; nếu không có sẵn, bản sao lưu ban đầu với thông báo cố định trong cấu hình sẽ được thử. Lý do bỏ qua và lựa chọn thực tế được in. Nếu phiên được chỉ định không hợp lệ, nó sẽ bị từ chối trực tiếp mà không lặng lẽ chọn tiến trình khác; nếu không có nguồn xác minh được, nó sẽ yêu cầu kiểm tra lịch sử hoặc trò chơi mới rõ ràng.

Các thử nghiệm hồ sơ hợp nhất, tiếng Nhật thông thường, mô hình gốc và mô hình ROM tiếp tục sử dụng các thư mục lịch sử hiện có tương ứng của chúng. Nhật Bản, Trung Quốc và Original/HD có chung danh tính JP trong cùng một hồ sơ; danh tính của các thử nghiệm mô hình ROM được kiểm tra riêng. Cả hai mục nhập `.command` đều sử dụng tham số dự án `.venv` và chuyển tiếp.

## Ranh giới xác minh và bảo vệ

Triển khai: `src/srw64_native/save_history.py`; Truy cập: `tools/recomp/run/play_native.py` và `run_host_probe.py`.

Các phiên ứng viên phải có báo cáo chạy hoàn chỉnh và có thể nhận dạng, mã thoát máy chủ 0, phiên bản ROM phù hợp với SHA-256 cũng như kích thước và bản ghi tóm tắt hiện có của SRAM cuối cùng. Hiện tại, chỉ chấp nhận cấu hình trò chơi gốc; các bản ghi liên quan đến cấu hình trò chơi không được hỗ trợ sẽ không được tự động khôi phục. Tệp phải có kích thước chính xác là 32 KiB, phù hợp với bản tóm tắt bản ghi và không phải tất cả số 0/tất cả FF. Các báo cáo bị thiếu/bị hỏng, các lần thoát bất thường, nội dung có cùng độ dài bị hỏng, bị cắt bớt, xác định sai và các kho lưu trữ ngoài giới hạn/được liên kết sẽ bị từ chối. Các thư mục biên soạn nội dung và các bản sao đầu vào không tham gia vào việc sắp xếp lịch sử.

**Tài liệu này phù hợp với các hồ sơ hiện có và không chứng minh rằng mọi vị trí trong trò chơi đều hợp lệ. ** Vòng này không phân tích tổng kiểm tra nội bộ SRAM của trò chơi gốc và cũng không thể sử dụng thông báo mới được tính toán để xác nhận các tệp không có bản ghi hiện có. Tải/Tiếp tục trong trò chơi vẫn được trò chơi gốc đọc và xác minh; một quy trình riêng biệt được thiết lập khi cần sửa chữa hoặc nhập các tệp cũ chưa được ghi.

Sau khi chọn, hãy kiểm tra lại bản tóm tắt, ghi các byte tương tự vào `.source.sram` bên cạnh phiên mới ở chế độ tạo độc quyền, xóa vào đĩa trước khi khởi động máy chủ; `.save-selection.json` ghi lại nguồn ban đầu, lý do lựa chọn và danh sách bỏ qua. `--save-sha256` của thăm dò xác minh thông báo hiện có này và tiếp tục duy trì các bước kiểm tra sau xây dựng đối với các thay đổi đầu vào. Trò chơi chỉ ghi thư mục chạy mới của riêng nó và các phiên ban đầu cũng như bản sao lưu cố định không bị ghi đè hoặc xóa.

Các bản sao nguồn hoặc bản ghi lựa chọn bị bỏ lại do gián đoạn khởi động sẽ không phải là ứng cử viên cho quá trình khôi phục tự động tiếp theo. Chúng là hồ sơ kiểm tra về dữ liệu đầu vào khôi phục, không phải "cam kết nguyên tử của lần lưu trò chơi mới"; bộ sưu tập lưu nút an toàn và loại bỏ luân phiên chưa được triển khai.

## Đọc khi khởi động nguội thực tế

Bằng chứng: [intermission-cold-1/reload-verification.json](../../build/recomp/save-recovery-check/intermission-cold-1/reload-verification.json). Sử dụng cùng ROM JP Rev 0, profile tiếng Nhật/bản gốc, bản sao SRAM độc lập, im lặng xuyên suốt.

Tệp bị đóng băng ban đầu là `build/recomp/gfx-probes/first-map-turn5-reload-1/stage1-clear-turn7.sram` và bản tóm tắt là `0c6ded15fdf60c6b0064b2260a335d17a4ff77386d14d634bfd7d3bcb8de7484`.

Quá trình thực tế: Khởi động nguội → Tải tiêu đề → Hộp mực ROM → Lưu trữ 1 → Xác nhận → Chuẩn bị → Khả năng trình điều khiển → Chi tiết Manami → Thoát bình thường.

| Vị trí quan sát | Đã kiểm tra kết quả | màn hình GPU |
| --- | --- | --- |
| Đọc danh sách vị trí | Chương 1 RAR RÀNG, Manami cấp 2, tổng số vòng 7, quỹ 14.500 | `present-2460.png` |
| Menu bảo trì sau khi phục hồi thực tế | Chương 1 RÕ RÀNG, tổng vòng 7, kinh phí 14.500 | `present-3000.png` |
| Chi tiết trình điều khiển được phục hồi | Manami Hamill, cấp 2, sức mạnh 100, SP 102/102 | `present-3960.png` |

Tất cả ba cảnh đều đã được xem, hàm băm và siêu dữ liệu được ghi lại trong tệp bằng chứng được đề cập ở trên. Mã thoát của máy chủ là 0; tất cả 4 luồng trò chơi đều được tham gia và số lần quan sát trước và sau khi RDRAM được phát hành là 0. Tệp bị đóng băng ban đầu, bản sao nguồn được chuyển đến máy chủ và bản tóm tắt SRAM khi kết thúc quá trình chạy đều giữ nguyên giá trị ban đầu của chúng. Không có quyền mua mod, lưu lại hoặc truy cập vào các tập thứ hai.

`config/recomp/inputs/load-intermission-check.json` được xuất từ bản ghi đầu vào VI đã được xác nhận thực tế của vòng này và có thể được sử dụng cho các lần chạy lại tiếp theo (nên sử dụng `--vis 9000`). Những gì được chấp nhận trong vòng này là khởi động nguội và kiểm soát chạy thực tế; đầu vào cố định đã xuất chưa được phát lại riêng biệt và không thể được đánh dấu là đã xác minh để phát lại xác định. Báo cáo chạy sẽ giữ lại tập lệnh đầu vào ban đầu và tất cả các sự kiện kiểm soát được áp dụng.

## Kiểm tra và công việc còn lại

- `make check`: Đã vượt qua 108 bài kiểm tra Python, kiểm tra tổng hợp và phần phụ thuộc. 10 thử nghiệm mới bao gồm khôi phục bản sao cũ và mới, từ chối khôi phục rõ ràng, kiểm tra báo cáo/danh tính, khoảng trống, liên kết tượng trưng, ​​​​đóng băng nguồn, xác minh thông báo thứ cấp, danh sách chỉ đọc và truyền tham số khởi động.
- Máy chủ gốc sử dụng cùng một tệp nhị phân đã được xác minh ở vòng trước và thực sự hoàn thành giai đoạn khởi động nguội của vòng này; không có sửa đổi nào đối với C++ hoặc kết luận chấp nhận các thành phần mới trong vòng này.
- Chưa hoàn thành: Xác minh định dạng nội bộ SRAM, tuần tự hóa nút bảo mật tùy ý, giao diện người dùng quản lý vị trí đa thủ công, sao lưu lưu/xoay tự động, các dấu trang khác nhau, so sánh trạng thái sự kiện/ngẫu nhiên hoàn chỉnh cũng như lưu và đọc ma trận lưu trữ dưới sự kết hợp đa ngôn ngữ/nghệ thuật.
- Không có so sánh mô phỏng tham chiếu mới và bằng chứng so sánh lịch sử về sự gián đoạn chiến thuật hiện có vẫn thuộc về hồ sơ tương ứng của họ.