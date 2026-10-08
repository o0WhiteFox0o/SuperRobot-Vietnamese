> **Language / Ngôn ngữ:** [English](original-images.en.md) · [Tiếng Việt](original-images.vi.md) · [中文](original-images.md)

# Original image extraction and weapon marking

Updated: 2026-09-11.

The raw data browser now displays raw images for characters, units, and maps. The image is a native PNG decoded from the fixed Japanese ROM and included in the output manifest along with the raw bytes. No modifications to ROM or runtime rendering paths.

See [Battle Images](battle-graphics.md) for large-scale images of the aircraft, animation parts, special effects and cut-ins in battle scenes; exports organized by aircraft/character names are also there.

## Coverage and entry

| Category | Related range | Current picture |
| --- | --- | --- |
| Characters | 361 names and identities | 96×96 or 97×97 avatars; decoded by respective palettes, identities can share images. |
| Aircraft | 363 airframes/forms | 16×16 tactical map icons, uniformly using our color palette 1010; not a large picture for combat animations. |
| Map | 158 map resource records | Complete static battlefield basemap; retaining tile flipping, excluding aircraft, auxiliary overlays, event changes and runtime effects. |
| Scene/Script | 144 physical map slots, 142 script slots | Reuse initial map preview; does not represent the number of playable levels, nor does it predict subsequent map changes in the script. |

The list displays thumbnails, details display images and source resource links, click on the image to open the original size PNG. "Map" has been promoted to the main category. 815 independent previews are deduplicated and written into `images/portrait/`, `images/unit-icon/`, `images/map/`; the map also generates thumbnails.

The generation method is still:

```sh
.venv/bin/python -B tools/content/extract_original.py \
  --snapshot build/recomp/gfx-probes/female-map-audio-1/latest-gfx-rdram.bin
```

`--snapshot` can be omitted when historical observation records are not needed. Image extraction does not rely on snapshots.

## Basis for binding characters and bodies

Binding and code byte locks are placed in `images`, `evidence` of `config/data/original-jp-v1.json`.

- Character: resident `8009C768..8009C7DC` reads two big-endian u16s from ROM `0x84220 + actor_id × 4`, which are image resources and palette resources. You cannot simply add a constant to the character ID as the picture ID. For example, characters 28 → `33/333`, 162 → `166/466`, 165 → `169/469`. The 361 avatar bindings are independent of the stat/spirit map which only has 360 slots.
- Body: `load_000AB160:801C60A4..801C6180` Get the body ID of the running body record `+2`, check VRAM `0x80218218`, and correspond to the u16 table of ROM `0x100D78`. The palette parameter is `1010 + 阵营`. Currently, 1010 is used uniformly, marked as our color matching. For example, the body 0 → 688, 36 → 718, 216 → 898, 362 → 1009.
- The avatar resource type is 15 or 6, and the 8-byte header is followed by the CI8 index; the body icon type is 14, followed by the CI4 index, with the high nibble first. The palette type is 3, the second u16 is the number of bytes in the palette, and after the header is the RGBA5551 big-endian color. Transparency bits are reserved; 5-bit color levels are mapped to 8-bit according to the project's existing picture decoding convention.

Each `images[]` item retains the file path, size, resource ID, and decompression SHA-256; characters and bodies also retain the ROM address, original bytes, and full table SHA-256 of the binding record. Images are not matched based on file adjacency or name similarity.

## Map layout format

The first three u16s of the resource record are layout, atlas, and palette. `801C6EFC` is passed in mode 8, and the renderer `800945D4` is selected via `80097C68`.

The layout's 8-byte header is `(type=7, group_count, width, height)`. `width`, `height` are in 8-pixel units; the actual 16×16 tile grid is `width/2 × height/2`. This grid is followed by a four-byte terrain record. This batch retains its original bytes and does not explain the terrain attributes.

Drawing groups start at `8 + width × height`, each group is six bytes:

```text
u16 tile      图集索引
u16 count     放置次数
u16 offset    放置列表相对布局资源起点的偏移
```

Each placement record is also six bytes: `u16 flags, u16 x, u16 y`. The atlas source coordinates are calculated according to the original renderer:

```text
sx = (tile & 0x000F) * 8 + ((tile & 0x0300) >> 1)
sy = ((tile & 0x00F0) >> 1) + ((tile & 0x0C00) >> 3)
```

Take 16×16 pixels from that position and draw as per placement record. `0x4000` flips horizontally, `0x8000` flips vertically; some maps also contain `0x2000`, which is not read by this drawing path, does not give additional semantics, and the complete flags are left in the preview metadata.

All 158 layouts, containing a total of 290,706 placed items, passed canvas bounds, atlas bounds, no duplicate positions, full grid coverage, drop list continuity, and resource tail bounds checks. Map 20 of Chapter 1 of Women uses `6284/6228/6243`, which outputs a 448×512, 28×32 grid base map; the auxiliary resource `6422/6429` remains in the original record and is not included in this base map.

## Weapon name and attributes

The original integration page repeated the entire menu string below the pure weapon name, such as `格アイアンネットP`. It now appears as:

| Weapon name | Attributes |
| --- | --- |
| アイアンネット | Grid · P |

`格` is for fighting, `射` is for shooting, `P` is for mobile use, `B` is for beam, and `MAP` is for map weapons. The page provides independent attribute columns, colors, hover descriptions and text legends. The original name, menu text and its TextKey are retained in the record and source details.

Parsing requires that "prefix + original name + allowed attribute suffix" is completely equal to the original menu string; the P and B in the name itself will not be truncated. A few pure names have MAP, and the menu inserts B before MAP. In this case, MAP will be removed from the display name only when the two strings match together. All 1,329 current weapon records match; unknown format retains name and displays "Mark pending parsing".

`weapon_traits.source` is explicitly `original-menu-text`. These are attribute mark displays on the original interface. They are not explanations of new ROM value bits, nor do they replace complete usability checks of strength, ammunition, form, skills, etc.

## Code and verification

- Decoding and correlation: `src/srw64_native/original_images.py`.
- Weapon marking: `src/srw64_native/weapon_traits.py`.
- Web page: `tools/data_viewer/web/images.js`, `weapons.js` and file rendering module.
- Added module SHA to generator records, all PNGs are included in `manifest.json.files`, and all resource references use existing stable identities.
- `PYTHONDONTWRITEBYTECODE=1 make check`: 103 tests passed, dependency check passed. Contains CI4 order and transparency bits, CI8, bad length/bad index, four flips, out of bounds/duplicate map positions, all actual picture bindings and complete map coverage, weapon name protection and all marker matching.

Test log: `build/original-data-qa/check-images.log`; Build log: `build/original-data-qa/build-images.log`; File, image size and resource reference checks: `build/original-data-qa/verification-images.json`. The size of 7,725 files and the actual decoding of SHA-256, 972 PNGs, and 1,168 file image associations all passed; the number of original image deduplications was 338 avatars, 320 body icons, and 157 maps.

The browser checked the thumbnail/details/grid and P independent attribute column of body 0, the avatar and profile of character 28, the complete base map of map 20, the picture was updated simultaneously when the next line was cut to map 21, and the script page of scene 1 reused map 20. After inspection, return to body 0 and retain the original 59110 service. The scope of this round of verification is static ROM decoding and data browser, and the game has not been launched.