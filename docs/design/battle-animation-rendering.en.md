> **Language / Ngôn ngữ:** [English](battle-animation-rendering.en.md) · [Tiếng Việt](battle-animation-rendering.vi.md) · [中文](battle-animation-rendering.md)

# Analysis of combat performance rendering mechanism

2026-09-30. Static analysis (disassembly + ROM data table, no new probes added) for the finalization of widescreen adaptation and the establishment of HD version of the battle performance. The state machine, suspension and settlement are in [battle-animation-skip.md](../native/battle-animation-skip.md), and the part that has been done for widescreen is in [deck-16x10.md](deck-16x10.md) Item 8/13; this article will not repeat those contents. Anyone writing "inference" has not yet verified it with actual machines.

Address convention: combat overlay `load_00121560` resides in `801C2600` (ROM offset = `0x121560 + RAM − 0x801C2600`); the rest are resident segments.

## 1. Overview: overlay I hardly draw anything.

Only 5 RDP command words appear in the entire battle overlay (`FF`, `F6`, `FA`, `B6` and the static list of the masking strip). The body, special effects, sky, ground, and HUD are all drawn through the resident **Sprite/Node Engine**. Therefore, there is no need to change the display list of the overlay in both widescreen and HD. You only need to modify several renderers and matrix routines of the resident engine. This is consistent with the path that has been taken between maps and fields.

The picture of a performance is composed of four layers, from back to front according to node priority:

| Layers | Implementation | Painter | Notes |
| --- | --- | --- | --- |
| Sky/starry sky | Elf slot 0/1 (second layer 3/4), mode 2 | `80095974` | 32×32 block TEXRECT, wrapped modulo 320×240 |
| Ground | 3 blocks × 3 layers 3D model node (resource display list) | Node type 2 | x = −1000·s / 0 / +1000·s, perspective projection |
| Body, weapon special effects, cut-in, explosion | Scene sprite, mode 0xE/0xF/0x10 | `8009761C` | One G_QUAD per part with 4 vertices, subject to node matrix transformation |
| Rolling special effects layer (speed line, flowing cloud) | Slot 0x19, mode 2 | `80095974` | `801C3610(kind, speed)` is created, also modulo 320 |
| HUD (HP window, gauge, number, avatar, dialogue box, mask strip) | Mode 9/7 sprite, text engine, static list `80222D50` | `800945D4``8009B74C``801C2C98``8008EB5C``800964E4` | Already provided by `battle_hud.cpp` welt |

## 2. Data resources

The decoding code is in `src/srw64_native/battle_graphics.py`, and the export directory is `assets/original-graphics/` (`battle-scenes/` 321 picture gallery previews, `cutins/` 15 groups, `animations.json` three animation libraries).

### 2.1 Scenario Triplet

Each drawable is a (scene, atlas, palette) triple, a 6-byte item:

| Table | ROM | Number of items | Reader | Purpose |
| --- | --- | --- | --- | --- |
| `unit_poses` | `0x84E40` | 365 | `8009C864` | The basic posture of the body (it is also used in the large pictures on the inter-field page) |
| `battle_scenes` | `0x11E3D0` | 1053 (1051 valid) | `801C3170` | Performance registration form: body movements, weapons, special effects, cut-in (984–1038), explosions |
| `chapter_titles` | `0x84B20` | 133 | `8009C8EC` | Not related to combat |

Scene resource = step sequence (frame number, number of frames) + frame table; one frame is a number of 16-byte parts {flags (0x10 horizontal flip), s, t, w, h, x, y, vertex offset}, `vertex_mode` 0 8 vertices per part (normal 4 + mirror 4), 1 only 4, 2 none. ROM statistics:

- 1051 scenes, 3905 frames, 34130 parts; 99% of the parts are 32×32 (33779 pieces), the rest are 16×32, 24×32, 8×32, etc., up to 40×40.
- vertex_mode: 0 has 965, 1 has 84, 2 has 2.
- 527 pictures in the atlas: 303 pictures of type 5 (CI4, 16 colors), 179 pictures of type 7 (CI8), 45 pictures of type 6 (CI8), totaling about 27.1 M pixels (CI4 16.8 M, CI8 10.3 M). The first 4 u16s are {type, width+1, height+1, 0}. Common sizes are 64×32, 96×32, 64×64, 96×160, 512×512 (large album of 11 pictures).
- 611 palettes: 333 of 32 bytes (16 colors), 185 of 256 bytes (128 colors), 54 of 128 bytes, 35 of 224 bytes, 4 of 1184 bytes (592 colors). CI8 can only index the first 256 colors. For the extra parts, see §5.4 Palette Animation.
- The largest scene canvas (bounding box of all frames) is 64×32, 32×32, 64×64, 96×96, 128×128, 128×96.
- **A total of 18398 different part slices (atlas, palette, s, t, w, h)**, of which 391 are used for the basic posture of the body. This is the order of magnitude key for the "replace by texture hash" route.

### 2.2 Weapon animation record (not bytecode)

Three libraries (`ANIMATION_BANKS`): `weapon` 1329 entries (by weapon number), `hit` 159 entries (hit_script in the weapon header; 156–158 is the knockdown), `reaction` 28 entries (defender reaction code). Reader `801C3128`/`801C31E8`/`801C3230`, DMA window 0x3C0 bytes.

One record = the first 4 s16 {camera 0–3, hit_script, action, defender_action} + sound effects list (≤8, ending with 0xFFFF) + cast list (≤24, 16 bytes per item: battle_scenes registration number, x, y, z, h4, h5, h6, behavior). behavior is an index into the behavior jump table `80225030` (389 entries, 294 different routines, see §6). ROM statistics: camera mode 1 accounts for 905 entries, 0 accounts for 405, 2 only 17, 3 only 2; the number of actors is 1–12, 2 is the most (472 entries); weapons reference a total of 815 different registration entries.

There are two additional 7×s16 tables: Aircraft Combat Log `0x118610` (354 rows; +1 sprite scaling percentage, +2..4 shield sprites, +5 additional scenes, +6 explosions) and Weapon Combat Log `0x119970` (1329 rows; dialogue weapon number, contact type, hit pattern, phase code).

### 2.3 Background record (ROM `0x5BC30`, 0x26 bytes one)

`8008422C` read; index `80084A78(a, b, side)`: record number = `D_800C5940[a]` (ROM `0x50330`, 32 items → group 0–0x17) × 101 + b, a/b from combat record +0xB/+0xA (infer b is map number). Approximately 2366 items are valid.

