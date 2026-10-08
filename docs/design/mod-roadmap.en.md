> **Language / Ngôn ngữ:** [English](mod-roadmap.en.md) · [Tiếng Việt](mod-roadmap.vi.md) · [中文](mod-roadmap.md)

# Built-in MOD roadmap: basic experience, multi-language and Original / HD

Date: 2026-09-12; 2026-09-16 Added bug source registration and EW replacement preview requirements. This document stipulates the scope, priority and acceptance thresholds for subsequent delivery; except for the capabilities explicitly listed in the "Current Starting Point", these are plans.

> **2026-09-18 Current priority**: At this stage, we will first explore the functions and gameplay improvements that recompilation can bring (native interface, reading control, original defect correction, optional gameplay and difficulty rules and verification tools). **Full text translation content and HD art production are delayed** and will not begin until some time after this stage. "Multi-lingual" and "Original / HD" in M1 below refer to platform capabilities (language hot switching, native text, item-by-item rollback image replacement), and do not include the production of translated text and art resources; the existing Chinese and English drafts and HD materials in the warehouse are only used to verify these processes.

> **2026-10-03**: The external MOD package (only data) has been included in the plan. For format, dependencies and classification, see [MOD package](mod-packages.md); the scope limit in the following paragraph shall be subject to that copy.

Scope Determination: The current MOD refers to the built-in functional modules maintained by this project and delivered with a program. The module code is compiled directly into the host, and the language and art continue to be configured by the data directory and manifest in the warehouse. There is currently no access to external MODs, no universal package loader, dependency version resolution, dynamic code loading, or public SDK; these do not fall within the delivery threshold of M0–M4. The language packs, art packs, and rule packs in this article only represent content collections or functional groupings that we maintain.

This article succeeds the work sequence and launch scope in [Early Enhancement Plan](native-enhancements-plan.md), especially including reliable archive management into the launch. [Extended Architecture](native-extensibility-architecture.md) continues to explain the content and interface design, [First Batch Implementation of Content](../native/native-content-foundation.md) records existing functions and historical evidence.

## 1. Product Decision

Using the same locked Japanese version of Rev 0 ROM and the original script as the running baseline, first make the original process, operation, reading and saving reliable, and then expand the query, preparation, rules and content expansion. The basic package does not change the strength of the machine by default, and does not bundle strategy tips or tracebacks.

Player configuration is divided into four independent dimensions:

| Dimensions | Selection and Boundaries |
| --- | --- |
| Language | `ja`, `zh-Hans` Complete product coverage first; other languages are registered through language packs. Language does not select another ROM, nor does it change routes, rules, or random status. |
| Art | Original / HD one-click switch; advanced settings can select pictures and models respectively. Fonts, UI font size, map zoom, and internal rendering resolution are configured separately. |
| Basic experience | Combat performance, scene speed, reading, archiving, map operation, input and readability. After turning off the enhancement, you can still start, play and read compatible saves normally. |
| Rules and Assistance | Rule amendments, additional information, automatic response, retrospection and content expansion can be started and stopped respectively; the option to change the persistent gameplay state has entered the archive compatibility list. |

Three basic experience presets are provided: "Original" maintains the rhythm and rules of the original performance; "Enhanced" enables accepted shortcut operations, reading, and safe node saving; and "Customized" retains item-by-item settings. Both presets turn off rule correction, hidden condition tracking, auto-response, and backtracking by default. The default does not overwrite the language and art selected by the player; the language and art installed for the first time are selected separately.

"Original" refers to the use of original art and does not promise to restore the full original UI or N64 resolution. When selecting Chinese and Original, you can still use the native Chinese typesetting; you need to keep it separately according to the development mode of the original word map. The existing F6 will continue to use the current meaning and will not change its behavior in advance until the full image quality setting is implemented.

## 2. Current starting point and gap

This table is maintained in combination with the code and each special operation record; the scope of evidence for each conclusion is subject to the linked document.

