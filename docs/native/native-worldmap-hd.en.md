> **Language / Ngôn ngữ:** [English](native-worldmap-hd.en.md) · [Tiếng Việt](native-worldmap-hd.vi.md) · [中文](native-worldmap-hd.md)

# Dialogue world map HD resources

2026-09-09. The current goal is "also vital. Intelligence that no one else can get," the world map behind this conversation. The user clearly corrected the scope with game screenshots: the forest and road tile experiments on the battle board do not belong to this delivery, and are not included in the current high-definition trial package.

Subsequent update: The standard plot dialogue of the high-definition entrance has been connected to [Real-time Apple UI](native-dialogue-ui.md), providing automatic line wrapping, paging, playback and speed control. The current profile only reads pure art textures in the allowed list; Chinese glyphs in historical merged packages do not enter the native art package.

## Resources and rendering paths

The original resource is **5604**, and the complete decompressed data uniquely matches the captured memory `0x2CF200`. Restore the map from the vertices and UVs of the original display list, and then take the European area to get a 512×512 source map. The original map uses 64×64 CI4 tiles; 512×512 is the old material size and is not the upper limit of native recomp or RT64.

The packaging script at that time `build_worldmap_runtime_pack.py` (deleted on 2026-09-24) cuts the high-definition map back to **512×512** tiles according to the original coordinates, which is **8 times the linear density** of the original texture, corresponding to the **4096×4096** map canvas. The game still submits the original map mesh, camera and markers, and RT64 selects HD assets with verified texture hashes. The map was not pushed back to CI4, nor was it made into a full-screen overlay with characters and text.

[`graphics.cpp`](../../src/host/graphics.cpp) reads `srw64-worldmap-hd.json` in the package, checks the actual replacement size and UV magnification in the lock of the texture cache, and writes the result to `worldmap-texture-runtime.json` in the run directory. This is the same set of data read by the GPU tile builder; checking does not modify the texture's access record or game RDRAM. It has been confirmed in the same mission replay that the original size of 57 / 57 tiles is 64×64, the replacement size is 512×512, and the coordinate magnification is 8×8.

RT64's `TextureSampler.hlsli` uses the actual `tcScale` for replacement textures; its low-precision native UV quantization does not apply to HD replacements. Regular texture filtering still exists, and internal rendering magnification and material pixel density are two independent settings. Increasing the internal rendering magnification alone cannot bring out details that were not present in the old footage.

## AI materials and original geometry

Use the built-in image_gen to edit the actual resource image and refer to the background style provided by the user. No characters, windows or yellow markers are drawn into the map assets.

- Whole image candidate: `assets/hd-ai/worldmap-runtime/ai-v1/`, actual model output **1254×1254**.
- European detail candidate: `ai-detail-v1/`, the source area is the original image `(0,64)-(320,256)`, the actual output is **1619×971**. Individually refine lens areas to achieve higher effective detail density and smaller mountain scales.
- Positioning correction: `ai-detail-registered-v2/`, using the land, sea and terrain color areas of the original map to constrain the smooth coordinate field, and resampling to generate the original pixels of the map. Document raw output, correction scripts, coordinate fields, library versions, and front and rear land mask coincidence indicators. The corrected original image is not equal to the exact original geometry, and the editing area is still limited by the source image protection layer.
- The original sea surface, narrow coastal edges and tile boundaries are retained during synthesis; the generated sea surface pixels are prohibited from adding new waters to the original land. Alpha is obtained from the original RGBA16 palette, first enlarged on the entire image, and then sliced.

4096×4096 is the **final running texture size** and does not mean that the model directly outputs native 4K images. The available details come from the aforementioned frozen AI output. The original image protective layer and the game's projection will also affect the look and feel of local edges.

57 verified map hashes were replaced; shared hashes with adjacency ambiguities continue to use the original package. Retain existing resources outside of European cut blocks. This time there is no claim that all world maps or battle maps have been converted into high definition.

## Current packaging

These 57 European tiles are stored in `assets/hd-ai/worldmap-runtime/pack-v6/`. Starting from 2026-09-25, they are no longer included in the package: Europe has changed to Bailian to use them as the base map to fill in the details and redraw them, see [Europe switches to Bailian](native-worldmap-regions-hd.md#欧洲改用百炼2026-09-25). pack-v6 should still be retained: it is the basemap of New Europe, and the painting style sample of [`worldmap_surfaces.py`](../../tools/hd_ai/worldmap_surfaces.py) `prepare` is also taken from its land texture.

The original packaging script, the apple square glyph package, and the old package that combined glyphs, avatar slices, and maps have been removed in the HD legacy cleanup on 2026-09-24. The above 57/57 texture verification and `live-v6` running records of 2026-09-09 are only for historical reference and do not represent the re-acceptance of the current package.