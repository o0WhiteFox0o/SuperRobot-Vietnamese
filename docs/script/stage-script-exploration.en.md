> **Language / Ngôn ngữ:** [English](stage-script-exploration.en.md) · [Tiếng Việt](stage-script-exploration.vi.md) · [中文](stage-script-exploration.md)

# Level script: complete command analysis

2026-09-12. The second round completed the static analysis of the event script virtual machine on the locked Japanese version of the original `rom.z64`: the parameter lengths and distribution relationships of all 73 ordinary instruction slots, 30 conditional instructions, 12 context markers, and 15 event registration types have been compared with the ROM machine code one by one. All 1,812 event entries have been read from the beginning to the `FFFF` terminator, and there are no more "stop at unknown instruction" events. Dialogue speakers, route branches, attack records and event trigger conditions have been entered into the read-only directory. **Things that have not yet been done**: There is no actual execution path of the simulation script, no script written back, and no game started with this batch of analysis for operation acceptance; the game effects of some instructions only retain the technical name of the call chain.

The first round of structural evidence (event library two-level pointers, DMA window, event first five words, `3D45` supporting record consumption chain) continues to be valid, and only the new and modified parts are recorded here.

## Extract results and count

| Structure | Quantity | Meaning |
| --- | ---: | --- |
| Event Library Scene Index / Independent Entry Table / Independent Event | 142 / 131 / 1,812 | Same as the first round; not the number of playable levels |
| Events where `FFFF` was read | 1,812 | Only 0 or 2 bytes of alignment padding left after terminator (790 / 1,022 events) |
| Decoded instructions | 67,160 | Contains 1,812 terminators; unknown instructions 0 |
| Dialogue citations | 33,582 | Number of citations; 30,154 parsed directly by the speaker, 2,983 parsed by protagonist paragraph, and 445 still relative to the route |
| Conditional blocks | 2,678 | Up to 5 levels deep; 29 blocks ended with `FFFF` instead of `3E1D`, 15 redundant `3E1D` |
| Scanning difference | 0 | The original program's word-by-word scanning and structure analysis have the same landing point (see dangerous rules below) |
| Companion records (sortie records) | 6,223 | 138 physical blocks, 13 blocks unaligned before upper bound 999, original bytes preserved |
| Scene flow edge | 148 | Obtained from the scene index parameter of `3D4B`, excluding runtime conditions |
| Machine code evidence window | 80 | There are 22 new items in this batch, located in `evidence` of `config/data/original-jp-v1.json` |

Statistics are reproducible from `script_coverage` of `assets/original-data/manifest.json`. ROM Instructions that never appear in the script: `3D31`, `3D41`, `3D76`–`3D79`, `3DD8`–`3DDB`, __ INL_CODE_18__, `3E01`, `3E05`, `3E07`, `3E19`, `3E1A`, `3E1C`.

## Virtual machine structure

The engine structure is located in `8015F950` and the event context is embedded in `+0x948` (script PC is `+0x964`). Separation of instruction fetching and execution: `8009EED0` only advances 2 bytes after reading the 16-bit command and writes the processing function to `+0x30`. The processing function is repeatedly called by `8009EFDC` every frame until it returns the command status `+0x96C` to zero and pushes the PC through its own parameters. Therefore, the parameter length of each ordinary instruction is the increment to the PC when its processing function is completed; this batch is confirmed function by function. The default branch of the distribution table returns an empty processing function, and `3D76/3D77` will stall the event; although `3D78/3D79` is within the distribution table, the mark loop of `8009F0E8` will not allow the words of `≥ 3D77` to reach distribution.

Before fetching, `8009F0E8` first processes two types of structural words:

- **Conditional instructions `3E00`–`3E1D`** (`8009F228 → 8009F288 → 800A1D68`): `800A1D68` Press `jtbl_800D0890` to call the conditional function, and the function advances the parameters by itself. When it is true, continue; when it is false, `8009F288` scans word by word from the parameter after the parameter. The instruction pointing to `8009F354` in `jtbl_800D0638` makes the nesting layer +1, `3E1C` also +1, `3E1D` makes the nesting layer −1, and after the layer number is reset to zero, it crosses the `3E1D` and continues; encountered during scanning `FFFF` then the event ends. The `3E1D` encountered during execution is always true.
- **Context tags `3DD0`–`3DDB`**: with `0x3DD0`, current protagonist tag `+0x99E`, `3DD5/3DD6` derived from it and `3DD7/3DD8`, selected limb result `+0x994` If one of the two is equal, skip and continue execution; otherwise, scan backwards verbatim to the matching token or `FFFF`.

