#!/usr/bin/env python3
"""Sync MkDocs wiki notes to Notion (CI/CD entrypoint).

Combines markdown conversion, page create/update, and local image uploads.
By default only processes files changed since a git base ref (incremental).

Logs go to stdout/stderr only — no log files are written into the repo.
"""

from __future__ import annotations

import argparse
import json
import logging
import mimetypes
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple
from urllib.parse import quote

from ruamel.yaml import YAML

# ---------------------------------------------------------------------------
# Paths & defaults
# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parents[1]
DOCS_ROOT = ROOT / "docs"
NAV_PATH = DOCS_ROOT / ".nav.yml"
DEFAULT_SITE_URL = "https://wiki.virtualguard101.com"
DEFAULT_STATE = Path(
    os.environ.get("NOTION_STATE_PATH", str(ROOT / ".notion_sync_state.json"))
)
DEFAULT_WIKI_DATA_SOURCE = os.environ.get(
    "NOTION_WIKI_DATA_SOURCE", "3aba3d42-6eec-80e9-8a37-000be17e3045"
)
DEFAULT_WIKI_DATABASE = os.environ.get(
    "NOTION_WIKI_DATABASE", "3aba3d42-6eec-816b-8e88-ed2956be408f"
)
DEFAULT_TITLE_PROP = os.environ.get("NOTION_TITLE_PROPERTY", "页面")

NOTION_VERSION_PAGES = "2025-09-03"
NOTION_VERSION_MARKDOWN = "2026-03-11"

ADMONITION_STYLES: Dict[str, Tuple[str, str]] = {
    "note": ("blue_bg", "✒️️"),
    "abstract": ("gray_bg", "📋"),
    "info": ("blue_bg", "ℹ️"),
    "tip": ("yellow_bg", "💡"),
    "success": ("green_bg", "✅"),
    "question": ("purple_bg", "❓"),
    "warning": ("orange_bg", "⚠️"),
    "failure": ("red_bg", "❌"),
    "danger": ("red_bg", "⛔"),
    "bug": ("red_bg", "🐛"),
    "example": ("gray_bg", "🧪"),
    "quote": ("gray_bg", "💬"),
    "important": ("orange_bg", "⚠️"),
    # Custom: docs/assets/stylesheets/admonitions.css (.review)
    "review": ("green_bg", "🔍"),
}

CONTENT_TYPES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".webp": "image/webp",
    ".awebp": "image/webp",
    ".svg": "image/svg+xml",
    ".bmp": "image/bmp",
    ".tif": "image/tiff",
    ".tiff": "image/tiff",
}

ASSET_SUFFIXES = set(CONTENT_TYPES) | {".pdf", ".mp4", ".webm", ".svg"}

log = logging.getLogger("notion_sync")


def _load_dotenv(path: Path) -> None:
    """Load KEY=VALUE lines into os.environ without overriding existing vars."""
    if not path.is_file():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip("'").strip('"')
        if key and key not in os.environ:
            os.environ[key] = value


