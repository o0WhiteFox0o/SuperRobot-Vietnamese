> **Language / Ngôn ngữ:** [English](mini-stage.en.md) · [Tiếng Việt](mini-stage.vi.md) · [中文](mini-stage.md)

# Mini levels: self-made levels as instruction verification carriers

Updated: 2026-09-16. The goal is to use a self-written mini-level (opening, dialogue, battlefield, battlefield events, ending) to verify the remaining script instructions in the real game process. This page records the first version: the host replaces the compiled level image with the original engine, press F8 from the title main menu and follow the original "New Game → Protagonist Selection → Name → Opening" path to enter.

## How to start the original chapter

- The world map overlay `load_000A7EC0:801C2B9C` or the read path (three places in `800801A4`) calculates the scene index `8010F5F0` and calls the resident `8009DD58(场景, 加载模式)`.
- `8009DD58` → `8009DBE4(场景)` DMA the sortie record block of this scene (≤ 0x2000 bytes) to `80199400`; `8009DC58(栈表, 场景)` DMA the events of this scene (≤ 0x1A00 bytes) to `8019B400`, and write the event pointer table to `8009DD58` Stack buffer (0x100 bytes, ending with −1).
- `8009DE7C(模式, 引擎, 指针表, 出击记录块)` clears 12 groups × 16 slots, registers 0–11 according to the 0th word type of the event header, stores types 12–14 in `engine+8/+C/+10`, and stores the sortie record block pointer in `engine+0` (`3D45` scans 14 half words from here).
- Tactical overlay `load_000AB160:80209D6C` uses `8010F5F0` to look up the table `802195B0` to get the map index and write it to `8010F5EE`.

Therefore, the replacement only requires replacing the pointer table and the contents of the two buffers at the `8009DE7C` entry, and rewriting the map index after `80209D6C`. ROM, directory data and other scenes are not moved.

## Level definition and compilation

`config/recomp/mini-stages/*.json` (schema `srw64.mini-stage.v1`):

