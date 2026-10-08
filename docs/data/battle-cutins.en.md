> **Language / Ngôn ngữ:** [English](battle-cutins.en.md) · [Tiếng Việt](battle-cutins.vi.md) · [中文](battle-cutins.md)

# combat cut-in summary list

2026-09-30 Organized. There are 55 cut-in scenes in the battle performance, all in items 984–1038 of the battle scene registration table (ROM `0x11E3D0`). This article lists what each item draws by move, its size and frame number, and which weapon and how to use it. For the format and decoding, see [Battle Image](battle-graphics.md), and for the rendering mechanism, masking frame, and HD route, see [Battle Performance Rendering Mechanism](../design/battle-animation-rendering.md) §6.3/§7.

The data is read directly from ROM by `read_triplets`, `read_animation_bank`, and `parse_scene` of `battle_graphics.py`; the "Content" column is written based on the exported image (`assets/original-graphics/cutins/`). The meaning of the actor field has only static basis, and there is no actual verification for the "inferred" field.

## 1. Scale

| Item | Quantity |
| --- | --- |
| Registered entries | 55 (984–1038), 46 cited in weapons records and 9 without any citation |
| Album | 27 pictures (1337, 1339–1364): CI8 large atlas 14 pictures (maximum 512×512), CI4 background atlas 13 pictures |
| Frame | 308 frames, including 26 frames of background class |
| Different parts slices | 1736 pieces |
| Weapons used | 14 weapon numbers, actual 10 moves (24/29, 874/881, 1062/1075 are two records of the same move; 18 and 1216 share ドモン close-up) |
| Works involved | G ガンダム（7 weapon number), ダンクーガ, レイズナー, ジャイアントロボ, ゴッドマーズ, コン・バトラーV |

Neither `hit` nor `reaction` reference cut-ins; all cut-ins are in the attacker's weapon record. All scenes are vertex_mode 1 (no mirror vertex groups, the enemy and friend are drawn the same), only 1025/1026 is mode 2.

## 2. The composition of a cut-in

Each segment consists of 2-3 actors stacked up, built in order of actors, and drawn according to node priority:

1. **Background**: 128×96 textures (speed lines, clouds, light strips) on CI4 atlas, 1–3 frames. Usually with h4 high flag `0x8000` or `0x4000`.
2. **Main image**: A close-up of a character/machine in the CI8 large atlas. The canvas is mostly 128×96, and all animations are in the frame (no sliding code).
3. **Overlay**: coat of arms, radiation, silhouette, lightning, etc., h5 is mostly 140–190 (inferred to be translucent, 255 to be opaque).

Actor field: h4 low byte is the trigger phase (`0x44`/`0x50`–`0x57`), `0xFFFF` and the single digit are the sequence numbers in the same segment; behavior 240 is the standard cut-in, 350 is the シャイニング／ゴッドDepartment's opening close-up, 351 is a long horizontal view of Structural Fist, 352 is a small piece with x/y offset (heraldry, logo), 373 is a controlled actor with h6 = 2. The display is scaled 1.29, centered on the screen, and y = 47, so a 128×96 canvas occupies approximately 165×124 screen pixels; an actor with z == 1 will hang a mask `800C6D00` (leaving a 140×120 window).

## 3. Press the move

"Frame/duration" is the total number of ticks in different frames/steps. The dimensions are the bounding box of all frames.

### 3.1 Super electromagnetic スピン (weapon 778, コン・バトラーV)

| Registration | Scene/Album/Palette | Dimensions | Frames/Duration | Behavior | h4 / h5 / z | Content |
| --- | --- | --- | --- | --- | --- | --- |
| 985 | 1406/1342/1372 | 128×96 | 1/1 | 240 | 8053 / 255 / 0 | Background: purple clouds |
| 984 | 1405/1341/1371 | 128×96 | 15／90 | 240 | 53 / 255 / 0 | コン・バトラーV Stance, electrify, fold into a drill and rotate |

h6 = 2 for both actors.

### 3.2 ファイナルゴッドマーズ (Weapon 742, ゴッドマーズ／ガイヤー)

