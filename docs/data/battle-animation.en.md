> **Language / Ngôn ngữ:** [English](battle-animation.en.md) · [Tiếng Việt](battle-animation.vi.md) · [中文](battle-animation.md)

# Combat animation processing logic and feasibility of customizing the body/weapon

Updated: 2026-09-19. Static analysis (disassembly and ROM data), without running the game. For image resources, scene formats and exports, see [Battle Images](battle-graphics.md). "Code confirmation" refers to reading the instructions to read/use the data; "static inference" refers to the meaning deduced from the usage method, which still needs to be verified on the actual machine.

## Conclusion

1. **Battle animation is not a bytecode script. ** Each weapon corresponds to a record with a fixed layout: 4 header fields, up to 8 sound effects, up to 24 actors. Each actor is assigned a combat scene (image), a set of coordinates, and a **behavior routine number**. The timing logic is all written in about 270 native routines in the combat overlay, and actors collaborate on a shared "phase" byte.
2. **Custom weapon animation can be done with data alone**: New records reuse existing behavior routines and point actors to new or existing scenes. Only new performance logic (actions that existing routines cannot do) requires writing C++ native routines.
3. **The format of custom art has been completely read through. ** The body atlas, palette, and scene (parts + vertices + step table) can all be generated reversely by the tool (PNG → Atlas/Palette/Scene), and HD replacement follows the existing mechanism of hashing by texture.
4. **The difficulty in adding aircraft/weapons is the ID, not the image. ** All tables are fixed-length tables connected end to end, and the table base address and the upper limit of the two IDs are hard-coded in the code.
- **Occupy existing placeholders or duplicate slots**: Only the data coverage and resource services of the host layer are required, and there is no need to regenerate the recomp code, which is the shortest way.
- **Really new ID**: To hook into multiple read functions, regenerate code, and handle archive compatibility.

## Data flow of an attack

```text
武器 ID ─→ ROM 0x11FC80[id] (u32 偏移) ─→ 动画库 0x184990 + 偏移，DMA 0x3C0 字节
          │                                   │
          │                                   ├─ 头部：镜头模式、命中特效号、攻方动作、守方动作
          │                                   ├─ 音效表（≤8）
          │                                   └─ actor（≤24）：registry, x, y, z, h4, h5, h6, behavior
          │                                        │
          │                                        └─ 0x11E3D0[registry] = (场景, 图集, 调色板) ─→ 资源加载 ─→ 精灵槽
          ├─ ROM 0x119970[id]：规范武器 ID（机师台词用）、接触标志、伤害节拍模式、相位码
          └─ 命中特效号 ─→ 0x216150 / 0x2129F0（同格式，159 条；156–158 为击毁）
守方：反应代码 ─→ 0x216630 / 0x2163D0（同格式，28 条）；盾牌图 0x2166A0（24 条）或机体战斗记录
双方基本姿势：0x84E40[机体 ID]；机体战斗记录：0x118610[机体 ID]
```

| Table | ROM | Entry | Index | Read | Confidence |
| --- | --- | ---: | --- | --- | --- |
| Weapon animation offset → Animation library | `0x11FC80` → `0x184990` | 1,329 (1,115 different records) | Weapon ID | `801C3128` ← `801C3C9C` | Code confirmation: `801C3C9C` Pass the weapon ID directly to the reading function, the records of weapons 29 and 24 are different |
| Hit effects library | `0x216150` → `0x2129F0` | 159 | Weapon head hit_script; 156–158 destruction | `801C31E8` | Code confirmation |
| Defense Reaction Library | `0x216630` → `0x2163D0` | 28 slots (8 different) | Reaction Codes | `801C3230` | Code Confirmation |
| Battle scene summary list | `0x11E3D0` | 1,051 | actor.registry | `801C3170` ← `801C50D8` | Code confirmation |
| Defense Wizard | `0x2166A0` | 24 | Response Code | `801C31AC` ← `801C4574` | Code Confirmation |
| Weapon Combat Log | `0x119970` | 1,329 × 7 s16 | Weapon ID | `801C3278` | [0] Canonical Weapon ID (`8022241C` check `< 0x531`) code confirmation; [3] Contact, [5] Damage Beat, [6] Phase code is statically inferred |
| Aircraft combat record | `0x118610` | **354** × 7 s16 | Aircraft ID | `801C30D0` | [1] Sprite scaling %, [2..4] Shield image, [5] Additional scene, [6]=2 Select destroyed 156, static inference |
| Damage beat pattern | `0x181DB0` (`D_80222E50`) | 25 × 8 | Weapon record [5] | `801C8A58` | Static inference |

