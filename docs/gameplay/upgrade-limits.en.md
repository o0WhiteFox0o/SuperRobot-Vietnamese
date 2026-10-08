> **Language / Ngôn ngữ:** [English](upgrade-limits.en.md) · [Tiếng Việt](upgrade-limits.vi.md) · [中文](upgrade-limits.md)

# Number of transformation stages and "ugly duckling" upper limit: each stage increment, price, body settings and MOD design

Date: 2026-09-18. Scope: Japanese Rev 0 ROM and static disassembly of this project (`build/recomp/cpu-scan`), extracted body/weapon directory (`assets/original-data/records`). Sections 1 to 6 are static analysis; the first-phase MOD in Section 7 (values ​​are configurable, the upper limit is exceeded to 15, and the transformation screen displays the original upper limit) has been implemented, and the transformation screen was checked with two bounded runs on 2026-09-18 (Section 7.5); the entries that have not yet been confirmed on the actual machine are in Section 8. For how to handle the number of replacement periods, see [Transformation Inheritance Analysis](upgrade-inheritance.md), which will not be repeated in this article.

The "ugly duckling" in this article refers to the upper limit of the SRW64's body modification that varies depending on the machine: strong machines can only be modified to 7 stages, while weak machines and mass-produced machines can be modified to 13 to 15 stages. After full modification, they can overtake the aircraft with a higher starting point.

## 1. Conclusion Summary

| Conclusion | Basis |
| --- | --- |
| The entire "ugly duckling" system is only determined by **one byte per body**: the body ROM records the upper limit of modification of `+0x20` (the original value is 6~15). The five abilities and **each weapon** of the mecha share this upper limit | `800A5330` Write instance `+0x51`; Transformation screen `801CFA78` (five items), `801D1318` (weapon) |
| Each increment is **irrelevant** to the aircraft: one 15-segment curve for each of the five items, shared by the entire aircraft. The machine with a high upper limit can only go further along the same curve | Five accumulation cycles of `800A5254`, table `D_800CA4F0`~`D_800CA570` |
| The price of each segment has nothing to do with the body and upper limit: just look at "which segment this item is now" | Check by segment number within `801CF988``D_801DC36C` and other five tables |
| Weapons are divided into 5 categories according to **modification type** (weapon ROM record `+0x0E`): Types 1 to 4 each have an increment curve and a price list, type 0 cannot be modified (all increments are 0, price is 0) | Cycle search starting from increment `800A55F4``D_800CA590`; price `801D0C7C` by example `+0x15` branch |
| There are **two copies** of the increment table: the resident table is used for recalculation capabilities, and there is also a "preview" table in the overlay of the modification screen. When confirming the modification, the preview value is directly added to the current body. The two original versions have the same value, and changing one of them will cause inconsistency | Add `D_801DC4AC[段数]` to `801CFD1C` and other places; use `D_800CA4F0` for `800A5254` |
| All tables only have 15 segments (the 16th item in the price list is Sentinel 99999), and the scale bar string only has 11 upper limits, ranging from 5 to 15. **Only adjust the upper limit to less than 15, no new data is required**; if it exceeds 15, the host must take over the value, price, preview and scale | Section 3, 5 |
| The upper limit also determines: EW equipment change trigger, fully modified additional weapons, body sales price, and the write upper limit of `3D6C`. When doing "Breaking the Upper Limit", these must be judged according to the **original upper limit** | Section 5 |
| The archive stores each of the five segments and the segment number of each weapon in **4 digits**. The upper limit of 15 is also the upper limit of the archive format; the upper limit byte `+0x51` is not archived and will be recalculated by ROM after reading the file | `80092240` (body), `80092498` (weapon), see Section 4.3 |
| Comparison with Akurasu's modification cost: ν's Fukuro 140,000, Makuzu's Z(JS)'s ロケットパンチ 364,000 It is completely consistent with the model in this article; ウイングゼロ's ツインバスターライフルMAP guide writes 110,000, and the model calculates 140,000, which is inconsistent | Section 3.3 |

## 2. How much does each section improve (Question 1)

### 2.1 Five items of the body

`800A5254(机体实例, 模式)` is the only ability recalculation function in the whole game: the basic value is read back from the body ROM record, and then the increment table is accumulated segment by segment according to the five segment numbers of instance `+0x4C..+0x50`. The 0th item is fixed to 0, and the segment number L is added to the 1st to L items.

