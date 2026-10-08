> **Language / Ngôn ngữ:** [English](upgrade-inheritance.en.md) · [Tiếng Việt](upgrade-inheritance.vi.md) · [中文](upgrade-inheritance.md)

# Transformation inheritance: How to transfer the number of replacement periods, and which items are really missing

Date: 2026-09-18. Scope: Japanese Rev 0 ROM and static disassembly of this project (`build/recomp/cpu-scan`), extracted body/weapon directory (`assets/original-data/records`). **All conclusions in this article come from static analysis, and there is no running game to reproduce**; items that need to be run to make a conclusion are listed in Section 7. Compare BUG07/BUG08/LEAD01/WATCH01/WATCH02 of [Original Bug Registration](original-bug-register.md).

2026-10-01 Added: `3D5A` The fourth parameter of 2000/3000/4000, the calling timing of EW equipment change, the correction of アースゲイン’s missing weapon name, and Section 10 (deployment addition is not inherited, the number of return segments of the W series five people according to the route, `3D6C` all 38 Article).

## 1. Conclusion Summary

| Conclusion | Basis |
| --- | --- |
| The "inheritance" of changing aircraft is completely driven by two ROM fixed tables: the predecessor table `D_800CA3A0` (30 pairs) determines which body to inherit from, and the weapon mapping table `D_800CB5E8` (114 entries) determines which weapon's segment number is moved to which weapon | `800AA814`, `800AA8F4` |
| The inheritance source is not the old machine number written in the script. The old aircraft in the script is only used for deletion; the inheritance source is the one found by pressing **New Body** on the predecessor table, and it must still be in the roster at the moment | `800AAD28` Steps 4 and 5 |
| The five segments of the body are copied in one block and propagated to other transformed/combined forms | `800AA8C0`, `800AAB5C` |
| Weapon segments are moved piece by piece according to the mapping table; weapons without entries in the table will always stop at 0, even if the new machine has a successor weapon with the same name and the same value | `800AA8F4` weapon cycle |
| Three suspected data omissions: Lenovo's flame radiator and Gore's fire emitterドラゴンファイヤー (EW Dressup). These weapons of the old and new machines have the same name, and all the values are the same except for the basic attack power, but there is no mapping entry | Section 4 |
| `800AA8C0` is copied together with the modification upper limit (`+0x51`), but the subsequent `800AAB5C → 800A5254` reloads the new machine's own ROM record and rewrites the upper limit back, which has **no actual impact**; the same call also recalculates the five values ​​and the power of each weapon according to the number of inherited segments | Section 5 |
| Most of the entries in Akurasu's "Lost upgrades" are not a matter of inherited code: the script is first deleted with `3D5A …,4000`, both human and machine, and then re-registered when returning. The predecessor no longer exists, so naturally there is no inheritance | Section 6 |

## 2. Code path

### 2.1 Entrance

| trigger | position | call form |
| --- | --- | --- |
| Script `3D5A` (the 4th parameter < 2000, including 500 for "do not delete old machines"; ≥ 2000 to delete, see 2.4) | `800A0BA8` → `800AAD28` | `(角色, 参数, 新机, 旧机)` |
| Endless Waltz automatic equipment change | `load_0008F4B0:801CF85C` (the only call point `801D0028`, that is, the transformation screen **after confirming five transformations**) loop table `D_801DC6E4` (5 pairs), when the five segment numbers **all** reach the instance `+0x51`; no driver can also change, and the weapon segment number does not participate | `800AAD28(驾驶员或 999, 目标机, 0, 旧机)`, the old machine is the predecessor and must be inherited |
| Special case of ガンダムmkⅡ 343 → 56 | `load_000AB160:802116CC` | The same function |
| Register only the aircraft (role 999) | `800AAD28` → `800A9A70` | The save/writeback logic is the same as the main path |

`D_801DC6E4`(5 Yes, it is consistent with the guide record): ウイングゼロ→ウイングゼロカスタム、ヘビーアームズ开→ヘビーアームズカスタム、デスサイズH→デスサイズHカスタム、アルトロン→アルトロンカスタム、サンドロック开→サンドロックカスタム. The triggering conditions only look at the five body modifications, not the weapon modifications.

### 2.2 Execution sequence of `800AAD28`

1. There is already "this character + this body" in the roster → return directly (repeated calls are idempotent, and the original script relies on this step for repeated registration in many places).
2. The new machine is 224 ダンクーガ → Hand it over to `800ACB74`: Change the number of the 223 instance in use to 224 and remove all the components. After returning non-0, the main function ends directly. Therefore Dancouga does not go down the inheritance table.
3. Character 999 (only the aircraft is registered) or aircraft 999 (only the pilot is registered) each has a single branch.
4. **Get the predecessor**: `800AA814` uses the new body number to find the predecessor body number in `D_800CA3A0`, then scans the 140 body instance tables, takes the **first** active instance of this number (without checking who the driver is), and stores its `+0x4C..+0x51` six bytes and all weapons (number, segment number, flag triplet) on the stack. Cannot find predecessor → No inheritance will be done later.
5. `800AA464(角色, 新机, 脚本给的旧机)`: Dissolve the relationship between the pilot and the current machine, and delete the instance with the number equal to **Script Old Machine**. In mode 500, the old machine number is 500, so the old machine will **remain in the roster and become a drone**.
6. New machine instance: If it is already in the roster, reuse it (if there is a driver on it, remove it first), otherwise create a new one according to the default driver table `D_800CA418`.
7. If the predecessor is obtained in step 4: `800A5C18` Recalculate the basic value → `800AA8F4` Write back inheritance → `800AAB5C` Propagate the five segment numbers to other forms of deformation/combination.

