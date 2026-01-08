# Advanced Session Management

Learn advanced techniques for managing browser sessions effectively.

## Session Persistence

### Cross-Request Session Maintenance

AgentCore Browser sessions persist across multiple MCP tool calls:

```python
# Request 1: Create session
await create_browser_session(
    session_id="persistent-session",
    description="Multi-step workflow"
)

# Request 2: Navigate (same session)
await navigate(
    session_id="persistent-session",
    url="https://example.com/login"
)

# Request 3: Login (same session, cookies preserved)
await interact(
    session_id="persistent-session",
    action="type",
    selector="input[name='username']",
    text="user@example.com"
)

# Request 4: Continue workflow (session state maintained)
await navigate(
    session_id="persistent-session",
    url="https://example.com/dashboard"
)
```

**Key Points:**
- Session state is maintained in MCP server memory
- Cookies, local storage, and navigation history persist
- Multiple operations can use the same session_id
- Sessions remain active until timeout or manual close

### Session Lifecycle Management

**1. Creation**
```python
session = await create_browser_session(
    session_id="workflow-001",
    description="Order processing workflow",
    session_timeout=7200  # 2 hours
)
```

**2. Active Use**
```python
# Session is automatically kept alive during operations
await navigate(session_id="workflow-001", ...)
await interact(session_id="workflow-001", ...)
# Last used timestamp is updated with each operation
```

**3. Monitoring**
```python
# Check session status
info = await get_session_info(session_id="workflow-001")
# Shows: age, idle time, current URL, tabs
```

**4. Cleanup**
```python
# Manual close
await close_session(session_id="workflow-001")

# Or let it timeout automatically
# Session expires after idle for session_timeout seconds
```

## Parallel Sessions

Run multiple browser sessions simultaneously for batch processing.

### Pattern: Parallel Data Collection

```python
# Create multiple sessions
session_ids = []
for i in range(5):
    session_id = f"scraper-{i}"
    await create_browser_session(
        session_id=session_id,
        description=f"Scraping batch {i}"
    )
    session_ids.append(session_id)

# Process URLs in parallel (conceptually)
urls = [
    "https://site1.com",
    "https://site2.com",
    "https://site3.com",
    "https://site4.com",
    "https://site5.com"
]

for session_id, url in zip(session_ids, urls):
    await navigate(session_id=session_id, url=url)
    # Extract data from each...

# Clean up all sessions
for session_id in session_ids:
    await close_session(session_id=session_id)
```

### Pattern: A/B Testing

```python
# Session A: Control
await create_browser_session(
    session_id="test-control",
    description="Control group"
)

# Session B: Variant
await create_browser_session(
    session_id="test-variant",
    description="Variant group"
)

# Run same workflow in both
for session_id in ["test-control", "test-variant"]:
    await navigate(session_id=session_id, url="https://example.com")
    # Perform actions...
    await screenshot(session_id=session_id, path=f"{session_id}.png")

# Compare results
```

### Limits

- **Maximum concurrent sessions**: 500 per account
- **Recommended**: 10-20 for most use cases
- **Monitor usage**: Use `list_sessions()` to track active sessions

## Session Timeout Strategies

### Short-Lived Sessions (< 15 minutes)

For quick, one-off tasks:

```python
await create_browser_session(
    session_id="quick-check",
    description="Quick status check",
    session_timeout=900  # 15 minutes
)

# Perform quick task
await navigate(...)
await extract_content(...)

# Close immediately
await close_session(session_id="quick-check")
```

**Use cases:**
- Status checks
- Quick data extraction
- Simple form submissions

### Medium Sessions (15-60 minutes)

For typical workflows:

```python
await create_browser_session(
    session_id="standard-workflow",
    description="Standard automation workflow",
    session_timeout=3600  # 1 hour (default)
)
```

**Use cases:**
- Multi-step forms
- Data collection workflows
- Testing scenarios

### Long-Running Sessions (1-8 hours)

For extended operations:

```python
await create_browser_session(
    session_id="long-running",
    description="Extended data collection",
    session_timeout=28800  # 8 hours (maximum)
)
```

**Use cases:**
- Large-scale scraping
- Monitoring tasks
- Complex multi-page workflows

**Important:** Longer timeouts cost more. Use shortest timeout needed.

