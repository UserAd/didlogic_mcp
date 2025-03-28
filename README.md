# Didlogic MCP Server

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

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Set your Didlogic API key:

```bash
export DIDLOGIC_API_KEY="your-api-key"
```

## Running the Server

Start the server:

```bash
python -m didlogic_mcp
```

For development mode:

```bash
mcp dev didlogic_mcp/server.py
```

## Using with Claude Desktop

Install the server in Claude Desktop:

```bash
mcp install didlogic_mcp/server.py -v DIDLOGIC_API_KEY="your-api-key"
```

## License

MIT
