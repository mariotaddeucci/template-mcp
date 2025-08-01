#!/usr/bin/env python3
"""Test script to verify Eunomia authorization integration."""

import asyncio
import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from template_mcp.eunomia_middleware import EunomiaAuthMiddleware
from template_mcp.config import AppConfig


async def test_authorization():
    """Test the Eunomia authorization middleware."""
    print("🔐 Testing Eunomia Authorization Integration")
    print("=" * 50)
    
    # Initialize middleware
    config = AppConfig()
    middleware = EunomiaAuthMiddleware(config=config)
    
    # Test different scenarios
    test_cases = [
        {
            "name": "Admin accessing hello tool",
            "user_role": "admin",
            "user_id": "admin_user",
            "action": "tools/call",
            "resource": {"tool_name": "hello"},
            "expected": True
        },
        {
            "name": "Guest accessing hello tool",
            "user_role": "guest", 
            "user_id": "guest_user",
            "action": "tools/call",
            "resource": {"tool_name": "hello"},
            "expected": True
        },
        {
            "name": "Guest accessing server_info tool",
            "user_role": "guest",
            "user_id": "guest_user", 
            "action": "tools/call",
            "resource": {"tool_name": "server_info"},
            "expected": False
        },
        {
            "name": "User accessing server_info tool",
            "user_role": "user",
            "user_id": "regular_user",
            "action": "tools/call", 
            "resource": {"tool_name": "server_info"},
            "expected": True
        },
        {
            "name": "User listing tools",
            "user_role": "user",
            "user_id": "regular_user",
            "action": "tools/list",
            "resource": {"scope": "all"},  # Add non-empty attributes
            "expected": True
        }
    ]
    
    # Run test cases
    passed = 0
    total = len(test_cases)
    
    for test_case in test_cases:
        print(f"\n🧪 Testing: {test_case['name']}")
        
        try:
            result = await middleware._check_authorization(
                user_role=test_case["user_role"],
                user_id=test_case["user_id"],
                agent_id="test_agent",
                action=test_case["action"],
                resource_attrs=test_case["resource"]
            )
            
            if result == test_case["expected"]:
                print(f"   ✅ PASS - Expected: {test_case['expected']}, Got: {result}")
                passed += 1
            else:
                print(f"   ❌ FAIL - Expected: {test_case['expected']}, Got: {result}")
                
        except Exception as e:
            print(f"   ❌ ERROR - {e}")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Eunomia authorization is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the configuration.")
        return False


async def test_policy_validation():
    """Test policy file validation."""
    print("\n📄 Testing Policy File Validation")
    print("=" * 30)
    
    policy_file = Path("configs/eunomia_policies.json")
    
    if not policy_file.exists():
        print("❌ Policy file not found!")
        return False
        
    try:
        with open(policy_file) as f:
            policies = json.load(f)
            
        print(f"✅ Policy file loaded successfully")
        print(f"   📋 Policy name: {policies.get('name', 'N/A')}")
        print(f"   📝 Description: {policies.get('description', 'N/A')}")
        print(f"   🔒 Default effect: {policies.get('default_effect', 'N/A')}")
        print(f"   📏 Number of rules: {len(policies.get('rules', []))}")
        
        # List rules
        for i, rule in enumerate(policies.get("rules", []), 1):
            print(f"   {i}. {rule.get('name', 'Unnamed')} - {rule.get('effect', 'unknown')} effect")
            
        return True
        
    except Exception as e:
        print(f"❌ Error loading policy file: {e}")
        return False


async def main():
    """Main test function."""
    print("🚀 Eunomia Authorization Test Suite")
    print("==================================")
    
    # Test policy validation
    policy_ok = await test_policy_validation()
    
    if not policy_ok:
        print("\n❌ Policy validation failed. Cannot proceed with authorization tests.")
        return False
    
    # Test authorization
    auth_ok = await test_authorization()
    
    print(f"\n🏁 Final Result: {'SUCCESS' if auth_ok else 'FAILURE'}")
    return auth_ok


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)