| Offset | Meaning |
| --- | --- |
| +0 | Type; when 1, create a gradient/fog node of side+0x25 slot (callback `8009BCC4`), +1..+7 is the color → `D_8010F5B7..BE` |
| +8 / +0xE / +0x14 | Three ground layers {kind u8, ?, resource u16, parameter u8, ?} |
| +0x1A / +0x1C / +0x1E | Sky kind (0 none; 2 common; 5/6/8/9/10 rare), sky resources, secondary resources (inferred to be palette) |
| +0x20 / +0x22 / +0x24 | The second sky layer (slot 3/4), only 14 are used |

Example: Record 20 (Makoto Z vs. ザクⅡ that map) Ground (1,5701) (1,5652) (1,5653), Sky 6092/6170; Record 87 (Space) Ground (1,5683) (6,5684) (1,5685), Sky 6109/6216. When the sky is kind 9 (resource 6104 starry sky), replace the first piece of ground with resource 5840.

HD Asset range to be replaced: Sky 6067–6115 (Sub assets 6116–6224), Ground models and textures 5584–6066, Starry sky 6104/5840, Scroll layers 3186/3190/3191 (Sub assets 3455–4747).

## 3. Elf and node engine

### 3.1 Record layout

- **Slot header** `800FFA70 + 槽×0xC4` (300 slots): +0 mode, +1 valid, +4/+8/+C xyz (f32), +10/14/18 scale, +1C/20/24 rotation (rad), +28/2C/30 Only read by motion routines (inferred to be speed, not entered into the matrix), +0x50 (`800FFAC0`) camp/mirror bit.
- **Subrecord** `800FFAA4 + 槽×0xC4 + 子×0x30` (3 per slot): +0 valid, +1 alpha, +4 node pointer, +8/9/A mode category bits, +C/E/10 raw resource number, +12/14/16 scene/gallery/palette **handle** (`80089E9C` allocate, `8008A11C` get address, handle table `80160340` 20 bytes per item: +2 ROM resource number, +0x10 data address), +18 remaining frames of this step, +19 current step, +1A animation flag (bit0 single, bit1 stop; `801C5328` passes 2 = manual stepping), +1C mirror bit, +1E..+2A palette effect record. The +0xA/+0xC/+0xE/+0x11 of `800FFAAC + …` written elsewhere in the document is the +12/+14/+16/+19 here.
- **Node** (0x6C bytes, pool `80163630`, chain head `80163638`): +0 priority, +1 low 2 bits type (0 static display list, 1 callback, 2 image) | 4 hidden | 8 shadow toggle | 0x10 shadow | 0x20/0x40 alignment, +C callback, **+14 Floating point 4×4 matrix**, +64 slots, +68 subs. `8008B614` is inserted in ascending order of priority, with equal values ​​inserted before existing ones.

### 3.2 Build Elf

`80098158(槽, 子, 模式, 优先级, 场景, 图集, 调色板, 动画标志)` is the shell of `80097C68`: press `jtbl_800D0530[模式−1]` to select the painter, and then `8008B4F4(槽, 子, 模式, 优先级, 4, 1, 节点标志, 绘制器)` to create the node. `80098204/80098590/80098604` Change the scene/atlas/palette respectively (release the old handle and allocate the new handle).

Schema table (the part this article is concerned with):

| Mode | Painter | Node Flag | Usage |
| --- | --- | --- | --- |
| 2 / 4 | `80095974` | — | Chunked TEXRECT, position +4/+8 rounded, with alpha: sky, scroll layer, interfield background |
| 7 | `800964E4` | — | Avatar |
| 8 / 9 | `800945D4` | — | 16×16 grid TEXRECT, no alpha: HUD box, badge |
| 0xB / 0xC | `800975A4` → `80096CD8` | — | One TEXRECT per part (screen coordinates, no scaling) |
| 0xD | `8009751C` → `80096CD8` | — | Same as above, y minus z |
| 0xE | `80097D94` → `8009761C` | 0 | Quad, translation + scaling + rotation around Z/Y/X |
| **0xF** | `80097D1C` → `8009761C` | 0x20 | Quad, after translation + zoom guAlign towards the camera (billboard) - body and most special effects |
| 0x10 | `80097D58` → `8009761C` | 0x40 | Same as 0xF, aligned with y/z components only |

Construction method in battle: `801C50D8` (actor) checks `800C9C6C` through `8009C130` to get the type byte and priority (default 0x9A); type 0x90/0x93/0x9C → mode 0xB (screen coordinates TEXRECT, inferred to be cut-in, subtitle type), the rest → 0xF; `8009C18C` hits `800C9C40` table → 0x10. `801C4160` (body of the machine, slot marked from +0x95) and `801C5328` (slot 0x9A) are fixed to 0xF. Shadow built by `801C28E0` at sub-1, atlas 0x1580/palette 0x1581, going `8009C004` → `8009BD68` LOADBLOCK.

**Scale**: `801C34D8` → `801C30D0(id, 1)` Take the percentage of the body record ÷100, and write +10/14/18 for the three axes.
**Mirror image is not vector flip**: The camp bit of `800FFAC0` is written by `801C55FC`/`801C7D40` (`801C5280` takes negative x at the same time); `8009761C` is in vertex_mode 0 and when this bit is set, the vertex address is +0x40, that is, the second group (mirror image) of 4 vertices stored in the part is taken. The 84 scenes of vertex_mode 1 have no mirror group.

### 3.3 Matrix: unified calculation in one place

The renderer `8009761C` **does not issue G_MTX itself**. `8008261C` (`801C9BA8` adjusted at the end of each frame) traverses 300 slots

- `800B4090` identity matrix → node flag 0x10 (shaded) `8007EA10` translation (x, 0, z) + `8007EA64` scaling (1 − y·0.003); otherwise translation (x, y, z), scaling (sx, sy, sz).
- Mode 0xE then `8007EE8C/EDC0/ECF0` rotates around Z/Y/X (+24/+20/+1C).
- Mode 0xF (flag 0x20) is left multiplied with guAlignF `800B31E0(0, 旋转 + eye − at)` by `800B3CC0`; 0x10 (0x40) uses only the y/z component.
- The result is written to node +14. When drawing `8008AE90`'s `8008B324` uses `800B3F50` (guMtxF2L) + `DA380003` (MODELVIEW LOAD, not pushed on the stack).

**Projection**: `800883FC` = guPerspective(`800B4430`) fovy **50°**, aspect = `D_8010F5C0 / D_8010F5C2` (320/240, from resolution table ROM `0x51320`, written by `8008BF60`), near **20**, far **3000** → `D_8015DCAC`; then guLookAtReflect `800B3C48` (eye `D_8015DDFC..`, at `D_8015DDF0..`, up `D_8015DE14..`) → `D_8010F71C`. Node flag 8 changes when `800885B4` LOAD perspective, then `80088580` MUL view. The viewport `D_800C6950` (ROM `0x51340`) is only filled in once by `8008C1D4(sx, sy)`/`8008C390(tx, ty)` when `8008C1AC/1B8` is initialized. Combat overlay does not change the viewport.

