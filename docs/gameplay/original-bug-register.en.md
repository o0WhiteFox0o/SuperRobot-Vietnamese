> **Language / Ngôn ngữ:** [English](original-bug-register.en.md) · [Tiếng Việt](original-bug-register.vi.md) · [中文](original-bug-register.md)

# SRW64 original bug and confusing behavior registration

Investigation date: 2026-09-16. Scope: The "スーパーロボット大戦64" report published online is used for comparison and reproduction of the Japanese Rev 0 original version of this project. **This is a report list, not a list of bugs that have been verified or fixed by this project, nor does it claim to be complete. ** No game replays were run, code reasons confirmed, or game rules changed this round.

Sources include direct player reports, personal guides, and community wikis. Multi-site records do not mean independent verification; reprint relationships, ROM versions, and use of real machines/emulators are often unclear. The "should have been" in the strategy cannot be directly used as a correction formula, especially the rules of other mechanized combat works cannot be applied. The sources were retrieved on the above date; the video was only verified with description and chapter information, not frame by frame.

## 1. How does this community feedback fit into the roadmap?

Reddit replies relayed by users put combat animation skipping first, followed by driver skill fixes, and suggested adding previews and confirmations before Wing→Endless Waltz switches. The description of his weapon inheritance is of a recall nature, and no specific machine body, weapon, archive or permanent link to the post is given.

| Feedback | Processing |
| --- | --- |
| Combat animation can be skipped | Corresponds to roadmap B01; it is a functional requirement. The current dialogue skipping demonstration cannot be regarded as combat animation skipping has been completed. |
| Driver Skill Bug | Divided into BUG01-03, see BUG02 for the relevant differences in special defense; after reappearing item by item, optional rule corrections will be entered, and the balance of the original version will not be silently changed. |
| EW Preview and Confirmation | Marked as QOL01, access the M2 modification budget/maintenance process; first verify the original replacement conditions and weapon mapping. |
| Certain weapons are not inherited correctly | Marked as LEAD01. It cannot yet be determined that EW is specific, nor can "the disappearance of a weapon" automatically equate to "the loss of a weapon modification that still exists". |

## 2. Bug candidate list

The **local status of the items in the following table was originally to be reproduced**; later, the causes of BUG01–04 (2026-09-17, optional rules) and BUG05 (2026-09-18, [Basic Repair](base-fixes.md)) effective by default have been confirmed, and the rest are still to be reproduced. "There are specific steps", "multiple records" and "divergent sources" only indicate the nature of external evidence. Modifications that change the trade-off between strengths and weaknesses are made into optional rules; like BUG05, where "the game is inconsistent with its own data and the repair does not change any original settings", basic repairs will be carried out according to the classification principles of the roadmap. Other items must first be proven to be anomalies rather than plot/resource rules.