Step 4 is before steps 5 and 6, so the order of "save first and then delete" is not problematic per se; the problem is that the predecessor has been deleted in an earlier script event (section 6).

### 2.3 `800AA8F4`: All inherited rules

- `800AA8C0`: Write the saved six bytes back to the new machine `+0x4C..+0x51`, that is, the five segment numbers** and the modification upper limit**.
- Other forms in the deformation family (`D_800CB40C` / `D_800CB5A4`) and the combined family (`D_800CAC94` / `D_800CAEF0`) are also written in the same six-byte block.
- Weapons: For each saved weapon, look up the "old weapon number" in `D_800CB5E8`. After a hit, look for the "new weapon number" in the new weapon instance array (`+0x2C` quantity, `+0x30` pointer, step 0x24), and write the segment number into `+0x16`. It cannot be found in the table, or the new machine does not have the target weapon → the new machine will leave this weapon at 0.
- This table is global and does not distinguish between pairs of aircraft; after hitting the first one, you will no longer search further. There are no duplicate source numbers among the current 114 items, so this "only take the first item" will not have any impact for the time being.
- The only additional processing: Weapon 314 ファンネルMAP will inherit bit 2 (unlock bit) of `+0x22`.

### 2.4 Related instructions and bypass

| Item | Behavior |
| --- | --- |
| `3D6C` (`800ACA1C`) | Only find the first instance of this number in our pool (do nothing if it cannot be found). The five items are written as `min(段数, 上限)`, and then `800A95DC` writes the number of segments of all weapons on the aircraft as the same value. Unconditional override can lower the number of inherited segments. Original script 38, see section 10 |
| `3D5A` 4th parameter ≥ 2000 | `800A3540`: **2000 deletes only the driver, 3000 deletes only the body, and 4000 deletes both the driver and the body**; skip deletion when the character reaches 999 (`800A355C`–`800A35CC`, `xori 0xFA0／0xBB8／0x7D0`), original script 3000 are all called with role 999, which is invalid. Any "registered new machine" after 4000 will no longer be inherited (2026-10-01 supplement 2000/3000) |
| `3D5A` Mode 500 | The old machine is not deleted and remains in the roster for unmanned driving |
| `3D6A` Mode 3 (`800AB808`) | ゴッドマーズ Fusion: delete the ガイヤー instance, change the driver pointer, **no segment number is copied** |
| Transformation screen (`load_0008F4B0`) | Five items (`801CFA78`) and each weapon (`801D130C`) are capped at the same `+0x51`, and each weapon +1 +1 |
| Source of aircraft instance `+0x51` | Aircraft ROM record `+0x20` (`800A5330`). This is the upper limit of modification for each machine body |

## 3. Predecessor table `D_800CA3A0` (30 pairs) compared with the upper limit

The upper limit is taken from the body ROM record `+0x20`. The upper limit is listed to document two isolated cases (サンドロック 6, マジンガーZ 12); as mentioned in Section 5, the upper limit itself is not taken away by inheritance.

| Predecessor | Upper Limit | New Machine | Upper Limit |
| --- | --- | --- | --- |
| 3 シャイニングガンダム | 9 | 1 ゴッドガンダム | 9 |
| 53 アルビオン | 13 | 51 アーガマ | 13 |
| 51 アーガマ | 13 | 63 ネェル・アーガマ | 13 |
| 63 ネェル・アーガマ | 13 | 69 ラー・カイラム | 13 |
| 119 ウイングゼロ | 7 | 121 ウイングゼロカスタム | 7 |
| **124 ガンダムサンドロック** | **6** | **126 ガンダムサンドロックchange** | **7** |
| 126 ガンダムサンドロック Kai | 7 | 125 サンドロックカスタム | 7 |
| 127 ガンダムデスサイズ | 7 | 128 ガンダムデスサイズH | 7 |
| 128 ガンダムデスサイズH | 7 | 129 デスサイズHカスタム | 7 |
| 130 ガンダムヘビーアームズ | 7 | 132 ガンダムヘビーアームズ modification | 7 |
| 132 ガンダムヘビーアームズ Kai | 7 | 131 ヘビーアームズカスタム | 7 |
| 133 シェンロンガンダム | 7 | 115 アルトロンガンダム | 7 |
| 115 アルトロンガンダム | 7 | 116 アルトロンカスタム | 7 |
| 171/172/173 ゲッター1/2/3 | 7 | 174/176/175 ドラゴン/ライガー/ポセイドン | 7 |
| 174/176/175 | 7 | 177/178/179 真・ゲッター1/2/3 | 7 |
| 223 ダンクーガ | 9 | 224 ダンクーガ | 9 |
| **262 マジンガーZ** | **12** | **263 マジンガーZ(JS)** | **13** |
| 273 レイズナー | 9 | 270 ニューレイズナー | 9 |
| 30 ソルデファー | 9 | 31 アシュクリーフ | 9 |
| 32 スヴァンヒルド | 9 | 33 ラーズグリーズ | 9 |
| 34 アースゲイン | 11 | 306 スーパーアースゲイン | 11 |
| 36 スイームルグ | 11 | 307 スイームルグS | 11 |
| 259 アフロダイA | 15 | 260 ダイアナンA | 15 |
| 65 メタス | 11 | 67 メタス开 | 11 |
| 73 100 Shiki | 9 | 295 フルアーマーHundred Shiki Kai | 9 |
| 77 キュベレイmkⅡ | 9 | 323 キュベレイmkⅡ | 9 |