**No Z buffer**: `E200001C 00000000` at the beginning of the frame, the renderer does not send E2, the context depends entirely on the node priority; z is only affected by perspective division.

### 3.4 Texture loading (once per part)

Atlas header u16[0] type 5/0xE → CI4 (`F0 0703C000` holds 16 colors), otherwise CI8 (`073FC000` holds 256 colors); palette from +8 RGBA16. Per part: `FD` SETTIMG (width = atlas width) → `F5` tile7 TMEM 0 → `F4` LOADTILE (s,t)-(s+w,t+h) → `F5` tile0 line=(w+8)/8, word1=0 (no mask, no clamp)→ Two `F2` (first (s,t)-(s+w,t+h), then covered by (0,0)-(w,h), vertex UV relative to the part) → `E3000C00 80000` perspective correction, `D7 FFFF`, `07000204/406` G_QUAD. CI only uses TMEM 2 KB lower: CI8 ≤ 2048 texel, CI4 ≤ 4096, so the vast majority of parts are 32×32. When alpha is not 0xFF, change CC to `FC119623/FF2FFFFF` concurrently `FA` prim alpha (`8009768C`).

### 3.5 Per frame sequence

`801C9D84` registers `801C9710` (updated) with `801C96F4` (drawn → `8008AE90`). `801C9710`: `801C9DAC` (input) → state table `80222DD4[D_80250000]` → `80098880` (300 slots each run `80098738` step sequence: +18 and reduce to 0 step; when the step number is reached, bit0 is set to bit1 and stopped, otherwise skip loop_step) → actor script `801C9404/801C8F4C` → `8008261C` Calculate the matrix. `8008AE90` clears the screen at the beginning of the frame `F6`, three lights `DC08`, `8008AD40` sends `gSPViewport(D_800C6950)`, `gSPClipRatio(1)`, `800883FC`, and then draws them in ascending order of node chain priority - **regardless of slot number and z**.

## 4. Lens

The camera does not move the relationship between eye and at, but "the sprite moves towards the target point and the at point follows":

- `801C9BD4` (from 801C9C04) initialization: distance `D_8015DE2C` = 260, pitch `D_8015DE08` = 2.4°, azimuth `D_8015DE0C` = 0, at.y `D_8015DE24` = 32, at.z = 0, x position of both machines ±800 (`D_802501F8/80250210`). Each frame `801C9BA0` adjusts the resident `800816D8`: eye = at + spherical coordinates (distance, pitch, azimuth), and recalculates up. `801C76A0` (801C7804) A certain state resets the angle to 2.4°/0. The amount of shake `D_80178D44/D48` (resident `80088650…` written) is stacked into x at `801C9AE0`.
- Target point `D_80250228/22C/230`: `801C6224` writes initial value from show record (+0x24 camera mode, +0x54/58/5C initial target, +0x7E orientation) and synchronizes at.x/at.y; `801C685C` at the end of each frame `D_80250228 += D_80250240` (x speed) and puts at Write as target value. The four camera modes are selected by the processor via `801C67EC`: 0 → `801C63BC`, 1 → `801C64D8` (illegal values also take it), 2 → `801C6584`, 3 → `801C6678`; they read the tracked handle (+0x894 of participant 0 = `D_800FA074`, mode 3 first follows +0x78 = `D_800F9858`), writes −2× direction to +0x20, and registers `D_80250220` (slot)/`D_80250252` (orientation) via `801C637C`. Inference: The only difference between the four modes is who to follow and whether to broadcast `801C63A8` first.
- `801C9DD0(a0)`: a0 is the handle of +0x78 {+0 slot number, +0x32 orientation} in the war participation record (`D_800F97E0` + idx×0x1074), and the call point is `801C7F78/801C8120/801C81F4`. It moves the slot toward the target at a speed of (target − position)/8 (write +28/2C/30, x plus 2×orientation), |dx| < 3 returns 0, which is "camera in place" for state 21, etc.
- Swap sides `801C7E1C` only exchange `D_80178C78`↔`D_80178B50`, reposition sprites (`801C40E0`×2, `801C39B0`×2) and then adjust `801C685C`; **No matrix mirror**, left and right are all ±800 The position and orientation bytes are determined (inferred).

## 5. Widescreen: Status Quo and Remainder

Already done (2026-09-29/30, `deck-16x10.md` Article 8/13): The sky is drawn twice more at ±320, the 3D viewport is no longer centered (the ground, body, and special effects are expanded with the viewport), the masking strip is left blank, and the HUD is bordered. According to this analysis, remaining hardcoding risks:

1. **Projection aspect comes from 320/240** (`800883FC` read `D_8010F5C0/C2`). Now the extended viewport of RT64 is being relaxed, the geometry itself is still calculated as 4:3, and the extra parts on both sides are the originally cropped parts, which is exactly what is wanted; as long as `D_8010F5C0` is not changed.
2. **Scope of ground model**: 3 blocks × 1000·s (template scaling 1.0 or 1.5, ROM `0x5A988`), eye distance 260, fov 50°, near 20 hours 16:9, field of view about ±(260+z)·tan25°·1.78, inference is enough; but a single ground of <5608 (only The outer edge of 1 node) and 9-node splicing may be exposed at 21:9 or when the camera is zoomed out. Please check the actual machine picture by picture.
3. **Scrolling special effects layer** `801C3610` (slot 0x19, mode 2) is modeled at 320 the same as the sky. The current ±320 repaint is only hung on "`80095974` during combat" - if the repaint is filtered by slot, slot 0x19 needs to be included (to be checked `host.cpp` No. 434 conditions near the row).
4. **Second sky layer** (slot 3/4, 14 records) uses the same renderer, which should have been covered, but has not been implemented in the actual machine.
5. The **cut-in mask** is the four black rectangles programmed with 320 in the resident static list `800C6D00` (§6.3): the upper and lower blocks will be filled up by RT64, and the left and right blocks (0,45)-(90,165), (230,45)-(320,165) will only cover the middle 4:3, after widening, the performance screen will be exposed on both sides, and the left and right pieces must be recalculated according to the width of the screen (the window remains centered). The cut-in image itself is centered with the camera x and does not need to be moved. The actor type 0x90/0x93/0x9C in mode 0xB (screen coordinates TEXRECT) in `801C50D8` has not been matched yet, and it is also centered at 4:3.
6. **Full-screen rectangle**: There are 4 `F6` and 2 `FA` (flash, mask) in the overlay. The RT64 "full width rectangle" rule has been covered; if there is a flash drawn by (0,0)-(320,240) in the behavior routine, it will be filled in the same way, see §6.
7. **Screenshake** is the 3D displacement superimposed on at.x and does not need to be processed after relaxation.

