> **Language / Ngôn ngữ:** [English](plume-pixel-compositor.en.md) · [Tiếng Việt](plume-pixel-compositor.vi.md) · [中文](plume-pixel-compositor.md)

# Universal Plume Pixel Compositing (P2b)

2026-09-20. Continued from [CPU/GPU backend split](shared-game-ui.md). Pixel upload and GPU compositor are now the default dialogue paths, working with [Chinese, Japanese and English cross-platform text](portable-text.md).
The three-platform surface migration of the full game is still not complete.

## Responsibility boundaries

`src/native/presentation/pixel_compositor.*` only uses the Plume public interface; input is
The own pixels of `Bgra8Surface`, the output is the drawing command recorded to the caller's command list.
It does not create windows, submit to queues, wait for the GPU, or read language directories, ROMs, or game state.
`cmake/PixelCompositor.cmake` is shared by the game and independent tests; the same pair of HLSL are compiled separately as
SPIR-V, DXIL and Metal. Simple whole-pixel compositing uses SM6.0, not requiring SM6.3 for no reason; Windows Server 2022
Validation of software drivers has proven that later versions can cause pipeline creation to fail. The generation tool is only used for building and does not put into the player startup chain.

Pixel conventions remain the same: tight top-down BGRA8, premultiplied alpha, targeting single-sample BGRA8/RGBA8 UNORM.
Uploads are copied with 256-byte line alignment; shaders read at integer fragment coordinates without added filtering, scaling or
sRGB conversion. Color mixing uses ONE / ONE_MINUS_SRC_ALPHA and cannot multiply the source alpha again.
Images of unknown formats, HDR, inconsistent dimensions, empty images, and other compositors will be rejected.

Each upload creates independent textures, staging buffers and descriptors, and textures still in use by the GPU cannot be updated.
The `Retention` returned by `Image` and `draw()` keeps these resources and their pipeline/layout/shader alive.
The caller must be retained until the corresponding GPU completes; separate recording uploads without drawing must also retain the Image.
Images are only used in the same ordered graphics queue, and the command list that relies on uploading must be submitted first; if the uploading list is abandoned,
The corresponding image must be discarded and cannot be used as a usable cache. The RenderDevice must be destroyed later than any in-transit resources.

Starting from 2026-10-02, there is a permanent canvas: `canvas(w, h)` creates a texture that retains content across frames, `update()` creates a
`Bgra8Surface` (x, y) uploaded to the canvas, recorded on the same ordered queue, ranked after the previous drawing of it; returned
Staging is also kept until the GPU is complete. `draw()` can be used with scissor to only draw the part actually covered by the image. Canvas content is being uploaded
The override was previously undefined.

## Game wiring

`src/host/dialogue_plume.cpp` is the thin adaptation layer of the host, shared by Metal and Vulkan: Find matching workload
Immutable dialogue frame, use `IncrementalRaster` to only redraw the changed rectangle and upload it to the resident canvas of the window size, and use `srw64_after_gpu` to retain the resource reference to the GPU to complete
(Metal uses the command buffer's completion handler, and other backends use RT64 to render the queue fence after waiting.
`RenderHookPresented`). The shader format is taken from the capabilities of `RenderInterface`. Targets are still queried only on Metal
The format of attachment; fixed B8G8R8A8 swap chain targeting RT64 on Vulkan (2026-09-25, [Linux Build](../guide/linux-build.md)).

The game compiles directly with the Plume dialogue adapter; the old dialogue Metal synth and backend selector switches have been removed.
The CPU scene uses FreeType/HarfBuzz/ICU, retaining the original reader, paging, review and language snapshot.

In an environment where you already have local ROM/full development dependencies, experiment with standalone builds and user directories:

```sh
make host
cmake -S src/host -B build/recomp/gfx-plume-build \
  -DSRW64_ENABLE_RT64=ON \
  -DPython3_EXECUTABLE="$PWD/.venv/bin/python"
cmake --build build/recomp/gfx-plume-build --target srw64-gfx-host --parallel 6
./build/recomp/gfx-plume-build/srw64-gfx-host --play \
  --rom "$PWD/rom.z64" --user-dir "$PWD/build/recomp/plume-play" --new-game
```

Do not overwrite the player data directory with the new game trial directory. The above game process needs to be verified on the actual machine and cannot be inferred from the component CI.

## Independent verification

`tests/pixel_compositor/` does not link to SDL, game code, or CoreText; uses synthesized asymmetric pixmaps,
Compare the actual GPU draw, fence completion, and readback results to the CPU premultiplied blending formula. Covers 1×1, 3×5,
65×17, 321×241, 800×600, 1100×760, BGRA/RGBA target switching, two-layer blending and transparent/translucent/opaque
Pixels, and full upload plus offset local update of resident canvas, 60 readbacks in total; allows for rounding error of 1 quantization unit per channel.

The test also releases the compositor and cache before submitting, leaving only the completion reference; drawing the old image, new image, and
Using the old image again, check for early resource release, content being overwritten, and post-completion reference leaks. Checking for invalid parameters continues.

Fixed Plume's texture-to-buffer readback direction having independent gap: Metal/Vulkan not implemented; D3D12 unconditional
Set sample positions per target texture, dereferencing a null pointer to the buffer target. So the readbacks for the test are respectively using
Metal blit, vkCmdCopyImageToBuffer and D3D12 CopyTextureRegion; Vulkan also has host barrier,
allocation invalidation after fence. These are in the test adaptation layer and do not modify or replace the public upload/draw under test.
They do not mean that the production screenshot backend has been migrated.

`SRW64_PIXEL_TEST_WARP` for Windows Only for standalone testing: verification fixed Plume source code summary, in
The build directory generates a copy that allows software adapter enumeration, enhanced failure diagnostics, and does not change dependencies on checkout or game backends.
WARP and Linux Mesa software Vulkan results are evidence of actual API/driver execution, not physical GPU performance or
Vendor driver coverage. The CI virtual driver for macOS 14 is missing the argument encoder call used by Plume; macOS 15
This test can be performed. This batch uses macOS 15 GPU CI, which does not infer that all physical macOS 14 machines are not supported.

```sh
cmake -S tests/pixel_compositor -B build/pixel-gpu \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DSRW64_RT64_HEADERS="$PWD/build/recomp/upstream/RT64"
cmake --build build/pixel-gpu --config RelWithDebInfo --parallel 2
ctest --test-dir build/pixel-gpu -C RelWithDebInfo --output-on-failure --verbose
```

GitHub Actions is closed and GPU tests can be executed locally with the command above. Synthetic readback does not replace the GPU for real games
workload/window scaling/language switching/exit regression. Currently, window surface, screenshot readback, and
Marker, OS input method and cold start acceptance of games on three platforms. Vulkan physical device verification must also cover non-coherent
Upload memory: Fixed Plume's map/unmap has not explicitly executed flush/invalidate, and the software driver cannot replace it.
Revision and verification of this memory visibility contract. No games, ROMs or font add-ons released.