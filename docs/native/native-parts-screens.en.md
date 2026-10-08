> **Language / Ngôn ngữ:** [English](native-parts-screens.en.md) · [Tiếng Việt](native-parts-screens.vi.md) · [中文](native-parts-screens.md)

# Strengthen パーツ screen: unit list, slots and inventory, holder's native takeover

Date: 2026-09-23. Item 7 of the Intersession Menu. The three original screens (screen numbers 7, 18, and 19) are taken over by the RmlUi page and the original composition is maintained; equipment, disassembly, and taking parts from other aircraft are all injected into the A edge and handed over to the original function for completion. The aircraft record and inventory record are not directly rewritten by the page. The original screen can be selected back in the "Inter-session screen" on the settings page, see [Inter-session main menu](native-intermission-menu.md).

## 1. Original screen (static analysis)

The coordinates are all 320×240. The disassembly takes the instruction comment (`build/recomp/cpu-bound/generated/`) from the recompilation output.

### Unit list (Screen 7)

| Project | Basis |
| --- | --- |
| Layout 0x70: a panel (21,21)–(299,219); fixed tags strengthened パーツ (120,24), equipment in the のパーツ (24,184) | Resident layout table `D_800C8BB8` (each item is 24 bytes, the second word points to the {text number, x, y} list, 0xFFFF end) |
| Initialization `801D4A00`: `80085B94(0,1)` darkens the background (including random number calls), builds the layout, `801CB540` (`801C5D3C` generates a list and bubble sorts it in descending order by driver level `+0x5`, and then counts the number of pages), `801CB5A0` draws the list, `801CB910` Draw details and write the selected body into `D_801DEC5C`, cursor sprite slot 0x14 (21,48) 278×16, fade in | `801D4A00` |
| List array `D_801DD210` (u16 body slot number, quantity `D_801DD0A0`), **8 lines per page**, page number `D_801DD14A` starting from 1, lines `D_801DEBC8` (copy `D_801DD53A`); page number `D_801DDA04`, last page line number `D_801DDA2E` | `801CB540`, `801CB5A0` |
| Each line y=48+16n: body name (0x20F+body number) x=24, pilot name (0x111E+driver number) x=152 or `--------`, RIL (0xFE1) x=248, level `%2d` x=280; page number `%2d/%2d` (24,24) | `801CB5A0` |
| Details: Select the component name (0x469+part number) or `--------` of each slot of the body, and the location table `D_801DC6C4`: (112,184) (209,184) (112,202) (209,202) | `801CB910` |
| Each frame `801D4A98`: A → sound effect 0xB7, `D_801DEC58=0`, next picture 18, transition; B → 0xB8, next picture 0. The direction keys are `801C4A20` (up and down, 8 lines per page or the number of lines on the last page), `801CDA88` (turn the page left and right, lower the cursor when the number of lines on the last page is insufficient), `801CDC24` (redraw details); write zero when there is no key | `801D4A98` |

### Slots and Inventory (Screen 18)

