"""Tests for configuration management."""

import os
import tempfile
from pathlib import Path

import pytest

from template_mcp.config import AppConfig, EunomiaConfig, LoggingConfig, McpServerConfig, load_config


class TestLoggingConfig:
    """Test logging configuration."""
    
    def test_default_values(self):
        """Test default logging configuration values."""
        config = LoggingConfig()
        
        assert config.level == "INFO"
        assert config.format == "json"
        assert config.file_enabled is True
        assert config.file_path == "logs/mcp_server.log"
        assert config.console_enabled is True
    
    def test_custom_values(self):
        """Test custom logging configuration values."""
        config = LoggingConfig(
            level="DEBUG",
            format="detailed",
            file_enabled=False,
            console_enabled=False,
        )
        
        assert config.level == "DEBUG"
        assert config.format == "detailed"
        assert config.file_enabled is False
        assert config.console_enabled is False


class TestEunomiaConfig:
    """Test Eunomia configuration."""
    
    def test_default_values(self):
        """Test default Eunomia configuration values."""
        config = EunomiaConfig()
        
        assert config.server_url == "http://localhost:8000"
        assert config.policies_file == "configs/eunomia_policies.json"
        assert config.timeout == 30
        assert config.enabled is True
    
    def test_custom_values(self):
        """Test custom Eunomia configuration values."""
        config = EunomiaConfig(
            server_url="https://eunomia.example.com",
            policies_file="/custom/path/policies.json",
            timeout=60,
            enabled=False,
        )
        
        assert config.server_url == "https://eunomia.example.com"
        assert config.policies_file == "/custom/path/policies.json"
        assert config.timeout == 60
        assert config.enabled is False


class TestMcpServerConfig:
    """Test MCP server configuration."""
    
    def test_default_values(self):
        """Test default MCP server configuration values."""
        config = McpServerConfig()
        
        assert config.name == "template-mcp"
        assert config.version == "0.1.0"
        assert config.port == 3000
        assert config.host == "localhost"
        assert config.debug is False
    
    def test_custom_values(self):
        """Test custom MCP server configuration values."""
        config = McpServerConfig(
            name="custom-mcp",
            version="1.0.0",
            port=8080,
            host="0.0.0.0",
            debug=True,
        )
        
        assert config.name == "custom-mcp"
        assert config.version == "1.0.0"
        assert config.port == 8080
        assert config.host == "0.0.0.0"
        assert config.debug is True


class TestAppConfig:
    """Test main application configuration."""
    
    def test_default_values(self):
        """Test default application configuration values."""
        config = AppConfig()
        
        assert config.environment == "development"
        assert isinstance(config.logging, LoggingConfig)
        assert isinstance(config.eunomia, EunomiaConfig)
        assert isinstance(config.mcp_server, McpServerConfig)
    
    def test_environment_properties(self):
        """Test environment property methods."""
        dev_config = AppConfig(environment="development")
        assert dev_config.is_development is True
        assert dev_config.is_production is False
        assert dev_config.is_testing is False
        
        prod_config = AppConfig(environment="production")
        assert prod_config.is_development is False
        assert prod_config.is_production is True
        assert prod_config.is_testing is False
        
        test_config = AppConfig(environment="testing")
        assert test_config.is_development is False
        assert test_config.is_production is False
        assert test_config.is_testing is True
    
    def test_nested_config_override(self):
        """Test overriding nested configuration values."""
        config = AppConfig(
            logging=LoggingConfig(level="DEBUG"),
            mcp_server=McpServerConfig(port=9000),
        )
        
        assert config.logging.level == "DEBUG"
        assert config.mcp_server.port == 9000
        assert config.eunomia.server_url == "http://localhost:8000"  # Default


class TestConfigLoading:
    """Test configuration loading functionality."""
    
    def test_load_config_default(self):
        """Test loading default configuration."""
        config = load_config()
        
        assert isinstance(config, AppConfig)
        assert config.environment == "development"
    
    def test_load_config_with_environment(self):
        """Test loading configuration with specific environment."""
        config = load_config("production")
        
        assert config.environment == "production"
        assert config.is_production is True
    
    def test_environment_from_env_var(self, monkeypatch):
        """Test loading environment from environment variable."""
        monkeypatch.setenv("ENVIRONMENT", "testing")
        
        config = AppConfig()
        
        assert config.environment == "testing"
        assert config.is_testing is True