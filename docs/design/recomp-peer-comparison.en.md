> **Language / Ngôn ngữ:** [English](recomp-peer-comparison.en.md) · [Tiếng Việt](recomp-peer-comparison.vi.md) · [中文](recomp-peer-comparison.md)

# Similar N64 recomp project and SRW64 enhancement feasibility

Verification date: 2026-09-10.

This time, we checked the open source codes of four game projects and five Harvest Story Mods, and compared them with the release notes and the current host implementation of SRW64. External projects are not compiled or run on this machine; "Source code has been implemented" and "Project Party Release/Verification" are described respectively. The current branch may contain modifications that have not yet entered the release version. The operation basis of SRW64 follows the existing acceptance records. There is no new game operation or modification of game implementation this time.

Conclusion: Mature directions that can be learned focus on native settings and Mods, 2D motion interpolation, scene widescreen, status information and resource editing. SRW64 already has native Chinese dialogue, partial high-definition textures, and independent GPU model prototypes. The next step can be to integrate them into a configurable version, and then expand the information sidebar, battle rhythm, and scene screens. Code from external projects cannot directly replace SRW64's resource, object and script mapping work.

## 1. Verified source code version

| Project | Verification Submission | Scope |
| --- | --- | --- |
| [Harvest Moon 64 Recompiled](https://github.com/HarvestMoon64Recomp/HarvestMoon64Recomp) | `399a4f2b82a8b8dde4bb033e81f8a9b41d796a32` | Map/Sprite Interpolation, Widescreen, Launcher and Mod Interfaces |
| [Trouble Makers](https://github.com/ThiagoLira/trouble-makers-pc-recomp) | `765b179c6f4bfbbb65dc7b371035798ca573202b` | Widescreen, scene rewind, fast forward, known display issues; corresponds to v0.8.2 pre-release |
| [Dr. Mario 64 Recomp Plus](https://github.com/theboy181/drmario64_recomp_plus) | `af91e3bf56b1ffc329ff4327fdc2380515463de7` | Capsule drawing patch and public function description |
| [Paper Mario ReCut](https://github.com/SMCGames/Paper-Mario-ReCut) | `098be0a501eecd5bb894a47964061d05eeedc3a2` | Texture export, replacement hot update, atlas editor |
| [HM64 Stats Display](https://github.com/SrBananaMan/HarvestMoon64StatsDisplayMod) | `2d4b700434002a55611d4bf2e075c0f6301f9db8` | Game field reading, paging status UI, refresh callback |
| [HM64 Enhanced](https://github.com/HarvestMoon64Recomp/HarvestMoon64EnhancedMod) | `b13995f5662fa5068958f3361c5136a8e67e297f` | Text speed, music continuation, map loading optimization |
| [HM64 Custom Audio](https://github.com/harvestwhisperer/HarvestMoon64RecompAudioMod) | `2c5ad56aaff0239a09d76f464a10545cfb2ef3b2` | External sequence files, track mapping and audio call patches |
| [HM64 FOV Config](https://github.com/SrBananaMan/HarvestMoon64FOVConfigMod) | `3ff901b4f916acf596f73deed58727d4edad80bd` | Orthogonal viewport scaling and UI size compensation |
| [HM64 Clock Speed](https://github.com/SrBananaMan/HarvestMoon64ClockSpeedMod) | `73e8bd781807b5411d79f354162464b47cb6447f` | In-game clock step magnification |

## 2. What exactly did they do?

### Harvest Moon 64: Mixed Scenarios and Native Extensions

- **Interpolation has object identity and classification strategies. ** The sprite corresponds to the inter-frame object through the matrix group ID; interpolation is prohibited for some backgrounds. Map construction tries to keep the order of plots stable; when there is a one-time change in the topology or map area, the vertex/map interpolation is skipped and the overall transformation interpolation is retained. Vertices with the same number in two frames cannot be automatically regarded as the same object. [Elf implementation](https://github.com/HarvestMoon64Recomp/HarvestMoon64Recomp/blob/399a4f2b82a8b8dde4bb033e81f8a9b41d796a32/patches/sprites.c) · [Map construction](https://github.com/HarvestMoon64Recomp/HarvestMoon64Recomp/blob/399a4f2b82a8b8dde4bb033e81f8a9b41d796a32/patches/culling.c) · [Interpolation strategy](https://github.com/HarvestMoon64Recomp/HarvestMoon64Recomp/blob/399a4f2b82a8b8dde4bb033e81f8a9b41d796a32/patches/patches.h)
- **Widescreen requires expanding the original game submission scope. ** The current map patch cancels tile visibility culling and expands the double-buffered display list and vertex capacity; there is also a 2D background expansion marker. The release notes for v1.2.0/1.2.1 also separately fix the interpolation of objects such as rain and snow ranges, tutorial background tiles, and NPCs. [Release Record](https://github.com/HarvestMoon64Recomp/HarvestMoon64Recomp/releases) · [2D Widescreen Category](https://github.com/HarvestMoon64Recomp/HarvestMoon64Recomp/blob/399a4f2b82a8b8dde4bb033e81f8a9b41d796a32/patches/widescreen.c)
- **Settings and Mods are part of the product. ** The main program is connected to RecompUI and registers UI export, texture package start and stop, and update callbacks; the game loop provides UI callback execution timing. [Startup and Mod Registration](https://github.com/HarvestMoon64Recomp/HarvestMoon64Recomp/blob/399a4f2b82a8b8dde4bb033e81f8a9b41d796a32/src/main/main.cpp)

Its independent Mod provides examples more suitable for SRW64 to learn from:

| Mod | Actual behavior in source code | Inspiration for SRW64 |
| --- | --- | --- |
| [Stats Display](https://github.com/SrBananaMan/HarvestMoon64StatsDisplayMod/blob/2d4b700434002a55611d4bf2e075c0f6301f9db8/src/stats_display.c) | Read physical strength, time, funds, character favorability, progress, etc. from the game status; refresh the paging UI at intervals in the game callback | HP/EN, strength, action status, terrain and weapon sidebar of the selected unit |
| [FOV Config](https://github.com/SrBananaMan/HarvestMoon64FOVConfigMod/blob/3ff901b4f916acf596f73deed58727d4edad80bd/src/fov_config.c) | Modify the left, right, upper and lower orthogonal boundaries of the camera, while compensating for UI nodes that do not change with the scene | Separate map scaling from the UI; SRW64 camera, tile range and cursor relationships need to be restored first |
| [Enhanced text configuration](https://github.com/HarvestMoon64Recomp/HarvestMoon64EnhancedMod/blob/b13995f5662fa5068958f3361c5136a8e67e297f/src/message_box.c) | Change text appearance, scrolling speed and text sound effect settings | Our standard dialogue already has adjustable speed, paging and playback, but it mainly lacks unified settings and more interface coverage |
| [Enhanced Map Optimization](https://github.com/HarvestMoon64Recomp/HarvestMoon64EnhancedMod/blob/b13995f5662fa5068958f3361c5136a8e67e297f/src/map_loading.c) | Reduce repeated reconstruction during batch loading, cache reused resources and terrain heights | Use measurements to find the specific repetitive work of loading pauses, and then optimize the corresponding functions |
| [Clock Speed](https://github.com/SrBananaMan/HarvestMoon64ClockSpeedMod/blob/73e8bd781807b5411d79f354162464b47cb6447f/src/clock_speed.c) | Only adjusts the step multiplier of in-game time | The speed of specific processes can be controlled separately; this is not proof of full game speed or battle skipping |
| [Custom Audio](https://github.com/harvestwhisperer/HarvestMoon64RecompAudioMod/blob/2c5ad56aaff0239a09d76f464a10545cfb2ef3b2/src/custom_music.c) | Load `.seq` from the host, map the map/plot music, and return it to the original audio engine for playback; the tool converts MIDI into seq | Please refer to the route that supports replacing music by track ID; direct playback of OGG/FLAC requires the establishment of a separate host playback and synchronization path |

### Mischief Makers: Scene-by-scene widescreen, interpolation and fast-forward

Code and engineering documents show that the project expands the drawing, cropping and generation/disappearance range of sprites/background tiles and some objects; retains 4:3 for cutscenes with a fixed canvas, and restores widescreen after stably entering the operation scene. [Rendering Analysis](https://github.com/ThiagoLira/trouble-makers-pc-recomp/blob/765b179c6f4bfbbb65dc7b371035798ca573202b/docs/README.md)

High frame rates are based on display interpolation of native 60 Hz game frames. Quickly changed sprites such as missile tail flames will have mismatches. The project will turn off interpolation for specific scenes and level selection interfaces, and restore user selections after leaving. v0.8.2 also made a separate panorama extension for the snow mountain background; the README's "no stretching" description of ordinary scrolling scenes cannot be extrapolated to all backgrounds. [Scenario Strategy](https://github.com/ThiagoLira/trouble-makers-pc-recomp/blob/765b179c6f4bfbbb65dc7b371035798ca573202b/src/game/presentation.h) · [v0.8.2](https://github.com/ThiagoLira/trouble-makers-pc-recomp/releases/tag/v0.8.2)

The 3x fast forward of holding down Tab is implemented through the host runtime speed multiplier, modifying the VI/timing rate. It's not a "just speed up the combat show, keep the music normal" feature; timing continuity, audio queues, and input boundaries still need to be verified before moving to SRW64. [Quick entry](https://github.com/ThiagoLira/trouble-makers-pc-recomp/blob/765b179c6f4bfbbb65dc7b371035798ca573202b/src/game/main.cpp) · [Runtime library patch](https://github.com/ThiagoLira/trouble-makers-pc-recomp/blob/765b179c6f4bfbbb65dc7b371035798ca573202b/patches/N64ModernRuntime/0004-Add-ultramodern-set_speed_multiplier-for-host-fast-f.patch)

The project explicitly addresses two types of issues: multi-part characters may be blurry or misaligned during interpolation, and sprite/terrain strip seams are not automatically eliminated by anti-aliasing. Full process verification is still pending. [Known Issues](https://github.com/ThiagoLira/trouble-makers-pc-recomp/blob/765b179c6f4bfbbb65dc7b371035798ca573202b/KNOWN_ISSUES.md)

### Dr. Mario 64: Partial 2D rendering transformation

The specific implementation of "capsules are switched to GPU drawing" is to replace the original CPU drawing function, load the CI4 capsule atlas, load the palette for the left and right half, and issue the texture rectangle command to continue drawing by RT64. It proves that local draw functions can be overridden and does not imply that standalone high-poly or modern PBR materials have been used. [Capsule patch](https://github.com/theboy181/drmario64_recomp_plus/blob/af91e3bf56b1ffc329ff4327fdc2380515463de7/patches/theboy181_workspace.c)

The README also lists high frame rate interpolation, four-player controllers, and CRT effects, while noting that there are very few overall tests. This time, no other source files inherited by the template will be considered as completed game functions. [Project Description](https://github.com/theboy181/drmario64_recomp_plus/blob/af91e3bf56b1ffc329ff4327fdc2380515463de7/README.md)

### Paper Mario ReCut: Replace materials into an editing process

Paper Atlas Tool supports dragging and dropping the exported fragmented PNGs into an atlas, saving the layout, sending it to an external image editor for modification, and then switching back to the replacement directory according to the original layout. The game rendering context checks the latest modification time of the replacement directory every 750 ms and reloads after changes. [Atlas tool](https://github.com/SMCGames/Paper-Mario-ReCut/blob/098be0a501eecd5bb894a47964061d05eeedc3a2/tools/PaperAtlasTool/README.md) · [Atlas editing code](https://github.com/SMCGames/Paper-Mario-ReCut/blob/098be0a501eecd5bb894a47964061d05eeedc3a2/tools/PaperAtlasTool/MainForm.cs) · [Replacement loading](https://github.com/SMCGames/Paper-Mario-ReCut/blob/098be0a501eecd5bb894a47964061d05eeedc3a2/src/paper_rt64_context.cpp)

SRW64 already has map puzzle construction, avatar slicing and resource viewer, which is suitable for organizing existing scripts into the editing process of "view usage scenarios → export complete picture → import modifications → automatic slicing → in-game comparison". The first version of the hot update can be limited to development mode, and the official package will continue to retain identity verification and clear versions.

## 3. Compare SRW64: What can be done

The following difficulty levels are engineering judgments based on known entrances and are not construction time commitments.

| Objectives | Current Basics | Work to be Done | Relative Difficulty |
| --- | --- | --- | --- |
| Unified enhanced settings | There are high-definition, native dialogue, and model experiment switches, but they are in different trial configurations | Merge compatible configurations, add settings panel, persistence options, and entity controller mapping; joint verification | Medium |
| Material editing and package management | RT64 texture replacement, map/avatar construction script, 3D viewer | Whole image import and export, slice mapping, scene association, A/B switch, package dependency and conflict management | Medium |
| Tactical information sidebar | Core Text/Metal UI and game running hooks are present | Restore currently selected units and fields, publish consistent snapshot; check with original menu | Medium to High |
| Battle performance 2×/4× | Dialogue quick reading and opening skipping are available, and the complete battle process can be run | Position the performance step, waiting and settlement boundaries; return to normal speed when selecting; check HP/EN, random advancement, rewards, plot and sound | Medium to High |
| Smooth movement of maps, lenses and some sprites | RT64 has been connected; the original refresh mode is still used | Stable object identity, front and rear frame transformation, scene invalidation, separate interpolation strategy; the native model must also use the same rendering moment | High |
| Actual 16:9 field of view | Currently centered 4:3 | Map/battle expanded projection, tile submission, cropping, background and effects respectively; cursor aligned with selection | High |
| High-definition combat background and modern model materials | 5600 independent GPU mesh, lighting, occlusion prototype verified | Find the resources and life cycle of the specific combat background; make models/materials; verify sprite overlay, camera and various effects | Single scene medium to high; general system high |
| Optional music package | Original audio link can be run | Track ID, switch/loop/fade semantics; select sequence to replace or add host player | Medium to High |

**Interpolation can make the displacement, scaling, and rotation of the entire body map smoother; when the body switches from one action map to the next, the arm posture in the middle will not be generated out of thin air. ** Supplementing action frames, redoing pieced animation, or changing to 3D skeletal animation are further materials and animation system work.

For native 3D, the codes currently available for reference in several projects are mainly RT64 adaptation, rectangle/sprite drawing and resource flow; this time, no universal high-poly/PBR replacement solution that can be directly moved into SRW64 was found. The 5600's host model path still needs to be extended with our own scene semantics.

## 4. Existing implementation verification and recommended sequence

- [`src/host/graphics.cpp`](../../src/host/graphics.cpp) The current explicit settings are `AspectRatio::Original`, `RefreshRate::Original`; RT64's own widescreen/interpolation capabilities cannot be regarded as SRW64's adaptation.
- [`play_native.py`](../../tools/recomp/run/play_native.py) Passed `--profile` to unify language, HD art, and native models; current acceptance is in [Content Architecture](../native/native-content-foundation.md).
- [Real-time dialogue](../native/native-dialogue-ui.md) Unicode typesetting, paging, font size, review and reading speed have been implemented; there are still gaps in full UI coverage and physical handles.
- [Native 5600](../native/native-model-replacement.md) There is evidence of actual gameplay and controlled occlusion; currently only Metal raster, without transparent refraction, dynamic projection and cross-backend implementation.
- Tactical information, battle rhythm and widescreen dependencies follow [Overall Implementation Plan](native-enhancements-plan.md); this report supplements external cases and does not change the plan item as completed.

It is recommended to proceed based on the acceptable results:

1. **Integrate existing enhancements and settings. ** The same version can switch on and off the Chinese UI, HD packages and model replacement, maintain clear save configurations, and complete joint verification from the opening to the first level and save and read files.
2. ** Deliver practical enhanced samples. ** First create a snapshot of the status of the selected unit and create an information sidebar next to the 4:3 game area; combat speed is verified as an independent function. The material editing process can be gradually improved without changing the gameplay.
3. **Delivery screen enhancement samples. **Choose an actual combat background to make modern models/materials; try local interpolation for maps or lenses first, and then expand them category by category. The real widescreen is accepted according to the scene, and the plot with fixed composition retains the corresponding presentation strategy.

This new content is only a research record; no other projects have been started, external implementations have not been copied into SRW64, and existing experiments or archives have not been changed.