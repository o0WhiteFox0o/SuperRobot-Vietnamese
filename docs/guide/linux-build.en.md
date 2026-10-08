> **Language / Ngôn ngữ:** [English](linux-build.en.md) · [Tiếng Việt](linux-build.vi.md) · [中文](linux-build.md)

# Linux and Steam Deck build

2026-09-25. [Three Platform Porting Plan](../design/three-platform-port.md) First version of X2: running the game with Vulkan on Linux x64. The five HD layers have been converted to plume (X1) and draw the same on Linux as on macOS. The HD material package is the same download as the macOS version, just unzip it to `~/.local/share/srw64-recomp/hd`; you can also use `build_linux.py --hd DIR` to directly put it into the package for your own use (`hd/` is next to the program).

## Build on Mac

Start with `make` as usual on your Mac, and have the font ready (`tools/content/prepare_fonts.py`). Then start Docker Desktop and run:

```sh
tools/release/linux/build.sh --jobs 8
```

The script does three things:

1. Run `prepare_rt64.py` on Mac and confirm that the RT64 patch (including the "rendering completion" hook) has been applied;
2. Build the Ubuntu 22.04 x64 image described by `tools/release/linux/Dockerfile`;
3. Run `tools/release/build_linux.py` in the container. The container hangs the warehouse at the same absolute path, so that the path recorded in the generated file is consistent with the Mac.

Containers on Apple Silicon run via x64 emulation, and the first build (dependencies plus RT64 plus generated code) takes a long time. Then only the changed files will be re-edited.

## Build on x86-64 Linux machine

Running the same container on a native x86-64 Linux machine is much faster than simulating it on a Mac. The method is to combine the warehouse (including `.git`, so that the submission number in the package name is consistent with `-dirty`) and the platform-independent input produced by `make` (under `build/recomp` `cpu-bound`, `upstream`, `audio-probe`, `runtime-lifecycle`, `graphics-source-patches.json`, `thirdparty/librashader/linux`, and `build/fonts`, `build/macos-deps/sources`), build the image there and run `build_linux.py`:

- The container must hang the warehouse at the same absolute path on the Mac, and the source code path recorded in the generated file must be correct;
- Run as the user of that machine (`--user $(id -u):$(id -g) -e HOME=/tmp`), the product will not become root owned;
- Each upstream checkout does not need to have `.git`, but `.srw64-revision` (the content is the result of `git rev-parse HEAD` on Mac) must be written in each checkout, the same as Windows CI; otherwise `prepare_runtime_lifecycle.py` will read the submission of the outer warehouse and report `Runtime lifecycle source revision differs`;
- What does not need to be passed: `target/`, the Rust product of librashader on Mac, the directory that relies on the source code package to be unpacked (re-unpacked from the compressed package when building), RT64 only for Windows, `mupen64plus-win32-deps`, a total of about 1.2 GB.

To run the test on a machine without a graphics card, use Xvfb plus lavapipe. The Mesa 22.3.6 lavapipe that comes with Debian 12 causes a segmentation error in the driver as soon as the game is started. It needs to be replaced with the Mesa 23.2.1 in the Ubuntu 22.04 update source: add `xvfb mesa-vulkan-drivers libvulkan1` to the build image, and the game is run in this container. Add `--network host --pid host` to the container. The loopback port of the game monitor and the process number in `debug.json` must match on the host. Connect from other computers as usual `attach.py --host <主机> --data-dir <数据目录>`:

```sh
docker run -d --name srw64-run --network host --pid host --user $(id -u):$(id -g) -e HOME=/tmp \
  -e XDG_DATA_HOME=$T/data -v $T:$T -w $T/<包名> <运行镜像> \
  sh -c "Xvfb :98 -screen 0 1280x800x24 & sleep 1; DISPLAY=:98 exec ./marchwind64.sh --debug"
```

(`T` is the test directory, the ROM is placed in `$T/data/srw64-recomp/rom.z64` and deleted after testing.)

## Construction steps and products

`build_linux.py` only runs on x86-64 Linux, and products are under `build/linux-x64/`:

| Steps | Content |
| --- | --- |
| Input checks | The generated code is consistent with the digest of `cpu-bound/report.json`, RT64 rendering completion hooks are present, RSPRecomp audio sources and fonts are present |
| Depends on `deps/prefix` | Use the same batch of source code packages in the macOS lock (`config/recomp/macos-dependencies.json`) to compile the shared libraries of SDL3, sdl2-compat, FreeType, HarfBuzz, and ICU. The source package cache is shared with macOS recipes `build/macos-deps/sources` |
| Host `gfx-build` | `src/host` builds `srw64-gfx-host` with `SRW64_ENABLE_RT64=ON`, compiler clang, linker lld; RT64's file dialog box goes to xdg-desktop-portal (`NFD_PORTAL=ON`), does not link to GTK |
| Package `Marchwind64-SteamDeck-<版本>-<提交日期>-<提交>.tar.gz` (named according to version, date and submission starting from 2026-09-29, the prefix before renamed Marchwind64 was `SRW64-SteamDeck-`, such as `SRW64-SteamDeck-0.3.1-20260929-eb1cd4a`; when there are unsubmitted changes, add `-dirty` after the submission number) | `VERSION.txt` (same name, installed to You can also see the version after `~/Games/SRW64`), programs `srw64`, `lib/` (the above five libraries, RUNPATH is set to `$ORIGIN`), `fonts/`, `dialogue/`, `licenses/`, startup script `marchwind64.sh`, `add-to-steam.sh` and `steam/` (see below), `README.txt` |

There are two checks when packaging, and it will stop if it fails:

- The system libraries that programs and package libraries depend on can only be glibc, libstdc++, libgcc_s, zlib, and libdbus;
- Required glibc symbol version no later than 2.35.

