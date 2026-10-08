> **Language / Ngôn ngữ:** [English](native-ui-text.en.md) · [Tiếng Việt](native-ui-text.vi.md) · [中文](native-ui-text.md)

# Original interface text: high-definition native rendering and multi-language

Date: 2026-09-25. There is no original interface for native pages, including tactical maps, battle screens, and various pop-up windows. They originally used the ROM's 14-pixel font to draw characters, and the Chinese and English interfaces were still in Japanese. Now redrawn by the host in HarmonyOS Sans in place and displayed in the reading language. The layout, flow, cursor and color matching of the original version remain unchanged, and the game logic is not affected. Screens that already have native pages (between games, title menu, pre-battle confirmation, name page) do not go through here.

- **Text Engine**: Single-line labels, text windows and number pools are all taken over, see §2.
- **Combat HUD**: Counter/Defense/Recovery Badges and ability banners are changed to native text, and the HUD border is redrawn into high-definition slices according to the original design, see §3.
- **Window border and page turning triangle**: High-definition color number pictures are added to the frame palette, and the frame lines flash as usual, see §4; for the damage numbers of map battles, see §5; for those that have not been done yet, see §7.

## 1. How to draw characters in the original version (static analysis)

All original text goes through the resident text engine, which is drawn in two passes per frame. The basis is the disassembly of `8008DC40`, `8008EB5C`, the coordinates are both 320×240.

| Pool | Location | Records | Drawn by Who |
| --- | --- | --- | --- |
| Single line label | `8015CB00`, 60 slots, 0x34 bytes per slot | +0 text record number (printed text is 0); +2 category (1 is drawn in A trip, 2 is drawn in B trip, 3 is drawn in both passes); +3 palette number; +4/+8 is x/y; +0xC starts with glyph code and ends with 0xFFFF. The word fetching function `8008CF14` does not check the length, long labels will be written into the next slot | A trip `8008DC40` (level 0x8A), B trip `8008EB5C` (level 0x86, drawn on the pop-up window) |
| Text | `800FBAB0`, 2 slots, 0x218 bytes per slot | Dialogue, battle purpose, select limbs. +0x214 is the page number, +0x215 is the current page; draw the current page, line spacing 16 | A trip is drawn first |
| Number | `801613E0`, 20 slots, 8 bytes per slot | Type, value, x, y. Each frame is reformatted with sprintf (`+%d`, `-%d`, `%5d`, `?????`, `%3d`), glyphs taken from the 8×8 grid of resource 1159 | Types 1–6 in pass A, 7 and above in pass B |

**Show list**:
- Each record is loaded with the palette first: `FD10` Add 5 commands and load the data corresponding to the palette handle `D_80178B52[色号]`.
- 11 commands per non-space glyph, ending with `F2 F2 E4 E1 F1`: glyph 8×14 (narrow) or 14×14 (wide), 1:1.
- The number pool only contains the entire palette once, and each character (including spaces) occupies an 8×8 rectangle.
- The output is completely deterministic, and the pool contents are unchanged when the function first returns, so the host can map each rectangle back to its corresponding pool slot.

**Color**: Only color No. 1 of the font is the text, and No. 2-10 is anti-aliasing towards the dark background, without stroke. The eight color palettes are: resources 2 white, 3 red, 4 gray (not available), 8, 7, 5 gold, 6 green, 1160.

## 2. Takeover method

Source code: [`ui_text.cpp`](../../src/host/ui_text.cpp), draw the `place_texts` of the reused scene sprite renderer [`native_sprite.cpp`](../../src/host/native_sprite.cpp), and the text is rasterized in [`sprite_text.cpp`](../../src/host/sprite_text.cpp).

