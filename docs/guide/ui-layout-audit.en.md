> **Language / Ngôn ngữ:** [English](ui-layout-audit.en.md) · [Tiếng Việt](ui-layout-audit.vi.md) · [中文](ui-layout-audit.md)

# Interface layout offline audit

Date: 2026-09-29. Without starting the game or reading the ROM and running it, you can also check whether the text in the shared interface (inter-game screen drawn by `src/native/ui/frontend.cpp`, pre-battle confirmation, title menu, settings window, linkage page) exceeds the frame and the frame line extends out of the frame in each language and each window size.

```bash
.venv/bin/python tools/recomp/ui_audit/run_audit.py                 # 四种尺寸 × 三种语言，约 3 分钟
.venv/bin/python tools/recomp/ui_audit/run_audit.py --sizes deck --only 'zh-Hans$'
```

Prerequisite: There has been a graphics host build (`build/recomp/gfx-build`, use its compilation parameters and RmlUi, RT64, plume static libraries) and fonts in `build/fonts`, and there is `rom.z64` (read-only text table) locally. When running, a small window will be opened to draw the page, the archive will not be touched, and the host will not be started, so there will be no conflict with the hosts of other sessions.

## Practice

- [`layout_audit.cpp`](../../tools/recomp/ui_audit/layout_audit.cpp) links the real `frontend.cpp`, language directory and RmlUi renderer; the page adapter (`battle_page::state()`, etc.), settings and controller status on the game side are replaced with avatars, and the page status in the fixture is returned directly. After each fixture typeset a few frames, take a screenshot, and then traverse the elements:
- `text-past-box`/`text-past-item`: Text without line wrapping exceeds the block or inline block or flexible item.
- `run-wider-than-block`: In text that will wrap, the section between two spaces is wider than the block. RmlUi only breaks lines at spaces, and long Chinese and Japanese sentences are overflowed (see [RmlUi breaks lines in Chinese and Japanese](../native/settings-window.md)).
- `box-past-parent`: A bordered box extends beyond the border of the parent element, for example, the divider is longer than the outer frame.
- `text-clipped`/`text-cut-below`: A line of text exceeds the right edge of the panel where it is cut, or more than half falls outside the lower edge of the panel (this line is equivalent to being lost).
- `text-overlap`: Two absolutely positioned grids in the same panel press each other. The grid width of the original 320×240 page follows the text, and it will not overflow, but will only hit the adjacent grid. Lines that have been horizontally compressed (`transform`), and numbers placed grid by grid on the high-definition original pre-war page according to the original number pool are not included in the comparison; the words in the absolute positioning box with a background color (combat appreciation selection box `#vw-pop`) covered on the page are only compared with the words in the box.
- `nowrap` The size of the text as it is when typesetting: consecutive spaces count as one (the key prompt "Select · ..." will increase the original size by 36 dp). A list that only scrolls vertically (`overflow-y:auto`) is also considered a cropping panel, and rolling out half of the lines does not count words outside the list.
- Differences less than 1.2 dp will be treated as rounding errors and will not be reported; overlaps within 3 dp will not be reported if the outer edges of the glyphs collide.
- [`run_audit.py`](../../tools/recomp/ui_audit/run_audit.py) Compile using the parameters of the `frontend.cpp` compilation command in the host build. Recompile only after the source file or header file is updated. The fixture comes from [`states.json`](../../tools/recomp/ui_audit/states.json): 9-23 inter-field page inspection, 9-24 title menu inspection, 9-28 pre-war confirmation inspection and recorded page status (the image path has been removed, which does not affect text layout). Each string is returned to the record number through the ROM text table, and then changed into Chinese, English, and Japanese characters; when the modified screen and track list are not recorded, they are spelled out according to the fields of `upgrade_page.cpp` and `title_page.cpp`. Plus the worst case scenario: the 7 widest aircraft names, pilot names, weapon list names, level names, 4-digit and 5-digit damage, and 99999 HP measured in actual fonts.
- Combat Appreciation: With the fixture `clicks` (press the id point control, the same path as the `srw64_click` of the debugging interface), open the entire page from the Settings "General" page `viewer-open`, and then click on each box of the airframe, pilot, weapon, counterattack weapon, both sides' results, scene, and BGM. The illustrated data (`library::contents()`) is spelled out from `run_audit.py` according to the fields of `library.cpp`: for aircraft 0 (`battle_viewer_pilots.inc` has the largest number of passengers, 13 people), for aircraft 28, the name, model, work name, skills, and weapon names are all the widest; the tracks are taken from ROM records 232–280. Scene thumbnails and avatars are not drawn (the avatar returns empty).
- Size: `deck` 1280×800 points, interface size "extra large" (Steam Deck default, also the basis for determining font size); `deck-standard` the same as the window "standard"; `wide` 1920×1080; `smallest` 960×720; `deck-4:3` the same `deck` but the screen ratio is 4:3 (the page is only typeset in the 1067×800 screen, directory name `deck-4x3`). Screenshot and `audit.json` in `build/recomp/ui-audit/<尺寸>/`.
- Exit code 1 when there is a problem.
- Abbreviation report: `fit` class will record the original font size (`data-fit-from`) on the element when it reduces the text that cannot fit. The audit will write each abbreviated element together with the original font size, current font size, proportion and text into `shrunk` of `audit.json`, and `run_audit.py` will list the items below in ascending order of proportion. Those of `--shrunk` (default 0.85). Reducing the characters is not considered a failure - `fit` is used for reduction - but the most severely reduced lines indicate where the font size is set to be larger and which column is set to be narrower. Look at it before changing the font size. `--shrunk 1` lists all, `--shrunk 0` does not.