The upper limit of the table lookup loop is 30 items (`800AA814`: `sltiu v0,v1,0x1E`), and the 31st item `247/181` immediately following in the ROM is data outside the table and will never be read. In the original script, the three pairs of 127→128, 130→132, and 133→115 will never be triggered (the old machine has already been deleted by `4000` when the new machine is registered), and 124→126 is only truly inherited on the completely peaceful route (Section 10, 2026-10-01).

There are **exchanges without** in the table: ミデア→アウドムラ、アウドムラ→アルビオン、ウイングガンダム→ウイングゼロ、ガイヤー→ゴッドマーズ、ドモン・カッシュ→シャイニングガンダム, エアリーズ→エピオンWait. These upgrades are not inherited, consistent with Akurasu's "Lost upgrades".

## 4. Pair-by-pair results of weapon mapping table `D_800CB5E8` (114 entries)

"Lost" means that the number of modification stages of the weapon is reset to zero after the weapon is replaced. The following table only lists the missing items; Dancouga is not applicable due to the in-place number change route.

| Changing phones | Lost weapons | Does the new phone have corresponding weapons |
| --- | --- | --- |
| シャイニングガンダム→ゴッドガンダム |シャイニングショット、シャイニングフィンガー、シャイニングフィンガーソード | The new machine does not have weapons with the same name (weapons are replaced as a whole) |
| アーガマ→ネェル・アーガマ | Aerial cannon | None |
| サンドロック→Change | クロスクラッシャー | None (this item is not changed) |
| サンドロック开→カスタム | ホーミングミサイル、シールドフラッシュ、ビームマシンガン | None (consistent with the EW armament reduction recorded in the guide) |
| デスサイズ→H | マシンキャノン | None |
| デスサイズH→カスタム | バスターシールド | None |
| ヘビーアームズ开→カスタム | アーミーナイフ | None |
| アルトロン→カスタム | ビームキャノン | None |
| **アルトロン→カスタム** | **ドラゴンファイヤー（470）** | **There are: 1291 ドラゴンファイヤー, attack power 2000→2400, the other values are the same** |
| ゲッター1/2/3→ドラゴン, etc. | ゲッターアーム, ドリルストーム, ドリルパンチ | No namesake |
| Same as above | **ツインビーム（1228）** | **There are: 1244 ツインビーム, the records are exactly the same (combination skills, see section 7)** |
| ドラゴンン→真・ゲッター |スピンカッター、ゲッターサイクロン、チェーンアタック、ツインビーム(1244) | No namesake |
| **レイズナー→ニューレイズナー** | **Fire radiator (1070), グレネードランチャー (1072)** | **There are: 1057 Fire radiator (attack power) 1200→1400), 1059 グレネードランチャー (1400→1600), the other values are the same** |
| スヴァンヒルド→ラーズグリーズ | グレネードランチャー | None |
| アースゲイン→スーパー | Wolf Claw (147), Wolf Fang (149) | No namesake (super form changed weapons). 2026-10-01 Corrected the name of the weapon (previously it was written as "Eyes, Two Claws, Two Teeth"); the Thunder-Charging Tianlong Demon Destruction Formation (1219) is a combined skill and cannot be modified alone, so it is not lost |
| アフロダイA→ダイアナンA | Repair device (1009) | There are: 1012 repair devices, the record is the same (see Section 7 for whether it can be modified) |
| メタス→メタス开 | Repair Devices (269) | There are: 274 Repair Devices, same as above |
| 100-Shiki→Haku-shiki Kai | 60mm バルカンcannon, クレイバズーカ | None |

There is another **dead entry**: `1021 ドリルミサイル → 1028 ドリルミサイル`. 1021 is not in any of the machine's weapon lists (Megatron Z does not have this weapon himself), so this mapping will never hit.

An entry that looks wrong by name but looks good by value: アルビオン's `219 対空レーザー砲 → 210 対空機関砲`, and アーガマ has another `211 対空レーザー砲` with the same name. All the values ​​​​of 219 and 210 are exactly the same, and 211 is stronger, so this item is matched by value rather than by name. This article does not judge it as a missing item, but when changing the mapping table, be careful not to "correct it easily".

