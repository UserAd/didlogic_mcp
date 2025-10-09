# Didlogic MCP Server

[![Trust Score](https://archestra.ai/mcp-catalog/api/badge/quality/UserAd/didlogic_mcp)](https://archestra.ai/mcp-catalog/userad__didlogic_mcp)
A Model Context Protocol (MCP) server implementation for the Didlogic API. This server allows Large Language Models (LLMs) to interact with Didlogic services through a standardized interface.

## Features

- Full access to Didlogic API through MCP tools
- Specialized prompts for common operations
- Balance management tools
- SIP account (sipfriends) management
- IP restriction management
- Purchases management
- Call hisory access
- Transaction history access

## Installation

### Using uv (recommended)

When using [`uv`](https://docs.astral.sh/uv/) no specific installation is needed. We will
use [`uvx`](https://docs.astral.sh/uv/guides/tools/) to directly run *didlogic_mcp*.

### Using PIP

Alternatively you can install `didlogic_mcp` via pip:

```bash
pip install didlogic_mcp
```

After installation, you can run it as a script using:

```bash
DIDLOGIC_API_KEY=YOUR_DIDLOGIC_KEY python -m didlogic_mcp
```

## Transport Modes

The server supports three transport modes:

### STDIO Mode (Default)

For local integration with Claude Desktop or similar tools. Uses the `DIDLOGIC_API_KEY` environment variable for authentication.

```bash
# Using uvx (recommended)
DIDLOGIC_API_KEY=your_key uvx didlogic_mcp

# Using uv run
DIDLOGIC_API_KEY=your_key uv run didlogic_mcp

# As Python module
DIDLOGIC_API_KEY=your_key python -m didlogic_mcp --transport stdio
```

### HTTP Mode

For remote access and web clients. Requires Bearer token in `Authorization` header for each request.

```bash
# Using default port (8000)
python -m didlogic_mcp --transport http

# Custom port via environment variable
PORT=9000 python -m didlogic_mcp --transport http

# Custom host and port
python -m didlogic_mcp --transport http --host 0.0.0.0 --port 9000

# With debug logging
python -m didlogic_mcp --transport http --log-level DEBUG
```

**Environment Variables:**
- `PORT` - Server port (default: 8000)
- `DIDLOGIC_API_URL` - Didlogic API base URL (default: https://app.didlogic.com/api)

**Note:** In HTTP mode, clients must provide their API key as a Bearer token in the `Authorization` header.

### SSE Mode (Server-Sent Events)

For streaming communication with persistent connections. Ideal for real-time updates and streaming scenarios. Requires Bearer token in `Authorization` header for each request.

```bash
# Using default port (8000)
python -m didlogic_mcp --transport sse

# Custom port via environment variable
PORT=9000 python -m didlogic_mcp --transport sse

# Custom host and port
python -m didlogic_mcp --transport sse --host 0.0.0.0 --port 9000

# With debug logging
python -m didlogic_mcp --transport sse --log-level DEBUG
```

**Environment Variables:**
- `PORT` - Server port (default: 8000)
- `DIDLOGIC_API_URL` - Didlogic API base URL (default: https://app.didlogic.com/api)

**Note:** In SSE mode, clients must provide their API key as a Bearer token in the `Authorization` header for persistent streaming connections.

## Configuration

### Configure for Claude.app

Add to your Claude settings:

#### Using uvx

```json
"mcpServers": {
  "didlogic": {
    "command": "uvx",
    "args": ["didlogic_mcp"],
    "env": {
      "DIDLOGIC_API_KEY": "YOUR_DIDLOGIC_KEY"
    }
  }
}
```

#### Using pip installation

```json
"mcpServers": {
  "didlogic": {
    "command": "python",
    "args": ["-m", "didlogic_mcp"],
    "env": {
      "DIDLOGIC_API_KEY": "YOUR_DIDLOGIC_KEY"
    }
  }
}
```

### Configure for Claude Code

For Claude Code, you can connect to a running SSE server instance:

```bash
claude mcp add didlogic --transport sse http://localhost:8000/sse --header "Authorization: Bearer YOUR_DIDLOGIC_API_KEY"
```

**Prerequisites:**
1. Start the server in SSE mode: `python -m didlogic_mcp --transport sse`
2. Run the above command, replacing `YOUR_DIDLOGIC_API_KEY` with your actual API key
3. The server must be running and accessible at the specified URL

**Custom configuration:**
- To use a different port: Change `http://localhost:8000/sse` to match your server's PORT setting
- To connect to a remote server: Replace `localhost` with the server's hostname or IP address

## License

MIT
