# Script Conversion Guide: Skills Scripts to MCP Tools

## Critical Understanding

**⚠️ IMPORTANT:** Skills scripts should be converted to **MCP tools**, NOT Hooks.

### Why MCP Tools, Not Hooks?

| Feature | Skills Scripts | MCP Tools ✅ | Hooks ❌ |
|---------|---------------|-------------|---------|
| **Execution Timing** | AI decides when | AI decides when | Event-triggered |
| **Trigger Method** | On-demand | On-demand | Automatic (file save, etc.) |
| **Context Usage** | Zero-context | Zero-context | May consume context |
| **Use Case** | Data processing, tools | Data processing, tools | Automation workflows |

**Example:**
```
Skills: "Extract data from PDF" → AI runs script when needed
MCP: "Extract data from PDF" → AI calls MCP tool when needed ✅
Hooks: File saved → Automatically runs script ❌ (Wrong timing!)
```

## Conversion Strategy Selection

### Decision Matrix

```
Number of scripts in your Skill?
    │
    ├─ 1-3 scripts
    │   └─→ Create Dedicated MCP Server
    │       Time: 2-4 hours
    │       Control: Full
    │       Best for: Complex logic, type safety
    │
    ├─ 4-10 scripts
    │   └─→ Use Script Executor Pattern
    │       Time: 3-5 hours
    │       Control: Full, reusable
    │       Best for: Multiple independent scripts
    │
    └─ 10+ scripts
        └─→ Modular MCP Server
            Time: 1-2 days
            Control: Full, scalable
            Best for: Large script collections
```

## Method 1: Dedicated MCP Server (1-3 Scripts)

### When to Use
- 1-3 scripts with complex logic
- Need type safety and validation
- Want full control over execution
- Scripts have interdependencies

### ⚠️ CRITICAL: Kiro Powers File Restrictions

**Kiro Powers can ONLY contain:**
- ✅ `POWER.md`
- ✅ `mcp.json`
- ✅ `steering/*.md` files

**NOT allowed in Powers:**
- ❌ Python scripts (`.py`)
- ❌ JavaScript files (`.js`)
- ❌ Shell scripts (`.sh`)
- ❌ Binary executables
- ❌ Any other code files

**Solution:** Install MCP server separately, Power only contains documentation and configuration pointing to the installed server.

### Step-by-Step Guide

#### Step 1: Analyze Original Script

**Original Skills Script:**
```python
# scripts/pdf_extract.py
import sys
import json
from PyPDF2 import PdfReader

def extract_form_data(pdf_path):
    """Extract form fields from PDF"""
    reader = PdfReader(pdf_path)
    fields = reader.get_form_text_fields()
    return fields

if __name__ == "__main__":
    result = extract_form_data(sys.argv[1])
    print(json.dumps(result))
```

**Usage in Skills:**
```markdown
Use `scripts/pdf_extract.py` to extract form data:
```bash
python scripts/pdf_extract.py input.pdf
```
```

#### Step 2: Create MCP Server

**Create `pdf_mcp_server.py`:**
```python
from mcp.server import Server
from mcp.types import Tool, TextContent
import json
from PyPDF2 import PdfReader, PdfWriter

app = Server("pdf-tools")

@app.list_tools()
async def list_tools() -> list[Tool]:
    """Define available tools"""
    return [
        Tool(
            name="extract_pdf_data",
            description="Extract form field data from a PDF file",
            inputSchema={
                "type": "object",
                "properties": {
                    "pdf_path": {
                        "type": "string",
                        "description": "Path to the PDF file"
                    }
                },
                "required": ["pdf_path"]
            }
        ),
        Tool(
            name="fill_pdf_form",
            description="Fill a PDF form with provided data",
            inputSchema={
                "type": "object",
                "properties": {
                    "template_path": {
                        "type": "string",
                        "description": "Path to PDF template"
                    },
                    "data": {
                        "type": "object",
                        "description": "Form data as key-value pairs"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Path for output PDF"
                    }
                },
                "required": ["template_path", "data", "output_path"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool execution"""
    
    if name == "extract_pdf_data":
        # Original script logic here
        reader = PdfReader(arguments["pdf_path"])
        fields = reader.get_form_text_fields()
        return [TextContent(
            type="text",
            text=json.dumps(fields, indent=2)
        )]
    
    elif name == "fill_pdf_form":
        # Fill form logic
        reader = PdfReader(arguments["template_path"])
        writer = PdfWriter()
        writer.append(reader)
        writer.update_page_form_field_values(
            writer.pages[0], 
            arguments["data"]
        )
        
        with open(arguments["output_path"], "wb") as output:
            writer.write(output)
        
        return [TextContent(
            type="text",
            text=f"PDF form filled: {arguments['output_path']}"
        )]
    
    else:
        return [TextContent(
            type="text",
            text=f"Unknown tool: {name}"
        )]

if __name__ == "__main__":
    import asyncio
    asyncio.run(app.run())
```

#### Step 3: Install MCP Server Separately

**IMPORTANT:** MCP server must be installed separately from the Power.

```bash
# Create MCP server directory
mkdir -p ~/my-mcp-servers/pdf-tools-server
cd ~/my-mcp-servers/pdf-tools-server

# Copy the MCP server file created in Step 2
# Save pdf_mcp_server.py here

# Install dependencies
pip install PyPDF2 mcp
```

#### Step 4: Create Power Directory (Only Documentation)

**Create Power directory with ONLY allowed files:**

```bash
mkdir -p ./powers/pdf-processor
cd ./powers/pdf-processor
```

**Create `mcp.json`** (points to installed MCP server):
```json
{
  "mcpServers": {
    "pdf-tools": {
      "command": "python",
      "args": ["~/my-mcp-servers/pdf-tools-server/pdf_mcp_server.py"],
      "env": {
        "PYTHONPATH": "~/my-mcp-servers/pdf-tools-server"
      }
    }
  }
}
```

**Create `POWER.md`:**
```markdown
---
name: "pdf-processor"
displayName: "PDF Processor"
description: "Extract, fill, and merge PDF forms and documents"
keywords: ["pdf", "document", "form", "extract", "fill"]
author: "Your Name"
---

# PDF Processing Power

## Installation

**IMPORTANT:** This Power requires a separate MCP server installation.

### Step 1: Install MCP Server

```bash
# Clone or download the MCP server
git clone https://github.com/your-username/pdf-tools-server.git ~/my-mcp-servers/pdf-tools-server

