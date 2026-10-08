> **Language / Ngôn ngữ:** [English](3d-model-replacement-analysis.en.md) · [Tiếng Việt](3d-model-replacement-analysis.vi.md) · [中文](3d-model-replacement-analysis.md)

# SRW64 Original 3D and model replacement analysis

2026-09-10 Update: 5600’s [Native GPU Water Drop Replacement](../native/native-model-replacement.md) has completed the bounded verification from the heroine’s opening to the first episode’s tactical map. Modern floating point meshes and Metal materials have been integrated into the scene draw order, and the original game provides poses and cameras.

2026-09-09. The object is the Japanese Rev 0 ROM in this repository, and the current N64Recomp + RT64/Metal native host. The basic structure of the battle screen is clearly **3D background + 2D body sprite**. The original work has three-dimensional geometry that can be extracted, which is suitable for starting from plot markers, battle scene backgrounds and ship shape resources; the 2D performance of ordinary combat bodies needs to be processed according to another type of engineering.

## Which parts of the original work were 3D used?

| Section | Current Evidence and Judgment | The Implications of Model Replacement |
| --- | --- | --- |
| Combat background | 3D background, presented in combination with 2D body sprites. Ground surfaces, relief surfaces, vertical background patches, and building shapes are visible in ROM geometry resources. What needs to be confirmed is the scene, camera and draw call corresponding to each background ID | The most worthwhile direction to expand art investment, which can replace terrain, architecture, distant view geometry and materials scene by scene, while retaining the original body sprites and combat scripts |
| Story world map | 5604 and 5605 each have 70 rectangular faces and 140 triangles drawn. The Y coordinates of all vertices used for drawing are 0; the mountains in the original image are mainly textures | The grid hosting the map can be replaced; adding real mountains is a new three-dimensional terrain based on the original plane |
| Plot map three-dimensional markers | 5600 original version with a total of 16 triangles drawn. Completed ownership confirmation, Diamond 8 → 96 side playback, and the actual opening of the experimental ROM to the first episode tactical map | Verified original loader, rotation, plot position changes and cuts; next step to verify re-entry/save recovery and more scenes |
| Ship/aircraft shape resources | 5584–5597 is the ship drawn on the front of the track when sailing on the plot world map `3D33`. The ship name has been bound to the model table and matching table (5584 アルビオン, 5585 アーガマ, 5588ネェル・アーガマ, 5591 ラー・カイラム, etc., see [World Map Cut Scene Model HD](../native/native-ship-model.md)); 5590, 5592, 5596 come with name tags, 5598/5607 are scene landmarks | 15 5597 and 5601 have been rebuilt according to the settings and replaced with real machines, 5597 and 5601 have no exit path and have not been processed |
| Some background layer/effect candidates | 5598, 5610, etc. are flat or multiple flat parts; 5599, etc. are a mix of multiple parts. There is no complete analysis of the relationship between animation and scene organization | The plane itself can also enter 3D rendering; textures and time sequences need to be combined to distinguish backgrounds, effect frames and solid components |
| Chapter 1 Tactical Chessboard | Viewed the map GPU picture; the last mission snapshot of `female-map-audio-*` checked was mainly textured rectangle drawing, and no vertex loading/triangle commands appeared. The three-dimensional look of the building is not enough to prove that there is a replaceable building model | High-definition tiles belong to the existing texture process; erecting checkerboard towns and forests requires new map scene rendering. This conclusion is limited to examined maps and missions |
| Ordinary combat body, character avatar, UI | The producer clearly stated that the robot itself is 2D. The battle pictures of Titan 3 in the first episode have been viewed; scaling and perspective cannot be used as evidence of skeletal models | It is most direct to continue to use 2D high-definition materials; changing to a 3D body requires a new model, actions and performance bindings, and the existing evidence does not support describing it as a simple model change |