Neither scan knows the parameter length. In this batch, the scanning placement points of the original program are compared with the structure analysis block by block. If the placement points are different, the `skip-scan` difference is recorded; the parameters located in the non-common section and whose values fall within `3DD0`–`3DDB`, `3E00`–`3E1D` or `FFFF` are recorded `marker-scan-control-word`. Both are 0 in the ROM script. The nine `3D39 FFFF` (stop sound effects) are located in the `3DD0` common section, and the mark scan will not pass through them.

### Context tags

| Mark | Meaning | Basis |
| --- | --- | --- |
| `3DD0` | Common section, any context matches | `s4` of `8009F0E8` |
| `3DD1`–`3DD4` | Mahmoru Route | `load_001090A0:801C69D0` Select by protagonist 2/3/0/1 Write `+0x99E` |
| `3DD5` / `3DD6` | リアル system (`3DD1/3DD2`) / スーパー system (`3DD3/3DD4`) | `+0x99E < 0x3DD3` is derived |
| `3DD7` / `3DD8` | Male (`3DD1/3DD3`) / Female (`3DD2/3DD4`) | Derived from `3DD8` when `+0x99E` is `3DD2/3DD4` |
| `3DD9`–`3DDB` | Select limb items 1–3 | `3D44` Write `+0x994 = 0x3DD9 + 序号` |

The same function also explains the dialogue speaker: the first three decimal digits of the 8-byte header of the text entry are the speaker character number (`8008CE54`), `25` and `29` are offset by `+0x99E − 0x3DD1` respectively, that is, the "protagonist" and "antagonist" change with the route: 25 アーク, 26セレイン, 27 ブラッド, 28 マナミ; 29 エルリッヒ, 30 リッシュ, 31 カーツ, 32 アイシャ. The relative speakers in the directory located in the `3DD1`–`3DD4` segments have been named according to the paragraphs. Two candidates are reserved for those located in the `3DD5`–`3DD8` segments, and four candidates are reserved for the others. The remaining digits in the header have not yet been interpreted by any read function and are simply retained with the original text.

### Conditional instructions

`+0x99C` is the only compare register (ACC). The statement class is always true and the block is not opened; when the block class is false, it jumps to `3E1D` of the same layer.

| Command | Parameters | Semantics |
| --- | ---: | --- |
| `3E00` | 0 | ACC = 0 |
| `3E01` | 3 | If character HP% < threshold and present, ACC = value (open block) |
| `3E02` / `3E03` | 2 / 3 | If variable ≠ value / If variable = value then ACC = value 2 (open block) |
| `3E04` | 2 | If the current round `8010F5EA` < the number of rounds, then ACC = value (open block). Round count starts from 0 (+1 when `801D1324` is displayed), so `3E04 N` is true ⇔ screen rounds ≤ N (2026-10-01) |
| `3E05` / `3E07` | 0 | Constant (jump table falls inline −1; open block) |
| `3E06` / `3E0D` | 2 / 1 | ACC taken from roster `80172F40` entry +5 comparison / +0x14; field meaning unconfirmed |
| `3E08` / `3E09` / `3E0A` / `3E0B` / `3E0C` | 1 | ACC = / ≥ / ≠ / ≥ / < value (open block) |
| `3E0E` / `3E0F` | 1 | variable = (variable ± 1) mod 4 |
| `3E10`–`3E12` | 0 | Select limb result = item 1/2/3 (open block) |
| `3E13` / `3E14` | 2 / 1 | variable = value / ACC = value |
| `3E15` | 1 | ACC = number of camp units (`+0x9B0`–`+0x9B2`, `802018C4` refresh) |
| `3E16` | 1 | ACC = the character of the other side of the war (excluding parameter characters) |
| `3E17`–`3E1A` | 0 | ACC or `+0x998` taken from engine fields, meaning unconfirmed |
| `3E1B` | 1 | ACC = Character presence status: 1 on the map / 0 shot down / 3 not on the scene or has left the map (retreat, escape). `800A1F7C → 800A3990 → 800A293C` Read status table `D_8015DE90`: value 0 → 0, value 1 → HP% (1–100 is classified as 1), the rest (initial value −1, departure 2) → 3; crash path `801FAFFC` write 0, departure path `8020C664`／`8020CA80`／`8020CFF8` Write 2 (revised on 2026-10-01, previously written "0 is not here / 3 has exited") |
| `3E1C` / `3E1D` | 0 | Unconditional block start / block end |

