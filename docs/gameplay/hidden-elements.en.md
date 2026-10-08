> **Language / Ngôn ngữ:** [English](hidden-elements.en.md) · [Tiếng Việt](hidden-elements.vi.md) · [中文](hidden-elements.md)

# Hidden factors, persuasion and route divergence: script and code implementation

2026-10-01, the second round of comprehensive static verification. Object is locked Japanese version Rev 0 `rom.z64`: **all 1,812 events** of the script IR (`assets/original-data/records/stage_events.jsonl`) are scanned one by one (conditional blocks, protagonist and department segments, select limbs, type 2/7/9 header threshold), and the involved decisions are read into the resident code (`build/recomp/cpu-scan/resident/`) and overlay (tactics `load_000AB160`, combat `load_00121560`, between scenes `load_0008F4B0`, world map `load_000A7EC0`, protagonist selection `load_001090A0`). The "previously unseen", "unchecked" and "inferred" left over from the first round (2026-09-17) have all been changed to code or script conclusions. **The game has not been run in this round, nor has it been written back to ROM**; the conclusion has been decided, but the points worth reviewing with a save are concentrated in Section 10.

Community guide [Akurasu Wiki: Super Robot Wars/64/Secrets][wiki] is only used for comparison and not as a basis for its Flow Chart. Section 6 identifies **Consistent**, **Different**, **Akurasu Not Included** item by item; Sections 7 and 8 summarize the latter two categories respectively.

Writing convention:

- `S49` is the scene number (level title id − 281), and the level name is the original Japanese name decoded by ROM, making it easy to search in the data browser.
- The event address is the ROM offset (such as `001bf55c`), `@520` is the instruction offset within the event.
- **Rounds are always written as screen rounds** (numbers on the game HUD). The original value in the script starts from 0, screen turn = original value + 1, see Section 4.1.
- `varN` refers to the 2-bit script variable N.

## 1. Conclusion Summary

