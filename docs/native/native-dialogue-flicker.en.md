> **Language / Ngôn ngữ:** [English](native-dialogue-flicker.en.md) · [Tiếng Việt](native-dialogue-flicker.vi.md) · [中文](native-dialogue-flicker.md)

# Fix the intermittent flickering of plot dialogue

Date: 2026-09-11. Users reported that plot dialogue would flicker intermittently in HD mode. The sound will be turned off for all subsequent returns this time.

## Actual findings

Continuous GPU readback finds two types of problems that cannot be adequately covered by a single screenshot or by sampling every 60 frames:

1. **Occasionally mix in old dialogue frames. ** After stopping at `base:t00_17412` segment 1 and switching the image mode, the original Japanese glyphs and original dialogue layout suddenly appeared in some frames, and the native Chinese interface was restored in the next frame. Maps and avatars are still in HD. In the continuous recording before restoration, 24 unexpected picture jumps were found, corresponding to the entry/exit of 12 short-lived old dialogue frames.
2. **Normal trial play carries periodic re-recording. ** The old host encoded PNGs in the GPU completion callback every 60 render frames, exporting 8 MiB of memory every 120 graphics tasks. In HD still scenes, the interval after screenshots averages 4.87 VI and maximum 5 VI (approximately 81–83 ms); other frames average approximately 2 VI (33 ms).

Example before repair: [Old dialogue flashes into frame](../../build/recomp/flicker-check/switch-before-1/present-4023.png), [Restores Chinese in next frame](../../build/recomp/flicker-check/switch-before-1/present-4024.png). What was captured this time was the alternating dialogue layout, and the entire black frame was not captured.

## Modify

### Keep another dialogue snapshot of the display list

The original game can prepare two display list buffers A and B in advance. Originally, if `take_frame()` removed A and then executed `drawings.clear()`, the prepared snapshot of B would be deleted together. When rendering B, it returns to the original glyph path to form a flash frame.

Now use `src/native/presentation/display_list_snapshots.hpp` to manage the bounded snapshot queue, and only delete records matching the current task; it will be cleared entirely when the scene fails. The queue is synchronized by the existing dialogue mutex, and the rendering side continues to search according to the actual workload, without guessing a frame of text from the latest game state to cover up the problem.

C++ regression coverage: publish A and B first, then consume A, B must still be readable; each snapshot can only be consumed once; mismatched tasks do not consume other snapshots; switching scenarios invalidates pending snapshots.

### Normal trial uses lightweight diagnostics

2026-10-01: The complete diagnosis has been deleted entirely, the host only has the lightweight behavior mentioned above, and the `--diagnostics` parameter has also been removed. The following is a record of that time.

`--interactive` for `run_host_probe.py` defaults to `--diagnostics light`, so all existing trial launchers will benefit. The lightweight mode turns off periodic GPU screenshots, 8 MiB memory export, and frame-by-frame dialogue JSON writing, while retaining native dialogue drawing, image switching, and game saving.

The bounded probe still defaults to `--diagnostics full`, maintaining the existing screenshot/playback acceptance process; it can also be selected explicitly. Report recording diagnostic mode, no screenshots will be falsely reported as a rendering failure when running lightweight operations.

## Continuous frame review

You can use `SRW64_FRAME_TRACE_FROM` and `SRW64_FRAME_TRACE_TO` to specify VI scope. Each completed GPU frame within the range records 160×120 RGB samples, workload, image mode and adjacent frame changes; significant changes are then saved as a full PNG. This diagnostic is turned off by default and does not enter the normal player path.

```sh
# 静音：不传 --audio。
SRW64_BACKGROUND=1 SRW64_WINDOW_CONTROL=1 \
SRW64_FRAME_TRACE_FROM=7000 SRW64_FRAME_TRACE_TO=10800 \
.venv/bin/python tools/recomp/run/run_host_probe.py --graphics \
  --diagnostics light --profile config/recomp/profiles/play-profile.json \
  --input assets/hd-ai/dialogue-polish/dialogue-only.json \
  --output build/recomp/flicker-check/new-run --vis 11000

.venv/bin/python tools/recomp/analysis/analyze_frame_trace.py \
  build/recomp/flicker-check/new-run --from-vi 7100 --require-stable
```

The analysis only applies to the above-mentioned still dialogue: the water droplet is allowed to rotate, and the frame in which the picture is actively cut is excluded. It cannot be used to recognize normal plot transitions as flickering.

The evidence directory `build/recomp/flicker-check/` retains the complete diagnostic and light diagnostic runs before repair, only turning off re-recording, and after snapshot repair. The results are shown in the acceptance record below.

## This acceptance

The following is the actual RT64/Metal game run with the original Japanese ROM, native Chinese dialogue, and native water drop model, and is not a fixed display list playback. Both sets of final runs turned off audio output, each running 11,000 VI; and actively switched original/HD four times during static dialogue.

