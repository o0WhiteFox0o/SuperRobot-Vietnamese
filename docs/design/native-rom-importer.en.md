> **Language / Ngôn ngữ:** [English](native-rom-importer.en.md) · [Tiếng Việt](native-rom-importer.vi.md) · [中文](native-rom-importer.md)

# Native ROM first import (P1 import stage)

2026-09-20. Continue [P0 Release Plan](cross-platform-release-plan.md). This page updates the status of "Native first import not yet implemented": import code, boot wiring, and ROM-less control testing have been added; full macOS app distribution is not yet complete. The graphics host still only supports macOS, which does not mean that Win/Linux can run games.

## Current entrance

After this branch is built according to the original `make`, run directly:

```sh
./build/recomp/gfx-build/srw64-gfx-host --play \
  --rom "$PWD/rom.z64" --language zh-Hans
```

`compile_profile.py`, `export_content.py`, or `--content` is no longer required. The first time C++ extracts the content from the matching Japanese Rev 0 ROM, then verifies and reuses the cache. `--content` still retains the ability to explicitly provide the path to existing local content for developers and does not remove the debugging method of P0.

Builds still use Python; the first import and subsequent runs do not start Python, Git, CMake, Ninja, or the recompiler. The game CLI has no options to skip ROM summaries, override imported configurations, or accept arbitrary baselines.

## Responsibility and Resource Boundaries

| Documentation | Responsibility |
| --- | --- |
| `tools/release/build_import_spec.py` | Read the stored layout, glyph mapping and language directory when building, verify the source lock and generate embedded metadata; do not read ROM, do not extract game resources |
| `src/native/app/rom_import_codec.hpp` | Bounded text table, LZ ring buffer, resource descriptor, 96/97 pixel avatar decoding |
| `src/native/app/portrait_png.hpp` | Small avatar RGBA8 PNG output; storage type DEFLATE, no new compression library dependency |
| `src/native/app/rom_import.cpp` | Identity verification, original text and translation binding, avatar generation, cache verification and release of the same ROM byte buffer |
| `src/native/app/launch.cpp` | Import after holding the user directory lock, and then use the original native bootstrap; fail to update the archive pointer |
| `tests/test_native_import.py` | Comparison with existing Python decoder, translation checker, Pillow pixel output |

Embedded in the program are layout, Unicode glyph mapping, stored translations and UI copywriting; the original Japanese records and character avatars come from the player's local ROM. The cache contains ROM derived content and is not uploaded as a public release resource. Import probes are only used for testing and are not distributed with player programs.

The PNG compression encoding of the avatar output can be different from Pillow; the acceptance comparison compares the decoded RGBA pixels and does not require the PNG file digest to be the same. The summaries in the table of contents are calculated based on the respective actual output.

## Caching and failure handling

The cache directory is located in `content-cache/` of the user data directory. The key is the full SHA-256 fingerprint of `(ROM SHA-256, importer version, embedded metadata SHA-256)`, preventing the Windows path from being crowded with two long digests. Updating glyphs, translations or importers will use the new directory and will not overwrite the previously valid directory.

The OS file lock of the same user directory is always held from reading and importing to the end of the game. First create an independent temporary directory in the same cache parent directory. After all content and manifest are written and verified, rename it to the official directory. Exceptions will clear the current temporary directory, but will not clear existing caches or archives; the `.tmp-` directory left by the process will not be regarded as a valid cache. There are no blackout-level transaction durability guarantees.

Bad ROM, out-of-bounds descriptors, LZ truncation, unknown control words, outdated translations, STOP/END barriers or modified dynamic name parameters will stop the import. If the bad cache is clearly reported in the directory, you need to delete only the cache subdirectory where the error is reported after the game is closed, and then start rebuilding. Do not delete the entire user directory or `sessions/`.

## Verify

The public three-platform CI builds the application layer, importer and fake host, and does not run the original game. Synthetic ROM contains no game code or game graphics, covers text, parameters, 20 tables of metadata, LZ mode, 16 avatar positions, 96/97 pixels, cache reuse/invalidation, failover, first boot and SRAM recovery. Another use case removes the development tools directory from PATH to verify native bootstrap without calling external tools.

Real ROM control is a separate optional test:

```sh
SRW64_TEST_ROM=/absolute/path/to/rom.z64 \
  ctest --test-dir build/native-app -C Release \
  -R native-import-oracle --output-on-failure
```

This will compare the entire original text, all valid translations, glyph maps, and 16 avatar pixels with the existing Python implementation. The public CI does not have a ROM, so this item is explicitly skipped; the synthetic use case pass is not equal to the real ROM or the game process has been accepted.

## Still missing

