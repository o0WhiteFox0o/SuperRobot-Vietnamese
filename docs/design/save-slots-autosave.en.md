> **Language / Ngôn ngữ:** [English](save-slots-autosave.en.md) · [Tiếng Việt](save-slots-autosave.vi.md) · [中文](save-slots-autosave.md)

# Multi-archive column, automatic archive and simulator archive interoperability

2026-10-01. Corresponds to [Roadmap](mod-roadmap.md) B04 (multiple manual slots, safe node automatic saving, rotating backup). This article only deals with planning: Section 1 is the conclusion of the static analysis (disassembly, existing SRAM files and simulator source code, no new probes have been added, and no actual machine operation has been performed), and Section 2 starts with the plan. The pre-construction verification items listed in Section 3 were completed statically on the same day, and the conclusion was written back to Section 1.

Three goals:

1. The host's cassette archive and the N64 emulator's archive are interoperable: you can read them when you copy them to the past, and you can read them when you copy them back.
2. The archive slots are not limited to the two in the original version.
3. Automatically archive when the original version would have been archived, and keep multiple copies in rotation.

One-sentence solution: The **32 KiB cassette file is retained as it is, as the one for interoperability; the newly added columns and automatic archives are stored in the host file, and each copy contains the bytes written into an archive column (or interrupt area) by the original version. ** When reading and writing, the host only transfers the original SRAM transfer to other files, and all serialization, verification, and recovery follow the original code.

## 1. Facts about the original archive

### 1.1 SRAM layout (32 KiB, address relative to SRAM starting point `0x08000000`)

| offset | size | content | write/read |
| --- | --- | --- | --- |
| `0x0000` | 0x10 | File header: the first 7 bytes magic number `SRW64V3` (table `800C6AE4`), +7 is the setting byte (`80162DA8`, bit0 sends `80076D90`, like sound mode) | Boot `8009171C` read; titleオプション Modified by `8009187C` and written back +7 |
| `0x0010` | 0x1F00 | Archive column 1 | `80092678(0)` write, `80092744(0)` read |
| `0x1F10` | 0x1F00 | Archive Column 2 | `80092678(1)`, `80092744(1)` |
| `0x3E10` | 0x3AE0 | Map interrupt archive (only one copy) | `80093278(1)` writes; `8009365C` reads all, `80093610` only reads the first 0x20 bytes depending on whether it is necessary |
| `0x78F0` | 0xA0 | The "seen" bitmap shared by all cassettes, from RAM `8010F4D0`, see §1.6 | **Every** column archive and interrupt archive are first written by `800916EC`; boot `8009171C` to read back |
| `0x7990` | 0x670 | Unused (existing file contains all zeros) | — |

- **Boot formatting**: `8009171C` Compare the first 7 bytes of the file header. If it does not match the magic number, clear the entire 32 KiB, and then write the magic number and default setting bytes. Therefore, the magic number must be in the correct position when importing, otherwise the game will clear the entire card.
- **SRAM transfer**: All pass through `80090E5C(方向, SRAM 地址, RAM 缓冲, 长度)`, direction 1 write, 0 read (the parameters are handed over to PI DMA `800AE4A0` as they are). The host side falls to librecomp's `save_write`/`save_read`.

### 1.2 Archive column record (0x1F00)

- Serialized from `800924D8` to buffer `801C2600–801C44FF` (airframe 0x2BC, driver, parts compressed item by item, funds, etc.). This memory is free only when the inter-field overlay (`load_0008F4B0`, starting from `801C4500`) is installed; both tactical overlay and combat overlay start from `801C2600`, so the column format can only be written between fields**.
- **+0 u16**: bit15 = used; lower 8 bits = checksum, equal to the lower 8 bits of the sum of 0x1F00 consecutive bytes starting from +2. These 0x1F00 bytes are 2 bytes past the end of the record, and are read into `801C4500–801C4501`, which is the first two bytes of the inter-field overlay. The ROM `0x8F4B0` is fixed to `00 00`. So **you can calculate the checksum just by looking at the file**: Column 1 and the interrupt area of ​​the three existing SRAM files are all consistent.
- Write `80092678`: write → read back in place → recalculate the checksum comparison and return success or failure.
- **Read without verification**: `80092744` and `80085CD4` (read the two column headers) only look at bit15; the read file `80092C70` of title ロード is also restored by `800927A4` if bit15 is 1.
- The fields used for the list are all in the record (relative to the starting point of the buffer): +0x4C total round u16, +0x4F number of words, +0x51 chapter title number, +0x54 fund u32, +0x98 and six name glyph codes; the protagonist category starts from +0x9D0 in the body table (12 bytes per item) and is obtained by looking up the initial body 0x19–0x1C; the level is obtained by `800A630C` is calculated based on driver data, so the host does not calculate it by itself, see §2.3.

