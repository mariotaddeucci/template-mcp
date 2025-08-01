# Template MCP Documentation

This directory contains documentation for the Template MCP server.

## Documentation Structure

- `setup.md` - Initial setup and configuration guide
- `architecture.md` - System architecture overview  
- `api.md` - API documentation
- `deployment.md` - Deployment guide
- `troubleshooting.md` - Common issues and solutions

## Quick Start

1. Install dependencies: `uv sync --all-extras`
2. Start Eunomia server: `docker run -d -p 8000:8000 ttommitt/eunomia-server:latest`
3. Run the MCP server: `uv run python -m template_mcp.main`

For detailed setup instructions, see [setup.md](setup.md).