| Current Base | Subsequent Gaps |
| --- | --- |
| `ja` / `zh-Hans` directory of the same JP ROM; standard double-frame dialogue, native reading UI and name page copy | 2026-09-23 Names, labels and system prompts are covered by [entry list](../native/localization-terms.md) (4,674 in Chinese and English) records, drafts), the original inter-scene scenes and pre-war pages can display translations; the plot dialogue still only has 93 drafts of the first episode; the original menu, opening baked text, etc. are not fully accessible to consumers; the translation and review of the entire plot have not been completed. |
| Start selecting the language, F7 to hot switch Japanese/Chinese/English cycle and remember, no pop-up window; missing translation/draft/review coverage report | This round of coverage settings, missing translation fallback, hot switching and reporting, translation is scheduled for another time; still need to expand consumer, font and layout acceptance. See [Three Verifications](../native/native-foundations-verification.md). |
| F6 on-the-fly switching allows images and 5600 models in the list; image mode is applied by the rendering thread | Fixed Original startup fallback when HD image/avatar files are missing, see [Verification Record](../native/native-original-fallback.md). At present, it is still partial art and a single model; the classification of assets, language map isolation and complete coverage need to be completed. |
| Verbatim dialogue, paging, replay and speed control | It cannot be directly regarded as a verified "jump-only read"; it requires stable read records, selection barriers and plot status control. |
| The unified entrance saves session history, summary verification, rollback and explicit selection; saves the collection transaction prototype; the original tactical backup of the first episode has been cold-started back to the map | There are still RNG and map record differences in the complete recovery comparison, and the default auto-save cannot be enabled; multi-slots, bookmarks and other nodes are still to be accepted. See [Archive Recovery](../guide/native-save-recovery.md), [Three Verifications](../native/native-foundations-verification.md). |
| Level script structure analysis, partial instruction code evidence and partial operation observation | There are still gaps in the status field and asynchronous completion semantics; legal actions, skipping, and recovery cannot be implemented based solely on static analysis. |
| Internal game adaptation, content compilation and configuration tools | `gameplay_mods` is currently forced to be empty; the built-in gameplay module still needs to be accessed for configuration, semantic interface and saving. This reserved field cannot load external MODs and does not constitute the current blocker. |

The thread recycling defect in [Exit Life Cycle Record](../native/native-window-close.md) has been fixed in this round, and the modern name→plot closing window, original name page closing window and VI automatic exit have been verified; see this record for specific final evidence and restrictions. M0's safe node saving, cold start recovery and other scenarios still need to be individually accepted. The entire M0 cannot be closed based on this, nor can old screenshots or the results of the first episode be promoted to the entire game.

## 3. Phased delivery and dependencies

| Phases | Work Packages | Completion Thresholds |
| --- | --- | --- |
| M0: Reliable base | Exit and thread life cycle; original return entry; semantic state snapshot; built-in module switch and setting verification; archive protocol design; language and art configuration boundaries | Turn off optional enhancements and still start; existing language/art configuration and module switches do not interfere with each other; internal repeated writing and illegal settings can be located; there is evidence of safe nodes and required recovery status. |
| M1: First release basic package | §4 All functions; §5 Multilingual basis; §6 Original/HD; Defects that have reproduced and been approved for basic repair | The results of each battle performance mode are consistent; safe node cold start recovery is passed; language × art interchange is compatible; the protagonist/route range declared by the first release has completed the actual process acceptance. |
| M2: The second phase of the basic package | Target attack query, threat range, mental retrieval, maintenance simplification, budget, compilation presets, selected animations, round battle reports | Query and execution share verification; re-verify when confirming; existing resources are not copied; no unverified accurate damage commitment. |
| M3: Rules and auxiliary package | Optional rule modifications, identity information, inheritance prompts, hidden conditions, automatic response, undo/rollback | The default status and impact are clear; the rule version is traceable; old archive compatibility and retroactive recovery are accepted separately. |
| M4: Own content expansion | Known field patches maintained by the project → original level parameters → structured events → new units/battles; linkage special projects | Each layer first verifies writeback, capacity, reference and archiving, and is still built and delivered with this project; it does not rely on external author interfaces or SDKs. |

In M0, language content and adaptation layer investigations can be promoted separately; M1's combat skipping and safe node recovery have independent technical thresholds, and the acceptance standards cannot be lowered for the sake of delivery progress. The query interface of M2 can be investigated in advance, but the product will be released after M1 is stable. Defect recurrence occurs throughout all stages; confirmed faults that affect the underlying process are fixed first, without waiting for M3.

The calendar construction period will not be reported for the time being. First complete three vertical prototypes of M0's combat, save and unit status, and then estimate the time based on the actual gap. When M1 is not completed, a beta version with clearly marked coverage can be released, and a partial first-episode demo cannot be called a complete first release. The full game release requires a separate list of protagonists, main routes, divergences, departure and rejoining, and ending coverage.

## 4. M1: First basic package

