> **Language / Ngôn ngữ:** [English](fixed-unit-name.en.md) · [Tiếng Việt](fixed-unit-name.vi.md) · [中文](fixed-unit-name.md)

# The troop name is fixed to the default name (3D5E)

2026-09-27 User-defined: Players are not allowed to change personal names and unit names, and the original page will not be opened (the same applies when selecting the original version in the settings). Therefore, the unit name is always the game's default "March Wind". When displayed, it is changed to "March Wind" according to the reading language. For the character's default name and display replacement, see [Default Name Trilingual Display](default-names.md). Only the unit name is recorded here.

## Behavior

- At the beginning of scenes 33, 46/58, and 62, the choice "それでかまわない／気に入らない" after Amino proposed "マーチウィンド" will no longer appear, just press No. 1 The item continues: The protagonist says "マーチウィンドか...いいんじゃないか", followed by "ブライト". The "気に入らない" branch (the protagonist dislikes the name, アムロ asks what it is called, `3D5E` opens the input of the unit name, the protagonist proposes a new name) is no longer executed.
- If `3D5E` is executed (mini level, debugging script), do nothing: do not switch to mode 6, do not open any page, leave `8010F698` as is, and the script continues immediately.
- The troop name buffer only stores original glyphs. The default name for trilingual registration is `Field::Unit`: `ja` is マーチウィンド, and other languages ​​​​take the `unit_default_name` of the language directory (zh-Hans "March Wind", en "March Wind", consistent with `content/translation/story-terms.json`). In the dialogue, `<G:012C>` (the dialogue file is written as `{HeroMech}`, the name is wrong, it is actually the name of the unit) is displayed according to the language, and the default name trilingual side is connected to the dialogue expansion place. Archives that have been renamed in the old version will appear as they are.
- Only takes effect in game hosts with RT64; CPU-only and fixed-frame diagnostic hosts do not install these two callbacks and maintain the original process.

## Original process (static analysis)

| Address | Function |
| --- | --- |
| Events `001AB86C` (scene 33), `001AC6F0` (62), `001BC304` (46/58) | Opening event `3D44 0,2,<文本>` (window slots 0, 2 items, text 24045/24417/32003, both are "それでかまわない／気に入らない"), after which `3E10` (item 1) branch and `3E11` (item 2) branch; `3D5E` is only in item 24045/24417/32003 2 branches. |
| `8009FA94` | `3D44` processing function, the parameter is the script VM context: `+0x1C` is the PC that exceeds the opcode (three parameters), `+0x26` The first frame is 0 (the first frame is windowed and set to 1), `+0x24` is the busy flag (VM The handler function is called every frame until it is cleared), `+0xC` points to the engine `+0x994`. Release window sprite 0x23, `+0x24=0`, PC+6, `*(+0xC)=0x3DD9+光标` when determined. `3E10`/`3E11` compares this value. |
| `800A1050` | Resident processing of `3D5E`: calls `801C517C` of the world map overlay, followed by `+0x24=0` to complete the command. |
| `load_000A7EC0:801C517C` | `801C58C4=2`, `80080188(6)` switches to mode 6, `80099814(5,1,2)` fades out. |
| `800801A4` → `800CFEC8[模式-1]` | Mode 6 Go to `8008032C`: `80080038` Install ROM `0x1090A0–0x10DA50` to `801C2600` (the same overlay as the protagonist selection and name page), register `801C69B4` → `801C6814(1)`. |
| `801C6814(a0)` | Public initialization; `a0=0` is the name of the new game (state 0, `801C5004`), `a0=1` sets the state `801C6FB0`/`801C7144` to 4 and calls `801C6034`. Each frame task `801C657C` checks the {initialization, each frame} table of `801C6F74` by state. State 4 is `801C6034`/`801C62D8`. |
| `801C6034` | Draw the kana character selection plate; after clearing `801C71E0` in the editing area, fill in the first 7 spaces with the glyph of `801C6F54` (マーチウィンド), and display the character selection table TEXT id of `801C6F64` (the same asマーチウィンド); cursor cell `801C7228`, insertion position `801C721C`. |
| `801C62D8` | Each frame: Call `801C4C40` when A is on the "decision" grid (0x7D). If it is not 0, the pop-up window 0x92, `801C71DC=1`, etc. will be pressed again; if it is 0, `801C70F4=2` will fade out. In other cells, the A key `801C4308` writes a word (stop at the 10th cell after filling the 10th cell), and the B key `801C465C` deletes the current cell and moves left. |
| `801C4C40` | Confirmation: Copy up to 10 glyphs of `801C71E0` into `8010F698` (the space at the end is the glyph 0 and is not copied, the middle word is counted), and no word is returned as 1; then add the 10 half-words of `8010F698` one by one to the 6 of `801C6EC8` Compare reserved names (10 half-words each) - OZ, オズ, スペシャルズ, ホワイトファング, アクシズ, ネオジオン - congruent and return 1; otherwise write after the name `0xFFFF` returns 0. |
| `801C657C` Fade out | `801C70F4==2`: Mode 5 (new game) `801C69D0` Set the first episode, mode 0x1F, `801C5FCC` Write the default unit name (`801C6F54`, 7 characters plus `0xFFFF`) `8010F698`; In other cases (troop name page), switch to mode 0xD and return to the world map. |

