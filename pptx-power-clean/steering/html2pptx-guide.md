---
inclusion: manual
---

# HTML to PowerPoint Conversion Guide

This guide covers converting HTML slides to PowerPoint presentations using the html2pptx MCP tool.

**Prerequisites:** This guide assumes you already have HTML slide files ready for conversion. If you're starting from a user request, see `user-request-to-html.md` first to create and get approval for an HTML preview.

## Design Principles

**CRITICAL**: Before creating any presentation, analyze the content and choose appropriate design elements:

1. **Consider the subject matter**: What is this presentation about? What tone, industry, or mood does it suggest?
2. **Check for branding**: If the user mentions a company/organization, consider their brand colors and identity
3. **Match palette to content**: Select colors that reflect the subject
4. **State your approach**: Explain your design choices before writing code

**Requirements**:
- ✅ State your content-informed design approach BEFORE writing code
- ✅ Use web-safe fonts only: Arial, Helvetica, Times New Roman, Georgia, Courier New, Verdana, Tahoma, Trebuchet MS, Impact
- ✅ Create clear visual hierarchy through size, weight, and color
- ✅ Ensure readability: strong contrast, appropriately sized text, clean alignment
- ✅ Be consistent: repeat patterns, spacing, and visual language across slides

## Color Palette Selection

**Choosing colors creatively**:
- **Think beyond defaults**: What colors genuinely match this specific topic?
- **Consider multiple angles**: Topic, industry, mood, energy level, target audience, brand identity
- **Be adventurous**: Try unexpected combinations
- **Build your palette**: Pick 3-5 colors that work together
- **Ensure contrast**: Text must be clearly readable on backgrounds

**Example color palettes**:

1. **Classic Blue**: Deep navy (#1C2833), slate gray (#2E4053), silver (#AAB7B8), off-white (#F4F6F6)
2. **Teal & Coral**: Teal (#5EA8A7), deep teal (#277884), coral (#FE4447), white (#FFFFFF)
3. **Bold Red**: Red (#C0392B), bright red (#E74C3C), orange (#F39C12), yellow (#F1C40F), green (#2ECC71)
4. **Warm Blush**: Mauve (#A49393), blush (#EED6D3), rose (#E8B4B8), cream (#FAF7F2)
5. **Burgundy Luxury**: Burgundy (#5D1D2E), crimson (#951233), rust (#C15937), gold (#997929)
6. **Deep Purple & Emerald**: Purple (#B165FB), dark blue (#181B24), emerald (#40695B), white (#FFFFFF)
7. **Cream & Forest Green**: Cream (#FFE1C7), forest green (#40695B), white (#FCFCFC)
8. **Pink & Purple**: Pink (#F8275B), coral (#FF574A), rose (#FF737D), purple (#3D2F68)
9. **Lime & Plum**: Lime (#C5DE82), plum (#7C3A5F), coral (#FD8C6E), blue-gray (#98ACB5)
10. **Black & Gold**: Gold (#BF9A4A), black (#000000), cream (#F4F6F6)

## Layout Tips

**When creating slides with charts or tables:**
- **Two-column layout (PREFERRED)**: Header spanning full width, then two columns - text/bullets in one, featured content in the other
- **Full-slide layout**: Let the featured content take up the entire slide for maximum impact
- **NEVER vertically stack**: Do not place charts/tables below text in a single column

## Workflow

**IMPORTANT**: This power provides MCP tools. Do NOT write scripts manually - use the MCP tools instead.

**Prerequisites**: Before using this guide, you should have:
- HTML preview approved by user (see `user-request-to-html.md`)
- Individual HTML slide files ready for conversion (720pt × 405pt)

### Step 1: Prepare Individual Slide Files

After user approves the preview, create individual HTML files for each slide.

**CRITICAL: File Organization**

All presentation files MUST be organized in a dedicated folder:

```
[presentation-name]/
├── preview.html                    # The approved preview
├── slide1.html                     # Individual slides
├── slide2.html
├── slide3.html
├── ...
├── [presentation-name].pptx        # Final output
└── [presentation-name]-thumbnails.jpg  # Validation thumbnails
```

**Example:**
```
ai-agents-presentation/
├── preview.html
├── slide1.html
├── slide2.html
├── slide3.html
├── slide4.html
├── slide5.html
├── slide6.html
├── slide7.html
├── slide8.html
├── ai-agents-presentation.pptx
└── ai-agents-presentation-thumbnails.jpg
```

**File naming rules:**
- Folder name: Use kebab-case (lowercase with hyphens)
- Slide files: `slide1.html`, `slide2.html`, etc. (sequential numbering)
- Preview: `preview.html`
- Output PPTX: `[presentation-name].pptx` (matches folder name)
- Thumbnails: `[presentation-name]-thumbnails.jpg`

**Dimension conversion from preview:**
```
Preview: 960px × 540px (for easy reading)
Slide files: 720pt × 405pt (for PPTX conversion)

Font size adjustment:
- Preview h1: 36pt → Slide h1: 14-18pt
- Preview p: 18pt → Slide p: 8-12pt
```

**Requirements:**
- Use `<p>`, `<h1>`-`<h6>`, `<ul>`, `<ol>` for all text content
- Use `class="placeholder"` for areas where charts/tables will be added
- **CRITICAL**: Rasterize gradients and icons as PNG images FIRST using Sharp
- Match the content from the approved preview
- Adjust font sizes for the smaller dimensions

### Step 2: Convert to PowerPoint using MCP tool
   
**Use the `html2pptx` MCP tool** - Do NOT create Node.js scripts manually.
   
Example usage:
```
"Use the html2pptx tool to convert these HTML files to PowerPoint:
- ai-agents-presentation/slide1.html
- ai-agents-presentation/slide2.html
- ai-agents-presentation/slide3.html
- ai-agents-presentation/slide4.html
- ai-agents-presentation/slide5.html
- ai-agents-presentation/slide6.html
- ai-agents-presentation/slide7.html
- ai-agents-presentation/slide8.html
Output file: ai-agents-presentation/ai-agents-presentation.pptx"
```
   
The MCP tool will:
- Process each HTML file
- Convert to PowerPoint slides
- Save as .pptx file in the same folder

### Step 3: Visual validation

Generate thumbnails using the `thumbnail` MCP tool
   
Example:
```
"Use the thumbnail tool to generate thumbnails for ai-agents-presentation/ai-agents-presentation.pptx"
```

## Handling Validation Errors

**CRITICAL**: When html2pptx reports validation errors, calculate the correct dimensions ONCE instead of iterating.

### Common Error: Content Overflow

**Error message format:**
```
HTML content overflows body by XXpt horizontally and YYpt vertically
```

**How to fix in ONE step:**

1. **Parse the error message** to extract overflow amounts:
   - Horizontal overflow: XXpt
   - Vertical overflow: YYpt

2. **Calculate new dimensions**:
   ```
   Current body: width: 720pt; height: 405pt
   Current padding: padding: 0pt 15pt 36pt 15pt (top right bottom left)
   
   Available content area:
   - Width: 720pt - 15pt (left) - 15pt (right) = 690pt
   - Height: 405pt - 0pt (top) - 36pt (bottom) = 369pt
   
   If overflow is XXpt horizontally and YYpt vertically:
   - Reduce font sizes proportionally
   - Or increase padding to constrain content
   - Or reduce content amount
   ```

3. **Calculate font size reduction**:
   ```
   If content overflows by XXpt horizontally:
   - Reduction factor = (690pt - XXpt) / 690pt
   - New font size = current font size × reduction factor
   
   Example:
   - Overflow: 69pt horizontally, 55.5pt vertically
   - Horizontal reduction: (690 - 69) / 690 = 0.90 (reduce by 10%)
   - Vertical reduction: (369 - 55.5) / 369 = 0.85 (reduce by 15%)
   - Use the larger reduction: 15%
   - If h1 was 14pt: 14pt × 0.85 = 11.9pt → use 12pt
   - If p was 8pt: 8pt × 0.85 = 6.8pt → use 7pt
   ```

4. **Apply changes to ALL slides at once**:
   - Update font sizes in the `<style>` section
   - Apply the same reduction to all text elements
   - Ensure consistency across all slides

**DO NOT:**
- ❌ Make small incremental changes (reducing by 1-2pt at a time)
- ❌ Only fix one slide and test again
- ❌ Iterate multiple times with trial and error

**DO:**
- ✅ Calculate the exact reduction needed from the error message
- ✅ Apply the reduction to all slides simultaneously
- ✅ Round font sizes to reasonable values (avoid 6.8pt, use 7pt)
- ✅ Maintain visual hierarchy (keep relative size differences)

### Example: Complete Fix

**Error:**
```
HTML content overflows body by 69.0pt horizontally and 55.5pt vertically
```

**Analysis:**
```
Available width: 690pt (720pt - 30pt padding)
Available height: 369pt (405pt - 36pt padding)
Overflow: 69pt horizontal (10% over), 55.5pt vertical (15% over)
Required reduction: 15% (use the larger percentage)
```

**Original styles:**
```css
h1 { font-size: 14pt; }
p { font-size: 8pt; }
.source { font-size: 7pt; }
```

**Corrected styles (15% reduction):**
```css
h1 { font-size: 12pt; }  /* 14pt × 0.85 = 11.9pt → 12pt */
p { font-size: 7pt; }    /* 8pt × 0.85 = 6.8pt → 7pt */
.source { font-size: 6pt; }  /* 7pt × 0.85 = 5.95pt → 6pt */
```

**Apply to all 8 slides at once**, then test again.

## Using MCP Tools

**Available MCP tools for this workflow:**

### html2pptx
Convert HTML slides to PowerPoint presentation.

**How to use:**
```
"Use the html2pptx tool with these parameters:
- html_files: ['slide1.html', 'slide2.html', 'slide3.html']
- output_file: 'presentation.pptx'"
```

### thumbnail
Generate visual thumbnail grids for validation.

**How to use:**
```
"Use the thumbnail tool to generate thumbnails for presentation.pptx with 4 columns"
```

**DO NOT:**
- ❌ Create Node.js scripts manually
- ❌ Try to install pptxgenjs yourself
- ❌ Write conversion code

**DO:**
- ✅ Use the html2pptx MCP tool
- ✅ Provide HTML files and output path
- ✅ Let the MCP tool handle the conversion

## Visual Details Options

**Geometric Patterns**:
- Diagonal section dividers instead of horizontal
- Asymmetric column widths (30/70, 40/60, 25/75)
- Rotated text headers at 90° or 270°
- Circular/hexagonal frames for images
- Triangular accent shapes in corners

**Border & Frame Treatments**:
- Thick single-color borders (10-20pt) on one side only
- Double-line borders with contrasting colors
- Corner brackets instead of full frames
- L-shaped borders (top+left or bottom+right)

**Typography Treatments**:
- Extreme size contrast (72pt headlines vs 11pt body)
- All-caps headers with wide letter spacing
- Numbered sections in oversized display type
- Monospace (Courier New) for data/stats/technical content

**Chart & Data Styling**:
- Monochrome charts with single accent color for key data
- Horizontal bar charts instead of vertical
- Minimal gridlines or none at all
- Data labels directly on elements (no legends)
- Oversized numbers for key metrics

## Code Style Guidelines

**IMPORTANT**: When generating code for PPTX operations:
- Write concise code
- Avoid verbose variable names and redundant operations
- Avoid unnecessary print statements