| ID/Module | Implementation Boundaries | Behavior that must be demonstrated |
| --- | --- | --- |
| B01 Combat Animation | Fully on/fully off; request to skip at any time during playback; hold down the shortcut key to temporarily accelerate and release to resume. Skip requests completed at the nearest authenticated security boundary. | Complete playback, closing, skipping at different time points, temporarily accelerated settlement, plot and random status are consistent; no repeated settlement, no missing pre-war/post-war events. Segments that cannot be safely skipped should be listed as incomplete. |
| B02 sub-scene speed | Independently set map movement, mental performance, enemy actions, menu transitions, and text speed; restore corresponding settings when switching scenes. | The speed only affects the recognized wait/presentation sequence; the confirmation key is consumed according to the real input edge, and acceleration does not create double clicks; the pressed accelerator key is not transparently transmitted when switching back to the menu. |
| B03 Plot Reading | Replay, display the entire sentence, and skip the read dialogue; different quick display triggers confirmation of the next sentence at the same time. | Stop at unread, selection, and unknown script barriers; execute original plot events one by one; do not skip branch selection, rewards, deployment, or route flag updates. |
| B04 Archiving and Backup | Multiple manual slots; automatic saving of verified nodes at the beginning of our turn, preparation phase, etc.; rotation backup; bookmarks before divergence. | Cold start restores the complete progress; the old generation is still available after the save is interrupted; the different bookmarks are restored to the checkpoint before selection, and the route flag is not changed directly. |
| B05 Map operation | Previous/next unmoved unit; List positioning; Menu/scrolling/sort memory; End of turn prompt; Stay mark for this turn. | Legal objects and map locations are accurate; staying behind only suppresses reminders for that round and does not consume actions or change AI; clear the next round, and resume loading according to the saved round. |
| B06 Status and unavailability reasons | Displays mental effects, action status, resources; gray weapons/commands give all relevant reasons. | Use the actual verification results to distinguish power, EN, ammunition, range, movement restrictions, combination conditions, etc.; unknown conditions are not yet supported and cannot be guessed as "available". |
| B07 PC operation and readability | Keyboard and mouse/handle rebinding, mouse selection, shortcut keys, font/UI scaling, screen shake/white flash reduction. | Key conflict and focus consumption are clear; map zoom, UI font size and rendering magnification are independent; text/icons are used simultaneously for status; mouse selection is accurate under zoom and edge scrolling. |

### Implementation constraints of combat and speed

Maintain an authoritative settlement path. The show can draw less, wait shorter, or push at proven boundaries, but it can't simulate a set of damage on its own based on the screen. If random numbers or plot events are found to be consumed during the performance, the same logic calls and sequences must be retained; simply fast forwarding to the end frame does not meet the requirements.

The comparison starts from the same checkpoint and random state, uses the same semantic instructions; compares HP/EN/SP, ammo, vitality, status effects, fake count, kills, experience, funds, team, action status, event flags and random state, and continues to the next action check to hide drift. Frame count and display-only timing can be different; exclusion fields must be described. Differences cannot be masked by forcibly overwriting random status at the end of settlement.

Input uses press/release handling independent of show tempo; menu bursts only use real time for allowed navigation operations. Audio, message waiting, and scene life cycles are adapted separately. The existing global running speed probe cannot directly become a scene-specific speed function for players.

### Read records

Use content package namespace, TextKey, structure fragment, source version/control structure summary and necessary event context to identify read, not just save the "last sentence number". Sentences containing dynamic parameters should preserve the semantic parameter signature or adopt a conservative stopping strategy to prevent new plots with the same template from being accidentally jumped. It will only be marked as read after it is fully displayed and actually advanced; looking back will not increase the read count.

The first version saves the read collection according to the game file and restores it with checkpoints; sharing across games can be opened independently later. Switching the language does not change the read status, and the selection always stops; the relevant records become invalid after the source text or event structure is changed. The review record saves the TextKey, parameters and version. When the old content is missing, the saved display text can be used as a record without re-executing the script accordingly.

### Secure Node Saving Protocol

1. First verify whether the native game save routine completely covers the target node. If not, list and serialize the required extended state; you cannot claim to support any-round recovery just by copying SRAM. Manually saving the first version is only available at safe nodes, and the reasons will be explained at other times.
2. Safety node requirements: no battle settlement, unfinished plot commands, resource/scene switching or instructions to be submitted; obtain a consistent state of the same generation in the game thread. The automatic save point is after the event at the beginning of the round is completed and before the player can operate; the divergence bookmark is generated at a stable node that has been verified before the selection occurs. If it cannot be stably intercepted, use an earlier node and indicate the location.
3. The save set contains basic game data, necessary expansion status, gameplay configuration fingerprints, stable ID mapping, read and auxiliary metadata; must cover random, event, team, transformation and component status required for restoration. The number of episodes, rounds, known routes, save time, play time and notes are displayed; unknown routes will not be disclosed in advance.
4. First write an immutable new generation, verify all members and summaries, and then atomically publish the index pointing to this generation; retain the old index if it fails. You cannot rename two separate files individually instead of a consistent commit that saves the collection. Concurrent saving and serial processing prevent the same file from being overwritten by multiple processes.
5. Manual, automatic rotation and bookmark pool management; the capacity is configurable. Automatic pools do not retire manual slots, locked bookmarks, or only valid backups; deletion of old generations occurs after a successful commit of the new generation.
6. Check the completeness and gameplay compatibility before loading, and then build the status; if it fails, the current progress will not be changed. Testing must include cold starts after a clean exit, abnormal interruptions, corrupting individual members, the program not supporting the state required for archiving, and reading after switching language/quality.

