import io
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

from scripts import mv_image


class MoveImageTests(unittest.TestCase):
    def test_moves_supported_images_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            downloads = root / "Downloads"
            dest = root / "dest"
            downloads.mkdir()
            (downloads / "1.jpg").write_text("image", encoding="utf-8")
            (downloads / "notes.txt").write_text("not an image", encoding="utf-8")

            stdout = io.StringIO()
            with (
                patch.object(mv_image, "DOWNLOADS", downloads),
                patch.object(sys, "argv", ["mv_image.py", str(dest)]),
                redirect_stdout(stdout),
            ):
                self.assertEqual(mv_image.main(), 0)

            self.assertEqual((dest / "1.jpg").read_text(encoding="utf-8"), "image")
            self.assertFalse((downloads / "1.jpg").exists())
            self.assertTrue((downloads / "notes.txt").exists())
            self.assertIn("Moved 1 file(s):", stdout.getvalue())

    def test_refuses_collisions_without_partial_moves(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            downloads = root / "Downloads"
            dest = root / "dest"
            downloads.mkdir()
            dest.mkdir()
            (downloads / "1.jpg").write_text("new image", encoding="utf-8")
            (downloads / "2.png").write_text("second image", encoding="utf-8")
            (dest / "1.jpg").write_text("existing image", encoding="utf-8")

            stderr = io.StringIO()
            with (
                patch.object(mv_image, "DOWNLOADS", downloads),
                patch.object(sys, "argv", ["mv_image.py", str(dest)]),
                redirect_stderr(stderr),
            ):
                self.assertEqual(mv_image.main(), 1)

            self.assertEqual((dest / "1.jpg").read_text(encoding="utf-8"), "existing image")
            self.assertFalse((dest / "2.png").exists())
            self.assertEqual((downloads / "1.jpg").read_text(encoding="utf-8"), "new image")
            self.assertEqual((downloads / "2.png").read_text(encoding="utf-8"), "second image")
            self.assertIn("Refusing to overwrite", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
