> **Language / Ngôn ngữ:** [English](native-dialogue-ui.en.md) · [Tiếng Việt](native-dialogue-ui.vi.md) · [中文](native-dialogue-ui.md)

# Native dialogue UI

2026-09-11: Added Japanese and Chinese language directory entries for unified original JP ROM, see [First batch implementation of native content architecture](native-content-foundation.md). The unified profile is currently used; the historical running evidence below still retains the original verification scope.

2026-09-09. This implementation connects the standard double-frame plot dialogue in the female super-type opening world map and the first tactical map to the host UI. It runs the original plot script, reads the current text ID, speaker, STOP fragment and waiting state, typeset it with a cross-platform text engine (FreeType + HarfBuzz + ICU, packaged HarmonyOS Sans), and draws it on the final Metal screen. The initial version used macOS Core Text, which was changed to a cross-platform engine starting from 2026-09-20. See [Chinese, Japanese and English cross-platform text and game dialogue](portable-text.md).

## Operation

The zoom text in the opening starry sky also supports E + Enter to skip the entire paragraph. For details, see [Opening Zoom Text](native-intro.md). The rest of the reading functions in the table below here are for standard dialogue.

| Functions | Game Keys | Current Keymap |
|---|---|---|
| Next reading page; the last page advances the original plot | Confirm A | Z |
| To increase the automatic reading speed, press and hold for continuous adjustment | Up | ↑ |
| Reduce speed to 0 and return to manual | Next | ↓ |
| Turn off automatic reading/cancel skipping | B |
| Fast forward: press once to turn one page, press and hold for 0.3 seconds to turn one page every 0.1 seconds; release to return to manual, and automatic reading will also be turned off | R + A | E + Z |
| Short skip: The plot script is executed directly to the next stopping point (end of script, limb selection, attack selection, switching to the battlefield, etc.), the dialogue and performance are not played, and the result is the same as after reading ([short skip](script-skip.md)) | R + START (controller R1 + menu) | E + Enter |
| Turn on/off conversation review | L | Q |
| Review: scroll up and down one line, turn left and right one screen (press and hold continuously; the joystick is the same as the cross key) / return; returning does not advance the plot | cross key or joystick / A, B, L, START | ↑↓←→ or WASD / K, L, Q, Enter |
| Text size 10–18, default 13 | C top/C bottom | I / K |

The handle also has two host keys (not visible in the game): R2 to fast forward (same as R+A; R2+menu is also pronounced as R+START, but pressing R2 will finish the current page first. The menu key often falls between two sentences, so the prompt bar reads R1+menu), and L2 switches to automatic reading (the last speed is used, the first time is 2nd gear). See [Steam Deck Keyboards](../design/steam-deck-controls.md).

