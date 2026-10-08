# Hướng Dẫn Chạy & Biên Dịch Bản PC (Windows) cho Super Robot Taisen 64 Recomp

> **Cập nhật:** Tháng 10/2026.  
> Tài liệu này mô tả toàn diện quy trình chạy bản PC dựng sẵn (`Marchwind64-windows-x64`) và quy trình tự biên dịch từ mã nguồn C++ trên hệ điều hành Windows.

---

## 1. Bản PC Đã Dựng Sẵn (Ready-to-Play Build Hỗ Trợ Tiếng Việt)

Bản PC chính thức với đầy đủ gói ngôn ngữ Tiếng Việt (`vi`) đã được đóng gói và cấu hình hoàn chỉnh trong thư mục:
```
dist/Marchwind64-windows-x64/
```
Ngoài ra, gói phân phối nén sạch (không kèm ROM) sẵn sàng chia sẻ nằm tại:
```
dist/Marchwind64-v0.4.2-vi-windows-x64.zip
```

### Cấu trúc gói phân phối PC:
* **`Marchwind64.exe`**: File thực thi độc lập (Native x64 Windows Executable), sử dụng engine đồ họa RT64 (DirectX 12 / Vulkan). Đã được áp dụng bản vá cổng kiểm tra ngôn ngữ và bộ font để chấp nhận `vi` và nạp phông chữ `HarmonyOS_Sans_Condensed` cùng `HarmonyOS_Sans_SC`.
* **`content/`**: Thư mục dữ liệu nội dung độc lập (Standalone Content) chứa `manifest.json`, `dialogue.json` (tích hợp đồng thời 4 ngôn ngữ `vi`, `ja`, `zh-Hans`, `en`), toàn bộ chân dung nhân vật (`name-entry/`) và đồ họa giao chiến (`battle/`).
* **`Marchwind64.cmd`**: Script khởi chạy nhanh tiện lợi (tự động nhận diện ROM, truyền tham số `--content content` và đặt ngôn ngữ mặc định `--language vi`).
* **`rom.z64`**: File ROM gốc *Super Robot Taisen 64 (Japan, Rev 0)* đã được chuẩn bị sẵn.
* **`dialogue/`**: Thư mục chứa các tệp kịch bản đối thoại dạng văn bản thuần (`vi/` - Tiếng Việt, `en/` - Tiếng Anh, `zh-Hans/` - Tiếng Trung).
* **`fonts/`**: Thư viện phông chữ HarmonyOS Sans hỗ trợ đầy đủ bộ ký tự có dấu Tiếng Việt.
* **`filters/`**: Các bộ lọc shader CRT / Scanline chất lượng cao từ RetroArch.
* **Các DLL phụ thuộc**: `SDL2.dll`, `dxcompiler.dll`, `dxil.dll`, `librashader.dll`, `freetype.dll`, `harfbuzz.dll`, `icu*.dll` và bộ thư viện Microsoft Visual C++ Runtime.

---

## 2. Cách Khởi Chạy Game Trên PC

