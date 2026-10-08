> **Language / Ngôn ngữ:** [English](native-foundations-verification.en.md) · [Tiếng Việt](native-foundations-verification.vi.md) · [中文](native-foundations-verification.md)

# Language settings, saved collections and status comparison

2026-09-12. The scope is the project's own modules and does not connect to external MODs. The production of language content will be rescheduled; the random timing of the original version remains unchanged, and only differences will be verified and recorded.

> This is the verification record for 2026-09-12. The translation size (153 items), Cocoa F7 and control file scripts have been replaced: the current translations are in [Native Content Architecture](native-content-foundation.md#多语言内容), and the actual machine check of language switching is in `tools/recomp/debug/check_localization.py`.

## Language settings and overrides

Press **F7** while the unified profile is running, and press **Japanese → Chinese → English** to cycle hot switch, **no pop-up window**, and remember the selection for next startup; the window title displays the current language. Settings are written to `build/recomp/profile-play/presentation.json`, separate from game SRAM and gameplay identity. Launcher priority is explicit `--language`, saved settings, profile default. Invalid settings will explicitly report an error and can be overridden with explicit language to resume startup.

Starting from 2026-09-13, the hotkeys cycle through profile registration order `ja` → `zh-Hans` → `en`, and the window language name comes from the directory configuration; the old single-language probe can still run. F7 handles the game screen and name editor through the same native event path; auto-repeat, combinations with modifier keys do not trigger switching, and F7 is left to the input method when the input method is composing words. Wait for the physical keyboard and original game input to be released during and after the switch to avoid the still-pressed OK/START/R keys being treated as new keys. The switching request is handed over to the game thread, and the new layout is prepared first. After success, the immutable directory and reading status are released; if it fails, the old directory and reading status are retained. Configure disk writing failure to be reported in the window title and log, without pop-up windows or pretending to have remembered the settings.

The current dialogue retains the same TextKey, structural fragment and event identity, is re-formatted and displayed from the beginning of the fragment, and automatically advances/fast-forwards/skips pauses; the next sentence will not be confirmed for the player. The completed replay clip is switched to the new language, and dynamic parameters such as names use the expansion results saved at the time of the event. There is no reliable cross-language character position mapping for unfinished fragments, so new languages ​​read from the beginning of the fragment and do not automatically put the unread tail into history. The game's original name field is not translated or rewritten. The input field and current focus are retained when the name page copy is refreshed.

Each rendered frame carries a reference to the language directory when generated; old frames still in the GPU queue continue to use their old fonts/labels, and new frames use the new directory as a whole to avoid mixing old text with new labels. Display switching does not write the gameplay memory. The original menu, baked text, etc. are not adapted and consumers still use the original text. It cannot be said that the entire UI has been localized.

`prepare_profile()` compiles all registered directories, verifies translation according to source version and control structure, and outputs `coverage.json`. The results of `tools/content/compile_profile.py` include the report path and summary. The report separately counts translations, drafts, reviewed, missing translations and each text table; records consumers who have not yet accessed the original menu, battle tags, opening baked text, etc. If the translation is missing, the original Japanese text will be used. Japanese is the source language, so "0 translations" is not used to indicate that Japanese is missing.

There are **51,174 items** in this source data; there are **153 draft items in Chinese and English, 0 items have been reviewed, and 51,021 items have been returned for missing translations**. The English range is the same as the existing Chinese, and there are also all 40 pieces of native UI copywriting. The denominator is the extracted text records, which does not mean that all records have native drawing paths; 153 cannot be called full game translation coverage.

Window and regression evidence:

- Records of early restart taking effect and pop-up hot switching are retained in `build/recomp/three-foundations/settings-live/`, `language-restart-ui/`, `hot-locale-flow-final/`; these interfaces have been replaced by direct hotkeys.
- The previous bilingual version of verify_locale_switch.py ​​(deleted, now checked by `tools/recomp/debug/check_localization.py`) sends actual Cocoa F7 press/release events to verify four bidirectional switches, no sheet, the same fragment/history number, look back translation, repeat/modify keys are not triggered, and the observation area before and after submission is consistent; the final run record is `hotkey-flow-final/hot-locale-verification.json`, and the window screenshot is `hotkey-flow-final/hotkey-ja-window.png`.
- The original input script formed a new keystroke and turned off review when START/R was still pressed; `ModalInputRelease` has been fixed, and the final hotkey run still covered this hold-in scenario.
- F7, group word protection, unsubmitted text retention and HD/Original independent switching of the name page were independently verified and recorded as `hotkey-name-final/hotkey-name-verification.json`. Test input `ナナ` maintains the original field after switching between Japanese + HD and Chinese + Original, without confirming the name to the game.
- Switching requests are handled by the adapter bridge with the original end-of-frame empty function `80085F30`, so name page/non-dialogue scenes can also be applied; the original function call is retained, and the adapter does not write guest context or gameplay RAM. The "only handle requests when the dialogue is updated" issue exposed by the first name page test remains in `hotkey-name/` and is not considered passed.
- Launcher tests verify that the save language enters the host parameters, explicit overrides take effect, and the save settings are not overwritten. This test is kept separate from the actual window evidence.

## English technical verification supplement (2026-09-13)

`content/locales/en.json` Independently writes an English draft, the scope is the same as the existing 153 Chinese records, including 60 menus/name tags and 93 first episode dialogues, and an additional 40 pieces of native UI copywriting are completed. Source summary, STOP/END, and dynamic name parameters are checked against the original Japanese record; no text from other English translation projects is cited. English uses Helvetica and Core Text for automatic word wrapping and pagination. The new language will not expand the rendering access range of the original menu; the name field and the name of the dialogue speaker will still use the original game values, and will fall back to Japanese if there is no translation.

This local evidence is located at `build/recomp/english-support/` and is not released with the warehouse:

- `compiled-en/coverage.json`: English 153 drafts, 0 reviewed, 51,021 fallbacks, native UI 40/40.
- `dialogue-live/hot-locale-verification.json`: Actual F7 switches six times in two rounds; each time the settings are saved, the same plot events and number of historical entries are maintained. The completed review content is in three different languages. Repeat/modification keys are not triggered, and there are no pop-ups. The observed game memory area before and after submission is consistent.
- `name-live/hotkey-name-verification.json`: four switches through all three languages; the edited value `ナナ` and the focus are retained, F7 is not triggered when IME is grouping words, HD/Original is switched independently, and the game name is not confirmed.
- `english-live/english-reading-verification.json`: Start directly in English, read eight dialogue fragments with normal confirmation, including two-page long fragments; each completed historical entry is consistent with the complete English text.
- `verification.json`: Three runs using the same host binary, the exit code is 0, all observed creation/join 4/4, remaining 0, and no game threads before and after RDRAM release; source file summary is also recorded.

`make check` was passed for 131 items, `make recomp-native-check` was passed. Launcher tests override saved `en` entry host parameters, as well as explicit Japanese/Chinese overrides without overwriting existing preferences. The actual window has been checked for English dialogue, replays, and name pages; this does not represent screen-by-screen review of all 153 items, full game English translation, or full-process compatibility acceptance. The original random timing remains unchanged.

## Save: File transaction has been verified, there is still a threshold for complete recovery

`src/srw64_native/checkpoints.py` is the **storage prototype** of the saved collection, which is automatically saved by players who have not yet connected. SRAM and extended state are written into immutable new generations, SHA-256 is calculated member by member, and a single index is atomically released after manifest verification. The restoration selects the complete generation by index. When damaged, the entire group is rolled back and members of different generations are not spliced. Unpublished directories left behind by an outage are not automatically promoted to recoverable archives. Rotation limits the number of generations in the index and currently does not automatically delete old directories.

Tests cover broken members, broken manifests, partial writes, failed index commits, unknown states/rules, bad indexes and symlinks. The `node_verified` here is a precondition that the adaptation layer must provide. The repository itself does not determine the game safe node. The existing extension prototype only contains RNG tables and indexes, and does not yet include reseeding counts, read status, and no production recovery consumers.

Lock the original serialization entry for JP Rev 0:

| Entrance | Function confirmed |
| --- | --- |
| `800924D8` | Conditioning data is written to RAM `801C2600`, long `1F00`. This RAM will cover another overlay during the map phase and cannot be called at any time. |
| `80093278` | Tactical data written to RAM `800FBEF0`, long `3AE0`. Parameter 0 is the original memory backup, and parameter 1 is written to SRAM. |
| `800927A4` / `800936A0` | Original preparation / tactical restoration. |
| `8009EDB8` | When the script stage `C1` is completed, the status `80` is converted to `C0`, and tactical memory backup is called. |

`original_saves.py` Verify the original format: The three SRAM slots are located at `10`, `1F10`, and `3E10`. The tactical raw check only accumulates `1F00` bytes, even if the entire tactical segment is `3AE0` long; tail corruption may pass the raw check and therefore cannot replace the full file digest.

Actual operation captured original memory backup after the opening event of the first episode of Female Super Series: `first-tactical-capture/state-96-tactical-save.json`, `tactical-95.payload`. This acquisition used an older probe with a file number difference of 1; the new probe has been changed to explicitly reference the same numbered attachment in the observation record.

Load this backup into the independent experimental SRAM, and use `config/recomp/inputs/load-continue.json` to completely exit and then cold start, and you have returned to the first episode map. The source, summary, and original verification record are in `first-turn-candidate.json`; the restored observation is in `first-turn-cold/state-1-tactical-restored.json`, and the map screenshot is `first-turn-cold/present-1620.png`.

`first-turn-restore-comparison.json` Compares the common observation area between the original serialization return and the original recovery return: the campaign flag, plot variables, player progress/name, machine, pilot and component arrays are consistent; there is a **2,079 byte difference** in the RNG area, and a **28 byte difference** in the map unit record. The latter are all located in the `+2` field of the 14 `20` byte record; recovery returns `FFFF`, which has been reallocated after the map has finished rebuilding. The `801DE0B8` and `801E06C4` instructions of overlay `000AB160` write the handle of the rendering object `800FFA70 + index*C4 + 48` to this field, so there is a static basis for rebuilding the presentation resource. The original differences remain, no RNG differences are removed or full equivalence is claimed on this basis. The old collection does not yet include two reseeding counts.

**Conclusion: It has been verified that this original backup can be cold booted back to the map, but the complete state recovery has not yet been verified. ** Therefore do not set the storage prototype or this experiment as the default auto-save, and do not claim that the different bookmarks and all rounds/maintenance nodes have been completed. The next implementation threshold is to complete the expansion status and recovery sequence, verify the reconstruction reference and the next actual action after recovery, and then turn on automatic saving node by node.

## Skip comparison: keep the original random timing

`SRW64_STATE_PROBE=1` Observe dialogue fragments, selections, original serialization and recovery boundaries synchronously in the game thread, and record key memory areas, RNG calls and return values. Observe that always flag `coverage_complete=false`; `compare_game_states.py` does not output local byte conformance as a full equivalent.

The vanilla RNG table is at `800D49E0`, indexed at `800D49D0`; combat and show reseeding also reads `8015DC50`, `80172D0C`. The main loop `80080838` advances the last two items each frame. New observations have been incorporated into both counts and cannot be dismissed as irrelevant display timings.

The first normal push/skip experiment differed by one initial seed before the skip occurred, and the difference in the entire RNG table cannot be attributed to the skip. To this add a silent-only, limited-duration, empty SRAM QA initial state alignment: `SRW64_STATE_FIXTURE` Only writes the RNG table, index, and two reseeding counts once at the specified first dialogue boundary. Only fixed addresses and lengths are allowed, all are verified before writing, and application records are retained; the status will not be rewritten by subsequent comparison nodes. Archives generated by the experiment are excluded from normal history recovery entry.

This facility is used to create identical test initial states, not save loaders or random rule modifications. These environment variables are not set during official operation, and the order of update and reseeding of the original version per frame remains unchanged. As a result, it is necessary to distinguish the initial state, subsequent dialogue nodes and combat coverage, and the dialogue experiment cannot be expanded to a full-on/full-off combat acceptance.

The results of the same binary and the same initial state fixture are stored in `paired-verification.json`: the first dialogue observation area is all consistent; the subsequent **5** matching nodes all have `battle_seed_clock` differences, and the remaining observed areas are consistent. For example, if the same `17410` subsequent fragment arrives at VI 3721 of normal advancement and VI 3601 of skipping, the reseeding count is different. According to the decision of this round of users, this original difference will be retained, **not mark the strict random state equivalence as passed, and no rule modification options will be added**. This experiment does not yet cover combat animation resolution.

## Verification entry

```sh
make check
make recomp-native-check
.venv/bin/python tools/content/compile_profile.py \
  --profile config/recomp/profiles/play-profile.json --language zh-Hans \
  --images original --output build/recomp/coverage-review
.venv/bin/python tools/recomp/analysis/compare_game_states.py LEFT.json RIGHT.json \
  --output build/recomp/state-comparison.json
```

Static/component inspection, window manipulation, map cold start and full gameplay equivalence are different acceptance levels. This record does not close the entire M0/M1.

In this round, `make check` means **129 items passed**; `make recomp-native-check` means **10 native component programs passed**. The final hotkey run still records the host exit code and 4/4 game thread recycling respectively, and does not replace the actual window check with component passing.