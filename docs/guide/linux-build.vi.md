> **Ngôn ngữ / Language:** [Tiếng Việt](linux-build.vi.md) · [English](linux-build.en.md) · [中文](linux-build.md)

# Bản dựng Linux và Steam Deck

2026-09-25. [Kế hoạch chuyển ba nền tảng](../design/three-platform-port.md) Phiên bản đầu tiên của X2: chạy trò chơi với Vulkan trên Linux x64. Năm lớp HD đã được chuyển đổi thành chùm (X1) và vẽ giống nhau trên Linux cũng như trên macOS. Gói tài liệu HD được tải xuống giống như phiên bản macOS, chỉ cần giải nén nó vào `~/.local/share/srw64-recomp/hd`; bạn cũng có thể sử dụng `build_linux.py --hd DIR` để trực tiếp đưa nó vào gói để bạn sử dụng (`hd/` nằm bên cạnh chương trình).

## Xây dựng trên Mac

Bắt đầu với `make` như thường lệ trên máy Mac của bạn và chuẩn bị sẵn phông chữ (`tools/content/prepare_fonts.py`). Sau đó khởi động Docker Desktop và chạy:

```sh
tools/release/linux/build.sh --jobs 8
```

Kịch bản thực hiện ba điều:

1. Chạy `prepare_rt64.py` trên máy Mac và xác nhận rằng bản vá RT64 (bao gồm cả móc "hoàn thành kết xuất") đã được áp dụng;
2. Xây dựng hình ảnh Ubuntu 22.04 x64 được mô tả bởi `tools/release/linux/Dockerfile`;
3. Chạy `tools/release/build_linux.py` trong vùng chứa. Container treo kho ở cùng một đường dẫn tuyệt đối, sao cho đường dẫn ghi trong file tạo ra thống nhất với Mac.

Các vùng chứa trên Apple Silicon chạy thông qua mô phỏng x64 và quá trình xây dựng đầu tiên (các phần phụ thuộc cộng với RT64 cộng với mã được tạo) mất nhiều thời gian. Sau đó, chỉ những tập tin đã thay đổi sẽ được chỉnh sửa lại.

## Xây dựng trên máy Linux x86-64

Chạy cùng một vùng chứa trên máy Linux x86-64 gốc nhanh hơn nhiều so với việc mô phỏng nó trên máy Mac. Phương pháp là kết hợp kho (bao gồm `.git`, sao cho số gửi trong tên gói nhất quán với `-dirty`) và đầu vào độc lập với nền tảng do `make` tạo ra (dưới `build/recomp` `cpu-bound`, `upstream`, `audio-probe`, `runtime-lifecycle`, `graphics-source-patches.json`, `thirdparty/librashader/linux` và `build/fonts`, `build/macos-deps/sources`), tạo hình ảnh ở đó và chạy `build_linux.py`:

- Container phải treo kho theo đường dẫn tuyệt đối giống trên Mac, đường dẫn mã nguồn ghi trong file tạo ra phải chính xác;
- Chạy với tư cách user của máy đó (`--user $(id -u):$(id -g) -e HOME=/tmp`), sản phẩm sẽ không bị sở hữu root;
- Mỗi lần kiểm tra ngược dòng không cần phải có `.git` nhưng phải ghi `.srw64-revision` (nội dung là kết quả của `git rev-parse HEAD` trên Mac) trong mỗi lần kiểm tra, giống như Windows CI; nếu không `prepare_runtime_lifecycle.py` sẽ đọc bản gửi của kho bên ngoài và báo cáo `Runtime lifecycle source revision differs`;
- Cái gì không cần pass: `target/`, sản phẩm Rust của librashader trên Mac, thư mục dựa vào gói mã nguồn cần giải nén (giải nén lại từ gói nén khi build), RT64 chỉ dành cho Windows, `mupen64plus-win32-deps`, tổng dung lượng khoảng 1,2 GB.

