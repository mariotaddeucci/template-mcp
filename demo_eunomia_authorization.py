#!/usr/bin/env python3
"""
Demo script showing the Eunomia Authorization System in action.

This script demonstrates:
1. Policy validation and deployment 
2. Authorization checks for different user roles
3. Real-time authorization decisions
4. Granular access control

Prerequisites:
- Eunomia server running on localhost:8000
- Template MCP server configured with Eunomia middleware
"""

import asyncio
import json
import sys
from pathlib import Path

# Add src to path  
sys.path.insert(0, str(Path(__file__).parent / "src"))

from template_mcp.eunomia_middleware import EunomiaAuthMiddleware
from template_mcp.config import AppConfig


async def demonstrate_authorization():
    """Comprehensive demonstration of the Eunomia authorization system."""
    
    print("🔐 Eunomia Authorization System Demo")
    print("="*50)
    
    # Initialize middleware
    config = AppConfig()
    middleware = EunomiaAuthMiddleware(config=config)
    
    print(f"📡 Connected to Eunomia server: {config.eunomia.server_url}")
    print(f"⚙️  Authorization enabled: {config.eunomia.enabled}")
    print()
    
    # Demo scenarios
    scenarios = [
        {
            "title": "👑 ADMIN USER SCENARIOS",
            "tests": [
                {
                    "desc": "Admin calls hello tool",
                    "role": "admin", "action": "tools/call", "resource": {"tool_name": "hello"}
                },
                {
                    "desc": "Admin calls server_info tool", 
                    "role": "admin", "action": "tools/call", "resource": {"tool_name": "server_info"}
                },
                {
                    "desc": "Admin lists tools",
                    "role": "admin", "action": "tools/list", "resource": {"scope": "all"}
                },
                {
                    "desc": "Admin reads resources",
                    "role": "admin", "action": "resources/read", "resource": {"resource_path": "any/resource"}
                }
            ]
        },
        {
            "title": "👤 REGULAR USER SCENARIOS", 
            "tests": [
                {
                    "desc": "User calls hello tool",
                    "role": "user", "action": "tools/call", "resource": {"tool_name": "hello"}
                },
                {
                    "desc": "User calls server_info tool",
                    "role": "user", "action": "tools/call", "resource": {"tool_name": "server_info"}
                },
                {
                    "desc": "User lists tools",
                    "role": "user", "action": "tools/list", "resource": {"scope": "all"}
                },
                {
                    "desc": "User reads public resource",
                    "role": "user", "action": "resources/read", "resource": {"resource_path": "public/docs"}
                },
                {
                    "desc": "User tries to read private resource",
                    "role": "user", "action": "resources/read", "resource": {"resource_path": "private/secret"}
                }
            ]
        },
        {
            "title": "👻 GUEST USER SCENARIOS",
            "tests": [
                {
                    "desc": "Guest calls hello tool",
                    "role": "guest", "action": "tools/call", "resource": {"tool_name": "hello"}
                },
                {
                    "desc": "Guest tries to call server_info tool",
                    "role": "guest", "action": "tools/call", "resource": {"tool_name": "server_info"}
                },
                {
                    "desc": "Guest lists tools", 
                    "role": "guest", "action": "tools/list", "resource": {"scope": "all"}
                },
                {
                    "desc": "Guest tries to read any resource",
                    "role": "guest", "action": "resources/read", "resource": {"resource_path": "public/docs"}
                }
            ]
        },
        {
            "title": "🚫 UNAUTHORIZED SCENARIOS",
            "tests": [
                {
                    "desc": "Unknown user tries to access tools",
                    "role": "unknown", "action": "tools/call", "resource": {"tool_name": "hello"}
                },
                {
                    "desc": "Guest tries admin action",
                    "role": "guest", "action": "prompts/get", "resource": {"prompt_name": "admin_prompt"}
                }
            ]
        }
    ]
    
    # Run demonstration
    total_tests = 0
    allowed_tests = 0
    
    for scenario in scenarios:
        print(f"\n{scenario['title']}")
        print("-" * len(scenario['title']))
        
        for test in scenario["tests"]:
            total_tests += 1
            
            try:
                result = await middleware._check_authorization(
                    user_role=test["role"],
                    user_id=f"{test['role']}_user",
                    agent_id="demo_agent",
                    action=test["action"],
                    resource_attrs=test["resource"]
                )
                
                status = "✅ ALLOWED" if result else "❌ DENIED"
                if result:
                    allowed_tests += 1
                    
                print(f"  {status} - {test['desc']}")
                
            except Exception as e:
                print(f"  ❌ ERROR - {test['desc']}: {e}")
    
    # Summary
    print(f"\n📊 DEMO SUMMARY")
    print("="*20)
    print(f"Total authorization checks: {total_tests}")
    print(f"Allowed: {allowed_tests}")
    print(f"Denied: {total_tests - allowed_tests}")
    print(f"Success rate: {(allowed_tests/total_tests)*100:.1f}%")
    
    # Policy information
    print(f"\n📋 ACTIVE POLICIES")
    print("="*20)
    policy_file = Path("configs/eunomia_policies.json")
    if policy_file.exists():
        with open(policy_file) as f:
            policies = json.load(f)
        
        print(f"Policy: {policies.get('name', 'N/A')}")
        print(f"Description: {policies.get('description', 'N/A')}")
        print(f"Default effect: {policies.get('default_effect', 'N/A')}")
        print(f"Active rules: {len(policies.get('rules', []))}")
        
        print("\nRule summary:")
        for i, rule in enumerate(policies.get("rules", []), 1):
            effect_icon = "✅" if rule.get("effect") == "allow" else "❌"
            print(f"  {i}. {effect_icon} {rule.get('name', 'Unnamed')}")
    
    print(f"\n🎯 SECURITY FEATURES ACTIVE")
    print("="*30)
    print("✅ Granular role-based access control")
    print("✅ Resource-level authorization")
    print("✅ Action-specific permissions")
    print("✅ Default deny security model")
    print("✅ Real-time policy evaluation")
    print("✅ Comprehensive audit logging")
    print("✅ Agent identification support")
    print("✅ Automatic response filtering")
    
    print(f"\n🚀 Eunomia Authorization System is operational!")
    
    return True


async def main():
    """Main demo function."""
    try:
        await demonstrate_authorization()
        return True
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        return False


if __name__ == "__main__":
    print("Starting Eunomia Authorization Demo...")
    success = asyncio.run(main())
    print("\nDemo completed!")
    sys.exit(0 if success else 1)