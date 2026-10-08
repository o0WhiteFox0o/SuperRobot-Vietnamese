> **Language / Ngôn ngữ:** [English](script-runtime-observation.en.md) · [Tiếng Việt](script-runtime-observation.vi.md) · [中文](script-runtime-observation.md)

# Observe the first silent script run

Follow-up progress: [Male super type opening and 3D3C unit movement](script-3d3c-runtime.md). The scope of evidence from the first run is retained below.

2026-09-12. Actual running of the original Japanese recomp, selecting the female super-type default name from the new game, through the opening scene of the first episode to a playable tactical map. Exited via control protocol with host exit code 0 after running approximately 185.8 seconds and 11,100 VIs. The audio device output is turned off, and the audio tasks of the original game are still calculated normally. Using independent empty SRAM, no trial history is read or overwritten.

## This evidence

Running directory: `build/recomp/script-analysis/opening-1/`. ROM SHA-256 is `ee5f4a21d8e5f7827d21199e27800edf250df9a8e4d10befb1a6992df597b13e`.

| Check | Results |
| --- | --- |
| Actual events | Scene 1, opening events `0019C1B0` |
| Normal/dialogue commands | 123 times, all observed and completed |
| Dialogue | 58 instructions, exactly the same as the original sequence of this opening |
| Instruction types | 13 types |
| Parameter raw bytes | 123/123 match |
| Inconsistent parameters or PC advancement | 0 |
| Corrupted log/poll unavailable | 0 / 0 |
| Automatically skip the entire dialogue | Not used; only use the normal A key to advance the dialogue |

The startup input only skips the previous zoom prologue text, and the original name grid uses the default name; starting from the first line of dialogue, the entire event command is passed. Select Original pictures and models, Japanese language, and still use native dialogue typesetting, so this is not a pixel-by-pixel comparison of the original hardware.

Report: [`acceptance.json`](../../build/recomp/script-analysis/opening-1/acceptance.json), [`script-observation.json`](../../build/recomp/script-analysis/opening-1/script-observation.json), [`report.json`](../../build/recomp/script-analysis/opening-1/report.json).

## Conclusion obtained

### 3D32: Related to world map location presentation, table fields still need to be disassembled

This time the parameters are executed according to `4 → 0 → 1`, and the three entries are consistent with the ROM. Table `801C5310` has three signed halfwords per entry; parameter 0 corresponds to `(18, -257, -1010)`, parameter 1 corresponds to `(18, -144, -372)`, and parameter 4 corresponds to `(17, 721, -435)`.

`801C4BCC` Converts the last two halfwords into floating point values and passes them into the map positioning/drawing call; depending on the current state, it may be set directly, or it may go through fadeout and subsequent state machines. Therefore, a more accurate research direction is "selecting map presentation configuration and positioning". We cannot just call all table items the same kind of camera movement.

- Parameter 0: VI 3179–3293, takes 114 VI; subsequent screens show the inland location of the continent.
- Parameter 1: VI 5791–5845, takes 54 VI; the subsequent screen is the coast/island location.
- Parameter 4: Completed in the same poll. This cannot be used to conclude that it is ineffective.

Corresponding to the real host frame: [after parameter 0](../../build/recomp/script-analysis/opening-1/present-1680.png), [after parameter 1](../../build/recomp/script-analysis/opening-1/present-2940.png). This time, only the original parameters are observed, and no single parameter replacement is performed; the formal semantic configuration still retains the original confidence level.

### 3D4D: Observed conversion of world map to battlefield loading

This command is executed at VI 7803 and advances the PC; the next `3D65` does not begin until VI 8415, with the battlefield loading and the first episode title screen appearing in the middle. This shows that in this example, it triggered the outer process switch, and it cannot be used to infer that the entire screen switch will be completed immediately by "this item is completed immediately".

Evidence: [Episode 1 title frame](../../build/recomp/script-analysis/opening-1/present-4140.png). The outer state machine and other call contexts still need to be tracked and will not be upgraded to global semantic confirmation this time.

### 3D45: All three deployment groups are executed by the opening event

Groups 0, 1, and 2 are executed at VI 8423–8845, 8849–9141, and 9465–9777 respectively; enemy and friendly units appear on the actual screen, and friendly units can be selected later. Evidence: [Map after appearance](../../build/recomp/script-analysis/opening-1/present-4800.png), [Unit selection range](../../build/recomp/script-analysis/opening-1/present-5220.png).

The three calls are all located in the `0019C1B0` opening event, and the independent type 13 event `0019C3A0` is not executed this time. Therefore, the "Initial Configuration" category in the story viewer does not mean that additional executions must be performed in this order in the new game; the entry path to C2 remains to be confirmed.

### Still no evidence obtained

There are no `3D3C`, `3D36`, `3D55` in this paragraph, and they cannot be confirmed based on this trial. There are no completed battles, defeat triggers, level playthroughs, and no verified writebacks or mods. Next time, you can choose the male super series opening containing `3D3C`, reuse the recorder to analyze the original value, and then do an isolated single parameter comparison.

## Logger and Reproduction

`SRW64_SCRIPT_TRACE=1` Enables read-only polling boundary logging at the existing `8009EFDC` wrapper, off by default. Logs go into `RUN.native.log`, starting with `SRW64_SCRIPT_TRACE`. `tools/recomp/analysis/analyze_script_trace.py` uses the scene runtime entry, original instruction boundary, handler and parameter bytes to make a unique match and output the actual normal/dialogue instructions passed.

The logger does not intercept every internal condition function; a poll may scan multiple conditions and then execute a normal command. The analyzer will not declare anything passed by the scan as actually executed. The instruction takes time to use the host VI and is not directly treated as the original script waiting for parameters.

```sh
SRW64_SCRIPT_TRACE=1 .venv/bin/python -B tools/recomp/run/run_host_probe.py \
  --graphics --profile config/recomp/profiles/play-profile.json --language ja \
  --images original --original-name-entry --resolution-scale 2 \
  --input build/recomp/script-analysis/opening-input.json \
  --output build/recomp/script-analysis/opening-next --vis 14500
.venv/bin/python -B tools/recomp/analysis/analyze_script_trace.py \
  build/recomp/script-analysis/opening-next
```

If `--audio` is not passed, the device output will be turned off. The run directory must not exist, the keystroke script and its summary have been saved in this evidence.

**Record version boundary:** This complete run uses `script-poll.v1`, PC, handler, status, and parameters are normal, but the auxiliary round only captures the high byte, the stage captures the original 32-bit value, and the camp number captures the adjacent raw halfword. These auxiliary fields are not used for this acceptance. Finally, `v2` corrected the field width and locked the complete log line. It has passed ASan/UBSan's endianness, field width, boundary and no-write tests and host compilation; this complete game log still retains v1 and does not pretend to be v2 running evidence.

The exit code only indicates the normal end of this time and does not replace the existing thread exit life cycle issue acceptance.