> **Language / Ngôn ngữ:** [English](native-enhancements-plan.en.md) · [Tiếng Việt](native-enhancements-plan.vi.md) · [中文](native-enhancements-plan.md)

# SRW64 native enhancement implementation plan

2026-09-12 Planning update: Subsequent priorities and launch boundaries are subject to [MOD Product Roadmap](mod-roadmap.md).
Safe node storage, multi-slots and backup are now included in the first release; the description of the "five directions" and non-single archive management below are within the scope of that time.
This article retains the early technical choices and experimental background and cannot be used to judge whether the tasks in the new roadmap have been completed.
The current MOD scope is only the built-in function modules maintained by the project; the following ideas about external package access are temporarily suspended and will not be used as a first-run dependency.

Date: 2026-09-09. T0 has completed the text rendering prototype of the fixed scene system; subsequently, real-time standard dialogue, font size and paging, review, plot speed and window scaling have been integrated. For the latest implementation scope and operation evidence, see [Real-time Apple UI](../native/native-dialogue-ui.md). This article retains the overall implementation plan; the full process, branches and real display DPI combinations still need to be verified item by item.

Users selected five directions: Chinese text system, battle rhythm control, tactical information panel, wide screen and art improvement, linkage and content Mod. Detailed plans and priorities will be delivered in this round; text rendering will give priority to macOS system text technology. The correctness of existing archives and reads will continue to be the acceptance condition at each stage, and archive management product functions will not be separately included in the five scopes.

## 1. Implementation sequence and delivery boundaries

| Sequence | Phases | Deliverables | Dependencies and relative difficulty |
| --- | --- | --- | --- |
| 1 | T0: System text quality verification | Core Text / Core Graphics generate text and synthesize it in the final picture of the real RT64 scene; verify the font size and pixel density | Medium; first prove that the rendering access and color are correct |
| 2 | T1: Real-time dialogue recognition | Runtime logging with text ID, speaker, show progress, and control events | Medium to high; requires recognition of interpreter and scene state |
| 3 | T2: Complete dialogue system | The heroine's first episode has adjustable font size, automatic line wrapping/pagination, complete translation, dialogue playback | High; depends on T0/T1, the scope is limited to dialogue first |
| 4 | B1: Combat rhythm | Specify the acceleration of the combat performance; then expand the enemy's movement and settlement wait | Medium to high; first locate the boundary between performance and logic |
| 5 | U1: Information panel and W1: Widescreen container | 4:3 Display current unit/weapon information next to the game area, sharing native text backend | Medium to high; complete field and selection state mapping first |
| 6 | B2 / W2 | Quick battle settlement; expand the actual map field of view, scene-by-scene widescreen and improve art | High; advance after verification of combat status and drawing range respectively |
| 7 | M1 / M2 | Data Mod package; Link Battler compatible special project | Medium to high data package, high protocol compatibility; linkage survey can be carried out in advance, but there are additional thresholds for implementation |

The text system was delivered first; combat speed-up followed; information panels and widescreen containers were designed together. Complete quick settlement, expanded actual map field of view and linkage are left until the relevant runtime boundaries are clarified. The above is the work sequence and relative difficulty. It has not been calibrated with an end-to-end prototype and cannot be converted into a reliable calendar construction period.

"Complete translation" in the text system acceptance means that the provided translation will not be truncated or forcibly shortened due to the capacity of the original frame. The translation, review and route coverage of the whole game are content work and need to be paid separately; the existing 153 Chinese test drafts do not mean that they are fully completed. For the text size, see [Original Data Directory](../data/original-data-catalog.md).

## 2. Current engineering foundation and actual gap