## 6. Behavior routines and screen effects

### 6.1 Actor Behavior Routines

- **Table**: `80220C0C(behavior)` Use behavior − 3 to check `jtbl_80225030` (valid 380 items, behavior 3–382; subscript ≥ 0x17C and the last 9 items belong to `802219A0`). Each item is a 12-byte thunk and returns the real routine; `80221988` (shared by 95 items) is the **empty slot** of `v0 = 0`. It gets NULL when loading, and `801C5BAC` is skipped. 284 valid routines. ROM `0x21AE0C` has a list of editors during the development period. Only high-end editors can match it (359 Stay, 362 Shield, 367 CoverDiffence, 375 BeamShield, 379 Dummy). It is inferred that they are leftover from different versions.
- **Calling Convention** (`801C5BAC(block)`): Actor records 0x50 bytes, in block+0x9C+i×0x50, quantity block+0x26; when phase byte block+0x25 contains 0x40, or actor+0x2E == 4 (first frame) `jalr *(+0x4C)(a0 = 演员)`, the return value is ignored. There is no frame-level frame count, each routine uses +0x44 (205 routines), substate +0x3C, auxiliary +0x3E/40/42. Fields: +0 elf slot, +2 alignment, +8/C/10 base xyz (z constant flag), +14/18/1C accumulated displacement, +20/24/28 speed (accumulated per frame), +2C registration number, +32 direction ±1, +34 h4, +36 activity, +38 mode (1/3 = absolute coordinates, otherwise superimposed host sprite +4..C With its speed +28..30), +3A h5 → sprite +0x35, +48 phase byte pointer.
- **Classified by the auxiliary functions used** (one routine can belong to multiple categories): position/speed `801C6038` 136 (including 14 using sinf/cosf); relative host distance `801C32D4` 44. Find companion actors `801C58E8` 16; scaling (writing sprite +10/14/18) 21; flip `801C3BE0` 67; show and hide `801C37FC/3840` 274; sound effect `801C355C` 188 (`8008FFAC` 10); change scene `801C5700` 232. change atlas/palette `80098204/590/604` 51; write phase byte (trigger hit Script/Concatenation) 273; camera following `801C637C`/cancel `801C63A8` 16; whole screen flash `801C9520/95CC`, `8009AC84` 41; sprite palette effect `801C963C` 38 (mode 4 has 73, 1 has 32, 9 has 9, 3 has 4, 2 has 3, 6 has 1); background hidden/restored `801C3C40/3C64` 23. Background overload `801C28E0` 17; damage beat `801C8DFC/8A44` 9; derived subroutine `80220C0C/801E4668` 13; defense elf `801C4574` 3; cut-in 5; end(`sb 0, 0x36`) 279. Represents: `801E4E20` shooting standby, `801EB410` beam, `801E6064` timing, `8021F5A4` shield, `8021FB4C` support, `80220734` explosion.

### 6.2 Full screen effect

- **Fade/Flash** is a resident 3-layer record `D_800FF9D8 + 16n`: `8009AC84(层, 类型, R, G, B, 目标 α, 间隔, 步长)` writes, `8009AFCC` steps per frame (type 1 `8009AD64` α stops after approaching target; type 2 `8009AE9C` Automatically hidden after one or two frames, inferred to be flashing), `8009A954` drawing: SETCOMBINE + `FA` PRIM + **`F65003C0 00000000` ie (0,0)-(320,240) hard-coded FILLRECT** (ROM `0x25358–0x2536C`), node priority 0x9D/0x83/0x9B. Shell for overlay: `801C9520(层, 白?, 目标 α, 步长)` white/black gradient, `801C95CC`/`801C94A0` layer 1 black α250 type 2. The full width rectangle is filled by RT64 and widescreen is covered.
- **Block**: `801C2C3C` uses `8008A5C4(0x85, 4, 0, 0x00222D50)` to register the static list, which has been made empty by `battle_hud.cpp`.
- **Shake**: There is no random shake in the overlay; the scroll origin `D_8015DDF0/DDF4` is only written by `801C2600/32D4/6224/685C/7494/840C`. The first analysis shows that `801C9AE0` superimposes the resident `D_80178D44/D48` into x. It is inferred that the vibration amount left by the map script (3D36) continues in the performance. It will be confirmed by the actual machine whether it is really effective.
- **The flash when hit is not the whole screen, nor PRIM**: `801C87C8` When hit, the tone is `801C963C(演员, 0, 颜色, 模式 4)`, the color is RGBA5551 (white 0xFFFF, red 0xF801, blue 0x3F) → `80099C88` changes **the sprite's palette** (mode 1 = changes to another palette resource, such as 0xBB4; mode 4 = full color replacement), while `801C94A0` triggers layer 1 black flash.

### 6.3 cut-in

Not special mode, **regular actor**: Registration number 984–1038, behavior 240 `801FBE3C` (37 places), 350 `80211378`, 351/352, 373 `8021F3C0` (h6 = 2 for control, 14 weapons). Display after equal phase == h4, change scene to this registration item, sprite scaling 1.29, mode 1 absolute coordinate x = `D_80250228` (lens x, center of screen) y = 47 (constant in `801FBE5C`/`8021F3E0`); write phase 0x56 after animation is played. There is no sliding code, and the animation effects are all in the scene frame. When actor z == 1 `8009C68C(0x35)` → `8008B4F4(…, 0x8E, 0x000C6D00)` hangs a resident static list (RAM `800C6D00`, ROM `0x516F0`): black FILLRECT (0,0)-(320,45), (0,165)-(320,240), (0,45)-(90,165), (230,45)-(320,165), **Leave a 140×120 window**; `8009C6C8` removed. The picture is a 128×96 sprite (55 scenes, 27 atlases, including large atlas type 6 512×448), not a full-screen image.

### 6.4 Down

State 22 `801C818C`: Body record `801C30D0(unit, 6) == 2` (30 units) select hit 156, otherwise +0xD of `801C49A0` == 2 → 157, otherwise 158; `801C84C0` loading; phase 0x56 release/hide sprite, 0x57 return to state 0x15. All three scripts have 7 actors, behaviors 382 `80220734` (`801C6038` flying, `801C95CC` black flash, `801C963C` changing color), explosion scenes 1042 (128², 11 frame), 1043 (192²), 1044 (176²), 1045 (192×176). `801C9DD0` Let the downed aircraft move 1/8 closer to the center of the camera every frame. Explosion = sprite + whole screen flash, no vector graphics.

