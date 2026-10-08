> **Language / Ngôn ngữ:** [English](recomp-progress.en.md) · [Tiếng Việt](recomp-progress.vi.md) · [中文](recomp-progress.md)

# SRW64 recomp implementation record

2026-09-12 Supplement: The clearance slots for the first episode have now been read through the native cold start, the total round of preparation has been restored to 7, the capital is 14,500, and the Manami level 2 / SP 102/102 has been checked; the second episode has not been entered, and no reference simulator comparison has been added. Digest verification and rollback have been added to historical SRAM selection, see [Current Archive Recovery Record](../guide/native-save-recovery.md) for details. The following "Reading of customs clearance slots to be verified" remains as the evidence status at that time.

Updated: 2026-09-08. Working base point: `bc93a869e99fcafaf2c836751a6d46ee9c7a14dc`.
Game text is now drawn by a cross-platform text engine, see [Chinese, Japanese and English cross-platform text and game dialogue](../native/portable-text.md); the font probe at that time has been deleted.
The goal is still to complete "New Game → Complete Battle → Clearance and Preparation → Save → Exit and Restart File Loading" in the Japanese version.
See [Native Content Architecture](../native/native-content-foundation.md) for the current status of language access. RT64/Metal native host has been advanced from the new game to the first chapter of the female super series
Complete the level and save for a total of rounds 7 and 14,500 funds. The user requests that the automatic test stop at this archive, and the user will
Trial play; the restart, loading and maintenance operations of the clearance slot remain to be verified.
For keyboard bindings and startup entry, see [Native Trial Instructions](../guide/native-playtest.md).

## Obtained evidence

| Project | Measurement results | Scope of evidence |
| --- | --- | --- |
| Toolchain | macOS arm64 compilation of N64Recomp, RSPRecomp, n64sym, full N64ModernRuntime and RT64 successful | Linked task record host and RT64/Metal graphics host |
| Startup mapping | The resident load range at the initialization entry is the same as the ROM byte by byte, BSS is zero, and the stack address matches | ares runtime observation |
| Native LZ | 6,436 / 6,436 resources consistent, 57,061,848 decoded bytes in total; AddressSanitizer runs on arm64 after generating C via | three native MIPS functions; ROM I/O, allocation and deallocation are provided by explicit experimental adapter |
| In-game LZ | Captures a call and return from the original game, the 127,016 byte output is consistent with the independent decoder | The original function is indeed used in the game, and the parameters/return/stack and decoding semantics have been cross-confirmed |
| Load ranges | Recovering 20 transfers, 18 different ranges, from a set of straight-line load functions | One of them is a zero-length transfer and one is 16 bytes of zero data; you can't call the number of ranges the number of code overlays |
| Overlay content | ROM `0x121560..0x184730` is identical to RAM `0x801C2600..0x802257D0` in full range | 405,968 bytes of runtime load content; this observation is not named for a human-accepted scenario |
| CPU function scan | After reviewing the text/data boundary, there are 3,526 candidates; there are 3 more precise splits at the system entrance | 3,407 reserved CPU functions are generated; scenario running is still required to verify boundaries and indirect calls |
| System binding | 282 complete normalized signature matches among 355 function tags of n64sym; 122 system names applied in combination with instruction-by-instruction review | Contains runtime alternatives and omitted system internals; 11 residual calls use diagnostic entry with clear error reporting |
| CPU native execution | 600 consecutive VIs, 296 graphics tasks, 598 audio tasks, 1,186,432 audio samples, sample rate 44,100 Hz | Game entry and thread native execution; graphics using task recorder, audio samples into diagnostic receiver, screen/speakers not verified |
| Native overlay reading | ROM `0x10DA50` → RAM `0x801C4500`, long `0x7C50`, all bytes are the same as ROM | The function lookup table is updated after the game blocking read is completed; this observation only covers the overlay |
| Native GPU screen | RT64/Metal actually runs on Apple M4 Max; the draw hook reads back PNG through the completed GPU blit | The opening starry sky, zoomed Japanese and public prologue have been viewed; the first paragraph of content is consistent with the existing simulator picture, and pixel-by-pixel/full scene comparison has not yet been done |
| Native input | Independent N64 button bitmask press VI tick playback to advance the public prologue | Input file with schema, source script hash and compiled hash; do not mix RetroPad numbering and native N64 mask |
| Female super type | `gfx-probes/female-route-1` Completed 5,400 VI; View present-2400 Confirm the default names of the heroine Malino・Hamaru and the opponent Aアイシャ・リッジモンド; present-2700 is the opening of the route | Verified selection and naming, not reached the tactical map |
| The first tactical map | `gfx-probes/female-map-audio-1/present-6660.png` has shown terrain, towns and enemy units; present-7080 shows the appearance of our units in blue | The actual GPU screen has been viewed; player movement, attack and clearance are still to be verified |
| Map operation and interrupted save and load | `female-map-audio-3` The two initial units move, standby, and save; after exiting, `first-map-reload-2` restores the first round, funds 0, unit position and action status | The native cross-process tactical save and load pass; the pass preparation and save still need to be verified |
| First complete engagement | `first-map-reload-2` Enemy missile attacks Big Titan 3, HP 8000 → 7990; enemy aircraft HP 1500 → 0 after solar laser counterattack, returns to map after explosion and triggers next engagement | Complete attack/counterattack/settlement/return map has been viewed; not the entire level completed |
| The first episode is cleared and saved | `first-map-turn5-reload-1/present-34260.png` shows the first episode is cleared, Malani level 2, total round 7, funds 14,500; 32 KiB SRAM has been frozen | Defeat all enemies natively, post-war plot and pass the level save; the restart reading of this slot has not been compared with the reference end |
| RSP task | Capture real graphics and audio OSTask, record microcode, data, commands and hashes | Task submission evidence; does not mean that native screen or speakers have been connected |
| Native audio task | A real task is completed; the 117 recorded RSP DMA writeback ranges are all consistent with the reference end, and ASan passes | The reference end is the RDRAM after the same task and before the next load; SP HALT/BROKE/SIG2 are all set |
| Native audio output | `gfx-probes/female-map-audio-1` has been connected to the SDL audio device; the user reported "I heard the sound ok" during this run | The native opening audio passed the manual audition; it cannot be used to overwrite the battle sound effects that have not yet entered |
| Warehouse inspection | 39 tests of `make check`, Python compilation and dependency check passed | Static and tool testing; does not replace native scene acceptance |

