> **Language / Ngôn ngữ:** [English](hd-ai-exploration.en.md) · [Tiếng Việt](hd-ai-exploration.vi.md) · [中文](hd-ai-exploration.md)

# UI and texture high-definition: Alibaba Cloud AI selection survey

Investigation date: 2026-09-08. Conclusion: Use a combination of font/regular graphics reconstruction, fidelity over-resolution, and constrained generative redrawing to prioritize the verification of cutscene backgrounds and a small number of decorative assets.

Subsequent status: After user confirmation, the first round of 42 model outputs and single-frame map playback have been completed. After looking at the picture, Qwen 3.0 Candidate 2 is preferred for the avatar; mechanical unit icons are not processed, map tiles such as forests are suspended, cutscene maps and UI borders are not significantly improved, and continued generation is suspended. See [Actual measurement results and manual decision by looking at pictures](hd-ai-benchmark.md). The following investigation and plan before calling are retained in this article. The actual quantities, costs and restrictions are subject to actual measurement records.

This time, official document verification, certification model catalog query of existing Bailian business space and current project inspection were completed. No image inference task was submitted, and no game images were uploaded to the cloud; the following quality judgments are candidate solutions, and there is no model effect comparison for this game.

## Existing services and evidence

- Reuse the existing DashScope/Bailian configuration of the SRW Z project, execute read-only `GET /compatible-mode/v1/models` in the North China 2 (Beijing) business space, HTTP 200, and return a total of 249 model IDs.
- Fixed snapshots `qwen-image-3.0-pro`, `qwen-image-3.0`, `wan2.7-image-pro`, `wan2.7-image`, and `qwen-image-2.0-pro-2026-06-22` are listed.
- Local query record: `assets/hd-ai/research/aliyun-hd-2026-09-08/model-catalog.json`. Records do not contain credentials; visibility in the certified directory does not equate to verified inference authority, balance, free credit, actual price, or image quality.
- `imageenhan` of the Visual Intelligence Open Platform is another set of services that uses Alibaba Cloud AccessKey/RAM authentication; the Bailian API Key cannot be used as the credential for this service. The service activation and account permissions have not been verified this time.
- The current project already has a single-frame high-definition font experiment with a real display list, see the font replacement experiment at that time (deleted). Text can be re-rasterized from outline fonts without relying on generative models to guess words. This experiment does not yet cover the real-time text engine and all UI.
- The independent image decoding implementation of the current warehouse covers the I4 font library; other assets such as maps and vertical drawings still need to confirm the resource format, splicing and actual drawing sources. The ability of a resource to be decompressed does not mean that it has been correctly decoded into a replaceable image.

## Select method by asset

| Assets | Preferred Methods | Purpose of AI | What Must Be Preserved |
| --- | --- | --- | --- |
| Text, name, value, menu label | Outline font and deterministic typesetting | Assist in identifying unregistered image text | Original text, control characters, kerning rules, display timing |
| Border, window, cursor, value bar | Vector or parametric reconstruction, and then generate the required texture | Decoration scheme reference | Precise size, alignment, corners of the nine-square grid, status differences |
| Cut scene world map background | High-fidelity contrast + constrained redraw candidates | Supplement texture details such as mountains, land surface, sea surface, etc. | Coastline, city/route location, frame, projection and color palette |
| Static backgrounds such as indoors, sky, ground, etc. | Image editing/super-resolution | Supplementary painting details and materials | Composition, perspective, number of objects, original painting style |
| Avatars, character portraits, mechanical icons | Overscore priority; try redrawing if you have a character setting reference | Clean up jagged edges and supplement lines | Facial features, clothing, emblems, mechanical structures, outlines and transparency |
| Tactical map tiles | Tile types and splicing relationships are confirmed and processed separately | Surface texture candidates | Terrain readability, grid boundaries, repeated tiling and adjacent seams |
| Animation sprites, blinking cursors, combat special effects | Processing and review as a whole set of animations | Verified local assistance | Inter-frame identity, posture, color matching, transparency and rhythm |

The first experiment focused on independent static assets. Generative models that change the animation frame by frame are prone to flickering and shape drift. A single good-looking picture is not enough to prove that the animation is usable.

## Model and API candidates

The following prices are the official original prices published in mainland China on the day of the survey; Bailian is from the Beijing area, and VIAPI image production usually uses the Shanghai area. The unit is RMB, without deducting free quota or discounts. It cannot be inferred from this table that this account has obtained the quota.

