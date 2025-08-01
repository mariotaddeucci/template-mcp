"""Eunomia authorization middleware for FastMCP integration."""

import asyncio
import logging
from typing import Any, Dict, Optional

import httpx
import mcp.types as mt
from fastmcp.server.middleware import CallNext, Middleware, MiddlewareContext
from fastmcp.tools.tool import Tool

from .config import AppConfig

logger = logging.getLogger(__name__)


class EunomiaAuthMiddleware(Middleware):
    """Custom Eunomia authorization middleware for FastMCP."""

    def __init__(self, config: Optional[AppConfig] = None):
        """Initialize the Eunomia middleware."""
        super().__init__()
        self.config = config
        self.eunomia_url = config.eunomia.server_url if config else "http://localhost:8000"
        self.timeout = config.eunomia.timeout if config else 30
        self.enabled = config.eunomia.enabled if config else True

    async def on_call_tool(
        self,
        context: MiddlewareContext[mt.CallToolRequestParams],
        call_next: CallNext[mt.CallToolRequestParams, mt.CallToolResult],
    ) -> mt.CallToolResult:
        """Authorize tool calls with Eunomia."""
        if not self.enabled:
            return await call_next(context)

        # Extract tool name from request parameters
        tool_name = context.message.name

        # Extract user information from context
        user_role = self._extract_user_role(context)
        user_id = self._extract_user_id(context)
        agent_id = self._extract_agent_id(context)

        # Check authorization
        is_authorized = await self._check_authorization(
            user_role=user_role,
            user_id=user_id,
            agent_id=agent_id,
            action="tools/call",
            resource_attrs={"tool_name": tool_name}
        )

        if not is_authorized:
            logger.warning(
                f"Tool call denied: {user_role} user {user_id} cannot call tool {tool_name}"
            )
            # Return an error result instead of raising an exception
            return mt.CallToolResult(
                content=[
                    mt.TextContent(
                        type="text",
                        text=f"Access denied: {user_role} users cannot call tool '{tool_name}'"
                    )
                ],
                isError=True
            )

        logger.info(f"Tool call authorized: {user_role} user {user_id} calling tool {tool_name}")
        return await call_next(context)

    async def on_list_tools(
        self,
        context: MiddlewareContext[mt.ListToolsRequest],
        call_next: CallNext[mt.ListToolsRequest, list[Tool]],
    ) -> list[Tool]:
        """Filter tools list based on user permissions."""
        if not self.enabled:
            return await call_next(context)

        # Get the full tools list first
        all_tools = await call_next(context)

        # Extract user information
        user_role = self._extract_user_role(context)
        user_id = self._extract_user_id(context)
        agent_id = self._extract_agent_id(context)

        # Filter tools based on authorization
        authorized_tools = []
        for tool in all_tools:
            is_authorized = await self._check_authorization(
                user_role=user_role,
                user_id=user_id,
                agent_id=agent_id,
                action="tools/list",
                resource_attrs={"tool_name": tool.name}
            )
            
            if is_authorized:
                authorized_tools.append(tool)

        logger.info(
            f"Tools filtered for {user_role} user {user_id}: "
            f"{len(authorized_tools)}/{len(all_tools)} tools visible"
        )
        
        return authorized_tools

    async def on_read_resource(
        self,
        context: MiddlewareContext[mt.ReadResourceRequestParams],
        call_next: CallNext[mt.ReadResourceRequestParams, mt.ReadResourceResult],
    ) -> mt.ReadResourceResult:
        """Authorize resource reads with Eunomia."""
        if not self.enabled:
            return await call_next(context)

        # Extract resource URI from request
        resource_uri = context.message.uri

        # Extract user information
        user_role = self._extract_user_role(context)
        user_id = self._extract_user_id(context)
        agent_id = self._extract_agent_id(context)

        # Check authorization
        is_authorized = await self._check_authorization(
            user_role=user_role,
            user_id=user_id,
            agent_id=agent_id,
            action="resources/read",
            resource_attrs={"resource_path": resource_uri}
        )

        if not is_authorized:
            logger.warning(
                f"Resource read denied: {user_role} user {user_id} cannot read {resource_uri}"
            )
            # Return empty resource content with error
            return mt.ReadResourceResult(
                contents=[
                    mt.TextResourceContents(
                        uri=resource_uri,
                        mimeType="text/plain",
                        text="Access denied: insufficient permissions to read this resource"
                    )
                ]
            )

        logger.info(f"Resource read authorized: {user_role} user {user_id} reading {resource_uri}")
        return await call_next(context)

    def _extract_user_id(self, context: MiddlewareContext[Any]) -> str:
        """Extract user ID from context metadata."""
        # In a real implementation, this would extract from JWT tokens, headers, etc.
        # For now, we'll use a simple approach based on FastMCP context
        if hasattr(context, 'fastmcp_context') and context.fastmcp_context:
            # Check if there's user info in the FastMCP context
            user_info = getattr(context.fastmcp_context, 'user_info', None)
            if user_info and hasattr(user_info, 'id'):
                return user_info.id
        
        # Fallback to a default user ID
        return "anonymous"

    def _extract_user_role(self, context: MiddlewareContext[Any]) -> str:
        """Extract user role from context."""
        # In a real implementation, this would be extracted from authenticated context
        # For demo purposes, we'll simulate different user types
        
        if hasattr(context, 'fastmcp_context') and context.fastmcp_context:
            # Check if there's role info in the FastMCP context
            user_info = getattr(context.fastmcp_context, 'user_info', None)
            if user_info and hasattr(user_info, 'role'):
                return user_info.role.lower()
        
        # For demo purposes, let's simulate role extraction from the method/context
        # In a real application, this would come from authentication middleware
        
        # Simulate admin access (could be based on API key, JWT claims, etc.)
        if self._is_admin_context(context):
            return "admin"
        elif self._is_user_context(context):
            return "user"
        else:
            return "guest"

    def _extract_agent_id(self, context: MiddlewareContext[Any]) -> Optional[str]:
        """Extract agent ID from context."""
        # This would typically come from X-Agent-ID header or similar
        return f"agent-{id(context)}"  # Simple unique ID for demo

    def _is_admin_context(self, context: MiddlewareContext[Any]) -> bool:
        """Check if context indicates admin privileges."""
        # In a real implementation, this would check JWT claims, API keys, etc.
        # For demo, let's say admins have special metadata
        return False  # Default to non-admin for safety

    def _is_user_context(self, context: MiddlewareContext[Any]) -> bool:
        """Check if context indicates regular user privileges."""
        # This would check for valid user authentication
        # For demo, let's assume most requests are from users unless specified
        return True  # Default to user role

    async def _check_authorization(
        self,
        user_role: str,
        user_id: str,
        agent_id: Optional[str],
        action: str,
        resource_attrs: Dict[str, Any]
    ) -> bool:
        """Check authorization with Eunomia server."""
        try:
            check_request = {
                "principal": {
                    "attributes": {
                        "role": user_role,
                        "user_id": user_id,
                        "agent_id": agent_id or "unknown"
                    }
                },
                "resource": {
                    "attributes": resource_attrs
                },
                "action": action
            }

            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.eunomia_url}/check",
                    json=check_request,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    allowed = result.get("allowed", False)
                    reason = result.get("reason", "")
                    
                    logger.debug(
                        f"Authorization check: action={action}, resource={resource_attrs}, "
                        f"user_role={user_role}, allowed={allowed}, reason={reason}"
                    )
                    
                    return allowed
                else:
                    logger.error(
                        f"Eunomia server returned status {response.status_code}: {response.text}"
                    )
                    # Default to deny for security
                    return False
                    
        except Exception as e:
            logger.error(f"Authorization check failed: {e}")
            # Default to deny for security
            return False