| Checked entries | What can be reused | What still needs to be completed |
| --- | --- | --- |
| [`catalog.py`](../../src/srw64_native/catalog.py), [`text.py`](../../src/srw64_rom/text.py) | Stable table/text ID, translation overlay, original control unit | Unicode runtime paragraph model, mapping of original control position to translation fragment |
| `resident_func_8008C510` of [`host.cpp`](../../src/host/host.cpp) | Text descriptor reading interception; there is a Chinese default name virtual record | Whether the current reading belongs to the displayed dialogue, speaker, verbatim/pause/confirmation status |
| `resident_func_8007F704` of the same file | ROM reading, overlay identity verification and loading notification | Clear the old state when switching text scenes to prevent the same address overlay from being misidentified |
| `dialogue_layout.hpp` (deleted on 2026-09-24) | Partial glyph drawing of the opening dialogue and name page has been recognized | Currently only the position is changed; automatic line wrapping is not possible, and it is not a complete text interpreter |
| [`graphics.cpp`](../../src/host/graphics.cpp) | RT64 final frame draw hook, Metal, GPU readback after completion, texture replacement | Final resolution text synthesis, unified DPI processing, reliable suppression of original glyphs |
| [`audio_timing.hpp`](../../src/host/audio_timing.hpp) | Already have audio queue feedback and duration limit | Currently assuming 60 VI; any solution to change the simulation speed needs to be re-validated |
| `auto_counter.py` (removed in 5b997c7 on 2026-10-01) | Bounded existing counter menu auto-confirmation probe | It uses a reviewed screenshot template and does not provide a combat state machine or unit data model |
| `host.cpp::get_device` and `ultramodern/input.hpp` of the fixed runtime library | Current controller input | The host returns `Pak::None`; `TransferPak` of the runtime library is still an annotation and requires special adaptation |

The scope of evidence for the current JP episode 1 clearance save, native language and high-definition configuration, and single-frame font experiment are shown in [recomp progress](recomp-progress.md), [native content configuration](../native/native-content-foundation.md), and font experiment (probe 2026-09-24 deleted). The three cannot replace each other.

## 3. Chinese text system: using OS native text rendering

> No longer used from 2026-09: Game text will be drawn by the cross-platform FreeType+HarfBuzz+ICU engine and packaged HarmonyOS Sans, see [Chinese, Japanese and English cross-platform text and game dialogue](../native/portable-text.md). This section retains the current plan and rationale.

### 3.1 Decision-making and screen effects

