> **Language / Ngôn ngữ:** [English](native-model-viewer.en.md) · [Tiếng Việt](native-model-viewer.vi.md) · [中文](native-model-viewer.md)

# Local model resource browsing and 5600 verification

5600 The "native water drop · 3,968 faces" option and actual game comparison have been added. This version uses host GPU mesh and pixel-by-pixel lighting; see [Native Model Replacement](../native/native-model-replacement.md) for the trial entry, access methods and evidence.

Established on 2026-09-09, supplemented with actual game verification on 2026-09-10. The page source code is in `tools/model_viewer/`, and the generated page, model and texture are kept in the ignored `build/model-viewer/`. The service only listens to `127.0.0.1`, there are no uploads, cloud publishing or external texture requests.

## Browse page

The page contains **483** geometric containers analyzed this time, with a total of **82,122** triangles drawn; including spatial geometry and coplanar geometry, the number of containers cannot be regarded as the number of independent bodies or scenes.

- Filter by number/name search, geometry type and positioned status; thumbnail on left is from original coordinates.
- "Previous/Next" at the top of the model window and the left and right arrow keys on the keyboard switch according to the current filtering results; the current position is displayed, and the corresponding buttons are automatically disabled at the beginning and end. Selecting a card will scroll to a visible position within the list.
- Drag the mouse to rotate, scroll wheel to zoom, and right-click to pan; provide squint/front/top view, rotation, reset, and wireframe overlay.
- Three display methods: source map, gray mold, and wireframe; multiple display list resources can display components individually.
- Exports the current part's geometry OBJ in its original local coordinates; no materials, bones, or animations are exported.
- 5600 is turned on by default; when there is a native HD mark resource (`build/recomp/native-marker`) locally, you can switch between the original diamond (8 sides) and the native HD grid, and its actual machine comparison picture is displayed in the upper right corner. URL fragments can be targeted directly, such as `/#5584`.

Reuse current static survey input:

```sh
npm ci --prefix tools/model_viewer --ignore-scripts --no-audit --no-fund
.venv/bin/python tools/model_viewer/build.py
.venv/bin/python tools/model_viewer/serve.py
```

Print the local URL after the service is started; the port can be specified with `--port`. The build inputs are the original resources under `assets/models/3d-2026-09-09/`, `geometry-data.json` and `geometry-survey.json`, see [3D Analysis](3d-model-replacement-analysis.md) for details. Three.js is fixed to `0.180.0`, and the dependent license is output with the page.

## Show bounds and checks

The page displays local vertices, triangles, and simplified materials and does not simulate original game scene transformations, lenses, animations, full RDP blending, or lighting. Multiple parts may also be effect frames, and all parts displayed at the same time cannot be regarded as one game gesture.

**2,713** texture files have been extracted; **27** resources contain unconfirmed texture loading methods, and the corresponding batches fall back to solid colors, as the page clearly prompts. The source map view makes it easy to identify assets and does not claim to be equivalent to RT64 game footage.

All 483 models were checked post-build for triangle count, vertex/UV length, finite values, and all texture/thumbnail references. Each of the 70 source textures in 5604 and 5605 is consistent with the RGBA pixels of the existing map extractor. JavaScript syntax, Python compilation, and native HTTP requests pass.

The browser reproduces an issue with table of contents cards being compressed to 2 pixels high by automatic grid rows; instead it calculates row heights based on content and lets thumbnails scale proportionally. After the repair, the layout height of all 483 cards was checked, the screenshots of 5631 and 5604 pages were actually viewed, and 5631 → 5632 → 5631, the head and tail disabling in the positioned filter, and the empty search result disabling were measured. JavaScript errors are not logged by the browser. These checks only verify page interactions and do not add game runtime evidence.

## 5600: Screen ownership and fixed topology deformation confirmed

Using the existing task snapshot of `female-story-2`, three independent copies are generated. The task descriptors are byte-for-byte identical and the original snapshot remains unchanged.

| Playback | Modification range | GPU image results |
| --- | --- | --- |
| baseline | No modification | Original yellow diamond and dotted ring |
| hidden | 12 sets of triangle commands changed to F3DEX2 SP no-op; 52 bytes actual change | diamonds and dashed rings gone; 1,369 pixel changes, range `(437,305)–(521,377)` |
| stretched | Only six three-dimensional vertices are changed, X/Z is multiplied by 2, Y is multiplied by 3; 14 bytes are actually changed | The three-dimensional part is lengthened, rings and other images are retained; 4,639 pixels are changed, the range is `(439,282)–(521,395)` |

The three RT64/Metal playbacks all exited 0; the 960×720 images read back by the GPU after completion have been viewed one by one. The pixel difference outside the target marked area is 0.

This proves that **5600 indeed corresponds to the yellow diamond and ring planes of the plot map, and also proves that modifying its vertices will enter actual RT64 drawing**. The scope of the evidence in this section is single-task rendering playback; see below for subsequent topology replacement and actual game loading.

## 5600: High-model prototype and experimental ROM (removed)

2026-09-24: The 96-sided high-module prototype, the experimental ROM that encoded the mesh into Resource 5600, as well as their playback and real-machine verification, have been replaced by [native HD tag](../native/native-model-replacement.md). The relevant scripts, `model5600` ROM variants, tests, and two model directories have been deleted in the HD legacy cleanup, and the browser no longer displays them; the replay evidence from the previous section is for historical purposes only.

## 5584: Found the static entrance, still need plot trigger evidence

2026-09-24 Update: This table is the model object table of the plot world map. 5584 is アルビオン (body → model matching table `801C560C`), which is drawn by `3D33` during navigation; each ship corresponds to 5591 ラー・カイラムFor a real machine replacement, see [World Map Cut Scene Model HD](../native/native-ship-model.md). The static analysis at that time is retained below.

`load_000A7EC0` in ROM `0xAAF30` / VRAM `0x801C5670` is the model object resource table, index 0 is 5584, index 15 is 5600. The table also contains previously extracted ship shape resources and map resources.

`0x801C3490` selects the table entry according to the low byte of the second parameter; `0x801C34EC` reads the resource ID, and then `0x801C3560` calls `0x8008B4F4` to write the resource ID into the parameter area `sp+0x1C`. There is also `0x801C4DC0` that compares/updates objects with selected values ​​in `0x801C58BC` and calls the same build path in `0x801C4E30`.

The subsequent verification method is: after confirming the identity of this overlay, trace the index 0 call of `0x801C3490`, record the caller, script location and scene, and then obtain the actual GPU frame. Currently, only static tables and call paths have been located, and there is no confirmation of chapters, ship names, or the actual appearance of this resource in the measured route. For structured records, see [model-5584-reference.json](../../assets/models/3d-2026-09-09/model-5584-reference.json).