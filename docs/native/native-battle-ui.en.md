> **Language / Ngôn ngữ:** [English](native-battle-ui.en.md) · [Tiếng Việt](native-battle-ui.vi.md) · [中文](native-battle-ui.md)

# Confirm UI before battle

Date: 2026-09-20. The native profile run displays the SDL/RmlUi pre-battle confirmation page by default after selecting a weapon and target. Use the same page to choose to counterattack, evade, or defend when an enemy attacks. The scene is a self-made `battle-ui` mini-level, not an independent web prototype.

For actual attack/counterattack diagrams, design goals and functional requirements, please see [Pre-war UI Design Description](battle-ui-design-brief.md).

## Pages and operations

The cards of both sides are laid out along the original dark blue background and cyan right-angled border, and the battlefield map is retained. Refer to the screenshots of the aircraft combat Y provided by the user and adjust them to equal width, equal height, left and right mirroring; the enemy is on the left, we are on the right, the large images of the aircraft are facing each other, and the driver's avatar is not mirrored. The remaining HP/EN is green, the lost part is red, and the resource bar on the right is filled in reverse. Displays level, energy, SP, mental status, weapons and consumption, hit rate, critical hit rate, estimated damage, and the probability of both sides cutting down/shielding/cloning. **Weapon hit modifiers and critical hit modifiers are listed separately; these modifiers are already included in the final probability. ** When there is no counterattack weapon, the attack value of the party will not be displayed, and the same layout height will be retained.

