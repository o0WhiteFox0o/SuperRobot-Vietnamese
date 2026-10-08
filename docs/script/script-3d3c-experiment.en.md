> **Language / Ngôn ngữ:** [English](script-3d3c-experiment.en.md) · [Tiếng Việt](script-3d3c-experiment.vi.md) · [中文](script-3d3c-experiment.md)

# 3D3C single parameter control experiment

2026-09-12. Following [Five Original Parameter Observations](script-3d3c-runtime.md), use fixed native binary, same keys and independent empty SRAM to compare the first episode of the male super series. Turn off the audio device output during runtime and use Japanese, Original pictures and model display.

## Acceptance results

**This absolute coordinate example passed: the target moved up one space, and the logical coordinates of the elf end point and unit roster were changed at the same time. **Both groups completed the opening 56 normal/dialogue commands, 18 dialogues, and exit code 0.

| Check | Original value group `move-baseline-2` | Changed value group `move-target17-1` |
| --- | --- | --- |
| Target Parameters | `1912` | Temporary `1911`, restored upon completion `1912` |
| Logical position before move | `(25,28)` | `(25,28)` |
| Logical position after completion | `(25,18)` | `(25,17)` |
| Sprite position after completion | `(432,320)` | `(432,304)` |
| Target Instructions VI | 6994–7054 | 6995–7059 |
| Time consuming | 60 VI | 64 VI |
| Brad's position at the end of the opening scene | `(25,18)` | `(25,17)` |
| Kaz's position at the end of the opening scene | `(23,19)` | `(23,19)` |
| Original parameter verification | All 56 items matched | 55 items matched, and the other 1 item only had a predetermined parameter difference |

Both sets of binary SHA-256 are `a8d361fb8683453ee8c1bc58d8f9d195d488766c026674fdd8791e168f7d12b4`, and the host source code, ROM, input and display configuration are consistent. At the two boundaries of movement completion and opening end, the recorded fields of all valid units only show the difference of Brad's y minus 1 and Elf's y minus 16. Starting point `(25,28)` in the roster has been vacated; revalued group `(25,18)` has no remaining units, `(25,17)` is only occupied by Brad. The entire 256-byte script in the final RDRAM snapshot is also consistent with the original ROM.

The picture will move as Brad's position changes. The following is not a fixed lens pixel-by-pixel difference; you can observe the relative distance between Brad and Kaz. The source frame's VI and file name are saved in JSON with the same name.

![Actual game screen with original value and target moved up one space](../../build/recomp/script-analysis/move-position-comparison.png)

Final evidence: [All 25 control checks passed](../../build/recomp/script-analysis/move-comparison-2.json), [Original value host report](../../build/recomp/script-analysis/move-baseline-2/report.json), [Changed value host report](../../build/recomp/script-analysis/move-target17-1/report.json). The two sets of `script-observation.json` retain complete instruction correspondence, and an original value mismatch in the modified value group is explicitly retained.

For the first time, the original value group `move-baseline-1` and the modified value group have the same source code and the status comparison is in line with expectations. However, the launcher regenerates the RSP and links it, and the binary digest is different, so [the first round of strict comparison failed](../../build/recomp/script-analysis/move-comparison-1.json). Then add `--reuse-build-from` with fingerprint verification, and reuse the original file of the modified value group to run `move-baseline-2`; the final acceptance uses the run-back result. Old reports are not overwritten.

## The meaning and boundaries of level Mod

`3D3C` of normal absolute coordinates can change the actual level unit position. The original value group also shows: the elf reaches the end point first, and the logical coordinates still retain the starting point; they are not written back until the end call is completed. Therefore subsequent events that depend on the location should wait for this command to complete.

Relative positions, out-of-bounds or inaccessible targets, multiple units with the same driver number, target non-existence, complete combat and save reloading are not accepted this round. The formal confidence level continues to be `structure-confirmed`, but there is operational evidence for absolute coordinate shifting, closing writeback, and this single parameter experiment.

## Experimental design and isolation

The only intervention is the second parameter of event `0019BF10 + 00C8`: `1912 → 1911`, that is, the target of driver 27 ブラッド is changed from `(25,18)` to `(25,17)`. The original ROM file remains unchanged.

