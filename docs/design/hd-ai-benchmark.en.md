> **Language / Ngôn ngữ:** [English](hd-ai-benchmark.en.md) · [Tiếng Việt](hd-ai-benchmark.vi.md) · [中文](hd-ai-benchmark.md)

# SRW64 The first round of actual testing of Alibaba Cloud image high-definition

2026-09-08. Completed live measurements of 6 source maps, 4 image edit models, 42 outputs, and tied a protected HD map to a real RT64/Metal display list snapshot. The public price estimate total is **¥17.64**, no actual bill has been read.

**The direction after viewing the pictures in this round: Qwen 3.0 Candidate 2 is the current first choice for the avatar; mechanical unit icons are not processed, tactical map tiles such as forests are postponed, the visible improvement of cutscene maps and UI borders is not obvious, and continued generation is postponed. ** The text continues to use outline font; if the window border needs to be high-definition, the benefits of rule drawing can be verified separately. This selection is limited to the current sample and does not represent full game HD pack acceptance or overall model ranking.

Update: A separate [Native Content Configuration](../native/native-content-foundation.md) has been built, using smaller avatar output and the local Lanczos 4x map. The historical scope and results of the first round of model comparison are retained below.

## Manual picture review (2026-09-08)

- **Character Avatar**: The user believes that Candidate 2 of `qwen-image-3.0` has the best effect, and uses this saved picture as the current preferred avatar and subsequent comparison benchmark. It has not been installed or rolled out to other characters within the game.
- **Mechanical unit icon**: No processing is required, and it will be moved out of the scope of subsequent high-definition.
- **Forest and other map tiles**: It is currently difficult to deal with, so it will be postponed.
- **Cut scene map**: The user thinks the contrast is not obvious, withdraws the suggestion to advance the map first, and retains the current round candidates and captured frame playback.
- **UI Border**: The user believes that the effect is not significant, so the continued generation is postponed; the benefits of rule drawing/nine-square grid reconstruction have not yet been verified.

The preferred file is Avatar Qwen 3.0 Candidate 2 (`runs/portrait--qwen-image-3.0--2/output.png`), raw output SHA-256: `45ac1a1c6719c2c117853f7f8b6844f0117809b55f2b9e2d31d7dfb24e13406f`. At that time, `review_decisions.json` was used to record the range and selection.

## Current round file

> 2026-09-24: All output, comparison maps, request records, replay evidence and local browsing pages (`assets/hd-ai/2026-09-08/`) for this round have been deleted in the HD legacy cleanup. See `build/cleanup-2026-09-24.tsv` for the list. The conclusions and figures at that time are retained below, and the file names are only for historical records.

## Model results and costs

| Model | Successful output | Public price estimate | Median request time of this round | Observation of this round |
| --- | ---: | ---: | ---: | --- |
| `qwen-image-3.0` | 12 | ¥2.40 | 41.98 seconds | Avatar candidate 2 was selected as the first choice for this round after the user viewed the picture; the visual benefit of the map is not obvious; the mechanical small picture is easy to reconstruct into a new shape |
| `qwen-image-3.0-pro` | 12 | ¥6.24 | 44.67 seconds | The European map is relatively stable, the first candidate was selected for protected synthesis and playback; the avatar still needs to be revised |
| `wan2.7-image-pro` | 12 | ¥6.00 | 10.36 seconds | This round returns the fastest; maps and avatars are worth keeping as candidates; machinery/forest tends to retain large pixel blocks, and new effective details are limited |
| `qwen-image-2.0-pro-2026-06-22` | 6 | ¥3.00 | 35.08 seconds | The fixed version is easy to track, but the mountains and avatars of the current round map are redrawn greatly; the composition of the small mechanical map has obviously been changed |

The time taken includes local network, inference and download, and is an observation value for these 42 requests, not a service performance commitment. 1 picture input, 1 picture output at a time, POST is not automatically retried; all requests are successful. The cost is accumulated based on [previously verified Beijing public price](hd-ai-exploration.md), and the discount/free quota is not deducted, which does not mean that the bill has been confirmed.

