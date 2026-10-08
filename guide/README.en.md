> **Language / Ngôn ngữ:** [English](README.en.md) · [Tiếng Việt](README.vi.md) · [中文](README.md)

# Walkthrough and Hidden Elements Guide

`srw64-flow-guide.html` is an offline single-file walkthrough guide for players. It includes multilingual support: switch language on the top right of the tab bar; the default language uses your previous selection or browser language, and can also be specified via URL `?lang=en|zh-Hans|ja|vi`.

Content includes: Progression flowcharts, hidden secrets, spirit commands, pilot skills, unit stats, enhancement parts, romance bonuses, upgrades and inheritance,追加 weapons, combination attacks, and Game Boy Link Battler data. The page embeds all styles and scripts, requires no internet connection, and can be opened directly in any web browser.

## Basis

All content comes from parsing the stage scripts and disassembled code of the Japanese ROM; community guides like Akurasu Wiki are only used for comparison.
Three badges indicate comparison results: "Differs from Akurasu", "Missing from Akurasu", "Unverified on real hardware" (notated as `{≠}`, `{+}`, `{?}` in the data). Technical references:

- [Hidden elements, persuasion, and route splits](../docs/gameplay/hidden-elements.md)
- [Battle formulas](../docs/gameplay/battle-formulas.md), [Upgrade inheritance](../docs/gameplay/upgrade-inheritance.md), [Upgrade limits](../docs/gameplay/upgrade-limits.md), [Link Battler](../docs/gameplay/link-battler.md)
- [Stage script commands](../docs/script/stage-script-exploration.md)

## Data

Located under `data/<language>/` in three files with identical structure and IDs:

- `progression.json`: Stage cards in the progression flowchart
- `hidden-elements.json`: Hidden elements, route splits, and persuasion rules
- `reference.json`: Reference data tabs

Names of characters, units, weapons, parts, and spirits are sourced from the localization directory (`content/locales/`).

Rebuild the page after modifying data:

```bash
python3 tools/content/build_guide.py
```

