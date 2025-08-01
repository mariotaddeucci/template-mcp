"""Tests for Pydantic models."""

from datetime import datetime

import pytest
from pydantic import ValidationError

from template_mcp.models import (
    AuditLogEntry,
    ErrorDetails,
    HelloRequest,
    HelloResponse,
    ServerInfo,
    ToolRequest,
    ToolResponse,
    ToolStatus,
    UserRole,
)


class TestHelloRequest:
    """Test HelloRequest model."""

    def test_valid_request(self):
        """Test valid hello request."""
        request = HelloRequest(
            name="John Doe",
            language="en",
            format="plain",
        )

        assert request.name == "John Doe"
        assert request.language == "en"
        assert request.format == "plain"

    def test_default_values(self):
        """Test default values for hello request."""
        request = HelloRequest(name="Alice")

        assert request.name == "Alice"
        assert request.language == "en"
        assert request.format == "plain"

    def test_name_validation(self):
        """Test name validation."""
        # Valid names
        HelloRequest(name="John")
        HelloRequest(name="  Mary  ")  # Whitespace should be stripped
        HelloRequest(name="José-Carlos")

        # Invalid names
        with pytest.raises(ValidationError):
            HelloRequest(name="")

        with pytest.raises(ValidationError):
            HelloRequest(name="123")  # No letters

    def test_language_validation(self):
        """Test language code validation."""
        # Valid language codes
        HelloRequest(name="John", language="en")
        HelloRequest(name="John", language="pt")
        HelloRequest(name="John", language="fr")

        # Invalid language codes
        with pytest.raises(ValidationError):
            HelloRequest(name="John", language="english")  # Too long

        with pytest.raises(ValidationError):
            HelloRequest(name="John", language="E")  # Too short

        with pytest.raises(ValidationError):
            HelloRequest(name="John", language="EN")  # Uppercase not allowed

    def test_format_validation(self):
        """Test format validation."""
        # Valid formats
        HelloRequest(name="John", format="plain")
        HelloRequest(name="John", format="json")
        HelloRequest(name="John", format="html")

        # Invalid format
        with pytest.raises(ValidationError):
            HelloRequest(name="John", format="xml")

    def test_name_cleaning(self):
        """Test name whitespace cleaning."""
        request = HelloRequest(name="  John Doe  ")
        assert request.name == "John Doe"


class TestHelloResponse:
    """Test HelloResponse model."""

    def test_valid_response(self):
        """Test valid hello response."""
        response = HelloResponse(
            greeting="Hello, John!",
            name="John",
            language="en",
        )

        assert response.greeting == "Hello, John!"
        assert response.name == "John"
        assert response.language == "en"
        assert isinstance(response.timestamp, datetime)


class TestToolRequest:
    """Test ToolRequest model."""

    def test_valid_request(self):
        """Test valid tool request."""
        request = ToolRequest(
            tool_name="hello",
            parameters={"name": "John", "language": "en"},
            user_id="user123",
            user_role=UserRole.USER,
        )

        assert request.tool_name == "hello"
        assert request.parameters == {"name": "John", "language": "en"}
        assert request.user_id == "user123"
        assert request.user_role == UserRole.USER
        assert isinstance(request.timestamp, datetime)

    def test_default_values(self):
        """Test default values for tool request."""
        request = ToolRequest(tool_name="test_tool")

        assert request.tool_name == "test_tool"
        assert request.parameters == {}
        assert request.user_id is None
        assert request.user_role == UserRole.GUEST

    def test_tool_name_validation(self):
        """Test tool name validation and normalization."""
        # Valid tool names
        request1 = ToolRequest(tool_name="hello")
        assert request1.tool_name == "hello"

        request2 = ToolRequest(tool_name="HELLO_WORLD")
        assert request2.tool_name == "hello_world"

        request3 = ToolRequest(tool_name="tool-name-123")
        assert request3.tool_name == "tool-name-123"

        # Invalid tool names
        with pytest.raises(ValidationError):
            ToolRequest(tool_name="")

        with pytest.raises(ValidationError):
            ToolRequest(tool_name="tool@name")  # Special characters


