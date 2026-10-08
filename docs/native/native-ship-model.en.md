> **Language / Ngôn ngữ:** [English](native-ship-model.en.md) · [Tiếng Việt](native-ship-model.vi.md) · [中文](native-ship-model.md)

# World map cutscene model HD: ships, landmarks and tracks

2026-09-24. On the world map between plots, the ships drawn on the front end of the track when the troops are sailing, the landmarks placed according to the scene, and the blue and white tracks are all replaced with high-precision versions drawn by the host GPU. 15 models have been redone according to official settings (08–21,000 faces each, original version 4–330 faces), the tracks have been replaced with smooth light strips, and the katakana nameplates display Japanese/Chinese/English according to the reading language. The game continues to provide position, orientation, camera and performance timing, without changing the ROM or writing RDRAM; F6 switches back to the original screen, and F7 switches the brand language.

## What to draw on the world map

The model object table `801C5670` (ROM `0xAAF30`) of the world map overlay `load_000A7EC0` collects all the three-dimensional resources that appear here: ships, 5600 markers, and the surface of each region. This time, three usage paths were read from the code and confirmed with the actual mini-level:

1. **Sailing ship**: `3D33` takes `D_801C5644` with `engine+0x990` (`3D72 n` is written as `n mod 15`) as the subscript. The value is the **model table subscript**, not the character number (the previous explanation of the layout lock has been corrected in place). When `n = 0` is used, take the body that ブライト (46) is riding on, and change it to the subscript through the body → model matching table `801C560C`; if it cannot be found, use 24.
2. **Landmarks placed by scene**: When entering the world map `801C310C` checks the 17 scenes of `801C5728` according to the current scene number, and then takes the (resources, locations) list from `801C57B0` and places them.
3. **Mark**: `801C2E30` Create 5600 yellow mark (slot `0x9C` onwards); the normal process only passes k = 0.

