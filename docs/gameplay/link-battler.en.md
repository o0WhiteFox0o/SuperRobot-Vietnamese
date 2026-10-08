> **Language / Ngôn ngữ:** [English](link-battler.en.md) · [Tiếng Việt](link-battler.vi.md) · [中文](link-battler.md)

# Link Battler linkage: F91, ゴーショーグン, ザンボット3 How to open

2026-09-19. This article is based on the locked Japanese version Rev 0 `rom.z64` for static analysis: GB Pak driver layer of resident code, preparation screen overlay `load_0008F4B0` (ROM `0x8F4B0`, VRAM `801C4500`; table ROM offset = VRAM − `0x801C4500` + `0x8F4B0`), and Scripts and deployment records for scenes 109–122 in `assets/original-data/records`. Community data comparison [Akurasu Wiki: Link Battler Units][wiki] (retrieved on the same day). **No game has been run this round, and there are no Link Battler cartridges or archives to compare to**. Items that require running to be finalized are listed in Section 8.

## 1. Conclusion Summary

| Conclusion | Basis |
| --- | --- |
| There is no "unlock mark" in the game. What linkage does is **change the next level into an insertion level**: the original next level is stored in `8010F5F2`, `8010F5F0` is changed to a linkage level; after completing the linkage level, the script uses `3D4B 500` to return to the original next level | `801D9F80`; the end event of scenes 109–122 |
| The open units are determined **according to the work**, with a total of 3 positions: F91 series (position 1), ゴーショーグン (position 2), and ザンボット3 (position 4). Each of the 7 combinations corresponds to a linkage level, and each linkage level has two versions (based on whether the next level is selected in the universe, it is inferred to be the ground version and the space version), with a total of 14 scenes | Table `D_801DCABC` |
| For a work to be open, it must meet the following requirements: 64 There is no body of the work here yet; there is one of the body or the protagonist pilot position of the work in the GB archive | `801D9F80` |
| The linkage level appears with our deployment: F91＋シーブック、ビギナ・ギナ＋セシリー；ゴーショーグン＋ Shingo; Sagittarius + Katsuhira, Sagittarius + Universe Tai, Sagittarius + Kaizi (the opening combination is Sagittarius 3) | Deployment Group 1 for Scenarios 109–122 |
| Progress variables var48 (F91), var49 (ゴーショーグン), var50 (ザンボット3) are written as 0 at the end of the linkage level, and then the 23 events in the main line only use them to add a dialogue of the added character | `3E13 48/49/50,0`; read point of `3E03`/`3E02` |
| The same linkage will also do two things: take the larger pilot experience value on both sides ("level alignment"); write the 12 pilots and 18 units of 64 into the GB archive | `801D975C`, `801D992C`; `801D9B54`, `801D9D70` |

## 2. Process

1. Select the linkage item on the maintenance screen and confirm (`load_0008F4B0:801CE318` branch, screen status 8). First clear the 4 KB buffer (`801D9300`), and then call `801D93C4` to check the cassette. Only when 0 is returned does it enter the linkage screen, otherwise it will enter the error screen (status `0x16`).
2. Linked screen initialization (`801D6FF4`) calls the main process `801D5B10`:
1. `801D9544`: Read the GB data block and verify it (section 3), and then use `801D975C` to list the drivers on both sides;
2. `801D9B54`/`801D9CF4`, `801D9D70`/`801D9ECC`: Register the pilots and aircraft that are available in 64 but not in GB into the data block. As long as there are new additions, they will be written back to the cassette by `801D966C` (Section 6);
3. Read the data block again;
4. `801D9F80`: Determine which works should be opened and rewrite the next level (section 4);
5. List of total drivers in descending order of rank, 7 per page.
3. The player confirms the level alignment in the list (`801D70FC` → `801D62D0` → `801D966C`), and the alignment result is written back to the cassette (Section 6).

Step 2.4 does not depend on step 3: as long as the card reading is successful, the next level has been modified in the memory, and it does not matter whether the subsequent level alignment is done or not.

## 3. Cassette identification and data block

**Cassette identification** (resident `80090F44` → `osGbpakInit`, `osGbpakReadId`; `800910C4` comparison): The 16 bytes of the card header area must be equal to `S ROBOT LB\0AL6J\x80` (title, product code `AL6J`, CGB logo `0x80`), the two bytes of the manufacturer code must be `44 39` (ASCII "D9"). The expected value is stored in the resident data `800C69E0`.

