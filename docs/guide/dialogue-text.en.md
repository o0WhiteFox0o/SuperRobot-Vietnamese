> **Language / Ngôn ngữ:** [English](dialogue-text.en.md) · [Tiếng Việt](dialogue-text.vi.md) · [中文](dialogue-text.md)

# Line text file: format, storage location and modification method

Date: 2026-09-23. Plot dialogue, optional limbs and combat lines are not written into the language directory `content/locales/<locale>.json`. Each language has a separate set of plain text files that players can modify directly. The name, interface label and system prompts still go to [term list](../native/localization-terms.md).

## Where to put it

| Location | Purpose |
| --- | --- |
| `content/dialogue/<locale>/` (warehouse); `Contents/Resources/dialogue/<locale>/` in the application package | The translation that comes with the program. The plot is divided into files according to scenes; the battle lines are divided into files according to characters (`battle/speaker-NNN.txt`). The `# 触发：` comment above each line indicates in what situation, which weapon is used, and which opponent the sentence appears (see [Battle Line Selection Table](../data/battle-quotes.md)); the entire set is replaced when updating the program |
| `dialogue/<locale>/` in the user directory (macOS application: `~/Library/Application Support/SRW64Recomp/dialogue/<locale>/`; development trial `scripts/Play SRW64 Native.command`: `build/recomp/profile-play/dialogue/<locale>/`; debugging session: `dialogue/` in the respective running directory) | Player's own modifications. **Coverage item by item** Comes with translation, file name and directory structure are arbitrary; the update program will not touch this place |

`<locale>` is `zh-Hans`, `en` or `ja` (the `ja` directory is used to change the display of the original Japanese text, optional). The program reads all `*.txt` of a certain language: first read the attached ones, and then read the ones in the user directory; for the same line, the user directory shall prevail.

If you want to change any sentence, just copy the sentence in the attached file (or the entire scene file) to the user directory and then change it. There is no need to copy the unchanged entries, otherwise if the accompanying translation is updated in the future, your old copy will still cover it.

## Format

UTF-8 plain text, as many as you want in one file. Example:

```text
# 第一话「出撃！スイームルグ」
@17412 ローレンス
> お嬢様、お茶のご用意ができました。本日はロシアンティーでございます。
小姐，茶已经准备好了。今天是俄罗斯红茶。
---
> どちらにお持ちしましょう？
要送到哪里呢？

@17413 {HeroNick}
> ……ローレンス、お茶のことはいいわ。
……劳伦斯，茶的事就算了。

@18020 选择肢
> * 協力する
> * 断る
* 合作
* 拒绝
```

| Writing | Meaning |
| --- | --- |
| `@17412 ローレンス` | The beginning of a line. The number is the record number of text table 0; followed by remarks (usually written as the speaker), the program does not read |
| `> …` | Original Japanese text, for comparison only. The program will compare with the original text of the ROM. If they are not consistent, it means that the record number is written incorrectly and this will not take effect. You can delete it without writing |
| Other lines | Translation. A page is usually written as one line, and the program automatically folds the lines according to the width of the dialog box. Manual line wrapping will force a new line in the game, only use it when really needed |
| `---` | The page turning point of the original version (the next page that appears after pressing A once in the original version). The number must be the same as the original text, and the game relies on it to align with the advancement of the original text. In the game, if a line of dialogue is connected in its entirety, the page will be re-paged according to the size of the dialogue box, and the page will not necessarily be turned here; the word-by-word display will stop here for about 0.3 seconds, and the page will be disconnected here first during paging |
| `* …` | Select an option for limbs, one per line, the number must be the same as the original text |
| `# …` | Comments |
| Blank line | meaningless, you can add it as you like |

The dynamic name is written as a placeholder and replaced with the name given by the player in the game:

| placeholder | content | placeholder | content |
| --- | --- | --- | --- |
| `{HeroNick}` | Protagonist's nickname | `{PartnerNick}` | Partner's nickname |
| `{HeroName}` | Protagonist's name | `{PartnerName}` | Partner's name |
| `{HeroSurname}` | Protagonist's last name | `{PartnerSurname}` | Partner's last name |
| `{HeroFull}` | Protagonist's full name | `{PartnerFull}` | Partner's full name |
| `{HeroMech}` | Unit name (the placeholder name follows the old name, see [Fixed unit name](../native/fixed-unit-name.md)) | `{G:0104}` | Other special glyphs (retained as they are) |

The placeholders on one page should be as many and of the same type as those used on the original page, and the order can be adjusted according to the word order of the translation.

To have a line of translation begin with `>`, `*`, `#`, `@`, `\` or for the entire line to be `---`, prepend it with `\` (for example, `\*`). Half-width `<` cannot appear in the translation, please use full-width `＜`.

## Validation, reloading and errors

- Read on startup. Press **F5** in the game (or use the menu "Reload Lines") to re-read all line files: the current line will be displayed from the beginning with new text, and the review will also be replaced with new text.
- The entire entry with errors will not take effect and will fall back to the next level: user directory → attached translation → original Japanese text. Other entries will remain as normal. After each reading, the number of entries and errors will be prompted at the top of the window, and the details will be written to `dialogue-report.txt` (file name, line number, record number, reason) in the user directory.
- Common errors: The page number (`---`) is inconsistent with the original text; the number of options is inconsistent; the placeholder is misspelled or missing; the original text line (`>`) does not match the record number; there is a half-width `<` in the translation.
- How to typesetting in the game (how to type the whole line, how many lines per page, English font size, and page turning position), please see [Dialogue Typesetting](../design/dialogue-typesetting.md).
- The battle lines are only replaced and displayed, and the original advancement rhythm remains unchanged. If it doesn't fit on one page, the font size will be automatically reduced and there will be no page breaks, so keep it as short as possible.

## Attachment: To the tool author

- Read implementation: `src/srw64_native/dialogue_text.py` (Python, for generation and checking) and `src/native/localization/dialogue_text.hpp` (in-game). The rules of the two are consistent and are jointly constrained by `tests/test_dialogue_text.py` and `tests/native_content.cpp`; the expansion results of the two attached files for the same batch are consistent one by one.
- A line is expanded into the language directory format: `<BR>` between lines, `<STOP>` between pages, placeholders become `<G:0124>`–`<G:012C>`, and `<END>` at the end. When a name occupies multiple spaces in the original text (the same character code is repeated), only write one placeholder; in the game, it is displayed by one name.
- Paging: `src/srw64_native/dialogue_paging.py` is the Python reference for game paging rules (continuous rows, font size and line spacing, page turning position). It shares the use case of `tests/data/dialogue-paging-cases.json` with the game, and `tests/test_dialogue_paging.py` is used to check that the page boundaries are the same one by one.
- Text page: `@intro:<资源号>` is the plot text drawn in the picture, the opening prologue is in `intro.txt` (5506–5535), and the ending is in `ending.txt` (5570–5576). No ROM comparison is performed; the game is drawn natively in the reading language, and Japanese uses the original line in the entry (`>`). `---` in the text page means a blank line, not page turning. See [Title Image and Story Image](../native/native-title-and-story-images.md).