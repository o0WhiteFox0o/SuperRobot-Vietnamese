> **Language / Ngôn ngữ:** [English](script-debug-injection.en.md) · [Tiếng Việt](script-debug-injection.vi.md) · [中文](script-debug-injection.md)

# Script injection debugging: use custom instructions to verify the effect of instructions

Updated: 2026-09-16. This page records the script injection debugging function of the native host: hand the event script you write to the original script engine for execution in the running game, and use polling tracking, status probes and sampling frames to check the actual effect of each instruction. It is a tool for steps 3 and 4 of [Remaining Instruction Semantic Confirmation](script-semantics-confirmation.md). It is not a script writeback, nor does it change ROM, directory data or original events.

## Host-side mechanism

- Switches `SRW64_SCRIPT_INJECT=1`; `src/host/script_inject.hpp` are called by `game_hooks.cpp` and `host.cpp`. `run_host_probe.py` only accepts this switch when the Japanese version profile, `--graphics`, silent, bounded VI and `SRW64_SCRIPT_TRACE=1` are turned on at the same time, and the report writes `script_inject_enabled`.
- Request file `script-inject.txt`: one line `SRWJ1 <sequence> <at_vi> <hex>`, hex is the event header 5 words (type + four parameters), instruction sequence and end `FFFF`. The VI thread reads at the same pace (every 6 VIs) as `control.txt`; the sequence number must be incremented, rejected and logged when the host is busy (queued or executing).
- The script writes to the top 64 KiB temporary storage area of RDRAM `807F0000`; the entire temporary storage area is required to be zero before application, and then cleared after completion.
- Idle determination (`idle_reason`): `engine+4 = 0xC0`, `+0x97C = 0x80` (no event operation), `+0x9AA = 0` (polling phase 0), `8010F5E8 = 1` (our phase; phase number 1 our team/2 enemy/3 third party, between levels: 0), `8010F6B0 = 0` (no defeat process), `8015DA02 ∈ {3, 0xB}` (tactical map). When it is not satisfied, it will be recorded as `deferred`. When it exceeds 1800 VI, it will be recorded as `idle-timeout` and give up.
- Start the image `8009EE98 → 8009EDB8`: `owner+0x1C` points to the 10th byte of the temporary storage area (skipping the event header), clear `+0x22..+0x2E`, `+0x30`, `+8/+9 = FF`, `engine+0x990 = 0`, `+0x97C = 0x2000`. After that there is the original `8009EFDC` polling every frame.
- Completed: PC is 0 and status is `0x80`, or `+0x97C` returns to `0x80`. At this time, the `+0x98E` registration number is restored and the temporary storage area is cleared, and `complete` is recorded; the PC leaves the temporary storage range and is recorded as `escaped`; the 3600 VI has no progress and is recorded as `stalled`.
- Event file `script-inject-events.jsonl` (schema `srw64.script-inject-event.v1`: `queued / deferred / rejected / applied / complete / escaped / stalled`, `applied` and `complete` with engine snapshot). The status probe stores a region snapshot at each of the two boundaries `script-inject-applied` and `script-inject-complete`.
- Unit test `tests/native_script_inject.cpp` (ASan, `make recomp-script-inject-test`, merged into `recomp-native-check`) covers parse rejection, idle determination, application, completion recovery, sequence number and busy rejection.

## Client `tools/recomp/script_lab/script_debug.py`

- `assemble`: JSON of input schema `srw64.debug-script.v1` (list of `{"op": "3D3B", "args": [0], "note": "…"}`, optional `event_type` and `header`). The parameter length is only taken from the layout lock `stage_scripts`. Unknown instructions, empty handler `3D76/3D77`, unreachable `3D78/3D79` and out-of-bounds parameters are all rejected, and a list of hex and offsets is output.
- `inject`: write `script-inject.txt`, save `script-inject-N.json`, wait for `complete / rejected / escaped`.
- `report`: Associate the polling line of `SRW64_SCRIPT_TRACE` to the instruction boundary according to the actual PC. A poll will first scan conditions and flags, and then execute at most one command: the PC stops after its opcode while the command is still executing, and the PC stops at the next boundary when it is completed; therefore, commands skipped by false condition blocks or other route segments will not be mistakenly recorded as executed and included in `commands_not_executed`. The start/end VI of each command takes the latest sample frame from `frame-trace.rgb` and saves it as PNG. The status probe area compares and decodes funds, variables, and roster coordinates by bytes.
- Fixed scripts in `config/recomp/debug-scripts/`: `fade`, `scroll`, `map`, `deploy`, `move`, `values`, `dialogue`.

## Running evidence: `build/recomp/script-debug/inject-2`

Chapter 1 (Scene Index 1 "Depu! スイームルグ", Marino route) Archive of our side's phase in the first round, mute, `--vis 12000`, frame sampling 160×120. Seven scripts are injected in sequence, all `complete`, no `escaped` or `stalled`; report `script-debug-report.json`, event `script-inject-events.jsonl`, host log `build/recomp/script-debug/inject-2.native.log`.