Japanese version of SHA-256:
`ee5f4a21d8e5f7827d21199e27800edf250df9a8e4d10befb1a6992df597b13e`.
The independent reference for native decompression is this repository `src/srw64_rom/resources.py`.
The audio reference port is fixed ares v148; the vector implementation of the runtime is also derived from ares, so the output comparison proves
The consistency of this task's recompilation/access path is not a proof between two completely independent hardware implementations.

Follow-up `gfx-probes/female-story-1` Originally planned for 11,400 VIs, but process exited with code 0 at 5,473 VIs
End; cannot infer complete input with `native-graphics-frames-captured` from its old report.
The exit source was not recorded at the time, and it cannot be concluded that the user closed the window or the game malfunctioned. The window exit event log has been added.
And runs with insufficient actual VIs are individually marked as `native-run-ended-before-VI-limit`.
GPU screenshots are now attached with the JSON of the draw-time VI, and the image and metadata are written only after the GPU command buffer is completed.

In order to continue the combat operation of the same process, the host adds `control.txt` atomic command reading, `live-state.json` per second
And `control-events.jsonl` recorded according to the actual VI; the tool entry is `tools/recomp/run/control_host.py`.
Live keystrokes have been made in `female-story-2` to advance character dialogue on the world map; actual VI and keystroke events are saved in
The current running directory. This item only proves that the input is effective and cannot replace tactical map, battle or save and load verification.

