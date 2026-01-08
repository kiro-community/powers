---
name: "convert-skills-to-power"
displayName: "Convert Skills to Power"
description: "Convert Claude Agent Skills to Kiro Powers with automated tools, best practices, and step-by-step guidance for script conversion and MCP integration."
keywords: ["claude", "skills", "conversion", "migration", "mcp", "power", "transform"]
author: "Kiro Community"
---

# Convert Skills to Power

## Overview

This power helps you convert Claude Agent Skills to Kiro Powers efficiently and correctly. It provides comprehensive guidance, automated conversion tools, and best practices based on detailed research comparing the two systems.

**Key capabilities:**
- Automated conversion of SKILL.md to POWER.md with proper frontmatter transformation
- Script-to-MCP conversion strategies (the correct way to handle Skills scripts)
- Installation and distribution mechanism guidance
- Decision trees for choosing the right conversion approach
- Complete code examples and templates

**What you'll learn:**
- Why Skills scripts should become MCP tools (not Hooks)
- How to create your own Script Executor MCP server for reliable conversions
- When to create dedicated MCP servers vs using script executor pattern
- Installation flow differences and migration strategies

## Available Steering Files

This power includes comprehensive guides for different aspects of the conversion process:

- **quick-start** - 5-minute decision flow and conversion checklist
- **script-conversion** - Detailed guide for converting Skills scripts to MCP tools
- **installation-migration** - Installation mechanism comparison and migration strategies
- **troubleshooting** - Common conversion issues and solutions

## Onboarding

### Prerequisites

**Required knowledge:**
- Basic understanding of Claude Skills structure
- Familiarity with Kiro Powers concept
- Command line basics

**Required tools:**
- Python 3.8+ (for conversion scripts)
- Git (for version control)
- Text editor or IDE

**Optional but recommended:**
- Node.js 16+ (if working with MCP servers)
- Docker (optional, for containerized deployments)

### Installation

No installation required! This is a Knowledge Base Power that provides documentation and guidance.

**To get started:**
1. Activate this power by mentioning "convert skills" or "skill migration"
2. Read the appropriate steering file based on your needs
3. Follow the step-by-step instructions

### Quick Setup

**Python MCP SDK:**
```bash
# Install MCP SDK
pip install mcp

# Verify installation
python -c "from mcp.server import Server; print('✅ MCP SDK installed')"
```

**Optional tools for script execution:**
```bash
# If you need subprocess management
pip install asyncio

# For JSON schema validation
pip install jsonschema
```

## Core Concepts

### Understanding the Conversion

**Claude Skills** and **Kiro Powers** are similar but have key differences:

| Aspect | Claude Skills | Kiro Powers |
|--------|--------------|-------------|
| **Main file** | SKILL.md | POWER.md |
| **Installation** | Manual file creation | IDE one-click / CLI |
| **Activation** | Description matching | Keyword triggering |
| **Scripts** | Zero-context execution | MCP tools (recommended) |
| **Updates** | Manual replacement | Version management |
| **Market** | No official market | Official + community |

### Critical Decision: Scripts Conversion

**⚠️ IMPORTANT:** Skills scripts should be converted to **MCP tools**, NOT Hooks.

**Why?**
- Skills scripts are **on-demand** (AI decides when to run)
- Hooks are **event-triggered** (automatic on file save, etc.)
- MCP tools preserve zero-context execution
- MCP tools support on-demand invocation

**Conversion options:**
1. **1-3 scripts** → Create dedicated MCP server (2-4 hours)
2. **4-10 scripts** → Use Script Executor Pattern (3-5 hours, recommended)
3. **10+ scripts** → Modular MCP server with dynamic script loading (1-2 days)

**Note:** We recommend creating your own MCP server using the Script Executor Pattern for better control, reliability, and maintenance. This approach is self-contained and doesn't rely on external dependencies.

## Common Workflows

### Workflow 1: Simple Skill Conversion (Pure Documentation)

**Goal:** Convert a Skill that only contains documentation/guidance (no scripts)

**Time:** 1-2 hours

**Steps:**

1. **Analyze the Skill**
   ```bash
   # Check Skill structure
   ls -la ~/.claude/skills/my-skill/
   
   # Verify it's documentation-only (no scripts)
   find ~/.claude/skills/my-skill/ -name "*.py" -o -name "*.sh"
   ```

2. **Create Power directory**
   ```bash
   mkdir -p ./powers/my-power
   cd ./powers/my-power
   ```

3. **Convert SKILL.md to POWER.md**
   
   **Transform frontmatter:**
   ```yaml
   # Original SKILL.md
   ---
   name: pr-reviewer
   description: Reviews pull requests for code quality
   ---
   
   # New POWER.md
   ---
   name: "pr-reviewer"
   displayName: "PR Reviewer"
   description: "Reviews pull requests for code quality and team standards"
   keywords: ["pr", "pull request", "review", "code review"]
   author: "Your Name"
   ---
   ```

4. **Move documentation**
   ```bash
   # If Skill has docs/ directory
   mkdir steering
   cp -r ~/.claude/skills/my-skill/docs/* ./steering/
   ```

