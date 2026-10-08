> **Language / Ngôn ngữ:** [English](60fps.en.md) · [Tiếng Việt](60fps.vi.md) · [中文](60fps.md)

# 60 Frame Study

**Status: Pending, not started yet** (2026-10-01 user decision). Start over with the experiment in Section 7.

2026-10-01. Static analysis (main loop disassembly, all overlay generated codes, RT64 and ultramodern source code, host drawing layer), no code changes, no real machine. Anything written as "inferred" or "unverified" must be confirmed in the test in Section 7.

## 1. Conclusion

1. **Original logic is fixed at 30 frames per second**: every 2 VIs run one frame of game logic and submit a display list. The interval value is only written once in the entire program at startup, and there is no scenario to change it.
2. **Changing the logic to 60 is not feasible**: All waiting, animation stepping, and scrolling are counted by frames. Changing the interval to 1 will double the speed of the entire game. (Sub-product: this is a ready-made global 2x speed switch, see §2.1.)
3. **What is feasible is to display interpolated frames**: the logic is still 30, RT64 draws a few more frames between two frames according to the monitor refresh rate. RT64 comes with this capability, and the host currently turns it off (`RefreshRate::Original`).
4. **Frame insertion is only valid for 3D drawing of matrix**. This work is divided into two categories according to scenes:
- There is a high probability that it will be available out of the box: the body and special effects of the battle show (a quadrilateral with MODELVIEW LOAD once per node), 3D ground, world map model, and zoom text of the title and prologue. The host drawing of the HD body diagram and HD model is already reading the interpolation matrix of RT64 and will be activated together.
- Completely motionless: everything TEXRECT - tiles, units, cursors, scrolling for tactical maps, sky layer for battles, backgrounds, avatars, HUD, dialogue. RT64 does not match rectangles.
5. **The tactical map that most wants 60 frames happens to be the type that does not move**. It is necessary to add the "interpolation of numbered rectangles" patch to RT64 (or change the map layer rectangle to an orthogonal quadrilateral). This is the biggest piece of work in the whole thing.
6. The interface (RmlUi page, dialogue bar) drawn by the host itself is rendered and drawn once in the rendering hook; now it is only rendered 30 times per second. When frame interpolation is turned on, the number of presentations will follow the display. The transition animations of these interfaces can reach 60/90/120 without changing.

Suggested order: first add a test switch to the actual machine to see the unboxing effect (half a day) → number the matrix groups according to the node slot number for the battle show/world map/title, and process the mirror cut (a few days) → rectangular interpolation of the tactical map (maximum).

## 2. Original frame rhythm

| Address | Function |
| --- | --- |
| `80080838` | Scheduling threads. Message `0x29A` (VI retrace): Tuning pile `80085F30`, `D_80172D0C`+1, `D_8015DC50`+1, then `80080A14`. `0x29B`/`0x29C` is SP/DP completion, `0x29D` is PreNMI |
| `80080600` | Create a scheduling thread, `osViSetEvent(队列, 0x29A, 回扫数)`; the retrace number is passed in by the caller, and the immediate number is not caught. It is inferred to 1 from the measured 30 frames (inference) |
| `8007F9A0` | Game thread main loop, every time a type 1 message is received, go to `8008163C` (inferred to be a retrace transferred from the scheduling thread) |
| `8008163C` | Read the controller each time and accumulate (`80087A48`, `80087AA4`); **`D_80172D0C < D_8010F0C8` will return **; otherwise, clear the count, count the key edges, and run the frame function of the current scene `D_8015DC7C` |
| `8007FC48` | Power-on initialization, **`D_8010F0C8 = 2`** |

- Search for access to `8010F0C8` in all generated code (`build/recomp/cpu-bound/generated`, resident section plus all overlay): one write (`8007FC64`), one read (`80081660`), no access via base address pointer. So the interval is always 2, the logic is always 30 frames, and it will be lower when frames are dropped.
- Consistent with actual measurements: the title screen is recorded for 8 seconds to obtain 240 frames ([debug-interface.md](../guide/debug-interface.md)); the frame rate reading (`frame_rate.hpp`) counts the display list submitted per second.
- Each VI of the controller reads and ORs into the accumulation words, so the input sampling is 60 Hz and the consumption is 30 Hz ([original-controls.md](../gameplay/original-controls.md)).
- `80085F30` is an empty stub called once by each VI (originally probably for performance management). The host treats it as a "frame boundary" and hangs a series of hooks (`game_hooks.cpp`). In other words, the host already has a 60 Hz beat, but the game logic only changes it every other beat.

