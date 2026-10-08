> **Language / Ngôn ngữ:** [English](touch-controls.en.md) · [Tiếng Việt](touch-controls.vi.md) · [中文](touch-controls.md)

# Mobile phone touch screen operation (designed according to the scene)

2026-10-03. How to operate an Android phone without a controller. The previous version was a fixed virtual controller (`src/host/touch_pad.hpp`, main 1c55cd9), and all screens showed the same set of N64 keys. This version displays buttons with function names according to scenes. The keys are still N64 keys and host keys at the bottom level, so there is no need to change the game, our page, or key prompts.

## 1. User-set goals

- **Like MOBA mobile games:** There are no fixed direction keys on the left side. Wherever you press your finger on the left area, the center of the direction key will be where you want it, just drag it.
- **Minimize the number of buttons:** Each scene only displays the buttons used in this scene.
- **Display function name:** The buttons write "OK", "Fast Forward" and "Next Unit" instead of A, R2, R1. Text and game languages ​​(Chinese, Japanese, English).
- **Not split:** Our own pages (pre-war confirmation, preparation, etc.) should at least retain the direction, "OK" and "Return". We cannot just enter the page and only have middle clicks.

## 2. Layout skeleton

All scenes share the same skeleton, and the scene only determines what is placed in each slot and whether it is displayed or not. The position is fixed, but the words will change.

| Slot | Location | Dimensions | Purpose |
| --- | --- | --- | --- |
| Orientation area | Game screen: The entire left side about 42% wide, below the top edge bar. Our page: lower left corner approximately 34 mm square | rocker appears where pressed, radius approximately 10 mm, dead zone 2.5 mm | four directions. When not touching, a light joystick is displayed in the lower left corner, indicating that it is available |
| Main key | Lower right corner, center 12 mm from the right and 14 mm from the bottom | Diameter about 16 mm | "Confirm" action in this scene |
| Secondary key 1 | To the left of the main key, 180° on the arc | About 11 mm in diameter | "Return" actions, always here |
| Sub-keys 2, 3 | Main key upper left 135°, straight up 90° | Diameter about 9 mm | Two common actions in this scene (previous/next, fast forward, etc.) |
| Small keys on the top | One bar on the top, two spaces on the upper left and two spaces on the upper right | About 12×5.5 mm | Uncommonly used actions; the first space on the upper left is always "Settings" |
| Click screen | Screens other than direction area and buttons | Full screen | Only valid in dialogue and any key window, equal to primary key |

Rules:

- The slots that are not displayed do not occupy the touch area. When your finger falls there, it is the "click screen" or direction area.
- In the same scene, an action only appears once.
- The feel of the button follows the existing implementation: press with multiple fingers at the same time; drag the finger in the direction area to change direction; slide from one button to another to switch; click and hold for at least 80 ms.
- The whole set is hidden when using a physical controller or keyboard; it appears when you touch the screen.

## 3. Scene table

The "Identification" column is the basis used by the host to judge the scene. The addresses are all in RDRAM and are read out by the game thread every frame and published to the interface thread (Section 4). The "N64" column is the key that the button actually emits.

