> **Language / Ngôn ngữ:** [English](custom-campaign.en.md) · [Tiếng Việt](custom-campaign.vi.md) · [中文](custom-campaign.md)

# Custom campaign: multi-level series, new dialogues and a whole new map drawn

2026-10-01. User-set goals: The mod can connect multiple custom levels into one campaign; the new map is based on "free drawing of the entire map": in HD mode, the entire map is drawn by the author, and in original mode, it displays an approximate version stuffed into the original format. This article is **static analysis** (reading the generated code, ROM, and Python prototype), and has not been run on the host; the address is based on the generated code of main 94f110b. Items marked [actual machine] have previous operation records, and the rest are subject to verification by the actual machine. For upper-level planning, see [mod roadmap](mod-roadmap.md) and [extended architecture](native-extensibility-architecture.md) §6.

## 1. Already have the foundation

- **Single level**: [Mini level](../script/mini-stage.md) Use JSON to write the map, events, deployment and initial resources. After compilation, replace a scene in the memory. The complete process (opening, attack, round event, victory, end, settlement archive) [actual machine] run through. All 1812 events in the script have been solved to the end symbol, and 73 ordinary instructions have been matched to the code ([Script Exploration](../script/stage-script-exploration.md)).
- **Dummy text records**: The host is already supplying the game with text records that are not included in the ROM. This is how to modify the slot text of the screen: `host.cpp` wraps the record lookup `8008C510` and the ROM read `8007F704`, `upgrade_rules.hpp:415-451` points the descriptor to the fake ROM area (`0x03000000 + id×0x40`) and then supplies bytes. New lines follow this approach (§5).
- **Entirely drawn map**: The HD tactical map has been drawn entirely by the host according to the layout number (`native_map.cpp`, 131 maps).
- **Multi-save bar and auto-save**: `saves/` library and auto-save are available next to `.json` ([Multi-save bar](save-slots-autosave.md)).

## 2. How to go between levels in the original version

| Steps | Code | What to do |
| --- | --- | --- |
| Pass | `3D4A` → `8020DB08` | Clear stages and rounds (F5E8/F5EA), cumulative total rounds (F5EC), add one to the number of words `8010F5EF`, copy the current scene F5F0 to F5F1 (passed scene), switch to mode 0x24; then run the end event (type 14) on the world map |
| Specify the next level | `3D4B n` → `800A0260` | `F5F0 = F5F2 = n`; when n=500, copy F5F2 back to F5F0. So F5F2 is always the last explicitly specified target |
| Between scenes | After the event ends, `8009EDB8` is set to mode 4 → `801D8F74(0)` | After passing the level, ask to save the file first ([actual machine] screenshot "Episode 1...クリア"), "Subsequent のマップへ" by `801D8D20` → Mode 0xC → `801C2B9C(0)` |
| Load the next level | `801C2B9C(0)` → `8009DD58(F5F0, 0)` → `8009DE7C` | F5F1 = F5F0; **When F5EF is 0, the route variable `801602EE` is used to launch the scene number**; DMA deployment and events by scene |
| World map plot | The level's own opening event (type 12) | The opening runs on the world map (`3D32`/`3D33`, `3D3A` plays music), `3D4D` switches to the tactical map; there is no separate "world map scene table" |

Table checked by scene number: map `802195B0[场景×2]` (`80209D6C` written into F5EE), title card `802195B1[场景×2]` (`801C72C8`), title text 281+F5F1 (between scenes `801CE0F8`, archive list `801C6944`/`801C754C`), the inter-scene menu with only "Save/Next Level" items left (F5F1 in `D_801DC6D4`: 13 "(previous)" scenes plus 132), Rinku levels 109–122 (`D_801DCABC`), universe scene table `D_801DCAD8`.

At the beginning of the level, `8009DE7C` resets variables 100–114 and 128–139 to 3 and variable 54 to 1; at the end of the opening, `80093278(0)` takes a snapshot in the memory (`800FBEF0`), and retries after the game ends to resume from here.

## 3. Campaign Pack

