# AgentCore Browser Power - Design Document

## Overview

This power provides comprehensive browser automation capabilities using AWS Bedrock AgentCore Browser through an MCP server interface.

## Key Design Decisions

### 1. Session Persistence Across Requests

**Decision:** Maintain session state in MCP server memory

**Rationale:**
- AgentCore Browser sessions are expensive to create
- Workflows often require multiple operations on the same page
- Authentication state needs to persist across operations
- Enables complex multi-step automations

**Implementation:**
```python
# Global session dictionary in MCP server
sessions: Dict[str, BrowserSession] = {}

# Sessions persist across MCP tool calls
# User can reference same session_id in multiple requests
```

**Benefits:**
- ✅ Efficient resource usage
- ✅ Maintains cookies and authentication
- ✅ Supports complex workflows
- ✅ Natural user experience

### 2. Headless Cloud Browser with Live View

**Decision:** Use AgentCore Browser (cloud-based, headless) with Live View option

**Rationale:**
- AgentCore Browser runs in AWS cloud (always headless)
- No local browser installation required
- Automatic scaling and isolation
- Live View provides visual monitoring when needed

**Implementation:**
```python
# Browser runs in AWS cloud
browser_client = BrowserClient(region=region)
session_id = browser_client.start(identifier="aws.browser.v1")

# Connect via CDP
cdp_url, cdp_headers = browser_client.generate_ws_headers()
browser = await playwright.chromium.connect_over_cdp(
    endpoint_url=cdp_url,
    headers=cdp_headers
)

# Live View URL for monitoring
live_view_url = f"https://console.aws.amazon.com/bedrock/home?region={region}#/agentcore/browser/sessions/{session_id}"
```

**Benefits:**
- ✅ No local setup required
- ✅ Enterprise-grade security
- ✅ Automatic scaling
- ✅ Visual debugging via Live View
- ✅ Session recording capability

### 3. Unified Interaction Interface

**Decision:** Single `interact` tool for multiple action types

**Rationale:**
- Simpler API surface
- Easier for AI agents to use
- Reduces tool count
- Consistent parameter patterns

**Implementation:**
```python
@app.tool()
async def interact(
    session_id: str,
    action: Literal["click", "type", "press_key", "scroll"],
    selector: Optional[str] = None,
    text: Optional[str] = None,
    key: Optional[str] = None,
    scroll_amount: Optional[int] = None
) -> dict:
    # Single tool handles multiple interaction types
```

**Alternative Considered:**
- Separate tools: `click`, `type`, `press_key`, `scroll`
- Rejected because: More tools to manage, harder for agents to discover

### 4. Session Timeout Management

**Decision:** Configurable timeout with automatic cleanup

**Rationale:**
- Prevent resource leaks
- Balance cost and usability
- Support both short and long workflows

**Implementation:**
```python
@dataclass
class BrowserSession:
    timeout: int = 3600  # Default 1 hour
    last_used: float = field(default_factory=time.time)
    
    def is_expired(self) -> bool:
        return (time.time() - self.last_used) > self.timeout

# Periodic cleanup
async def cleanup_expired_sessions():
    expired = [sid for sid, s in sessions.items() if s.is_expired()]
    for session_id in expired:
        await close_session_internal(session_id)
```

**Timeout Options:**
- Short (900s / 15 min): Quick tasks
- Medium (3600s / 1 hour): Standard workflows
- Long (28800s / 8 hours): Extended operations

### 5. Multi-Tab Support

**Decision:** Support multiple tabs within a single session

**Rationale:**
- Common use case: comparing data across sites
- More efficient than multiple sessions
- Natural browser behavior

**Implementation:**
```python
@dataclass
class BrowserSession:
    tabs: Dict[str, Page] = field(default_factory=dict)
    active_tab_id: str = "main"
    
# Tab management
await manage_tabs(action="new_tab", tab_id="tab2")
await manage_tabs(action="switch_tab", tab_id="tab2")
await manage_tabs(action="close_tab", tab_id="tab2")
```

### 6. Error Handling Strategy

**Decision:** Return descriptive error messages, don't raise exceptions

**Rationale:**
- MCP tools should return results, not throw
- AI agents can better handle text responses
- Enables graceful degradation

**Implementation:**
```python
try:
    await page.click(selector)
    return [TextContent(type="text", text=f"✅ Clicked element: {selector}")]
except Exception as e:
    return [TextContent(type="text", text=f"Error: {str(e)}")]
```

## Architecture

### Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         Kiro Agent                          │
└────────────────────────┬────────────────────────────────────┘
                         │ MCP Protocol
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              AgentCore Browser MCP Server                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Session Manager                                      │  │
│  │  - sessions: Dict[str, BrowserSession]               │  │
│  │  - cleanup_expired_sessions()                        │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Tool Handlers                                        │  │
│  │  - create_browser_session()                          │  │
│  │  - navigate()                                         │  │
│  │  - interact()                                         │  │
│  │  - extract_content()                                  │  │
│  │  - execute_script()                                   │  │
│  │  - screenshot()                                       │  │
│  │  - manage_tabs()                                      │  │
│  │  - list_sessions()                                    │  │
│  │  - get_session_info()                                 │  │
│  │  - close_session()                                    │  │
│  │  - get_live_view_url()                               │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │ Playwright + CDP
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              AWS Bedrock AgentCore Browser                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  BrowserClient                                        │  │
│  │  - start() → session_id                              │  │
│  │  - generate_ws_headers() → CDP URL                   │  │
│  │  - stop()                                             │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Cloud Browser Instance (Chromium)                   │  │
│  │  - Isolated microVM                                   │  │
│  │  - Session recording (optional)                       │  │
│  │  - Live View streaming                                │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Session Creation**
   ```
   Agent → MCP Server → BrowserClient.start() → CDP Connection → Browser Instance
   ```

