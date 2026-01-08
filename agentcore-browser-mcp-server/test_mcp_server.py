#!/usr/bin/env python3
"""
Test script for AgentCore Browser MCP Server

This script tests the MCP server with real AWS AgentCore Browser.
Requires AWS credentials and proper IAM permissions.
"""

import asyncio
import json
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from agentcore_browser_mcp import (
    app,
    sessions,
    handle_create_session,
    handle_navigate,
    handle_interact,
    handle_extract_content,
    handle_execute_script,
    handle_screenshot,
    handle_manage_tabs,
    handle_list_sessions,
    handle_get_session_info,
    handle_close_session,
    handle_get_live_view_url
)


class TestResults:
    """Track test results"""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.skipped = 0
        self.tests = []
    
    def add_pass(self, name: str):
        self.passed += 1
        self.tests.append((name, "PASS", None))
        print(f"✅ {name}")
    
    def add_fail(self, name: str, error: str):
        self.failed += 1
        self.tests.append((name, "FAIL", error))
        print(f"❌ {name}: {error}")
    
    def add_skip(self, name: str, reason: str):
        self.skipped += 1
        self.tests.append((name, "SKIP", reason))
        print(f"⏭️  {name}: {reason}")
    
    def summary(self):
        total = self.passed + self.failed + self.skipped
        print(f"\n{'='*60}")
        print(f"Test Results: {self.passed}/{total} passed, {self.skipped} skipped, {self.failed} failed")
        print(f"{'='*60}")
        if self.failed > 0:
            print("\nFailed tests:")
            for name, status, error in self.tests:
                if status == "FAIL":
                    print(f"  - {name}: {error}")
        return self.failed == 0


results = TestResults()


def check_aws_credentials():
    """Check if AWS credentials are configured"""
    try:
        import boto3
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()
        print(f"✓ AWS credentials configured")
        print(f"  Account: {identity['Account']}")
        print(f"  User/Role: {identity['Arn']}")
        return True
    except Exception as e:
        print(f"❌ AWS credentials not configured: {e}")
        print("   Please run: aws configure")
        return False


def check_region():
    """Check if region is supported"""
    region = os.getenv('AWS_REGION', 'us-east-1')
    supported_regions = ['us-east-1', 'us-west-2', 'eu-central-1', 'ap-southeast-2']
    
    if region in supported_regions:
        print(f"✓ Using region: {region}")
        return True
    else:
        print(f"⚠️  Warning: Region {region} may not support AgentCore Browser")
        print(f"   Supported regions: {', '.join(supported_regions)}")
        return True  # Continue anyway


async def test_list_tools():
    """Test that tools are properly defined"""
    try:
        # list_tools is decorated with @app.list_tools() which makes it a regular function
        # We need to call the decorated function directly
        tools_func = None
        for name, obj in vars(app).items():
            if callable(obj) and hasattr(obj, '__name__') and 'list_tools' in obj.__name__:
                tools_func = obj
                break
        
        if tools_func:
            tools = await tools_func()
        else:
            # Fallback: call the function directly
            from agentcore_browser_mcp import list_tools as list_tools_func
            tools = await list_tools_func()
        
        expected_tools = [
            "create_browser_session",
            "navigate",
            "interact",
            "extract_content",
            "execute_script",
            "screenshot",
            "manage_tabs",
            "list_sessions",
            "get_session_info",
            "close_session",
            "get_live_view_url"
        ]
        
        tool_names = [tool.name for tool in tools]
        
        missing = [t for t in expected_tools if t not in tool_names]
        if missing:
            results.add_fail("test_list_tools", f"Missing tools: {missing}")
            return
        
        results.add_pass("test_list_tools")
    except Exception as e:
        results.add_fail("test_list_tools", str(e))


async def test_create_session():
    """Test session creation with real AWS"""
    try:
        # Clear any existing sessions
        sessions.clear()
        
        print("  Creating browser session (this may take 10-15 seconds)...")
        response = await handle_create_session({
            "session_id": "test-session",
            "description": "Automated test session",
            "region": os.getenv('AWS_REGION', 'us-east-1'),
            "session_timeout": 1800,  # 30 minutes
            "enable_recording": False
        })
        
        # Verify response
        if len(response) == 0:
            results.add_fail("test_create_session", "Empty response")
            return
        
        text = response[0].text
        if "✅" not in text or "test-session" not in text:
            results.add_fail("test_create_session", f"Unexpected response: {text}")
            return
        
        # Verify session was created
        if "test-session" not in sessions:
            results.add_fail("test_create_session", "Session not in sessions dict")
            return
        
        print(f"  Session created successfully")
        results.add_pass("test_create_session")
    
    except Exception as e:
        results.add_fail("test_create_session", str(e))


