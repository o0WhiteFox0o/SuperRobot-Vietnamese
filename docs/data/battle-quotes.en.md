> **Language / Ngôn ngữ:** [English](battle-quotes.en.md) · [Tiếng Việt](battle-quotes.vi.md) · [中文](battle-quotes.md)

# Selection list of battle lines: which words should be said when

Date: 2026-09-27. The combat overlay (ROM `0x121560`, starting from code `0x801C2600`) prepares two line slots for each combatant (recording `+0x2C` to say when attacking, `+0x848` to say when being hit/evaded), which are filled in by `func_80222050`. The filling method is divided into two levels. First, check the **conditional line list**, and then draw from the **general line segments** according to the situation. The decoding is implemented in `src/srw64_native/battle_quotes.py`, and the export (`tools/content/export_text.py`) writes the results into `assets/text-export/records.jsonl``context.triggers` for each battle line, and summarizes them by voice into `assets/text-export/battle/triggers.json`; the `# 触发：` comments above each line in the shipping file `content/dialogue/<locale>/battle/` also come from here.

## Voice

The driver looks up the table not by character number but by **voice number**: `D_800CA9C4[人物号] = 声部号` (-1 means no lines). Most of the characters have their own voice; the cloned characters in the plot (Dumbron 273/274, copies of the four members of the Structural Alliance) share the voice with the original character, and ウォン and コンピュータ share the number 9. 257 voices, 160 conditional lines.

## Common line segments (records 5813–14226)

Table `ROM 0x1161C0`, 36 bytes per voice: nine pairs (start offset, number of bars), record number = 5813 + offset. The nine situations are numbered according to the number passed in by the caller:

| Number | Situation | Determination (`func_80222050`) |
| --- | --- | --- |
| 0 | Attack | Our side takes action |
| 1 | Knocked down | Remaining HP after hit is 0 |
| 2 | Seriously injured | Remaining HP less than 30% |
| 3 | Medium damage | Remaining HP 30–90% |
| 4 | Slight injuries | More than 90% HP remaining |
| 5 | Avoidance | Result codes 21, 22; special avoidance such as clones (result codes 6–12) also have a condition code base of 27500, and this situation is still used in the general section |
| 6 | Attack invalid | Result code 2–5 (shield, armor absorption) |
| 7 | Insufficient ammunition/EN | Weapon number -2: Unable to counterattack |
| 8 | Out of range | Weapon number -3: Unable to counterattack |

`func_80222B14` Randomly selects a code within the segment. When the number is 0, if the slot is still empty, fill in 5813 (the first sentence of コウ) as a clue.

## Conditional dialogue list (records 14227–17346)

Index `ROM 0x121150` (one u32 offset per voice), data `ROM 0x20F250 + 偏移`, two u16s per item: condition code, text offset (record number = 14227 + offset), end `0xFFFF`. Condition code 40000/40001 means "continue the previous condition". A group of consecutive items constitute a multi-person conversation that is triggered and displayed in sequence (the speaker of each sentence is determined by the first three characters of the text header). `func_8022245C` Divide the hit items into three priority groups, and only randomly select one item from the highest group:

| Group | Source |
| --- | --- |
| 0 (highest) | Fusion skill dialogue (8000 series) |
| 1 | 2600 series weapon lines, 10000 series situation lines with opponent/co-pilot conditions in the lines, plot marks or co-pilot conditions in the condition table |
| 2 (minimum) | Lines for 900-series weapons, situational lines for riding a specific aircraft, the opponent is female, and the condition table is based on the opponent's mobile phone/pilot |

After getting the second group of lines, the general line will still be drawn again, and it will be rejected with a two-thirds probability (`func_80222B14`: when there are already lines, roll the dice in 1.5 times the number of lines, and replace it only when the number of lines is rolled). Therefore, the 900 series weapon lines (バルカン, ゴッドフィールドダッシュ, etc.) are just "sometimes said".

The meaning of condition code:

| Condition code | Meaning |
| --- | --- |
| 0–90 | A row (c, w) of the condition table `D_80222F20`: c is shown in the table below, w is the weapon (-1 None, 900+weapon number, 2600+weapon number). c When 700–879, the next line is the plot flag check (flag number, value), for example, ドモン's シャイニングフィンガーソード is divided into two groups of "flag 45 = 0" and "= 3" |
| 900 + weapon number | Use this weapon (Group 2) |
| 2600 + weapon number | Use this weapon (Group 1) |
| 5000 | Opponent driver is female (1st place with driver record +4) |
| 8000 + n | Combination skills. Weapon record field 0 1222–1229 corresponds to the base number 8000–8700 (ダブルバーニングファイヤー、ダブルライトニングバスター、ツインビーム、マジンガートルネード、ファイナルダイナミックスペシャル、トリプルマジンガーパンn Detected from the partner table `[主驾驶][搭档]` (`func_80221CF8`/`func_80221ACC`), only effective in combat mode 3 |
| 10000 + 2500·s + k | Situation s (base 10000 shot down, 12500 serious injury, 15000 moderate injury, 17500 slight injury, 20000 attack, 22500 attack invalid, 25000 avoidance, 27500 clone avoidance, 30000 out of ammunition, 32500 Outside the range) plus condition k: k < 400 riding body k; 400–999 same as c in the table below |

The meaning of c (`func_80221F5C`):

| c | meaning |
| --- | --- |
| 0–399 | Phone number |
| 400–699 | Opponent voice number + 400 |
| 700–879 | Value of plot flag (c − 700) (`func_800A496C`, 2 bits per flag) |
| 880–889 | Co-pilot (`func_801C4A08`): 880 チャム, 881 シルキー, 882 ローレンス, 883 アイシャ, 884 甲児, 885ひかる、886 マリア、887 鄄也、888 ジュン、889 ナイーダ |

Weapons are compared according to the 0th field of the weapon record (`ROM 0x119970`, each 14 bytes), so weapons with the same name on different bodies (various バルカンcannons, ロケットパンチ) are regarded as the same one; `desc` of `triggers.json` will list all the names of the same group.

## Lines that cannot be read in the original version

- The condition table reads only `0x1E0` bytes (120 entries) per voice. The tables of デューク (voice 90,448 items), ボス (164,274 items), and Jiafu (165,298 items) exceed the upper limit, and the original version of the next 150 sentences (records 15420–15523, 15925–15953, 16242–16258) will never be displayed; export the tags `unreachable`, the comment reads "exceeded the original reading limit".
- 39 sentences without any table citation: 7343, 8105, 10481–10483, 10702–10731, 14527–14530. Shipping documents are placed in `battle/other.txt`.
- 5799–5812 (`battle.special`) is not in these two tables: main program `800A2890` press `D_800C9A08` when the flagship is shot down Choose one from each of the captains in order (Haruto, Seru, Ere, Dr. Hazuki, Erma, Toro, and Hare).

## Not yet studied in details

- When the belligerent record `+0x8` is `0x14`, the main pilot voice pointed to by `+0x106C` is used instead and the damage proportion is calculated according to its HP field (presumably it is the ship/multiplayer body), which has no effect on the line attribution.
- The two lines (49, 51) in the condition table where c is between 700-879 and w < 900 will use c as the weapon number for comparison according to the code, and it is likely to never hit; it only affects the three sentences of "ゲイル Lieutenant's revenge" by カルラ.
- The semantics of plot markers 45–49 (a certain state of the five members of the Structural Alliance).