| Sequence | Script | Command | Result |
| --- | --- | --- | --- |
| 1 | fade | `3D3B` 0/1/2/3 each connected to `3D38` | Each of the four modes has 88 VI; the average sampling frame value is 54.6 → 0.6 (black opaque) → 54 (black transparent) → 252.5 (white opaque) → 57 (white transparent). `3D38` 45/30 counts respectively 90/60 VI: 2 VI per count. |
| 2 | scroll | `3D35` (5,5), `3D54`, `3D35` 0x4000/0x4103/0x4203 | `3D35` Same poll completed, picture moved on subsequent frames (absolute target 15006/19200 pixel change); 0x4000 back `3D54` The picture is restored after remembering the position; the top 3/right 3 only change by 85–100 pixels due to the viewpoint edge. |
| 3 | map | `3D34` 0,10,10,0 and 0,24,24,1 | Current map index `8010F5EE` 20 → 0, the random number table is rebuilt, and the whole picture is replaced with map 0; 64/42 VI. The first parameter is the map number, not the mode: `8020A874` Write it to `8010F5EE` and then reload the resource (evidence `script_map_switch_direct`). |
| 4 | deploy | `3D45` 3 | 292 VI post-roster 0/2 appears (12,21) Group 3 units, new body, driver (character 204) and weapon instance record, our unit appears in the center of the screen. |
| 5 | move | `3D3C` 28,(25,20); `3D46` 503,1 | 100 VI post-roster 0/0 changed from (19,5) to (25,20); `3D46` 36 VI post-roster 0/2 was removed, the aircraft instance record is retained: exit confirmation. |
| 6 | values Blocks, `3DD4`/`3DD1`/`3DD0` segments each contain `3D5B` | Funds 0 → 8000 = (5+1+2)×1000; variable 7 is written from 3 to 2; ACC = 9; variable 7=1 Blocks and sections are skipped (`commands_not_executed`). The +0x4C..+0x50 of the body 36 modification section are all 3, and the weapon instances are recalculated simultaneously; the +0x20 of the three pilots changes from 100 to 70, that is, the strength is −30. |
| 7 | dialogue | `3D3F`, `3D3E`, `3D48`, `3D38` | The injected text is displayed in the dialogue window, and the speaker is parsed as Malina according to the runtime route; the two dialogues are 740/2260 VI (including waiting to press A), `3D48` Done immediately. |

All experiments after Sequence 3 are conducted on map 0; this does not affect the roster and numerical conclusions, but the pixel statistics of the viewpoint type are subject to the current scene. The first run of `inject-1` was rejected because the idle determination regarded the stage number as starting from 0 (`not-player-side`). It has been corrected to start from 1 and the layout locks `engine` and `operand_roles` were written.

These results have been backfilled into the `runtime` field of each `config/data/original-jp-v1.json` instruction (shown as "Run Injection Observation" on the instruction page of the Catalog and Viewer): `3D34`, `3D3B`, `3D46`, `3D5F`, `3D6C` were upgraded to `code-confirmed`, `3D34` was renamed to "Switch map and scroll to location", `3D46` was renamed to "Unit exits", `3D5F` was confirmed as overall strength −30. Common instructions are now 33 items `code-confirmed`, 21 items `structure-confirmed`, 19 items `unknown`.

## Limitations

- Can only be injected during our phase, when the tactical map is idle, and when no events are running; dialogue commands need to be advanced through the `control_host.py` button.
- The observation range is limited to the fixed area of the status probe, 160×120 sampling frame and script polling; memory changes not covered by the probe will not appear in the report.
- Injection proves "the effect of this instruction in this context" and cannot replace the verification of the original script instance; writing back to ROM or editing the original event still requires independent byte round-trip and acceptance.

## Recurrence

```sh
SRW64_SCRIPT_INJECT=1 SRW64_SCRIPT_TRACE=1 SRW64_STATE_PROBE=1 SRW64_FRAME_TRACE_FROM=2400 SRW64_FRAME_TRACE_TO=9600 \
  .venv/bin/python tools/recomp/run/run_host_probe.py --graphics --profile config/recomp/profiles/play-profile.json --language ja \
  --images original --original-name-entry --resolution-scale 2 --input config/recomp/inputs/load-continue.json \
  --save-from build/recomp/gfx-probes/female-map-audio-3/first-map-turn1.sram \
  --save-sha256 b340a9c686b627d00dfaee9b4d89c896039547f8d607cb51b035d3f7bb2d756b \
  --output build/recomp/script-debug/inject-3 --vis 12000
```

```sh
.venv/bin/python tools/recomp/script_lab/script_debug.py inject build/recomp/script-debug/inject-3 --script config/recomp/debug-scripts/fade.json
```

```sh
.venv/bin/python tools/recomp/script_lab/script_debug.py report build/recomp/script-debug/inject-3
```

Use a new output directory for each run; `control_host.py --buttons` for dialogue scripts and `control_host.py --quit` for termination.