## Session State Management

### Cookies and Authentication

Sessions preserve authentication state:

```python
# Create session
await create_browser_session(session_id="auth-session", ...)

# Login
await navigate(session_id="auth-session", url="https://example.com/login")
await interact(session_id="auth-session", action="type", selector="input[name='email']", text="user@example.com")
await interact(session_id="auth-session", action="type", selector="input[name='password']", text="password")
await interact(session_id="auth-session", action="click", selector="button[type='submit']")

# Cookies are now set, navigate to protected pages
await navigate(session_id="auth-session", url="https://example.com/dashboard")
# Still authenticated!

await navigate(session_id="auth-session", url="https://example.com/profile")
# Still authenticated!
```

### Local Storage

Local storage persists across navigations:

```python
# Set local storage
await execute_script(
    session_id="session",
    script="localStorage.setItem('key', 'value')"
)

# Navigate to another page
await navigate(session_id="session", url="https://example.com/other")

# Local storage still available
result = await execute_script(
    session_id="session",
    script="return localStorage.getItem('key')"
)
# Returns: 'value'
```

### Navigation History

Use back/forward navigation:

```python
# Navigate through pages
await navigate(session_id="session", url="https://example.com/page1")
await navigate(session_id="session", url="https://example.com/page2")
await navigate(session_id="session", url="https://example.com/page3")

# Go back
await execute_script(session_id="session", script="history.back()")
# Now on page2

# Go forward
await execute_script(session_id="session", script="history.forward()")
# Now on page3
```

## Multi-Tab Workflows

Manage multiple tabs within a single session.

### Creating Tabs

```python
# Create session
await create_browser_session(session_id="multi-tab", ...)

# Main tab is created automatically (id: "main")

# Create additional tabs
await manage_tabs(
    session_id="multi-tab",
    action="new_tab",
    tab_id="tab2"
)

await manage_tabs(
    session_id="multi-tab",
    action="new_tab",
    tab_id="tab3"
)
```

### Switching Between Tabs

```python
# List all tabs
await manage_tabs(
    session_id="multi-tab",
    action="list_tabs"
)

# Switch to specific tab
await manage_tabs(
    session_id="multi-tab",
    action="switch_tab",
    tab_id="tab2"
)

# All subsequent operations use tab2
await navigate(session_id="multi-tab", url="https://example.com")
```

### Pattern: Comparing Data Across Sites

```python
# Create session
await create_browser_session(session_id="comparison", ...)

# Main tab: Site 1
await navigate(session_id="comparison", url="https://site1.com/product")
price1 = await extract_content(
    session_id="comparison",
    content_type="text",
    selector=".price"
)

# New tab: Site 2
await manage_tabs(session_id="comparison", action="new_tab", tab_id="site2")
await navigate(session_id="comparison", url="https://site2.com/product")
price2 = await extract_content(
    session_id="comparison",
    content_type="text",
    selector=".price"
)

# New tab: Site 3
await manage_tabs(session_id="comparison", action="new_tab", tab_id="site3")
await navigate(session_id="comparison", url="https://site3.com/product")
price3 = await extract_content(
    session_id="comparison",
    content_type="text",
    selector=".price"
)

# Compare prices...
```

### Closing Tabs

```python
# Close specific tab
await manage_tabs(
    session_id="multi-tab",
    action="close_tab",
    tab_id="tab2"
)

# Close current tab (active tab)
await manage_tabs(
    session_id="multi-tab",
    action="close_tab"
)
```

## Session Monitoring

### Listing Active Sessions

```python
# Get all active sessions
sessions = await list_sessions()

# Shows:
# - Session IDs
# - Descriptions
# - Age and idle time
# - Number of tabs
```

### Getting Session Details

```python
info = await get_session_info(session_id="your-session")

# Returns:
# - Current URL
# - Active tab
# - All tabs with URLs
# - Age and idle time
# - Recording status
```

### Live View Monitoring

```python
# Get Live View URL
url = await get_live_view_url(session_id="your-session")

# Open in browser to:
# - Watch real-time video stream
# - See what automation is doing
# - Intervene manually if needed
# - Debug visual issues
```

## Error Handling

### Session Not Found

