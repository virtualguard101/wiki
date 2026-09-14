from pathlib import Path

from mkdocs.config.defaults import MkDocsConfig


def on_post_build(config: MkDocsConfig, **kwargs) -> None:
    """Copy repo-root CNAME into the built site so gh-deploy keeps the custom domain."""
    src = Path(config.config_file_path).resolve().parent / "CNAME"
    if not src.is_file():
        return
    dst = Path(config.site_dir) / "CNAME"
    dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
