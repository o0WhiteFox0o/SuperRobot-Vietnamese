> **Language / Ngôn ngữ:** [English](native-extensibility-architecture.en.md) · [Tiếng Việt](native-extensibility-architecture.vi.md) · [中文](native-extensibility-architecture.md)

# SRW64 Multi-Language and Content Mod Architecture Recommendations

2026-09-12: Product stage, default settings, safe node saving and language/image quality acceptance to
[Built-in MOD Roadmap](mod-roadmap.md) shall prevail. Currently, we only organize our own functions into MOD modules and compile them directly into the host; we do not connect to external MODs. The semantic interface, content layering and saving boundaries of this article can be reused; external package loading, `.nrm` access, community distribution and public SDK belong to suspended architectural research and are not current tasks or blockers.

Date: 2026-09-10; Implementation status update: 2026-09-11. The first batch of refactorings has started: unified JP running baseline, independent language directory, pure art package and original image/HD switching during running. See [First Implementation](../native/native-content-foundation.md) for details. The remaining chapters continue to be target architectures and do not mean that the SDK has been released.

The goal is to support original Japanese and Chinese in the same native program, allow other contributors to add language packs, and gradually support aircraft, characters, weapons, resources, and level Mods. This article distinguishes between existing capabilities and proposed interfaces; the example paths, namespaces, and data formats are not already available in the SDK.

## 1. Core Decisions

1. Use the locked original Japanese ROM as a unified running baseline. Language, HD resources, model replacement and gameplay Mod are selected separately; the same gameplay configuration can use different display languages.
2. Separate game object ID, display name and resource location. Translating names does not change unit identity, and replacing avatars does not change driver data.
3. Use data packages for general language, art, and numerical modification of supported fields; use code Mod when new logic is needed.
4. The original game address, byte order, overlay identity and internal structure are concentrated in the game adaptation layer. The public interface uses stable IDs, value objects, generational instance handles, and explicit lifecycles.
5. First support the coverage of known fields of the original object, and then support new objects and levels; adding new IDs requires verification of the original array, index and archive capacity.

## 2. Code structure worthy of reference

### N64ModernRuntime: Reuse Mod Infrastructure

The local fixed dependency and the upstream of this verification are both `cdf5abbd5026fef5c364c676e4667c45e42b6863`. `librecomp` already contains Mod manifest, dependencies, function replacement/hooks/events, import/export and content type registration. `ModContentType` provides callbacks for enabling, disabling, sorting changes and runtime switching; suitable for registering SRW64's own language, data and resource content in the same package management mechanism.