| ID | Phenomenon reported online | Conditions, disputes and sources | Preliminary classification |
| --- | --- | --- | --- |
| BUG01 | The super power (ESP) level does not affect some corrections, and the attack power bonus is missing | Japanese data states that both hit and avoidance are fixed at +64; Akurasu Bugs claims that only avoidance +64 is available. You cannot directly choose one as the actual measurement conclusion. [S1][S2][S3] | Rule modification; check hit, avoidance, and attack power separately |
| BUG02 | Aura Warrior's evasion is fixed at +32, and Hyper Aura Slash's attack power correction is missing | There are also reports that Aura Barrier's correction is higher than in the strategy book. The skill table still lists barrier modifiers as changing with level, so it's not "all effects fixed". [S2][S4][S5] | Rule modification; Barrier control alone |
| BUG03 | Potential hit and avoidance corrections are too high | Akurasu weighs twice as much, and L9/HP ≤ 10% is +100; the Japanese table lists +90 at the corresponding position. Maximum values, thresholds, and expected tables all need to be verified. [S1][S2] | Rule correction; cannot directly divide everything by two |
| BUG04 | Limit reaction does not actually limit hit/avoidance | The original red text prompt may be inconsistent with the actual settlement; the limit modification still participates in the W series EW replacement threshold, and this attribute cannot be completely deleted. [S1][S6] | Rule modification; UI and conditional dependencies are handled separately |
| BUG05 | The number of clones when the five-fly enemy is hostile is affected by the number of previous kills | The data points to the Independence Army's "Decisive Space Domain Part 1" and OZ "Life and Death's Future"; it is not a fixed "21 times". **2026-09-18 Recurred and confirmed the cause**, see update below. [S5][S6] | Corresponds to FIX01; has been taken as a basic fix that takes effect by default |
| BUG06 | After the real-life protagonist leaves OZ, Wan Zhang/Titan 3 appears in the dialogue but cannot play | After the strategy has positioned "そのkenに心素して"; in the later stage, "Haruka no Gamble" who went to the Miya universe may be added, but the remaining earth circle will continue to be absent. [S6] | Corresponds to FIX02; team and plot consistency |
| BUG07 | The transformation was reset after Spiegel left the team and rejoined | The unit entry is located in the Guyana Highlands related to leaving/rejoining the team; it is unknown whether all routes and all transformation fields are affected. [S7] | Corresponds to FIX03; first distinguish between temporary participation in the war and permanent participation |
| BUG08 | Reznar → The flamethrower modification is lost when strengthening Reznar | Akurasu clearly listed it as a "possible omission/bug"; some players discussed the non-inheritance of the same weapon. It has not been proven whether it is a mismapping or the weapon replacement rules. [S8][S9] | Corresponds to FIX04; Doubts about weapon inheritance |
| BUG09 | The enhanced parts menu exceeds the slot, which may exceed the slot equipment and destroy the running status | Wiki records that the cursor on A+ is out of bounds; 5ch 573, 574, and 576 floors (2022-06) have personal attempts, abnormal values/driver changes/black screen crash reports. The actual writing range and archiving impact have not been confirmed. [S5][S10] | Added FIX05; input/boundary check, priority for recurrence |

"+64", "+32", etc. follow the data notation. This round has not confirmed whether they are internal ability values, final hit rate percentages or intermediate correction items; they cannot be directly multiplied by percentages in implementation. The critical hit bonus of base power must also be measured independently, and it cannot be inferred from the hit/avoidance problem that the critical hit also has a bug.

**2026-09-17 Update (BUG01–04)**: The reason has been found in the code and an optional rule correction has been made that is turned off by default. See [Optional Rule Correction](rule-fixes.md). Key points: The correction functions of superpowers and holy warriors are empty functions. What the caller gets is the skill flag itself (64, 32), which is directly added or subtracted on the hit rate percentage, regardless of level, and it also takes effect at level 0; superpowers are available on both offense and defense, while holy warriors only have the defensive side; neither has an attack power item in the damage formula. Limits are only used for status page warning colors, modifications and EW conditions, and hit formulas are not read. The maximum base power table is 90, the HP level is one level earlier than the two data, and the hit, avoidance, and critical hits take the same value; the "2 times" statement does not match the maximum value of the code, and the halving correction is only provided as a weak basis option. The real machine probe has checked the numerical changes of each correction according to the formula.

**2026-09-18 Update (BUG05)**: It has been reproduced and the reason has been confirmed in the code. **As a basic fix that takes effect by default and has no switch**, see [Basic Fix](base-fixes.md). Key Points: The enemy unit's driver record `+0x14` is the number of clones, and the same field of our unit is the number of kills; the five W-series pilots also have persistent kill backup tables `801614E0`, `800A5054`. When creating a new driver record, the backup is written back to `+0x14`, which is used to retain the number of kills after leaving the team and rejoining, but it does not check the camp. Wu Fei's two enemy deployment records do not have fake positions, so the number of fake positions he has when he is hostile is the cumulative number of kills on our side (the upper limit is 999, not a fixed 21). Consuming the dummy will not affect the backup, and the number of kills will be restored as usual when rejoining.

## 3. Reproduction design (this project is planned but not yet implemented)

