> **Language / Ngôn ngữ:** [English](native-intermission-menu.en.md) · [Tiếng Việt](native-intermission-menu.vi.md) · [中文](native-intermission-menu.md)

# Inter-field main menu: original logic and native takeover

Date: 2026-09-21. Status: **Implemented, full menu has been verified on the real machine; two menus and RNG control have not yet been run for verification** (see Section 9). Sections 1–3 are the static analysis conclusions (disassembly and ROM data table) of `load_0008F4B0` and the resident section; Section 4 onwards is the takeover plan. The screen baseline is the original screenshot left by `sdl-link-01` running, and the running directory is not retained.

## 1. Original screen

The background is a large picture that is selected as the process progresses, with four dark blue translucent right-angled panels with blue thin edges stacked on top. The current menu item is represented by a green highlight bar and white dot matrix characters. The coordinates are all 320×240:

| Panel | Rectangle (top left – bottom right) | Content |
| --- | --- | --- |
| Title | (120,25)–(199,39) | `0xFCC` インターミッション, text starting point (124,25) |
| Menu | (33,41)–(103,183); the two menus are (33,41)–(103,71) | Text x=34, y=41+16×n; highlight bar x=33, width 70, height 16 |
| Information | (145,49)–(287,79) | `0xFD6` 総ターンnumber/funds in (146,50); values are right-justified, `%4d` in (254,49), `%8d` in (222,65) |
| Chapter | (34,193)–(287,207) | `0xFD7` episode ␣␣ is in (34,193); episode number `%2d` is in (48,193); title text number `8010F5F1+0x119` is in (82,193), followed by `0xFE0`クリア |

The rectangle comes from the layout's display list (F3DEX2 `G_FILLRECT`, 10.2 fixed point), not measured from the screenshot.のりかえ popup (layout 0x86) rectangle (109,121)–(155,160), two items `0xFEC` パイロット (112,123), `0x1002` fairy (112,143), cursor step size 20.

Menu item text number `0xFCD`–`0xFD5`：データセーブ、ユニット开Build, weapon modification, ユニット ability, パイロット ability, のりかえ, strengthened パーツ, リンク, sub-のマップへ.

## 2. Scheduling framework

- Entry `801D8F74(mode)`: clear `D_801DECB8` (next screen), `D_801DECCC` (current screen), `D_801DD540` (exit code), `D_801DD548` (main menu cursor), adjust main menu initialization, `8007E810(0x21)`, and register `801D8D20` as a per-frame task.
- `801D8D20` Read transition status `80099B30()` for each frame:
- 3 (fade out end): exit code 2 → enter the next level (`80080188(0xC)` followed by `801D9F74`); exit code 1 → soft reset; otherwise clear the sprite and text slot, press `D_801DECB8×8` to check `D_801DC9D0` to adjust the screen initialization.
- -1 (idle) and `D_8015D9FA & 0x3000 == 0x3000` (both keys pressed simultaneously): Exit code 1, transition.
- Not 0 or 2: adjust the function of each frame of the current picture.
- Screen table 23 items {initialization, each frame}: 0 main menu; 1–8 corresponding to menu items 1–8; 9–22 sub-screens (10 transformation details, 20/21 Fairy のりかえ, 22 reached by Rinko). Write 0 in B of each screen to return to the main menu, and the transitions will always be `80099814(5,1,2)`.
- `801D796C`–`801D8CC8` is a chain of legacy test frames that no one references.

## 3. Main menu (Screen 0)

