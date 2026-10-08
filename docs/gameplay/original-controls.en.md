> **Language / Ngôn ngữ:** [English](original-controls.en.md) · [Tiếng Việt](original-controls.vi.md) · [中文](original-controls.md)

# Original key bindings (static analysis)

2026-09-28. This article answers the question "How does the game read the controller and what does each key do on each screen?" All conclusions come from disassembly (`build/recomp/cpu-scan/<overlay>/*.text.s`) and ROM data sheets, **not verified by actual machine**; where there are actual machine records, please indicate the source. The host side (keyboard/controller → N64 masking, remapping) is outside the scope of this article, see [Steam Deck Keyboards](../design/steam-deck-controls.md) and `src/host/input_bindings.hpp`.

Scanning method: Find all instructions for reading the input table (318), write down the function and the mask for subsequent tests, and then classify them by overlay and status table; the script is in the session temporary directory other than `tools` and has not been submitted.

## 1. Sampling layer (resident section)

| Function | Effect |
| --- | --- |
| `80087730` | Initialization: `osContInit` Get connection mask `D_8010F6C0`, clear all tables, input lock `D_8010F6BA=0` |
| `8008163C` | Each time the main loop is called: `80087A48` initiates reading from port 0 (`osContStartReadData`/`osContGetReadData` → `OSContPad D_800F97B0[4]`), `80087AA4` **ORs the key read this time into** the accumulated word `D_8010F1A4[口]`, and the direction of the joystick conversion is OR `D_8015F73C[口]`. Only continue when the game frame (`D_80172D0C ≥ D_8010F0C8`) is reached: `80087DD4` calculates edges, `80087C9C` reseedes with current values, `80081D60` synthesizes three tables |
| `80087AA4` | Joystick → Direction: `|x|≥45` is for the left and right positions, `|y|≥45` is for the upper and lower positions; the stored joystick value only goes out, and is cleared when it is retracted (ratchet), so the loose stick will not shake |
| `80087C9C` | End-of-frame reseeding: threshold changed to ±50 |
| `80087DD4` | Each port: valid flag `D_80178D24[口]`, calculated when the input lock is 0; `press = new & ~old` |
| `80081D60` | Synthesis: When the joystick has direction, use the `0xF00` bit of the joystick to **replace** the cross key bit; see the continuous words below |

Multiple samples between two game frames are accumulated by OR, and short press will not be lost.

### Three tables (one u16 for each port, port 0 is at the lowest address)

| Table | Meaning |
| --- | --- |
| `D_8015D9FA` / `D_8015CAF0` | Original hold / Original edge (without joystick) |
| `D_8010F124` / `D_8010F724` | Joystick conversion direction Press and hold / Edge |
| `D_800F97D0` **Press and hold** | Original press and hold, when the joystick has a direction, the direction position is changed to the joystick |
| `D_80178A08` **Press** | Edge version of the same; most screens read it |
| `D_801612E0` **Burst** | There is a press in this frame → Burst = press, count 12; otherwise the count reaches 0 and there is a press → Burst = press and hold, count 3. That is, the first delay is 12 frames, and then every 3 frames. **Burst is the whole word**, not just the direction keys: pressing A, L, R where you read the word will also burst (title track, map L/R switching) |

Bits: A `0x8000`, B `0x4000`, Z `0x2000`, START `0x1000`, upper `0x800`, lower `0x400`, left `0x200`, right `0x100`, L `0x20`, R `0x10`, C↑ `8`, C↓ `4`, C← `2`, C→ `1`.

- The game logic only reads port 0 (the first element of the table); only the `1p–4p ON/OFF` of the debug menu and the two viewer press port loops.
- The inter-field overlay also has a private chain table with the same algorithm `D_801DD62C`/count `D_801DECE0` (`801C4538`, `801C4A20`, etc. read it).
- Input lock `D_8010F6BA`: When set to 1, all four ports are cleared. `800A344C` (full screen flash/fade, script `3D3B` family) and tactics `801F2AAC` are set and cleared after completion.
- Dialogue advancement `8008D748` reads the A of **original edge** `D_8015CAF0` without going through the synthesis table.

## 2. Global combination

