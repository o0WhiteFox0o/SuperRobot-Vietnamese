> **Language / Ngôn ngữ:** [English](native-swap-screens.en.md) · [Tiếng Việt](native-swap-screens.vi.md) · [中文](native-swap-screens.md)

# のりかえ Screen: Pilot list, unit list, confirmation page and native takeover of Fairy Transfer

Date: 2026-09-23. Item 6 of the interplay menu (submenu パイロット／Fairy). The five original screens (screen numbers 6, 16, 17, 20, and 21) are taken over by the RmlUi page and the original composition is maintained; the transfer itself is injected into the A edge and handed over to the original function for completion, and the transfer of rosters, parts, and co-passengers is not rewritten by the page. The original screen can be selected back in the "Inter-session screen" on the settings page, see [Inter-session main menu](native-intermission-menu.md).

## 1. Original screen (static analysis)

The coordinates are all 320×240. The disassembly takes the instruction comments from the recompilation output. For the processing of のりかえ in the main menu (pop-up window and buzzer when the candidate list is empty), see [Inter-field main menu](native-intermission-menu.md) §3.

### Driver list (Screen 6) and Goblin list (Screen 20)

| Project | Basis |
| --- | --- |
| Layout 0x6F／0x88: Panel (21,21)–(299,219); Tag のりかえ（0xFD2）(144,24), 0x1002 Fairy／0xFEC (24,200), レベル (248,200) | Layout table |
| Initialization `801D25A4`/`801D4164`: Background (including random numbers), layout, `801CA75C` (`801C5618` Generate candidate pilot table `D_801DD3A8`: Organisms, pilots whose category has more than two available aircraft, `801C58BC` sorting; then count the number of pages, and sort by `D_801DD538` Decide whether to go back to the last page) or `801CAC0C` (`801C60DC` generates the fairy table `D_801DD550`); **9 rows per page**, starting from page `D_801DD14A` 1, row `D_801DEBC8`; `801C8ED8`/`801CAC84` Draw a list; `801CA524`/`801CAFE0` draw details and write the selected items into `D_801DEC5C` | `801D25A4`, `801D4164` |
| Row y=48＋16n: pilot name x=24, name of the aircraft being flown on x=96 (morphological offset of ゲッター group plus `801C8E50`; inorganic body `--`), Lenox=248, level x=280 | `801C8ED8`, `801CAC84` |
| Detail line y=200: Screen 6 is the name and level of the goblin (second crew member `+4 & 0x40`) on the cursor pilot's body; Screen 20 is the main pilot of the body where the goblin is located | `801CA524`, `801CAFE0` |
| Each frame `801D263C`/`801D41FC`: A → `D_801DEC58=0`, next picture 16/21; B → 0; nine lines up and down, page turning left and right (`801CD5B4`), redraw details | Same as above |

### Target aircraft list (Screen 16) and target pilot list (Screen 21)

| Project | Basis |
| --- | --- |
| Layout 0x7C／0x89: Panel (18,10)–(299,219); のりかえ (208,16), レベル (248,44), 0x1002／0xFEC (116,64), レベル (248,64) | Layout table |
| Initialization `801D2758`/`801D42FC`: background, layout, `801CA824` (`801C59AC` generates the body table `D_801DCF02` that the pilot can ride, quantity `D_801DD0A4`) or `801CB1A8` (`801C5C00` Generate a list of pilots who can ride with fairies), **7 lines per page**, starting from page `D_801DD544` 1, row `D_801DEC58`; avatar `801C6350` (16,8); full name (0x1287) (116,44), level (280,44); second line Fairy/main driver name (152,64) with level or `--------`/`--`; page number `%2d/%2d` (112,16); cursor sprite 0x14 (18,105) 281×16 | `801D2758`, `801D42FC` |
| Row y=106+16n: Screen 16 machine name x=24, pilot name x=152, HP (0xFE7) x=232, display HP x=256; screen 21 pilot name x=24, machine name x=152, Ryuru x=248, level x=280 | `801CA8AC`, `801CB230` |
| Each frame `801D2A24`: A → `D_801DD0A2=0`, next screen 17; B → 6; after moving, write the body slot number of the cursor line into `D_801DD3A0`. Each frame `801D4578`: Mode 0 A → Build pop-up window (layout 0x8A: 0x1012 (56,104), よろしいですか (56,122), はい／いいえ (224,128)/(224,148), cursor 0x15), mode 1; in mode 1, B closes the pop-up window, A and the cursor is 0 → Goblin board: Goblin `+0x38` points to the target body, target body `+0x3C`=goblin, `+0x34`=2, original body `+0x34`=1, `+0x3C`=0, return to the screen 20; B → 20 in mode 0 | `801D2A24`, `801D4578` |

