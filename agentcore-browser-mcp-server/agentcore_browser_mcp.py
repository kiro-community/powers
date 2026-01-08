#!/usr/bin/env python3
"""
AgentCore Browser MCP Server

Provides browser automation tools using AWS Bedrock AgentCore Browser.
Maintains session state across multiple requests for persistent workflows.
"""

import asyncio
import logging
import os
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from bedrock_agentcore.tools.browser_client import BrowserClient
from mcp.server import Server
from mcp.types import Tool, TextContent
from playwright.async_api import Browser as PlaywrightBrowser
from playwright.async_api import BrowserContext, Page, async_playwright

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize MCP server
app = Server("agentcore-browser")

# Global state for session management
sessions: Dict[str, "BrowserSession"] = {}
playwright_instance = None


@dataclass
class BrowserSession:
    """Browser session state"""
    session_id: str
    description: str
    region: str
    browser_client: BrowserClient
    browser: Optional[PlaywrightBrowser] = None
    context: Optional[BrowserContext] = None
    page: Optional[Page] = None
    tabs: Dict[str, Page] = field(default_factory=dict)
    active_tab_id: str = "main"
    created_at: float = field(default_factory=time.time)
    last_used: float = field(default_factory=time.time)
    timeout: int = 3600
    recording_enabled: bool = False
    
    def update_last_used(self):
        """Update last used timestamp"""
        self.last_used = time.time()
    
    def is_expired(self) -> bool:
        """Check if session has expired"""
        return (time.time() - self.last_used) > self.timeout


async def init_playwright():
    """Initialize Playwright instance"""
    global playwright_instance
    if playwright_instance is None:
        playwright_instance = await async_playwright().start()
    return playwright_instance


async def cleanup_expired_sessions():
    """Clean up expired sessions"""
    expired = [sid for sid, session in sessions.items() if session.is_expired()]
    for session_id in expired:
        try:
            await close_session_internal(session_id)
            logger.info(f"Cleaned up expired session: {session_id}")
        except Exception as e:
            logger.error(f"Error cleaning up session {session_id}: {e}")


async def close_session_internal(session_id: str):
    """Internal session cleanup"""
    if session_id not in sessions:
        return
    
    session = sessions[session_id]
    
    # Close browser
    if session.browser:
        try:
            await session.browser.close()
        except Exception as e:
            logger.error(f"Error closing browser: {e}")
    
    # Stop browser client
    if session.browser_client:
        try:
            session.browser_client.stop()
        except Exception as e:
            logger.error(f"Error stopping browser client: {e}")
    
    # Remove from sessions
    del sessions[session_id]


