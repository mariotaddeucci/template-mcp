"""Main entry point for the Template MCP server."""

import asyncio
import os
import sys

from .config import load_config
from .logging import log_shutdown, log_startup, setup_logging
from .server import run_server


async def main() -> None:
    """Main entry point for the Template MCP server."""
    try:
        # Load configuration
        environment = os.getenv("ENVIRONMENT", "development")
        config = load_config(environment)

        # Setup logging
        setup_logging(config.logging)

        # Log startup
        log_startup(
            config.mcp_server.name,
            config.mcp_server.version,
            config.mcp_server.port,
        )

        # Run the server
        await run_server(config)

    except KeyboardInterrupt:
        print("\nReceived interrupt signal")
    except Exception as e:
        print(f"Failed to start server: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        # Log shutdown
        if "config" in locals():
            log_shutdown(config.mcp_server.name)


def sync_main() -> None:
    """Synchronous wrapper for the main async function."""
    asyncio.run(main())


if __name__ == "__main__":
    sync_main()
