"""Pydantic models for Template MCP server business data."""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator


class ToolStatus(str, Enum):
    """Tool execution status."""

    SUCCESS = "success"
    ERROR = "error"
    PENDING = "pending"


class LogLevel(str, Enum):
    """Log levels."""

    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class UserRole(str, Enum):
    """User roles for authorization."""

    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


class ToolRequest(BaseModel):
    """Model for tool execution requests."""

    tool_name: str = Field(..., description="Name of the tool to execute", min_length=1, max_length=100)
    parameters: dict[str, Any] = Field(default_factory=dict, description="Tool parameters")
    user_id: str | None = Field(None, description="ID of the user making the request", max_length=255)
    user_role: UserRole = Field(default=UserRole.GUEST, description="Role of the user making the request")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Request timestamp")

    @field_validator("tool_name")
    @classmethod
    def validate_tool_name(cls, v: str) -> str:
        """Validate tool name format."""
        if not v.replace("_", "").replace("-", "").isalnum():
            raise ValueError("Tool name must contain only alphanumeric characters, hyphens, and underscores")
        return v.lower()


class ToolResponse(BaseModel):
    """Model for tool execution responses."""

    tool_name: str = Field(..., description="Name of the executed tool")
    status: ToolStatus = Field(..., description="Execution status")
    result: Any | None = Field(None, description="Tool execution result")
    error_message: str | None = Field(None, description="Error message if execution failed")
    execution_time_ms: float | None = Field(None, description="Execution time in milliseconds", ge=0)
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

    @field_validator("error_message")
    @classmethod
    def validate_error_message(cls, v: str | None, info) -> str | None:
        """Ensure error message is present when status is ERROR."""
        if hasattr(info, "data") and info.data and info.data.get("status") == ToolStatus.ERROR and not v:
            raise ValueError("Error message is required when status is ERROR")
        return v

    @model_validator(mode="after")
    def validate_error_status(self) -> "ToolResponse":
        """Ensure error message is provided when status is ERROR."""
        if self.status == ToolStatus.ERROR and not self.error_message:
            raise ValueError("Error message is required when status is ERROR")
        return self


class HelloRequest(BaseModel):
    """Model for hello tool request parameters."""

    name: str = Field(..., description="Name to greet", min_length=1, max_length=100)
    language: str = Field(default="en", description="Language for greeting", pattern="^[a-z]{2}$")
    format: str = Field(default="plain", description="Response format", pattern="^(plain|json|html)$")

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate and clean the name."""
        # Remove extra whitespace and ensure it contains at least one letter
        cleaned = v.strip()
        if not any(c.isalpha() for c in cleaned):
            raise ValueError("Name must contain at least one letter")
        return cleaned


class HelloResponse(BaseModel):
    """Model for hello tool response."""

    greeting: str = Field(..., description="Generated greeting message")
    name: str = Field(..., description="Name that was greeted")
    language: str = Field(..., description="Language used for greeting")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")


class AuditLogEntry(BaseModel):
    """Model for audit log entries."""

    event_id: str = Field(..., description="Unique event identifier")
    event_type: str = Field(..., description="Type of event", max_length=50)
    user_id: str | None = Field(None, description="User identifier", max_length=255)
    user_role: UserRole | None = Field(None, description="User role")
    resource: str = Field(..., description="Resource accessed", max_length=255)
    action: str = Field(..., description="Action performed", max_length=50)
    result: str = Field(..., description="Action result", max_length=20)
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Event timestamp")
    ip_address: str | None = Field(None, description="Client IP address", max_length=45)
    user_agent: str | None = Field(None, description="Client user agent", max_length=500)
    additional_data: dict[str, Any] = Field(default_factory=dict, description="Additional event data")

    @field_validator("result")
    @classmethod
    def validate_result(cls, v: str) -> str:
        """Validate result values."""
        allowed_results = {"success", "failure", "denied", "error"}
        if v.lower() not in allowed_results:
            raise ValueError(f"Result must be one of: {', '.join(allowed_results)}")
        return v.lower()


class ServerInfo(BaseModel):
    """Model for server information."""

    name: str = Field(..., description="Server name")
    version: str = Field(..., description="Server version")
    status: str = Field(..., description="Server status")
    uptime_seconds: float = Field(..., description="Server uptime in seconds", ge=0)
    total_requests: int = Field(default=0, description="Total number of requests processed", ge=0)
    active_connections: int = Field(default=0, description="Number of active connections", ge=0)
    last_restart: datetime = Field(default_factory=datetime.utcnow, description="Last server restart time")
    capabilities: list[str] = Field(default_factory=list, description="Server capabilities")

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        """Validate server status."""
        allowed_statuses = {"starting", "running", "stopping", "stopped", "error"}
        if v.lower() not in allowed_statuses:
            raise ValueError(f"Status must be one of: {', '.join(allowed_statuses)}")
        return v.lower()


class ErrorDetails(BaseModel):
    """Model for detailed error information."""

    error_code: str = Field(..., description="Error code", max_length=20)
    error_message: str = Field(..., description="Human-readable error message")
    error_type: str = Field(..., description="Type/category of error", max_length=50)
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Error timestamp")
    correlation_id: str | None = Field(None, description="Request correlation ID", max_length=100)
    stack_trace: str | None = Field(None, description="Stack trace for debugging")
    context: dict[str, Any] = Field(default_factory=dict, description="Additional error context")

    @field_validator("error_code")
    @classmethod
    def validate_error_code(cls, v: str) -> str:
        """Validate error code format."""
        if not v.replace("_", "").replace("-", "").isalnum():
            raise ValueError("Error code must contain only alphanumeric characters, hyphens, and underscores")
        return v.upper()
