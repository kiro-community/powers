#!/usr/bin/env python3
"""
MCP Server for PowerPoint Presentation Tools
Executes Python and JavaScript scripts for PPTX manipulation
"""

import asyncio
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from mcp.server import Server
from mcp.types import Tool, TextContent


# Script definitions
SCRIPTS = {
    "html2pptx": {
        "path": "scripts/html2pptx-cli.js",
        "interpreter": "node",
        "description": "Convert HTML slides to PowerPoint presentation",
        "parameters": {
            "type": "object",
            "properties": {
                "html_files": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Array of HTML file paths for each slide"
                },
                "output_file": {
                    "type": "string",
                    "description": "Output .pptx file path"
                },
                "config": {
                    "type": "object",
                    "description": "Optional configuration (charts, tables, etc.)",
                    "properties": {}
                }
            },
            "required": ["html_files", "output_file"]
        }
    },
    "inventory": {
        "path": "scripts/inventory.py",
        "interpreter": "python",
        "description": "Extract all text shapes and properties from a presentation",
        "parameters": {
            "type": "object",
            "properties": {
                "input_file": {
                    "type": "string",
                    "description": "Input .pptx file path"
                },
                "output_file": {
                    "type": "string",
                    "description": "Output JSON file path for inventory"
                }
            },
            "required": ["input_file", "output_file"]
        }
    },
    "rearrange": {
        "path": "scripts/rearrange.py",
        "interpreter": "python",
        "description": "Duplicate, reorder, and delete slides in a presentation",
        "parameters": {
            "type": "object",
            "properties": {
                "input_file": {
                    "type": "string",
                    "description": "Input .pptx file path"
                },
                "output_file": {
                    "type": "string",
                    "description": "Output .pptx file path"
                },
                "slide_indices": {
                    "type": "string",
                    "description": "Comma-separated slide indices (0-based, can repeat)"
                }
            },
            "required": ["input_file", "output_file", "slide_indices"]
        }
    },
    "replace": {
        "path": "scripts/replace.py",
        "interpreter": "python",
        "description": "Replace text content in presentation while preserving formatting",
        "parameters": {
            "type": "object",
            "properties": {
                "input_file": {
                    "type": "string",
                    "description": "Input .pptx file path"
                },
                "replacement_json": {
                    "type": "string",
                    "description": "JSON file with replacement text and formatting"
                },
                "output_file": {
                    "type": "string",
                    "description": "Output .pptx file path"
                }
            },
            "required": ["input_file", "replacement_json", "output_file"]
        }
    },
    "thumbnail": {
        "path": "scripts/thumbnail.py",
        "interpreter": "python",
        "description": "Generate visual thumbnail grids of presentation slides",
        "parameters": {
            "type": "object",
            "properties": {
                "input_file": {
                    "type": "string",
                    "description": "Input .pptx file path"
                },
                "output_prefix": {
                    "type": "string",
                    "description": "Output file prefix (optional, default: 'thumbnails')"
                },
                "columns": {
                    "type": "integer",
                    "description": "Number of columns (3-6, default: 5)"
                }
            },
            "required": ["input_file"]
        }
    }
}


app = Server("pptx-tools")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available PPTX manipulation tools."""
    tools = []
    for name, config in SCRIPTS.items():
        tools.append(
            Tool(
                name=name,
                description=config["description"],
                inputSchema=config["parameters"]
            )
        )
    return tools


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Execute a PPTX manipulation script."""
    if name not in SCRIPTS:
        return [TextContent(
            type="text",
            text=f"Error: Unknown tool '{name}'"
        )]
    
    script_config = SCRIPTS[name]
    script_path = Path(__file__).parent / script_config["path"]
    
    if not script_path.exists():
        return [TextContent(
            type="text",
            text=f"Error: Script not found at {script_path}"
        )]
    
    # Build command based on script type
    interpreter = script_config["interpreter"]
    
    try:
        if name == "html2pptx":
            # Special handling for html2pptx - needs config file
            config_data = {
                "html_files": arguments.get("html_files", []),
                "output_file": arguments.get("output_file"),
                "config": arguments.get("config", {})
            }
            config_path = Path(__file__).parent / "temp_config.json"
            config_path.write_text(json.dumps(config_data, indent=2))
            
            cmd = [interpreter, str(script_path), str(config_path)]
        
        elif name == "inventory":
            cmd = [
                interpreter,
                str(script_path),
                arguments["input_file"],
                arguments["output_file"]
            ]
        
        elif name == "rearrange":
            cmd = [
                interpreter,
                str(script_path),
                arguments["input_file"],
                arguments["output_file"],
                arguments["slide_indices"]
            ]
        
        elif name == "replace":
            cmd = [
                interpreter,
                str(script_path),
                arguments["input_file"],
                arguments["replacement_json"],
                arguments["output_file"]
            ]
        
        elif name == "thumbnail":
            cmd = [interpreter, str(script_path), arguments["input_file"]]
            if "output_prefix" in arguments:
                cmd.append(arguments["output_prefix"])
            if "columns" in arguments:
                cmd.extend(["--cols", str(arguments["columns"])])
        
        else:
            return [TextContent(
                type="text",
                text=f"Error: No command builder for tool '{name}'"
            )]
        
        # Execute the script
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        # Clean up temp config if created
        if name == "html2pptx":
            config_path.unlink(missing_ok=True)
        
        # Format output
        output = []
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")
        if result.returncode != 0:
            output.append(f"\nExit code: {result.returncode}")
        
        return [TextContent(
            type="text",
            text="\n\n".join(output) if output else "Script executed successfully (no output)"
        )]
    
    except subprocess.TimeoutExpired:
        return [TextContent(
            type="text",
            text=f"Error: Script execution timed out after 300 seconds"
        )]
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error executing script: {str(e)}"
        )]


async def main():
    """Run the MCP server."""
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
