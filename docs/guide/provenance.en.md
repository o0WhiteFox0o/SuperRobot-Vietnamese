> **Language / Ngôn ngữ:** [English](provenance.en.md) · [Tiếng Việt](provenance.vi.md) · [中文](provenance.md)

# Local input and source records

This file records the input required to reproduce the experiment but cannot be submitted to Git. Hashes are identity gates, they do not represent
These files can be redistributed.

## Japanese ROM

- File location: local `rom.z64`, not submitted;
- Size: 33,554,432 bytes;
- SHA-256: `ee5f4a21d8e5f7827d21199e27800edf250df9a8e4d10befb1a6992df597b13e`;
- Endian magic: `80371240`;
- Game code/revision: `NS4J`, Rev 0;
- Header CRC: `1649d810 f73ad6d2`.

## Original Japanese glyph mapping

- Warehouse location: `reference/original-glyph-map.csv`;
- Independent identity lock: `config/data/original-glyph-map.json`, records the current SHA-256 (deviated from upstream, see next section);
- Source: [Localize](https://github.com/snowyegret23/Localize), commit `91e0c15b76b44c302f29ddebc1c45e61f1828cd0`;
- Upstream file: `SRW N64/reference/srw64_glyph_map_seed.csv`, SHA-256
`f9e98bfca8ba13e5b37287bad5c795d57dd3f48b9e0d7865b330a5d5c1bd3567`;
- Purpose: Decode text from original Japanese ROM for use in native language catalogs, data browsing and font experiments.

The mapping is initially moved in unchanged from the old reference clone; the build no longer relies on the entire reference repository.
ROM identity, text table and resource parsing is done independently by `src/srw64_rom/`.

### Deviation from the upstream seed (2026-09-17/18, checked according to the font bitmap)

The 1,936 lines of the upstream seed are all labeled `confirmed`, but 109 of them are mapped by multiple glyph IDs.
Each tile in the font library is an independent glyph. If two tiles have different bitmaps but interpret the same character, one of them is probably a misreading:
Among the 109 groups, only 1 group (composite block tail block) has exactly the same bitmap. After comparing the remaining 108 groups one by one, almost every group has one
It's a completely different word. The misreading is not limited to duplicate rows, so recheck the entire table.

Check method:

1. Extract the font bitmap from ROM resource 0/1 (I4, 504×504 and 504×252; half-width 8×14 corresponds to ID 0–314,
Full-width 14×14 from `0x13B` and resource 1 from `0x597` and
`src/srw64_native/battle_assets.py` of the same set of `font_tile`), cut out each tile by ID;
2. Render all 7,335 CP932 characters with the system Japanese font, and sort each tile by shape: map the characters first and
The leading 1,149 lines were judged to be consistent with the bitmaps (72 lines were randomly selected for manual review, and all were correct);
3. The remaining 602 full-width tiles and all 315 half-width tiles were manually compared and enlarged one by one, and reviewed with the corrected text context
(For example, 1758+1774 reads "twilight", 1504+1845 reads "Jiaozuo", 442+488+441 reads "cow hungry ghost");
Compare the rare characters by parts with the existing characters in the character library (for example, 1318's "evil" to "can" 356, "ge" to "戦" 428,
1919's black pair 434, sell pair + buy 1175);
4. Most sections of the character library are sorted according to Japanese pronunciation (fifty syllables), which can be used as independent circumstantial evidence: 878 Zuo, 879 Zuo fall
"Today's troubled marriage and hatred → Zuo Zuo Cha Cha → Cai Bei", 1401 seal, 1402 right opens the section "Yin right Ao liquid Yin goes to the Netherlands",
1109 Zhi is in "Zhang Yu Town View → Zhi → Shen Zhen", 1200 Father is in "Fu couple Bupu → Father → Fu Fufu",
1094 break is in "団 → break → male talk", 722 pavilion is in "sure comparison → pavilion → xue 楽", 912 video is in "private → video → test",
1516 collapse according to the training reading つい(える) falls into "rent → collapse → stop", the new 1004 tough (ジン), 1562 悛(シュン)
It also happens to fall between "end → ? →図" and "粛 → ? → pure"; the original value of the seed (right, chasing, sister, 対, palace, attribute, embrace)
It cannot be read in these positions. Character names, mental instructions, terrain and other sections as well as supplementary words after several paragraphs are not arranged according to pronunciation.

Result (now 2,020 rows, all `confirmed`):

- Corrected **Line 147**: Line 112 was misrecognized as other Chinese characters (457 闘→ship, 1635 dark→wipe, 912 attribute→sight, 1109 chase→straight, etc.),
Line 24 is a compound block (1815+1816 combined→パーツ, 1923–1953 re-divided, 2047–2049 former→(front),
1478beeの巣→grey), 6 lines are symbols and icons (212 $→±, 217 p→%, 218 _→~, 226 Ⅱ→Ⅲ,
258 f→🔧 Repair wrench, 259 c→Small E), 2 pairs of overall interchangeable (471/878 Zuo↔wei, 879/1402 left↔right),
1 line of variant characters (1920 far → far away, distinguished from the new glyph of 1872).
- Added **84 lines**: tiles with unmapped seeds but visible bitmaps, including half-width `,゛゜#*@©▷◀▶$☆●vxqw`,
Full-width 絵博齢囮Gu Taipin Yinglongqi concubine 撹看dig hard algae 沢沴洴袴恁恁恁狠 all the idiots are still talking about Ning Fei is afraid of spreading the sweat and twisting the snake in need of Shu Xun Ji 聡 accompanying the eyebrows and standing in front of the list of suburbs and the Nuojing Gallery, etc.,
Uncommon characters: Ren(1004), 悂(1562), 歼(1318), 黩(1919), stroked W(1460),
And compound block 1462–1464 `真・天馬翔覇` (1462 is true +・, the structure is the same as 1888 "array・"; 1463 is Tian + horse;
The left half of 1464 is compressed Xiang, and the right half is compressed Ba, which corresponds to 1453 and 1166 part by part).
- Each line `note` begins with `bitmap-corrected`, `bitmap-identified`, or `bitmap-checked`, recording the original value and evidence.
- Impact: Compared with the upstream seed, the decoding results of 3,908 out of 51,174 ROM texts are different, and a total of 5,851 glyph readings are different.
(Including new tiles and re-segmentation of composite blocks); the highest frequency is 457 "ships" at 1,081 locations (advance fleet/departure warship selection/対车ミサイル).

`FUN_8008d1d8` records the **ASCII characters entered by the game** rather than the tile content: the code `'p'`→217, `'$'`→212,
`'_'`→218, like `'('`→224, is a substitute; the actual drawings of these three tiles are `%`, `±`, and `～`.

#### Glyph scale (`form` column)

The original font has four ratios, and a new `form` column is added to the code table to distinguish them (the loader only reads `glyph_id` and `char`,
The extra columns do not affect decoding):

| form | tiles | quantity | content |
| --- | --- | --- | --- |
| `half` | 8×14 | 270 | Numbers, Latin letters, hiragana, katakana, punctuation |
| `full` | 14×14 | 1,692 | Chinese characters and full-width symbols |
| `compound` | 14×14 | 49 | A composite block that presses two or three characters into one grid to control spacing |
| `icon` | 8×14 or 14×14 | 9 | Non-text icon, replaced by text or symbol |

It is normal for the same character to appear in different scales: Katakana バ has a compressed version in half-width 187 and compound block 1936,
B and P have half-width letters 12, 26 and circle icons 242, 241. Shooting and grid have full-width Chinese characters 612, 622 and attack type icons 243, 244.
E has the half-width letter 15 and the small E 259 next to the meter, ▶ has the half-width 246, the full-width 576 and the rating bar 291.
There are only 6 sets of repetitions in the same proportion, all of which are true repetitions: Full-width Jun (710/1823), Discussion (1144/1853), Huan (1597/1826)
It is the same character drawn twice in the character library (the difference between the main strokes is only 3, 1, and 26 pixels respectively); the composite block ダブ(1944/1949),
イン) (1937/1940/1943) has exactly the same pixels, and ニン (1946/1951) both have ニン painted on them, but there are remnants of different adjacent characters on the edges.
There is no separate category of "narrow Chinese characters": full-width characters almost always have a main stroke width of 12–14 pixels.
The narrowest one is just the font itself.

Icon (`icon`): 241/242 is the circle Ⓟ (available after moving) and Ⓑ (beam) at the end of the weapon name, 243/244 is before the weapon name
Shooting and grid icons, text avatars P/B/shoot/grid are retained because `src/srw64_native/weapon_traits.py` relies on these
token is the weapon mark; 575 is the MAP weapon icon; 258 (🔧) and 259 (small E) are the marks on both sides of the instrument grid;
219/291 are the spaces and full spaces (▷／▶) of the rating bar.

#### Compound block

1923–1953 are composite blocks that were originally specially cut to control spacing: the entire sequence of special move names was compressed and then cut into several blocks at 14 pixels.
There are often two or three pseudonyms within a block, and there are often pseudonyms across block boundaries. Segmentation rules: cross-border kana pixels are assigned to the main stroke (palette index 1)
The side with the larger number will be the last piece if they are completely equal; each set of splicing results is compared with the text that actually uses it.

| Group | Each piece of content | Used for |
| --- | --- | --- |
| 1815–1816 | パ／ーツ | t00_00517 |
| 1923–1925 | (quantity／グレ／ート) | t00_02609, 02610 |
| 1926–1928 | (グ／レー／ト) | t00_02592, 02613 |
| 1929–1931 | （マ／ジン／ガー） | t00_02607 |
| 1932–1934 | (ミ／ネル／バ) | t00_02608 |
| 1935–1937 | (ビル／バ／イン) | t00_02600 |
| 1938–1940 | (ダ／ンバ／イン) | t00_02611 |
| 1941–1943 | (サ／ーバ／イン) | t00_02612 |
| 1944–1948 | ダブ／ルバー／ニン／グファ／イヤー | t00_02592、02607–02609 |
| 1949–1953 | ダブ／ルライト／ニン／グバ／スター | t00_02593, 02610, 02613 |

(There is also a corresponding "Grid...P" menu text.) The upstream seed's 1945–1953 segmentation has a pseudonym.
(such as ーニ／ング／ファイヤー、ルラ／イト／ニング／バスター), the splicing result happens to be correct;
The 1934 seed is written as `バＸ）`, but the tiles only draw バ, ゛ and ), and the game actually displays "(ミネルバ)",
There is no X in the machine name MireraX. The remaining compound blocks are Chinese characters compressed in pairs: 1454–1456 锔 dance/reappearance/江湖,
1457–1459 School/Eastern/Undefeated, 1462–1464 Zhen・/Tianma/Xiangba, 1886–1888 Mantuo/Rayen/Zhen・,
Also 632 capabilities, 2047–2049 (front) (middle) (rear).

