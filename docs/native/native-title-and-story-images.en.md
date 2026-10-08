> **Language / Ngôn ngữ:** [English](native-title-and-story-images.en.md) · [Tiếng Việt](native-title-and-story-images.vi.md) · [中文](native-title-and-story-images.md)

# Title screen and plot text image

2026-09-24. The logo and flames on the title screen are replaced by full-frame high-definition images, and the seams of the tiles disappear; the title menu words, and the text displayed by pictures in the plot (chapter title card, opening prologue page, ending page) are all drawn with native text according to the reading language, and the movements follow the game's own scaling, rotation, and flipping. The plot text picture **no longer displays the original picture**, the same is true when F6 cuts to the original picture; the logo and flames follow F6.

| Screen | Original image | Now |
| --- | --- | --- |
| Title Logo | Scene 683: 64 16×16 parts assembled into 256×64 | Full frame HD picture, follow F6 |
| Title Flame | Scene 686: 16 frames with 40 32×32 parts per frame | 16 horizontally loopable HD tiles, follow F6 |
| PRESS START BUTTON, four items in the ring menu | Scene 651–655 (Gallery 623) | Native text, follow language (Chinese: please press START key, start, read, continue, option) |
| The title of the work that flies by when booting | Scene 628–650 (Album 623 / Palette 624), 23 works | Native text, following language: small subtitle at the top, title of the work at the bottom, take the noun of the work |
| The name of the aircraft before the demonstration battle | Scene 658–680 (Atlas 656 / Palette 657), 23 units | Native text, follow the language: model at the top (same in each language), aircraft name at the bottom, take the aircraft noun entry |
| Chapter title card | 133 cards (table 0x84B20), "Episode N" is scene 5106+N−1 | Native text "Episode N" and "Title", retain the entry action |
| Prologue | 30 text pages (5506–5535) | Native text, translation taken from `intro.txt` |
| Ending | 7 pictures (5570–5576) | Native text, translation taken from `ending.txt` (newly written this time) |
| Credits | 20 pages (5544–5563), between epilogue and "end" | Native text, following language, taken from `credits.txt` |
| Copyright page | 620 at boot (scene 622) | Native text, all languages retain the original text |
| BANPRESTO logo, GAME OVER | 617 (scene 619), 615 (scene 614) | Full frame high-definition picture, generated from ROM when the game is running, follow F6; without AI |

No handling: title focus line (611, palette animation).

## How to draw the game

### Scene Wizard

Title elements and plot text images are all **scene sprites**: a frame is made up of several parts listed in the scene resources, and each part is taken from the album. `80097C68` Select painter by mode (jump table `800D0530`, subscript mode − 1):

| Mode | Painter | Drawing Method |
| --- | --- | --- |
| 11, 12 | `800975A4` → `80096CD8` | One TEXRECT for each part (screen coordinates, cannot be scaled) |
| 13 | `8009751C` → `80096CD8` | Same as above, y minus depth |
| 14, 15, 16 | `8009761C` | Four vertices of each part plus one G_QUAD, subject to sprite matrix transformation (scaling, rotation, perspective) |

Command to display each part in the list:

- `80096CD8`: `FD48` Tile, `F5`, `E6`, `F4` LoadTile, `E7`, `F5`, `F2` SETTILESIZE, then `E4`/`E1`/`F1` consists of three TEXRECT. When the coordinate is negative, clamp to 0 and adjust S.
- `8009761C`: `01004008` G_VTX (4 vertices of the part), map load, two `F2`, then `07` G_QUAD. When reading statically, I thought G_VTX was close to the quad, but it was only in the actual machine dump that I saw it clearly before the texture was loaded.

Both load a 16-color palette at the beginning (`FD10` + LoadTLUT); when the sprite transparency is not FF, write another `FA` primary color (alpha is in the low byte).

**The resource number can be read directly. ** The sprite is recorded in `800FFAAC + 槽 × 0xC4 + 子 × 0x30`: +0xA scene, +0xC atlas, +0xE palette are all resource handles, +0x11 is the current step. The handle table is in `80160340`, each item is 20 bytes: +0 in use, +2 **ROM resource number**, +0x10 data address (`8008A11C` takes the address, `80089EB0` searches or allocates according to the resource number). So there is no need to identify by pixel summary like avatars do. The 0th byte of the scene data is the step number, and each step starting from the 2nd byte is (frame number, duration).

### Title screen

The header overlay is in ROM `0x10DA50` (RAM `801C4500`).