| Project | Basis |
| --- | --- |
| Layout 0x7E: Panel (21,21)–(299,219), internally divided into upper left (page number + enhanced selection), middle left (slot list), lower left (six abilities), upper right (body name), middle right (inventory list), lower right (part description); fixed tags 0xFF0 (40,24), 0x1016 (72,24), HP/EN/Mobility/Mobility/Armor/Limit (0xFE7, 0xFE8, 0x1024, 0xFE9, 0xFEA, 0xFEB) x=24 y=120+16n, each row ▶ (0x101E) x=104 | Layout table |
| Initialization `801D4BEC`: background, layout, inventory page `D_801DD63C=1`, `801CBA78` Generate inventory list, `D_801DECCA=0`, mode `D_801DECD8=0`, `801CBFAC` draw the entire screen, slot cursor sprite 0x14 (21,45) 144×17, fade in, `D_801DEC50=0` | `801D4BEC` |
| Inventory list `D_801DD3A8` (u16): The first item 0x12 means はずす, followed by the part number (0...17) of each ** holding number > 0**; 6 rows per page, page number `D_801DECF0`, last page row number `D_801DD542`, row `D_801DD0A2` | `801CBA78`, `801CBB18` |
| Inventory display: page number (24,24); page 1, line 0 はずす (0x1017) (168,64); remaining lines y=64+16n: part name x=176, number of equipment `%d` x=268, number of possessions `(%d)` x=276; page turning arrow 0x1041 (168,48)／0x1042 (288,48) | `801CBB18` |
| Inventory record `D_8015E990`: one u16 for each part, high byte holding number, low byte equipment number | `801CBB18`, `801D4C94` |
| Body: `+0x21` Number of slots, `+0x22` Number of equipped, `+0x23…+0x26` Part number of each slot (s8, −1 is empty) | `801CBFAC`, `801D4C94` |
| Ability column: `800A5254(机体,2)` After recalculation, `801C4DE4` will contain the displayed values of the components (HP `D_801DEB08`, mobility `D_801DD14C`, mobility `D_801DD14E`, armor `D_801DEB06`, limit `D_801DEB04`, EN direct reading `+0x08`). **The left column "now" = the displayed value minus the bonus of the part on the cursor slot**, the right column "Preview" adds the bonus of the part under the cursor in the inventory in mode 1 (はずす does not add); the preview is green above the current value and red below the current value | `801CBFAC` |
| Part Bonus Table `D_801DC578`: 7 u16 per piece - HP, Mobility, Movement, Armor, Limits, Two Flags. 18 pieces; No. 7 is a component with strength +5 (`801D4BB4` changes to driver `+0x20` when loading and unloading), No. 9 and 10 only have logos | ROM data |
| Description table `D_801DC97C`: Each item {text base address, line number}, text number 0x10AF＋base address＋n, drawn at (168,168+16n) | `801D4C94` |
| Per frame `801D4C94`: Mode 0: B → next screen 7; A → build inventory cursor sprite 0x15 (166,64) 132×16, row 0, mode 1. Mode 1: B → Release the sprite and description text, mode 0; A → Page 1, line 0 (はずす): If the slot is empty, just re-enter the screen, otherwise `+0x22` minus 1, the number of inventory equipment minus 1, No. 7 part restores strength, slot write −1, `800A5924(机体,1)` spread, re-enter the screen 18; Other lines: `D_801DD63E=槽位光标`, `D_801DEC58=0`, next screen 19. Then move the cursor according to the mode (number of slots or number of lines per page), turn the page (`801CDC94`), write the parts under the inventory cursor into `D_801DECCA`, and redraw the instructions | `801D4C94` |

### Owner List (Screen 19)

| Project | Basis |
| --- | --- |
| Layout 0x7F: Panel (21,21)–(299,219), label Equipped のパーツ (24,24); local slot component name position table `D_801DC6CC`: (112,24) (209,24) (112,42) (209,42) | Layout table, `801CCA80` |
| Initialization `801D5168`: background, layout, `801CC988` generate holder table `D_801DCF10` (one item for each held copy: the slot number of the machine that holds it, or 0xFFF means not equipped), `801CCA80` drawing list, cursor sprite 0x14 (21,63) 278×17, fade in | `801D5168`, `801CC988` |
| Each row y=64+17n: component name x=24; with holder: body name x=120, pilot name x=232; not equipped: `------------` x=120, `--------` x=232 | `801CCA80` |
| Each frame `801D51EC`: B → Return to screen 18. A: The selected copy is not equipped → If the target slot is empty, add 1 to `+0x22` and add 1 to the equipment number, otherwise replace (remove the original parts and restore strength to No. 7); the copy is on another body → remove it from that body (`+0x22` minus 1, write −1, `800A5924`) and then install it to this machine. If the machine is the same and has the same slot, it is the same as removing it. Finally `800A5924(本机,1)`, `D_801DEC58=0`, return to screen 18 | `801D51EC` |

## 2. Takeover method

Source code: [`parts_page.cpp`](../../src/host/parts_page.cpp) (game thread adapter), [`frontend.cpp`](../../src/native/ui/frontend.cpp)’s `parts_sync` (page), [`game_hooks.cpp`](../../src/host/game_hooks.cpp) packaging (`parts_build`/`parts_step`/`parts_frame`, the six hooks are in `generate_cpu.py` and `NATIVE_HOOKS`, the CPU code must be regenerated after modification). When the original version is selected in the "Inter-field screen" of the settings page, all three construction entrances are returned to the original screen; `SRW64_NATIVE_PARTS=0` or when profile is not loaded, the original screen is retained throughout the run.