Để chạy thử nghiệm trên máy không có card đồ họa, hãy sử dụng Xvfb cộng với dung nham. Lavapipe Mesa 22.3.6 đi kèm với Debian 12 gây ra lỗi phân đoạn trong trình điều khiển ngay khi trò chơi bắt đầu. Nó cần được thay thế bằng Mesa 23.2.1 trong nguồn cập nhật Ubuntu 22.04: thêm `xvfb mesa-vulkan-drivers libvulkan1` vào hình ảnh bản dựng và trò chơi sẽ chạy trong vùng chứa này. Thêm `--network host --pid host` vào vùng chứa. Cổng loopback của màn hình trò chơi và số quy trình trong `debug.json` phải khớp với máy chủ. Kết nối từ các máy tính khác như bình thường `attach.py --host <主机> --data-dir <数据目录>`:

```sh
docker run -d --name srw64-run --network host --pid host --user $(id -u):$(id -g) -e HOME=/tmp \
  -e XDG_DATA_HOME=$T/data -v $T:$T -w $T/<包名> <运行镜像> \
  sh -c "Xvfb :98 -screen 0 1280x800x24 & sleep 1; DISPLAY=:98 exec ./marchwind64.sh --debug"
```

(`T` là thư mục kiểm tra, ROM được đặt trong `$T/data/srw64-recomp/rom.z64` và bị xóa sau khi kiểm tra.)

##Các bước thi công và sản phẩm

`build_linux.py` chỉ chạy trên Linux x86-64 và các sản phẩm có phiên bản dưới `build/linux-x64/`:

| Bước | Nội dung |
| --- | --- |
| Kiểm tra đầu vào | Mã được tạo nhất quán với bản tóm tắt của `cpu-bound/report.json`, có các móc hoàn thành kết xuất RT64, có nguồn âm thanh và phông chữ RSPRecomp |
| Phụ thuộc vào `deps/prefix` | Sử dụng cùng một loạt gói mã nguồn trong khóa macOS (`config/recomp/macos-dependencies.json`) để biên dịch các thư viện dùng chung của SDL3, sdl2-compat, FreeType, HarfBuzz và ICU. Bộ đệm của gói nguồn được chia sẻ với các công thức macOS `build/macos-deps/sources` |
| Máy chủ `gfx-build` | `src/host` xây dựng `srw64-gfx-host` với `SRW64_ENABLE_RT64=ON`, tiếng kêu của trình biên dịch, trình liên kết lld; Hộp thoại file của RT64 đi tới xdg-desktop-portal (`NFD_PORTAL=ON`), không liên kết tới GTK |
| Gói `Marchwind64-SteamDeck-<版本>-<提交日期>-<提交>.tar.gz` (được đặt tên theo phiên bản, ngày và gửi bắt đầu từ 29-09-2026, tiền tố trước khi đổi tên Marchwind64 là `SRW64-SteamDeck-`, chẳng hạn như `SRW64-SteamDeck-0.3.1-20260929-eb1cd4a`; khi có thay đổi chưa gửi, hãy thêm `-dirty` sau số gửi) | `VERSION.txt` (cùng tên, được cài đặt vào Bạn cũng có thể xem phiên bản sau `~/Games/SRW64`), các chương trình `srw64`, `lib/` (năm thư viện trên, RUNPATH được đặt thành `$ORIGIN`), `fonts/`, `dialogue/`, `licenses/`, tập lệnh khởi động `marchwind64.sh`, `add-to-steam.sh` và `steam/` (xem bên dưới), `README.txt` |

Có hai bước kiểm tra khi đóng gói và nó sẽ dừng nếu không thành công:

- Thư viện hệ thống mà các chương trình, thư viện gói phụ thuộc chỉ có thể là glibc, libstdc++, libgcc_s, zlib, và libdbus;
- Phiên bản biểu tượng glibc bắt buộc không muộn hơn 2.35.

X11/Wayland, PipeWire/PulseAudio/ALSA được tải khi SDL3 đang chạy và Vulkan được tải động bởi Plume qua volk, vì vậy chúng sẽ không xuất hiện trong danh sách phụ thuộc. Báo cáo được viết bằng `build/linux-x64/package.json`.

