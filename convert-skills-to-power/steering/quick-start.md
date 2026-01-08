# Quick Start Guide: Convert Skills to Power

## 5-Minute Decision Flow

```
Your Skill contains what?
    │
    ├─ Only documentation/guidance ────────────────┐
    │                                               │
    ├─ Scripts (1-3 files) ────────────────────────┤
    │                                               │
    ├─ Scripts (4-10 files) ───────────────────────┤
    │                                               │
    ├─ Scripts (10+ files) ────────────────────────┤
    │                                               │
    └─ Uses allowed-tools ─────────────────────────┘
                                                    │
                                                    ▼
┌────────────────────────────────────────────────────────┐
│  Conversion Approach                                   │
├────────────────────────────────────────────────────────┤
│  ✅ Simple Conversion (1-2 hours)                      │
│     - Rename SKILL.md → POWER.md                      │
│     - Add keywords field                              │
│     - Move docs/ to steering/                         │
│                                                        │
│  🔧 Dedicated MCP Server (2-4 hours)                  │
│     - Create custom MCP server                        │
│     - Migrate script logic to MCP tools               │
│     - Add mcpServers to frontmatter                   │
│                                                        │
│  ⚡ Script Executor Pattern (3-5 hours)               │
│     - Create reusable script executor MCP             │
│     - Configure SCRIPTS dictionary                    │
│     - Full control, zero external dependencies        │
│                                                        │
│  🎨 Modular MCP Server (1-2 days)                     │
│     - Organize scripts by category                    │
│     - Create modular MCP architecture                 │
│     - Best for 10+ scripts                            │
│                                                        │
│  🔐 Create MCP Server (4-8 hours)                     │
│     - Analyze tool requirements                       │
│     - Develop MCP server                              │
│     - Implement permissions                           │
└────────────────────────────────────────────────────────┘
```

## Conversion Checklist

### Phase 0: Understand Installation Differences (5 min)

**Claude Skills Installation:**
- [ ] Manual file creation
- [ ] Requires restart
- [ ] No version management

**Kiro Powers Installation:**
- [ ] IDE one-click or CLI command
- [ ] Immediate effect, no restart
- [ ] Automatic version management

**Key Difference:**
```
Claude Skills: Create files → Restart → Use (5-10 min)
Kiro Powers:   Click install → Use immediately (30 sec)
```

### Phase 1: Evaluate (15 min)

- [ ] List all your Skills
- [ ] Identify each Skill type:
  - [ ] Pure documentation
  - [ ] Contains scripts
  - [ ] Uses allowed-tools
  - [ ] External API integration
- [ ] Count scripts in each Skill
- [ ] Prioritize conversion order

### Phase 2: Prepare (30 min)

- [ ] Install MCP SDK
  ```bash
  pip install mcp
  ```
- [ ] Create output directory
  ```bash
  mkdir -p ./converted-powers
  ```
- [ ] Backup original Skills
  ```bash
  cp -r ~/.claude/skills ~/.claude/skills.backup
  ```

### Phase 3: Convert (Varies by type)

#### For Pure Documentation Skills (1-2 hours each)

- [ ] Copy SKILL.md to POWER.md
- [ ] Transform frontmatter:
  ```yaml
  # Add
  displayName: "Friendly Name"
  keywords: [keyword1, keyword2]
  
  # Remove (if present)
  model: ...
  allowed-tools: ...
  ```
- [ ] Move documentation:
  ```bash
  mv docs/ steering/
  ```
- [ ] Test activation in Kiro

#### For Skills with Scripts (3-5 hours each)

**Using Script Executor Pattern (Recommended for 4+ scripts):**

- [ ] Create script_executor_mcp.py
- [ ] Configure SCRIPTS dictionary:
  ```python
  SCRIPTS = {
      "script_name": {
          "path": "scripts/script.py",
          "description": "What it does",
          "args": ["arg1"],
          "timeout": 30
      }
  }
  ```
- [ ] Copy scripts to Power directory
- [ ] Create mcp.json configuration
- [ ] Add MCP config to POWER.md:
  ```yaml
  mcpServers:
    - my-scripts
  ```
- [ ] Test script execution

**Using Dedicated MCP (For 1-3 scripts):**

- [ ] Create MCP server file
- [ ] Migrate script logic to MCP tools
- [ ] Define tool schemas
- [ ] Implement tool handlers
- [ ] Test MCP server
- [ ] Update POWER.md