### 6.5 HP Bar and Damage Beat

Queue `D_80250270` is created by `801C8A58` (status 1 `801C70A8`/14 `801C7FC4`) by weapon record [5] check `D_80222E50`. `801C87C8(0x45, 0x45)` is adjusted by the state processor every frame: phase 0x45 and `D_80250488 == 0` start, `801C8D04` pops up one step → `801C8D6C` writes the undetermined value to display HP (combat record +0x22, inferred), flash defender, black flash; the routine can also be `801C8DFC` Advance (5 places), `801C8A44` sets `D_80250490 = 200` (presumed to be digital timing). `801C2C98` (`801C728C` registration) draws 88-wide bars at +0x22/+0x20 per frame: x 44–132/184–272, y 29–31 (const ROM `0x121C0C–0x121E30`), already bound by `battle_hud.cpp` with HP windows.

## 7. HD route evaluation

Both candidate routes do not need to touch overlay:

### 7.1 RT64 texture hash replacement (like map body icon)

- Key: TMEM content of LOADTILE once per part (including the used TLUT items). 18398 different slices; different color palettes (friendly and enemy colors) in the same atlas count as different keys. RT64 v5 hashes contain TLUT, this is verified on the icon.
- Advantages: No need to reproduce any transformations, the matrix, mirror, alpha, and priority are all original; widescreen follows naturally.
- Difficulties:
- **Seams**: Parts are independently sampled at 32×32. After the HD image is multiplied 8 times, the bilinear clamps are clamped at the edges of the slices respectively, and thin lines will appear at the joints (the problem of puzzle seams has been encountered on the world map). To add 1–2 pixels of adjacent block content to the HD slice for padding, cut the whole frame according to the master when exporting.
- **Palette animation** (§5.4, `8009A358` rewrites the palette data every frame, `80098604` changes the entire sheet) will cause the TLUT hash to change frame by frame, and the affected sprites must have a key for each state, otherwise it will flash back to the original image. It is necessary to first count which registration items have palette effect records (sub-records +1E..+2A).
- The same applies to the 4 special effects of the 592-color palette.
- Applicable to: the body of the machine, most weapon special effects, and explosions.

### 7.2 Host whole frame drawing (like avatar, title image)

- Already have the foundation: `resident_func_8009761C`'s host wrapper and `native_sprite.cpp` by sub-record +12/14/16 handle identification (scene, atlas, palette), read +19 current step approach.
- Need to reproduce on the host: node +14 matrix (**just read the memory directly, no need to recalculate `8008261C`**), perspective `8015DCAC` and view `8010F71C` and node flag 8, mirror bit +1C/`800FFAC0`, alpha +1, step → frame → Assembly of parts, priority order (replacement occurs at the original node position, naturally order-preserving), palette effect (just read the current palette data, and the entire frame is recolored).
- Advantages: One HD picture per frame, no seams; palette animation can be remapped on the host according to the current TLUT; the drawing can be larger than the original canvas (special effects expansion should be restrained, see [[srw64-hd-effects-keep-footprint]] for lessons).
- Difficulty: One frame must be identified by (scene, atlas, palette, frame number), 3905 frames × color matching; the quadrilateral under perspective must use the same projection as RT64 (the existing mode 14 title image is already undergoing matrix transformation and can be reused).

### 7.3 Suggestions

- The body and special effects go first **7.1**: Fast output, zero risk, return to the original image, first use the ESRGAN formula (`unit-pose-hd.md` finalized) to enlarge the entire 527-image set 8 times, then slice it according to the parts and do padding; the sprites of the palette animation are eliminated first, and then finalized after statistics.
- Sky, ground textures, starry sky walk RT64 hash + sky can be generated by external expansion (same method as inter-field background `background_wide.py`).
- Cut-in (55 scenes, 27 atlases, canvas 128×96, about 165×124 after zooming 1.29) and explosion (4 scenes) go **7.2**: a small number of large pictures, no concerns about palette animation, the whole frame image quality gain is the greatest; cut-in mask frame is recalculated according to the screen width.
- **Flickering when hit and color matching variants must be resolved first**: `80099C88` Mode 1 (changing palette resources) and mode 4 (whole color replacement) act on the sprite palette. Both routes must be able to recolor according to the current TLUT - the hash route is a key for each color state (white/red/blue × primary color), and the host route reads the current palette for mapping. First use read-only probes to count the number of TLUT states that appear in a typical battle before making a decision.
- If you want to change the geometry of the 3D ground model, follow the model replacement route of `native-model-replacement.md`.

## 8. To be verified on the real machine

- What are the types of actors in mode 0xB in `801C50D8` (0x90/0x93/0x9C).
- Whether the vibration amount of `D_80178D44/D48` actually causes displacement during the performance.
- Recalculation and actual effects after the cut-in mask frame is relaxed.
- Outer edge of ground 9 nodes at 16:9/21:9; level list for single ground (<5608).
- Whether the patch at scroll layer slot 0x19 is overwritten by the existing sky patch.
- List of registry entries covered by palette animation (just add a read-only probe to `80099C88`).
- The relationship between near 20 / far 3000 and the aircraft entry advance under the RT64 extended viewport (16:9 is about 54 units, observed).

## 9. Ground model mapping HD pilot (2026-09-30, city, real machine passed)

Scene: Background record 58 (block 0, terrain 58), ground 5836 (sea surface) + 5837 (buildings, cargo ships, docks) + 5838 (foreground layer), sky 6087. Use the `check_battle_backgrounds.py` method to write `800F97EA/B` (one copy on each side) in the `battle-ui` mini-level before starting the battle to force the background. Working directory `assets/hd-ai/battle-backgrounds/test-1` (do not enter git):

1. `run_battle_bg.py OUT 块 地形 --dump`: Run a game with RT64 texture dumps and note down the 180 new TMEM dumps that appeared after the war started.
2. `decode_dumps.py 5836 5837 5838`: Press `tile.json` to solve `.tmem` (CI4/CI8, two words are swapped every 8 bytes in odd-numbered lines, the palette is 8 bytes per item starting from 0x800), and compared pixel by pixel with the map solved by the model viewer. All 16 maps of the three models are matched one by one, and the hash is the key to RT64.
3. `upscale.py`: Expand 16 pixels according to the wrapping method of the texture (repeated tiling, pinched edge), then mix UltraSharpV2+PixelPerfectV4 in half, 4 times, crop back; pass through alpha again with transparency. Write a test package, list `art.json` (type temporarily borrowed `space`) and profile that only contains these 16 pictures.
4. `run_battle_bg.py OUT 0 58 --profile profile.json`: Actual screenshots of the same battle.