#### Unmapped graphics

That leaves only 257 (like Д, unused text) and instrumentation 260–272, decoded as `<G:…>`. 260–270 are the same vertical bar shape
11 levels of filling (the palette index changes colors line by line from bottom to top, 260 is empty, 270 is full), 271/272 is the two-color version without stroke.
They only appear in the 46 single-cell texts t00_05104–05149: optional 258 before the bar (🔧 Repair wrench),
After the bar, you can choose 259 (small E), 11 levels × 4 combinations, plus one each of 271 and 272. Wrench with E hint and repair,
EN is related, but the specific interface has not been confirmed by operation.

The native font is HarmonyOS Sans 2.040 (the original files and protocols in Huawei's official package are placed in `content/fonts/`, the license allows redistribution with the software as it is, and is not allowed to be distributed or modified separately; `tools/content/prepare_fonts.py` is checked by hash and put into the application package) and the symbol font in the warehouse is `content/fonts/SRW64Symbols.ttf`, and the button icon font is `content/fonts/SRW64Prompts.ttf` (Yukari Adaptation of PromptFont by "Shinmera" Hafner, SIL OFL 1.1, licensed and documented in `content/fonts/LICENSE-SRW64Prompts.txt`, generated by `tools/content/build_prompt_font.py` from PromptFont with Zelda64Recomp). The official package comes from [Huawei Developer Design Resource Page](https://developer.huawei.com/consumer/cn/design/resource/), the local copy is placed in `assets/fonts/HarmonyOS-Sans-2.040.zip`, and SHA-256 is recorded in `content/fonts/harmonyos-sans.json`.

## Libretro Core

The native SRAM comparison tool uses the core report submission `98c1b0d` corresponding to the source code review aggregate save area layout:
[libretro_memory.h](https://github.com/libretro/mupen64plus-libretro-nx/blob/98c1b0d/libretro/libretro_memory.h)
and [sram.c](https://github.com/libretro/mupen64plus-libretro-nx/blob/98c1b0d/mupen64plus-core/src/device/cart/sram.c).
The local copy is located at `build/recomp/reference-sram-source/`, and the SHA-256 of the two files are
`4d89673af5424d31b391e6afcdaeaaca9fcf73d062637d32c9090906a428582e`
and `609e1b94dd03384128c579abf0a90faeefea8c1f8a095f65a80a7cd68bdbe0fb`.
The tool also locks the full SHA-256 and runtime aggregate save sizes of the accepted cores listed below, before and after importing
Verify that non-SRAM bytes have not changed. The source code review and the actual file reading results of the reference simulator are kept separately.

- Core: Mupen64Plus-Next arm64;
- Acquisition date: 2026-08-02;
- Source: `https://buildbot.libretro.com/nightly/apple/osx/arm64/latest/mupen64plus_next_libretro.dylib.zip`;
- dylib SHA-256:
`8cd7541261b06b89c18189d7621b825e4e6f906b64f4449056a40d0647a6f58d`;
- Local location: `build/libretro/cores/mupen64plus_next_libretro.dylib`.

The `latest` address will drift; any different hashes should be revalidated as a new runtime environment and cannot be inherited
Current screenshot or archived conclusion.

## Recomp tools and reference runtimes

Fixed inputs see `config/recomp/toolchain.json` and `config/recomp/requirements.lock`,
Source clones, generated code, and binaries are located in ignored `build/recomp/`.

| Input | Fixed commit/version | Current usage |
| --- | --- | --- |
| [N64Recomp / RSPRecomp](https://github.com/N64Recomp/N64Recomp) | `ffb39cdad1da5de07eaaa48bd1db4a89a7986771` | MIPS CPU and RSP code generation; recursive dependencies fixed by parent commit |
| [n64sym](https://github.com/shygoo/n64sym) | `ccf4600f3389f1a84bde23339225cf372fdf7712` | libultra signature candidate; not directly considered a confirmed system binding. The output of this ROM (`n64sym rom.z64 -s -f splat`) is stored as `config/recomp/n64sym-symbols.txt`, and the build is no longer generated on-site |
| [N64ModernRuntime](https://github.com/N64Recomp/N64ModernRuntime) | `cdf5abbd5026fef5c364c676e4667c45e42b6863` | A complete static runtime library has been built, connected to the CPU diagnostic host and RSP audio task |
| [spimdisasm](https://github.com/Decompollaborate/spimdisasm) | `1.42.4` | Segmented disassembly and function candidates |
| [splat](https://github.com/ethteck/splat) | `splat64==0.50.0` | Prepared segmentation tool, the current scan does not rely on its export |
| [RT64](https://github.com/rt64/rt64) | `43373749dac9bbc1b653e6a02aed40a9e1783bed` | Actual Metal rendering and GPU framebuffer readback; recursive dependencies fixed by parent commit |
| [Zelda64Recomp](https://github.com/Zelda64Recomp/Zelda64Recomp) | `1a9c26613c6e0906140dc8bcca7362cbe00bf1eb` | Read the reference source code for host window and RT64 interface usage |

N64ModernRuntime's own N64Recomp submodule is
`81213c1831fab2521a6a5459c67b63437d67e253`, recursive dependencies have been initialized and compiled.
This version is checked byte by byte before the host is built to be the same as the standalone generator's `recomp.h` to verify the context and
The interface of the helpers; this does not mean that all internal interfaces of the two submissions are the same.
The `compiled` status of bootstrap means that the analysis tool has been compiled, not that the game host has been compiled.

Graphics dependencies are prepared separately by `tools/recomp/toolchain/prepare_rt64.py`. The Plume submodule is fixed in
`d890ac899e505fb30040e037a4037cdeca68f033`. The current machine only has Command Line Tools,
There is no offline Metal compiler; experiments use optional MSL source code embedding, through the Metal runtime
The source code compilation interface loads the same SPIRV-Cross output. The backend's original internal shaders also use this interface.
The two source code adaptations are in ignored clones, and each preparation checks the original content, fixed commits, and change scope,
Record `build/recomp/graphics-source-patches.json`; the warehouse saves the adaptation script. Plume's
`CocoaWindow` delivers the block that reads the window size from the rendering thread to the main queue, and the original block captures it directly
`this`; Release the swap chain in the graphics thread when RT64 ends, and run SDL's `Cocoa_VideoQuit` again when exiting
In the main loop, the residual block reads the released object and crashes (occurred when exiting after adjusting the window size). patch let
The block shares a survival mark and returns directly after the window is destructed. Also in this project
CMake adds the declaration header file of `labs` for the fixed hlsl++ version.

GPU images are generated by the host using RT64's draw hook, Metal texture-to-buffer blit and completion callbacks
Read back and write out, without relying on the system desktop screenshot permission. The output represents actual GPU results and must still be checked for correctness
Corresponding scenes and reference terminals cannot be inferred from the existence of pictures that the entire set of games has passed.

Reference ares v148 executable located at `/Applications/ares.app/Contents/MacOS/ares`,
This time SHA-256 is
`7a49f00f96a691458461d7c9cf453d95c0f5c054389bbd87c253987b8b6fa345`.
Runtime capture records ROM, ares, session and memory identities simultaneously. See the results and their boundaries
[recomp-progress.md](../design/recomp-progress.md).

## Shared UI dependencies (2026-09-20)

Default game UI and optional name page prototype using [RecompFrontend](https://github.com/N64Recomp/RecompFrontend)
Commit `b1a1477c6556aeb7ed45defbfb5924f721efebc1`, where the RmlUi submodule is fixed to
`7a06f27db04fe5d13a5dacc19b2b4544673a4eca`. independent lock view
`config/recomp/frontend.json`, for implementation scope and verification, see [Shared Game Interface](../native/shared-game-ui.md) and [Name Page Prototype](../native/shared-name-page-probe.md).
Only reuse its UI renderer and RmlUi, and record the SHA-256 of the original renderer and adaptation header files when preparing;
Do not update existing RT64/N64ModernRuntime, do not submit dependent source code, fonts or generate shaders.
Runtime FreeType comes from a development environment; this is not a release build with a full dependency/font licensing list.