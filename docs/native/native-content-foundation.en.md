> **Language / Ngôn ngữ:** [English](native-content-foundation.en.md) · [Tiếng Việt](native-content-foundation.vi.md) · [中文](native-content-foundation.md)

# Native content architecture: first batch of implementations

2026-09-12 Scope update: We will continue to promote our own functional modules according to the [Built-in MOD Roadmap](../design/mod-roadmap.md); the registration of external content types, package dependencies and public SDK access in the "next batch of work" in this article are temporarily suspended. Existing directories, profiles, language and art switching continue to be reused.

2026-09-11 Timing fix: Fixed the problem of the dialogue snapshot of the next frame being cleared by mistake; the normal trial turns off periodic screenshots and memory export by default, and the complete probe remains available. See [Dialogue Flicker Fix](native-dialogue-flicker.md) for details.

Date: 2026-09-11. This batch connects the unified JP baseline, external language directory, independent art package and image switching to the real host. See [architecture plan](../design/native-extensibility-architecture.md) for the overall design.

## Runnable entry

Double-click `scripts/Play SRW64 Native.command` in the root directory of the repository, or:

```sh
.venv/bin/python tools/recomp/run/play_native.py \
  --profile config/recomp/profiles/play-profile.json --new-game

# 同一个原始 ROM、同一个存档目录；启动时选择日文和原图。
.venv/bin/python tools/recomp/run/play_native.py \
  --profile config/recomp/profiles/play-profile.json --language ja --images original --new-game
```

The default configuration is Chinese dialogue, high-definition pictures, native water droplets, and 4 times the internal rendering resolution. Press **F6** during operation to switch back and forth between Original and HD, and the window title displays the current mode. Starting from 2026-09-11, the 5600 model also switches: Original uses the original diamond shape, and HD uses the model selected by the configuration. `presentation.model_5600: waterdrop` means HD mode enables water droplets; when set to `original`, both modes maintain the original model. F6 only changes this run; press profile/command line selection for next startup. Language, native fonts, and rendering resolution do not change with this switch.

The save history of the new entry is unified in `build/recomp/profile-play/sessions/`, and the Japanese, Chinese and two picture modes share the same JP game identity. Starting from 2026-09-12, when `--new-game` is not specified and the most recent verifiable save is selected by completed run report, ROM identity, and final summary, corrupted copies are reported and rolled back; first use of original, locked JP episode one playthrough archive copy. Supports listing history and explicit selection, see [Archive Recovery](../guide/native-save-recovery.md) for details. The old patch ROM entry has been removed, and historical archives will not be automatically migrated.

This entry still uses the local original `rom.z64`, the generated recomp build, and the verified art file. RT64 uses the original image when the resource lacks a single replacement; starting from 2026-09-12, Original can continue to start when encountering a missing HD package/avatar file, and displays that HD is unavailable; an error is still reported if explicit HD or summary does not match. See [Original Fallback](native-original-fallback.md) for details. Package distribution for releases has not yet been implemented.

## Removed responsibilities

| Module | Actual responsibilities at this stage |
| --- | --- |
| `src/srw64_native/catalog.py` | Generate local source directory from fixed original ROM with glyph map; TextKey, source text excerpt, script barrier and parameter validation |
| `src/srw64_native/profile.py` | Parse language, image, model, font and resolution respectively; compile immutable run configuration |
| `src/srw64_native/assets.py` | Verify the pure art allowed list and each file summary, and output an independent RT64 package |
| `src/native/localization/` | Host TextKey search, corresponding source text fallback, font/locale/native UI string |
| `src/native/game_adapter/dialogue_source.hpp` | Make it clear that the standard dialogue comes from table 0; identify the actual bound font atlas when drawing |
| `src/native/presentation/image_mode.hpp` | The window thread only submits image mode requests, and the rendering thread confirms the application |
| `src/host/` | Continue to carry the existing game bridge, read control and platform backend; gradually migrate, retain the existing acceptance port |

The auto-generated recomp C files are not moved, and a second code mod loader is not introduced. `gameplay_mods` must be empty in this batch to prevent the configuration from appearing to accept a gameplay mod that is not actually loaded.

## Multilingual content

The original game text is generated from the user's local ROM. The translation is divided into two parts, both using Unicode and not occupying or extending the N64 font library:
- **Data text** (name, label, prompt, record 0–5643): expanded from the entry table `content/locales/terms/` through `tools/content/apply_terms.py` to `content/locales/<语言>.json`, 4,712 entries in Chinese and English, see [data text entry table](localization-terms.md).
- **Plot and Combat Lines**: Player-changeable line text file `content/dialogue/<语言>/`, see [Line Text File](../guide/dialogue-text.md).