| Element | Slot | Mode | Scene/Gallery/Palette |
| --- | --- | --- | --- |
| Flame | 9 | 11 | 686 / 684 / 685, location (160, 120) |
| Logo | 2 | 11 after 14 (entry) | 683 / 681 / 682 |
| PRESS START BUTTON | 3 | 11 | 651 / 623 / 625 |
| Ring menu | 3–6 | 14 | 652 スタート, 653 ロード, 654 コンティニュー, 655 オプション; Gallery 623 |
| Flying work name | Assigned by `801C5500` | 14 | 628 + n / 623 / 624, n taken from `D_801CC340` |
| Unit name before demonstration | 2 | 15 | 658 + n / 656 / 657 (`801C9EA8`), the unit is drawn vertically in slot 3 |

The donut menu differentiates states by color palette: 624 off-white, 625 and 626 blue (front items), 627 dark. Native text is drawn with a white to light gray gradient, multiplied by the lightest color in the current palette, so the original highlights and darkens still take effect.

Each frame of the flame is actually a 128×128 tile in the atlas, spread horizontally 2.5 times (x −160…160, y −8…120, column order 3, 0–3, 0–3, 0). There are two exceptions:

- There are two missing blocks in the top row of frames 4 and 10. Those two blocks in the atlas are irrelevant bright yellow pixels, which were not drawn intentionally in the original work;
- In frame 5, draw two more 16×16 flames (y −24) above the tile.

Therefore, the high-definition picture is reconstructed according to the "actually drawn parts", leaving an extra 16 px at the top.

### The work name and machine name of the title demonstration

There are 23 pictures in each group, corresponding to the 23 title demonstrations (the last 23 demonstration records of ROM `0x83110`).

- **Work name**: After booting up, after BANPRESTO and the copyright page, and before the logo appears, `801C5500` makes the work name fly from a distance (mode 14, with frame buffer afterimage). The picture is a two-layered text: the subtitle in small letters on the top (Mobile Warrior, Super Electromagnetic Force, etc.), and the name of the work on the bottom; 0083, and below there are STARDUST MEMORY, ジャイアント・ロボ, and below there are THE ANIMATION and "The Earth Stands Still".
- **Unit name**: In the bright field with a white background before the start of each demonstration, the name of the unit (slot 2) and the three-dimensional drawing of the unit (slot 3) appear together. Scene number = 658 + `D_801CC198[D_80161566]`, the body and BGM are taken from the table `D_801CB124` (each item is s16 body number, s16 song number). The 8 Gundam series machines have model numbers in small letters above their names (MSZ-006, RX-93, etc.).

### Chapter title card

The opening state machine `D_80217AE8` of the map overlay (`load_000AB160`):

1. `801C72C8` creates two mode 14 wizards: slot 0x9C is the title (card number = `D_802195B1[场景 × 2]`, `8009C8EC` looks up the table `0x84B20` to get the scene/atlas/palette), slot 0x9D is "Nth episode" (scene 5106 + episode count, upper limit 98). Initial value: scale 20, depth 740, 180° around the Y axis; and call `800836CC(1)` to turn on afterimage.
2. `801C7460`: The zoom is subtracted by 1/24 for each frame and rotated 5° around the Z axis until the zoom is ≤ 1.
3. `801C7514`: Continue to the full circle.
4. `801C765C`: Rotate 5° per frame from 180° around the Y axis (flip).
5. `801C77A0`: Release two elves after stopping for 91 frames, `800836CC(2)` turns off afterimage.

Afterimage is implemented by `80083744`: When `D_8010F5B6` is 1–3, the previous frame is used as a texture and stacked back to the screen with decreasing alpha (from 200). RT64 copies this frame buffer at the native resolution, so the smear when rotating is square; this has nothing to do with this replacement, the frozen card itself is high-definition native text.

### Opening Prologue and Ending

- Prologue (title overlay): `801CA468` Build a mode 14 sprite in slot 2 or 3 (scene and gallery taken from `D_801CB230[组][页]`, palette 5536), scale 10; `801CA608` converted to a mode 11 still page after subtracting 0.4 to 1 per frame.
- Ending (`load_001156A0`): Page table `D_801C3050` (ROM `0x1160F0`), each item (scene, gallery, frame number), ends at 0xFFFF. First the epilogue text 5570-5575, then the credits 5544-5563, and finally the "end" 5576; the color palette is all 5564, and the same mode 14 is used to zoom in and then switch to mode 11.
- Asset inventory once classified 5582 as the starry sky at the end of the credits, but it is actually the background of the world map overlay (`load_000A7EC0`).

