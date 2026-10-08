> **Language / Ngôn ngữ:** [English](base-fixes.en.md) · [Tiếng Việt](base-fixes.vi.md) · [中文](base-fixes.md)

# Basic repair: effective by default, no switch

Date: 2026-09-18. Here is a record of the original bug fix that takes effect by default: the game is inconsistent with its own data, and no original gameplay has been changed after the fix, so it is not made a player option. Changes that require players to decide their own strengths and weaknesses are in [Optional Rule Modifications](rule-fixes.md), and the original clues for external reports are in [Original Bug Registration](original-bug-register.md).

| ID | Fix | Implementation |
| --- | --- | --- |
| BUG05 | Wu Fei and other W pilots no longer bring fake bodies when hostile | Host package `resident_func_800A5054` (`src/host/base_fixes.hpp`, `game_hooks.cpp`), unconditionally effective |

Judgment criteria: The original deployment record clearly stated that these units did not have fake bodies (behavior bit 14 was not set, and the additional value was 0), but the code included the number of our kills due to a lack of camp judgment. Restoring to the state required by the record itself does not require player choice, and does not change the original number of disguises for any boss.

## 1. BUG05: When Wu Fei is hostile, his number of fakes is equal to his number of kills on our side.

The addresses are distributed in resident codes (`800A…`, `8009…`) and tactical overlays (`801E…`–`8020…`).

**Original fake body mechanism**

- `801E0410` When placing units, the roster slots of camps 1 and 2 (`8015E100 + 阵营×0x258 + 槽×0x14`) `+1` are set to `0x80`; when the original camp of the deployment record is non-0 (including the record value 3 placed on our side), `8020B324`/`8020BE34` will also be set. It means "non-player control".
- For this type of unit, the driver record `+0x14` (u16) is the number of clones**; the same field for our units is the number of kills, `801FB374` is only added by 1 (maximum 999) when camp 0 and the roster does not have `0x80`.
- When deployment record (28 bytes) behavior word `+0x16` bit 14 is set and camp is non-0, `8020ABB4` writes `+0x18` to `+0x14`. The original version has a total of 42 such records, all belonging to ハマーン, シャア, シロッコ, グレミー, ミリアルド, ギュネイ, ガトー, ル・カイン. 2, 3, 5, 7.
- Settlement order (`801F7204`): First press the hit rate of `+0x12` in the battle table (clamped to 0–100) and 1–100 If the random number roll hits, **only the attack that should have hit** will check the clone ability (`801F6C44`), cut り払い (`801F6D10`), and fake body (`801F6E3C`) in order. The conditions for the fake body are that the camp is not 0, the roster `0x80` is set and `+0x14 ≠ 0` is established. When established, the result is `0x15`, the attack is invalid, and then `801FCA78` (normal combat) or `801FE068` (map weapons) reduces `+0x14` by 1. The remaining times are not displayed in the game.

**reason**

- There is also a long-lasting knockdown table for the five members of the W series `801614E0` (5 u16), with the subscripts 0 ヒイロ (character 95), 1 デュオ (92), 2 トロワ (93), 3 カトル (89), 4 Wufei (91). `801FB374` is called after adding a kill to our record. `800A4FBC` is added synchronously by 1; `80091ED0`/`800920B4` is saved and read with the intermediate archive, and `800A4F94` is cleared in the new game.
- `3D5A … 4000` When leaving the team, `800AA62C` calls `800A7E88` to clear the entire driver record and `+0x14` is reset to zero; when re-registering, `800A84F8` creates a new record and `800A5054` lifts `+0x14` back to the value in the table. This is prepared for "leaving the team and rejoining to retain the number of kills".
- But `800A84F8` will call `800A5054` when creating a new named pilot (character number < 287) for **any faction**, while `800A5054` only looks at the character number, not the faction. Wu Fei's two enemy records themselves have no avatars: "In front of the decisive battle in the space domain" `00202a0c` (camp 1) and "Life and death in the future" `00208568` (camp 2) have both behavior words and added values ​​of 0. So when he created a new record as the enemy, `+0x14` was written as the number of previous kills on our side, and the enemy unit read this field as the number of fakes.
- The backup will no longer increase after leaving the team, so the number of clones is equal to the cumulative number of kills until leaving the team (the upper limit is 999), not a fixed 21. Consuming the avatar only changes the enemy's record, not the backup, so the number of kills will be restored as usual when he rejoins (`3D5A 91,0,115,500`).
- Four other people take the same path. Hino appears as a third party (record value 4) in "OZ Split Before", "Nana Nasana" and "Toro Assassination Order". If he was shot down by our side before, he will also wear a fake body. Whether these levels are ranked after his downfall in each route has not been verified in this round.

