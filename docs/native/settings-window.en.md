> **Language / Ngôn ngữ:** [English](settings-window.en.md) · [Tiếng Việt](settings-window.vi.md) · [中文](settings-window.md)

# Settings window: From hotkeys and menus to "Options"

Date: 2026-09-18. **The first version has been implemented, see §6; on 2026-09-27, it was changed to a paging board superimposed in the game, see §7; the rest is still under planning. ** Currently, the things that players can adjust are scattered in hot keys (F6 image, F7 language), the "Rules" menu in the menu bar, startup parameters and profile files; there are already seven rules, and there will be more in the future, requiring a centralized entrance. This article stipulates the entrance structure, classification, effective timing and acceptance requirements for each item, and the specific implementation will be arranged separately.

## 1. Current status inventory

| Existing Entrance | Coverage | Questions |
| --- | --- | --- |
| F6 | Original / HD image | Only cycle switching, cannot see the current value and optional value |
| F7 | ja / zh-Hans / en loop | Same as above |
| Menu bar "Rules" | Two types of rules and presets, namely correction and difficulty adjustment, take effect in real time and are written back to `rules.json` (the entry during planning has been replaced by "Options" in §6) | Entries will grow longer as the rules increase, without grouping and explanatory text |
| Startup parameters | `--rules`/`--rule-fixes`, `--language`, `--images`, `--resolution-scale`, `--font-size`, etc. | Only available at startup, ordinary players will not use the command line |
| profile/setting file | `presentation` of `play-profile.json` (locale, images, model_5600, resolution_scale, font_size), `rules.json` in the trial directory | Manual editing, no interface |

## 2. Entrance and structure

The menu bar is changed to **"Options"** a top-level menu, with submenus given below by category, and "Settings..." to open a pop-up window. Windows and menus share the same settings model, and any changes in one are immediately reflected in the other.

```
选项
├─ 游戏性调整…      规则修正、难度调整（现在的「规则」菜单内容）
├─ 显示…            Original / HD、分辨率缩放、字号、减少闪白
├─ 语言与文本…      界面与剧情语言、阅读速度、已读跳过
├─ 存档…            历史会话、自动保存节点（M1 落地后）
└─ 设置…            打开完整设置窗口（以上分类为标签页）
```

- **"Options → Gameplay Adjustment" is the path determined this round**: The current "Rules" menu has been moved here as a whole, and is divided into two groups: "Correction" (enabled by default, fixes the contradictions in the original version) and "Difficulty Adjustment" (disabled by default, changing the strength). The group names are separated by dividing lines and non-clickable description items.
- [Basic Repair](../gameplay/base-fixes.md), which takes effect by default and has no switch, does not enter the setting interface and is only explained in the documentation and "About".
- The window uses tabs to host the same categories, each with a one-line description, current value, default value, and "Restore Default".

## 3. The metadata to be written for each setting

Following the rule directory approach, the settings are defined as data, and the interface is generated from it. Adding a new item does not change the UI code:

| Field | Purpose |
| --- | --- |
| id, classification | Stable identification and classification |
| Control type | Switch, radio selection (mutually exclusive group of original/halved/closed), numerical value, drop-down |
| Tag key | UI key of `content/locales/*.json`, three languages must be complete (`UI_KEYS` of `profile.py` has been derived according to the rule directory, if one is missing, startup will be refused) |
| Default value | Value for first startup; correction type is on by default, difficulty type is off by default |
| Effective time | Immediate/next settlement/next appearance/next entry/next start - the current rule is "next settlement", and the boss avatar is "next appearance". Such differences must be displayed on the interface |
| Write location | `rules.json`, presentation settings or profile |
| Archive impact | Whether to change the persistent gameplay state; changes must be entered into the archive compatibility list |

Mutually exclusive groups (such as the original version of the boss avatar/halved/off) can still be two Boolean switches in the data layer, but the interface is presented as a single selection, avoiding the current state of "cancel when both are checked" that requires explanation.

## 4. Technical solution

- The first version made **AppKit pop-up windows**, which were on the same layer as the menu bar code at that time, and could directly reuse language tags and real-time switching mechanisms without affecting game rendering. (Later, the entire page has been changed to RmlUi page, see the end of the article.)
- The in-game overlay UI (RT64 layer) is left until controller operation or cross-platform is required; at that time, the model settings remain unchanged and only the presentation layer is changed.
- Set the model in a header file of the host (similar to `rule_fixes.hpp` and `catalog`). The Python side continues to derive startup parameters and verification from the same definition to ensure that both sides will not drift.

