> **Language / Ngôn ngữ:** [English](script-3d3c-runtime.en.md) · [Tiếng Việt](script-3d3c-runtime.vi.md) · [中文](script-3d3c-runtime.md)

# 3D3C: Silent running observation of the male super series opening

For subsequent progress, please see [Single Parameter Control Experiment](script-3d3c-experiment.md). This paper retains the evidence boundaries of the original parameter observations.

2026-09-12. The original Japanese version of the recomp actually runs about 154.9 seconds, entering the first episode from the default name of the male super type, and arriving at the operational tactical map after the complete opening. Exited via control protocol at VI 9252 with exit code 0, leaving no gametest process. The audio device output is turned off, and the audio task is still calculated; independent empty SRAM, Original pictures/models, Japanese and native dialogue layout are used. No ROM or script parameters have been modified this time.

## Running evidence

Directory: `build/recomp/script-analysis/male-opening-2/`. ROM SHA-256: `ee5f4a21d8e5f7827d21199e27800edf250df9a8e4d10befb1a6992df597b13e`.

| Check | Results |
| --- | --- |
| Scene/Route | 0／`3DD3`, male super type |
| Actual events | `base:stage_events:0019bf10` |
| Normal/dialogue commands | 56 times, all completed; the order is consistent with the entire opening event |
| Dialogue commands/Command types | 18／17 |
| Original parameter bytes | 56/56 match |
| Inconsistent PC or Parameters/Unmatched Polls/Bad Logs | 0/0/0 |
| Logger version | `srw64.script-poll.v2`, 103 poll boundary records |
| Audio output | `false` |

Complete report: [Acceptance](../../build/recomp/script-analysis/male-opening-2/acceptance.json), [Command Correspondence](../../build/recomp/script-analysis/male-opening-2/script-observation.json), [Host Report](../../build/recomp/script-analysis/male-opening-2/report.json). Final screen: [Unit selection for tactical map](../../build/recomp/script-analysis/male-opening-2/present-4615.png). The key press only skips the opening zoom text, and the event dialogue is advanced with the normal A key.

## Modification of parameter meaning

`3D3C` was originally labeled "Map position effect (type, position)", now changed to **"Unit moves to position (driver, position)"**, `unknown → structure-confirmed`. The first parameter is associated with the driver profile.

Machine code link:

1. Close the window with resident `800A0360`, use `800A38DC` to decode the second parameter, and then call `8020A030(x, y, 第一参数)` of the battlefield overlay.
2. `8020A030` traverses the three camps of `8015E100`, each camp has 30 slots, the slot step size is `0x14`, and the camp step size is `0x258`. The valid slot's `+0xC` points to the unit, the unit's `+0x38` points to the driver, and the number of the driver's `+2` is compared. Take the first occurrence in traversal order. So the first parameter is the driver number.
3. The target grid coordinates are converted to `格坐标 × 16 + 32`. The status table `8021E230` points to lateral movement `8020A4BC`, vertical movement `8020A5F0`, closing `8020A724` and empty processing in turn. Horizontal and vertical movement uses signed 8-unit steps; it cannot be directly converted to the original game "frames per frame" because it needs to distinguish between VI, polling and draw frequency.
4. `8020A788` updates the lens with the sprite position and returns to completion in status 3. The resident handler advances the parameter PC by 4 bytes.

Evidence window `script_actor_movement` locks the raw ROM bytes of `load_000AB160:8020A030..8020A874` with SHA-256; the instruction evidence link in the directory has associated this window. Regression testing independently checks the ROM's Unit→Driver→Number load instructions and checks character references and position decoding for five real script instances.

## Five original parameter calls

The offset is relative to the beginning of the event; the grid coordinates are the script's original values, not screen pixels.

| Event offset | Driver number | Target position | VI start and end | Time-consuming VI |
| --- | --- | --- | --- | --- |
| `006C` | 298 | `1508` → (21, 8) | 5668–5700 | 32 |
| `00BE` | 27 ブラッド | `191C` → (25, 28) | 6932–6958 | 26 |
| `00C8` | 27 ブラッド | `1912` → (25, 18) | 6994–7054 | 60 |
| `00DE` | 31 カーツ | `171C` → (23, 28) | 7560–7586 | 26 |
| `00E8` | 31 カーツ | `1713` → (23, 19) | 7622–7678 | 56 |

GPU consecutive frames do appear to correspond to unit movement and camera tracking. The following contact table takes frames from `frame-trace.rgb` in the order recorded in `frame-trace.jsonl`, each frame is 160×120 RGB; titled Real VI. They are used for alignment behavior and do not replace memory acceptance of logical unit coordinates.

![Brad’s second move](../../build/recomp/script-analysis/male-opening-2/move-2-27.png)

![Kaz’s second move](../../build/recomp/script-analysis/male-opening-2/move-4-31.png)

Other examples: [298](../../build/recomp/script-analysis/male-opening-2/move-0-298.png), [Brad's first paragraph](../../build/recomp/script-analysis/male-opening-2/move-1-27.png), [Katz's first paragraph](../../build/recomp/script-analysis/male-opening-2/move-3-31.png).

The same section is also executed twice, namely VI 3946-3964 and 4142-4160, each waiting for 18 VIs; this only confirms the execution and time-consuming, but does not confirm the complete performance semantics of the parameter, and the confidence level remains unknown.

## Not yet accepted and compared with the next time

This time, I did not complete the battle, defeat the trigger, or clear the level, nor did I observe the internal conditional instructions. The movement of ordinary absolute coordinates is mutually supported by code and screen; the following still needs to be confirmed: relative position and correction branch, driver number shared by multiple valid units, target not found, out-of-bounds position, logical coordinates and occupation status after the movement is completed, and archive writeback.

The next minimal comparison can be fixed: only change the second parameter of event `0019BF10 + 00C8` to `1912 → 1911`, that is, Brad's second paragraph target is changed from (25,18) to (25,17), retaining driver 27 and all other bytes. The original ROM address of the parameter is `0019BFDC`; the runtime parameter address of this scenario is `8019B4CC`. The loading identity must be rechecked before it can be overwritten. The runtime address cannot be used in other scenarios.

Expect only the end point and duration of this move to change. The comparison needs to record the sprite position, logical unit coordinates, occupation status and subsequent Kaz movement at the same time, and clearly register the changed bytes as experiments, and the original value consistency check cannot be silently released. This time only the experimental design was determined and no parameter replacement was performed.

## Recurrence

```sh
SRW64_SCRIPT_TRACE=1 SRW64_FRAME_TRACE_FROM=3600 SRW64_FRAME_TRACE_TO=12000 \
.venv/bin/python -B tools/recomp/run/run_host_probe.py \
  --graphics --profile config/recomp/profiles/play-profile.json --language ja \
  --images original --original-name-entry --resolution-scale 2 \
  --input build/recomp/script-analysis/male-opening-input.json \
  --output build/recomp/script-analysis/male-opening-next --vis 14500
.venv/bin/python -B tools/recomp/analysis/analyze_script_trace.py \
  build/recomp/script-analysis/male-opening-next
```

Do not pass `--audio`. The input file summary is in the host report; the output directory must not exist. After arriving at the tactical map, use `control_host.py RUN --quit` to end, to avoid subsequent A key selection of units. The first attempt at `male-opening-1` was rejected before launching the game because `--vis 13000` was smaller than the input event range; this report only uses the subsequently successful `male-opening-2` without mixing the logs twice.

Verification: `PYTHONDONTWRITEBYTECODE=1 make check`, 97 tests passed, compilation check and dependency check passed; the original directory was regenerated, 82 evidence items, and all references were parsable.