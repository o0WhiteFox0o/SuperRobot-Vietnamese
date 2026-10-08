> **Language / Ngôn ngữ:** [English](battle-ui-design-brief.en.md) · [Tiếng Việt](battle-ui-design-brief.vi.md) · [中文](battle-ui-design-brief.md)

# Pre-war UI: Attack and Counterattack Design Instructions

Date: 2026-09-21. This article is used for interface design review and subsequent adjustments. The actual machine screenshots (self-made mini-levels) at that time were used as the current baseline and were not saved with the warehouse; the design goals and acceptance requirements do not mean that every visual detail has reached the final effect.

## Design goals

1. **Be able to make combat decisions before confirming. ** Players can quickly compare the hit, critical hit, damage and defense capabilities of both sides, and complete changing weapons, using spirits and choosing response methods on the current page.
2. **The left and right sides are symmetrical and the warring relationship is clear. ** The enemy is fixed on the left and we are fixed on the right; attack and counterattack follow the same layout. The body is facing the center, similar information is at the same height, and the main values ​​are easy to compare horizontally.
3. **Continue the look and feel of the original version and absorb the information organization of Machine War Y. ** Retain the dark blue panel, cyan border and battlefield map; refer to Y’s mirror images of both sides, driver information area, mental status grid and central operation area.
4. **Show credible and interpretable results. ** Hits, critical hits, and damage are consistent with actual settlement. The effects of spirit, skills, shields, etc. should be understandable to players; the interface does not reveal random determination results in advance.
5. **Retain the sense of battlefield location. ** The map and units can still be seen between and below the panels, preventing pre-battle confirmation from completely blocking the battlefield.

## Picture 1: Our active attack

Scene: Wanzhang on the right actively attacks the enemy aircraft on the left. The sure hit and big roots have been used, the SP remaining is 18, the HP is restored to 3000/3000, and the base power is not activated. This diagram is used to review the information, mental state, and operational entry points of both parties involved in active attacks.

**Operational Requirements**

- The main operation is "Start Combat"; the auxiliary operations include "Select Weapon", "Spirit", "Combat Animation On/Off" and "Return to Selection".
- Selecting a weapon should directly open the weapon list. Range, ammo, EN, energy, and post-movement availability restrictions are preserved; preview is recalculated after selecting a weapon and legal target.
- Return to the current engagement after using spirit, retain valid weapons and targets, refresh SP, HP, energy, hit, critical hit, damage and ability status.
- Returning to target selection or canceling an attack does not consume the attack action; the spirit that has been cast and its SP consumption are retained.

## Picture 2: Enemy attack/our counterattack

Scenario: The enemy attacks on the left, and Wan Zhang responds on the right. Wan Zhang has used must-dodge, has 3 SP left, and the opponent's hit is 0%; reselect a legal weapon and resume counterattack. HP 1575/3000, EN 75/150, the lost part is indicated in red.

**Operational Requirements**

- Support three responses: "counterattack", "avoidance" and "defense" to clarify the current choice; the confirmation button or adjacent state should let the player know which one will be executed.
- You can change counterattack weapons, and you can also use spirits on this page. Use spirit after selecting evasion/defense, and keep the response option when returning; reselect a legal counterattack weapon and switch back to counterattack.
- When avoidance/defense prevents us from attacking, the attack value will be displayed as "-" and the reason will be explained. The card height and information position will remain stable.
- When the enemy attack has been established, there is no ordinary cancellation entrance to exit the engagement; closing the mental menu will only return to the response page.

## Common needs of both pages

| Information area | Required display and behavior |
| --- | --- |
| Body and pilot | Large picture of the body, name of the body, driver's avatar and name, level, and strength. The two sides of the machine face each other; the driver's avatar remains in the original direction. |
| Resources | Current/maximum HP and EN of both parties, current/maximum SP of the driver. HP/EN is currently partially green, and has lost some red; the left and right fill directions are mirrored, and the values ​​are consistent with the bar length. |
| Weapon | Current weapon name, EN/ammo consumption, weapon hit and critical hit correction; unavailable options indicate restrictions. Weapon corrections have been included in the final probability and cannot be added again. |
| Core Preview | Hit rate, critical hit rate, damage on hit and critical hit damage of both sides. Highlight major values ​​and place minor explanations in adjacent areas or details. |
| Mental state | The spirits that both parties have learned and are currently in effect are presented in the status grid. Gray when not in effect, highlighted when in effect; instant recovery types are not displayed as continuous buffs. Display names to avoid expressing status by color alone. |
| Spirit Selection | Each pilot of our participating aircraft displays the acquired spirit, current SP, consumption and available status respectively; no overdraft, repeated error deductions or consumption of another pilot's SP are allowed. |
| Special Defense | Both sides display the probability of cutting down, shield defense, and clone. Explain the restrictions on equipment, skill level, strength, guaranteed hit coverage, whether the weapon can be cut off, etc.; these are the conditional probabilities of each judgment and cannot be added directly. |
| Shield | Based on the actual shield type and weapon attributes of this game, it will display whether it is applicable, neutralization/damage reduction/penetration, damage change and EN consumption. You cannot judge based on whether the weapon name contains "beam" alone. |
| Ability effects | Basic power, new human/enhanced human world, holy warrior, super power, and other abilities that affect hit, avoidance, defense, display level, whether it takes effect this time, specific corrections and reasons for not taking effect. The base strength is refreshed with the current HP, and the armor bonus from other works is not used. |

## Layout and interaction acceptance

- The cards on both sides have the same width and height, and the HP/EN, identity, spirit, weapons, core values, special defense and ability areas are aligned line by line. The entire card cannot be raised because there is more content on one side.
- Hit, damage and current response are visible first; detailed corrections allow independent scrolling, but cannot squeeze out of the main operation area. Long names and mental state boxes cannot overlap or obscure the main data.
- When the mental menu is open, background operations cannot be triggered; the arrow keys and Tab only cycle through the currently available options. Esc closes the submenu first, and the confirmation key cannot penetrate the map.
- Complete operation via mouse and keyboard. After changing weapons, using spirits, and switching responses, all associated values ​​will be refreshed simultaneously.
- Under the logical windows of Chinese 960×720, English 800×600, and Japanese 1100×760, the main buttons are visible and operable, and the left and right structures remain consistent.
- Verify with new native build → Main menu → Customized mini-level; use existing debugging interface, actual SP/resource changes and GPU screenshot acceptance.

## Current boundary and next round of visual focus

- The spirit of selecting a target on the map, as well as self-destruction and resurrection are currently disabled on the pre-war page and prompt for map entry; the current page does not include the map target selection process.
- In the counterattack screen at that time, "0% hit" was still juxtaposed with the conditional damage. In the future, the meaning of "damage on hit" should be placed near the value to avoid being understood as being certain to receive this damage.
- The current counterattack confirmation button still reads "Start Fight"; in the future, "Start Counterattack/Avoidance/Defense" can be displayed based on the response to strengthen the current operating status.
- The side with more information currently requires scrolling to view some corrections. Subsequent adjustments should prioritize keeping the main numerical values ​​and ability status visible, then compress and repeat explanations, and continue to retain map space.

The screenshots were taken from `actions-zh-Hans.png` and `counter-ready.png` of the local debugging run, and the corresponding running check is `action-checks.json`; these local files are not saved with the warehouse.

For implementation details, formula caliber and verification records, see [Pre-war UI technical documentation](native-battle-ui.md).