"""Tests for the Template MCP package."""

import pytest

from template_mcp import __version__


def test_version():
    """Test that version is correctly defined."""
    assert __version__ == "0.1.0"


def test_import():
    """Test that the package can be imported."""
    import template_mcp

    assert template_mcp is not None


def test_main_imports():
    """Test that main components can be imported."""
    from template_mcp import (
        AppConfig,
        get_config,
        HelloRequest,
        HelloResponse,
        TemplateMcpServer,
        ToolStatus,
        UserRole,
    )
    
    # Test that classes can be instantiated
    assert AppConfig is not None
    assert get_config() is not None
    assert HelloRequest is not None
    assert HelloResponse is not None
    assert TemplateMcpServer is not None
    assert ToolStatus.SUCCESS == "success"
    assert UserRole.ADMIN == "admin"


@pytest.mark.asyncio
async def test_main_function_import():
    """Test that main function can be imported."""
    from template_mcp import main, sync_main
    
    assert main is not None
    assert sync_main is not None
    # Note: We don't actually run main() as it would start the server
