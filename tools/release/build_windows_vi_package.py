#!/usr/bin/env python3
"""Build and package Marchwind64 Windows distribution with Vietnamese support.

Combines the Windows binary release with the compiled Vietnamese locale content,
applies the font check patch to Marchwind64.exe, and configures Marchwind64.cmd.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import zipfile

ROOT = Path(__file__).resolve().parents[2]


def patch_exe_for_vietnamese(exe_path: Path) -> bool:
    """Patch Marchwind64.exe to allow 'vi' in font checks.

    1. File offset 0x6c0591: Bypasses the 2-character locale throw so 'vi' is accepted.
    2. File offset 0x6bf648: Includes HarmonyOS Condensed font for 'vi' as well as 'en'.
    """
    with open(exe_path, "r+b") as f:
        # Check 1: game_font_sources check
        f.seek(0x6C0591)
        cur1 = f.read(2)
        if cur1 == b"\xeb\x10":
            already_patched_1 = True
        elif cur1 == b"\x66\x81":
            already_patched_1 = False
        else:
            raise ValueError(f"Unexpected bytes at 0x6c0591 in {exe_path}: {cur1.hex()}")

        # Check 2: packaged condensed font check
        f.seek(0x6BF648)
        cur2 = f.read(6)
        if cur2 == bytes.fromhex("664181386a61"):
            already_patched_2 = True
        elif cur2 == bytes.fromhex("66418138656e"):
            already_patched_2 = False
        else:
            raise ValueError(f"Unexpected bytes at 0x6bf648 in {exe_path}: {cur2.hex()}")

        if already_patched_1 and already_patched_2:
            return False

        # Apply Patch 1: jmp +0x10, 16x nop
        if not already_patched_1:
            f.seek(0x6C0591)
            f.write(bytes.fromhex("eb10" + "90" * 16))

        # Apply Patch 2: cmp word ptr [r8], 0x616a (ja); jne +0x55e
        if not already_patched_2:
            f.seek(0x6BF648)
            f.write(bytes.fromhex("664181386a610f855e050000"))

        return True


def build_package(rom_path: Path, dist_dir: Path, output_zip: Path | None = None) -> None:
    os.environ["PYTHONUTF8"] = "1"
    import sys
    sys.path.insert(0, str(ROOT / "src"))
    sys.path.insert(0, str(ROOT / "tools"))

    from srw64_native.profile import load_profile, prepare_profile
    from release.export_content import export_content

    # 1. Compile profile
    profile_cfg = ROOT / "config/recomp/profiles/play-profile.json"
    profile = load_profile(profile_cfg, locale="vi", images="original")

    prepared_dir = ROOT / "build/prepared_vi"
    if prepared_dir.exists():
        shutil.rmtree(prepared_dir)

    print("Compiling Vietnamese presentation profile...")
    prepare_profile(ROOT, profile, rom_path, prepared_dir)

    # 2. Export content directory
    content_dir = dist_dir / "content"
    if content_dir.exists():
        shutil.rmtree(content_dir)

    print("Exporting standalone content to dist/content...")
    export_content(prepared_dir, content_dir)

    # 3. Copy Vietnamese dialogue source files
    vi_dialogue_src = ROOT / "content/dialogue/vi"
    vi_dialogue_dest = dist_dir / "dialogue/vi"
    if vi_dialogue_src.exists():
        if vi_dialogue_dest.exists():
            shutil.rmtree(vi_dialogue_dest)
        shutil.copytree(vi_dialogue_src, vi_dialogue_dest)

    # 4. Patch executable
    exe_path = dist_dir / "Marchwind64.exe"
    if exe_path.exists():
        patched = patch_exe_for_vietnamese(exe_path)
        if patched:
            print(f"Patched {exe_path.name} to support Vietnamese fonts.")
        else:
            print(f"{exe_path.name} was already patched.")

    # 5. Copy launcher script
    cmd_template = ROOT / "tools/release/windows/Marchwind64.cmd"
    if cmd_template.exists():
        shutil.copyfile(cmd_template, dist_dir / "Marchwind64.cmd")
        print("Updated Marchwind64.cmd.")

    # 6. Optional zip packaging
    if output_zip:
        print(f"Creating archive {output_zip}...")
        with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zf:
            for root, _, files in os.walk(dist_dir):
                for f in files:
                    # Skip ROM or temporary files in zip release
                    if f == "rom.z64" or f.endswith(".bak") or f.endswith(".orig"):
                        continue
                    p = Path(root) / f
                    arcname = p.relative_to(dist_dir)
                    zf.write(p, arcname)
        print(f"Archive written: {output_zip}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rom", type=Path, default=ROOT / "rom.z64", help="Path to Super Robot Taisen 64 ROM (Japan, Rev 0)")
    parser.add_argument("--dist", type=Path, default=ROOT / "dist/Marchwind64-windows-x64", help="Windows distribution directory")
    parser.add_argument("--zip", type=Path, default=None, help="Optional output zip file path")
    args = parser.parse_args()

    if not args.rom.exists():
        parser.error(f"ROM not found at {args.rom}")
    if not args.dist.exists():
        parser.error(f"Distribution directory not found at {args.dist}")

    build_package(args.rom.resolve(), args.dist.resolve(), args.zip.resolve() if args.zip else None)
    print("Done! You can now launch Marchwind64 in Vietnamese.")


if __name__ == "__main__":
    main()