| Combination | Code | Effect |
| --- | --- | --- |
| Hold Z + press START | `80085EF8`=`rawhold&Z && rawpress&START`. World Map `801C28E4`, Tactics `801DFBD0`, For Sale `801C3788`, Title `801CA9CC`, Combat `801C9710`, Pak Management `801C34B0` Called every frame; Between Fields `801D8D20`, Name Page `801C657C`, the two viewers judge themselves `rawhold&0x3000` | `80099814(5,1,2)` fade out, then mode 1 (BANPRESTO logo → title). At the end of the fade out, if START **still pressed** and the first half word bit15 of SRAM `0x08003E10` is 1 (`80093610`) → mode `0x11` reload the current level, otherwise mode 7 title (battle `801C97E4`, world map `801C2968`, interfield `801D8DDC` is the same in three places). For retail cartridges, this bit is 0, and the player will only return the title. See the actual measurement in the battle performance [Battle performance skip](../native/battle-animation-skip.md) |
| Power on and hold down START | `800801A4` samples once `D_8010F1A4&START` | Initial mode `0x19` (`load_0022CFD0`, コントローラパック management), otherwise mode 7 |
| Script selection limb `3D44` | `8009F3A8` | Continuous words ↑↓ Move the cursor (sound 0xB9), press A to confirm |
| Dialogue | `8008D748` | Only A's. There is no fast forward, B has no effect; the same function of battle lines |

## 3. Mode and overlay

`800801A4 → 800CFEC8[模式−1]`, each item is a loading stub. Modes requested with constants: 1 logo, 2 battle show, 3/0x11/0x16/0x22 tactics, 4 intergame, 5/6 name, 7 title, 12/13 world map, 0x12–0x15 load, 0x1A/0x1C battle variant, 0x1F, 0x20 ending, 0x21 sale, 0x23/0x24. The following are only accessible from the debugging menu or boot combination:

| mode | overlay | content (ASCII string in ROM) |
| --- | --- | --- |
| 1 | `load_000856D0` | BANPRESTO flag; `[64 BASE SAMPLES]` debugging menu in the same overlay |
| 8/9 | `load_00089EA0` | `ROBO VIEWER !!` (Sprite/Animation Viewer, `komaokuri!` frame by frame) |
| 10 | `load_0008E580` | `ROBO VIEWER !!` 3D version (`FOG`, `rotx/roty/rotz`, `dist`) |
| 16 | `load_00216730` | `BTLINIT`: Combat parameter editing, press and hold Z to enter mode 2 |
| 0x18 | `load_0022E580` | `[KARAOKE MAKER]` (`BLOCK EDIT`, `TIMING EDIT`) |
| 0x19 | `load_0022CFD0` | コントローラパック Management (press and hold START when booting) |

Debugging menu `801C3174` (table `801C69C8`): Continuous ↑↓ cycles through 27 items; ←→ and C←/C→ adjust two parameters, and while holding B, hold down the direction to change continuously; A executes `801C35D0 → 80080188(D_801C69D4[项])`. Items: TITLE, NAMEENTRY0/1, VIEWER, VIEWER2, ​​HMF VIEWER, CONTINUE, LOAD1–4, ENDING, INTERMISSION, TACTICS, BTLINIT, WGADRS, KARAOKE, SELL UNIT, DEBUG CONTINUE, SAMPLE DATA 0–3, 1p–4p ON/OFF, fbuf clear color. The conditions for entering the menu are not pursued (cannot be entered during normal startup).

## 4. Each screen

Writing method: `按下`=`D_80178A08`, `按住`=`D_800F97D0`, `连发`=`D_801612E0`, `原始`=`D_8015D9FA`/`D_8015CAF0`. If B is measured first and then A is measured in the same place, it is written as "B/A".

### Title `load_0010DA50`

| Screen | Function | Key |
| --- | --- | --- |
| PRESS START Pages | `801C5188`, `801C53F4`, `801C591C`, `801C5D94`, `801C6514` | Press A or START (`0x9000`) |
| Ring menu | `801C642C` | **Hold** ←→ Move the cursor (not the edge, see [Title Menu](../native/native-title-menus.md)) |
| オプション | `801C6B14` | Continuously fire ↑↓, press A |
| ロード Each page | `801C709C`, `801C783C`, `801C7A48`, `801C8074` | Continuous ↑↓, press A/B |
| サウンド list | `801C8724`, `801C9904`; EXIT focus `801C89E4`, `801C9ADC` | Continuous ↑↓ (↓ measured alone), press A, A/B |
| Playing | `801C9268`, `801C97AC` | Press B to return; burst Z/↑/L for previous song, ↓/R for next song; press C↑ −10, C↓ +10; C← only in tracks `0x124` and `D_801CC1FA[项]==1` There is action from time to time (hidden item, not pursued) |
| Prologue pages | `801C9EA8`, `801CA0A4`, `801CA1C0` | Any key → `801C5F04(1)` to turn to the next page; `801CA608` Press A |

