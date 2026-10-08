> **Language / Ngôn ngữ:** [English](battle-formulas.en.md) · [Tiếng Việt](battle-formulas.vi.md) · [中文](battle-formulas.md)

# Combat calculation: damage, hit, critical hit, defense determination and mental command

Date: 2026-09-20. This article records all the calculations actually performed by the game in a battle: damage and hit formulas, critical hits, five types of defense determinations, the three commands of the defender, and how mental commands rewrite these values. **Unless otherwise noted, the conclusions are static code confirmation** (disassembled `build/recomp/cpu-scan/load_000AB160/rom_801C2600.text.s`, the table value is read directly from `rom.z64`); the damage formula is consistent with 24 lines of running data. For performance (animation), please see [Combat Animation and Customized Aircraft](../data/battle-animation.md), and for image resources, please see [Combat Images](../data/battle-graphics.md).

2026-10-01 According to the static verification on the strategy data page, the love correction distance, terrain byte order, must-hit skip range, shield's weapon condition/EN/defense doubled/reset to zero, てかげん's comparison amount and mental duration were corrected, and the round start settlement, V-MAX, super mode and knockdown fund bonus (§7) were added; dates and addresses were noted everywhere.

The direct motivation for writing this document was the pre-war interface: the original version only showed the hit rate. Players could not see the damage, critical hit rate, the opponent's clone/cutting/shielding probability, nor the number of remaining clones. To make up for these, you must first confirm the formula to the extent that you can recalculate it yourself.

## 0. The order of execution of a battle

```
801F7D6C  结算驱动（命中 801F4384 与伤害 801F5628 各三次：攻击／反击／二次攻击）
  └ 801F7204  判定顺序：命中掷骰 → 分身 → 切り払い → 假身 → 护罩 → S防御
```

All calls inside `801F7D6C` fall in the `801E*`/`801F*` logical area. There are no calls to resident graphics/wait routines and no blocking primitives. In the running data, the attack and counterattack of a round of combat are recorded in the same VI (5316/6956/8336 of `rules-battle-1`). Based on this, it is inferred that settlement and performance are separated, and a round of settlement is inseparable - but the battle animation was not played in this run, so "settlement precedes performance" has not been directly covered by the run evidence. The evidence on the other side is that the **defense reaction code** set in `801F7204` is exactly what is read when the animation is played (see the reaction code table of [Battle Animation](../data/battle-animation.md)), and the two correspond one to one.

## 1. Damage

IEEE single-precision floating point throughout, and finally `trunc.w.s` rounded. `80203418` is an estimated version that does not throw critical hits (**does not consume random numbers**, and can be safely called in the pre-war interface), `801F5628` is an actual combat version, and both **until the love correction and the lower limit of 10** are the same instruction by instruction (the estimated version also applies love correction, but does not throw critical hits; 2026-09-22 disassembly review `802035C8..80203644` and `801F5884..801F5928`).

```
stat = (武器[+0x04] & 0x80) ? 驾驶员[+0x22] 格斗 : 驾驶员[+0x24] 射击

A = 武器攻击力 × 武器地形适应 × stat/100 × 攻方气力/100 × 机体地形适应
D = 装甲 × (鉄壁 ? 2 : 1) × 守方气力/100 × 守方机体地形适应
R = (A − D) × 地形效果                    # 地形效果 = (100 − 地块防御)/100
R = R + (爱A ? R×0.3 : 0) − (爱D ? R×0.3 : 0)
R = max(R, 10)                            # 下限 10
if 攻方精神 魂:   R ×= 3
elif 攻方精神 熱血: R ×= 2
else【仅实战】暴击命中: R ×= 1.5
【仅实战】防御指令: R ÷= 2
【仅实战】守方机体 id == 149 → R 固定 10；R = min(R, 65535)
```

Key points:

- **Vigor** multiplies once on each side of the offense and defense (`80203528` for the attacker, `lhu 0x20($s2)`, `80203578` for the defender), with a base of 100.
- **Terrain adaptation is multiplicative, not additive**. The magnification tables `D_80218744` (ROM `0x1012A4`) and `D_8021874C` (`0x1012AC`) are both `{0, 60, 80, 100, 120}`, that is, `-`/D/C/B/A → 0/60/80/100/120%. Weapon A + Machine A total **1.44 times**.
- **On the aircraft side, take the sum of the aircraft ranking and the pilot ranking and then divide it into different grades** (`800A6194`: sum 0→0%, 1–3→60%, 4–5→80%, 6–7→100%, **≥8→120%**); the weapon side is a single ranking (`801F40A4`).
- **The terrain channel is determined by the body handle**, do not read the battle table `+0x10`: `801F3FA8`, judge in order: whole map universe → space, altitude category = 1 → air, water block → sea, otherwise → land.
- **Size does not enter into the damage formula**. The size (0/80/100/120/140) is only the true multiplier in the hit rate function `801F4568`/`801F4580`; there is only a degenerate branch in the damage that will never trigger on the real body.
- **Love/Friendship Correction ±30%** (`801F4908`). The attacker holds +30% and the defender holds -30%, which only affects damage and does not affect hits; when the first partner is found, 1 is returned, without stacking.
- **The distance is the sum of the horizontal and vertical distances ≤ 2** (including diagonal adjacent ones, 13 grids in total): `801F4A2C..801F4B7C` marks the row width 1/3/5/3/1 in the 31×31 grid with the **holder** as the center rhombus, each grid then passes the "grid within the map" check (`x ≥ 原点+32`, `x ≤ 原点+地图宽−48`, `D_80172EC4` is written by `801C6394`, the same judgment as the movement range `801C44D4`/`801F2B24`), and then scans our handle 0x42–0x5F The partner in the picture. Regardless of the visible range of the screen. (Correction on 2026-10-01: It was previously written as "a 31×31 window anchored by the lens and then cropped to the viewport".)
- Only for our side: `801E510C` returns 0 if the camp is not 0 (`801F49FC`); the roster `+0x101 & 0x80` also returns 0 if it is set. In scenes 4–9, the characters 196 Kagu and 197 Yuko have no corrections as holders (`801F4988..801F49C4`).
- Pairing table `D_80218754` (ROM `0x1012B4`), 47 lines × 8 bytes: `+2` holder role number, `+4`/`+6` partner 1/2 (−1 None), `+0` code not read. Both partner columns are compared (`801F4C64`/`801F4C78`), so row 24 デューク←ひかる,ナイーダ and row 27 デューク←ひかる,ナイーダ are compared with row 27 锅←さやか,マリアWith their respective reverse rows, they are both **bidirectional** (checked on 2026-10-01).

### Ranking byte position

| | ROM table | stride | intraline offset | order |
| --- | ---: | ---: | --- | --- |
| Aircraft | 465792 | 36 | **14–17** | Air/Land/Sea/Space |
| Weapons | 478864 | 16 | **9–12** | Same as above |

2026-10-01 Revised order (previously written as "Sea/Air/Land/Space"): `800A5254`'s Minovsky aircraft is branched to mobile type `0x02` and written body instance `+0x16 = 4`, weapon instance `+0x10 = 4` (that is, the first byte is empty), super mode `801FE96C` Only change the weapon `+0x11..+0x13` (land/sea/space); ROM data アーガマ `[A,-,-,A]`, ゲッター3 `[-,A,A,B]` consistent.

Other fields in the same table: airframe `armor` is at offset 10 (u16) in the row; weapon `power` is at 1 (×100), `hit_modifier` is at 4 (**signed**), `en_cost` is at 6, `will_required` is at 7, `critical_modifier` is at 13 (signed). Note that the `numeric_fields` offset of `config/data/original-jp-v1.json` is the ROM table in-row offset, not the runtime record offset - reading at the runtime offset will get irrelevant fields.

### Run verification

The 24 lines of `build/recomp/mini-stage/rules-aura-1/rule-probe.jsonl``damage` (the probe calls the real `80203418`) are exactly matched by **24/24** after being substituted into the above formula, and the residual is 0. The terrain of this level is empty, and the strength of both sides is constant 100.

> **Methodological warning. ** The same data is fitted with "`1.2 × (攻击力 − 装甲) + 每攻方常数`" ** which is also 24/24 accurate**, but the structure is completely wrong - because in this data set, the power is always 100 and the attacker's weapon terrain adaptation is always A, both variables are absorbed into the constant term. The true form is pure multiplication followed by subtraction without any additive constant. **Fitting and agreement does not mean that the formula is correct**; the variables must be truly changed, or cross-validated with the code/strategy.