### Cách 1: Khởi chạy bằng 1 cú nhấp chuột (Khuyên dùng)
1. Mở thư mục `dist\Marchwind64-windows-x64\`.
2. Nhấp đúp chuột vào file **`Marchwind64.cmd`**.
3. Trò chơi sẽ tự động mở cửa sổ đồ họa native Direct3D 12 và khởi động ngay với giao diện tiếng Việt.

### Cách 2: Chạy trực tiếp từ dòng lệnh PowerShell hoặc Terminal
```powershell
cd dist\Marchwind64-windows-x64
.\Marchwind64.exe --play --rom rom.z64 --content content --language vi
```
*(Nếu đã chạy một lần, thiết lập `--language vi` sẽ được lưu tự động vào `%LOCALAPPDATA%\SRW64Recomp\presentation.json` nên các lần sau có thể chạy đơn giản `.\Marchwind64.exe --play --rom rom.z64 --content content`)*

---

## 3. Bảng Phím Bấm Điều Khiển Trên PC

### Điều khiển cơ bản (Bàn phím):
| Phím trên PC | Chức năng trong Game |
| :--- | :--- |
| **Các phím mũi tên `↑` `↓` `←` `→`** | Di chuyển con trỏ bản đồ / Điều hướng menu |
| **`Z`** | Nút Xác nhận (Nút A trên tay cầm N64) |
| **`X`** | Nút Hủy / Quay lại (Nút B trên tay cầm N64) |
| **`Enter`** | Nút START (Mở menu hệ thống, bỏ qua) |
| **`A` / `S`** | Nút L / R (Chuyển trang thông tin, đổi đơn vị) |
| **`Esc`** | Thoát / Đóng cửa sổ trò chơi an toàn |

### Phím tắt tính năng nâng cao (In-game Hotkeys):
* **`F7`**: Chuyển đổi ngôn ngữ nóng tức thì giữa: `vi` (Tiếng Việt) ➔ `ja` (Tiếng Nhật) ➔ `zh-Hans` (Tiếng Trung) ➔ `en` (Tiếng Anh). Trò chơi sẽ tự động lưu lại ngôn ngữ bạn chọn.
* **`F6`**: Chuyển đổi giữa chế độ đồ họa gốc (Original pixel) và đồ họa nâng cấp (HD Asset Pack + Model 5600 Waterdrop).
* **`F11`** hoặc **`Alt + Enter`**: Bật/tắt chế độ toàn màn hình (Fullscreen).
* **`F5`**: Tải lại nóng kịch bản đối thoại từ thư mục `dialogue/` (rất hữu ích khi vừa dịch vừa thử nghiệm trong game mà không cần bật lại game).
* **`E + Z`**: Giữ để tua nhanh cốt truyện (Fast Forward).
* **`E + Enter`**: Bỏ qua đoạn hội thoại hiện tại (Skip Dialogue).
* **`Q`**: Mở lịch sử đọc thoại (Dialogue Backlog).
* **`↑` / `↓`**: Điều chỉnh tốc độ tự động cuộn chữ thoại.

---

## 4. Tự Động Đóng Gói Bản Build Tiếng Việt (Vietnamese Package Automation)

Để đóng gói bản PC hoàn chỉnh với tiếng Việt hoặc cập nhật lại gói phân phối bất cứ lúc nào, dự án cung cấp script tự động hóa:
```
tools/release/build_windows_vi_package.py
```

### Lệnh chạy đóng gói:
```powershell
python tools/release/build_windows_vi_package.py --rom rom.z64 --zip dist/Marchwind64-v0.4.2-vi-windows-x64.zip
```

### Các công đoạn script thực hiện tự động:
1. **Biên dịch nội dung Tiếng Việt (`compile_profile`)**: Quét ROM và các tệp dịch thuật `content/locales/vi.json`, `content/dialogue/vi/` để tạo hồ sơ trình diễn (`prepared-profile`) với 4.674 câu thoại và 695 mục giao diện đã đối chiếu mã băm an toàn SHA-256.
2. **Xuất kho dữ liệu nội dung độc lập (`export_content`)**: Sinh thư mục `dist/Marchwind64-windows-x64/content/` gồm `manifest.json`, `dialogue.json`, bộ chân dung `name-entry/` và tư thế robot chiến đấu `battle/`.
3. **Vá cổng kiểm tra phông chữ (`Marchwind64.exe`)**:
   * Offset `0x6c0591`: Cho phép mã ngôn ngữ 2 ký tự `vi` vượt qua cổng kiểm tra giới hạn ban đầu của binary thượng nguồn (`zh-Hans, ja, en`).
   * Offset `0x6bf648`: Tự động nạp bộ phông chữ cô đọng `HarmonyOS_Sans_Condensed.ttf` kết hợp cùng `HarmonyOS_Sans_SC.ttf` để hiển thị chữ tiếng Việt sắc nét, chuẩn tỉ lệ giao diện.
4. **Cập nhật launcher `Marchwind64.cmd`**: Đảm bảo lệnh gọi nạp `--content "%HERE%content"` và ưu tiên `--language vi`.
5. **Nén gói phát hành sạch (`--zip`)**: Tạo file nén zip hoàn chỉnh `Marchwind64-v0.4.2-vi-windows-x64.zip` (loại trừ file ROM bản quyền để sẵn sàng chia sẻ).

---

## 5. Quy Trình Biên Dịch Từ Mã Nguồn (Build Engine From Source)

Nếu bạn muốn tự thay đổi mã nguồn C++ của engine (`src/native`, `src/host`) và tự biên dịch lại file `Marchwind64.exe` mới từ đầu, quy trình được thực hiện như sau:

#### 5.1. Công cụ tiền đề (Prerequisites)
Cần cài đặt các công cụ sau trên máy Windows 10/11 64-bit:
1. **Visual Studio 2022** (bản Community hoặc Build Tools):
   * Tích hợp thành phần: *Desktop development with C++* (MSVC v143 x64, Windows 10/11 SDK).
2. **LLVM / Clang**: Cần compiler `clang-cl` (có sẵn trong gói cài đặt Visual Studio hoặc tải từ LLVM Releases).
3. **CMake** (phiên bản 3.25 trở lên) & **Ninja Build System**:
   * Cài đặt qua winget: `winget install Kitware.CMake Ninja-build.Ninja`
4. **vcpkg** (Trình quản lý thư viện C++):
   ```powershell
   git clone https://github.com/microsoft/vcpkg.git C:\vcpkg
   C:\vcpkg\bootstrap-vcpkg.bat
   $env:VCPKG_INSTALLATION_ROOT = "C:\vcpkg"
   ```
5. **Python 3.12**:
   * Bật chế độ UTF-8: `[Environment]::SetEnvironmentVariable("PYTHONUTF8", "1", "User")`

---

### 5.2. Các bước biên dịch chi tiết

#### Bước 1: Chuẩn bị thư viện qua vcpkg
Cài đặt 3 thư viện xử lý phông chữ và chuẩn hóa văn bản quốc tế:
```powershell
& "$env:VCPKG_INSTALLATION_ROOT\vcpkg.exe" install freetype harfbuzz icu --triplet x64-windows
```

#### Bước 2: Chuẩn bị tài nguyên và sinh mã tái biên dịch N64 (Code Generation)
```powershell
# 1. Kích hoạt môi trường Python
$env:PYTHONPATH = "src;tools"
$env:PYTHONUTF8 = "1"

