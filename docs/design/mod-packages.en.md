> **Language / Ngôn ngữ:** [English](mod-packages.en.md) · [Tiếng Việt](mod-packages.vi.md) · [中文](mod-packages.md)

# MOD package: format, dependencies, classification and challenge rewards

2026-10-03. This article summarizes the MOD direction determined through discussions with users. It is a design and has not yet been implemented (except for the parts marked "already"). It succeeds the scope limitation at the beginning of [Built-in MOD Roadmap](mod-roadmap.md) "Currently no external MODs are connected, and no package loaders and dependencies are made." It now supports players to install third-party MOD packages, but only data and no code are included. For the existing basics, see [Customized Campaign](custom-campaign.md) (additional costs, MOD management, independent archives) and [Modification Limit](../gameplay/upgrade-limits.md) §7 (modification rule file).

## 1. Established principles

- **The original version is not included in the MOD list**. The original plot and data are the game itself; MODs are just changes, and if there is no package coverage, everything will go to ROM.
- **Our built-in content is delivered in packages**, listed below the user packages: HD package `srw64.hd`, our translations. They are marked "built-in" in the MOD management and cannot be deleted; HD packages and image mode switches, translations and language settings.
- **The package contains only data, no code**. Rule changes can only be made by opening the host's own rules and filling in the parameters (§6). The code MOD (upstream `.nrm`) will really need to be made separately in the future.
- **No online warehouse and automatic download**. When a dependency is missing, indicate what is missing and it is up to the player to install it.

## 2. Package format v1

A package is a folder or zip (extension `.srw64mod`). Use a folder when making, use zip when publishing, drag it into MOD management and install it to the user directory `mods/`.

```text
mod.json
campaign/   追加剧本（现在 campaigns/<id>/ 的内容）
challenge/  单关挑战（§8）
story/      改主线关卡（§7）
data/       数值（§5）
rules.json  打开宿主规则（§6）
art/        美术（§4）
dialogue/   台词与语言
audio/      音乐与语音
```

Only the directories that need to be used. `mod.json`:

```json
{
  "schema": "srw64.mod.v1",
  "id": "example.gaiden",
  "version": "1.2.0",
  "name": { "ja": "外伝", "zh-Hans": "外传", "en": "Gaiden" },
  "description": { "zh-Hans": "…" },
  "authors": ["example"],
  "game": ">=0.4",
  "requires": { "example.newpilots": ">=1.0" },
  "optional": { "srw64.hd": ">=1.0" },
  "conflicts": { "someone.oldgaiden": "*" }
}
```

- `id` will not be changed after release, use "author.name" to avoid name collision; version `主.次.修`.
- `game` is the host version requirement.
- After v1 is set, only fields will be added, the meaning of existing fields will not be changed, and an error will be reported for unknown fields (the same strictness as the modification of the rule file).

## 3. Dependencies and loading order

- Three relationships: **Required** (cannot be enabled if it is missing, indicate which one is missing and which version is required), **Optional** (if it is available, it will be ranked behind it, it can be used if it is not available), **Conflict** (cannot be enabled at the same time).
- Only one copy of each `id` is installed, so it only checks whether the version is satisfied and does not solve the version.
- **Automatic order calculation**: dependent packages are at the bottom, and built-in packages are at the bottom; players can only adjust the order of unrelated packages. Depend on the loop to report errors.
- When a package is deactivated, it will prompt that the packages that depend on it will be deactivated together.
- MOD management plus "installed" summary list: each package's category, dependencies, conflicts, how many items are covered, and order. Four category pages (Additional scripts/art/lines and language/music and voice) list packages containing content of this type.
- **Pre-start verification**: Python tools and hosts share a set of rules, bad packages are not enabled, and errors are reported with the files, fields, and reasons.

## 4. Appearance type: button overlay

The order is original version → built-in package → user package (according to the order of §3) → player's own modification in the user directory; the one behind the same key wins, and the key that is not provided is found in the lower layer.

| content | key |
| --- | --- |
| Avatar | Image resource number-palette number |
| Body three-dimensional painting | Scene-Atlas-Palette |
| Tactical map | Map number (whole sheet) |
| Background and plot pictures | Resource number |
| Icons, world maps, borders, etc. RT64 textures | Texture hash; the runtime library loads multiple replacement directories in order, and the later ones overwrite the previous ones |
| Lines | Record number (`@17410`), that is, the existing user directory overwriting method is expanded into multiple layers |
| Music | Track number |
| Plot voice, battle voice | Line record number; Combat line number |