More granular post-combat undo and turn rollback return to M3. The first release does not provide or imply simulator-style instant saving at any time.

## 5. Multilingual: Platform support and translation content are accepted separately.

| Jobs | Delivery Requirements |
| --- | --- |
| Text coverage ledger | Lists plot, name, weapon/spirit/skill, menu, combat text, archive/setting, baked text; records whether it has been extracted, accessed, translated, reviewed, and accepted by the actual machine. Statistics by unique key, while indicating actual display consumer coverage. |
| Language Pack Protocol | Stable namespace and TextKey; source language, applicable content version, source summary, named parameters, control barriers, review status, font policy. Adding a new language does not require modifying the host language enumeration. |
| Compilation and rollback | If the basic content is not translated, it will fall back to Japanese; if the new content is not translated, it will fall back to the source language declared by the content. Single missing translations can be rolled back. If the summary/control structure is invalid, the invalid package will be diagnosed and rejected before loading. Event errors cannot be masked as ordinary missing translations. |
| Full text access | Adapt menus, battles, names and other consumers one by one; the source word map will only display path suppression after it has been taken over. Language maps are classified separately to prevent Original from forcibly losing the selected language. |
| Typesetting | Unicode, font fallback, Japanese and Chinese prohibitions, long names, English long words, dynamic parameters, paging, UI scaling and missing word prompts; Chinese and English data texts have been covered by the entry table (4,674 entries each), and the first draft of the plot and battle lines has been translated (line text file), which are all drafts, and we do not claim to have completed the translation based on this. There is a separate acceptance check for complex writing directions. |
| Player name | Keep the player's custom name and the original game encoding/verification; it cannot be judged whether it has been modified by being equal to the default string. Any Unicode name requires a dedicated persistence solution for subsequent implementation. |
| Selection and Validation | Select the language at startup; use F7 in the game to cycle through Japanese/Chinese/English and remember it, without pop-up windows. Table of contents, paging, review and input are updated together; the same fragment is displayed from the beginning, automatic advancement is paused, and the next sentence is not confirmed. Old rendering frames retain the old directory, and hot switching does not change the gameplay state. |

First set `ja` / `zh-Hans` as product support targets and deliver a third language sample package. **The language system supports Chinese, which does not mean that the entire game is completed in Chinese. ** The actual coverage, draft and missing translation fallback range are listed when publishing; if the complete Chinese version is claimed, the entire claimed range must be translated, reviewed and verified by the actual process. Full language content production is scheduled separately by protagonist/route and glossary, and can be progressed simultaneously with runtime development.

## 6. Original / HD: item-by-item reversible presentation system

Assets are classified by "images without text, language-related images, models, UI skins". The stable asset ID must have a verifiable original resource identity; when the hash is ambiguous, the scene/resource context is added. Replacement packages declare coverage, versions and file summaries, not the replacement quantity to represent the full HD.

| Settings | Behavior |
| --- | --- |
| One-click Original / HD | Original selects the original art; HD selects the replacement provided by the project and passed the verification. If there is no single replacement, use the original image/original model. Packages that require changes to model structure, collision, or gameplay data may not be classified as pure HD. |
| Custom art | Then select pictures, models and UI skins respectively; the mixed configuration displays "Custom". The last configuration is remembered when switching from Custom to Original, and can be restored when switching back. M1 can use linkage switching first. |
| Language-related images | Select the corresponding style in the selected language; if the style is missing, use the same language replacement or native text layer, and then process it according to the language pack fallback rules. Translation cannot be turned off by turning off HD. |
| Font/UI/Map/Resolution | Save separately, the image quality shortcut keys are not modified; reducing white flash/shock screen is also independent. The settings UI shows the actual active mode and uncovered items. |

