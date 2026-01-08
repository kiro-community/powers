---
inclusion: manual
---

# Template-Based Presentation Creation

This guide covers creating presentations using existing templates by duplicating and rearranging slides, then replacing content.

## Overview

When you need to create a presentation that follows an existing template's design, use this workflow to duplicate template slides, rearrange them, and replace placeholder content.

## Workflow Steps

### 1. Extract Template Content and Create Thumbnails

**Extract text**: Use the `inventory` MCP tool to extract text content from the template presentation.

**Create thumbnail grids**: Use the `thumbnail` MCP tool to generate visual thumbnails for the template.

Example:
```
"Use the thumbnail tool to generate thumbnails for template.pptx"
```

Review the extracted content to understand the template structure.

### 2. Analyze Template and Save Inventory

**Visual Analysis**: Review thumbnail grids to understand:
- Slide layouts and design patterns
- Visual structure and hierarchy
- Image placeholder locations

**Create template inventory** at `template-inventory.md`:
```markdown
# Template Inventory Analysis
**Total Slides: [count]**
**IMPORTANT: Slides are 0-indexed (first slide = 0, last slide = count-1)**

## [Category Name]
- Slide 0: [Layout code] - Description/purpose
- Slide 1: [Layout code] - Description/purpose
[... EVERY slide must be listed individually ...]
```

### 3. Create Presentation Outline

**CRITICAL: Match layout structure to actual content**:
- Single-column layouts: Use for unified narrative or single topic
- Two-column layouts: Use ONLY when you have exactly 2 distinct items
- Three-column layouts: Use ONLY when you have exactly 3 distinct items
- Image + text layouts: Use ONLY when you have actual images
- Quote layouts: Use ONLY for actual quotes with attribution
- Never use layouts with more placeholders than you have content

**Count your content pieces BEFORE selecting the layout**

Save `outline.md` with content AND template mapping:
```python
# Template slides to use (0-based indexing)
# WARNING: Verify indices are within range!
template_mapping = [
    0,   # Use slide 0 (Title/Cover)
    34,  # Use slide 34 (B1: Title and body)
    34,  # Use slide 34 again (duplicate)
    50,  # Use slide 50 (E1: Quote)
]
```

### 4. Rearrange Slides

**Use the `rearrange` MCP tool** - Do NOT run Python scripts directly.

Example:
```
"Use the rearrange tool on template.pptx with slide indices 0,34,34,50,52 and save to working.pptx"
```

The MCP tool will:
- Duplicate slides as needed (e.g., slide 34 appears twice)
- Reorder slides in the specified sequence
- Delete unused slides automatically
- Save the result to working.pptx

**Note:** Slide indices are 0-based (first slide is 0, second is 1, etc.)

### 5. Extract Text Inventory

**Use the `inventory` MCP tool** - Do NOT run Python scripts directly.

Example:
```
"Use the inventory tool to extract text from working.pptx and save to text-inventory.json"
```

The MCP tool will extract all text shapes and their properties, saving them to a JSON file.

Read the complete text-inventory.json file to understand all shapes and properties.

**Inventory JSON structure**:
```json
{
  "slide-0": {
    "shape-0": {
      "placeholder_type": "TITLE",
      "left": 1.5,
      "top": 2.0,
      "width": 7.5,
      "height": 1.2,
      "paragraphs": [
        {
          "text": "Paragraph text",
          "bullet": true,
          "level": 0,
          "alignment": "CENTER",
          "font_name": "Arial",
          "font_size": 14.0,
          "bold": true,
          "color": "FF0000"
        }
      ]
    }
  }
}
```

### 6. Generate Replacement Text

**CRITICAL validation**:
- First verify which shapes exist in the inventory
- Only reference shapes that are actually present
- The replace.py script validates all shapes exist

**AUTOMATIC CLEARING**:
- ALL text shapes from inventory will be cleared
- Only shapes with "paragraphs" in replacement JSON get new content
- Shapes without "paragraphs" are cleared automatically

**ESSENTIAL FORMATTING RULES**:
- Headers/titles should have `"bold": true`
- List items should have `"bullet": true, "level": 0`
- Preserve alignment properties (e.g., `"alignment": "CENTER"`)
- Include font properties when different from default
- Colors: Use `"color": "FF0000"` for RGB or `"theme_color": "DARK_1"` for theme colors
- **IMPORTANT**: When bullet: true, do NOT include bullet symbols in text

**Example paragraphs**:
```json
"paragraphs": [
  {
    "text": "New presentation title",
    "alignment": "CENTER",
    "bold": true
  },
  {
    "text": "First bullet point",
    "bullet": true,
    "level": 0
  },
  {
    "text": "Red colored text",
    "color": "FF0000"
  }
]
```

Save to `replacement-text.json`.

### 7. Apply Replacements

**Use the `replace` MCP tool** - Do NOT run Python scripts directly.

Example:
```
"Use the replace tool to update working.pptx with replacements from replacement-text.json, save to output.pptx"
```

The MCP tool will:
- Extract inventory of ALL text shapes
- Validate all shapes in replacement JSON exist
- Clear text from ALL shapes
- Apply new text to shapes with "paragraphs"
- Preserve formatting from JSON properties

## Creating Thumbnail Grids

Use the `thumbnail` MCP tool to create visual grids of presentation slides.

Example:
```
"Use the thumbnail tool on template.pptx with 5 columns and save with prefix 'template-grid'"
```

**Features**:
- Default: 5 columns, max 30 slides per grid
- Custom columns: Specify between 3-6 columns
- Slides are zero-indexed

**Use cases**:
- Template analysis
- Content review
- Navigation reference
- Quality check

## Converting Slides to Images

**IMPORTANT**: For converting slides to images, you'll need to use external tools that are not part of this Power:

1. Convert PPTX to PDF using LibreOffice:
   - Install LibreOffice if not already installed
   - Use: `soffice --headless --convert-to pdf template.pptx`

2. Convert PDF to JPEG using Poppler:
   - Install Poppler if not already installed
   - Use: `pdftoppm -jpeg -r 150 template.pdf slide`

This creates files like `slide-1.jpg`, `slide-2.jpg`, etc.

Note: These are external dependencies not managed by the PPTX Power MCP server.