- Most of the images used by the attacker's actors are on the attacker's own battle atlas (for example, registry 297 = ガンダムシュピーゲル (2477, 1612, 1908)); beams, explosions, etc. are on the special effects atlas.
- Pilot lines are selected separately by `80222050` according to pilot, standard weapon ID and reaction, and are not written in the animation record.
- There is another copy of the same read function in `load_00216730` (`801C2634`–`801C27DC`); when moving any table, both places must be modified together.
- Each animation library is followed by a copy of the unused offset table (`0x19AA40`, `0x215ED0`, `0x2165B8`).

## Animation record format

Parser `801C3D38`/`801C4EF0`; the remaining developer editor (see the end of the article) is compiled in the same format, which can be used as circumstantial evidence.

```text
u16 camera          镜头／站位模式 0–3（801C67EC 选择每帧处理 801C63BC/64D8/6584/6678）
u16 hit_script      命中特效库条目
u16 action          攻方主精灵动作号（0–188，跳转表 0x80223990，经 801E4668）
u16 defender_action 普通命中时守方的动作号
s16 sounds[≤8], 0xFFFF     行为例程用 801C355C(n) 播放第 n 个；−2 = 静音
actor[≤24] { u16 registry; s16 x, y, z; u16 h4, h5, h6; s16 behavior }, 0xFFFF
```

| actor field | meaning | credibility |
| --- | --- | --- |
| registry | Combat scene general table index, loaded into the rotation elf slot (`801C50D8`); x on the defending side is inverted | Code confirmation |
| x, y, z | Offset relative to own body sprite; some routines use them as parameters | Code confirmation |
| h4 | Interpreted by routines, mostly the starting delay frame number or character number; bit15 is the flag | Partial confirmation |
| h5 | Each frame is copied to elf byte +0x35 (mostly 0xFF, the routine will gradient it, presumably for opacity) | Copy the code to confirm, the meaning is inferred |
| h6 | Display mode: 1 = never automatically hide, 2 = never automatically show (control actor) | Code confirmation |
| behavior | Behavior routine 3–382, function pointer table `0x80225030` (via `80220C0C`); 4, 5, 370, 371, 380, 381 are empty | Code confirmation |

All 1,329 + 159 + 28 records are parsed in this format: maximum 406 bytes, exactly 24 actor records exist, registry maximum 1045, behaviors are all in 3–382.

### Example

| Weapon | Head (camera, hit effects, attacker, defender) | actor |
| --- | --- | --- |
| 0 アイアンネット（シュピーゲル） | (1, 0, 88, 128), sound effects 3, 58, 250 | registry 222 "WepIanNet" at (0, 36), behavior 28 (equal phase 0x44/0x46, write 0x43/0x45) |
| 3 シュピーゲルブレード | (0, 33, 23, 148) | registry 297 (native posture) behavior 43; registry 250 "WepDoubleCut" behavior 44 |
| 228 ビームライフル（ガンダム） | (1, 6, 113, 125), sound effects −2, 1, 5, 8 | registry 121 shooting posture behavior 359 (displayed at 0x44, h4 determines whether to hide the body, play sound effects and flash); registry 0 Stealth timer behavior 124 (write 0x50 20 frames after 0x44); registry 56 "WepBeamRed00" at (−65, 28) behavior 118 |
| 29 シャイニングフィンガー | — | Quotes other than native parts cut-in 1009–1016: ドモン close-up, シャイニング close-up, King of Hearts coat of arms, etc. |

The parsing results for all weapons are exported in `animations.json` and for each aircraft in `unit.json` (actors are directly linked to image files).