**Automatic hiding of the bottom bar (2026-10-06, user determined):** The bottom bar (reading mode, automatic speed, font size, key prompts) under the dialogue is hidden for 5 seconds after the dialogue appears, and is displayed for 3 seconds when pressing any direction key, or changing the reading mode (font size, automatic speed, automatic switch, review, fast forward, skip); it is always displayed during fast forward and skip; switching keyboard and handle (the prompt icon changes accordingly) is also displayed for 3 seconds. The last 0.3 seconds fade out. Ordinary page turning does not count. Timing press VI (60 per second), in `native_dialogue.cpp` (`bar_until`, `show_bar`); `Frame.bar_fade` is handed over to `dialogue_scene.cpp`, `Painter::fade` is multiplied by the padding and text transparency of the bottom bar and enters the cache key of incremental drawing. When it is 0, the entire bar is not drawn. There is an `controls_bar` block (`fade`) in the scenario report. "Options → Interface → Dialogue Operation Prompts" can be changed to always display (`presentation.json`'s `dialogue_hints`: `auto`/`always`).

Auto speed 1–4 changes the display speed and the waiting time after reading at the same time; 0 is manual. The confirmation key directly goes to the next reading page, and there is no requirement to complete the word-by-word animation before pressing it again. Holding Normal to confirm will not advance continuously. The quick plot still advances according to the reading page. Short skip (from 2026-09-29) no longer confirms page by page: the host continuously executes script commands in the same frame, and the dialogue is not displayed, waiting and performing when the frame is completed, see [short skip](script-skip.md). The entire game's clock has not been modified.

**Fast Forward Release Key (2026-09-27):** Users require that after releasing the Fast Forward key, they will immediately return to "Click to Forward".

- Before the change (conclusion of read-only code): in fast forward state, each frame is recalculated according to the current key (press R and A at the same time), and there is no latch. Therefore, after releasing the frame, it will no longer fast forward, it will not enter automatic reading, and the first Z after releasing will not be swallowed. There are three reasons why it is not like "click and go":
- Press that frame to turn one page first, then every 6 VI (0.1 seconds). So holding down the key combination for more than 0.1 seconds will turn two pages. On the keyboard, first release Z and then press Z while E is still pressed, and it will be fast forward again; the same goes for short pressing R2 on the handle. A normal click often turns two pages.
- Fast forward without turning off automatic reading. It turned out that the automatic reading was on, but after releasing it, it continued to go down automatically.
- At 10 pages per second plus reaction time, you will typically have gone 2–3 pages more by the time you let go. The last page of this article has been confirmed. The original version will finish this article as usual. Stop and wait for A after the next article appears. This is the fast forward speed itself, not counting the residual state.
- Now (`Reader::update`, [dialogue_model.hpp](../../src/host/dialogue_model.hpp)):
- Press the fast forward key to turn one page immediately; after pressing and holding for `fast_hold_vis` (18 VI, 0.3 seconds), it will turn one page every `fast_step_vis` (6 VI). Short press only turns one page: Z when E is still pressed, short press R2.
- The released update will return to manual, and automatic reading will be turned off (user selected; if you want to go back to automatic, press L2 or ↑). The current page is stopped waiting for A, and the background confirmation will not go beyond the current page. If this item has been confirmed when you release it, you will also wait for A after the next one appears.
- The fast forward state only follows keystrokes: script boundaries and language changes will no longer clear it. Therefore, when you keep pressing across the border, it will not be regarded as a new click and wait for 0.3 seconds again.
- The keyboard and controller follow the same judgment: controller R2 is read as R+A in `input()`, which is the same as E+Z. R2+menu (R+A+START) enters to skip the current segment; releasing R2 while the skip is in progress will not be processed, and the skip will continue until the end of the script, selection or scene switching.
- Two new records are added to the event log: `fast` (`held`, `automatic`, `skip`) is recorded every time the fast forward key is pressed and released, and `turn` (`page`, `pending`) is recorded every time the reader turns a page (including the last page and enters waiting), and whether it was at that time. `fast`). State snapshots have `fast` added.
- The component test (`tests/native_dialogue.cpp`, run as `dialogue-reader` in `tests/dialogue_cpu`) covers the following situations. The reader before the change failed in the "short press to only turn a page" item:
- Short press and E while holding point Z will only turn one page.
- Page turning rhythm when pressed.
- After releasing, there is no page turning or background confirmation within 1900 VI. A only turns one page at a time.
- Release this item after confirming it, and wait for the next one. A. Turn off automatic reading.
- Press and hold across script boundaries does not re-wait.
- R2+Menu Skip to continue after releasing R2.
- Actual machine inspection script `tools/recomp/debug/check_fast_release.py`: Read the first dialogue of the new game, do the following operations in sequence, judge according to `fast`/`turn` in the log, and write the result as `fast-release-checks.json`:
- E+Z Press and release, then press Z again.
- Press and hold E point Z.
- Press and release R2, then press A again.
- Short press R2.
- Press and release R2 while auto-reading is on.
- R2+ menu.

For the two items of short press, first check that the press and hold duration is indeed between 6-18 VI. If it is not within this range, it will be judged as invalid. **Not yet running on the actual machine** (The user decided not to run it yet on 2026-09-27).

The current interface maintains the original avatar and double-frame layout. Use blue `#69BFFF` for the person's name; the current text is white and the other dialog box is gray. Playback saves the latest 256 dialogues of the current session; the one being read only records the content that has been displayed, the confirmed pages can be read back completely, and subsequent scripts that have not yet arrived will not be added in advance.