The variables are 200 2-bit values (`8015E818`, `800A496C/800A4888`). When playing a new game, the protagonist chooses overlay to adjust `800A4790` and writes all 26 half-words to `FFFF`, that is, all 200 variables are 3 (`load_001090A0:801C69E4`); when a new level starts, `8009DE7C` sets 100–114, 128–139 to 3, and 54 to 3. 1. Set the selection register `+0x994` to `3DD9` (item 1). `+0x994` is only rewritten by `3D44`, and is retained across events until the end of the level, so when there is no second `3D44` in the level, the `3E10`/`3E11` that ends the event reads the opening choice (Supplemented on 2026-10-01).

### Common commands

The parameter lengths, processing functions and basis of the 73 slots are all recorded in `commands` of the layout lock, and the directory page `script_opcodes` can be checked item by item. Core commands with confirmed game meaning:

| Command | Parameters | Meaning |
| --- | ---: | --- |
| `3D38` / `3D39` / `3D3A` / `3D3B` | 1 | Wait for the number of frames / Play sound effects (`FFFF` stops) / Play BGM (0 stop) / Fade the picture |
| `3D3E`–`3D43` | 1 | Dialogue, six display modes; speaker comes from text header |
| `3D44` | 3 | Select limb (window slot, number of options, option text), the result enters `+0x994`; earlier noted as "text, number of options, window parameters", corrected, see below |
| `3D45` | 1 | Deployment supporting record group (debut); `8020B154 → 8020ABB4` generates the body and pilot from 28-byte records |
| `3D46` / `3D4F` | 2 / 1 | Unit list performance A / B: Parameter < 500 is the role, ≥ 500 is the supporting group (value −500); A is called with the exit processing of area arrival |
| `3D47` / `3D48` / `3D4E` | 0 | Close the dialogue window (wait 32 frames / immediately / yield one frame respectively) |
| `3D4A` / `3D4B` / `3D4C` | 0 / 1 / 0 | Level victory settlement (→ Stage C3) / Set next scene index (500 = recovery) / Game over |
| `3D52` / `3D53` | 3 / 1 | Enable/disable type 1 delay count events (slot, turn, stage) |
| `3D54` / `3D35` / `3D34` | 1 / 2 / 4 | Remember character position / scroll to position (`0x40`–`0x44` relative to remembered position) / switch map and scroll to position (map number, x, y, type; run injection confirmation) |
| `3D57` | 2 | Enable type 8 zone arrival event slot |
| `3D5B` / `3D62` / `3D6C` | 1 / 2 / 2 | Funds + Parameters × 1000 / Change character identity / Set the number of body modification stages (`800ACA1C`: Only find the first instance of this number in our pool, five items and all weapons are written `min(N, 上限)`, invalid if not found) |
| `3D60` | 3 | Our troops are arranged and deployed according to the grid |
| `3D6D` | 1 | The current stage is set to our side (`8010F5E8 = 1`; stage number 1 our side / 2 enemy / 3 third party, between levels is 0) |
| `3D5A` | 4 | Roster entry/removal (role, parameters, new unit, word 4). Word 4 `< 2000` → `800AAD28` Registration: If the same pilot is already on the same numbered aircraft, do nothing (`3D5A …,500` repeated registration is harmless); aircraft 999 only registers the pilot (`800A9CF0`), pilot 999 only registers the aircraft; when there are both and the roster already has the aircraft number `800A9DCC` Remove the original pilot and let the new pilot take over, otherwise create a new one; when the 4th character is an old aircraft, it will be inherited and transformed according to the predecessor table (see [Transformation Inheritance](../gameplay/upgrade-inheritance.md)), 500 = Do not delete the old aircraft. Word 4 `≥ 2000` → `800A3540` Removal: **2000 deletes only the pilot, 3000 only deletes the body, 4000 deletes both**, skip deletion when the character is 999 (`800A355C`–`800A35CC`); all 3000 in the original script are used as the character 999 Call, equal to invalid (2026-10-01, `800A0B3C`) |
| `3D65` | 2 | Set the victory and defeat condition display (victory number, defeat number) → `engine+0x996`; the only reader `load_000AB160:801C68F0` (via `800A3524`) draws text **5567 + victory number** (`801C6918 addiu 0x15BF`) and **5593 + Defeat number** (`801C6954 addiu 0x15D9`). Only used for display: pass depends on `3D4A`, failure depends on `3D4C` or the engine's total destruction judgment `801FF934` (2026-10-01) |
| `3D6B` / `3D73` / `3D74` | 3 / 1 / 0 | Detachment mark: `3D6B 角色,机体,1` Set pilot +0 bit 7 and body +0xC bit 6, `…,0` clear; `3D73 n` passed `800AD990` marks the whole batch according to the preset list (n≠0 list A `D_800D06A8`, n=0 list B `D_800D06E4`); `3D74` clears all. The sortie candidate list `801EBBA8` (called by `801C78A0`) skips the units of `+0xC & 0x40` (`801EBEDC`–`801EBEE8`), so the marked person **cannot sortie** temporarily** (example: scene 23 `3D6B` Wan Zhang), restored after clearing (2026-10-01) |
| `3D6F` | 1 | Unlock weapon (weapon number) |