### Protagonist selection and name `load_001090A0`

`801C50B8` Protagonist choice A (←→ in `801C34E4`), `801C5644`/`801C5AD0` Name edit A, B, A or B, `801C5E88` Final confirmation A/B, `801C62D8` Kana plate A, B. Each frame `801C657C` self-determines Z+START and START. The host has taken over, see [name page](../native/native-name-entry.md) and [unit name fixed](../native/fixed-unit-name.md).

### World Map `load_000A7EC0`

There is only Z+START for each frame. The rest is all scripted (Dialogue A, Select Limb).

### Tactical map `load_000AB160` (main status table `D_80217E0C`, status meaning see [enemy-cycle](../native/enemy-cycle.md), [move-jump](../native/move-jump.md))

| Status/Function | Function | Key |
| --- | --- | --- |
| Cursor movement | `801C63D8` (adjusted by `801C66E8`) | Read press when there is no direction in the previous frame, otherwise read hold; direction table `D_80217AAC` includes oblique direction; **Hold C↓ or C←** 8 pixels per frame, otherwise 4 |
| Idle 5 | `801C8B04` | Continuous fire Z/L Previous, R next unaction our side (`0x2030`, Z is synonymous with L); press A to select; B unit window/terrain panel |
| Unit menu 8, 0x3A | `801CA7E4` | Burst ↑↓; press A to decide; press START only valid on item type 5 (Mothership Haijin) → `801D050C(0,0)`, read START in it (details not followed) |
| Move selection 0xC/0 | `801CBB04` | A confirm, B cancel; do not read R, L, Z, START |
| 0xC/7 | `801CDF7C` | Continuous ↑↓ `D_80172ED6`, press A／B |
| State 9 | `801CB074` | Press any key to close the window and select the unit under the cursor |
| Status 0xB | `801CB88C` | Any key to close the window; `0x2030` switch (Z/L previous, R next) |
| 0xD/0xE family | `801CE144` (`801CE1E4`, `801CE234`, `801CE3A0`); `801CE234`; `801CF70C`; `801D21D0` | `801CE144`: Z/L Previous, R next (`D_80172ED6`). `801CE234`: When there are multiple drivers, A or → next, ← previous, B returns. `801CF70C`: B is returned and released. `801D21D0`: A or B close the message window |
| Attack/weapon 0x17 family | `801D3010` (7 tunes including `801D3140`), `801D2A10`, `801D3140`…`801D4320` | Press A to decide each sub-state, B Cancel; `801D26B4` (`801D3140`, `801D6FFC` key): Burst Z/L/R Switch target in 60-slot roster |
| Confirmed before the war | `801D5064`, `801D5294` | A/B; `801D5294` There is also a burst ↑↓. Taken over, see [Combat UI](../native/native-battle-ui.md) |
| Information window 0x1B, 0x22, 0x2E, 0x2F, 0x30, 0x34, 0x36, 0x37, 0x3C | Press A to advance each status function; share `801D6FFC` B to close + `801D26B4` L/R/Z to switch units |
| Ability page | `801F9BB4` (`801D1DB8` key), `801D6784`, `801F1B10` | A; continuous cross-hair keys; L/R page turning (R next page, Z/L previous page, `D_80227A82..84`); `801D6784` B return, continuous fire ↑↓ List `D_80227A81` |
| Grid list (sortie selection, etc.) | `801EDBE0` (`801C7DB8`, `801D0EE0`, `801D1C28`, `801DBEE4`), `801EE060` (`801D1CE8`), `801EE594` | Press ←→ column `D_8015DA0B`, burst ↑↓ row `D_8015DA0F`, R next page, Z/L previous page, A decision |
| Two-dimensional list | `801F9238` (`801CE3A0`, `801D2FB8`, `801D5404`) | Continuous ↑↓ `D_802271DB`, press ←→ `D_802271D8`, B |
| Options window | `801D1F88` | B/A; write `D_8015DDA8` (including combat animation switch) and `8009187C` write back to SRAM header |
| Return to title confirmation | `801D22FC` (table `80217C84`) | Continuous ↑↓(`801C2600`); A in item 1 → Mode 7 title; B or A in item 0 → `801C8AB4` Return |
| Defeat tips | `801DF53C` (table `80217DF4`/`80217E08`) | Press A, B or START → sound 0xB4, mode `0x16` to restart this level |
| Result screen | `8020DA08` (table `8021E274`) | Wait 20 frames and press A to advance |
| Opening state 2 subtable `80217AFC` | `801C7BF0`, `801C7DB8`, `801C7E30`, `801C7FA0`, `801C80A4` | Any key to advance; B; A decides at item 0, A/B returns (inferred to be list and confirmation before attack) |
| Each frame | `801DFBD0` | Z+START |
| Dead code | `801E03C4` | Raw pressing START toggle `D_8015DDA8` bit2 (combat animation); no calls or table references |