```python
# Always check if session exists
sessions = await list_sessions()

if "my-session" in sessions:
    await navigate(session_id="my-session", ...)
else:
    # Create session first
    await create_browser_session(session_id="my-session", ...)
```

### Session Expired

```python
# Sessions expire after timeout
# Check session info before long operations
info = await get_session_info(session_id="my-session")

# If idle too long, recreate
if info["idle_time"] > 3000:  # 50 minutes
    await close_session(session_id="my-session")
    await create_browser_session(session_id="my-session", ...)
```

### Graceful Cleanup

```python
try:
    # Your automation
    await create_browser_session(...)
    await navigate(...)
    await interact(...)
    
except Exception as e:
    print(f"Error: {e}")
    
finally:
    # Always clean up
    try:
        await close_session(session_id="your-session")
    except:
        pass  # Session might already be closed
```

## Best Practices

### 1. Use Descriptive Session IDs

```python
# Good
"order-processing-2024-01-05-batch-1"
"qa-test-login-flow-chrome"
"scrape-products-electronics-category"

# Bad
"session1"
"test"
"temp"
```

### 2. Set Appropriate Timeouts

```python
# Match timeout to workflow duration
# Add buffer for unexpected delays

# Quick task: 15 minutes
session_timeout=900

# Standard workflow: 1 hour
session_timeout=3600

# Long operation: 2-4 hours
session_timeout=14400
```

### 3. Monitor Resource Usage

```python
# Periodically check active sessions
sessions = await list_sessions()

# Close unused sessions
for session in sessions:
    if session["idle_time"] > 1800:  # 30 minutes idle
        await close_session(session_id=session["id"])
```

### 4. Use Session Recording for Production

```python
# Enable recording for audit trails
await create_browser_session(
    session_id="production-workflow",
    description="Production order processing",
    enable_recording=True  # Important for debugging
)
```

### 5. Implement Retry Logic

```python
max_retries = 3
for attempt in range(max_retries):
    try:
        await navigate(session_id="session", url="https://example.com")
        break
    except Exception as e:
        if attempt == max_retries - 1:
            raise
        # Wait before retry
        await execute_script(
            session_id="session",
            script="await new Promise(r => setTimeout(r, 2000))"
        )
```

## Advanced Patterns

### Pattern: Session Pooling

Reuse sessions for multiple tasks:

```python
# Create pool of sessions
pool = []
for i in range(5):
    session_id = f"pool-{i}"
    await create_browser_session(session_id=session_id, ...)
    pool.append(session_id)

# Use sessions from pool
def get_available_session():
    # Return least recently used session
    sessions_info = await list_sessions()
    return min(sessions_info, key=lambda s: s["last_used"])

# Process tasks
for task in tasks:
    session_id = get_available_session()
    await navigate(session_id=session_id, url=task["url"])
    # Process...
```

### Pattern: Session Checkpointing

Save and restore session state:

```python
# Save checkpoint
checkpoint = {
    "url": await execute_script(session_id="session", script="return window.location.href"),
    "cookies": await execute_script(session_id="session", script="return document.cookie"),
    "localStorage": await execute_script(session_id="session", script="return JSON.stringify(localStorage)")
}

# Later, restore checkpoint
await navigate(session_id="session", url=checkpoint["url"])
await execute_script(
    session_id="session",
    script=f"document.cookie = '{checkpoint['cookies']}'"
)
await execute_script(
    session_id="session",
    script=f"Object.assign(localStorage, JSON.parse('{checkpoint['localStorage']}'))"
)
```

### Pattern: Conditional Session Creation

Create sessions only when needed:

```python
def ensure_session(session_id):
    sessions = await list_sessions()
    if session_id not in [s["id"] for s in sessions]:
        await create_browser_session(session_id=session_id, ...)
    return session_id

# Use in workflow
session_id = ensure_session("my-workflow")
await navigate(session_id=session_id, ...)
```

## Summary

Key takeaways:
- ✅ Sessions persist across multiple MCP tool calls
- ✅ Use appropriate timeouts for your workflow
- ✅ Parallel sessions enable batch processing
- ✅ Multi-tab workflows allow complex scenarios
- ✅ Always monitor and clean up sessions
- ✅ Implement error handling and retries
- ✅ Use session recording for production workflows

Next: Read `web-automation-patterns.md` for automation techniques.
