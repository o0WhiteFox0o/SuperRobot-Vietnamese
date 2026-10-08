> **Language / Ngôn ngữ:** [English](localization-terms.en.md) · [Tiếng Việt](localization-terms.vi.md) · [中文](localization-terms.md)

# Chineseization of data text: entry list and translation specifications

Date: 2026-09-23. This article explains how to translate "data text" such as names, labels, and system prompts, how to enter the language directory, and the unified translation specifications for Chinese (`zh-Hans`) and English (`en`). Lines do not go here: Combat lines (approximately 5799–17346), plot dialogue, and selected limbs (from 17347) are placed in independent plain text files. Players can modify them one by one, see [Line Text File](../guide/dialogue-text.md); there is a separate process for their machine translation drafts, and the translations are subject to the entry list of this article.

## Why use a word list?

The first 5,650 entries in the text table `base:t00` are names and interface text: terrain, title of work, level title, body, pilot, weapon, mental command, special abilities and skills, enhancement program, inter-field screen labels and prompts, as well as name input prompts, character list, counterattack command instructions, victory or defeat conditions, and damage levels. The same Japanese original text will be repeated in many records (one for each machine body with the same name weapon, one for each form of the same pilot), and the weapon list text (`格ビームサーベルP`) is a combination of "mark + weapon name + mark". Line-by-line translation is both repetitive and prone to inconsistency.

So there is a list of entries for each language `content/locales/terms/<locale>.json`: "Japanese original text → translation" is listed by partition, and each different original text is only translated once. `content/locales/terms/sections.json` specifies the record range corresponding to each partition. `tools/content/apply_terms.py` expands the entry table into ordinary entries with `source_sha256` (labeled `"origin": "terms"`) in the language directory. Runtime and the C++ first importer still read only entries, and there is no need to know the entry table.

- The weapon list (`weapon_menus` partition) is not translated separately: the translation from the `weapons` partition is spelled out according to the original syntax - `格`/`射` prefixes, translations, `P`/`B`/`MAP` suffixes remain unchanged. These letters are just placeholders: the original drawings use the special icon glyphs (241–244, 575) in the font library, and the native weapon tables also draw these original icons, regardless of language. For weapons whose original name ends in `MAP` (`ファンネルMAP`), the translation must also end in `MAP`.
- The partition marked `complete` requires that each original text containing Japanese text has a translation; `models` (airframe model) only translates non-model text such as `飛行試作型MA`.
- When the corresponding record cannot be found for the original text in the entry table (the original text is misspelled or the partition is misplaced), the tool reports "unused".
- Entries and handwritten entries cannot cover the same record; the original 73 handwritten translations in the data area have been moved to the entry table, and the 93 handwritten dialogues of the first episode have been moved to the line text file. Now only the entry entries are left in the language directory.

```sh
PYTHONPATH=src .venv/bin/python tools/content/apply_terms.py            # 改完词条表后重写语言目录
PYTHONPATH=src .venv/bin/python tools/content/apply_terms.py --check    # 只检查，目录过期时失败
PYTHONPATH=src .venv/bin/python tools/content/apply_terms.py --missing  # 列出 complete 分区还缺的原文
```

`tests/test_terms.py` Check that the partitions of the Chinese and English entry tables are consistent with the original text collection, and the translation remains unchanged. `<G:...>` Parameters and entry entries are all drafts; when ROM is available, also confirm that the language directory is consistent with the expansion results of the entry table.

## Show position and boundaries

- The original page (pre-war confirmation page, each screen between games) retrieves these texts through the language directory, and switches to Chinese or English to display the translation; missing translations fall back to Japanese.
- When switching the interface back to the original version in the settings, the original screen is drawn with the ROM font model and still displays Japanese text; this is the original mode that is intentionally retained.
- The labels in the original tactical map menus, combat animations, and the text baked into the pictures have not yet been integrated into the language directory; their records have been translated and will be available directly when they are integrated.
- Not translated: debug tags (hiragana entries 1179–1369, 4307–4381 for battle animation editor, battle and story flag editor 5644–5798), music titles (232–280), modified scale bars (4145–4267), map icon fonts (5104–5149), name input pads (5220–5239, 5247–5449).

## General specifications