Direct interview with the producer: [Dengeki Online, 2022-02-11](https://dengekionline.com/articles/109826/). The interview uses the wording "suspected 3D" for the background; this report clearly categorises the project by "3D background + 2D body sprite" to avoid interpreting this wording as meaning that the background is only a flat picture. A 3D scene can contain both three-dimensional meshes and textured planes, and the specific composition of each background element still needs to be bound one by one. This time, we do not infer the realization of all weapon special effects based on this.

## This ROM static survey

Enter SHA-256: `ee5f4a21d8e5f7827d21199e27800edf250df9a8e4d10befb1a6992df597b13e`.

- Scan all **6,436** entries in the compressed resource table.
- Resources **5584–6066** total **483** with `36340038` header, consistent with containers recognized by existing map parsers.
- Vertex loads and triangle references were resolved for **606** display lists of type 0/5 within these containers; all reached the end command and reference and range checks passed. The 624 MoveWords are all light color settings and do not change the vertex position of this statistics.
- Checking together the local coordinates of each container's referenced vertices: **182** coplanar, **301** non-coplanar. The splicing of multiple different planes may also be non-coplanar and cannot be called 301 closed entities, 301 bodies or 301 bound scene models accordingly.
- Scene hierarchy, animation, conditional clipping and full materials are not interpreted by the parser. 5638 also contains type 8 descriptors, whose functions will not be explained this time. Other areas of ROM and geometry generated at runtime are also not included in this container statistical caliber.
- The vertex position set and triangle number of 5604/5605 are consistent with the existing map extraction results.

Diagnostic plots are drawn based on extracted raw coordinates, with no original textures, materials, game cameras or animations loaded. The English shape tag is a candidate category and is not a confirmed game asset name.

![ROM original geometry sample](../../assets/models/3d-2026-09-09/geometry-samples.png)

Local survey products:

- [Resource head census](../../assets/models/3d-2026-09-09/header-survey.json)
- [Geometry list and each display list check](../../assets/models/3d-2026-09-09/geometry-survey.json)
- [Static parsing script](../../assets/models/3d-2026-09-09/survey_geometry.py) and [Verification result](../../assets/models/3d-2026-09-09/validation.json)
- [Existing task snapshot binding](../../assets/models/3d-2026-09-09/snapshot-bindings.json)
- Geometry OBJ samples: [5584](../../assets/models/3d-2026-09-09/resource-5584-geometry.obj), [5592](../../assets/models/3d-2026-09-09/resource-5592-geometry.obj), [5600](../../assets/models/3d-2026-09-09/resource-5600-geometry.obj), [5604](../../assets/models/3d-2026-09-09/resource-5604-geometry.obj), [5614](../../assets/models/3d-2026-09-09/resource-5614-geometry.obj), [5750](../../assets/models/3d-2026-09-09/resource-5750-geometry.obj). Contains only local vertices and faces, no materials, UVs, bones or animations; left under ignored `build/`.

## Runtime evidence boundaries

The initial analysis review is the existing task/RDRAM snapshot on disk. Subsequently, RT64/Metal playback of independent copies, individual hiding, fixed topology vertex deformation and 96-sided high-poly replacement were completed for the 5600. 2026-09-10 The high-module was compiled into independent ROM resources, and the original loader was used to complete the actual running of 16,800 VIs starting from empty SRAM, the female opening dialogue to the tactical map of the first episode. Loading, rotation, plot position changes, and cuts all have mission/GPU evidence; full route not verified with N64 hardware. For details, see [Local Resource Page and Verification Records](native-model-viewer.md).

In `build/recomp/gfx-probes/female-story-2/`, 5604 the complete decompression content matches the memory `0x2BF9F0`, and its display list entry `0x2E4480` is called by the root task; 5600 the complete content matches `0x2BDE68`, and the entry `0x2BF7D0` is called. The address only belongs to this snapshot and cannot be written as a fixed address for the whole scene.

`first-map-reload-2` end snapshot also resides at 5729, 5734, 5878, 5879, 5974, 5975; `first-map-turn5-reload-1` resides at 5746, 5747, 5748, 5920, 5975. The root tasks are not observed calling their geometry display lists at this moment, so they only provide subsequent scene tracking clues and cannot be directly attributed to the currently visible background.

Viewed existing GPU images: World Map `worldmap-runtime/live-v6/present-3540.png`, Tactics Board `female-map-audio-1/present-6660.png`, Battle of Titans 3 `first-map-reload-2/present-3780.png`. Image observation, static geometry, memory residency, and display list calls are recorded separately and do not replace each other.

## What can the current native project do?

The existing [`graphics.cpp`](../../src/host/graphics.cpp) accepts the original task in `send_dl()` and allows modifications in `display_copy` before submission in `processDisplayLists()`; this is a ready entry point for studying local geometry replacement. Existing fonts, avatars and world maps have been converted to high-definition to `loadReplacementDirectory()`, which is a texture replacement.

The fixed RT64 used is `43373749dac9bbc1b653e6a02aed40a9e1783bed`. Its README and the [upstream description](https://github.com/rt64/rt64#features-in-development-in-priority-order) of this check still list Model replacements as under development. The current host does not have glTF/FBX/OBJ model replacement package loader, and cannot promise that the model can be replaced by putting it into the texture package directory.

Currently completed experiments and follow-up projects:

1. **The mission replay and the actual opening of 5600 have been passed. ** The original position, size and dashed ring are used after the diamond 8 → 96 surface, and the difference between the real game comparison frames is limited to the diamond check area. Keep the original display list entry, append the new geometry to the resource and use the segment 4 relative pointer. The original loader is responsible for the resource memory; the snapshot fixed address is not brought into the runtime.
2. **Universal grid import and wider coverage still need to be implemented. ** Currently it is a 5600-specific compiler, and the OBJ/glTF import and arbitrary scene recognition system has not been established. Other resources still need to be verified separately for material, transparency, depth, cropping, camera, capacity and life cycle; re-entry and archive recovery of 5600 have not been accepted.

ROM direct swapping is still constrained by compression capacity, memory, and legacy display lists. The 5600 experiment solves capacity growth by redirecting resource table entries to the ROM blank pool; this only proves that the resource and this process are available. The native host can also provide additional asset and rendering access, and the existing high-definition texture function will not automatically provide universal geometry replacement.

## Recommended priority order

| Sequence | Object | Reason for selection and next verification |
| --- | --- | --- |
| 1 | 5600 plot marks | 96 experimental ROM opening runs have been completed to verify rotation, position changes and cuts; subsequent re-entry, archive recovery and more routes will be added |
| 2 | A common combat background | The highest visible benefit. Capture stable frames during the battle, bind the ground, distant views and buildings to IDs respectively, and then make a single scene sample |
| 3 | A ship that has been bound to the scene | The mesh can be extracted; first add the texture and lens ownership, verify the components, orientation and movement, and then expand to other ships |
| 4 | Three-dimensional plot world map | The original version is flat, and mountains or landmarks can be added; the coast, place names/plot mark positions and the original lens performance must be maintained |
| Follow-up independent direction | Full 3D tactical chessboard and full 3D combat body | The former requires map scene generation and selection/occlusion rules, while the latter requires action and weapon performance systems; the scope of work is significantly larger than the replacement of existing geometry |

The current recommendation is "2D performance of the original airframe + more refined scene geometry + high-definition textures", first using mark verification technology, and then using the combat background to verify the screen benefits. The naming of all route assets and the coverage of all scenarios have not yet been completed. This report gives the verified entrance and candidate range.