## Cài đặt và chạy

Xem `README.txt` trong gói. Tóm tắt:

1. Giải nén vào bất kỳ thư mục nào.
2. Đặt ROM vào `~/.local/share/srw64-recomp/rom.z64` hoặc đặt bên cạnh `marchwind64.sh` và đặt tên là `rom.z64`.
3. Chạy `./marchwind64.sh`.

`marchwind64.sh` Trước tiên hãy tìm ROM, mặc định là Tiếng Trung giản thể khi bắt đầu lần đầu tiên, sau đó thực thi `srw64 --play`. Khi không tìm thấy ROM, hãy sử dụng `kdialog` (đi kèm với máy tính để bàn SteamOS) hoặc `zenity` để bật lên mô tả vì không thể nhìn thấy đầu ra của thiết bị đầu cuối trong chế độ trò chơi của Bộ bài. Các bản lưu trữ và cài đặt nằm trong `~/.local/share/srw64-recomp`, có cấu trúc thư mục giống như phiên bản macOS.

Trên Steam Deck: Vào chế độ máy tính để bàn, mở Steam và nhấp đúp vào `add-to-steam.sh`. Sau đó bạn có thể khởi động từ chế độ trò chơi. Để ánh xạ bộ điều khiển, hãy xem phần bộ điều khiển của `graphics.cpp` và có một danh sách trong README.

`add-to-steam.sh` gọi `steam/add_to_steam.py` theo cách tương tự như nhấp chuột phải vào "Thêm vào Steam" trong trình quản lý tệp SteamOS:

