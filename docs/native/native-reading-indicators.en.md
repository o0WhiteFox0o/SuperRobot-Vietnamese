> **Language / Ngôn ngữ:** [English](native-reading-indicators.en.md) · [Tiếng Việt](native-reading-indicators.vi.md) · [中文](native-reading-indicators.md)

# Automatically read gears, advance progress and double-frame focus

Date: 2026-09-11. Referring to the screenshots of "Mech Z" provided by users, the automatic gear and advancement progress are added to the native dual dialog boxes.

## In-game performance

- The bottom bar displays "Auto 3/4" and a four-segment scale, and the number of lights is consistent with the current gear. The automatic upper limit is 4, the manual mode displays "Manual" and the scale goes out.
- The current conversation dialog box is only distinguished by slightly brighter names: the names in the two boxes are both blue, and the brightness of the other box is 80%; the text of the other box is still dimmed. It turns out that there is a circle of cyan corners at the four corners of the frame and a triangle mark on the left side of the name. On 2026-09-26, these were removed according to user requirements (`verify_reading_indicators.py` no longer checks the triangle).
- The thin bar at the top of the current box indicates the progress until the next automatic advancement: it is cyan when the text is displayed, orange during the waiting period after the text is displayed, and advances after it is filled. The long text enters the next reading page first, and then the last page is handed back to the original game to enter the next segment. Page numbers such as "1/2" will no longer be displayed starting from 2026-09-23: the continuation page is the same as the original page turning. Press A to continue displaying.
- Pause the reading timer when replaying, and continue after returning; the automatic countdown bar will not be displayed when manual, fast forwarding or skipping.
- The names in the review will alternate between blue/orange when changing people, and consecutive clips of the same person will remain the same color. Color is determined when the lookback record is written, scrolling or retiring older records will not change the color of existing names; the text remains white.
- During a handover, if both boxes are temporarily inactive, the mark remains on the box that has just been read and is still visible, and switches after the next one starts. Marks are not retained after the dialog box is closed or the script is invalidated.

The operations follow the existing keys: ↑↓ to adjust gears, Japanese and Chinese continue to use their respective external UI entries; the new interface text is not hardcoded in the Chinese branch.

## Actual screenshot

The following are actual screenshots of the initial eight-level version. Based on subsequent feedback, it has been reduced to four gears; the original speeds of gears 1–4 are retained, and the same gear constants are used for numbers, scales, and key upper limits.

Talk in the upper frame:

![Automatic reading on the upper frame](../../build/recomp/reading-indicators/zh-full/present-3600.png)

Speak below:

![Automatic reading in the lower box](../../build/recomp/reading-indicators/zh-full/present-3660.png)

Japanese text, original image, No. 18 text and pagination: [actual screenshot](../../build/recomp/reading-indicators/ja-full/present-3780.png). Chinese, HD, No. 18 text and pagination: [actual screenshots](../../build/recomp/reading-indicators/zh-full/present-5220.png). They are all readbacks after the GPU is completed, not schematic diagrams.

## Status and Timing

`dialogue_model.hpp` and `page_timing()` are used for actual automatic confirmation and progress display at the same time. The original word display speed and waiting time formulas are used to avoid creating another animation timer that is out of touch with the plot advancement. The progress is calculated based on the ticks that have been processed by the reader, sandwiched between 0-1000; replaying will pause this timeline, reset the new reading page, and keep the grid full while waiting for the game to receive confirmation.

The game thread adds reading events, progress and interface status to immutable `Frame`. Rendering still uses snapshots corresponding to the RT64 workload. `focused_box()` gives priority to selecting the only active frame; when there is no active frame, only the frame in the frame that matches the last reading event and is still visible can be selected. Speakers or words are not borrowed from other workloads.

The progress bar uses the top space of the original dialog box without reducing the name width or text layout area. The bottom bar continues to be displayed according to the visibility of the entire dialogue interface, retaining the previous [Autoplay bottom bar flickering repair](native-dialogue-flicker.md).

## Verify

Both sets are actual RT64/Metal implementations of the original Japanese ROM, each running 11800 VI, with sound turned off:

| Check | Chinese / HD, No. 13 → No. 18 | Japanese / Original image, No. 18 |
| --- | ---: | ---: |
| Consecutive GPU completion frames | 2206 | 2300 |
| Bottom column pixel check | 2135 | 2300 |
| Current speaker triangle marker pixel check | 1955 | 2120 |
| Push bar fill pixel check | 1756 | 1919 |
| Review pause frame | 180 | 180 |
| Handover frame without active frame | 107 | 10 |
| Check failed | 0 | 0 |

The above two sets of first editions have gone through all the gears 0-8 at that time, two upper and lower speech boxes, display/wait, manual recovery, review, and long text paging. Events, pages read, and progress values ​​remain unchanged during replay. In the Chinese group, there are another 71 frames where the dialogue is turned off and the bottom bar is hidden normally; among the dialogue frames that are still visible, the bottom bar does not disappear unexpectedly. After the fourth-level adjustment, the host construction and existing reading component inspection will be completed separately; the first version running evidence will remain intact.

`verify_reading_indicators.py` reads the lit ticks, name triangle, and progress bar length from consecutive GPU pixels and compares them to the status of this workload frame by frame. Occluded triangles and progress bars are not checked when reviewing the overlay dialog; the bottom bar is still checked. The endpoint allows for anti-aliasing error for a low-resolution sampled pixel.

60 Python tests, compilation, and dependency checks passed for `make check`; passed for `make recomp-content-test`. New components return to cover the actual automatic deadline, progress monotony and full grid, review freeze, manual/fast forward hiding, paging clear, handover focus, double active box ambiguity and close box.

Review:

```sh
.venv/bin/python tools/recomp/verify/verify_reading_indicators.py build/recomp/reading-indicators/zh-full
.venv/bin/python tools/recomp/verify/verify_reading_indicators.py build/recomp/reading-indicators/ja-full
.venv/bin/python tools/recomp/analysis/analyze_toolbar_trace.py build/recomp/reading-indicators/zh-full \
  --require-matching-dialogue --output build/recomp/reading-indicators/zh-full/toolbar-boundaries.json
```

See [acceptance.json](../../build/recomp/reading-indicators/acceptance.json) for source files, inputs, and evidence hashes. The scope of this actual machine is the opening world map dialogue, covering the two image/language configurations listed; full diagnostic recording is used, and its frame time is not used as performance data for normal play.