| Function | Effect |
| --- | --- |
| `801CDF30` Initialization | First entry (`D_801DC240==0`): `80085B94(0,0)` brightens the background, `D_801DD5CC=30` frame delay; enters again: `80085B94(0,1)` darkens the background, no delay. Clear `D_801DEC50` (built flag), fade in `80099814(4,2,0)`. |
| `801CDFB0` Build | Check whether `8010F5F1` is in `D_801DC6D4` (13 "(previous)" scenes + 132 "アクシズのattack and defense (middle)"): hit with layout 0x8D, `D_801DECD8=10`; otherwise layout 0x69, `D_801DECD8=0`. Draw values ​​and chapter titles, build cursors (elf slot 0x14, image 0x8E, animation `801C45F4`), `80085B94(0,1)`, `D_801DEC50=1`. |
| `801CE19C` per frame | When built, first run the cursor `801C4A20` (read 0x800/0x400 of `D_801DD62C`, loop, sound effect 0xB9), and **each frame** write `D_801DECB8` as cursor + 1 (two menus: 0→1, 1→9). Idle and not built: build after countdown. Idle and built: see below. |

Key processing when idle (`D_80178A08`: A=0x8000, B=0x4000):

- `D_801DECD8==0` (full menu) Press A, sound effect 0xB7:
- Next screen 9: `D_801DD540=2`, transition (to the next level).
- Next screen 8 (リンク): `801D9300`, `801D93C4` → `D_801DD114`; if it is 0, it will go to screen 8, if it is not 0, it will go to screen 22.
- Next screen 6 (のりかえ): Create layout 0x86 pop-up window and slot 0x15 cursor, `D_801DECD8=1`, no transition.
- The rest: `801CDE9C` (clear the selection cache of each sub-screen) and then transition.
- `D_801DECD8==1` (のりかえ pop-up window): B closes the pop-up window (0xB8); A first `801CDE9C`, cursor 0 adjusts `801C5618`, cursor 1 adjusts `801C5E64` to build a candidate list, return 0 and buzz 0xB8 remains in the pop-up window, otherwise `D_801DEC60=光标`, the goblin changed the next screen to 0x14, transition. Branch A does not touch the pop-up wizard.
- `D_801DECD8==10` (two-item menu) Press A: Same as "Next Screen 9" or normal transition.

Two points will constrain the takeover method:

1. `80085B94` adjusts `80082334` (random upper limit) every time, **consuming RNG**, see below. Calls to it during initialization and build must be left intact.
2. `801C5618`/`801C5E64` only writes the candidate table in the coverage segment (without `jal`), which is the table to be used later in the のりかえ screen and can be called locally.

### Background image

There are **8 pictures** in total, each of which is a 320×240 8-bit indexed picture (resource `0x155E`–`0x1565`), each with two sets of 256 color palettes (`0x1566`–`0x156D`, `0x156E`–`0x1575`). Confirm that all resource decoders of the used project have been decoded.

`80085A24` Scan our body pool (`8016A210`, 140 slots × 0x54, the body number is `+2`), take the first protagonist machine to determine the category; `80085B94(槽, 暗)` Check by category `D_800C59AC` (8 bytes/item: picture, bright palette, dark palette, number of candidates):

| Category | Protagonist | Picture |
| ---: | --- | --- |
| 0 | アシュクリーフ `0x1F` | `0x155E` |
| 1 | ソルデファー `0x1E` | `0x155F` |
| 2 | スヴァンヒルド `0x20` | `0x1560` |
| 3 | ラーズグリーズ `0x21` | `0x1561` |
| 4 | アースゲイン `0x22` | `0x1562` |
| 5 | スーパーアースゲイン `0x132` | `0x1563` |
| 6 | スイームルグ `0x24` | `0x1564` |
| 7 | スイームルグS `0x133` | `0x1565` |
| 8 | The protagonist machine cannot be found | Same category 0 |

Therefore, the background does not change with the number of episodes, but only with the protagonist's machine (including the two enhanced models that will be transferred later). Each candidate number is 1, `80082334(1)` always gets 0, but the call itself still advances the RNG; the "choose one of nine" branch of category 9 is not available in this game. The bright palette is used when entering for the first time, and the dark palette is changed when the menu is built and when returning from the sub-screen, and the image itself remains unchanged. The background is drawn at sprite slot 0, `80098158(槽, 0, 4, 0xA4, 0, 图, 调色板, 0)`.

