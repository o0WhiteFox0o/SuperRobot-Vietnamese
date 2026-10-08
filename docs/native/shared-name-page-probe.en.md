> **Language / Ngôn ngữ:** [English](shared-name-page-probe.en.md) · [Tiếng Việt](shared-name-page-probe.vi.md) · [中文](shared-name-page-probe.md)

# RecompFrontend Shared name page prototype

2026-09-20. Continuation of P2/P3 of [Cross-Platform Release Plan](../design/cross-platform-release-plan.md).

This is a standalone window experiment: reusing RecompFrontend's RT64/Plume renderer with its fixed version
RmlUi, displays the protagonist selection and confirmation page (no more name input starting from 2026-09-27, see [Default name trilingual display](default-names.md)). The official game now uses the same shared page by default, see [Game Integration](shared-game-ui.md).
Requests in the prototype are served by the synthetic adapter and do not execute the original game, write to SRAM, or prove
Windows/Linux games are playable.

## Dependencies and code boundaries

- `config/recomp/frontend.json` Fixed RecompFrontend commit with RmlUi.
- `tools/recomp/toolchain/prepare_frontend.py --fetch` download to ignored dependency directory; reject
Wrong version or dirty upstream, existing checkout is not automatically updated. No network access by default.
- The prototype uses the full rendering implementation of upstream's `RmlRenderInterface_RT64`. The preparation tool only converts the header file's
The launcher umbrella include is changed to the minimum dependency of RmlUi/Plume; the generated copy and summary remain local.
Does not interface with the full launcher, MOD menus, configurations, recompinput, or upstream's macOS global swizzle.
- `src/native/ui/name_page.*` uses existing `names::Request` and semantic callbacks with serial.
The page only handles display and input, and does not touch the game memory; the verification, writeback and status advancement on the real game side are still performed by
`src/host/native_name_entry.cpp` is responsible. Standalone executables still use the synthetic adapter to which the official host has been connected.
- `src/native/ui/text_input.*` Supplement fixed version SDL backend missing group word event (temporary text,
Submit, cancel, focus recovery, confirmation key isolation), now only the fund input box in the game host is used, and the name page and probe are no longer used.
- `src/native/ui/probe_surface_macos.cpp` separately hosts Metal window and GPU screenshot readback.
The page and group code do not reference Cocoa, CoreText, or Metal; the current probe construction entry is still limited to macOS.

## Build and interact

First press [Development Guide](../guide/native-development.md) to prepare the native graphics tool chain, and then execute:

```sh
make recomp-ui-probe
./build/recomp/gfx-build/ui-probe/srw64-ui-probe \
  --catalog-dir content/locales \
  --font '/absolute/path/to/local-cjk-font.ttf' \
  --output build/recomp/ui-manual-01
```

Fonts must be provided explicitly locally; loaded into FreeType and uniformly registered as `srw64-ui`, no language directory is used
macOS PostScript names in , system fonts are not copied or submitted. The example requires a font covering Chinese, Japanese and English.
The selection and authorization of fonts for distribution still need to be implemented separately.

Four cards are synthetic data. Use the left and right keys to select, Enter/Z to enter the confirmation page; Enter to start the confirmation page, Esc to return to casting;
F7 switches between Japanese/Chinese/English. The final confirmation of the synthesis process only records `starts`, returns `backs`, and does not start the game.
The name is displayed as requested: changing to the reading language is a matter of the game host front-end, not the probe.

Optional `--dialogue /absolute/path/to/prepared/dialogue.json` to use local prepared content
The first eight portraits. The avatar is only an example of visual material and does not mean that the character is bound to the synthesized name.
This is a private ROM derivative and is not distributed with the prototype code.

## Rerunable semantic control

```sh
./build/recomp/gfx-build/ui-probe/srw64-ui-probe \
  --catalog-dir content/locales \
  --font '/absolute/path/to/local-cjk-font.ttf' \
  --output build/recomp/ui-script-01 \
  --script config/recomp/ui-probe/name-entry.json
```

The output directory must not exist. The script uses `srw64.ui-probe-script.v1` and supports `click` (control ID),
`key`, `language`, `resize`, `capture`, `expect` and `quit`. SDL/RmlUi used for button interaction
Processing path; `click` directly calls the semantic action of the page, not the mouse hit test. Returns non-zero on assertion failure. Each step status is written to `events.jsonl`;
The screenshot is read back after the GPU fence completes, along with the frame status JSON. `result.json` indicates the scope of the synthesis process.

Script verification: selection, casting page Esc invalid, confirmation, three-language switching, zoom, confirmation page returns to casting, substitution confirmation, start.
2026-09-27 It has not been re-run after rewriting.

### Local verification record (2026-09-20, name editing page period)

macOS arm64 completed using existing fixed RT64/Plume, AppleClang, FreeType and native CJK fonts
Compilation and actual Metal window execution. 66-step script, 17 status assertions passed, 7 GPU readback screenshots
Checked the Chinese and English selection page, name page in group words, Japanese error message, English name page, partner page and confirmation page.
Also checked are Chinese word group submission, Japanese backspace and retaining input focus after language switching.

The local recording directory is `build/recomp/ui-probe-check-07`, `verification.json` recording scripts, source code,
Binary and screenshot summary; synthesized name with local avatar for visual verification,
Not original game character binding or evidence of game running. `make check` passed 256 tests (11 skipped),
Recorded in `build/recomp/ui-make-check.log`. Fonts, avatars, screenshots and dependent products are not included in the database.
In addition, the official `srw64-gfx-host` has been recompiled to confirm that the optional prototype does not block the original host build; it is not built with this
Run acceptance instead of real game.

## Acceptance after prototype

1. ~~Verify Chinese/Japanese candidates under the real OS input method~~: The name page no longer inputs text.
2. Real name request, workload occlusion and window/rendering thread serialization have been connected to the default host, see the game integration documentation.
3. By default, the host reuses the input release gate; subsequent platforms will continue to verify that the close button does not penetrate.
4. Migrate controller navigation/recompinput, and add Windows/Linux surface and build verification.
5. The shared page has passed the real opening and naming; the first episode and archive cold start of the three platforms are still subject to subsequent acceptance.