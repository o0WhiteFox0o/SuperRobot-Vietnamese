> **Language / Ngôn ngữ:** [English](story-reader.en.md) · [Tiếng Việt](story-reader.vi.md) · [中文](story-reader.md)

# plot review station

2026-09-12. Following the continuous dialogue, character avatar, chapter navigation, full-text search and sentence-by-sentence positioning methods of the Z review station, the original script extracted by SRW64 is used to generate a read-only page.

## Start and read

```sh
.venv/bin/python -B tools/content/extract_original.py
python3 -B tools/data_viewer/serve.py --port 59110
```

Open <http://127.0.0.1:59110/story.html#scene=1>. The catalog includes 142 scenes and 34,369 dialogue quotes; shared scripts are counted separately in each scene and are not equal to the number of independent texts or the number of playable levels.

- Search by title or scene number in the left column; previous/next chapter moves by scene index, and the "From/Flow to" link under the title comes from the original script `3D4B`.
- Full text search supports Japanese text, speaker and text number, at least two characters; can be limited to this chapter. If there are more than 200 items, the total number will be displayed and prompted to narrow the range. The truncated number will not be regarded as the total number.
- Click "Go" next to a search result or sentence to get a copyable link, such as `#scene=1&line=0019c1b0-1c`. The identity consists of scene, event ROM address, instruction offset, and does not rely on list line number.
- You can filter by opening, initial configuration, battlefield events, and ending, and jump directly to the events in this chapter. The event header holds a summary of the triggering conditions.
- The route filtering of the four protagonists only controls the protagonist paragraphs. Common segments and selected limbs are still retained; the relative speaker whose route has not been determined displays a candidate list and a question mark by default, and the corresponding avatar is displayed only after a compatible route is selected.
- Names alternate between blue and orange when the speaker changes. The avatar, conditions and performance tips, original number and font size can be adjusted; the browser saves reading preferences and last position.

The original text line breaks are retained, and page turning is marked with `▸`; dynamic names use placeholders.

Starting from 2026-09-23, you can select Chinese, English or both in "Translation", the translation will be displayed under each original sentence, and the translation will be displayed under the chapter title. The source is marked before each translation: entry, handwriting, machine translation, review, failed; the reasons for review and machine translation questions are placed in the hover prompt. The translation data is written from `tools/translation/export_review.py` to `assets/original-data/translations/<locale>.json`. The draft can also be read and translated before being merged into the language directory. For the process, see [Full-text Chineseization Planning](../design/translation-plan.md). Rerunning `extract_original.py` will completely replace `assets/original-data/`, and then you need to rerun `export_review.py`. The page can only be read, and cannot be modified or submitted for review online. There is no account system.

## Reading boundaries

Events unfold in entry order, and the actual execution path of the game has not yet been calculated. Turns, defeats, variables, and selection results may be mutually exclusive, and the page will retain them at the same time. Route selection also does not mean that all level conditions have been simulated. When locating a sentence hidden on the current route, the page restores all route segments and prompts.

The protagonist who has been determined based on static basis in this episode will not be renamed with the reader route option; the selected route is only used for the relative identity that has not yet been determined. Complete instructions, original text and maps can be entered into the data map for verification from the page.

## Implementation and checking

- `src/srw64_native/original_story.py`: Construct scene-by-scene plots and search lines, preserving source identities and speaker candidates.
- `tools/content/extract_original.py`: Generate `story/index.json`, 142 scene JSON, `story/search.json`; search data is about 5 MB, loaded and cached on first search.
- `tools/data_viewer/web/story.html`, `story.css`, `story.js`: Read pages. `story-state.js` Pure functions providing routes, speakers, anchors, and searches.
- `tests/test_original_story.py`: Real ROM full source mapping, speaker, dynamic name and search index checks.
- `tests/story_reader.mjs`: stable link, route relative avatar, filter boundary, search range and truncation count.

```sh
PYTHONDONTWRITEBYTECODE=1 make check
node --test tests/story_reader.mjs
```

Static inspection and browser verification only prove that the page is extracted and read, and are not equivalent to verification of game script execution. For the specific method of the next stage, see [Remaining Instruction Semantic Confirmation](script-semantics-confirmation.md).