| Registration | Scene/Album/Palette | Dimensions | Frames/Duration | Behavior | h4 / h5 / z | Content |
| --- | --- | --- | --- | --- | --- | --- |
| 988 | 1409/1344/1374 | 128×96 | 2／107 | 240 | 8057 / 255 / 0 | Background: green energy cloud, the second frame is all black |
| 986 | 1407/1343/1373 | 160×144 | 8／107 | 240 | 57 / 255 / 1 | ゴッドマーズ Raising the sword, lightning, close-up of the sword tip |
| 989 | 1410/1343/1373 | 32×32 | 1/107 | 352 | 57 / 255 / 2 | Chest "M" mark, offset (−53, 30) |
| 987 | 1408/1343/1373 | 128×96 | 7／107 | 240 | 50 / 255 / 0 | White slash line and cross flash |

### 3.3 ジャイアントロボ (weapon 820 ロケットバズーカ, 821 ロケットミサイル)

| Registration | Weapons | Scene/Album/Palette | Dimensions | Frames/Duration | Behavior | h4 / h5 / z | Content |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 991 | 821 | 1421/1350/1380 | 128×96 | 1/1 | 240 | 8044 / 255 / 0 | Background: blue oblique speed line |
| 990 | 821 | 1420/1349/1379 | 144×96 | 9／80 | 240 | 44 / 255 / 0 | The missile tube on the shoulder is raised and fired, and the last close-up of the face |
| 994 | 820 | 1424/1350/1380 | 128×96 | 1/1 | 240 | 8052 / 255 / 0 | Background: blue horizontal speed line |
| 992 | 820 | 1422/1349/1379 | 128×104 | 7／54 | 240 | 52 / 255 / 0 | The muzzle of the rocket launcher extends, the last close-up of the face |
| 993 | 820 | 1423/1349/1379 | 72×64 | 6／54 | 240 | 52 / 255 / 0 | Muzzle smoke |

### 3.4 V-MAX (Weapons 1075 レイズナー, 1062 ニューレイズナー)

| Registration | Weapons | Scene/Album/Palette | Dimensions | Frames/Duration | Behavior | h4 / h5 / z | Content |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 997 | Both | 1434/1356/1384 | 128×96 | 2／88 | 240 | 53 / 255 / 0 | Background: dark green vertical lines, the second frame is all white |
| 995 | 1075 | 1432/1355/1383 | 128×96 | 7／88 | 240 | 53 / 255 / 0 | レイズナー head close-up, whole body, turns into blue silhouette |
| 996 | 1075 | 1433/1355/1383 | 128×96 | 6／88 | 240 | 53 / 180 / 0 | Eye yellow light, radiation, light blue silhouette |
| 998 | 1062 | 1435/1355/1383 | 128×96 | 7／88 | 240 | 53 / 255 / 0 | Same as 995, the body is changed to ニューレイズナー |
| 999 | 1062 | 1436/1355/1383 | 128×96 | 6/88 | 240 | 53/180/0 | Same as 996 |

Combat logs for both weapons point the dialogue weapon to 1062.

### 3.5 ドモン opening close-up (shared by weapons 18, 24, 29, 1216)

| Registration | Scene/Album/Palette | Dimensions | Frames/Duration | Behavior | h4 / h5 / z | Content |
| --- | --- | --- | --- | --- | --- | --- |
| 1011 | 1404/1340/1396 | 128×96 | 1/69 | 350 | 2/255/0 | Background: blue vertical line |
| 1009 | 1402/1339/1395 | 128×112 | 8／69 | 350 | 1 / 255 / 0 | ドモン face, raising his right hand to show the back of his hand |
| 1010 | 1403/1339/1395 | 69×66 | 1/69 | 350 | 1 / 150 / 0 | King of Hearts coat of arms on the back of the hand |

The h4 of the three items in weapon 1216 are all 0, and the z of 1010 is 1.

### 3.6 シャイニングフィンガー（Weapon 29 シャイニングガンダム; 24 is a record of the same move without body equipment)

Play 3.5 first, then:

| Registration | Scene/Album/Palette | Dimensions | Frames/Duration | Behavior | h4 / h5 / z | Content |
| --- | --- | --- | --- | --- | --- | --- |
| 1014 | 1429/1353/1397 | 128×96 | 1/22 | 350 | FFFF / 255 / 0 | シャイニングガンダム Face and fist, still |
| 1015 | 1430/1353/1397 | 64×64 | 1/22 | 350 | FFFF / 153 / 1 | Red arc light |
| 1013 | 1428/1354/1398 | 128×96 | 1/65 | 373 | FFFF / 255 / 0 | Background: purple light band |
| 1012 |
| 1016 | 1431/1354/1398 | 128×96 | 1/22 | — | — | All black background, **no quotes** |

