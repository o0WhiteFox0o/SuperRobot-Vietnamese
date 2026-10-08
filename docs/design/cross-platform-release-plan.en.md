> **Language / Ngôn ngữ:** [English](cross-platform-release-plan.en.md) · [Tiếng Việt](cross-platform-release-plan.vi.md) · [中文](cross-platform-release-plan.md)

# Cross-platform publishing transformation: plan and first implementation

Baseline: `22706a4294f7e0ddee40563e7c6e4972376811f9` (2026-09-19).

> 2026-09-24: The order and thresholds of P2–P4 below have been replaced by [Three Platforms Porting Plan](three-platform-port.md); the goals, boundaries and authorization constraints of this page are still valid.

**This batch is an independent running portal and portable application layer, not a Windows/Linux game transplant. **
Graphics host still uses Metal; dialogue has been switched to FreeType/HarfBuzz/ICU; default game page has been changed to SDL/RmlUi, desktop ROM selector still uses AppKit; `src/host/CMakeLists.txt`
Non-Apple platform rejections are intentionally retained. The previous three-platform component test covered application launch/archive logic (now only runs locally),
Not the original game, GPU, input method, or full level.

## Goals and Boundaries

The final player process: Download the program for the corresponding platform → Select the matching ROM you have for the first time → Import locally → Start the game.
Players do not install Python, Git, CMake, Ninja, compilers or recompilation tools. Python remains in development,
ROM analysis, code generation, translation and compilation, art processing and QA; do not rewrite this entire set of tools.

Original game execution, gameplay fixes, TextKey/language directories, reading states, and verified thread exit behavior are preserved.
Don't announce cross-platform completion by removing native dialogue, name pages, Link Battler pages, or settings.
Existing `.command`/Python demos, probes, MCP and `build/recomp/profile-play` archives are not automatically migrated or deleted.

## First batch: implemented code

| Documentation | Responsibility |
| --- | --- |
| `src/native/app/runtime.*` | Parameters, user data directories, Windows/POSIX file locks, independent sessions, archive replication and integrity checks |
| `src/native/app/sha256.hpp` | Streaming ROM/content/SRAM digest; digest does not equate to source being trusted or authorized |
| `src/native/app/launch.*` | Read the migratable content directory, restore language/rules, clear development environment variables, and directly call the compiled host |
| `src/host/host.cpp` | Added `--play`; original positional probe ABI retained; no change to game loop |
| `tools/release/export_content.py` | Export the existing prepared profile as a relative path content directory for local use |
| Root `CMakeLists.txt` | A basic test entry that does not rely on ROM, SDL, RT64 renderer, and Python; not a game build entry |
| `tests/native_launch.cpp` | ROM-free native application testing; build and execute locally through root CMake |

`srw64_app` relies only on the C++20 standard library and a small amount of OS file locking APIs.
`srw64_launch` reuses the JSON single header file in fixed RT64 and does not link the RT64 renderer.
The application layer does not contain Metal/AppKit/CoreText header files and does not execute external processes.
The game rules directory is passed in from the host to avoid copying a set of rule IDs/default values that will drift in the new entry.

### New entrance for developers to try out (currently still only available for macOS graphics host)

Execute in the root directory of the warehouse where `rom.z64` and the development environment exist:

```sh
# 原有构建入口保留。构建过程中仍然会使用 Python。
make

# 一次性本地内容准备；两个输出目录均须不存在。
.venv/bin/python tools/content/compile_profile.py \
  --images original --output build/standalone-prepared
.venv/bin/python tools/release/export_content.py \
  --prepared build/standalone-prepared --output build/standalone-content

# 运行阶段直接调用 native binary，不经过 Python/build/probe launcher。
./build/recomp/gfx-build/srw64-gfx-host --play \
  --rom "$PWD/rom.z64" --content "$PWD/build/standalone-content" \
  --language zh-Hans
```

`--user-dir PATH` specifies an independent user directory; `--new-game` starts from a blank cartridge;
`--import-save PATH` Import an emulator archive as a cassette (see "Contents and Archives" below);
`--export-save PATH [--export-format ares|project64|mupen64plus|retroarch]` Only exports the cassette and does not start the game;
`--mute` mute; `--rules original|fixed|all` select and remember rule presets;
`--resolution-scale 1..8` specifies this resolution. The language can be switched in-game and restored next time.

Paths to ROM, content and binaries can be outside of the source directory. The new entry itself does not query the source code, `.git`,
Generate code or toolchain reports; however, this does not mean that the dynamic library collection, signing and distribution of macOS `.app` has been completed.
The first batch had no file picker or double-click launch UI. When the content directory is not prepared, an error will be reported explicitly and Python will not be called secretly.

