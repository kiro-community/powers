#!/bin/bash
# PPTX MCP Server Installation Script

set -e  # Exit on error

echo "=========================================="
echo "PPTX MCP Server Installation"
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

# Step 1: Create directory
echo "Step 1: Creating MCP server directory..."
mkdir -p ~/.kiro/mcp-servers
echo "✓ Directory created: ~/.kiro/mcp-servers"
echo ""

# Step 2: Copy files
echo "Step 2: Copying MCP server files..."
if [ -d "pptx-mcp-server" ]; then
    cp -r pptx-mcp-server ~/.kiro/mcp-servers/
    echo "✓ Files copied to ~/.kiro/mcp-servers/pptx-mcp-server"
else
    echo "❌ Error: pptx-mcp-server directory not found"
    echo "   Please run this script from the project root directory"
    exit 1
fi
echo ""

# Step 3: Install Python dependencies
echo "Step 3: Installing Python dependencies..."
cd ~/.kiro/mcp-servers/pptx-mcp-server

if command -v pip &> /dev/null; then
    pip install -r requirements.txt
    echo "✓ Python dependencies installed"
elif command -v pip3 &> /dev/null; then
    pip3 install -r requirements.txt
    echo "✓ Python dependencies installed"
else
    echo "❌ Error: pip not found"
    echo "   Please install Python and pip first"
    exit 1
fi
echo ""

# Step 4: Install Node.js dependencies
echo "Step 4: Installing Node.js dependencies..."
if command -v npm &> /dev/null; then
    # Install locally using package.json
    cd ~/.kiro/mcp-servers/pptx-mcp-server
    npm install
    echo "✓ Node.js dependencies installed locally"
else
    echo "⚠️  Warning: npm not found"
    echo "   Node.js dependencies are required for html2pptx functionality"
    echo "   Please install Node.js and run:"
    echo "   cd ~/.kiro/mcp-servers/pptx-mcp-server"
    echo "   npm install"
fi
echo ""

# Step 5: Install system tools
echo "Step 5: Installing system tools..."
if [ "$OS" == "macos" ]; then
    if command -v brew &> /dev/null; then
        echo "Installing LibreOffice and Poppler..."
        brew install libreoffice poppler
        echo "✓ System tools installed"
    else
        echo "⚠️  Warning: Homebrew not found"
        echo "   Please install Homebrew and run:"
        echo "   brew install libreoffice poppler"
    fi
elif [ "$OS" == "linux" ]; then
    if command -v apt-get &> /dev/null; then
        echo "Installing LibreOffice and Poppler..."
        sudo apt-get update
        sudo apt-get install -y libreoffice poppler-utils
        echo "✓ System tools installed"
    else
        echo "⚠️  Warning: apt-get not found"
        echo "   Please install LibreOffice and Poppler manually"
    fi
fi
echo ""

# Step 6: Test installation
echo "Step 6: Testing MCP server..."
cd ~/.kiro/mcp-servers/pptx-mcp-server
python test_mcp_server.py

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ Installation Complete!"
    echo "=========================================="
    echo ""
    echo "MCP Server installed at:"
    echo "  ~/.kiro/mcp-servers/pptx-mcp-server/"
    echo ""
    echo "Next steps:"
    echo "  1. Open Kiro Powers panel"
    echo "  2. Add Power from: powers/pptx-power-clean"
    echo "  3. Start using PPTX tools in Kiro!"
    echo ""
else
    echo ""
    echo "=========================================="
    echo "⚠️  Installation completed with warnings"
    echo "=========================================="
    echo ""
    echo "Some tests failed. Please check the output above."
    echo "You may need to install missing dependencies."
    echo ""
fi