This batch only covers Original rendering and does not migrate HD packages; the HD function of the old Python trial entrance is retained. Starting from 2026-09-24, you can create a full HD application package for your own use ([macOS local compatible build](../native/macos-release.md#全-hd-自用包)): HD materials are brought into `Contents/Resources/hd` when packaging, and only the original content will be generated from the ROM for the first import. Desktop file selection and `.app` staging/dependency collection have been added, see the next section; Developer ID notarization, real game and clean machine acceptance are still not completed. Metal/CoreText/AppKit decoupling, Win/Linux graphics, IME, and gamepads are still coming stages.

## P1b: macOS desktop portal and application packaging

P0/P1 has been merged into the main branch via PR #2. The desktop portal runs in the existing graphics host without adding another layer.
Python launcher or subprocess. Start using the system ROM selection box without parameters; read the user directory next time
`last-rom.txt` and recheck the ROM. Launch with Option, or launch with `--choose-rom`,
You can reselect the ROM. `--play` and the old positional probe parameters do not pop up the window and continue to be used for automation.

Select box uses AppKit `NSOpenPanel`; incorrectly uses `NSAlert`. Does not take over SDL's application delegate,
Do not open another GUI thread. Only after the native bootstrap verifies the content and archives, and holds the Session lock, is it saved atomically.
Selected ROM path. Cancel does not create a user directory; bad ROMs can be reselected; cache, archive or game errors only report an error and exit.
Do not restart the initialized game in the same process and do not open new archives silently. The application package remains read-only.

The code is located in `src/native/app/desktop.cpp`, `src/host/macos/desktop_macos.mm`; the former has no GUI dependency,
The latter is a standalone Cocoa adapter. Windows/Linux only tests the common control logic, and there is no GUI for those two systems in this batch.

### Developers generate local application packages

First complete the game build according to the original `make`, then explicitly specify the minimum macOS target and rebuild:

```sh
cmake -S src/host -B build/recomp/gfx-build -DCMAKE_OSX_DEPLOYMENT_TARGET=14.0
cmake --build build/recomp/gfx-build --target srw64-gfx-host --parallel 6
.venv/bin/python tools/release/package_macos.py \
  --binary build/recomp/gfx-build/srw64-gfx-host \
  --output "dist/SRW64 Recompiled.app" --minimum-macos 14.0
```

The output directory must not exist. `tools/release/package_macos.py` is a local development and packaging tool and is not distributed with the application;
It explicitly copies the executable, link dependencies, and plain text permissions specified via `--license-file`, without scanning or copying
Entire repository, ROM, archive, import cache or font. Generate `Info.plist`, call CMake BundleUtilities
Collect and relocate dependencies, remove the build machine RPATH, then verify dependencies and minimum system versions, and finally sign from the inside out.

The minimum macOS version is a verifiable packaging constraint, not a compatibility statement that only modifies the plist. Any Mach-O slice
Or the minimum version of the dependency declaration is higher than `--minimum-macos` will fail; you need to recompile the dependency or select a higher and pass
The lowest version that is actually verified. Failure does not leave the published half-package behind, nor does it overwrite the old `.app`.

Ad-hoc signature is used by default and is only used for local testing. It is not equal to Developer ID or Gatekeeper release.
`--sign-identity` can specify the developer's own signing identity; the script does not obtain credentials, submit for notarization, or upload release.
Complete dependency licenses, signatures/notarization, and hardened runtime requirements must still be verified before release. Application package with packaged fonts
HarmonyOS Sans (with full license) and symbol fonts.

### Added acceptance and remaining thresholds

`tests/native_desktop.cpp` Test cancellation, bad/missing/Unicode ROM path, remember selection, fail to restart host,
Error archives are not reset, real session locks, and irrelevant working directories. `tests/test_macos_package.py` Test file whitelist,
No overrides, exception cleanup, version constraints, RPATH and signature call order.

macOS CI compiles the real Cocoa adapter and packages it with an executable that does not contain game code and a dynamic library test.
`tests/check_macos_bundle.py` hides the original binary/dynamic library directory and moves `.app` to a path containing Chinese characters and spaces.
Make it read-only, run and review the signature in an environment with the development tools and DYLD override variables removed. It verifies the actual Mach-O dependency closure,
Not opening the modal selection box, not running ROM, SDL or GPU, does not mean that Finder → Import → Game has been accepted by the actual machine.

Real macOS acceptance also requires: Finder double-click, cancel, bad ROM, first import, second startup, Option reselection,
F7, name input, save/exit/restart, application migration, clean machine without Homebrew/Xcode.
The existing fail-fast `abort`/process crash does not guarantee that the error box will pop up. The current error dialog box covers captureable startup errors and return codes.
Metal/CoreText/AppKit game display migration is still in the next stage, and Win/Linux playability is not announced this time.

Reference: CMake official [BundleUtilities](https://cmake.org/cmake/help/latest/module/BundleUtilities.html),
Apple official [Notarization FAQ](https://developer.apple.com/documentation/security/resolving-common-notarization-issues).

### ICU and dynamic loading library

The packager can repeatedly pass in `--search-dir` for CMake to parse the `@loader_path` dependencies of libraries such as ICU on the build machine.
SDL2-compat loads SDL3 through `dlopen`, which does not appear in the ordinary link dependencies of SDL2; it must be used when using the compatibility layer
Pass in `--runtime-library /path/to/libSDL3.dylib` explicitly. The packager copies the Mach-O dylib by the specified name,
Then collect its dependencies together, check the minimum system version, correct the path and sign; the entire dependency directory will not be copied in batches.

Below is an example of a historical build using the native Homebrew library. Please use lower system version
[macOS Native Compatibility Build](../native/macos-release.md), refactors the host and runtime libraries from fixed source.

```sh
.venv/bin/python tools/release/package_macos.py \
  --binary build/recomp/macos-app-build/srw64-gfx-host \
  --output "dist/SRW64-237b629-macos-arm64/SRW64 Recompiled.app" \
  --minimum-macos 27.0 \
  --search-dir /opt/homebrew/opt/icu4c/lib \
  --runtime-library /opt/homebrew/opt/sdl3/lib/libSDL3.dylib
```

2026-09-20 Mach-O claims for native SDL3 are at least macOS 27, even if the host is built with 26, the entire package must claim 27.
Packages for older systems require matching dependency builds and cannot just change Info.plist. The application package is only locally signed ad-hoc and not notarized.