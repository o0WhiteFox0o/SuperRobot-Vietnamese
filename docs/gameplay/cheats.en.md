> **Language / Ngôn ngữ:** [English](cheats.en.md) · [Tiếng Việt](cheats.vi.md) · [中文](cheats.md)

# goldenfinger

Date: 2026-10-05. The "Cheating" page of the settings window (after "Rules") is all closed by default; the pilot level row is closed by default. Click "Expand" to list the pilots. The content is six items defined by the user. All are implemented by themselves according to the fields and upper limits in the original code. The GameShark code is not read, and RetroArch's `.cht` is not imported. Codes: `src/host/cheats.hpp` (fields, upper limits and writing rules for each frame), `src/host/cheats.cpp` (hook, pilot list, changing level), the interface is in `cheats_page` of `frontend.cpp` (the expanded state is not saved, and the settings are collapsed each time it is opened), and the switch is saved with `cheats` of `presentation-settings.json`.

## 1. Why not use libretro code?

There are only 7 `cht/Nintendo - Nintendo 64/Super Robot Taisen 64 (Japan).cht` of libretro-database, and none of them can take effect according to the name when checked according to the code (mupen64plus's `mupencheat.txt` does not have this one):

| entry | code | actual |
| --- | --- | --- |
| Enable Code | `F10C0FE0 2400` | Change the resident code segment (`80076610`–`800C34B0`); the changed instructions are invalid after recompiling. The original machine was tested by GameShark |
| Two Activators | `D00F97B0`／`D00F97B1`／`D10F97B0` | Just the condition of "when a key is pressed" (`800F97B0` is `OSContPad`), opening it alone will do nothing |
| Money | `8110F5F6 0000` | Fund `8010F5F4` is u32 (only lw/sw in the whole process). This clears the lower half word and reduces the money |
| Life | `8116A214 00A0`+`8116A268 0000` | The body instance +4 is the current HP (`800A55D0` is filled by +6): Slot 0 HP is set to 160, slot 1 is set to 0 |
| Energy | `811613F2 00A0`+`811613FA 0000` | Fall into the number wizard pool `801613E0` (20 × 8 bytes), only change the displayed number |

## 2. Six items

| Item | What to write | Basis |
| --- | --- | --- |
| Maximum funds | `8010F5F4` = 99,999,999 per frame | There is no upper limit for the ways to add money (`3D5B``800A0D24`, kill income `801FC5E8`, fund props `801D5CE0`, sale); all funds are displayed as `%8d`. Deduction at the end of the level `8020DA98` Judging by the sign, the funds cannot reach 0x80000000, 99,999,999 is far away |
| All 9 enhanced parts | Write the number of 18 types of parts (`8015E990`, each u16: high byte held, low byte equipped) in each frame as max(9, in equipment) | Number of types 0x12 (`800A8BC8`); drops only when held + to be accounted + dropped in this field < 9 When recorded (`801F88C0`), the holding number of the part screen is only one bit wide (`801CBEB4`). The original version will no longer drop parts after it is full. `8015E9B4` is the threshold for financial props, do not touch it |
| Our EN is not reduced | Write +8 = +0xA to our body pool (`8016A210`, 140 × 0x54, +0 ≠ 0) every frame | Weapon EN is directly deducted from the instance +8 (`801FC8D8`), no copy; unconditionally full instead of "make up for less", because the refund of canceled movement (`801CC1F0`) and frame-by-frame recovery animation will briefly exceed the upper limit |
| SP does not decrease | Write +0x16 = +0x18 to our driver's table (`80172F40`, 100 × 0x4C, +0 ≠ 0) every frame | The mental consumption is only directly deducted at `801E195C` +0x16 |
| Power 150 | Write +0x20 = 150 in the same table, skip the driver with the upper two bits of +4 (0xC0) set | 150 is the constant upper limit of all power paths (`801FAD58`, `801E1460`), there is no distinction based on people; `801F12D0` vs. 0xC0 The pilot in position does not reset or lose strength. The meaning is unclear and is still skipped |
| Pilot rating | See §3 | |

The writing of each frame is done in the frame boundary hook `80085F30` (`srw64_game_hooks.cheats_frame`). Turning off the switch will no longer write, and the values that have been written will remain unchanged.

Side effects: When the strength is fixed at 150, the spirit "can only be used if the strength is less than 150" (such as Jihe, `801EFEA4` area, to be verified) will become gray. The effects of Super Mode, Mirror Shisui, V-MAX, and Clone with power starting from 130 will always be valid.

## 3. Change pilot level

- **Level is derived from experience**: +0x12 is the accumulated experience (u16), level = min(experience / 500 + 1, 99) (`800A630C`), and the upper limit of experience is 49,000 (`801FC0E4`). Each person's archive only saves the character number, experience, kills and body slot (`800923B4`), which will be rebuilt based on experience when loading the file (`800A8E0C` → `800A7F8C(record, 1)`). So if you only write +5 but not experience, loading the file will return you to the original level.
- **Original writing method** (`800AC220`, new joiners make up for the base level): +5 = L, +0x12 = (L − 1) × 500 (`800AC340`–`800AC368`), then `800A7F8C(record, 1)`. The host does as he is told.
- **`800A7F8C` is a complete set of recalculation**: rewrite six abilities, terrain, SP upper limit, skill slots from the basic record (`D_800CA9C4[人物]` → ROM `0x7A1A0`), and then add (L − 1) level fixed growth to `800A6238` (fighting, shooting, reaction, skill +1 each, avoidance, hit, SP upper limit each +2), the spirit is refilled according to the acquisition level +0x0A/+0x0B (`800A63E0`), the skill level is refilled according to the threshold +6/+7/+8 (`800A6340`), and the second action level is written +0x34. When a1 = 1, SP and the number of actions in this round are filled up, which is the same as loading. The same is true for downgrading.
- **Only done in the interfield menu**: The request is queued first, before each step of the interfield menu (`801CE19C` wrapper, `srw64_game_hooks.cheats_intermission`), and executed after the screen fade-in ends (`8015E9C5` = −1). When the game is not between games, the page says "You can only modify the level after returning to the game menu", but the button does not appear.
- **Who to list**: Same as the original pilot list `801C549C`, our table has +0 ≠ 0 and there is no 0x80 bit record; the name is the text `0x111E + 人物号`.
- **G Gundam Fighter's super mode bonus** (`801FEB70`, in the tactical overlay) will be washed away by recalculation, and will be added immediately after the original version is upgraded after the war; it will also not be available when loading files, and will be restored according to the original rules after entering the map. Changing levels between games is consistent with loading files.
- Changing the level will affect the enemy level benchmark for subsequent levels (`D_8010F5F3`, when entering the tactical map, take the average of the top 15 pilots on our side, `800A4BE0`).

## 4. Archive and switch

- Funds, parts, and levels are written about the game's own status, and are saved together when the player saves the game. User-defined: **The use of cheats will not be recorded in the archive**.
- The switch is saved in `cheats` of `presentation-settings.json` (id list: `funds`, `parts`, `en`, `sp`, `morale`) and will be used at the next startup. Debug runs can use the environment variable `SRW64_CHEATS=funds,en` instead of the saved list.
- Events are recorded in `cheat-events.jsonl` in the running directory (before and after switch changes and level changes).

## 5. Verification

- Static: The above addresses and upper limits are all from disassembly (two rounds of static verification, 2026-10-05).
- Unit: `make recomp-cheats-test` (`tests/native_cheats.cpp`) Check each frame writing rules and level/experience conversion.
- Actual machine (2026-10-05, `tools/recomp/debug/check_cheats.py`, running `build/recomp/debug/20261005T064406.061075Z`, all 12 items passed): The first episode of the game is read into the game, and the "Rules" page is set (the current location) to list 4 pilots; Manami 2 → Level 12: 5,500 experience, six abilities +1/+1/+2/+2/+1/+1 At each level, SP upper limit +20 and replenished, spirit 1 → 4, and then dropped back to level 2 to be consistent with the original value; after the five switches are turned on, the fund is 99,999,999, and 18 types of parts hold 9; manually change EN, SP to low, and strength to 100, and return to the upper limit/150 in the next frame; after saving in column 2, the archive list shows level 12, funds 99,999,999 (the list is based on saved experience levels).
- Changed to a separate "cheating" page, closed the pilot level by default and then re-run (run `build/recomp/debug/20261005T065348.468538Z`, all 13 items passed, and there is an additional item of "no pilot row when opening the page").
- There is no actual combat: the consumption of EN and SP in battle has only been statically confirmed (directly deducted from the instance, there is no copy), and "150 strength makes the combination gray" has not been seen in actual combat.