> **Language / Ngôn ngữ:** [English](controls-remapping.en.md) · [Tiếng Việt](controls-remapping.vi.md) · [中文](controls-remapping.md)

# Change keys

2026-09-28. User requirements: Button settings plus controller diagram comparison, plus the additional buttons of this game, which can be identified and set with one click. Process: First, I used the N64 controller diagram provided by the user (two versions, the second version added a virtual L2/R2 under L/R, and a label for each of the four directions of the cross key); after reading [original button analysis](../gameplay/original-controls.md), the user thought that the original version did not have many useful keys, so it was changed to **organized by function** and the layout of Steam Deck ("Just use steamdeck" "), the picture is drawn by ourselves according to the flat style given by the user (dark gray background, white button shape, key name written on the shape). On the same day, the user decided not to take pictures ("I still feel like I don't want to take pictures"): the controller will be set up as Steam Deck by default, and the keyboard will be set up as PCSX2 by default. The settled approach:

- After changing the key, the native page will follow the new key, and Enter, Esc, and arrow keys are always available;
- The joystick does not need to be changed separately (user: the joystick is not needed), it is "moved" like the cross key;
- The default values ​​of the controller are rearranged by function. The keyboard defaults to the layout of PCSX2, which is in the same position and function as the controller (see "Data" below);
- The operation page only has a menu and no handle diagram.

## Data

[`input_bindings.hpp`](../../src/host/input_bindings.hpp) (does not rely on SDL, key code and controller number are as per SDL, check with `static_assert` in `graphics.cpp`):

- **Actions**: N64's A, B, Z, START, L, R, C four-way, D-pad four-way, joystick four-way, plus six buttons for this game - setting window (view key), function 1 (L2: dialogue automatic reading switch, an enemy on the map), function 2 (R2: dialogue fast forward, next enemy on the map, end the show in battle), battle animation switch (Y), switch language (L3), original/HD (R3).
- **Binding**: Each action has a keyboard key list (scan code) and a handle input list (keys, or a direction of a certain axis, counted after 16000 presses). The default value of the handle was changed to function priority on 2026-09-28 (the direction determined by the user after reading [original button analysis](../gameplay/original-controls.md)): A, B, START, LB/RB, cross keys, and left joystick are as in the original version; Z is just an alias for L in the list, and only Z+START is left alone to return to the title, and no more keys are given; map cursor acceleration); Y switches battle animation; press the left and right joysticks to switch language and original/HD; the right joystick is still the C key (↑↓ dialogue font size, title track ±10); the view key and two triggers return to the host.
- **Keyboard Default** (User 2026-09-28: "The default key positions of PC/MAC use the default setting method of PCSX2"): PCSX2's keyboard automatic mapping (`pcsx2/Input/InputManager.cpp`'s `GetKeyboardGenericBindingMapping`) gives each key of the controller a key position, and we let each key do the same thing as the key of the controller:

| Controller (Deck) | PCSX2 Keys | Functions |
  |---|---|---|
| A (bottom) | K | Confirm (A) |
| B (right) | L | Cancel (B) |
| X (left) | J | Press and hold the cursor to accelerate (C←) |
| Y (upper) | I | Combat animation switch |
| Menu | Enter | START |
| View | Backspace | Settings window (also fixed Ctrl/Cmd + ,) |
| L1／R1 | Q／E | L／R |
| L2／R2 | 1／3 | Function 1/ Function 2 |
| Press the left/right joystick | 2/4 | Switch language/original HD (there is also a fixed F7/F6) |
| Cross keys | Direction keys | Cross keys |
| Left Joystick | W A S D | Joystick |
| Right joystick | T F G H | C key (F is also C←) |

