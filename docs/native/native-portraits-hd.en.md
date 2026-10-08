> **Language / Ngôn ngữ:** [English](native-portraits-hd.en.md) · [Tiếng Việt](native-portraits-hd.vi.md) · [中文](native-portraits-hd.md)

# avatar HD

2026-09-24. All character avatars have been generated as high-definition masters, cut out to transparency, and connected to the game as **entire images**: each avatar is a 768×768 image, and the host draws it all at once in the position where the avatar is drawn in the game, without replacing textures in 32×32 small blocks. For the cutout method and problems with the old version, see [Original and High-Definition Images](native-content-foundation.md#原图与高清图).

## Scope

- Character table `0x84220` assigns one set (image, palette) to each of the 361 identities, for a total of 338 sets, involving 300 different images (Resource 9–308). There are also 4 main character portraits 1308–1311, with palettes 1312–1315, used by `save_page.cpp`.
- Each picture is only generated once according to the basic color palette:
- The basic palette is "picture number + 300", 294 of the 300 pictures are like this;
- 259–264 These 6 pictures are matched with misaligned palettes (559–564) in the table and inside, as shown in the table;
- The remaining palettes are considered variants, derived from the HD results and not generated separately:
- 609 is the silhouette palette, with only one dark gray (41,41,41), used in 34 images;
- No. 134 universal face is borrowed from four other sets: 309, 313, 392, and 515.
- The palette has only 64 colors, transparency No. 0; the image is CI8 96×96 (232 pictures) or 97×97 (68 pictures).
- 29, 33, 166, and 169 that have been reviewed in the first episode will not be generated again. This time, there are 300 photos in total.

## Generate

[`portrait_batch.py`](../../tools/hd_ai/portrait_batch.py)'s `prepare` is decoded from ROM, freezing input and prompt words; `run` sends requests in sequence, and the bottom layer is `run_benchmark.run_one` (reserved fee, not automatically repeated POST).

- Model `qwen-image-3.0`, output 2048², seed 640903, the same as the reviewed single avatar.
- Each request is a 2×2 puzzle: gray background (100,100,112), 16 original pixels in the grid, and the input is enlarged 6 times by nearest neighbor. Group by size (separate group of 97 px), sort by resource number within the same size, characters of the same work are mostly together.
- A total of 15.0 yuan for 75 requests (estimated public price, priced per piece). `400 InvalidParameter` was sent 12 times on the way, all of which were returned within 2 seconds, without charge, and the resend was successful. Rejected records are moved to `rejected/` for retention.
- Approximately 819 px per cell, which is larger than the 768 px of the 8x master. 3×3 only has about 560 px per square, so don’t use it.

First, we did a comparative test using 4 reviewed avatars (`grid-test-1`):
- After the 2×2 gray background is reduced to its original size, the difference from the original image is 8.1 / 9.0 / 9.8 / 6.7, and the reviewed leaflet is 14.8 / 10.4 / 10.1 / 5.9;
- The solid green background (0,255,0) is the furthest away from the character's color, but the model enlarges each grid and fills the space, so there is no need to key the background with a solid color.

## Alignment and cutout

The model treats each cell differently: 3–10% magnification, translation up to 7 native pixels, and beveling for some cells (number 14 is 5 native pixels above and below). So `compose` frame-by-frame registration:

1. Find the displacement of the whole grid at half resolution;
2. Around this displacement, use a 32 px window to match block by block, and least squares fit the complete affine transformation (6 parameters);
3. According to the transformation of this grid, 8 times the master is resampled from the entire output, and the content that overflows into the grid can also be retrieved;
4. Leave it to [`portrait_matte.py`](../../tools/hd_ai/portrait_matte.py) for fine registration and cutout.

Fine registration residuals between 3–5 px (runtime pixels, 4 px equals 1 original pixel) are marked as "local deformation" for review, and those exceeding 5 px are rejected. The cut-off edge of the picture frame only checks the position that is more than 2 original pixels away from the transparent area of ​​the original image, and the closer position is considered as outline floating.

## Result

- All 300 images were cut out, the median IoU of the contours was 0.991, and the lowest was 0.935 (1310 spiked hair). The difference from the original image after shrinking to the original size, the median is 8.8 and the maximum is 17.5.
- After simulating non-premultiplied bilinear amplification, the pixels with edge deviation exceeding 16 levels: 292 pictures have 0, 8 pictures have 1–87, all on the 1-pixel dark line at the bottom of the 97 px image.
- I have manually read it page by page, and there is nothing that needs to be redrawn.
- On No. 14, I once thought that I drew a closed mouth instead of an open mouth, but the original picture originally showed an open mouth, so I kept the first version. The version that was redrawn by pressing Shut Up (`redo-1`) was not used.
- 196, 200, 1310 are marked as local deformation, and there is no problem in viewing the picture.
- The review pictures are in `assets/hd-ai/portrait-batch/full-1/review/page-01.png`–`page-15.png`, 20 pictures per page, the original pictures are side by side with HD, and the background is blue background of dialogue box. Reported as `report.json` in the same directory.

**The spaces around the frame are gray. ** When the model draws a puzzle, it often stops at a place that is one or two original pixels away from the edge of the grid, so the edge where the picture frame is cut off will leave a gray space between the grids (130 out of 300 pictures). When cutting out the image, look for up to 3 original pixels in the opaque position of the original image on the edge of the frame: if there is only background gray in the middle (plus a transition of up to 3 pixels), extend the first solid color to the edge; the gray clothes are originally there. After processing, there are only 6 pictures left with more than 10%. The pictures are all gray content such as circuit boards and gray armor.

## Access the game

### How to draw an avatar in the game

All avatars are drawn in Sprite Mode 7. Several loading functions that read the character table `0x84220` build sprites like this: dialogue `8008F970`, and `801C6350`, `801CB4D0`, `801CD718`, `801C3280`, `801C8D74` in overlays such as battles, tactical maps, openings, etc. The calling form is `80098158(槽, 0, 7, 0x8D, …, 图像, 调色板, 2)`, and the drawing function is `800964E4`. Static reading results:

- First add `SETTIMG` (`FD10`, RGBA16) to `LoadTLUT` to load the 64-color palette.
- Use two more constant loops (`y`, `x` take 0/32/64) to draw 3×3 blocks. Each block is `SETTIMG` (`FD48`, CI8, width capture image header), `LoadTile` 32×32, `SETTILESIZE`, `TEXRECT`. **The 97 px picture only draws the upper left 96×96, and the 97th row and 97th column are never drawn. **
- `E3000C00 / 0` turns off texture perspective correction; `E3001001 / 8000` sets TLUT to RGBA16. The filtering method is not set in this function.
- Toggle flag in subrecord +0x14. When flipped, the S of each block starts from 32 and is drawn by tile mirroring, and the texture content remains unchanged.
- The sprite is recorded in `800FFAAC + 槽×0xC4 + 子×0x30`, +0xC/+0xE stores **resource handle** (actually measured decimals such as 17, 18, 19, and 20), not the ROM resource number.

### Replace the entire sheet

[`native_portrait.cpp`](../../src/host/native_portrait.cpp) Follow the method of tactical map (`native_map.cpp`):

1. `generate_cpu.py` Rename `800964E4` to `srw64_original_portrait_draw`, wrap `game_hooks.cpp` one layer, and note the display list range written this time.
2. Identify avatars on the game thread: The handle is unreliable, so directly calculate the FNV-1a 64 summary for the pixel pointed to by `FD48` (96² or 97² bytes) and the palette pointed by `FD10` (128 bytes), and use (pixel, palette) to look up the list. The basic palette finds the color picture; the silhouette palette 609 finds the same picture and uses (41,41,41) for coloring instead. There is a pair of images with the same pixels but different palettes, so the key must be used for both.
3. Rewrite only if there are 9 rectangles that add up to exactly 96×96 and are not scaled: the last rectangle is changed to a tag that covers the entire avatar, the `SETTILESIZE` in front of it is changed to a numbered G_NOOP tag, and the remaining 8 rectangles are left blank. In other cases, keep the original drawing.
4. RT64 recognizes the label when constructing drawing, calls the host callback at the same drawing sequence position, and draws a rectangle through Plume (`src/host/shaders/HdPortrait*.hlsl`):
- Texture is premultiplied alpha, with mipmap, linear sampling;
- Mixing method One / OneMinusSrcAlpha;
- Swap UVs left and right when flipping.
5. The texture is decoded on first occurrence (~10 ms) and the mipmap is generated. After more than 64 photos are stored, the ones not used for 20 seconds will be released.

In the original image mode (F6), no rewriting is performed, and the game is drawn as it is. This path goes through Plume like other HD layers, and is available under both Metal and Vulkan (Vulkan has been tested with MoltenVK on Mac, and the actual Steam Deck is to be tested, see [Three Platforms Porting](../design/three-platform-port.md)).

### Resources

- [`build_portrait_images.py`](../../tools/hd_ai/build_portrait_images.py) Crops the upper left 768×768 from the 8x master (96 px master is 768, 97 px is 776), outputs `assets/hd-ai/portrait-batch/whole-v1/portrait-<图号>.png`, a total of 304 sheets, 183 MB.
- Also generates `portraits.json`, recording the SHA-256, pixel digest and palette digest of each image, as well as the silhouette palette digest and color.
- `--bind` Add the `portraits` section to [`stage1-hd.json`](../../content/art/stage1-hd.json), and remove the original avatar slice entries, leaving only 70 world map and dialogue border replacements.
- `compile_art` After verifying the summary, copy the graph to the running directory `art/portraits/`, write `srw64-portraits-hd.json`, and the host reads it from here.
- The four color palettes borrowed by No. 134 are all messed up, and they should be unused placeholder entries. The original images should be retained.

### Actual machine (2026-09-24, HD mode)

- In the opening demo battle, Ryoma's avatar is in full HD.
- In the mini-level of Episode 8, the dialogue avatars of Bioti, Jia'er, Wan Zhang, Garrison, and Lijia are all in HD. When using double-frame dialogue, the upper and lower frames are replaced.
- F6 can switch back and forth between HD and original images.
- Exit count (`hd-portrait-summary.json`):
- 6977 avatar drawings were rewritten;
- Content recognition did not fail once;
- RT64 draws two targets per frame, so native drawing is twice the number of rewrites;
- 22 pictures decoded in total.
- Another 713 drawings are kept as they are, all of which are "texture width 3": there are no initialized protagonist group avatars (アーク, Lu, Era, characters 25-32) in the mini-level, and they are also garbled in the original image mode, which has nothing to do with HD.

### Native page

The pages taken over by RmlUi also use this set of HD avatars: pre-battle confirmation, のりかえ, ability check, データセーブ, リンク and name page.

- When preparing to run the configuration, `assets.portrait_lookup` finds the entire avatar by (image, palette):
- The basic palette directly uses the images in the compilation directory;
- Silhouette palette 609 is filled in (41,41,41) according to the original image Alpha. Each image is only generated once and placed in the running directory `portraits/`;
- Other palettes (4 sets borrowed from 134) are not available in HD.
- `battle_assets` adds `hd` to 357 of the 361 identities; `name_assets` adds `hd` to the 8 opening cards and 8 combo cards. No. 33, which was originally registered separately in the name page coverage list, is no longer needed. That list was deleted on 2026-09-24.
- The page displays HD when the currently applied image mode is HD and the entry has `hd`, otherwise the original image is displayed. The cache key of each page contains this mode, and the page will be regenerated after switching.
- RmlUi sampling without mipmap, directly reducing 768 px to 56–160 dp will produce aliasing. Therefore, `frontend.cpp` performs an average area reduction according to the actual display width (dp × current density, or the pixel unit of the inter-field page) when loading, calculates based on premultiplied Alpha, and caches one copy of each size. The original image is 96 px smaller than the displayed size and is loaded as is.

Actual machine (2026-09-24, `battle-ui` mini-level): The two driver avatars on the pre-war confirmation page are clear and full images in HD; use the settings to switch to the original image and then switch back, the avatars will switch accordingly, and the two HD screenshots are consistent pixel by pixel. When the pre-war confirmation page is opened, F6 is blocked by the button received by the page, switching to go to settings. The other pages share the same set of image capture and reduction codes, and there are no actual screenshots one by one.

### Cutting plan used

Initially, RT64 texture hashing was used: 9 blocks of 128×128 for each face, 3037 blocks in total, covering the base and silhouette versions of 304 images. The hash can be calculated offline, and all 72 blocks captured in the first episode match. The rules are as follows:
- Odd lines are swapped by 4 bytes;
- Each used palette item is repeated 4 times;
- The last parameters are (32, 32, 32768, 4, 1, 2).

After changing to full replacement, this set has been deleted.

## Command

```sh
.venv/bin/python -m tools.hd_ai.portrait_batch prepare --output assets/hd-ai/portrait-batch/full-1 --skip 29 33 166 169
.venv/bin/python -m tools.hd_ai.portrait_batch run --output assets/hd-ai/portrait-batch/full-1 --env-file /path/to/.env
.venv/bin/python -m tools.hd_ai.portrait_batch compose --output assets/hd-ai/portrait-batch/full-1 [--only grid-058]
.venv/bin/python -m tools.hd_ai.build_portrait_images --batch assets/hd-ai/portrait-batch/full-1 \
  --reviewed assets/hd-ai/portrait-matte/v2 --output assets/hd-ai/portrait-batch/whole-v1 --bind
```

Groups that already have request records will not be sent again. `compose` and `build_portrait_images` cost no money and can be run repeatedly; the output directory of the latter must not exist. After changing the `generate_cpu.py` hook, you must rerun it first and then build the host.