When translation is missing, press the complete TextKey to return to the corresponding Japanese source record.

An example TextKey is `base:t00_17412`; another table's `base:t01_17412` is a different record. The current standard dialogue adapter comes from the original function `8008C9C0`, and its `8008CA5C..8008CA6C` call always passes in table 0. Other UI/text consumers must still adapt one by one, and cannot claim to have been Chineseized just because the directory contains their records.

The translation allows changing the length, line breaks, and native reading pagination. The STOP/END order must be preserved, as well as the dynamic name/special glyph token in each paragraph. Changes in the original text summary, duplicate keys, unknown keys or illegal control characters will prevent loading. Content compilation only reads the original ROM; no ROM text injection is performed.

Add language: Add a word list with the same key as Chinese and English in `content/locales/terms/` and run `apply_terms.py`, put the line file in `content/dialogue/<语言>/`, register it in `locales` of the profile, and start it with `--language <语言>`. There is no C++ enumeration for language tags, so there is no need to reprogram the host for new languages.

You can compile and verify first without starting:

```sh
.venv/bin/python tools/content/compile_profile.py \
  --language zh-Hans --images original \
  --output build/recomp/content-preview
```

The output must be a new directory that records the original ROM, a directory of all registered languages, an art list, and a summary of the build files. Registration directory is verified and frozen before startup; **F7 hot-switches languages ​​while running, F6 switches images with 5600 models**. Hot switching uses immutable directories and frame-by-frame referencing, and the current dialogue does not advance to the next clip. See [Three Base Verifications](native-foundations-verification.md) for setup, coverage reporting, and actual verification.

Currently accessed: plot and battle dialogue (native reading UI) and all native pages (inter-game screens, pre-battle page, name page, settings). The original menu, opening and ending picture text, etc. still display the original images. The names of the protagonist and partner cannot be changed. The default names are displayed according to the reading language. See [Default name display in three languages](default-names.md).

## Original and HD pictures

`content/art/stage1-hd.json` lists two categories of HD art (2026-09-24):

- **RT64 texture hash replacement, 270 items**: 213 for story world map surface (resources 5602–5606), 27 for universe objects, 30 for border slices (13 for dialogs, 17 for combat HUD). The source package is `assets/hd-ai/worldmap-surfaces/pack-v5`. The font images and other textures in the package are not in the list and will not be included during compilation; the filtering is completed during offline compilation, and the resource category is not guessed based on the file name during runtime.
- **Host draws the whole picture**: avatar (`portraits` segment, see [Character Avatar HD](native-portraits-hd.md)), interfield background (`backgrounds`, see [Interfield Background HD](native-backgrounds-hd.md)), title Logo and flames (`scene_images`, see [title screen and plot text image](native-title-and-story-images.md)). The BANPRESTO flag, GAME OVER and window borders are not in the package and are generated from the ROM when the game is run (`src/host/rom_art.cpp`).

The default profile is `images: original`; start it with `--images hd`, or press F6 in the game to use HD.

2026-09-23 It was found that the earliest transparency processing of the avatar had three flaws. After replacing the original image, there was a problem with the edge of the avatar:

- The color of transparent pixels is saved as black. Both RT64 and RmlUi pages perform bilinear sampling based on non-premultiplied Alpha, so dark edges appear on the outer edge of the outline.
- The model output is offset and scaled relative to the original image (Laurence is offset to the right by about 1.5 original pixels, Manami is reduced by about 1%), and the mask follows the offset outline. The result is that one side is eaten away, the other side expands, and 13–519 light-transmitting pixels appear within 2 original pixels inside the outline.
- The gray background floods from all four sides of the image, and light-transmitting spots appear on the clothes and hair cut off by the frame (bottom and top edges).

Modification of [`portrait_matte.py`](../../tools/hd_ai/portrait_matte.py):

- First register the model output to the original image;
- The outline is only allowed to move within ±1.5 original pixels of the original image mask;
- The gray background only floods from the transparent pixels of the original image;
- Transparent pixels are filled with the nearest solid color;
- Separate resampling of color and alpha when downscaling.