### Credits, copyright page, BANPRESTO logo and GAME OVER

2026-09-24 added. All four are scene sprites in Mode 14, using the same set of hooks:

| Screen | Slot | Scene/Album/Palette | Created by |
| --- | --- | --- | --- |
| BANPRESTO logo | 2 | 619 / 617 / 618 | title overlay `801C4E8C` |
| Copyright page | 0 | 622 / 620 / 621 | Title overlay `801C5104` |
| GAME OVER | 0x3D | 614 / 615 / 616 | Map overlay `801DF338` (`3D4C` Game Over) |
| Credits | 2, 3 | 5565–5569 / 5544–5563 / 5564 | Ending page table, 85 frames on page 1, 55 frames each |

- **Credit**: The same treatment as the ending page, the `staff_style` of [`sprite_text.cpp`](../../src/host/sprite_text.cpp) is centered and the line spacing is about 30 units (the line spacing of the original image). The text is in the `@intro:<资源号>` entry of `content/dialogue/<语言>/credits.txt`: the position is translated; the Chinese name is converted to simplified Chinese characters, and the kana pen name remains the same; the English name is Romanized, with the first name first. The original text line (`>`) is the content displayed in Japanese.
- **Copyright Page**: `copyright_style` is left aligned and also placed in `credits.txt` (`@intro:620`). According to the user's request, only the original text is changed, and the three languages ​​​​are all original texts.
- **BANPRESTO logo with GAME OVER**: Magnification 8x (1792×768, 1280×256). The logo is a trademark, not AI: both have only a few flat colors and anti-aliasing. Each pixel is decomposed according to the two nearest key colors. Each color layer is enlarged and smoothed to take a steep soft maximum value. The edge is about 1 output pixel wide; GAME OVER gray stroke layer retains the original light and dark.
- Generated from the player's ROM when the game is running (user-determined) from 2026-09-25, these two pictures are not included in the HD package: [`rom_art.cpp`](../../src/host/rom_art.cpp)'s `flat_image` transplanted the algorithm of [`flat_scene_hd.py`](../../tools/hd_ai/flat_scene_hd.py) (Pillow The bicubic scaling and box-type fuzzy approximate Gaussian are all implemented accordingly), `host.cpp` is registered in `on_init` with `add_generated_image` of [`native_sprite`](../../src/host/native_sprite.cpp). The scene is generated on the decoding thread when it first appears, and the whole frame is drawn like the file image. Register only if you have HD art package (`SRW64_ART_PACK`).
- `scene_images` of `stage1-hd.json` changed back to `assets/hd-ai/title/whole-v1` (title logo with flame). The output of `flat_scene_hd.py``whole-v2` is only used for comparison on this machine: `make recomp-rom-art-test` compares the difference after premultiplication, BANPRESTO averages 0.2 levels; GAME OVER is about 4 levels, the difference is staggered by one pixel at the stroke edge, and the picture is the same.
- Actual machine: BANPRESTO draws the generated graph (`build/recomp/debug/20260925T071832.109292Z/banpresto.png`) from the 147th frame after booting; GAME OVER draws the generated graph in the test level (`20260925T072039.132657Z`, `scene-sprites.jsonl` of `20260925T072411.224535Z` and `image` line of scene 614). Users have seen it on the actual machine and there are no problems.
- Test level `game-over.json`: Directly `3D4C` after switching to the battlefield at the beginning.

## Text recognition

- **Chapter Title Card**: 133 pictures are read one by one (Claude recognized), saved as `assets/transcriptions/chapter-titles.ja.json`, the original pictures are retained and line-wrapped, and "previous/middle/post-editing" are separated into separate lines. Compare with the title text 281 + scenes one by one: 136 out of 143 scenes are exactly the same; card 8 "Jie Farewell" and the text "Jie Farewell のとき", card 89 "戦 field へ帰る" and "戦 field に帰る" each differ by one pseudonym; reserved scenes 125–127 share the card with scene 81 82 "Purification"; cards 0 and 1 only have "Episode 1" (placeholder, used in scenes 58 and 142); cards 127 and 128 are the same "Confluence".
- **End Page**: 7 pages of pictures read line by line, saved as `assets/transcriptions/ending-pages.ja.json`.
- **Opening Prologue**: Follow the transcription of 2026-09-23 `assets/transcriptions/intro-pages.ja.json`.

The transcription contains the original Japanese text and is only placed locally in `assets/`. Only the cards obtained from it are submitted to the warehouse → text number comparison ([`story_cards.hpp`](../../src/host/story_cards.hpp), generated by [`text_images.py`](../../tools/content/text_images.py) and checked by the test).