**Typesetting (2026-09-23, for rules, see [Dialogue Typesetting](../design/dialogue-typesetting.md)): **
- The name is number 10, placed in the upper left corner of the box; the text area is immediately below, 177 in width and 43 in height. The box ranges from 20 above the text origin to 34 below, for a total of 54 heights.
- The number of lines per page is adaptive according to the font size: first calculate how many lines can be placed according to the minimum line spacing (1.08 times for Chinese, 1.15 times for English), and then divide the remaining height among each line, up to 1.22 times. The default number 13 is 3 lines per page for both Chinese and English. The English text is arranged at 0.85 times the font size setting, and the number displayed in the bottom column remains unchanged.
- Use dynamic programming to select the page turning position: the smallest number of pages, followed by less cutting in the middle of the sentence, less cutting at commas, and less one or two words at the end of the line (punctuation and quotation marks do not count); when these items are the same, the front page will be full. The original page turning point only counts as the end of the sentence in Japanese: the translation marks the end of the sentence itself, and the original page turning point without punctuation is a sentence that continues across the page. The punctuation at the end of a Chinese line can therefore be reduced to half width when an extra word is added.
- These three details are set on 2026-09-24 according to the lines with the punctuation at the end of the page. 1,500 multi-page records were selected for typesetting, and the number of pages remains unchanged: the Chinese page with a sentence cut in the middle is 116 → 31, the first page with only one line is 156 → 55; the English page is 229 → 80, 164 → 77 respectively.
- **A whole line of dialogue. ** In the original version, the fragments (between `<STOP>`) that are turned out by pressing A each time are connected into one paragraph. Chinese is connected directly, and English is connected with spaces. The pages are re-paged according to the size of the frame. Once the page turned by the host contains the beginning of the next fragment, the previous `<STOP>` will be confirmed for the original version in the background; `<END>` will be confirmed when pressing A on the last page. The number of original confirmations is always the number of fragments plus one, and it will only move forward. The word-by-word display stops for 0.3 seconds when it reaches the original page turning point.
- The number of clips is based on the Japanese ROM record (which is what the game actually executes). When the `---` of the translation is less than that of the original text, the missing ones will be confirmed on the last page; the extra ones will be treated as ordinary sentence fragments.
- When changing the font size, the entire article will be rearranged, and the current page will still start from the same font. When switching languages, the entire paragraph is changed to another language, and reading continues from the beginning of the current paragraph in the original version.
- The battle lines are not consecutively arranged: they are still replaced and displayed segment by segment according to the original clips, and the font size is gradually reduced when they cannot fit.
- **Real machine verification (2026-09-24, `tools/recomp/debug/check_dialogue.py`): ** For the new game, select the default protagonist and name, read 18 dialogues from the beginning of the route (15 Chinese, 3 English, 11 of which have original page turning points, up to 3), and all 25 inspections passed.
- The number of background confirmations for each item is equal to the number of `<STOP>`, and `<END>` is exactly once; the original version never reaches the front of the host page.
- I/K is executed twice in Chinese and English, and the beginning of the current page remains unchanged.
- F7 rotates Chinese→English→Japanese→Chinese (or English→Japanese→Chinese→English) three times. Each time, it continues reading from the beginning of the current segment of the original version, and the original version does not advance.
- In the screenshot, the name line does not overlap with the text, and all three lines of text are within the frame.
- Problems with the content seen: The machine-translated Chinese often has no punctuation at the original page turning, and it is read into a sentence (such as "It's silly that your guerrillas lost in the battle..."); the default names of the protagonist and partner are still Japanese katakana.
- The use cases compared with the Python reference implementation are in `tests/data/dialogue-paging-cases.json`: 30 (real lines in Chinese and English, including different font sizes and forced page turning). All intermediate quantities used by typesetting rules on each strip (grapheme boundaries and widths, legal line breaks, full lines at each starting point), as well as game spacing, line boundaries, margins, and half-width positions. Input `dialogue-paging-inputs.json` in the same directory, generated by `tests/dialogue_cpu/paging_cases.cpp`; use `--check` to rearrange and compare, and run as `dialogue-paging-cases` test when CMake sets `SRW64_TEST_FONT_DIR`.

The latest additions include automatic gear scale, next advancement progress and double-frame current speaker mark, see [Reading Tips and Actual Machine Verification](native-reading-indicators.md).

Names in the review alternate between blue and orange according to the speaker, and consecutive clips of the same person remain the same color; scrolling through the review or cropping older records does not change the color of the existing names.

## Data and script boundaries

