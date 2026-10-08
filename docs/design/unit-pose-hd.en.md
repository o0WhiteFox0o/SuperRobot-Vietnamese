> **Language / Ngôn ngữ:** [English](unit-pose-hd.en.md) · [Tiếng Việt](unit-pose-hd.vi.md) · [中文](unit-pose-hd.md)

# 3D rendering HD: scale and first trial production

2026-09-26. The large pictures of the aircraft drawn on the original pages such as pre-war confirmation, transformation, ability, and のりかえ are from `battle_assets.units` (the basic posture of the aircraft, deduplicated according to the Scene/Album/Palette triplet). The page can be enlarged up to 6 times, and the pixel blocks are obvious. This article records the scale estimate of redrawing using `qwen-image-3.0-pro` and the trial production results of 3 airframes. Tool: [`unit_pose_hd.py`](../../tools/hd_ai/unit_pose_hd.py), output in `assets/hd-ai/unit-poses/` (do not enter git).

## Scale

```sh
.venv/bin/python -m tools.hd_ai.unit_pose_hd scale
```

| item | number |
| --- | ---: |
| Body | 363 |
| Basic posture after weight loss | 332 |
| 96×96 | 249 |
| 128×128 | 57 |
| 128×96 | 16 |
| The rest (32×32 ×3, 128×64 ×3, 96×97, 160×128, 144×144, 130×228) | 10 |

The fee is based on one request, one candidate, and the original price:

| Method | Number of requests | Cost (yuan) |
| --- | ---: | ---: |
| Leaflets, `qwen-image-3.0-pro` | 332 | About 173 |
| Leaflets, `qwen-image-3.0` | 332 | About 66 |
| 2×2 Puzzle, Pro (not verified on body) | 83 | Approx. 43 |
| 3×3 Puzzle, Pro (not verified) | 37 | About 19 |

Requests denied by IP filters are not billed (see below). `aliyun.py` Each output directory has a reserved upper limit of 18.12 yuan, which must be released before running in full.

## Try it

Three units: 3 Seiko (96), 177 Shin・ゲッター1 (128), 156 Dark General (128). Each image: gray background (100,100,112), pre-magnification 6 times, output 2048², registration and cutout using `portrait_matte`, master 8 times (96 → 768).

| Table of contents | Pre-amplification | Prompt words | Results |
| --- | --- | --- | --- |
| test-1 | Nearest Neighbor | `faithful` (specify "Pixel Drawing Vertical Drawing") | Both passed; Pro copied it as a pixel drawing, but straightened out the lines and retained all jagged edges. Registration IoU 0.995 / 0.987 |
| test-2 | Nearest neighbor | `smooth` (requires anti-aliasing, drawn as a cel illustration) | シャイニング half-pixel half-line draft, horizontally reduced by 3.5%, registration exceeds the threshold; ゲッター rejected |
| **test-3** | **Double Cubic** | **`smooth`** | **シャイニング is a clean celluloid line drawing with a faithful structure, registration x1.000/y0.998, IoU 0.986, and an average edge filtering error of 0.86. Set as baseline. ** ゲッター rejected |
| test-4 | Double three times | `smooth-plain` (remove SD/two-headed body words) | ゲッター Still rejected |
| test-5 | Double triple | `faithful` | ゲッター was rejected (after 45 seconds of reasoning, output side); Dark General was rejected in 5.7 seconds (input side) |

**Conclusion**

- Bicubic preamplification + `smooth` hint words is available; nearest neighbor input will guide the model to preserve pixel wind.
- **IP filtering is the main risk**: True・ゲッター1 Only the pixel style version passed, and the smooth line drawing was blocked by the output side filter; Dark General did not even accept the input. Only 1 of the 3 machines was successful according to the baseline method, and there is no data on the full pass rate. It is estimated that 10-20 machines will be selected and run through (rejected ones will not be charged, only the successful ones will be paid).
- When there is no alternative for the rejected body, you can return `faithful`+nearest neighbor (the result of test-1 that "organizes the lines without de-aliasing"), or amplify by the local algorithm.

## Access

Already done, see "Finalization and Access" below. The HD image is named according to the key of `battle_assets` (`unit-<scene>-<atlas>-<palette>.png`). In the page, `unit_art` is cropped by alpha to `rect`. The transparent area of ​​the master is filled with the nearest solid color without dark edges.

## Local ESRGAN comparison (2026-09-26)

[`esrgan_pose.py`](../../tools/hd_ai/esrgan_pose.py) Use spandrel to run the community 4x ESRGAN model: the color map first fills the transparent pixels into the nearest solid color, and the alpha is passed through the model separately as the grayscale image, and then Lanczos shrinks it to 8x the master. Environment `build/esrgan-venv` (python3.14 + torch + spandrel), model `build/esrgan-models/` (4x-PixelPerfectV4 WTFPL; 4x-AnimeSharp CC-BY-NC-SA 4.0, Kim2091), neither git nor public package. Output `assets/hd-ai/unit-poses/esrgan-1/`, compare each line of the page: original image, AnimeSharp ×1/×2 passes, PixelPerfectV4 ×1/×2 passes, Pro (if available).