## 4. Take over the target

1. **Look and feel unchanged, clarity and language modernized. ** Keep the background image, the position proportions of the four panels, the dark blue translucent bottom, the thin blue edges, the green highlight bars and the white text; use vector fonts, follow the window scaling, and the text will be in the Chinese/Japanese/English directory. Do not change to a new card-style design (full-page rearrangement like the Rinko page does not apply here).
2. **Zero changes to the process. ** What happens after selecting which item (inspection, sound effects, transitions, RNG, exit code) is still determined by the original function; the adaptation layer only replaces "draw" and "read key".
3. **Both the mouse and keyboard can complete all operations**, and the B/Esc behavior is consistent with the original version (B on the main menu is invalid, and B in the pop-up window is closed).
4. Can be turned off: Select the original version (`intermission_ui` of `presentation.json`, debugging interface `settings {"intermission_ui": "original"}`) in the "Inter-field screen" on the settings page. It will take effect when the next screen is built. The opened native page will be closed when leaving; `SRW64_NATIVE_INTERMISSION=0` or if the profile is not loaded, the original screen will be retained during the entire run. Verification script `tools/recomp/debug/check_intermission_ui_switch.py` (2026-09-23, `build/recomp/debug/20260923T025544.572614Z/`, 8 items passed, exit code 0: When the native menu is open, switch to the original version, enter the ユニット transformation, the original list appears, B returns to the original menu; after switching back to the new version, Z enters the native list, B returns to the native menu, and the cursor is still thereユニット transformation; `presentation-settings.json` followed by writing `intermission_ui`; 2026-09-23 `build/recomp/debug/20260923T045406.607280Z/` 9 items passed, added to the original menu and went up リンク The original linkage screen appears instead of the native linkage page).

Out of the scope of this page: The eight sub-screens are still the original ones (except for the Rinko front page). There will be a look and feel switch when entering the original sub-screen from the native main menu, which is a known transition state for phased takeover.

## 5. Takeover plan

Follow the pattern of the pre-war page: the game thread adapter publishes JSON snapshots, `frontend.cpp` read-only snapshots, returns semantic actions with serial, and does not read RDRAM.

**Hook** (two new items are added to `NATIVE_HOOKS` of `generate_cpu.py`, and the CPU code needs to be regenerated after modification):

| Original function | Packaging behavior |
| --- | --- |
| `801CDFB0` Build | Do not adjust the original function. Copy the non-drawing part of it: determine the two menu items and write `D_801DECD8`, `80085B94(0,1)`, `D_801DEC50=1`. No layout, text and cursor are built, so the original panel will not appear, and it will not occupy the sprite slot or text slot. Then publish the snapshot and the page will be visible. |
| `801CE19C` per frame | The input has been filtered to 0 while the page is visible, and the original function is called as usual (it will just idle and refresh `D_801DECB8`). Receive `choose:N`: write `D_801DD548=N`, give `D_80178A08` an A edge, adjust the original function, and restore `D_80178A08`. Received `move:N`: Write the cursor and play the original movement sound 0xB9, so the cursor stays in the game and stops at the original item when returning from the sprite. |

Initialization `801CDF30` is not hooked: the background, 30-frame delay, and fade-in remain unchanged.

Note that the original per-frame function called `801C4A20` for slot 0x14 when it was built. It has only two branches, `0x800` and `0x400`. If neither branch hits, it returns directly and writes zero (confirmed by the disassembly); `D_801DD62C` of the frame where the A edge is injected is still 0. Therefore it is safe not to build a cursor sprite.

The original function only handles A when `80099B30()==-1`. The adapter must consume the action under the same conditions, otherwise it will be left to the next frame and cannot be lost.