@app.list_tools()
async def list_tools() -> List[Tool]:
    """List available browser automation tools"""
    return [
        Tool(
            name="create_browser_session",
            description="Create a new browser session with persistent state",
            inputSchema={
                "type": "object",
                "properties": {
                    "session_id": {
                        "type": "string",
                        "description": "Unique identifier for this session (e.g., 'order-processing-001')"
                    },
                    "description": {
                        "type": "string",
                        "description": "Description of what this session will be used for"
                    },
                    "region": {
                        "type": "string",
                        "description": "AWS region (default: us-east-1)",
                        "default": "us-east-1"
                    },
                    "session_timeout": {
                        "type": "integer",
                        "description": "Session timeout in seconds (default: 3600, max: 28800)",
                        "default": 3600
                    },
                    "enable_recording": {
                        "type": "boolean",
                        "description": "Enable session recording to S3 (default: false)",
                        "default": False
                    }
                },
                "required": ["session_id", "description"]
            }
        ),
        Tool(
            name="navigate",
            description="Navigate to a URL in the browser session",
            inputSchema={
                "type": "object",
                "properties": {
                    "session_id": {
                        "type": "string",
                        "description": "Session ID from create_browser_session"
                    },
                    "url": {
                        "type": "string",
                        "description": "URL to navigate to"
                    },
                    "wait_for": {
                        "type": "string",
                        "description": "Wait condition: 'load', 'domcontentloaded', 'networkidle' (default: 'networkidle')",
                        "default": "networkidle"
                    }
                },
                "required": ["session_id", "url"]
            }
        ),
        Tool(
            name="interact",
            description="Interact with page elements (click, type, press keys, scroll)",
            inputSchema={
                "type": "object",
                "properties": {
                    "session_id": {
                        "type": "string",
                        "description": "Session ID"
                    },
                    "action": {
                        "type": "string",
                        "enum": ["click", "type", "press_key", "scroll"],
                        "description": "Action to perform"
                    },
                    "selector": {
                        "type": "string",
                        "description": "CSS selector for target element (not needed for scroll)"
                    },
                    "text": {
                        "type": "string",
                        "description": "Text to type (for 'type' action)"
                    },
                    "key": {
                        "type": "string",
                        "description": "Key to press (for 'press_key' action, e.g., 'Enter', 'Tab')"
                    },
                    "scroll_amount": {
                        "type": "integer",
                        "description": "Pixels to scroll (for 'scroll' action, negative for up)"
                    }
                },
                "required": ["session_id", "action"]
            }
        ),
        Tool(
            name="extract_content",
            description="Extract content from the page (text, HTML, attributes)",
            inputSchema={
                "type": "object",
                "properties": {
                    "session_id": {
                        "type": "string",
                        "description": "Session ID"
                    },
                    "content_type": {
                        "type": "string",
                        "enum": ["text", "html", "attribute"],
                        "description": "Type of content to extract"
                    },
                    "selector": {
                        "type": "string",
                        "description": "CSS selector (optional, extracts from whole page if not provided)"
                    },
                    "attribute": {
                        "type": "string",
                        "description": "Attribute name (for 'attribute' content_type)"
                    }
                },
                "required": ["session_id", "content_type"]
            }
        ),
        Tool(
            name="execute_script",
            description="Execute JavaScript code in the browser context",
            inputSchema={
                "type": "object",
                "properties": {
                    "session_id": {
                        "type": "string",
                        "description": "Session ID"
                    },
                    "script": {
                        "type": "string",
                        "description": "JavaScript code to execute"
                    }
                },
                "required": ["session_id", "script"]
            }
        ),
        Tool(
            name="screenshot",
            description="Take a screenshot of the page or element",
            inputSchema={
                "type": "object",
                "properties": {
                    "session_id": {
                        "type": "string",
                        "description": "Session ID"
                    },
                    "path": {
                        "type": "string",
                        "description": "File path to save screenshot (optional)"
                    },
                    "selector": {
                        "type": "string",
                        "description": "CSS selector for specific element (optional, full page if not provided)"
                    },
                    "full_page": {
                        "type": "boolean",
                        "description": "Capture full scrollable page (default: false)",
                        "default": False
                    }
                },
                "required": ["session_id"]
            }
        ),
        Tool(
            name="manage_tabs",
            description="Manage browser tabs (new, switch, close, list)",
            inputSchema={
                "type": "object",
                "properties": {
                    "session_id": {
                        "type": "string",
                        "description": "Session ID"
                    },
                    "action": {
                        "type": "string",
                        "enum": ["new_tab", "switch_tab", "close_tab", "list_tabs"],
                        "description": "Tab management action"
                    },
                    "tab_id": {
                        "type": "string",
                        "description": "Tab ID (for switch_tab, close_tab, or custom ID for new_tab)"
                    }
                },
                "required": ["session_id", "action"]
            }
        ),
        Tool(
            name="list_sessions",
            description="List all active browser sessions",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_session_info",
            description="Get detailed information about a session",
            inputSchema={
                "type": "object",
                "properties": {
                    "session_id": {
                        "type": "string",
                        "description": "Session ID"
                    }
                },
                "required": ["session_id"]
            }
        ),
        Tool(
            name="close_session",
            description="Close a browser session and clean up resources",
            inputSchema={
                "type": "object",
                "properties": {
                    "session_id": {
                        "type": "string",
                        "description": "Session ID"
                    }
                },
                "required": ["session_id"]
            }
        ),
        Tool(
            name="get_live_view_url",
            description="Get the Live View URL for real-time browser monitoring",
            inputSchema={
                "type": "object",
                "properties": {
                    "session_id": {
                        "type": "string",
                        "description": "Session ID"
                    }
                },
                "required": ["session_id"]
            }
        )
    ]



