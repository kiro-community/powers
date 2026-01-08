---
inclusion: manual
---

# OOXML Editing Guide

This guide covers editing existing PowerPoint presentations by working with the raw Office Open XML (OOXML) format.

## Overview

A .pptx file is essentially a ZIP archive containing XML files and other resources. To edit presentations at a deep level, you need to unpack the file, edit the XML content, and repack it.

**CRITICAL**: All OOXML operations MUST be performed using the MCP tools provided by this Power. DO NOT create Python scripts or run commands manually. The MCP server handles all script execution automatically.

## Reading and Analyzing Content

### Text Extraction
For simple text reading, use the inventory tool to extract text content from the presentation.

### Raw XML Access
For comments, speaker notes, slide layouts, animations, design elements, and complex formatting, you need raw XML access.

#### Unpacking a File
Use the `unpack` MCP tool to extract the OOXML structure:
- Provide the path to the .pptx file
- Specify an output directory where the XML files will be extracted
- The tool will unpack the presentation into its component XML files and resources

#### Key File Structures
- `ppt/presentation.xml` - Main presentation metadata and slide references
- `ppt/slides/slide{N}.xml` - Individual slide contents
- `ppt/notesSlides/notesSlide{N}.xml` - Speaker notes
- `ppt/comments/modernComment_*.xml` - Comments
- `ppt/slideLayouts/` - Layout templates
- `ppt/slideMasters/` - Master slide templates
- `ppt/theme/` - Theme and styling information
- `ppt/media/` - Images and other media files

#### Typography and Color Extraction
When analyzing an example design:
1. **Read theme file**: Check `ppt/theme/theme1.xml` for colors and fonts
2. **Sample slide content**: Examine `ppt/slides/slide1.xml` for actual usage
3. **Search for patterns**: Use grep to find color and font references

## Editing Workflow

**IMPORTANT**: Use MCP tools for ALL operations. DO NOT create or run Python scripts manually.

1. **Read ooxml.md**: Read the complete ooxml.md documentation file for detailed OOXML structure information
2. **Unpack**: Use the `unpack` MCP tool to extract the presentation to a directory
3. **Edit XML**: Modify `ppt/slides/slide{N}.xml` and related files using file editing tools
4. **Validate**: Use the `validate` MCP tool to check your changes
   - Provide the unpacked directory path
   - Provide the original .pptx file path for comparison
   - **CRITICAL**: Validate immediately after each edit
   - Fix any validation errors before proceeding
5. **Pack**: Use the `pack` MCP tool to create the final .pptx file from the edited directory

## Best Practices

- Always validate after each edit
- Keep backups of original files
- Test changes incrementally
- Use the validation script to catch errors early
- Understand the XML structure before making changes

## Common Use Cases

- Adding or modifying comments
- Editing speaker notes
- Changing slide layouts
- Modifying animations
- Adjusting design elements
- Complex formatting changes