## 5. Modification upper limit: copied, but then reset

`800AA8C0` copies six bytes, and the sixth is the upper limit `+0x51`; the unilateral path of `800A9A70` also writes the upper limit of the predecessor into the new machine first. **But both paths will then call `800AAB5C`**, and the first thing `800AAB5C` does is `800A5254(新机, 1)`: this function reads back its own 36-byte ROM record with the aircraft number, writes `+0x20` into `+0x51` (`800A5330`), and presses `+0x4C..+0x50` recalculates HP/EN/Mobility/Armor/Limit, and recalculates weapon power piece by piece (loop starting from `800A55F4`: read back the weapon ROM record to get the basic attack power, and then add it up from `D_800CA590` according to the `+0x16` segment number of the weapon). The pattern propagation loop of `800AAB5C` also calls `800A5254` for each active pattern.

Therefore, the upper limit copy is transient: no code reads `+0x51` from `800AA8C0` to `800AAB5C`, and ultimately each machine uses the upper limit in its own ROM record. **This does not constitute a bug and does not require correction. **

By the way, two data orphan cases are kept (not related to inheritance, only affecting the machine itself): among the 363 machines in the whole table, there is only one 124 ガンダムサンドロック with an upper limit of 6, and only one 262 マジンガーZ with an upper limit of 12; their successors are 7 respectively. and 13, and other W series TV units are all 7. The upper limit simultaneously restricts five items and each weapon (`801CFA78`, `801D130C`), and also determines the trigger point of EW change (from `801CF8AC`, compare item by item with `+0x51`).

This section also explains the point of correction when inheriting missing items: after the segment number is written into `+0x16`, the power is recalculated by the game itself in `800AAB5C`, so the correction must occur after `800AA8F4` returns and before `800AAB5C`.

## 6. Compare Akurasu’s two tables

| Strategy items | Mechanisms found in this project | Judgment |
| --- | --- | --- |
| Medea→Audhumla, Audhumla→Albion transformation is lost | There are no two pairs in the predecessor table; the script `3D5A 46,4,52,64` / `…,53,52` is just a machine change, not inherited | This is the rule, not a code error |
| Gaia→Godmars lost | Go to `3D6A` mode 3, `800AB808` only delete ガイヤー and change the pointer, no copy | The rules are like this |
| The machine in the W series (Sandrock→Kai, Deathscythe→H, Heavyarms→Kai, Shenlong→Altron) is lost, but the new machine comes with 3 segments | The script is deleted with `3D5A …,4000` in the event of leaving the team (such as scene 032/036/046), and when returning, use mode 500 to register or join with deployment records. The predecessor no longer exists → no inheritance. The number of regression segments **different according to the route**: there are 0, 3, and 5 segments, not all 3 segments (Section 10, 2026-10-01) | Script flow, non-inherited code error. The loss actually occurred in the episode of **leaving the team**, not the episode of changing phones |
| Wing Zero (Hiro) was lost in OZ 36 | `3D5A 95,0,119,4000` was deleted at the end of scene 057, and `…,119,500` was created in scene 073; and 117→119 was not in the predecessor list. 2026-10-01 Supplement: What was deleted at the end of OZ Chapter 33 was the temporary flying-wing Zero driven by Jacks (deployment group 3, stage 0); the next-generation Gundam previously used by Hero was given to Jacks in a reused manner together with modifications (`001C7984@248`), so there is no modification to be lost in the OZ route | Same as above |
| Transformation and reset after Spiegel left the team and then rejoined (BUG07) | In many cases of leaving the team, `3D5A 3,0,0,4000` (deletion of the entire body) was used, and when he rejoined, he used mode 500 to create a new one; the aircraft was not in the predecessor's list | The script used "Delete the entire body" instead of mode 2000, which only deleted the pilot; whether it was a design choice or an omission requires plot basis |
| レイズナー→ニューレイズナー The flamethrower modification is missing (BUG08) | The mapping table is missing 1070→1057, **also missing 1072→1059** | Suspected data missing items, the guide only mentions one of them |
| Some weapons in the EW version are not inherited correctly (LEAD01) | The disappearance of the Desert/Reaper/Heavy weapon belongs to the weapon itself being cancelled; but the アルトロンカスタム's ドラゴンファイヤー does exist (1291) but there is no mapping |アルトロン's ドラゴンファイヤー is currently the only specific candidate that matches LEAD01 |
| Components were removed when the machine was changed and automatic attack | `800ACB74` (ダンクーガ) explicitly called `800A9D60` to remove the components; the component processing of other paths was not checked in this round | Not verified, reserved for follow-up |

## 7. Items that have not yet been verified

The following all need to run the game to make a conclusion. This round has not been run. `config/recomp/mini-stages/inherit.json` has prepared four use cases (Layzner, Altron→Custom, Albion→Argama, and "whether re-registering when the old machine is still on the roster will cover the number of new machine segments") according to the writing method of [mini level](../script/mini-stage.md). It can be compiled and run directly; the usage is to first write `3D6C 机体,N` to write all the weapons of the old machine into the same segment number, and then it will always be 0 after changing the machine. weapons are not inherited.