| Segment | 1 to 5 segments for each segment | 6 to 15 segments for each segment | Instance field | Resident increment table (ROM) |
| --- | --- | --- | --- | --- |
| HP | +200 | +200 | Max HP `+0x06` | `D_800CA4F0` (`0x54EE0`) |
| EN | +10 | +20 | Maximum EN `+0x0A` | `D_800CA510` (`0x54F00`) |
| Movement | +5 | +10 | `+0x10` | `D_800CA530` (`0x54F20`) |
| Armor | +100 | +150 | `+0x12` | `D_800CA550` (`0x54F40`) |
| Limits | +10 | +20 | `+0x14` | `D_800CA570` (`0x54F60`) |

Cumulative improvement at full level based on the upper limit (the upper limit that appeared in the original version):

| Cap | HP | EN | Mobility | Armor | Limits |
| --- | --- | --- | --- | --- | --- |
| 6 | +1200 | +70 | +35 | +650 | +70 |
| 7 | +1400 | +90 | +45 | +800 | +90 |
| 8 | +1600 | +110 | +55 | +950 | +110 |
| 9 | +1800 | +130 | +65 | +1100 | +130 |
| 10 | +2000 | +150 | +75 | +1250 | +150 |
| 11 | +2200 | +170 | +85 | +1400 | +170 |
| 12 | +2400 | +190 | +95 | +1550 | +190 |
| 13 | +2600 | +210 | +105 | +1700 | +210 |
| 15 | +3000 | +250 | +125 | +2000 | +250 |

The magnitude of the "ugly duckling" is in this table: a unit with a cap of 15 is maxed out, its mobility is +80 more than a unit with a cap of 7, and its armor is +1200.

### 2.2 Weapon Power

The power of the weapon instance (step 0x24, body instance `+0x2C` pieces, `+0x30` pointer) `+0x06` = weapon ROM record `+0x01` × 100 + the sum of the first L items of the increment table, L is the number of segments of the weapon instance `+0x16`. Increment table selects rows by weapon instance `+0x15` (modification type, copied from weapon ROM record `+0x0E` by `800A6A98`), 15 entries per row, table `D_800CA590` (ROM `0x54F80`, 5 rows × 15 entries u16, a 0 at the end).

| Type | Increment for each stage from 1st to 15th stage | Cumulative after 15 stages | Number of original weapons |
| --- | --- | --- | --- |
| 0 | All 0s (cannot be modified, see Section 6.1) | 0 | 102 |
| 1 | 100,100,150,150,200,200,200,200,200,250,250,250,250,250,300 | +3050 | 541 |
| 2 | 100,100,150,150,150,150,200,200,200,200,250,250,250,250,300 | +2900 | 616 |
| 3 | Same as type 2 | +2900 | 3 (120mm キャノンcannon, ミサイルランチャー, スペシャルボロットパンチ) |
| 4 | 100,100,150,150,150,150,150,150,200,200,200,200,200,200,300 | +2600 | 67 (バルカンcannon, airborne machine gun, etc.) |

Type 2 has exactly the same power curve as Type 3, only the price differs (Section 3.2). The cumulative power of the full stage according to the upper limit: upper limit 7 is type 1 +1100/type 2, 3 +1000/type 4 +950; upper limit 9 is +1500/+1400/+1300; upper limit 13 is +2500/+2350/+2100; upper limit 15 is +3050/+2900/+2600.

Type 0 includes: Fusion Techniques (ツインビーム, ダブルゴッドフィンガー, etc.), repair device/supply device, シャッフル Alliance and ゴッドガンダムH His special move, ドモン's パンチ/キック/rush, and a batch of enemy-specific weapons.

## 3. How much money does each segment consume (Question 2)

The price list is remodeling the screen overlay `load_0008F4B0` (ROM `0x8F4B0`, VRAM `801C4500`; ROM offset of the table = VRAM − `0x801C4500` + `0x8F4B0`), 16 u32 per sheet, and the price is taken according to the **current segment number** (the 0th item is 0→1 segment price), item 16 is fixed at 99999. The funds are `D_8010F5F4` (u32); insufficient funds display text 4144 "Funds are enough", and the number of segments has reached the upper limit displays text 4143 "これ上の reformはできません". When the price is 0 or 99999, the five-item interface displays `-----`.

### 3.1 Five items of the body

| Current paragraph → Next paragraph | 0→1 | 1→2 | 2→3 | 3→4 | 4→5 | 5→6 | 6→7 | 7→8 | 8→9 | 9→10 | 10→11 | 11→12 | 12→13 | 13→14 | 14→15 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HP `D_801DC36C` | 2000 | 4000 | 6000 | 8000 | 10000 | 12000 | 14000 | 16000 | 18000 | 20000 | 22000 | 24000 | 26000 | 28000 | 30000 |
| EN `D_801DC3AC` | 1000 | 1500 | 1500 | 2000 | 2000 | 3000 | 3000 | 4000 | 4000 | 5000 | 5000 | 6000 | 6000 | 7000 | 7000 |
| Movement `D_801DC3EC` | 5000 | 8000 | 10000 | 12000 | 15000 | 20000 | 25000 | 30000 | 35000 | 40000 | 45000 | 50000 | 55000 | 60000 | 65000 |
| Armor `D_801DC42C` | 3000 | 5000 | 8000 | 10000 | 15000 | 20000 | 25000 | 30000 | 35000 | 40000 | 45000 | 50000 | 55000 | 60000 | 65000 |
| Limits `D_801DC46C` | Same as EN |