- `map`: map index (`base:map_assets`); `slot`: optional, fixed replacement scene index; by default, it replaces the first episode registered after the host is enabled.
- `events`: event list, each item is `type` (0–14), `header` (four parameters, see [Event Registration Type](stage-script-exploration.md#事件登记类型与触发条件) for meaning) and `commands` (the same instruction writing method as [Script Injection Debugging](script-debug-injection.md)). You can also write `copy_from` (`base:stage_events:*`) to copy an original event according to the instruction flow until the end character; at the same time, when giving `header`, only four trigger parameters are replaced and the instruction bytes remain unchanged. This is used to trigger trigger conditions (late rounds, number of clearances) that cannot be reached by bounded operation.
- `deployments_from`: Copy the entire original sortie record block (`base:stage_auxiliary:*`, up to 999); `deployments`: Additional 28-byte record, field name `group/x/y/actor/level_offset/unit/upgrade/faction/behavior/extra`, uninterpreted bytes use `byte8/raw14/raw16/raw18/raw26`, available `template` Specify an original record (`base:stage_deployments:*`) as the base plate.

`tools/recomp/script_lab/mini_stage.py compile 关卡.json --out 镜像.json` generates `srw64.mini-stage-image.v1`: events are spliced according to 4-byte alignment (pointer = `8019B400` + offset), and `03E7 0000` is added at the end of the sortie record block; more than 63 events, 0x1A00 byte events or 0x2000 byte records are rejected.

## Host side

- Switches `SRW64_MINI_STAGE=<镜像路径>`; `src/host/mini_stage.hpp`, called by two wrappers of `game_hooks.cpp`: `resident_func_8009DE7C` (replaces first and then calls the original function) and `load_000AB160_func_80209D6C` (the original function is then overridden `8010F5EE`). Both hooks are bound through `NATIVE_HOOKS` of `generate_cpu.py` and require `make recomp-cpu` to be regenerated.
- Read the image and verify (schema, length, alignment, number of events) during startup; illegal images will cause the host to fail directly.
- Event file `mini-stage-events.jsonl` (schema `srw64.mini-stage-event.v1`): `loaded / applied / skipped / map`, `applied` records scene index, loading mode, pointer table address and original sortie record block address.
- `run_host_probe.py` requires the Japanese version profile and `--graphics`; bounded operation requires `SRW64_SCRIPT_TRACE=1`, and bounded operation with `--audio` must use `SRW64_AUDIO_CAPTURE_FROM/_TO` to give the acquisition window; `--interactive` is not subject to these two restrictions. Report writing `mini_stage`.
- `mini_stage.py report 运行目录 --image 镜像.json` associates the script polling by PC to each event: whether to trigger, the first and last VI, the start/end of each command VI and sampling frame, and unexecuted commands.

## Main menu entry

- Interactive trial: `play_native.py --profile … --mini-stage config/recomp/mini-stages/flow.json` Compile the image and give the path to the host; add "F8: mini stage <name>" to the window title. Press **F8** in the title main menu (opening overlay state 3, that is, "ニューゲーム／コンティニュー..." menu): The host presses START to select a new game for the player, and automatically requests native skip when the prologue text sequence appears (equivalent to R+START), the protagonist selection and name page are operated by the player as usual; when registering the first episode, it is replaced by a mini level, recorded `armed / skip-requested / entered`. Pressing F8 when not in the main menu only records `hotkey-ignored`. The original menu codes and menu items remain unchanged.
- Bounded verification: `SRW64_MINI_STAGE_ARM_VI=<vi>` allows the host to be automatically armed as soon as it reaches the main menu after this VI. Entering the script only requires START twice to reach the main menu, and then provides buttons for protagonist selection and name (`entry-input.json`).
- Unit test `tests/native_mini_stage.cpp` (`make recomp-mini-stage-test`, merged into `recomp-native-check`): image verification, registration replacement, map hook only acts on binding scenes, hotkeys are only armed in the main menu, START maintains four polls, prologue skip count and entry record.

## Smoke level `smoke.json`

Taking the first episode (scene index 1 "Departure! スイームルグ") as the base: the same map (20), a complete copy of its attack records (20 entries, 5 groups), the opening event is cut into 6 lines of dialogue and all structural commands (BGM, world map `3D32`, fade in and fade out, `3D4D` Switch the battlefield, `3D65`, three groups of `3D45` appear, `3D35` scroll), add an additional "First round our phase starts" event that is not in the original story (type 0), retain reinforcements (type 7, enemy ≤ 6), victory (type 7, enemy = 0 → `3D4A`), defeat (type 2, Malina is defeated → `3D4C`) and the end event (type 14 → `3D4B 4`).

Enter script `smoke-input.json`: cold start skip common prologue, female super default name, skip route prologue, then press A every 120 VI.

## Running results

### smoke-1 (`build/recomp/mini-stage/smoke-1`, 14,400 VI, silent)

- The host applies the image (`mini-stage-events.jsonl`: `applied`) in VI 3137 scene index 1, loading mode 0, and the pointer table is in the stack buffer of `8009DD58`; after VI 4669 `80209D6C`, the map index is written as 20 (the same as the original words, used to prove that the hook is effective).
- All 27 commands in the opening event are executed in order (`mini-stage-report.json`): `3D32 4` is completed immediately, `3D32 0` 114 VI (world map positioning), dialogue waiting button, `3D4D` This polling is completed but the next one `3D65` is started after 612 VI (overlay Switching, map loading and title screen), three groups of `3D45` each 422/292/312 VI, `3D35` are completed immediately. Sampling frames: World map highlight (`stage-0-3D32-end_vi-3293.png`), empty battlefield after switching (`stage-0-3D65-end_vi-5245.png`), three groups of enemy and friendly units after appearing (`stage-0-3D45-end_vi-6881.png`).
- The dialogue event only shows the 6 text numbers in the mirror (17410, 17411, 17436, 17460, 17461, 17464), and the lines with the original words cut off do not appear.
- Type 13 initial configuration event is not triggered: the new episode is executed by the opening event itself `3D45`, type 13 is only used in the C2 path, consistent with the original episode.
- Type 0 "Turn ≥ 1, Our Phase" event does not fire: the engine turn count `+0x9AC` is 0 at turn 1 (consistent with the snapshot of the injection run), so the turn parameter of the turn 1 event should be written with 0. `flow.json` has been fixed as such.
- Enemy quantity type, destruction type and end event are not triggered (no combat in this round), `commands_not_executed` lists all their commands.

### flow-1 (`build/recomp/mini-stage/flow-1`, 16,000 VI, mute)

`flow.json` only changes the first round event to "Two lines of dialogue, waiting for 30, `3D4A`", and writes 0 for the round parameters. The result is that the entire level process is completed automatically without fighting:

- The 27 commands in the opening are the same as smoke-1; in the first round, our phase event is triggered at VI 7349 (2 VIs after the end of the opening), `3D3E` 114 VI, `3D3F` 478 VI (waiting button), `3D48`, `3D38 30` 60 VI, `3D4A` 20 VI.
- 38 VI after `3D4A`, type 14 end event fires: `3D3A`, `3D32 1`, `3D33 2` (340 VI, spacecraft movement on the world map, `stage-6-3D33-end_vi-8447.png`), `3D3B`, dialogue, `3D47`, `3D4B 4`, all 8 commands are executed.
- Then enter the original clearance process: The GPU screenshot of VI 15973 `present-7980.png` is the archive screen, showing "Episode 1...スイームルグ クリア総ターン Number 1 Funds 0" and "RecordをUpdateします.よろしいですか?". The next episode (scene 4) has not yet been registered within the VI limit of this round, so there is no `skipped` record.
- Reinforcement, victory (enemy = 0), and defeat events are not triggered: there is no battle this round, and there is no change in the number of enemy troops.

## Command verification level

Item 3, "Verification of the remaining instructions one by one with mini-levels," has begun. The two levels divide the work according to the overlay required by the instruction, and the parameters are all taken from the original script instance; each probe is followed by an `3D38` wait, so that the sampling frame and status snapshot can be attributed to a single instruction.

### Command status snapshot one by one

Switch `SRW64_MINI_STAGE_CAPTURE=1` (requires also `SRW64_STATE_PROBE=1`). `poll_hook` of `mini_stage.hpp` is called by the script polling wrapper of `game_hooks.cpp`: when the script PC falls in the replaced event block and is different from the last time, it saves a region snapshot `state-N-mini-stage-command.json`, `argument` is the offset of the PC relative to the event block, and records the `capture` event. 0 VI is completed and there is no before-and-after comparison for field writing instructions with no screen changes. The host only reads from the PC and does not write anything back.

### `worldmap.json` — World map overlay

The opening event runs before `3D4D` and is the only reachable context of the `load_000A7EC0` world map overlay; the idle judgment injected by the script requires the tactical map and cannot reach here. See [running results worldmap-1](#worldmap-1buildrecompmini-stageworldmap-119000-vi静音).

### `tactical.json` — tactical map overlay

All probes are placed after `3D4D` and `3D45` in the opening event. In the first round, `tactical-1` placed the probe in the "Turn 1 Our Phase" event, but it was not triggered in the whole round: this event requires the player to complete a round, but the bounded input script only presses A, and the operation always stops at the unit selection interface. The opening event does not require player advancement and is the only reliable position in bounded operations.

`3D49` is left alone in `duel.json`: it starts a scripted battle that may eat up the entire VI budget. Actual results are shown below.

## Running results (command verification)

### worldmap-1 (`build/recomp/mini-stage/worldmap-1`, 19,000 VI, silent)

- `3D32` is **World Map Positioning**: the mark is always in the center of the screen, and the map as a whole moves to the position of the item in the table `801C5310`; when the 0th half-word of the table item is different, the entire surface of the land is replaced (Item 2 Mediterranean Sea, Item 19 Coast, Item 46 Snow Mountain, Item 63 Desert). Except for the first call at this location (0 VI), 106 VIs are fixed each time, regardless of distance, and are fixed-length switches.
- `3D31` (the original script has no instance) shares `800A0E64` with `3D32`: `3D31 4` has the same screen as the baseline `3D32 4` and is the same 106 VI.
- `3D33` is **world map movement**: draw a blue and white track moving from the current location to the target, `3D33 2` and `3D33 69` are 316/566 VI respectively, **change with distance**. This is exactly the division of labor with `3D32`: `3D32` changes places and `3D33` performs the moving process.
- `3D5E` 0 VI completes immediately with no changes to the probe area.
- `3D68` here **never completes**, the event stops at this bar: its `80212780`/`80212898` is located in the `load_000AB160` tactical overlay, the VRAM under the world map is not these two functions, and the waiting state machine never advances. Removed from this level and changed to `tactical.json` for verification (87 VI completed normally). This is the level design's fault, not a game flaw.

Table `801C5310` has a total of 127 items (0-126), each item has three signed half words `(地表, x, y)`, and the surface value is 13/14/17/18/19/20; the structure changes from item 127 onwards, and the table ends here.

### tactical-3 (`build/recomp/mini-stage/tactical-3`, 19,000 VI, mute, snapshot-by-snapshot)

All 56 commands in the opening sequence have been executed; 96 step-by-step snapshots. All 12 self-created sortie records appear on the map.

| Command | Parameters | Usage | Observation |
| --- | --- | ---: | --- |
| `3D50` | 95,118,117 / 238,49,48 | 66/66 VI | **Unit deformation**: The roster slot unit pointer moves forward by one record (0x54), the grid coordinates remain unchanged, the unit instance +2 number is 118 → 117, 49 → 48, HP 4300/3800 remains unchanged |
| `3D58` | 31,1 | 0 VI | **Switch camp**: Slot 0/9 cleared, same coordinate (8,14) appears at 1/1, side count 11/1 → 10/2, pilot and machine instances cleared and rebuilt |
| `3D58` | 59,0 | 0 VI | ロザミア is already in slot 0/10 (side 0), writing the current side → No change: **idempotent** |
| `3D5C` | 145,1 | 18 VI | Already combined → No change in roster |
| `3D5C` | 145,0 | 48 VI | **Separation**: Our roster has 10 → 14 slots, the original slot 0/6 body pointer has changed, four new slots appear in the adjacent grid (9,12)/(8,13)/(7,12)/(8,11), that is, コン・バトラーV is divided into five machines |
| `3D6E` | 179 | 0 VI | **Unit exits**: Slot 0/4 cleared, pilot +0x130 1 → 65, body +0x2F8 17 → 58 |
| `3D55` | 4,30 / 31,9 | 424／68 VI | The former moves the camera to the unit and selects it (white frame); the latter makes the unit display a glowing diamond special effect. The second parameter is shown in the table `80217D20` Select the performance to be added to the unit, not just the moving camera |
| `3D36` | 5 / 6 | 18/22 VI | Viewport transition with black border, no change in roster and instance; two values appear in pairs (original script 85/76 times) |
| `3D63` | 145 | 22 VI | Only change roster 1 byte |
| `3D75` | 179 / 999 | 188/188 VI | The time consumption is exactly the same and there is no state change: 999 takes the same path as the actual character, it is pure performance |
| `3D67` | 1 / 4 | 654/896 VI | The two longest performances, no state changes; silent running cannot check the BGM switching |
| `3D68` | — | 87 VI | Complete normally on tactical map, no status change |
| `3D6B` | 165,216,0 / ,1 | 0 VI | Flag 0 has no change; flag 1 is set to driver +0 bit 7, and +0x0C of body instance 0/1/2 is set to 0x40 |
| `3D69` | 4,1 / 4,0 | 0 VI | `4,1` No change (ドモン is in slot 0/8, the two fields are already the same under this value, idempotent); `4,0` sets the roster +0xAB bit 7 and changes the +0x35** of **driver record 12** to 1 Cleared to 0, it is the field predicted by static analysis |
| `3D70` | 181,183 | 0 VI | ショウ has been deployed (slot 0/3), but the character 183 チャム does not appear in all 6,223 original sortie records** and never appears as a map unit; supports the direction of "associated non-sorty role" (co-pilot/partner), no direct evidence this round |
| `3D6F` | 53 / 874 | 0 VI | There is no part record with matching number in this level → No operation |

`3D32`／`3D31`／`3D33`／`3D50`／`3D58`／`3D5C`／`3D6E` was promoted to `code-confirmed` and renamed. Together with the subsequent `3D49`/`3D6F`/`3D70`, the ordinary instructions change from 33 items `code-confirmed`, 19 items `unknown` to **43 items `code-confirmed`, 22 items `structure-confirmed`, 8 items `unknown`**.

### duel-2 → duel-3: `3D49` requires the character to be present and does not need to enter the battle

`3D49 15,16` in duel-2 The host crashes as soon as it starts (`native-run-failed`, exit code −10). The system crash report gives the exact location: the faulting thread stopped at `load_000AB160_func_80211BD0`, called by `80211DA4` (`3D49` handler function), `EXC_BAD_ACCESS / SIGBUS`, address `0x708000002F`.

Reading `80211BD0` shows the reason: it takes the aircraft instance pointer of the roster slot (base address `8015E10C`, side step `0x258`, slot step `0x14`, field `+0x0C`), and then press `+0x2C` Quantity/`+0x30` pointer, step `0x24` Traverse the list of units without verifying the pointer. duel-2 uses the original sortie record block. The レイン and アレンビー named in table `800C9A18` item 15/16 are not in the roster, and it crashes after reading the uninitialized pointer.

**Conclusion: `3D49` Two characters need to appear on the map roster and do not need to enter the battle process first. ** duel-3 After deploying two groups of four characters, the two `3D49` are completed normally with 1572/972 VI respectively, and `exit 0`.

### duel-3 (`build/recomp/mini-stage/duel-3`): `3D49` is a scripted battle show

A complete battle appears on the screen: HP/EN bars of both sides, driver avatars, lines and attack animations - レイン「いくわよっ!!」→ アレンビー「ぎゃあああああっ!!」. The second group is ドモン vs. ゾンビ兵. The result will be written back: the status of the roster slot `0/1` of one side in item 16 changes from 1 to 2 (failed/immovable), and the HP of its aircraft instance `+0x58/+0x59` is reset from 8000 to zero, consistent with the screen `0/8000`; the pilot `+0x35` of one side in item 3 is cleared.

The 4th half-word of the entry is not screen HP (screen 8000/5000, table 32760/10), and its meaning is still unconfirmed. `3D49` was upgraded to `code-confirmed` and renamed "Scripted Combat Performance (Combat List Item A, Combat List Item B)".

### targets-1 (`build/recomp/mini-stage/targets-1`): Add the action object to the no operation

The same line of thought ("No operation = missing object") advances three others. Levels [`targets.json`](../../config/recomp/mini-stages/targets.json) have objectives specifically for them.

- **`3D6F`** was upgraded to `code-confirmed`. Instead, use the original script parameters that actually exist and have been set in the parts table of this level (19/773/775, picked out by the `part_instances` snapshot of tactical-3; the 53/874 used before is not in the table at all): `3D6F 773`/`3D6F 775`. Record the `+0x22` of 31/32 by `0x0C` is changed to `0x08`, which clears bit 2, which is completely consistent with the static analysis `800ACF44`. What matches is the number of record `+2`, not the index.
- **`3D70`** was upgraded to `code-confirmed` and renamed "Mounted Co-Rider Role". In the 10 instances of the original script, it all follows `3D5A`, while the co-passenger character (183 チャム/182 シルキー) does not appear in all 6,223 sortie records, and is registered with `3D5A` with body 999. According to this writing method, first `3D5A 183,0,999,500` creates driver record 7, and then `3D70 181,183`: the record `+0x37` is set to 1, `+0x38` is written into the body instance pointer; at the same time, the **ビルバイン driven by ショウ`+0x34` changes from 1 to 2, `+0x3C` writes the address of driver record 7** - that is, `+0x34` is the number of passengers, and `+0x38` is the driver pointer array (consistent with the basis of `3D55`).
- **`3D69`** is still `unknown`, but the scope of effect has been confirmed: in the level where Leopard Horse attacks, `3D69 145,0` records ** driver 1–5 as `+0x35` Clear all**, that is, all the co-pilots of the unit driven by the character (five people from コン・バトラーV), not a single record. All that is missing is the game name in these two fields.

## Enable audio operation (audio-1 / audio-2)

The semantics of `3D67` is audible but not invisible, so the mini-level's requirement for silence is relaxed: bounded running still requires the script trace to be turned on, but `--audio` can be added, and `SRW64_AUDIO_CAPTURE_FROM/_TO` must be used to specify the VI window for collection. The original collection is fixed to retain the first 30 seconds after the sound is turned on, and the command to be listened to often appears after running for a few minutes; the window logic draws `Srw64AudioCaptureWindow` of `audio_timing.hpp`, which is overwritten by `tests/native_audio_queue.cpp` (skipping before the window, writing in the window, closing once when crossing the boundary, and no longer writing after that, and `to <= from` The degradation window is treated as "windowless" to avoid mistyping the boundary and causing the entire acquisition to be lost).

Level [`audio.json`](../../config/recomp/mini-stages/audio.json) Sandwich each probe between `3D3A 0` (stop BGM), use `3D3A 49` at the beginning as a positive control; [`audio-tail.json`](../../config/recomp/mini-stages/audio-tail.json) just advance the last few probes so that they fall into the same window.

### `3D67` is the debut cut-in performance (promoted to `code-confirmed`)

The four original script values are all sounded, RMS 2301–3092, peak value 15,000–18,000, while the adjacent silent segment is only RMS 84–139, and is louder than the control BGM (RMS 1328). The picture gives the exact meaning: a body appears in the center of the screen passing through the same light speed tunnel background - 0 is a blue and red model, 1 is gray and red, 3 is green, 4 is orange and red, **different**.

The spectrum of 1/3/4 is highly similar to the envelope (cosine 0.96–0.99, envelope correlation 0.93–0.99, because of the shared tunnel background), but the sample level correlation is only **+0.007** and no alignment displacement can be found, which is different audio for different aircraft; duration 10.87/13.93/14.93 seconds. 0 has a significantly different spectrum (cosine 0.42–0.46 to the other three), no 0.75 second prelude, and a duration of 16.03 seconds.

This is completely consistent with the only two ways of writing in the original script: `3D4E → 3D67 n → 3D38 → 3D45 <组>` (before reinforcements appear) and `3D54 145 → 3D35 → 3D67 0 → 3D5C 145,1` (before integration).

### The remaining four: three are confirmed to be silent, and one has sound effects.

| Command | RMS (within window) | Conclusion |
| --- | ---: | --- |
| Control BGM `3D3A 49` | 1328 | Positive control, proving that the collection is effective |
| Silent segment | 3.0 | Digital silent noise floor |
| `3D75 145` | 3.0 | **Completely silent**, no state, no visible changes |
| `3D68` | 3.0 | **Completely silent** |
| `3D36 5+6` | 3.0 | **Completely silent** |
| `3D63 145` | 48 (peak 541) | **With sound effects**, significantly higher than the noise floor but well below the BGM |

`3D68` was finalized by frame-by-frame comparison and upgraded to `code-confirmed`: before execution, the screen was offset, with black borders, and the cursor stopped at the enemy unit in the distance; after execution, the screen was centered to the selected unit, a white selection box appeared, and the black borders disappeared - **The camera pulled back to the selected unit**.

`3D63` is set to a short unit animation with sound effects: the `+1` bytes of roster slot `0/0` are 2 → 5 → 1 during the command and are the status of the animation in execution rather than a persistent flag.

`3D75` The three-round running time is always 188 VI, no status is written, no sound is made, and no screen changes can be seen in this level, it is still `unknown` - it probably requires a specific unit state to appear. (Later it was finalized: the mother ship needs to have carrying units, see the section "`3D75`: Release carrying units from the mother ship".)

## Backwards from the original call point (stage_script.py)

The most effective round is not to construct the scene, but to read and use the original script. `tools/recomp/script_lab/stage_script.py` has two subcommands: `show <场景>` prints all the events of an episode in reading order (commands, parameters, dialogue text and speakers have been parsed), `usage <操作码>` lists where the command is called in all 1,812 events with three contexts before and after. Reproduction according to the real call point is much more reliable than self-made parameters - this is how the following five items are finalized.

### `3D5E` = Open the unit name input interface

The 3 call shapes in the original script are exactly the same: マナミ says "マーチウィンド? うーん, もう小し比の名がいいわね", アムロAsk "なら, 君はどんな久名がいいんだい?", and then `3D5E`. After reproducing in this way, the sampled frame directly gives the answer - the screen is "The name of the unit is してください", the unit name column is pre-filled with the default name, and below it is the kana input panel and "Decision". The event is suspended here waiting for player input. Bounded operation has no input and will never continue. (The original note here is pre-filled as "アーチウィンド"; on 2026-09-27, according to the default name form `801C6F54` and word selection list id `801C6F64` of ROM, it was corrected toマーチウィンド. For the complete process, see [Fixed Troop Name](../native/fixed-unit-name.md): This page is no longer open in the game host, `3D5E` does nothing, test level `config/recomp/mini-stages/unit-name.json`).

**At the same time, an old conclusion is corrected**: The previous record "`3D68` will never be completed under the world map" is not true. The opening event of worldmap-1 actually stops at the earlier `3D5E` (named interface hangs), and `3D68` is not executed at all.

### `3D69` = Set unit action status

The calling point first gives the direction: the value 0 appears in the scene where Leopard Horse is restrained (immediately after the lines "うぅ...しまった...体が..." and the enemy "とどめを, さしておやり!!") and the NPC is moved to position and stabilized using `3D3C`; the value 1 Appears after ヒイロ is about to activate his spirit and his masterpiece exits.

The lens is locked on the unit and measured pixel by pixel to give a final conclusion: the brightness of the 12×12 area where the sprite is located is **97.12 → (value 0) 91.23 → (value 1) 97.12**, each state lasts for 12 consecutive frames min = max (no standby animation noise), and the full frame brightness is almost unchanged - the change is limited to the unit sprite, which is the darkening performance of the "acted" unit in this game. At the same time, the roster `+0x0B` is set to position 7 and the driver `+0x35` is cleared, which affects all co-drivers in the unit.

### `3D36` = Screen shake

Frame-by-frame sampling finalization: `mean_delta` jumps from 0 to 23.65 during the command and remains constant, while `mean_rgb` alternates frame-by-frame between 56.53 and 50.37 (54.23 when at rest, i.e. swinging on either side of the rest bit). The constant inter-frame difference is combined with the alternation of two values, which means that the picture reciprocates between the two positions frame by frame. Almost all of the 196 places in the original script are "`3D39` sound effects → `3D36 n` → character surprise lines". The parameters determine the duration: 5 → 18 VI, 6 → 22 VI, both accounting for 161 times.

### `3D6B` = Select mark switch

Reproduce according to the original call point (event 001AB86C: `3D6B 124,171,0` immediately follows `3D5A 124,0,174,171`, リョウ is transferred from ゲッター1 to ゲッタードラゴン). The snapshots give the division of labor one by one: After the execution of `3D6B`, the aircraft number in the roster ** remains unchanged **, and the transfer is completely completed by the subsequent `3D5A`; similarly, after `3D6B 165,216,1`, Wan Zhang is still on the roster, and it is the subsequent `3D46` that makes him disappear.

Static cross-reference completion consumer: `resident_func_800AD990` - the same function called by `3D73` "Group by fixed role list" - first traverse and clear bit 7 (`andi 0x7F`) and bit 6 (`andi 0xBF`) of driver `+0`, and then set the entries with matching numbers in the list 7(`ori 0x80`). This pair is the "selected/registered" flag: `3D73` for the entire batch, `3D6B` for the individual combinations set or cleared.

### Exclusions

`3D69` is not a combination and separation: the same character and the same shot are executed back to back, `3D69 145,0` The number of our front and rear slots remains unchanged (2 → 2), and the subsequent `3D5C 145,0` allows four separate units to appear around the main body (2 → 6). It's not a change of body either: after five calls to Aアルベルト/シュバルツ (both of them have other body entries named after themselves), not a single body number in the roster has changed.

## Improve testing efficiency

Two expenses previously occupied every round: going through the title process, and running through the entire VI budget.

### Enter without title F8 (`--save-from` does not read files)

No need to press F8 from the title to skip the prologue. Run with `--save-from` and the input script, the mini-level will still be replaced when registering the scene for the first time:

```sh
SRW64_MINI_STAGE=<镜像> SRW64_SCRIPT_TRACE=1 \
  .venv/bin/python tools/recomp/run/run_host_probe.py --graphics --profile config/recomp/profiles/play-profile.json \
  --language ja --images original --resolution-scale 2 --original-name-entry --input <输入脚本> \
  --save-from build/recomp/save-recovery-check/intermission-cold-1.source.sram \
  --save-sha256 0c6ded15fdf60c6b0064b2260a335d17a4ff77386d14d634bfd7d3bcb8de7484 \
  --output <运行目录> --vis 19000
```

This does not require `SRW64_MINI_STAGE_ARM_VI`, and `armed`/`skip-requested`/`entered` will not appear in the event file. The advantage is just to omit the title F8 and the prologue:

- This path **does not read the archive** (Corrected on 2026-09-18; earlier I thought it would read the archive and skip the naming), `--save-from` just copies the SRAM into the running directory. The title button of `dense-input.json` is ニューゲーム, and the replacement is **Scene 1** (if you really read the first episode, the next episode should be Scene 4), and the `intermission-restored`/`tactical-restored` status snapshot will not appear during operation.
- The operation will still pass through the name page. The existing scripts such as `dense-input.json` rely on the keys of the original kana disk to pass it, so `--original-name-entry` must be added. Without adding time for the modern name page to take over the input, the execution will always stop on the name overlay (`001090A0`) and the scene will not be registered (this is the case for rules-2).
- **The persistent data in the archive (number of kills, flags, funds, composition) are the initial values of the new game in this run**: The new game will call `800A4F94` and other initializations, `wufei-dummy-original-1` is like this, and the modified backup archive will not take effect at all. When you need to archive content, you need to use the input script that actually goes to the Load menu (such as the path of `config/recomp/inputs/load-intermission-check.json`), or create the required state yourself in the level like `wufei-dummy.json`.

### Exit after the command is triggered

`SRW64_MINI_STAGE_EXIT_AFTER=<操作码>` (hex) Causes execution of `SRW64_MINI_STAGE_EXIT_GRACE` VIs (default 300) after this opcode is reached. The grace period is to allow the effects of the command and subsequent frames to still be captured.

Actual measurement: scene78-turn level verification `3D75`/`3D46`, originally ran to 19,000 VIs, changed to `EXIT_AFTER=3D46 EXIT_GRACE=400` and ended at **7,416 VI** (the event file records `exit-armed` in VI 7016, `exit` in 7416), running 61% less. The report is generated as usual, except that subsequent unexecuted instructions will be listed truthfully in `commands_not_executed`.

Exiting observation and taking snapshots one by one are independent of deduplication: the observer uses `exit_seen` to self-lock and does not share the collection boundary for deduplication - otherwise, opening the collection midway will lose the boundary that the observer has passed. The unit tests cover this, as well as "only exit on the specified opcode" and "only trigger once".

### Probe added to the engine block

The status probe originally covered areas such as rosters, pilots, airframes, parts, etc., but the block for the engine itself was not among them - it fell right in the gap between the roster (to `0x8015E808`) and the airframe instance (from `0x8016A210`). So the instruction that only writes the engine field has no trace in all snapshots, and it reads like it did nothing.

After adding `script_engine` (`0x8015F950`, 0xA00 byte), `3D66` immediately appears: `3D66 1` changes `engine+0x997` from `0x1F` to `0x9F` (set bit 7), `3D66 0` changes back to `0x1F`, which is completely symmetrical and consistent with the static description. There are another 6 bytes changing at the same time, but the two conversions are exactly the same. It is polling bookkeeping that is activated by every command of the engine.

Use the regional difference chart on the screen side to verify: the difference between "off → on" and the control group "off → off again" is 2.8/3.1 (the same diagonal band, which is standby animation noise), that is, the switch itself does not change the screen. The consumer of this bit has not yet been confirmed, so it remains `structure-confirmed`.

This blind spot also means that all the previous conclusions of "zero change in the entire probe area" are not valid for the **write only engine field** instruction, so it has been re-read.

#### Distinguish between bookkeeping and instruction effects

There is a section in the engine block (about `+0x966`–`+0x97B`) that is the working status of the script virtual machine itself. Almost every command will change: `+0x967` has changed 100%, `+0x96D` 74%, and `+0x97A/+0x97B` among the 90 conversions in scene78t-3. 51%. Exclude "bytes with an occurrence rate of more than 20%" as bookkeeping, and the rest is the instruction effect. This criterion has cross-validation: `+0x997` (bit 7 of `3D66`) only changes 5 times in the same round, which is exactly where `3D66` is in the scene; `+0x9B0` only changes 4 times, which is the unit count of `3D46` decrementing - both rare and specific.

#### Retest results

- `3D75` (scene78t-3, real context): The engine block only moved `+0x96D` (74% bookkeeping) during the span. **After covering all areas, there is still no exclusive write**, and the conclusion of the first six rounds is established.
- `3D63` (scene80-2, real context): The only exclusive write is still the roster slot `+0x001` (2 → 5 → 1), no change to the engine block. Hidden engine-side effects are excluded.
- The following `3D69 145,0` in the same round is written again consistent with act-1, which can be used for cross-validation.

## Structure confirmed → Code confirmed (2026-09-17)

Supplementally test the instructions of `structure-confirmed` one by one. The method is the same as before: first use `stage_script.py usage` to read the original call point, and then reproduce it according to the original sequence. Use snapshots one by one, sampling frame by frame and static code reading to confirm each other. All 21 articles have been finalized:

| Directive | Effect | Decisive evidence |
| --- | --- | --- |
| `3D65` | Set victory/defeat conditions | Two 7-bit fields are text numbers (0x15BF+high, 0x15D9+low), 17 = "The enemy's total destruction", 31 = "The protagonist's machine is destroyed"; read 17/31 when running |
| `3D72` | Set the world map travel vehicle | `engine+0x990` = parameter mod 15, and the table `D_801C5644` has exactly 15 items; the table value is the subscript of the world map model table `801C5670` (14 →ラー・カイラム, see [World Map Cut Scene Model HD](../native/native-ship-model.md)), not a character number |
| `3D73` | Troop division: Select according to the default list | 3D73 1 Select only Wan Zhang and Hura in list A, and do not select Kura - consistent with the line "Kara will stay" |
| `3D74` | Clear all team selection marks | Clear the marks of four people in both executions |
| `3D37` | Map special effects overlay | Screenshot: No. 0 big explosion, 1 bombed spark, 11 blue shield halo |
| `3D4F` | Unit destroyed | HP 7800→0, roster status 1→2, unit remains in the roster; compared to 3D46, the entire line is deleted |
| `3D60` | Our troops are in formation | Four scattered units are gathered into a staggered formation at (5,5), and the enemy is stationary |
| `3D56` | Highlighted green target area | Screenshot: The flashing green rectangle, which is "グリーンエリア" in the victory condition |
| `3D35` | Lens scroll (position, wait flag) | The first word is the wait flag, not the speed; relative to the upper/lower/left 3 frames each |
| `3D5A` | Troop formation (five modes) | 500 registration, <2000 transfer, 2000 driver removal, 4000 removal together; 3000 are all invalid calls in the original script |
| `3D4D` | Switch from the world map to the battlefield | `engine+4` changes from 0xC1 to 0x03, and then about 612 VIs switch to overlay |
| `3D64` | Remove co-driver | 500,500 Special case: Link アイシャ to マナミ's スイームルグS, replacing ローレンス |
| `3D5D` | Set the form of the combined robot | The 1st character selects the family (ダンクーガ／コン・バトラーV), the 0th character selects fusion or separation, the two are mutually exclusive |
| `3D6A` | ゴッドマーズ Fusion processing | Mode 3 delete ガイヤー, change the name to ゴッドマーズ; the fusion animation will only play when ガイヤー HP < 11 |
| `3D51` | Launch MAP weapons | The original name "Move to coordinates" is wrong: the second word is all MAP weapons (バスターライフルMAP, etc.); the screenshot shows launching energy balls |
| `3D3C` | The unit moves to the position | Supplementary measurement of the relative position: Right 2, Bottom 2, and the same position are all accurate |
| `3D71` | Entering the ending | The screenshot is the ending text; must be executed on the world map |
| `3D61` | Pause the judgment of "all our units are destroyed or defeated" | Comparison of parameters only: when the value is 0, GAME OVER will appear after the only friendly unit is defeated, when the value is 1, the event will be executed as usual and our turn will be entered |
| `3D66` | Does not automatically move the camera to the speaker during dialogue | The only difference is parameter comparison: when the value is 0, the camera jumps to the two speakers before the two lines of dialogue, and when the value is 1, the camera stops where it is |
| `3D3D` | Sortie (0 units select mothership/200 automatically/the rest open sortie selection interface) | Three verification levels: interface, mothership selection, automatic sortie all appear according to parameters, units fall near the base group |
| `3D59` | No attack allowed (exclusion list) | Only parameter comparison: whoever is excluded will disappear from the attack list |

Two points deserve separate explanation:

- **`3D5A` Mode 3000 is an invalid call to the original**. The dispatch function skips two removal calls when the role is 999. However, all five 3000 calls in the original script are called with the role 999. The list remains completely unchanged before and after the actual measurement.
- **`3D56` was not drawn the first time** because the position of the rectangle depends on the lens; according to the original script, first use `3D35` to roll the lens into place and then it will be displayed. **When verifying performance instructions, the lens settings before it must be copied. **
- The original name of **`3D51` is wrong**. The structural layer only sees that it "finds the map slot of the character + body and drives the movement", but when the value of the second word is checked in the weapon table, it is all MAP weapons.
- **`3D71` Misplaced overlay will cause the host to abort**. The `801C51B4` it calls only exists in the world map overlay, and the function lookup fails (`get_function` assertion) when executed on the tactical map. This is the same situation as `3D68` earlier: the command is tested in the overlay it belongs to.

### `3D61`: Find the reader and do a comparison with only one parameter difference

The write is already acknowledged (`engine+0x996` bit 15), all that's missing is who reads it. Searching for `0x2E6(`/`0x996(` in recompiled C, there are only four reading points: `800A3524` for winning and losing conditions (mask `0x7F7F` excludes bit 15 and bit 7), area trigger `800A4288` (set 15), debugging display `80208D80`, and `801FF934` for tactical overlays:

```c
// load_000AB160_func_801FF934(kind, unit)
if (kind == 0) {                       // 全灭判定
    if (unit_count[side 0] /*0x80172EDC*/ != 0) return 0;
    return (engine[0x996] & 0x8000) == 0;   // 位 15 置位时不算全灭
}
/* kind != 0：逐台「须保护的机体」被击破判定，与位 15 无关 */
```

`801D5898`/`801D90C4` is called when `801FF934(0)` is true: BGM is stopped and tactical status `0x80172EB0` is set to `0x54`, which is the defeat process. Based on this, allost-0/allost-1 is done: our team only deploys アレンビー, the enemy's レイン, the defeat condition is set to "Ajika's total destruction", `3D61 x` and then use the script to fight `3D49 15,16` to let アレンビーBeing defeated, the difference between the two levels is only x.

| 3D61 | Number of our units | Tactical status | Screen | Opening execution |
| --- | --- | --- | --- | --- |
| 0 | 1 → 0 | `0x05` → `0x54` | White flash, star stream, "GAME OVER", then leaving the level | 9 out of 11, then interrupted by the defeat process |
| 1 | 1 → 0 | Keep `0x05` | After the event is executed, enter our turn ("フェイズEnd" menu) | All 11 items |

So `3D61 1` is "suspend the judgment of total destruction of our team". The 7 usages of the original script are all correct: Scene 32 uses 1/0 to cover the scripted battle between the enemies; Scene 78 is set in the opening before our side attacks, and cleared at the end of the opening; Scene 11 (our side has no units in the opening) is set in the opening, and cleared before `3D4C` (the end of the game). The area trigger `800A4288` also sets the position when our unit leaves the field. The reason is the same - the last unit evacuating does not count as total destruction.

### `3D66`: The reader is hidden in the pointer of the virtual machine context

Directly searching for the `0x996` offset cannot find the reader of bit 7. The reason is that the script virtual machine context `+0xC` stores `&engine+0x994` and reads `(ctx->[+0xC])[+2]`. Search according to this shape and get `800A3530` (return `& 0x80`). The only caller is the pre-step `8009F4B4` of the dialogue instruction `3D3E`/`3D40`:

```c
// resident_func_8009F4B4(ctx, window)，3D3E = window 0，3D40 = window 1
if (first_frame && on_tactical_map) {
    speaker = text_speaker(text_id);                  // 8008CE54
    slot = find_unit_slot(speaker, engine[0x996] & 0x80);   // 800A2C18
    if (slot)            camera_target = slot->x, slot->y;
    else if (mode == 0)  camera_target = fallback_position(speaker);  // 800A3854
}
if (camera_target set) { if (scroll_camera_to(target)) clear target; }   // 80209DAC
else if (show_dialogue(window, text_id) == done) pc += 2;              // 8008FED4
```

`800A2C18` always returns 0 when using `0x80` as mode, so setting bit 7 means "dialogue does not follow the speaker". focus-0/focus-1 only lacks the parameters of `3D66`: the two speakers are located at the upper left and lower right of the map, and the camera first stops between them.

| 3D66 | アレンビー Before speaking | レイン Before speaking | Frame by frame displacement |
| --- | --- | --- | --- |
| 0 | The camera jumps to her unit in the upper left corner | The camera jumps to her unit in the lower right corner | Two full frame jumps (VI 4907, 5094) |
| 1 | The camera does not move | The camera does not move | 0 |

In the original script, `3D66 1`/`0` are strictly paired, always covering "`3D35` scroll + dialogue" - first put the camera to the position to be shown, and then let the characters outside the screen speak without being pulled away. The earlier isolated experiment had no dialogue in between, so no changes were visible. **Write only the engine field switch, you need to find its reader, and then put the context required by the reader (here, dialogue) into the level, then the effect will be visible. **

### `3D59`／`3D3D`: Attack selection

After adding `8015F700` to the probe, it is known that `3D59` adds characters to the list and `3D3D` is read and cleared, but scene8-2 never enters the attack selection interface. Read `3D3D` (`800A09D0`) and the `801C78A0` it calls to figure out the reason:

```c
// 3D3D w0,w1,w2,w3,w4
wait(10);
base = first deployment record whose group == w4;       // w0/w1 不读，原脚本抄的是基准坐标
n = (w3 != 0 && w3 != 200 && w3 >= 16) ? 15 : w3;        // 100 实为 15
801C78A0(base.x, base.y, w2, n, w4);
if (w3) unit_list_8015F700 = {-1};

// 801C78A0：候选 = 我方机体库里 +0xC 有 0x80、驾驶员不在场、且不在 8015F700 名单里的机体
if (candidates == 0)      state = 5;                     // 什么都不做
else if (n == 0)          pick_mothership();             // 只看 +0x28 0x80000；唯一候选直接定
else if (n == 200)        select_all(); deploy();         // 不开界面
else                      open_sortie_screen(min(candidates, n));   // 战术状态 2
```

During the state 2 (selection interface) and state 3 (transfer stage by stage), the tactical main loop does not advance the script and returns to state 5 before continuing - `3D3D` itself is not blocked, but the entire script is frozen. The list of scene8 is `3D59 46`. At that time, our aircraft library only had the mothership of ブライト, and the number of candidates was 0, so nothing happened. **`8015F700` is an exclusion list: `3D59` is "not allowed to attack", not "must attack". **

Three levels are used for verification. At the beginning, `3D5A` is used to register the two candidates ドモン and ヒイロ:

| Level | Command | Result |
| --- | --- | --- |
| sortie-a | `3D59 95`, `3D3D 8,8,0,1,2` | There is only ドモン in the list of "これでよろしいですか?" → (8,8) Teleport appearance, script Continued after 384 VI |
| sortie-b | Just change `3D59` to 4 | There is only ヒイロ's ウイングゼロ in the list, and the one who appears is ヒイロ |
| sortie-c | `3D5A 46,0,52,500`, `3D3D 5,10,0,0,3`, `3D3D 8,8,0,200,2` | No exiting the interface in two steps: アウドムラ enters the mothership table and appears at (5,10); then ドモン and ヒイロ appear at (8,8)/(8,6) Automatically appear |

The status sequence given by the snapshots one by one is consistent with the code: a/b is `05 → 02 → 05`, c is `05 → 03 → 05` twice; the map slot `+0xB` of the appearing unit is equal to the base group number, and the driver's presence status `8015DE90[角色]` changes from -1 to 1.

There are 216 `3D3D` in the original script, 193 of which are in the opening, all after `3D4D`; in the third word, there are 85 places for 0, 100 for 100, and 21 for 200 (scenes 4–10). The most common one is 0 first and then 100. Use both together: select the mothership first, then select the attacking unit.

The probe adds five more areas for this purpose: `sortie_candidates` (`0x8015DA08`, candidate list and number of candidates), `pilot_map_state` (`0x8015DE90`, each character -1 not present/1 present/2 Retreat), `ship_table` (`0x8015E850`), `sortie_selection` (`0x80223538`, selected flag, pointer, upper limit and selected number), `sortie_base` (`0x802279E8`, reference point).

While reading the code, I discovered by the way: `8009EDB8` runs type 13 events when `engine+4 == 0xC2`, but there is no place where `0xC2` is found in the generated code. The 7 events of type 13 (all `3D45`) will probably not be executed in the formal process. There is only static evidence of this.

At this point, all 21 `structure-confirmed` general instructions have been finalized.

## `3D75`: Release the mounted unit from the mothership (2026-09-17)

The first seven rounds have been unable to measure the effect. After reading `80213758`/`80213AAC`, you will know the reason: it deals with the units carried in the mothership, and the motherships in the first seven rounds did not have any units.

```c
// 3D75 actor
if (actor == 999) actor = 46;
if (actor in captains /*8021E398: ブライト シーラ エレ 葉月博士 エマリー ヘンケン ハワード*/)
    select every unit aboard that captain's ship;          // 母舰表 8015E85C/60，搭载表 8015E864
else
    select the actor's unit if it is aboard either ship;   // 否则什么也不做
every 4 frames: place one selected unit next to the ship, remove it from the aboard list,
                play SE 0xD1, player unit count += 1;        // 80213AAC
```

Loading is only done by the player's movement commands (`801CD0E4 → 801EAF88`). There are no script commands to allow units to board the ship, so launch-1 uses buttons to drive player operations for the first time (`config/recomp/inputs/mini-stages/launch-input.json`):

1. Opening: `3D5A` registers ブライト＋アウドムラ and ドモン, `3D3D …,0,3` lets アウドムラ enter the mothership table and appear on (5,10), `3D3D …,200,2` Let ドモン stand to the right of it.
2. Our phase: Move the cursor to the right to select ドモン → "Move" → Move to the left to the mothership grid → The "Mount" prompt will appear (when the cursor is on the ship grid in the move selection state, `0x80172EB2 == 4` is not a menu item) → Confirm.ドモン disappears from the map, the number of carried `8015E858` 0 → 1.
3. Map menu "フェイズEnd" → "はい".
4. The event at the beginning of the enemy phase in turn 1 (type 0, head `[0,2]`) executes `3D75 999`.

| | Before execution (VI 6495) | After execution (VI 6751) |
| --- | --- | --- |
| Our map slot | Only アウドムラ (5,10) | Extra ドモン (5,8), group number 2 |
| Number of carried | 1 | 0 |
| Number of our units | 1 | 2 |
| Screen | — | The camera moves to the mothership, a purple forward effect appears above it, and ドモン appears above the mothership |

In the original script, `3D75` is always before the captain or character leaves: シーラ, エレ returns to バイストンウェル, ブライトBefore leaving the Rura, you must first release the units in the ship, so as not to leave with the mother ship. The "disappear, leave the battlefield" seen in the actual video is followed by `3D46`; when there are no units in the ship, or non-captain characters are not mounted on the mothership, `3D75` does nothing - this is the case in the first seven rounds and in most videos.

Two pitfalls that were clarified by the way:

- **The turn number of the type 0 event header is compared with `8010F5EA`, which starts from 0**: the first turn is 0, and the "ターン number 2" on the screen is 1. The head `[1,2]` (enemy phase in round 2) and `[2,1]` (friendly phase in round 3) will not be triggered in rounds 1 and 2.
- ** (Supplemented on 2026-09-18) Directly `3D5A … 4000`** for units still on the map: the pilot and aircraft records are cleared, but the roster slots still point to them; if this level continues to be handed over to the player, SIGBUS will occur when traversing the roster (`801FD020`→`801EB344`, see `wufei-dummy-original-3`). Use `3D46 角色,1` first to make it exit and then `4000`. In the original script, such removal occurs at the end of the level event or at the beginning, and will not return to the operating state in the same level.
- **The real reason why "turn events are not triggered in bounded runs" before**: The headers of the turn events of those levels are written with `[0,0,0,0]`, and stage 0 is never equal to 1/2. Scene 78 After that round was changed to `[0,1]`, it was triggered in the first round of our phase.

## `3D63`: Landing/flight switching (2026-09-17)

There is only one scene 80 in the whole game: `3D37 0` (explosion on leopard horse) → `3D63 145` → `3D69 145,0` → "うぅ...しまった...体が...". It looks like "immobility", but that's what `3D69` does. In order to see it separately, I made a level that can be played manually `hyoma-3d63`: only deploy the leopard horse (scene 80 own record, バトルジェット), and each time "フェイズEnd" is pressed, a step is executed at the beginning of the next round.

| Round | Execution | Roster `+1` | Screen | Can Action |
| --- | --- | --- | --- | --- |
| 1 (after deployment) | — | 2 | Hanging in the air, with a shadow below | Can |
| 2 | `3D63 145` | 2 → (5) → 1 | Fall to the ground, the shadow disappears | Ability (press A to enter "Movement/Spirit/Ability") |
| 3 | `3D63 145` | 1 → (7) → 2 | Lift back into the air | Can |
| 4 | Original sequence (explosion, `3D63`, `3D69 145,0`, lines) | 2 → (5) → 1 | Landing | Cannot (press A to see only ability) |
| 5 | `3D69 145,1` | — | — | Restore |

The code matches: `80212290` reads the height of the unit 3D model. When it is equal to 5.0 (hanging), the landing animation of mode 5/9 is played according to the terrain. Otherwise, the take-off animation of mode 7/0xA is played, using the same animation function `801F1C48` for the player's flight/landing command. So scene 80 is a two-step process of "shot down → unable to move".

Interactive play:

```sh
.venv/bin/python tools/recomp/run/play_native.py --profile config/recomp/profiles/play-profile.json --language ja --images original --mini-stage config/recomp/mini-stages/hyoma-3d63.json
```

Press F8 to enter the main menu; press Z in a blank area of the map to open the menu → "フェイズEnd" → "はい". Use `hyoma-3d63-input.json` for bounded verification (key presses after the 4th round will stop in the ability screen, and the 5th round will only be verified manually).

So far, all 73 ordinary instructions are `code-confirmed`.

## Next step

1. Visible menu items of the main menu: The current entrance is the F8 hotkey on the main menu and the window title prompt; drawing native menu items on the title screen requires a native drawing path outside the dialogue layer.
2. Chapter title and custom text: The title is text `281 + 场景索引`, and the dialogue can only reference the existing text number; custom text requires the overlay entry of the host text layer.
3. The common commands no longer have `unknown`; `3D69`/`3D6B`. The exact fields (pilot `+0x34/+0x35`, machine body `+0x0C`) have been located. What is missing is the consumer chasing these bits - these two are static cross-references, and the mini-level has already given out all that it can provide.
4. The item-by-item correspondence between the second parameter of `3D55` and the table `80217D20`, and the open and closed interface layer of `3D36` still require special experiments.

## Direct entry and runtime loading (2026-09-21)

Mini-levels are debugging facilities and no longer go through the new game process. After the main menu is armed (button, F8, `SRW64_MINI_STAGE_ARM_VI` or runtime loading), the host returns control at the game thread's frame boundary (`80085F30` wrapper) by the title overlay's own exit sequence: `800836CC(0)` → `800A5138()` (game state reset on return to title, internal `800814F0` Will clear the scene number) → write `8010F5F0 = 场景`, `8010F5EF = 1` → `80080188(0xC)` → `8007F510(0x800801A4, 0, 1)`. This is the same as the interfield "next level" exit `801D8D20` (`801D8D94` at `set_mode(0xC)`): top distributor `800801A4` press `8015DA02 - 1` table lookup, mode 12 into `801C2D30 → 801C2B9C(0)`; `8010F5EF` non-0 When `801C2B9C` is used directly, `8010F5F0` is no longer used to calculate the scene (scenario 253 will be obtained when not initialized). Then `8009DD58 → 8009DE7C` registers the scene and the image is replaced as usual.

Actual measurement (`battle-ui-skills`, 60 VI/s): Click to the mirror application 6 VI, the map appears in about 1.4 seconds, and the mask black screen takes about 0.3 seconds; the old path (new game → Prologue A → Protagonist/Name → Prologue B) is 688 VI, about 12 seconds. The opening script of the level itself (`3D4D` about 612 VIs, two `3D45` about 292 VIs each, etc.) remains unchanged, and it takes about 26 seconds to be ready when clicked (original 38 seconds). `SRW64_MINI_STAGE_DIRECT=0` Keep the old path. Without going through the name page, the protagonist's name and route variables remain empty after reset; levels that require them should be set up with their own scripts, or use the old path.

Advancing the entry timing by about 700 VI will change the RNG state, and the enemy's attack targets and order will change accordingly; the counterattack section of `check_battle_actions.py` has been changed to perform corresponding checks based on the actual defender (25 items passed, exit code 0, `build/recomp/debug/20260921T083602.242953Z/`).

**Load any local level file at runtime**: When the title main menu is displayed,
- Debug interface `mini_stage.load {"path": ...}` (`srw64_mini_stage_load` for MCP), or
- When the debugging interface is turned on (`--debug`, or set the debugging interface switch on the "About" page), drag the level file to the game window (SDL drag and drop event; success or failure is displayed in the notification bar).

There is no entrance to the mini-level in normal play (2026-10-06 user-defined): Drag and drop does not load when the debugging interface is closed; F8 and "Enter mini-level" on the title only appear when the level has been loaded, and the level can only be loaded through the debugging interface or development tools (`play_native.py --mini-stage`, `srw64ctl launch --mini-stage`).

The compiled image (`srw64.mini-stage-image.v1`) is loaded directly; the level source file (`srw64.mini-stage.v1`) is first compiled to `runtime-mini-stage-N.json` in the running directory through `SRW64_MINI_STAGE_COMPILER` (the launcher is set to shell-escaped `python tools/recomp/script_lab/mini_stage.py`), and the compilation output is in `runtime-mini-stage-compile.log`. Loading replaces the current image, resets bindings, and immediately arms entry; no need to start with `SRW64_MINI_STAGE`. Non-title menus, unreadable files, and compilation failures are all rejected and the reasons are given. Verification: Launch without level, pre-title menu load rejected, missing file rejected, ready 26.1 seconds after loading `battle-ui.json` source file, exit code 0 (`build/recomp/debug/20260921T083917.598168Z/`). The drag-and-drop path shares `mini_stage::load_file` with the debugging command, and the drag-and-drop event itself is not automatically verified.