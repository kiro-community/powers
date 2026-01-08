# Installation and Testing Guide

Complete guide for installing and testing the AgentCore Browser Power.

## Prerequisites

Before installing, ensure you have:

### 1. AWS Account and Credentials

```bash
# Install AWS CLI
brew install awscli  # macOS
# or
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Configure credentials
aws configure
# Enter: Access Key ID, Secret Access Key, Region (us-east-1), Format (json)

# Verify
aws sts get-caller-identity
```

### 2. IAM Permissions

Attach this policy to your IAM user/role:

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

### 3. Python and uv

```bash
# Check Python version (need 3.10+)
python3 --version

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Restart terminal or source profile
source ~/.bashrc  # or ~/.zshrc

# Verify
uv --version
```

## Installation Steps

### Step 1: Copy Power to Kiro Directory

```bash
# Create powers directory if it doesn't exist
mkdir -p ~/.kiro/powers

# Copy the power
cp -r powers/agentcore-browser ~/.kiro/powers/

# Verify
ls -la ~/.kiro/powers/agentcore-browser
```

### Step 2: Install Python Dependencies

```bash
# Navigate to power directory
cd ~/.kiro/powers/agentcore-browser

# Install dependencies with uv
uv sync

# This creates a virtual environment and installs:
# - mcp
# - playwright
# - bedrock-agentcore
# - boto3
```

### Step 3: Install Playwright Browsers

```bash
# Still in power directory
uv run playwright install chromium

# This downloads Chromium browser binaries
# Takes a few minutes on first run
```

### Step 4: Verify Installation

```bash
# Check virtual environment
ls -la .venv

# Check installed packages
uv pip list

# Should see:
# - mcp
# - playwright
# - bedrock-agentcore
# - boto3
```

### Step 5: Install Power in Kiro

**Option A: Via Kiro UI (Recommended)**

1. Open Kiro
2. Open Command Palette (Cmd/Ctrl + Shift + P)
3. Type "Powers" and select "Open Powers Panel"
4. Click "Install from directory"
5. Navigate to `~/.kiro/powers/agentcore-browser`
6. Click "Install"

**Option B: Manual Configuration**

1. Open Kiro settings
2. Navigate to MCP section
3. Add server configuration:
   ```json
   {
     "mcpServers": {
       "agentcore-browser": {
         "command": "uv",
         "args": [
           "--directory",
           "~/.kiro/powers/agentcore-browser",
           "run",
           "agentcore_browser_mcp.py"
         ],
         "env": {
           "AWS_REGION": "us-east-1"
         }
       }
     }
   }
   ```

### Step 6: Restart Kiro

```bash
# Restart Kiro to load the new power
# Or use Command Palette: "Reload Window"
```

### Step 7: Verify Power is Loaded

1. Open Kiro
2. Check MCP servers status
3. Look for "agentcore-browser" in connected servers
4. Should show "Connected" status

## Testing the Installation

### Test 1: Basic Connection

Ask Kiro:
```
"List all available browser automation tools"
```

Expected response should include:
- create_browser_session
- navigate
- interact
- extract_content
- etc.

### Test 2: Create Session

Ask Kiro:
```
"Create a browser session called 'test-session' for testing"
```

Expected response:
```
✅ Browser session created successfully!
Session ID: test-session
Region: us-east-1
...
```

### Test 3: Navigate

Ask Kiro:
```
"Navigate to example.com in test-session"
```

Expected response:
```
✅ Navigated to https://example.com
Current URL: https://example.com/
```

### Test 4: Extract Content

Ask Kiro:
```
"Extract the main heading from test-session"
```

Expected response:
```
Extracted text:
Example Domain
```

### Test 5: Close Session

Ask Kiro:
```
"Close test-session"
```

Expected response:
```
✅ Session 'test-session' closed successfully
```

### Test 6: Complete Workflow

Ask Kiro to run this complete workflow:

```
"Create a browser session called 'workflow-test', navigate to example.com, 
extract the page title, take a screenshot, and close the session"
```

This tests:
- Session creation
- Navigation
- Content extraction
- Screenshot
- Session cleanup

## Troubleshooting Installation

### Issue: "uv command not found"

**Solution:**
```bash
# Reinstall uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add to PATH
export PATH="$HOME/.cargo/bin:$PATH"

# Add to shell profile
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Issue: "Python version too old"

**Solution:**
```bash
# Install Python 3.10+ using pyenv
curl https://pyenv.run | bash

# Add to shell profile
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"

# Install Python 3.11
pyenv install 3.11
pyenv global 3.11

# Verify
python --version
```

### Issue: "Playwright install fails"

**Solution:**
```bash
# Install system dependencies (Linux)
sudo apt-get install -y \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2