1. Viết `~/.local/share/applications/srw64-recomp.desktop` và tên theo ngôn ngữ trò chơi (`presentation.json`'s `locale`; nó sẽ là tiếng Trung giản thể nếu nó chưa được bắt đầu): Super Robot Wars 64 / Super Robot Wars 64 / スーパーロボット大戦64;
2. Sử dụng `steam://addnonsteamgame/<desktop 文件>` để chuyển nó sang Steam đang chạy;
3. Đợi phím tắt bắt đầu `marchwind64.sh` xuất hiện trong `userdata/<用户>/config/shortcuts.vdf` (KeyValues nhị phân) và đọc ứng dụng của nó (phím tắt `srw64.sh` trước khi đổi tên trong cùng thư mục cũng được coi là có trong thư viện và sẽ không được thêm lại. Nó chỉ nhắc thay đổi mục tiêu thành `marchwind64.sh` trong thuộc tính Steam). Appid của phiên bản Steam mới là ngẫu nhiên và không thể tính toán trước;
4. Sao chép bìa trong `steam/` sang `userdata/<用户>/config/grid/`: `<appid>p.png` phiên bản dọc 600×900, `<appid>.png` phiên bản ngang 920×430, `<appid>_hero.png` banner trên cùng, `<appid>_logo.png`, `<appid>_icon.png`.

Chỉ trang bìa được làm mới khi ở trong thư viện. Bìa có `tools/release/linux/steam-art/*.png` trong kho, được sao chép nguyên trạng khi đóng gói nên gói hàng được xây dựng trên GitHub Actions cũng có bìa. Chúng được tạo bởi `tools/release/linux/steam_art.py`: logo tiêu đề của gói HD (`scene_images` của `content/art/stage1-hd.json`) được đặt chồng lên ngọn lửa tiêu đề, bên dưới là logo tiêu đề MARCHWIND64 của dự án (`web/public/brand/title-en.webp`), biểu tượng là logo M64 (`m64-icon.png`), bộ giống nhau cho từng ngôn ngữ; nếu hình ảnh tiêu đề hoặc hình ảnh thương hiệu thay đổi, hãy chạy lại trên máy này `steam_art.py --output tools/release/linux/steam-art` Gửi lại.

## Xác minh hồ sơ

**2026-10-06 Máy Linux từ xa (Debian 12, không có card đồ họa): Giao diện gỡ lỗi và MCP. ** Gói được xây dựng bằng cách sử dụng bộ chứa ở trên và trò chơi được chạy qua Xvfb cộng với dung nham trong bộ chứa Ubuntu 22.04 cộng với Mesa 23.2.1. Chỉ cần dựa vào nút chuyển trong "Tùy chọn → Giới thiệu" (không cần thêm `--debug`) để bắt đầu theo dõi và lời nhắc khởi động là bình thường. Trên máy Mac, `attach.py` đọc `debug.json` từ xa, `ssh -L` chuyển tiếp cổng cục bộ, `srw64_attach` của MCP (không có tham số), `srw64_status`, `srw64_screenshot` (được truy xuất qua màn hình `file.read` 1280×800), `srw64_events`, `srw64_quit` đều bình thường và điều khiển từ xa `debug.json` sẽ bị xóa sau khi thoát. Nếu cùng một gói được chạy trực tiếp trên máy chủ Debian 12, nó sẽ bị lỗi trong dung nham của Mesa 22.3.6 (giao diện gỡ lỗi đã được mở và không liên quan gì đến thay đổi này).

**2026-09-25 Thử nghiệm khói container. **Phương pháp thử nghiệm:

- Bộ chứa Ubuntu 22.04 x64, chạy trên Apple Silicon thông qua Rosetta;
- Xvfb dùng để hiển thị, Vulkan dùng phần mềm của Mesa để triển khai lavapipe (llvmpipe, Vulkan 1.3);
- Sau khi gói được giải nén, gói sẽ được khởi động thông qua `marchwind64.sh`.

Kết quả:

- Chương trình nạp thư viện gói;
- Lần nhập ROM đầu tiên: 51174 văn bản, 16 hình đại diện;
- `SRW64_GRAPHICS_API 1` (Vulkan);
- Phần mở đầu chạy liên tục hơn 5 phút ở tốc độ 60 VI/s, render ra logo và trang bản quyền BANPRESTO không bị treo;
- Cuối cùng window thread xử lý sự kiện exit bình thường, báo giao diện không bị kẹt chờ thông báo hoàn thành GPU.

Có ba điểm **không được xác nhận** lần này:

- Không nhập tiêu đề và trang gốc: phần mềm hiển thị quá chậm và không xác nhận liệu các phím do xdotool tổng hợp có được đưa vào trò chơi hay không.
- Cầu nối điều khiển chưa được thử nghiệm.
- Màn hình có các đường viền chấm chéo. Nó xuất hiện trên raster phần mềm của lavapipe cộng với MSAA. Việc nó có xuất hiện trên GPU thực hay không tùy thuộc vào Bộ bài.

Ba điểm trên phải được xác nhận trên Steam Deck thực tế.

##Sự khác biệt so với macOS

| Dự án | Hiện trạng Linux | Sẽ được bổ sung ở giai đoạn nào |
| --- | --- | --- |
| Lớp HD | Tương tự như macOS (lông); Gói tài liệu HD phải được tải xuống riêng hoặc đóng gói với `--hd` | Đã hoàn thành |
| Ảnh chụp màn hình giao diện gỡ lỗi | Có sẵn: kết cấu được thêm vào Vulkan → bản sao bộ đệm, hình ảnh chuỗi trao đổi có thể được sử dụng làm nguồn sao chép | Đã hoàn thành |
| Thông báo hoàn thành GPU | `RenderHookPresented` (bản vá `prepare_rt64.py`) được gọi sau hàng rào của hàng đợi kết xuất RT64, thay vì trình xử lý hoàn thành của Metal | Đã hoàn thành |
| Thanh thực đơn | Không có; cửa sổ cài đặt được mở bằng Ctrl+, (`frontend.cpp:1537`). Không thể mở boong tạm thời khi chỉ sử dụng bộ điều khiển. Bạn có thể ánh xạ phím quay lại tới Ctrl+, |
| Lựa chọn ROM | `marchwind64.sh` Tìm kiếm theo vị trí cố định | Theo dõi X2: đã đổi thành trang lựa chọn RmlUi |