### 1.3 Interrupt archive (0x3AE0)

- Map menu Interrupt → はい: Tactical overlay `load_000AB160`'s `801D21D0` first writes `80172EB2 = 8`, then adjusts `80093278(1)`, then writes `80172F09 = 1`, adjusts `801D1534(4,0)` to return to the title.
- `80172EB0`/`80172EB2` is the main state/substate of the map interface, **not in the interrupt record** (the recovery routine only restores the body, driver, components, mothership loading and progress blocks). Writing 8 just goes down the state machine of this confirmation menu.
- `80172F09` is the "just interrupted" flag: the map distributor `801DFCCC` decides to return the title after leaving the map accordingly; `800840C0`, `801E0350` will clear it. It's not in the record either.
- So the host adjusts `80093278(1)` by itself and does not need to imitate these two writes.
- Buffer `800FBEF0` (resident segment), +0 u16 is also bit15+ checksum, only covering the first 0x1F00 bytes.
- `80093278(0)` only serializes to this buffer and does not write to SRAM. `8009EDB8` Do this once before switching to another screen in the middle of the map. When you return, use mode 0x16 (`800801A4` item 21) or 0x22 (item 33) to adjust `800936A0(0)` directly from the buffer. The snapshot is used when the map is returned, so overwriting the buffer when the map is idle has no effect.
- Serializer only writes its own buffer. The only bypass call to `800A4148` recalculates the summary bitmap of `8016A1F0` according to its existing state, with unchanged results.
- Title コンティニュー (main state 6) adjust `8009365C`: if bit15 is 1, switch to mode 0x11 and return to the map, otherwise it will buzz. **Not cleared after reading**, the interrupt archive will be kept until the next interrupt overwrite.
- The original interrupt archive does not save the random number status starting from `800D49D0` 0x834 bytes (this is what the README "Incomplete random status recovery" says). Not only that, every time the tactical overlay is started, `801E00AC` is used to count `8015DC50` and `800821B0` is re-seeded, so the original version reads the same interrupt file, and the result of the subsequent battle is not fixed.

### 1.4 File byte order

- `save_write` of librecomp is written byte by byte according to the N64 byte address, so the host file is in big-endian original order, and `SRW64V3` can be read directly from the beginning (`build/recomp/save-recovery-check/intermission-cold-1.source.sram` has been checked).
The byte order is determined by the simulator and has nothing to do with the game, so read the source code of each simulator directly (2026-10-01):

| emulator | file | endianness | basis |
| --- | --- | --- | --- |
| This host (librecomp) | `<id>.bin`, 32 KiB | Big-endian raw order | `pi.cpp``save_write` written byte-by-byte as `MEM_B` |
| ares | `save.ram`, 32 KiB | **Big endian, the same as the host** | `n64/memory/lsb/writable.hpp` uses `readm/writem(4)` to read and write each word as big endian; 2026-09-30 ares actually reads through after the host file is renamed |
| Project64 | `.sra`, 32 KiB | 32-bit word reverse order | `SaveType/Sram.cpp``DmaToSram` Write RDRAM (PJ64 internally stored as little endian) directly into the file, and when not aligned, press `^3` byte by byte |
| mupen64plus | `.sra`, 32 KiB | 32-bit words in reverse order | `device/cart/sram.c`: `mem[(cart_addr+i)^S8]`, S8=3 on little-endian host, file is memory |
| RetroArch mupen64plus-next | `.srm`, 0x48800 | The SRAM segment in the container is the same as mupen64plus | `libretro_memory.h`: EEPROM 0x800＋4×handle package 0x8000＋SRAM 0x8000＋FlashRAM 0x20000, the SRAM segment is in 0x20800 |

ParaLLEl-N64 and other other cores are not checked. If you encounter it during import, just use the magic number to identify it (§2.5). The identification does not rely on the above table: the magic number `SRW64V3` in the file header is fixed in various byte orders.

