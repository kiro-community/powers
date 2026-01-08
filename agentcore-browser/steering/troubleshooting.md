# Troubleshooting Guide

Common issues and solutions for AgentCore Browser.

## Installation Issues

### "uv command not found"

**Problem:** uv package manager not installed

**Solution:**
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Restart terminal
source ~/.bashrc  # or ~/.zshrc

# Verify
uv --version
```

### "Playwright not installed"

**Problem:** Playwright browsers not downloaded

**Solution:**
```bash
cd ~/.kiro/powers/agentcore-browser
uv run playwright install chromium

# If that fails, try:
uv sync
uv run playwright install chromium
```

### "MCP server not connected"

**Problem:** MCP server failed to start

**Solutions:**
1. Check MCP server logs in Kiro
2. Verify Python version: `python3 --version` (need 3.10+)
3. Reinstall dependencies:
   ```bash
   cd ~/.kiro/powers/agentcore-browser
   rm -rf .venv
   uv sync
   ```
4. Restart Kiro

## AWS Credential Issues

### "AWS credentials not configured"

**Problem:** No AWS credentials found

**Solution:**
```bash
# Configure AWS CLI
aws configure

# Enter:
# - AWS Access Key ID
# - AWS Secret Access Key
# - Default region (e.g., us-east-1)
# - Output format (json)

