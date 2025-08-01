"""Tests for the Template MCP package."""

from template_mcp import __version__


def test_version():
    """Test that version is correctly defined."""
    assert __version__ == "0.1.0"


def test_import():
    """Test that the package can be imported."""
    import template_mcp

    assert template_mcp is not None
