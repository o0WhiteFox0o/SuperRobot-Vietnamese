> **Language / Ngôn ngữ:** [English](steam-deck-controls.en.md) · [Tiếng Việt](steam-deck-controls.vi.md) · [中文](steam-deck-controls.md)

# Steam Deck keys and button icons

2026-09-25. The Steam Deck version operates according to the **Steam default controller template**, and players do not need to change the Steam input settings. This page records the current key position (subject to code), the setting entry added this time, and the key icon (PromptFont). For the superior plan, see [Three-Platform Porting](three-platform-port.md) X2, and for the construction and installation, see [Linux Build](../guide/linux-build.md).

## Principles

- Only use the original meaning of the Deck button in the default template: SDL sees the standard controller (Steam Virtual Controller), and the button names are the same as the Xbox layout.
- A key can only do one thing in the same scene; the combination already occupied by the original version will not be changed.
- New functions added by the host (settings, dialogue reading, skipping) give priority to keys that are not used in the original version: view keys, L2, R2, and back keys. L2 and R2 are given to the host (agreed by user 2026-09-25), these two keys are not visible in the game itself.
- The prompt follows the player's last used device: the controller prompt (`<key>_pad` entry) is displayed after controller input, and the keyboard prompt is replaced after keyboard, mouse or touch screen input.
- You can use the touch screen to click anywhere you can click.

## Existing keys

The mapping of the controller to the N64 buttons is the default binding of `src/host/input_bindings.hpp`. Players can change it on the settings "Operation" page ([Change Keys](../native/controls-remapping.md)); 2026-09-28 Press [Original Button Analysis](../gameplay/original-controls.md) to change the function priority: the original useful A, B, START, cross keys, joystick, L/R are still the same, Z and X/Y Free it up for this function. The native page uses `frontend.cpp` and `pad_keys` to convert the handle into page buttons; the setting window is `settings_pad`, and the pre-war confirmation page is `battle_buttons`.

| Deck button | In game (N64) | Native page (session, title, archive, name, etc.) | Dialogue reading | Settings window |
| --- | --- | --- | --- | --- |
| A | A | OK | Next page | Press current button |
| B | B | Return | — | Close |
|
| Y | For host: Switch the battle animation on the pre-battle confirmation page | Switch the battle animation on the pre-battle confirmation page | — | — |
| L2 | For host: When the map is idle, the cursor moves to the previous enemy body | — | Automatic reading on/off | — |
| R2 | For host: When the map is idle, the cursor goes to the next enemy body | — | Press and hold to fast forward; R2+menu to skip paragraphs | — |
| L1 / R1 | L / R (switch our inactive body when the map is idle) | L / R (turn the stage, previous song, etc.) | L1 review; R1 and other key combinations | Previous page/next page |
| Menu key ☰ | START | OK (partial page) | R2 (or R1) + menu Skip paragraph | Press current button |
| View key ⧉ | — (for host) | Open settings | Open settings | Close settings |
| D-pad/Left joystick | D-pad/Left joystick | Move cursor | ↑↓ Automatic speed | ↑↓ Line feed, ←→ page change (on page tab ←→ page change) |
| Right joystick | C key (up, down, left and right; ↑↓ title track ±10) | C key; pre-battle confirmation page ↓ also switches battle animation | adjust font size up or down | — |
| L3 / R3 (press the joystick) | For host: switch language/original and HD screen | Same as left | Same as left | Same as left |
| (none) | Z: synonymous with L in the list, Z+START returns to the title; there are no keys on the handle, and the keyboard is still a space | — | — | — |
| L4 L5 R4 R5 Back keys | Not used | — | — | — |
| Steam Key, Quick Access Key | Owned by Steam | — | — | — |

Others:

- **Dialogue:** R2 press and hold fast forward, R2+menu skips the current paragraph, L2 switches to automatic reading (the last speed is used when opening, the first time is 2 gear; ↑↓ can still adjust the speed), L1 opens review (↑↓ scroll in review, L1/A/B returns). The original R1+A, R1+ menu is still available (N64’s R key combination). Implementation: R2 is passed to the reader as R+A in `input()` of `native_dialogue.cpp`; L2 is called `Reader::toggle_auto`.
- **Casting and confirmation page:** A confirms, B returns to casting on the confirmation page. The name cannot be changed (2026-09-27), and the on-screen keyboard is no longer required.
- **Pre-battle confirmation page:** A confirms, B returns, L1 changes weapons, R1 spirit, right joystick ↓ switches battle animation (the original global switch `D_8015DDA8` bit2, the battle will not enter the show after it is turned off).
- **Tactical Map:** L1/R1 switches between our inactive aircraft (original version), L2/R2 switches between enemy and third-party aircraft (the practice of modern aircraft warfare, [`enemy_cycle.cpp`](../../src/host/enemy_cycle.cpp), see [L2 / R2 switching enemy aircraft](../native/enemy-cycle.md)).
- **Startup:** Automatic full screen when `SteamDeck=1`; START pressed within 2 seconds of booting is ignored (Pak management screen will be terminated).

## Set entrance (Added on 2026-09-25)

User feedback: The Deck version does not have a direct entry to switch language, HD and options. The reason is that the entrance on the Mac is in the menu bar, and there is no menu bar on the Deck. You can only rely on the view key, and there is no prompt on the screen. Now two visible entrances have been added, both opening the same settings window (language, original/HD graphics, rule modifications, and switching between interfaces):

- **Title screen** (PRESS START and ring menu, title main state 2, 3): a small button in the upper left corner (from 2026-10-02; the lower right corner is given to the MOD entrance, see [Customized Campaign](custom-campaign.md) §8). The handle prompt is "View Key Settings", and under the keyboard is "Settings...". It can also be opened by touching the screen or clicking the mouse. Mac has a menu bar that only appears after controller input. The code is in `home_sync` of `frontend.cpp`.
- **Inter-game main menu**: Add "View Key Settings" at the end of the handle prompt.

A line "Language/Screen/Rules..." was added under the original three items of the title オプション page. Users should not insert host settings into the original settings page. It has been removed (2026-09-25). What users want is the setting of "one-click calling in the game": see "Settings Interface Revision" below.

At the same time, one thing has been fixed: the prompt at the bottom of the pre-battle confirmation page and the animated switch prompt of the original battle HUD were originally hardcoded into keyboard and N64 key names ("Z/A" "K/C▼"). A, L1, R1, right joystick ↓, and B are now displayed under the handle.

The above has only been compiled on Mac, and has not been checked with actual screenshots, nor verified on Deck.

## Known issues and pending issues

- **Z + START is the original "exit level"**: pressing it during the battle performance will return to the BANPRESTO logo and title screen, and all unsaved progress will be lost (the original abort branch `801C97E4` selects mode 7 or 0x11, 2026-09-25 The session skipped by the battle performance returns to the title, recorded in its probe code comment, and has not yet been submitted). It turns out that L2 is also Z, and the L2+ menu is the left index finger and the right thumb, which is easy to press by mistake; now L2 belongs to the host, and only the Y+ menu is left (both are on the right hand, and you have to press it deliberately). Whether to block the Y+ menu during the performance is **up to the user's decision**.
- **Skip mid-performance**: Another session is doing "Press B during the performance to go directly to the end of the performance", the code has not been submitted, and the actual machine verification has not been completed. It is recommended to recognize R2 on the controller at the same time (consistent with "R2 fast forward" in the dialogue, prompting to write R2), B is still available; the session has been informed.
- **Back Key Idle**: Don’t use it yet (not all controllers have it).
- **Quick switching between language and HD**: The keyboard has F7 (language) and F6 (original/HD). For the time being, the handle only accesses the settings window without adding key combinations to avoid accidental touches.
- **Handle navigation of settings window**: Changed to paging (2026-09-27): L1/R1 page change, ↑↓ to move between settings, ←→ to move between options in a row, see next section.