The force item has not been covered by operational data so far (the force of all existing data sets is constant 100). [`config/recomp/mini-stages/damage-morale.json`](../../config/recomp/mini-stages/damage-morale.json) has been prepared for this: a single command change to `rules.json`, inserting `3D5F` (overall strength 100→70) before the first `3D38`. The comparison between the predicted value and the actual measurement has not yet been completed.

## 2. Hit rate

```
base = (攻方命中 + 攻方反应 + 武器命中修正 + 100 + 攻方运动性)
     − (守方回避 + 守方反应 + 守方运动性)
       再乘尺寸与地形倍率（801F4568 / 801F4580）
```

Short circuit and correction (`801F4384`, in the order of code appearance):

| Condition | Effect | Location |
| --- | --- | --- |
| **Defending** Spirit ひらめき（`+0x1C & 0x20`） | **Return 0** directly, and set the "Avoid!" prompt flag | `801F4460` |
| **Attack** Spirit must hit (`& 0x80`) | **Directly return 100** (Delay slot `addiu $v0,$zero,0x64`) | `801F44A0` |
| **Attack** Mental Concentration (`& 0x10`) | `hit += 30` | `801F4584` |
| **Defender** Mental concentration | `hit −= 30` | `801F45A4` |
| **Attack** `+0x1C & 0x800000` (Spirit id 23, chaos, added to each enemy/third-party unit by the caster `801D9F94`) | `hit ÷= 2` | `801F472C` |
| **Avoid command** (halve parameter) | `hit ÷= 2` | `801F4750` |

The last two items are **independent and stackable** (up to ÷4). Note the MIPS delay slot: `andi $v0,$s7,0xFF` of `801F473C` is executed before the previous branch takes effect, so the second judgment uses parameters rather than mental bits.

Roll on `801F7204`: `hit` clamp 0–100, `r = rand(99)+1` (**1..99**), `hit >= r` hit. So **a hit rate of 99 has the same effect as a 100**, and a hit rate of 0 never hits.

> This formula accurately matches only 2 of the 24 lines of `rules-aura-1`, and the residuals vary systematically with the weapon and defender's body - the specific method of selecting the size/terrain multiplier has not been confirmed item by item. **The pre-war interface should directly call the game's estimation function `80204254`** (also does not consume random numbers, `rule_probe.hpp` has encapsulated the battle table save/restore), rather than recalculating by itself.

## 3. Critical hit

`801F47B0`:

```
rate = 攻方技量[+0x2C] − 守方技量 + 武器暴击修正[行内偏移 13, 有符号]
阵营 0（我方）：rate += 底力补正（801E1D64，0–90）
阵营 1、2（敌／第三方）：rate /= 4        ← 且不加底力
rate = max(rate, 1)
暴击 = rand(100) < rate     →  伤害 ×1.5
```

The camp is determined by the attacker's handle: `801E510C` is divided into three categories according to `<0x60 / <0x7E / 其他`, and the handle code is `0x42/0x60/0x7E + 槽位` corresponding to camp 0/1/2 (see `src/host/rule_probe.hpp:27`).

**The enemy almost never gets critical hits. ** There are only eight types of weapon critical hit corrections in the table: `-20/-10/-5/0/10/15/20/30`; the boss’s basic skills are 95–117, and against allies with about 120 skills:

| Enemy | Base Skill | Weapon +0 | +20 | +30 |
| --- | ---: | ---: | ---: | ---: |
| ギュネイ | 117 | 1% | 4% | 6% |
| ガトー | 110 | 1% | 2% | 4% |
| ハマーン | 108 | 1% | 1% | 4% |
| シャア／シロッコ | 105 | 1% | 1% | 3% |
| キラル・メキレル | **155** | 8% | 13% | 16% |

Among the 257 pilots, the one with the highest basic skill is Kirara (155), which is only 16% even with +30 weapons. Under the same conditions, we can reach 29–32%.

**No critical hits are rolled when blood/soul is in effect**: `801F5A14` is only called when neither bit is set, otherwise the critical hit flag is forced to 0. That is, "Hot Blood ×2" and "Crit ×1.5" **cannot coexist**.