| Models/Abilities | Suggested Characters | Confirmed Abilities and Limitations | Single Reference Cost |
| --- | --- | --- | --- |
| `qwen-image-3.0-pro` | High-quality repaint candidates for key comparison | Support image input and editing; official current recommendation; 2K file output | 1 input + 1 2K output about 0.52 yuan; 1K about 0.27 yuan |
| `qwen-image-3.0` | Batch cost comparison of the same solution | Supports image input and editing; whether it is sufficiently fidelity requires sample verification of this project | 1 input + 1 output costs about 0.20 yuan, and the unit price of 1K/2K output is the same |
| `wan2.7-image-pro` | Multiple reference images, local modifications and style consistency candidates | Up to 9 reference images; each image can have up to 2 bounding boxes; edited into 2K files, 4K is limited to specified Vincentian image scenes | 0.50 yuan/output image |
| `qwen-image-2.0-pro-2026-06-22` | Regression comparison of fixed model version | Fixed snapshot; image generation and editing; final output still needs to be frozen | 0.50 yuan/output image |
| `MakeSuperResolutionImage` | Fidelity super-resolution baseline candidate | 1/2/3/4 times; `Mode` has been abandoned, passing it in will not affect the results | 100 free rules per natural month, excess is 0.02 yuan/time; the balance has not been checked |
| `GenerateSuperResolutionImage` | Generative super-score candidate with slight detail filling | 1/2/3/4 times; asynchronous interface; input aspect ratio does not exceed 2:1 | First grade 0.06 yuan/time |

