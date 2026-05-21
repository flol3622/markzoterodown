# markzoterodown

[![PyPI](https://img.shields.io/pypi/v/markzoterodown)](https://pypi.org/project/markzoterodown/)
[![Python](https://img.shields.io/pypi/pyversions/markzoterodown)](https://pypi.org/project/markzoterodown/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An MCP server that gives Claude (or any MCP client) **full-text Markdown access**
to files attached to your Zotero library items.

It complements the [zotero-remote MCP](https://github.com/flol3622/markzoterodown)
— which lets you search and browse your library — by resolving the local file
path of any attachment and converting it to Markdown via
[MarkItDown](https://github.com/microsoft/markitdown).

## Tools

| Tool | Description |
|---|---|
| `list_item_attachments` | List all file attachments for a Zotero item (key, filename, MIME type, local path) |
| `get_attachment_as_markdown` | Convert an attachment (PDF, DOCX, PPTX, HTML, …) to full-text Markdown |

## Typical workflow

```
zotero_search("gypsum sorption")           ← zotero-remote MCP
  → item key: BZPBTWVU

list_item_attachments("BZPBTWVU")          ← this server
  → attachment key: AE7VF5JI
     filename: Wilkes 2004.pdf

get_attachment_as_markdown("AE7VF5JI")     ← this server
  → full Markdown text of the paper
```

## Installation

No cloning or manual installs needed. Uses [`uvx`](https://docs.astral.sh/uv/)
to pull the package from PyPI into an isolated environment on first run:

```bash
uvx markzoterodown   # that's it
```

## Setup

### 1. Get your Zotero credentials

Go to [zotero.org/settings/keys](https://www.zotero.org/settings/keys):

- Your **library ID** is the number shown under "Your userID for use in API calls"
- Click **Create new private key** to generate an API key

### 2. Add to Claude Desktop / Claude Code

Edit your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "zotero-fulltext": {
      "command": "uvx",
      "args": ["markzoterodown"],
      "env": {
        "ZOTERO_LIBRARY_ID": "<your numeric user ID>",
        "ZOTERO_API_KEY":    "<your API key>"
      }
    }
  }
}
```

On **macOS** the config file lives at:
`~/Library/Application Support/Claude/claude_desktop_config.json`

Restart Claude after saving.

## Configuration

All configuration is via environment variables:

| Variable | Default | Description |
|---|---|---|
| `ZOTERO_LIBRARY_ID` | *(required)* | Numeric Zotero user or group ID |
| `ZOTERO_API_KEY` | `""` | Zotero API key |
| `ZOTERO_LIBRARY_TYPE` | `user` | `user` or `group` |
| `ZOTERO_USE_LOCAL` | `false` | Set `true` to use the Zotero local API (port 23119) instead of the web API — requires enabling it in Zotero → Settings → Advanced |
| `ZOTERO_STORAGE_PATH` | `~/Zotero/storage` | Path where Zotero stores synced attachment files |

## Troubleshooting

**"File not found" error**  
The attachment exists in Zotero but hasn't been downloaded locally. Open Zotero,
right-click the item → *Find Available PDF* or *Download PDF*. The file must be
present in `ZOTERO_STORAGE_PATH` on this machine.

**403 from the Zotero API**  
Your API key doesn't have read access. Regenerate it at
[zotero.org/settings/keys](https://www.zotero.org/settings/keys) and make sure
"Allow library access" is checked.

**`ZOTERO_LIBRARY_ID` not set**  
The server will return a clear error message. Add the env var to your MCP config.

**Using a Zotero group library**  
Set `ZOTERO_LIBRARY_TYPE=group` and use the group's numeric ID (visible in its
URL on zotero.org).

## Development

```bash
git clone https://github.com/flol3622/markzoterodown
cd markzoterodown
uv sync

# verify tools register
uv run python -c "from markzoterodown.server import mcp; print([t.name for t in mcp._tool_manager.list_tools()])"

# build + publish
uv build
uv publish --token pypi-...
```

## License

MIT
