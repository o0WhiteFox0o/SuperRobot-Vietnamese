> **Language / Ngôn ngữ:** [English](pc-windows-build.en.md) · [Tiếng Việt](pc-windows-build.vi.md) · [中文](pc-windows-build.md)

# Instructions for Running & Compiling PC Version (Windows) for Super Robot Taisen 64 Recomp

> **Update:** October 2026.
> This document comprehensively describes the process of running the pre-built PC version (`Marchwind64-windows-x64`) and the process of self-compiling from C++ source code on the Windows operating system.

---

## 1. Pre-Built PC Version (Ready-to-Play Build Supports Vietnamese)

The official PC version with full Vietnamese language package (`vi`) has been packaged and completely configured in the folder:
```
dist/Marchwind64-windows-x64/
```
Additionally, the clean compressed distribution package (no ROM included) available to share is located at:
```
dist/Marchwind64-v0.4.2-vi-windows-x64.zip
```

### PC distribution package structure:
* **`Marchwind64.exe`**: Standalone executable file (Native x64 Windows Executable), using RT64 graphics engine (DirectX 12 / Vulkan). The language and font set check port patch has been applied to accept `vi` and load fonts `HarmonyOS_Sans_Condensed` and `HarmonyOS_Sans_SC`.
* **`content/`**: Independent content data folder (Standalone Content) contains `manifest.json`, `dialogue.json` (simultaneously integrating 4 languages `vi`, `ja`, `zh-Hans`, `en`), all character portraits (`name-entry/`) and combat graphics (`battle/`).
* **`Marchwind64.cmd`**: Convenient quick launch script (automatically detects ROM, passes parameter `--content content` and sets default language `--language vi`).
* **`rom.z64`**: Original ROM file *Super Robot Taisen 64 (Japan, Rev 0)* has been prepared.
* **`dialogue/`**: Folder containing plain text dialogue script files (`vi/` - Vietnamese, `en/` - English, `zh-Hans/` - Chinese).
* **`fonts/`**: HarmonyOS Sans font library fully supports Vietnamese accented character set.
* **`filters/`**: High quality CRT/Scanline shader filters from RetroArch.
* **Dependent DLLs**: `SDL2.dll`, `dxcompiler.dll`, `dxil.dll`, `librashader.dll`, `freetype.dll`, `harfbuzz.dll`, `icu*.dll` and the Microsoft Visual C++ Runtime library set.

---

## 2. How to Launch Games on PC

### Method 1: Launch with 1 click (Recommended)
1. Open the `dist\Marchwind64-windows-x64\` folder.
2. Double click on file **`Marchwind64.cmd`**.
3. The game will automatically open the native Direct3D 12 graphics window and start immediately with the Vietnamese interface.

### Method 2: Run directly from the PowerShell or Terminal command line
```powershell
cd dist\Marchwind64-windows-x64
.\Marchwind64.exe --play --rom rom.z64 --content content --language vi
```
*(If run once, the `--language vi` setting will be automatically saved to `%LOCALAPPDATA%\SRW64Recomp\presentation.json` so future times you can simply run `.\Marchwind64.exe --play --rom rom.z64 --content content`)*

---

## 3. Control Keyboard on PC

### Basic controls (Keyboard):
| Keys on PC | Functions in the Game |
| :--- | :--- |
| **Arrow keys `↑` `↓` `←` `→`** | Move map cursor / Menu navigation |
| **`Z`** | Confirm Button (A Button on N64 Handle) |
| **`X`** | Cancel / Back button (Button B on N64 handle) |
| **`Enter`** | START button (Opens system menu, skip) |
| **`A` / `S`** | L / R button (Switch information pages, change units) |
| **`Esc`** | Exit / Close game window safely |

### Advanced feature shortcuts (In-game Hotkeys):
* **`F7`**: Instant hot language switching between: `vi` (Vietnamese) ➔ `ja` (Japanese) ➔ `zh-Hans` (Chinese) ➔ `en` (English). The game will automatically save the language you choose.
* **`F6`**: Switch between original graphics mode (Original pixel) and upgraded graphics mode (HD Asset Pack + Model 5600 Waterdrop).
* **`F11`** or **`Alt + Enter`**: Enable/disable full screen mode (Fullscreen).
* **`F5`**: Hot reload the dialogue script from the `dialogue/` folder (very useful when translating and testing in game without restarting the game).
* **`E + Z`**: Hold to fast forward the plot (Fast Forward).
* **`E + Enter`**: Skip the current dialogue (Skip Dialogue).
* **`Q`**: Open voice reading history (Dialogue Backlog).
* **`↑` / `↓`**: Adjust the speed of automatically scrolling voice text.

---

## 4. Vietnamese Package Automation

To package the complete PC version in Vietnamese or update the distribution package at any time, the project provides automation scripts:
```
tools/release/build_windows_vi_package.py
```

### Command to run packaging:
```powershell
python tools/release/build_windows_vi_package.py --rom rom.z64 --zip dist/Marchwind64-v0.4.2-vi-windows-x64.zip
```

### Script steps performed automatically:
1. **Compile Vietnamese content (`compile_profile`)**: Scans ROM and translation files `content/locales/vi.json`, `content/dialogue/vi/` to create a demonstration profile (`prepared-profile`) with 4,674 lines of dialogue and 695 interface entries with SHA-256 secure hash code collated.
2. **Export independent content data store (`export_content`)**: Generate folder `dist/Marchwind64-windows-x64/content/` including `manifest.json`, `dialogue.json`, portrait set `name-entry/` and battle robot pose `battle/`.
3. **Patch the font check port (`Marchwind64.exe`)**:
* Offset `0x6c0591`: Allows the 2-character language code `vi` to pass the initial bounds check of the upstream binary (`zh-Hans, ja, en`).
* Offset `0x6bf648`: Automatically load the condensed font set `HarmonyOS_Sans_Condensed.ttf` combined with `HarmonyOS_Sans_SC.ttf` to display sharp Vietnamese text with standard interface ratio.
4. **Update launcher `Marchwind64.cmd`**: Ensure `--content "%HERE%content"` load call and prioritize `--language vi`.
5. **Compress clean release package (`--zip`)**: Create complete zip archive `Marchwind64-v0.4.2-vi-windows-x64.zip` (exclude copyright ROM file for ready sharing).

---

## 5. Build Engine From Source Process

If you want to manually change the engine's C++ source code (`src/native`, `src/host`) and recompile the new `Marchwind64.exe` file from scratch, the procedure is as follows:

#### 5.1. Prerequisites
The following tools need to be installed on Windows 10/11 64-bit machines:
1. **Visual Studio 2022** (Community or Build Tools version):
* Component integration: *Desktop development with C++* (MSVC v143 x64, Windows 10/11 SDK).
2. **LLVM / Clang**: Requires compiler `clang-cl` (available in the Visual Studio installation package or downloaded from LLVM Releases).
3. **CMake** (version 3.25 or higher) & **Ninja Build System**:
* Install via winget: `winget install Kitware.CMake Ninja-build.Ninja`
4. **vcpkg** (C++ library manager):
   ```powershell
   git clone https://github.com/microsoft/vcpkg.git C:\vcpkg
   C:\vcpkg\bootstrap-vcpkg.bat
   $env:VCPKG_INSTALLATION_ROOT = "C:\vcpkg"
   ```
5. **Python 3.12**:
* Enable UTF-8 mode: `[Environment]::SetEnvironmentVariable("PYTHONUTF8", "1", "User")`

---

### 5.2. Detailed compilation steps

#### Step 1: Prepare library via vcpkg
Install 3 libraries that handle fonts and international text normalization:
```powershell
& "$env:VCPKG_INSTALLATION_ROOT\vcpkg.exe" install freetype harfbuzz icu --triplet x64-windows
```

#### Step 2: Prepare resources and generate N64 recompiled code (Code Generation)
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

#### Step 3: Load the MSVC x64 environment
Open Developer PowerShell for VS 2022 or run the command:
```powershell
$vsPath = & "${env:ProgramFiles(x86)}\Microsoft Visual Studio\Installer\vswhere.exe" -latest -property installationPath
cmd /c "`"$vsPath\VC\Auxiliary\Build\vcvars64.bat`" && powershell"
```