| Scene | Recognition | Direction | Primary key | Secondary key 1 | Secondary key 2, 3 | Top edge | Click screen |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Boot logo, opening demo, PRESS START | Mode `8015DA02` = 1, 7, `title_major` is not 3 | None | Start (START) | None | None | Settings | Start |
| Title ring menu | `title_major` = 3 | Turn the ring left and right (press and hold) | OK (START) | None | None | Settings; enlarge the "MOD" and "Picture Book" buttons in the corner, click directly | None |
| Prologue text page | Title overlay Prologue page (`801C9EA8` family) | None | Next page (A) | None | Skip (R1+START) | Settings | Next page |
| Dialogue (plot, world map, intermission, battle lines) | The native dialogue reader has a dialogue box and is waiting for page turning | None (the direction area can still be used to look back and forth, without drawing the joystick) | Next sentence (A) | None | Fast forward (press and hold R2), automatic (L2) | Settings, skip (R1+START, only displayed in the plot), review (L1) | Next sentence |
| Select limbs (script `3D44`) | Select limb window opens (script engine current command `3D44`) | Select up and down | OK (A) | None | None | Settings | None |
| Tactical map · Idle | Mode is tactical, main state `0x80172EB0` = 5 (6 during cursor movement) | Move the cursor; drag to the bottom to accelerate for 1 second (C←) | Selection (A) | Unit information (B) | Previous unit (L1), next unit (R1) | Settings, previous enemy (L2), next enemy (R2) | None |
| Unit menu, moved menu, actioned menu, space menu | Main status 8, 0x3A, 0xD, 0x16 | Up and down selection | OK (A) | Return (B) | None | Settings | None |
| Select move destination | Main state 0xC, substate 0 | Move cursor | Move here (A) | Cancel (B) | Farthest (hold R1) | Settings | None |
| Weapon, target, spirit list | Main state 0x17 family, 0x19 | Up and down selection | OK (A) | Return (B) | Previous target (L1), next target (R1), only when selecting target | Settings | None |
| Information window, capability page | Main status 0x1B, 0x22, 0x2E–0x37, 0x3C, capability page | Page turning, list | OK (A) | Close (B) | Previous unit (L1), next unit (R1) | Settings | None |
| Grid list (sortie selection, etc.) | `801EDBE0` Family status | Select grid | Confirm (A) | Return (B) | Previous page (L1), next page (R1) | Settings | None |
| Battle Show | Mode 2 | None | None | None | Skip Show (R2) | Settings | None |
| Result screen, defeat prompt, any key window | Result `8020DA08`, defeat `801DF53C` Status | None | Continue (A) | None | None | Settings | Continue |
| Ending | Mode 0x20 | None | Continue (A) | None | None | None | Continue |
| Pre-battle confirmation (change to touch screen layout when touching, see below) | Request for pre-battle confirmation page `visible`, do not select spirit | Lower left fixed direction area: switch left and right to counterattack/avoidance/defense | Start combat (page command) | Return (B) | Select weapon, spirit (page command) | Settings, animation on/off | Choose one of the three options directly |
| Select spirit | `spirit_menu` on the pre-war confirmation page | Lower left fixed direction area | Confirm (A) | Return (B) | None | Settings | Direct point to the spirit list |
| Our page: Prepare each page, archive page, title subpage, name page | Request for each page `visible` | Lower left fixed direction area | OK (A) | Return (B) | When the page supports: previous page (L1), next page (R1) | Settings | Click the page's own button directly |
| Settings window, illustrations, MOD management | `settings_open`, `library_open` | None | None | None | None | None | Click all directly; return key to close |
| Unrecognized screen | None of the above | Complete direction area | OK (A) | Return (B) | L1, R1 | Settings, START, L2, R2 | None |

**Touch screen layout of the pre-war confirmation page** (selected by the user on 2026-10-03, only when the touch screen buttons are displayed, the three pre-war interface styles are replaced by this version): The bottom row of buttons and key prompts are not displayed, and the function is given to the right button group (the green "Start Combat" is in the main key position); the two pilot information bars below are moved to the middle, the lower left is given to the direction area, and the lower right is given to the button group; the entire page is moved down about 8 mm, put "Settings" and "Animation On/Off" on the top edge. When switching from avoidance or defense to counterattack, follow the original process and advance to the original weapon list to select a counterattack weapon.

Description:

- On the **Pre-battle confirmation page**, "Start Battle", "Select Weapon", "Spirit" and "Battle Animation" are originally buttons on the page, click them directly; the virtual buttons only retain direction, confirmation, and return, which satisfies "no separation".
- **Dialogue** The most commonly used action is to turn pages, so click anywhere on the screen to turn pages; the direction area still accepts dragging for review, but the joystick is not drawn to avoid occlusion.
- **Tactical Map·Idle** is the scene with the most buttons (5 plus settings). L2 and R2 (switching enemies) are placed on the top side because they are rarely used.
- **Unrecognized screens** return a complete set to ensure that no keys are missing on any screen. During implementation, record every scene that falls into this line in the log, and then add it to the table one by one.
- The return key and return gesture are equal to the secondary key 1 (B) in all scenes; close the window in the settings window, illustrated book, and MOD management.

## 4. Scene recognition

The interface thread does not read the game memory (the rules of `frontend.cpp`), so a new game thread module is added. Each game frame reads the following values, calculates the scene number and several flags, and publishes it with an atomic weight:

| Basis | Source | Confirmed |
| --- | --- | --- |
| Top-level mode | `8015DA02` (`800801A4` distributes table subscripts, see Section 3 of the original key document) | Static |
| Title stage | `intro::title_major()` | Actual machine |
| Tactical main state, sub-state | `0x80172EB0``+0`, `+2` | Actual machine (tactical UI state table) |
| Dialogue waiting for page turning | Native dialogue reader (`native_dialogue.cpp`) current frame | Actual machine |
| Select limb | Script engine current command (`8009EFDC` polled vm), `3D44` | Waiting for real machine |
| Prologue page | `intro::title_major()` is 13 (common prologue and each route prologue, added after 0.4.0) | Waiting for real machine |
| Result screen, defeat prompt | The hook of the corresponding function, or its state table subscript | Waiting for real machine |
| Our page | The interface thread itself has the `visible` requested by each page | Actual machine |

The recognition results only determine which buttons are displayed. The buttons still emit N64 keys, so even if the recognition is wrong, it is just that the buttons are missing or the labels are wrong, and the game will not receive incorrect operations.

## 5. Text