- **Hook**:
- The wrapper for `8008DC40` calls `ui_text_drawn(..., false)` after the dialogue module.
- `8008EB5C` is renamed to `srw64_original_text_front_draw` in `NATIVE_HOOKS` of `generate_cpu.py`, and is called `ui_text_drawn(..., true)` after packaging.
- **CHECK**:
- Reread the pool in engine order each time (text → tag by slot number → number), and check it with the display list one by one: the number of records, the palette address of each item, and the number of glyphs and first character position calculated for each tag according to "narrow 8, wide 14, space 8, newline + 14".
- If any part does not match, keep the entire trip as it is and record it in `ui-text.jsonl`.
- **Native drawing in one pass**:
- All the taken over glyph rectangles are cleared, leaving only the first one as a mark, and the previous one `F2` is replaced with a label.
- RT64 calls back the host at the mark, and the host draws all the text for this trip in the same rendering pass. The drawing order is the same as the original version, and pop-ups, transitions, and afterimages are all still covered on top.
- **Translation**:
- When the label still displays the Japanese of the record, the translation in the language directory is used, and the rules are the same as the speaker of the dialogue (`dialogue::label_text`).
- The name entered by the player and the printed text (record number 0) are drawn as they are in high definition.
- The grid/shoot/P/B/MAP before and after the weapon list name is replaced with the original icon in the symbol font (U+E000+font size).
- Icon glyphs without names in the glyph table (aircraft marks and map icons in the unit table) retain their original images.
- **Location**:
- The label (number, sprintf) with record number 0 is drawn grid by grid, and each character is centered in the original grid, so the column alignment remains unchanged.
- Exceptions are continuous grids where the font does not fit: ROM Kana is half-width 8 pixels, and the font is full-width. Each word of the lyrics of カラオケ has a label (the spacing between Chinese characters is 16, and the kana is 8), and the words can be overlapped in frame-by-frame drawings (discovered by user 2026-09-25). Adjacent grids (separated by less than a space of 8 pixels) are connected into a section. When the sum of the font width exceeds the original width of this section, the width of this section is divided according to the font width of each word. The words in the same section are uniformly narrowed and the font size remains unchanged; each word still uses its own label color, so the lyrics change color as usual. The paragraphs separated by spaces are processed separately; only the paragraphs with numbers and letters can be placed, and they are still drawn one by one.
- Other labels are left aligned at the original label. Two or more consecutive spaces in the original text are spaces reserved for numbers: each paragraph of text is returned to the starting point of the original paragraph.
- When the word order of the translation is different (for example, "The operation has ended"), move the number drawn in the blank space into the translated sentence, and draw the entire sentence together: There are still 4 machines that have not yet completed their operations.
- **Width**:
- Each piece of text can use the 4 pixels before the next thing on the same line (other labels, numbers, number pool entries).
- The text (Japanese) displayed as-is does not exceed the original width because the ROM's kana is half-width. The translation can be used about 35% more when there is nothing behind it.
- When exceeding the limit, first compress it horizontally: up to 70% for Chinese and Japanese, and 80% for English. If it is not enough, reduce the font size, up to 1.5 points. Therefore, font sizes in the same language remain consistent.
- **Font size**: Chinese and Japanese 12.5, English 12 (use Condensed first); the numbers and letters drawn by the grid use regular width SC in all languages.
- **Text window**: The dialogue box is drawn by the dialogue module and is not touched here. After all the text on the current page (such as the text outside the dialogue box (composition, selection text)) and other words on the current page are drawn out, draw the entire page with a line spacing of 16, and the width is the longest line of the original text.
- **Number Pool**:
- After formatting by type, draw grid by grid, retaining the original grid.
- The two sets of glyphs correspond to the original "white text with black borders" (types 1, 2, 7, and 8) and "white text with gray shadow" respectively.
- **When does it take effect**:
- Valid when dialogue module is configured. When Japanese plus original picture mode is turned off, it is the original picture. Other languages ​​will still be translated in the original picture mode, consistent with the convention of HD asset inventory.
- When "Original" is selected on the pre-war confirmation interface (`battle_ui` is `original`), that screen is processed in the original image mode: Chinese and English are translated as usual, and Japanese is the original ROM character; its window frame 1196/1197 also uses the original image. See [Pre-battle confirmation UI](native-battle-ui.md#三种界面2026-09-27).
- `SRW64_NATIVE_UI_TEXT=0` can be turned off for the entire run.

**Snapshot**: `status.ui_text` contains:
- Count: `passes`, `drawn`, `mismatched`, `labels`, `translated`, `glyphs`, `numbers`, `reader_owned`, `items_placed`, `items_waiting`.
- The content of the last two trips: `back`/`front`, each item is a label (`slot`, `record`, `x`, __INL _CODE_49__, `text`, `translated`, `consumed`), text (`body`), or number (`number`).

## 3. Combat HUD

**Badges and Ability Banners**: Mode 9 scene (drawn by `800945D4`, Atlas 1159, Palette 1160). First adjust `sprites::rewrite_grid` in `map_drawn` of `host.cpp`. After it recognizes the scene number, it clears the original grid and draws the native text in the same place.

| Scene | Original | Show |
| --- | --- | --- |
| 1142–1149, 1152, 1153, 1157 | Iフィールド、ビームコート、ゴッドシャドー、オーラバリア、プラネイトディフェンサー、マッハスペシャル, 真ッハスペシャル, clone, ゲッタービジョン, instant phantom foot, ハイパージャマー| Translation of ability name records 1020, 1019, 1026, 1022, 1021, 1024, 1025, 1023, 1100, 1101, 1116 |
| 1150, 1151 | シールド Defense, クリティカル | Interface tags `hud_shield_defense`, `hud_critical` |
| 1154–1156 | Counter, defense, return badge | `hud_counter`/`hud_defend`/`hud_evade`: Chinese counter/prevention/avoidance (the word "return" is not like avoidance in Chinese), English CTR/DEF/EVA |

The banner is a dark blue background with green gradient characters; the badge is a blue background with yellow characters in a yellow frame, 16×16.

**HUD Borders** (Scene 1193): Two 288×32 HP/EN panels composed of 19 slices from Resource 1296, Palette 1301. The dialogue box also uses this strip ([Dialog HD Border](native-dialogue-runtime-hd.md)), in which the upper and lower straight slices (source x 48, 208) are shared on both sides, and are still drawn with the dialogue box tool. The remaining 17 are redrawn by [`hud_frame_asset.py`](../../tools/hd_ai/hud_frame_asset.py):

- The position of the ribbon is shown in the ROM, and the colors are the same when redrawn with a dialogue frame: bright on the top and left, dark on the bottom and right, and a dark blue line in the innermost part. Press 4x to zoom in and stay sharp.
- The blue light bar is painted like a glass light bar like a dialogue frame.
- HP／EN uses HarmonyOS Sans Bold, ROM yellow characters are deepened with yellow shadow; slashes are drawn as anti-aliased straight lines.
- Crop each slice according to its position in the HUD, write to `worldmap-surfaces/pack-v2`, and replace by RT64 by texture hash. `--art` will register them into `content/art/stage1-hd.json`.

```sh
PYTHONPATH=src:. .venv/bin/python -B tools/hd_ai/hud_frame_asset.py \
  --pack assets/hd-ai/worldmap-surfaces/pack-v2 --output build/hd-ai/hud-frame \
  --art content/art/stage1-hd.json
```

## 4. Window border

The border of the original window is a mode 9 grid scene (drawn by `800945D4`): a 16×16 line segment grid of atlas 1295, some flipped horizontally, specified by the layout table `D_800C8BB8`, or determined by the tactical overlay selected at runtime (1165, 1172, 1173, 1014, and the number of menu lines) 1198, 1199, etc.). The page-turning red triangle is a similar scene to Album 1302. Some palettes are cycling (1016–1019, 1304), and the borders will flicker, so RT64 replacement by texture hash can only match the previous frame.

