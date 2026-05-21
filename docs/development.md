# Development Guide

This page keeps contributor, local checkout, build, publish, and release notes
out of the README.

## Development Tasks

<details>
<summary>Set up a local checkout</summary>

```bash
git clone https://github.com/flol3622/markzoterodown
cd markzoterodown
uv sync
```

The package requires Python 3.11 or newer. `uv sync` installs the project and
its development environment from `pyproject.toml` and `uv.lock`.

</details>

<details>
<summary>Run the server manually</summary>

Use this for low-level stdio debugging:

```bash
uv run python src/markzoterodown/server.py
```

The process waits for MCP JSON-RPC messages on stdio. Stop it with `Ctrl+C`.
For normal manual startup through the package entry point, use:

```bash
uv run markzoterodown
```

</details>

<details>
<summary>Verify tool registration</summary>

```bash
uv run python -c "from markzoterodown.server import mcp; print([t.name for t in mcp._tool_manager.list_tools()])"
```

Expected tools:

```text
['list_item_attachments', 'get_attachment_as_markdown']
```

</details>

<details>
<summary>Run an MCP client against a local checkout</summary>

Use this when you want an MCP client to run your local checkout instead of the
PyPI package:

```json
{
  "mcpServers": {
    "zotero-fulltext-dev": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/markzoterodown",
        "run",
        "markzoterodown"
      ],
      "env": {
        "ZOTERO_LIBRARY_ID": "123456",
        "ZOTERO_API_KEY": "zotero_api_key"
      }
    }
  }
}
```

On Windows, use a doubled-backslash or forward-slash path in JSON, for example
`C:/scratch_phd/markzoterodown`.

</details>

<details>
<summary>Build distribution artifacts</summary>

```bash
uv build
```

This creates source and wheel artifacts in `dist/`.

</details>

<details>
<summary>Publish to PyPI</summary>

With a token:

```bash
uv publish --token pypi-...
```

Or, if `UV_PUBLISH_TOKEN` is already exported:

```bash
uv publish
```

</details>

<details>
<summary>Release checklist</summary>

1. Bump `version` in `pyproject.toml`.
2. Bump `__version__` in `src/markzoterodown/__init__.py`.
3. Run `uv build`.
4. Run `uv publish --token pypi-...` or `uv publish`.
5. Tag the release:

```bash
git tag vX.Y.Z
git push --tags
```

</details>
