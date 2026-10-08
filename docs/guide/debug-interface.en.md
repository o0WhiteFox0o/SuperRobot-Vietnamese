> **Language / Ngôn ngữ:** [English](debug-interface.en.md) · [Tiếng Việt](debug-interface.vi.md) · [中文](debug-interface.md)

> **Language / Language:** [中文](debug-interface.md) · [Tiếng Việt](debug-interface.vi.md) · [English](debug-interface.en.md)

# Debug interface and MCP

Date: 2026-09-20. A real-machine debugging entrance shared by developers and Claude: starting an isolated debugging session, pressing keys, taking screenshots, reading status, operating the native interface, and exiting are all completed through the same interface. There is no need to rely on manual keystrokes or separate control files.

## Structure

| Layer | Location | Function |
| --- | --- | --- |
| Host debugging service | `src/host/debug_server.cpp`, `debug_transport.cpp`, switch `SRW64_DEBUG=1` | Monitor local loopback TCP (`127.0.0.1`, port assigned by the system), one JSON-RPC 2.0 request/response per line; the port and token are written in `debug.json` of the running directory (see "Connection method" below). Normal trial play is not enabled. Operations requiring SDL/RmlUi are queued to the window thread for execution. |
| Game keyboard layer | `src/host/debug_protocol.hpp`, `graphics.cpp` | The virtual keys follow the same reading path as the real keys: bound to the scan code of the same name, the pressing edge of F6/F7/F8/Esc passes through the same name page and language switching gate control; the release check after the name page is closed is also counted in the virtual keys. Virtual keys do not require window focus and the game can be driven in the background. |
| Native interface layer | `src/host/debug_ui.hpp`, `src/native/ui/frontend.cpp` | Shared SDL/RmlUi page provides interface tree, stable ID/text/coordinate click, input text and keys; settings and notifications are all within the game surface. |
| Sessions and Clients | `tools/recomp/debug/session.py` | Start session (via `run_host_probe.py --graphics --interactive`, output to `build/recomp/debug/<时间戳>/`, do not touch archives and preferences of `profile-play`), connect client (`Client(运行目录)`), wait conditions, event log incremental reading. |
| Command line | `tools/recomp/debug/srw64ctl.py` | The same set of operations for human use. |
| MCP server | `tools/recomp/debug/mcp_server.py`, warehouse root `.mcp.json` | stdio MCP implemented by the standard library (the project environment does not have the `mcp` package), Claude Code can call the `srw64_*` tool after approving the project MCP and reopening the session. |

## Coverage

The goal is that every input received by the game can be sent through the interface, and try to follow the same code path as the player:

| Inputs received by the game | Sources of players | Interfaces |
| --- | --- | --- |
| 18 game keys (14 N64 keys corresponding to the WASD joystick) | SDL keyboard status | `keys`: Merge the old keyboard table (`input::classic_keys`: Z=A,
| F6 screen, F8 mini-level, Esc exit | SDL key event | `keys`: The virtual pressing edge passes through the same name page and language switching gate as the real key |
| F7 language | SDL keyboard events, handed over to the input method during word grouping | `keys f7`: Enter the same SDL word group/repeat gate control |
| N64 handle (bypass keyboard layer) | None (for diagnostics) | `buttons` |
| Protagonist selection page: four cards, ←→, Enter／Z | SDL mouse and keyboard | `ui.click --text <主角全名>` (highlight and press Continue or Enter), `ui.key right`/`return`; `status.name_page` gives `route` and four options |
| Inter-scene main menu: nine items (two items after the "(previous)" scene), のりかえ secondary menu | SDL mouse and keyboard | `ui.click --text intermission:N` (or visible text) Confirm the Nth item, `intermission-swap:0|1` Select driver/goblin; `ui.key up`/`down`/`return`/`escape`; `status.intermission_page` gives `cursor`, `submenu`, `swap_refused`, number of rounds and funds |
| Modification screen: body list, five modifications, confirmation window and message | SDL mouse and keyboard | `ui.click --text upgrade:N` (current line confirmation, other lines movement), `upgrade-confirm`/`upgrade-cancel`/`upgrade-dismiss`; `ui.key up`/_ _INL_CODE_44__／`left`／`right`／`return`／`escape`；`status.upgrade_page` Given `screen`, `rows`, `window`, `funds`; direct modification of funds: `ui.click --text upgrade-funds` (main menu `intermission-funds`), `ui.type <数字>`, `ui.key return` |
| Linkage page: three work cards, ←→, space/Z, Enter, Esc/X | SDL mouse and keyboard | `ui.click --text <作品名>` (check each switch), `ui.click --text <继续按钮>`, `ui.key right`/`space`/`return`; `status.link_page` is given `joined` and `scheduled` |
| Casting and confirmation pages: cards, buttons, ←→/Enter/Esc | SDL mouse and keyboard | `ui.click`, `ui.key`; `status.name_page` gives four routes to `person` (3 castings, 2 confirmations) and casting pages |
| Pre-battle confirmation page: Probability of both sides, response, animation, start/return; keys are the same as the game (Z/Enter, X/Esc, direction keys/WASD, Q, E, K) and controller | SDL/RmlUi | `ui.click --id battle-confirm`, `battle-weapon`, `battle-counter`, `battle-evade`, `battle-defend`, `battle-spirits`, `battle-animation`, `battle-back`; `status.battle_page` is a snapshot released by the game thread |
| Load the level file during runtime | When the debugging interface is open, drag the file to the window in the title menu | `mini_stage.load {"path": <镜像或关卡源文件>}`; enter directly without specifying the level at startup, see [Mini Level](../script/mini-stage.md) |
| Main menu mini-level entrance | RmlUi button/F8 | `ui.click --id mini-enter`, or `keys f8` after starting with mini stage; wait for `status.mini_stage.ready`. Automatically complete default character initialization, unchanged for normal new games |
| In-game "options" and rule settings | RmlUi control, Ctrl/Cmd+, | `ui.click`, `ui.key`; `menu` retains compatible forwarding of localized rule titles |
| Interfield Enhanced パーツ page: Unit list, slot/inventory, holder | RmlUi page | `ui.click --id parts:N`/`parts-slot:N`, or `keys`'s arrow keys, Z/X; `status.parts_page`, waiting condition `parts_page`, event log `parts` |
| Interfield ユニットabilities/パイロットabilities page | RmlUi page | `ui.click --id ability:N`, or `keys`'s direction keys, Z/X, Q/E; `status.ability_page`, wait condition `ability_page`, event log `ability` |
| Field のりかえ page: pilot/goblin list, target list, confirmation | RmlUi page | `ui.click --id swap:N`／`swap-yes`／`swap-no`, or `keys`; `status.swap_page`, wait condition `swap_page`, event log `swap` |
| Interfield データセーブ page: media selection, archive bar, overwrite confirmation, Pak prompt | RmlUi page | `ui.click --id save:N`／`save-yes`／`save-no`, or `keys`; `status.save_page`, wait conditions `save_page`, event log `save` |
| Shared settings: rules, defaults, language, screen, screen ratio, interface size, pre-battle confirmation interface, inter-scene screen, protagonist selection, title menu screen (divided into five pages, click by id to turn to the page first) | RmlUi page | `ui.click`/`ui.tree`/Default `screenshot`; or use `settings` Direct setting (`rules`/`images`/`aspect` (`auto`/`4:3`)/__INL _CODE_120__／`battle_ui`／`ui_size`／`intermission_ui`／`name_entry_ui`／`title_ui`） |
| Game window: size, foreground, close button | Window management | `window` (`width`/`height`, `front`, `close`) |
| Normal exit | Esc, close window, ⌘Q | `quit`, or `keys escape`, `window close` |

`tests/test_debug_coverage.py` statically checks the premise of this table. Missing interfaces when adding keys or methods will cause the test to fail: each SDL scan code read by the host has a virtual key with the same name; F6/F8/Esc has a virtual press edge, and F7 has a corresponding virtual key; the button table of `buttons` is consistent with the input compiler (`native_inputs.BUTTONS`); MCP The key name of the tool description is consistent with the host; there is an MCP tool for each host method.

## Host method

| Method | Parameters | Description |
| --- | --- | --- |
| `status` | `history` | VI, running directory, window focus and size, language, screen mode, rules, opening state (`title_major` 3 is the main menu, `step` is the current page), dialogue reader (page, font size, speed, automatic, review, skip, each dialogue box text), name page request, linkage page (`link_page`), main menu between scenes (`intermission_page`), transformation screen (__INL_CODE _143__), pre-war confirmation page (`battle_page`), mini-level status (`mini_stage.available/entering/active/ready`), recent native prompt bar (`notices`, refund if you leave the team), native window and focus, virtual key pressed |
| `keys` | `press`+`hold_ms` / `down` / `up` / `release_all` | Game keyboard; key name `z x space return up down left right q e i k j l w a s d escape f6 f7 f8 f5` (F5 reloads the line text), used in combination `+`, such as `e+return` |
| `pad` | `press`+`hold_ms` / `down` / `up` / `release_all` | Virtual controller, each frame is merged into the state of the real controller (controller prompts, pages, L2/R2 and other host keys are treated as real controllers); key names are as per Steam Deck: `a b x y menu view l1 r1 l2 r2 up down left right ls_up… rs_down…`, combined with `+`. Command line `srw64ctl.py pad r2 l2:600 wait:300` |
| `buttons` | `buttons`, `vis` | N64 controller layer keys (`a b z start up down left right l r c_up c_down c_left c_right`), effective immediately, without going through the keyboard layer |
| `screenshot` | `path`, `overlays`, `window`, `timeout_ms` | Grab the GPU readback of the next render, already including the shared UI. `window` Use the default game window; no longer provides a standalone settings window or AppKit compositing. |
| `ui.tree` | `window` | RmlUi element tree: tag, `id`, `frame` (window point coordinates), text, available, focus; pixel = point × `scale`. |
| `ui.click` | `text` or `id` or `x`/`y`, `button`, `count` | After stable ID or visible text matching, via RmlUi Mouse hit test clicks; use the same path for both front and back. |
| `ui.key` | `key`, `modifiers` | SDL key names: return, tab, escape, delete, arrow keys, a–z, 0–9, f1–f12; macOS `key_code` is no longer used. |
| `ui.type` | `text`, `marked`, `unmark`, `window` | Insert text into the focused input box, which is equivalent to typing; `marked: true` is reserved for input method grouping (underlined, not submitted), `unmark: true` Submit the group word; the response `marked` indicates whether to inject the group word this time |
| `menu` | `path` | Localized headers compatible with forwarding settings and rules; OS menus are no longer enumerated. |
| `settings` | `rules` (default name or ID list), `locale`, `images` | Directly change rules, language, screen |
| `window` | `width`/`height`, `front`, `close` | Resize the game window (640–2560 × 480–1600 click), bring to the foreground (only required when you want to verify real focus or real mouse events), press the close button (`SDL_WINDOWEVENT_CLOSE`); respond to window status |
| `wait_vi` | `vi`, `timeout_ms` | Wait until specified VI |
| `memory.read` | `address`, `size` (≤ 0x10000) | Read the object memory and return hexadecimal; do not pause the game, it is a debug view instead of a snapshot ([Short skip] (../native/script-skip.md) use it for status control) |
| `memory.write` | `address`, `hex` (integer bytes, ≤ 4096 bytes) | Write object memory (for probes, such as forced combat background; only in debugging sessions) |
| `record.start`, `record.stop` | `width` (default 960) | Recording: after starting, each rendering is read back, shortened to `width`, and appended to the original frame and time of `record-<VI>/` in the running directory. The game sound is written as it is sent to the output device. `audio.s16` (stereo s16le); returns the frame number and size when stopped, as well as `audio_frames`, `audio_rate` and `audio_start` (the number of seconds since the first piece of sound started recording). `Session.record(秒数)` (or `record_start`... `record_stop(path)`, you can operate the game in the middle) arrange the screen into a fixed 30-frame timeline (each moment displays the latest frame at that time, and the stuck place is the freeze frame), press `audio_start` to align and mix into the AAC audio track, and use ffmpeg to compile it into MP4 And delete the original file; MCP is `srw64_record`, `srw64_record_start`/`srw64_record_stop` (`path` can be given, the directory will be created if it does not exist). The debugging session is muted by default. If you want sound, you need `srw64_launch(audio=true)`; the game itself has no sound for about 27 seconds before booting (logo and opening). The actual measured title screen was recorded for 8 seconds with 240 frames and the longest interval was 40 ms. The recording itself was almost not slowed down |
| `quit` | — | Normal exit, reported as controlled exit |
| `methods` | — | List methods supported by the host |

All game pages now share a single SDL window; screenshots use the default window or `"game"`.

## Command line

```sh
.venv/bin/python tools/recomp/debug/srw64ctl.py launch --language zh-Hans   # 构建并启动，打印运行目录
.venv/bin/python tools/recomp/debug/srw64ctl.py wait --title-menu
.venv/bin/python tools/recomp/debug/srw64ctl.py keys return                  # 主菜单确认
.venv/bin/python tools/recomp/debug/srw64ctl.py keys e+return:200            # 跳过序章
.venv/bin/python tools/recomp/debug/srw64ctl.py click --text 继续            # 姓名页按钮
.venv/bin/python tools/recomp/debug/srw64ctl.py type ナナ --marked            # 输入法组字；type --unmark 提交
.venv/bin/python tools/recomp/debug/srw64ctl.py keys i i k e+z:1500          # 字号、快进
.venv/bin/python tools/recomp/debug/srw64ctl.py shot                         # 截图路径与元数据
.venv/bin/python tools/recomp/debug/srw64ctl.py window --size 1280 960
.venv/bin/python tools/recomp/debug/srw64ctl.py events dialogue --kind font
.venv/bin/python tools/recomp/debug/srw64ctl.py quit
```

Each item of `keys` is a key combination, and `:按住毫秒` can be added; `wait:500` is just a pause. Commands other than `launch` default to the most recently started session (`build/recomp/debug/current`), which can also be specified with `--run`. `--reuse-build` Skip rebuilding when source code remains unchanged.

Session life: The game started by `Session.launch` in the script will only live until the process that started it ends - the check is run, the assertion fails, and the timeout kills (including `kill -9`) will cause `run_host_probe.py` to send `quit` to shut down the game (SIGTERM when there is no socket), and the report will record `ended_with_owner`; If the script is gone during the build, the game will no longer be launched. The mechanism is a pipe (`SRW64_DEBUG_OWNER_FD`) where only the initiating process holds the write end. The session of `srw64ctl.py launch` should be reserved for subsequent commands and is not subject to this restriction. When used up, `quit` must be used; the session started by MCP exits with the MCP server. After the script ends, if you want to leave the window open for others to see, pass `Session.launch(detach=True)`.

##MCP Tools

`srw64_launch`, `srw64_attach`, `srw64_status`, `srw64_keys`, `srw64_buttons`, `srw64_screenshot` (directly return to the picture), `srw64_record` (record a video with sound MP4, return path), `srw64_record_start`/`srw64_record_stop`, `srw64_ui_tree`, `srw64_click`, `srw64_type`, `srw64_ui_key`, `srw64_menu`, `srw64_window`, __INL_CODE_272_ _, `srw64_mini_stage_load`, `srw64_memory`, `srw64_wait` (`vi`, `dialogue_active`, `intro_active`, `name_page`, `link_page`, `intermission_page`, __INL_ CODE_282__, `title_major`, `text`, `event`), `srw64_events` (log: `dialogue`, `intro`, `name`, `rules`, __INL_CODE _291__, `control`, `script`, `mini_stage`, `settings`, `refunds`, `link`, `intermission`, `unit_name`), `srw64_quit`. Tool errors are returned as `isError` and do not interrupt the server. The host no longer takes regular screenshots or exports memory (2026-10-01 deleted "Complete Diagnosis": screenshot a whole window every two seconds or so, export 8 MiB of memory, and the title flame will drop from 30 frames to 18); if you want a picture, use `srw64_screenshot`, if you want a process, use video.

## Connection method

Starting from 2026-10-06, the three desktop platforms (macOS, Linux, and Windows) will use native loopback TCP to replace the original Unix socket (`debug.sock`). The reason is that the Windows version of CPython does not have `socket.AF_UNIX`; incidentally, the upper limit on the length of the socket path is removed (macOS 104 bytes).

- The host listens to `127.0.0.1:0`, the port is assigned by the system; add `SO_EXCLUSIVEADDRUSE` on Windows.
- `debug.json` (`srw64.debug-endpoint.v2`) of the run directory writes `transport: "tcp"`, `host`, `port`, `token` (256 bit random number, hexadecimal) and `pid`. The file is first created and can only be read and written by the owner, and then the token is written. After writing and renaming, the client will not read half of it; it will be deleted when the game exits.
- The first line of each connection must be `{"jsonrpc":"2.0","id":0,"method":"auth","params":{"token":"…"}}`, tokens are compared in constant time. If it is wrong or missing, return an error and disconnect; cache up to 4 KiB before handshake.
- The token replaces the role of the original socket file 0600: any process on the local machine can connect to the loopback port, and only the player can read `debug.json`.
- Client `Client(运行目录)` reads `debug.json` first; if not, look for `debug.tcp` (Android: local port forwarded by adb, without token). `Session.launch` and `Session.attach` both use "whether these two files exist" to determine whether the session is running.
- Android unchanged: still abstract socket `@srw64-debug`, only adb forwarding can reach it. Changing to TCP and adding a token does not work: the release version of the APK cannot be debugged, and adb cannot read the token in the application's private directory.
- Incompatibility between old and new: The new version of the client cannot connect to games before 2026-10-06, and vice versa.

## Opening method: switch in options

Players do not need the command line: "Options → About → AI debugging interface (MCP)" (`debug_interface` of `presentation.json`, the default is off). The window thread compares the switch and listening status every frame (`debug::service_main`):

- Open: Listen immediately (each new port, new token), and post a prompt (`debug_interface_notice`); if the switch is saved, it will listen and prompt once every time it is started.
- Close: `transport::stop()` stops accepting connections, disconnects existing connections, deletes `debug.json`; queued window thread requests return with errors.
- `--debug` (`SRW64_DEBUG=1`) still monitors before the window is opened and does not post a prompt; the switch is displayed as "on" and cannot be clicked, and cannot be turned off during this run. Development sessions (`Session.launch`) all go this way.
- When the About page is open, the listening address and running directory are displayed (the home directory is written as `~`, if it is too long, only the end is displayed), "Copy running directory" copies the complete path. The status in the settings is passed to the page via `settings::set_debug_endpoint`.

When monitoring fails (for example, `debug.json` cannot be written), the log records `SRW64_DEBUG_FAILED` and will not try again until the switch changes again.

## attach without parameters

`Session.attach()` (MCP's `srw64_attach` without `run`) Press `running_games()` to find: `build/recomp/debug/current` (most recent `srw64ctl launch` or `attach.py`) plus all `sessions/*/run/debug.json` in the local player user directory (`player_data()`: macOS `~/Library/Application Support/SRW64Recomp`, Windows `%LOCALAPPDATA%\SRW64Recomp`, Linux `$XDG_DATA_HOME/srw64-recomp`), try connecting one by one from the latest to the oldest file time (3 Second timeout, `methods`), the first one that can respond is. The `debug.json` left by the crash cannot be connected and will be skipped naturally.

## Files on another machine

Screenshots, video frames and event logs are files written by the host on its own machine. The host has two methods that are limited to the current running directory: `file.read {path, offset, size}` (up to 4 MiB at a time, base64, returns the total file length and `eof`) and `file.remove {path}` (the running directory itself cannot be deleted). When `Session.local()` is false (there is `remote.json` or `debug.tcp` in the running directory, that is, Deck or mobile phone), `Session.local_file()` is retrieved in chunks with `file.read`, and `Session.record()` is used. `file.remove` clears the frame directory on the host side, `Session.events()` press `status.run` to get the remote log. Deck no longer requires scp, and Android can also take screenshots and videos.

## On Steam Deck (or other Linux machine)

The `--play` of the release package will clear all `SRW64_*` environment variables, and `SRW64_DEBUG=1` will not work there; to open the debugging interface, pass `--debug` to the game. `debug.json` is written in the running directory of this session (`~/.local/share/srw64-recomp/sessions/<id>/run/`). Without `--debug` it is exactly the same as before. On Windows, `--debug` (`Marchwind64.cmd --debug`) is also uploaded, and the running directory is in `%LOCALAPPDATA%\SRW64Recomp\sessions\<id>\run\`.

1. On the Deck: Write `%command% --debug` in the "Properties → Launch Options" of this shortcut in Steam, and then play with the usual controller. No need to quit when something goes wrong.
2. On Mac: `.venv/bin/python tools/release/linux/attach.py` (default ssh host `Deck`, `--host` can be changed). It reads the `debug.json` of the game that is running with the debugging interface enabled (the switch in the options or `--debug`) through ssh, picks a local free port and forwards it to the remote port using `ssh -L`, writes the local port and original token (permission 0600) in `build/recomp/debug/deck-<时间>/debug.json`, and sets it as the current session; then `srw64ctl.py`, `Session.attach()`, MCP's `srw64_attach` are all directly available.
3. When you do not want to change the Steam settings, `attach.py --start` will start the game through ssh with `--debug` (game mode is in Xwayland `:1`, desktop mode is `--display :0`). Adding `--data-dir ~/srw64-debug` uses a separate set of data directories: ROM and HD packages are soft links, archives and settings are copied, and debugging will not write the player's own archives. Game parameters are written after `--`.

`remote.json` in the running directory remembers the host, remote running directory and forwarding process. Screenshots, videos (`srw64_record`) and event logs (`srw64_events`, `event` conditions of `wait`) are files written by the host on the Deck, and `Session.local_file()` is retrieved to `remote-files/` via the same connection (`file.read`). `quit` will turn off the game and local forwarding, leaving reports on the Deck. The standard error of the game is `journalctl --user` (recorded under the name of the steam process) when Steam is started. When `--start`, the game is run as a temporary unit of user systemd `srw64-debug` (SteamOS is turned on `KillUserProcesses=True`, and the process left in the ssh login session will be cleared when ssh is disconnected). See the output. `journalctl --user -u srw64-debug`.

## Relationship to existing control files

`control.txt`, `script-inject.txt` and SDL window/language controls are retained. Old AppKit name/rule control file
Belonging to the legacy backend, the shared UI uses JSON-RPC and `tools/recomp/verify/verify_shared_ui.py` acceptance.
`control.txt` only injects handle status; `ui.*` is required for word grouping, page click and window focus.

## Historical measurement: old AppKit backend (`build/recomp/debug/20260918T090743.895227Z`)

The entire process from cold start is driven by the interface, without manual keys: Enter to return to the title and select "スタート" in the ring menu, E+Enter to skip the public prologue (VI 12826), Z to select the super male protagonist and confirm, use `click --text` on the modern name page and press "Continue: Partner", "Continue: Confirm" and "Start Story" in sequence (the application is in the background, the button has been `performClick:`), press E+Enter in the prologue of the male protagonist's route to skip VI 18154 (group 1); after entering the dialogue, I, I, K change the font size to 13→14→15→14 (all three times take effect), and when pressing E+Z, 14 VIs push 3 paragraphs in succession; the screenshot is superimposed with the name page overlay; open the settings window through the menu "Options → Settings..." and take a screenshot, use `click --text` Check and cancel "Boss fake: times halved", the rules and event logs will change simultaneously; `quit` exit code 0, the socket will be cleared.

Another session on the same day (on startup `--reuse-build`): `window --size 1280 960` followed by `status` and screenshot both reported 1280×960; on name page `type なな --marked` returned `composing: true`, the screenshot shows "なな" with input method highlighting in the name column, `type --unmark` followed by `composing: false`; `quit` exit code 0. `window --close` Reuse window QA has verified the `performClose:` path, only compilation check has been done.

This also rechecks the name page fix on 2026-09-18: before the fix, the game keys pressed after the name page was closed were all swallowed, and the route prologue skip, font size, and fast forward were all invalid.

## Limitations

- Do not press Enter (START) after booting until the title screen appears: The original version detects that pressing START will enter the Controller Pak management screen when booting, in which the `osPfsIsPlug` called is currently intercepted by the generated code, and the host will abort. First `wait --vi 600` after startup.
- Screenshots depend on the game being rendered; it will time out when the window is minimized or the game is paused.
- The native interface layer only covers the program's own window; the system dialog box and input method candidate window are not within the scope (the group word itself is simulated with `marked` of `ui.type`).
- `status.ui.focus` is the focus element of RmlUi, and `active` separately indicates whether the SDL window has system keyboard focus.
- Menu items are matched by title, and the title changes with the interface language.
- The input of the real controller does not go through the interface; the interface has its own virtual controller (`pad`/`srw64_pad`), which is merged with the input of the real controller.
- Interface implemented on Windows (loopback TCP). 2026-10-06 Connected to AWS (Windows Server 2022, Tesla T4, D3D12) real machine: The game is started with `Marchwind64.cmd --debug`, `ssh -L` on Mac forwards the port in `debug.json`, and the local running directory writes the forwarded `debug.json` (port, original token) and `remote.json`, `srw64_attach` (with run), status, screenshot, keys, pad, ui.tree, ui.click, settings, window, and wait are all normal; the screenshot is retrieved through `file.read` (`local_file` takes the file name according to the Windows path). The pitfalls that were fixed at that time: plume's D3D12 `copyTextureRegion` asserted the empty texture when copying to the buffer, and the game aborted after taking the first screenshot (`prepare_rt64.py` patch). `Session.launch` (`srw64ctl launch`, MCP's `srw64_launch`) is still not available on Windows: it uses `os.pipe` plus `pass_fds` to make the game exit with the startup process; the player path (the switch in the options or `--debug`, plus `srw64_attach`) is not affected.

The pre-war page return can run `.venv/bin/python tools/recomp/debug/check_battle_ui.py`; the mental and active attack return process can run `.venv/bin/python tools/recomp/debug/check_battle_spirits.py`. Both build the current native host, enter through the main menu `mini-enter`, and do not enable legacy character selection. `status.mini_stage.waiting_reason` diagnoses why the level is not ready; only `ready=true` begins map operation. Screenshots and assertion results are saved in their respective debug session directories.

Weapon changing before battle and spirit casting on the spot are executable. `.venv/bin/python tools/recomp/debug/check_battle_actions.py`: Enter the mini level from scratch to verify active attack weapon changing, actual SP deduction, spirit effect refresh, counterattack/avoidance selection retention, co-driver SP, and Chinese/Japanese/English left and right mirror layout. Executed via `ui.click`, `ui.key`, `status.battle_page` and GPU screenshots without overwriting combat snapshots.