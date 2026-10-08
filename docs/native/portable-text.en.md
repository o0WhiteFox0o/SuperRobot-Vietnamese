> **Language / Ngôn ngữ:** [English](portable-text.en.md) · [Tiếng Việt](portable-text.vi.md) · [中文](portable-text.md)

# Chinese, Japanese and English cross-platform text and game dialogue

2026-09-20. The text, names, pagination prompts, reading progress, bottom bar and review of the actual game are now used by default.
FreeType + HarfBuzz + ICU, pixels handed over to [Plume compositor](plume-pixel-compositor.md).
Dialogue is no longer linked to CoreText/CoreGraphics, and there is no option to switch to the old backend. The supported range is `zh-Hans`, `ja`, `en`.
Menus, names and settings continue to use SDL/RmlUi; screenshots and HD layers have also been changed to Plume, see [Three Platforms Porting](../design/three-platform-port.md).

## Actual path

`src/host/dialogue_scene.cpp` implements `typeset()` and `rasterize_frame()`, using
`src/native/text/portable_text.*` typesetting and drawing; `src/native/text/game_fonts.*` is responsible for selecting fonts.
`src/host/dialogue_layout_adapter.hpp` Give the line/page range to the original Reader and save it in the Layout
Immutable TextLayout. The game frame then holds the glyph position and font bytes, and the word-by-word display only changes the visible range, without rearrangement.
The original Reader's page turning, automatic reading, review, language switching and guest confirmation logic remain unchanged.

2026-10-02 The scene is first recorded as a series of drawing steps (filling or a line of text), each step has a key (what to draw, where) and pixel range.
`rasterize_frame()` draws all the steps in sequence; the `IncrementalRaster` used for presentation is compared with the previous frame, only the increase or decrease is
The step's rectangle is redrawn and uploaded (the resident canvas of [Plume Compositor](plume-pixel-compositor.md)). Show each step verbatim only
Redraw the striped area of ​​one line, and the progress bar of automatic reading only redraws the progress bar; previously, every time the status changed, the entire window CPU raster and new
The entire window texture is uploaded again (16 MB per frame at 2560×1600, now about 1 MB, CPU 2.2 ms → 0.5 ms).
`tests/native_dialogue_raster.cpp` The frame-by-frame verification patch will be the same as the entire frame raster pixel-by-pixel after being pasted back.

The rules for darkening the text are the same as the original version: only look at the palette bytes of the text slot +3 (`8008C5E4` filled in the table: 0 white = resource 2,
2 dark = resource 4). When the plot changes to the other side and the conversation is `8008FD40`, write the old box as 2; the battle lines are `8008FFAC`,
Never write 2, so it stays white until the box disappears. Whether it has been read or not (status +2: 1 reading, 3 still displayed after reading) does not affect the color.

The dialogue layer is also covered during the transition: the transition task `80099508` draws an opaque black filled rectangle for each of the 240 lines in each frame, with the left and right ends
Line-by-line floating point numbers starting from `0x8015E9C8`/`0x8015ED88` (various erasing and fading only update these two sets of numbers). The task always exists after it is first created.
(handle `D_8015E9C0`), the two columns [0,1) and [319,320) are still drawn when idle. The host reads the black bar of this frame when submitting the display list,
Truncated by the integer of the task, mapping of `wide_map::wipe_end` in wide screen (left end ≤1 aligns with the left edge of the screen, right end ≥319 aligns with the right edge,
The rest are scaled to the width of the frame) and drawn into the dialogue layer as a final "erase" step. Previously, words would float on the black field of blinds where battles alternate between attack and defense.
2026-10-02 Measured array (`build/recomp/debug/20261002T120943.791168Z/cover-dump.json`): Each row alternates when all black
[0,319)/[1,320). I once mistakenly extended "from 0" to the edge of the window, and the free [0,1) erased our dialogue box extending outside 4:3.

The original's own glyphs are removed from the submitted copy of the display list by `take_frame` (an E4 rectangle drawn with the font texture within the dialog box).
Each glyph in the game has a separate texture (`FD4800FB`): glyph size < 0x597 uses resource 0 (504×504), ≥ 0x597 uses resource 0
Resource 1 (504×252, less common Chinese characters, such as insult regret burn; `sltiu 0x597` of `8008EE64`). The two pictures are the same width, only the one with texture header
The height is different (`01F8`/`00FC`). Before 2026-10-03, only resource 0 was recognized, and the original glyph of resource 1 remained on the screen, with 1x pixels.
The Japanese kanji are superimposed under the translation ("Insult/Regret" for "ブライ大帝", "Ran" for "Ryuイン" in the title demonstration battle); this has nothing to do with incremental redrawing.

ICU handles grapheme boundaries and Chinese and Japanese prohibitions, HarfBuzz shaping, and FreeType output grayscale coverage.
Offsets use UTF-16 code unit; combining sequences, explicit newlines, and blank lines are preserved. The layout is generated once and drawn according to the selected rows
and grapheme range display; when the line width is insufficient, only emergency line wrapping occurs at the grapheme boundary. The main text is cropped to the dialogue box, and labels and review areas each have cropping areas.
Pixels are top-down BGRA8, alpha premultiplied; layout snapshots remain valid across language/font sizes and asynchronous GPU rendering.
There is no commitment to pixel-by-pixel equivalent CoreText anti-aliasing or extended product support for Arabic, color emoji, or other languages.

