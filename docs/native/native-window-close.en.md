> **Language / Ngôn ngữ:** [English](native-window-close.en.md) · [Tiếng Việt](native-window-close.vi.md) · [中文](native-window-close.md)

# Host exit issue when closing window

2026-09-12 Update: The cooperative stopping, awakening and complete recycling of the game thread have been implemented; the final versions of the modern name→plot closing window and the original name page closing window have been passed. The original "4 game threads are still alive when RDRAM is released" bug has been eliminated in these entries. The results and complete evidence of this round of automatic exit of VI are summarized in the acceptance record below; we do not claim that the entire game, archive recovery, or any stuck scene has been accepted based on this.

## 2026-09-12 Fixed

The source code is located in `tools/recomp/toolchain/prepare_runtime_lifecycle.py` and `src/host/runtime-support/guest_shutdown.hpp`. The generator is checked against a fixed version and produces local adaptations of `threads.cpp`, `mesgqueue.cpp`, `scheduling.cpp`, `timer.cpp` and `recomp.cpp`, leaving the upstream checkout and build CPU C unchanged.

- Register the host thread created by `osCreateThread`, and use the same lock for registration, release of thread handle and initialization confirmation. Reject new threads after exit; prevent the cleaner from destroying the initialization semaphore in advance when the thread exits immediately.
- Wake up scheduling waiting and external message waiting when exiting; the game thread throws an existing termination exception at runtime at the scheduling/message safe point, and the exit path will no longer restore game logic or continue to schedule other threads.
- The cleaner no longer stops prematurely with `exited` and must join all registered threads one by one. The thread context that has been joined during exit is retained until all game threads end, preventing threads that are still in the scheduling operation from accessing the released semaphore.
- RDRAM is released after the entry thread, timer, event thread, game thread cleaner and save thread are all recycled. Game threads that have not reached the stop checkpoint will prevent release; no forced release, detach, or delay is used.
- The binary reuse fingerprint is added to the life cycle generator and support source code. After modifying these files, the old host cannot be used as the current repair evidence.

Verification distinguishes between host exit codes, actual join records, and macOS thread observations. `shutdown_verified` requires an equal number of creations/joins, clear zero thread observations before and after RDRAM is released, and join logs before release. When the system thread enumeration is incomplete, `UNOBSERVED` is output and cannot be regarded as zero thread.

This round of component testing uses the actual adapted scheduling/messaging/cleaning source code. ASan/UBSan covers blocked reception, idle message waiting, unstarted threads, running polling, normal destruction/reuse, retention of scheduling objects during exit, 40 times of creation/exit race conditions, no game threads and repeated joins. The entry is `make recomp-guest-shutdown-test`, and `make recomp-native-check` has been added.

### Final acceptance

Summary: [guest-shutdown-check/verification.json](../../build/recomp/guest-shutdown-check/verification.json). The three portals use the same final host binary, handwritten source code summary and life cycle adaptation, all silent.

| Run | Exit path | Host exit code | Created/joined | Survival game threads before/after releasing RDRAM |
| --- | --- | --- | --- | --- |
| `name-window-final` | Complete modern name verification, write-back, zoom, real window closing after entering the plot | 0 | 4 / 4 | 0 / 0 |
| `original-window-final-2` | The original name selection page is truly closed | 0 | 4 / 4 | 0 / 0 |
| `vi-stop-final` | 600 VI upper limit triggers runtime exit | 0 | 4 / 4 | 0 / 0 |

The status of the two wrappers that closed the window in advance is `native-run-ended-before-VI-limit`, and the CLI returns 1; this is the original strategy that has not reached the preset VI upper limit, and the host exits normally. The actual acceptance is judged based on the host exit code, window closing action, join and system thread observation.

The first final run of `original-window-final` encountered an incomplete system thread enumeration before being freed; its `shutdown_lifecycle_verified: false` was left intact and not counted as a pass. Subsequent `original-window-final-2` of the same binary obtains the complete observation. Early `original-window-1` / `name-window-1` are intermediate versions before the reinforcement context is retained and are not counted in the final matrix.

- `make check`: 98 Python tests, compileall, dependency checks passed.
- `make recomp-native-check`: 9 component programs passed, and the new game thread component uses ASan/UBSan; the actual native host is not built using sanitizer.
- The three graphics host target builds passed, and the upstream N64ModernRuntime checkout was not modified.
- `page-exited-to-story-window.png` of the final modern name run has been viewed, custom nicknames, Chinese dialogue and 1200×800 windows render normally; not expanded to full scene visual acceptance.

This fix closes the reoccurring "RDRAM released while game thread is still alive" bug. There is no verification of full game or SRAM cold start recovery; for any infinite loop that no longer calls the schedule/message checkpoint, the cooperative stop may wait without returning, and the memory will not be released beyond the join at this time.

## Historical reappearance and evidence before restoration

The following is the original record from 2026-09-11. At that time the defect was acknowledged but not fixed; normal process exit could not overwrite these thread evidences.

## Current verification

Summary of evidence: `build/recomp/window-close-check/verification.json`. All tests are muted and use a new run directory for each round.