# Then retry
cd ~/.kiro/powers/agentcore-browser
uv run playwright install chromium
```

### Issue: "MCP server won't start"

**Solution:**
```bash
# Check logs in Kiro
# Look for error messages

# Common fixes:
# 1. Reinstall dependencies
cd ~/.kiro/powers/agentcore-browser
rm -rf .venv
uv sync

# 2. Check Python path
which python3

# 3. Test MCP server manually
cd ~/.kiro/powers/agentcore-browser
uv run python agentcore_browser_mcp.py
# Should start without errors
```

### Issue: "AWS credentials not found"

**Solution:**
```bash
# Configure AWS credentials
aws configure

# Or set environment variables
export AWS_ACCESS_KEY_ID="your-key"
export AWS_SECRET_ACCESS_KEY="your-secret"
export AWS_REGION="us-east-1"

# Verify
aws sts get-caller-identity
```

### Issue: "AccessDeniedException"

**Solution:**
1. Check IAM permissions (see Prerequisites)
2. Verify you're using correct AWS account
3. Try different region:
   ```bash
   export AWS_REGION="us-west-2"
   ```

## Updating the Power

### Update from Git

```bash
# Pull latest changes
cd /path/to/repo
git pull

# Copy updated files
cp -r powers/agentcore-browser ~/.kiro/powers/

# Reinstall dependencies
cd ~/.kiro/powers/agentcore-browser
uv sync

# Restart Kiro
```

### Update Dependencies

```bash
cd ~/.kiro/powers/agentcore-browser

# Update all dependencies
uv sync --upgrade

# Or update specific package
uv pip install --upgrade bedrock-agentcore
```

## Uninstalling

### Remove Power

```bash
# Remove power directory
rm -rf ~/.kiro/powers/agentcore-browser

# Remove from Kiro MCP config
# Edit ~/.kiro/settings/mcp.json
# Remove "agentcore-browser" entry

# Restart Kiro
```

## Environment Variables

Optional environment variables for customization:

```bash
# AWS Configuration
export AWS_REGION="us-east-1"
export AWS_PROFILE="default"

# Browser Configuration
export BROWSER_SESSION_TIMEOUT="3600"
export BROWSER_IDENTIFIER="aws.browser.v1"
export BROWSER_SCREENSHOTS_DIR="screenshots"

# MCP Configuration
export FASTMCP_LOG_LEVEL="INFO"
```

Add to `~/.bashrc` or `~/.zshrc` to persist.

## Verification Checklist

After installation, verify:

- [ ] AWS CLI installed and configured
- [ ] IAM permissions attached
- [ ] Python 3.10+ installed
- [ ] uv package manager installed
- [ ] Power copied to ~/.kiro/powers/
- [ ] Python dependencies installed (uv sync)
- [ ] Playwright browsers installed
- [ ] Power loaded in Kiro
- [ ] MCP server connected
- [ ] Test session creation works
- [ ] Test navigation works
- [ ] Test content extraction works

## Getting Help

If you encounter issues:

1. **Check logs**
   - Kiro MCP server logs
   - Terminal output from manual test

2. **Review documentation**
   - README.md - Quick reference
   - POWER.md - Complete guide
   - troubleshooting.md - Common issues

3. **Test components**
   ```bash
   # Test AWS credentials
   aws sts get-caller-identity
   
   # Test Python
   python3 --version
   
   # Test uv
   uv --version
   
   # Test Playwright
   cd ~/.kiro/powers/agentcore-browser
   uv run python -c "from playwright.async_api import async_playwright; print('OK')"
   ```

4. **Contact support**
   - AWS Support for AgentCore issues
   - Kiro support for MCP issues
   - GitHub issues for power bugs

## Next Steps

After successful installation:

1. **Read getting started guide**
   ```
   Ask Kiro: "Show me the getting started guide for AgentCore Browser"
   ```

2. **Try examples**
   - See `example_usage.md` for real-world examples
   - Start with simple navigation
   - Progress to complex workflows

3. **Learn advanced features**
   - Session management
   - Multi-tab workflows
   - Live View monitoring
   - Session recording

4. **Build your automation**
   - Identify your use case
   - Design workflow
   - Implement with AgentCore Browser
   - Test and refine

## Summary

Installation steps:
1. ✅ Install prerequisites (AWS CLI, Python, uv)
2. ✅ Copy power to ~/.kiro/powers/
3. ✅ Install dependencies (uv sync)
4. ✅ Install Playwright browsers
5. ✅ Load power in Kiro
6. ✅ Test basic functionality
7. ✅ Start automating!

You're ready to automate! 🚀