5. **Test the Power**
   - Open Kiro Powers panel
   - Add from local directory
   - Test keyword activation

**Example:**

See `steering/quick-start.md` for a complete example with code.

### Workflow 2: Skill with Scripts Conversion

**Goal:** Convert a Skill that includes executable scripts

**Time:** 3-5 hours (using Script Executor Pattern) or 2-4 hours (dedicated MCP for 1-3 scripts)

**⚠️ IMPORTANT:** Kiro Powers cannot contain script files. You must install the MCP server separately.

**Steps:**

1. **Analyze scripts**
   ```bash
   # List all scripts
   find ~/.claude/skills/my-skill/scripts/ -type f
   
   # Count scripts
   find ~/.claude/skills/my-skill/scripts/ -type f | wc -l
   ```

2. **Choose conversion strategy**
   
   **Decision tree:**
   ```
   Number of scripts?
   ├─ 1-3 scripts → Dedicated MCP server
   ├─ 4-10 scripts → Script Executor Pattern (recommended)
   └─ 10+ scripts → Modular MCP server
   ```

3. **Create MCP Server (Separate from Power)**
   
   Install MCP server to a separate location (e.g., `~/my-mcp-servers/my-server/`)
   
   See `steering/script-conversion.md` for complete code examples and templates.
   
   **Key benefits:**
   - ✅ No external dependencies
   - ✅ Full control over execution
   - ✅ Easy to customize
   - ✅ Complies with Kiro Powers restrictions

4. **Create Power Directory (Only Documentation)**
   
   Power contains ONLY:
   - `POWER.md` - Documentation with installation instructions
   - `mcp.json` - Configuration pointing to installed MCP server
   - `steering/` - Optional workflow guides

5. **Update POWER.md with Installation Instructions**
   
   Include clear instructions for users to install the MCP server:
   ```markdown
   ## Installation
   
   ### Step 1: Install MCP Server
   ```bash
   git clone https://github.com/user/my-server.git ~/my-mcp-servers/my-server
   cd ~/my-mcp-servers/my-server
   pip install -r requirements.txt
   ```
   
   ### Step 2: Install the Power
   Install this Power through Kiro Powers panel.
   ```

6. **Create mcp.json with Absolute Path**
   ```json
   {
     "mcpServers": {
       "my-scripts": {
         "command": "python",
         "args": ["~/my-mcp-servers/my-server/script_executor_mcp.py"]
       }
     }
   }
   ```

7. **Test the MCP Server** ⚠️ **CRITICAL STEP**
   
   Before deploying, test your MCP server to ensure it works:
   
   ```bash
   # Create a test script (see steering/script-conversion.md for full template)
   python test_mcp_server.py
   ```
   
   **What to verify:**
   - ✅ Server starts without errors
   - ✅ All tools are registered
   - ✅ Tool schemas are valid
   - ✅ Tools can be called successfully
   - ✅ Dependencies are installed
   
   **If tests fail:**
   - Check for missing dependencies (`pip install <package>`)
   - Verify script paths are correct
   - Ensure scripts have execute permissions
   - Review error messages carefully
   
   See `steering/script-conversion.md` → "Testing Your MCP Server" section for detailed testing guide.

**Complete example:**

See `steering/script-conversion.md` for full code examples and templates.

### Workflow 3: Batch Conversion

**Goal:** Convert multiple Skills at once

**Time:** Varies based on number and complexity

**Steps:**

1. **Prepare conversion environment**
   ```bash
   mkdir -p ./converted-powers
   ```

2. **Use automated conversion tool**
   ```bash
   # Download conversion script
   # (See documentation for actual tool location)
   
   # Run batch conversion
   python batch_convert_skills.sh ~/.claude/skills ./converted-powers
   ```

3. **Review each converted Power**
   ```bash
   # Check conversion results
   for power in ./converted-powers/*; do
     echo "=== $(basename $power) ==="
     cat "$power/POWER.md" | head -20
     echo ""
   done
   ```

4. **Test each Power individually**
   - Install via Kiro Powers panel
   - Test keyword activation
   - Verify functionality

5. **Iterate and fix issues**
   - Adjust keywords if activation is incorrect
   - Fix any conversion errors
   - Update documentation as needed

## Best Practices

### Conversion Strategy

1. **Start Simple**
   - Begin with 2-3 simple documentation-only Skills
   - Build confidence with the process
   - Learn the conversion patterns

2. **Scripts → MCP Tools**
   - Always convert scripts to MCP tools (not Hooks)
   - Use Script Executor Pattern for reliable deployment
   - Create dedicated MCP for complex logic

3. **Keywords Matter**
   - Extract specific keywords from Skill descriptions
   - Avoid overly broad terms ("test", "debug", "help")
   - Test keyword activation thoroughly

4. **Preserve Zero-Context**
   - MCP tools maintain zero-context execution
   - Don't inline scripts into POWER.md
   - Keep tool definitions separate

5. **Version Control**
   - Keep original Skills as backup
   - Use Git for converted Powers
   - Tag versions for easy rollback

