> **Language / Ngôn ngữ:** [English](bug-report.en.md) · [Tiếng Việt](bug-report.vi.md) · [中文](bug-report.md)

# problem report

2026-10-07. The "Feedback" page of the settings window (`frontend.cpp feedback_page`, between "Actions" and "About") has three lines:

- **Platform information**: "Copy platform information" puts a few lines of text into the clipboard (`bug_report::summary`: version, original/HD, HD package version; system, model, processor, architecture, memory; graphics API and graphics card; window and pixel size, interface size, language, widescreen, filter and frame; controller, touch screen, handheld; number of open corrections and cheats). The page will also display what is copied, and the player will paste it into the Issue.
- **Issue Report**: Write a zip for "Export Issue Report" and attach it when raising issues on GitHub (Issue form `.github/ISSUE_TEMPLATE/bug.yml` please ask them to attach it).
- **Where to give feedback**: "Feedback on GitHub" opens the form selection page of Issues; "Official website provides text comments" opens the official website story page in the current language.

Available on all platforms, including Android and Steam Deck. 8 tabs are squeezed into one line, the left and right inner margins of the tabs are reduced from 10dp to 6dp, and the English page name uses Report (`test_settings_window` checked by width).

## What to export

`<用户目录>/reports/Marchwind64-report-<日期>-<时间>.zip` (`src/host/bug_report.cpp`):

| Documentation | Content |
| --- | --- |
| `report.json` | `srw64.bug-report.v1`: `system` (platform, system version and build number, model, processor, core number, memory, whether it is Steam Deck; Linux also has a release version, kernel, desktop and session type, Windows has the version number and whether of RtlGetVersion Wine, Android has system version, SDK, manufacturer model, chip); `game` (`frontend.cpp report_facts`: version, language, interface size, original/HD, whether the HD package is installed with the version, widescreen, filter and frame file names, open rule corrections and cheats, controller name, touch screen, handheld, debugging interface, window size, graphics API and graphics card name/manufacturer/driver/video memory `srw64_graphics_info`); `files` (other files in zip) |
| `settings/*.json` | `presentation.json`, `input.json`, `rules.json`, `update.json`, `saves/settings.json`, `hd/hd.json` in the user directory (whichever one comes with which one) |
| `sessions/<编号>/launch.json`, `sessions/<编号>/run/*` | The last 3 runs kept in the user directory (this run ranks first): `launch.json`, and the non-empty `.json`, `.jsonl`, `.log`, `.txt` in the run directory, including `console.log` |

Not included: ROM and ROM copy in the running directory (`runtime-data/`), archive, recorded audio (`audio-output.s16`), screenshots, `debug.json` (token for debugging interface), `last-rom.txt`. The home directory in each text file is written as `~` (even the JSON-escaped `C:\\Users\\…` and forward slash writing on Windows are also changed). If a single file exceeds 4 MiB, only the last 4 MiB is retained. zip is written in memory with miniz (librecomp has been linked), and then written out using the `std::filesystem` path, so the user name on Windows can be written even if the user name is not ASCII.

After exporting, this line displays the file location; for platforms that can open folders (desktop and Android), click "Open the folder where it is located"; for Android, open the `reports` folder in the "Files" App; for Steam Deck game mode, touch screens, and handheld devices, click "Copy file path."

## console.log

Previously there were no log files on the player side: the host's `SRW64_*` line and RT64 output were only to stderr, macOS was discarded directly when opened from the finder, and Windows was only in the console window. Now `main` initially calls `console_log::start()` (`src/host/console_log.cpp`): stdout and stderr are each connected to a pipe, and the read content is written back to the original place (terminal; Android goes to logcat, replacing the original `forward_output_to_logcat`), and at the same time, it is written to `console.log` in the current running directory. The running directory is only known in `run_host` (`console_log::attach`). The previous output is first stored in the memory (up to 1 MiB), and is written first after being connected. Wait up to 0.2 seconds for the pipe to drain when exiting. In addition to stderr, Linux's crash handling (`crash_backtrace`) also writes the traceback directly into `console.log`, because the pipe may not be read when the process is crashing.

Therefore, after crashing or freezing, if the player reopens the game and exports it, the `console.log` of the last run will also be in the report (the user directory will retain the last 3 times).