### 3.7 Explosive Heat ゴッドフィンガー (Weapon 18, ゴッドガンダム)

Play 3.5 first, then two paragraphs, and finally follow 3.8's three paragraphs of Mingjing Shisui (h4 `4053`/`53`):

| Registration | Scene/Album/Palette | Dimensions | Frames/Duration | Behavior | h4 / h5 / z | Content |
| --- | --- | --- | --- | --- | --- | --- |
| 1007 | 1414/1345/1375 | 128×96 | 1/22 | 350 | FFFF / 255 / 0 | ゴッドガンダム face and fist, still |
| 1008 | 1415/1345/1375 | 64×64 | 1/22 | 350 | FFFF / 153 / 2 | Red arc light |
| 1004 | 1411/1345/1375 | 128×96 | 8／47 | 373 | 0 / 255 / 0 | Palms open, armor unfolded, glowing |
| 1005 | 1412/1345/1375 | 128×96 | 5／47 | 373 | FFFF / 150 / 0 | Red silhouette (flame) |
| 1006 | 1413/1346/1376 | 128×96 | 2/74 | — | — | Background: all black, golden oblique light, **no quotes** |

### 3.8 Mingjing Shisui (weapons 18: Explosive Heat Fist, 19: Stone Breaking Fist)

| Registration | Scene/Album/Palette | Dimensions | Frames/Duration | Behavior | h4 / h5 / z | Content |
| --- | --- | --- | --- | --- | --- | --- |
| 1002 |
| 1000 | 1416/1347/1377 | 128×96 | 11/120 | 240 | 4053 (4044) / 255 / 0 | Golden ドモン gassho, ゴッドガンダム chest, back wings spread |
| 1001 |
| 1003 | 1419/1347/1377 | 64×64 | 1/120 | — | — | Alone coat of arms, **no citation** |

### 3.9 Stone Potion Shocking Fist (Weapon 19, ゴッドガンダム)

After 3.8:

| Registration | Scene/Album/Palette | Dimensions | Frames/Duration | Behavior | h4 / h5 / z | Content |
| --- | --- | --- | --- | --- | --- | --- |
| 1036 | 1453/1364/1392 | 128×96 | 1/28 | 240 | 51 / 255 / 0 | Background: blue and white oblique light rain |
| 1034 | 1451/1363/1391 | 128×96 | 3／28 | 240 | 51 / 255 / 0 | Golden ドモン face, double palm launch |
| 1035 | 1452/1363/1391 | 128×96 | 2／28 | 240 | 51 / 190 / 0 | red halo |

### 3.10 Stone Breaking Sky Fist (Weapon 1216, ゴッドガンダム＋ライジングガンダム)

Play 3.5 first, then:

| Registration | Scene/Album/Palette | Dimensions | Frames/Duration | Behavior | h4 / h5 / z | Content |
| --- | --- | --- | --- | --- | --- | --- |
| 1024 | 1448/1362/1388 | 128×96 | 2／175 | 240 | 54 / 255 / 0 | Background: golden light strip, green star dots |
| 1023 | 1447/1361/1387 | 144×96 | 18／175 | 240 | 54 / 255 / 0 | ドモン and レイン: hugging each other under the white moon, holding hands, and holding hands together |
| 1020 | 1444/1360/1386 | 128×96 | 3/108 | 240 | 56 / 255 / 0 | Background: Orange-green radiating energy |
| 1022 |
| 1021 | 1445/1359/1385 | 64×64 | 1/108 | 352 | 56 / 255 / 3 | King of Hearts Coat of Arms, Offset (20, 17) |
| 1025 | 1449/1361/1387 | 128×96 | 1/1 | — | — | Part fragment of 1023 (mode 2), **no reference** |
| 1026 | 1450/1361/1387 | 128×96 | 1/1 | — | — | Same as above, **no citation** |

### 3.11 Structural Alliance Fist (Weapon 1217, Structural Fist)