## Setting interface revision (done on 2026-09-27)

2026-09-25 Actual screenshots: The view key does indeed open the settings with one click, but it opens a full-screen, opaque "options" page (the left column of rules, the right column of languages and interface switches need to be scrolled), like the settings page of a desktop program, covering the entire game. What users want is "the feeling of calling out with one click in the game":

- Layer a translucent background on the game screen, and a panel in the middle. The style is consistent with the original page. When you close it, you will return to the original position;
- One key to call out, the same key or B to close: view key on Deck, pending on keyboard (Esc now exits the game);
- Paging (for example, general: language, screen; interface: each original/new version switch; rules: modification and difficulty; keys: key map), L1/R1 page turning, cross key options, A switching;
- TBD: Whether to pause the game when opening.

The "Steam Deck SSH Connection and Installation" session mentions the same directions (pagination, L1/R1, consistent with RecompFrontend).

2026-09-27 Implementation: translucent panel superimposed on the game, five pages (general: language, screen; interface: each original/new version switch; rules; operation: key table; about: version and font), L1/R1 page turning, cross key option, A to confirm, B or view key to close, the last paging is written into `presentation.json` and will be used next time. The keyboard is still Ctrl/Cmd+ to open, Esc to close, and Q/E to turn pages. The game still doesn't pause. See [Settings Window](../native/settings-window.md) §7 for details. No actual screenshots yet.

## Key icon

2026-09-28 Realized. The original plan was to draw a set of icon fonts by myself; the user pointed out that there is a ready-made key font, and used **PromptFont** (Yukari "Shinmera" Hafner, SIL OFL 1.1) instead. Zelda64Recomp also uses it; a copy (`Zelda64Recomp-reference/assets/promptfont`, 2023-12-29) is included in the fixed upstream checkout of this machine, so there is no need to download it separately. The range set by the user: the handle prompt displays the key icon of the controller on the hand, and the keyboard prompt adds keycap icons for function keys such as Esc and Enter; the original N64 keys do not do this. 2026-09-30 Keycap icons are also used for letter keys, numeric keys, Backspace, Shift, Alt, and Delete (PromptFont is drawn on full-width letters U+FF21–FF3A, full-width numbers U+FF10–FF19, and moved to U+E850–E87D): Users require that all key prompts use PromptFont. The previous pre-battle confirmation page had “K to start the battle· Q Select Weapon" is written. The only things that can still be written are punctuation marks and keypad keys without icons.

### Font

- PromptFont puts icons on common code points (arrows, mathematical symbols). HarmonyOS Sans also has 9 of them. If it is only used as a fallback font, it will never be used. и will be displayed as an ordinary arrow.
- So [`build_prompt_font.py`](../../tools/content/build_prompt_font.py) only selects the 99 glyphs to be used (letters, numbers and four modifier keys added on 2026-09-30), moves them to the private area starting from U+E800, scales them according to the ratio of the height of the uppercase letters of the two fonts 700/660, and the vertical measurement is as shown in HarmonyOS Sans SC. The generated `content/fonts/SRW64Prompts.ttf` is about 18 KB and is submitted with the warehouse; it is renamed according to OFL, and the license and signature are in `LICENSE-SRW64Prompts.txt`.
- Both sets of text engines connect it to the end of the font chain (RmlUi is registered as a backup font, the dialogue engine sees `game_fonts.cpp`), and is put into the font directory together with other fonts by `prepare_fonts.py`. The "About" page of the settings window is signed as required by PromptFont.
- Note: Zelda64Recomp and RecompFrontend's `promptfont.h` reverses the two code bits of the keyboard direction keys. It is actually U+23F5 on the right and U+23F6 on the top. The font shall prevail.

### How to write in text