def _token_from_cursor_mcp() -> Optional[str]:
    """Reuse Notion token already configured for Cursor MCP (local dev)."""
    mcp_path = Path.home() / ".cursor" / "mcp.json"
    if not mcp_path.is_file():
        return None
    try:
        data = json.loads(mcp_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    servers = data.get("mcpServers") or {}
    for name in ("notionApi", "Notion", "notion"):
        env = (servers.get(name) or {}).get("env") or {}
        for key in ("NOTION_TOKEN", "NOTION_API_KEY"):
            val = env.get(key)
            if val:
                return str(val).strip()
    for cfg in servers.values():
        env = (cfg or {}).get("env") or {}
        for key in ("NOTION_TOKEN", "NOTION_API_KEY"):
            val = env.get(key)
            if val:
                return str(val).strip()
    return None


def resolve_token(explicit: Optional[str] = None) -> Optional[str]:
    """Resolve Notion token without requiring --token every run.

    Order: CLI → env → wiki `.env` / `.notion_token` → ~/.config/notion/token
    → Cursor `~/.cursor/mcp.json`.
    """
    if explicit and explicit.strip():
        return explicit.strip()

    _load_dotenv(ROOT / ".env")
    for key in ("NOTION_TOKEN", "NOTION_API_KEY"):
        val = os.environ.get(key)
        if val and val.strip():
            return val.strip()

    for path in (
        ROOT / ".notion_token",
        Path.home() / ".config" / "notion" / "token",
    ):
        if path.is_file():
            val = path.read_text(encoding="utf-8").strip()
            if val:
                return val

    return _token_from_cursor_mcp()


def setup_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(level)
    # Keep urllib noise down unless debugging.
    logging.getLogger("urllib3").setLevel(logging.WARNING)


# ---------------------------------------------------------------------------
# Nav / markdown conversion
# ---------------------------------------------------------------------------


@dataclass
class NavItem:
    key: str
    title: str
    file_rel: Optional[str]
    parent_key: str
    children: List["NavItem"] = field(default_factory=list)


@dataclass
class MigrationState:
    root_page_id: str = ""
    data_source_id: str = ""
    title_property: str = DEFAULT_TITLE_PROP
    pages: Dict[str, Dict[str, str]] = field(default_factory=dict)


def docs_rel(path: str) -> str:
    return path.replace("\\", "/")


def load_nav() -> List[Any]:
    yaml = YAML()
    with NAV_PATH.open("r", encoding="utf-8") as f:
        data = yaml.load(f)
    return data.get("nav", data)


def title_from_path(path: Path) -> str:
    return path.stem


def resolve_doc_path(raw: str) -> str:
    raw = raw.strip().strip('"').strip("'")
    if raw.startswith("docs/"):
        raw = raw[5:]
    return docs_rel(raw)


def build_nav_tree(nodes: List[Any], parent_key: str = "") -> List[NavItem]:
    items: List[NavItem] = []
    for node in nodes:
        if isinstance(node, str):
            rel = resolve_doc_path(node)
            items.append(
                NavItem(
                    key=rel,
                    title=title_from_path(Path(rel)),
                    file_rel=rel,
                    parent_key=parent_key,
                )
            )
            continue
        if not isinstance(node, dict):
            continue
        for title, child in node.items():
            title_s = str(title)
            if isinstance(child, str):
                rel = resolve_doc_path(child)
                items.append(
                    NavItem(
                        key=rel,
                        title=title_s,
                        file_rel=rel,
                        parent_key=parent_key,
                    )
                )
            elif isinstance(child, list):
                section_key = f"{parent_key}/{title_s}" if parent_key else title_s
                section = NavItem(
                    key=section_key,
                    title=title_s,
                    file_rel=None,
                    parent_key=parent_key,
                    children=build_nav_tree(child, section_key),
                )
                items.append(section)
    return items


def walk_nav(items: List[NavItem]) -> List[NavItem]:
    ordered: List[NavItem] = []
    for item in items:
        ordered.append(item)
        ordered.extend(walk_nav(item.children))
    return ordered


def index_nav(tree: List[NavItem]) -> Dict[str, NavItem]:
    return {item.key: item for item in walk_nav(tree)}


def parse_frontmatter(text: str) -> Tuple[Dict[str, Any], str]:
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    raw = text[3:end].strip()
    body = text[end + 4 :].lstrip("\n")
    meta: Dict[str, Any] = {}
    for line in raw.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
        meta[key] = value
    return meta, body


def strip_duplicate_h1(title: str, body: str) -> str:
    lines = body.splitlines()
    if not lines:
        return body
    first = lines[0].strip()
    if first.startswith("# "):
        h1 = first[2:].strip()
        if h1 == title or h1 in title or title in h1:
            return "\n".join(lines[1:]).lstrip("\n")
    return body


def collect_indented_block(lines: List[str], start: int, indent: int) -> Tuple[List[str], int]:
    collected: List[str] = []
    i = start
    while i < len(lines):
        line = lines[i]
        if line.strip() == "":
            collected.append("")
            i += 1
            continue
        leading = len(line) - len(line.lstrip(" "))
        # Also accept tabs as indent units (rare in these notes).
        if leading < indent and not line.startswith("\t" * (indent // 4 or 1)):
            # Allow tab-indented content roughly equivalent to spaces.
            if line.startswith("\t"):
                tab_count = len(line) - len(line.lstrip("\t"))
                if tab_count * 4 < indent:
                    break
                collected.append(line[tab_count:])
                i += 1
                continue
            break
        collected.append(line[indent:] if leading >= indent else line.lstrip(" "))
        i += 1
    return collected, i


def notion_indent_block(text: str, tabs: int = 1) -> str:
    """Indent block children for Notion; keep blank lines indented so nesting holds."""
    prefix = "\t" * tabs
    out: List[str] = []
    for line in text.splitlines():
        if line.strip() == "":
            out.append(f"{prefix}<empty-block/>")
        else:
            out.append(prefix + line)
    return "\n".join(out)


_ADMON_LINE_RE = re.compile(
    r"^(?P<indent>[ \t]*)"
    r"(?P<markers>[!?]{3})(?P<expanded>\+?)"
    r"\s*(?P<type>\w+)"
    r"(?P<rest>.*?)\s*$"
)
_ADMON_INLINE_RE = re.compile(r"\binline(?:\s+end)?\b", re.IGNORECASE)
_ADMON_TITLE_RE = re.compile(r'"([^"]*)"')


def _parse_admonition_rest(rest: str) -> Tuple[Optional[str], bool]:
    """Parse optional inline flag + quoted title from the remainder of an admonition header."""
    rest = rest.strip()
    if not rest:
        return None, False
    inline = bool(_ADMON_INLINE_RE.search(rest))
    # Strip inline markers before / after title.
    cleaned = _ADMON_INLINE_RE.sub(" ", rest)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    title_match = _ADMON_TITLE_RE.search(cleaned)
    title = title_match.group(1) if title_match else None
    return title, inline


def convert_admonitions_and_tabs(text: str) -> str:
    lines = text.splitlines()
    out: List[str] = []
    i = 0
    tab_re = re.compile(r'^([ \t]*)===\s+"([^"]+)"\s*$')

    while i < len(lines):
        line = lines[i]
        ad_match = _ADMON_LINE_RE.match(line)
        if ad_match:
            indent_ws = ad_match.group("indent") or ""
            indent = len(indent_ws.replace("\t", "    "))
            markers = ad_match.group("markers")
            ad_type = ad_match.group("type")
            title, _inline = _parse_admonition_rest(ad_match.group("rest") or "")
            # Material body is indented 4 spaces beyond the admonition marker line.
            body_indent = indent + 4
            block_lines, i = collect_indented_block(lines, i + 1, body_indent)
            inner = convert_admonitions_and_tabs("\n".join(block_lines).strip("\n"))
            if markers.startswith("?"):
                summary = title or ad_type.capitalize()
                block = (
                    f"<details>\n<summary>{summary}</summary>\n"
                    f"{notion_indent_block(inner)}\n</details>"
                )
            else:
                color, icon = ADMONITION_STYLES.get(ad_type, ("gray_bg", "📌"))
                # Inline admonitions have no Notion float equivalent → normal callout.
                header = f"**{title}**\n" if title else ""
                block = (
                    f'<callout icon="{icon}" color="{color}">\n'
                    f"{notion_indent_block(header + inner)}\n"
                    "</callout>"
                )
            out.append(block)
            continue

        tab_match = tab_re.match(line)
        if tab_match:
            label = tab_match.group(2)
            indent_ws = tab_match.group(1) or ""
            indent = len(indent_ws.replace("\t", "    "))
            block_lines, i = collect_indented_block(lines, i + 1, indent + 4)
            inner = convert_admonitions_and_tabs("\n".join(block_lines).strip("\n"))
            out.append(f"### {label}")
            out.append(inner)
            continue

        out.append(line)
        i += 1

    return "\n".join(out)


def convert_inline_math(text: str) -> str:
    def repl_block(match: re.Match[str]) -> str:
        return f"$`{match.group(1).strip()}`$"

    text = re.sub(r"\$\$([\s\S]+?)\$\$", lambda m: f"$${m.group(1)}$$", text)
    text = re.sub(r"(?<!\$)\$(?!\$)([^$\n]+?)\$(?!\$)", repl_block, text)
    return text


def convert_html_blocks(text: str) -> str:
    text = re.sub(
        r'<div\s+class="responsive-video-container">\s*'
        r'<iframe[^>]+src="([^"]+)"[^>]*>\s*</iframe>\s*</div>',
        lambda m: f'<video src="{m.group(1)}">Video</video>',
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    return text


def resolve_local_asset_path(raw: str, source_file: Path) -> Optional[Path]:
    raw = raw.strip()
    if not raw or raw.startswith(("http://", "https://")):
        return None
    if raw.startswith("/"):
        candidate = (DOCS_ROOT / raw.lstrip("/")).resolve()
    else:
        candidate = (source_file.parent / raw).resolve()
    try:
        candidate.relative_to(DOCS_ROOT.resolve())
    except ValueError:
        return None
    return candidate if candidate.exists() else None


def resolve_image_url(raw: str, source_file: Path, site_url: str) -> str:
    raw = raw.strip()
    if raw.startswith(("http://", "https://")):
        return raw
    if raw.startswith("/"):
        rel = docs_rel(raw.lstrip("/"))
    else:
        candidate = resolve_local_asset_path(raw, source_file)
        if candidate is not None:
            rel = docs_rel(str(candidate.relative_to(DOCS_ROOT)))
        else:
            rel = docs_rel(str((source_file.parent / raw).resolve().relative_to(DOCS_ROOT)))
    encoded = "/".join(quote(part, safe="") for part in rel.split("/"))
    return f"{site_url.rstrip('/')}/{encoded}"


def resolve_internal_target(raw: str, source_file: Path) -> str:
    target = raw.split("#", 1)[0].strip()
    if not target:
        return ""
    if target.startswith("/"):
        resolved = (DOCS_ROOT / target.lstrip("/")).resolve()
    else:
        resolved = (source_file.parent / target).resolve()
    try:
        rel = docs_rel(str(resolved.relative_to(DOCS_ROOT)))
    except ValueError:
        return target
    if rel.endswith(".ipynb"):
        rel = rel[:-6] + ".md"
    return rel


def convert_images(
    text: str,
    source_file: Path,
    site_url: str,
    upload_local: Optional[Any] = None,
) -> str:
    def repl(match: re.Match[str]) -> str:
        alt = match.group(1) or ""
        src = match.group(2).strip()
        if upload_local is not None and not src.startswith(("http://", "https://")):
            local = resolve_local_asset_path(src, source_file)
            if local is not None:
                uploaded = upload_local(local)
                if uploaded:
                    if str(uploaded).startswith("file-upload://"):
                        return f'<image src="{uploaded}">{alt}</image>'
                    return f"\n\n{uploaded}\n\n"
        url = resolve_image_url(src, source_file, site_url)
        return f"![{alt}]({url})"

    return re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", repl, text)


def convert_links(
    text: str,
    source_file: Path,
    page_map: Dict[str, Dict[str, str]],
) -> str:
    def repl(match: re.Match[str]) -> str:
        label = match.group(1)
        raw = match.group(2)
        if raw.startswith(("http://", "https://")):
            return match.group(0)
        anchor = ""
        if "#" in raw:
            path_part, anchor = raw.split("#", 1)
        else:
            path_part = raw
        if not path_part:
            return match.group(0)
        rel = resolve_internal_target(path_part, source_file)
        if rel in page_map and page_map[rel].get("url"):
            url = page_map[rel]["url"]
            if anchor:
                url = f"{url}#{anchor}"
            return f'<mention-page url="{url}">{label}</mention-page>'
        return f"[{label}]({raw})"

    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", repl, text)


def ipynb_to_markdown(path: Path) -> Tuple[Dict[str, Any], str]:
    """Convert a Jupyter notebook to markdown (cells only; no raw JSON)."""
    data = json.loads(path.read_text(encoding="utf-8"))
    meta: Dict[str, Any] = {}
    nb_meta = data.get("metadata") or {}
    # Prefer explicit title from notebook metadata when present.
    if isinstance(nb_meta.get("title"), str):
        meta["title"] = nb_meta["title"]

    parts: List[str] = []
    for cell in data.get("cells") or []:
        ctype = cell.get("cell_type")
        source = cell.get("source") or []
        if isinstance(source, list):
            text = "".join(source)
        else:
            text = str(source)
        text = text.rstrip("\n")
        if not text.strip():
            continue
        if ctype == "markdown":
            parts.append(text)
        elif ctype == "code":
            lang = ""
            kernelspec = nb_meta.get("kernelspec") or {}
            language = kernelspec.get("language") or ""
            if language:
                lang = str(language)
            else:
                lang = "python"
            parts.append(f"```{lang}\n{text}\n```")
            # Include plain-text / stream outputs when useful.
            outputs = cell.get("outputs") or []
            out_chunks: List[str] = []
            for out in outputs:
                otype = out.get("output_type")
                if otype == "stream":
                    text_out = out.get("text") or ""
                    if isinstance(text_out, list):
                        text_out = "".join(text_out)
                    if str(text_out).strip():
                        out_chunks.append(str(text_out).rstrip())
                elif otype in ("execute_result", "display_data"):
                    data_out = out.get("data") or {}
                    if "text/plain" in data_out:
                        plain = data_out["text/plain"]
                        if isinstance(plain, list):
                            plain = "".join(plain)
                        if str(plain).strip():
                            out_chunks.append(str(plain).rstrip())
                    elif "text/markdown" in data_out:
                        md = data_out["text/markdown"]
                        if isinstance(md, list):
                            md = "".join(md)
                        if str(md).strip():
                            out_chunks.append(str(md).rstrip())
            if out_chunks:
                parts.append("```\n" + "\n".join(out_chunks) + "\n```")
        # skip raw cells
    body = "\n\n".join(parts).strip() + "\n"
    return meta, body


def convert_markdown_file(
    file_path: Path,
    site_url: str,
    page_map: Dict[str, Dict[str, str]],
    upload_local: Optional[Any] = None,
) -> Tuple[str, str, Dict[str, Any]]:
    if file_path.suffix.lower() == ".ipynb":
        meta, body = ipynb_to_markdown(file_path)
        title = (meta.get("title") or title_from_path(file_path)).strip()
    else:
        raw = file_path.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(raw)
        title = (meta.get("title") or title_from_path(file_path)).strip()
        body = strip_duplicate_h1(title, body)

    body = convert_html_blocks(body)
    body = convert_admonitions_and_tabs(body)
    body = convert_inline_math(body)
    body = convert_images(body, file_path, site_url, upload_local=upload_local)
    body = convert_links(body, file_path, page_map)
    body = re.sub(r"\n{3,}", "\n\n", body).strip()
    return title, body, meta


def page_has_local_images(source: Path) -> bool:
    text = source.read_text(encoding="utf-8", errors="ignore")
    for _, src in re.findall(r"!\[([^\]]*)\]\(([^)]+)\)", text):
        raw = src.strip()
        if not raw.startswith(("http://", "https://")):
            return True
    return False


def md_references_asset(source: Path, asset_rel: str) -> bool:
    """Cheap check: whether markdown likely references a docs-relative asset."""
    text = source.read_text(encoding="utf-8", errors="ignore")
    name = Path(asset_rel).name
    if name not in text:
        return False
    for _, src in re.findall(r"!\[([^\]]*)\]\(([^)]+)\)", text):
        local = resolve_local_asset_path(src.strip(), source)
        if local is None:
            continue
        if docs_rel(str(local.relative_to(DOCS_ROOT))) == asset_rel:
            return True
    return False


# ---------------------------------------------------------------------------
# Notion API
# ---------------------------------------------------------------------------


def notion_request(
    token: str,
    method: str,
    path: str,
    payload: Optional[dict] = None,
    notion_version: str = NOTION_VERSION_PAGES,
    retries: int = 6,
) -> dict:
    import http.client
    import ssl

    url = f"https://api.notion.com/v1/{path}"
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    last_error: Optional[Exception] = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                url,
                data=data,
                method=method,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Notion-Version": notion_version,
                    "Content-Type": "application/json",
                },
            )
            with urllib.request.urlopen(req, timeout=180) as resp:
                body = resp.read().decode("utf-8")
                return json.loads(body) if body else {}
        except urllib.error.HTTPError as exc:
            last_error = exc
            err_body = exc.read().decode("utf-8", errors="replace")
            if exc.code in (429, 502, 503, 504):
                wait = 2.0 * (attempt + 1)
                log.warning("HTTP %s; retry in %.1fs", exc.code, wait)
                time.sleep(wait)
                continue
            raise urllib.error.HTTPError(url, exc.code, err_body, exc.headers, None) from exc
        except (
            urllib.error.URLError,
            TimeoutError,
            http.client.IncompleteRead,
            http.client.RemoteDisconnected,
            ssl.SSLError,
            ConnectionResetError,
            BrokenPipeError,
        ) as exc:
            last_error = exc
            wait = 1.5 * (attempt + 1)
            log.warning("transient network error (%s); retry in %.1fs", type(exc).__name__, wait)
            time.sleep(wait)
    assert last_error is not None
    raise last_error


def create_page(
    token: str,
    parent_id: str,
    title: str,
    *,
    title_property: str,
    parent_kind: str,
) -> Dict[str, str]:
    """Create a Notion page under a wiki data source or parent page."""
    if parent_kind == "data_source":
        parent: dict = {"type": "data_source_id", "data_source_id": parent_id}
    elif parent_kind == "database":
        parent = {"type": "database_id", "database_id": parent_id}
    else:
        parent = {"page_id": parent_id}

    # Wiki pages (including nested children) use the data-source title property.
    prop_name = title_property or "title"
    props = {
        prop_name: {
            "title": [{"type": "text", "text": {"content": title[:2000]}}],
        }
    }
    try:
        page = notion_request(token, "POST", "pages", {"parent": parent, "properties": props})
    except urllib.error.HTTPError as exc:
        # Some parent page_id contexts only accept the generic "title" property.
        if prop_name != "title" and "title" in str(exc):
            props = {
                "title": {
                    "title": [{"type": "text", "text": {"content": title[:2000]}}],
                }
            }
            page = notion_request(
                token, "POST", "pages", {"parent": parent, "properties": props}
            )
        else:
            raise
    return {"id": page["id"], "url": page.get("url", "")}


def update_page_markdown(token: str, page_id: str, markdown: str) -> None:
    notion_request(
        token,
        "PATCH",
        f"pages/{page_id}/markdown",
        {
            "type": "replace_content",
            "replace_content": {"new_str": markdown},
        },
        notion_version=NOTION_VERSION_MARKDOWN,
    )


def upload_local_file(token: str, path: Path, cache: Dict[str, str]) -> str:
    key = str(path.resolve())
    if key in cache:
        return cache[key]

    suffix = path.suffix.lower()
    filename = path.name
    if suffix == ".awebp":
        filename = path.stem + ".webp"
        suffix = ".webp"

    content_type = (
        CONTENT_TYPES.get(suffix)
        or mimetypes.guess_type(filename)[0]
        or "application/octet-stream"
    )
    created = notion_request(
        token,
        "POST",
        "file_uploads",
        {"filename": filename, "content_type": content_type},
    )
    upload_id = created["id"]

    boundary = f"----NotionBoundary{int(time.time() * 1000)}"
    file_bytes = path.read_bytes()
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
        f"Content-Type: {content_type}\r\n\r\n"
    ).encode("utf-8") + file_bytes + f"\r\n--{boundary}--\r\n".encode("utf-8")

    url = f"https://api.notion.com/v1/file_uploads/{upload_id}/send"
    req = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Notion-Version": NOTION_VERSION_PAGES,
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        json.loads(resp.read().decode("utf-8"))

    source = f"file-upload://{upload_id}"
    cache[key] = source
    return source


def iter_blocks(token: str, block_id: str):
    cursor: Optional[str] = None
    while True:
        path = f"blocks/{block_id}/children?page_size=100"
        if cursor:
            path += f"&start_cursor={cursor}"
        data = notion_request(token, "GET", path)
        for block in data.get("results", []):
            yield block
            btype = block.get("type")
            if block.get("has_children") and btype not in ("child_page", "child_database"):
                yield from iter_blocks(token, block["id"])
        if not data.get("has_more"):
            break
        cursor = data.get("next_cursor")


def rich_text_plain(block: dict) -> str:
    btype = block.get("type")
    payload = block.get(btype) or {}
    parts = payload.get("rich_text") or []
    return "".join(p.get("plain_text", "") for p in parts)


def delete_block(token: str, block_id: str) -> None:
    notion_request(token, "DELETE", f"blocks/{block_id}")


def insert_image_after(
    token: str,
    parent_id: str,
    after_block_id: str,
    upload_id: str,
    caption: str = "",
) -> None:
    image: dict = {
        "type": "file_upload",
        "file_upload": {"id": upload_id},
    }
    if caption:
        image["caption"] = [{"type": "text", "text": {"content": caption[:2000]}}]
    notion_request(
        token,
        "PATCH",
        f"blocks/{parent_id}/children",
        {
            "after": after_block_id,
            "children": [
                {
                    "object": "block",
                    "type": "image",
                    "image": image,
                }
            ],
        },
    )


def attach_placeholder_images(
    token: str,
    page_id: str,
    image_paths: List[Path],
) -> int:
    upload_cache: Dict[str, str] = {}
    attached = 0
    placeholder_re = re.compile(r"^⟦LOCALIMG:(\d+)⟧$")

    matches: List[Tuple[dict, int]] = []
    for block in iter_blocks(token, page_id):
        if block.get("type") != "paragraph":
            continue
        text = rich_text_plain(block).strip()
        m = placeholder_re.match(text)
        if not m:
            continue
        matches.append((block, int(m.group(1))))

    for block, idx in matches:
        if idx < 0 or idx >= len(image_paths):
            log.warning("placeholder index out of range: %s", idx)
            continue
        path = image_paths[idx]
        source = upload_local_file(token, path, upload_cache)
        upload_id = source.split("://", 1)[1]
        parent = block.get("parent", {})
        parent_id = parent.get("page_id") or parent.get("block_id") or page_id
        insert_image_after(token, parent_id, block["id"], upload_id, caption=path.name)
        delete_block(token, block["id"])
        attached += 1
        time.sleep(0.15)
    return attached


# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------


def load_state(path: Path) -> MigrationState:
    if not path.exists():
        return MigrationState()
    data = json.loads(path.read_text(encoding="utf-8"))
    return MigrationState(
        root_page_id=data.get("root_page_id", ""),
        data_source_id=data.get("data_source_id", ""),
        title_property=data.get("title_property", DEFAULT_TITLE_PROP),
        pages=data.get("pages", {}),
    )


def save_state(path: Path, state: MigrationState) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "root_page_id": state.root_page_id,
                "data_source_id": state.data_source_id,
                "title_property": state.title_property,
                "pages": state.pages,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


def page_title(page: dict) -> str:
    props = page.get("properties", {})
    for key in (DEFAULT_TITLE_PROP, "页面", "title", "Title", "Name", "名称"):
        prop = props.get(key)
        if not prop or prop.get("type") != "title":
            continue
        parts = prop.get("title") or []
        return "".join(t.get("plain_text", "") for t in parts)
    for prop in props.values():
        if prop.get("type") == "title":
            parts = prop.get("title") or []
            return "".join(t.get("plain_text", "") for t in parts)
    return ""


def list_wiki_pages(token: str, data_source_id: str) -> List[dict]:
    pages: List[dict] = []
    cursor: Optional[str] = None
    while True:
        payload: dict = {"page_size": 100}
        if cursor:
            payload["start_cursor"] = cursor
        data = notion_request(token, "POST", f"data_sources/{data_source_id}/query", payload)
        pages.extend(data.get("results", []))
        if not data.get("has_more"):
            break
        cursor = data.get("next_cursor")
    return pages


def rebuild_state_from_wiki(
    token: str,
    data_source_id: str = DEFAULT_WIKI_DATA_SOURCE,
    database_id: str = DEFAULT_WIKI_DATABASE,
    sections: Optional[List[str]] = None,
) -> MigrationState:
    """Match existing Notebook wiki pages to nav keys (one-time / recovery)."""
    state = MigrationState(
        root_page_id=database_id,
        data_source_id=data_source_id,
        title_property=DEFAULT_TITLE_PROP,
    )
    pages = list_wiki_pages(token, data_source_id)
    log.info("fetched %d pages from wiki for state rebuild", len(pages))

    by_parent: Dict[str, List[Dict[str, str]]] = {}
    for page in pages:
        title = page_title(page)
        parent = page.get("parent", {})
        if parent.get("type") == "page_id":
            parent_key = parent["page_id"]
        elif parent.get("type") == "database_id":
            parent_key = parent["database_id"]
        elif parent.get("type") == "data_source_id":
            parent_key = parent["data_source_id"]
        else:
            parent_key = database_id
        by_parent.setdefault(parent_key, []).append(
            {
                "id": page["id"],
                "title": title,
                "url": page.get("url", f"https://www.notion.so/{page['id'].replace('-', '')}"),
            }
        )

    tree = build_nav_tree(load_nav())
    notebook = next((item for item in tree if item.title == "Notebook"), None)
    start_items = notebook.children if notebook else tree
    if notebook:
        state.pages[notebook.key] = {
            "id": database_id,
            "url": f"https://www.notion.so/{database_id.replace('-', '')}",
        }

    def section_allowed(item: NavItem) -> bool:
        if not sections:
            return True
        if item.file_rel:
            return any(item.file_rel.startswith(s) for s in sections)
        return any(section_allowed(c) for c in item.children)

    def match_items(items: List[NavItem], parent_page_id: str) -> None:
        unused = list(by_parent.get(parent_page_id, []))
        for item in items:
            if not section_allowed(item):
                continue
            match = next((c for c in unused if c["title"] == item.title), None)
            if match is None:
                log.warning("missing Notion page for %r title=%r", item.key, item.title)
                continue
            unused.remove(match)
            state.pages[item.key] = {"id": match["id"], "url": match["url"]}
            if item.children:
                match_items(item.children, match["id"])

    match_items(start_items, database_id)
    if data_source_id != database_id:
        match_items([i for i in start_items if i.key not in state.pages], data_source_id)
    return state


# ---------------------------------------------------------------------------
# Git diff (incremental)
# ---------------------------------------------------------------------------


@dataclass
class DiffSet:
    md_changed: Set[str] = field(default_factory=set)
    md_deleted: Set[str] = field(default_factory=set)
    assets_changed: Set[str] = field(default_factory=set)
    nav_changed: bool = False

def _run_git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"git {' '.join(args)} failed ({result.returncode}): {result.stderr.strip()}"
        )
    return result.stdout