## Behavior routines and phase bytes (mainly static inference)

- `801C5BAC` The routines of all active actors are called in sequence every frame when the block phase byte (B+0x25) has 0x40; the master sprite shares this byte with all actors (E+0x48 points to it).
- Seen phase codes: 0x41–0x46, 0x48, 0x49, 0x4B, 0x4C, 0x50–0x57, 0x5A. 0x44 = "Fire": Action 88 has the attacker rush forward for 21 frames before writing 0x44, 142 routines waiting for it. 0x49 deactivates the actor. 0x50–0x57 are substeps concatenated between actors (e.g. timer 124 writes 0x50 after h4 frame). The meaning of 0x43, 0x45, and 0x46 is inference.
- Basic operations available for routines: change scene/atlas/palette (`801C5700`, `80098204`, `80098590`, `80098604`), show/hide ( `801C3840`/`801C37FC`), play sound effects (`801C355C`), full screen flash white/black (`801C9520`, `801C95CC` → `8009AC84`), 10 sprite palette effects (`801C963C` → `80099C88`), camera follow (`801C637C`/`801C63A8`), advance damage rhythm (`801C8DFC`), load defense elf (__INL_C ODE_56__), background hiding/restoration (`801C3C40`/`801C3C64`, unconfirmed), derived subroutines (`80220C0C`, `801E4668`).
- Per-side state `0x800F97E0 + side × 0x1074`, including 0x81C bytes each for weapon block (+0x2C) and reaction block (+0x848): 0x4C header, main sprite pseudo-actor, 24 0x50-byte actors.
- Effect sprite slots 0xAA–0x107 (94) are used in rotation, without overflow check; three blocks × 24 actors can fit.
- Special weapon IDs (`801C3C9C`): −1 no animation; −2/−3 (defend/evade instead of counterattack) log with built-in null `D_80222D40`; `0x1000` read RAM `0x80250010` (where developer editor writes).

### Defense reaction code (`load_000AB160:801F7204` setting, static inference)

| Code | Meaning |
| --- | --- |
| −1 | Normal hit: The defender performs defender_action on the head of the weapon |
| 0 | Not attacked |
| 22 | Avoidance (Action 15) |
| 6–12 |ゲッタービジョン、マッハスペシャル、真マッハスペシャル, ゴッドシャドー, instant phantom foot, ハイパージャマー, clone |
| 2→13, 3→14, 4→15, 5→16 | Iフィールド,ビームコート,オーラバリア,プラネットディフェンサー: The former is completely blocked, the latter is penetrated |
| 17 | Shield Defense |
| 18／19 | Cut り払い, distinguished by the operating time of the attack weapon |
| 20 | Support defense (another machine takes the hit on your behalf) |
| 21 | Unknown (related to map grid flag 0x80) |

## Resource loading and memory

- Resource table in ROM `0xA20BD0`: u32 number (6,436) + 8-byte descriptor; each item is u32 decompression length + LZSS (`src/srw64_rom/resources.py`).
- Load function `80089E9C(id)`:
- `sltiu 0x1924` of `80089EAC` is the only resource ID cap (code confirmation).
- The loaded resources are only reference counted; the slot table `D_80160340` has 200 entries and is allocated for the first adaptation.
- The descriptor is read directly from `osEPiStartDma` by `80089BBC`, without going through `8007F704` that the host has hooked; data decompression goes through `8007F704`.
- The heap is `0x80277800–0x80400000` (1,607,680 bytes), all loaded resources are shared, and there is no additional limit for individual events or single battles.
- An allocation failure will print "ALLOCATE ERROR", return −1, and the caller will then get a null pointer.
- Maximum resource 263,177 bytes (1349), maximum airframe atlas 201,609 bytes. The battle map of an airframe is 3 resources (scene about 1.4 KB, gallery, 264 byte palette).
- The actual margin in combat has not been tested.
- recomp runs with 8 MiB RAM, the game only uses more than 4 MiB of `0x80400000–0x804152F0` (developer editor) and host script injection area `0x807F0000`, leaving about 3.9 MiB free in the middle.
- Image constraints: Most parts are 32×32 (maximum 48×32, 40×40), CI8 has a maximum of 2,048 texels per part in 2 KB TMEM; the atlas size is 32k+1 (leave 1 pixel edge for bilinear filtering); a single frame can see up to 123 parts; CI8 palette 256 colors.