| Subscript | Resources | Model | Appearance | This time |
| --- | --- | --- | --- | --- |
| 0 | 5584 | アルビオン | Pairing table unit 53; `3D72 11` | HD |
| 1 | 5585 | アーガマ | Unit 51; `3D72 12` | HD |
| 2 | 5586 | アウドムラ | Unit 52; `3D72 10` | HD |
| 3 | 5587 | ミデア | Unit 64; `3D72 9` | HD |
| 4 | 5588 | ネェル・アーガマ | Unit 63; `3D72 13` | HD |
| 5 | 5589 | ピースミリオン (Gundam W, sector) | `3D72 7` (original script not used) | HD |
| 6 | 5590 | リーブラ(with name tag) | `3D72 6`; scene 84 landmarks | HD, name tag redrawn by language |
| 7 | 5591 | ラー・カイラム | Unit 69; `3D72 14` | HD |
| 8 | 5592 | ラビアンローズ (with name tag) | Unit 70; `3D72 4` | HD, name tag redrawn by language |
| 9 | 5593 | ゴラオン | Unit 244; `3D72 2` | HD |
| 10 | 5594 | グラン・ガラン | Unit 243; `3D72 1` | HD |
| 11 | 5595 | ガンドール (Super Beast Machine God ダンクーガ) | Unit 222; `3D72 3` | HD |
| 12 | 5596 | バルジ(with name tag) | `3D72 5` | HD, name tag redrawn by language |
| 15 | 5600 | yellow mark | always | [native drop](native-model-replacement.md) |
| 16 | 5601 | Red flag | Created without code | Not processed |
| 21 | 5597 | デビルアクシズ (with name tag) | No scene placement | Not processed |
| 22 | 5598 | アクシズ (bulletin board picture + name tag) | Landmarks in 13 scenes | HD, name tags redrawn by language |
| 23 | 5607 | フィフス・ルナ(with name tag) | Scene 103 Landmark | HD, name tag redrawn by language |
| 24 | 5587 | (Micro's second item) | `3D72 8`, default fallback | The original version will not be displayed, keep |

Subscripts 13, 14, 17–20 are the surface of each region (14 = 5599 universe; 18/19 = 5604/5605 earth), which are high-definition textures and are not within the scope of this page. The actual `3D72` parameters used by the original script are only 0, 3, 8, 10, 12, and 14; the other ships appear or never appear when ブライト happens to be on board, but they are also replaced and behave the same.

Landmark list: アクシズAppears before and after "Ana's Attack and Defense", before and after "Despair's Sorrow's Fist", "Ama's Shadow", "Asa's Rebellion" and "Terror! Ama's Begins to Move!" Before and after, "Screaming Universe" and "Decisive Universe" before and after, "駆り立てるAmbition", "Life, Sanって", "Haruka Nana Gamble", "Awakening Nana Dream"; Furuta Only in "シャアの rebel"; Ruri in "Victor's War". The scenes in "Agarashi Begins" also feature ordinary Agarashi, so 5597 has no chance to appear.

There are two display lists for resources with nameplates: hull (type 0) and nameplate (type 5). Component drawing `8008A914` draws type 5 as a bulletin board that always faces the camera; the main body of アクシズ is also a type 5 picture. When replacing the hull, only the one with the hull is moved (the one with the picture is replaced by アクシズ), and the name plate is redrawn according to the language (see the "Name Brand" section). The two share the same origin; アクシズ's HD model applies the same bulletin board matrix, so it is modeled according to the posture of the picture, always facing the camera.

## Setup and Modeling

The model is built locally with Blender and exported to `assets/models/<key>/mesh.json`; the warehouse only contains the packaging program [`build_native_models.py`](../../tools/models/build_native_models.py). The scripts, reference materials and material records for generating the model are all left in the local `assets/models/generators/` and are not entered into the warehouse (2026-10-06 user-defined: only package the model into HD package). Reference images are only viewable in a browser.

- **Coordinate system**: The local coordinates of each original resource are used, +Y is upward, the ship's bow direction is consistent with the original version (this batch is +Z), the size is based on the original bounding box, and the proportion is according to the official setting. According to the official aspect ratio, アウドムラ and ミデア are 16–21% shorter than the original version; the remaining major axis differences are within ±4%.
- **Output**: `assets/models/<key>/mesh.json` (position, corner-wise normal, sRGB vertex color, alpha < 128 for self-illuminating vents), `model.glb`, preview and `compare.png`. Mesh, like other HD assets, is only local to `assets/` and is not distributed with the source code.
- **Known trade-offs**: The color matching is based on the original model (2026-10-05 user determined): ゴラオン uses the original blue (peripheral products are dark gray green), アウドムラ uses the original ocher orange (TV setting is orange pink); ピースミリオンThere are only perspective color pictures, and the plane proportions follow the original version; the ネェル・アーガマ is based on the UC version proportions; the ガンドール dragon form refers to the prototype of modern products. The build script (local) for each model lists the remaining deficiencies.

The setting basis of Rare and Garra: "Counterattack" Rare and Rare class, total length 487 m, total width 165 m, Rare Rare Masao Shoichi; equipped with 4 miga particle cannons (3 at the front and 1 at the rear), 6 bow missiles, and 22 anti-aircraft guns Base, left and right ejection decks and aft landing deck, double bridge, engine block with long radiator plate ([ガンダムチャンネル](https://www.gundam-c.com/manual/mechanic/counter/ra-cailum.html), [ガンダムWiki](https://gundam.wiki.cre.jp/wiki/%E3%83%A9%E3%83%BC%E3%83%BB%E3%82%AB%E3%82%A4%E3%83%A9%E3%83%A0%E7%B4%9A)), the appearance is compared with [Cosmo Fleet Special](https://www.megahobby.jp/products/item/1437/).

## Track

The original track is gradually issued by `801C4960` every frame: one `G_QUAD` at each step, the vertices are taken from the buffer `801C97C0` (`801C3694` is appended to the translation template at each step), and the c of the PRIM color `(c, c, 255)` is gradually changed from 0 to `801C3958` according to the total number of steps. 255. The Earth area template is 10×10 blocks, one step every 8 units; the universe area is 6×6, every 4 units, height −10. The blocks are aligned on their axes and stacked into step sawtooth when sailing diagonally. The world map only has this kind of track, and the only difference between the two styles is the template.

When the host recognizes this set of commands (the fixed sequence of `FA`/`E7`/`G_VTX 8`/`G_QUAD`, the vertex address falls in the buffer, and the resident `801C4960` code is consistent with the ROM), it snaps the center, width and color of all steps on the first block, and suppresses the remaining blocks. The center point is an integer coordinate. First do the moving average of the end points; then draw a triangle strip: the width is equal to the original square, plus a 45% light halo, extending half a square at both ends, anti-aliasing the edges according to `fwidth`, and the color is gradually interpolated from the original `(c, c, 255)`. Depth comparison follows the original draw, no depth is written, and mixed drawing is performed.

## Tag: golden beacon

The dashed yellow ring outside the 5600 mark is a 28×28 horizontal square (y = 4) with a 64×64, 1-bit transparent map: 12 dashes, centered at atan2(−z, x) = 20.2° + 30°k, each about 10.5° long and with a radius of 0.87–0.955 half-width; offset by Draw the four TRI2 strips of `0x1A08`–`0x1A20` (both sides). The host recognizes these four when identifying 5600: the first one is replaced with a square piece of the same size, and a rounded arc segment is drawn in the fragment shader according to the above angle and radius (the edge is anti-aliased according to `fwidth`, plus a light and dark edge, which is more clear on light-colored land), and the rest is suppressed; the color is the original yellow. Like the 5600 body, it only takes effect when the HD screen is loaded and the 5600 resource pack is loaded.

On this basis, a "golden beacon" is made (the user selects from three directions): the host uses its own clock to drive the animation, and the position, lens and appearance time are still determined by the game.

- **Appear**: If the mark has not been drawn for more than 0.25 seconds, it is considered to have just appeared; the body and the ring will rebound and enlarge (ease-out-back) within 0.55 seconds, and at the same time, a brighter ripple will be emitted from the center (radius 4 → 16 units within 0.8 seconds). Opening fade in, triggered every time `3D33` arrives.
- **Stay**: The body floats up and down ±1.2 units along the local Y with a period of 2.8 seconds (multiplied by the local transformation before the game's world matrix, without changing the game data); the 12 segments of the dotted ring rotate 18° per second; a dark chassis under the center (radius about 8.5 units, within the dotted line) increases the contrast on the land; a circle of fade-out ripples expands from radius 5 to 15 every 2.4 seconds unit, disappears just after crossing the dotted line (radius about 12.8). All effects are collected near the original dotted ring (±14), which is no larger than the original mark; the ring square piece is only widened to ±17 units to allow the ripple to fade out.
- **Ontology modeling** is not here: 5600 resource package is maintained by another line of work, currently it is a golden polyhedron; the beacon only adds floating and entrance scaling.

## Famous Brand

The name tags of リーブラ, ラビアンローズ, バルジ, アクシズ, and フィフス・ルナ are 200×30 green framed black background signs (the green frame is 2 units wide, with one on each of the two inner sides) 64×64 katakana map), drawn above the same origin of the ship or landmark. The text is in the texture and does not go through the text system, so it is processed separately:

- **Name**: Japanese uses the original nameplate text; for Chinese and English, take the data area entry table `content/locales/terms/`. If not, check the line name list (フィフス・ルナ → Luna 5 / Fifth Luna, Chinese is consistent with the data area terrain name "5th ルナ"). Currently Libra, La Vie en Rose, Barge, Axis, and Fifth Luna. Just repackage the entry list after changing it.
- **Texture**: redraw according to the original brand style when packaging (8 pixels per unit, 1600×240; HarmonyOS Sans bold stroke, right tilt 0.22, plus dark shadow), one for each language; mipmap is generated after the host loads.
- **Drawing**: The nameplate display list (type 5) is also identified by command offset. The first one is replaced by a 200×30 textured quadrilateral, and the rest are suppressed. The language takes the current directory (`localization::snapshot()`) when classifying, and compiles the drawing id. The two rendering targets in the same frame are consistent; F7 takes effect immediately.
- **Screen Mode**: The nameplate is text, so in the original screen, only the Japanese version retains the original texture, and the Chinese and English still display the translated name; in the HD screen, all three languages ​​use redrawn brands.
- **Space area name tags**: Space surface 5599 itself carries 7 identical brands (type 5 display list 6–12: サイド1/2/3/5/6/7, スウィートウォーター). They do not change the grid, and there are only brand-name entries in the resource package (list `plates`, packaged script's `BOARDS`). The host still recognizes by command offset and draws by language. Chinese and English are Side 1…Side 7 (line translation) and Sweetwater. See [Drama World Map HD](native-worldmap-regions-hd.md).

Actual machine: The same level is started in Japanese, Chinese, and English respectively. The two landmarks and the nameplates of the three famous ships are displayed according to language, and the direction is consistent with the original version (the nameplate rotates with the course and is inverted when flying to the left, which is the original behavior); press F7 repeatedly during running, and the Axis nameplate changes to Japanese → Chinese → English; in the original screen, the Japanese text maintains the original texture, and the Chinese and English translations are displayed.

The Chinese version of "ラビアンローズ" has been unified as "La Vie en Rose" according to the user's decision (the entry list in the data area is consistent with the line name list). The Chinese name of バルジ is determined by the user as "Baruchi Fortress" (the full name of the terrain name and nameplate is used, and the words that appear alone in the lines are changed to "Baruchi"). The English name is unified as Barge (the line "バルジ fortress" is Barge Fortress).

## Host access

Follow the path of [5600 native water droplets](native-model-replacement.md):

- [`native_model_hook_patches.py`](../../tools/recomp/toolchain/native_model_hook_patches.py) Let RT64's `TRI2` (`G_QUAD` also go here) call the classification hook; ship DL is mainly `TRI2`.
- [`native_marker.cpp`](../../src/host/native_marker.cpp) Check the complete original resource byte by byte at the segment 4 base address. The command offset falls in the triangular command table of the replaced display list before hitting; the first one has the native drawing mark, the rest are suppressed (id segment `0x534D`), and the track id segment `0x5452`. The transformation comes from the immutable workload where the draw is located, and the depth setting follows the original draw; the ship shading is the vertex color plus main light, fill light, highlight and edge light.
- [`build_native_models.py`](../../tools/models/build_native_models.py) Retrieve each resource from ROM (check SHA-256), parse the triangle command of the replaced display list (reject matrix changes and sublist calls), and write `build/recomp/native-models/assets/` together with the grid; the sailing ship is enlarged 1.3 times when packaged (the selection is presented, the grid is still at the set scale), and the nameplates and landmarks are not enlarged. The manifest records the ROM location and fingerprint of the track code, as well as missing meshes and unprocessed resources.
- **The resource package does not contain ROM data** (from 2026-09-25, manifest `srw64.native-models.v2`, `srw64.native-marker.v2`): The original resource is only recorded in the manifest with the resource number, decoded byte number and SHA-256, and the track code is recorded with the ROM offset, length and SHA-256. The host decodes these originals (`src/native/app/rom_import_codec.hpp`, the same set as the importer) from the player's ROM when it first recognizes the display list, checks the summary and saves it in RDRAM word order, and then compares it byte by byte. The game has not been loaded into ROM when the renderer is created, so it is done during the first recognition; if the summary does not match, it will not be replaced, and `SRW64 native models disabled` will be written in the log. Only play back the frame probe of the display list without loading the game, use `SRW64_ROM_PATH` to point to `.z64`. The rest of the files in the package are all newly created: the mesh is from Blender modeling (the original model was only used for comparison rendering), the nameplate is generated from HarmonyOS Sans and drawn borders (Japanese is also retyped), and the 5600 mesh is generated in the original bipyramidal size. `validate()` requires every file in the directory to be in the list, and extra files (such as the old version of `*.reference.bin`) will directly report an error.
- Anti-aliasing: The host defaults to letting RT64 draw the entire scene at 4x MSAA (`SRW64_MSAA`, see [Development Guide](../guide/native-development.md)). These native pipelines are built according to the number of samples of the scene target, so the edges of ships and famous brands are also anti-aliased; the 5600 water drop pipeline is also changed to be cached according to the target format to avoid repeated compilation when the original size and the enlarged target alternate. The actual machine compared the entire mini-level process with dialogue (world map, tactical map, inter-field and archive pages) with frame-by-frame comparison when MSAA was turned off. The content of the screen was consistent and there was no missing or misplaced (edge ​​pixels are different); the horizontal bars in the transition are the same and are the game's own scan line effect.
- Switch: `SRW64_NATIVE_MODELS=<资源包>` or `run_host_probe.py --native-models`; the host behavior remains unchanged when not set. Linked to the picture mode, Original retains all original triangles and original tracks (see the previous section for nameplate rules).

## verify

Two mini-levels:

- [`worldmap-models.json`](../../config/recomp/mini-stages/worldmap-models.json): Binding scene 103, the world map automatically displays アクシズ and フィフス・ルナ; after locating two landmarks in sequence, `3D72 1`–`14` each make a short trip in the universe area `3D33`.
- [`worldmap-libra.json`](../../config/recomp/mini-stages/worldmap-libra.json): Bind scene 84, stop at リーブラ landmark.
- [`ra-cailum.json`](../../config/recomp/mini-stages/ra-cailum.json) for single ship display: two voyages each in the Earth and space areas.

```sh
.venv/bin/python tools/models/build_native_models.py
SRW64_NATIVE_MODELS=build/recomp/native-models/assets .venv/bin/python tools/recomp/debug/srw64ctl.py \
  launch --mini-stage config/recomp/mini-stages/worldmap-models.json --images hd
```

2026-09-24 Actual machine results:

- `worldmap-models` In one run, 15 models are all drawn natively (about 260-300 times each for the sailing ship, and 5,704 times each for the two landmarks). Press F6 to get the original frame and each has the original drawing, `rdram_modified: false`; 1,417 snapshots of the track, 2,834 native drawings, and no expired snapshots.
- Run the same level once in HD and Original, and take fixed-point screenshots every 50 VIs since entering; the timing of the level is determined, and the positions of the ships in the same frame are consistent, and they are compared one by one. All ship bows are facing the sailing direction, and the occlusion relationship between the nameplate and the ship body is consistent with the original version; `3D72 8` (subscript 24) has only tracks and no ships on both sides, which is consistent with the original version.
- `worldmap-libra`'s HD/original fixed-point screenshot: リーブラ Landmarks are replaced, and nameplates and marks are superimposed as usual.
- `tests/test_native_models.py`: Read two tables from ROM to confirm that `3D72 14` and body 69 both point to 5591; the command and triangle number of 5591; resource package round trip, tamper detection, bad mesh rejection; name brand naming, style and packaging of branded resources.

## Limitations and follow-up

- 5597 (デビルアクシズ) and 5601 (red mark) do not have exit paths and will not be processed for the time being; the map surface will be processed in high-definition textures.
- The original plot scene itself has not been walked on the real machine; the verification is based on the original world map overlay, original `3D72`/`3D33` and scene landmark initialization.
- The lighting is a fixed visual space approximation, with no shadows or environmental reflections; nozzle self-illumination and track halo are new features.
- Same as 5600, only accesses the macOS Metal path. Grid assets (`assets/models/`) are local only; resource bundles do not contain ROM data and can be distributed separately with HD bundles.