`female-map-audio-1` Subsequently, two of our aircraft have been operated on the first tactical map to move and stand by.
But exited with SIGBUS after about 19,333 VI. System crash stack confirmation `srw64_queue_audio`
Unusually large sample lengths were replicated. Audio dispatch of raw `0x8007E28C` reads AI_LEN, by target
736 frames minus remaining frames plus 240, finally written as signed halfword; write entire SDL queue as AI_LEN
Will make this length negative when backlogging. `n64/ai/io.cpp` of ares v148 reads
`dmaLength[0]`, which is the current DMA, not the sum of the current and subsequent segments.

The first patch changed to track the current DMA, but `female-map-audio-2` exposed another issue: user feedback
Sound and image are out of sync, 17,418 VI After normal stop, SDL queue peak is 1,480,816 frames,
That’s 33.58 seconds. The current DMA length does not reflect the total backlog of the native device, so this implementation does not pass synchronization
Acceptance. `sync-issue.json` Preserves manual feedback and measurements; audio cannot be passed as "no crashes".

The current host reuses the entire device queue to feed back the synthesized beat, retains a VI output margin at the front end, and
The amount of feedback is limited to a VI and is then handled by the runtime's existing lead times. This is SRW64 native audio
Adaptation, does not claim to fully simulate AI two-stage FIFO. Input outside the AI DMA length range will clearly report an error;
When the device backlog exceeds 100 ms the old queue is discarded and a recovery event is logged, normal playback should not require this recovery.
Added `audio-live.json` to record queue duration and recovery times per second.
`tests/native_audio_queue.cpp` now combines the original game length formula with the 512 frame device consumption granularity,
The delayed callback combination ran 36,000 VIs while checking length and backlog caps, and ASan/UBSan passed.
The native rerun directory is `female-map-audio-3`. Two consecutive minutes, 120 samples, covering
VI 2,924..10,064: SDL queuing time is 24.67–38.82 ms, mean 30.98 ms;
As of the end of sampling, the peak value of the entire run is 41.00 ms, and the number of backlog recovery times is zero. The evidence is located
`audio-timing-report.json` and `audio-timing-observations.jsonl`.
This item verifies that the device queue no longer continues to grow; the actual output delay of the sound card and complete audio and video synchronization are still accepted by actual playback.
The process then ran to 23,100 VIs and exited normally after a control command; the final peak value of the device queue was still
1,808 frames (41.00 ms), zero backlog recoveries, no recurrence of the previous crash of ~19,333 VI.

Then `first-map-reload-2` continues until 70,583 VI (approximately 19.61 minutes), covering multiple rounds
The enemy's counterattack, our active attack and return to the map. Device queue peak for this checkpoint was 2,016 frames
(45.71 ms), the recovery count is still zero; see `audio-sync-checkpoint.json` in this directory.
Passed 39 tests for `make check`, Python compilation checks, and dependency checks; native audio
Cohort tested by ASan/UBSan. Here we only prove the device queue and native process, and do not write them as
Sound card loopback measurement or user's manual acceptance of battle picture and sound synchronization.

The process is then saved at round 5, capital 8,300, running to 100,968 VI, via control command
Normal exit (measured 1,683.92 seconds). The final audio queue peak is still 45.71 ms, with zero recoveries.
Freeze the SHA-256 of `first-map-turn5.sram` as
`591c7db67fb909bc4216f16103757309332fe12e7c65cc64636559cba5579953`.
Follow-up `first-map-turn5-reload-1` continues from this archive; also starts this startup phase of the reference simulator
Eight backlog recoveries were recorded at VI 292..536, peaking at 5,008 frames (113.56 ms). subsequently until
VI 70,770 exits normally, no increase in resume times, typical queue time is about 25–40 ms. This phenomenon occurs simultaneously with parallel startup loads and has not been demonstrated
The only cause and effect; it is reserved as the risk of short-term sound skipping during the startup phase and cannot be covered up by the previous zero-recovery operation.
This startup also shows that the absolute VI input script will be affected by the initialization progress: fixed title script is not completed
Continue, and then continue to read files successfully through actual menu screenshots and control events.