Return value of `801D93C4`:

| Value | Meaning |
| --- | --- |
| 0 | Is Link Battler |
| 1 | The card head does not match (not Link Battler) |
| 2 | Other Pak errors (such as Transfer Pak not inserted) |
| 3 | Pak is there, but GB cartridge is not inserted (`osGbpakInit` returns 12) |
| 5 | Communication failed (return 4) |

The meanings of 2, 3, and 5 are inferred from the PFS error constants of libultra and are not compared with the error screen text.

**SRAM access**: Resident `80091120` first writes `0x01` to GB address `0x6000`, then writes `0x0A` to `0x0000` (open the cassette RAM). `80091284(读/写, 线性地址, 缓冲, 长度)` splits the linear address into RAM bank (address >> 13, write `0x4000` to toggle) and `0xA000` offset within the window, read and write in 8 KB segments. The linkage fixes the input linear address `0xA000` and length `0x1000`, which is the 4 KB at the beginning of bank 5. The actual SRAM capacity of Link Battler has not been checked, and how the bank number is wrapped on the cartridge has not been confirmed.

**Data block format** (buffer `801DDAA0`):

| Offset | Content | User |
| --- | --- | --- |
| `+0x000` | Magic number `ROBOT_TAISENN_GB` (16 bytes) | `801DAEAC` Check |
| `+0x010` | 64 → GB driver bitmap (12 bits) | `801D9CF4` Write |
| `+0x018` | 64 → GB body bitmap (22 bits) | `801D9ECC` write |
| `+0x020` | Driver bitmap held by GB (92 bits, corresponding to character number 64 according to table `D_801DCB90`) | Level alignment, open determination |
| `+0x02D` and above | Body bitmap held by GB | Open judgment, `801D9D70` |
| `+0x138 + 2i` | GB The experience value of the i-th driver, u16 little endian | Level alignment |
| `+0x9B9` | Magic number `LINK_BATTLER_V00` (16 bytes) | `801DAEAC` Check |
| `+0x9C9` | Sum of first `0x9C9` bytes, u16 little endian | Calculated from `801D98EC` before writing back |

When reading, only the first and last two magic numbers are checked, and the checksum is not checked.

## 4. Open determination: `801D9F80`

1. **Inherit the scheduled linkage**: If `8010F5F0` is already one of 109-122 (linked before this adjustment), first merge the corresponding work position of the scene into this result.
2. **64 existing works**: Scan our machine instance table `8016A210` (140 × 0x54), the machine number is 42 F91 or 289 ビギナ・ギナ → F91 series; 184 ゴーショーグン, 206ザンボット3 The same principle applies. Existing works are no longer checked against GB.
3. **GB Conditions**: For works that do not exist yet, if any of the following bits is 1, they are open:

| Works | Bits | GB body bits (from `+0x2D`, byte/mask) | GB driver bits (from `+0x20`) |
| --- | --- | --- | --- |
| F91 series | 1 | 3／`0x10`, 16／`0x02` | 23rd place シーブック, 80th place セシリー |
| ゴーショーグン | 2 | 11／`0x40` | No. 55 Shingo |
| ザンボット3 | 4 | 12／`0x08` | No. 59 Shengping |

The driver's seat is confirmed by table `D_801DCB90` to correspond to roles 41, 230, 133, and 152 of 64. The two body positions of the F91 series are inferred to be F91 and ビギナ・ギナ based on their structure. The body number of the Link Battler has not been verified. The constant is in `D_801DCD04..D_801DCD13`.

4. **Rewrite next level**: When the result is not 0, if the old linkage level is not used in step 1, first save `8010F5F0` to `8010F5F2`; then press `D_801DCABC` to select the scene and write it into `8010F5F0`:

| Work position | Scene | Title |
| --- | --- | --- |
| 1 | 109／110 | F91発jin |
| 2 | 111／112 | ゴーショーグン発jinせよ! |
| 4 | 113／114 | Steady 3 appears! |
| 1+2 | 115/116 | Convergence |
| 1+4 | 117／118 | Convergence |
| 2+4 | 119／120 | 2つの大きな力 |
| 1+2+4 | 121／122 | 新しきcomrade |