## Fonts and dependencies

The build depends on FreeType >= 2.10, HarfBuzz >= 2.8, ICU >= 70. Available on macOS:

```sh
brew install freetype harfbuzz icu4c
```

Linux installable `libfreetype6-dev libharfbuzz-dev libicu-dev fonts-noto-cjk`; native component build for Windows
CMake toolchains (such as UCRT64) that provide the three libraries mentioned above are available, but a full Windows build of the game is not yet available.

Starting from 2026-09-23, the game uses packaged fonts: the launcher points `SRW64_FONT_DIR` to `tools/content/prepare_fonts.py`
Prepared directories (`build/fonts/` for development runs, `Contents/Resources/fonts/` for application packages). Font chain: Chinese and Japanese
HarmonyOS Sans SC → Symbol font `SRW64Symbols.ttf` → Button icon `SRW64Prompts.ttf`; English is HarmonyOS Sans Condensed → SC → Symbol font → Button icon. There are also weapon mark icons in the symbol font (U+E000+original font size, see [Modification Screen](native-upgrade-screens.md)).
The font package starting from 2026-09-24 is HarmonyOS Sans 2.040: `HarmonyOS_Sans_SC.ttf` (20.6 MB) and `HarmonyOS_Sans_Condensed.ttf` (0.3 MB) are both variable fonts (wght 40–900),
Each file contains all weights. When `FontSource::weight` is 0, use the file default instance Regular (400); other values use the nearest named instance on the wght axis,
Both shaping and rasterization use this instance. The title menu and chapter title card use `game_font_sources(locale, 700)`, which is the Bold instance (706); the symbol font has only one weight and is not affected.
RmlUi reloads the instance with the same name (Normal, Regular) according to the word given by `LoadFontFace`. Compared to 1.0 Regular, the typography is only slightly different:
"——" is connected into a ligature, the English "Th" ligature, and the Chinese curly quotation marks have a width difference of 0.03 em; the line breaks and page turning of the 30 shared use cases have not changed.
When files are missing in the directory, an error will be reported explicitly and system fonts will not be returned. Still looking for local machine when there is no `SRW64_FONT_DIR` (unit tests, old probes)
Noto Sans CJK (Linux), Arial Unicode (macOS), Microsoft Yahei (Windows); Noto standard TTC selects the corresponding face according to Chinese/Japanese.
Available for development and testing `SRW64_TEXT_FONT` specifies a clear TTF/OTF/TTC file; does not search the current directory or download from the Internet.
The font is held by the layout after being read in. macOS PostScript font names in old content packs no longer determine dialogue fonts, and content packs do not need to be re-imported.
Distribution application packages package fonts and licenses (`tools/release/package_macos.py`) with `Contents/Resources/fonts/`.

## Local verification

GitHub Actions is closed and the repository does not retain remote workflows. The following tests are executed locally with no ROM or GPU dependencies:

```sh
# 完整游戏对白场景、原 Reader 和 UTF 转换；只使用 RT64 的 JSON 头文件。
cmake -S tests/dialogue_cpu -B build/dialogue-portable -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DSRW64_RT64_HEADERS="$PWD/build/recomp/upstream/RT64"
cmake --build build/dialogue-portable --parallel 6
ctest --test-dir build/dialogue-portable --output-on-failure

# 独立排版组件。也可以给出自己的本地 CJK 字体，跳过字体准备。
python tests/portable_text/prepare_fonts.py build/text-fonts
cmake -S tests/portable_text -B build/text-cjk -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DSRW64_TEST_CJK_FONT="$PWD/build/text-fonts/NotoSansCJKsc-Regular.otf" \
  -DSRW64_TEST_VARIABLE_FONT="$PWD/build/fonts/HarmonyOS_Sans_SC.ttf"   # 可选：字重检查
cmake --build build/text-cjk --parallel 6
ctest --test-dir build/text-cjk --output-on-failure
```

Independent typesetting tests cover Chinese, Japanese and English mixed typesetting, prohibitions, combined characters, long text, paging, cropping, scaling, pre-multiplied alpha,
Old layout and concurrent rearrangement after font file deletion; game scenario testing covers double boxes, names, verbatim, review, bottom column, language change and font size.
`SRW64_TEST_CJK_FONT` can also be passed to CMake for dialogue scene testing to explicitly specify the test font.
Component tests and real game screenshots are recorded separately, and the entire game is playable on Windows/Linux without CPU success.

## This acceptance

Local `make check`: 260 entries, 249 passed, 11 skipped; 4 CTest passes for independent text components and full dialogue CPU.
In a real macOS game running `build/recomp/portable-dialogue-02/`, first enter the regression by sharing the UI/name and plot,
Then use `tools/recomp/verify/verify_portable_dialogue.py` to cover Chinese, Japanese and English switching, 10/13/18 font size, review,
800×600 and 1100×760 windows, only host paging is advanced and the original script is not advanced. A total of 18 GPU screenshots are saved.
Reports `portable-dialogue-verification.json` for this directory; tests silent, independent new game, exits normally.
Screenshot inspection found and fixed the problem of "the entire text can fit, but the line breaks early because the line break breakpoint of ICU contains a line break".
Component tests retain this regression. This new scenario or full game has not been executed on Windows/Linux and no old components have been used for testing to make this statement.