# markzoterodown — Claude Code context

## What this is

A Python MCP server that provides full-text Markdown access to files attached to
Zotero library items. It is a **companion** to the `zotero-remote` MCP (which
handles searching and browsing); this server handles the file content layer.

## Architecture

```
src/markzoterodown/
├── __init__.py      # version only
└── server.py        # all logic: FastMCP server + two tools
```

Single-file server, intentionally simple. No CLI, no config files, no database —
just environment variables read at startup and two MCP tools exposed via stdio.

### The two tools

| Tool | Input | What it does |
|---|---|---|
| `list_item_attachments` | `item_key` (Zotero item key) | Calls `pyzotero.children()` on the web API, filters to file attachments, resolves local paths |
| `get_attachment_as_markdown` | `attachment_key` | Fetches attachment metadata, resolves file path on disk, runs `MarkItDown.convert()` |

### File path resolution (`_resolve_file_path`)

- **`imported_file` / `imported_url`**: `~/Zotero/storage/{KEY}/{filename}` — standard Zotero layout
- **`linked_file`**: uses the `path` field; strips `attachments:` prefix for relative paths
- **`linked_url`**: no local file — `get_attachment_as_markdown` fetches the URL directly via MarkItDown

## Key dependencies

| Package | Why |
|---|---|
| `mcp[cli]` | FastMCP server framework (stdio transport) |
| `pyzotero` | Zotero web API client |
| `markitdown[all]` | Converts PDF/DOCX/PPTX/HTML/… to Markdown |

## Environment variables

| Variable | Default | Notes |
|---|---|---|
| `ZOTERO_LIBRARY_ID` | *(required)* | Numeric user/group ID from zotero.org/settings/keys |
| `ZOTERO_API_KEY` | `""` | API key from zotero.org/settings/keys |
| `ZOTERO_LIBRARY_TYPE` | `user` | `user` or `group` |
| `ZOTERO_USE_LOCAL` | `false` | `true` = use local API at port 23119 (must be enabled in Zotero prefs) |
| `ZOTERO_STORAGE_PATH` | `~/Zotero/storage` | Where Zotero stores synced attachment files |

## Development workflow

```bash
# Install dependencies
uv sync

# Run the server manually (stdio, for debugging)
uv run python src/markzoterodown/server.py

# Quick import / tool registration check
uv run python -c "from markzoterodown.server import mcp; print([t.name for t in mcp._tool_manager.list_tools()])"

# Build distribution artefacts
uv build

# Publish to PyPI (token stored in macOS Keychain via `keyring`)
uv publish --token pypi-...
# or if UV_PUBLISH_TOKEN is exported:
uv publish
```

## Claude Desktop / Claude Code MCP config

```json
{
  "mcpServers": {
    "zotero-fulltext": {
      "command": "uvx",
      "args": ["markzoterodown"],
      "env": {
        "ZOTERO_LIBRARY_ID": "...",
        "ZOTERO_API_KEY": "..."
      }
    }
  }
}
```

`uvx` pulls the package from PyPI into an isolated environment on first run and
caches it — no manual install required on any machine.

## Release checklist

1. Bump `version` in `pyproject.toml` **and** `src/markzoterodown/__init__.py`
2. `uv build`
3. `uv publish --token pypi-...`
4. `git tag vX.Y.Z && git push --tags`