@app.call_tool()
async def call_tool(name: str, arguments: Any) -> List[TextContent]:
    """Handle tool calls"""
    
    # Clean up expired sessions periodically
    await cleanup_expired_sessions()
    
    try:
        if name == "create_browser_session":
            return await handle_create_session(arguments)
        elif name == "navigate":
            return await handle_navigate(arguments)
        elif name == "interact":
            return await handle_interact(arguments)
        elif name == "extract_content":
            return await handle_extract_content(arguments)
        elif name == "execute_script":
            return await handle_execute_script(arguments)
        elif name == "screenshot":
            return await handle_screenshot(arguments)
        elif name == "manage_tabs":
            return await handle_manage_tabs(arguments)
        elif name == "list_sessions":
            return await handle_list_sessions(arguments)
        elif name == "get_session_info":
            return await handle_get_session_info(arguments)
        elif name == "close_session":
            return await handle_close_session(arguments)
        elif name == "get_live_view_url":
            return await handle_get_live_view_url(arguments)
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    
    except Exception as e:
        logger.error(f"Error in {name}: {e}", exc_info=True)
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_create_session(args: Dict[str, Any]) -> List[TextContent]:
    """Create a new browser session"""
    session_id = args["session_id"]
    description = args["description"]
    region = args.get("region", os.getenv("AWS_REGION", "us-east-1"))
    session_timeout = args.get("session_timeout", 3600)
    enable_recording = args.get("enable_recording", False)
    
    # Check if session already exists
    if session_id in sessions:
        return [TextContent(
            type="text",
            text=f"Error: Session '{session_id}' already exists. Use a different session_id or close the existing session first."
        )]
    
    try:
        # Initialize Playwright
        playwright = await init_playwright()
        
        # Create browser client
        browser_client = BrowserClient(region=region)
        
        # Start browser session
        identifier = os.getenv("BROWSER_IDENTIFIER", "aws.browser.v1")
        aws_session_id = browser_client.start(
            identifier=identifier,
            session_timeout_seconds=session_timeout
        )
        
        logger.info(f"Started AgentCore browser session: {aws_session_id}")
        
        # Get CDP connection details
        cdp_url, cdp_headers = browser_client.generate_ws_headers()
        
        # Connect to browser via CDP
        browser = await playwright.chromium.connect_over_cdp(
            endpoint_url=cdp_url,
            headers=cdp_headers
        )
        
        # Get default context and create page
        if not browser.contexts:
            raise RuntimeError("No browser contexts available")
        
        context = browser.contexts[0]
        page = await context.new_page()
        
        # Create session object
        session = BrowserSession(
            session_id=session_id,
            description=description,
            region=region,
            browser_client=browser_client,
            browser=browser,
            context=context,
            page=page,
            timeout=session_timeout,
            recording_enabled=enable_recording
        )
        
        # Add main tab
        session.tabs["main"] = page
        
        # Store session
        sessions[session_id] = session
        
        # Generate Live View URL
        live_view_url = f"https://console.aws.amazon.com/bedrock/home?region={region}#/agentcore/browser/sessions/{aws_session_id}"
        
        result = f"""✅ Browser session created successfully!

Session ID: {session_id}
Description: {description}
Region: {region}
Timeout: {session_timeout} seconds
Recording: {'Enabled' if enable_recording else 'Disabled'}

Live View URL: {live_view_url}

You can now use this session_id with other tools like navigate, interact, extract_content, etc.
The session will remain active for {session_timeout} seconds or until you close it.
"""
        
        return [TextContent(type="text", text=result)]
    
    except Exception as e:
        logger.error(f"Failed to create session: {e}", exc_info=True)
        return [TextContent(type="text", text=f"Error creating session: {str(e)}")]