### Confirmation page (Screen 17)

| Project | Basis |
| --- | --- |
| Layout 0x7D: Panel (18,10)–(302,219); レベル (114,18), HP (114,42), 0x1012 (182,138), よろしいですか (182,154), はい(224,176), いいえ (224,196), 0x1002 (24,106), 0x1013 (24,128), 0x1014 (20,144), limit (24,168), avoidance (0x100D) (24,185), hit (0xFF4) (24,202), terrain (0xFF6) (268,138), air, land and sea (264,154…202) | Layout table |
| Initialization `801D2B64`: avatar (16,8), target body battle map `801C6410` (176,8); pilot name (32,88), level (158,18); fairy name (64,106); `D_801DECBC` = mobility of the current body (organism time) `800A5254` + `801C4DE4` recalculated, otherwise 0); target body after recalculation: HP (134,42), body name (184,120), limit (64,168); avoidance = `+0x26`, hit = `+0x28`: `值+目标運動性` (64,y) Red when target limit exceeded, `值+当前運動性` (128,y); terrain: `800A6194(1, 驾驶员 rank, 机体 rank)` = sum of both: 0 for `-`, 1–3 D, 4–5 C, 6–7 B, 8 above A (288,154…); Cursor 0x14 (220,173) 30×20 | `801D2B64` |
| Each frame `801D3A90`: A and cursor 0 (はい) → transfer: the driver exchanges with the original driver of the target body (including co-passenger and status bit `+0x34`), parts are transported according to `801D33F4`, `801D35A4`/`801D3838` Recalculate, `800ABF70`, next screen 6; A and cursor 1 or B → screen 16 | `801D3A90` |

## 2. Takeover method

