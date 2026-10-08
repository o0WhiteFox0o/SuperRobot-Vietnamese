> **Language / Ngôn ngữ:** [English](original-data-catalog.en.md) · [Tiếng Việt](original-data-catalog.vi.md) · [中文](original-data-catalog.md)

# Original game data directory and parsing progress

Updated: 2026-09-12.

This batch of implementations converts the original Japanese ROM into a reproducible and traceable read-only directory for subsequent multi-language, data Mod and level analysis. The output contains raw bytes, stable identity, source address, hash, cross-table references, and field confidence. **It is not yet a writable game data ABI; the level script has completed static instruction parsing, but has not yet done run comparison and writeback. **

## Run

Execute in the warehouse root directory:

```sh
.venv/bin/python -B tools/content/extract_original.py
python3 -B tools/data_viewer/serve.py --port 59110
```

Browse `http://127.0.0.1:59110/`. The server only listens to the loopback and only provides `assets/original-data/`, no write API. Stop the terminal to shut down the service. `story.html` in the same directory is a plot viewer that reads the original Japanese text by chapter. The data comes from `story/index.json` and `story/NNNN.json`. See [Complete Analysis of Level Scripts](../script/stage-script-exploration.md#剧情查看器).

Optionally add the snapshot of the first chapter of the existing female super series:

```sh
.venv/bin/python -B tools/content/extract_original.py \
  --snapshot build/recomp/gfx-probes/female-map-audio-1/latest-gfx-rdram.bin
```

When snapshots are not provided, the extraction does not rely on the historical running directory, and the "first episode observation" category will not be generated. When providing snapshots, it is required to have `report.json` and `scene-evidence.json` in the same directory, and check the original ROM identity and scene ID. Observations in the directory save hashes of snapshots, reports, and scenario descriptions. The screenshot of the scene description is not necessarily the same frame as the final RDRAM; the screenshot frame number cannot be assigned to the snapshot.

## The range of extraction this time

| Category | Quantity | Evidence and scope |
| --- | ---: | --- |
| Text record | 51,174 / 20 tables | Use independent original ROM text parsing; retain 8-byte header, control word, dynamic name placeholder and TextKey. Table 0 has 50,975 entries, and the remaining tables total 199 entries. Not all image text is visible. |
| Resource block | 6,436 | Parse descriptor, retain original compressed span/padding, decompress all and output SHA-256. Successful decompression does not mean that the purpose or image format has been confirmed. |
| Airframe basic record | 363 | Confirmed read step size 36; the number is the complete record based on the boundary of the next table, with a 4-byte gap at the end. The name `527 + unit_id` is confirmed by the menu code, HP, EN, Mobility, Mobility, Armor, Limits and Repair Cost are confirmed by the load and display code. |
| Weapon basic record | 1,329 | Confirmed reading step size 16; pure name `1370 + weapon_id`, menu name `2699 + weapon_id`, both have display code basis. Attack power, range, hit correction, number of bullets, EN, energy requirements and critical hit correction have been confirmed; the number is defined by physical boundaries and is not equal to the number of names after deduplication. |
| Character name and identity | 361 | The abbreviation of `4382 + actor_id`, the full name of `4743 + actor_id`, is proved by the two loading of `80081130`. |
| Character→Basic/Spiritual Mapping | 360 each | Two consecutive resident `s16` tables, 720 bytes each. Negative values ​​are saved as is. |
| Driver base record | 257 | Covered by non-negative index in map `0..256`, step size 16. The six basic abilities, spirit points, growth at each level and seven skill marks already have consumer evidence. |
| Skill threshold record | 256 | Step size 30, physical interval is before the mental meter. Each of the three groups occupies 10 bytes, and each level loop reads the first 9 bytes; the grouping and name selection of special abilities, cut り払い, and S defense have been confirmed. |
| Mental Acquisition Record | 148 | Mapping index `0..147`, step size 12. Each group of six `(习得等级, 指令编号)`; the name `969 + command_id` has been confirmed, and the original table covers 30 instructions. |
| Scene→Map | 144 physical two-byte slots | The first byte is the initial map number; the all-zero slot at the end may be alignment filling, and the purpose of the second byte is to be tracked. Not the number of playable levels. |
| Map resource record | 158 | Step size 12; the first three slots are layout, atlas, and palette, and the static battlefield basemap has been assembled; auxiliary resources are to be analyzed further. |
| Chapter title candidates | 143 | `281..423` in Table 0, including duplicate/reserved titles; not the conclusion that "the game has 143 levels in total". |
| Scene script/event entry | 142 slots / 1,812 entries | 131 independent entry tables; all 1,812 events are read to the end character, a total of 67,160 instructions, 33,582 dialogue references (including speakers), 2,678 condition blocks; 73 command slots, 30 conditional instructions, 12 context markers and 15 trigger types are compared against the machine code one by one. See [Complete Analysis of Level Script](../script/stage-script-exploration.md). |
| Script supporting data/sortie records | 138 blocks / 6,223 entries | Matching index has 144 slots; parsed to 999 in 14 halfwords, fields from 8020ABB4 read order; 13 blocks unaligned to 999, original bytes retained. |

In the airframe weapon table, 363 airframe pointers correspond to 266 different list addresses, referencing 1,182 different weapon numbers, with a maximum of 1,327. You cannot delete another weapon record just because it is not referenced by this set of lists.

## Structural evidence

Layout and evidence byte lock: `config/data/original-jp-v1.json`. The relationship between the resident address and the ROM address is `ROM = VRAM - 0x80075610`. The overlay must be converted according to the corresponding load segment in `config/recomp/code-sections.json`, and the resident offset cannot be applied. The browse page "Parse Evidence" contains segment names, addresses, bytes and hashes for 58 code/data windows; resident disassembly in `build/recomp/disasm/cpu-main/rom_80076610.text.s` and overlay disassembly in `build/recomp/cpu-scan/<section>/`.

| Data | ROM starting point | Loading/consuming code | Explanation |
| --- | --- | --- | --- |
| Body | `0x71B80` | `800A6E68`, ROM read calls `800A6FB8` | Index multiplied by 36, read `0x24`. The original record +0/+2 is copied to runtime +4/+6 and +8/+10; then displayed after `load_0008F4B0:801C4DE4` cache and `801C6E64`, confirm HP/EN. |
| Weapons | `0x74E90` | `800A642C`, called `800A6448` | Index multiplied by 16. `800A6A18..800A6A30` Multiplies the original +1 byte by 100 and writes the runtime +6; the `load_000AB160:801E6410` status page displays this value by the attack power label. |
| Driver Basics | `0x7A1A0` | `800A6398` | The actor is mapped by `s16[800CA9C4 + actor*2]` and multiplied by 16. Six bytes +1..+6 are written to six u16 fields at runtime, the order is confirmed: fighting, shooting, avoidance, hit, reaction, skill. |
| Skill threshold | `0x7B1B0` | `800A6340` | Use the same base record mapping, then multiply by 30; subsequent counting by level. |
| Mental acquisition | `0x7CFB0` | `800A63E0`, `800A8098` onwards | actor mapped by `s16[800CA6F4 + actor*2]`; negative values skipped. Six sets of records compare the current level and append the command number. |
| Aircraft weapon list | `0x7E210` | `800A67C8`, `800A68BC` | `base + u32[base + unit*4]` points to a 12-byte record stream; the first u16 is the weapon ID, and the remaining five u16 are matching airframe form slots. The entire record with the first field FFFF is the termination item. |

The five form slots are copied from `800A6AC8..800A6AE0` to runtime weapons +0x18..+0x20. `load_0008F4B0:801C72C0..801C7314` is compared item-by-item with the current body ID, and then also checked for the `0x600` flag of runtime weapon +0x22. The parser adds `eligible_unit_ids` (filter FFFF), retaining the original `remaining_u16` five slots and complete bytes; morphological matching is not a complete weapon available determination. The list itself can include weapons used in other forms. The page says "Loadable weapons (including shared forms)" and cannot be directly used as the weapon list in the current form menu.

The second batch of new semantic evidence:

| Association/field | Loading segment and key address | Evidence chain |
| --- | --- | --- |
| Body name | `load_0008F4B0:801C6DD0..801C6DEC` | 84-byte runtime body record +2 → Add `0x20F` → Text display `8008D0E8`. |
| Weapon pure name | `load_00216730:801C2928..801C2A30` | The first u16 in the original body weapon list → add `0x55A` → text display. `load_000AB160:801E7B44..801E7BA4` also uses this formula. |
| Weapon menu name | `load_0008F4B0:801C76B8..801C77BC` | Weapon array of body +0x30, step size 36, record +2 → add `0xA8B` → text display. Keep the original markings such as grid/shooting/P, and do not deduce weapon behavior from the name. |
| Spirit name | `load_0008F4B0:801C9D84..801C9DB4` | Driver step size 76, spirit slot starts from +0x0B → command number plus `0x3C9` → text display. Number 0 is self-destruction, 29 is resurrection. |
| Repair Cost | `load_000AB160:8020D894..8020D8DC` | Text 933 "Repair Cost" displays runtime body +0x1C next to it; `800A709C..800A70A8` copies the u16 from the original record +0x14. |

The third batch of numerical semantics and encoding:

| Table | Original record offset and type | Confirmed explanation |
| --- | --- | --- |
| Unit | `+0 u16`, `+2 u16`, `+6 u8`, `+8 u16`, `+A u16`, `+C u16`, `+14 u16` | HP, EN, mobility, mobility, armor, limits, repair cost. All are basic values, equipment, mental state and modifications are separately included. |
| Weapons | `+1 u8 × 100`, `+2/+3 u8`, `+4 s8`, `+5 s8`, `+6/+7 u8`, `+D s8` | Attack power, minimum/maximum range, hit correction, number of bullets, EN consumption/required energy, critical hit correction. The number of bullets `FF` is reserved for the no-bomb limit flag of `-1`. |
| Driver | `+1..+6 u8`, `+C u8` | Fighting, shooting, avoidance, hit, reaction, skill, maximum mental points. Starting from level 1, fighting/shooting/reactions/skills +1 per level, avoidance/hit/maximum mental points +2 per level. |

The basis is not that the numerical value looks reasonable, but the relationship between the original record → runtime field → display coordinates and text label. The resident tag tables ROM `0x518C0` (aircraft), `0x51968` (pilot), `0x51A80` (weapon) all retain byte locks. The status shows that the consumer is in `load_000AB160:801E517C / 801E6410 / 801E6C5C`; the growth cycle is in resident `800A6238`. The driver's basic hit/avoidance and the interface total value should be separated, and the interface will also add the body value.

There are seven explained skill slots for the driver `+F`: `01` Cut り払い, `02` S Defense, `04` Base Strength, `08` NT, `10` Strengthen the World, `20` Holy warrior, `40` superpower; `80` unexplained. The three groups of skill thresholds each occupy 10 bytes, but `800A80F0` only reads the first 9 items in each group, and counts the number of items that satisfy `0 < 阈值 <= 当前等级`. The first group corresponds to the mask `7C`, and the name is selected according to the priority of `04→08→10→20→40`; the second and third groups correspond to `01`, `02` respectively. The last byte of each group is 0 in all 256 original records, this tool retains it and cannot interpret it as level 10. The original text link of the name retains the decoding results of the existing character list; individual suspected misrecognized glyphs in the character list have not been rewritten without authorization in this batch.

The third batch of scenes is associated with the map:

- `load_000AB160:80209D6C` reads ROM `0x102110` with the scene index of `8010F5F0`, step size 2, and writes the first byte to the current map index `8010F5EE`. Adjacent symbol boundaries accommodate 144 slots; the trailing `00 00` may be padding and cannot be used to claim 144 levels.
- `load_000AB160:801C6EFC` reads ROM `0x10267C` with map index, step size 12, to `0x102DE4`, 158 entries in total. Five u16s are consumed by the resource loading chain, and two are skipped when the auxiliary number is 0; the complete meaning of the two tail bytes has not yet been explained.
- The scene index of the historical snapshot of the first episode of Women is 1, and the map index is 20; the corresponding resources are **6284, 6228, 6243, 6422, 6429**. The entire map resource table in the snapshot is consistent with the ROM bytes. This confirms the index and resource relationships, but is not a complete explanation of the map grid, events and organization.
- The entrance to the tactical scene is by resident `800801A4` selecting `801E022C / 801E0268 / 801E028C / 801E0350` in `load_000AB160`, and then entering `801E00AC`. In addition, resident `8009DD58 → 8009DBE4 / 8009DC58` loads the data of ROM `0x1E3FE0` and `0x19BF10`, which is reserved as the entry point for the next step of event flow analysis and has not yet been output as a decompiled script.

Currently, three types of boundary problems remain:

1. The name area has 361 entries, and the two mapping tables have 360 entries each. The name of the character 360 can be displayed, but the next table will not be read out of bounds to fabricate driver data.
2. Person 284 mapping base record 256. The threshold loading formula `0x7B1B0 + 256*30` falls right into the mental table `0x7CFB0`. Keep this exception; you need to trace the control flow later to confirm whether the path is reachable. You cannot just conclude that the original game has a bug based on this.
2026-10-01 Static confirmation **reachable**, waiting for real machine: character 284 is our クェス (`3D5A` is registered as 284; enemy クェス is character 55, use normal line 42), `800A7F8C`/`800A80F0` There is no boundary check when reading the threshold, and the bytes at the beginning of the mental acquisition table are read. Skill level = the number of `0 < 阈值 ≤ 当前等级` in 9 thresholds, calculated based on these bytes: NT `1,11,4,5,7,18,9,23,12` → Level 1 L1, Level 23 L9; Cut `32,22,1,11,2,5,10,12,21` → Level 32 L9; S defense `26,4,48,25,1,7,9,25,18` → Level 48 L9. Minimum actual machine confirmation: After クェス joins, check whether the status page displays NT L9 at level 23.
3. The distance from the weapon pointer area to the first payload is `0x5B0`, which is equivalent to 364 u32. Currently, 363 bodies are read; the last boundary word and the gap at the end of the body table have not yet been explained, and the number of records is the result of the current physical interval division.

## Female Super Series Chapter 1 Observation

The original JP ROM RDRAM of `female-map-audio-1` is used, and the current extraction process does not start the game. The final status of the historical report is `native-run-failed`, exit code `-10`; it can be used to study the saved memory, and cannot be used to claim that the current version has been accepted for running or exiting.

The starting point of the array when the machine is running is `0x8016A210`, each bar is 84 bytes, and each bank has 140 slots. Reads the allocated record with status 1, the number of drivers along +0x34 and the pointer from +0x38 associated with the 76-byte driver record. This association has a code basis in `800A7C08` and its calling path.

| Assigned aircraft ID | Name | Pilot actor ID |
| --- | --- | --- |
| 36 | スイームルグ | 28 マナミ、24 ローレンス |
| 216 | ダイターン3 | 165 thousand feet |
| 218 | ダイファイター | 1.65 million feet, sharing the same driver pointer |
| 217 | ダイタンク | 1.65 million, sharing the same driver pointer |

These four allocation records are not equal to four map attack units. There are 12 other bank 1 airframe records in the snapshot; they are also assigned status at this point in time only and cannot replace event triggers, reinforcements, or enemy scripting.

`unit 36 → weapons 160..163`; `actor 28 → pilot_stats 18 → thresholds 18`, and `actor 28 → spirits 13` can jump item by item on the page. Identities such as characters and weapons retain their original numbers and cannot be deduplicated or renumbered according to their translated names.

## Airframe/Pilot Integrated File

When browsing the home page, "Unit" and "Pilot" are the main entrances; scenes, resources and each original table are stored in expandable auxiliary categories. Existing `base:units:NNNN`, `base:actors:NNNN` and original table deep links remain valid.

- **Unit File**: Basic ability cards, weapon tables with names and parameters, and related forms in the shared weapon list. Distinguish the current form matching weapon from other form weapons according to the original five form slots; the latter are folded and displayed. Matching still does not mean meeting all usage conditions.
- **Pilot Profile**: abbreviation/full name, six abilities and mental points, growth at each level, six mental acquisitions, and L1-L9 acquisition levels of each enabled skill. Characters associate base, mental, and threshold records through their own mappings, and actor IDs cannot be used directly as indexes in these tables.
- **Same name and empty mapping**: 361 name identities are reserved respectively; 264 of them are associated with fixed ability records, which can be filtered by "Only display pilots with associated abilities". Mappings of negative numbers, threshold boundary anomalies for person 284, and missing mappings for person 360 are still explicitly preserved without zero padding or guessing capabilities.
- **Search**: The aircraft supports searching by referenced weapon name and form name; the pilot supports full name, mental name and skill name. Searching by stable ID is still possible.
- **Original basis**: The original table entry is retained below each integrated file, and detailed fields, bytes and evidence are collapsed by default. The original tables of weapons/spirits/abilities/thresholds etc. also provide links back to related integration files.
- **Flight Relationship**: Only summarize the two-way aircraft/pilot relationship when historical snapshots are provided, clearly mark the observation at that point in time and link the source of the snapshot; it is not treated as a fixed pairing rule for the whole game.

The integration is generated by `src/srw64_native/original_profiles.py`, and the result is attached to the `profile` of the original record. It is read-only display data and does not change the original `fields`, `raw_hex`, mapping and identity. `search_terms`, `summary`, `has_stats` enter the lightweight index, and the page does not need to request other data tables one by one to splice the files. Generate code to join the producer byte lock of the manifest.

Skill levels are not simply marked according to the slots in the original array. The original program counts all items that meet `0 < 阈值 <= 当前等级`; it sorts the valid thresholds among the nine items during display, so it can correctly handle invalid zero slots, non-increasing thresholds, and simultaneous addition of multiple skill levels to the same level. The original order remains in the threshold record.

## All special abilities and special skills

Two new entries have been added to the browser: "Machine Special Abilities" and "Character Special Skills". Each entry lists all original holders and allows you to jump back to the file. Ability cards and skill names in the profile are linked back to the summary. Supports searching by Japanese name, Chinese definition, classification or holder name. The Chinese definition is only a search/display aid for the catalog and does not rewrite the original text.

The body scan covers all **363** original records: `+0x1C u32` special ability bits and `+0x18 u8` equipment bits, a total of **22** categories, **429** records holding associations; 109 records do not have these two organized flags set. The actual occurrences of the bits in the original record are overwritten; this does not mean that the complete behavior of all other fields, event appends, and special functions has been resolved.

| Classification | Organized items (the parentheses are the original body/form number) |
| --- | --- |
| Form | Changing shape (60), separation (11), combination (27) |
| Reply | HP recovery 10% (10), HP recovery 20% (4) |
| Avoidance | Clone (26), マッハスペシャル (1), real マッハスペシャル (1), ゴッドシャドー(2), ゲッタービジョン(1), Shunphanzu(3), ハイパージャマー(3) |
| Shield | Iフィールド(11), ビームコート(7), プラネイトディフェンサー(3), オーラバリア(23) |
| Support and loading | Repair device (10), supply device (3), mothership/loading function (11) |
| Strengthening | Power Strengthening (4): Code determination and increment have been confirmed; V-MAX series name correspondence is still clearly marked as a candidate |
| Equipment conditions | Cut off corresponding equipment (147), shield equipment (61) |

The naming evidence comes from the 16-entry display table of `load_000AB160:8021818C` (ROM `0x100CEC`, each of `u32 mask / u16 text_id / u8 width / u8 reserved`). The status page `801E5400..801E5480` uses the runtime body `+0x28` and the mask, and then displays the text; resident `800A70EC..800A70F8` copies the original body `+0x1C` to this field. Another equipment field is copied from the original record `+0x18` to the runtime `+0x20` via `800A70BC..800A70C8`. The definition is based on the mark position/mask and does not guess the ability from the name of the aircraft.

- **HP reply**: Bits `0x4` and `0x8` share the original interface text 1027, but `801FA544..801FA57C` is passed in 10.0 and 20.0 respectively; `801FA324..801FA3D8` confirms the reply according to the percentage of the maximum HP, and truncates the write back after capping. When both are set at the same time, 10% branch priority is given. Aggregation retains different holders and is not merged into one undifferentiated "reply" entry.
- **Avoidance class**: The shared mask of `801F6C44` is `0x163011`; after the main pilot's strength reaches 130, it needs to be randomly determined to meet the conditions. The summary presents the original holding position, does not simulate whether each battle is triggered, nor does it simply superimpose multiple clones.
- **Repair/Supply**: Bit `0x400 / 0x8000` is queried by `801F07A8 / 801F044C` respectively, menu `801CA394..801CA444` is associated with text 518/519 of ROM `0x106918 / 0x10691C`. Actual commands are still limited by target and action status.
- **Vigor Enhancement**: When bit `0x10000`, vigor >=130 and there is no enhanced state, call `801FE9CC` via `801FF2A0..801FF2F8`, set the state and add movement 1, mobility 20, limit 100, and add `0x200` beam coating. The 7 original beam coating holders in the summary do not include the units added during operation. The name V-MAX series is a candidate correspondence and cannot be regarded as semantic confirmation that all relevant variants have been completed.
- **Mothership**: The registration and load list consumption evidence of location `0x80000` are in `801DC170..801DC1CC` and `8020C664` respectively; here only the functional classification is confirmed, and the complete load capacity or load list is not deduced.
- **Separation of equipment and skills**: Cutting off requires machine equipment slot 1, pilot skill slot 1, non-zero skill level and attack type conditions (`801F6D5C..801F6DB4`); shield defense requires machine equipment slot 2, pilot skill slot 2 and non-zero level (`801F7020..801F7068`). For example, body 216 has a shield, but aircraft form 218 does not. Equipment cannot be automatically inherited between shared forms.

The character summary retains all **361** identities, of which 264 are associated with fixed abilities; 97 are unassociated and are not counted as "no skills". Of the 264 identities with recorded abilities, 99 did not have the seven-category skill flag set. A total of **314** skills are associated; the identities of records with the same name or shared values ​​are retained separately, and the number of independent value records is listed separately on the page.

| Skill | Flag Holding Identity | Has Valid Threshold | All Zero Threshold | Threshold Not Associated |
| --- | ---: | ---: | ---: | ---: |
| 杀り払い | 140 | 138 | 1 | 1 |
| S Defense | 91 | 87 | 3 | 1 |
| Bottom power | 23 | 23 | 0 | 0 |
| NT | 27 | 26 | 0 | 1 |
| Strengthen the world | 15 | 15 | 0 | 0 |
| Holy Warrior | 10 | 10 | 0 | 0 |
| Super Powers | 8 | 8 | 0 | 0 |

The three "threshold uncorrelated" all belong to the same boundary anomaly of character 284, not three different characters. Name precedence for the first set of skills is retained; positive thresholds count first acquisition and highest level with count semantics, and all-zero thresholds do not appear as learnable. The skill bit `0x80` does not appear in the current original base record and the parser still retains this unknown bit.

`original_abilities.py` Adds read-only projections after file generation: `profile.abilities / ability_flags`, skill's `definition_key / equipment_note`, and `unit_abilities / pilot_skills` two directories. The original record's bytes, fields, names, or mappings are not overwritten. Defines the original display table/code span and evidence link against which the entry is retained, `manifest.ability_coverage` lists the full scan count and unassociated, unflags, unknown bit identities. It does not belong to the runtime Mod Write schema.

## Output, modules and subsequent architecture

- `src/srw64_native/original_data.py`: ROM table parsing, boundary checking, reference relationships and optional snapshot observation; no ROM writing, no UI import.
- `src/srw64_native/original_abilities.py`: Body ability/equipment definition, character skill holder index, two-way file link and complete coverage audit; unknown bits are not discarded.
- `tools/content/extract_original.py`: lock verification, unified directory generation, original resource decompression, full reference check.
- `tools/data_viewer/web/`: read-only HTML/CSS/JS without third-party network dependencies; `app.js` manages categories and navigation, `profiles.js` displays integrated files, `ui.js` provides shared secure DOM components. Supports search, capability filtering, paging, adjacent records, stable hash links and resource downloads.
- `tools/data_viewer/web/abilities.js`: All holders of abilities/skills, acquisition classification and coverage description.
- `assets/original-data/manifest.json`: Source ROM, layout, production code and output file hashes, counts, check ranges and unconfirmed items.
- `records/*.jsonl`: full record for tool consumption; textual `text_ir` preserves the lossless record schema. `indexes/` and `details/` every 256 entries are page cache formats.
- `raw/resources/*.bin`: All decompressed data. `raw/resource-spans.bin`: Splice the original compressed spans sequentially; each resource record retains the pack offset, span length and original ROM address.

The build directory is only allowed to be in a separate `build/` subdirectory. Existing directories must have matching manifest schema before they can be replaced; complete parsing and reference checking before publishing the output. The original content remains in the build directory, which is ignored by Git.

The subsequent Mod layer should consume another semantically confirmed definition schema; do not use this `raw_hex` or candidate field directly as a writable configuration. Recommended order:

1. Continue to confirm terrain adaptation, position marks, special conditions for growth, modification/transformation and weapon availability conditions; this batch of explanations of main numerical values and unit conversions have been completed.
2. The level IR has been read out completely (event flow, text references, reinforcement groups, victory and defeat, and route commands all have static interpretation); the next step is to compare runtime script tracking with static interpretation, as well as the internal structure of the map (terrain, auxiliary layers).
3. Use one body parameter, one mental acquisition level and one event to make the minimum recoverable replacement, check it in the silent native run; open the corresponding Mod schema after passing it.

The language pack continues to use `base:tNN_NNNNN` and the original text hash, and the character/body definition refers to the name through TextKey. Pictures and 3D replacement belong to independent resource axes, and language, image quality switches and game values ​​are not tied together.

## Acceptance range of "parsing completed"

The goal is to make the original content reproducible, translatable, and character/machine/level moddable. recomp retains the execution logic of the original program and can provide loading and consumption evidence, but does not automatically restore the meaning of field names, data models, or event instructions.

| Field | Already have a foundation | Must be completed before completion |
| --- | --- | --- |
| Text and language | 20 table lossless text IR, name TextKey association | Control word and calling context coverage, font library and picture text list, Japanese/Chinese switching and fallback scene acceptance. Extracting the original text does not mean completing the translation. |
| Characters, bodies, weapons, spirits | Fixed tables, names, main basic values, linear level growth, skill grouping and cross-table relationships | The remaining fields and bit flags, special growth/transformation/deformation conditions, negative values ​​and abnormal index control flow form a writable definition item by item. |
| Level | Chapter title candidates, scene → map → resources, static battlefield base map, historical memory relationship of the first episode, complete event command IR (conditional block, protagonist paragraph, speaker, trigger type, `3D4B` route flow, sortie record) | Complete correspondence between title and scene ID, terrain attributes and auxiliary layers, game effects of map performance commands, comparison of runtime script tracking and static interpretation, unmodified reconstruction and single event replacement verification. |
| Images, models and other resources | descriptor, full decompression and byte lock, 361 character avatars/363 body map icons/158 basemap associations | Battle map and other resource types and usage locations, replacement specifications, and origin/HD switching verification. |
| Mod write link | Read-only directory and stable identity | Define schema, reference and range checking, unmodified writeback consistency, single modification and restoration, silent game verification. |

Each domain is accepted according to "lossless extraction → field and instruction explanation → reference closure → reconstruction without changes → modification and running verification". Unknown bytes/opcodes must be preserved and marked explicitly; they cannot be disguised as parsed fields. There is still substantial work on level scripts and remaining field semantics; full-game parsing cannot be claimed as complete at this time, nor is progress reported as a percentage without a denominator.

## verify

```sh
.venv/bin/python -B -m unittest discover -s tests -p test_original_data.py -v
PYTHONDONTWRITEBYTECODE=1 make check
```

Test coverage: out-of-bounds, bad pointers, no termination items, dangling weapon/form IDs, ROM/layout/code evidence drift, byte-by-byte reorganization of all fixed tables, common list and form differences, negative sentinels, two mapping exceptions, episode 1 cross-table references and historical snapshot shared driver pointers. The second batch adds independent display command checks, weapon name first and last boundaries, spirit numbers 0 and 29, repair costs and overlay address ownership checks. The full build also checks that 51,174 pieces of text are raw-byte reassembled, 6,436 blocks of resources are decompressed, and all directory links are resolvable. Resource decompression is not a proof-of-difference that reruns native LZ this round.

2026-09-11 The first batch of results: All 67 tests of `make check` passed; the same manifest was generated twice in a row with the same input, and all 6,714 output file hashes in the manifest passed; the 6,436 segments of the original compressed span pack are consistent with the original ROM byte by byte. See `build/original-data-qa/verification.json` for records and `build/original-data-qa/logs/original-data-check.log` for test logs.

The second batch of results on the same day: all 70 tests of `make check` passed; after regenerating the directory, the size and SHA-256 of 6,714 output files, 61,200 unique identities, and 17,867 associated links all passed. See `build/original-data-qa/verification-pass2.json` for records and `build/original-data-qa/logs/original-data-check-pass2.log` for test logs. The browser confirms repair costs, form relationships, unit → weapon jump, Japanese weapon name search, pure name/menu name, and six name associations for Spirit Table 13. The game has not been launched in this batch; run verification after field modifications is still to be completed.

The third batch of results on the same day: all 76 tests of `make check` passed, and the dependency check passed. New verifications cover signed modifiers, attack power multipliers and bomb sentries, skill slot priorities, nine thresholds and reserved bytes, independent UI label coordinates, scene → map → resources and historical snapshot table byte consistency. Post-generation verification of 6,720 file sizes and hashes, 61,519 unique identities, 39,014 resolvable links, and byte-for-byte consistency of 6,436 raw compressed resource spans. The results are shown in `build/original-data-qa/verification-pass3.json`, and the test and extraction logs are `build/original-data-qa/logs/original-data-check-pass3.log` and `build/original-data-qa/logs/original-data-extract-pass3.log` respectively. The browser confirmed the machine body 36, weapons 160, pilot value 18, skill threshold 18, and the jump and download entry for scene 1→map 20→resource 6284. This batch only performed static extraction, historical snapshot reading and development page verification, and did not start the game or write Mods.

The browser checked the coverage category, paging, adjacent records, repeated selection of the current category, original text search, empty result boundary, 5600 resource download link and Chapter 1→Manami→Spirit Table jump, and checked the actual display of the page. This item is the acceptance of the development tools page; the native game has not been launched this round.

Integrated file verification: 82 tests of `make check` passed; specifically covering actor mapping summary, morphological differences in shared weapon lists, skill threshold count semantics, negative value/missing/out-of-bounds mapping, original bytes and identity unchanged, bidirectional association of historical ride relationships, and consistency of repeated generation. The sizes and hashes of 6,722 generated files, 48,458 directory links, and 57,622 in-file references were all checked. The browser checked the pilot's complete profile, ability filtering, spirit name search, body shape and folded weapons, old spirit table return profile, adjacent navigation and empty search; the game was not started. The log is `build/original-data-qa/logs/original-data-check-profiles.log` and the verification manifest is `build/original-data-qa/verification-profiles.json`.

Overall Competency/Skills Verification: **88** tests of `make check` passed, dependency checks passed. A new test is added to independently check the original ability display table, field copy instructions and HP recovery constants; all abilities/equipment settings are reorganized one by one to verify the difference in form, the difference between skill holding and effective acquisition, retention of unknown bits, unchanged original records, and consistency of repeated projections. The generated directory contains a total of 6,729 files, 61,564 identities, 50,119 directory links, and 59,733 references within file/capability definitions. File hashes and references all passed the check. The test log is `build/original-data-qa/logs/original-data-check-abilities.log` and the generation log is `build/original-data-qa/logs/original-data-extract-abilities.log`; see `build/original-data-qa/verification-abilities.json` for the coverage list and browser verification results. The game has not been started in this batch, and no Mod has been written.

Image and weapon marking validation: **103** tests of `make check` passed, dependency checks passed. 361 identity-related avatars, 363 body/form-related map icons, and 158 map record stitched basemaps; the independent preview is 338 avatars, 320 icons, and 157 maps, a total of 815 images, and a total of 972 PNGs after adding map thumbnails. All 7,725 generated files were size checked and SHA-256 checked, 74,861 directory links were all closed, and 1,329 weapon raw menu strings were all matched to mark splits. For details, see [Original Pictures and Weapon Markings](original-images.md); the verification list is `build/original-data-qa/verification-images.json`. This batch is static decoding and browser verification, and the game has not been started.