#!/usr/bin/env python3
"""Regression tests: Notion sync must not rewrite $vars inside fenced code."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import notion_sync as ns  # noqa: E402


class FenceProtectionTests(unittest.TestCase):
    def test_shell_positional_params_untouched(self) -> None:
        src = (
            "See math $a+b$ outside.\n\n"
            "```sh\n"
            'echo "This command which named $0 has called $# params just now"\n'
            'echo "\\$1 is $1"\n'
            "```\n"
        )
        out = ns.convert_inline_math(src)
        # Prose math is converted; fenced shell stays literal.
        self.assertIn("$`a+b`$", out)
        self.assertIn(
            'echo "This command which named $0 has called $# params just now"',
            out,
        )
        self.assertIn('echo "\\$1 is $1"', out)
        self.assertNotIn("$`0 has called`", out)

    def test_nginx_and_cmake_vars_untouched(self) -> None:
        src = (
            "```nginx\n"
            "try_files $uri $uri/ =404;\n"
            "```\n\n"
            "```cmake\n"
            "target_link_libraries(${PROJECT_NAME} PRIVATE ${PROJECT_NAME}_lib)\n"
            "```\n"
        )
        out = ns.convert_inline_math(src)
        self.assertIn("try_files $uri $uri/ =404;", out)
        self.assertIn(
            "target_link_libraries(${PROJECT_NAME} PRIVATE ${PROJECT_NAME}_lib)",
            out,
        )

    def test_git_mergetool_cmd_untouched(self) -> None:
        src = (
            "```bash\n"
            "git config --global mergetool.vscode.cmd "
            "'code --wait --merge $REMOTE $LOCAL $BASE $MERGED'\n"
            "```\n"
        )
        out = ns.convert_inline_math(src)
        self.assertIn("$REMOTE $LOCAL $BASE $MERGED", out)
        self.assertNotIn("$`REMOTE`", out)

    def test_images_inside_fence_untouched(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp)
            ns.DOCS_ROOT = docs
            note = docs / "note.md"
            note.write_text("x", encoding="utf-8")
            src = "```markdown\n![alt](assets/x.png)\n```\n\n![real](https://ex/a.png)\n"
            out = ns.convert_images(src, note, "https://wiki.example")
            self.assertIn("![alt](assets/x.png)", out)
            self.assertIn("![real](https://ex/a.png)", out)


if __name__ == "__main__":
    unittest.main()