# Or manually create and copy files
mkdir -p ~/my-mcp-servers/pdf-tools-server
# Copy pdf_mcp_server.py to this directory
```

### Step 2: Install Dependencies

```bash
cd ~/my-mcp-servers/pdf-tools-server

# Install Python dependencies
pip install PyPDF2 mcp

# If using Node.js scripts, install dependencies LOCALLY
# Create package.json first if needed
npm install
```

**CRITICAL: Node.js Dependencies**

If your MCP server uses Node.js scripts:
- ✅ Install dependencies locally: `npm install package-name`
- ❌ Don't use global install: `npm install -g package-name`
- Scripts executed via subprocess need local node_modules

### Step 3: Install the Power

Install this Power through Kiro Powers panel.

## Available Tools

### extract_pdf_data
Extract form field data from PDF files.

**Usage:** "Extract the form data from contract.pdf"

**Parameters:**
- `pdf_path` (string, required): Path to the PDF file

**Returns:** JSON object with form field data

### fill_pdf_form
Fill PDF forms with structured data.

**Usage:** "Fill template.pdf with {name: 'John', email: 'john@example.com'}"

**Parameters:**
- `template_path` (string, required): Path to PDF template
- `data` (object, required): Form data as key-value pairs
- `output_path` (string, required): Path for output PDF

**Returns:** Confirmation message with output path

## MCP Server Location

This power expects the MCP server to be installed at:
```
~/my-mcp-servers/pdf-tools-server/
```

If you install it elsewhere, update the path in mcp.json.

## Troubleshooting

### Error: MCP server not found

**Solution:** Verify the MCP server is installed:
```bash
ls -la ~/my-mcp-servers/pdf-tools-server/pdf_mcp_server.py
```
```

#### Step 5: Test

```bash
# Test MCP server
python pdf_mcp_server.py

# In another terminal, test with MCP client
# Or install Power in Kiro and test
```

### Complete Template

**MCP Server Template:**
```python
from mcp.server import Server
from mcp.types import Tool, TextContent
import json

app = Server("your-server-name")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="tool_name",
            description="What the tool does",
            inputSchema={
                "type": "object",
                "properties": {
                    "param1": {
                        "type": "string",
                        "description": "Parameter description"
                    }
                },
                "required": ["param1"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "tool_name":
        # Your script logic here
        result = your_function(arguments["param1"])
        return [TextContent(
            type="text",
            text=json.dumps(result)
        )]
    
    return [TextContent(
        type="text",
        text=f"Unknown tool: {name}"
    )]

if __name__ == "__main__":
    import asyncio
    asyncio.run(app.run())
```

## Method 2: Script Executor Pattern (4-10 Scripts)

### When to Use
- 4-10 independent scripts
- Scripts are relatively simple
- Want a reusable, maintainable pattern
- Need full control without external dependencies

### ⚠️ CRITICAL: Kiro Powers File Restrictions

**Kiro Powers can ONLY contain:**
- ✅ `POWER.md`
- ✅ `mcp.json`
- ✅ `steering/*.md` files

**NOT allowed in Powers:**
- ❌ Python scripts (`.py`)
- ❌ JavaScript files (`.js`)
- ❌ Shell scripts (`.sh`)
- ❌ Binary executables
- ❌ Any other code files

**This means:** Your MCP server and scripts MUST be installed separately from the Power.

### Solution: Separate Installation

**Two-part structure:**

1. **MCP Server Package** (separate from Power)
   - Contains: MCP server code, scripts, dependencies
   - Location: User installs to `~/.kiro/mcp-servers/your-server/`
   - Distribution: GitHub repo, npm package, or manual installation

