> **Language / Ngôn ngữ:** [English](native-save-screens.en.md) · [Tiếng Việt](native-save-screens.vi.md) · [中文](native-save-screens.md)

# データセーブ Screen: Native takeover of media selection and archive bar

Date: 2026-09-23. Interplay menu item 1. The two original screens (screen numbers 1 and 9) are taken over by the RmlUi page and keep the original composition; the page runs its own state machine and only calls the original archive header reading and SRAM/コントローラパック writing routines. The original screen can be selected back in the "Inter-session screen" on the settings page, see [Inter-session main menu](native-intermission-menu.md). The ロード of the title screen reuses the same page (`context` is `title`), see [Title Menu Screen](native-title-menus.md).

## 1. Original screen (static analysis)

The coordinates are all 320×240. The disassembly takes the instruction comments from the recompilation output; the layout table `D_800C8BB8` is 24 bytes per item, the second word is the `{文本号,x,y,0}` label table, and the third word is the filled rectangular display list (`G_FILLRECT`, 10 bits for each coordinate).

### Media Selection (Screen 1)

| Project | Basis |
| --- | --- |
| Layout 0x6A: option box (117,61)–(203,99), label ROMカートリッジ (0xFD9) (124,63), コントローラパック (0xFDA) (124,83); message box (85,125)–(235,147), tag にセーブします. (0xFDC)(169,128) | Layout table |
| Initialization `801CEA30`: `80085B94(0,1)` dark background (including random numbers), layout, `801C6620` draw the cursor medium name in (90／88,128) and record the text slot `D_801DD0B0`; cursor sprite 0x14 (87,61) 116×20 binding `D_801DEBC8` (medium: 0 ROM, 1 Pak); fade in; `D_801DDA30=0`, `D_801DECD8=0` | `801CEA30` |
| Each frame `801CEABC`: When no message is played, B → sound 0xB8, fade out, next picture 0; A → sound 0xB7, window layout 0x72 (frame (101,109)–(219,131), label (0xFDD) (112,112)), `D_801DDA30=1`, `D_801DECD8=30`; countdown when the message is popped, to 0 → `D_801DD0A2=0` (archive column cursor), next screen 9, fade out. When no message is played, run the cursor `801C4A20` every frame and redraw the media name `801C6680` when pressing the up and down keys (`D_801DD62C & 0xC00`) | `801CEABC` |

### Archive Column (Screen 9)

| Project | Basis |
| --- | --- |
| Layout 0x73: title box (117,21)–(203,43); two columns (21,69)–(299,139), (21,149)–(299,219), label セーブデータ (0xFDE) (90,72), (90,152); avatar frame (21,y)–(87,y+70) is placed by the sprite of `801C6260` | layout table, screenshot |
| Initialization `801CECE8`: background, layout; media name (0xFD9/0xFDA) (122,26); Pak first `80094168(0)` → `D_801DD116`, ≥2 then `801CE578` prompt, `D_801DECD8=2`; otherwise `80085CD4(介质, D_801DD118)` Read two columns of archive header; Column number `"1"`/`"2"` (140,72/152); `801C66B8` Draw used columns; Cursor sprite 0x14 (89,69/149) 209×19 Binding `D_801DD0A2`; `D_801DECD8=0`; Fade in | `801CECE8` |
| Archive header record `D_801DD118`, each column 0x18: `+0` used; `+2` six name glyph codes (`0x801C2698`, the same code as the name input page, empty space 0x1549); `+0xE` protagonist category 0–3 (0x19–0x1C in the archive body table) one); `+0xF` level; `+0x10` number of words (`0x801C264F`); `+0x11` chapter title number (`0x801C2651`, text `0x119+`); `+0x12` total rounds (u16, `0x801C264C`); `+0x14` funds (u32, `0x801C2654`). ROM read head `80092744(栏)`, Pak read head `80093F4C(栏)` | `80085CD4` |
| Used column `801C66B8` (y=69＋80n): avatar `801C6260(n, 类别, 21, y)`, resource `D_801DC680[类别]`=picture `0x51C+类别`, palette `0x520+类别`; name `801D920C` (160,y+3);レベル(0xFE1)(248), level `%2d` (280); No. (0xFD7)(90,y+20), number of words `%2d` (104); title `0x119+号` (89,y+37), followed byクリア (0xFE0); 総ターンnumber (0x101B) (90,y+54), `%3d` (146); Funds (0x1019) (192), `%8d` (232) | `801C66B8` |
| Each frame `801CEEF8`, mode `D_801DECD8`: **0** B → sound 0xB8, fade out, next picture 1; A → sound 0xB7, if the field is empty, write (ROM `80092678(栏)`; Pak first `80094168` then `80093FD4(栏)`), `D_801DD116==0` Then fade out, next screen 9 (re-enter), otherwise `801CEC00` clears the elf text, `801CE578` pops up the prompt, mode 2; if the column is used, open the window layout 0x74 (frame (53,101)–(267,139), record をUpdateします (0xFE3) (56,104), よろしいですか? (0xFE4) (56,120), はい／いいえ. (224,128)/(224,148), option box (221,122)–(251,163)), cursor 0x15 bound `D_801DDA08`, mode 1. **1** B or A in いいえ → Close window, mode 0; A in はい → Same as writing. **2** Each frame `800906A0`; B → fade out, next picture 1; A → `80090844(0x8015F508,0)` fixed when state 7, otherwise `80094168(0)` recheck, <2 or state changes, fade out and re-enter picture 9. When mode <2 and the medium is Pak, each frame `8009412C`, non-0 (Pak pulled out) → State 2, mode 2 pop-up prompt | `801CEEF8` |
| Tips `801CE578`: Window layout 0x8C (frame (29,77)–(291,179)), press `D_801DD116` to place text: 2/3 → 0x1A8 (80,86), 0x1AA (80,106), 0x1AE (104,126), 0x1AF (72,156); 4 → 0x1BC, 0x1BD, 0x1BE, 0x1BF, 0x1AF; 5 → 0x1B7, 0x1BA, 0x1BB, 0x1AF; 6 → 0x1B3, 0x1B4, 0x1C0, 0x1AE, 0x1B0; 7 → 0x1A9, 0x1B8, 0x1B9, 0x1B2, 0x1B5, 0x1B6, 0x1AF | `801CE578` |