| Running | Continuous completion of frames | Unexpected screen jump | Result |
| --- | ---: | ---: | --- |
| Before restoration, full diagnosis, switching images | 2144 | 24 | 12 old dialogue flash-in frames and their restoration |
| After fix, full diagnostics | 1823 | 0 | Old dialogue is no longer mixed in under heavier recording loads |
| After repair, lightweight diagnosis | 1846 | 0 | Normal player configuration and image cut check passed |

The final light run after the last switch back to HD and stabilization (VI 9500 onwards), 649 intervals of 650 consecutive frames were all 2 VI, about 33 ms. Full diagnostics still retain recording costs and cannot treat its frame times as normal gaming performance. Resource updates at the moment of cutting the picture, diagnostic tracking and actively saving screenshots of changes are not included in the stable scene performance conclusion.

In addition, a silent run started with `--interactive` without passing `--diagnostics` confirms that `light` is selected by default, exits normally, and has no periodic PNG or 8 MiB memory files. `make check` passes 60 Python tests, compilation checks, and dependency checks; `make recomp-content-test` passes snapshot queue regression and Core Text/Reading Control checks.

Summary, source files and evidence hashes are available in [acceptance.json](../../build/recomp/flicker-check/acceptance.json). This proves that the recurring dialogue flickering and periodic recording pauses have been fixed; the acceptance scope is the dialogue and image switching in the first level, which does not mean that the entire plot or all types of black screens/flickers have been covered.

## The bottom status bar disappears during automatic playback

Follow-up feedback on the same day is located in the "Auto 3/Font Size 13/Operation Tips" column at the bottom. The previous static dialogue check does not cover the handover status of automatic substitutions.

Actual reproduction found that: when the original game confirms a sentence and switches speakers, both dialogue boxes can be temporarily inactive, but still displayed on the screen. The native bottom bar is drawn within `if (box.active)` of `native_dialogue_text.cpp`, so it will disappear with the active speaker's temporary gap and appear with the next sentence. This is a different trigger condition from the previous frame loss in the snapshot queue.

The bottom bar is now shared by two frames, which are drawn once per frame; as long as the native dialogue box matching the current GPU workload is still visible, the reading mode, font size, and operation prompts are displayed. Active dialogue still determines text brightness and page numbering. When the dialog box is completely closed, the bottom bar is also closed, and there is no delayed frame filling or text from other workloads. (2026-10-06 The bottom bar will be automatically hidden by default: the dialogue will fade out after 5 seconds, and the direction keys will be displayed for another 3 seconds. See [Dialogue Interface · Operation](native-dialogue-ui.md#操作). The following frame-by-frame comparison was done before that; to review now, you need to set the "Dialogue Operation Prompt" in "Options → Interface" to always display, or only compare the `controls_bar` block `fade` is greater than 0).

Using the same input script, the same original ROM and HD configuration, perform a silent real-time run at automatic speed 3, running 11400 VIs before and after:

| Inspection | Before Repair | After Repair |
| --- | ---: | ---: |
| Same dialogue, VI 7200–8580 | 669 completed frames | 685 completed frames |
| Bottom bar disappears unexpectedly | 8 times, one frame each | 0 times |
| Extended Checks, VI 7200–11200 | — | 1959 completion frames |
| Frames with dialogue and no active speaker | — | 109 frames, all bottom bars retained |
| Frames in which the dialog box has been closed | — | 73 frames, the bottom bar is hidden |

The difference in the number of completed frames before and after is due to the fact that older versions of flickering would trigger additional diagnostic PNG saves. The extended check compares the bottom bar in actual GPU pixels to the dialog visible state for that workload on a frame-by-frame basis, and there are no inconsistencies. The detection also checks the dark bottom panel and prompt text of the bottom bar to avoid mistaking the entire black transition scene for the bottom bar.

See [present-3628.png](../../build/recomp/auto-toolbar-check/before/present-3628.png) for the disappearing frame before repair; see [handoff-3627-sample.png](../../build/recomp/auto-toolbar-check/after/handoff-3627-sample.png) for the GPU sample when the same VI and both parties are temporarily inactive after repair. The latter are 160×120 samples read back continuously, not native resolution screenshots.

Review command:

```sh
.venv/bin/python tools/recomp/analysis/analyze_toolbar_trace.py \
  build/recomp/auto-toolbar-check/after --to-vi 8580 --require-visible
.venv/bin/python tools/recomp/analysis/analyze_toolbar_trace.py \
  build/recomp/auto-toolbar-check/after --require-matching-dialogue \
  --output build/recomp/auto-toolbar-check/after/toolbar-boundaries.json
```

This time 60 Python tests for `make check` and `make recomp-content-test` passed. See [Bottom Bar Fix Acceptance](../../build/recomp/auto-toolbar-check/acceptance.json) for run configuration, input and evidence hashes.