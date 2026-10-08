> **Language / Ngôn ngữ:** [English](translation-plan.en.md) · [Tiếng Việt](translation-plan.vi.md) · [中文](translation-plan.md)

# Full text localization: text export and Chinese-English translation

Date: 2026-09-23. This document explains the following things:

- How to export all text;
- Who is responsible for translation;
- How to use DeepSeek on Alibaba Cloud Bailian to produce a first draft in Chinese and English and do AI review;
- How to give the translation to the game;
- What steps are left after that.

Numbers are derived from actual calls and production results for the day.

## Conclusion

- **EXPORT**: Covered all 51,174 ROM text records, 30 pages of opening scale text (human transcribed), and 244 pieces of native UI copy, each grouped into a category with context. The export tool checks two things: each record occurs exactly once, and the plot area (starting at 17347) exactly matches the 33,628 text numbers actually referenced in the script.
- **Division of labor**:
- The name, interface, and system prompts (the parts of records 0–5798 that need to be translated) are listed in the entry list, and both Chinese and English sets have been completed by another session. See [Data text Chineseization: entry list and translation specifications](../native/localization-terms.md);
- The plot dialogue, body selection, battle lines, and opening prologue follow the machine-to-machine translation process of this article. Person names, machine names, and weapon names are all taken from the entry list. There is also a Chinese and English vocabulary list (`content/translation/story-terms.json`) for unique proper names in the lines.
- **Completion status (2026-09-23)**: The full first draft and one round of AI review in both Chinese and English languages have been completed.
- The first draft uses `deepseek-v4.1-flash` (DeepSeek with the latest version number in the business space), items that fail to be checked are retried for three rounds, and `deepseek-v4-pro-0813` is used in the final round.
- Use `deepseek-v4-pro-0813` for review.
- Result: 45,197 out of 45,206 Chinese items passed all mechanical inspections, and 45,139 English items passed; 2,114 Chinese items and 1,931 English items were revised.
- **How to hand it over to the game**: The lines decided by the user are made into a text file that can be changed by the player and are not merged into the language directory.
- `tools/translation/write_dialogue.py` has been written `content/dialogue/{zh-Hans,en}/`, 422 files per language, with 45,013 machine translations, 70 templates to be translated and 30 pages of openings.
- There are another 93 pieces of handwritten dialogue in `story/scene-0001.txt`, which is not altered by the generator.
- The reading end is implemented by another session (`da649d3`), and the expansion results of C++ and Python are consistent one by one, with zero errors.
- **Cost**: All calls cost about 50 yuan based on the flash price; of which the review and the last round of re-trials were pro, and the price of pro is subject to the console.
- **Next step**: Mainly manual review (the only original text is about 910,000 words) and display access.
- **Dialogue Typesetting (Defined on 2026-09-23)**: HarmonyOS fonts are packaged in a unified way, and the English font size is 0.85 times the font size. One line of dialogue is arranged in a row, and the original page turning points are only synchronized. The name remains in the box but the name line is tightened. According to simulation, the number of page turns is reduced by 24% in Chinese and 37% in English, see [Dialogue Typesetting](dialogue-typesetting.md).
- Plot dialogue can now be displayed in the game;
- The battle lines have been connected, and the actual machine verification on 2026-09-23 that the switching between Chinese and English is normal;
- The opening prologue, chapter title card and ending page 2026-09-24 have been drawn natively in the reading language, see [Title Screen and Plot Text Picture](../native/native-title-and-story-images.md); the choice of limbs and victory and defeat conditions have not yet been connected.
- On the plot review page, you can compare the original text with the Chinese and English translations (see P3).

## 1. Export

```sh
.venv/bin/python -B tools/content/extract_original.py      # 先有原始数据目录（make recomp-data）
.venv/bin/python -B tools/content/export_text.py           # → assets/text-export/
```

The output contains the original Japanese text, which is only placed in `assets/text-export/`, which is ignored by git, and replaced as a whole each time. Complete in about 2 seconds.

| Documentation | Content |
| --- | --- |
| `manifest.json` | ROM, production code and input file summary, each category count, number interval table, control character and tag description, SHA-256 of all output files |
| `records.jsonl` | One line for each record: `key`, `category`, `group`, basis (`code`/`content`/`transcribed`), lossless original text `source` (inclusive) `<BR>`/`<STOP>`/`<G:XXXX>`), `display` (dynamic name folded into [protagonist name], etc.), `source_sha256`, visible word count, tags, `native_page`, `terms_section`, Chinese and English translations available, and context by category |
| `summary.md` | Number of records in each category, number of unique original texts, number of words, native pages and entry table coverage |
| `categories/*.csv` | One table per category (UTF-8 BOM, can be opened directly with Excel): key, context summary, original text (⏎ means line break, ▸ means page turn), mark, existing translation |
| `story/scene-NNNN.json` | 142 scenes, listing the events, stages, triggering conditions, route segments, speakers and candidates, and dialogue modes of each sentence in script order |
| `battle/speaker-runs.json` | The battle lines are in the order in the table and the same speaker is one continuous paragraph (1,524 paragraphs) |
| `battle/triggers.json` | The battle line selection table is organized by voice (2026-09-27 reverse, see [battle-quotes.md](../data/battle-quotes.md)): nine common segments for each voice, as well as condition codes, interpretations of conditional lines, and record number sequences of multi-person conversations |

Context fields differ by category:

- Plot: All locations appear. Shared scripts will appear in multiple scenes, with the first one serving as the main context.
- Combat lines: speaker (the first three digits of the text header), the paragraph and the position within the paragraph, the starting sentence of the combined skill (the text header is suffixed with `0024`); `triggers` (interpretation of trigger conditions such as situations, weapons, opponents, co-pilots, combined skills, etc., and the sequence and position given in multi-person conversations), `voice` and `voice_actors` (voice number and the character who possesses it).
- Name: body/weapon/character number, and corresponding records, such as weapon menu name ↔ pure name, abbreviation ↔ full name, spiritual name ↔ description.

Tags:

| Mark | Meaning |
| --- | --- |
| `numeric-gap` | The original version draws numbers in the spaces, and the translation must retain the spaces |
| `fragment` | Sentence fragments spliced together at runtime |
| `dynamic-name` | Contains dynamic name |
| `paged` | Contains `<STOP>` Page turn |
| `blank` | No visible characters |