The host does not have コントローラパック: `80090778` (`osPfsIsPlug`) is taken over by `game_hooks.cpp` to "no Pak is inserted into the four controllers", and the Pak path stably enters state 7 (requires repair).

## 2. Takeover method

Source code: [`save_page.cpp`](../../src/host/save_page.cpp) (game thread adapter), [`frontend.cpp`](../../src/native/ui/frontend.cpp)’s `save_sync` (page), [`game_hooks.cpp`](../../src/host/game_hooks.cpp) packaging (`save_build`/`save_step`/`save_frame`, four hooks in `generate_cpu.py`'s `NATIVE_HOOKS`). When the original version is selected in the "Inter-field screen" of the settings page, both construction entrances will be returned to the original screen; `SRW64_NATIVE_SAVE=0` or when profile is not loaded, the original screen will be retained throughout the run.

| original function | wrapper |
| --- | --- |
| `801CEA30` Media selection initialization | Do not adjust the original function. Keep background calls (including random numbers), clear `D_801DDA30`, `D_801DECD8` |
| `801CEABC` media selection per frame | The cursor is written by the adapter `D_801DEBC8`; confirmation is set by the adapter `D_801DDA30=1`, `D_801DECD8=30` and displays データを动べています. , after that each frame returns the original function countdown and transition (nothing is drawn); return and inject B |
| `801CECE8` Archive column initialization | Do not adjust the original function. Keep background; `80094168` definite state when Pak, otherwise `80085CD4(介质, D_801DD118)` Read two columns |
| `801CEEF8` Each frame of the archive bar | Do not adjust the original function (the original A and Pak pull out the branch and draw the pop-up window yourself). The adapter follows the original state machine: write call `80092678`/`80094168`+`80093FD4`, successfully fade out and re-enter screen 9, fail to enter prompt mode; prompt mode every frame `800906A0`, A goes `80090844`/`80094168` recheck; mode <2 and Pak Time per frame `8009412C` |

**Snapshot**: `status.save_page`: `screen` (`choice`/`slots`), `serial`, __INL_ CODE_117__ (rom, pak, save_to, checking, slot, level, episode, clear, turns, funds, overwrite, ask, yes, no); media options are `cursor`, `waiting`; the archive column has `medium`, `cursor`, `mode` (0 list, 1 overwrite confirmation, 2 prompt), `window_cursor`, `status`, `slots[]` (`index`, `used`, `name`, __INL_CODE _129__, `level`, `episode`, `title`, `turns`, `funds`, `art`), prompt mode is additional `message[]` (`text`, `x`, `y`). event log `save-page-events.jsonl` (`open`, `choose`, `window-open`/`window-close`, __INL_COD E_145__, `recheck`, `pak-removed`, `back`, `close`/`left`).

**DEBUG**: Stable ID `save:N` (media or archive bar), `save-yes`/`save-no`; keyboard ↑↓, Enter/Z, Esc/X; wait condition `save_page`.

## 3. Real machine verification

```sh
.venv/bin/python tools/recomp/debug/check_save.py            # 构建、读第一话存档并检查
.venv/bin/python tools/recomp/debug/check_save.py --reuse-build
```

Archive `intermission-cold-1.source.sram` (Chapter 1 cleared, Column 1 Malina Level 2, Chapter 1 "Out! スイームルグ", 7 rounds, 14500). Running `build/recomp/debug/20260923T044601.424135Z/`: `save-checks.json` 19 items passed, exit code 0.

| Check | Results |
| --- | --- |
| Media selection | Cursor 0, ↓ to コントローラパック, Z then データを动べています. (`waiting`) Enter the archive bar in about half a second |
| Archive Column | Column 1 The name is decoded from the glyph code "Mama", and the avatar is face No. 28 (category 3) on the name input page; Column 2 is empty |
| Write in the blank column | ↓ Column 2, Z: `80092678(1)` and then the screen will re-enter, and the contents of column 2 and column 1 are consistent |
| Overwrite confirmation | Z opens the window on column 1, ↓ いいえ, Z closes the window; open the window again はい and re-enter after writing |
| Return to Pak |

Original version comparison (`build/recomp/debug/20260923T041741.927962Z/save-*.png`, `80090778` original picture after the hook takes effect): the composition is consistent; the original version in the prompt box splits the same line into two paragraphs of text (for example, 0x1B8+0x1B9), and the page is merged into one line by pressing y.

## 4. Extension column (2026-10-01)

For the design, see [Multi-Archive Column and Auto-Archive](../design/save-slots-autosave.md). The independent application passes the archive library (user directory `saves/`) to the host through `SRW64_SAVE_LIBRARY`; when not set (debugging session, `check_save.py`), there are only two columns, the behavior is the same as above.

- **Reroute**: [`save_store.cpp`](../../src/host/save_store.cpp) wraps `80090E5C` (`NATIVE_HOOKS` renames `srw64_original_sram_transfer`). During one operation, the page uses `save_store::Window` to map the game column 0/1 to the extension column. The read and write of the address `0x10`/`0x1F10` and the length 0x1F00 is changed to read and write `saves/slots/NNN.rec`. After writing and running `80092678` (serialization, writing, reading back and comparing) according to the original version, the file read back is the file just written.
- **Immediate Publish**: The rest of the writes fall to the cassette as usual, and a copy of the cassette in the host is updated at the same time; the copy is immediately published as `saves/cartridge.sram` when the file header and checksum are correct. `0x78F0` Shared blocks are not published when written individually, and are written together with subsequent columns. There is no file header during the formatting of the new game and it will not be published.
- **List**: After the two columns of the cassette, there is the existing expansion column, and the smallest empty number is added when archiving. The archive header of the extended column is mapped and read from the original `80085CD4` (two columns once). After reading, read the two columns of the cassette again, and the archive header table is restored to its original state. There are more page states: `count`, `page`, `pages`, `slots[]`. Only two columns are placed on the current page, with `number` (column number) and `index` (list position), `cursor` is the list position; the game's own cursor just writes 0/1.
- **Interface**: Keep the original two-column composition, two columns per page. ↑↓ Go through all columns, ←→ turn pages; the upper left mark of page 1 is "カートリッジ", and the upper right is the page number. Prompt to use `save_slots_hint_pages`/`title_load_hint_pages` instead.
- **Title Reading**: When selecting the extended column `save_store::arm_load(栏号)`, write the game cursor as 0, and then hand it to the original version for confirmation; after a few frames, overlay `80092C70(0)` between fields and read the column 0 to get this file, and release it after reading. Also released when returning to the title ring, reopening the column list, or the save screen between games.
- **Original screen**: When switching back to the original version in the settings, only two columns of the cassette are visible on the original screen, and the mapping does not take effect.
- **Event Log**: `save-store-events.jsonl` (`open`, `slot-write`, `slot-read`, `publish`, `arm`, `disarm`, `*-error`).

Real machine: `tools/recomp/debug/check_save_slots.py`, ran two rounds with a new archive library, and passed 14 items:

- First round: The list is column 1, 2 and empty column 3; after storing in column 3, `003.rec` (checksum pair) is generated, and the cassette file remains unchanged; ← returns to page 1; column 3 is overwritten and rewritten after confirmation; when the cassette column 2 is stored, the cassette is released immediately, and `.prev` is left.
- Second round: First change the fund of `003.rec` to 123456 and recalculate the checksum. Column 3 in the title reading list shows 123456. After reading the file, the fund in the inter-site menu is 123456. There is `slot-read` in column 3 in the log, and the cassette file remains unchanged.
- Screenshot: `build/recomp/save-slots-check/<时间>/`. `check_save.py` (16 entries) without archive library also passes as `check_title_menus.py --skip-karaoke` (16 entries).

Auto-archiving and deletion (2026-10-01): The title ロード list is listed in the auto-archive after the expansion column (`kind` is `intermission`/`turn`, with `time`; the archived round's title, round, fund, name are from the record +0x26C progress block reading, no level and avatar); the page status has more `tools` (can the item under the cursor be deleted) and mode 3 (deletion confirmation). Press R to delete and prompt to use `save_slots_hint_delete`/`title_load_hint_delete` instead. There is no column note function. For practices and verification, see [Design Document](../design/save-slots-autosave.md) §8.

## 5. Not verified

- Only SRAM media is actually written; the コントローラパック path is always a prompt (status 7) because the host does not have Pak, and the writing and repair branches only have static analysis.
- The text prompts for states 2–6 are arranged according to disassembly coordinates, and there is no actual screenshot for comparison.