Whether to choose the previous or the latter one is determined by `801D9F1C`: if the original next level (`8010F5F2` is taken when it is already in the linkage level) is among the 52 scenes in the table `D_801DCAD8`, the latter one will be used. These 52 scenes range from "Pseudo Peace", "Geki Ka! Rareland" to "Decisive Space Domain (Part 2)". According to the title, they are all in the universe. The former version uses map 52, the latter uses map 114, and the world map ends at locations 117 and 122 respectively. Therefore, it is inferred that the former one is the ground version and the latter one is the space version, and the terrain has not been confirmed on the actual machine.

For multiple linkages in the same preparation, the work points will only be accumulated, and `8010F5F2` will always be reserved for the next level before the first linkage.

## 5. Linkage and follow-up

Scenes 109–122 share 7 sets of scripts (one for each pair) with the same structure:

- **Opening**: Select the starting point and end point of the world map according to the current scene index; switch to the battlefield after the conversation with the newly added character; the victory and defeat conditions are `3D65 17,41`; deploy enemy group 0, and then deploy our group 1. The version with Gatorade finally executes `3D5C 152,1`, which combines Katsuhira's Gatorade.
- **Defeat**: The game ends when newly added characters such as Seiko (41), Seiko (230), and Shingo (133) are defeated (type 2 trigger).
- **Victory**: All enemies destroyed → `3D4A`.
- **End**: Write `var48`/`var49`/`var50` = 0 for the participating works, then execute `3D4B 500` and restore the original next level from `8010F5F2`.

The only places where the main line reads these three variables are `3E03 变量,0`/`3E02 变量,0` conditional dialogues, such as "The sound of the universe", "Dream, come again", "Life, Sanって", etc.; at the end of "Dream, come again", Nana will speak one of the 7 lines according to the combination of the three. None of the three variables control joining the team, which is completed by our deployment through the linkage level.

## 6. Bidirectional data exchange

**Level Alignment** (`801D975C` list, `801D992C` execution): For each bit in the GB driver bitmap, press `D_801DCB90` to find the same character in our driver table `80172F40` (100 × 0x4C). There are two pairs of aliases in the table: 36 アムロ also matches 262, and 96 ミリアルド also matches 286 ゼクス. The comparison is the experience value of the driver `+0x12`:

- GB lower → write a value of 64 into the data block;
- 64 is lower → The experience of 64 is changed to the value of GB, the level `+5` is changed to the value pre-calculated on the linkage screen, and then the ability is recalculated by `800A7F8C`. Teammates of the combined machine plus the same experience difference will be converted into levels according to the new experience by `800A630C`. The teammate grouping is shown in the table `D_801DCA88`: Shinobi (Sara, Ryo, Masato), Leopard Horse (Daisuu, Mizu, Kosuke, Ju) 3), Shengping (恵子, Cosmo Tai), Shingo (キリー, レミー), Malino (ローレンス, アイシャ).

`801D62D0` can align only the person where the cursor is, or align in batches according to the list `D_801DD5D0` (ending with `0xFF`); there is no tracking on how to fill in this list. After confirmation, `801D966C` recalculates the checksum and writes it back to the cartridge.

**64 → GB**：

- driver(`D_801DCC48`, 12 Name): アーク, セレイン, ブラッド, マナミ, エルリッヒ, リッシュ, カーツ, デューク, マリア, ひかる, キリカ, ナイーダ;
- Body (`D_801DCC78`, 18 of 22 slots Valid in Taiwan): ソルデファー, アシュクリーフ, ノウルーズ, スヴァンヒルド, ラーズグリーズ、シグルーン、スイームルグ、スイームルグS、アルトロンガンダム、ウイングゼロ、ガンダムサンドロック开、ガンダムデスサイズH、ガンダムヘビーアームズ开、グレンダイザー、真・ゲッター1、アースゲイン、スーパーアースゲイン、ヴァイローズ.

The condition is that 64 exists in our table, but does not exist in GB’s holding bitmap (`+0x20`/`+0x2D`); when satisfied, write `+0x10`/`+0x18`. Skips pilot slots marked with `0x80` and airframe instances marked with `+0xC`. How Link Battler uses these two bitmaps is not included in this ROM.