## 5. Acceptance requirements

- Each category and each control has a title and description in three languages; when switching languages, the window and menu are redrawn at the same time (the menu already has this, the window will use it).
- Changes are written to the corresponding file and appended to the event log (currently the method of `rule-fixes-events.jsonl`), and the run report can restore "what settings were used for this run".
- Provide QA control hook: press an item like `rule-control.json` to write out the control status for bounded run verification.
- "Restore to Default" and "Original" presets are separated: the former returns to the default values (correction on, difficulty off), while the latter is all original behaviors turned off.
- It should be clear whether the game is paused when the window is opened; the time when the changes take effect is shown in §3, and players cannot be made to think that switching in the middle of the battle will affect the settlement this time.

## 6. First version implementation (2026-09-18)

| Section | Status |
| --- | --- |
| Menu bar "Options" | First version: "Gameplay Adjustment" submenu and "Settings..." (⌘,), AppKit. Now only the menu bar entry (`macos/app_menu.mm`) is retained. |
| Settings window | First version: rules (grouping), three presets, language radio selection, picture radio selection (grayed out when HD is not available), one line description for each group, AppKit. It is now the RmlUi settings page of `src/native/ui/frontend.cpp`, which also includes two new/original versions of "Pre-war Confirmation Interface" and "Inter-game Screen" (the latter was added on 2026-09-23, covering the main menu and transformation screen, and will take effect the next time you open the screen, write `intermission_ui` of `presentation.json`). |
| Synchronization | Window, menu, F6/F7 and QA hook share the same state; the window reads back the current value every frame, and retrieves all titles when the language changes. |
| Input | The game cannot receive keyboard input while the window is open. Wait until all keys are released after closing (`ModalInputRelease`). **The game does not pause. ** |
| Write back | The rule is written as `rules.json`; the language follows the original presentation setting (written as `presentation.json`); the screen does not write files and only affects this run. |
| Group source | Each item in the rule directory has `Kind` (`correction`/`difficulty`), from which menus, windows and default collections are derived; `tests/test_rule_fixes.py` Check that it is consistent with `rule_settings.CORRECTIONS`/`DIFFICULTY`. |
| QA hook | `SRW64_WINDOW_CONTROL=1`: `settings-control.json` (schema `srw64.settings-control.v1`, `action` as `open`/`close`/`press`, `id` as `rule:limit-cap`, `preset:rules_defaults`, `locale:zh-Hans`, `images:original`), the result and all control status are written to `settings-window-events.jsonl`. |

Actual measurement (`build/recomp/profile-play/sessions/20260918T023907.954768Z`): After selecting Chinese in the window, the game language changes from ja to zh-Hans, and the window title is synchronized to Chinese; selecting Original and HD triggers screen switching at VI 638/820 respectively (`image-mode-events.jsonl`); "Restore to default" removes the difficulty item and retains six modifications; closing the window and exiting normally (`native-graphics-run-completed`, exit code 0). For the actual measurement of menu grouping, see `20260918T023623.862474Z` (ja title, "Weapon inheritance" is included in the correction group).

The window width should be at least 460 points, and should be widened according to the longest line: the three English default buttons are one line wider than 460 points, and the last button was cut off; now the width is recalculated based on the content and the default line (including margins on both sides) after building the window and each time changing languages (`fit`, 2026-09-18).

Problems fixed in the process: radio buttons in the same view are treated as a group by AppKit, language and screen cancel each other, and are now placed in independent containers; the early version crashed once in the window attribute callback of RT64/plume when exiting (`EXC_BAD_ACCESS`, `CocoaWindow::updateWindowAttributesInternal`), the release of the panel was changed to be completed synchronously before SDL exit, and the delegate was removed first It did not appear again, but the callback itself belonged to the graphics layer and there was no separate recurrence to confirm the root cause.

Not done: Display class resolution/font size, archive classification, and description of each individual item's effective timing (now one line per group). See §7 for the About page.

2026-09-22: The native interface is unified into the recomp SDL/RmlUi page, and no system-dependent UI is made; the first version of the AppKit files above (`settings_window_macos.mm`, `rule_menu_macos.mm`, `presentation_settings_macos.mm`, etc.) have been deleted, `src/host/macos/` only retains the application menu bar entry `app_menu.mm` and `desktop_macos.mm`.