```text
mods/<战役>/
  mod.json              名字、作者、版本
  campaign.json         关卡表、开局、标题、所借场景号
  stages/<关>.json      迷你关卡格式（srw64.mini-stage.v1）
  text/<语言>.txt       新台词，台词文本格式，记录号用 mod 段（§5）
  maps/<图>/            新地图：整张底图、地形格、可选水面色号图（§6）
```

`campaign.json` indicates:

```json
{
  "schema": "srw64.campaign.v1",
  "start": "prologue",
  "stages": {
    "prologue": {"scene": 1, "file": "stages/prologue.json", "title": "序章　新しい風"},
    "ch2":      {"scene": 2, "file": "stages/ch2.json",      "title": "第2話"}
  }
}
```

The connection between levels is written in the end event of each level (`3D4B <下一关借的场景号>`), and branches use condition blocks and plot variables, just like the original version; `campaign.json` only registers "which scene number corresponds to which level."

## 4. What the host has to do

### 4.1 Borrow scene number

- **Borrow a different original scene number (0–142) for each level**. The original version first DMAs events and deployments according to the scene number, and the host is changed in `8009DE7C`, so the number borrowed must actually exist; if different numbers are borrowed for each level, the scene bytes in the archive can uniquely point back to which level.
- **Avoid**: "(Previous)" scene and 132 (there will be fewer items in the inter-scene menu), Rinko levels 109–122 (the Rinko page will be messed up).
- **Host changes**: `mini_stage.hpp` now has only one `Image`, which locks the first registered scene. Other scenes are marked as "skipped" and can only be loaded in the title menu. Change to "Scene Number → Image" table, `register_hook` and `map_hook` are obtained by `8010F5F0`. The table is fixed with the battle: コンティニュー, game end retry, and map return halfway will be re-registered (`8009DD58(场景, 1/2)`, call point `800803D4`/`8008046C`/`80080594`), and the pair must be changed at this time.
- **リンク Menu** will overwrite F5F0/F5F2 and should be disabled or blocked during the campaign.

### 4.2 Beginning and ending

- **Start**: Enter directly (write F5F0 and F5EF=1 after `800A5138`) [actual machine]. `800A5138` clears F5EF–F5F2 via `800814F0` and clears the roster via `800A4F94`, so the start is an empty roster, no name, and no route variable. **F5EF must be non-0**, otherwise the next level will be derived from the route variable (if you enter directly, you will get scene 253 without setting the time).
- **Initial Force**: In the opening event, use `3D5A 驾驶员,0,机体,500` to register (unit 999 = only register the driver) [actual machine], `3D5B` to add funds, `3E13` to set variables; the player's deployment record itself will also be permanently added to the team (this is how people are added to the Rinku level) [actual machine]. Pitfalls: `3D5A … 4000` will leave a dangling roster for units that are still on the map. After SIGBUS, you must first `3D46` [actual machine]; `3D49` crashes when the character is not on the map [real machine]. `SRW64_STATE_FIXTURE` only aligns random numbers and cannot seed the campaign. The archive code (`load_000856D0:801C39C4…`) of the debugging menu "SAMPLE DATA" can be used as a reference.
- **Ending**: `3D71` Must be run on the world map overlay (running on the tactical map will cause the host to abort) [actual machine]. The ending overlay sets the clearance bit (`8015DDA8` bit 3), writes the archive header, and returns the title. Put `3D71` in the ending event of the last level of the campaign.
- **Game Over**: `3D4C` → GAME OVER → Restoring the snapshot after the opening and re-registering the scene is equivalent to replaying the level; there is no snapshot at `3D4C` halfway through the opening, and scene 0 [real machine] will be registered.

### 4.3 Plot variables

200 two-bit variables in `8015E818`, 26 halfwords from archive +0x2. 0–54 is what the original version continuously reads, and 100–114 and 128–139 are reset at the beginning of the level. The battle's own flag must use a variable that cannot be read and written in the original script. The specific free interval needs to be counted (scan `3E13` and conditions in all events).

### 4.4 Archive

