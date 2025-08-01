# Eunomia Authorization System - Usage Guide

## 🎯 Overview

The Template MCP server now includes a complete Eunomia authorization system that provides granular access control for MCP operations. This guide explains how to use and configure the authorization system.

## 🚀 Quick Start

### 1. Start the Eunomia Server
```bash
# Start Eunomia authorization server (runs on port 8000 by default)
uv run eunomia server --host 0.0.0.0 --port 8000
```

### 2. Deploy Authorization Policies
```bash
# The policies are automatically deployed when the server starts
# Or manually deploy using curl:
curl -X POST -H "Content-Type: application/json" \
  -d @configs/eunomia_policies.json \
  http://localhost:8000/admin/policies
```

### 3. Start the MCP Server
```bash
# Start the Template MCP server with authorization enabled
uv run python -m template_mcp.main
```

### 4. Test Authorization
```bash
# Run the integration test suite
uv run python test_eunomia_integration.py

# Run the comprehensive demo
uv run python demo_eunomia_authorization.py
```

## 🔐 Authorization Policies

The system uses three main user roles with different permission levels:

### Admin Users (`role: admin`)
- ✅ **Full Access**: All MCP operations (tools, resources, prompts)
- ✅ **All Tools**: Can call any tool (hello, server_info, etc.)
- ✅ **All Resources**: Can read any resource
- ✅ **All Prompts**: Can access any prompt

### Regular Users (`role: user`) 
- ✅ **Tool Access**: Can call hello and server_info tools
- ✅ **Tool Listing**: Can list all available tools
- ✅ **Public Resources**: Can read resources under `public/` paths
- ❌ **Private Resources**: Cannot read private or restricted resources

### Guest Users (`role: guest`)
- ✅ **Hello Tool**: Can call the hello tool only
- ✅ **Tool Listing**: Can see available tools in lists
- ❌ **Server Info**: Explicitly denied access to server_info tool
- ❌ **Resources**: Cannot read any resources

### Default Behavior
- ❌ **Deny by Default**: All unauthorized actions are denied
- 🔒 **Secure First**: Unknown users have no permissions

## 🛠 Configuration

### Environment Variables
```bash
# .env.dev or .env.prod
EUNOMIA_SERVER_URL=http://localhost:8000
EUNOMIA_ENABLED=true
EUNOMIA_TIMEOUT=30
```

### Policy File Structure
The authorization policies are defined in `configs/eunomia_policies.json`:

```json
{
  "version": "1.0",
  "name": "mcp_policies", 
  "description": "MCP authorization policies...",
  "default_effect": "deny",
  "rules": [
    {
      "name": "admin_full_access",
      "effect": "allow",
      "actions": ["tools/list", "tools/call", "resources/list", "resources/read"],
      "principal_conditions": [
        {"path": "attributes.role", "operator": "equals", "value": "admin"}
      ],
      "resource_conditions": []
    }
    // ... more rules
  ]
}
```

## 🔍 How Authorization Works

### 1. Request Interception
The `EunomiaAuthMiddleware` intercepts all MCP requests before they reach the tool handlers.

### 2. User Identification
The middleware extracts user information from:
- **X-User-ID header**: Explicit user identification
- **X-User-Role header**: Role specification
- **X-Agent-ID header**: Agent identification
- **User-Agent header**: Role hints in user agent string
- **Authorization header**: JWT tokens or API keys

### 3. Policy Evaluation
For each request, the middleware:
1. Maps the MCP method to an action (e.g., `tools/call`)
2. Extracts resource attributes (e.g., `tool_name: "hello"`)
3. Sends authorization request to Eunomia server
4. Gets allow/deny decision with reasoning

### 4. Response Handling
Based on the authorization decision:
- ✅ **Allowed**: Request proceeds to tool handler
- ❌ **Denied**: Returns access denied error
- 🔄 **Filtered**: Tool lists are filtered based on permissions

## 🎛 Advanced Features

### Agent Identification
```python
# Set user context in requests
headers = {
    "X-User-ID": "user123",
    "X-User-Role": "user", 
    "X-Agent-ID": "mcp-client-v1.0"
}
```

### Automatic Filtering
The middleware automatically filters responses:
- **Tool Lists**: Only shows tools the user can access
- **Resource Lists**: Filters based on resource permissions
- **Prompt Lists**: Shows only accessible prompts

### Audit Logging
All authorization decisions are logged with:
- User ID and role
- Requested action and resource
- Allow/deny decision with reason
- Execution time and context

### Error Handling
The system gracefully handles:
- Eunomia server unavailable → Deny for security
- Invalid policy format → Deny for security  
- Network errors → Deny for security
- Invalid user context → Treat as guest

## 🧪 Testing Scenarios

### Successful Authorization
```python
# Admin accessing any tool
{
  "user_role": "admin",
  "action": "tools/call", 
  "resource": {"tool_name": "hello"}
}
# Result: ✅ ALLOWED

# User accessing allowed tool
{
  "user_role": "user",
  "action": "tools/call",
  "resource": {"tool_name": "server_info"} 
}
# Result: ✅ ALLOWED
```

### Blocked Authorization
```python
# Guest accessing restricted tool
{
  "user_role": "guest",
  "action": "tools/call",
  "resource": {"tool_name": "server_info"}
}
# Result: ❌ DENIED

# User accessing private resource  
{
  "user_role": "user", 
  "action": "resources/read",
  "resource": {"resource_path": "private/secret"}
}
# Result: ❌ DENIED
```

## 📊 Monitoring and Debugging

### Check Eunomia Server Status
```bash
curl http://localhost:8000/health
```

### View Current Policies
```bash
curl http://localhost:8000/admin/policies
```

### Test Authorization Manually
```bash
curl -X POST http://localhost:8000/check \
  -H "Content-Type: application/json" \
  -d '{
    "principal": {"attributes": {"role": "user"}},
    "resource": {"attributes": {"tool_name": "hello"}},
    "action": "tools/call"
  }'
```

### Debug Authorization Issues
1. Check Eunomia server logs
2. Verify policy deployment
3. Test with demo script
4. Check middleware logs in MCP server

## 🔒 Security Best Practices

1. **Default Deny**: Always use deny as default effect
2. **Least Privilege**: Give users minimum required permissions
3. **Regular Audits**: Review policies and access logs regularly
4. **Secure Transport**: Use HTTPS in production
5. **Token Validation**: Implement proper JWT validation for production
6. **Rate Limiting**: Add rate limiting to authorization endpoints
7. **Monitoring**: Set up alerts for authorization failures

## 📚 References

- [Eunomia Authorization Guide](https://gofastmcp.com/integrations/eunomia-authorization)
- [FastMCP Middleware Documentation](https://gofastmcp.com/docs/middleware)
- [MCP Protocol Specification](https://modelcontextprotocol.io/docs/)

---

The Eunomia authorization system provides enterprise-grade security for MCP servers with fine-grained access control, comprehensive auditing, and seamless integration with FastMCP.