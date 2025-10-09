#!/usr/bin/env python3
"""
Didlogic MCP Server CLI
-----------------------
Command-line interface for running the Didlogic MCP server.

Supports two transport modes:
- stdio: Standard input/output (default, for local Claude Desktop integration)
- http: HTTP server (for remote access and web clients)
"""

import argparse
import os
import sys
import logging
from pathlib import Path

# Import the actual server.py module, not the server() function from __init__.py
sys.path.insert(0, str(Path(__file__).parent))
import server as server_module

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Didlogic MCP Server - Connect LLMs to Didlogic API"
    )
    parser.add_argument(
        "--transport",
        type=str,
        choices=["stdio", "http", "sse"],
        default="stdio",
        help="Transport mode: stdio (default), http, or sse"
    )
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Host to bind to in HTTP mode (default: 127.0.0.1)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=None,
        help="Port to bind to in HTTP mode (default: from PORT env or 8000)"
    )
    parser.add_argument(
        "--log-level",
        type=str,
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Logging level (default: INFO)"
    )

    args = parser.parse_args()

    # Set log level
    logging.getLogger().setLevel(args.log_level)

    # Set transport mode
    server_module.set_transport_mode(args.transport)

    # Run server based on transport mode
    if args.transport == "stdio":
        logger.info("Starting Didlogic MCP server in stdio mode")
        # Check for API key in stdio mode
        if not os.environ.get("DIDLOGIC_API_KEY"):
            logger.error("DIDLOGIC_API_KEY environment variable not set!")
            sys.exit(1)
        server_module.mcp.run(transport="stdio")

    elif args.transport == "http":
        # Get port from args or environment or default
        port = args.port or int(os.environ.get("PORT", "8000"))

        logger.info(f"Starting Didlogic MCP server in HTTP mode on {args.host}:{port}")
        logger.info("Authentication: Bearer token required in Authorization header")
        logger.info("No environment API key fallback in HTTP mode")

        # Configure host and port for HTTP mode
        server_module.configure_http_server(host=args.host, port=port)

        # Create app with middleware and run with uvicorn
        import uvicorn
        app = server_module.create_app_with_middleware(transport="streamable-http")
        uvicorn.run(app, host=args.host, port=port)

    elif args.transport == "sse":
        # Get port from args or environment or default
        port = args.port or int(os.environ.get("PORT", "8000"))

        logger.info(f"Starting Didlogic MCP server in SSE mode on {args.host}:{port}")
        logger.info("Authentication: Bearer token required in Authorization header")
        logger.info("No environment API key fallback in SSE mode")

        # Configure host and port for SSE mode
        server_module.configure_http_server(host=args.host, port=port)

        # Create app with middleware and run with uvicorn
        import uvicorn
        app = server_module.create_app_with_middleware(transport="sse")
        uvicorn.run(app, host=args.host, port=port)


if __name__ == "__main__":
    main()