Follow the path of "window submission request→rendering thread applied at safety boundary→confirm mode"; old resources wait to be released after GPU usage is completed. Models, textures, and flags that suppress the original image must be switched in the same generation to avoid blank frames or mixed sizes. If the switch fails, the last valid configuration will be retained and the reason will be reported. It cannot be shown that the switch has been performed but the old resources will continue to be used.

If the entire art package referenced by the current configuration is missing/summaries are inconsistent, a startup error will be reported; M0/M1 should be supplemented with visible diagnostics and a "continue with original image" entry. Unsafe loading is still prevented when the program does not support the required gameplay state for archiving; art errors should not prevent players from restoring the original presentation. Normal image quality operations do not change the archive, plot or random status; the user explicitly saves the settings before updating the configuration for next startup.

The acceptance should include at least `ja` / `zh-Hans` × Original / HD with the same scene and checkpoint comparison, and then add third language samples, missing translations, missing assets, long sentences/large font sizes, repeated switching and scene switching. Compare the gameplay status, and check the screen, text, transparency, model, resource release and input; static compilation cannot replace actual native running and manual screen inspection.

## 7. M2: Query and preparation

The common prerequisites are unit snapshots, reachability, legal actions and command verification interfaces. The query is read-only and does not consume random numbers or change gameplay status other than cache; it outputs the binding status generation. The game thread re-verifies before the player confirms, and the result is refreshed after the status changes. The stale preview cannot be executed directly.

| Features | Specific Delivery and Boundaries |
| --- | --- |
| Target center attack query | Select enemy → List attackable friendly units, legal movement positions, weapons and consumption → Preview → Player confirmation; the first version does not provide unverified precise damage figures. |
| Enemy threat range | Legal attack coverage of single or all known enemies; enemies that can attack the destination are displayed when moving. Clarify the attack caliber after standing/moving, and deal with terrain, obstruction, EN, ammunition, energy, movement restrictions and special weapons; the unknown rule mark is incomplete. Indicates abilities, does not predict AI, does not reveal reinforcements that do not show up. |
| Team spirit search | Find the legal caster by effect/target, display consumption and remaining SP, enter normal target selection and confirmation; do not bypass range, object or plot restrictions. |
| Simplified maintenance | Parts can be directly exchanged, collected, and locked, and unit/part filtering and comparison before and after transfer can be performed; the exchange is performed as a part instance, and all failures are rolled back. |
| Transformation budget | Temporarily store multi-machine plans, total prices and results, which can be withdrawn; check funds, prices and qualifications during unified confirmation, submit atomically, and cancel without consumption. |
| EW Switch Preview and Confirmation | Before the last modification of the airframe triggers the switch, the capabilities, weapon/range changes, modification inheritance, component slots and component destinations will be displayed; cancellation will not result in payment or status change. Verify the original mapping first; after modification, keep the TV form as an independent behavior option if it is otherwise supported. See [QOL01](../gameplay/original-bug-register.md). |
| Compile presets | Attack teams, legal transfers, and allocation of existing parts; differences and missing/conflict reports are given before loading, and no silent replacement is performed. Only existing resources are allocated, components are not copied, and transfer and attack restrictions are not exceeded. |
| Selected animations | First-time weapons, collection units, designated bosses/special battles are played first; the first record is submitted after the actual battle is completed, and the identity does not depend on language. Follow the same settlement path as B01. |
| Round Battle Report | Subscribe to completed events to summarize damage, kills, resources, and important events; click to locate a valid unit, and only records of objects that have left the field will be displayed. Event IDs are deduplicated and files are read and restored without duplication. |

## 8. Defect registration and optional rules

The following items are all **leads to be verified**. 2026-09-16 [Online Bug and Confusing Behavior Registration](../gameplay/original-bug-register.md) has been added, including 9 bug candidates, source differences of skill values, EW/weapon inheritance verification and recommended reproduction steps; the original version has not been reproduced or the game code has been modified. Fix reproducible saves, routes, inputs, and original behavior first, then decide how to fix it.

