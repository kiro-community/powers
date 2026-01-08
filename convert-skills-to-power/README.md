# Convert Skills to Power

A comprehensive Kiro Power for converting Claude Agent Skills to Kiro Powers.

## What This Power Does

This Knowledge Base Power provides complete guidance for converting Claude Agent Skills to Kiro Powers, including:

- **Automated conversion strategies** for different Skill types
- **Script-to-MCP conversion** (the correct approach, not Hooks!)
- **Installation mechanism comparison** and migration strategies
- **Step-by-step workflows** with code examples
- **Troubleshooting guide** for common issues

## Power Type

**Knowledge Base Power** - No MCP server required. This is pure documentation and guidance.

## Installation

### Option 1: Install in Kiro (Recommended)

1. Open Kiro IDE
2. Click Kiro icon → Powers panel
3. Click "Add Custom Power"
4. Select "Local Directory"
5. Navigate to this directory: `powers/convert-skills-to-power`
6. Click "Add"

### Option 2: Copy to Powers Directory

```bash
# Copy to Kiro powers directory
cp -r powers/convert-skills-to-power ~/.kiro/powers/
```

## Usage

Once installed, activate this power by mentioning relevant keywords:

- "convert skills"
- "skill migration"
- "claude to kiro"
- "skill conversion"

Then ask for specific guidance:

- "How do I convert a Skill with scripts?"
- "Show me the quick start guide"
- "What's the installation migration strategy?"
- "Help me troubleshoot conversion issues"

## Available Steering Files

This power includes four comprehensive guides:

1. **quick-start.md** - 5-minute decision flow and conversion checklist
2. **script-conversion.md** - Detailed guide for converting Skills scripts to MCP tools
3. **installation-migration.md** - Installation mechanism comparison and migration strategies
4. **troubleshooting.md** - Common conversion issues and solutions

## Key Insights

### Critical: Scripts → MCP Tools, Not Hooks!

**Why?**
- Skills scripts are **on-demand** (AI decides when to run)
- Hooks are **event-triggered** (automatic on file save, etc.)
- MCP tools preserve zero-context execution
- MCP tools support on-demand invocation

### Conversion Options

| Scripts | Recommended Approach | Time |
|---------|---------------------|------|
| 1-3 scripts | Dedicated MCP server | 2-4 hours |
| 4-10 scripts | Script Executor Pattern | 3-5 hours |
| 10+ scripts | Modular MCP server | 1-2 days |

### Installation Comparison

| Feature | Claude Skills | Kiro Powers |
|---------|--------------|-------------|
| Installation | Manual files | One-click |
| Time | 5-10 minutes | 30 seconds |
| Restart | Required | Not required |
| Versions | Manual | Automatic |
| Market | None | Official + community |

## Structure

```
convert-skills-to-power/
├── POWER.md                          # Main documentation
├── README.md                         # This file
└── steering/
    ├── quick-start.md                # Quick start guide
    ├── script-conversion.md          # Script conversion details
    ├── installation-migration.md     # Installation strategies
    └── troubleshooting.md            # Common issues
```

## Testing

After installation, test the power:

1. **Test activation:**
   ```
   "Help me convert skills to powers"
   ```
   Power should activate and provide overview.

2. **Test steering files:**
   ```
   "Show me the quick start guide"
   ```
   Should load quick-start.md content.

3. **Test specific queries:**
   ```
   "How do I convert scripts to MCP tools?"
   ```
   Should provide relevant guidance.

## Contributing

This power is based on comprehensive research comparing Claude Skills and Kiro Powers. If you find issues or have suggestions:

1. Document the issue clearly
2. Provide examples if possible
3. Suggest improvements
4. Share your conversion experiences

## Resources

### Related Documentation
- [Claude Skills Official Docs](https://code.claude.com/docs/en/skills)
- [Kiro Powers Documentation](https://kiro.dev/docs/powers/)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)

### Tools
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [MCP Servers Directory](https://mcpservers.org/)

## License

This power is provided as-is for educational and practical use in converting Claude Skills to Kiro Powers.

## Version

**Version:** 1.0.0  
**Last Updated:** 2026-01-04  
**Author:** Kiro Community

---

**Ready to convert your Skills?** Install this power and start with the quick-start guide!