`script_move_probe.hpp` is turned off by default, `SRW64_SCRIPT_MOVE_PROBE=baseline` is only recorded, and `target17` is temporarily overwritten. The fixed experiment will check scene 0, route `3DD3`, stage `C1`, PC to be executed `8019B4C8`, 256-byte event fingerprint and original instructions/parameters, and write `8019B4CC` only if all match. Executed only once, `1912` will be restored after the command is completed; if it is found that the parameters have been overwritten by other codes, the conflict will be recorded without overwriting. Launcher requires raw JP, mute, empty SRAM, script logging enabled.

Both runs use the same [input file](../../config/recomp/inputs/script-move-probe-input.json). `SRW64_SCRIPT_TRACE` in the log retains the actual parameters, so the change group must produce an explicit mismatch of the original value; the independent comparator only accepts the prespecified `1912 → 1911` and does not hide the difference.

## Recorded status

Each target command poll records all valid units in 30 slots for each of the three factions: faction, slot, unit pointer, driver number, status byte, logical x/y, sprite index, and sprite x/y. Also record the boundaries before moving, after overwriting, command completion, after recovery, and completion of the last sentence of the opening.

Logical coordinates are written back from `load_000AB160:801CBEB8`: `801E510C` finds the camp/slot from the sprite index and writes `(精灵位置−32)>>4` to `8015E100 + 阵营×0x258 + 槽×0x14 + 4/+5`. The new `script_actor_movement_commit` evidence window locks this raw machine code; the test checks the two coordinate write instructions independently.

The "occupancy" here is based on valid roster coordinate enumeration and does not mean that the game collision query, terrain passability, blocking rules or independent occupation cache have been verified.

## Reproduction command

```sh
# 先运行改值组，保留构建指纹。
SRW64_SCRIPT_TRACE=1 SRW64_SCRIPT_MOVE_PROBE=target17 \
SRW64_FRAME_TRACE_FROM=6800 SRW64_FRAME_TRACE_TO=8100 \
.venv/bin/python -B tools/recomp/run/run_host_probe.py \
  --graphics --profile config/recomp/profiles/play-profile.json --language ja \
  --images original --original-name-entry --resolution-scale 2 \
  --input config/recomp/inputs/script-move-probe-input.json \
  --output build/recomp/script-analysis/move-target17-next --vis 9000

# 原值组复用同一文件，拒绝二进制、源码、ROM、生成报告或 ABI 指纹变化。
SRW64_SCRIPT_TRACE=1 SRW64_SCRIPT_MOVE_PROBE=baseline \
SRW64_FRAME_TRACE_FROM=6800 SRW64_FRAME_TRACE_TO=8100 \
.venv/bin/python -B tools/recomp/run/run_host_probe.py \
  --graphics --profile config/recomp/profiles/play-profile.json --language ja \
  --images original --original-name-entry --resolution-scale 2 \
  --input config/recomp/inputs/script-move-probe-input.json \
  --reuse-build-from build/recomp/script-analysis/move-target17-next \
  --output build/recomp/script-analysis/move-baseline-next --vis 9000

.venv/bin/python -B tools/recomp/analysis/analyze_move_probe.py \
  build/recomp/script-analysis/move-baseline-next \
  build/recomp/script-analysis/move-target17-next \
  --output build/recomp/script-analysis/move-comparison-next.json
```

After the opening, you can exit early through `control_host.py RUN --quit`; this experiment does not require completing the battle. The final acceptance of the two groups is based on the target command and the opening boundary, and does not require that the wall clock times of start and exit are exactly the same.

## Code and verification

- [Fixed Experiment Probe](../../src/host/script_move_probe.hpp): Default shutdown, identity verification, single overwrite, final recovery and status snapshot.
- [Comparator](../../tools/recomp/analysis/analyze_move_probe.py): Accepts exactly one predetermined parameter difference while checking source/binary, instruction sequence, recovery and roster changes.
- [Component Test](../../tests/native_script_move_probe.cpp): Verification under ASan/UBSan defaults to no writing, identity incompatibility rejection, only one byte change, recovery, single execution and conflict will not be overwritten.
- `PYTHONDONTWRITEBYTECODE=1 make check`: 97 items passed, compilation and dependency checks passed; directory reconstructed to 83 evidence items, all references resolvable.
- Launcher negative example: the experiment of turning on the sound was rejected; the reuse request of the forged binary digest was rejected. The comparator also rejects two original value records as a value change experiment.