## 7. Pagination overlay panel (2026-09-27)

User 2026-09-25 reported that the full-screen opaque "Options" page looks like a desktop program and requires a "one-click call out of the game" panel (see [Steam Deck Keyboard](../design/steam-deck-controls.md) "Settings Interface Revision"). 2026-09-27 Set five paging, overlay panels, and remember the last paging, implemented in `settings_sync` of `src/native/ui/frontend.cpp`.

**Appearance**: The game screen runs as usual, darkened (translucent bottom), with a straight-edged panel in the middle with the same color scheme as the pre-war confirmation page (User 2026-09-27: The frame does not need beveled edges, and the tabs are also straight-edged rectangles): The top title and seven tabs (2026-10-01 adds the "Archive" page, 2026-10-05 Add a "cheat" page), the middle is the scrollable current page, and the bottom is the key prompt and "Close". The logical size of the interface is not less than 960×720 dp (when the interface size is enlarged, it is not less than 800×540 dp, see below), the panel accounts for 88%, the maximum width is 1040 dp, and the window is scaled together when scaling. **Game does not pause**, input is still blocked by `ModalInputRelease`.

| Page (`settings_page` value) | Content |
| --- | --- |
| General `general` | Language (Japanese/Simplified Chinese/English), picture (Original/HD, both buttons are grayed out when HD material is missing), aspect ratio (automatic: with the screen 4:3–16:9/4:3 original, write `presentation.json` for `aspect`, see [Widescreen](../design/deck-16x10.md)), frame (only 4:3), filter and filter row number (2026-10-05, see [Frame and Filter](bezels-and-filters.md)); the desktop platform also has other display modes (window/full screen) and window size (1×–4×), see §8 |
| Interface `interface` | Interface size (standard/large/extra large); pre-battle confirmation interface (new version/HD original/original), inter-scene screen, protagonist selection and name input, title menu screen, one row of segmented buttons each; display frame rate (off/on, write `presentation.json` for `show_fps`): the upper right corner updates "Game frames per second· The longest frame in this half second", based on the display list handed to the graphics thread by the game (`src/host/frame_rate.hpp`) |
| Rule `rules` | Three defaults and effective instructions at the top, two groups below: "Modification (default on)" and "Difficulty (default off)", each rule has one line of switches |
| Cheating `cheats` | 2026-10-05: Five switches (off by default) and a row of "Pilot Level". Click "Expand" to list the pilots and the button to change the level ([Goldfinger](../gameplay/cheats.md)). After adding this page, change the English tabs "Interface" and "Controls" to "UI" and "Input", otherwise the 7 tabs will not fit in the smallest window |
| Archive `saves` | 2026-10-01, see [Multiple Archive Column and Automatic Archive](../design/save-slots-autosave.md) §8: Automatic archive switch; keep 1/3/5/10 copies of each of the two automatic archives between games and rounds; write the cassette into four files: ares, Project64, mupen64plus, and RetroArch (archive library) `export/`); List the simulator files in the archive library `import/`, and import them into extended columns column by column (columns with inconsistent checksums must be clicked again and imported after repair). Set `settings.json` that exists in the archive library, and do not enter `presentation.json`. Only one line of description is displayed when the debug session has no archive library |
| Operation `controls` | Key changing page (2026-09-28, see [Key changing](controls-remapping.md)): Recognized controller, keyboard default (PCSX2 layout) description, key changing table listed by function (one column each for keyboard and controller, change by pressing a new key after selection), fixed shortcut keys and restoration to default |
| Feedback `feedback` (English Report) | 2026-10-07: Copy platform information, export problem reports, where to give feedback (GitHub form, official website text comments), see [Problem Report](bug-report.md) |
| About `about` | Application name Marchwind64, one sentence introduction, version number (taken from the `project(... VERSION)` of the root directory `CMakeLists.txt`, compiled with `SRW64_VERSION` Incoming); link line (official website, source code, problem feedback, system browser opened); update line ("Check for updates", results, "Download page" and "Update instructions" when there is a new version) and "Check for updates at startup" switch ([Update check](update-check.md)); "AI Debug Interface (MCP)" switch, when turned on, displays the listening address, running directory and "Copy running directory" ([Debug Interface](../guide/debug-interface.md#打开方式选项里的开关)); HarmonyOS Sans, PromptFont, librashader statement |

Each switch generates a row from `settings_choice(键, id 前缀, 模式列表, 当前模式)`: above it is `label(键)` and a mode and a button on the right, and below the whole row is `label(键+"_note")` with the id `前缀:模式` (same as §6, as `battle-ui:native`, `images:hd`). To add an original/new version switch, just add a line to call it on the "Interface" page, and then add its current value to the refresh stamp.

**operate**

| Input | Keyboard | Controller | Mouse/Touch |
| --- | --- | --- | --- |
| Open/Close | Ctrl/Cmd+, open; Esc or |
| Page change | Q／E, PageUp／PageDown, Ctrl+Tab／Ctrl+Shift+Tab | L1／R1 | Click tab |
| Select | ↑↓ (or W/S) to move between rows; ←→ (or A/D) to move between options in a row; when the focus is on the tab ←→ directly change pages | Cross keys/left joystick, same as left | Direct point |
| OK | Enter, Z, Space | A, menu key | — |

"Row" is the tab bar and each setting (element with `nav` class); ↑↓ on pages without options (operations, about) is changed to scrolling. After the page change, the focus falls on the first setting of the new page (the focus remains on the tab when the page is changed). Don't show focus box when using mouse (`body.pointer`). The entire page is rebuilt after a value change, with focus and scroll position preserved.

**Remember paging**: Write `settings_page` (`settings::set_settings_page`) of `presentation.json` every time you change the page, and return to this page next time you open it (including after restarting). When the launcher rewrites this file with `--language`, it will still bring it (`launch.cpp`).

**Debugging interface**: `ui.click` When clicking a setting control that is not on the current page by id, it will first turn to the page it is on and then click it (consistent with the player's operation), so `press` of `settings-control.json` and the old script clicked by id do not need to be changed; the id of the page label itself is `settings-page:<页>`. `ui.key` is used to send `q`/`e`/`pageup`, `pad` can be used to change pages if L1/R1 is sent.

**Chinese and Japanese line breaks**: RmlUi only breaks lines in ASCII blank spaces. Chinese and Japanese sentences without spaces are a whole paragraph and overflow if they cannot fit (09-27 actual machine: the description of the Japanese "インターミッション screen" is pressed under the button). So the description text alone takes up the entire line width. `word-break: break-word` can be forcibly disconnected, but it will cause RmlUi's line-breaking loop to get stuck (`ElementText.cpp:508` asserts that the screen will be refreshed and the window thread will no longer respond). **Do not use**. `tests/test_settings_window.py` Based on the smallest window, it is estimated that each piece of text without spaces (description, rule name, two columns of key table, page label, name plus button one row) can be accommodated, and it will be reported when a new entry is added or lengthened.

**Check**: `tests/test_settings_window.py` (the two lists of pages and key rows are consistent, the three language entries are complete, each column is not overflowed according to the minimum window estimate, paging write-back and `--language` are retained, and the key position for page change is maintained). Actual machine: `tools/recomp/debug/check_settings_pages.py` (Settings are opened on the title screen; five Chinese, English and Japanese pages are cut out at 960×720; Q/E, PageDown and handle L1/R1 for page change, movement and confirmation between lines and within lines; the rule of clicking the page by id will turn the page first; close and reopen to return to the last page; handle prompt, B close, view key on; 1600×1000 Large window screenshot), all passed on 2026-09-27, the screenshot is in the running directory.

Another fix: the old version of the refresh stamp missed the two switches "Protagonist Selection and Name Input" and "Title Menu Screen". After clicking, the selected status of the button will not be updated; now the stamp includes all switches.

Returns: [Optional rules](../gameplay/rule-fixes.md) · [Basic fixes](../gameplay/base-fixes.md) · [Built-in MOD roadmap](../design/mod-roadmap.md)

## Interface size

2026-09-28 Users reported on Steam Deck: The bottom operation prompts, the setting key prompts on the title screen, and the fonts on the pre-war confirmation page are all too small. Reason: For interfaces typed in dp (setting window, confirm new version before war, setting button in the lower right corner of the title, notification), a dp is a point. When the window is larger than 960×720 points, it only has more space and does not enlarge; a dp on the Deck’s 7-inch 1280×800 screen is only about half the size of the desktop. Pages drawn according to the original 320×240 ratio (inter-game pages, high-definition original pre-war pages) scale with the screen without being affected.

- **Settings**: "Interface Size" in the first line of the "Interface" page: Standard/Large/Extra Large=1/1.25/1.5 times (`settings::UiSize`, saved as `ui_size` of presentation.json, written only after the player has selected it). If not selected, the Steam Deck (`SteamDeck=1` or firmware report Valve Jupiter/Galileo, `src/host/steam_deck.hpp`) is extra large, and the others are standard.
- **How to enlarge**: `frontend.cpp`'s `sync`: dp is first kept as usual (zoomed down when the window is less than 960×720 points), and then multiplied by the interface size, but the logical size after enlargement is not less than 800×540 dp (large on Deck = 1024×640, extra large ≈ 864×540). Accordingly, the page must be arranged under 800×540 dp: the text in each column of the setting window is checked according to 800 width (`tests/test_settings_window.py`, the Japanese tab "インターフェース" was therefore changed to "screen", and a space was added for the long Japanese description to make a line break); the width of the pre-war confirmation page is less than 1000 dp When adding `narrow` (the avatar is 64 dp, the inner margin of the button becomes smaller), the numbers no longer wrap.
- **Dialogue bottom bar** (host draws in 320×240 coordinates): enlarge with the size of the interface (up to 1.4 times, to the lower edge of the dialogue box below), the operation prompt on the right side reduces the font size instead of truncating it when it cannot fit in the remaining width.
- **Button icons**: The icons of SRW64Prompts were originally scaled according to the height of Latin capital letters, and were placed one size smaller next to the Chinese characters, with only a thin slit for LB/RB; now each icon is enlarged to the height of a Chinese character (about 930/1000, centered at 380, up to 1.4 times magnified, see `build_prompt_font.py`).
- **Tip comes with the device**: There is no entry for the controller version (`_pad`), and the action symbols in the controller also display the controller icon when the controller is in use (originally all keyboard keys are displayed); the bottom of the pre-war confirmation page prompts to use symbols instead (originally hard-coded `Z / A`, `K / C▼`).

Actual machine (Mac, 1280×800 dot window simulates the logical size of the Deck, 2026-09-28): Under standard/large/extra large, I have seen the title, dialogue bottom bar, pre-war confirmation page, settings window and operation page; under extra large, the numbers on the pre-war confirmation page do not wrap, the buttons are in one row, and the prompt is a button icon.

## 8. Full screen and window size (2026-09-29)

Desktop platforms can go to full screen and set the window to an integer multiple of the original size; handheld consoles (Steam Deck, identified by firmware, game mode or desktop mode are both included) can go to full screen without these two options.

| Entrance | Method |
| --- | --- |
| Mac menu bar "Display" | "Full screen" ⌃⌘F (check = current full screen); "Window size 1×–4×" ⌘1–⌘4 (check = window is exactly this size). SDL has the same key as the English Toggle Full Screen in the Window menu, which has been hidden. `src/host/macos/app_menu.mm` only remembers the request, and the window thread handles it in `frontend.cpp`. |
| Windows／Linux | F11 switches to full screen (no modifier keys). No Alt+Enter: The game presses the scan code to read the keyboard, and Enter will also press START. |
| Set the "General" page | "Display mode" window/full screen, "Window size" 1×–4×, available on all desktop platforms. |

- Use `SDL_WINDOW_FULLSCREEN_DESKTOP` for full screen (native full screen on Mac is independent space).
- The window size n× = 240n points high, and the width is n times the screen width at the current ratio (`frame::width`): 2× at 16:10 is 768×480, 2× at 16:9 is 853×480, and when set to 4:3, 2× is 640×480. When changing gears, keep the center of the window stationary and keep it within the available range of the screen; gears that cannot be placed (including the title bar) and all gears in full screen are not selectable.
- The full-screen state is not saved, and it is a window every time it is started.
- Debug interface: `menu path=["显示","窗口大小 2×"]` Press menu item; `status.window.fullscreen`.

Actual measurement (`build/recomp/debug/20260929T132807.116292Z`, window start at 16:10): Menu 1×–4× successively obtains 384×240, 768×480, 1152×720, 1536×960; "Full Screen" obtains 2560×1440, while the four levels are grayed out and "Full Screen" is checked; click "Window" on the settings page to return 1536×960, click "2×" to return to 768×480; exit normally.