1. The actual performance of three suspected omissions (1070/1072/470) on the real machine.
2. The number of weapon segments of the newly created new machine instance does start from 0 (structurally, this is true, but `800A6B30` is copied from the template record when the table is created and is not confirmed frame by frame).
3. ~~ダンクーガ's 対空剣: 223 form uses 873, 224 form uses 880, the two are different weapon instances, and the `880 → 873` direction in the mapping table is opposite to all other entries (the source is for new machines only, and the target is for old machines). Since the in-situ number change path does not check the table at all, you need to confirm whether the 対空剣 transformation on 223 is still there on 224. ~~ 2026-09-18 Static solution: The weapon name is the Sky Sword; ダンクーガ. The weapon list of the whole family has 873 and 880 at the same time. After each modification of the modification screen, `800A5F84` synchronizes the power and segment number to another item. The number is changed in place without moving the weapon array, so it will not be lost ([Transformation segment number](upgrade-limits.md) Section 5).
4. ~~Can repair devices (1009→1012, 269→274) and combined skills (1228→1244) be modified independently? If not, these two types of "loss" have no actual impact. ~~ 2026-09-18 Static solution: Both categories are transformation type 0; the repair device has a power of 0 and is rejected before entering the confirmation (`801D0970`), and the ツインビーム has a combined skill position and does not enter the transformation list (`801C7254`). None of them can be modified individually, and the lack of these entries in the mapping table has no practical impact ([Number of Modified Segments](upgrade-limits.md) Section 6.1).
5. Is MaジンガーZ no Maドリルミサイル (1021 not in any weapon list) consistent with the strategy?
6. Will the old unmanned aircraft left behind in Mode 500 really appear on the roster/maintenance screen in the original process?
7. Overwriting risk of "inheriting again when reusing an existing machine": If the predecessor and successor are in the roster at the same time, registering again will overwrite the successor with the predecessor's segment number (`800AAD28` steps 6 and 7). Whether such a route combination exists in the original script has not yet been investigated one by one.

## 8. Optional adjustment plans (8.1, B0 and 8.5 have been implemented, the rest have not yet been implemented)

The causes of the three types of problems are different, and the changes in laws and costs are very different. The costs are listed from small to large. Common premise: According to the agreement of [Optional Rule Modification](rule-fixes.md), the modification category is enabled by default and the difficulty category is disabled by default. When closed, the host only calls the original function; the ROM and the archive format are not changed.

### 8.1 Correction A: Add three weapon mappings (implemented on 2026-09-18, not verified on actual machine)

Corresponding to BUG08 and LEAD01, the modification surface is the smallest and the boundary is clearest. The switch `weapon-inherit-map` is classified into the correction category (it is turned on by default, and can be turned off in the game "Options → Gameplay Adjustments"); for implementation, see `inherit_missing_weapons` of `src/host/rule_fixes.hpp` and `resident_func_800AA8F4` of `game_hooks.cpp`. The unit test is in `tests/native_rule_fixes.cpp`. **Not yet run in the game**, verification of Section 7 still needs to be done.

| Item | Content |
| --- | --- |
| id | `weapon-inherit-map` |
| binding | `NATIVE_HOOKS` of `tools/recomp/toolchain/generate_cpu.py` is increased by `"resident_func_800AA8F4": "srw64_original_weapon_inherit"`, then `make recomp-cpu` |
| Packaging location | Added `resident_func_800AA8F4` in `src/host/game_hooks.cpp`: call the original function first, and then write three pairs of mappings |
| Parameters | `a0` = new machine instance; `a1` = saved old machine weapon array (4 bytes per piece: u16 number, u8 segment number, u8 flag); `a2` = number of pieces; `a3` = saved six-byte segment number |
| Supplementary table | `{1070→1057}` (fire emitter), `{1072→1059}` (グレネードランチャー), `{470→1291}` (ドラゴンファイヤー) |
| What to write | Find the old number in `a1` and take its segment number. Find the new number in the new weapon array (`+0x2C` number of pieces, `+0x30` pointer, step 0x24, `+2` number) and write `+0x16`. **Don't use power**: The two call points of `800AA8F4` (`800AB2F8`, `800A9CB0`) are immediately followed by `800AAB5C → 800A5254`, and the power will be recalculated according to the number of segments (section 5) |
| Scope of effect | Only these three pairs of aircraft exchanges will take effect, and they will only take effect on the exchange of aircraft where the "predecessor is still on the roster"; the other aircraft and other routes will remain completely unchanged |
| Archive Impact | The number of segments written into the roster is persistent. The switch only works at the moment when the replacement occurs. Turning it on or off will not destroy the old gear, but the replacement that has already occurred will not be retroactively compensated |

~~After Section 7, Item 4 is confirmed, three more candidates can be considered: `1228→1244` (Fusion Technique), `1009→1012` and `269→274` (Repair Device). ~~Section 7, Item 4 has statically confirmed that these weapons cannot be modified individually and do not need to be repaired.

### 8.2 No need to change: upper limit of transformation

Section 5 has confirmed that the `800AA8C0` replication limit is reset by `800A5254`, making the originally thought `upgrade-cap-keep` switch unnecessary.

