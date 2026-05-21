# Agent Setup Guide

This page keeps the copy-paste MCP setup snippets out of the README. Pick the
agent or tool you use and expand its section.

## Universal Values

Most clients ultimately need the same pieces:

| Field | Value |
|---|---|
| Server name | `zotero-fulltext` |
| Transport | `stdio` |
| Command | `uvx` |
| Arguments | `markzoterodown` |
| Required env | `ZOTERO_LIBRARY_ID`, plus `ZOTERO_API_KEY` unless using `ZOTERO_USE_LOCAL=true` |

Base config for clients that use Claude-style `mcpServers` JSON:

```json
{
  "mcpServers": {
    "zotero-fulltext": {
      "command": "uvx",
      "args": ["markzoterodown"],
      "env": {
        "ZOTERO_LIBRARY_ID": "<your numeric user or group ID>",
        "ZOTERO_API_KEY": "<your Zotero API key>"
      }
    }
  }
}
```

For group libraries, add:

```json
"ZOTERO_LIBRARY_TYPE": "group"
```

For Zotero Desktop local API mode, use:

```json
"ZOTERO_USE_LOCAL": "true"
```

If a GUI app cannot find `uvx`, replace `"command": "uvx"` with the absolute
path returned by one of these commands:

```bash
which uvx
```

```powershell
where.exe uvx
```

## Agents And Tools

<details>
<summary>Claude Desktop</summary>

Open Claude Desktop settings, go to **Developer**, and choose **Edit Config**.
Paste the universal `mcpServers` JSON into `claude_desktop_config.json`.

Config file locations:

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

Restart Claude Desktop after saving.

</details>

<details>
<summary>Claude Code</summary>

User-wide setup:

```bash
claude mcp add --transport stdio --scope user --env ZOTERO_LIBRARY_ID=123456 --env ZOTERO_API_KEY=zotero_api_key zotero-fulltext -- uvx markzoterodown
```

Project setup, which writes `.mcp.json` in the current project:

```bash
claude mcp add --transport stdio --scope project --env ZOTERO_LIBRARY_ID=123456 --env ZOTERO_API_KEY=zotero_api_key zotero-fulltext -- uvx markzoterodown
```

Verify:

```bash
claude mcp list
```

Use `--scope local` instead of `project` when you want the server only in the
current project but do not want to commit config.

</details>

<details>
<summary>Codex CLI and Codex IDE extension</summary>

Command setup:

```bash
codex mcp add zotero-fulltext --env ZOTERO_LIBRARY_ID=123456 --env ZOTERO_API_KEY=zotero_api_key -- uvx markzoterodown
```

Verify:

```bash
codex mcp --help
```

Manual config in `~/.codex/config.toml` or project `.codex/config.toml`:

```toml
[mcp_servers."zotero-fulltext"]
command = "uvx"
args = ["markzoterodown"]

[mcp_servers."zotero-fulltext".env]
ZOTERO_LIBRARY_ID = "123456"
ZOTERO_API_KEY = "zotero_api_key"
```

In the Codex TUI, use `/mcp` to see active servers.

</details>

<details>
<summary>VS Code / GitHub Copilot</summary>

Use **MCP: Add Server** from the Command Palette, or add this to
`.vscode/mcp.json` for a workspace server:

```json
{
  "inputs": [
    {
      "type": "promptString",
      "id": "zotero-library-id",
      "description": "Zotero library ID"
    },
    {
      "type": "promptString",
      "id": "zotero-api-key",
      "description": "Zotero API key",
      "password": true
    }
  ],
  "servers": {
    "zotero-fulltext": {
      "type": "stdio",
      "command": "uvx",
      "args": ["markzoterodown"],
      "env": {
        "ZOTERO_LIBRARY_ID": "${input:zotero-library-id}",
        "ZOTERO_API_KEY": "${input:zotero-api-key}"
      }
    }
  }
}
```

Command-line install is also possible:

```bash
code --add-mcp "{\"name\":\"zotero-fulltext\",\"command\":\"uvx\",\"args\":[\"markzoterodown\"],\"env\":{\"ZOTERO_LIBRARY_ID\":\"123456\",\"ZOTERO_API_KEY\":\"zotero_api_key\"}}"
```

The `mcp.json` version with inputs is preferable because it avoids putting the
API key in shell history.

</details>

<details>
<summary>Cursor</summary>

Create one of these files:

- Project: `.cursor/mcp.json`
- Global: `~/.cursor/mcp.json`

```json
{
  "mcpServers": {
    "zotero-fulltext": {
      "type": "stdio",
      "command": "uvx",
      "args": ["markzoterodown"],
      "env": {
        "ZOTERO_LIBRARY_ID": "123456",
        "ZOTERO_API_KEY": "zotero_api_key"
      }
    }
  }
}
```

Cursor's CLI can inspect configured servers:

```bash
cursor-agent mcp list
cursor-agent mcp list-tools zotero-fulltext
```

</details>

<details>
<summary>Windsurf / Cascade</summary>

Open **Windsurf Settings** -> **Cascade** -> **MCP Servers**, or edit the raw
config file:

```text
~/.codeium/windsurf/mcp_config.json
```

