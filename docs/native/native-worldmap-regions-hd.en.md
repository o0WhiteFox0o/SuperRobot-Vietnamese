> **Language / Ngôn ngữ:** [English](native-worldmap-regions-hd.en.md) · [Tiếng Việt](native-worldmap-regions-hd.vi.md) · [中文](native-worldmap-regions-hd.md)

# Story World Map HD: All areas

2026-09-24. The background between scenes in the plot is drawn by the world map overlay (`load_000A7EC0`), and now all areas are HD. Starting from 2026-09-25, all four surfaces are redrawn by Codex's image_gen ([use image_gen](#改用-image_gen2026-09-25)), and the painting style follows the image_gen version of Europe in the first episode ([World Map HD](native-worldmap-hd.md)). Starting from 2026-09-25, Europe will switch to Bailian. Please add details to the image_gen version. See [Europe switches to Bailian](#欧洲改用百炼2026-09-25).

## What areas are there?

The model object table `801C5670` lists the surface of each region. The location table `801C5310` has a total of 127 items, each item has three signed half-words (surface = model table subscript, x, y), see [Mini Level](../script/mini-stage.md). There are 827 times (661/166) of `3D32`/`3D33` in the script, statistics based on location:

| Resources | Content | Number of locations | Number of targeting | How to |
| --- | --- | ---: | ---: | --- |
| 5599 | Universe: starry sky, earth, moon, meteorites, two small facilities, name tags | 32 | 369 | The starry sky is drawn entirely, the rest are replaced by RT64, and the name tags are redrawn according to language |
| 5602 | Entire Earth | 28 | 184 | 6 windows generated |
| 5603 | The entire Earth (same tile-by-tile as 5602, just a different grid) | 29 | 164 | Shared HD with 5602 |
| 5606 | North America | 22 | 70 | 9 windows generated |
| 5604 | The Mediterranean, Europe, the Middle East, and North Africa (Chapter 1) | 10 | 28 | image_gen version 1, details of Bailianbu, 9 windows (2026-09-25) |
| 5605 | Central Asia, India | 6 | 12 | Generate 8 windows |

Each region of the Earth is a tiled grid of 64×64 CI4 tiles, each with its own 16-color palette; the transparent sea displays the clear screen color RGB(0,55,90).

## Earth's surface

[`worldmap_surfaces.py`](../../tools/hd_ai/worldmap_surfaces.py):

- `prepare`: Put all the components in each area into one picture according to the grid vertices (north facing up), cut it into a 256×256 window with an overlap of 48, and enlarge the nearest neighbor 8 times as input (2048²).
- **Painting style reference** (Picture 2): Take four pure land textures (forest, mountain, sand dune, desert mountain) from the reviewed HD picture of Europe in the first episode, and put them together into a 1024² sample.
- Initially, a map of Europe is directly used as a reference, and the model will copy its coastline: the Central Asian window becomes the Mediterranean Sea, and there is an extra desert continent in the Pacific Ocean.
- After giving only the texture and not the coastline, we will no longer copy it.
- `run`: Model `qwen-image-3.0-pro`, one page is displayed in each window, and then automatically checked:
- Reduce the output to its original size, compare the distribution of land/ocean (IoU) with the original image, ignore 1 original pixel on both sides of the coastline (the model will draw a circle of shallow water along the coast);
- If it is lower than 0.90, change the seed and redraw, up to 3 times, and take the best one;
- The copied output is only 0.34–0.84, while the normal output is above 0.90.
- `compose`:
- Each window is registered to the original image grid according to zoom and translation;
- Linear transition in overlapping areas to form a whole picture;
- The coastline is enlarged and smoothed using the original image mask, and the sea surface remains clear and transparent.
- The painting style originally requires changing the color, so the low-frequency color of the original image is not locked by default (`--colour-lock` can be turned on).
- `pack`: Cut the original block coordinates into 512×512, and use `rt64_hash.map_hash` to calculate the RT64 key of each block:
- 5603 and 5602 share the same HD image;
- The entire sea tile is left with a clear screen color;
- The same key corresponds to two different contents, there are 2 blocks, keep them as they are;
- The 57 pieces reviewed in the first episode will remain intact (before 2026-09-25).

