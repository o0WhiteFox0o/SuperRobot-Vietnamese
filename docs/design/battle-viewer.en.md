> **Language / Ngôn ngữ:** [English](battle-viewer.en.md) · [Tiếng Việt](battle-viewer.vi.md) · [中文](battle-viewer.md)

# Battle Viewer design research

2026-10-03. Pure static analysis (disassembly of `build/recomp/cpu-scan/*/rom_*.text.s`, ROM data), **no game running, no building**. Goal: Add a "Battle Appreciation" entry next to "Library" and "MOD" on the title screen (refer to SRW Z スペシャルディスク's Battle Viewer), the player selects the attacking unit + pilot, weapons, defending unit + pilot, whether to counterattack and counterattack weapons, the defender's defensive reaction (hit/avoid/clone/cut/S defense/shield), damage amount, whether to shoot down, combat background on both sides, BGM, and then use the original performance overlay `load_00121560` to play, and return to the appreciation page after the end. It also serves as a testing tool for our own performances.

Anyone writing "inference" has not checked it with the actual machine; the line number refers to the disassembled text under `build/recomp/cpu-scan/` (`resident/rom_80076610.text.s` is called resident, `load_00121560/rom_801C2600.text.s` is called battle, `load_000AB160/rom_801C2600.text.s` is called map, and `load_0010DA50/rom_801C4500.text.s` is called title).

Related documents: [Battle show rendering mechanism](battle-animation-rendering.md), [Combat show exit midway](../native/battle-animation-skip.md), [Combat calculation](../gameplay/battle-formulas.md), [Library](../native/library.md), [Title menu](../native/native-title-menus.md).

## 0. Conclusion first

**The original version itself has a path to "play a show without entering the level"**: the demonstration battle of the title standby (game mode `0x1C`) and the background battle of カラオケモード (mode `0x1A`). Both of them only install the performance overlay. The resident function **`8009C2DC`** directly fills in the combat records `D_800F97E0 + side×0x1074` on both sides according to the 32-byte demonstration record in the ROM (ROM `0x83110` and above). There is no need for map overlay, roster, level, or archive. After playing, the main show loop will switch back to the title overlay.

Therefore, there is no need to create hidden mini-levels or fake map settlements for battle appreciation: **The entry and return of mode `0x1C` are followed, the host hooks on `8009C2DC`, and the battle participation record is rewritten according to the selection on the appreciation page**. Hit/avoidance/clone/cutting/S defense/shield, damage amount, and knockdown are all determined by several fields in the battle record. The performance overlay does not roll any dice to determine the result (the calculation is in the map overlay, and this path does not run at all).

## 1. Normal process: Map → Show → Map

| Steps | Location | Facts |
| --- | --- | --- |
| Attack process | map state 24 `801D6534`, sub-state table `D_80217CC4` | sub-state 0 build participation table `8018B6E8` (step size 0x5C), 2/3 settlement `801F7D6C`, 8 request fork via `801DF96C` (see details [battle-animation-skip.md](../native/battle-animation-skip.md)) |
| Fill in the performance participation record | map `801F3578` (map:55379) | Write `D_800F97E0`/`D_800F97E0+0x1074` from the two items in the participation table, see §2 for the fields |
| Fork | map `801D4E6C` (map:20953) | `8015DDA8 & 4` clear (animate on) → `8009DB8C()`, `80080188(2)`, `80099814(5,1,2)` fade out |
| Change overlay | resident `800801A4` (resident:11582), jump table `jtbl_800CFEC8` (subscript = mode − 1) | Mode 2 → `8007FF4C` (resident:11372) install ROM `0x121560..0x184730` to `801C2600`, install separately `0x217FD0..0x22CFD0` to `80400000`; then `8007F510(801C9BD4,0,0)` |
| Performance entrance | battle `801C9BD4` (battle:8698) | Use global frame count `D_8010E09C` to reseed `800821B0`; lens and lighting initial values; `80084A54` clear background status; `801C2C3C` mask; mode 0x1A adjustment `8009C1DC`+`8009C2DC(0)`, mode 0x1C calls `8009C2DC(1)`; registers each frame `801C9710`/draws `801C96F4` |
| per frame | battle `801C9710` (battle:8367) | status `D_80250000`, jump table `D_80222DD4` (25 items, see battle data segment `rom_80222D44.data.s:87`) |
| Ending | battle `801C9854..801C99F0` | After fadeout completes `800B6620(1)`, `8009ABCC`, `800997D0`, `8008B950` (release 300 Elf slot), `8008DB2C`, `8008AC78(4)`; press the mode to select the next mode (§4), `8007F510(800801A4,0,1)` Return to the distributor |
| Return to the map | Mode 0xB (when the previous mode is `D_8015DD60 == 3`) otherwise 0x10 | The map is in state 24 substate 4 by `801FCA78` and write the result into the roster |

Key points: **The performance overlay only reads the battle record `D_800F97E0`**, never writes the roster; the settlement `801F7D6C` has been run through the map overlay before it is loaded. The random draws in the show only include line selection (`80222B14` twice `80082334`) and universal weapon action-0 posture once (`801E3BA0`), which do not affect the result.

Status numbers and routines (`D_80222DD4`): 0 `801C6FE8` reset, 1 `801C70A8` load, 2/7/13/18 `801C840C` lines, 3 `801C7494` approach, 4/15 `801C75D0`, 5/16 `801C76A0` Fire (switch to defender background), 6/17 `801C7890`, 8/19 `801C78DC`, 9/20 `801C7960` Deduct blood to finish, 10 `801C7BC0` Counterattack preparation, 11 `801C7E1C` Change sides, 12 `801C7F18`, 14 `801C7FC4`, 21 `801C80C0` Closure, 22 `801C818C` Down, 23 `801C83CC`, 24 `801C7448`.

## 2. War participation record `D_800F97E0 + side × 0x1074`

`side` 0/1; the attacking subscript is `D_80178C78`, the defensive subscript is `D_80178B50` (s16, switch sides and `801C7E1C` is interchanged). The following table "Writer" lists what the map path `801F3578` and the demo path `8009C2DC` write.

| Offset | Type | Meaning | Map path source (combat entry + offset) | Demonstration path `8009C2DC` | Performance reading |
| --- | --- | --- | --- | --- | --- |
| +0x00 | s8 | This record is attacker 0/defender 1 | constant | record subscript | everywhere |
| +0x02 | u16 | Driver **Capability Record Number** = `D_800CA9C4[人物号]` | Driver instance +2 → Lookup table | Demonstration field 1 → Lookup table | Lines `80222B14`, `8022245C` (ROM `0x1161C0` line list, step size 0x24) |
| +0x04 | u16 | Airframe number | Aircraft instance +2 | Demonstration field 0 | Sprite, scaling `801C34D8`, `801C3F44` |
| +0x06 | s16 | **Weapon performance number** (weapon library subscript) | `801F3554` = `800AB470(机体, 武器)`; when there is no weapon, it is the reason code `+0x11` | Demonstration field 3 | `801C410C` → `801C3D38(+6, +0x2C, 0)` Load attack block |
| +0x08 | s16 | **Defender reaction code** (reaction library subscript, −1 = normal hit) | `+0x26` written in settlement; 0x14 during rescue | Demonstration field 4 | `801C410C` → `801C3D38(+8, +0x848, 1)` Load reaction block; `801C3E7C` determines whether to deduct blood |
| +0x0A | u8 | background record b (terrain) | `+0x27` | demo field 6 | `80084A78(+0xB, +0xA, side)` |
| +0x0B | u8 | background record a (group via `D_800C5940[a]`) | `+0x28` | demo field 5 | Same as above |
| +0x0C | u8 | Inference: air/ground attitude position (mostly 1 when +0xA=100 in the demonstration) | `+0x29` | Demonstration field 7 | `801C4920`/`801C4940` (positioning `801C39B0`, body `801C4160`) |
| +0x0D | u8 | Size file 0–4 | `+0x2A` | +4 size bit conversion recorded by ROM body | Shooting script selection `801C49A0` |
| +0x0E | u8 | Sprite scaling (show written by myself) | 0 | 0 | `801C3F44` written |
| +0x12/+0x16 | | Weapon combat record column 6/column 3 (written by the performance) | | | `801C3F44` |
| +0x17 | s8 | Participation table `+0x16` | | | `801C87C8`, `801C91C0` |
| +0x18 | s8 | **Defender Order**: 0 Counterattack, 1 Defense, 2 Avoidance (non-0 = no counterattack) | Defender converted by `D_8018B754`; Attacker 0 | 0 | Status 9/20 `801C7B5C`: Non-0 → Status 21 No counterattack round; HUD label `801C2FDC` (0x482/0x483/0x484) |
| +0x1A | u16 | **Damage caused by our side** | Battle table `+0x14` | When the opponent's "Downed" flag is set = opponent's HP, otherwise `rand(对方HP−20)+10` | `801C3E7C` |
| +0x1C | u16 | The damage suffered by our side (the performance is calculated by yourself) | — | 10 | `801C3F44` write = `801C3E7C(side)`; blood deduction queue `801C8A58` read the defender's |
| +0x1E | u16 | Participation table `+0x18` | | 0 | |
| +0x20/+0x22 | u16 | Max HP/Current HP | Unit Instance +6/+4 | Both ROM Unit Records +0 | HP Window `801C2C98`; `+0x22 == 0` → Downed `801C5AF4` |
| +0x24/+0x26 | u16 | Maximum EN/Current EN | Unit instance +0xA/+8 | Both ROM unit records +2 | HP window |
| +0x28 | s8 | Currently attacking block 0/defending block 1 | Attack 0, defend 1 | Attack 0, defend 1 | `80222C5C` |
| +0x2C / +0x848 | 0x81C×2 | Attack animation block/reaction animation block (fill in by yourself for the performance) | | | |
| +0x1064 | u32 | Airframe instance pointer | Participation table `+4` | `&D_8016A210` (placeholder) | `801E40B0` (rescue HP exchange), `8022245C` (only when the previous mode = 3) |
| +0x1068 | u16 | Participation table `+0x2C` | | 0 | `801C4A08` |
| +0x106C | u32 | Body instance pointer for caregiver/dummy | Protector or self or 0 | `&D_8016A210` | Assistance branch `801C3E7C`, `801C4AEC`, `80222B14` |
| +0x1070 | s16 | Responder's response code, −1 None | | −1 | `801C3E7C`, `801C4808` |

The demonstration path is also written as `D_80178C78 = 0`, `D_80178B50 = 1`, `D_800F9808 = 0`, `D_800FA87C = 1` (resident `8009C63C..8009C660`).

### 2.1 Weapon Performance Number

- `800AB470(机体号, 武器号)` (resident: 61973): Check the resident table `D_800CB7BC` (ROM `0x561AC`, 89 entries {weapon, body, performance number}, ending with {0,0,0}), if hit, use the performance number in the table, otherwise **performance number = weapon number**. Example: (34, 7) → 38, (130, 308) → 1191. You must go through this table when appreciating the weapons on the page, otherwise the weapon with the same name will have the wrong animation on a specific machine.
- `801C3C9C(id, kind)` (battle:1674): kind 0 → `id == 0x1000` records `D_80250010` with memory, `id ∈ {−2, −3}` records `D_80222D40` with null, and the rest `801C3128(id)` (weapon library, ROM `0x11FC80` Offset table + `0x184990`); kind 1 → reaction library `801C3230`; kind 3 → hit library `801C31E8`. `801C3D38` is not loaded directly when id == −1.
- Weapon name text `1370 + 武器号`, machine name `527 + 机体号`, character name `4382 + 人物号` (`src/host/battle_page.cpp:194-196`).

### 2.2 Defender’s reaction code (determines the defender’s performance)

Settlement `801F7204` (map:59633) Press "Hit → Clone → Cut り払い → False Body → Shield → S Defense" to write the participation form `+0x26`, and move it into `+8` as it is. Code confirmation value:

| Code | Meaning | Settlement source | reaction library record (`assets/original-graphics/animations.json`) | Defender's blood deduction |
| --- | --- | --- | --- | --- |
| −1 | Normal hit | Default | Not loaded, the defender uses the default hit action of `801C49D8` | Buckle |
| 2 / 3 / 5 | I Force Field/Beam Coating/Planetary Defense **Block** | `801F6F3C` (map:59421) | 0x2164CC (Behavior 375 BeamShield) | No deduction |
| 4 | Blocked by aura barrier | `801F7590` | Same as above | No deduction |
| 6–0xC | Clone: 0x20000 Getter Phantom 6, 0x1000 Mach Special 7, 0x2000 True Mach Special 8, 0x1 God's Clone 9, 0x40000 Instant Phantom Foot 0xA, 0x100000 Super Jammer 0xB, 0x10 Clone 0xC | `801F6C44` (map:59196) | All the same 0x2163D0 (behavior 272 afterimage) | No deduction |
| 0xD / 0xE / 0x10 | I Force Field/Beam Coating/Planetary Defense **Damage Reduced by Penetration** | `801F768C..801F76C4` | 0x2164CC | Buckle |
| 0xF | The aura barrier was penetrated | `801F7568` | 0x2164CC | Buckle |
| 0x11 | S Defense (Shield) | `801F6FDC` (map:59472) | 0x2164FC (behavior 362 Shield) | Buckle |
| 0x12 / 0x13 | Cut り払い (attacker's weapon `+0x22 & 1` is set to 0x13) | `801F6D10` (map:59255) | 0x216538 / 0x216518 (behavior 377, action 10 / 11) | No deduction |
| 0x14 | Support Defense | `801F3974` | 0x2164A0 (Behavior 367 CoverDiffence) | Detain Protector (read `+0x106C`) |
| 0x15 | fake | `801F6E3C` | 0x216568 (registration 969, behavior 103) | read `+0x106C` |
| 0x16 | Miss (avoid) | `801F732C` | 0x216558 (no actor, defender action 15) | No deduction |

Of the 28 entries in the reaction library, 0, 1, and 13–16 share BeamShield, and 0x17–0x1B and 6–0xC share afterimage records, so the types on the screen are actually only: hit, shield, clone afterimage, cut × 2, shield, support, fake body, and avoidance**.

Whether to deduct blood is determined by `801C3E7C` (battle:1813): when the reaction code is −1 or 0xD..0x11, the damage suffered by the party = `min(对方 +0x1A, 本方 +0x22)`, otherwise it is 0; 0x14/0x15 changes to the HP of the body pointed to by `+0x1070` and `+0x106C`. The result is written into `+0x1C` by `801C3F44` in status 1, and the HP deduction queue `801C8A58` (battle:7385) is listed by weapon combat record 5. Check `D_80222E50` and split it into several beats. `801C8D6C` is written into HP `+0x22` for each beat.

### 2.3 Downing

Status 9/20 `801C7960` (battle:6180) adjusts `801C5AF4(守方, 0xA)` (battle:3974) after the blood deduction queue is released: when the defender reaches `+0x22 == 0`, the attacker's weapon performance number == `0x4A6` → status 21 (no explosion), otherwise → **status 22 Knockdown**; when the defender is still alive, `+0x18 != 0` → state 21, otherwise enter the counterattack round (state 10). Status 22 `801C818C` According to the aircraft combat record column 6 == 2, select hit 156, otherwise size `+0xD == 2` select 157, otherwise 158.

So "Kill down" = attacker's `+0x1A ≥ 守方 +0x22` and the reaction code belongs to the type that deducts blood. The branch condition of "0x14 and 0x15" in `801C5AF4` is always false, which is dead code.

### 2.4 Background

`80084A78(a, b, side)` (resident:16807): Background record number = `D_800C5940[a] × 101 + b` (ROM `0x5BC30`, 0x26 bytes), a = war participation record `+0xB`, b = `+0xA`. Status 0 `801C6FE8` uses the **attacking side**'s share; firing status 5/16 `801C76A0` is replaced by `801C2AD0(side)` (battle:343) with the **other side's" share. In other words, **SRW64 originally has one background on each side**, which is switched when the attack flies to the opposite side, which matches the one row of terrain on each side of the Z appreciation page.

## 3. Original independent performance entrance: mode 0x1A / 0x1C

| Mode | Who sets | Load | Entry call | Special behavior |
| --- | --- | --- | --- | --- |
| 0x1A カラオケ | title `801C9904` (title:6181) Press A: `D_80172D08 = 歌号`, `80080188(0x1A)`, `80099814(5,1,2)` | `8007FF9C` (only install `0x121560`) | `8009C1DC` (static list + `80090128(歌)` starts karaoke), `8009C2DC(0)` | Do not build HP window and HUD (`801C7268`), do not draw a mask; draw lyrics for each frame `8009055C`; B Fade out after the key or song is played; **Start over** when the performance is finished while `D_80161310 == 1` (the song is still playing): `D_801613DA = (+1) mod 6` Change to the next record, `8009C2DC(0)`, status 0 |
| 0x1C Title Demonstration | title `801CA1C0` (title:6805) Standby 180 frames: `80080188(0x1C)`, `D_80161310 = 1`, `80099814(5,1,2)` | `8007FFD0` (only install `0x121560`) | `8009C2DC(1)`, record selected by `D_8018B87C` | HUD normal; `D_80178A08` (press word) any key other than 0 will fade out |

(Mode 2 also installs additional ROM `0x217FD0` to `80400000`, but there is no direct call to `804xxxxx` in the performance overlay, resident, or map. The two demo modes can be played without installing it, so it is inferred that it has nothing to do with the performance.)

**DEMO RECORD**: ROM `0x83110` starts with 42 u32 offsets (first 19 = 6 each for カラオケ 19 songs, last 23 = 1 each for title demo), 32 bytes each = 8 s16 on each side:

```
[机体号, 人物号, 被击坠标志, 武器演出号, 反应码, 背景 a(+0xB), 背景 b(+0xA), +0xC]
```

Example: Title Demonstration #29 `(196,145,0,778,−1,0,100,1) / (300,150,1,1165,−1,0,100,1)` The defender was shot down; #24 The defender’s reaction code was 18 (cut り払い); #26 The defender was 13 (the shield was penetrated). The downed symbol is written in §2 +0x1A.

All actions for `8009C2DC(arg)` (resident:43956): Allocate temporary buffer `80089970`, DMA demo recording; for each side `8009C218` (resident:43902) Write default value (+0x18=0, +0x1A=`rand(3000)+10`, +0x20/+0x22=5000, +0x1070=−1, +0x1064/+0x106C=`&D_8016A210`, etc.), DMA ROM For the aircraft record (`0x71B80 + 机体×0x24`), write the fields according to the §2 table; then press the downed flag to set +0x1A; finally write the offensive and defensive subscripts. **It doesn't read rosters, it doesn't read saves, it doesn't require maps**.

**Return** (battle `801C98CC..801C99D8`):

- Mode 0x1C: `D_80161566++`, `D_801614EA++`; if `D_801614EA == 5` and `D_80161310 == 1` → clear, `8007E87C(0xB4)`, **Mode 7 (restart screen)**; otherwise `D_80161310 != 0` → Clear, `8007E87C(0xB4)`, mode 0x1E; `== 0` → `D_801614EA = 0`, `8007E87C(0xB4)`, **mode 0x1D**.
- Pattern 0x1A: The song ends → Pattern 0x1B.
- 0x1B/0x1D/0x1E all enter the title overlay's `801CAB50(kind)` (title:7511), kind = 1/2/3: 1 returns the karaoke list, 2 calls `801C5F04(0)` (title), 3 calls `801CA27C` (inference: cutscene before the next demonstration).

**Key press abort**: Main loop `801C9754..801C97B0`: pattern 0x1A and `D_80161310==1` and `D_80178A08 & 0x4000` (B) → fade out; pattern 0x1A and `D_80161310==0` → fade out immediately; pattern 0x1C and `D_80178A08 != 0` → fade out. Aborted on `D_80161310 = 0`.

## 4. Existing extension entry for title screen

- Library/MOD is the host RmlUi button, not the original menu item: `src/native/ui/frontend.cpp:2419``home_sync()` In the title main state 2 (PRESS START) and 3 (ring menu), draw `library-open`/`mod-open` (`frontend.cpp:2434`) in the lower right corner, click Process `frontend.cpp:2618/2621`, the panel is hung on the setting window frame (`library_panel()`, `frontend.cpp:1110`), and the input takeover is the same as the setting window. Data is read from ROM by `src/host/library.cpp` (airframe table `0x71B80`, weapons `0x74E90`, airframe weapon list `0x7E210`, character abilities `D_800CA9C4`, etc.), and the menus on the appreciation page can be reused directly.
- A precedent for the host to switch to game mode from the title: mini-level is entered directly, `src/host/game_hooks.cpp:85-98` is adjusted in the frame boundary `resident_func_80085F30`, `800836CC(0)`, `800A5138()`, and the scene number, `80080188(0xC)`, `8007F510(0x800801A4,0,1)` is written.
- Title overlay's own exit: every frame `801CA9CC` (title:7403) sees the fadeout complete (`80099B30() == 3`) and does `800B6620(1)`, `800997D0`, `8008B950`, `8008DB2C`, `8008AC78(4)`, if `D_801CC3A3` (start the game) then `800836CC(0)`, `800A5138` and select mode 7/0x11, and finally `8007F510(800801A4,0,1)`. The description of カラオケ and the title is "First `80080188(模式)`, then `80099814(5,1,2)`, wait for the end here", **do not adjust `800A5138`**.

## 5. Recommended solution

**Follow the entire path of the title demo (mode 0x1C) and replace only the data of `8009C2DC` with the selection of the appreciation page. **

1. **Appreciation page**: RmlUi panel, the entrance is in the same place as Library (add a button to the corner of `home_sync`, and add a line to the "General" setting page). All data is read from ROM and reused in `library.cpp`.
2. **Start**: At a certain frame while the title is still running (frame boundary hook, same location as the mini-level):
- Optional BGM: `8007E810(歌号)` (§6.6)
- `D_80161310 = 0`, `D_801614EA = 0`, `D_801CC3A3 = 0`
- `80080188(0x1C)`, `80099814(5,1,2)`, let the `801CA9CC` of the title overlay be finished as the original and handed over to the distributor (the same method as `801CA230..801CA250`);
- The host sets the "appreciation in progress" mark, the appreciation panel is closed, and the input is returned.
3. **Fill in the war participation record**: Add host packaging to `resident_func_8009C2DC` (add an item to `NATIVE_HOOKS`, change it to `make recomp-cpu` manually). When appreciating: first adjust the original function (set `D_8018B87C` to 0, ensure that it goes through the default value of `8009C218`, writes the offensive and defensive subscripts and placeholder pointers), and then press select to overwrite:
- Both sides `+2 = D_800CA9C4[人物]`, `+4 = 机体`, `+0xD` according to the ROM body record +4 converted size (same as the original function `8009C490..8009C4E4`)
- `+0x20/+0x22`, `+0x24/+0x26`: ROM body HP/EN, or appreciation page custom HP
- Attacker `+6 = 800AB470 规则下的演出号`; Defender `+6` = Counterattack weapon performance number (just put any legal value when not counterattacking)
- Defender `+8` = reaction code in §2.2; Attacker `+8` = reaction code of the original attacker in the counterattack round (−1 when not counterattacking)
- Defender `+0x18`: Counterattack 0; when not counterattacking, 1 (HUD displays "Defense") or 2 ("Evasion")
- Attacker's `+0x1A` = damage; to be knocked down, ≥ defender's `+0x22`, if not to be knocked down, < it; defender's `+0x1A` = counterattack damage, the same principle determines whether the original attacker is knocked down.
- Both sides `+0xB/+0xA/+0xC` = background (§6.5)
- The demonstration has been reseeded before calling `8009C2DC(1)`. If you want the same lines every time, you can use a fixed seed at the end of the package to re-seed `800821B0`.
4. **Return**: `D_80161310 == 0`, after the performance mode 0x1D → `801CAB50(2)` returns to the title; the host sees the "Appreciation" mark and the title main status returns to the 2/3 time-clear mark, and reopens the appreciation panel (retaining the last selection).
5. **Abort**: Any key (`D_80178A08 != 0`) in mode 0x1C will fade out, just like "press any key to return". The existing X abort (`battle_animation_probe.hpp`, set to state 21) will also work; its map-side replay (state 24 substate 4) will not trigger because the map overlay is not present. If you want to allow pressing A to advance the line without exiting, you need to block the judgment of 0x1C+ in the `801C9710` package (for example, only temporarily clear `D_80178A08` before calling the `801C9778` section), and wait for the actual machine to confirm which word is read when A advances the line.

**Why not use other methods**:

- Hidden mini-level: You need to install maps, units, and scripts, and you also need to run map settlement and `801FCA78` to write the roster. In the end, you have to overwrite the settlement to force it; and it takes more than ten seconds to enter and exit.
- Directly switch to mode 2: It can be used, but `801C9BD4` does not fill in the war participation record in mode 2 (the host must write it before switching). At the end, press `D_8015DD60` to select 0xB/0x10 (return to the map). You must use another hook to change the return mode; Z+START abort will go `800A5138` → Mode 7/0x11. The return path for 0x1C is ready.
- カラオケ mode 0x1A: There is no HP window and HUD, and it can also draw lyrics and play karaoke, so it is not suitable.

**Archives and rosters will not be touched**: This path does not adjust `800A5138`, does not run the map, and does not adjust any SRAM writing routines; the performance only writes the battle record area and its own BSS. Only `800F97E0..800FA868` is rewritten by the host.

## 6. Compare Z appreciation page (`assets/reference/battle-viewer-zsp.jpg`)

Reference picture: left "counter" (counterattack/defender), right "attack", middle △ swap; each side: big picture of the machine + avatar, machine name, pilot name, weapon name (with tags such as ALL), "HIT: Screen Through Defense ＜★★＞", terrain row "Track Elevator (4)"; bottom ♪ BGM row, explanation bar, "Battle Start" button; pop-up menu Project Settings/BGM Settings/Vibration/End.

| Z control | Does SRW64 have | How to |
| --- | --- | --- |
| Attack/Reverse sides, △ swap | There are: two battle records, `D_80178C78`/`D_80178B50` determines who attacks first | Swap = swap the selection of both sides, the attacking side is fixed at side 0 when writing the record |
| Body, pilot | There are: `+4`, `+2` (capability record number). The driver only affects the lines (`80222B14`, check the ROM `0x1161C0` according to the ability record number) and HUD | Any combination can be played; lines that do not match the original combination are still the driver's common lines |
| Weapons (tags like ALL) | Have: `+6`. SRW64 does not have ALL attack/support attack (only support defense) | The list is based on the body weapon table; the tags can continue to use the Library's grid/shooting/P/B/MAP tags. TBD if MAP Arms' show will be available to stream here |
| The weapon of the counterattacking party, whether to counterattack | There are: Defender `+6`, `+0x18` | When "No counterattack" `+0x18` Choose 1 (defense) or 2 (avoidance), only change the HUD label |
| HIT line "Screen Penetration Defense" | Partial correspondence: screen = shield blocked (code 2/3/4/5); Penetration = shield penetrated to reduce damage (0xD/0xE/0xF/0x10); Defense = S defense (0x11, shield). There are also those not listed in Z: miss (0x16), clone afterimage (0xC), cut out (0x12/0x13), aid (0x14), fake body (0x15) | Make a "Defender's reaction" single choice: hit/avoid/clone/cut/shield/shield block/shield breakdown; support and avatar require the host to create another instance of the machine, so don't do it yet (§7) |
| Damage ＜★★＞ | SRW64 has no classification, the damage is a number: `+0x1A` for the attacker, and the blood deduction is divided according to the weapon | Change it to a numerical value or three levels of "light injury/serious injury/down" (converted according to the defender's HP); a separate switch for "down" is more intuitive |
| Whether to shoot down | Yes: `+0x1A ≥ 对方 +0x22` → Status 22, explosion script 156/157/158 Select by body | Switch; weapon 0x4A6 Never explode (original rules) |
| Terrain "Track Elevator (4)" on each side | There are: `+0xB/+0xA` (+0xC) on each side, switch to the other side when firing | One background menu on each side; see the name below |
| ♪ BGM | Performance overlay does not select songs: full overlay does not call `8007E810`, only calls `8009003C(0/1)` (it is inferred that the sound effects channels on both sides are stopped). In a normal game, the song played during battle is the song played before entering the battle (presumed to be a level song) | The host plays `8007E810(歌号)` before the battle; the track list uses 49 songs with the title サウンドセレクト (`D_801CB290`), and the song names remain in Japanese |
| Vibration | Vibration package support for SRW64 has not been studied | Not done |
| Project Settings/End | Host Side | RmlUi Menu |
| Description column, start of battle | Host side | |

### 6.5 How to choose background

There are about 2366 valid background records (`D_800C5940` 32 groups × 101), and there are no ready-made names. Suggestions: ① Use `check_battle_backgrounds.py` offline to render a thumbnail for each used (a, b); ② Name the map "which chapter uses it" - `+0xA/+0xB`. The map path comes from the battle table. `+0x27/+0x28`, written by plot, can be statically inferred from the map data of each episode (to be done); ③ First, give a hand-selected common table (universe, city, sea, base, air b=100, etc.), and put all the lists in "More".

### 6.6 BGM

`8007E810(歌)` starts playing music (`80090128`'s karaoke is also passed through it); mode 0x1C returns when `8007E87C(0xB4)` (inference: fade out the music). Therefore, the selected song is played before the appreciation battle starts, and the original version will fade out when returning to the title.

### 6.7 Original combat BGM and mirror Shisui weapon conditions (static)

2026-10-03 Static analysis (disassembly of `build/recomp/cpu-scan/load_000AB160/rom_801C2600.text.s`, resident `build/recomp/disasm/cpu-main`, the table is directly decoded by ROM), not actual machine. "Confirmation" = the code and data have been read; "inference" = the semantics or timing have not been followed.

**Correction §6 table ♪ BGM row**: The battle song is not the "level song before entering the battle". It is true that the performance overlay does not select a song, but the map overlay has already changed the battle song after the battle is settled and before switching to the performance (confirmed).

#### Play function and song selection function

- `8007E810(歌号)` (confirmation): do nothing when the song number is equal to the current song `D_800FFA6C` (the same song will not be restarted); negative number → `80077B38` stop, `D_800FFA6C = -1`; otherwise `80077868` starts and is recorded in `D_800FFA6C`.
- **Battle Selection = `801E085C(句柄A, 句柄B, 单方)`** (confirmed). The handle is split into (camp, slot) via `801E510C`: `0x42–0x5F` our side 0, `0x60–0x7D` enemy 1, `0x7E` starting from third party 2; body instance = `D_8015E10C[阵营×0x258 + 槽×0x14]`, body number = instance `+2`, main pilot = instance `+0x38`, character number = driver `+2`. Finally, `801E07C4(ROM 地址, 模式)`: Mode 0 uses `80089970` to borrow the buffer, `8007F704` reads 2 bytes from ROM as the song number; mode 1/2/3 directly puts `0xD`/`0xB`/`0xA`.
- Caller (confirmation): `801C90F4` (`801F7D6C(攻, 守)` immediately after settlement `801E085C(攻, 守, 0)`; called by `801C9604`, `801CD664`), `801D3140` (`801D3240`: `D_80172EE2` Action unit versus target, one side = 0), `80211DA4` (script `3D49` forced combat, `80212154`, one side = 0), `801D3278` (`801D33A0`, one side = 1, same function as single settlement `801FE068`, inferred as MAP Weapon/unilateral action), `8020ECE0` (`8020EE3C`, unilateral = 1, purpose not pursued). Because the song is selected during the map process, the song will also be changed when the battle animation is turned off (inference, not actual).

#### Rules (confirmation)

Two-party mode (one-party = 0), in order:

1. The main pilot character number of A or B is **33–35 (0x21–0x23: ヴァル＝ア, アヴィ＝ルー, ジェイ＝レン)** → Song `0x22` "Crazy Hungry Warrior", regardless of other conditions.
2. Otherwise **A is our side** → use A; **otherwise B is our side** → use B. That is to say, as long as one of the parties is our side, the song of our station will be played, regardless of offense or defense - our units that are beaten during the enemy phase will still play their own theme song.
3. Neither party is our side (enemy vs third party) → Use A’s **body surface** song.

Unilateral mode (Unilateral = 1) only looks at A, without step 1: Our side → Our side rules below; Not our side → Unit table.

**Our unit's song**: Read main pilot `+0x1C` (mental bitmap, bit 30/31 = Hyper Mode/Shisui/V-MAX state, see [battle-formulas.md](../gameplay/battle-formulas.md) Hyper Mode section).

- `+0x1C & 0xC0000000` is 0 → **Character table** (by character number).
- Hard-code the machine number when setting: Machine 2 (ゴッドガンダムH)→ `0xA` "Mikyo Shisui"; 4/10/12/14/16 (シャイニング／マックスター／ローズ／ドラゴン／ボルト's S form)→ `0xB`「burning the upper part of the story」; 270/273/2 77／278（ニューレイズナー、レイズナー、ガッシュラン、ザカール）→ `0xD` "V-MAX"; other units (such as the Maxi S 28, the ノーベルガンダムB 7, the battleship fleet and the silver bell are only set to 30) → still use the character table.
- We never check the machine table; the enemy and third parties never check the character table.

**No** branches based on plot variables, levels, and Boss signs (`801E085C` only reads the above fields); the Mingjing Zhishui variable 45 does not affect the song selection, and the "Mingjing Zhishui" song only follows the H form (bit 30).

#### Two tables (confirm)

| table | ROM | index | item | description |
| --- | --- | --- | --- | --- |
| Character song | `0x7D6A0` | Character number 0–360 | s16 × 361, to `0x7D971`, followed by 0 | 63 items are −1 (soldiers, NPCs, unused characters; put −1 = stop playing). Value range −1, 1–9, 12, 14–29, 34, 37 |
| Airframe song | `0x7DF30` | Aircraft number 0–362 | s16 × 363, to `0x7E205`, then 10 bytes 0, `0x7E210` onwards is the airframe weapon table | None −1. Value range 1–12, 14–23, 25–29, 34 |

Specification example:

| Object | Table | Song Number | サウンドセレクト Row: Song Title |
| --- | --- | --- | --- |
| Unit 1 ゴッドガンダム | Unit | 4 | 3：FLYING THE SKY |
| Body 2 ゴッドガンダムH | Body (our side uses hard coding, the same value) | 10 | 9: Mirror Shisui |
| Mechanism 97 ザクⅡ | Mechanism | 1 | 0: 兰の中で光いて |
| Unit 196 コン・バトラーV | Unit | 20 | 19：コン・バトラーVのテーマ |
| Unit 50 νガンダム | Unit | 7 | 6：メインテーマ |
| Character 4 ドモン | Character | 4 | 3: FLYING THE SKY (change to `0xA` when in H form, `0xB` when in S form) |
|Character 36 アムロ|Character|7|6：メインテーマ|
|Character 70 シャア |Character | 7 | 6：メインテーマ |

Therefore, "Our アムロ fights the enemy's ザクⅡ" and "The enemy's ザクⅡ fights our アムロ" both put メインテーマ; when the enemy's ザクⅡ fights the third party, put "岚の中で光いて". Grouped by works: character table 2 = Z series, 3 = ZZ series, 8 = W series, 37 = "Where do you go from here?" (レジスタンス, ゲリラ, etc.); body table 12 = all レイズナー series (including enemy aircraft), etc., can be decoded directly according to the table above.

#### Song number → サウンドセレクト OK (confirm)

Title overlay `load_0010DA50` (VRAM `801C4500` = ROM `0x10DA50`) of `D_801CB290` in ROM `0x1147E0`, 49 × {text number u16, song number u16}; text number 232–280 consecutive, song name = text 232 + Line number. Song number and line number:

- song `0x01–0x20` → row = song number − 1 (rows 0–31);
- Song `0x30`, `0x31` → Lines 32, 33 (日こそ我が时、明あるlimitり);
- song `0x21–0x2F` → row = song number + 1 (lines 34–48).

Every song number that appears in the two battle tables is in these 49 rows, so the appreciation page can directly use this table to make the song title (reverse search: search for rows in the table by song number). The カラオケ table `D_801CB354` (ROM `0x1148A4`, 19 items) is a subset.

#### Other curve-changing points on the map (confirmed, use part inferred)

- **Level song = map resource record `+0xB`**: `D_80219B27 + 地图号×12`, that is, ROM `0x10267C + 地图号×12 + 0xB` (the one with "last byte to be interpreted" in [original data directory](../data/original-data-catalog.md)). 158 pictures only use `0x23`, `0x2A–0x2F`. Where to put it: Tactical entry `801E028C` (mode 0x11, etc.) / `801E0350` (mode 0x16), **Start of each phase** `801FA88C`, `801C7798` (after waiting 60 frames for a certain state), `801E076C` (see below).
- **Level songs will not be restored after the war**: The performance return map is in mode 0xB → `8008029C` → `801E0268` → `801E00AC(1)`, and the whole process will not adjust `8007E810`. Therefore, the battle song remains on the map until the beginning of the next stage (`801FA88C`) or the song is changed in the next battle (inferred player body perception, code path confirmation).
- Script `3D3A` puts BGM (`8009F9D0`: parameter 0 → `8007E87C(0xA)` fades out, otherwise `8007E810`).
- `3D45` appears `8020C524(0)`: non-first round, `D_802237F5 ≥ 2` (meaning not pursued), current appearance handle `D_802272E0` is released when it belongs to the enemy `0x26`「これが実力か」(inferred as enemy reinforcement jingle); every frame `801E076C` finds that the current song is `0x26` and `80077AD0()` returns 0 (inference: it has been played) and then changes back to the level song.
- Other fixed songs: `801C72C8` plays `0x27` "いざ戦わん" (inferring preparations for sortie); `801DF444``0x28`, `801DF8A8``0x18`, `801DF280`/`801DF5BC`/`801DFD04` First `8007E810(-1)` stops (ending/game end sequence, not pursued); `802176A8(k)` press k to play `0x14`／`6`／`0xE`／`0x17` After cutting mode 6, `80212CC0` fades out or plays `0x17` according to parameters (the purpose is not pursued).

**Appreciation Page Usage Suggestions**: The default song is calculated according to the original rules - if there is a friendly player, take the character song of the main pilot of our unit (if you choose the H/S/V-MAX form, use the hard-coded song above), otherwise, take the attacker's body song; if there are three people present, the default song will be `0x22`.

#### Meaning of Weapon ROM `+8` (required skill) = 2 (confirmed)

- Copy: `800A6A68` Write the weapon ROM record `+8` into the weapon instance **`+0xF`** (instance step size 0x24; ROM `+0xF` flag byte into the instance `+0x22`, don't mix the two).
- Judgment: **`801E6214(阵营, 主驾驶员, 武器实例, 机体实例, 跳过消耗检查)`** returns 0 available, 1 necessary skills not met, 2 insufficient power (`+0xE` > pilot `+0x20`), 3 insufficient EN (`+0xD` > body `+8`), 4 number of bullets. 0 (`+0xC ≠ −1` and `+0xB == 0`); necessary skills are judged first. Caller `801E6410` (status page weapon list `801E6650`, details `801E6B0C`), `801F8B38`/`801F8DB0` (`801F8BA0`/`801F8EB8`), `80200530` (`802008E0`), `80201D98` (`80201E68`), all passed to the body `+0x38` is the **main driver**.
- `+0xF` Press jump table `jtbl_8021EBF0` (17 items, subscript value −1):

| Value | Condition (returns 1 if not met) | Display text (0xFBA + value) | Weapons used in ROM |
| --- | --- | --- | --- |
| 0 | None | — | Most |
| 1 | Faction = 0 (only us can use it) | Do not display (details will only be displayed when ≥2) | 79 Mandala Formation·Jiyue Rebirth |
| **2** | **Main pilot `+0x1C` bit 30 (`0x40000000`) has been set** | "Dingjing" | **15–19** |
| 3 | Same as 2 | "HP" | None |
| 4 | Same as 2 | "Sモード" | 30, 53, 62, 71, 76 (The four-machine S form of the alliance between the SャャイニングS and the Sシャッフル alliance) |
| 5–11 | Driver level `+5` ≥ 10/15/20/25/30/35/45 | 「LV10」…「LV45」 | 150–159, 1177–1183, 1219, etc. |
| 12／13 | Skill `+0x36 & 0x18` (NT or Enhanced Human World) and level `+6` ≥ 1/4 | "NT1" "NT4" | ファンネル category／ファンネルMAP category |
| 14/15 |
| 16 | Bit 30 | "V-MAX" | None |
| 17 | Position 31 (V-MAX Red Power) | "V-MAX" | None |

- **So `+8 = 2` only requires the main driver's status bit 30**, the code is exactly the same as `4` (Sモード), `16` (V-MAX), "Dingjing" just displays text. **Don't read** Plot variables 45. Don't read `800A4BB8`, and don't look at strength or skills. `800A4BB8` There are only three callers in the full ROM, `load_0008F4B0:801CA27C`, `801E59D0`, and `801E5BE8`, all of which just add the text "Ding Jing Shisui" to the ドモン skill bar; there are no variables to read in `801FF1BC`/`801FEDF4`.
- Source of bit 30: `801FF1BC` (called by `801D61C8`, `801D92E4`) for our ドモン (andアルゴ, サイ・サイシー, ジョルジュ, チボデー; Eastern Undefeated Any camp) Vigor ≥ 130 → `801FEDF4`: In the form table `D_80218A34` (ROM `0x101594`, line 0 = {1, 2}) finds the current body, changes the body number to the enhanced form and sets the bit 30. For ゴッドガンダム, this step is 1 → 2 (H). Bit 30 is only cleared during the crash process `801FF4E0`, and does not fall back with the force.
- In addition, the form slots of weapons 15–19 in the body weapon table (`0x7E210`) are only for body 2, and the list of body 1 does not originally contain these 5 items; position 30 is the second door. Actual effect: **The driving and strength of **ドモン can only be used after it automatically changes to H**, and has nothing to do with the "Shisui Shisui" plot variable 45 (45 only determines the skill bar text and the シャッフフル Alliance's killer line, see [hidden-elements.md](../gameplay/hidden-elements.md) §5.1). The subsequent strength thresholds are as usual: 15 none, 16/17 ≥ 110, 18 ≥ 130, 19 ≥ 150 (ROM `+7`).
- For the appreciation page: the performance path is not adjusted to `801E6214`. You can directly fill in 15-19 for the war participation record, without worrying about position 30 (inference: the performance overlay does not read this field).

## 7. Risks and Limitations

- **Aid (0x14) and False Body (0x15)**: `801C3E7C`, `80222B14`, `801E40B0` will read the real airframe instance through `+0x106C` (and its `+0x38` pilot pointer); in the demo, these two pointers point to placeholders `D_8016A210`, the content is not guaranteed to be valid. To do this, the host must create a body instance in free memory (+4/+6 HP, +8/+A EN, +0x38 points to the created driver instance, driver +2 = character number). Not available in the first edition.
- **`8022245C`'s conditional lines**: 0x1388–0x2710 This section (level-specific, lovers, etc.) is only judged in the previous mode `D_8015DD60 == 3` (map), and will be interpreted as `+0x1064 → +0x38`; when viewing the title mode, this section is skipped, and only general lines are displayed - safe, but not exactly the same as the lines in the main story.
- **Prop map of Shield and Kiriruり払い**: The reaction record shows that the actor registration number on 17/18/19 is 17 (it is inferred that the shield/sword parts were obtained based on the local atlas). Selecting these two items for a mecha without a shield/sword may result in empty or wrong parts. The appreciation page should only be provided when the aircraft has corresponding equipment slots (ROM aircraft record +0x18 equipment slots, Library has resolved "shield").
- **Keys**: Mode 0x1C, any key is aborted; touching the joystick on the Deck does not count, it depends on the source of `D_80178A08`, wait for the actual machine to see.
- **RNG**: Appreciation does not affect any save content; line selection changes with frame count, fixed seed if necessary (§5 step 3).
- **Coexists with X abort hook**: `battle_animation_probe.hpp` hangs in `801C9710`, appreciation does not need its map-side logic; confirms that it does not read map variables like `D_80172EB0` when there is no map overlay.
- **HD Replacement**: The performance scenes are drawn in the same set as the main story, and the HD replacement of the body rendering, cut-in, and ground textures will take effect naturally.
- **Widescreen**: `battle_hud.cpp` The overlay logic takes effect according to the performance overlay, does not rely on the map, and the inference does not need to be changed.

## 8. Code confirmation and inference

Code confirmation:

- Mode table, loading function and entry of mode 2/0x1A/0x1C (resident:11582, `jtbl_800CFEC8`)
- `8009C2DC`/`8009C218` Fill in all fields of the record and demonstrate the record format (resident: 43902-44200, ROM `0x83110` has solved 19×6 + 23 items)
- Title settings 0x1A (title:6181) and 0x1C (title:6805), title exit (title:7403), return entry `801CAB50` (title:7511)
- Performance reading `+6/+8` selected animation (battle:2011 `801C410C`), diversion of `801C3C9C`, performance number mapping of `800AB470` and table `D_800CB7BC`
- Full table of reaction codes and settlement sources (map:59196–59633), blood deduction conditions of `801C3E7C`, knockdown branch of `801C5AF4`, counterattack conditions of `801C7B5C`
- Background switching by side (`801C6FE8`, `801C76A0` → `801C2AD0`)
- Performance overlay is not tuned `8007E810`

Inference:

- The meaning of `+0xC` (empty bit), the purpose of `+0x17/+0x1E/+0x1068`
- `801CAB50(2)` is to return to the PRESS START/ring menu; `8007E87C(0xB4)` is to fade out the music; `8009003C` is to stop the sound effect channel
- Shield/cutting, the actor presses the machine to get the prop parts
- The BGM in normal battle is the song before entering the battle.
- The additional overlay for `80400000` has nothing to do with the show

## 9. To be verified on real machine

1. In the title main state 2/3, the host calls `80080188(0x1C)` + `80099814(5,1,2)` whether the performance can be entered cleanly (whether the title substate should be advanced like `801CA254`, otherwise the title will still respond to input during the fade-out period).
2. After the `8009C2DC` package is overwritten, can any combination (airframe, driver, weapon) be played normally? Select a few weapons covered by `D_800CB7BC` to check the animation.
3. The screen of each reaction code: hit, 0x16, 0xC, 0x12, 0x13, 0x11, 2/4 (block), 0xD/0xF (penetration); for a machine without shield/sword, choose 0x11/0x12.
4. Downed: `+0x1A ≥ +0x22` Time advance state 22, three explosion scripts; weapon 0x4A6 does not explode.
5. Counterattack round: When counterattacking, `+0x18 = 0`, the original attacker's `+8` and the defender's `+0x1A` are as expected; when `+0x18 = 1/2`, the HUD label.
6. Switching timing between different backgrounds on both sides.
7. Which title screen will you stop at after returning to running mode 0x1D? Can the host reopen the appreciation page there? Are there any resource leaks (elf slots, heap tag 4) when playing more than ten games in a row?
8. BGM: Whether the song `8007E810` before the war is played all the time during the performance and whether it fades out when returning; whether the sound effects channel during the performance interrupts the music.
9. Whether pressing A to advance the line in mode 0x1C is equivalent to aborting; X/R2 aborts the performance of the hook in this path.
10. Are the widescreen, HD replacement, and interface text overlay (HP window body name) normal in the demo path?

### 9.1 Prototype actual test (2026-10-03)

The host prototype has been connected: `resident_func_8009C2DC` packaging (`NATIVE_HOOKS` → `srw64_original_demo_battle_fill`, `game_hooks.cpp`), frame boundary hooks `viewer_start`, `src/host/battle_viewer.cpp` (debugging command `viewer.start`: the original fields of the combat records on both sides are written, the status is `status.battle_viewer`). The test script records (ROM `0x71B80 + 机体×0x24`: HP, EN, size bits) and `D_800CA9C4[人物]` calculation fields by body. Conclusion:

- Items 1, 2, and 7 passed: the title ring menu is idle (intro major 3 / substate 2, `D_801CC3A6` 2/3) time-switching mode 0x1C clean entry; overwriting takes effect after the original version is filled in (ゴッドガンダム "石波ラブラブ天星剑" 1216 Play ザクⅡ, cut-in 1023, HD frame normal); after the performance, return to the title "Please press the START key" screen (not the ring menu), there is no abnormality for 9 consecutive fields, and then `previous_mode` is 0x1D. After returning to the title, leave it for about 6 seconds and the original version will start the standby demonstration by itself. Please block it when the appreciation page is opened.
- Items 3 and 4: Hit (damage divided into blood points), avoidance 0x16, clone 0xC ("Clone" text + afterimage), S defense 0x11 ("Shield Defense", α・アジール without a shield is also displayed), shield blocked 2 ("I force field", no blood deduction), shield penetrated 0xD ("I force field" + blood deduction), knockdown (damage ≥ HP, explosion) are all played according to the record. Cut り払い 0x12 For α・アジール without a sword, it just does not deduct blood, does not wield a sword and has no words - the first version is only open to sword-wielding mechas.
- Item 5: When the defender reaches `+0x18 = 0`, the HUD displays "Counter", and the counterattack round itself is not intercepted and needs to be filled.
- There are also problems with overlapping words and residual words in the line display (which may occur in both demonstration paths and normal battles), which are related to incremental redrawing of dialogues. They should be checked separately and are not part of this function.

### 9.2 Finalization of the appreciation page (2026-10-03)

- The layout is designed according to the canvas (Design artifact "Combat Appreciation Interface Design"): "Reverse" on the left (the body diagram and avatar are flipped horizontally to the right), two cards for "Attack" on the right, three rows of grids, and two result areas "Reverse and Attacked / Attack and Counterattack" below; the height of the card is calculated according to the window (panel 94% is reduced by 270 dp, 150–400 dp). `viewer_*` of `src/native/ui/frontend.cpp`.
- Reactions are open according to the original conditions (`viewer_gate`, based on battle-formulas.md): shield = body equipment 2 + pilot S defense; cut off = equipment 1 + pilot cut り払い + incoming weapon `& 0x08`; shield = aura (requires holy warrior) or I force field/beam coating/planetary defense (incoming weapon) `& 0x02`); clone = ability `0x163011`. Shield damage of 0 means blocking (code 2/3/4/5), and greater than 0 means penetration (0xD/0xE/0xF/0x10); the clone code is 6-0xC according to the ability level. The Library data has been supplemented with `equipment_bits`, `ability_bits`, weapons `flags`, and pilot `skill_bits`, and additional weapons (486 out of 120 units) that are only in the modification table have been added to the weapon list. Weapons list removed MAP weapons.
- The damage will leave the opponent with 10 HP by default; counterattack is enabled by default, the defender's counterattack weapon defaults to the strongest one, and the attacker defaults to the last weapon. The attacker's reaction code in the counterattack round is written as `+8`.
- The pilot only lists people who can fly the machine (`tools/content/battle_viewer_pilots.py` generates `src/host/battle_viewer_pilots.inc`: level deployment record (removing the stand-in with a record value of 3), のりかえ category, the form of the same weapon table and the super mode table), ensuring that the lines are originally written for this pair.
- BGM defaults to the original rules of §6.7 to take the attacking side song (pilot table, H/S/V-MAX form is hard-coded, and the body table is used when there is no pilot song).
- Incidental correction verified by actual machine: in wide screen, the left and right blocks of the cut-in black frame only cover 4:3, instead branch `800C6D00` to a copy of `807FFF00` in each frame, and use gEX rectangular alignment to extend the left and right blocks to the edge of the screen (`battle_hud.cpp`; the script injection temporary area is shrunk to 0xFF00). The HD full-frame image follows the original in-place palette effect (Shisui Gold, Flash on Hit): if the palette is different from the ROM, two sets of palettes (up to 256 colors) are used to recolor the pixel-by-pixel lookup table and a variant is cached in the asset table. When not ready, the original sprite (`native_sprite.cpp``recolor_pixels`, upper limit 256 sets) is displayed.

### 9.3 Selection Page (2026-10-03, superseded by 9.4)

In the first version, the aircraft, pilots, BGM, and scenes were each made into a full-page card grid; the pilot page also had an "All Pilots" tab. If you select a pilot who cannot activate the current aircraft, you can replace it with his default aircraft. 2026-10-04 Changed to the single-page approach of 9.4, and these two points were removed. The following practices are carried over to 9.4:

- Default pilot: Take the combination that appears the most in the level deployment (`battle_viewer_pilots.inc`).
- BGM is grouped and auditioned by works.
- Scene thumbnail: Enter the `scenes` section (`cutin_hd.py scenes --bind`) of the HD package `battle_sprites`, and the host uses `sprites::viewer_scene_image` to get the picture.
- The title has two standby timers, which are reset when the page is opened or when the battle is waiting:
- `D_801CC390`: Enter the demonstration battle after 180 frames of standby;
- `D_801CC3A4` (u16): "Please press START" and the standby time on the ring menu exceeds 0x385 frames, and enters the opening scene of main state 12 through `801C9BF8`.

### 9.4 single page (2026-10-04, imitation Z appreciation)

A canvas "single page solution" was built into the game (`viewer_*` of `frontend.cpp`).

- **One page**: There is one card and five rows of grids on the left "Counter" and the right "Attack".
- On the card are the body diagram, avatar, HP → remaining HP, and a thumbnail of the scene on this side is laid out on the back.
- The five elements are the body, the pilot, the weapon (the opponent is a counterattack weapon), the result of the attack, and the scene.
- The hit result line is written as "Hit > Normal·Damage 6690 (remaining 10)", and the three small marks "Shield/Cover/Cut" behind it light up when this side is available (Z's "Screen Through Defense").
- Below is the BGM line; the bottom line explains the current selection, and on the right is closing and combat start.
- **Selection Box**: Click on a line, the selection box covers the other half (the BGM box covers the opposite side), and this side remains visible.
- Whichever item the cursor stops on, it will be immediately changed to that item: the card, grid, and BGM line will change accordingly, and the card will be marked "Previewing".
- Save a copy of the current state when opening the selection box: "Return"/B to put back that copy, "Decide", A or click the same item again to retain it.
- List maintains scroll position when refreshing page.
- **Select the aircraft first, then select the pilot** (Z order):
- The body frame is paged by works ("◀ Work n / N ▶" at the top of the frame, use L / R or the left and right keys to turn the page, and turning the page will preview the first page of the new page).
- For the selected aircraft, if the pilot selected when the selection box is opened can be used, it will be retained. If it cannot be used, it will be replaced with the default pilot of this unit.
- The pilot box only lists people who can pilot the current machine, with "current" and "default" marked.
- Selecting a pilot does not change the aircraft, so the "default aircraft for each pilot" is no longer needed, `battle_viewer_units.inc` and the part of the code that generates it have been deleted.
- **Hit Result Box**: According to Z, it is divided into two columns.
- The left column is the result: hit > normal / shield / shield, miss > avoid / clone / cut off, write the reason why it cannot be used; there is also "no counterattack / counterattack" on the top of the attacker's side.
- The right column is damage: 10 left (default), large / medium / small (25% / 50% / 75% left), knockdown, plus ±100 / ±1000 fine-tuning.
- **Scene Frame**: Divided into four tabs: "All/Ground/Air/Universe" (air=air, different space, universe=universe, moon). When changing tabs, the current scene will not move in the new tab, and will preview the first one in the new tab.
- **BGM box**: The attack songs are at the top, grouped by works below; press C← to audition (the X key on the Deck), and moving the cursor during the audition will change songs.
- **Operation**: Press the direction keys to move to the nearest button, and the left and right only move in the same line; when the selection box is open, only move within the box.
- **Real machine verification** (1280×800 window, extra large interface):
- Body frame preview: God Gundam → Extreme Star Gundam, the pilot is replaced by Chipodi, the weapon is replaced by a giant magnum, and the "shield" is lit; the entire page is restored after B.
- R Turn to the new Mobile Suit Gundam W, preview Wing Gundam and Hiro, and the BGM line will change to the attacking song.
- Select "Small damage" as the result of the attack, and the HP display will be 6700 → 5025.
- The aerial tab of the scene frame and the grouping of BGM frames by works are normal.
- After the battle started, Wing Gundam and Hero were used.

## 10. Interface

The appreciation page only uses RmlUi (`src/native/ui/frontend.cpp`, the only UI toolkit for the project; system interfaces such as AppKit are not used). The layout refers to the left and right columns of Z. The style follows the final draft of the pre-war confirmation page: beveled edge (`slant` decorator), top page label, large body diagram, and large font size; the layout is based on the Steam Deck "extra large" interface (same as Library), and the offline audit `run_audit.py` needs to cover the new page. New entries enter `content/locales/*.json` and register `UI_KEYS` of `src/srw64_native/profile.py`. The debugging interface follows `ui.click --id …`.