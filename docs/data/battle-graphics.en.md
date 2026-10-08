> **Language / Ngôn ngữ:** [English](battle-graphics.en.md) · [Tiếng Việt](battle-graphics.vi.md) · [中文](battle-graphics.md)

# Combat images: aircraft combat images, animation parts, special effects and cut-in

Updated: 2026-09-19. This article records 2D images used for combat and plot performances: resource distribution, binding tables, "elf scene" format and organization and export. How to use these scenes for weapon animation, and whether you can add custom bodies and weapons, see [Combat Animation and Customized Body](battle-animation.md). All static ROM parsing, no game launched.

## One-click export

```sh
.venv/bin/python -B tools/content/export_graphics.py
```

About 15 seconds, output to ignored `assets/original-graphics/` (about 70 MB), rerun the entire replacement. `index.html` is a picture gallery (needs to be opened via local HTTP, such as `python3 -m http.server --directory assets/original-graphics`). The thumbnails are horizontally arranged frame by frame and clicked to be APNG animations; `manifest.json` records the type, SHA-256, source resource and binding table index for each file.

| Directory/File | Content |
| --- | --- |
| `units/NNN-机体名/` | One folder for each of the 363 aircraft: `battle.png` basic combat postures, `battle-sheet.png` combat atlas of the aircraft (with its own color palette), `map-icon.png` map icons, `animations/` All animated parts on the aircraft atlas, `unit.json` (value; value of each weapon, attribute mark, combat record, animation record and hit special effects record, actor points to the exported image file one by one) |
| `cutins/NNNN-武器名/` | Combat cut-in: 14 Weaponsァイナルゴッドマーズ, Super Electromagnetic スピン, Sora Light Tooth Sword, V-MAX etc.), grouped by weapons, with the photo album used |
| `movies/NN-名称/` | 12 segments of fusion/transformation animations on the map (コン・バトラーV, ゴッドマーズ fusion, ゲッター 6 transformations, オーラロード 4 segments), numbered in the order of playback |
| `battle-scenes/atlas-AAAA/` | The rest of the battle scenes: special effects such as beams, explosions, slashes, and shields, grouped by album, with the entire album attached |
| `portraits/NNN-全名.png` | Avatars of 361 identities (multiple identities can share the same picture) |
| `chapter-titles/`, `maps/` | 133 chapter title cards; 158 static battlefield basemaps |
| `units.csv`, `weapons.csv` | General table of body and weapon values (UTF-8 BOM, table software can be opened directly) |
| `animations.json` | Analysis results of all weapon animations, hit special effects, and defense reaction records |

The original data browser image `assets/original-data/images/` is still named according to the resource number for browser use; this export reorganizes the same batch of avatars, map icons and battlefield basemaps according to the names of aircraft, characters, and weapons, and adds all battle images. Both use the same set of bindings.

## Resource distribution

The number is the ID of the 6,436-item resource table. The following table is just a distribution overview; which palette is matched with the image is based on the binding table read by the code, and is not inferred based on adjacent numbers.

| Resource Scope | Content |
| --- | --- |
| 9–308, 309–609 | Character avatars (CI8 96×96) and color palette; 1308–1311 are archive/select screen avatars for the four original protagonists |
| 687–1009, 1010 | Map icon (CI4 16×16) and our color palette |
| 1337–1368 | battle cut-in Close-up photo albumントロボ, レイズナー, ダンクーガ, シャッフルAlliance, etc.) and ゲッターTransformation Atlas |
| 1472–1478, 1521–1587 | Album of ゴッドマーズ fusion, ゲッターG transformation, オーラロード, コン・バトラーV fusion |
| 1399–1471, 1486–1611 | Scene data of the above cut-in/map animation |
| 1612–1907 (and 2762–2767, 2894, etc.) | **Aircraft Combat Atlas**, CI8, image type 7, dimensions 32k+1 (e.g. 257×193) |
| 1908–2212 | Aircraft Combat Atlas Palette |
| 2213–2476 | Basic body posture scene |
| 2477–2749, 3533–4257, etc. | Weapon animation parts and special effects scenes |
| 3006–3243, 3244–3532 | Special effects atlas (CI4/CI8) and color palette |
| 4267–4296, 4297–4326, 4327–4357 | Shield diagrams, palettes, scenes for shield defense |
| 4988–5104, 5105, 5106–5334 | Chapter title image (CI4 514×65), shared 16-color palette, title scene |
| 6067–6115, 6116–6227 | 320×240 CI4 background map and color palette, which belongs to the 3D combat background and is not included in this export |

## Binding table

(Scene, Atlas, Palette) Triplets are all 6 bytes `u16 scene, u16 atlas, u16 palette`, with 2 bytes at the end of the table padded with zeros. SHA-256 table bytes are fixed at `src/srw64_native/battle_graphics.py`.

| Table | ROM | Entry | Read Code | Index |
| --- | --- | ---: | --- | --- |
| Basic combat posture of the machine | `0x84E40` | 365 slots (0–362 valid) | Resident `func_8009C864` | Machine ID |
| Battle scene summary table | `0x11E3D0` | 1,053 slots (1,051 effective) | `func_801C3170` for battle overlay `load_00121560` | Registry fields for weapon animation actors |
| Map animation | `0x106F20–0x107200` | 12 segments, 95 items | Player for tactical map overlay `load_000AB160``func_802176A8(id)` | Animation number 0–11 |
| Chapter title | `0x84B20` | 133 | Resident `func_8009C8EC` (tactical map `func_801C72C8` called at the opening) | Title number |