The method is the same as the tactical map HD: high-definition color number map plus frame palette. The border is redrawn by us using code (style A selected by the user on 2026-09-25: follow the original line position, double line, round head, smooth). It is generated by the player's own ROM when the game is running. These pictures are not included in the HD package, and it does not contain original pixels.

- **Generate** ([`rom_art.cpp`](../../src/host/rom_art.cpp), CPU only):
- `on_init` of `host.cpp` gives it the ROM. It reads the layout table, the scenes used by the tactical overlay, and the remaining grid scenes in 1165–1330, and builds a "Scene → Atlas, Palette" table, 146 in total.
- When a certain border appears for the first time, it is done on the decoding thread:
1. Spell out the 1× color number chart from ROM, just to know where the lines are;
2. According to the brightness of the palette, it is divided into two categories: blue line and dark shadow;
3. Redraw at 4 times the resolution: each pixel is a rounded stroke with a radius of 0.5, connected to the same up, down, left, right and diagonal neighbors (no diagonal lines when there are right-angle neighbors to avoid corner filling), the edges are anti-aliased, and the blue line covers the dark shadow;
4. Each texel on the stroke takes the color number of the nearest original pixel. The original version relied on palette cycling to allow light to flow along the frame, and this still works.
- The same file also generates full-frame high-definition images of the BANPRESTO logo and GAME OVER, see [Title Screen and Plot Text Image](native-title-and-story-images.md).
- **CHECK**: `make recomp-rom-art-test` Check the following three items. [`frame_hd.py`](../../tools/hd_ai/frame_hd.py) Use the same scene table and cropping to write the comparison directory `assets/hd-ai/frames/v1` (only on this machine, not included in the HD package).
- Tables, crops, reference palettes for 146 scenes consistent with `frame_hd.py`;
- The center of each original line pixel is covered by the stroke;
- The strokes only use the color numbers present in the original scene.
- **Runtime** ([`native_map.cpp`](../../src/host/native_map.cpp)):
- The +4 recorded by the sprite in mode 9 is the scene number (1198, 1199, 1227 confirmed on the actual machine), and the existing `host.cpp` is used to find resources.
- The border is generated only when there is HD art package (`SRW64_ART_PACK` is set), and it is only drawn in HD picture mode.
- Add the resource table to the resource table when each border appears for the first time. The original image will still be drawn in this frame, and the high-definition will be drawn in the next frame. The transparency of the basemap is equal to the palette transparency multiplied by the stroke coverage.
- uv is converted according to the starting point of cropping. Transparencies are mixed with premultiply, and palette differences are added in pass-through space, which was added by the Steam Deck session during the plume port (05f339c).
- Each grid of the small window is re-textured, and there is always a loading command between two adjacent rectangles. So the mark can also be placed next to SETTILESIZE: the rectangle drawn this time will be replaced, changing it has no effect.