async def test_list_sessions():
    """Test listing sessions"""
    try:
        response = await handle_list_sessions({})
        
        if len(response) == 0:
            results.add_fail("test_list_sessions", "Empty response")
            return
        
        text = response[0].text
        if "test-session" not in text:
            results.add_fail("test_list_sessions", "Session not in list")
            return
        
        results.add_pass("test_list_sessions")
    
    except Exception as e:
        results.add_fail("test_list_sessions", str(e))


async def test_get_session_info():
    """Test getting session info"""
    try:
        response = await handle_get_session_info({
            "session_id": "test-session"
        })
        
        if len(response) == 0:
            results.add_fail("test_get_session_info", "Empty response")
            return
        
        text = response[0].text
        if "test-session" not in text or "Session Information" not in text:
            results.add_fail("test_get_session_info", f"Unexpected response: {text}")
            return
        
        results.add_pass("test_get_session_info")
    
    except Exception as e:
        results.add_fail("test_get_session_info", str(e))


async def test_navigate():
    """Test navigation"""
    try:
        if "test-session" not in sessions:
            results.add_skip("test_navigate", "No test session available")
            return
        
        print("  Navigating to example.com...")
        response = await handle_navigate({
            "session_id": "test-session",
            "url": "https://example.com",
            "wait_for": "networkidle"
        })
        
        if len(response) == 0:
            results.add_fail("test_navigate", "Empty response")
            return
        
        text = response[0].text
        if "✅" not in text or "example.com" not in text:
            results.add_fail("test_navigate", f"Unexpected response: {text}")
            return
        
        results.add_pass("test_navigate")
    
    except Exception as e:
        results.add_fail("test_navigate", str(e))


async def test_extract_content():
    """Test content extraction"""
    try:
        if "test-session" not in sessions:
            results.add_skip("test_extract_content", "No test session available")
            return
        
        print("  Extracting page title...")
        response = await handle_extract_content({
            "session_id": "test-session",
            "content_type": "text",
            "selector": "h1"
        })
        
        if len(response) == 0:
            results.add_fail("test_extract_content", "Empty response")
            return
        
        text = response[0].text
        if "Example Domain" not in text:
            results.add_fail("test_extract_content", f"Expected 'Example Domain', got: {text}")
            return
        
        results.add_pass("test_extract_content")
    
    except Exception as e:
        results.add_fail("test_extract_content", str(e))


async def test_execute_script():
    """Test JavaScript execution"""
    try:
        if "test-session" not in sessions:
            results.add_skip("test_execute_script", "No test session available")
            return
        
        print("  Executing JavaScript...")
        response = await handle_execute_script({
            "session_id": "test-session",
            "script": "document.title"  # Remove 'return' keyword
        })
        
        if len(response) == 0:
            results.add_fail("test_execute_script", "Empty response")
            return
        
        text = response[0].text
        if "Example Domain" not in text:
            results.add_fail("test_execute_script", f"Unexpected result: {text}")
            return
        
        results.add_pass("test_execute_script")
    
    except Exception as e:
        results.add_fail("test_execute_script", str(e))


async def test_screenshot():
    """Test screenshot capture"""
    try:
        if "test-session" not in sessions:
            results.add_skip("test_screenshot", "No test session available")
            return
        
        print("  Taking screenshot...")
        
        # Create screenshots directory
        screenshots_dir = Path("screenshots")
        screenshots_dir.mkdir(exist_ok=True)
        
        response = await handle_screenshot({
            "session_id": "test-session",
            "path": "screenshots/test-screenshot.png"
        })
        
        if len(response) == 0:
            results.add_fail("test_screenshot", "Empty response")
            return
        
        text = response[0].text
        if "✅" not in text or "screenshot" not in text.lower():
            results.add_fail("test_screenshot", f"Unexpected response: {text}")
            return
        
        # Verify file was created
        screenshot_path = Path("screenshots/test-screenshot.png")
        if not screenshot_path.exists():
            results.add_fail("test_screenshot", "Screenshot file not created")
            return
        
        results.add_pass("test_screenshot")
    
    except Exception as e:
        results.add_fail("test_screenshot", str(e))