The newly added resources (not the original ones) have package names, such as `example.newpilots:portraits/ryu.png`, which will not cover each other; other packages use this name to reference it, which is the main purpose of dependency.

Now all types of loading codes only recognize one `hd/`. It needs to be changed to merge all packages into a "key → file" table in order, and then hand it over to the drawing code. Supporting export tool: Export original images and HD images by category, and the file name is the key.

## 5. Numeric class

The tables that can be changed have been parsed ([original data directory](../data/original-data-catalog.md)): 363 aircraft, 1329 weapons, 361 characters (257 ability records, skill thresholds, mental acquisition), modification increment and price, upper limit of aircraft modification, and weapon modification types.

```json
// data/units.json：按机体号逐字段覆盖，没写的保持原版
{ "36":  { "hp": 4500, "armor": 1300, "upgrade_cap": 12 } }
// data/weapons.json
{ "160": { "power": 2600, "upgrade_type": 2 } }
// data/pilots.json：按人物号
{ "28":  { "skills": { "NT": [1,4,8,12,18,24,30,38,45] }, "spirits": ["熱血", "必中", "ひらめき"] } }
// data/rules.json：批量规则，逐条覆盖优先
[{ "select": { "faction": "enemy" }, "set": { "hp": "×1.3", "armor": "+200" } }]
```

- **Effectiveness method**: The host changes the corresponding bytes of the ROM data in its hand before starting the game. The original logic, our status page and the modification page, illustrated book, and battle viewer read the same number, and there will be no "one number on the interface, another number on the settlement". Transformation rules file (`srw64.upgrade-rules.v1`, existing) is merged unchanged into `data/`.
- **Effective time is marked by field**, displayed in MOD management:
- Each current read: the basic value of the body (the ability is recalculated `800A5254` each time it is read back from the ROM record), and the old archive takes effect immediately;
- Copied once when creating a new weapon: weapon modification type (`800A6A98` is only copied when creating a weapon instance), and the existing ones in the roster remain unchanged;
- To be verified: Whether the pilot ability is loaded and recalculated or stored in the archive.
- **Shared Record**: Multiple characters share an ability record, and changing one will affect others. The editing tool should prompt the co-sharer; if one person makes a modification alone, he needs to change his mapping to another record, and how many empty records there are needs to be checked.
- **Editing Tool**: Add "Change this item" to the original data browsing page/picture book and export it to `data/*.json`. Ordinary players do not need to write the number by hand.

Acceptance: Change a body, a weapon, and a pilot field, and check that the original status page, our page, actual battle settlement, and saving and loading files are all consistent.

## 6. Rule class

Logic changes such as experience multiplier, fund multiplier, and enemy level bonus are implemented by the host into rules (using the existing [optional rules](../gameplay/rule-fixes.md)). The `rules.json` in the package is only responsible for opening and giving parameters. Packages cannot bring new logic.

## 7. Drama: Change the main plot

Press **event** to change, do not press the whole level:

- **Additional Events**: Events added by several packages to the same level can be merged; if more than 63 events per level are exceeded, an error of 0x1A00 bytes will be reported.
- **Replace/Delete original event**: When two packages move the same event, the latter will take effect in order, and a conflict will be prompted.
- **Assault Deployment**: Change according to the record number (change body, change level).
- Events that have not been changed use `copy_from: base:stage_events:*` to reference the original version, and the scripts taken out of the ROM are not included in the package.

Example: "Allow a certain enemy to join" = Add an event to a certain level, and register it in `3D5A 机师,0,机体,500` when the conditions are met; at the same time, add the person's spirit and skills in `data/`, and add the upper limit of body modification and weapon modification type. Awaiting actual machine: roster limit (140 machine instances), map icon (including HD icon) after the enemy machine is replaced by our camp, and のりかえ list.

The additional code (`campaign/`) still clicks [Customized Campaign](custom-campaign.md): complete levels, borrow scene numbers, and save independently.

## 8. Single level challenges and rewards

The challenge is a mini-level with a preset army, and the results such as the number of rounds will be displayed after the game is completed. Rewards can be brought back to the main line.

### 8.1 Two ways to enter