### Correction

`800A5054` is changed to only execute when the driver record is in our table (`80172F40`–`80174CEF`, 100 entries × 0x4C). The new records of the enemy and the third party will maintain the value when deployed (five flies 0, the boss still presses the recorded number of times), and the behavior of leaving the team and then joining again to restore the number of kills remains unchanged. Another caller of `800A5054`, `80210758` (the unit present is converted to our side), is only called when the target camp is 0, and the pointer in our table is also passed in, which is not affected.

## 2. Real machine reproduction and comparison

The process of the original version spans multiple episodes (Join → Shoot down → Leave → Hostile → Join again), so I made a mini-level that compresses it into one level [`wufei-dummy.json`](../../config/recomp/mini-stages/wufei-dummy.json), input script `wufei-dummy-input.json`, running mode (Japanese, Original, `--original-name-entry`, mute, `SRW64_STATE_PROBE=1` and `SRW64_MINI_STAGE_CAPTURE=1`), 20,000 VI.

Level process and comparison settings:

- Round 1: Wu Fei (アルトロンガンダム, level offset 60) is on our side, with three Dozers around him; after ending our turn, he counterattacks and knocks down these three units during the enemy phase. Kaoru (same level offset 60) stands in the distance as the anchor point of the camera, and is also the one attacking Wu Fei from behind.
- Round 2 event: `3D46 91,1` makes him retire, `3D5A 91,0,115,4000` clears the pilot and aircraft records, and then uses `3D45 2` to press his own "before the decisive battle in the space domain" record (camp 1, behavior word 0, additional value 0) Appears as an enemy; in the same group, there is also the record of "アクシズのATTACK BEFORE" (action word `0x4000`, additional value 3) by グレミー as a **design value comparison**.
- Enemy phase after the end of the 2nd round: The enemy's five-fly attack is carried out, and the carried out counterattack is carried out.
- Round 3 event: After reading `3D5A 91,0,115,500`, ask him to rejoin, read it again, and check that the correction has not destroyed "rejoin to retain the number of kills".

Each observation point is given by a snapshot of the command boundary after `3D38`, which reads the roster slot (`8015E100`), airframe instance (`8016A210`), and pilot instance (`80172F40`).

### Two rounds of comparison (`wufei-dummy-original-5` and `wufei-dummy-fixed-1`, 20,000 VI each)

When the correction was still an optional switch, the two runs were distinguished by `SRW64_RULE_FIXES`; after being set as a basic repair, the switch has been removed. The right column is the current behavior of each run, and the left column is the original version.

The two rounds are identical except for this switch (the host log prints `SRW64_RULE_FIXES none` and `wing-kill-dummy` respectively), the same binary, the same image, and the same input script; they are consistent frame by frame until the correction takes effect.

