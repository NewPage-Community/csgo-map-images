#!/usr/bin/env python3
"""Sync map images from KZGlobalTeam/cs2kz-images into this repo's flat images/."""

import filecmp
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

UPSTREAM = "https://github.com/KZGlobalTeam/cs2kz-images.git"
MIN_WIDTH = 1920
MIN_HEIGHT = 1080

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
DEST_DIR = REPO_ROOT / "images"

COURSE_RE = re.compile(r"^(\d+)\.(jpe?g)$", re.IGNORECASE)


def course_sort_key(path: Path):
    m = COURSE_RE.match(path.name)
    if m:
        return (0, int(m.group(1)), path.name.lower())
    return (1, path.name.lower())


def pick_first_course(map_dir: Path) -> Path | None:
    candidates = [
        p for p in map_dir.iterdir()
        if p.is_file() and p.suffix.lower() in {".jpg", ".jpeg"}
    ]
    if not candidates:
        return None
    return sorted(candidates, key=course_sort_key)[0]


def clone_upstream(tmp: Path) -> Path:
    repo = tmp / "cs2kz-images"
    # Sparse clone: only images/ (shallow)
    subprocess.run(
        ["git", "clone", "--depth", "1", "--filter=blob:none", "--sparse", UPSTREAM, str(repo)],
        check=True,
    )
    subprocess.run(
        ["git", "sparse-checkout", "set", "--cone", "images"],
        cwd=repo,
        check=True,
    )
    return repo / "images"


def sync():
    if not DEST_DIR.is_dir():
        print(f"Missing destination directory: {DEST_DIR}", file=sys.stderr)
        sys.exit(1)

    added = updated = skipped = 0
    missing_source = []
    below_1080 = []

    with tempfile.TemporaryDirectory(prefix="cs2kz-images-sync-") as tmp:
        print(f"Cloning upstream into {tmp} ...")
        src_images = clone_upstream(Path(tmp))
        if not src_images.is_dir():
            print(f"Upstream images/ not found at {src_images}", file=sys.stderr)
            sys.exit(1)

        map_dirs = sorted(p for p in src_images.iterdir() if p.is_dir())
        print(f"Found {len(map_dirs)} map folders upstream\n")

        for map_dir in map_dirs:
            map_name = map_dir.name
            src = pick_first_course(map_dir)
            if src is None:
                missing_source.append(map_name)
                continue

            dest = DEST_DIR / f"{map_name}.jpg"
            if dest.is_file() and filecmp.cmp(src, dest, shallow=False):
                skipped += 1
            elif dest.is_file():
                shutil.copy2(src, dest)
                updated += 1
                print(f"updated  {map_name}  (from {src.name})")
            else:
                shutil.copy2(src, dest)
                added += 1
                print(f"added    {map_name}  (from {src.name})")

            try:
                with Image.open(dest) as im:
                    w, h = im.size
            except OSError as e:
                below_1080.append((map_name, f"unreadable: {e}"))
                continue
            if w < MIN_WIDTH or h < MIN_HEIGHT:
                below_1080.append((map_name, f"{w}x{h}"))

    print("\n--- summary ---")
    print(f"added:   {added}")
    print(f"updated: {updated}")
    print(f"skipped: {skipped}  (identical)")
    if missing_source:
        print(f"\nno jpg in upstream folder ({len(missing_source)}):")
        for name in missing_source:
            print(f"  {name}")
    if below_1080:
        print(f"\nbelow {MIN_WIDTH}x{MIN_HEIGHT} ({len(below_1080)}):")
        for name, res in below_1080:
            print(f"  {name}: {res}")
    else:
        print(f"\nall synced images meet {MIN_WIDTH}x{MIN_HEIGHT}")


if __name__ == "__main__":
    sync()