Real machine: `check_ui_text.py` (Chinese) running `build/recomp/debug/20260925T060748.275759Z/`, 12 items passed. `hd-map-summary.json` shows 11 borders drawn, 888 overwrites, and no marker not found. The border lines of the command menu, troop table, and weapon table are smooth, the corners are beveled like the original version, and the positions and colors are consistent with the original version.

## 5. Damage numbers for map battles

When the combat animation is not playing, the damage/recovery numbers that pop up on the map are drawn by the `80209900` of the tactical overlay.

- Up to 6 cells, data in three places:
- The 1159 grid numbers of each grid are in `80228530`, where 0 is empty, 1 is `+`, 2 is `-`, 3–12 are white numbers with black edges, and 13–22 are white numbers with gray shadow;
- Display flag in `80228536`;
- x, y are in `80228548`.
- The display list has the same shape as the text engine: once the palette, then one rectangle per grid.
- `80209900` is renamed to `srw64_original_map_damage_draw` in `NATIVE_HOOKS`, and is called `damage_drawn` after packaging. `ui_text.cpp` After checking the number and position of the cells, draw high-definition figures one by one.

## 6. Real machine verification

```sh
.venv/bin/python tools/recomp/debug/check_ui_text.py --language zh-Hans   # 也可以 en、ja
```

Test level `battle-ui.json`: Unit command menu → Turn menu → Troop table → Battle purpose → End of round confirmation → Enemy turn → Original weapon table → Battle.

| Language | Run | Results |
| --- | --- | --- |
| Chinese | `build/recomp/debug/20260925T023727.281197Z/` | 11 passes: menu, unit list, combat objectives and two texts, "There are still 4 airframes that have not yet completed the operation" (digits moved into translation), weapon icons, HUD numbers, anti-badges, no failed verification trip |
| English | `build/recomp/debug/20260925T023850.869823Z/` | 11 passes (“4 unit(s) have not acted yet.”) |
| Japanese | `build/recomp/debug/20260925T023546.815759Z/` | 10 passes (Japanese does not move the numbers, there is no one); "The action is over" is narrowed within the original width and no longer covers the numbers |

See the screenshots one by one:
- Chinese round menu, troop list (same font size), confirmation window, combat objectives, and weapon list.
- English command menu, troop list, confirmation window, and weapon list.
- Japanese confirmation window, troop list, and weapon list.
- Combat HUD's HP/EN, slash, border and anti badges.

## 7. Not done and restricted

- **Scattered text not yet answered**:
- Mode 10 drawn ability banner: `8009504C` has no hook.
- Stage banner: Resources pending.
- **Select limb window**: The same text path is taken, but there is no real machine to enter the selected limb.
- **Text outside the dialog box of the original page**: It will only be taken over after the current page is fully displayed; the few frames where the text appears verbatim are still the original text.
- **First Frame**: New text must be rasterized in the background thread. When it first appears, the text will be empty for one or two frames, and will be cached thereafter.
- **Platform**: Native draw hooks are currently only Metal.