### 1.5 Status related to archive timing

- **Entry Room**: `801D8F74(参数)`. Parameter 0 = normal entry (after passing the level, the plot will be transferred); 1, 2 = title ロード reading column 0, 1 (call `80092C70(参数−1)`); 3 and up is コントローラパック.
- **时のマップへ**: Each frame of the main menu of the game (`801CE19C`, has been packaged as `srw64_original_intermission_menu_step`). When pressing A in the 9th item, write the exit code `D_801DD540 = 2` and fade out; screen scheduling `801D8D20` will open the game after seeing 2 and enter the next map.
- **Our turn idle**: The script injects the existing idle determination (`docs/script/script-debug-injection.md`) - event engine idle, `8010F5E8 = 1` (our stage), `8010F6B0 = 0` (no defeat process), `8015DA02 ∈ {3, 0xB}` (tactical map) - plus the main map state `80172EB0 = 5` (idle cursor, per frame function) `801C8B04`, wrapped as `srw64_original_map_idle`). The current round `8010F5EA` starts at 0.

### 1.6 Shared block: two "seen" bitmaps

Starting from `8010F4D0`, the 0xA0 bytes are two 0x50-byte (640-bit) bitmaps, which are only set and never cleared (cleared only during boot formatting `80091470`):

| bitmap | set | read |
| --- | --- | --- |
| `8010F4D0` character | `800914F4(人物号<287)`, via alias table `800C6A08`; called when loading dialogue avatar `8008F970` and creating a new driver record `800A84F8` | title overlay `801C8AF8` (`80091574`) |
| `8010F520` unit | `800915F0`; called when assigning unit instance `800A6E68` | Title Music Appreciation/Unlocking of カラオケ (`80091670`, see title menu documentation) |

They are cumulative collection records for all cassettes, regardless of which column. Automatically archive photo original writing. It will only write down the bits that have been seen, without any side effects. When importing an emulator cassette, you can bitwise OR the bits on both sides, see §2.5.

### 1.7 Host status

- Standalone application (`src/native/app/runtime.cpp`): Copy the last `sessions/<id>/save.bin` into a new session each time it is run, and write `runtime-data/saves/<id>.bin` while the host is running. **Submit only after normal exit** into `save.bin` of the new session, and update `last-session.txt`; the archive of this run will not be submitted when it crashes.
- The archive screen (`src/host/save_page.cpp`) and title ロード have been taken over by the RmlUi page. The writing call is `80092678`, the reading head is called `80085CD4`, and the file reading is handed over to the original load mode `0x12 + 栏`.
- `800924D8`, `80093278`, `800927A4`, `800936A0` already have hooks (`game_hooks.cpp`), currently only used by `state_probe`.
- The host does not have a コントローラパック, and the Pak path is fixed, and this plan does not involve it.

## 2. Plan

### 2.1 Archive library (user directory `saves/`)

```
saves/
  cartridge.sram            32 KiB 卡带，大端，和 ares 的 .ram 同一份字节
  cartridge.sram.prev       上一代，发布新代前保留
  slots/007.rec  007.json   扩展栏：0x1F00 记录 + 旁注
  auto/inter-0.rec  .json   场间自动存档（栏格式），轮转
  auto/turn-0.sus   .json   回合自动存档（中断格式 0x3AE0），轮转
  imports/<时间>.sram        每次导入前的卡带备份
  trash/                    删掉的栏先挪到这里
```

- **Column numbers are consecutive numbers for users**: Columns 1 and 2 are the two physical columns in the cassette, and the interface is marked "cassette"; Column 3 and up are expansion columns.
- **Side note json**: Logged SHA-256, write time, play time, cached save headers (§2.3), and optional random state (§2.6). (Remarks were originally planned, but have been discontinued at the request of the user, see §8.) Broken or missing marginal notes only affect the display and random status, but do not affect file reading; the record itself is only valid based on bit15 and summary judgment.
- **Write**: Always "Temporary file → Flush → Rename". The cassette file is released immediately after each original archive operation (column archive, interruption, option) is completed, no longer waiting for normal exit; `sessions/` still makes audit and historical copies.
- **Migration**: When the new version is started for the first time, the `save.bin` pointed to by `last-session.txt` is verified and copied to `cartridge.sram`, and the old session remains unchanged. `--import-save` is imported to cassette instead (follow §2.5).
- **Isolation**: The debugging sessions (srw64ctl/MCP) still use their own running directory. The archive path is given by the environment variable. By default, it points to the copy in the running directory and does not touch the player archive.

