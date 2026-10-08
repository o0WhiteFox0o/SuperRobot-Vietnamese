> **Language / Ngôn ngữ:** [English](macos-release.en.md) · [Tiếng Việt](macos-release.vi.md) · [中文](macos-release.md)

# macOS native compatible build

Release build targets Apple Silicon, macOS 14.0. This target must be used for the host and all runtime dependencies;
Compatibility cannot be achieved by lowering Info.plist or overwriting the version field of a ready-made dylib.
Building, checking Mach-O, and running the game on a new system can only prove the results of the build and running on the current machine;
The actual startup and game process of macOS 14/15 still need to be accepted by the corresponding system.

## Dependencies

`config/recomp/macos-dependencies.json` Fixed SDL3, SDL2-compat, FreeType, HarfBuzz, ICU
Source code URL and SHA-256. `tools/release/build_macos_dependencies.py` is downloaded and verified and built from the source code.
Install to `build/macos-deps/14.0-arm64/prefix` without changing Homebrew or system directories.
Build tools can still come from Homebrew; the runtime libraries are not linked against the Homebrew path.

Keep the existing SDL2 API → SDL2-compat → SDL3 path. Text uses FreeType + HarfBuzz’s OpenType
Typesetting and ICU segmentation; turn off HarfBuzz CoreText, GLib, Graphite2, accessibility tools, and FreeType
PNG/Brotli/BZip2 and other dependencies that are not used by current TTF/TTC text. The application package comes with fonts prepared by `tools/content/prepare_fonts.py` (HarmonyOS Sans 2.040 as-is with the full text of the license and signed fonts).

Prepare the fixed tool chain and generated code of the original project and run:

```sh
.venv/bin/python tools/release/build_macos_dependencies.py --jobs 8

release_deps="$PWD/build/macos-deps/14.0-arm64/prefix"
cmake -S src/host -B build/recomp/macos14-app-build -G Ninja \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_C_COMPILER=/usr/bin/clang -DCMAKE_CXX_COMPILER=/usr/bin/clang++ \
  -DCMAKE_OSX_DEPLOYMENT_TARGET=14.0 -DCMAKE_OSX_ARCHITECTURES=arm64 \
  -DCMAKE_PREFIX_PATH="$release_deps" \
  '-DCMAKE_IGNORE_PREFIX_PATH=/opt/homebrew;/usr/local' \
  -DSDL2_DIR="$release_deps/lib/cmake/SDL2" \
  -DICU_ROOT="$release_deps" \
  -Dharfbuzz_DIR="$release_deps/lib/cmake/harfbuzz" \
  -DSRW64_ENABLE_RT64=ON -DSRW64_METAL_SOURCE_SHADERS=ON \
  -DPython3_EXECUTABLE="$PWD/.venv/bin/python"
cmake --build build/recomp/macos14-app-build --target srw64-gfx-host --parallel 8

.venv/bin/python tools/release/package_macos.py \
  --binary build/recomp/macos14-app-build/srw64-gfx-host \
  --output "dist/Marchwind64-macos14-arm64/Marchwind64.app" \
  --minimum-macos 14.0 --search-dir "$release_deps/lib" \
  --runtime-library "$release_deps/lib/libSDL3.dylib"
```

Use a new build directory to avoid reusing the CMake cache containing Homebrew library paths. The packager refuses to overwrite existing output;
Change the output directory when packaging repeatedly. SDL3 is dynamically loaded by the compatibility layer and must be passed explicitly to the packager.
Dependency build report in `build/macos-deps/14.0-arm64/dependencies.json`; packager checks all
Minimum system version, dependency paths and signatures for Mach-O. The entire process only runs locally and does not use GitHub Actions.

The product is only locally ad-hoc signed and does not have Developer ID notarization. You should carry the license instructions for each dependency before distributing it externally.

## Full HD personal package

The package produced by default only has the original screen. To package a package that enables all HD by default, first prepare the HD directory, and then pass `--hd` when packaging:

```sh
.venv/bin/python tools/release/prepare_hd_bundle.py --output build/release/hd-$(date +%F)
.venv/bin/python tools/release/package_macos.py ...（同上） --hd build/release/hd-$(date +%F)
```

- `prepare_hd_bundle.py` compiles the art list `content/art/stage1-hd.json` from the local machine `assets/`: world map surface,
There are 270 RT64 replacement textures for space objects, dialogue boxes and combat HUD borders, 304 full avatars, 17 inter-field backgrounds, and 19 title images.
The avatar and background are then converted to JPEG (quality 95, no chroma sampling) by [`compress_hd.py`](../../tools/release/compress_hd.py):
The color of the avatar is saved as `.jpg`, and the transparency is saved as `.alpha.png` (grayscale plus transparency, grayscale is the silhouette color). The two are merged when the game is loaded;
The background is opaque and only one `.jpg` is stored. The measured PSNR of the avatar is no less than 44.6 dB, the median is 47.4 dB, and the transparency remains unchanged pixel by pixel;
Background PSNR is no less than 46.9 dB. RT64 textures and title images are still PNGs.
It also builds an index for the avatar of the native page (picture, palette), and the silhouette directly uses the `.alpha.png` of the avatar; then verify and copy
World map ships and landmarks pack (`build/recomp/native-models/assets`) and 5600 markers pack
(`build/recomp/native-marker/assets`). The tactical map is imported into `art/maps` with the art list, and the base map is converted to JPEG, about 350 MB.
The art part has been reduced from about 315 MB to about 151 MB: avatar 182 → 60 MB, background 45 → 10 MB, and silhouette 7 MB are no longer stored separately.
- When the launcher sees `Contents/Resources/hd/art`, set `SRW64_ART_PACK` to start with HD (`SRW64_IMAGE_MODE=hd`),
Connect HD images to the avatars on the name page, pre-war confirmation, archive and linkage pages, and reset them when the two model packages exist.
`SRW64_NATIVE_MARKER`, `SRW64_NATIVE_MODELS`. F6 or the settings window can switch back to the original version and choose not to write the settings file.
- The first import still only generates original content from ROM; importer version 3 notes battle avatars (pictures, palettes), and the old cache will be re-imported once.
- This kind of package is only for the packager's own use: the distribution license of AI Art has not been reviewed, and the two model packages contain reference bytes copied from ROM.
`Distribution.txt` will indicate not to distribute.
The existing minimum 27 legacy packages come from deployment targets for native Homebrew binaries, not source code requirements for SDL or literal components.

## Local verification (2026-09-20)

`build/recomp/macos14-game-01/bundle-verification.json` records 8 Mach-Os for new packages
(Main program and 7 dylibs) All declared minimum 14.0. Launch the real game from `/tmp`, reduced PATH,
Dynamic loading logs without Homebrew or dependent build directories, SDL3 from app package, exit code 0, signature check passed.
Shared UI validation in the same directory covers app menus, shortcut keys, name writeback, and Retina window scaling; dialogue validation overrides
Chinese, Japanese and English, font size, history and page turning, a total of 18 GPU screenshots. The 4 text/dialogue C++ checks corresponding to the new dependency passed.

The above running machine is macOS 27; we cannot claim that macOS 14/15 has completed the actual machine acceptance based on this.