### Phase 4: Test (30 min per Power)

- [ ] Functional testing
  - [ ] Keywords trigger correctly
  - [ ] Tools work as expected
  - [ ] Documentation links valid
- [ ] Performance testing
  - [ ] Context loading time
  - [ ] Dynamic loading/unloading
- [ ] Integration testing
  - [ ] Compatible with other Powers
  - [ ] Works in different projects

### Phase 5: Deploy (15 min per Power)

- [ ] Commit to version control
  ```bash
  git add converted-powers/
  git commit -m "Convert Skills to Powers"
  ```
- [ ] Install in Kiro
  - [ ] Via IDE import
  - [ ] Or copy to Powers directory
- [ ] Verify installation
- [ ] Update team documentation

## Quick Examples

### Example 1: Simple PR Review Skill (5 min)

**Original Skill:**
```yaml
---
name: pr-reviewer
description: Reviews pull requests for code quality
---
# PR Review Skill
Check code style, tests, and security.
```

**Conversion:**
```bash
# 1. Create Power directory
mkdir -p converted-powers/pr-reviewer

# 2. Convert frontmatter
cat > converted-powers/pr-reviewer/POWER.md << 'EOF'
---
name: "pr-reviewer"
displayName: "PR Reviewer"
description: "Reviews pull requests for code quality"
keywords: ["pr", "pull request", "review", "code review"]
author: "Your Name"
---
# PR Review Power
Check code style, tests, and security.
EOF

# 3. Done!
```

### Example 2: PDF Processing with Scripts (3-4 hours)

**Original Skill Structure:**
```
skills/pdf-processor/
├── SKILL.md
└── scripts/
    ├── extract.py
    └── fill.py
```

**Conversion Steps:**
```bash
# 1. Create Power structure
mkdir -p converted-powers/pdf-processor/scripts
cp skills/pdf-processor/scripts/* converted-powers/pdf-processor/scripts/

# 2. Create Script Executor MCP
cat > converted-powers/pdf-processor/script_executor_mcp.py << 'EOF'
from mcp.server import Server
from mcp.types import Tool, TextContent
import subprocess
import sys
from pathlib import Path

app = Server("pdf-scripts")

SCRIPTS = {
    "pdf_extract": {
        "path": "scripts/extract.py",
        "description": "Extract PDF form data",
        "args": ["pdf_path"],
        "timeout": 30
    },
    "pdf_fill": {
        "path": "scripts/fill.py",
        "description": "Fill PDF forms",
        "args": ["template", "data", "output"],
        "timeout": 30
    }
}

@app.list_tools()
async def list_tools() -> list[Tool]:
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

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name not in SCRIPTS:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]
    
    config = SCRIPTS[name]
    cmd = [sys.executable, config["path"]] + [arguments[arg] for arg in config["args"]]
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=config["timeout"])
    return [TextContent(type="text", text=result.stdout if result.returncode == 0 else result.stderr)]

if __name__ == "__main__":
    import asyncio
    asyncio.run(app.run())
EOF

# 3. Create MCP configuration
cat > converted-powers/pdf-processor/mcp.json << 'EOF'
{
  "mcpServers": {
    "pdf-scripts": {
      "command": "python",
      "args": ["script_executor_mcp.py"]
    }
  }
}
EOF

# 4. Create POWER.md
cat > converted-powers/pdf-processor/POWER.md << 'EOF'
---
name: "pdf-processor"
displayName: "PDF Processor"
description: "Extract and fill PDF forms"
keywords: ["pdf", "form", "extract", "fill"]
author: "Your Name"
mcpServers:
  - pdf-scripts
---
# PDF Processing Power

## Tools
- **pdf_extract**: Extract form data
- **pdf_fill**: Fill PDF forms

## Usage
"Extract data from contract.pdf"
"Fill template.pdf with this data"
EOF

# 5. Test
cd converted-powers/pdf-processor
python script_executor_mcp.py
```

### Example 3: Batch Convert All Skills (1 hour)

```bash
# 1. Download conversion tool
# (Assuming tool is available)

# 2. Batch convert
for skill in ~/.claude/skills/*; do
    skill_name=$(basename "$skill")
    echo "Converting $skill_name..."
    python skill_to_power_converter.py \
        "$skill/SKILL.md" \
        "./converted-powers/$skill_name"
done

# 3. Review results
ls -la ./converted-powers/

# 4. Test each Power individually
```