def resolve_git_base(explicit: Optional[str]) -> Optional[str]:
    """Pick a base ref for incremental sync.

    Priority: CLI --base → GITHUB_EVENT_BEFORE → NOTION_SYNC_BASE → HEAD~1.
    Returns None when a full sync is required (empty / all-zero before SHA).
    """
    if explicit:
        if explicit in ("", "0" * 40, "full"):
            return None
        return explicit

    before = os.environ.get("GITHUB_EVENT_BEFORE") or os.environ.get("NOTION_SYNC_BASE")
    if before:
        if before in ("", "0" * 40):
            return None
        return before

    try:
        _run_git("rev-parse", "--verify", "HEAD~1")
        return "HEAD~1"
    except RuntimeError:
        return None


def git_diff(base: Optional[str]) -> DiffSet:
    """Collect docs/ changes between base...HEAD. If base is None → treat as full."""
    if base is None:
        diff = DiffSet(nav_changed=True)
        # Caller will expand to all pages when nav_changed + full mode.
        return diff

    # Include rename detection; name-status relative to wiki repo root.
    out = _run_git("diff", "--name-status", "--find-renames", f"{base}...HEAD", "--", "docs")
    diff = DiffSet()
    for line in out.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        status = parts[0]
        paths = parts[1:]
        # Renames: R100\told\tnew
        if status.startswith("R") and len(paths) == 2:
            old, new = paths
            _classify_path(diff, old, deleted=True)
            _classify_path(diff, new, deleted=False)
            continue
        path = paths[0]
        deleted = status.startswith("D")
        _classify_path(diff, path, deleted=deleted)
    return diff