The ROM offsets of the five tables are `0xA731C`, `0xA735C`, `0xA739C`, `0xA73DC`, `0xA741C`.

Total price based on upper limit:

| Cap | HP | EN | Mobility | Armor | Limit | Five Totals |
| --- | --- | --- | --- | --- | --- | --- |
| 6 | 42,000 | 11,000 | 70,000 | 61,000 | 11,000 | 195,000 |
| 7 | 56,000 | 14,000 | 95,000 | 86,000 | 14,000 | 265,000 |
| 9 | 90,000 | 22,000 | 160,000 | 151,000 | 22,000 | 445,000 |
| 11 | 132,000 | 32,000 | 245,000 | 236,000 | 32,000 | 677,000 |
| 13 | 182,000 | 44,000 | 350,000 | 341,000 | 44,000 | 961,000 |
| 15 | 240,000 | 58,000 | 475,000 | 466,000 | 58,000 | 1,297,000 |

### 3.2 Weapons

The price of the weapon also only depends on the type and the current number of stages, and has nothing to do with the upper limit of the machine body. The price of each stage is an arithmetic sequence:

| Type | Price for nth segment (from 0) | Price list (ROM) | Full 7 segments | Full 9 segments | Full 13 segments | Full 15 segments |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 5000 × (n+1) | `D_801DC7BC` (`0xA776C`) | 140,000 | 225,000 | 455,000 | 600,000 |
| 2 | 4000 × (n+1) | `D_801DC77C` (`0xA772C`) | 112,000 | 180,000 | 364,000 | 480,000 |
| 3 | 3000 × (n+1) | `D_801DC73C` (`0xA76EC`) | 84,000 | 135,000 | 273,000 | 360,000 |
| 4 | 2000 × (n+1) | `D_801DC6FC` (`0xA76AC`) | 56,000 | 90,000 | 182,000 | 240,000 |
| 0 | Without looking up the table, the price is 0 | — | — | — | — | — |

### 3.3 Comparison with strategy numbers

The Akurasu “Unit Upgrades” page lists the cumulative cost of three fully upgraded additional weapons:

| Weapons | Strategy | Model of this article | Results |
| --- | --- | --- | --- |
| νガンダム フィンファンネル (upper limit 7, type 1) | 140,000 | 5000 × (1+…+7) = 140,000 | Consistent |
| マジンガーZ(JS) ロケットパンチ (limit 13, type 2) | 364,000 | 4000 × (1+…+13) = 364,000 | Consistent |
| ウイングゼロ ツインバスターライフルMAP (upper limit 7, type 1) | 110,000 | 140,000 | Inconsistent; the cumulative price of any type or upper limit is not equal to 110,000, suspected to be a clerical error in the strategy, to be confirmed on the actual machine |

## 4. Where are the settings for different bodies (Question 3)

### 4.1 Fields and tables