# 2. Chuẩn bị phông chữ
python tools/content/prepare_fonts.py

# 3. Phân tích ROM và sinh mã C++ cho toàn bộ CPU N64
python tools/recomp/toolchain/analyze_layout.py --rom rom.z64
python tools/recomp/toolchain/scan_functions.py --rom rom.z64
python tools/recomp/toolchain/generate_cpu.py

# 4. Chuẩn bị renderer RT64 và giao diện Frontend RmlUi
python tools/recomp/toolchain/prepare_rt64.py
python tools/recomp/toolchain/prepare_frontend.py --fetch
```

#### Bước 3: Nạp môi trường MSVC x64
Mở Developer PowerShell for VS 2022 hoặc chạy lệnh:
```powershell
$vsPath = & "${env:ProgramFiles(x86)}\Microsoft Visual Studio\Installer\vswhere.exe" -latest -property installationPath
cmd /c "`"$vsPath\VC\Auxiliary\Build\vcvars64.bat`" && powershell"
```

#### Bước 4: Cấu hình dự án bằng CMake
```powershell
cmake -S src/host -B build/recomp/gfx-build -G Ninja -DCMAKE_BUILD_TYPE=Release `
  -DCMAKE_C_COMPILER=clang-cl -DCMAKE_CXX_COMPILER=clang-cl `
  "-DCMAKE_TOOLCHAIN_FILE=$env:VCPKG_INSTALLATION_ROOT/scripts/buildsystems/vcpkg.cmake" `
  -DSRW64_ENABLE_RT64=ON -DSRW64_METAL_SOURCE_SHADERS=OFF
```

#### Bước 5: Biên dịch mã trò chơi và Host thực thi
```powershell
# Biên dịch nhân CPU trò chơi
cmake --build build/recomp/gfx-build --target srw64_cpu -j 4

# Biên dịch Host đồ họa (Marchwind64)
cmake --build build/recomp/gfx-build --target srw64-gfx-host -j 4
```
Sau khi hoàn tất, file thực thi `srw64-gfx-host.exe` sẽ được tạo tại `build/recomp/gfx-build/srw64-gfx-host.exe`.

#### Bước 6: Đóng gói bản cài đặt Windows
1. Đổi tên `srw64-gfx-host.exe` thành `Marchwind64.exe`.
2. Gom các tệp DLL đi kèm:
   * `SDL2.dll` (từ `build/recomp/upstream/RT64/.../SDL2.dll`)
   * `dxcompiler.dll`, `dxil.dll` (từ DirectX Shader Compiler)
   * `freetype.dll`, `harfbuzz.dll`, `icu*.dll` (từ thư mục bin của vcpkg)
   * `librashader.dll` (từ `tools/recomp/toolchain/fetch_librashader.py`)
3. Sao chép thư mục `fonts/`, `dialogue/`, `filters/` và script `Marchwind64.cmd` vào cùng thư mục.

---

## 6. Quy Trình Tự Động Qua GitHub Actions CI

Dự án có sẵn quy trình CI hoàn chỉnh tại [`.github/workflows/build.yml`](file:///c:/Users/NHSON/Documents/GitHub/SuperRobot/.github/workflows/build.yml). Mỗi khi có commit mới hoặc tạo tag phiên bản (ví dụ `v0.4.2`):
1. **Runner Ubuntu 24.04 (`generate`)**: Tự động giải mã ROM, chạy công cụ tái biên dịch tĩnh `N64Recomp` sinh toàn bộ mã C++, sau đó nén gói mã nguồn.
2. **Runner Windows Server 2022 (`windows`)**: Tải gói mã đã sinh, cài đặt vcpkg cache, biên dịch bằng `clang-cl` và `Ninja`, nhúng các runtime VC++, tự động kiểm tra `Marchwind64.exe --play --help`, và đóng gói thành tệp zip `Marchwind64-<version>-windows-x64.zip`.

---

## 7. Lưu Ý Khi Chơi & Tùy Biến Thêm

* **Cập nhật kịch bản đối thoại**: Để dịch thêm màn chơi, chỉnh sửa trực tiếp các tệp `.txt` trong `dist/Marchwind64-windows-x64/dialogue/vi/` và nhấn `F5` trong game để cập nhật ngay.
* **Vị trí lưu File Save**: Lưu trữ tiến trình tại `%LOCALAPPDATA%\SRW64Recomp\sessions\`. Khi cần sao lưu, bạn chỉ cần copy thư mục này.