def _classify_path(diff: DiffSet, path: str, *, deleted: bool) -> None:
    path = docs_rel(path)
    if path == "docs/.nav.yml" or path.endswith("/.nav.yml"):
        diff.nav_changed = True
        return
    if not path.startswith("docs/"):
        return
    rel = path[5:]  # strip docs/
    suffix = Path(rel).suffix.lower()
    if suffix in (".md", ".ipynb"):
        # Keep .ipynb keys as-is when that is the nav source (mkdocs-jupyter).
        if deleted:
            diff.md_deleted.add(rel)
        else:
            diff.md_changed.add(rel)
    elif suffix in ASSET_SUFFIXES:
        if not deleted:
            diff.assets_changed.add(rel)


def expand_asset_dependents(
    assets: Set[str],
    nav_index: Dict[str, NavItem],
    sections: Optional[List[str]],
) -> Set[str]:
    """Find nav-listed markdown files that reference changed assets (scoped)."""
    if not assets:
        return set()
    candidates: List[Path] = []
    for item in nav_index.values():
        if not item.file_rel:
            continue
        if sections and not any(item.file_rel.startswith(s) for s in sections):
            continue
        source = DOCS_ROOT / item.file_rel
        if source.exists():
            candidates.append(source)

    affected: Set[str] = set()
    for source in candidates:
        rel = docs_rel(str(source.relative_to(DOCS_ROOT)))
        for asset in assets:
            if md_references_asset(source, asset):
                affected.add(rel)
                break
    return affected