### 8.3 Fix B: Script level missing

Most of the "Lost upgrades" in Akurasu (W-series mid-game machine, Spiegel, Mizuno, Ayaru, and Gyro) are not a problem with the table, but with the script using `3D5A …,4000` to delete both the player and the machine, and the funds invested by the player disappear together with the random body. Of the three modification methods, **refund is the most restrained one**:

#### B0: Refund transformation funds when deleted (implemented as difficulty adjustment `upgrade-refund` on 2026-09-18, see [Optional Rule Amendment](rule-fixes.md) §2.6)

It does not change the strength curve of any aircraft, nor does it allow the EW equipment change to be triggered in advance. It only returns the "wasted money", and players can re-decide which aircraft to invest in. The feasibility has been checked into the price model:

| Item | Original data |
| --- | --- |
| Five unit prices of the body | Five 15-segment tables `D_801DC36C`(HP)/`3AC`(EN)/`3EC`(movement)/`42C`(armor)/`46C`(limit), the price is based on the **current number of segments**, **irrelevant to the body**. Example: HP per section 2000, 4000… 30000; Movement 5000, 8000… 65000 |
| Weapon unit price | Select one of the four 16-item tables according to the weapon modification type (weapon record `+0x0E` → instance `+0x15`), and then take the price according to the current segment number (for example, type 4 uses `D_801DC6FC[段数]`), **has nothing to do with the upper limit of the machine body**. 2026-09-18 Correction: `D_801DC340[上限−5]` written in the original text is a scale bar string table, not a price list. See [Renovation of segments](upgrade-limits.md) Section 3 |
| Amount spent | For each item/weapon, just sum up the unit prices of 0...the current number of stages - 1, which can be completely calculated by the host |
| Funding | `D_8010F5F4`(u32) |

Three things to solve when landing (for implementation details, see [Optional Rule Amendment](rule-fixes.md) §2.6):

1. **Which deletions are to be rolled back**: Only the ones that "will not be inherited" will be rolled back. `800AA3C4` is the only exit for deleting an organism instance (the caller `800AA464` twice, `800AB808`, `800A7DEC`, and the sales screen `801C3678`), but it itself does not know the calling context. The implementation wraps `800AA464` and `800AB808` as the refund range (`800A7DEC` and sale are not among them), and wraps `800AAD28`: Find the instance that will be inherited this time according to the predecessor table. If it is this instance that is deleted, no refund will be given. In addition, only our instance pool (the 0th pool of `800A6E68`) will be refunded, and the `3D6C` stages given in the plot will not be refunded.
2. ~~**Weapon Category Field**: The weapon price list is branched by category, and which byte of the weapon record the category is taken from has not yet been confirmed. ~~ Confirmed to be weapons record `+0x0E` (2026-09-18).
3. **Division of labor with 8.1**: The missing items of each weapon will be accurately repaired by 8.1; refunds will only be responsible for coarse-grained losses such as deletion of the entire machine, and the two do not overlap.

#### B1/B2: Reserve or backfill the number of transformation segments (more expensive)

- **Plan B1 (Narrow)**: For the designated "return after temporary departure" character + aircraft + scene whitelist, downgrade `4000` to `2000` (only the pilot is deleted, the aircraft remains in the roster). The changes are concentrated, but it is necessary to confirm one by one that the mecha should be retained in the plot, otherwise it will leave a mecha in the roster that should have disappeared; and the returning `3D5A …,500` will reuse the old instance left behind, and subsequent `3D6C 机体,3` will still **overwrite** the number of stages.
- **Plan B2 (wide)**: On the host side, remember the five segments and the segment numbers of each weapon of the deleted instance according to the body number, and backfill it when the same body number is re-registered. The original structure is not changed, but this memory must be entered into the save collection ([Roadmap](../design/mod-roadmap.md) M2), otherwise the file reading will be invalid; and it must be decided whether the coverage of `3D6C` should remain as usual or be changed to a larger value - if it remains the same, the W system mid-range interval is still fixed at 3 segments, and backfilling is useless.
- Both solutions obviously change the resources and strength. They belong to the rule package rather than QoL. They require separate effect description and compatibility acceptance with the old files.

### 8.5 Parts accompanying (implemented as difficulty adjustment `parts-carry-over` on 2026-09-24)

When changing the machine, all the enhanced parts of the old machine will be removed (`800AA3C4` → `800A9DCC` → `800A9D60`). Unloading ** is not destroying **: Inventory record `D_8015E990` Each component has a u16, the high byte holding number, and the low byte equipment number. Unloading only reduces the equipment number, so the parts are returned to the warehouse, but the new body is empty and cannot be reinstalled until the next maintenance. After opening `parts-carry-over`, the packaging of `800AAD28` takes over before and after the original function, and installs the components into the empty slots of the new body in the original order.

The number of slots is taken from the aircraft record `+0x19` (instance `+0x21`). Only eight of the 30 sets of replacements will be reduced, all of which are 2 → 1: five EWs and three Shineゲッター; one of these replacements will be left in the warehouse at a time. The rest (including the 3 slots of the Maxion Z and the 1 slot of the ship) are consistent. See [Optional Rule Amendment](rule-fixes.md) §2.7 for details and verification.