| items | results |
| --- | --- |
| Speed | 0.6 seconds for 96² one trip, 1.3 seconds for two trips on MPS; about twice that on 128². 332 photos completed in a few minutes, zero fee, no IP filtering |
| Fidelity | Pixel-by-pixel correspondence, no structural drift, smooth alpha edges |
| AnimeSharp | Hard edges, dark lines, closest to celluloid line drawing; two passes are cleaner than one. Suitable for hard-edged pixel art such as シャイニング and ゲッター |
| PixelPerfectV4 | Softer, more painterly, with smooth transition of color levels; suitable for pictures like the Dark General with inherent light and dark gradients |
| Comparison with Pro | Pro's lines are more like those drawn by human hands, and the block surface is neater, but there are minor changes in details (chest, fingers); ESRGAN's lines are slightly "shaky", but all details are retained |

Conclusion: ESRGAN can be used as the base for all applications, and the two machines rejected by IP filtering have also been processed; Pro is only used as a bonus for the main machine.

## Finalization and access (2026-09-26)

After comparing 14 local models ([`esrgan_pose.py`](../../tools/hd_ai/esrgan_pose.py), output `assets/hd-ai/unit-poses/esrgan-2`) on three machines, the final decision was made: a half-mix of 4x-UltraSharpV2 and 4x-PixelPerfectV4**. UltraSharpV2 (DAT) has the most details and the cleanest lines, but users feel it is slightly sharper; among the six sharpening methods (one pass plus Lanczos, 1.5 / 2.5 px Gaussian, half and half mixture with BS-Deviance / PixelPerfectV4, `esrgan-5`), PixelPerfectV4 mixture was selected. Eliminated: AnimeSharpV4_RCAN, HFA2k_realplksr (gray ghosting), Drawimation (fuzzy), NumericFrames (too dark), Faithful-Lite (retaining pixelation), two 2x AnimeSharp (three passes superimposed, soft or grainy). Starting from 2026-09-27 `build/esrgan-models/` Only 4x-UltraSharpV2 and 4x-PixelPerfectV4 are left for finalization (only the latter is used in the icon pipeline). The other comparison models have been deleted and should be re-downloaded from OpenModelDB when the comparison is to be redone.

Pipeline:

```sh
.venv/bin/python -m tools.hd_ai.unit_pose_hd prepare --output assets/hd-ai/unit-poses/all-1 --all --prescale bicubic
build/esrgan-venv/bin/python tools/hd_ai/esrgan_pose.py --samples assets/hd-ai/unit-poses/all-1 \
    --models build/esrgan-models --output assets/hd-ai/unit-poses/all-1 --blend 4x-UltraSharpV2 4x-PixelPerfectV4
.venv/bin/python -m tools.hd_ai.build_unit_images --run assets/hd-ai/unit-poses/all-1 --output assets/hd-ai/unit-poses/whole-v1 --bind
```

- `esrgan_pose.py --blend` Run two models for each pose (two passes each to 16x, Lanczos back to 8x; alpha passes the model alone), write `hd/unit-<scene>-<atlas>-<palette>.png`. 332 shots in about 1 hour on MPS.
- [`build_unit_images.py`](../../tools/hd_ai/build_unit_images.py) generates package directories `whole-v1/` (PNG preserves alpha) and `units.json` (`srw64.unit-images.v1`, indexed by triplet), `--bind` writes the `units` section into `content/art/stage1-hd.json`.
- Access and follow the path of the avatar: `compile_art` is copied into `art/units/` and `srw64-units-hd.json`; `assets.unit_lookup` finds the file by triplet; `profile.py` → `prepare_battle_assets(..., hd_unit)` is added to `battle_assets.units[n]``hd`; release launcher `launch.cpp` reads the same index as `resources` triplet hangs `hd` (the body entry of the C++ importer adds `resources`).
- Page: The pre-war confirmation page `battle_unit` and the transformation page use `portrait_path()` (when in HD mode and with `hd`, take the HD file), the ability/のりかえ/save page originally uses `portrait_path`, no need to change. Confirm that the maximum page enlargement limit is calculated in ROM pixels (6 × ROM width ÷ file width), and HD files are resampled according to the display width.
- Actual machine verification: [`check_unit_pose_hd.py`](../../tools/recomp/debug/check_unit_pose_hd.py), HD screenshot of the confirmation page before entering the battle, F6 to cut the original picture for comparison.
- Copyright: For the license of the model, see the description of [`esrgan_pose.py`](../../tools/hd_ai/esrgan_pose.py); the product is derived from the original screen and is released with the HD package (the public package is the same as for personal use, 2026-09-28 user determined), NOTICE indicates the model used. The release package stores JPEG with 6 times the ROM pixels plus transparent PNG (`compress_hd.py`).

## Can combat animations be handled this way?

Yes, and it is the "atlas master + part slicing" route specified in the inventory, but it is not as simple as throwing the entire atlas into the model. There are three things to do:

1. **Parts are textures loaded in blocks. ** Each part is loaded by `8009761C` using LoadTile from the CI8 atlas (mostly 32×32, maximum 2 KB TMEM), and RT64 calculates a hash for the loaded piece and replaces it. Therefore, HD should be sliced ​​by parts, not by the entire atlas; the same area is loaded with different sizes and calculated as different textures. The RT64 hash algorithm of the CI8 block has not been tested against TMEM dumps like CI4 (`rt64_hash.py` only has two types: font and map), so it needs to be verified first.
2. **Seams. ** Adjacent parts in the atlas may not be adjacent on the screen. Enlarging the entire atlas will mix the colors of adjacent blocks into the edges. A safe approach is to synthesize the entire frame like a pose, then zoom in, and then cut back according to the position of the part in the frame (the exporter can already record and synthesize each frame according to the part); the scaled and rotated part in mode 1 uses the undeformed frame.
3. **Generate separately according to palette. ** ESRGAN only recognizes RGB. There are 296 atlases with 305 sets of color palettes (color difference between enemy and friend). Each set must be produced separately. It is enough to save the slices at 4 times (32×32 → 128×128). 8 times the volume is not necessary.

The scope is limited to the body atlas, weapon parts, shields and cut-in; the special effects use palette animation, and the hash changes with each jump, which is not applicable (the same conclusion has been reached in the tactical map section). This route does not touch the battle logic and timing, and only changes the textures, which is in line with the constraint of "the combat performance does not change the settlement".

**Two errors in the first real machine (already fixed)**: ESRGAN's alpha leaves sporadic weak values on the entire canvas, and the page's `rect` calculated based on alpha becomes the entire document, and the body shrinks and floats in the transparent canvas; `clean_alpha` (also called `build_unit_images.py`, `esrgan_pose.run_pose`) limits the alpha to 12 px outside the original mask. and remove values less than 8. The page boundary only counts pixels with alpha ≥ 16. In addition, the `<img>` of the confirmation page cannot be resampled according to the display width, and `rect` is in file pixels. The edited `check_unit_pose_hd.py` screenshot is the same size and position as the original version.

## The large picture of the body is scaled according to size level (2026-09-26, under evaluation)

Users suggested that the large image of the aircraft should be scaled according to "volume" instead of each unit filling the area. The data source is the size level of the airframe record: ROM airframe table (`0x71B80`, 36 bytes per bar) **+4's lower 5 bits** are 1/2/4/8/0x10 → SS/S/M/L/LL (runtime record `+0x0C`, capability page `801D1680` same algorithm; high bit 0x80 has another meaning). 363 stations according to level and posture pixel statistics:

| Level | Number of units | Pose canvas | Pixel bounding box height (minimum/median/maximum) |
| --- | ---: | --- | --- |
| SS | 5 | 32² × 3 (ドモン, マスターアジア, アルベルト生生), 96² × 2 | 18 / 25 / 87 |
| S | 57 | 96² ×55, 128×96 ×2 | 39 / 84 / 96 |
| M | 205 | 96² ×173, 128² ×20, 128×96 ×10, 130×228 ×1 | 40 / 87 / 122 |
| L | 58 | 96² ×46, 128² ×10, 144² ×1, 128×96 ×1 | 65 / 88 / 126 |
| LL | 38 | 128² ×28, 160×128, 128×64 ×3, 128×96 ×3, 96² ×3 | 53 / 94 / 128 |

Conclusion: **Sprite pixel size does not reflect size class**. Most of the S, M, and L levels are painted on the 96² canvas and the bounding box is around 85-90 px (the S level of the ダンバイン series is also 96 px). Only LL generally uses 128²; within the same level, there are Flat or small pictures such as Gフォートレス (96×40) and バトルクラフト (60×39). Therefore, "unifying the proportion according to ROM pixels" will not work. It must be based on the level of body data.

Draft (implemented in the workspace, not yet submitted): The pre-war confirmation page snapshot has `size` (0–4). The page takes a share of the area by level and then adapts it according to the bounding box, still retaining 6 times the ROM pixel limit. The first version has LL 100%, L 86%, M 72%, S 58%, and SS 46%; after reading it, users requested that the driver panel be recompressed, the body be larger, SS/S be smaller, and LL be more oppressive. The second version: ability effect area 70dp → 44dp, body area height constant 462 → 436, upper limit 320 → 360dp (960×720 The body frame under the logical window is 258 → 300dp), and the shares are LL 100%, L 84%, M 70%, S 52%, and SS 30%. The third version (finalized): LL mentioned 115%, with the top banner and bottom driver panel, just enough not to overwhelm other elements; test level `config/recomp/mini-stages/battle-ui-ll.json` (the enemy is replaced by デビルガンダム), `check_unit_pose_hd.py` can pass the level path. The schematic diagram (three units per level, synthesized offline from whole-v1) and the actual machine screenshots (ゼーロン L vs. Miミニフォー S) have been shown to users. To be determined: share value; 32²'s biological character is limited to 6 times the upper limit of only about 120 px, whether it should be relaxed; 362 シュバルツ and other placeholder records are marked SS but borrowed from シャイニング's picture.