# ---------------------------------------------------------------------------
# Sync orchestration
# ---------------------------------------------------------------------------


def filter_sections(rel: str, sections: Optional[List[str]]) -> bool:
    if not sections:
        return True
    return any(rel.startswith(s) for s in sections)


def ensure_section(
    token: str,
    state: MigrationState,
    state_path: Path,
    nav_index: Dict[str, NavItem],
    key: str,
    delay: float,
    dry_run: bool,
) -> str:
    """Ensure a section (or Notebook root) exists; return Notion page id."""
    if key in state.pages:
        return state.pages[key]["id"]

    item = nav_index.get(key)
    if item is None:
        raise KeyError(f"nav key not found: {key}")

    # Notebook root maps to the wiki database itself.
    if item.title == "Notebook" and not item.parent_key:
        state.pages[key] = {
            "id": state.root_page_id,
            "url": f"https://www.notion.so/{state.root_page_id.replace('-', '')}",
        }
        if not dry_run:
            save_state(state_path, state)
        return state.root_page_id

    if item.parent_key:
        parent_id = ensure_section(
            token, state, state_path, nav_index, item.parent_key, delay, dry_run
        )
        parent_kind = "page"
    else:
        parent_id = state.data_source_id or state.root_page_id
        parent_kind = "data_source" if state.data_source_id else "database"

    log.info("create section %s (%s)", item.title, key)
    if dry_run:
        fake = f"dry-run-{key}"
        state.pages[key] = {"id": fake, "url": f"https://www.notion.so/{fake}"}
        return fake

    info = create_page(
        token,
        parent_id,
        item.title,
        title_property=state.title_property,
        parent_kind=parent_kind,
    )
    state.pages[key] = info
    save_state(state_path, state)
    time.sleep(delay)
    return info["id"]


