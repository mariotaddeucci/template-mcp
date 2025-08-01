"""Configuration management for Template MCP server using Pydantic Settings."""

import os
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class LoggingConfig(BaseSettings):
    """Logging configuration."""

    model_config = SettingsConfigDict(
        env_prefix="LOG_",
        case_sensitive=False,
    )

    level: str = Field(default="INFO", description="Log level")
    format: str = Field(default="json", description="Log format: json or detailed")
    file_enabled: bool = Field(default=True, description="Enable file logging")
    file_path: str = Field(default="logs/mcp_server.log", description="Log file path")
    console_enabled: bool = Field(default=True, description="Enable console logging")


class EunomiaConfig(BaseSettings):
    """Eunomia authorization configuration."""

    model_config = SettingsConfigDict(
        env_prefix="EUNOMIA_",
        case_sensitive=False,
    )

    server_url: str = Field(default="http://localhost:8000", description="Eunomia authorization server URL")
    policies_file: str = Field(default="configs/eunomia_policies.json", description="Path to policies file")
    timeout: int = Field(default=30, description="Request timeout in seconds")
    enabled: bool = Field(default=True, description="Enable Eunomia authorization")


class McpServerConfig(BaseSettings):
    """MCP server configuration."""

    model_config = SettingsConfigDict(
        env_prefix="MCP_SERVER_",
        case_sensitive=False,
    )

    name: str = Field(default="template-mcp", description="Server name")
    version: str = Field(default="0.1.0", description="Server version")
    port: int = Field(default=3000, description="Server port")
    host: str = Field(default="localhost", description="Server host")
    debug: bool = Field(default=False, description="Enable debug mode")


class AppConfig(BaseSettings):
    """Main application configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        case_sensitive=False,
        extra="ignore",  # Ignore extra fields instead of forbidding them
    )

    # Environment
    environment: str = Field(default="development", description="Application environment")

    # Nested configurations
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    eunomia: EunomiaConfig = Field(default_factory=EunomiaConfig)
    mcp_server: McpServerConfig = Field(default_factory=McpServerConfig)

    def __init__(self, **kwargs):
        """Initialize configuration with environment-specific settings."""
        # Determine environment and load appropriate .env file
        env = kwargs.get("environment", os.getenv("ENVIRONMENT", "development"))

        # Map environment to .env file
        env_files = {"development": ".env.dev", "testing": ".env.test", "production": ".env.prod"}

        # Set the env_file based on environment
        if env in env_files:
            env_file = env_files[env]
            if Path(env_file).exists():
                self.model_config["env_file"] = env_file

        super().__init__(**kwargs)

    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.environment.lower() in ("development", "dev")

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment.lower() in ("production", "prod")

    @property
    def is_testing(self) -> bool:
        """Check if running in testing environment."""
        return self.environment.lower() in ("testing", "test")


# Global configuration instance
_config: AppConfig | None = None


def get_config() -> AppConfig:
    """Get the global configuration instance."""
    global _config
    if _config is None:
        _config = AppConfig()
    return _config


def set_config(config: AppConfig) -> None:
    """Set the global configuration instance."""
    global _config
    _config = config


def load_config(environment: str | None = None) -> AppConfig:
    """Load configuration for the specified environment."""
    config = AppConfig(environment=environment) if environment else AppConfig()
    set_config(config)
    return config