A total of **12 plan outputs are not executed** for ordinary super-score and generative super-score: `GetOssStsToken` successfully returns temporary credentials, but when trying to transfer the first source image to VIAPI temporary OSS, `403 AccessDenied` is returned. This result can only prove that the upload link is not connected this time, and cannot infer that the super score service has been activated or not; neither super score API has submitted inference. No RAM policy changes, Bucket creation, or service purchases. Temporary credentials were not written to disk. Bailian's temporary upload URL is bound to the model and cannot be directly used as a general input address for another set of services. [VIAPI file processing](https://help.aliyun.com/zh/viapi/getting-started/the-file-url-processing), [Bailian temporary URL restrictions](https://help.aliyun.com/zh/model-studio/get-temporary-file-url)

## Input source and applicable boundary

| Sample | Source | Size/Handling | Validation Scope |
| --- | --- | --- | --- |
| Map of Europe | Resource 5604's model display list, CI4 tiles and independent RGBA16 palette | 70 rectangular faces; restore the atlas by vertices and take the fully covered 512×512 area, flipped to north side | The full resource is the same as the captured RDRAM bytes; the pixels and palettes of the 63 captured textures are matched byte by byte |
| Asia map layer | Resource 5605, similar model tile structure | Restore the effective rectangle of the atlas, and then cut out the 640×320 area | Static decoding and visual inspection; No real-time/playback binding of this scene |
| Avatar | Resource 29, 96×96 CI8 | TLUT using real capture; gray RGB inference + preserved source alpha | Resource bytes match capture, palette from actual sampling |
| Decorative border | Drawing strips of resource 1296 | Crop `[320,0,400,16]`, position on 96×96 transparent canvas | Use real captured TLUT; just a section of border, not verified full set of nine-square grid |
| Mechanical Icons | Resources 688 + Shared Team Palette 1010 | Original 16×16, deterministic nearest neighbor pre-upscaling | Color matching visually inspected; actual unit mapping and animation not verified |
| Forest samples | Atlas resources 6228 + palette 6237 | Atlas cutouts `[272,16,304,48]`, 32×32 | Not a complete scene; real tile segmentation and map adjacency have not been approved |

The originally planned ordinary scene background was replaced by forest atlas cuts in this round: although the scene background resources can be decompressed, their accurate palette matching has not yet been confirmed, and the guessed colors are not sent to the model as a formal comparison.

Low-resolution input is first nearest-neighbor pre-amplified to meet the editing model input size; this does not increase the original information. Output is 2048×2048, Asian samples are 2048×1024. The final comparison is also scaled back to the same source size/4x the size, to avoid equating large file sizes with effective HD.

There is a clear experimental limitation on the Asian sample: the water area in the original image is partially transparent, and a gray background was synthesized when it was sent to the model, but the map prompt words used still require a dark blue sea surface. This input is not consistent with the prompt constraints, and some outputs try to repaint blue waters. The results are only used to expose issues with transparent layer processing and are not included in cross-model fidelity sorting and are not used as publishable basemaps. In the next round, the independent water layer and background color should be clarified first, and the special prompt words should be revised.

Mechanical icon prompt words also describe the interpretation of the body structure of the low-definition image. The occurrence of whole-body reconstruction indicates that "16 pixel input + this prompt" is not constrained enough; this round cannot attribute all distortion to the model itself. After viewing the picture, the user has determined that the mechanical unit icon does not need to be processed, and therefore does not continue to advance this route.

## Actual access verification of the map

1. Select the first candidate for the European map using `qwen-image-3.0-pro`.
2. Generate a water mask from the original color palette, retaining deterministic bilinear amplification of the sea surface and the area approximately 3 source pixels from the coast. Blending AI results only inside the landmass. The RGB difference of the protected area relative to this baseline is **0 pixels**; the source alpha is recovered separately.
3. Switch back to 256×256 tiles according to the original atlas coordinates and flip transformation, and bind **58 RT64 hashes** that actually appear and are located within the selected tile. Other tiles continue to use the original resources.
4. Verified to 60th render in 960×720 output using raw RDRAM, OSTask and RT64/Metal; GPU reads frame when finished. The final tile package is `map-probe-final/hd-pack-stall`.
5. Generate another map + existing 22 outline glyphs package, showing that the two paths of text and background can take effect at the same time. The font came from the font replacement experiment at the time (deleted); this round did not allow AI to generate text, nor did unreviewed AI avatars be installed into the demonstration.