2. **Browser Operation**
   ```
   Agent → MCP Tool → Session Lookup → Playwright API → CDP → Browser
   ```

3. **Session Cleanup**
   ```
   Timeout/Manual → close_session() → Browser.close() → BrowserClient.stop()
   ```

## Tool Design

### Tool Categories

1. **Session Management** (4 tools)
   - `create_browser_session` - Initialize
   - `list_sessions` - Discover
   - `get_session_info` - Inspect
   - `close_session` - Cleanup

2. **Browser Automation** (5 tools)
   - `navigate` - Page navigation
   - `interact` - Element interaction
   - `extract_content` - Data extraction
   - `execute_script` - JavaScript execution
   - `screenshot` - Visual capture

3. **Advanced Features** (2 tools)
   - `manage_tabs` - Multi-tab workflows
   - `get_live_view_url` - Visual monitoring

### Tool Parameter Design

**Consistent Patterns:**
- All tools (except `list_sessions`) require `session_id`
- Optional parameters have sensible defaults
- Enums for action types (type-safe)
- Clear parameter descriptions

**Example:**
```python
{
    "session_id": "required-string",
    "action": "enum-value",
    "selector": "optional-css-selector",
    "text": "optional-text-content"
}
```

## Security Considerations

### 1. AWS Credentials

- Never hardcode credentials
- Use AWS credential chain (env vars, ~/.aws/credentials, IAM roles)
- Require minimal IAM permissions

### 2. Session Isolation

- Each session runs in isolated microVM
- Sessions don't share state
- Automatic cleanup prevents leaks

### 3. Input Validation

- Validate session_id format
- Sanitize JavaScript code (user responsibility)
- Validate CSS selectors

### 4. Resource Limits

- Maximum 500 concurrent sessions
- Configurable timeouts
- Automatic cleanup of expired sessions

## Performance Considerations

### 1. Session Reuse

- Encourage session reuse for multiple operations
- Avoid creating new session for each operation
- Document session lifecycle best practices

### 2. Parallel Sessions

- Support up to 500 concurrent sessions
- Enable batch processing
- Document parallel patterns

### 3. Network Optimization

- Use appropriate wait conditions
- Minimize unnecessary screenshots
- Close unused tabs

### 4. Memory Management

- Store only essential session data
- Clean up expired sessions automatically
- Limit screenshot storage

## Testing Strategy

### Unit Tests

- Test each tool handler independently
- Mock AWS BrowserClient
- Test error handling

### Integration Tests

- Test with real AgentCore Browser
- Verify session persistence
- Test multi-tab workflows

### End-to-End Tests

- Complete automation workflows
- Authentication flows
- Error recovery scenarios

## Future Enhancements

### Potential Additions

1. **Cookie Management**
   - Export/import cookies
   - Cookie-based authentication

2. **Network Interception**
   - Capture API requests
   - Mock responses

3. **Performance Metrics**
   - Page load times
   - Resource usage

4. **Advanced Selectors**
   - XPath support
   - Text-based selection

5. **File Downloads**
   - Handle file downloads
   - Upload files

6. **Mobile Emulation**
   - Mobile viewport
   - Touch events

### Not Planned

- Local browser support (use Playwright directly)
- Browser extensions (not supported by AgentCore)
- Multiple browser engines (AgentCore uses Chromium)

## Documentation Structure

### POWER.md
- Overview and quick start
- Tool reference
- Configuration
- Best practices

### Steering Files
- `getting-started.md` - Complete setup guide
- `session-management.md` - Advanced session techniques
- `troubleshooting.md` - Common issues and solutions

### Additional Docs
- `README.md` - Installation and quick reference
- `example_usage.md` - Real-world examples
- `DESIGN.md` - This document

## Comparison with Alternatives

### vs. Local Playwright

| Feature | AgentCore Browser | Local Playwright |
|---------|------------------|------------------|
| Setup | No local install | Requires installation |
| Scaling | Automatic | Manual |
| Security | Isolated cloud | Local machine |
| Cost | Pay per use | Free |
| Live View | Built-in | Manual setup |
| Recording | Built-in | Manual setup |

### vs. Strands Browser Tool

| Feature | This Power | Strands Tool |
|---------|-----------|--------------|
| Integration | MCP-based | Strands-native |
| Session Mgmt | Explicit | Implicit |
| Documentation | Comprehensive | Code-focused |
| Flexibility | High | Medium |

## Success Metrics

### User Experience
- Time to first automation: < 15 minutes
- Session creation success rate: > 95%
- Error message clarity: User can resolve without docs

### Performance
- Session creation time: < 10 seconds
- Operation latency: < 2 seconds
- Concurrent sessions: Up to 500

### Reliability
- Session stability: > 99%
- Automatic cleanup: 100%
- Error recovery: Graceful degradation

## Conclusion

This power provides a production-ready browser automation solution with:
- ✅ Persistent session management
- ✅ Cloud-based execution
- ✅ Comprehensive tooling
- ✅ Excellent documentation
- ✅ Real-world examples

The design balances simplicity, power, and reliability for AI agent workflows.