Each function name is an interface entry, available in three languages, and registered in `UI_KEYS` (`src/srw64_native/profile.py`). Try to limit the number of Chinese characters to four characters so that the round button with a diameter of 12 mm can fit; if it cannot fit, the font size will be automatically reduced according to the width. L1, R1, L2, and R2 are only used for unrecognized images.

| Key | Simplified Chinese | Japanese | English |
| --- | --- | --- | --- |
| `touch_settings` | Settings | Settings |
| `touch_ok` | OK | Decision | OK |
| `touch_back` | Return | 戻る | Back |
| `touch_close` | Close | close じる | Close |
| `touch_start` | Start | スタート | Start |
| `touch_l1` | L1 | L1 | L1 |
| `touch_r1` | R1 | R1 | R1 |
| `touch_l2` | L2 | L2 | L2 |
| `touch_r2` | R2 | R2 | R2 |
| `touch_next_page` | Next page | 时ページ | Next page |
| `touch_prev_page` | Previous page | 前ページ | Prev page |
| `touch_skip` | Skip | スキップ | Skip |
| `touch_next_line` | Next sentence | Time | Next |
| `touch_fast` | Fast forward | Early delivery | Fast |
| `touch_auto` | Automatic | オート | Auto |
| `touch_select` | Select | Select | Select |
| `touch_info` | Unit information | Intelligence | Info |
| `touch_prev_unit` | Previous unit | 前の丝方 | Prev unit |
| `touch_next_unit` | Next unit | 时の丝方 | Next unit |
| `touch_prev_enemy` | Previous enemy | Previous enemy | Prev enemy |
| `touch_next_enemy` | Next enemy | 下 enemy | Next enemy |
| `touch_move_here` | Move here | ここへ | Move here |
| `touch_cancel` | Cancel | キャンセル | Cancel |
| `touch_farthest` | Farthest | Farthest | Farthest |
| `touch_prev_target` | Previous target | Previous target | Prev target |
| `touch_next_target` | Next target | Second target | Next target |
| `touch_skip_battle` | Skip scene | Showスキップ | Skip scene |
| `touch_continue` | Continue | Times | Continue |

Japanese and English are the first drafts, and I will go through them again according to the rules for selecting proper names (mainland simplified Chinese, official English takes precedence).

## 6. Implementation sequence

1. **Skeleton:** Direction area (anywhere on the game screen, lower left corner of our page), primary key plus secondary key arc, small key on the top, click on the screen. The scenes are divided into three categories: our page, setting up this type of full touch-screen window, and others (a complete set). Acceptance: The existing process (opening → title → mini-level → battle) can only be completed by touching.
2. **Identification layer:** Game thread module and scene number, the current scene can be seen in the debugging interface `status` for easy inspection.
3. **Scene-by-scene access:** First connect the dialogue and tactical map (idle, menu, mobile selection), which account for the majority of the game time; then connect the title, battle performance, results and any key window; finally connect the list, information window, and ability page. Every time you pick up a scene, use the debugging interface to enter and take screenshots to check.
4. **Final:** Fill in the unrecognizable scenes one by one from the log; go through the three-language entries; play a complete episode on Seeker (opening → episode 1 → a battle → save), just touch.

### Progress (2026-10-03)

- Steps 1 and 2 completed; Step 3 accesses the opening, title, dialogue, map idle, unit menu, movement destination selection, weapon and target list, information window, battle show, ending, as well as our page and full touch screen window.
- Seeker has verified the recognition and buttons in the real machine: opening, title, dialogue (click the screen to turn the page), map idle, unit menu, select movement destination, pre-battle confirmation, battle performance ("skip performance" on the main key). The "Picture Book", "MOD" and "Settings" in the corner of the title have been changed to touch buttons at the top.
- Not picked up yet: Select limbs, grid list, results and defeat prompts (press "Unrecognized" temporarily to display the complete set, and select limbs to display along with the dialogue). The weapon and target list and information window are connected according to the status table, but I haven't gone there to check it on the actual machine.
- 2026-10-07 (after the release of 0.4.0): The prologue page originally fell in the "Opening" and only START, without skipping; it was changed to title stage 13 to identify it as a prologue page (next page + skip). The host also re-transmitted `title_waiting`, PRESS START redisplays the two top buttons of the illustrated book and the battle viewer.
- When the script is running between two dialogues, the map status is also idle when read, and the map button will be displayed briefly; it does not affect the operation.

## 7. TBD

Determined (user 2026-10-03): No point grid movement will be performed on the map, and the cursor will still use the direction area to add "Select" and "Unit Information" (A, B).


- Should a joystick be drawn in the direction area in the dialogue? My current plan is not to draw, but to just drag and review.
- When the unrecognizable scenes fall into a complete set, the appearance is very different from other scenes; whether to change it to just one more "More" button, and then expand it to display the other buttons.