Reference: [Content Types and Mod Interfaces](https://github.com/N64Recomp/N64ModernRuntime/blob/cdf5abbd5026fef5c364c676e4667c45e42b6863/librecomp/include/librecomp/mods.hpp) · [Mod Writing Instructions](https://hackmd.io/fMDiGEJ9TBSjomuZZOgzNg) · [Pasture Mod Template](https://github.com/HarvestMoon64Recomp/HM64RecompModTemplate).

It is recommended to continue using the upstream `.nrm` Code Mod toolchain, supplemented by SRW64 versioned exports and symbol templates. Language/data schema, merge rules, and archive semantics still need to be implemented by yourself; upstream identification function replacement conflicts do not mean being able to identify two packages that modify the HP of the same body at the same time.

### RecompFrontend: Borrow menu and input modules

Verify commit `b1a1477c6556aeb7ed45defbfb5924f721efebc1`. Its `recompinput` manages keyboard, mouse, handle and mapping; `recompui` manages settings, Mod menu and Mod’s self-built UI, and uses RmlUi and RT64/plume internally. [Project Description](https://github.com/N64Recomp/RecompFrontend/blob/b1a1477c6556aeb7ed45defbfb5924f721efebc1/README.md)

It is suitable as an integration candidate for launchers, inputs and admin menus. The current conversational typesetting of SRW64 (a cross-platform text engine) and Metal compositing should remain in the platform backend, with text provided through a unified multi-language service. This check did not find a ready-made complete multi-language directory service, and the access to RecompFrontend cannot be regarded as a Japanese-Chinese switch. The integrated prototype needs to verify input consumption, rendering order, and language updates for both UI layers.

### Wesnoth: Drawing on the separation of content and language in war chess

Wesnoth is not a recomp, but it defines unit unique IDs, translatable names, images, abilities, and weapons respectively; levels are connected to the next level through IDs, maps, camps, events, and additional content can have independent translation fields. This is similar to SRW64’s goal of “body/character data + levels + multi-language expansion”.

Reference: [Unit Definition](https://wiki.wesnoth.org/UnitTypeWML) · [Level Definition](https://wiki.wesnoth.org/ScenarioWML) · [Additional Content Translation](https://wiki.wesnoth.org/GettextForWesnothDevelopers).

Drawing on its content layering and translation domain ideas, the first version continues to use the existing JSON tool chain of this project to avoid introducing a whole set of WML engines for configuration files.

## 3. Demolished boundaries and remaining work

2026-09-12 The old ROM Chinese pipeline has been removed. The original parsing is at `src/srw64_rom/`,
Japanese glyph mapping has independent source lock, language directory, TextKey and unified JP profile are located in
`src/srw64_native/`. The native name page uses the original game name encoding and no longer relies on the patch ROM's glyph allocation.

It is still necessary to continue to separate text typesetting and platform drawing, restore other game text consumers, and integrate internal
`SRW64GameHooks` is converted into a semantic event that can be used by Mods. Current slot and RDRAM interface
It continues to belong to the internal adaptation layer; it cannot be directly used as a public SDK. See [Native Development Guide](../guide/native-development.md) for actual responsibilities.

## 4. Suggested module boundaries

Proposed catalog, solely to express responsibility:

```text
src/native/
  app/                 启动、PlayProfile、设置、模块生命周期
  game_adapter/        日版资源/地址映射、overlay、数据读写与原脚本桥接
  content/             包解析、schema、内容注册表、合并和来源记录
  localization/        TextKey、目录、回退、格式参数、语言配置
  presentation/        对话与界面模型、资源解析、模型替换接口
  platform/macos/      Metal 合成与菜单栏
  mod_api/             版本化导出、语义事件与命令
tools/content/         提取、校验、导入导出、打包、差异报告
```

The host continues to use C++ value types and immutable snapshots internally. Interfaces that need to cross `.nrm` or dynamic library boundaries use fixed-width types, clear lengths and versions, and do not export C++ STL containers or original game memory structures.

Data flow: ROM generates basic content through the adaptation layer; the package manager merges content coverage; the adaptation layer returns valid fields to the original game at the verified loading time. The UI reads from the same payload as the running snapshot, and the language service finally parses the text for display. It must be verified that the numerical changes are consumed by the combat logic and cannot just update the data panel.

## 5. Multi-language design

### 5.1 Language and presentation are independent of each other

- The first version of locale is `ja` and `zh-Hans`; `zh-Hant`, `en`, etc. can be added in the future. Language tags are treated as data, and C++ branches are not built for each language.
- The original game text of `ja` is exported from the user's local original ROM to a directory; the newly added Japanese and Chinese strings of the native UI are maintained by the project. Unknown glyphs retain the original glyph identity and fallback capabilities.
- Original typeface and native layout are separate presentation options. HD maps, modern models, and native fonts are also available when selecting Japanese.
- The baked text in the image belongs to the language resource. No text avatars/maps can be shared; Chinese label stickers and Chinese font atlases cannot be unconditionally enabled in Japanese mode.
- Fonts, fallback, line breaks, and writing direction are handled by language configuration and text backend. The first edition is verified as being in Japan; future languages ​​do not mean that all complex writing systems have been accepted.

### 5.2 Stable text keys and control flow

The original text key retains the table and record ID, such as `base:t00_17412`; the new Mod uses its own namespace, such as `example.campaign:dialogue.intro.001`. Names, menus, and system prompts also use the same TextKey concept and are maintained in separate directories.

Original paragraphs are converted into structured messages: text fragments, named parameters, specialized glyphs and script barriers are separated. STOP/END and original interpreter advancement belong to program metadata; the translation author only modifies the corresponding fragments and allowed parameter positions. Automatic word wrapping/reading pagination can be added, but the original script barrier cannot be exceeded. Adding or removing story events is a level mod.

The translation export should include the original text, TextKey, fragment number, speaker/scene (when recognized), parameter description, source version summary, translation and review status; screenshots can be added for association. The first version uses JSON and provides PO import and export as a subsequent contribution tool. All formats are compiled into the same runtime directory.

### 5.3 Fallback and Community Language Pack

When the base game is missing translation, it falls back to the corresponding Japanese source record; when the new Mod is missing translation, it falls back to the source language declared by the content author. Third parties can publish separate translation packages, stating which content packs are translated and which versions are applicable, without copying their body or level data.

The parsing order is "determine the package to which the content belongs and the final source record → select the effective override of the language corresponding to the record → the source language of the package". The final source language of the basic text is Japanese; custom campaigns can be selected. When the source text or control structure changes, the old translation mark needs to be updated; invalid fragments fall back to the source text and are reported, and the script cannot be changed silently.

The first version selects the language during the startup/title phase and creates an immutable directory at startup. In-game hot switching is left until dialogue waiting, paging, and scene invalidation strategies are verified; you cannot just clear the texture and keep the old language paging.

The default character display name follows the locale; the name changed by the user retains the original input. In the original archive, it is difficult to identify whether the name is the default and the original value is retained. It cannot be inferred by "exactly equal to the default string". Arbitrary Unicode name input and persistence are designed independently, and the first version of language switching does not require changing the original name storage format.

2026-09-11 [Native name input prototype](../native/native-name-entry.md) has been added: the opening name editing is taken over by the system input box, supports direct typing within the original ROM glyph, and retains the original name field and verification. Archiving of arbitrary Unicode names and extensions is still work in progress.

## 6. Content Mod: From known fields to complete levels

### 6.1 Unified content registry

Create explicit types: `UnitDef`, `PilotDef`, `WeaponDef`, `StageDef`, `AssetRef`, and `TextKey`. The definition is separated from the running instance: the basic HP of the machine belongs to UnitDef; the current HP, strength and action status of this level belong to the instance.

The original object retains a stable baseline ID, and the new object uses the author namespace. The bottom layer can be converted to a compact integer index, but the mapping needs to be able to be saved and verified, and cannot change with the packet scanning order. Fields whose semantics are not yet recognized retain opaque data and origin, prohibiting name guessing or allowing arbitrary rearrangement.

Modifying existing objects prefers field overrides, with optional old value/source record summary assertions. Indicate:

```json
{
  "target": "base:unit/<verified-id>",
  "expect": { "hp": 8000 },
  "set": { "hp": 9000 }
}
```

The above example only expresses the proposed interface, and the ID and field mapping needs to be verified. The underlying adaptation is responsible for the scope, layout, derived values ​​and application timing; when modifying the maximum HP, it is also necessary to specify the processing of the current HP of the generated unit/old archive, which cannot be implicitly treated as treatment.

Modifications to different fields in two packages can be merged; modifications to the same field require clear coverage relationships or reporting conflicts. Each final value records the source package and change chain. Don't make directory ordering or any arbitrary "last person loaded wins" the default rule.

### 6.2 Package structure

Proposed content package:

```text
example.campaign/
  manifest.json
  data/units.json
  data/pilots.json
  data/weapons.json
  stages/intro.json
  locales/ja.json
  locales/zh-Hans.json
  assets/
```

Manifests reuse package ID, version, target game, and dependency fields supported by upstream; project additional metadata expresses schema, source language, content capabilities, and baseline compatibility. A package can only have `locales/`, or only assets. A package namespace is logically owned and does not rely on its disk file name.

The first version only needs to register the data content type, directory development mode and packaging entrance. Code mods continue to go upstream to `.nrm`, avoiding the need to maintain a second set of function patch loaders. For authors who only change language/numeric values, there is no requirement to install a C++ compiler.

### 6.3 Levels are opened layer by layer

1. **Original level parameter coverage**: Verified attack unit, camp, initial position, reinforcement and reward fields.
2. **Structured event editing**: Maps, deployments, conditions, actions, dialogue references and victory-defeat relationships are separated and converted into understood original script operations or verified native bridge calls.
3. **New level/campaign**: It will be opened after completing the stage ID allocation, level transfer, team inheritance, event status, saving and resource life cycle.

Keep the original script interpreter running semantics. The extractor first completes an unmodified round trip; areas containing unknown opcodes, unresolved jumps, or relocation dependencies are retained as opaque blocks, limiting their editable operations. The first version does not introduce a universal Lua interpreter to replace the original plot system. Starting from 2026-09-12, the instructions, conditional blocks, context markers and trigger types of the original script can be read statically (see [Complete Analysis of Level Scripts](../script/stage-script-exploration.md)); the writeback and run comparison have not yet started.

New aircraft are also phased in: changes to existing data are available earliest; new entries must check the array limit, weapon/character reference, AI, list rotation, and archive index. recomp allows modification of these limits, but the JSON registry itself does not automatically enlarge them.

## 7. Mod API and game life cycle

The internal adaptation layer uniformly reads and writes game state, exposing read-only snapshots and explicit commands. Proposed events include `stage_entered`, `unit_selected`, `dialogue_segment_ready`, `battle_resolved`; defining the triggering phase, sequence, parameter lifetime and whether command submission is allowed.

Data coverage and read-only observation events in the first version of the open loading phase. UI callbacks can only submit requests, and the game thread is used at defined times; the rendering thread does not directly modify RDRAM. The replacement of core rules such as damage will be subsequently opened through a separate versioned interface, and will not be repeatedly settled through multiple event callbacks in any sequence.

The public instance handle has a generation, and will be invalid after switching, reading files, and exiting. There is a clear sequence for archiving operations, content loading and scene initialization; multiple subscribers to the same event are managed by the adaptation layer, and new Mods cannot overwrite existing native dialogue hooks.

Mod API version, data schema version and game baseline version are recorded separately. Low-level direct function patches are still available as high-level extensions, but their address/symbol compatibility requires explicitly binding the version; regular content authors use stable IDs and fields.

## 8. Archive and package configuration

Language and display-only resources belong to the rendering configuration, and the goal is to switch languages without changing the level state, random numbers, or original save content. The gameplay data and the level package form a content configuration, recording ID, version, effective content summary and instance ID mapping.

The original compatible save continues to retain the original SRAM data; the extended state can be placed in a versioned sidecar/container, bound to the original save generation and hash, and atomically formed into a save set. If the code or content Mod is changed, it will persist. You cannot claim that it only affects the display.

Check the gameplay package and mapping when loading. When a new unit or level package is missing, a clear missing report and a configuration restoration entry will be provided. Unknown IDs cannot be treated as another unit to continue execution. Old stage1 Chinese experiment archives involve proprietary glyphs and name paths, and migration to the unified JP baseline requires special validation; not automatically considered interchangeable.

## 9. Implementation sequence and acceptance

1. **Language Basics**: Extract TextKey, independent Japanese source directory and zh-Hans directory; remove font/locale hard coding; run through the same scene on the original Japanese ROM with mid-day selection, missing translation fallback and native font layout. Use existing Chinese samples as migration input and retain the original acceptance evidence.
2. **Package and Configuration**: Connect to the existing Mod content type mechanism to create a language package, a pure resource package and a unified PlayProfile. Adding a third language sample only changes the data and does not recompile the host.
3. **Airframe/Character/Weapon schema and tools**: First extract, verify and report differences, and then load and overwrite a known field to prove that the original menu, actual combat and saved and read files are consistent. The editor uses the same schema and validator.
4. **Level and public SDK**: First verify the original level deployment/event round-trip, and then make a minimum level coverage sample; when the interface is actually used by two independent samples, release the SDK, template, and compatibility statement.

Key checks: Control events are consistent between Japan and China under the same operation; language switching does not change gameplay data; text IDs with the same name do not conflict when they are in different tables; template parameters and STOP/END verification; translation expiration and missing word fallback; package sorting certainty and field conflicts; UI values ​​are consistent with settlement; missing Mod/old archive processing. The acceptance of new content must include the actual game, and passing the static schema only proves that the format is legal.

2026-09-11 The development configuration/resource switching foundation in steps 1 and 2 has been implemented; content type registration, gameplay field coverage, levels and public SDK have not yet been implemented. The exact available scope and acceptance are in [First Implementations](../native/native-content-foundation.md).