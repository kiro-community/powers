# AgentCore Browser MCP Server

MCP server implementation for AWS Bedrock AgentCore Browser automation.

## Installation

### Via uvx (Recommended)

```bash
# Install and run directly
uvx agentcore-browser-mcp-server
```

### Via pip

```bash
# Install
pip install agentcore-browser-mcp-server

# Run
python -m agentcore_browser_mcp
```

### From Source

```bash
# Clone repository
git clone <repo-url>
cd agentcore-browser-mcp-server

# Install with uv
uv sync

# Install Playwright browsers
uv run playwright install chromium

# Run
uv run python agentcore_browser_mcp.py
```

## Prerequisites

1. **AWS Credentials** configured:
   ```bash
   aws configure
   ```

2. **IAM Permissions**:
   ```json
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
   ```

3. **Python 3.10+**

4. **Playwright browsers**:
   ```bash
   playwright install chromium
   ```

## Testing

```bash
# Run tests
uv run pytest

# Run with coverage
uv run pytest --cov=agentcore_browser_mcp

# Test manually
uv run python test_mcp_server.py
```

## Environment Variables

- `AWS_REGION` - AWS region (default: us-east-1)
- `BROWSER_SESSION_TIMEOUT` - Default timeout in seconds (default: 3600)
- `BROWSER_IDENTIFIER` - Browser identifier (default: aws.browser.v1)
- `BROWSER_SCREENSHOTS_DIR` - Screenshot directory (default: screenshots)

## Usage with Kiro

Add to your Kiro MCP configuration:

```json
{
  "mcpServers": {
    "agentcore-browser": {
      "command": "uvx",
      "args": ["agentcore-browser-mcp-server"],
      "env": {
        "AWS_REGION": "us-east-1"
      }
    }
  }
}
```

## Development

```bash
# Install dev dependencies
uv sync --all-extras

# Run linter
uv run ruff check .

# Format code
uv run ruff format .

# Type check
uv run mypy agentcore_browser_mcp.py
```

## License

MIT
