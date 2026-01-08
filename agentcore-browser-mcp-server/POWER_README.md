# AgentCore Browser Power

Automate web interactions with AWS Bedrock AgentCore Browser - a secure, cloud-based browser for AI agents.

## Features

- **Session Management** - Persistent browser sessions across multiple operations
- **Web Automation** - Navigate, click, type, extract content, execute JavaScript
- **Live Viewing** - Real-time browser monitoring through AWS Console
- **Session Recording** - Capture and replay for debugging
- **Multi-Tab Support** - Manage multiple tabs within a session
- **Headless Cloud Browser** - No local installation required

## Installation

### Prerequisites

1. **AWS Account** with Bedrock AgentCore access
2. **AWS Credentials** configured:
   ```bash
   aws configure
   ```

3. **IAM Permissions**:
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

4. **Python 3.10+**

### Install MCP Server

```bash
# Navigate to MCP server directory
cd agentcore-browser-mcp-server

# Run installation script
chmod +x install.sh
./install.sh
```

This will:
- Install Python dependencies (mcp, playwright, bedrock-agentcore, boto3)
- Install Playwright Chromium browser
- Copy files to `~/.kiro/mcp-servers/agentcore-browser-mcp-server/`
- Run tests to verify installation

### Install Power

1. **Via Kiro UI**:
   - Open Powers panel in Kiro
   - Click "Install from directory"
   - Select `powers/agentcore-browser`

2. **Manual Installation**:
   ```bash
   # Copy to Kiro powers directory
   cp -r powers/agentcore-browser ~/.kiro/powers/
   ```

3. **Restart Kiro** to load the power

## Quick Start

### Example 1: Simple Navigation

```python
# Create session
await create_browser_session(
    session_id="my-session",
    description="Testing navigation"
)

# Navigate
await navigate(
    session_id="my-session",
    url="https://example.com"
)

# Extract content
await extract_content(
    session_id="my-session",
    content_type="text",
    selector="h1"
)

# Close
await close_session(session_id="my-session")
```

### Example 2: Form Automation

```python
# Create session
await create_browser_session(
    session_id="form-session",
    description="Form automation"
)

# Navigate to form
await navigate(
    session_id="form-session",
    url="https://example.com/form"
)

# Fill fields
await interact(
    session_id="form-session",
    action="type",
    selector="input[name='email']",
    text="user@example.com"
)

# Submit
await interact(
    session_id="form-session",
    action="click",
    selector="button[type='submit']"
)

# Close
await close_session(session_id="form-session")
```

## Configuration

### Environment Variables

- `AWS_REGION` - AWS region (default: us-east-1)
- `BROWSER_SESSION_TIMEOUT` - Default session timeout in seconds (default: 3600)
- `BROWSER_IDENTIFIER` - Browser identifier (default: aws.browser.v1)
- `BROWSER_SCREENSHOTS_DIR` - Screenshot directory (default: screenshots)

### Supported Regions

- us-east-1 (N. Virginia)
- us-west-2 (Oregon)
- eu-central-1 (Frankfurt)
- ap-southeast-2 (Sydney)

## Available Tools

- `create_browser_session` - Create persistent browser session
- `navigate` - Navigate to URL
- `interact` - Click, type, press keys, scroll
- `extract_content` - Extract text, HTML, attributes
- `execute_script` - Run JavaScript
- `screenshot` - Capture screenshots
- `manage_tabs` - Multi-tab management
- `list_sessions` - List active sessions
- `get_session_info` - Get session details
- `close_session` - Close and cleanup
- `get_live_view_url` - Get Live View URL

## Troubleshooting

### "Session not found"
- Ensure you created the session first
- Check session hasn't expired
- Use `list_sessions` to see active sessions

### "AccessDeniedException"
- Verify AWS credentials: `aws sts get-caller-identity`
- Check IAM permissions
- Ensure region is supported

### "Playwright not installed"
```bash
cd ~/.kiro/powers/agentcore-browser
uv run playwright install chromium
```

### "Connection timeout"
- Check internet connectivity
- Verify AWS region is accessible
- Try different region

## Documentation

For detailed guides, see POWER.md or use steering files:
- `getting-started.md` - Complete setup guide
- `web-automation-patterns.md` - Automation patterns
- `session-management.md` - Advanced session management
- `troubleshooting.md` - Common issues

## Support

- [AgentCore Browser Docs](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/browser-tool.html)
- [AWS Support](https://aws.amazon.com/support/)
- [GitHub Issues](https://github.com/your-repo/issues)

## License

MIT License - See LICENSE file for details