async def handle_navigate(args: Dict[str, Any]) -> List[TextContent]:
    """Navigate to a URL"""
    session_id = args["session_id"]
    url = args["url"]
    wait_for = args.get("wait_for", "networkidle")
    
    if session_id not in sessions:
        return [TextContent(type="text", text=f"Error: Session '{session_id}' not found")]
    
    session = sessions[session_id]
    session.update_last_used()
    
    try:
        page = session.tabs.get(session.active_tab_id, session.page)
        await page.goto(url)
        await page.wait_for_load_state(wait_for)
        
        return [TextContent(
            type="text",
            text=f"✅ Navigated to {url}\nCurrent URL: {page.url}"
        )]
    
    except Exception as e:
        return [TextContent(type="text", text=f"Error navigating: {str(e)}")]


async def handle_interact(args: Dict[str, Any]) -> List[TextContent]:
    """Handle page interactions"""
    session_id = args["session_id"]
    action = args["action"]
    
    if session_id not in sessions:
        return [TextContent(type="text", text=f"Error: Session '{session_id}' not found")]
    
    session = sessions[session_id]
    session.update_last_used()
    page = session.tabs.get(session.active_tab_id, session.page)
    
    try:
        if action == "click":
            selector = args["selector"]
            await page.click(selector)
            return [TextContent(type="text", text=f"✅ Clicked element: {selector}")]
        
        elif action == "type":
            selector = args["selector"]
            text = args["text"]
            await page.fill(selector, text)
            return [TextContent(type="text", text=f"✅ Typed text into: {selector}")]
        
        elif action == "press_key":
            key = args["key"]
            await page.keyboard.press(key)
            return [TextContent(type="text", text=f"✅ Pressed key: {key}")]
        
        elif action == "scroll":
            scroll_amount = args.get("scroll_amount", 500)
            await page.evaluate(f"window.scrollBy(0, {scroll_amount})")
            return [TextContent(type="text", text=f"✅ Scrolled {scroll_amount} pixels")]
        
        else:
            return [TextContent(type="text", text=f"Error: Unknown action '{action}'")]
    
    except Exception as e:
        return [TextContent(type="text", text=f"Error during {action}: {str(e)}")]


async def handle_extract_content(args: Dict[str, Any]) -> List[TextContent]:
    """Extract content from page"""
    session_id = args["session_id"]
    content_type = args["content_type"]
    selector = args.get("selector")
    
    if session_id not in sessions:
        return [TextContent(type="text", text=f"Error: Session '{session_id}' not found")]
    
    session = sessions[session_id]
    session.update_last_used()
    page = session.tabs.get(session.active_tab_id, session.page)
    
    try:
        if content_type == "text":
            if selector:
                content = await page.text_content(selector)
            else:
                content = await page.evaluate("document.body.innerText")
            return [TextContent(type="text", text=f"Extracted text:\n\n{content}")]
        
        elif content_type == "html":
            if selector:
                content = await page.inner_html(selector)
            else:
                content = await page.content()
            # Truncate if too long
            if len(content) > 5000:
                content = content[:5000] + "\n\n... (truncated)"
            return [TextContent(type="text", text=f"Extracted HTML:\n\n{content}")]
        
        elif content_type == "attribute":
            if not selector:
                return [TextContent(type="text", text="Error: selector required for attribute extraction")]
            attribute = args.get("attribute")
            if not attribute:
                return [TextContent(type="text", text="Error: attribute name required")]
            content = await page.get_attribute(selector, attribute)
            return [TextContent(type="text", text=f"Attribute '{attribute}': {content}")]
        
        else:
            return [TextContent(type="text", text=f"Error: Unknown content_type '{content_type}'")]
    
    except Exception as e:
        return [TextContent(type="text", text=f"Error extracting content: {str(e)}")]



