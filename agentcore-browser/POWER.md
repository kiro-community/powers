---
name: "agentcore-browser"
displayName: "AgentCore Browser"
description: "Automate web interactions with AWS Bedrock AgentCore Browser - a secure, cloud-based browser for AI agents. Navigate websites, fill forms, extract content, and automate workflows with session management, live viewing, and recording capabilities."
keywords: ["browser", "automation", "web", "agentcore", "playwright", "scraping", "testing", "aws", "bedrock"]
author: "Kiro Team"
---

# AgentCore Browser

## Overview

Automate web interactions using Amazon Bedrock AgentCore Browser - a fully managed, cloud-based browser designed for AI agents. This power provides comprehensive browser automation capabilities including:

- **Session Management** - Create persistent browser sessions that maintain state across multiple operations
- **Web Automation** - Navigate, click, type, extract content, execute JavaScript
- **Live Viewing** - Real-time browser monitoring through AWS Console or WebSocket
- **Session Recording** - Capture and replay browser interactions for debugging
- **Security** - Isolated sessions, ephemeral environments, CloudTrail logging
- **Scalability** - Serverless infrastructure, up to 500 concurrent sessions

Unlike local browser automation, AgentCore Browser runs in AWS cloud with enterprise-grade security, automatic scaling, and built-in observability.

## When to Use This Power

Use AgentCore Browser when you need to:

- **Automate web workflows** - Fill forms, submit data, navigate multi-step processes
- **Extract web content** - Scrape data, monitor websites, gather information
- **Test web applications** - Automated QA, visual regression testing
- **Integrate legacy systems** - Interact with web UIs that lack APIs
- **Research and intelligence** - Automated web research, competitive analysis
- **E-commerce automation** - Order processing, inventory monitoring

**Key Advantages:**
- No local browser installation required
- Runs in secure, isolated cloud environment
- Automatic scaling for parallel sessions
- Built-in recording and replay for debugging
- Live view for human intervention when needed

## Available MCP Tools

This power provides a Python MCP server with the following tools:

### Session Management

**`create_browser_session`** - Create a new browser session
- Maintains state across multiple operations
- Configurable timeout (up to 8 hours)
- Optional recording to S3
- Returns session ID and Live View URL

**`list_sessions`** - List all active browser sessions
- Shows session IDs, descriptions, status
- Useful for managing multiple parallel sessions

**`get_session_info`** - Get detailed information about a session
- Current URL, tabs, status
- Live View URL for monitoring

**`close_session`** - Close a browser session and clean up resources
- Releases cloud resources
- Stops recording if enabled

### Browser Automation

**`navigate`** - Navigate to a URL
- Waits for page load
- Handles network errors gracefully

**`interact`** - Unified interaction interface
- Actions: click, type, press_key, scroll
- CSS selector-based element targeting
- Automatic wait for elements

**`extract_content`** - Extract content from page
- Get text, HTML, or attributes
- CSS selector support
- Full page or specific elements

**`execute_script`** - Execute JavaScript in browser context
- Run custom scripts
- Access DOM directly
- Return results to agent

**`screenshot`** - Capture page screenshot
- Full page or specific element
- Saved locally or returned as base64
- Useful for visual verification

### Tab Management

**`manage_tabs`** - Manage browser tabs
- Actions: new_tab, switch_tab, close_tab, list_tabs
- Multi-tab workflows
- Parallel page operations

### Advanced Features

**`get_live_view_url`** - Get Live View URL for a session
- Real-time browser monitoring
- Human intervention capability
- WebSocket-based streaming

**`search_browser_docs`** - Search AgentCore Browser documentation
- Find specific features
- Troubleshooting guidance
- API references

## Quick Start

### 1. Create a Browser Session

```python
# Create a new session
result = await create_browser_session(
    session_id="my-automation-session",
    description="Automating form submission",
    region="us-east-1",
    session_timeout=3600,  # 1 hour
    enable_recording=False
)

# Result includes:
# - session_id: "my-automation-session"
# - live_view_url: "https://console.aws.amazon.com/..."
# - status: "ready"
```

### 2. Navigate and Interact

```python
# Navigate to a website
await navigate(
    session_id="my-automation-session",
    url="https://example.com/form"
)

# Fill out a form
await interact(
    session_id="my-automation-session",
    action="type",
    selector="input[name='email']",
    text="user@example.com"
)

await interact(
    session_id="my-automation-session",
    action="click",
    selector="button[type='submit']"
)
```

