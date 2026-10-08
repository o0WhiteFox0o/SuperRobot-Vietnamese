> **Language / Ngôn ngữ:** [English](native-intro.en.md) · [Tiếng Việt](native-intro.vi.md) · [中文](native-intro.md)

# Opening zoom text: skip and resource directory

2026-09-10. The native RT64 host supports **R + START** to skip the entire opening zoom text, and the current keymap is **E + Enter**. The public prologue and the route prologue after selecting the protagonist use the same control entrance. Ordinary confirmation still advances page by page according to the original game; the skip key combination is blocked until released after scene switching to avoid misoperation of the protagonist selection or the first line of dialogue.

New game experience:

```sh
python3 tools/recomp/run/play_native.py --profile config/recomp/profiles/play-profile.json --new-game
```

First use Enter to pass the logo, title and select New Game; enter the zoom text on the starry sky background and press E + Enter. The two prologues need to be clicked once respectively. This feature is enabled by default in the graphics host, regardless of whether the native dialogue UI is enabled.

## Original resources

Run `.venv/bin/python tools/content/extract_intro.py`, output to `build/recomp/intro/assets/`:

- `index.html`: Browse in the order of playback, supporting original size/2 times, transparent shading, and single page opening.
- `group-0.png` to `group-4.png`: Overview of five groups.
- `pages/`: A complete text page reorganized according to the original model, 30 transparent PNGs.
- `textures/`: Original texture atlas, retaining original size and original color palette.
- `decoded/`, `manifest.json`: Decompressed resources, ROM identities, resource offsets, SHA-256, page order and per-block splice coordinates.

| Group | Number of play pages | Resources |
|---|---:|---|
| Public Prologue | 11 | 5506–5516 |
| Route 1 | 6 | 5517, 5524, 5525, 5533, 5526, 5527 |
| Route 2 (the actual machine in this round is the female super series) | 6 | 5517, 5528, 5529, 5534, 5530, 5531 |
| Route 3 | 5 | 5517, 5518, 5519, 5520, 5535 |
| Route 4 | 5 | 5517, 5521, 5522, 5532, 5523 |

33 impressions, 30 individual textures in total. 5517 is the chronology page shared by the four routes; 5536 is the shared RGBA16 palette, and 5537–5543 are the seven text page geometries.

The original texture is mostly 304 pixels wide and the page is 256 pixels wide. They are atlases and cannot be directly treated as complete text pages: for example, model 5537 stores the first 32×32 text in the source image `(256,0)`, which is actually placed in the upper left corner of the entire page. The extractor reorganizes the page into 16-byte sprite descriptors and checks the four vertices used by the scaling animation, pixel coverage and overlap. Actual page main width 256 pixels, some 224 pixels wide; height 32–192 pixels. The gallery displays the reorganized pages, while the unreorganized gallery remains.

This time only the original Japanese assets are extracted, no text is replaced or redrawn. Subsequent Chinese culture can organize these pages into text and re-layout them using the native text engine, while retaining the time and order of the original zoom animation.

## Implementation and verification

`native_intro.cpp` In the `801CA9CC` package entry of ROM overlay `0x10DA50` (RAM `0x801C4500`, length `0x7C50`) observe the main state 13. Legal group number and page number, sub-state 0/1. If a request is received during the initial fade-in, wait for the text object to be created before finishing. Call the original object release `8008B888` and the end of the original paragraph `801CA5B4`, set the page number to the end point and the sub-state to 2; music stop, fade out and next mode selection continue to be executed by the original game. overlay overlay cancels pending requests while loading and keeps consumed keystrokes until physically released.

- `make check`: 53 Python checks, compileall, and dependency checks passed.
- `tests/native_intro.cpp`: Key combination edge, initial fade-in wait, single trigger, cross-scene continuous shielding, key release recovery, ordinary confirmation transparent transmission; ASan/UBSan passed.
- `tests/native_intro_adapter.cpp`: Real memory adapter, with 8 MiB RDRAM and original function stub to verify end status, object slot, call context retention, overlay isolation; ASan/UBSan passed.
- `build/recomp/intro/common-3/`: native RT64/Metal, 1,200 VI, exit 0. The public prologue static page VI 600 is skipped, VI 634 loads the protagonist selection; the key combination continues until VI 900, and the GPU readback still stops at the protagonist selection. The input is `config/recomp/inputs/intro-skip-common.json`.
- `build/recomp/intro/female-1/`: native RT64/Metal + Apple dialogue, 4,800 VI, exit 0. VI 500 requests to skip, VI 518 ends in the text scaling phase; select the female super type normally and complete the default name. Route 2 skips at VI 3100, VI 3134 enters the world map, VI 3290 appears with Lawrence text 17410; the key combination continues until VI 3400, and the first sentence remains manual until VI 4800. The input is `config/recomp/inputs/intro-skip-female.json`.

`report.json` of each running directory saves input and code hashes, `intro-events.jsonl` saves events, and `present-*.png` is the readback after GPU completion. Asset catalog 1/2x with transparent shading viewed in native browser.

`common-1` is a failed run before the guest address sign extension is repaired and is not used as evidence of success. The key combination of `common-2` starts from the New Game menu and is not designed to skip the prologue entered later. The current actual operation covers the public prologue and female super series routes; the other three routes share the adaptation code and have not yet been run separately for acceptance. The test sent keys through the host N64 input path, but the physical controller was not connected.

Component checks can be run with `make recomp-intro-test`.