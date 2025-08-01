"""Tests for server initialization and basic functionality."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from template_mcp.config import AppConfig
from template_mcp.models import UserRole
from template_mcp.server import TemplateMcpServer


class TestTemplateMcpServer:
    """Test TemplateMcpServer class."""

    @pytest.fixture
    def mock_config(self):
        """Create a mock configuration."""
        config = AppConfig()
        config.mcp_server.name = "test-mcp"
        config.mcp_server.version = "0.1.0"
        config.mcp_server.host = "localhost"
        config.mcp_server.port = 3000
        return config

    @patch("template_mcp.server.FastMCP")
    @patch("template_mcp.server.EunomiaMcpMiddleware")
    def test_server_initialization(self, mock_middleware, mock_fastmcp, mock_config):
        """Test server initialization."""
        # Mock FastMCP instance
        mock_app = MagicMock()
        mock_fastmcp.return_value = mock_app

        # Mock middleware instance
        mock_middleware_instance = MagicMock()
        mock_middleware.return_value = mock_middleware_instance

        # Create server
        server = TemplateMcpServer(mock_config)

        # Verify FastMCP was initialized correctly
        mock_fastmcp.assert_called_once_with(
            name="test-mcp",
            version="0.1.0",
        )

        # Verify middleware was added
        mock_middleware.assert_called_once()
        mock_app.add_middleware.assert_called_once_with(mock_middleware_instance)

        # Verify server attributes
        assert server.config == mock_config
        assert server.app == mock_app
        assert server.request_count == 0

    @patch("template_mcp.server.FastMCP")
    @patch("template_mcp.server.EunomiaMcpMiddleware")
    def test_tools_registration(self, mock_middleware, mock_fastmcp, mock_config):
        """Test that tools are registered during initialization."""
        mock_app = MagicMock()
        mock_fastmcp.return_value = mock_app

        # Create server
        server = TemplateMcpServer(mock_config)

        # Verify server was created
        assert server is not None

        # Verify tools were registered using the @app.tool decorator
        # The exact number of calls depends on how FastMCP internal implementation works
        assert mock_app.tool.call_count == 2

        # Verify that the tool decorator was called (not checking specific details
        # since that's internal to FastMCP implementation)
        mock_app.tool.assert_called()

    @patch("template_mcp.server.FastMCP")
    @patch("template_mcp.server.EunomiaMcpMiddleware")
    @pytest.mark.asyncio
    async def test_hello_tool_success(self, mock_middleware, mock_fastmcp, mock_config):
        """Test successful hello tool execution."""
        mock_app = MagicMock()
        mock_fastmcp.return_value = mock_app

        server = TemplateMcpServer(mock_config)

        # Test hello tool with valid parameters
        request = {
            "params": {"name": "John", "language": "en", "format": "plain"},
            "user_id": "user123",
            "user_role": UserRole.USER,
        }

        result = await server._handle_hello_tool(request)

        # Verify response structure
        assert "content" in result
        assert len(result["content"]) == 1
        assert result["content"][0]["type"] == "text"
        assert "Hello, John!" in result["content"][0]["text"]
        assert "isError" not in result

        # Verify request counter was incremented
        assert server.request_count == 1

    @patch("template_mcp.server.FastMCP")
    @patch("template_mcp.server.EunomiaMcpMiddleware")
    @pytest.mark.asyncio
    async def test_hello_tool_different_languages(self, mock_middleware, mock_fastmcp, mock_config):
        """Test hello tool with different languages."""
        mock_app = MagicMock()
        mock_fastmcp.return_value = mock_app

        server = TemplateMcpServer(mock_config)

        # Test different languages
        test_cases = [
            ("en", "Hello, Alice!"),
            ("es", "¡Hola, Alice!"),
            ("fr", "Bonjour, Alice!"),
            ("pt", "Olá, Alice!"),
        ]

        for language, expected_greeting in test_cases:
            request = {"params": {"name": "Alice", "language": language, "format": "plain"}}

            result = await server._handle_hello_tool(request)

            assert expected_greeting in result["content"][0]["text"]

    @patch("template_mcp.server.FastMCP")
    @patch("template_mcp.server.EunomiaMcpMiddleware")
    @pytest.mark.asyncio
    async def test_hello_tool_json_format(self, mock_middleware, mock_fastmcp, mock_config):
        """Test hello tool with JSON format."""
        mock_app = MagicMock()
        mock_fastmcp.return_value = mock_app

        server = TemplateMcpServer(mock_config)

        request = {"params": {"name": "Bob", "language": "en", "format": "json"}}

        result = await server._handle_hello_tool(request)

        # For JSON format, the response should be a string representation of the JSON
        response_text = result["content"][0]["text"]
        assert "greeting" in response_text
        assert "name" in response_text
        assert "language" in response_text

    @patch("template_mcp.server.FastMCP")
    @patch("template_mcp.server.EunomiaMcpMiddleware")
    @pytest.mark.asyncio
    async def test_hello_tool_error_handling(self, mock_middleware, mock_fastmcp, mock_config):
        """Test hello tool error handling."""
        mock_app = MagicMock()
        mock_fastmcp.return_value = mock_app

        server = TemplateMcpServer(mock_config)

        # Test with invalid parameters
        request = {
            "params": {
                "name": "",  # Invalid empty name
                "language": "en",
                "format": "plain",
            }
        }

        result = await server._handle_hello_tool(request)

        # Verify error response
        assert "content" in result
        assert "Error:" in result["content"][0]["text"]
        assert result.get("isError") is True

    @patch("template_mcp.server.FastMCP")
    @patch("template_mcp.server.EunomiaMcpMiddleware")
    @pytest.mark.asyncio
    async def test_server_info_tool(self, mock_middleware, mock_fastmcp, mock_config):
        """Test server info tool."""
        mock_app = MagicMock()
        mock_fastmcp.return_value = mock_app

        server = TemplateMcpServer(mock_config)

        request = {"user_id": "admin", "user_role": UserRole.ADMIN}

        result = await server._handle_server_info_tool(request)

        # Verify response structure
        assert "content" in result
        assert len(result["content"]) == 1
        assert result["content"][0]["type"] == "text"

        # Verify server info contains expected fields
        response_text = result["content"][0]["text"]
        assert "test-mcp" in response_text
        assert "0.1.0" in response_text
        assert "running" in response_text
        assert "uptime_seconds" in response_text

    @patch("template_mcp.server.FastMCP")
    @patch("template_mcp.server.EunomiaMcpMiddleware")
    def test_get_server_stats(self, mock_middleware, mock_fastmcp, mock_config):
        """Test server statistics."""
        mock_app = MagicMock()
        mock_fastmcp.return_value = mock_app

        server = TemplateMcpServer(mock_config)
        server.request_count = 5

        stats = server.get_server_stats()

        # Verify stats structure
        assert stats["name"] == "test-mcp"
        assert stats["version"] == "0.1.0"
        assert stats["total_requests"] == 5
        assert stats["status"] == "running"
        assert "uptime_seconds" in stats
        assert "start_time" in stats


class TestServerFunctions:
    """Test module-level server functions."""

    @pytest.fixture
    def mock_config(self):
        """Create a mock configuration."""
        return AppConfig()

    @patch("template_mcp.server.TemplateMcpServer")
    @pytest.mark.asyncio
    async def test_create_server(self, mock_server_class, mock_config):
        """Test server creation function."""
        mock_server_instance = MagicMock()
        mock_server_class.return_value = mock_server_instance

        from template_mcp.server import create_server

        server = await create_server(mock_config)

        mock_server_class.assert_called_once_with(mock_config)
        assert server == mock_server_instance

    @patch("template_mcp.server.create_server")
    @pytest.mark.asyncio
    async def test_run_server(self, mock_create_server, mock_config):
        """Test run server function."""
        # Mock server instance
        mock_server = MagicMock()
        mock_server.start_server = AsyncMock()
        mock_server.stop_server = AsyncMock()
        mock_server.logger = MagicMock()
        mock_create_server.return_value = mock_server

        from template_mcp.server import run_server

        # Test normal execution
        await run_server(mock_config)

        mock_create_server.assert_called_once_with(mock_config)
        mock_server.start_server.assert_called_once()
        mock_server.stop_server.assert_called_once()

    @patch("template_mcp.server.create_server")
    @pytest.mark.asyncio
    async def test_run_server_keyboard_interrupt(self, mock_create_server, mock_config):
        """Test run server function with keyboard interrupt."""
        # Mock server instance
        mock_server = MagicMock()
        mock_server.start_server = AsyncMock(side_effect=KeyboardInterrupt())
        mock_server.stop_server = AsyncMock()
        mock_server.logger = MagicMock()
        mock_create_server.return_value = mock_server

        from template_mcp.server import run_server

        # Should handle KeyboardInterrupt gracefully
        await run_server(mock_config)

        mock_server.start_server.assert_called_once()
        mock_server.stop_server.assert_called_once()
        mock_server.logger.info.assert_called_with("Received shutdown signal")