### 3. Extract Content

```python
# Extract text from page
result = await extract_content(
    session_id="my-automation-session",
    content_type="text",
    selector="div.result"
)

print(result["content"])
```

### 4. Clean Up

```python
# Close session when done
await close_session(session_id="my-automation-session")
```

## Session Management Best Practices

### Session Lifecycle

1. **Create** - Initialize session with unique ID
2. **Use** - Perform multiple operations with same session_id
3. **Monitor** - Use Live View URL if needed
4. **Close** - Always close when done to free resources

### Session Naming

Use descriptive session IDs:
- ✅ Good: `order-processing-2024-01`, `qa-test-login-flow`
- ❌ Bad: `session1`, `test`, `abc123`

### Timeout Configuration

Choose appropriate timeout based on workflow:
- **Short tasks** (< 15 min): Use default 900 seconds
- **Medium workflows** (15-60 min): Use 3600 seconds (1 hour)
- **Long-running** (1-8 hours): Use up to 28800 seconds (8 hours)

### Parallel Sessions

You can run up to 500 concurrent sessions:

```python
# Create multiple sessions for parallel processing
for i in range(10):
    await create_browser_session(
        session_id=f"parallel-session-{i}",
        description=f"Processing batch {i}"
    )

# Process in parallel
# Each session maintains independent state
```

## Available Steering Files

This power includes detailed guides for specific workflows:

- **getting-started.md** - Complete setup and first automation
- **web-automation-patterns.md** - Common automation patterns and best practices
- **session-management.md** - Advanced session management techniques
- **live-view-recording.md** - Using Live View and session recording
- **integration-strands.md** - Integrating with Strands agents
- **troubleshooting.md** - Common issues and solutions

Access steering files with:
```
readSteering("agentcore-browser", "getting-started.md")
```

## Tool Usage Examples

### Example 1: Form Automation

```python
# Create session
await create_browser_session(
    session_id="form-automation",
    description="Automated form submission"
)

# Navigate to form
await navigate(
    session_id="form-automation",
    url="https://example.com/contact"
)

# Fill form fields
await interact(
    session_id="form-automation",
    action="type",
    selector="input[name='name']",
    text="John Doe"
)

await interact(
    session_id="form-automation",
    action="type",
    selector="input[name='email']",
    text="john@example.com"
)

await interact(
    session_id="form-automation",
    action="type",
    selector="textarea[name='message']",
    text="This is an automated message"
)

# Submit form
await interact(
    session_id="form-automation",
    action="click",
    selector="button[type='submit']"
)

# Verify submission
result = await extract_content(
    session_id="form-automation",
    content_type="text",
    selector="div.success-message"
)

# Clean up
await close_session(session_id="form-automation")
```

### Example 2: Web Scraping

```python
# Create session with recording
await create_browser_session(
    session_id="web-scraper",
    description="Scraping product data",
    enable_recording=True
)

# Navigate to target page
await navigate(
    session_id="web-scraper",
    url="https://example.com/products"
)

# Extract product information
products = await execute_script(
    session_id="web-scraper",
    script="""
    return Array.from(document.querySelectorAll('.product')).map(p => ({
        name: p.querySelector('.name').textContent,
        price: p.querySelector('.price').textContent,
        url: p.querySelector('a').href
    }));
    """
)

# Close session (recording saved to S3)
await close_session(session_id="web-scraper")
```

### Example 3: Multi-Tab Workflow

```python
# Create session
await create_browser_session(
    session_id="multi-tab-workflow",
    description="Comparing data across sites"
)

# Open first site in main tab
await navigate(
    session_id="multi-tab-workflow",
    url="https://site1.com"
)

# Open second site in new tab
await manage_tabs(
    session_id="multi-tab-workflow",
    action="new_tab",
    tab_id="site2"
)

await navigate(
    session_id="multi-tab-workflow",
    url="https://site2.com"
)

# Extract from second tab
data2 = await extract_content(
    session_id="multi-tab-workflow",
    content_type="text",
    selector="div.data"
)

# Switch back to first tab
await manage_tabs(
    session_id="multi-tab-workflow",
    action="switch_tab",
    tab_id="main"
)

# Extract from first tab
data1 = await extract_content(
    session_id="multi-tab-workflow",
    content_type="text",
    selector="div.data"
)

# Compare data...

await close_session(session_id="multi-tab-workflow")
```

## Configuration

### Installation Steps