- The game does not have a dedicated hidden element system. All conditions are implemented using 200 2-bit script variables (`8015E818`): 0–54 are saved across levels, which are the progress of hidden features and routes; 100–139 are single-level temporary variables. **In a new game, all 200 variables are set to 3** (`800A4790`, code fact), so 3 generally means "not started/failed".
- **The preconditions for persuasion are written in the type 9 event header**: `[9, 说服者, 对象, 门槛变量, 门槛值]`, `FFF8` means no threshold. The resident function `800A4634` is responsible for checking and selecting: the persuader is the main driver of the action unit, the event has not been executed, the threshold is met, the two parties are adjacent up, down, left, and right, and the first one is taken according to the registration order. The threshold chain for all 71 persuasion events is read out (Section 3).
- The threshold variables of type 2 (defeated) and type 7 (number of survivors) are **not triggered** when equal to 3; the first word in the header of type 6 (all enemies destroyed) is the **latest** round; `3E04 n` is equal to "screen round ≤ n" (section 4).
- The variable table is completed to 0-54 with all the writing points and reading effects of each variable; 45, 53, and 54 are read by the native code (Shisui Mirror display, Fortress バルジ landmark, flagship downing lines), 46 has no actual effect (section 5).
- An item-by-item comparison of about 60 items on the Akurasu Secrets page (Section 6): 30 differences in conclusions (Section 7), and more than 40 conditions, disagreements, and results not included in Akurasu (Section 8, including new discoveries N1–N17 from the full scan).
- Combination skills are not unlocked through the plot: `8020178C` Each time a weapon is listed, the locked position of the combination skill will be rewritten. `3D6F 1215` (Double God's Finger) has no lasting effect; Ishiba's Sky Shocking Fist also requires that Ishiba's Shocking Fist has been unlocked (section 6.5).
- The only two remaining items that are truly statically inconclusive (Section 10.1).

## 2. Implementation mechanism

### 2.1 Variables

| Command | Function |
| --- | --- |
| `3E13 变量, 值` | Write |
| `3E0E` / `3E0F` | Add 1 / Subtract 1 (modulo 4), used as counter |
| `3E03 变量, 值[, v]` / `3E02 变量, 值` | Enter conditional block when equal to / not equal to |
| `3E10`–`3E12` | Press the selection register (item 1/2/3) to enter the conditional block |

The variable has only 2 bits, and a factor can have up to four positions. Common usage: `0`, `1`, `2` indicates progress, `3` indicates not started or failed.

**Initial value (code fact)**: The protagonist chooses `load_001090A0:801C69D0` to call `800A4790`, which writes 26 half-words starting from `8015E818``0xFFFF` (`800A479C`–`800A47C4`), and all 200 variables are 3.

**Reset after entry** (`8009DE7C`):

| Object | Processing | Evidence |
| --- | --- | --- |
| var100–114, var128–139 | Set to 3 | `8009E06C`/`8009E09C` loop |
| var54 | Set to 1 | `8009E0C4` |
| Select register `engine+0x994` | Set `3DD9` (item 1) | `8009E04C` |
| Persuasion slot number `engine+0x992` | Set to −1 | `8009E020` |
| 12 event groups | Clear and re-register | `8009DEC4`–`8009DEFC`, `8009DF3C` onwards |

var115–127 are not in reset scope, and scripts never read or write to them (var117–122 is also used by native code, see Section 5.2). var55–99, var140–199 have no reads or writes in all 1,812 events.

**Select register**: In the resident code, only `3D44` is rewritten to `engine+0x994`, which is retained within a level and stored in the interrupt archive (`800A47D4`) along with the variables. Therefore, when there is only one opening `3D44` in a level, the `3E10`/`3E11` of the event at the end of the level reads the opening choice (for example: S138 Cardo leaves the team, S32 is completely peaceful).

### 2.2 Source of judgment

| Source | Implementation | Typical examples |
| --- | --- | --- |
| Persuasion | Type 9 event, header with threshold; progress variable written in the event | アイナ, フォウ, プルツー |
| Select limbs | `3D44` and then use `3E10`–`3E12` branches | シーラ／エレ、エリカ、ナイーダ |
| Specified knockdown | Type 2 defeat trigger + `3E16` (ACC = the other side of the battle) + `3E08 角色` | カーツ（ブラッド）、キラル（ドモン） |
| Number of kills/level | `3E0D` (number of kills), `3E06` (level comparison) followed by `3E09`/`3E0B`/`3E0C` | Ginling, シルキー, フォウ |
| Engagement | Type 4/5 (after/before the battle); `3E17` Read "Should we take action in this battle?" | アイナ (engage first), ガラリア (cancel) |
| Present | `3E1B`: 1 on the map, 0 shot down, 3 not present or left | ロザミア, プル, シュバルツ |
| Survival, area, turn, HP | Type 7, Type 8, Type 0/`3E04`, Type 3 | アイシャ, ガトー, decisive death breakthrough game |

See Section 4 for the precise semantics of each trigger type and conditional instruction.

### 2.3 Persuasive events (type 9)

Type 9 is all about persuasion. The last two words of the event header `[9, 说服者, 对象, 门槛变量, 门槛值]` are preconditions (the directory `trigger.fields` marks all four words as "reserved", so they were not recognized in the first round). The checking and selection is done by the resident `800A4634`, which is called by the tactical overlay in two places: building the command menu (`801C9DFC`) and executing "say it" (`801DECE8`). The execution is completed by `8009EC3C` in event polling phase 6. After execution, the slot status changes to `0x2000`, and this level no longer matches; the execution mark is saved with the interrupt archive. The cross-level "Nth step requires N-1th step" is completely realized by the threshold variable. See Section 3 for the complete mechanism.

### 2.4 Driver Record Field

| Field | Conclusion | Basis |
| --- | --- | --- |
| `+5` | Level | `3E06` → `800A22CC` (ACC = !(A level < B level)) → `800A32C0`／`800A32EC` Find the first one in the three driver tables according to the role number, take `+5` |
| `+0x14` | Number of kills | `3E0D` There are 6 places in total, the readings are masterpiece ×2, Malik ×2, ブラッド, leopard horse; kill fund bonus `801F66C8` also uses `+0x14 ≥ 20` as the number of kills |

These two items in layout lock `conditions` are still written as "Roster [role]+0x14/+5" and will be renamed separately.

### 2.5 Joining, leaving and transferring

| Directive | Semantics | Evidence |
| --- | --- | --- |
| `3D5A 角色, 参数, 机体, 模式` | Mode 500 registration; `< 2000` represents the old aircraft number, that is, transfer; 2000 only deletes the driver; 3000 only deletes the aircraft; 4000 deletes both. Airframe 999 = Only the pilot is registered; Character 999 = Only the airframe is registered, skipped when deleting. Do nothing if the same pilot is already on the same aircraft (no harm done by double registration). 3000 in the original script are all called with role 999, which are all no-ops | `800A0B3C`, `800AAD28`, `800A3540` |
| `3D58 角色, 阵营` | Transfer the units present to the designated camp and join them on the spot (ガラリア, ヒルデ, アイシャ); the dropped parts in the new slot will be cleared when switching camps | `80210758` → `802106FC` |
| `3D45 组` | Deploy the sortie supporting record group. Record camp value 0/3 falls in our pool, and the driver will join the team directly if it is < 287 (early levels do not have `3D5A`); 2/4 are third parties | `8020ABB4`, `8020B154` |
| `3D59 角色` | No attacks allowed in this level | |
| `3D6B 角色, 机体, 1／0` | Set/clear the "no attack" mark; `3D73 n` is set in batches according to the resident list, `3D74` is cleared all | `801C78A0` |
| `3D6C 机体, N` | The five items and all weapons of the first unit in our pool are set to `min(N, 上限)` | `800ACA1C` |
| `3D64 500, 500` | Make the character the second pilot of the current machine (アイシャ replaces ローレンス) | `800AB96C` |
| `3D70 主驾驶, 同乘者` | Shared ride (`3D70 186,182`: シルキー is attached to the トッド machine) | |
| `3D6F 武器` | Clear weapon instance `+0x22` bit 2 (unlocked); has no lasting effect on combo skills, see section 6.5 | |
| `3D5B n` | Funds + n×1000 | |

## 3. Persuasion mechanism

### 3.1 Conditions for "Shuoda" to appear in the command menu

The **main driver** of the cursor unit also has the number of actions (driver `+0x35 ≠ 0`; it’s okay to move it), and a certain type of 9 slot registered in this level also satisfies:

1. The first character in the header (persuader) is equal to the role number of the main pilot of the unit;
2. The slot is not executed (status `< 0x2000`), and no event is currently executing (`engine+0x97C < 0x2000`);
3. The threshold is met: the third word is `FFF8`, or `var[第 3 字] == 第 4 字`;
4. The unit with the 2nd word (object) is on the map (any camp will do, just match any driver on the object unit), and is adjacent to the persuader **up, down, left, and right** (the Manhattan distance is exactly 1, diagonal directions are not counted).

Evidence: Menu build `load_000AB160:801C9DFC`. `801C9EB8`–`801C9EC8` Write the main driver role number into `engine+0x9A8` (`D_801602F8`) and call `800A4634`; when the return value is ≠ −1 and the number of remaining actions is ≠ 0, add the menu item `D_8021DD88` (command 1, text `0x1FF` "speaks well"). The `移動` item also requires that it has not been moved yet, so convince not to look at it.

### 3.2 Selection of `800A4634`

Type 9 packets are at `engine+0x6F8` (packet base `engine + 0x14 + 类型×0xC4`). Within the group: `+0` number of items; `+4` 16 event pointers; `+0x44[i]` object; `+0x64[i]` persuader (changed to `0x2000` after execution); `+0x84[i]` threshold variable; `+0xA4[i]` threshold value (registration `8009DFA0`–`8009DFE8`).

The function loops in the registration order, takes the first slot that meets the conditions of 3.1, writes the slot number into `engine+0x992`, and returns the role number of the object's main driver; if there is none, write −1 (`800A475C`). The threshold reading variable goes to `800A2A84 → 800A496C` (subscript ≥ 0xC9 returns −1); the roster entries of both sides are looked up by `800A2BF4 → 800A2C18` (the slot of our state 2 is skipped); the adjacent comparison is in `800A4704`–`800A4738`.

Therefore, the object of persuasion is determined by the program, and the player cannot choose: when the same persuader sticks to two persuadable objects at the same time, he will only persuade the one at the top of the list. Example: In Common Battle Line (S61)/Brothers and Brothers (S76), when Yukari sticks to both Matsuda and Matsuda at the same time, he will only persuade Matsugat; In アクシズの Offense and Defense (Previous) (S88), when ジュドー is attached to both マシュマー and キャラ, it will only convince マシュマー.

### 3.3 Event header field

| word | field within group | meaning |
| --- | --- | --- |
| w1 | `+0x64` | Persuader role number (must be the main driver of the action unit); after execution, it will be changed to `0x2000` |
| w2 | `+0x44` | Object role number |
| w3 | `+0x84` | Threshold variable number; `0xFFF8` (−8) means no threshold |
| w4 | `+0xA4` | Threshold value: variable == value only appears "said" |

Among the 71 events, 24 were without threshold and 47 were with threshold. Threshold variables 2, 3, 6, 9, 11, 12, 13, 14, 15, 18, 22, 24, 26, 27, 29, 30, 32 are used, as well as single-level variables 128 and 129.

### 3.4 Execution process and action consumption

1. Menu command 1 → `801DECE8`: adjust `800A4634` again, write `+0x992`, select the special effect 0x35/0x36 according to the coordinates of both sides, `801EE838` plays the orientation special effect, and the status is set to 0x52.
2. `801DF22C` Wait until the special effect ends → `801DEBF4`: The status is set to 0x53, `D_80172F0A = 1`, polling phase `engine+0x9AA` (`D_801602FA`) = **6**, write down the persuader handle.
3. Event polling `8009E180` uses `8009E3B0(8,10)` in phases 0, 6, 1, and 2 for polling types 8 and 9. Type 9 handler function `8009EC3C` (`jtbl_800D0610[9]`) is only executed when `+0x992 ≠ −1` and `+0x9AA == 6`: the slot status is changed to `0x2000`, `+0x97C = 0x2000`, `8009EE98` On startup event, `+0x992` is reset to −1.
4. After the event, the `801DFF40`–`801DFF7C` check is completed and `801DEC68` is called: `+0x9AA` returns to 0, `801C29DC(说服者)` deducts an action and returns to the map.

One persuasion consumes one action of the persuader, regardless of whether the event content is effective or not.

### 3.5 Multi-step persuasion, cross-level and archiving

- **Inside level**: The slots that have been executed no longer match, and the next persuasion of the same pair of characters will naturally fall into the next slot that meets the threshold. The threshold variable of the second step is written by the event of the first step. Examples: Sadness しみのホンコンシティ フォウ ×2, 戦いの意は ミネルバX ×2, ランタオ岛／Despair ドモン→レイン.
- **Cross-level**: Re-register at the beginning of each level, and the execution mark will not cross levels. Cross-level prepositioning only relies on threshold variables (var0–54).
- **Interrupted Archive**: `80093278 → 80091ED0 → 800A4148` stores the slots with status `0x2000` in the 12 groups into `D_8016A1F0` bit by bit. The persuasion that has been executed after continuing the game is still considered to have been executed.
- Each group has a maximum of 16 slots (`8009DF8C`); the scenes with the most persuasion events (S57, S66) only have 4.

### 3.6 Failure in checking will also consume: one-time persuasion

`8009EC3C` marks the slot as `0x2000` before execution, and the conditional block in the event only determines which instructions to execute. So:

| Events | Failure Conditions | Consequences |
| --- | --- | --- |
| ロザミア（S41 `001b15cc`） | ゲーツ is still there (`3E1B ゲーツ` = 1) | Only dialogue is played, and the only slot in this level is consumed |
| プル（S85 `001cff84`） | グレミー is present (joined only after ≠ 1) | Dialogue only |
| プル（S98 `001dad58`） | グレミー has not been shot down (joined only after == 0) | Play dialogue only |
| プルツー（S132 `001d47fc`） | グレミー** is not in ** (register only if == 1) | Dialogue only |
| Empty event outside the route segment | The event content is only written in a certain protagonist/department segment, and can still be initiated on the other side | The slot is consumed and nothing is executed (`8009F0E8` skips unmatched segments) |

Empty events outside route segments: エマ `001a2124` (super segment), キリマンジャロ フォウ`001c7768`／`001c7790` (real segment), キリカ（マリア）`001cc108`／`001d6374` (super segment), エルリッヒ`001b1514`／`001b6ba4`（アークsection）、アイシャ `001ad258`／`001b6464`／`001b6c40`（マナミsection）、リッシュ`001b8928` (セレインsection). The persuader itself is limited to the protagonist and has no actual effect; "Speaking" will appear in three places: クワトロ→エマ(real system), カミーユ→フォウ(S57 super system), and Marika → キリカ (real system), but it will have no effect after persuasion.

### 3.7 There is no persuasive effect at the code level

`800A4634`, `801DECE8`, `801DEBF4`, `8009EC3C`, `801DEC68` do not write the camp, roster or level status of the target unit. Exiting (`3D46`), defeating the performance (`3D4F`), transferring to our side (`3D58`), registering (`3D5A`), and level victory (`3D4A`) are all completed by event scripts. Among all 71 events, only one directly ends the level: Hazama Yuu of the Sea and the Land (S20) The third step of フォウ `001a4420@512 3D4A`.

### 3.8 All persuasion chains

The "threshold" is the header w3/w4; the "write" only lists variables and instructions to change the situation.

| chain | event (scenario): threshold → write |
| --- | --- |
| アイナ | `0019f2cc` (S11): var128==0 → var12=0, exit (var128 is only written 0 by the type 5 battle event `0019f2a8` between シロー and アイナ) → `001a6368` (S24): var12==0 → var12=2, exit |
| ゲイル | `0019fc28` (S12): None → Break the performance, var0=0 |
| エマ | `001a2124` (S16): None → Super segment var1=0, exit |
| フォウ | `001a344c` (S18): None → var2=0; `001a347c` (S18): var2==0 → var2=1, exit; `001a43f4` (S20): var2==0 → Dialogue only; `001a4420` (S20): var2==1 → var2=2, `3D4A`; `001b4b58` (S128): var2==2 → Start delay slot 3 (level comparison, write var17); `001c7708` (S57): var2==2 → Break the performance, var17=0; `001c7768`/`001c7790` (S57): var2==0/1 → real segment var128=0 |
| アレンビー | `001a34e8` (S18)/`001a3cac` (S19): None → Exit, group 8, var3=0; `001b4cfc` (S128)/`001c7884` (S57): var3==0 → Exit, var3=1; `001d32dc` (S129 ドモン): var128==0 → var128=1; `001d32fc` (S129 レイン): var128==1 → script battle, var128=2; `001d7cac` (S137ドモン): var129==0 → 1; `001d7ccc` (S137 レイン): var129==1 → Exit, var129=2 |
| トッド | `001a6ad4` (S25): None → var6=0; `001ac1a8` (S33)/`001bd924` (S47)/`001acc08` (S62): var6==0 → var6=1 |
| アイシャ | `001ad258` (S34): None → var13=0; `001af7e8` (S38): var13==0 → 2; `001b6464` (S65): None → 0; `001b6c40` (S66): var13==0 → 1; `001c6134` (S56): var13==0 → 2 |
| ヒルデ | `001af71c` (S38): None → `3D58` transfer to our side, var16=0 |
| リッシュ | `001af760`（S38）／`001b8928`（S69）：var14==1 → var14=2 |
| エルリッヒ | `001b1514` (S41): var9==0 → var18=2; `001b6ba4` (S66): None → `3D58` transfer to us, var18=2; `001bfaf0` (S49): None → Exit, var18=0; `001c6094` (S56): var18==1 → Exit, var18=2 |
| ロザミア | `001b15cc` (S41): var15==0 → Exit, register, var15=1 when ゲーツ is not present |
| マーグ | `001b42b8`（S45）／`001c8384`（S59）／`001bb31c`（S75）／`001bbfdc`（S136）：None → var22=0; `001c94e4` (S61)/`001b7af0` (S76): var22==0 → var22=1; `001cb548` (S77): var22==0 → var25=0 |
| ロゼ | `001c9878` (S61)/`001b7e38` (S76)/`001cb870` (S77): var26==0 → var26=1; `001d5ba4` (S91)/`001d3dd8` (S130): var26==1 → Exit, var26=2 |
| ナイーダ | `001b4370`（S45）／`001c9938`（S61）／`001b7e60`（S76）：None → Exit, var23=0 |
| キリカ | `001cc0d8`（S78）／`001d6344`（S92）デューク：None → var24=0；`001cc108`（S78）／`001d6374`（S92）マリア：var24==0 → Super segment breaking performance, var24=1 |
| ミネルバX | `001b68f8` (S66): None → var128=0; `001b6928` (S66): var128==0 → AI exits, var128=1 |
| プル | `001cf998` (S84): None → Exit, var27=0; `001cff84` (S85): var27==0 → When グレミー is not present `3D58`, var27=1; `001dad58` (S98): None → When グレミー is shot down var27=1, `3D58` |
| プルツー | `001d0e84`（S141）／`001db848`（S99）：var27==1 → var30=0；`001d1438`（S87）／`001dc174`（S100）：var30==0 → var30=1; `001d47fc` (S132): var30==1 → defeat the performance when グレミー is present, register, var30=2; `001dc7a4` (S101): var30==1 → var30=2, defeat the performance, register |
| マシュマー／キャラ | `001d17c0` (S88): var29==0 → var32==0, var29=1, var32=3; `001d17ec` (S88): var32==0 → var29==0, var32=1, var29=3 |
| ミリアルド | `001cf654` (S84): None; `001dfa00` (S103): var11==0. Both have only dialogue |

There are 71 events in total; for an item-by-item list (including paragraphs and summaries of all instructions within the event), see the second-round verification manuscript `persuade.md`.

## 4. Trigger threshold and round

### 4.1 Round Count

`D_8010F5EA` is the round count, **starts from 0**: add 1 when the tactical HUD is displayed (`load_000AB160:801D1324`/`801D1338` calls `sprintf` after `addiu a2,a2,1`); `801DF994`/`801DF9A4` copy it in `engine+0x9AC`; `801FA9D8` Add 1 at the end of the turn. The actual machine record of `docs/script/mini-stage.md` also confirms that it is 0 in the first round.

**Screen turn = original value + 1**. The "number of rounds = N" printed by the script reader is always increased by 1.

### 4.2 Header semantics of trigger type

| Type | Name | Header and judgment | Code |
| --- | --- | --- | --- |
| 0 | Start of round | `[0, 回合, 阶段]`: `engine+0x9AC ≥ 回合` and phases are equal. Original value N = **Turn N+1 of the screen** | `8009E598` |
| 1 | Delay count | Started by `3D52 槽, N, 阶段`: the count is set to N, and the last round is recorded as `0xFD`; the first poll only records the current round, and is decremented by 1 for each subsequent round, and is executed when it is 0 and the stages match (4 = arbitrary). Only poll at `engine+0x9AA == 0` (beginning of phase, end of each action and return to idle). Slot number = registration sequence of type 1 events in this level. The count started in the opening event, after N round changes, is **Turn N+1 of the screen** | `800A05D0`, `8009EB5C`, `8009E180` |
| 2 | Defeat/Retire | `[2, 门槛变量, 角色]`. Threshold variable does not trigger when 100–115 and value == 3; 0 = no threshold | `8009E604` |
| 3 | HP below | `HP/最大HP×100` (float, lower limit 1) **≤** threshold and unit is present | `8009E6E4` |
| 4/5 | After/Before the battle | The two characters are matched with the attacker or defender (0 = any), the order of attack and defense has nothing to do; the map weapon does not trigger (the defender pointer is 0) | `8009E9B4`, `8009EA88` |
| 6 | All enemies are destroyed | The first word in the header is the **latest** round: the original value < the current round is not triggered; 254 means no limit. Full ROM only S45 `001b42e4` uses 4 (within the 5th round of the screen) | `8009E834` |
| 7 | Faction remnants | `[7, 阵营选择, 上限, 阶段, 门槛变量]`: Faction selection 2 = third party (`+0x9B2`), otherwise the enemy (`+0x9B1`); **triggered when the number of survivors ≤ upper limit**; not triggered when the threshold variable value == 3 | `8009E8B4` |
| 8 | Area arrival | Coordinate code `x0 = 值/10`, width = `值%10`, range `[x0, x0+宽)`, y is the same. Target 21 = the first player in the captain list `D_800C9A08` (our flagship), 500 = any of our units. Mode `FF`: Triggered when a unit enters; Mode `FE`: Each unit entering immediately withdraws from the map, and it is triggered only when all camp 0 withdraws | `800A4288` |
| 9 | Persuasion | See Section 3 | `8009EC3C` |
| 12／14 | Opening/end of the chapter | | |

### 4.3 Conditional instructions

| Directives | Semantics | Code |
| --- | --- | --- |
| `3E04 n` | `D_8010F5EA < n`, that is, ** screen round ≤ n** | `800A2344` |
| `3E1B 角色` | 1 = on the map; 0 = shot down; 3 = not on the scene or has left the map (retreat, escape). Status table `D_8015DE90`: Write 0 for the crash path `801FAFFC`, write 2 for the departure path `8020C664`/`8020CA80`/`8020CFF8` (read as 3), initial value −1 (read as 3). The "0 absent/3 exited" written in the directory is inaccurate | `800A1F7C → 800A3990 → 800A293C` |
| `3E16 角色` | ACC = the character number of the other party | |
| `3E17` | ACC = `engine+0x9B6`: The attacker is our side → 1; the defender is our side and the response is not defense/avoidance → 1; otherwise 0. Also write 1 when the attacking side of the map weapon is our side | Write `801F3F88`, `801FE794` |
| `3E15 阵营` | ACC = number of units in this camp | |
| `3E0D 角色`／`3E06 A, B` | Number of kills/level comparison, see section 2.4 | `800A22CC` |

Idiomatic writing method: `3E14 v` or `3E03 变量, 值, v` within the block sets ACC as the mark of "this block has been executed", and the subsequent `3E0A v`/`3E08 v` is the "else"/"then" of this block.

### 4.4 Switching conventions for threshold variables

100–114 is set to 3 when entering the level, so the threshold type 2/7 triggers **closed by default**, and the script uses `3E13 10x, 0` to open and `3E13 10x, 3` to close. Example: Fist of Despair and Sadness (Later) (S137) `001d7c94` After writing var100=0, `001d7da8` can be triggered when the remaining value is ≤ 10; Gorgeous なるル・カイン (S14) Write first when the guerrillas reach the escape zone var100–102=3 Turn off your own break trigger before exiting. The directory (`trigger.fields`) is the opposite of the "threshold variable must be 3" marked in the old reading script.

### 4.5 Victory and defeat conditions

`3D65 胜, 败` writes `engine+0x996`, and the only reader of `load_000AB160:801C68F0` (via `800A3524`) is displayed as "win = text 5567+v, lose = text 5593+d". It only displays: pass depends on the script `3D4A`, failure depends on the script `3D4C` or the engine's own total destruction judgment (`801FF934`, `3D61` can be paused).

## 5. Progress variable table

### 5.1 Cross-level variables 0–54

"Writing" is in order of appearance; "Reading and effects" only lists reads that change the formation, formation, attack, process or native behavior. For reading points that only change lines, see Section 5.3.

| Variables | Purpose | Writing | Reading and effects |
| --- | --- | --- | --- |
| 0 | ゲイル | S12 Persuasion `0019fc28@170` → 0 | 0 → S32 The real segment registration at the end of the level ゲイル＋グライムカイザル (`3D6C` 3 segments); S52 opening/S53 Real stage registration at the end of the pass (4 stages); S83/S93 re-registered and prohibited from attacking; S83/S131/S93/S94 changed to Yuru as the escort (N5) |
| 1 | エマ | S16 opening real segment → 0; S16 persuasion (super segment) → 0; S43/S44 opening, S46 end of level real segment → 0 (repeat) | 0 → S16 delay slot 1 super segment registration エマ＋ガンダムmkⅡ; S17 The opening real segment is registered as エマ＋ジェガン (1 segment); S26 super type ==3 when カミーユ rides mkⅡ to appear |
| 2 | フォウEarly part | S18 Persuasion → 0 → 1; S20 Persuasion → 2 | Persuasion threshold (S18/20/128/57); 2 → S128 The opening カミーユ cannot attack (in the 3rd round of the screen or when the enemy is ≤8, take Z to arrive), S57カミーユ cannot attack; S57 enemy reinforcement group press ==2 to select |
| 3 | アレンビー | S18/S19 persuasion → 0; S128/S57 persuasion → 1; S129 end of the pass var128==2 → 2; S137 end of the pass → 1 (rescued) or 3 | Persuasion threshold; 1 → S128/S57 At the end of the level, register アレンビー＋ノーベルガンダム; S129/S137 opens persuasion when ∈{0,1}; S137 ≠1 when the berserker appears; S41 end of the level ==1 → `3D6F 1215` (no lasting effect) |
| 4 | ガラリア | S20 Delay slot 1 `001a41a4@136` → 0 (at the same time `3D58`) | 0 → S33/S48/S63 Opening "Ensure programming" re-registration (no effect when already programming); シルキー condition; S20フォウ exits at the third step |
| 5 | エリカ | S23 Final Selection Item 1 → 0 (one each for ブラッドdan and マナミdan) | Change lines only |
| 6 | トッド | S25 persuasion → 0; S33/S47/S62 persuasion → 1; S81/S92 shot down → 3; S81/S92 did not appear at the end of the level → 3 | Persuasion threshold; 1 → S81/S92 Our side deploys トッド in the third round of the screen |
| 7 | シーラ／エレ | S26 Select 1 → 0 at the beginning, select 2 → 1 | S26 Map and our team; S33 (IA) The unselected party appears midway and is removed from the same level; S62 Registration at the beginning, S63 is removed at the end of the level (CP); S48 appears, removed from the same level (OZ); the remaining 100 lines |
| 8 | Rura (front) | S27 Three opening choices → 0/1/2 (real system) | S30 Opening decision var9 |
| 9 | レラ branch | S30 opening → 0/1 (see section 6.1); S63 opening ==0 → 3 | S42 The real relationship at the end of the pass ==0 → S43; S41 エルリッヒ persuasion threshold; S140 opening plot; more than ten lines of dialogue |
| 10 | OZ side | S30 end of the stage, choose 1 → 1, choose 2 → 0 | S123/S124 ==1 → S57; S137 end of the stage ==1 → choose one of the mass-produced νガンダム; S103/S104/S105 enemy group |
| 11 | Complete Peace | S32 Select item 3 at the beginning → 0 (one for each of the four protagonists); S32 Select 3 at the end of the level and then choose 2 → 1, otherwise → 0 | S32 End of the level ==1 → S62; S123/S124 ==0 → S42; FA Hundred Shika Kai; S103 end of level ==0 → ノイエ・ジール; S84 opening ==1 → ドロシー group 14; S103 persuasion of ミリアルド threshold; S103/S104/S105 enemy group. OZ does not go through S32, keep 3 |
| 12 | アイナ | S11 persuasion → 0; S24 opening super segment → 0; S24 persuasion → 2 | persuasion threshold; 2 → S24 end of the pass registration アイナ＋アプサラス |
| 13 | アイシャ | IA: S34 persuasion → 0, S38 persuasion → 2, S40 remaining ≤9 when Marino is not there → 3; CP: S65 → 0, S66 → 1, S69 → 2; OZ: S49 choose 1/2 → 0, S50 choose 1 at the end of the pass → 0, S56 Persuasion → 2 | Persuasion threshold; 2 → S40 `3D58` (IA), S69 `3D58` (CP), S57 Check-in registration (OZ); スイームルグS transfer timing; S57 マナミ cannot attack |
| 14 | リッシュ | S35/S65 Before the battle, choose 1 → 0, choose 2/3 → 1; S38/S69 Persuasion → 2; S49 Choose "Reply" → 1; S50 At the end of the level, choose 1 → 2; S51/S108 Opening 1 → 2 | Persuasion threshold; IA S40 Opening ==2 Registration; CP S70 End of level registration; OZ S51/S108 opening registration (3 paragraphs); S38 opening ==1 One more confession |
| 15 | ロザミア | S37 When the second wave appeared, カミーユ was not there → 3; ゲーツ was shot down and ロザミア was present → 0; ロザミア was shot down → 3; S41 was persuaded and ゲーツ was not present → 1 | S41 Persuasion Threshold |
| 16 | ヒルデ | S38 Persuasion → 0; S38 ヒルデ was shot down → 3 | 0 → S38 Sekimo changed to register No. 266 ヒルデ＋トーラス; S45 When ノイン joined the team ==0 Only register the driver, otherwise bring Torosu |
| 17 | Fukuru's second chapter | S128 Delay slot 3 level comparison is established → 0, not established → 1; S57 Persuasion → 0; S57 Fukuru was shot down → 1/3 | 0 → S128/S57 Fukuru registered at the end of the pass (inorganic body) |
| 18 | エルリッヒ | S41 Persuasion → 2; S41/S56 End of the Pass 1 → 3; S66 Persuasion → 2; S49 Persuasion → 0; S56 Survival ≤13 When Aiko is present → 1; S56 Persuasion → 2 | Persuasion threshold; S41/S56 End of the Pass ==2 Only one of the two options is available, choose 2 → var128=1 → S123; S66 Registration at the end of the pass |
| 19 | キラル | S41／S56 キラル was shot down by ドモン → 0 | S104 When the first wave was completely wiped out ==0 → キラル appeared with team 6 |
| 20 | カーツ count | 8 levels of カーツ defeat event: カラッド fell → +1, to 2, press back to 1 | Three different levels ==1 → var21=0; S102 end of level (original flaws, see section 6.1) |
| 21 | カーツ results | S41/S56/S66 defeat event → 0; S66 end of level 0 → 2; S124 end of level → 1 (insufficient kill)/2 | S41/S56 end of level ==0 → S124, ==3 → When the switch is completed, the transfer function; S42/S57 opening ==1 → Transfer; ==2 7 lines of the switch |
| 22 | マーグPersuasion | S45/S59/S75/S136 Persuasion → 0; S61/S76 Persuasion → 1 | Persuasion threshold; only affects lines |
| 23 | ナイーダ | S45／S61／S76 Persuasion → 0; S77 opening choice 2 → 2; S91 opening choice 1 → 1, choice 2 → 2 | S77／S91 opening choice ==0 only the choice: choose 1 Register ナイーダ＋ダブルスペイザー; choose 2 and she will self-destruct, and デューク cannot attack; S91 When choosing 2, the enemy group will change to group 6 |
| 24 | キリカ | S78／S92 デュークPersuasion → 0; マリアPersuasion → 1 (Super Segment) | Persuasion threshold; 1 → Check-end registration キリカ (driver only) |
| 25 | Marathon's lines | S77 persuade Marathon → 0; S61/S76 Marathon was shot down by Marty and var22==1 → 1; S77 Same conditions and var25==0 → 1 | Only select Marathon's exit and subsequent lines |
| 26 | ロゼ | S61／S76／S77 マーグ was shot down by タケル and ロゼ was present → 0 (without looking at var22／25); persuade ロゼ → 1; S91／S130 persuade → 2 | persuasion threshold; 2 → S91／S130 Sekimo Registration ロゼ＋ゼーロン (3 paragraphs) |
| 27 | プル | S84 persuasion → 0; S85 persuasion and グレミー is not present → 1; S98 persuasion and グレミー is shot down → 1 | プルツー threshold; キュベレイmkⅡ color change conditions |
| 28 | ルー | S85 When Emperor ルー was defeated, ルー was present → 0 | Only lines changed (S85/S86/S132) |
| 29 | MASTER | S86 presence when the delay slot is 1 → 0; S88 persuasion → 1, persuasion キャラ → 3; S103 reinforcements at the end of the level did not appear → 3 | persuasion threshold; 1 → S103 our phase deployment group 4 in the 8th round of the screen |
| 30 | プルツー | S141／S99 → 0; S87／S100 → 1; S132 (グレミー is present)／S101 → 2 | Persuasion threshold; 2 → Color change conditions |
| 31 | ムゲ／Earth Circle | S89／S139 At the end of the level, choose 1 → 0, choose 2 → 1 | When ==1, the color change selection occurs in the same event; S104 lines |
| 32 | キャラ | Symmetrical with var29 | 1 → S103 Screen Round 8 Deployment Group 5 |
| 33, 34 | — | Not used | — |
| 35 | Silver Bell | S32 The final masterpiece is shot down ≥20 → 0; S107 Opening ≥30 → 0 (registered at the same time) | Only lines are changed; S103 No attack allowed |
| 36 | Beast Fighter Base | S78 At the end of the level, choose 2 → 0, choose 3 → 1 (choose 1, do not write, keep 3) | S81 opening plot; `3E02 36,0` → `3D6F 19` (Shipotian Jingquan) |
| 37 | ガトー | S49 area: flagship → 0, シロッコ → 1, バスク → 3; third party is completely destroyed (after var101 is opened) → 0; close end 1 → 3 | S49 close end 0 → register and go to S51, 3 → S108; S54/S60/S98 Formation; S97/S138 leaving the team |
| 38 | ロームフェラ | S107 Choose 1 → 0 at the end of the level, choose 2 → 1 | S107 Where to go; S56 エルリッヒ conditions |
| 39 | Niu Hungry Ghost | S25 Niu Hungry Ghost is defeated `001a6944` → 0 | S26 When all enemies are destroyed ==0 → Group 11 Niu Hungry Ghost (carrying composite armor) reinforcements |
| 40 | シルキー | S81／S92 Screen Round 3: var6==1, var4==0, Malta was shot down ≥30 → 0; Tota was shot down → 3 | 0 → Register シルキー and `3D70` Ride with Toto |
| 41 | — | Not used | — |
| 42 | Purification enemy composition | S62 Furuya HP ≤30% `001acc24`: Write 3 first; Furu is present → 0; Ani is present → 1 (Furu is not there)/2 (Furu is also there) | S63 Opening value-based deployment group 0–3 (Who is the enemy between アレン and フェイ) |
| 43 | ハマーン | S138 Choose 1 → 0 in the opening, choose 2 → 1; S100 choose 1 → 0 in the opening, choose 2 → 1 | S97 end of the pass var37==0 ∧ var43==0 → ガトーLeave the team; S101 opening lines |
| 44 | Belonging side | S34 end of pass → 0 (IA); S136 end of pass → 0 (CP fights alone); S76 end of pass → 1 (CP follows Toro); S46 end of pass → 1 (OZ) | S103 ==1 → ノイン cannot attack; S103–S105 70 Lines |
| 45 | Shimizu Shisui | S39 Survival ≤10, S55 Survival ≤10, S70 Delay slot 0 → 0 | **Native read**: `800A4BB8` returns var45==0; inter-field `load_0008F4B0:801CA27C`, tactics `801E59D0`／`801E5BE8` Added "Mirror Shisui" (Text 241) to the ドモン skill column; battle line list `D_80222F20` Press ==0／==3 to select a set of lines for each of the 5 pieces of シャッフル alliance special kill |
| 46 | シュバルツ | S137 end of the pass var130==0 → 0 | Read the selected lines only once in the same event; the line list `D_80222F20` has a line pointing to it, but `80222664` actually compares the var45 of the next line, and the value is discarded. **NO OTHER EFFECT** |
| 47 | クェス | S105 シャア was shot down by アムロ, var130==3, クェス was present → 0 | 0 → Registration at the end of the pass for クェス＋ヤクト・ドーガ (6 paragraphs) |
| 48–50 | Link Battler | End of linkage level: 48 (S109/115/117/121), 49 (S111/115/119/121), 50 (S113/117/119/121) → 0 | Click here to join the team natively ([Link Battler linkage](link-battler.md)); main line 23 Lines |
| 51 | ちずる | S138 The leopard horse is shot down at the end of the pass ≥15 → 0; S97 The leopard horse is present at the beginning → 1; S97 The end of the pass 0 → 1 | S99 The opening ==1 → `3D59 145` (the leopard horse cannot attack); S97/S98/S99 plot |
| 52 | Limited time divergence | S81 opening → 3; S81 when passing the level (area FE or all enemies are destroyed), the screen turn is ≤10 → 0 | S130 when passing the level ==0 and the screen turn is ≤10 → var128=0 → S82 |
| 53 | Fortress バルジ | S45/S72/S97 end of level (defeat バルジ) → 0 | **Native loading**: World map `load_000A7EC0:801C3390 → 800A4B8C`, when ==3, place resource 5596 (バルジ, with name tag) in slot 0xB |
| 54 | Flagship down lines | Enter → 1 (`8009E0C4`); S48 ドレイク defeated, S63 ドレイク／ショット defeated → 3 | **Native read and write**: `800A26DC` (event polling `8009E194` call) write 2, read, write 0, arrange the flagship downing lines according to the captain list `D_800C9A08` (from text 5799); close when ==3; `800A3F7C` copied into `D_8010F6B4`. Not related to hidden features |

### 5.2 Single-level variables 100–139

| Variables | Entering | Usage |
| --- | --- | --- |
| 100–103 | Set 3 | Type 2/7 Threshold switch (section 4.4), also used as a sign inside the gate. Write/read: 100 is 95/81 places, 101 is 53/31, 102 is 19/11, 103 is 7/9 |
| 104, 105 | Set to 3 | Only write at S26, never read |
| 106–114 | Set to 3 | Script not used |
| 115–127 | No reset (3 for new games) | Script not used. var117–122 accessed by tactical overlay `801CF420`/`801CF884` as `127 − D_80217AC5[驾驶员]`: When the pilot's aircraft is 171–176, if this variable == 3, write 0 and call `802176A8`. Since it does not reset, this is a one-time flag per driver; see Section 10.1 for usage |
| 128–136 | Set to 3 | The state within the level, each level has different meanings (128: 212 write 248 Reading; 129: 134/120; 130: 74/64; 131: 42/52; 132: 31/39; 133: 28/36; 134: 27/43; 135: 10/15; 136: 2/3). Relevant to this article: S14 escort count (128) and three units (129–131); S41/S56 Kanmo var128==1 → S123; S66 ミネルバX; S129 var128, S137 var128/129 アレンビー; S130 var128 limited time destination; S89 var130, S139 var129 detachment destination; S103 var129 マシュマー／キャラ reinforcements; S105 var129／130／136 クェス; S129 var131, S137 var133 Dongfang Invincible Lines |
| 137–139 | Set to 3 | Script not used |

### 5.3 Only change the reading point of lines

| Variables | Scenarios |
| --- | --- |
| 0 | S12, S81, S82, S93, S94, S101, S131 |
| 1 | S16, S17, S20, S23, S24, S30, S37, S40, S43, S44, S45, S46, S57, S61, S77, S99, S107, S137 |
| 2 | S20, S38, S57, S128 |
| 3 | S41, S57, S59, S129 |
| 4 | S20, S33, S42, S81, S91, S92, S140, S141 |
| 5 | S43, S44, S56, S70, S77, S91 |
| 6 | S48, S63, S96, S100 |
| 7 | S26–S33, S42, S47, S50, S54, S55, S61, S81, S85, S89, S90, S92, S98, S100, S102, S103, S106, S132, S138–S140 |
| 9 | S31, S33, S39, S45–S49, S55, S77, S91, S101, S106, S107, S140 |
| 10 | S91, S93, S99, S103–S105, S139 |
| 11 | S77, S78, S84, S85, S89, S97, S98, S103–S105 |
| 12 | S11, S24, S108, S137 |
| 13 | S38, S44, S56, S57, S66, S85, S89, S90, S100, S102, S103, S139 |
| 14 | S38, S40, S43, S44, S51, S55, S69, S85, S89–S91, S100–S103, S108, S136, S139 |
| 15 | S141 |
| 16 | S38, S84, S85, S89 |
| 17 | S39, S45, S57, S59, S98, S128, S137, S141 |
| 18 | S41, S43, S44, S56, S66, S77, S85, S89–S91, S100–S103, S139 |
| 19, 20 | S104; S102 |
| 21 | S44, S85, S89, S90, S100, S103, S139 |
| 23 | S45, S61, S76, S77, S80, S91, S92, S98, S138, S141 |
| 24 | S85, S96, S133 |
| 25 | S61, S76, S77, S91, S99, S130 |
| 26 | S61, S76, S77, S82, S85, S94, S96, S99, S101, S130, S131 |
| 27 | S85, S87, S98, S99, S101, S132, S141 |
| 28 | S85, S86, S132 |
| 29–32 | S88, S105; S101; S104; S105 |
| 36 | S81 |
| 37 | S54, S55, S59, S60, S91, S97–S99, S101, S103 |
| 38, 39, 40 | S56; S25; S81, S92 |
| 43 | S97, S100, S101 |
| 44 | S103–S105 |
| 46 | S137 |
| 48–50 | Main Line 23 locations |
| 51 | S97–S99 |

## 6. Item-by-item comparison

"Conclusion" column: **Consistent** means that the script conclusion is consistent with Akurasu; **Different** means that the conditions, values ​​or results are inconsistent with Akurasu (see Section 7 for details); **Akurasu Not Included** means that Akurasu does not have this item, or the main points are consistent but the key conditions are only on our side (see Section 8 for details).

### 6.1 Protagonist exclusive

| Hidden Elements | Akurasu (Summary) | Script Conclusion | Conclusion |
| --- | --- | --- | --- |
| カーツ＋ヴァイローズ（ブラッド） | Before the divergence level, the カラッド shot down the カーツ twice; before the end of the Chaos Earth Circle, he shot down ≥100; at the end of the level, choose the 3rd item | Karna appears as an enemy in 9 levels (S16, S25, S34, S41, S46, S56, S64, S66, S124). S25/S46/S64 immediately retreats when Karra is not present. In the defeat event of each level, the other side fighting is ブラッド (counterattack also counts) → var20+1, and when it reaches 2, it will be pushed back to 1 (3→0→1). In the divergence level (S41, S56, S66), the same event is counted first and then judged var20==1 → var21=0, so ** the divergence level must be shot down by ブラッド, and it is counted twice**. There is no ブラッド selection limb in the divergence level (S41 `001b181c` is the only `3D44` in the アーク section), var21==0 automatically enters the S124 decision time. S124 Only ブラッド attacks, and the game ends when ブラッド is defeated; the moment when カーツ is defeated `001e31b0`: `3E0D ブラッド`, `3E0C 100` → Less than 100, write var128=1. Guanmo ≥100 → Register カーツ＋ヴァイローズ, `3D6C 35,3`, var21=2; insufficient → var21=1. Return var11==0 → S42, var10==1 → S57 | different |
| スーパーアースゲイン | Upgrade when not taking the カーツ | All are `3D5A 27,0,306,34`: IA Chaos Earth Circle End of Pass (var21==3), OZ トレーズ erasure command The end of the level (var21==3); the decisive moment fails → the next level (S42/S57) opens; CP 戦いのmeaningは All transfers at the end of the level (`001b6ccc`, var21==0 When Karra survives, he actively contributes Rakura, but does not join the team); if Karra is recruited, he will never transfer | Consistent |
| アイシャ＋エルブルス（マナミ） | IA/CP/OZ each has steps; "less than 9/7 units"; CP "2nd round"; OZ S57 joins at the beginning | IA: S34 Persuasion → S38 Persuasion (var13==0) → S40 `001b0990` When the enemy remains **≤9**, if var13==2: Malino is present → Group 8, `3D58 32,0`; not present → var13=3, permanent failure. CP: S65 → S66 (var13==0 → 1) → S69 After Malin is defeated in the opening script battle, **Our phase in the 3rd round of the screen** (`3D52 0,2,1`) or the enemy remaining **≤7**, whichever comes first will trigger once, and Malin must be present. OZ: In S49, when the third-party survival is ≤10, Mali will only make three choices when he is present (the first two → 0), or at the end of S50, he chooses "びとめる" → 0; S56 persuasion (var13==0 → 2); S57 opening `3D59 28` Malani cannot attack and register at the end of the **pass**. After joining, `3D64 500,500` replaces ローレンス as co-pilot | different |
| スイームルグS | Obtained in the same level regardless of whether it is recruited or not | Recruited: S40 end of level (IA)/S69 end of level (CP)/S57 end of level (OZ); not recruited: S41 opening (IA)/S69 end of level (CP)/S57 opening (OZ). When it is not recruited, エルブルス's `3D5A 999,0,37,3000` is a no-op | different |
| エルリッヒ＋ノウルーズ（アーク） | IA: Ideal, Collapse, choose the 2nd option, Chaos Earth Circle, Persuasion, Guanmo 2; CP: Persuasion; OZ: Must be on the ロームフェラ side, the moon is hell! and トレーズ persuade twice | IA: S41 persuasion threshold **var9==0** (レラ branch is established, see the row of レラ branch in this table) → var18=2; choose one of the two at the end of the pass only Appears when var18==2, choose 2 "わかりません..." → S123, choose 1 → var18=3 and it will be lost permanently. CP: S66 There is no threshold for persuasion, `3D58` will be transferred to us on the spot, and registration will be completed (no modification). OZ: S49 Persuasion → var18=0; S56 **アーク is present** when the enemy remaining ≤13**: var38==0 requires var18==0, var38==1 without prerequisite → var18=1; Persuasion (var18==1) → 2; Guanmo is the same as IA. S123 Only アーク attacks. If the enemy plane enters the target building or アーク is destroyed, the game ends; clearance registration, `3D6C 327,4` | Different |
| リッシュ＋シグルーン（セレイン） | IA chooses "姧様の笑言は..."; CP chooses the other two; CP joins before the start of S70; OZ Choose "Reply する" or "もう once sound をかける" | S35/S65 Three choices before the battle: Item 1 → var14=0 (**Cannot be convinced after**), Items 2 and 3 → 1; S38/S69 The persuasion thresholds are all var14==1. IA is registered at the beginning of S40, and CP is registered at the end of S70 **Guanmo**, both of which have no modifications. OZ: In S49, when リッシュ appears, the second choice is only given when セレイン is present, "Reply する" → 1 → S51/S108 opening registration; S50 end of level "もう一声をかける" → 2 → S108 opening registration; OZ both `3D6C 328,3` | Different |
| レラ branch (var8/var9) | Ideal, collapse, choose item 2 | Only for the real system. After the opening of S30 "レラに声をかける": S27 select the 1st and 2nd items → var9=0; select the 3rd item "Ignore する" → then select (アーク 1st item, セレイン 2nd item → 0). S30 Select "put it" → var9=1. Influence: S42 The real system at the end of the level var9==0 → S43 (Role dies in battle), otherwise S44; S41 Era's threshold; S63 opening CP Rila leaves the team (var9=3); S140 plot (composed to be the same on both sides); more than ten levels of lines. S43 and S44 are obtained at the end of the level the same | different |
| アシュクリーフ（アーク） | Galactic Empire Army advance fleet | Unconditional `3D5A 25,0,31,30`: S77 opening (IA, CP fight alone), S91 opening (OZ, CP with Toro) | Consistent |
| ラーズグリーズ（セレイン） | Galactic Empire Army advance fleet | Unconditional `3D5A 26,0,33,32`: IA S40 **End of the pass**; CP fighting alone S136 end of the pass; OZ/CP with Toro S91 opening | Different |

### 6.2 Common

| Hidden Elements | Akurasu (Summary) | Script Conclusion | Conclusion |
| --- | --- | --- | --- |
| アイナ＋アプサラス | 时は流れた、撃のビクトリア persuade twice; super type only needs the second time | S11 persuasion threshold var128==0, var128 Only the event `0019f2a8` before the battle between Siro and Aina is written as 0, so **must fight once** (whoever fights first is fine). S24 アイナ appears after the second wave (the 5th round of the screen when our team or the enemy is ≤8) and when the enemy is ≤10; persuasion (var12==0) → 2; registration at the end of the level. For super type S24, write var12=0 directly at the beginning; エイジ cannot attack in this level | Akurasu Unloaded |
| アレンビー＋ノーベルガンダム | Two persuasion; in the later stage, ドモン and レイン must be persuaded in the same round, ランタオ within 4 rounds, despair. There are less than 10 enemies before; those who have never been recruited cannot be persuaded | Step 1 In S18/S19, it will appear when the number of enemies is ≤5, and there is no threshold; in S19, the level will be cleared automatically at the beginning of the enemy phase in the 9th round. Step 2 S128/S57 threshold var3==0. S129: var3∈{0,1} can be persuaded; the berserker version appears in the enemy phase in the 2nd round of the screen or when the enemy is ≤15; **First ドモン and then レイン, it does not need to be in the same round** (there is no event to reset var128/var129 by round in both levels); Screen 5 She retreats at the beginning of the enemy's turn (before she is defeated). Save → var3=2 and register (**join the team even if you have only done step 1**); if not saved, you will become the core of デビルガンダム, and `3D5A 9,0,6,4000` will be deleted when defeated. S137 is the same: the enemy attracts 12 reinforcements when it reaches ≤10 for the first time, and retreats when it reaches ≤10 again; players who join the team but do not attack cannot see her in this level and will not lose her | Different |
| ガラリア＋バストール | No attack or counterattack within 4 rounds | S20 opening delay slot 0 (2nd round of the screen) → slot 1, **When the enemy phase starts in the 4th round of the screen** `3D58 185,0`, var4=0. There are only two cancellations: she is shot down; the battle between Xiang and her (6 Type 4 events, starting with `[185,181]`) has `3E17`==1, i.e. Xiang attacks her, or she attacks Xiang and Xiang chooses to fight back. She does not cancel attacks by other organisms | Different |
| シーラ＋グラン・ガラン／エレ＋ゴラオン | Choose 1 Sheela in the opening, choose 2 Airei | S26 The opening selection determines the map of this level (62/9), which is the same as our team 0/1 and the enemy team. Unselected side: IA S33 appeared as our side in the middle and was removed at the end of the same level. `4000` was removed at the end of the same level. CP S62 was registered at the beginning and was removed at the end of the level in S63. OZ S48 appeared and was removed at the end of the same level. | Consistent |
| Endless Waltz body | Automatically changes to Custom after five items are modified | Maintenance `load_0008F4B0:801CF85C` (the only call point `801D0028`, modification confirmation path): `D_801DC6E4` The number of five segments in the five pairs is ≥ the instance upper limit `+0x51` (these five units are 7), then `800AAD28` Change clothes; don't look at weapons. For inheritance, see [Transformation Inheritance](upgrade-inheritance.md) | Consistent |

### 6.3 Series Exclusive

| Hidden Elements | Akurasu (Summary) | Script Conclusion | Conclusion |
| --- | --- | --- | --- |
| エマ (super type) | クワトロ persuade, join after the level | S16 エマ appears in the 3rd round of the screen when our stage or the enemy is ≤12; there is no threshold for persuasion → var1=0; to be respectful (デビルガンダム) HP ≤50% Or persuade before being defeated, at that moment the delay slot 1 registers エマ＋mkⅡ and passes the level with `3D4A`. The real system was added in the opening scene of S17 by Sugaru (Part 1) | Consistent |
| エリカ (super type) | Rikiri no Town, final selection 1 | S23 final selection 1 → `3D5A 199,0,999,999` (driver only), var5=0 | consistent |
| ナイーダ (Super type) | デューク Persuasion, choose 1 in the next level; without persuasion, デューク cannot attack | There is no threshold for persuasion (only deployed in the super level). S77/S91 When var23==0 opens, the choice is made: the first item is to register the ナイーダ＋ダブルスペイザー; the second item is that she self-destructs (`3D4F`), **デュークcannot attack in this level**, S91 the enemy group is changed to another group 6. When there is no persuasion, S77 only Kamitu and Sho cannot attack, S91 unlimited | consistent |
| Karika (super type) | デューク, Malika persuade in turn | S78 Round 3 friendly phase, S92 appears when the enemy is ≤15; Malika threshold var24==0; only the driver at the end of the level | Consistent |
| アポリー, ロベルト (real system) | Automatically join | No `3D5A`: S2 (the enemy phase in the 2nd round or all enemies are destroyed)/S3 (the enemy ≤10 after the second wave) deploy our team 4 (クワトロ, アポリー, ロベルト＋2 台リック・ディアス), join the team directly | unanimous |
| ゲイル＋グライムカイザル (real type) | エイジPersuasion, added with 4 stages of transformation | S12 There is no threshold for persuasion. IA/CP registers at the end of level S32, **3 stages**; OZ registers at the beginning of S52 (S49 recruits ガトー → S51 → S52) or the end of S53 level (does not recruit or moves ムーンアタック → S108 → S53), 4 stages | different |
| ガンダム, ガンキャノン, ガンタンク (real system) | Keep three units and you will get | S14 Each of the three units will be judged: if they enter the green area, they will be evacuated and counted as saved; if they are shot down, var128+1, corresponding var129/130/131=3; Raku・カイン will pass the level immediately when HP ≤50%, and those who have not been shot down at this time are also saved. At the end of the pass (not a total loss), each unit will be registered and transformed in one stage, and a bonus (N3) will be given based on the number of units lost | Different |
| フォウ (real system) | ホンコン twice, sea and earth once, IA カミーユ level ≥ ジェリド (average +3 for all members), OZ persuasion | Threshold chain var2: None → 0 → 1 → 2. In S20, when you only did the ホンコン persuasion once, there was only dialogue here; the third step of persuasion was passed directly with `3D4A`. S128: The カミーユ cannot attack at the beginning. In the third round of the screen, when our phase or the enemy's level is ≤8, take Z to arrive; immediately after persuasion, `3E06 38,69`, **カミーユ's current level ≥ If the ジェリド level** is successful (var17=0), if it fails, the フォウ will be defeated (var17=1).ジェリド level = `D_8010F5F3`＋3, `800A4BE0` Calculated when entering the tactical map: the average of the top 15 levels of our pilots who have boarded the aircraft (rounded off decimals), sandwiched between 1 and min(99, number of cleared sessions + 40, 95). S57 Persuasion without level conditions | Different |

### 6.4 Route exclusive

| Hidden Elements | Akurasu (Summary) | Script Conclusion | Conclusion |
| --- | --- | --- | --- |
| Silver Bell + Silver Bell ロボ | IA/CP masterpiece kills more than 20; OZ more than 30, all before the end of this level | S32 **End of level** (after `3D4A`) `3E0D 156`, `3E09 20` → **≥20**; OZ S107 **Opening** `3E0B 30` → ≥30, downing in this level is not counted | Different |
| ロザミア | Defeat ゲーツ without defeating her, and then convince カミーユ, and join after the level | S37 The second wave (our team will be completely destroyed at the beginning of the 5th round of the screen or earlier) **Kuカミーユ must be present** when it appears**, otherwise the two of them will retreat on the spot, var15=3; she will be killed after appearing with our record `3D58` Becomes an enemy (drops are cleared); then knock down ゲーツ → she leaves the field, var15=0. S41 She and ゲーツ appear when バレン is defeated; **must **kill ゲーツ before convincing**, otherwise it will be invalid; **register on the spot** when persuading (only the driver) | Different |
| ヒルデ＋トーラス | デュオ is persuaded and will not be shot down; other routes will automatically join | IA S38 Persuasion → `3D58` Switch to our side on the spot; if he is shot down thereafter, トーラス will be removed. OZ S59, CP Sui Toru S75 Unconditional registration No. 266 at the end of the level, **only the driver**; CP cannot be obtained by fighting alone | different |
| ガンダムmkⅢ, メタス开 | IA Obtained after clearing マーズとマーグ | S42 Unconditional at the end of the level: `3D5A 999,0,57,500`, `3D5A 999,0,67,65` | Consistent |
| Mireba |
| ゼクス＋エピオン | OZ pilots ウイングゼロ in this level, exchange after the level; トレーズ branch brother and brotherと | OZ S57 end of level `3D5A 286,0,123,500`, while ヒイロ连ウイングゼロ leaves the team (`3D5A 95,0,119,4000`); CP opens with トレーズ S76 | Consistent |
| Mass-produced グレートマジンガー (CP) | Obtained by clearing customs | S135 Unconditional registration at the end of the level, level 3 | Consistent |
| ガトー＋GP02A (OZ) | トールギス壊 Choose 1, 月はHellだ! Do not let the yellow unit reach the base | Base area x10–11, y4–5. **Our flagship enters first** → var37=0 immediate victory; シロッコ enters first → 1 (modified to 3 at the end of the level); バスク enters first → 3; other yellow units enter first and have no effect. You can also annihilate all the enemies first (the first annihilation will bring in シャピロ reinforcement group 13, and then var101=0 after annihilation), and then annihilate the third party → var37=0. Sekimo 0 → Register Gaito＋GP02A (3 stages), Z, GP03, Re-GZ, go to S51; 3 → Go to S108 | Different |
| ガトーLeave the team | Secrets: The future of life and death. After leaving the team, choose cooperation to advance one level; Flow Chart: Choose 1 at the end of the next level, choose 2 at the end of this level | S138 Opening "Cooperation するべきだ" → var43=0 → S97 Leaving the team at the end of the level; "すべきではない" → 1 → **S138 Leaving the team at the end of the level, and leaving the map on the spot when Harumon fell out during the attack in this level | Different |
| FA Hyundai Kai | OZ upgrades when reaching this level | S59 unconditional opening `3D5A 999,0,295,73` (at the same time the flagship changes to ネェル・アーガマ) | Consistent |
| トッド | Recruit ガラリア first, then persuade three times; IA decisive breakthrough (Part 1) reinforcements, OZ see えないTomorrow's opening | Only look at var6==1: S81/S92 **Our phase in the third round of the screen** (type 0 original value 2) deployment; this level is shot down and lost permanently. Neither convince nor join checks var4 | different |
| シルキー | マーベル Knocked down before the start of this level ≥30 | Judgment of the same event as トッド: var6==1, var4==0, マーベベル Knocked down ≥30 → Register and ride together; Knockdowns in the 1st and 2nd rounds of the screen are also counted | Different |
| ロゼ＋ゼーロン | Convince マーグ → Convince and defeat マーグ, then convince ロゼ → Convince ロゼ again | All that is required are: second level (S61/S76/S77) **Kill down Malik by タケル when ロゼ is present** (var26=0, don’t look at var22/25) → convince ロゼ → third level (S91/S130) and then convince → register at the end of the level (3 stages). Persuading Maris to just change the lines | Different |
| プル | IA persuaded twice, the second time after shooting down the グレミー; OZ convinced after shooting down the グレミー | IA S84 persuasion → S85 when convincing, the グレミー must no longer be on the map; OZ S98グレミーshould ** be shot down ** (`3E1B`==0). Persuasion first is invalid (section 3.6) | Consistency |
| プルツー | Recruit プル first, then persuade in turn, before shooting down グレミー | Threshold chain var27==1 → var30 0 → 1 → 2. IA S132 The グレミー must still be present** when persuading; OZ S100 When the グレミー HP is ≤30%, it will retreat with the プルツー, and must be persuaded before; S101 No グレミー conditions | Consistent |
| MASTER or キャラ | Both survive, only convince one person, dream, come again, choose 2, reinforcements in the 8th round | S86 Both of them must be on the map when the event is settled at the end of the level; S88 can only convince one of them; S103 **Reinforcements appear in our 8th round of the screen** reinforcements, the previous level is var29/var32=3 Permanently Lost | Consistent |
| ノイエ・ジール | Dream, come again, choose 2, and get it after the next level | S103 Register only after var11==0 at the end of the level (stage 3). var11 is only written in S32, so only independent players who have never gone to complete peace can get it; OZ keeps 3 and cannot get it | Akurasu Unloaded |
| キュベレイmkⅡ Change color | Recruit プル, プルツー, and dream again. Choose 2, and then choose 2 before the next level starts | In the same end-of-level event in S89/S139, if you choose "Earth Circle Remains" var27==1, var30==2, then choose one of the two; choose 2 `3D5A 57,0,323,77`, change to the red version and give it to プルツー | Consistent |
| Mass-produced type νガンダム | Only choose OZ after the first difference; choose one of the two equipments | S137 At the end of the level, when var10==1, "ファンネル equipment type/インコム equipment type" → No. 294/296 | Consistent |
| Saber Survival (OZ) | Let the real Saber attack; whether to return is uncertain | S137 After the opening sortie, **Riber (pilot, body is not limited)** is on the map → var130=0. Of the two settlement events, `3D5A 3,0,0,4000` is only executed when var130 ≠ 0, so he and ガンダムシュピーゲル** remain in the list**; another dialogue of "Surviving on the ゲッター Line" is broadcast at the end of the level | Different |
| トールギスⅢ | ハマーンの影 Select 2 | S99 Final Select 2 → `3D5A 286,0,136,123` | Consistent |
| Kirara＋Marinaダラガンダム | Kirara defeated Kirara (appeared in the 5th round), and then joined Kurara (front) | S41／S56 Korra was shot down by Dumran → var19=0. Appearance: S41 Delay Slot 2 is activated when バレン is defeated. バレン is defeated in the opening script battle, so it is the enemy phase in the 5th round of the screen; S56 is the next friendly phase after the first wave is completely destroyed. S104 When the first wave was completely wiped out, var19==0 → Kirara appeared as our team 6, **still present when the last wave was wiped out** before `3D58` joined | different |
| クェス＋ヤクト・ドーガ | ラー・カイラム アクシズ within 2 turns (or before) アムロ knocks down シャア | S105: Write var130=0 in the 2nd friendly phase `001e12e0` after ラー・カイラム enters the area (the push away phase starts).シャア was shot down by アムロ and var130 is still 3 → escape, クェス is present → var47=0. Also: At the beginning of our phase in the 8th round of the screen, both var130 and var136 are 3 → Game over | Consistent |
| Breakthrough Battle to the Death 10 rounds | Both levels are completed within 10 rounds → One side | `3E04 10`: The upper and lower chapters are completed within ** the 10th round of the screen (inclusive)**; both chapters are completed → S82 | Consistent |
| A decisive breakthrough battle. Victory method | Any unit reaches the designated location | Victory text "Enter the full machine of the flavor"; regional mode FE, exit immediately after entering, **All personnel withdraw** (or all enemies are destroyed) to pass the level | Different |
| Three choices for the zodiac war machine base | Garnera line: Kontra V four weapons; Rakuten line: Shipotian Jingquan | Choose 1/2/3 → S81/S79/S80. The four pieces of コンバトラーV (770/773/775/777) are unlocked **unconditionally** at the beginning of S81 (OZ starts at S93); the Shipotian Jingquan ランタオ line is at the end of S79, and the other two lines are at the beginning of S81 (var36≠0, keep the initial value when choosing 1 3), OZ at the end of S95 level | different |
| ムゲ／Earth Circle Detachment | Choose 1 to go to ムゲ Universe, choose 2 to stay; works available on both sides | S89／S139 End-of-level selection → `3D73`: Choose ムゲ Universe and set list B (`D_800D06E4`, 61 people) as unattackable, leaving the Earth Circle list A (`D_800D06A8`, 29 people) is set as unattackable; S104 opening `3D74` is cleared. There are two lists of Gura, and neither one is available; Link Battler character is not in the list | Consistent |
| ミリアルド（ノインpersuasion） | Can be persuaded by ノイン | S84 no threshold, S103 threshold var11==0; both places only have dialogue, no variables | consistent |
| Fully modified weapons unlocked | Unlocked after fully modified | Modification confirmation `801D1100` → `801D0AE4`: Table `D_801DC87C` 18 items (body number, fully modified weapon number, unlocked weapon number) | Consistent |

### 6.5 Weapons and Combination Skills Unlocked in the Plot

| Project | Akurasu (Abstract) | Conclusion (Script & Code) | Conclusion |
| --- | --- | --- | --- |
| シャッフルAlliance four-machine sure-kill (53/62/71/76) | — | `3D6F`: S39 opening (IA), S55 opening (OZ), S70 the enemy is completely destroyed or the 15th round our phase comes first (CP); write var45=0 for the same batch of events | Akurasu Not included |
| Duankong Guangfang Sword (874) | S81 | S78 Guanmo (IA), S92 Guanmo (OZ) | Different |
| Shi Potian Shocking Fist (19) | Exclusive to Raku line | S79 end, S81 opening (var36≠0), S95 end, all three lines will get | Different |
| コンバトラーV four pieces | ジャネラ line | S81 opening, S93 opening; S80 no `3D6F` | Different |
| The emergence of combined skills | — | Each time you open the weapon list `8020178C` (call points `801CD798`, `801F8FE4`), call the judgment function for each combined skill: return 0 and set the lock bit (`+0x22` bit 0x04), otherwise clear the lock and write the power. Participants must find the first present unit in the same camp and **connect each other** (counting diagonally, three or more units do not need to be adjacent two by two; `80200530`, `801E966C`, `801E95DC`), each person's EN, strength, and condition number meet the standards | Akurasu Not included |
| ダブルゴッドフィンガー (1215) | Only in the Independent Army (Process Card) | The only `3D6F 1215` in the whole ROM is at the end of S41 (var3==1), but the lock bit will be overwritten by `8020178C`, **This command has no lasting effect**. Any route can be used as long as the god ガンダムH (ドモンki ≥130 automatic transformation, `801FF1BC → 801FEDF4`) is adjacent to our ノーベルガンダム, each with EN ≥60 and ki ≥130 | Different |
| Ishiba Tenjin Fist | OZ 42, ドモン branch line 38, others 53 | Determination function `80200B1C` also requires the first instance No. 19 in the weapon pool `D_80178F80` to be unlocked, so the `3D6F 19` that follows Ishiba Tenjin Fist Go: S79 end of level/S81 opening/S95 end of level | different |
| Structural Allied Fist | Tactical Fist (Later) added | No plot unlock; God's S-form H and four S forms are connected together, each EN ≥100, power ≥130 | Different |

## 7. Discrepancies with Akurasu

Here are all the "differences" confirmed this round.

1. **カーツ**: In the divergence stage, the ブラッド must be shot down by the ブラッド, and it is counted as "twice" (Akurasu: two times before the divergence stage); there is no ブラッド's choice limb in the divergence stage (Akurasu Flow Chart: choose the 3rd option); 100 kills at the time of decision. Judgment at the moment of defeating the Akurasu (Akurasu summary list: Before the end of Chaos Earth Circle; the personal page is the same).
2. **アイシャ**: The number of survivors is ≤9/≤7 (Akurasu: less than 9/7; Flow Chart: less than 8/6 units); the CP delayed branch is the 3rd round of the screen in our phase (Akurasu: 2nd round); OZ S49 selection requires the presence of Marino; OZ in S57 **End of level** joins and Malani cannot attack in this level (Akurasu: opening).
3. **スイームルグS**: When Aアイシャ is not recruited, IA opens at S41 and OZ transfers at the opening of S57 (Akurasu: same level).
4. **エルリッヒ IA**: The threshold is var9==0 (レラ branch), ideal, えて, items 1 and 2 are all OK, the key is オペレーション・デイブレイクChoose "レラに声をかける" (Akurasu: Ideal Collapse, choose item 2).
5. **エルリッヒ OZ**: It is not necessary to go to the ロームフェラ side; トレーズ erases the command and the enemy must be present when the remaining enemy is ≤13 (Akurasu: must be on the ロームフェラ side, not mentioning presence).
6. **リッシュ**: IA also has to choose item 2 or 3, and cannot be persuaded after item 1 (Akurasu: item 1); CP joins at the end of the **Kanmen** in the battle field (Akurasu: before the start).
7. **Rura Branch**: See section 6.1 for combinations (Akurasu: Just write Ideal Breaker and choose item 2).
8. **ラーズグリーズ**: IA at the end of the Seki no Ming はエピオン, early 6th episode (Akurasu: Galactic Empire Army Advance Fleet).
9. **アレンビー**: The two later levels do not have to be in the same round; players who have only done step 1 can also be rescued and joined into the team; the S129 retreat moment is the beginning of the enemy phase in the 5th round of the screen (Akurasu: the same round, within 4 rounds; those who have not been recruited cannot be persuaded).
10. **ガラリア**: Only the battle between Xiang and her will be cancelled, other mechas can attack; the joining time is the beginning of the enemy phase in the 4th round of the screen (Akurasu: no attack or counterattack within 4 rounds).
11. **ゲイル**: IA/CP is a 3-stage transformation, OZ is a 4-stage transformation; the S52/S53 boundary of OZ is whether or not ガトー joins the team (Akurasu: 4 stages, divided according to routes).
12. **ガンダム三机**: Judgment one by one, which one you keep will get which one (Akurasu: keep three).
13. **フォウ**: The ジェリド level is "the average of the top 15 people who have boarded the machine (rounded, the upper limit is 95) + 3", calculated when entering this level (Akurasu Secrets: the average of all members +3; the "top 15" of Flow Chart is consistent).
14. **Silver Bell**: The threshold contains an equal sign (≥20/≥30); OZ is judged at the beginning of the Toruルギス opening, and the knockdown of this level does not count (Akurasu: exceeds, before the end of this level).
15. **ロザミア**: In the 5th round of the S37 screen (when the second wave appears), the カミーユ must be present; in S41, kill the ゲーツ first and then persuade, otherwise it will be invalid; persuade to join the team on the spot (Akurasu: join after the level, no presence conditions).
16. **ヒルデ**: OZ and CP can only be obtained with Toruzu as the driver, but CP cannot be obtained by fighting alone (Akurasu: other routes are automatically added).
17. **ナイーダ**: The condition for the デューク to be unable to attack is that it has been persuaded and choose item 2; it can attack without persuasion (Akurasu Flow Chart: it cannot attack without persuasion).
18. **ガトーEnter the team**: The only targets of determination are シロッコ and バスク themselves; it will be considered a success if our flagship enters the base first or if both stages are completely destroyed (Akurasu: no yellow units are allowed to enter).
19. **ガトーLeave the team**: Choose "Join force するべきだ" to leave the team at the end of the next level (S97), choose "すべきではない" to leave the team at the end of this level (S138) (the Akurasu Secrets page is opposite; the Flow Chart is the same).
20. **トッド**: There is no ガラリア prerequisite; reinforcements are in our phase in the 3rd round of the screen (Akurasu: recruit ガラリア first; OZ joins at the beginning).
21. **シルキー**: Determined at the same time as the トッド, the knockdown in the 1st and 2nd rounds also counts (Akurasu: before the start of this level).
22. **ロゼ**: Persuading Malik is not the prerequisite, the key is that Malik is shot down by Malik when ロゼ is present (Akurasu: You must convince Malik first in all three levels).
23. **シュバルツ**: It is judged to be the pilot Riko; he will not be removed from the list after surviving (Akurasu: True ゲッター, return is uncertain).
24. **キラル**: S104 must wait until the last wave of total annihilation before joining; OZ appears in the next friendly stage after the first wave of total annihilation (Akurasu: appears in the 5th round, automatically joins in the middle of the level).
25. **Death Breakthrough Strategy**: Passing the level requires all members to enter the green area and withdraw (Akurasu: any unit arrives).
26. **Ishipoten Shocking Fist, 4 pieces of Konnoli V, and the Sky-breaking Light Tooth Sword**: See Section 6.5 for unlocking levels (Akurasu: belong to the Rura line, the ジャネラ line, respectively, S81).
27. **Fusion Techniques**: ダブルゴッドフィンガー, シャッフルAllied Fist does not need to be unlocked through the plot, and is also available in the OZ line; Ishiba ラブラブ天翖剑 follows Ishiba Tianjingquan (Akurasu: OZ 42, ドモン branch 38, others 53).
28. **サンクキングダム, ミリアルド** of Collapse (S67): When our phase starts in the third round of the screen, ヒイロ is not present → our team temporarily joins the battle, and is present → the enemy (Akurasu: When ヒイロ is knocked down before appearing).
29. **Humanity's Victory, Nana... (Later) (S140)**: var9 only changed the plot, and the opening arrangement is the same on both sides (the old draft of the guide said that the arrangement will be changed).
30. ** Side by side from now on (S123) **: Only アーク can enter, OZ episode 31, Independent Army episode 32 (Akurasu Flow Chart: 32/33 episodes).

## 8. Akurasu Not included

### 8.1 Mechanism

| # | Content | Basis |
| --- | --- | --- |
| M1 | Persuasion only appears when adjacent up, down, left, and right. The persuader must be the main pilot and have the number of actions; it can also be done after moving | Section 3.1 |
| M2 | When the same persuader is attached to two objects, he can only persuade the one registered first | Section 3.2 |
| M3 | The preconditions of each persuasion chain are written in the event header threshold (all 47 events with thresholds) | Sections 3.3, 3.8 |
| M4 | One persuasion consumes one action, and if the check fails, the slot of this level will also be invalidated (ロザミア, プル, プルツー (middle), outside the route section) | Section 3.4, 3.6 |
| M5 | Components are only dropped when our units are shot down in battle; `3D58` will be cleared when changing sides, so the biosensor of S37 ロザミア cannot be obtained | `801F6778`, `802106FC` |
| M6 | `3E1B` Distinguish between "Being shot down (0)" and "Retreating, not showing up (3)", プル (S98) requires being shot down | Section 4.3 |

### 8.2 New findings from full scan N1–N17

| # | Content | Evidence |
| --- | --- | --- |
| N1 | ちずるSurgical line: S138 The leopard horse is knocked down at the end of the pass ≥15, ** or ** S97 Let the leopard horse attack (regardless of the number of kills), and the surgical line will be used (var51=1), S99 The opening `3D59 145` The leopard horse cannot attack; when neither is satisfied, コンバトラーV is available as usual | `001da000@532`, `001d8b64@976`, `001d9430@430`, `001db3d0@866`/`@882` |
| N2 | The opening selection of Gunman Killing Machine (S10) アーク chapter "もう小し考えさせてください" → `3D59 25`, アーク cannot attack at the beginning; screen 4 In the turn, all our phases or the enemies will be destroyed (`0019eb7c`/`0019ec90`), lead out the ゲイル team and write var129=1, var101=0; after that, in the 6th round of the screen, our phases or the enemies will be destroyed When ≤6 (`0019ec70`/`0019ecb8`), アーク took the ソルディファー to arrive (`0019ece4@36 3D45 7`). No cross-border impact | `0019e7e8@398`／`@732` |
| N3 | Gorgeous Naru・カイン (S14) Escort Bonus: Loss of 0 units +35000, 1 unit +20000, 2 units +10000, total loss means neither body nor bonus | `001a0e80@54`, `@158`/`@184`/`@210 3D5B 10/20/35` |
| N4 | Ushiugi is defeated (S25) → var39=0 → Blood-painted られた道 (S26) When all enemies are wiped out, Ushiguki brings 2 reinforcements and composite armor; otherwise it does not appear | `001a6944@18`, `001a7564@34` |
| N5 | When Kaoru has joined the team, Kosugaru (Front/Back) (S83/S131), Kusuko Jueku Defense Line (Front) ／Later) (S93/S94) It was changed to Guara on standby and escort, and the victory or defeat condition changed to "Jaru Machine"; Yuru can attack at this time | `001ce7ec@692`, `001d4018@56`/`@134`, `001d69f4@1226`, `001de548@116` |
| N6 | There is only one `3D6F` of the Finger of the Dual God (S41), but it has no lasting effect on combined skills, see Section 6.5 | `001b181c@814`, `8020178C` |
| N7 | All three lines of Shi Potian Jing Fist will be obtained | Section 6.5 |
| N8 | コンバトラーV The four items have nothing to do with the ジャネラ line | Section 6.5 |
| N9 | Nautilus: The real condition why Nautilus cannot attack | Section 6.3 |
| N10 | S67 MIRARA's enemies and friends are determined by whether ヒイロ is present at the beginning of the friendly phase in the 3rd round of the screen; S67 automatic victory in the 10th round of the friendly phase | `001b71ac@12`–`@50`, `001b734c@162` |
| N11 | Component carriers that appear depending on operations: S20 バーン (Joined by ガラリア, or shot down by **Xiang**); S51/S108 シャピロ combat machine (nin was present when the シャピロ was shot down); S56 ガイア三星(enemy) ≤15 when Haru is present); S97 Haruhiruビ・ジェリド (Maharu is not present when shot down); S63 large thruster (carried by the Black Knight when the Black Knight is shot down by Sho and Era is present); S35ガブスレイ・ジェリド (no parts) | `001a42a0@190`, `001c1798@38`, `001c6200@20`, `001d8fd8@120`, `001b53c4`, `001ad960@124` |
| N12 | Other hidden attack restrictions: S128 and S57 カミーユ cannot attack when var2==2; S57 マナミ cannot attack when var13==2 in OZ マナミ; S103 ノイン cannot attack when var44==1; S103 The whole route of Kaoru and Ginling cannot attack | `001b4638@440`, `001c6b90@1264`/`@1288`, `001decc0@1794`/`@1810` |
| N13 | ジャネラ Line (S80) Super Beast: The two AI mother bodies #359/#313 are only determined when ジャネラ is present, and the one that is defeated first determines var129 (the other one is present: #359 first → 0, #313 first → 1; the other one has been shot down → 2), delay slot 0 (All enemies are destroyed or our phase is in the 5th round of the screen) Press 0/1/2 to reinforce Surasu, Kaurai, Kaoru, or two units (both equipped with thrusters); when Sura is present, additional teams of Sirius and Karuno (ワキメデス carry composite armor) will be added. | `001cd350`, `001cd390`, `001cd48c@268`–`@560` |
| N14 | Select limbs that only change the lines: S2 アーク Chapter 3 choices, S16 マナミ Chapter 2 choices, S46 セレイン Chapter 3 choices; S33/S62/S46 ship name "Matsumoto" second choice (the 2nd item opens the unit name input `3D5E`, ported version fixed automatic answer item 1) | `0019ca34@172`, `001a2068@146`, `001bcaa8@72`, `001ab86c@428` |
| N15 | Cross-level variables only change the reading point of lines | Section 5.3 |
| N16 | Dongfang Bubai's ending lines: S129 (var131) / S137 (var133) Depending on whether he has fought with him before, two different sets of lines will be played when Domen defeats him | `001d38c8`, `001d3acc@20`/`@132`; `001d8250`, `001d849c@42` |
| N17 | Reinforcements determined by presence judgment (does not affect joining the team): S15 Third party ウイングガンダム when ヒイロ is not present; S68 Dark General is present → Mass-produced グレート × 8, ボス is not present → 戦阘獣 × 9; S75バスク is present → ビルゴ ×9; S136 ガンダル is present → ミニフォー ×9; S84 トレーズ is present → 五飞シェンロン, ハマーン is present →プルのキュベレイmkⅡ；S101 ガトー／キャラ is present → each will change the machine and appear again | `001a16e0@246`, `001b77f8`, `001bb25c@64`, `001bc058@20`, `001cf6d0@142`, `001cf878@20`, `001dc868` |