class TestToolResponse:
    """Test ToolResponse model."""

    def test_valid_success_response(self):
        """Test valid success response."""
        response = ToolResponse(
            tool_name="hello",
            status=ToolStatus.SUCCESS,
            result={"greeting": "Hello, World!"},
            execution_time_ms=15.5,
        )

        assert response.tool_name == "hello"
        assert response.status == ToolStatus.SUCCESS
        assert response.result == {"greeting": "Hello, World!"}
        assert response.execution_time_ms == 15.5
        assert response.error_message is None

    def test_valid_error_response(self):
        """Test valid error response."""
        response = ToolResponse(
            tool_name="hello",
            status=ToolStatus.ERROR,
            error_message="Tool execution failed",
            execution_time_ms=5.0,
        )

        assert response.tool_name == "hello"
        assert response.status == ToolStatus.ERROR
        assert response.error_message == "Tool execution failed"
        assert response.result is None

    def test_error_message_validation(self):
        """Test error message validation."""
        # Error message required when status is ERROR
        with pytest.raises(ValidationError):
            ToolResponse(
                tool_name="hello",
                status=ToolStatus.ERROR,
                # Missing error_message
            )

        # Error message not required for success
        ToolResponse(
            tool_name="hello",
            status=ToolStatus.SUCCESS,
            result="Success!",
        )


class TestServerInfo:
    """Test ServerInfo model."""

    def test_valid_server_info(self):
        """Test valid server info."""
        info = ServerInfo(
            name="template-mcp",
            version="0.1.0",
            status="running",
            uptime_seconds=3600.5,
            total_requests=42,
            active_connections=3,
            capabilities=["hello", "server_info"],
        )

        assert info.name == "template-mcp"
        assert info.version == "0.1.0"
        assert info.status == "running"
        assert info.uptime_seconds == 3600.5
        assert info.total_requests == 42
        assert info.active_connections == 3
        assert info.capabilities == ["hello", "server_info"]

    def test_status_validation(self):
        """Test status validation."""
        # Valid statuses
        for status in ["starting", "running", "stopping", "stopped", "error"]:
            ServerInfo(
                name="test",
                version="1.0.0",
                status=status,
                uptime_seconds=0,
            )

        # Invalid status
        with pytest.raises(ValidationError):
            ServerInfo(
                name="test",
                version="1.0.0",
                status="invalid_status",
                uptime_seconds=0,
            )


class TestAuditLogEntry:
    """Test AuditLogEntry model."""

    def test_valid_audit_entry(self):
        """Test valid audit log entry."""
        entry = AuditLogEntry(
            event_id="evt_123",
            event_type="tool_execution",
            user_id="user123",
            user_role=UserRole.USER,
            resource="tools/hello",
            action="execute",
            result="success",
            ip_address="192.168.1.1",
        )

        assert entry.event_id == "evt_123"
        assert entry.event_type == "tool_execution"
        assert entry.user_id == "user123"
        assert entry.user_role == UserRole.USER
        assert entry.resource == "tools/hello"
        assert entry.action == "execute"
        assert entry.result == "success"
        assert entry.ip_address == "192.168.1.1"

    def test_result_validation(self):
        """Test result validation."""
        # Valid results
        for result in ["success", "failure", "denied", "error"]:
            AuditLogEntry(
                event_id="evt_123",
                event_type="test",
                resource="test",
                action="test",
                result=result,
            )

        # Invalid result
        with pytest.raises(ValidationError):
            AuditLogEntry(
                event_id="evt_123",
                event_type="test",
                resource="test",
                action="test",
                result="invalid_result",
            )


class TestErrorDetails:
    """Test ErrorDetails model."""

    def test_valid_error_details(self):
        """Test valid error details."""
        error = ErrorDetails(
            error_code="TOOL_EXEC_001",
            error_message="Tool execution failed",
            error_type="execution_error",
            correlation_id="req_abc123",
            stack_trace="Traceback...",
            context={"tool_name": "hello", "user_id": "user123"},
        )

        assert error.error_code == "TOOL_EXEC_001"
        assert error.error_message == "Tool execution failed"
        assert error.error_type == "execution_error"
        assert error.correlation_id == "req_abc123"
        assert error.stack_trace == "Traceback..."
        assert error.context == {"tool_name": "hello", "user_id": "user123"}

    def test_error_code_validation(self):
        """Test error code validation and normalization."""
        error = ErrorDetails(
            error_code="tool_exec_001",
            error_message="Test error",
            error_type="test",
        )

        assert error.error_code == "TOOL_EXEC_001"  # Should be uppercase

        # Invalid error code
        with pytest.raises(ValidationError):
            ErrorDetails(
                error_code="tool@exec@001",  # Special characters
                error_message="Test error",
                error_type="test",
            )
