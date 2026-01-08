# PowerPoint Presentation Tools Power

A comprehensive Kiro Power for creating, editing, and analyzing PowerPoint presentations (.pptx files).

## Quick Start

### 1. Install MCP Server

```bash
# Clone or copy MCP server to standard location
mkdir -p ~/.kiro/mcp-servers
cp -r pptx-mcp-server ~/.kiro/mcp-servers/

# Install dependencies
cd ~/.kiro/mcp-servers/pptx-mcp-server
pip install -r requirements.txt
npm install -g pptxgenjs playwright react-icons sharp

# Test installation
python test_mcp_server.py
```

### 2. Install Power

1. Open Kiro Powers panel
2. Add from local directory: `powers/pptx-power-clean`
3. Power will connect to the installed MCP server

### 3. Use in Kiro

Mention keywords like "pptx", "powerpoint", or "presentation" to activate the power.

## Features

- **Create from Scratch**: HTML-to-PPTX conversion with precise positioning
- **Template-Based**: Duplicate and customize existing templates
- **Advanced Editing**: Direct OOXML manipulation
- **Text Analysis**: Extract and analyze content
- **Visual Tools**: Generate thumbnails and convert slides

### Example Output

Here's an example of a presentation created with this power:

![Example Presentation Thumbnails](examples/example-presentation-thumbnails.jpg)

*8-slide presentation about AI Agents, generated from HTML using the html2pptx tool*

## Available Tools

- **html2pptx** - Convert HTML to PowerPoint
- **inventory** - Extract text shapes and properties
- **rearrange** - Duplicate, reorder, delete slides
- **replace** - Replace text while preserving formatting
- **thumbnail** - Generate visual thumbnail grids

## Documentation

- **POWER.md** - Main documentation with installation guide
- **steering/html2pptx-guide.md** - HTML conversion workflow
- **steering/ooxml-guide.md** - OOXML editing workflow
- **steering/template-workflow.md** - Template-based creation

## Architecture

**Two-Part Structure:**

1. **MCP Server** (separate installation)
   - Location: `~/.kiro/mcp-servers/pptx-mcp-server/`
   - Contains: Scripts, MCP server code, dependencies
   - Repository: [Link to MCP server repo]

2. **Power** (this directory)
   - Contains: Documentation only (POWER.md, mcp.json, steering/)
   - Purpose: Configuration and usage guide

## Requirements

### Python Packages
```bash
pip install mcp markitdown[pptx] defusedxml Pillow python-pptx
```

### Node.js Packages
```bash
npm install -g pptxgenjs playwright react-icons sharp
```

### System Tools
```bash
# macOS
brew install libreoffice poppler

# Ubuntu/Debian
sudo apt-get install libreoffice poppler-utils
```

## Troubleshooting

### MCP Server Not Found

```bash
# Verify installation
ls -la ~/.kiro/mcp-servers/pptx-mcp-server/

# Test server
cd ~/.kiro/mcp-servers/pptx-mcp-server
python script_executor_mcp.py
```

### Missing Dependencies

```bash
cd ~/.kiro/mcp-servers/pptx-mcp-server
pip install -r requirements.txt
```

### Permission Issues

```bash
cd ~/.kiro/mcp-servers/pptx-mcp-server
chmod +x scripts/*.py scripts/*.js
chmod +x ooxml/scripts/*.py
```

## Updates

To update the MCP server:

```bash
cd ~/.kiro/mcp-servers/pptx-mcp-server
git pull  # If using git
pip install -r requirements.txt
python test_mcp_server.py
```

No need to reinstall the Power after MCP server updates.

## Conversion Notes

This power was converted from a Claude Agent Skill using the "Convert Skills to Power" tool:
- Original: Claude Agent Skill with 5 scripts
- Conversion approach: Script Executor Pattern with separate MCP server installation
- All scripts preserved as-is for reliability
- Documentation reorganized for Kiro Powers

## Support

For issues or questions:
1. Check POWER.md for detailed troubleshooting
2. Review steering files for workflow guidance
3. Test MCP server with `test_mcp_server.py`
4. Check MCP logs in Kiro

## License

[Your License Here]
