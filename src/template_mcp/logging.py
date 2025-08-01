"""Structured logging setup for Template MCP server using loguru and structlog."""

import logging
import sys
from pathlib import Path
from typing import Any

import structlog
from loguru import logger

from .config import LoggingConfig
from .models import AuditLogEntry


class LoguruHandler(logging.Handler):
    """Handler to bridge Python's logging to loguru."""

    def emit(self, record: logging.LogRecord) -> None:
        """Emit a log record using loguru."""
        # Get corresponding loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where the logging call was made
        frame, depth = sys._getframe(6), 6
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_structlog() -> None:
    """Configure structlog for structured logging."""
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="ISO"),
            structlog.dev.ConsoleRenderer() if sys.stdout.isatty() else structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        logger_factory=structlog.WriteLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def setup_logging(config: LoggingConfig) -> None:
    """Setup logging configuration using loguru and structlog."""
    # Remove default loguru handler
    logger.remove()

    # Setup console logging if enabled
    if config.console_enabled:
        if config.format == "json":
            logger.add(
                sys.stdout,
                level=config.level.upper(),
                format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {name}:{function}:{line} | {message}",
                serialize=True,
                enqueue=True,
            )
        else:
            logger.add(
                sys.stdout,
                level=config.level.upper(),
                format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
                "<level>{level: <8}</level> | "
                "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
                "<level>{message}</level>",
                enqueue=True,
            )

    # Setup file logging if enabled
    if config.file_enabled:
        # Ensure log directory exists
        log_path = Path(config.file_path)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        logger.add(
            config.file_path,
            level=config.level.upper(),
            format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {name}:{function}:{line} | {message}",
            rotation="1 day",
            retention="30 days",
            compression="gz",
            serialize=True,
            enqueue=True,
        )

    # Bridge Python's logging to loguru
    logging.basicConfig(handlers=[LoguruHandler()], level=0, force=True)

    # Setup structlog
    setup_structlog()


def get_logger(name: str) -> Any:
    """Get a logger instance with the given name."""
    # Bind the logger name for better tracking
    return logger.bind(logger_name=name)


def get_structured_logger(name: str) -> Any:
    """Get a structured logger instance."""
    return structlog.get_logger(name)


class AuditLogger:
    """Specialized logger for audit events."""

    def __init__(self):
        """Initialize audit logger."""
        self._logger = get_logger("audit")
        self._structured_logger = get_structured_logger("audit")

    def log_tool_execution(
        self,
        tool_name: str,
        user_id: str | None,
        user_role: str | None,
        result: str,
        execution_time_ms: float | None = None,
        error_message: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Log tool execution for audit purposes."""
        audit_data = {
            "event_type": "tool_execution",
            "tool_name": tool_name,
            "user_id": user_id,
            "user_role": user_role,
            "result": result,
            "execution_time_ms": execution_time_ms,
            "error_message": error_message,
            **kwargs,
        }

        self._structured_logger.info("Tool execution", **audit_data)

        # Also log via regular logger for file output
        self._logger.info(
            f"Tool execution: {tool_name} by {user_id or 'anonymous'} ({user_role or 'unknown'}) - {result}"
        )

    def log_authorization_check(
        self, user_id: str | None, user_role: str | None, resource: str, action: str, result: str, **kwargs: Any
    ) -> None:
        """Log authorization check for audit purposes."""
        audit_data = {
            "event_type": "authorization_check",
            "user_id": user_id,
            "user_role": user_role,
            "resource": resource,
            "action": action,
            "result": result,
            **kwargs,
        }

        self._structured_logger.info("Authorization check", **audit_data)

        self._logger.info(
            f"Authorization check: {user_id or 'anonymous'} "
            f"({user_role or 'unknown'}) {action} on {resource} - {result}"
        )

    def log_server_event(self, event_type: str, description: str, **kwargs: Any) -> None:
        """Log server events for audit purposes."""
        audit_data = {"event_type": event_type, "description": description, **kwargs}

        self._structured_logger.info("Server event", **audit_data)
        self._logger.info(f"Server event: {event_type} - {description}")

    def log_audit_entry(self, entry: AuditLogEntry) -> None:
        """Log a complete audit entry."""
        audit_data = entry.model_dump()

        self._structured_logger.info(
            "Audit entry",
            event_id=entry.event_id,
            event_type=entry.event_type,
            user_id=entry.user_id,
            user_role=entry.user_role.value if entry.user_role else None,
            resource=entry.resource,
            action=entry.action,
            result=entry.result,
            timestamp=entry.timestamp.isoformat(),
            ip_address=entry.ip_address,
            additional_data=entry.additional_data,
        )

        self._logger.info(
            f"Audit: {entry.event_type} - {entry.user_id or 'anonymous'} "
            f"{entry.action} on {entry.resource} - {entry.result}"
        )


# Global audit logger instance
_audit_logger: AuditLogger | None = None


def get_audit_logger() -> AuditLogger:
    """Get the global audit logger instance."""
    global _audit_logger
    if _audit_logger is None:
        _audit_logger = AuditLogger()
    return _audit_logger


def log_startup(server_name: str, version: str, port: int) -> None:
    """Log server startup information."""
    logger.info(f"Starting {server_name} v{version} on port {port}")
    get_audit_logger().log_server_event(
        "server_startup",
        f"Server {server_name} v{version} starting on port {port}",
        server_name=server_name,
        version=version,
        port=port,
    )


def log_shutdown(server_name: str) -> None:
    """Log server shutdown information."""
    logger.info(f"Shutting down {server_name}")
    get_audit_logger().log_server_event(
        "server_shutdown",
        f"Server {server_name} shutting down",
        server_name=server_name,
    )