# Verify
aws sts get-caller-identity
```

### "AccessDeniedException"

**Problem:** Insufficient IAM permissions

**Solution:**
1. Check your IAM permissions include:
   ```json
   {
     "Effect": "Allow",
     "Action": [
       "bedrock-agentcore:CreateBrowser",
       "bedrock-agentcore:StartBrowserSession",
       "bedrock-agentcore:StopBrowserSession"
     ],
     "Resource": "*"
   }
   ```

2. Verify you're using correct AWS account:
   ```bash
   aws sts get-caller-identity
   ```

3. Try different region:
   ```python
   await create_browser_session(
       session_id="test",
       region="us-west-2"  # Try different region
   )
   ```

### "Region not supported"

**Problem:** AgentCore Browser not available in region

**Solution:**
Use supported regions:
- us-east-1 (N. Virginia)
- us-west-2 (Oregon)
- eu-central-1 (Frankfurt)
- ap-southeast-2 (Sydney)

```python
await create_browser_session(
    session_id="test",
    region="us-east-1"  # Use supported region
)
```

## Session Issues

### "Session not found"

**Problem:** Session doesn't exist or expired

**Solutions:**
1. List active sessions:
   ```python
   await list_sessions()
   ```

2. Create session if missing:
   ```python
   await create_browser_session(
       session_id="your-session",
       description="Your workflow"
   )
   ```

3. Check session hasn't expired:
   ```python
   info = await get_session_info(session_id="your-session")
   # Check idle_time
   ```

### "Session creation fails"

**Problem:** Cannot create new session

**Solutions:**
1. Check AWS credentials:
   ```bash
   aws sts get-caller-identity
   ```

2. Verify region is supported

3. Check session limit (max 500):
   ```python
   sessions = await list_sessions()
   # If too many, close unused ones
   ```

4. Try with minimal options:
   ```python
   await create_browser_session(
       session_id="test-minimal",
       description="Test"
   )
   ```

### "Session timeout too short"

**Problem:** Session expires before workflow completes

**Solution:**
Increase timeout:
```python
await create_browser_session(
    session_id="long-workflow",
    description="Extended workflow",
    session_timeout=28800  # 8 hours (maximum)
)
```

## Navigation Issues

### "Navigation timeout"

**Problem:** Page takes too long to load

**Solutions:**
1. Increase wait time:
   ```python
   await navigate(
       session_id="session",
       url="https://slow-site.com",
       wait_for="domcontentloaded"  # Don't wait for all resources
   )
   ```

2. Check URL is accessible:
   ```bash
   curl -I https://your-url.com
   ```

3. Try different wait condition:
   ```python
   # Options: 'load', 'domcontentloaded', 'networkidle'
   await navigate(
       session_id="session",
       url="https://example.com",
       wait_for="load"  # Faster but less complete
   )
   ```

### "ERR_NAME_NOT_RESOLVED"

**Problem:** Domain doesn't exist or DNS issue

**Solutions:**
1. Verify URL is correct
2. Check domain exists:
   ```bash
   nslookup example.com
   ```
3. Try with www prefix:
   ```python
   await navigate(
       session_id="session",
       url="https://www.example.com"  # Add www
   )
   ```

### "ERR_CONNECTION_REFUSED"

**Problem:** Server refusing connections

**Solutions:**
1. Check if site is up:
   ```bash
   curl https://example.com
   ```
2. Try different protocol:
   ```python
   # Try http instead of https
   await navigate(
       session_id="session",
       url="http://example.com"
   )
   ```
3. Check if site blocks automation (use Live View to verify)

## Element Interaction Issues

### "Selector not found"

**Problem:** CSS selector doesn't match any element

**Solutions:**
1. Verify selector in browser DevTools:
   - Open site in regular browser
   - Right-click element → Inspect
   - Test selector in Console: `document.querySelector("your-selector")`

2. Wait for element to appear:
   ```python
   # Wait before interacting
   await execute_script(
       session_id="session",
       script="await new Promise(r => setTimeout(r, 2000))"
   )
   
   await interact(
       session_id="session",
       action="click",
       selector="button.submit"
   )
   ```

3. Use more specific selector:
   ```python
   # Instead of: "button"
   # Use: "button[type='submit']"
   # Or: "button.primary-button"
   # Or: "#submit-btn"
   ```

4. Check if element is in iframe:
   ```python
   # Switch to iframe first
   await execute_script(
       session_id="session",
       script="""
       const iframe = document.querySelector('iframe');
       const iframeDoc = iframe.contentDocument;
       return iframeDoc.querySelector('button').click();
       """
   )
   ```

### "Element not clickable"

**Problem:** Element is hidden, covered, or disabled

**Solutions:**
1. Scroll element into view:
   ```python
   await execute_script(
       session_id="session",
       script="""
       document.querySelector('button').scrollIntoView();
       """
   )
   
   await interact(
       session_id="session",
       action="click",
       selector="button"
   )
   ```

2. Wait for element to be clickable:
   ```python
   await execute_script(
       session_id="session",
       script="await new Promise(r => setTimeout(r, 1000))"
   )
   ```

3. Use JavaScript click instead:
   ```python
   await execute_script(
       session_id="session",
       script="document.querySelector('button').click()"
   )
   ```

### "Type action fails"

**Problem:** Cannot type into input field

**Solutions:**
1. Click field first:
   ```python
   await interact(
       session_id="session",
       action="click",
       selector="input[name='email']"
   )
   
   await interact(
       session_id="session",
       action="type",
       selector="input[name='email']",
       text="user@example.com"
   )
   ```

2. Clear field first:
   ```python
   await execute_script(
       session_id="session",
       script="document.querySelector('input[name=\"email\"]').value = ''"
   )
   
   await interact(
       session_id="session",
       action="type",
       selector="input[name='email']",
       text="user@example.com"
   )
   ```

3. Use JavaScript to set value:
   ```python
   await execute_script(
       session_id="session",
       script="""
       document.querySelector('input[name="email"]').value = 'user@example.com';
       document.querySelector('input[name="email"]').dispatchEvent(new Event('input'));
       """
   )
   ```

## Content Extraction Issues

### "Extracted content is empty"

**Problem:** Element exists but has no content

**Solutions:**
1. Wait for content to load:
   ```python
   await execute_script(
       session_id="session",
       script="await new Promise(r => setTimeout(r, 2000))"
   )
   
   await extract_content(
       session_id="session",
       content_type="text",
       selector=".content"
   )
   ```

2. Check if content is in different element:
   ```python
   # Try parent element
   await extract_content(
       session_id="session",
       content_type="html",
       selector=".parent-container"
   )
   ```

3. Use JavaScript to extract:
   ```python
   await execute_script(
       session_id="session",
       script="return document.querySelector('.content').textContent"
   )
   ```

### "HTML extraction truncated"

**Problem:** HTML content is too large

**Solution:**
Extract specific parts:
```python
# Instead of full page HTML
await extract_content(
    session_id="session",
    content_type="html"
)

# Extract specific section
await extract_content(
    session_id="session",
    content_type="html",
    selector="#main-content"
)
```

## JavaScript Execution Issues

### "Script execution fails"

**Problem:** JavaScript error in executed script

**Solutions:**
1. Test script in browser console first

2. Check for syntax errors:
   ```python
   # Bad: Missing return
   script = "document.title"
   
   # Good: Explicit return
   script = "return document.title"
   ```

3. Handle async operations:
   ```python
   # For async operations
   await execute_script(
       session_id="session",
       script="""
       return await new Promise(resolve => {
           setTimeout(() => resolve('done'), 1000);
       });
       """
   )
   ```

4. Wrap in try-catch:
   ```python
   await execute_script(
       session_id="session",
       script="""
       try {
           return document.querySelector('.element').textContent;
       } catch (e) {
           return 'Error: ' + e.message;
       }
       """
   )
   ```

## Screenshot Issues

### "Screenshot is blank"

**Problem:** Page not fully loaded

**Solutions:**
1. Wait before screenshot:
   ```python
   await navigate(session_id="session", url="https://example.com")
   
   # Wait for page to render
   await execute_script(
       session_id="session",
       script="await new Promise(r => setTimeout(r, 2000))"
   )
   
   await screenshot(session_id="session")
   ```

2. Use full_page option:
   ```python
   await screenshot(
       session_id="session",
       full_page=True
   )
   ```

### "Screenshot file not found"

**Problem:** Screenshot directory doesn't exist

**Solution:**
```bash
# Create screenshots directory
mkdir -p screenshots

