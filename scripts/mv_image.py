#!/usr/bin/env python3
import shutil
import sys
from pathlib import Path

IMAGE_EXTENSIONS = {".jpg", ".png", ".webp"}
DOWNLOADS = Path.home() / "Downloads"


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <destination-dir>", file=sys.stderr)
        return 1

    dest = Path(sys.argv[1])
    dest.mkdir(parents=True, exist_ok=True)

    if not DOWNLOADS.is_dir():
        print("No image files (.jpg, .png, .webp) in ~/Downloads")
        return 0

    moved: list[Path] = []
    for path in sorted(DOWNLOADS.iterdir()):
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS:
            shutil.move(path, dest / path.name)
            moved.append(path)

    if not moved:
        print("No image files (.jpg, .png, .webp) in ~/Downloads")
        return 0

    print(f"Moved {len(moved)} file(s):")
    for path in moved:
        print(f"  {path.name} -> {dest}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
