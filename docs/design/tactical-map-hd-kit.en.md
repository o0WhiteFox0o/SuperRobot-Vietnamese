> **Language / Ngôn ngữ:** [English](tactical-map-hd-kit.en.md) · [Tiếng Việt](tactical-map-hd-kit.vi.md) · [中文](tactical-map-hd-kit.md)

# Tactical Map HD: List reorganization, dynamic elements and image_gen generation package planning

2026-09-25. The HD basemap of the tactical map is drawn by Codex's image_gen (the same method as [Story World Map](../native/native-worldmap-regions-hd.md#改用-image_gen2026-09-25)). This article reorganizes the map list according to the caliber of "HD assets", confirms one by one how to retain the dynamic elements on the map in HD, plans the composition of the generation package, and gives the method of "pseudo-tile" terrain panel. The runtime mechanism follows [HD planning §3](hd-pipeline-plan.md#3-战术地图) (map 20 template), and the dynamic data one by one can be found in [tactical map list](../data/tactical-maps.md).

The numbers in this article are calculated by `build/content/map-dynamics.json` and ROM (window division is calculated using a one-time script, see §3.4), without running the game.

## 1. Map list (according to HD asset caliber)

Runtime assets are keyed by **layout number** (`native_map.cpp`'s `find_asset(layout)`), and the palette is not keyed. So the inventory object is not the 158 map records, but the layout to be drawn:

| Caliber | Quantity | Description |
| --- | ---: | --- |
| Map records | 158 | `map_assets` table |
| Different layouts | 154 | 0/138/139, 60/64, 66/157 Three groups of the same layout, only changing the color palette, one HD will automatically cover |
| Remove 25 pictures without static references | 131 | See [List §5](../data/tactical-maps.md#5-未找到静态引用的-25-张) for the list; although 138/139 is among them, it has the same layout as 0, so it is there by the way |
| Among them, 3D34 variant | 22 | Using the root graph as the base, only the changed grid is redrawn (§1.2), not the entire picture separately |
| **Want to draw the entire root picture** | **109** | 7 pictures are 320×240 single screen |

### 1.1 Root map by atlas family

Each of the 8 picture albums is of a painting style. Image_gen’s painting style samples are given by family:

| Atlas | Content (look at the picture and name it) | Root map | Map number |
| --- | --- | ---: | --- |
| 6228 | Ground: grassland, forest, city, road, river and sea | 60 | 0–6, 8–27, 29–33, 38, 40–43, 45–48, 51–59, 61–63, 65, 67–69, 71, 73, 119 |
| 6229 | Universe: starry sky, meteorite belt, colony, wreckage | 37 | 75–78, 81–102, 104, 105, 107–111, 113–116 |
| 6230 | Inside the fortress/asteroid base: gray structures and black holes | 5 | 7, 35, 37, 44, 72 |
| 6231 | Moon surface: craters, gray surface | 3 | 49, 50, 60 |
| 6232 | Desert and Nazca Paintings | 1 | 36 |
| 6233 | Clouds overlooking the coast | 1 | 66 |
| 6234 | Galaxy | 1 | 112 |
| 6236 | The surface under the clouds (single screen) | 1 | 74 |

Single screen root map: 65, 66, 73, 74, 81, 116, 119.

### 1.2 3D34 variant (22 photos)

Variants have the same dimensions as the root diagram, differing only in a few cells. Difference bounding box (grid):

| root graph → variant | difference grid number | bounding box (grid) | description |
| --- | ---: | --- | --- |
| 109 → 121, 123, 125, 127, 129, 131, 133, 135, 136 | 38–46 | x14–52 × y8–28, 39×21 | Scene 103 comic strip, 9 steps share the same bounding box |
| 111 → 141, 143 … 155 | 28–43 | Gradually growing from 8×4 to 22×4 (y12–15) | Scene 105 Comic strip, a horizontally growing strip |
| 111 → 156 | 42 | 26×10 (x12–37 × y6–15) | end of sequence |
| 37 → 39 | 5 | 3×2 | Scene 134 |
| 116 → 117 | 17 | 7×4 | Scene 38, single screen |
| 90 → 118 | 22 | 8×5 | Scene 54 |
| 104 → 137 | 17 | 6×5 | Scene 97 |

The even numbers (120–134, 140–154) in the sequence do not have static references, so we will not do it now; if the state table `8021E240` of 3D34 type 0 is found during operation, they will be cut to them, and they will also be filled according to the variant.

## 2. Dynamic element confirmation table

Each item lists vanilla mechanics, retention in HD, required assets, and status in the map 20 template.

| # | Dynamic | Vanilla Mechanics | HD Retention | Assets | Status |
| --- | --- | --- | --- | --- | --- |
| 1 | Palette cycle: water surface, light, lava, red pulsation, starry sky flash (67 pictures visible) | `8009CC0C` writes the next frame color into the map palette at each jump; `800945D4` reloads TLUT at each frame | Shader `底图 + (当帧色 − 参考色)[色号]`, the rhythm and pause gate control are naturally consistent with the original | Each picture has a 4x color number map (MMPX, only copies the original color number); the loop area is not handed over AI | Implemented |
| 2 | Invalid loop (28 pictures) | The loop resource is quoted but there is no corresponding color number in the atlas | The same mechanism as 1, the picture naturally does not move | None | Implemented |
| 3 | Colony rotation (39 pictures, 53 instances) | The universe map of mode byte 1 copies the next frame of 6235 (64×48, 8 frames) into the atlas (208,0) every 27 hops; frame number `80178C6D` | An 8-frame HD sprite is superimposed on the base map; the instance position is calculated from the layout when exporting (occupies 12 of this area of the atlas) grid number), write into `meta.json` | An 8-frame picture (§3.3) | To be done |
| 4 | 3D34 layout change (22 variants) | Overload layout, atlas, palette, aux, colony | Variant is another asset, automatically switched according to the layout number | Variant only draws the change grid (§3.3) | Runtime is supported; it needs to be verified whether two pictures are drawn in the same frame during the band transition (§7) |
| 5 | 3D34 Same layout changing palette (night scene/daytime, red light → darkening, full black) | Changing palette resources | Same mechanism as 1: shifting colors by color number pixel by pixel | None | Implemented |
| 6 | Scroll, vibration (3D36) | Lens integer pixel offset, vibration is the lens X swing | Each frame reading slot origin + `8010F5D4/D8` | None | Implemented |
| 7 | Fade in and out (3D3B) | Full-screen color block overlay | Drawn on the map, unaffected | None | Implemented |
| 8 | Overview scaling | `800943E0` Calculates scaling, `800945D4` draws the entire image to 266×200 with non-zero mode byte (subrecord + 3), skipping the outer 2-frame border | The same basemap is drawn in reduced size; mipmap is required | None | To be done (§5) |
| 9 | Terrain panel | `801E2D54` Take out the cursor grid from the atlas and enlarge it to 37×37 | Crop the 64×64 block of the cursor grid from the entire HD base map and use the same shader | None | To be done (§4) |
| 10 | Concentrated lines 610–612 | Same drawer `800945D4` | Identified by layout number, no takeover | None | Implemented |
| 11 | 2 dark borders in the outer circle (tile 1/2) | Part of the layout | Not handed over to AI; drawn by color number map + palette (i.e. pixel amplification) | None | Implemented |

The conclusion remains unchanged: all dynamics are reproduced at runtime by "color number map + current frame palette + changing assets according to layout number". The generated package only requires a static base map and a colony frame map.

## 3. image_gen generated package

### 3.1 Similarities and differences with the world map package

Follow the method of `assets/hd-ai/imagegen-kit` (`manifest.json`, one `*-input.png` + `*-prompt.txt` for each card, and put `outputs/`, README to the user). The new package puts `assets/hd-ai/tactical-kit`, and add a section of `maps` to the manifest. Differences:

- **Must be aligned by grid**. 16 pixels per frame ↔ HD 64 pixels. The window boundary only falls on the edge of the grid. Check it grid by grid after registration (§3.5), otherwise the terrain panel will not cut out the cursor grid.
- **The water surface and borders do not fit into the picture**. The cyclic color area in the input picture is given as it is (to let the model know that it is water), and the prompt word requires that it be drawn as a calm and uniform water surface; during synthesis, these areas will be discarded and replaced with a color map. The outer 2-frame border is cut directly from the input and does not occupy the screen.
- **Rotating colonies are excluded from static generated graphs**. The original input retains frame 0 as a position reference, and the prompt word requires that the body, ring, and mirror panel be erased and filled with nearby dark starry sky, leaving no silhouette or halo. The 8-frame animation is produced separately, and must still be processed according to the instance area when compositing and running; removing objects in the static image does not mean that the animation access has been verified.
- **Figure 2 by family**. There is currently no tactical map drawn by image_gen, so we first draw 8 family templates (§3.6), and after the user approves, cut out a portion to become Figure 2.

### 3.2 Composition of each root graph

| item | source pixels | input amplification | target output | quantity |
| --- | --- | --- | --- | --- |
| The whole image | The whole image after removing the borders | Nearest neighbor, the long side is about 1536 | The same scale as Figure 1, image_gen actually gives about 1.5 MP | 1 image per root |
| Local window | Usually 384×256 (24×16 grids), step 320×192 (overlapping 4 grids), the border window shrinks inward; map-054 narrow image is 368×256 | nearest neighbor 4 times | usually 1536×1024 (3:2); narrow image 1472×1024, always maintain the actual input ratio | See §3.4 |

The function of the entire map is the same as that of the world map package: the color and landform distribution of the entire map are determined, and it is also the base map when there is no window; the window adds 4 times the details. The same set of logic of `worldmap_surfaces.py imagegen` was used for synthesis (the whole image was registered as the base, the window was blended according to "the one farthest from the inner edge dominates", and the color above 48 HD pixels was rounded), changed to grid alignment and then moved to `tactical_map_hd.py`.

### 3.3 Variations and Colonies

2026-09-27: Variant pack has been generated from `tactical_map_kit.py build-variants` to `assets/hd-ai/tactical-kit-variants` (22 variants, 50 windows, ~81 MB). Figure 1 is a window cut out of the root image composite basemap (`runtime-integrated-v4` of Codex), with the changing grid replaced by hard pixels of the variant; Figure 2 is a white grid mask; only the changing grid is taken and 1 grid is added for feathering during synthesis. There are 4 windows for each of the 9 steps of scene 103, 1 for each of the 8 steps of 105, 2 for the final step, and 1 for each of the 4 local variants.

Variant synthesis `compose-variants`: Based on the root image synthesis base map, after registering the drawings of each window, only the variation grid is added and half-frame feathering is taken; the unpainted windows return to the color number image pixel enlargement (`pixel_fallback`), so there is a set of variant assets available before the Codex is completed. Cycle colors, borders, and colony blocks are restored according to the same rules for root graph synthesis, and colony instances and background color numbers follow the `tactical_colony_pack` of the Codex. The output is in `tactical-kit-variants/runtime/map-NNN`. The metadata is in the same format as the root graph run package. `layout` is the layout number of the variant itself. `runtime-all/` uses symbolic links to combine the root graph run package and variants into a directory for `SRW64_HD_MAPS`. Actual machine (`map-variant-view` mini level, 109 → 121 type 1): After switching, variant assets are drawn, all 131 assets are loaded, skipped 0, unmarked 0.

2026-09-27 Codex finished drawing 50 windows and re-ran `compose-variants`. All 22 pictures were converted to drawings (pixels rolled back 0 cells). The background color of the starry sky of the drawing is slightly different from that of the root image, and squares will be exposed on the feathered edge, so low-frequency color preservation is performed before compositing: the reference image takes the objects displayed in the variant original pixels in the change grid, and the rest uses the background of the root image interpolated from the surrounding unchanged area (`variant_reference`, radius 192 HD pixels) to avoid bringing in the brightness of the old object or the original pure black background. The remaining base color differs by 1–2 light levels. Actual machine 109 → 121 re-inspection skipped 0, unmarked 0.


- **Variation window**: Figure 1 = HD result of the root image (after synthesis), replace the changed grids back to the original image and enlarge the hard pixels; the prompt word indicates that only these grids will be redrawn, and the rest will remain unchanged. The synthesis only takes the transformation grid and adds 1 feather grid. Scene 103 has a bounding box of 39×21 cells over a window, 2 images per step; scene 105 has 1–2 images per step; 1 image for each of the 4 local variants. Approximately 32 photos.
- **Colony frame picture**: 8 frames of 6235 are assembled into a 4×2 picture (256×192 ×8 = 1024×384), which is completed in one request to ensure consistency between frames; the prompt word indicates that these are 8 phases of the rotation of the same colony, and the background starry sky must be consistent with adjacent frames. If the painting is not straight, return to MMPX to enlarge. 1 sheet.

### 3.4 Quantity and Binning

The generated package is generated from [`tactical_map_kit.py`](../../tools/hd_ai/tactical_map_kit.py) to `assets/hd-ai/tactical-kit` (generated on 2026-09-25: 109 whole pictures, 772 windows, 1 colony frame picture, about 99 MB, not entered into git). The window only covers the picture after the borders are removed. The entire single-screen map is 4 times larger, and the window is no longer cut. The README in the package states how to start with the sample first and divide it into 11 batches according to the order of the plot; a second package will be released after the variant version is finalized.

Divided according to the windows in §3.2, there are 109 root graphs with a total of 772 windows (the estimate before border removal is 904). I tried filtering out the pure background windows by clicking "Background Tiles in Grid Number Statistics", and could only remove 3: the grassland forest of the Ground family should have been redrawn, and the meteorite debris of the Space family is scattered throughout the map. So I can’t save it, I can only divide it into different categories:

| File | Content | Number of sheets |
| --- | --- | ---: |
| First level: whole picture | 1 each of 109 root pictures + family template included | 109 |
| Second level: Ground family window | 60 root pictures | 349 |
| Second gear: Universe family window | 37 root pictures | 339 |
| Second level: other 6 family windows | 12 root pictures | 84 |
| Variants + Colonies | | 33 |

The effect of using the entire image alone: the actual size of the large map is about 1.5–2.6 times, and the single screen is about 4.4 times; after zooming in to 4 times the canvas, it is much better than the nearest neighbor zoom in the original image, and the water surface is still clear by the color map.

**Suggestion**: Make the first stage (109 maps) first, with all maps having an HD version first; then make the second stage of the ground family (349 pictures, divided into 8 batches, each batch of maps with one chapter) according to the plot sequence; the starry sky of the universe family is a point light source, and the second stage has the smallest profit, so leave it to the end to fill in as needed. If you want to press the second level of the number of pictures, you can change the window to 3 times (512×341 source pixels → 1536×1024, no need to change the code when running `scale: 3`). The number of pictures will be reduced by about 40%, at the expense of the base image being slightly softer than 4 times.

### 3.5 Alignment Verification

Window registration follows `fit_scale` (least squares for two-axis scaling + translation). The tactical map also adds a square-by-square verification: shrink the registered window by 1 time, compare the average color with the original image square by square, and report the square with the largest deviation; the window with a deviation of more than half a square (8 source pixels) is redrawn. This is the correct premise for pseudo-tiles in terrain panels.

### 3.6 Family template and sequence

1. Each of the 8 families will have a full picture, and the 6 families with windows will have another window No. 01, a total of 14 pictures (20 on the ground, 87 in the universe, 35 in the fortress, 49 on the moon, 36 in the desert, 66 in the sea of clouds, 112 in the Milky Way, and 74 under the clouds); the two cloud families do not have another window. After the user approves, the window family will use the window as Figure 2, and the cloud family will use the entire image.
2. One file contains 109 whole pictures.
3. 1 colony frame picture (can be made after passing the universe family template).
4. The second level is divided into batches according to chapters.
5. Variations are made after their root diagram is finalized.

After each batch is completed, `export` will be used to view it on the actual machine; after the image quality is approved, it will be registered into the art list and into the full HD package.

## 4. "Pseudo tile" of the terrain panel

### 4.1 How to draw the original version (`801E2D54`, read from decompilation)

1. Record `800FFA74 + 槽×0xC4` from the panel sprite slot to get the panel origin (x, y); when recording +0x70 is equal to 0x495, it is a high version panel (the background rectangle is to y+0x5D), otherwise it is to y+0x44.
2. Read the grid word `80172ED8` of the cell where the cursor is located (the high half-word is the flip sign: 0x4000 mirror, 0x8000 flip up and down; the low half-word is the cell number), the atlas handle `801027E4`, the palette handle `801027E6`, and the data is obtained through `8008A11C`.
3. Grid number → Atlas coordinates: `sx = (t & 15)×8 + ((t & 0x300) >> 1)`, `sy = ((t & 0xF0) >> 1) + ((t & 0xC00) >> 3)`, the same as `map_dynamics.compose`; load 16×16, set mirror/flip according to the flag.
4. Draw a texrect from (x+4, y+5) to (x+41, y+42), 37×37 pixels, dsdx = dtdy = 0x1BA ≈ 16/37, that is, enlarged 2.31 times.

In other words, the panel displays the tile in the atlas, not the grid itself on the map; the two are the same thing in the original version, because the grid is a copy of the tile.

### 4.2 HD method

The HD basemap is drawn as a whole, and the same tile is drawn differently in different positions, so "tile" is changed to **the 64×64 block of the cursor's grid on the basemap**:

- Take the cursor `80102308/0C` from the pixel origin of the grid on the map (f32 map pixels, including borders; [Hold R to jump to the farthest grid](../native/move-jump.md)'s record is grid × 16+32). Crop uv = [cx/W, cy/H, (cx+16)/W, (cy+16)/H], W and H are the map pixel dimensions.
- Use the same `HdMap` shader to draw to the position of the original texrect, when the frame TLUT is read from the panel's own display list (look for `F0` after `FD` like the map). So when the cursor stops on the river, the water in the panel also circulates with the palette; the night scene palette also takes effect.
- When the cursor grid falls within the colony instance, the corresponding 64×64 sub-block of the colony sprite is stacked (the frame number also reads `80178C6D`).
- Don't worry about the flip flag: the base image is already in the composite orientation.
- When sampling, uv retracts half a texel inward to avoid bilinearity from bringing in the color of adjacent cells.
- If there are no assets for this layout or in original mode, it will not be rewritten and the original tiles will still be drawn.

### 4.3 Implementation and Verification (Completed on 2026-09-27)

The implementation was carried out according to the following steps, and the actual machine passed:

- Hook `load_000AB160_func_801E2D54 → srw64_original_terrain_panel_draw` (`generate_cpu.py`), wrapped in `game_hooks.cpp`, callback `srw64_game_hooks.terrain_panel_drawn(ram, begin, end)`, `host.cpp` receives `hdmap::rewrite_panel`.
- `rewrite_panel` of `native_map.cpp`: remember the most recently rewritten map asset (`current_map`), read the TLUT and the only rectangle from the panel display list, uv takes the cursor grid and retracts half an HD texel inward, and the mark is written on `SETTILESIZE` in front of the rectangle; colony overlay follows the Codex `project_overlay`, the frame number is also `80178C6D`. The count is written to `hd-map-summary.json` of `panel_draws` / `panel_unmarked`.
- **Triggering of terrain panel**: In idle state (`801C8B04`), press **B** on the space, `801CABAC` to open the window (scene 0x8E); stop the cursor on the unit and press B to open the unit window. The first time I ran, I didn’t capture the panel because I didn’t press B.
- **The cursor is the grid origin has been confirmed**: `801CABAC` Use `trunc(光标) >> 4` directly as the grid number (including the border) and check `801E2074`, which is 2 different from the game grid number of "grid=(v−32)>>4", which is exactly the 2-grid border.
- Verification script `tools/recomp/debug/check_terrain_panel.py`: In the move-jump level, move the cursor to the (11,8) road grid and (13,12) forest grid to open a window each, and take a screenshot of the HD and original versions; compare the panel tiles with the cursor grid and 8 adjacent grids on the HD base map. The cursor grid difference is 3.7 / 2.7, and the minimum adjacent grid is 6.4 / 14.1, the panel displays the cursor grid. When passing `map87-colony-view` to open a window in the colony tile, the phases of the colony sub-blocks in the panel are different in the two screenshots taken 1.6 seconds apart, and the original mode is still the original tile.

### 4.4 Original implementation steps

1. Add `load_000AB160_func_801E2D54 → srw64_original_terrain_panel_draw` to `NATIVE_HOOKS` of `generate_cpu.py` and generate it again (you need to run it manually after changing the table).
2. Add packaging to `game_hooks.cpp`: the display list pointer is at `*a0`, read it once before and after the call to get the range, and give it to `srw64_game_hooks.terrain_panel_drawn(ram, begin, end)`.
3. Add `native_map.cpp` to `rewrite_panel`: Find the only `E4` rectangle in the range, calculate the uv according to 4.2, and rewrite it using the existing mark + ring recording mechanism; the current layout number takes the value recorded in the most recent map rewrite.
4. Verify the script `tools/recomp/debug/check_terrain_panel.py`: Use the debugging interface to place the cursor on the river, city, border, and colonial grid in sequence, take a picture of each, and compare the panel area with the corresponding block of the base map (reduced to 37×37). The registration offset should be 0.

## 5. Overview zoom

2026-09-27 Completed and verified on actual machine. **The entrance is to press C-right on the idle map** (B to exit); the keyboard debugging interface does not map this key, so you need to use the N64 key name `c_right` called by `buttons`. The troop table (C-top, `801CB1B4`) is just pre-calculated and scaled and stored in `80172EF8`, and the unit drawing `801E21F8`/`801E26C0` is scaled by it in the overview.

Rewrite the entire path (`MapDraw.overview`, judged by the sub-record +3), uv inverts the skipped borders based on the actual number of grids and rows drawn, the basemap texture has a box filter mip chain (calculated in the decoding thread), and the sampler turns on mipmap. `check_hd_overview.py`: The overview of map 20 occupies the same screen frame (864×1008 screen pixels) in HD and the original version, the unit position is consistent, and the overview is drawn 75 times without skipping.

Original design:

`800945D4` shrinks the entire map (excluding the outer 2 cells) to 266×200 when the mode byte is non-zero. Now `host.cpp` directly skips rewriting when encountering this kind of drawing. HD method:

- Rewrite the same path, mark the rectangle and take the bounding box of all rectangles, and the uv is fixed to [32/W, 32/H, (W−32)/W, (H−32)/H].
- Basemap texture generation mipmap (now only one layer), otherwise the 4x basemap will flicker when reduced to 1/13. The color number map cannot be mip. During the overview, just press the nearest color number to get the translation amount. The color of the water surface area is still the same as the frame.

## 6. Acceptance

- Use `SRW64_HD_MAPS` after each batch of `SRW64_HD_MAPS`. See the actual machine: roll to the four corners and cut one piece off, and the offset from the original registration is 0 (method of map 20 sample).
- Select a map for each of the water surface, flash mob, and colony to record a segment, which is consistent with the original frame-by-frame rhythm.
- The terrain panel is checked according to step 4 of §4.3.
- Night scene/day scene (scene 90/102 to 60/64/157 switching) color follow on real machine.

## 6.5 Access to the game (2026-09-27)

- **Asset package**: `tactical_map_kit.py pack` Copy the root map run package and variant (`runtime-all`, unzip the symbolic link) into `assets/hd-ai/tactical-maps/pack-v1`: 131 maps each have `base.png`, `index.png`, `meta.json`, plus 8 Frame colony, `tactical-maps.json` records the SHA-256 of each file.
- **Art Manifest**: `content/art/stage1-hd.json` Added `tactical_maps` (path plus manifest summary). `compile_art` File-by-file verification: `art/maps` is copied when packaging, and development operation (`profile.py`) does not copy and directly points to the asset directory; both write `art/srw64-tactical-maps.json`, `root` is the relative `maps` or absolute path.
- **Host**: When `SRW64_HD_MAPS` is not set, the map directory is found from the index of `SRW64_ART_PACK`, so the launcher, self-use full HD package, and development run of `--images hd` will be automatically brought. The map is changed to load on demand: when a certain layout is drawn for the first time, it is handed over to the decoding thread (counted together with the mip chain). The game thread waits for up to 400 milliseconds. According to actual measurements, the first frame after entering the level is HD; about 900 maps that are not used in map drawing use `gpu::retire` to release the texture in the rendering thread, and then decode it next time (`SRW64_HD_MAPS_EVICT_AFTER` is adjustable, for checking). In the past, all maps were decoded into memory at startup, which was about 4 GB.
- **Full HD package for your own use**: `compress_hd.py` converts the map basemap to JPEG (quality 95), `meta.json`'s `base` points to `base.jpg`, color map and colony frame remain PNG; map part 1.0 GB → 350 MB, the entire HD directory is about 708 MB.
- **The public package also comes with** (2026-09-28 user-defined: the public HD package is the same as for personal use): the color number map and the loop area pixels are enlarged from the original map pixels. This is stated in the NOTICE and release notes. Previously, `build_release.py` listed `art/maps` into `ROM_DERIVED` and deleted it from the public package, which has been cancelled. Basemap JPEG quality 92, 4:2:0 (`compress_hd.py`), map portion approximately 236 MB.
- **Verification**: `test_tactical_maps_pack.py` (verification and compression), `test_hd_release.py`; the actual machine used the JPEG map in the self-use package to run the terrain panel (176 times) and the colony (8 frames), and used the development path to run the overview and 109→121 switch (released 1 time). There was no skip or decoding failure.

## 7. To be verified

2026-09-27 Verified **3D34 image change transition** (`map-switch-view` mini-level, map 9 → 62, type 0): The old image is blackened every other line, completely black in one frame, and the new image is displayed in alternate lines. The two maps never appear in the same frame, and the HD rewriting process is normal (skipped 0, unmarked 0). The variant sequence uses type 1 (instant switching) and does not have this problem. Remaining:


- `8021E240` Whether the state table will switch to the even-numbered map in the sequence.
- How to trigger overview zoom (the writing point of `801027DB` was not found), and how to enter the overview on the actual machine.