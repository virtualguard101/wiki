"""Normalize relative media URLs in raw HTML for MkDocs.

MkDocs rewrites relative links inside Markdown elements (``img``, ``a``)
against the generated page URL. Raw HTML such as
``<video><source src="assets/demo.mp4"></video>`` is passed through
untouched, so a note written for Obsidian, where ``assets/...`` is relative
to the Markdown file, resolves one directory too deep on the built site: the
page URL (``.../note/tools/调试器/``) has an extra path segment compared with
the source file (``.../note/tools/调试器.md``).

Rewrite ``src``/``poster`` on ``video``/``audio``/``source`` tags so they stay
relative to the source file, matching how MkDocs handles images.
"""

import logging
import posixpath
import re
from urllib.parse import unquote, urlsplit, urlunsplit

from mkdocs.utils import get_relative_url

log = logging.getLogger("mkdocs.plugins")

MEDIA_TAG = re.compile(
    r"<(?:video|audio|source)\b(?:\"[^\"]*\"|'[^']*'|[^>\"'])*>",
    re.IGNORECASE,
)
MEDIA_ATTR = re.compile(
    r"\b(src|poster)\s*=\s*([\"'])(.*?)\2",
    re.IGNORECASE | re.DOTALL,
)


def _is_external(url: str) -> bool:
    return (
        not url
        or url.startswith("/")
        or url.startswith("#")
        or url.startswith("//")
        or url.startswith("data:")
        or url.startswith("mailto:")
        or "://" in url
    )


def _rewrite_media_tag(tag: str, page, files) -> str:
    src_dir = posixpath.dirname(page.file.src_uri)
    page_url = page.url or ""

    def replace(match: re.Match) -> str:
        attr, quote, url = match.groups()
        if _is_external(url):
            return match.group(0)
        parts = urlsplit(url)
        if not parts.path:
            return match.group(0)
        target_uri = posixpath.normpath(
            posixpath.join(src_dir, unquote(parts.path))
        )
        # Resolve through MkDocs' file collection so plugin-specific URL
        # mappings are honored (e.g. the blog plugin publishes files under
        # ``blog/posts/`` as ``blog/assets/``).
        target_file = files.get_file_from_path(target_uri) if files else None
        target_url = target_file.url if target_file is not None else target_uri
        new_path = get_relative_url(target_url, page_url)
        new_url = urlunsplit(("", "", new_path, parts.query, parts.fragment))
        return f"{attr}={quote}{new_url}{quote}"

    return MEDIA_ATTR.sub(replace, tag)


def on_page_content(html: str, page, config, files=None, **kwargs) -> str:
    if "<video" not in html and "<audio" not in html:
        return html
    return MEDIA_TAG.sub(
        lambda match: _rewrite_media_tag(match.group(0), page, files),
        html,
    )
