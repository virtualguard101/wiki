import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import mv_image


class MoveImageTests(unittest.TestCase):
    def test_refuses_to_overwrite_existing_destination_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            downloads = root / "Downloads"
            dest = root / "assets"
            downloads.mkdir()
            dest.mkdir()

            source = downloads / "1.jpg"
            existing = dest / "1.jpg"
            source.write_text("new image")
            existing.write_text("old image")

            with (
                patch.object(mv_image, "DOWNLOADS", downloads),
                patch("sys.argv", ["mv_image.py", str(dest)]),
                patch("sys.stderr"),
            ):
                result = mv_image.main()

            self.assertEqual(result, 1)
            self.assertEqual(existing.read_text(), "old image")
            self.assertEqual(source.read_text(), "new image")

    def test_moves_supported_images_when_no_destination_collisions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            downloads = root / "Downloads"
            dest = root / "assets"
            downloads.mkdir()

            source = downloads / "diagram.png"
            ignored = downloads / "notes.txt"
            source.write_text("image")
            ignored.write_text("not an image")

            with (
                patch.object(mv_image, "DOWNLOADS", downloads),
                patch("sys.argv", ["mv_image.py", str(dest)]),
                patch("sys.stdout"),
            ):
                result = mv_image.main()

            self.assertEqual(result, 0)
            self.assertFalse(source.exists())
            self.assertEqual((dest / "diagram.png").read_text(), "image")
            self.assertEqual(ignored.read_text(), "not an image")


if __name__ == "__main__":
    unittest.main()