# Or specify full path
await screenshot(
    session_id="session",
    path="/full/path/to/screenshot.png"
)
```

## Performance Issues

### "Operations are slow"

**Problem:** Browser operations taking too long

**Solutions:**
1. Use faster wait conditions:
   ```python
   await navigate(
       session_id="session",
       url="https://example.com",
       wait_for="domcontentloaded"  # Faster than 'networkidle'
   )
   ```

2. Disable images (if not needed):
   ```python
   # Note: This requires custom browser configuration
   # Contact AWS support for advanced options
   ```

3. Use parallel sessions for batch operations

4. Close unused tabs:
   ```python
   await manage_tabs(
       session_id="session",
       action="close_tab",
       tab_id="unused-tab"
   )
   ```

### "Too many sessions"

**Problem:** Hitting session limit

**Solution:**
```python
# Clean up old sessions
sessions = await list_sessions()

for session in sessions:
    if session["idle_time"] > 1800:  # 30 minutes
        await close_session(session_id=session["id"])
```

## Live View Issues

### "Live View URL doesn't work"

**Problem:** Cannot access Live View

**Solutions:**
1. Check IAM permissions for console access

2. Verify you're logged into correct AWS account

3. Check region matches session region

4. Try opening in incognito/private window

### "Live View shows black screen"

**Problem:** Session not active or expired

**Solutions:**
1. Check session is active:
   ```python
   await get_session_info(session_id="your-session")
   ```

2. Perform an operation to activate:
   ```python
   await navigate(
       session_id="your-session",
       url="https://example.com"
   )
   ```

## Debugging Strategies

### Enable Verbose Logging

Check MCP server logs in Kiro for detailed error messages.

### Use Live View

Monitor automation visually:
```python
url = await get_live_view_url(session_id="your-session")
# Open URL in browser to watch
```

### Take Screenshots

Capture state at each step:
```python
await screenshot(session_id="session", path="step1.png")
await interact(...)
await screenshot(session_id="session", path="step2.png")
await interact(...)
await screenshot(session_id="session", path="step3.png")
```

### Extract Page HTML

See what browser sees:
```python
html = await extract_content(
    session_id="session",
    content_type="html"
)
# Save to file for inspection
```

### Check Console Logs

```python
logs = await execute_script(
    session_id="session",
    script="""
    return console.logs || [];
    """
)
```

## Getting Help

### Check Documentation

1. Read POWER.md for overview
2. Check steering files for specific topics
3. Review AWS AgentCore Browser docs

### AWS Support

For AWS service issues:
1. Open AWS Support case
2. Include:
   - Session ID
   - Error messages
   - Region
   - Timestamp

### Kiro Support

For MCP/Kiro issues:
1. Check Kiro documentation
2. Review MCP server logs
3. Report issues with:
   - MCP server logs
   - Steps to reproduce
   - Expected vs actual behavior

## Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| "Session not found" | Session expired or doesn't exist | Create new session |
| "AccessDeniedException" | Missing IAM permissions | Add required permissions |
| "Region not supported" | Invalid region | Use supported region |
| "Selector not found" | Element doesn't exist | Verify selector, wait for element |
| "Navigation timeout" | Page load too slow | Increase timeout, check URL |
| "Connection refused" | Server down or blocking | Check site status, try different URL |
| "Maximum sessions exceeded" | Too many active sessions | Close unused sessions |
| "Script execution failed" | JavaScript error | Test script in console, add error handling |

## Prevention Tips

1. **Always close sessions** when done
2. **Use appropriate timeouts** for your workflow
3. **Implement error handling** and retries
4. **Test selectors** in browser DevTools first
5. **Monitor session usage** regularly
6. **Enable recording** for production workflows
7. **Use Live View** for debugging complex issues
8. **Keep sessions under limit** (< 20 concurrent)

## Summary

Most issues can be resolved by:
- ✅ Verifying AWS credentials and permissions
- ✅ Using correct regions
- ✅ Testing selectors in browser first
- ✅ Adding appropriate waits
- ✅ Implementing error handling
- ✅ Using Live View for visual debugging
- ✅ Checking MCP server logs

Still stuck? Check AWS AgentCore Browser documentation or contact support.
