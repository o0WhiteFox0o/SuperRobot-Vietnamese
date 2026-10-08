> **Language / Ngôn ngữ:** [English](tactical-maps.en.md) · [Tiếng Việt](tactical-maps.vi.md) · [中文](tactical-maps.md)

# Tactical map list and dynamic effects

Date: 2026-09-23. This article lists all tactical maps and their runtime dynamics one by one for [HD Planning §3](../design/hd-pipeline-plan.md#3-战术地图). A description of the mechanism (data format for palette cycling, colony frames, 3D34 swapping) can be found in [HD Asset Inventory §3](hd-asset-inventory.md#3-战术地图的动态效果).

The data is calculated from ROM by [`map_dynamics.py`](../../tools/content/map_dynamics.py) and written to `build/content/map-dynamics.json`; adding the `--markdown` parameter will output the table in Section 6 at the same time.

The two items "Initial Scene" and "3D34 Cut-in" read the self-exported plot directory `assets/original-data`, and the other items only read ROM. The corresponding test is [`test_map_dynamics.py`](../../tests/test_map_dynamics.py). All conclusions come from static analysis, not running games.

"Pixels" refers to the number of pixels of the original image that fall within the cycle color range after the entire map is assembled according to the layout, which is the actual moving area on the screen.

## 1. Overview

- **Scale**: 158 map records, 154 different layouts, sharing 8 topographic atlases:
- 6229 universes, 79 maps;
- 6228 ground, 64 pictures;
- 6230, 6 pictures;
- 6231, 4 pictures;
- 6233, 2 pictures;
- 6232, 6234, 6236, 1 each.
- **Motion**: 104 pictures have visible movement, 54 pictures are purely static.
- **References**: 97 are the initial maps of a certain scene, 37 will be switched in by the plot script 3D34, and 25 have no static references found (Section 5).
- **Single screen map**: 11 maps are only 320×240, which is the size of one screen: 34, 65, 66, 70, 73, 74, 81, 116, 117, 119, 157.

| Dynamic | Number of maps | Description |
| --- | ---: | --- |
| Palette cycle (visible) | 67 | 36 water, 34 other cycles (3 have both water and other cycles) |
| Colony rotation | 39 pictures have examples, total 53 | Another 38 universe maps have colonies opened in the pattern byte, but there are no colonies on the screen |
| 3D34 map replacement | 37 pictures are cut in | comic strip sequence, partial variation, whole map replaced with another map |
| Same layout but change color palette | 3 groups | 0 / 138 / 139; 60 / 64; 66 / 157 (all black) |
| Invalid circular reference | 28 pictures | Circular resources are referenced, but there are no pixels with corresponding color numbers in the atlas, and the screen will not move |

## 2. Types of palette cycling

17 recycled resources. Only the water surface is confirmed on screen (river on map 20); the rest of the names are inferred by color and using the map.

| Resources | Name | Color range | Color × Frame | Number of hops | Visible map |
| --- | --- | --- | --- | ---: | --- |
| 6419 | Water surface (blue) | 0xC0–0xD0 | 17 × 9 | 81 | 2, 3, 5, 8, 9, 12, 13, 21, 22, 32, 38, 40, 53, 55, 57 |
| 6420 | Water surface (purple gray) | Same as above | Same as above | 81 | 11, 17, 56, 68 |
| 6421 | Water surface (dark blue, suspected to be a night scene) | Same as above | Same as above | 81 | 15, 63 |
| 6422 | Water surface (grey) | Same as above | Same as above | 81 | 14, 20 |
| 6423 | Water surface (bright blue) | Same as above | Same as above | 81 | 10, 16, 41, 43, 46 |
| 6424 | Water surface (turquoise) | Same as above | Same as above | 81 | 6, 30, 31, 45, 58, 59, 61, 73 |
| 6425 | Water surface (blue) | Same as above | Same as above | 81 | Not used |
| 6426 | Dark green cycle | 0xB0–0xBE | 15 × 8 | 64 | 35, 37, 39, 44, 72 |
| 6427 | Green slow loop | 0xA0–0xA8 | 9 × 32 | 192 | 7 |
| 6428 | Orange-brown cycle | 0x10–0x14 | 5 × 10 | 90 | 3, 11 |
| 6429 / 6430 | Red pulsation | 0x15–0x17 | 3 × 8 | 67 | 19, 20 / 0 |
| 6431 | Dark blue flash (one frame per jump) | 0xD0–0xDA | 11 × 11 | 11 | 109, 120–135 |
| 6432 | Yellow loop | 0xDC–0xE0 | 5 × 8 | 48 | 78, 88 (10 pixels each) |
| 6433 | Red brown fast loop | 0xF8–0xFF | 8 × 7 | 14 | 156 |
| 6434 | Red-brown loop | 0xF0–0xFF | 16 × 15 | 30 | 136 |
| 6435 | Orange loop | 0xE0–0xE2 | 3 × 8 | 48 | 49, 50 |

**Water surface area**: 36 maps, arranged from most to least according to the number of moving pixels:

- 56: 204,824; 13: 196,030; 16: 162,164; 46: 152,410; 15: 114,147
- 58: 99,320; 40: 90,252; 14: 84,949; 55: 78,347; 53: 74,685
- 11: 70,340; 6: 67,257; 5: 66,224; 45: 65,027; 8: 63,311; 63: 61,664
- 31:59,651; 12:58,156; 10:52,639; 30:48,755; 17:48,018; 41:42,421
- 9: 38,472; 43: 30,834; 68: 29,423; 2: 29,209; 59: 25,097; 38: 18,890
- 73: 16,423; 3: 13,740; 20: 13,010; 21: 8,091; 22: 6,852; 61: 5,992; 57: 5,834; 32: 5,669

The water surface in the first 5 pictures exceeds 110,000 pixels, which is close to half the picture.

## 3. Colony

The 77 universe maps with a mode byte of 1 will jump to a colony map every 27 frames. 39 of the frames actually have colonies on them:

| Number of colonies | Map |
| --- | --- |
| 5 | 90 |
| 4 | 77, 118 |
| 3 | 100 |
| 2 | 92, 98 |
| 1 | 79, 81, 86–89, 95, 96, 99, 103, 106, 107, 110, 111, 113, 116, and 140–156 |

The remaining 38 have colony animations but no colony grid and do not move on the screen: 75, 76, 78, 80, 82–85, 91, 93, 94, 97, 101, 102, 104, 105, 108, 109, 114, 115, 117, 120–136.

## 4. 3D34 image change

| Type | Scenario | Map Change |
| --- | --- | --- |
| Comic strip sequence | 103 | 109 → 121, 123 … 135 → 136, each step is 38–46 different from 109 |
| Comic strip sequence | 105 | 111 → 141, 143… 155 → 156, each step is 28–43 different from 111 |
| Local variant | 134 | 37 → 39 (5 cells) |
| local variant | 38 | 116 → 117 (17 cells) |
| Local variant | 54 | 90 → 118 (22 cells) |
| Local variant | 97 | 104 → 137 (17 cells) |
| Change color palette with the same layout | 90, 102 | Switch from 99 to 60, 64 (same layout, two sets of red and dark color palettes) and 157 (all black), the order is to be checked |
| Replace the whole map with another map | 5, 7, 12, 16, 17, 26, 36, 38, 43, 44, 53, 100 | For example, scene 26 switches from 9 to 62; scene 16 switches to single-screen 74 |

The number of cells in the table is the difference compared with the initial map of the scene, not compared with the previous step. Only the odd numbers in the comic sequence are directly cut into the script; the even numbers 120-134 and 140-154 belong to the "static reference not found" in Section 5.

## 5. 25 static references not found

28, 34, 70, 79, 80, 103, 106, 120, 122, 124, 126, 128, 130, 132, 134, 138, 139, 140, 142, 144, 146, 148, 150, 152, 154

They may be accessed indirectly via the 3D34 type 0 state table (`8021E240`), or they may not be used at all. 138 / 139 has the same layout as map 0. According to [HD Asset Inventory §3.3](hd-asset-inventory.md#33-其他动态), it is the night scene and daytime variant, indicating that there is indeed an unresolved switching path. These 25 photos will not be included in HD production until the usage is confirmed.

## 6. List one by one

Dynamic column:
- "Invalid loop": the referenced loop resource has no pixels in the atlas;
- "Colony (no instance)": The colony animation is turned on, but there is no colony on the screen;
- "Same Layout": Lists other maps that share the same layout.

| Map | Dimensions | Gallery | Color Palette | Initial Scene | Dynamics |
| ---: | --- | --- | --- | --- | --- |
| 0 | 608×512 | 6228 | 6239 | 3 Gunsmoke の中で and other 5 | Red pulsation 375 px; same layout 138/139 |
| 1 | 592×384 | 6228 | 6237 | 11 时は流れた | static |
| 2 | 560×512 | 6228 | 6237 | 13 黑いガンダム | Water surface 29,209 px |
| 3 | 592×640 | 6228 | 6237 | 15 Kuしみの刀 | Water surface 13,740 px; orange-brown cycle 91 px |
| 4 | 496×608 | 6228 | 6243 | 10 Group of Killing Machines | Invalid Loop 6422 |
| 5 | 672×560 | 6228 | 6237 | 0 戦え!热き血のファイターたち | Water surface 66,224 px |
| 6 | 624×512 | 6228 | 6249 | 30 オペレーション・デイブレイク and other 3 | Water surface 67,257 px |
| 7 | 864×800 | 6230 | 6256 | 82 ゆがむCosmos and other 3 | Green slow loop 322 px |
| 8 | 704×608 | 6228 | 6237 | 24 撃撃のビクトリア and other 2 | Water surface 63,311 px |
| 9 | 560×800 | 6228 | 6237 | | Water 38,472 px; 3D34 Cut (Scene 26) |
| 10 | 624×512 | 6228 | 6247 | | Water 52,639 px; 3D34 Cut (Scene 12) |
| 11 | 864×544 | 6228 | 6238 | 18 Sad しみのホンコンシティ and other 2 | Water surface 70,340 px; Orange-brown cycle 956 px |
| 12 | 704×592 | 6228 | 6237 | 23 Rikiri no Town | Water surface 58,156 px |
| 13 | 704×640 | 6228 | 6237 | 16 杀を道くガンダム | Water surface 196,030 px |
| 14 | 672×608 | 6228 | 6243 | 28 Goodbye, I am a teacher, etc. 2 | Water surface 84,949 px |
| 15 | 752×432 | 6228 | 6239 | 21 Misato Fate and other 2 | Water surface 114,147 px |
| 16 | 720×592 | 6228 | 6246 | 31 さらば戦士よ | Water surface 162,164 px |
| 17 | 672×592 | 6228 | 6238 | 32 Liangshan Bo's の戦い and other 2 | Water surface 48,018 px |
| 18 | 576×512 | 6228 | 6243 | | 3D34 Cut-in (Scene 17) |
| 19 | 480×400 | 6228 | 6237 | 2 flow | red pulsation 423 px |
| 20 | 448×512 | 6228 | 6243 | 1 出撃!スイームルグ | Water surface 13,010 px; Red pulsation 69 px |
| 21 | 496×400 | 6228 | 6237 | 4 Angry りの家児魔神立つ! | Water surface 8,091 px |
| 22 | 672×496 | 6228 | 6237 | 5 ミケーネと百鬼 and other 2 | Water surface 6,852 px; 3D34 cut (scene 5) |
| 23 | 544×432 | 6228 | 6237 | 14 Gorgeous Naru・カイン | Invalid loop 6419 |
| 24 | 704×800 | 6228 | 6237 | 63 purge | static |
| 25 | 608×768 | 6228 | 6237 | 33 The sound of the universe | static |
| 26 | 544×432 | 6228 | 6243 | 9 Daring to lose! ル・カインのChallenge | Static |
| 27 | 560×544 | 6228 | 6252 | | 3D34 Cut-in (Scene 7) |
| 28 | 624×672 | 6228 | 6238 | | Static reference not found |
| 29 | 544×704 | 6228 | 6252 | 20 Hazama Yuu of the Sea and the Earth | Static |
| 30 | 704×592 | 6228 | 6245 | 27 ideal, collapse | water surface 48,755 px |
| 31 | 864×640 | 6228 | 6250 | 39 Ming Jing Shi Shui | Water surface 59,651 px |
| 32 | 768×672 | 6228 | 6237 | 40 その名はエピオン and other 2 | Water surface 5,669 px |
| 33 | 672×592 | 6228 | 6237 | 42 マーズとマーグ | static |
| 34 | 320×240 | 6228 | 6237 | | Static reference not found |
| 35 | 864×672 | 6230 | 6262 | | Dark green loop 173 px; 3D34 cut-in (scene 43/44) |
| 36 | 704×592 | 6232 | 6254 | 25 シャピロ、転生! | Static |
| 37 | 528×1024 | 6230 | 6261 | 134 Horror! The デビルアクシズ starts to move! (Back) | Dark green cycle 132 px |
| 38 | 640×560 | 6228 | 6242 | 65 Burning Burning Meteor | Water surface 18,890 px |
| 39 | 528×1024 | 6230 | 6261 | | Dark green loop 132 px; 3D34 cut-in (scene 134) |
| 40 | 704×608 | 6228 | 6237 | 68 Break in! Mobile Fortress をbreak 壊せよ! (front) | Water surface 90,252 px |
| 41 | 704×544 | 6228 | 6246 | 64 far き平和 | water surface 42,421 px |
| 42 | 704×544 | 6228 | 6237 | 66 戦いの意は | Static |
| 43 | 704×624 | 6228 | 6246 | 67 サンクキングダム、Beng Lei | Water surface 30,834 px |
| 44 | 960×704 | 6230 | 6261 | 135 Break in! Mobile Fortress をbreaker壊せよ! (Back) | Dark green cycle 301 px |
| 45 | 608×704 | 6228 | 6249 | 69 earth circle covered with dark clouds | water surface 65,027 px |
| 46 | 784×640 | 6228 | 6247 | 47 The unity of the earth circle | Water surface 152,410 px |
| 47 | 752×608 | 6228 | 6245 | 46 新しき道 | static |
| 48 | 640×880 | 6228 | 6245 | 48 Humanity's Victory, Hikari... (front) and 2 more | Static |
| 49 | 608×816 | 6231 | 6253 | 36 The End of Ambition and 2 more | Orange Loop 45 px |
| 50 | 736×688 | 6231 | 6253 | 50 ムーンアタック and other 3 | Orange loop 45 px |
| 51 | 832×640 | 6228 | 6255 | 57 キリマンジャロの兰 | static |
| 52 | 800×672 | 6228 | 6237 | 58 Eternal のフォウ(ボツ) and other 8 | Static |
| 53 | 608×800 | 6228 | 6237 | 55 その风に心素して | Water surface 74,685 px |
| 54 | 432×544 | 6228 | 6238 | 8 汉の意地!? 比比のとき | Static |
| 55 | 800×560 | 6228 | 6237 | 78 Beast Fighter Base Hui Attack | Water Surface 78,347 px |
| 56 | 864×800 | 6228 | 6238 | 129 Death Gate! Ruga Island Battle (Later) and 2 more | Water surface 204,824 px |
| 57 | 640×560 | 6228 | 6237 | 80 Empress ジャネラの人人杀り | Water surface 5,834 px |
| 58 | 560×640 | 6228 | 6249 | 81 The decisive breakthrough battle (front) | Water surface 99,320 px |
| 59 | 720×672 | 6228 | 6249 | 83 それでもあきらめずに (front) and other 2 | Water surface 25,097 px |
| 60 | 800×640 | 6231 | 6259 | | Same layout as 64; 3D34 cut-in (scene 90/102) |
| 61 | 784×656 | 6228 | 6245 | 92 见えないTomorrow | Water surface 5,992 px |
| 62 | 576×800 | 6228 | 6255 | | 3D34 Cut-in (Scene 26) |
| 63 | 864×544 | 6228 | 6239 | 79 Death Gate! The Battle of Ruga Island (front) and other 2 | Water surface 61,664 px |
| 64 | 800×640 | 6231 | 6251 | | Same layout as 60; 3D34 cut-in (scene 90/102) |
| 65 | 320×240 | 6228 | 6252 | 7 Meteor がfallちた日 | Invalid loop 6429 |
| 66 | 320×240 | 6233 | 6257 | 12 Maiden Meteor Meteor | Same layout 157 |
| 67 | 480×416 | 6228 | 6243 | 17 爱・戦士たち | static |
| 68 | 512×416 | 6228 | 6238 | 124 determinable time | water surface 29,423 px |
| 69 | 704×608 | 6228 | 6237 | 123 ここより公に | static |
| 70 | 320×240 | 6229 | 6258 | | Static reference not found |
| 71 | 640×896 | 6228 | 6237 | 130 The decisive breakthrough battle (Later) | Static |
| 72 | 960×704 | 6230 | 6261 | 132 アクシズのattack and defense (medium) | Dark green cycle 243 px |
| 73 | 320×240 | 6228 | 6250 | 43 その striking future は影ることなく and other 2 | water surface 16,423 px |
| 74 | 320×240 | 6236 | 6244 | | 3D34 Cut-in (Scene 16) |
| 75 | 880×672 | 6229 | 6258 | 34 pseudoりの平和 | Colony (no instance) |
| 76 | 880×672 | 6229 | 6258 | 35 热闘!ラビアンローズ | Colony (no instance) |
| 77 | 880×672 | 6229 | 6258 | 37 スウィートウォーターDefense War | Colony ×4 |
| 78 | 800×640 | 6229 | 6258 | | Yellow Loop 10 px; Colony (no instance); 3D34 Cut (Scene 36) |
| 79 | 800×704 | 6229 | 6258 | | Colony ×1; static reference not found |
| 80 | 800×640 | 6229 | 6258 | | Colony (no instance); static reference not found |
| 81 | 320×240 | 6229 | 6258 | 100 駆り立てるAmbition | Colony ×1 |
| 82 | 880×720 | 6229 | 6258 | 107 トールギス壊 | Colony (no instance) |
| 83 | 832×752 | 6229 | 6258 | 76 brother and brother | Colony (no instance) |
| 84 | 816×736 | 6229 | 6258 | 71 Threat of the Galactic Empire and 3 more | Colonies (no instance) |
| 85 | 880×800 | 6229 | 6258 | 72 ホワイトファング | Colony (no instance) |
| 86 | 784×704 | 6229 | 6258 | 75 Jupiter 帰りの男 | Colony ×1 |
| 87 | 720×560 | 6229 | 6258 | 53 The End of Chaos | Colony ×1 |
| 88 | 736×784 | 6229 | 6258 | 51 Ambition no line, no fruit, etc. 2 | Yellow loop 10 px; Colony ×1 |
| 89 | 880×704 | 6229 | 6258 | 61 Common Front | Colony ×1 |
| 90 | 784×704 | 6229 | 6258 | 54 真粋であるがゆえに | Colony ×5 |
| 91 | 848×752 | 6229 | 6258 | 59 アクシズからの Messenger | Colony (no instance) |
| 92 | 864×704 | 6229 | 6258 | 60 シロッコ立つ | Colony ×2 |
| 93 | 704×624 | 6229 | 6258 | | Colony (no instance); 3D34 Cut-in (Scene 38) |
| 94 | 768×704 | 6229 | 6258 | 77 Galactic Imperial Army Advance Fleet | Colony (no instance) |
| 95 | 880×704 | 6229 | 6258 | 84 Victory | Colony ×1 |
| 96 | 880×640 | 6229 | 6258 | 85 Earth Circle Pressure | Colony ×1 |
| 97 | 560×960 | 6229 | 6258 | 86 Battlefield (former) and other 3 | Colony (no instance) |
| 98 | 880×704 | 6229 | 6258 | 87 Ambition | Colony ×2 |
| 99 | 880×704 | 6229 | 6258 | 89 Dream, Zai Lai, etc. 4 | Colony ×1 |
| 100 | 960×720 | 6229 | 6258 | 88 アクシズのattack and defense (front) and other 3 | Colony ×3 |
| 101 | 800×704 | 6229 | 6258 | 91 Overture to the Destruction | Colony (no instance) |
| 102 | 880×720 | 6229 | 6258 | 96 Battle! Emperor's Battle! (Previous) | Colony (no instance) |
| 103 | 800×640 | 6229 | 6258 | | Colony ×1; static reference not found |
| 104 | 864×640 | 6229 | 6258 | 97 The future of life and death | Invalid loop 6432; Colony (no instance) |
| 105 | 880×624 | 6229 | 6258 | 73 contend for the world (previously) and 2 more | Colony (no instance) |
| 106 | 880×720 | 6229 | 6258 | | Colony ×1; static reference not found |
| 107 | 880×704 | 6229 | 6258 | | Colony ×1; 3D34 Cut (Scene 100) |
| 108 | 960×720 | 6229 | 6258 | 101 life, Sanって | Colony (no instance) |
| 109 |
| 110 | 800×640 | 6229 | 6258 | 104 Horror! The デビルアクシズ starts! (Previous) | Colony ×1 |
| 111 | 800×640 | 6229 | 6258 | 105 The Screaming Universe | Invalid Loop 6431; Colony ×1 |
| 112 | 736×544 | 6234 | 6260 | 106 Future をこの手に | Static |
| 113 | 800×704 | 6229 | 6258 | 45 Hunmiへの出撃 | Invalid loop 6431; Colony ×1 |
| 114 | 896×800 | 6229 | 6258 | 110 F91 Jin and other 7 | Invalid loop 6431; Colony (no instance) |
| 115 | 864×768 | 6229 | 6258 | | Invalid loop 6431; Colony (no instance); 3D34 Cut (scene 53) |
| 116 | 320×240 | 6229 | 6258 | 38 OZ Split (formerly) | Invalid Cycle 6431; Colony ×1 |
| 117 | 320×240 | 6229 | 6258 | | Invalid loop 6431; Colony (no instance); 3D34 cut (scene 38) |
| 118 | 784×704 | 6229 | 6258 | | Invalid loop 6431; Colony ×4; 3D34 Cut (Scene 54) |
| 119 | 320×240 | 6228 | 6237 | 26 Blood Painted Road | Static |
| 120 | 880×720 | 6229 | 6258 | | dark blue flash 1,009 px; colony (no instance); static reference not found |
| 121 | 880×720 | 6229 | 6258 | | Dark blue flash 1,009 px; colony (no instance); 3D34 cut-in (scene 103) |
| 122 | 880×720 | 6229 | 6258 | | dark blue flash 1,009 px; colony (no instance); static reference not found |
| 123 | 880×720 | 6229 | 6258 | | Dark blue flash 1,009 px; colony (no instance); 3D34 cut-in (scene 103) |
| 124 | 880×720 | 6229 | 6258 | | dark blue flash 1,009 px; colony (no instance); static reference not found |
| 125 | 880×720 | 6229 | 6258 | | Dark blue flash 1,009 px; colony (no instance); 3D34 cut-in (scene 103) |
| 126 | 880×720 | 6229 | 6258 | | dark blue flash 1,009 px; colony (no instance); static reference not found |
| 127 | 880×720 | 6229 | 6258 | | Dark blue flash 1,009 px; colony (no instance); 3D34 cut-in (scene 103) |
| 128 | 880×720 | 6229 | 6258 | | dark blue flash 1,009 px; colony (no instance); static reference not found |
| 129 | 880×720 | 6229 | 6258 | | Dark blue flash 1,009 px; colony (no instance); 3D34 cut-in (scene 103) |
| 130 | 880×720 | 6229 | 6258 | | dark blue flash 1,009 px; colony (no instance); static reference not found |
| 131 | 880×720 | 6229 | 6258 | | Dark blue flash 1,009 px; colony (no instance); 3D34 cut-in (scene 103) |
| 132 | 880×720 | 6229 | 6258 | | dark blue flash 1,009 px; colony (no instance); static reference not found |
| 133 | 880×720 | 6229 | 6258 | | Dark blue flash 1,009 px; colony (no instance); 3D34 cut-in (scene 103) |
| 134 | 880×720 | 6229 | 6258 | | dark blue flash 1,009 px; colony (no instance); static reference not found |
| 135 | 880×720 | 6229 | 6258 | | Dark blue flash 1,009 px; colony (no instance); 3D34 cut-in (scene 103) |
| 136 | 880×720 | 6229 | 6258 | | red-brown loop 699 px; colony (no instance); 3D34 cut-in (scene 103) |
| 137 | 864×640 | 6229 | 6258 | | Invalid loop 6434; 3D34 cut (scene 97) |
| 138 | 608×512 | 6228 | 6237 | | Same layout 0/139; static reference not found |
| 139 | 608×512 | 6228 | 6237 | | Same layout 0/138; static reference not found |
| 140 | 800×640 | 6229 | 6258 | | Invalid loop 6433; Colony ×1; Static reference not found |
| 141 | 800×640 | 6229 | 6258 | | Invalid loop 6433; Colony ×1; 3D34 cut (scene 105) |
| 142 | 800×640 | 6229 | 6258 | | Invalid loop 6433; Colony ×1; Static reference not found |
| 143 | 800×640 | 6229 | 6258 | | Invalid loop 6433; Colony ×1; 3D34 cut (scene 105) |
| 144 | 800×640 | 6229 | 6258 | | Invalid loop 6433; Colony ×1; Static reference not found |
| 145 | 800×640 | 6229 | 6258 | | Invalid loop 6433; Colony ×1; 3D34 cut (scene 105) |
| 146 | 800×640 | 6229 | 6258 | | Invalid loop 6433; Colony ×1; Static reference not found |
| 147 | 800×640 | 6229 | 6258 | | Invalid loop 6433; Colony ×1; 3D34 cut (scene 105) |
| 148 | 800×640 | 6229 | 6258 | | Invalid loop 6433; Colony ×1; Static reference not found |
| 149 | 800×640 | 6229 | 6258 | | Invalid loop 6433; Colony ×1; 3D34 cut (scene 105) |
| 150 | 800×640 | 6229 | 6258 | | Invalid loop 6433; Colony ×1; Static reference not found |
| 151 | 800×640 | 6229 | 6258 | | Invalid loop 6433; Colony ×1; 3D34 cut (scene 105) |
| 152 | 800×640 | 6229 | 6258 | | Invalid loop 6433; Colony ×1; Static reference not found |
| 153 | 800×640 | 6229 | 6258 | | Invalid loop 6433; Colony ×1; 3D34 cut (scene 105) |
| 154 | 800×640 | 6229 | 6258 | | Invalid loop 6433; Colony ×1; Static reference not found |
| 155 | 800×640 | 6229 | 6258 | | Invalid loop 6433; Colony ×1; 3D34 cut (scene 105) |
| 156 | 800×640 | 6229 | 6258 | | Red Brown Fast Loop 134 px; Colony ×1; 3D34 Cut (Scene 105) |
| 157 | 320×240 | 6233 | 6263 | | Same as layout 66; 3D34 cut-in (scene 90/102) |