#### Step 4: Configure the project using CMake
```powershell
cmake -S src/host -B build/recomp/gfx-build -G Ninja -DCMAKE_BUILD_TYPE=Release `
  -DCMAKE_C_COMPILER=clang-cl -DCMAKE_CXX_COMPILER=clang-cl `
  "-DCMAKE_TOOLCHAIN_FILE=$env:VCPKG_INSTALLATION_ROOT/scripts/buildsystems/vcpkg.cmake" `
  -DSRW64_ENABLE_RT64=ON -DSRW64_METAL_SOURCE_SHADERS=OFF
```

#### Step 5: Compile the game code and host the executable
```powershell
# Biên dịch nhân CPU trò chơi
cmake --build build/recomp/gfx-build --target srw64_cpu -j 4

# Biên dịch Host đồ họa (Marchwind64)
cmake --build build/recomp/gfx-build --target srw64-gfx-host -j 4
```
Once completed, the executable file `srw64-gfx-host.exe` will be created at `build/recomp/gfx-build/srw64-gfx-host.exe`.

#### Step 6: Package the Windows installation
1. Rename `srw64-gfx-host.exe` to `Marchwind64.exe`.
2. Gather the included DLL files:
* `SDL2.dll` (from `build/recomp/upstream/RT64/.../SDL2.dll`)
* `dxcompiler.dll`, `dxil.dll` (from DirectX Shader Compiler)
* `freetype.dll`, `harfbuzz.dll`, `icu*.dll` (from vcpkg's bin directory)
* `librashader.dll` (from `tools/recomp/toolchain/fetch_librashader.py`)
3. Copy folder `fonts/`, `dialogue/`, `filters/` and script `Marchwind64.cmd` to the same folder.

---

## 6. Automated Processes Through GitHub Actions CI

The project has a complete CI pipeline available at [`.github/workflows/build.yml`](file:///c:/Users/NHSON/Documents/GitHub/SuperRobot/.github/workflows/build.yml). Every time there is a new commit or a version tag is created (eg `v0.4.2`):
1. **Runner Ubuntu 24.04 (`generate`)**: Automatically decode the ROM, run the static recompilation tool `N64Recomp` to generate all C++ code, then compress the source code package.
2. **Runner Windows Server 2022 (`windows`)**: Load the generated code package, install vcpkg cache, compile with `clang-cl` and `Ninja`, embed VC++ runtimes, automatically check `Marchwind64.exe --play --help`, and package into `Marchwind64-<version>-windows-x64.zip` zip file.

---

## 7. Notes When Playing & Further Customization

* **Dialogue script update**: To translate more levels, directly edit the `.txt` files in `dist/Marchwind64-windows-x64/dialogue/vi/` and press `F5` in game to update immediately.
* **Location to save File Save**: Store process at `%LOCALAPPDATA%\SRW64Recomp\sessions\`. When you need to back up, you just need to copy this folder.

