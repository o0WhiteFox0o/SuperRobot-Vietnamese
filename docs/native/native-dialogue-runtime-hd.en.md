> **Language / Ngôn ngữ:** [English](native-dialogue-runtime-hd.en.md) · [Tiếng Việt](native-dialogue-runtime-hd.vi.md) · [中文](native-dialogue-runtime-hd.md)

# Dialog HD Border

First edition on 2026-09-09, redrawn according to the original design on 2026-09-24. The borders of the plot dialogue boxes are changed to high-definition slices, which are still replaced by RT64 texture hashing. The position of the box, the transparency of the text bottom plate, and the text drawing order are all the same as in the game.

This page originally documented two early experiments that are no longer on the current launch path:

- The high-definition background of the map of Europe in Chapter 1 (57 tiles of resource 5604): now the entire area is covered by [Story World Map HD](native-worldmap-regions-hd.md), see [World Map HD](native-worldmap-hd.md) for the method.
- The blue glyph of the name: The old glyph dialogue path was deleted on 2026-09-24. The current dialogue is drawn by the native text layer, see [Dialogue UI](native-dialogue-ui.md).

## HD border resources

Target is ROM **Resource 1296**, 4,104 bytes, header is CI4 / 512×16 strip. The complete decompressed data uniquely matches the current capture RDRAM `0x2B8598`. The dialog uses 13 of these different 16×16 slices, repeatedly arranged into a 192×64 logical window.

[`dialogue_frame_asset.py`](../../tools/hd_ai/dialogue_frame_asset.py) is redrawn according to the original design, and each slice is changed to 64×64; all 13 calculated RT64 v5 hashes are equal to the real TMEM dump (checked one by one when giving `--capture`, usually calculated directly from ROM data and fixed palette).

- **Color Ribbon**: The original frame is a four-layered ribbon outside the rounded rectangle. The light comes from the upper left: white, silver, gray on the upper and left sides, light gray, gray, dark gray on the lower and right sides, and a dark blue line in the innermost part. When redrawing, the entire frame is drawn once according to geometry, the pixel steps are changed to smooth rounded corners, the light and dark boundaries are transitioned along the diagonal lines of the four corners, and then sliced ​​according to the original position.
- **Protruding pieces and blue light strips**: The original version has several small raised pieces on the upper and lower borders, with blue light strips embedded in them; there is a vertical light strip in the lower left corner and the upper right corner. The different top and bottom slices only differ in the position of these decorations. When redrawing, read out the protrusions and light bars from the rows of each original slice, and draw them into glass light bars with dark blue outer rings, gradients and highlights; the light bars across the slices are continued on both sides.
- 2026-09-24 The previous version was a code-painted silver beveled border with a full circle of cobalt blue inner lines, the four corners were cut to 45°, and all top edge slices used the same drawing. Users thought the "blue chamfer" was strange and changed it to what it looks like now. The old pictures are left in `assets/hd-ai/dialogue-runtime/v3/`, and the new version preview and build records are in `v4/`.
- The cyan four-corner mark of the current talk box (drawn on the native text layer, see [Reading mark](native-reading-indicators.md)) is also changed from a 45° bevel to a rounded corner consistent with the border.

The geometric position of the border resources, the transparency of the text base, and the text drawing order follow the game. It is drawn separately from the background map and text, without using the entire screenshot to cover the game. The scope of verification is the current opening dialogue; the use of these resources in other interfaces has not been checked one by one.

## Rebuild

13 slices are written into the world map package `worldmap-surfaces/pack-v5`, `--art` and the SHA-256 of these 13 items in the art list are updated at the same time; when giving `--capture`, the real TMEM load is used to check the hashes one by one:

```sh
PYTHONPATH=src:. .venv/bin/python -B tools/hd_ai/dialogue_frame_asset.py \
  --pack assets/hd-ai/worldmap-surfaces/pack-v5 --output build/hd-ai/dialogue-frame \
  --art content/art/stage1-hd.json
```

Previews and builds of the current version are documented in `assets/hd-ai/dialogue-runtime/v4/`.