async def handle_execute_script(args: Dict[str, Any]) -> List[TextContent]:
    """Execute JavaScript"""
    session_id = args["session_id"]
    script = args["script"]
    
    if session_id not in sessions:
        return [TextContent(type="text", text=f"Error: Session '{session_id}' not found")]
    
    session = sessions[session_id]
    session.update_last_used()
    page = session.tabs.get(session.active_tab_id, session.page)
    
    try:
        result = await page.evaluate(script)
        return [TextContent(type="text", text=f"Script result:\n\n{result}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error executing script: {str(e)}")]


async def handle_screenshot(args: Dict[str, Any]) -> List[TextContent]:
    """Take screenshot"""
    session_id = args["session_id"]
    path = args.get("path")
    selector = args.get("selector")
    full_page = args.get("full_page", False)
    
    if session_id not in sessions:
        return [TextContent(type="text", text=f"Error: Session '{session_id}' not found")]
    
    session = sessions[session_id]
    session.update_last_used()
    page = session.tabs.get(session.active_tab_id, session.page)
    
    try:
        # Generate path if not provided
        if not path:
            screenshots_dir = os.getenv("BROWSER_SCREENSHOTS_DIR", "screenshots")
            os.makedirs(screenshots_dir, exist_ok=True)
            path = os.path.join(screenshots_dir, f"screenshot_{int(time.time())}.png")
        
        # Take screenshot
        if selector:
            element = await page.query_selector(selector)
            if element:
                await element.screenshot(path=path)
            else:
                return [TextContent(type="text", text=f"Error: Element '{selector}' not found")]
        else:
            await page.screenshot(path=path, full_page=full_page)
        
        return [TextContent(type="text", text=f"✅ Screenshot saved to: {path}")]
    
    except Exception as e:
        return [TextContent(type="text", text=f"Error taking screenshot: {str(e)}")]


async def handle_manage_tabs(args: Dict[str, Any]) -> List[TextContent]:
    """Manage browser tabs"""
    session_id = args["session_id"]
    action = args["action"]
    
    if session_id not in sessions:
        return [TextContent(type="text", text=f"Error: Session '{session_id}' not found")]
    
    session = sessions[session_id]
    session.update_last_used()
    
    try:
        if action == "new_tab":
            tab_id = args.get("tab_id", f"tab_{len(session.tabs) + 1}")
            if tab_id in session.tabs:
                return [TextContent(type="text", text=f"Error: Tab '{tab_id}' already exists")]
            
            new_page = await session.context.new_page()
            session.tabs[tab_id] = new_page
            session.active_tab_id = tab_id
            
            return [TextContent(type="text", text=f"✅ Created new tab: {tab_id} (now active)")]
        
        elif action == "switch_tab":
            tab_id = args.get("tab_id")
            if not tab_id or tab_id not in session.tabs:
                available = ", ".join(session.tabs.keys())
                return [TextContent(type="text", text=f"Error: Tab '{tab_id}' not found. Available: {available}")]
            
            session.active_tab_id = tab_id
            page = session.tabs[tab_id]
            await page.bring_to_front()
            
            return [TextContent(type="text", text=f"✅ Switched to tab: {tab_id}")]
        
        elif action == "close_tab":
            tab_id = args.get("tab_id", session.active_tab_id)
            if tab_id not in session.tabs:
                return [TextContent(type="text", text=f"Error: Tab '{tab_id}' not found")]
            
            await session.tabs[tab_id].close()
            del session.tabs[tab_id]
            
            # Switch to another tab if current was closed
            if session.active_tab_id == tab_id and session.tabs:
                session.active_tab_id = next(iter(session.tabs.keys()))
            
            return [TextContent(type="text", text=f"✅ Closed tab: {tab_id}")]
        
        elif action == "list_tabs":
            tabs_info = []
            for tab_id, page in session.tabs.items():
                is_active = "✓" if tab_id == session.active_tab_id else " "
                tabs_info.append(f"[{is_active}] {tab_id}: {page.url}")
            
            result = "Active tabs:\n\n" + "\n".join(tabs_info)
            return [TextContent(type="text", text=result)]
        
        else:
            return [TextContent(type="text", text=f"Error: Unknown action '{action}'")]
    
    except Exception as e:
        return [TextContent(type="text", text=f"Error managing tabs: {str(e)}")]



