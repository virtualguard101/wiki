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

    candidates = [
        path
        for path in sorted(DOWNLOADS.iterdir())
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    ]

    if not candidates:
        print("No image files (.jpg, .png, .webp) in ~/Downloads")
        return 0

    collisions = [dest / path.name for path in candidates if (dest / path.name).exists()]
    if collisions:
        print("Refusing to overwrite existing file(s):", file=sys.stderr)
        for path in collisions:
            print(f"  {path}", file=sys.stderr)
        return 1

    moved: list[Path] = []
    for path in candidates:
        shutil.move(path, dest / path.name)
        moved.append(path)

    print(f"Moved {len(moved)} file(s):")
    for path in moved:
        print(f"  {path.name} -> {dest}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