Results: The floor panes, cargo ships, and crane arms have become significantly clearer, and tile joints have not appeared; the sea surface texture is originally a smooth ripple, with little change. Sky 6087 is a 2D block map, which is not in this scope. It is still the dithering color block of the original version. It is more conspicuous behind the clear buildings, so it should be done together.

Official access is still lacking: `compile_art` has been added to the category whitelist (currently only worldmap/frame/space/icon); the keys of all 442 models can be calculated directly from resource static calculations according to the solution of `decode_dumps.py` without relying on dumping (`rt64_hash.py` already has CI4 64×64 algorithm, and needs to be supplemented by CI8 with other sizes), then use a small dump to spot check.

## 10. Ground model HD grid pilot (2026-09-30, city 5837, passed the actual machine)

The host changes (baked model, water surface shader) and modeling tools in Sections 10 and 11 have not yet been submitted and are only tested locally. The user rejected the practice of one 4096² baked map for each model and switched to tileable materials + vertex AO for mass production.

§9 Only the stickers are changed, but the building is still the same sticker. This section replaces the entire 5837 with a new grid and uses the native model of the world map ship ([native-ship-model.md](../native/native-ship-model.md)):

- **Recognition is established in combat**: Ground models and ships are in the same resource format (descriptor table + a type 0 model display list), and segment 4 is also set when the game is called; the list of 5837 only has triangle commands (227 items), without matrix switching and sublists. The host hits each frame, and each of the three splicing blocks (x −1000/0/+1000) is drawn once. The original draw is used for depth testing and depth writing. Press F6 to return to the original draw. First use the placeholder mesh converted from the original geometry to vertex color for confirmation, and then change to the official mesh.
- **The truth about the original model**: The "city" in the distance is a 1000-meter-wide low-rise texture board (z −500, y 17..77) plus two high-rise texture boards (z −475, top to y 147); in the near distance are the dock platform (y 26) and the quay wall, the white passenger ship "Yokohama Maru" and the black-hull work ship (door crane, red and white boom).
- **HD Grid**: Local Blender script `battle_city_blender.py` (does not enter the warehouse, see `assets/models/generators/`; Blender 4.3 runs headless, outputs `assets/models/battle-city/mesh.json`, does not enter git). 7.3 Thousands of triangles, vertex color: pier with quay wall joints, fenders, bollards, street trees, street lights; three rows of buildings (glass core of office tower + wall between windows on each floor + pilasters + roof equipment, balconies and railings on each floor of apartment buildings, strip windows of mid-rise office buildings) , the positions and heights of the two original high-rise buildings were retained; the two ships were reconstructed according to the original bounding boxes and hull outlines (passenger ship layered superstructure, window strips, lifeboats, chimneys, ship name text grid; operating ship door crane trusses, containers, deckhouses, red and white booms). Only build the +z plane and sides visible to the camera. Thousands of squares are merged into a small amount of bmesh according to color and then sent to Kit for export.
- **Packaging**: 5837 items are added to the model table of `build_native_models.py`; `--output build/recomp/native-models/battle-city-test`, `SRW64_NATIVE_MODELS` points to it (`test-1/run_battle_bg.py --models`) at runtime.

**Look and Feel**: The buildings have real floor undulations and front-to-back levels, there is parallax when the camera pans, and the details of the passenger ships and work boats are much more than in the original version. The host's ship coloring (vertex color + fixed key light) is grayer than the original map, and the buildings are denser than the original; the color and density have to be adjusted according to the bright white buildings of the original.

**The sky does not move model**: The sky is a 2D block image of Mode 2, and the same drawing function as the inter-field background is `80095974`; the whole image replacement of `native_background.cpp` is identified by the resource number of the sub-record (image, palette), regardless of mode, so the battle sky (this scene 6087/6145) only needs to make an HD whole image and register it into the background list. The sky is rotated horizontally at 320 degrees, and the HD image should be drawn so that the left and right sides are seamless, and both sides of the widescreen are covered by ±320 fill-in pictures.

**Amount of work to spread**: Most of the 442 ground models are ground panels and a small amount of scenery. The ones that are really worth rebuilding the grid are cities, ruins, bases, bridges, and forests with scenery (about dozens of resources), and the rest only have textures (§9). One resource requires a Blender script, which is about 400 lines long.

## 11. Baked lighting model and real-time water surface (2026-09-30, city, real machine passed)

**Not released yet** (2026-10-01 user: "Don't want this yet"): The host code is retained, and the packager `build_native_models.py` puts these three items in `BATTLE_BACKGROUNDS`. The HD package is not included by default. The battle background of 0.3.2 is still the original version; the local build `SRW64_BATTLE_BACKGROUNDS=1` is entered.

The vertex color mesh of §10 was rated as "not high-definition enough" by users: the host ship shading only has vertex color plus a fixed light, without textures, reflections, or ambient occlusion. Changed to two new pipelines:

- **Baked lighting model** (`shading: baked`): Local script `battle_bake.py` combines the parts of the modeling script into an object, assigns materials according to color names (glass is randomly lighted and darkened according to each pane, concrete and road noise, hull semi-gloss), adds Nishita sky and sun, deletes the back and bottom surfaces that the camera can never see, and uses Cycles after Smart UV expansion (Metal GPU, 128 samples, about 70 seconds) to bake overall lighting, shadows, skylight and reflections into a 4096² map. The mesh has 46,000 triangles, mesh.json v2 with uv and texture; vertex color alpha 200 standard glass. The host `HdBakedVS/PS.hlsl` directly samples the texture (mip, linear), and the glass is layered with a layer of sky Fresnel and highlight depending on the viewing angle.
- **Real-time water surface** (`shading: water`): There are actually two layers of water, 5836 is the flat surface, and 5838 is the wave layer covering the entire ground (y 3..14). The latter is the water you see. 5838 The mesh plane (y 6) generated by the packer takes over, 5836 set to `hidden` (triangles are all suppressed and not drawn). `HdWaterPS.hlsl`: The slope of 16 directional waves is synthesized as a normal line, the x component of the wave vector is 2π·integer/1000, and the three splicing seams are aligned; the dark water color and the sky gradient are mixed according to Fresnel, the sun is low in the direction of the city, forming a flash band; the distance is fogged to the horizon color; the time is taken from the host clock.
- **Host changes**: `native_marker.cpp`'s model adds `Shading` (colour/baked/water/hidden), vertex step size by type (28 or 36), textures are bound after uploading when first drawn; additional data for the water surface is the model view matrix and time. `native_gpu.cpp` Register HdBaked, HdWater. The packager `build_native_models.py` supports uv mesh, copy texture, and generate water surface mesh.