### 8.3 Supplementary details for each element

| Elements | Content | Basis |
| --- | --- | --- |
| カーツ | The content of the ending, 3 stages of transformation, the conditions for defeat and the return destination; CP "カーツ survived, volunteered ヴァイローズ" branch | `001e31fc`, `001b6ccc@462` |
| カーツ (Original defect) | The CP survivor branch also writes var21=2, and 7 levels after merging into the independent army, the lines treat him as being in the team; at the end of S102, var20 is used (the `3E03 20,2` block is empty), and カーツ’s lines will be played regardless of whether he is in the team or not | `001dd890@134`／`@152` |
| アイシャ | When IA failed to recruit, she was seriously injured and returned home, and エルブルス was handed over to Malima | `001b0be4` |
| エルリッヒ | S41 Time limit: In the 11th round of the screen, our phase will be lost (all enemies will be destroyed within 10 rounds); from then on, the 4th stage of transformation will be carried out side by side, and the enemy aircraft will fail when it enters the target building | `001b174c`, `001e2efc` |
| リッシュ | OZ S49 selection requires the presence of セレイン; OZ both joins with level 3 | `001bfa04@122` |
| レラ | When var9==0, CP leaves the team during purification (S63), and OZ sacrifices in Humanity's victory (after) (S140); at the end of S43 and S44, both get ダブルスペイザー, ドリルスペイザー, and マリア| `001b4fc4@254`, `001ca8b8@22`, `001b30b4`, `001b3dd4` |
| フォウ | S20 The third step of persuasion ends the level directly; S128 if the level comparison fails, フォウ will be defeated and lost permanently | `001a4420@512`, `001b4b8c` |
| アイナ | S11 Kanmo Sugaru＋Ez8 (1st paragraph) registration | `0019f6d0@436` |
| ガラリア | When being shot down by a machine other than Sho, the second wave (バーン) will not appear. After all enemies are destroyed, it will directly enter the wave of フォウ | `001a42a0@30`–`@264` |
| エマ(Super type) | When not recruited, S26 カミーユ appears on mkⅡ; when recruited, only register カミーユ, and register Gディフェンサー | `001a7494`, `001a765c@142` |
| ゲイル | S83/S93 re-register and prohibited from attacking | `001ce7ec@716`, `001d69f4@1244` |
| ガトー | Decision of whether to stay or go S54 opening registration, S60 enemy reinforcements (Group 5, where ガトー drives GP02A), S98 whether he drives GP02A or ノイエ・ジール | `001c39a4@1602`–`@1714`, `001c8d04`, `001da3b8@1130` |
| クワトロ | S98 returns as reinforcement and cannot attack; var11==1 drives one hundred styles, otherwise FA one hundred styles will be changed; the driver leaves the team again at the end of the level | `001da3b8@1168`–`@1220`, `001db0f0@562` |
| S100 The second choice at the opening: "Dekata See" only requires the complete destruction of the グレミー army, and the "両方を相手にする" requires both armies to be completely destroyed; S138 The second choice at the opening: In the second round of the cooperation screen, Haruman and others appear as a third party | `001dbacc@1156`, `001d992c` |
| クェス | The only 0 point written in var130 is `001e12e0` (the second friendly stage after the arrival of ラー・カイラム) | `001e12e0@920`／`@964` |
| ノイエ・ジール | OZ cannot be obtained (var11 maintains 3) | Section 6.4 |
| Camp side var44 | IA/CP fighting alone is 0, OZ/CP with Tororo is 1 | Section 5.1 |
| Variables read natively | var45 Shisui Shisui’s display and killer lines, var53 Fortress バルジ landmark, var54 Flagship downing lines | Section 5.1 |
| Purify enemy composition | S62 ドレイク When HP ≤30%, the アレン/フェイ present will reappear at the beginning of S63 | var42 |