**のりかえ**: The original page displays the "Driver/Fairy" secondary menu by itself, and the original pop-up window is not created. When confirming, the adapter writes `D_801DECB8=6`, `D_801DECD8=1`, `D_801DEC58=选择`, injects A, and adjusts the original function; it completes the check, `D_801DEC60`, picture number and transition. If the transition does not start after returning (the candidate is empty and the original version has been played), reset `D_801DECD8` to 0, and the page will remain open and prompt that it is unavailable. Advanced: When opening the secondary menu, first adjust two candidate table functions locally and gray out the empty one.

**リンク**: No special treatment, the original function will take the `801D9300/801D93C4` branch by itself after the A edge, and then the existing リンク page will take over.

**Snapshot fields**: `serial`, `visible`, `restricted` (two-item menu), `cursor`, `turns` (`8010F5EC` u16), `funds` (`8010F5F4` u32), `episode` (`8010F5EF`), `scene` (`8010F5F1`), `title_key` (`base:t00_{281+scene}`), `submenu` (のりかえ secondary menu status).

**Visible timing**: `D_801DECCC==0` is visible when it has been constructed and the exit code is 0; when the action is submitted (transition starts), it is hidden and enters the key release gate. The fade in and fade out is still the original effect in the game screen. The page itself makes a short opacity transition to align with it; it does not pursue frame-by-frame synchronization.

**Input**: `host.cpp` Add `intermission_page::input` to the filter chain; add one channel to each of `sync/choose/dispatch/summary` of `frontend.cpp`, parallel to link/battle. Arrow keys and Tab cycle movement (retaining the original head-to-tail cycle), Enter/Z confirms, and Esc/X is only valid in the secondary menu.

**Soft reset key combination**: The original version reads and holds the state `D_8015D9FA` in the scheduler. This combination will be eaten when the page has input. Solution: The filter allows "press and hold two keys at the same time" and does not make a native alternative entry.

## 6. Visual specifications

- Use 320×240 as the design coordinates, scale proportionally according to the short side of the window, use the rectangle of Section 1 for the four panels; center the whole at window ratios other than 4:3, and the background is still drawn by the game.
- Panel: dark blue translucent bottom (take the original look and feel, about `rgba(10,14,60,0.78)`, adjust it to the screenshot when implementing), blue edge of 1 design pixel (about `#3A78E0`), right angle.
- Highlight bar: original green (approximately `#00C800`) solid bar, width is the same as the width of the menu panel, and the text remains white; use the same color and low transparency for mouse hovering to avoid confusion with the current item; the hovering color is only displayed after the mouse is actually moved or clicked, and is retracted as soon as the button or handle is pressed (`pointer_mode` of `frontend.cpp`, `pointer_mode` of the page body `pointer` class), otherwise the pointer parked in the window will keep a certain line with a light green bar (discovered by user 2026-09-25 on the track list).
- Font: Follow the font discovery found in the shared UI; the font height is designed to be 16 pixels and the line spacing is approximately 13–14. If Chinese and English are too wide, tighten the character spacing first and then reduce it. Do not wrap lines or expand the panel (English "Pilot Abilities" is the longest item and needs to be measured).
- Values ​​are right-aligned to the original position; funds retain an 8-bit width alignment baseline without adding thousandths (consistent with the original and modified screens).
- The chapter line format follows the table of contents template, such as `第{n}话 {title} 通关`, and the title falls back to Japanese when it is not translated.
- Modernization only adds two things: a very light button prompt on the bottom line (the same as the Rinko page), and an optional one-sentence description of the current item; both of them do not enter the four panels, and they correspond to the original panel one by one after they are turned off.

## 6a. Direct modification of funds (2026-09-22)

The fund number in the main menu and transformation screen is a button: after clicking, the original position becomes an input box (the old number is selected). After entering an integer from 0 to 99999999, Enter immediately writes `D_8010F5F4`, and Esc cancels. The write is completed on the game thread (adapter action `funds:N`, `intermission_menu.hpp::parse_funds` check), the page and subsequent transformation judgments read the new number; the event log records `{"kind":"funds"}`. This is a convenient function of the built-in MOD. It is not controlled by the rule switch, and does not make legality judgments beyond the upper limit (the original display width is 8 digits, so the upper limit is 99,999,999).

