# Getting Started with AgentCore Browser

Complete guide to setting up and using AgentCore Browser for web automation.

## Prerequisites

### 1. AWS Account Setup

You need an AWS account with access to Amazon Bedrock AgentCore:

1. **Sign up for AWS** (if you don't have an account)
   - Visit https://aws.amazon.com/
   - Click "Create an AWS Account"
   - Follow the registration process

2. **Enable Bedrock AgentCore**
   - Navigate to AWS Bedrock console
   - Enable AgentCore services in your region
   - Available regions: us-east-1, us-west-2, eu-central-1, ap-southeast-2

### 2. Configure AWS Credentials

Set up your AWS credentials locally:

```bash
# Install AWS CLI if not already installed
# macOS
brew install awscli

# Linux
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Configure credentials
aws configure
```

You'll be prompted for:
- AWS Access Key ID
- AWS Secret Access Key
- Default region (e.g., us-east-1)
- Default output format (json)

**Verify credentials:**
```bash
aws sts get-caller-identity
```

### 3. IAM Permissions

Ensure your IAM user/role has these permissions:

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
        "bedrock-agentcore:GetBrowserSession",
        "bedrock-agentcore:ListBrowserSessions"
      ],
      "Resource": "*"
    }
  ]
}
```

**Optional: For session recording, add S3 permissions:**
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

### 4. Install Python and uv

AgentCore Browser MCP server requires Python 3.10+:

```bash
# Check Python version
python3 --version

# Install uv package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Verify installation
uv --version
```

### 5. Install Playwright

After installing the power, install Playwright browsers:

```bash
cd ~/.kiro/powers/agentcore-browser
uv run playwright install chromium
```

## Installation

### Method 1: Via Kiro UI (Recommended)

1. Open Kiro
2. Open Powers panel (Cmd/Ctrl + Shift + P → "Powers")
3. Click "Install from directory"
4. Navigate to `powers/agentcore-browser`
5. Click "Install"

### Method 2: Manual Installation

```bash
# Copy power to Kiro directory
mkdir -p ~/.kiro/powers
cp -r powers/agentcore-browser ~/.kiro/powers/

# Install dependencies
cd ~/.kiro/powers/agentcore-browser
uv sync

# Install Playwright browsers
uv run playwright install chromium
```

### Verify Installation

1. Restart Kiro
2. Check MCP servers are connected:
   - Open Kiro settings
   - Navigate to MCP section
   - Verify "agentcore-browser" is listed and connected

## Your First Automation

Let's create a simple automation to navigate to a website and extract content.

### Step 1: Create a Browser Session

```python
# In Kiro, ask the agent:
"Create a browser session called 'test-session' for testing navigation"

# This will call:
await create_browser_session(
    session_id="test-session",
    description="Testing navigation and content extraction",
    region="us-east-1",
    session_timeout=3600
)
```

**What happens:**
- AgentCore creates a cloud browser instance
- Session is ready for automation
- You receive a Live View URL for monitoring

### Step 2: Navigate to a Website

```python
# Ask the agent:
"Navigate to example.com in test-session"

# This will call:
await navigate(
    session_id="test-session",
    url="https://example.com"
)
```

**What happens:**
- Browser loads the URL
- Waits for page to be fully loaded
- Returns success confirmation

### Step 3: Extract Content

```python
# Ask the agent:
"Extract the main heading text from test-session"

# This will call:
await extract_content(
    session_id="test-session",
    content_type="text",
    selector="h1"
)
```

**What happens:**
- Finds the h1 element
- Extracts text content
- Returns the text to you

### Step 4: Take a Screenshot

```python
# Ask the agent:
"Take a screenshot of the page in test-session"

# This will call:
await screenshot(
    session_id="test-session"
)
```

**What happens:**
- Captures full page screenshot
- Saves to local screenshots directory
- Returns file path

### Step 5: Close the Session

```python
# Ask the agent:
"Close test-session"

# This will call:
await close_session(
    session_id="test-session"
)
```

**What happens:**
- Browser session is terminated
- Resources are freed
- Session is removed from active sessions

## Complete Example: Form Automation

Here's a complete workflow for automating a contact form:

```python
# 1. Create session
await create_browser_session(
    session_id="contact-form",
    description="Automating contact form submission"
)

# 2. Navigate to form
await navigate(
    session_id="contact-form",
    url="https://example.com/contact"
)

# 3. Fill name field
await interact(
    session_id="contact-form",
    action="type",
    selector="input[name='name']",
    text="John Doe"
)

# 4. Fill email field
await interact(
    session_id="contact-form",
    action="type",
    selector="input[name='email']",
    text="john@example.com"
)

# 5. Fill message
await interact(
    session_id="contact-form",
    action="type",
    selector="textarea[name='message']",
    text="This is an automated test message"
)

# 6. Submit form
await interact(
    session_id="contact-form",
    action="click",
    selector="button[type='submit']"
)