async def test_manage_tabs():
    """Test tab management"""
    try:
        if "test-session" not in sessions:
            results.add_skip("test_manage_tabs", "No test session available")
            return
        
        print("  Creating new tab...")
        response = await handle_manage_tabs({
            "session_id": "test-session",
            "action": "new_tab",
            "tab_id": "tab2"
        })
        
        if len(response) == 0:
            results.add_fail("test_manage_tabs", "Empty response")
            return
        
        text = response[0].text
        if "✅" not in text or "tab2" not in text:
            results.add_fail("test_manage_tabs", f"Unexpected response: {text}")
            return
        
        # List tabs
        response = await handle_manage_tabs({
            "session_id": "test-session",
            "action": "list_tabs"
        })
        
        text = response[0].text
        if "tab2" not in text:
            results.add_fail("test_manage_tabs", "New tab not in list")
            return
        
        results.add_pass("test_manage_tabs")
    
    except Exception as e:
        results.add_fail("test_manage_tabs", str(e))


async def test_get_live_view_url():
    """Test getting Live View URL"""
    try:
        if "test-session" not in sessions:
            results.add_skip("test_get_live_view_url", "No test session available")
            return
        
        response = await handle_get_live_view_url({
            "session_id": "test-session"
        })
        
        if len(response) == 0:
            results.add_fail("test_get_live_view_url", "Empty response")
            return
        
        text = response[0].text
        if "Live View URL" not in text or "console.aws.amazon.com" not in text:
            results.add_fail("test_get_live_view_url", f"Unexpected response: {text}")
            return
        
        results.add_pass("test_get_live_view_url")
    
    except Exception as e:
        results.add_fail("test_get_live_view_url", str(e))


async def test_close_session():
    """Test session cleanup"""
    try:
        if "test-session" not in sessions:
            results.add_skip("test_close_session", "No test session available")
            return
        
        print("  Closing session...")
        response = await handle_close_session({
            "session_id": "test-session"
        })
        
        if len(response) == 0:
            results.add_fail("test_close_session", "Empty response")
            return
        
        text = response[0].text
        if "✅" not in text or "closed" not in text:
            results.add_fail("test_close_session", f"Unexpected response: {text}")
            return
        
        # Verify session was removed
        if "test-session" in sessions:
            results.add_fail("test_close_session", "Session still in sessions dict")
            return
        
        results.add_pass("test_close_session")
    
    except Exception as e:
        results.add_fail("test_close_session", str(e))


async def run_all_tests():
    """Run all tests"""
    print("="*60)
    print("AgentCore Browser MCP Server - Test Suite")
    print("="*60)
    print()
    
    # Check prerequisites
    print("Checking prerequisites...")
    if not check_aws_credentials():
        print("\n❌ AWS credentials not configured. Cannot run tests.")
        print("   Please run: aws configure")
        return False
    
    check_region()
    print()
    
    # Run tests in order
    print("Running tests...")
    print()
    
    await test_list_tools()
    await test_create_session()
    await test_list_sessions()
    await test_get_session_info()
    await test_navigate()
    await test_extract_content()
    await test_execute_script()
    await test_screenshot()
    await test_manage_tabs()
    await test_get_live_view_url()
    await test_close_session()
    
    # Print summary
    success = results.summary()
    
    if success:
        print("\n✅ All tests passed!")
        print("\nThe MCP server is ready to use.")
        print("Next steps:")
        print("  1. Add the Power to Kiro")
        print("  2. Start automating with AgentCore Browser!")
    else:
        print("\n⚠️  Some tests failed.")
        print("Please check the errors above and:")
        print("  1. Verify AWS credentials are configured")
        print("  2. Check IAM permissions for AgentCore Browser")
        print("  3. Ensure region supports AgentCore Browser")
    
    return success


def main():
    """Main entry point"""
    try:
        success = asyncio.run(run_all_tests())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