### 2.1 Why can’t the logic be changed to 60?

After `D_8010F0C8 = 1`, each VI runs one frame of logic. The waiting in the game ("wait for 20 frames" and "30 frames of delay"), animation steps, scrolling steps, and the 1/8 coefficient of camera approach are all hard-coded by frame. There is no concept of time steps, and the result is a global 2x speed. Halving the step size step by step is equivalent to rewriting all overlays, regardless.

By-product: This is a **global 2x speed** that does not move the VI and the audio clock (inference, not actual). The audio thread sends back the scan message by itself, the music speed remains unchanged, and the sound effect triggering is doubled; the two broadcast clocks are not affected by VI. The previous record that "the host does not have any speed control facilities" refers to the speed multiplier of ultramodern; this spacer is the game's own. If you want to "press and hold fast forward", you can try it from here, it has nothing to do with 60 frames.

## 3. How does the host appear now?

- Ultramodern's VI thread is fixed at 60 Hz (`events.cpp``vi_thread_func`, speed multiplier constant 1), and each VI queues a screen update to the graphics thread.
- The game submits a display list for every 2 VIs → `send_dl` → RT64 workload.
- RT64 `updateScreen` only produces a render (`rt64_state.cpp:1950`) when the VI register or framebuffer contents change, so 30 renders per second.
- `graphics.cpp:399`: `refreshRate = RefreshRate::Original`, target frame rate 0, no frame matching, no frame insertion.
- The host's rendering hook (`capture_frame`) is adjusted once for each rendering: black on both sides, dialogue bar, RmlUi (`context->Update()`/`Render()`). So the host interface is now also 30fps.

## 4. How does RT64 frame insertion work?

The source code is in `build/recomp/upstream/RT64` (commit 4337374 plus this project patch).