Debugging interface: `ui.click --text intermission-funds` (renovation screen `upgrade-funds`) → `ui.type 900000` → `ui.key return`; `tools/recomp/debug/check_funds.py` covers the main menu modification, Esc cancellation, five screen modifications, the funds/confirmation window, and the deduction based on the new number (8 If the entry passes, run `build/recomp/debug/` (see script output).

## 7. Localization

- `entries` of `content/locales/*.json` is not currently available `t00_04044`–`04055` (title, nine items, information tag, chapter ␣␣), `04064` (クリア), `04076`/`04098` (パイロット/ fairy). Chinese and English translations are needed; the Japanese source text is required.
- Chapter titles `t00_00281`+: about 140 items. The current table of contents only covers the first draft of the chapter. We are not responsible for completing this page, and will return it to Japanese if it is not translated.
- Put the `ui` tag in the template copy (the nth episode, key prompt, and unavailability reason), and the key name prefix is `intermission_`.

## 8. Verification plan

Static and components:

- The adapter's "two menu determinations" are written as pure functions, and unit tests are performed on 14 scene numbers plus a number of non-hit values (`tests/native_*.cpp` style).
- `test_*` Added: `NATIVE_HOOKS` contains two new hooks, `game_hooks.cpp` has corresponding packaging (imitation of `test_link_battler.py`).

Run (need to obtain consent first; continue to use the debugging interface):

1. `srw64ctl launch --save build/recomp/save-recovery-check/intermission-cold-1.source.sram`, read the file through the title ring and enter the venue.
2. `ui.tree` Assertion: title, 9 items, round 7, funds 14500, `第 1 话 …`; screenshots are manually compared with the original baseline side by side for panel position.
3. Enter item by item and press B to return: the page will reappear each time and the cursor will stop at the original item (the original `D_801DD548` is not cleared).
4. のりかえ Secondary menu: driver, goblin (there should be no goblin in the first episode archive → buzzer, the page is still there), Esc to close.
5. リンク → Native linkage page → Return → Main menu.
6. Submariner: Exit code 2, enter the next level.
7. Two menus: requires a save after the "(previous)" scene. First find a ready-made archive; if not, use the archive editing tool to change the scene byte to 38 to make a controlled sample, and indicate it as an edited sample in the report.
8. Three languages × 800×600/960×720/1100×760; release gate control after pressing and holding Z to confirm; the main menu does not respond when the setting page overlay is opened.
9. RNG comparison: The same archive, the same input sequence, run the original version and the takeover once each, and compare the RNG status when entering the sub-screen (verify that the number of `80085B94` calls has not changed).

## 9. Implementation status and steps

Completed (2026-09-21):

- [`intermission_page.cpp`](../../src/host/intermission_page.cpp): Build/three callbacks per frame/frame boundary, snapshot, action, event log `intermission-events.jsonl`; pure logic in [`intermission_menu.hpp`](../../src/host/intermission_menu.hpp).
- [`game_hooks.cpp`](../../src/host/game_hooks.cpp), `generate_cpu.py`: two hooks; `host.cpp` input filter chain; `status.intermission_page` of `debug_server.cpp`.
- [`frontend.cpp`](../../src/native/ui/frontend.cpp): The four panels are positioned equally according to 320×240 coordinates, the text is automatically reduced according to the panel width (English menu items are wider than Japanese), のりかえ secondary menu, keyboard and mouse operation.
- The Chinese and English catalogs are supplemented with 15 texts, and 4 `intermission_*` tags in each of the three languages.
- Check: `make recomp-intermission-test` (two menu judgments, input filtering, ASan/UBSan) passed; `tests/test_intermission_page.py` (hook wiring, labels, panel rectangle/scene table/background table in ROM) passed; the modified C++ file was only syntax checked using the host's compilation parameters.

Actual machine verification (2026-09-21, `intermission-cold-1` first episode archive, read the file through the title ring):

```sh
.venv/bin/python tools/recomp/debug/check_intermission.py            # 构建并检查
.venv/bin/python tools/recomp/debug/check_intermission.py --reuse-build
```

Running `build/recomp/debug/20260921T140756.835850Z/`: `intermission-checks.json` 12 items passed, exit code 0.

| Check | Results |
| --- | --- |
| Data | Round 7, Funds 14500, Episode 1, Scene 1, Nine-item, non-two-item menu |
| Cursor | ↑ Wrap from the first item to the last item, ↓ Wrap back; the sound effect is the original 0xB9 |
| のりかえ | Z opens the secondary menu; select the goblin (there is no goblin in the first episode). The original beeps, the page remains in the secondary menu and prompts; X closes |
| Sub-screen | Click "ユニット Transformation" to enter the original transformation screen. After B returns, the page reappears (serial is added), and the cursor stops at the original item |
| リンク | Leave it to the native linkage page, and the cursor will stop at リンク after Esc returns |
| Language | After switching to Chinese and English, the menu text will be updated immediately; English menu items will automatically be reduced to a small font size |
| 时のマップへ | Exit code 2, close the page, enter and return, and then enter the next dialogue |

In addition, I saw the 800×600 window (English) in the first manual session, and the four panels and text were all within the range.

**Not yet verified**:

- There are no ready-made archives for the two menus (after the "(Previous)" scene), only component test coverage determination; the two layouts of the page have not been seen on the actual machine.
- RNG control (section 8, item 9) did not run. The build hook is adjusted once to `80085B94(0,1)` as it is. The function of each frame is the original function itself, which should be consistent according to the structure, but this is not an actual test.
- The soft reset key combination has only been released through component testing and has not been pressed on a real machine.
- The release gate control of pressing the confirmation key follows the mechanism of other pages and has not been tested separately.
- The visual parameters (background color `#0a0e3c` 78%, edge color `#3a78e0`, highlight `#00c800`) are determined based on the original screenshot, and the color is not taken from the original image resources.

Original step-by-step (1–4 completed):

1. Adapter `intermission_page.{hpp,cpp}` + two hooks + input filtering, first publish a snapshot, and only draw non-interactive static panels on the page. Make sure that the original panel disappears and the background and fade-in are normal.
2. Interaction: move, confirm, mouse; secondary menu; release gate; soft reset release.
3. Localized entries and `ui` tag; three-language typesetting.
4. Debug interface fields (`status.intermission_page`, stable ID `intermission:0..8`, `intermission-swap:0|1`, wait condition `intermission_page`, event log `intermission`) and check script [`check_intermission.py`](../../tools/recomp/debug/check_intermission.py).
5. Verification, this article is rewritten into an implementation document.

Subsequent pages: ユニット transformation/weapon transformation ([Transformation screen takeover](native-upgrade-screens.md)), strengthened パーツ ([strengthened パーツScreen takeover](native-parts-screens.md)), ユニット ability/パイロット ability ([Ability view screen takeover](native-ability-screens.md)), のりかえ ([のりかえ screen takeover](native-swap-screens.md)) and The データセーブ([データセーブ screen takeover](native-save-screens.md)) has been taken over; the リンク page (`link_page.cpp`) has also returned the original linkage screen with the same settings. All inter-field scenes can now be switched between the original version and the native version.

## 10. Open issues

- The purpose of screen 22 is not read (the リンク item is entered when `801D93C4` is non-0, it is presumed to be a prompt screen).
- The panel border is drawn by `80098158` using the image `0x499/0x50F/0x511`. The exact color and line width should be taken from the exported original image, not estimated from the screenshot.