**Real machine** (`test-1/water2`, 1280×720 window): 5837, 5838 each draw 1389 times, 5836 all suppressed. The city is bright, with volumetric light and shadow, and the window panes are staggered in light and dark; the water surface has dynamic ripples, sky reflections, and flash strips. Still the original: 2D sky image (replace the entire image in §10 with HD in the next step), body and special effects sprites.

To be adjusted: the position of the flash strip (the direction of the sun is a fixed assumption), the choice between the deep water color and the original saturated blue, and the aerial perspective of the distant buildings.

## 12. The combat body was replaced with the existing HD rendering and underwater perspective (2026-09-30, the actual aircraft passed)

**Unit**: The scene triplet used for the main body of the aircraft in battle is the same as the large body image on the page (`unit_poses`). It is single frame and drawn according to the scene boundary. The existing HD vertical painting (`unit-poses/whole-v1`, 8 times, 332 pictures) can be directly replaced. The whole frame replacement of the scene sprite of `native_sprite.cpp` was originally hung on the quadrilateral renderer (used for the title picture), identified by (scene, atlas, palette, frame), and used the game's matrix to draw the entire picture; now `configure` reads `srw64-units-hd.json` in the art package at the same time, and each picture is registered as frame 0. The original mirror is to take the second set of vertices of the part. When replacing the entire image, the flip is judged based on the S coordinates of the leftmost and rightmost vertices of the part. When flipping, the UV left and right are swapped. This list already exists in the official HD package, so no additional resources are needed and it will take effect in normal games; F6 returns to the original version.

Actual machine (`test-1/units`, `pairs`): MINUEP ォー (2365/1765/2065) and ダンバイン (2438/1841/2141) have been replaced, and the size and orientation are consistent with the original version at the same time.

Not covered:
- The same machine with different color palettes: 11 sets of the same (scene, album) with multiple color palettes in `unit_poses` (such as ギラ・ドーガ 91/315, バウンド・ドック 105/317/318) each have HD Standing posture; バストール The solved diagrams of 2953 and 2144 are identical pixel by pixel and have also been covered. 5 color-changing registrations in `battle_scenes` are only used for weapon performances (2026-10-02 static verification): 675/676 (Mascuit series "锔 Dance・Reappearance Jianghu デッドリーウェーブ", weapon 111/120, red and orange), 862 (ヴァルディスキューズ「スピリッツクラッシュ」1248, blue), 863 (アヴィエスレルム「オ"メガクラッシュ" 1253, eye color change), 864 (スーパーアースゲイン "Explosive Ax Unparalleled Break" 1177, blue), is an afterimage/doppelganger (behavior) of the overall color change 314;272 7 each, h5 50–230 increments), derived in §13 "Global color change or glow" and packaged with `unit_extras` (palette 2997/2998/2992/2993/2994). Therefore, all color variations of the body's stance have been covered. **Color change review (2026-10-02)**: Some of the pure color change diagrams derived based on color ratios are blurry and missing details (the block lines of eyes, gems, and MASK 2997/2998 turn to olive green), and are changed to the color lookup table: `unit_extra_derive.py``PALETTE_SWAPS`／`palette_swap` Select the most common target color for each stance color where the original frame overlaps with the stance. Each HD pixel is weighted and changed according to the colors of the last 4 stances. Places where the stance is present but not in the frame are removed with a soft-edged mask. Currently used for 8 sheets: マスターガンダム 2997/2998 (original color matching 1935), ゴッドガンダムH gold 2485, スーパーアースゲイン2901, アヴィエスレルム 2928, ヴァルディスキューズ 2934, ヴァイローズ purple 2862, スヴァンヒルド 2809. For those with new parts (the gun barrel of Masukura S 2758, the missile bay of Sagittarius 2802), the parts will be lost when looking up the table, and the original derivation will still be followed. In `unit_poses`, each of the 11 groups of multi-color stances were enlarged with ESRGAN, and compared group by group with the "Brothers Color Lookup Table": the existing versions are better (there are often multiple pairs of one-to-one color palettes, and the white version of ズワァース, ガンダムmkⅡ will have wrong colors when looking up the table) and will not be changed.
- The additional pictures of the machine body (props, second posture, combined parts, § "Body Drawing" totals about 300) and weapon special effects are still the original ones.
- Flash white when hit: Mode 4 rewrites the palette in place, and the HD image does not change color; Mode 1 changes the palette resources, and those frames are not recognized and fall back to the original version.

**Underwater perspective**: The original water has two layers - 5836 opaque plane (y 0) and 5838 wavy layer (vertex alpha 178, no depth, y 3..14). The submerged part of the body is between the two layers and can be seen through the wave layer. §11 Make the water opaque and hide 5836, so the underwater part is gone. Now both layers use the water surface shader: 5836 opaque, 5838 mixed according to the original alpha (more opaque according to Fresnel at glancing angle), and the legs of the body can be seen through the water on the real machine.

## 13. Classification and derivation of additional body diagrams (2026-09-30)

For the pictures in the body atlas other than the standing posture, remove the prop parts and align and compare the standing postures one by one according to the game coordinates (`assets/hd-ai/battle-backgrounds/unit-extra-analysis.json`, `method` fields):

| Processing method | Quantity |
| --- | --- |
| Directly reuse stance | 6 |
| Overall color change or glow | 11 |
| Afterimage or decomposition effects | 8 |
| Standing posture + floating cannon flying out | 2 |
| Partial changes (standing + patching one piece) | 47 |
| The whole new picture | 16 (two of them are the same, the actual picture is 15) |

A total of 27 pictures in the first four categories are derived from HD stance by `tools/hd_ai/unit_extra_derive.py` (output `assets/hd-ai/unit-extras-derived/`, 111 frames): pixel by pixel judgment "same stance → HD stance" "same position color change → HD multiplied by color ratio" "new pixels not in stance → original image enlargement" "empty → transparent"; the overall luminescence of a single tone is changed to "standing brightness → "Target Color" mapping table; the afterimage first estimates the lateral misalignment row by row. There is no separate mirror image drawn, the left and right orientation depends entirely on changing the vertices. The entire 15 new pictures are made into the image_gen generation package `assets/hd-ai/unit-extra-imagegen/` (original picture, HD stance with the same color for style reference, prompt words one by one, README). 47 partial changes and prop parts have not yet been processed. The 15 pictures (chest, arms, fists) that were once classified as "partial color change" were tested to "whether the same color in the standing posture always corresponds to the same color in the new picture". The consistency is only 23-59% (the true color change is close to 100%). They are actually redrawn and have been incorporated into local changes.