Z, like the controller, does not have a key. The keyboard table before the change (Z=A,
- **Seize**: When an input is given to an action, it replaces all the input of the action on this device; the action that originally occupied it loses it. If there is no key because of this, the original first key of this action is obtained - equal to interchange, no key will be lost.
- **Save**: `input.json` (the launcher is placed in the user directory, `SRW64_INPUT_SETTINGS`; the development run is placed next to the presentation settings), only write actions different from the default, according to the SDL name (`"Z"`, `"Return"`; `"a"`, `"leftshoulder"`, `"righty-"`). If you read a name you don't recognize, throw it away.
- **Per frame**: `graphics.cpp` counts the N64 bit and the host bit according to the binding; the virtual key held down by the debugging interface does not look at the binding, and is fixed according to `classic_keys()`, so `z` in the script is still A. Read the merged state of the three places of the L2/R2/view key (dialogue, enemy switching, setting entry), so it can be used even when tied to the keyboard.

## Tips and Pages

- The token of the prompt entry is an action (`{A}``{Start}``{L}``{CUp}``{DPad}``{Settings}``{AuxL}` ...), display the current binding: the handle prompt displays the key icon (press the controller family), and the keyboard prompt displays the key cap icon or key name (following the keyboard layout). Combination symbols display an overall icon by default. Page fixed keys `{Enter}``{Esc}``{Tab}` and arrow key icons do not change with binding. See [`button_prompts.hpp`](../../src/native/text/button_prompts.hpp).
- Native page: The page code presses the old keyboard recognition keys (Z to confirm, X to cancel...). When a keyboard event comes in, the key bound to a certain N64 key is translated into the key in the old table (A→Z, L→Q, cross key/joystick→direction key..., `follow_bindings` of `frontend.cpp`); Enter, Esc, Tab, and direction keys are not translated; letter keys that are not bound to any function do not work on the page (otherwise, Z, X are defaulted to will still confirm, cancel); the keys bound to the setting window open and close the setting window; the keys bound to functions 1 and 2 have no effect on the page. The key pressed in the debugging interface does not have a window number. Press the old table to enter the page directly. The name page no longer has an input box (the name is fixed) and is also bound. The handle has been moved according to the N64 position through `pad_keys` and follows naturally.
- Dialogue bottom bar prompts are expanded when the host takes a frame snapshot (`Frame.controls_text`), portable scene drawing does not require SDL.

## Operation page

`controls_page` of `frontend.cpp`:

1. **Recognized handle**: The name of the handle reported by SDL, it is recognized when plugged in (press Deck when `SteamDeck=1`); if there is no handle, write "not connected". Change button icons by controller family (Xbox/Deck/PlayStation/Nintendo). The next line states that the keyboard defaults to the PCSX2 layout.
2. **Change keys**: One row for each function (`control_rows[]`: OK, Cancel, START, Previous, Next, Function 1, Function 2, Cursor Acceleration, Font Size Enlargement, Font Size Reduction, Combat Animation, Settings Window, Language, Original/HD, Four-way Cross Keys, Z). The two columns on the right are the current bindings of the keyboard and controller. Select a line, and a pop-up message "Please press the new key for "..." will appear. The next keyboard key or handle key (press the button or push the joystick or trigger to the end) will be bound to it, and the device will be changed from which device it was pressed. Esc cancels, and it will be canceled if it is not pressed for 6 seconds; F5-F8 are rejected. After pressing the handle, you must wait until all are released before the page can re-accept handle navigation.
3. **Fixed shortcut keys** and **Restore default keys**: Ctrl/Cmd +, settings, F5 to reload lines, F6 original/HD, F7 language, Esc to exit, cannot be changed.

The original four sets of read-only key tables (`settings_key_*`/`settings_bind_*`) are replaced by this function table, and the entries have been deleted. The existing Steam Deck controller diagram (drawing script draw_deck_diagram.py, image directory content/ui, `SRW64_UI_ASSETS` and the ui directory in the package, see 8b7518d and before) has been deleted along with the "unnecessary pictures".

## Test

- `make recomp-input-bindings-test`: The keyboard defaults to the PCSX2 layout and has the same functions as the controller. The old table, exchange rules, and save copies are only saved when there is a real change.
- `make recomp-button-prompts-test`: The mark is expanded according to the binding, and the prompt will change after changing the key.
- `tests/test_button_prompts.py`: The symbols in the three languages are consistent, the handle prompts do not require page fixed keys, and the keyboard prompts no longer write down letters.
- `tests/test_debug_coverage.py`: The keys in the old table all have virtual keys with the same name. The virtual keys are calculated according to the old table, and the physical keys are calculated according to the binding.
- Keyboard rekeying 2026-09-28 has been verified on the actual machine (there was also a picture of the controller at that time); the handle rekeying has not been implemented on the actual machine.