### Content and Archives

The export directory contains Japanese text/avatars derived from the original ROM and must not be uploaded as a public release artifact for this project.
The current export only covers Original mode, native multi-language and name/linked avatar; the migration of HD images and model packages will be left in the subsequent stages.
The HD function of the original trial entrance is not affected by this batch. The exporter does not copy ROMs, fonts, source code, archives or the entire `assets/`.
Manifest lists files allowed to be read with SHA-256; runtime rejects out-of-bounds paths, external symlinks, and digest inconsistencies.

The first batch still requires a content preparation by development tools. **"The original ROM does not require Python for first time import" has not been implemented yet**,
The native importer must be completed before being released to the general public, and this batch of local content directories cannot be used as a publicly distributable substitute.

Default user directory:

| Platform | Path |
| --- | --- |
| Windows | `%LOCALAPPDATA%/SRW64Recomp` |
| macOS | `~/Library/Application Support/SRW64Recomp` |
| Linux | `$XDG_DATA_HOME/srw64-recomp`; `~/.local/share/srw64-recomp` when no valid absolute path is set |

Archived in `saves/` in the user directory (from 2026-10-01, see [Multiple Archive Column and Automatic Archive](save-slots-autosave.md) for design):

| Documentation | Content |
| --- | --- |
| `saves/cartridge.sram` | 32 KiB cartridge, byte-for-byte identical to ares' `save.ram` |
| `saves/cartridge.sram.prev` | Cassette before last release |
| `saves/slots/NNN.rec` | Extension column 3–99: The game writes 0x1F00 bytes into a save column |
| `saves/imports/` | Import the replaced old cassette each time |

Each run occupies an independent session, and the host only modifies this SRAM copy. Release the final SRAM to cassette only after normal return
(Leave the old cassette as `.prev`), and copy to `sessions/<id>/save.bin`, write summary, and replace `last-session.txt` as usual.
No archive, error return or abnormal termination will not be published. The cassette must have the checksum of `SRW64V3` file header, used field and interrupt area
It must be correct, otherwise it will refuse to start, and will not quietly roll back or open a new file.

- `--import-save`: recognizes 32 KiB SRAM (Big Endian/32-bit Word Reverse/16-bit Reverse) and RetroArch `.srm` (SRAM segment at 0x20800),
Judging based on the magic number of the file header, the extension is not recognized. The old cassette is saved into `imports/` first, and the archives in old columns 1 and 2 that are different from the new card are moved to the extended column.
The "seen" bitmaps on both sides are merged.
- `--import-save` without `--rom`: only imports and does not start the game; the user directory is locked when the game is running and will be rejected.
- `--export-save`: The format is selected by extension by default (`.ram`/`.sav` ares, `.sra` Project64, `.srm` RetroArch),
`--export-format` can be specified. If the target already exists, copy it to `*.before-srw64` first; keep other archives in it when writing to RetroArch `.srm`.
- `--new-game`: Start from a blank cassette; when exiting, the intact archives in the old cassette slots 1 and 2 will be moved to the extended slot and will not be lost (the old cassette will start as usual if it is damaged).
- The old version only has `sessions/`: When starting for the first time, the `save.bin` pointed to by `last-session.txt` and with a matching digest is moved to the cassette.

The historical snapshot remains at `sessions/<id>/save.bin`, point to it with `--import-save` when needed.
When importing the original Python trial history, explicitly select `runtime-data/saves/*.bin` for that session.

There is no automatic cleanup history; the logs and runtime-data of this host will also be retained, which may include cache ROM.
These directories are private runtime data, not shareable error reporting packages. Shared ROM/cache directory and log desensitization will be added in the future
and configurable retention policies. Atomic replacement currently prevents reads from half-written pointers and does not claim power-down transaction durability.

## Subsequent implementation sequence and acceptance threshold

### P1: Native first import vs. full macOS distribution

Migrate `source_catalog`, the **runtime subset** required for original ROM decoding/glyph mapping, name and linked avatar extraction into C++.
The Python implementation remains as oracle, with fixed ROM and synthetic fixtures doing byte-by-byte/record-by-record comparison.
The import cache is marked with `(ROM hash, importer version, locale/content schema)`; after the import is successful, it is published atomically.
Failure does not destroy existing cache. Do not compile C/C++ on first startup.

Added file selection, clear error prompts, independent read-only resources/writable user directories, and dynamic library collection of macOS bundles.
Binaries, native UI font schemes, language packs and distributable resources need to be clearly inventoried.