- Original archive record (0x1F00, written by `800924D8`): +0x2 variables, +0x48 progress blocks (+0x4E map, +0x4F number of episodes, +0x50 next level F5F0, +0x51 title scene F5F1, +0x52 F5F2, +0x53 baseline level, +0x54 funds), +0x110 body, +0x9D0 pilot, +0xE80 parts. Interrupted archive 0x3AE0 also contains map status.
- **Identification of campaign archives**: The archive itself only has a borrowed scene number. The host writes an additional file (campaign id, version, scene table) next to it, and loads the campaign accordingly when reading the file; when the additional file is missing or the campaign is not installed, it refuses to read the file and explains, and cannot quietly load the original scene.
- Drop point: `saves/` The automatic archive in the library already has `.json` (`save_store.cpp`'s `sidecar()`); the manual expansion column and the cassette 1/2 column are not yet available. There is no file path when writing the cassette column in the original interface. Press the record SHA-256 as the key. It is recommended that each campaign have an independent archive library, separate from this article.

### 4.5 Title and interface text

The title card (`sprite_text.cpp:365-391`), inter-scene chapter line (`intermission_page.cpp:30`), and archive list (`save_page.cpp`) are all retrieved from the host entry table without reading the ROM, so they can be overwritten by campaign: the host adds a "borrowed scene number → campaign title" table. The pictures of the title card in the original interface mode are counted separately (title card table `802195B1`).

## 5. New lines

- **Record number segment**: The text number in the script is u16, and there are 50,975 entries in table 0 (maximum `0xC71E`). The game does not check when the number exceeds the limit, and will read the text as a descriptor with random length. **mod uses `0xC800`–`0xFFFF`**, and the host will catch it first at the search location. Skip the path and directly call `8008CE54` (`game_hooks.cpp:433`), but also connect it.
- **What the host wants to forge** (use the virtual ROM area of the modified screen, change the address, and allow only the first 4 bytes to be read):
- 8-byte ASCII header: three digits for speaker (000–360, i.e. character number), one digit for mode, and four digits for waiting;
- Text space: exactly "page number - 1" `0xFFFD`, ending with `0xFFFF`, no more than 255 words (the original copy has no boundary check);
- There is an entry for each language in the entry table, including `ja` and `<STOP>`. The number is consistent with the number of pages (the host drives page turning according to the STOP number of `ja`).
- **Loading layer**: `dialogue_text::compile` Reject records that are not in the ROM, and mod lines must go to a separate layer (`Catalog::with_translations`).
- **Speaker and avatar**: The avatar is obtained from the speaker's account via ROM `0x84220 + 人物×4`; you can borrow the avatar and name of an existing character at will. New name: The host replaces the nameplate record number (`0x111E + 说话人`) with a virtual number. New avatar: The one drawn in the game is still the borrowed one, and the HD layer (`native_portrait.cpp`, identified by pixel and palette hash) should be overwritten by the mod speaker or line number; the borrowed face will be revealed in the original image mode.
- **Select limb**: `3D44 槽, 项数, 文本号`, up to 3 items, the result is written as `+0x994` for `3E10`–`3E12` to judge. When displayed, `ui_text.cpp:307` will only change the translation when the `ja` entry is equal to the glyph solved by the game. The mod number must either match the placeholder glyph or change it to a trust mod number.
- **Battle lines** (to be done later): Press `D_800CA9C4[人物]` to get the voice slot, which is listed in ROM `0x1161C0` and `0x121150`. To assign lines to a new character, either accept `800A3DD0` to return the virtual line, or accept the selection function `80222B14`/`80222050`; whether `5813 + 偏移` can reach `0xC800` is not confirmed.

## 6. New map

### 6.1 Original format (checked)

- **Map record**: 158 entries × 12 bytes, table in `0x80219B1C` (ROM `0x10267C`): `u16 布局, 图集, 调色板, aux1, aux2; u8 模式; u8 BGM`. Read `8010F5EE` (map number) from `801C6EFC` and then load: `80098158(0x3B, 0, 8, 0x93, 布局, 图集, 调色板, 0)`, aux enters the palette cycle channel, and mode 1 installs another colonial frame. `3D34` Change the picture (`8020A874`) and use the same set.
- **Layout**: 8-byte header `(7, 组数, 宽, 高)` (8 pixel units), then 4 bytes per 16×16 grid: `u16 (翻转 0xE000 | 地形号)`, `u16 图块号`, then drawgroup. All 154 layouts and 285,974 cells were checked: the tile number and flip bit of the grid were consistent with the drawing group. Atlas CI8 512×512, up to 1024 16×16 tiles (tile coordinates 12 bits).
- **Terrain**: Take the +1 (lower 8 bits) of the terrain `801E213C(x格, y格, 0x3B, 0)` read-only grid record, no out-of-bounds check. Attribute table `0x802196D0` (ROM `0x102230`), 100 entries × 11 bytes:

| Bytes | Meaning | Reader |
| --- | --- | --- |
| +0 | Terrain name (Table 0 text number 0–59) | Terrain window `801CABAC` |
| +1 | Defense: Damage ×(100 − value)/100 | `801F424C` Select 0 (constant 100 while flying) |
| +2 | Hit modifier, signed (mostly negative) | `801F424C` Choose 1 |
| +3 / +4 | Start of turn HP / EN recovery % | `801FA3DC` → `801FA260` |
| +5..+10 | Movement consumption of six movement methods, 0xFF not accessible | `801C3E50` Use `801EEA14(单位)` to select columns; 0=ground, 1=air, 3=water, 5=space (inference), 2 and 4 are undecided |

Terrain 63 is the wall (all 0xFF, named "wall"), 99 is the outer border, and 100 is the "sky" pseudo-terrain used for the battle background. Water terrain code list `0x802180D4`: 31–36, 87–89, 91.
- **Table by map number** (158 items each): Universe flag `0x802180E0` (1=Universe movement rules; combat terrain adaptation when non-0 is calculated according to the universe; 2 only changes the combat environment bytes, like "Ground type map in the universe", map 37, 39, 49, 50, 60, 64, 72); Grid line color `0x80218510` (0 black, 1 Gray, 0xFF None, set bit `8015DDA8 & 2` (used when opening the grid).
- **The combat background is determined by the palette number**: `801F68E8` Writes the grid terrain (100 when flying) and the environment bytes into the combat context. The environment bytes are taken from the table looked up by the palette resource number (`0x80218A57 + 调色板号`, covering 6237–6263). The new map will borrow an existing palette number to select the background.

### 6.2 Dimensions

The map size is completely determined by the layout header (`801C6394` writes `80172EC4/EC8`), and a fixed-length array opened by grid cannot be found: the movement range is a 31×31 local grid centered on the unit (`801C3E50`, the upper limit of the range is 15 grids), and the occupancy is scanned according to the unit pixel coordinates. There are only three constraints: the outer 2-tile border is inaccessible (playable range x, y ∈ [32, W−48]); the overview zoom `800943E0` will divide by zero when it is about 4256 pixels wide and 3200 pixels high; the upper limit of the atlas is 1024 tiles. The original version maxes out at 960×720.

### 6.3 Install into the game

- **There is only one entry point for resource reading**: `80089E9C(资源号) → 句柄`. Number ≥ `0x1924` is directly rejected; if the same number is already in the memory, only the reference count is added; otherwise `80089BBC` reads the descriptor and decompressed size of ROM `0xA20BD4 + 号×8`, and `800897AC` is decompressed from ROM LZ into the heap (area 6, `0x80277800`, about 1.6 MB). These two internal functions are only called by `80089E9C`.
- **Method**: Borrow the map number of an original map. In the campaign level, the host replaces its layout, atlas, and palette with mod bytes: take over `80089BBC` and report the size of the mod, and change `800897AC` to copy (judge which one it is based on the resource number just written into the handle table +2). Replacement should be consistent during the period when the same number is parked. The new resource number cannot be used (≥ `0x1924` rejected), so the number can only be borrowed; which number to borrow is determined by the campaign package, and the palette number also determines the battle background (§6.1). The tables of BGM, universe logo, and grid color according to map numbers are also rewritten according to the borrowed map numbers.
- **HD Conflict**: HD maps are recognized by layout number (`find_asset` of `find_asset`), and the borrowed layout number will be drawn on the HD basemap of the original map. The host needs to click on the mod map to get the map in the campaign level.

### 6.4 Whole drawing and original downgraded version

- **HD**: The author draws a large map 4 times the original size (same as the existing HD map), and the host draws the entire map. If the water surface wants to move, give another color code map to indicate the water surface area (the existing HD map is the base map plus color code map).
- **Original downgraded version**: The tool reduces the large image to the original size, cuts it into a 16×16 grid, uses k-means to gather it into no more than 1024 tiles (allowing horizontal and vertical flipping and reuse), and then quantizes it to 256 colors to generate a layout, atlas and palette. The prototype (2026-10-01, Python script in scratchpad, not in the warehouse) tried with the HD base map of Map 56: 864×800, 2700 grids squeezed into 1024 blocks, relative to the target map PSNR 35.8 dB (only 256 color quantization is 42.4 dB). The landforms, coastlines, forests, and mountains have been preserved, and the texture of the grass has been averaged out to a blur. Maps smaller than 1024 cells (e.g. map 20,896 cells) do not need clustering.
- **Water surface recycling**: The original water surface relies on palette recycling (color number 0xC0–0xD0). The downgraded version needs to map the color of the water surface area into this section, and hang the water surface recycling resource in aux.
- **Terrain**: The author gives each grid a terrain number (0–98, and the outer circle is automatically filled with 99) in the editor. There are only 100 attributes in the attribute table, and new terrain types are not supported yet.

## 7. Phased

| Stage | Content | Acceptance |
| --- | --- | --- |
| C1 multi-level connection | `campaign.json`; mini-level host changed to scene number list; start, ending; Rinko interception; title overwriting; archive attached files and refusal to read files | Use the original map and original lines to make a 3-level mini-campaign: join the team at the beginning, save the level, load the file to continue playing, retry at the end of the game, branch, and return to the title at the end |
| C2 new lines | mod text segment `0xC800`+, virtual records, trilingual entries, optional limbs, new name tags | There are new dialogues and optional limbs in the campaign, and the pages are turned correctly in three languages; F5 hot reload |
| C3 new map | Resource replacement, borrowed map numbers and related tables, HD map acquisition by mod, map tools (large map + terrain grid → layout/atlas/palette + HD) | A self-drawn map: movement consumption, terrain defense and hit, recovery, water surface, combat background, overview, terrain window are all correct; see the downgraded version of the original image mode |
| C4 new characters | New avatars (HD override by mod speaker), battle lines | Plot dialogue and battle lines for new characters |

## 8. C1 implementation (2026-10-01, worktree custom-campaign)

User-defined: Only existing resources (original maps, lines, characters, deployments) will be used for the test campaign. New maps, plot dialogue backgrounds, new characters and new machines will be studied later.

| Part | Method |
| --- | --- |
| Battle source | `config/recomp/campaigns/<名>/campaign.json` (`srw64.campaign.v1`): `id`, `start`, `stages` for each level `scene`, `file` (mini-level source), `title` (string or object by language) |
| Compile | `mini_stage.py campaign <campaign.json> --out <image.json>` → `srw64.campaign-image.v1`. Compile level by level, rejecting scene numbers that cannot be borrowed ("(former)" 13 and 132, 109–122, >142), two levels borrowing the same scene number, the starting level cannot be found, and `3D4B` points to scenes other than the campaign (500 exceptions) |
| Host | `campaign.hpp` records the identity and title of the campaign; `mini_stage.hpp` adds a new "scene number → level image" table: `SRW64_CAMPAIGN` to load, `register_hook`, press `8010F5F0` to get the image, `map_hook` Use the map of the level; if there is no borrowed scene number from the level, it will load concurrently according to the original version. Directly enter the scene number to write the level; after registering the first level, clear the number of words `8010F5EF` back to 0, so that after the first level is passed, the first episode |
| Title | `dialogue::ui_text` For 281+ scene number, return the campaign title. It will be used between scenes and archive lists; it will also be used if the title is stuck in the campaign level |
| リンク | When opening the original リンク page during the campaign, you will directly press cancel to exit and prompt (the original リンク screen is originally an empty block) |
| Archive | Launcher `--campaign <编译后的战役>`: The archive library is changed to `用户目录/campaigns/<id>/saves`, which is separate from this article and does not migrate old sessions; mutually exclusive with `--import-save`. Debugging session `Session.launch(campaign=…)` compiles the source files, and the archive library is placed in the running directory `campaign-saves` |
| Sample | `config/recomp/campaigns/sample`: Prologue (scene 1, map 20) → fork in the road (scene 2, map 19, select limb 18402) → ending A (scene 3, map 0) or ending B (scene 4, map 21), automatic victory in the first round of each level, the end event of the ending level runs `3D71` |

**Real machine** (`tools/recomp/debug/check_campaign.py`, running `build/recomp/debug/20261001T151257.210854Z`, all 12 items passed): The campaign is loaded; after entering directly, the prologue is registered in scene 1; after passing the level, "Prologue: Departure" and episode 1 are displayed in the game; saved to the first column of the cassette, the archive list shows the same title; Rinku is stopped; the next level is a fork in the road (scene 2, map 19); Choose the first option to enter ending A, and return to the title after the ending; read the first column from the title to return to the scene after passing the prologue, then enter the fork in the road, choose the second option to enter ending B (Map 21), and return to the title after the ending.

**Test**: `tests/test_mini_stage.py` (sample compilation, non-borrowable scenes, repeated scenes and out-of-bounds `3D4B`), `tests/native_mini_stage.cpp` (change the image and map according to the scene number, unregistered scenes, opening scenes and number of chapters, illegal battles; by the way, fixed a place where the test has already failed: the main menu section tests the new game path, you must first close it and enter directly), `tests/native_app.cpp` (`--campaign` parameter).

**Game End Retry** (2026-10-02, `tools/recomp/debug/check_campaign_retry.py`, running `build/recomp/debug/20261002T011836.386183Z`, all 4 items passed): Test campaign `config/recomp/campaigns/retry` has only one level (borrowed from scene 5), the first option of round 1 is `3D4C`, and the second item is `3D4A`. Choose the first option → GAME OVER → When retrying, you will still be re-registering at the battle level (scene 5, map 20, without falling back to the original scene 5); then choose the second option to win, and return to the title after the ending.

**Prompt text**: When Rinku was stopped, the two prompts "The scene does not belong to the battle" were entered into the entry list (`campaign_link_blocked`, `campaign_scene_unmapped`, trilingual).

### MOD Management and Additional Costs (2026-10-02)

The user wants "the feeling of the DLC entrance, similar to the Z SP", **DLC levels are separate archives**; then a "MOD" entrance is placed on the title screen, and the overall MOD management is entered, classified by function (user selection: native button in the lower right corner; all four categories are required). practice:

- **Entrance**: "MOD" in the lower right corner of the title screen, the word picture is the item in the ring menu (`menu_style`'s 14 original pixel font size, 1 pixel dark stroke, 0.8 pixel shadow, dark gray and blue when not selected, bright blue when the mouse points or the handle is selected), no frame. Four corners of the title screen (user-defined): upper left setting entrance, upper right frame rate, lower left version number, lower right MOD. The controller is entered in the "MOD Management" line of the "General" page of the settings (can be opened at any time). Do not enter the original ring menu.
- **MOD Management**: A dedicated view of the settings panel, its own four tabs, L/R or Q/E page change:
- **Additional script**: One line for each campaign: name, introduction, level, version, author, whether there is an archive, and the button "Enter"; there is an additional line in the campaign "Playing: <name>" and "Return to this chapter", and the button you are playing displays "Playing" and is grayed out. The toggle is only available on the title screen, otherwise the button is grayed out and explained. The name and introduction can be written by language (`name`, `description` of `campaign.json`, brought into the image when compiling).
- **Art**: original/HD switch (the same switch as the setting), whether the HD package is installed and the directory where it is located.
- **Lines and Languages**: Player's lines folder, "Reload Lines" (same as F5), and how many lines are loaded in each language, from several files, and how many errors (`dialogue::text_summary()`).
- **Music & Voice**: Still under development, description only.
- **Switch without restarting, only change the archive path** (User: "We will separate the archive path"; once did a version of restarting and changing disks, which has been deleted): Click "Enter" on the title ring menu → `campaign_switch::enter`:
1. Copy `cartridge.sram` of the campaign archive library to `saves/campaigns/<id>/<游戏>.bin` of the runtime library (if not, delete it, and format the game as a new cassette);
2. `ultramodern::change_save_file("campaigns/<id>", 游戏)`: The runtime library first writes the current SRAM back to the file of this chapter, and then reads it into the campaign;
3. `save_store::switch_library`: The archive column, automatic archive, and cassette release are all changed to `用户目录/campaigns/<id>/saves`;
4. `mini_stage::load_file(战役, enter=false)`: Only install the campaign, return to the title and wait for "Start Campaign" or load the file.

"Return to this article" conversely: `change_save_file("")` Read back the SRAM file of this article (it has not been touched after cutting it away), replace the archive library with the one at startup, and uninstall the campaign. The runtime library file of this chapter is not written during the campaign, so the launcher still submits it to the archive library of this chapter when exiting; the archive of the campaign has been published to the campaign's own library every time the cassette is written in the game. Those started with `--campaign` do not have this article to return to and do not provide switching.
- **Title screen in the campaign**: "Start campaign" and campaign name in the middle; "Return to this chapter" from MOD management.
- **Installation location**: `用户目录/campaigns/<id>/campaign.json` (compiled campaign), `saves/` archived in the same directory; also read the `campaigns/` (Mac package's `Resources/campaigns`) that comes with the program, and the same ID is subject to the user directory. The launcher gives the host `SRW64_CAMPAIGN_DIRS`, `SRW64_CAMPAIGN_SAVES`.
- **Known minor issues**: The options for the game to read from the SRAM head into the memory (stereo/mono, clearance marks) and seen records when starting the game will not be re-read after switching. The first save of the campaign will be written to the campaign cartridge from the memory.
- **Fixed by the way**: The document where the start button of the mini-level/campaign is located used to be "remove the class name after the modal", `body` is still `pointer-events:auto`, and the entire screen is occupied by clicks; now only the button receives clicks, and other entries on the title screen can be clicked.

**Real machine** (`tools/recomp/debug/check_mod.py`, `build/recomp/debug/20261002T033647.970249Z`, all 13 items passed, completed in one process): The title of this article has "MOD"; there are four pages of MOD management (the additional script lists the two campaigns, art, lines and language, music and voice under `config/recomp/campaigns`) in both Chinese and English; click on the sample campaign → Without exiting the game, the title will show "Start Campaign"; start the campaign, pass the prologue and save it to the first column of the cartridge (campaign library generates `cartridge.sram`), choose the first item on the fork, end A and return to the title; the sample campaign in MOD management shows "Playing" and "Return to this article"; after returning to this article, both columns of the file loading list are empty (screenshot `main-load-list.png`); enter the sample campaign again, Chapter 1 The column is "Prologue: Departure" (`sample-load-list.png`), and the file is loaded to return to the scene after the prologue is cleared. When I ran it for the first time, I found out: I got all zero SRAM from a campaign I had never played before. The original version was only formatted when booting, and the archive module written in the game refused to be released. Now when entering, a formatted blank card is released to the campaign library (the option byte is taken from this article).

**Not done yet**: Archive additional files (each campaign has its own independent archive library, and loading another campaign in the same library will still not refuse to read files). The "Start" of the original ring menu in the battle still follows the new game process of this article (user determined: no change).

## 9. To be verified

- The above new conclusions are all derived from static analysis: resource replacement, scene number list replacement, virtual line recording, and map rewriting must be verified on the actual machine.
- The meaning of columns 2 and 4 of the movement cost; the complete purpose of the water terrain number table; `3D34` status table `8021E240`.
- Plot variable intervals not used in the original script.
- In addition to the "(previous)" scene, are there any other side effects in borrowing scene numbers from other scenes (the purpose of the universe scene table `D_801DCAD8`).
- Whether the battle lines `5813 + 偏移` can fall into the mod text segment.