async def handle_list_sessions(args: Dict[str, Any]) -> List[TextContent]:
    """List all active sessions"""
    if not sessions:
        return [TextContent(type="text", text="No active sessions")]
    
    session_list = []
    for sid, session in sessions.items():
        age = int(time.time() - session.created_at)
        idle = int(time.time() - session.last_used)
        session_list.append(
            f"• {sid}\n"
            f"  Description: {session.description}\n"
            f"  Region: {session.region}\n"
            f"  Age: {age}s, Idle: {idle}s\n"
            f"  Tabs: {len(session.tabs)}, Active: {session.active_tab_id}"
        )
    
    result = f"Active sessions ({len(sessions)}):\n\n" + "\n\n".join(session_list)
    return [TextContent(type="text", text=result)]


async def handle_get_session_info(args: Dict[str, Any]) -> List[TextContent]:
    """Get session information"""
    session_id = args["session_id"]
    
    if session_id not in sessions:
        return [TextContent(type="text", text=f"Error: Session '{session_id}' not found")]
    
    session = sessions[session_id]
    page = session.tabs.get(session.active_tab_id, session.page)
    
    age = int(time.time() - session.created_at)
    idle = int(time.time() - session.last_used)
    
    info = f"""Session Information:

Session ID: {session_id}
Description: {session.description}
Region: {session.region}
Status: Active
Age: {age} seconds
Idle: {idle} seconds
Timeout: {session.timeout} seconds

Current URL: {page.url if page else 'N/A'}
Active Tab: {session.active_tab_id}
Total Tabs: {len(session.tabs)}
Recording: {'Enabled' if session.recording_enabled else 'Disabled'}

Tabs:
"""
    
    for tab_id, tab_page in session.tabs.items():
        is_active = "✓" if tab_id == session.active_tab_id else " "
        info += f"  [{is_active}] {tab_id}: {tab_page.url}\n"
    
    return [TextContent(type="text", text=info)]


async def handle_close_session(args: Dict[str, Any]) -> List[TextContent]:
    """Close a session"""
    session_id = args["session_id"]
    
    if session_id not in sessions:
        return [TextContent(type="text", text=f"Error: Session '{session_id}' not found")]
    
    try:
        await close_session_internal(session_id)
        return [TextContent(type="text", text=f"✅ Session '{session_id}' closed successfully")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error closing session: {str(e)}")]


async def handle_get_live_view_url(args: Dict[str, Any]) -> List[TextContent]:
    """Get Live View URL"""
    session_id = args["session_id"]
    
    if session_id not in sessions:
        return [TextContent(type="text", text=f"Error: Session '{session_id}' not found")]
    
    session = sessions[session_id]
    
    # Note: This is a simplified URL. In production, you'd get the actual session ID from browser_client
    live_view_url = f"https://console.aws.amazon.com/bedrock/home?region={session.region}#/agentcore/browser/sessions"
    
    result = f"""Live View URL for session '{session_id}':

{live_view_url}

Open this URL in your browser to:
• Watch the browser session in real-time
• Interact with the page manually if needed
• Debug automation issues visually
• Take over control when necessary

Note: You need appropriate AWS IAM permissions to access the Live View.
"""
    
    return [TextContent(type="text", text=result)]


async def main():
    """Main entry point for the MCP server"""
    from mcp.server.stdio import stdio_server
    
    logger.info("Starting AgentCore Browser MCP Server")
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


# Run the server
if __name__ == "__main__":
    asyncio.run(main())
