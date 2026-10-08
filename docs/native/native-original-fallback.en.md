> **Language / Ngôn ngữ:** [English](native-original-fallback.en.md) · [Tiếng Việt](native-original-fallback.vi.md) · [中文](native-original-fallback.md)

# Original mode HD resource fallback

Date: 2026-09-12. It belongs to the built-in rendering module of this project; there is no new external MOD interface.

## Current behavior

| Configuration and Resources | Startup Behavior |
| --- | --- |
| Original, complete HD pictures and name and avatar resources | Verify and prepare HD resources, F6 can switch pictures and 5600 models in configuration |
| Original, HD manifest, picture or name avatar files are missing | Use ROM image and eight original opening avatars; retain selected language, fonts and UI; HD switching disabled for this run, no water drop model prepared |
| HD, necessary HD files are missing | Startup error, need to complete the resources or explicitly switch to Original |
| The picture/avatar summary does not match, the list is illegal, the path is out of bounds | Error report, do not ignore the damage due to "lack of resources" |

The startup log states that the path is missing; the window title shows `Original | HD unavailable`, and neither F6 nor auto-validated HD requests enable unprepared content. Restarting after resource recovery can regain switching capabilities; currently, running resources installation/reloading is not supported.

This fallback is only for optional HD art files. Basic inputs such as the original ROM, language catalog, glyph maps, toolchains, etc. must still be valid. The water drop model will still be generated/verified according to the original process when full HD art is available and the configuration is enabled; damage to existing models does not fall within the scope of this rollback.

```sh
.venv/bin/python tools/recomp/run/play_native.py \
  --profile config/recomp/profiles/play-profile.json --language zh-Hans --images original --new-game
```

Original means original art; Chinese, native name pages and independent fonts can still be used, which does not mean restoring the entire N64 UI. The language is still selected at startup, and full-game multilingual coverage and on-the-fly language switching have not yet been completed.

## Implement boundaries

- `profile.py` only captures `FileNotFoundError` in HD preparation; Original records `hd_available: false` and the reason, and HD continues to report errors. Image output that has been compiled but is later found to be missing the avatar will not be loaded by the host.
- `name_assets.py` Verify HD avatars before writing out; ROM-only extraction does not read the HD avatar list. The eight original images still verify the ROM table and image shape.
- `run_host_probe.py` Prepare the model after the content availability is clear; do not pass the image package/model path when there is no HD, and explicitly pass the HD unavailable status.
- `ImageMode` clearly distinguishes three states: unconfigured, original only, and switchable. Window titles and run records reflect actual capabilities.

## Verify

`make check`: 115 Python tests passed, with 7 new ones covering missing packages, missing avatars, explicit HD failures, illegal manifest failures, language/font preservation, ROM-only avatar extraction, and corrupted avatars.

`make recomp-native-check`: 9 native component programs passed; the image mode use case confirms that only when Original is requested, neither HD nor toggle can change the mode. The passing of native components is not equivalent to the acceptance of the entire game.

Actual run with raw evidence placed in `build/recomp/original-fallback-check/`, using new configuration pointing to non-existent art manifest; no existing HD files moved or deleted, no player saves read or overwritten.

- `missing-zh`: Chinese Original cold start, VI 1270 opens the modern name page; records that HD is unavailable, original model, and no picture package; VI 2400 exits normally, and all 4 game threads are recycled. GPU frames still record Original after delivering HD request around VI 780. This round did not capture a screenshot of the Cocoa name page window, and the GPU screenshot does not include the page overlay.
- `intact-ja`: The first Japanese configuration switching observation, the model modes of Original→HD→Original are all correct, but U+0010 has appeared in the name field before the first snapshot; the source is not determined and cannot be accepted as the default name integrity. After restoring the default, the reshoot will exit when the VI upper limit is reached, and the failure record will be retained.
- `intact-ja-final`: Pass independent retest using the same binary. The Japanese name page is switched to Original→HD→Original three times, the avatar visual is switched and restored, and the name/surname/nickname remain `マナミ` / `ハミル` / `マナミ`; VI 1404 request to exit, host exit code 0, and all 4 game threads are recycled. See `build/recomp/original-fallback-check/verification.json` and current round `roundtrip-verification.json` for the final summary.

This round does not verify full-game HD coverage, all routes, save restores, or full game state/RNG equivalency; name page model status only certifies mode selection and does not replace visual acceptance of the world map model. For evidence of existing world map switching, see [Content Architecture](native-content-foundation.md).