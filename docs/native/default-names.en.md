> **Language / Ngôn ngữ:** [English](default-names.en.md) · [Tiếng Việt](default-names.vi.md) · [中文](default-names.md)

# Trilingual display of default name

2026-09-27. The user determines that the names of the protagonist, partner and troops are **not allowed to be changed by the player**. The default names are displayed in Chinese, English or Japanese according to the reading language. For the half of the unit name (skip the naming choice in Chapter 33, `3D5E` is the bottom line), see [Fixed unit name](fixed-unit-name.md).

## Practice

**Storage unchanged. ** The name area (from `8010F5F8`, see [Protagonist Selection and Confirmation Page](native-name-entry.md)) and unit name `8010F698` only store the original glyph, which is the Japanese version of the ROM default name. The archive format remains unchanged, and the original archive written by this ported version can also be read. The ROM font library only has about 2,000 Japanese characters, and Chinese names such as "Brad" cannot be stored in it. After name changes are not allowed, the font library does not need to be expanded.

**Replace when shown. **[`default_names.hpp`](../../src/native/game_adapter/default_names.hpp)'s `DefaultNames` determines whether a field is still the default name:

- If the Japanese content is equal to a certain default name (leading and trailing spaces are not counted), its translated name in the reading language will be displayed;
- Other content is displayed as is, the same in all three languages. This includes names entered by players in the old version, as well as archives whose names have been changed in the original game;
- First name, last name, nickname, and unit name are judged separately and only fields of the same type are compared;
- The full name is split into two segments according to the original midpoint "・" (glyph `0xE7`), judged separately, and then connected using the separator of the language: Chinese "·", English space, Japanese "・". Therefore, the old save file with only the last name changed is displayed as "Brad·ヒカリ";
- Japanese text will always be returned as it is, which is word-for-word identical to the original text drawn on the game screen, and the dialogue adapter will use it for comparison.

**Data only exists in one place. ** The translated names of the eight people are taken directly from the `default_names` partition of [entry table](localization-terms.md) without creating another table: ROM records 487–494 are the abbreviations and the default nicknames (`801C3744` are intercepted from the names: generally 5 cells, アークライト 3 cells, getアーク); 495–502 is the full name, with the first and last names separated from the full name by the language's delimiter. `add_people()` is registered from the language directory in `dialogue::configure`. It will take effect after changing the entry table and re-running `apply_terms`. When the full name of a certain language cannot be split into two parts, the first and last names of this language are displayed in Japanese, and an `default_names_unsplit` is recorded in the event log. The unit name マーチウィンド is registered by `unit_name.cpp`, and the interface entry is `unit_default_name`.

The shared instance is `names::default_names()` ([`native_name_entry.hpp`](../../src/host/native_name_entry.hpp)): written at startup, read-only for both the game thread and the interface thread thereafter.

## Access point

| Display location | Naming method |
| --- | --- |
| Placeholders such as `{HeroName}` in the lines (`<G:0124>`–`<G:012C>`) | `expand(ram, text, locale)` of `native_dialogue.cpp` is read and displayed by language through `shown_name` |
| Dialogue speaker, review, battle lines | `speaker_name`. When looking back, save one copy in each language, and each copy uses the default name of its own language |
| Driver name on the native page: pre-war confirmation, ability, のりかえ, strengthened パーツ, transformation | `ui_text` → `record_text`: Original word extraction function `8008CF14` replaces records 4407–4414, 4768–4775 with name fields, the host does the same, and then displays them by language |
| Text overlay of the original interface (tactical map, battle screen labels) | `label_text`, same as above |
| Archive page and title screen load list | `save_page.cpp`'s `slot_json`: The archive header stores the protagonist's nickname |
| Casting cards and confirmation pages | `frontend.cpp` of `sync()` Change reading language before handing over page |

**Switch language** (F7 or Settings) takes effect immediately: dialog boxes and playbacks are rearranged according to the new language, each native page is rebuilt according to the original `relocalize`, and the archive list is rebuilt along with the page.

## Casting process

- **New version** (default): Select the protagonist → Confirm → Start the story, click "Return to Character Selection" on the confirmation page to return to the casting page. When selecting a route, the host writes the default names of the two people in the same way as the original name submission: put the first name, last name, and nickname into the editing buffer `801C71E0`, and then adjusts the original verification function `801C474C` for the protagonist and partner each, and uses it to write out the four fields of first name, last name, nickname, and full name. The verification will not reject the default name; if it is rejected, the original name page will be returned and the log will record `defaults-rejected`.
- **Original** (Set "Protagonist Selection" to select the original version): After "はい" on the original casting page, also write the default name and `801C70F4 = 2`. After the fade-out, go directly to the route prologue without entering the original character selection page. Logging `original-started`.
- `SRW64_NATIVE_NAME_ENTRY=0`: Keep all pages of the original version during the entire run, including name changes, and are only used to reproduce the old baseline.

The old name editing page, input method grouping, character verification, `E000..` dummy text records, and 23 interface entries have been deleted.

## Archive compatible

- **Old Archives**: The default name is automatically displayed in the reading language; previously changed names are displayed as they are.
- **New Archive**: The content is consistent with the original version. Both the original game and the old version can be read.
- **Price**: If the hand-typed name in the old version happens to be exactly the same as the default name, it will also be regarded as the default name and will be switched with the language.

## Translation

From the entry list (checked the official name on 2026-09-24, Chinese is written in mainland China). These eight people are 64 original characters. There is no common Chinese name or official Simplified Chinese, and the current translation is retained; those in English who have the 2001 official card spelling (スクランブルギャザー) use the official spelling, and the rest follow the current translation.

| Route | Characters | Japanese (first name, last name, nickname) | Chinese | English |
| --- | --- | --- | --- | --- |
| Super male | Protagonist | ブラッド・スカイウィンド／ブラッド | Brad Skywind／Brad | Brad Skywind／Brad (official) |
| | Partner | カーツ・フォルネウス／カーツ | Katz Forneus／Katz | Kurtz Forneus／Kurtz |
| Super girl | Protagonist | Manami Hamill／Manami (official) | Manami Hamill／Manami (official) |
| | Partner | Aisha Ridgemond／Aisha | Aisha Ridgemond／Aisha |
| Real male | Protagonist | Arklight Blue／Ark (official) | Arklight Blue／Ark (official) |
| | Partner | Ehrlich Stasen／Ehrlich | Ehrlich Stasen／Ehrlich |
| Real girl | Protagonist | Selain Meneth／Selain (official) |
| | Partner | Rish Griswell／Rish | Rish Griswell／Rish |
| Troop name | — | マーチウィンド | March Wind | March Wind |

## Verify

- **Component Testing:**
- `tests/native_content.cpp`: Matching of `DefaultNames` and `add_people`, spaces, full name split, Japanese original, non-default name original, missing translation fallback.
- `tests/native_name_entry.cpp` (`make recomp-name-entry-test`): casting writing and nickname truncation, template reloading when the route changes, return to the original page when verification is rejected, confirmation page return and start, original "はい" starts directly.
- **Real machine script:**
- `tools/recomp/verify/verify_shared_ui.py`: Confirm page with trilingual name, settings, zoom, return to casting, start story.
- `tools/recomp/debug/check_name_entry_ui_switch.py`: In the original version "はい", enter the plot directly after writing the default name.
- `tools/recomp/debug/check_localization.py`: Default name on intervening pages changes with language.
- **Not yet running on real machine. ** The above three scripts have not been run after being rewritten on 2026-09-27.