**`3D44` Parameter order correction (2026-09-17). ** Earlier, parameter 1 was regarded as the option text, so the directory linked all 46 selection limbs to `t00_00000`/`t00_00001`, and the plot page was displayed as "plain/forest/forest". Machine code basis: `8009EED0` After fetching the instruction, the PC has passed the command word. In the first frame of `8009FA94`, `lh 0(PC)` (parameter 1) is used to call `8008FF34`. The latter gets the window coordinates from `800C6994`/`800C6996` according to parameter 1×12; then `a0 = lh 0(PC)`, `a1 = lhu 4(PC)` (parameter 3) calls `8008FF04 → 8008F648(槽位, 文本, 模式 2)`. `8008F648` saves `a1` into `s6` and gives it to `8008CD8C` for drawing, which is the same path as the dialogue processing `8009F4B4` passes through `lhu 0(PC)` via `8008FED4` (mode 1); parameter 2 (`lh 2(PC)`) is passed to `8009F3A8` as the upper limit of the cursor. Data check: among 46 places, parameter 1 has only 0 (44 places) and 1 (2 places). Parameter 3 continues the dialogue numbers before and after (such as scene 026 event `001A6DE8`: dialogue 21812–21814 followed by `3D44 [0, 2, 21815]`, `t00_21815` is "シーラのsquare へdirectional かう / エレのsquare へdirectional かう"), and the number of `<BR>` lines of 46 texts is equal to parameter 2. The option text is a text branched by `<BR>`, not multiple consecutive text IDs; the table of contents and plot pages have been rebuilt accordingly.

The rest of the commands (`3D31`–`3D33` World Map Show, `3D36`/`3D49`/`3D50`/`3D55`/__INL_CODE_26 0__/`3D5C`/`3D63`/`3D67`/`3D68`/`3D75` Waiting for map performances, `3D5D`/`3D70` and other roster operations; `3D5A`, `3D6B`/`3D73`/`3D74` are listed in the table above) The parameter length and call target have been confirmed, `semantic_confidence` is marked as `structure-confirmed` or `unknown`, name reserved for technical description. The first two of the five parameters of `3D3D` are not read by the resident code, the third parameter of `3D56` is not read, and the parameters of `3D5F`/`3D6D` are not read but still occupy 2 bytes.