| ID | Problem to be verified | Minimum reproduction/control and target |
| --- | --- | --- |
| FIX01 | The number of five flying clones is abnormal | **Recurred, the cause is confirmed, and it is effective as a basic fix by default** (2026-09-18, no switch is provided): The enemy pilot's record `+0x14` is both the number of clones and the number of our kills, `800A5054` puts W The pilot's kill backup is written into a new record for any faction; Wu Fei's enemy deployment record itself says there is no dummy, so the repair is just to restore the state required by the record. See [Basic Fix](../gameplay/base-fixes.md). Still to be added: Comparison of different kill numbers on the original route, and the return of save files after adding it. |
| FIX02 | Specific route Wan Zhang/Titan 3 has not been added | Fixed archive before divergence and actual options, compare event execution, route status, pilot/aircraft roster and actual available teams; add counterexamples where conditions are not met to avoid unconditional release of units. |
| FIX03 | Modifications were lost after Spiegel and others rejoined | Save the status of modifications/components before leaving the team, after rejoining, and after loading files; track initialization and inheritance sources, and distinguish abnormal losses from clear plot resets. |
| FIX04 | Other issues with leaving/rejoining/switching status | Check pilots, airframes, modifications, component instances and flags by event type; cover repeated triggers, transferred components, transfer conflicts and save files, without batch recovery to cover legal changes. |
| FIX05 | Enhanced parts menu cursor out of bounds | Reproduce from quarantine archive A/combine input, check slot, number of parts, adjacent status and write boundary; external report includes over-slot equipment, abnormal status and crash, local reasons need to be confirmed. Corresponds to registration BUG09. |

Records for each case: baseline/build/rule version, source clues, trigger conditions, minimum input, expected basis, original reproduction, field read-write chain, repair switch comparison, regression and compatibility impact. The status is "To be reproduced → Reproduced → Reason confirmed → Default classification decision → Implemented → Accepted"; when the evidence does not support it, record the behavior that cannot be reproduced or expected, and do not force repairs.

Default classification principle: Failures that can be proven to violate team/archive consistency and do not involve design reset can enter basic repairs; boundary reactions, superpowers/holy warrior corrections, special defenses and other behaviors that significantly change the strength or weakness can enter optional "rule corrections". Even if the cause is a bug, the original balance will not be automatically replaced. Newly added confirmed fixes are listed and versioned first, and old archive behavior cannot be changed silently with updates.

2026-09-18: The default of the trial entrance is changed from "all closed" to **all open** (determined by the user), and a "rules" menu is added to the program menu bar, which can be switched one by one in real time in the game, take effect immediately and remember; the windowless probe host still defaults to the original rules. The following "default default off rule modification" principle therefore only applies to future release defaults and needs to be reconfirmed before launch.

2026-09-17: BUG01–04 (superpower, holy warrior, base power, limit) has been implemented as five optional rule switches. The launcher is selected with `--rules original|fixed` or `--rule-fixes`. Each session records the rule version and enabled items; these corrections do not write archives, and you can switch directly if you have progress. BUG05/FIX01 (the number of fakes when Wu Fei is hostile) was classified as **Basic Fix** on 2026-09-18: According to the default classification principle of this section, it is a fault that "can prove a violation of its own data consistency and does not involve design reset", so it takes effect by default and does not make a switch. See [Basic Fix](../gameplay/base-fixes.md). See [OPTIONAL RULE MODIFICATION](../gameplay/rule-fixes.md). The settings interface and rule summaries in archive metadata still need to be designed uniformly.

2026-09-18: The rules are divided into corrections (default on, currently six items) and difficulty adjustment (default off, currently two boss disguises). The entrance gradually shifts from the "Rules" menu in the menu bar to "Options → Gameplay Adjustments". For the complete setting window structure, each metadata and acceptance, see [Settings Window Plan](../native/settings-window.md) (the first version has been implemented that day, and the rest are still plans).

The rule configuration provides "Original Rules/Amendment Rules/Customized", recording the actual sub-items, implementation version and effective rule summary. The first version establishes the gameplay configuration in the new game; existing progress changes need to be clearly compatible and migrated, back up first, and cannot be eager in battle. If migration is not possible, keep the original configuration and continue or request a new game.

## 9. M3: Information and auxiliary package

All can be started and stopped independently and are not tied to basic archiving, quick operations or repairs. The following additional information and proxy operation functions are turned off by default for the first release.

| Modules | Behavior and Acceptance Boundaries |
| --- | --- |
| Avatar information | Displays the existence and remaining number of times. The battle preview indicates whether only the avatar is consumed this time according to the confirmed rules; unverified exceptions cannot give a confirmation prompt. Only reveal information, do not reduce the number of times. |
| Transformation inheritance tips | All/part/no inheritance and explain the scope of application; the name of the successor can be hidden. The source and version of the information can be checked and will not be inherited uniformly. |
| Hidden condition tracking | Off by default; known information sorting, fuzzy prompts, and complete strategy level three; only generate known information from events that have occurred to avoid the UI leaking hidden units in advance. |
| Automatically respond to enemy turns | Off by default; set retention thresholds for EN, ammunition, SP, etc.; pause when abnormal, high-risk or insufficient information occurs, and the user can take over at any time. The normal checksum command process is called, and the combat results are not written directly. |
| Undo/turn back after combat | Expressly stated will affect difficulty; relies on complete checkpoint/event recovery, covering random, plot, battle report, read and MOD expansion status. You can only roll back accepted boundaries and cannot cross unknown external side effects. |
| Optional rule package | Modification refunds, unified inheritance, fake body weakening, etc. that change resources or strength, single-column effects and archiving requirements are not marked as pure QoL. |

