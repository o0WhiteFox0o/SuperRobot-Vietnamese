> **Language / Ngôn ngữ:** [English](script-skip.en.md) · [Tiếng Việt](script-skip.vi.md) · [中文](script-skip.md)

# Short plot skip (R + START)

2026-09-29. "Short skip" in modern machine combat: Press R + START (Keyboard E + Enter, Steam Deck R1 + Menu) during plot dialogue. The plot script will be executed directly to the next stopping point. The dialogue in the middle will not be displayed, and the waiting and performance will not be played. All commands are still executed by the original processing function, so the results of flags, variables, funds, unit appearance and movement, and map switching are the same as reading them sentence by sentence. Pressing B or turning on playback will stop you at your current location. Code: `skip_begin`/`skip_polls` of [script_skip.hpp](../../src/host/script_skip.hpp), [game_hooks.cpp](../../src/host/game_hooks.cpp), starting and stopping are handled by [dialogue reader](native-dialogue-ui.md) ([native_dialogue.cpp](../../src/host/native_dialogue.cpp)).

The previous skip just allowed the reader to confirm one page for the player each frame, and the script was executed at the original speed. There were a lot of performances, shots, and waiting. It looked like fast forwarding with lines flashing all the way (the world map segment in the first episode was about 14 seconds). The same paragraph is now completed in 2 VI.

## Script polling contract (static analysis)

The event engine is in `8015F950` and the context is in `+0x948` (hereinafter called vm). Each frame `8009E180` calls `8009EFDC(engine, vm)` once when an event is running, and writes the return value back to `engine+0x97C`.

- `8009EFDC`: When the command status `vm+0x24` is 0, the `FFFF` end event (status 0x80) is encountered; otherwise, `8009F0E8` processes the condition and route mark, and `8009EED0` fetches the instruction (the PC only advances 2 bytes, the processing function writes `vm+0x30`, and the status is set to 1). If the status is not 0, the processing function is called; after the call, the status is changed from 1 to 2. At most one poll is taken and the processing function is called once.
- The handler does its own thing: clears the status to 0 and pushes the PC through the parameters. `+0x26`, `+0x28`, `+0x2A`, `+0x2E` are their local fields and are cleared when fetching the instruction.

So to skip just continue polling in the same frame: take the next one as soon as the command is completed.

## Practice

1. The reader detects R + START (`Reader::update`), and there is currently a script being read, which is `script_skip::start(vm)`.
2. Before the first polling of this script frame (`skip_begin`): If it is just starting, first call `800A34D8` to close the dialogue window being read (same as `3D48`). After that, `8008FED4` directly returns 3 in the skip, which is the original reply of "This page has been read", and the dialog box does not open.
3. After each polling (`skip_polls`): The command just executed stops at the stopping point; if the command is still waiting, press the table to push it to the end point and poll again. When encountering a command that cannot be solved, give up the current frame and continue in the next frame. It will complete this section at the original speed.
4. Each skipped page can still be viewed (`Reader::skipped`). `8008FED4` is stopped with the panel and text numbers (a0, a1); the host calls the original `8008CE54` to read the speaker number in the record header, and the name is taken from the record `0x111E 加说话人数字`. This is exactly the record displayed in the original name box (`8008F648` is called `8008D0E8` with the original number of panel `+0x20C` plus 0x111E), so the protagonist and partner No. 25–32 are also displayed as the player's name through `record_text`. Save one copy of the text and names for each reading language. After changing the language, you can read back and change them. The page you were reading at the beginning will be skipped and will not be repeated, only the complete read entries will be completed. Episode 1 Actual Measurement: The four skipped pages of speakers (Katz, Katz, Brad, Katz) are the same as the game itself shows when reading sentence by sentence.
5. The sound effects are muted during the skip period (`8007E8A8`, -1 stops releasing), otherwise the commands executed in one frame will sound at the same time; BGM switches as usual.