def resolve_parent_id(
    token: str,
    state: MigrationState,
    state_path: Path,
    nav_index: Dict[str, NavItem],
    parent_key: str,
    delay: float,
    dry_run: bool,
) -> Tuple[str, str]:
    if not parent_key:
        parent_id = state.data_source_id or state.root_page_id
        kind = "data_source" if state.data_source_id else "database"
        return parent_id, kind
    # Notebook root → wiki database / data source for children.
    parent_item = nav_index.get(parent_key)
    if parent_item and parent_item.title == "Notebook" and not parent_item.parent_key:
        state.pages.setdefault(
            parent_key,
            {
                "id": state.root_page_id,
                "url": f"https://www.notion.so/{state.root_page_id.replace('-', '')}",
            },
        )
        parent_id = state.data_source_id or state.root_page_id
        kind = "data_source" if state.data_source_id else "database"
        return parent_id, kind
    page_id = ensure_section(
        token, state, state_path, nav_index, parent_key, delay, dry_run
    )
    return page_id, "page"


def sync_one_page(
    token: str,
    state: MigrationState,
    state_path: Path,
    nav_index: Dict[str, NavItem],
    item: NavItem,
    site_url: str,
    delay: float,
    dry_run: bool,
    upload_images: bool,
) -> str:
    assert item.file_rel
    source = DOCS_ROOT / item.file_rel
    if not source.exists():
        log.warning("skip missing file %s", item.file_rel)
        return "missing"

    parent_id, parent_kind = resolve_parent_id(
        token,
        state,
        state_path,
        nav_index,
        item.parent_key,
        delay,
        dry_run,
    )

    created = item.file_rel not in state.pages
    if created:
        log.info("create page %s", item.file_rel)
        if dry_run:
            state.pages[item.file_rel] = {
                "id": f"dry-run-{item.file_rel}",
                "url": f"https://www.notion.so/dry-run",
            }
        else:
            info = create_page(
                token,
                parent_id,
                item.title,
                title_property=state.title_property,
                parent_kind=parent_kind,
            )
            state.pages[item.file_rel] = info
            save_state(state_path, state)
            time.sleep(delay)
    else:
        log.info("update page %s", item.file_rel)

    image_paths: List[Path] = []

    def upload_local(path: Path) -> str:
        if not upload_images:
            return ""
        image_paths.append(path)
        return f"⟦LOCALIMG:{len(image_paths) - 1}⟧"

    title_conv, content, _ = convert_markdown_file(
        source,
        site_url,
        state.pages,
        upload_local=upload_local if upload_images else None,
    )
    _ = title_conv

    if dry_run:
        log.info(
            "dry-run %s content=%d chars images=%d",
            item.file_rel,
            len(content),
            len(image_paths),
        )
        return "dry-run"

    page_id = state.pages[item.file_rel]["id"]
    update_page_markdown(token, page_id, content)
    attached = 0
    if upload_images and image_paths:
        attached = attach_placeholder_images(token, page_id, image_paths)
    log.info(
        "ok %s (%s, images=%d/%d)",
        item.file_rel,
        "created" if created else "updated",
        attached,
        len(image_paths),
    )
    time.sleep(delay)
    return "created" if created else "updated"