## 4. Defense judgment (after hitting, early exit series)

Sequence: **Clone → Cut → False → Shield → S Defense**. Each item only works on attacks that "should have hit", so when the probabilities are displayed they are **conditional probabilities**. When the attacking pilot's `+0x1C & 0x80` (must hit) is set, **only skips the clone and cut り払い**: `801F7204` only checks once after these two items for a sure hit (`801F7384`, `801F73D8`), the fake `801F6E3C` and its consumption location `801FCC28` No matter what, the shield and S defense are the same. (2026-10-01 Correction: It was previously written as "skip the first three items".)

| Judgment | Probability/Effect | Condition | Location |
| --- | --- | --- | --- |
| **Clone** | **Fixed 50%** | Body `+0x28 & 0x163011` and pilot strength `+0x20 ≥ 130` | `801F6C44` |
| **cutり払い** | `等级 / (16 × scale) × 100%`: `scale` The **defender** handle passes through `801E510C` to get the camp, our side (0) is 1, the enemy and the third party are 2, that is, our L9 = 57% (throw 0–99 is less than 56.25 to succeed), the enemy's L9 = 29% | The attacker's current weapon instance `+0x04 & 0x08` ("cutable" bit, from byte 0 of the weapon ROM record), body `+0x20 & 0x01` (equipped with sword), pilot `+0x36 & 0x01`, level `+0x07` is non-0. When successful, press the attacking weapon `+0x22 & 1` to return 0x13 or 0x12 as two results | `801F6D10` |
| **Fake** | Deterministic, no dice roll | Faction is not 0, roster `0x80` set, driver `+0x14 ≠ 0`; after taking effect, this field is −1 | `801F6E3C` |
| **Aura Barrier** | **Threshold Absorption**: Threshold `3000 + 表[主驾驶员圣战士等级]`, **When the defender chooses defense ×2**. Damage ≤ threshold → **Reset to zero**, EN consumption +5; > Threshold → **Pass as is** (result 0xF), after that **No longer determine universal shield and S defense** | Body `+0x28 & 0x4000`; Attacker's weapon is beam shooting; Defender's EN is 5 | `801F6ED0`/`801F6EE0`, `801F7520..801F75C0` |
| **Universal shield** | **Subtractive and superimposable**: `2000·[0x800 行星防御] + 2000·[0x20 I力场] + 1000·[0x200 光束涂层]`, **During defense ×2**; Shield ≥ damage → **Damage 0** (`801F7704`), otherwise `max(伤害 − 护罩, 10)`; In both cases, EN consumption is +5 | The corresponding position of the body `+0x28`; The attacker's weapon is beam shooting; The defender's EN Foot 5 | `801F6F3C`, `801F7668..801F7740` |
| **S Defense** | The probability is the same, and it is also divided according to the defender's camp 16/32 (using driver `+0x08` level / skill position `0x02` / body equipment position `0x02`; regardless of the attacker's weapon); the effect is that the damage is halved and rounded down to a multiple of 10, the minimum 10**, damage < 20 not processed | Same as above | `801F6FDC` |

The clone mask `0x163011` has been checked with the `unit_abilities` "avoidance" family seven items of `config/data/original-jp-v1.json`: clone `0x10`, Mach special `0x1000`, true Mach special `0x2000`, God's clone `0x1`, Getter Phantom `0x20000`, Telescope Foot `0x40000`, Super Jammer `0x100000`, and the union is **exactly** `0x163011`. Aura barrier table `80218930` (ROM `0xab160 + 0x80218930 − 0x801c2600`) has been read from ROM: `0, 200, 400, 600, 800, 1000, 1200, 1300, 1400, 1500`.

A few points worth noting:

- **The clone has nothing to do with level or skill**, it only depends on whether the strength reaches 130.
- **Aura barrier is a cliff effect**: if it is almost not penetrated, it will be completely ineffective, if it is penetrated, it will be fully passed. The pre-battle interface that displays "Add N damage to penetrate" is very valuable.
- **The remaining number of avatars is not displayed in the original game** (see [Basic Repair](base-fixes.md)).
- The shield is evaluated **after the damage is calculated**, so to predict the result of the shield, the damage must be calculated as well.

