# markzoterodown

An MCP server that gives Claude (or any MCP client) full-text Markdown access to
files attached to your Zotero library items.

It complements the [zotero-remote MCP](https://github.com/) — which lets you
search and browse your library — by resolving the local file path of any
attachment and converting it to Markdown via
[MarkItDown](https://github.com/microsoft/markitdown).

## Tools

| Tool | Description |
|---|---|
| `list_item_attachments` | List all file attachments for a Zotero item (key, filename, MIME type, local path) |
| `get_attachment_as_markdown` | Convert an attachment (PDF, DOCX, PPTX, …) to full-text Markdown |

## Installation

No cloning needed. Install and run directly with [`uvx`](https://docs.astral.sh/uv/):

```bash
uvx markzoterodown
```

## Claude Code / Claude Desktop setup

Add this to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "zotero-fulltext": {
      "command": "uvx",
      "args": ["markzoterodown"],
      "env": {
        "ZOTERO_LIBRARY_ID": "<your numeric Zotero user ID>",
        "ZOTERO_API_KEY":    "<your Zotero API key>"
      }
    }
  }
}
```

> Find your **library ID** and generate an **API key** at
> https://www.zotero.org/settings/keys

## Environment variables

| Variable | Default | Description |
|---|---|---|
| `ZOTERO_LIBRARY_ID` | *(required)* | Numeric Zotero user or group ID |
| `ZOTERO_API_KEY` | `""` | Zotero API key (required for web API) |
| `ZOTERO_LIBRARY_TYPE` | `user` | `user` or `group` |
| `ZOTERO_USE_LOCAL` | `false` | Set to `true` to use the Zotero local API (port 23119) instead of the web API |
| `ZOTERO_STORAGE_PATH` | `~/Zotero/storage` | Local path where Zotero stores attachment files |

## Typical workflow

```
zotero_search("gypsum sorption")          ← zotero-remote MCP
  → item key: BZPBTWVU

list_item_attachments("BZPBTWVU")         ← this server
  → attachment key: AE7VF5JI, filename: Wilkes 2004.pdf

get_attachment_as_markdown("AE7VF5JI")    ← this server
  → full Markdown text of the paper
```

## Requirements

- Python ≥ 3.11
- Zotero attachments synced locally (the file must exist in `ZOTERO_STORAGE_PATH`)

## License

MIT