| original function | wrapper |
| --- | --- |
| `801D4A00` List initialization | Do not adjust the original function. Keep background calls (including random numbers), `801CB540` (sorting, page number), row copies, and write `D_801DEC5C` to the selected machine; do not build layout, text, or cursor sprites. Fade in after posting snapshot |
| `801D4A98` list per frame | Move/turn page: The adapter writes page, line, copy and `D_801DEC5C`, plays 0xB9 (8 lines per page, the last page lowers the cursor to be consistent with the original). Confirm/Return: Inject A/B edge reshaping function |
| `801D4BEC` Slot initialization | Do not adjust the original function. Keep the background, inventory page 1, `801CBA78`, mode 0, clear the count; write the initial value of `D_801DECCA` as 0x12 (write 0 in the original version, which will make the preview without moving have the bonus of part 0 - the page will be displayed unchanged according to the はずす under the cursor) |
| `801D4C94` slot per frame | Mode 0: mobile write `D_801DEC58`; confirm that the adapter switches to mode 1 (the original A branch only builds cursor sprites, line clearing and counting, no sprites are built here); return to injection B. Mode 1: Move/turn pages to write `D_801DD0A2`/`D_801DD63C` and write the component under the cursor into `D_801DECCA`; cancel the switch back to mode 0 by the adapter (the sprites and text released by the original B branch have never been built here); confirm the injection of A, complete the unloading or enter the screen from the original version 19 |
| `801D5168` holder initialization | Do not adjust the original function. Preserve background with `801CC988` |
| `801D51EC` holder per frame | Move write `D_801DEC58`; confirm/return inject A/B |

**Snapshot**: `status.parts_page`: `screen` (`list`/`slots`/`holders`), `serial`, `labels`; the list has `page` (0 (from), `pages`, `cursor`, `rows[]` (`slot`, `number`, `name`, `pilot`, `level`, `parts[]{part,name}`, `en`); the slot screen has `unit` (same as above), `cursor` (slot), `mode` (0 slot/1 Inventory), `stats[]{key,current,preview}`, `selected` (part number under the inventory cursor, 0x12＝はずす), `description[]`, `inventory{page,pages,cursor,rows[]{part,name,remove,equipped,owned}}`; the holder screen has `unit`, `part{part,name}`, `target_slot`, `cursor`, `rows[]{free,slot,name,pilot}`. Event log `parts-page-events.jsonl`.

**Page**: The three-block layout is based on the rectangle above; each row of the list is 16, the slot row is 17, the inventory row is 16, and the holder row is 17; the preview column is green above the current value and red below (the original version uses two text colors).

**Debug**: Stable ID `parts:N` (current list row: body list/inventory/holder; click the cursor line to confirm, click other lines to move), `parts-slot:N` (slot line; click to return to the slot first when the inventory is opened); keyboard ↑↓, ←→ (page turning), Enter/Z, Esc/X; waiting condition `parts_page`.

## 3. Real machine verification (2026-09-23)

```sh
.venv/bin/python tools/recomp/debug/check_parts.py            # 构建并检查
.venv/bin/python tools/recomp/debug/check_parts.py --reuse-build
```

`intermission-cold-1` Chapter 1 completed save (without any parts). Running `build/recomp/debug/20260923T031518.017920Z/`: `parts-checks.json` 14 items passed, exit code 0.

| Check | Results |
| --- | --- |
| List | ダイターン3（万 Zhang Lv5）, ドール（シモーヌ Lv3）, スイームルグ（マナミ Lv2）, in descending order by driver level; 1/1 page; ↑↓ first and last loop; tags Strengthened パーツ／Equipment のパーツ／レベル Taken from the original text |
| Slot screen | ダイターン3 Two empty slots; Current value of six abilities = preview (HP 8000, EN 200, mobility 5, mobility 70, armor 1800, limit 270); inventory first row はずす, cursor 0, page 1 |
| Slot cursor | ↓ to second slot, ↑ back |
| Inventory | Z opens (mode 1, `selected` = 0x12, no description); X closes back to mode 0 |
| はずす Anti-empty slot | Z Z After the original version re-enters the screen (serial increases), the slot is still empty |
| Return |

In the first version, the keyboard does not respond but the mouse can click: In the keyboard distribution of `frontend.cpp`, there are two guards that click "Which pages are open" to release, not counting new pages, which have been added. The first version inventory cursor reads 0xFFFF: the original version only clears `D_801DD0A2` when entering mode 1, and writes 0 to the page itself when building.

## 4. Not verified

- Equipment, replacement, and taking from other aircraft: There are no parts in the archive of the first episode, and you can only check the re-entry screen of the empty slot by はずす; the script `check_parts.py` will continue to check the equipment and holder screen when there are parts in the inventory, and a save with parts is required.
- Page turning of multi-page lists (more than 8 units, more than 7 parts).
- The power changes of part 7 and the logo effects of part 9/10 are only processed by the original version and will not be displayed on the page.