## 7. Comparison with strategy

| Akurasu's statement | Code |
| --- | --- |
| Purchase the unit in Link Battler, connect it to Transfer Pak, and select linkage on the preparation screen | Consistent. The actual condition is that the GB archive has the corresponding body position ** or ** the protagonist's driver's seat. Either one will bring all the characters and bodies of the work |
| Linkage will make the levels of the drivers on both sides equal | Consistent, the comparison and rewriting are experience points; players need to confirm in the list |
| The next level is a special level "New Comrade" that introduces new units, which will change with the number of openings | Consistent. "New Comrade" is only the title when the three games are complete. The other combinations are F91発jin, ゴーショーグン発jinせよ!, ザンボット3 appears!, Confluence, 2つの大きな力; there are also two versions of ground and space |
| The newly added driver's level is adjusted according to the average force level | The deployment record has a "level offset" field (0/1), and the calculation of the average level is not tracked in this round |
| The BGM and karaoke of these works can be used after unlocking | No tracking for this round |

## 8. Requires running or external data to confirm

- Actual terrain in both ground and space versions.
- The text on the screen when selecting linkage, and the corresponding prompts for error codes 2, 3, and 5.
- 64 "Already owned" here only recognizes the machine number 42/289/184/206. If all these units are sold or leave the team, will they be re-entered into the linkage level if they are linked again? Will the Steady 3 always exist as instance No. 206 during maintenance (instead of the three units after separation).
- Whether the Link Battler save is really in RAM bank 5, and the number of the `+0x2D` body bitmap. These require a Link Battler ROM or save.
- The native host originally did not have a Transfer Pak, and some SI/ContRam routines that `osGbpakInit` depends on have explicit abort traps (`funcs_unsupported.c`) in the generated code. Selecting linkage static view will cause the host to abort. The virtual cartridge of Section 10 replaces the entire driver layer and these routines are no longer called.

`801DA52C..801DAA28` also has a set of card reading, verification, and write-back functions, driven by `801DABE4` via function table `D_801DCB10`. The call or address reference to `801DABE4` cannot be found in the full ROM. It may be a test entry that is not connected and is not included in the process in this article.

## 9. Meaning of M2 (when planning)

M2 corresponding to [native enhancement solution](../design/native-enhancements-plan.md):

- **OPTIONAL CONTENT OPEN MOD**: Required scripts, deployments, maps and dialogues are all in ROM, no dependence on GB of data. In the preparation screen, write `8010F5F2`/`8010F5F0` according to the rules in Section 4, and it will be queued into the linkage level. After that, the original script will complete the addition, write variables and return to the main line. This approach does not involve the Transfer Pak protocol, and there will be no level alignment and 64 → GB writeback.
- **Compatible with original linkage**: The host needs to provide Transfer Pak and simulate `osGbpak*` lower-layer SI reading and writing; the data layer only involves the 4 KB data block in the above table, two magic numbers and the checksum when writing back.

In the end, the approach adopted in Section 10 was to retain the original linkage screen and only replace the card reading with the player's check.

## 10. Processing of native version

Implemented on 2026-09-19, compiled and passed the unit test, and checked the linkage page, original screen and return using the debugging interface on the same day (see the end of this section).

**Process**: Select "リンク" in the maintenance menu → Native linkage page (the layout is the same as the protagonist selection page) → The player selects the work → "Enter linkage" and then runs the original linkage screen (there is a total of driver list, オートリンク) → B Return to the menu. Insert the corresponding linkage level before the next battle, and return to the main line after the battle, which is consistent with the original version. "Return" Press the path of the original B key to return to the preparation menu without changing the next level.

**Linkage page** (`link_page.cpp`, RmlUi page is in `src/native/ui/frontend.cpp`): three work cards, respectively showing the main pilot's big avatar, work name, body and companion pilot's small avatar. ←→ Switch, space/Z or click the card to check, Enter to continue, Esc/X to return. Cards have three states:

| Status | Judgment | Display |
| --- | --- | --- |
| Already added | The variable (48/49/50) is 0, or we have the body of this work | It turns gray and cannot be checked |
| Scheduled | The next level is already a linkage level containing this work | Locked as checked |
| Optional | The rest | Can be checked |