## 9. Level flow with different conditions

`3D4B` only takes the edge between the common segment and the main character segment; `3D4B 500` (return from linkage) does not count the number of words.

| Source level (end of level) | Conditions → Next level |
| --- | --- |
| S5 ミケーネと百鬼 | ブラッド → S7; マナミ → S6 |
| S7 Meteor Falling Day | ブラッド → S8; マナミ → S9 |
| S17 Ai・戦士たち | Real type → S18; Super type → S19 |
| S20 Hazama Yuu of the Sea and the Earth | Real type → S21; Super type → S22 |
| S30 オペレーション・デイブレイク | Choose 1 "OZ に入り, order recovery にNU める" (var10=1) → S46 New Road (OZ); choose 2 (var10=0) → S31さらば戦士よ(Independence Army) |
| S32 Liangshan Bo's の戦い | var11==1 → S62 広がっていく悪义 (complete peace); otherwise → S33 |
| S41 The Earth Circle of Chaos | ブラッドsection var21==0 → S124 The decisive hour; アークsection var128==1 → S123 ここより公に; otherwise → S42 |
| S56 トレーズ erase command | Same as above, otherwise → S57 |
| S123／S124 | var11==0 → S42; var10==1 → S57 |
| S42 マーズとマーグ | Real system and var9==0 → S43; otherwise → S44 |
| S107 トールギス壊 | Select 1 "ロームフェラには従えない" (var38=0) → S49; Select 2「あくまでもOZとして动く」（var38=1）→ S50 |
| S49 Moon Hell! | var37==0 → S51 → S52; var37==3 → S108 → S53 (S50 also → S108) |
| S70 War Battle Field | Choose 1 (Follow Toru) → S74 → S75 → S76 → S91 (Incorporate into the back section of OZ); Choose 2 (Fight alone) → S71 → S72 → S73 → S136 → S77 (Incorporate into the back section of the Independent Army) |
| S78 Battleship Base Attack | Choose 1 → S81; Choose 2 (var36=0) → S79 → S129 → S81; Choose 3 (var36=1) → S80 → S81 |
| S130 A decisive breakthrough battle (Part 2) | var128==0 (both parts are in the 10th round of the screen) → S82 → S84; otherwise → S83 → S131 → S84 |
| S89 Dreaming, come again | Choose ムゲuniverse (var130==0) → S90 → S104; otherwise → S103 → S104 |
| S139 Awakening Dream | Choose the universe (var129==0) → S102 → S104; otherwise → S103 → S104 |