### 8.4 Landing sequence

1. 8.1 has been implemented and passed the unit test; it still needs to run the verification of Section 7 (`config/recomp/mini-stages/inherit.json` is ready) to confirm three missing items and "the number of new instance segments starts from 0".
2. B0 refund has been implemented (`upgrade-refund`, closed by default), with screen prompts and review records; verification has not yet been triggered in the actual plot.
3. If B1/B2 is to be done, the preparatory work is to complete the plot basis of "which departures from the team are temporary".

## 9. Circumstantial evidence and other findings

- **`3D6F` is "unlocking the weapon", not a component operation**: it clears bit 2 of the weapon instance `+0x22`. The 11 parameters of the original script are all the special weapon numbers unlocked in the plot (19 Rock-breaking Fist, 1215ダブルゴッドフィンガー, 53/62/71/76 シャッフルAlliance machines, 770/773/775/777 コン・バトラーV, 874 対空光剣). This bit is exactly the one in `800AA8F4` that was specially inherited by 314 ファンネルMAP. The `3d6f` entry for layout lock `config/data/original-jp-v1.json` has been corrected in-place with this analysis (was "Clear Part Record Flag (Part Number)").
- Therefore, the first 700 items × 36 bytes of the area named `part_instances` (from `0x80178F80`) in the status probe `src/host/state_probe.hpp` are the **weapon instance pool**: the body instance `+0x30` points to it, and `+0x2C` is the number of pieces. Reinforcement components are another set of structures (aircraft instance `+0x21`/`+0x23` slots and `D_8015E990` inventory, see `800A9D60`). The name of the area has not yet been revised.
- The predecessor search does not look at the driver, but only takes the first active instance with a matching number.
- The stack buffer used to save weapons is 50 items, and the maximum number of weapons in the entire table is 28 (ランドライガーH), which will not overflow.
- Transformed forms share the same weapon instance array (for example, ゲッター1/2/3 share 12 pieces), so the weapon modifications of each form are the same data.

## 10. Deployment join, `3D6C` full table and W series according to the number of segments of the route (Supplemented on 2026-10-01)

All are static conclusions (disassembly + `stage_events.jsonl`/`stage_deployments.jsonl` full script scan), not actual machine.

### 10.1 Deployment join does not inherit

`3D45` Deployment record camp 0 (and record value 3) falls in pool 0 (our side). `8020ABB4`: When the pilot number < 287, first find the aircraft where the pilot is located in the roster **reuse** (at this time, ignore the aircraft number and enhancement index in the record, `8020AC38`–`8020AD58`); if not found, create a new one, and write the five items as `D_800CB5DC[强化索引]` (ROM `0x55FCC`: `0,1,3,5,7,9,11,13,15`), all weapons of the non-transforming combined machine (`800A79EC` returns 0) are also written with the same value (`800A95DC`; `8020AFB4`–`8020B044`). Deployment and joining do not pass through `800AAD28`, and **does not make any inheritance**.

`80211680` (called by the tactical map exit process `801DFD14`) mkⅡ 343→56 number change: 343 only appears in the real system episode 5 "Black Gundam" deployment group 3 (`001E6E04`). It has not been maintained when changing numbers, and there is no modification to throw away.

### 10.2 The number of stages when the five members of the W series return (according to route)

Leaving the team is `3D5A …,4000`: Flying Wings/Heavy Equipment/Death/Desert at the beginning of OZ Chapter 21 (`001BC304`), the end of Chapter 22 of the Independent Army and Complete Peace (`001AB4A0`); Shenlong chooses OZ at the end of Chapter 20 (`001A9E0C@804`) or Chapter 22 The end of the story.

| Aircraft | OZ | Complete Peace → Sutelles | Complete Peace → Fighting Alone | Independent Army |
| --- | --- | --- | --- | --- |
| Desert Gundam Kai (カトル) | Deployment in episode 33 (`001C71BC` group 3, index 0) → **0** | Episode 28 opens with the return of Desert Gundam (`001B6FA0@68` + `3D6C 124,3`) → 3; end of episode 32 `3D5A 89,0,126,124` Transfer **True Inheritance** (Only Lost クロスクラッシャー) | Same as Left | Chapter 36 Opening `001B3F30@780` + `3D6C 126,3` → **3** |
| Hell Death Gundam (デュオ) | Chapter 34 Deployment in the Pass (`001C8240` Group 4, Index 3) → **5** (Five items and weapons) | Chapter 34 Deployment in the Pass (`001BB348` Group 7) → 3 | Beginning of Chapter 35 `3D5A …,500` (`001BA234@186`), none `3D6C` → **0** | Deployed in episode 28 (`001AF65C` group 6) → 3; if not triggered, end of episode `3D5A` + `3D6C 128,3` (`001AF8E8@82/92`) → 3 |
| Flying Wing Zero (ヒイロ) | Chapter 36 Deployment in Guanzhong (`001C98F0` Group 6) → **0** | Chapter 35 Deployment (`001B7E94` Group 6, Index 2) → 3 | Chapter 35 Opening `3D5A …,500` (`001BA234@166/514`) → **0** | Episode 36 opening `001B3F30@770` + `3D6C 119,3` → 3 |
| Heavy Gundam Kai (Toro) | The end of Chapter 45 `001D9430@310/320` → 3 | Same as OZ | The opening of Chapter 42 `001CEC70@1138/1148` → 3 | Same as left |
| Double-Headed Dragon Gundam (Five Flying) | End of Chapter 45 `001D9430@294/304` → 3 | Same as OZ | End of Chapter 45 `001D0FEC@402/412` → 3 | Same as Zuo |