Running addition: `3D3C` has been corrected to "Unit moves to position(driver, position)", the first parameter is associated with the driver profile, and the confidence level is `structure-confirmed`. The five opening calls of the male super system are shown in [Original Parameter Observation](script-3d3c-runtime.md); the subsequent [Single Parameter Control](script-3d3c-experiment.md) confirms the absolute target change and roster coordinate writing back. Boundaries such as relative position, collision and multiple units with the same number are still to be accepted.

## Event registration types and trigger conditions

`8009DE7C` registers types 0–11 into 12 classification groups (16 items each), and 12–14 into `engine+0x8/0xC/0x10`. `8009E180` calls `8009E3B0` according to the polling phase `+0x9AA` when the event state is idle and `engine+4 = 0xC0`, and each group of trigger functions is given by `jtbl_800D0610` (`8009E308`). The meanings of words 2–5 in the event header are explained by type:

| Type | Trigger condition | Header parameters | Polling |
| ---: | --- | --- | --- |
| 0 | Start of round | Number of rounds (current round ≥; original value calculated from 0, screen round = original value + 1), stage (= `8010F5E8`) | Stage 0 |
| 1 | Delay count (started by `3D52`, decremented by `+0x97E[槽]` every round) | Runtime override | Phase 0 |
| 2 | The unit driven by the character is defeated/retired | Threshold variable (not triggered when 100–115 and equal to 3; set to 3 at the beginning of each level from 100–114, and enabled by writing 0 in the script), character | always |
| 3 | Character HP% ≤ threshold | Character (138 special case: HP < 11), percentage | Always |
| 4 | Engagement event (after combat) | Character A, Character B (0 = any) | Phase 7, status code `0x2002` |
| 5 | Engagement event (before combat) | Character A, Character B | Phase 4, status code `0x2001` |
| 6 | All enemies are destroyed (`+0x9B1 = 0`) | The latest round (the current round is triggered when ≤ this value; the round starts from 0, the screen round = value + 1; 254 = no limit; `8009E834`; in full ROM, only scene 45's `001B42E4` uses 4), stage (4 = any) | Always |
| 7 | Number of remaining factions ≤ N | Faction selection (2 = third party, otherwise enemy), N, stage, threshold variable (the same rule as 2) | Always |
| 8 | Area arrival (requires `3D57` to be enabled) | Round or mode (`FF` triggers when entering; `FE` Each entrant will withdraw from the map immediately, and camp 0 will only trigger when all camp 0 withdraws), N×1000+target, x0×10+width, y0×10+height (range `[x0, x0+宽)`, see below) | Stage 0/1/2/6 |
| 9 | Persuasion: `800A4634` The selected slot is written to `+0x992` | The persuader, object, threshold variable (`FFF8` has no threshold), and threshold value; the persuader also has the number of actions, the slot has not been executed, the threshold is met, and "said" appears only when both parties are adjacent up, down, left, and right, and the first one is taken in the order of registration; when executing, `8009EC3C` changes the slot to `0x2000`, this level no longer matches | The processing function is called in stage 0/1/2/6 and is only executed in stage 6 (set by the "Shuode" command `801DEBF4`) |
| 10 / 11 | Register but not poll | — | None |
| 12 / 13 / 14 | Opening (C1)/Initial configuration (C2)/End (C3, after `3D4A`) | — | `8009EDB8` |

Stage source: `load_000AB160:801DF96C` writes the round, stage and unit numbers of the three camps into the engine before the battle and sets stage 4, `801DF9F8` sets 7 after the battle, `801DEBF4` sets 6, `8020DB08` resets the round to zero when passing the level and sets `engine+4` to C3. The sequence of type 4/5 is judged by the order in which status codes are processed by `801DFEA8`, which is marked as structure confirmation; the code entering C2 has not yet been located, but the contents of the seven type 13 events are all initial deployments of `3D45`. Type 8 area matching is in `800A4288`: target < 500 for character, 500+ camp for any unit of that camp, 21 for captain list `D_800C9A08` (ブライト, シーラ, エレ, Dr. Hazuki, エマリー, ヘンケン...) is the first person present, that is, our flagship. The encoding of the area word is `x0 = 值 / 10`, width = `值 % 10`, covering `[x0, x0 + 宽)`, y is the same; in mode `FE`, the units entering the area are withdrawn according to the exit performance, and the event will only be executed when all camp 0 withdraws (2026-10-01 supplement, the same function).

The first episode of the Female Super Type (Scene Index 1) is interpreted as follows: Type 12 opening dialogue → Type 13 Deployment Group 0–2 → Reinforcement when the enemy remains ≤ 8 / ≤ 6 (Group 3, Group 4) → Ending dialogue when the enemy remains 0 → Type 2 (Malna defeated) → Type 14 Ending Event; `3D4B` Point to scene 4. This is a static interpretation, which is consistent with the existing native running evidence (clearing the first episode), but the game has not been launched in this batch.

2026-09-12 Running Addendum: The new female super-type game actually executes deployment groups 0–2 in the opening event `0019C1B0`, and no separate execution of type 13 events is observed. The event relationship in the above paragraph is a static deduction and cannot be regarded as an actual measured sequence. The complete corresponding results of 123 normal/dialogue commands can be found in [Silent Operation Observation](script-runtime-observation.md).

## Supporting records (attack records)

The supporting data consumed by `3D45` is a 28-byte (14 half-word) record stream, ending with the first word 999. The reading order of `8020ABB4` gives the fields: +0 group number, +2/+4 grid coordinates (`3D3D → 801C78A0` rotates the screen at ×16+32), +6 pilot role (reuse an already assigned airframe in the roster when < 287), +9 level offset (level = `8010F5F3` + offset), +A airframe, +C Reinforcement index (`800CB5DC` → five transformation stages), +14 alignment (3 → 0, 4 → 2), +16/+18 behavioral parameters (+18 writes driver +0x14 when bit 14 is set). +8, +E–+13, +1A Not explained. The sortie position writing chain has been confirmed by the mini-level (2026-09-17, see [mini-level](mini-stage.md)): `3D3D` takes the grid coordinates of the first record of the group as the reference point, and the unit selected for sortie or automatic sortie is put into the empty map slot near the reference point by `801C835C`, slot `+0xB` Note the group number.

A new `stage_deployments` category (6,223 entries) has been added to the directory, each linking the body, character and corresponding block; the scene page lists the groups and corresponding records referenced by the script. The 13 blocks without alignment 999 are truncated at the upper bound and do not add terminators.

## Chapter title and plot viewer

2026-09-12 Reader upgrade: Added full-text search, sentence-by-sentence deep links, compact dialogue, blue/orange speaker distinction, reading preferences and route-relative avatar processing. The current usage, data range and checks can be found in the [Drama Review Station](story-reader.md), and the item-by-item confirmation process for the remaining commands can be found in the [Semantic Confirmation Plan](script-semantics-confirmation.md). The first version implementation and historical verification records are retained below.

The preparation screen `load_0008F4B0:801CE0F8` uses the just-cleared scene index `8010F5F1` plus 281 as the text number to display the chapter title, and the archive list `801C6944/801C754C` uses the same formula for the saved scene bytes (evidence `stage_title_display`). Therefore, the title of scene index n is the text `281 + n`: Scene 0 "戦え!热き血のファイターたち", 1 "出撃!スイームルグ", 4 "Anger りの甲児魔神立つ!"... No. 143 title candidates (423) have no corresponding scenes and are still marked as candidates. Scene and chapter titles in the Table of Contents are now linked to each other.

`tools/data_viewer/web/story.html` uses these data to make a plot viewer: the left column lists chapter titles and sentence numbers according to scene index, and the main column expands the opening, initial configuration, battlefield events (with summary of trigger conditions) and ending events in the order of event entry; each line of dialogue displays the speaker, 96×96 original avatar, and original Japanese text (`<BR>` line breaks, `<STOP>` Displayed as page turn mark) and text number; the protagonist route segments are displayed as paragraph labels, which can be filtered by the four protagonists; system prompts such as condition blocks, selected limbs, appearance groups, and BGM can be hidden. Dynamic name tokens are collapsed into placeholders (such as [Protagonist Name], [Partner Nickname]). The data is written by `src/srw64_native/original_story.py` to `story/index.json` and `story/NNNN.json` during extraction; it only contains the original Japanese text, and the route segments and conditional blocks are not evaluated, so a scene will list the branch text of four routes at the same time, without filtering by the actual game path.

## Implementation and Reproduction

- Layout and evidence lock: `stage_scripts` (schema `srw64.stage-script-layout.v2`) of `config/data/original-jp-v1.json` and 22 new pieces of evidence; when extracting, `verify_vm_tables` checks the machine codes of the distribution table, conditional jump table, scan table and trigger table one by one. If any processing function does not match, the generation will be rejected.
- Parser: `src/srw64_native/original_scripts.py`, called by `tools/content/extract_original.py`; text header provided by `srw64_native.catalog.text_headers`. Story view: `src/srw64_native/original_story.py`, test `tests/test_original_story.py`.
- Page: `tools/data_viewer/web/scripts.js`. New categories `stage_deployments`, `script_conditions`, `script_markers`, `script_event_types`; event pages are indented according to nesting levels, markers are displayed as paragraphs, dialogues display speakers, and scene pages display trigger parameters, route flow, and attack groups.
- Test: `tests/test_original_scripts.py`, covering unknown command non-resynchronization, parameter out-of-bounds, conditional blocks and markers, scan difference detection, speaker rules, machine code tampering rejection, all event byte reorganization, first episode trigger condition and slot link, and attack record byte consistency.

```sh
PYTHONDONTWRITEBYTECODE=1 make check
.venv/bin/python -B tools/content/extract_original.py
python3 -B tools/data_viewer/serve.py --port 59110
```

This batch `make check` passed 90 tests, compileall and dependency checks (`build/original-data-qa/logs/original-data-check-scripts2.log`). After regenerating the directory, check the size of 7,758 output files with SHA-256, 70,043 unique identities, and 202,670 directory links all closed (`build/original-data-qa/verification-scripts-v2.json`, build log `build/original-data-qa/logs/original-data-extract-scripts2.log`). The browser checked scene index 1, event 0019C3BC, conditional command 3E03, and the sortie record page: trigger parameters, indented command sequences, speaker links, route flow, and sortie groups all displayed as expected, and there were no errors in the console. This batch is static extraction and development page verification, and the game is not started.

After the plot viewer and chapter titles are added: `make check` passes 95 tests (`build/original-data-qa/logs/original-data-check-story.log`); the regenerated directory has a total of 7,904 files, 70,044 identities, and 203,238 links all checked and passed, `story/` has 143 files; 142 scenes are all titled, and the plot view has a total of 7,904 files, 70,044 identities, and 203,238 links. There are 34,369 lines of dialogue (scenes with shared scripts are counted separately), 30,753 lines are parsed directly by the speaker, 3,058 lines are parsed by paragraph, 123 lines are divided by the protagonist of the first episode, and 435 lines are still relative to the route. All the dialogues of the parsed speaker have avatar files. Browser check `story.html` Scene 1: The title "DEPU! スイームルグ", the next episode, the protagonist of this episode, the avatar, the speaker, the page turner and the BGM prompt are all displayed correctly, and there are no errors in the console (`build/original-data-qa/verification-scripts-v2.json`).

## Not yet completed

1. Run verification: Add silent script tracking (scene index, event entry, PC, actual executed instructions) to the first episode, and compare it with the static interpretation of this batch; this is the threshold before the analysis results can be used to replace a single event that can be recovered.
2. Commands whose semantics need to be parsed: map performance class overlay function (state machine after `80209DAC`), roster operations `800AA464/800AA62C/800AAD28`, `3E06/3E0D/3E17`–`3E1A`, engine fields and roster fields referenced.
3. The entry path for type 13 events (the writing point of `engine+4 = 0xC2`). (The write point of type 9 index `+0x992` has been solved: `800A4634`, called by building menu `801C9DFC` and executing "Said" `801DECE8`, 2026-10-01.)
4. The purpose of the five digits after the text header, and the actual value of the route relative to the speaker in the common segment (requires runtime `+0x99E`).
5. The scene flow diagram only reflects the `3D4B` parameter and does not include the runtime source of `500` (recovery); the plot viewer cannot yet fold branches according to the actual route, and there is no Chinese translation.