X11/Wayland, PipeWire/PulseAudio/ALSA are loaded when SDL3 is running, and Vulkan is dynamically loaded by plume via volk, so they will not appear in the dependency list. The report is written in `build/linux-x64/package.json`.

## Install and run

See `README.txt` in the package. Summary:

1. Unzip to any directory.
2. Place the ROM in `~/.local/share/srw64-recomp/rom.z64`, or put it next to `marchwind64.sh` and name it `rom.z64`.
3. Run `./marchwind64.sh`.

`marchwind64.sh` Find the ROM first, default to Simplified Chinese when starting for the first time, and then execute `srw64 --play`. When the ROM cannot be found, use `kdialog` (comes with SteamOS desktop) or `zenity` to pop up a description, because the terminal output cannot be seen in the game mode of the Deck. Archives and settings are in `~/.local/share/srw64-recomp`, which has the same directory structure as the macOS version.

On the Steam Deck: Enter desktop mode, open Steam, and double-click `add-to-steam.sh`. You can then boot from game mode. For controller mapping, see the controller section of `graphics.cpp`, and there is a list in README.

`add-to-steam.sh` calls `steam/add_to_steam.py` in the same way as right-clicking "Add to Steam" in the SteamOS file manager:

1. Write `~/.local/share/applications/srw64-recomp.desktop`, and the name follows the game language (`presentation.json`'s `locale`; it will be simplified Chinese if it is not started): Super Robot Wars 64 / Super Robot Wars 64 / スーパーロボット大戦64;
2. Use `steam://addnonsteamgame/<desktop 文件>` to pass it to running Steam;
3. Wait for the shortcut to start `marchwind64.sh` to appear in `userdata/<用户>/config/shortcuts.vdf` (binary KeyValues), and read out its appid (the `srw64.sh` shortcut before renaming in the same folder is also considered to be in the library and will not be added again. It only prompts to change the target to `marchwind64.sh` in the Steam properties). The appid of the new version of Steam is random and cannot be calculated in advance;
4. Copy the cover in `steam/` to `userdata/<用户>/config/grid/`: `<appid>p.png` vertical version 600×900, `<appid>.png` horizontal version 920×430, `<appid>_hero.png` top banner, `<appid>_logo.png`, `<appid>_icon.png`.

Only the cover page is refreshed when in the library. The cover is `tools/release/linux/steam-art/*.png` in the warehouse, which is copied in as it is when packaging, so the package built on GitHub Actions also has a cover. They are generated by `tools/release/linux/steam_art.py`: the title logo of the HD package (`scene_images` of `content/art/stage1-hd.json`) is superimposed on the title flame, below is the MARCHWIND64 title logo of the project (`web/public/brand/title-en.webp`), the icon is the M64 logo (`m64-icon.png`), the same set for each language; if the title image or brand image changes, rerun it on this machine `steam_art.py --output tools/release/linux/steam-art` Submit again.

## Verify records

**2026-10-06 Remote Linux machine (Debian 12, no graphics card): Debug interface and MCP. ** The package is built using the above container, and the game is run via Xvfb plus lavapipe in a Ubuntu 22.04 plus Mesa 23.2.1 container. Just rely on the switch in "Options → About" (without adding `--debug`) to start monitoring, and the startup prompt is normal. On Mac, `attach.py` reads the remote `debug.json`, `ssh -L` forwards the local port, MCP's `srw64_attach` (without parameters), `srw64_status`, `srw64_screenshot` (retrieved through `file.read` 1280×800 screen), `srw64_events`, `srw64_quit` are all normal, and the remote `debug.json` is deleted after exiting. If the same package is run directly on the Debian 12 host, it will segfault in lavapipe of Mesa 22.3.6 (the debugging interface has been opened and has nothing to do with this change).

**2026-09-25 Container smoke test. **Test method:

- Ubuntu 22.04 x64 container, running on Apple Silicon via Rosetta;
- Xvfb is used for display, and Vulkan uses Mesa's software to implement lavapipe (llvmpipe, Vulkan 1.3);
- After the package is unzipped, it is started via `marchwind64.sh`.

Result:

- The program loads the package library;
- First import of ROM: 51174 texts, 16 avatars;
- `SRW64_GRAPHICS_API 1` (Vulkan);
- The opening ran continuously for more than 5 minutes at 60 VI/s, rendering to the BANPRESTO logo and copyright page without crashing;
- At the end, the window thread handles the exit event normally, indicating that the interface is not stuck waiting for the GPU completion notification.

There are three points **not confirmed** this time:

- Did not enter the title and native page: the software rendering is too slow, and it is not confirmed whether the keys synthesized by xdotool are delivered to the game.
- Controller bridging has not been tested.
- The screen has diagonal dotted seams. It appears on the software raster of lavapipe plus MSAA. Whether it appears on the real GPU depends on the Deck.

The above three points must be confirmed on the actual Steam Deck.

## Differences from macOS

| Project | Current status of Linux | At what stage will it be supplemented |
| --- | --- | --- |
| HD layer | Same as macOS (plume); HD material package must be downloaded separately or packaged with `--hd` | Completed |
| Debugging interface screenshot | Available: plume Vulkan added texture → buffer copy, swap chain image can be used as copy source | Completed |
| GPU completion notification | `RenderHookPresented` (`prepare_rt64.py` patch) is called after the RT64 rendering queue's fence wait, instead of Metal's completion handler | Completed |
| Menu bar | None; the settings window is opened with Ctrl+, (`frontend.cpp:1537`). Deck cannot be opened temporarily when using only a controller. You can map a back key to Ctrl+, |
| ROM selection | `marchwind64.sh` Search by fixed position | X2 follow-up: changed to RmlUi selection page |