- **Cut り払い only takes effect on weapons with the "cutable" bit** (Weapon ROM record 0th byte `& 0x08`, `800A6A44` is copied to the instance `+0x04`). Of the total 1,329 weapons, 574 have this bit: 183 for missiles, torpedoes, grenades and other live-fire weapons, and 391 for combat weapons; none have it for beams and machine guns. It's not all about fighting either: 192 pieces of fighting, including the Earth-shattering Fist, Finger of God, and Boxing, can't be cut off.
- **The probability of cutting and S defense is divided according to the defender's camp**: our side `等级/16`, the enemy and the third party `等级/32`. 2026-10-01 Correction: Previously, this table wrote the condition as "weapon id < 0x60". The actual parameter of `801E510C` is the defender's handle; the host pre-war page `src/host/defense_preview.hpp` is always calculated according to the camp, and the optional probe `battle_ui_probe.hpp` is the same as the original function 32/32 consistent([native pre-war page](../native/native-battle-ui.md)).

2026-10-01 Corrected the four conditions for shields (spiritual energy barrier and universal shield). This section had not been written before or was written incorrectly:

| Items | Code Facts | Locations |
| --- | --- | --- |
| Only fires against the beam | If the attacker's weapon instance `+0x04 & 0x02` (weapon ROM byte 0) is not set, the entire section will be skipped. 225 of the total 1329 pieces have this bit, all are shooting, and have no intersection with the "cutable" `0x08`; beam sabers, floating cannons/fin floating cannons, Getter beams, photon force rays, and Aura cannons are not equipped with it | `801F7470` |
| "×2" is a defense command | The incoming "Terrain 2" is actually `+0x10` (`D_8018B6F8`, step size 0x5C) of each item in the combat table; the first item is the command byte `D_8018B754` of §5, value 2 = defense. Item 0 (original attacker) is set to −1 in `801F7B54`, so the original attacker cannot get ×2 during counterattack | `801F6F20`, `801F6FB4` |
| Requires and consumes EN 5 | `EN − 反击武器 EN ≥ 5` is required when the defender chooses to counterattack, otherwise `EN ≥ 5` is required; `D_8018B6FF` (EN consumption) +5 is given for blocking or reducing damage | `801F70DC`, `801F74E8`, `801F7704` |
| Shield ≥ Damage returns to zero | Only "Damage > Shield" will go `max(伤害 − 护罩, 10)`; after the aura barrier is penetrated, the shield segment will end directly and S defense will not enter | `801F7704`, `801F7520..801F75C0` |