## Original screen text overlay

The aircraft abilities, pilot abilities, weapon list, command menu, etc. of the tactical map are the original screens, and the text is covered by [`ui_text.cpp`](../../src/host/ui_text.cpp) ([Original interface text overlay](../native/native-ui-text.md)). Its row width rules are certain, so [`overlay_fit.py`](../../tools/recomp/ui_audit/overlay_fit.py) can judge all data texts (records 0–5643) offline:

```bash
.venv/bin/python tools/recomp/ui_audit/overlay_fit.py                # 中英日；中文有「一定放不下」时退出码 1
```

- The original width is calculated according to the ROM font format: code 0 and 0x13B and below are 8 narrow, and the rest are 14 wide. The original width can be used for translation, and up to 1.35 times + 4 is used when there is nothing behind it; first narrow it (70% for Chinese and Japanese, 80% for English), and then reduce it to 1.5 points at most.
- `overflows`: It cannot be placed even if the back is empty; `depends`: It can be placed only when it is not followed by anything else.
- Lines containing more than two consecutive spaces (to leave space for numbers) can be placed paragraph by paragraph, or the numbers can be placed after moving them into the entire sentence, which is consistent with the approach of `ui_text`.
- Japanese is the control group: the ROM text displayed as it is must fit according to the rules, and the result is 0.
- We only know the width of each record, not what follows the same line; the entry of `depends` depends on the specific screen.

## Not covered

- The dialogue box, bottom bar (`dialogue_scene.cpp`), and HUD badge are not found in RmlUi and cannot be found here; they are checked with the actual machine (`check_dialogue.py`, `check_ui_text.py`). The original picture overlay can only be judged by records, see the previous section.
- The name page takes its own probe (`srw64-ui-probe`).
- Only check for overflow in the horizontal direction; the inline box is slightly higher than the row height (16-unit list row) is very common and cannot be seen, so it is not reported.
- The fixture is the recorded state plus the worst case, not the entire game state; for new pages or new fields, the state must be added to `states.json` or spelled out in `run_audit.py`.

## 2026-09-29 Repaired in the first audit

Two runs after the deck video check (now 159 pages × 4 sizes, plus overlay check) found and trimmed:

| Page | Question | Change the law |
| --- | --- | --- |
| Confirmation before the war (new version) | Press "100 / 100" on the right side of the pilot panel to hold down "SP" | The two grids of strength and SP are divided into widths according to content, leaving a 6 dp spacing within the grid |
| Pre-battle confirmation (new version) | 4-digit damage (such as 2390) exceeds the middle half column by 11 dp, and is crowded together with arrows and "enemy first mover" | 4-digit and 5-digit numbers reduce the font size by digits |
| Pre-war confirmation (new version, high-definition original version) | English and Japanese long machine name, weapon name, and defense condition lines are truncated | Universal `fit` class: After typesetting, the excess text is reduced proportionally, up to 60% |
| Weapon modification, weapon performance | Long weapon names are truncated by the column width, along with the P/B/MAP icon behind | The name is limited to the width left by the icon, and is reduced by `fit` (up to 50%) |
| Each list page between fields | The dividing line of the "Elf" and "Pilot" rows at the bottom is about 2.5 original pixels longer than the outer frame | This row is changed to `box-sizing:border-box` |
| Title "Options" | "Stereo" exceeds the value column by 7 dp | The name and value should be font sizes according to their own column widths |
| 320×240 pages between fields | English and Japanese long names and labels are truncated | The `span()` cells of these pages all have `fit` |
| Body abilities (between fields) | Special abilities are placed in one line and can only be arranged in two lines. The third one of this type of mecha with three abilities (transformation, clone, and Aura barrier) was cut off | According to the original version, it is arranged horizontally from (25,188) and cannot be placed in the next line; when there are more than two lines, the entire column font size and line height are reduced together |
| Body ability (between fields) | English movement type is written as "LndAirSea" | English is separated by "/", and the column is reduced by `fit` |
| Pilot ability (inter-field) | The English skill "Holy Warrior L3" and the Japanese spirit "ひらめき" are cut off from the panel; the Japanese "レベル" suppresses the level | The spirit and skill grids are given width according to the original grid (the last column of the spirit is only 36), and the label width is limited, both with `fit` |
| Explanation of counterattack command (original screen) | Split one sentence into three records. In Chinese, put "avoid or defend," into the paragraph that was originally only "檒し" wide. The same is true in English | Redistribute three paragraphs: "Avoid or defend when the enemy's level is lower than yourself," "Otherwise" and "Counterattack." |
| Terrain name (original screen) | "Baruch Fortress" cannot fit "バルジ" in the grid | The terrain name is "Baruch" ("Baruch Fortress" in the lines remains unchanged) |