**Completion conditions:** Clean macOS user environment, no Python/Git/Homebrew/Xcode, programs and ROM are located outside the source code directory;
First time import, switching between Japanese, Chinese and English, normal save/exit/restart, bad ROM, missing resources, read-only application directory all passed.

### P2: Decoupling graphics and text backends

Directly depend on `graphics.cpp`, `native_dialogue_text.cpp`, `native_marker.cpp`
Portions of `MTL::*`, `plume::Metal*`, `SDL_MetalView` are moved out of the shared code.
Keep RT64/Plume: macOS Metal, Linux Vulkan, Windows. First choose a supported path (Vulkan or D3D12) and run through it.
Screenshots/readback, named page occlusion and present completion must also be abstracted, and window initialization cannot be replaced.

Dialogue model, paging/verbatim/reading state and render snapshot are retained; text shaping/raster and GPU synthesis layering.
Evaluate shared font rasterization schemes and redistributable fonts without hardcoding macOS PostScript font names on Windows/Linux.

**Unbreakable:** The UI must match the workload being rendered and cannot read the "latest RDRAM" and overwrite old frames;
Resize, asynchronous GPU completion callbacks, font metrics, end-of-line rules, and language switching cannot advance the original script.

**Complete conditions:** For each platform, at least pass the opening→name→first episode→archive cold start, including window scaling, F6/F7,
Dialogue occlusion/flickering and safe exit; hold platform gate before passing, not claiming full support.

### P3: Shared UI and Input

2026-09-20 The default game page has been switched to [SDL/RmlUi](../native/shared-game-ui.md): protagonist selection, name,
Confirmation, settings, Link Battler, notifications and debugging UI share events and rendering paths, and the original AppKit game page is no longer compiled.
[Independent name page probe](../native/shared-name-page-probe.md) is reserved for word grouping and layout regression.
Real game naming and writeback have been verified; OS input method candidate window, controller, cross-platform surface and first episode/save cold start are still to be accepted.
The old AppKit source code is temporarily used as a regression reference; the dialogue has been switched to [Cross-platform text component](../native/portable-text.md).

Connect controllers and configurable buttons; MCP/QA uses semantic actions to avoid treating Cocoa control paths as public protocols.
The debug socket must be excludeable at release build time, not just closed at runtime.

### P4: Release Build and Automation

The first batch of targets are fixed at Windows x64, Linux x64, and macOS arm64. Intel macOS, Windows ARM64,
Universal binary is independently accepted with more Linux distribution formats, without using the `*-latest` tag to implicitly extend the commitment.

GitHub Actions is turned off and remote CIs are not added. Source code component inspection and verification of the game holding the ROM are performed locally and logged separately.
Code generation is separated from three-platform compilation, and the generated product records ROM/toolchain/patch/schema summary.
Only the binaries, necessary dependencies, and distributable resources are collected according to the manifest when publishing, and the entire `build/` or user directory is never packaged.
Source code/generated code/binary, translation, art and fonts are checked separately for authorization boundaries; this check is not replaced by "without ROM".

First use Windows zip, Linux tar.gz to clarify the glibc baseline, macOS `.app` zip;
Dynamic library closure, Mac signature/notarization, Windows signature and clean machine testing will be completed before being available for download by ordinary players.
AppImage/Flatpak, installer and automatic updates are not the first prerequisite tasks.

## Verification entry and evidence scope

```sh
# 无 ROM、无 Python、无 renderer 依赖的原生基础测试。
cmake -S . -B build/native-app -DCMAKE_BUILD_TYPE=Release
cmake --build build/native-app --config Release
ctest --test-dir build/native-app -C Release --output-on-failure

# 加入完整 bootstrap 的合成内容 + fake-host 测试；只需要已固定的 JSON 头文件。
cmake -S . -B build/native-app \
  -DSRW64_APP_JSON_INCLUDE_DIR="$PWD/build/recomp/upstream/RT64/src/contrib"
cmake --build build/native-app --config Release
ctest --test-dir build/native-app -C Release --output-on-failure

python -m unittest discover -s tests -p test_release_content.py -v
```

Basic tests cover parameters/UTF-8 paths, directory strategies for each platform, file locks, SHA-256 known vectors and block reading,
Archive isolation, damage rejection, explicit recovery, abnormal exit without submission, path out of bounds and environment variable cleaning.
Full bootstrap testing using synthetic ROM/avatar and in-memory fake host, covering content relocation, arbitrary cwd,
Language/rule recovery and error returns; **not a substitute for real host builds or GPU/game verification**.

Before merging the first batch, a new entrance must be built in the developer's macOS + matching ROM environment, run the above real trial process and check
There is no return to the old entrance. Only then did we get into the native importer and platform graphics/UI migrations.