> **Language / Ngôn ngữ:** [English](native-title-menus.en.md) · [Tiếng Việt](native-title-menus.vi.md) · [中文](native-title-menus.md)

# Title menu screen: native takeover of ロード, オプション, サウンドセレクト, カラオケモード

Date: 2026-09-24. The screen after the four items in the title menu.ロード reuses [データセーブ page](native-save-screens.md) and changes it to the read copy and process; オプション and the two track lists are new pages ([`title_page.cpp`](../../src/host/title_page.cpp)). The page is only responsible for drawing, and the original state function continues to manage unlocking, scrolling, playing songs, and switching overlays. The selection of the page is handed over to them in the form of button presses. You can choose to return to the original screen in the "Title Menu Screen" of the settings page. The names of the four items on the ring menu are shown in [Title Screen and Plot Text Image](native-title-and-story-images.md).

## 1. Original screen (static analysis)

The header overlay is `load_0010DA50` (RAM `801C4500`, ROM `0x10DA50`, BSS starting from `0x801CC150`, not cleared on reload). Each frame task `801CA9CC` first looks at the fade-in and fade-out state `80099B30()`: only when it is not 0 or 2, press the main state `D_801CC3A6` to look up the table `D_801CB250` to adjust the state function, and the sub-state is `D_801CC3A7`. The coordinates are all 320×240.

### Ring menu and where to go

| Project | Basis |
| --- | --- |
| Cursor `D_801CC3AC`: 0 スタート, 1 オプション, 2 コンティニュー, 3 ロード. Hold down the right cursor +1, left cursor -1. After pressing A or START, the main state = cursor + 4, the original sound effect will not be played here, and will be played on the next screen | `801C6514`, `801C642C` |
| The item names are just sprites (scenes 652–655). There are no such strings in the text table, so an additional `title_start/load/continue/option` is added to the `ui` tag | scene table |
| Return to the ring menu to unify the main state 7 Sub-state 0xC `801C7BE0`: Redraw the logo and flame, rebuild the ring according to the current cursor, BGM 0x1E; Sub-state 0xD `801C7C48` Return to the main state 3 after the fade-in is completed | `801C7BE0` |
| **コンティニュー (main state 6) has no picture**: `8009365C` reads SRAM `0x3E10` and starts 0x3AE0 bytes of interrupt data; if it is invalid, it will broadcast the buzzer 0xBA and stay on the ring, if it is valid, it will switch mode 0x11 and return directly to the tactical map | `801C6D1C` |
| **キャラクターリスト (main state 9), ロボットリスト (main state 10) are not reachable**: initialization `801C8F1C`, `801C96FC` There is no caller in the entire ROM, and there is no code to write the main state as 9 or 10. It will not appear after clearing the level | Full ROM reference scan |

### オプション (main state 5)

| Project | Basis |
| --- | --- |
| Build `801C697C`: Free slots 2–6 (ring) and 9 (flame); layout 0x5A to slot 0x2E, title box (133,21)–(187,43) draw オプション(0xE1), item box (109,84)–(213,139) drawサウンド(0x3EF), サウンドセレクト(0xE2), カラオケモード(0xE5), value labelステレオ(0x3F0)/モノラル(0x3F1) is drawn at (176,90). Cursor slot 0x27 is at (110,87+16n). 3 items in total, no hidden items | `801C697C` |
| Each frame `801C6B14`: Up and down keys cycle the cursor `D_801CC397`. A is in item 0: `D_8015DDA8=(D_8015DDA8^1)&0xFB`, `8009187C` immediately writes back the 7th byte of the SRAM header, `80076D90(bit0)` switches the audio channel. A in items 1 and 2: The same frame calls `801C86A8`/`801C9888` to create a list. B: Fade out, return to the circular menu | `801C6B14` |
| Setting byte `D_8015DDA8`: bit0 is mono, bit2 is a temporary bit of the tactical map (it will be cleared every time the setting is written), bit3 has been cleared (the ending is set) | `8009171C`, `8009187C` |

### サウンドセレクト (main state 8) and カラオケモード (main state 11)