## Add custom bodies and weapons

### Tables involved in a body

| table | location | size | read method |
| --- | --- | --- | --- |
| Base value | ROM `0x71B80` | 363 × 36 | `800A6E68`, `800A5254`, `800A8CE8`, `8009C2DC`, via `8007F704` |
| Weapons list | ROM `0x7E210` pointer → 12 byte row | 363+1 empty; `0x82E40–0x83110` has 720 bytes 0xFF gap | `800A67C8`, `800A68BC` |
| Name | Text 527 + Unit ID | — | `801C6DD0` etc., via `8008C510` |
| Status screen offset | ROM `0x7D980` | 363 × 4 | `8009C6E4` |
| Basic combat postures | ROM `0x84E40` | 365 slots | `8009C864` (combat `801C5328`, `801C5808`, `8021FB4C`) |
| Airframe combat record | ROM `0x118610` | **354** × 14; ID ≥ 354 will read the subsequent weapon combat table | `801C30D0` |
| map icon | overlay RAM `0x80218218` (ROM `0x100D78`) | 363 × 2, no gaps | 5 inlines `lhu`: `801C5F14`, `801C60BC`, `801C84F4`, `801CCD38`, `801CE818` |
| Optional | Transform `D_800CB40C`/`B5A4`, Combined `D_800CAC94`/`AEF0`, Inherit `D_800CA3A0`, Crew `D_800CA418`, Seen bit set (ID < 354) | — | Resident/overlay |

A weapon: base value ROM `0x74E90` (1,329 × 16, `800A642C`); name text 1370＋ID and menu name 2699＋ID; weapon combat record `0x119970`; animation offset `0x11FC80`; appears in the weapon list line of a certain aircraft; optional modification inheritance mapping `D_800CB5E8`.

Upper limit: The weapon only has `< 0x531` of `8022241C` (there is another place in the debugging module); the body does not check 363 in the game logic, and if it crosses the limit, it will silently read to the next table. There are only 2 empty slots left in the battle scene table, and there is no bounds check for reading.

### Route A: Occupy existing slots (recommended to do first)

- **Candidate body slot**:
- 314 and 325 are νガンダム records with exactly the same bytes (only a few bytes different from No. 50); 309 ゴッドガンダム shares the weapon list with 1 and 2. There are no references to them in the deployment, event, transformation/fusion tables, and they need to be checked one by one.
- 354–362 are placeholder records, but there are no airframe combat record lines (`0x118610` only has 354 lines). To use them, you must first resolve the out-of-bounds combat record, so they are suitable for route B.
- **Candidate Weapon Slots**: 147 weapon IDs not in any of the aircraft's weapon lists (e.g. 10–14, 1191–1198, 1328). Many of these are real weapons, such as the 24 シャイニングフィンガー which has its own cut-in animation, possibly granted by code by form. It can only be used as a candidate, and code references should be excluded one by one before use.
- **What the host has to do**:
- **Data Overlay**: Expand the `patch_copy` byte patch (`src/host/upgrade_rules.hpp`, currently used to modify the rules to modify the body +0x20, weapon +0x0E) into a universal data overlay. All ROM tables read by `8007F704` can be overwritten, including all overlay loaded data and map icon tables.
- **Weapon List**: The new list is written into the 0xFF gap and the pointer is changed, leaving the shared list unchanged.
- **Animation records**: The offset of `0x11FC80` is u32, new records can be put into the host's existing virtual ROM window (`0x02400000`, `0x03000000` mechanisms).
- **NEW IMAGE**: Override `80089BBC` to make the descriptor read point to a new resource in the virtual window (or use a data ROM variant like the 5600); the same mechanism can also replace existing resources.
- **Name**: Provide a string such as 527+ID using an existing dummy text path. The menu can only draw fonts that are in the ROM font library, and the menu name must retain the grid/shoot/P mark.
- **Risk**: If you have an existing archive with this ID, it will be displayed as a new body (the above candidates are not expected to be available); the remaining amount of the battle pile has not been measured.

