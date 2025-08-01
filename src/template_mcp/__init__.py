"""Template MCP - Secure MCP Server with FastMCP and Eunomia Authorization."""

from .config import AppConfig, get_config, load_config
from .main import main, sync_main
from .models import (
    HelloRequest,
    HelloResponse,
    ToolRequest,
    ToolResponse,
    ToolStatus,
    UserRole,
)
from .server import TemplateMcpServer, create_server, run_server

__version__ = "0.1.0"
__all__ = [
    "AppConfig",
    "get_config",
    "load_config",
    "main",
    "sync_main",
    "HelloRequest",
    "HelloResponse",
    "ToolRequest",
    "ToolResponse",
    "ToolStatus",
    "UserRole",
    "TemplateMcpServer",
    "create_server",
    "run_server",
]