| Project | Basis |
| --- | --- |
| Build `801C86A8`/`801C9888`: `801C4850` clean, stop BGM; layout 0x5B/0x61 draw full screen frame (21,21)–(299,219), title (80,25), EXIT (0xE6) (248,25); `801C81C0(0／1)` Create a list, `801C83D0` draws 10 lines (x=80, y=52+16r); arrow layout 0x5C in slot 0x2F | `801C86A8`, `801C9888` |
| List variable: `D_801CC190` The number of items, `D_801CC192` The current item, `D_801CC194` The line number in the window (0–9), `D_801CC196` The first item in the window, `D_801CC198[]` is the table subscript | `801C81C0` |
| Each item in the music list is {text number, music number}: サウンドセレクト uses `D_801CB290` (49 items, text 0xE8–0x118), and カラオケモード uses `D_801CB354` (19 items). The song number currently being played is in `D_800FFA6C` | data segment |
| Unlocking conditions: F91 ガンダム出撃, 行けザンボット3, ゴーショーグン発进せよ requires seeing the corresponding machine (`80091670`, illustration bit `D_8010F520`); The Green Land requires `D_8015DDA8 & 8`, which is to pass the level.カラオケ's ザンボット3, ゴーショーグン two songs are the same | `801C81C0` |
| Each frame of the list `801C8724`/`801C9904`: up and down (read consecutive words `D_801612E0`) move and scroll through `801C8520`. Pressing on the first item will move the focus to EXIT (substate 1, `801C89E4`/`801C9ADC`).サウンドセレクト: A plays the song (replays it from the beginning when playing the same song), B only stops the song when playing the song, and returns to オプション when it is not playing, Z/L (0x2020) and R (0x10) move up or down one song and play it immediately.カラオケモード: A writes `D_80172D08=曲号`, switches to mode 0x1A, enters combat and overlays the demonstration battle and lyrics; after the end, return to title entrance 1 in mode 0x1B, move the cursor to the song just now | `801C8724`, `801C9904` |

### ロード (main state 7)

The screen composition and archive header format are the same as those of データセーブ in the field. The difference lies in the text and process:

| Substate | Function | Effect |
| --- | --- | --- |
| 3 | `801C709C` (Build `801C6F3C`) | Media selection. Medium `D_801CC359`; message is からロードします. (0x1E3). A: Pak `D_801CC37C=80094168(1)`, then open the "データを动べています." window, `D_801CC368=0`, enter 4; B: Loopback |
| 4, 5 | `801C71C0`, `801C777C` | Check for stalls (ROM 7 frames), fade out. When Pak and the status is not 0, call `801C7C90(状态)` into 0xE, otherwise call `801C7328` to create the archive column |
| 7 | `801C783C` (builds `801C7328`) | Archive bar. `80085CD4(介质, 0x801CC158)` Read two columns of archive header, cursor `D_801CC358`. A In the empty column: buzzer; in the column with data: on. Record を読み込みます. (0x1E4)／よろしいですか? Confirmation window, `D_801CC150=0`, enter 0xA. `8009412C` detects whether to pull out every frame when Pak |
| 0xA | `801C7A48` | Confirmation window.はい: `80080188(ROM 0x12+栏，Pak 0x14+栏)` and then fade out. The actual file reading is done in `801D8F74` of the inter-field overlay, and then enters the main menu of the inter-field.いいえ or B: back to 7 |
| 0xE |

## 2. Takeover method

Source code: [`title_page.cpp`](../../src/host/title_page.cpp) (game thread adapter for オプション and track list), [`save_page.cpp`](../../src/host/save_page.cpp) `title_*` (ロード), [`frontend.cpp`](../../src/native/ui/frontend.cpp)'s `title_sync` (オプション and track list page; ロード is still made by `save_sync``SRW64_TITLE_BUILD`/`SRW64_TITLE_STEP` package of [`game_hooks.cpp`](../../src/host/game_hooks.cpp). 16 functions were renamed to `srw64_original_title_*` in `NATIVE_HOOKS` of `generate_cpu.py`. After the change, `generate_cpu` must be rerun.