### Route B: Really add ID

- recomp allows the host to take over the function (`NATIVE_HOOKS` of `tools/recomp/toolchain/generate_cpu.py` renames the generated function, and the host provides the original name in `src/host/game_hooks.cpp`). N64Recomp also supports instruction patching, but the currently generated `recomp.toml` is not useful.
- **TO DO**:
- **Reading function**: Take over the small reading functions (copies in `8009C6E4`, `8009C864`, `801C30D0`, `801C3278`, `801C3128` and `load_00216730`).
- **Table reading function**: Use the instruction patch to change the table base address of `800A6E68`, `800A5254`, `800A8CE8`, `800A642C`, `800A67C8`, `800A68BC` to the virtual window containing the original table plus new rows.
- **Map Icon**: 5 reads changed to new table in free RAM.
- **ID Cap**: Release `0x531` and `0x1924`.
- **Name**: Hook the name call point, mapping to a private text ID.
- **ARCHIVE**: According to a subagent's reading of the archive serialization code, the airframe ID is saved in 10 digits (`id << 6 | 武器数`), with a maximum of 63 weapons per unit, and each archive has a pool of 140 airframes, 100 pilots, and 700 weapons (pending verification). Therefore, the new body ID should be ≤ 1022, and the archive will depend on MOD - loading without MOD will silently read incorrect data, requiring fingerprints or accompanying files, and `src/srw64_native/checkpoints.py` currently rejects additional fields.
- Missing any read point will silently read the error without reporting an error. This is the main risk of this route.

### Route C: ROM expansion

The host already supports data ROM variants (`config/recomp/rom-variants.json`), with ROMs available at `0x1D8C000–0x2000000` (2.45 MiB) and `0x86B000–0x89A000`. However, the end-to-end connection of each table, the base address, and the upper limit are all code constants. The expansion itself only helps the resource redirection of route A. The overlay code bytes must be consistent with the original (from which the recomp code is generated), and the variant also brings separate archive and hash locks, which need to be distributed as a patch.

### New art production process

1. Draw a body diagram (combat posture and weapon action parts) and quantify it to within 256 colors.
2. Reverse tool cuts into 32×32 parts, arranges into 32k+1 size atlas, generates palette and mode 0 scene (8 vertices per part, second set is mirrored). The format has been verified step by step by this exporter and tests, this tool has not yet been written.
3. Write a scene summary entry and weapon animation record actor for each action. The behavior routine selects the corresponding one from the existing 270 (shooting posture 359, beam 118, slash 43/44, etc.). `animations.json` can be used as a ready-made reference library.
4. HD version continues to replace by texture hash.

### Projects that require actual machine verification

The actual remaining amount of the stack during the battle; the number of VIs corresponding to one beat; the meaning of the phase code 0x43/0x45/0x46; the fields of `0x118610` and `0x7D980`; Route A replaces one body and fights a complete battle (attack, counterattack, shield defense, destruction). As per project practice, these are confirmed before running.

## Remaining development tools

- **`load_00089EA0`: ROBO VIEWER. ** The airframe image viewer for debugging comes with a 1,449-item scene table (ROM `0x8AB58`).
- **`load_00217FD0`: Combat animation editor. ** Load `0x80400000`, write the editing result to `0x80250010`, and pilot with the special weapon ID `0x1000`.
- Its name table (`0x80402E3C`) names the entries in the battle scene summary table, such as 222 "WepIanNet", 121 "WepGndm00", 602 "WepBSRedSwing1".
- The routine names at the end of the table (BtlProcShield, BtlProcCoverDiffence, BtlProcBeamShield, etc.) correspond to the behavior routine ID at an offset of 767.
- Editing restrictions are registry < 0x41B, behavior ≤ 0x17F, h6 ≤ 4.
- These names are the best source for naming scenes and behavior routines, which can be exported together in the next step.