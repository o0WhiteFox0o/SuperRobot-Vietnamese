> **Language / Ngôn ngữ:** [English](shared-game-ui.en.md) · [Tiếng Việt](shared-game-ui.vi.md) · [中文](shared-game-ui.md)

# SDL/RmlUi game interface

2026-09-20. The in-game interface switches to SDL2 events, RmlUi layout and FreeType fonts by default.
Fixed version of RecompFrontend RT64/Plume renderer. Protagonist selection, name input, confirmation, Link Battler,
Settings and tooltips are drawn within the game's GPU surface. The default host no longer compiles the corresponding AppKit page.

"Settings..." or Ctrl/Cmd+ in the top application menu of macOS, open the sharing settings, Esc or "Return" to close;
The game screen does not have permanent option buttons. The system menu is only responsible for opening the entrance, and the settings page is still shared SDL/RmlUi. rules, presets, languages,
Original/HD still calls the original interface. F7 uniformly enters the SDL event path, and the word grouping period is handed over to the input method.
The game adapter continues to be responsible for name encoding, duplicate checking, writeback, linkage status, and script advancement.

## Code and thread boundaries

- `src/native/ui/frontend.cpp`: SDL events, RmlUi context, shared settings/linkage/notifications and debug UI.
- `name_page.*`, `text_input.*`: Name page and group word bridges shared with standalone prototypes.
- `presentation_settings.cpp`: Original language request/completion/key release logic, save and use public `app::atomic_write`.
- `window_test_control.cpp`: Window size and closed SDL QA backend.
- `src/host/macos/app_menu.mm`: A single setting entrance of the system application menu, the language title switches with the game;
Click Submit Open Request Only to hand over the sharing settings page in the window thread.
- `src/host/graphics.cpp`: Connect RT64 render hook, draw the UI after blocking the name corresponding to the workload,
The GPU completion callback unlocks resources; the screenshot contains the UI in the same GPU submission, and AppKit screenshot overlay is no longer done.

All RmlUi calls are protected by the same mutex. The window thread is responsible for events, layout and semantic actions, and the rendering thread only records
Drawing commands. The next layout/release texture waits for the completion of the previous submission; fixed RT64 present queue itself waits for fence frame by frame,
Satisfies the non-double-buffering constraints of the upstream renderer. SDL text start, stop, and candidate box positioning are deferred to window thread execution.
Destroy RmlUi and renderer before destroying the GPU; maintain the thread recycling order of the original host.

UI reads only `names::Request`, `link_page::Request`, immutable language directory and settings snapshot, does not read RDRAM.
Name masking continues to be searched by RT64 workload, and the late-arriving old workload will not re-expose the original grid due to window thread switching.
The avatar is registered with an internal resource name to avoid RmlUi URL normalization changing the absolute file path; Original/HD still uses local assets.
Key release gating after closing a modal page counts towards SDL actual state and debug virtual keys.

## Builds and fonts

`make host` / `run_host_probe.py --graphics` automatically prepares the fixed ones in `config/recomp/frontend.json`
RecompFrontend with RmlUi; does not overwrite dirty upstream or bad versions. Source code preparation and compilation require development tools, games
Python is still not required for running and local ROM import. The standalone name page prototype is retained as `make recomp-ui-probe`.

Shared UI and dialogue use the same set of packaged fonts: the launcher points `SRW64_FONT_DIR` to `tools/content/prepare_fonts.py`
Prepared directory (HarmonyOS Sans SC and Condensed, plus the symbol font `content/fonts/SRW64Symbols.ttf` and button icon font `SRW64Prompts.ttf` in the warehouse),
Explicitly report an error when files are missing. The application package carries these fonts and licenses in `Contents/Resources/fonts/`, and the "About" page of the settings window indicates the source of the fonts.
`SRW64_UI_FONT` is available in the development environment to specify a single font; only look for the local machine when `SRW64_FONT_DIR` is not available (unit tests, old probes)
Arial Unicode, Microsoft Yahei or Noto Sans CJK. See [Chinese, Japanese and English cross-platform text and game dialogue](portable-text.md).

## Debugging and Regression

