# Troubleshooting Guide

## Common Conversion Issues

### Issue 1: Power Not Activating

**Symptoms:**
- Mention keywords but Power doesn't load
- Power not appearing in available list
- No response when using expected triggers

**Diagnostic Steps:**

1. **Check Power installation**
   ```bash
   # Verify Power is installed
   # Open Powers panel in Kiro
   # Look for your Power in the list
   ```

2. **Verify frontmatter**
   ```bash
   # Check POWER.md frontmatter
   head -20 powers/my-power/POWER.md
   
   # Ensure keywords are present
   # keywords: ["keyword1", "keyword2"]
   ```

3. **Test keyword specificity**
   ```
   # Try exact keyword match
   "Use keyword1 to do something"
   
   # If still not working, keywords may be too generic
   ```

**Solutions:**

**Solution A: Fix Keywords**
```yaml
# Bad keywords (too generic)
keywords: ["test", "help", "debug"]

# Good keywords (specific)
keywords: ["pytest", "unit-testing", "python-test"]
```

**Solution B: Validate YAML Syntax**
```bash
# Check YAML is valid
python -c "
import yaml
with open('powers/my-power/POWER.md') as f:
    content = f.read()
    frontmatter = content.split('---')[1]
    yaml.safe_load(frontmatter)
print('✅ YAML is valid')
"
```

**Solution C: Reinstall Power**
```
1. Open Powers panel
2. Find your Power
3. Click "Uninstall"
4. Click "Add Custom Power"
5. Select "Local Directory"
6. Choose Power directory
7. Click "Add"
```

### Issue 2: Scripts Not Converting to MCP Tools

**Symptoms:**
- MCP tools not found
- "Tool not available" errors
- Script execution fails

**Diagnostic Steps:**

1. **Verify MCP configuration**
   ```bash
   # Check mcp.json exists
   ls -la powers/my-power/mcp.json
   
   # Validate JSON syntax
   cat powers/my-power/mcp.json | python -m json.tool
   ```

2. **Check script paths**
   ```bash
   # Verify scripts exist
   ls -la powers/my-power/scripts/
   
   # Check paths in config
   cat powers/my-power/.mcp-config.json
   ```

3. **Test MCP server**
   ```bash
   # For Script Executor Pattern
   cd powers/my-power
   python script_executor_mcp.py
   
   # For custom MCP
   python powers/my-power/my_mcp_server.py
   ```

**Solutions:**

**Solution A: Fix Script Paths**
```json
// Wrong (absolute path)
{
  "scripts": {
    "my_script": {
      "path": "/Users/john/scripts/script.py"  // ❌
    }
  }
}

// Correct (relative path)
{
  "scripts": {
    "my_script": {
      "path": "scripts/script.py"  // ✅
    }
  }
}
```

**Solution B: Fix Permissions**
```bash
# Make scripts executable
chmod +x powers/my-power/scripts/*.sh
chmod +x powers/my-power/scripts/*.py

# Verify
ls -la powers/my-power/scripts/
```

**Solution C: Install Dependencies**
```bash
# Check script requirements
head -20 powers/my-power/scripts/my_script.py

# Install missing packages
pip install required-package

# Or use requirements.txt
pip install -r powers/my-power/requirements.txt
```

### Issue 3: Frontmatter Validation Errors

**Symptoms:**
- "Invalid frontmatter" error
- Power won't install
- YAML parsing errors

**Diagnostic Steps:**

1. **Check frontmatter structure**
   ```yaml
   # Must start with --- on line 1
   ---
   name: "power-name"
   displayName: "Display Name"
   description: "Description"
   keywords: ["key1", "key2"]
   ---
   ```

2. **Validate required fields**
   ```yaml
   # Required fields:
   name: "..."        # ✅ Required
   displayName: "..." # ✅ Required
   description: "..." # ✅ Required
   
   # Optional fields:
   keywords: [...]    # Recommended
   author: "..."      # Optional
   ```

3. **Check for invalid fields**
   ```yaml
   # These fields DO NOT exist:
   version: "1.0.0"      # ❌ Invalid
   tags: ["tag1"]        # ❌ Invalid
   repository: "..."     # ❌ Invalid
   license: "MIT"        # ❌ Invalid
   ```

**Solutions:**

