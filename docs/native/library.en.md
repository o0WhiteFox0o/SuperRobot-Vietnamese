> **Language / Ngôn ngữ:** [English](library.en.md) · [Tiếng Việt](library.vi.md) · [中文](library.md)

# Library

Date: 2026-10-02. Data pages that are not available in the original version: "Library" on the left side of the MOD in the lower right corner of the title screen, which can also be accessed from the "Library·Illustrated Book" on the "General" page of the settings (for a controller that cannot reach the title button). The window follows the frame of the settings window, with a list on the left and details on the right, divided into two pages: "Unit" and "Character".

## Data source

All are read from the player's ROM at runtime (`src/host/library.cpp`), and the original data is not included with the release package; the field basis can be found in [Original Game Data Directory](../data/original-data-catalog.md). The readings on this page have been checked against the loading code:

| Content | Source | Basis |
| --- | --- | --- |
| Unit values | ROM `0x71B80`, 363 items × 0x24 | `800A6E68` copied to runtime: +0 HP, +2 EN, +4 size bits, +5 movement type bits, +6 mobility, +8 mobility, +A armor, +C limits, +E..+11 terrain, +14 repair cost, +18 Equipment (2 = Shield), +1C Special Ability |
| Size/Type/Special Ability Name | Text `0x446+n`; movement icon table `801DC8F0` of ユニット ability overlay, ability table `801DC8FC` (16 items `mask, text`) | Same as `ability_page.cpp`; HP reply Two people share one text, press `801FA544` Top up 10%/20% |
| Body weapons | Weapon list `0x7E210`, only take the entries with the body number in the form slot | `800A68BC`; The list of common forms will not mix weapons of other forms |
| Weapon values | ROM `0x74E90`, 16 bytes | `800A6A18`: +1×100 attack power, +2/+3 range, +4 hit, +5 bullets (FF none), +6 EN, +7 strength, +8 necessary skills, +9..+C terrain, +D critical hit correction; name grid/shoot/P/B/MAP Marked with `upgrade_page::weapon_markers` demolished |
| Character abilities | Character → Ability record `s16[800CA9C4]`, record `0x7A1A0` × 16 | `800A7FBC`: +1..+6 fighting, shooting, avoidance, hit, reaction, skill, +7..+A terrain, +C SP, +F skill slot |
| Second round action level | Ability record +E | `800A6238`: After reaching this level, the driver's +34 (number of actions per round) is 2, otherwise 1; each action on the map reduces +35 by 1 (`801C2AA4`). The co-pilot and goblin are 0, showing "-" |
| Growth | Constant | `800A6238`: Fighting/shooting/reaction/skill +1, avoidance/hit/SP +2 at each level, the same for everyone; upgrade (`801FC470`) is also recalculated from the basic record with `800A7F8C` after level +1. There is no other growth path. The page shows the values ​​for level 1 (white) and level 99 (blue) side by side. G Gundam Fighter (Characters 4, 8, 11, 12, 13, 18) also has six items of `801FEB70` under the special status `0x40000000` +10, and the terrain is all A, excluding illustrations |
| Special skill level | Threshold `0x7B1B0` × 30 | `800A80F0`: L level = the Lth smallest non-zero value among the 9 thresholds; only the highest level is displayed for the levels reached at the same driver level at the same time |
| Mental command | Character → Mental record `s16[800CA6F4]`, record `0x7CFB0` × 12 | Six groups (acquisition level, command); name `969+指令` |
| Spirit consumption | `D_80217F70` (ROM `0x100AD0`), one u8 for each command | Same for everyone: `801E195C` directly deducts the meter value from the caster SP, without correction by the driver (see [Combat Calculation](../gameplay/battle-formulas.md)) |
| Name | Body `527+id`, character `4382+id`/`4743+id` | The protagonist and partner (characters 25–32) use the default name record 487/495, do not read the name buffer filled in the archive |
| Picture | `units` (battle portrait), `portraits` (avatar) of `battle_assets` | Use HD version in HD mode |

