> **Language / Ngôn ngữ:** [English](enemy-cycle.en.md) · [Tiếng Việt](enemy-cycle.vi.md) · [中文](enemy-cycle.md)

# Tactical map: L2 / R2 switch enemy aircraft

2026-09-25 User request: Use L2 and R2 to traverse enemy aircraft on the battlefield like modern aircraft combat. The original L/R (and Z) already switch between our inactive units, and here we fill in the enemy's. It is implemented in [`enemy_cycle.cpp`](../../src/host/enemy_cycle.cpp), and the key list can be found in [Steam Deck Keys](../design/steam-deck-controls.md).

## Operation

- When the map is idle (no unit menu opened, no grid selected): **R2** put the cursor on the next enemy body, **L2** put the cursor on the previous one. Hold down to fire in bursts: 24 VIs followed by one for every 8 VIs.
- If the cursor is originally on an enemy aircraft, count forward or backward from it; if the cursor is not on any enemy aircraft, R2 starts from the first one, L2 starts from the last one, and the cycle starts from beginning to end.
- The order is roster order: first the enemy (Faction 1) 30 slots, then the third party (Faction 2) 30 slots, only those on the map are counted (status byte is 1).
- The operations after placing the cursor are the same as the original: press A to view the body (ability, movement range, etc.), which is the same as using the direction keys to move the cursor.
- It does not work when two triggers are pressed at the same time and the setting window is open. L2 and R2 are host keys and cannot be seen in the game itself; they have other uses in dialogue (L2 auto-read, R2 fast-forward).

Currently, only the controller can be used, and there are no corresponding keys on the keyboard.

## How to make the original version (static analysis)

The `load_000AB160_func_801C8B04` in the generated code `build/recomp/cpu-bound/generated/funcs_32.c` is the function of each frame in the idle state of the tactical map (main state 5, state table `0x80217E0C`):

| Steps | Instructions |
| --- | --- |
| Trigger | Read the consecutive words `D_801612E0 & 0x2030` (Z, L, R); if it is not 0, switch, otherwise process the direction (`801C66E8`), A, B, etc. |
| List | Traverse our roster `0x8015E100 + 槽×0x14` (30 slots): Status byte `+0` = 1. Pilot (`+0xC` body → `+0x38`) `+0x35` is not 0, `+1 & 0x80` is 0 (no action); `801E514C(阵营, 槽)` give handle |
| Current position | `801C2BFC()` is the handle under the cursor, find its subscript in the list, there is `0x80172EDF`; Z or L decreases by one, R increases by one, out-of-bounds loop |
| Put the cursor | The object coordinates `0x800FFA74 + 句柄×0xC4` (`+0`, `+4`, f32 map pixel) corresponding to the handle are written into the cursor `0x80102308/0C` and the target `0x80172EB4/B8`; `801FFE34(x, y)` is judged whether it is in the screen or not, `801FFCB0(x, y)` Move the camera |
| Sound effects | Play from the beginning `8007E8A8(0xB9)` |

`801E514C` just replaces the camp and slot with handles: camp 0/1/2 are `0x42`/`0x60`/`0x7E` plus the slot number respectively. Roster `0x258` bytes per camp.

## Takeover method

- `NATIVE_HOOKS` renames `801C8B04` to `srw64_original_map_idle`, and the packaging of [`game_hooks.cpp`](../../src/host/game_hooks.cpp) first asks the `map_idle` hook. If `NATIVE_HOOKS` is changed, run `make recomp-cpu` again.
- In the frame when the trigger is just pressed (or held until the burst moment), the host will place the cursor as in the original version: first play 0xB9, write the cursor and target, the camera will only move when the body leaves the screen, and then the original function will not run in this frame. Other frames run as is, and directions, A, B, L, R, are not affected.
- Neither the enemy nor the third party looks at the action position, nor the driver's `+0x35` (these two items are only meaningful to us).
- Whether the cursor is already on an enemy body is judged by coordinates (the difference is less than half a grid), and `801C2BFC` is not called.
- Log: `enemy-cycle-events.jsonl`, one line per step (direction, camp, slot, handle, coordinates, number of enemies). The debugging interface `status` has `enemy_cycle` (the number of steps and the last step).

## Verify

It has not been run in real machine yet. How to prepare:

- The debugging interface adds the `pad` method and `srw64ctl pad` (press the Deck key name, such as `srw64ctl pad r2 r2 l2`), so you can press L2 and R2 on Mac without using a real controller.
- In a mini-level with multiple enemies: press R2 repeatedly to traverse all the enemies and finally return to the first one; L2 reverses; the camera follows the enemy when it is outside the screen; press A with the cursor on the enemy to open the original enemy view; press and hold R2 to fire continuously.
- Static inference that requires confirmation: the object coordinates of the third-party (camp 2) handle are also in the object table; when the enemy's status byte is 1, it must be on the map and can be pointed by the cursor.