| Command | Handler function | Method when frame is completed |
| --- | --- | --- |
| Dialogue `3D3E`–`3D43` | `8009F654` every 0x1C | Call the original version for the first time to teleport the camera to the speaker (`80209DAC`, if the third parameter is non-0, teleport); next time `8008FED4` returns 3 |
| Wait for `3D38` | `800A00F0` | Set count `+0x2E` to 0, the next call will be completed < 0 |
| Close the window and wait for 32 frames `3D47` | `800A013C` | `+0x2E` Set to 0x1F and call to 32 next time |
| Close the window and let one frame `3D4E` | `800A0468` | Poll once again to complete |
| Fade `3D3B` | `8009F948` | Fade engine record 1 (`800FF9E8`): `+C` Current transparency written as `+5` target, `+4` cleared to 0. This is exactly what the last step of `8009AD64` does; the handler then unlocks the input lock itself `8010F6BA` |
| Screen shake `3D36` | `8009F880` | End judgment `8020D4B0` (tactical map) / `801C5138` (world map) Each time a push is called, the same frame is continuously polled |
| Appearance `3D45` | `8009FC04` | Tactical map only: the two 10-frame count is pushed to 9; the appearance animation `8020C524(0)` is pushed one step at a time and polled continuously. The hull and pilot are generated as usual by `8020B154` |
| Unit movement `3D3C` | `800A0360` | Tactical maps only: `8020A788` Only sets the speed (±8 pixels) of the unit sprite each time, and the position is integrated by the frame-by-frame sprite movement `80081BFC`; polling continuously, calling `80081BFC` once before each time. After reaching the grid, `801CBEB8` is written back to the roster coordinates |

"Continuous polling" allows each command to be polled up to 600 times per frame. If it exceeds the limit, the current frame will be given up.

When `8020C524` is called with parameter 1, all units will be placed immediately through `8020BE34`, but the only caller in the original version, `3D45`, only passes 0. This path has never been executed, so it is not used.

## Stop point

Skip ends at the following position and the reader returns to manual:

- Event script ends (`FFFF`);
- Select limb `3D44` (`8009FA94`, the selection page appears as usual);
- Attack selection `3D3D`, level victory settlement `3D4A`, game end `3D4C`, ending `3D71`;
- Switch from the world map to the battlefield `3D4D` (`800A031C`): It only sets `engine+4` to 3. It takes a few frames for the overlay to switch, and the script continues to take down one item during this period. The original version relies on the 10 frames starting with `3D45` to wait until the tactical overlay is installed; compressing it will cause the tactical overlay's `8020B0D4` to be called in the world map overlay and crash (actual measurement). So there is no acceleration after `3D4D`;
- Overlay switching, script substitution, dialogue reset (original stopping point of the reader).

## Verify

- Component test: `make recomp-script-skip-test` ([tests/native_script_skip.cpp](../../tests/native_script_skip.cpp), merged into `recomp-native-check`), covering stop point table, dialogue processing function identification, fields written by each command, non-tactical maps are not accelerated.
- Actual machine: [check_script_skip.py](../../tools/recomp/debug/check_script_skip.py) In the new game (Brad's route), the first dialogue is skipped after reading two pages, and the first sentence of the battlefield is skipped again. World map segment 2 VI stops at `3D4D`, battlefield opening segment (deployment, four `3D3C`, dialogue) 2 VI executes to the end of the script, and no dialogue is displayed twice. `SRW64_SCRIPT_SKIP_TRACE=1` records skipped execution commands one by one; commands executed at original speed always record one line `SRW64_SCRIPT_SKIP wait`.
- State comparison: [check_script_skip_state.py](../../tools/recomp/debug/check_script_skip_state.py) Run two rounds in sequence, press A sentence by sentence in each round to read the opening, skip twice in one round, and go to the tactical map. After our turn is idle, go through the debugging interface `memory.read` Reading rosters, unit instances, pilot instances, plot variables, level fields (stage, turn, map, scene, money), event context, sortie exclusion list, and mothership table: 2026-09-29 The eight regions are byte-for-byte identical (read VI 8222, skip VI 6496). There is no unit under the cursor in the last frame of the two games, and the continuous shooting confirms that it is the original flicker.

## Unmade and known differences

- Other performance commands (`3D32`/`3D33` world map positioning and trajectory, `3D35` blocking scrolling, `3D37` grid special effects, `3D46`/`3D4F` exit and defeat, `3D49` Scripted combat, `3D51` MAP weapons, `3D55` Spiritual performance, `3D50`/`3D5C`/`3D63`/`3D67`/`3D6A`/`3D75` etc.) are still executed at the original speed; the execution is correct, but that section is not fast. Fill in order of occurrence.
- Skipping less running frames will make the two random seeding clocks (`8015DC50`, `80172D0C`) different from reading them, and the random selection of lines, backgrounds, etc. for subsequent battles may be different. There are already similar differences in dialogue fast-forwarding, and the battle results in this game are settled before the show.