| Settings | Location | Runtime | Description |
| --- | --- | --- | --- |
| Body modification upper limit | Body ROM record `+0x20` (record table ROM `0x71B80` + body number × 36) | Instance `+0x51` | Written when creating a new instance (`800A7100`, `800A8DF0`), rewritten from ROM each time `800A5254` is recalculated |
| Five segments | — | Examples `+0x4C` HP, `+0x4D` EN, `+0x4E` Mobility, `+0x4F` Armor, `+0x50` Limits | Airframe instance table `D_8016A210`, 140 items × 0x54 |
| Weapon modification type | Weapon ROM record `+0x0E` (record table ROM `0x74E90` + weapon number × 16) | Weapon instance `+0x15` | Copied only when creating a weapon instance (`800A6A98`) |
| Weapon segment number | — | Weapon instance `+0x16` | Independent by piece; the upper limit is the `+0x51` of the host machine |
| Five increments (for capacity calculation) | `D_800CA4F0`～`D_800CA570`, ROM starting from `0x54EE0`, 5 × 16 u16 | Resident RDRAM | The 0th item is 0 |
| Five increments (for interface preview and confirmation) | `D_801DC4AC`～`D_801DC52C`, starting from ROM `0xA745C`, 5 × 16 u16 | overlay | nth item = increment of n+1 segment, last item 0 |
| Weapon increment (for power calculation) | `D_800CA590`, ROM `0x54F80` | Resident | Type × 15 items |
| Weapon increment (interface preview) | `D_801DC85C` (type 1), `D_801DC83C` (2), `D_801DC81C` (3), `D_801DC7FC` (4), ROM `0xA780C`／`0xA77EC`／`0xA77CC`／`0xA77AC` | overlay | consistent with the resident table item by item |
| Pentathon and Weapon Prices | Section 3 | overlay | — |
| Scale bar | `D_801DC340` (ROM `0xA72F0`): 11 pointers, press "upper limit − 5" to select a group of text numbers, and then take one according to the current number of segments | overlay | text 4145~4267, such as the 3rd segment of upper limit 7 is "▶▶▶▷▷▷▷"; upper limit 5 and 14 Two gears have strings but no body to use |
| Fully modified additional weapons | `D_801DC87C` (ROM `0xA782C`), 18 items (body, fully modified weapons, unlocked weapons), 999 end | overlay | See Section 5 |
| EW Overlay | `D_801DC6E4` (ROM `0xA7694`), 5 pairs | overlay | See [Transformation Inheritance Analysis](upgrade-inheritance.md) Section 2.1 |
| Enemy segment number | Deployment record `+12` (enhanced index) → `D_800CB5DC` (ROM `0x55FCC`): 0,1,3,5,7,9,11,13,15 | Write five items when deploying, and write the same value for all weapons when creating a new instance | The original version only uses index 0~5 (number of segments 0~9), all of which do not exceed the upper limit of the body |

### 4.2 Original upper limit distribution

363 aircraft records: upper limit: 6 one unit, 7 forty units, 8 five units, 9 fifty-one units, 10 eighteen units, 11 thirty-four units, 12 one unit, 13 twenty-eight units, 15 one hundred and eighty-five units (mostly enemy units). The upper limit is set manually one by one and is not calculated from basic capabilities, but the trend is clear: strong machines are low and weak machines are high. Examples of our commonly used aircraft (the original script uses `3D5A` to register the body and combined form):