### Installation Migration

1. **Gradual Migration**
   - Don't convert all Skills at once
   - Test each Power thoroughly
   - Gather feedback before proceeding

2. **Team Communication**
   - Inform team about the migration
   - Provide training on Powers
   - Share conversion experiences

3. **Documentation**
   - Document conversion decisions
   - Keep notes on issues encountered
   - Share lessons learned

### Quality Assurance

1. **Test MCP Server First** ⚠️ **CRITICAL**
   - Create and run test script before deployment
   - Verify all tools are registered correctly
   - Test tool execution with sample data
   - Check for missing dependencies
   - Validate error handling
   - See `steering/script-conversion.md` for testing guide

2. **Test Thoroughly**
   - Functional testing (does it work?)
   - Performance testing (context usage)
   - Integration testing (with other Powers)

3. **Validate Metadata**
   - Check frontmatter syntax
   - Verify keywords trigger correctly
   - Ensure descriptions are clear

4. **Review Documentation**
   - Update examples to Kiro context
   - Fix broken links
   - Clarify Power-specific instructions

## Troubleshooting

### Issue: Power Not Activating

**Symptoms:**
- Mention keywords but Power doesn't load
- Power not appearing in list

**Causes:**
- Keywords too generic or incorrect
- Frontmatter syntax error
- Power not installed correctly

**Solutions:**

1. **Check keywords**
   ```bash
   # View Power frontmatter
   head -20 powers/my-power/POWER.md
   
   # Verify keywords are specific
   # Bad: ["test", "help"]
   # Good: ["pytest", "unit-testing"]
   ```

2. **Validate YAML syntax**
   ```bash
   # Use Python to check YAML
   python -c "import yaml; yaml.safe_load(open('powers/my-power/POWER.md').read().split('---')[1])"
   ```

3. **Reinstall Power**
   - Remove from Powers panel
   - Re-add from local directory
   - Test activation again

### Issue: Scripts Not Working as MCP Tools

**Symptoms:**
- MCP tools not found
- Script execution fails
- Timeout errors

**Causes:**
- MCP server not configured correctly
- Script paths incorrect
- Dependencies missing

**Solutions:**

1. **Verify MCP configuration**
   ```bash
   # Check mcp.json syntax
   cat powers/my-power/mcp.json | python -m json.tool
   
   # Test MCP server
   cd powers/my-power
   python script_executor_mcp.py
   ```

2. **Check script paths**
   ```json
   // Ensure paths are relative
   {
     "scripts": {
       "my_script": {
         "path": "scripts/my_script.py",  // ✅ Relative
         // NOT: "/absolute/path/script.py"  // ❌ Absolute
       }
     }
   }
   ```

3. **Install dependencies**
   ```bash
   # Check script requirements
   head -20 scripts/my_script.py
   
   # Install missing packages
   pip install required-package
   ```

### Issue: Conversion Tool Errors

**Symptoms:**
- Conversion script fails
- Generated files incomplete
- Syntax errors in output

**Causes:**
- Invalid SKILL.md format
- Unsupported Skill features
- Tool bugs

**Solutions:**

1. **Validate Skill format**
   ```bash
   # Check SKILL.md structure
   head -30 ~/.claude/skills/my-skill/SKILL.md
   
   # Ensure frontmatter is valid
   ```

2. **Manual conversion**
   - If automated tool fails, convert manually
   - Follow templates in steering files
   - Copy and adapt from examples

3. **Report issues**
   - Document the error
   - Share Skill structure (sanitized)
   - Help improve conversion tools

### Issue: Performance Degradation

**Symptoms:**
- Kiro slower after installing Powers
- High context usage
- Delayed responses

**Causes:**
- Too many Powers installed
- Powers with broad keywords
- Large POWER.md files

**Solutions:**

1. **Audit installed Powers**
   ```bash
   # List all Powers
   # (Use Kiro Powers panel)
   
   # Identify unused Powers
   # Uninstall what you don't need
   ```

2. **Refine keywords**
   - Make keywords more specific
   - Reduce false activations
   - Test keyword precision

3. **Split large Powers**
   - If POWER.md > 500 lines, consider splitting
   - Move content to steering files
   - Use progressive disclosure

## Configuration

**No additional configuration required** - this is a Knowledge Base Power.

**To use the conversion tools:**
- Follow installation steps in Onboarding section
- Configure paths in conversion scripts
- Set up your own MCP server using provided templates

## Additional Resources

### Documentation
- [Claude Skills Official Docs](https://code.claude.com/docs/en/skills)
- [Kiro Powers Documentation](https://kiro.dev/docs/powers/)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)

### Tools
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [MCP Servers Directory](https://mcpservers.org/)

### Community
- [Kiro Community Forum](https://community.kiro.dev/)
- [MCP Servers Directory](https://mcpservers.org/)
- [Powers Marketplace](https://kiro.dev/powers/)

---

**Knowledge Base Power** - No MCP server required
**Documentation Source:** Comprehensive research comparing Claude Skills and Kiro Powers
**Last Updated:** 2026-01-04