Route skeleton: starting point アーク S2, セレイン S3, ブラッド S0, マナミ S1 (`load_001090A0:801C69D0` writes `+0x99E`). Independent Army S31 → … → S38 → S128 → S39 → S40 → S41; OZ S46 → S47 → S48 → S140 → S107 → S49/S50; Independent Army and CP share S77–S90, S129–S133, S141 in independent combat; OZ and CP share with Toro S91–S101, S137–S139; S102 can only be entered through S139, S90 can only be entered through S89; S103–S106, S134 are shared by all routes.

**Number of words**: From now on, only アーク/ブラッド can enter when the conditions are met. The number of words for other players thereafter is 1 (super type) or 2 (real type) less than the Akurasu card; "ここより公に" is the 31st episode of OZ and the 32nd episode of "Independence Army". The number of words calculated for each scene according to the protagonist and route can be found in Section 6 of the process verification manuscript `flow-audit.md`.

**Unreachable scenario**: Link Battler 109–122 is only inserted through native code (see [Link Battler linkage](link-battler.md)), without `3D4B` pointing; reserve 125–127 shares events with S0; S58 "Eternal のフォウ(ボツ)" and S46 Shared events, the end also jumps to S47; 142 only has chapter titles.

## 10. Still unresolved and confirmed with actual machine

