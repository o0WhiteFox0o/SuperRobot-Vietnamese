> **Language / Ngôn ngữ:** [English](unit-icon-hd.en.md) · [Tiếng Việt](unit-icon-hd.vi.md) · [中文](unit-icon-hd.md)

# Aircraft logo (map unit icon) HD: a repaint scheme that retains the pixel feel

2026-09-26. Each aircraft on the tactical map is a 16×16 CI4 SD avatar (resources 688–1009, 320 different pictures, 323 aircraft records). The camp colors come entirely from the palette (1010 blue, 1011 red, 1012 yellow, 1013 gray; numbers 1–6 are camp color scales, numbers 7–13 are fixed colors such as eyes and pink, and number 0 is transparent). User requirements: High-definition should **preserve the pixel feel**, but instead of simply enlarging the original pixels, it is best to look like a newly drawn pixel painting with a higher resolution. This article records the routes tried and the methods adopted. Tool [`unit_icon_hd.py`](../../tools/hd_ai/unit_icon_hd.py), output and research materials are in `assets/hd-ai/unit-icons/` (do not enter git).

## Conclusion (finalized on 2026-09-26)

**MMPX×2 → 4x-PixelPerfectV4 → Hard quantization 32 → MMPX×2, the product is a 64×64 color map. ** The whole process is local, without blurring, anti-aliasing and dithering. Each output pixel only takes the color number used in the original image:

1. MMPX×2 (`pixel_scale.py`, only copy the color number): smooth the steps, shake the checkerboard and shrink it into a 2-pixel square;
2. 4x-PixelPerfectV4 (local ESRGAN, `build/esrgan-models`) takes this 32×32 and produces a 128×128 smooth painting (color and alpha are separated through the model, and transparent pixels are filled with the nearest solid color first);
3. The BOX is reduced to 32×32, each pixel is pasted to the color number used in the original image according to the CIELAB distance, and the isolated pixels are removed twice;
4. Then MMPX×2 to 64×64, and only follow the steps of the 32-pixel result.

The key is to place MMPX in front of the model: if the model directly consumes 16 pixels, the jitter will be rolled into a rounded block ("smear"), and if MMPX×4 is used, it will be locked by the large block and almost unchanged; The last step of MMPX is compared to directly hard quantizing to 64. The shape is more neat and more like hand-pointed pixel paintings. 320 shots in 17 seconds on MPS, zero fees, no IP filtering issues.

```sh
build/esrgan-venv/bin/python tools/hd_ai/unit_icon_hd.py export --output assets/hd-ai/unit-icons/v2
build/esrgan-venv/bin/python tools/hd_ai/unit_icon_hd.py run --output assets/hd-ai/unit-icons/v2   # --pre 2 --size 32 --post 2
```

`v2/hd/<rid>.idx.png` is a 64×64 color number image, `<rid>-<palette>.png` is four sets of renderings; `review.png` is 9 samples (original image, smooth, 64 px, red, gray), and `sheet.png` is a list of all 320 images.

**Resolution**: The `resolution_scale` of the play profile is 4 (the upper limit is 8). The 16-pixel icon occupies 64×64 internal pixels on the screen, so the 64-bit master is drawn at 1:1 at the default magnification; it is displayed at 2:1 at magnification of 8. The source information is limited, and the 128 version only has more transitions on the hypotenuse, which is unnecessary.

**Status (2026-09-27)**: The user confirms to enter the game according to this process first (HD/original version uses F6 or settings to switch, the icon is switched with the art package), and may be adjusted later; the adjustment only changes `--pre`, `--size`, `--post`, `--model` and reruns `run` and `pack --bind`, no need to connect.

## Exploration process

### Round 1: Smooth → Re-pixelate 32 (No)

PixelPerfectV4 directly eats 16 pixels → Gaussian 0.7 → BOX to 32 → paste color number → remove isolated pixels. After viewing it, the user said: **"There is no sense of pixels anymore"**, the color gradient transition is too smooth, and the hard edges and checkerboard flavor of the original work are all gone. Leave it as `--pre 0 --post 0 --blur 0.7` in the tool.

### Round 2: Get back the pixel feel (rejected)