## Where does the translation come from?

| Text | Source |
| --- | --- |
| Four menu items, PRESS START BUTTON | locale interface text `title_start`, `title_load`, `title_continue`, `title_option`, `title_press_start` |
| "Chapter N" | Interface text `intermission_episode` |
| Chapter title | Word entry (`story.chapter_title`), the host takes the current language through `dialogue::ui_text`; add "" for Chinese and Japanese |
| Prologue | `@intro:<资源号>` entry for `content/dialogue/<语言>/intro.txt` |
| Ending | `content/dialogue/<语言>/ending.txt`, also an `@intro:<资源号>` entry, this time handwritten, `---` means an empty line |
| Demonstrated work title | Text 85 + work number (written in two lines, with the subtitle before and the work name after the line break; the two lines are swapped when the English subtitle ends with a colon, such as Dancouga); text for the subtitle of Counterattack のシャア, 08th MS Team 60 (mobile warrior ガンダム); STARDUST MEMORY, THE ANIMATION As it is; "The Earth is Still Still" is the interface text `title_demo_giant_robo_subtitle` |
| Demonstration aircraft name | Text 527 + aircraft number; the demonstration table says MASCUBAZ (JS) (263), and the picture says MASKODEZ, so take 262; the model number is written as it is in the picture in `sprite_text.cpp` |

Japanese display directly uses the original lines in these entries (`>`). The lines file can be placed in the user directory and overwritten. After pressing F5 to read it again, the text page will also be updated.

## Host implementation

- [`native_sprite.cpp`](../../src/host/native_sprite.cpp) (shared by three hosts): `generate_cpu.py` Rename `80096CD8`, `8009761C` to the original function, wrap one layer with [`game_hooks.cpp`](../../src/host/game_hooks.cpp), and note the display list range written this time. After drawing, obtain (scene, atlas, palette, frame) according to the sub-record and handle table, and decide what to replace:
- With native text: always replaced;
- There is a high-definition picture of this frame in the art package, and in HD mode: Replace;
- Otherwise keep original parts.

When replacing, leave the last part as a mark and leave the rest blank: TEXRECT is changed to a rectangle covering the entire frame; the quadrilateral retains the original G_VTX and G_QUAD. Mark the previous command with a numbered G_NOOP tag. RT64 recognizes the tag when building, calls the host callback at the same drawing position, and draws via Plume (`src/host/shaders/HdSprite*.hlsl`): TEXRECT draws a rectangle according to screen coordinates; the quadrilateral takes the world matrix and projection drawn this time, and draws a rectangle in the model space, so the scaling, rotation, flipping, and perspective are consistent with the original version.
- The text is placed according to the center of the original frame (the chapter title is according to the top edge), and the size is determined by the typesetting, and it can be wider than the original image.
- The decoding and text rasterization of high-definition images are completed in the background thread. When not ready, the high-definition frame will draw the original picture this time, and the text will not be drawn (mostly the first few frames of zooming). The texture is premultiplied Alpha with mipmap; after more than 48 images are resident, the ones that have been idle for more than 20 seconds will be released.
- [`sprite_text.cpp`](../../src/host/sprite_text.cpp) (only in the game host) determines which text is displayed for each sprite, and types, strokes, and shadows are added:
- Menus and title cards use HarmonyOS Sans 2.040 variable font **Bold** instance (wght 706, `game_font_sources(locale, 700)`), there is no separate bold file; English uses Condensed first, then SC, and the symbol font is padded;
- Use Regular for the prologue and ending pages, with a width of 256, and gradually reduce the font size when it cannot fit;
- The stroke is obtained by distance transformation, and the text has a vertical gradient.
- Log: `scene-sprites.jsonl` in the running directory records the first processing method and VI of each type (scene, atlas, palette, frame); write `scene-sprite-summary.json` when exiting.

## HD material

[`title_hd.py`](../../tools/hd_ai/title_hd.py) is divided into four steps: `prepare` freezes the request from ROM, `run` is sent via `run_benchmark.run_one`, `compose` registers, preserves color, and cuts out the image, and `build` writes out the runtime directory.