- `8008C9C0` After the text is loaded, the actual text ID is associated with the script instance; the plot dialogue uses the loading generation of each slot as the event identity (one record for one event), and the combat lines are added with the STOP sequence number. Repeated frames are not re-entered into history.
- `8008D748` is the original dialogue advancement function. The text buffer is `0x800FBAB0 + slot × 0x218`; the name buffer is `0x8015CB00 + slot × 52`. Read status, text, name, timing mode, STOP count and current fragment, and do not regard the number of text resource loading times as plot progress.
- This vanilla display path draws the entire STOP segment at once, without the vanilla verbatim cursor that can be directly inherited. The new UI maintains the display progress of Unicode glyph clusters by itself; the game provides fragments and wait states. Combining characters and UTF-16 surrogate pairs are not chopped into half words.
- The default external text source is `content/locales/zh-Hans.json`. Unicode translations are selected via the full TextKey, with the uncovered text falling back from the original ROM source directory. Adding text and line breaks is allowed, but the original STOP / END script barriers must be retained. Dynamic names are expanded from the game's current name buffer.
- The reading page of the new UI only consumes host input. When the host page reaches the next fragment, it temporarily submits an A trigger to the original `8008D748` to confirm the `<STOP>`, and immediately restores the input field; if the original version does not advance, it will be resent after 0.5 seconds. After pressing A on the last page, all `<STOP>` are confirmed and then `<END>` is submitted. STOP increment, completion status and subsequent plot are all handled by the original function. Timed dialogue also waits for the reading page of the new UI. In the event record, each background confirmation is recorded as `guest_stop` and `<END>` as `guest_confirm`.
- `8009EFDC` provides script instance boundaries; lookback only pauses polling for the owning script. `8009FA94` Select branch entry, script termination and overlay changes to be skipped to prevent them from being brought to the next stage.
- The adapter simultaneously checks the world map/tactical map overlay (ROM `0xA7EC0`, `0xAB160`), name visible markers, coordinates and `189×61` standard dialog box. Non-matching interfaces continue to display as they are.
- The speaker's name is translated into the current language according to the record number (`+0`) in the name tag; if the font displayed on the tag is inconsistent with the original Japanese text of the record (such as the protagonist's name entered by the player), it will remain unchanged. When reviewing entries, save the speaker by language and change them together when switching with F7.
- **Battle Lines** (Joined on 2026-09-23; Actual verification on the `battle-ui` mini-level on the same day: 4 lines are all native redraws, no original glyphs remain, Chinese and switched English texts and speakers are all from the language directory and line files, there is no `battle_overflow`): Line experience of the battle overlay (ROM `0x121560`) `8008FFAC → 8008F648 → 8008CD8C` enters the same set of text and name buffers and the same `189×61` box, so it is also within the adaptation range, but only **display replacement** is done: no reading events are created, no input is taken over, and timing fields are not changed. The original version is advanced and timed as usual, and the frame number and random number seeding remain unchanged. The translation is not paginated. If it does not fit on one page, it will be reduced from the current font size to 9 step by step. If it still cannot fit, the log will record `battle_overflow` and each sentence will record `battle_quote`. The reading status bar at the bottom is not displayed, and the battle lines cannot be reviewed.

## Draw

`native_dialogue.cpp` Release an immutable snapshot from the game thread. `graphics.cpp` Only removes the old glyph rectangle matching the two text boxes within the original `8008DC40` dialog drawing range, modifying the copy submitted to RT64 without changing the RDRAM original display list. The background, avatar, frame lines, and map markers are retained separately.

The RT64 rendering hook exposes the current workload ID, and the new text is associated with the corresponding game frame to avoid name/dialogue skewing caused by delays in the rendering queue. The text engine breaks pages into lines within the logical text width (see [Dialogue Typesetting](../design/dialogue-typesetting.md) for rules), rasterizes by final drawable pixels, and Metal is composited during final rendering. Window changes will regenerate clear text without stretching low-resolution text images. The current game layout is still a centered 4:3; widening the window does not mean widening the map field of view.

## Reproduction and Evidence

`scripts/Play SRW64 Native.command` is enabled by default. To rewatch the new game opening run:

```sh
.venv/bin/python tools/recomp/run/play_native.py --profile config/recomp/profiles/play-profile.json --new-game
```

Choose a female super type and default name. This entrance still uses the independent trial directory and archived copy.

Debugging interface script for real machine inspection `tools/recomp/debug/check_dialogue.py`: At the beginning of the new game's post-reading route, check the number of background confirmations, I/K and F7 one by one. The results are shown in the "Typesetting" section above.

