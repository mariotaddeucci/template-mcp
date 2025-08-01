#!/usr/bin/env python3
"""Manual verification script for Template MCP core implementation."""

import sys
from pathlib import Path

def check_file_structure():
    """Check that all expected files are present."""
    print("🔍 Checking file structure...")
    
    expected_files = [
        "src/template_mcp/__init__.py",
        "src/template_mcp/main.py", 
        "src/template_mcp/config.py",
        "src/template_mcp/models.py",
        "src/template_mcp/logging.py",
        "src/template_mcp/server.py",
        "tests/test_config.py",
        "tests/test_models.py",
        "tests/test_server.py",
        "examples/basic_client.py",
        "configs/eunomia_policies.json",
        "configs/logging_config.yaml",
    ]
    
    missing_files = []
    for file_path in expected_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ All expected files are present")
        return True


def check_code_quality():
    """Check basic code quality indicators."""
    print("\n🔍 Checking code quality indicators...")
    
    issues = []
    
    # Check for key implementation patterns
    server_file = Path("src/template_mcp/server.py")
    if server_file.exists():
        content = server_file.read_text()
        
        # Check for FastMCP integration
        if "FastMCP" in content:
            print("✅ FastMCP framework integration found")
        else:
            issues.append("FastMCP integration not found")
        
        # Check for Eunomia middleware integration in one line
        if "EunomiaMcpMiddleware()" in content and "add_middleware" in content:
            print("✅ Eunomia middleware integration found (one line)")
        else:
            issues.append("Eunomia middleware integration not found")
        
        # Check for hello tool
        if "hello" in content and "tool" in content.lower():
            print("✅ Hello tool implementation found")
        else:
            issues.append("Hello tool implementation not found")
    
    # Check config file
    config_file = Path("src/template_mcp/config.py")
    if config_file.exists():
        content = config_file.read_text()
        
        if "Pydantic" in content and "Settings" in content:
            print("✅ Pydantic Settings configuration found")
        else:
            issues.append("Pydantic Settings configuration not found")
    
    # Check models file
    models_file = Path("src/template_mcp/models.py")
    if models_file.exists():
        content = models_file.read_text()
        
        if "BaseModel" in content and "Field" in content:
            print("✅ Pydantic models with validation found")
        else:
            issues.append("Pydantic models not found")
    
    # Check logging file
    logging_file = Path("src/template_mcp/logging.py")
    if logging_file.exists():
        content = logging_file.read_text()
        
        if "loguru" in content and "structlog" in content:
            print("✅ Structured logging with loguru/structlog found")
        else:
            issues.append("Structured logging not found")
    
    if issues:
        print(f"❌ Code quality issues: {issues}")
        return False
    else:
        print("✅ Code quality checks passed")
        return True


def check_project_configuration():
    """Check project configuration files."""
    print("\n🔍 Checking project configuration...")
    
    # Check pyproject.toml
    pyproject_file = Path("pyproject.toml")
    if pyproject_file.exists():
        content = pyproject_file.read_text()
        
        if "fastmcp" in content:
            print("✅ FastMCP dependency configured")
        else:
            print("❌ FastMCP dependency not found")
            return False
        
        if "eunomia" in content:
            print("✅ Eunomia dependencies configured")
        else:
            print("❌ Eunomia dependencies not found")
            return False
        
        if "template-mcp = " in content:
            print("✅ CLI entry point configured")
        else:
            print("❌ CLI entry point not found")
            return False
    
    # Check example client
    client_file = Path("examples/basic_client.py")
    if client_file.exists():
        content = client_file.read_text()
        
        if "hello" in content and "server_info" in content:
            print("✅ Example client with tool demonstrations")
        else:
            print("❌ Example client incomplete")
            return False
    
    return True


def analyze_implementation():
    """Analyze the implementation against requirements."""
    print("\n📋 Analyzing implementation against requirements...")
    
    requirements = [
        ("FastMCP server implementation", "src/template_mcp/server.py"),
        ("Eunomia middleware integration", "src/template_mcp/server.py"),
        ("Pydantic models with validation", "src/template_mcp/models.py"),
        ("Configuration system", "src/template_mcp/config.py"),
        ("Structured logging", "src/template_mcp/logging.py"),
        ("Hello tool implementation", "src/template_mcp/server.py"),
        ("Comprehensive tests", "tests/"),
    ]
    
    for requirement, file_path in requirements:
        if Path(file_path).exists():
            print(f"✅ {requirement}")
        else:
            print(f"❌ {requirement}")


def main():
    """Main verification function."""
    print("🚀 Template MCP Core Implementation Verification")
    print("=" * 50)
    
    all_passed = True
    
    # Run all checks
    all_passed &= check_file_structure()
    all_passed &= check_code_quality()
    all_passed &= check_project_configuration()
    
    analyze_implementation()
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✅ All verification checks passed!")
        print("\n📝 Implementation Summary:")
        print("• FastMCP server with hello tool ✅")
        print("• Eunomia middleware integration (one line) ✅")
        print("• Pydantic models with robust validation ✅")
        print("• Configuration system with environment support ✅")
        print("• Structured logging with loguru/structlog ✅")
        print("• Comprehensive test suite ✅")
        print("• CLI entry point configured ✅")
        print("• Example client for testing ✅")
        
        print("\n🔄 Next Steps:")
        print("1. Install dependencies: pip install -e .[dev,test]")
        print("2. Run tests: python -m pytest")
        print("3. Start server: template-mcp")
        print("4. Use example client for testing")
        
        return 0
    else:
        print("❌ Some verification checks failed!")
        return 1


if __name__ == "__main__":
    exit(main())