`fit` is processed uniformly in `document()` of `frontend.cpp` (`fit_lines`): elements that are not wide enough after typesetting will be proportionally reduced in size and viewed again in the flexible row; elements can use `data-fit-min` to set their own lower limit.

## 2026-09-30 Adjusted according to abbreviation report

Looking at the abbreviation report based on Deck (1280×800, extra large), the situation of machine names and weapon names: Chinese maintains at least 88% of the original font size on all pages (the narrowest is "Double Burning Flame (mass-produced Great Demon)" in the weapon list), English is the narrowest 75% (weapon list "Focused Charged Particle Cannon", pilot list "Byston Well Soldier"), Japanese font Kana is full width and ROM The kana is half-width, and the 21-character "ダブルバーニングファイヤー (マジンガー)" in the weapon list is only 57% (lower limit 50%), which has not been processed yet. Changed:

| Page | Question | Change the law |
| --- | --- | --- |
| Each list page between fields (transfers, abilities, enhanced parts, modifications, archives) | The name is shortened to just fill its own column and is connected to the right column: "Byston Well Soldier Wing Gundam (bird form)" "Byston Well SoldierHP" | The name box without class gives up 4 units to the right margin (`span()`), `fit` is reduced according to the remaining width; the label box and the right-aligned number box remain unchanged |
| Pre-battle confirmation (new version) | The 5-digit damage on the Deck is only 31 dp, the 4-digit 38 dp, leaving 22 dp on both sides of the middle column empty | The left and right inner margins of the narrow version (<1000 dp) of the damage box are 22→14 dp, the 5-digit 36 dp, the 4-digit 42 dp; the wide version 5-digit 36→42 dp; the numbers also have `fit`, if the number width of the font is different, it will only shrink but not overflow |
| All 320×240 pages in the field (menu, transformation, enhanced parts, transfers, archives, abilities) | Screenshot of user viewing transfer list: the base font size is too large | The entire family has been reduced by one size: list rows and in-line labels are unified `face`=10.5 units (original 11.5, labels can still reach 12.5), and other panels 12→11, 11.5→10.5, 11→10, `fit` The upper limit is 12.5→11.5; the weapon list and ability bar are originally 10.5 unchanged |

## 2026-10-04 The battle appreciation page has been audited.

`frontend.cpp` The newly used host functions (combat appreciation, picture book, MOD switching, line overwriting directory, title waiting) have been replaced in `layout_audit.cpp`, and the audit can be linked again; 27 battle appreciation fixtures (9 screens × 3 languages) have been added, and now 204 pages × 4 sizes have all been passed. By the way, I fixed two false positives in my audit (see the space and scrolling list in "How to do").

Revised (same day): `viewer_sync` and the illustration page were adjusted again to `fit_lines` after `document()`. Originally, the second pass calculated the 60% lower limit from the reduced font size (about 36% at worst). `data-fit-from` was also changed to the reduced font size, and the abbreviation report would be underestimated. Now `fit_lines` has `data-fit-from`, so the calculation starts from it, and the lower limit is relative to it; the redundant call to `viewer_sync` is deleted (after `document()`, only the background color of `.modal` is changed, which does not affect the typesetting; the illustration page needs to be retained, and the details area is redrawn). Side effects: The first line of the English/Japanese pilot box on the Deck, "Byston Well Soldier", was originally shrunk to 6.7 dp (52%) and just dropped, but now it stops at 13 → 7.8 dp (60%). The line with the "Now" badge still overflows 9.0 / 4.6 dp, and the audit reported two text-clipped places. 10-07 Changed to give way to subtitles: the name of the list row (`.n`) and the subtitle (`.s`, pilot's skills) are both narrowed in proportion to the natural width, and both have `fit`. The name of this row on the Deck is 83%, the skill is 79%, and there are 0 problems in each size.