`ui.tree` Returns the `id`, text, available, focus, and window point coordinates of the RmlUi element.
`text` of `ui.click` supports visible text or stable IDs such as `route1`, `field0`, `next`,
`rule:esp-level`, `locale:en`, `images:hd`, `link:0`. After the setting window is paging, pressing the id and clicking the setting control on another page will turn to that page first;
The tab itself is `settings-page:general` etc. (see [Settings Window](settings-window.md) §7).
Clicks are hit tested by RmlUi and game functions are not called directly. `ui.key` uses the SDL key name,
`ui.type` uses `SDL_TEXTINPUT` / `SDL_TEXTEDITING_EXT`; no longer relies on macOS key_code.
Screenshots use the default game window, and the setting is no longer a separate OS window. `menu` returns the setup header and `native_menu` ready status;
macOS actually executes the system menu item when called by the setting title, and the rule title remains compatible with forwarding.
The old AppKit name/rule control file script is not an acceptance port of the shared UI.

Execute in a **new quarantine session** (will start a new game and change the name, do not run on the player session):

```sh
SRW64_DEBUG=1 .venv/bin/python tools/recomp/run/run_host_probe.py \
  --graphics --interactive \
  --profile config/recomp/profiles/play-profile.json --language zh-Hans \
  --images original --output build/recomp/shared-game-test
# 在另一终端运行：
.venv/bin/python tools/recomp/verify/verify_shared_ui.py --run build/recomp/shared-game-test
```

Check coverage: real opening and casting, rejection of unsupported characters, Return/F7 isolation during word composition, text submission,
Language switching preserves editing, rules settings, 800×600 and 1100×760 scaling, partner/confirmation, game name writeback, and story activation.
The verification report and GPU screenshots are kept in the local run directory and are not stored in the library.

## Local evidence (2026-09-20, shared UI commit a8a2de)

- `build/recomp/sdl-game-07/shared-ui-verification.json`: real opening, casting, word combination, language, setting,
Small window, name writing back, partner confirmation and story start; press and hold W to close settings, press and hold Return to confirm the release gate of the story,
The route prologue was successfully skipped, and the game buttons were restored after confirming that the page was closed.
- `build/recomp/sdl-game-03/shared-small.png` etc. GPU readbacks undergo manual image inspection; 800×600 vs.
The 1100×760 input box, avatar, and buttons are all within the scope of the interface.
- `build/recomp/sdl-link-01/shared-link-verification.json`: Read the existing SRAM and enter the linkage page.
Select F91 and Zambot; the original game adapter records `selection=5`, `kind=linked`.
`status.link_page.scheduled` is a snapshot when the page is opened. It is not used to infer the game state after submission.
- Run through `window close`/`quit`, exit code 0, log `created=4 joined=4 remaining=0`.
Extra `sdl-shutdown-01` opens OS thread trace: observed as 0 after release, but logged as before release
`UNOBSERVED`, so the reported `shutdown_lifecycle_verified=false`; does not exit normally
or join counts as full OS boundary gate passes.
- `build/recomp/ui-probe-sdl-final`: Standalone 66-step name page script passed.
- `make check`: 245 of 256 tests passed, 11 skipped, plus compileall and dependency checks.

The above is the real game and GPU evidence submitted on macOS for this shared UI, and is not the game acceptance for subsequent dialogue backend split;
The group word is SDL event injection and the OS candidate window is not verified. The prompt bar has been connected to the shared rendering, but this round did not trigger a plot refund to accept the prompt bar separately.

## Dialogue text and composition

The default dialogue has been accessed [Chinese, Japanese and English cross-platform text](portable-text.md), CoreText/CoreGraphics will no longer be entered
Game dialogue objectives. `src/host/dialogue_scene.cpp` is responsible for the main text, person's name, reading indicator, bottom column and review,
`src/host/dialogue_layout_adapter.hpp` lets Reader and Draw share the same immutable layout.
`src/host/dialogue_plume.cpp` uses [universal Plume synthesizer](plume-pixel-compositor.md),
Preserves dialogue snapshots of matching workloads and resource references before GPU completion.

The local CPU verification entry is `tests/dialogue_cpu/`, there is no remote CI; see the text document for commands, dependencies and font configuration.
The pixel-by-pixel comparison of the previous CoreText split was historical verification. The new backend uses Chinese, Japanese and English behavior, cropping and actual game screen acceptance.
Anti-aliasing to emulate legacy system fonts is not required.

## Unfinished cross-platform work

HD layers, screenshot readback and name page occlusion are implemented in the non-Metal backend Plume, and the Linux/Steam Deck version can be built and run.
([Three-platform port](../design/three-platform-port.md)); The desktop first-time ROM selector is still only implemented in macOS,
Windows has not been built yet.
The real Chinese and Japanese OS input method candidate window, controller navigation, redistributable fonts and the first episode/archive cold start of the three platforms still need independent acceptance.