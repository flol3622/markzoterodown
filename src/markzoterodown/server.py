#!/usr/bin/env python3
"""
MCP server providing full-text access to Zotero attachments via MarkItDown.
Complements the zotero-remote MCP (which handles item browsing/searching) by
resolving the local file path of attachments and converting them to Markdown.
"""

import json
import os
from pathlib import Path

from mcp.server.fastmcp import FastMCP
from markitdown import MarkItDown
import pyzotero.zotero as zotero_lib

mcp = FastMCP(
    "zotero-fulltext",
    instructions=(
        "This server provides full-text access to files attached to Zotero items. "
        "Use list_item_attachments to discover which files belong to an item, "
        "then get_attachment_as_markdown to retrieve their full text."
    ),
)

# ── Configuration ────────────────────────────────────────────────────────────
LIBRARY_ID   = os.environ.get("ZOTERO_LIBRARY_ID", "")
API_KEY      = os.environ.get("ZOTERO_API_KEY", "")
LIBRARY_TYPE = os.environ.get("ZOTERO_LIBRARY_TYPE", "user")
# Set ZOTERO_USE_LOCAL=true to use the local Zotero API (port 23119, requires it to be enabled)
USE_LOCAL    = os.environ.get("ZOTERO_USE_LOCAL", "false").lower() == "true"
# Where Zotero stores imported attachment files
STORAGE_PATH = Path(
    os.environ.get("ZOTERO_STORAGE_PATH", "~/Zotero/storage")
).expanduser()


def _zot() -> zotero_lib.Zotero:
    if not LIBRARY_ID:
        raise RuntimeError(
            "ZOTERO_LIBRARY_ID environment variable is not set. "
            "Set it to your Zotero user/group ID."
        )
    return zotero_lib.Zotero(LIBRARY_ID, LIBRARY_TYPE, API_KEY, local=USE_LOCAL)


def _resolve_file_path(data: dict) -> Path:
    """Return the local filesystem path for an attachment item's data dict."""
    link_mode = data.get("linkMode", "")
    key       = data.get("key", "")
    filename  = data.get("filename", "")

    if link_mode == "linked_file":
        raw = data.get("path", "")
        # Zotero prefixes relative linked paths with "attachments:"
        if raw.startswith("attachments:"):
            rel = raw[len("attachments:"):]
            return STORAGE_PATH.parent / "attachments" / rel
        return Path(raw).expanduser()

    # imported_file / imported_url — stored under storage/{KEY}/{filename}
    if not filename:
        raise ValueError(f"Attachment {key} has no filename in its metadata.")
    return STORAGE_PATH / key / filename


# ── Tools ────────────────────────────────────────────────────────────────────

@mcp.tool()
def list_item_attachments(item_key: str) -> str:
    """
    List all file attachments for a Zotero item.

    Returns a JSON array of attachment objects, each with:
    - key:         use this with get_attachment_as_markdown
    - title:       human-readable title stored in Zotero
    - filename:    actual file name on disk
    - contentType: MIME type (e.g. "application/pdf")
    - linkMode:    how the file is stored ("imported_file", "linked_file", "imported_url")
    - localPath:   resolved absolute path on this machine (may not exist if not synced)

    Args:
        item_key: Zotero item key, e.g. "ABC12DEF"
    """
    zot = _zot()
    children = zot.children(item_key)

    attachments = []
    for child in children:
        data = child.get("data", {})
        if data.get("itemType") != "attachment":
            continue
        link_mode = data.get("linkMode", "")
        # Skip pure URL links that have no associated file
        if link_mode == "linked_url":
            continue

        try:
            local_path = str(_resolve_file_path({**data, "key": child["key"]}))
        except ValueError:
            local_path = None

        attachments.append({
            "key":         child["key"],
            "title":       data.get("title", ""),
            "filename":    data.get("filename", ""),
            "contentType": data.get("contentType", ""),
            "linkMode":    link_mode,
            "localPath":   local_path,
        })

    if not attachments:
        return json.dumps(
            {"message": "No file attachments found for this item.", "attachments": []},
            indent=2,
        )

    return json.dumps({"attachments": attachments}, indent=2)


@mcp.tool()
def get_attachment_as_markdown(attachment_key: str) -> str:
    """
    Convert a Zotero attachment's file to Markdown using MarkItDown.

    Supports PDF, DOCX, XLSX, PPTX, HTML, images, audio, and many other
    formats. The file must be present locally (i.e. Zotero has synced it).

    Call list_item_attachments first to find the right attachment_key.

    Args:
        attachment_key: Zotero attachment item key, e.g. "XYZ98GHI"
    """
    zot = _zot()
    item = zot.item(attachment_key)
    data = item.get("data", {})

    if data.get("itemType") != "attachment":
        return f"Error: {attachment_key} is not an attachment item."

    if data.get("linkMode") == "linked_url":
        url = data.get("url", "")
        if not url:
            return "Error: linked_url attachment has no URL."
        md = MarkItDown()
        result = md.convert(url)
        return result.text_content

    try:
        file_path = _resolve_file_path({**data, "key": attachment_key})
    except ValueError as exc:
        return f"Error: {exc}"

    if not file_path.exists():
        return (
            f"Error: file not found at {file_path}.\n"
            "Make sure Zotero has synced this attachment locally and that "
            "ZOTERO_STORAGE_PATH points to your Zotero storage directory "
            f"(currently: {STORAGE_PATH})."
        )

    md = MarkItDown()
    result = md.convert(str(file_path))
    return result.text_content


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
