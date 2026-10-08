> **Language / Ngôn ngữ:** [English](native-playtest.en.md) · [Tiếng Việt](native-playtest.vi.md) · [中文](native-playtest.md)

# Native trial

Updated: 2026-09-18. Only supported on macOS (Apple Silicon, Metal). For build preparation, see [Native Development Guide](native-development.md).

## Start

First run `make` once in the warehouse directory (see [Native Development Guide](native-development.md#Building and Daily Checking)), then double-click `scripts/Play SRW64 Native.command`, or run in the terminal:

```sh
scripts/Play\ SRW64\ Native.command --language zh-Hans
```

The script is `tools/recomp/run/play_native.py --profile config/recomp/profiles/play-profile.json`, and the subsequent parameters are passed in as they are. The program will check the ROM and generated code identity, recompile the host if the source code changes, and then open the macOS Metal window. When there is no trial session (and no frozen backup), start a new game directly from the opening scene; later, automatically read the SRAM of the last normally exited and verifiable trial session, `--new-game` and start again. If there are already sessions but all cannot be verified, an error will be reported and stopped, and the game will not be quietly changed to a new game.

| Parameters | Function |
| --- | --- |
| `--language ja｜zh-Hans｜en` | Initial language; F7 cycles to switch in the game, the selection will be remembered |
| `--images original｜hd` | Initial screen; HD requires experimental materials in local `assets/`, F6 switch |
| `--rules original｜fixed｜all`, `--rule-fixes IDS` | Original rules, bug fixes (default for first time) or with difficulty adjustment; will be remembered, see [Optional Rule Fixes](../gameplay/rule-fixes.md) |
| `--upgrade-rules PATH` | For the rule file of modification increment, price and upper limit, see [Number of modification stages and upper limit](../gameplay/upgrade-limits.md) |
| `--resolution-scale 1..8` | Internal resolution multiple, font size and layout unchanged |
| `--mute` | Turn off sound |
| `--list-saves`, `--restore-session ID` | View or specify restored trial sessions |
| `--mini-stage FILE` | Replace the first episode with a self-made mini stage. Click "Enter Mini Stage" on the main menu or press F8 to access it directly. The default character initialization is automatically completed. See [Mini Stage](../script/mini-stage.md) |

`scripts/Play SRW64.command` (without `--profile`) is the early trial entry: the language directory and profile are not loaded, the archive history is in `build/recomp/play/`, and the first run relies on the developer's locally frozen first episode clearance file, and the new clone cannot be used directly.

## Button

Letter keys are mapped to physical keys. Release all keys when the window loses focus; system shortcuts with Command, Option, or Control are not carried into the game. Gamepads other than the keyboard have not yet been connected.

| Keyboard | N64 Input/Usage |
| --- | --- |
| Direction keys | Cross keys: cursor, menu; title ring menu to rotate left and right |
| Z | A: Confirm and advance dialogue |
| X | B: Cancel, return |
| Enter | START; Confirm title menu with Enter |
| Q / E | L / R; you can switch our aircraft on the map |
| Space | Z Trigger |
| I / K / J / L | C Up / Down / Left / Right |
| W / S / A / D | Analog stick up / down / left / right |
| F5 | Reload the dialogue text file (modifications in `build/recomp/profile-play/dialogue/<语言>/` overwrite the accompanying translations one by one, see [Line Text File](dialogue-text.md)); the application menu "Reload Lines" has the same effect |
| F6 | Switch Original/HD (requires local HD material) |
| F7 | Japanese → Chinese → English switches languages cyclically, no pop-up window, no restart |
| F8 | Enter the mini-level in the main menu with `--mini-stage` |
| Esc or window close button | Exit program |

Do not hold Enter until the startup screen appears: the original version will enter the Controller Pak management screen, in which `osPfsIsPlug` has not yet been implemented, and the host will abort.

Reading operations for plot dialogue and opening (see [Dialogue UI](../native/native-dialogue-ui.md) for details):

| Operations | Keyboard |
| --- | --- |
| Next reading page | Z |
| Automatic reading acceleration/deceleration (0 means manual) | ↑ / ↓ |
| Turn off automatic reading and cancel skipping | X |
| Press and hold to fast forward, release to stop | E + Z |
| Skip the current script segment; opening zoom text and route prologue are also applicable | E + Enter |
| Turn on/off replay; Replaying ↑↓ Scroll | Q |
| Text size 10–18 (default 13) | I/K |

## Native interface

- **Protagonist selection page**: The new game appears after skipping the public prologue, with four cards (super type/real type × male/female) side by side; ←→ switch, Enter/Z to confirm, or click on the card.
- **Confirmation page**: After selecting the protagonist, the names of the protagonist and partner are displayed. Enter/Z starts the story, and Esc returns to the casting selection. The name cannot be changed and is displayed according to the reading language. See [Protagonist Selection and Confirmation Page] (../native/native-name-entry.md).
- **Linkage page**: Appears when selecting "リンク" on the preparation screen. Transfer Pak and Link Battler cartridges are not required. Three work cards (ガンダムF91, ゴーショーグン, ザンボット3) are side by side, ←→ switch, space/Z or click the card to check, Enter to continue to the original linkage screen, Esc/X to return to the preparation menu. Checked works will be added as a special level before the next battle; already added works will be grayed out, and scheduled locks will be checked. See [Link Battler linkage](../gameplay/link-battler.md) §10.
- **Pre-battle confirmation page**: After selecting the weapon and target, the HP/EN, energy, weapon, final hit rate and critical hit rate of both sides will be displayed, as well as the single column weapon correction and the estimated damage including spirit, defense and shield. When the enemy attacks, you can choose counterattack weapons, evasion or defense; press the mouse or Tab button to select, Enter/Z to execute, and when your own party attacks, press Esc/X to return to target selection. The animation switches follow the original game settings. See [Pre-battle confirmation UI](../native/native-battle-ui.md).
- **Menu bar "Options"**: "Gameplay Adjustment" switches optional rules one by one. "Settings..." (⌘,) opens the settings window to switch rules, languages and screens. It will take effect immediately and be remembered. See [Settings Window] (../native/settings-window.md).
- **Prompt Bar**: After turning on the difficulty adjustment "Leading Refund", the plot will require the machine to refund its modification funds when it leaves the army. A prompt will be displayed at the top of the window for about 6 seconds, and a line will be left in the dialogue review. See [Optional Rule Fixes] (../gameplay/rule-fixes.md) §2.6.

## Archive

Save the game and then exit. Each run is written to a separate session directory (`build/recomp/profile-play/sessions/`), with subsequent runs filtering the most recent verifiable copy by ROM identity reported by the run, normal exit, and final summary; corrupted sessions report the cause and fallback to an earlier verifiable copy. Available `--list-saves` to view, `--restore-session SESSION_ID` to specify recovery. File integrity and in-game slot validity are judged separately, see [Save Recovery](native-save-recovery.md) for details. The window does not have an automatic exit time limit and the game will not operate automatically. The trial mode only retains the latest GPU screenshot and corresponding metadata, and audio and control diagnostics are saved in this subdirectory.

## Verification status

The current audio fix is that the verified device queue will not continue to accumulate in tested battles, and the actual speaker audio and video synchronization still requires manual listening. 2026-09-12 Restored from cold start of frozen playthrough to maintenance, checked the total round 7, funds 14,500 and Manami level 2 / SP 102/102; did not enter the second episode. 2026-09-18 Use [Debug Interface] (debug-interface.md) from the cold start driver to the male protagonist's route dialogue, and review the prologue skip, font size, fast forward and name page.