# 7. Wait a moment for submission
await execute_script(
    session_id="contact-form",
    script="await new Promise(r => setTimeout(r, 2000))"
)

# 8. Verify success
await extract_content(
    session_id="contact-form",
    content_type="text",
    selector=".success-message"
)

# 9. Take screenshot for verification
await screenshot(
    session_id="contact-form",
    path="form-submitted.png"
)

# 10. Close session
await close_session(
    session_id="contact-form"
)
```

## Understanding Sessions

### Session Lifecycle

1. **Create** - Initialize with unique ID
2. **Active** - Perform operations
3. **Idle** - No operations for some time
4. **Expired** - Timeout reached (auto-closed)
5. **Closed** - Manually closed

### Session State

Sessions maintain state across operations:
- **Cookies** - Preserved between requests
- **Local Storage** - Maintained
- **Navigation History** - Available for back/forward
- **Tabs** - Multiple tabs in one session

### Session Timeout

Choose appropriate timeout:
- **Short tasks** (< 15 min): 900 seconds (default)
- **Medium workflows** (15-60 min): 3600 seconds
- **Long-running** (1-8 hours): Up to 28800 seconds

**Example:**
```python
await create_browser_session(
    session_id="long-running",
    description="Multi-hour data collection",
    session_timeout=28800  # 8 hours
)
```

## Live View

Monitor your browser sessions in real-time:

### Getting Live View URL

```python
await get_live_view_url(
    session_id="your-session"
)
```

### Using Live View

1. Open the URL in your browser
2. You'll see real-time video stream
3. Can interact manually if needed
4. Useful for debugging

### When to Use Live View

- **Debugging** - See what's happening visually
- **Human intervention** - Take over when needed
- **Verification** - Confirm automation is working
- **Training** - Learn how automation works

## Session Recording

Enable recording for audit trails and debugging:

### Enable Recording

```python
await create_browser_session(
    session_id="recorded-session",
    description="Session with recording",
    enable_recording=True
)
```

### What Gets Recorded

- All browser interactions
- Network requests
- Console logs
- DOM changes
- Screenshots at key points

### Accessing Recordings

Recordings are stored in S3 (if configured):
- Check AWS Console → S3
- Look for your recording bucket
- Download and replay recordings

## Best Practices

### 1. Session Naming

Use descriptive, unique session IDs:
```python
# Good
"order-processing-2024-01-05"
"qa-test-login-flow"
"scrape-product-data-batch-1"

# Bad
"session1"
"test"
"abc"
```

### 2. Always Close Sessions

```python
try:
    # Your automation
    await navigate(...)
    await interact(...)
finally:
    # Always close, even if error occurs
    await close_session(session_id="your-session")
```

### 3. Handle Errors Gracefully

```python
# Check if element exists before interacting
result = await extract_content(
    session_id="session",
    content_type="html",
    selector="button.submit"
)

if "Error" not in result:
    await interact(
        session_id="session",
        action="click",
        selector="button.submit"
    )
```

### 4. Use Appropriate Timeouts

```python
# Short task
await create_browser_session(
    session_id="quick-check",
    session_timeout=900  # 15 minutes
)

# Long workflow
await create_browser_session(
    session_id="data-collection",
    session_timeout=7200  # 2 hours
)
```

### 5. Monitor Session Usage

```python
# List all active sessions
await list_sessions()

# Get specific session info
await get_session_info(session_id="your-session")
```

## Next Steps

Now that you're set up, explore:

1. **Web Automation Patterns** - Common automation patterns
   - Read: `web-automation-patterns.md`

2. **Session Management** - Advanced session techniques
   - Read: `session-management.md`

3. **Live View & Recording** - Monitoring and debugging
   - Read: `live-view-recording.md`

4. **Integration with Strands** - Use with Strands agents
   - Read: `integration-strands.md`

## Troubleshooting

### Common Issues

**"AWS credentials not configured"**
```bash
aws configure
# Enter your credentials
```

**"Region not supported"**
- Use: us-east-1, us-west-2, eu-central-1, or ap-southeast-2

**"Playwright not installed"**
```bash
cd ~/.kiro/powers/agentcore-browser
uv run playwright install chromium
```

**"Session creation fails"**
- Check IAM permissions
- Verify AWS credentials
- Ensure region is correct

**"MCP server not connected"**
- Restart Kiro
- Check MCP settings
- Verify uv is installed

## Getting Help

- Check `troubleshooting.md` for detailed solutions
- Review AWS AgentCore documentation
- Contact AWS Support for service issues
- Check Kiro documentation for MCP issues

## Summary

You've learned:
- ✅ How to set up AWS credentials and permissions
- ✅ How to install the AgentCore Browser power
- ✅ How to create and manage browser sessions
- ✅ How to perform basic automation tasks
- ✅ How to use Live View for monitoring
- ✅ Best practices for session management

Ready to automate! 🚀
