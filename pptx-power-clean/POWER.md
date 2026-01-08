---
name: "pptx"
displayName: "PowerPoint Presentation Tools"
description: "Create, edit, and analyze PowerPoint presentations (.pptx files) with advanced OOXML manipulation, HTML-to-PPTX conversion, and template-based workflows"
keywords: ["pptx", "powerpoint", "presentation", "slides", "ooxml", "html2pptx"]
author: "Converted from Claude Skill"
version: "1.0.0"
---

# PowerPoint Presentation Tools

## ⚠️ CRITICAL: New Presentation Workflow

**When user requests a NEW presentation, you MUST follow this workflow:**

1. **FIRST: Read `user-request-to-html.md` steering file** (call readSteering action)
2. **Create HTML preview** (`preview.html`) for user to review in browser
3. **WAIT for user approval** before proceeding
4. **Only after approval**: Create individual slide files and convert to PPTX

**DO NOT skip the HTML preview step. DO NOT generate PPTX directly from user request.**

This workflow ensures user can review content/design before PPTX generation.

---

## Overview

This power enables comprehensive PowerPoint presentation creation, editing, and analysis through MCP tools that provide:

- **Text extraction and analysis** - Convert presentations to markdown for content review
- **HTML-to-PPTX conversion** - Create new presentations from HTML with precise positioning
- **OOXML editing** - Direct XML manipulation for advanced editing tasks
- **Template-based creation** - Duplicate and customize existing presentation templates
- **Visual analysis** - Generate thumbnail grids and convert slides to images

**IMPORTANT**: This power provides **MCP tools** for PowerPoint operations. When working with presentations:
- ✅ **USE the MCP tools** (html2pptx, inventory, rearrange, replace, thumbnail)
- ❌ **DO NOT create scripts manually** or try to install libraries yourself
- ✅ **Let the MCP tools handle all PowerPoint operations**

## Installation

**IMPORTANT:** This Power requires a separate MCP server installation.

### Step 1: Install MCP Server

Choose one of the following installation methods:

#### Option A: Install to Standard Location (Recommended)

```bash
# Create MCP servers directory
mkdir -p ~/.kiro/mcp-servers

# Clone the MCP server repository
git clone https://github.com/your-username/pptx-mcp-server.git ~/.kiro/mcp-servers/pptx-mcp-server

# Or manually copy if you have the files locally
cp -r pptx-mcp-server ~/.kiro/mcp-servers/
```

#### Option B: Install from Source

```bash
# If you have the source files
mkdir -p ~/.kiro/mcp-servers/pptx-mcp-server
cd ~/.kiro/mcp-servers/pptx-mcp-server

# Copy all files from pptx-mcp-server directory
# - script_executor_mcp.py
# - scripts/
# - ooxml/
# - requirements.txt
```

### Step 2: Install Dependencies

```bash
cd ~/.kiro/mcp-servers/pptx-mcp-server

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies locally
npm install

# Install system tools
# macOS:
brew install libreoffice poppler

# Ubuntu/Debian:
sudo apt-get install libreoffice poppler-utils
```

### Step 3: Test MCP Server

```bash
cd ~/.kiro/mcp-servers/pptx-mcp-server

# Run test suite
python test_mcp_server.py
```

Expected output:
```
============================================================
✅ ALL TESTS COMPLETED
============================================================
🎉 The MCP server is working properly!
```

### Step 4: Install the Power

1. Open Kiro Powers panel
2. Click "Add from local directory" or "Add Custom Power"
3. Select this power directory
4. The Power will automatically connect to the installed MCP server

**Note:** The MCP server will be **automatically started** by Kiro when the Power is activated. You don't need to manually start the server.

## Available Tools

This power provides 5 MCP tools for PowerPoint manipulation. **Always use these MCP tools instead of writing scripts manually.**

### html2pptx
Convert HTML slides to PowerPoint presentation with precise positioning and styling.

**How to use:**
```
"Use the html2pptx tool to convert these HTML files to PowerPoint:
- slide1.html
- slide2.html  
- slide3.html
Output: presentation.pptx"
```

**Parameters:**
- `html_files` (array): Array of HTML file paths for each slide
- `output_file` (string): Output .pptx file path
- `config` (object, optional): Configuration for charts, tables, etc.

### inventory
Extract all text shapes and properties from a presentation for analysis or modification.

**How to use:**
```
"Use the inventory tool to extract text from presentation.pptx and save to inventory.json"
```

**Parameters:**
- `input_file` (string): Input .pptx file path
- `output_file` (string): Output JSON file path for inventory

### rearrange
Duplicate, reorder, and delete slides in a presentation.

**How to use:**
```
"Use the rearrange tool on template.pptx: keep slides 0, 5, 5, 10 and save to working.pptx"
```

**Parameters:**
- `input_file` (string): Input .pptx file path
- `output_file` (string): Output .pptx file path
- `slide_indices` (string): Comma-separated slide indices (0-based, can repeat)

### replace
Replace text content in presentation while preserving all formatting.

**How to use:**
```
"Use the replace tool to update working.pptx with replacements from replacements.json, save to output.pptx"
```

**Parameters:**
- `input_file` (string): Input .pptx file path
- `replacement_json` (string): JSON file with replacement text and formatting
- `output_file` (string): Output .pptx file path

### thumbnail
Generate visual thumbnail grids of presentation slides for quick review.

**How to use:**
```
"Use the thumbnail tool to generate thumbnails for presentation.pptx with 4 columns"
```

