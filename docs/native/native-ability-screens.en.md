> **Language / Ngôn ngữ:** [English](native-ability-screens.en.md) · [Tiếng Việt](native-ability-screens.vi.md) · [中文](native-ability-screens.md)

# Ability view screen: Native takeover of ユニット ability/パイロット ability

Date: 2026-09-23. Items 4 and 5 of the inter-session menu. The five read-only screens (screen numbers 4, 13, 14, 5, and 15) are taken over by the RmlUi page, maintaining the original composition; switching between screens is injected into the key edge and handed over to the original function without changing any game data. The original screen can be selected back in the "Inter-session screen" on the settings page, see [Inter-session main menu](native-intermission-menu.md).

## 1. Original screen (static analysis)

The coordinates are all 320×240. The disassembly takes the instruction comments from the recompilation output.

### Unit list (Screen 4) and pilot list (Screen 5)

| Project | Basis |
| --- | --- |
| Layout 0x6D/0x6E: one panel (21,21)–(299,219); tag ユニットabilities/パイロットabilities (144,24), 0x1002 (Fairy) (24,200), レベル (248,200) | Layout table |
| Initialization `801D14BC`/`801D22E0`: background (including random numbers), layout, `801C87DC` (`801C4FB0(0)` generates a list of all aircraft `D_801DD210`) or `801C8DD8` (`801C549C(0)` generates a list of all pilots `D_801DD3A8`, the element is the driver table subscript), **9 rows per page**, starting from page `D_801DD14A` 1, row `D_801DEBC8` (copy `D_801DD53A`); `801C8854`/`801C8ED8` drawing list; `801C8BAC`/`801CA524` Draw details and write the selected items into `D_801DEC5C` (body slot number or driver subscript); cursor wizard 0x14 (21,48) 278×16 | `801D14BC`, `801D22E0` |
| Airframe row y=48+16n: airframe name x=24, pilot name x=152 (unmanned `--------`), HP (0xFE7) x=232, display HP (`800A5254`+`801C4DE4`) x=256 | `801C8854` |
| Pilot row: pilot name x=24, aircraft name x=96 (the name plus `801C8E50` gives the form offset of the ゲッター group; inorganic body `--`), レベル x=248, level x=280 | `801C8ED8` |
| Detail line y=200: When the cursor body (pilot's body) has ≥2 crew members and the second crew member `+4 & 0x40`, draw the second crew member (goblin) name x=64 and level x=280, otherwise `--------`/`--` | `801C8BAC`, `801CA524` |
| Each frame: A → next picture 13/15; B → 0; 9-line loop up and down, left and right page turning (`801CD2D4`/`801CD5B4`), redraw details | `801D1554`, `801D2378` |

Driver table: 100 entries × 0x4C bytes, starting from `0x80172F40`. Fields: `+0x02` number, `+0x04` flag (ability is displayed as `---` when 0xC0 is set), `+0x05` level, `+0x06/+0x07/+0x08` skill level, `+0x0A` spirit number, `+0x0B…` spirit id, `+0x12` experience, `+0x16/+0x18` SP current value/upper limit, `+0x20` strength, `+0x22` grid, `+0x24` shooting, `+0x26` avoidance, `+0x28` hit, `+0x2A` Reaction, `+0x2C` skill, `+0x2E…+0x31` terrain adaptation, `+0x36` skill mark, `+0x37` organism, `+0x38` body pointer.

### Body Abilities (Screen 13)

| Project | Basis |
| --- | --- |
| Layout 0x79: Panel (21,10)–(302,219), the interior is divided according to the original screenshot: body name (21,10)–(175,35); サイズ (0x1003)/repair cost (0x1004) (21,36)–(175,58); strengthening parts (21,59)–(175,131); HP/EN (21,132)–(155,163); Special ability (0x1005) (21,164)–(155,219); タイプ (0x1006)/Mobility (0x1007)/Mobility/Armor/Limited (156,132)–(259,219); Terrain (0xFF6) Air, Land and Sea (0xFF7–0xFFA) (260,132)–(299,219); Combat Map (176,8)–(302,132) | Layout table, screenshots |
| Size: `801D1680` According to the body `+0x0C` bit 1/2/4/8/0x10 is 0–4, text 0x446+n (SS…LL); repair cost `+0x1C` | `801D16D8` |
| Part: `+0x21` slot number, `+0x23…` part number, name 0x469+n | Same as above |
| HP／EN: Display HP `D_801DEB08` drawn twice (current value/upper limit, equal between fields), EN `+0x0A`; two 2-pixel-high cursor sprites 0x14/0x15 are green scales | Same as above |
| Movement type: `+0x0D` Bits 0–3 and 0x10 correspond to the icon text `D_801DC8F0[0…4]`, ranked from right to left (258,138) | Same as above |
| シールド：`+0x20 & 2` → text 0x38F (yes) otherwise 0x390 (no), drawn at (104,168) | Same as above |
| Special ability: `+0x28`'s 32-bit flag comparison table `D_801DC8FC` (16 items × 8 bytes: mask u32, text u16, width u8), wraps from (25,188) (the native page also wraps horizontally; up to 3 can be displayed, such as ビルバイン's Changsha/Clone/オーラバリア, the entire column is reduced when there are more than two lines, 2026-09-29) | Same as above |
| Right column: Mobility `D_801DD14C`, Mobility `D_801DD14E`, Armor `D_801DEB06`, Limit `D_801DEB04`; Terrain `+0x16…+0x19` gets letters through `800A6104(1,rank)` (4=A, 3=B, 2=C, 1=D, same for weapons), air adaptation in `D_801DDA06` When non-0, press 4 to display | Same as above |
| Each frame `801D2030`: L/R (`D_80178A08 & 0x2030`) → `801CCDA0(&行, 8)` Move forward and backward in the list, `D_801DEC5C` changes to a new body, re-enter screen 13; A → screen 14 (`D_801DEC58=0`); B → screen 4 | `801D2030` |

