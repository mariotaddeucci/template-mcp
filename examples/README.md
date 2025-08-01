# Template MCP Examples

This directory contains example scripts and configurations for the Template MCP server.

## Examples

- `basic_client.py` - Basic MCP client example
- `docker-compose.yml` - Docker Compose setup for development
- `policy_examples.json` - Additional policy examples

## Usage

Run examples from the project root:

```bash
uv run python examples/basic_client.py
```

For Docker Compose setup:

```bash
docker-compose -f examples/docker-compose.yml up
```