Use the same `mcpServers` JSON:

```json
{
  "mcpServers": {
    "zotero-fulltext": {
      "command": "uvx",
      "args": ["markzoterodown"],
      "env": {
        "ZOTERO_LIBRARY_ID": "123456",
        "ZOTERO_API_KEY": "zotero_api_key"
      }
    }
  }
}
```

Refresh the MCP servers in Cascade after saving.

</details>

<details>
<summary>Gemini CLI</summary>

Command setup:

```bash
gemini mcp add --scope user --transport stdio --env ZOTERO_LIBRARY_ID=123456 --env ZOTERO_API_KEY=zotero_api_key zotero-fulltext uvx markzoterodown
```

Verify:

```bash
gemini mcp list
```

Manual config in `~/.gemini/settings.json` or project `.gemini/settings.json`:

```json
{
  "mcpServers": {
    "zotero-fulltext": {
      "command": "uvx",
      "args": ["markzoterodown"],
      "env": {
        "ZOTERO_LIBRARY_ID": "123456",
        "ZOTERO_API_KEY": "zotero_api_key"
      }
    }
  }
}
```

Inside Gemini CLI, `/mcp` shows connection status and available tools.

</details>

<details>
<summary>OpenCode</summary>

Add this to global `~/.config/opencode/opencode.json` or project
`opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "zotero-fulltext": {
      "type": "local",
      "command": ["uvx", "markzoterodown"],
      "enabled": true,
      "environment": {
        "ZOTERO_LIBRARY_ID": "123456",
        "ZOTERO_API_KEY": "zotero_api_key"
      }
    }
  }
}
```

Verify:

```bash
opencode mcp list
```

</details>

<details>
<summary>MetaMCP</summary>

In the MetaMCP dashboard:

1. Go to **MCP Servers**.
2. Click **Add Server**.
3. Use `STDIO` as the server type.
4. Set `command` to `uvx`.
5. Set `args` to `["markzoterodown"]`.
6. Add the Zotero environment variables.
7. Test, then save.

Bulk import JSON:

```json
{
  "mcpServers": {
    "zotero-fulltext": {
      "type": "stdio",
      "command": "uvx",
      "args": ["markzoterodown"],
      "env": {
        "ZOTERO_LIBRARY_ID": "123456",
        "ZOTERO_API_KEY": "zotero_api_key"
      },
      "description": "Read Zotero attachment files as Markdown"
    }
  }
}
```

After importing, add the server to a namespace and expose that namespace through
an endpoint for your downstream clients.

</details>

<details>
<summary>Other MCP clients</summary>

If your client supports local stdio MCP servers, choose:

- Transport: `stdio`
- Command: `uvx`
- Args: `markzoterodown`
- Env: the Zotero variables from the configuration table in the README

If it asks for JSON, try the universal `mcpServers` block first.

</details>

## Local Checkout Setup

If you want an MCP client to run a local development checkout instead of the
PyPI package, see the
**[development guide](development.md#run-an-mcp-client-against-a-local-checkout)**.

## Troubleshooting

<details>
<summary>The MCP client cannot find <code>uvx</code></summary>

GUI apps often have a smaller PATH than your terminal. Find the absolute path
with `which uvx` or `where.exe uvx`, then use that path as the command.

</details>

<details>
<summary><code>get_attachment_as_markdown</code> says "file not found"</summary>

The attachment exists in Zotero but has not been downloaded locally. Open
Zotero, right-click the item or attachment, and download/sync the file. The file
must be present in `ZOTERO_STORAGE_PATH` on the machine running the MCP server.

</details>

<details>
<summary>Zotero API returns <code>403</code></summary>

Your API key does not have read access. Regenerate it at
[zotero.org/settings/keys](https://www.zotero.org/settings/keys) and make sure
library access is enabled.

</details>

<details>
<summary>Group library attachments do not show up</summary>

Set `ZOTERO_LIBRARY_TYPE=group` and use the group's numeric ID from Zotero's
web URL.

</details>

<details>
<summary>Claude Desktop shows no tools</summary>

Restart Claude Desktop completely, then inspect the MCP logs:

- macOS: `~/Library/Logs/Claude`
- Windows: `%APPDATA%\Claude\logs`

Look for `mcp.log` and `mcp-server-zotero-fulltext.log`.

</details>

## Client Docs Referenced

- [Claude Desktop local MCP setup](https://modelcontextprotocol.io/docs/develop/connect-local-servers)
- [Claude Code MCP](https://code.claude.com/docs/en/mcp)
- [Codex MCP](https://developers.openai.com/codex/mcp)
- [VS Code MCP configuration](https://code.visualstudio.com/docs/copilot/reference/mcp-configuration)
- [Cursor MCP](https://docs.cursor.com/en/context/mcp)
- [Windsurf Cascade MCP](https://docs.windsurf.com/windsurf/cascade/mcp)
- [Gemini CLI MCP](https://google-gemini.github.io/gemini-cli/docs/tools/mcp-server.html)
- [OpenCode MCP servers](https://opencode.ai/docs/mcp-servers/)
- [MetaMCP server configuration](https://docs.metamcp.com/en/concepts/mcp-servers)