- **Unit Table** Indexed by unit ID, visual check one by one: 0 ガンダムシュピーゲル, 3 シャイニングガンダム, 5ドモン・カッシュ(生生, dedicated small album 4930), 7 ノーベルガンダムB, etc. The callers are distributed in combat `load_00121560` (`801C5328`, `801C5808`, `8021FB4C`), tactical map `load_000AB160` and `load_0008E580`, `load_0008F4B0`, `load_0010DA50`, `load_00217FD0`. 330 atlases serve 363 units; morphological differences often share atlases (such as 11/12 ガンダムローズ).
- **354–362** (イーグル号…シャトル号, ブラックジョーカー, シュバルツ) value is the same as the weapon (HP 4000, パンチ/キック/rush), all borrowed from the combat map of シャイニングガンダム, and the combat unit table only has 354 rows - it is a placeholder record, see [Feasibility](battle-animation.md#加入自定义机体与武器).
- **Battle cut-in** are items 984–1038 of the combat scene master list, referenced by normal actors for weapon animations; 9 of them are not directly referenced by any weapon record.
- **Map animation**: The player uses `80098158(slot, 0, 0xB, 0x8D, scene, atlas, palette, 1)` to load it piece by piece. ID 5–10 share a piece of data of 30 items, divided into groups of 5 items. Trigger source (code confirmation): Script command `3D67` (ID 0–4), `3D6A` (ゴッドマーズ combination, ID 11), ゲッター system body 171–176 first transformation (controlled by 2-bit script variable, only released once; hold down START Can be rewatched, the meaning of the button is speculation), and the combination of Kono and Toro V (196). Caller ID 2 not found.
- Resident `0x847D0` has another 141-slot table of the same format, which is a summary of cut-in and map animations, but its read function `func_8009C7DC` does not have any calls (it is not in the function pointer table), and some entries are different from the two copies actually used; the 1,449-entry table of ROM `0x8AB58` belongs to the ROBO for debugging VIEWER(`load_00089EA0`). These two tables are not used in this export.

## Elf scene format

Scene resources cut an album into several pieces (mostly 32×32), assemble them into several frames, and then play them according to the step list. Big endian:

```text
u8  step_count, u8 vertex_mode
step_count × (u8 frame, u8 ticks)     frame = 0xFF：这几拍什么都不画
u8  0xFF, u8 loop_step                 结束标记；loop_step 为循环回到的步骤
u16 frame_offsets[n]                   n = (frame_offsets[0] − 表起点) / 2
frame：16 字节零件，直到 flags & 0x8000
    u16 flags   0x0010 = 水平翻转（其余位全 ROM 未出现）
    u16 s, t    图集内源坐标
    u8  w, h    零件尺寸
    s16 x, y    相对场景原点的屏幕坐标（y 向下）
    u32 vertex_offset
```

- **Playback** (code confirmation): Resident `func_80098880` calls `func_80098738` once per overlay frame for each of the 300 sprite slots (slot record `0x800FFA70 + slot × 0xC4`). It counts down and enters the next step when it reaches 0; when the last step is completed, the play flag bit0 of the slot is set and it stops at the last step (map animation), otherwise it jumps back to `loop_step` (`80098838`). So one shot = one sprite update; how many VIs it corresponds to are not checked, and the exported APNG is temporarily previewed at 33 ms per shot.
- **Drawing**: Rectangle painter `80096CD8` (mode 11, for map animation) reads only part records; vertex painter `8009761C` (mode 14–16) reads `vertex_mode`: 0 = 8 vertices per part, the first 4 are a group according to the part rectangle, the last 4 are x-inverted mirror groups (enemy and enemy orientation, when drawing) +0x40 optional); 1 = 4 vertices per part; 2 = no drawing. Both skip the 0xFF step.
- The vertex rectangles and flip positions of 19,408 Mode 0 parts are all consistent with the part records, and the export is drawn directly according to the part records. Mode 1 has 686 parts whose vertices are not simple rectangles (a scale/rotation type performance), and these shots are exported undistorted.
- The basic postures of the aircraft are only one frame; there are 470 battle scenes and some map animations are multi-frame.
- There are parts in 19 scenes that exceed the right/bottom edge of the atlas, and the out-of-border parts are treated as transparent (the actual machine is sampled according to the texture clamping/repeat rules, and the difference is only at the edge).
- Some palettes have more than the image can index: CI4 special effects often have 112 colors (7 groups × 16), and a few CI8 have 592 colors. Group 0 is used for export; the rest are palette animation data, and the group selection method is not tracked.

## Verify

- `tests/test_battle_graphics.py`: Composition use cases for step tables/blank frames/loops, flips, illegal inputs, overlong palettes and animation recording. When ROM is available, check each table hash and key binding, parse all scenes referenced by all tables, decode all atlases, and compare mode 0 parts and vertices one by one, confirming that 1,329+159+28 animation records all reference real scenes, and cut-in is referenced by exactly 14 weapons.
- `tests/test_original_images.py`: avatar, map icon, battlefield base map binding (image type 7 remains unchanged after adding decodable types).
- Visually inspected all 363 airframe basic poses, cut-ins, map animations and some weapon parts in the browser; the background map group table ROM `0x1161C0` (`(首资源, 数量)` pair, covering 6063–6214) was left as a follow-up clue for the 3D background.