| Registration | Scene/Album/Palette | Dimensions | Frames/Duration | Behavior | h4 / h5 / z | Content |
| --- | --- | --- | --- | --- | --- | --- |
| 1031 | 1441/1358/1390 | 128×96 | 1/52 | 351 | 4/255/0 | Background: pale golden light band |
| 1027 | 1437/1357/1389 | 528×96 | 26／52 | 351 | 0 / 255 / 0 | Five golden busts slide in and line up from right to left |
| 1028 | 1438/1357/1389 | 434×51 | 26／52 | 351 | 1 / 140 / 0 | Five red light spots (the coat of arms on the back of each person’s hand) |
| 1029 |
| 1030 | 1440/1358/1390 | 128×96 | 1/98 | — | — | Background light strip (same as picture 1031), **No reference** |
| 1032 | 1442/1357/1389 | 160×168 | 4／37 | — | — | Five coats of arms gathered into one, **No quotation** |
| 1033 | 1443/1358/1390 | 128×96 | 3／37 | — | — | All black, flash, all white, **no quotes** |

1027–1029 are the only scenes that exceed the 140×120 matte window and rely on intra-frame displacement for horizontal movement; these three items are most needed to be seen in real-time in widescreen.

### 3.12 Sky-breaking Light Fang Sword (weapons 874 ダンクーガ and various beast fighters; 881 is a record of the same move without body equipment)

| Registration | Scene/Album/Palette | Dimensions | Frames/Duration | Behavior | h4 / h5 / z | Content |
| --- | --- | --- | --- | --- | --- | --- |
| 1038 | 1426/1352/1382 | 128×96 | 1/90 | 240 | 4044 / 255 / 1 | Background: blue vertical line |
| 1037 | 1425/1351/1381 | 128×120 | 4／90 | 240 | 4044 / 255 / 0 | Ren shouted, and then the eye bars of Sara, Masato, and Ryo were stacked one by one |
| 1017 | 1399/1337/1369 | 112×288 | 14／110 | 240 | 54 / 255 / 1 | The empty sword is drawn from top to bottom, ダンクーガ holds the sword all over |
| 1018 | 1400/1337/1369 | 144×96 | 11／110 | 240 | 54 / 140 / 0 | Orange, magenta energy column and slash arc light |
| 1019 | 1401/1337/1369 | 128×96 | 3／110 | 240 | 54 / 140 / 0 | Blue Lightning |

## 4. 9 items without citations

1003, 1006, 1016, 1025, 1026, 1029, 1030, 1032, 1033. They are all on the same picture album of the cited scene, and are spare or discarded shots of the same move: the Structural Alliance Fist is missing the three shots of "full body palm", "heraldry gathering" and "explosion flash" (1029-1033), and the Ishiba Rural Fist is left with two mode 2 fragments. Behavior routines can also use `801C5700` to change the scene, so "weapon records are not referenced" does not mean "must not appear during runtime" - to confirm, add a read-only probe according to the registration number on `801C3170`.

## 5. Grouping when doing HD

After merging according to the album, there are 13 groups of main pictures + corresponding backgrounds, HD in groups:

| Group | Main Album (CI8) | Background Album (CI4) | Registration Items |
| --- | --- | --- | --- |
| コン・バトラーV | 1341 | 1342 | 984–985 |
| ゴッドマーズ | 1343 | 1344 | 986–989 |
| ジャイアントロボ | 1349 | 1350 | 990–994 |
| レイズナー | 1355 | 1356 | 995–999 |
| ゴッド Ming Jing Shisui | 1347 | 1348 | 1000–1003 |
| ゴッドフィンガー | 1345 | 1346 | 1004–1008 |
| ドモン close-up | 1339 | 1340 | 1009–1011 |
| シャイニングフィンガー | 1353 | 1354 | 1012–1016 |
| ダンクーガ 空剣 | 1337 | — | 1017–1019 |
| ダンクーガ four people | 1351 | 1352 | 1037–1038 |
| Rare Sky Fist | 1359, 1361 | 1360, 1362 | 1020–1026 |
| シャッフル Alliance Boxing | 1357 | 1358 | 1027–1033 |
| Shi Potian Shocking Fist | 1363 | 1364 | 1034–1036 |

- Character close-ups (1000, 1009, 1022, 1023, 1027, 1034, 1037) are the part with the greatest image quality gain. You can use approved HD avatars as identity reference.
- Solid color silhouettes, radial lines, slash lines, and lightning (987, 996/999, 1005, 1018, 1019, 1028, 1035) are flat color blocks, which can be vectorized or directly enlarged without generating a model.
- The 13 background pictures are all 128×96 small textures, and the entire picture is enlarged.
- All vertex_mode 1. There is no concern about the palette effect, and it is suitable for the host to draw the entire frame (Rendering Mechanism Document §7.2); the key is (scene, atlas, palette, frame number), a total of 308 frames.