- The model is `qwen-image-3.0`, seed 640903 (same as the avatar), a total of 5 requests, and the public price is about 1 yuan:
- Logo once: Leave 16 px margin on black background, magnify 7 times;
- Flame four times: 2×2 four frames each, with 64 px of its own looping content on the left and right of each frame, enlarged 4x.
- Registration: Measure the displacement window by window, and fit the scaling and offset according to the two axes; when resampling, the cell edges are copied outward to avoid sucking the black intervals into the bottom edge.
- Color preservation: High-frequency details are taken from the model output, and low-frequency colors are taken from the original image (radius 2 original pixels). Alpha takes a 1-bit mask of the original image, enlarges it and smoothes it to a side about 1 output pixel wide.
- Loop: The 8 original pixels on the left side of the tile cross-fade into the continuation content drawn by the model outside the right side, so the beginning and end are seamless.
- Average difference from original image after shrinking to original size: logo 5.1, flame 3.7–8.5.
- Output in `assets/hd-ai/title/whole-v1` (Logo 1792×448, flame 16 sheets 512×576), referenced by the `scene_images` section of [`stage1-hd.json`](../../content/art/stage1-hd.json), [`assets.py`](../../src/srw64_native/assets.py) After verifying the digest, copy it to the art package and write `srw64-scene-images.json`.

## Actual machine verification (2026-09-24)

- **Title**: In the Chinese and English screenshots, the logo and flame are in full-frame high-definition, and the seams disappear; the menu words are displayed according to language, with the front items in blue and the rest in gray, consistent with the original version. After F6 switches to the original version, the logo and flame return to the original image, and the menu text is still the original text. The user has switched languages ​​in the window and confirmed that multi-language is normal.
- **Opening Prologue**: The public prologue of the new game, natively displayed page by page in Chinese, English and Japanese, with zoom entry and page turning driven by the original version.
- **Ending**: `ending.json` The mini-level is executed in 3D71, and the 7 pages of the ending are all natively drawn (Chinese); subsequent credits are still the original drawings.
- **Chapter Title Card**: All three places are zoomed in and rotated into the scene: `act.json` Mini level, the second episode entered through "Go to the next level" in the first episode, and the first episode of the new game. `act.json` That time I pressed VI to take a fixed-point screenshot, and captured the flip and the final freeze frame: "Episode 2" and "Fight! Fiery-blooded Fighters", which are in native Chinese (the number of episodes in the mini-level increases by 1 for "Episode N").
- Exit statistics (the second episode): 2951 drawings were rewritten, 0 were left as they were, and all 24 materials were decoded successfully.
- **Credit list and startup screen** (Supplementary): Chinese `ending.json` is cut all the way to the 2D art page, and English is cut to the SD original art page (17 pages out of 20 pages). The original text is displayed page by page. The BANPRESTO logo at startup is a high-definition full frame, the original text on the copyright page, and Japanese characters such as "Reed" are normal.
- **GAME OVER** (Supplement): English `game-over.json`, freeze frame to high definition, cut to the original version to see the original picture (there are thin lines formed by the seams of parts at the bottom of the original picture), and then cut back to high definition.

## Command

```sh
.venv/bin/python -m tools.hd_ai.title_hd prepare --output assets/hd-ai/title/v1
.venv/bin/python -m tools.hd_ai.title_hd run --output assets/hd-ai/title/v1 --env-file /path/to/.env
.venv/bin/python -m tools.hd_ai.title_hd compose --output assets/hd-ai/title/v1
.venv/bin/python -m tools.hd_ai.title_hd build --output assets/hd-ai/title/v1 --target assets/hd-ai/title/whole-v1
.venv/bin/python tools/content/text_images.py header --write   # 卡片 → 话名对照
.venv/bin/python tools/content/text_images.py render           # 结局页原图，供转写核对
.venv/bin/python -m tools.hd_ai.flat_scene_hd build --base assets/hd-ai/title/whole-v1 --target assets/hd-ai/title/whole-v2 --bind
```

After changing the hook of `generate_cpu.py`, you need to rerun it first and then build the host.

## Legacy

- The title concentration line is still the original image.
- Most of the English names in the production credits are based on the pronunciation of Chinese characters, and the original work has no phonetic notations; the sources were verified on 2026-09-27, including Akabane Jin, Nomura Kyouhiro (Michihiro, originally mistaken as Norihiro), Kono Yuko, Hamada Tomoyuki, and the rest are still listed at the beginning of `content/dialogue/en/credits.txt` to be verified.
- Afterimages when title cards are rotated are still at native resolution (the way RT64 copies the framebuffer).
- The ending has only been tested in the mini-level; the full ending has not been played from the pass save.
- This path follows Plume like other HD layers, and is available under both Metal and Vulkan; Vulkan has only been tested with MoltenVK on Mac.