| Object | Minimal experimentation and evidence to be retained |
| --- | --- |
| BUG01 Super Power | Change skill levels one by one under the same combat conditions, separate driver growth, terrain, strength, spirit, love/friendship correction; record hit display value, actual settlement input, avoidance and non-critical damage. Must cover skills/no skills and both enemy and friendly to avoid 0%/100% clamping to cover up the difference. |
| BUG02 Holy Warrior | Independently test avoidance, designated weapon attack power, and barrier threshold; the comparison of skills L1/L5/L9 cannot rely on only one hit or one damage. Keep the basic weapon values ​​and settlement corrections, and check the applicable weapons and resource conditions of the barrier. |
| BUG03 Base Power | Two-dimensional comparison between skill level and HP ratio, taking a value before and after the boundaries of 10%, 20%, etc.; excluding rounding differences, recording hits, avoidance, and critical hits respectively, without pre-programming +90 or +100. |
| BUG04 Limit | Select counterexamples whose total ability is lower/higher than the limit and change the limit individually; compare the red letter, battle preview, actual settlement and EW full transformation qualifications. |
| BUG05 Five Flying | ~~Establish checkpoints before leaving the team with different numbers of kills, and count the actual consumption of the fake body after hostile events on the same route~~; Mini level `wufei-dummy.json` has been used to complete "Kill down → Leave team → Enemy appears" in one level and check the fields, see update below. The comparison of different kill numbers on the original route and the results after adding them are still not covered. |
| BUG06 Wanzhang | Male and female real type × OZ are reported as positive examples, super type × OZ, real type × independent army are candidate counterexamples; keep the list before and after joining the event, the list of available attacks, route flags and later disagreement status. |
| BUG07 Spiegel | Before leaving the team, set the number of distinguishable body/weapon modification stages and record the component instances; check after adding them one after another, check the new and old unit instances and initialization calls, and do not need to make a backup to cover all before adding. |
| BUG08 Weapon inheritance | Set different modification levels on different weapons of the old machine, and compare the weapon ID, name, modification value and basic power one by one through the real machine replacement script; at least cover the OZ/Independent Army replacement path listed in the guide. |
| BUG09 Parts out of bounds | Use quarantine archives to test A/ on the same frame and adjacent frame input on the preparation page where the number of parts is greater than the number of slots. Observe the cursor and writing boundary first, then check the parts inventory and body/pilot fields; do not use crash status as the only judgment, and do not run commonly used archives. |

Common requirements: lock ROM identity, record host build, input, checkpoints and original reference environment; distinguish original defects from defects introduced by recomp. Modification of a single variable during diagnosis must be marked as a controlled experiment and cannot be disguised as a state obtained by a normal process. Original random timing is preserved; RNG differences due to rendering time are reported separately.

## 4. Wing → EW: First, separate "change" and "inherit"

### LEAD01: It is still unknown which weapon is at fault.

The Reddit spinoff did not give a name for the weapon. The current information is sufficient to build a checklist, but not enough to claim to have found the specific cause of the "EW Weapon Inheritance Bug".

| Situation | Existing data and processing |
| --- | --- |
| W Early-stage machine → TV Late-stage machine | Akurasu records do not inherit the old transformation, and late-stage machine comes with three stages. This is a candidate for machine replacement rules and is not equivalent to the loss of later machine → EW. [S8] |
| TV later machine → EW | The Japanese guide records the trigger when all items of the machine are changed to full. Weapon changes coexist with partial inheritance; they should be verified item by item and not just compare total combat power. [S11] |
| Disappeared weapons in EW | Focus on checking the desert's long-range weapon, the Reaper's Buster Shield, the heavily armed Army Knife, and the Two-Headed Dragon's Beam Cannon; "weapon without successor" does not directly equal a missing copy of the program. [S11] |
| EW comes with additional MAP weapons | Additional MAP weapons for Zero and Heavy may be obtained directly after the aircraft body is fully modified, and it is not prerequisite that the corresponding weapons are fully modified first; they are listed as original behavior verification and cannot be removed without authorization. [S11] |
| Parts are not on the machine body after automatic sortie | Akurasu records that the parts will be removed when changing the machine and automatic sortie. The inventory should be checked first, and "unloaded" should not be mistakenly reported as "destroyed". [S8] |

### QOL01: Preview and confirmation of replacement (plan)

EW does not become stronger in one direction for all usage methods: the documented component slots may be reduced, the Desert/Reaper range is shortened, and the Zippleback loses its long-range cannon. [S11] This supports the addition of confirmation pages, but does not prove that the changes themselves are bugs.

The design requirements are proposed by this project:

- Before triggering the payment for the last modification of the aircraft replacement, display the front and rear capabilities, weapon increases and decreases, range/consumption, weapon modification inheritance and component destination; allow the name of the successor aircraft to be hidden.
- When canceling, the funds, modifications, weapons, components, and flags will not change; when confirming, the actual conditions will be rechecked and submitted in one go.
- By default, the trigger is still based on the original threshold; if "the body has been completely modified, but the EW will not be changed for the time being" is provided, this is an additional behavior option, which requires definition of qualification retention, retriggering and archiving, and will not be quietly mixed into the confirmation page.
- The preview only shows verified mappings; unknown items are clearly marked, no full inheritance by default, no automatic refunds, and no copying of missing weapons or parts.