Result: 152 new blocks, plus 57 blocks already reviewed, for a total of 209 map replacements. 2026-09-25 Europe switched to Bailian, other regions still had 213 blocks (`pack-v4`) after changing the painting style, and the same 213 blocks (`pack-v5`) after switching to image_gen. `srw64-worldmap-hd.json` Added `resources` field, the host accepts 5602–5606, the old single-region format of the first episode is still available.

### Individual windows

- Repaint: earth-04, central-asia-05, coast-05, coast-06, coast-08. The land distribution in the first picture is wrong. It passed after automatically changing the seeds; earth-01 took the third picture.
- The Tibetan Plateau (central-asia-03) is almost entirely land:
- The first three pictures either have more islands or paint the plateau into green grassland;
- The fourth picture added "almost all land, tan is mountains, don't draw grassland" in the prompt. The position is correct, but the painting style is lighter than that of the adjacent window.
- When redrawing, the tool's single-batch cost limit (18.12 yuan per output directory) was encountered, so the fourth picture was retained first.

## UNIVERSE

[`worldmap_space.py`](../../tools/hd_ai/worldmap_space.py)：

- The earth (4×4 blocks) and the moon (2×2) are assembled into a bulletin board picture according to the vertices; the 32×32 textures of 4 meteorites and two small facilities are put into a grid.
- Starry Sky 5582 (CI4 320×240, Palette 5583) is processed as the entire background.
- Request `qwen-image-3.0-pro` once each, 4 times in total. After registration, Alpha takes the original image mask and smoothes it, and slices according to the tile; the RT64 key of the CI4 tile is calculated by `ci4_hash` (64×64 is the same as `map_hash`, 32×32 line width is reduced by half), a total of 27 blocks. They are a new category in the inventory `space` and do not participate in the 64→512 check of the world map.
- The 7 name tags (サイド1/2/3/5/6/7, スウィートウォーター) are text and will not be replaced by RT64. They are the same 200×30 green-framed signs as the nameplates of ships and landmarks (items 6–12 type 5 display list of 5599). They are redrawn by the nameplates of the world map cutscene model HD according to the reading language: the native model package types them into only nameplates, no grid entries, Chinese and English are Side 1...Side 7 (the way the lines are translated) and Oasis/Sweetwater.

### Starry Sky

The starry sky is drawn in sprite slot 0, and goes the same way as the interfield background `80095974`. It is drawn entirely by [`native_background.cpp`](../../src/host/native_background.cpp), and the file is placed in `backgrounds/whole-v2` (16 interfield backgrounds plus 1 starry sky). There are two differences compared with the interfield background:

- CI4 images are loaded as 8-bit, half width (`SETTIMG` 160 wide). The column coordinates of `LOADTILE` must be multiplied by "original image width ÷ SETTIMG width" to obtain pixels.
- The starry sky is the first thing drawn in each frame. When the host draws the entire picture at the first block, RT64 has not yet performed the screen clearing of this frame, and will clear it to black at the beginning of the next rendering pass.
- Now keep the first block drawn as is by RT64 to trigger its pass; the entire picture is drawn at the position of the last block, covering the first block.
- The background between scenes is also processed in this way, and the appearance remains unchanged.

## Europe switches to Bailian (2026-09-25)

The first episode of Europe was originally drawn by the image_gen that comes with the encoding tool (`worldmap-runtime/pack-v6`). During synthesis, the narrow coastline and crop boundaries of the original image were retained. About 6% of the visible pixels were enlarged from the original image, and there were a few patches in the upper right corner that were not HD. The HD package needs to be released to the public, and the description states that it is generated by Bailian, so Europe uses Bailian for redrawing, and the painting style is subject to the image_gen version:

- The first time (`worldmap-surfaces/europe-1`) was redrawn from the original image as in other areas: the Arabian Peninsula and Egypt turned into green grasslands when the color was not preserved; the color was correct after `compose --colour-lock` was preserved, but the painting style was gray and flat, and there were seams caused by the boundaries of the original image blocks. After reading this, users thought it was far inferior to the image_gen version and did not adopt it.
- The method adopted (`worldmap-surfaces/europe-2`): 8 times the image_gen version of Europe into the whole picture (`approved_canvas`, the tiles without HD are enlarged by the nearest neighbor of the original picture), cut into the same 9 windows as picture 1, the prompts require that the painting style, color matching, composition and landform distribution remain completely unchanged, and only a small amount of details are added. No drawing style samples are given, and the color is not preserved. `samples.json` notes the input summary and prompt words for each window.
- The synthesis is as usual: registered to the original image, the coast is smoothly cut out according to the original image mask, and the overpainted island in the model is removed.
- Result: 61 blocks are all from Bailian. It can be seen that the pixels that are the same as the original image are 0. There are 5 locations in Russia in the upper right corner that share the same original image texture (`b820c653dd7fc5ec`). One HD image cannot match 5 locations at the same time and will still be displayed as the original image.

## Other areas rely on the image_gen style (2026-09-25)

The user requested that all areas should be closer to the style of the image_gen version of the first episode. Earth, Central Asia, and North America do not have image_gen versions that can be used as basemaps, so `restyle` is used:

- Figure 1: `run-5` The synthesized area window, saturation ×1.3, makes the landform colors more distinct; Figure 2: Sample of the same painting style.
- The prompt word (`RESTYLE_PROMPT`) only allows you to change the painting method: the color and landform type of each place must be the same as in Figure 1. The brown plateau is still the brown rock mountain, the yellow is still the desert, only the green places are painted with grasslands and forests, and no new lakes and seas are added. The original prompt word did not have these constraints, painting the Tibetan Plateau as a green grassland and adding a lake (`restyle-trial-central-asia`).
- Acceptance: Still only use land coincidence (≥ 0.90) to automatically change seeds. I once tried comparing landforms by color classification and automatically redrawing, but the new strokes themselves would change the color classification. As a result, the candidates with "almost no change" were selected, so I changed to recording only these two numbers (`terrain`, `new_water`), and let people look at the picture window by window.
- Several additional additions were made after manual review: `earth-01` took the 3rd candidate; `central-asia-04` took the 3rd one (the 1st one is a messy mosaic); `earth-04` The 2nd one was weak but the other candidates moved the entire landmass and kept it; `central-asia-07` the 1st one One is a bit mixed, but the other two paint Bangladesh-Indochina as a desert, and the first one is retained.
- Results in `restyle-earth`, `restyle-central-asia`, `restyle-coast`, together with `europe-2` in Europe scored `pack-v4`. All visible pixels on the surface that are the same as the original image are 0.

## Use image_gen instead (2026-09-25)

After seeing Qianwen's two methods (`europe-2`, `restyle-*`), users thought they were far inferior to image_gen, so the four surfaces were drawn by users using image_gen in Codex:

- Generating package `assets/hd-ai/imagegen-kit`: 1 whole area in each area (nearest neighbor enlargement of the original image 1) plus 3:2 local window (384×256 source pixels, 4 times, 1536×1024; almost the whole sea window is not drawn), a total of 24 pictures. Figure 2 is always a part of Europe drawn by 9-09 image_gen (`worldmap-runtime/ai-detail-v1/map-ai.png`). The prompt words are rewritten from the two paragraphs in 9-09, and each landform type is required to remain unchanged; `manifest.json` records the window position, and the generation of Codex is recorded in `outputs/generation-records.json` (the tool only reports `image_gen.imagegen (built-in)`, not the specific model).
- Synthesize `worldmap_surfaces.py imagegen --kit … --output worldmap-surfaces/imagegen-1`:
- The whole area map is registered to the 8x grid base; the windows are registered one by one.
- The windows overlap by as much as two-thirds, and the two paintings will be blurry on average, so blend according to "The window farthest from the inner edge is dominant" (`kit_weight`), and only make a soft transition near the dividing line.
- The window retains its own details, and the color above 48 HD pixels is rounded to the whole area, and the color of adjacent windows is consistent; the color is only taken from the pixels drawn as land, and the coastal deviation does not take into account the sea color.
- There is a shallow seaside in the outer circle of the land mask in the original image, and the inside of the painting is the sea: when there are no pixels painted as land nearby, the image is left as it is and is not painted in a land color.
- The coast is still cut out according to the original image mask.
- The result is scored as `pack-v5`: among the four visible pixels on the surface, the same as the original image when enlarged is 0. The 5 blocks of Russian shared textures in the upper right corner are still the original ones.