## Work grouping

There are two screens in the original title overlay (`load_0010DA50`, ROM `0x10DA50` contained in `801C4500`) that players cannot enter "キャラクターリスト" and "ロボットリスト" (initialization `801C8F1C`/`801C96FC` has no caller, see [Title Menu](native-title-menus.md)), the data and display code are complete, and they are used for grouping the illustrations:

| Table | Location | Format | Original Usage |
| --- | --- | --- | --- |
| Character table | `D_801CB3A0`, ROM `0x1148F0`, 246 entries | `u16 人物, s16 作品, u16 标志` | `801C8AF8` Create table, `801C8D74` Details display full name and work title |
| Body table | `D_801CB964`, ROM `0x114EB4`, 316 entries | `u16 机体, s16 作品, s16 型号` | `801C930C` Create table, `801C9578` Details display model (text `110+型号`, −1 None) and work name |
| Title of work | Text `60+作品` (version with line breaks `85+作品`), 25 works | | Chinese and English translations are in the `series` section of the entry table |
| Duplicate record aliases | Character `D_800C6A08` (ROM `0x513F8`, 33 pairs), body `D_800C6A8C` (ROM `0x5147C`, 22 pairs) | `u16 重复编号, u16 主编号` | Original "seen" judgment `80091574`/`80091670` Use it to return duplicate records to the main record; when the same number appears multiple times, the last pair will take effect, copy |

The original version has no introduction text: the two detail screens only display the above, and there are no paragraphs of character/machine introduction in the ROM text. The original list also determines which ones to display based on the "seen" bitmap (`D_8010F4D0`/`D_8010F520`). The illustrations are not unlocked and all are displayed.

Grouping order: in the table → find the main record by alias → record with the same name in the table → supplementary table of `library.cpp` (walking ドモンEtc., Hakuta system オーラバトラー, Getter fighter, ビッグゴールド, ドラゴノザウルス, and miscellaneous soldiers whose works can be determined from the name of the unit)→ Those that don't work are classified as "others" (AI, ゲリラ, etc.). **Main・ゲッター1/2/3 The original list belongs to オリジナル, and the illustrated book belongs to ゲッターロボ** (user decision). The order of the group is the order in which the works first appeared in the original list (UC Gundam works → G → W → Super Series → Original). Within the group, the order is in the original list, and those outside the list are in ROM order; the details of the machine are plus the model number, and the name of the work is displayed on both pages of details.

## Page

The layout is designed based on the Steam Deck "extra large" interface (1280×800 pixels, 1.48 pixels/dp, approximately 865×540dp): the panel almost fills the window (96%×94%, upper limit 1180×760dp), the title and tab are on the same line, and the list is fixed at 210dp; the picture frame takes the width of the details area 30% (150–220dp, Deck about 164), the terrain is placed under the map; the gold label (upper limit of transformation/second action) is on the right side of the name, and short labels such as the character’s camp follow the full name; the body value is 3 cells per line, the character 7 items plus a "Lv1 → Lv99" legend cell are 4 cells per line, and the love correction is on a separate line; the label after the weapon name is changed to a new line, and long names in the list are automatically abbreviated. The entire page is rebuilt when the interface size or window is changed. The same layout is more relaxed in Mac "standard" size.

The two pages have the same layout: a large square picture on the left (aircraft combat portrait, character avatar), works on the right (aircraft plus model), name (character plus full name), label line, value bar, and terrain; below are their respective sections.