**Solution A: Fix Structure**
```yaml
# Wrong
name: power-name  # ❌ Missing quotes
keywords: key1, key2  # ❌ Not an array

# Correct
name: "power-name"  # ✅ Quoted
keywords: ["key1", "key2"]  # ✅ Array
```

**Solution B: Remove Invalid Fields**
```yaml
# Before
---
name: "my-power"
version: "1.0.0"  # ❌ Remove this
tags: ["tag1"]    # ❌ Remove this
---

# After
---
name: "my-power"
displayName: "My Power"
description: "What it does"
keywords: ["keyword1"]
---
```

**Solution C: Validate with Tool**
```bash
# Use Python to validate
python -c "
import yaml
import sys

with open('powers/my-power/POWER.md') as f:
    content = f.read()
    parts = content.split('---')
    if len(parts) < 3:
        print('❌ Invalid frontmatter structure')
        sys.exit(1)
    
    try:
        meta = yaml.safe_load(parts[1])
        required = ['name', 'displayName', 'description']
        for field in required:
            if field not in meta:
                print(f'❌ Missing required field: {field}')
                sys.exit(1)
        print('✅ Frontmatter is valid')
    except yaml.YAMLError as e:
        print(f'❌ YAML error: {e}')
        sys.exit(1)
"
```

### Issue 4: MCP Server Connection Failures

**Symptoms:**
- "MCP server not responding"
- "Connection refused"
- Tools timeout

**Diagnostic Steps:**

1. **Check MCP server status**
   ```bash
   # Test server manually
   python -m mcp_script_runner.server
   # Should start without errors
   ```

2. **Verify configuration**
   ```json
   // Check mcp.json
   {
     "mcpServers": {
       "my-server": {
         "command": "python",  // Correct command?
         "args": ["server.py"],  // Correct args?
         "env": {}  // Required env vars?
       }
     }
   }
   ```

3. **Check logs**
   ```bash
   # Look for error messages in Kiro logs
   # (Location varies by OS)
   ```

**Solutions:**

**Solution A: Fix Command Path**
```json
// Wrong
{
  "command": "python3",  // May not be in PATH
  "args": ["server.py"]
}

// Correct
{
  "command": "python",  // Use standard name
  "args": ["-m", "mcp_script_runner.server"]
}
```

**Solution B: Add Environment Variables**
```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["server.py"],
      "env": {
        "PYTHONPATH": ".",
        "API_KEY": "API_KEY_ENV_VAR"
      }
    }
  }
}
```

**Solution C: Use Absolute Path**
```json
{
  "mcpServers": {
    "my-server": {
      "command": "/usr/bin/python3",
      "args": ["/full/path/to/server.py"]
    }
  }
}
```

### Issue 5: Performance Degradation

**Symptoms:**
- Kiro slower after installing Powers
- High memory usage
- Delayed responses

**Diagnostic Steps:**

1. **Check number of installed Powers**
   ```
   # Open Powers panel
   # Count installed Powers
   # More than 10-15 may cause issues
   ```

2. **Identify large Powers**
   ```bash
   # Check POWER.md sizes
   find powers/ -name "POWER.md" -exec wc -l {} \;
   
   # Powers > 500 lines should use steering files
   ```

3. **Review keyword specificity**
   ```yaml
   # Generic keywords cause false activations
   keywords: ["test", "debug"]  # ❌ Too broad
   
   # Specific keywords reduce false activations
   keywords: ["pytest", "python-unittest"]  # ✅ Specific
   ```

**Solutions:**

**Solution A: Uninstall Unused Powers**
```
1. Review installed Powers
2. Identify rarely used ones
3. Uninstall unnecessary Powers
4. Keep only essential Powers
```

**Solution B: Split Large Powers**
```bash
# If POWER.md > 500 lines
# Move content to steering files

mkdir powers/my-power/steering
# Move sections to separate files
# Update POWER.md to reference them
```

**Solution C: Refine Keywords**
```yaml
# Before (causes false activations)
keywords: ["api", "test", "data"]

# After (more specific)
keywords: ["rest-api", "integration-test", "json-data"]
```

### Issue 6: Conversion Tool Errors

**Symptoms:**
- Automated conversion fails
- Generated files incomplete
- Syntax errors in output