**Chinese (Simplified)**: Use the common translations of mainland players (Gundam, Mazinger Z, Getter), and do not use the Hong Kong and Taiwan translations (Gundam, Magnum, Getter).パイロット is always translated as "pilot" (the deputy パイロット is "secondary pilot"; determined by the user on 2026-09-25, the "pilot" in the lines will be changed at the same time and recorded in `content/translation/renames.json`). Use a spacer `·` (U+00B7) between names; use full-width exclamation marks, question marks, and parentheses. The machine model, `HP`, `EN`, `MAP`, `L1`–`L9`, `S`/`M`/`L` dimensions, etc. remain the same. The popular names take precedence over the official writing: the current translation is the retention of the popular names in mainland China (Camus Bidan, Shiro Wei, Zaku, Dongfang Bubai); when there is no popular name, use the official Simplified Chinese; if there is neither, press the transliteration, and try to use the commonly used names of people. **Do not use Taiwanese and Hong Kong translations** (2026-09-24 user decision): The official Traditional Chinese, Taiwanese version, Taiwanese homophonic name, and Hong Kong version are not used as a basis, only for reference. King of Thunder is an exception confirmed by users: the one broadcast in mainland China in 1994-95 was the Taiwanese version, and there is no official version from Station B; only the work name and machine name are retained, and the names and moves of the Taiwanese version will be reviewed separately.

**English**: Give priority to official writing: Bandai Namco official English version (Super Robot Wars V/X/T/30), Gundam official English website, official English release (Discotek, etc.) and official cards; if not, follow the popular Roman characters and English circle conventions (Hepburn, long sounds without symbols: `Koji Kabuto`). Keep labels as short as possible: the native page column width is designed according to Japanese, and overly long text will be cut off.

**Both languages**: Keep the information of the original text without explanation; keep the numbers, `+`, `%` in the original text; two or more consecutive spaces in the original text are placeholders for filling in numbers (`第  話`, `(最大で  段階まで)`, `あと  機`, `命中率    %`), the native page replaces the first double space with a number, and the translation must keep these spaces as they are (`第  话`, `(最多  段)`, `Stage  `); in multi-line prompts The position of `<BR>` can be adjusted.

## Title of work

| Original | Chinese | English |
| --- | --- | --- |
| Mobile Suit Gundam | Mobile Suit Gundam |
| The 08th MS Team | The 08th MS Team | The 08th MS Team |
| Mobile Suit Gundam 0083 | Mobile Suit Gundam 0083 |
| Mobile Suit Zeta Gundam | Mobile Suit Zeta Gundam |
| Mobile Suit Gundam ZZ | Mobile Suit Gundam ZZ |
|Char's Counterattack | Char's Counterattack |
| Mobile Suit Gundam F91 | Mobile Suit Gundam F91 | Mobile Suit Gundam F91 |
| Mobile Fighter G Gundam | Mobile Fighter G Gundam |
| New Mobile Suit Gundam Wing | New Mobile Suit Gundam Wing |
| Mazinger Z | Mazinger Z |
| グレートマジンガー | Great Mazinger |
| UFO Robot Grendizer | UFO Robot Grendizer |
| Getter Robo / Getter Robo G | Getter Robo / Getter Robo G |
| Super Electromagnetic Robot Combattler V | Super Electromagnetic Robot Combattler V |
| Invincible Super Man Zambot 3 | Invincible Super Man Zambot 3 |
| Invincible Steel Man Titan 3 | Invincible Steel Man Titan 3 |
| Sengoku Majin GoShogun | Sengoku Majin GoShogun | Sengoku Majin GoShogun |
| Holy Warrior Dunbine | Holy Warrior Dunbine | Aura Battler Dunbine |
| Dancouga: Super Beast Machine God | Dancouga: Super Beast Machine God |
| Blue Comet SPT Layzner | Blue Comet SPT Layzner |
| Six God Combination God Mars | Six God Combination Thunder King | Six God Combination God Mars |
| ジャイアント・ロボ | Giant Robo |
| オリジナル | Original | Original |

## Commonly used word formations

The same word formation remains consistent in the machine name, weapon name, ability name and level title.