Pure prompt switch changes should not prevent loading. Automatic response and backtracking If you save policies or checkpoints, you should use the respective versioned extension status; it will affect the compatibility judgment when restoring semantics, and cannot be ignored by "UI MOD".

## 10. Minimal built-in module architecture

Keep the fixed recomp runtime and implement our own functional modules directly in the existing host. Explicit interfaces and configurations are separated according to actual functions, and do not require first access to N64ModernRuntime’s external content loading mechanism or `.nrm`. Safe storage, compatibility detection, language fallback and diagnosis are core services; reading, combat performance, map convenience operation, information prompts and rule correction are enabled separately by function.

The first version just uses the explicit module assembly and initialization sequence in the code. Each module calls the shared adaptation layer and subscribes to the required semantic events; it does not impose dynamic loading, import and export, or independent package formats on each module in order to simulate the plug-in system. The internal C++ interface can use type-safe value objects and immutable snapshots and does not require cross-binary ABI stability; persistence schema and stable IDs require versioning.

| Capabilities | Minimum Contract |
| --- | --- |
| Module and configuration | Stable module ID, start and stop, default value, setting schema, effective time, saving impact; unified release with host version. Capability preconditions are explicitly verified by the code, and external package dependency versions are not solved. Configuration changes must indicate whether they affect the current archive. |
| Life cycle | Distinguish between taking effect at startup, taking effect at the next safe node and showing hot switching; the gameplay configuration is frozen before the first version is started. Explicit initialization, event sequence, switch/load reset, and exit cleanup; subscribers cannot overwrite existing hooks. When a module error occurs, unsubmitted requests are rejected, and the executed gameplay effects cannot be automatically rolled back by closing the module. |
| Read-only queries | Unit/pilot/weapon definitions are separate from running instances; unit snapshots, legal actions, ranges and unavailability reasons use the same rules source. The handle has a generation and becomes invalid after switching/reading the file. The query does not consume random status. |
| Command | UI submits a request with status generation; the game thread re-verifies and executes at a legal time, and returns the reason and result. The render/window thread does not write to RDRAM and does not expose arbitrary memory writes as a normal interface. |
| Events | Semantic events such as start of round, selection change, dialogue fragment, battle completion, level entry, save/load, etc.; clarify before/after the occurrence, whether commands can be issued, and event ID. Restoring state is separate from newly occurring events, and reward callbacks are not replayed. |
| Field patch | The changes we maintain are expressed as stable ID + field path, with baseline value/source summary assertion, verification range and reference; repeated writing of the same field will report an error or explicit combination during development/configuration check. Indicate the source of the module, define the combination behavior by the project, and do not give players arbitrary loading order arbitration. |
| Content and code | Translation, art, and supported data fields inherit the local directory/manifest; function code is compiled together with the host. Game addresses, symbols and overlays are concentrated in the adaptation layer. The modules use semantic interfaces and do not maintain memory addresses separately. |
| Diagnosis | Records the start and stop of built-in modules, valid configurations, field sources, events and comparison results; provides an optional enhanced recovery startup preset that can use the source language and original art. This default does not bypass gameplay save compatibility verification. |

Responsibilities are divided internally according to game adaptation, content data, language, presentation, archiving and functional modules; the corresponding layers in [Extended Architecture](native-extensibility-architecture.md) can be reused, and the external packages and public API parts are not implemented for the time being. Migrate step by step by function, do not move the host or generate code all at once for planning. Language/display only generates output from payloads and snapshots, and cannot maintain an additional set of properties that are disconnected from billing.

### Archive Compatibility Decisions

Save and record the game baseline, host build version, save schema, built-in modules and rule configurations that affect gameplay, effective content/rule versions, object ID mapping and extended state schema; display settings are saved as a file. The gameplay fingerprint ignores language, fonts and pure art; when the same module has both UI and gameplay, it will be processed according to the actual saving impact. The build version is used for traceability. It does not require rejecting old archives every time it is recompiled. The compatibility judgment is based on the actual status and rule agreement.

