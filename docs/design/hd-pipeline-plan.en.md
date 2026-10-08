> **Language / Ngôn ngữ:** [English](hd-pipeline-plan.en.md) · [Tiếng Việt](hd-pipeline-plan.vi.md) · [中文](hd-pipeline-plan.md)

# HD: Current status, access methods and follow-up

Drafted on 2026-09-23, rewritten according to actual implementation on 2026-09-24. The product boundaries follow [Built-in MOD Roadmap](mod-roadmap.md) §6 (Original / HD can be rolled back item by item, and the original image will be used if any item is missing). For full ROM resource inventory and Alibaba Cloud model selection of each type, please see [HD Asset Inventory](../data/hd-asset-inventory.md); for the dynamic effects of tactical maps one by one, please see [Tactical Map List](../data/tactical-maps.md).

The art list is `content/art/stage1-hd.json`. The development profile defaults to `images: original`. HD needs to be started with `--images hd` or press F6 in the game.

Full HD self-use package (2026-09-24) starts from HD. For the method, see [macOS build · Full HD self-use package](../native/macos-release.md#全-hd-自用包):
- [`prepare_hd_bundle.py`](../../tools/release/prepare_hd_bundle.py) Compile the art list and copy in the verified ship model package and 5600 mark package;
- `package_macos.py --hd` Put it into the application; the launcher sees it and opens the HD and two model packages.

This package is for local use only and is not distributed. Tactical maps (from 2026-09-27) are included in the package with the art list, and the basemap is saved as JPEG.

## 1. Current situation

| Category | Practice | Status | Documentation |
| --- | --- | --- | --- |
| Character avatars (300 pictures, the other 4 protagonists) | The whole picture is drawn by the host, 768×768 | Accessed | [Character avatars HD](../native/native-portraits-hd.md) |
| Interfield background (8 pictures, light/dark) | Host draws the whole picture | Connected | [Interfield background HD](../native/native-backgrounds-hd.md) |
| Title Logo and flames | Host whole frame drawing (scene sprite) | Connected | [Title screen and plot text image](../native/native-title-and-story-images.md) |
| Title menu, chapter title card, prologue, ending, credits | Native text, following language | Connected | Same as above |
| Story world map (surface 5602–5606, universe 5599) | RT64 hash replacement, 512 px slice; starry sky drawn in its entirety | Accessed | [story world map HD](../native/native-worldmap-regions-hd.md) |
| World map ships, landmarks, tracks | Native models | Accessed | [World map cutscene model HD](../native/native-ship-model.md) |
| 5600 plot map markers | Native model | Accessed | [Model replacement](../native/native-model-replacement.md) |
| Dialog box border | RT64 hash replacement, redraw according to original design code | Connected | [Dialog box HD border](../native/native-dialogue-runtime-hd.md) |
| Tactical map (131 layouts in use, including 22 3D34 variants) | The whole map is drawn by the host, color number map + real-time palette; 8-frame coverage of the colony; the terrain panel and the overview have the same base map | Art list and HD package have been connected (2026-09-27; the public package will also be included from 2026-09-28) | §3, [Generation package planning](tactical-map-hd-kit.md) |
| Aircraft identification (320 map unit icons) | MMPX×2 → Local ESRGAN → Hard quantization 32 → MMPX×2, 64×64 color map; RT64 hash replacement, one copy for each camp | Accessed (local package, not included in the public package) | [Aircraft identification HD](unit-icon-hd.md) |
| Combat: sprites, special effects, cut-in, 3D background | — | Suspended (decided on 2026-09-23) | Same as above |

## 2. Four access paths

### Host entire drawing

Used for scenes where "the original split a large picture into many pieces": avatars, backgrounds between scenes, title frames, and tactical maps.

- The game issues chunking commands as usual.
- The host recognizes which picture is being drawn this time, suppresses the original blocks, and draws the entire high-definition picture at one time in the same position and in the same drawing order of the same command buffer in RT64 (the layer of the entire picture has been changed to plume, see [Three Platforms Porting Plan](three-platform-port.md) X1).
- Benefits: There are no seams between blocks; versions with different palettes do not need to be hashed block by block; the picture is not limited by the original cutting method.
- Identify RT64's native drawing hook (`NativeMeshHooks`). Both TRI1/TRI2 and texrect call classify, and each module is hung behind it in a chain.
- Implementation:
- Avatar: `native_portrait.cpp`
- Inter-field background: `native_background.cpp`
- Title and other scene sprites: `native_sprite.cpp`
- Tactical map: `native_map.cpp`

### RT64 texture hash replacement

Used for scenes that are inherently independent of small textures and hash stable: 64 px blocks of world map surfaces, universe objects, dialog slices.

- Key is RT64 v5 content hash, computed offline by [`rt64_hash.py`](../../tools/hd_ai/rt64_hash.py).
- The manifest allows four categories: `worldmap`, `frame`, `space`, `icon`; `icon` (aircraft identification) is redrawn from the original pixels and will be included in the public HD package together with other categories from 2026-09-28.
- Don’t use this method if the color palette changes, the same block appears in multiple places, or if replacing content by block leaves seams.

### Native model

For 3D display list: 5600 markers, world map ships and landmarks. `native_marker.cpp` Identify the original DL, suppress it, and draw the host mesh.

### Native text

Text used for baking in images: title menu, chapter title card, prologue, ending, credits. The text is rearranged according to the reading language, and the scaling, rotation, and flipping movements of the original version are retained.

## 3. Tactical map

The map has palette cycling (water, light, lava), colony texture frames and 3D34 full map swaps, see [Tactical Map List](../data/tactical-maps.md) for details. The textures in these areas change every hop, and hash replacement does not work here, so the host draws the entire frame, and the color is taken from the game frame palette.

### Runtime (`src/host/native_map.cpp`)

1. **Hook**: After the map drawing function `800945D4` is executed, `game_hooks.cpp` hands over the display list range, slot and sub-record written this time to the host.
2. **Identification**: The host reads the layout number from the sub-record and only takes over the map layout with HD assets; other sprites drawn by the same renderer such as concentrated lines do not move.
3. **Rewrite**: It will not be rewritten in the original mode, when there are no assets or when the recognition fails. Otherwise:
- Read out the TLUT address and capture 256 colors of the current frame;
- Calculate the map coordinates using the bounding box of each rectangle and the camera offset (slot origin + `8010F5D4/D8`);
- Leave a marked rectangle in the display list and leave the rest blank. Texture loading and status commands remain unchanged.
4. **Drawing**: RT64 calls back the host when it processes this rectangle, and the host calculates (`src/host/shaders/HdMapPS.hlsl`) `底图 + (当帧色 − 参考色)[色号]` in pixels. When the palette remains unchanged, the base map remains the same; when the water surface changes frames and the palette changes, the colors follow the game.
5. **Asset**: `SRW64_HD_MAPS` points to the output directory of `tools/hd_ai/tactical_map_hd.py export`. One subdirectory per map containing the 4x basemap `base.png`, the 4x colormap `index.png`, and the `meta.json` with reference palette.

Pitfalls: The `screenScale`/`screenOffset` drawn by RT64 for a rectangle is relative to the scope of the rectangle itself, not the entire screen. The entire map must be converted directly to the full-screen N64 coordinates, otherwise it will be stretched horizontally and "breathe" when scrolling.

Validation of map 20 template:
- Take a screenshot at the same position and after scrolling to the bottom. The registration offset between HD and original version will be 0 in the entire screen.
- The upper screen rhythm is the same as the original version: one frame every 33 ms, up to 38 ms.
- Judgment fluency is no longer affected by diagnosis: the "Complete Diagnosis" that periodically screenshots 5K pictures and exports memory has been deleted on 2026-10-01 (it will cause 200-270 ms of lag).

### Offline production (`tools/hd_ai/tactical_map_hd.py`)

1. **`prepare`**: Create a 1x color code map and original image according to the layout, generate an animation mask and a border mask, use MMPX to enlarge the color code map 4 times, and freeze a request.
2. **Request**: `python -m tools.hd_ai.aliyun` Send once, each output directory has a budget limit.
3. **`compose`**：
- Overall amplification and inverse transformation of the fitted model output by two axes. Qianwen will put about 0.2–0.5% of the content.
- Color preservation: Only the high-frequency details of the model are taken, and the low-frequency colors continue to be used in the original image.
- The result of using no model for the animation area and outer border.
- Output comparison report and water surface loop preview.
4. **`export`**: Write out runtime assets.

Map 20 (448×512) can produce the entire 1792×2048 map in one request; the final choice was `qwen-image-3.0-pro`.

### To be done

For the reorganization of the generation package and map list, the dynamic element confirmation table, the terrain panel and the overview, please see [Tactical Map HD Generation Package Planning](tactical-map-hd-kit.md) (2026-09-25).

- **Coastline Smoothing**: The color number map is enlarged by pixels, and the coastline is still stepped. The boundary needs to be smoothed and then aligned with the land drawn by the AI.
- **Large image is divided into windows**: 135 of the 155 layouts exceed 2048² after being enlarged 4 times. They need to be generated in separate windows, with overlap, and then combined in the protected area.
- **Colonial Elves**: Set of 8 frames, frame number reads `80178C6D`.
- **3D34 variant**: Based on the previous step, only the changed grid is redrawn.
- **Overview Zoom and Terrain Panel**: Overview Zoom (`800943E0`) and Terrain Panel (`801E2D54`) still draw the original grid.
- **Advance order**: First make a map with a large water area (56, 13, 16, 46, 15), and then make two comic strip sequences.

## 4. Production tools

| Tools | Purpose |
| --- | --- |
| [`aliyun.py`](../../tools/hd_ai/aliyun.py) | Freeze the single sending of the request: write the request record before sending, do not retry POST, each output directory has a budget limit; `load_env` Read the DashScope key in `.env` |
| [`rom_images.py`](../../tools/hd_ai/rom_images.py) | ROM palette and color map decoding |
| [`pixel_scale.py`](../../tools/hd_ai/pixel_scale.py) | Only copy the pixel art enlargement of the original color number (MMPX, Scale2x) for use in color number diagrams and body identification |
| `portrait_batch.py`, `build_portrait_images.py`, `build_portrait_review_site.py`, `portrait_matte.py` | Avatar: 2×2 puzzle generation, frame-by-frame registration, cutout, entire output and image review station |
| `background_hd.py` | Background between scenes |
| `title_hd.py`, `flat_scene_hd.py` | Title Logo, Flame and Flat Color Block Scene |
| `worldmap_surfaces.py`, `worldmap_space.py` | Plot world map surface and universe |
| [`dialogue_frame_asset.py`](../../tools/hd_ai/dialogue_frame_asset.py) | Dialog border slicing |
| `tactical_map_hd.py` | Tactical Map |

Common process: freeze request → single transmission → registration and color preservation → protected area synthesis or cutout → export → update list (attached with SHA-256) → actual machine comparison. Generated graphs, request records and intermediate files are all placed in `assets/hd-ai/` which is not included in git. For directory description, see `assets/README.md`.

## 5. Follow-up

1. **Tactical Map**: Completed and accessed (see [Generation Package Planning](tactical-map-hd-kit.md) §6.5). The only remaining features are coastline smoothing and whether the public package will generate color maps from ROM at runtime.
2. **Body ID**: Accessed ([Body ID HD](unit-icon-hd.md)); the remaining shadow ellipse 687 has not been changed.
3. **Combat**: Suspended. When restoring, the sprites and special effects are mastered according to the atlas and then cut into parts, and the 3D background is replaced with textures and added with native geometry.
4. **Widescreen**: The entire drawn picture can be drawn wider than 4:3 in the future, but this must be done after the widescreen container is implemented.