### 10.1 remains unsolved

| Project | Where is it stuck | Minimal confirmation method |
| --- | --- | --- |
| The difference between deployment record camp values 4 and 2 | The attack function `8020ABB4` maps both to camp 2; whether the value 4 is saved and affects the AI (for example, not attacking our side) is not pursued. You need to check the use of `800A6E68`/`800A84F8` for `sp+0x2E` | S138 Choose "Cooperation" in the opening game to see if the ハマーン troops attack us |
| Purpose of var117–122 | Tactical overlay `801CF2EC` (called by `801CA97C`) changes the corresponding variable from 3 to 0 on the pilot of aircraft 171–176 and calls `802176A8` (switch display mode); because it is not reset with entry, it only happens once for each person. `801CF2EC` corresponds to which player's operation has not been traced | Monitor the var117–122 bits in `8015E818` in the new game and record the operation when it changes from 3 to 0 |

### 10.2 The conclusion has been drawn and it is recommended to conduct a real machine review

| Project | Minimum Confirmation Method |
| --- | --- |
| Adjacent rules of persuasion (3.1) | The persuader is leaning against the object, and there is no "speakable" in the menu |
| アイナ prerequisites for fighting | S11 Let シロー stick to アイナ without fighting, see if it makes sense |
| アレンビー does not have to be in the same round | S129 After ドモン persuades, the round ends. In the next round, レイン persuades, and the team will join the team at the end of the pass |
| アレンビー S137 Retreat Timing | Record the number of enemies at the moment she retreats after 12 reinforcements appear |
| ガラリア Cancellation condition | S20 Let other mechas hit her until the 4th round, and see if she still turns to our side; another time, let Xiang choose to counterattack when she is attacked, and see if she doesn't switch again |
| ガラリア will be edited after transferring to our side | Check the list on the preparation screen after passing the level |
| フォウ Level Benchmark | S128 Opening Reading `D_8010F5F3` Check the level with our top 15 |
| フォウ Step 3 | S20 Convince フォウ in the save file of var2==1 and see that you will enter the victory settlement immediately |
| リッシュ IA option | Select item 1 in S35, go to S38 and let セレイン stick to リッシュ to see if it makes sense |
| エルリッヒ IA Threshold | Choose item 2 in S27, choose "Put it out" in S30, and see if there is no "sound" in S41 |
| ロゼ No need to convince Maマーグ | S61 No need to convince Maマーグ, when ロゼ is present, use タケル to knock down マーグ, and watch ロゼ appear "Speaking" |
| トッド, シルキー | If you haven’t recruited Kirara and have been persuaded three times, enter the save file in S92 and look at the screen for reinforcements in the 3rd round (not the 2nd round) |
| カーツ 100 shot down | ブラッド 99 shot down to enter S124, after shooting カーツ, see if you can join the team |
| アイシャ CP delayed branch | S69 If you don’t overwhelm the number of enemies, watch アイシャ appear on our side in the third round of the screen |
| After アイシャ joins エルブルス | After joining, open the unit list to see if the pilotless エルブルス is still there |
| ガトー Join the team | S49 Let the バスク advanced base and the flagship advanced base be saved once each to see if you can get GP02A after the level |
| ガトー Leaving the team | S138 Select "すべきではない" and after passing the level, check whether GP02A has left the team |
| シュバルツ Stay in the team | S137 Let Riko attack and pass the level at the beginning, watch シュバルツ on the preparation screen |
| Korra OZ appears | S56 records the screen turn in which Korra actually appeared |
| クェス time window | Don't fight シャア in the round when クェスム arrives, and use アムロ to knock it down in the next round to see if it joins the team |
| MASHIMARAー／キャラ Reinforcements | S103 Watch the reinforcements at the end of the 7th round and the beginning of the 8th round |
| A desperate breakthrough battle | Pass the level within the 10th round to see if it enters S82; only let the flagship enter the green zone to see if it passes |
| ちずる surgical line (N1) | S97 does not attack コンバトラーV, leopard horse shoots down <15, see if S99 can attack |
| The Cow-Knife Ghost (N4) | S25 Let ドレイク retreat first without hitting the Cow-Hungry Ghost (it retreats with the script), and see if the Cow-Knife Ghost appears at the end of S26 (confirm whether type 2 is triggered by `3D46`) |
| ロザミア dropped | S37 Shoot down ロザミア and see that there is no part information (this will lose the recruitment opportunity) |
| ダブルゴッドフィンガー OZ Line | OZ Line アレンビー After joining the team, let the two people be adjacent and have a strength of 130. Look at the God ガンダムH weapon list |
| Squad list | Select the ムゲ universe and the earth circle once each, and see if ゲイル is both unavailable |

### 10.3 Scope and Recurrence

- Not in the script, this article only quotes conclusions: EW dress-up and full-modification unlocking ([Transformation inheritance](upgrade-inheritance.md)), Link Battler joining the team ([Link Battler linkage](link-battler.md)), component drops and combined skill determination (see text for code address).
- Reproduction: The input is the disassembly of `stage_events.jsonl`, `stage_deployments.jsonl`, `stage_auxiliary.jsonl`, `actors.jsonl`, `units.jsonl`, `texts.jsonl`, and `build/recomp/cpu-scan/` produced by `make recomp-data`. The second round of scanning scripts and item-by-item manuscripts (persuasion, protagonist, early, mid-term, late, full scan, process, components, data pages) are one-time analysis products and are not stored in the database; all event addresses in the text can be opened and viewed in the data browser.
- To support the "hidden condition tracking" of [Roadmap](../design/mod-roadmap.md) M3, the variable table in Section 5.1 should be solidified as layout lock data and tested; the type 9 "reserved" and type 2/7 "must be 3" in the directory `trigger.fields` should also be corrected according to sections 3 and 4.

[wiki]: https://akurasu.net/wiki/Super_Robot_Wars/64/Secrets