| Differences | Loading processing |
| --- | --- |
| Language, font, pure UI, art changes or missing | Allow file reading, use explicit rollback; report shows differences, does not modify the progress. |
| Same gameplay identity and compatible save format | To allow reading, first verify the mapping of all saved members and IDs. |
| Built-in gameplay module/rule version changes | Only tested compatibility statements or migrators are accepted; larger version numbers do not automatically equal compatibility. Back up before migration and keep the original files if migration fails. |
| The current program does not support necessary states, unknown unit/level IDs, incompatible rules | Prevent loading before applying any state, list the required program version, built-in content or rule configuration and recovery method, do not automatically replace objects. |
| Old JP originals without MOD metadata | Identified and verified according to the clear original import process; do not guess that the current rules are the original rules. Old patch ROM/Chinese experimental archives require special migration verification. |

## 11. The first batch of executable tasks and delivery sequence

| Sequence/Task | Deliverables | Subsequent dependencies |
| --- | --- | --- |
| 1. Return of the original version and life cycle | Fixed new game/first episode/load/exit entrance, repaired or confirmed to have fixed thread recycling; supplemented the entrance for other representative protagonists. Record components, native operations and manual acceptance respectively. | All safe save, resource switching and recovery tests. |
| 2. Semantic states and probes | Read-only snapshots and differential reports of unit/team/turn/event/random states; settlement and performance boundary diagrams of an engagement; a complete list of candidate save points. Unknown fields are registered item by item. | B01, B02, B04, B06, and M2 queries. |
| 3. Built-in modules and configurations | First group existing reading, picture/model settings into clear module boundaries; declare switches, effective timing and saving impact, provide effective configuration summary and turn off enhanced presets; Original can be started without optional HD resources. | First-release presets, function combinations, and archive identification; do not rely on external loaders. |
| 4. Secure archive vertical prototype | Complete manual save → exit → cold start recovery → damage rollback on a confirmed complete node; save collections are released by generation. | Expanded safe nodes, automatic rotation, and different bookmarks. |
| 5. Combat control vertical prototype | Fully open/full off/skip midway/press and hold to accelerate a normal battle, compare the settlement and the next action; then expand to special defense, fake body, knockdown and event battles. | B01/B02 release threshold, selected animations and battle reports. |
| 6. First expansion | Press §4 to complete the map, unavailability reasons, reading, and input; press §5/§6 to supplement the consumer, settings, and language × image quality combination; expand the FIX01–05 reproduction entrance. | M1 functional complete beta version and route acceptance. |

The investigation of combat and saving in item 2 should lead to feasibility conclusions before large-scale UI development. After each item is completed, the actual status, evidence path, and missing boundaries are updated; this table cannot be directly checked as implemented.

Code submission is split according to "Adaptation/Snapshot → Built-in Module and Configuration → Save Protocol → Specific QoL → Content → Run Acceptance", and the rule repair and prompt interface will be split separately. Keep changes to existing working trees attributable, without mixing in ROMs, archives, makefiles or screenshots.

## 12. Release acceptance matrix

| Category | Minimum Check |
| --- | --- |
| Enhancements that do not change gameplay | Off/on, press semantic operations to compare key states with the next action from the same checkpoint; animation, speed, reading, art and language combination coverage, random states remain consistent. |
| Input and reading | Press and hold, quick click, repeated key press, out of focus, handle switch, selection, unread, long sentence/pagination; check that one input will not display the entire sentence and confirm the selection at the same time. |
| Archives | Manual/automatic/rotation/bookmarks, safe node rejection, cold start, save interruption, corrupted members, out of space, old schema, required module status unsupported and rule changes. |
| Query and resource operation | Query does not change status; display available is consistent with actual execution; stale results are rechecked; budget, transfer, component and preset cancellation/failure have no side effects. |
| Rule repair | Original reproduction, repair comparison, non-triggered counterexamples, design reset retention, old file compatibility; not merged into pure display test results. |
| Language and Art | Japanese/Chinese × Original/HD, third language samples, missing translations/missing images, font size and scaling, continuous switching, menu/plot/battle different consumers. |
| Process | Protagonists/route supported by each statement, cross-session saving and loading, differences, leaving the team and rejoining, special battles and endings; the coverage is not publicly listed. |

Static schema and Python/C++ components are checked to prove the format and local logic; the actual native operation proves the status and performance of the corresponding entrance; the original reference simulator is used for comparison when necessary; manual acceptance covers the screen and input experience. The evidence is recorded separately, and the entire game process is not replaced by an exit code of 0, a screenshot, or directory coverage.

The initial delivery should also provide: feature and default value list, language/HD coverage report, built-in gameplay module and archive compatibility instructions, verified process list, known defects and recovery startup method. After completing these, expand the efficiency functions of M2 and the optional gameplay and content of M3/M4.