| Original | Chinese | English |
| --- | --- | --- |
| ガンダム | Gundam | Gundam |
| マジンガー | 魔神 | Mazinger |
| ゲッター | Getter | Getter |
| オーラ | Aura | Aura |
| ビーム | Beam |
| Mega Particle Cannon | Mega Particle Cannon |
| ビームサーベル | Beam Saber | Beam Saber |
| ビームライフル | Beam Rifle | Beam Rifle |
| Vulcan | Vulcan |
| ミサイル | Missile | Missile |
| ファンネル | Floating Cannon | Funnel |
| ドリル | Drill | Drill |
| ロケットパンチ | Rocket Punch | Rocket Punch |
| Photon Force ビーム | Photon Force Ray | Photon Beam |
| ブレストファイヤー | Breast Fire |
| Tomahawk | Tomahawk |
| ミノフスキー | Minovsky | Minovsky |
| Iフィールド | I force field | I-Field |
| Super Alloy Z／Super Alloy NiニューZ | Super Alloy Z／New Super Alloy Z | Super Alloy Z / Super Alloy New Z |

## Main characters

| Original | Chinese | English |
| --- | --- | --- |
| アムロ・レイ | Amuro Ray | Amuro Ray |
| シャア・アズナブル | Char Aznable | Char Aznable |
| カミーユ・ビダン | Kamille Bidan | Kamille Bidan |
| ジュドー・アーシタ | Judau Ashta |
| ドモン・カッシュ | Domon Kasshu | Domon Kasshu |
| ヒイロ・ユイ | Heero Yuy | Heero Yuy |
| Koji Kabuto | Koji Kabuto |
| 剣鉄也 | 剑 Tetsuya | Tetsuya Tsurugi |
| Ryoma Nagare | Ryoma Nagare |
| Hyoma Aoi | Hyoma Aoi |
| 神胜平 | 神胜平 | Kappei Jin |
|Banjo Haran |Banjo Haran|
| ショウ・ザマ | Zama Sho | Show Zama |
| Shinobu Fujiwara | Shinobu Fujiwara |
| Myojin タケル | Myojin Wu | Takeru Myojin |
| Daisaku Kusama | Daisaku Kusama | Daisaku Kusama |

The default name of the original character uses the same translated name as the same character in the pilot list (for example, Manami Hamill). The `default_names` partition (records 487–502) is also the data source for the default name trilingual display in the game. The first name and last name are separated from the full name according to the separator, see [Default name trilingual display](default-names.md).

## Display access and project backlog (2026-09-23 inventory)

All original text goes through the resident text engine: `8008D0E8`/`8008D140` single-line tag pool (60 slots, `0x8015CB00`), `8008C9C0` body text pool (`0x800FBAB0`), `8008C88C` number pool, drawn every frame by `8008DC40`. The word-retrieval function `8008CF14` only reads text table 0, and replaces the name records of the protagonist and partner with the memory names. There are only two ways to go through the language directory: dialogue adapter (plot dialogue; display-only battle lines will be added from 2026-09-23), and native RmlUi pages (inter-scene screens, pre-battle pages, name pages, linkage pages, settings).

Fixed (`cb86e82`, `27b221e`): The native page displays the default name instead of the name entered by the player, the dialogue speaker is not translated, the name is not refreshed after switching languages on the inter-scene page, the weapon confirmation page and full modification reward display marked menu name, the machine name of the refund prompt, and the battle lines. 2026-09-23 Real machine verification using `tools/recomp/debug/check_localization.py`: All the screens in the first episode of the clearance file passed all checks in Chinese and English, including switching languages ​​when opening, the protagonist's name being consistent in three languages, weapon confirmation pages and F5 reloading error reports; `battle` mode confirms that the lines are natively redrawn and the speaker has been translated during battle. The transfer screen cannot be accessed in this archive (too few drivers) and is not covered. (From 2026-09-27, the default name is displayed according to language, and the "Protagonist's name is consistent in three languages" item is changed to check that the default name changes with the language.)

To-do, in order of priority:

1. **Native page layout**:
- The fragments spliced in Japanese word order have been changed to interface templates with `{name}`: full modification rewards, fairy rides, archive media, Pak prompts, and inter-game footers.
- Change the double space number placeholder to `{n}` template. English currently displays `Stage12`.
- ~~RmlUi loads fonts by language~~: Starting from 2026-09-23, the packaged HarmonyOS Sans (`3beb303`) will be used in Chinese, English and Japanese, and system fonts such as Hiragino and Arial Unicode will no longer be used; there is no bold font weight.
- Change the width to actual measurement, and add the minimum font size and ellipses. There are several labels on the driver ability page that overlap with values.
- ~~Weapon mark badges are changed to use mark id and interface copy~~: 2026-09-24 Change to draw the original icon directly, the same in each language, see [Modification Screen](native-upgrade-screens.md).
- The skill names on the pre-battle page and ability page are unified from the same source.
2. **Select limb window and combat target window**: The same `8008F648` is used, the difference is that there is no name box and cursor.
3. **Original interface of tactical map**: command menu, status/ability page, spirit list and description, troop table, counterattack order, sortie selection. 2026-09-25 The universal overlay has been completed: the labels, numbers and text outside the dialogue box of the two lines of text (`8008DC40`, `8008EB5C`) are redrawn according to the native reading language, see [original interface text](native-ui-text.md). Frequently viewed status pages can still be made into native pages in the future.
4. **Picture text**: opening zoom text (translated), chapter title card, stage banner, battle special effects text. It can be rearranged with native text, or replaced with language-prepared images, and the entire image replacement sharing mechanism in HD planning.
5. **Toolchain**:
- Add review marks to the entry list. Before changing the format, inform the script machine which way to translate it.
- The consumer list of the coverage report is changed to a real "text coverage ledger".
- ~~The import specification after merging the lines is too large~~: It has been changed so that the lines are not entered into the language directory and an independent [Line text file](../guide/dialogue-text.md) is used instead. The embedded import specification still only has the name and interface text (about 1.7 MB).
6. ~~**To be determined**: The Chinese default name is not in the ROM character set. It cannot be input as a name now, and the translation of the default name is never displayed~~: 2026-09-27 It is determined that no name change is allowed. Only the original glyph is stored in the name area. The default name is changed to the reading language when displayed. See [Default name trilingual display](default-names.md).

## The first batch of translations (2026-09-23)

All 2,433 original texts in 31 partitions have Chinese and English translations, which are expanded to 4,674 records in each language; `--missing` and `unused` are both 0.

2026-09-29 Added `songs` partition (records 232–280, track names in music appreciation and karaoke modes): Deck During video inspection, it was found that the Chinese track list displayed Japanese song names. 38 Japanese song titles have Chinese-English translations. The original English names such as `FLYING THE SKY` are not translated; the English song titles written in katakana (サイレント・ヴォイス, バーニング・ラブ) also use the original English names in Chinese. Now 32 partitions, 2,471 original texts, 4,712 records per language.

2026-09-30 Withdrawal of track title translation: Users require that song titles in music appreciation and karaoke modes must remain in Japanese. The `songs` partition was changed to `complete: false`, and 38 song titles were deleted from the two entry lists. After expansion, each language returned to 4,674 records, and the track list showed the original text of the ROM. Do not add any additional translations to this paragraph in the future.

The first batch of translations other than those listed above:

- **Spiritual Commands in English** According to T/30, the English version is called: Bullseye, Flash, Vigor, Guts, Wall, Valor, Soul, Faith, Rouse, and Daunt. In Chinese, popular community names such as intuition, perseverance, great perseverance, iron wall, passion, and soul are used. The single-character abbreviation (1149–1178) takes the first letter of the translated name in Chinese, and takes "big" for "great perseverance"; it takes three letters in English, and it explodes as `SD`.
- **Status and Skills**: 気力 in English has been unified to Will, and the original Morale on the pre-war page has been changed. The English version of Holy Warrior is unified as Holy Warrior, and the rules of the original Aura Warrior have been changed. Cut り払い in Chinese means "cut off", strengthen means "strengthen the person", and S defense means "S defense". The handwritten labels on the pre-war page have been unified by terms: Aura Barrier, I Force Field, Planetary Defender, Mach Special, Shadow of God.
- **Hardware and proper names**: コントローラパック is the "handle memory card", 64GB パック is the "64GB transfer card", and シャッフル is unified into the "Shuffle Alliance". The Chinese version of "Eastern Invincible" commonly used in mainland China is the "Supreme Gundam".
- **English MAP weapons** are written as `Buster Rifle MAP`. The spelled out list text will have an extra space before the mark, but it must be retained when split according to the original syntax during runtime, so it cannot be seen on the display.
- **ROM Typos** Do not copy: モンド・アガケ and モンド・アカゲ are both translated as Mondo Agake. The official writing is Agake, and アカゲ in the ROM is a typo (the first batch of アカゲ was translated as Akage, corrected on 2026-09-24).ゲーツ・キャバ and ゲーツ・キャパ are both translated as Gates Capa/Gates Capa.
- The "・" in **Victory and Loss Conditions** has been changed to a comma in Chinese and a semicolon in English. "～の撃波" is written as the neutral "～撃撃／～ destroyed", because the same sentence will appear in both the victory and defeat lists.