The contour IoU of the four modified avatars is 0.984–0.994, the frame cutoff is 100% opaque, and the number of transparent pixels within the contour is 0–3 (Lanczos ringing, Alpha ≥ 245). After 3x simulated non-premultiplied bilinear amplification, pixels with edge deviations exceeding 16 levels dropped from 203 / 74 / 97 / 0 to 0. These modifications are now used by the entire avatar pipeline, and the reconstruction method can be found in [Character Avatar HD](native-portraits-hd.md).

F6 does not unload textures in use by the GPU. The window thread submits the request; the rendering submission thread waits for the submitted workload/present to be completed and idle, and then changes the replacement switch in the texture-map mutex of RT64. This way UV scaling and texture descriptors are built in the same mode; textures are still managed by RT64. The 5600's native replacement markers are also built according to the applied mode: Original does not add native draw/suppress markers and retains the full eight original planes; HD only marks water drop replacement. This switch currently works on pure art packages and 5600, and cannot be used directly when connecting language maps in the future.

`image-mode.json` records the applied mode and the actual `model_5600`, `image-mode-events.jsonl` record switch; GPU screenshot metadata for full diagnostic mode includes the applied mode. The `SRW64_WINDOW_CONTROL=1` file request for testing shares the same request/application path as F6 and does not modify game memory or archives.

## Validation and follow-up boundaries

Python validation, C++ TextKey/fallback/mode request tests, and actual Core Text formatting tests are run separately. The avatar round-trip verification script (`verify_profile_images.py`, deleted in 5b997c7 with the full diagnostic mode on 2026-10-01) reached the same section of `base:t00_17412` in the real new game story at that time, executed the original image→HD→original image→HD, and checked that the dialogue status remained unchanged and the static avatar/map area round-trip pixels were consistent. The actual operation results are shown in the acceptance record at the end of this document.

Next batch of work:

1. Continue to include consumers such as names and menus into the TextKey service; the default display name and custom name are processed separately to complete the Japanese and Chinese language selection UI.
2. Register the SRW64 content type of N64ModernRuntime, supplementary package dependencies, version and loading conflicts; the current external JSON is for development input and is not yet `.nrm`/public SDK.
3. Extract the known field schema of the body, character, and weapon. First, go back and forth without modification, and then select a field to verify that the data page, actual settlement, and saving are consistent.
4. Level deployment and events are first processed through structured extraction/round-trip; newly added units or levels require verification of capacity and archive mapping before opening.


## 2026-09-11 Actual acceptance

- `make check`: 60 Python tests, compileall, dependency checks passed; `make recomp-content-test`: C++ content/adaptation tests and actual Core Text conversational formatting/reading control tests passed.
- Four startup configurations (Japanese/Chinese × original image/HD) are compiled and passed, all of which are the same locked JP ROM. The handwritten host source code summaries of the two real machines are consistent, and the language is selected through data.
- `build/recomp/profile-check/live-zh-3/`: 7848 VI exits normally; `live-ja-3/`: 8064 VI exits normally. Both runs from the new game to segment 1 of `base:t00_17412`.
- Each language actually captures four frames of original image → high-definition → original image → high-definition. The avatar ROI `[48,45,330,335]` has 70680 pixel changes, and the map ROI `[0,0,100,45]` has 4500 pixel changes; both areas are consistent pixel by pixel when switching back to the original image and high definition. Dialogue events, owners, page numbers, reveal progress and content remain unchanged during cuts.
- 57 world map textures confirmed in both languages to reach 512×512 in RT64 actual cache, UV scaled 8x; native droplets drawn 1398 / 1608 times respectively. Manually check the completed GPU screenshots to confirm that Chinese/Japanese, original/HD and modern models are valid at the same time.
- It has been confirmed that the font in drawing is a runtime 504×504 atlas; the 504×252 file header of the original ROM resource 1 cannot be directly used as a judgment condition for drawing binding. The adaptation layer is identified according to the actual atlas. (Correction on 2026-10-03: The rare Chinese characters with font size ≥ 0x597 are indeed drawn from the 504×252 image of resource 1, and the adaptation layer recognizes both, see [portable-text.md](portable-text.md).)

Aggregate evidence: [acceptance.json](../../build/recomp/profile-check/acceptance.json). Screenshots: [Chinese original image](../../build/recomp/profile-check/live-zh-3/profile-checks/original.png), [Chinese HD](../../build/recomp/profile-check/live-zh-3/profile-checks/hd.png), [Japanese HD](../../build/recomp/profile-check/live-ja-3/profile-checks/hd.png). This time does not cover the full game, old Chinese save migration or physical keyboard automation; F6 and test requests share the same application path.