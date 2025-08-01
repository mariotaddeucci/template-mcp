"""Test configuration and fixtures for Template MCP tests."""

import asyncio

import pytest


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def sample_config():
    """Sample configuration for testing."""
    return {"eunomia_server_url": "http://localhost:8000", "mcp_server_port": 3000, "log_level": "DEBUG"}