### Combat performance `load_00121560`

- `801C9710` Main loop: When the flag `0x1A` (`8008016C`) and `D_80161310==1` are pressed, **B** will end the current segment and fade out; when `D_80161310==0`, it will end automatically; when the flag `0x1C`, **any key** will end. No input is read outside: no skipping, no fast forwarding. Z+START See Section 2.
- `801C9DAC` Each frame: Press and hold **C↑** to clear `D_8010F5BA` (`8008422C` is set and the flag of each overlay entry is cleared, the purpose is not pursued).

### Interfield `load_0008F4B0` (screen table `D_801DC9D0`)

Click the table to read all, and the direction is published by the private link. A/B screen: main menu `801CE19C`, archive `801CEABC`/`801CEEF8`, transformation `801CF564`/`801CF988`/`801D04A4`/`801D087C`/`801D1100`, ability `801D1554`／`801D2378`, weapon list `801D21F8` (B only), transfer `801D263C`／`801D2A24`／`801D3A90`／`801D41FC`／`801D4578`, parts `801D4A98`/`801D4C94`/`801D51EC`, Link Battler `801D70FC`.

- Ability page `801D2030`/`801D24C8` and Link Battler `801D6D34`: `0x2030` → `801CCDA0`: Z/L for the previous one, R for the next one.
- `801D8D20` Per frame: **Hold** Z+START (`0x3000`) → exit code 1 → fade out → title (or SRAM debug bits + START → `0x11`).
- Unreferenced legacy chains `801D796C`–`801D8CC8` (A/B/↑↓) and `801DA2C0`–`801DAAEC` (R/Z＋L,↑↓,C←,A,Z＋START) see [Intersession Menu](../native/native-intermission-menu.md), [Link Battler](link-battler.md).

### For Sale `load_00107BF0`, Ending `load_001156A0`

For Sale: `801C3088` Any Key, `801C3514` Continuous ↑↓, A, A or B, `801C3788` Z+START. Ending `801C2D1C`: Advance with any key.

### Debugging overlay

- Pak management `load_0022CFD0`: `801C35E4` A/B, burst ↑↓; `801C36BC` burst ←→, B/A; `801C37F0`/`801C382C` A; exit back to mode 7.
- Wizard Viewer `load_00089EA0`: Press orally to read L, C←, Z+START.
- 3D viewer `load_0008E580`: Press and hold ←→/↑↓ to adjust the camera (`D_8015DDF0` a set of floating points, `80081CB8` reset), START, L/R, Z, Z+START.
- BTLINIT `load_00216730`: `801C32EC` Each of the ten keys changes parameters continuously (subscript `D_8010F7BE`, table `D_8015DCBA…`), `801C3850` press and hold Z → state 0x17 → mode 2.
- KARAOKE MAKER `load_0022E580`: ↓／↑／C→, C↑, L／R, burst ↑↓, A＋B＋→, C→／Z, B.

## 5. Useful conclusions for remapping

- **Z is an alias of L in the list**: all "previous" tests `0x2020`, "next" tests `0x10`; the only uses of Z are Z+START reset and BTLINIT. You won't lose functionality by assigning another key to Z.
- **C key only has three functions in the normal process**: map cursor acceleration (C↓, C←), title track ±10 (C↑, C↓), and holding down C↑ to clear a mark during battle. C→ Not used in normal procedures.
- **START in the normal process only has **: PRESS START, Z+START, mothership entry, and "any key" for defeat prompts. The combat animation switch goes through the options window, not START (that START switch is dead code).
- **The cross keys are equivalent to the joystick**. When the joystick has a direction, it covers the cross keys; the oblique direction is defined in the map cursor table.
- **Continuous words are whole words**: Mapping a certain key to "press and hold" will trigger continuously in the screen of reading continuous words (L/R to switch units, track switching).
- The dialogue only recognizes the original edge of A, and any synthesis and fast forwarding are done by the host.
- Short presses will not be lost (inter-frame OR accumulation), but the button must span one game frame sample to be seen; just give a frame edge when injecting the button (this is already done for field-to-field takeover).