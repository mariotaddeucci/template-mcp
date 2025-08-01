#!/usr/bin/env python3
"""Example MCP client for testing Template MCP server functionality."""

import asyncio
import json
import sys
from typing import Any, Dict


class SimpleMcpClient:
    """Simple MCP client for testing purposes."""
    
    def __init__(self):
        """Initialize the client."""
        self.request_id = 0
    
    def _create_request(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create a JSON-RPC request."""
        self.request_id += 1
        return {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method,
            "params": params,
        }
    
    def test_hello_tool(self) -> Dict[str, Any]:
        """Test the hello tool."""
        return self._create_request(
            "tools/call",
            {
                "name": "hello",
                "arguments": {
                    "name": "World",
                    "language": "en",
                    "format": "plain"
                }
            }
        )
    
    def test_hello_tool_spanish(self) -> Dict[str, Any]:
        """Test the hello tool with Spanish."""
        return self._create_request(
            "tools/call",
            {
                "name": "hello",
                "arguments": {
                    "name": "Mundo",
                    "language": "es",
                    "format": "plain"
                }
            }
        )
    
    def test_hello_tool_json_format(self) -> Dict[str, Any]:
        """Test the hello tool with JSON format."""
        return self._create_request(
            "tools/call",
            {
                "name": "hello",
                "arguments": {
                    "name": "Alice",
                    "language": "en",
                    "format": "json"
                }
            }
        )
    
    def test_server_info_tool(self) -> Dict[str, Any]:
        """Test the server info tool."""
        return self._create_request(
            "tools/call",
            {
                "name": "server_info",
                "arguments": {}
            }
        )
    
    def list_tools(self) -> Dict[str, Any]:
        """List available tools."""
        return self._create_request(
            "tools/list",
            {}
        )


async def basic_client_example():
    """Demonstrate client usage."""
    print("🚀 Template MCP Client Example")
    print("=" * 40)
    
    client = SimpleMcpClient()
    
    # Example requests
    test_requests = [
        ("List Tools", client.list_tools()),
        ("Hello Tool (English)", client.test_hello_tool()),
        ("Hello Tool (Spanish)", client.test_hello_tool_spanish()),
        ("Hello Tool (JSON)", client.test_hello_tool_json_format()),
        ("Server Info", client.test_server_info_tool()),
    ]
    
    for description, request in test_requests:
        print(f"\n📝 {description}:")
        print("-" * (len(description) + 4))
        print(json.dumps(request, indent=2))
    
    print("\n" + "=" * 40)
    print("📋 To use these requests:")
    print("1. Start the Template MCP server: python -m template_mcp")
    print("2. Send these JSON-RPC requests via stdio or HTTP")
    print("3. The server will respond with appropriate results")
    print("✅ Example completed")


if __name__ == "__main__":
    asyncio.run(basic_client_example())