## 5. Behavior and other clues not directly classified as bugs

| ID | Behavior/Lead | Registration Decision |
| --- | --- | --- |
| WATCH01 | Gaia → Godmars, Hiro's Wing Zero's reappearance in OZ and other transformation and lost records | Akurasu lists route nodes, and some indicate other routes to be checked. [S8] As the route return seed of FIX04; no error will be detected before initialization and plot basis are obtained. |
| WATCH02 | Early motherships or weapons that disappear after replacement are not inherited | The data has listed items that are not inherited. [S8][S9] Providing tips first; unified inheritance/refund are optional rules; the modification and refund of the plot-deleted aircraft have been implemented as difficulty adjustment `upgrade-refund`, see [Optional Rule Amendment](rule-fixes.md) §2.6. |
| WATCH03 | The upper limit of funds obtained in a single battle is 65,535 | The player log calls it a bug, and the SRW Wiki records it as the upper limit. [S12][S13] First distinguish between clamping, overflow and display truncation, without directly determining that the upper limit should be increased. |
| WATCH04 | The general statement that "special defenses such as cutting, shield defense, and clones are buggy" | This time, a sufficiently specific SRW64 independent problem report was not located; there is an error in not extending "many bugged Pilot skills" to include all skills. Separate from BUG02's Aura Barrier diff. |
| WATCH05 | Modification type 0 weapons with power greater than 0 can be "free modification" | Static analysis of this project (2026-09-18), no external report. The modification list only excludes combined skills and ununlocked weapons, and only weapons with a power of 0 are rejected before confirmation; type 0 has a price of 0 and a preview power of 0. After confirmation, the number of stages +1 and the power temporarily changes to 0 until the next recalculation. We only have weapons such as the Structural H, the Structural Alliance S form, and the Bion belt, which cannot be reached in the basic form during preparation. See Section 6.1 of [Modification Sections](upgrade-limits.md); first use the actual machine to confirm whether it can be reached, and do not directly diagnose the bug. |
| QOL02 | The boss's fake body is hidden and the consumption process is cumbersome | The normal fake body mechanism is different from BUG05. Displaying the remaining times is information enhancement, and reducing the number is a rule change. |
| QOL03 | Combat performances cannot be skipped | Corresponds to B01 functional gap and is not listed as an original program error; the priority remains the first core. |

Cross-work skill bugs, abnormal units caused by cheat codes, simulator-specific graphics/audio glitches, and poor Transfer Pak contacts will not be merged into the original bug list this round.

## 6. Survey and Delivery Sequence

1. The B01 combat animation will be skipped and continue to be the starting core; this survey does not declare that random equivalence has been passed.
2. Defect investigation prioritizes the boundary recurrence of BUG09 and the status consistency check of BUG06; BUG05 has been completed (2026-09-18), and the rest is the comparison and return of archives on the original route.
3. ~~BUG01–04 Establish a skill/settlement comparison table, and decide on optional correction rules after numerical conflicts are resolved~~: Completed (2026-09-17), see [Optional Rule Corrections](rule-fixes.md).
4. BUG07/08 and LEAD01 establish field-level difference records for device switching, leaving the team and then joining; QOL01 uses the verified mapping.

Each upgrade to "reproduced" requires at least: input baseline and summary, clear steps, original and host observations, expected basis, and untriggered counterexamples. Upgrading to "Fixed" also requires evidence of cause, local fixes, regressions, and legacy compatibility. The amount of external data is not a substitute for these thresholds.

## 7. Source Index

All sources are clues; no official errata or complete test package with version identity was found that could be used for direct acceptance of this project. The full text of the guide or the entire value table will not be copied below.