- Our active attack: start combat, select weapons, spirit, return to target selection, combat animation switch. Selecting a weapon directly opens the original attack weapon list; the original version B only returns the selected target, so the adapter sequentially executes two entrances: the original confirmation return and the original target return.
- Enemy attack: select counterattack weapon, spirit, avoidance, defense, combat animation switch, and start the battle. After switching responses, re-post the snapshots of both parties, select the weapon to enter the original game weapon list, and then return to the new page.
- Mouse, ↑↓ or Tab selection button, Enter/Z to execute; Esc/X to return when our side actively attacks. Intercept the underlying game input during the modal period and wait for the key to be released after closing to avoid confirmation key penetration.
- The copywriting uses the existing Chinese/Japanese/English catalog, and the untranslated names of the aircraft, pilots and weapons are returned to Japanese; the dynamic protagonist names are expanded according to the existing names.
- The "Pre-war Confirmation Interface" of the settings page (the "Interface" page of the settings window) has three levels: **New version** (this page), **HD original** (redrawn with RmlUi according to the original layout), **Original** (the original game screen, text is translated as usual, and the window frame uses the original image), see [Three Interfaces](#三种界面2026-09-27). `battle_ui` (`native`/`hd`/`original`) saved to `presentation.json` will take effect after the next pre-war confirmation; the debugging interface is `settings {"battle_ui": ...}`. K/C▼ can be used to switch combat animations (`8015DDA8 & 4`) in all three gears, and the original A/B/menu processing remains unchanged.
- `SRW64_NATIVE_BATTLE_UI=0` forces the entire run to use the original confirmation interface; old entries that do not load the profile also retain the original interface. Script forced combat and AI vs. AI engagements do not pop up this page.

## Pre-war spirit use

Both attack and counterattack provide the mental selection page of our participating aircraft, including the commands and independent SP that the co-pilots have learned. The status grid summarizes the spirit that the machine has learned and is currently in effect: gray means it is not in effect, orange/green highlight means the actual effect bit is turned on; instant recovery commands such as root nature are not disguised as continuous buffs.

The learned quantity and command read driver `+0x0A`, `+0x0B`, the current/maximum SP is `+0x16/+0x18`, and the consumption reads ROM run table `80217F70`. If the original `801F18A0(handle,id)` is available, the list check is performed on the RAM copy and verified again after selection. Effective, insufficient SP and need to be used on the map are marked separately; commands that require map targets, self-destruction and resurrection still retain the map entrance and do not automatically specify objects for the user.

After selecting the available command, call the original `801D6A68`, and the original effect and performance process will be responsible for the spirit, HP, strength, number of actions and SP deduction (`801E195C`). Only intercept `801C8AB4` that returns to the map normally during this period of pre-war casting: restore the saved menu/cursor/battle table, re-call the original hit calculation and battle display cache, and then open the pre-war spirit page. No unit, driver, item, phase or RNG data is restored, so actual costs and effects are not undone upon return.

Esc closes the mental page and returns to the current battle; then Esc again cancels the original active attack. Evasion/Defense selections and current weapon are retained during cast; options with insufficient SP cannot be bypassed via old serial or repeated clicks. The background combat button is disabled when the spirit page is open, and the D-pad and Tab select between available commands and the back button.

## Data caliber

| Project | Source and Processing |
| --- | --- |
| Hit rate | The original game's calculated participation table `8018B6E8 + slot*0x5C + 0x12`, limited to 0–100; includes halving the evasion and mental effects of responding to instructions. The display caliber is consistent with the original game, and its random number endpoints are not reinterpreted. |
| Weapon hit correction | Runtime weapon record `+0x0A`, signed bytes; ROM table row `+4`. |
| Weapon critical hit correction | Runtime weapon record `+0x14`, signed byte; ROM table row `+13`. |
| Critical hit rate | Pure function recalculates the threshold of `801F47B0`. The own side is skill difference + weapon correction + base power; the enemy/third party is (skill difference + weapon correction) ÷ 4. The lower limit is 1, and then press the integer random number 0-99 to display the successful number: `clamp(ceil(threshold),0,100)`. 0 when blood/soul is in effect. |
| Estimated damage | Call `801F5628` in the complete RDRAM/context copy, select the non-critical/critical branch respectively; incorporate spirit, defense instructions, shields, and finally pass the hand addition/subtraction/survival limit of `801F5B78`. Random numbers are only fixed in isolated copies and do not consume real combat RNG. Shows the damage on hit without special avoidance, not the probability weighted average. |
| Cut off/Shield defense | The pilot skills, level, and machine equipment must all be met. Cut off also checks the opponent's current weapon `+4 & 8`; not guessing by weapon name. The chance is `ceil(level*100/16)` for ourselves and `ceil(level*100/32)` for the enemy/third party, capped at 100%. |
| Clone Category | 50% when the body's corresponding ability and the main pilot's strength are ≥130; the opponent will hit the target, causing the cut and clone to fail. Each probability is the conditional probability when reaching the defense judgment and cannot be added together. |
| Spirit and image | The spirit reads the main pilot status bit, and the name goes to the language directory; the first non-empty posture of the body and the driver's avatar are imported from the local ROM. 363 valid bindings and 361 avatar bindings among the 365 posture bindings have Python/C++ pixel consistency checks. |

A critical hit is the **conditional probability** after hitting. For example, if the enemy threshold is `21/4 = 5.25`, all integers from 0 to 5 are successful, and **6%** is displayed. It cannot be directly truncated to 5%. Weapon hit `+20` does not necessarily increase the final hit by 20 percentage points, since the terrain/size multiplier is then multiplied.

This page does not display pre-rolled critical hit marks or hit results, nor does it combine special defenses into "actual damage probability." The number of disguises is displayed in the ability area, and the secondary attack is not displayed separately. For formula research, see [Combat Calculation](../gameplay/battle-formulas.md).

## Shield caliber

`801F7204` of the current normal combat requires at least 5 EN after checking the attack weapon `+4 & 2` at the shield branch entrance and retaining the EN of the selected counter weapon. The four types of shields in this work pass through this entrance; the name containing "ビーム" does not mean that the weapon has this bit set. For example, the original attribute of the mini-level's ベガトロンビーム (678) is `0x40`, which will not trigger this branch.

- I Force Field 2000, Planetary Defense 2000, Beam Coating 1000, can be accumulated; if the damage does not exceed the intensity, it will be ineffective. If it exceeds, the intensity will be subtracted, and the minimum remaining value will be 10.
- The aura barrier is 3000 + the bonus of the holy warrior level table; if it does not exceed the threshold, it will be ineffective; if it exceeds the threshold, it will be fully penetrated without any subtraction.
- The defense command (participation table `+0x10 == 2`) will double the strength of the shield. This is not "Terrain 2."
- Successful neutralization/damage reduction consumes 5 EN; penetration of the aura barrier does not consume these 5 EN. After the shield reaction occurs, shield defense will no longer be assessed, including the aura barrier penetration branch.
- When the shield defense is successful, the damage ≥20 will be rounded to the nearest ten and halved according to the original version; the damage caused by the opponent's shield defense will be listed separately on the interface.

The above is composed of 616 sets of original settlement function comparisons covering four categories and combinations, beam mark presence/absence, EN 4/5 boundary, counterattack weapon EN reservation, defense command and damage threshold. The scope is ordinary combat in this work; it does not generally refer to all abilities called "shields" in other works.

## Access method

`battle_page.cpp` reads the participating parties in the game thread and publishes JSON snapshots; `frontend.cpp` reads only snapshots, sends semantic actions with serial to the adaptation layer, and does not read RDRAM. The original estimation function written in the preview copy will not enter the real battle situation.

The packaging of `801D5064` (main confirmation) and `801D5294` (enemy response) stays in the original input state. When the user confirms, the A/B edge and original menu options are only provided once to the original function. The original function continues to be responsible for weapon legality, pre-battle events and combat processes. The animation switch follows `8015DDA8 & 4` (set to indicate off).

Switching the language only updates the snapshot name; opening settings will not mix the new rules into already prepared combat snapshots. The next time the original game recalculates the battle, the current rules are used.

Source code:

- [`battle_page.cpp`](../../src/host/battle_page.cpp): state adaptation, original process call and input ownership.
- [`combat_preview.hpp`](../../src/host/combat_preview.hpp), [`critical_probability.hpp`](../../src/host/critical_probability.hpp): Preview and discrete critical hit probability.
- [`frontend.cpp`](../../src/native/ui/frontend.cpp): Shared RmlUi layout, operations and multilingualization.
- [`battle_ui_probe.hpp`](../../src/host/battle_ui_probe.hpp): Optional running probe, only executed when `SRW64_BATTLE_UI_PROBE=1`; the random number fixed value only acts on the isolated copy call of this thread.

## Mini-level verification and reproduction

**Current entrance: New native build → Main menu "Enter mini-level" (or F8) → Level is ready. ** Keep the native character/name adapter, automatically initialize with default route and name; do not use `--original-name-entry`, do not replay the old character selection script of fixed VI. Ordinary new games still display the native player and name page.

`Session.enter_mini_stage()` Check entry using `status`, `ui.click` and GPU screenshot. `status.mini_stage` provides available, entering, active, ready, waiting_reason; ready reuses the idle gate injected by the existing script at the game frame boundary: our stage, tactical map, no event/transition/defeat process being executed; `3D48` only closes the dialogue and does not mean that the map has received operations. Post-release confirmation edges are retried during menu fade-in until the game state leaves the main menu.

[`battle-ui.json`](../../config/recomp/mini-stages/battle-ui.json) Deploy four friendly units and three adjacent enemies. The original rules and all rules are modified to test both sides, 100%/5% HP, weapon correction -20/0/+20/+30, a total of **32 groups**; each group uses real `801F47B0` to exhaustively extract 100 random number values, a total of **3,200 times**. The displayed value of the hit estimate `80204254` and the actual calculated `801F4384` are also checked on a group-by-group basis.

Original rules, controlled data of our full health:

| Weapon correction (both items are set to this value at the same time) | Hit | Critical hit |
| ---: | ---: | ---: |
| −20 | 27 | 1% |
| 0 | 51 | 21% |
| +20 | 75 | 41% |
| +30 | 87 | 51% |

Local evidence directory: `build/recomp/mini-stage/battle-ui-final/`.

- `battle-ui-probe.json`: 32/32 consistent, the game logic area, combat table, CPU context and RNG remain unchanged, and the RNG of each group of copies remains unchanged. The comparison for the entire 8 MB block still logs false because there are other memory changes during the concurrent rendering job; it is not "full memory unchanged" proof.
- `ui-checks.json`: 11 interface operations passed, covering animation switching, avoidance recalculation, prohibition of counterattack, defense, return after original weapon selection, three languages and window sizes, closing after confirmation, and next engagement.
- `player-ui-checks.json`: On the active attack page, use Esc to return to the selected target, re-specify the target and restore the page, press and hold Z to confirm closing; `player-confirm.png` and `player-back-to-target.png` have GPU screenshots.
- `battle-zh-Hans.png`, `battle-en.png`, `battle-ja.png`: Real GPU screenshots, checking 960×720, 800×600, 1100×760 logical windows respectively; no buttons or text clipping are seen.
- After changing to Wire Claw in the first group of actual counterattacks, the weapon hit correction +30, critical hit correction +10, the final hit is 100%, and the critical hit is 26%. When choosing to avoid, the enemy hits 7→3, and our counterattack weapons are cleared.

```sh
# 构建并启动当前 native UI，通过调试接口从主菜单进入并检查战前页。
SRW64_BATTLE_UI_PROBE=1 .venv/bin/python tools/recomp/debug/check_battle_ui.py

# 手动试玩同一关卡：主菜单点“进入迷你关卡”或按 F8。
scripts/Play\ SRW64\ Native.command --new-game \
  --mini-stage config/recomp/mini-stages/battle-ui.json
```

The spirit display level is `config/recomp/mini-stages/battle-ui-spirits.json`, use real `3D55` to cast the spirit, including power improvement. New native entry evidence see `build/recomp/debug/20260920T150549.479573Z/`: `direct-entry.json`, `spirit-checks.json`, `mini-menu.png`, `spirits-player.png`, exit code 0. The previous `battle-ui-final` is historical evidence of early interactions and formulas and is no longer used as an acceptance entry for the current startup process.

Component verification: `make recomp-native-check` (including ASan/UBSan critical integer domain exhaustion) passed; `make check` 262 tests (11 of which were skipped) passed, dependency check passed; graphics host build passed. These evidences cover the normal combat process in this mini-level, and do not mean the return of the full plot, all special weapons and scripted battles.

Acceptance record of current main menu entry and pre-war UI: `build/recomp/debug/20260920T151636.072446Z/`, exit code 0.

- `direct-entry.json`: The native character page is not displayed, and the map input is sent after mini-levels `ready=true` and `waiting_reason=""`.
- `ui-checks.json`: 13 passes, including both sides image/defense fields, non-beam markers not accidentally triggering aura barriers, as well as counter, weapon swap, language/window, and continuous engagement.
- `battle-ui-probe.json`: 32 groups of hits/crits, 24 groups of cuts/shield defense/clone, and 616 groups of shield controls all passed; the isolation test kept the game logic and RNG unchanged.
- `battle-zh-Hans.png`, `battle-en.png`, `battle-ja.png`: current native GPU screenshots, retaining the battlefield map.
- `make check`: 262 passed (11 skipped); ASan/UBSan component checks passed for names, mini-level readiness gates, battle preview.
- standalone importer CTest 6/6 passed, the real ROM oracle covers all valid body/avatar pixels. This demonstrates asset import consistency and does not replace a full trial of the standalone release package.

Current acceptance for mental and active attacks: `build/recomp/debug/20260920T151928.251713Z/`, 6 checks passed, exit code 0. The spirit of both sides is truly released, 100% sure hit, 0% critical hit during hot blood, 50% clone after 130 strength, and Esc to return to target selection, re-specify the target, and keyboard confirmation are all passed; `spirits-player.png` is a screenshot of the current native GPU. Can be reproduced using `.venv/bin/python tools/recomp/debug/check_battle_spirits.py`.

## Not full HP/EN verification (2026-09-21)

`battle-ui-resources.json` Use the original script to cast Must Hit/Iron Wall at the beginning, allowing both sides to actually fight and survive. Our side chooses the オーラzanり which consumes 10 EN; after entering the enemy stage, the next native pre-battle page reads the results: enemy HP 3000→1941, our HP 2800→1562, EN 80→70, the upper limit remains unchanged, which is consistent with the first round damage of 1059/1238 and EN consumption of 10 respectively.

Evidence directory `build/recomp/debug/20260921T011025.169262Z/`: `resource-before.json`, `resource-bars.json` (status and ui.tree actual layout size), `resource-checks.json` (6 passes), `resource-partial.png` (GPU screenshot), normal exit code 0. There is no direct modification of HP/EN or injection of display data.

The numerical values are displayed as actual integers; long press the current bar to round down the integer percentage. The actual measured enemy HP is 64%, our HP is 55%, and our EN is 87%. So the bar length of 70/80 is 87%, not exactly 87.5%; this is a bar accuracy limit, not a resource value that is not updated. Boundary screens with 0 EN or extremely low HP are not covered this time.

## Ability effects and base strength of both parties (2026-09-21)

A new scrollable "Ability Effect" area has been added to both sides' cards, which reads actual pilot skills, skill levels, current HP and machine capabilities. The correction value is a formula item that has been included in the hit/critical hit estimate and will not be superimposed again; final coverage such as sure hit, sure dodge, etc. will still take priority. If the skill exists but does not meet the conditions this time, keep the entry and explain the reason.

| Ability | Demonstration caliber |
| --- | --- |
| New Humanity/Enhanced Human World | Skill level, hit and avoidance corrections. The original calculation is processed according to the same skill mark group, and there is no repeated superposition. |
| Base power | Level, whether it takes effect, current hit/avoidance/crit correction, and the HP activation threshold of this level. **This game does not add armor**. The enemy/third party does not add base power to critical hits; our team is also reminded that critical hits cannot be made during the period of blood/soul. |
| Holy Warrior | Avoidance correction; the original hit calculation does not include a call for the attacking Holy Warrior to add hit points. Level also affects the strength of the aura barrier. |
| Super Powers | Hit and avoid corrections. |
| Cut off/Shield defense | Respective skill level, probability of this time, and reasons such as no equipment, insufficient level, weapons that cannot be cut off, must hit or shield priority. |
| Clone machine-like abilities | Clone, Mach Special, True Mach Special, God's Clone, Getta Phantom, Instant Phantom Foot, Super Disruptor, display their respective names and the probability/reason for not being activated. |
| Shield | Aura barrier, I force field, beam coating, planetary defense, respectively listed in basic strength and current status. The final combination strength, defense command and EN consumption are still handled by the shield calculation above. |
| Other special defenses | The number of remaining times of the dummy; the fixed damage armor of a specific body. The fake body is not converted into probability, nor does it turn conditional damage into probability-weighted damage. |

Under the current default modification rules, base power L4 takes effect when **HP < 40%**. 1050/3000 (35%) corresponds to the base value of ROM table 10: hit +5, avoidance +5, friendly critical hit +10; exactly 40% does not take effect. The lower the HP, the higher it is by pressing subsequent gears. When the gear correction is turned off, the original version is advanced by one gear as a whole; when the halving correction is turned off, the hit/avoidance uses the full base value, and the critical hit remains unchanged. The interface follows the rules set when the battle is opened.

The mechanism is based on the local original function and ROM table: hit call chain around `801F45C4`, base power `801E1D64`/`80217F90`, new human `801E1EDC`, holy warrior `801E1F08`, super power `801E1F10`, and critical hit `801F47B0`. The empty function of the original holy warrior/superpower retains the caller's skill mask, and actually gets avoidance +32 and hit/evasion +64; the values ​​are calculated according to the level table after level correction is enabled. There is no misinterpretation of an empty function as zero addition.

Added [`battle_effects.hpp`](../../src/host/battle_effects.hpp) unified generation capability field. The isolation operation probe covers **2,400 groups**: 4 base power correction combinations × 5 skills × 4 levels × 10 HP boundary values ​​× 3 camps. When compared with the results of the original function/current rule hook one by one, all are consistent; the original 32 groups of hit/crit, 24 groups of defense probability, and 616 groups of shields also all passed. Game logic and RNG are not changed by probes; no claims are made that full memory is unchanged during concurrent rendering.

The new level [`battle-ui-skills.json`](../../config/recomp/mini-stages/battle-ui-skills.json) uses explicit `initial_resources` to set the HP/EN of the real unit once when the map is ready for the first time, which is used to stably reproduce the base power and resource bar. This field only accepts factions, deployment slots, and bounded percentages; it is not written to any address, nor does it modify the display snapshot. This set of controlled initial states is recorded separately from the above evidence of blood loss/EN consumption in actual battles.

```sh
SRW64_BATTLE_UI_PROBE=1 .venv/bin/python tools/recomp/debug/check_battle_skills.py
```

Current native evidence directory: `build/recomp/debug/20260921T012634.998258Z/`, normal exit code 0. `skill-checks.json` 15 passes, including both sides' base/superpowers, equipment restrictions, visible text and button borders in three languages, GPU red pixel checks for loss of four HP/EN bars, and primitive function probes. `skill-zh-Hans.png`, `skill-en.png`, `skill-ja.png` are 960×720, 800×600, 1100×760 logical window screenshots respectively. They have been manually viewed. The battlefield map and confirmation menu are still visible.

Build, rules and mini-levels ASan/UBSan checks passed; `make check` 263 items passed (11 skipped), dependency checks passed. There are special tests for resource setting boundary rejection and only initialization once behavior. These verifications do not replace the return of full story special battles.

The saved script starts again from a new build and goes directly to the mini-level, with the evidence directory `build/recomp/debug/20260921T013311.920719Z/`: all 15 items passed; not just attached to the open pre-war page. Exit code 0.

## Weapon replacement, pre-war spirit and mirror layout acceptance (2026-09-21)

Current native build evidence directory: `build/recomp/debug/20260921T041103.588214Z/`, binary SHA-256 `e9e907b530dc90942cee1acbcc8c3b3b0b282f0314515002e5f45a3c2aeab01e`. Enter `battle-ui-skills` directly from the main menu; `action-checks.json` 23 items passed, and the final exit code was 0.

- Active attack: Weapon 677→678, enter the original weapon list, re-specify the target, and then return to the native confirmation page and actually engage in combat. The bridge calls the original confirmation cancellation and target cancellation `801D3010`, retaining the original weapon legality check.
- Attack spirit: guaranteed hit SP 83→58, hit 100%, repeated casting is disabled; big root SP 58→18, HP 1050→3000, base power becomes unactivated with recovery; hot blood is disabled due to insufficient SP.
- Counterattack spirit: Xiang uses acceleration SP 62→52, retains the counterattack weapon, and the co-pilot SP 32 remains unchanged. In the next battle, Wan Zhang chooses to evade first, and then uses the must-dodge SP 18→3; the evasion selection and non-counterattack weapon status are retained, and the enemy's hit rate becomes 0%.
- Counterattack and change weapons: Keep the necessary dodge and remaining SP, reselect a legal weapon and resume counterattack. The first weapon is out of range and is correctly rejected by the original list; this round of inspection sends `down,a` through the debugging interface to select the second weapon. The saved script already contains the option not to treat the first rejected confirmation as a success.
- Mental menu Tab focus cycle and Esc return are passed; the gray inactive/highlighted mental grid, equal-width and equal-height cards in three languages and the boundary of the confirmation area are passed. `actions-zh-Hans.png`, `actions-en.png`, `actions-ja.png`, `spirits-menu.png`, `counter-flash.png`, `counter-ready.png` are actual GPU screenshots.
- The original function isolation probe’s 32 sets of hits/crits, 24 sets of special defense, 616 sets of shields, and 2,400 sets of ability corrections have all passed without changing the actual gameplay/RNG.

`make host recomp-native-check` (including ASan/UBSan) passed; the final keyboard focus correction was built again and the above running verification was completed. `make check` 263 items (11 skipped) passed. Recurrence entry: `SRW64_BATTLE_UI_PROBE=1 .venv/bin/python tools/recomp/debug/check_battle_actions.py`.

Also logged is a non-final acceptance session `20260921T040904.424564Z` Cocoa crash on shutdown (exit code -11): diagnostic `srw64-gfx-host-2026-09-21-121108.ips`, asynchronous block with stack at `CocoaWindow::updateWindowAttributesInternal`, access to invalid object during `SDL_Quit`. The window destruction path has not been modified in this round; in the end, the complete combat session exited normally, and we do not claim that the intermittent exit problem has been fixed.

## Open partition layout (2026-09-21)

The pre-war page of `frontend.cpp` is rearranged according to the 1b plan selected by Claude Design project "Battle Preview" (`BattleOpen.dc.html`, 1920×1080 canvas is converted to dp at 0.5); the snapshot fields, original process calls and data caliber are unchanged.

- **Three rows and three columns. ** The top is the banner of both sides' aircraft (unit name, first/secondary label, weapon, mirror image HP/EN, consumption and weapon correction); the two sides of the middle section are large pictures of the opposing aircraft. The central collision area is juxtaposed with the large numbers of "hit damage" of both sides, the first mover arrow, as well as the hit rate/critical hit rate comparison line and critical hit damage/damage during shield defense/shield details; both sides of the bottom are the driver's panel (avatar, level, strength, SP, mental status grid, cut/shield defense/clone and ability effects), and the center is the operation area. The enemy is pink `#ff6fa8`, our team is cyan `#3fd0ff`, and the main value is gold `#ffd75e`.
- **The description of conditional damage is close to the numerical value. ** "Damage on hit" is marked directly under the big number; the non-attacking side all displays "-", and the position of each row remains unchanged.
- **Coping with segmented controls. ** When the enemy attacks, "Counterattack | Avoidance | Defense" is displayed. The current response is highlighted and displayed repeatedly below the collision area and on our banner label. The "Counterattack" section sends a new action `counter`: only when it is currently avoiding/defending, it will be converted to the original weapon list (the same path as `weapon`, and the original legality check will be used). There is no operation when it is already counterattacking.
- **Input binding (consistent with the game key table, the keyboard/controller is the same set). ** Directional keys/WASD (cross keys/left joystick) move the focus, Z/Enter (A/START) executes the focus item, X/Esc (B) returns, Q (L) selects weapons, E (R) spirit, K (C▼) combat animation; Tab/Shift+Tab can still cycle. The original Space/W/G/A hotkeys have been removed (W, A conflict with the joystick keys). The keyboard uses `frontend.cpp`'s `dispatch()`, the controller uses `graphics.cpp` and the newly added SDL GameController maps it to the same N64 key mask (available in all games). The page uses `srw64_pad_state()` to take the rising edge, and the two are merged into the same `battle_buttons()`. The controller path has not been tested with a physical controller; the linkage page, name page, and inter-field page have not yet been connected to the controller.
- **Spirit page. ** Changed to a line list: name, SP consumption, driver and SP, status; effective commands are highlighted in gold.
- **Differences from the design draft. ** RmlUi None `clip-path`/`filter`/CSS grid: The beveled edges are changed to right-angled borders, the body light and map blur are omitted, and only the translucent darkening and left and right camp color gradients are retained. The mental state grid retains the complete name instead of single words to meet the requirements of the English interface and "not just relying on color expression". The weapon submenu with weapon-by-weapon estimation in the design draft has not been implemented, and the selected weapon still enters the original game weapon list. The weapon category label (Fighting/Shooting) is not in the snapshot and is not displayed.
- ** Move and avoid/defend switch keys by row (2026-10-04). ** The user requested that there be a key to directly switch defense/evasion (refer to modern machine combat), and that pressing the counterattack/evasion/defense row directly returns to the start of attack. The direction keys no longer press one line to cycle, but press three to walk: start attack | counterattack, avoidance, defense (when the enemy attacks) | change weapons, spirit, animation, and return. Wrap up and down, do not wrap around, move left and right within the line; press up to return to the starting attack from any item in the response line, press to enter the response line and fall on the currently selected item. Tab/Shift+Tab still traverses all buttons in the original order, and the mental page is still linear. C◀ (Deck's The bottom prompts that when the enemy attacks, there is one more `{CLeft}` avoidance/defense (entry `battle_guard_switch`, registered `UI_KEYS`). When redrawing the page in the same battle (pressing the controller for the first time, prompting to change to the controller icon, changing language, changing window), the focus remains on the original button; it would have been reset to start attacking before, so the first arrow key pressed when switching from the keyboard to the controller will be lost. It still returns to the default button when engaging in a new battle, changing the response, or switching the spirit page. The high-definition original version and touch screen layout remain unchanged. Actual machine: `check_battle_actions.py` Added `rows-*` (handle direction keys) and `guard-switch-*` (handle X, keyboard J) checks on the enemy attack page. On 2026-10-04, all 32 items passed, and the host exit code was 0.
- **Check script. ** `battle-card-left/right` now refers to the top banner, and `battle-pilot-left/right` is added; the mirror check of `check_battle_actions.py` covers both at the same time, and the resource bar positioning of `check_battle_skills.py` is changed to the order of "key | bar | value".

- **Description text. ** The four translucent caliber descriptions (damage/crit/defense/correction) originally centered in the center have been removed from the page; labels such as "damage on hit" are directly pasted next to the values. The corresponding language key remains unchanged.

- **Text streamlined (after user review). ** "Combat Preparation" is no longer displayed at the top; the small words "Who → Who" above the large damage numbers are removed; the words "Weapon Correction" are removed from the banner consumption line; "Hit/Evasion/Crit Correction" in three languages ​​is shortened to "Hit/Evasion/Crit"; the ability line is compressed into one line (only the reason is written when it is not effective, and the HP threshold is written at the bottom), and there is no longer the "Ability Effect" title. Cut/Shield Defense/Clone only displays the items that the body actually has (no equipment or skills are missing), the clone category uses the body's own ability name, and the two rows of fixed heights are left blank; these three categories are no longer repeated in the ability list. The fake body is displayed as "Fake Body × N", which is only displayed when the remaining times are greater than 0.
- **Subsequent fine-tuning. ** The hit rate/crit rate label block is widened (the Japanese "クリティカル Rate" is no longer full); the detail label column is widened (the English "Damage if target shields" does not wrap); the shield row only displays "Original Damage → Actual Damage" when invalidating/reducing damage, not applicable/EN is insufficient/penetration only displays status; the ability effect area is increased to 108dp, scroll bars no longer appear on common content.

- **Beveled Edges and Stages Tab (2026-09-26, after user review). ** Retain the hypotenuse according to the design draft: Add RmlUi custom decorator `slant` ([`slant_decorator.hpp`](../../src/native/ui/slant_decorator.hpp), `decorator:slant(填充 边色 边宽 顶条 左上 右上 左下 右下)`, four lengths of horizontal indentation of each corner, pure geometry, outer edge feathering of 1 px, the element itself no longer has a background and border). The inner side of the banner, the central collision area (lower narrow trapezoid), the hit rate/critical hit rate row (parallelogram) and its label (trapezoid), and the start combat button (lower wide trapezoid) are all drawn with it; the pilot panel is kept at right angles according to the design draft. The "Enemy Attack | Our Attack" two-frame tab of the design draft is restored in the center of the top, and the current stage is highlighted according to the camp color (entries `battle_phase_enemy`/`battle_phase_player`, `UI_KEYS` are synchronized). The large image of the aircraft is first alpha-cropped to actual pixels (`rect` attribute), and then enlarged according to the remaining height between the column width and the banner/pilot panel, up to 6 times; the snapshot stamp is added to the window size, and rearranged after changing the window. The overall font size of the pilot area has been increased (name 17, strength/SP 13, mental grid and ability line 12, cut/shield defense/clone 13), and the mental grid area 46dp can accommodate two lines. The driver's avatar is 96dp (originally 62dp, 2026-09-26 user requested a larger size), which is the same height as the three lines of name, strength/SP, and spirit. The large picture of the body is taken from the entire HD pose (`docs/design/unit-pose-hd.md`) in HD mode. The upper limit of enlargement is calculated based on ROM pixels. The picture is not resampled, and the boundary only counts pixels with alpha ≥ 16. The original/new version switching ("Pre-war Confirmation Interface" on the settings page) and the K/C▼ animation switch on the original interface remain unchanged, and `check_battle_ui_switch.py` 6 items passed.
- **The small screen and pilot panel are left blank (2026-09-28, Steam Deck). ** Interface size (the "Interface" page of the settings window, Deck is extra large by default, see [Settings Window](settings-window.md#界面大小)) After enlargement, the page is only about 864×540 dp. When the page width is less than 1000 dp, add `narrow`: avatar 64 dp, button inner margin becomes smaller, power/SP does not break lines, small text is enlarged (first-last label 10, consumption line 11, collision area description and details 11, first mover arrow 10). The bottom prompt uses key symbols instead (`{A}``{L}``{R}``{Anim}``{B}`). The keyboard displays the bound keys and the handle displays the icon. The pilot panel originally had two rows for mental grid (46 dp), one row for cut/shield defense/clone (18 dp), and about two and a half rows for abilities (44 dp), which were empty without content; users can view the Deck The screenshot asks why so many are left - now keep the number required by both sides in this battle (`PilotRoom`): the number of mental grid rows is calculated based on the labels on both sides, whichever is larger. The cut/shield defense/clone row is only retained when either side **owns** the ability (whether it is applicable based on ownership rather than the current weapon, and the weapon change page does not jump). The ability row is based on the number on both sides, whichever is larger; both sides are still of equal height, and the dividing lines are aligned. The estimated remaining height (original `logical_h-436`) is no longer used for large body pictures. After typesetting, the actual height of the middle row `battle-mid` is measured and then resized (`battle_fit_units`, the upper limit is still 360 dp, 6 times ROM pixels). The figure of the aircraft in the same scene is about 60% higher when the deck is extra large. `check_battle_ui.py` 13 passes.

Run acceptance (same build, directly into the mini-level):

| Script | Results | Evidence Directory `build/recomp/debug/` |
| --- | --- | --- |
| `check_battle_actions.py` | 25 passes, exit code 0 | `20260921T111932.966579Z` |
| `check_battle_skills.py` | 15 passes (three languages/windows, four resource bar red pixels, 2,400 sets of capability probes) | `20260921T111719.596115Z` |
| `check_battle_ui.py` | 13 passes | `20260921T112117.478933Z` |
| `check_battle_spirits.py` | 6 passes, exit code 0 | `20260921T111816.467122Z` |

`check_battle_spirits.py` The original keyboard layer takes 100 ms to click. Occasional key loss occurs when the map menu is expanded (recurred in both old and new entry paths). It has been changed to the same handle layer as other scripts `buttons` (timed by VI); the counterattack section of `check_battle_actions.py` is branched according to the actual defender (direct entry changes the RNG Status, see [Mini Level](../script/mini-stage.md)). An earlier run of `20260921T071023.404326Z` passed all checks, but the intermittent Cocoa exit crash (-11) recorded above occurred when closing. After that, each run exited normally. `make check` is not running this round.

## Three interfaces (2026-09-27)

User 2026-09-27 requested that the pre-war confirmation interface has three levels: our revised version/HD version/original version. The meaning confirmed by the user: "HD" is redone one-to-one using RmlUi according to the layout and color matching of the original version; "Original" is the original screen drawn by the game itself, the text is still translated according to the reading language, and only the pictures are replaced with the original ones.

| File | `battle_ui` | Screen | Operation |
| --- | --- | --- | --- |
| New version | `native` | Modern page of previous sections in this article | Previous sections in this article |
| High-definition original | `hd` | RmlUi redraws according to the original 320×240 coordinates, zooming to the 4:3 screen in the window, the method is the same as the inter-field screen | Same as the original: A starts, B returns to select the target; when the enemy attacks, there is a four-item menu, and B opens the weapon list. K／C▼ Cut animation |
| Original | `original` | Original game screen; window frame 1196/1197 uses the original image, text is processed according to the original image mode | Original; plus K/C▼ cut animation |

**Setup and Migration. ** `settings::battle_ui()` changed from bool to enumeration `BattleUi {Native,HD,Original}`, [`presentation_settings.hpp`](../../src/host/presentation_settings.hpp). The meanings of `native` and `original` in the old `presentation.json` remain unchanged and will be used directly; unrecognized values ​​are treated as `native`. When the old version of the program reads `hd`, it will also be regarded as the new version. The launcher (`launch.cpp`) transcribes this value unchanged. Both the debug interface and MCP's `battle_ui` accept `native`/`hd`/`original`. The setting row is placed on the "Interface" page according to the paging method of the setting window. The entry `settings_battle_ui_{native,hd,original,note}` is complete in three languages ​​and has been registered in `UI_KEYS`.

### Original screen (static analysis)

The basis is the disassembly of `801D4CCC`, `801D4660`, `801E7A28`, `801D51A8`; the coordinates are all 320×240. The original screen does not have avatars, body pictures, damage, critical hits and spirits.

- **Build and Step**:
- Call `801D4CCC(arg)` once when entering to create the screen: arg 0 is our attack, arg 2 is the enemy's attack, arg 1 is the refresh after selecting avoidance/defense.
- Window is layout `0x45` (box 1196, gallery 1295, palette 1297, streamer 1017), with sprite slot 0x2E.
- `801D4660` draws two panels; for arg 2, the menu is created by `801D51A8` (layout `0x46`, box 1197).
- The step function `801D5064`/`801D5294` only processes input and does not draw anything.
- **Left and Right**: Our team is always on the right (panel 0 of `801E7A28`, text x=168), and the enemy is on the left (panel 1, x=24).
- **Panel**: The inner bottom of the left panel (21,21)–(155,139), RGBA (0,0,32,0xC0); the blue line of the outer frame is at x=19/156, y=19/140, and the inner dark line (16,16,32); y=51/52 is the dividing line. The right panel is shifted 144 to the right as a whole.
- **HP／EN**：
- "HP", "EN" and slashes are yellow and white characters in the block diagram.
- Number walking number pool (8×8, white letters and gray shading). HP uses `%5d`, the current value is at (53,26), and the upper limit is at (102,26); EN uses `%3d`, at (53,39)/(86,39).
- Display `?????`/`???` when the enemy is unknown. Judgment conditions: Our side or the aircraft +0x38 bit 0x40 of pilot byte 0 has been set.
- Health bar at (52,35), 88×2; EN bar at (112,42), 28×2. Always draw the entire red line first, then press `trunc(值×宽／上限)` to stack green; also draw when the enemy is unknown.
- **Text Lines** (ROM characters 14 high, line spacing 16):

| Location (left panel) | Content |
| --- | --- |
| (24,56) | Aircraft name (record 527 + aircraft number) |
| (24,72); (112,72); (137,72) | Driver name (4382+); "レベル" 898; Level `%2d`, unknown is `??` |
| (24,88) | Weapon name (1370+). If there is no weapon, write 1109 and counterattack is not possible; if the defender chooses avoidance/defense, write 927 avoidance/890 defense |
| (24,104); (56,104) | 「気力」908; Strength `%3d` |
| (24,122); (72,122) | "Hit rate %" 1014; hit `%3d` (battle table +0x12, limited to 0–100), no weapon written `---` |

- **Enemy Attack Menu**:
- Insole (125,149)–(195,219).
- The four items are Counterattack Start 1015, Weapon 1016, Avoidance 927, Defense 1017, located at (128,152+16n).
- The cursor is a 71×17 translucent green block starting from (124,150+16·sel); the option exists `80227A81`, looping up and down.
- A selects counterattack to start the battle, select a weapon or press B to open the weapon list. Selecting avoidance/defense will be recalculated with weapon 0, then refreshed with `801D4CCC(1)`, and the cursor will return to the first item.
- **Our Attack**: Only two panels. Our phase B returns to target selection; when it is not our phase or it is a forced battle, it will start automatically after about 61 steps.

Actual machine reference screenshots (pure original version, 3 times): Main checkout `build/recomp/mini-stage/duel-3/present-2311.png` (our attack), `build/recomp/mini-stage/rules-battle-1/present-3540.png` (enemy attack menu, the enemy on the left is unknown). Screenshots under `build/` may be cleaned at any time.

### HD original version

Source code: `battle_hd_page`/`battle_hd_buttons` of [`frontend.cpp`](../../src/native/ui/frontend.cpp), CSS is `.bh-*`.

- **Data**:
- Take the same set of snapshots and actions ([`battle_page.cpp`](../../src/host/battle_page.cpp)) on the new page. Note the `style` of the snapshot at the opening position.
- Add three more items: `words` (the records in the above table are `dialogue::ui_text` to get the text of the reading language, which has the same origin as the text overlay of the original screen), `known`/`level_known` of each party, and the `???` judgment above.
- The original screen is cleared by `8009DB8C` (same as the new page), and the map is displayed as usual without being darkened.
- **Typesetting**:
- All positions are as shown in the table above, the proportion u=min (window width/320, window height/240). The border width is one native pixel and at least one screen pixel wide.
- The text is aligned to the left at the starting point of the original grid, and the right-aligned value is aligned to the right end of the original grid.
- ROM kana is half-width, and the font is full-width, so a line that is too long is first compressed horizontally (70% for Chinese and Japanese, 80% for English, the same as `ui_text.cpp`), and then the font size is reduced if it cannot fit.
- "Hit rate %" is split according to the position of two or more consecutive spaces in the translation, and the numbers are put into the blank spaces, so the word order of the translation is not affected.
- The values in the digital pool are in regular font size 10.5, with white text plus a gray shadow of the original pixel.
- The position of "レベル" has been moved forward from 112 to right-aligned 135, leaving a little more width for the driver's name.
- **Operation** (`battle_hd_buttons`, shared by keyboard and controller):
- A/START: Start the battle when our team attacks; execute the item where the cursor is when the enemy attacks.
- B: Return to target selection when we attack (only `can_cancel`); open the weapon list when the enemy attacks, consistent with the original version.
- Up and down (left and right, rocker can also be used): Move the menu cursor in a circular manner.
- K／C▼: Switch animation. The small label at the bottom is the same as on the original screen.
- There are no shortcut keys for spirit and weapon changing, and they are not available on the original screen.
- Menu items can be clicked with the mouse.
- When the same battle is redrawn, the cursor remains in the same place; for new battles, and refreshes after avoidance/defense, the cursor returns to the first item (the same is true for the original version).
- **Differences from the original version**:
- The streamer of the frame line is not done, and a static base color is used; the frame angle is a right angle.
- When it is not our phase, it will not start automatically after about 61 steps. Just like the new page, you have to press A.
- Forced combat and AI vs. AI still have vanilla graphics (`step` is returned before gear is judged).

### Original original picture

- **Window box**: `native_map.cpp` Added `set_original_frames` hook (`srw64-frame-host` does not link to `battle_page`, so use the hook instead of calling it directly), install `battle_page::configure`. When the gear is original, frame 1196/1197 will not be redrawn in HD, even if the picture mode is HD. These two frames are only used by this screen, so they are judged by the scene number and no timing is required.
- **Text**: `battle_page::original_screen()` is true within 3 VIs of each frame step of the original confirmation screen (forced combat also counts) or 1196/1197 drawn. `ui_text.cpp` At this time, it is processed according to the original image mode: Chinese and English are translated and drawn natively as usual, and Japanese is the original ROM character.
- **STATUS**: `status.battle_page.original_images` reflects this status.
- If the text in the first frame is drawn before the frame and step, there may be one frame of Japanese text with high-definition text, which has not been confirmed on the actual machine.

### Verify

[`check_battle_ui_switch.py`](../../tools/recomp/debug/check_battle_ui_switch.py) has been expanded to three levels:
- Original version: no native page, `original_images` is true, C▼ cuts animation, and restores after exiting;
- New version: C▼ cut animation;
- High-definition original: C▼ cuts animation, B returns, A starts combat; after the round ends, the enemy attacks, check the menu cursor is initially at the start of counterattack, go down three times to defense, select defense and then the panel refreshes (`response`=2, weapon −1) and the cursor returns to the first item, B opens the weapon table, selects the weapon and returns to the high-definition original page;
- Check settings persistence for each gear.

The screenshots are stored in the running directory: `original-confirm.png`, `native-confirm.png`, `hd-confirm.png`, `hd-menu.png`, `hd-defend.png`, `hd-counter.png`.

**Not yet running on real machine** (it takes several minutes to run the native host, and it will compete with other sessions to build). Now only the `-fsyntax-only` compilation check is done on the changed files in the main checkout build configuration.