Implemented in `src/srw64_native/text_export.py` (classification and context) and `tools/content/export_text.py` (writing files), tested in `tests/test_text_export.py`.

### Classification and basis

The numbered interval is compared section by section; the interval confirmed by the code formula is marked `code`:

- Episode 281 + Scene
- Aircraft 527+ airframe
- Spirit 969＋No.
- Size 1094+ size
- Parts 1129＋Parts
- Weapons 1370/2699+weapons
- Inter-scene and screen labels 4044–4144
- Characters 4382／4743＋Characters
- Plot dialogue and body selection

The remaining intervals are divided by content and marked `content`. The number directly used by the native page is taken from the constant of `src/host/*_page.cpp` and recorded in `native_page`.

| Responsible | Category (number of records) | Number of visible words |
| --- | --- | ---: |
| **This article is translated from the machine** | Plot dialogue 33,582, choice of limbs 46, opening prologue 30, battle lines 11,534, special battle lines 14 | 1,145,144 (only 908,925) |
| **entry list** (another session) | Word name 143, victory and defeat conditions 73; body 363, weapon 1,329 (menu name 1,329 derived from this), character abbreviation/full name 361 each, default name 16, character list 108; spirit 30 and single-character abbreviation 30, special ability 15, skill 79, parts 20, terrain 60, work title 50; interface label 260, system prompt 65, new game and name input 27; spirit/parts/modification/counterattack instructions 96; title option 7 | About 36,000 |
| Native UI (`ui` table, manual maintenance) | 244 items; both Chinese and English are provided | 2,777 |
| Copied, not translated | Body model 115 (only the non-model text in the entry list is translated), map icon 46, scale bar and page turning arrow 123 | — |
| Not displayed or has been replaced | Debugging text such as battle animation editor, plot logo editor, etc. 421; original name dial 223 | — |
| **To Be Determined** | Song Title 49, Karaoke Lyrics 199 (Tables 1–19 of 20) | 3,313 |

### Text not in the text table

- **Opening Zoom Text**: 30 pages, public prologue 11 pages, four routes 5–6 pages each. They are texture images, not text records.
- 2026-09-23 has been manually transcribed line by line, there is `assets/transcriptions/intro-pages.ja.json`, and each page is attached with picture SHA-256; when the picture changes, the export will report an error.
- The export key is `intro:<资源号>`, with playback route and sequence attached.
- Which protagonist corresponds to Route 1/3/4 is inferred based on the text content: a boy from the martial arts fighting style, a boy born from a colonial satellite, and a guerrilla girl. Route 2 has been confirmed to be Malino by the actual machine.
- 2026-09-27 Page-by-page translation of Chinese and English by Claude (batch `read-fixes/intro-close.json`), see [Line Polishing Plan](dialogue-polish-plan.md) Stage 2c.
- **Chapter Title Cards**: 133 images (`assets/original-graphics/chapter-titles/`). 2026-09-24 Recognize each picture and compare it with the name of the call one by one. The game is drawn according to the translation of the call name ([title screen and plot text picture](../native/native-title-and-story-images.md)).
- **End Page**: 7 (5570–5576). 2026-09-24 Transcribed and handwritten Chinese-English translation, placed in `content/dialogue/<语言>/ending.txt`, also drawn natively; 2026-09-27 refined.
- **Other text baked into the picture**: battle special effects words, title logo, etc., have not yet been counted by the system. This article makes no claims to have been covered.

## 2. Division of labor and writing boundaries

- **Term table**: Names and system texts are maintained by partition by `content/locales/terms/<locale>.json`, and each different original text is only translated once; `tools/content/apply_terms.py` is expanded into language directory entries (`"origin": "terms"`). Machine translation does not write these keys.
- **Machine translation draft**: `assets/translation-runs/<tag>/` exists first, one copy for each batch, saves the request context, usage, and check results one by one, and can continue running. `run_mt.py collect` organizes the checked entries into language directory format (`"origin": "mt"`, `"review_status": "draft"`, with model, prompt word version, and batch tag), and verifies them with `compile_locale`.
- **The final destination of the lines (updated on 2026-09-23)**: The user decides that the plot and combat lines are made into independent text files (tentatively `content/dialogue/<locale>/`). Players can modify them themselves. The files attached to the program can be overwritten by files with the same name in the user directory. Lines are not merged into `content/locales/*.json`, nor into embedded import specs.
- The file format, reading, verification and overwriting are handled by the term table session, and the file content is produced by this process; after the format is finalized, `collect` will be directly output in the new format.
- One of the reasons for giving up merging into the language directory is the size. According to actual measurements, if 45,013 lines in Chinese and English are merged, each language file will increase from about 1.1 MB to 13.5 MB, the import spec used for embedding will increase from 1.7 MB to about 23 MB, and the generated C++ header file is estimated to be about 76 MB (currently 5.6 MB).
- **Character Card**: SRW64 The gender, identity and voice of the original character are written in `content/translation/zh-Hans/roster.json`. The translation is not determined here, the translation is still based on the entry list.

## 3. Machine translation process

Tools in `tools/translation/`:

| File | Function |
| --- | --- |
| `run_mt.py` | Batch, request, check, correct (`run`), AI review (`review`), recheck (`recheck`), report (`report`), organize into language directory format (`collect`, subsequent batches overwrite the previous ones) |
| `run_full.sh` | The whole process of a language: two drafts (the second pass is only for failed batches), two proofreads, and a report |
| `dashscope.py` | Bailian OpenAI compatible interface |
| `references.py` | Vocabulary and character cards (Chinese and English) |
| `term_candidates.py`, `draft_terms.py`, `audit_terms.py` | Candidate, drafting and consistency audit of line names |

The logic to ensure that the translation structure is correct is in `src/srw64_native/translation.py`, and the test is in `tests/test_translation.py`.

```sh
export SRW64_DASHSCOPE_ENV=<百炼 .env>
tools/translation/run_full.sh zh-Hans zh-v1 draft      # 或 review / all；en 同理
PYTHONPATH=src .venv/bin/python -B tools/translation/run_mt.py collect --tag zh-v1 --tag zh-v1-review --output <zh 文件>
```