### 2.2 Virtual Column: Only change the direction of SRAM transfer

Packaging `80090E5C`. The host maintains two mappings:

- `slot_window[2]`: Physical columns 0 and 1 correspond to the cassette or expansion file. The default is the cassette.
- `suspend_target`: Does the interrupt area correspond to the cassette or which automatic archive file.

Reroute only if the address and length exactly match the following three transmissions:

| Transport | Matching | Diversion Practices |
| --- | --- | --- |
| Column read and write | `0x10` or `0x1F10`, length 0x1F00 | Read: write the content of the target file into RAM in big-endian format; write: first put it into the buffer to be submitted |
| Interrupt reading and writing | `0x3E10`, length 0x3AE0 | Same as above |
| Interrupt detection | `0x3E10`, length 0x20 | Read the first 0x20 bytes of the target file |

The rest of the transfer proceeds as usual: everything except the file header, `0x78F0` shared block, and interrupt area falls to the cartridge.

Key points:

- `80092678` will be read back for comparison immediately after writing. The readback must retrieve the uncommitted buffer just received, otherwise the write will be judged as failed. After the original function returns successfully, the host publishes the file atomically.
- Mapping only takes effect during one operation initiated by the page: write a column, read a column, read a batch of headers. The default will be restored after the operation is completed. So vanilla interface mode and any paths not taken over will only hit the cartridge and behave exactly like vanilla.
- Do not change librecomp. The redirection occurs at the game function layer, and the host file is only placed after the original call returns.

### 2.3 Multi-column reading, writing and listing

- **Write to extended column k**: Map physical column 0 → k, adjust `80092678(0)`, and the original serialization, writing, and readback verification will all run as usual.
- **Read extended column k**: map the physical column 0 → k, then use the original load mode `0x12 + 0`, and adjust `80092C70(0)` by the inter-field overlay.
- **List**: Map two expansion columns to physical columns 0 and 1 each time, adjust `80085CD4` once, and get the two-column archive header (including level). The results are cached together with the record summary and are not recalculated if the summary remains unchanged. In this way, the level and protagonist's avatar are all given by the original logic, and the host does not have to parse the driver data by itself.
- **Original Interface Mode**: Only two columns of cassettes are displayed, which is exactly the same as the original version. The expansion bar and auto-save only appear on modern pages.

### 2.4 Automatic archiving

There are two types of nodes, each using the original format and rotating respectively (default 3 copies between games and 5 copies per round, which can be changed or turned off in the settings).

**A. Between Fields (Column Format)**

- Node 1 (entering the site): package `801D8F74`, record "to be automatically archived" when the parameter is 0; build the main menu between sites (`801CDFB0`, the native page has been taken over) and execute and clear the flag when running for the first time. Reading files and entering the field (starting from parameter 1) are not remembered.
- Node 2 (before attack): Pack `801D8D20`, see `D_801DD540 == 2`, and when it is about to be dismantled, save it first and then call the original function. This one contains all the changes that players have made this time.
- Method: Map physical column 0 → `auto/inter-n.rec`, adjust `80092678(0)`. This is the same path that players take when saving in データセーブ; when both nodes are equipped with an interfield overlay, the `801C2600` buffer is idle (§1.2).
- This kind of archive is a normal column record, which can be copied to the cassette column 1 and 2 for the emulator.

**B. Our turn starts (interruption format)**

- Node: In the package of `srw64_original_map_idle` (per-frame function of main state 5), if the idle condition of our turn in §1.5 is met, and `8010F5EA` (turn) is different from the automatic archive of the last turn, the original function will be saved first and then called. It is only saved once per round; it will not return to idle until the event at the beginning of the round is performed, so it is naturally ranked after the event.
- Method: Reroute the interrupt area to `auto/turn-n.sus` and adjust `80093278(1)`. Do not write `80172EB2`, `80172F09`, nor return the title: they are not in the record (§1.3). Serialization will overwrite the resident buffer `800FBEF0`. At this time, the mid-way snapshot there has been used and has no impact.
- Read: The interruption area is redirected to the selected file, and then takes the original path of the title コンティニュー (main state 6).
- If the player selects Interrupt in the map menu, the cassette interruption area is still written to ensure that the simulator can continue to play.