The evidence at that time was four reports: resource and texture binding, map protection and tile recording, map playback, and map and font combination playback.

The surface texture has been added to this snapshot, but users think the overall improvement is not obvious when looking at the picture. In order to maintain the geographical outline, the coast still retains the sense of steps brought by the limited sampling of the original image; successful access alone does not mean that the visual benefits are sufficient. Maps retain observations.

The control experiment of decoding the original image into PNG and then replacing it did not achieve completely consistent pixels in the entire frame: compared to the new packet-free playback of the same host, 32,561 of the 691,200 pixels were different, and most of the maximum channel errors were 1; only 100 pixels had a maximum channel error greater than 2, and the average RGB absolute error was 0.01922/255. This control experiment cannot be labeled as zero difference. Source texture/palette byte matching and the final render being identical pixel-by-pixel are two different pieces of evidence.

Duplicate entry assertion for RT64 `ReplacementMap::addLoadedTexture` triggered when initial HD package uses `preload`. To complete this isolation playback, the package was loaded using the officially supported `stall` and the output was successfully obtained; the renderer source code was not modified, and the root cause of the assertion was not considered fixed. The production loading strategy remains to be investigated. [RT64 loading method](https://github.com/rt64/rt64/blob/main/TEXTURE-PACKS.md#operation)

## The next stage direction after looking at the picture

- **Avatar**: Qwen 3.0 Candidate 2 is the current first choice. Subsequently, we will first verify the source Alpha synthesis, the actual display size of the game and the original character characteristics, and then use a small number of other characters to check the style and identity stability. Freezes selected outputs and does not consider recalled models as identical candidates.
- **Text**: Continue to use outline font.
- **UI Border**: The AI processing effect is not significant, and the generation is postponed; if you need to continue, separately verify the border/nine-square grid reconstructed according to size.
- **Mechanical unit icon**: Not processed, the original material will be used.
- **Forest and other map tiles**: On hold, batch generation and replacement are not currently involved.
- **Cross-scene map**: Keep for observation; if you continue later, first explain the visible benefits under actual display, and then evaluate the expansion scope. Existing replays only prove the replacement link within the snapshot and do not replace the real-time game process and cross-platform verification.

The low-resolution water mask IoU for the original candidate for the Euromap is 0.9779–0.9922; it reflects a rough outline drift of this sample and does not prove that island identity, mountain location, or visual quality are all correct. The "production pass rate" is not calculated based on this. All candidates are still experimental material and have not yet been released.

## Recurrence and file boundaries

> 2026-09-24: `extract_samples`, `prepare_samples`, `run_approved_batch`, `review_outputs`, `build_map_probe`, `build_gallery` and `review_decisions.json` used in this round have been deleted in the HD legacy cleanup. The following commands are only used for historical records; they are used for single requests. `tools/hd_ai/aliyun.py` (formerly `run_benchmark.py`).

The script at that time was located at `tools/hd_ai/`. Generated images, ROM decoded content, palettes, capture memory, temporary dependencies, and reporting are all located in ignored `assets/hd-ai/`; the original ROM, live game source code, and existing font packages are unmodified. Commit/push is not executed.

```sh
.venv/bin/python tools/hd_ai/extract_samples.py
.venv/bin/python -m tools.hd_ai.prepare_samples
# 有费用的运行必须沿用冻结清单。已存在请求记录会跳过，不会自动重试 POST。
.venv/bin/python -m tools.hd_ai.run_approved_batch /absolute/path/to/existing/.env
.venv/bin/python -m tools.hd_ai.review_outputs
.venv/bin/python -m tools.hd_ai.build_map_probe
```

The prompt words of this round are saved in `prepare_samples`, and it requires real snapshots/texture dumps; it is not a general resource exporter that is divorced from the evidence of this project. The European model input uses the original palette of RGB as the opaque basemap, and the runtime package additionally restores the original palette Alpha. Generated candidates should not request the model again on a production build.