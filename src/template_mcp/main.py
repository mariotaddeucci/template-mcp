"""Main entry point for the Template MCP server."""

import logging

logger = logging.getLogger(__name__)


def main():
    """Main entry point for the Template MCP server."""
    logging.basicConfig(level=logging.INFO)
    logger.info("Hello from template-mcp!")


if __name__ == "__main__":
    main()