## Check official and popular translations (2026-09-24)

The "Text Formatting System Export and Translation Planning" session checked the official and popular translations of each work one by one according to the above specifications. References were made to the official Chinese and English versions of Machine War, GUNDAM.INFO, Discotek, Bilibili, Baidu Encyclopedia, Mengniang Encyclopedia, etc. The original comparison table is in `assets/translation-runs/official-names/` (do not enter git), and the selection principle can be found in `POLICY.md` in the same directory.
- There are 625 entries in total, of which 595 have been studied, and the other 30 are written in sync with the name change in the level name and victory and defeat conditions. The plot name list is maintained by the other party.
- Written into the entry table: 403 values in Chinese and 174 values in English.
- Example:
- Chinese: Hanazono Rei, Zama Sho, Ming Shenwu, Fukamura Rei, Zanbo 3, Thunder King, Big Iron Man (title and body of the work), chest flame, photon force ray;
- English: G Gundam uses the North American name Burning Gundam/Dark Gundam; the original machine uses the official card spelling Sweemurg, Virose, and Razgreez.
- The English translations of the original opponents are Kurtz Forneus, Rish Griswell, and Ehrlich Stasen: the community spelling is a mispronunciation, and Forneus is the name of the devil.
- The names in the text of the lines are replaced by the other party according to the same table, so the speaker in the dialogue box is consistent with the text.

User’s decision (2026-09-24):
- 14 items suspended:
- The homophonic names in the Taiwan version are not used, and the transliterations are retained: Boqiuen, Miuji Poe, Dozdozi, Jinjin;
- アラン retains Alan; ケンジ changes to Kenji, アキラ changes to Hui; ヴェスバー uses VSBR;
- Thunder King retains the title of the work and the name of the machine. It is an exception: the version broadcast in mainland China in 1994-95 was the Taiwanese version, and there was no original version from Station B.
- After that, the other party clicked "No need for Taiwanese translation" to review the entire list and created a web page for the user to select items one by one. The user's choice has been changed to another 65 Chinese values, while the English values ​​remain unchanged. Six of them are level names and victory and defeat conditions that are synchronized with the name change.
- Names: Mako (Marco), Rose (Roger), Kara Suen (Kira Mori), Bran, Reika Sanjo, Tachibana Meili, Tokida Garrison, Quake Soldiers, Commander Otsuka;
- Units: Gondor, Zvas, Laineke, Leprakon, Hound;
- Weapons: Gaia Crush, Dark Finger, Venerable Belt, Roaring Rose, Solar Flash Bomb, Spin Drill, Cosmic Thunder, etc.
- Old changes based on official Traditional Chinese are also decided one by one by users in this round.

## Pending review and unverified

- All translations are drafts (`review_status: draft`). After review, change the entries one by one to `reviewed`: Modify the entry list, re-run `apply_terms.py`, and then mark it in the language directory.
- The following are only tentative: transliterations of original aircraft, enemy aircraft and moves that do not have popular Chinese names, such as アースゲイン Asgain, ヴァルディスキューズ Valdisquez; Layzner's "Seal"; Kong Ming and other names that have only one origin. The verification on 2026-09-24 has been determined as シャインスパーク Flash Explosion, ストナーサンシャイン Sun Flash Bomb (user selected), レイン・ミカムラ Fukamura Rei.
- English long names may be cut off in the native list. The abbreviations used in the list have been shortened from "Dark General" and "Hell Marshal" to Dark General and Hell Marshal, and the full names retain their official translations. The native list will reduce the font size according to the width of the box; the longest English unit name after checking is Super Beast Shishiris Garo/Kiba (26 characters).
- Prompts broken into multiple pieces are spelled out in order to translate, including Pak prompts, counterattack command instructions, full modification rewards and "X が, Y になります". The actual splicing method and line wrapping have not been verified on the screen.
- The Chinese and English actual screenshots of the native page have been generated and checked by `check_localization.py`, see above.
- Plot and battle lines are not within the scope of this article: they are in the line text file, generated by another machine translation process, and the translation is based on the entry table here.