Predecessors 127→128, 130→132, 133→115 are therefore never triggered in the original scenario; 124→126 are only triggered in the completely peaceful route.

### 10.3 `3D6C` All 38 items (26 units)

Actual number of segments = `min(N, 该机上限)`, only applies to the first unit in our pool.

| Level (event) | Body | N | Conditions |
| --- | --- | ---: | --- |
| Real Episode 3 Ending (`0019F6D0@446`) | Gundam Ez8 | 1 | シロー Join |
| End of chapter 6 of the real series (`001A0E80@98/124/150`) | Guntank/Gundam/Gundam | 1 each | var128≠3, and keep each (var129/130/131=0) |
| The opening of episode 9, real system (`001A278C@508`) | Jie Gang | 1 | エマ joins |
| The opening of episode 10 of the Real Series (`001A2F9C@592`) | Dole (シモーヌ) | 3 | — |
| End of Chapter 11, Super Type (`001A4680@346`) | Gundam Ez8 | 3 | シロー Join |
| Independence Army/Complete Peace Chapter 22 Opening (`001AADDC@232/238`) | Baldi, Beble | 3 each | — |
| Independent Army/Complete Peace Chapter 22 Ending, Reality (`001AB4A0@310`) | Graeme Caesar | 3 | var0=0 |
| Independence Army Chapter 28 End of Pass (`001AF8E8@92`) | Hell Death Gundam | 3 | var129≠1 |
| The opening of Chapter 36 of the Independence Army (`001B3F30@790/796`) | Flying Wing Zero, Desert Gundam Kai | 3 each | — |
| Complete Peace Chapter 26 End of Pass (`001B6534@172`) | Full Armor Hundred Style Change | 8 | **Failed**: There is no 295 in this route roster |
| Complete Peace Chapter 27 Ending (`001B6CCC@172`) | MinervaX | 5 | var128=1 |
| Complete Peace Chapter 28 Opening (`001B6FA0@78`) | Desert Gundam | 3 (maximum 6) | — |
| Complete Peace Chapter 30 End of Pass (`001BBD3C@346`) | Mass-produced Great Demon God | 3 | — |
| Complete Peace (Suiteles) Chapter 35 Opening (`001B7918@298`) | Next Generation Gundam (ゼクス) | 3 | — |
| OZ Episode 22 Opening (`001BCEA8@1540/1546`) | Baldi, Beble | 3 each | — |
| End of Chapter 26 of OZ (`001BFF5C@686/1362`) | GP02A | 3 | var37=0; var37=3 branch is not registered GP02A, **failed** |
| OZ Episode 27 Opening (`001C10F8@1076`, `001C1B94@1448/1636`) | Sigurun | 3 | var14 |
| OZ Chapter 28 (`001C283C@252`, `001C3658@662`) | Graeme Caesar | 4 | var0=0 |
| OZ Episode 31 When All Enemies Are Destroyed (`001C62AC@44`) | Next Generation Gundam (ヒイロ) | 3 | — |
| "Stand side by side from now on" Guanmo (`001E2F44@118`) | Nowruz | 4 | — |
| "The End of Time" Guan Mo (`001E31FC@354`) | Vairos | 3 | var128=0 |
| The end of OZ Chapter 37 (`001D5C48@502`) / The end of Chapter 40 of the Independent Army (`001D3EB4@294`) | Zelong | 3 | var26=2 |
| The opening of Chapter 42 of the Independence Army (`001CEC70@1148`) | Heavy Gundam Kai | 3 | — |
| Independence Army Chapter 45 End of Pass (`001D0FEC@412`) | Double-Headed Dragon Gundam | 3 | — |
| OZ Chapter 45 End of Pass (`001D9430@304/320`) | Double-Headed Dragon Gundam, Heavy Gear Gundam Kai | 3 each | — |
| End of Chapter 51 (`001DFB88@644`) | Noye Gill | 3 | var11=0 |
| End of Chapter 54 (`001E1B18@1210`) | Acto Deka | 6 | var47=0 |

Waiting for real machine: Deploy whether the added instances of our team will be retained at the end of the level (10.2 depends on this; the minimum confirmation is to see if Hell Death is 5 stages after OZ Chapter 34); two failed `3D6C`; the number of stages after the Thunder King is combined.

Return: [Original Bug Registration](original-bug-register.md) · [Built-in MOD Roadmap](../design/mod-roadmap.md) · [Technical Document Index](../README.md)