**Diagnostic Steps:**

1. **Validate input Skill**
   ```bash
   # Check SKILL.md format
   head -30 ~/.claude/skills/my-skill/SKILL.md
   
   # Ensure frontmatter is valid
   # Ensure content is readable
   ```

2. **Check tool version**
   ```bash
   # Verify conversion tool is up to date
   python skill_to_power_converter.py --version
   
   # Update if needed
   git pull
   ```

3. **Run with debug mode**
   ```bash
   # Enable verbose output
   python skill_to_power_converter.py \
       --debug \
       input.md \
       output/
   ```

**Solutions:**

**Solution A: Manual Conversion**
```bash
# If automated tool fails
# Convert manually using templates

# 1. Copy template
cp templates/POWER.md.template powers/my-power/POWER.md

# 2. Fill in manually
# Edit frontmatter
# Copy content from SKILL.md
# Adjust formatting
```

**Solution B: Fix Input Format**
```yaml
# Ensure SKILL.md has valid frontmatter
---
name: my-skill
description: What it does
---

# Content starts here
```

**Solution C: Report Issue**
```bash
# Document the error
# Create minimal reproduction
# Report to tool maintainer
```

## Script-Specific Issues

### Python Script Issues

**Issue: Module Not Found**
```bash
# Error
ModuleNotFoundError: No module named 'PyPDF2'

# Solution
pip install PyPDF2

# Or install all requirements
pip install -r requirements.txt
```

**Issue: Python Version**
```bash
# Error
SyntaxError: invalid syntax (Python 2.7)

# Solution
# Use Python 3.8+
python3 --version
# Update shebang in scripts
#!/usr/bin/env python3
```

### Shell Script Issues

**Issue: Command Not Found**
```bash
# Error
bash: jq: command not found

# Solution (macOS)
brew install jq

# Solution (Linux)
apt-get install jq
```

**Issue: Line Endings**
```bash
# Error
/bin/bash^M: bad interpreter

# Solution
# Convert line endings
dos2unix scripts/*.sh

# Or use sed
sed -i 's/\r$//' scripts/*.sh
```

## MCP-Specific Issues

### Tool Not Found

**Error:**
```
Error: Tool 'my_tool' not found
```

**Solution:**
```python
# Check tool is registered
@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="my_tool",  # Must match exactly
            description="...",
            inputSchema={...}
        )
    ]
```

### Invalid Tool Schema

**Error:**
```
Error: Invalid tool schema
```

**Solution:**
```python
# Ensure schema is valid JSON Schema
Tool(
    name="my_tool",
    description="What it does",
    inputSchema={
        "type": "object",
        "properties": {
            "param1": {
                "type": "string",  # Valid JSON Schema type
                "description": "Parameter description"
            }
        },
        "required": ["param1"]  # List required params
    }
)
```

## Getting Help

### Self-Help Resources

1. **Check Documentation**
   - Read POWER.md thoroughly
   - Review steering files
   - Check examples

2. **Search Issues**
   - GitHub issues
   - Community forum
   - Stack Overflow

3. **Test Incrementally**
   - Test each component
   - Isolate the problem
   - Verify assumptions

### Community Support

1. **Kiro Community Forum**
   - Post detailed questions
   - Include error messages
   - Share minimal reproduction

2. **GitHub Issues**
   - Report bugs
   - Request features
   - Contribute fixes

3. **Discord/Slack**
   - Real-time help
   - Quick questions
   - Community discussion

### Creating Good Bug Reports

**Include:**
- Kiro version
- Power name and version
- Steps to reproduce
- Expected behavior
- Actual behavior
- Error messages
- Relevant configuration

**Template:**
```markdown
## Bug Report

**Environment:**
- Kiro Version: 1.0.0
- OS: macOS 14.0
- Power: my-power v1.0.0

**Steps to Reproduce:**
1. Install Power
2. Mention keyword "test"
3. Observe error

**Expected:**
Power should activate

**Actual:**
Error: "Tool not found"

**Error Message:**
```
[Full error message here]
```

**Configuration:**
```json
{
  "mcpServers": {
    ...
  }
}
```
```

---

**Still having issues?**
- Review the main POWER.md
- Check other steering files
- Ask in community forum
- Report bugs on GitHub