- **Switch**: `RefreshRate::Display` (takes the swap chain refresh rate, Metal via `CocoaWindow::getRefreshRate`) or `Manual` (`refreshRateTarget`).
- **Original frame rate**: `VIHistory::logicalRateFromFactors` - Several VIs have been separated between the last few screen changes. If they are all the same, 60÷ interval is given, otherwise 0 (no insertion). When the game is stable, it is 30; when reading disks or switching scenes, it will temporarily return to unplugged, and will automatically recover after stabilization. Can be nailed with the extension instruction `gEXSetRefreshRate(30)`.
- **Premise**: The frame buffer presented must be the color map drawn by this workload (`interpolationEnabled`, check VI history in the default SkipBuffering mode). This work is an ordinary double buffering, which is presumed to be true but has not been verified.
- **Each game frame is rendered N times** (N=target ÷ original, 60 Hz is 2, 90 Hz is 3, 120 Hz is 4), and each time the transformation of "previous frame → current frame" is interpolated with different weights, the entire frame is redrawn, not cheap reprojection. GPU load is calculated as N times.
- **Match** (`rt64_game_frame.cpp`):
- Only look at the drawing under two types of projection: perspective and orthogonal projection; **Rectangular projection (TEXRECT/FILLRECT) does not participate** (the switch of `GameFrame::set` is skipped directly).
- When there is no explicit number (`G_EX_ID_AUTO`): First bucket the hash according to the draw call. The hash only contains the synthesizer, OtherMode, geometry mode, triangle number, **excluding textures**; in the bucket, calculate the difference in position, orientation, and screen position for all "current matrix × previous frame matrix", and greedily match them from small to large.
- When there is an explicit number (`gEXMatrixGroup…`), it is paired according to the number. Interpolation or skipping can be specified component by component, and vertex interpolation and UV interpolation can be turned on.
- View/projection matrix, texture scrolling (tile's uls/ult), LookAt also interpolate.
- **Something not matched** Draw directly according to the current frame, which is still 30 frames. There will be no error, but it is not smooth. **Mismatching** will cause problems (two objects slide towards each other's position).
- Delay: The inserted frame goes before the current frame, and the current frame itself is displayed later. At 60 Hz, it is about half a game frame longer (17 ms), and it does not matter in the game.

## 5. Can each scene be inserted?

| Scene | Moving things | Drawing methods | Unboxing expectations | Things to make up |
| --- | --- | --- | --- | --- |
| Combat performance | Body, weapon effects, explosion, cut-in | Mode 0xE/0xF/0x10: `8008B324` Each node `DA380003` MODELVIEW LOAD, one for each part G_QUAD ([battle-animation-rendering.md](battle-animation-rendering.md) §3) | Active. However, the quadrilateral hashes of all parts are the same, and they are matched only by distance: dense bullets, tail flames, and clusters of explosions are easy to mismatch (the same source of known issues in Mischief Makers recompilation) | Explicitly number the matrix group by (slot, sub); skip interpolation at the frame when creating a node, changing scene resources, or cutting the lens |
| Battle show | Camera | guLookAtReflect view matrix | Active | Skip when the camera cuts hard |
| Combat performance | 3D ground, HD city and water surface | Model node; HD walking `native_marker.cpp` | Active; host drawing read `lerpWorldTransforms`/`modViewProjTransforms` | The time parameter of the water surface shader is advanced by the rendering frame (current status is not checked) |
| Combat performance | HD overall picture of the aircraft | `native_sprite.cpp` Use the matrix drawn this time | Same as above, follow the movement | — |
| Combat performance | Sky, scrolling layer | Mode 2, 32×32 block TEXRECT | **Unmoving** | It cannot be seen when the sky scrolls slowly; when the camera moves quickly, it will be out of sync with the 60-frame body, please watch again then |
| Combat performance | Mode 0xB screen coordinates actors, HUD, damage numbers | TEXRECT | Don't move | Don't care |
| Combat performance | Sprite frame changing, palette flashing | Texture changing | Unable to be inserted (the content itself is 30 frames or lower) | There is no solution, and it should not be inserted |
| World map | Ship models, landmarks, tracks, lenses | 3D model plus matrix; HD walking `native_marker.cpp` | Active | Close-up of quadrilaterals and map blocks on both sides of the starry sky to see if there are any seams flickering |
| Title, prologue, chapter title card, ending | Mode 14 scaling/rotating text | Quadrilateral plus matrix | Active | Afterimage (`80083744` frame feedback) reads the real frame buffer, and the inserted frame does not participate in feedback. It is inferred to be harmless and needs to be seen on the real machine |
| Title | Flame, concentrated line | TEXRECT frame change | Unmoving | — |
| **Tactical map** | Map scrolling, cursor, unit movement, range flashing, map special effects | Mode 4/5/6/8/12/13, all TEXRECT; HD map layer is a rectangle drawn by the host according to `view_left` | **The whole screen does not move, still 30 frames** | See §6.2 |
| Host interfaces such as dialogue, inter-scene, pre-war confirmation, settings, etc. | RmlUi transition, text appears word by word | Draw in the presentation hook | Draw every time when the frame insertion is on, and automatically adjust to the monitor frame rate | Press the workload in the hook to check the accounting (§6.3) |
| Interscene/dialogue in original mode | — | TEXRECT | Not moving | It’s basically a static picture, it doesn’t matter |

## 6. Things to do

### 6.1 First gear: matrix scene

1. Set the item "Frame rate: Original 30/Follow the monitor" (leave 30 by default), save `presentation.json`; correspond to `RefreshRate::Original`/`Display`, switch to the existing `updateUserConfig`. Debugging session fixed 30: Screenshot comparison scripts (`check_aspect.py` and other "only animation frames" comparisons) and recordings assume one workload per frame.
2. `srw64_render_node` (`game_hooks.cpp`) has wrapped the drawing of each elf node and obtained (slot, child). For mode 0xE/0xF/0x10 and model nodes, insert `gEXMatrixGroup` (number = slot × 3 + sub + constant) before drawing the node, and then reset. Extended GBI has been prescribed frequently.
3. Skip conditions: The node has a new or changed scene/atlas in this frame (the slot is reused by other actors), the position jump exceeds the threshold, the lens is cut hard, and the performance state machine changes segments. The corresponding frame is given to the group `G_EX_COMPONENT_SKIP`, and the shot is skipped to the view group.
4. Insert `gEXSetRefreshRate(30)` at the beginning of the frame to avoid switching back and forth when reading from the disk.
5. Keep a table that is closed by scene (follow the Mischief Makers approach), and the show with the problem is closed first.
6. Performance: 4×MSAA plus HD layer on the Deck, each frame must be pushed into 16.7 ms (90 Hz OLED is 11.1 ms) to be meaningful; if it cannot be reached, RT64 will not degrade, but will only slow down overall. To measure realistically, limit the target to 60 if necessary.

### 6.2 Second gear: Tactical map

All movements on the map are rectangular translations: scrolling is the same offset for all sprites on the map layer, and the cursor and units are their respective screen coordinates. Two approaches:

- **A. RT64 patch: Numbered rectangular interpolation**. Use the numbered G_NOOP tag in the display list (existing HD hooks are already using this tag) to mark the group number for the following rectangle; RT64 records it in `DrawCall`. When matching frames, match the rectangles of the two frames before and after according to "group number + intra-group serial number". When rendering the interpolation frame, insert the rectangle coordinates (and crop) according to the weight. The rectangle does not use the vertex velocity buffer (that set of `pos − vel × (1 − w)` is only in RSP vertex shading), and must be added separately when the rectangle is converted to screen coordinates. The host side `srw64_render_node` sends labels to the map layer sprites; the host drawing of HD map layers and HD unit icons must get the same interpolated offset. The changes are concentrated on RT64 and are small on the game side, but RT64 patches need to keep up with upstream maintenance.
- **B. On the game side, change the rectangle of the map layer to a quadrilateral under orthogonal projection**. Each sprite has a matrix, and RT64's ready-made matrix interpolation can be used. Do not change RT64, but rewrite the instructions issued by several renderers such as `80095974`, `800945D4`, `80096CD8`, etc. Widescreen has already applied `gEXSetRectAlign`/cropping to these drawings, and HD texture replacement is identified by rectangular hash, which is very involved.

Tendency A. No matter which one is used, the map block frame-changing animation (water surface, range flashing) and the cursor's own frame animation are not inserted.

There is no amount of map scrolling and how many pixels the cursor moves per frame (`801FFADC` is followed by direct conversion such as "scrolling amount = 32 − cursor x", and the step size depends on the cursor's own movement). They are measured together during the test to determine the visual benefit of 30 → 60.

### 6.3 Points to check on the host layer

- Each workload of the rendering hook will be called N times: the visible bands of `srw64::ui::presented()`/`in_flight`, `names::cover_presented(workload)`, `dialogue::gpu_draw(workload)`, `wide_map` are counted according to the workload number. Repeated calls should be idempotent and confirmed one by one.
- `record.start` reads back one frame per rendering, and the number of frames will be doubled; `srw64_screenshot` may intercept interpolated frames.
- The frame rate reading now counts the display list (constantly 30). You need to add a rendering count to see whether the frame insertion is effective.
- `get_display_framerate()` Two deadlocks of 60 (`host.cpp:106`, `graphics.cpp:524`), ultramodern uses it for other beats, don't touch it yet.
- Audio is completely unaffected (logic and VI tempo remain unchanged).

## 7. Test plan (half a day, requires construction and actual machine)

1. `graphics.cpp` plus `SRW64_REFRESH_RATE=display|<数字>`, corresponding to `Display`/`Manual`; frame rate reading plus rendering count.
2. Watch and record in sequence: title (zoom text, flames), prologue, world map, a battle show with camera movement and barrage, tactical map scrolling and unit movement, dialogue, and inter-game RmlUi page.
3. Record: whether the rendering frame rate reaches 60; what things have moved; examples of mismatching; whether the host layer is flickering, misaligned, or duplicated; whether `logicalRateFromFactors` is stable at 30; GPU time per frame on Mac.
4. Measure the number of pixels per frame for tactical map scrolling, cursor, and unit movement.
5. Based on this, decide the numbering and skipping rules of the first gear, and whether to go A or B in the second gear.

## 8. Not verified

- The retrace number of `osViSetEvent` (reversely estimated to be 1 based on the actual measured 30 frames).
- The buffering method of this game meets the `interpolationEnabled` condition of RT64.
- The effect of afterimage (frame feedback) and frame interpolation coexisting.
- Automatically match actual mismatch rates in combat performances.
- The value of the swap chain refresh rate under Deck (Vulkan), and the performance when gamescope frames are limited.
- Does the 2x speedup of `D_8010F0C8 = 1` have any non-logical side effects (shows whether the list buffer is enough for each VI).