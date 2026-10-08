> **Language / Ngôn ngữ:** [English](rule-fixes.en.md) · [Tiếng Việt](rule-fixes.vi.md) · [中文](rule-fixes.md)

# Optional rules: corrections and difficulty adjustments

Date: 2026-09-17 (2026-09-18 adds real-time switching to the menu bar, turns on the correction category by default in the trial, adds difficulty adjustments to the boss avatar and the upper limit of transformation, adds the power of Holy Warrior Aura's weapon, and adds refunds for leaving the team). BUG01–04 and BUG08 corresponding to [Original Bug Registration](original-bug-register.md); BUG05 (Five Flying False Body) has been set as [Basic Repair](base-fixes.md) that takes effect by default and has no switch, and is not on this page. A total of seven independent switches have been corrected (the weapon inheritance of BUG08 has not been verified in real-time), and there are also several difficulty adjustments (see §1 table); **When the trial entrance is launched for the first time, all corrections are turned on and difficulty adjustments are turned off by default**. When any one is turned off, the host only calls the original function, and the behavior is consistent with the original version.

## 1. Use

Default: `scripts/Play SRW64 Native.command` When first started, **Correction is fully on and difficulty adjustment is fully off**. There are two entrances when the game is running. They share the same settings and synchronize with each other in real time:

- Menu bar **"Options → Gameplay Adjustment"**: "Modification" and "Difficulty Adjustment" two sets of check options (the group name is a non-clickable title), below are the three defaults of "Restore Default (Modification On, Difficulty Off)", "All Off (Original Rules)" and "All On".
- **"Options → Settings..." (⌘,)**: Settings window, including the same rule switches and three presets, as well as language (ja/zh-Hans/en) and screen (Original/HD). The game cannot receive keyboard input while the window is open, and it will not resume until all keys are released after closing.

Changes take effect immediately and settings are written back. The titles of menus and windows follow the current language, and the new language will be used immediately after F7 or switching languages ​​in the window.

You can also select at startup:

```sh
./Play\ SRW64\ Native.command --rules fixed          # 全部修正（难度调整仍关闭）
./Play\ SRW64\ Native.command --rules all            # 修正 + 难度调整
./Play\ SRW64\ Native.command --rules original       # 原版规则
./Play\ SRW64\ Native.command --rule-fixes esp-level,limit-cap   # 自选
./Play\ SRW64\ Native.command --rule-fixes ''        # 自选为空，等同 original
```

| ID | Content |
| --- | --- |
| `esp-level` | Super power hit/avoidance correction is based on skill level, the original version is fixed at 64 |
| `seisenshi-level` | Holy warrior's avoidance correction is based on skill level, the original version is fixed at 32 |
| `limit-cap` | The sum of the driver's hit/avoidance and the body's mobility does not exceed the body's limits. The original version has no limit |
| `potential-bands` | The base power is aligned according to the HP level: there is no bonus above 90%, and it reaches the highest level when it is below 10%; the original version is one level ahead of schedule |
| `potential-half` | The base hit/avoidance correction is halved, and the critical hit rate remains unchanged |
| `weapon-inherit-map` | Three missing weapons were added to the inheritance when changing the machine: the fire emitter of the レイズナー and the グレネードランチャー, アルトロンドラゴンファイヤー (for reasons and basis, please see [Transformation Inheritance Analysis](upgrade-inheritance.md); it has not yet been verified on the actual machine) |
| `aura-slash-power` | Holy Warrior: The ハイパーオーラ series weapons unlocked at L3 increase in power by +200...+1500 according to skill level (the original version is completely missing), see §2.2 |

The above six items are **Correction**: the original code is inconsistent with its own data or interface caliber, it is enabled by default, `--rules fixed` refers to these six items. `weapon-inherit-map` is different from the other five items. It writes the segment number into the roster at the moment of changing the machine. It is a persistent state: turning the switch off will not be withdrawn, and turning it on will not retroactively make up for the change that has already occurred. The following four items are **Difficulty Adjustment**: The original behavior itself is normal, it just allows players to choose strength. It is turned off by default. To turn it on, you need `--rules all` or specify it item by item.

| ID | Content |
| --- | --- |
| `boss-dummy-half` | The number of boss disguises is halved, keeping at least 1 |
| `boss-dummy-none` | The boss no longer has a fake body; when checked at the same time as halving, this item shall prevail |
| `upgrade-cap-break` | Breakthrough of the upper limit of modification: All aircraft in the modification screen can be changed to 15 stages (the original works are based on aircraft 6 to 15), and the scale uses ●/☆ to mark the grids beyond the upper limit of the original work; EW equipment changes, additional weapons after full modification, and sales prices are still based on the upper limit of the original work. The changed segment number is a persistent state and will be retained after shutdown but cannot be changed again. For details, see Section 7 of [Modification Stages and Upper Limits](upgrade-limits.md). On the same page, there is an upgrade rule file (`--upgrade-rules`) that can change the increment, price, upper limit and weapon type of each stage. |
| `upgrade-refund` | Refund after leaving the team: When the plot causes the aircraft to leave the army (leaving the team, deleting the old aircraft after transferring, or merging the aircraft), the player's modification funds spent on the aircraft will be refunded at the current price, and a prompt will be displayed at the top of the screen and in the dialogue review; the number of stages inherited by the replacement aircraft and the number of stages donated by the plot using `3D6C` will not be refunded. See §2.6 |
| `parts-carry-over` | Components go with you: When changing the machine, install the enhanced parts installed in the old body directly onto the new body (the original version will be unloaded back to the warehouse and will have to wait for the next overhaul before reinstalling it); if the new body does not have enough slots, the extra parts will still be left in the warehouse. See §2.7 |

- Select `rules.json` written in the trial directory (the unified profile entry is `build/recomp/profile-play/rules.json`, schema `srw64.rule-settings.v1`), and it will be used when starting without parameters. **If there is no such file, open it by default**; an empty list in the file means that the original rules are clearly selected and will not be regarded as "not selected". The terminal prints the current rules on startup.
- Windowless diagnostic/probe host does not leave the launcher: there is no `SRW64_RULE_FIXES` when running `run_host_probe.py` directly, which is the original rule, ensuring that the evidence of bounded operation can be reproduced.
- Changes in the menu are immediately written to the same `rules.json`, and `rule-fixes-events.jsonl` (schema `srw64.rule-fixes-change.v1`, including VI) is appended to the running directory. The running report is `rule_fix_changes`.
- The switch will take effect in the **next settlement**: the battle that has already calculated the hit rate will not be affected, and the switch during the battle performance will not change the result of this time.
- The correction only changes the value read during settlement, not writing to the archive, nor changing the archive format. You can directly change the rules to continue if you have progressed. Each session's `report.json` records `rule_fixes` (`rules_version` with enabled items), the host writes another `rule-fixes.json` and prints `SRW64_RULE_FIXES` in the log. When resuming a save from a session, the launcher will prompt if it was played under different rules last time. Freeze initial backup and sessions before this function are counted according to the original rules.
- The settings page only appears in hosts with interfaces (apply "Settings..." in the menu bar or Ctrl/Cmd+, open the RmlUi page). The windowless diagnostic host still only uses startup parameters.
- The correction is also effective for both the enemy and ourselves, and is consistent with the calling method of the original code: enemy super powers, holy warriors, and low-power pilots are also calculated according to the new rules.
- The underlying switch is the environment variable `SRW64_RULE_FIXES=<逗号分隔的 ID>`; `run_host_probe.py` will verify the ID, and unknown ID will cause the startup to fail directly.

## 2. Original code and corrections

The addresses are all in tactical overlay `load_000AB160` (VRAM `801C2600` onwards, ROM `0xAB160` onwards).

### 2.1 Actual hit rate

The formulas of `801F4384` (actual combat, the results are written back to the combat table `8018B6E8` for each item `+0x12`) and `80204254` (estimates when selecting targets and weapons, called by `80201D98`, `80204564`, `8020500C`) are the same:

```
(命中a + 反应a + 武器命中补正 + 100 + 运动性a) − (回避d + 反应d + 运动性d)
  × 地形补正 × 机体尺寸补正
  ± 集中类状态 30
  + NT/强化(a) − NT/强化(d)          801E1EDC，表 80218080，L1–L9 为 10,14,18,21,24,26,28,29,30
  + 底力(a) − 底力(d)                801E1D64
  − 圣战士(d)                        801E1F08（只有防守方的调用）
  + 超能力(a) − 超能力(d)            801E1F10
  → 之后才处理两种减半条件；80204254 另外把负值钳到 0
```

Driver running record (step size 0x4C): `+05` level, `+06` special skill level (shared with NT, enhanced human world, bottom power, holy warrior, super power), `+26` avoidance, `+28` hit, `+2A` reaction, `+2C` Skill, `+36` skill mark (`04` base power, `08` NT, `10` strengthen the world, `20` holy warrior, `40` super power). Body running record (step size 0x54): `+04/+06` HP and maximum HP, `+10` mobility, `+14` limits.

### 2.2 Super powers, holy warriors: empty function (`esp-level`, `seisenshi-level`)

The function bodies of `801E1F08` and `801E1F10` are only `jr $ra; nop`, and `$v0` is not written. `andi v0, v0, 0x20` (or `0x40`) has just been executed before the call, so the "correction" the caller gets is the skill mark itself:

- Super power: Hit +64 when attacking, enemy hit −64 when attacked;
- Holy Warrior: Only causes the enemy to hit -32 when attacked, and there is no correction when attacking;
- Both only judge the flag, not the level. It also takes effect when the skill level is 0. For example, if Garuri is in front of the driver Lv7, and Hazel and Black Knight are in front of Lv6, the status page will not show the holy warrior, but there is still −32.

After the correction, the two functions are changed to check the NT level table according to `+06` (`801E1EDC` uses `80218080`), that is, L1–L9 is 10…30, and L0 is 0. The calling position remains unchanged: the superpower is still on both the offensive and defensive sides, and the holy warrior is still only on the defensive side.

The basis for selecting this table: the hit row and the avoidance row of the NT table are the same; the three rows of the table `802180B4` immediately followed without any code reference have the same curve in the first two rows, and the third row 0,20,40…150 is exactly one-tenth of the Aura barrier table `80218930` (0,200…1500), like data that was not connected after preparation for the holy warriors. There is no more direct evidence of the numerical values ​​intended by the original work.

**Corrected and added on 2026-09-18 (`aura-slash-power`). ** Missing items mentioned in the data: Holy warriors should increase the power of Aura weapons such as **Hurra's sword**, and superpowers should increase the attack power of all weapons. There are only 5 places where the Holy Warrior flag is checked in the entire ROM (two weapon unlocking conditions, two hit rates, and Ora Barrier), and there are only 4 places where the super power flag is checked in the hit rate function; neither the actual combat damage `801F5628` nor the AI ​​damage estimate `80203418` reads the driver skill flag (`tests/test_rule_fixes.py` is confirmed by bytes). So **the two attack power bonuses do not exist at all in the original code**, it is not a numerical error.

Value basis: ゲームカタログ@Wiki quoted "バグがなかった occasion, L9's hit, evasion +30, attack power +1500". The rows of unread data at the back of the NT table in ROM correspond exactly to:

| Table row | L0–L9 | Correspondence |
| --- | --- | --- |
| `80218080` lines 0–2, `802180B4` lines 0–1 | 0,10,14,18,21,24,26,28,29,30 | Hit/Avoid, L9 = +30 |
| `8021809E`, `802180C8` | 0,20,40,60,80,100,120,130,140,150 | ×10 = Attack power +200…+1500, L9 = +1500 |
| `802180A8` | 0,20,30,40,50,60,70,80,90,100 | ×10 = +200…+1000, consistent with the barrier value of the guide seal |

`aura-slash-power` During the period of calling `801F5628` and `80203418`, the attacker's weapon power (weapon operation record `+0x06`, the same unit as the interface display) is temporarily added to `802180C8`[skill level]×10, and restored after the call. Only affects **weapon condition 15** used by **Jihadi Pilot** (requires Holy Warrior L3) Weapons: Hazel, Hazel , ハイパーオーラショットアーム, ツインオーラアタック, in total 20 weapon records; not added to normal オーラzanり (condition 14). Condition 15 itself requires L3, so the actual bonus is L3 +600 to L9 +1500. The weapon power numbers on the interface remain unchanged, and the bonus is reflected in the battle preview and settlement.

The all-weapon attack power bonus of super powers is also missing, which can be compensated by using the same curve. **The user did not request it, and no switch was added this round**.

Aura Barrier: The actual value used in the game is +200...+1500 (`80218930`, which is the curve of attack power), and the guidebook prints +200...+1000 (the last row in the above table). It is decided by the user to **keep the original version**. It will be deemed that the guidebook is incorrect and no switch will be made.

The Holy Warrior level in the original version also affects: weapon conditions 14/15 (`801E6214`) require L1/L3 respectively; Aura barrier value is 3000 + `80218930`[level] (`801F6EE0`).

### 2.3 Limit: settlement is not read (`limit-cap`)

The driver status page (`801E6C5C`, `801E7174`/`801E71C8`) displays avoidance and hits as `%3d+%3d` (pilot value + body movement), and draws warning colors when exceeding the limit. However, the above hit formula is directly added, and the full ROM reads limited fields only for display, load copy, modification and component addition (`800A5254`, each segment of limited modification +10/+20) and special mode bonus (`801FE9CC`, etc.). In the original version, the modification limit and equipment limit parts have no effect on combat.

After the correction, during the call of the two hit functions, the attacker's "hit + mobility" and the defender's "avoidance + mobility" each do not exceed the limit of the aircraft being flown, and the reaction is not included in the upper limit, which is consistent with the comparison caliber on the status page. The implementation method is to temporarily reduce these two fields during the call of the original function (first reduce the driver value to not exceed the limit, and then let the mobility complement the limit), and then restore it to the original state after the call, and the rest of the original formula remains completely unchanged.

Note: The limit of most mobile units is more than 100 higher than the mobility, but it is easy to exceed it by low-level robots (such as Mitsubishi: mobility 95, limit 140) or high-level pilots, and the hit/avoidance of these combinations will be significantly reduced when turned on.

### 2.4 Bottom force: The gear is advanced by one gear, and the three uses have the same value (`potential-bands`, `potential-half`)

`801E1D64(用途, 驾驶员, 机体)` Check the 10×10 table of `80217F90`: rows are skill levels, columns are HP levels, row L and column c are max(0, c+L−9)×10, L9 is the highest 90. The gear level is determined by HP/maximum HP×100:

| HP | Original gear | Corrected gear |
| --- | ---: | ---: |
| More than 90% | 1 | 0 |
| 80–90% | 2 | 1 |
| … | … | … |
| 20–30% | 8 | 7 |
| 10–20% | 9 | 8 |
| Below 10% | 9 | 9 |

The first comparison with the original version records more than 90% as gear 1, and column 0 can never be read, so L9 has +10 full health, and the highest value occurs when the HP is below 20%. Both documents (S-RPG navi, Akurasu) write the highest level below HP 10%, and the 0th column of the table is all 0, which corresponds to "full health, no bonus", so it is judged that there is one less offset. `potential-bands` uses the gears in the right column instead (the comparison still uses the same single-precision operation).

The three call points respectively pass in the uses 2 (attacker hits), 1 (defender avoids), and 0 (crit rate, only called when our team attacks, and the enemy's critical hit is divided by 4), but this parameter is overwritten into a table address at the beginning of the function, and the three uses get the same value. Both sources say that base power's hit/avoidance correction is "higher than the original", with Akurasu saying it's 2x. `potential-half` Halve the results of uses 1 and 2, leaving the critical hit rate unchanged. **This item is only based on community data and unused parameters, and the evidence is weaker than the others**; the specific numbers given by the data ("L9, HP below 10% should be +50, actual +100") do not match the code's maximum value of 90.

### 2.5 Number of boss disguises (`boss-dummy-half`, `boss-dummy-none`)

This item is not a bug fix. The original mechanism itself is normal: when bit 14 of the deployment record (28 bytes) behavior word `+0x16` is set and the camp is not ours, `8020ABB4` writes `+0x18` into the `+0x14` of the new driver record. During combat, `801F6E3C` is used. Judgment, `801FCA78`/`801FE068` are consumed one by one, and the remaining times are not displayed in the game. Original version total 42 The records with this bit all belong to ハマーン, シャア, シロッコ, グレミー, ミリアルド, ギュネイ, ガトー, ル・カイン, and the value 2, 3, 5, 7. For a complete description of fields and judgments, see [Basic Repair](base-fixes.md) (the problem there is dealing with the number of times Wufei was mistakenly written, which has nothing to do with this item).

The correction method is to rewrite its `+0x18` while `8020ABB4` is processing **this record**, and restore it to its original state after the call is completed:

| Rules | 2 | 3 | 5 | 7 |
| --- | ---: | ---: | ---: | ---: |
| Original | 2 | 3 | 5 | 7 |
| `boss-dummy-half` | 1 | 1 | 2 | 3 |
| `boss-dummy-none` | 0 | 0 | 0 | 0 |

After halving and rounding, keep at least 1 time so that the mechanism still appears; when both are enabled at the same time, cancellation shall prevail. The rewrite only applies to the deployment record of **this level copy** recorded in `80199400`. No ROM or archive is written. Switching rules after the appearance will not change the remaining number of units already present - the next time they appear, they will be generated according to the new rules. Records without false identities (for example, two records when Wu Fei is hostile) will not be affected at all.

### 2.6 Refund after leaving the team (`upgrade-refund`)

The original script uses `3D5A …,4000` (or 3000) to delete the aircraft that left the team, delete the old aircraft when transferring, and delete the ゴッドマーズ when the ゴッドマーズ merges; the aircraft instance disappears together with all modifications, and the funds invested by the player are gone. [Transformation Inheritance Analysis](upgrade-inheritance.md) Sections 6, 8.3 list which "transformation losses" fall into this category. In this item, before the deletion occurs, the modification of this machine body will be refunded according to the current price, and the strength of any machine body will not be changed.

**When to exit**: Only deletion in the plot routine. The host wraps four functions:

| function | role | packaging |
| --- | --- | --- |
| `800AA464` | The pilot leaves the body and deletes the instance with the number equal to the parameter (`3D5A` mode 3000/4000 is called by `800A3540`; delete the old machine given by the script when registering a new machine) | Mark the "plot removal" range |
| `800AB808` | `3D6A` Mode 3, ゴッドマーズcombination deleteガイヤー | Mark "combination" range |
| `800AAD28` | Register the new machine; Step 4: Get the first active instance corresponding to the predecessor table (`D_800CA3A0`, via `800AA814`) and save its segment number | First find this instance according to the same rules and record it as "inherited" |
| `800AA3C4` | Release the body instance (all deletions go through here) | Within the above range, the host settles according to the table, and then calls the original function |

Sale (sale screen `801C3678`, comes with a selling price including modifications) and removal on the tactical map (`800A7DEC`) also call `800AA3C4`, but are not within these scopes and no refunds are given. Only our instance pool (140 units from `8016A210`, pool 0 with allocator `800A6E68`) will be processed, instances from other pools will not be refunded.

**How ​​much to refund**: The five items are based on their respective price lists, and the weapons are based on the price list of modification type (instance `+0x15`, type 0 cannot be modified, and is not counted), and the unit prices of 0...the current segment number −1 are added up; the price comes from the currently effective table, so when `--upgrade-rules` is included, it is based on the price of the rule file. The non-refundable part:

- **Inherited Instance**: The predecessor's segments have been moved to the new machine when changing devices (such as サンドロック→Change), and deleting the predecessor does not count as a loss.
- **Number of segments provided by plot**: 26 units will be directly written as N segments by `3D6C` in the original script (38 instructions, up to 8 segments, listed in `upgrade_refund.hpp`, `tests/test_upgrade_refund.py` is checked against the ROM). `3D6C` Write the five items and all weapons as the same value (not exceeding the upper limit of the machine), so the instance that receives the gift does not have any transformable items lower than N: The host only counts these N segments as free when all five items and transformable weapons are ≥ N. As long as one item is lower than N, it means that the instance did not receive the gift (another route, or the segments were inherited from the predecessor, or purchased on the predecessor), and all items will be refunded. The same machine may or may not receive gifts in different routes (such as ウイングゼロ); the only situation where there will be less refunds is if no gifts are received and the player changes each item to N or more. In this case, the first N segments will not be refunded.

Funds (`D_8010F5F4`, u32) plus refund, stopping at maximum on overflow. There is no upper limit for the original method of adding funds (`3D5B`, combat income), and there is no additional limit for this item.

**Tip**: When the refund is not 0, a prompt bar (in the current language) will appear at the top of the game window for about 6 seconds, and a line will be added to the dialogue replay (all three languages ​​will be saved, and will change after switching with F7), for example, "サンドロック has left the army, and the transformation fund of 17,000 will be returned." The aircraft name remains its original Japanese name. The prompt relies on the native dialogue module and only appears in the unified profile entrance; the windowless host will still be refunded and only logs will be written.

**Persistence**: The refund will be written into the funds and saved with the game archive; closing this item will not take it back, and opening it will not retroactively delete the item that has already occurred. During the startup period, every plot deletion (including non-refundable) will add `upgrade-refund-events.jsonl` (schema `srw64.upgrade-refund.v1`: body, source, whether it is inherited, free segments, five items and weapon amounts, and front and rear funds) in the running directory. The debugging interface can be read with `srw64ctl events refunds`.

### 2.7 Parts accompanying (`parts-carry-over`)

When the original version releases the machine instance, all its enhancements will be removed: `800AA3C4` → `800A9DCC(.., 0, 1)` → `800A9D60` Write −1 to the slot, clear the number of equipment of the machine body, and reduce the number of equipment in the inventory record (`D_8015E990`, each part u16: high byte number of possessions, low byte number of equipment) 1. **The holding count does not change, so the parts will not disappear**. You just go back to the warehouse and have to wait for the next maintenance before you can reinstall it - you can only play the level where you automatically attack immediately after changing the machine.ダンクーガ's in-situ upgrade (`800ACB74`) also removes the parts of itself and each beast's fighter plane.

After this item is turned on, the package of `800AAD28` records the components of the driver's current body before the original function. After the original function returns, install them into the empty slots of the new body in the original order, and add back the number of equipment in the inventory. Finally, adjust the `800A5924(机体, 1)` propagation as in the maintenance screen. Those that cannot be loaded are left in the warehouse: Wutai EWタム, ヘビーアームズカスタム, アルトロンカスタム) and Santai Makoto 's slot is all 1, while its predecessor was 2, so these swaps will leave one piece behind each time.

No repeated installation: If the original function returns early because "the driver is already on this machine" and no parts have been removed at all, the package will find that the number of equipment on the old machine has not changed and skip it. It will also be skipped if the number of possessions is less than the number of equipment, there are no empty slots, and no new machine instance can be found. Each time it is successfully carried, `parts-carry-events.jsonl` (schema `srw64.parts-carry.v1`: front and rear body numbers, parts carried, parts left in the warehouse) is added to the running directory.

## 3. Implementation

| Location | Content |
| --- | --- |
| `tools/recomp/toolchain/generate_cpu.py` | `NATIVE_HOOKS` Eight new names have been added: `801E1D64`, `801E1F08`, `801E1F10`, `801F4384`, `80204254`, `8020ABB4`, `801F5628`, `80203418`. The original functions have been renamed respectively. `srw64_original_potential_bonus`, `_seisenshi_bonus`, `_esp_bonus`, `_battle_hit_rate`, `_hit_estimate`, `_deploy_record`, `_battle_damage`, `_damage_estimate`. Requires `make recomp-cpu` to be regenerated. |
| `src/host/rule_fixes.hpp` | Rule directory and analysis, startup report, level table reading, base power level, `StatCap` (temporary capping of the limit), `DummyScale` (temporary rewriting of the number of fakes in the deployment record). |
| `src/host/game_hooks.cpp` | Eight wrapper functions: When the rule is not enabled, only the original function is called (when the probe is enabled, the calls to the two hit rate functions are also read-only and recorded). |
| `src/host/rule_probe.hpp` | Actual machine probe, see next section. |
| `src/native/ui/frontend.cpp` (settings page), `macos/app_menu.mm` (menu bar entry) | [Settings page](../native/settings-window.md) generates rule buttons, check status, and three presets (`rules::presets`) grouped by directory, and re-titles according to the language. |
| `src/host/graphics.cpp` | Install the menu after the window is created (retry every frame if the menu bar appears late), and remove it when the window is closed. |
| `content/locales/*.json`, `src/srw64_native/profile.py` | Menu copy; `UI_KEYS` is automatically derived according to the rule directory. New rules must be supplemented with titles in three languages. |
| `src/srw64_native/rule_settings.py` | The rule directory, saving and session record reading shared by the launcher and probe script; `CORRECTIONS`/`DIFFICULTY` determines which ones are opened by default at first startup. |
| `tools/recomp/run/play_native.py`, `run_host_probe.py` | `--rules`/`--rule-fixes`; reporting fields `rule_fixes`, `rule_probe_enabled`. |
| `src/host/upgrade_refund.hpp` | Departure refund: four packaging ranges, predecessor instance search, transformation cost and free segments, fund writing and logs, machine name reading (text table 0, starting from id 527). `generate_cpu.py` adds four more renames (`srw64_original_unit_register`, `_unit_remove`, `_unit_merge`, `_unit_delete`) to `800AAD28`, `800AA464`, `800AB808`, `800AA3C4`. |
| `src/host/parts_carry.hpp` | Components on the go: Capture the parts of the old body, determine whether the original function has really been removed, install it into the new body according to the empty slot, add several times to the inventory equipment and log. Reuse the existing renamed wrapper of `800AAD28`. |
| `src/host/native_dialogue.cpp`, `dialogue_model.hpp`, `native_dialogue_text.cpp` | Refund tips: copywriting in three languages (`refund_notice`), prompt line in review (`Entry::notice`, does not participate in speaker color matching, inserted before the fragment being read). |
| `src/host/notices.hpp` (implemented in `src/native/ui/frontend.cpp`) | The prompt bar at the top of the game window (RmlUi, any thread delivery, window thread display), `status.notices` of the debugging interface and screenshots can be seen. |

All callers go through the overlay function table (`LOOKUP_FUNC`), so actual combat, AI estimation, and probes use the same set of wrapper functions.

## 4. Verification

- `make recomp-rule-fixes-test` (merged into `recomp-native-check`): ID parsing and reporting, temporary coverage of probes, level table reading, limit capping and recovery (including nesting, invalid pointers, limits lower than driver values), two sets of bottom power gear boundaries (including the inf/NaN case where HP is 0), number of fakes conversion and `DummyScale` Rewrite/restoration (including our records and records without fake identity will not be affected).
- `tests/test_rule_fixes.py`: Settings saving and reading, session recording, difficulty adjustment are turned off by default, host and Python directories are consistent, hook rename and packaging exist; ROM facts (two empty functions, hook entry bytes, NT table and unreferenced table are on the same curve, barrier table is 10 times as much, bottom force table shape and first gear are 1, usage parameter is overwritten, limit comparison of status page).
- Menu: `SRW64_WINDOW_CONTROL=1` is written when `rule-control.json` (schema `srw64.rule-control.v1`, fields `sequence` and `item`, `item` is the rule ID, `original` or `all`), the host presses the item through the menu's own `performActionForItemAtIndex:`, and writes the pressing result, all item titles and check status into `rule-menu-events.jsonl`. See the end of §5 for actual measurements.
- `make recomp-upgrade-refund-test` (merged into `recomp-native-check`): price accumulation, number of free segments (obtained/not received as a gift), rule closure and no refund outside the scope, inherited instances will not be refunded but logged, other pools and non-aligned addresses, fund caps, log fields, machine name reading. Review the order, color and language switching of prompt lines in `tests/native_dialogue.cpp`.
- `make recomp-parts-carry-test` (merged into `recomp-native-check`): No capture when the rule is turned off, only the one that can fit when the slot is insufficient, full installation when the slot is sufficient, no repeated installation when the original function is not removed, memory and log fields are not written when the number of possessions is insufficient/the new body is not in the roster/there is no driver.
- `tests/test_upgrade_refund.py`: Four hook renames and packaging, difficulty groups and three language copywriting; ROM facts (`3D6C`, 38 items in total, the gift table is consistent item by item, the starting point of the body name id is 527, the content of the predecessor table and the lookup command of `800AA814`).
- Real machine probe: see §5.

## 5. Real machine probe

When `SRW64_RULE_PROBE=1`:

- When the script stops at `3D38` for the first time and both the enemy and the enemy have units, the host calls `801F4384` and `80204254` for each pair of friendly/enemy units (both directions) and four types of HP (100/85/15/5%). Each time, the original version, each single item, and all corrections are used in turn, and the results are written into `rule-probe.jsonl` (schema `srw64.rule-probe.v1`). The battle table, HP and registers will all be restored. The critical strike function consumes random numbers and is not called within the probe.
- Each call to these two functions (including the game's own engagements and AI estimates) is also credited to `rule-calls.jsonl` (schema `srw64.rule-call.v1`, `source` distinguishes `probe` from `game`).

The attacks in the two mini-levels are the same: our ally's タケル (super power L1), Mari's (super power L2), ショウ (holy warrior L3), and Manzhang on the ミニフォー (base power L4, hit/avoidance + mobility beyond the limit 63); the enemy's ロゼ (super power) L2), ガラリア (holy warrior mark, skill level 0), ムニフォームゲ兵 (over the limit 50/55). Both are entered from the frozen maintenance archive, `--original-name-entry`, and the input scripts can be found in the respective files.

### rules-3 (`build/recomp/mini-stage/rules-3`, [`rules.json`](../../config/recomp/mini-stages/rules.json), 4,655 VI ended by `EXIT_AFTER=3D47`)

All five items of `SRW64_RULE_FIXES` are printed when the host starts; the probe is triggered in VI 4473 (`3D38` at the beginning), `players=4 enemies=3`, a total of 192 lines (12 pairs × 2 directions × 4 HP × 2 functions), 7 sets of rules per line. Check line by line (checking script calculates expectations according to the following formula):

| Rules | Expected changes | Results |
| --- | --- | --- |
| `esp-level` | +[Attacker's Super Power] (Level Table − 64) −[Defender's Super Power] (Level Table − 64) | 192/192 Consistent |
| `seisenshi-level` | −[Defending Holy Warrior] (Level Table − 32) | 192/192 consistent; Guraira (skill level 0)’s hit rate increased from 40 to 72 when attacked, confirming that the original version also gave 32 at level 0 |
| `potential-bands` | The difference between the offensive and defensive base power values from the original gear to the modified gear | 192/192 consistent; the original/corrected values of Wan Zhang (L4) at 100/85/15/5% HP are 0/0, 0/0, 40/30, 40/40 |
| `potential-half` | The difference between the base power of the offensive and defensive sides halved | 192/192 consistent; for example, Wan Zhang 5% HP attack Gaara 80 → 60 |
| `limit-cap` | Excess amount × terrain and size magnification | Combinations with an excess of 0 are unchanged; combinations with excess changes are consistent with the magnification of 0.8, 1.0, 1.2 (for example: ムゲ兵attacksタケル−50, attacks ショウ −39; Wanzhang attacks ロゼ −75); the estimation function is 6 Rows change less due to clamping to 0 |
| All | Sum of individual terms | 186 rows (excluding 6 rows with estimation function clamp) error does not exceed 1 (truncated) |

### rules-battle-1 (`build/recomp/mini-stage/rules-battle-1`, [`rules-battle.json`](../../config/recomp/mini-stages/rules-battle.json), 12,000 VI)

The enemy is close to us, all corrections are enabled, our turn ends after the opening, and every 90 VIs in the enemy's turn press A to accept counterattack. The calls of the game itself in `rule-calls.jsonl`: AI estimates 14 times, actual battles 6 times (VI 5316 ムゲ兵→ショウ and counterattack, VI 6956 ガラリア→Wanzhang and counterattack, VI 8336ロゼ → Wan Zhang and Counterattack), the pilot/machine pairings in the calling parameters are correct, indicating that the actual calling registers are consistent with the stack parameter layout and probe. The operation reaches the upper limit of VI and ends normally without host error; map screenshots `present-2700.png` and `present-4200.png` show units on both sides and gray enemy aircraft after action.

### Menu actual measurement (`build/recomp/profile-play/sessions/20260918T015241.213153Z`)

Start with zh-Hans, turn off all rules, use the control hook to press four items in sequence, log `SRW64_RULE_MENU installed items=11`:

| Rules activated after pressing | | Checked status |
| --- | --- | --- |
| Limits | `limit-cap` | Limits only tick |
| Turn all on | All six items | Check all six items |
| Super Powers (click again) | Remove `esp-level` | Uncheck Super Powers and keep the rest |
| Close all (original rules) | None | Uncheck all |

`rules.json` (eventually an empty array), `rule-fixes-events.jsonl` (VI 177/180/238/241) and log lines are written for each change. The `rule_fix_changes` of the run report contains these four changes. The entry title is Chinese copy in the current language, and the description is not clickable.

This round was run when `wing-kill-dummy` was still an optional rule, so there were six items in "Open All", `installed items=11`; this item was later designated as [Basic Repair](base-fixes.md) and removed from the directory. Now there is one less item in the menu, and the record itself has not been changed.

### rules-aura-1 (`build/recomp/mini-stage/rules-aura-1`, `aura-slash-power`)

The probe adds a third function: AI damage estimation `80203418` (does not throw critical hits, does not move random numbers; actual combat damage `801F5628` will throw critical hits, and the probe does not call). Holy warrior pilots use their own Condition 15 weapons instead. 288 lines in total.

| Attack → Defender | Original version | After opening | Poor |
| --- | ---: | ---: | ---: |
| ショウ (Sacred Warrior L3, ハイパーオーラ杀り 2400, bonus +600) → ロゼ | 2367 | 3499 | +1132 |
| Same → ガラリア | 3807 | 4939 | +1132 |
| Same → ムゲ兵 | 2727 | 3859 | +1132 |

The increments of the three targets are the same, which means that only the attack item is amplified (2400→3000 multiplied by a set of multipliers equal to fighting, strength, and terrain adaptation), and the defense item is not affected. The damage and hit rate of the remaining attackers remain unchanged. The packaging of the actual combat damage function and the estimation function use the same piece of logic and are covered by unit tests. This round does not have a separate value in the actual combat.

### refund-2 (`build/recomp/debug/20260918T131851.399969Z`, [`refund.json`](../../config/recomp/mini-stages/refund.json), `upgrade-refund`)

Debugging interface driver: Press F8 on the main menu to enter the mini-level, and delete the opening events in four ways. `upgrade-refund-events.jsonl` is consistent with the item-by-item recalculation of the ROM price list:

| Delete | Source | Free Levels | Pentathon | Weapons | Refund |
| --- | --- | ---: | ---: | ---: | ---: |
| ヘビーアームズ 130 (`3D6C 130,4` after `3D5A …,4000`) | removal | 0 | 93,000 | 260,000 | 353,000 |
| デスサイズ 127 (transferred to 128, predecessor was inherited) | removal, `inherited` | — | 0 | 0 | 0 |
| デスサイズH 128 (bought at 127, then `4000`) | removal | 0 | 32,000 | 30,000 | 62,000 |
| ウイングゼロ 119 (give away 3, change all to 5) | removal | 3 | 78,000 | 198,000 | 276,000 |
| ガイヤー 185 (`3D6A 3` combined) | merge | 0 | 32,000 | 87,000 | 119,000 |

Funds 0 → 810,000. Four prompts appear in order (up to three at the same time, the fourth one is queued), and there are four lines of prompts in front of the dialogue in the review; after F7 switches to English, the prompts in the review become English simultaneously. In the previous round (refund-1), according to the old "take the lowest number of segments" rule, all 2 segments of デスサイズH were regarded as gifts, and the refund was 0. It was also found that the width of the prompt bar was insufficient and the end was truncated, both of which have been corrected.

### Not covered

- The critical hit rate path (`801F47B0` calls the base force, purpose 0) is only covered by the unit test and does not take a separate value in the actual machine.
- There is no checking whether the hit rate display on the interface is consistent with the settlement, and there is no long-term trial play; after turning on `limit-cap`, the warning color meaning on the status page changes to "Capped", and the interface itself remains unchanged.
- The attack power bonus of the super power is not implemented (it does not exist in the original code, see §2.2); the power of the Holy Warrior's Orla weapon has been supplemented by `aura-slash-power`.
- The refund for leaving the team (§2.6) has been verified using the mini-level [`refund.json`](../../config/recomp/mini-stages/refund.json) (see §5), but it has not yet been triggered in the real leaving event in the original plot.