### Weapon List (Screen 14)

Layout 0x7A, panel (21,21)–(299,219), header 0xFF1–0xFF4 (weapon name/attack power/range/hit) y=24, detail row labels 0xFF5–0xFFA y=160, 0xFFB/0xFFD y=184, 0xFFC/0xFFE y=201. Initialize `801D2144`: `801C7254` Generate weapon list (same as weapon modification: `D_801DEC68`, quantity `D_801DECBE`, 6 rows per page, page `D_801DD20C`, row `D_801DEC58`), `801C75C0`/`801C7A9C` Drawing list and details (number of missiles, four-letter terrain, required power (red if power is insufficient), EN consumption (red if EN is insufficient), necessary skills, クリティカル correction). Each frame `801D21F8`: only B → picture 13; up and down, page turning (`801CD0CC`).

### Driver Abilities (Screen 15)

| Project | Basis |
| --- | --- |
| Layout 0x7B: Panel (18,10)–(299,219), divided according to the original screenshot: avatar (18,10)–(110,101) (`801C6350`); prompt LRZ: 二のパイロット (0x1008) (111,10)–(299,35); name block (111,36)–(299,101): full name (0x1287+number) (120,40), 気力 (0x1009) (128,64) value (160,64), レベル (192,64) value Ability block (18,102)–(299,137): grid (0x100C) (24,106) value (64,106), avoidance (0x100D) (112,106) `值+ 運動性` (152,106), reaction (0x100E) (232,106) value (272,106), shooting (0x1023) (24,122), hit (0xFF4) (112,122), skill (0x100F) (232,122); mental health (0x1010) (24,144) six grid positions `D_801DC6B0`: (136,144) (192,144) (24,162) (80,162) (136,162) (192,162), missing `---`; special skills (0x1011) (24,184) location `D_801DC6BC`: (96,184) (96,202) (168,202); terrain (0xFF6) (254,150), air, land and sea (240,176) (272,176) (240,200) (272,200) | Layout table, `801C936C`, screenshot |
| NEXT: Level 99 displays `---`, otherwise the return value of `8008407C(+0x12)` | `801C936C` |
| Avoidance/hit: `值+ 運動性`, value + mobility. Red when the limit of the aircraft is exceeded (the aircraft is recalculated with `800A5254` + `801C4DE4`; the pilot of the ゲッター group finds a shared aircraft with `801C924C`) | Same as above |
| Skill: `+0x36` bits 0x04/0x08/0x10/0x20/0x40 choose one in order → text 0x433/0x40F/0x418/0x421/0x42A + `+0x06`; bits 0x01 and `+0x07` → 0x43C+`+0x07`; bit 0x02 and `+0x08` → 0x406+`+0x08`; number 4 and `800A4BB8()` not 0 → text 0xF1 | Same as above |
| Each frame `801D24C8`: L／R → `801CCDA0(&行, 8)` Move forward and back and re-enter screen 15 (`D_801DEC5C` is changed to the new driver subscript); B → Screen 5 | `801D24C8` |

## 2. Takeover method