- Bayer 2×2 / 4×4 orderly dithering of the whole image: it becomes noise, unlike hand-pointed ones;
- Flat color block + 1 pixel dark stroke (majority filter): still smooth, and most filters will eat up single-pixel highlights and eyes;
- hybrid (the original pixels including checkerboard are used internally, and only the redraw results are used in the outlines and steps): the strongest pixel feel but almost no new details;
- The user clearly stated: **Please use "very high-definition, re-pointed" pixel art, without any smearing or smoothing**.

### Round 3: Hard quantization (no blur, no jitter)

xBRZ×4 source → Hard 64: The steps are clean and the block surface is flat, but xBRZ is GPLv3 and the shape is vectorized; the user asked instead **MMPX + ESRGAN**.

### Round 4: MMPX in front

| chain | results |
| --- | --- |
| MMPX×2 → PPv4 → Hard 64 (F) | Structure one-to-one correspondence, dithering becomes directional light and dark, user primary selection |
| MMPX×2 → PPv4 → Hard 32 | 2x version of the same chain, larger blocks |
| MMPX×4 → PPv4 → Hard 64 (G) | Locked by the 4-pixel square, it is almost the original image; change to UltraSharpV2 / Nomos8kSC / 2x AnimeSharpV3, two-pass model, MMPX×8, there is no difference; add more filters to eat up the highlights. User: "The quality has gone backwards this time" |
| Half and half F and G source images (H) | Compromise, not selected |
| Variation of F: Do not remove isolated pixels, two passes, sharpen before quantization, Scale2x / xBRZ×2 as front, UltraSharpV2 combination | Do not remove isolated pixels and keep a few more single-pixel highlights; the rest have no substantial improvement or rounder |

### Round 5: Permutation and combination of MMPX×2 and PPv4

| Combination | Result |
| --- | --- |
| PPv4 → Hard 64 (without MMPX) | Shake and knead into large pieces, the most "smeared", ドモン's face is deformed |
| MMPX×2 → PPv4 → Hard 64(F) | Balance Point |
| PPv4 → Hard 32 → MMPX×2 | Mechanical amplification of 32-pixel results, with the roundness of PPv4 |
| **MMPX×2 → PPv4 → Hard 32 → MMPX×2** | The 32 version of F then uses MMPX along the steps; **User finalization** |
| PPv4 two passes → Hard 64 | Rounder, like an illustration |
| MMPX×4 alone | Guaranteed, almost equal to the original image |

MMPX only makes sense when placed in front of the model; placing it behind is just a mechanical enlargement, but it is used on the hard quantization result of 32 pixels, which is neater than direct hard quantization of 64.

## Comparison of all routes in the first round

9 samples: ガンダム 737, マジンガーZ 944, ゲッター1 853, ダンバイン 929, ザクⅡ 779, アーガマ733. Kono・バトラーV 878. Dark General 838. ドモン 692 (Born). The comparison chart is in `assets/hd-ai/unit-icons/research-2026-09-26/`.

| Directions | Results | Conclusion |
| --- | --- | --- |
| Nearest Neighbor ×4 | As is | Guaranteed |
| Scale4x (EPX twice, color number chart) | The diagonal lines become smoother, but many small sharp corners and "burrs" are produced, and the jittered areas are enlarged into patterns | No use |
| MMPX ×4 (color number chart) | Too conservative, almost the nearest neighbor | No use |
| xBRZ ×4 / ×6 (GPLv3, Zenju) | The smoothest, close to vector graphics; the jittered area becomes the entire color level | Used alone, there is no pixelation; as a "re-pixelated" source image, the effect is similar to the next row |
| **4x-PixelPerfectV4 directly eats 16 px** | Clean smooth painting, natural light and dark transition, faithful structure | **Re-pixelated source image** |
| 4x-PixelPerfectV4 Eat nearest neighbor ×4 | Just sharpen the edges of the pixel block, still 16 frames | No need |
| 4x-deviantPixelHD, 4x-Fatality | Too sharp, cracked, and misplaced highlights | Not used |
| 4x-UltraSharpV2, 4x-AnimeSharp, 4x-Nomos8kSC | Similar or harder than PixelPerfectV4 | Alternative |
| 4x-NXbrz, 4x-Fatal-Pixels (OpenModelDB) | Download source in KB per second, not available | Not tried |
| Re-pixelation 32 (source image PixelPerfectV4 + blur 0.7) | 2x pixel art like a new painting; four sets of color palettes are directly available | The first round of finalization, later rejected by the user (no pixel feeling) |
| Re-pixelate 32 (source image PixelPerfectV4 and half xBRZ ×6) | Almost the same as the previous row, with slightly less edge noise | It’s not worth introducing GPL code, use Gaussian blur instead to achieve the same effect |
| Re-pixelation 48 / 64 | Gradually approaching the smoothness of xBRZ | Not used |
| qwen-image-3.0, nearest neighbor ×32 input | Copy 16 cells, only correct the wrong color (eyes appear red, green and pink) | No |
| qwen-image-3.0, bicubic ×32 input | Still reconstructed to 16 cells | No |
| qwen-image-3.0, PixelPerfectV4 smooth image input | Draw a 48–64 px pixel image, but the shape is off (ガンダム’s V-shaped antenna becomes two corners, and the face is blurred) | No |
| qwen-image-3.0, add the same three-dimensional drawing of the body as a reference picture | The full-body image is drawn according to the reference picture, and it is no longer a head portrait composition | No |