Marks are written in the entry, and the `expand_prompts()` of [`button_prompts.hpp`](../../src/native/text/button_prompts.hpp) is changed to the icon character before display: the RmlUi page is changed in `label()`, the name page is changed before the entry table is transferred, and the dialogue bottom column and review are changed in `dialogue_scene.cpp`. Placeholders such as `{n}` are not affected.

| Mark | Deck | Xbox | PlayStation | Switch |
| --- | --- | --- | --- | --- |
| `{A}``{B}``{X}``{Y}` | A B |
| `{L1}``{R1}``{L2}``{R2}` | L1 R1 L2 R2 | LB RB LT RT | L1 R1 L2 R2 | L R ZL ZR |
| `{View}``{Menu}` | View/Menu | View/Menu | Create／Options | − / + |
| `{DPad}``{DUp}` … `{DUpDown}``{DLeftRight}` | Cross keys (whole or highlighted direction) | Same as left | Same as left | Same as left |
| `{LStick}``{RStick}``{RStickUp}``{RStickDown}``{RStickUpDown}` | Joystick (with direction arrow) | Same as left | Same as left | Same as left |

Keyboard notations are the same for each family: `{Esc}``{Enter}``{Tab}``{Space}``{Ctrl}``{KeyUp}``{KeyDown}``{KeyLeft}``{KeyRight}``{Arrows}``{WASD}``{F5}``{F6}``{F7}` (`{IJKL}` is removed with the old keyboard table; the keyboard defaults to PCSX2 layout, see [Change Keys](../native/controls-remapping.md)).

- Controller family: `SteamDeck=1` Fixed Deck (SDL sees the Steam virtual controller in game mode and will be treated as Xbox); otherwise when pressing connect, `SDL_GameControllerGetType`: PS3/4/5 → PlayStation, Switch Pro → Switch, the rest → Xbox. `input::pad_family` exists, and a copy is also included in the dialogue frame snapshot.
- The Switch handle is displayed according to its position (OK is the lower key, Return is the right key), not printing, so the universal four-point diagram of PromptFont is used.
- All 57 `_pad` entries and the corresponding keyboard entries, `pad_rstick_down` (the animation switch of the original pre-war interface), a total of 303 entries in three languages, have been changed to notation.

### Test

- `tests/test_button_prompts.py`: Every character used in the C++ table is in the font, and the original code bit has been removed; the symbols in the entry are all known, and there is no `{{`; the symbols in the three languages ​​of the same entry are the same; the handle entry only uses the handle mark, and the keyboard entry only uses the keyboard mark; the font and license are in the packaging list.
- `make recomp-button-prompts-test` (`tests/native_button_prompts.cpp`): The replacement results and placeholders of each family are not affected.
- No actual screenshots yet.

## Verification plan

- **Controller injection of the debugging interface:** The `pad` method (`srw64ctl pad r2 l2`) merges the virtual controller into the state of the real controller (the same mask as `srw64_pad_state()`). You can intercept the controller prompts and icons and test L2/R2 on Mac.
- **Mac screenshot check:** Entrance in the lower right corner of the title, view key to open settings, inter-game prompts, pre-war confirmation page prompts, one each in Chinese, Japanese and English; two states of keyboard and controller.
- **Deck Actual Unit:** In game mode, only use the controller, open the settings from the title, switch language and HD, and go through Name → Episode 1 → Battle → Interscene → Archive; confirm that the view key does reach the game under the default template.

## Implementation order

1. Set entrance and pre-battle confirmation page prompts; L2 automatic reading, R2 fast forward; L2/R2 switching between enemies on the map (this time, it has been compiled, and the reader unit test has been added, waiting for screenshots and actual machines).
2. Inject the handle of the debugging interface (`pad` method and `srw64ctl pad`, added), and add Mac screenshots to check.
3. Icon font: Use PromptFont instead (done on 2026-09-28, see above).
4. Change all `_pad` entries to notation (already done).
5. There are several things to be decided by the user: whether to block the Y+ menu during the performance; whether to skip the R2 prompt after the performance goes online.