Source code: [`swap_page.cpp`](../../src/host/swap_page.cpp) (game thread adapter), [`frontend.cpp`](../../src/native/ui/frontend.cpp)’s `swap_sync` (page), [`game_hooks.cpp`](../../src/host/game_hooks.cpp) packaging (`swap_build`/`swap_step`/`swap_frame`, ten hooks in `generate_cpu.py`'s `NATIVE_HOOKS`). When the original version is selected in the "Inter-field screen" of the settings page, all five construction entrances are returned to the original screen; `SRW64_NATIVE_SWAP=0` or when profile is not loaded, the original screen is retained throughout the run.

| original function | wrapper |
| --- | --- |
| `801D25A4`／`801D4164` List initialization | Do not adjust the original function. Preserve background calls (with random numbers) and candidate table generation, row copies, `D_801DEC5C` writes |
| `801D263C`/`801D41FC` List per frame | Move/page adapter written by itself (9 lines per page); confirmation/return injected A/B |
| `801D2758`/`801D42FC` Target list initialization | Do not adjust the original function. Keep the background and target table generation; `D_801DD3A0` press the cursor first to write |
| `801D2A24` Each frame of the body list | Move/turn pages, write pages, lines and `D_801DD3A0`; confirm/return to inject A/B |
| `801D4578` Fairy target every frame | List mode: move and write by yourself; confirm switching from adapter to pop-up mode (the original A branch only builds pop-up sprites and text); return to injection B. Pop-up mode: はい Inject A (the original version completes the computer and returns to screen 20); いいえ/Cancel the window closed by the adapter |
| `801D2B64` Confirm initialization | Do not adjust the original function. Keep the background; `D_801DECBC` is written as the original mobility of the current body |
| `801D3A90` Confirm each frame | Move the cursor and write by yourself; confirm/return to inject A/B (the original version performs the transfer when はい) |

**Snapshot**: `status.swap_page`: `screen` (`pilots`/`fairies`/`targets`/`fairy_targets`/`confirm`), `serial`, `labels`; the list is `page`, `pages`, `cursor`, `rows[]` (`index`, `number`, __I NL_CODE_117__, `full_name`, `level`, `unit`, `art`), `sub{name,level}`; the target list is additional `pilot{…,unit}`, OK (airframe: `slot`, `name`, `pilot`, `hp`; pilot: same list row), goblin targets are `mode`, `window_cursor`; confirmation page is `pilot`, `from{name,pilot,sub,art}`, `to{slot,name,hp,limit,mobility,sub,art}`, `evade`/`hit{value,after,now,over}`, `terrain`, `cursor`. Event log `swap-page-events.jsonl`.

**Debug**: Stable ID `swap:N` (list line), `swap-yes`/`swap-no`; keyboard ↑↓, ←→ (page turning), Enter/Z, Esc/X; wait condition `swap_page`.

## 3. Real machine verification (2026-09-23)

```sh
.venv/bin/python tools/recomp/debug/check_swap.py            # 构建、跑测试关卡并检查
.venv/bin/python tools/recomp/debug/check_swap.py --reuse-build
```

There is no transferable object in the archive of the first episode (the main menu will beep directly). Candidate condition (`801C5618`): driver category (pilot ROM record `+0xB`, runtime `+0x32`) is non-0, and the same category in the roster (aircraft ROM record `+0x12`, runtime `+0x1A`), `+0x0C & 0x80` There are more than two units of the machine (category 1 can also be used as category 7, category 3 can also be used as category 4). The original machine (category 0) was never a candidate, so the test level `config/recomp/mini-stages/swap-test.json` was registered with `3D5A 95,0,117,500`, `3D5A 91,0,115,500` at the beginning of `flow.json` (no combat, `3D4A` ended)ヒイロ／ウイングガンダム and 五飞／ガンダムシュピーゲル (both category 3), after finishing the level and entering the interplay screen, there are candidates for のりかえ. **Register drones with `3D5A 999,0,机体,500` to experience destruction roster**: `800ABF70` → `800ABF08` reads bad pointer crash during tactical round.

Running `build/recomp/debug/20260923T042217.100733Z/`: `swap-checks.json` 12 items passed, exit code 0.

| Check | Results |
| --- | --- |
| Candidate list | ヒイロ／ウイングガンダム、五飞／アルトロンガンダム； ↓ Move |
| Unit list | The only aircraft that can be boarded by Hako is the Aアルトロンガンダム (Wu Fei is already on the list; the Atolu is not on the list - the rules of the original `801C59AC`, the page copies the results) |
| Confirmation page | ヒイロ → アルトロンガンダム: Limit 330, avoidance 120+115 (220), hit 113+115 (213), terrain CABA; ↓ to いいえ, Z return unit list |
| はい | The original version performs transfer: ヒイロ in the candidate list becomes アルトロンガンダム, Wufei becomes ウイングガンダム; and then changes back |
| Return |

Original version comparison (`build/recomp/debug/20260923T041326.824813Z/swapo-confirm.png`, set the same process after cutting the original version): Confirm that the terrain of the page is Empty C Land A Sea B Yu A——`800A6194` is the sum of the two ranks. The first version of the page is calculated as `-ABA` according to the lower level, which has been corrected; the name of the aircraft is below the battle map (184,120), two lines explaining "limited をうけるabilities/( )内は本のabilities" are on the left, and the second page of the page is formatted accordingly.

## 4. Not verified

- Goblin list and goblin boarding (Screen 20/21): There is no save file with goblins, only static analysis.
- Page turning of multi-page lists.