## Seams, Coastal Purple Edge, Sharpening and Close-up (2026-09-27)

Looking at the first episode and various locations in the south of 5604 on a real machine (the perspective lens enlarges 1 pixel of the original image to 19–30 pixels in the 1440p window), there is a horizontal seam at the junction of each row of tiles, and there is a purple edge on the coasts of Libya and Tunisia, which is overall soft. The first two places are in the tool:

- **Seam**: `assemble` Places all quads as `UNIT` (611/64), but the grid has only 600 world units (62.85 pixels) of row spacing and 611 column spacing. Therefore, each row in the puzzle is 62–63 pixels lower than the previous row instead of 64, and the next row covers the last one or two rows of pixels of the previous row; `pack` and then cut by 64 pixels, the beginning of the next block is cut into the end of the previous block. In the game, the 1 pixel (HD 8 pixels) is displayed twice, becoming a horizontal line. There are no longitudinal seams because the row spacing is exactly 64. Now `pack` uses `tile_span` to get the actual range of each piece in the puzzle (until the next piece in the same column, rows 62–64), and then pull it back to 512×512 (`cut_tile`). The puzzle itself has not been changed, the image_gen generation package and the synthesized image are both registered according to it. Offline checking of 52 pairs of upper and lower adjacent blocks of 5604: the average difference of adjacent rows at the junction dropped from 14.4 to 3.4, the same as the adjacent rows within a block.
- **Purple Edge**: The outer circle of the land mask in the original image is a circle of shallow sea, and the inside of the painting is the sea. When compositing, "keep the picture as it is", while image_gen painted the circle of shallow sea purple, and mixed the purple into a strip of sand close to the coast. `imagegen` Add `coast_tidy` at the end of the composition: the pixels in the mask that are painted as water (blue is greater than red and green) only change the hue to the hue of the clear sea color; the inner side of the coast `COAST_BAND` (10 HD Pixel) wide strip of land, the color is taken from the more inland land (`land_blur`), retaining its own brightness, and the texture of the painting remains unchanged; the island has no inland to choose from (`land_blur`, the weight going to zero will calculate the gray, yellow and red variegated colors, which have appeared at both ends of Malta), and only change colors in sufficient places inland.
- **Sharpening**: The drawing is 4x, zoomed to 8x and then magnified by the lens, it looks soft. The synthesized land map is overall USM (`SHARPEN`, radius 3, 60%), before `coast_tidy`.

Resynthesized to `imagegen-2`, retyped on `pack-v5` to `pack-v6`:

```sh
.venv/bin/python -m tools.hd_ai.worldmap_surfaces imagegen --kit assets/hd-ai/imagegen-kit \
  --output assets/hd-ai/worldmap-surfaces/imagegen-2
.venv/bin/python -m tools.hd_ai.worldmap_surfaces pack --output assets/hd-ai/worldmap-surfaces/imagegen-2 \
  --base-pack assets/hd-ai/worldmap-surfaces/pack-v5 --pack-output assets/hd-ai/worldmap-surfaces/pack-v6 --bind
```

### Close view window

The lens is equally close to each surface: when positioned the center of the screen is about 3.2 screen pixels (320 base) to 1 native pixel, which is about 100×75 native pixels per screen. The local window of image_gen is 384×256 and the original pixels are drawn to 1536×1024 (4 times). When zoomed to 8 times and then enlarged 2.5-7 times, the close-up view becomes blurry. Improvements can only be made by creating smaller windows by location:

- `closeup-kit`: Calculate the number of uses of each location from the ROM location table `801C5310` and the extracted scene events (3D32/3D33 words in `assets/original-data/records/stage_events.jsonl`, 827 times in total, 458 times on the earth's surface), greedy coverage by number: each window 120×80 The original pixel (`CLOSEUP`) is centered on the most commonly used uncovered location and absorbs locations near the center. `--always` specifies the location that is given priority to the window (the default is 4, 0, 1, 2 in the first episode), and `--count` limits the number of images. Two pictures are given for each picture: `*-input.png` is an 8-fold cut (960×640) of this window on the current composite picture (`--base` running directory), `*-source.png` is a hard pixel enlargement of the original picture 12 times (1440×960); the prompt words allow the model to maintain the composition, color and painting style, and only increase the density of details. The coastline is as shown in Figure 2. `manifest.json` records the window position (`box`, puzzle coordinates), covered locations and times; `index.jpg` is the thumbnail.
- `closeup`: Register the drawn `outputs/*-out.png` back to their respective original image windows, place it on the composite image at 8 times, feather the edge 12 original pixels for handover, and use the base image for the coast alpha, do `coast_tidy` again, and write a new running directory for `pack`.

```sh
.venv/bin/python -m tools.hd_ai.worldmap_surfaces closeup-kit --base assets/hd-ai/worldmap-surfaces/imagegen-2 \
  --output assets/hd-ai/imagegen-closeup-kit --count 13 --always 4,0,1,2
.venv/bin/python -m tools.hd_ai.worldmap_surfaces closeup --kit assets/hd-ai/imagegen-closeup-kit \
  --base assets/hd-ai/worldmap-surfaces/imagegen-2 --output assets/hd-ai/worldmap-surfaces/imagegen-3
.venv/bin/python -m tools.hd_ai.worldmap_surfaces pack --output assets/hd-ai/worldmap-surfaces/imagegen-3 \
  --base-pack assets/hd-ai/worldmap-surfaces/pack-v6 --pack-output assets/hd-ai/worldmap-surfaces/pack-v7 --bind
```

2026-09-27 The user finished drawing 13 pictures in Codex, `closeup` was synthesized into `imagegen-3`, typed into `pack-v7` and bound. The registration scaling is between 0.93–1.02 (image_gen will shrink the frame by a few percentage points), and the `place` padding will draw stripes on the edges that are not drawn, so the feathering is calculated from the range that the drawing actually covers (`covered` in the report). Watch the Alps (Location 0) and Italy (Location 2) in the first episode on the real machine: the peaks and trees are clearly defined, and they naturally connect with the surrounding places where there is no close-up view; Atlas (Location 15, no close-up window) only relies on sharpening, and there are no seams.

The opening shot (location 4) is still virtual: 5603 draws the same tiles as 5602, but the map is rotated horizontally by 4 tiles (the puzzle cannot be seen according to the vertex position, and the 7-frame original picture is shrunk by 15–20 times to perform NCC calibration with the original surface map, y is completely correct, and x difference is 256). `locations()` adds 256 to the x of subscript 17 and takes modulo 576 (`SURFACE_WRAP`); `closeup-kit --extend` retains the drawn window, only adds new locations that have not been covered, and adds closeup-14 to 19, of which 14 is the opening shot. Six pictures were painted on the same day, and 19 pictures were synthesized into `imagegen-3`, typed into `pack-v8` and bound; the opening shot of the real machine, Greenland, and South America were all close-ups.

The close-up view is still an 8x map (the host `graphics.cpp` only accepts replacement blocks of 512). Going to 16x would have to allow auditing to accept 1024 blocks and let `pack` cut 1024 separately for close-up blocks, TBD.

## Spend

- Earth's surface: 34 times, 17.68 yuan. Among them, 3 test windows were used 5 times, the remaining 20 windows were used 27 times (including 7 automatic redraws), 5604 was added once, and the fourth picture of the Tibetan Plateau was used once.
- The first few rounds of painting style experiment (realistic style and single map reference): 6.76 yuan, invalid.
- Universe: 4 times, 2.08 yuan.
- Europe (2026-09-25): `europe-1` 9 times 4.68 yuan (not adopted); `europe-2` 10 times 5.20 yuan (one window is redrawn once).
- Changing the painting style in other areas: 2 trials for 1.04 yuan; `restyle-*` for a total of 46 times for 23.92 yuan, about half of which was spent on automatic redrawing of color classifications that was later removed.

## Actual machine (2026-09-24, HD mode)

- `worldmap-regions` The mini-levels go to locations 3 (Central Asia 5605), 18 (North America 5606), 5 (Whole Earth 5602), 9 (Whole Earth 5603), 0 (Mediterranean Sea 5604).
- At first, I read the location list by 12 bytes, and the selected ones were 5605, 5603, and three times 5604. North America and 5602 were not included. After correction, I reran and found that Central Asia, North America, India and Qinghai-Tibet on 5602, and the Middle East on 5603 were all HD.
- `worldmap-space` Travel to all 32 locations in the universe.
- The surface of each area, the starry sky of the universe, the earth, and meteorites have been changed to HD, and the setting will be restored after switching back to the original image.
- All 1506 drawings of the starry sky have been rewritten, with 0 recognition failures.
- Nameplate: With native model package, Chinese operation, each of the 7 nameplates has been drawn 7300 times; the screen is Oasis, Side 1/2/3/7, which is consistent with the ship nameplate (Libra).

## Command

The current package `pack-v5` was retyped on `pack-v4` on 2026-09-25: all four surfaces were taken from image_gen to synthesize `imagegen-1`.

```sh
.venv/bin/python -m tools.hd_ai.worldmap_surfaces imagegen --kit assets/hd-ai/imagegen-kit \
  --output assets/hd-ai/worldmap-surfaces/imagegen-1
.venv/bin/python -m tools.hd_ai.worldmap_surfaces pack --output assets/hd-ai/worldmap-surfaces/imagegen-1 \
  --base-pack assets/hd-ai/worldmap-surfaces/pack-v4 --pack-output assets/hd-ai/worldmap-surfaces/pack-v5 --bind
```

How to do `pack-v4` (Qianwen version):

`pack-v4` was retyped on `pack-v3` (including the universe, dialog box border and combat HUD border) on 2026-09-25: `restyle-*` is used for Earth, Central Asia, and North America, and `europe-2` is used for Europe. The 57 blocks drawn by image_gen in the first episode are no longer included in the package.

```sh
for s in earth central-asia coast; do
  .venv/bin/python -m tools.hd_ai.worldmap_surfaces restyle --output assets/hd-ai/worldmap-surfaces/restyle-$s \
    --from assets/hd-ai/worldmap-surfaces/run-5 --surface $s
  .venv/bin/python -m tools.hd_ai.worldmap_surfaces run --output assets/hd-ai/worldmap-surfaces/restyle-$s --env-file .env
  .venv/bin/python -m tools.hd_ai.worldmap_surfaces compose --output assets/hd-ai/worldmap-surfaces/restyle-$s
done
.venv/bin/python -m tools.hd_ai.worldmap_surfaces compose --output assets/hd-ai/worldmap-surfaces/europe-2
.venv/bin/python -m tools.hd_ai.worldmap_surfaces pack --output assets/hd-ai/worldmap-surfaces/restyle-earth \
  --extra-run assets/hd-ai/worldmap-surfaces/restyle-central-asia --extra-run assets/hd-ai/worldmap-surfaces/restyle-coast \
  --extra-run assets/hd-ai/worldmap-surfaces/europe-2 \
  --base-pack assets/hd-ai/worldmap-surfaces/pack-v3 --pack-output assets/hd-ai/worldmap-surfaces/pack-v4 --bind
```

`pack-v1` The original approach:

```sh
.venv/bin/python -m tools.hd_ai.worldmap_surfaces prepare --output assets/hd-ai/worldmap-surfaces/run-5
.venv/bin/python -m tools.hd_ai.worldmap_surfaces run --output assets/hd-ai/worldmap-surfaces/run-5 --env-file /path/to/.env
.venv/bin/python -m tools.hd_ai.worldmap_surfaces compose --output assets/hd-ai/worldmap-surfaces/run-5
.venv/bin/python -m tools.hd_ai.worldmap_surfaces pack --output assets/hd-ai/worldmap-surfaces/run-5 \
  --base-pack assets/hd-ai/portrait-matte/v2/pack --pack-output assets/hd-ai/worldmap-surfaces/pack-v1 --bind
.venv/bin/python -m tools.hd_ai.worldmap_space pack --output assets/hd-ai/worldmap-space/run-1 \
  --pack assets/hd-ai/worldmap-surfaces/pack-v1 \
  --backgrounds-from assets/hd-ai/backgrounds/whole-v1 --backgrounds-to assets/hd-ai/backgrounds/whole-v2 --bind
```

`SRW64_BG_DUMP=1` will write the display list of the first drawing of the sprite background without HD to the running directory `background-draws.jsonl`, which will be used to check the drawing method when receiving new pictures.