**AI review (`review`)**:

- Use `deepseek-v4-pro-0813`, maximum 70 sentences per batch. The model sees the original text and the first draft, and only returns the items to be changed and the reasons (in Chinese).
- Changes must also pass all mechanical inspections. Changes that are the same as the first draft or cannot be inspected will not be adopted.
- The latest entry list and line names are loaded during review, and names decided after the first draft can also be unified in this round.

Credentials are read from `--env-file`, `SRW64_DASHSCOPE_ENV`, or the repository root `.env` (ignored by git), and are only sent to the HTTPS address of `*.aliyuncs.com`. The trial run used the existing North China 2 business space configuration of the Chinese version of "Mech Z".

Request parameters: `temperature 0.1`, JSON output, turn off thinking; only retry on 429 or 5xx. I tried thinking mode in the special chapter of "Mech Z", but reasoning would exhaust the output limit, so I didn't use it.

### Guaranteed to load

Each source text is cut into pages at `<STOP>`, and the selection limb is cut into options at `<BR>`. In-page processing:

- Remove `<BR>`, and the native dialogue box will automatically wrap lines and paginate;
- Each string of characters in the dynamic name becomes placeholders such as [Protagonist’s Name] and [Partner’s Nickname], and other special glyphs become ⟦G1⟧.

The model must return an array with the same number of pages, and the number and order of placeholders must remain unchanged. When restoring, the original code string is put back as it is, so the page structure and `signature` are consistent with the original text. Any discrepancy will result in an error and no silent repair will be done. `<` and `>` in the translation will be replaced by full-width characters, and the model cannot write control characters.

### Batching and context

**Plot**: Batch by scene, no more than 40 sentences or 2,400 words per batch. Sentences in a shared script are only translated in the first scene where they appear, and are used as read-only context (`ctx`) in other scenes. The batches of the same scene are run in order, and the latter batch contains the original text and translation of the last 8 sentences of the previous batch; different scenes are run in parallel. There are 904 batches in total. Each batch comes with:

- Scene title and protagonist;
- Stages, route segments and triggering conditions for each sentence;
- Speaker character card: The Chinese name is taken from the entry list, the original character is taken from the roster, and the characters of existing works are taken from the introduction and gender of the Chinese illustrated book of "Mech Z", for reference only;
- Related word lists: "Must-use" comes from the name, body, weapon, and work name divisions of this project's entry list. There are three exceptions that are only for "reference": 1-2 character names (コウ, masterpiece, nin), hiragana names (ひかる), ボス, マスター and other common words. Hiragana weapon names (した, くちばし) do not participate in matching; spirits, abilities, and parts are only for "reference". Another part of the "reference" comes from the proper name category of the Chinese vocabulary list of "Mech Z". It only accepts Japanese items that have not yet been determined in the entry list of this project, and removes items that are only written in English.

**Battle Lines**: One batch every 60-80 sentences according to the order in the table, try to cut when the speaker changes, a total of 164 batches. Before about No. 14000, it was a common situation block for each character. The approximate order was attack → being shot down → big damage → small damage → avoidance → defense beam → out of range/out of range. This is followed by weapon-specific lines and multi-player combo skill dialogue. The selection table has not yet been reversed during machine translation, and the prompt words only give descriptions of the speaker and section; the reverse was completed on 2026-09-27 ([battle-quotes.md](../data/battle-quotes.md)), and the intensive reading stage was reviewed by voice and trigger conditions (`tools/translation/read_battle.py`).

**Opening Prologue**: A batch of 30 pages, corresponding to paragraphs.

### Check and correct

Check the following items item by item; for items that cannot be checked, write the question in Chinese and resend it again, only retranslate these items:

- Page number, placeholder, control character;
- Empty translation;
- Remaining pseudonyms;
- Unconverted "" "";
- Whether the entire quotation marks are in pairs;
- The length ratio of the translation to the original text.

If the "must use" translation does not appear, it will only be recorded as a warning and will not be automatically retransmitted to prevent names such as "ボス" that are also ordinary words from being forcibly replaced. Questions marked by the model itself (unclear references, puns, new translations) are written in `flag`.

## 4. Trial run results (2026-09-23)

Scope:

- Scenes 0-2 of the plot: The first episode of the three routes of ブラッド, マナミ, and アーク, with a total of 273 sentences, including speakers named according to route sections;
- Battle lines 5813–5912 (general block of コウ/ガトー) and 15340–15420 (multiplayer dialogue of ファイナルダイナミックスペシャル), a total of 181 lines;
- Opening 30 pages.

| batch | number of items | pass | input/output tokens | description |
| --- | ---: | ---: | --- | --- |
| Plot, prompt words v1 | 273 | 263 | With correction wheel | 9 sentences combine two pages into one page, and 1 sentence leaves a blank page; the correction prompt of v1 is in English and has not been repaired |
| Plot, prompt words v2 | 273 | 272 | 35,373 / 8,461 | Mark the page number for each sentence, and stipulate that quotation marks should be placed at the beginning and end of the original text; the correction wheel has fixed 2 sentences, leaving 1 sentence (8 pages to 7 pages) for manual processing |
| Battle lines | 181 | 181 | 10,645 / 3,846 | Passed all in the first round |
| Opening Prologue | 30 | 30 | 3,104 / 1,917 | Model marked with 3 new translations |
| Plot scene 1, `deepseek-v4-pro-0813` comparison | 93 | 92 | 15,142 / 3,777 | 68 out of 93 sentences in flash are worded differently |

The mechanical check of the v1 batch once reported 94 errors, most of which were caused by the checker judging whether the quotation marks were paired based on a single page: the quotation marks of the dialogue originally opened on the first page and closed on the last page. The entire judgment has been changed, and the saved results have been rechecked with `recheck`. v1 All 13 lots are priced at $0.26 (priced based on busy hours).

Observations from manual reading:

- **Tone**: The honorifics of the butler Rurasu, the coldness of Kara, and the maniacal laughter of the Dark General are all shown; "Mukiha Ken-ryu" is correctly converted to "Mukiha Ken-ryu"; [Protagonist's full name] and other placeholders are in the correct position.
- **Inconsistency**, all because the entry list only had 73 seeds at that time:
- アースゲイン There are three translations of Earth Gein/Ax Gein/As Gein;
- スイームルグ is translated as Siimlug, and the entry list is Swaimlug;
- ムゲゾルバドス appears in two ways of writing: Mugai/Muge;
- おじい様 is sometimes translated as grandpa and sometimes as grandpa in the same sentence.
- **flash and pro**: pro is slightly concise in wording and consistent in title; flash is slightly more literal. Neither is an obvious mistranslation.
- **Period at the end of sentence**: When there is no "." at the end of the Japanese page, the translation will probably not add it, but it is not completely consistent. This requires a uniform rule (see Section 8).

## 5. Full results (2026-09-23)

| | Chinese (`zh-v1`) | English (`en-v1`) |
| --- | ---: | ---: |
| Number of entries (story 33,628 + battle 11,548 + prologue 30) | 45,206 | 45,206 |
| Passed mechanical inspection after first draft | 45,110 | 44,962 |
| Passed after three retries | **45,197** | **45,139** |
| Input/output tokens for first draft and retry | 6.42M / 1.28M | 7.60M / 1.48M |
| Cost based on flash price (busy time/free time) | 22.1/11.0 yuan | 24.0/12.0 yuan |
| Reviewer: Reviewed / Modified | 45,127 / 2,114 | 45,139 / 1,931 |
| Review tokens (pro) | 5.00M / 0.72M | 5.18M / 0.95M |

- **First Draft**: Two languages are run at the same time, 6 parallel routes each, about 1 hour for each language. Both languages ​​had a "Two JSON objects in reply" issue once in the first 20+ batches, and the parser has been changed to merge multiple objects.
- **Content review interception**: A batch of Chinese files were rejected by Bailian's input review (`data_inspection_failed`), and the same batch of English files passed. `retry` When encountering this situation, first remove the context, then divide it into single sentences, and finally translate this batch separately.
- **English placeholder**: The placeholder in the first draft of English initially uses Chinese labels, and the model will "translate" [Partner's Name] into [Partner's Name], accounting for 118 failures. Try again after using ASCII placeholders such as `{PartnerName}`, and this type of failure will basically disappear.
- **Inspector tweaks**:
- The length ratio is changed to be calculated based on the whole line, and Japanese characters are weighted by character type (katakana counts as half, long sounds and lowercase kana are not counted), otherwise shouting moves such as ライトニングソォォォォード→Lightning Sword will be falsely reported;
- Added Japanese honorific check (`-sama`, `-san`) in English.
- **Remaining failed**: 9 Chinese items and 67 English items, mostly due to page merging and missing `{HeroMech}`. These items are written as templates for translation in both languages ​​in the lines file, with draft notes attached.
- **Review**:
- Initially had the review model return using the `tr` field, which often copied the first draft. After changing to a separate `revised` field and requiring it to be different from the first draft, the changes were really implemented.
- The main changes include: mistranslation (call out せんのか), Japanese wording (发jin→departure), pronouns and addressees, さん→Mr., and missing quotation marks.
- The reviewer will add periods to the Chinese text, which conflicts with the rule of "end-of-page punctuation follows the original text" (see Section 8).
- 2–3 batches each failed twice due to response truncation, and these batches retained the first draft.
- **Punctuation at the end of the page (2026-09-24, `zh-v1-joins`)**: After the game was changed to a whole series, the actual machine found that Chinese often lacked punctuation at the original page turning, and the two sentences before and after were stuck together. The reason is the v4 rule "Punctuation at the end of the page follows the original text": Japanese pages often do not have periods at the end.
- Scale: About 5,200 of the 13,358 page turns in Chinese have no punctuation, involving 4,347 items. English does not need to be processed: the 304 places where the page ends with a letter and the next page begins with a capital are almost all proper name spreads.
- How to do it: `run_mt.py joins` Let `deepseek-v4-pro-0813` read through the entire connected Chinese text (with the original Japanese text attached) to fill in the punctuation. The program compares words word for word, retaining only the punctuation points (.,!?, etc.) inserted exactly at these page turns, discarding all other changes, and leaving the existing punctuation marks unchanged; 39 missed answers were re-questioned with `--missing`.
- Result: 401 items have been changed, and 477 periods, 6 commas, and 6 question marks have been added; the remaining 4,700 items are judged to be sentences that continue across pages (such as "Master will cry under the Nine Springs |") and are not added. Input 0.47M, output 0.16M tokens.
- Closing punctuation on the last page (`zh-v1-final`, `zh-v1-final2`, `joins --final`): There are 3,057 (9%) lines of plot dialogue that do not have end-of-sentence punctuation before the closing quotation mark. The remaining 91% already have them, so they are all added. Only allowed before the closing quote or parenthesis. ! ? ..., the model moves periods into quotation marks when placing them outside quotation marks.
- Result: 2,967 items have been added; 59 items are left, and the model determines that no need to add them is needed.
- About 400 items were missed in the first round because the model wrote the period outside the quotation marks and the program did not recognize it. After it was changed to accept this writing method, it was made up in the second round.
- Half-width exclamation points and question marks: There are 74 places in Chinese that use the half-width ! ? of the original Japanese text. When writing lines, change them to full-width! ? ; The period immediately following the ellipsis ("...", 171 places, mostly copied from Japanese in the first draft) is also deleted when writing (`chinese_marks`).
- Two methods were eliminated during the trial run: one method was to let the model directly give the complete punctuation at the end of each page, which resulted in deleting the originally correct "!?"
- **Normalization before writing**:
- When the original text is a pair of "..." or (...) spanning all pages, it should be unified into an open quotation mark on the first page and a closed quotation mark on the last page. This step corrects the problem of missing quotation marks in the model or adding a pair of quotation marks on each page: the number of English incompatible items is reduced from 888 to 47, and the rest are cases where there are multiple pairs of quotation marks in one sentence, and no changes are made.
- The original batch results are unchanged.

## 6. Stage

| Stage | Content | Status (2026-09-23) |
| --- | --- | --- |
| P0 Export | Section 1 of this article | Completed |
| P1 Names and proper names | Two sets of entry lists in Chinese and English (another conversation); 647 candidates for proper names of lines. After drafting in Chinese and English, Claude checked and corrected 37 items, and 12 truncated fragments and 1 common word were relabeled, and finally there were 269 proper names; consistency audit with the entry list | Completed; 2026-09-24 The final draft will be checked together with the official translation (see "Official Translation of Proper Nouns"). The final writing method shall be `renames.json`. The `status: draft` in `story-terms.json` has not been backfilled |
| P2 first draft | 45,206 items each in Chinese and English, including retries | Completed, pass rate 99.98% (Chinese) / 99.85% (English) |
| P3 review | One round of AI review has been completed. Manual review can be carried out in the "Translation" comparison on the plot review page: `tools/translation/export_review.py` generates data, the source of each sentence mark (entry, handwriting, machine translation, review, failed), the reason for review and machine translation questions are displayed in the hover prompt | AI review completed; manual review has not started |
| P4 written as a line file | `write_dialogue.py --runs zh-Hans=zh-v1,zh-v1-review,zh-v1-joins,zh-v1-final,zh-v1-final2,zh-v1-names,zh-v1-fixes,zh-v1-names2 --runs en=en-v1,en-v1-review,en-v1-fixes` Write `content/dialogue/<locale>/`: the plot is based on the scene, and the battle lines are based on the voice, one file per person (`battle/speaker-NNN.txt`, NNN is the character number with the voice; first the common segments of the nine situations, and then the conditional lines in the order of the table, each with `# 触发：` annotation; 2026-09-27 (starting), 39 sentences without table quotations are in `battle/other.txt`, and there are `battle/special.txt` (flagship captain) and `intro.txt`. Only rewrite files with generation tags; use `dialogue_text.load` to verify that the two languages have zero errors and have the same key set before writing out | Completed, not yet submitted |
| P5 display access | Plot dialogue and combat lines (`27b221e`) have been accessed, and have been verified on 2026-09-23. F7 Chinese/English/Japanese switching; opening prologue, chapter title card, ending page 2026-09-24 access (native drawing, no original image left); limb selection window, combat purpose window not accessed | In progress (another session) |
| P6 actual machine acceptance | The first episode of the four routes, some divergent episodes, combat line sampling, archiving and loading | Not started |

In the future, if the vocabulary list, prompt words, or proper names are manually determined, just rerun the affected parts. Both `run_mt.py` and `write_dialogue.py` support continuation and overall regeneration, and overlay files placed by players in the user directory will not be affected.

## English version

Chinese and English languages share the same set of export, batching, placeholder protection, checking and merging processes. Only the language rules and vocabulary sources of prompt words are different. English is translated directly from Japanese without Chinese translation to avoid superimposing errors twice.

- **Vocabulary**:
- The name comes from the English version of the entry list (`content/locales/terms/en.json`, finalized in the same batch as the Chinese version);
- The proper name of the line comes from the `en` field of `content/translation/story-terms.json`;
- The Chinese reference vocabulary of "Mech Z" is not used in English.
- **Character Card**: The English name is taken from the entry list. The gender and identity description of the original character, the gender in the "Mech Z" illustrated book, the works and the introduction (Chinese) are all in two languages, and the model can understand them.
- **World view explanation**: All proper names in the prompt words should be written in the original Japanese name (ムゲゾルバドスEmpire, etc.), not in Chinese, to prevent Chinese translations from seeping into English.
- **Writing**: Following the practice of the existing 153 English drafts, the dialogue is wrapped in curly quotation marks " ", お嬢様 = "my lady". See Section 7 for additional rules.
- **CHECK**: Checks done in both languages are for page number, placeholder, residual kana and whole quote pairs. In English, check the following items in addition, any one of them will be reissued:
- Remaining Chinese characters;
- Full-width punctuation;
- direct quotation marks;
- Romanized honorifics, such as `-sama`, `-san`. "Banjo-sama" appeared once in the test run, so this item was added.
  
The length ratio threshold for English is relaxed to 0.6–8.
- **Coverage in two languages**: Both languages will be completed as much as possible; if there are entries that only pass the check in one language, the other language will fall back to Japanese. The lines are not entered into the language directory, so they are not subject to the constraints of `tests/test_english_locale.py` "Chinese and English key sets must be the same".

The English test run (same range as Chinese, 484 items) all passed the inspection in the first round, and the correction round was only used once. Manual review:

- コウ’s battle lines are short and natural, such as “Why you—!!” and “Take this!!”;
- The honorific of ローレンス corresponds to "My lady... Where shall I bring it for you?";
- The combined skill "Final Dynamic Special!!" retains the name of the move.

## Line names

There are no proper names recorded in the data area, such as organizations (ロームフェラ财団, カラバ, Earth Liberation War Front), Place names (ジャブロー, サンクキングダム) and ships (ブライトship) are processed by three scripts:

1. `term_candidates.py` Find candidates from the lines: katakana, and words with suffixes such as empire/finance/base/team/stream, a total of 647 words;
2. `draft_terms.py` will be handed over to `deepseek-v4-pro-0813` to divide each candidate into proper names, common words or truncated fragments, and draft Chinese and English translations at the same time. Candidates are first sorted in Japanese so that related words are arranged together; the related translations determined previously will be brought to subsequent batches as constraints;
3. `audit_terms.py` Compare the proper name of each line with all entries containing it in the entry list (including sentences such as victory or defeat conditions) one by one, in both Chinese and English.

Results for 2026-09-23:

- Drafting results: 282 proper names, 337 common words, 28 fragments, using 98,000 input and 35,000 output tokens.
- Manual review (Claude) corrected 37 items and marked another 4 as fragments:
- The first draft of "ムゲゾルバドスEmpire" missed "ムゲ" and changed it to Muge Zolbados Empire/Muge Zolbados Empire;
- Gemma was mistaken for the name of a country, but is actually a character from Z Gundam;
- A list of more than 20 aligned entries including ザンボット, ランタオ岛 (Lantau Island), etc.;
- The English names of the ブライトship and other ships were changed to "Bright's ship".
- There are 4 groups of synonyms in the entry table, which have been unified by the entry table conversation: ムゲ=Moog, ジオン=Zion, バイストンウェル=Beston Will, ミネルバ=Minerva (submitted `c62a01f`).
- The remaining 18 items in the audit are all substrings that accidentally collided with unrelated words, such as ライフ collided with ライフル, and ブライ collided with ウェイブライダー.
- Later, I discovered that the suffix rules cut ○○Captain/○○Captain into ○○ship/○○Team: 188 places in the ブライトship are actually Captain ブライト. These 8 items have been relabeled as fragments, and the rules have been revised (ship, team, army are not followed by commander, member, person, etc.). The English first draft did not use the wrong "Bright's ship"; the Chinese "Captain Bright" originally included "Bright's ship" and was not affected. There are currently 269 proper names.

The proper name status is all `draft`; manually change an entry to `approved` or `rejected` and then rerun the affected scene.

## Official translation of proper nouns (2026-09-24)

The user requested "try to find an official translator, sort out the proper nouns such as names, aircraft, weapons, etc. and polish them."

**Scope**: ~1,900 names, distributed as follows:
- `units`, `weapons`, `pilots`, `pilot_full_names`, `character_list`, `series`, `default_names` of the entry table;
- 269 line names in `content/translation/story-terms.json`.

**Method**: Divide the works into 7 groups, and use subtasks to search for sources in parallel.
- Gundam series: GUNDAM.INFO official Simplified Chinese and English website, Bandai Model Chinese website, G Century.
- Super Series: The official Simplified Chinese and English versions of Mecha 30/Y, the Traditional Chinese version of Mecha DD, the official version from Station B, and Discotek.
- 64 Original: The foreign language writing of the official card "スクランブルギャザー" in 2001 (according to srw.wiki), and the community writing.
- Each name is given origin and confidence level: Official, Passed, Polished, Reserved.
- Approximately 300 works that were classified incorrectly were forwarded to the corresponding team for re-examination.

**Choice (determined by the user)**: Commonly used Chinese names are given priority, and official English names are given priority. Details:
- The current translation is the popular name in mainland China, which is retained, even if the official Simplified Chinese is different, such as Camus Bidan, Hero Wei, Zaku, Dongfang Bubai;
- If the current translation has no source, change it to the popular name;
- If there is no popular name, the official way is used.

**Results**: 625 entries have been changed, including 483 in Chinese and 220 in English; the other 30 entries are level titles and victory and defeat conditions synchronized with the name change. The entry table has been written (`9477893`) by the session that maintains it, 14 of which are pending (see below).
- Comparison page: https://claude.ai/artifact/6uGNTsTAydmzZsnAJW4BQz
- Data: `assets/translation-runs/official-names/` (native), where each group has `final-*.json` and the combined result is `term-changes.json`.
- The entry table is written after review by the session that maintains it.

**The lines will be changed accordingly**:
- `content/translation/renames.json`: 521 name changes, applied by `run_mt.final_target` when writing lines.
- Chinese names within two characters, English names within five letters (Burn, Todd, Cham, etc.), English pronunciation (Swooord), and old names that are still the current names of other entries (Rosamia It's still a ロザミア, the floating cannon is still a ファンネル), only replace the lines containing the name in the original Japanese text; when comparing, remove newlines, spaces, "・" and "=", and write (シャーリー) separately when comparing. If the longer name is unique enough, the full text will be replaced;
- The long name of the door that is not open does not block the short name inside ("Duke Delmayo" is still replaced by "Duke Delmayo" in the sentence that only says "Duke Delmayo");
- Line names that are only name fragments (コン・バトラー lacks V, the second half of the call, and メールシュトローム lacks "combat") will not be replaced globally;
- Whole name, longest match: known longer names are protected and will not be replaced as substrings;
- English matches by whole word;
- The name placeholder does not move.
- Single-character short names (Xiu → Xiang, Zun → Wu, Fo → Feng, Fa → Hua) cannot be replaced by words:
- Use `run_mt.py names` to number each word in the line, so that the model only picks out the number that refers to this person, and the program replaces it accordingly;
- Known longer names (such as Soltifa) are covered first and do not participate in the numbering;
- A total of 472 lines were changed, and the result is `zh-v1-names`.
- A total of 4,342 lines of Chinese and 1,702 lines of English lines have been updated accordingly (the speaker's name in the entry comments also changes with the entry list). Another session checked the remaining names according to the old names, and finally only 3 places were left, which have been processed: シャーリー's other writing; two places in the first draft mistook マーズ as "mag", and manually corrected the batch `zh-v1-fixes` to "mas"; one place in English was called ロザミィ`en-v1-fixes` changed to Rosamy.
- The long-sounding shouts (Eiji~~, Lightning Sword——) will not be replaced globally.

**Only Mainland Simplified (Recheck)**: The user then requested "No Taiwanese translation, but Chinese Simplified Chinese".
- Based on only recognized mainland sources: Baidu, Mengniang, B station wiki, mecha, mainland mecha station, GUNDAM.INFO Simplified Chinese;
- Traditional Chinese official, Taiwanese version, Hong Kong version, writing methods only seen in Chinese Wiki are not counted, nor are those copied from Taiwanese translation on Baidu Encyclopedia;
- Rechecked 146 items by "Mainland Access → Official Simplified Chinese → Keep Old Translation or Transliteration".

**User Confirmation**: Click one by one on the translation confirmation page (https://claude.ai/artifact/X2N7dwfbXZb6fMUSnFjmtA).
- 640 spellings combined into 396 names. The way the same name is written in each zone, as well as the weapon, model, full name, level title, and victory or defeat conditions containing this name all follow the same choice.
- All 100 names to be decided have been decided: 43 will be changed and 57 will be retained; the rest will keep their current names.
- The homophonic names in the Taiwanese version are not used, and the transliterations are retained: Boqiong, Miuji, Dozdozi, and Jinjin.
- Call for VSBR.
- "Thunder King" is only used in the title of the work and the name of the machine. It does not match the name of the person: Magu, Rose.
- アラン retains Alan, アキラ changes to Hui, and ケンジ changes to Kenji.
- Kirara・スーン Returns to Kira Mori, which is consistent with the short name Kira.
- ビューティ The short name is kept Biyoti, and the full name is changed to Tachibana Meili.
- Entry list: Write `9638799`, and the following two items of キャラ・スーン.
- Lines: `deferred` of `renames.json` has been cleared; Ming→Hui changed 8 lines from `run_mt.py names`, and the result is in `zh-v1-names2`.
- Script that reads back page selection `finalize.py` and data in `assets/translation-runs/official-names/`.

The English translations of the original opponents are Kurtz Forneus, Rish Griswell, and Ehrlich Stasen, because the community spelling is a mispronunciation.

**English comparison Akurasu (2026-09-24)**: The user asked to refer to Akurasu's SRW64 page and gave it to Claude for evaluation.
- Crawled 58 pages and obtained 809 sets of Japanese and English comparisons. Compared to our English, about 600 sets are identical.
- In addition, compare the writing in the official English version of Aircraft War 30/T/V/X/DD step by step. For the comparison page, see https://claude.ai/artifact/6uHNPqtvUM5M6gvHUy2PVB.
- Mental Command: Akurasu's SRW64 page is a mix of early player names (Sure-Hit, Guts, Awaken) and another set of old names (Strike, Alert, Luck, Tire). We use the official name of T/30, reserved.
- Personal name and machine name: Akurasu's different writing methods are mostly Roman characters with long sounds, or we have changed them according to the official writing method, so we will keep it.
- Level title: Akurasu is a literal translation, keep ours.
- Only 4 items have been changed: アフロダイA Aphrodite A, ダイアナンA Diana A, ダイアナンミサイル Diana Missile, high-performance レーダー High-Fidelity Radar (official T/X).
- Data and scripts are in `assets/translation-runs/official-names/akurasu/`.

## Reference control polish: Serenes Forest English LP (2026-09-26)

The user found an English human translation: Serenes Forest Forum Balcerzak's Let's Play (https://forums.serenesforest.net/topic/104832-super-robot-wars-64/, 2024-07 to 2026-04, 56 episodes, one episode of the Manami route, the full text of the plot is written in the folded block according to "Speaker: Lines"). The user decided to **only refer to it and not copy it**: capture it for comparison, and check the Chinese version for problems found in English.

- **Fetch**: The site blocks curl, use the built-in browser to expand the folded block and save it as `assets/translation-runs/reference-en/raw/chNN.txt` (without entering git), and filter out battle reports and data tables. Episodes 1–5 are currently saved.
- **Alignment**: `tools/translation/align_reference.py` According to the roadmap, try to align and find the scene one by one (the writing of the title is very different, so choose based on the number of alignment hits). At the line level, use the speaker + the word overlap between the two English languages to do Needleman-Wunsch. Automatically learn the speaker alias (Brai the Great=Emperor Burai), write `reference-en/aligned/scene-NNNN.jsonl`. Episodes 1–5 match 82–91% of the reference lines (366 lines).
- **Comparison**: `tools/translation/polish_reference.py` Show ja/en/zh/ref to `deepseek-v4-pro-0813`, only change when the meaning, missing translation, reference, and tone are obviously inconsistent. Change the batch written with stage=polish (`en-<tag>`, `zh-<tag>`), which can be stacked in the runs of write_dialogue Behind; `--report` shows the table before and after the change.
- **Pilot results (tag `ref-pilot`, scene 1/4/5/6/7)**: Out of 366 rows, the model only thinks that 9 rows have problems. After mechanical inspection, the English is changed to 1 and the Chinese is changed to 4; manually check these 5 rows: 17916 Filling in the omitted predicates is a real improvement; 17831 (paw no scale を fry じ て drink む = "learn from others") model has a problem with the Chinese version, but the literal translation "nail scale decoction water" cannot be used, and **missing the English literal translation** (pointed out by the user); 17958 changing "she" to "he" is an improvement; 17497 The English modification did not fall into the text.
- Claude himself read the 130 lines of Chapters 1 and 4 line by line: Our translation did not make mistakes in meaning, but the references were wrong in five or six places ("did you bring the Doll", "more than half the engineering staff", Jia'er "grandpa was called away", Professor Gong "people who need protection", etc.). I also found two problems that were not revealed in the reference, both in the handwritten scene-0001 (returned to the entry table conversation): 17497 "Western Federation/Western Federation" (original text "Old Federation") is missing in both Chinese and English, 17461 "后は頼む" is missing in Chinese.
- Conclusion: **Machine translation has reached the same level as this reference in terms of meaning. The yield of line-by-line comparison of meaning is very low**, and the recall of DeepSeek comparison is also unreliable; the difference is mainly in the tone of the characters (in the reference, Manami's aristocratic accent and Lawrence's butler accent are more distinct, while ours is more neutral).
- Idiom spot check: Use more than 100 common idioms to scan the script library, and hit 17 (except common words such as oil break and breath root), and check all Chinese and English translations one by one; 17831 This is an isolated case, and the reason is probably that the idiom is cut in the middle by turning the page ("paw no dirt でも｜せんじて Drink ませて"). 17831 has been written into manual.json of `en-v1-fixes`/`zh-v1-fixes` and regenerated the lines file.

## 7. Translation specifications (specified in the prompts)

- Be faithful, natural, colloquial, and consistent with the character's identity and tone; do not add or delete information, or add comments.
- The number of pages is consistent with the original text, and there are no line breaks within the page; quotation marks follow the first and last pages of the original text.
- Placeholders such as [Protagonist's name] are retained as they are, and the number and order remain unchanged; most of the さん and くん after the name are omitted.
- Punctuation:
- "" is changed to "", "" is changed to '';
- () inner monologue retains full angle brackets;
- Use... for ellipses, and -- for dashes;
- ! ? Use full-width; use half-width for numbers; use spacers · for foreign names.
- Titles and military ranks: Second Lieutenant/Lieutenant/Captain = Second Lieutenant/Lieutenant/Captain, Major/Lieutenant Colonel/Colonel = Major/Lieutenant Colonel/Colonel, Captain = Captain, お嬢様 = Miss, Your Excellency, Your Majesty = Your Excellency, Master = Master.
- Retain the level of mouth habits, stuttering, pronunciation, and honorifics; maintain momentum when shouting move names.
- Vocabulary list: "Must-use" items must be used as usual; proper names outside the vocabulary list, works such as Gundam, etc., use the commonly translated names in mainland China. There are no transliterations of the commonly translated names in mainland China, and the new translation names should be written in `flag`.
- Common to both languages: add the subject or pronoun when necessary, based on the gender of the speaker, conversation partner, context and role card; when the reference cannot be determined, use a name or a neutral term and mark "unknown reference". The game connects the pages of a line into one paragraph for display (see [Dialogue Layout](dialogue-typesetting.md)), so punctuation is required when the end of the page is at the boundary of a sentence or clause, but not when the sentence continues across pages (prompt words starting from v5; the rule of v4 is "the punctuation at the end of the page follows the original text").

English:

- Natural spoken language, abbreviated forms can be used; names are in Western order in the entry list.
- Remove -san／-kun／-chan; the titles used as salutations are translated into English: お嬢様 my lady, Master, Your Excellency, Captain.
- Ranks: Ensign, Lieutenant, Captain, Major, Lieutenant Colonel, Colonel.
- Use only ASCII punctuation plus curly quotes “ ” ‘ ’:... Writing...,! ? Writing ?!, inner monologue with ( ).
- Move names are written as Title Case according to the entry list; moans and screams are written in natural English, such as Ngh!, Gah!.

## 8. Matters that have been processed by default

Processed by default (can be changed, rerun the affected parts after changing):

- **Model**: Use `deepseek-v4.1-flash` for first drafts, `deepseek-v4-pro-0813` for revisions and final reprints.
- **Pronoun**: Add it when needed, mark it if the reference is unclear, follow the method of the special chapter of "Mech Z".
- **English writing**: Use curly quotation marks for dialogue; follow English conventions for titles (my lady, Master, Captain); use normal English punctuation for periods at the end of the page.
- **Karaoke Lyrics and Song Titles**: Not translated this round.

- **Chinese end of page punctuation** (Defined on 2026-09-24): After the game is changed to a whole series, the end of the page is determined according to the sentence structure and will no longer follow Japanese text. See Section 5 "End of page punctuation".
- **Opening Prologue and Chapter Title Cards** (Defined on 2026-09-24): Use native text to rearrange according to reading language, and no longer display the original image; the ending page will be treated similarly.

The original names of the lines to be decided have been finalized in the official translation check on 2026-09-24 (the user clicks on the 100 names to be determined one by one), and the lines are written according to `renames.json`; the `status` field of `story-terms.json` is not backfilled, which does not mean that it has not been finalized.

## Known limitations

- Plot context is given in script static order, route segments and conditional blocks are not evaluated. The same scene may list branch text for several routes at the same time.
- The battle line selection table has been reversed (2026-09-27), but the semantics of plot flags 45–49 and the meaning of the belligerent record type `0x14` have not been studied in detail. See [battle-quotes.md](../data/battle-quotes.md) "Not yet studied in detail".
- The transcription of the opening relies on manual picture reading; the correspondence between the prologue route and the protagonist, except route 2, is inferred based on the content.
- The text in the image has not been counted except for the opening, chapter title card, ending page and title menu.
- Mechanical inspection can only ensure correct structure and obvious formatting problems; the quality of the translation depends on manual review. AI review changes about 4.5%, which does not mean that the remaining 95% has been confirmed.

### Protagonist’s body and weapons (verified on 2026-09-27)

English machine names will always use the official spelling of the Japanese Wiki's "Foreign Language Notation" (Earthgain, Virose, Svanheld, Sigroon, Razgreez, Soldifar, Ashcleef, Sweemurg, Elbulls), instead of the commonly used Vairose/Svanhild/Razgriz/Simurgh/Elbrus in the English circle; Chinese transliterations are based on katakana, and mythological translations are not used. The moves of the Wujiba Fist style are still using Chinese characters in Chinese and Roman characters in English. This change: シグルーン Sigrun → Sigroon; アッシャークルー Ashekru → Angel Light Wheel (chest continuous light wheel, source unknown); スプラッシュブレイカー Splash Destroyer → Scatter Breaker (Splash It is the name of the automatic turret); ダブルライトニングソード Double Lightning Sword → Double Lightning Sword (dual wield); ノーブルフェニックス Noble Phoenix → Phoenix Assault. For the verification page and source, please see the "Protagonist Machine and Weapon Verification" produced by the session.

## Military rank, title and writing method (2026-09-28 user decision)

- **Military ranks are written according to the system of the target language and do not copy Japanese Kanji**. The Chinese military ranks are as follows: General→General, Colonel→Colonel, Lieutenant Colonel→Lieutenant Colonel, Major→Major, Captain→Captain, Lieutenant/Second Lieutenant unchanged, Brigadier General unchanged; English uniformly uses the Army system: Captain, Major, Lieutenant Colonel, Colonel, Brigadier General, Lieutenant Lieutenant, Second Lieutenant (the original naval Ensign has been changed). Captain (captain) is also called Captain in English. The same word as military rank is an English convention and will not be changed. The title "Dark General" is not a military rank, as usual; the common name "General" (boss) is translated according to meaning. The entry "Captain ゴーマン" was changed to "Captain Gorman". OZ's unique special lieutenants/special lieutenants/special soldiers are still the same (Special Lieutenant, etc.).
- **Jia'er treats Sayaka according to the occasion**: address her directly as "Sayaka" in person (daily, in battle); use "Ms. Sayaka" when referring to her to others. English is always Sayaka.
- **Saint** English unity Saint (Saint Julia, the Saint, the ‘Saint of Cusco’, organization name Saints’ Corps).
- **Cosmic Century Year** Use half-width: Chinese "A.C. 195", English "A.C. 195". When the month is included, the Chinese is "January, A.C. 191" (without commas), and the English is "January, A.C. 191".
- **Episode marks for chapter titles** (2026-09-27): Japanese (front) (middle) (back), Chinese (upper) (middle) (lower), English (Part 1)/(Part 2)/(Part 3).
- **Select limb** (2026-09-27): There is no "" in the original text, and there are no quotation marks in the translation; there is no period at the end of the option,! ? … Retain as original text.