"Joined" looks at one more variable than the original version: the original version only looks at the body. After the body is sold and linked again, it will be re-entered into the linkage level; here, the variable will prevail and will not be added repeatedly. Avatar by `name_assets.py` from ROM The avatar table (according to character number) is solved: シーブック, セシリー, Shingo, キリー, レミー, Shengping, Cosmo Tai, Keiko, among which シーブック and セシリー are 97×97.

**Timing**: The initialization of the linkage screen `801D6FF4` will read the card. The hook does not execute it first, but opens the linkage page, updates `801D70FC` every frame and skips it during the waiting period. After the player confirms, the data block is generated, and then the original initialization is called. When canceling, follow the B key processing of `801D7148`: play the sound effect `0xB8`, write `801DECB8` as 0, and call `80099814(5,1,2)` to transition back to the menu.

**Virtual Cassette** (`link_battler.hpp`, `game_hooks.cpp`): 6 functions of the resident driver are replaced: `80090F44` initialization, `80090FA0` status, `80090FC4` power, `800910C4` card comparison, `80091120` open RAM, all return 0 directly; the reads and writes of `80091284` fall on the 4 KB data block in the host memory. Data block content:

- Two magic numbers at the beginning and end;
- The driver bitmap and experience points mirror the player's own driver (according to the matching rules of `801D975C`, including アムロ, ゼクスalias), so the original list appears as usual, and level alignment will not change anyone;
- For the works that are checked but not added, set their main pilot positions (Shingo 23, Shingo 55, Katsuhira 59), and hand them over to the original version `801D9F80` for judgment and rerouting;
- The four key bits of the work (23, 80, 55, 59) do not participate in mirroring, and the body bitmaps are all 0.

Write back (64 → GB registration, level alignment) only enters this memory and does not write to disk. The diagnostic host without a native interface (`srw64-host`) runs according to the original process, and the data block does not contain any work bits.

**Real machine verification** (2026-09-19, first episode clearance archive, Malino route, Simplified Chinese): Load the file to prepare, select "リンク" and a linkage page will appear. All three games are optional. After checking F91 and ザンボット3, continue, the original "GB リンク" screen appears, listing Wanzhang, シモーヌ, マナミ, N64 and GB both sides have the same level and experience value; the event log `linked` line `next_scene` from 4 becomes 117 ("Confluence" ground version), `story_scene` is 4. B Return to the menu and then enter "リンク", F91 and ザンボット3 display "scheduled", the focus is on ゴーショーグン; Esc returns, return to the maintenance menu and the cursor is still in "リンク", `next_scene` remains 117.

**Linked off real machine verification** (second run on the same day, bounded run with debugging interface and script injection turned on at the same time): Check F91 and ザンボット3, then select "Subject" and enter "Episode 2 "Confluence"" (Scene 117, Map 52 Ground). After the opening dialogue, F91, ビギナ・ギナ and ザンバード/ザンブル/ザンベース appear on our side and merge into ザンボット3 (3 friendly units, 14 enemy units). In our phase, the same `3D4E 3D4A` as the original enemy annihilation event is injected. The battle is skipped, and the original end event takes over. After "…なんとかEndわったようね", the player returns to preparation, and "Episode 2: Convergence,クリア" is displayed. At this time, the linkage page event records `joined=5`, `next_scene=4`, that is, var48 and var50 have been written with 0, and the next level has been restored; the two games on the page display "Joined". "Practice Ability" lists シーブック (F91, Lv4), セシリー (ビギナ・ギナ, L v3), Kappei (ザンボット3), Kokunta (ザンブル) and Keiko (ザンベース), the latter three are all Level 4. "Second Time" enters scene 4, and the opening line is "発多はコロニー国であった...", which is consistent with the script of scene 4. The run exited normally without triggering the abort trap.

**Still to be confirmed by actual machine**: The terrain of the universe version (the latter scene); save and then load the file after scheduling the linkage level, whether `8010F5F2` should be retained; the result of the real battle being completed (rather than injecting victory). Verify available debug interfaces: `srw64ctl wait --link-page`, `status.link_page`, event log `link` (`open`, `confirmed`, `linked`, `back`, each line with `next_scene` and `story_scene`).

[wiki]: https://akurasu.net/wiki/Super_Robot_Wars/64/Link_Battler_Units