Qianwen’s 8 requests totaled about 1.6 yuan, recorded in `assets/hd-ai/unit-icons/test-1`, `test-2`. 16×16 only has 256 pixels of information, and the editing model must either copy the grid or reinvent the shape; the local "super resolution + quantization" is the most faithful. **The user then decided that no cloud model should be used for such resources. ** This machine (M4 Max, 128 GB) runs SDXL/Flux + pixel art LoRA. Making pictures is the only local route that can add "new details", but it requires the environment to be installed and reviewed one by one, so it has not been started.

## Access (done on 2026-09-26)

Take RT64 texture hash replacement, the same way as world maps and universe objects:

- **Key**: The icon is drawn from subslot 0 (mode 5) built in `801C60A4`, which is a separately loaded 16×16 CI4 map, palette parameter `1010 + 阵营`. The TMEM hash of RT64 v5 also counts the palette items used, so the four camps of the same icon are four different keys, which correspond to four sets of renderings. The hash algorithm follows `worldmap_space.ci4_hash` (TMEM Rich number line 4 bytes swapped, used color number 8 bytes each, plus width 16/height 16/tlut 0x8000/line 1/siz 0/fmt 2), **checked with real dump**: `--dump-textures` In run (`Session.launch(dump_textures=True)`, write `<run>/textures/<hash>.{tmem,tile.json,rice.json}` for RT64), the 16×16 textures (tile line 1, fmt 2, siz 0, masks 4) of the three machines on the map correspond to the calculated keys one-to-one.
- **Package**: `unit_icon_hd.py pack --output v2 --pack assets/hd-ai/worldmap-surfaces/pack-v5 --bind` Write 320 × 4 pictures of 64×64 as `icon-<hash>.png` (the RGB of transparent pixels is filled with the nearest solid color, and linear sampling does not produce dark edges; 1256 pictures of icons with the same pixels are deduplicated) and merged into `rt64.json`, registered as `content/art/stage1-hd.json``kind: icon`; `compile_art` accept this class and retain `kind` in the compiled `rt64.json` (RT64 ignores redundant fields).
- **Real Machine**: `check_unit_icon_hd.py` Move-jump the mini-level screenshot in HD, cut the original version with F6 and take another screenshot, and assert that the 16×16 body texture hash in the dump is in the package. Drawn at 1:1 with 64 pixels at the default magnification of 4, the camp colors are correct and there are no dark edges at the edges.
- **Public package**: The public HD package starting from 2026-09-28 is the same as for personal use, and the icon is also in it; NOTICE indicates that it is enlarged and redrawn from the original pixel image. Previously `build_release.py` was culled by `kind` (`ROM_DERIVED_TEXTURE_KINDS`), canceled.
- Not yet done: The shadow ellipse (resource 687) has not been changed; the meaning of the camp corresponding to 1013 (gray) and whether the color palette of "Actioned" has been changed has not yet been confirmed - the gray version is already in the package and will take effect naturally when used.
- Copyright: PixelPerfectV4 is WTFPL; the product is derived from the original image and is stated in NOTICE when released with the HD package (see [HD Planning](hd-pipeline-plan.md)).