**Shared block processing**: Both automatic archives will write the `0x78F0` shared block to the cassette according to the original version. It is a "seen" bitmap (§1.6) that only increases but does not decrease. Writing it in has the same effect as the player's manual archive; columns 1, 2 and the cassette interruption area will not be changed by the automatic archive.

### 2.5 Interoperability with the simulator

**Export**: The cassette file itself is in ares format and can be directly copied to ares for use.

- Other simulators convert and export according to the format of §1.4: `.sra` of Project64 and mupen64plus is a 32-bit word in reverse order. RetroArch's `.srm` is also in this byte order, but it needs to be written into the merge container: if the user gives the existing `.srm`, only the SRAM segment in it will be replaced; if it is not given, it will be newly created and the remaining segments will be filled with zeros.
- If you want to bring the expansion bar or automatic save to the simulator: "Copy to cassette bar 1/2" is provided on the interface. Confirm before overwriting. The overwritten old bar will be automatically moved to an expansion bar.

**Import** is divided into two types:

- **Whole card import**: Convert the emulator file into a new cassette file. The original cassette is backed up to `imports/` first, and the original archives in cassette columns 1 and 2 are automatically copied to the extended column and will not be lost; the "seen" bitmaps on both sides are bitwise ORed (§1.6), and the collection progress will not be lost.
- **Single column import**: Only take out a certain column or interruption area in the simulator file and put it into an extended column or automatic archive. The card will not move.

**Format Identification** by file size and magic number:

- 32 KiB: Try the original, 32-bit word reverse order, and 16-bit reverse order to see if offset 0 can read `SRW64V3`;
- 0x48800 (RetroArch merged archive): Find the magic number in the SRAM segment of 0x20800 in the same way;
- None match: reject the import and do not make guesses. The game will clear all cartridges that do not match the magic number (§1.1), so the wrong import must be blocked at the host level.

**Validity**: The original read file is not verified, but the checksum can be calculated from the file (§1.2). When importing, check whether the magic number, bit15 of each column, checksum, and archive header fields are within a reasonable range (number of words, title number, round). Columns with inconsistent checksums are marked, and it is up to the user to decide whether to import them anyway.

### 2.6 Random status notes (only interrupt format, does not affect interoperability)