Unsolved: The message code remapping of the shield has an unreachable branch; the two results of 0x12/0x13 returned when the cut is successful (according to the attacker's weapon `+0x22 & 1`, this bit is set on the sword combat weapon) are not checked for which performance they correspond to. Neither affects damage arithmetic.

## 5. Three instructions for the defender

The selectors are **signed byte `D_8018B754`**: `-1` unselected, `0` counterattack, `1` avoid, `2` defend.
(`D_8018B74C` is the **counterattack weapon pointer**, 0 means no counterattack, not a command selector.)

`801F84D4``bnez $v1` is shunted, and the delay slot sets `$v0` to 1 as the comparison value:

| Command | Hit Rate | Damage | Counterattack |
| --- | --- | --- | --- |
| **Counterattack** (0) | Original value | Original value | ✓ (`801F69D8` select weapon) |
| **Avoid**(1) | **÷2** | Original value | ✗ |
| **Defense** (2) | Original value | **÷2** | ✗ |

Defense also increases the shield value and the aura barrier threshold by ×2 (§4, supplemented on 2026-10-01).

The avoidance branch (`.L801F86DC`)** only calls `801F4384`**, the defense branch (`.L801F870C`)** only calls `801F5628`** - each does not touch the other function at all. Both set `D_8018B74C` to 0 to cancel counterattack.

`801F7D6C`'s own third parameter `$s7` only appears 6 times in the whole function, and is never passed as a parameter to hit/damage; `a2` of the six call points are all hard-coded literals, and only avoidance/defense branches pass 1.

**AI automatic selection** (`801F7B34`): `slti 0x15` - predicted hit rate **< 21, choose avoidance, otherwise choose defense**; in addition, in `801F849C`, if you will still be shot down after defense (`伤害>>1 ≥ 攻方武器+4`), **change to avoidance**.

Strategy support: The SRW series wiki states that "the hit rate is halved under the avoidance command", which is consistent with the code. There is no record of the specific numerical values ​​of SRW64's defense, so the code shall prevail.

## 6. Spiritual Instructions

The driver's running record `+0x1C` (word) is the spirit effect bitmap, **the spirit id is the bit number** (`bit = 1 << id`, set by `801E0E6C(id, unit)`, always writes the first pilot of the aircraft `+0x38`, so the state spirit cast by the co-pilot also affects the entire aircraft; the tower system body 171–179 Then copy it to two other people). spiritname = text 969+id. The 31 items in `jtbl_8021ED08` are the determination of "can it be cast now", not the cast itself; the casting assignment is `801D6A68(id, 免费)` → tactical status `0x1A + id`.

| id | bit | spirit | effect | reading location |
| ---: | --- | --- | --- | --- |
| 2 | `0x4` | Acceleration | Movement +3 | `801CBA60`, `80201D14` |
| 3 | `0x8` | てかげん | When the target HP ≥ 20 and the attacker's skill (`+0x2C`) is strictly greater than the defender's skill**, the damage will be clamped and the target will have 10 HP; attack, counterattack, and map weapons will all be judged | `801F5B78` (`sltiu HP,0x14`, `sltu 守技量,攻技量`); call `801F875C`/`801F8774`/`801FE330` |
| 4 | `0x10` | Concentration | Attacker's hit +30/Defender's hit −30 (symmetrical) | `801F4584`/`801F45A4` |
| 5 | `0x20` | ひらめき | held by the defender → hit rate** returns 0** (must hit first) | `801F4460` |
| 7 | `0x80` | Must hit | Attacker holds → Hit rate** returns 100**, and skips the clone/cut; **does not skip the clone** | `801F44A0`, `801F7384`/`801F73D8` |
| 9 | `0x200` | Iron Wall | Defender **Armor ×2** | `801F57D8` |
| 10 | `0x400` | みがわり | When the protected ally is the defender, the caster fights instead, and then clears the position; it will not be replaced when the protected ally has ひらめき | `801F7844` (`+0x1C & 0x420 == 0x400`) |
| 11 | `0x800` | Hot blood | Damage ×2 | `801F59CC` |
| 14 | `0x4000` | Luck | Funds ×2 | `801F673C` |
| 16 | `0x10000` | Effort | Experience ×2 | `801F635C` |
| 17 | `0x20000` | Soul | damage |
| 18 | `0x40000` | Gakushen | Enemy weapons cannot target it, and it is not affected by self-destruction | `801F89E4`, `801EFA14` |
| 21 | `0x200000` | Challenge | The provoked enemy AI only targets the caster | `80203F24` |
| 23 | `0x800000` | かくRAN | Added to **each** enemy/third-party unit when cast; when the leader attacks (including counterattack), its own hit rate ÷2 | `801D9F94`, `801F472C` |

2026-10-01 Correction: id 3 was previously written as "Attack HP > Defender", and the address was written as `801F5BB4` in the function; the actual comparison skill is `801F5B78`. There is another branch of the same function that has nothing to do with the spirit: the defender's body `0xB9` (ガイヤー) unconditionally retains 10 HP. id 7 was previously written as "skip the false body", see §4.

**Duration** (`801E0F9C`/`801E1070` clear bits according to mask table):

- Clear after one move: `0x4` acceleration (`D_80218054`, called from `801C2A2C`/`801CCC70`/`801CD28C` at the end of the move, only clear this unit)
- **When the number of rounds is +1, clear all units present in the three camps**: `0x10` Concentration, `0x200` Iron Wall, `0x80` Must hit, `0x800000` Chaos, `0x40000` Gakushen (`D_80218058`; `801FA88C` Add 1 to the number of rounds `D_8010F5EA`, and adjust the upper limit to 250 to `801E1070(0)`). So these effects cast during the player phase are valid throughout the enemy phase. (2026-10-01 Correction: Previously written as "end of round".)
- **After one battle** Clear: `0x800` blood, `0x20000` soul, `0x4000` luck, `0x10000` effort, `0x8` てかげん(`D_8021806C`); normal battle `801FCA78` Clear once for both the offensive and defensive sides. The map weapon `801FE068` only clears the attacking side.
- Not in any mask: `0x20` ひらめき is set to `D_8018B72B[侧]` when triggered, cleared by `801FB460` (normal combat settlement) / `801FE068` (map weapon), and will be kept until triggered; `0x400` みがわり is in `801F7844` is cleared after replacement; `0x200000` Challenge is only cleared when the linked object is removed (`801E11B0`), mounted/integrated/separated command sub-state or resurrection reset (`801F13C4`), there is no round limit

**SP consumption**: u8 × 32 table `D_80217F70` (ROM `0x100AD0`), sorted by id: `1 1 10 10 15 15 20 25 30 30 35 40 40 40 45 50 20 60 60 60 65 35 70 70 70 90 90 100 100 120`, item 31 (id 30) = 1. `801E195C` is deducted from the pilot's `+0x16` (script `3D55` is skipped when casting for free); `801F1B10` is judged to be insufficient by `SP < 消耗`, so the SP can be used even if it is consumed. ID 30 has no name and description text, and is not included in the 148 learning tables. The effect is that the entire driver's strength +30 (`801E1380`: `id==30 ? 30 : 10`). The enemy AI has no autonomous casting path: `801D6A68` only has two callers: the player's mental menu `801D69EC` and the script `3D55` (`80210490`). (Added on 2026-10-01, previously written "the position has not been determined".)

The SP consumption and effect descriptions given in the strategy guide (`srw.wiki.cre.jp`'s Spirit コマンド/64 pages) are consistent with the above table: acceleration 10, concentration 15 (hit avoidance +30%), ひらめき 15 (one complete avoidance), root 20, sure hit 25 (hit 100%), iron wall 30 (armor) 2 times), blood 40 (damage 2 times), fusion 40 (power +10), root 40, soul 60 (damage 3 times).

The `spirits` table (ROM 511920, stride 12, line 148) is not a mental definition table, but an acquisition list for each driver: 6 sets of `(等级, 精神id)`. The levels of all rows 148 are monotonically non-decreasing, and the ids are all in the range 0-29, which is consistent with the jump table id space.

The casting effects of all 30 spirits (target selection, recovery ratio, upper and lower limits of strength, unfolding order of miracles, etc.) are detailed on the strategy information page (Spirit Command tab of `guide/data/zh-Hans/reference.json`); this section only lists the positions that enter the battle calculation.

## 7. Settlement at the beginning of the round, V-MAX, super mode and downfall funds (Supplemented on 2026-10-01)

**Settlement at the beginning of the round** `801FA3DC`: Called by `801FA88C` after the number of rounds +1, traversing 3 camps

| Items | Rules | Locations |
| --- | --- | --- |
| EN reply | EN +5 for each unit (absolute value, not exceeding the upper limit) | `801FA450..801FA460` |
| Land recovery | HP%/EN% by land type (`D_802196D3/D4`) | Same function |
| HP recovery | Ability bit `0x4` → Maximum HP 10%, otherwise `0x8` → 20%; `当前 + 上限/100 × 百分比`, truncated, not exceeding the upper limit | `801FA550..801FA578`, `801FA260` |
| Inside the mothership | Equipped with mid-ship HP and EN +25% each, replenish ammunition; for the first time of each unit (slot flag 0x80 is not set), additionally adjust `801F12B0(机体,10)`: pilot strength −10, lower limit 50 | `801FA5A4..801FA640` |

**V-MAX** (ability bit `0x10000`): `801FF1BC` traverses handle 0x42–0x9B **all camps**, the main driver's power is ≥ 130 and `+0x1C` bit 30 is not set → `801FE9CC(…,1)`: first `800A5254` Recalculate according to the original values, then move power +1, mobility +20, limit +100, and ability level `|= 0x200` (beam coating). **V-MAX Red Power**: Body 278 (ザカール), position 30 set, strength ≥ 140 → `801FEA70`: After recalculation, mobility +2, mobility **+40**, limit **+200**, beam coating, position 31 set; because recalculation first replaces rather than superimposes V-MAX. Both are not released with force, and are only released when the crash processing `801FF63C` → `801FF4E0` is performed.

**Super Mode/Shisui Shisui/Berserker**: Same as `801FF1BC`. characters 0x12 (Eastern Undefeated) any camp; 4, 8, 0xB, 0xC, 0xD (ドモン, アルゴ,サイ・サイシー、ジョルジュ、チボデー) only on our side; 9 (アレンビー) only on the enemy; strength ≥ 130 → `801FEDF4`: Find the current body in the form table `D_80218A34` (line 9 [normal, enhanced]). If it is not found, it will not be activated; if it is found, it will be recalculated and set to 30. Maximum HP +200/EN +50 (the current value is scaled up), body `+0x17..+0x19` (land/sea/space) = A (unchanged), mobility +10, limit +10, the body number is changed to S/H/B form; God Gundam H also gets the ability slot `0x1` (Shadow of God). `801FE96C` Change the non-"-" of the weapon land/sea/yu to A. `801FEB70` Only for the first 6 people: The driver's six items +10, the driver's terrain is all A, and the power of 10 special kills (weapon numbers 0x0F–0x13, 0x1E, 0x35, 0x3E, 0x47, 0x4C) is **rewritten** as ROM base attack power + level bonus (the number of modification stages is not counted): 41–44 +100, 45–48 +200, 49–52 +350, 53–56 +500, 57–60 +700, 61–64 +900, 65–68 +1100, 69–72 +1400, 73–76 +1700, 77–79 +2000, **80 onwards +2500** (`801FEC80..801FED64`). Allenby's Berserker only has the body part. There are also: Beast Fleet Sharo/Liang/Masato/Nin (0xA8–0xAB) and Silver Bell (0x9A) with strength ≥ 120. Only set 30, no value added.

**Downed Fund Bonus** `801F6588`: Funds are available only if the target is shot down (target aircraft `+0x1E`); Attacker's camp 0, roster `+1 & 0x80` is not placed, number of downs (pilot `+0x14`; the same field of the enemy unit is the number of clones, §4) ≥ 20 `资金 × D_80218908[min((击坠−20)/20, 9)] / 10` (Table 11…20, i.e. ×1.1 at 20–39…×2.0 from 200, truncated); then Luck ×2 (any alignment); finally clamped to 65,535 – capped at **per unit downed**. Experience `801F60D4` does not have any branch to read the number of kills.

## 8. The significance of the pre-war interface

All the above quantities are **pure functions in a readable state**. The pre-war interface can be displayed accurately without consuming random numbers - the premise is that **recalculate the formula yourself and do not directly call the judgment function**: `801F6C44` Roll a random number as soon as you enter the door, regardless of whether the target has the ability to evade. Use `80203418` for damage and `80204254` for hits. Both of them do not throw critical hits and do not move RNG.

The original interface only gives hit rate. Information that can be supplemented: expected damage and critical hit damage, critical hit rate (distinguishing friendly/enemy ÷4), clone/cutting/S defense probability, remaining number of clones, difference between shield threshold and penetration, reasons why the weapon is unusable due to insufficient necessary strength, and the currently active spirit.

The interface draft (following the original double-panel layout, battlefield background and color, including combat animation ON/OFF and the results of three commands side by side) can be found in the artifact in the session record; when implementing, the body orientation should reuse the original **vertex mirror group** (`vertex_mode 0` 8 vertices per part, the last 4 are x-inverted mirror groups, selected when drawing `+0x40`), press side Just select the group, there is no need to pre-bake two images.

## Attachment: This article does not cover

- Operation verification of the strength item (the mini-level is ready but not executed)
- Confirm the size/terrain multiplier of the hit formula item by item
- `D_80219444[]` table of function pointers by weapon id (`801F8070`/`801F8618` indirect calls), possibly with additional per-weapon fixes
- Whether random numbers are consumed during the performance and whether the downfall/experience/plot trigger will be missed if the performance is forcibly ended (requires a battle with animation played)

Returns: [Optional Rule Corrections](rule-fixes.md) · [Basic Fixes](base-fixes.md) · [Combat Animations and Customized Units](../data/battle-animation.md) · [Technical Document Index](../README.md)