In this process, in the seventh round, I used "Hot Blood" and Santiago to defeat the last battle monster,
Advance the post-war story and save the first episode clearance status in Save 1 of the ROM cartridge. The frozen file is
`first-map-turn5-reload-1/stage1-clear-turn7.sram`, SHA-256:
`0c6ded15fdf60c6b0064b2260a335d17a4ff77386d14d634bfd7d3bcb8de7484`.
`intermission-save-evidence.json` Record save screen and status; user subsequently requests automatic testing
This is the end, so we will not continue with the second episode, preparation operations, clearance slots and restart reading.

To hand over manual playback, the host adds focus-restricted SDL keyboard input and uses atomic state snapshots across threads.
`scripts/Play SRW64.command` / `tools/recomp/run/play_native.py` Copy the above frozen archive for the first time, and later
Copy the SRAM of the most recent standalone trial directory; only one trial process is allowed to be open at a time. Interactive mode is not set
Automatic exit time limit, GPU pictures use the fixed file name of the latest screenshot. The new host is already in
`keyboard-build-smoke-1` Completed 600 VI startup check; physical keyboard and speaker synchronization are still checked manually.

In `female-map-audio-3/present-10500.png`, the game shows that the in-map save is complete.
The original SRAM SHA-256 was `97a08fb524d03b8f0caaf344205b1dda9f5ea18b42bd48d0627b146998e19904`,
After saving, it will be `b340a9c686b627d00dfaee9b4d89c896039547f8d607cb51b035d3f7bb2d756b`,
Both are 32 KiB in length. The independent frozen copy `first-map-turn1.sram` will be used for new processes to read files;
The current status is the first round, the capital is 0, and the two initial friendly units are moving and waiting. This is a tactical interruption to preserve evidence,
The complete battle, clearance preparation and saving of this stage still need to continue to be verified.

`first-map-reload-2` Use that frozen SRAM to complete the header in a new process → Continue →
Tactical map. present-1320 displays the position of the two machines after moving and the gray status of the action;
The system menu of present-1740 shows Round 1, Funds 0. Evidence and hashes can be found in this directory
`save-reload-evidence.json`. The title menu rotates options through the left and right keys, and the Continue button at the top of the screen
You cannot use the up key to select directly; the first time you try to enter a new game, it is not counted as a successful file load.

The same frozen SRAM has also been read by the fixed Mupen64Plus-Next core cold boot. Save natively as
Big-endian; the reference core's aggregate save area places 32 KiB SRAM at `0x20800`, according to its
S8 access rules for `sram.c` After converting intraword endianness, only write to this range and do a complete readback check.
The reference end actually restores the map through Continue, the body position matches the action status, and the menu is displayed.
First round, capital 0. The SRAM hash remains the same before import and after the reference run. The evidence is located
`reference-save/turn1-load-1` and `turn1-inspect-1`; the entry is
`tools/recomp/probes/run_reference_save.py`. This is the actual reference simulator file reading and screen comparison.
The reference side live state is not used as a native checkpoint, nor does it overwrite the unfinished clearance status.

The native save of Round 5 has also been restored to 8,300 funds in the reference simulator, and the map and machine positions have been
`reference-save/turn5-load-1`, `turn5-inspect-1` comparison. Further from the same SRAM
Replay the recovered state and the protagonist moves three spaces down and one space to the left, and uses a 100% hit rate
Dexter's HP: Both native and reference versions have changed Dexter's HP from 3,000
Dropped to 0, the protagonist's HP remains at 3,881, and EN drops from 85 to 45. The reference end actually executed the
Mobile and complete attacks; `reference-save/turn5-attack-1/visual-comparison.json`
Record the corresponding picture and hash. This does not deduce that all random battles, frame timing, or subsequent levels will be consistent.

The identity of the current Japanese version and 5600 model experiment is locked in `config/recomp/rom-variants.json`, the host's
The XXH3 identity table is generated from this file. Verify complete ROM SHA-256, initial 1 MiB and all before compilation
Censored load segment; CPU results from verified Japanese builds. Native language switching always uses the Japanese ROM.

## Platforms and hardened boundaries

Currently running macOS ARM64 + Metal host. Windows/Linux are targets that can be adapted along the upstream architecture,
This project has not yet been compiled and game verified for these platforms. A browser version is also not yet implemented.