- **S1 — [Akurasu:64/Bugs](https://akurasu.net/wiki/Super_Robot_Wars/64/Bugs)**. Community summary, the page shows oldid=62318; the super power and base strength values ​​conflict with the Japanese data.
- **S2 — [S-RPG navi：パイロットSpecial Skills](https://s-rpg-navi.com/srw64/sp-skill/)**. Skill effect table for personal strategy; no replayable test input for this project is provided.
- **S3 — [SRW Wiki: Super Powers](https://srw.wiki.cre.jp/wiki/超能力)**. Only use the "64" section and cannot apply to other work tables on the same page.
- **S4 — [SRW Wiki: Holy Warriors](https://srw.wiki.cre.jp/wiki/聖戦士)**. Only section 64 is used; documentation of barrier changes with levels.
- **S5 — [SRW Wiki：バグ（ゲーム）](https://srw.wiki.cre.jp/wiki/バグ_%28ゲーム%29)**. Only use the "64" section; five fly scenes, join issues, widget menu out of bounds. The "year of discovery" on this page does not retroactively refer to the first report and is not intended to be a definitive date.
- **S6 — [S-RPG navi：バグ](https://s-rpg-navi.com/srw64/bug/)**. Detailed strategy descriptions for Wan Zhang, Wu Fei and Limit.
- **S7 — [SRW Wiki：ガンダムシュピーゲル](https://srw.wiki.cre.jp/wiki/ガンダムシュピーゲル)**. Only subsection "64" is used; see also the rejoining record at [Game Directory Wiki](https://w.atwiki.jp/gcmatome/pages/3679.html), both of which have not proven independent forensics.
- **S8 — [Akurasu: Upgrades inheritance](https://akurasu.net/wiki/Super_Robot_Wars/64/Upgrades_inheritance)**. The page shows oldid=62286; there is a change route table and Rezner doubts, including reservation instructions for other routes that have not been checked.
- **S9 — [5ch: Comprehensive 12](https://mevius.5ch.io/test/read.cgi/gamerobo/1432899611)**. 2015-08-14 Nearby players discuss weapons that are not inherited; this can only prove player reports, not design intent.
- **S10 — [5ch: Comprehensive 14](https://mevius.5ch.io/test/read.cgi/gamerobo/1615283967)**. 2022-06-25～26 Direct attempt report from Building 573/574/576, including picture link and operation description; the reading is limited to the text visible in the search index, the crawling of the URL in the sub-floor range failed, and the attached pictures were not downloaded or identified.
- **S11 — [S-RPG navi: Transforming Relationships](https://s-rpg-navi.com/srw64/modification/)**. W Series Customization and Weapon Mapping; this table only extracts phenomena relevant to verification and is not considered a complete or verified conversion table.
- **S12 — [たくよ：スパロボ64をクリア](https://takuyo.blog.jp/archives/33876877.html)**. The player's clearance log has a bug classification on the upper limit of funds; no formula proof is attached.
- **S13 — [SRW Wiki：スーパーロボット大戦64](https://srw.wiki.cre.jp/wiki/スーパーロボット大戦64)**. Community notes on funding caps and vanilla mechanics.
- **Video clue — [ぎんぱちゅ：スパロボ64のバグ 5 selections](https://www.youtube.com/watch?v=mCOgwvxBmHQ)**. 2022-08-30; The description states that the actual Nintendo 64 machine is used, and the chapters are 00:28 Limits, 02:16 Skills, 04:56 Titan 3, 06:27 False Body, 07:31 Another Bug. This round only reads the author description and chapters in the index. The playback page fails to be captured. It does not claim to have seen the actual screen or confirm the steps to reproduce the last section.

Returns: [Built-in MOD Roadmap](../design/mod-roadmap.md) · [Technical Document Index](../README.md)

[S1]: https://akurasu.net/wiki/Super_Robot_Wars/64/Bugs
[S2]: https://s-rpg-navi.com/srw64/sp-skill/
[S3]: https://srw.wiki.cre.jp/wiki/Superpowers
[S4]: https://srw.wiki.cre.jp/wiki/圣戦士
[S5]: https://srw.wiki.cre.jp/wiki/バグ_%28ゲーム%29
[S6]: https://s-rpg-navi.com/srw64/bug/
[S7]: https://srw.wiki.cre.jp/wiki/ガンダムシュピーゲル
[S8]: https://akurasu.net/wiki/Super_Robot_Wars/64/Upgrades_inheritance
[S9]: https://mevius.5ch.io/test/read.cgi/gamerobo/1432899611
[S10]: https://mevius.5ch.io/test/read.cgi/gamerobo/1615283967
[S11]: https://s-rpg-navi.com/srw64/modification/
[S12]: https://takuyo.blog.jp/archives/33876877.html
[S13]: https://srw.wiki.cre.jp/wiki/スーパーロボット大戦64