Only round autosave (and player's map interruption, if desired) is required. There is no need to save between games: when the next map starts, `801E00AC` will always be reseeded with the count `8015DC50`, and the random state between games will not be left on the map (§1.3).

- Save random number status `800D49D0` (0x834 bytes) and record summary in side notes when archiving.
- When reading the file, the record summary read back by `800936A0(1)` is consistent with the marginal notes, so "to be written back" is recorded.
- The writeback point is placed in the existing seeding package `resident_func_800821B0`: when the tactical overlay is started, `801E00AC` is seeded. After the original function returns, the 0x834 bytes are written back and the flag is cleared immediately. The first time the random number is taken after that, the state at the moment of archiving is used.

In this way, the automatic archiving of the read round in the host can completely reproduce the moment of archiving, meeting the requirements of the roadmap that "the randomness required for recovery must be overwritten"; the same record will have no annotations in the simulator, and the performance will be the same as the original version.

### 2.7 Interface and settings

- **データセーブ** (Modern Interface): Scrollable, paginated list of columns, columns 1 and 2 marked with cassettes, and "New Column" at the end. Each column can be deleted (moved into `trash/`). The coverage confirmation still uses the original two sentences.
- **Title ロード**: The tab is divided into "manual/automatic". The automatic tab lists two automatic archives between games and rounds, with the number of words, rounds and time marked.
- **Settings Overlay Panel**: automatic archiving switch, two types of rotation copies, and import and export entrances.
- All new characters are added to the entry list, and all three languages are available.

## 3. Verification items before starting work (statically completed on 2026-10-01)

| Item | Conclusion | See |
| --- | --- | --- |
| `80172EB2 = 8`, `80172F09 = 1` | The sub-state of the map interface and the "just interrupted" flag are not recorded, and there is no need to imitate the automatic round archiving | §1.3 |
| `0x78F0` Shared block | Two additional "seen" bitmaps for characters and machines, regardless of column | §1.6 |
| Interfield node | `801D8F74(0)` Entering interfield; `801D8D20` See exit code 2 sortie | §1.5, §2.4 |
| Round node | Idle condition injected by script + main state 5 + round number change, hung in `srw64_original_map_idle` | §1.5, §2.4 |
| Random state writeback | Tactical overlay must be re-seeded when started; writeback is placed after seeding packaging; no need between fields | §1.3, §2.6 |
| Simulator format | Determined from source code, no sample files required | §1.4 |
| Checksum | The out-of-bounds 2 bytes are `00 00` in the inter-field overlay header, which can be calculated from the file | §1.2 |

There are still things that can only be proven by actual performance: the screen is consistent with the values after reading back the automatic save, the battle results are reproduced after the random state is written back, and the ares are read and written back and forth (S2–S5).

## 4. Stages and Acceptance

| Stage | Content | Acceptance |
| --- | --- | --- |
| S0 | Static completion §3 | Completed (2026-10-01) |
| S1 | Archive library, migration, whole card and single column import and export, format recognition | Completed (2026-10-01), see Section 6 |
| S2 | `80090E5C` Rerouting, multi-column saving and reading, instant publishing, modern pages | Completed (2026-10-01), see Section 7 and [Archived Screen Document](../native/native-save-screens.md) Section 4 |
| S3 | Automatic archiving of two nodes between sites, rotation | Completed (2026-10-01), see Section 8 |
| S4 | Round auto-save, コンティニュー redirected reading, random status side notes | Completed (2026-10-01), see Section 8 |
| S5 | and simulator actual measurement | Completed (2026-10-01), see Section 9 |

For real-machine running of S2 and above, and simulator running of S5, please ask before starting each run.

## 5. What not to do

- No real-time archiving at any time (see the roadmap for reasons). Intra-turn undo is left to M3.
- The original archive format will not be changed, and no host private data will be written to the cassette; the host private data will only be placed in the side notes.
- Cannon Torotron is not supported.

## 6. S1 implementation record (2026-10-01)

Code:

- Format layer: [`src/native/app/sram.hpp`](../../src/native/app/sram.hpp)/`sram.cpp`, pure byte processing, no file touching.
- Archive library: [`save_library.hpp`](../../src/native/app/save_library.hpp)/`save_library.cpp`.
- Initiate session access: `Session` of `runtime.cpp`.
- Command line: `--export-save`, `--export-format` (`export_save` of `runtime.cpp`, `--play` branches of `host.cpp`).

Differences from §2:

- **Cassettes are not released immediately** and are still released by `Session::commit_save` when the host exits normally (older cartridges are left as `.prev`). For immediate release, you need to know in the game thread that "an original save operation is completed", and do it together with S2's `80090E5C` package.
- **Side note json saved for S2**. The record file of S1 only stores the original bytes, the integrity relies on bit15 and the calculable checksum (§1.2), and writing relies on atomic rename. Side note is only for display cache and random state, profiled by a host that can use nlohmann json.
- **Command line import is strict**: If the cassette lacks the magic number, or the used column/interrupt area checksum does not match, the import will be refused. The option of "Import still needs to be imported if the checksum does not match" is left to the S2 interface.
- **`--new-game` No column loss**: Before exiting to publish a new cassette, the intact columns 1 and 2 in the old cassette are stored in the extended column; records with the same bytes will not be saved repeatedly. Even if the old cartridge is damaged, it will not hinder the new game. Only the intact columns will be retained; the old directories that have not yet been migrated will be migrated first. If the migration fails, the new game will start as usual.
- **Auto Archive Pool** (`auto/`) and **Recycle Bin** (`trash/`) added in S3, S4 and interface.

Test (no ROM required):

- `tests/native_save.cpp` (`native-save`): Conversion between four export formats and 16-bit reverse order, RetroArch container retains other archives, two checksum boundaries (column out of bounds 2 bytes, interrupt only counts 0x1F00), archive header fields, corruption reporting, "seen" bitmap merging, release retention `.prev`, import retains old columns and backups, repeats import without duplicating columns, single column import, backup before export, refuse to overwrite irrelevant large files, extension column 3-99 is full.
- `tests/native_app.cpp`: session releases cartridges, rejects unformatted host archives, refuses to boot if cartridge is damaged and can be `--import-save` restored, `--new-game` retains old columns, old `sessions/` migrates, export parameters.
- Fake hosts of `native_launch.cpp` and `native_rom_import_probe.cpp` rewrite the cassette with magic numbers.
- There are currently 3 real SRAMs (Chapter 1 cleared, Round 5 interrupted, Round 1 interrupted) all judged to be intact. Column 1 reads Chapter 1, Round 7, and Funds 14500, which is consistent with [Archive Screen Document](../native/native-save-screens.md).

## 7. S2 implementation record (2026-10-01)

The practice and actual results are written in Section 4 of [Archived Screen Document](../native/native-save-screens.md). Only the differences and remainders from §2 are recorded here:

- **Instant release of cassette has been done**: The host tracks every write to the cassette and releases it when the cassette is available; `Session::commit_save` releases it again when exiting (the contents will not change if the content is the same). At the beginning of a new game, move the column of the old cartridge into the extension column (when constructing `Session`), because the blank cartridge will be released after the game is formatted.
- **List not cached**: Extension column archive headers are reread with `80085CD4` every time the column list is opened. Column 99 is only dozens of memory copies, so the archive header cache in the side note is not done; the side note json will be added when there is a random state (S4).
- The deletion column, import and export in the interface, and "Import still needs to be imported if the checksum does not match" that did not exist at the time have been completed in §8. The original interface (switch back to the original inter-field screen and title screen in the settings) only has two columns for the cassette as in the original version. This is intentional: the original mode does not add anything that the original version does not have; the expansion column and automatic archive can be read and written in the new version interface.

## 8. S3, S4 and in-game interface (2026-10-01)

### Automatic archive (`src/host/autosave.cpp`)

Only enabled when there is an archive library (standalone application; debugging session needs to pass `SRW64_SAVE_LIBRARY`).

| Node | Hook | Writing method |
| --- | --- | --- |
| Entering the interfield | `801D8F74` packaging (newly renamed `srw64_original_intermission_enter`) is recorded when the parameter is 0, and is saved every frame of the next interfield menu (after `801CE19C`) | `save_store::Window(0, 新文件)` down `80092678(0)` |
| Before attack | You will see `D_801DD540 == 2` after each frame in the inter-game menu (the same inter-game is only saved once) | Same as above |
| Round starts | Map is idle every frame `801C8B04` Before: Main state 5. Idle conditions injected by script, (title number, round) are different from last time | `save_store::SuspendWindow(新文件)` Downgraded `80093278(1)` |

- File: `auto/inter-NNNNNN.rec` (column format), `auto/turn-NNNNNN.sus` (interruption format), both share an incrementing serial number, the newer the bigger. The `.json` next to it records the node, time, title number, round, and funds; the round archive also records the random number 0x834 bytes (hexadecimal) and the recorded SHA-256.
- Rotation: After writing, only the latest N copies will be kept according to type (default is 3 games, 5 rounds; optional 1/3/5/10 on the settings page), and the extra ones will be deleted together with the marginalia. Manual bars and cassettes are not affected.
- The "once per round" mark is reset between entering the field, attacking, and when the map is restored: reading a round save and returning to the same round will not save another copy immediately.

### Read automatic archive

- The list of titles ロード lists all autosaves after the expansion bar, with the newer ones first. The inter-session archive uses the same "one-time redirection to load column 0" as the expansion column.
- Round archive: After confirming `arm_suspend(文件)`, write the main state of the title as 6 (コンティニュー), sub-state 0, and hand it to the original version: `801C6D1C`, check the read interruption area, switch mode 0x11, `800936A0(1)`, read it again and restore the map. Both reads are from this file; the recovery is completed (after `800936A0` packaging) and the redirection is released. Initially, calling `801C6D1C` directly will write the increment of the substate by one to the substate of ロード, and the screen will stop at the confirmation box, so it is changed to the main state 6.
- Random number: When the recovery is completed, if the file summary is consistent with the marginalia, write it down to be written back; when the map overlay is started, `801E00AC` is seeded (after `800821B0` packaging) and 0x834 bytes are written back immediately. After that, the random number will still be advanced frame by frame according to the original version, and another count `8010E09C` will be reseeded at the beginning of the battle, so the results will be different if the player's operating rhythm is different; writing back only ensures that the random state at the moment of loading is the same as when saving. These two counts may have other timing purposes and have not been touched.

### In-game interface

- **REMOVED** (R): Expansion bar and auto-save. The confirmation window inherits the position of the overlay window (mode 3, "データを気ます.よろしいですか?", the default is "いいえ"); "はい" moves the record and marginalia into `trash/`. Cassette slots 1 and 2 cannot be deleted.
- Automatic archiving displays the archive time on the right side of "Episode N". Column remarks (L input in place) were done before, deleted at user request on 2026-10-01: There is no comment function, and L does not work on the archive page.
- **Archive settings page** (new page of the settings window "Archive", `saves_page` of `frontend.cpp`): automatic archive switch and number of copies, export, import, see [Settings window](../native/settings-window.md). Export writes `export/srw64-ares.ram`, `srw64-project64.sra`, `srw64-mupen64plus.sra`, `srw64-retroarch.srm`, overwriting the previous one each time. Import scan `import/`, each file lists the used columns; columns that do not match the checksum will be prompted first, click again to import with the repaired checksum (`SaveLibrary::import_slot(…, repair)`). Importing the entire card is still only through the command line `--import-save`: replacing the cassette while the game is running will be inconsistent with the cassette in the game memory.
- Bring the expansion column or autosave to the simulator: after reading the file, save into column 1 or 2, and then export.

### Verify

- Offline: `native-save` 71 items (new automatic archive serial number, rotation by category with marginalia, deletion into recycle bin, single column repair import, scan); layout audit added samples of automatic archive, expansion column, deletion window and archive settings page (including import list), four window sizes and three languages 0 problems.
- Actual machine: `tools/recomp/debug/check_autosave.py` is run in five times (mini level flow, pass the level and enter the field and attack, enemy-cycle map round starts, title read round save, title read, attack save and save into column 3 (L does not work), delete the oldest automatic archive); `check_save_settings.py` (Archive settings page: switch, number of copies, export four files, check byte by byte, import, checksum inconsistent columns are rejected first and then revised) 8 items passed.
- Three issues found and fixed in the actual game: Directly calling `801C6D1C` in the round save will get stuck in the confirmation box (see above); the title page will adjust the page step every frame, and empty actions were treated as "cancel" and the delete window will be closed immediately.

## 9. S5: actual measurement with simulator (2026-10-01)

`tools/recomp/debug/check_emulator_interop.py`, 7 items passed; no game window is opened, the host is only used for export and import.

- **Command line only imports**: `srw64-gfx-host --play --import-save 文件 [--user-dir 目录]`, without `--rom`, it only imports the file into a cassette, does not start the game (`import_save` of `runtime.cpp`), and holds the same user directory lock as the game (`UserLock`, rejected when the game is running).
- **RetroArch (mupen64plus-next core, fixed version in `build/libretro/cores`, headless driver)**: Put the entire `.srm` written by `--export-save` into the core's archive memory (the way RetroArch reads `.srm`); the script input is from the titleロード Read column 1. After entering the field, データセーブ is stored in column 2; write the core archive memory back to `.srm` and then `--import-save`: recognized as RetroArch/32-bit word reverse order, column 2 It is written by the core, the checksum is correct, and the archive header (number of words, rounds, funds, name) is the same as column 1. Screenshots: loading list, between games, after saving.
- **ares(`/Applications/ares.app`, GDB service reads memory)**:
- Read: The cassette is read as `save.ram`. After booting, the "seen" bitmap of `8010F4D0` is the same byte-for-byte as the cassette's `0x78F0`. Comparison: The same cartridge is given to ares in reverse order of 32-bit words, and the bitmap is all zero (the game treats it as if the cartridge has not been formatted), indicating that this check can distinguish the byte order.
- Write: No archive is given, the game formats the cassette in ares, ares' own memory is automatically saved (every 30 seconds) and writes out `save.ram`; `--import-save` is recognized as big endian, and the imported cassette is the same as the ares file byte by byte.
- **What is not done**: Ares does not drive the game to save a certain column (ares only recognizes the keyboard of the focused window, and the test does not grab the front desk); column-level in-game writing is covered by the RetroArch core above, and the file byte order of ares is determined by both reading and writing. Project64 does not have a macOS version. According to the source code, it is in the same order as mupen64plus (§1.4), and is only covered by the S1 format test.