| original function | wrapper |
| --- | --- |
| `801C697C` オプション Construction | Do not adjust the original function. Free slots 2–6 and 9 only, then open page |
| `801C6B14` オプション per frame | Mobile: written by adapter `D_801CC397` and broadcast 0xB9.サウンド: The adapter completes the switching by itself, `8009187C`, `80076D90` (the original branch will draw words into the tag slot that may have expired). A and B of other items: call the original function by pressing a key, and let it call the hooked list construction, or fade out the loop |
| `801C86A8`／`801C9888` List construction | Do not adjust the original function. Do `801C4850`, `8007E810(-1)`, `801C81C0(0／1)`, then open page |
| `801C8724`, `801C89E4`, `801C9904`, `801C9ADC` List each frame | The original function is adjusted for each frame (it needs to track whether the song is playing, B's behavior depends on this). Use the keys to write continuous words up and down, A, B, Z, R are written into the current frame and the word is pressed; when a certain line is clicked, the list variable is changed by the adapter; after the adjustment is completed, the arrow of the slot 0x2F is released |
| `801C83D0` Draw list | Change to no operation and resend page status. It will also be called during カラオケ return and fade-in, and the page will follow the cursor here |
| `801C6F3C`, `801C709C`, `801C7328`, `801C783C`, `801C7A48`, `801C7C90`, `801C8074` ロード | Press [データセーブ](native-save-screens.md) approach: The construction function does not adjust the original function, and the archive header reading, media switching, confirmation window and Pak prompt are processed by the adapter according to the original state machine. B. はい in the confirmation window and A/B on the prompt page. After writing the variables, press the button to call the original function, and the original function will fade out or switch modes |
| `801CA9CC` Task per frame | Check the main state after the original function is finished: close the page when it is not in the corresponding main state or has reached the sub-state 0xD |

**overlay switching**: カラオケ play, ロード confirmation, コンティニュー will let other overlays be installed to `801C4500`. `overlay_loaded` As long as the newly loaded range overlaps with `801C4500–801CC150`, the page will be closed as a frame, and the BSS of the title overlay will no longer be read.

**Original/New version**: Setting page "Title Menu Screen" (`title_ui` of `presentation.json`, debugging interface `settings {"title_ui": "original"}`). It will take effect the next time the screen is opened, covering ロード, オプション, サウンドセレクト, and カラオケモード.

**Page**: According to the original position of the frame, title, EXIT, 10-line song name and up and down arrows; add ▶ before the song name of the song being played, and change the text to light blue when it is not in the cursor line.

**Text**: The title, project, and song title are all fetched from the text table through `dialogue::ui_text`, following the reading language; ロード replace the two sentences with 0x1E3 and 0x1E4 in the title environment. The song name (text 0xE8–0x118) is currently not in the data entry table, so the original Japanese name is still displayed in the Chinese and English interfaces.

**Snapshot**: `status.title_page` fields are as follows, and events are written in `title-page-events.jsonl`.

- Common: `screen` (`options`/`sound`/`karaoke`), `serial`, `title`.
- オプション: `items[]` (`label`, and optionally `value`), `cursor`, `mono`.
- Tracklist: `songs[]` (`text`, `song`, `playing`), `current`, `top`, `rows`, `exit`, `exit_focus`.
- ロード: Use `status.save_page`, plus `context` (`title` or `intermission`).

**Debug**: Stable IDs are `tp-option:N`, `tp-song:N`, `tp-exit`; keyboard ↑↓, Q/E (previous/next song), Enter/Z, Esc/X.

## 3. Real machine verification

```sh
.venv/bin/python tools/recomp/debug/check_title_menus.py              # 中文界面，含 カラオケ
.venv/bin/python tools/recomp/debug/check_title_menus.py --skip-karaoke
```

Archive `intermission-cold-1.source.sram` (cleared the first episode). Running `build/recomp/debug/20260924T070500.307818Z/`: `title-checks.json` All 18 items passed. After changing the button padding and "now playing" mark of the track list, I ran it again with `--skip-karaoke` (`build/recomp/debug/20260924T071216.285758Z/`), and all 16 items passed. The Chinese interface removed the space between the media name and the sentence and ran it again (`build/recomp/debug/20260924T071435.026778Z/`), and all 16 items still passed.

| Check | Results |
| --- | --- |
| オプション | Three items: sound/music appreciation/karaoke mode, cursor 0; click sound to switch to mono and then switch back to stereo, `mono` synchronized changes |
| サウンドセレクト | 49 songs that have been unlocked are listed, and there are no songs playing when you first enter; ↓3 After Z plays FLYING THE SKY, Q plays the previous song サイレント・ヴォイス; ↓12 After the window scrolls to the first item 5; Esc Stop the song, then Esc to return to オプション and the cursor is at 1 |
| カラオケモード | There are at least 15 songs in the list; select the 2nd song to start, enter the カラオケ battle, press X after about 12 seconds, and the cursor is still on the 2nd song when you return to the list |
| Original switch | Switch `title_ui=original` to backward オプション is the original sprite screen, there is no native page; X loops, and then switches back to the new version |
| ロード | Media selection `context=title`; after entering the archive column, column 1 is empty, and column 2 is empty; press Z in the empty column to be rejected (the mode is still 0); column 1 opens a confirmation window, and the text is Read archive records. /Are you sure? ; Yes → Enter the main menu between games, 7 rounds, capital 14500 |

## 4. Unverified and restricted

- The file loading and repair branches of コントローラパック only have static analysis: the host does not have Pak, and the Pak path is stable at status 7.
- There are no special archives to verify the unlocks of those who have cleared the game (Green Earth's Upper Land) and have seen specific aircraft; the page only displays the list created by `801C81C0`.
- The song title is not available in Chinese or English yet, you have to wait for the data entry table to include the text 0xE8–0x118.
- The option box of the original confirmation window: `native-save-screens.md` is written as (221,122)–(251,163), and the layout table is the main window (53,101)–(267,139) and then continues down to (221,139)–(251,163). The original page is drawn according to the former in both places, and has not been compared with the original screenshot.