**Parameters:**
- `input_file` (string): Input .pptx file path
- `output_prefix` (string, optional): Output file prefix (default: 'thumbnails')
- `columns` (integer, optional): Number of columns 3-6 (default: 5)

## Common Workflows

### Creating a New Presentation from User Request (RECOMMENDED)

**This is the recommended workflow for new presentations.**

**⚠️ FIRST: Read the `user-request-to-html.md` steering file before starting!**

1. **Create HTML preview** for user review
   - Single-page HTML with all slides
   - Larger dimensions for easy reading (960px × 540px)
   - Get user approval before proceeding

2. **After approval, create individual slide files**
   - One HTML file per slide (720pt × 405pt)
   - Adjust font sizes for smaller dimensions
   - Match content from approved preview

3. **Convert to PowerPoint**
   - Use html2pptx tool to convert HTML files
   - Generate thumbnails to validate layout
   - Make adjustments if needed

**Why this workflow?**
- User can review content before PPTX generation
- Easier to iterate on HTML than PPTX
- Catches issues early
- Ensures alignment with expectations

### Creating a New Presentation from HTML (Direct)

**Use this only if you already have approved HTML slides.**

1. Create HTML files for each slide (720pt × 405pt)
2. Use html2pptx tool to convert to PowerPoint
3. Generate thumbnails to validate layout
4. Make adjustments as needed

### Using a Template

1. Generate thumbnail grid of template
2. Use rearrange tool to duplicate/reorder slides
3. Use inventory tool to extract text shapes
4. Use replace tool to update content with new text

### Editing Existing Presentations

1. Use inventory tool to understand structure
2. Modify content as needed
3. Use replace tool to apply changes
4. Generate thumbnails to verify results

## MCP Server Location

This power expects the MCP server to be installed at:
```
~/.kiro/mcp-servers/pptx-mcp-server/
```

If you installed it elsewhere, update the path in `mcp.json`:
```json
{
  "mcpServers": {
    "pptx-tools": {
      "command": "python",
      "args": ["/your/custom/path/pptx-mcp-server/script_executor_mcp.py"]
    }
  }
}
```

## Troubleshooting

### Error: MCP server not found

**Symptoms:**
- "Connection refused" or "Server not responding"
- Tools not available

**Solution:**
1. Verify MCP server is installed:
   ```bash
   ls -la ~/.kiro/mcp-servers/pptx-mcp-server/script_executor_mcp.py
   ```

2. Test MCP server directly:
   ```bash
   cd ~/.kiro/mcp-servers/pptx-mcp-server
   python script_executor_mcp.py
   # Should start without errors
   ```

3. Check mcp.json path is correct

### Error: ModuleNotFoundError

**Symptoms:**
- "No module named 'mcp'"
- "No module named 'PIL'"
- "No module named 'pptx'"

**Solution:**
```bash
cd ~/.kiro/mcp-servers/pptx-mcp-server
pip install -r requirements.txt
```

### Error: Script not found

**Symptoms:**
- "Script not found at scripts/..."

**Solution:**
1. Verify all scripts are present:
   ```bash
   ls -la ~/.kiro/mcp-servers/pptx-mcp-server/scripts/
   ```

2. Reinstall MCP server if files are missing

### Error: Permission denied

**Symptoms:**
- "Permission denied" when executing scripts

**Solution:**
```bash
cd ~/.kiro/mcp-servers/pptx-mcp-server
chmod +x scripts/*.py scripts/*.js
chmod +x ooxml/scripts/*.py
```

### Tools not appearing in Kiro

**Solution:**
1. Restart Kiro
2. Reinstall the Power
3. Check MCP logs in Kiro for errors

## Available Steering Files

**IMPORTANT:** Read the appropriate steering file BEFORE starting any workflow.

| Steering File | When to Read | Description |
|---------------|--------------|-------------|
| `user-request-to-html.md` | **FIRST** - When creating a new presentation from user request | Complete guide for creating HTML preview for user approval |
| `html2pptx-guide.md` | After user approves HTML preview | HTML to PPTX conversion, validation errors, design guidelines |
| `template-workflow.md` | When using an existing PPTX as template | Template-based creation with rearrange/replace tools |
| `ooxml-guide.md` | For advanced XML editing | Direct OOXML manipulation for complex edits |

**Workflow Decision:**
- User wants a **new presentation** → Read `user-request-to-html.md` first
- User has **approved HTML slides** → Read `html2pptx-guide.md`
- User wants to **modify existing PPTX** → Read `template-workflow.md` or `ooxml-guide.md`

## Technical Details

**Architecture:** Script Executor Pattern
- MCP server executes Python and JavaScript scripts
- Zero-context execution for all operations
- Full control over script execution and error handling

**Supported Formats:**
- Input: .pptx, HTML, JSON
- Output: .pptx, JSON, JPEG (thumbnails)

**Performance:**
- Startup time: < 1 second
- Tool execution: Depends on file size and operation
- Memory: Low (scripts loaded on demand)

## Updates and Maintenance

To update the MCP server:

```bash
cd ~/.kiro/mcp-servers/pptx-mcp-server

# Pull latest changes (if using git)
git pull

# Or manually replace files

# Reinstall dependencies if needed
pip install -r requirements.txt

# Test after update
python test_mcp_server.py
```

No need to reinstall the Power after MCP server updates.

## Related Resources

- **MCP Server Repository:** [GitHub link]
- **Original Claude Skill:** Converted from pptx skill
- **Documentation:** See steering files for detailed guides

---

**Power Type:** Guided MCP Power  
**MCP Server:** pptx-tools  
**Installation:** Two-step (MCP server + Power)  
**Last Updated:** 2026-01-04