## 14. Access HD package (submitted on 2026-09-30)

- Art list `content/art/stage1-hd.json` adds `unit_extras`, pointing to `assets/hd-ai/unit-extras-derived/pack` (`unit_extra_derive.py --pack` generation: each frame is cropped according to the range of the parts it actually draws, and the transparent parts are filled with the nearest solid color, index `unit-extras.json`, schema `srw64.unit-extra-images.v1`, 96 frames).
- `compile_art` Compile it into `srw64-unit-extras-hd.json` and `unit-extras/`; publish and compress `compress_hd.py` in the same way as the body rendering, reduce it to 6 times, and decompose JPEG+alpha PNG.
- Host `native_sprite.cpp`: Read `srw64-units-hd.json` (frame 0) and `srw64-unit-extras-hd.json` (by frame number), and use the shared `presentation::load_rgba` (JPEG+alpha of the release package) for decoding; the original image is judged and flipped according to the part vertex S; there is no quadrilateral sprite in the HD image. `scene-sprites.jsonl` Make a note of `no image`.
- Actual machine (Mac, normal play profile): The log loads 332 vertical paintings and 96 frames of derivation graphics; in the battle-ui mini-level, ミニフォー, ダンバイン, and ゴッドガンダム are all replaced. The extra frames derived did not appear in these battles (they are only used when performing specific weapons). They were only compared offline and have not been seen on the actual machine.

**Orientation correction (2026-10-01)**: Initially, the mirror image was judged according to the S direction of the vertex of the part, but 134 of the 316 stances (mostly enemy aircraft) were stored upside down, and each part had a flip mark (0x10). When drawing normally, the S was reversed, so it was mistakenly judged as a mirror image, and the HD image faced the wrong direction. Change to accurate judgment: the vertex address of the quadrilateral is equal to "scene data + part vertex offset" which is the first group, plus 0x40 is the mirror group (`vertex_set`). The HD of the actual デスアーミー(restore) and ダンバイン are in the same direction as the original version at the same time.

## 15. Additional images of the aircraft body image_gen, cut-in, props, ground textures (2026-10-02, completed offline, not actual machine)

**Extra body image image_gen access**: Generate package `assets/hd-ai/unit-extra-imagegen` (62 pictures: 15 new pictures, 47 partial changes, see `selected-manifest.json` for the selected version). Accessed by `tools/hd_ai/unit_extra_imagegen.py compose`: use `portrait_matte.matte_portrait` to register each picture and cut out the original frame outline into an 8x master (55 The default threshold is passed; the overall size of 01, 03, 07, and 08 deviates from the original image by 2–8%, and the redrawn parts of 17, 18, and 24 deviate from the original image, and are relaxed to `RELAXED = (0.09, 20, 9)` and then checked manually); for local changes, use HD stance in the gray area of the marked image, and obtain the draft in the red area, and feather it by 1 original pixel; the remaining frames of the multi-frame animation are used with `also` scenes. `derive_frame` is derived from a drawn frame. The results are merged into `unit-extras-derived/manifest.json` with `method: image_gen`, `unit_extra_derive.py` A full rerun will retain these entries. 196 frames in the package, including 100 frames in image_gen.

**cut-in** (§6.3, registration 984–1038, 55 scenes 308 frames, deduplication 208): `tools/hd_ai/cutin_hd.py` Rendered frame by frame, cut to part bounding box, enlarged with ESRGAN formula of body stance; full frame replacement is the same as the body, the host only reads one more index. The face has only 6-20 original pixels. ESRGAN will fabricate the facial features (1029 five figures with palms raised into a ball), and redraw it by image_gen according to the **whole picture in the atlas**: the cut-in frame is cut from the parts of the picture that is completely stored in the atlas (translation, several characters gathered together are the same picture to change the position), so `tools/hd_ai/cutin_imagegen.py compose` redraw the 10 After registering and cutting out the images, they were pasted into the 8x atlas, and then all involved frames were reconstructed according to the original parts list (stacked in order, flipped horizontally at 0x10), for a total of 36 frames. 1029 f24 stacks 5 eye patches (15×7 pixels) from other places, omit them first during reconstruction (`OVERLAY_LIMIT`), and generate package No. 16 to add the eyes separately. Close-up of big face (1000, 1009, 1022, 1023 close-up, 1034, 1037) ESRGAN fits the original image without redrawing.

**Prop Parts**: Registrations other than standing poses, extra pictures, and cut-in in the body atlas (289 scenes, 431 frames, 394 deduplication; `cutin_hd.prop_registries`), amplified by the same recipe, packaged with cut-in.

**Index and size**: cut-in and props share the `battle_sprites` of the art list (runtime `srw64-battle-sprites-hd.json`, schema the same as the extra image `srw64.unit-extra-images.v1`, host `native_sprite.cpp` loaded). The full frame image that only appears in battle is packaged in `PACK_SCALE = 5` (body scaling 80–110%, cut-in 129%, 3.2–5.2 screen pixels per native pixel at default 4x internal resolution), the 8x master remains in `hd/`; the body stance is still 6x published (displayed enlarged on the page).

**Ground model texture**: `tools/hd_ai/battle_ground_hd.py` Don’t run the game, statically calculate RT64 v5 hash from ROM: simulate RDP loading according to the display list (dxt odd line change/LOADTILE/LOADTLUT four copies of SETTIMG/SETTILE/SETTILESIZE/LOADBLOCK) to get 4 KB TMEM, and then follow `rt64_tmem_hasher.h` Version 5 hash (sampling width and height takes the smaller of the texture size and mask, TLUT only hashes the items used, and the tail is width/height/tlut/line/siz/fmt). §9 All 16 real-machine hashes of the pilot are reproduced. There are 424 ground models with a total of 1419 textures. After expanding by 16 pixels in a wraparound manner, ESRGAN is 4 times larger. The texture package written into RT64 is `battle-<hash>.png`, and the art list category is `battle` (`compile_art` whitelist has been added). Noise textures (grass, hay, gravel) appear as brush stroke textures when enlarged, which is acceptable to users.

**ESRGAN speedup actual measurement** (M4 Max, cut-in 4 frames): bfloat16/float16 is 1.3 times faster, and only PixelPerfectV4 is used for the transparency channel, which is 1.9 times faster in one pass, and both have no impact on the face; shrinking to 2 times before the second pass is 3.6 times faster, but it will change the facial features, so it is rejected. No tools have been added yet.