# PPTX MCP Server

MCP Server for PowerPoint presentation manipulation. Provides tools for creating, editing, and analyzing .pptx files.

## Features

- **html2pptx** - Convert HTML slides to PowerPoint presentation
- **inventory** - Extract all text shapes and properties from a presentation
- **rearrange** - Duplicate, reorder, and delete slides
- **replace** - Replace text content while preserving formatting
- **thumbnail** - Generate visual thumbnail grids of slides

## Installation

### Prerequisites

- Python 3.8+
- Node.js 16+ (for html2pptx)

### Quick Installation

Use the provided installation script:

```bash
cd powers/pptx-mcp-server
./install-pptx-mcp-server.sh
```

This script will:
1. Copy files to `~/.kiro/mcp-servers/pptx-mcp-server/`
2. Install Python dependencies
3. Install Node.js dependencies locally
4. Install system tools (LibreOffice, Poppler)
5. Run tests to verify installation

### Manual Installation

If you prefer to install manually:

```bash
# Python dependencies
pip install -r requirements.txt

# Node.js dependencies (installed locally)
npm install

# System tools
# macOS
brew install libreoffice poppler

# Ubuntu/Debian
sudo apt-get install libreoffice poppler-utils
```

### Install to Standard Location

```bash
# Clone or copy to standard location
mkdir -p ~/.kiro/mcp-servers
cp -r pptx-mcp-server ~/.kiro/mcp-servers/

# Or clone from GitHub
git clone https://github.com/your-username/pptx-mcp-server.git ~/.kiro/mcp-servers/pptx-mcp-server
```

## Testing

```bash
# Run test suite
python test_mcp_server.py
```

Expected output:
```
============================================================
MCP SERVER TEST SUITE
============================================================
...
✅ ALL TESTS COMPLETED
🎉 The MCP server is working properly!
```

## Usage with Kiro

This MCP server is designed to be used with the **PPTX Power** in Kiro.

1. Install this MCP server to `~/.kiro/mcp-servers/pptx-mcp-server/`
2. Install the PPTX Power through Kiro Powers panel
3. The Power's mcp.json will automatically connect to this server

## Directory Structure

```
pptx-mcp-server/
├── script_executor_mcp.py    # Main MCP server
├── test_mcp_server.py         # Test suite
├── requirements.txt           # Python dependencies
├── scripts/                   # PowerPoint manipulation scripts
│   ├── html2pptx.js          # HTML to PPTX converter
│   ├── inventory.py          # Text extraction
│   ├── rearrange.py          # Slide manipulation
│   ├── replace.py            # Text replacement
│   └── thumbnail.py          # Thumbnail generation
└── ooxml/                     # OOXML utilities
    └── scripts/
        ├── pack.py
        ├── unpack.py
        └── validate.py
```

## Available Tools

### html2pptx
Convert HTML slides to PowerPoint presentation.

**Parameters:**
- `html_files` (array): Array of HTML file paths for each slide
- `output_file` (string): Output .pptx file path
- `config` (object, optional): Configuration for charts, tables, etc.

### inventory
Extract all text shapes and properties from a presentation.

**Parameters:**
- `input_file` (string): Input .pptx file path
- `output_file` (string): Output JSON file path for inventory

### rearrange
Duplicate, reorder, and delete slides in a presentation.

**Parameters:**
- `input_file` (string): Input .pptx file path
- `output_file` (string): Output .pptx file path
- `slide_indices` (string): Comma-separated slide indices (0-based, can repeat)

### replace
Replace text content in presentation while preserving formatting.

**Parameters:**
- `input_file` (string): Input .pptx file path
- `replacement_json` (string): JSON file with replacement text and formatting
- `output_file` (string): Output .pptx file path

### thumbnail
Generate visual thumbnail grids of presentation slides.

**Parameters:**
- `input_file` (string): Input .pptx file path
- `output_prefix` (string, optional): Output file prefix (default: 'thumbnails')
- `columns` (integer, optional): Number of columns 3-6 (default: 5)

## Troubleshooting

### Error: ModuleNotFoundError

**Solution:** Install missing dependencies
```bash
pip install -r requirements.txt
```

### Error: Script not found

**Solution:** Verify all scripts are present
```bash
ls -la scripts/
ls -la ooxml/scripts/
```

### Error: Permission denied

**Solution:** Make scripts executable
```bash
chmod +x scripts/*.py scripts/*.js
chmod +x ooxml/scripts/*.py
```

## Development

### Running Tests

```bash
python test_mcp_server.py
```

### Adding New Tools

1. Add script to `scripts/` directory
2. Update `SCRIPTS` dictionary in `script_executor_mcp.py`
3. Add tests to `test_mcp_server.py`
4. Update this README

## License

[Your License Here]

## Contributing

Contributions welcome! Please open an issue or PR.

## Related

- **PPTX Power** - Kiro Power that uses this MCP server
- **Original Skill** - Converted from Claude Agent Skill
