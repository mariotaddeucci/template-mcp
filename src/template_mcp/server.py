"""FastMCP server implementation with Eunomia middleware integration."""

import asyncio
import time
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4

from fastmcp import FastMCP
from fastmcp.tools import Tool
from eunomia_ai.mcp_middleware import EunomiaMcpMiddleware

from .config import AppConfig, get_config
from .logging import get_audit_logger, get_logger
from .models import (
    HelloRequest,
    HelloResponse,
    ServerInfo,
    ToolRequest,
    ToolResponse,
    ToolStatus,
    UserRole,
)


class TemplateMcpServer:
    """Template MCP Server with FastMCP and Eunomia authorization."""
    
    def __init__(self, config: Optional[AppConfig] = None):
        """Initialize the MCP server."""
        self.config = config or get_config()
        self.logger = get_logger(__name__)
        self.audit_logger = get_audit_logger()
        self.start_time = time.time()
        self.request_count = 0
        
        # Initialize FastMCP server
        self.app = FastMCP(
            name=self.config.mcp_server.name,
            version=self.config.mcp_server.version,
        )
        
        # Add Eunomia middleware integration in one line as required
        self.app.add_middleware(EunomiaMcpMiddleware())
        
        # Register tools
        self._register_tools()
        
        self.logger.info(
            f"Initialized {self.config.mcp_server.name} v{self.config.mcp_server.version}"
        )
    
    def _register_tools(self) -> None:
        """Register all available tools."""
        # Register hello tool
        hello_tool = Tool(
            name="hello",
            description="Simple greeting tool that says hello to a user",
            input_schema=HelloRequest.model_json_schema(),
        )
        
        @hello_tool.call
        async def hello_handler(request: Dict[str, Any]) -> Dict[str, Any]:
            """Handle hello tool requests."""
            return await self._handle_hello_tool(request)
        
        self.app.add_tool(hello_tool)
        
        # Register server info tool
        info_tool = Tool(
            name="server_info",
            description="Get server information and status",
            input_schema={
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
        )
        
        @info_tool.call
        async def info_handler(request: Dict[str, Any]) -> Dict[str, Any]:
            """Handle server info requests."""
            return await self._handle_server_info_tool(request)
        
        self.app.add_tool(info_tool)
        
        self.logger.info("Registered tools: hello, server_info")
    
    async def _handle_hello_tool(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle hello tool execution."""
        start_time = time.time()
        user_id = request.get("user_id")
        user_role = request.get("user_role", UserRole.GUEST)
        
        try:
            # Extract and validate parameters
            params = request.get("params", {})
            hello_request = HelloRequest(**params)
            
            # Generate greeting based on language
            greetings = {
                "en": f"Hello, {hello_request.name}!",
                "es": f"¡Hola, {hello_request.name}!",
                "fr": f"Bonjour, {hello_request.name}!",
                "de": f"Hallo, {hello_request.name}!",
                "pt": f"Olá, {hello_request.name}!",
                "it": f"Ciao, {hello_request.name}!",
            }
            
            greeting = greetings.get(hello_request.language, greetings["en"])
            
            # Create response
            hello_response = HelloResponse(
                greeting=greeting,
                name=hello_request.name,
                language=hello_request.language,
            )
            
            # Format response based on requested format
            if hello_request.format == "json":
                result = hello_response.model_dump()
            elif hello_request.format == "html":
                result = f"<h1>{greeting}</h1><p>Welcome, <strong>{hello_request.name}</strong>!</p>"
            else:  # plain text
                result = greeting
            
            execution_time = (time.time() - start_time) * 1000
            
            # Log successful execution
            self.audit_logger.log_tool_execution(
                tool_name="hello",
                user_id=user_id,
                user_role=user_role,
                result="success",
                execution_time_ms=execution_time,
                greeting_language=hello_request.language,
                greeting_format=hello_request.format,
            )
            
            self.request_count += 1
            
            return {
                "content": [
                    {
                        "type": "text",
                        "text": result if isinstance(result, str) else str(result),
                    }
                ]
            }
            
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            error_msg = str(e)
            
            self.logger.error(f"Error in hello tool: {error_msg}")
            self.audit_logger.log_tool_execution(
                tool_name="hello",
                user_id=user_id,
                user_role=user_role,
                result="error",
                execution_time_ms=execution_time,
                error_message=error_msg,
            )
            
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Error: {error_msg}",
                    }
                ],
                "isError": True,
            }
    
    async def _handle_server_info_tool(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle server info tool execution."""
        start_time = time.time()
        user_id = request.get("user_id")
        user_role = request.get("user_role", UserRole.GUEST)
        
        try:
            # Calculate uptime
            uptime_seconds = time.time() - self.start_time
            
            # Create server info
            server_info = ServerInfo(
                name=self.config.mcp_server.name,
                version=self.config.mcp_server.version,
                status="running",
                uptime_seconds=uptime_seconds,
                total_requests=self.request_count,
                active_connections=1,  # Simplified for this implementation
                capabilities=["hello", "server_info"],
            )
            
            execution_time = (time.time() - start_time) * 1000
            
            # Log successful execution
            self.audit_logger.log_tool_execution(
                tool_name="server_info",
                user_id=user_id,
                user_role=user_role,
                result="success",
                execution_time_ms=execution_time,
            )
            
            return {
                "content": [
                    {
                        "type": "text",
                        "text": server_info.model_dump_json(indent=2),
                    }
                ]
            }
            
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            error_msg = str(e)
            
            self.logger.error(f"Error in server_info tool: {error_msg}")
            self.audit_logger.log_tool_execution(
                tool_name="server_info",
                user_id=user_id,
                user_role=user_role,
                result="error",
                execution_time_ms=execution_time,
                error_message=error_msg,
            )
            
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Error: {error_msg}",
                    }
                ],
                "isError": True,
            }
    
    async def start_server(self) -> None:
        """Start the MCP server."""
        try:
            self.logger.info(
                f"Starting {self.config.mcp_server.name} server on "
                f"{self.config.mcp_server.host}:{self.config.mcp_server.port}"
            )
            
            self.audit_logger.log_server_event(
                "server_start",
                f"MCP server starting on {self.config.mcp_server.host}:{self.config.mcp_server.port}",
                host=self.config.mcp_server.host,
                port=self.config.mcp_server.port,
            )
            
            # Start the FastMCP server
            await self.app.run(
                transport="stdio"  # MCP typically uses stdio transport
            )
            
        except Exception as e:
            self.logger.error(f"Failed to start server: {e}")
            self.audit_logger.log_server_event(
                "server_start_failed",
                f"Failed to start MCP server: {e}",
                error=str(e),
            )
            raise
    
    async def stop_server(self) -> None:
        """Stop the MCP server."""
        self.logger.info(f"Stopping {self.config.mcp_server.name} server")
        self.audit_logger.log_server_event(
            "server_stop",
            "MCP server stopping",
        )
        
        # Cleanup if needed
        # FastMCP handles the cleanup automatically
    
    def get_server_stats(self) -> Dict[str, Any]:
        """Get current server statistics."""
        uptime_seconds = time.time() - self.start_time
        
        return {
            "name": self.config.mcp_server.name,
            "version": self.config.mcp_server.version,
            "uptime_seconds": uptime_seconds,
            "total_requests": self.request_count,
            "start_time": datetime.fromtimestamp(self.start_time).isoformat(),
            "status": "running",
        }


async def create_server(config: Optional[AppConfig] = None) -> TemplateMcpServer:
    """Create and initialize the MCP server."""
    return TemplateMcpServer(config)


async def run_server(config: Optional[AppConfig] = None) -> None:
    """Run the MCP server."""
    server = await create_server(config)
    
    try:
        await server.start_server()
    except KeyboardInterrupt:
        server.logger.info("Received shutdown signal")
    finally:
        await server.stop_server()