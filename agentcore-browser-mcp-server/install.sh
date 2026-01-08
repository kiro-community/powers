#!/bin/bash
# AgentCore Browser MCP Server Installation Script

set -e  # Exit on error

echo "=========================================="
echo "AgentCore Browser MCP Server Installation"
echo "=========================================="
echo ""

# Check if running on macOS or Linux
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
else
    echo "❌ Unsupported operating system: $OSTYPE"
    exit 1
fi

echo "✓ Detected OS: $OS"
echo ""

# Step 1: Check AWS CLI
echo "Step 1: Checking AWS CLI..."
if command -v aws &> /dev/null; then
    echo "✓ AWS CLI found: $(aws --version)"
    
    # Check if credentials are configured
    if aws sts get-caller-identity &> /dev/null; then
        echo "✓ AWS credentials configured"
    else
        echo "⚠️  Warning: AWS credentials not configured"
        echo "   Please run: aws configure"
    fi
else
    echo "❌ Error: AWS CLI not found"
    echo "   Please install AWS CLI first:"
    echo "   macOS: brew install awscli"
    echo "   Linux: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html"
    exit 1
fi
echo ""

# Step 2: Check Python version
echo "Step 2: Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)
    
    if [ "$PYTHON_MAJOR" -ge 3 ] && [ "$PYTHON_MINOR" -ge 10 ]; then
        echo "✓ Python $PYTHON_VERSION found"
    else
        echo "❌ Error: Python 3.10+ required, found $PYTHON_VERSION"
        exit 1
    fi
else
    echo "❌ Error: Python 3 not found"
    exit 1
fi
echo ""

# Step 3: Create directory
echo "Step 3: Creating MCP server directory..."
mkdir -p ~/.kiro/mcp-servers
echo "✓ Directory created: ~/.kiro/mcp-servers"
echo ""

# Step 4: Copy files
echo "Step 4: Copying MCP server files..."
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cp -r "$SCRIPT_DIR" ~/.kiro/mcp-servers/agentcore-browser-mcp-server
echo "✓ Files copied to ~/.kiro/mcp-servers/agentcore-browser-mcp-server"
echo ""

# Step 5: Install Python dependencies
echo "Step 5: Installing Python dependencies..."
cd ~/.kiro/mcp-servers/agentcore-browser-mcp-server

# Try different installation methods
if command -v conda &> /dev/null; then
    echo "  Detected conda environment"
    # Use conda's pip
    pip install -r requirements.txt
    echo "✓ Python dependencies installed via conda pip"
elif command -v pip3 &> /dev/null; then
    # Try with --break-system-packages for externally managed environments
    if pip3 install -r requirements.txt 2>&1 | grep -q "externally-managed-environment"; then
        echo "  Detected externally managed environment, using --break-system-packages"
        pip3 install --break-system-packages -r requirements.txt
    else
        pip3 install -r requirements.txt
    fi
    echo "✓ Python dependencies installed"
elif command -v pip &> /dev/null; then
    if pip install -r requirements.txt 2>&1 | grep -q "externally-managed-environment"; then
        echo "  Detected externally managed environment, using --break-system-packages"
        pip install --break-system-packages -r requirements.txt
    else
        pip install -r requirements.txt
    fi
    echo "✓ Python dependencies installed"
else
    echo "❌ Error: pip not found"
    echo "   Please install pip first"
    exit 1
fi
echo ""

# Step 6: Install Playwright browsers
echo "Step 6: Installing Playwright browsers..."

# Use the same Python that has playwright installed
if command -v conda &> /dev/null && [ -n "$CONDA_DEFAULT_ENV" ]; then
    # In conda environment, use conda's python
    python -m playwright install chromium
elif command -v python3 &> /dev/null; then
    python3 -m playwright install chromium
else
    python -m playwright install chromium
fi

echo "✓ Playwright Chromium installed"
echo ""

# Step 7: Test installation
echo "Step 7: Testing MCP server..."

# Use the same Python that has the dependencies
if command -v conda &> /dev/null && [ -n "$CONDA_DEFAULT_ENV" ]; then
    python test_mcp_server.py
elif command -v python3 &> /dev/null; then
    python3 test_mcp_server.py
else
    python test_mcp_server.py
fi

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ Installation Complete!"
    echo "=========================================="
    echo ""
    echo "MCP Server installed at:"
    echo "  ~/.kiro/mcp-servers/agentcore-browser-mcp-server/"
    echo ""
    echo "Next steps:"
    echo "  1. Ensure AWS credentials are configured: aws configure"
    echo "  2. Verify IAM permissions for AgentCore Browser"
    echo "  3. Open Kiro Powers panel"
    echo "  4. Add Power from: powers/agentcore-browser"
    echo "  5. Start automating with AgentCore Browser!"
    echo ""
    echo "Test the installation:"
    echo "  Ask Kiro: 'Create a browser session called test-session'"
    echo ""
else
    echo ""
    echo "=========================================="
    echo "⚠️  Installation completed with warnings"
    echo "=========================================="
    echo ""
    echo "Some tests failed. Please check the output above."
    echo "Common issues:"
    echo "  - AWS credentials not configured"
    echo "  - Missing IAM permissions"
    echo "  - Python dependencies not installed"
    echo ""
fi
