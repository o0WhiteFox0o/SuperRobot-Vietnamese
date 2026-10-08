> **Language / Ngôn ngữ:** [English](battle-animation-skip.en.md) · [Tiếng Việt](battle-animation-skip.vi.md) · [中文](battle-animation-skip.md)

# Exit the battle performance (press X)

2026-09-25. After entering the battle, press **X** (Keyboard It is enabled by default and has no settings.

Implemented in [`battle_animation_probe.hpp`](../../src/host/battle_animation_probe.hpp), hung in `load_00121560_func_801C9710` (show main loop) and `load_000AB160_func_801DFBD0` (map per frame dispatcher). The address comes from static analysis and real machine verification, and the running record is in `build/recomp/debug/`.

**2026-09-26: Both parts have been completed and verified on the actual machine** - After aborting and returning to the map, the map follows the original process of "off animation" to calculate damage, draw numbers and HP bars, deduct blood, and issue rewards. For the method, see [Return to the original animation branch](#交还给原版的关动画分支).

## Already done: Abort

The performance state machine is in `D_80250000`, and the main loop is in `801C9710`. When pressing X:

1. The status byte is written to 21 (ending status), and the frame count `D_8025020C` is cleared.
2. Directly send the fadeout request `80099814(5, 1, 2)` for it, and set `D_80250205` to 1 to avoid sending status 21 again.
3. Status 0..20 are all accepted, so you can press it in the first frame of the battle; status 21 and above are excluded, and the ending is already fading out.

**Cannot use the original Z+START abort**. That path is set to `D_80225810`, the branch of `801C97E4` will be adjusted to `800A5138` and then select game mode 7 or 0x11 - which is the title/reset route. In actual testing, the level was thrown directly back to the title screen (`build/recomp/debug/20260925T023507.767082Z`). Its semantics is "exit this battle level", not "skip this animation".

State 21 originally had to wait until `801C9DD0` reported that the lens was stable and the frame count exceeded 10 (`slti 0xA` of `801C813C`) before fading out by itself. The actual measured end-to-end time was 7.8–8.8 seconds. Since the player has expressed that he doesn’t want to see it, just send it directly.

**WHY IT'S SAFE**: The real heavy cleanup (`8008B950` freeing all 300 sprite slots, `8008DB2C`, `8008AC78(4)`) runs the shared ending segment **after** the fadeout in `801C9710`, not in a skipped state.

**There is no "jump to counterattack" function**. Push the state machine forward (4 → 10) and it looks right on the state track. The picture is bad: states 3..9 are where the sprites, atlases, and driver lines for this round are loaded. State 9 (`801C7960`) also needs to run its own cleanup, while state 10 (`801C7BC0`) only moves the camera. After skipping, the counterattacking party does not appear and the dialog boxes are stacked together. Abandoned.

## Two paths of the original version

This section corrects an earlier statement in this article ("Damage is calculated from substate 2 of the 0x4B chain"). Substate 2 is the "next round" step. Reading the previous round's table is used as input, not the entrance; the damage is actually settled before the performance.

**State 24 (`801D6534`) is the entire attack process**, sub-state table `D_80217CC4`:

| Substate | Function | Effect |
| --- | --- | --- |
| 0 | `801D4794` | Create battle table `8018B6E8` (step size `0x5C`: +0 handle, +4 unit record, +8 weapon, +0x14 damage caused, +0x26 reaction code) |
| 1 | `801D5064` | Our attack confirmation page (host's `battle_confirm_step`) |
| 2 / 3 | `801D5294` / `801D5404` | **Settlement `801F7D6C`**: Hits/damage are all counted and written into the battle table; when the enemy attacks, 2 is the defender's response page |
| 8 | `801D5898` | `801DF96C`: `D_801602FA = 4`, the status changes to `0x4F` (idling), the next frame distributor adjusts `801D4E6C` |
| 4 | `801D5498` | **The landing point after turning on the animation**: `801FCA78` Silently apply the result, and then 9 |
| 9 | `801D5E88` | `801FC160` Send experience and funds frame |

**Fork `801D4E6C`** First adjust `801FC994` (just ask "Will the defender be shot down", don't change anything), then look at the switch `8015DDA8 & 4` (set = turn off animation):

```
动画开：80080188(2) 装战斗 overlay，80099814(5,1,2) 淡出。
        战斗 overlay 是纯演出，读 801F3578 填好的演出方块 800F97E0，从不写名册。
        回来时 801C7168（D_8022722C==1）把地图放回状态 24 子状态 4：
          801FCA78 → 801FB460：开关位清零 → 把 HP 直接写进名册、不排回合
                   → 801FC83C 扣 EN／弹药、气力 +5、清精神位
          然后子状态 9 发奖励。玩家看不到任何数字——动画已经演过了。
动画关：D_80228528 = 0；8009DB8C()；
        （D_8022796C==1 时：8008B888(0x9C) 释放，镜头对准守方格，801CBEB8）
        同一个 801FCA78 → 801FB460：开关位置位 → 不动名册，
                   把每一回合排进表：D_802277E8 回合数、D_802277E9[] 目标句柄、D_80227862[] 伤害
        回合数为 0 → 801C29DC(D_80172EE4) + 801C8AB4；否则 D_80172EB0 = 0x4B、D_80172EB2 = 3
        D_8022731C = 0、D_8021F464 = 0；最后给两个参战单位打「已行动」位 0x40
```

**Status 0x4B (`801D92B0`) is just a show**, sub-state table `D_80217D4C`: 3 takes the target and damage of this round, 4 waits for 20 frames to put hit effects `801E3AE4`, 5 deducts HP from the roster frame by frame and uses `801FCC6C` to seed numbers, 6 numbers float, 7..10 The next turn or the ending - the ending is to return to ** state 24 sub-state 9**, where it merges with the path of the animation.

Therefore, the difference between the two paths is only one branch of `801FB460`: the switch position determines whether to "write the roster immediately" or "arrange rounds and let the 0x4B chain be slowly deducted."

## Return to the original Guan animation branch

After pressing X to abort, the map will still be in state 24 substate 4 when it comes back. The host sees `D_80172EB0 == 24 && D_80172EB2 == 4` in the dispatcher hook (before `801DFBD0`) and needs a result display, so it replaces substate 4 and runs the forked animation branch (`801D4E6C` from `.L801D4EE0`, `replay_animation_off`):

1. `D_80228528 = 0`, `8009DB8C()`
2. Write back the `D_8022796C` and `D_80227250/54` recorded in the forked frame (they are in the area covered by the combat overlay; the forked frame is the frame where the distributor sees `D_801602FA == 4` and the switch bit is cleared. The hook runs before the distributor and can just read it)
3. Temporarily set bit 4 of `8015DDA8`, adjust `801FCA78`, and then restore it - only `801FB460` reads this bit, which determines whether to schedule rounds or write rosters
4. The number of rounds is 0, go `801C29DC` + `801C8AB4`, otherwise the state is 0x4B substate 3; clear `D_8022731C`, `D_8021F464`

No input is required: the battle table, roster, and `D_80172EE2` are all under the overlay. The battle overlay only reads the battle table (`80221B5C` in one place); the roster HP is still the pre-war value because substate 4 has not yet run; `801FC994` and the actioned position have already been done when forking, so there is no duplication. After that, 0x4B chain calculates, performs, and buckles by itself. The rhythm, sound effects, and crash overflow processing are all original. The ending is as usual with 9 rounds of rewards.

**RNG**: `801FCA78` will originally run in sub-state 4, and there will be no extra playback; the rest is the performance of the 0x4B chain, which is consistent with the off animation.

**Real machine results** (`build/recomp/debug/20260926T014604.081648Z`, enemy ムゲ兵 3000, attack ミニフォー 2800, state 3 press X):

```
replay-animation-off  hp_before [3000, 2800]  rounds [{target 98, damage 1029}]
chain-done            hp_after  [1971, 2800]
ui-text.jsonl         " -1029" 逐位浮现，map_state 75 sub 6
```

`anim-abort-t4.png` is the scene of the animation: next to the attacked unit, `-1029` outlines white text and blue frame HP bar; `t5` is the response page for the next game. 3000→1971 is consistent with the baseline for the full show.

The other two situations are also passed (slot 0 in the battle table is the attacker, slot 1 is the defender):

| Situations | Runs | Rounds | Roster |
| --- | --- | --- | --- |
| Enemy attack, counterattack round status 12 Press X | `20260926T015443.874339Z` | `{98, 1544}` | 3000→1456 |
| Our attack (`--player`), status 3 press X | `20260926T020357.464905Z` | `{98, 1609}` | 3000→1391 |

### Detours taken

- **The host draws numbers by itself** (`801FCC6C` + `801FCF00` per frame) can be drawn, and the measured `-200` appears normally. But there was no damage value available at that time - the roster was still the pre-war HP, and "Performance Cube − Roster" was not damage; and the slots in the combat table were regarded as performance cube subscripts, and the actual measurement showed `hp=3000/2800` (extremely long health bar exceeding the upper limit).
- **Entering 0x4B chain from substate 0** crashed three times in a row: `D_802284DC` null pointer (`801FCA78` is the only writer through `801FC110/801FC45C`), `D_802277E9[0]` are cleared to 0, and the legal handle starts from `0x42`, `801FB8B4` The pointer parameter is a wild value. The root cause is that substate 2 is not an entry - it is "next turn", reading the previous turn's table. The correct entry is the fork branch itself: `801FCA78` and then directly enter substate 3.
- **Manually fill in `D_80228530` six cells** Can't draw anything: `80209900` is only referenced once in the entire map overlay, which is `801FCC6C`. At the end, it is registered to `8008B4F4` when the sprite is drawn callback.
- The return value of **`801FCF00` is inverse**: 1 is returned only after all six cells have reached state 3, non-zero = **End**.
- **The grid coordinate table step size is `0xC4`** (indexed by handle), not `0x34`.
- **`8008B888(id)` is released, not loaded**: Only when `D_800FFA71[id]` is non-zero will the three slots be released and `8008198C` adjusted. The `8008B888(0x9C)` in the fork was to clear the elves in the aiming phase.

## Verify

[`check_battle_animation.py`](../../tools/recomp/debug/check_battle_animation.py), mini-level `config/recomp/mini-stages/battle-ui.json`:

```bash
SRW64_BATTLE_ANIMATION_PROBE=1 .venv/bin/python tools/recomp/debug/check_battle_animation.py --mode abort --at 3
```

- By default, the phase ends in a space, allowing the enemy to attack and confirm on the response page; `--player` is changed to our active attack (Unit Menu → Attack → First Weapon → First Target), covering another caller of the fork
- `--mode baseline` records the state sequence without pressing the button; `--no-anim` records the performance of the map when recording the level animation for comparison.
- `--pad` uses handle R2 instead of keyboard
- Assertions: `jumped-to-winddown`, `replayed-animation-off` (the frame where the hook took over substate 4), `rounds-queued`, `roster-untouched-by-animation` (roster HP when forking is the same as when replaying), `chain-done`, **`hp-settled-like-animation-off`** (final HP of each participating unit = pre-battle HP − Damage entered into the table, clamped to 0), `damage-redrawn` (numbers really appear in `ui-text.jsonl`)
- When the script exits, it will always be `Session.quit()`; the key condition is `state >= --at` rather than equal, because polling the trace file will race against the state machine

## Cannot press and hold X in advance

X is "Cancel" on the pre-battle confirmation page (`battle_page.cpp` maps back to `0x4000`). Pressing and holding it to confirm will prevent the battle from starting at all. This is a semantic conflict, not a bug.