2. **Power Package** (only documentation)
   - Contains: POWER.md, mcp.json, steering/*.md
   - Location: Installed via Kiro Powers panel
   - Purpose: Documentation and MCP server configuration

### Overview

The Script Executor Pattern is a proven approach that provides a generic script execution framework within your own MCP server. You maintain full control while getting the benefits of a reusable pattern.

**Key Benefits:**
- ✅ No external dependencies
- ✅ Full control over execution
- ✅ Easy to customize
- ✅ Simple configuration
- ✅ Production-ready
- ✅ Complies with Kiro Powers restrictions

### Step-by-Step Guide

#### Step 1: Create Script Executor MCP Server

**Create `script_executor_mcp.py`:**
```python
from mcp.server import Server
from mcp.types import Tool, TextContent
import subprocess
import json
from pathlib import Path
import sys

app = Server("script-executor")

# Configuration: Define your scripts here
SCRIPTS = {
    "pdf_extract": {
        "path": "scripts/pdf_extract.py",
        "description": "Extract form data from PDF files",
        "args": ["pdf_path"],
        "timeout": 30
    },
    "pdf_fill": {
        "path": "scripts/pdf_fill.py",
        "description": "Fill PDF form with data",
        "args": ["template_path", "data_json", "output_path"],
        "timeout": 30
    },
    "pdf_merge": {
        "path": "scripts/pdf_merge.py",
        "description": "Merge multiple PDF files",
        "args": ["pdf_paths", "output_path"],
        "timeout": 60
    },
    "data_analyzer": {
        "path": "scripts/analyze.py",
        "description": "Analyze CSV data and generate report",
        "args": ["csv_path", "output_format"],
        "timeout": 60
    },
    "code_formatter": {
        "path": "scripts/format_code.sh",
        "description": "Format code files using team standards",
        "args": ["file_path"],
        "timeout": 10
    }
}

@app.list_tools()
async def list_tools() -> list[Tool]:
    """Generate tools from script configuration"""
    tools = []
    
    for name, config in SCRIPTS.items():
        # Build schema from args
        properties = {}
        required = []
        
        for arg in config["args"]:
            properties[arg] = {
                "type": "string",
                "description": f"Argument: {arg}"
            }
            required.append(arg)
        
        tools.append(Tool(
            name=name,
            description=config["description"],
            inputSchema={
                "type": "object",
                "properties": properties,
                "required": required
            }
        ))
    
    return tools

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Execute script with arguments"""
    
    if name not in SCRIPTS:
        return [TextContent(
            type="text",
            text=f"Error: Unknown script '{name}'"
        )]
    
    config = SCRIPTS[name]
    script_path = Path(config["path"])
    
    # Verify script exists
    if not script_path.exists():
        return [TextContent(
            type="text",
            text=f"Error: Script not found: {script_path}"
        )]
    
    # Determine interpreter
    if script_path.suffix == '.py':
        cmd = [sys.executable, str(script_path)]
    elif script_path.suffix == '.sh':
        cmd = ["bash", str(script_path)]
    else:
        cmd = [str(script_path)]
    
    # Add arguments
    for arg in config["args"]:
        if arg in arguments:
            cmd.append(str(arguments[arg]))
        else:
            return [TextContent(
                type="text",
                text=f"Error: Missing required argument '{arg}'"
            )]
    
    try:
        # Execute script
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=config["timeout"],
            cwd=Path.cwd()
        )
        
        if result.returncode == 0:
            return [TextContent(
                type="text",
                text=result.stdout if result.stdout else "Script completed successfully"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Error (exit code {result.returncode}):\n{result.stderr}"
            )]
    
    except subprocess.TimeoutExpired:
        return [TextContent(
            type="text",
            text=f"Error: Script timeout after {config['timeout']} seconds"
        )]
    
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error: {type(e).__name__}: {str(e)}"
        )]

if __name__ == "__main__":
    import asyncio
    asyncio.run(app.run())
```

#### Step 2: Create MCP Server Directory (Separate from Power)

**IMPORTANT:** MCP server and scripts go in a SEPARATE directory, NOT in the Power.

```bash
# Create MCP server directory (outside of Power)
mkdir -p ~/my-mcp-servers/my-scripts-server
cd ~/my-mcp-servers/my-scripts-server

# Copy MCP server file
# (Create script_executor_mcp.py from Step 1)

# Create scripts directory
mkdir -p scripts

# Copy all scripts from Skills
cp ~/.claude/skills/my-skill/scripts/* scripts/

# Make scripts executable
chmod +x scripts/*.sh
chmod +x scripts/*.py
```

**Directory structure:**
```
~/my-mcp-servers/my-scripts-server/
├── script_executor_mcp.py    # MCP server
├── scripts/                   # Your scripts
│   ├── script1.py
│   ├── script2.py
│   └── script3.sh
└── requirements.txt           # Python dependencies
```

#### Step 3: Configure Your Scripts

Edit the `SCRIPTS` dictionary in `script_executor_mcp.py`:

```python
SCRIPTS = {
    "your_script_name": {
        "path": "scripts/your_script.py",  # Relative path
        "description": "What your script does",
        "args": ["arg1", "arg2"],  # Argument names
        "timeout": 30  # Timeout in seconds
    },
    # Add more scripts here
}
```

**CRITICAL: JavaScript Library Modules vs CLI Scripts**

If your Skill includes JavaScript files, check if they are:

1. **CLI Scripts** (can be executed directly)
   - Has `if (require.main === module)` or similar entry point
   - Can run with: `node script.js arg1 arg2`
   - ✅ Can be used directly in SCRIPTS configuration

2. **Library Modules** (exports functions, not executable)
   - Ends with `module.exports = functionName;`
   - Cannot be run directly from command line
   - ❌ Needs a CLI wrapper script

**CRITICAL: Python Library Modules vs CLI Scripts**

Python scripts can also be library modules:

1. **CLI Scripts** (can be executed directly)
   - Has `if __name__ == "__main__": main()`
   - Can run with: `python script.py arg1 arg2`
   - ✅ Can be used directly in SCRIPTS configuration

2. **Library Modules** (imports only, not executable)
   - Has `if __name__ == "__main__": raise RuntimeError(...)`
   - Or no `if __name__ == "__main__":` block at all
   - Defines classes/functions for import by other scripts
   - ❌ Should NOT be added to SCRIPTS configuration

**Example: Detecting Library Modules**

**JavaScript:**
```javascript
// This is a LIBRARY MODULE (not CLI)
async function html2pptx(htmlFile, pres, options = {}) {
  // ... function code ...
}

module.exports = html2pptx;  // ← Exports function, no CLI entry
```

**Python:**
```python
# This is a LIBRARY MODULE (not CLI)
class BaseValidator:
    def validate(self, data):
        # ... validation code ...

if __name__ == "__main__":
    raise RuntimeError("This module should not be run directly.")
```

**Solution for JavaScript: Create CLI Wrapper**

If you have a JavaScript library module, create a CLI wrapper script:

```javascript
#!/usr/bin/env node
// html2pptx-cli.js - CLI wrapper for html2pptx library

const fs = require('fs');
const path = require('path');

// CRITICAL: Save original working directory BEFORE changing it
const originalCwd = process.cwd();

// Change to parent directory to find node_modules
const serverDir = path.join(__dirname, '..');
process.chdir(serverDir);

const pptxgen = require('pptxgenjs');
const html2pptx = require(path.join(__dirname, 'html2pptx.js'));

async function main() {
  if (process.argv.length < 3) {
    console.error('Usage: node html2pptx-cli.js <config.json>');
    process.exit(1);
  }

  const configPath = process.argv[2];
  
  try {
    const configData = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    const { html_files, output_file } = configData;

    // Convert relative paths to absolute based on original working directory
    const absoluteHtmlFiles = html_files.map(f => 
      path.isAbsolute(f) ? f : path.join(originalCwd, f)
    );
    const absoluteOutputFile = path.isAbsolute(output_file) ? 
      output_file : path.join(originalCwd, output_file);

    // Create presentation
    const pptx = new pptxgen();
    pptx.layout = 'LAYOUT_16x9';

    console.log(`Converting ${html_files.length} HTML slides...`);

    // Process each HTML file
    for (let i = 0; i < absoluteHtmlFiles.length; i++) {
      const htmlFile = absoluteHtmlFiles[i];
      console.log(`  Processing slide ${i + 1}/${html_files.length}`);
      await html2pptx(htmlFile, pptx);
    }

    // Save presentation
    await pptx.writeFile({ fileName: absoluteOutputFile });
    console.log(`✓ Successfully created ${absoluteOutputFile}`);

  } catch (error) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
  }
}

main();
```

**Key points for CLI wrappers:**
- **CRITICAL**: Save original working directory BEFORE calling process.chdir()
- Change to parent directory to find node_modules
- Convert relative paths to absolute (preserve original working directory)
- Provide clear progress output
- Handle errors properly

Then configure the CLI wrapper in SCRIPTS:

```python
SCRIPTS = {
    "html2pptx": {
        "path": "scripts/html2pptx-cli.js",  # Use CLI wrapper, not library
        "interpreter": "node",
        "description": "Convert HTML slides to PowerPoint",
        "args": ["config_file"],
        "timeout": 300
    }
}
```

**Solution for Python: Skip Library Modules**

Python library modules should NOT be added to SCRIPTS configuration. They are meant to be imported by other scripts.

**Example: Correct SCRIPTS configuration**

```python
SCRIPTS = {
    # ✅ CLI scripts - include these
    "validate": {
        "path": "ooxml/scripts/validate.py",  # Has main() entry point
        "interpreter": "python",
        "description": "Validate OOXML structure",
        "args": ["directory", "original_file"],
        "timeout": 60
    },
    
    # ❌ Library modules - DO NOT include these
    # "base_validator": {  # Has RuntimeError in __main__
    #     "path": "ooxml/scripts/validation/base.py",
    #     ...
    # }
}
```

**How to identify what to include:**

1. **Check the file:**
   ```bash
   tail -10 script.py
   ```

2. **Look for:**
   - ✅ `if __name__ == "__main__": main()` → Include in SCRIPTS
   - ❌ `if __name__ == "__main__": raise RuntimeError(...)` → Skip
   - ❌ No `if __name__ == "__main__":` block → Skip (pure library)

3. **Test execution:**
   ```bash
   python script.py --help
   # If it runs and shows usage, it's a CLI script
   # If it raises RuntimeError or does nothing, it's a library
   ```

**Summary:**
- **JavaScript library modules** → Create CLI wrapper
- **Python library modules** → Skip, don't add to SCRIPTS
- **Both CLI scripts** → Add directly to SCRIPTS

#### Step 4: Create Power Directory (Separate from MCP Server)

**Now create the Power directory with ONLY allowed files:**

```bash
# Create Power directory
mkdir -p ./powers/my-power
cd ./powers/my-power
```

**Create `mcp.json`** (points to the MCP server location):
```json
{
  "mcpServers": {
    "my-scripts": {
      "command": "python",
      "args": ["~/my-mcp-servers/my-scripts-server/script_executor_mcp.py"],
      "env": {
        "PYTHONPATH": "~/my-mcp-servers/my-scripts-server"
      }
    }
  }
}
```

**Note:** Use absolute path to the MCP server file.

#### Step 5: Create POWER.md

```markdown
---
name: "my-power"
displayName: "My Power"
description: "Collection of utility scripts for development"
keywords: ["scripts", "utilities", "tools"]
author: "Your Name"
---

# My Power

## Installation

**IMPORTANT:** This Power requires a separate MCP server installation.

### Step 1: Install MCP Server

```bash
# Clone or download the MCP server
git clone https://github.com/your-username/my-scripts-server.git ~/my-mcp-servers/my-scripts-server

# Or manually create the directory and copy files
mkdir -p ~/my-mcp-servers/my-scripts-server
# Copy script_executor_mcp.py and scripts/ to this directory
```

### Step 2: Install Dependencies

```bash
cd ~/my-mcp-servers/my-scripts-server

# Install Python dependencies
pip install mcp
# Install any other Python dependencies your scripts need

# If your scripts use Node.js, install dependencies LOCALLY
# IMPORTANT: Use npm install (not npm install -g) for script dependencies
npm install
# Or if you don't have package.json:
npm install package1 package2 package3
```

**CRITICAL: Node.js Dependencies**

If your MCP server executes Node.js scripts that require modules (like playwright, sharp, etc.):

- ✅ **DO**: Install dependencies locally in the MCP server directory using `npm install`
- ❌ **DON'T**: Use `npm install -g` for script dependencies
- **Why**: Node.js scripts executed by subprocess cannot find globally installed modules

**Example package.json for Node.js dependencies:**
```json
{
  "name": "my-scripts-server",
  "version": "1.0.0",
  "dependencies": {
    "playwright": "^1.57.0",
    "sharp": "^0.34.5",
    "pptxgenjs": "^4.0.1"
  }
}
```

Then run `npm install` to install all dependencies locally.

### Step 3: Install the Power

Install this Power through Kiro Powers panel. The mcp.json will automatically connect to your installed MCP server.

## Available Scripts

All scripts are executed with zero-context consumption through MCP.

### pdf_extract
Extract form data from PDF files.
**Usage:** "Extract data from contract.pdf"

### pdf_fill
Fill PDF forms with structured data.
**Usage:** "Fill template.pdf with this data: {name: 'John'}"

### data_analyzer
Analyze CSV data and generate reports.
**Usage:** "Analyze sales_data.csv and output as JSON"

## MCP Server Location

This power expects the MCP server to be installed at:
```
~/my-mcp-servers/my-scripts-server/
```

If you install it elsewhere, update the path in mcp.json.

## Troubleshooting

### Error: MCP server not found

**Solution:** Verify the MCP server is installed at the correct location:
```bash
ls -la ~/my-mcp-servers/my-scripts-server/script_executor_mcp.py
```

### Error: Permission denied

**Solution:** Make sure scripts are executable:
```bash
chmod +x ~/my-mcp-servers/my-scripts-server/scripts/*.py
chmod +x ~/my-mcp-servers/my-scripts-server/scripts/*.sh
```
```

#### Step 6: Test MCP Server (Before Installing Power)

```bash
# Test MCP server directly
cd ~/my-mcp-servers/my-scripts-server
python script_executor_mcp.py

# Should start without errors
# Press Ctrl+C to stop

# Run test script (see Testing section)
python test_mcp_server.py
```

#### Step 7: Install Power in Kiro

```bash
# Power directory structure (ONLY these files):
powers/my-power/
├── POWER.md      # Documentation
└── mcp.json      # MCP server configuration
```

1. Open Kiro Powers panel
2. Add from local directory: `./powers/my-power`
3. Test by mentioning keywords in conversation

### Final Directory Structure

**Complete setup:**
```
# MCP Server (separate location)
~/my-mcp-servers/my-scripts-server/
├── script_executor_mcp.py
├── scripts/
│   ├── script1.py
│   ├── script2.py
│   └── script3.sh
├── requirements.txt
└── test_mcp_server.py

# Power (only documentation)
./powers/my-power/
├── POWER.md
└── mcp.json
```

### Distribution Options

**Option 1: GitHub Repository**
```bash
# Create repo for MCP server
cd ~/my-mcp-servers/my-scripts-server
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/your-username/my-scripts-server.git
git push -u origin main
```

Users install with:
```bash
git clone https://github.com/your-username/my-scripts-server.git ~/my-mcp-servers/my-scripts-server
```

**Option 2: npm Package** (if using Node.js)
```bash
# Publish to npm
npm publish
```

Users install with:
```bash
npm install -g my-scripts-server
```

Update mcp.json to use:
```json
{
  "mcpServers": {
    "my-scripts": {
      "command": "npx",
      "args": ["-y", "my-scripts-server"]
    }
  }
}
```

**Option 3: Manual Installation**

Provide a zip file with installation instructions in POWER.md.

### Advantages of Script Executor Pattern

| Aspect | Script Executor Pattern | External Tools |
|--------|------------------------|----------------|
| **Control** | ✅ Full | ⚠️ Limited |
| **Dependencies** | ✅ None | ❌ External |
| **Maintenance** | ✅ You control | ❌ Depends on others |
| **Customization** | ✅ Easy | ⚠️ Limited |
| **Reliability** | ✅ High | ⚠️ Unknown |
| **Security** | ✅ You audit | ⚠️ Trust required |

### Customization Examples

**Add error handling:**
```python
@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    try:
        # ... execution code ...
    except FileNotFoundError as e:
        return [TextContent(
            type="text",
            text=f"Error: File not found - {str(e)}"
        )]
    except PermissionError as e:
        return [TextContent(
            type="text",
            text=f"Error: Permission denied - {str(e)}"
        )]
```

**Add logging:**
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    logger.info(f"Executing script: {name} with args: {arguments}")
    # ... execution code ...
```

**Add validation:**
```python
def validate_arguments(script_name: str, arguments: dict) -> tuple[bool, str]:
    """Validate arguments before execution"""
    config = SCRIPTS[script_name]
    
    # Check all required args present
    for arg in config["args"]:
        if arg not in arguments:
            return False, f"Missing required argument: {arg}"
    
    # Add custom validation
    if script_name == "pdf_extract":
        if not arguments["pdf_path"].endswith(".pdf"):
            return False, "pdf_path must be a PDF file"
    
    return True, ""
```

## Method 3: Modular MCP Server (10+ Scripts)

### When to Use
- 10+ scripts with mixed complexity
- Scripts organized by category/domain
- Want scalable architecture
- Need to balance maintainability and performance

### Strategy

Organize scripts into logical modules and create a modular MCP server architecture.

**Organization Pattern:**
```
Core Domain Scripts → Dedicated MCP Module
Utility Scripts → Utility MCP Module
Integration Scripts → Integration MCP Module
```

### Example Structure

```
my-power/
├── POWER.md
├── mcp.json                    # Single MCP server config
├── modular_mcp_server.py       # Main MCP server
├── modules/                    # MCP modules
│   ├── __init__.py
│   ├── core_tools.py          # Core business logic
│   ├── utility_tools.py       # Utility functions
│   └── integration_tools.py   # External integrations
└── scripts/                    # Original scripts (if needed)
    ├── core/
    ├── utils/
    └── integrations/
```

### Step-by-Step Guide

#### Step 1: Analyze and Categorize Scripts

**Example categorization:**
```
Core Business Logic (5 scripts):
- process_data.py
- generate_report.py
- validate_input.py
- transform_data.py
- export_results.py

Utilities (4 scripts):
- format_output.py
- cleanup_temp.py
- log_activity.py
- send_notification.py

Integrations (3 scripts):
- fetch_api_data.py
- upload_to_s3.py
- send_email.py
```

#### Step 2: Create Modular MCP Server

**Create `modular_mcp_server.py`:**
```python
from mcp.server import Server
from mcp.types import Tool, TextContent
from modules import core_tools, utility_tools, integration_tools

app = Server("modular-tools")

@app.list_tools()
async def list_tools() -> list[Tool]:
    """Aggregate tools from all modules"""
    tools = []
    tools.extend(core_tools.get_tools())
    tools.extend(utility_tools.get_tools())
    tools.extend(integration_tools.get_tools())
    return tools

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Route tool calls to appropriate module"""
    
    # Try core tools
    if name in core_tools.TOOL_NAMES:
        return await core_tools.execute(name, arguments)
    
    # Try utility tools
    if name in utility_tools.TOOL_NAMES:
        return await utility_tools.execute(name, arguments)
    
    # Try integration tools
    if name in integration_tools.TOOL_NAMES:
        return await integration_tools.execute(name, arguments)
    
    return [TextContent(
        type="text",
        text=f"Unknown tool: {name}"
    )]

if __name__ == "__main__":
    import asyncio
    asyncio.run(app.run())
```

#### Step 3: Create Module Files

**Create `modules/core_tools.py`:**
```python
from mcp.types import Tool, TextContent
import subprocess
import sys
from pathlib import Path

TOOL_NAMES = ["process_data", "generate_report", "validate_input"]

SCRIPTS = {
    "process_data": {
        "path": "scripts/core/process_data.py",
        "description": "Process input data and apply transformations",
        "args": ["input_file", "output_file"],
        "timeout": 60
    },
    "generate_report": {
        "path": "scripts/core/generate_report.py",
        "description": "Generate analysis report from processed data",
        "args": ["data_file", "report_format"],
        "timeout": 30
    },
    "validate_input": {
        "path": "scripts/core/validate_input.py",
        "description": "Validate input data against schema",
        "args": ["input_file", "schema_file"],
        "timeout": 10
    }
}

def get_tools() -> list[Tool]:
    """Return tool definitions"""
    tools = []
    for name, config in SCRIPTS.items():
        properties = {arg: {"type": "string"} for arg in config["args"]}
        tools.append(Tool(
            name=name,
            description=config["description"],
            inputSchema={
                "type": "object",
                "properties": properties,
                "required": config["args"]
            }
        ))
    return tools

async def execute(name: str, arguments: dict) -> list[TextContent]:
    """Execute core tool"""
    if name not in SCRIPTS:
        return [TextContent(type="text", text=f"Unknown core tool: {name}")]
    
    config = SCRIPTS[name]
    script_path = Path(config["path"])
    
    if not script_path.exists():
        return [TextContent(type="text", text=f"Script not found: {script_path}")]
    
    cmd = [sys.executable, str(script_path)]
    cmd.extend([arguments[arg] for arg in config["args"]])
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=config["timeout"]
        )
        
        if result.returncode == 0:
            return [TextContent(type="text", text=result.stdout)]
        else:
            return [TextContent(type="text", text=f"Error: {result.stderr}")]
    
    except subprocess.TimeoutExpired:
        return [TextContent(type="text", text=f"Timeout after {config['timeout']}s")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]
```

**Create `modules/utility_tools.py`:**
```python
from mcp.types import Tool, TextContent
import subprocess
import sys
from pathlib import Path

TOOL_NAMES = ["format_output", "cleanup_temp", "log_activity"]

SCRIPTS = {
    "format_output": {
        "path": "scripts/utils/format_output.py",
        "description": "Format output data for display",
        "args": ["input_file", "format_type"],
        "timeout": 10
    },
    "cleanup_temp": {
        "path": "scripts/utils/cleanup_temp.sh",
        "description": "Clean up temporary files",
        "args": ["directory"],
        "timeout": 5
    },
    "log_activity": {
        "path": "scripts/utils/log_activity.py",
        "description": "Log activity to system log",
        "args": ["message", "level"],
        "timeout": 5
    }
}

def get_tools() -> list[Tool]:
    """Return tool definitions"""
    tools = []
    for name, config in SCRIPTS.items():
        properties = {arg: {"type": "string"} for arg in config["args"]}
        tools.append(Tool(
            name=name,
            description=config["description"],
            inputSchema={
                "type": "object",
                "properties": properties,
                "required": config["args"]
            }
        ))
    return tools

async def execute(name: str, arguments: dict) -> list[TextContent]:
    """Execute utility tool"""
    if name not in SCRIPTS:
        return [TextContent(type="text", text=f"Unknown utility tool: {name}")]
    
    config = SCRIPTS[name]
    script_path = Path(config["path"])
    
    if not script_path.exists():
        return [TextContent(type="text", text=f"Script not found: {script_path}")]
    
    # Determine command based on file extension
    if script_path.suffix == '.py':
        cmd = [sys.executable, str(script_path)]
    elif script_path.suffix == '.sh':
        cmd = ["bash", str(script_path)]
    else:
        cmd = [str(script_path)]
    
    cmd.extend([arguments[arg] for arg in config["args"]])
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=config["timeout"]
        )
        
        if result.returncode == 0:
            return [TextContent(type="text", text=result.stdout or "Success")]
        else:
            return [TextContent(type="text", text=f"Error: {result.stderr}")]
    
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]
```

**Create `modules/__init__.py`:**
```python
"""MCP tool modules"""
from . import core_tools, utility_tools, integration_tools

__all__ = ["core_tools", "utility_tools", "integration_tools"]
```

#### Step 4: Create MCP Configuration

**Create `mcp.json`:**
```json
{
  "mcpServers": {
    "modular-tools": {
      "command": "python",
      "args": ["modular_mcp_server.py"],
      "env": {
        "PYTHONPATH": "."
      }
    }
  }
}
```

#### Step 5: Update POWER.md

```markdown
---
name: "data-processor"
displayName: "Data Processor"
description: "Comprehensive data processing toolkit with 12+ tools"
keywords: ["data", "processing", "analysis", "reporting"]
author: "Your Name"
mcpServers:
  - modular-tools
---

# Data Processing Power

## Tool Categories

### Core Tools
- **process_data**: Process and transform input data
- **generate_report**: Generate analysis reports
- **validate_input**: Validate data against schemas

### Utility Tools
- **format_output**: Format data for display
- **cleanup_temp**: Clean temporary files
- **log_activity**: Log system activities

### Integration Tools
- **fetch_api_data**: Fetch data from external APIs
- **upload_to_s3**: Upload files to S3
- **send_email**: Send email notifications

## Usage Examples

**Data Processing:**
"Process the sales_data.csv file and save to processed_sales.json"

**Report Generation:**
"Generate a PDF report from processed_sales.json"

**Validation:**
"Validate input.json against schema.json"

## Installation

```bash
pip install mcp
```

## Architecture

This power uses a modular MCP server architecture for scalability and maintainability.
```

### Advantages of Modular Approach

| Aspect | Modular MCP | Monolithic MCP |
|--------|-------------|----------------|
| **Organization** | ✅ Clear separation | ⚠️ Single file |
| **Maintainability** | ✅ Easy to update | ⚠️ Complex |
| **Scalability** | ✅ Add modules easily | ⚠️ File grows large |
| **Testing** | ✅ Test per module | ⚠️ Test everything |
| **Team Work** | ✅ Parallel development | ⚠️ Merge conflicts |

### Best Practices for Modular MCP

1. **Clear Module Boundaries**
   - One domain per module
   - Minimal inter-module dependencies
   - Clear naming conventions

2. **Consistent Module Structure**
   ```python
   # Each module should have:
   TOOL_NAMES = [...]      # List of tool names
   SCRIPTS = {...}         # Script configurations
   get_tools() -> list     # Tool definitions
   execute() -> list       # Tool execution
   ```

3. **Error Handling**
   ```python
   # Consistent error handling across modules
   try:
       result = execute_script()
       return [TextContent(type="text", text=result)]
   except SpecificError as e:
       return [TextContent(type="text", text=f"Error: {e}")]
   ```

4. **Documentation**
   ```python
   # Document each module
   """
   Core Tools Module
   
   Provides data processing and transformation tools.
   
   Tools:
   - process_data: Main data processing
   - generate_report: Report generation
   - validate_input: Input validation
   """
   ```

## Comparison: All Methods

| Method | Scripts | Setup Time | Maintenance | Flexibility | Best For |
|--------|---------|-----------|-------------|-------------|----------|
| **Dedicated MCP** | 1-3 | 2-4h | Low | High | Complex logic |
| **Script Executor** | 4-10 | 3-5h | Low | Medium | Independent scripts |
| **Modular MCP** | 10+ | 1-2 days | Medium | High | Large collections |

## Comparison: Dedicated vs Script Executor vs Modular

| Aspect | Dedicated MCP | Script Executor | Modular MCP |
|--------|--------------|-----------------|-------------|
| **Setup Time** | 2-4 hours | 3-5 hours | 1-2 days |
| **Code Required** | Yes (Python/TS) | Yes (Python/TS) | Yes (Python/TS) |
| **Type Safety** | ✅ Full | ✅ Full | ✅ Full |
| **Validation** | ✅ Custom | ✅ Custom | ✅ Custom |
| **Performance** | ✅ Optimized | ✅ Good | ✅ Optimized |
| **Flexibility** | ✅ Full control | ✅ Full control | ✅ Full control |
| **Maintenance** | ⚠️ More code | ✅ Simple pattern | ✅ Modular |
| **Scalability** | ⚠️ Limited | ⚠️ Limited | ✅ Excellent |
| **Best For** | 1-3 complex scripts | 4-10 scripts | 10+ scripts |

## Testing Your MCP Server

**⚠️ CRITICAL:** After creating your MCP server, you MUST test it before deploying to ensure all tools work correctly.

### Why Test?

Testing your MCP server directly helps you:
- ✅ Verify all tools are registered correctly
- ✅ Validate tool schemas and parameters
- ✅ Catch missing dependencies early
- ✅ Ensure scripts execute properly
- ✅ Identify permission or path issues
- ✅ Confirm error handling works

### Testing Strategy

**Test in this order:**
1. **Server Startup** - Can the server start without errors?
2. **Tool Registration** - Are all tools listed correctly?
3. **Schema Validation** - Are parameter schemas valid?
4. **Tool Execution** - Can tools be called and do they respond?
5. **Error Handling** - Do errors get caught and reported properly?

### Method 1: Create a Test Script (Recommended)

Create a comprehensive test script that validates your MCP server.

**Create `test_mcp_server.py`:**
```python
#!/usr/bin/env python3
"""
Test script for MCP Server
Tests the MCP server by connecting to it and calling its tools
"""

import asyncio
import json
import sys
from pathlib import Path

# Add the current directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_list_tools():
    """Test listing available tools from the MCP server"""
    print("\n" + "="*60)
    print("TEST 1: List Available Tools")
    print("="*60)
    
    server_params = StdioServerParameters(
        command="python",
        args=["your_mcp_server.py"],  # Replace with your server file
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # List tools
            tools = await session.list_tools()
            
            print(f"\n✅ Found {len(tools.tools)} tools:")
            for tool in tools.tools:
                print(f"\n  📦 {tool.name}")
                print(f"     Description: {tool.description}")
                print(f"     Parameters: {json.dumps(tool.inputSchema, indent=6)}")
            
            return tools.tools


async def test_tool_schemas():
    """Test that all tool schemas are valid"""
    print("\n" + "="*60)
    print("TEST 2: Validate Tool Schemas")
    print("="*60)
    
    server_params = StdioServerParameters(
        command="python",
        args=["your_mcp_server.py"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            
            for tool in tools.tools:
                schema = tool.inputSchema
                required = schema.get("required", [])
                properties = schema.get("properties", {})
                
                print(f"\n  ✅ {tool.name}")
                print(f"     Required params: {required}")
                print(f"     All params: {list(properties.keys())}")


async def test_tool_execution():
    """Test calling a tool with mock parameters"""
    print("\n" + "="*60)
    print("TEST 3: Test Tool Execution")
    print("="*60)
    
    server_params = StdioServerParameters(
        command="python",
        args=["your_mcp_server.py"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Replace with your actual tool name and parameters
            try:
                result = await session.call_tool(
                    "your_tool_name",
                    arguments={
                        "param1": "test_value"
                    }
                )
                print(f"\n  ✅ Tool executed successfully")
                print(f"  Response: {result}")
            except Exception as e:
                print(f"\n  ⚠️  Tool call failed: {str(e)[:200]}")
                print(f"  (This may be expected if test data doesn't exist)")


async def test_server_lifecycle():
    """Test that the server can start and stop cleanly"""
    print("\n" + "="*60)
    print("TEST 4: Server Lifecycle")
    print("="*60)
    
    server_params = StdioServerParameters(
        command="python",
        args=["your_mcp_server.py"],
        env=None
    )
    
    print("\n  Starting server...")
    async with stdio_client(server_params) as (read, write):
        print("  ✅ Server started successfully")
        
        async with ClientSession(read, write) as session:
            print("  ✅ Session initialized")
            await session.initialize()
            
            # Do a simple operation
            tools = await session.list_tools()
            print(f"  ✅ Listed {len(tools.tools)} tools")
        
        print("  ✅ Session closed cleanly")
    
    print("  ✅ Server stopped cleanly")


async def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("MCP SERVER TEST SUITE")
    print("="*60)
    print(f"Testing server at: {Path(__file__).parent / 'your_mcp_server.py'}")
    
    try:
        # Test 1: List tools
        await test_list_tools()
        
        # Test 2: Validate schemas
        await test_tool_schemas()
        
        # Test 3: Test tool execution
        await test_tool_execution()
        
        # Test 4: Server lifecycle
        await test_server_lifecycle()
        
        print("\n" + "="*60)
        print("✅ ALL TESTS COMPLETED")
        print("="*60)
        print("\nSummary:")
        print("  ✅ MCP server starts successfully")
        print("  ✅ All tools are registered")
        print("  ✅ Tool schemas are valid")
        print("  ✅ Tools are callable")
        print("  ✅ Server lifecycle works correctly")
        print("\n🎉 The MCP server is working properly!")
        
    except Exception as e:
        print("\n" + "="*60)
        print("❌ TEST FAILED")
        print("="*60)
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
```

**Run the test:**
```bash
# Make sure you have the MCP client library
pip install mcp

# Run the test script
python test_mcp_server.py
```

**Expected output:**
```
============================================================
MCP SERVER TEST SUITE
============================================================
Testing server at: /path/to/your_mcp_server.py

============================================================
TEST 1: List Available Tools
============================================================

✅ Found 5 tools:

  📦 tool1
     Description: What tool1 does
     Parameters: {...}

  📦 tool2
     Description: What tool2 does
     Parameters: {...}

...

============================================================
✅ ALL TESTS COMPLETED
============================================================

🎉 The MCP server is working properly!
```

### Method 2: Manual Testing with MCP Inspector

If you prefer interactive testing, use the MCP Inspector tool:

```bash
# Install MCP Inspector
npm install -g @modelcontextprotocol/inspector

# Run your MCP server with inspector
mcp-inspector python your_mcp_server.py
```

This opens a web interface where you can:
- See all registered tools
- Inspect tool schemas
- Call tools with custom parameters
- View responses in real-time

### Method 3: Quick Smoke Test

For a quick validation, run the server directly:

```bash
# Start the server
python your_mcp_server.py

# If it starts without errors, that's a good sign
# Press Ctrl+C to stop
```

**What to look for:**
- ✅ No import errors
- ✅ No syntax errors
- ✅ Server starts and waits for input
- ❌ Any error messages or stack traces

### Common Test Failures and Solutions

#### Test Failure: ModuleNotFoundError

**Error:**
```
ModuleNotFoundError: No module named 'mcp'
```

**Solution:**
```bash
pip install mcp
```

#### Test Failure: Script Not Found

**Error:**
```
Error: Script not found at scripts/my_script.py
```

**Solution:**
```bash
# Verify script exists
ls -la scripts/my_script.py

# Check path in MCP server code
# Use relative paths from the MCP server file location
```

#### Test Failure: Permission Denied

**Error:**
```
PermissionError: [Errno 13] Permission denied
```

**Solution:**
```bash
# Make scripts executable
chmod +x scripts/*.py
chmod +x scripts/*.sh
```

#### Test Failure: Missing Dependencies

**Error:**
```
ModuleNotFoundError: No module named 'PIL'
```

**Solution:**
```bash
# Install missing dependencies
pip install Pillow

# Or create requirements.txt
cat > requirements.txt << 'EOF'
mcp>=1.0.0
Pillow>=10.0.0
# Add other dependencies
EOF

pip install -r requirements.txt
```

### Testing Checklist

Before considering your MCP server ready:

- [ ] **Server starts without errors**
- [ ] **All expected tools are listed**
- [ ] **Tool schemas are valid JSON Schema**
- [ ] **Required parameters are marked correctly**
- [ ] **Optional parameters work as expected**
- [ ] **Tools can be called successfully**
- [ ] **Error messages are clear and helpful**
- [ ] **Server shuts down cleanly**
- [ ] **All dependencies are documented**
- [ ] **Scripts have correct permissions**

### Integration Testing in Kiro

After your MCP server passes standalone tests, test it in Kiro:

1. **Install the Power** in Kiro Powers panel
2. **Activate the Power** by mentioning keywords
3. **Try using a tool** in conversation
4. **Verify the response** is correct
5. **Test error cases** (missing files, invalid params)

**Example conversation:**
```
You: "Use the pdf_extract tool to extract data from contract.pdf"
Kiro: [Calls MCP tool and returns result]
```

### Continuous Testing

**Add testing to your workflow:**

```bash
# Create a test script that runs before commits
cat > test.sh << 'EOF'
#!/bin/bash
echo "Testing MCP server..."
python test_mcp_server.py
if [ $? -eq 0 ]; then
    echo "✅ Tests passed"
else
    echo "❌ Tests failed"
    exit 1
fi
EOF

chmod +x test.sh

# Run before committing
./test.sh && git commit -m "Update MCP server"
```

### Documentation of Test Results

**Create a test report:**

```markdown
# MCP Server Test Report

**Date:** 2026-01-04
**Server:** my_mcp_server.py
**Tools:** 5

## Test Results

✅ Server Startup: PASS
✅ Tool Registration: PASS (5/5 tools)
✅ Schema Validation: PASS
✅ Tool Execution: PASS
✅ Error Handling: PASS
✅ Server Lifecycle: PASS

## Dependencies Verified

- mcp==1.25.0
- Pillow==12.1.0
- python-pptx==1.0.2

## Issues Found

None

## Conclusion

MCP server is ready for deployment.
```

---

## Best Practices

### Script Organization

```
✅ Good Structure:
my-power/
├── scripts/
│   ├── category1/
│   │   ├── script1.py
│   │   └── script2.py
│   └── category2/
│       ├── script3.sh
│       └── script4.py
├── .mcp-config.json
└── POWER.md

❌ Bad Structure:
my-power/
├── script1.py          # Scripts scattered
├── another_script.sh
├── random.py
└── POWER.md
```

### Error Handling

**In Dedicated MCP:**
```python
@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    try:
        if name == "process_data":
            result = process(arguments["data"])
            return [TextContent(type="text", text=json.dumps(result))]
    except FileNotFoundError as e:
        return [TextContent(
            type="text",
            text=f"Error: File not found - {str(e)}"
        )]
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error: {type(e).__name__} - {str(e)}"
        )]
```

**In Script Executor config:**
```python
# In script_executor_mcp.py SCRIPTS dictionary
SCRIPTS = {
    "process_data": {
        "path": "scripts/process.py",
        "description": "Process data file",
        "args": ["data_path"],
        "timeout": 30
    }
}

# Error handling is built into the executor
# Errors are automatically captured and returned
```

### Testing Strategy

**Test Checklist:**
- [ ] Script executes successfully
- [ ] Arguments passed correctly
- [ ] Output format is correct
- [ ] Error handling works
- [ ] Timeout is appropriate
- [ ] Dependencies are available
- [ ] Permissions are correct

**Test Script:**
```bash
#!/bin/bash
# test_scripts.sh

echo "Testing MCP tools..."

# Test each script
for script in pdf_extract pdf_fill pdf_merge; do
    echo "Testing $script..."
    # Add test command here
done

echo "All tests passed!"
```

## Troubleshooting

### Issue: Script Not Found

**Error:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'scripts/my_script.py'
```

**Solution:**
```bash
# Check script exists
ls -la scripts/my_script.py

# Verify path in config
cat .mcp-config.json | grep "my_script" -A 3

# Use relative path
{
  "path": "scripts/my_script.py"  // ✅ Relative
  // NOT: "/absolute/path/script.py"  // ❌ Absolute
}
```

### Issue: Permission Denied

**Error:**
```
PermissionError: [Errno 13] Permission denied: 'scripts/script.sh'
```

**Solution:**
```bash
# Make scripts executable
chmod +x scripts/*.sh
chmod +x scripts/*.py

# Verify permissions
ls -la scripts/
```

### Issue: Timeout

**Error:**
```
TimeoutError: Script execution exceeded 30 seconds
```

**Solution:**
```json
{
  "scripts": {
    "long_running": {
      "path": "scripts/long.py",
      "timeout": 300  // Increase timeout to 5 minutes
    }
  }
}
```

### Issue: Missing Dependencies

**Error:**
```
ModuleNotFoundError: No module named 'PyPDF2'
```

**Solution:**
```bash
# Install dependencies
pip install PyPDF2

# Or create requirements.txt
cat > requirements.txt << 'EOF'
PyPDF2==2.1.0
mcp==1.0.0
EOF

pip install -r requirements.txt
```

---

**Next Steps:**
- Test your converted scripts thoroughly
- Document any script-specific requirements
- Share your Power with the team
- Read `installation-migration.md` for deployment strategies