- **Unit**: The gold label is the upper limit of modification (+0x20, levels 6–15, shared by weapons), followed by movement type, size, special abilities, shield, reinforced component slot (+0x19), and repair cost. The six numerical bars are filled with the top 10% of the total (HP 22000, EN 300, mobility 10, mobility 130, armor 2300, limit 380). The weapon table adds "full modification" (changed to the upper limit of attack power) and "type" (modification type I-IV, weapon +0xE; each increment is a row of the resident table `D_800CA590`, and the cost is the four u32 tables in the overlay of the modification screen). The table below lists the total attack power added and the amount of money spent according to the type that appears on the machine. Weapons unlocked by full modification (`D_801DC87C` 18 items, already in the body weapon table, +0xF with unlocked bit 0x04) are marked as "unlocked by full modification", and +0xF 0x02 are marked as "combined skills".
- **Character**: The gold label is the level of the second action, followed by the camp (the third field of the original character table, 1 = appearing as the enemy), co-pilot/goblin (0x80/0x40 with ability record +0; these two types of six abilities and the second action show "-" as on the original ability page, and the spirit points are as usual). Love correction (Table ROM `0x1012B4`) Each partner has a small avatar, marked "two-way" or "one-way": the partner also has a line that refers back to the person, which is considered two-way. The original version has 7 one-way lines (Allenbi → Domon, Lixiu → Cerein, Emmary → Bright, Bicha → Ellu, Ellu → Jidu, Boss → Jun, Boss → Sayaka). The value bar goes from white to level 1 and cyan to level 99. Mental commands are cards (acquisition level, consumption), and special skills are drawn on a scale of levels 1–99.
- Original data not displayed: transfer category (aircraft +0x12, driver +0xB), basic sales price (only 9 mass-produced machines are available for sale, table ROM `0x109030`), which are not displayed according to the user's decision.

## Inclusion rules

- Grouped by works, see above.
- Placeholders with empty names, `???` or pure numbers will not be accepted.
- Subsequent entries with the same name and identical records will be removed (compare the 36-byte record and weapon number of the machine; compare the ability, threshold, and mental record of the character); retain the same name but different values, and add "(2)" and "(3)" starting from the second one in the same work (characters with the same name in different works, such as two "masterpieces", will not be numbered). Current ROM: 353 units and 293 characters.
- Characters without ability records (mapped as −1) only display their avatar and name, with the note "Characters who do not fight".
- Values are base values: do not include modifications, enhanced parts, mental and physical effects. The threshold value of character 284 (our クェス) is read into the spirit table according to the actual reading method of the game, and the page is displayed according to the game.

## Operation

| Input | Function |
| --- | --- |
| ↑↓ / Cross-key up and down (press and hold for burst) | Select an item; press up on the first item to return to the tab |
| ←→ / Left and right cross keys | Jump to the first item of the next work; ← In the middle of a work, return to the first item of this work, and then press to jump to the previous work; On a page tab, cut pages |
| C up/down (Deck right rocker, keyboard default I/K), mouse wheel | Scroll details (press and hold the handle to scroll continuously) |
| Q／E／L1／R1 | Unit ↔ Character |
| Mouse | Click on items, click on tabs, scroll the list and details with the scroll wheel |
| Esc／X／B | Close |

The bottom layer of Library and Battle Appreciation is opaque, and the title is invisible underneath; when any page (Library, MOD, Settings) on the settings window frame is open, `battle_viewer::hold_title` sets the title's two standby counts per frame (`D_801CC390` to 180 frames to open the demo, `D_801CC3A4` to 0x385 The frame returns to the opening plot) is cleared, and the title stays in place, and the demo or opening plot will not be opened at the bottom of the page (actual test on 2026-10-04: Before the revision, the title entered the opening plot in about 55 seconds after opening the Library, and it was still in the main state 2 after 65 seconds).

Each of the two pages will remember the position you selected; switching languages and Original/HD will rebuild the page. Details following the selection are updated locally using `SetInnerRML`, without rebuilding the entire window. Debugging interface: `ui.click --id library-open`, `lib-tab:0|1`, `lib-item:N`.

## code

- `src/host/library.{hpp,cpp}`: ROM parsing and deduplication, caching by reading language, window thread call.
- `src/native/ui/frontend.cpp`: Title corner button (`home_sync`), setting general page entry, `library_panel`/`library_select`/`library_move`; hung on `settings_open` of the settings window, so the input takeover is the same as the MOD manager.
- Entry: `library_*` of `content/locales/*.json`, registered `UI_KEYS`.