Below is the historical evidence for the original version on 2026-09-09. At the time rendering with Core Text, the verify_native_dialogue.py check was driven by the control file, both of which have been removed. The check at that time only submitted keystrokes and optional SDL window sizes to the host and did not modify game memory. The evidence is recorded separately: `dialogue-state.json` is the CPU conversation state, `dialogue-events.jsonl` is the fragment/confirmation/boundary event, `dialogue-present.json` is the actual rendering workload, `present-*.png` is the readback after GPU completion, and `ui-checks/acceptance.json` is the run check.

Static check: `make check`. Typesetting and reading status check: `cmake --build build/recomp/gfx-build --target srw64-dialogue-test`, then run `build/recomp/gfx-build/srw64-dialogue-test`.

The actual running checks are at `build/recomp/native-dialogue/live-4/ui-checks/acceptance.json`: target dialogue `17412 / STOP 1`, page break 18, replay pause and scroll, confirm return without forwarding, automatic speed back to 0, three window sizes, fast forward release key, opening skip boundary and tactical map first sentence `17460` passed. Among them, "Fast Forward Release Key" is to use the control file to hold down R+A 24 VI at the same time and then release it at the same time. After that, the dialogue events in the 160 VI remain unchanged and no longer automatically read; there is no verification that A only turns one page after release, and there is no verification that E is still pressed, R2, and automatic reading is on. These situations were later added to the section "Fast Forward Release Key" above. The screenshots are all GPU readbacks after the CPU script is actually run. Skipping the overlay toggle stopped in VI 18056, the first sentence of the map appeared in VI 19364 and kept waiting manually.

`live-3` is the previous round of inspection: the key function is visible, but the resize screenshot inspection mistakenly used a thicker 60-VI state sample and may repeatedly reference the old frame, so the window scaling acceptance uses the modified `live-4` independent frame. The initial fast-forward check of `live-4` was also sampled before the key was released; instead, it waited for the actual VI and duration in the control receipt, and then passed the retest in the same game process. The above problem belongs to the sampling time of the verification script, and failed assertions are not counted as evidence of success.

This round does not mean that all UI of the entire game has been taken over. Name input, options menu, tactics/weapons menu and text within pictures still follow the existing paths; post-war branches, post-load history segments and all real monitor DPI combinations must be added with run coverage respectively. The current controller buttons are verified by the host N64 input status; this host has not yet connected to the physical controller device.

## Host exit repair

The actual startup/exit check of the HD entry found that the timer thread in the fixed version runtime uses `detach`, which may still run after the main program releases RDRAM and destroys the queue. The crash report locates the queue wait at `timer_thread`.

`prepare_runtime_lifecycle.py` Generates two locally compiled copies from locked and unmodified upstream source: waking up the timer thread with a stop message, and `join` before releasing RDRAM. The upstream checkout remains intact; the SHA-256 before and after the generated file is recorded in `build/recomp/runtime-lifecycle/manifest.json`, and the host run report also records this adaptation. `tests/native_timer_shutdown.cpp` tests the empty queue, long wait, period timer, repeated shutdown and RDRAM life cycle on the actual adaptation source code, and loops through AddressSanitizer / UndefinedBehaviorSanitizer 30 times.

Final HD entry startup/exit check completed 1,704 VI, exit 0, SHA-256 of initial SRAM unchanged. This use of SDL dummy audio device verification process life cycle is not used as speaker audition evidence. 47 Python checks, Core Text/reading status checks, and CPU host startup exit checks passed. The total delivery record was `build/recomp/native-dialogue/acceptance.json`, distinguishing between a live UI run of 22,758 VIs, subsequent long text automated component testing awaiting fixes, and entry checks after final lifecycle fixes.

To reproduce the timer check:

```sh
clang++ -std=c++20 -fsanitize=address,undefined -g \
  -I build/recomp/runtime-lifecycle \
  -I build/recomp/upstream/N64ModernRuntime/ultramodern/include \
  -I build/recomp/upstream/N64ModernRuntime/thirdparty \
  -I build/recomp/upstream/N64ModernRuntime/thirdparty/concurrentqueue \
  tests/native_timer_shutdown.cpp -o build/recomp/native-dialogue/timer-shutdown-test
build/recomp/native-dialogue/timer-shutdown-test
```