| Upper limit | Body |
| --- | --- |
| 6 | ガンダムサンドロック (the only one in the whole list) |
| 7 | νガンダム, mass-produced νガンダムF, W series TV version and EW version (first generation ガンダムサンドロックExcluded: Serotype, ゼロ, デスサイズ series, ヘビーアームズ series, シェンロン/アルトロン series, サンドロック Kai ／カスタム、エピオン）、ゲッター1／ドラゴン／真・ゲッター、ダイターン3、ゴッドマーズ、ドモンBiology |
| 8 | ザンボット3 series (ザンバード, ザンブル, ザンベース, ザンボエース) |
| 9 |ゴッド／シャイニングガンダム, シャッフルAlliance Four Machines, ZZ, mkⅢ, 100 Shiki, フルアーマーHyakushikai, キュベレイmkⅡ, ヤクト・ドーガ, トールギスⅢ, ダンクーガ, グレンダイザーEach form, スペイザー, レイズナー, ニューレイズナー, サーバイン、ビルバイン、ズワウス、アシュクリーフ、ラーズグリーズ|
| 10 | コン・バトラーV and Five Machines, ダンクーガThe four machines (イーグルファイター, ビッグモス, ランドクーガー, ランドライガー) |
| 11 | Zガンダム、スーパーガンダム、ディジェSE-R、メタス开、リ・ガズィ(BWS ), mass production type νガンダムI, GP03, ノイエ・ジール, トールギス, ピースミリオン, グレートマジンガー, mass production type グレート, シュピーゲル, ノーベル, ライジング, ゼーロン、ヴァイローズ、スーパーアースゲイン、スイームルグS、バルディ、ベイブル|
| 12 | マジンガーZ (the only one in the whole list; JS version is 13) |
| 13 | Each mothership (アーガマ, ネェル・アーガマ, ラー・カイラム, アルビオン, アウドムラ, ラビアンローズ、グラン・ガラン、ゴラオン）、ガンダムmkⅡ、マジンガーZ(JS)、ビューナスA、ダブル／ドリル／マリンスペイザー、ジャイアント・ロボ、ブラックウイング、ダンバイン、バストール、グライムカイザル、ガイヤー、トーラス、ノウルーズ、シグルーン|
| 15 |ガンダム、ガンキャノン、ガンタンク、ジェガン、シュツルム・ディアス、ガンダムEz8、Gディフェンサー、ダイアナンA、ボスボロット、ミネルバX、ボチューン、ドール, コスモクラッシャー, Ginlingrobo, エルブルス, シャトル号|

The upper limit within the same combination/transformation family is not necessarily the same: ガンダムmkⅡ 13 and スーパーガンダム 11, ダンクーガ four machines 10 and ダンクーガ9, スペイザー various types 13 and グレンダイザー 9, ガイヤー 13 and ゴッドマーズ 7. Among them, mkⅡ→スーパーガンダム will trigger the number of segments to exceed the limit, see Section 6.3.

### 4.3 Number of segments in the archive

The interrupt archive (`800924D8` is written to the `801C2600` buffer, starting from SRAM `0x10`) does not save the aircraft instance as it is, but is compressed into 16 bytes (`80092240`) one by one: `+0` is the aircraft number <<6 | Number of weapons, `+2` is HP<<4 | EN, `+3` is mobility <<4 | Armor, `+4` is flag (high 2 bits) | limit, `+0xE` is the serial number of the first weapon of the aircraft. 6 bytes per weapon (`80092498`): number, available forms, number of segments <<4 | low 4 bits of flag. The funds are u32 (`800918DC`) within the block `+0x54`.

Therefore, the pentathlon and weapon segment numbers in the archive only have 4 digits, and **15 is the upper limit of the archive format itself**; the upper limit byte `+0x51` and ability values are not saved, and will be recalculated by the segment number after reading the file. This determines the boundaries of the MOD: if the number exceeds 15, the archive format will not be touched, and if the number exceeds 15, another segment number must be saved (Section 7.6). `tools/recomp/gameplay/upgrade_save.py` Use this format to do controlled archive editing (funds, number of paragraphs), for verification only.

## 5. All readers of the upper limit

Read all codes of `+0x51` (or `D_8016A261` + instance offset), divided by purpose:

| Purpose | Location | Rules |
| --- | --- | --- |
| Can the five items be changed | `801CFA78` within `801CF988`; Confirm from `801CFCA4` | Can be changed only when the number of segments < the upper limit; When confirming, first deduct money, add preview increment, and then +1 when < upper limit |
| Five items of price display | `801CF988` starting from `801D0168` | Check the price only when the number of segments < the upper limit, otherwise it will display `-----` |
| Five items of preview and scale | `801C80E0` (`801C8194` takes the scale, `801C8224` takes the preview) | When the number of segments = upper limit, it displays `-----`; scale `D_801DC340[上限−5][段数]` |
| Weapon prices, previews and scales | `801D0C7C` | Number of stages = The upper limit will display "これ上の综合はできません" |
| Weapon confirmation | `801D1100` (`801D1318`, `801D1384`) | Deduction and power are written as preview values; the number of stages < the upper limit is +1; then `801D0AE4` is called when the number of stages **= the upper limit** to unlock additional weapons |
| Fully modified additional weapons | `801D0AE4`, table `D_801DC87C` | When the body number matches the newly modified weapon number, clear bit 2 (unlocked bit) of the target weapon `+0x22`. Example: ν フィンファンネル→フィンファンネルMAP、mkⅡ／スーパーガンダム拡sanバズーカ→MAP、キュベレイmkⅡ ファンネル→MAP、ゼロツインバスターライフルMAP→2MAP, ヘビーアームズ开 ダブルガトリングガン→全弾発shoot MAP, グレートブレストバーン→MAP, マジンガーZ(JS) ロケットパンチ→Big Wheel ロケットパンチ and other 18 items |
| EW Change equipment | `801CF85C` | Five segments**All ≥** Called at the upper limit `800AAD28` Change equipment; do not look at weapons |
| Script `3D6C` | `800ACA1C` (`800ACA74`) | Five items are written as min(N, upper limit), and all weapons are written as the same value |
| Airframe sales price | Sales screen overlay `load_00107BF0` (ROM `0x107BF0`) `801C2600` | Price = base price + 20000 × (number of five stages + number of all weapon stages) ÷ (upper limit × (number of weapons + 5)); basic price list `D_801C3A40` (ROM `0x109030`), there are 12 machine numbers in the table, and 9 types of mass-produced machines are available for sale (ガンキャノン 11000, ガンダム 12000, ガンタンク 10000, ジェガン13000, シュツルム・ディアス 13000, リ・ガズィ(BWS) 15000, Ez8 11000, ドール 10000, etc.); the proportional part is rounded |
| Switch inheritance | `800AAD28`, `800A9A70`, `800AA8C0` | The upper limit is reset by `800A5254` after copying, with no actual impact ([Transformation Inheritance Analysis](upgrade-inheritance.md) Section 5) |
| Whole block backup of instance | `800ACD5C` | Copy together with the upper limit, no judgment is made |

After the weapon modification is successful, `800A5F84` will synchronize the power and segment number to the "twin weapons" on the same body: `232 ↔ 254`ビームサーベル（ガンダムmkⅡ／スーパーガンダム）, `873 ↔ 880` 空剣（ダンクーガ two numbers). After the five transformations are successful, `800A5924` copies the five segments to the existing forms in the combined family and the deformed family, and calls `800A5254` for each form to recalculate.

## 6. Circumstantial evidence and potential problems

### 6.1 Type 0 weapons: Only blocks those with 0 power

The weapon modification list (`801C7254`) only excludes weapons with `+0x22` bit 1 or 2 set (the combined skill has bit 1, bit 2 is not unlocked); before entering the confirmation (`801D0970` of `801D087C`) only weapons with **power 0** are rejected. Therefore:

- Repair devices and supply devices (power 0) only have a prompt sound when clicked and cannot be modified;
- Combination skills such as ツインビーム (position 1) are not in the list at all;
- But Type 0 weapons with power greater than 0 are not blocked. According to the code, the price is 0 when confirmed, the power is written as the preview value 0, and the number of segments +1. The original power will not be restored until the next `800A5254` recalculation.

This type of weapon only appears on our side in the S form of the S-Form H, the four S-forms of the Structural Alliance, and the Bioman. The list filters weapons by "current form machine number", so as long as these machines are in their basic form during preparation, this path will not be available. **This is a potential problem with static inference**, registered as [WATCH05](original-bug-register.md); MOD should explicitly treat type 0 as "non-transformable" when taking over the modification logic.

### 6.2 Revision of the previous document

[Modification Inheritance Analysis](upgrade-inheritance.md) The original text of Section 8.3 is "`D_801DC340[上限−5]` Select the table of the aircraft's gear level, and then take the price according to the weapon category." The actual `D_801DC340` is a scale bar string table. The weapon price is only determined by the modification type and the current number of segments, and has nothing to do with the upper limit of the body; the "weapon category field" is the weapon record `+0x0E`. Items 3 and 4 of Section 7 of this article can also be statically solved by this article: the Skybreaker 873/880 is synchronized by `800A5F84` every time it is modified; the repair device power is 0, and the ツインビーム with combined skills cannot be modified alone, and their absence in the mapping table will not cause actual losses. Three corrections have been made to the original text.

### 6.3 The number of segments of ガンダムmkⅡ → スーパーガンダム exceeds the limit

`800A5924` Two groups of transmissions are hard-coded at the end: source body 56 ガンダムmkⅡ → 61 スーパーガンダム, source body 158 グレンダイザー → 159~161 each form. The upper limit of mkⅡ is 13, and the upper limit of スーパーガンダム is 11, so after mkⅡ is changed to 12 and 13 levels, the number of five levels of スーパーガンダム exceeds its upper limit: the ability is 13 Segment calculation (the increment table is long enough and the values are normal), and the screen cannot be changed. If the scale is read to the string of the next level (upper limit 12) according to `D_801DC340[6][13]`, there will be a misaligned scale on the screen. The limit violation itself can be determined statically; the actual picture of the scale needs to be confirmed by the actual machine. **This shows that the original version has a state of "the number of segments exceeds the upper limit". MODs that exceed the upper limit encounter the same state after turning off the switch, and the handling methods are the same. **

## 7. MOD: Settable values and "Breakthrough of the upper limit" (realized in the first phase)

### 7.1 Usage

The two parts are independent of each other and can be used separately or simultaneously:

| Part | How to open | Scope of action |
| --- | --- | --- |
| Upper limit breakthrough `upgrade-cap-break` | "Difficulty adjustment" of [optional rule](rule-fixes.md), turned off by default. Instant switch of "Options → Gameplay Adjustment" in the game, or `play_native.py --rule-fixes upgrade-cap-break` | Only the modification screen: all units can be changed to segment 15 |
| Upgrade rule file | `play_native.py --upgrade-rules FILE` (specified each time, not memorized); the bottom layer is the environment variable `SRW64_UPGRADE_RULES` | Each increment and price of five items and four categories of weapons, the original upper limit of any machine body, and the modification type of any weapon |

Rule file template:

```sh
.venv/bin/python tools/recomp/gameplay/upgrade_rules.py export my-rules.json --units --weapons
.venv/bin/python tools/recomp/gameplay/upgrade_rules.py check my-rules.json
```

`export` Write out the original value (`--units`/`--weapons` is also attached with the upper limit of all 363 units and the types of 1329 weapons, with names), change the required items, and delete the rest; each section and field can be omitted, and the original version will be used if omitted. Format (schema `srw64.upgrade-rules.v1`):

```json
{
  "schema": "srw64.upgrade-rules.v1",
  "stats": {"hp": {"increments": [15 个], "prices": [15 个]}, "en": ..., "mobility": ..., "armor": ..., "limit": ...},
  "weapon_types": {"1": {"increments": [...], "prices": [...]}, "2": ..., "3": ..., "4": ...},
  "unit_caps": [{"id": 124, "name": "ガンダムサンドロック", "cap": 7}],
  "weapon_type_overrides": [{"id": 19, "type": 2}]
}
```

Verification (Python is the same as the host, bad files are rejected before starting): The curve has exactly 15 items; each segment increments from 0 to 9999 and the sum of the 15 segments does not exceed 30000 (the ability value is u16); price 1 to 99998 (0 and 99999 are the `-----` sentinels of the interface); upper limit 5 to 15 (the scale only has these 11 file); weapon type 0~4; unknown fields will always report an error. `increments[n]` is the increment of segment n+1, and `prices[n]` is the price from segment n to segment n+1.

### 7.2 Two upper limits

| Purpose | Which upper limit to use |
| --- | --- |
| Modification screen: whether it can be changed again, price, preview, scale, "maximum N stages" | **Effective upper limit**: 15 when breakthrough is enabled, otherwise it is the upper limit of the original work |
| EW equipment change, fully modified additional weapons, sale price, `3D6C`, machine replacement inheritance | **Original upper limit** (ROM value, or the value of rule file `unit_caps`) |

`unit_caps` changes the "original upper limit" itself, so it will also change the determination of EW, additional weapons and sales price; the breakthrough only affects the transformation screen.

### 7.3 Implementation

The code is in `src/host/upgrade_rules.hpp`, wrapped in `game_hooks.cpp`, and bound in `generate_cpu.py`'s `NATIVE_HOOKS`.

- **Value**: After reading the rule file, calculate every byte that is different from the ROM (resident increment table, overlay price list and preview table, body record `+0x20`, weapon record `+0x0E`), patch after each ROM copy: resident segment at startup, each read of `8007F704` (overlay Loading after byte verification, airframe and weapon records are read). The game continues to use its own table, and the preview table and the resident table are rewritten simultaneously, so it is confirmed that the value added during the modification is consistent with the value recalculated later in `800A5254`. Weapon instances only copy types when created, and the wrapper for `800A5254` will first refresh `+0x15` according to the rules file. When there is no file, the patch table is empty and no memory is written.
- **Upper limit**: Each of the six routines for modifying the screen includes one layer of scope - `801CF680` (open the screen and print the upper limit), `801CF988` (selection and confirmation of five items), press "Can it be changed", __INL_COD E_213__ (values, previews and scales of five items), press "Display", `801D0C7C`/`801D1100` (preview and confirmation of weapons), press "Selected Weapon", `801CF85C` (EW Judgment) according to the upper limit of the original work. When entering, write the `+0x51` of all present machines to the upper limit of the scope, and write it back when exiting. Only the bytes that are different from the current value are written; `800A5254` will rewrite `+0x51` from ROM, and its packaging will make up for it in the scope. Codes outside the screen will always only see the upper limit of the original work, and `+0x51` will not be entered into the archive (section 4.3).
- **Full modified additional weapons**: `801D1100` calls `800A5F84` after the segment number +1, and then compares "segment number = `+0x51`". The packaging of `800A5F84` adjusts this comparison when the selected weapon belongs to `D_801DC87C`: when the number of stages has just reached the original upper limit, the comparison is made valid (additional weapons are unlocked according to the original timing, and the prompts are as usual), and when the upper limit is reached after the breakthrough, the comparison is not valid (no repeated unlocking).
- **The number of segments that has exceeded the upper limit**: After turning off the breakthrough, the number of segments that was previously changed will be retained. The display scope widens the scale to the existing segment number to avoid taking strings based on the segment number. The weapon scope allows weapons that exceed the limit to see their own segment number. The screen directly prompts "これ上の Modificationはできません", and the money will not be deducted before adding segments like the original comparison. The original version of ガンダムmkⅡ→スーパーガンダム also follows this path (section 6.3), so the scale is no longer misaligned.
- **Sale price**: The result of `801C2600` of `load_00107BF0` is clamped to "base price + 20000", which will never be triggered under the original data.
- **Scale**: When the packaging of `8008C510` (text descriptor) and `8007F704` is within the display scope, the effective upper limit of the current body or the number of existing segments exceeds the upper limit of the original work, the scale text is replaced with a string spelled according to the upper limit of the original work: the original glyph ▶/▷ is used within the upper limit of the original work, and ● (changed) / ☆ (unchanged) is used for the part beyond the upper limit of the original work. When breakthrough is enabled, the full 15 grids are drawn; when breakthrough is not enabled, only the existing segments are drawn.

### 7.4 Testing

- `make recomp-upgrade-rules-test` (added to `recomp-native-check`): Use real ROM to check the original table, scale text number and upper limit, cover rule file verification, byte patch (including partial copy), record coverage, type refresh, upper limit and nesting of each scope, `800A5254` post-fill, two adjustments for additional weapons, sales price clamp, two widths of the scale string.
- `tests/test_upgrade_rules.py`: Python verification is consistent with host constants, hooks are bound, ROM original values ​​​​and distribution, templates are complete, and controlled archive editing.

### 7.5 Real machine verification (2026-09-18, bounded operation, Japanese, Original screen)

Use `tools/recomp/gameplay/upgrade_save.py` to make **controlled editing** on the first episode pass archive (funds 900000; ダイターン3 three forms of HP stages, ダイターンザンバー stages), and take the first 9 of `load-intermission-check.json` Each input file is read and interrupted, and then the screen is modified by key-by-key operation. The run directory itself is not preserved.

| Run | Conditions | What you see on the screen |
| --- | --- | --- |
| `run-on-2` | Breakthrough; ダイターン3 (upper limit 7) HP 7 levels, ザンバー 7 levels | HP 9400 after loading (8000 + 7×200); Screen title "Maximum 15 levels"; HP cost 16000, preview 9400→9600, scale 7 divisions ▶ + 8 divisions ☆. After confirmation, HP 9600, capital 900000→884000, next period cost 18000, scale 7▶ + 1● + 7☆.ザンバー 2300 (1300 + type 2 first 7 segments 1000), cost 32000, preview 2500, after confirmation 2500, funds 852000, next segment 36000, scale 7▶ + 1● + 7☆; weapon table 6 lines per page, with `行 + 6×(页−1)` consistent |
| `run-off-3` | Breakthrough; HP 9 levels, EN 3 levels, ザンバー 9 levels; rule file: HP price 1234, armor +500 per level, スイームルグ upper limit 11→13 (patch 91 bytes) |ダイターン3 title "Maximum 7 Stages", HP displays `-----`, scale 7▶ + 2●, EN scale remains the original 7 grid; press A on HP to prompt "これ上の综合はできません", the funds remain unchanged; armor preview 1800 → 2300, 2300 after confirmation, capital −3000 (original armor price), still 2300 after returning to the list and recalculating; スイームルグ title "Maximum 13th stage", HP cost 1234, 13 squares original glyph scale; ザンバー (9 paragraph) directly prompts "これ上の reformはできません", the fund is always 897000 |

There is no failure record in running the host twice (`report.json` status `native-run-ended-by-control`, exit code 0), and the run report records `rule_fixes` and `upgrade_rules` (file path and summary) respectively. First attempt `run-on-1` mistakenly entered a new game and was discarded.

### 7.6 Restrictions and Phase II

- **Segment 15 is a hard boundary**: table length, tick table and archive format all end at 15. Exceeding 15 requires the host to take over the ability to recalculate, price, preview and scale, and save segments other than 4 digits into the save collection ([Roadmap](../design/mod-roadmap.md) M2's archive protocol), which is not within the scope of one issue.
- Breakthrough is a switch rather than a value: all units can reach 15. If you want "original upper limit + N", just change `allowed_cap()` to read a numerical setting, and a numerical control is required on the interface ([Setting window planning](../native/settings-window.md) has been reserved).
- The rule file is read at startup and cannot be changed during operation; the breakthrough switch can be switched at any time and will take effect the next time you enter the routine of the transformation screen.
- Weapon power is displayed in 4 digits and cost in 5 digits. The interface will be truncated when the rule file sets the value too large. The verification only ensures that it does not overflow u16/u32.

## 8. Items that still need to be confirmed by actual machine

1. The fully modified additional weapons are still unlocked at the upper limit of the original game when the breakthrough is opened, the prompts are normal, and they are not repeated until the 15th stage (the unit test has covered the logic; there is no mecha with additional weapons in the roster of the first episode, and it has not been reached this round).
2. When the breakthrough is turned on, the EW dress-up is still triggered when all five items reach the upper limit of the original work.
3. Can the free transformation path for Type 0 weapons in Section 6.1 be reached in the original process?
4. Sell screen price clamp after breakout.
5. The actual cumulative price of ウイングゼロ ツインバスターライフルMAP (model 140,000, strategy 110,000).

Returns: [Modification Inheritance Analysis](upgrade-inheritance.md) · [Original Bug Registration](original-bug-register.md) · [Optional Rule Correction](rule-fixes.md) · [Built-in MOD Roadmap](../design/mod-roadmap.md) · [Technical Document Index](../README.md)