| Observation Points (Command Boundary Snapshot) | Original | Corrected (now default behavior) |
| --- | --- | --- |
| Start of Round 2: The number of kills of five flies (our side) | VI 11817: +0x14=3 | VI 11817: +0x14=3 |
| `3D46 91,1` After exiting | VI 11905: The record is still there, +0x14=3 | Same as left |
| After `3D5A 91,0,115,4000` | VI 11907: Driver record disappears | Same as left |
| `3D45 2` After appearing according to his own enemy record | VI 12273: **五飞 (camp 1) +0x14=3**; グレミー +0x14=3 | VI 12273: **五飞 (camp 1) +0x14=0**; グレミー +0x14=3 |
| After the second enemy phase (タケル counterattack) | VI 15293: Wufei +0x14=**2**, HP is still 5700/5700 | VI 15623: Wufei has been defeated, グレミー +0x14=3 unchanged |
| `3D5A 91,0,115,500` After joining again | VI 15355: Five Flying (Faction 0) +0x14=3 | VI 15685: Five Flying (Faction 0) +0x14=3 |

- In the original version, the number of enemy Gofei's clones is exactly equal to the 3 kills he made while on our side, and his deployment record does not have a clone position; グレミー's 3 times come from the record itself, and the two sources appear at the same time in the same level.
- The same counterattack is in the same frame in two rounds (`present-7380.png`, VI 14754/14766): the original version displays a green "ダミー" and the five flying HP remains unchanged; the corrected version displays "クリティカル 5700", the HP returns to zero and is defeated. This is the direct reason why players feel "unable to play".
- After two rounds of rejoining, our team's record +0x14=3 was obtained, indicating that the correction did not affect the original purpose of "leaving the team and rejoining to retain the number of kills".
- There are another three rounds of process running: `original-2` uses the binary before adding the hook, and the level has not yet been reached. `3D46` exits the stage, but the common observation point (our side shoots down 3 → the enemy enters the fake body 3, グレミー3) Consistent with subsequent rounds; `original-3`/`original-4` (including hooks, rule closure) and `original-5` are the same frame by frame at all observation points. In other words, adding the wrapper function itself does not change the original behavior. `original-3` also exposed a pitfall of the mini-level itself: directly `3D5A … 4000` to a unit still on the map will leave a dangling roster slot and SIGBUS after returning to the operation, so the level first uses `3D46` to exit, see [Mini-level](../script/mini-stage.md).

## 3. Not covered

- There is no actual running in the original levels (Independence Army "Before the Battle of the Universe", OZ "The Future of Life and Death"), the mini-levels just put the same instructions and records into one level; the continuous comparison of different kill numbers, the differences between the two routes, and the return of the save data after rejoining have not been done yet.
- The actual performance of the other four W pilots who appeared as third parties has not been tested; it has not been verified whether the three records of ヒイロ are all ranked after his crash.
- The display of the remaining number of dummies (Roadmap QOL02) has nothing to do with this correction and is not involved in this round.

## 4. Implementation and verification

| Location | Content |
| --- | --- |
| `tools/recomp/toolchain/generate_cpu.py` | `NATIVE_HOOKS` Rename the resident `800A5054` to `srw64_original_wing_kill_restore`; `make recomp-cpu` is required after the change. |
| `src/host/base_fixes.hpp` | Our pilot table range `player_pilot`, and the basis for this fix. |
| `src/host/game_hooks.cpp` | `resident_func_800A5054`: Return directly when the record is not in our table, without checking any rule switch. |
| `config/recomp/mini-stages/wufei-dummy.json` | To reproduce the level, see §2. `tools/recomp/gameplay/wing_kill_save.py` also provides a controlled method of overwriting the crash backup in the archive and recalculating the checksum, which is only effective for archives actually read by the game. |

- `make recomp-base-fixes-test` (merged into `recomp-native-check`): Boundary determination of our pilot's table range.
- `tests/test_wing_kill_dummy.py`: The hook is renamed, the wrapper function takes effect unconditionally and does not reference the rule directory. This item is no longer in the optional rules and the menu copy in the three languages; ROM facts of BUG05 (the backup table is written at the same time when shooting down, the call point of `800A84F8`, `800A5054` read-only character number, the jump table from the character to the backup subscript, and the pseudonym judgment read `+0x14`, the setting of roster `0x80`, the behavior word of two enemy records is 0); and the checksum processing of the archive tool.