- `8010F698` has a total of 12 half-words (`801C5FCC` clears 12). The name can be up to 10 characters plus a terminator; the dialogue uses the glyph `0x12C` to reference it.
- The original bug of reserved name comparison: `801C4C40` does not clear the old content after the name when copying, but compares all 10 half-words. The buffer after the new game is マーチウィンド＋`0xFFFF`, so only reserved names with more than 8 characters (ホワイトファング) will be rejected. Short names such as "OZ" and "アクシズ" can pass. Now players cannot reach this page, leaving it for record.
- There is another `801C3634(801C6F64[i]+0x14D0, i, 0)` in `801C6034`. If you write `801C71E0[i]` according to an irrelevant TEXT id, it will be overwritten by the glyph of `801C6F54`, which will not affect the result.

## Implementation

- `src/host/unit_name.hpp`/`unit_name.cpp`, configured by `host.cpp` after the dialogue directory is loaded (`dialogue::configure`):
- `answer_choice`: In the first frame of `3D44` (`+0x26==0`), two choices with text 24045/24417/32003 are encountered. Write `0x3DD9`, PC+6, `+0x24=0` according to the original path. The original processing function does not run and the window does not open. Called via `srw64_game_hooks.choice_step` by the `resident_func_8009FA94` wrapper of `game_hooks.cpp`.
- `3D5E`: `NATIVE_HOOKS` of `generate_cpu.py` renames `load_000A7EC0_func_801C517C` to `srw64_original_unit_name_command`, and the package is returned directly through `srw64_game_hooks.unit_name_page`. After changing `NATIVE_HOOKS`, you need to manually rerun `generate_cpu.py`.
- `add_default`: Take the name from `unit_default_name` of each language directory and register it into `names::default_names()`; regardless of the name page switch, the dialogue will also be displayed according to language when `SRW64_NATIVE_NAME_ENTRY=0` is set.
- Event log `unit-name-events.jsonl` (debug interface `events unit_name`): `default` (registered name of each language), `choice-answered` (text, item 1), `page-skipped`.

## Verify

- Component test `make recomp-unit-name-test` (`tests/native_unit_name.cpp`, ASan+UBSan): answer item 1 in all three options and complete the command; other options, non-item 2, non-first frame, bad pointer does not move the memory; hooks and event logs; default name registration and display in each language. `make recomp-name-entry-test` Incidentally, the missing test function stub has been added (this target has always failed to connect after adding the name page switch on 2026-09-23).
- `tests/test_unit_name.py`: hook wiring, only configured in the game host and after the dialogue directory, three-language default name; when there is a ROM, check the command bytes and option text selected in three places, `3D5E` is only branched in the second item, the determined path of `8009FA94`, the processing of `3D5E`, and the default name format.
- Actual machine: Mini level `config/recomp/mini-stages/unit-name.json` (replay the selection and two branches of the 33rd scene, and execute `3D5E` separately again, and then the "Ninja" line prints the unit name), check the script `tools/recomp/debug/check_unit_name.py`. **Not yet operational. **

Also: In the [Mini Level](../script/mini-stage.md) section, I previously noted that the pre-filled value is "アーチウィンド". According to the ROM, both tables are "マーチウィンド", which has been corrected.