1. **Install MCP Server** (if not already installed):
   ```bash
   cd agentcore-browser-mcp-server
   chmod +x install.sh
   ./install.sh
   ```
   This installs the MCP server to `~/.kiro/mcp-servers/agentcore-browser-mcp-server/`

2. **Install Power in Kiro**:
   - Open Kiro Powers panel
   - Click "Install from directory"
   - Select the `powers/agentcore-browser` directory
   - Kiro will automatically configure the MCP server connection

3. **Verify Installation**:
   - Restart Kiro
   - The power should appear in your installed powers list
   - MCP server will connect automatically

**Note**: The `mcp.json` file contains a placeholder path that Kiro will automatically update to your home directory during installation. If you encounter path issues, you can manually edit the MCP configuration in Kiro's settings.

### Prerequisites

1. **AWS Account** with Bedrock AgentCore access
2. **AWS Credentials** configured (via `aws configure` or environment variables)
3. **IAM Permissions** for AgentCore Browser:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": [
           "bedrock-agentcore:CreateBrowser",
           "bedrock-agentcore:StartBrowserSession",
           "bedrock-agentcore:StopBrowserSession",
           "bedrock-agentcore:GetBrowserSession"
         ],
         "Resource": "*"
       }
     ]
   }
   ```

4. **Python 3.10+** for MCP server
5. **Region Availability** - AgentCore Browser is available in:
   - us-east-1 (N. Virginia)
   - us-west-2 (Oregon)
   - eu-central-1 (Frankfurt)
   - ap-southeast-2 (Sydney)

### Optional: Session Recording

To enable session recording, add S3 permissions:

```json
{
  "Effect": "Allow",
  "Action": [
    "s3:PutObject",
    "s3:GetObject"
  ],
  "Resource": "arn:aws:s3:::your-recording-bucket/*"
}
```

## Troubleshooting

### Session Creation Fails

**Error:** `AccessDeniedException`
**Solution:** Verify IAM permissions and AWS credentials

**Error:** `Region not supported`
**Solution:** Use supported region (us-east-1, us-west-2, eu-central-1, ap-southeast-2)

### Navigation Timeout

**Error:** `Navigation timeout exceeded`
**Solution:** 
- Check URL is accessible
- Increase timeout in navigate call
- Verify network connectivity

### Element Not Found

**Error:** `Selector not found`
**Solution:**
- Verify CSS selector is correct
- Wait for page to fully load
- Use browser DevTools to test selector

### Session Limit Reached

**Error:** `Maximum sessions exceeded`
**Solution:**
- Close unused sessions
- Implement session pooling
- Contact AWS for limit increase

## Best Practices

### Security

- **Never hardcode credentials** - Use environment variables or AWS Secrets Manager
- **Close sessions promptly** - Free resources and reduce costs
- **Use session recording** - For audit trails and debugging
- **Limit session timeout** - Use shortest timeout needed for workflow

### Performance

- **Reuse sessions** - For multiple operations on same site
- **Parallel sessions** - For batch processing
- **Minimize screenshots** - Only when necessary for verification
- **Use CSS selectors** - More reliable than XPath

### Reliability

- **Handle errors gracefully** - Network issues, timeouts, element changes
- **Implement retries** - For transient failures
- **Use Live View** - For debugging complex workflows
- **Enable recording** - For production workflows

### Cost Optimization

- **Close idle sessions** - Don't leave sessions running
- **Use appropriate timeouts** - Shorter is cheaper
- **Batch operations** - Minimize session creation overhead
- **Monitor usage** - Track session count and duration

## Integration with Other Powers

### With Strands Agents

```python
from strands import Agent
from strands_tools.browser import AgentCoreBrowser

# Create browser tool
browser = AgentCoreBrowser(region="us-east-1")

# Add to agent
agent = Agent(
    name="Web Automation Agent",
    tools=[browser.browser]
)

# Agent can now use browser automatically
```

### With AWS AgentCore

AgentCore Browser integrates seamlessly with other AgentCore services:
- **AgentCore Memory** - Store extracted data
- **AgentCore Gateway** - Expose browser automation as API
- **AgentCore Runtime** - Deploy browser agents

## Additional Resources

- [AgentCore Browser Documentation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/browser-tool.html)
- [Strands Browser Integration](https://github.com/strands-agents/tools/tree/main/src/strands_tools/browser)
- [AWS Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Playwright Documentation](https://playwright.dev/)

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Read steering files for detailed guides
3. Search AgentCore Browser documentation
4. Contact AWS Support for service issues