Ability sources: [Bailian Model Overview](https://help.aliyun.com/zh/model-studio/image-model/), [Qianwen Image Editing](https://help.aliyun.com/zh/model-studio/qwen-image-edit-guide), [Wanxiang Image Editing](https://help.aliyun.com/zh/model-studio/wan-image-edit), [Normal Super Score](https://help.aliyun.com/zh/viapi/developer-reference/api-px24vm), [Generative Super Score](https://help.aliyun.com/zh/viapi/developer-reference/api-generated-image-super-score).

Price source: [Qianwen 3.0 Pro](https://help.aliyun.com/zh/model-studio/qwen-image-3-0-pro), [Qianwen 3.0](https://help.aliyun.com/zh/model-studio/qwen-image-3-0), [Wanxiang 2.7 Pro](https://help.aliyun.com/zh/model-studio/wan2-7-image-pro), [Qianwen 2.0 Pro and snapshot](https://help.aliyun.com/zh/model-studio/qwen-image-2-0-pro), [VIAPI billing](https://help.aliyun.com/zh/viapi/product-overview/billing-is-introduced-12).

General super-resolution "more fidelity" is a selection assumption relative to generative redrawing, and is not a promise of lossless recovery; it may also change edges and small details. It cannot be claimed that the model restores true details that were not present in the original image.

`z-image-turbo` is a Vincent diagram model with no image editing capabilities and is not the first choice for faithful high-definition. `qwen-image-edit-max`/`plus` in the catalog can be used as a comparison for old versions, but there is no need to expand the number of models in the first round. The visual understanding model can assist in classification, OCR and finding anomalies, but cannot be the sole acceptor.

## Real restrictions that should be noted when accessing

1. **Small image input**: The minimum normal super score is 32×32, the maximum long side is 1920/short side 1080, and the file does not exceed 5MB; the generative super score is a minimum of 64×64, the long side does not exceed 5000, and the short side exceeds 1080, it will be automatically adjusted, and the ratio does not exceed 2:1. Narrow bars and tiny icons cannot be submitted to all services as-is.
2. **Transparent Channel**: The Wanxiang editing input specification clearly states that PNG does not support transparent channels. Transparent assets should retain independent original masks, and only send the RGB area that needs to be generated to the model, and then synthesize and accept it according to the registered outline rules; the generated white background image cannot be directly used as a transparent texture.
3. **Super-resolution output format**: Normal super-resolution should usually specify PNG explicitly; the document states that PNG will be forced when RGBA is input, but it may be automatically changed to JPEG when the output resolution exceeds 3840×2160. Actual format, size and alpha need to be verified, not just the file extension.
4. **Frame selection does not equal pixel locking**: Wanxiang's `bbox_list` is an editing guide, and it cannot be used to guarantee that pixels outside the frame will remain unchanged. The areas that are allowed to be modified must be synthesized as independent masks, and the protected areas are copied from the deterministic baseline and checked for differences.
5. **Request interface**: The OpenAI compatible `chat/completions` path of the existing text task cannot be directly used as an image editing interface. Qianwen editing guide provides DashScope `MultiModalConversation`, Wanxiang provides `ImageGeneration` and multi-modal generation interface; each adapter constructs a request corresponding to the current document.
6. **Size and prompt words**: Select the output size, aspect ratio, and input size according to the model API; retain the cropping transformation when edge padding is required. For models that support `prompt_extend`, faithful reproduction tests should explicitly turn off automatic expansion to avoid changing censored prompt words. Do not assume that there is a "redraw strength" parameter common to all models.
7. **Reproducibility**: Fixed snapshots, input hashes, request parameters and seeds are helpful for tracking, but the official statement clearly states that the same seed does not guarantee the same output. Publish uses the image that has been reviewed and saved the hash, and does not re-request the model on the production build.
8. **Quota and batch**: The default current limits in Beijing listed on the official card are Qianwen 3.0 Pro 5 RPM, Qianwen 3.0 20 RPM, Qianwen 2.0 Pro Snapshot 2 RPM, and Wanxiang 2.7 Pro 300 RPM; the actual limit is subject to account return. "Batch inference not supported" does not prevent the client from submitting ordinary requests one by one according to the current limit, but it cannot apply batch inference discounts.

The above specifications are based on each model document; the old version of Qianwen editing API parameter table has not yet fully covered 3.0, and the 3.0 request implementation should be based on the current 3.0 examples and actual verification. [Qianwen Editing API](https://help.aliyun.com/zh/model-studio/qwen-image-edit-api)

## The specific process of cutscene map background

1. **Extract the complete basemap**: Locate the original resources and actual RT64 samples, and do not use the final screenshot containing text, characters, marks, and cursors as production input. If the base image is uploaded in parts, first restore the complete image and the cropping, flipping and color palette relationships of each block.
2. **Establish structural protection layers**: Register coastlines, roads, rivers, boundaries and key markers separately. Structures that can be reconstructed from vectors or primitive masks are drawn individually; surface textures, sea surfaces, and clouds are available as editable areas. The baked text in the original image must also be reconstructed separately.
3. **Same source comparison**: The same original image is subjected to ordinary interpolation, ordinary super-resolution, generative super-resolution, thousand-question editing and multi-phase editing respectively. Ordinary interpolation serves as a visual baseline that adds no new semantics.
4. **Limited redrawing task**: Keep the original color palette and hand-painted style, and only supplement the texture of the editable area; the model is not required to turn the map into a realistic satellite photo. The supporting reference drawings are used to unify the art and are not used to replace the spatial layout.
5. **Deterministic synthesis**: Synthesize the approved materials according to the protective layer, and redraw place names, routes and markers. Switch back to high-definition tiles according to the original sampling relationship, and unify the proportion, edge expansion and filtering methods.
6. **Runtime Acceptance**: Bind to confirmed RT64 texture hash, check for seams, misalignment, chromatic aberration, transparent edges and sample flicker during pan, zoom, transition and fade. The cutscene basemap and tactical map tiles will be accepted separately.

Suggested word starting points for wordless basemaps (spatial constraints are ultimately still guaranteed by the structural layer and manual review):

> Use Figure 1 as the only spatial layout benchmark, keeping the same frame, projection, camera direction and original painting color palette. Preserve the location, shape and number of coastlines, rivers, roads, islands and cities. Based on the original two-dimensional hand-drawn science fiction strategic map style, the clarity of surface and sea surface textures is improved, and the existing mountains and vegetation are refined. Preserve large-block color relationships and terrain recognition. Outputs a map basemap without text, labels, units, cursors and interfaces, and does not add new features.

## First round comparison suggestions and costs

There are 6 original assets to be extracted and registered: two cutscene maps of different styles, a scene background, an avatar, a mechanical icon, and a UI decoration texture. Here are sample category suggestions, 6 resources have not yet been located and populated into the executable list.

Per sample:

- Qianwen 3.0 Pro, Qianwen 3.0, and Wanxiang 2.7 Pro each independently request 2 candidates (one input and one output each time).
- Qianwen 2.0 Pro fixed snapshot request 1 comparison.
- One comparison each for ordinary super score and generative super score. Confirm its activation and input conditions before adding it.
- Local ordinary interpolation is used as an additional baseline, regardless of the number of images produced in the cloud.

A total of 54 photos were output to the cloud. Estimated based on the 2K price of Qianwen 3.0 Pro, all request form inputs, and the above prices of other models:

`6 × [2 × (0.52 + 0.20 + 0.50) + 0.50 + 0.02 + 0.06] = 18.12元`.

This is the cost of a reference test that was not performed and is not a bill or budget authorization. Retries, additional reference images, storage traffic, and free credits are not included; there is no need to purchase GPU instances or train models for this round of testing.

Predefined by asset via criteria:

- **Structurally correct**: Landmarks, coastlines, mechanical parts, and character identities have not been tampered with; incorrect candidates will be eliminated even if they are sharper.
- **Engineering Correct**: Dimensions are consistent with texture mapping, protected areas pass diff checks, transparent outlines have no white edges, tile seams are correct.
- **Visually Valid**: Compare readability, style consistency and detail at the target game display size, rather than just viewing an enlarged static preview.
- **Run correctly**: Complete the scrolling, zooming, overlaying and animation comparison of the target scene; the passing of static pictures does not mean the acceptance of real-time rendering.
- **Cost Effective**: Statistics of the review pass rate, the number of requests for each qualified asset, and manual retouching time are used to determine the batch model. The single API price is not the full production cost.

## Subsequent asset recording and release

Each item records the original resource ID, source image hash, RT64 sampling/hash, palette and mask, complete model ID, call date, prompt words and parameters, candidate hash, review conclusion, output size, composition/tile transformation and runtime evidence. Models that do not provide fixed snapshots should be recorded as floating service versions, with output frozen after review.

HD assets are carried by independent RT64 texture packs. AI generation only occurs in the offline production stage, and the reviewed results are loaded when the game is running; assets can be reused on desktop/Android and other platforms, and the format, video memory, and sampling effects are verified separately. Texture pack production, compression, and preloading strategies are implemented according to [RT64 Texture Pack Document](https://github.com/rt64/rt64/blob/main/TEXTURE-PACKS.md).

No modifications were made to the game code, ROM, existing font packages or runtime configuration at this time. Model effect testing, target cutscene background extraction and HD package acceptance are still follow-up tasks.