Upstream [RT64](https://github.com/rt64/rt64) currently lists D3D12, Vulkan, Metal and
Windows/Linux/macOS, no out-of-the-box WebGPU backend. If you make a browser version, plan to reuse the automatically generated game C
and resource parsing, with additional verification of Emscripten/Wasm, threads/message queues, memory allocation, graphics, and persistent archiving.
Fixed version of N64ModernRuntime's librecomp also links against LiveRecomp/SLJIT; web builds must be reviewed and
To isolate this type of native runtime generated code path, you cannot just change the CMake compiler to emcc.
[Emscripten pthread documentation](https://emscripten.org/docs/porting/pthreads.html) explains multithreading
Depends on SharedArrayBuffer and COOP/COEP; [Runtime Environment Document](https://emscripten.org/docs/porting/emscripten-runtime-environment.html)
Explain the difference between browser main loop and file persistence. These are follow-up adaptation plans and there is no proof of Wasm executability yet.

[Zelda64Recomp](https://github.com/Zelda64Recomp/Zelda64Recomp) combines static conversion, modern runtime layer,
RT64 combined with game-specific patches. In fixed reference version read, `patches/sky_transform_tagging.c`
Assisted inter-frame interpolation through transformation flags, `patches/ui_patches.c` adds extended GBI and interface alignment,
`patches/autosaving.c` Selects the save time based on the game state. If SRW64 is to be strengthened, it also needs to be identified and modified.
The game's drawing, layout, timing, and saving logic; these Zelda patches are not intended to be direct replacements for SRW64 functions.

## Startup, memory and loading

Observed startup relationships:

- ROM header entry: `0x80076610`.
- Initialization entry: `0x8007F5B8`, stack: `0x8010F0B0`.
- Resident load: ROM `[0x1000, 0x5BC30)` → RAM `[0x80076610, 0x800D1240)`.
- The resident CPU text is followed by RSP boot, and the end of the text is ROM `0x4DEA0` / RAM `0x800C34B0`.
- Start BSS: `[0x800D1240, 0x8018DAC0)`.
- The current emulator's `osMemSize` is 8 MiB; the capturer now reads this field by default. Early 4 MiB
The file is a partial RDRAM snapshot and cannot be used to exclude code or data in the Expansion Pak area.

`0x8007F704` is the blocking ROM reading wrapper function of the game. The parameters are ROM offset, RAM destination,
Length; internally splits PI DMA by at most `0x400` bytes and waits for messages. load function family
The constant parameters of `[0x8007FD80, 0x8008016C)` can be reconstructed from `analyze_layout.py`.
The parser supports the small number of instructions that actually occur, handles JAL latency slots, and refuses to continue on unknown instructions/arguments.

Different ROM ranges are repeatedly loaded into `0x801C2600` or `0x801C4500`, and transferred to `0x80400000`.
Therefore, the function identity must include the ROM segment and the runtime lookup table must be updated with the load, not just RAM
The address gives the function a globally unique name. Current scan exports `load_ROMOFFSET_func_VRAM`, identity preserved.

The first round of resident code generation failed due to missing `0x801FD020` symbols. One of its sources is currently confirmed to be
ROM `0x15BF80`, belongs to `load_00121560`. After filling in candidates differentiated by load range, the original
Missing symbol issues for 64 different external JAL targets are no longer the first blocker for the generator.
This conclusion does not mean that all calls have runtime binding acceptance.

The generator may directly bind a target address that appears only once to a certain ROM segment, but the uniqueness of the candidate does not prove
There is no code for this address in other sections. The current build explicitly changes 7,213 named calls to overlay to
`LOOKUP_FUNC` of the same MIPS address retains the function definition and original calling address.
Reading the entire ROM section still executes the original MIPS function; after returning, all read bytes are checked, and then the conflicting section is unloaded and
Register new segment. Just a single PI DMA update runtime by `0x400` does not represent that the full overlay has been loaded.

The first real host run triggers an access error when reading `AI_LEN_REG` from `0x800AEBC0` on game thread 3.
Confirm that it is `osAiGetLength` instruction by instruction and then receive it from the runtime library. The next round of continuous operation will pass.
The guest clock of `osInitialize` is globally filled with `46,875,000` and NTSC VI clock according to the original instructions.
`48,681,812`; Currently it is a static semantic access, and the field-by-field comparison of the original function return point has not yet been captured.

The 11 unsupported entries in the diagnostic host print the function name and terminate; no fake success value is returned.
The current successful run does not trigger them and cannot therefore claim Controller Pak, Transfer Pak or all
System calls are supported. Each run uses a new independent SRAM/config directory and has not been verified for cross-process archiving.

The task recording host completed an additional 1,800 VI runs continuously: 896 graphics tasks, 1,797 audio tasks.
The graphics host's `gfx-probes/boot-3` completes 600 VIs and outputs 5 GPU images;
The first paragraph of the public prologue of `start-1/present-420.png` is the same as the existing
`build/libretro/start-scan/screenshots/frame-000900.png` has the same content. The output pixels of both
The proportions are different. Only the scene/text correspondence obtained by direct viewing is recorded here.

## Audio microcode and task comparison

The observed boot microcode is located in ROM `0x4DEA0` / RAM `0x800C34B0`, size `0xD0`.
Its SHA-256 is
`5759e9bb21f2e504bfbb3e5b75173cb81aa50c60b19e77bcee1d0f6fc34e8fa4`.
boot will load `0xF80` bytes into IMEM `0x1080`; audio OSTask's `ucode_size=0`
Doesn't mean there is no microcode. The graphics task points to ROM `0x4DF70`, whose data shows F3DEX fifo 2.08.

Audio executable prefix is located in ROM `[0x4F300, 0x50120)`, long `0xE20`, SHA-256 is
`14e3b245e8cd4e0bdf4cbb864af82d1ccba6d3d3ff33f73cb52c5821a76f30fc`.
In the first round, the end was mistakenly cut at `0xE10`, and the host compiler found that `L_1E94` was missing; after checking the delay slot and tail jump
Corrected to `0xE20`. The subsequent CPU data is also read into IMEM by boot, but the current task does not execute it.
The 24-byte difference in the full `0xF80` block in the early capture starts at relative `0xE21`, with consistent executable prefixes;
This difference is not characterized as self-modifying microcode.

The audio command jump table is located in microcode data `+0x10`, corresponding to the 16 half words of ROM `0x59ED0`.
`audio-probe.toml` Explicitly record these indirect jump targets; check that the values in the snapshot are identical before replaying.
Audio experiments using N64ModernRuntime's real RSP vectors and DMA helpers. Only when generating code
The DMA write interface adds an observer, retains the original writing behavior and records the destination range.

Compare flow: Stop at audio `osSpTaskLoad` entry → Save descriptor with 8 MiB input →
Continue to next consecutive `osSpTaskLoad` entry → Check SP status and save reference memory →
The unit plays back the same input → compares all recorded DMA destination ranges.
The SP status of this sample is `0x243`, and all 117 writebacks are consistent. Follow-up `female-map-audio-1`
The native PCM has been output via SDL, and the user confirmed that the opening audition is normal. Complete BGM, various combat sound effects,
Long playback and sample rate/mix timing still need to be covered independently.

## Rerunable entrance

```sh
# 隔离的固定版本分析工具；首次需要网络及本机 clang/cmake/ninja。
make recomp-bootstrap

# 静态装载范围与按段的函数候选。
make recomp-layout
make recomp-scan

# 全部资源的真实 MIPS → C → arm64 对照。
make recomp-lz

# 带系统符号复核、overlay 地址查找和明确 unsupported 诊断入口的 CPU 生成。
make recomp-cpu

# 编译完整 CPU 宿主并运行；目录必须新建，图形仍为任务记录器。
python3 tools/recomp/run/run_host_probe.py \
  --output build/recomp/host-probes/new-boot --vis 600

# 图形依赖与可选的运行时 Metal 源码编译适配；只改变 build/ 下的固定克隆。
python3 tools/recomp/toolchain/prepare_rt64.py
python3 tools/recomp/run/run_host_probe.py --graphics \
  --input config/recomp/inputs/start-scan.json \
  --output build/recomp/gfx-probes/new-start --vis 960
```

ares uses a baseline copy of `build/recomp/runtime/srw64-jp.z64` and independent settings, saving the file will not
Written next to the original `rom.z64`. Background behavior uses `Input/Defocus=Block`, allowing the simulation to continue without
Receive background keystrokes. Debug signal `S10` allows continuation of the original exception handler only on checked COP1 instructions;
Other unexpected exceptions will fail and be logged.

```sh
# 输出目录必须尚不存在；--already-halted 仅用于等待 GDB 的冷启动状态。
python3 tools/recomp/probes/rsp_capture.py \
  --session build/recomp/runtime/session.json \
  --output build/recomp/captures/new-memory

python3 tools/recomp/toolchain/analyze_layout.py \
  --capture build/recomp/captures/idle-8mb \
  --output build/recomp/layout-observed.json

python3 tools/recomp/probes/capture_rsp_tasks.py \
  --session build/recomp/runtime/session.json \
  --output build/recomp/captures/new-audio-task --count 6 \
  --snapshot-first-type 2 --snapshot-following-task

.venv/bin/python tools/recomp/probes/run_audio_probe.py \
  --capture build/recomp/captures/new-audio-task \
  --output build/recomp/audio-probe/new-audio-task
```

Main local evidence (all under ignored `build/`):

| path | content |
| --- | --- |
| `recomp/toolchain-build.json` | Tool submissions, compilers, dependencies and binary hashes |
| `recomp/captures/init-entry-2/` | Initialize entry register and part of RDRAM |
| `recomp/captures/lz-first-call-3/report.json` | In-game decompression call and output comparison |
| `recomp/lz-probe/report.json` | Native results for 6,436 resources |
| `recomp/captures/idle-8mb/` | 8 MiB runtime memory and hashing |
| `recomp/layout.json` | Load functions, ranges, hashes, external calls compared to the current snapshot |
| `recomp/cpu-scan/report.json` | 3,526 candidate segment scan commands and results |
| `recomp/cpu-bound/report.json` | System bindings, generated file hashes, overlay call adaptations and unsupported manifests |
| `recomp/host-probes/boot-2/` | Record of failure at AI hardware reading after entering the game thread for the first time |
| `recomp/host-build/boot-2-debug.log` | Native access error location captured by LLDB |
| `recomp/host-probes/boot-3/` | Successful runs and task count of 600 VIs; memory snapshot is for diagnostics only |
| `recomp/host-probes/boot-4/` | 1,800 VIs running continuously and task count |
| `recomp/gfx-probes/boot-3/` | Opening GPU pictures and full run report |
| `recomp/gfx-probes/start-1/` | Start replay and public prologue first screen |
| `recomp/gfx-probes/prologue-1/` | Press A to advance to the GPU screen of the second public prologue |
| `recomp/captures/rsp-tasks-idle-2/` | 24 graphics/audio tasks and microcode samples |
| `recomp/captures/audio-differential-1/` | Input and next load boundary snapshot of the same audio task |
| `recomp/audio-probe/differential-1/report.json` | 117 DMA range comparisons for native audio tasks |

## Next step and completion threshold

1. Continue scenario coverage and system compatibility review. Build, native compilation, and one continuous run passed; verification required
Same-site overlay switching, indirect calls, system global and post-start paths.
2. Continue RT64 scene comparison and advance maps and battles. Protagonist selection, naming, route opening and opening audio have been
Obtain evidence; GPU, input and audio device outputs need to cover the combat path.
3. Expand the language, target scenarios, and archive acceptance of the unified JP profile; keep each type of evidence independent.

Automation is responsible for sampling, analysis, generation, compilation, playback and comparison; retaining input identity, command,
Status and logs, and then advance to specific gaps. The generation is successful, the components are running, the target scene and the entire game are completed respectively.
record. Overall completion percentage is not currently reported, nor are playable loops replaced with function numbers.