Source code: [`ability_page.cpp`](../../src/host/ability_page.cpp) (game thread adapter), [`frontend.cpp`](../../src/native/ui/frontend.cpp)’s `ability_sync` (page), [`game_hooks.cpp`](../../src/host/game_hooks.cpp) packaging (`ability_build`/`ability_step`/`ability_frame`, ten hooks in `generate_cpu.py`'s `NATIVE_HOOKS`). Weapon row and weapon column labels reuse `upgrade_page::weapon_row_json`/`weapon_labels_json`. When the original version is selected in the "Inter-field screen" of the settings page, all five construction entrances are returned to the original screen; `SRW64_NATIVE_ABILITY=0` or when the profile is not loaded, the original screen is retained throughout the run.

| original function | wrapper |
| --- | --- |
| `801D14BC`／`801D22E0` List initialization | Do not adjust the original function. Keep background calls (including random numbers) and list generation, row copy, `D_801DEC5C` writing; do not build layout, text, cursor sprite |
| `801D1554`/`801D2378` list per frame | Move/Page: Adapter writes page, row, copy with `D_801DEC5C` (9 rows per page); confirm/return inject A/B |
| `801D16D8`／`801D2480` Capability page initialization | Do not adjust the original function. Keep the background call; the page takes the fields directly from the record |
| `801D2030`/`801D24C8` Capability page per frame | Previous/next machine injection L/R (the original version moves the list cursor and re-enters the screen, and the page is rebuilt); A (body page)/B injection |
| `801D2144` Weapon list initialization | Do not adjust the original function. Keep background, `801C7254`; page write 1 |
| `801D21F8` Weapon list every frame | Write the mobile/page turning adapter yourself; return injection B |

**Snapshot**: `status.ability_page`: `screen` (`units`/`pilots`/`unit`／`weapons`／`pilot`), `serial`, `labels`, `weapon_labels`; the list is `page`, `pages`, `cursor`, `rows[]` (body: `slot`, `number`, `name`, `pilot`, __I NL_CODE_159__, `art`; Pilot: `index`, `number`, `name`, `unit`, `level`), `sub{name,level}`; The aircraft page has `unit`, `size`, `repair`, `parts[]`, `hp`/`hp_max`, `en`/`en_max`, `types[]`,__ INL_CODE_176__, `abilities[]`, `move`, `mobility`, `armor`, `limit`, `terrain`, `index`, `count`; the list of weapons is `unit{…,en,morale}`, `page`, `pages`, `cursor`, `rows[]` (same as weapon modification); driver page has `pilot{index,number,name,full_name,level,hidden,art}`, `unit`, `morale`, `next`, `sp`/`sp_max`, `stats{melee,ranged,hit,evade,skill,reaction}`, `over{hit,evade}`, `mobility`, `spirits[]`, `skills[]`, `terrain`, `index`, `count`. Event log `ability-page-events.jsonl`.

**Debug**: Stable ID `ability:N` (list line; click the cursor line to enter, click the cursor line to return to the weapon list); keyboard ↑↓, ←→ (page turning), Enter/Z, Esc/X, ability page Q/E (or ←→) to switch back and forth; waiting condition `ability_page`.

## 3. Real machine verification (2026-09-23)

```sh
.venv/bin/python tools/recomp/debug/check_ability.py            # 构建并检查
.venv/bin/python tools/recomp/debug/check_ability.py --reuse-build
```

`intermission-cold-1` The first episode is cleared and saved. Running `build/recomp/debug/20260923T033850.329381Z/`: `ability-checks.json` 18 items passed, exit code 0.

| Check | Results |
| --- | --- |
| Body list | Six lines (ダイターン3／ダイファイター／ダイタンク／スイームルグ／ドール／ドール(flying), `801C4FB0` List each form), HP 8000, driver ten thousand feet; ↑↓ Movement |
| Unit page | Sussex LL, repair cost 14000, HP 8000/EN 200, mobility 5, mobility 70, armor 1800, limit 270, terrain AABA, シールド有, special ability 変shaped, タイプ land and air |
| Switch back and forth | E → ダイファイター (serial added, original version re-enters the screen), Q → ダイターン3 |
| Weapon list | Six lines, 2 pages, first line Shooting ダイターンミサイル 900; → turn to page 2, ← return; ↓ move; X return to the body page |
| Return | X returns to the list (cursor 0), |
| Pilot list | Manzhang／シモーヌ／Marioミ／ローレンス Each unit name and level |
| Driver page | Breaking through the mountains: 気力 100, レベル 5, NEXT 444, SP 83/83, grid 150, shooting 126, avoidance 108+70, hit 108+70, reaction 92, skill 124, spirit Must hit/ドroot nature/気合/ひらめき/hot blood+?????, skill base L4/cut り払いL4/S defense L4, terrain AAAA - consistent with the original screenshots item by item |
| Switch forward and back and return | E → second driver; X returns to the list (cursor 1); |

Static analysis errors corrected in the process: the driver's `+0x20` is power, not the number of kills; `+0x26` is avoidance, `+0x28` is hit (text 0x100D avoidance, 0xFF4 hit, 0x100E reaction, 0x100F skill); terrain rank is 0–4 (4=A), the same goes for weapons (the modification page was originally displayed as 5=A, and it will be corrected this time); the avatar resource key is `battle_assets.portraits`.

## 4. Not verified

- Page turning of multi-page lists (more than 10 units/pilots, more than 7 weapons).
- The hidden pilot (`+4 & 0xC0`) whose ability is displayed as `---`, the name offset of the unit shared by the ゲッター group, and the red text in the weapon row when the power/EN is insufficient: the first episode archive does not have these situations.
- The current value and upper limit of HP on the aircraft page: the two are equal between fields. The page will display HP twice, which is the same as the original version.