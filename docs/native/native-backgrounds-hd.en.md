> **Language / Ngôn ngữ:** [English](native-backgrounds-hd.en.md) · [Tiếng Việt](native-backgrounds-hd.vi.md) · [中文](native-backgrounds-hd.md)

# BACKGROUND HD

2026-09-24. The 8 background images of the インターミッション screen have been generated in HD, and are integrated into the game as a whole image, with one set each of light version and dark version.

## What is the background?

- A total of 8 320×240 CI8 3D CG illustrations, resources 5470–5477 (`0x155E`–`0x1565`). Each picture shows a protagonist machine with the SRW64 logo in the upper right corner.
- Two 256-color palettes per sheet: light version 5478–5485, dark version 5486–5493. Use the light version when entering for the first time; change to the dark version after the menu is constructed and when returning from the sub-screen. The graph itself remains unchanged.
- Select the picture according to the first protagonist machine, and it will not change with the number of words. For details, see [Inter-Scene Main Menu](native-intermission-menu.md) §3.
- Color 0 is transparent black. The background of the game is set to black, so HD images are made opaque.

## How to draw the game

The background is drawn in sprite slot 0, mode 4, `80098158(槽, 0, 4, 0xA4, 0, 图, 调色板, 0)`, and the drawing function is `80095974` (mode 2 also uses it). Display list captured on real machine:

- First set `E3000C00`, `E3001001` (TLUT RGBA16), combiner `FC119623 FF2FFFFF`, that is, color and Alpha are both TEXEL0 × PRIM; then use `FA` to set PRIM (fading in and out depends on it).
- Then load the 256 color palette.
- Then draw 80 blocks of 32×32: `SETTIMG` for each block (the entire image), `LOADTILE` to load the area of this block (loading 1 pixel more for bilinear filtering), `SETTILESIZE` to set the rendering tile to (0,0)–(31,31), and finally `TEXRECT` to draw to the screen.
- Elf subrecord +0xC/+0xE is the resource handle. The resource number can be exchanged by pressing the handle table of `8008A11C` (`0x160340`, each item is 20 bytes, +2 is the ROM resource number).

## Replace the entire sheet

The method of [`native_background.cpp`](../../src/host/native_background.cpp) is the same as the avatar:

1. Hang `80095974`;
2. Use the resource number to check the HD image corresponding to (image, palette);
3. Calculate the range of each block on the original image from the starting point of `LOADTILE`, the S/T of `TEXRECT` and dsdx/dtdy, and write down (screen rectangle, original image rectangle);
4. Change the last block to a labeled mark, keep the first block as it is (let RT64 start the rendering pass of this frame first, see the starry sky section of [Story World Map HD](native-worldmap-regions-hd.md)), and leave the rest blank;
5. The host uses instanced drawing to draw all the blocks at once (plume, `src/host/shaders/HdBackground*.hlsl`, the same copy of Metal/Vulkan/D3D12), sampling the same HD image, so there are no seams between blocks.

Shaders are multiplied by PRIM and fade as original; textures are premultiplied alpha with mipmaps. It will not be rewritten in the original image mode. When scrolling or drawing only a part, each block is also mapped according to its own original image range.

## Generate

[`background_hd.py`](../../tools/hd_ai/background_hd.py):

- `prepare`: Bright version enlarged by nearest neighbor 6 times as input. The prompt words are required to retain the composition, body and logo text (large characters "SRW64", small characters "super robot wars 64").
- `run`: Request `qwen-image-3.0-pro` and `qwen-image-3.0` once for each image, output 2048×1536, a total of 16 times, 5.76 yuan. All worked at once, no 400 occurred.
- `compose`: Register by window, fit scaling and translation axis-by-axis (deviations are within 0.2%), resample to 1920×1440 (6 times), and output a comparison chart.
- `build`: Take the selected model (default Pro) as a highlighted version. The dark version uses a 17³ color table fitted from two sets of ROM palettes, mapped from the light version.
- The dark version is not uniformly darkened: the ratio of each color is between 0.5–0.95.
- Use the original image to verify: the average difference between the color table and the dark version of the game is 1.2-2.6 levels, and when multiplied by 0.75, the difference is 3-23 levels.

Both models retain the composition, parts and logo text. The Pro's shadows and surfaces are cleaner, while the regular version is slightly sharper and has slightly jagged edges. After shrinking to its original size, the difference from the original image is both 2–5 levels. The default is Pro, you can use `build --choice '{"background-5470": "qwen-image-3.0"}'` to change the selection one by one.

Resources in `assets/hd-ai/backgrounds/whole-v1`: 16 images 1920×1440, total 42 MB. The manifest now uses `whole-v2`, which is whole-v1 plus the starry sky of the story world map ([story world map HD](native-worldmap-regions-hd.md)). The `backgrounds` section of [`stage1-hd.json`](../../content/art/stage1-hd.json) lists them, and `compile_art` is copied to the running directory `art/backgrounds/` after verification.

## Actual machine (2026-09-24, HD mode)

- After reading the first episode and clearing the save file and entering インターミッション: the background (スイームルグ, 5476) is displayed as an HD dark version, and the menu panel is stacked on top as usual.
- Set to switch to the original image and then switch back, the two HD screenshots will be consistent pixel by pixel.
- Exit count: 986 background drawings all rewritten, 0 recognition failures, 2 decodings (light, dark).

## Command

```sh
.venv/bin/python -m tools.hd_ai.background_hd prepare --output assets/hd-ai/backgrounds/run-1
.venv/bin/python -m tools.hd_ai.background_hd run --output assets/hd-ai/backgrounds/run-1 --env-file /path/to/.env
.venv/bin/python -m tools.hd_ai.background_hd compose --output assets/hd-ai/backgrounds/run-1
.venv/bin/python -m tools.hd_ai.background_hd build --output assets/hd-ai/backgrounds/run-1 --images assets/hd-ai/backgrounds/whole-v1 --bind
```

After changing the hook of `generate_cpu.py`, you need to rerun it first and then build the host.