## Common Commands

### Conversion Commands

```bash
# Convert single Skill
python skill_to_power_converter.py \
    ~/.claude/skills/my-skill/SKILL.md \
    ./converted-powers/my-skill

# Batch convert
./batch_convert_skills.sh ~/.claude/skills ./converted-powers

# Validate YAML
python -c "import yaml; yaml.safe_load(open('POWER.md').read().split('---')[1])"
```

### MCP Commands

```bash
# Test Script Executor MCP
python script_executor_mcp.py

# Test custom MCP server
python my_mcp_server.py

# Validate MCP config
python -c "import json; print(json.load(open('mcp.json')))"
```

### Debugging Commands

```bash
# Check Power structure
tree converted-powers/my-power/

# View frontmatter
head -n 20 converted-powers/my-power/POWER.md

# Test script execution
python scripts/my_script.py --test

# List MCP tools (in Kiro)
# Ask: "List all available MCP tools"
```

## Common Pitfalls

### ❌ Pitfall 1: Moving Scripts to Hooks

**Wrong:**
```bash
mv scripts/ hooks/  # ❌ Don't do this!
```

**Right:**
```bash
# Convert scripts to MCP tools
# Use Script Executor Pattern or create dedicated MCP
```

**Why:** Hooks are event-triggered, not on-demand like Skills scripts.

### ❌ Pitfall 2: Forgetting Keywords

**Wrong:**
```yaml
---
displayName: My Power
description: Does something useful
# ❌ Missing keywords
---
```

**Right:**
```yaml
---
displayName: My Power
description: Does something useful
keywords: ["keyword1", "keyword2"]  # ✅ Required!
---
```

### ❌ Pitfall 3: Using Absolute Paths

**Wrong:**
```json
{
  "scripts": {
    "my_script": {
      "path": "/absolute/path/script.py"  // ❌ Absolute
    }
  }
}
```

**Right:**
```json
{
  "scripts": {
    "my_script": {
      "path": "scripts/script.py"  // ✅ Relative
    }
  }
}
```

### ❌ Pitfall 4: Broad Keywords

**Wrong:**
```yaml
keywords: ["test", "debug", "help", "api"]  # ❌ Too generic
```

**Right:**
```yaml
keywords: ["pytest", "unit-test", "python-testing"]  # ✅ Specific
```

**Why:** Generic keywords cause false activations and annoy users.

## Progress Tracking Template

```markdown
# Skills Conversion Progress

## Statistics
- Total Skills: __
- Converted: __
- In Progress: __
- Pending: __

## Detailed List

| Skill Name | Type | Scripts | Approach | Status | Time | Notes |
|-----------|------|---------|----------|--------|------|-------|
| pr-reviewer | Doc | 0 | Simple | ✅ Done | 1h | - |
| pdf-processor | Scripts | 3 | Dedicated MCP | 🔄 In Progress | 3h | Testing |
| data-analyzer | Scripts | 8 | Script Executor | ⏳ Pending | 4h | - |
| code-formatter | Tools | 1 | Simple | ✅ Done | 0.5h | - |

## Next Steps
1. [ ] Complete pdf-processor MCP server
2. [ ] Start data-analyzer conversion
3. [ ] Test all converted Powers
```

## Time Estimates

| Skill Type | Conversion Time | Testing Time | Total |
|-----------|----------------|--------------|-------|
| Pure documentation | 1-2 hours | 30 min | 1.5-2.5 hours |
| 1-3 scripts (dedicated MCP) | 2-4 hours | 1 hour | 3-5 hours |
| 4-10 scripts (Script Executor) | 3-5 hours | 1 hour | 4-6 hours |
| 10+ scripts (modular MCP) | 1-2 days | 2-3 hours | 1.5-2.5 days |
| Complex integration | 2-5 days | 1 day | 3-6 days |

## Success Criteria

✅ **Conversion is successful when:**
- Power activates with correct keywords
- All tools/scripts work as expected
- Documentation is clear and complete
- No context performance issues
- Team can use it without training

✅ **Ready to share when:**
- Thoroughly tested in multiple scenarios
- Documentation includes examples
- Common errors documented
- Version controlled
- Team feedback incorporated

---

**Next Steps:**
- For detailed script conversion: Read `script-conversion.md`
- For installation migration: Read `installation-migration.md`
- For troubleshooting: Read `troubleshooting.md`