macOS preferred **Core Text typesetting + Core Graphics rasterization + Metal final screen composition**. This actually calls the system text technology to handle font metrics, glyph selection, layout, and drawing. Apple’s explanation of the relationship between the two and font fallback can be found in [Core Text Overview](https://developer.apple.com/library/archive/documentation/StringsTextFonts/Conceptual/CoreText_Programming/Overview/Overview.html).

The font source is independent of the renderer: you can choose system Chinese fonts or use HarmonyOS Sans SC through the same system rendering backend. The first version provides two candidates, "System Chinese" and the current font, which are compared according to the same text, size, font weight and background to determine the default value. Follows the system's font selection using the language-aware API, writing evidence of the actual resolved fonts and fallback fonts, without assuming a certain font name exists on all machines.

The text is generated according to the pixel density of the final drawable, and the font size is expressed in interface logical units; the game's internal rendering magnification is separate from the text size. Relayout/rasterization when window is resized or moved across monitors. Desktop text quality is targeted; system version, font version, anti-aliasing, and compositing settings affect pixels and are not guaranteed to be pixel-by-pixel identical to any macOS app.

Core Text provides in-box typesetting and automatic line breaking; the game's paging, verbatim display, history and script synchronization are still implemented by this project. Chinese punctuation prohibitions, consecutive ellipsis, mixed layout and special symbols must be verified through samples, and calling the typesetting API cannot be regarded as acceptance. Refer to [Apple Text Layout Operations](https://developer.apple.com/library/archive/documentation/StringsTextFonts/Conceptual/CoreText_Programming/LayoutOperations/LayoutOperations.html).

### 3.2 Suggested structure

```text
原游戏对白解释器 / 场景与文本 ID
              ↓
DialogueSnapshot：完整片段、说话者、控制边界、显示进度、事件序号
              ↓
翻译覆盖层 + 动态姓名 + 专用符号
              ↓
Core Text：字形选择、度量、行布局、分页所需范围
              ↓
Core Graphics：按最终像素密度绘制可见字形
              ↓
Metal：游戏画面完成后合成 → GPU 完成后截图
              ↓
已显示片段进入对话历史
```

Shared logic is in C++; the macOS backend is put into a separate `.mm` file and built against CoreText, CoreGraphics, and the required system frameworks. The interface is defined around layout inputs, glyph cluster ranges, and composable pixel outputs, without propagating macOS types to the game interpreter. Other platform backends are reserved for subsequent porting points, and this round does not promise consistent font pixels across platforms.

The layout is initially cached by dialogue segment and only reflows when text, font, weight, width or DPI change. The word-by-word display uses the arranged glyph positions and updates the drawing according to the visible range; first measure the CPU rasterization and texture upload time, and then decide whether to introduce a more complex glyph atlas.

### 3.3 T0: First prove that the system rendering can correctly enter the game screen

1. Use real-life scene snapshots of documented identities, along with canned samples of Chinese, Japanese, Latin letters, and numbers; include quotation marks, brackets, ellipses, and longer names.
2. Use Core Text / Core Graphics to generate transparent background text; specify color space, premultiplied alpha, and texel format explicitly.
3. Draw hook synthesizes text in the final frame. Fixed `rt64_present_queue.cpp` for RT64 checked: hook is located after `viRenderer->render` but before rendering is submitted; existing GPU screenshots also use this entry. Adding new compositions should be done before taking screenshots blit.
4. First use an independent area to compare the quality of glyphs, and then only replace the original glyphs that have been clearly assigned. Frame lines, backgrounds, avatars, cursors and special icons must be retained; similar textures cannot be generally hidden.
5. Verify three font sizes, narrow/wide text boxes, window scaling, and available 1×/2× pixel density; record the window logical size and actual drawable size. Real monitor combinations that are not connected are reserved for testing.

T0 pass condition: no double text, color cast, dark edges, cropping or extra scaling blur; final GPU image contains new text. Output includes reproducible commands, scene/font identities, layout parameters, and GPU frames. This stage only proves rendering and does not claim that the real-time dialogue system is completed.

### 3.4 T1: Dialogue semantics and event recognition

The text reading entry is only used to associate ID and data, and each ROM read cannot be recorded as a historical dialogue. It is necessary to locate the actual display function and text interpreter, and identify the speaker, current fragment, display position, waiting for confirmation, and end status of each of the two dialog boxes.

The game thread issues immutable snapshots at explicit times; the rendering thread uses the snapshot associated with that display task. The event carries a monotonic sequence number and scene generation to prevent repeated drawing from generating duplicate logs, or the text of the previous scene appearing after overlay switching. There is a boundary check between threads, and the rendering thread is prohibited from modifying the game's text pointer at will.

First, keep the original screen unchanged, and collect paths such as female super type name confirmation, opening double-frame dialogue, map dialogue, and post-war dialogue. Use actual pictures and control events to prove that the same text can appear multiple times, and each occurrence only generates a corresponding set of display events.

### 3.5 T2: Font size, complete translation, pagination and history

- **Unicode Text**: Load external translations by existing stable ID; dynamic names retain insertion semantics. Special symbols that have not been recognized yet retain explicit placeholder/original image capabilities and are not deleted silently. The translation content can be advanced paragraph by paragraph and is not restricted by the ROM font capacity.
- **Control Flags**: Keep the original sequence of `END=FFFF`, `BR=FFFE`, `STOP=FFFD` and special glyphs. The first pass preserves explicit word wrapping; automatic word wrapping only adds presentation layer breakpoints and does not rewrite ROM control flow. The actual wait/push semantics of `STOP` shall be confirmed by T1 runtime evidence.
- **Long translation**: Re-format the text in the corresponding control segment, and add reading pages if necessary. The newly added page first consumes the confirmation input at the host layer, and then delivers the confirmation corresponding to the fragment to the game after the page is read; the next script event cannot be consumed in advance. The specific interception point is determined by T1.
- **Verbatim display**: The length of the translation fragment is independent of the original text; set the speed of displaying words according to glyph clusters, and clarify the mapping of UTF-16 range, Unicode glyph clusters and game tokens. Complete the layout of each page before revealing the content to avoid skipping the entire line every time a word is added.
- **Conversation review**: Save the content that has been presented, the name and speaker at the time, and the sequence number; no new records will be added for repeated frames, and the undisclosed subsequent text will not be displayed in advance. The first version saves a bounded history of the current session, loads files, and creates new segments for new games. Cross-process history recovery is designed separately for archive association.
- **Input and Pause**: The history window consumes its own scroll, confirm and return input. Open only at verified dialogue wait points; no actions are sent to the game during replay. If there is automatic dialogue advancement, a safe scene pause mechanism must be established before the path can be opened.
- **Size and Color**: Font size/line spacing/margins are adjustable. Synchronize with the game's original text color, fade and dialog visibility; these effects must be processed separately during final picture composition to avoid floating text across scenes.

The first delivery scope of T2: the plot dialogue involved in the first episode of the Female Super Series; the name page, tactics menu, weapon menu and baked text in the picture are respectively registered for coverage status. The complete translation of the first episode is checked with branch reviewers as the coverage is run. Full coverage cannot be declared based solely on the continuous range of IDs.

Acceptance coverage: long translation, name insertion, double dialog box, explicit pause, cross-page, history switch, missing word fallback, font size switching, window/DPI change, scene switching and file reading. Execute the new game to save after the battle, and continue loading in the new process; compare the corresponding game state and event sequence. Static layout testing, single-frame playback and real-time game acceptance are recorded separately.

## 4. Combat rhythm control

**B0 Survey**: Locate attack/counterattack options, damage calculations, resource consumption, animations, kills, experience/funds and return map boundaries through actual engagements; record game status at each stage. It has not yet been proven that there is an original skip entrance that can be directly reused.

**B1 First Edition**: Provides normal/accelerated and press-and-hold temporary acceleration for a verified performance path. Prioritize review of show waits and animation stepping; if analog clock acceleration is used, the VI, audio feedback, input samples, and thread timing must be processed simultaneously, not just changing `get_display_framerate()`. The speed change strategy used for background music and sound effects is clarified in the prototype and manually auditioned.

Then it covers enemy movement, repeated prompts and settlement waiting; the interactive rhythm is restored when player selection is required or the plot is triggered. Using scene state judgment, absolute VI input scripts and screenshot templates cannot become product state machines.

**B2 Quick Settlement**: After proving that rule execution and performance can be separated, add "normal animation/quick performance/concise result". Each mode must make resource consumption, HP, kills, rewards, triggers and random number advancement consistent with normal mode under the same conditions. You cannot directly set the result variable to pretend that the battle is completed.

Verification starts from the same archive and controllable state; random states can be accurately compared when fixed, otherwise the comparison range is clear. Covering hits, misses, counterattacks, knockdowns, upgrades, triggering plots and returning to the map, the process time and audio queue are measured respectively.

## 5. Tactical information panel and widescreen

**U0 Data Survey**: Establish mapping of the currently selected unit, driver, HP/EN, energy, action status, terrain, weapons, and ammo/consumption fields. The source of each record is overlay/address or function, type, valid conditions, and actual measurement comparison. First, only display information that can be verified with the original menu.

**U1 + W1 first version**: Design the window into the original 4:3 game area plus sidebar. The unit status is displayed when a unit is selected; both sides and selected weapons are displayed after entering attack selection. The sidebar uses the text capabilities of T0/T2, and the font size is linked to the window width; it can be retracted when there is insufficient space. The first version is read-only and does not change selected units or battle decisions.

This step provides a widescreen interface container and does not claim that the map view has been expanded. Panel updates use safe snapshots to check with the actual selected state of the game; unknown or currently invalid fields are explicitly not displayed and cannot be inherited from the old scene cache.

**W2 Actual Map/Battle Widescreen**: Restore map camera, tile submission range, visibility culling, cursor coordinates and edge scrolling respectively; battle also checks background coverage, sprites/special effects, lenses and cropping. Verify 16:9 first, then expand the ratio without stretching the original 4:3 content.

**Art**: Prepare avatars, maps, interfaces and battle material lists based on complete scenes except glyphs; unify style, outline, transparency, color and original image rollback. The RT64 replacement package records the original texture identity and coverage scene. Materials with known source hash ambiguities require context solutions before replacement. Existing AI images can be used as candidates, and new material generation is a subsequent art work.

## 6. Linkage and content Mod

**M1 Data Mod comes first**: First supports translation and texture packages in understood formats, and the manifest records package versions, applicable ROMs, dependencies, conflicts and data hashes. Only then will the unit/weapon values ​​of the verified structure be opened; changing the range and default values ​​can be reviewed, and closing the Mod can restore the basic configuration. Restarting to take effect can be used as the first version boundary, and any hot reloading is not designed for the time being.

Native function patches and data packages are managed separately. The function patch must bind the version, overlay identity and symbol; the patch output method of N64Recomp can be evaluated, and the main body continues to be generated in groups. Each object of the current static library contains multiple functions. The link granularity and repeated definitions need to be verified before overwriting symbols with the same name. You cannot just add `single_file_output=true` and assume that the overwriting mechanism is established.

**M2 Link Battler Special** is divided into two clear product directions:

1. **Compatible with the original linkage process**: Investigate the Pak/GB cartridge calls and protocols used by the game, identify data formats, verification and reading and writing behaviors. The fixed runtime library does not yet have an enabled Transfer Pak implementation, and needs to supplement the interface and compatibility layer. Correct input, no device, incorrect input and duplicate linkages are first checked against independent data copies; if a real GB ROM/archive reference is required, its source and availability are used as implementation dependencies.
2. **Optional content opening Mod**: Clearly state the content and conditions for direct opening, first verify the content tags, resources and subsequent event dependencies, and then implement the rules that can be closed. This mode is independently identified and is not used as evidence of Transfer Pak protocol compatibility.

Level scripts, route rewrites, randomization, and new units require a more complete format and event model, placed behind the M1 data layer and scene coverage expansion.

## 7. First round of development tasks and verification

The first round of development only undertakes feasibility verification of T0/T1. After delivery, the workload of T2 will be refined based on evidence:

1. Add an independent macOS text backend and testing tool to output the system font/current font's three font sizes, long sentences and mixed layout comparison.
2. Access the final frame synthesis and adjust the order of screenshots to complete color, Alpha, DPI and window change checks.
3. Collect text ID, speaker and control progress for a verified opening dialogue scene to form an explicit event model and evidence.
4. Clarify the original glyph suppression range and dialogue advancement interface; only after these two items are established, real-time replacement and paging of T2 will begin.

It is recommended that the new module be placed in `src/host/text/`, with the platform backend, layout/pagination, game event adaptation and historical model as independent boundaries; the specific file name will be determined during development. Configuration falls into `config/recomp/`, real ROM derived data, fonts, pictures, session records remain in `build/`.

Submission is separated by "Text Backend → Scene Recognition → Real-time Paging and Input → History → Run Acceptance"; subsequent battles, panels, widescreen and linkage are independent. When starting code work, re-inventory the work tree. The existing uncommitted content cannot be mixed into the new submission as a whole package.

Static testing focuses on controlling the sequence of events, Unicode boundaries, paging integrity, historical deduplication and scene failure; native testing covers resource life cycle, layout range and thread snapshots. GPU results record font, platform, configuration and scene identity; system upgrades may change glyph pixels and do not make cross-system PNG hash equality a common condition. The inspection required by the warehouse is performed before formal submission, and the runtime evidence is recorded according to the actual completion scope.

When the solution was established, the source code entry and the official interface were checked; then the fixed scene Core Text rendering verification of T0 was implemented according to user requirements. This experiment used an independent graphics replay target and did not start a new game session or change the save file; the Core Text probe and verification records were deleted on 2026-09-24.