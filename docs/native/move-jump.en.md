> **Language / Ngôn ngữ:** [English](move-jump.en.md) · [Tiếng Việt](move-jump.vi.md) · [中文](move-jump.md)

# Move the selected frame: Press and hold R to jump to the furthest frame

2026-09-25 The user requested the operation of adding modern aircraft combat: when selecting the moving destination, press R1 and highlight the farthest grid that can be reached; press the direction while holding R, the cursor will quickly jump between these grids, and press A to confirm the move. Refer to "Super Robot Wars 30": Press R1 when the movement range is displayed, and the cursor jumps to the maximum range ([ナノゲームス TIPS](https://ds-can.com/srw30/system/s_tips.html)).

Implemented in [`move_jump.cpp`](../../src/host/move_jump.cpp). The addresses below are all from static analysis (tactical overlay `load_000AB160`, generated code `build/recomp/cpu-bound/generated/`).

## Operation

- **Hold R** (Keyboard E, Controller RB): Stack a layer of warm yellow on the farthest grid, breathe slowly, and the range does not exceed the original grid. If the cursor has left the unit before pressing R, it will jump to the farthest grid in this direction; the cursor will not move while it is still on the unit.
- **Press direction while holding R** (D-pad or joystick, diagonal also works):
- The cursor is on the farthest square: jump to the nearest farthest square within 45° to the left and right of this direction. Hold down the direction and walk along the outer circle one square at a time, without skipping corners; if there is no one in this range, just take the one with the least deviation in front.
- The cursor is not on the farthest cell: Jump to the farthest cell in this direction from the unit.
- Move according to the game's own burst rhythm while holding down the direction: press to move one frame immediately, and every 3 frames after 12 frames.
- **A／B**: Confirm and cancel as usual, whether loose or not is the same. Release R, the highlight disappears, the cursor stays where it is, and the arrow keys resume the original frame-by-frame movement.

## What is the "farthest grid"

Among the squares where the unit can stop, there is no shortest path that passes through it and leads to another square where the unit can stop. The shortest path is calculated based on the entry cost of each grid in the grid, which is consistent with the `801C3B0C` of the original form.

- Flat ground is the outer circle of the range; the end of a dead end also counts.
- When the range touches the edge of the map, only the two ends of the line are counted.
- Grids that are only blocked by lakes and friendly forces on one side are not counted: you can go further by going around them.

## How to make the original version (static analysis)

| Item | Address | Description |
| --- | --- | --- |
| Status distribution per frame | `801DFBD0` | Table `0x80217E0C[状态]`, status byte in `0x80172EB0`. Then call `801C3020` (unit under cursor), `80081BFC` (object speed), `801FFADC` (lens following) in sequence |
| Status 0xC | `801CD6E4` | Check table `0x80217B38` by sub-state `0x80172EB2`: 0 selection `801CBB04`, 1 unit walking `801CC290`, 2 `801CC72C`, later 3–6 |
| Selection | `801CBB04` | A confirms, B cancels (tone 0xB8, cursor returns to anchor point, returns to state 8), direction call `801C66E8`→`801C63D8`, press and hold C down/C left to accelerate movement. **R, L, Z, and START are not read in states 0xC and 6** |
| Input words | `D_80178A08` Press this frame, press `D_800F97D0` and hold, `D_801612E0` burst | One and a half words per mouth, the joystick is integrated into the cross key. A 0x8000, B 0x4000, R 0x10, upper 0x0800, lower 0x0400, left 0x0200, right 0x0100 |
| Cursor | `0x80102308`/`0C` | f32 map pixels, equal to grid × 16+32 (object 0x35); target `0x80172EB4`/`EB8`, speed `0x8010232C`/`30` |
| Lens | `0x8010F5D4`/`D8` | Integer, screen coordinates = map coordinates + offset. `801FFCB0(px,py)` Move the point to the center of the screen: x offset = clamp(152−px, 320−map width, 0), y offset = clamp(112−py, 240−map height, 0); `801FFE34` determines whether the point is within [32,288]×[32,208] |
| Map size | `0x80172EC4`/`EC8` | Pixels |
| Movement range | `0x80227BD0` | A 31×31 grid centered on the unit, stored in rows, the unit is at (15,15): 2 can stop, 3 can only pass through if friendly troops are present, and the center is 0. Entry cost at `0x80227328` |
| Drawing range | `801E4760` | Callback of node 0x2E (`801CB9B0` registration), a0 = `Gfx**`. Assume the combiner is primitive color, off texture, primitive color (0,192,0,96), each grid with a value of 2 is a 16×16 G_FILLRECT; upper left corner = anchor point + camera offset + (grid −15) × 16 |
| Confirm | Branch A of `801CBB04` | `801E0B94(2, 光标x, 光标y)` Check whether the cursor cell is 2; if not, it will buzz 0xBA, if it is, it will even if the path and unit have passed |

In the original version, when the cursor is placed somewhere (`801C8E20`, switching units, etc.), the same paragraph is inlined: the cursor and the target are written together. If the point is not within the screen, `801FFCB0` is called, and the cursor notation 0xB9 is played. Do the same for tabs while holding down R.

## Takeover method

- `NATIVE_HOOKS` wraps two functions ([`game_hooks.cpp`](../../src/host/game_hooks.cpp)):
- `801CBB04` was renamed to `srw64_original_move_select`.
- `801E4760` was renamed to `srw64_original_move_range_draw`.
- After changing `NATIVE_HOOKS`, run `generate_cpu.py` again.
- **Cell selection**: When R is pressed and A or B is not pressed in this frame, the host will process this frame, the original function will not run, and the direction will not allow the cursor to move frame by frame (state 6 cannot be entered). In other cases, it runs as the original version.
- **Tap Frame**: The method is the same as the original section where the cursor is placed, and the conditions for moving the camera to the center are also the same.
- **Highlight**: After the original drawing range is completed, add a primitive color (warm yellow, alpha 72–128, press VI to breathe) and the farthest frame G_FILLRECT after the same display list, and crop it to the screen. The blending mode follows the settings of the original drawing range.
- **Recalculation Timing**: If the anchor point changes (the unit is changed), if R is released and then pressed, the farthest grid will be recalculated.
- **Log**: `move-jump-events.jsonl`, records on, off and jump events.

## Actual machine verification

Test level [`move-jump.json`](../../config/recomp/mini-stages/move-jump.json): Map 20, タケル is at (8,8), friendly ダンバイン is at (10,8), enemy is at (15,12). Check Script [`check_move_jump.py`](../../tools/recomp/debug/check_move_jump.py) By debugging keyboard operations (E is R), check the following 10 items:

1. Enter the selection box;
2. Press and hold R to display the furthest grid and the cursor will not move;
3. The highlights are drawn;
4. Press right to jump to the rightmost grid;
5. Press down twice to walk along the outer circle;
6. Press and hold left burst;
7. The highlight disappears after releasing R;
8. The direction keys resume moving frame by frame;
9. Press and hold R again to jump out along the ray;
10. Press A while holding R. The unit will walk over and the post-move menu will appear.

Result (`build/recomp/debug/20260925T103341.713940Z/`):

- All 10 passed.
- The range of ガイヤー is a rhombus with a radius of 6, and the farthest tile is exactly 24 tiles from the outer circle.
- While pressing left, move along the outer circle one square at a time to the leftmost square, passing the bottom corner as well. When running for the first time, the straight line is given priority and the bottom corner is skipped. It has been changed to the closest value within 45°.
- The highlight is a translucent warm yellow, superimposed on the original green grid without exceeding the grid.

Not covered:

- The farthest grid when terrain blocks the road (lake, mountain): the range of this level is a complete diamond.
- Camera shift when jumping off-screen: the entire range of this level is on the screen.
- Press and hold the direction first (the cursor is already moving, state 6) and then press R: it will not take over at this time, and you have to wait for the direction key to be released.
- Hold R while viewing enemy range (roster flag read-only): Also able to skip, but A-shot doesn't work.