| Running directory | Path | Process exit code | Game thread after releasing RDRAM |
| --- | --- | --- | --- |
| `window-1` | Full name of new page → Story → Real Cocoa Close window | 0 | Diagnostics not enabled |
| `control-trace` | Full name of new page → Plot → VI script exit | 0 | 4 |
| `window-trace` | Full name of new page → Plot → Real Cocoa Close window | 0 | 4 |
| `original-ui-trace` | Disable the new name UI and close the window in the original word selection interface | 0 | 4 |

The actual closing of the window here is made by calling the window's own closing action through `NSWindow.performClose`, which is generated through SDL's window delegation. There is no direct synthesis of SDL_QUIT, and no process killing. `window-close-events.jsonl` records actions and VIs. `run_host_probe.py` Returning non-zero CLI status for early window closing is a strategy for not reaching the upper limit of the VI. The return value of this wrapper cannot be regarded as a host crash; `report.json.exit_code` shall prevail.

Three rounds of complete name checks were confirmed: protagonist/partner editing, Tab/Shift-Tab, window keyboard dispatch, invalid input and duplicate name rejection, cancel re-entry, confirmation page return for modification, eight name fields for two people, and custom nicknames in the plot. 800×600 → 1200×800 After scaling, the GPU/dialogue raster size is consistent, and the dialogue and frame positions in the actual window have been checked. The latest screenshot is at `window-trace/page-exited-to-story-window.png`.

## Exit evidence

`SRW64_SHUTDOWN_TRACE=1` Enabled only in diagnostic runs. Before and after `recomp::start` releases RDRAM, check the current host's own thread through macOS `proc_pidinfo`. It is observed that **Game Thread 1, 6, 4, and 3** are still alive when the script exits and Cocoa closes the window. Same result after disabling the new name UI. They wait for most of the sample; Game Thread 1 is running during one pre-release sample.

So it has been confirmed that the runtime does not wait for all game threads to finish before releasing the memory they still reference; this is not an issue unique to the new name interface. SIGSEGV is not triggered again this round, and the new diagnosis may also change the race sequence. Four normal process exits cannot be interpreted as having been repaired.

The original crash occurred at `build/recomp/name-page/final-hd/`, the log ended at `SRW64_WINDOW_QUIT event=256 vi=2855`, followed by the host exit code `-11`. Direct evidence was obtained after re-reading the system crash report:

- The main thread is located at `__munmap → recomp::start → main`.
- The faulty thread is `Game Thread 6`, located at `resident_func_8008AE90 → load_000A7EC0_func_801C28C8`.
- The fault address is `0x7000025c00`, which corresponds to the RDRAM base address observed by this machine `0x7000000000` plus `0x25c00`.

Originally reported as `~/Library/Logs/DiagnosticReports/srw64-gfx-host-2026-09-11-165355.ips`; the stack and hashes related to this issue have been extracted to `build/recomp/window-close-check/original-crash-evidence.json`.

Fixed runtime `thread_cleaner_func` ends the loop after `exited` is set; the exit process only waits for entry, event, cleanup, archive and adapted timer threads, without completely stopping, waking up and recycling all game threads created by `osCreateThread`. The repair must first complete the cooperative exit and join of the game thread, and then release the RDRAM. It cannot rely on delayed release or hidden crashes.

## Recurrence

At that time, the complete naming and real window closing were driven by the control file of the AppKit name page and verify_native_name_entry.py, both of which have been deleted with the AppKit page; the current name page is driven by the debugging interface (see [Native Name Input](native-name-entry.md#验证与证据)). When verifying the original input UI, add `--original-name-entry` to the launcher and use `verify_window_close.py --run RUN --at-vi 1350` to trigger the actual window closing of the specified VI. The close action is only available when `SRW64_WINDOW_CONTROL` is enabled.

This round only adds new verification entries, result records, and thread diagnostics that are closed by default, and the exit algorithm has not been changed. 60 tests of `make check` passed.

## Regression after code tidying up

2026-09-11: The universal window closing, zooming and picture mode test controls have been split into independent files (then `window_test_control_macos.mm`, now `src/native/ui/window_test_control.cpp`), which are called by the graphics host window update and no longer rely on the name page. The thread diagnostic source code is stored independently in `src/host/runtime-support/shutdown_trace.hpp`, and the generator still records the summary and injects it into the local runtime source code. The exit algorithm has not changed.

- `build/recomp/cleanup-check/name-window/`: complete modern name process, original verification, eight-field readback, 1200×800 plot display and real window closing, host exit code 0.
- `build/recomp/cleanup-check/original-window/`: Disable the native name page, call the actual window closing at VI 1350 in the original word selection interface; independent SDL scaling and Original/HD requests/applications also pass, with host exit code 0. This only validated the common control path and did not replicate the full art ROI comparison.
- 4 game threads were still observed after RDRAM release in both rounds. This new report clearly uses "process exit code 0" and records `shutdown_lifecycle_verified: false`, and does not equate normal process exit with safe recycling.

Three graphics host compilations, 60 Python checks, and 8 component programs of `make recomp-native-check` passed, and the entire test was silent. The latest sorting results are located at `build/recomp/cleanup-check/verification.json`; for the development and operation and maintenance entrance, see [Native Development Guide](../guide/native-development.md).