- **Independent challenge plus reward box (do it first)**: Enter from the title or MOD management, with preset troops, independent of the main line. After passing the level, the rewards will be put into the reward box; when playing the main line and going to the inter-game, the inter-game menu will prompt "There are challenge rewards to receive", and after receiving them, they will be written into the current game. The level-clearing rewards for additional costs also go to the same reward box.
- **Enter from the field (played later)**: Like the DLC level of Machine Combat V/X/T, use the current troops to fight, and return to the field after the game, and the funds, experience, and parts will naturally be left behind. Before entering the challenge, the host records the progress of the main story (number of words `8010F5EF`, scenes `F5F0`–`F5F2`, total round `F5EC`, variables 100–114 and 128–139 that will be reset at the beginning of the level), and recover after completing the challenge. What will be changed in the customs clearance process (`3D4A`) must be verified on the actual machine first, and no one item can be missed.

### 8.2 Rewards that can be given (user decided on 2026-10-03: only give these three categories)

| Reward | Where to write | Note |
| --- | --- | --- |
| Funds | `D_8010F5F4` (u32) | Funds can be changed directly on the inter-field screen |
| Enhanced parts | Inventory `D_8015E990`, each part has one u16, high byte holding number, low byte holding number | The holding number is one byte, check the upper limit before adding |
| Transformation stage, pilot level/experience | Airframe instance `D_8016A210` (140 × 0x54) `+0x4C..+0x50` Five stages, weapon instance `+0x16`; Pilot record `80172F40` (0x4C one) `+0x05` level, `+0x12` experience | After changing the number of segments, the ability can be recalculated to `800A5254`, which will not exceed the upper limit of the machine body `+0x51`. Changing the level will not automatically increase the ability. You need to follow the original growth process (growth cycle `800A6238`). The specific calling method needs to be verified; first do the experience or number of stages |

No airframes/pilots are allowed to join the team, and no plot variables or hidden elements are allowed (which will disrupt the judgment of the main line route).

### 8.3 Rules

- The rewards are written in `mod.json` of the challenge package and are displayed before the game starts.
- **Only the memory is changed, not the archive file**: The host writes the memory between scenes, and the player saves it as usual; the original version is still responsible for the archive format and verification.
- **Each challenge can only be claimed once per main-line save**, and the claim record is placed next to the save file with additional information. `saves/` The library already has additional information files, but the cassette column does not. It needs to be filled. There is also "Allow repeated collection" in the settings, which is off by default.
- For archives that have received rewards, record the source in the additional information and put them together with the gameplay MOD records (§9).

## 9. Archive

- Additional information about the mainline archive records the numerical classes, rule classes enabled at that time, packages and versions of the mainline changes, as well as the challenge rewards received. If the file cannot be read, a difference reminder will be listed, but the file will still be read (it is common to install a balance patch midway).
- Appearance categories are not recorded.
- Use separate archives for additional scripts and independent challenges (the existing separation method).

## 10. Sequence

1. Package format v1, `mods/` directory, dependency check and "Installed" page; migrate the sample campaign, HD package, and transformation rule files into packages.
2. Acceptance of numerical classes (including batch rules) and §5.
3. Rule switch.
4. Independent challenge plus reward box (funds, parts, levels/experience).
5. Appearance multi-layer overlay and export tools; dubbing and BGM replacement.
6. Change the event-level modification of the main storyline; enter the challenge from the intervening stage.
7. New maps, new characters, and new aircraft (custom campaign C3, C4).

## 11. To be verified

- Whether the pilot ability is recalculated when loading a file or stored in the archive (determines whether the value MOD will take effect on the old archive).
- Can be used to individually change how many idle ability records a person has.
- How to use the original growth process when changing the pilot level.
- All mainline progress fields have been changed in the clearance process (for entering challenges between games).
- The list of camp icons and のりかえ after enemy mechas are added.

## 12. Reference method

| Ecology | Packages and dependencies | Reference |
| --- | --- | --- |
| N64Recomp (Zelda64Recomp, etc.) | `.nrm` zip `mod.json`, `id:版本` lists are divided into required and optional | The same runtime library, field names are similar |
| Factorio | `info.json`, one per line: `base >= 1.1`, `? 可选`, `! 冲突` | Dependence on the division of three relationships |
| RimWorld | `About.xml`: `modDependencies` is separated from `loadAfter`/`loadBefore` | "Dependency" is separated from "Only affects order" |
| Stardew Valley SMAPI | `manifest.json`: `UniqueID`, `MinimumVersion`, `IsRequired` | When a dependency is missing, clearly state which one is missing and which version is required |
| Bethesda (The Elder Scrolls, Fallout) | The order of plug-ins is manually arranged by the player, and is remedied by third-party tools such as LOOT | Negative example: the order is automatically calculated by dependencies |
| RimWorld, Bethesda loading files | Archive record MOD list, comparison reminder when loading files | Archive records of §9 |