def collect_targets(
    *,
    full: bool,
    diff: DiffSet,
    nav_index: Dict[str, NavItem],
    sections: Optional[List[str]],
) -> Tuple[List[NavItem], Set[str]]:
    """Return (pages to sync, deleted rel paths)."""
    deleted = {p for p in diff.md_deleted if filter_sections(p, sections)}

    if full:
        items = [
            item
            for item in nav_index.values()
            if item.file_rel
            and filter_sections(item.file_rel, sections)
            and (DOCS_ROOT / item.file_rel).exists()
        ]
        return items, deleted

    wanted = set(diff.md_changed)
    if diff.assets_changed:
        wanted |= expand_asset_dependents(diff.assets_changed, nav_index, sections)

    items: List[NavItem] = []
    for rel in sorted(wanted):
        if not filter_sections(rel, sections):
            continue
        item = nav_index.get(rel)
        if item is None or not item.file_rel:
            log.warning("changed file not in nav, skip: %s", rel)
            continue
        items.append(item)
    return items, deleted


def run_sync(args: argparse.Namespace) -> int:
    token = resolve_token(args.token)
    if not token and not args.dry_run:
        log.error(
            "Notion token not found. Set NOTION_TOKEN, add wiki/.env, "
            "or configure notionApi in ~/.cursor/mcp.json"
        )
        return 1

    state_path: Path = args.state
    sections: Optional[List[str]] = args.section

    # Resolve what to sync.
    path_list: list[str] = []
    if args.paths:
        path_list.extend(args.paths)
    if getattr(args, "paths_file", None):
        raw = Path(args.paths_file).read_text(encoding="utf-8")
        path_list.extend(line.strip() for line in raw.splitlines() if line.strip())

    if path_list:
        normalized = set()
        for p in path_list:
            rel = docs_rel(p)
            if rel.startswith("docs/"):
                rel = rel[5:]
            normalized.add(rel)
        diff = DiffSet(md_changed=normalized)
        base = "(paths)"
        full = False
    elif args.full:
        diff = DiffSet(nav_changed=True)
        base = None
        full = True
    else:
        base = resolve_git_base(args.base)
        full = base is None
        if full:
            log.info("no git base available → full sync")
            diff = DiffSet(nav_changed=True)
        else:
            log.info("incremental sync since %s", base)
            diff = git_diff(base)

    log.info(
        "diff: md=%d deleted=%d assets=%d nav_changed=%s full=%s",
        len(diff.md_changed),
        len(diff.md_deleted),
        len(diff.assets_changed),
        diff.nav_changed,
        full,
    )

    tree = build_nav_tree(load_nav())
    nav_index = index_nav(tree)

    # Load / rebuild page map.
    state = load_state(state_path)
    need_rebuild = args.rebuild_state or not state.pages
    if need_rebuild:
        if args.dry_run and not token:
            log.warning("dry-run without token: empty state")
        else:
            assert token
            log.info("rebuilding page map from Notion wiki…")
            state = rebuild_state_from_wiki(
                token,
                data_source_id=args.data_source_id,
                database_id=args.database_id,
                sections=sections,
            )
            if not args.dry_run:
                save_state(state_path, state)
            log.info("mapped %d keys", len(state.pages))
    else:
        state.root_page_id = state.root_page_id or args.database_id
        state.data_source_id = state.data_source_id or args.data_source_id
        state.title_property = state.title_property or DEFAULT_TITLE_PROP

    targets, deleted = collect_targets(
        full=full, diff=diff, nav_index=nav_index, sections=sections
    )

    if deleted:
        for rel in sorted(deleted):
            log.info("deleted locally (Notion page left intact): %s", rel)

    if not targets:
        log.info("nothing to sync")
        return 0

    log.info("syncing %d page(s)", len(targets))
    stats = {"created": 0, "updated": 0, "dry-run": 0, "missing": 0, "failed": 0}
    for item in targets:
        try:
            result = sync_one_page(
                token or "",
                state,
                state_path,
                nav_index,
                item,
                args.site_url,
                args.delay,
                args.dry_run,
                upload_images=not args.no_images,
            )
            stats[result] = stats.get(result, 0) + 1
        except urllib.error.HTTPError as exc:
            body = getattr(exc, "reason", "") or ""
            log.error("FAIL %s: %s %s", item.file_rel, exc.code, body)
            stats["failed"] += 1
            if not args.continue_on_error:
                return 1
        except Exception as exc:
            log.error("FAIL %s: %s", item.file_rel, exc)
            stats["failed"] += 1
            if not args.continue_on_error:
                return 1

    if not args.dry_run:
        save_state(state_path, state)
    log.info("done %s", json.dumps(stats, ensure_ascii=False))
    return 1 if stats["failed"] else 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Sync MkDocs wiki → Notion (incremental via git diff)"
    )
    p.add_argument(
        "--full",
        action="store_true",
        help="Process all nav pages (ignore git diff)",
    )
    p.add_argument(
        "--base",
        help="Git base ref for diff (default: GITHUB_EVENT_BEFORE / HEAD~1). "
        "Use 'full' to force full sync.",
    )
    p.add_argument(
        "--paths",
        nargs="+",
        help="Only sync these docs-relative paths (skip git diff)",
    )
    p.add_argument(
        "--paths-file",
        type=Path,
        help="Newline-separated docs-relative paths (handles spaces safely)",
    )
    p.add_argument("--site-url", default=DEFAULT_SITE_URL)
    p.add_argument("--state", type=Path, default=DEFAULT_STATE)
    p.add_argument("--database-id", default=DEFAULT_WIKI_DATABASE)
    p.add_argument("--data-source-id", default=DEFAULT_WIKI_DATA_SOURCE)
    p.add_argument("--section", action="append", help="Limit to path prefixes, e.g. obsidian/")
    p.add_argument("--delay", type=float, default=0.35)
    p.add_argument("--token")
    p.add_argument("--rebuild-state", action="store_true", help="Remap pages from Notion wiki")
    p.add_argument("--no-images", action="store_true", help="Skip local image upload")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--continue-on-error", action="store_true")
    p.add_argument("-v", "--verbose", action="store_true")
    return p


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    setup_logging(args.verbose)
    try:
        return run_sync(args)
    except KeyboardInterrupt:
        log.error("interrupted")
        return 130


if __name__ == "__main__":
    sys.exit(main())
